"""Parse a create_multi_simulation MCP result file and print key metrics.

修复 (2026-08-18): 复合表达式(含 add/subtract/multiply)需额外抓 IS_LADDER 指标
- 复合表达式的 two_year_sharpe 在 metrics 中可能缺失, 需从 is_ladder 中提取
"""
import json
import re
import sys
from pathlib import Path


def _is_composite_expr(code: str) -> bool:
    """判断是否为复合表达式(含 add/subtract/multiply 等组合算子)"""
    composite_ops = {'add', 'subtract', 'multiply', 'divide'}
    # 提取所有函数名
    fns = set(re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code))
    return bool(fns & composite_ops)


def _extract_two_year_sharpe(alpha: dict) -> float:
    """提取 two_year_sharpe, 复合表达式需从 is_ladder 中抓取"""
    m = alpha.get('metrics', {})
    # 先尝试从 metrics 中直接获取
    tys = m.get('two_year_sharpe')
    if tys is not None:
        return tys
    
    # 复合表达式: 从 is_ladder 中提取
    code = alpha.get('code', '')
    if _is_composite_expr(code):
        is_ladder = alpha.get('is_ladder', {})
        if isinstance(is_ladder, dict):
            # is_ladder 结构: {'sharpe': [{'year': 2024, 'value': 1.23}, ...]}
            sharpe_list = is_ladder.get('sharpe', [])
            if isinstance(sharpe_list, list) and len(sharpe_list) >= 2:
                # 取最近两年的 sharpe 平均值
                recent = sharpe_list[-2:]
                values = [s.get('value', 0) for s in recent if isinstance(s, dict)]
                if values:
                    return sum(values) / len(values)
    
    return None


def main(path: str) -> None:
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    # Strip the prefix "The MCP server responded with: " if present.
    marker = "The MCP server responded with: "
    if marker in raw:
        raw = raw.split(marker, 1)[1]
    # The file content is wrapped: [{ "type":"text", "text": "<JSON string>" }]
    outer = json.loads(raw)
    inner_text = outer[0]["text"]
    data = json.loads(inner_text)

    print(f"multisim_id: {data.get('multisimulation_id')}")
    print(f"total_created: {data.get('total_created')}")
    print()

    header = (
        f"{'#':>2}  {'shrp':>6}  {'fit':>5}  {'2y':>6}  {'marg':>8}  "
        f"{'turn':>6}  {'rn_sh':>6}  {'rn_fit':>6}  {'rn_mrg':>7}  "
        f"{'ra':>3}  code"
    )
    print(header)
    print("-" * len(header))

    for i, a in enumerate(data["alpha_results"], 1):
        m = a.get("metrics", {})
        ra = a.get("ra", {})
        # rn_fitness / rn_margin not always present in summary; try get
        rn_fit = m.get("risk_neutralized_fitness")
        rn_mrg = m.get("risk_neutralized_margin")
        
        # 修复: 复合表达式需额外抓 IS_LADDER 指标
        tys = _extract_two_year_sharpe(a)
        tys_str = f"{tys:.2f}" if tys is not None else "-"
        
        print(
            f"{i:>2}  "
            f"{m.get('sharpe',''):>6}  "
            f"{m.get('fitness',''):>5}  "
            f"{tys_str:>6}  "
            f"{m.get('margin',''):>8}  "
            f"{m.get('turnover',''):>6}  "
            f"{m.get('risk_neutralized_sharpe',''):>6}  "
            f"{str(rn_fit if rn_fit is not None else '-'):>6}  "
            f"{str(rn_mrg if rn_mrg is not None else '-'):>7}  "
            f"{ra.get('failed_ra_count','-'):>3}  "
            f"{a.get('code','')}"
        )
        alpha_id = a.get("alpha_id") or a.get("id")
        print(f"     alpha_id={alpha_id}")
        failed_checks = ra.get("ra_failed_checks", [])
        if failed_checks:
            print(f"     ra_failed_checks: {', '.join(failed_checks)}")
        # 标记复合表达式
        if _is_composite_expr(a.get('code', '')):
            print(f"     [复合表达式] two_year_sharpe 从 IS_LADDER 提取")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python parse_simresult.py <result-file>")
        sys.exit(1)
    main(sys.argv[1])
