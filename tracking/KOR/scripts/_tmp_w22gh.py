import json
P = r"d:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json"
st = json.load(open(P, encoding="utf-8"))
ms = st["wave16_multisims"]
ms.append({"wave":"wave22G","id":"ee20leWz4lBascbeCAFmA4","dataset":"model170","setting":"SECTOR d4 t0.06",
           "exprs":8,"style":"绿灯深挖: EM镜像窗口+AP窗口+双/三腿融合","status":"submitted","submitted":"2026-08-15"})
ms.append({"wave":"wave22H","id":"4EDpBY1BX5focD8qr03CGVX","dataset":"model170","setting":"INDUSTRY d4 t0.06",
           "exprs":8,"style":"绿灯深挖INDUSTRY对照","status":"submitted","submitted":"2026-08-15"})
st["pipeline_note"] = "model170绿灯2.84: 深挖批G/H在飞(16式); 重点=双腿融合EM水平x AP-av_diff10(互补频率)+镜像方向验证"
json.dump(st, open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("G/H recorded")
