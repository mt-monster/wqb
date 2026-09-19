# Region Universe 配置对比与更新报告

> 数据来源：平台 get_platform_setting_options（2026-09-11 实时）
> 对比对象：src/wqb/config.py + tracking/region_config.json

---

## 一、平台最新 Universe 配置（权威源）

| Region | Delay | 可用 Universe | 默认 Universe |
|--------|-------|--------------|---------------|
| **USA** | 0, 1 | TOP3000, TOP2000, TOP1000, TOP500, TOP200, ILLIQUID_MINVOL1M, TOPSP500 | TOP3000 |
| **GLB** | 1 | TOP3000, MINVOL1M, MINVOL10M, TOPDIV3000 | TOP3000 |
| **EUR** | 0, 1 | TOP2500, TOP1200, TOP800, TOP400, ILLIQUID_MINVOL1M, TOPCS1600 | TOP2500 |
| **ASI** | 1 | MINVOL1M, MINVOL10M, ILLIQUID_MINVOL1M, TOP500 | MINVOL1M |
| **CHN** | 0, 1 | TOP2000U | TOP2000U |
| **KOR** | 1 | TOP600 | TOP600 |
| **HKG** | 1 | TOP800, TOP500 | TOP800 |
| **IND** | 1 | TOP500 | TOP500 |
| **DEU** | 0, 1 | TOP500 | TOP500 |
| **GBR** | 0, 1 | TOP700 | TOP700 |
| **ALL** | 1 | LARGE, MEDIUM, SMALL | - |

---

## 二、项目配置对比

### 2.1 src/wqb/config.py 差异

| Region | 项目配置 | 平台最新 | 差异 | 状态 |
|--------|---------|---------|------|------|
| **USA** | TOP3000, TOP2000, TOP1000, TOP500, TOP200 | + ILLIQUID_MINVOL1M, TOPSP500 | ⚠️ 缺少 2 个 | 需更新 |
| **EUR** | TOP2500, TOPCS1600, TOP1200, TOP800, TOP400, ILLIQUID_MINVOL1M | 一致 | ✅ 匹配 | 无需更新 |
| **CHN** | TOP2000U, TOP1000, TOP500 | 仅 TOP2000U | ⚠️ 多余 2 个 | 需更新 |
| **ASI** | TOP2000, TOP1000, TOP500 | MINVOL1M, MINVOL10M, ILLIQUID_MINVOL1M, TOP500 | ❌ 完全不符 | 需更新 |
| **GLB** | MINVOL10M, TOPDIV3000, TOP3000, TOP2000 | TOP3000, MINVOL1M, MINVOL10M, TOPDIV3000 | ⚠️ 缺少 MINVOL1M，多余 TOP2000 | 需更新 |
| **KOR** | TOP3000, TOP1000, TOP500 | 仅 TOP600 | ❌ 完全不符 | 需更新 |
| **GBR** | TOP700, TOP350 | 仅 TOP700 | ⚠️ 多余 TOP350 | 需更新 |
| **DEU** | TOP500, TOP300 | 仅 TOP500 | ⚠️ 多余 TOP300 | 需更新 |
| **IND** | TOP500, TOP300 | 仅 TOP500 | ⚠️ 多余 TOP300 | 需更新 |
| **HKG** | TOP800, TOP500 | 一致 | ✅ 匹配 | 无需更新 |
| **MEA** | TOP400, TOP200 | 平台无 MEA | ⚠️ 平台未列出 | 需确认 |
| **JPN** | TOP2000, TOP1000, TOP500 | 平台无 JPN | ⚠️ 平台未列出 | 需确认 |
| **AMR** | TOP2000, TOP1000, TOP500 | 平台无 AMR | ⚠️ 平台未列出 | 需确认 |
| **TWN** | TOP1000, TOP500 | 平台无 TWN | ⚠️ 平台未列出 | 需确认 |

### 2.2 tracking/region_config.json 差异

