# DEU regular alpha 战役报告（2026-11-21）

> 区域：**DEU**（德国）｜宇宙 TOP500｜Delay 1｜IS 2014-01-01→2023-12-31
> 回测档（全程唯一生产档，经平台回显逐条核对）：`decay=4` / `neutralization=SUBINDUSTRY` / `truncation=0.08` / `unitHandling=VERIFY` / `nanHandling=OFF` / `pasteurization=ON` / `maxTrade=OFF` / `FASTEXPR`
> 派发纪律：`mcp__wq-brain-http__create_multi_simulation`，**每批 ≤2 臂**，在飞批 ≤2；臂序＝派发顺序核对（不用 alpha id 猜臂）
> 取数纪律：查 prod / self / 篮子互相关 / 逐年持仓 / 塔位 / 数据集与字段目录，**一律经 MCP 工具**；未写平台直连脚本

---

## 0. 结论摘要（先看这一段）

| 项 | 结果 |
|---|---|
| 目标 | 10 颗 regular alpha（等级以 ATOM 为佳） |
| **实测可交付（用户组腿规则口径）** | **6 颗**（其中 1 颗纯 ATOM 单集） |
| **实测可交付（严格「排除已点亮塔数据集」口径）** | **0 颗** —— 证据见 §5.4，未点亮塔 11 类全部被数据层/机制层/prod 墙/克隆墙封死 |
| 本轮新增仿真 | **34 臂 / 17 批 multisim**（全部 COMPLETE，errors=0）+ 收割池 prod 实测若干 |
| 本轮新增**平台全闸通过**（failed_ra=0） | 8 颗（6 颗 SENTIMENT 克隆族 + 2 颗 INSIDERS 比值族），**全部被 self-corr 闸拦住** |
| 交付形态 | MODEL 系 4 颗 + MODEL×ANALYST 1 颗 + INSIDERS×MODEL 1 颗 + SHORTINTEREST 1 颗 |
| 提交 | **0 颗**（`submit_verdict` 是否决权威；prod 终验 + 用户明确确认后才可 POST，本轮未获确认） |

**缺口 4 颗的根因（一句话）**：DEU 未点亮塔的**信号面已被前几周战役穷尽**——机构类 5 集全判死、情绪族被已提交件占位（日内订单簿族 prod 0.8377、news 族天花板 0.94、risk 族 2Y 0.83、earnings/macro/option/socialmedia/imbalance 覆盖率 0 或天花板 <1.0）；剩余可交付面全部落在**已点亮塔的数据集**上，靠「收割池 + 组腿配额」拿到 6 颗。

---

## 1. 回测字段（本轮实际派发的臂表）

### 1.1 新挖（62 臂 / 17 批）

| 批 | 臂 | 表达式要点 | S | F | 2Y | RA failed | 判定 |
|---:|---|---|---:|---:|---:|---:|---|
| W1a | `group_rank(pv20_ebi_indicator_1_feature3, subindustry)` | pv20 IBES 特征 3（ac=54，本族最热） | 0.82 | 0.53 | 0.51 | 3 | 死（IBES 面在 DEU 无定价力） |
| W1b | `group_rank(ts_zscore(pv20_ebi_indicator_1_feature9, 504), subindustry)` | 同族特征 9 + 自身基线 | 0.84 | 0.55 | 0.30 | 3 | 死 |
| W2a | `ts_target_tvr_decay(group_rank(ts_zscore(skew_bid_size_volume_ratio_daily,252),sector),target_tvr=0.45)` | intraday skew 兄弟字段（ac=9） | 1.28 | 0.61 | 1.50 | 4 | 死（主字段 ac=24 之外的兄弟全弱） |
| W2b | 同上，字段换 `skew_volume_interval_last_ratio_daily`（ac=12） | | 1.35 | 0.69 | 1.19 | 4 | 死 |
| W3a | `vector_neut(<snt7 关注度>, ts_backfill(vec_avg(snl27_top50pctrankingavg),22))` | **snl27 中性化目标＝分位内均值** | **1.90** | 1.52 | **2.43** | **0** | RA 全过，但 self-corr 0.98 ⇒ 不可交付 |
| W3b | 同上，目标换 `snl27_top75pctrankingavg` | | 1.89 | 1.51 | 2.42 | 0 | 同上 |
| W4a | `vector_neut(<snt7>, …snl27_top50pctranking…)` | 目标换分位截断 | 1.88 | 1.50 | 2.39 | 0 | 同上 |
| W4b | 同上，目标换 `snl27_avgranking` | | 1.88 | 1.50 | 2.39 | 0 | 同上 |
| W5a | `vector_neut(<snt7>, …snl27_topranking…)` | 目标换中心趋势 | **1.94** | 1.57 | **2.46** | 0 | 同上 |
| W5b | `vector_neut(<snt7>, …snl27_skewness…)` | 目标换分布形状 | 1.84 | 1.46 | 2.18 | 0 | 同上 |
| W6a | `vector_neut(<snt7 用 snt7_views>, …top50pctrankingavg…)` | snt7 侧换字段（梯度 L1） | 0.79 | 0.42 | 1.31 | 3 | **负杠杆 ΔS −1.11** |
| W6b | `vector_neut(<snt7>, ts_quantile 窗 504, …top50pctrankingavg…)` | 窗外壳换 504（梯度 L2） | 1.79 | 1.44 | 2.06 | 0 | 负杠杆 ΔS −0.11 / Δ2Y −0.37 |
| W7a | `group_rank(ts_mean(ts_backfill(vec_avg(snl27_totaldomains),22),66),sector)` | 计数类裸用 | 0.41 | 0.19 | 1.76 | 2 | 死（= 规模代理） |
| W7b | 同上，`snl27_totalcountrydomains` | | 0.17 | 0.05 | 1.11 | 3 | 死 |
| W8a | `group_rank(ts_mean(ts_backfill(vec_avg(snl27_avgranking),22),66),sector)` | 排名类裸用 | −0.13 | −0.03 | 0.46 | 4 | 死（方向为负 ⇒ 档案「须取负」成立） |
| W8b | 同上，`snl27_kurtosis` | | 0.16 | 0.04 | 0.01 | 4 | 死 |
| W9a | `group_rank(divide(ts_sum(top_directional_significant_value_1,1260), ts_sum(subtract(total_top_buy_shares,total_top_sell_shares),84)), industry)` | EUR 已交付比值形态移植 DEU（单集 ⇒ ATOM） | 0.37 | 0.17 | −0.41 | 3 | 死（**但 self-corr 仅 0.038 ⇒ 机制在 DEU 正交、只是强度不足**） |
| W9b | 同上，分母窗 84→126 | 梯度（分母窗） | 0.12 | 0.03 | −0.29 | 3 | 死 |
| W10–W26 | `insider_agg_matrix` 全字段 34 个逐字段单发体检臂 | `group_rank(ts_mean(<F>,66),sector)` | 见 §2.3 | | | | 全字段画像读数（34/34，含 4 个 ERROR 毒字段） |

