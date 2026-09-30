# -*- coding: utf-8 -*-
"""机制-形状一致性软闸（--template-family，WARN 不阻断）。

从 2026-09-30 单文件 `tools/wave_gate.py` 拆出。
校验候选字段的形状+语义是否满足 template_families.json 里该族的 mechanism_premise。
"""
import json
import os
import re

from ._paths import _campaign_store_cls, _load_template_families_for_gate, _wqb_db_path


def _field_profile_map_for_gate(region, dataset, campaign_dir=None):
    """从 wqb.db 读 field_profile（注入 src/）。"""
    try:
        CampaignStore = _campaign_store_cls(campaign_dir)
        st = CampaignStore(_wqb_db_path(campaign_dir))
        try:
            return st.get_field_profile_map(region, dataset)
        finally:
            st.close()
    except Exception:
        return {}


def _extract_fields_from_expr(expr, known_fields):
    """从表达式提取引用的字段 id（在 known_fields 集合内）。"""
    tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr)
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
        if not any(re.search(p, fid, flags=re.IGNORECASE) for p in patterns):
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

    prof_map = _field_profile_map_for_gate(region, a.dataset, campaign)
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
