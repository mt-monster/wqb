# DEU pv30 模板池（S1 发波前置产物）

- 区域设置：EQUITY / DEU / TOP500 / delay 1 / SUBINDUSTRY / decay4 / trunc 0.08
- 数据集：pv30（统计行业聚类 / 同业分组）——DEU 实拉画像（2026-11-02）：**285 字段全部 type=GROUP，169 个 ac=0 未测**
- 字段族：`factor{1..4}_group{2,5,10,20,50}_top800_513`（聚类标签，cov 1.0）/ `factor{N}_grouping{K}_score_top{100,200}_eas513`（分数，cov 1.0）/ `{ordinal}_pca_component_top{300,400,600,1200}_group513`（成分暴露，cov 0.13-0.50）/ `pca_factor_score_{0..14}_top{300,800}(_513)` / `principal_component_grouping_method{1..4}_{K}clusters_*` / `sta2_top{400,1200}_fact{1..4}_c{K}` / `top300_factor{N}_group{K}_score` / `robust_factor_{0..2}_top300`
- **★★ 类型错位已实测定性（2026-11-02 P1）**：`rank(pca_factor_score_0_top800_513)` 直接 ERROR——`Incompatible unit for input of "rank": expected "Unit[]", found "Unit[Group:1]"`。平台 Unit 系统**硬拒** GROUP 字段进数值位：score / pca_factor_score / robust_factor 的 "Continuous" 描述全是错配文本，**只能当 group 轴/条件位**。T8/T9/T11 判死，169 个 ac=0 数值面关死；P2（score 当 group 轴）另测。
- 塔归属纪律：pv30 作**分组轴不算腿**；数值腿用内建 returns/close 时为 PV 单塔，不触塔混禁令。若类型探针证明 score 可数值化，含「pv30 数值腿 + PV 腿」的模板须先核 pv30 的 dataset category 再组（trio 禁混仍生效）。
- 拥挤度轴序（优先→回避）：factor2_group50/ac0、factor2_group10/ac1、factor2_group2/ac1、factor1_group2/ac2、factor1_group10/ac4、factor1_group5/ac5 → 回避 factor1_group50/ac58、factor1_group20/ac25、sta2_top400_fact1_c10/ac31。
- 覆盖口径：只用 cov=1.0 的 top800_513 与 eas513 系（TOP500 全覆盖）；top300/400/600/1200 系 cov 0.13-0.50 仅作备选轴。
- 时间窗白名单：1/5/22/66/252/504/1008/1260。12M 动量=252、1M 反转=22 均有论文出处。

## 模板池（12 个，结构互异；差异落点=骨架/算子几何/矩/分组轴/非线性）

