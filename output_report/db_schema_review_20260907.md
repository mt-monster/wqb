# wqb.db 数据库表结构审查报告（2026-09-07）

> 审查对象：`data/wqb.db`（73 MB，16 表，无 WAL 残留）
> 方法：全表 DDL + 索引 + 外键 + 引用完整性 + 冗余度 + 对账交叉验证

---

## 一、表结构总览

```
regions (14)
  └─ datasets (1,880)
       ├─ fields (135,824)          ← 平台字段目录（verified 三态）
       └─ field_profile (30,705)    ← WebDataScope S1 字段画像
waves (541)
  └─ expressions (9,988)
       └─ backtest_results (1,625)
alphas (1,638) ← 平台 alpha 池
submission_ledger (21) ← 提交账本
ledger_kv (1,923) / registry_empirical (729) / wave_results (418)
gate_results (422) / campaign_state (7) / external_fields (24)
cross_region_lessons (11)
```

**体积分布**：fields 25.7 MB + 其索引 14 MB｜ledger_kv 13.7 MB｜datasets 5.1 MB｜field_profile 3.7 MB｜其余合计 <10 MB

---

## 二、结构合理性评审

### ✅ 做得对的地方

| 项 | 证据 |
|---|---|
| 唯一约束完整 | fields(dataset_id, field_name)、waves(region_id, wave_number)、expressions(wave_id, expression)、backtest_results alpha 唯一索引、alphas.alpha_id 零重复、ledger_kv(region,key) 零重复 |
| 分层清晰 | regions→datasets→fields 三级目录与 waves→expressions→backtest_results 流水线分离，职责不混 |
| 索引覆盖合理 | 21 个索引覆盖 region/status/sharpe/fingerprint 主要查询路径 |
| 外键已写进 DDL | 8 张表定义了 REFERENCES |
| 验证体系（9/1 新增） | verified/verified_context/verified_at 三列 + external_fields 表，token-name 隐患可拦截 |

### ❌ 结构问题（按严重度）

| # | 问题 | 证据 | 影响 |
|---|---|---|---|
| 1 | **PRAGMA foreign_keys=0，外键从未生效** | DDL 有 REFERENCES 但连接级开关未开 | waves.dataset_id 137 个 NULL 孤儿、expressions 85 个 wave_id 孤儿已产生 |
| 2 | **双轨引用（设计债）** | expressions 同时有 wave_id FK 和 region/wave/dataset TEXT；registry_empirical / wave_results 同时有 region TEXT + region_id（region_id NULL 分别 494/135 个） | 18 条双轨冲突数据；查询时两条路径可能给出不同答案 |
| 3 | **status 枚举失控** | expressions.status 15 种值，大小写混用（COMPLETE 22 / completed 16）；pending 3,448 条积压 | 状态机不可枚举，统计口径易错 |
| 4 | **alphas 新列未回填** | universe/delay 86.6% NULL、alpha_type/platform_status 88.5% NULL、neutralization 60.9% NULL | 按区域/延迟筛选 alpha 时漏数据 |
| 5 | **expressions.alpha_id 无索引** | 1,106 个非空值，join alphas 全表扫 | 每次对账 join 慢 |
| 6 | **catalog_json 滞留** | datasets 568 行结构化列已提取但原始 JSON 未清 | 约 2-3 MB 冗余 |
| 7 | **指标双存** | backtest_results 与 expressions 有 992 个 alpha_id 重叠，sharpe/fitness 双份 | 更新时可能不同步 |

---

## 三、数据齐全性评审

### 字段验证覆盖（9/1 重跑后状态）

| 区域 | fields 总数 | verified=1 | 缺口 |
|---|---|---|---|
| GLB | 28,465 | 28,465 | ✅ 齐 |
| HKG | 25,648 | 25,648 | ✅ 齐 |
| DEU | 22,494 | 22,494 | ✅ 齐 |
| USA | 40,948 | **0** | ❌ **全未验**（当时按你要求跳过） |
| EUR | 6,360 | 4,570 | ⚠️ 1,790 未验（9/6 新灌 S1 数据集：intraday_pv_feats 585 / ai_equity_alpha 582 / model193 173 等） |
| KOR | 8,055 | 3,320 | ⚠️ 4,735 未验（analyst_consensus 2,343 / analyst10 640 / analyst44 540 等） |
| MEA | 2,115 | 2,115 | ✅ 齐 |
| IND | 974 | 974 | ✅ 齐 |
| GBR | 765 | 765 | ✅ 齐 |
| **合计** | **135,824** | **88,351** | **47,473 未验** |

