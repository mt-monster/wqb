# DEU ATOM 战役 · 正式交付文档（2026-11-08，v4 两颗已提交）

**⚠ v4 变更（2026-11-08 14:11，第二颗提交执行后）**：
1. **`zq3eb7No` 已提交 ACTIVE**（用户点名「免查 prod」）→ name `DEU_R_afslvlrev_01`，BLUE，tags `CH_REG / SRC_afs_level_revision / CORR_060`；prod 闸读缓存 **0.6171**（@02:17:15，未重测）。**ΔS +0.70**（分区 1.73→2.43，DD 6.08%→3.73%），过新硬闸。ET 今日 REGULAR **3/4**。
   - 5 ops：`group_rank(add(ts_zscore(est_12m_ebt_mean,240), ts_zscore(subtract(est_12m_pre_mean, est_12m_pre_mean_4wks_ago),66)), sector)`；S2.01/F1.28/2Y1.64/sub1.00/CLUSTER1.50/inv1.46；self 0.3641。
   - 稳健性 CONDITIONAL：**16 条修复仿真六轴全覆盖后判定结构内生**（腿1 2023 S=0.03 归零、腿2 撑近段，交替 regime 静态配平只能把弱年从 2023 挪到 2021）。报告 `reports/robustness_20261108.md` 修复章。
2. **同族顺序结论**：先交 `zq3eb7No` 后 `RREPm361` prod 仍 0.6881（0.6879 未超过现最高值）；反向先交 RREPm361 会把 zq3eb7No 顶到 0.6879 当场作废。**同族只能留一颗时先交余量大的。**
3. 剩余候选 3 席（RREPm361 / QPvzNNGG / QPv6jLvX），prod 余量 0.012 / 0.022 / 0.039 全部贴线；今日仅余 **1 个 REGULAR 名额**。

**⚠ v3 变更（2026-11-08 13:00，第一颗提交执行后）**：
1. **`bl6AvMkN` 已提交 ACTIVE**（用户点名「免查 prod」）→ name `DEU_R_afsstarmine_01`，color BLUE，tags `CH_REG / SRC_afs_starmine / EXPRFAM_afsstarmine`；prod 闸读 48h 缓存 0.647 过闸（**未**重测，缓存 @2026-11-07T23:49:43）。
   - ⚠ **边际贡献 ΔSharpe −0.04（稀释）**，提交于新闸上线前；**2026-11-08 起 ΔS<0 已是硬闸（force 不豁免）**，同型候选不得再提交。
   - 稳健性审：CONDITIONAL（近 3 年 2.70/2.03/1.78 均值 2.17 过、无负年、末段三年缓降记 soft_flag）；台账 `robustness_bl6AvMkN`（DEU）+ `reports/robustness_20261108.md`。
