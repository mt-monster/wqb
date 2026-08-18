# -*- coding: utf-8 -*-
"""wave26-28 判弱 verdict + 台账回写（pattern_scores/model264/news104 判死）"""
import json
from datetime import datetime

GBR = r"D:\coding\traeCN_project\wqb\tracking\GBR"

verdicts = {
    26: {
        "wave": 26,
        "dataset": "pattern_scores",
        "total": 24,
        "backtested": 24,
        "conclusion": "技术形态相似度数据集判弱。24/24 全回测，top asc_triangle_mean_simscore sh=0.13，全部 |sh|<0.6 且多数为负。图表形态相似度评分在 GBR D1 TOP700 无 alpha（形态信号本身无方向性信息或已被套利）。判死。",
        "top": [
            {"id": "0mwbaoP2", "code": "rank(asc_triangle_mean_simscore_lookback120)", "sharpe": 0.13, "fitness": 0.03, "two_year_sharpe": 0.63},
        ],
        "lessons": [
            "pattern_scores 形态相似度字段方向性极弱（sh 正负混杂接近 0），GBR D1 无 alpha",
            "技术形态类数据集探针 1 轮 24 条足以判定天花板（全弱即判死，不必二轮）",
        ],
        "next": "判死，转 model264。",
    },
    27: {
        "wave": 27,
        "dataset": "model264",
        "total": 24,
        "backtested": 24,
        "conclusion": "ML 趋势概率数据集判弱。24/24 全回测，top rank(mdl264_es_ebit_fy1_r1m_l3) sh=0.22。es 组 l3（move-up 概率）、1l 组技术趋势概率、news 情绪趋势概率全部 |sh|<0.25。ML 预测的趋势概率在 GBR D1 TOP700 无 alpha。判死。",
        "top": [
            {"id": "0mwbaJVk", "code": "rank(mdl264_es_ebit_fy1_r1m_l3)", "sharpe": 0.22, "fitness": 0.07, "two_year_sharpe": 0.41},
        ],
        "lessons": [
            "model264 的 l1/l2/l3 三分类趋势概率与 1l 单概率字段均无 alpha（sh<0.25）",
            "es 组字段命名只有 ebit/ebitda/roe/sale/vol（无 bps/cfps/dps l3），设计前必须查字段清单",
        ],
        "next": "判死，转 news104。",
    },
    28: {
        "wave": 28,
        "dataset": "news104",
        "total": 12,
        "backtested": 12,
        "conclusion": "新闻情绪数据集判弱。12/12 全回测，top vec_avg(marketimpactscore) sh=0.30 tvr=61.9%。与 news20 判死一致：GBR 新闻情绪类信号天花板 ~0.3-0.83，远低于 1.58。GBR tier1 数据集至此全部挖穿。判死。",
        "top": [
            {"id": "lejLY052", "code": "rank(vec_avg(nws104_marketimpactscore))", "sharpe": 0.30, "fitness": 0.05, "two_year_sharpe": 1.23},
        ],
        "lessons": [
            "GBR 新闻情绪天花板确认：news20 0.83、news104 0.30，均远低于 1.58",
            "GBR tier1 全部挖穿：仅 starmine earnings 家族可达 1.58+，其余家族天花板 0.2-1.5",
        ],
        "next": "GBR 战役收官。4 个可提交评估见最终报告。",
    },
}

for w, v in verdicts.items():
    path = GBR + rf"\reviews\wave{w}_verdict.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)
    print(f"verdict wave{w} written")

import sys
sys.path.insert(0, r"C:\Users\MENGTAO\.qoder-cn\skills\wq-brain-campaign-toolkit\scripts")
from _lib.ledger import LedgerStore

store = LedgerStore(GBR + r"\gbr_d1_campaign_state.json")
now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def mut(d):
    ws = d.setdefault("waves", {})
    for w, v in verdicts.items():
        key = str(w)
        if key not in ws:
            ws[key] = {}
        ws[key]["dataset"] = v["dataset"]
        ws[key]["note"] = v["conclusion"][:200]
        ws[key]["at"] = now
        d[f"wave{w}_verdict"] = v
    dd = d.setdefault("dead_datasets", {})
    dd["pattern_scores"] = {"at": now, "reason": "probe 24/24 all weak, top sh=0.13; chart-pattern similarity no alpha in GBR D1"}
    dd["model264"] = {"at": now, "reason": "probe 24/24 all weak, top sh=0.22; ML trend-probability no alpha in GBR D1"}
    dd["news104"] = {"at": now, "reason": "probe 12/12 all weak, top sh=0.30; GBR news sentiment ceiling confirmed low"}
    dd["pv29"] = {"at": now, "reason": "cluster-label only fields, not a signal source"}
    dd["pv30"] = {"at": now, "reason": "GROUP pca/cluster labels only, not rankable signal source"}
    d["gbr_tier1_exhausted"] = {
        "at": now,
        "note": "GBR tier1 全部挖穿：starmine 1 ACTIVE + 11 同族硬闸全过；其余数据集（model53/analyst9/news20/news104/fund_holdings_panel/model238/sentiment27/shortinterest3/pattern_scores/model264/other455/pv29/pv30）全部判弱或判死。非 earnings 家族 sh 天花板 0.2-1.5 < 1.58。",
    }


store.update(mut)
print("ledger updated")
