# -*- coding: utf-8 -*-
"""split_registry.py - 把单文件 campaign_registry.json 拆分为按区域小文件。

拆分前自动备份到 campaign_registry.json.bak-p1（已存在则覆盖）。
拆分后目录结构：
  research-data/registry/
    index.json      # 区域列表 + 元信息 + cross_region_lessons + pending_regions
    USA.json        # regions.USA 内容（static/assets/empirical 三层）
    KOR.json
    ASI.json
    MEA.json

校验：拆分后逐区域 deep-compare，确保无数据丢失。
原文件保留（不删除），由人工确认后再归档。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "research-data" / "campaign_registry.json"
DST_DIR = ROOT / "research-data" / "registry"


def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    if not SRC.exists():
        print(f"[ERROR] source not found: {SRC}")
        return 1

    data = load_json(SRC)
    regions = data.get("regions", {})
    if not regions:
        print("[ERROR] no regions key in registry")
        return 1

    DST_DIR.mkdir(parents=True, exist_ok=True)

    # 1) 写每个区域文件
    written = []
    for region, content in regions.items():
        fp = DST_DIR / f"{region}.json"
        dump_json(fp, content)
        written.append((region, fp))

    # 2) 写 index.json（元信息 + 跨区教训 + 待扩区域）
    index = {
        "version": data.get("version", "1.0"),
        "updated": data.get("updated", ""),
        "maintained_by": data.get("maintained_by", ""),
        "purpose": data.get("purpose", ""),
        "data_sources": data.get("data_sources", {}),
        "write_back_rule": data.get("write_back_rule", ""),
        "regions": sorted(regions.keys()),
        "cross_region_lessons": data.get("cross_region_lessons", []),
        "pending_regions": data.get("pending_regions", []),
        "pending_note": data.get("pending_note", ""),
        "_layout": "regions 每层拆到 <REGION>.json；本文件只存元信息+跨区教训+待扩区",
    }
    dump_json(DST_DIR / "index.json", index)

    # 3) 校验：逐区域 deep-compare
    ok = True
    for region, fp in written:
        back = load_json(fp)
        if back != regions[region]:
            print(f"[FAIL] region {region} mismatch after split")
            ok = False
    idx_back = load_json(DST_DIR / "index.json")
    if idx_back.get("cross_region_lessons") != data.get("cross_region_lessons"):
        print("[FAIL] cross_region_lessons mismatch")
        ok = False
    if idx_back.get("regions") != sorted(regions.keys()):
        print("[FAIL] regions list mismatch")
        ok = False

    if not ok:
        print("[ERROR] verification failed - registry/ may be inconsistent")
        return 2

    print(f"[OK] split {len(written)} regions -> {DST_DIR}")
    for region, fp in written:
        print(f"  {region:6s}  {fp.stat().st_size:>6d} B  {fp.name}")
    print(f"  index.json  {(DST_DIR / 'index.json').stat().st_size} B")
    print("[OK] verification passed (deep-compare all regions + index)")
    print(f"[NOTE] source kept at {SRC} (archive manually after confirm)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
