# GBR NEWS 第二波 `news_light3_2` — 强几何壳 × news50/news104/news20 字段（模板池 v1）

> **动机（对 `news_light3_1` 全灭的归因修正）**：T1–T12 全跑在弱几何壳 `group_rank(<结构>, subindustry)` 上，
> 10/12 已收全 REJECT（S −0.96 ~ 0.40）。而 `template_library_gbr_news_strong_geometry.md` 实证：
> **同类新闻字段弱几何 S 上限 0.91、强几何壳下 S 1.85–2.18**——「N1–N10 全灭」当年就是骨架选错误判成字段没信号。
> 本波把 news50/news104/news20 的字段搬到**强几何壳**上重测，落实「判字段效应固定结构、判结构效应固定字段」的归因纪律。
>
> **与强几何库的分工**：强库测的是 news17/news18（到达率字段池），其 5 条全闸候选 4 条撞 prod 墙/生产池克隆
> （`leA6jmoe` 0.7077 / `wpQwjWn6` 1.0 / `6XdPedNJ` 1.0 / `9qxPX77V` 0.94），只有 `58E7jkaN` 已提交。
> 本波改用 **news50/news104/news20 的冷门字段**（ac 1–10）⇒ 骨架力量 × 破 prod 墙，两头占优。

---

## §0 统一基底（唯一被固定的部分，与强库 §0 逐字一致）

```
G(SIG) = ts_target_tvr_decay(
           group_neutralize(
             -ts_rank(ts_mean(SIG, 60), 252),
             densify(market)),
           target_tvr=0.05, lambda_max=5, lambda_min=0)
```

设置档（GBR D1 news 族现行档，与 news_light3_1 逐项一致）：

```
region=GBR  universe=TOP700  delay=1  language=FASTEXPR
neutralization = FAST      decay = 15      truncation = 0.05
nanHandling = ON   maxTrade = OFF   pasteurization = ON   unitHandling = VERIFY
```

**方向约定**：壳内 `-ts_rank` = 「SIG 高 → 做空」（注意力/密度/量能反转方向）。
弱几何实测方向先验：T10 量能比值 −0.96、T2 到达率 −0.19 与壳方向一致；T3 新颖度 +0.40、T4 情绪 +0.26 与壳相反。
第一轮全用统一方向跑（归因干净）；**出「大幅负号」（|S|≥0.8）的条目才做单条翻向探针**，不批量翻。

---

## §1 十二模板（8 类骨架互异 + 4 条同结构不同字段轴的字段探针）

| # | 结构轴 | `SIG` | 机制 | 来源 | 弱几何先验 |
|---|---|---|---|---|---|
| **U1** | 裸 level（到达率求和） | `vec_sum(mws50_rp_story_event_count)` | 新闻到达率 → 注意力高估反转 | 强库 §4.11 第一性依据（本集是事件到达率数据集） | T2: −0.19 |
| **U2** | 裸 level（强度求和） | `vec_sum(mws50_vea)` | 事件量能强度 | 自建 + 强库 W4 `vec_sum` level 结构 | — |
| **U3** | 长期偏离 `ts_av_diff` | `ts_av_diff(vec_avg(mws50_ess), 252)` | 情绪分长期偏离 → 均值回归 | 强库 S10 结构 + **paper Barber & Odean (2008)** | T4: +0.26（方向与壳相反） |
| **U4** | 乘性置信 `multiply(x, rank(C))` | `multiply(vec_sum(mws50_vea), rank(vec_avg(mws50_ens_similarity_gap)))` | 量能 × 新颖度置信 | 强库 S1 结构 + forum `42659817284375`（novelty 加权已验证）+ 强库 §6.6（新颖度只能进乘子位） | T3: +0.40 |
| **U5** | 同单位比值 `divide` | `divide(vec_sum(mws50_vea), vec_sum(mws50_rp_story_event_count))` | 单事件量能密度（信息集中度） | 强库 S4 结构 + news_light3_1 T10 实测 | **T10: −0.96（本波最大幅度，方向与壳一致）** |
| **U6** | 双源分歧 `subtract(rank, rank)` | `subtract(rank(vec_avg(mws50_ssc)), rank(vec_avg(nws20_multiple_comp_ssc)))` | 双新闻源情绪分歧 → 不确定性溢价 | 强库 S3 结构（修正：跨数据集 + `vec_avg` 保留数值，避开 §6.1 `vec_count` 恒零陷阱） | T7 同集版: −0.21 |
| **U7** | 一阶差分 `ts_delta` | `ts_delta(vec_avg(nws104_marketimpactscore), 22)` | 市场冲击预测变化 | 强库 §4.12 `ts_delta` + news_light3_1 T11 | T11 在测（弱几何） |
| **U8** | 时序标准化 `ts_zscore` | `ts_zscore(vec_avg(nws104_automessage), 252)` | 自动消息异常注意力 | 强库 S6 结构 + **paper Da, Engelberg & Gao (2011)** ASVI 异常 | — |
| **U9** | 长期偏离（冷门浅新闻） | `ts_av_diff(vec_avg(nws104_headlineonly), 252)` | 浅新闻占比偏离 → 注意力过度定价 | 强库 S10 结构 × news104 冷门字段（ac=8） | T12 在测（rank 版） |
| **U10** | 二阶矩协方差 | `ts_covariance(vec_avg(mws50_ssc), vec_sum(mws50_vea), 66)` | 情绪-事件量协动 | 强库 S7 同族二阶矩 + forum `35294898626711` | T5: 0.29 |
| **U11** | 跨集门控 `multiply(x, rank(C))` | `multiply(vec_sum(mws50_rp_story_event_count), rank(vec_avg(nws20_multiple_comp_relevance)))` | 到达率 × 相关度置信 | 强库 X1 结构 + memory wave249（SUB 最强杠杆 +67%） | — |
| **U12** | 二阶矩自相关 | `ts_corr(vec_avg(nws20_multiple_comp_ssc), ts_delay(vec_avg(nws20_multiple_comp_ssc), 5), 66)` | 叙事情绪持续性 | 强库 S7 结构 | — |

