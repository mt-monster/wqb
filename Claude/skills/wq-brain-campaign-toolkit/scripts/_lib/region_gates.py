# -*- coding: utf-8 -*-
"""region_gates.py — 开波前的区域闸（2026-09-17 P0-1 下沉到 toolkit 入口；同日 +catalog 前置闸）。

问题（实测 2026-09-17）：`signal_floor` / `stop_rules` / `backlog` 三道闸由
`src/wqb/workflow/nodes/campaign.py` 在 S2/S3 阶段调用，**只有走 workflow 节点才生效**。
实际操作若直调 toolkit 脚本（`build_wave.py` / `wave_gate.py`），闸完全不触发 ——
实证：JPN 2026-09-16 首日 `_run_backlog_gate` 会拦截（conversion=0.0% < 10%），
却照跑完整波（gem 1,640 / 回测 0），说明该波未经过 campaign 节点。

本模块把这组闸下沉到 toolkit 的开波入口，使"绕过成本 > 遵守成本"。

2026-09-17 追加第 0 道 **catalog 前置闸**（S123 报告建议③）：为缺 typed catalog
的数据集开波/生成，必然在 gate.py 崩 FileNotFoundError、或积压成无门禁死库存
（实测全库 385 波 / 6,311 条从未过闸；JPN 白名单 12 集缺 10）。本闸把失败从
"gate 时崩"提前到"开波前拒"。判定单源 = `gate.load_whitelist`
（DB catalog → catalog 文件 → whitelist 文件），与门禁同源，零双真相源。

模式（`--gate-mode` / 环境变量 `WQB_GATE_MODE`）：
  off      不检查（等价旧行为）
  warn     **默认**：跑全部闸并打印，命中只警告不阻断（灰度阶段，避免全池停摆）
  enforce  任一闸命中即返回 ok=False，由调用方以非零退出码阻断开波

逃生口：环境变量 `WQB_DISABLE_REGION_GATES=1` 直接跳过（单测隔离用）。
"""
import json
import os
import sys

MODE_OFF = "off"
MODE_WARN = "warn"
MODE_ENFORCE = "enforce"
MODE_CHOICES = (MODE_OFF, MODE_WARN, MODE_ENFORCE)

#: 闸清单（顺序即执行顺序：catalog 前置 → 天花板 → 停止规则 → 积压）
GATE_NAMES = ("catalog", "signal_floor", "stop_rules", "backlog")


def resolve_workspace_root(campaign_dir):
    """从 campaign_dir 向上推导工作区根（与 build_wave._workspace_root_from_campaign 同源）。

    skill 安装位与工作区不同树，靠 __file__ 向上找不到；但 campaign_dir 总是形如
    <工作区根>/tracking/<REGION>，向上数层即命中。认据：存在 src/wqb 或 data/wqb.db。
    """
    if campaign_dir:
        p = os.path.abspath(campaign_dir)
        for _ in range(8):
            if os.path.isdir(os.path.join(p, "src", "wqb")) or \
                    os.path.isfile(os.path.join(p, "data", "wqb.db")):
                return p
            parent = os.path.dirname(p)
            if parent == p:
                break
            p = parent
    for env in ("WQB_WORKSPACE_ROOT", "WQB_ROOT", "WQ_PROJECT_ROOT"):
        root = os.environ.get(env)
        if root and os.path.isdir(os.path.join(root, "src", "wqb")):
            return root
    return None


def load_gates(campaign_dir):
    """导入 `wqb.workflow.nodes.campaign` 并返回该模块（内含三道闸）。"""
    root = resolve_workspace_root(campaign_dir)
    if not root:
        return None, "未能从 campaign_dir 推导工作区根（可设 WQB_WORKSPACE_ROOT）"
    src = os.path.join(root, "src")
    if not os.path.isdir(os.path.join(src, "wqb")):
        return None, f"{root} 下无 src/wqb"
    if src not in sys.path:
        sys.path.insert(0, src)
    try:
        from wqb.workflow.nodes import campaign as C
    except Exception as e:  # 导入失败不应阻断开波，交由调用方按 mode 处理
        return None, f"导入 wqb.workflow.nodes.campaign 失败: {type(e).__name__}: {e}"
    return C, None


