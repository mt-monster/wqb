# S1 族级判死机制设计（v1，草案）

> 状态：**仅设计，未实施**。本文不修改任何 S1 代码，等待评审确认后再动手。
> 依据：2026-09-30 对本仓真实数据的实测（回测 9125 条、表达式 69281 条、registry_empirical 1037 行）。

---

## 1. 为什么需要它

### 1.1 现状浪费（实测）

| 指标 | 值 |
|---|---|
| 历史回测总数 | 9125 条 |
| 其中 `ra_clean`（\|S\|≥1.58 ∧ F≥1.0 ∧ 无 RA 失败） | 646 条 = **7.1%** |
| 打在「后来被证伪」数据集上的回测 | 4475 条 = **49%** |
| 平均每个死集耗掉的回测 | **22.8 条** |

### 1.2 数据集级判死为什么不行（已实测否决）

`registry_empirical` 有 486 条 `dead_end`，96% 能解析出数据集名（268 个 `(region,dataset)`）。
但把判死挂在**数据集级**做反事实推算：

| | 值 |
|---|---|
| 这 268 个组合中我们真回测过的 | 154 个，涉及 5064 条回测 |
| 其中有产出的集 | **26 个，累计 319 条 ra_clean** |
| 占全部历史产出（646 条） | **49%** |
| 可避免的回测 | ≈2292 条 |

→ 省 2292 条回测的代价是误杀 26 个产能集、威胁近一半历史产出。**风险/收益比很差，数据集级判死不做。**

### 1.3 根因：判死记的是「族」不是「集」

判死条目的 `payload.family` 写得很具体：

- `"pv1 vol/adv/cap G2 (zqkazgld 族)"` → 死因 `PROD_CORRELATION 0.7723 > 0.7 REJECT`
- `"fundamental72 is_q 水平场 zscore252 (oper_inc/EBITDA 族)"` → 死因 `PROD 0.7879 > 0.7 REJECT`
- `"pv106 spread 白空间 (bid_ask_price_gap / price_difference_bid_ask 的 level/zscore/delta 变体)"`

死因集中在 **PROD 硬闸**——是这个**变体族**死了，同一个集里别的族照样能活。
所以判死必须下沉到族级，并挂在 **S1（选字段/定骨架）** 而不是 S0（选数据集）。

---

## 2. 族指纹：用什么粒度

### 2.1 可复用的现成字段

`expressions` 表（69281 行）已 100% 填充两个现成的结构分量：

| 列 | 填充率 | 唯一值 | 说明 |
|---|---|---|---|
| `skeleton` | 100% | 7233 | 算子几何骨架，字段被抽成占位符，如 `rank(vec_avg(F))`、`subtract(N, rank(vec_avg(F)))` |
| `fingerprint` | 100% | 64676 | 每条几乎唯一 → **太细，不适合做族** |
| `dataset` | 98% | — | 数据集分量 |

字段簇分量需从 `expression` 文本里正则抽取（已有先例：`build_field_prefix_clusters`，见 `src/wqb/store/_field_catalog.py`）。

### 2.2 粒度实测（40000 条表达式样本，基线 max\|S\|≥1.25 = 0.5%）

| 粒度 | 族数 | 平均条/族 | ≥8 条样本的族 | 其中 max\|S\|≥1.25 | lift |
|---|---|---|---|---|---|
| G1 精确字段集 + 骨架 | 34160 | 1.2 | 14 | 4（28.6%） | **52.9x** |
| G2 字段前 2 段 + 骨架 + 集 | 18179 | 2.2 | 694 | 8（1.2%） | 2.1x |
| G3 字段首段 + 骨架 + 集 | 13384 | 3.0 | 958 | 9（0.9%） | 1.7x |
| G4 集 + 骨架（无字段） | 6328 | 6.3 | 1490 | 12（0.8%） | 1.5x |
| G5 字段前 2 段 + 骨架（跨集） | 17919 | 2.2 | 711 | 10（1.4%） | 2.6x |

