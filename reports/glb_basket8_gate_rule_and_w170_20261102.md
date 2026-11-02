# GLB 战役 · 篮内 8 颗全闸通过 + 门控选型第二判据 + w170 NEWS 单塔开波

日期：2026-11-02（GMT+8） / 区域：GLB / D1 / MINVOL1M / 设置格：decay=10、FAST、trunc=0.08、nanHandling=OFF、maxTrade=OFF、maxPosition=OFF

---

## 一、本轮最重要的一件事：确认可提交库存从 6 颗升到 8 颗，且 8 颗**四闸全过**

三颗候选的 prod 实测收尾（后台脚本 `results/glb_w160_prod2.py`，账号级单并发队列）：

| alpha | 门控字段 | 塔组合 | S | F | TO | 2Y | sub | **prod** | prod 直方图 | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| **`leA0X7lA`** | `assets_total_2` | OTHER+FUND | **3.41** | **2.29** | 14.44% | 2.72 | 1.94 | **0.6022** | n[0.6,0.7)=2，≥0.7 全 0 | ✅ |
| **`9qxR097o`** | `ern3_pre_reptime` | EARNINGS+OTHER | 2.56 | 1.50 | 9.55% | 2.72 | 1.32 | **0.6502** | n[0.6,0.7)=9，≥0.7 全 0 | ✅ |
| `mLoqmkd5` | `count_institutional_sellers_security` | INST+OTHER | 2.76 | 1.89 | 13.76% | 2.73 | 2.10 | **0.7694** | n[0.6,0.7)=93，**n[0.7,0.8)=5** | ❌ 拥挤型 |

- `mLoqmkd5` 第一次测到 601s 平台侧未算完（历史首次超时，此前 350–457s），30s 后重跑仅 4s 就命中缓存值 0.7694 ⇒ **超时 ≠ 未测，平台可能已算完，重跑成本几乎是零**。
- `leA0X7lA` 成为至今最强候选（S 3.41 / F 2.29，12 项 checks 全 PASS，仅 `MATCHES_THEMES` / `OSMOSIS_ALLOCATION` 两条 warning），prod 0.6022 还是篮内第二低。

### 8 颗的四闸终态

| # | alpha | 塔组合 | S | F | TO | 2Y | sub | prod | **self(local)** | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `QPvJ6KVw` | RISK+OTHER | 3.19 | 1.59 | 28.97% | 3.43 | 1.84 | 0.6385 | **0.6120** | 0 |
| 2 | `npv9WLVE` | RISK+OTHER | 3.08 | 1.42 | 60.83% | 3.19 | 2.38 | 0.6638 | **0.6644** ⚠ | 0 |
| 3 | `RRE3O8r1` | FUND+OTHER | 2.89 | 1.73 | 16.02% | 2.13 | 1.71 | 0.6479 | **0.4955** | 0 |
| 4 | `d5WqeQbx` | FUND+OTHER | 2.71 | 1.43 | 7.55% | 2.68 | 1.64 | 0.5846 | **0.4597** | 0 |
| 5 | `j2Yg2q9j` | OTHER+SENT | 2.73 | 2.02 | 14.69% | 2.85 | 2.22 | 0.6585 | **0.5520** | 0 |
| 6 | `xArnqeAw` | OTHER+SENT | 2.74 | 1.42 | 21.24% | 2.36 | 1.87 | 0.6335 | **0.4665** | 0 |
| 7 | **`leA0X7lA`** | OTHER+FUND | **3.41** | **2.29** | 14.44% | 2.72 | 1.94 | **0.6022** | **0.5110** | 0 |
| 8 | **`9qxR097o`** | EARNINGS+OTHER | 2.56 | 1.50 | 9.55% | 2.72 | 1.32 | **0.6502** | **0.5596** | 0 |