def run_region_gates(campaign_dir, region, mode=MODE_WARN, dataset=None, out=None):
    """跑四道区域闸（catalog 前置 + signal_floor/stop_rules/backlog），打印结论。

    返回 dict：{"mode", "region", "ok", "skipped_reason", "results": {name: result}}
    `ok=False` 仅当 mode==enforce 且至少一道闸命中（success=False）。
    mode==off 或 WQB_DISABLE_REGION_GATES=1 时不做任何检查，ok=True。
    """
    stream = out if out is not None else sys.stdout
    report = {"mode": mode, "region": region, "ok": True,
              "skipped_reason": None, "results": {}}

    if mode not in MODE_CHOICES:
        report["mode"] = MODE_WARN
        mode = MODE_WARN
    if mode == MODE_OFF:
        report["skipped_reason"] = "gate-mode=off"
        return report
    if os.environ.get("WQB_DISABLE_REGION_GATES") == "1":
        report["skipped_reason"] = "WQB_DISABLE_REGION_GATES=1"
        return report
    if not campaign_dir or not region:
        report["skipped_reason"] = "缺少 campaign_dir / region"
        return report

    hits = []

    # —— 第 0 道：catalog 前置（不依赖 workflow 模块，toolkit 自足）——
    # 即使三道区域闸因 C 模块不可用而缺检，catalog 结果也要落进 report。
    try:
        r = _run_catalog_gate(region, dataset, str(campaign_dir))
    except Exception as e:
        r = {"step": "catalog_gate", "success": True,
             "warning": f"catalog gate raised {type(e).__name__}: {e}"}
        print(f"[region-gates] catalog     ★异常降级（未拦截）：{type(e).__name__}: {e}",
              file=stream)
    report["results"]["catalog"] = r
    _print_one("catalog", r, stream)
    if not r.get("success", True):
        hits.append("catalog")

    C, err = load_gates(campaign_dir)
    if C is None:
        # 闸不可用：enforce 下也不能拦（不能因环境问题阻断业务），但必须显式告警
        print(f"[region-gates] ★区域闸不可用：{err}（signal_floor/stop_rules/backlog 本次未拦截）",
              file=stream)
        report["skipped_reason"] = err
    else:
        runners = (
            ("signal_floor", C._run_signal_floor_gate),
            ("stop_rules", C._run_stop_rules_gate),
            ("backlog", C._run_backlog_gate),
        )
        for name, fn in runners:
            try:
                r = fn(region, dataset, str(campaign_dir))
            except Exception as e:
                r = {"step": name, "success": True,
                     "warning": f"{name} gate raised {type(e).__name__}: {e}"}
                report["results"][name] = r
                print(f"[region-gates] {name:12s} ★异常降级（未拦截）：{type(e).__name__}: {e}",
                      file=stream)
                continue
            report["results"][name] = r
            _print_one(name, r, stream)
            if not r.get("success", True):
                hits.append(name)

    report["hits"] = hits
    if hits:
        if mode == MODE_ENFORCE:
            report["ok"] = False
            print(f"[region-gates] ★★ 开波被阻断（enforce）：{'、'.join(hits)} 命中。"
                  f"按闸提示消化积压/补 catalog/换区，或用 ledger override 显式放行留痕。", file=stream)
        else:
            print(f"[region-gates] ★ 命中 {'、'.join(hits)}，但 gate-mode=warn（灰度）→ 仅告警不阻断。"
                  f"确认无误后改 --gate-mode enforce 或设 WQB_GATE_MODE=enforce。", file=stream)
    else:
        print("[region-gates] 四道闸全部放行。", file=stream)
    return report


def _run_catalog_gate(region, dataset, campaign_dir):
    """catalog 前置闸（第 0 道）：缺 typed catalog 的数据集不开波/不生成。

    依据（S123 报告建议③，2026-09-17 实测）：全库 25% 白名单数据集（23/93）无
    catalog——这些集的波在 gate.py 必崩 FileNotFoundError（fail 于异常而非干净
    拒绝），或根本没人敢闸、积压成死库存（385 波 / 6,311 条从未过闸）。
    判定单源 = `gate.load_whitelist`（DB catalog → catalog 文件 → whitelist 文件），
    与真正门禁走同一条解析路径，零双真相源。

    dataset 给定 → 只查该数据集（开波单集语义）；
    dataset=None → 查该区白名单全覆盖（开区语义，JPN 实测 12 缺 10）。
    白名单/DB 读不到 → 显式告警放行（环境问题不阻断，与其余闸同纪律）。
    """
    result = {"step": "catalog_gate", "success": True}
    scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # _lib → scripts
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    try:
        import gate as gate_mod
        from _lib.common import CampaignContext
    except Exception as e:
        result["warning"] = f"catalog gate unavailable: {type(e).__name__}: {e}"
        return result

    if dataset:
        targets, scope = [dataset], f"{region}/{dataset}"
    else:
        targets, err = _region_whitelist_datasets(campaign_dir, region)
        if err:
            result["warning"] = err
            return result
        if not targets:
            result["warning"] = f"{region} 的 s0_whitelist 无数据集（S0 未选集？）→ 跳过 catalog 检查"
            return result
        scope = f"{region}（白名单 {len(targets)} 集）"

    ctx = CampaignContext(campaign_dir)
    missing = []
    for ds in targets:
        try:
            gate_mod.load_whitelist(ctx, ds)
        except Exception:
            missing.append(ds)

    result["scope"] = scope
    result["evidence"] = {
        "datasets": len(targets),
        "have_catalog": len(targets) - len(missing),
        "missing": missing,
    }
    if missing:
        show = ", ".join(missing[:8]) + (f" …(+{len(missing) - 8})" if len(missing) > 8 else "")
        result["success"] = False
        result["error"] = (
            f"catalog 前置闸命中（{scope}）：{len(missing)}/{len(targets)} 个数据集无 typed catalog"
            f" → 这些集的波在门禁必崩或积压成无门禁死库存。先跑 "
            f"scan_fields.py --campaign-dir {campaign_dir} --dataset <缺集> 补 catalog，"
            f"或把缺集移出 s0_whitelist。缺: {show}"
        )
    return result


