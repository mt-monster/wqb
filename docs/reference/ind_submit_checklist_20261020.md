# IND 提交清单（2026-10-20 15:50 核对版）

> **判定口径**：`ra.failed_ra_count == 0`（权威）+ IS 全闸 + prod<0.70 + self<0.70。
> ⚠ **本文档纠正了此前一个错误**：`harvest2.py` 输出的 `RA_FAIL` 字段只统计 `checks.fail[]`，
> 漏掉落在 `checks.warning[]` 却计入 `ra.failed_ra_count` 的 `CONCENTRATED_WEIGHT`。
> 真实可提交数不是 9 颗，而是 **6 颗可提交 + 1 颗已落地**。

---

## 一、可提交（GREEN，6 颗）

按建议提交顺序排列（先提交 self 余量大、指标最稳的）。

### 1. `O0JZwrEp` — IND_R_AFS_EPSY1REV_SKEWQ1_01
- **数据集**：analyst_factor_signals（纯 ATOM）
- **表达式**：`signed_power(group_rank(divide(ts_backfill(eps_y1_estimate_change_3mo, 22), add(ts_mean(ts_backfill(eps_q1_estimate_skewness, 22), 55), 0.01)), sector), 2.0)`
- **设置**：IND / TOP500 / D1 / STATISTICAL / decay 4 / truncation 0.08
- **指标**：S 1.96｜F 1.46｜TO 0.138｜2Y 1.76｜sub 1.24｜rob 1.05｜**prod 0.5810**｜**self 0.5119**｜failed_ra 0
- **描述**：已写入（96 词三段式）

### 2. `j2eZ3KAk` — IND_R_AFS_EPSREV_SKEWQ1_01
- **数据集**：analyst_factor_signals（纯 ATOM）
- **表达式**：`signed_power(group_rank(divide(ts_backfill(eps_revision_magnitude, 22), add(ts_mean(ts_backfill(eps_q1_estimate_skewness, 22), 55), 0.01)), sector), 2.0)`
- **指标**：S 1.75｜F 1.23｜TO 0.140｜2Y 1.70｜sub 1.09｜rob 1.02｜**prod 0.6118**｜**self 0.4998**｜failed_ra 0

### 3. `VkdPw6VY` — IND_R_AFS_EPSREV_SKEWQ2_01
- **数据集**：analyst_factor_signals（纯 ATOM）
- **表达式**：`signed_power(group_rank(divide(ts_backfill(eps_revision_magnitude, 22), add(ts_mean(ts_backfill(eps_q2_estimate_skewness, 22), 55), 0.01)), sector), 2.0)`
- **指标**：S 1.97｜F 1.50｜TO 0.138｜2Y 2.09｜sub 1.35｜rob 1.04｜**prod 0.6994**｜**self 0.5567**｜failed_ra 0
- ⚠ **prod 余量仅 0.0006**，平台重算有翻转风险。建议放在第 3 位，先交前两颗。

### 4. `omo3E2Jv` — IND_R_AFS_EPSY2REV_CV_01
- **数据集**：analyst_factor_signals（纯 ATOM）
- **表达式**：`signed_power(group_rank(divide(ts_backfill(eps_y2_estimate_change_3mo, 22), add(ts_mean(ts_backfill(eps_y2_estimate_coeff_var, 22), 55), 0.01)), industry), 3.0)`
- **指标**：S 1.74｜2Y 1.62｜rob 1.21｜self 0.563｜failed_ra 0

### 5. `JjPngb5m` — IND_R_PSM_REVSCORE_RESID_01
- **数据集**：predictive_starmine（纯 ATOM）
- **表达式**：`rank(ts_regression(ts_zscore(analyst_revisions_score_2, 252), ts_zscore(analyst_upward_revision_count_fy1_earnings_14d_3, 252), 252, rettype=0))`
- **指标**：S 1.89｜2Y 2.19｜rob 1.33｜**self 0.169（余量最大）**｜failed_ra 0

