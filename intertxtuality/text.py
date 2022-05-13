from .imports import *
from .database import get_collection

TEXT_CACHE={}
TMP_CORPUS='tmp'



def Text(_id=None,_corpus=None,**kwargs):
    return BaseText(_id,_corpus,**kwargs)




class BaseText(BaseObject):
    __COLLECTION__='text'

    def __init__(self,_id,_corpus=None,**kwargs):
        if type(_id)==str and _id and not IDSEP in _id and IDSEP_DB in _id:
            _id=_id.replace(IDSEP_DB,IDSEP)
        if not _id: _id=get_idx()
        if not is_textish(_id):
            if not _corpus: _corpus=TMP_CORPUS
            _id = to_addr(_corpus,_id)
                
        if not is_textish(_id):
            raise Exception(f"Cannot get an ID? {_id}")    
        assert is_textish(_id)
        
        self._id=_id                       # text 'addr'
        self._corpus=addr_to_corpus(_id)   # corpus id
        self.id=addr_to_id(_id)            # text id
        self._data=kwargs                  # all metadata


    @property
    def _meta(self):
        return self.ensure_id(just_meta(self._data))
    @property
    def _params(self):
        return self.ensure_id(just_params(self._data))
    @property
    def data(self): return self._meta
    
    

    def ensure_id(self,d={},idkey='_id',**kwargs):
        print([d,idkey])
        id=getattr(self,idkey)
        return merge_dict({idkey:id}, just_meta(merge_dict(self._data, d, kwargs)))

    def ensure_id_db(self,d={},idkey='_key',**kwargs):
        return self.ensure_id(d=d,idkey=idkey,**kwargs)


    @property
    def collection(self): return get_collection(self.__COLLECTION__)
    coll=collection
    
    ## database funcs
    def load(self):
        data = self.collection.get(self._key)
        if data: self._data={**self._data,**just_meta(data)}
    
    def exists(self):
        return self._key in self.collection
    
    def upsert(self,d={},tryagain=True):
        to_insert = self.ensure_id_db(d)
        saved_meta={}
        try:
            saved_meta = self.coll.update(to_insert)
        except Exception as e:
            if log>2: log.error(e)
            try:
                saved_meta = self.coll.insert(to_insert)
            except Exception as e:
                if log: log.error(e)
        if log: log(saved_meta)
        return saved_meta
        
    
        

    def save(self):
        saved_meta=self.upsert()
        if not saved_meta: return
        assert saved_meta['_key'] == self._key
        self._data = {**self._data, **just_meta(saved_meta)}
        return saved_meta

    


































































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