**闸口覆盖情况**：
- prod 全部 < 0.70 ✅（最高 0.6638，最低 0.5846）
- local self 全部 < 0.70 ✅（最高 0.6644 = `npv9WLVE`，余量仅 0.0356）
- `failed_ra_count` 全部 = 0 ✅
- 候选间互相关（`compute_mutual_correlation`，1023 点，4 年）`max_pair` = `RRE3O8r1 ↔ d5WqeQbx` **0.6741**，`pairs_over_threshold=[]`，`max_mutually_below_subset_size=8`，`max_subset_exact=true` ⇒ **8 颗可整批提交，不需要砍**

### 十年覆盖核查（新增两颗，按「连续多年空窗」判据）

`leA0X7lA` —— **十年全覆盖，零空窗，且每一年的 Sharpe 都 ≥1.58**：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | 4.54 | 4.23 | 4.72 | 4.52 | 2.47 | 2.43 | 2.42 | 4.08 | 3.63 | 1.88 |
| longCount | 4114 | 4206 | 4129 | 4272 | 4737 | 4394 | 4443 | 5204 | 5098 | 4448 |
| pnl | +0.86M | +0.90M | +0.85M | +0.72M | +0.57M | +0.47M | +0.49M | +0.79M | +0.70M | +0.40M |

最弱年 2023 的 S 1.88 仍高于 1.58 基准 ⇒ **这是篮内唯一「每一年都独立达标」的件**，比 `QPvJ6KVw`/`npv9WLVE`（2014 空窗、2015 覆盖薄）扎实一个量级。

`9qxR097o` —— 同样十年无空窗（longCount 3980–5373、pnl 每年为正），但**收益年份分布极不均**：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | **0.75** | 4.64 | 4.87 | 2.43 | 4.45 | 2.24 | **0.41** | 2.95 | 3.84 | 1.51 |
| pnl | +0.24M | +0.80M | +0.76M | +0.28M | +0.70M | +0.29M | +0.06M | +0.53M | +0.58M | +0.21M |

2020 年几乎不赚（+0.06M / S 0.41），2014 与 2023 也偏弱。按用户判据（无连续多年空窗）**通过**，但按稳定性它明显弱于 `leA0X7lA`。保留理由是它与 `leA0X7lA` 的互相关只有 **0.2275**（篮内最正交的一对），分散价值大于其自身强度。

⚠ 两点余量偏薄，提交时必须相邻并读回平台结果：
1. `npv9WLVE` self 0.6644（余量 0.036）+ TO 60.83%（距 HIGH_TURNOVER 70% 仅 9.2 点）双薄；
2. `RRE3O8r1 ↔ d5WqeQbx` 互相关 0.6741（余量 0.026）—— 但两者对现有 OS 池的 self 只有 0.4955 / 0.4597，所以先后提交时对方进池后 max 也只会是 0.6741，仍过。

---

## 二、新规则：门控字段选型的**第二判据** —— 三区域普遍有值

把 w169 八条的 `ra_failed_checks` 逐条从本地库拉出来（此前只看了 `failed_ra_count` 的计数，没看名单），失败项结构高度一致：

| alpha | 门控字段 | 门控类型 | `ra_failed_checks` |
|---|---|---|---|
| `leA0X7lA` | `assets_total_2` | 连续·资产负债表存量 | `[]` |
| `9qxR097o` | `ern3_pre_reptime` | 连续·财报时间戳 | `[]` |
| `N1NO9nRe` | `ern3_all_delay_1_pre_reptime` | 连续·财报时间戳 | `[]` |
| `3qoALER6` | `dividend_per_share_declared` | 半稀疏·分红额（部分市场不派） | LOW_FITNESS, IS_LADDER, **AMER, EMEA** |
| `LLMRJn1a` | `inst18_fundownershipv2_num_held` | 计数·机构持股家数 | LOW_FITNESS, IS_LADDER, **AMER** |
| `LLMRJnp2` | `count_institutional_buyers_security` | 计数·机构买方家数 | LOW_SHARPE, LOW_FITNESS, IS_LADDER, **EMEA, APAC** |
| `RRErWNmn` | `snt22_5neg_mean_420` | 连续但低覆盖(cov 0.69)·情绪 | LOW_SHARPE, LOW_FITNESS, **EMEA, APAC** |
| `qMLXqn62` | `snt22_2neg_conf_low_396` | 同上 | LOW_SHARPE, LOW_FITNESS, **EMEA, APAC** |

