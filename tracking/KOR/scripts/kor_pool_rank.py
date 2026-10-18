"""Scan KOR IS alpha pool: find candidates blocked ONLY by prod/self.

Reads the get_user_alphas dump saved by MCP and ranks by
"distance to all-gates pass" = failed_ra_count first, then sharpe.

用法（仓库根下执行；dump 先用 MCP `get_user_alphas` 落盘再喂进来）：
  $WQ_PY tracking/KOR/scripts/kor_pool_rank.py <dump.json>

⚠ 为什么必须先落盘：`get_user_alphas` 单批返回体积极大（实测 50 条 ≈ 155 KB），
  直接进对话会挤爆上下文；且 KOR 的 `results[].datasets` 为空，归组只能靠解析
  `code` 字段前缀（SKILL.md「工程坑」）。本脚本只吃落盘文件，不发请求、不占配额。
"""
import json
import sys


def load(path):
    s = open(path, encoding="utf-8").read()
    i = s.find("{")
    return json.loads(s[i:s.rfind("}") + 1])


def main():
    path = sys.argv[1]
    d = load(path)
    rs = d.get("results", [])
    print(f"KOR IS pool: {len(rs)} shown (total={d.get('count')})\n")
    rows = []
    for r in rs:
        m = r.get("metrics") or {}
        ra = r.get("ra") or {}
        frc = ra.get("failed_ra_count")
        if frc is None:
            continue
        rows.append({
            "id": r.get("id"),
            "S": m.get("sharpe"),
            "F": m.get("fitness"),
            "2Y": m.get("two_year_sharpe"),
            "subU": m.get("sub_universe_sharpe"),
            "inv": m.get("investability_sharpe"),
            "TO": m.get("turnover"),
            "frc": frc,
            "fpc": ra.get("failed_ppa_count"),
            "fails": ",".join(ra.get("ra_failed_checks") or []),
            "date": (r.get("dateCreated") or "")[:10],
        })
    # best first: fewest failed gates, then highest sharpe
    rows.sort(key=lambda x: (x["frc"], -(x["S"] or -9)))
    print(f"{'id':<12}{'S':>6}{'F':>6}{'2Y':>6}{'subU':>6}{'inv':>6}{'TO':>8}{'frc':>5}{'fpc':>5}  fails")
    for x in rows[:40]:
        print(f"{x['id']:<12}{x['S'] if x['S'] is not None else '-':>6}"
              f"{x['F'] if x['F'] is not None else '-':>6}"
              f"{x['2Y'] if x['2Y'] is not None else '-':>6}"
              f"{x['subU'] if x['subU'] is not None else '-':>6}"
              f"{x['inv'] if x['inv'] is not None else '-':>6}"
              f"{x['TO'] if x['TO'] is not None else '-':>8}"
              f"{x['frc']:>5}{x['fpc'] if x['fpc'] is not None else '-':>5}  {x['fails']}")

    # group by failed-gate signature
    print("\n=== failed-gate signature clusters ===")
    sig = {}
    for x in rows:
        sig.setdefault(x["fails"], []).append(x)
    for k, v in sorted(sig.items(), key=lambda kv: -len(kv[1]))[:15]:
        best = max(v, key=lambda y: (y["S"] or -9))
        print(f"{len(v):>4}x  S<={best['S']}  [{k}]")


if __name__ == "__main__":
    main()