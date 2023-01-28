#!/usr/bin/env python
# coding: utf-8

# In[4]:


import sys; sys.path.insert(0,'../..')
from txtuality import *


# In[5]:


authors=OrderedSetDict()
for c in get_tqdm(['chadwyck','chicago','txtlab','tedjdh']):
    for t in lookfor_texts(_corpus=c):
        authors[t.au]=t.addr
authors


# In[2]:



l=list(authors.items())
iterr=sorted(l)
iterr=get_tqdm(l)
for au,addrs in iterr:
    au_tl = TextList(addrs)
    if len(au_tl)>1: 
        matchdf = au_tl.match(_progress=False)
        desc=f'{au} ({len(addrs)}t, {len(matchdf)}m)'
        if safebool(matchdf) and 'id_1' in set(matchdf.columns):
            desc+=f' [e.g. {Text(matchdf.id_1.iloc[-1])._id} ]'
            iterr.set_description(desc)
        
        # break


# In[ ]:





# In[ ]:




