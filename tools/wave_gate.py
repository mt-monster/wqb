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
            # 2026-09-03 修复：--from-db 时保留 expressions.id，避免 gate_results.syntax.items[].id 是 1-N 序号
            # 2026-09-03 修复2：排除 superseded 行（坏行/已提交候选不应再入门禁与回测）
            items = [{"id": r.get("id"), "expression": r.get("expression")} for r in rows
                     if r.get("expression") and r.get("status") != "superseded"]
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


# ---- 机制-形状一致性软闸（--template-family，WARN 不阻断）----
import re as _re


def _load_template_families_for_gate():
    """加载 toolkit config/template_families.json（config 在 scripts 上一级）。"""
    for d in _TOOLKIT_CANDIDATES:
        if not d:
            continue
        for cand in (os.path.join(os.path.dirname(d), "config", "template_families.json"),
                     os.path.join(d, "config", "template_families.json")):
            if os.path.isfile(cand):
                try:
                    return json.load(open(cand, encoding="utf-8"))
                except Exception:
                    continue
    return {}


def _field_profile_map_for_gate(region, dataset):
    """从 wqb.db 读 field_profile（注入 src/，与 parse_candidates 同模式）。"""
    wqb_root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or r"D:\coding\traeCN_project\wqb"
    src = os.path.join(wqb_root, "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    try:
        from wqb.store import CampaignStore
        st = CampaignStore(os.path.join(wqb_root, "data", "wqb.db"))
        try:
            return st.get_field_profile_map(region, dataset)
        finally:
            st.close()
    except Exception:
        return {}


def _extract_fields_from_expr(expr, known_fields):
    """从表达式提取引用的字段 id（在 known_fields 集合内）。"""
    tokens = _re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr)
    return [t for t in tokens if t in known_fields]


def _match_premise(profile, premise, field_id):
    """轻量版机制前提校验（与 implement_idea._field_matches_family 同逻辑，纯标准库）。"""
    if not premise or not profile:
        return True
    forbidden = premise.get("forbidden_shape")
    if forbidden and (profile.get("shape") or "unknown") in forbidden:
        return False
    shape_req = premise.get("shape_requirement") or {}
    shapes = premise.get("shape") or shape_req.get("shape")
    if shapes and (profile.get("shape") or "unknown") not in shapes:
        return False
    cov = profile.get("coverage")
    cov_max = premise.get("coverage_max") or shape_req.get("coverage_max")
    if cov_max is not None and cov is not None and float(cov) > float(cov_max):
        return False
    cov_min = premise.get("coverage_min") or shape_req.get("coverage_min")
    if cov_min is not None and cov is not None and float(cov) < float(cov_min):
        return False
    if "integer" in premise or "integer" in shape_req:
        want = bool(premise.get("integer", shape_req.get("integer")))
        if bool(profile.get("integer")) != want:
            return False
    freqs = premise.get("freq") or shape_req.get("freq")
    if freqs and (profile.get("freq") or "") not in freqs:
        return False
    dtypes = premise.get("data_type")
    if dtypes:
        ftype = (profile.get("data_type") or profile.get("type") or "").upper()
        if ftype and ftype not in [str(d).upper() for d in dtypes]:
            return False
    sem = premise.get("semantic_requirement") or {}
    patterns = sem.get("field_name_pattern") or []
    if patterns and field_id:
        fid = str(field_id).lower()
        if not any(_re.search(p, fid, flags=_re.IGNORECASE) for p in patterns):
            return False
    return True


def _family_shape_gate(items, a, campaign):
    """机制-形状一致性软闸：校验候选字段形状+语义是否满足 --template-family 的 mechanism_premise。

    WARN 不阻断。返回 {family, checked, mismatches: [{id, fields, shapes}], warn: bool}。
    """
    families = _load_template_families_for_gate().get("families") or []
    family = next((f for f in families if f.get("family_id") == a.template_family), None)
    if not family:
        print(f"[famshape] warn: 族 '{a.template_family}' 未注册，跳过软闸")
        return None
    premise = family.get("mechanism_premise") or family.get("field_profile_match") or {}
    if not premise:
        print(f"[famshape] warn: 族 '{a.template_family}' 无 mechanism_premise，跳过软闸")
        return None

    region = a.region
    if not region:
        try:
            settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
            region = settings.get("region")
        except Exception:
            region = None
    if not region:
        print("[famshape] warn: 无 region，跳过软闸")
        return None

    prof_map = _field_profile_map_for_gate(region, a.dataset)
    if not prof_map:
        print(f"[famshape] warn: {region}/{a.dataset} 无 field_profile，跳过软闸")
        return None
    known = set(prof_map.keys())

    mismatches = []
    checked = 0
    for cid, expr in items:
        fields = _extract_fields_from_expr(expr, known)
        if not fields:
            continue
        checked += 1
        bad = [(f, (prof_map[f].get("shape") or "unknown")) for f in fields
               if not _match_premise(prof_map[f], premise, f)]
        if bad:
            mismatches.append({"id": cid, "bad_fields": bad, "expr": expr[:80]})

    warn = bool(mismatches)
    print(f"[famshape] 族 '{a.template_family}' 机制-形状一致性: {checked} 候选校验, "
          f"{len(mismatches)} 不匹配 => {'WARN' if warn else 'PASS'}")
    for m in mismatches[:5]:
        print(f"[famshape]   不匹配 id={m['id']}: {m['bad_fields']}")
    return {"family": a.template_family, "checked": checked,
            "mismatch_count": len(mismatches), "mismatches": mismatches, "warn": warn}


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
    ap.add_argument("--probe-mode", action="store_true",
                    help="启用 2+6 探针批模式（早期判死）")
    ap.add_argument("--gem-validate", action="store_true",
                    help="启用 GEM 候选池强制校验")
    ap.add_argument("--min-gem-ratio", type=float, default=0.8,
                    help="GEM 候选最小占比（默认 0.8）")
    ap.add_argument("--s2-field-validate", action="store_true",
                    help="启用 S1 字段候选池强制校验（防止跳过特征工程推荐）")
    ap.add_argument("--s2-field-block", action="store_true",
                    help="S1 字段校验失败时计入 FAIL（默认仅标注）")
    ap.add_argument("--template-family", default=None,
                    help="模板族 family_id（template_families.json）。指定时启用机制-形状一致性软闸："
                         "校验候选字段形状+语义是否满足该族 mechanism_premise，不满足标 WARN（不阻断）")
    a = ap.parse_args()

    items = parse_candidates(a)
    campaign = a.campaign_dir.rstrip("/\\")
    tag = a.wave or int(__import__("time").time())

    # ---- 0) GEM 候选池校验（可选）----
    gem_report = None
    if a.gem_validate:
        try:
            tools_dir = os.path.dirname(os.path.abspath(__file__))
            if tools_dir not in sys.path:
                sys.path.insert(0, tools_dir)
            from gem_validator import GEMValidator
            validator = GEMValidator()
            candidates_for_gem = [{"id": cid, "expression": e} for cid, e in items]
            gem_report = validator.validate_wave(candidates_for_gem, tag, a.min_gem_ratio)
            print(f"[gem  ] GEM 候选: {gem_report['gem_count']}/{gem_report['total']} "
                  f"({gem_report['gem_ratio']:.1%}) => {'PASS' if gem_report['pass'] else 'FAIL'}")
            if not gem_report["pass"]:
                print(f"[gem  ] 非 GEM 候选: {len(gem_report['non_gem_candidates'])} 条")
        except Exception as e:
            print(f"[gem  ] GEM 校验失败（不阻断）: {e}")

    # ---- 0.6) 机制-形状一致性软闸（--template-family 指定时启用，WARN 不阻断）----
    family_shape_report = None
    if a.template_family:
        family_shape_report = _family_shape_gate(items, a, campaign)

    # ---- 0.5) S1 字段候选池强制校验（2026-09-03 落地，防 wave=170 事故）----
    s2_field_report = None
    if a.s2_field_validate:
        try:
            tools_dir = os.path.dirname(os.path.abspath(__file__))
            if tools_dir not in sys.path:
                sys.path.insert(0, tools_dir)
            from s2_field_validator import validate_wave_fields
            wqb_root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or r"D:\coding\traeCN_project\wqb"
            db_path = os.path.join(wqb_root, "data", "wqb.db")
            # region 缺省时从 settings.json 读取（与 parse_candidates 对齐）
            region = a.region
            if not region:
                settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
                region = settings.get("region")
            exprs_only = [e for _, e in items]
            s2_field_report = validate_wave_fields(
                region, str(tag), a.dataset, exprs_only, db_path
            )
            print(f"[s2fld] {s2_field_report['message']}")
            if s2_field_report["extra"]:
                print(f"[s2fld] 额外字段（非 S1 推荐）: {s2_field_report['extra'][:5]}")
            if s2_field_report["forbidden"]:
                print(f"[s2fld] 禁用字段命中: {s2_field_report['forbidden']}")
            if not s2_field_report["pass"] and a.s2_field_block:
                print(f"[s2fld] BLOCK 模式：计入 FAIL")
        except Exception as e:
            print(f"[s2fld] S1 字段校验失败（不阻断）: {e}")
            s2_field_report = {"pass": True, "message": f"校验异常: {e}"}

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
    if s2_field_report:
        report["s2_field_validation"] = s2_field_report

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
            
            # 2026-09-04 新增：算子类别覆盖检查（Logical/Group/Vector 至少 1 个）
            import re as _re2
            def _extract_all_operators(expr: str) -> set:
                """提取表达式中所有算子（函数名）。"""
                return set(_re2.findall(r"([a-z_]+)\(", expr))
            
            OP_CATEGORIES = {
                "Logical": {"or", "and", "not", "is_nan", "less", "equal", "greater", "if_else", "not_equal", "less_equal", "greater_equal"},
                "Group": {"group_mean", "group_rank", "group_backfill", "group_scale", "group_count", "group_zscore", "group_std_dev", "group_sum", "group_neutralize", "group_cartesian_product"},
                "Vector": {"vec_min", "vec_count", "vec_sum", "vec_max", "vec_avg", "vec_stddev", "vec_range"},
                "Time Series": {"ts_corr", "ts_zscore", "ts_returns", "ts_product", "ts_std_dev", "ts_backfill", "days_from_last_change", "last_diff_value", "ts_scale", "ts_step", "ts_sum", "ts_av_diff", "ts_kurtosis", "ts_mean", "ts_arg_max", "ts_rank", "ts_ir", "ts_delay", "ts_quantile", "ts_count_nans", "ts_covariance", "ts_decay_linear", "ts_arg_min", "ts_regression", "ts_max_diff", "kth_element", "hump", "ts_delta"},
                "Cross Sectional": {"winsorize", "rank", "zscore", "scale", "normalize", "quantile"},
                "Arithmetic": {"add", "multiply", "sign", "subtract", "pasteurize", "log", "max", "abs", "divide", "min", "signed_power", "inverse", "sqrt", "reverse", "power", "densify"},
            }
            
            all_ops = set()
            for e in passed_exprs:
                all_ops.update(_extract_all_operators(e))
            
            category_coverage = {}
            for cat, ops in OP_CATEGORIES.items():
                covered = ops & all_ops
                category_coverage[cat] = {"covered": len(covered), "total": len(ops), "ops": sorted(covered)}
            
            report["operator_category_coverage"] = category_coverage
            
            # 硬闸：Logical/Group/Vector 至少 1 个
            logical_ok = category_coverage["Logical"]["covered"] >= 1
            group_ok = category_coverage["Group"]["covered"] >= 1
            vector_ok = category_coverage["Vector"]["covered"] >= 1
            
            # 2026-09-04 优化：MATRIX 数据集豁免 Vector 类别（无 VECTOR 字段可用）
            dataset_data_type = None
            try:
                import sqlite3 as _sq2
                wqb_root_tmp = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or r"D:\coding\traeCN_project\wqb"
                conn_tmp = _sq2.connect(os.path.join(wqb_root_tmp, "data", "wqb.db"))
                row_tmp = conn_tmp.execute(
                    "SELECT data_type FROM datasets WHERE name=? LIMIT 1",
                    (a.dataset,)
                ).fetchone()
                conn_tmp.close()
                if row_tmp:
                    dataset_data_type = row_tmp[0]
            except Exception:
                pass
            
            vector_required = dataset_data_type != "MATRIX"  # MATRIX 数据集豁免 Vector
            vector_ok = category_coverage["Vector"]["covered"] >= 1 if vector_required else True
            
            if not (logical_ok and group_ok and vector_ok):
                missing = []
                if not logical_ok:
                    missing.append("Logical")
                if not group_ok:
                    missing.append("Group")
                if not vector_ok:
                    missing.append("Vector")
                report["operator_category_gate"] = {
                    "pass": False,
                    "missing": missing,
                    "message": f"算子类别覆盖不足：缺 {', '.join(missing)} 类别（Logical/Group/Vector 至少各 1 个）"
                }
                print(f"[opcat] 算子类别覆盖 FAIL：缺 {', '.join(missing)} 类别")
                print(f"        Logical: {category_coverage['Logical']['covered']}/{category_coverage['Logical']['total']}, "
                      f"Group: {category_coverage['Group']['covered']}/{category_coverage['Group']['total']}, "
                      f"Vector: {category_coverage['Vector']['covered']}/{category_coverage['Vector']['total']}")
            else:
                report["operator_category_gate"] = {"pass": True}
                print(f"[opcat] 算子类别覆盖 PASS（Logical {category_coverage['Logical']['covered']}/11, "
                      f"Group {category_coverage['Group']['covered']}/10, Vector {category_coverage['Vector']['covered']}/7）")
            wqb_root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or r"D:\coding\traeCN_project\wqb"
            settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
            qregion = a.region or settings.get("region")
            qconn = _sq.connect(os.path.join(wqb_root, "data", "wqb.db"))
            try:
                q_results, _ = qp_mod.predict_all([(e, a.dataset) for e in passed_exprs], qregion, qconn)
            finally:
                qconn.close()
            by_expr = {qr["expr"]: qr for qr in q_results}  # expr 被截断 120 字符，全量表达式前缀匹配
            qp_summary = {"direct_submit": 0, "combo_candidate": 0, "weak_signal": 0,
                          "expected_block": 0, "hard_reject": 0, "blocked": []}
            for (cid, e), s in zip(items, syntax):
                if not s["valid"]:
                    continue
                qr = by_expr.get(e[:120])
                if not qr:
                    continue
                v = qr["verdict"]
                if v == "DIRECT_SUBMIT":
                    qp_summary["direct_submit"] += 1
                elif v == "COMBO_CANDIDATE":
                    qp_summary["combo_candidate"] += 1
                elif v == "WEAK_SIGNAL":
                    qp_summary["weak_signal"] += 1
                elif v == "HARD_REJECT":
                    qp_summary["hard_reject"] += 1
                    quality_block_ids.append(cid)
                    qp_summary["blocked"].append({"id": cid, "reasons": qr["reasons"], "verdict": v})
                    print(f"[qp   ] HARD_REJECT {cid}: {'; '.join(qr['reasons'])}")
                else:  # EXPECTED_BLOCK
                    qp_summary["expected_block"] += 1
                    quality_block_ids.append(cid)
                    qp_summary["blocked"].append({"id": cid, "reasons": qr["reasons"], "verdict": v})
                    print(f"[qp   ] BLOCK {cid}: {'; '.join(qr['reasons'])}")
            report["quality_predict"] = qp_summary
            print(f"[qp   ] 质量预估: DIRECT={qp_summary['direct_submit']} COMBO={qp_summary['combo_candidate']} "
                  f"WEAK={qp_summary['weak_signal']} BLOCK={qp_summary['expected_block']} "
                  f"HARD={qp_summary['hard_reject']}" + ("（计入 FAIL）" if a.quality_block else "（仅标注）"))
        except Exception as e:
            report["quality_predict"] = {"error": str(e)}
            print(f"[qp   ] 质量预估阶段失败（不阻断门禁）: {e}")

    # ---- 3.5) 参数变体聚类（2026-09-02 优化点⑤：同骨架同字段仅差参数的归一簇）----
    # 背景：wave 146 三条全闸通过候选互相关 0.9933-0.9985（max_mutually_below_subset=1），
    # Mode A 参数变体不构成多颗额度。此闸在回测前识别变体簇，每簇只留 1 条。
    variant_clusters = {}
    variant_warnings = []
    if not a.skip_quality:
        import re as _re
        def _extract_skeleton(expr: str) -> str:
            """提取表达式骨架：去掉数字参数，只留结构。"""
            s = _re.sub(r'\d+\.?\d*', 'N', expr)
            s = _re.sub(r'\s+', '', s)
            return s
        def _extract_fields(expr: str) -> frozenset:
            """提取表达式中的字段名（vec_avg/vec_sum 包裹的或裸字段）。"""
            fields = set()
            for m in _re.finditer(r'vec_(?:avg|sum)\(([a-zA-Z_][\w]*)\)', expr):
                fields.add(m.group(1))
            _ops = {'rank','ts_delta','ts_mean','ts_zscore','ts_backfill','vec_avg','vec_sum',
                    'divide','subtract','add','multiply','ts_decay_linear','group_neutralize',
                    'ts_std_dev','abs','sign','log','max','min','if_else','ts_rank','scale',
                    'group_rank','ts_sum','ts_av_diff','ts_delay','ts_corr','ts_covariance',
                    'group_zscore','ts_regression','last_diff_value','kth_element','ts_arg_max',
                    'ts_arg_min','ts_max','ts_min','ts_product','inverse','signed_power','tail',
                    'trade_when','is_nan','nan_out','purify','densify','winsorize','zscore',
                    'ts_count_nans','ts_median','ts_percentile','ts_step','ts_scale','reverse',
                    'bucket','industry','sector','subindustry','market','country'}
            for tok in _re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]{3,}\b', expr):
                if tok.lower() not in _ops and not tok.isdigit():
                    fields.add(tok)
            return frozenset(fields)
        passed_items = [(cid, e) for (cid, e), s in zip(items, syntax) if s["valid"]]
        for cid, e in passed_items:
            skel = _extract_skeleton(e)
            fields = _extract_fields(e)
            key = (skel, fields)
            if key not in variant_clusters:
                variant_clusters[key] = []
            variant_clusters[key].append((cid, e))
        for key, cluster in variant_clusters.items():
            if len(cluster) > 1:
                ids = [cid for cid, _ in cluster]
                variant_warnings.append({
                    "cluster_ids": ids,
                    "count": len(cluster),
                    "skeleton_preview": cluster[0][1][:80],
                    "fields": sorted(key[1]),
                })
                print(f"[var  ] 参数变体簇 {ids}: {len(cluster)} 条同骨架同字段，建议只留 1 条")
        if variant_warnings:
            report["variant_clusters"] = variant_warnings
            print(f"[var  ] 共发现 {len(variant_warnings)} 个参数变体簇（回测前建议每簇只留 1 条）")
        else:
            print(f"[var  ] 参数变体聚类 PASS（无同骨架同字段变体）")

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

    # ---- 4) 探针批模式（可选）----
    probe_report = None
    if a.probe_mode and len(items) > 2:
        try:
            tools_dir = os.path.dirname(os.path.abspath(__file__))
            if tools_dir not in sys.path:
                sys.path.insert(0, tools_dir)
            from probe_batch_mode import ProbeBatchExecutor
            # gate 阶段只做探针分配标记（结构预判），不做真实回测
            executor = ProbeBatchExecutor(
                campaign, a.dataset, 0,  # wave=0 占位，gate 阶段不需要
                datasets_extra=a.datasets or "",
                dry_run=True)
            candidates_for_probe = [{"id": cid, "expression": e} for cid, e in items]
            # 只做探针分配，不执行回测
            probe_candidates = executor.select_probe_candidates(candidates_for_probe, n=2)
            probe_report = {
                "status": "PROBE_ASSIGNED",
                "probe_ids": [c.get("id") for c in probe_candidates],
                "probe_count": len(probe_candidates),
                "total_count": len(candidates_for_probe),
                "decision_reason": "gate 阶段探针分配（回测判死走 probe_batch_mode.py）",
                "saved_quota": 0,
            }
            print(f"[probe] 探针批模式: {probe_report['status']}")
            print(f"[probe] 决策原因: {probe_report['decision_reason']}")
            if probe_report["saved_quota"] > 0:
                print(f"[probe] 节省配额: {probe_report['saved_quota']} 条")
        except Exception as e:
            print(f"[probe] 探针批模式失败（不阻断）: {e}")

    all_pass = all(s["valid"] for s in syntax) and r.returncode == 0
    if a.quality_block and quality_block_ids:
        all_pass = False
    if gem_report and not gem_report["pass"]:
        all_pass = False
    if s2_field_report and not s2_field_report["pass"] and a.s2_field_block:
        all_pass = False
    if probe_report and probe_report["status"] == "PROBE_DEAD":
        all_pass = False
        print(f"[done ] 探针批判死数据集，整波拦截")
    g = gate_json or {}
    qp = report.get("quality_predict") or {}
    qp_note = ""
    if isinstance(qp, dict) and "error" not in qp and qp:
        qp_note = (f" 质量预估 D/C/W/B/H={qp.get('direct_submit')}/{qp.get('combo_candidate')}/"
                   f"{qp.get('weak_signal')}/{qp.get('expected_block')}/{qp.get('hard_reject')}"
                   + (f"（拦截 {len(quality_block_ids)} 条{'计入 FAIL' if a.quality_block else ' 仅标注'}）"
                      if (qp.get('expected_block') or qp.get('hard_reject')) else ""))
    gem_note = f" GEM={gem_report['gem_ratio']:.0%}" if gem_report else ""
    s2fld_note = ""
    if s2_field_report:
        cov = s2_field_report.get("coverage", 0)
        s2fld_note = f" S1字段={cov:.0%}" + ("(BLOCK)" if not s2_field_report["pass"] and a.s2_field_block else "")
    probe_note = f" Probe={probe_report['status']}" if probe_report else ""
    print(f"[done ] 语法 {report['syntax']['passed']}/{report['syntax']['total']}, "
          f"gate all_pass={g.get('all_pass')} passed={g.get('passed')}/{g.get('total')}"
          f"{qp_note}{gem_note}{s2fld_note}{probe_note} => {'PASS' if all_pass else 'FAIL'}")
    if r.stderr:
        print(r.stderr[-800:])
    sys.exit(0 if all_pass else 1)

if __name__ == "__main__":
    main()
