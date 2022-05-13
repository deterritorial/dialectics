from .imports import *

class BaseObject(object):
    __COLLECTION__='obj'

    @property
    def _dbtbl(self):
        return self.__COLLECTION__
    @property
    def _dbkey(self):
        return self._id.replace(IDSEP,IDSEP_DB)
    _key=_dbkey
    @property
    def _dbid(self):
        return f'{self._dbtbl}/{self._dbkey}'
    

