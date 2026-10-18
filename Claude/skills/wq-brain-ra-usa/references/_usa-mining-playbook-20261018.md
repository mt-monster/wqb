# USA 数据挖掘经验手册：字段画像 × 适用模板 × 回测指标

> **定位**：USA 区两个战役（campaign_20261014 未点亮塔横跨 6 数据集 + campaign_20261017 Analyst 攻坚）的
> **可复用沉淀**。只收"下次挖还能用上"的规律（含实测数字与 alpha id），一次性流水账进 `tracking/` 不进本文件。
> **as_of**：2026-10-18（平台阈值 / operator 清单 / 塔点亮状态以此日期为准；变更后须复核）。
> **数据来源**：60+ 波回测、17 次 prod 实测、`get_alpha_details` / `get_alpha_yearly_stats` / `check_correlation` 平台权威读数。
> **怎么用**：开新战役先读 §0 三条选择链 → §1 按字段画像选题 → §2 按模板组装 → §3 对照指标预期与判死清单。
> 详细战例见 [_analyst-campaign-20261017.md](_analyst-campaign-20261017.md) 与 [_unlit-tower-campaign-20261014.md](_unlit-tower-campaign-20261014.md)。

---

## 0. 速查：三条选择链（先读这个再开挖）

### 0.1 base payment 最大化选型链（用户实证口径）

> 论坛版本答案（4 帖互证）：**高 fitness + 低 PC**；self-corr < 0.3 是 BP>1.5 的强信号；
> **`returns` 只影响 OS 特许权使用费、不影响 BP 档位**；VF（Value Factor）是账号级乘数、同批候选无差异。

```
F×(1−PC) 粗排 → robustness Phase B/C（近3年 Sharpe 均值 ≥ 平台 2Y 线，见 `PLATFORM_CHECK_LINES.low_2y_sharpe_min`；且每年 >0.3）→ 提交前 PC 重测 → self 互残检查 → 提交
```

### 0.2 prod 墙破解链（本区实证）

```
IS 全过但 prod ≥0.7 → 换 REVERSION_AND_MOMENTUM 中性化重跑（成本 1 条 sim，实测 prod −0.055）
  → 仍不过 → 换 CROWDING（水平背离族有效，加速度族无效）
  → 仍不过 → 换机制/数据集（该信号与生产池深度重叠）
```

### 0.3 self 互残链（提交即改变格局）

```
同族候选只能逐个提交；每提交 1 个即重测剩余候选 PC+self（新 alpha 同时进 prod+self 两池）
互残 >0.9 立即放弃；单数据集同族实际上限 2–3 颗
```

---

## 一、字段画像

### 1.1 analyst44（USA/D1/ANALYST，mult 1.2）——本轮唯一出交付的数据集

300 字段**全 VECTOR**（统一 `vec_avg` 归约）。按族画像：

#### 族 A：事件级修正配对 `anl44_2_<metric>_value` / `_prevalue`（αC=0，全库无人挖）

| 指标 | cov(value/prevalue) | 修正率 S（T1 模板实测） | 判定 |
|---|---:|---:|---|
| **eps** | 0.958 / 0.953 | **1.77**（配背离 1.81） | ★ 唯一强腿 |
| sales | 0.957 / 0.950 | 1.61 | 次优（差 3 闸） |
| netprofit | 0.952 / 0.946 | 1.36 | 弱 |
| ebit | 0.940 / 0.930 | 1.22 | 弱 |
| pretaxprofit | 0.940 / 0.935 | 1.00 | 弱 |
| ebitda | 0.845 / 0.833 | 0.48 | 判死 |
| dps/bps/cfps/nav/roe/roa/grossmargin/netdebt/capex/epsr | 0.61–0.94 | ≤1.32 | 判死 |
| operatingprofit | **0.21–0.31** | — | 毒字段（低于 0.5 硬闸） |

