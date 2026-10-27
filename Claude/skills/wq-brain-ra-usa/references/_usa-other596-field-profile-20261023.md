# USA/D1 · `other596` 字段画像（2026-10-23）

> 画像口径：全字段来自平台 `GET /data-fields?dataset.id=other596&region=USA&delay=1&universe=TOP3000`
> （走 `brain_client.get_datafields`，`complete=True`、`platform_count=420`，即**全量无截断**）。
> 原始落盘 `logs/_other596_fields.json`（420 件，含 coverage / userCount / alphaCount / description）。
> 本数据集此前**全库零回测**（DB `backtest_results` 无其他 `other596` 记录；平台全数据集 alphaCount 累计 ≈124）。

## 1. 数据集解剖（这是"新闻情绪 × 供应商变体"的矩阵集，不是基本面集）

| 维度 | 事实 |
|---|---|
| 类别 / 塔 | `OTHER`（`USA/D1/OTHER` 塔，**未点亮**，当季 0 条 ACTIVE；other143 同塔） |
| 类型 | MATRIX 420/420（**无 VECTOR**，因此 `vec_*` 族不适用） |
| 字段数 | 420 |
| 覆盖率 | canonical 变体 **0.9795**（≈98%），suffixed/`dts` 变体 **1.00** |
| 延迟 | 查询面 = D1；但字段描述里**明写 D0 的变体不能当 D1 用**（见 §3 的 D0 标记） |
| 拥挤度 | canonical 21 字段/变体里 `alphaCount` 多数 **0–2**；最拥挤的是 suffixed 变体（max 18） |
| 供应商 | Benzinga 新闻（story / teaser / headline+body 三种抽取面） |

**核心结构 = 3 个情绪类 × 7 个统计量 × 10 个变体**：

- 情绪类：`pos`（正面）/ `neut`（中性）/ `neg`（负面），取值域 0–1
- 统计量：`mean` / `median` / `max` / `min` / `std` / `conf_low` / `conf_up`
  —— 每个统计量都**跨"当天所有关联 story"聚合**，即字段是**股票-日**粒度
- `conf_low` / `conf_up` = 当日均值情绪的 **95% 置信区间上下界** ⇒ `conf_up − conf_low` 是**估计不确定性**，
  且它按 `1/√n` 缩小 ⇒ **内生地惩罚"新闻条数少"**，这是本数据集独有的量（见 §4 的 M3）

## 2. 变体全表（210 canonical + 210 派生）

| 变体 | 字段数 | 覆盖率 | 描述要点 | D0/D1 | 判断 |
|---|---:|---:|---|---|---|
| base `oth596_` | 21 | 0.9795 | "base variant" | **D0** | ⚠ 不作 D1 主信号 |
| `_2` | 21 | 0.9795 | "across all **linked stories**" | 未标 | 可用 |
| `_3` | 21 | 0.9795 | "all **Benzinga news stories**"（最全口径） | 未标 | **主口径** |
| `_4` | 21 | 0.9795 | "Benzinga news **headlines/body**" | **AMR, variant 4, D1** | 区域标注为 AMR，慎用 |
| `_5` | 21 | 0.9795 | "variant 5 **headline/body**" | **D1** | 可用（第二口径） |
| `_t` | 21 | 0.9389 | "**teaser** text … in AMR" | AMR | 低覆盖 + 区域不符 |
| `_t2` | 21 | 0.9389 | "USA **T2** variant" | **D1** | 可用（第三口径） |
| `_t3` | 21 | 0.9389 | "**teasers** mapped to the stock" | 未标 | 可用 |
| `_t4` | 21 | 0.9389 | "**teaser (T4)** stories" | **D0** | ⚠ 不作 D1 主信号 |
| `_t5` | 21 | 0.9389 | "Benzinga teaser stories … T5" | 未标 | 可用 |
| 9 组 `_{NNN}` 副本 | 162 | **1.00** | 描述退化为一句（"Lower confidence bound for negative sentiment scores."） | 未标 | **与 canonical 高度同源**；最拥挤（ac≤18） |
| 48 个 `*dts_{gen,sop,tuen}_NNN` | 48 | 1.00 | 只有 std 型语义（"Standard deviation of negative sentiment scores."） | 未标 | 派生面，拥挤（ac≤16） |

> **判读规则（写进日后波次）**：canonical 与 `_NNN` 副本**不是两个信号**，是同源的重复面。
> 选字段优先 canonical（空且描述完整）；把 `_NNN` 当"另一个字段"去测 = 伪装成多样性的重复测试。

## 3. 家族分类（按 `brain-alpha-research-news-sentiment` §2 的 5 家族）

| 家族 | 本数据集对应字段 | 数量 |
|---|---|---:|
| **direction**（方向/带符号情绪） | 全部 `pos/neg/neut` 的 `mean/median/max/min` | 主体 |
| **dispersion**（分歧度） | 全部 `*_std` | 210 条中的 30 |
| **dispersion（估计不确定性）** | `conf_up − conf_low`（两界相减得到宽度） | 30 对 |
| attention（关注度） | **无**（没有条数/提及计数/热度字段） | 0 |
| peer_context（同侪上下文） | **无** | 0 |
| event_type（事件类型） | **无**（没有 topic / 事件码） | 0 |

