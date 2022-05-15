from totality.models import *

def run_match_by_title(*x,**y):
    print(f'run_match_by_title({x},{y})')
    # db=CDB(force=True)
    bag = match_by_title(*x,**y)#db=db,
    return bag
    #return [promise.result() for promise in bag]


def match_by_author(self,corpora=['chadwyck','chicago','txtlab','tedjdh']):
    authors=OrderedSetDict()
    for c in get_tqdm(corpora):
        for t in lookfor_texts(_corpus=c):
            authors[t.au]=t.addr

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


def match_by_title(
        df,
        df2=None,
        full=False,
        compare_by=DEFAULT_COMPAREBY,
        method_string='levenshtein',
        **kwargs):
    # get df
    # set up index
    import recordlinkage as rl
    indexer = rl.Index()
    indexer.block(left_on='author', right_on='author') if not full else indexer.full()
    # get candidates
    df2= (df2 if df2 is not None else df)
    candidates = indexer.index(df,df2)
    # set up comparison model
    c = rl.Compare()
    for k,v in compare_by.items():
        c.string(k,k,threshold=v,method=method_string) if v<1.0 else c.exact(k,k)
    res = c.compute(candidates, df, df2)

    res.columns = [f'match_{k}' for k in compare_by]
    res['match_sum'] = res.sum(axis=1)
    res['match_rel'] = res['match_sum'] / len(compare_by)
    res['match'] = res['match_rel'] == 1
    res=res.reset_index()
    res = res[res.id_1 != res.id_2]
    res = res[res.match==True]
    return res


def get_lsh(redis=True, threshold=0.95):
    from datasketch import MinHashLSH
    if redis:
        lsh = MinHashLSH(
            threshold=threshold, num_perm=HASH_NUMPERM, storage_config={
                'type': 'redis',
                'basename': MINHASH_KEYPREF,
                'redis': {'host': 'localhost', 'port': 6379},
            }
        )
    else:
        lsh = MinHashLSH(threshold=threshold, num_perm=HASH_NUMPERM)
    return lsh

def get_all_lsh_keys(lsh):
    return {(b"_"+b'_'.join(k.split(b'_')[1:]).split(b'\x94')[0]).decode() for k in lsh.keys.keys()}


def find_matches_by_hash(self, texts_iter=None, lsh=None, threshold=0.95, progress=True):
    # Approximate
    if texts_iter is None: texts_iter = self.iter_texts_each()
    texts = []
    if lsh is None:
        lsh = get_lsh()
        for t in texts_iter:
            try:
                minhash = t.minhash()
                if minhash:
                    lsh.insert(t.addr, minhash)
                    texts.append(t)
            except Exception as e:
                self.log.error(e)
    
    o=[]
    if texts:
        iterr = texts
        if progress and len(texts)>=0: iterr=get_tqdm(texts,desc='Matching texts')
        for t in iterr:
            for t2addr in lsh.query(t.minhash()):
                if t2addr!=t.addr:
                    t2=Text(t2addr)
                    t.add_source(t2,rel_type='minhash')
                    o.append((t.addr,t2.addr))
    return o


