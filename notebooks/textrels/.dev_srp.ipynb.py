#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys; sys.path.insert(0,'../..')
from txtuality import Text,log,Corpus
log.off()
N_DIM=640


# In[2]:


from txtuality import *
class SRPModel(DocspaceModel):
    NAME='srp'

    def init_collection(self,drop=False):
        if log>0: log(self)
        if self.db.has_collection(self.name) and drop: self.db.delete_collection(self.name)
        if not self.db.has_collection(self.name): self.db.create_collection(self.name)
        coll = self._coll=self.db.collection(self.name)
        coll.add_persistent_index(fields=['_addr'],unique=True)
        return self._coll


# In[3]:


sm = SRPModel()
sm


# In[4]:





# In[9]:


for c in ['chadwyck','chicago','clmet']:
    for i,t in enumerate(Corpus(c).texts(progress=True)):
        dat = t.srp(n_dim=N_DIM)
        if dat is not None and len(dat):
            odx=safejson({'_key':t._key, '_addr':t.addr, 'n_dim':N_DIM, 'val':dat})
            try:
                sm.coll.insert(odx)
            except DocumentInsertError:
                sm.coll.update(odx)
            # t.save()


# In[7]:


sm.coll.get(t._key)


# In[12]:


from txtuality import Corpus
for t in Corpus('chadwyck').texts(progress=True):
    t.srp(num_dim=2, cache=True, force=True)


# In[7]:


t = Corpus('chadwyck').t
t


# In[8]:


array = t.srp(cache=True,force=True)
array


# In[9]:


from txtuality import Textspace
Textspace().coll.find_near(float(array[0]), float(array[1]))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


mat = t.srp(n_dim=640, cache=False)
mat


# In[ ]:


from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, random_state=0)


# In[ ]:


tsne.fit_transform(mat)


# In[ ]:


get_ipython().system('pip install -U pip')
# # 


# In[ ]:




