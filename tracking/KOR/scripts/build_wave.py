# -*- coding: utf-8 -*-
"""build_wave.py - 统一选波器（多维骨架标签默认启用）

能力:
  - 全历史去重（M6）：对 tracking/KOR 下全部 kor_wave*_exprs.json / candidates/*.json
    建表达式哈希集，重复候选直接丢弃（战役实测 92/854 重复 = 11% 配额浪费）
  - 多维骨架标签（默认启用）：四维标签选波（结构/构造链/机制/字段匹配）
  - 配额约束：按 tools/skeleton_quota.json 的配额配置限制各维度占比
  - near-miss 加权：读 reviews/*.json 的 near 池字段，含近门槛字段的候选优先
  - 波内字段去重：同一字段在单波出现次数上限

用法:
  python build_wave.py --file candidates/new_exprs.json --wave 36A [--size 48]
  python build_wave.py --file candidates/new_exprs.json --wave 36A --legacy [--size 48]  # 传统模式（已废弃）
输出:
  candidates/kor_wave<wave>_exprs.json
"""
import argparse, collections, datetime, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# 注入 tools 目录以导入 skeleton_tags
# 从 tracking/KOR/scripts 向上三级到项目根目录，再进入 tools
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TOOLS_DIR = os.path.join(PROJECT_ROOT, "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

try:
    from skeleton_tags import batch_extract_tags, summarize_tags, DEFAULT_QUOTA
    MULTIDIM_AVAILABLE = True
except ImportError:
    MULTIDIM_AVAILABLE = False
    print("[error] skeleton_tags 未安装，多维标签功能不可用")
    sys.exit(1)


def norm(e):
    return re.sub(r"\s+", "", e)


def history_hashes(exclude_path=None):
    seen = set()
    excl = os.path.normcase(os.path.abspath(exclude_path)) if exclude_path else None
    for f in glob.glob(os.path.join(ROOT, "kor_wave*_exprs.json")) + \
             glob.glob(os.path.join(ROOT, "candidates", "*.json")):
        if excl and os.path.normcase(os.path.abspath(f)) == excl:
            continue  # 输入文件自身不算历史
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        ex = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
        for e in ex:
            if isinstance(e, str):
                seen.add(norm(e))
    return seen


def near_fields():
    """reviews/*.json near 池 + 台账 near_pool 的字段集合（增强优先）。"""
    flds = set()
    for f in glob.glob(os.path.join(ROOT, "reviews", "*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for r in d.get("near", []):
            for tok in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", r.get("code", "")):
                if len(tok) > 6:
                    flds.add(tok)
    return flds


def expr_fields(e):
    return {t for t in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", e) if len(t) > 6}


def load_quota_config():
    """加载多维配额配置。"""
    quota_path = os.path.join(TOOLS_DIR, "skeleton_quota.json")
    if os.path.exists(quota_path):
        with open(quota_path, encoding="utf-8") as f:
            return json.load(f)
    return None


def select_with_multidim(exprs, size, field_profiles=None, quota_config=None, max_field_repeat=3):
    """多维标签选波（经济学构造链感知）。

    Args:
        exprs: 候选表达式列表
        size: 目标选波大小
        field_profiles: 字段画像 {field_id: {shape, coverage, ...}}
        quota_config: 配额配置（默认从 skeleton_quota.json 加载）
        max_field_repeat: 单字段最大重复次数

    Returns:
        picked: 选中的表达式列表
        meta: 选波元数据
    """
    # 提取标签
    tags_list = batch_extract_tags(exprs, field_profiles)

    # 加载配额配置
    if quota_config is None:
        quota_config = load_quota_config()
    if quota_config is None:
        quota_config = DEFAULT_QUOTA

    # 按机制族分桶
    mechanism_buckets = collections.defaultdict(list)
    for i, tags in enumerate(tags_list):
        mechanism_buckets[tags['mechanism']].append((i, tags))

    # 按结构分桶
    structure_buckets = collections.defaultdict(list)
    for i, tags in enumerate(tags_list):
        structure_buckets[tags['structure']].append((i, tags))

    # 轮转抽样：优先满足机制多样性
    picked = []
    picked_indices = set()
    picked_tags = []
    field_count = collections.Counter()

    # 第一轮：按机制配额抽样
    mechanism_quota = quota_config.get('dimensions', {}).get('mechanism', {})
    for mechanism, conf in mechanism_quota.items():
        cap = conf.get('cap', 0.05)
        bucket = mechanism_buckets.get(mechanism, [])
        target = max(1, int(size * cap))
        for i, tags in bucket[:target]:
            if len(picked) >= size:
                break
            if i not in picked_indices:
                # 字段重复检查
                fields = tags.get('fields', [])
                if sum(1 for f in fields if field_count[f] >= max_field_repeat) > 0:
                    continue
                picked.append(exprs[i])
                picked_indices.add(i)
                picked_tags.append(tags)
                for f in fields:
                    field_count[f] += 1

    # 第二轮：填充剩余配额（按结构多样性）
    remaining = size - len(picked)
    if remaining > 0:
        structure_quota = quota_config.get('dimensions', {}).get('structure', {})
        for structure, conf in sorted(structure_quota.items(),
                                      key=lambda x: -x[1].get('cap', 0)):
            bucket = structure_buckets.get(structure, [])
            for i, tags in bucket:
                if len(picked) >= size:
                    break
                if i not in picked_indices:
                    # 字段重复检查
                    fields = tags.get('fields', [])
                    if sum(1 for f in fields if field_count[f] >= max_field_repeat) > 0:
                        continue
                    picked.append(exprs[i])
                    picked_indices.add(i)
                    picked_tags.append(tags)
                    for f in fields:
                        field_count[f] += 1

    # 汇总标签统计
    summary = summarize_tags(picked_tags)

    # 配额校验
    violations = []
    for dim, quotas in quota_config.get('dimensions', {}).items():
        actual = summary.get(f'{dim}_share', {})
        for tag, conf in quotas.items():
            cap = conf.get('cap', 1.0)
            if actual.get(tag, 0) > cap:
                violations.append(f"{dim}.{tag} 超配 {actual[tag]:.0%} > {cap:.0%}")

    meta = {
        'multidim': True,
        'summary': summary,
        'quota_violations': violations,
        'quota_passed': not violations,
    }

    return picked, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--wave", required=True)
    ap.add_argument("--size", type=int, default=48)
    ap.add_argument("--max-field-repeat", type=int, default=3)
    ap.add_argument("--legacy", action="store_true",
                    help="传统选波模式（已废弃，仅用于对比）")
    ap.add_argument("--field-profiles", help="字段画像 JSON 文件路径（可选）")
    a = ap.parse_args()

    # 加载候选表达式
    d = json.load(open(a.file, encoding="utf-8"))
    exprs = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
    exprs = [e for e in exprs if isinstance(e, str)]

    # 全历史去重
    hist = history_hashes(exclude_path=a.file)
    deduped = [e for e in exprs if norm(e) not in hist]
    n_dup = len(exprs) - len(deduped)

    # near-miss 加权
    nf = near_fields()
    deduped.sort(key=lambda e: 0 if expr_fields(e) & nf else 1)

    # 加载字段画像（如果提供）
    field_profiles = None
    if a.field_profiles and os.path.exists(a.field_profiles):
        with open(a.field_profiles, encoding="utf-8") as f:
            field_profiles = json.load(f)

    # 选波（默认多维模式）
    if a.legacy:
        print("[warn] 传统选波模式已废弃，仅用于对比")
        # 传统模式：加载旧配额
        cons_path = os.path.join(ROOT, "reference", "kor_generation_constraints.json")
        quota = {"linear_mix": 0.5}
        if os.path.exists(cons_path):
            quota = json.load(open(cons_path, encoding="utf-8"))["injection_rules"]["skeleton_quota"]
            quota = {k.split("(")[0]: v for k, v in quota.items()}
        lm_cap = quota.get("linear_mix", 0.5)

        # 传统选波逻辑（简化版）
        def skeleton(expr):
            if "trade_when(" in expr or "if_else(" in expr:
                return "event_gated"
            if "group_" in expr:
                return "group"
            if "divide(" in expr:
                return "ratio"
            if "add(" in expr or "multiply(" in expr:
                return "linear_mix"
            return "single"

        buckets = collections.defaultdict(list)
        for e in deduped:
            buckets[skeleton(e)].append(e)

        picked, lm_count = [], 0
        for sk in ['event_gated', 'group', 'ratio', 'single', 'linear_mix']:
            bucket = buckets.get(sk, [])
            for e in bucket:
                if len(picked) >= a.size:
                    break
                if sk == "linear_mix" and lm_count >= max(1, int(a.size * lm_cap)):
                    continue
                picked.append(e)
                if sk == "linear_mix":
                    lm_count += 1

        sk_dist = collections.Counter(skeleton(e) for e in picked)
        meta = {
            'multidim': False,
            'skeleton_distribution': dict(sk_dist),
            'linear_mix_cap': lm_cap,
        }
    else:
        # 多维选波（默认）
        picked, meta = select_with_multidim(deduped, a.size, field_profiles, max_field_repeat=a.max_field_repeat)

    # 输出
    meta.update({
        "wave": a.wave, "source": a.file,
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "input": len(exprs), "duplicates_dropped": n_dup, "selected": len(picked),
    })

    out = os.path.join(ROOT, "candidates", f"kor_wave{a.wave}_exprs.json")
    payload = {"meta": meta, "expressions": picked}
    tmp = out + ".tmp"
    json.dump(payload, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, out)
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    print(f"wave -> {out}")


if __name__ == "__main__":
    main()