| # | 模板 | 表达式骨架 | 机制 | 差异落点 | 来源 |
|---|---|---|---|---|---|
| T1 | 簇内长窗动量 | `group_rank(ts_mean(returns,252), factor2_group50_top800_513)` | 统计同业相对动量；低可见性同业最强、持续 12 个月 | group_rank×水平矩×细簇轴 | 论文：Hoberg-Phillips 2018 (JFQA) + Verdad Peer Momentum |
| T2 | 粗簇短窗反转 | `subtract(0, group_rank(ts_mean(returns,22), factor2_group2_top800_513))` | 行业/同业 1 月反转；粗粒度>细粒度 | 负向×短窗×粗簇轴（与 T1 轴粒度反向） | 论文：Li-Turkington Mapping Momentum + Industry classification and momentum |
| T3 | 同业残差动量 | `group_neutralize(ts_mean(returns,252), factor1_group10_top800_513)` | 剥离簇内共同成分后的个股残差动量 | group_neutralize 残差几何（≠rank 族） | 论文：Hoberg-Phillips peer-relative + 自建 |
| T4 | 双聚类交叉确认 | `multiply(group_rank(ts_mean(returns,252), factor2_group10_top800_513), group_rank(ts_mean(returns,252), factor3_group20_top800_513))` | 两套独立聚类同时认可的「真同业」动量更可靠 | rank×rank 乘积共识×双轴 | 论文：Bonne-Lo AI-Based Peer Grouping（多聚类优于单一分类） |
| T5 | 同业相对低波动 | `subtract(0, group_zscore(ts_std_dev(returns,66), factor2_group20_top800_513))` | 簇内相对波动低者有溢价（低波动异象的同业版） | group_zscore×二阶矩×负向 | 自建（低波动异象 + 簇内相对化） |
| T6 | 波动状态门控动量 | `trade_when(less(group_zscore(ts_std_dev(returns,22), factor2_group50_top800_513), 0.5), group_rank(ts_mean(returns,252), factor2_group50_top800_513), 0)` | 仅在簇内低波动状态持有动量（稀疏路径） | trade_when 稀疏骨架（PnL 路径改变，兼降 self/prod） | 论坛 CH62432（聚类协方差 JPN 模板）+ 自建 |
| T7 | 同业相对尾部风险 | `subtract(0, group_zscore(ts_kurtosis(returns,66), factor1_group10_top800_513))` | 簇内相对厚尾者负alpha（尾部风险惩罚） | kurtosis 高阶矩×group_zscore×负向 | KOR s1_pv30 实证（尾部负向） |
| T8 | 主成分动量 | `rank(ts_delta(pca_factor_score_0_top800_513, 5))` | 行业因子暴露的变化=资金在因子维度上的轮动 | ts_delta 一阶差分×PCA 分数【P1 依赖】 | KOR s1_pv30（主成分动量） |
| T9 | 双成分联动 | `ts_corr(pca_factor_score_0_top800_513, pca_factor_score_1_top800_513, 66)` | 两个行业因子暴露的相关结构变化预警风格切换 | ts_corr 关联矩【P1 依赖】 | KOR s1_pv30（双成分 ts_corr） |
| T10 | 簇内 zscore 截尾 | `tail(group_zscore(ts_mean(returns,252), factor1_group5_top800_513), lower=3)` | 同业最滞后的尾部补涨（信息扩散慢的同业） | tail 非线性截断 | 论坛 XX88140（tail(group_zscore)） |
| T11 | 因子分数水平 | `rank(ts_mean(factor1_grouping20_score_top200_eas513, 22))` | 聚类内生因子分数的水平=统计同业定价偏离 | 平滑水平 rank×分数直用【P1 依赖】 | 自建 + EUR pv30 参考（grouping score 族） |
| T12 | 簇内动量加速度 | `group_rank(ts_delta(ts_mean(returns,252), 22), factor2_group10_top800_513)` | 同业动量的二阶导=趋势强化确认 | 二阶矩（动量的变化）×group_rank | 自建（动量斜率/加速度） |

**模板来源统计**：论文 5（T1/T2/T3/T4/T10 部分）+ 论坛 2（T6/T10）+ KOR 实证 2（T7/T8/T9）+ 自建 4（T3/T5/T11/T12）——覆盖论坛/论文/跨区实证/自建四源。

## 发波前置探针（必跑）

- **P1 类型探针（已跑，2026-11-02）**：`rank(pca_factor_score_0_top800_513)` → ERROR `Unit[Group:1]` 不入 rank。**T8/T9/T11 判死**。替补轴族模板（保持 ≥10 互异）：**T13 簇内动量分歧** `group_std_dev(ts_mean(returns,252), factor1_group10_top800_513)`（簇内分歧大=个股信息主导，来源：自建）；**T14 双轴残差** `group_neutralize(group_rank(ts_mean(returns,252), factor2_group20_top800_513), factor1_group20_top800_513)`（两套聚类的嵌套残差，来源：Bonne-Lo+自建）；**T15 归属不一致门控** `trade_when(not_equal(factor2_group20_top800_513, factor1_group20_top800_513), group_rank(ts_mean(returns,252), factor2_group20_top800_513), 0)`（两聚类归属分歧=分类不确定期，来源：KOR 归属事件门控）。
- **P2 分组轴探针**：`group_rank(ts_mean(returns,22), factor1_grouping20_score_top200_eas513)`——score 字段能否当 group 轴（KOR 口径存疑）。
- **P3 覆盖探针**：TOP500 实际持仓覆盖率核对（field coverage 1.0 是数据面口径，需 1 个小 sim 看实际 longCount）。

## 发波纪律

- 模板池 12 ≥ 10 ✓；归因按**模板族**统计，防「一骨架刷 N 条」伪覆盖。
- 单数据集 atom 优先；pv30+第二数据集组合受塔混禁令约束（trio 互混禁、trio×非trio ≤5 已满）⇒ **本波全走 PV 腿 + pv30 轴/条件的单塔形态**。
- 每模板先发 1 个代表参数（窗口取白名单中位），出信号再扩参数——禁止同族灌水。

## 首波发波记录（2026-11-02）

