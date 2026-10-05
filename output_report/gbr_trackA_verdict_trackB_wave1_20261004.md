# GBR 战役 · Track A 判定与 Track B 首波设计（2026-10-04）

> 目标：10 颗可提交 REGULAR alpha（用户硬指标，不达标不停）· 不换 region · 不组 SA · 不频繁换数据集
> 当前进度：可提交 **0 / 10** · NEAR_MISS 资产 1（analyst47 顶点族 A1v1MKmW）

---

## 一、Track A：analyst47 顶点族 F 攻坚 —— 判 NEAR_MISS 天花板收手

**multisim `4o1ayAcXh5anaOS7g3aEUob`** · 10/10 完成 · 0 错误 · 设置严格锁顶点族原档
（GBR/TOP700/delay1/decay2/STATISTICAL/trunc0.08/pasteurization ON/unitHandling VERIFY/nanHandling ON/maxTrade ON）

| # | 结构维度 | 表达式核心 | S | F | TO | margin | 2Y | sub | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | trade_when 门控 | `rank(rawexperts)>0.6` | 0.03 | 0.00 | 0.109 | 0.12bp | −0.48 | −0.26 | 全灭 |
| 2 | trade_when 门控 | `rank(rawexperts)>0.4` | −0.03 | −0.00 | 0.118 | −0.12bp | 0.43 | 0.07 | 全灭 |
| 3 | trade_when 门控 | `rank(rawexperts)>0.8` | 0.44 | 0.13 | 0.123 | 1.73bp | −0.08 | 0.29 | 全灭 |
| 4 | trade_when 门控 | `rank(rawalphadecay)>0.5` | −0.04 | −0.00 | 0.116 | −0.21bp | 0.74 | 0.42 | 全灭 |
| 5 | trade_when 门控 | `rank(indicator)>0.7` | 0.60 | 0.19 | 0.133 | 1.96bp | −0.14 | 0.33 | 全灭 |
| 6 | winsorize | `std=2.0` | 1.95 | 0.96 | 0.190 | 4.82bp | 1.75 | 1.30 | 持平略降 |
| 7 | quantile 等价替换 | `quantile(ts_quantile(x,504))` | 1.69 | 0.76 | 0.213 | 4.02bp | 1.24 | 1.01 | **负效应** |
| 8 | group_rank 分组轴 | `group_rank(..., subindustry)` | 0.76 | 0.24 | 0.182 | 2.07bp | 0.97 | 0.89 | 毒药 |
| 9 | 未测字段单因子 | `rawexperts` | 0.55 | 0.14 | 0.203 | 1.23bp | −0.16 | −0.05 | 弱 |
| 10 | 未测字段单因子 | `rawalphadecay` | **−1.38** | −0.60 | 0.173 | −3.73bp | −0.17 | −0.71 | **反向有信号** |

**对照基线（顶点族 A1v1MKmW）**：S 1.96 / F 0.97 / TO 0.1896 / margin 4.85bp / 2Y 1.73 / sub 1.32

### F 杠杆反解（本次核心方法论产出）

WQ BRAIN Fitness 公式：`F = S × √(|Returns| / max(TO, 0.125))`
实测 `returns ≈ margin × TO × 504`（R/(m·TO) = 499–500 恒定）⇒ **`F = S × √(504 × margin)`，turnover 完全约掉**。

- 破 F=1.0 需 **margin ≥ 5.165bp**（当前 4.85bp，需 +6.5%）
- 或 margin 不变则需 **S ≥ 2.0226**（+3.2%）
- margin 4.85bp 同时低于 goal_verdict 硬闸 `Margin>5bp` —— 修 F 即修 margin

**本轮实测最高 margin 4.82bp（winsorize），未达 5.165bp ⇒ F 无法破 1.0。**

### 判定

按 **GLOBAL-LADDER-CEILING-PHENOMENON**（>20 结构性变体仍差 <0.05 即判天花板）：
两轮共 50+ 变体、F 始终卡 0.96–0.97 ⇒ **判 NEAR_MISS，停止微调烧配额**。
顶点族 `A1v1MKmW` 保留为 GBR 最强资产（D4 过线 + prod 干净）。

---

## 二、本轮三条新禁区（已写 registry `GBR-ANL47-SENTIMENT-TSQUANTILE-PINNACLE`）

1. **`trade_when` 事件门控在慢信号上是毒药** —— `ts_quantile(x,504)` 是连续慢信号，门控后 TO 从 0.19 掉到 0.11–0.13（大部分时间空仓），收益被一起切掉。
   ⚠ analyst44 死路里"trade_when 事件门控是 GBR analyst 域最强机制形态"那条经验**只适用稀疏事件型信号，勿外推到慢信号**。

2. **`quantile()` 等价替换在 GBR 是负效应**（S 1.96→1.69）。§1.1 记的 KOR `signed_power→quantile` +0.05 结论**区域特异，禁外推**——等价算子效应必须本区实测。

3. **margin 提升不能靠门控切交易**（会把收益一起切掉），只能靠换信号源 / 换维度。

**意外收获**：`anl47_rawalphadecay` 单因子 S **−1.38**（强反向）——反向后作为新信号并入 Track B（P6）。

---

## 三、Track B：未测族系统性探针 —— 关键纠偏

### 纠偏：差点把已判死的机制当金矿