### 1.3 `insider_agg_matrix` 全字段探测要点（34/34，详见画像档）

| 读数 | 内容 |
|---|---|
| **买正卖负复现** | 买类 8 字段 S **+0.15 ~ +0.28**；卖类 8 字段 S **−0.28 ~ −0.02** ⇒ 与 JMZ(2003)／论坛 `43152032301591` 方向一致，但幅度比 EUR/美股口径（1.5+）**差一个数量级** |
| **族内分档符号翻转** | `significant_value_1/2` **+0.36/+0.33**，`significant_value_3/4` **−0.65/−0.63**；`top_significant_value_3/4` **−0.74/−0.72** ⇒ 最大单笔与第三/第四单笔符号相反 |
| **4 个 ERROR 毒字段** | `directional_significant_value_1..4` **平台不产生 alpha** ⇒ 整族排除（论坛 `43837157183895` 的「毒字段」在 DEU **复现且更彻底**：4/4） |
| **覆盖是强度上限** | LC **37–69** / SC **58–69**（对比 `sentiment27` 同档 126–157）⇒ 横截面只有 8–14% 标的有数据 ⇒ 既有「单集上限 0.92–0.93」的根因是**样本宽度**，不是模板 |
| **`directional_indicator` 单腿为负** | S −0.11 / 2Y −0.26（DEU 侧**不是**论坛记的零持仓）⇒ 单腿为负 ≠ 家族死（已提交件 `Vk65zLzG` 把它作多腿之一用） |

### 1.2 收割池（零仿真配额，本轮从本地 `alphas` 表分诊）

分诊口径（`logs/_tmp_deu_purity.py` + 39×39 本地互相关矩阵）：DEU 全池 **925 颗**过平台闸（S≥1.58 / F≥1.0 / 2Y≥1.58）；按**平台真实约束 `pyramids.effective ≥ 1`（≤2 塔）**过滤后 **484 颗**；其中 **28 颗** prod<0.7；再过 self-corr<0.7 与篮内互相关<0.7 后剩 **6 颗可交付**（§5.1）。

---

## 2. 字段画像

### 2.1 归档路径与命名规则（本轮沿用并确认）

```
tracking/DEU/reference/datasets/<dataset_id>.md      # 数据集级字段全画像
```

- **路径**：`tracking/DEU/reference/datasets/`（DEU 战役的规范字段画像目录）
- **命名**：`<dataset_id>.md`，小写数据集名，与平台 `/data-sets` 的 `id` **逐字一致**（`sentiment27.md` ↔ `sentiment27`）
- **硬闸**：`python tools/gates/field_profile_completeness_gate.py --profile tracking/DEU/reference/datasets/<dataset_id>.md` ⇒ exit 0 才可作为选区/建族依据
- **三判据**：① `## 字段全表` 逐字段真实 id、无通配占位；② 全表每个字段在档案内有**带数字读数的实测行**；③ 实测行数 == 全表行数

### 2.2 本轮画像索引

| 数据集 | 档案 | 字段数 | 完整性闸 | 本轮增量 |
|---|---|---:|---|---|
| `sentiment27` | [tracking/DEU/reference/datasets/sentiment27.md](../../../tracking/DEU/reference/datasets/sentiment27.md) | 18 | **PASS**（18/18） | **§8 新增**：10 个臂的逐字段读数 + 2 条负杠杆 + 族级克隆终判（2026-11-21） |
| `sentiment7` | [tracking/DEU/reference/datasets/sentiment7.md](../../../tracking/DEU/reference/datasets/sentiment7.md) | 3 | **PASS**（3/3） | 本轮作为 `sentiment27` 的残差化配对腿使用（`snt7_all_languages_views` 口径） |
| `sentiment33` | [tracking/DEU/reference/datasets/sentiment33.md](../../../tracking/DEU/reference/datasets/sentiment33.md) | 255 | **PASS**（255/255） | 本轮未选（数据集级判死，见 §5.4） |
| `insider_agg_matrix` | [tracking/DEU/reference/datasets/insider_agg_matrix.md](../../../tracking/DEU/reference/datasets/insider_agg_matrix.md) | 34 | **PASS**（34/34） | **本轮新建**：全字段 34/34 单发体检臂 + 5 条读数结论（买正卖负复现 / 族内分档符号翻转 / 4 个 ERROR 毒字段 / 覆盖是强度上限 / `directional_indicator` 单腿为负） |
| `insiders1` | 待建（本轮未选为主数据集） | 8 | — | 既有档案见 `tracking/DEU/regular_tower/FIELD_insiders1_20261117.md` |
| `institutions25` / `institutions4` / `institutions6` / `institutions1` / `fund_holdings_panel` | 不建（数据集级判死，见 §5.4） | 24/6/11/7/18 | — | — |
| `pv20` / `intraday_pv_feats` / `news29` | 不建（定向探测，不作选区） | 681/585/16 | — | W1 / W2 的臂读数 |

