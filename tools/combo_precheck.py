# -*- coding: utf-8 -*-
"""combo_precheck.py - 组合预检串联工作流（P1-C + P1-D，2026-08-31）。

把组合质量的三个独立预检（P0-2 正交性 / P1-2 家族天花板 / P0-A 方向一致）
串成一个入口，外加 P1-D 的"主信号强度 -> 辅助腿数"建议，一行命令完成
组合前的全部质量判定。

用法:
  # 两腿组合预检（无回测数据：静态检查）
  python tools/combo_precheck.py --expr-a "rank(ts_backfill(close, 66))" \
      --expr-b "rank(ts_delta(volume, 10))"

  # 两腿组合预检（有 IS 回测 Sharpe：方向检查升级为硬判定）
  python tools/combo_precheck.py --expr-a "..." --expr-b "..." \
      --sharpe-a 1.24 --sharpe-b -0.38

  # 批量组合预检（>=3 条：家族天花板也生效）
  python tools/combo_precheck.py --exprs-file candidates/combo.json

  # 主信号强度 -> 辅助腿数建议（独立查询）
  python tools/combo_precheck.py --advise --sharpe 1.24 --fitness 0.82 --two-year 1.30

退出码: 0 = 预检全绿（或仅 WARN），1 = 存在硬违规（方向抵消/同族/天花板/Jaccard）
"""
import argparse
import json
import os
import sys

# 工作区 tools 目录保留在 sys.path（validator 在 src/wqb 下需经 WQB_WORKSPACE_ROOT）
_WORKSPACE = os.environ.get("WQB_WORKSPACE_ROOT") or os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
_SRC = os.path.join(_WORKSPACE, "src")
if os.path.isdir(_SRC) and _SRC not in sys.path:
    sys.path.insert(0, _SRC)


def _load_validator():
    try:
        from wqb.expression.validator import (
            check_combo_orthogonality, check_combo_direction, check_family_ceiling)
        return check_combo_orthogonality, check_combo_direction, check_family_ceiling
    except Exception as e:
        print(f"[combo_precheck] validator 导入失败: {e}", file=sys.stderr)
        return None, None, None


def advise_combo(sharpe=None, fitness=None, two_year=None,
                 prod_corr=None) -> dict:
    """P1-D 主信号强度 -> 辅助腿数建议（Mode B 四区域实证映射表）。

    实证基础（KOR 评级修正 / USA multifactor / IND Operating-Margin）：
      - 强  S>=1.5 且 F>=1.0  -> 0-1 腿（高正交腿）
      - 中  单项短板          -> 1 个高正交腿
      - 弱  多项不达标        -> 2+ 腿但成功率低，先判死评估
      - 无  S<0.8             -> 判死不组合

    返回 dict: {level, legs, advice, orthogonal_dim}
    """
    if sharpe is None:
        return {"level": "unknown", "legs": None,
                "advice": "缺少 Sharpe，无法判定主信号强度",
                "orthogonal_dim": None}
    weaknesses = []
    if fitness is not None and fitness < 1.0:
        weaknesses.append("Fitness<1.0")
    if two_year is not None and two_year < 1.58:
        weaknesses.append("2Y<1.58")
    if prod_corr is not None and prod_corr >= 0.7:
        weaknesses.append("PROD>=0.7")

    if sharpe >= 1.5 and (fitness is None or fitness >= 1.0):
        return {"level": "strong", "legs": "0-1",
                "advice": "主信号强，最多配 1 个高正交腿（周期/逻辑正交），过度组合反而引入噪声（USA Wave 20 教训）",
                "orthogonal_dim": "周期正交（慢×快）优先，其次跨金字塔数据集"}
    if sharpe >= 1.2:
        dims = []
        if "Fitness<1.0" in weaknesses:
            dims.append("结构正交：换骨架/加门控提 Fitness，而非堆腿")
        if "2Y<1.58" in weaknesses:
            dims.append("周期正交：补慢变量腿（基本面残差）延 2Y")
        if "PROD>=0.7" in weaknesses:
            dims.append("数据集正交：换信号族/数据集降 PROD")
        return {"level": "medium", "legs": "1",
                "advice": f"单项短板（{'; '.join(weaknesses) or '2Y/Fitness'}），配 1 个高正交腿补短板",
                "orthogonal_dim": dims[0] if dims else "周期正交（慢×快）"}
    if sharpe >= 0.8:
        return {"level": "weak", "legs": "2+",
                "advice": "多项不达标，组合成功率低；先过稳健性判死评估再决定是否投资配额",
                "orthogonal_dim": "跨金字塔层三腿（≥3 数据集验证上限）"}
    return {"level": "dead", "legs": None,
            "advice": "主信号无（S<0.8），任何组合无效（USA acquisition_model 教训），判死不组合",
            "orthogonal_dim": None}


