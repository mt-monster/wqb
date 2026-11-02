# GBR NEWS 第三波 `news_light3_3` — news17 破轴变体 × 未测字段轴（模板池 v1）

> **动机**：`news_light3_1`（弱壳×冷字段）与 `news_light3_2`（强壳×冷字段）均 0/12 全灭；现货盘点后
> news17/18 既有 5 条独立轴（强库 §6.8）**除 E 轴外全部撞 prod 墙或生产池克隆**：
> A 轴 `wpQwjWn6` 1.0 / `j2Yle6q5` 0.8465 / `vR1nAj6z` 与 wpQwjWn6 逐位相同；B 轴 `6XdPedNJ` 1.0；
> C 轴 `leA6jmoe` 0.7077（单钉子，窗口法死刑 n≥1）/ `88R7j2Nz` 0.7212；D 轴 `9qxPX77V` 0.9399。
> **唯一活下来的 E 轴（`58E7jkaN`，prod 0.5611）= 信号 × 元变量交互**——这是全库唯一实证破轴的机制。
>
> **本波设计命题**：prod 墙的根源是**轴被生产池克隆**，不是信号弱（IS 1.85–2.18 都在）。
> 破轴两条腿：① **换字段轴**（news17 未测机制族：分析师修正 / M&A / NLP 技术分歧 / 叙事位置 / 事件时长）
> ——强库 §6.4 实证「字段效应主导轴归属」；② **交互元变量结构**（E 轴机制平移到新轴）。
>
> **缺口**：目标 10 条 regular（最好 ATOM），已备 8 条 ⇒ 本波目标 **≥2 条过闸**。
> NEWS 塔位：`58E7jkaN`（已提交）+ `MPYq0819`（篮内）= 2，本波出 1 条即点亮（3 条一塔）。

---

## §0 统一基底（与强库 §0 逐字一致）

```
G(SIG) = ts_target_tvr_decay(
           group_neutralize(
             -ts_rank(ts_mean(SIG, 60), 252),
             densify(market)),
           target_tvr=0.05, lambda_max=5, lambda_min=0)
```

设置档（GBR D1 news 族现行档）：

```
region=GBR  universe=TOP700  delay=1  language=FASTEXPR
neutralization = FAST      decay = 15      truncation = 0.05
nanHandling = ON   maxTrade = OFF   pasteurization = ON   unitHandling = VERIFY
```

**方向约定**：统一跑壳内 `-ts_rank`（SIG 高 → 做空），第一轮不翻向（归因干净）；
出「大幅负号」（|S|≥0.8）才做单条翻向探针。注意分析师修正机制的文献先验是**顺势漂移**
（Womack 1996 / Bernard-Thomas 1989 ⇒ 高修正 → 后续涨）——若 V1–V3 出负号，与文献一致，
翻向优先级高。

---

## §1 十二模板（11 类骨架互异 + 1 条同骨架不同元变量探针）

