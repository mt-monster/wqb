# GBR fundamental72 模板池（Route B 第一波）— 2026-11-02

## 0. 背景与约束

- 目标：Goal「10 个 regular alpha」缺口走 B 路线；fundamental72 = GBR 全库产出率最高选集（205 行 / ra_clean 74 / 36.1% / prod 墙零撞）。
- 模板池纪律：**≥10 个结构互异模板**，差异落在骨架 / 算子几何 / 矩 / 分组轴 / 非线性变换；每条标注来源。
- 数据归属纪律：EV 收益率变化族字段属 fundamental17/fundamental6，**不属于 fundamental72**；本波只用 fundamental72 单集（ATOM，不占两塔配额）。
- 时序归一化纪律：水平型比值因子**禁止** ts_zscore / ts_rank / group_rank（逐股时序归一化抹截面排序）；对「变化量」做时序分位是允许的（EV 族实证）。
- 窗口纪律：252（年）/ 66（季）/ 22（月）；本波主窗 252，S4 二级窗 22。
- 方向纪律：一次只动一个自由度；本波只测骨架 × 机制，方向按文献先验固定，收批归因时再翻。
- 设置档（GBR 实用档）：TOP700 / D1 / neutralization=FAST / decay 15 / truncation 0.05 / nanHandling ON / maxTrade OFF / pasteurization ON / unitHandling VERIFY / FASTEXPR / IS 2014-01-01~2023-12-31。
- 闸线：S ≥ 1.58、F ≥ 1.0、2Y ≥ 1.58、SUB ≈ 0.478×S；判过闸以 `ra_failed_checks == []` 为准。

## 1. 论坛机制先验（本次检索，2026-11-02）

| 机制 | 帖子 | 票数 | 要点 |
|---|---|---|---|
| 现金流含金量 | 现金流从不说谎：fundamental72 核心逻辑浅思 | 29 | 「利润是编出来的，现金流是真金白银」；经营现金流含金量 |
| 应计质量 | 利润和现金流的距离：应计质量的一种观察 | 28 | NI vs OCF 的距离 = 盈利质量；持续利润>现金需警惕 |
| 商誉减值 | 商誉占比高，真正要担心的是什么 | 28 | 商誉/总资产 = 减值风险暴露 |
| A/Q 频率错位 | 季报与年报不要硬拼 | 27 | 年度平滑慢、季度灵敏噪；直接相减有会计周期假象 |
| PIT 时间边界 | 财报不是在披露日之前就存在 | 27 | 公告日/录入日字段可用；披露时点 ≠ 覆盖期 |
| 应收-销售剪刀差 | 收入增长快，应收也跑得快？ | 28 | 应收增长跑赢销售 = 回款恶化 |
| A/Q 镜像与 PIT 时间戳 | 我挖到了一个被严重低估的数据集 | 27 | 1700+ 字段中真正有价值的是 PIT 时间戳与 A/Q 镜像结构 |
| 波动率调整估值偏离模板 | 【Alpha 模版】在CHN中点亮fundamental | 108 | `divide(ts_zscore({f},500), ts_std_dev(ts_zscore({f},63),252))`（CHN 先例） |

⚠ 108 票模板是**逐股时序归一化**结构，与本项目「水平比值禁标准化」实证冲突（EUR ZYQoKRL1 实测 S 1.70→0.45）。
本波不直接照搬；只把它的「波动率调整」思想用在**变化量**上（S4 已含）。

⚠ 【数据集壁垒贴】有人报 fundamental6/risk70/other72 产出差；与 GBR 本地 36% 产出率相反——以本地实测为准（区域差异）。

## 2. 模板池（10 个骨架，结构互异）

约定：`{NI}`=fnd72_s_pit_or_cf_a_cf_net_inc（现金流量表净利润）；`{OCF}`=fnd72_s_pit_or_cf_a_cf_cash_from_oper；
`{SALES}`=fnd72_s_pit_or_is_a_sales_rev_turn；`{WC}`=fnd72_s_pit_or_cf_a_cf_chng_non_cash_work_cap；
`{CAPEX}`=fnd72_s_pit_or_cf_a_cf_cap_expend_prpty_add；`{DA}`=fnd72_s_pit_or_cf_a_cf_depr_amort；
`{INTAN}`=other_intangible_assets_value；`{TAX}`=fnd72_s_pit_or_cf_a_cf_cash_paid_for_tax；
`{EBITDA}`=fnd72_s_pit_or_is_a_ebitda；`{ANN}`=fnd72_s_pit_or_cf_a_announcement_dt；
`{PEND}`=fnd72_s_pit_or_cf_a_latest_period_end_dt_full_record；`{CASHINT}`=fnd72_s_pit_or_cf_a_cf_act_cash_paid_for_int_debt。