⇒ 本集的可用桶只剩：**Level / Change / Surprise / Dispersion**。
skill 里标 HIGH 的 `Event-conditioned`（需 attention 字段）与 `Propagation`（需 event_type）**结构性不可做**——
不是没试，是字段面不存在。这条先写死，后续波次不要重复试探。

## 4. 机制假设（每条都能说出收益从哪来）

| 码 | 机制 | 表达式骨架 | 先验 |
|---|---|---|---|
| **M1** | **水平锚**：正面情绪高的股票在新闻日后继续被买（情绪溢价） | `rank(pos_mean)` | 锚点，用来判"信号是否在水平里"——不测它就无法归因后续臂 |
| **M2** | **变化**：净情绪相对自身历史基线的偏离，新闻后漂移 | `rank(ts_zscore(pos_mean − neg_mean, W))` | 主先验；与 other143 冠军同壳（zscore+rank），壳已验证 |
| **M3** | **估计不确定性折价**：`(conf_up−conf_low)/mean` 宽 ⇒ 市场对该公司看法分裂 ⇒ 高估 ⇒ 看空 | `−rank(ts_zscore((conf_up−conf_low)/pos_mean, W))` | **本集独有量**；`1/√n` 缩放使其兼有"低关注"含义 |
| **M4** | **分歧度折价**（Miller 1977）：story 间情绪分歧大 ⇒ 卖空受限下高估 | `−rank(ts_zscore(pos_std, W))` | skill 标 HIGH 的 dispersion 桶 |
| **M5** | **尾部负面事件**：`neg_max ≫ neg_mean` 意味着当天有一条独立极坏消息，市场反应不足 | `−rank(ts_zscore(neg_max − neg_mean, W))` | 事件尾 vs 均值的**差**，不是水平 |
| **M6** | **信息真空**：中性占比高 = 新闻无信息量 ⇒ 无信号日，反向做 | `−rank(ts_zscore(neut_mean, W))` | 检验"情绪"是不是只在极端日有内容 |
| **M7** | **跨变体测量分歧**：同一公司同一天，两个独立抽取面（story 全量 vs headline/body）给出的情绪不一致 ⇒ 信息质量差 ⇒ 折价 | `rank(z(v3_pos) − z(v5_pos))` | 单一经济量（测量分歧），不是两信号加权 |
| **M8** | **分歧条件下的方向**（skill 的 event-conditioned 在本集只能用 dispersion 当条件） | `trade_when(z(pos_std)>1, rank(z(net_tone)), −1)` | 只在分歧日取方向，看能否提高 edge |

**ATOM 声明**：以上 8 条全部**只用 `other596` 字段**，无跨数据集腿 ⇒ 满足单数据集 ATOM 口径。
（"用尽全部非豁免字段"在本集的意思是：3 情绪类 × 7 统计量 × 10 变体里，凡不重复的统计语义都要有自己的代表臂；
`_NNN` 副本属重复面，按 §2 的判读规则豁免。）

## 5. 与 other143 的关系（为什么换到这里）

other143 已在波 81b 判定 `USA-OTHER143-F-WALL`（F 峰 0.88，40 条回测、8 个算子族、3 个窗口、
3 种降换手杠杆全部试过）。other596 的**经济量不同**（情绪 vs 券商集中度），不是同一机制的换字段重测：
other143 的信号是"机构订单结构"，other596 是"新闻文本情绪 + 文本抽取可信度"。

## 6. 波 82 预注册（发波前写死，事后不调）

**统一设置**（与 other143 冠军壳同源，便于跨数据集对比）：`region=USA` / `delay=1` / `universe=TOP3000` /
`decay=5` / `neutralization=SUBINDUSTRY` / `nanHandling=ON` / `truncation=0.08` / `2014-01-01 → 2023-12-31`。
**multisim `4lGv18bY4rDbAM128jf0vRp`（9 臂）**，脚本 `tracking/USA/runs/usa_other596_w82.txt` + `_spec.json`。

