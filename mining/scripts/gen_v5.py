import json

# xAdL5vmN 精确复刻：单字段 earnings surprise，sharpe 4.51, ra_failed:false
# 模板: ts_decay_linear(signed_power(subtract(group_rank(vec_avg(F), subindustry), 0.5), 5), 90)
# 账户已占用: 无后缀(xAdL5vmN), _7(6XpMb0aG) => 新挖 _1.._6
TEMPLATE = "ts_decay_linear(signed_power(subtract(group_rank(vec_avg({F}), subindustry), 0.5), 5), 90)"
SETTINGS = {
    "instrumentType": "EQUITY",
    "region": "USA",
    "universe": "TOP3000",
    "delay": 1,
    "decay": 6,
    "neutralization": "SLOW_AND_FAST",
    "truncation": 0.08,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "ON",
    "maxTrade": "ON",
    "maxPosition": "OFF",
    "language": "FASTEXPR",
    "visualization": False,
    "startDate": "2014-01-01",
    "endDate": "2023-12-31",
}

alphas = []
for h in [1, 2, 3, 4, 5, 6]:
    f = f"historic_earnings_surprise_score_{h}"
    alphas.append({
        "type": "REGULAR",
        "regular": TEMPLATE.format(F=f),
        "settings": dict(SETTINGS),
    })

out = "C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/data/alpha_list_usa_d1_sentiment_v5.json"
with open(out, "w") as fh:
    json.dump(alphas, fh, indent=2)
print(f"wrote {len(alphas)} candidates to {out}")
for a in alphas:
    print(" ", a["regular"])