**读法**：越细区分度越高，但样本量断崖式枯竭（G1 只剩 14 个族够 8 条）。单一粒度无解。

### 2.3 结论：双粒度

| 层 | 定义 | 语义 | 处置 |
|---|---|---|---|
| **FAM-EXACT** | `sha1(region \| dataset \| sorted(字段名集) \| skeleton)[:12]` | 完全同构的变体族 | 命中 dead_end → **硬拒** |
| **FAM-PREFIX** | `sha1(region \| dataset \| sorted(字段名前 2 段簇) \| skeleton)[:12]` | 同一字段簇 + 同一几何 | 命中 dead_end → **软警告，需人工确认** |

- FAM-EXACT 平均 1.2 条/族 ⇒ 命中即说明**这条几乎一模一样的路已经走过**，误伤风险≈0，可硬拒。
- FAM-PREFIX 有 2.1x lift 且能积累样本（694 个族够 8 条），是唯一可「判死」的粒度，但仍会连坐 → 只软警告。
- **不做**数据集级（G4 的 1.5x lift 不足以抵消 49% 的产出连坐风险）。

---

## 3. 拦截点

```
S0 选数据集（s0-select）          ← 不动，族级判死不在这里
   ↓
S1 扫字段 → field_catalog         ← ★ 新增闸：族级判死在此拦截
   ↓  s1_<ds>_d<delay> ledger
S2 生成表达式（GEM / 模板）
   ↓
S3 回测
```

**拦截时机**：S1 产出 `s1_<ds>_d<delay>` 之后、S2 生成表达式之前。
对每个「待生成族」计算 FAM-EXACT / FAM-PREFIX，查族级判死表，命中则拦下（硬）/ 标注（软）。

**为什么不放在 S2 之后**：S2 已经烧掉生成算力与回测槽位了，判死要在出表达式之前。

---

## 4. 数据源与判死表

### 4.1 三路来源

| 来源 | 现状 | 处置 |
|---|---|---|
| `registry_empirical.layer='dead_end'` | 486 行，其中 230 行 payload 含 `family`（可解析 198 条） | **主源**。现有 family 是自然语言，需一次性回填族指纹 |
| `ledger_kv` 的 `*_dead` 键 | 全库 45 条 | 保留，**数据集级**，仅作 S0 的粗筛（现状不变） |
| `backtest_results` 的族级失败 | 可自动派生 | **新增**：族样本 ≥8 且 ra_clean=0 且 max\|S\|<1.0 → 自动判死候选（人工确认后入表） |

### 4.2 新增表（建议）

```
family_deadend(
  fam_key        TEXT PRIMARY KEY,   -- FAM-EXACT 或 FAM-PREFIX 的 sha1[:12]
  fam_level      TEXT,               -- 'exact' | 'prefix'
  region, dataset, skeleton,
  field_clusters TEXT,               -- 归一化后的字段簇串（可读）
  reason         TEXT,               -- 死因：PROD_CORR / 2Y / CW / NO_SIGNAL / ...
  evidence       TEXT,               -- alpha_id 或 wave 号（必须可回溯）
  source         TEXT,               -- 'registry' | 'auto' | 'manual'
  dead_at        TEXT,
  confidence     TEXT                -- 'hard' | 'soft'
)
```

**写入纪律**：`evidence` 必填且必须可回溯到真实 alpha_id/wave；`source='auto'` 的条目默认 `confidence='soft'`。

---

## 5. 匹配与判级

1. 对待生成族计算两个 key。
2. 查 `family_deadend`：
   - 命中 `exact` → **HARD：拒绝生成**（打印命中条目的 evidence + reason）
   - 命中 `prefix` → **SOFT：打印警告 + 需要 `--force-family` 才能继续**（留痕）
3. 未命中 → 放行。