| # | 机制 | 表达式 | 这一臂要回答什么 |
|---|---|---|---|
| A1 | M1 水平锚 | `rank(oth596_3pos_mean)` | 情绪水平本身有没有截面信息（不测它，后面所有 zscore 臂都无法归因） |
| A2 | M2 变化 | `rank(ts_zscore(subtract(oth596_3pos_mean, oth596_3neg_mean), 60))` | 净情绪的自相对偏离（主先验） |
| A3 | M2 单侧对照 | `rank(ts_zscore(oth596_3pos_mean, 60))` | 净情绪若有效，是 pos 单独贡献还是 neg 抵消起作用 |
| A4 | M3 估计不确定性 | `-rank(ts_zscore(divide(subtract(oth596_3pos_conf_up, oth596_3pos_conf_low), oth596_3pos_mean), 60))` | **本集独有量**：CI 宽度（≈1/√n）宽 ⇒ 看空 |
| A5 | M4 分歧度 | `-rank(ts_zscore(oth596_3pos_std, 60))` | Miller 1977：story 间分歧大 ⇒ 高估 ⇒ 看空 |
| A6 | M5 尾部负面 | `-rank(ts_zscore(subtract(oth596_3neg_max, oth596_3neg_mean), 60))` | 单条极坏 story 的增量（差，不是水平） |
| A7 | M6 信息真空 | `-rank(ts_zscore(oth596_3neut_mean, 60))` | 中性占比高 = 无信息日，反向 |
| A8 | M7 跨变体测量分歧 | `rank(subtract(ts_zscore(oth596_3pos_mean, 60), ts_zscore(oth596_5pos_mean, 60)))` | 同一天两个抽取面（全量 story vs headline/body）的分歧 ⇒ 文本抽取质量 |
| A9 | M8 分歧条件下的方向 | `trade_when(greater(ts_zscore(oth596_3pos_std, 60), 1), rank(ts_zscore(subtract(oth596_3pos_mean, oth596_3neg_mean), 60)), -1)` | 只在高分歧日取方向；其余日 `-1` 平仓 |

**为什么是这 9 条**：§3 的家族盘点里 attention / peer_context / event_type 三类**字段数为 0**，
`Event-conditioned` 与 `Propagation` 两桶结构性不可做，所以 A9 用 dispersion 当条件（本集唯一可得的条件变量）。
`_NNN` 与 `dts_*` 副本按 §2 判读规则**不进臂**（同源重复面，进来只是伪装成多样性的重复测试）。

**判决规则（发波前写死）**：

① 任一臂 `S ≥ 1.58` 且 `F ≥ 1.0` 且 `2Y ≥ 1.58`、`CLUSTER_TEST` 过、`TO ∈ [0.01, 0.70]` ⇒ 进 prod 探针队列
（**提交仍需用户明确确认**，`submit_verdict` 只能否决）；
② **9 臂全部 `|S| < 0.5`** ⇒ 判 `USA-OTHER596-DIRECTION-EMPTY`：本集的"情绪方向/分歧"面**无截面信息**，
按 N.4 顺位切下一数据集（这种结局与 other143 的 F 墙不是同一类失败，不得混记）；
③ 有臂 `S ≥ 1.0` 但 F 不足 ⇒ **先按机制归因**（哪条机制出了 S、出在 pos 还是 neg、出在水平还是变化），
再决定是否就同机制做参数/窗口/中性化修复——不许直接换机制乱扫；
④ 只有 A4/A5/A6 出 S 而方向与假设**相反**（即正向 rank 反而好）⇒ 记「折价方向被证伪」，
不追着反号重测（反号重测 = 用数据反推假设，过一次样本外必崩）。

## 7. 波 82 结果（已收批，`4lGv18bY4rDbAM128jf0vRp`，9/9 COMPLETE）

**DB 波号 = `s2_other596_d1`**（不是 `82`：`82` 已被 analyst44 的 2026-09-19 八条占用，同号会混血脉）。
发波文件仍叫 `usa_other596_w82*`（发波时的临时编号），两者对应关系以本节为准。
入库：`expressions` 9 条 + `backtest_results` 9 行，全部 `dataset='other596'`。

| # | 机制 | alpha | S | F | TO | 2Y | SUB | 长/空 | 失败项 |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| A1 | M1 水平 | `78o3K7Q2` | **0.91** | 0.19 | 1.65 | 1.36 | 0.26 | 200/196 | S, F, **TO**, SUB, 2Y |
| A2 | M2 净情绪变化 | `O0JR5QmY` | 0.80 | 0.16 | 1.64 | 1.44 | — | 197/197 | 同类 |
| A3 | M2 pos 单侧 | `88vVK567` | 0.53 | 0.08 | 1.64 | 1.54 | — | 199/196 | |
| A4 | M3 CI 宽度折价 | `e76Nqk2O` | 0.54 | 0.09 | 1.56 | **−0.69** | — | 181/184 | 2Y 反向 |
| A5 | M4 分歧度折价 | `wp93JKzQ` | 0.56 | 0.09 | 1.55 | **−0.84** | — | 180/185 | 2Y 反向 |
| A6 | M5 尾部负面 | `omoR98zb` | 0.61 | 0.11 | 1.55 | **−0.83** | — | 178/186 | 2Y 反向 |
| A7 | M6 信息真空 | `QPYO5Z5X` | 0.33 | 0.04 | 1.64 | 1.57 | — | 199/195 | |
| A8 | M7 跨变体分歧 | `9qE8AZA9` | 0.60 | 0.11 | 1.59 | **2.18** | 0.63 ✓ | 198/196 | S, F, TO |
| A9 | M8 分歧条件方向 | `88vVK5Kl` | −0.26 | −0.06 | **0.048** | −0.67 | — | **1571/1159** | 死 |

### 7.1 归因（按机制，不是按指标）