| # | 结构轴 | `SIG`（进 G 壳） | 字段轴（机制） | 来源 | 先验 |
|---|---|---|---|---|---|
| **V1** | 裸 level 净额 `vec_sum` | `vec_sum(nws17_multiple_comp_ber)` | **F 分析师修正**（净升级−降级） | **paper Womack (1996) *JF* + Bernard & Thomas (1989)** 修正/盈余漂移；forum「Data Idea 系列3」analyst recommendation 主题 | 未测（ac=3） |
| **V2** | 交互置信 `multiply(x, rank(C))` | `multiply(vec_sum(nws17_multiple_comp_ber), rank(vec_avg(nws17_multiple_comp_event_similarity_days)))` | F × 新颖度 | 强库 S1（E 轴机制）+ forum `42659817284375` novelty 加权 | E 轴实证 prod 0.5611 |
| **V3** | 长期偏离 `ts_av_diff` | `ts_av_diff(vec_sum(nws17_multiple_comp_ber), 252)` | F 偏离 | 强库 S10 结构 + **paper Barber & Odean (2008)** 注意力均值回归 | S10 结构 S 1.93 |
| **V4** | 裸 level 净额（M&A 轴） | `vec_sum(nws17_multiple_comp_bam)` | **G 并购/公司行动情绪** | 自建（ac=4 未测；机制=并购叙事情绪） | 未测 |
| **V5** | 一阶差分 `ts_delta` | `ts_delta(vec_sum(nws17_multiple_comp_qcm), 22)` | **J 高置信语气变化** | 强库 `ts_delta` 结构 + 自建（qcm=BMQ/BEE/BCA 合成高置信，ac=3 未测） | 未测 |
| **V6** | 跨技术分歧 `subtract(rank, rank)` | `subtract(rank(vec_avg(nws17_multiple_comp_ssc)), rank(vec_avg(nws17_multiple_comp_qep)))` | **H 综合 vs 词典分歧** | 自建 + news_light3_2 U6 放行形态（`vec_avg` 保数值，避开 §6.1 恒零） | U6 结构冷字段 0.26 |
| **V7** | 跨实体离散度 `vec_stddev` | `vec_stddev(nws17_multiple_comp_qep)` | **H' 实体间情绪分歧** | 自建 + memory「`vec_stddev` 才对」 | 未测 |
| **V8** | **zscore 壳变体**（幅度保持几何） | G2：`-ts_zscore(ts_mean(vec_sum(nws17_multiple_comp_qcm), 60), 252)` | J（固定字段换几何） | 88R7j2Nz 结构 + §6.3 边界（内层不叠 zscore） | zscore 壳 C 轴 0.7212 |
| **V9** | **稀疏化门控** `trade_when` | `trade_when(rank(ts_mean(vec_avg(nws17_multiple_comp_event_similarity_days), 22)) > 0.7, -ts_rank(ts_mean(vec_sum(nws17_multiple_comp_ber), 60), 252), -1)` 外套 group_neutralize+tvr_decay | F + 新颖度门控 | **memory GLB 8/8 prod<0.67（唯一实测有效降 prod 路径）** + §6.6 元变量进门控位 | 高（降 prod 主武器） |
| **V10** | 实体序位（叙事位置） | `vec_avg(nws17_multiple_comp_rp_story_event_index)` | **I 叙事位置**（主角 vs 配角） | 自建（ac=0 完全未测；机制=首发实体承载主要信息） | 未测 |
| **V11** | 事件时长 `subtract(vec_avg, vec_avg)` | `subtract(vec_avg(nws17_multiple_comp_event_end_time_utc), vec_avg(nws17_multiple_comp_event_start_time_utc))` | **I' 事件持续时长** | 自建（ac=0/1 未测）⚠ 退化风险：多数事件瞬时 ⇒ 恒 0，收批时按 §6.1 口径单列 | 未测 |
| **V12** | 交互置信（分歧元变量） | `multiply(vec_sum(nws17_multiple_comp_ber), rank(vec_stddev(nws17_multiple_comp_ssc)))` | F × 分歧置信 | memory wave249（不确定性进乘子位）+ E 轴机制 | 与 V2 同骨架字段探针 |

**结构互异自检**：裸 level ×2（F/G 两机制轴）｜交互置信 ×2（新颖度/分歧两个元变量探针）｜长期偏离｜一阶差分｜
跨技术 rank 差｜跨实体离散度｜zscore 幅度保持壳｜稀疏化门控｜叙事序位｜事件时长。骨架 11 类互异；
V2/V12 为「同骨架不同元变量」探针（强库 N1/N2 同例）。

**字段覆盖（全部 multiple_comp，cov=0.967 > 0.9 ⇒ 不需要 backfill）**：
`ber`(ac=3) / `bam`(ac=4) / `qcm`(ac=3) / `qep`(ac=10) / `ssc`(ac=12) / `event_similarity_days`(ac=8) /
`rp_story_event_index`(ac=0) / `event_end_time_utc`(ac=0) / `event_start_time_utc`(ac=1)。
**未测字段占 6/9 ⇒ 全新轴（F/G/H/I/J）**，与被克隆的 A/B/C/D 轴字段（relevance/sse/event_relevance/情绪计数）零重叠。

---

## §2 合规声明

| 约束 | 本库处置 |
|---|---|
| 禁止 `add(A,B)` 混信号 | ✅ 零 `add`；合成只有 `multiply(x, rank(C))`（权重恒 1）、`subtract(rank,rank)` 与 `subtract(vec_avg,vec_avg)`（单概念派生量：分歧/时长，非双信号混合） |
| 窗口白名单 | ✅ 只用 22 / 60 / 252。60 有「一季度」经济解释 + EUR 三点实测（强库 §1） |
| unit_handling=VERIFY | ✅ V11 时长两侧同为 UTC 时间戳；V6 两侧同为情绪分 rank；无带单位 × 裸常数 |
| 模板池 ≥10 结构互异 | ✅ 12 条 11 类骨架 |
| 机制前查论坛 + 论文 | ✅ 来源列已标 forum/paper；forum 已检（Data Idea 系列3「analyst recommendation and news sentiment」主题命中）；web_search 402 期间用既有文献先验 |
| trio 塔混 | ✅ 全部 news17 单数据集 ATOM ⇒ 不占两塔配额 |
| 元变量不进信号位 | ✅ 新颖度/分歧只进乘子位与门控位（§6.6）；V7 的 `vec_stddev` 是信号本体（跨实体分歧是方向性风险概念，非元变量） |
| 慢矩不套双层平滑壳 | ✅ 全部模板为水平/差分/偏离/离散度类，无 ts_covariance/ts_corr |
| 归因纪律（一次动一个自由度） | ✅ V1↔V3↔V2 = 同字段轴 F 三结构对照；V5↔V8 = 同字段 J 两几何对照；V2↔V12 = 同结构两元变量对照 |

