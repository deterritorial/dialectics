#print(__file__,'imported')
from intertxt.imports import *




def get_addr_str(text=None,corpus=None,source=None,**kwargs):
    from intertxt.corpora import Corpus
    corpus=Corpus(corpus)

    # rescue via source?
    if text is None:
        if source is not None: return get_addr_str(source,corpus,None,**kwargs)
        return get_addr_str(
            get_idx(
                # i=corpus.num_texts+1 if corpus else None,
                **kwargs),
                corpus,
            **kwargs
        )
    
    # corpus set? if not, work to get it so
    if not corpus:
        if is_text_obj(text): return text.addr
        if type(text)==str:
            cx,ix = to_corpus_and_id(text)
            if cx and ix: return text
            if ix: return get_addr_str(ix,TMP_CORPUS_ID,**kwargs)
        return get_addr_str(text,TMP_CORPUS_ID,**kwargs)

    # now can assume we have both corpus and text
    corpus = corpus.id if is_corpus_obj(corpus) else str(corpus)
    idx=get_idx(text)
    cpref=IDSEP_START + corpus + IDSEP
    o=cpref + idx if not idx.startswith(cpref) else idx
    if log>3: log(f'-> {o}')
    return o


      
def dict_to_addr(d1={},**d2):
    d={**d1,**d2}
    addr,id,corp=d.get(COL_ADDR),d.get(COL_ID),d.get(COL_CORPUS)
    if addr: return addr
    if id and corp: return to_addr(id,corp)
    if id and is_addr(id): return id
    # if not id: id=d.get('_id')
    
    # if 'corpus' in d: d[]
    raise Exception(f"Where is the id? {d}")


def get_imsg(__id=None,__corpus=None,__source=None,**kwargs):
    o=[]
    _id,_corpus,_source = __id,__corpus,__source
    if _id: o.append(f'id = {_id}')
    if _corpus: o.append(f'corpus = {_corpus}')
    if _source: o.append(f'source = {_source}')
    if kwargs: o.append(f'kwargs = {str(kwargs)[:100]})')
    # if kwargs: o.append(f'kwargs = {list(kwargs.keys())}')
    return ', '.join(o) if o else ''








def TextKeys(id=None,_corpus=None,_load=True,_force=False,_id=None,_addr=None,**kwargs):
    if type(id)==dict:
        odx=merge_dict(id, kwargs, dict(_corpus=_corpus,_force=_force,_id=_id,_addr=_addr))
        return TextKeys(**odx)

    # in case we have addr
    for idx in [_addr,_id,id]:
        if is_textish(idx):
            idx=idx.addr if is_text_obj(idx) else idx
            return get_textkeys_addr(idx) if not _corpus else get_textkeys_id_corpus(idx,_corpus,_source=idx)
    
    # contingencies...
    if _id and not id: id=_id
    

    # if not corpus...
    if not _corpus:
        # if id already text -- give it back immediately
        if is_text_obj(id): return id

        ## if no id at all -- give both defaults
        if not id:
            _corpus,id=TMP_CORPUS,get_idx()
        
        # if id...
        else:
            ## if id already an address -- parse it
            if is_addr(id):
                _corpus,id=to_corpus_and_id(id)
            # if not, then keep this id but use default corpus
            else:
                _corpus=TMP_CORPUS
    
    # if IS a corpus...
    else:
        # if no id
        if not id:
            id=get_idx()
        # if IS id
        else:
            # already a text? add as source?
            if is_textish(id):
                _source = id
            else:
                # normal situation! corpus and id
                pass

    assert id and _corpus
    return get_textkeys_id_corpus(id,_corpus)


def get_textkeys_addr(addr,_clean=True,**extra):
    assert is_addr(addr)

    # clean!  ## all comes through here?
    if _clean: addr = get_idx(addr)
    ####

    _corpus,id = to_corpus_and_id(addr)
    key = addr_to_dbkey(addr)
    dbid = f'{TEXT_COLLECTION_NAME}/{key}'
    return dict(
        _id=dbid,
        _key=key,
        _addr=addr,
        _corpus=_corpus,
        id=id,
        **extra
    )
def get_textkeys_id_corpus(id,_corpus,**kwargs):
    addr = to_addr(_corpus,id)
    return get_textkeys_addr(addr,**kwargs)














### Funcs



META_KEYS_USED_IN_AUTO_IDX = {
    'author',
    'title',
    'edition',
    'year',
    'publisher',
    'vol',
}

# def get_idx_from_meta(meta,sep_kv='=',sep='/',hidden='_'):
#     o=[]
#     for k,v in sorted(meta.items()):
#         if k and k[0]!=hidden:
#             o.append(f'{k}{sep_kv}{v}')
#     ostr=sep.join(o)
#     return get_idx(ostr)

def get_idx_from_meta(
        meta,
        keys=META_KEYS_USED_IN_AUTO_IDX,
        sep_kv='=',
        sep='/',
        hidden='_'):
    o=[]
    for k in keys:
        v = get_prop_ish(meta,k)
        if v is not None:
            o.append(f'{k}{sep_kv}{v}')
    o.sort()
    ostr=sep.join(o)
    return get_idx(ostr) if o else None

def get_idx_from_int(i=None,numzero=5,prefstr='T'):
    if not i:
        numposs=int(f'1{"0"*5}')
        i=random.randint(1,numposs-1)
    return f'{prefstr}{i:0{numzero}}'


def get_idx(
        id=None,
        i=None,
        allow='_/.-:,=',
        prefstr='T',
        numzero=5,
        use_meta=True,
        force_meta=True,
        **meta):
    
    if is_text_obj(id): return id.id
    id1=id
    if log>1: log(f'<- id = {id}, i = {i}')
    # already given?
    if safebool(id):
        if type(id)==str:
            id = ensure_snake(
                str(id),
                allow=allow,
                lower=False
            )
            if log>2:
                if log: log(f'id set via `id` str: {id1} -> {id}')
        
        elif type(id) in {int,float}:
            id = get_idx_from_int(int(id))
            if log>1: log(f'id set via `id` int: {id1} -> {id}')
        
        else:
            raise Exception(f'What kind of ID is this? {type(id1)}')

    else:
        if meta and (force_meta or (use_meta and not i)):
            id = get_idx_from_meta(meta)
            if log>1: log(f'id set via `meta`: {id1} -> {id}')
        elif i:
            id = get_idx_from_int(i,numzero=numzero,prefstr=prefstr)
            if log>1: log(f'id set via `i` int: {id1} -> {id}')

    
    if not id:
        id = get_idx_from_int(numzero=numzero,prefstr=prefstr) # last resort
        if log>1: log(f'id set via random int: {id1} -> {id}')
    
    if not id: raise Exception('what happened?')
        
    if log>1: log(f'-> {id}')
    return id



