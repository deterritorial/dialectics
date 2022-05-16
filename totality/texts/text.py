#print(__file__,'imported')
from totality.imports import *
log = Log()




def Text(id=None, _corpus=None, _force=False, **kwargs):
    global TEXT_CACHE
    from totality.corpora import Corpus

    if not _corpus and is_text_obj(id): return id
    
    keys = TextKeys(id=id, _corpus=_corpus, **kwargs)
    addr = keys.get(COL_ADDR)
    if not _force and addr in TEXT_CACHE:
        t = TEXT_CACHE[addr]
    else:
        corp,id=keys.get(COL_CORPUS),keys.get(COL_ID)
        t = Corpus(corp).text(id,**kwargs)
        TEXT_CACHE[t.addr] = TEXT_CACHE[t._id] = TEXT_CACHE[t._key] = t
    
    return t


class BaseText(BaseObject):
    __COLLECTION__=TEXT_COLLECTION_NAME

    def __init__(self,id=None,_corpus=None,_source=None,**kwargs):
        self._keys=TextKeys(id=id,_corpus=_corpus,_source=_source,**kwargs)
        self._data=kwargs
        self._node=None

    @property
    def paths(self):
        pathd={}
        pathd['corpus']=os.path.join(PATH_CORPORA,self._corpus)
        pathd['root']=os.path.join(pathd['corpus'],'texts',self.id)
        pathd['txt']=os.path.join(pathd['root'],'text.txt')
        pathd['txt_']=os.path.join(pathd['corpus'],'txt',self.id+'.txt')
        return pathd


    # def __str__(self):
        # return f"Text('{self._addr}')"

    def __repr__(self):
        return self.nice
    
    def is_valid(self):
        return self.addr and is_addr(self.addr)

    @property
    def nice(self,force=True):
        if not self.is_valid(): return ''
        yr,au,ti,addr = self.yr, self.au, self.ti, self.addr
        austr=f"{au}, " if au else ""
        tistr=f"{ti.upper()[:50].strip()} " if ti else ""
        yrstr=f"({int(yr)}) " if safebool(yr) else ""
        addrstr=f"[{addr}] <{self._key}>"
        return ''.join([austr,tistr,yrstr,addrstr])

    def __getattr__(self,key):
        res = super().__getattr__(key)
        if res is not None: return res

        dicts = [(self,'_keys'), (self,'_data')]
        for obj,attrname in dicts:
            if hasattr(obj,attrname):
                attr=getattr(obj,attrname)
                if is_dictish(attr) and key in attr:
                    res = attr.get(key)
                    if res is not None:
                        return res

        if hasattr(self,'_data') and is_dictish(self._data) and key in self._data:
            res = self._data.get(key)
            if res is not None: return res
        
        return None


    @property
    def au(self):
        return zeropunc(to_lastname(self.author))
    @property
    def ti(self): return to_shorttitle(self.title)
    @property
    def yr(self): return pd.to_numeric(self.year,errors='coerce')
    

    @property
    def _meta(self):
        return self.ensure_id(just_meta(self._data))

    @property
    def meta(self): return self.metadata() #just_meta_no_id(self._meta) #metadata()
    def metadata(self,sources=True,stamp_source=False,**kwargs):
        meta = OrderedSetDict()
        for k,v in just_meta_no_id(self._data).items(): meta[k]=v
        if sources:
            for src in self.copies():
                for k,v in just_meta_no_id(src._data).items():
                    mk=k if not stamp_source else k+'__'+src._corpus
                    meta[mk]=v
        odx={k:v for k,v in sorted(meta.to_dict().items())}
        return self.ensure_id(odx)

    def metadata_srcs(self,sources=True,**kwargs):
        dds={}
        meta_srcs = [self] + (list(self.copies()) if sources else [])
        for src in meta_srcs:
            for k,v in just_meta_no_id(src._data).items():
                if not k in dds: dds[k]={}
                if not v in dds[k]: dds[k][v]=set()
                dds[k][v]|={src._corpus}
        odx={k:v for k,v in sorted(dds.items())}
        return self.ensure_id(odx)






    data=_meta
    @property
    def _params(self): return self.ensure_id(just_params(self._data))
    @property
    def addr(self): return to_addr(self._corpus, self.id)
    _addr=addr
    @property
    def corpus(self):
        if self._corpusobj is not None:
            from totality.corpora import Corpus
            self._corpusobj=Corpus(self._corpus) 
        return self._corpusobj
    
    
    @property
    def _qmeta(self):
        return {
            'au':self.au,
            'ti':self.ti,
            'yr':self.yr,
        }

    def ensure_id(self,d={},idkey='_id',**kwargs):
        newmeta=just_meta(merge_dict(self._data, d, kwargs))
        return merge_dict(
            self._keys,
            self._qmeta,
            newmeta,
        )

    def copies(self,find_if_nec=True):
        from arango import GraphTraverseError
        try:
            return self.ties(rel=MATCHRELNAME)
        except GraphTraverseError:
            if find_if_nec:
                self.find_copies()
                return self.copies(find_if_nec=False)
        return []

    def find_copies(self):
        if self.au:
            tl = self.tspace.find(au=self.au)
            mdf = tl.match(self)
        return self.copies(find_if_nec=False)



    @property
    def coll(self): return Textspace().coll
    collection=coll
    
    ## database funcs
    def load(self,force=False):
        if force or not self._loadd:
            data = self.coll.get(self._key)
            if data: self._data={**self._data,**just_meta(data)}
            self._loadd=True

    def update(self,**meta):
        #meta1=self._meta
        for k,v in meta.items(): self._data[k]=v
        #meta2=self._meta
        # if meta1!=meta2:
            # if log: log(f'updating db record for {self}')
            # self.save()
        
    def init(self,force=False,**kwargs):
        self.load(force=force)
        self.update(**kwargs)
        return self
    
    def exists(self):
        return self._key in self.collection
    
    def upsert(self,d={},tryagain=True):
        to_insert = safebool(safejson(self.ensure_id(d)))
        saved_meta={}
        try:
            saved_meta = self.coll.update(to_insert)
        except Exception as e:
            if log>2: log.error(e)
            try:
                saved_meta = self.coll.insert(to_insert)
            except Exception as e:
                if log: log.error(f'{e}. d = {to_insert}')
        if log>1: log(saved_meta)
        return {**to_insert, **saved_meta}
        
    
    def save(self):
        # with Log(f'Saving {self} in database')
        saved_meta=self.upsert()
        if not saved_meta: return
        assert saved_meta['_key'] == self._key
        self._data = {**self._data, **just_meta(saved_meta)}
        return saved_meta

    





    ### RELATIONS


    def relate(self,other,rel=MATCHRELNAME,rel_type='',yn='',**kwargs):
        from totality.database import Relspace
        other = Text(other)
        return Relspace().link(self,other,rel=rel,rel_type=rel_type,yn=yn,**just_meta_no_id(kwargs))
    
    def strong_ties(self, relspace='is_also', data=False, direction=None):
        from .textlist import TextList

        rs = Relspace(relspace)
        res=rs.graph.edges(rs.name, self._id, direction=direction)
        if type(res)!=dict or not res: return []
        res = res.get('edges')
        if type(res)!=list: return []
        
        ## otherwise
        me_id = self._id
        o=[]
        for d in res:
            you_id = d.get('_from') if d.get('_from')!=me_id else d.get('_to')
            u=self
            v=Textspace().get(you_id)
            o.append((v,d) if data else v)
        return o if not data else o
    neighbors=strong_ties
        
    def traverse_ties(self,
            direction="any",
            strategy="depthfirst",
            max_depth=2,
            rel=MATCHRELNAME,
            **kwargs):
        from .textlist import TextList
        
        return Relspace().graph.traverse(
            start_vertex=self._id,
            direction=direction,
            max_depth=max_depth,
            strategy=strategy,
            **kwargs
        )

    def all_ties(self,data=False,rel=MATCHRELNAME,**kwargs):
        traversal_data = self.traverse_ties(**kwargs)
        o=set()
        dd={
            vertexd.get('_id'):vertexd
            for vertexd in traversal_data.get('vertices',[])
        }
        for pathd in traversal_data.get('paths',[]):
            for edged in pathd.get('edges'):
                if not rel or edged.get('rel') == rel:
                    for _id in [edged.get('_from'), edged.get('_to')]:
                        if _id and _id in dd:
                            td = dd[_id]
                            t = Text(td)
                            o|={t}
        return o
    
    
    def ties(self, only_strong=False, rel=MATCHRELNAME, allow_tmp=False, **kwargs):
        o = self.strong_ties() if only_strong else self.all_ties()
        if o and not allow_tmp: o = {t for t in o if t._corpus != TMP_CORPUS}
        return o

    def weak_ties(self,data=False,**kwargs):
        from .textlist import TextList

        all_ties = self.all_ties(data=data,**kwargs)
        if log: log(f'all_tues = {all_ties}')
        
        strong_ties = set(self.strong_ties())
        if log: log(f'strong_ties = {strong_ties}')
        
        weak_ties = all_ties - strong_ties - {self}
        if log: log(f'weak+ties = {weak_ties}')
        
        return weak_ties if not data else [(t,{}) for t in weak_ties]

    def graph_ties(self,allow_tmp=False, node_repr='nice', **kwargs):
        import networkx as nx
        g=nx.DiGraph()
        traversal_data = self.traverse_ties(**kwargs)
        dd={
            vertexd.get('_id'):vertexd
            for vertexd in traversal_data.get('vertices',[])
        }
        for pathd in traversal_data.get('paths',[]):
            for edged in pathd.get('edges'):
                d1=dd.get(edged.get('_from',''),{})
                d2=dd.get(edged.get('_to',''),{})
                if d1 and d2:
                    t1=Text(d1)
                    t2=Text(d2)
                    if not hasattr(t1,node_repr) or not hasattr(t2,node_repr):
                        log.error('??')
                        continue

                    ts={t1,t2}-{self}
                    cs={tx._corpus for tx in ts}
                    if allow_tmp or not {TMP_CORPUS}&cs:
                        g.add_edge(getattr(t1,node_repr), getattr(t2,node_repr), **edged)
        return g

    def draw_ties(self,g=None,**kwargs):
        from totality.models.networks import draw_nx
        if g is None: g=self.graph_ties(**kwargs)
        return draw_nx(g)
        
    def sources(self): return self.ties()




    def get_txt(self,sources=True):
        if self._txt: return self._txt
        for pathtype,path in self.paths.items():
            if pathtype.startswith('txt') and os.path.exists(path):
                txt=readtxt(path)
                if txt: 
                    return txt
        
        if sources:
            for src in self.strong_ties():
                txt=src.get_txt(sources=False)
                if txt: return txt
        
        return ''

    @property
    def txt(self): return self.get_txt()

    def tokens(self,tokenizer=tokenize_fast,lower=True,sources=True):
        txt=self.get_txt(sources=sources)
        return tokenizer(txt.lower() if lower else txt)

    def counts(self,tokens=None,**kwargs):
        if not tokens: tokens=self.tokens(**kwargs)
        return Counter(tokens)



    def minhash(self,cache=True,force=False):
        if not self._minhash:
            words = self.tokens(sources=False)
            if not words: return None
            
            from datasketch import MinHash
            self._minhash = m = MinHash(num_perm=HASH_NUMPERM)
            for word in self.tokens(): m.update(word.encode('utf-8'))
        return self._minhash

    def hashdist(self,text,cache=True):
        m1=self.minhash(cache=cache)
        m2=text.minhash(cache=cache)
        return 1 - m1.jaccard(m2)