- **更新频率**：事件级（单次修正），非周期平滑 ⇒ 信息量高于任何滞后窗口配对。
- **机理**：17 个配对中只有 eps 强，因为**分析师真正修正的就是 EPS**；其他盈利口径是同一信息的不同投影（高度共线 ⇒ 互相背离无信号，8 配对横扫实证）。
- **配对纪律**：`value−prevalue` 用**对称化比率** `(v−p)/(v+p)`——分母不随趋零而爆（优于 `v/(p+1)`）。

#### 族 B：BEst 共识 `anl44_best_*`（日更截面统计量）

| 字段 | cov | αC | 画像与判定 |
|---|---:|---:|---|
| `best_eps_numest` | 0.988 | 21 | 覆盖广度；变化率 TO 0.0074 ⇒ **触发 LOW_TURNOVER 闸**（太慢也是罪） |
| `best_eps_stddev` | 0.857 | 39 | 分歧度；单独用 S 1.05，2Y 可达 2.39 但 fitness 不足 |
| `best_eps_4wk_up/dn` | 0.877 | 27/22 | 上调/下调家数（breadth）；**全族 S ≤0.30 判死**（与 `USA-ANALYST44-BREADTH-DEAD` 一致） |
| `best_eps_4wk_chg` | 0.871 | 12 | 共识 4 周变化；TO 0.0092 触发 LOW_TURNOVER |
| `best_pe_ratio` | — | **399** | 极拥挤 + E/P 族已判死（prod 0.93） |
| `best_eps_median` | 0.877 | 16 | median−mean 偏度；S 0.85 判死 |
| `best_{ebit,ptp,ni_adj}_to_sales` | 0.88–0.92 | 15–53 | 前瞻盈利率；单独弱，未成腿 |

#### 族 C：`anl44_{metric}_best_eeps_{cur,nxt}_yr`（MATRIX，fiscal period 元数据）

horizon gap（FY2−FY1）实测 **S 0.22 判死**；`lastactvalue` 三级修正（value vs 上期实际）S 1.38 差 0.2 判死；
事件流 vs 共识水平差 S ≤1.43 判死。

### 1.2 analyst7（USA/D1，300 字段全 MATRIX，cov 恒 0.5）——判死

| 族 | 字段形态 | 画像 | 判定 |
|---|---|---|---|
| 滞后窗口修正配对 | `est_12m_eps_mean` vs `_mean_4wks_ago` / `_3mth_ago` | TO 0.029–0.044（过平滑） | S ≤0.95 判死 |
| 广度 | `raised_1wk` / `lowered_1wk` / `raisednum_4wks` | 事件型计数 | S ≤0.95 |
| 分歧 | `est_12m_*_std` | αC 37–151（更拥挤） | S ≤0.69 |

⇒ **判据（可迁移）**：修正类信号用**事件级配对**（`value`/`prevalue`）优于**固定滞后窗口配对**（`mean`/`mean_4wks_ago`）——后者被窗口平均抹平。

### 1.3 已横扫判死的 6 个数据集（campaign_20261014，细节见 _unlit-tower-campaign-20261014.md）

| 数据集 | 塔/mult | 字段画像要点 | 死因（结构性） |
|---|---|---|---|
| `short_interest_pred` | shortinterest/1.1 | 日更空头预测 | **TO 0.66 结构性出局**（fitness 分母爆）；reverse 判据实证：原向 S −1.48 → reverse +2.13 |
| `twitter_sentiment_l2` | socialmedia/1.0 | 高频推文情绪 | TO 0.48–1.06，HIGH_TURNOVER 破闸 |
| `workforce_flow_skills` | **other/1.4** | 月频招聘流入/流出（cov 0.5754） | 机制成立、2Y 数据期硬顶 1.65；**但产出 3 条可迁移杠杆**（SECTOR 破 F、winsorize 破 2Y、ts_corr 第二腿） |
| `hiring_trends` | other/1.4 | cov 0.4998 VECTOR；`aggregate_open_positions_count` 唯一强字段 | 另两个字段是子集口径；`ILLIQUID_MINVOL1M` 对 USA 已失效 ⇒ 存量 ACTIVE 设置不可复现 |
| `institutions18` | institutions/1.0 | 季频持仓存量（cur/pre 配对） | **TO 0.037–0.143 全部达标但 S ≤0.92** ⇒ 季频存量差分噪声太大 |
| `macro27` | macro/1.1 | 周频抓取招聘（jobs created/removed） | 同机制更钝（周更 vs 日更）S ≤0.92 |