**子串匹配的坑（实测）**：一条 `MEA-PV106-SPREAD-DEAD` 会同时命中 `pv106 / pv1 / pv`，一条 `FND72` 会命中 `fundamental72 / fundamental7 / fundamental`。
→ 自然语言 family 只在**回填**阶段用（一次性、人工核对），**运行期只用哈希 key 精确匹配**，不做子串。

---

## 6. 与现有 gate 的关系

建议作为 **闸 1.5**（S1 出口闸），排在所有现有闸之前：

| 闸 | 阶段 | 作用 |
|---|---|---|
| **闸 1.5（新）** | S1 出口 | 族级判死：这条路走过吗？ |
| 闸 2/3 | S1 | 字段类型 / 覆盖率 |
| 闸 7 | S1 | VECTOR 字段 longCount（建议阈值 80 → 100，另案） |

---

## 7. 验收指标（可测，先定后做）

| 指标 | 定义 | 目标 |
|---|---|---|
| 族级命中率 | 被闸 1.5 拦下的族 / 进入 S2 的族总数 | 先观察 2 周，不设硬目标 |
| 误伤率 | 被拦下族中，同一族在其它区/其它期后来产出 ra_clean 的比例 | **< 5%** |
| 回测节省 | 同等工作量下，投入死族的回测条数降幅 | 相对基线降 **≥30%** |
| 每族证伪成本 | 判定一个族死亡所耗回测条数 | 从 22.8（数据集级）降到 **≤8** |

> 误伤率怎么测：`family_deadend` 每条记 `dead_at`，事后回查该族在 `dead_at` 之后是否出现 ra_clean。

---

## 8. 风险与回滚

| 风险 | 缓解 |
|---|---|
| 族指纹定义变更导致历史 key 全部失效 | `fam_key` 带版本前缀（如 `v1:`），变更即新建版本，旧版本仍可查 |
| FAM-PREFIX 连坐误杀 | 只做 SOFT（需 `--force-family`），且默认不阻断 |
| 自然语言 family 回填质量差 | 回填只跑一次、人工核对；运行期不依赖它 |
| 判死表膨胀后无人维护 | `source='auto'` 条目 90 天无复核自动降为 `soft` |

**回滚**：闸 1.5 默认开启，提供 `--no-family-gate`；判死表是独立表，删表即完全回到现状。

---

## 9. 分步实施计划（待评审）

| 步 | 内容 | 产物 | 依赖 |
|---|---|---|---|
| 1 | 族指纹计算函数 `fam_key(region, dataset, fields, skeleton, level)` | `tools/family_key.py` | 无 |
| 2 | 对现存 69281 条 `expressions` 回填 fam_key（双粒度） | `expressions` 新增 2 列 | 步 1 |
| 3 | 一次性把 198 条自然语言 family 映射到 fam_key（人工核对） | `family_deadend` 初始数据 | 步 1 |
| 4 | 自动派生：族样本 ≥8 且 ra_clean=0 且 max\|S\|<1.0 → soft 条目 | `family_deadend` | 步 2 |
| 5 | 闸 1.5 实现 + `--force-family` / `--no-family-gate` | gate.py | 步 3+4 |
| 6 | 回归测试（误伤率 / 命中率 / 粒度不漂移） | `tests/unit/test_family_deadend*.py` | 步 5 |
| 7 | 影子模式跑 2 周（只打印不拦截），用 §7 指标验收 | 报告 | 步 5 |

**建议先只做步 1–2**（纯回填、零行为变更），拿真实族分布再决定是否上闸。

---

## 附：本文引用的实测命令口径

- `ra_clean` = `ABS(sharpe)>=1.58 AND fitness>=1.0 AND TRIM(ra_failed_checks) IN ('','[]')`
- 粒度扫描样本：`expressions` 前 40000 条（dataset/skeleton 非空）
- 反事实推算：判死条目按「最长匹配、每条目只归一个数据集」解析，避免 `pv1` 连坐 `pv106`