**结构互异自检**：裸 level ×2（到达率 / 强度两轴）｜长期偏离 ×2（情绪 / 浅新闻两字段轴）｜乘性置信 ×2（同集新颖度 / 跨集相关度）｜同单位比值｜双源 rank 差｜一阶差分｜时序标准化｜协方差｜自相关。主骨架 8 类互异，4 条重复骨架均为「同结构不同字段轴」的字段探针（强库 N1/N2 同例）。

**字段覆盖（全部 VECTOR，须 vec_* 聚合）**：`mws50_rp_story_event_count` / `mws50_vea` / `mws50_ess` / `mws50_ssc` / `mws50_ens_similarity_gap` / `nws104_marketimpactscore` / `nws104_automessage`(ac=10) / `nws104_headlineonly`(ac=8) / `nws20_multiple_comp_ssc` / `nws20_multiple_comp_relevance`(ac=4)。冷门字段占 5/10 ⇒ 破 prod 墙抓手。

---

## §2 合规声明

| 约束 | 本库处置 |
|---|---|
| 禁止 `add(A,B)` 混信号 | ✅ 零 `add`；合成只有 `multiply(x, rank(C))`（权重恒 1）与 `subtract(rank, rank)`（放行形态） |
| 窗口白名单 | ✅ 只用 5 / 22 / 60 / 66 / 252。60 有「一季度」经济解释 + EUR 三点实测 20<60>120（强库 §1 同例） |
| unit_handling=VERIFY | ✅ U5 比值同单位（count/count）；U6 两侧同为情绪分 rank；无带单位 × 常数 |
| 模板池 ≥10 结构互异 | ✅ 12 条 8 类骨架 |
| 机制前查论坛 + 论文 | ✅ 来源列已标 forum 帖号 / paper；web_search 402 期间用已有文献先验 |
| trio 塔混 | ✅ 全部 NEWS 塔内单塔（news50/news20/news104 同属 NEWS）⇒ 不占两塔配额 |
| 并发 2 | ✅ 6 批 × 2 条串行 |
| 元变量不进信号位 | ⚠ U4/U11 的新颖度/相关度只进乘子位（强库 §6.6）；U3/U9 的偏离是信号本体（ts_av_diff 已实证可作信号，S10 全闸） |

---

## §3 收批账本（待填）

| # | alpha | S | F | 2Y | SUB | TO | failed_ra | 结论 |
|---|---|---|---|---|---|---|---|---|

---

## §4 归因口径

1. 判「字段效应」：U1/U2/U5 对照 news50 到达率/强度轴；U3/U9 对照情绪 vs 浅新闻偏离。
2. 出信号条目（S≥1.2）立即查 `SUB/S`（GBR 线 ≈ 0.478×S）与 prod 预筛（本地筛选器，终验须 refresh=True）。
3. 任何 `longCount==0` 单列（空字段 ≠ 信号弱）。
4. **全灭的判读**：若强几何壳 × news50/104/20 仍全灭，则「骨架修正」假设被证伪，NEWS 点塔改走 news17/news18 未测字段族或判死该方向。