| 数据集 | 字段数 | 字段真相 | 判定 |
|---|---|---|---|
| `other455` | 1500 | **全是 `oth455_competitor_n2v_*`**（N2V 竞争者关系嵌入的 PCA/kmeans 聚类） | ❌ 已判死机制（`GBR-O455-N2V-PROBE-DEAD`，8 探针 max\|S\| 0.38）的 1500 个变体。**不是 1500 个机会，是 1 个死机制** |
| `analyst44` | 72 | 全是 `anl44_2_*` 预期修正族（EPS/Sales/DPS/EBITDA estimate） | ❌ dead_end 已整族封 |
| `pv30` | 240 | **全是 GROUP 型聚类标签**（`factor1_group*_top800_513` / `sta2_top1200_fact*_c*`） | ✅ 无主信号，但**作 `group_rank` 分组轴是真机会** |
| `insider_matrix` | 33 | `eur_*` 董事/高管显著持股买卖额，`eur_signal_value_2` ac=45 最热 | ✅ 用户绿榜 insiders，未测 |
| `institutions1` | 7 | `inst1_*` 交易明细含 `tradesignificance`(1–3 重要性) | ✅ 未测，cov 0.31 偏低 |
| `analyst48` | 7 | 剩余全是 index 元数据（idivisor/return_code/indx_typ） | ❌ 无信号 |

⚠ **数据口径告警**：`expressions` / `backtest_results` 两表**都不是"已测"的可靠全集**——
`other455` 那 8 探针回测在两表均无记录，只有 dead_end 30 条是判死权威来源。

### 未测候选池（严格过滤后 75 个）

- 绿榜族：analyst **14** · pv **11** · insiders **2**
- 其他族：other **19** · fundamental **8** · risk **5** · institutions **2** · socialmedia **2** · 其余单集若干
- 已剔除：MODEL 全系 · 红榜（chart_patterns / news_sentiment / ai_ml / credit_risk / glb_emotion）· dead 21 集 · 脏名（`_unknown` / `pv/model/other`）

---

## 四、Track B 首波 8 探针（multisim `MI0Of6yO4v9avA121UZuwia`）

**设计原则**：沿用顶点族已实证骨架 `signed_power(ts_quantile(x,504),0.3)`，**只换信号源 / 分组轴**，设置严格控变量（STATISTICAL/trunc0.08/nan ON/maxTrade ON）。

| # | 表达式 | 机制假设 | 维度 |
|---|---|---|---|
| P1 | `signed_power(ts_quantile(eur_signal_value_2,504),0.3)` | 董事显著持股**买入额**（ac45 最热） | insider 主信号 |
| P2 | `signed_power(ts_quantile(subtract(eur_signal_value_2, eur_signal_value_4),504),0.3)` | **净买入**（买 − 卖） | insider 净额 |
| P3 | `signed_power(ts_quantile(eur_top_signal_value_2,504),0.3)` | **高管**显著持股买入额 | insider 高管 |
| P4 | `group_rank(signed_power(ts_quantile(anl47_rawsentiment,504),0.3), factor1_group10_top800_513)` | 顶点骨架换**统计行业聚类轴** | 分组轴几何 |
| P5 | `group_zscore(同上, factor1_group10_top800_513)` | 换算子（group_zscore） | 分组轴几何 |
| P6 | `-signed_power(ts_quantile(anl47_rawalphadecay,504),0.3)` | 本轮发现的反向信号（原 S −1.38） | 顶点族新字段 |
| P7 | `signed_power(ts_quantile(inst1_tradesignificance,504),0.3)` | 机构交易重要性评分（1–3） | institutions 探针 |
| P8 | `subtract(rank(ts_quantile(eur_signal_value_2,504)), rank(ts_quantile(eur_signal_value_4,504)))` | 买卖**分歧度**（rank 差，放行形态） | insider 分歧 |

**轴选择依据**：P4/P5 用 `factor1_group10_top800_513`（"statistically derived **industry** cluster"，替代行业分类）
而非 `sta2_top1200_fact*_c*`（"**return-based**" 收益聚类）——后者与收益信号同源，按 §1.1c「同源兄弟轴必自损」会削掉信号本体。

**三道闸全过**：
- `operator_audit` mode 2 → `safe: true, violations: []`
- 离线 `check_expression` 元数闸 → **8/8 PASS**
- 幽灵算子（18 个）→ **0 违规**

---

## 五、台账口径告警

profile_drift 显示 GBR tier1/tier2 白名单（2026-08-19 生成，**已过期 46 天**）与实际判死严重脱节：
`analyst_earnings_ibes` / `model264` / `news104` / `pattern_scores` / `predictive_starmine` / `pv109` / `shortinterest3` / `dl_riskfree_returns` / `institutions6`
—— 这些仍列 tier1/2，却全在 red/dead 名单。

另有 **24 条** win/dead_end 条目缺 `payload.dataset` 绑定，无法进精确层。

---

## 六、下一步

1. 收割 Track B 首波（`MI0Of6yO4v9avA121UZuwia`），判 8 探针生死（8 探针快判死纪律：max\|S\| <0.5 即判死）
2. 若 insider 族有信号 → 扩批（净买入/分歧度的窗口梯度、分组轴几何）
3. 重建 GBR 白名单（剔除过期 tier1/2 里的 red/dead 项），锁 `s0_whitelist` 台账键
4. 凑齐后走步 8：`brain-alpha-robustness` → `submit_verdict` → **停下报告等确认，绝不自动提交**
