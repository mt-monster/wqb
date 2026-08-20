# -*- coding: utf-8 -*-
import os
"""wave22-25 starmine 战役闭环：verdict 写入 + 台账回写"""
import json
from datetime import datetime

GBR = r"D:\coding\traeCN_project\wqb\tracking\GBR"

verdicts = {
    22: {
        "wave": 22,
        "dataset": "predictive_starmine",
        "total": 24,
        "backtested": 24,
        "conclusion": "starmine 参数扫描第一波（decay 6/8 + 14 条新变体）。24/24 全回测，无过闸。top e7zlGen6（av20 单信号 decay6）sh=1.51 2y=0.27——sh 主力但 2y 毒性；78jkmOkL（三向混合）sh=1.36 2y=1.68——2y 主力但 sh 低。确认 sh 与 2y 权衡矛盾：av20 抬 sh 毁 2y，fwdPE 反转抬 2y 拖 sh。需要两者混合。",
        "top": [
            {"id": "e7zlGen6", "code": "rank(ts_av_diff(ep_yield_pct_smest_fy2_3, 20))", "sharpe": 1.51, "fitness": 0.85, "two_year_sharpe": 0.27, "rn_fitness": 0.46},
            {"id": "78jkmOkL", "code": "三向混合", "sharpe": 1.36, "two_year_sharpe": 1.68, "rn_fitness": 0.46},
            {"id": "rKj1GkK1", "code": "fwdPE fy1_3 反转族", "sharpe": 1.31, "two_year_sharpe": 1.33, "rn_fitness": 0.64},
        ],
        "lessons": [
            "av20（ts_av_diff(ep_yield_pct_smest_fy2_3, 20)）是 sh 主力（1.51）但 2y=0.27 毒性，单信号必死",
            "fwdPE fy1_3 反转是 2y 主力（1.68-2.05）但 sh 低（1.3-1.36），单信号也过不了 sh 硬闸",
            "per-item settings 绕过 build_wave 历史去重：同表达式不同 settings 必须直接走 runner 不进 build_wave",
            "forward_pe_smest_fy2_3 不在字段白名单，fy2 的 fwdPE 只能用 ts_av_diff 变换后的 fy1_3",
        ],
        "next": "wave23 四向混合（av20+fwdPE反转+fy1水平+delta66）冲 1.58 线。",
    },
    23: {
        "wave": 23,
        "dataset": "predictive_starmine",
        "total": 24,
        "backtested": 24,
        "conclusion": "四向混合冲刺。24/24 全回测，无过闸。top A1lRzrAw（0.3 av20 四向 d4）sh=1.83 fit=1.19 但 2y=1.21（LOW_2Y_SHARPE）+ rn_f=0.67。8 条 sh≥1.67 全卡 2y/rn_f。四向混合 sh 已够但 2y 与 rn_fitness 双短板。",
        "top": [
            {"id": "A1lRzrAw", "code": "0.3 av20 四向", "sharpe": 1.83, "fitness": 1.19, "two_year_sharpe": 1.21, "rn_fitness": 0.67},
            {"id": "QP71zNxW", "code": "四向变体", "sharpe": 1.77, "two_year_sharpe": 1.09, "rn_fitness": 0.64},
            {"id": "RR7Jzlgb", "code": "四向变体", "sharpe": 1.75, "two_year_sharpe": 1.2, "rn_fitness": 0.76},
        ],
        "lessons": [
            "四向混合 sh 天花板 1.83，但 2y 被 av20 毒性压低到 1.2 附近",
            "rn_fitness 成为新约束短板：decay 增大抬 2y 但降 rn_fitness，阈值 >0.7 严格大于",
            "权重再分配（av20 降到 0.3 以下）是同时抬 2y 和 rn_f 的方向",
        ],
        "next": "wave24 网格：四向权重 0.2-0.4 全网格 + decay 变体 + 门控变体。",
    },
    24: {
        "wave": 24,
        "dataset": "predictive_starmine",
        "total": 24,
        "backtested": 24,
        "conclusion": "权重网格突破。24/24 全回测，1 条过闸：GrlqxwKx（0.3 av20 四向 d4）sh=1.80 fit=1.28 2y=1.62 mg=10.1 tvr=13.0 rn=1.30 rn_f=0.71 fc=[]——战役首个硬闸全过候选。4 条 near-miss（rn_f 0.62-0.70）全卡 rn_fitness>0.7。0.3 av20 权重是 2y/rn_f 双过阈值的最优点。",
        "top": [
            {"id": "GrlqxwKx", "code": "add(0.3 * rank(ts_av_diff(ep_yield_pct_smest_fy2_3, 20)), 0.233 * multiply(rank(forward_pe_smest_fy1_3), -1), 0.233 * rank(ep_yield_pct_smest_fy1_3), 0.233 * rank(ts_delta(ep_yield_pct_smest_fy1_3, 66)))", "sharpe": 1.80, "fitness": 1.28, "two_year_sharpe": 1.62, "margin_bp": 10.1, "turnover_pct": 13.0, "rn_sharpe": 1.30, "rn_fitness": 0.71},
            {"id": "mLjP180E", "code": "0.25 四向 d4", "sharpe": 1.78, "two_year_sharpe": 1.66, "rn_fitness": 0.70},
            {"id": "58lZewAk", "code": "0.4 四向 d4", "sharpe": 1.84, "two_year_sharpe": 1.43},
        ],
        "lessons": [
            "0.3 av20 权重是甜点：0.25/0.2 系 rn_f 略低（0.67-0.70），0.4/0.5 系 2y 崩（1.38-1.43）",
            "rn_fitness 阈值 >0.7 严格大于，0.70 就是失败",
            "gate 用字符串数组格式（非对象数组），对象数组会 total=0",
        ],
        "next": "wave25 围绕 0.3 av20 结构微调：decay 3/5/6/7 + truncation 0.05/0.1 + 第三维权重微调 + 五向结构。",
    },
    25: {
        "wave": 25,
        "dataset": "predictive_starmine",
        "total": 24,
        "backtested": 24,
        "conclusion": "微调网格大丰收。24/24 全回测，11 条过闸（硬闸全过）。rnf 0.71-0.72 稳定，2y 1.61-1.76 全部过线，sh 1.77-1.81。最佳 A1lREYlR（0.3/0.267 fwdPE 强化 d5）sh=1.81 2y=1.76 rnf=0.71。0.3 av20 四向结构是稳定过闸面，wave24 GrlqxwKx 等价点（0.3/0.233 d4）复现 2 次（Jj7VrYpj/bljYAVLM）。",
        "top": [
            {"id": "A1lREYlR", "code": "0.3 av20 + 0.267 fwdPE 反转 + 0.217 fy1 + 0.217 delta66", "sharpe": 1.81, "fitness": 1.30, "two_year_sharpe": 1.76, "rn_fitness": 0.71},
            {"id": "6XlnN3pE", "code": "0.3 av20 + 0.25/0.225/0.225", "sharpe": 1.81, "two_year_sharpe": 1.69, "rn_fitness": 0.71},
            {"id": "0mwb5kl2", "code": "0.28 av20 + 0.24 等权", "sharpe": 1.77, "two_year_sharpe": 1.69, "rn_fitness": 0.71},
        ],
        "lessons": [
            "0.3 av20 四向结构在 decay 3-7 × 权重微调 × truncation 0.05-0.1 全域稳定过闸（rnf 0.71-0.72）",
            "五向结构（+fwdPE_av_diff66 反转）sh 1.82-1.84 但 2y 1.48-1.50 卡线，五向不如四向",
            "per-item truncation override 有效，0.1/0.05 均过闸",
            "同家族 12 个过闸点（wave24 1 + wave25 11）相互 self-corr 预计很高，提交需挑差异最大的 4 个",
        ],
        "next": "战役收尾：verdict 台账回写、查提交配额（remaining=4）、self-corr 检查后挑 4 个提交候选。",
    },
}

