"""Parse a create_multi_simulation MCP result file and print key metrics."""
import json
import sys
from pathlib import Path


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
        print(
            f"{i:>2}  "
            f"{m.get('sharpe',''):>6}  "
            f"{m.get('fitness',''):>5}  "
            f"{m.get('two_year_sharpe',''):>6}  "
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python parse_simresult.py <result-file>")
        sys.exit(1)
    main(sys.argv[1])