---

## §3 收批账本（2026-11-02 收批，0/12 全 REJECT）

批 1 `3xUzYG1cz4J5bNVcwMOHrDP`（V1–V6）/ 批 2 `1Tp8277hT4xzavc14xxATOOQ`（V7–V12）；
GBR/TOP700/D1/decay15/trunc0.05/nan ON/maxTrade OFF。闸线 S 1.58 / F 1.0 / 2Y 1.58。

| # | 模板 | alpha | S | F | 2Y | SUB | TO | failed_ra | 结论 |
|---|---|---|---|---|---|---|---|---|---|
| V1 | 裸 level 净修正（ber） | QPva2rwX | 0.38 | 0.10 | −0.36 | 0.43 | 0.076 | 3 | REJECT |
| V2 | 修正×新颖度交互 | WjOpawvN | 0.19 | 0.04 | −1.43 | 0.50 | 0.081 | 3 | REJECT |
| V3 | 修正偏离（ts_av_diff 252） | kqN31kzg | **0.45** | 0.13 | −0.39 | 0.46 | 0.075 | 3 | REJECT（全波最高） |
| V4 | M&A 情绪（bam） | 2rA7aq36 | 0.14 | 0.02 | 0.06 | 0.37 | 0.084 | 3 | REJECT |
| V5 | qcm 22 日差分 | RREp2qJj | **−0.60** | −0.21 | −1.18 | −0.33 | 0.079 | 4 | REJECT（全波最大 \|S\|） |
| V6 | ssc−qep 跨技术分歧 | Vkxp2qvw | 0.07 | 0.01 | 0.27 | 0.19 | 0.071 | 3 | REJECT |
| V7 | qep 实体离散度（vec_stddev） | pwd6VOR6 | 0.13 | 0.02 | 0.30 | 0.22 | 0.075 | 3 | REJECT |
| V8 | zscore 壳×qcm | 78Lwa9NL | 0.11 | 0.02 | −0.61 | 0.24 | 0.081 | 3 | REJECT |
| V9 | trade_when 稀疏化（降 prod 主武器） | vR1LegrG | 0.04 | 0.00 | −0.30 | −0.15 | 0.075 | 4 | REJECT |
| V10 | 叙事序位（rp_story_event_index） | LLMpgJN2 | −0.32 | −0.08 | −1.12 | −0.19 | 0.073 | 4 | REJECT |
| V11 | 事件时长（end−start） | 1YN7aEXM | −0.20 | −0.05 | −0.23 | −0.28 | 0.149 | 4 | REJECT |
| V12 | 修正×分歧交互 | 88Rza1Po | 0.20 | 0.04 | −0.78 | −0.02 | 0.078 | 4 | REJECT |

- V11 longCount 正常（TO 0.149 偏高因时长字段跳变），**计入模板试错数**，无 §6.1 退化豁免。
- 全部条目 2Y 为负或远低于 1.58；无一条接近 near 线 1.2 ⇒ prod 未测（省配额），破轴判定不适用（IS 已死）。

---

## §4 归因口径

1. **破轴判定**：新候选先跑 prod 实测（本地缓存优先）；prod<0.7 且直方图 n([0.7,0.8))=0 才算破轴成功。
2. **字段轴归因**：V1/V3/V2 同轴 F 对照三结构——若三者 prod 相近 ⇒ F 轴本身决定，结构无效（§6.9 同款）；
   若 V2 低于 V1 ⇒ 交互元变量再次实证破轴。
3. **结构归因**：V5 vs V8（同字段 qcm：delta vs level×zscore 壳）；V2 vs V12（同结构：新颖度 vs 分歧元变量）。
4. V11 若 longCount=0 ⇒ 单列「退化」不计入模板试错数（§6.1 口径）。
5. 出信号条目（S≥1.2）立即查 SUB/S（GBR 线 ≈ 0.478×S）与 self 互相关（vs `58E7jkaN` / `MPYq0819` 重点）。
6. **全灭判读**：若 F/G/H/I/J 新轴 × 强壳仍全灭 ⇒ news17 剩余机制面穷尽，转 news20/news104 交互破轴版或判死 NEWS 线补塔（改用其它塔凑 10 条）。**已兑现（§6）**。

---

## §6 归因定稿（2026-11-02，0/12 全灭后）

### 6.1 交互元变量不是普适破轴杠杆（本波最重要负结果）

