"""Step 2. Counts how often the hidden book continues the series of the last liked book, and scores a 'next in series' rule. Writes series.json.
Note: the 'hold_in_series' count in the output is not used: it treats missing series names as true."""
import numpy as np, pandas as pd, re, json
b=pd.read_csv('books.csv'); r=pd.read_csv('ratings.csv'); r['order']=np.arange(len(r))
def ser(t):
    m=re.search(r'\(([^()#]+?),?\s*#(\d+(?:\.\d+)?)\)\s*$',str(t))
    return (m.group(1).strip().lower(), float(m.group(2))) if m else (None,None)
S=b.title.map(ser); b['series']=[s[0] for s in S]; b['num']=[s[1] for s in S]
print('books in a series', b.series.notna().mean())
info=b.set_index('book_id')[['series','num','title']]
ev=np.load('ev.npy'); evs=set(ev.tolist())
pos=r[r.rating>=4]
last=pos[pos.user_id.isin(evs)].sort_values('order').groupby('user_id').tail(1).set_index('user_id')
prev_rows=[]
cnt=dict(hold_in_series=0,same_series_as_prev=0,n=0,rule_fires=0,rule_hit=0)
by_series={}
for (s,grp) in b.dropna(subset=['series']).groupby('series'): by_series[s]=grp.sort_values('num')[['book_id','num']].values.tolist()
for u,row in last.iterrows():
    hb=row.book_id; cut=row.order
    hist=r[(r.user_id==u)&(r.order<cut)]
    liked=hist[hist.rating>=4].sort_values('order')
    if not len(liked): continue
    pb=liked.book_id.values[-1]
    cnt['n']+=1
    hs,hn=info.loc[hb,'series'],info.loc[hb,'num']; ps,pn=info.loc[pb,'series'],info.loc[pb,'num']
    if hs: cnt['hold_in_series']+=1
    if hs and hs==ps: cnt['same_series_as_prev']+=1
    # rule: next unread books of the series of the most recent liked book (up to 10)
    if ps:
        seen=set(hist.book_id.tolist())
        nxt=[bid for bid,num in by_series.get(ps,[]) if num>pn and bid not in seen][:10]
        if nxt:
            cnt['rule_fires']+=1; cnt['rule_hit']+= hb in nxt
print(cnt)
json.dump(cnt,open('series.json','w'))