⇒ **选集铁律**：**频率 × 形态**两维同时满足——频率够慢（TO<0.125）且是**流量/变化率**而非**存量/水平值**；日更字段直接跳过，季频存量差分直接跳过。

---

## 二、适用模板

以下模板均在美国 analyst44 实证通过平台八闸；`W` = 平滑窗，`AXIS` = 分组轴。

### T1 事件级修正率（单指标）

```
quantile(group_rank(ts_av_diff(divide(subtract(vec_avg(<M>_value), vec_avg(<M>_prevalue)),
        add(vec_avg(<M>_value), vec_avg(<M>_prevalue))), 756), industry))
```

- **适用画像**：族 A 配对（`<M>` ∈ eps/sales/…），事件级更新。
- **要点**：对称化比率；`ts_av_diff`（只减均值不除波动 ⇒ 保留幅度，比 `ts_zscore(ts_backfill)` +41%，限慢变量）；
  756 窗是 SUB 甜点（504/756/1008 三档实测 SUB 0.42→0.81→0.57）。
- **实测**：eps 单指标 S 1.77 但 **prod 0.7775 撞墙** ⇒ 单指标腿不可提交，只作组件。

### T2 修正背离（eps − sales，盈利质量）

```
quantile(group_rank(hump(ts_av_diff(subtract(<T1(eps)>, <T1(sales)>), 756), hump=0.01), market))
```

- **适用画像**：必须「经济上不同类」的配对——盈利率 vs 收入（盈利质量：EPS 上修是否被收入验证）。
  **同财报不同盈利口径互相背离无信号**（共线，8 配对横扫实证）。
- **中性化**：RAM 或 CROWDING 破 prod；SECTOR 破 fitness/margin；**不要用 STATISTICAL/MARKET/INDUSTRY**（F/SUB/2Y 崩）。
- **实测**：IS 全过 S 1.64–1.81 / F 1.14–1.25 / 2Y 1.63–1.84 / SUB 0.79–0.86。

### T3 背离加速度（T2 的二阶差分）

```
quantile(group_rank(hump(ts_delta(ts_av_diff(subtract(<T1(eps)>, <T1(sales)>), 504), 252), hump=0.01), market))
```

- **适用画像**：同 T2；测「盈利质量背离的改善速度」。2Y 全族最高（2.19–2.21）。
- **中性化**：**只认 RAM**（CROWDING 下 prod 0.772 无效）。
- **实测**：S 1.74–1.75 / F 1.20–1.27 / 2Y 2.19–2.21 / SUB 0.85–0.89 / prod 0.689–0.698（贴线但过）。

### T4 秩背离（分布free）

```
quantile(group_rank(hump(ts_av_diff(subtract(rank(<eps_rev>), rank(<sales_rev>)), 756), hump=0.01), market))
```

- **适用画像**：同 T2；`rank` 使信号对量纲/极值不敏感。
- **注意**：与 T2 在 PnL 层高度共线（互相关 0.94）⇒ **同批只能二者取一**。
- **实测**：S 1.61–1.76 / F 1.11–1.20 / 2Y 1.62–1.64 / SUB 0.84 / prod 0.642–0.676。

### T5 慢变量水平值（跨数据集，workflow_flow_skills 实证）

```
quantile(group_rank(winsorize(ts_av_diff(<慢变量流量比>, 504), std=3), sector))  @ neutralization=SECTOR
```

