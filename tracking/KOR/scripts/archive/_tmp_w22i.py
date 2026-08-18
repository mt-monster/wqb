import json
P = r"d:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json"
st = json.load(open(P, encoding="utf-8"))
st["wave16_multisims"].append({"wave":"wave22I","id":"2Grr0x36a4XSaiJtyE2WIGn","dataset":"model170",
    "setting":"SECTOR d4 t0.06","exprs":8,"style":"双腿骨架参数精磨(权重/平滑/窗口/第三腿/ts_ir)",
    "status":"submitted","submitted":"2026-08-15"})
st["pipeline_note"] = "model170双腿骨架sh1.18/rn1.42确立; 批I精磨在飞: fitness(tvr)+2y双攻关"
json.dump(st, open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("I recorded")
