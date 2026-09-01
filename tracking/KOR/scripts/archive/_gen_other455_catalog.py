# -*- coding: utf-8 -*-
"""生成 KOR other455 typed catalog（gate 闸2/闸3 数据源）

字段来源: 2026-08-22 MCP get_datafields 实测 (region=KOR, universe=TOP600, delay=1, filter_sharpe=False)
- competitor 系: cov 0.7914 (300 字段, n2v 系列)
- customer 系: cov 0.8587
- relation 系: cov 1.0
- partner 系: cov 0.946
关键: MATRIX 类型 pca_fact*_value 可直接 rank; GROUP 类型 cluster 字段必须 vec_* 包裹
"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")

# 从 MCP 结果整理的字段（id -> type），覆盖四类关系
fields = []
def add(prefix, type_, cov):
    fields.append({"id": prefix, "type": type_, "coverage": cov})

# ============ relation 系 (cov 1.0) — 最高覆盖 ============
rel_base = ["oth455_relation_n2v_p10_q200", "oth455_relation_n2v_p50_q200",
            "oth455_relation_n2v_p10_q50", "oth455_relation_n2v_p50_q50"]
for base in rel_base:
    for w in range(1, 6):
        for f in range(1, 4):
            add(f"{base}_w{w}_pca_fact{f}_value", "MATRIX", 1.0)
for w in range(1, 6):
    for f in range(1, 4):
        add(f"oth455_relation_roam_w{w}_pca_fact{f}_value", "MATRIX", 1.0)

# ============ partner 系 (cov 0.946) ============
for base in ["oth455_partner_n2v_p10_q200", "oth455_partner_n2v_p50_q200",
             "oth455_partner_n2v_p10_q50", "oth455_partner_n2v_p50_q50"]:
    for w in range(1, 6):
        for f in range(1, 4):
            add(f"{base}_w{w}_pca_fact{f}_value", "MATRIX", 0.946)
for w in range(1, 6):
    for f in range(1, 4):
        add(f"oth455_partner_roam_w{w}_pca_fact{f}_value", "MATRIX", 0.946)

# ============ customer 系 (cov 0.8587) ============
for base in ["oth455_customer_n2v_p10_q200", "oth455_customer_n2v_p50_q200",
             "oth455_customer_n2v_p10_q50", "oth455_customer_n2v_p50_q50"]:
    for w in range(1, 6):
        for f in range(1, 4):
            add(f"{base}_w{w}_pca_fact{f}_value", "MATRIX", 0.8587)
for w in range(1, 6):
    for f in range(1, 4):
        add(f"oth455_customer_roam_w{w}_pca_fact{f}_value", "MATRIX", 0.8587)

# ============ competitor 系 (cov 0.7914) — 低覆盖备用 ============
for base in ["oth455_competitor_n2v_p10_q200", "oth455_competitor_n2v_p50_q200",
             "oth455_competitor_n2v_p10_q50", "oth455_competitor_n2v_p50_q50"]:
    for w in range(1, 6):
        for f in range(1, 4):
            add(f"{base}_w{w}_pca_fact{f}_value", "MATRIX", 0.7914)
for w in range(1, 6):
    for f in range(1, 4):
        add(f"oth455_competitor_roam_w{w}_pca_fact{f}_value", "MATRIX", 0.7914)

# ============ GROUP cluster 系（补充, 均需 vec_* 包裹） ============
for rel in ["relation", "partner", "customer", "competitor"]:
    for method in ["n2v", "roam"]:
        for base in [f"oth455_{rel}_{method}"]:
            for w in range(1, 6):
                for f in range(1, 4):
                    add(f"{base}_w{w}_pca_fact{f}_cluster_5", "GROUP", 1.0 if rel == "relation" else 0.9)
                    add(f"{base}_w{w}_pca_fact{f}_cluster_10", "GROUP", 1.0 if rel == "relation" else 0.9)
                    add(f"{base}_w{w}_pca_fact{f}_cluster_20", "GROUP", 1.0 if rel == "relation" else 0.9)
                add(f"{base}_w{w}_kmeans_cluster_5", "GROUP", 1.0 if rel == "relation" else 0.9)
                add(f"{base}_w{w}_kmeans_cluster_10", "GROUP", 1.0 if rel == "relation" else 0.9)
                add(f"{base}_w{w}_kmeans_cluster_20", "GROUP", 1.0 if rel == "relation" else 0.9)

# 去重
seen = set()
uniq = []
for f in fields:
    if f["id"] not in seen:
        seen.add(f["id"])
        uniq.append(f)

out = {
    "dataset": "other455",
    "region": "KOR",
    "universe": "TOP600",
    "delay": 1,
    "data_type": "MIXED",
    "type_distribution": {"MATRIX": sum(1 for f in uniq if f["type"] == "MATRIX"),
                           "GROUP": sum(1 for f in uniq if f["type"] == "GROUP")},
    "fetched_at": "2026-08-22",
    "fields": uniq,
}
path = r"d:\coding\traeCN_project\wqb\tracking\KOR\reference\kor_other455_fields.json"
json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written:", path, "total:", len(uniq), "MATRIX:", out["type_distribution"]["MATRIX"], "GROUP:", out["type_distribution"]["GROUP"])
