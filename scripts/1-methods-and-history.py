"""Step 1. Hides each test reader's most recent 4 or 5 star book, then scores the bestseller list, 'readers also liked' and the taste profile model,
using the whole history and the last 1, 3 and 10 liked books. Writes res_full.json and ev.npy (the 10,000 test readers)."""
import numpy as np, pandas as pd, scipy.sparse as sp, json, time
from sklearn.decomposition import TruncatedSVD
rng=np.random.default_rng(20261120)
r=pd.read_csv('ratings.csv'); r['order']=np.arange(len(r))  # file order = time order (dataset README)
pos=r[r.rating>=4]
users=pos.user_id.unique(); ev=rng.choice(users,10000,replace=False); evs=set(ev.tolist())
# holdout: each eval user's most recent liked book; history = earlier ratings (all ratings count as "read")
last=pos[pos.user_id.isin(evs)].sort_values('order').groupby('user_id').tail(1).set_index('user_id')
hold=last.book_id.to_dict(); cut=last.order.to_dict()
keep=~r.user_id.isin(evs) | (r.order < r.user_id.map(cut).fillna(np.inf))
train=r[keep]; tpos=train[train.rating>=4]
U,I=53425,10001
X=sp.csr_matrix((np.ones(len(tpos),np.float32),(tpos.user_id,tpos.book_id)),shape=(U,I))
seen=sp.csr_matrix((np.ones(len(train),np.float32),(train.user_id,train.book_id)),shape=(U,I))
pop=np.asarray(X.sum(0)).ravel(); pop[0]=-1
top100=set(np.argsort(-pop)[:100].tolist())
t=time.time()
# item-item cosine
norms=np.sqrt(np.asarray(X.multiply(X).sum(0)).ravel())+1e-9
S=(X.T@X).toarray().astype(np.float32); S/=norms[:,None]; S/=norms[None,:]; np.fill_diagonal(S,0)
print('item-item',round(time.time()-t),'s')
svd=TruncatedSVD(64,random_state=7).fit(X); V=svd.components_.astype(np.float32)  # 64 x I
def recs(u,method,hist_items):
    if method=='pop': s=pop.copy()
    elif method=='item': s=S[hist_items].sum(0) if len(hist_items) else pop*0
    elif method=='svd':
        x=np.zeros(I,np.float32); x[hist_items]=1; s=(x@V.T)@V
    s=s.astype(np.float64); s[0]=-np.inf
    s[seen[u].indices]=-np.inf
    return np.argpartition(-s,10)[:10]
def run(limit=None):
    out={m:dict(hit=0,n=0,recs=set(),top=0) for m in ['pop','item','svd']}
    seg={}
    for u in ev:
        h=X[u].indices
        # most recent liked items first for truncation
        if limit is not None:
            order=tpos[tpos.user_id==u].sort_values('order').book_id.values[::-1][:limit]; h=order
        b=len(X[u].indices); g='1-20' if b<=20 else '21-50' if b<=50 else '51+'
        for m in out:
            rr=recs(u,m,h); hit=hold[u] in set(rr.tolist())
            o=out[m]; o['hit']+=hit; o['n']+=1; o['recs'].update(rr.tolist()); o['top']+=sum(1 for x in rr if x in top100)
            seg.setdefault((g,m),[0,0]); seg[(g,m)][0]+=hit; seg[(g,m)][1]+=1
    return {m:dict(hit_rate=round(o['hit']/o['n'],4),coverage=len(o['recs']),top100_share=round(o['top']/(10*o['n']),3)) for m,o in out.items()}, {f'{g}|{m}':[v[0],v[1]] for (g,m),v in seg.items()}
import os
if True:
  t=time.time(); full,seg=run(); print('full',full,round(time.time()-t),'s'); print(seg)
  json.dump(dict(full=full,seg=seg),open('res_full.json','w'))

# New-user test: keep only each reader's most recent N liked books as history
hist_sorted=tpos.sort_values('order').groupby('user_id').book_id.apply(lambda s:s.values[::-1])
def run_limit(n):
    out={m:dict(hit=0,c=0,recs=set(),top=0) for m in ['pop','item','svd']}
    for u in ev:
        h=hist_sorted.get(u,np.array([],int))[:n]
        for m in out:
            rr=recs(u,m,h); o=out[m]; o['hit']+=hold[u] in set(rr.tolist()); o['c']+=1; o['recs'].update(rr.tolist()); o['top']+=sum(1 for x in rr if x in top100)
    return {m:dict(hit_rate=round(o['hit']/o['c'],4),coverage=len(o['recs']),top100_share=round(o['top']/(10*o['c']),3)) for m,o in out.items()}
cold={n:run_limit(n) for n in [1,3,10]}
print('cold',cold)
d=json.load(open('res_full.json')); d['cold']=cold; d['n_eval']=len(ev); json.dump(d,open('res_full.json','w'))
np.save('ev.npy',ev)