| Region | 项目配置 | 平台最新 | 差异 | 状态 |
|--------|---------|---------|------|------|
| **GBR** | TOP700, TOP1000 | 仅 TOP700 | ⚠️ 多余 TOP1000 | 需更新 |
| **USA** | TOP3000, TOP1000, TOP500 | + TOP2000, TOP200, ILLIQUID_MINVOL1M, TOPSP500 | ⚠️ 缺少 4 个 | 需更新 |
| **KOR** | TOP600 | 一致 | ✅ 匹配 | 无需更新 |
| **MEA** | TOP400, TOP300 | 平台无 MEA | ⚠️ 平台未列出 | 需确认 |

---

## 三、需要更新的配置

### 3.1 src/wqb/config.py 更新

```python
REGIONS: Dict[str, dict] = {
    "USA": {
        "universes": ["TOP3000", "TOP2000", "TOP1000", "TOP500", "TOP200",
                      "ILLIQUID_MINVOL1M", "TOPSP500"],  # 新增 2 个
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP3000",
    },
    "EUR": {
        "universes": ["TOP2500", "TOPCS1600", "TOP1200", "TOP800", "TOP400",
                      "ILLIQUID_MINVOL1M"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP2500",
    },
    "CHN": {
        "universes": ["TOP2000U"],  # 移除 TOP1000, TOP500
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP2000U",
    },
    "ASI": {
        "universes": ["MINVOL1M", "MINVOL10M", "ILLIQUID_MINVOL1M", "TOP500"],  # 完全更新
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1],  # 仅 D1
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "MINVOL1M",  # 更新默认
    },
    "GLB": {
        "universes": ["TOP3000", "MINVOL1M", "MINVOL10M", "TOPDIV3000"],  # 新增 MINVOL1M，移除 TOP2000
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1],  # 仅 D1
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP3000",
    },
    "KOR": {
        "universes": ["TOP600"],  # 完全更新
        "neutralizations": ["SECTOR"] + [n for n in _USA_NEUTRALIZATIONS if n != "SECTOR"],
        "delays": [1],  # 仅 D1
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP600",
    },
    "GBR": {
        "universes": ["TOP700"],  # 移除 TOP350
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [0, 1],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP700",
    },
    "DEU": {
        "universes": ["TOP500"],  # 移除 TOP300
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP500",
    },
    "IND": {
        "universes": ["TOP500"],  # 移除 TOP300
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1],  # 仅 D1
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP500",
    },
    "HKG": {
        "universes": ["TOP800", "TOP500"],
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1],  # 仅 D1
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP800",
    },
    # 以下区域平台未列出，保留但标注需确认
    "MEA": {
        "universes": ["TOP400", "TOP200"],  # 平台未列出，需确认
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP400",
        "_note": "平台 get_platform_setting_options 未列出，需确认是否仍可用",
    },
    "JPN": {
        "universes": ["TOP2000", "TOP1000", "TOP500"],  # 平台未列出，需确认
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP2000",
        "_note": "平台 get_platform_setting_options 未列出，需确认是否仍可用",
    },
    "AMR": {
        "universes": ["TOP2000", "TOP1000", "TOP500"],  # 平台未列出，需确认
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP2000",
        "_note": "平台 get_platform_setting_options 未列出，需确认是否仍可用",
    },
    "TWN": {
        "universes": ["TOP1000", "TOP500"],  # 平台未列出，需确认
        "neutralizations": list(_USA_NEUTRALIZATIONS),
        "delays": [1, 0],
        "categories": list(PLATFORM_CATEGORIES),
        "default_universe": "TOP1000",
        "_note": "平台 get_platform_setting_options 未列出，需确认是否仍可用",
    },
}
```

### 3.2 tracking/region_config.json 更新

