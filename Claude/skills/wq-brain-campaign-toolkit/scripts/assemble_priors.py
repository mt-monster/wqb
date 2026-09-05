# -*- coding: utf-8 -*-
"""assemble_priors.py - 从 DB 结构化 KB 确定性组装 GEM 消费用的 priors 文件。

把"知识库走不走"从"自觉"变成"结构"：

  病根：之前 tracking/USA/priors/usa_priors.json 的 wins:[] 永远为空，因为没人把
  region_kb.win_recipes 与 registry win 层组装进文件 → GEM 永远收不到胜方配方；
  且 ad-hoc 手写 json 不会被批量驱动默认传入（dry-run 也不跑）。

  本脚本是 priors 文件的唯一权威来源：DB -> 文件，确定性、可重跑、可审计。
   gate.py 复用 assemble_priors_dict() 做文件缺失兜底（保证闸永远 KB-aware）；
   build_wave.py 复用 priors_sha() 把波指纹写进 meta（波 <-> KB 状态可回溯）。

产物：<campaign>/priors/<region>_priors.json
schema: {"wins":[{id,what,key,...}], "dead_ends":[{family,reason,...}],
         "_meta":{region,generated_at,sources}}
注意：sha256 不写入文件本体（自引用会错位），由 CLI 打印 + 从磁盘重算保持一致。
GEM 的 compact_priors_text() 只读 wins/dead_ends，忽略 _meta，故附加 _meta 安全。
"""
import argparse
import datetime
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import CampaignContext, add_campaign_arg, atomic_write
from _lib.wqb_store import get_store
from _lib.registry import RegistryStore

MAX_WINS = 6
MAX_DEADENDS = 12

# profile 探测路径（与 skeletons.load_region_priors 同序：env → .trae-cn → .qoder-cn）
def _profile_path(region):
    candidates = []
    env_dir = os.environ.get("WQ_RA_PIPELINE_DIR")
    if env_dir:
        candidates.append(os.path.join(env_dir, "references", "regions", f"{region.upper()}.md"))
    for home in (os.path.expanduser("~"),):
        for d in (os.path.join(home, ".trae-cn", "skills", "wq-brain-ra-pipeline"),
                  os.path.join(home, ".qoder-cn", "skills", "wq-brain-ra-pipeline")):
            candidates.append(os.path.join(d, "references", "regions", f"{region.upper()}.md"))
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def _profile_fallback(region):
    """region_kb 为空时，从区域 profile front-matter 的 priors 段兜底（静态种子）。

    简易 YAML 文本解析（不引第三方依赖）：win_recipes 列表行 + signal_families_exclude
    列表行；解析失败静默降级返回空。
    """
    path = _profile_path(region)
    if not path:
        return {"wins": [], "dead_ends": []}
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return {"wins": [], "dead_ends": []}
    fm = text.split("---", 2)
    if len(fm) < 3:
        return {"wins": [], "dead_ends": []}
    front = fm[1]
    wins = []
    for line in front.splitlines():
        line = line.strip()
        if line.startswith("- \"") or line.startswith("- '"):
            # 仅收集 win_recipes 块内的条目（列表项行）
            wins.append(line[2:].strip().strip('"').strip("'"))
    if not wins:
        return {"wins": [], "dead_ends": []}
    de = []
    for ln in front.splitlines():
        ln = ln.strip()
        if ln.startswith("signal_families_exclude:") or ln.startswith("- "):
            continue
    # exclude 列表解析：signal_families_exclude: [a, b] 单行或后续列表行
    import re as _re
    excl = []
    m = _re.search(r"signal_families_exclude:\s*\[([^\]]*)\]", front)
    if m:
        excl = [x.strip().strip('"').strip("'") for x in m.group(1).split(",") if x.strip()]
    for fam in excl:
        de.append({"family": fam, "reason": "profile 静态 exclude（DB KB 空时兜底）",
                   "source": "profile_fallback"})
    return {"wins": wins, "dead_ends": de}


# ---------------------------------------------------------------------------
# 数据源读取
# ---------------------------------------------------------------------------

def _region_kb(ctx):
    st = get_store(ctx)
    try:
        kb = st.get_ledger(ctx.region, "region_kb")
    finally:
        st.close()
    return kb if isinstance(kb, dict) else {}


def _template_kb(ctx):
    st = get_store(ctx)
    try:
        kb = st.get_ledger("KB", "template_kb")
    finally:
        st.close()
    return kb if isinstance(kb, dict) else {}


