# risk70 · KOR / TOP600 / D1 字段画像

> 类型 MATRIX · 96 字段 · 主体覆盖率 0.967 · 本地 `n_tests=0`（**全字段 UNTESTED**，wave 214 首测）
> 金字塔 category = **risk**（multiplier 1.3，**未点亮塔**）
> 采集：`get_field_catalog(region=KOR, dataset=risk70)`，2026-10-30
> 画像角色：区分「风格载荷」与「残差风险量」，决定 ATOM 单集骨架形态

## 0. 头部字段质量先验（按 alphaCount 降序，同分按 userCount）

| # | 字段 | αC | users | cov | description |
|---|---|---|---|---|---|
| 1 | `rsk70_mfm2_asetrd_anlystsn` | **2546** | 491 | .967 | Analysts' Sentiment Style Factor Loading |
| 2 | `rsk70_mfm2_asetrd_earnyild` | 1537 | 446 | .967 | Earnings Yield Style Factor Loading |
| 3 | `rsk70_mfm2_asetrd_srtindcnt` | 1240 | 176 | .967 | Industry factor loading |
| 4 | `rsk70_mfm2_asetrd_dsrt` | 932 | 193 | .967 | **Specific returns**（= risk72 已判死量） |
| 5 | `rsk70_mfm2_asetrd_resvol` | 920 | 198 | .967 | Residual Volatility Style Factor Loading |
| 6 | `rsk70_mfm2_asetrd_btop` | 758 | 219 | .967 | Book-to-Price Style Factor Loading |
| 7 | `rsk70_mfm2_asetrd_season` | 591 | 85 | .967 | Season Style Factor Loading |
| 8 | `rsk70_mfm2_asetrd_srisku` | 527 | 146 | .967 | Unadjusted initial specific risk（年化 %²） |
| 9 | `rsk70_mfm2_asetrd_earnvar` | 509 | 102 | .967 | Earnings Variability Style Factor Loading |
| 10 | `rsk70_mfm2_asetrd_growth` | 506 | 132 | .967 | Growth Style Factor Loading |
| 11 | `rsk70_mfm2_asetrd_beta` | 475 | 129 | .967 | Beta Style Factor Loading |
| 12 | `rsk70_mfm2_asetrd_invsqlty` | 457 | 105 | .967 | Investment Quality Style Factor Loading |
| 13 | `rsk70_mfm2_asetrd_size` | 456 | 109 | .967 | Size Style Factor Loading |
| 14 | `rsk70_mfm2_asetrd_srisk` | 444 | 127 | .967 | Final specific risk（年化 %²） |
| 15 | `rsk70_mfm2_asetrd_momentum` | 404 | 99 | .967 | Momentum Style Factor Loading |
| 16 | `rsk70_mfm2_asetrd_othermat` | 399 | 116 | .967 | Other Materials Industry Factor Loading |
| 17 | `rsk70_mfm2_asetrd_ltrevrsl` | 386 | 100 | .967 | Long-Term Reversal Style Factor Loading |
| 18 | `rsk70_mfm2_asetrd_cnt_kor` | 385 | 93 | .967 | South Korea Country Factor Loading |
| 19 | `rsk70_mfm2_asetrd_leverage` | 380 | 100 | .967 | Leverage Style Factor Loading |
| 20 | `rsk70_mfm2_asetrd_profit` | 380 | 88 | .967 | Profit Style Factor Loading |
| 21 | `rsk70_mfm2_asetrd_indmom` | 371 | 84 | .967 | Industrial Momentum Style Factor Loading |
| 22 | `rsk70_mfm2_asetrd_midcap` | 367 | 74 | .967 | Midcap Style Factor Loading |
| 23 | `rsk70_mfm2_asetrd_indadj` | 285 | 90 | .943 | Industry factor loading |
| 24 | `rsk70_mfm2_asetrd_divyild` | 266 | 101 | .967 | Dividend Yield Style Factor Loading |
| 25 | `rsk70_mfm2_asetrd_shortint` | 238 | 81 | .967 | Short Interest Style Factor Loading |
| 26 | `rsk70_mfm2_asetrd_cntadj` | 236 | 80 | .943 | Country adjusted factor loading |
| 27 | `rsk70_mfm2_asetrd_earnqlty` | 235 | 76 | .967 | Earnings Quality Style Factor Loading |
| 28 | `rsk70_mfm2_asetrd_strevrsl` | 182 | 62 | .967 | Short-Term Reversal Style Factor Loading |
| 29 | `rsk70_mfm2_asetrd_metals` | 127 | 52 | .967 | Metals Industry Factor Loading |
| 30 | `rsk70_mfm2_asetrd_primaryindustry` | 123 | 54 | .962 | Industry factor loading |

