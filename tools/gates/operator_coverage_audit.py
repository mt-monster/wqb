#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""算子覆盖审计 —— 把「用算子必须考虑所有可能情况」变成机械步骤，而不是靠人记。

纪律（用户 2026-10-09 明令）
--------------------------------
**用算子时，务必把所有可能的算子情况都考虑到。** 落在两处强制动作：

1. **设计新批次之前** —— 先跑 ``--checklist``，把平台 REGULAR 可用算子清单**逐类过一遍**，
   对每个类别问一句「这个类别在本信号上有没有可能出东西」，而不是凭直觉挑几个熟算子。
2. **宣称「方向穷尽」之前** —— 必须跑本工具审计覆盖率；**覆盖率不足即不得宣称穷尽**，
   正确表述是「已用算子集合内穷尽」。

为什么必须机械化（实证）
--------------------------------
2026-10-09 DEU 战役：连续 26 批 148 条表达式后曾表述「结构/字段/持仓/门控四路穷尽」，
事后对账发现**只用了 33 个算子，而平台 REGULAR 可用 84 个 ⇒ 51 个从未试过**
（含 ``group_backfill``/``log``/``pasteurize``/``days_from_last_change``/``vec_count`` 等有明确假设的算子）。
即「穷尽」是**错觉**，根因就是没有做过一次算子对账。

数据源
------
权威清单 = ``docs/reference/operators_catalog.json``（由 ``tools/refresh_operator_catalog.py``
把 MCP ``get_operators`` 的实时输出刷进来）。本工具**不自己联网**，只读这份目录，
所以在 MCP 断连时仍可用。

用法
----
::

    # ① 设计前 checklist：按类别列出全部 REGULAR 算子 + 一句「何时用」
    python tools/gates/operator_coverage_audit.py --checklist
    python tools/gates/operator_coverage_audit.py --checklist --category "Time Series"

    # ② 审计已用覆盖率（支持 glob / 显式文件 / DB wave）
    python tools/gates/operator_coverage_audit.py --glob "cache/deu_w2*.json"
    python tools/gates/operator_coverage_audit.py --expr-file cache/x.txt cache/y.txt
    python tools/gates/operator_coverage_audit.py --wave W232 --region DEU

    # ③ 当闸用：覆盖率低于阈值即 exit 1（可挂到发批前）
    python tools/gates/operator_coverage_audit.py --glob "cache/w2*.json" --min-coverage 0.5