| # | 骨架 | 结构轴 | 机制 | 方向先验 | 来源 |
|---|---|---|---|---|---|
| T1 | `subtract(0, rank(ts_mean(divide(subtract({NI},{OCF}),{SALES}),252)))` | 水平比值+年平滑 | 应计/销售（盈利质量） | 高应计=负 | forum 28票 |
| T2 | `subtract(0, rank(ts_delta(divide(subtract({NI},{OCF}),{SALES}),252)))` | 一阶差分 | 应计恶化速度 | 恶化=负 | forum 衍生 |
| T3 | `subtract(0, rank(ts_std_dev(divide({WC},{SALES}),252)))` | 二阶矩 | 营运资本噪音 | 高波动=负 | forum 现金流帖衍生 |
| T4 | `subtract(0, rank(ts_quantile(ts_av_diff(divide({CAPEX},{DA}),252),22,driver=gaussian)))` | 年变化+时序分位（EV 族几何） | 投资周期（CapEx/折旧） | 扩张加速=负（Jensen 过度投资） | 自建（EV 几何迁移） |
| T5 | `subtract(0, rank(divide(subtract({NI},{OCF}),add(abs({NI}),abs({OCF})))))` | 纯截面对称比差（无时序、无分母） | 对称应计 | 高应计=负 | forum 应计帖 |
| T6 | `subtract(0, rank(ts_mean(log(add(divide({INTAN},{SALES}),0.01)),252)))` | 非线性 log（凹变换） | 无形资产负担 | 高负担=负 | forum 商誉帖 |
| T7 | `group_rank(subtract(0,divide({TAX},{EBITDA})),sector)` | 分组轴（行业内） | 现金避税程度 | 避税=正（风险补偿） | 自建 |

⚠ 算子签名教训（2026-11-02 静态闸实拦）：`group_rank(x, group)` **只收 2 个位置参数**，没有 `group=`/`rev=` 命名参数；方向反转用内部 `subtract(0, x)` 实现。
| T8 | `subtract(0, rank(ts_mean(subtract({ANN},{PEND}),252)))` | 日期差算术 | 披露滞后（透明度） | 滞后长=负（质量效应） | forum PIT 帖 |
| T9 | `rank(ts_decay_linear(divide({EBITDA},{CASHINT}),252))` | 衰减加权几何 | 利息保障倍数 | 保障高=正 | 自建 |
| T10 | `subtract(0, rank(ts_arg_max(divide({CAPEX},{DA}),252)))` | 时序位置几何 | CapEx 峰值位置 | 峰值近（扩张中）=负 | 自建 |

结构互异性核对：平滑水平 / 一阶差分 / 二阶矩 / 两层时序分位 / 纯截面比差 / 非线性 log / 分组轴 / 日期算术 / 衰减加权 / 时序位置 —— 10 个骨架两两不同骨架或不同几何。
机制覆盖：应计质量（3 骨架）、营运资本、投资周期（2 骨架）、无形负担、税务、透明度、偿债 —— 9 个机制。

## 3. 方向不确定项（收批归因时重点）

- T7 税负方向文献两可（避税=风险补偿 vs 激进=未来低收益）；本波取「避税=正」。
- T8 披露滞后方向文献两可（SLOO 补偿效应=正 vs 质量效应=负）；本波取负。
- T4/T10 同 CapEx 机制：若两者同向强，归因「投资周期」成立；若背离，骨架差异主导。

## 4. 派发与归因

- 派发：`create_multi_simulation`（10 条一批），GBR 实用档。
- 台账：`upsert_expressions(region=GBR, wave=routeB_f72_w1, dataset=fundamental72, source=manual)`。
- 归因纪律：按模板编号 T1-T10 归因，不按单条 alpha 归因；全灭时先区分「骨架错」与「字段/机制错」。

---

## 5. 第一波收批结果（2026-11-02，multisim `2UkIwQ3yL4kEaDNbP1zuF5S`）—— 10/10 全 REJECT

设置：GBR / TOP700 / D1 / decay 15 / FAST / trunc 0.05。**全部 MATCHES_PYRAMID: PASS**（塔位机制验证通过）。
TO 全落 7.5-8.7% 健康区间（模板 TO 设计目标达成），但信号强度全批不足：