**★ 0.1 读数（关键纠偏）**：头部不是残差风险，而是
`anlystsn`（αC 2546，是第 2 名的 1.7 倍、是 `srisk` 的 5.7 倍）——
**该集最强经济轴 = 分析师情绪风格载荷**，不是本波拟挖的 idiosyncratic-vol 轴。
按 skill 0.1「头部字段 = 该集最强经济轴，若 ≠ 拟挖方向先纠偏」，
wave 214 仍按风险轴探针（理由见 §3），但 **wave 215 必须补 `anlystsn` 轴**。

## 1. 名 vs description 差异（按名分类会漏掉的资产）

| 族 | 名形态 | 实际含义 | 若按名前缀分类的错误 |
|---|---|---|---|
| 风格载荷 25 支 | `rsk70_mfm2_asetrd_<style>` | 个股对**风险模型风格因子**的暴露度（回归载荷），不是该风格指标本身 | 会与 PV/fundamental 的同名指标混为「重复字段」，实际是**正交的载荷口径** |
| 行业载荷 20 支 | `rsk70_mfm2_asetrd_<industry>` | 行业因子载荷，**几乎恒为 1 或 0**（行业哑变量） | 会被当成「信号字段」误用；实际只可作分组轴 |
| 残差风险 3 支 | `srisk` / `srisku` / `resvol` | 年化特异风险 `%²`（srisku=未调整初始，srisk=最终，resvol=风格载荷口径） | 三者**高度相关但不同步**，必须视为同一机制的三档测量，不可当三腿 |
| 残差收益 1 支 | `dsrt` | **Specific returns** | 名不含 risk，极易被当独立 alpha；**实为 risk72 已判死同一个量** |
| 裸名辅件 12 支 | `sector_exposure_*` / `us_equity_*_flag` / `hedge_fund_*` / `*market_cap_usd` / `sector_relative_momentum` | cov 全 1.0，但 **αC 基本 0–8** | 看着「满覆盖」很诱人，实为**纯分组轴/规模轴素材**（市值、行业哑变量、国家哑变量） |

⚠ `sector_exposure_*` 与 `rsk70_mfm2_asetrd_<industry>` 是**同一件事的两种写法**，
但 αC 差 2 个数量级（0 vs 44–399）⇒ 平台用户只认 `rsk70_*` 前缀。

## 2. 字段画像五问

| # | 问 | 答 |
|---|---|---|
| 1 时间维度 | 存量 / 流量 / 变化率 | **存量**：载荷与风险都是**水平量**（每个交易日一个横截面快照）⇒ 铁律 A 只对「单边恒正」的 srisk/resvol 生效；对载荷（可正可负）不适用 |
| 2 相对性 | 水平差异 / 排序差异 | **排序差异**为主：载荷的绝对量级无经济含义，只有横截面相对位置有意义 ⇒ `group_rank` / `group_zscore` |
| 3 被定价的是谁 | 广度 / 强度 | **强度**：风险模型的载荷是「对因子的敏感度」，不是覆盖家数 ⇒ 必须按敏感度排序，不能取变化率 |
| 4 有无博弈 | 拥挤 / 规模 / 可投资性 | **有**：`anlystsn` αC 2546 属极拥挤轴；小市值段风险最高 ⇒ 需规模轴残差化或分组中性化 |
| 5 事件性 | 是否事件稀疏 | **否**：cov .967 连续，逐日更新 ⇒ 禁 `trade_when` 门控（会把连续信号切碎） |

## 3. 预处理决策（B → 骨架）

| 体征 | 决策 |
|---|---|
| cov 0.967（有 3.3% NaN） | `ts_backfill(F, 5)` 前置（缺 NaN 时首个有效值回填 5 日） |
| 载荷可正可负、量级无意义 | 禁裸水平，必须 `group_rank(F, sector)`；粗轴优先（risk59 实证 sector 1.04 > industry .96 > subindustry .70） |
| `srisk` / `resvol` 单边恒正（`%²`） | 铁律 A：裸水平多空需谨慎 → 同时上一档 `ts_delta(F,22)` 变化率作对照实验 |
| 季频 `freq_hint`（`rsk70_mfm2_asetrd_srisk` 本地标注「低频（季/年）」） | 窗口 ≥ 22；若短窗被 NaN 污染取 66/252。**注意**：风险模型载荷实际逐日重估，该 fréqu hint 是启发式猜测，需本波实测验证 |
| 残差风险三兄弟同机制 | **一条腿只出 1 颗**：srisk（主）/ srisku（对照）/ resvol（对照），不叠加 |
| `dsrt` | **排除**：与 risk72 已判死量同源 |
| 行业载荷 20 支 + `sector_exposure_*` | **只作分组轴**，不作信号 |
| `anlystsn` αC 2546 | **本波不碰**（拥挤；且属「修正」类机制，与风险轴不同族），留 wave 215 单独立机制 |