def _registry_layer(ctx, layer):
    rs = RegistryStore(ctx.region)
    out = []
    for r in rs.list(layer=layer):
        p = r["payload"] if isinstance(r["payload"], dict) else json.loads(r["payload"])
        out.append((r, p))
    return out


# ---------------------------------------------------------------------------
# 组装核心（无副作用，供 gate 兜底复用）
# ---------------------------------------------------------------------------

def assemble_priors_dict(ctx):
    """从 DB 结构化 KB 组装 GEM priors dict。

    wins 来源（去重，≤MAX_WINS；banned=true 条目不注入）：
      1) region_kb.forum_templates  （论坛验证模板，含完整表达式+实测指标，最高优先级）
      2) region_kb.win_recipes      （如 SuperAlpha selection+combo 胜方配方）
      3) registry_empirical win 层（如 USA-MFP-4LEG-WIN / USA-SA-KPGvRMg1）
      4) template_kb validated 含本区的跨区模板（SOP 协议第 2 源）
      5) region_kb.active_alphas    （活跃 ACTIVE alpha 作为补充胜绩）
    dead_ends 来源（去重，≤MAX_DEADENDS）：
      1) region_kb.dead_patterns    （机制级死路：starmine 全家 16 死/双子星互挤等）
      2) registry_empirical dead_end 层（含 family+reason，数据集级）
      3) template_kb failed 含本区的模板
    region_context 来源：
      region_kb.notes / settings_proven / tier （区域特性，供 GEM 理解区域约束）
    """
    kb = _region_kb(ctx)

    # ---- wins ----
    wins, seen = [], set()
    # 论坛验证模板（最高优先级：含完整表达式+实测指标，可直接复用机制）
    for ft in (kb.get("forum_templates") or []):
        wid = ft.get("name") or ft.get("id") or "forum_template"
        if wid in seen:
            continue
        seen.add(wid)
        # 构建模板描述：表达式 + 关键指标 + 变体提示
        expr = ft.get("expression", "")
        metrics = ft.get("metrics", {})
        metric_str = " / ".join(f"{k}={v}" for k, v in list(metrics.items())[:4])
        variants = ft.get("variants", [])
        variant_hint = f" | 变体: {'; '.join(variants[:2])}" if variants else ""
        wins.append({
            "id": wid,
            "what": f"[论坛模板] {wid}",
            "key": f"expr={expr} | metrics={metric_str}{variant_hint}",
            "evidence": ft.get("evidence", ""),
            "source": "forum_template",
        })
    for wr in (kb.get("win_recipes") or []):
        if wr.get("banned"):
            continue  # 2026-09-03 修复：banned 配方（如 MODEL×PV 禁令）不入 priors
        wid = wr.get("name") or wr.get("id") or "win_recipe"
        if wid in seen:
            continue
        seen.add(wid)
        wins.append({
            "id": wid, "what": wid,
            "key": wr.get("skeleton") or wr.get("key") or "",
            "evidence": wr.get("evidence", ""),
            "source": "region_kb",
        })
    for _r, p in _registry_layer(ctx, "win"):
        if p.get("banned"):
            continue  # 2026-09-03 修复：registry win 层 banned 证据条目同样跳过
        # 双 schema 兼容（2026-09-03 修复）：toolkit upsert 行 payload 用 id/what/key；
        # MCP(wqb-db) 写入行用 example_id/mechanism/evidence——原实现 p.get("entry_id")
        # 永远取不到（entry_id 在 _r 行而非 payload），3 条 MCP win 全兜底成同一 'win' 空壳
        wid = (p.get("id") or p.get("what") or p.get("example_id")
               or _r.get("entry_id") or "win")
        if wid in seen:
            continue
        seen.add(wid)
        key = (p.get("key") or p.get("evidence") or p.get("mechanism") or "")
        wins.append({
            "id": wid,
            "what": p.get("what") or p.get("mechanism") or wid,
            "key": key, "evidence": p.get("evidence", ""),
            "source": "registry_win",
        })
    # template_kb validated 含本区的跨区模板（SOP 协议第 2 源，先于 active_alphas）
    tkb = _template_kb(ctx)
    for t in (tkb.get("templates") or []):
        v = (t.get("validated") or {}).get(ctx.region)
        if not v:
            continue
        wid = f"{t.get('id', 'T')} {t.get('name', '')}".strip()
        if wid in seen:
            continue
        seen.add(wid)
        wins.append({
            "id": wid, "what": wid,
            "key": f"skeleton={t.get('skeleton', '')}; iron_law={t.get('iron_law', '')}",
            "evidence": v,
            "source": "template_kb_validated",
        })
    for a in (kb.get("active_alphas") or []):
        if a in seen:
            continue
        seen.add(a)
        wins.append({
            "id": a, "what": a, "key": "ACTIVE alpha (详见 region_kb)",
            "source": "region_kb_active",
        })
    wins = wins[:MAX_WINS]
    if not wins:
        fb = _profile_fallback(ctx.region)
        wins = [{"id": w, "what": w, "key": "profile 静态 win recipe（DB KB 空时兜底）",
                 "source": "profile_fallback"} for w in fb["wins"]][:MAX_WINS]

    # ---- dead_ends ----
    # 2026-09-03 修复：region_kb.dead_patterns 优先级前移——它们是"机制级死路"
    # （starmine 全家 16 死/双子星互挤等），跨数据集任务直接适用；registry dead_end
    # 是"数据集级"记录，名额有限时应先保机制级死路（与 SOP 协议 ①dead_patterns 对齐）。
    de, dseen = [], set()
    for dp in (kb.get("dead_patterns") or []):
        if dp in dseen:
            continue
        dseen.add(dp)
        de.append({
            "family": "region_kb",
            "reason": dp,
            "source": "region_kb_dead_pattern",
        })
    for _r, p in _registry_layer(ctx, "dead_end"):
        fam = p.get("family") or _r.get("family") or _r.get("entry_id")
        if fam in dseen:
            continue
        dseen.add(fam)
        de.append({
            "family": fam,
            "reason": p.get("reason") or p.get("rule") or "",
            "salvage": p.get("salvage"),
            "source": "registry_dead_end",
            "_entry_id": _r.get("entry_id"),
        })
    # template_kb failed 含本区的模板（SOP 协议第 3 源）
    for t in (tkb.get("templates") or []):
        f = (t.get("failed") or {}).get(ctx.region)
        if not f:
            continue
        fam = f"{t.get('id', 'T')} {t.get('name', '')}".strip()
        if fam in dseen:
            continue
        dseen.add(fam)
        de.append({"family": fam, "reason": f, "source": "template_kb_failed"})
    de = de[:MAX_DEADENDS]
    if not de:
        fb = _profile_fallback(ctx.region)
        for d in fb["dead_ends"]:
            if d["family"] in dseen:
                continue
            dseen.add(d["family"])
            de.append(d)
        de = de[:MAX_DEADENDS]

    return {
        "wins": wins,
        "dead_ends": de,
        "region_context": _build_region_context(kb),
        "_meta": {
            "region": ctx.region,
            # 注意：不写入生成时间戳——时间戳会让文件内容每次变化导致 sha 漂移，
            # 破坏"同一 KB 状态 => 同一 sha"的可追溯性。时间戳仅由 CLI 打印，不落盘。
            "sources": ["ledger_kv:region_kb (forum_templates/win_recipes/dead_patterns/notes)",
                        "registry_empirical:win",
                        "registry_empirical:dead_end",
                        "ledger_kv:KB/template_kb",
                        "profile_fallback (仅 DB KB 空时)"],
        },
    }


