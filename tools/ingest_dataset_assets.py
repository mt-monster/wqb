# -*- coding: utf-8 -*-
"""ingest_dataset_assets.py - 把 fetch_dataset_assets.py 拉取的 JSON 批量写入 wqb.db。

直接操作 SQLite（通过 CampaignStore 连接），比 MCP 调用快 100 倍。
写入目标:
  - datasets 表: 数据集级元数据 + catalog_json
  - fields 表: 字段级明细
  - registry_empirical 表: PPA 预筛结果（layer=campaign）
"""
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from wqb.store.campaign import CampaignStore

ASSETS_DIR = "data/dataset_assets"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ingest_region(store, region):
    """入库指定 Region 的全部数据集资产。"""
    # 1. 读取数据集列表
    ds_path = os.path.join(ASSETS_DIR, f"{region}_datasets.json")
    if not os.path.exists(ds_path):
        print(f"[SKIP] {ds_path} 不存在")
        return
    
    ds_data = load_json(ds_path)
    datasets = ds_data.get("datasets", [])
    print(f"[{region}] 数据集列表: {len(datasets)} 个")
    
    conn = store.connection
    c = conn.cursor()
    now = datetime.now().isoformat(timespec="seconds")
    
    # 先获取 region_id，避免 SQL 子查询在 REPLACE 时的问题
    c.execute("SELECT id FROM regions WHERE name=?", (region,))
    region_row = c.fetchone()
    if not region_row:
        print(f"[ERROR] region {region} 不存在于 regions 表")
        return
    region_id = region_row[0]
    print(f"[{region}] region_id={region_id}")
    
    inserted_ds = 0
    inserted_fields = 0
    inserted_reg = 0
    
    for ds in datasets:
        ds_id = ds["id"]
        
        # 提取 category/subcategory 的 id（JSON 中为 dict）
        cat = ds.get("category", {})
        cat_id = cat.get("id", "") if isinstance(cat, dict) else str(cat)
        subcat = ds.get("subcategory", {})
        subcat_id = subcat.get("id", "") if isinstance(subcat, dict) else str(subcat)
        
        # 2. 写入 datasets 表（先查后插/更，避免 REPLACE 导致 fields 外键孤儿）
        c.execute("SELECT id FROM datasets WHERE name=? AND region_id=?", (ds_id, region_id))
        existing = c.fetchone()
        
        tier_val = "PPA_PASS" if (ds.get("coverage", 0) >= 0.6 and ds.get("alphaCount", 999) <= 200 and ds.get("fieldCount", 0) >= 10) else "STANDARD"
        catalog_json = json.dumps(ds, ensure_ascii=False)
        
        if existing:
            # UPDATE
            c.execute("""
                UPDATE datasets SET
                    category=?, field_count=?, coverage=?, alpha_count=?,
                    value_score=?, pyramid_multiplier=?, tier=?, status=?,
                    updated_at=?, data_type=?, catalog_json=?
                WHERE id=?
            """, (
                cat_id, ds.get("fieldCount", 0), ds.get("coverage", 0), ds.get("alphaCount", 0),
                ds.get("valueScore", 0), ds.get("pyramidMultiplier", 1.0), tier_val, "ACTIVE",
                now, "MATRIX", catalog_json, existing[0]
            ))
            dataset_db_id = existing[0]
        else:
            # INSERT
            c.execute("""
                INSERT INTO datasets 
                (name, region_id, category, field_count, coverage, alpha_count, 
                 value_score, pyramid_multiplier, tier, status, created_at, updated_at, data_type, catalog_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ds_id, region_id, cat_id,
                ds.get("fieldCount", 0), ds.get("coverage", 0), ds.get("alphaCount", 0),
                ds.get("valueScore", 0), ds.get("pyramidMultiplier", 1.0), tier_val, "ACTIVE",
                now, now, "MATRIX", catalog_json
            ))
            dataset_db_id = c.lastrowid
        inserted_ds += 1
        
        # 3. 写入 registry_empirical（PPA 预筛结果）
        ppa_pass = ds.get("coverage", 0) >= 0.6 and ds.get("alphaCount", 999) <= 200 and ds.get("fieldCount", 0) >= 10
        payload = {
            "id": ds_id,
            "name": ds.get("name", ""),
            "category": cat_id,
            "subcategory": subcat_id,
            "coverage": ds.get("coverage", 0),
            "alphaCount": ds.get("alphaCount", 0),
            "fieldCount": ds.get("fieldCount", 0),
            "valueScore": ds.get("valueScore", 0),
            "pyramidMultiplier": ds.get("pyramidMultiplier", 1.0),
            "ppa_prefilter": {
                "pass": ppa_pass,
                "coverage": ds.get("coverage", 0),
                "alphaCount": ds.get("alphaCount", 0),
                "fieldCount": ds.get("fieldCount", 0),
                "valueScore": ds.get("valueScore", 0),
                "pyramidMultiplier": ds.get("pyramidMultiplier", 1.0),
            },
            "source": "fetch_dataset_assets",
            "fetched_at": ds_data.get("fetched_at", now),
        }
        c.execute("""
            INSERT OR REPLACE INTO registry_empirical
            (region, layer, entry_id, family, payload, dead_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            region, "campaign", ds_id, cat_id,
            json.dumps(payload, ensure_ascii=False),
            None, now, now
        ))
        inserted_reg += 1
        
        # 4. 读取字段文件并写入 fields 表
        field_path = os.path.join(ASSETS_DIR, f"{region}_{ds_id}_fields.json")
        if os.path.exists(field_path):
            field_data = load_json(field_path)
            fields = field_data.get("fields", [])
            
            # 更新 datasets 表的 data_type（从字段推断）
            if fields:
                type_counts = {}
                for f in fields:
                    t = f.get("type", "UNKNOWN")
                    type_counts[t] = type_counts.get(t, 0) + 1
                main_type = max(type_counts, key=type_counts.get) if type_counts else "MATRIX"
                c.execute("UPDATE datasets SET data_type=? WHERE id=?", (main_type, dataset_db_id))
            
            for f in fields:
                # 先查后插/更 fields
                c.execute("SELECT id FROM fields WHERE dataset_id=? AND field_name=?", (dataset_db_id, f.get("id", "")))
                existing_field = c.fetchone()
                if existing_field:
                    c.execute("""
                        UPDATE fields SET
                            field_type=?, coverage=?, user_count=?, alpha_count=?,
                            description=?, field_group=?
                        WHERE id=?
                    """, (
                        f.get("type", "UNKNOWN"), f.get("coverage", 0),
                        f.get("userCount", 0), f.get("alphaCount", 0),
                        (f.get("description") or "")[:500], f.get("group", ""),
                        existing_field[0]
                    ))
                else:
                    c.execute("""
                        INSERT INTO fields
                        (dataset_id, field_name, field_type, coverage, user_count, alpha_count, description, field_group, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        dataset_db_id, f.get("id", ""),
                        f.get("type", "UNKNOWN"), f.get("coverage", 0),
                        f.get("userCount", 0), f.get("alphaCount", 0),
                        (f.get("description") or "")[:500], f.get("group", ""), now
                    ))
                inserted_fields += 1
    
    conn.commit()
    print(f"[{region}] 入库完成: datasets={inserted_ds}, registry={inserted_reg}, fields={inserted_fields}")


def main():
    store = CampaignStore("data/wqb.db")
    print(f"数据库连接: {store.path}")
    
    # 处理 USA + MEA（其他 Region 后续按需添加）
    ingest_region(store, "USA")
    ingest_region(store, "MEA")
    
    store.close()
    print("全部完成")


if __name__ == "__main__":
    main()