E 轴 `58E7jkaN`（信号×元变量交互，prod 0.5611）是唯一实证破轴成功案例，但同结构平移到 ber 轴即失效：
V2（修正×新颖度）S 0.19 **低于** V1 裸 level 0.38；V12（修正×分歧）0.20 同样折半。
⇒ **交互的成功取决于字段对本身的信息互补，不是结构可复制的杠杆**。E 轴的元变量（成交/流动性类）
与主信号互补；而 novelty/ssc 与 ber 同源（都在同一新闻事件流上），交互只引入噪声。
**推论**：「信号×元变量」只能作为候选武器逐对实测，不能当默认骨架批量铺。

### 6.2 分析师修正轴（ber）天花板 0.45，判死

V1 0.38 / V2 0.19 / V3 0.45 / V9 门控版 0.04 —— 四种结构同轴全灭。V3（偏离形式）最优但仅为闸线 28%。
Womack 1996 顺势漂移在 GBR TOP700 D1 不成立（大盘股 D1 内已被定价；修正信息无截面区分度）。

### 6.3 trade_when 稀疏化杀信号（GLB 记忆的边界条件）

V9（S 0.04）vs V1（S 0.38）：门控条件 `rank>0.7` 只留 30% 交易日，而信号是 60/252 慢矩，
被门控切成碎片。**GLB 8/8 降 prod 成立的前提是 IS 信号本身 ≥1.5**；信号 0.38 时稀疏化只留噪声。
降 prod 主武器对弱信号无效——先有信号才谈降相关。

### 6.4 未测字段轴一次性全灭（bam/qcm/qep/ssc/rp_story_event_index/event duration）

| 轴 | 最优条目 | S | 判定 |
|---|---|---|---|
| ber 分析师修正 | V3 | 0.45 | 死 |
| bam M&A | V4 | 0.14 | 死 |
| qcm 高置信语气 | V5 | −0.60 | 死（\|S\|<0.8 不烧翻向，机制级弱不加码纪律） |
| qep 词典情绪 | V7 | 0.13 | 死 |
| ssc 技术分歧 | V6/V8 | 0.11 | 死 |
| rp_story_event_index 叙事序位 | V10 | −0.32 | 死 |
| event duration 时长 | V11 | −0.20 | 死 |

V5 负号 0.60 未达翻向探针线（0.8）；qcm 差分方向与「高置信负面语气→价格下行」一致但幅度不足。

### 6.5 news17 机制面穷尽判定（三波总账）

news_light3_1（弱壳 12 条）+ news_light3_2（强壳 12 条）+ news_light3_3（破轴 12 条）= **36 条全 REJECT**，
全波最高 S 0.91（light3_2）。叠加现货五轴判死（vR1nAj6z 克隆 / j2Yle6q5 prod 0.8465 /
leA6jmoe 单钉子 / 88R7j2Nz prod 0.7212），**news17/nws17 字段空间关闭**。
幸存者仅 E 轴 `58E7jkaN`（已提交，prod 0.5611）+ `MPYq0819`（篮内）——NEWS 塔 2/3 不变。

### 6.6 转向决策（待用户裁定）

缺口 2 条（10 − 8）。NEWS 第 3 条（点亮塔）候选路径：
- **A. news18 未测轴**（70 字段，本三波均未触及）——但冷字段天花板 ~0.9 已三次实证，预期低；
- **B. 判死 NEWS 点塔、改用其它塔凑 10 条**（§4.6 预案）——总数可达成，NEWS 停在 2/3；
- **C. 先提交现有 8 条**（等授权），提交后再决定缺口路线。

---

## §5 前置盘点结论（2026-11-02，输入本设计）

| 现货 | 结论 | 证据 |
|---|---|---|
| `vR1nAj6z`（S 2.10，ra=[]） | **判死**：与 `wpQwjWn6` 逐位相同（互相关 1.0000），后者 prod=1.0 生产池克隆 | 强库 §6.8 + `vec_count` 同事件集恒等（§6.1） |
| `j2Yle6q5`（S 1.93，ra=[]，2Y 2.66，覆盖 10/10 实测过） | **判死**：prod 实测 **0.8465**（直方图 n([0.8,0.9))=1，钉子=wpQwjWn6 生产池克隆） | 2026-11-02 `check_correlation` 实测 |
| `leA6jmoe`（S 2.18） | **判死**：prod 0.7077 且 n([0.7,0.8))=1 ⇒ 窗口谷底法死刑（KOR 16/16 零例外） | 直方图实测 + `wq-window-valley-break-prod-wall` 前置判据 |
| `88R7j2Nz`（zscore 壳 C 轴） | **判死**：prod 0.7212 | alphas 表 platform_sync |
| `58E7jkaN` | ✅ 已提交（prod 0.5611，E 轴） | — |
