#print(__file__,'imported')
from intertxt.imports import *
log = Log()



TEXT_CACHE={}
TMP_CORPUS='tmp'




def Text(id=None, _corpus=None, _force=False, **kwargs):
    global TEXT_CACHE
    from intertxt.corpora import Corpus

    if not _corpus and is_text_obj(id): return id
    
    keys = TextKeys(id=id, _corpus=_corpus, **kwargs)
    addr = keys.get(COL_ADDR)
    if not _force and addr in TEXT_CACHE:
        t = TEXT_CACHE[addr].init(**kwargs)
    else:
        corp,id=keys.get(COL_CORPUS),keys.get(COL_ID)
        t = TEXT_CACHE[addr] = Corpus(corp).text(id,**kwargs)
    
    return t


class BaseText(BaseObject):
    __COLLECTION__=TEXT_COLLECTION_NAME

    def __init__(self,id=None,_corpus=None,_source=None,**kwargs):
        self._keys=TextKeys(id=id,_corpus=_corpus,_source=_source,**kwargs)
        self._data=kwargs
        self._node=None

    def __str__(self):
        return f"Text('{self._addr}')"

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
        addrstr=f"[{addr}]"
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
    meta=_meta
    data=_meta
    @property
    def _params(self): return self.ensure_id(just_params(self._data))
    @property
    def addr(self): return to_addr(self._corpus, self.id)
    _addr=addr
    @property
    def corpus(self):
        if not self._corpusobj:
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
        other = Text(other)
        
        # odx={
            
        # }