def run_precheck(exprs, sharpe_map=None):
    """串联预检：正交性（两两）+ 方向一致（两两）+ 家族天花板（≥3 条时）。

    exprs: 表达式列表（2-N 条）
    sharpe_map: {expr: sharpe} 可选，提供后方向检查升级为硬判定
    返回 (ok, issues) — issues 为 [severity, msg] 列表，severity ∈ {"FAIL","WARN"}
    """
    ortho, direction, ceiling = _load_validator()
    if ortho is None:
        return False, [["FAIL", "validator 不可达，无法预检"]]
    issues = []
    n = len(exprs)
    if n < 2:
        return False, [["FAIL", "至少需要 2 条表达式"]]

    # 1. 两两正交性 + 方向
    for i in range(n):
        for j in range(i + 1, n):
            ea, eb = exprs[i], exprs[j]
            ok_o, reason_o, _ = ortho(ea, eb)
            if not ok_o:
                issues.append(["FAIL", f"L{i+1}×L{j+1} 正交性: {reason_o}"])
            sa = (sharpe_map or {}).get(ea)
            sb = (sharpe_map or {}).get(eb)
            ok_d, reason_d, det_d = direction(ea, eb, sharpe_a=sa, sharpe_b=sb)
            if not ok_d:
                issues.append(["FAIL", f"L{i+1}×L{j+1} 方向: {reason_d}"])
            elif det_d.get("static_flip_conflict") and not det_d.get("has_is_results"):
                issues.append(["WARN", f"L{i+1}×L{j+1} 静态翻转结构差异（未传入 Sharpe，仅提示）: {reason_d}"])

    # 2. 家族天花板（≥3 条才有效，2 条时 Jaccard 已覆盖共享字段风险）
    if n >= 3:
        ok_c, reason_c, _ = ceiling(exprs)
        if not ok_c:
            issues.append(["FAIL", f"家族天花板: {reason_c}"])

    hard = [m for s, m in issues if s == "FAIL"]
    return len(hard) == 0, issues


def main():
    ap = argparse.ArgumentParser(description="组合预检串联工作流（P1-C + P1-D）")
    ap.add_argument("--expr-a", default=None, help="腿 A 表达式")
    ap.add_argument("--expr-b", default=None, help="腿 B 表达式")
    ap.add_argument("--exprs-file", default=None, help="表达式列表 JSON（[{expression|expr:...}, ...] 或 纯字符串列表）")
    ap.add_argument("--sharpe-a", type=float, default=None, help="腿 A IS Sharpe（可选）")
    ap.add_argument("--sharpe-b", type=float, default=None, help="腿 B IS Sharpe（可选）")
    ap.add_argument("--sharpe-file", default=None,
                    help="Sharpe 映射 JSON（{expression: sharpe}），与 --exprs-file 配合")
    ap.add_argument("--advise", action="store_true", help="只输出组合建议（P1-D），需要 --sharpe 等")
    ap.add_argument("--sharpe", type=float, default=None, help="主信号 Sharpe（--advise 用）")
    ap.add_argument("--fitness", type=float, default=None, help="主信号 Fitness（--advise 用）")
    ap.add_argument("--two-year", type=float, default=None, help="主信号 2Y Sharpe（--advise 用）")
    ap.add_argument("--prod-corr", type=float, default=None, help="主信号 PROD 相关（--advise 用）")
    a = ap.parse_args()

    if a.advise:
        adv = advise_combo(a.sharpe, a.fitness, a.two_year, a.prod_corr)
        print(f"[combo] 主信号强度: {adv['level']}")
        print(f"[combo] 建议辅助腿: {adv['legs'] or '—'}")
        print(f"[combo] 建议: {adv['advice']}")
        if adv["orthogonal_dim"]:
            print(f"[combo] 正交维度: {adv['orthogonal_dim']}")
        return

    exprs = []
    if a.expr_a and a.expr_b:
        exprs = [a.expr_a, a.expr_b]
    elif a.exprs_file:
        if not os.path.isfile(a.exprs_file):
            print(f"[combo_precheck] 文件不存在: {a.exprs_file}", file=sys.stderr)
            sys.exit(1)
        data = json.load(open(a.exprs_file, encoding="utf-8"))
        for item in data:
            if isinstance(item, str):
                exprs.append(item)
            elif isinstance(item, dict):
                exprs.append(item.get("expression") or item.get("expr") or "")
    if not exprs:
        ap.error("需要 --expr-a/--expr-b 或 --exprs-file")

    sharpe_map = {}
    if a.sharpe_file:
        sharpe_map = json.load(open(a.sharpe_file, encoding="utf-8"))
    if a.sharpe_a is not None:
        sharpe_map[exprs[0]] = a.sharpe_a
    if a.sharpe_b is not None and len(exprs) >= 2:
        sharpe_map[exprs[1]] = a.sharpe_b

    ok, issues = run_precheck(exprs, sharpe_map)
    print(f"[combo_precheck] 预检 {len(exprs)} 条表达式: "
          f"{'全绿' if ok else '存在硬违规'}")
    for sev, msg in issues:
        print(f"  [{sev}] {msg}")
    if ok:
        print("[combo_precheck] 通过：可组合发批（回测后仍须核 SELF/PROD 相关）")
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()