### 6. `3qjzz5O6` — IND_R_AN44_EPSY1_QTRDELTA_01
- **数据集**：analyst44（纯 ATOM）
- **表达式**：`rank(ts_zscore(ts_delta(ts_backfill(eps_estimate_current_year_2, 22), 66), 504))`
- **指标**：S 1.94｜2Y 2.15｜rob 1.01｜prod 0.6709｜self 0.624｜failed_ra 0

---

## 二、已落地（1 颗，勿重复提交）

| alpha | 数据集 | 状态 | failed_ra | 备注 |
|---|---|---|---:|---|
| `LL5gZoLm` | analyst_factor_signals | **ACTIVE（已提交）** | 0 | IND_R_AFS_EPSREV_CV_01，prod 0.666 |

---

## 三、被阻断（YELLOW，2 颗，**不可提交**）

| alpha | 体系 | S | F | 2Y | rob | 阻断原因 |
|---|---|---:|---:|---:|---:|---|
| `d5KZaxzY` | fundamental86 | 1.82 | 1.34 | 1.64 | 1.02 | **CONCENTRATED_WEIGHT**（failed_ra=1） |
| `9qEp8YXr` | fundamental86 | 1.81 | 1.33 | 1.64 | 1.03 | **CONCENTRATED_WEIGHT**（failed_ra=1） |
| `zqrN29xX` | fundamental86 | 1.82 | 1.34 | 1.64 | 1.02 | CW + 与 d5KZaxzY 完全重复（prod/self 一字不差） |

**IS 六闸全过、prod 0.5603、self 0.3353 —— 唯一障碍是持仓权重集中。**

### 修复方向（未验证，按优先级）
1. **提高 truncation**：0.08 → 0.10 / 0.12（直接压单票权重上限）
2. **加 `bucket` 分散**：`group_rank(x, bucket(rank(<第二字段>), range="0,1,0.1"))`
3. **提高平滑窗**：5 → 11（持仓更稳，但 rob 已实测掉到 0.81）
4. **改用 `rank(ts_rank(...))` 双层排名**压极端权重

---

## 四、候选（GREEN，8 颗，差一闸，可直接看不用改）

| alpha | 体系 | S | F | TO | 2Y | rob | 差什么 |
|---|---|---:|---:|---:|---:|---:|---|
| `6XApZ7pE` | f86 平滑6 | 1.81 | 1.33 | 0.099 | **1.65** | 0.99 | rob 差 0.01 |
| `bl8Q8EQ6` | f86 std60 | 1.78 | 1.30 | 0.103 | 1.58 | 0.98 | rob 差 0.02 |
| `xA1NYJPg` | f86 decay4 | 1.76 | 1.28 | 0.097 | 1.59 | 0.96 | rob 差 0.04 |
| `0mjpR1e6` | f86 平滑11 | 1.82 | 1.34 | 0.084 | 1.55 | 0.96 | rob + 2Y |
| `2rjpw3QY` | f86 std120 | 1.97 | 1.51 | 0.083 | 1.76 | 0.87 | rob |
| `LL5GEWGa` | f86 平滑4 | **2.18** | 0.89 | **0.429❌** | 1.90 | **1.27** | TO 超限拖垮 F |
| `wp9a3qa2` | f86 平滑3 | 2.14 | 0.81 | **0.419❌** | 1.93 | **1.34** | 同上 |
| `78ozzKe5` | f94 论坛模板 | 1.60 | 1.10 | 0.078 | **3.02** | 0.19 | rob |
| `N1ebQYpo` | f86 无平滑 | 1.63 | 0.42 | 0.399 | 1.50 | **1.03** | F + 2Y |

⚠ **候选里的 f86 系列大概率同样触发 CONCENTRATED_WEIGHT**（同一信号族），提交前需用 `submit_verdict` 逐颗核。

---

## 五、提交前必做（逐颗）

```bash
# 1. 权威判定（唯一否决）
submit_verdict(alpha_id)          # 必须 verdict != BLOCKED, failed_ra == 0
# 2. 相关性刷新（平台实时值）
check_correlation(alpha_id, refresh=True)   # prod < 0.70 且 self < 0.70
# 3. 用户明确确认后再提交
```

**禁止**：凭 `checks.fail[]` 为空就当过关；凭 `harvest2.py` 的 `RA_FAIL=-` 就当过关。