- **适用画像**：月频**流量**比（如净招聘 `(in−out)/(in+out)`）；SECTOR 中性化把「行业内共性」剥成行业内相对信号。
- **杠杆**：`winsorize(std=3)` 外包破 2Y（1.48→1.63，抑制少数极端公司主导近期收益）；`ts_corr(in,out)` 是第二条正交腿（节奏 vs 量）。
- **天花板**：该族 2Y 数据期硬顶 ≈1.65（后疫情用工正常化，20+ 变体穷尽证实）。

### 模板通用杠杆与禁忌（全战役实测）

| 手段 | 效果 | 备注 |
|---|---|---|
| `REVERSION_AND_MOMENTUM` 中性化 | **prod −0.055**（破墙第一杠杆） | 同时抬 S/SUB |
| `CROWDING` 中性化 | prod −0.03~−0.06（水平背离族） | 加速度族无效 |
| `SECTOR` 中性化 | fitness/margin 杠杆（F +0.13、margin ×2.7） | 与 RAM/CROWDING 分工 |
| `winsorize(x, std=3)` 外包 | 2Y +0.15 | 必须是具名参数；preflight 误报 `unknown_fields:["std"]` ≠ 不可用 |
| `quantile` 外包 | S +0.11 | 慢信号低换手族的增益算子 |
| `hump` | SUB +0.18、TO 减半 | **参数不敏感**（0.01–0.05 同效，不需扫参）；但 prod +0.012 |
| `ts_av_diff` vs `ts_zscore` | +41% | 第五次跨族验证 |
| decay | 越小 S 越高；d15/d20 修 SUB | d3 撞 HIGH_TURNOVER；decay 不改善 fitness |
| `ts_delta(·,252)` | 2Y +0.7（T2→T3） | 加速度是 2Y 杠杆但 prod 更高 |

| 禁忌 | 实证 |
|---|---|
| `ts_regression` | 本数据集**全零持仓**（毒算子，勿再试） |
| `truncation` 扫参 | **对秩信号完全无效**（0.02/0.04/0.08 指标逐位相同——`group_rank`+`quantile` 输出有界） |
| TO < 0.01 | 触发 `LOW_TURNOVER` 闸（`numest`/`4wk_chg` 实证出局） |
| delay=0 | `workforce_flow_skills` 报 unknown variable ⇒ 慢数据集无法靠鲜数据提 2Y |
| 日更字段 | TO 结构性爆表（short_interest 实证） |
| 同族连提 | self 互残 0.9+，第 N 颗必被顶爆 |

---

## 三、回测结果及指标

### 3.1 十个 IS 全过候选总表（USA/TOP3000/D1/trunc 0.08，通用设置）

`failed_ra_count=0`（SHARPE/FITNESS/2Y/SUB/TO/CW/MATCHES_PYRAMID 八闸）+ `ppa_failed=false`。