**5 条 fRA>0 的，每一条都挂 ≥1 个 `LOW_GLB_<REGION>_SHARPE`；3 条 fRA=0 的一个区域项都没有。**

这里的因果链是清楚的：`trade_when(rank(ts_mean(GATE,22)) > 0.7, ...)` 按门控读数的**横截面高分位**选持仓。如果门控字段本身在 AMER/EMEA/APAC 覆盖不均（机构持仓数据在 EMEA/APAC 稀疏、分红字段在部分市场恒 0、snt22 的 cov 只有 0.69），那 `rank > 0.7` 选出来的子集就会**系统性集中在一两个区域**，区域 Sharpe 立刻失衡。

⇒ **门控字段现在有两条判据，缺一不可：**

| # | 判据 | 反例 | 正例 |
|---|---|---|---|
| ① 拥挤度 | 信号腿位高 `alphaCount` ⇒ 死亡预判；门控腿位 ⇒ 中性 | `dl_riskfree_returns`(22585)、`risk70`(62320) 当信号腿全撞墙 | `fundamental44`(4081)、`risk60`(5583)、`sentiment21`(8672) 当门控全过 |
| ② 区域均衡 | 门控字段必须三区域普遍有值 | `count_institutional_buyers_security`、`inst18_fundownershipv2_num_held`、`dividend_per_share_declared`、`snt22_*` | `assets_total_2`、`ern3_pre_reptime`、`risk60_crowding`、`fnd44_perc_accruals`、`snt21_*` |

**推论**：选门控时先问「这个字段在 EMEA / APAC 有没有值」，而不是先问「这个字段有没有信号」。全球通用的会计存量 / 财报时间戳天然满足；机构持仓、分红、特定情绪打分会天然破坏区域均衡。

### 顺带证伪：`multiply` 不能伪装成降 prod

`mLoqmkd5` 用的是 `multiply(subtract(group_zscore(SIGNAL, exchange), 0.5), rank(ts_mean(count_institutional_sellers_security, 22)))`，与 8 颗的 `trade_when` 只差骨架。结果：

- `trade_when`（把持仓切成稀疏子集）⇒ 8/8 prod < 0.67
- `multiply`（全宇宙持仓、只调权重强弱）⇒ prod 0.7694，直方图 n[0.6,0.7)=93、n[0.7,0.8)=5，是典型**拥挤型**而非单钉子型

⇒ **降 prod 只有一条实测有效的路：让持仓变稀疏。** `multiply` 式弱加权不但不降相关，反而因为满仓而更接近既有 alpha 的 PnL 构造。

---

## 三、组合配额已见底：OTHER 信号腿把所有 OTHER 组合吃满

| 组合 | 已占 | 明细 | 状态 |
|---|---|---|---|
| `RISK+OTHER` | 3/3 | `QPvJ6KVw`、`npv9WLVE`、1 条已死 | **满座** |
| `FUND+OTHER` | 3/3 | `RRE3O8r1`、`d5WqeQbx`、`leA0X7lA` | **满座** |
| `OTHER+SENT` | 3/3 | `j2Yg2q9j`、`xArnqeAw`、`qMLXqn62`(死) | **满座** |
| `INST+OTHER` | 3/3 | `mLoqmkd5`(死)、`LLMRJnp2`(死)、`LLMRJn1a`(死) | **满座**（死件也占位） |
| `EARNINGS+OTHER` | 2/3 | `9qxR097o`、`6Xd8dgzL`(死) | 剩 1 席 |