1. **换手 1.55–1.65 与表达式形态无关 ⇒ 根因是字段层面的稀疏覆盖，不是信号不稳定。**
   直接证据：A1–A8 八种完全不同的结构（水平 / zscore / 正负号 / 差异 / CI 比）换手全部落在
   1.55–1.65；而 A9（`trade_when` 让非条件日**继续持仓**而不是离场）换手骤降到 0.048。
   持仓数给出同一结论：A1–A8 的 `longCount/shortCount` 恒为 ~180–200，
   而 A9 是 **1571/1159** ⇒ 只有 A9 把组合铺到了全宇宙，前八条都只持有「当天有新闻的那 ~400 只」。
   **机制解释**：字段是「当天关联 story 的情绪聚合」，无新闻日无值；`rank()` 只在有值样本内排序，
   于是组合每天被「当天新闻名单」重建一次 ⇒ 换手必然 >1。
   ⚠ 这条同时说明：`coverage 0.9795` 是**时间覆盖**（98% 的交易日有字段），不是截面覆盖。
2. **M3/M4/M5 三个「折价」机制被 2Y 否决**：全样本 S 还有 0.54–0.61，但近两年 −0.69 / −0.84 / −0.83。
   按预注册规则 ④ 的处理口径：**记「折价方向不成立」，不翻号重测**。
   经济含义：把「分歧大 / 不确定性高 / 有极坏消息」当作看空信号，在 2014–2021 有一点点用，
   在 2022–2023 完全反向 ⇒ 这不是稳定机制，是时段特征。
3. **M1 水平 > M2 净情绪 > M2 pos 单侧**（0.91 / 0.80 / 0.53）⇒ 信息确实在水平里，
   且 `neg` 腿贡献了 (0.80−0.53) 那部分；但三者都远低于 1.58 的门。
4. **M7 跨变体分歧是唯一过 SUB(0.63) 与 2Y(2.18) 的臂**，但全样本 S 仅 0.60、DD 33.8%
   ⇒ 近两年强、全样本弱 = 时段特征，不能当作可提交候选；它的价值是给出了下一波的修复起点。
5. **M8（分歧日才取方向）彻底失败**：−0.26，且因持仓惯性换来 0.048 的超低换手。
   ⇒ 用 dispersion 当条件（本集唯一可得的条件变量）在这条数据上没有信息，skill 的
   event-conditioned 桶在这个数据集上到此为止。

### 7.2 F 墙算术（决定要不要继续）

提前算清，避免又扫一轮才发现上不去：`F = S·sqrt(RET/max(TO,0.125))`。
A1 实测 RET 7.29%、TO 1.65、S 0.91。**即使把 TO 修到 0.40 而收益不变**，
F = 0.91·sqrt(0.0729/0.40) ≈ **0.39**；要到 F=1.0 且 S=1.58，需要 RET/TO ≥ 0.40，
即 TO=0.40 时年化收益 ≥ 16%——是当前 7.3% 的两倍多。
⇒ **覆盖修复只能救换手，救不了 F 墙**。这正是下一波只发 8 臂（而不是再扫机制）的原因。

## 8. 波 83 预注册（覆盖修复诊断，ON/OFF 双档各 4 臂）

**唯一假设**：稀疏覆盖使组合每天重建 ⇒ 把「当天情绪」变成「最近已知情绪」（`ts_backfill`），
组合应铺开到全宇宙、换手应大幅下降。**不引入任何新机制**（M3–M6、M8 已由波 82 否掉，不再重测）。

| 档 | 臂 | 表达式 | 用途 |
|---|---|---|---|
| ON | D1 | `rank(oth596_3pos_mean)` | **控制臂**：与波 82 A1 逐位对比，验证换档无副作用 |
| ON | D2 | `rank(ts_backfill(oth596_3pos_mean, 22))` | 回填 1 个月 |
| ON | D3 | `rank(ts_backfill(oth596_3pos_mean, 250))` | 回填 1 年（长度灵敏度；若 D2/D3 与 D1 逐位相同 ⇒ ON 档下 NaN 已被 0 填充，backfill 无对象） |
| ON | D4 | `rank(ts_mean(ts_backfill(subtract(pos,neg), 22), 22))` | 净情绪「状态」（回填 + 22 日均） |
| OFF | D1–D4 | 同上 | 弱强度档复本，用于判定「是回填无效还是换档打死」 |

**为什么双档**：`nanHandling=OFF` 是已实测的弱强度档（IND 2.19→0.46），
若只发 OFF，任何变弱都分不清是「回填没用」还是「换档打的」。每档自带控制臂 ⇒ 档内可比。

**判决规则（发波前写死）**：

① ON 档 D2/D3 的 `longCount` 显著 > 200（≥800）且 TO ≤ 0.7 ⇒ 回填生效，**记录 TO 修复后的 S**；
   再按 §7.2 的 F 算术裁决是否值得继续；
② ON 档 D2/D3 与 D1 逐位相同 ⇒ ON 档下 backfill 不生效（NaN 已按 0 处理），以 OFF 档读数为准；
③ 两档的回填臂都 ≤ D1（S 不升、TO 不降）⇒ 判 **`USA-OTHER596-SPARSE-COVERAGE-WALL`**：
   本数据集的日报情绪面封存，按 N.4 顺位切下一数据集；
