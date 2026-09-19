# -*- coding: utf-8 -*-
"""GEM 知识库层：CampaignStore 定位与模板族（field_profile 画像）绑定。

2026-09-12 从 run_pipeline.py 拆出。

注意：_wqb_campaign_store 被 economic_priors.py 反向引用
（`from run_pipeline import _wqb_campaign_store`，函数内延迟导入以避免循环），
run_pipeline.py 必须 re-export 本函数的引用。
"""
import json
import os
import sys
from pathlib import Path

from skill_roots import candidate_paths_under_skill


def _wqb_campaign_store():
    """Locate CampaignStore from skill scripts (workspace src/)."""
    roots = [
        os.environ.get("WQB_ROOT"),
        os.environ.get("WQ_PROJECT_ROOT"),
        r"D:\coding\traeCN_project\wqb",
    ]
    for root in roots:
        if not root:
            continue
        src = os.path.join(root, "src")
        if os.path.isdir(os.path.join(src, "wqb")):
            if src not in sys.path:
                sys.path.insert(0, src)
            from wqb.store import CampaignStore
            db = os.environ.get("WQB_DB_PATH") or os.path.join(root, "data", "wqb.db")
            return CampaignStore(db)
    raise ImportError("wqb.store not found; set WQB_ROOT")


def _load_template_families() -> dict:
    """加载 toolkit config/template_families.json（字段画像驱动模板族）。

    定位顺序：WQ_TOOLKIT_DIR 覆盖 → `skill_roots()`（技能根单源：env → ~/.claude →
    ~/.codex → 历史位 → 仓库自带 Claude/skills，见同目录 skill_roots.py 模块头）。
    返回 {'families': [...], 'free_explore_family': {...}}；找不到返回 {}。
    """
    candidates = []
    env = os.environ.get("WQ_TOOLKIT_DIR")
    if env:
        # WQ_TOOLKIT_DIR 指向 scripts/，config 在其上一级
        candidates.append(os.path.join(os.path.dirname(env), "config", "template_families.json"))
        candidates.append(os.path.join(env, "config", "template_families.json"))
    candidates.extend(candidate_paths_under_skill(
        "wq-brain-campaign-toolkit", "config", "template_families.json"))
    for path in candidates:
        try:
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            continue
    return {}


def _check_family_dataset_fit(family: dict, data_category: str) -> tuple:
    """机制⇄数据类别匹配门：数据集类别是否在族的 mechanism_premise.data_category 内。

    返回 (fit: bool, reason: str)。data_category 为空（未约束）→ 通过。
    这是烧配额前的拦截门：analyst 数据集不该进 event_conviction 族（KOR 实证全 fail）。
    """
    premise = family.get("mechanism_premise") or {}
    allowed = premise.get("data_category") or (family.get("field_profile_match") or {}).get("data_category") or []
    if not allowed:
        return True, ""
    dc = (data_category or "").strip().lower()
    allowed_l = [str(c).lower() for c in allowed]
    if dc and dc not in allowed_l:
        exclusion = premise.get("dataset_exclusion") or ""
        reason = (f"数据集类别 '{data_category}' 不在族 '{family.get('family_id')}' 的适用类别 {allowed}"
                  f"（机制前提不匹配）" + (f"；{exclusion}" if exclusion else ""))
        return False, reason
    return True, ""


def _prepare_family_binding(region: str, dataset_id: str, family_id: str,
                            out_dir: Path, data_category: str | None = None) -> tuple:
    """为模板族生成准备画像过滤输入（field_profile + family_match JSON 文件）。

    流程：① 机制⇄数据类别匹配门（不匹配返回 ('BLOCKED', reason)）；② 读 field_profile；
    ③ 优先取 mechanism_premise 作为 family_match（含 forbidden_shape + semantic_requirement），
    fallback 到 field_profile_match；④ 各写一个 JSON 文件供 implement_idea.py 消费。
    返回 (field_profile_path, family_match_path)；('BLOCKED', reason) 表示机制不匹配应拦截；
    (None, None) 表示跳过画像过滤（降级）。
    """
    families_cfg = _load_template_families()
    families = families_cfg.get("families") or []
    family = next((f for f in families if f.get("family_id") == family_id), None)
    if not family:
        print(f"[family] warn: template family '{family_id}' 未在 template_families.json 注册，跳过画像过滤", flush=True)
        return None, None

    # 机制⇄数据类别匹配门（烧配额前拦截）
    if data_category:
        fit, reason = _check_family_dataset_fit(family, data_category)
        if not fit:
            print(f"[family] BLOCKED: {reason}", flush=True)
            return "BLOCKED", reason

    # 优先 mechanism_premise（含 forbidden_shape + semantic_requirement），fallback field_profile_match
    family_match = family.get("mechanism_premise") or family.get("field_profile_match") or {}
    if not family_match:
        print(f"[family] warn: family '{family_id}' 无 mechanism_premise/field_profile_match，跳过画像过滤", flush=True)
        return None, None

    try:
        store = _wqb_campaign_store()
        try:
            profile_map = store.get_field_profile_map(region, dataset_id)
        finally:
            try:
                store.close()
            except Exception:
                pass
    except Exception as exc:
        print(f"[family] warn: 读取 field_profile 失败（{exc}），跳过画像过滤", flush=True)
        return None, None
    if not profile_map:
        print(f"[family] warn: {region}/{dataset_id} 无 field_profile（先跑 tools/field_profile_backfill.py），跳过画像过滤", flush=True)
        return None, None

    out_dir.mkdir(parents=True, exist_ok=True)
    fp_path = out_dir / "family_field_profile.json"
    fm_path = out_dir / "family_match.json"
    fp_path.write_text(json.dumps(profile_map, ensure_ascii=False, indent=1), encoding="utf-8")
    fm_path.write_text(json.dumps(family_match, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[family] 模板族 '{family_id}' 画像过滤就绪: {len(profile_map)} 字段画像, "
          f"match={list(family_match.keys())}", flush=True)
    return str(fp_path), str(fm_path)
