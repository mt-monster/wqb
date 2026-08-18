import json
P = r"d:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json"
st = json.load(open(P, encoding="utf-8"))
st["wave16_multisims"] += [
 {"wave":"wave22K","id":"yLEDk4Qn4j89GNPLGkGnRq","dataset":"model170","setting":"SECTOR d8 t0.06",
  "exprs":8,"style":"三腿融合权重矩阵+decay8攻fitness","status":"submitted","submitted":"2026-08-15"},
 {"wave":"wave22L","id":"4pZI9fcD94XfaMV9LIyDHaq","dataset":"model170","setting":"SECTOR d6 t0.08",
  "exprs":8,"style":"三腿融合 decay6 t0.08对照","status":"submitted","submitted":"2026-08-15"}]
st["pipeline_note"] = "model170三腿(EM+APdiff+upside)批K/L在飞; 双腿最佳sh1.20/fit0.76/2y1.58/rn1.50"
json.dump(st, open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("K/L recorded")