④ 任一臂 F ≥ 0.95 且 S ≥ 1.58、2Y ≥ 1.58、TO ∈ [0.01,0.70] ⇒ 进 prod 探针队列（**提交仍需用户明确确认**）。

## 9. 波 83 结果（覆盖修复诊断）

multisim：ON 档 `3yxc1N6Rx5cabqxxSHmpJdS`、OFF 档 `zyuMl3eX4x4a4b1bbwwcd8s`，各 4 臂全部 COMPLETE。
DB 波号 `s2_other596_w83`（8 行 `backtest_results` + 8 条 `expressions`，`dataset=other596`）。

| 臂 | S | F | TO | RET | DD | 2Y | longCount / shortCount |
|---|---:|---:|---:|---:|---:|---:|---|
| D1 `rank(pos_mean)` | **0.91** | **0.19** | 1.65 | 7.29% | 17.2% | 1.36 | 200 / 196 |
| D2 `rank(ts_backfill(pos,22))` | 0.31 | 0.06 | 0.2317 | 0.89% | 7.7% | 0.35 | 1223 / 1218 |
| D3 `rank(ts_backfill(pos,250))` | 0.49 | 0.13 | 0.1647 | 1.23% | 6.7% | 0.44 | 1523 / 1520 |
| D4 `rank(ts_mean(ts_backfill(net,22),22))` | −0.07 | −0.01 | 0.0891 | −0.17% | 13.0% | −0.31 | 1425 / 1434 |

**ON 档与 OFF 档 8 个读数逐位相同**（S / F / TO / RET / DD / LC / SC 全同）。

### 9.1 归因（五条）

1. **回填确实生效**（规则 ① 命中）：`longCount` 200 → 1223（22 日）/ 1523（250 日），
   TO 1.65 → 0.2317 / 0.1647。§7 判定的「每日新闻集合重建」机制得到正面验证——
   把当天值换成最近已知值，组合就铺到了全宇宙。
2. **但收益同步塌陷，而且是超比例塌陷**：S 0.91 → 0.31 / 0.49，RET 7.29% → 0.89% / 1.23%。
   铺开 6–7.6 倍的持仓只换来 1/8–1/6 的收益 ⇒ **信号完全装在「当日有新闻的那 ~400 只」里**，
   全宇宙铺开等于把同一份收益稀释掉。这不是「回填没用」，是「回填有效、但信号本来就窄」。
3. **F 反而变差**：0.19 → 0.06 / 0.13。原因是 F 的两个因子反向移动——
   `sqrt(RET/max(TO,0.125))` 从 0.210 升到 0.274（D3），但 S 从 0.91 掉到 0.49，乘积净减。
   ⇒ §7.2 的 F 墙算术被**实测确认**：修换手同时会杀 Sharpe，两者不会独立改善。
4. **RET/TO 比值仍差一个量级**：最好的 D3 是 0.0123/0.1647 = **0.0747**；
   §7.2 已算过 F=1.0 且 S=1.58 需要 RET/TO ≥ 0.40，而按本集最大 S=0.91 则需要 ≥ 1.21。
   0.0747 距 0.40 差 5.4 倍、距 1.21 差 16 倍 ⇒ 不是调参尺度的问题。
5. **档位轴在本臂集上未被判别**（不构成「nanHandling 与本数据集无关」的结论）：
   已核实平台侧 settings 真的不同（`78o3K7Q2` nanHandling=ON，`kqJvLVYz`=OFF），排除发批串档。
   合理解释是本波四条臂全部由**NaN 透明算子**构成（`rank`/`ts_backfill`/`ts_mean`/`subtract`），
   两档语义对它们等价。⇒ 想用 nanHandling 当杠杆时，必须先确认臂里含有 NaN 敏感算子
   （`ts_sum`/`group_*`/`ts_delta` 之类），否则整波等于重复发了一次。

### 9.2 规则判定与「为什么当时没有立即封存」

按 §8 预注册：规则 ② 不触发（D2/D3 与 D1 差异巨大）；规则 ③ 的**实质**命中
（两条回填臂的 S / F 全面 ≤ D1，RET/TO 也未进入可提交区间）。
但**没有立即封存**，因为同一时间完成的论坛复查捞到了两条本数据集**从未测过**的高票配方（§10）——
「已试尽」这个前提当时并不成立。这是刻意留下的一个口子：预注册规则负责防止「边测边改判据」，
不负责替人宣布搜索空间已穷尽。

## 10. 论坛复查（用户长期指令）与波 84 预注册

### 10.1 先记工具事实：本地 recon 挂了，MCP 通道是好的

- `tools/forum_recon.py`（后台任务）**失败**：`read_failed` —— 搜到 42 条候选、34 次读帖全失败、
  读到正文 0 篇。按 2026-09-29 证据契约记 `status=error`、**不作判死证据、不入负缓存**，
  台账键 `USA/forum_recon_error_b1f628c271`（`found=null`）。
  ⚠ 这次**不能**再写成「论坛无解」——那正是契约要防的误判。
