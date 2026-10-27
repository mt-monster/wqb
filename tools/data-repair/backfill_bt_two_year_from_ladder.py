# -*- coding: utf-8 -*-
"""把 `backtest_results.two_year_sharpe` 从已存 payload 的 `is_ladder_sharpe` 补齐。

## 为什么需要
平台对 2Y 读数有**两个载体**（`wqb.config.RA_2Y_NAMES` 同时收录）：
`LOW_2Y_SHARPE` 与 `IS_LADDER_SHARPE`。部分区域/alpha 代际只发后者，而采集层
（`tools/harvest_multisim.py::_extract_two_year_sharpe`、`wqb_db_mcp._flatten_platform_alpha`）
2026-10-23 前只认前者 ⇒ 这些行 `two_year_sharpe` 落空，`payload_json` 里却躺着
`is_ladder_sharpe` 的真值。

后果（IND/wave232 实测）：
- 字段画像 `best_2y` 低报（`count_institutional_sellers_security` 显示 −0.15，
  真值 2.87；`market_value_institutional_shares_disposed` 直接 NULL，真值 2.98）；
- 提交队列 / Mode B 判死规则（`two_year_sharpe_max`）读到 None ⇒ 静默跳过 2Y 证据。

## 口径
- **只补空值**：`two_year_sharpe IS NULL` 且 payload 的 `is_ladder_sharpe` 非空才动。
- **不臆造**：payload 没有 ladder 就跳过（宁缺勿错）。
- **合并式写入**：走 `CampaignStore.upsert_backtest_rows`（AGENTS.md §8.8：没带不等于清空），
  不直写 SQL。
- `--infer-dataset` 可选：按表达式里的字段反查 `fields` 表补 `dataset` 归属，
  **只补「与波自身所属数据集一致」的行**（波没有数据集、或反查结果是别的数据集 ⇒ 留 NULL 并报出来）。
  这条限制是为了不把波改指向别的数据集：`CampaignStore._ensure_wave` 在传 dataset 时会
  `UPDATE waves SET dataset_id=?`，给跨数据集探针波补归属会把整波改指。

## 用法
```bash
# 只看会改哪些行（默认 dry-run）
python tools/data-repair/backfill_bt_two_year_from_ladder.py --region IND --wave 232
# 真写
python tools/data-repair/backfill_bt_two_year_from_ladder.py --region IND --wave 232 --apply
# 顺带按字段反查补数据集归属（仅补与波自身数据集一致的行）
python tools/data-repair/backfill_bt_two_year_from_ladder.py --region IND --wave 232 \
    --infer-dataset --apply
```
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _bootstrap() -> Path:
    """仓库根（向上找 pyproject.toml + src/wqb 双标记），并把 src/ 放进 sys.path。"""
    here = Path(__file__).resolve()
    for p in (here, *here.parents):
        if (p / "pyproject.toml").is_file() and (p / "src" / "wqb").is_dir():
            src = str(p / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return p
    raise SystemExit("[error] 未找到仓库根（需要 pyproject.toml + src/wqb）")


REPO = _bootstrap()


def _ladder_of(payload: Dict[str, Any]) -> Optional[float]:
    """payload 里的 2Y 替代读数（ladder 优先，其次 metrics 里的同名字段）。"""
    for v in (payload.get("is_ladder_sharpe"),
              (payload.get("metrics") or {}).get("is_ladder_sharpe")):
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                continue
    return None


_TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

#: 到处都在用的环境字段，不能用来判数据集归属（每个 alpha 都写 returns）
_AMBIENT_FIELDS = {
    "returns", "close", "open", "high", "low", "volume", "vwap", "cap", "sharesout",
    "adv20", "country", "sector", "industry", "subindustry", "market", "exchange",
}


def _field_dataset_index(store, region: str) -> Dict[str, set]:
    """region 内 field_name → {dataset_name}（用于反查表达式归属）。"""
    idx: Dict[str, set] = defaultdict(set)
    for fname, dsname in store.connection.execute(
        "SELECT f.field_name, d.name FROM fields f JOIN datasets d ON f.dataset_id=d.id "
        "JOIN regions r ON d.region_id=r.id WHERE r.name=?",
        (region,),
    ):
        if fname:
            idx[fname].add(dsname)
    return idx


def _infer_dataset(code: str, idx: Dict[str, set]) -> Optional[str]:
    """表达式里所有非环境字段同属一个数据集时返回它；无字段/跨数据集返回 None。"""
    hits = set()
    for tok in set(_TOKEN.findall(code or "")):
        if tok in _AMBIENT_FIELDS:
            continue
        hits |= idx.get(tok, set())
    return next(iter(hits)) if len(hits) == 1 else None


def _wave_dataset_map(store, region: str) -> Dict[str, Optional[str]]:
    """wave_number → 该波已登记的数据集名（没有则 None）。"""
    out: Dict[str, Optional[str]] = {}
    for wave, ds in store.connection.execute(
        "SELECT w.wave_number, d.name FROM waves w JOIN regions r ON w.region_id=r.id "
        "LEFT JOIN datasets d ON w.dataset_id=d.id WHERE r.name=?",
        (region,),
    ):
        out[str(wave)] = ds
    return out




def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="从 payload.is_ladder_sharpe 补 backtest_results.two_year_sharpe")
    ap.add_argument("--region", required=True, help="区域，如 IND")
    ap.add_argument("--wave", default=None, help="只处理某波（缺省=全区）")
    ap.add_argument("--infer-dataset", action="store_true",
                    help="按表达式字段反查归属；只补与波自身数据集一致的行（推荐）")
    ap.add_argument("--apply", action="store_true", help="真写（缺省 dry-run）")
    ap.add_argument("--limit", type=int, default=0, help="最多处理多少行（0=不限）")
    args = ap.parse_args(argv)

    from wqb.store import CampaignStore

    store = CampaignStore(str(REPO / "data" / "wqb.db"))
    try:
        q = ("SELECT alpha_id, wave, dataset, payload_json FROM backtest_results "
             "WHERE region=? AND two_year_sharpe IS NULL")
        p: List[Any] = [args.region]
        if args.wave:
            q += " AND wave=?"
            p.append(str(args.wave))
        q += " ORDER BY wave, alpha_id"
        rows = store.connection.execute(q, p).fetchall()
        if args.limit:
            rows = rows[: args.limit]

        targets: List[Tuple[str, str, str, Dict[str, Any], float]] = []  # region, wave, ds, row, ladder
        skipped_no_payload = skipped_no_ladder = 0
        skipped_dataset = 0
        idx = _field_dataset_index(store, args.region) if args.infer_dataset else {}
        wave_ds = _wave_dataset_map(store, args.region) if args.infer_dataset else {}
        for alpha_id, wave, ds, payload_json in rows:
            if not payload_json:
                skipped_no_payload += 1
                continue
            try:
                payload = json.loads(payload_json)
            except (TypeError, ValueError):
                skipped_no_payload += 1
                continue
            ladder = _ladder_of(payload)
            if ladder is None:
                skipped_no_ladder += 1
                continue
            row = dict(payload)
            row["alpha_id"] = row.get("alpha_id") or alpha_id
            row["two_year_sharpe"] = ladder
            ds_target = ds or ""
            if not ds_target and args.infer_dataset:
                inferred = _infer_dataset(row.get("code") or row.get("expression") or "", idx)
                own = wave_ds.get(str(wave))
                # 只补与波自身数据集一致的行：传 dataset 会 UPDATE waves.dataset_id，
                # 给跨数据集探针补归属等于把整波改指（见模块 docstring）。
                if inferred and own and inferred == own:
                    ds_target = inferred
                else:
                    skipped_dataset += 1
            targets.append((args.region, str(wave), ds_target, row, ladder))

        print(f"[scan] {args.region}{' wave=' + str(args.wave) if args.wave else ''}: "
              f"待补 {len(targets)} 行 / 候选 {len(rows)} 行 "
              f"(无 payload {skipped_no_payload}, 无 ladder {skipped_no_ladder}"
              + (f", 归属不符/不明 {skipped_dataset}" if args.infer_dataset else "") + ")")
        for _r, wave, ds, row, ladder in targets[:40]:
            print(f"  wave={wave:>6}  ds={ds or '-':<18} {row['alpha_id']:<10} 2Y←{ladder}")
        if len(targets) > 40:
            print(f"  … 其余 {len(targets) - 40} 行略")

        if not args.apply:
            print("[dry-run] 未写库；加 --apply 执行")
            return 0
        if not targets:
            return 0

        groups: Dict[Tuple[str, str, Optional[str]], List[Dict[str, Any]]] = defaultdict(list)
        for region, wave, ds, row, _ladder in targets:
            groups[(region, wave, ds or None)].append(row)
        written = 0
        for (region, wave, ds), grow in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2] or "")):
            n = store.upsert_backtest_rows(region, wave, grow, dataset=ds)
            written += n
            print(f"[write] {region} wave={wave} ds={ds or '-'}: {n}/{len(grow)} 行")
        print(f"[done] 写入 {written} 行")
        return 0
    finally:
        store.close()


if __name__ == "__main__":
    raise SystemExit(main())