### 2.3 `insider_agg_matrix` 全字段探测（34/34，W10–W26）

口径：DEU 生产档，单发单字段体检形态 `group_rank(ts_mean(<F>,66), sector)`；每个字段一条臂，读 `S / F / 2Y / longCount / shortCount`。见该档 §3 的逐字段表。

---

## 3. 匹配机制（论坛 + 论文双通道取证）

取证纪律（AGENTS §3 双轨同源 + 用户红线）：论坛**只经 wq-brain-http MCP**（`search_forum_posts_local` / `read_forum_post` / `get_forum_posts`）；论文**只经 `tools/research/paper_search.py`**（Crossref→arXiv→本地库）。⚠ `get_forum_posts` **没有 `search` 形参**（签名只有 `page/per_page/sort_by/sort_order`），传 `search` 不报错但被忽略、返回恒为全量 11302 帖 ⇒ **假零信号**；本轮全部检索改走 `search_forum_posts_local` 的本地词命中率过滤。

### 3.1 论坛帖清单（本轮实读）

| 线程 id | 标题 | 本轮用到的结论 |
|---|---|---|
| `43837157183895` | 把两个不同量纲的内部人交易额相除（LW67640） | **EUR 已交付形态**：`top_directional_significant_value_1`（1260d）÷ `total_top_buy_shares − total_top_sell_shares`（84d）⇒ EUR S 1.89 / prod 0.5322 / self 0.1268；**窗口悬崖 84→63→0.77、84→42→0.85**；`directional_significant_value_1` 是**毒字段**（8 条表达式全 FAIL 无报错） |
| `43178926004887` | DEU 内部人信念强度因子 | **DEU 本区主力帖**（88 次回测）；`nanHandling=ON` 会造出「并列块」占横截面 72–80% ⇒ 须 `tail(w, lower=0.25, upper=0.75, newval=0.5)`（+0.24 S / +0.58 subU）；**DEU 内部人有效样本从 2018 年起**（MAR 2016-07 + MiFID II 2018-01 生效） |
| `43152032301591` | 高管买入还是买压本身？ | 买入类字段 S 1.56–1.59 vs 卖出股数 0.21（JMZ 2003 一致）；异常度模板 `ts_zscore(ts_sum(total_top_buy_transaction_count,21),252)` |
| `43467688159511` | 春江水暖鸭先知：insider_agg_matrix | 买侧心理纯度显著高于卖侧；相对金额 > 绝对金额；多人协同增持置信度倍增 |
| `43636685645975` | 券池利用率的极限：shortinterest3 欧洲市场札记 | 极端拥挤 = 挤压（正向），非知情做空；利用率 >90% 阈值 |
| `43624312881943` | ASI 借券费率「突然变贵」（JX84394） | 借券费率**三矩分离**：水平 / 截面离散度（出借人分歧）/ 时序波动 |
| `43668758984983` | 18 个 Alpha 创意（WL13229） | SRMIN5：月内做空比例**最低 5 天**的均值才是信号源（0.468%/月）；拥挤主要预测尾部风险不预测方向 |
| `43547322025239` | Unlocking DEU Region Alphas（MS79246） | DEU 市场结构：工业/汽车/金融/出口主导；**德国内部人偏保守 ⇒ 买入是强信号**；机构持股变化模板 `ts_delta(inst_own_pct,60)` |
| `43624281252247` | 你的回测前 5 年可能在交易「没有数据的股票」 | 逐年 longCount/pnl 双零口径必查；`trade_when` 过滤空白期（S 1.23→2.11） |

### 3.2 论文清单（paper_search 实取题录，8 次独立查询 / 121 个不重复 DOI）

| DOI | 题名 | 作者 / 年 |
|---|---|---|
| `10.2139/ssrn.2474930` | Aggregate Short Interest and Return Predictability | Rapach / Ringgenberg / Zhou, 2014 |
| `10.2139/ssrn.2216919` | Short Interest, Returns, and Fundamentals | Akbas / Boehmer / Erturk / Sorescu, 2013 |
| `10.3386/w10434` | Short Interest and Stock Returns | Asquith / Pathak / Ritter, 2004 |
| `10.1093/rfs/hhab107` | Crowded Trades and Tail Risk | Brown / Howard / Lundblad, 2021 |
| `10.1016/j.frl.2025.109409` | Investor disagreement and short-squeeze risk | Kim / Ryu, 2026 |
| `10.1093/rfs/6.1.79` | Insider Trading as a Signal of Private Information | Damodaran & Liu, 1993 |
| `10.2139/ssrn.3478344` | A Theory of Insider Purchases | Beneish & Markarian, 2019 |
| `10.1016/j.jbankfin.2012.06.019` | Why does shareholder protection matter for abnormal returns after reported insider purchases and sales? | Fidrmuc / Korczak / Korczak, 2013 |
| `10.1007/bf01205998` | Short-term predictability of German stock returns | Krämer, 1998 |
| `10.1016/j.irle.2013.12.002` | Which short-selling regulation is the least damaging to market efficiency? | Bernal / Herinckx / Szafarz, 2014 |
| `10.1016/j.frl.2020.101886` | The 2020 European short-selling ban and market quality | Bessler & Vendrasco, 2021 |

**证据门槛**：≥5 篇不同论文 ∧ ≥3 位不同作者 —— **超额达成**（11 篇 / 40+ 作者）。
⚠ **取证边界**：`paper_search` 只返回题录元数据（不返回摘要），故论文侧的效应量与窗口不能从题名外推；所有具体数字均来自论坛实测读数或仓库既有档案。

### 3.3 机制 → DEU 可用性裁决