**结论：靠 OTHER 信号腿再也产不出新 alpha。** 这不是参数问题而是配额结构问题 —— 8 颗全部把 `single_bucket_*_return_estimate_ohlcv_img*`（OTHER 塔）当信号腿，每条都同时吃掉一个 `xxx+OTHER` 组合席。

⇒ 要继续往 20 颗走，**必须换掉信号腿的塔**，这正好回到用户「优先使用不属于 PV/MODEL/OTHER 三类塔的数据集」的指令。w170 因此改走 NEWS 单塔。

---

## 四、w170：NEWS 单塔 10 模板（已派发，multisim `46CKGY8hH4hoa2NOfcFLTgB`）

### 为什么是 NEWS
- `news48` alphaCount **298**、`news73` **337** —— 全 GLB 最低拥挤档（对比已死族 4595–22585）
- 字段级 alphaCount 4–33
- 与 `dl_riskfree`（OTHER）语义完全正交 ⇒ 天然填补 OTHER 之外的信号源
- 同塔不同数据集（news48 实体级 / news73 文章级）⇒ **单塔 `len(combo)==1`，零组合配额**，且规避 `GLB-PURE-SINGLE-TOWER-DEAD` 的同集同源共线

### 10 个结构互异模板（全部 VECTOR，已 `vec_avg`/`vec_max`/`vec_min` 聚合）

| # | 骨架 | 矩 | 表达式 |
|---|---|---|---|
| T1 | 水平反转 | 水平 | `-group_zscore(ts_mean(vec_avg(nws48_nip), 5), country)` |
| T2 | 一阶差分动量 | 一阶 | `group_zscore(ts_delta(vec_avg(nws48_qcm), 5), country)` |
| T3 | 二阶波动惩罚 | 二阶 | `-group_rank(ts_std_dev(vec_avg(nws48_ssc), 22), country)` |
| T4 | 时序分位 | 分位 | `group_zscore(ts_rank(vec_avg(nws48_ens), 66), country)` |
| T5 | 协方差背离 | 协方差 | `-group_zscore(ts_covariance(vec_avg(nws48_ssc), vec_avg(nws48_aes), 22), country)` |
| T6 | 跨字段比值 | 比值 | `group_zscore(divide(vec_avg(nws48_ens), vec_avg(nws48_ssc)), country)` |
| T7 | 条件门控 | 条件 | `trade_when(rank(ts_mean(vec_avg(nws48_ens), 22)) > 0.7, group_zscore(vec_avg(nws48_nip), country), 0)` |
| T8 | 时序 z 分数 | 时序标准化 | `group_zscore(ts_zscore(vec_avg(nws73_globalsent_uncertaintyscore), 66), country)` |
| T9 | 排名差分 | 排名一阶 | `group_zscore(ts_delta(rank(vec_avg(nws48_vea)), 22), country)` |
| T10 | 极值差 | 极值离散 | `group_rank(subtract(vec_max(nws73_globalsent_fearscore), vec_min(nws73_globalsent_fearscore)), country)` |

### 派发前的三道预检（全过）
1. **语法**：`alpha-expression-verifier` 10/10 `valid=true`
2. **字段存在性**：`preflight_expressions` `unknown_fields=[]`、`vector_fields=[]`（已先手动聚合）
3. **算子存在性**：`operator_audit` `safe=true`、`violations=[]`

### 一条单位错误踩坑记录
T6 初版是 `group_zscore(divide(vec_avg(nws48_nip), add(vec_avg(nws48_relevance), 1)), country)` —— `add(字段, 裸常数)` 是已知的 `Unit[]` 硬失败写法（`add(session_market_value,1)` 曾整条 sim ERROR、无 alpha 记录）。虽然 `add(vwap, 0.0001)` 这类只报 WARNING，但**一条错误会连坐整批 10 条**，所以直接换成同量纲比值 `divide(nws48_ens, nws48_ssc)`，彻底不引入常数。

