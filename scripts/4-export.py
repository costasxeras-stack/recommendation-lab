"""Combines the outputs of steps 1 to 3 into data/results.json for the results page."""
import json
s=json.load(open('summary.json')); f=json.load(open('res_full.json')); ex=json.load(open('examples.json')); se=json.load(open('series.json'))
c=f['cold']
curve={'item':[c['1']['item']['hit_rate'],c['3']['item']['hit_rate'],c['10']['item']['hit_rate'],f['full']['item']['hit_rate']],
       'svd':[c['1']['svd']['hit_rate'],c['3']['svd']['hit_rate'],c['10']['svd']['hit_rate'],f['full']['svd']['hit_rate']],
       'pop':[f['full']['pop']['hit_rate']]*4}
out=dict(summary=s,curve=dict(labels=['Last 1 book','Last 3 books','Last 10 books','Whole history'],**curve),
         series=dict(rule_fired=se['rule_fires'],rule_hit=se['rule_hit']),examples=ex)
json.dump(out,open('../data/results.json','w'),ensure_ascii=False)
print('wrote ../data/results.json')