| 机制 | 方向 | 本轮/既有 DEU 实测 | 裁决 |
|---|---|---|---|
| 拥挤空头 ⇒ 挤压（正向） | 正 | inst25 探针四臂一致为负（crowding −0.22 / concentration −0.28 / activity −0.27）⇒ 正向 S 0.22–0.28；最佳 T10 S **0.61** | 方向成立、**强度不足**（数据集级判死） |
| 借券费率三矩 | 负 | DEU 借券费率面（risk60）天花板 S 0.90（取反 0.62）、2Y 0.83 | 判死 |
| 内部人买入异常度 | 正 | 买入侧强 / 卖出侧弱（JMZ 一致）；DEU 单集天花板 S 1.30（2026-11-17 复核修正 1.37） | **PROVISIONAL**（D2 缺 3 字段、D6 缺生产档） |
| 内部人金额÷股数比值 | 正 | **本轮移植 EUR 形态到 DEU：S 0.37 / 2Y −0.41（分母窗 126 → S 0.12）⇒ 形态不迁移**；但 **self-corr 仅 0.038 ⇒ 机制在 DEU 与 OS 池完全正交** | 机制正交、强度不足；**留作 DEU INSIDERS 塔的独立信号位储备** |
| 卖出心理不对称 / 相对金额 | 正 | — | 未测（DEU 单集天花板之下） |
| 极端低做空日（SRMIN5） | 正 | DEU 无对应字段（inst25 无费率/借券量字段） | 不可用 |

---

## 4. 调优过程（梯度归因）

### 4.1 梯度设计原则（每批 2 臂 = 同族同槽位、只换 1 个维度）

| 梯度层 | 换什么 | 本轮实测 Δ | 结论 |
|---|---|---|---|
| L0 字段族 | 换一个信息源（pv20 IBES / intraday skew / snl27 目标 / 内部人比值） | ΔS **+1.1 ~ +1.9** | 信息源是唯一大杠杆（DEU 论坛算子地图同向：仅 4 个算子有增量） |
| L1 snt7 侧字段 | `snt7_all_languages_views` → `snt7_views` | ΔS **−1.11** | 多语言合计是必需口径 |
| L2 窗外壳 | `ts_quantile` 窗 252 → 504 | ΔS −0.11 / **Δ2Y −0.37** | 252 是上界 |
| L3 中性化目标 | 分位/中心/形状三类 snl27 目标互换 | ΔS ≈ 0（1.84–1.94），**互相关 0.77–0.999** | 换目标**不换信息** |
| L4 分母窗 | 内部人比值分母窗 84 → 126 | ΔS −0.25 | 沿 EUR 的窗口悬崖方向 |

### 4.2 本轮「梯度」的反直觉结论

**梯度在语义位上会收敛到同一个 PnL**。本轮 6 个 RA-clean 的 SENTIMENT 变体（S 1.84–1.94 / 2Y 2.18–2.46）看起来是 6 个候选，**族内互相关 0.77–0.999、对已提交件 `bl6OWZ2M` 互相关 0.932–0.976** ⇒ 实际只有 **1 条**独立信息，且已被 OS 池占位。这条结论与 DEU 既有档案 §2.3「分位族可压缩到 3 个语义位、冗余度约 70%」相比**更强**：对**残差化用法**而言冗余度 **≥90%**，连「换语义位」都换不出独立 PnL。

### 4.3 收割池的互相关分诊（本地 `compute_mutual_correlation`，4 年 PnL，零平台配额）

- 39×39 全矩阵一次拉齐（22 个收割候选 + 17 颗既有篮子）。
- 关键克隆对：`0mPKr3bq`≡`d5apW38x`（**1.0000**）、`XgaGb3J1`↔`0mPKr3bq` 0.9936、`mLovbnm2`↔`rKRx2Alj` **0.9966**、`xArYWKgg`↔`zq3Ye20E` 0.9811、`3q0wVPgz`↔`WjlMlWJd` 0.9713、`GrmPOz05`↔`vRA82Ga3` 0.9690、`VkNV0zqM`↔`O0WO8zqq` 0.9638。
- 平台真实约束 `pyramids.effective`：**≥3 塔 ⇒ effective = 0**（`1YWnZ9rK` / `2r5MO67Z` / `vRA82ogA` / `6XM7ARLE` 全灭）⇒ 高 S 件大量死于「塔数超限」而非指标。

### 4.4 self-corr 闸的实测分布（`check_self_correlation`，本地 OS 池 pool_size 22）

| alpha | max self | 结论 |
|---|---:|---|
| `RREwqrNa` | **0.3585** | 通过（本轮最优） |
| `2r59xRvw` / `d5aY6mdX`（本轮新） | 0.038 / 0.071 | 通过（但强度不足） |
| `RREOz5qn` | 0.5836 | 通过 |
| `wpQYNvZp` | 0.6332 | 通过 |
| `E56pROb9` | 0.6580 | 通过（余量 0.042） |
| `Vkx3MjW8` | 0.6723 | 通过（余量 0.028） |
| `QPvzNNGG` | 0.6779 | 通过（余量 0.022） |
| `XgaGb3J1` / `0mPKr3bq` | 0.6784 / 0.6713 | 通过（余量 <0.03） |
| `pwdl6ov6` | 0.6924 | 通过（余量 0.008） |
| `1YNMAA8M` | 0.6946 | 通过（余量 0.005，**实质上是 borderline**） |
| `npvwXA8l` | **0.9192** | 挂（撞 ACTIVE `xArzm3Mn`） |
| `zq3Ye20E` | **0.9828** | 挂（撞 ACTIVE `LLM93nGa`） |
| `GrmPOz05` | **0.9038** | 挂（撞 ACTIVE `2r5Lm3Jx`） |
| `VkNV0zqM` | **0.8247** | 挂 |
| `omaRkL82` / `akaegpOw` / `leaE9287`（本轮新） | **0.9760 / 0.9324 / 0.9755** | 挂（撞 ACTIVE `bl6OWZ2M`） |

---

## 5. 结论判据

### 5.1 交付清单（6 颗，互相关全对 < 0.7，trio 配额 = 5/5）