# 写 verdict 文件
for w, v in verdicts.items():
    path = GBR + rf"\reviews\wave{w}_verdict.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)
    print(f"verdict wave{w} written")

# 台账回写
import sys
sys.path.insert(0, os.environ.get("WQ_TOOLKIT", os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts")))
from _lib.ledger import LedgerStore

store = LedgerStore(GBR + r"\gbr_d1_campaign_state.json")
now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def mut(d):
    ws = d.setdefault("waves", {})
    for w, v in verdicts.items():
        key = str(w)
        if key not in ws:
            ws[key] = {}
        ws[key]["dataset"] = "predictive_starmine"
        ws[key]["note"] = v["conclusion"][:200]
        ws[key]["at"] = now
        d[f"wave{w}_verdict"] = v
    # 过闸候选汇总
    passed = [
        {"id": "GrlqxwKx", "wave": 24, "sharpe": 1.80, "two_year_sharpe": 1.62, "rn_fitness": 0.71},
        {"id": "A1lREYlR", "wave": 25, "sharpe": 1.81, "two_year_sharpe": 1.76, "rn_fitness": 0.71},
        {"id": "6XlnN3pE", "wave": 25, "sharpe": 1.81, "two_year_sharpe": 1.69, "rn_fitness": 0.71},
        {"id": "0mwb5kl2", "wave": 25, "sharpe": 1.77, "two_year_sharpe": 1.69, "rn_fitness": 0.71},
        {"id": "O071gwY7", "wave": 25, "sharpe": 1.79, "two_year_sharpe": 1.66, "rn_fitness": 0.72},
        {"id": "N17X8WwX", "wave": 25, "sharpe": 1.78, "two_year_sharpe": 1.65, "rn_fitness": 0.71},
        {"id": "qMjKVkrv", "wave": 25, "sharpe": 1.79, "two_year_sharpe": 1.62, "rn_fitness": 0.72},
        {"id": "Jj7VrYpj", "wave": 25, "sharpe": 1.80, "two_year_sharpe": 1.62, "rn_fitness": 0.71},
        {"id": "bljYAVLM", "wave": 25, "sharpe": 1.80, "two_year_sharpe": 1.62, "rn_fitness": 0.71},
        {"id": "88lmX7la", "wave": 25, "sharpe": 1.79, "two_year_sharpe": 1.61, "rn_fitness": 0.71},
        {"id": "d5j2vgjX", "wave": 25, "sharpe": 1.80, "two_year_sharpe": 1.61, "rn_fitness": 0.71},
        {"id": "wpj8WOa2", "wave": 25, "sharpe": 1.78, "two_year_sharpe": 1.61, "rn_fitness": 0.71},
    ]
    d["starmine_passed_candidates"] = passed
    d["starmine_conclusion"] = (
        "starmine 参数扫描战役（wave22-25）收官：0.3 av20 四向混合结构在 decay 3-7 全域稳定过闸，"
        "共 12 个硬闸全过点（wave24 1 + wave25 11）。轮换路线（model238/sentiment27/shortinterest3）三败后，"
        "后备 starmine 扫描成功补齐 4+ 过闸 alpha。"
    )


store.update(mut)
print("ledger updated")