```json
{
  "GBR": {
    "universe": ["TOP700"],
    "neutralization": ["SUBINDUSTRY", "SECTOR"],
    "strong_datasets": ["starmine"],
    "weak_datasets": ["model264", "model36", "other455"],
    "field_rules": {
      "model264": "mdl264_ 前缀 + _l1 分层",
      "model36": "star_sr_ 前缀 + _d1 分层"
    },
    "window_adaptive": {
      "news_abno_vol": 10,
      "ep_yield_pct_smest": 30
    },
    "probe_size": 3,
    "settings_priority": [
      {"universe": "TOP700", "neutralization": "SUBINDUSTRY"},
      {"universe": "TOP700", "neutralization": "SECTOR"}
    ]
  },
  "USA": {
    "universe": ["TOP3000", "TOP2000", "TOP1000", "TOP500", "TOP200",
                 "ILLIQUID_MINVOL1M", "TOPSP500"],
    "neutralization": ["SUBINDUSTRY", "SECTOR", "MARKET"],
    "strong_datasets": ["starmine"],
    "weak_datasets": ["ml_factor_proj"],
    "field_groups": {
      "ml_factor_proj": ["attention_*", "change_*", "基础指标"],
      "starmine": ["ep_yield_pct_smest_*"]
    },
    "combo_signal": [
      "ts_zscore(ep_yield_pct_smest_fy1_3, 20) + ts_zscore(ep_yield_pct_smest_fy2_3, 20)"
    ],
    "probe_size": 4,
    "settings_priority": [
      {"universe": "TOP3000", "neutralization": "SUBINDUSTRY"},
      {"universe": "TOP2000", "neutralization": "SUBINDUSTRY"},
      {"universe": "TOP1000", "neutralization": "SUBINDUSTRY"},
      {"universe": "TOP3000", "neutralization": "SECTOR"},
      {"universe": "TOP3000", "neutralization": "MARKET"},
      {"universe": "TOP500", "neutralization": "SUBINDUSTRY"}
    ]
  },
  "KOR": {
    "universe": ["TOP600"],
    "neutralization": ["SECTOR"],
    "strong_datasets": ["insider_feats"],
    "weak_datasets": [],
    "prod_wall": {
      "insider_feats": 0.78,
      "DL": "0.84-0.92"
    },
    "structure_rebuild": true,
    "probe_size": 3,
    "settings_priority": [
      {"universe": "TOP600", "neutralization": "SECTOR"}
    ]
  },
  "MEA": {
    "universe": ["TOP400", "TOP300"],
    "neutralization": ["SUBINDUSTRY", "SECTOR", "INDUSTRY", "MARKET", "COUNTRY"],
    "strong_datasets": [],
    "weak_datasets": [],
    "probe_size": 3,
    "settings_priority": [
      {"universe": "TOP400", "neutralization": "SUBINDUSTRY"},
      {"universe": "TOP400", "neutralization": "SECTOR"},
      {"universe": "TOP300", "neutralization": "SUBINDUSTRY"},
      {"universe": "TOP400", "neutralization": "MARKET"},
      {"universe": "TOP400", "neutralization": "COUNTRY"}
    ],
    "_note": "平台 get_platform_setting_options 未列出 MEA，需确认是否仍可用"
  }
}
```

---

## 四、关键变更总结

| 变更类型 | Region | 变更内容 |
|---------|--------|---------|
| **新增 Universe** | USA | + ILLIQUID_MINVOL1M, TOPSP500 |
| **移除 Universe** | CHN | - TOP1000, TOP500 |
| **完全更新** | ASI | 从 TOP2000/1000/500 → MINVOL1M/MINVOL10M/ILLIQUID_MINVOL1M/TOP500 |
| **完全更新** | KOR | 从 TOP3000/1000/500 → 仅 TOP600 |
| **新增 Universe** | GLB | + MINVOL1M |
| **移除 Universe** | GLB | - TOP2000 |
| **移除 Universe** | GBR | - TOP350, TOP1000 |
| **移除 Universe** | DEU | - TOP300 |
| **移除 Universe** | IND | - TOP300 |
| **Delay 更新** | ASI, GLB, KOR, IND, HKG | 仅 D1（移除 D0） |
| **需确认** | MEA, JPN, AMR, TWN | 平台未列出，需确认是否仍可用 |

---

## 五、建议操作

1. **立即更新**：src/wqb/config.py 和 tracking/region_config.json
2. **验证可用性**：对 MEA/JPN/AMR/TWN 区域进行平台实测确认
3. **更新文档**：同步更新相关战役文档中的 universe 引用
4. **通知团队**：告知 KOR/ASI 区域 universe 完全变更

---

*报告生成时间：2026-09-11*