## 4. 机制（A-2 收益来源声明）

**谁在被定价**：韩国散户主导市场中的**彩票偏好者 / 注意力受限投资者**。

**为什么会被错**：高特异波动股票在韩国被当作「彩票」超额追捧（KOSPI/KOSDAQ 1997–2016
实证 IVOL 异象显著；对 beta / 反转 / 动量 / 流动性 / 协偏度 / 特异偏度稳健）；
韩国存在卖空约束与涨跌停制度 ⇒ 套利受限使误价持续。

**错了多久修复**：约 **1 个月至 1 季**（文献常用月度组合；对应窗口 22–66d）。

**预期方向**：高特异波动 ⇒ 后续**低**收益 ⇒ `reverse(rank(srisk))`。
⚠ 铁律 B：`reverse()` 与正向**不精确反号**（截断 × decay × 符号交互）⇒ 正反各测一条。

**Boundary Conditions**：停牌 / 覆盖变更 / 风险模型版本切换（`mfm2` 口径变更）；
韩股涨跌停下 IVOL 被人为截断，极端值可能失真。

### ★ 双通道取证（2026-10-30 完成）

| 通道 | 来源 | 结论 |
|---|---|---|
| **A 论坛** | `search_forum_posts("idiosyncratic volatility")` → `read_forum_post(43607291078935)`《特质波动率之谜：从 risk60 谈谈高风险的陷阱》（29 赞，2026-09-19） | ① 高特质波动股 = 低价/概念/题材股，散户当彩票买 ⇒ **价格被过度高估**；② 机构受风控约束回避 ⇒ **缺乏纠偏买盘**；③ 用法「作为**做空或剔除端**非常有效…直接将排名前 10% 的特质高波标的剔除」；④ ★ **「特质波动容易因单日偶发爆雷瞬间飙升，时序上需做平滑，重点关注持续高波动的标的」** |
| **B 论文** | KOSPI/KOSDAQ 1997–2016 实证 IVOL 异象；JBEF 2019（2000–2016，对 beta/反转/动量/流动性/协偏度/特异偏度稳健）；Pacific-Basin（高 MAX 组负关系更强，市场高波时放大） | 韩国是**已记录强 IVOL 谜题**的市场；方向 = 高 IVOL ⇒ 后续低收益；持有期 ~1 月 |
| **裁决** | **A、B 指向同一机制** | ⭐ 最高优先级组装。**A 提供了 B 没有的关键实现细节：必须先做时序平滑**（否则单日爆雷的瞬时飙升会污染排序） |

**★ 该论坛模板对 wave 214 的直接影响**：wave 214 的 #1/#2 是**未平滑的裸 `ts_backfill(srisk,5)`**
⇒ 正好构成「未平滑 vs 平滑」的**天然对照基线**。
若 wave 214 的裸水平已出正向读数，则 wave 215 直接上
`ts_mean(ts_backfill(srisk,5), 22)` / `ts_decay_linear(...,22)`（**同字段仅窗口差异 ⇒ 单信号多窗平滑，合规**），
并补 `ts_rank` 长窗口径（「持续高波动」= 长窗分位而非瞬时水平）。

## 5. 本波（wave 214）取式与理由

| # | 表达式 | 设计意图 |
|---|---|---|
| 1 | `reverse(group_rank(ts_backfill(rsk70_mfm2_asetrd_srisk, 5), sector))` | 主腿：低特异波动溢价（正向经济方向） |
| 2 | `group_rank(ts_backfill(rsk70_mfm2_asetrd_srisk, 5), sector)` | **铁律 B 对照**：方向反测 |
| 3 | `reverse(group_rank(ts_delta(ts_backfill(rsk70_mfm2_asetrd_srisk, 5), 22), sector))` | **铁律 A 对照**：变化率口径（风险下降 ⇒ ?） |
| 4 | `reverse(group_rank(ts_backfill(rsk70_mfm2_asetrd_srisku, 5), sector))` | 换分子口径：未调整初始特异风险（与最终值的差 = 模型调整幅度） |

设置：KOR/TOP600/D1，STATISTICAL，decay 4，truncation 0.08，2013-01-01→2023-12-31。

## 6. 实测记录

### 6.1 wave 214（8 条，KOR/TOP600/D1，STATISTICAL/decay4/trunc .08）

