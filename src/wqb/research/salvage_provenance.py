"""Resolve rescue candidates to exact alpha provenance; unknown is not orthogonal."""
from __future__ import annotations


def resolve_salvage_entries(conn, region, entries):
    resolved = []
    for original in entries:
        entry = dict(original)
        alpha_id = entry.get("alpha_id")
        datasets = set()
        if alpha_id:
            for table in ("backtest_results", "expressions"):
                rows = conn.execute(
                    f"SELECT DISTINCT dataset FROM {table} WHERE region=? AND alpha_id=?",
                    (region, alpha_id),
                ).fetchall()
                datasets.update(r[0] for r in rows if r[0] and r[0] != region)
        if datasets:
            entry["dataset_provenance"] = "exact_alpha_db"
        elif entry.get("dataset") and entry["dataset"] != region:
            datasets.add(entry["dataset"])
            entry["dataset_provenance"] = "ledger"
        else:
            entry["dataset_provenance"] = "unknown"
        entry["datasets"] = sorted(datasets)
        entry["dataset"] = next(iter(datasets)) if len(datasets) == 1 else None
        resolved.append(entry)
    return resolved
