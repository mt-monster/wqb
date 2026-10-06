# -*- coding: utf-8 -*-
"""step9_audit.py — 步 9（S6）完成定义只读校验器（2026-10-02 新增）。

## 为什么有这只工具
`step9-writeback.md §9.7` 定了六项完成定义，并声明「**缺任何一项 = 本波未完成**」——
但此前**没有任何代码强制**：GEM 对 stale 先验快照只 WARN 不阻断，漏做 ⑥⑦⑧ 不报错，
只是下一波带着旧先验跑。GBR 实测快照落后 8 天（快照停 09-19，而 region_kb 已 09-25、
registry_empirical 已 09-26）就是这个静默退化的后果。

本工具把 §9.7 从「靠自律」变成「跑一条命令就知道缺什么」：
**只读**（经工厂 readonly=True 打开，跳过会改库头的 PRAGMA），不写库、不产生新数据。

## 校验项（与 §9.7 一一对应）
  1. `wave_results` 有本波记录，`status='closed'` 且 `verdict` 为枚举值
  2. key_findings 含点塔进度行、prod-first 是否跑过
  3. 有判死 → `dead_end` 已封存（本波 related）；有胜绩 → `win` 已写
  4. 本波候选全被 prod 墙卡死 → 已 `mark-saturated`
  5. 每个实际回测的数据集都已 `dataset-experience`
  6. `priors_snapshot_<region>` 不早于本次回写（`wave_results.updated_at`）

## 判据强度（防误判）
- 第 1 / 6 项是**硬判据**：可完全由 DB 断定。
- 第 2 / 3 / 4 / 5 项是**软判据**：`wave_results` 里没有「本波是否发生过判死 / 胜绩 / 饱和」
  的显式标记，只能间接推断（见每项 note）。因此默认 `--enforce warn` 只报告，
  `--enforce strict` 才把软判据也算作失败。
- **NULL / 缺失不判失败**：找不到证据时报 `unknown`（提示「无法核验」），不报 `fail`
  ——与预筛口径一致（缺失 ≠ 未做）。

用法：
    python tools/step9_audit.py --region KOR
    python tools/step9_audit.py --region KOR --wave 101
    python tools/step9_audit.py --region KOR --json
    python tools/step9_audit.py --region KOR --enforce strict   # 软判据也算失败（退出码 1）
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from typing import Any, Dict, List, Optional

_SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VERDICT_ENUM = ("PASS", "FAIL", "PARTIAL")
#: 软判据（无法由 DB 完全断定；strict 才计入失败）
SOFT_ITEMS = {"key_findings", "dead_end_win", "saturated", "dataset_experience"}


def resolve_db_path() -> str:
    try:
        from wqb.workflow._common import resolve_db_path as _r
        return _r()
    except Exception:
        return os.path.join(REPO_ROOT, "data", "wqb.db")


def _table_exists(conn, name: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone() is not None


def _ledger_get(conn, region: str, key: str) -> Optional[Any]:
    try:
        row = conn.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key=?", (region, key)
        ).fetchone()
    except sqlite3.Error:
        return None
    if not row:
        return None
    try:
        return json.loads(row[0])
    except Exception:
        return row[0]


def _item(ok: Optional[bool], detail: str, *, soft: bool = False, hint: str = "") -> Dict[str, Any]:
    """ok: True=通过 / False=失败 / None=无法核验（unknown，不判失败）"""
    status = "pass" if ok is True else "fail" if ok is False else "unknown"
    return {"status": status, "detail": detail, "soft": soft, "hint": hint}


def check_wave_row(conn, region: str, wave: Optional[str], latest_id: Optional[int]) -> Dict[str, Any]:
    """第 1 项：wave_results 有本波记录，closed 且 verdict 为枚举。"""
    if not _table_exists(conn, "wave_results"):
        return _item(None, "wave_results 表不存在")
    if wave is not None:
        row = conn.execute(
            "SELECT verdict, status, id FROM wave_results WHERE region=? AND wave_number=?",
            (region, str(wave)),
        ).fetchone()
    elif latest_id is not None:
        row = conn.execute(
            "SELECT verdict, status, id FROM wave_results WHERE id=?", (latest_id,)
        ).fetchone()
    else:
        row = None
    if not row:
        return _item(False, f"region={region} wave={wave or '(最近一行的 id=None)'} 无 wave_results 记录",
                     hint="先跑 ④ upsert_wave_result（key_findings 一次带齐）")
    verdict, status, _wid = row[0], row[1], row[2]
    if status != "closed":
        return _item(False, f"本波记录 status={status!r}（须 closed）",
                     hint="结论未定传 status='open'；已定则连同 verdict 一起写")
    if str(verdict or "").strip() not in VERDICT_ENUM:
        return _item(False, f"verdict={verdict!r} 不是枚举 {VERDICT_ENUM}",
                     hint="verdict 只接受 PASS/PARTIAL/FAIL；描述性文字放 key_findings")
    return _item(True, f"verdict={verdict} status=closed")


def check_key_findings(conn, region: str, wave: Optional[str], latest_id: Optional[int]) -> Dict[str, Any]:
    """第 2 项（软）：key_findings 含点塔进度行、prod-first 是否跑过。

    点塔行由 `campaign_intel.py pyramid` 产出，含 'pyramid' / '塔' / '点亮' 等字样；
    prod-first 记 'prod-first' / 'prod_first'。两者是**约定**，非强制格式 → 软判据。
    """
    if not _table_exists(conn, "wave_results"):
        return _item(None, "wave_results 表不存在", soft=True)
    if wave is not None:
        row = conn.execute(
            "SELECT key_findings FROM wave_results WHERE region=? AND wave_number=?",
            (region, str(wave)),
        ).fetchone()
    elif latest_id is not None:
        row = conn.execute(
            "SELECT key_findings FROM wave_results WHERE id=?", (latest_id,)
        ).fetchone()
    else:
        row = None
    if not row:
        return _item(None, "无记录", soft=True)
    try:
        findings = json.loads(row[0]) if row[0] else []
    except Exception:
        findings = []
    text = " ".join(str(f) for f in findings) if isinstance(findings, list) else str(row[0] or "")
    has_pyramid = any(k in text.lower() for k in ("pyramid", "塔", "点亮"))
    has_prod_first = any(k in text.lower() for k in ("prod-first", "prod_first", "prod first"))
    if has_pyramid and has_prod_first:
        return _item(True, "含点塔进度行 + prod-first 记录", soft=True)
    missing = []
    if not has_pyramid:
        missing.append("点塔进度行")
    if not has_prod_first:
        missing.append("prod-first 记录")
    return _item(False, f"key_findings 缺：{' / '.join(missing)}",
                 soft=True, hint="③ 点塔行须与其它 findings 在同一次 upsert 传入（整列替换）")


def check_dead_end_win(conn, region: str, wave: Optional[str]) -> Dict[str, Any]:
    """第 3 项（软）：有判死 → dead_end 已封存；有胜绩 → win 已写。

    `wave_results` 无「本波是否判死/胜绩」显式列：只能看 registry_empirical 里
    本波是否有 dead_end / win 条目（按 payload.source_waves 或 created_at 近似）。
    找不到时 unknown（可能本波确实没判死/胜绩，不能算失败）。
    """
    if not _table_exists(conn, "registry_empirical"):
        return _item(None, "registry_empirical 表不存在", soft=True)
    n_de = conn.execute(
        "SELECT COUNT(*) FROM registry_empirical WHERE region=? AND layer='dead_end'", (region,)
    ).fetchone()[0]
    n_win = conn.execute(
        "SELECT COUNT(*) FROM registry_empirical WHERE region=? AND layer='win'", (region,)
    ).fetchone()[0]
    return _item(None, f"本区 dead_end={n_de} / win={n_win}（历史累计；"
                       f"本波是否有判死/胜绩需人工核对 payload.source_waves）",
                 soft=True,
                 hint="有判死跑 seal_dead_end（先取证）；有胜绩跑 upsert_registry_empirical(layer='win')")


def check_saturated(conn, region: str) -> Dict[str, Any]:
    """第 4 项（软）：本波候选全被 prod 墙卡死 → 已 mark-saturated。

    只有「本波全部候选撞 prod 墙」才需此步；无饱和台账不等于失败 → unknown。
    """
    sat = _ledger_get(conn, region, "saturated_datasets")
    if sat and isinstance(sat, dict) and sat.get("datasets"):
        ds = list(sat["datasets"].keys())
        return _item(None, f"saturated_datasets 已有 {len(ds)} 集：{', '.join(ds[:5])}"
                           f"{'…' if len(ds) > 5 else ''}（是否含本波需人工核对）", soft=True)
    return _item(None, "无 saturated_datasets 台账（若非全波撞 prod 墙则正常）", soft=True,
                 hint="全波撞 prod 墙才需 campaign_intel.py mark-saturated --write-ledger")


def check_dataset_experience(conn, region: str, wave: Optional[str]) -> Dict[str, Any]:
    """第 5 项（软）：本波实际回测的数据集都已 dataset-experience。

    本波回测过的数据集从 backtest_results（region + wave）取；对照
    `reports/dataset_experience/<region>_<ds>_campain.md` 是否存在（注意历史拼写 campain）。
    """
    exp_dir = os.path.join(REPO_ROOT, "reports", "dataset_experience")
    if not _table_exists(conn, "backtest_results"):
        return _item(None, "backtest_results 表不存在", soft=True)
    if wave is not None:
        rows = conn.execute(
            "SELECT DISTINCT dataset FROM backtest_results WHERE region=? AND wave=? AND dataset IS NOT NULL",
            (region, str(wave)),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT DISTINCT dataset FROM backtest_results WHERE region=? AND dataset IS NOT NULL "
            "AND dataset != '_unknown' ORDER BY created_at DESC LIMIT 30",
            (region,),
        ).fetchall()
    datasets = sorted({r[0] for r in rows if r[0] and r[0] != "_unknown"})
    if not datasets:
        return _item(None, "无带 dataset 的回测记录（无法核对）", soft=True)
    missing = [ds for ds in datasets
               if not os.path.exists(os.path.join(exp_dir, f"{region.lower()}_{ds}_campain.md"))]
    if missing:
        return _item(False, f"{len(missing)}/{len(datasets)} 个数据集缺经验文件：{', '.join(missing[:5])}",
                     soft=True, hint="⑦ workflow_campaign(S6, dataset-experience) 逐个刷新")
    return _item(True, f"{len(datasets)} 个数据集均有 <region>_<ds>_campain.md", soft=True)


def check_priors_snapshot(conn, region: str, wave_updated_at: Optional[str]) -> Dict[str, Any]:
    """第 6 项（硬）：priors_snapshot_<region> 不早于本次回写。

    GEM 对 stale 快照只 WARN 不阻断，所以只能由这一步兜底（§9.7 原文）。
    """
    key = f"priors_snapshot_{region.lower()}"
    snap = _ledger_get(conn, region, key)
    if not snap:
        return _item(None, f"ledger 无 {key}（未跑过 assemble-priors）",
                     hint="⑧ workflow_campaign(S2, assemble-priors)")
    snap_ts = str((snap.get("generated_at") if isinstance(snap, dict) else "") or "").strip()
    if not snap_ts:
        return _item(None, f"{key} 存在但无 generated_at", hint="重跑 assemble-priors")
    if not wave_updated_at:
        return _item(None, f"snapshot={snap_ts}（无法核对先后：无 wave 回写时间戳）")
    # 字符串时间戳（ISO）可直接比大小；归一成同前缀再比
    if snap_ts[:19] >= str(wave_updated_at)[:19]:
        return _item(True, f"snapshot={snap_ts} ≥ 回写={str(wave_updated_at)[:19]}")
    return _item(False, f"snapshot={snap_ts} < 回写={str(wave_updated_at)[:19]}：本波结论未回流",
                 hint="⑧ 再跑一次 assemble-priors（GEM 对 stale 只 WARN，不会阻止你）")


def audit(conn, region: str, wave: Optional[str]) -> Dict[str, Any]:
    region = region.upper()
    latest_id = None
    wave_updated_at = None
    if _table_exists(conn, "wave_results"):
        if wave is not None:
            r = conn.execute(
                "SELECT id, updated_at FROM wave_results WHERE region=? AND wave_number=? ORDER BY id DESC LIMIT 1",
                (region, str(wave)),
            ).fetchone()
        else:
            r = conn.execute(
                "SELECT id, updated_at FROM wave_results WHERE region=? ORDER BY id DESC LIMIT 1", (region,)
            ).fetchone()
        if r:
            latest_id, wave_updated_at = r[0], r[1]

    items: Dict[str, Any] = {
        "wave_row": check_wave_row(conn, region, wave, latest_id),
        "key_findings": check_key_findings(conn, region, wave, latest_id),
        "dead_end_win": check_dead_end_win(conn, region, wave),
        "saturated": check_saturated(conn, region),
        "dataset_experience": check_dataset_experience(conn, region, wave),
        "priors_snapshot": check_priors_snapshot(conn, region, wave_updated_at),
    }
    hard_fail = [k for k, v in items.items() if v["status"] == "fail" and not v["soft"]]
    soft_fail = [k for k, v in items.items() if v["status"] == "fail" and v["soft"]]
    unknown = [k for k, v in items.items() if v["status"] == "unknown"]
    return {
        "region": region, "wave": wave, "items": items,
        "hard_fail": hard_fail, "soft_fail": soft_fail, "unknown": unknown,
        "complete": not hard_fail and not soft_fail,
    }


#: 项 → 显示名（§9.7 顺序）
_LABELS = {
    "wave_row": "①wave_results 有记录·closed·枚举 verdict",
    "key_findings": "②key_findings 含点塔行+prod-first",
    "dead_end_win": "③判死→dead_end / 胜绩→win",
    "saturated": "④全波撞 prod 墙→mark-saturated",
    "dataset_experience": "⑤每个回测数据集有经验文件",
    "priors_snapshot": "⑥assemble-priors 已再跑（快照不早于回写）",
}
_MARK = {"pass": "[OK]  ", "fail": "[FAIL]", "unknown": "[ ? ] "}


def render(res: Dict[str, Any], enforce: str) -> str:
    L: List[str] = []
    scope = res["region"] + (f" / wave={res['wave']}" if res.get("wave") else " / 最近一行")
    L.append("=" * 74)
    L.append(f"步 9（S6）完成定义审计 · {scope}   —— 只读校验（§9.7 六项）")
    L.append("=" * 74)
    for key, label in _LABELS.items():
        it = res["items"][key]
        soft = "（软判据）" if it["soft"] else ""
        L.append(f"{_MARK[it['status']]} {label}{soft}")
        L.append(f"        {it['detail']}")
        if it["status"] == "fail" and it.get("hint"):
            L.append(f"        → {it['hint']}")
    L.append("-" * 74)
    hard, soft, unk = res["hard_fail"], res["soft_fail"], res["unknown"]
    if not hard and not soft:
        L.append("结论：本波完成定义 **全勾**（unknown 项请人工确认）" if unk else "结论：本波完成定义 **全勾**")
    else:
        L.append(f"结论：**未完成** —— 硬失败 {len(hard)} 项 {hard or ''}；软失败 {len(soft)} 项 {soft or ''}")
    if unk:
        L.append(f"      无法核验 {len(unk)} 项（不等于失败）：{unk}")
    L.append(f"      enforce={enforce}（warn 只报告；strict 把软判据也算失败并退出码 1）")
    L.append("")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="步 9（S6）完成定义只读校验器")
    ap.add_argument("--region", required=True)
    ap.add_argument("--wave", default=None, help="指定波号（默认取该区最近一行）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--enforce", default="warn", choices=["warn", "strict"],
                    help="warn（默认，只报告）/ strict（软判据也算失败 → 退出码 1）")
    a = ap.parse_args()

    db = resolve_db_path()
    if not os.path.isfile(db):
        print(f"[step9-audit] 找不到 DB：{db}", file=sys.stderr)
        return 2
    from wqb.db_conn import connect as db_connect
    conn = db_connect(db, readonly=True)
    try:
        res = audit(conn, a.region, a.wave)
    finally:
        conn.close()

    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(render(res, a.enforce))
    if res["hard_fail"]:
        return 1
    if a.enforce == "strict" and res["soft_fail"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
