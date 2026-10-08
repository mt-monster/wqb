# 在用表结构合理性评估（2026-08-26）

> 范围：对 `data/wqb.db` 当前 **15 张在用表**做"结构本身设计是否合理"的评审（区别于上一轮"代码↔schema 对应"审计）。
> 方法：导出全部 DDL + 索引 + 行数 → 全仓精确 SQL 引用扫描确认"在用" → 孤儿行 + 冗余列一致性 + 类型实测。

## 一、哪些表在用（按角色与强度）

全部 15 张表均被活动代码读写（精确 DML 引用 ≥2 个文件），无遗留死表。

| 角色 | 表 | 行数 | 引用强度 | 说明 |
|---|---|---|---|---|
| 核心业务 | `fields` | 45,079 | 极高(142) | 字段字典，库最大表 |
| 核心业务 | `expressions` | 5,963 | 高(56) | alpha 候选表达式 |
| 核心业务 | `alphas` | 509 | 高(46) | 已成型 alpha 主表 |
| 核心业务 | `datasets` | 530 | 高(38) | 数据集目录 |
| 核心业务 | `waves` | 280 | 中(20) | 波次追踪 |
| 核心业务 | `backtest_results` | 473 | 低(3) | 回测结果快照 |
| 配置 | `regions` | 10 | 中(15) | 区域配置（上轮已补种子） |
| 状态/账本 | `ledger_kv` | 1,131 | 中(6) | 通用 KV 账本 |
| 状态/账本 | `campaign_state` | 4 | 低(2) | 战役进度 |
| 知识沉淀 | `registry_empirical` | 535 | 中(6) | 经验注册表 |
| 知识沉淀 | `wave_results` | 282 | 中(9) | 波次复盘 |
| 知识沉淀 | `cross_region_lessons` | 10 | 低(5) | 跨区教训 |
| 知识沉淀 | `gate_results` | 151 | 低(4) | 闸门结果日志 |
| 知识沉淀 | `diversity_potential` | 3 | 低(5) | 多样性潜力 |

## 二、结构评审结论

**总体：可用，但存在 2 处真实结构性缺陷（其中 1 处已实际破坏数据）+ 若干小瑕疵。**

### 🔴 缺陷 1（已实际发生）：外键普遍缺失，参照完整性已被破坏

DDL 中**仅 `backtest_results.expression_id` 声明了 FOREIGN KEY**；其余 9 处 ID 关联（`region_id`/`dataset_id`/`wave_id`）**全部无 FK 声明**。本期已开启 `PRAGMA foreign_keys=ON`，但**无 FK 子句的连接不受约束**。实测孤儿行：

| 关联（无 FK 声明） | 孤儿行 | 占比 |
|---|---|---|
| `fields.dataset_id → datasets.id` | **17,098** | **38%** |
| `waves.dataset_id → datasets.id` | 99 | 35% |
| 其余 8 处（`expressions.wave_id`/`alphas.region_id` 等） | 0 | — |

**根因（已定位）**：`datasets.id` 当前最小值为 **13**（表被重导/reseed 过，旧 id 1–12 已不存在），而 `fields.dataset_id` 仍使用旧的 **1–196** id 空间。没有外键兜底，重导直接把 38% 的字段行变成了孤儿 → **任何"按数据集统计字段"的查询都会静默丢 38% 数据**。这是设计缺陷造成的数据破坏，不是偶发。

`PRAGMA foreign_key_check` 报告 0 违例——因为它只检查**已声明**的 FK，恰恰掩盖了这 9 处未声明关联的问题。

### 🟠 缺陷 2（已漂移）：冗余反规范化 TEXT 列

`expressions` 同时持有 `wave_id`（→waves 外键）**和** 冗余的 `region`/`wave`/`dataset` TEXT 副本；`backtest_results` 同理有 `region`/`wave`/`dataset` TEXT。这些副本本可由 `wave_id → waves → regions/datasets` 推导，属于反规范化加速查询。

实测一致性（TEXT 副本 vs ID 关联派生值）：

| 表.列 | 不一致行 | 占比 |
|---|---|---|
| `expressions.region`/`wave` | 262 | 4.4% |
| `expressions.dataset` | 257 | 4.3% |
| `backtest_results.region`/`wave` | 0 | 0% |

**`expressions` 的冗余副本已经漂移**（262 行对不上父表）——证明该反规范化模式在实际写入中**不可靠**，将来用 TEXT 副本做筛选会得到错误结果。

### 🟡 瑕疵 3：alpha_id 三处副本

`expressions.alpha_id` / `backtest_results.alpha_id` / `alphas.alpha_id` 三处各存一份。`expressions.alpha_id` 有 **6 行**在 `alphas` 中查不到（悬挂引用）；`backtest_results` 一致。

