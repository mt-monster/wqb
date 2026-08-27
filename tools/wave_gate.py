# -*- coding: utf-8 -*-
"""wave_gate.py - 每波门禁编排器（替代 tracking/<REGION>/scripts/_gate_waveNN.py 族）。

在单次调用内完成：
  1) 候选解析：--candidates JSON（{expressions:[{id,expr}]} / [str] / {exprs:[...]}）
     或 --exprs-file（每行一条）或 --expr（单条）
  2) 语法校验：alpha-expression-verifier（与 gate 闸1 同源，先于 5 闸执行，
     失败即整波拦截——语法错误是整批 CANCELLED 连坐的头号元凶）
  3) 5 闸预检 + 批级多样性：复用 wq-brain-campaign-toolkit 的权威 gate.py
     （路径自动解析 WQ_TOOLKIT_DIR → ~/.qoder-cn/skills → ~/.workbuddy/skills，勿硬编码）
  4) 六维结构多样性 + 质量预估（建议2/3 落地，2026-08-27）：
     pool_diversity.assess 六维报告；quality_predict.predict_all 回测前预估，
     EXPECTED_BLOCK 候选默认仅标注，--quality-block 开启硬拦截（回测配额闸门）
  5) 结果落盘：<campaign-dir>/cache/gate_wave<wave>_<dataset>.json（完整）
     + <campaign-dir>/cache/gate_wave<wave>_<dataset>.out.txt（人类摘要）

用法:
  python tools/wave_gate.py --campaign-dir tracking/KOR --dataset model219 --wave 97 \
      --candidates candidates/wave97_exprs.json
  python tools/wave_gate.py --campaign-dir tracking/USA --dataset fund28 --wave 31 \
      --exprs-file candidates/w31.txt --skip-diversity-gate
  python tools/wave_gate.py --campaign-dir tracking/KOR --dataset model219 \
      --expr "rank(close)" --wave 98

退出码: 0=语法+5 闸全 PASS, 1=存在 FAIL
运行环境: 与 gate.py 一致，纯标准库，任意 Python 3.10+ 均可。
"""
import argparse
import importlib
import json
import os
import subprocess
import sys

# ---- skill 目录自动解析（与 gate.py 的 WQ_VALIDATOR_DIR 模式对齐）----
# 权威套为 ~/.qoder-cn/skills（2026-08-23 单源化），~/.cursor/skills 为 Cursor 联接安装位，
# ~/.workbuddy/skills 仅作跨 Agent 回退。
_TOOLKIT_CANDIDATES = [
    os.environ.get("WQ_TOOLKIT_DIR"),
    os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts"),
    os.path.join(os.path.expanduser("~"), ".cursor", "skills", "wq-brain-campaign-toolkit", "scripts"),
    os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "wq-brain-campaign-toolkit", "scripts"),
]
_VALIDATOR_CANDIDATES = [
    os.environ.get("WQ_VALIDATOR_DIR"),
    os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills", "alpha-expression-verifier", "scripts"),
    os.path.join(os.path.expanduser("~"), ".cursor", "skills", "alpha-expression-verifier", "scripts"),
    os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "alpha-expression-verifier", "scripts"),
]


def find_script(candidates, name):
    for d in candidates:
        if d and os.path.isfile(os.path.join(d, name)):
            return os.path.join(d, name)
    raise FileNotFoundError(
        f"未找到 {name}：设 WQ_TOOLKIT_DIR/WQ_VALIDATOR_DIR 指定（已搜 "
        f"{', '.join(c for c in candidates if c)}）")


def load_validator():
    """动态加载 alpha-expression-verifier 的 ExpressionValidator（直调，免子进程）。"""
    dir_ = os.path.dirname(find_script(_VALIDATOR_CANDIDATES, "validator.py"))
    sys.path.insert(0, dir_)
    mod = importlib.import_module("validator")
    return mod.ExpressionValidator()


