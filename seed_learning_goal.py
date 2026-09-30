#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""灌入学习目标管理台的预置示例数据（在线存储到资料库三张表）。
日期相对"今天"生成，使示例在首次打开时状态新鲜。"""
import subprocess, json, sys
from datetime import date, timedelta

SK = "D:/Program Files/WorkBuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/library"
DB_GOALS   = "RIlejxRPY9GvJ1pfAiGvgN"
DB_CHECKINS= "4LlAsS4BNqOrdDcTSV42od"
DB_WEEKLY  = "9HSCD1xNXZoSThAP1a8pYM"

T = date(2026, 9, 29)  # 今天

def d(n):  # T + n 天 -> 'YYYY-MM-DD'
    return (T + timedelta(days=n)).isoformat()

def run(db_id, records):
    payload = json.dumps({"database_id": db_id, "records": records}, ensure_ascii=False)
    cmd = [
        "python3", f"{SK}/database/batch_add_database_records.py",
        "--stdin",
    ]
    p = subprocess.run(cmd, input=payload, capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0:
        print("STDOUT:", p.stdout)
        print("STDERR:", p.stderr, file=sys.stderr)
        raise SystemExit(f"batch_add failed for {db_id}")
    # 解析结果，返回 id 列表
    try:
        out = json.loads(p.stdout)
    except Exception:
        print("RAW:", p.stdout)
        raise
    results = out.get("results", [])
    ids = [r.get("id") for r in results]
    fails = [r for r in results if not r.get("success")]
    print(f"[batch_add {db_id}] total={len(ids)} fails={len(fails)}")
    if fails:
        print("  FAILS:", fails[:5])
    return ids

# ---------- 目标 ----------
goals = [
    {
        "名称": {"text": "背英语单词"},
        "单位": {"text": "个"},
        "总量": {"number": 2500},
        "截止日": {"date": d(30)},
        "创建日": {"date": d(-25)},
        "配色": {"text": "#6366f1"},
        "障碍": {"text": ""},
        "对策": {"text": ""},
        "示例": {"checkbox": True},
    },
    {
        "名称": {"text": "读《人类简史》"},
        "单位": {"text": "页"},
        "总量": {"number": 440},
        "截止日": {"date": d(-8)},     # 已逾期 -> 红卡
        "创建日": {"date": d(-40)},
        "配色": {"text": "#059669"},
        "障碍": {"text": "工作太忙、通勤很累，晚上没力气读"},
        "对策": {"text": "午休读 15 分钟、周末集中补读 30 页"},
        "示例": {"checkbox": True},
    },
    {
        "名称": {"text": "Python 入门课"},
        "单位": {"text": "节"},
        "总量": {"number": 45},
        "截止日": {"date": d(5)},
        "创建日": {"date": d(-14)},
        "配色": {"text": "#0ea5e9"},
        "障碍": {"text": ""},
        "对策": {"text": "每天固定晚 9 点学一节"},
        "示例": {"checkbox": True},
    },
]

print("== 插入目标 ==")
goal_ids = run(DB_GOALS, goals)
assert len(goal_ids) == 3, f"目标插入不全: {goal_ids}"
g1, g2, g3 = goal_ids
print("  goal ids:", goal_ids)

# ---------- 打卡记录 ----------
logs = []

# g1 背单词：T-25 .. T-1 全勤，每天 80 个（长连续、在轨）
for n in range(-25, 0):
    logs.append({
        "目标ID": {"text": g1},
        "日期": {"date": d(n)},
        "数量": {"number": 80},
        "分钟": {"number": 25},
        "补记": {"checkbox": False},
        "备注": {"text": ""},
        "示例": {"checkbox": True},
    })

# g2 人类简史：拖后 + 连续漏打 + 障碍预案 + 补记
#   T-40..T-5 每日 10 页；T-4 漏；T-3/T-2 补；T-1 漏（连续漏打）
#   其中 T-20 标记为补记（补填更早漏掉的一天）
g2_days = list(range(-40, -5 + 1))  # -40 .. -5
g2_days += [-3, -2]                 # 补回两天
for n in g2_days:
    makeup = (n == -20)
    logs.append({
        "目标ID": {"text": g2},
        "日期": {"date": d(n)},
        "数量": {"number": 10},
        "分钟": {"number": 20},
        "补记": {"checkbox": makeup},
        "备注": {"text": "补记前一天落下的量" if makeup else ""},
        "示例": {"checkbox": True},
    })

# g3 Python：T-14..T-2 全勤（含本周），T-1 用掉本周休息日 -> 今天琥珀休息卡
for n in range(-14, -2 + 1):  # -14 .. -2
    logs.append({
        "目标ID": {"text": g3},
        "日期": {"date": d(n)},
        "数量": {"number": 3},
        "分钟": {"number": 40},
        "补记": {"checkbox": False},
        "备注": {"text": ""},
        "示例": {"checkbox": True},
    })

print(f"== 插入打卡记录（共 {len(logs)} 条，分批）==")
CHUNK = 90
for i in range(0, len(logs), CHUNK):
    run(DB_CHECKINS, logs[i:i+CHUNK])

# ---------- 周复盘（历史周，样例） ----------
def monday_of(dt):
    return dt - timedelta(days=(dt.weekday()))  # weekday(): Mon=0

weekly = []
for wk_offset in (-21, -14, -7):
    ws = monday_of(T + timedelta(days=wk_offset))
    invest, days, mins, keep, problem, try_, nxt = {
        -21: (120, 7, 280, "单词和阅读都保持了节奏", "周末有点赶", "工作日早起半小时", "把人类简史读到 250 页"),
        -14: (135, 7, 320, "Python 入门课跟上进度", "通勤累影响晚上状态", "午休读 15 分钟书", "人类简史补上落下的 30 页"),
        -7:  (150, 7, 360, "三门目标都有打卡", "人类简史进度偏慢", "每天多读 2 页", "本周把人类简史追平计划"),
    }[wk_offset]
    weekly.append({
        "周起始": {"date": ws.isoformat()},
        "投入量": {"number": invest},
        "打卡天数": {"number": days},
        "分钟数": {"number": mins},
        "保持": {"text": keep},
        "问题": {"text": problem},
        "尝试": {"text": try_},
        "下周预案": {"text": nxt},
        "示例": {"checkbox": True},
    })

print("== 插入周复盘 ==")
run(DB_WEEKLY, weekly)

print("\n全部示例数据写入完成。")
