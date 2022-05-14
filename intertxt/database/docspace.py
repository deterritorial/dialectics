#print(__file__,'imported')
from intertxt.imports import *
from .baseobj import BaseObject



class Docspace(BaseObject):
    def __init__(self,
            name=TEXT_COLLECTION_NAME,
            dbname=DATABASE+'_'+VNUM,
            _client=None,
            _db=None,
            _coll=None,
            ):
        self.name=name
        self.dbname=dbname
        self._client=None
        self._db=None
        self._coll=None
    
    @property
    def client(self):
        if self._client is None: self.init_database()
        return self._client
    @property
    def db(self):
        if self._db is None: self.init_database()
        return self._db
    @property
    def coll(self): 
        if self._coll is None: self.init_collection()
        return self._coll

    def init_database(self,force=False):
        if force or self._db is None:
            from arango import ArangoClient
            self._client = ArangoClient(hosts=','.join(SERVERS))
            self._sydb  = self._client.db('_system', username='root', password='passwd')
            self._db = self._client.db(self.dbname, username='root', password='passwd')
        return self.db

    def init_collection(self,drop=False):
        if self.db.has_collection(self.name): 
            if drop: 
                self.db.delete_collection(self.name)
                self._coll=self.db.create_collection(self.name)
            else:
                self._coll=self.db.collection(self.name)
                return self._coll
        else:
            self._coll=self.db.create_collection(self.name)
        return self._coll
        

            
    ### TREATS FULL TEXT OPERATOR FOR MULTIPLE ARGUMENTS AS 'OR' so far
    def find(self,*args,**kwargs):
        from intertxt.texts.textlist import TextList
        return TextList(self.look(*args,**kwargs))
    def look(self, id_key=COL_ADDR, **query_meta):
        from intertxt import Text,Log
            
        # prime
        if not self.coll: return

        fulltextmeta={k:v for k,v in query_meta.items() if k in FULL_TEXT_KEYS}
        exactmeta={k:v for k,v in query_meta.items() if k not in FULL_TEXT_KEYS}

        ids_given=set()

        if exactmeta:
            with Log(f'Querying exact metadata: {exactmeta}'):
                res_exact = self.coll.find(exactmeta)
                for d in res_exact:
                    id=d.get(id_key)
                    if id not in ids_given:
                        yield Text(**d)
                        ids_given|={id}
        
        if fulltextmeta:
            with Log(f'Querying full text metadata: {fulltextmeta}'):
                for qk,qv in fulltextmeta.items():
                    res = self.coll.find_by_text(qk,qv)
                    for d in res:
                        id=d.get(id_key)
                        if id not in ids_given:
                            yield Text(**d)
                            ids_given|={id}



class Textspace(Docspace):
    def init(self,drop=False):
        super().init(drop=drop)
        if self.coll:
            coll=self.coll
            coll.add_persistent_index(fields=['_addr'],unique=True)
            coll.add_persistent_index(fields=['_corpus'])
            coll.add_persistent_index(fields=['id'])
            coll.add_persistent_index(fields=['au'])
            coll.add_persistent_index(fields=['ti'])
            coll.add_persistent_index(fields=['yr'])
            coll.add_fulltext_index(fields=['author'])
            coll.add_fulltext_index(fields=['title'])
        return self






DOCSPACES={}
def DocspaceX(name, dbname=f"{DATABASE}_{VNUM}", force=False, _class=Docspace,**kwargs):
    if not force and (name,dbname) in DOCSPACES:
        return DOCSPACES[(name,dbname)]
    obj = _class(name=name,dbname=dbname)
    DOCSPACES[(name,dbname)] = obj
    return obj


def Textspace(force=False, **kwargs):
    return Docspace(TEXT_COLLECTION_NAME, **kwargs)

    