### 提交对账缺口

- alphas 有 date_submitted：**71** 个
- submission_ledger 仅 **21** 行
- → **约 50 个早期提交未走 ledger 记账**（账本建立前的历史提交），账本完整性从 2026-08 下旬才开始

### 其他数据缺口

| 项 | 状态 |
|---|---|
| ASI 区域 | datasets 表 169 个数据集，但平台无权限（get 0），field_profile 无对应画像 |
| PINGTEST/CHN/JPN/ILLIQUID | 4 个测试/边缘区域混在 regions 正式表（PINGTEST 2 数据集、CHN 11、JPN 2、ILLIQUID 1） |
| field_profile 来源单一 | 全部 30,705 行 source=webdatascope，与 fields 仅 8,469 字段名交集 |
| expressions.pending | 3,448 条积压未流转（gated 2,652 之后最大的池） |

---

## 四、优化方案

### P0 — 数据修复（防止继续污染，~1 小时）

1. **统一 status 枚举**：`COMPLETE/COMPLETED → completed`，一个 UPDATE 搞定；同时约定小写枚举集 {pending, gem, enhanced, gated, selected, backtested, completed, submitted, superseded, dropped}
2. **expressions 85 个 wave_id 孤儿**：先查明指向（可能是 waves 表清理时删除的行），归档到 `wave_id=NULL + source='orphan'` 或补建 wave
3. **submission_ledger 回补 50 条历史**：从 alphas.date_submitted IS NOT NULL 且不在 ledger 的行反插（status='SUCCESS', source='backfill'）

### P1 — 结构加固（半天）

4. **启用外键**：在所有连接入口（`wqb_db_mcp.py` 的 connect、`tools/lib/*.py`）统一加 `PRAGMA foreign_keys=ON`；先清干净孤儿再开，否则插入报错
5. **补索引**：
   ```sql
   CREATE INDEX idx_expressions_alpha_id ON expressions(alpha_id);
   CREATE INDEX idx_datasets_region ON datasets(region_id);
   CREATE INDEX idx_waves_region ON waves(region_id);
   ```
6. **清 catalog_json**：结构化列已提取的 568 行置 NULL（先备份）
7. **waves.dataset_id 137 NULL 回填**：多数可从 expressions.dataset TEXT 反推

### P2 — 数据补齐（按需排期）

8. **USA 字段验证**：40,948 字段 / 391 数据集，是唯一整区缺口。按 9/1 速度（~950 字段/分钟）约 45 分钟一批跑完，建议分 4 批防 429
9. **KOR 4,735 + EUR 1,790 新灌字段验证**：`validate_fields_batch.py --region KOR --dataset analyst_consensus --sleep 3` 逐数据集补
10. **alphas universe/delay 回填**：从 expressions.settings_json JOIN 或平台 get_alpha_details 批拉
11. **ASI 处置**：确认无权限后从 regions 表移除（保留备份），避免 S0 白名单误选

### P3 — 长期规范（下次大版本）

12. **双轨收敛**：region TEXT 列冻结只读，新代码一律用 region_id；分批迁移存量（registry_empirical 494 个 NULL region_id 可从 region TEXT 反填）
13. **指标单一真相源**：expressions 保留生成期指标，平台回测指标以 backtest_results 为准；alphas 保留提交后快照 —— 三者职责写进 AGENTS.md
14. **field_profile 挂接**：加 fields_id 列关联（同名 8,469 交集可先挂），S1 画像可直接 join 目录

### 建议执行顺序

```
P0.1 枚举统一 → P0.2 孤儿处置 → P0.3 账本回补
→ P1.5 补索引（零风险先做）→ P1.4 启用外键
→ P2.8 USA 验证（大活，约 45 分钟×4 批）
→ P2.9 KOR/EUR 补验 → P2.10 alphas 回填
→ P3 择机
```

---

## 五、快速体检脚本（可复用）

本次审查的全部检查已固化为查询，关键对账 SQL：

```sql
-- 孤儿检查
SELECT COUNT(*) FROM waves w LEFT JOIN datasets d ON w.dataset_id=d.id WHERE d.id IS NULL;
-- 提交对账
SELECT s.alpha_id FROM submission_ledger s LEFT JOIN alphas a ON a.alpha_id=s.alpha_id
WHERE s.status='SUCCESS' AND a.date_submitted IS NULL;
-- 验证覆盖率
SELECT r.name, SUM(f.verified=1)*100.0/COUNT(*) FROM fields f
JOIN datasets d ON f.dataset_id=d.id JOIN regions r ON d.region_id=r.id GROUP BY r.name;
```