def parse_candidates(a):
    """候选解析 → [(id_or_index, expr)]；兼容 DB / JSON / txt / 单条。"""
    if getattr(a, "from_db", False):
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        # tools/wave_gate.py 不在 toolkit scripts 下，直接 import wqb.store
        wqb_root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or r"D:\coding\traeCN_project\wqb"
        src = os.path.join(wqb_root, "src")
        if src not in sys.path:
            sys.path.insert(0, src)
        from wqb.store import CampaignStore
        st = CampaignStore(os.path.join(wqb_root, "data", "wqb.db"))
        try:
            region = a.region
            if not region:
                settings = json.load(open(os.path.join(a.campaign_dir, "config", "settings.json"), encoding="utf-8"))
                region = settings.get("region")
            rows = st.list_expressions(region, str(a.wave), dataset=a.dataset)
            if not rows:
                rows = st.list_expressions(region, str(a.wave))
            items = [r.get("expression") for r in rows if r.get("expression")]
        finally:
            st.close()
        if not items:
            raise SystemExit(f"db 无候选: wave={a.wave} dataset={a.dataset}")
    elif a.candidates:
        d = json.load(open(a.candidates, encoding="utf-8"))
        items = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
    elif a.exprs_file:
        items = [ln.strip() for ln in open(a.exprs_file, encoding="utf-8") if ln.strip()]
    elif a.expr:
        items = [a.expr]
    else:
        raise SystemExit("need --from-db / --candidates / --exprs-file / --expr 之一")
    out = []
    for i, it in enumerate(items, 1):
        if isinstance(it, dict):
            e = it.get("expr") or it.get("code") or it.get("expression")
            cid = it.get("id") or it.get("name") or i
        elif isinstance(it, str):
            e, cid = it, i
        else:
            continue
        if e:
            out.append((cid, e))
    if not out:
        raise SystemExit("候选解析为空")
    return out