- 两道预检已过：语法/元数 14/14（T10 修正为 `lower=3` 命名参）+ preflight 字段存在性 `unknown_fields: []`。
- **已入队 7**：T1=`26nZdYgoK5h19mwPaYcVNpi`、T3=`3Lm7DI82Y4sMatAdngp8sZ1`、T4=`cfynPa9i5hH9cJRryMDzZG`、T5=`3ws69S5Li515aPQ1112rHnZ1`、T6=`v483I9EJ4hpbAm1cRsZZPNx`、T7=`41ezJy19F4UwajK1dVNEg4Kt`、T13=`6FzSgehE4ogc7p18WKNJfPG`。
- **并发槽撞车待补发 4**：T10 / T12 / T14 / T15（CONCURRENT_SIMULATION_LIMIT_EXCEEDED，等 60-90s 补发）。
- T2 纯反转按平台 reversion 警告本波跳过；T8/T9/T11 已判死不发。
## 尾批 + 全景归因（2026-11-02 收齐 → 封盘）

- 尾批落地：T12=`leAl5ren`（S −0.09）、T14=`JjeOW1dW`（S 0.74）；**T15 判死**（`not_equal` 拒 GROUP 标签——`Incompatible unit ... Unit[Group:1]`）；T10 连环语法坑（`tail` 四参必须全显式）修正为 **T10v3=`vR1lGbMG`**（`tail(group_zscore(ts_mean(returns,252), factor1_group5_top800_513), lower=-3, upper=99, newval=0)`，WARNING=reversion 放行）。

### 全景读数（10 条全量，2026-11-02 batch_get_alpha_metrics）

| 模板 | alpha | S | F | TO | 2Y | sub | margin | 失败闸 |
|---|---|---|---|---|---|---|---|---|
| T1 簇内长窗动量 | mLoboKlW | 0.79 | 0.57 | 7.5% | 0.23 | 0.63 | 17.3bp | 3 |
| T3 同业残差动量 | Xg9n9N35 | 0.68 | 0.53 | 6.7% | 0.04 | 0.49 | 22.7bp | 3 |
| T4 双聚类交叉确认 | 1YNdNAWX | 0.77 | 0.57 | 6.7% | 0.17 | 0.66 | 20.1bp | 3 |
| T5 同业相对低波动 | LLM1Mmma | 0.12 | 0.04 | 5.9% | 0.33 | 0.00 | 4.9bp | 4 |
| T6 波动门控动量 | 3qoR0rWO | 0.72 | 0.48 | 6.7% | 0.37 | 0.71 | 16.6bp | 3 |
| T7 同业相对尾部风险 | E56E6nEL | 0.73 | 0.46 | 8.5% | 0.45 | 0.11 | 11.6bp | 4 |
| T10v3 簇内截尾 | vR1lGbMG | 0.45 | 0.50 | 15.2% | −0.55 | −0.05 | 25.2bp | 5 |
| T12 簇内动量加速度 | leAl5ren | −0.09 | −0.02 | 19.5% | −0.33 | 0.21 | −0.7bp | 3 |
| T13 簇内动量分歧 | npv2vEZz | −0.06 | −0.01 | 8.2% | −0.80 | −0.42 | −1.0bp | 4 |
| T14 双轴残差 | JjeOW1dW | 0.74 | 0.52 | 7.5% | 0.21 | 0.63 | 16.6bp | 3 |

### 封盘判据与归因

- **判据**：10/10 prescreen REJECT；最高 S=0.79（距闸 1.58 差 2 倍）；2Y 全 ≤0.45；动量族 5 条同形全挤在 0.68–0.79 窄带 ⇒ **机制性弱而非参数问题**，换参数无上台阶迹象。
- **归因**：① 动量族（T1/T3/T4/T6/T14）——TOP500+SUBINDUSTRY 中性化已剥掉子行业共同成分，pv30 统计簇是「第二个行业分类」，重叠剥除后残差信息量不足；② 风险矩族（T5/T7/T12/T13）全灭——二阶/高阶矩在 D1 TOP500 无截面区分度；③ 非线性/门控/截尾族（T10v3、T15）不出货或单位制死。
- **教训记档**：GROUP 字段连 `not_equal` 也拒 ⇒ **GROUP 只能进 group_* 的轴位**，不能进任何算子的数值/比较位；`tail` 四参（lower/upper/newval）必须全显式给值。P2（score 当 group 轴）被族级归因覆盖，不再单独投 sim。
- **结论**：**pv30 分组轴 × PV 腿在 DEU/TOP500/D1 整体不出货，封盘**。拥挤度轴序（factor2_group50/ac0 等）已用尽，本集不再投 sim。
