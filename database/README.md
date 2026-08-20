# WQB 数据库模块

本模块提供数据库存储和访问功能，用于替代现有的 JSON/CSV 文件存储。

> **单轨数据库模式**（2026-08-21 起）：历史 JSON 文件（`campaign_registry.json` / `registry/` 拆分目录 / `*_campaign_state.json` / `wave*_results.json`）已全部迁入 SQLite 并归档到 `attic/json_archive/`。唯一事实源为 `data/wqb.db`，不再维护 JSON 副本。

## 功能特性

- **数据库存储**：使用 SQLite 存储所有挖掘数据
- **数据访问层（DAO）**：提供高级数据操作接口
- **数据迁移**：从现有 JSON/CSV 文件迁移数据（`migrate.py` / `full_migrate.py` / `tools/migrate_phase2.py`）
- **集成接口**：与现有流程兼容的数据库操作接口
- **事务支持**：保证数据操作的原子性
- **关联查询**：支持复杂的数据关联分析

## 数据库架构

### 核心表（Phase 1，14 张）

1. **regions** - 区域配置
2. **datasets** - 数据集信息
3. **fields** - 字段信息
4. **alphas** - Alpha 记录
5. **waves** - 波次信息
6. **expressions** - 表达式记录
7. **diversity_potential** - 多样性潜力报告
8. **campaign_state** - 战役状态

### Phase 2 增量表（4 张）

9. **cross_region_lessons** - 跨区域铁律（GLB emotion 死路 / anl15 封禁 / 非法 universe 档）
10. **registry_empirical** - registry 实证层（dead_end / win / orphan / campaign 四层，按区域）
11. **wave_results** - wave 台账摘要（key_findings / candidates / batches / verdict / status / archived）
12. **ledger_kv** - LedgerStore 的 SQLite 后端（通用 kv，替代 `<region>_d1_campaign_state.json`）

### 关系图

```
regions (1) ----< (N) datasets
datasets (1) ----< (N) fields
datasets (1) ----< (N) alphas
regions (1) ----< (N) waves
waves (1) ----< (N) expressions
regions (1) ----< (N) diversity_potential
regions (1) ----< (1) campaign_state
```

## 使用方法

### 1. 初始化数据库

```python
from database import init_wqb_database

# 初始化数据库并迁移现有数据
db_manager = init_wqb_database(
    workspace_root="D:\\coding\\traeCN_project\\wqb",
    db_path="data/wqb.db",
    migrate_data=True
)
```

### 2. 使用 DAO 操作数据

```python
from database import get_region_dao, get_dataset_dao, get_alpha_dao

# 获取区域
region_dao = get_region_dao()
region = region_dao.get_by_name("MEA")

# 获取数据集
dataset_dao = get_dataset_dao()
datasets = dataset_dao.get_by_region(region['id'])

# 获取可提交的 alpha
alpha_dao = get_alpha_dao()
submit_ready = alpha_dao.get_submit_ready(region['id'])
```

### 3. 使用集成接口

```python
from database import (
    save_diversity_potential, load_diversity_potential,
    save_wave_expressions, load_wave_expressions,
    save_alpha_result, get_submit_ready_alphas
)

# 保存多样性潜力报告
save_diversity_potential("MEA", "model31", {
    'diversity_score': 0.875,
    'recommended_rounds': 5,
    'field_categories': {...},
    'operator_buckets': {...},
    'parameter_space': {...}
})

# 加载多样性潜力报告
potential = load_diversity_potential("MEA", "model31")

# 保存 wave 表达式
expressions = [
    {
        'expression': 'rank(ts_zscore(mdl31_roe_pct_t4q, 120))',
        'fingerprint': 'abc123',
        'status': 'completed',
        'alpha_id': 'A1lZ08Al',
        'sharpe': 1.39,
        'fitness': 0.96,
        'margin': 9.47,
        'turnover': 23.58
    }
]
save_wave_expressions("MEA", "15C", expressions)

# 加载 wave 表达式
expressions = load_wave_expressions("MEA", "15C")

# 保存 alpha 结果
save_alpha_result(
    alpha_id="A1lZ08Al",
    region="MEA",
    dataset="model31",
    expression="rank(ts_zscore(mdl31_roe_pct_t4q, 120))",
    settings={
        'universe': 'TOP400',
        'delay': 1,
        'neutralization': 'SECTOR'
    },
    metrics={
        'sharpe': 1.39,
        'fitness': 0.96,
        'margin': 9.47,
        'turnover': 23.58,
        'status': 'UNSUBMITTED'
    }
)

# 获取可提交的 alpha
submit_ready = get_submit_ready_alphas("MEA")
```

### 4. 数据迁移

```python
from database import DataMigrator

# 创建迁移器
migrator = DataMigrator("D:\\coding\\traeCN_project\\wqb")

# 迁移所有数据
migrator.migrate_all()

# 或者迁移特定类型的数据
migrator.migrate_regions()
migrator.migrate_datasets()
migrator.migrate_fields()
migrator.migrate_alphas()
migrator.migrate_waves()
migrator.migrate_expressions()
migrator.migrate_diversity_potential()
migrator.migrate_campaign_state()
```

## 与现有流程的集成

### 替换文件操作

| 原文件操作 | 数据库操作 |
|-----------|-----------|
| `diversity_potential.json` | `save_diversity_potential()` / `load_diversity_potential()` |
| `wave<TAG>_exprs.json` | `save_wave_expressions()` / `load_wave_expressions()` |
| `*_status.csv` | `save_alpha_result()` |
| 手动筛选可提交 alpha | `get_submit_ready_alphas()` |
| 手动统计战役进度 | `get_campaign_progress()` |

### 兼容性接口

```python
from database import get_database_integration

integration = get_database_integration()

# 导出数据到 JSON（兼容性）
integration.export_to_json("MEA", "output/json")

# 从 JSON 导入数据（兼容性）
integration.import_from_json("MEA", "input/json")
```

## 优势

1. **高效查询**：支持 SQL 查询，快速检索特定数据
2. **关联分析**：可以轻松建立表之间的关联关系
3. **并发安全**：数据库提供事务和锁机制
4. **数据完整性**：支持约束、索引等保证数据质量
5. **扩展性**：可以轻松扩展以支持更大规模的数据
6. **事务支持**：保证数据操作的原子性
7. **备份恢复**：支持数据库备份和恢复

## 注意事项

1. **数据库文件**：默认存储在 `data/wqb.db`
2. **并发访问**：SQLite 支持多线程读写，但不支持多进程同时写入
3. **数据迁移**：首次使用需要运行数据迁移脚本
4. **备份**：建议定期备份数据库文件
5. **性能**：对于大量数据，建议使用索引优化查询性能

## 未来扩展

1. **PostgreSQL 支持**：可以扩展到 PostgreSQL 以支持多进程并发
2. **数据可视化**：可以集成数据可视化工具
3. **实时监控**：可以添加实时监控和告警功能
4. **API 接口**：可以提供 REST API 接口供外部系统调用