def main():
    ap = argparse.ArgumentParser(description="每波门禁编排器：语法 + 5 闸 + 多样性")
    ap.add_argument("--campaign-dir", required=True, help="战役根目录 (如 tracking/KOR)")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--datasets", default="",
                    help="逗号分隔额外数据集，与 --dataset 合并白名单（跨金字塔 mix）")
    ap.add_argument("--wave", type=int, default=0, help="波号")
    ap.add_argument("--from-db", action="store_true", help="从 expressions 表读候选（推荐）")
    ap.add_argument("--region", default=None, help="区域（缺省读 settings.json）")
    ap.add_argument("--candidates", help="兼容：候选 JSON")
    ap.add_argument("--exprs-file", help="每行一条表达式的 txt")
    ap.add_argument("--expr", help="单条表达式")
    ap.add_argument("--skip-diversity-gate", action="store_true", help="透传 toolkit gate.py（repair 批等）")
    ap.add_argument("--batch-type", default="explore", help="透传 toolkit gate.py（explore/repair...）")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--fix", action="store_true", help="透传：VECTOR 数据集自动裹 vec_* 后检测")
    ap.add_argument("--skip-quality", action="store_true", help="跳过质量预估+六维多样性阶段")
    ap.add_argument("--quality-block", action="store_true",
                    help="EXPECTED_BLOCK 候选计入 FAIL（默认仅标注；回测配额闸门建议开启）")
    a = ap.parse_args()

    items = parse_candidates(a)
    campaign = a.campaign_dir.rstrip("/\\")
    tag = a.wave or int(__import__("time").time())

    # ---- 1) 语法校验 ----
    validator = load_validator()
    syntax = []
    for cid, e in items:
        r = validator.check_expression(e)
        ok = bool(r.get("valid"))
        syntax.append({"id": cid, "valid": ok,
                       "errors": r.get("errors") if not ok else []})
        print(f"[syntax] {cid}: {'PASS' if ok else 'FAIL ' + str(r.get('errors'))[:160]}")

    # ---- 2) 5 闸 + 多样性（权威实现：toolkit gate.py，从 DB 或 stdin 表达式）----
    gate_py = find_script(_TOOLKIT_CANDIDATES, "gate.py")
    cmd = [sys.executable, gate_py, "--campaign-dir", campaign, "--dataset", a.dataset,
           "--wave", str(tag), "--batch-type", a.batch_type]
    if a.datasets:
        cmd.extend(["--datasets", a.datasets])
    if a.from_db or (not a.candidates and not a.exprs_file and not a.expr):
        cmd.append("--from-db")
    else:
        # 兼容旧入口：把解析后的表达式 upsert 再 --from-db，避免写 cache json
        wqb_root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or r"D:\coding\traeCN_project\wqb"
        src = os.path.join(wqb_root, "src")
        if src not in sys.path:
            sys.path.insert(0, src)
        from wqb.store import CampaignStore
        settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
        region = a.region or settings.get("region")
        st = CampaignStore(os.path.join(wqb_root, "data", "wqb.db"))
        try:
            st.upsert_expressions(region, str(tag), [e for _, e in items], dataset=a.dataset, status="gated")
        finally:
            st.close()
        cmd.append("--from-db")
    if a.skip_diversity_gate:
        cmd.append("--skip-diversity-gate")
    if a.no_cache:
        cmd.append("--no-cache")
    if a.fix:
        cmd.append("--fix")
    print(f"\n[gate ] {os.path.basename(gate_py)} --from-db --wave {tag}")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    gate_json = None
    try:
        start, end = r.stdout.find("{"), r.stdout.rfind("}")
        if start >= 0 and end > start:
            gate_json = json.loads(r.stdout[start:end + 1])
    except Exception:
        gate_json = None

    report = {
        "wave": a.wave, "dataset": a.dataset, "campaign_dir": campaign,
        "gate_exit": r.returncode,
        "syntax": {"total": len(syntax), "passed": sum(1 for s in syntax if s["valid"]),
                   "items": syntax},
        "gate": gate_json or {"all_pass": False, "raw_tail": (r.stdout or "")[-2000:]},
    }

    # ---- 3) 六维多样性 + 质量预估（建议2/3 落地；仅对语法通过候选，避免噪声）----
    quality_block_ids = []
    if not a.skip_quality:
        try:
            tools_dir = os.path.dirname(os.path.abspath(__file__))
            if tools_dir not in sys.path:
                sys.path.insert(0, tools_dir)
            import pool_diversity as pd_mod
            import quality_predict as qp_mod
            import sqlite3 as _sq
            passed_exprs = [e for (cid, e), s in zip(items, syntax) if s["valid"]]
            div_report = pd_mod.assess(passed_exprs, region=a.region)
            report["diversity"] = div_report
            if div_report["issues"]:
                print("\n[div  ] 六维多样性风险:")
                for it in div_report["issues"]:
                    print(f"        - {it}")
            else:
                print(f"\n[div  ] 六维多样性 PASS（算子熵={div_report['operator_stats']['entropy']}, "
                      f"同质占比={div_report['structural_similarity']['homog_ratio']:.0%}）")
            wqb_root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or r"D:\coding\traeCN_project\wqb"
            settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
            qregion = a.region or settings.get("region")
            qconn = _sq.connect(os.path.join(wqb_root, "data", "wqb.db"))
            try:
                q_results, _ = qp_mod.predict_all([(e, a.dataset) for e in passed_exprs], qregion, qconn)
            finally:
                qconn.close()
            by_expr = {qr["expr"]: qr for qr in q_results}  # expr 被截断 120 字符，全量表达式前缀匹配
            qp_summary = {"pass": 0, "review": 0, "block": 0, "blocked": []}
            for (cid, e), s in zip(items, syntax):
                if not s["valid"]:
                    continue
                qr = by_expr.get(e[:120])
                if not qr:
                    continue
                v = qr["verdict"]
                if v == "EXPECTED_PASS":
                    qp_summary["pass"] += 1
                elif v == "REVIEW":
                    qp_summary["review"] += 1
                else:
                    qp_summary["block"] += 1
                    quality_block_ids.append(cid)
                    qp_summary["blocked"].append({"id": cid, "reasons": qr["reasons"]})
                    print(f"[qp   ] BLOCK {cid}: {'; '.join(qr['reasons'])}")
            report["quality_predict"] = qp_summary
            print(f"[qp   ] 质量预估: PASS={qp_summary['pass']} REVIEW={qp_summary['review']} "
                  f"BLOCK={qp_summary['block']}" + ("（计入 FAIL）" if a.quality_block else "（仅标注）"))
        except Exception as e:
            report["quality_predict"] = {"error": str(e)}
            print(f"[qp   ] 质量预估阶段失败（不阻断门禁）: {e}")

    try:
        wqb_root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or r"D:\coding\traeCN_project\wqb"
        src = os.path.join(wqb_root, "src")
        if src not in sys.path:
            sys.path.insert(0, src)
        from wqb.store import CampaignStore
        settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
        region = a.region or settings.get("region")
        st = CampaignStore(os.path.join(wqb_root, "data", "wqb.db"))
        try:
            st.upsert_gate_result(region, str(tag), a.dataset, report)
        finally:
            st.close()
        print(f"\n[out  ] db gate_results/{region}/{tag}/{a.dataset}")
    except Exception as e:
        print(f"[out  ] gate 入库失败: {e}")

    all_pass = all(s["valid"] for s in syntax) and r.returncode == 0
    if a.quality_block and quality_block_ids:
        all_pass = False
    g = gate_json or {}
    qp = report.get("quality_predict") or {}
    qp_note = ""
    if isinstance(qp, dict) and "error" not in qp and qp:
        qp_note = (f" 质量预估 P/R/B={qp.get('pass')}/{qp.get('review')}/{qp.get('block')}"
                   + (f"（BLOCK {len(quality_block_ids)} 条{'计入 FAIL' if a.quality_block else ' 仅标注'}）"
                      if qp.get('block') else ""))
    print(f"[done ] 语法 {report['syntax']['passed']}/{report['syntax']['total']}, "
          f"gate all_pass={g.get('all_pass')} passed={g.get('passed')}/{g.get('total')}"
          f"{qp_note} => {'PASS' if all_pass else 'FAIL'}")
    if r.stderr:
        print(r.stderr[-800:])
    sys.exit(0 if all_pass else 1)

if __name__ == "__main__":
    main()
