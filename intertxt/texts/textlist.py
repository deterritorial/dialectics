from intertxt.imports import *
from collections import UserList
from .text import Text

class TextList(BaseObject, UserList):
    def __init__(self, l=[],unique=True):
        self.unique = unique
        self.data_all = list(map(Text,l))
        self._g=None
        self.sort()

    def sort(self):
        self.data_all.sort(key=lambda t: t.yr)
        return self

    @property
    def data(self):
        o=None
        if self.unique and self._data_uniq: o=self._data_uniq
        if not o: o=self.data_all
        if not o: o=[]
        return sorted(o,key=lambda t: t.year)
    
    @property
    def data_uniq(self):
        if not self._data_uniq: self.filter()
        return self._data_uniq
    uniq=data_uniq

    def __iter__(self): yield from self.data
    def __len__(self): return len(self.data_all)

    def __repr__(self,maxnum=25):
        pref='TextList('
        iterr = self.data
        o=[]
        for i,t in enumerate(sorted(iterr,key=lambda t: t.year)):
            if i:
                prefx=' '*(len(pref)+1)
            else:
                prefx='['
            o+=[prefx + repr(t)]
        o='\n'.join(o)
        if o: return pref + o + '])'
        return f'[TextList]({len(self.data_all)} texts)'
    
    @property
    def addrs(self): return [t.addr for t in self.data_all]
    
    

    def filter(self,text_iter=None,**kwargs):
        if text_iter is None: text_iter = self.data_all
        self._data_uniq = sorted(
            list(self.iter_texts_uniq(self.data_all,**kwargs)),
            key=lambda t: t.year
        )
        if log:
            log(f'data_all={len(self.data_all)}, _data_uniq={len(self._data_uniq)}')
        return self._data_uniq
    filtered=filter
    
    def iter_texts(self,text_iter=None,_unique=True,**kwargs):
        if _unique and self._data_uniq:
            yield from self._data_uniq
        else:
            yield from self.data_all


    def iter_texts_uniq(
            self,
            progress=False,
            force=True,
            force_inner=True,
            desc='[LLTK] iterating distinct texts',
            leave=True,
            **kwargs):

        if False: #not force and self._data_uniq:
            yield from self._data_uniq
        else:
            self._g = g = self.get_matchgraph() if (True or not self._g) else self._g
            if log: log(f'<- matchgraph! = {g}')
            if g and isinstance(g,nx.Graph):
                cmps=list(nx.connected_components(g))
                if 0: cmps=get_tqdm(cmps,desc=desc,leave=leave)
                for i,nodeset in enumerate(cmps):
                    nset=list(nodeset)
                    nset.sort(key=lambda x: CORPUS_SOURCE_RANKS.get(to_corpus_and_id(x)[0],1000))
                    t=Text(nset[0])
                    if log: log(f'{i} {t}')
                    if 0: cmps.set_description(f'{desc}: {t}')
                    yield t


    def quiet(self): self.progress=False
    def verbose(self): self.progress=True

        
        

    @property
    def t(self): return random.choice(self.data)

    def sample(self,n): 
        if n < len(self.data): return random.sample(self.data,n)
        o = [x for x in self.data]
        random.shuffle(o)
        return o


    def run(self,func,text_iter=None,*args,**kwargs):
        return llmap(
            self.addrs,
            func,
            *args,
            **kwargs
        )
    map = run
                
    def get_matchgraph(self,node_name='addr'):
        g = nx.Graph()
        for t in self.data_all:
            tg=t.matchgraph(draw=False,node_name='addr')
            g = nx.compose(g,tg)

        for node in list(g.nodes()):
            if IDSEP_START+TMP_CORPUS_ID+IDSEP in node:
                g.remove_node(node)

        if node_name!='addr':
            labeld=dict((addr,Text(addr).node) for addr in g.nodes())
            nx.relabel_nodes(g,labeld,copy=False)
        return g
        

    def matchgraph(self,draw=True,node_name='node',**kwargs):
        from lltk.model.networks import draw_nx
        g=self.get_matchgraph(node_name=node_name)
        return g if g is None or not draw else draw_nx(g)



    def init(self,progress=True,**kwargs):
        for t in self.data_all: t.init()
        return self

    def queue_remote_sources(self):
        for t in self: t.queue_remote_sources()

    def match(self,callback=None,verbose=True,**kwargs):
        # input
        if log: log('...')
        df = pd.DataFrame(
            dict(id=t.addr, author=t.au, title=t.shorttitle)
            for t in self
            if t.au and t.shorttitle
        ).set_index('id')
        ofn=f'.tmp.data.{zeropunc(str(time.time()))}.pkl'
        df.to_pickle(ofn)
        wasnum_uniq = len(self.data_uniq)
        if log: log('llcode...')
        code="""

df=pd.read_pickle('%s')

now=time.time()

if log: log('finding by title...')
from lltk.model.matcher import match_by_title

res=match_by_title(df)
if %s:
    log.info(
        f'found {len(res)} title matches in {round(time.time()-now,2)}s'
    )
""" % (ofn,verbose)

        def callback(res):
            rmfn(ofn)
            if verbose:
                num_uniq = len(self.filtered())
                if wasnum_uniq != num_uniq:
                    log.info(f'Filtered from {wasnum_uniq} to {num_uniq} distinct texts:\n{self}')

        log.info('searching for matches in background process')
        llcode(code,callback=callback)
        # return self

def hellofunc():
    o=[]
    for n in range(5):
        x=f'Hello, {n}...'
        print(x)
        time.sleep(random.random())
        o.append(x)
    return o
def callback(x): print('call back done!!')

def do_and_then(func,*args,callback=None,**kwargs):
    print(func,args,kwargs)
    if callback: print(f'callback = {callback}')
    pool = mp.Pool(1)
    res = pool.apply_async(
        func,
        args=args,
        kwds=kwargs,
        callback=callback
    )
    return res#.get(timeout=15)






#     def match(self,callback=None,verbose=True,**kwargs):
#         # input
#         if log: log('...')
#         df = pd.DataFrame(dict(id=t.addr, author=t.au, title=t.shorttitle)
#             for t in self
#             if t.au and t.shorttitle
#         ).set_index('id')
#         ofn=f'.tmp.data.{zeropunc(str(time.time()))}.pkl'
#         df.to_pickle(ofn)
#         wasnum_uniq = len(self.data_uniq)
#         if log: log('llcode...')
#         code="""

# df=pd.read_pickle('%s')

# now=time.time()

# if log: log('finding by title...')
# from lltk.model.matcher import match_by_title

# res=match_by_title(df)
# if %s:
#     log.info(
#         f'found {len(res)} title matches in {round(time.time()-now,2)}s'
#     )
# """ % (ofn,verbose)

#         def callback(res):
#             rmfn(ofn)
#             if verbose:
#                 num_uniq = len(self.filtered())
#                 if wasnum_uniq != num_uniq:
#                     log.info(f'Filtered from {wasnum_uniq} to {num_uniq} distinct texts:\n{self}')

#         log.info('searching for matches in background process')
#         llcode(code,callback=callback)
#         # return self




#     # for text in intertxt.find(author="Eliza Haywood"):
#     #      print(f"""{str(text)[:30]:<30}\t{str(text.author)[:25]:<25}\t{str(text.title)[:50]:<50}\t{text.year}""")