def _build_region_context(kb: dict) -> dict:
    """从 region_kb 提取区域特性上下文，供 GEM 理解区域约束与机会。"""
    ctx = {}
    # 区域层级（如收官区/新区）
    if tier := kb.get("tier"):
        ctx["tier"] = tier
    # 已验证设置
    if settings := kb.get("settings_proven"):
        ctx["settings_proven"] = settings
    # 区域特性笔记（取前 6 条核心经验）
    if notes := kb.get("notes"):
        ctx["key_notes"] = notes[:6]
    # 2026-09-04 新增：算子使用频率反馈（从 backtest_results 统计）
    if op_stats := kb.get("operator_usage_stats"):
        ctx["operator_usage_stats"] = op_stats
    return ctx


# ---------------------------------------------------------------------------
# 文件 I/O + sha
# ---------------------------------------------------------------------------

def priors_path(ctx):
    # 用 ctx.prefix（小写 region）保证与 GEM 批量驱动硬编码的
    # tracking/<REGION>/priors/<region>_priors.json（如 usa_priors.json）一致。
    return ctx.path("priors", f"{ctx.prefix}_priors.json")


def _sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def write_priors(ctx, payload=None):
    """组装并原子写文件，返回 (path, sha256, payload)。

    关键：sha256 不写入文件本体（避免"文件含自身 sha"导致内容自引用错位）。
    文件即最终稳定产物，sha 对其内容直接计算，故 CLI 打印值 == priors_sha()
    从磁盘重算值 == build_wave 写入 wave meta 的 priors_sha，三者恒等。
    """
    if payload is None:
        payload = assemble_priors_dict(ctx)
    path = priors_path(ctx)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    atomic_write(path, payload, encoding="utf-8", indent=1)
    sha = _sha256_file(path)
    return path, sha, payload


