#print(__file__,'imported')
from intertxt.imports import *
from intertxt.database.baseobj import BaseObject
TEXT_COLLECTION_NAME='text'
FULL_TEXT_KEYS={'author','title'}

DATABASE='intertxt'
_ADB_ = None
_ADB_CLIENT = None
_ADB_SYSDB = None
VNUM='2022_05_13e'


def get_database(dbname=DATABASE,force=False):
    global _ADB_,_ADB_CLIENT,_ADB_SYSDB

    if force or _ADB_ is None:
        # Initialize the ArangoDB client.
        from arango import ArangoClient
        client = ArangoClient(hosts=','.join(SERVERS))
        sysdb = client.db('_system', username='root', password='passwd')

        # Create a new database named "test" if it does not exist.
        if not sysdb.has_database(dbname):
            sysdb.create_database(dbname)

        # Connect to "test" database as root user.
        # This returns an API wrapper for "test" database.
        db = client.db(dbname, username='root', password='passwd')

        _ADB_ = db
        _ADB_CLIENT = client
        _ADB_SYSDB = sysdb
    
    return _ADB_


def get_collection(name,dbname=DATABASE,drop=False):
    dbname=f'{dbname}_{VNUM}'
    db=get_database(dbname)
    if db.has_collection(name): 
        if drop: 
            db.delete_collection(name)
        else:
            return db.collection(name)
    
    coll=db.create_collection(name)

    coll.add_persistent_index(fields=['_addr'],unique=True)
    coll.add_persistent_index(fields=['_corpus'])
    coll.add_persistent_index(fields=['id'])
    coll.add_persistent_index(fields=['au'])
    coll.add_persistent_index(fields=['ti'])
    coll.add_persistent_index(fields=['yr'])

    coll.add_fulltext_index(fields=['author'])
    coll.add_fulltext_index(fields=['title'])

    return coll



def get_text_collection(name=TEXT_COLLECTION_NAME,**kwargs):
    return get_collection(name,**kwargs)


# underscored={'corpus','au','ti','yr','addr'}

### TREATS OPERATOR FOR MULTIPLE ARGUMENTS AS 'OR' so far
def look(_collection=TEXT_COLLECTION_NAME, id_key=COL_ADDR, **query_meta):
    from intertxt import Text,Log

    
    coll=get_collection(_collection)
    fulltextmeta={k:v for k,v in query_meta.items() if k in FULL_TEXT_KEYS}
    exactmeta={k:v for k,v in query_meta.items() if k not in FULL_TEXT_KEYS}

    ids_given=set()

    if exactmeta:
        with Log(f'Querying exact metadata: {exactmeta}'):
            res_exact = coll.find(exactmeta)
            for d in res_exact:
                id=d.get(id_key)
                if id not in ids_given:
                    yield Text(**d)
                    ids_given|={id}
    
    if fulltextmeta:
        with Log(f'Querying full text metadata: {fulltextmeta}'):
            for qk,qv in fulltextmeta.items():
                res = coll.find_by_text(qk,qv)
                for d in res:
                    id=d.get(id_key)
                    if id not in ids_given:
                        yield Text(**d)
                        ids_given|={id}




def find(*args,**kwargs): return list(look(*args,**kwargs))