def _region_whitelist_datasets(campaign_dir, region):
    """读该区 s0_whitelist 的数据集清单。

    归一单源 = `wqb.ledger_whitelist`（P0-4，覆盖 datasets/whitelist/candidates/
    推断/损坏抢救 5 种历史 schema）；wqb 不可用时降级为最小兜底解析（仅顶层三键）。
    返回 (datasets, err)；err 非 None 表示读不到/解析不了（调用方告警放行）。
    """
    root = resolve_workspace_root(campaign_dir)
    db_path = os.path.join(root, "data", "wqb.db") if root else None
    raw = None
    if db_path and os.path.isfile(db_path):
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            try:
                row = conn.execute(
                    "SELECT value FROM ledger_kv WHERE region=? AND key='s0_whitelist'",
                    (region,)).fetchone()
            finally:
                conn.close()
            raw = row[0] if row else None
        except Exception:
            raw = None
    if raw is None:
        return [], f"{region} 读不到 s0_whitelist（DB={'缺' if not db_path or not os.path.isfile(db_path or '') else '无该键'}）"

    payload = raw if isinstance(raw, (dict, list)) else None
    if payload is None:
        try:
            payload = json.loads(raw)
        except Exception:
            return [], f"{region} s0_whitelist 不是合法 JSON"

    # 主路径：P0-4 归一（需要仓库 src 可导入）
    try:
        wroot = resolve_workspace_root(campaign_dir)
        src = os.path.join(wroot, "src") if wroot else None
        if src and os.path.isdir(src) and src not in sys.path:
            sys.path.insert(0, src)
        from wqb.ledger_whitelist import normalize as _norm
        rec = _norm(payload)
        datasets = [d for d in (rec.get("datasets") or []) if d]
        if datasets:
            return [str(d) for d in datasets], None
        if rec.get("ok") is False:
            return [], f"{region} s0_whitelist 归一失败（schema={rec.get('schema')}）：{rec.get('reason')}"
    except Exception:
        pass

    # 兜底：顶层三键直取（仅当 wqb 不可用/归一未产出）
    try:
        for k in ("datasets", "whitelist", "candidates"):
            v = payload.get(k) if isinstance(payload, dict) else None
            if isinstance(v, list) and v:
                out = [x if isinstance(x, str) else (x.get("id") or x.get("dataset") or "")
                       for x in v]
                out = [x for x in out if x]
                if out:
                    return out, None
    except Exception:
        pass
    return [], f"{region} s0_whitelist 无法解析出数据集清单"


def _print_one(name, r, stream):
    status = "放行" if r.get("success", True) else "命中"
    detail = r.get("skipped") or r.get("error") or r.get("warning") or ""
    line = f"[region-gates] {name:12s} {status}"
    if detail:
        line += f" — {str(detail)[:220]}"
    print(line, file=stream)
    if r.get("evidence"):
        keys = ("total", "backtested", "pending_gated", "gem", "selected",
                "unconsumed", "conversion", "pending_gated_ratio", "unconsumed_ratio")
        ev = r["evidence"]
        picked = ", ".join(f"{k}={ev[k]}" for k in keys if k in ev)
        if picked:
            print(f"[region-gates] {'':12s}   evidence: {picked}", file=stream)
    for w in (r.get("warnings") or []):
        print(f"[region-gates] {'':12s}   WARN: {str(w)[:220]}", file=stream)