### 🟡 瑕疵 4：`DECIMAL(x,y)` 是"装饰性约束"

SQLite 无原生 DECIMAL，`DECIMAL(8,4)` 仅为 NUMERIC affinity，**不强制精度/范围**。实测 `alphas.sharpe` 存储为 `real`/`integer`、`expressions.turnover` 含 `null`。字段定义给人"受约束"的错觉，实际没有。

### 🟢 合理之处（无需改）

- **索引覆盖良好**：region/status/wave/dataset 查询路径均有索引（`idx_alphas_region`/`idx_expr_region_wave`/`idx_registry_empirical_layer` 等），未发现缺失的关键索引。
- **JSON 大字段模式合理**：`payload_json`/`catalog_json`/`settings_json`/`report_json` 等作为研究期快速演进 schema 的弹性容器，对本项目（快速试错、字段结构常变）是恰当权衡，代价是 JSON 内部不可索引/不可直接查询——可接受。
- **命名大体一致**：绝大多数表用 `created_at`/`updated_at` TIMESTAMP 约定。
- **候选键/唯一约束合理**：`alpha_id`/`lesson_id`/`entry_id` 唯一键、`UNIQUE(region_id, dataset_id)` 等设计正确。

### 🟡 瑕疵 5：区域引用口径不统一

`regions` 在部分表用 **INT `region_id`**（alphas/datasets/waves/expressions），在部分表用 **TEXT `name`**（wave_results/registry_empirical/ledger_kv/gate_results）。两套口径混用，跨表关联需额外转换，易错。

### 🟡 瑕疵 6：命名小不一致

`campaign_state` 用 `last_updated` 而非 `updated_at`；`cross_region_lessons` 用 `updated_at`。轻微。

## 三、优先级修复建议（仅评估，未执行）

| 级别 | 项 | 建议 |
|---|---|---|
| **P0** | 缺陷1 数据破坏 | 重建 `fields↔datasets` 映射：因 `fields` 无 dataset 名称列，**最稳方案**是在 `fields` 补 `dataset_name` 列，用导入源按名称回链，再重算 `dataset_id`；或整体重导 `fields` 以对齐当前 `datasets.id`。同时给 `datasets`/`waves` 加 `AUTOINCREMENT` 保护避免再次 reseed。 |
| **P0** | 缺陷1 预防 | 在 DDL 为 9 处 ID 关联补 `FOREIGN KEY` 子句（现已开 FK pragma，立即生效防未来孤儿）。 |
| **P1** | 缺陷2 冗余漂移 | 短期：代码统一改用 `wave_id` JOIN 取 region/wave/dataset，**停用 `expressions.region/wave/dataset`**；长期：删除冗余 TEXT 列。 |
| **P2** | 瑕疵3 | `expressions.alpha_id` 悬挂 6 行清理或回链。 |
| **P2** | 瑕疵4 | `DECIMAL` → `REAL`（声明即真实类型），避免误导。 |
| **P2** | 瑕疵5 | 统一区域引用为 `region_id`（INT），TEXT 表加 `region_id` 列。 |
| **P3** | 瑕疵6 | `campaign_state.last_updated` → `updated_at`。 |

## 四、一句话结论

> 表结构**骨架合理**（索引、唯一键、JSON 弹性设计都对），但**"无外键 + 冗余反规范化 TEXT 列"两个老问题已经实际咬人**：17k 字段行因 datasets 重导变成孤儿、262 行表达式副本已漂移。这两点不修，依赖"按数据集归因字段"的分析会持续丢 38% 数据。

---

## 五、P0 修复记录（2026-08-27 已执行）

**备份**：`data/wqb.db.bak.p0_20260827_003345`（27MB，改前全量，可回滚）。

### 5.1 根因确认
- `datasets` 表曾被重导/reseed（当前 `id` 最小=13），`fields.dataset_id` 仍用旧 1–196 id 空间；无 FK 兜底 → 45 个 dataset 被从目录删掉后，其字段变孤儿。
- 45 个缺失 id = `[1, 63, 64, …, 107]`（连续段），占 `fields` 38%（17,098 行）；`waves.dataset_id` 也引用同一批。
- **孤儿 dataset 名称已不可恢复**：`ledger_kv` 的 catalog 只按 dataset 名称存、不含旧 id；`data/` 被 gitignore 无历史快照；ranking JSON 用名称不用旧数字 id。

