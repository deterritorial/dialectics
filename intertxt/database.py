from .imports import *
from intertxt.models import BaseObject

DATABASE='intertxt'
_ADB_ = None
_ADB_CLIENT = None
_ADB_SYSDB = None



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


def get_collection(name,dbname=DATABASE):
    db=get_database(dbname)
    if db.has_collection(name):
        return db.collection(name)
    else:
        return db.create_collection(name)

















































































































































### Notes







# Other collections
# List all collections in the database.
# db.collections()
# # Retrieve collection properties.
# students.name
# students.db_name
# students.properties()
# students.revision()
# students.statistics()
# students.checksum()
# students.count()

# # Perform various operations.
# students.load()
# students.unload()
# students.truncate()
# students.configure()

# # Delete the collection.
# db.delete_collection('students')