def priors_sha(ctx):
    """返回当前 priors 文件 sha256；文件不存在返回 None。供 build_wave 写波指纹。"""
    path = priors_path(ctx)
    return _sha256_file(path) if os.path.exists(path) else None


def load_priors_file(ctx):
    """读取已落盘的 priors 文件；不存在返回 None。"""
    path = priors_path(ctx)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def restore_from_db(ctx):
    """从 DB 全量快照（priors_snapshot_<prefix>）恢复 priors 文件。

    重建内容与 assemble 落盘文件结构完全一致（wins/dead_ends 原样 + _meta 无时间戳、
    无 sha256 字段——与 write_priors 契约一致，否则文件哈希会漂移）。
    DB 快照的 sha256 仅用于校验重建内容一致性，不写入文件。文件丢失/损坏时用。
    """
    st = get_store(ctx)
    try:
        snap = st.get_ledger(ctx.region, f"priors_snapshot_{ctx.prefix}")
    finally:
        st.close()
    if not isinstance(snap, dict) or "wins" not in snap or "sha256" not in snap:
        raise SystemExit(
            f"DB 无 priors 全量快照（{ctx.region}/priors_snapshot_{ctx.prefix}）；"
            "先跑 assemble-priors --snapshot-ledger")
    payload = {
        "wins": snap.get("wins", []),
        "dead_ends": snap.get("dead_ends", []),
        "_meta": {"region": ctx.region, "sources": snap.get("sources", [])},
    }
    path = priors_path(ctx)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    atomic_write(path, payload, encoding="utf-8", indent=1)
    sha = _sha256_file(path)
    db_sha = snap.get("sha256")
    if db_sha and sha != db_sha:
        raise SystemExit(f"[restore] sha 不一致 DB={db_sha} file={sha}——DB 快照被篡改或字段结构漂移")
    print(f"restored {path}")
    print(f"wins={len(payload['wins'])} dead_ends={len(payload['dead_ends'])} "
          f"sha256={sha} (matches DB, sha 不入文件保持确定性)")
    return path, sha, payload


def main():
    ap = argparse.ArgumentParser(
        prog="campaign.py assemble-priors",
        description="从 DB 结构化 KB 确定性组装 GEM priors 文件（取代手写 usa_priors.json）")
    add_campaign_arg(ap)
    ap.add_argument("--print", action="store_true", help="只打印组装结果，不写文件")
    ap.add_argument("--sha-only", action="store_true", help="只输出当前文件 sha256（无文件则空行）")
    ap.add_argument("--snapshot-ledger", action="store_true",
                    help="写 DB 全量快照（wins/dead_ends 全字段 + sha + 源）到 ledger key priors_snapshot_<region>")
    ap.add_argument("--restore", action="store_true",
                    help="从 DB 全量快照恢复 priors 文件（文件丢失/损坏时用，sha 校验）")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)

    if a.sha_only:
        print(priors_sha(ctx) or "")
        return

    if a.restore:
        restore_from_db(ctx)
        return

    payload = assemble_priors_dict(ctx)
    if a.print:
        print(json.dumps(payload, ensure_ascii=False, indent=1))
        return

    path, sha, payload = write_priors(ctx, payload)
    print(f"wrote {path}")
    print(f"wins={len(payload['wins'])} dead_ends={len(payload['dead_ends'])} "
          f"sha256={sha}")
    if a.snapshot_ledger:
        st = get_store(ctx)
        try:
            st.upsert_ledger(ctx.region, f"priors_snapshot_{ctx.prefix}", {
                "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
                "sha256": sha,
                "wins": payload["wins"],
                "dead_ends": payload["dead_ends"],
                "sources": payload.get("_meta", {}).get("sources", []),
            })
            print(f"snapshot(full) -> ledger key priors_snapshot_{ctx.prefix} "
                  f"(wins={len(payload['wins'])} dead_ends={len(payload['dead_ends'])})")
        finally:
            st.close()
    print(f"generated_at={datetime.datetime.now().isoformat(timespec='seconds')} "
          f"(timestamp 仅显示，不写入文件以保证 sha 确定性)")


if __name__ == "__main__":
    main()