### 5.2 修复动作
1. **保留孤儿字段**（依用户"偏好可恢复、不硬删"纪律）：把 45 个缺失 dataset 以**占位行**补回 `datasets`，保留原始 id，`name=recovered_ds_<id>`、`region_id=1`(USA 哨兵)、`status=orphan_recovered`。
2. **9 处外键补入活动代码** `src/wqb/store/campaign.py` 的 `ensure_schema()`：datasets(region_id)、fields(dataset_id)、waves(region_id,dataset_id)、expressions(wave_id)、alphas(region_id,dataset_id)、diversity_potential(region_id,dataset_id)、backtest_results(expression_id，原缺失补上)。
3. **实时库重建加 FK**：SQLite 不支持 `ALTER ADD FK`，脚本 `tracking/_scratch/_db_fix_p0.py` 重建 datasets/waves/expressions/alphas/fields/diversity_potential/campaign_state 7 表并注入 FK；backtest_results 保留既有 FK。

### 5.3 校验结果
| 项 | 结果 |
|---|---|
| `foreign_key_check` 违例 | **0** |
| `fields` / `waves` 孤儿 | **0 / 0** |
| `fields` 行数（修复前后） | 45,079 / 45,079（无损） |
| `datasets` 行数 | 530 → 575（+45 占位） |
| `recovered_ds_*` 占位 | 45 行，标记 `orphan_recovered` |
| WAL 模式 | 仍在（`wal`） |
| `campaign.py` 语法 | OK |

### 5.4 遗留（未决）
- **45 个 `recovered_ds_*` 占位 dataset**：region 标 USA 哨兵、元数据缺失，待用户决定——补全真实元数据，或 purge 占位 + 其字段。
- **`campaign_state` 等 4 表的 DDL 仍只在归档 `attic/db_layer_archive/`**（P0 单源问题，用户此前 defer，未解）；其 FK 仅加在实时库。
- **缺陷 2（冗余 TEXT 列漂移）本轮未修**：`expressions.region/wave/dataset` 262 行仍与父表不一致，建议下轮停用冗余列、统一走 `wave_id` JOIN。

---

## 六、修复全部问题（2026-08-27 第二轮）

用户要求"修复全部问题"，本轮清零全部遗留 open 项（P0 单源 + 缺陷 2/3/5/6；缺陷 4 因纯 cosmetic 且重建有风险而 defer）。

**备份**：`data/wqb.db.bak.all_20260827_003853`。

### 6.1 P0 单源（代码层）
- 把 `wave_results`/`registry_empirical`/`cross_region_lessons`/`campaign_state` 4 张 MCP 表 DDL 并入 `src/wqb/store/campaign.py` 的 `ensure_schema()`。活动代码现成为 **14 张表的唯一事实源**；删库重 bootstrap 不再缺表（原 P0 隐患根除）。

### 6.2 缺陷 2（冗余 TEXT 列漂移）
- **根因**：`upsert_expressions` 写入 `region`/`wave`/`dataset` 取自函数参数而非 `wave_id` 关联，参数与父表不一致即漂移。
- **写入端修复**：改为从 `wave_id → waves → regions/datasets` 关联派生，杜绝再漂移。
- **存量同步**：5971 行 `expressions` + 473 行 `backtest_results` 全部重新同步到真值，漂移 **262 → 0**。
- **未删列**：这些列被 `list_expressions(region, wave, dataset=...)` 等海量工具当作过滤条件，删列会破坏调用，故保留列 + 同步（而非删）。

### 6.3 缺陷 3 / 5 / 6
- **缺陷 3**：6 行悬挂 `expressions.alpha_id` 清 `NULL`。
- **缺陷 5**：`wave_results`/`registry_empirical` 加 `region_id` 列并按 `regions.name` 填充（0 NULL），统一 region 引用口径（TEXT 名 + INT id 双键）。
- **缺陷 6**：`campaign_state.last_updated` → `updated_at`（`ALTER RENAME COLUMN`，无项目代码读取方，安全）。

### 6.4 校验
| 项 | 结果 |
|---|---|
| 8 张核心表 FK 声明 | 齐全（alphas2/datasets1/fields1/waves2/expressions1/diversity2/campaign_state1/backtest1） |
| `foreign_key_check` 违例 | 0 |
| expressions / backtest_results 漂移 | 0 / 0 |
| 悬挂 alpha_id | 0 |
| region_id 填充（wave_results/registry_empirical） | 0 NULL |
| 行数 | fields 45079 / expressions 5971 / backtest 473 均无损 |

### 6.5 唯一 defer
- **缺陷 4（DECIMAL→REAL）**：SQLite 本就不强制 `DECIMAL` 精度、存储值完全一致，改为 `REAL` 纯属 cosmetic，且需重建多张表有数据风险、零功能收益，故 defer。如坚持可补。

### 6.6 仍待用户拍板的非缺陷项
- **45 个 `recovered_ds_*` 占位 dataset**（来自首轮 P0 修复）：属被删 dataset 的孤儿回填，元数据缺失、region 标 USA 哨兵。可后续补全真实元数据，或 purge 占位 + 其字段（依用户"偏好可恢复"纪律，暂保留）。


