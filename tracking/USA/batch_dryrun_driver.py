# -*- coding: utf-8 -*-
"""USA 批量 dry-run 驱动：对 S0 白名单数据集跑 S1(scan-fields)→S2(GEM v2 ideas)→S3(build-wave+gate)。

Path 1 修复验证横向扩展：每个数据集生成含 ts_arg_max/ts_arg_min 概念的 ideas 文件
（满足 explore_contract 多样性契约），GEM --ideas-file 直实现（无 LLM），零回测配额。

断点续跑：checkpoint 原子写（tmp+os.replace）；status=done 的数据集跳过。
用法:
  python batch_dryrun_driver.py                # 跑全部待办
  python batch_dryrun_driver.py --limit 5      # 只跑前 5 个（冒烟）
  python batch_dryrun_driver.py --only ds1,ds2 # 指定数据集
  python batch_dryrun_driver.py --include-done # 含已完成也重跑
"""
import argparse
import datetime
import json
import os
import sqlite3
import subprocess
import sys
import time

import os.path as _osp

# ---- 路径自动解析（与 tools/wave_gate.py 的 WQ_TOOLKIT_DIR 模式对齐，勿硬编码）----
_HOME = os.path.expanduser("~")
_REPO_ROOT = _osp.dirname(_osp.dirname(_osp.dirname(_osp.abspath(__file__))))