| # | alpha id | 表达式 | S | F | TO | 2Y | 卡闸 |
|---|---|---|---|---|---|---|---|
| 1 | `9qxP55Vq` | `reverse(group_rank(ts_backfill(rsk70_mfm2_asetrd_srisk,5),sector))` | **0.57** | 0.32 | .0907 | 1.64 | S / F / investability |
| 2 | `P0orLLZq` | `group_rank(ts_backfill(rsk70_mfm2_asetrd_srisk,5),sector)` | **−0.73** | −0.46 | .0904 | −1.88 | S / F / investability |
| 3 | `leA6ww8l` | `reverse(group_rank(ts_delta(ts_backfill(…srisk,5),22),sector))` | −0.04 | 0 | .1738 | 0.08 | 无信号 |
| 4 | `omEwjj6k` | `reverse(group_rank(ts_backfill(rsk70_mfm2_asetrd_srisku,5),sector))` | 0.57 | 0.32 | .0906 | 1.62 | 与 #1 同 |
| — | `88RkWWjq` / `Xg9wZZb8` / `qMLk22xO` / `xArw77bw` | 见 [`other496.md`](other496.md) §6 | | | | | |

**读数**：`srisk`（终版 IVOL）与 `srisku`（原始版 IVOL）**S/TO 到小数点后两位完全一致**（.57/.0907 vs .57/.0906）
⇒ 在本区二者是**同一个量**，不构成两条独立腿。**ΔIVOL 为 null**（S −0.04 / F 0）⇒ 字段只有**水平**信息、
没有变化率信息；铁律 A 的反面实证：对 IVOL 这类**均值回复型水平量**取 `ts_delta` 会直接归零。

### 6.2 ★ 归因（铁律 F，读数先落再决定下一波）

`get_alpha_yearly_stats` 实测 `9qxP55Vq`（正向最好臂）/ `P0orLLZq`（|S| 最好臂）：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | −1.36 | 0.05 | 1.51 | 1.00 | 0.32 | 1.17 | −0.48 | 0.26 | **2.41** | 1.03 |
| longCount | 344 | 339 | 331 | 328 | 314 | 311 | 314 | 308 | 299 | 295 |

| 判据 | 读数 | 结论 |
|---|---|---|
| **S<1.0 年份占比** | **5/10 = 50%**（2014/2015/2018/2020/2021） | ⛔ 2Y 闸**结构性不可达**（实测 2Y 1.64 是靠 2Y 窗口恰好避开 2014/2020；LADDER 仍卡） |
| **单年占正收益** | 正收益年和 ≈ 5,194k，其中 **2022 = 1,638k = 31.5%** | ⛔ 过拟合指纹（>30%） |
| **曲线形态** | 两段深负（2014 −1.36、2020 −0.48）+ 一年独大（2022 2.41） | ⛔ regime 依赖 |
| **十年覆盖（约束 4）** | longCount 295–344，**2014–2023 每年都有** | ✅ PASS |
| **TO** | 0.0907，落在本区获胜带 .075–.136 内 | ✅ 不是换手问题，纯强度不足 |

**裁决（按发波决策表）**：`S<1.0 年份 ≥3 成` + `单年 >30%` 两条同时命中 ⇒
**⛔ 停扫 decay / 平滑 / 门控 / 窗口；必须换机制族**。本字段族**不做第二个参数波**。

### 6.3 方向性结论（本数据集在 KOR 的定性）

- **低 IVOL 跑赢（正向 0.57 / 反向 0.73）** 是**方向正确但强度不足**：S 门槛 1.58、fitness 门槛 1.0，
  实测只有 0.57/0.32 ⇒ 差 2.8× S。**单塔 ATOM 上限验证值 = 0.73**（与路线图实测的 ≤1.02 同量级、更低）。
- **头部字段是「风格暴露」而非「特异风险」**：αC 2546 的 `rsk70_mfm2_asetrd_anlystsn` = *Analysts' Sentiment
  Style Factor Loading*，即该集的主体是 **ATS 风格因子的载荷**，`srisk/srisku` 只是其中一个特异风险量。
  ⇒ 若继续在本集挖，**下一步该打的是「载荷 × 载荷」的结构**（`srtindcnt` αC 1240 / `dsrt` 932 / `resvol` 920），
  而不是 IVOL 水平；但这些载荷都是**拥挤的风格暴露**，prod 相关性风险高（本区已多次撞 0.7 墙）。
- **两段深负正好落在 2014 / 2020**：2014 = KOSPI 低波环境、2020 = COVID 流动性冲击 ⇒
  低波异象在**流动性危机年**失效（教科书结论：低波溢价在 flight-to-liquidity 时反向）。这不是参数问题。

（本文件在本集重新进入「载荷轴」前保持活跃；IVOL 轴已封闭）