---

## 五、招聘（hiring）机制调研结论 —— 但先别派

按「用机制前先查论坛 + 论文」的纪律，查了论坛与论文：

- 论文源头：**Are Online Job Postings Informative to Investors?**
- 论坛最佳实践（`43322749748503`，92 赞）：`aggregate_open_positions_count` 的 **21 日相对变化** 做行业内排名，`group_rank(if_else(p>0, (a-p)/p, NaN), industry)`，中性化用 **SLOW**（比 INDUSTRY 的 S 1.57 → 2.40）。**加「收入同比为正」的条件反而更差**（S 2.40 → 3.00 是删掉之后）。
- 评论补充：计数类字段用 `vec_sum`，比率/时长效用 `vec_avg`；另一条 EUR 样本用 `bucket_avg_days_job_closed` 的 `vec_skewness` + `ts_corr` + `country` 标准化出 S 2.49。

**但论坛同时明确写了：招聘数据的有效历史集中在 2019—2023（USA），2014—2018 是空白，前段横线来自缺持仓。** 而本轮用户要求「近十年都要有数据」。

⇒ GLB 的 `macro27`（33 个 VECTOR 字段，字段级 alphaCount 仅 5–720，MACRO 塔当前 0 颗）虽然拥挤度极佳、机制扎实，但**历史起点大概率不满足十年覆盖**。按纪律不能直接开波，必须先用一条探针拿到 `get_alpha_yearly_stats` 逐年 `longCount/pnl` 才能判。已登记为待办，不进本轮。

---

## 六、塔位账与提交计划

现有 GLB/D1 塔位：`pv 2 / model 3 / other 3 / risk 1 / institutions 1`，其余 9 座 0（点亮门槛 = 3 颗）。

8 颗提交后（每条同时记入两个塔）：

| 塔 | 前 | 后 | 是否点亮 |
|---|---:|---:|---|
| OTHER | 3 | 11 | 早已亮 |
| **RISK** | 1 | **3** | **✅ 点亮** |
| **FUNDAMENTAL** | 0 | **3** | **✅ 点亮** |
| SENTIMENT | 0 | 2 | 差 1 |
| EARNINGS | 0 | 1 | 差 2 |
| PV / MODEL | 2 / 3 | 不变 | — |
| NEWS / ANALYST / MACRO / SOCIALMEDIA / INSIDERS | 0 | 0 | 未动 |

**日配额 4 颗/天** ⇒ 8 颗需 2 个 ET 日。建议今天先提 4 颗：`QPvJ6KVw`（RISK+OTHER）+ `npv9WLVE`（RISK+OTHER）+ `RRE3O8r1`（FUND+OTHER）+ `leA0X7lA`（FUND+OTHER）—— 这 4 颗一次性点亮 **RISK + FUNDAMENTAL 两座塔**，且天然包含最紧的一对（`RRE3O8r1 ↔ d5WqeQbx` 的另一半留到明天，反而让互相关检查更松）。

---

## 七、下一步

1. **等授权**：8 颗已四闸全过，提交是不可逆动作，需用户明确确认。
2. w170 收批（在飞），按模板归因：哪个骨架族出货、哪个全灭。
3. 若 w170 有骨架出货 ⇒ w171 用该骨架 × 已证门控（`risk60_crowding` / `fnd44_perc_accruals` / `assets_total_2` / `ern3_pre_reptime`）做 NEWS × RISK / NEWS × FUND 组合，这些都是**非 trio × 非 trio**，组合数不限、只受每对 ≤3。
4. 若 w170 全灭 ⇒ 转 `analyst45`(696) / `analyst82`(140) / `analyst_base_ref`(495) 低拥挤 ANALYST 子集，或 `insider_agg_matrix`(2696)。
5. `macro27` 先做覆盖探针再决定，不得跳过年限核查。