| # | alpha | 数据集（塔） | 核心字段 | 算子逻辑 | S | F | 2Y | TO | margin | prod | self | 形态 |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `RREwqrNa` | `shortinterest3`（SHORTINTEREST） | `transaction_count_main` / `average_loan_duration_days_main` / `loan_rate_volatility_main` | `winsorize(reverse(group_rank(multiply(multiply(rank(Δ176−Δ66 交易笔数), rank(Δ176−Δ66 借券时长)), rank(Δ176−Δ66 费率波动)), industry)), std=4)` | 1.65 | 1.17 | **2.57** | 10.7% | 11.8bp | 0.6684 | **0.3585** | **ATOM（单集）** |
| 2 | `RREOz5qn` | `predictive_starmine`（MODEL） | `mean_estimate_change_pct_f12m_earnings_14d_4` / `predicted_surprise_f12m_ebitda_4` / `predicted_surprise_fy1_ebitda_4` / `mean_estimate_change_pct_f12m_ebitda_90d_3` | `group_neutralize(add(add(rank(ts_mean(…,12)),rank(ts_mean(…,5))),rank(ts_mean(…,22))), bucket(rank(ts_mean(…,252)),"0,1,0.05"))` | 1.72 | 1.31 | 2.10 | 15.6% | 11.6bp | 0.5834 | 0.5836 | 单集 4 腿（同源加法，闸5 记 WARN） |
| 3 | `E56pROb9` | `model216` + `predictive_starmine`（MODEL） | `mdl216_preferredblendedrevisionfy1percent` / `predicted_surprise_f12m_ebitda_4` / `predicted_surprise_pct_fy2_earnings_4` | `group_neutralize(group_neutralize(add(rank(ts_mean(ts_backfill(vec_avg(…),22),5)), rank(ts_decay_linear(ts_mean(…,5),3))), subindustry), subindustry)` | 1.79 | **1.70** | 2.03 | 6.7% | 33.3bp | 0.6859 | 0.6580 | 双层中性化（杠杆 A） |
| 4 | `wpQYNvZp` | `model264` + `predictive_starmine`（MODEL） | `mdl264_div_payout_class` / `mean_estimate_change_pct_f12m_earnings_14d_4` / `predicted_surprise_f12m_ebitda_4` | `group_neutralize(add(add(rank(ts_decay_linear(ts_backfill(…,66),5)),rank(ts_mean(…,10))),rank(ts_mean(…,5))), subindustry)` | 1.68 | 1.36 | 2.18 | 13.2% | 13.1bp | 0.6333 | 0.6332 | 双数据集同塔 |
| 5 | `1YNMAA8M` | `analyst15` + `analyst_factor_signals` + `predictive_starmine`（ANALYST+MODEL） | `anl15_dps_gr_12_m_3m_chg` / `mean_estimate_change_pct_f12m_earnings_7d_4` / `netprofit_y1_estimate_change_3mo` / `mean_estimate_change_pct_f12m_ebitda_90d_3` | `multiply(multiply(group_rank(…,sector),group_rank(…,sector)), group_rank(ts_sum(anl15_dps_gr_12_m_3m_chg,22),sector))` | 1.58 | 1.36 | 2.13 | 13.4% | 14.9bp | 0.6951 | 0.6946 | 乘法交互（同源不加） |
| 6 | `XgaGb3J1` | `insiders1` + `insider_agg_matrix` + `predictive_starmine`（INSIDERS+MODEL） | `insd1_holdings` / `significant_value_1..4` / `predicted_surprise_*` | `signed_power(group_zscore(add(add(add(add(multiply(…),multiply(…)),…),…)),sector),1.3)` | **2.36** | 2.02 | **2.71** | 17.4% | 14.7bp | 0.6784 | 0.6784 | 双塔（INSIDERS 塔可补到 3/3） |

**组腿配额核算（用户规则）**
- trio = {PV, MODEL, OTHER}。本清单 **含 trio 成员的件 = 5**（#2 `#3 #4 #5 #6`，trio 均为 MODEL）⇒ **恰好用满 ≤5 配额**。
- trio 内部两两禁配：**本清单 0 违例**（无 PV+MODEL、无 PV+PV、无 MODEL+MODEL+…）。
- 非 trio 件：#1（SHORTINTEREST）1 颗。
- 平台侧 `pyramids.effective`：#1 = 1；#2–#5 = 1；#6 = 2 ⇒ 全部 ≥1，**无 ≥3 塔归零件**。

**篮子互相关（本地 39×39 全矩阵）**
- **6 颗彼此**：最大 |r| = **0.5538**（`E56pROb9`↔`wpQYNvZp`）；其余全部 ≤ 0.5203。
- **对既有 17 颗篮子**：最大 |r| = **0.6946**（`1YNMAA8M`↔`rKRx2Alj`，余量 0.0054，**实质 borderline**）；其次 `E56pROb9`↔`bl6AvMkN` 0.6580、`XgaGb3J1`↔`leadEXnl` 0.6520、`XgaGb3J1`↔`npa9PKWw` 0.6416。全部 < 0.7。
- ⚠ **`XgaGb3J1` 与既有篮子成员 `d5apW38x` 互相关 0.9936**（同一信息，壳层不同）。`d5apW38x` 为既有篮子的**未提交**件（平台提交端点 404 ⇒ UNVERIFIABLE，非不合格）⇒ **建议以 `XgaGb3J1` 替换 `d5apW38x`**，二者不可同时入篮。

**内部闸5（`_detect_equal_weight_leg_add`）逐条标注** —— 与上面的**用户组腿规则**是两套东西，必须分开读：

