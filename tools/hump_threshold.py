# -*- coding: utf-8 -*-
"""hump_threshold.py - hump 阈值按宇宙档位自适应（P2-2，2026-08-31）。

背景：hump(alpha, threshold)  dampens 极端股驱动的 Sharpe（解决 sub-universe Sharpe 失败），
YW79016 实证阈值 0.02 是 MEA/TOP300 的值。但小宇宙极端股权重更高，需更强阻尼；
大宇宙极端股被稀释，阻尼可放宽。当前所有区域共用一个阈值，存在区域适配缺口。

自适应规则（按 universe 档位）：
  TOP3000+ 大宇宙 -> 0.02（极端股被稀释，弱阻尼即可）
  TOP1000-2000 中宇宙 -> 0.03
  TOP500-600 中小宇宙 -> 0.04
  TOP300-400 小宇宙 -> 0.05（极端股权重高，强阻尼）

用法:
  # 查某宇宙档位的推荐 hump 阈值
  python tools/hump_threshold.py --universe TOP300
  python tools/hump_threshold.py --universe TOP3000

  # 给表达式自动包裹自适应 hump
  python tools/hump_threshold.py --universe TOP300 --expr "rank(ts_delta(close, 10))"

  # dry-run 全档位阈值表
  python tools/hump_threshold.py --table
"""
import argparse
import re

# universe 档位 -> (推荐 hump 阈值, 档位描述)
_UNIVERSE_HUMP = {
    "TOP3000": (0.02, "大宇宙，极端股被稀释，弱阻尼"),
    "TOP2000": (0.025, "中大宇宙"),
    "TOP1500": (0.03, "中宇宙"),
    "TOP1000": (0.03, "中宇宙"),
    "TOP700": (0.035, "中小宇宙"),
    "TOP600": (0.04, "中小宇宙"),
    "TOP500": (0.04, "中小宇宙"),
    "TOP400": (0.05, "小宇宙，极端股权重高，强阻尼"),
    "TOP300": (0.05, "小宇宙，极端股权重高，强阻尼"),
    "TOP200": (0.06, "极小宇宙"),
    "MINVOL1M": (0.03, "最小成交量 1M（中宇宙等效）"),
}

_DEFAULT_THRESHOLD = 0.03


def recommend_threshold(universe: str) -> tuple:
    """返回 (threshold, description)。未知档位用默认 0.03。"""
    u = (universe or "").upper()
    if u in _UNIVERSE_HUMP:
        return _UNIVERSE_HUMP[u]
    # 尝试解析 TOP<N> 数字
    m = re.match(r"TOP(\d+)", u)
    if m:
        n = int(m.group(1))
        if n >= 3000:
            return (0.02, "大宇宙（外推）")
        if n >= 1000:
            return (0.03, "中宇宙（外推）")
        if n >= 500:
            return (0.04, "中小宇宙（外推）")
        return (0.05, "小宇宙（外推）")
    return (_DEFAULT_THRESHOLD, f"未知档位 {universe}，用默认 {_DEFAULT_THRESHOLD}")


def wrap_hump(expr: str, universe: str) -> str:
    """给表达式包裹自适应 hump（若已含 hump 则不重复包裹）。"""
    if "hump(" in expr:
        return expr
    thr, _ = recommend_threshold(universe)
    return f"hump({expr}, {thr})"


def print_table():
    print("universe 档位 -> 推荐 hump 阈值（P2-2 自适应）")
    print(f"{'universe':<12} {'threshold':>10}  说明")
    for u, (thr, desc) in sorted(_UNIVERSE_HUMP.items(),
                                 key=lambda kv: -int(re.sub(r'\D', '', kv[0]) or 0)):
        print(f"{u:<12} {thr:>10}  {desc}")
    print(f"{'(未知)':<12} {_DEFAULT_THRESHOLD:>10}  默认值")


def main():
    ap = argparse.ArgumentParser(description="hump 阈值按宇宙档位自适应（P2-2）")
    ap.add_argument("--universe", default=None, help="宇宙档位（如 TOP300）")
    ap.add_argument("--expr", default=None, help="给表达式自动包裹自适应 hump")
    ap.add_argument("--table", action="store_true", help="打印全档位阈值表")
    a = ap.parse_args()

    if a.table:
        print_table()
        return
    if not a.universe:
        ap.error("需要 --universe 或 --table")
    thr, desc = recommend_threshold(a.universe)
    print(f"[hump] {a.universe}: 推荐阈值 {thr}（{desc}）")
    if a.expr:
        wrapped = wrap_hump(a.expr, a.universe)
        print(f"[hump] 包裹后: {wrapped}")


if __name__ == "__main__":
    main()
