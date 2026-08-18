# -*- coding: utf-8 -*-
import json, sys
data = json.load(open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\7d427548\a56e8bb0.txt', encoding='utf-8'))
ids = ['FkJB4bB4pk8y1ngbd0ogK','RbJIVa8m4wr9MF1gSayVqeo','3v43ME3rZ4jMbDVf7hqaFPc','GHbsY7Cb59QchtMIpO6g0W','4GEZAy6b156ccGA11Opxh88Z','yUj9H3jK4OdbfvTrwqmoUo','3u9iFy7fC4QT9nj1gv0ihd0F','2Gb6HggU04nM8ysYdEwWScR']
ap = [x for x in data['results'] if x['id'] in ids]
print(f"找到 {len(ap)} 条 AP 批 alpha")
for a in ap:
    print(f"{a['id']}: sh={a['metrics']['sharpe']} fit={a['metrics']['fitness']} rn={a['metrics']['risk_neutralized_sharpe']} y2={a['metrics']['two_year_sharpe']} margin={a['metrics']['margin']} tv={a['metrics']['turnover']} ra_failed={a['ra']['ra_failed']}")