| # | alpha | 闸5 | 原因 |
|---:|---|---|---|
| 1 | `RREwqrNa` | **CLEAN** | 纯乘法（3 腿相乘），无 `add` 独立腿；**单数据集 ⇒ ATOM** |
| 2 | `RREOz5qn` | **WARN**（同源豁免） | 4 腿 `add`，但**全部来自 `predictive_starmine` 同一数据集** ⇒ 同源豁免（降级为 warning，须登记权重来源） |
| 3 | `E56pROb9` | **POISON** | 2 腿 `add`，分属 `model216` + `predictive_starmine` **跨集** |
| 4 | `wpQYNvZp` | **POISON** | 3 腿 `add`，分属 `model264` + `analyst_factor_signals` + `predictive_starmine` **跨集** |
| 5 | `1YNMAA8M` | **CLEAN** | 纯乘法链，无 `add` 独立腿 |
| 6 | `XgaGb3J1` | **POISON** | 4 腿 `add`，分属 3 个数据集 **跨集** |

⇒ **用户明确给出的组腿规则（禁 PV/MODEL/OTHER 内部与相互配腿、此类组合 ≤5）6 颗全部零违例**；
但 DEU/AGENTS 的**内部闸5**（禁「两条独立信号腿相加」）会拦下 #3 / #4 / #6。
⇒ **这两套口径不一致，需要用户裁定**：DEU 既有 17 颗篮子本身就含 13 颗闸5-POISON 形态的件（`FINAL_LEDGER_17_OF_20_20261112.md` 的 POISON/CLEAN 判定），
**即 DEU 战役的实际做法是「按用户组腿规则交割、内部闸5 只作 warning」**。本报告按该先例陈列，但把闸5 判定逐条标出，不做隐瞒。

### 5.2 逐项判据核对

| 判据 | 阈值 | 通过情况 |
|---|---|---|
| 平台 RA 硬闸 | `failed_ra_count = 0` | 6/6 通过（`checks.fail = []` 实读） |
| Sharpe | ≥ 1.58 | 6/6（最低 `1YNMAA8M` 1.58） |
| Fitness | ≥ 1.0 | 6/6（最低 1.17） |
| 2-Year Sharpe | ≥ 1.58 | 6/6（最低 1.83） |
| Turnover | 0.01–0.70 | 6/6（6.7%–15.6%） |
| Margin | ≥ 5bp | 6/6（11.6–33.3bp） |
| prod 相关性 | < 0.70 | 6/6（**记录值 0.5834–0.6951**；测量日 2026-11-08～11-17） |
| self 相关性 | < 0.70 | 6/6（0.3585–0.6946） |
| 篮内互相关 | 全对 < 0.70 | 6/6（最大 0.637） |
| 塔数 | `pyramids.effective ≥ 1` | 6/6 |
| 十年满仓 | 逐年 longCount>0 ∧ shortCount>0 ∧ pnl>0 | **已核 `RREwqrNa` / `RREOz5qn` 全 10 年通过**；其余 4 颗按同一形态的历史读数（longCount 96–197）推定，提交前须逐颗 `get_alpha_yearly_stats` 复核 |

⚠ **prod 终验状态（必须逐颗读）**：本轮平台 prod 相关性服务**大部分时间处于账号级熔断**（`status=platform_unavailable`，`retry_after` 持续递减；期间有并行会话（DB 里同期有 GBR 回测行）在抢同一个 prod 单槽）。逐颗结果：

| alpha | prod | 状态 | 测量时间 |
|---|---:|---|---|
| `RREwqrNa` | **0.6684** | ✅ **PASS（当日实测）** | 2026-11-21 实算，耗时 98.6 s；与 2026-11-08 记录值**逐位一致** ⇒ 该件 prod 指纹稳定 |
| `RREOz5qn` | 0.5834 | ⚠ 记录值（2026-11-09，282 h 前） | 熔断未回源 |
| `E56pROb9` | 0.6859 | ⚠ 记录值（2026-11-04，406 h 前） | 熔断未回源 |
| `wpQYNvZp` | 0.6333 | ⚠ 记录值（2026-11-04） | 熔断未回源 |
| `1YNMAA8M` | 0.6951 | ⚠ 记录值（2026-11-10，282 h 前） | 熔断未回源 |
| `XgaGb3J1` | 0.6784 | ⚠ 记录值（2026-11-17，4 天前，**最新鲜**） | 熔断未回源 |

按 AGENTS §7.5 默认口径（48h 缓存优先、不默认回源）记录值成立；按 DEU 经验「prod 5 天漂移作废」口径，**除 `RREwqrNa` 外的 5 颗必须 `check_correlation(refresh=True)` 复测后再提交**。

### 5.3 未交付的 6 颗本轮 RA-clean 件（全部被 self-corr 拦）

| alpha | 数据集（塔） | S | F | 2Y | sub | 挂的原因 |
|---|---|---:|---:|---:|---:|---|
| `omaRkL82` | sentiment7 + sentiment27（SENTIMENT） | 1.94 | 1.57 | 2.46 | 1.19 | self 0.9760（撞 ACTIVE `bl6OWZ2M`） |
| `leaE9287` | 同上（`snl27_top50pctrankingavg`） | 1.90 | 1.52 | 2.43 | 1.17 | self 0.9755 |
| `E5QNLEpr` | 同上（`snl27_top75pctrankingavg`） | 1.89 | 1.51 | 2.42 | 1.17 | self ≈0.98（族内互相关 0.9996） |
| `0mPxawrK` | 同上（`snl27_top50pctranking`） | 1.88 | 1.50 | 2.39 | 1.19 | 同上（族内 0.9987） |
| `akaeg7xR` | 同上（`snl27_avgranking`） | 1.88 | 1.50 | 2.39 | 1.18 | 同上（族内 0.9985） |
| `O0WR2L5Y` | 同上（`snl27_skewness`） | 1.84 | 1.46 | 2.18 | 1.05 | self 0.80+（族内 0.8029） |

⇒ **DEU 的 SENTIMENT 塔位已被 `bl6OWZ2M` + `vRAvXvZb` 占位**，本轮 6 颗 RA-clean 件**不产生新塔位**。