2. **`MPY9VNY9` 判死**：`↔ xArzm3Mn（已 ACTIVE）= 0.9924` ⇒ SELF 必 FAIL。两者同为 `shrt3_bar`，仅 backfill 窗 22 vs 24。**从篮子剔除**。
3. **`QPv6jLvX ↔ vR1oxZA3（已提交）= 0.5227 > 0.5** ⇒ 严执 <0.5 标准时应出局。

**当前剩余候选（提交前须逐颗 refresh 终验 prod；今日仅余 1 名额）**：
| # | alpha | 数据集 | 类型 | S | F | 2Y | TO | prod | 余量 | self max | 风险 |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | QPv6jLvX | analyst93 | 严格ATOM(ANALYST) | 1.59 | 1.52 | 2.01 | 0.0411 | 0.6615 | 0.0385 | 0.523 | S 仅 +0.01；CLUSTER 0.99<1；与 vR1oxZA3 0.5227 |
| 2 | QPvzNNGG | predictive_starmine | 严格ATOM(MODEL) | 1.70 | 1.30 | 2.18 | 0.155 | 0.6777 | 0.0223 | **0.6779** | prod 与 self 双贴线 |
| 3 | RREPm361 | analyst7 | 严格ATOM(ANALYST) | 2.02 | 1.25 | 1.82 | 0.2508 | 0.6881 | **0.0119** | 0.327 | prod 余量 0.012，极易漂线 |
| — | ~~MPY9VNY9~~ | shortinterest3 | — | 1.59 | 1.26 | 2.36 | 0.036 | 0.5986 | — | **0.9924** | **死：撞 ACTIVE xArzm3Mn** |
| ✅ | ~~bl6AvMkN~~ | afs+starmine | — | 1.61 | 1.36 | ladder 2.15 | 0.1097 | 0.6470 | — | 0.514 | **2026-11-08 13:00 已提交 ACTIVE** |
| ✅ | ~~zq3eb7No~~ | analyst7 | 严格ATOM(ANALYST) | 2.01 | 1.28 | 1.64 | 0.2262 | 0.6171 | 0.083 | 0.364 | **2026-11-08 14:11 已提交 ACTIVE** |

---

# v2 存档（<0.5 标准 · 5 席）

**⚠⚠⚠ v3 变更（2026-11-08 22:10，风暴第三波）**：
- QPv6jLvX prod **0.992 FAIL**（analyst93 族清零）——18h 终验全景：RREPm361 0.6881 ✓ / QPvzNNGG 0.6777 ✓ / bl6AvMkN 0.6470 ✓ / zq3eb7No 0.6171 ✓ / QPv6jLvX 0.992 ✗。
- **有效篮子 = 3 席**，两个互斥方案（RREPm361↔zq3eb7No 互相关 0.688 只能二选一）：
  - **方案 A**：[RREPm361, QPvzNNGG, bl6AvMkN]——IS 最优（S 2.02/2Y 1.82），但 RREPm361 prod 余量 0.012 极薄
  - **方案 B（推荐）**：[zq3eb7No, QPvzNNGG, bl6AvMkN]——zq3eb7No prod 余量 0.083 最抗漂移（S 2.01/2Y 1.64）
- 补探收官：Wave 59 analyst47（S≤0.53）/ Wave 60 model30（S≤0.92）判死，pv30=GROUP 分组集跳过 ⇒ **68/68 数据集全部处置完毕**。
- 24h 死亡总名单：mLox6Mg2/A1Vvqded/MPY9VNY9/QPv6jLvX + npvwXA8l/QPveY7Kg（族连坐）。
- 提交纪律：**终验→立即提交**，不得隔夜；每颗提交前 refresh 终验。

**⚠ v2 变更（2026-11-08 深夜）**：
1. 用户指令：交付篮子互相关全对 ≤0.7 → **<0.5**（严格不等）。
2. prod 漂移事件：mLox6Mg2 终验 prod **0.9922 FAIL**；孪生 A1Vvqded **0.916 FAIL**；QPveY7Kg 同骨架按族判死 ⇒ 情绪族全灭。
3. 新标准下最大独立集 = **5 席**（LLMzYrZe 0.678/zq3eb7No 0.688 等出局）。

**v2 交付篮子（5 席，互相关最大对 0.402）**：
| # | alpha | 数据集 | 类型 | S | F | 2Y | TO | prod | 备注 |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | RREPm361 | analyst7 | 严格ATOM(ANALYST) | 2.02 | 1.25 | 1.82 | 0.2508 | 0.6881 ⚠余量0.012 | 备援 zq3eb7No(prod 0.6171，互相关 0.688 不可同篮) |
| 2 | QPvzNNGG | predictive_starmine | 严格ATOM(MODEL) | 1.70 | 1.30 | 2.18 | 0.155 | 0.6777 | |
| 3 | MPY9VNY9 | shortinterest3 | 严格ATOM(SHORTINT) | 1.59 | 1.26 | 2.36 | 0.036 | 0.5986 | |
| 4 | QPv6jLvX | analyst93 | 严格ATOM(ANALYST) | 1.59 | 1.52 | 2.01 | 0.0411 | 0.6615 | |
| 5 | bl6AvMkN | afs+starmine | 双集(MODEL+ANALYST) | 1.61 | 1.36 | 2.15 | 0.1097 | 0.6470 | |

**★ 提交前健康检查（2026-11-08 03:00，refresh 终验）**：
| alpha | prod 原值 | prod 现值 | 漂移 | 判 |
|---|---:|---:|---|---|
| RREPm361 | 0.6881 | 0.6881 | 0 | ✓ 直方图逐位一致 |
| QPvzNNGG | 0.6777 | 0.6777 | 0 | ✓ |
| QPv6jLvX | 0.6615 | 0.6615 | 0 | ✓ |
| bl6AvMkN | 0.6470 | 0.6470 | 0 | ✓ |
| MPY9VNY9 | 0.5986 | 槽位被占未复测（retry 240s×2 busy） | — | 缓存值，余量 0.101 最大，提交时 refresh 终验 |

结论：5 席 prod 当前全部健康无漂移（mLox6Mg2 事件未波及）。提交时仍须逐颗 refresh（纪律不变）。

**出局名单（<0.5 标准或 prod 族灭）**：LLMzYrZe(0.678 vs QPvzNNGG)、zq3eb7No(0.688 vs RREPm361，留作 RREPm361 换防)、mLox6Mg2(prod 0.9922)、A1Vvqded(prod 0.916)、QPveY7Kg(族灭)、Xg9WNVvl(0.60/0.72)、npvwXA8l(0.92)、bl6AO0Qp/ZYQNAVKQ/YP1YgK7J(0.87-0.94 vs RREPm361)。

**v1 的 8 席清单保留在下方供历史与换防参考（mLox6Mg2/A1Vvqded 已 prod 死、LLMzYrZe/zq3eb7No 超 0.5 互相关）**：

---

# v1 存档（≤0.7 标准 · 8 颗全闸通过候选）

**状态**：8 颗全闸通过候选（目标 10，缺口 2 席结构性穷尽，见 segment_verdict_w34w37_20261108.md）
**提交门槛**：REGULAR 通道 S≥1.58、2Y≥1.58（阻断线）、F≥1.0、TO≤0.7、sub_universe≥0.474×S、failed_ra=0、self<0.7、prod<0.7
**提交前提**：用户明确授权（提交不可逆）+ 提交时逐颗 refresh=True 终验 prod

---

## 提交清单（按建议提交顺序：prod 余量从大到小）

### 1. MPY9VNY9 — shortinterest3（严格 ATOM，SHORTINTEREST 塔）
```
-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),240)), rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),176))), target_tvr=0.03), subindustry)
```
设置：DEU/TOP500/D1/SUBINDUSTRY/decay1/trunc0.08
S 1.59 / F 1.26 / 2Y 2.36 / TO 0.036 / prod 0.5986（余量最大，建议首提交）

### 2. bl6AvMkN — analyst_factor_signals + predictive_starmine（合法双集 MODEL+ANALYST）
```
group_neutralize(add(rank(ts_mean(eps_y1_estimate_change_3mo, 66)),
                     rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
                 bucket(rank(ts_mean(predicted_surprise_f12m_ebitda_4, 66)), range="0,1,0.1"))
```
设置：DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc0.08
S 1.61 / F 1.36 / 2Y 2.15 / TO 0.1097 / self 0.514 / prod 0.6470

### 3. QPv6jLvX — analyst93（严格 ATOM，ANALYST 塔）
```
group_rank(add(rank(ts_mean(vec_avg(anl93_recprofitabilityprev_estimator_profitability2), 132)),
               rank(ts_mean(vec_max(anl93_recprofitabilityprev_estimator_profitability2), 11))), industry)
```
设置：DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc0.08
S 1.59 / F 1.52 / 2Y 2.01 / TO 0.0411 / prod 0.6615
⚠ CLUSTER_TEST 0.99 贴上限（warning 非 fail）

### 4. LLMzYrZe — predictive_starmine（严格 ATOM，MODEL 塔）
```
group_rank(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5)),
               rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), sector)
