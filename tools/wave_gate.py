# -*- coding: utf-8 -*-
"""wave_gate.py - 每波门禁编排器（替代 tracking/<REGION>/scripts/_gate_waveNN.py 族）。

在单次调用内完成：
  1) 候选解析：--candidates JSON（{expressions:[{id,expr}]} / [str] / {exprs:[...]}）
     或 --exprs-file（每行一条）或 --expr（单条）
  2) 语法校验：alpha-expression-verifier（与 gate 闸1 同源，先于 5 闸执行，
     失败即整波拦截——语法错误是整批 CANCELLED 连坐的头号元凶）
  3) 5 闸预检 + 批级多样性：复用 wq-brain-campaign-toolkit 的权威 gate.py
     （路径自动解析 WQ_TOOLKIT_DIR → .qoder-cn/.workbuddy/.cursor，勿硬编码）
  4) 结果落盘：<campaign-dir>/cache/gate_wave<wave>_<dataset>.json（完整）
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
_TOOLKIT_CANDIDATES = [
    os.environ.get("WQ_TOOLKIT_DIR"),
    os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts"),
    os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "wq-brain-campaign-toolkit", "scripts"),
    r"D:\coding\traeCN_project\wqb\.cursor\skills\wq-brain-campaign-toolkit\scripts",
]
_VALIDATOR_CANDIDATES = [
    os.environ.get("WQ_VALIDATOR_DIR"),
    os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills", "alpha-expression-verifier", "scripts"),
    os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "alpha-expression-verifier", "scripts"),
    r"D:\coding\traeCN_project\wqb\.cursor\skills\alpha-expression-verifier\scripts",
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
    """候选解析 → [(id_or_index, expr)]；兼容 {expressions:[{id,expr}...]} / [str] / {exprs}。"""
    if a.candidates:
        d = json.load(open(a.candidates, encoding="utf-8"))
        items = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
    elif a.exprs_file:
        items = [ln.strip() for ln in open(a.exprs_file, encoding="utf-8") if ln.strip()]
    elif a.expr:
        items = [a.expr]
    else:
        raise SystemExit("need --candidates / --exprs-file / --expr 之一")
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
        raise SystemExit(f"候选解析为空（{a.candidates or a.exprs_file or a.expr}）")
    return out


def main():
    ap = argparse.ArgumentParser(description="每波门禁编排器：语法 + 5 闸 + 多样性，一键落盘")
    ap.add_argument("--campaign-dir", required=True, help="战役根目录 (如 tracking/KOR)")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--wave", type=int, default=0, help="波号，用于落盘文件名（缺省用当前时间）")
    ap.add_argument("--candidates", help="候选 JSON（门禁主入口，格式兼容 gate.py）")
    ap.add_argument("--exprs-file", help="每行一条表达式的 txt")
    ap.add_argument("--expr", help="单条表达式")
    ap.add_argument("--skip-diversity-gate", action="store_true", help="透传 toolkit gate.py（repair 批等）")
    ap.add_argument("--batch-type", default="explore", help="透传 toolkit gate.py（explore/repair...）")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--fix", action="store_true", help="透传：VECTOR 数据集自动裹 vec_* 后检测")
    a = ap.parse_args()

    items = parse_candidates(a)
    campaign = a.campaign_dir.rstrip("/\\")
    cache_dir = os.path.join(campaign, "cache")
    os.makedirs(cache_dir, exist_ok=True)
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

    # ---- 2) 5 闸 + 多样性（权威实现：toolkit gate.py）----
    gate_py = find_script(_TOOLKIT_CANDIDATES, "gate.py")
    inp = os.path.join(cache_dir, f"wave{tag}_gate_input.json")
    json.dump({"expressions": [e for _, e in items]}, open(inp, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    cache_file = os.path.join(cache_dir, f"gate_wave{tag}_{a.dataset}.json")
    cmd = [sys.executable, gate_py, "--campaign-dir", campaign, "--dataset", a.dataset,
           "--file", inp, "--cache-file", cache_file, "--batch-type", a.batch_type]
    if a.skip_diversity_gate:
        cmd.append("--skip-diversity-gate")
    if a.no_cache:
        cmd.append("--no-cache")
    if a.fix:
        cmd.append("--fix")
    print(f"\n[gate ] {os.path.basename(gate_py)} (exit 数据见 cache/gate_wave{tag}_{a.dataset}.json)")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    gate_json = None
    try:
        start, end = r.stdout.find("{"), r.stdout.rfind("}")
        if start >= 0 and end > start:
            gate_json = json.loads(r.stdout[start:end + 1])
    except Exception:
        gate_json = None

    # ---- 3) 落盘完整报告 + 人类摘要 ----
    report = {
        "wave": a.wave, "dataset": a.dataset, "campaign_dir": campaign,
        "gate_exit": r.returncode,
        "syntax": {"total": len(syntax), "passed": sum(1 for s in syntax if s["valid"]),
                   "items": syntax},
        "gate": gate_json or {"all_pass": False, "raw_tail": (r.stdout or "")[-2000:]},
    }
    json.dump(report, open(os.path.join(cache_dir, f"gate_wave{tag}_{a.dataset}.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=1)
    out_txt = os.path.join(cache_dir, f"gate_wave{tag}_{a.dataset}.out.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"wave={a.wave} dataset={a.dataset}\n")
        f.write(f"[syntax] {report['syntax']['passed']}/{report['syntax']['total']} PASS\n")
        f.write("--- gate stdout ---\n" + (r.stdout or "")[-2500:] + "\n--- gate stderr ---\n" + (r.stderr or "")[-800:])
    print(f"\n[out  ] {out_txt}")

    all_pass = all(s["valid"] for s in syntax) and r.returncode == 0
    g = gate_json or {}
    print(f"[done ] 语法 {report['syntax']['passed']}/{report['syntax']['total']}, "
          f"gate all_pass={g.get('all_pass')} passed={g.get('passed')}/{g.get('total')} "
          f"=> {'PASS' if all_pass else 'FAIL'}")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()