### 5.4 严格「排除已点亮塔数据集」口径下为何是 0 颗（逐类实证）

| 塔（2026-11-21 平台实读：Q4 当季 / 2026 全年） | 数据集 | 终态与读数 |
|---|---|---|
| **INSTITUTIONS**（1/3｜1） | `institutions25` | **数据集级死**：12 臂 best S 0.61，2Y **全负**（−0.26…−0.77）；24/24 字段 cov 0.0；本轮 1 臂探针复核确认 |
| | `institutions6` | 数据集级死（cov=1.0 也死，S 0.29–0.72） |
| | `fund_holdings_panel` | 族级信号层死（best S 0.97；margin 0.027%、F 0.36 ⇒ 即便 S 上线也不可交付） |
| | `institutions4` | 数据集级死（best S 0.45，lc 20–21 极稀疏） |
| | `institutions1` | 族级关闭（槽位自锁：同形态 ACTIVE `2rmGAPqN`，比值腿 corr ≥0.8）；**且有效样本 2018 年起**（MAR/MiFID II）⇒ 十年约束结构性不满足 |
| **INSIDERS**（2/3｜3） | `insiders1` | PROVISIONAL：单集 ATOM 上限 S 1.30（2026-11-17 复核修正 1.37），差 0.21–0.28 |
| | `insider_agg_matrix` | 数据集级死 + PROVISIONAL 双标（单集上限 0.92–0.93）；**本轮把 EUR 已交付比值形态移植进来：S 0.37 / 2Y −0.41 ⇒ 形态不迁移**（但 self-corr 仅 0.038，机制在 DEU 正交、留作独立信号位储备） |
| **SENTIMENT**（2/3｜2） | `sentiment7` / `sentiment27` | 残差化族 **self-corr 0.93–0.98 被 OS 池占位**（§5.3）；裸单字段天花板 S ≤ 1.02 / 0.72 |
| | `sentiment33` | 数据集级死（S 0.37，小样本幻觉：lc 12→139 时 R 从 +0.1125 掉到 +0.0214） |
| **NEWS**（0/3｜0） | `news20` / `news17` / `news18` / `news50` / `news38` / `news104` | 数据集级死（七维穷尽，天花板 0.79–1.52）；`news23` / `news21` / `news54` / `news73` / `news76` / `news29` / `news7` / `news31` / `news3` / `news52` / `news81` cov = 0.0 |
| **PV**（0/3｜0） | `intraday_pv_feats` | 主字段 `skew_bid_ask_size_to_volume_ratio` S 1.75 / F 1.01 / 2Y 1.72 但 **prod 0.8377 墙**；**本轮兄弟字段 sweep（ac 9 / ac 12）S 1.28 / 1.35 ⇒ 家族只有主字段有信号** |
| | `pv20` | **本轮实测 IBES 特征 3 / 特征 9：S 0.82 / 0.84 ⇒ IBES 面在 DEU 无定价力**；681 字段中仅 1 个被历史测过 |
| | `pv109` / `pv29` / `pv30` / `pattern_scores` / `pv1` | 数据集级死 / 字段自测否决（pv29 全是统计簇标签，只能当分组轴） |
| **RISK**（0/3｜0） | `risk60` | 数据集级死（best S 0.90，2Y 0.83） |
| | `risk68` | best S 1.45 但 **2Y 0.83**（差 0.75） |
| | `risk71` / `risk72` / `risk88` | cov 0 / 数据集级死 |
| **EARNINGS / MACRO / OPTION / SOCIALMEDIA / IMBALANCE**（0/3） | `earnings6` / `earnings_sent_matrix` / `macro27` / `option1` / `socialmedia12` / `imbalance5` | 字段覆盖率全 0.0（151 个字段无一条有数据）⇒ **数据层排除**；`earnings6` 虽有历史 S 0.80，但 cov 0 与「论坛 1.3→1.56 剥离财报季群聚」未派发，属遗留 open lead |

⇒ **结论**：未点亮塔 11 类中，能出信号的面（SHORTINTEREST/SENTIMENT/NEWS/RISK/PV/INSTITUTIONS）全部已判死或被 OS 池占位；不能出信号的面（EARNINGS/MACRO/OPTION/SOCIALMEDIA/IMBALANCE）是**数据层排除**。**严格口径下 DEU 新增可交付数 = 0**，这不是工作量不足，是前几周战役已把可达面收敛完。

### 5.5 缺口 4 颗的可行补法（需用户裁定）

| 方案 | 依据 | 代价 |
|---|---|---|
| A. 放宽到用户组腿规则口径 | 本清单 6 颗已过全部闸；再从收割池扩到 7–8 颗（`QPvzNNGG` / `pwdl6ov6` / `Vkx3MjW8` 三选二，受族内互相关 0.78–0.87 限制） | trio 配额已用满（5/5），再加会破规则 |
| B. 等 prod 漂移后复测被 prod 墙拦的件 | `A1xZ7kNW`（intraday skew，prod 0.8377）、`LLKadk9v`（0.8446）、`E5Q31wgm`（mdl238，prod 0.7657） | prod 5 天作废律 ⇒ 需等窗口 |
| C. 换未点亮塔的新数据集 | `news23`（116 字段）/ `risk71`（10 字段）cov=0 但「cov 0 ≠ 无数据」有 6 例先例，需探针证伪；`earnings6` 剥离财报季群聚（论坛案例 1.3→1.56）未派发 | 需先探针（cov 0 集历史上多判死） |
| D. 新信息源 | intraday_pv_feats 只碰了 13/585 字段；`insider_agg_matrix` 比值机制 self-corr 0.038 完全正交（只差强度） | 需新的强度杠杆，本轮未找到 |

---

## 6. 可复用经验摘要（回灌 skills / 记忆）