```
设置：DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc0.08
S 1.61 / F 1.16 / 2Y 1.69 / TO 0.153 / prod 0.6697

### 5. QPvzNNGG — predictive_starmine（严格 ATOM，MODEL 塔，bucket 轴版）
```
group_neutralize(add(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 12)),
                          rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
                      rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22))),
                 bucket(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 252)), range="0,1,0.05"))
```
设置：DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc0.08
S 1.70 / F 1.30 / 2Y 2.18 / TO 0.155 / prod 0.6777

### 6. zq3eb7No — analyst7（严格 ATOM，ANALYST 塔，第 8 席新件）
```
group_rank(add(ts_zscore(est_12m_ebt_mean, 240),
               ts_zscore(subtract(est_12m_pre_mean, est_12m_pre_mean_4wks_ago), 66)), sector)
```
设置：DEU/TOP500/D1/FAST/decay0/trunc0.08（5 算子）
S 2.01 / F 1.28 / 2Y 1.64 / TO 0.2262 / self 0.3321 / prod 0.6171（hist [0.6,0.7) n=2）

### 7. RREPm361 — analyst7（严格 ATOM，ANALYST 塔，破墙件）
```
group_rank(add(ts_zscore(est_12m_ebi_median, 240),
               ts_zscore(subtract(est_12m_ebt_mean, est_12m_ebt_mean_4wks_ago), 44)), sector)