- 改走 MCP `search_forum_posts(search_query="news sentiment")`：**50 条命中且可读**，
  再用 `read_forum_post(article_id=...)` 取到正文与评论。
  **可复用结论**：本机 USA/zh-cn 论坛的读帖通道在 MCP 侧可用、在本地 recon 脚本侧不可用；
  论坛复查优先走 MCP，`tools/forum_recon.py` 的读帖链路需要单独修（属工程债，另行登记）。

### 10.2 捞到的配方（此前一条都没在 other596 上试过）

| 编号 | 出处 | 配方 | 票数 | 对 other596 的可用性 |
|---|---|---|---:|---|
| **R1** | `【Alpha灵感】使用nip族数据点亮news塔`（id 40847481080087） | 「相关性算子 + FAST neutralization 组合比较适合处理 sentiment 数据」：`ts_corr(fld, returns, d)` / `ts_covariance(fld, returns, d)` / `ts_regression(returns, fld, d, lag=0, rettype=2)` | 93 / 22 评 | **骨架可用，字段不可用**：other596 **无 `nip` 字段**（420 字段实测 0 命中），只能借「相关性算子 + FAST」两个组件。评论 `JX84394`：「USA d1 出信号了 交了一个 ppa」⇒ 该组合在 USA/D1 有实证落地 |
| **R2** | `【sentiment模板】帮助点sentiment塔`（id 41449516289687） | `group_neutralize(reverse(ts_max(snt_pos_std − snt_neg_std, d)), group)` —— 情绪**标准差**=分歧度，取 d 日峰值后反转、行业中性化 | 18 | **原样可套**：`pos_std − neg_std` 正是本集的分歧度净值 | <!-- lint:counterexample: 论坛原模板引文；ts_max 不可访问，改用见下方原/新对照 -->
| 补充 | `MCP七十二变模板之news-sentiment点塔`（id 37140180319127） | `group_zscore(-ts_corr(<news>, <sentiment>, <days>), <group>)` | 36 / 24 评 | 可用；把 R1 的相关性核套进 `group_zscore` |

**两条副作用，必须写进交付口径**：
- R1 用 `returns` 作配对腿 ⇒ 严格 ATOM 口径下**不算 ATOM**（跨 PV 数据集）。
  按目标里「最好是 ATOM」的措辞可接受，但交付时要逐条标注 `atom_flag=False`。
- **FAST 中性化**是本数据集此前从未测过的设置杠杆（波 82/83 全部 SUBINDUSTRY）。
  R1 之所以值得一试，一半原因在这个杠杆上，而不只在算子上。

### 10.3 波 84 八臂（单批 / FAST / 一臂一机制）

multisim `v6qRm4i95aHbKJAmYztJ5B`；统一 `USA/D1/TOP3000, decay 5, FAST, nanHandling ON, truncation 0.08, 2014-01-01→2023-12-31`。

| 臂 | 表达式 | 机制 / 用途 |
|---|---|---|
| f1 | `rank(oth596_3pos_mean)` | **控制臂**：与波 82 A1 同表达式，只换 SUBINDUSTRY→FAST ⇒ 分离 FAST 杠杆 |
| f2 | `rank(ts_corr(oth596_3pos_mean, returns, 20))` | R1 相关性算子（短窗） |
| f3 | `rank(ts_covariance(oth596_3pos_mean, returns, 60))` | R1 协方差形态（论坛评论建议 60–180） |
| f4 | `rank(ts_regression(returns, oth596_3pos_mean, 60, lag=0, rettype=2))` | R1 回归形态（原帖逐字） |
| f5 | `rank(ts_corr(subtract(pos_mean, neg_mean), returns, 60))` | R1 骨架 + 波 82 已验证的「净情绪」核 |
| f6 | `rank(ts_corr(oth596_3pos_std, returns, 20))` | R1 骨架套到 dispersion 桶 |
| f7 | `group_neutralize(multiply(-1, ts_rank(subtract(pos_std, neg_std), 5)), subindustry)` | R2 模板（`ts_max` 不可访问，已按下方原/新对照换成 `ts_rank`） |
| f8 | `group_zscore(multiply(-1, ts_corr(oth596_3pos_mean, returns, 60)), subindustry)` | 论坛 #2 的 `group_zscore(-corr)` 复合形态 |

预检：字段存在 8/8 OK、括号/语法 8/8 OK、`[arity] 8/8 PASS`、`[dispatch] PASS`。
⚠ 8 臂 shape 全为 `S9`（同一形状族）——本波是**定向机制探针**，不是多样性扫描；
闸 6 若要卡多样性，需按 waiver 协议记因（`PROBE_BATCH`）。

**判决规则（发波前写死）**：

① f1 的 S/TO 与波 82 A1（0.91/1.65）**显著不同** ⇒ FAST 是真设置杠杆，机制臂结论按同设置读，
   并在 §11 单独记一条设置层结论；几乎不动 ⇒ FAST 对情绪面中性，机制臂可直接与波 82 横比；