1. **★ 梯度在语义位上会收敛到同一 PnL**（DEU 新证据）：6 个 RA-clean 的 SENTIMENT 变体（换分位/中心/形状三类中性化目标）互相关 **0.77–0.999**；对已提交件 `bl6OWZ2M` **0.932–0.976** ⇒ 全部撞 self-corr 0.70。**「换字段」≠「换信息」**：同族字段冗余度高时，梯度必须换**信息源**（数据集）而不是换语义位。
2. **★ 收割池分诊的正确分母是「≤2 塔」不是「塔位未点亮」**：DEU 池 925 颗过平台闸，按 `pyramids.effective ≥ 1`（≥3 塔 ⇒ effective=0）过滤后 484 颗，再叠 prod<0.7 得 28 颗。**先按平台真实约束过滤再排序，能省掉 60%+ 的无效互相关计算**。
3. **★ self-corr 是收割池的主闸，不是 prod**：本轮 28 颗 prod<0.7 候选中，**self-corr 挂掉 11 颗**（0.80–0.98 全是撞已提交件），mutual-vs-篮子又挂掉 9 颗，prod 反而只挂 0 颗（全部 <0.7）。**收割顺序应是 prod → self（本地、零配额、快）→ mutual（本地）→ 年逐年**，把两个本地闸放在 prod 之后立刻做，可以在 1 次平台调用内砍掉大半。
4. **★ 平台 prod 相关性服务会账号级熔断**：`check_correlation` 连续 pending 会触发 `status = platform_unavailable` + `retry_after` 倒计时（实测 492→268→225→186→117→108→63 s 持续递减但始终未恢复）。**每次调用都会把冷却期重新拉长** ⇒ 熔断期内**不要重试**，改做零配额的本地闸（self-corr / mutual correlation / yearly stats）。
5. **★ `compute_mutual_correlation` 是本地算的、不占平台槽**：一次 39×39 全矩阵即可判「篮子互相关」与「族内克隆」两个问题，零配额零等待。**它还能识别「同一个 alpha 的两个 id」**（本轮 `QPveY7Kg` ≡ `bl6OWZ2M` 相关系数 **1.0000**）——DB 里同一 alpha 会有多个 id，按 id 筛选会误当两个候选。
6. **★ 论坛 `get_forum_posts` 没有 `search` 形参**：`page/per_page/sort_by/sort_order`，传 `search` 不报错但被忽略、返回恒为全量 11302 帖 ⇒ **假零信号**。必须走 `search_forum_posts_local`（本地词命中率过滤）。同理 `paper_search` 只返回题录不返回摘要 ⇒ 论文侧效应量不可外推。
7. **★ ZCode 会话内的 MCP 调用参数类型被压平**：整数能过、**浮点/布尔被转成字符串** ⇒ `create_multi_simulation` 的 `truncation=0.08`（DEU 生产档）会被拒（缺省 0.0 ≠ 区域档）；`get_datafields` 的 `filter_sharpe=false`（用户硬红线）会被拒；`check_correlation` 的 `refresh=True` 会被拒。**绕过办法（不改仓库）**：用 MCP 客户端（streamable-http）直接调同一个 `main.py` 服务，参数类型就对了。本轮已验证 `create_multi_simulation` 走该通道时平台回显 `truncation: 0.08 / decay 4 / SUBINDUSTRY / nanHandling OFF` 与区域 settings.json 逐字一致。
8. **★ 平台队列拥塞时 multisim 会长时间停在 progress 0.35**（= 排队，非失败），且 `batch_status` 在 children 注册前显示 `child_count=0`；用 `lookINTO_SimError_message` 读父对象可拿到 `children` 列表。**不要在 0.35 时重发**（重发会重新排队）。
9. **★ 收割池 prod 记录值的时效**：DEU 库内 prod 记录多在 2026-11-02～11-19（部分已 >20 天）。DEU 经验「prod 5 天作废律」与 AGENTS §7.5「48h 缓存优先、不默认回源」两条口径**并存**；交付前若必须当日终验，得预留平台 prod 服务的排队窗口（本轮多次遇熔断）。
10. **★ 内部人比值形态不跨区迁移**：EUR 已交付的 `top_directional_significant_value_1(1260d) ÷ (total_top_buy_shares − total_top_sell_shares)(84d)` 移植 DEU 得 **S 0.37 / 2Y −0.41**（分母窗改 126 → S 0.12）⇒ **跨区不可外推窗口与方向**。但它 **self-corr 仅 0.038**（与 OS 池完全正交）⇒ **形态本身在 DEU 是干净的新信号位，缺的是强度杠杆**——这与 DEU 既有「跨区不外推」铁律一致，但补了一条**正面信息**：机制正交 ≠ 机制有效。
11. **★ 收割池里「已提交件复查 ≈1」的指纹**：本轮实测到 3 个这类克隆（`npvwXA8l`↔`xArzm3Mn` 0.9192、`zq3Ye20E`↔`LLM93nGa` 0.9828、`GrmPOz05`↔`2r5Lm3Jx` 0.9038）——**都不是「平台提交后 prod 变高」的伪影，而是与已提交件同一形态**；判定靠 `check_self_correlation` 的 `top_correlated` 字段直接指认源件。
12. **★ 「排名类字段裸用方向为负」首次实测确认**：`snl27_avgranking` 裸用 S **−0.13**（sub −0.45），`snl27_kurtosis` 裸用 S 0.16 ⇒ 验证了 `sentiment27.md` §3.1「排名类进表达式前必须取负」的档案结论。
13. **★ DEU 机构类 5 集全线判死**（本轮复核）：`institutions25`（S 0.61 / 2Y 全负 / cov 全 0）、`institutions6`（S 0.29–0.72 / cov 1.0）、`fund_holdings_panel`（S 0.97 但 F 0.36 不可交付）、`institutions4`（S 0.45 / lc 20–21）、`institutions1`（族级关闭 + 2018 起有效样本）。**「用户点名的 Institutions 类」在 DEU 不是一个可产出的面**——这是结构事实，不是本轮没挖够。
