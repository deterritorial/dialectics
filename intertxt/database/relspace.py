from intertxt.imports import *
from .docspace import Docspace

RELSPACE_DEFAULT='is_also'
FROM_DEFAULT=['text']
TO_DEFAULT=['text']

class Relspace(Docspace):
    def __init__(self,
            name=RELSPACE_DEFAULT,
            from_collections=FROM_DEFAULT,
            to_collections=TO_DEFAULT,
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
        self._from=from_collections
        self._to=to_collections
        self._graph=None
        self._edgedf=None

    @property
    def graph(self):
        if self._graph is None: self.init_graph()
        return self._graph

    def __repr__(self):
        return f"Relspace('{self.name}')"


    def init_graph(self):
        if self.db.has_graph(GRAPHNAME):
             self._graph = self.db.graph(GRAPHNAME)
        else:
            self._graph = self.db.create_graph(GRAPHNAME)


    def init_collection(self, drop=False):
        if not self.graph.has_edge_definition(self.name):
            self._coll = self.graph.create_edge_definition(
                edge_collection=self.name,
                from_vertex_collections=self._from,
                to_vertex_collections=self._to
            )
        else:
            self._coll = self.graph.edge_collection(self.name)

            

    def link(self,id1,id2,d1={},**d2):
        from intertxt.texts import Text

        with Log('linking texts') as log:
            
            t1,t2=Text(id1),Text(id2)
            id1,id2=t1._id,t2._id
            key=f'{t1._key}__{t2._key}'
            obj={
                '_key':key,
                '_from':t1._id,
                '_to':t2._id,
                **safebool(safejson(merge_dict(d1,d2)))
            }
            saved_meta={}
            try:
                saved_meta = self.coll.update(obj)
            except Exception as e:
                if log>2: log.error(e)
                try:
                    saved_meta = self.coll.insert(obj)
                except Exception as e:
                    if log: log.error(e)
            if log>1: log(saved_meta)
            return {**obj, **saved_meta}