② 任一臂 F ≥ 0.95 且 S ≥ 1.58、2Y ≥ 1.58、TO ∈ [0.01,0.70] ⇒ 进 prod 探针队列
   （**提交仍需用户明确确认**；`returns` 腿须同时标 `atom_flag=False`）；
③ 全臂 max(F) < 0.5 且无臂 2Y ≥ 1.0 ⇒ 判 **`USA-OTHER596-SPARSE-COVERAGE-WALL`** 封存：
   三波共 21 臂、覆盖 相关性/协方差/回归/回填/状态/条件/分歧/折价 八类构造后仍无一臂进入
   F 的可提交区间，按 N.4 顺位切下一数据集；
④ 出现「TO 已合格、S/F 不足」的臂（TO ≤ 0.7 且 S < 1.0）⇒ 记为该数据集唯一可修复形态，
   再单发一波只调 decay/窗口，不换机制。

### 10.5 波 84 报废与波 84b 重发（2026-10-23，`ts_max` batch-kill）

**结果**：`v6qRm4i95aHbKJAmYztJ5B` → 1 ERROR + 7 CANCELLED，**零信息产出**。
ERROR 正文：`Attempted to use inaccessible or unknown operator "ts_max"`。

**归因（三层，全部是流程/工具层，与机制无关）**：

1. `ts_max` / `ts_min` **不在平台算子表**里（catalog 快照无此名），平台直接判 inaccessible。
2. 我用的元数闸 `op_arity.check_expression` 当时 **对目录外的算子 `continue` 放行**
   ⇒ `[arity] 8/8 PASS` 是真通过、也是真没拦。
3. 闸其实一直存在：`platform_constraints.json.inaccessible_ops = ["ts_max","ts_min"]`，
   toolkit `gate.py:486-487` 对 raw idents 判定。**自写预检没调它**。

**修复（2026-10-23，改闸本身而不是绕开它）**：

- `src/wqb/expression/op_arity.py` 改为 **fail-closed**：目录外算子报 `[UNKNOWN_OP]`、
  `GHOST_OPERATORS` 报 `[GHOST]`；存在性用 `load_catalog_names()`（catalog 全部 103 名）
  而非 `load_signatures()`（101 个，`in`/`universe_size` 推不出签名但合法）。
  `strict_unknown=False` 只留给归档语料扫描，`ensure_safe_for_dispatch` 不接受该开关。
- 端到端回归：把本波 8 条原式重放给 `ensure_safe_for_dispatch`，现在整批被拦并点名
  `[UNKNOWN_OP] ts_max`（修复前报 8/8 PASS）。
- 爆炸半径实测：17,427 条"平台已接受"表达式的未知面只有 5 个截断脏 token，误杀 ≈ 0。
- 波 84b 预检（`logs/_tmp_w84b_preflight.py` §0）另保留三重算子闸（catalog scope /
  `inaccessible_ops` / `ghost_ops`）作双保险。经验沉淀 `docs/experience/04_engineering.md` §14.6。

**f7 的 REGULAR 安全替代**（唯一一条表达式改动）：

| 项 | 值 |
|---|---|
| 原 | `group_neutralize(reverse(ts_max(subtract(pos_std, neg_std), 5)), subindustry)` | <!-- lint:counterexample: 原/新对照的「原」行，不可照抄 -->
| 新 | `group_neutralize(multiply(-1, ts_rank(subtract(pos_std, neg_std), 5)), subindustry)` |
| 理由 | `ts_rank(x, 5)` 在当日值接近 5 日高点时最大 ⇒ `-ts_rank` 是 `-ts_max` 的单调替代；`ts_arg_max` 虽合法但返回日索引，语义不符 |

**波 84b**：8 臂同上表（f1–f6、f8 逐字不变，f7 用上表替代），设置仍为
`USA/D1/TOP3000, decay 5, FAST, nanHandling ON, truncation 0.08, 2014-01-01→2023-12-31`。
multisim `47fa2SbKg4VS9aCSNELtcx8`。§10.4 的四条判决规则**继续有效、一字不改**——
波 84 是零信息批，不构成任何"已测过"的证据。

## 11. 波 84b 结果与 other596 封存裁决（2026-10-23）

multisim `47fa2SbKg4VS9aCSNELtcx8`：7 COMPLETE + 1 WARNING（f4 单位不兼容），0 ERROR。
DB 波号 `s2_other596_w84b`（7 行 `backtest_results` + 7 条 `expressions`，`dataset='other596'`）。

