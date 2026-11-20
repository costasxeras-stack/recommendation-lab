"""Step 3. Scores every method reader by reader, split by same-series and other readers, plus coverage and bestseller share.
Writes summary.json, per_user.csv and examples.json (40 random readers for the page)."""
import numpy as np, pandas as pd, scipy.sparse as sp, json, re
from sklearn.decomposition import TruncatedSVD
r=pd.read_csv('ratings.csv'); r['order']=np.arange(len(r)); b=pd.read_csv('books.csv')
ev=np.load('ev.npy'); evs=set(ev.tolist())
pos=r[r.rating>=4]
last=pos[pos.user_id.isin(evs)].sort_values('order').groupby('user_id').tail(1).set_index('user_id')
hold=last.book_id.to_dict(); cut=last.order.to_dict()
keep=~r.user_id.isin(evs) | (r.order < r.user_id.map(cut).fillna(np.inf))
train=r[keep]; tpos=train[train.rating>=4]
U,I=53425,10001
X=sp.csr_matrix((np.ones(len(tpos),np.float32),(tpos.user_id,tpos.book_id)),shape=(U,I))
seen=sp.csr_matrix((np.ones(len(train),np.float32),(train.user_id,train.book_id)),shape=(U,I))
pop=np.asarray(X.sum(0)).ravel().astype(np.float64); pop[0]=-1; rank=np.empty(I,int); rank[np.argsort(-pop)]=np.arange(I)
norms=np.sqrt(np.asarray(X.multiply(X).sum(0)).ravel())+1e-9
S=(X.T@X).toarray().astype(np.float32); S/=norms[:,None]; S/=norms[None,:]; np.fill_diagonal(S,0)
V=TruncatedSVD(64,random_state=7).fit(X).components_.astype(np.float32)
def ser(t):
    m=re.search(r'\(([^()#]+?),?\s*#(\d+(?:\.\d+)?)\)\s*$',str(t)); return (m.group(1).strip().lower(), float(m.group(2))) if m else (None,None)
SS=b.title.map(ser); sname=dict(zip(b.book_id,[s[0] for s in SS])); snum=dict(zip(b.book_id,[s[1] for s in SS]))
by_series={}
for bid,s in sname.items():
    if s: by_series.setdefault(s,[]).append((snum[bid],bid))
for s in by_series: by_series[s].sort()
hist_sorted=tpos.sort_values('order').groupby('user_id').book_id.apply(lambda s:s.values[::-1])
def top10(s,u):
    s=s.astype(np.float64); s[0]=-np.inf; s[seen[u].indices]=-np.inf
    idx=np.argpartition(-s,10)[:10]; return idx[np.argsort(-s[idx])]
rows=[]; recsets={}
for u in ev:
    full=X[u].indices; h=hist_sorted.get(u,np.array([],int)); h1,h3=h[:1],h[:3]
    R={'pop':top10(pop.copy(),u),'item_full':top10(S[full].sum(0),u),'svd_full':top10((np.isin(np.arange(I),full).astype(np.float32)@V.T)@V,u),
       'item_last3':top10(S[h3].sum(0),u),'item_last1':top10(S[h1].sum(0),u)}
    # series rule then fill with item_last3
    nxt=[]
    if len(h1) and sname.get(int(h1[0])):
        sv=set(seen[u].indices.tolist()); nxt=[bid for num,bid in by_series[sname[int(h1[0])]] if num>snum[int(h1[0])] and bid not in sv][:10]
    hyb=list(nxt)+[x for x in R['item_last3'] if x not in nxt]; R['hybrid']=np.array(hyb[:10])
    same=bool(len(h1) and sname.get(int(h1[0])) and sname.get(hold[u])==sname.get(int(h1[0])))
    rows.append(dict(u=int(u),same_series=same,series_rule_fired=bool(nxt),n_liked=int(len(full)),**{m:int(hold[u] in set(v.tolist())) for m,v in R.items()}))
    for m,v in R.items(): recsets.setdefault(m,[]).append(v)
df=pd.DataFrame(rows); M=['pop','svd_full','item_full','item_last3','item_last1','hybrid']
top100=set(np.argsort(-pop)[:100].tolist())
summ={}
for m in M:
    allr=np.concatenate(recsets[m]); summ[m]=dict(hit=round(df[m].mean(),4),hit_series=round(df[df.same_series][m].mean(),4),hit_other=round(df[~df.same_series][m].mean(),4),
      coverage=int(len(set(allr.tolist()))),top100=round(float(np.mean([x in top100 for x in allr])),3),median_pop_rank=int(np.median(rank[allr])))
summ['_n']=dict(users=len(df),same_series=int(df.same_series.sum()),rule_fired=int(df.series_rule_fired.sum()))
print(json.dumps(summ,indent=1))
df.to_csv('per_user.csv',index=False); json.dump(summ,open('summary.json','w'))
# examples for the app: 30 readers with titles
title=dict(zip(b.book_id,b.title)); ex=[]
rng=np.random.default_rng(1)
for i in rng.choice(len(ev),40,replace=False):
    u=int(ev[i]); h=hist_sorted.get(u,np.array([],int))[:3]
    ex.append(dict(recent=[title[int(x)] for x in h],hidden=title[hold[u]],recs={m:[title[int(x)] for x in recsets[m][i]] for m in ['pop','item_full','item_last3','hybrid']}))
json.dump(ex,open('examples.json','w'),ensure_ascii=False)