| # | alpha | 机制(T) | neut | 轴 | 窗 | decay | S | F | 2Y | SUB | TO | returns | margin | **prod** | **self** | 状态 |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `npAONOVa` | T2 | RAM | market | 756 | 10 | 1.81 | 1.25 | 1.82 | 0.83 | 0.111 | 5.94% | 10.7bp | 0.6481→**0.7088**⚠ | 0.3861 | 未提交（PC 漂移过线） |
| 2 | `gJWoaJqv` | T3 | RAM | market | 504 | 20 | 1.74 | **1.27** | 2.21 | 0.86 | 0.101 | 6.71% | 13.2bp | 0.6978 | 0.5803 | ✅ **ACTIVE/OS** |
| 3 | `kqJLawqP` | T4 | CROWDING | market | 756 | 10 | 1.61 | 1.11 | 1.62 | 0.84 | 0.096 | 5.98% | 12.5bp | 0.6757 | 0.6445 | ✅ **ACTIVE/OS** |
| 4 | `mLYxaLxp` | T4 | RAM | market | 756 | 10 | 1.76 | 1.20 | 1.64 | 0.84 | 0.114 | 5.83% | 10.3bp | 0.6420 | 0.3992 | 未提交（robustness REJECT） |
| 5 | `xA1mvAmw` | T3 | RAM | sector | 756 | 10 | 1.75 | 1.21 | 2.20 | 0.85 | 0.134 | 6.36% | 9.5bp | 0.6955→**0.9779**⚠ | 0.5577 | 未提交（提交后互残） |
| 6 | `3qjnoddP` | T3 | RAM | sector | 504 | 10 | 1.74 | 1.20 | 2.19 | 0.89 | 0.134 | 6.33% | 9.5bp | 0.6891→**0.9852**⚠ | 0.5541 | 未提交（提交后互残） |
| 7 | `MP056Plk` | T2 | RAM | market | 756 | 20 | 1.73 | 1.19 | 1.83 | 0.75 | 0.086 | 5.94% | 13.9bp | 0.6735→**0.7262**⚠ | 0.3998 | 未提交（PC 漂移过线） |
| 8 | `wp9JopwY` | T2 | RAM | market | 504 | 20 | 1.73 | 1.19 | 1.63 | 0.86 | 0.086 | 5.95% | 13.8bp | 0.6784→**0.7408**⚠ | 0.4152 | 未提交（PC 漂移过线） |
| 9 | `wp9JanRl` | T2 | CROWDING | sector | 756 | 10 | 1.66 | 1.15 | 1.72 | 0.81 | 0.094 | 5.97% | 12.7bp | 0.6877 | →0.941⚠ | 0.5318 | 未提交（self 互残） |
| 10 | `LL5lGgp2` | T2 | CROWDING | market | 756 | 10 | 1.64 | 1.14 | 1.84 | 0.79 | 0.093 | 6.03% | 12.9bp | 0.6819 | →0.942⚠ | 0.5218 | 未提交（self 互残） |

⚠ = 同日重测已过线/互残（**PC 只向上漂**：生产池单调增长，早→晚 +0.01~+0.29；提交 2 颗后同族候选 PC/self 暴涨）。

### 3.2 已提交 2 颗（2026-10-18，ACTIVE/OS）

| alpha | name | F | PC | self | 机制 |
|---|---|---:|---:|---:|---|
| `gJWoaJqv` | USA_R_ANALYST_03 | **1.27** | 0.6978 | 0.5803 | T3 加速度 / RAM / market / 504 / d20 |
| `kqJLawqP` | USA_R_ANALYST_04 | 1.11 | 0.6757 | 0.6445 | T4 秩背离 / CROWDING / market / 756 |

### 3.3 robustness 判定分布（提交前必过，fail-closed）

- **PASS**：`gJWoaJqv`（近3年 1.86/2.27/2.19，均值 2.11）
- **CONDITIONAL**（近3年 CV 0.45–0.46，2023 突强型；软标记已写进 description）：`kqJLawqP`、`wp9JanRl`、`LL5lGgp2`
- **REJECT**：`mLYxaLxp`（近3年 1.05/1.62/1.79，**均值 1.49 < 1.58**）——平台 2Y 过线但内部近 3 窗制更严

### 3.4 判死清单（勿重试）

 Analyst 类别内：breadth 全族（S ≤0.30）、17 配对中非 eps 的 16 个、dispersion 单独用、horizon gap、median−mean、lastactvalue 三级、事件流−共识差、analyst7 全机制、`ts_regression` 毒算子、`numest`/`4wk_chg`（TO<0.01）。
 跨数据集（campaign_20261014）：见 §1.3 六行。

---

## 四、给下一位挖掘者的三句话

1. **USA 分析师族的墙不在 IS 在 prod**——解法是 RAM/CROWDING 中性化，不是磨算子（10 个算子穷尽不如换一次 neutralization）。
2. **提交前夜必须重测 PC**——早上 0.64 的候选下午可能 0.71；且每提交 1 颗，同族候选 PC/self 暴涨（互残 >0.9 放弃）。
3. **base payment 看 fitness + PC，不看 returns**——按 returns 选型是把 OS 特许权使用费的口径错套到 base payment 上。
