import json
P = r"d:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json"
st = json.load(open(P, encoding="utf-8"))
st["wave16_multisims"].append({"wave":"wave22J","id":"91gFP2gm4Ef8yrw1kdY2U9","dataset":"model170",
    "setting":"SECTOR d6 t0.06","exprs":8,"style":"decay6降tvr+跨字段FE(隐含估值/昨收错定价)",
    "status":"submitted","submitted":"2026-08-15"})
st["pipeline_note"] = "model170: 批J(decay6+FE)在飞; 骨架sh1.20/fit0.71/2y1.56/rn1.48, 攻fitness+sh上限"
json.dump(st, open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("J recorded")
