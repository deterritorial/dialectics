from intertxt.imports import *

from collections import UserList
class TextList(UserList, BaseObject):
    pass

    def match(self,callback=None,verbose=True,**kwargs):
        # input
        if log: log('...')
        df = pd.DataFrame(dict(id=t.addr, author=t.au, title=t.shorttitle)
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




    # for text in intertxt.find(author="Eliza Haywood"):
    #      print(f"""{str(text)[:30]:<30}\t{str(text.author)[:25]:<25}\t{str(text.title)[:50]:<50}\t{text.year}""")