退出码：0 = 正常；1 = 覆盖率低于 ``--min-coverage``；2 = 参数/数据源错误。
"""
from __future__ import annotations

import argparse
import glob as _glob
import io
import json
import os
import re
import sqlite3
import sys
from collections import defaultdict
from typing import Dict, Iterable, List, Optional, Set, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG = os.path.join(ROOT, "docs", "reference", "operators_catalog.json")
DB = os.path.join(ROOT, "data", "wqb.db")

#: 非 REGULAR 通道（COMBO/SELECTION 专用）——不能用于 Regular Alpha 表达式
_NON_REGULAR_ONLY = {"combo_a", "self_corr", "generate_stats", "in", "universe_size"}

#: 关键算子的「何时用」提示（覆盖 high-yield + 易被忽略项）。清单模式下打印，防止漏想。
#: 只写**作用机制**，不写"推荐"，避免把设计带偏。
HINTS: Dict[str, str] = {
    # 缺失/稀疏处置
    "group_backfill": "组内 winsorized 均值填充缺失 → 稀疏事件型的「事前填充」"
                      "（⚠ nanHandling=ON 已把无事件填 0、无 NaN 可填 ⇒ 恒等，实测 2026-10-09）",
    "ts_backfill": "时序前向填充最近有效值（「随身卡片」）；只适用状态量，事件量禁用",
    "is_nan": "缺失指示；诊断「填充后并列块」必备（从未用过时优先补）",
    "ts_count_nans": "窗口内 NaN 计数 = 事件密度的反面",
    "vec_count": "VECTOR 元素个数 = 当日申报笔数（事件密度）",
    "vec_stddev": "单笔交易内部离散度",
    "vec_range": "单条记录内极差",
    # 尾部/异常值
    "tail": "把 (lower,upper) 中段压为 newval；修「中段无信息」并列块。"
            "⚠ 边界是**信号分布依赖**（分析师信号 0.10 最优 / 内部人 0.25 最优，实测）",
    "winsorize": "按标准差截尾；与 tail 常成对使用",
    "pasteurize": "去 INF + 宇宙外 → 减少 outlier（论坛实证 may help reduce outliers）",
    "log": "对数压缩右尾（论坛《基本面因子》帖实证助过 IS ladder）",
    "signed_power": "保号幂变换；<1 压中间、>1 放大尾部 —— 不牺牲 TO 的增强杠杆之一",
    "quantile": "秩 + 指定分布变换（gaussian/cauchy/uniform）压异常",
    # 标准化家族（**不同分布假设，须分别试**）
    "rank": "全市场秩 → 0-1（会翻转多空结构）",
    "zscore": "横截面 z 分数（保号、保幅度）",
    "normalize": "减市场均值，可选除截面 std 并 clamp",
    "scale": "缩放至账面规模；可分别指定多头/空头系数",
    "quantile": "（见上）",
    "group_rank": "组内秩；第 2 参**必须是 GROUP 类型**（数值表达式会报 unit 不兼容）",
    "group_zscore": "组内 z；与 group_rank 非保序 ⇒ 换用后相关性须重测",
    "group_scale": "组内 0-1 归一",
    "group_std_dev": "组内标准差",
    "group_sum": "组内求和",
    "group_mean": "组内（调和）均值",
    "group_count": "组内有效值个数",
    # 时序
    "ts_mean": "窗口均值（⚠ 事件型数据上会**除掉频率信息**，实测 Sharpe 1.44→0.73）",
    "ts_sum": "窗口累加（事件型保频率信息，优于 ts_mean）",
    "ts_std_dev": "窗口波动 = 分歧度/不确定性",
    "ts_zscore": "时序 z：风险调整后的偏离",
    "ts_ir": "时序信息比 mean/std",
    "ts_scale": "窗口 min-max 归一到 0-1",
    "ts_av_diff": "偏离自身均值；可恢复被归一化抹掉的幅度（margin 恢复手段）",
    "ts_delta": "与 d 日前之差 = 变化量",
    "ts_returns": "相对变化率",
    "ts_delay": "滞后取值",
    "ts_rank": "时序秩（当前值在窗口内的分位）",
    "ts_quantile": "时序秩 + 分位函数变换",
    "ts_decay_linear": "线性衰减平滑；d 是 self/prod 双旋钮，逐档实测",
    "days_from_last_change": "距上次变化的**天数** = 事件新鲜度（稀疏事件型天然信号）",
    "last_diff_value": "最近一次与当前不同的取值",
    "kth_element": "窗口内第 k 个值（可指定忽略项）",
    "ts_arg_max": "距窗口最大值的天数",
    "ts_arg_min": "距窗口最小值的天数",
    "ts_max_diff": "x − ts_max(x,d)",
    "ts_kurtosis": "窗口峰度（尾部厚度）",
    "ts_product": "窗口乘积（几何均值/复利）",
    "ts_corr": "两变量窗口相关（需第二变量）",
    "ts_covariance": "两变量窗口协方差（需第二变量）",
    "ts_regression": "时序回归参数（可提残差/slope/截距）",
    "hump": "限速器（降 TO）**非去相关器**；实测 TO 0.245→0.0042 同时 S 2.37→0.67 零和",
    "ts_target_tvr_decay": "按目标换手自动调 decay",
    "ts_target_tvr_hump": "按目标换手自动调 hump",
    # 结构/条件
    "trade_when": "条件持仓；⚠ 门控=减仓=降统计量，多数场景压 S（实测 8 种门控全部降 ladder）",
    "if_else": "条件赋值",
    "bucket": "按字段分箱造 GROUP 轴；箱必须**命名 + 双引号** range=\"0,1,0.1\"",
    "densify": "分组字段降桶（把稀疏 group 压成紧凑 idx）",
    "vector_neut": "对第二向量正交化（异源残差轴）",
    "group_cartesian_product": "两分组轴笛卡尔积 = 复合轴（从未用过时优先补）",
    "group_neutralize": "组内去均值；⚠ 内层粒度必须**严格细于**外层 setting，否则退化为恒等",
    "and": "复合条件（与）", "or": "复合条件（或）", "not": "条件取反",
    "equal": "相等判定", "not_equal": "不等判定",
    "less_equal": "≤", "greater_equal": "≥",
    "max": "逐元素取大（可与常数封顶）", "min": "逐元素取小（可与常数托底）",
    "abs": "绝对值", "sqrt": "平方根（等效 signed_power 0.5，但丢号）",
    "reverse": "取负", "inverse": "倒数（注意除零）",
    "power": "幂（非整数次会丢号，用 signed_power 保号）",
    "sign": "符号；⚠ 返回普通数值，**不能当 group 键**（实测 unit 不兼容）",
    "log": "（见上）",
    "add": "相加；⚠ 同一 add 内出现 ≥2 个不同信号字段即判混信号（同字段双窗合规）",
    "subtract": "相减", "multiply": "相乘", "divide": "相除（比值构造，分母加 ε 防除零）",
}


def _load_catalog() -> List[dict]:
    if not os.path.exists(CATALOG):
        raise SystemExit(f"[op-cov] 找不到算子目录 {CATALOG}；"
                         f"先用 tools/refresh_operator_catalog.py 刷入 get_operators 输出")
    d = json.load(io.open(CATALOG, encoding="utf-8"))
    ops = d.get("results") if isinstance(d, dict) else d
    if not isinstance(ops, list):
        raise SystemExit("[op-cov] 目录格式异常：期望 results 为 list")
    return ops


def _regular_ops(ops: Iterable[dict]) -> Dict[str, dict]:
    """只保留可用于 Regular Alpha 的算子（scope 含 REGULAR，排除 COMBO/SELECTION 专用）。"""
    out: Dict[str, dict] = {}
    for o in ops:
        name = (o.get("name") or "").strip()
        if not name or name in _NON_REGULAR_ONLY:
            continue
        scope = o.get("scope") or []
        if scope and "REGULAR" not in scope:
            continue
        out[name] = o
    return out


def _extract_used(texts: Iterable[str]) -> Set[str]:
    """从表达式文本提取算子名（形如 name( 的长 token）。"""
    used: Set[str] = set()
    for t in texts:
        if not t:
            continue
        used |= set(re.findall(r"\b([a-z_][a-z0-9_]*)\s*\(", t))
    return used


def _texts_from_glob(patterns: List[str]) -> Tuple[List[str], int]:
    texts, n = [], 0
    for pat in patterns:
        for p in sorted(_glob.glob(pat, recursive=True)):
            texts.extend(_texts_from_file(p))
            n += 1
    return texts, n


def _texts_from_file(path: str) -> List[str]:
    if path.endswith(".txt"):
        return [ln.strip() for ln in io.open(path, encoding="utf-8") if ln.strip()]
    try:
        d = json.load(io.open(path, encoding="utf-8"))
    except Exception:
        return []
    out: List[str] = []
    if isinstance(d, dict):
        for v in d.values():
            if isinstance(v, str):
                out.append(v)
            elif isinstance(v, dict):
                for k in ("expr", "expression", "code", "regular"):
                    if isinstance(v.get(k), str):
                        out.append(v[k])
    elif isinstance(d, list):
        for v in d:
            if isinstance(v, str):
                out.append(v)
            elif isinstance(v, dict):
                for k in ("expr", "expression", "code", "regular"):
                    if isinstance(v.get(k), str):
                        out.append(v[k])
    return out


def _texts_from_wave(wave: str, region: str) -> List[str]:
    if not os.path.exists(DB):
        raise SystemExit(f"[op-cov] 找不到 DB {DB}")
    con = sqlite3.connect(DB); con.execute("PRAGMA busy_timeout=60000")
    try:
        rows = con.execute(
            "SELECT code FROM backtest_results WHERE region=? AND wave=? AND code IS NOT NULL",
            (region, wave)).fetchall()
    finally:
        con.close()
    return [r[0] for r in rows]


def cmd_checklist(ops: Dict[str, dict], category: Optional[str]) -> int:
    by_cat: Dict[str, List[str]] = defaultdict(list)
    for name, o in ops.items():
        cat = (o.get("category") or "Uncategorized").strip()
        if category and category.lower() not in cat.lower():
            continue
        by_cat[cat].append(name)
    total = sum(len(v) for v in by_cat.values())
    print(f"=== 算子检查清单（REGULAR 可用 {total} 个）===")
    print("用法：逐类问一句「这个类别在本信号上有没有可能出东西」，再决定试哪几个。\n")
    for cat in sorted(by_cat, key=lambda c: (-len(by_cat[c]), c)):
        names = sorted(by_cat[cat])
        print(f"【{cat}】{len(names)} 个")
        for n in names:
            h = HINTS.get(n, "")
            print(f"  - {n:<26}{('  ' + h) if h else ''}")
        print()
    print("⚠ 未在 HINTS 里给出机制说明的算子，须先读平台 description 再决定是否适用。")
    return 0


def audit(ops: Dict[str, dict], used: Set[str], min_coverage: float, src_desc: str) -> int:
    known = {n for n in used if n in ops}
    unknown = sorted(used - set(ops))
    # 平台外/内置关键字（如 sector/industry/close 等字段名也会被 name( 规则漏抓，这里不苛求）
    untried = sorted(set(ops) - known)
    cov = len(known) / len(ops) if ops else 0.0

    by_cat: Dict[str, List[str]] = defaultdict(list)
    for n in untried:
        by_cat[(ops[n].get("category") or "Uncategorized").strip()].append(n)

    print(f"=== 算子覆盖审计 ===  来源：{src_desc}")
    print(f"  平台 REGULAR 可用 : {len(ops)}")
    print(f"  本战役已用        : {len(known)}")
    print(f"  **从未用过**      : {len(untried)}")
    print(f"  覆盖率            : {cov:.1%}   （阈值 {min_coverage:.0%}）")
    if unknown:
        print(f"  ⚠ 出现但不在目录中 : {unknown[:12]}{' …' if len(unknown) > 12 else ''}")
    print()
    if untried:
        print("—— 从未用过的算子，按平台类别 ——")
        for cat in sorted(by_cat, key=lambda c: (-len(by_cat[c]), c)):
            names = sorted(by_cat[cat])
            print(f"  【{cat}】{len(names)} 个：{', '.join(names)}")
            hinted = [n for n in names if n in HINTS]
            for n in hinted:
                print(f"      · {n:<24}{HINTS[n]}")
    print()
    if cov < min_coverage:
        print(f"✗ 覆盖率 {cov:.1%} < {min_coverage:.0%} ⇒ **不得宣称「方向穷尽」**；"
              f"正确表述是「已用算子集合内（{len(known)}/{len(ops)}）穷尽」。")
        return 1
    print(f"✓ 覆盖率 {cov:.1%} ≥ {min_coverage:.0%}。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="算子覆盖审计（用算子必须考虑所有可能情况的机械化闸）")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--checklist", action="store_true", help="只打印全量 REGULAR 算子清单（设计前用）")
    g.add_argument("--glob", nargs="+", help="表达式来源 glob（json/txt）")
    g.add_argument("--expr-file", nargs="+", help="表达式来源文件")
    g.add_argument("--wave", help="从 DB backtest_results 取该 wave 的 code")
    ap.add_argument("--region", default="DEU", help="配合 --wave（缺省 DEU）")
    ap.add_argument("--category", help="--checklist 时按类别过滤（子串匹配）")
    ap.add_argument("--min-coverage", type=float, default=0.5,
                    help="覆盖率闸（缺省 0.5；低于即 exit 1）")
    a = ap.parse_args()

    ops = _regular_ops(_load_catalog())
    if a.checklist or not (a.glob or a.expr_file or a.wave):
        return cmd_checklist(ops, a.category)

    if a.glob:
        texts, nf = _texts_from_glob(a.glob)
        desc = f"glob {a.glob}（{nf} 文件 / {len(texts)} 表达式）"
    elif a.expr_file:
        texts = []
        for p in a.expr_file:
            texts.extend(_texts_from_file(p))
        desc = f"{len(a.expr_file)} 个文件 / {len(texts)} 表达式"
    else:
        texts = _texts_from_wave(a.wave, a.region)
        desc = f"DB wave={a.wave} region={a.region} / {len(texts)} 表达式"

    if not texts:
        print("[op-cov] 未取到任何表达式；检查 --glob/--expr-file/--wave 是否写对", file=sys.stderr)
        return 2
    return audit(ops, _extract_used(texts), a.min_coverage, desc)


if __name__ == "__main__":
    raise SystemExit(main())