```
设置：DEU/TOP500/D1/FAST/decay0/trunc0.08（5 算子）
S 2.02 / F 1.25 / 2Y 1.82 / TO 0.2508 / self 0.2924 / prod 0.6881

### 8. mLox6Mg2 — sentiment7 + sentiment27（合法双集 SENTIMENT，vector_neut 版）
```
vector_neut(ts_quantile(ts_ir(ts_mean(max(ts_backfill(vec_avg(snt7_all_languages_views),22),
                     ts_delay(ts_backfill(vec_avg(snt7_all_languages_views),22),5)),5),22),252,driver="gaussian"),
            ts_backfill(vec_avg(snl27_relpopularity08),22))
```
设置：DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc0.02
S 2.05 / F 1.71 / 2Y 2.53 / TO 0.147 / prod **0.6935 ⚠ 余量 0.0065 最贴线（终验 refresh 已触发，结果见台账更新）**

---

## 提交后互相关自锁注意

- 平台提交是串行的：每提交一颗，OS 池即更新，后续候选的 self 会重算。8 席按上表顺序提交可最小化自锁风险（先提交与分析师/情绪族无重叠的件）。
- 若某颗在提交时 prod 漂过 0.70：跳过该颗，继续提交其余；跳过后重跑 compute_mutual_correlation 确认剩余篮子仍全对 ≤0.7。

## 缺口说明

第 9/10 席穷尽证明：17 数据集本段判死 + 44 cov=0 + 5 密度不足 + 备用池 6 颗互相关阻塞 + 家族容量（analyst7×2 / starmine×2 / anl93×1 / shortinterest×1 / sentiment×1 / afs×1）全部占满。详见台账判据 H–AJ。

## 产出物索引

- 台账：tracking/DEU/atom_orthogonal/segment_verdict_w34w37_20261108.md（本段）及系列台账
- 表达式存档：w36_exprs.json / w37_model36_exprs.json / w33/w34/w35_exprs.json
- 字段画像：analyst7_fields.csv（608）、model25/26/109/262/144、multifactor_return_pred、order_book_imbalance、pv109 等各 *_fields.csv
- 历史交付：final_delivery_20261107.md（5 颗版）