| T | 机制 | alpha | S | F | 2Y | TO | fRA | 判定 |
|---|---|---|---|---|---|---|---|---|
| T1 | 应计水平 | QPvaAPOM | -0.04 | -0.0 | 0.31 | 7.5% | 4 | 死 |
| T2 | 应计差分 | e75OP7Nd | 0.02 | 0.0 | 0.41 | 7.8% | 4 | 死 |
| T3 | 营运资本波动 | leAVYeEl | **0.67** | 0.28 | 0.04 | 8.1% | 3 | 死（S 全批最高） |
| T4 | CapEx 分位 | akKd8keR | 0.11 | 0.02 | 0.50 | 7.5% | 4 | 死 |
| T5 | 对称应计 | d5Wx65YJ | 0.31 | 0.09 | 0.60 | 7.8% | 4 | 死 |
| T6 | 无形负担 log | VkxpLkmJ | **0.63** | 0.27 | 0.72 | 8.2% | 3 | 死（S 次高） |
| T7 | 税负分组 | YP1pOPEA | -0.12 | -0.02 | 0.26 | 7.9% | 4 | 死 |
| T8 | 披露滞后 | akKd8kQR | 0.28 | 0.08 | **1.41** | 8.7% | 3 | 死（2Y 全批最高） |
| T9 | 利息保障 | LLMpwLmv | 0.51 | 0.20 | -0.85 | 8.6% | 3 | 死 |
| T10 | CapEx 峰位 | xArxoAGw | -0.13 | -0.02 | -0.64 | 7.8% | 4 | 死 |

### 归因（按模板族）

1. **纯应计质量族（T1/T2/T5）全灭**（S −0.04~0.31）：应计 anomaly（NI−OCF 口径）在 GBR TOP700 **单信号不成立**——
   与论坛 28 票模板的直觉相反（论坛票数 ≠ GBR 实证）。EBITDA/NI/PIT OCF 的差分与对称比都没有截面区分度。
2. **投资周期族（T4/T10）全灭**（S ≤ 0.11）：CapEx/Assets 的水平、变化、峰位都没有定价。
3. **结构性负担/风险视角是本批最强的两个**：T3（营运资本波动，S 0.67）+ T6（无形负担 log，S 0.63）——
   「这家公司有多脆弱」比「盈利质量好不好」在 GBR 更有区分度。但离 1.58 仍有量级差距。
4. **T8（披露滞后）结构奇特**：2Y 1.41 全批最高（几乎贴 1.58 线）但全期 S 只有 0.28——**远期强、近期弱**。
   PIT 时间戳（t0/t1 差 = 信息透明度）方向值得做二阶变体，但 S 需要 5 倍提升，单靠换窗/换几何不现实。
5. **T7 税负分组全灭**（S −0.12）：`group_neutrank(sector)` 轴上有效税率无区分度。
6. **36% 历史产出率与本波 0/10 的矛盾——已破案（骨架取证 `logs/_f72_hist_top_details.json`）**：
   历史 11 条 S≥1.58 的「f72 相关」达标行真实骨架集中在**两族**，与本波 9 机制零重叠：
   - **融资现金流/总资产 反向比值族**：`reverse(rank(ts_mean(divide(ts_backfill(total_financing_cash_flow,252), ts_backfill(assets_total_2,252)), 252|504)))`
     （78LwQKYx S 1.70 / qMLAdj7V S 1.63 / 6Xdw1OqG vector_neut 变体 S 1.68）。
     ★ 与 2026-11-02 EUR 实证的「融资/资产」家族同源——504 延窗版（qMLAdj7V）在 EUR self=0.6910 过线先验。
   - **模型预测字段族**：`single_bucket_20day_return_estimate_ohlcv_img_2` 当主信号 + f72 字段做 trade_when 门控
     （leA0X7lA S **3.41**/F 2.29/2Y 2.72/SUB 1.94；3qoALER6 S 1.93）。
   - 另有 add 混信号遗留族（qfl_cassie_convention_ocf_currliab + 融资/资产 0.5 权重，hump 三胞胎
     1YNJVzvQ/npv3k8ba/N1NOq7rX/LLMke1xa/P0ovedLE 同指标互相关≈1，只可取一且受「禁 add 混信号」纪律约束）。
   ⇒ **第一波 0/10 不是「f72 没信号」，是 9 个机制完美避开了它的两族真实产线**。

### 判定

- **fundamental72 本波 9 机制单信号验证：全不达标**。按「三波判死」规则这是第 1 波；机制面还有
  历史骨架取证 + 二阶变体两条未走的路，但当前证据下继续在 f72 单信号上加码的期望值低。
- **亮点收割**：T3/T6 的「脆弱性」视角 + T8 的「透明度」视角若要续，应作为**辅助腿**或换区域验证，
  不应继续单信号硬磨。