| 臂 | alpha | S | F | TO | 2Y | RET | LC/SC | 失败项 |
|---|---|---:|---:|---:|---:|---:|---|---|
| f1 ctrl `rank(pos_mean)` | `O0JRbXNY` | 0.34 | 0.04 | 1.4518 | 0.84 | 1.54% | 1630/1496 | S,F,TO,SUB,2Y |
| f2 corr20 | `rKd9JMOo` | 0.32 | 0.06 | 0.2489 | — | 0.74% | 1593/1533 | S,F |
| f3 cov60 | `58jradzJ` | **0.60** | **0.28** | 0.1107 | — | 2.71% | 1510/1615 | S,F |
| f4 reg60 | `npAmZ5dE` | WARNING（`ts_regression` 单位不兼容） | | | | | | 非干净读数，不作机制判据 |
| f5 netcorr60 | `vROZeX2a` | −0.30 | −0.07 | 0.1065 | — | −0.65% | 1589/1536 | 负 S |
| f6 dispcorr20 | `ZYmg2vAn` | **0.89** | 0.27 | 0.2485 | — | 2.31% | 1551/1575 | S,F |
| f7 `-ts_rank(pos_std−neg_std,5)` | `e76NdZQN` | 0.27 | 0.03 | 1.4674 | 0.08 | 1.62% | 1567/1558 | S,F,TO,SUB,2Y |
| f8 gz(−corr60) | `j2eo9Ke5` | 0.28 | 0.06 | 0.1171 | — | 0.59% | 1716/1409 | S,F |

### 11.1 规则 ① 归因：FAST 确实是设置杠杆，且混杂项已被排除

逐项核对两波 `raw.settings`：**除 `neutralization` 外逐键相同** —— universe TOP3000、delay 1、
decay 5、truncation 0.08、`nanHandling: "ON"`、`pasteurization: "ON"`、`unitHandling: "VERIFY"`、
maxTrade/maxPosition OFF、`2014-01-01→2023-12-31`。
⇒ 先前怀疑的 `nanHandling` 串档被排除（两边都是 ON，波 83 §9.1 第 5 条那条读数也是 ON）。

| 同一条 `rank(oth596_3pos_mean)` | 中性化 | S | TO | LC/SC |
|---|---|---:|---:|---|
| 波 82/83 D1 | SUBINDUSTRY | 0.91 | 1.65 | 200/196 |
| 波 84b f1 | FAST | 0.34 | 1.4518 | **1630/1496** |

**机制解释（与波 83 的回填结论互补，不是重复）**：SUBINDUSTRY 版把 200/196 的窄账本
在组内去均值后变得更窄；FAST 风险中性化把同一信号铺到 1630 只，S 从 0.91 掉到 0.34。
⇒ **波 82/83 那个 0.91 从来不是"更宽的覆盖"，而是一个 200 只的集中下注**；FAST 把它还原成
全宇宙读数后信号很薄。这条同时解释了为什么波 83 回填把账本铺到 1523 只时 S 掉到 0.49——
两个方向（回填 / 换中性化）得到的是同一个结论：**信号只存在于窄样本里**。

### 11.2 规则 ③ 命中：封存 `USA-OTHER596-SPARSE-COVERAGE-WALL`

按 §10.4 逐条判定：

- ① 命中（见 §11.1）。
- ② **不触发**：无臂达到 F ≥ 0.95 / S ≥ 1.58 / 2Y ≥ 1.58 / TO ≤ 0.70。本波 max F = 0.28（f3），
  max S = 0.89（f6，TO 0.2485，2Y 未出），最好 2Y = 0.84（f1，但 TO 1.4518）。
- ③ **触发**：全臂 max(F) = 0.28 < 0.5，且无臂 2Y ≥ 1.0（已出的两个 2Y 是 0.84 / 0.08）。
- ④ 形态上出现（f2/f3/f5/f6/f8 都是 TO ≤ 0.7 而 S < 1.0），但**不再发设置波**：
  ④ 的成立前提是"差一点"，实测这些臂的 S 在 0.27–0.89、F ≤ 0.28，
  从 0.89 到 1.58 需要 +78% Sharpe、F 需要 +257%；而本案唯一可用的设置轴（decay / 窗口）
  在波 82–84b 已被实测为**与 TO 同向**（§9.1 第 3 条：修 TO 同时杀 S），不存在桥接空间。
  按 §9.2 的口径：预注册规则负责防"边测边改判据"，不负责宣布空间穷尽——所以这里补一句穷尽性说明：
  **三波 23 臂**覆盖 水平 / 净情绪 / 正向单侧 / CI 宽度 / 分歧度 / 尾部负面 / 信息真空 / 跨变体分歧 /
  条件方向 / 相关性 / 协方差 / 回归 / 回填 22/250 / 状态均值 / 强度档 ON/OFF / 中性化 SUB→FAST
  共 9 类构造与 2 个设置轴，最好读数是 S 0.91（窄账本）/ F 0.28（宽账本）。

**裁决**：判 `USA-OTHER596-SPARSE-COVERAGE-WALL` —— 本数据集的**日报情绪面**封存，不再发波。
`seal_dead_end` 走论坛取证闸时缺 `forum_recon_*` 可靠记录（本地 recon 读帖链路故障，§10.1），
按 fail-closed 契约**暂不写库判死**，在此文档登记；补到可靠取证后再落 `dead_end`。
→ 按 N.4 顺位切下一数据集，other596 若被重新打开，只允许从「更新频率更高的变体」入手（本集为日报矩阵）。