WQ_PY = os.environ.get(
    "WQ_PY",
    _osp.join(_REPO_ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe"),
)

_TOOLKIT_CANDIDATES = [
    os.environ.get("WQ_TOOLKIT_DIR"),
    _osp.join(_HOME, ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts"),
    _osp.join(_HOME, ".cursor", "skills", "wq-brain-campaign-toolkit", "scripts"),
    _osp.join(_HOME, ".workbuddy", "skills", "wq-brain-campaign-toolkit", "scripts"),
]
TK = next((c for c in _TOOLKIT_CANDIDATES if c and _osp.isdir(_osp.join(c, "_lib"))), _TOOLKIT_CANDIDATES[1])

_GEM_CANDIDATES = [
    os.environ.get("WQ_GEM_DIR"),
    _osp.join(_HOME, ".qoder-cn", "skills", "brain-makeSomeGem", "scripts", "headless_runner"),
    _osp.join(_HOME, ".cursor", "skills", "brain-makeSomeGem", "scripts", "headless_runner"),
    _osp.join(_HOME, ".workbuddy", "skills", "brain-makeSomeGem", "scripts", "headless_runner"),
]
_GEM_DIR = next((c for c in _GEM_CANDIDATES if c and _osp.isfile(_osp.join(c, "run.py"))), _GEM_CANDIDATES[1])
GEM_RUN = _osp.join(_GEM_DIR, "run.py")
GEM_CFG = _osp.join(_GEM_DIR, "config.json")
GEM_CWD = _GEM_DIR

CD = _osp.join(_REPO_ROOT, "tracking", "USA")
DB = _osp.join(_REPO_ROOT, "data", "wqb.db")
PRIORS = os.path.join(CD, "priors", "usa_priors.json")
IDEAS_DIR = os.path.join(CD, "ideas_gen")
CKPT = os.path.join(CD, "batch_dryrun_ckpt.json")

# registry dead_end family 前缀（这些数据集不进批量，S-PRE 纪律）
DEAD_PREFIXES = (
    "ai_news_scores", "earningscall_embed", "event_sentiment_signals",
    "insider_feats", "multifactor_return_pred", "news_sentiment_dl",
    "ml_factor_proj", "option_chart_model",
)

sys.path.insert(0, TK)


def run_cmd(cmd, timeout=600, cwd=None):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace",
                           timeout=timeout, cwd=cwd)
        return p.returncode, p.stdout or "", p.stderr or ""
    except subprocess.TimeoutExpired:
        return -9, "", "TIMEOUT"


def atomic_write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def load_whitelist():
    db = sqlite3.connect(DB)
    try:
        row = db.execute("SELECT value FROM ledger_kv WHERE region='USA' AND key='s0_whitelist'").fetchone()
        return json.loads(row[0])["whitelist"]
    finally:
        db.close()


def load_checkpoint():
    if os.path.exists(CKPT):
        try:
            return json.load(open(CKPT, encoding="utf-8"))
        except Exception:
            pass
    return {"results": []}


def save_checkpoint(ckpt):
    atomic_write_json(CKPT, ckpt)


def gen_ideas_md(ds, catalog, region="USA", delay=1):
    """从 catalog top 字段生成 Path1 v2 ideas（4 ts_arg + 4 level/delta 概念）。"""
    fields = [f for f in (catalog.get("fields") or []) if f.get("id")]
    data_type = (catalog.get("data_type") or "MATRIX").upper()
    if data_type not in ("MATRIX", "VECTOR"):
        data_type = "MATRIX"
    pool = [f for f in fields if (f.get("type") or "").upper() == data_type]
    if not pool:  # 类型不符时回退到全量
        pool = fields
        data_type = (pool[0].get("type") or "MATRIX").upper() if pool else "MATRIX"
        if data_type not in ("MATRIX", "VECTOR"):
            data_type = "MATRIX"
    pool.sort(key=lambda f: -(f.get("coverage") or 0))
    top = pool[:2]
    if len(top) < 2:
        top = (pool + [None])[:2] if pool else [None, None]

    def wrap(name):
        # VECTOR 字段先 vec_avg 转矩阵
        return f"vec_avg({{{name}}})" if data_type == "VECTOR" else f"{{{name}}}"

    f1 = top[0]["id"] if top[0] else None
    f2 = top[1]["id"] if top[1] else f1
    concepts = []
    if f1:
        w1 = wrap(f1)
        concepts += [
            (f"Recency of peak conviction on {f1} (ts_arg_max, 20d)",
             f"quantile(-ts_arg_max(ts_backfill({w1}, 66), 20))"),
            (f"Recency of trough conviction on {f1} (ts_arg_min, 20d)",
             f"quantile(ts_arg_min(ts_backfill({w1}, 66), 20))"),
            (f"Revision of {f1} (5-day change)",
             f"quantile(ts_delta(ts_backfill({w1}, 66), 5))"),
        ]
    if f2 and f2 != f1:
        w2 = wrap(f2)
        concepts += [
            (f"Recency of peak signal on {f2} (ts_arg_max, 10d)",
             f"quantile(-ts_arg_max(ts_backfill({w2}, 66), 10))"),
            (f"Recency of trough signal on {f2} (ts_arg_min, 10d)",
             f"quantile(ts_arg_min(ts_backfill({w2}, 66), 10))"),
            (f"Cross spread {f1} minus {f2}",
             f"quantile(subtract(ts_backfill({wrap(f1)}, 66), ts_backfill({w2}, 66)))"),
            (f"Level rank of {f2}",
             f"quantile(rank(ts_backfill({w2}, 66)))"),
        ]
    # 去重模板
    seen, uniq = set(), []
    for name, tpl in concepts:
        if tpl not in seen:
            seen.add(tpl)
            uniq.append((name, tpl))

    lines = [f"**Dataset**: {ds}  ", f"**Region**: {region}  ",
             f"**Delay**: {delay}  ", "**Universe**: TOP3000", ""]
    for i, (name, tpl) in enumerate(uniq, 1):
        fields_str = ", ".join(f"`{f1}`" if j == 0 else f"`{f2}`"
                                for j in range(min(2, 1 if not f2 or f2 == f1 else 2)))
        lines += [
            f"**Concept**: {name}",
            "- **Mechanism**: Generic Path-1 diversity concept for dry-run extensibility "
            f"validation on dataset {ds}. The operator topology (ts_arg_max/ts_arg_min timing "
            "features plus level/difference probes) is what matters here, not signal semantics.",
            f"- **Fields**: {fields_str}",
            f"- **Implementation Example**: `{tpl}`",
            "- **Direction**: High → long.",
            "- **Why not crowded**: ts_arg timing features are outside the saturated "
            "level/revision probe family.",
            "",
        ]
    os.makedirs(IDEAS_DIR, exist_ok=True)
    path = os.path.join(IDEAS_DIR, f"{ds}_v2.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path, data_type, f1, f2


def count_wave_exprs(ds):
    db = sqlite3.connect(DB)
    try:
        n = db.execute("SELECT COUNT(*) FROM expressions WHERE wave=?", (f"s2_{ds}_d1",)).fetchone()[0]
        w = db.execute("SELECT COUNT(*) FROM expressions WHERE wave=?", (f"w_{ds}",)).fetchone()[0]
        return n, w
    finally:
        db.close()


def parse_gate_json(stdout):
    idx = stdout.find("{")
    if idx < 0:
        return None
    try:
        return json.loads(stdout[idx:])
    except Exception:
        # 尝试匹配最外层大括号
        depth, start = 0, idx
        for i, ch in enumerate(stdout[idx:], idx):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(stdout[start:i + 1])
                    except Exception:
                        return None
        return None


def process_dataset(entry):
    ds = entry["id"]
    rec = {"dataset": ds, "category": entry.get("category"),
           "score": entry.get("score"), "started_at": datetime.datetime.now().isoformat(timespec="seconds")}
    t0 = time.time()

    # S1: scan-fields（落 catalog 到 DB）
    rc, out, err = run_cmd([WQ_PY, os.path.join(TK, "campaign.py"), "--campaign-dir", CD,
                            "scan-fields", "--dataset", ds], timeout=300)
    if rc != 0:
        rec.update(status="scan_fail", error=(err or out)[-400:])
        return rec
    rec["scan"] = (err or "").strip().splitlines()[-1] if err else "ok"

    # 读 catalog
    try:
        from _lib.common import CampaignContext
        from _lib.wqb_store import load_catalog
        catalog = load_catalog(CampaignContext(CD), ds)
    except Exception as exc:
        rec.update(status="catalog_fail", error=f"{type(exc).__name__}: {exc}"[:400])
        return rec
    if not catalog or not catalog.get("fields"):
        rec.update(status="empty_catalog", error=f"field_count={catalog.get('field_count') if catalog else None}")
        return rec

    # 生成 v2 ideas
    try:
        ideas_path, data_type, f1, f2 = gen_ideas_md(ds, catalog)
    except Exception as exc:
        rec.update(status="ideas_fail", error=f"{type(exc).__name__}: {exc}"[:400])
        return rec
    rec.update(field_count=catalog.get("field_count"), data_type=data_type,
               top_fields=[f1, f2])

    # S2: GEM --ideas-file（无 LLM，模板实现）
    rc, out, err = run_cmd([WQ_PY, GEM_RUN, "--config", GEM_CFG,
                            "--data-category", str(entry.get("category") or "other"),
                            "--region", "USA", "--delay", "1",
                            "--dataset-id", ds, "--universe", "TOP3000",
                            "--instrument-type", "EQUITY", "--data-type", data_type,
                            "--ideas-file", ideas_path,
                            "--priors-file", PRIORS, "--max-expressions", "12"],
                           timeout=900, cwd=GEM_CWD)
    if rc != 0:
        rec.update(status="gem_fail", error=(err or out)[-400:])
        return rec

    # S3a: build-wave
    rc, out, err = run_cmd([WQ_PY, os.path.join(TK, "campaign.py"), "--campaign-dir", CD,
                            "build-wave", "--from-db", "--dataset", ds,
                            "--wave", f"w_{ds}"], timeout=300)
    if rc != 0:
        rec.update(status="buildwave_fail", error=(err or out)[-400:])
        return rec

    # S3b: gate
    rc, out, err = run_cmd([WQ_PY, os.path.join(TK, "campaign.py"), "--campaign-dir", CD,
                            "gate", "--from-db", "--wave", f"w_{ds}", "--dataset", ds],
                           timeout=300)
    gate = parse_gate_json(out) if rc == 0 else None
    n_s2, n_wave = count_wave_exprs(ds)
    rec.update(n_gem_exprs=n_s2, n_wave_selected=n_wave)
    if gate is None:
        rec.update(status="gate_parse_fail", error=(err or out)[-400:])
        return rec
    div = gate.get("diversity_gate") or {}
    rec.update(status="done",
               gate_all_pass=gate.get("all_pass"),
               gate_total=gate.get("total"),
               gate_passed=gate.get("passed"),
               diversity_applied=div.get("applied"),
               diversity_pass=div.get("pass"),
               diversity_issues=div.get("issues") or [],
               duration_s=round(time.time() - t0, 1))
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--only", default=None, help="逗号分隔数据集")
    ap.add_argument("--include-done", action="store_true")
    a = ap.parse_args()

    wl = load_whitelist()
    ckpt = load_checkpoint()
    done = {r["dataset"] for r in ckpt["results"] if r.get("status") == "done"}

    # seed：event_return_model 已在 event02 手工验证
    if "event_return_model" not in done and "event_return_model" not in (a.only or ""):
        ckpt["results"].append({
            "dataset": "event_return_model", "category": "news", "score": 0.828,
            "status": "done", "gate_all_pass": True, "gate_total": 6, "gate_passed": 6,
            "diversity_applied": True, "diversity_pass": True, "diversity_issues": [],
            "note": "seed: event02 手工验证（Path1 v2 ideas）",
        })
        done.add("event_return_model")
        save_checkpoint(ckpt)

    todo = []
    for e in sorted(wl, key=lambda x: -x["score"]):
        ds = e["id"]
        if ds.startswith(DEAD_PREFIXES):
            continue
        if a.only:
            if ds in [s.strip() for s in a.only.split(",")]:
                todo.append(e)
            continue
        if not a.include_done and ds in done:
            continue
        todo.append(e)
    if a.limit:
        todo = todo[:a.limit]

    print(f"[batch] whitelist={len(wl)} done={len(done)} todo={len(todo)}", flush=True)
    for i, e in enumerate(todo, 1):
        print(f"\n[batch {i}/{len(todo)}] {e['id']} (cat={e['category']}, score={e['score']:.3f})", flush=True)
        try:
            rec = process_dataset(e)
        except Exception as exc:
            rec = {"dataset": e["id"], "status": "crash",
                   "error": f"{type(exc).__name__}: {exc}"[:400]}
        # 记录（幂等：替换同 dataset 旧记录）
        ckpt = load_checkpoint()
        ckpt["results"] = [r for r in ckpt["results"] if r["dataset"] != rec["dataset"]]
        ckpt["results"].append(rec)
        ckpt["updated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
        save_checkpoint(ckpt)
        print(f"[batch] {e['id']} -> {rec.get('status')} "
              f"(all_pass={rec.get('gate_all_pass')} div={rec.get('diversity_pass')} "
              f"{rec.get('duration_s','?')}s)", flush=True)

    # 汇总
    ckpt = load_checkpoint()
    rs = [r for r in ckpt["results"]]
    done_rs = [r for r in rs if r.get("status") == "done"]
    n_allpass = sum(1 for r in done_rs if r.get("gate_all_pass"))
    n_div = sum(1 for r in done_rs if r.get("diversity_pass"))
    print(f"\n[summary] total={len(rs)} done={len(done_rs)} all_pass={n_allpass} "
          f"diversity_pass={n_div} fail={len(rs)-len(done_rs)}", flush=True)
    for st in ("scan_fail", "catalog_fail", "empty_catalog", "ideas_fail",
               "gem_fail", "buildwave_fail", "gate_parse_fail", "crash"):
        bad = [r["dataset"] for r in rs if r.get("status") == st]
        if bad:
            print(f"  {st}: {bad}", flush=True)


if __name__ == "__main__":
    main()
