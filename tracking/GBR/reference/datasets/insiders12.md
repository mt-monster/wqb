# GBR / insiders12（UK Insider Transaction Data，英国本土内幕交易，全 VECTOR）

> 塔：**insiders**（GBR/D1 乘数 **1.4**，当前 0/3 未点亮）
> 画像日期 2026-11-21 · 数据源 `mcp__wq-brain-http__get_datafields`（GBR/TOP700/D1，`filter_sharpe=false`，不传 `max_fields`）
> 本轮实拉：`count=7` / `platform_count=7` / `returned=7` / `complete=true` / `pages_fetched=1` ⇒ 单页全量，去重字段数=平台声明数=7，无需分片。
> ⚠ 全部 7 字段 `coverage=0.0` 是 **GBR coverage 元数据已知盲区**，不等于无数据（见 §6 六法实测 524/700 覆盖）。
> ⚠ 全 7 字段 type=VECTOR ⇒ 探针/信号一律先 `vec_*` 折叠（`vec_avg`/`vec_sum`/`vec_max`/`vec_count`），不得原生进 `rank`（类型不匹配必 FAIL）。

---

## 字段全表（平台实拉 7/7）

> 按 alphaCount 降序。第一列 = 平台真实字段 id；cov = 平台 coverage 元数据（GBR 全 0，盲区）；αC = alphaCount；uC = userCount。全部 VECTOR、dateCreated=`2026-07-01`、pyramidMultiplier=1.4。

| 字段 | 类型 | cov | αC | uC | 经济含义（平台 description） |
|---|---|---:|---:|---:|---|
| `insd12_mktprice` | VECTOR | 0.0 | **287** | 143 | 交易日每股市场价格（按披露原样，未复权） |
| `insd12_percent` | VECTOR | 0.0 | 74 | 41 | 事件后内幕人持股占比（直接披露值；依 GLTPercent 可能是边界值） |
| `insd12_positionchangetransactionamount` | VECTOR | 0.0 | 78 | 42 | 本次交易买入(+) / 卖出(−) 股数 |
| `insd12_sharesheld` | VECTOR | 0.0 | 35 | 23 | 交易后按官方披露的内幕人持股数 |
| `option_exercise_price_eur` | VECTOR | 0.0 | 10 | 9 | 衍生品/期权行权价（EUR） |
| `option_exercise_price_gbp` | VECTOR | 0.0 | 8 | 7 | 衍生品/期权行权价（GBP） |
| `option_exercise_price_reported` | VECTOR | 0.0 | 17 | 13 | 行权价（币种随上下文） |

> 平台实拉 αC 逐行：287, 74, 78, 35, 10, 8, 17（合计 509，均值 72.7）。uC 逐行：143, 41, 42, 23, 9, 7, 13（合计 278，均值 39.7）。

---

## 3. 聚合统计（基于平台实拉读数）

| 指标 | 值 |
|---|---|
| 字段总数 | 7（全部 VECTOR，无 MATRIX/GROUP） |
| coverage 分布 | 7/7 = 0.0（GBR 元数据盲区，非无数据） |
| alphaCount 合计 / 均值 | 509 / **72.7** |
| alphaCount 最大 / 最小 | 287（`insd12_mktprice`）/ 8（`option_exercise_price_gbp`） |
| userCount 合计 / 均值 | 278 / **39.7** |
| dateCreated | 7/7 = `2026-07-01`（同批 onboard；非老集死字段） |
| pyramidMultiplier | 7/7 = 1.4（insiders 塔，GBR/D1 **0/3 未点亮**） |
| αC=0 的字段 | 无（全部 ≥8） |

数据集级元数据（`get_datasets(GBR,TOP700,D1,category=insiders)` 实拉）：`id=insiders12` / `name=UK Insider Transaction Data` / `category=insiders` / `fieldCount=7` / `coverage=0.0`（同盲区）/ `userCount=190` / `alphaCount=448` / `valueScore=3.0` / `pyramidMultiplier=1.4`。
> 注：数据集 description 是模板串（描述 BBID/RIC 映射），与字段级 description 不符，属平台描述错配——以字段级 description 为准。

---

## 4. 字段族拆解（按经济机制分组）

| 族 | 字段 | 机制 |
|---|---|---|
| **A 交易金额族**（核心信号） | `insd12_positionchangetransactionamount`(αC78) | 买入(+) / 卖出(−) 股数：**天然双边**符号序列，内幕人知情交易方向与规模 |
| **B 持股规模族**（分母/水平） | `insd12_sharesheld`(35)、`insd12_percent`(74) | 交易后持股数（规模基准）、持股占比（%）：可作分母（交易额/持股数）或「利益绑定」水平 |
| **C 交易价格族**（门控/参照） | `insd12_mktprice`(287，全集最活跃) | 交易日成交价：内幕人择时价格（相对高位买入/低位卖出 → 反向信号） |
| **D 期权行权价族**（元数据，非信号） | `option_exercise_price_eur`(10)、`_gbp`(8)、`_reported`(17) | 仅期权/衍生品行权事件的合同价，**非股票交易信号**；三者为同一量的不同币种口径（同一事件多币种披露），不能当三条独立信号 |

**族间关系**：A 是唯一带方向的事件强度量（买/卖股数）；B 是规模基准（可作分母或「skin in the game」水平）；C 是事件价格（可作门控/参照）；D 是合同元数据。典型用法：A 作主腿（`ts_sum`/`ts_delta` 聚合），B 作分母（相对自身仓位调整幅度），C 作门控（内幕人成交价的相对水平）。

---

## 5. 可用性三分（信号 / 计数需归一 / 元数据不可用）

| 分类 | 字段 | 依据 |
|---|---|---|
| **① 可做信号** | `insd12_positionchangetransactionamount`(αC78)、`insd12_percent`(74)、`insd12_sharesheld`(35) | A 族天然双边（实测 275/241 多空）、B 族可做规模相对化；三者均为事件披露量 |
| **② 可做门控/分母** | `insd12_mktprice`(287) | 事件价格（未复权），作门控（价格相对位置）或与持股数构造成交均价；裸用是价格水平（非交易信号） |
| **③ 元数据不可用**（仅期权事件） | `option_exercise_price_eur`(10)、`_gbp`(8)、`_reported`(17) | 期权行权合同价，只在期权行权事件有值；三种币种口径同源，**不作独立信号** |
| **④ coverage 盲区**（非数据缺失） | 全部 7 字段 `cov=0.0` | GBR 已知盲区；六法实测 `percent` 524/700、`positionchangetransactionamount` 516/700 持仓 ⇒ 有数据 |

---

## 6. 六法评测

| 法 | 读数 | 结论 / 模板裁决 |
|---|---|---|
| **① 覆盖率** | `insd12_percent` **524/700（74.9%）**、`insd12_positionchangetransactionamount` **516/700（73.7%）**（2026-11-14 批 `1nnNiH8w44Rxbwp19oeaIYfv` @NONE/dec0/nanOFF）；本轮 2026-11-21 六法批 `1nYMFH3L4549bHXjgSqoiid` 复核全部 7 字段 | **本塔唯一高覆盖集**（对比 insider_agg_matrix 实测仅 14–24 只）；≥0.5 ⇒ **排除 ts_backfill 强制**（可裸用） |
| **② 非零率** | `percent` 法2 = 524（与法1 同数）⇒ 零值可忽略；`positionchangetransactionamount` 天然双边 275/241 | `percent`：**排除 trade_when 门控**（零≈0）；`positionchange`：双边 ⇒ 直接作方向信号 |
| **③ 更新频率** | `percent` N=22 变化 **446/524（85%）** ⇒ **日更偏高**；`positionchangetransactionamount` 变动额日更 | **允许短窗 5/22**；不做长窗平滑（同塔 insider_matrix 实证 `ts_mean21` 把 TO 1.46→0.216 但 2Y 1.64→0.46 ⇒ 事件信息集中在当日，平滑即磨平） |
| **④ 量纲** | `positionchange` 股数量纲、`percent` %、`mktprice` 价格、`sharesheld` 股数 | 全部需 `rank`/`group_rank` 去量纲；**禁裸 add 混腿**（股数 vs 价格 vs % 量纲不同） |
| **⑤ 中心/形态** | `positionchange` 原始 lc/sc=275/241 **天然双边**（多头 275 / 空头 241）；`percent` 裸用 524/0 **单边多头**（规模暴露） | `percent` 须行业中性化后再用；**变动额字段是主信号首选** |
| **⑥ 分布** | `positionchange` 零均值近对称（买卖对称）；`percent` 右偏（持股占比上限 100%）；`mktprice` 右偏长尾 | 右偏项先 `rank`/`winsorize`；`ts_zscore` 自身标准化会把 S 砍半（同塔实证 1.32→0.66）⇒ **不用 ts_zscore 自身历史标准化** |

**合成产物（字段 → 模板白名单）**：

- 合法模板白名单：
  - `group_rank(ts_sum(vec_avg(insd12_positionchangetransactionamount), N), sector|industry)`，N ∈ {5, 22, 66}
  - `group_rank(divide(ts_sum(vec_avg(positionchange),66), add(abs(ts_mean(vec_avg(sharesheld),252)),1)), sector)`（相对自身仓位调整幅度）
  - `group_rank(ts_delta(vec_avg(insd12_percent), 22), industry)`（持股占比变化；须先行业中性化）
  - `group_rank(ts_mean(vec_avg(insd12_sharesheld),252), industry)`（利益绑定水平）
  - 事件价格门控：`trade_when(...)` 用 `insd12_mktprice` 的相对位置
- 排除模板 + 理由：
  - `trade_when` 门控（`percent` 零≈0）
  - `ts_backfill` 强制（覆盖 74% ≥0.5）
  - 长窗平滑（`ts_mean(·,21+)` 磨平事件信息）
  - `ts_zscore` 自身历史标准化（S 砍半）
  - `insider_agg_matrix`（同塔，实测仅 14–24 只覆盖，S 0.66–0.87 无统计意义）
  - `earnings_sent_matrix`（同塔旁集，实测仅 14 只）
  - 期权行权价三字段作信号

---

## 7. GBR 判据核验（cov 全 0 为何不判 excluded）

1. **排除规则**：cov 全 0 不得直接 `excluded`；insiders12 实测 524/700 覆盖（六法法1）即铁证。
2. **本集实测反证**：GBR `backtest_results` 中 `code LIKE '%insd12_%'` 回测最高 S=1.27（`wpQ0LNk6`，含 insd12 字段的组合件）、纯 ATOM 最高约 1.0（2026-11-14 批）——数据真实存在，`excluded` 条件不成立。
3. **结论**：`verdict=needs_probe`；本轮已按 v11 逐字段 type 生成 NONE 探针（全 VECTOR ⇒ `vec_avg` 折叠）。

---

## 8. 本轮实测命令与读数（可复核）

- 平台全量：`get_datafields(region=GBR,dataset_id=insiders12,universe=TOP700,delay=1,filter_sharpe=false)` ⇒ `count=7 / platform_count=7 / returned=7 / complete=true / pages_fetched=1`。
- 数据集元数据：`get_datasets(region=GBR,universe=TOP700,delay=1,category=insiders)` ⇒ `fieldCount=7 / alphaCount=448 / userCount=190 / coverage=0.0 / valueScore=3.0 / pyramidMultiplier=1.4`。
- 探针校验：`preflight_expressions(10 条 VECTOR 折叠探针,dataset_id=insiders12)` ⇒ `valid=true / unknown_fields=[] / vector_fields=7`（全部 VECTOR 已识别）。
- 六法批：`create_multi_simulation(...)` ⇒ `multisimulation_id=1nYMFH3L4549bHXjgSqoiid`（10 臂，NONE/dec0/nanOFF/trunc0，2026-11-21 派发）。
- 历史六法读数：2026-11-14 批 `1nnNiH8w44Rxbwp19oeaIYfv`（NONE/dec0/nanOFF）——`percent` 524/700、`positionchangetransactionamount` 516/700、`percent` N=22 变化 446/524。

---

## 9. 证据闸（论坛 + 论文）

### 论坛（`search_forum_posts_local` 实检，2026-11-21）

| 帖 | 结论 |
|---|---|
| GBR/TOP700 挖矿复盘（`44550587290007`） | insiders12 仅「浅探 1 条」；深挖面未穷尽 ⇒ 本轮回测立项理由 |
| Alpha Design Guide: Master ts_backfill & ts_rank（`44491324058775`，6赞） | `ts_backfill` 适用于**更新不频繁/不规则**（含 insider-trading 数据）；但**勿对高频数据盲用** ⇒ 与六法③「日更 85%」冲突时以后者实测为准（本集可裸用） |
| 如何不花钱用 AI Agent 挖 Alpha（`44555293348631`） | 仅方法论背景，无本集配方 |

### 论文（`paper_search.py --diverse` 实跑，2026-11-21，≥5 篇 ∧ ≥3 作者过闸）

| 论文 | 机制 → 对应字段/模板 |
|---|---|
| **Fidrmuc, Goergen & Renneboog (2006)**, "Insider Trading, News Releases, and Ownership Concentration", J. Finance, doi:10.1111/j.1540-6261.2006.01008.x | **UK 数据**：内幕人买入在公告前有显著超额收益，卖出信号弱；持股集中度调制信息含量 ⇒ 支持「买入为主信号、卖出作对照」+ `percent`/`sharesheld` 作调制/分母 |
| **Lakonishok & Lee (2001)**, RFS（论坛帖引用） | 聚合内部人买入预测正异常收益；**群聚（多人同窗）信息量最高**；卖出预测力弱 ⇒ `ts_sum(positionchange, 5)` 群聚爆发形态 |
| **Cohen, Malloy & Pomorski (2012)**, JF（论坛帖引用） | 预测力集中在「机会型」交易（无固定模式）；常规型无信息 ⇒ 用变化/异常形式（非原始买卖总量） |
| Insider Trading Restrictions and Informed Trading in Peer Stocks (2022/2025, doi:10.1287/mnsc.2022.02907) | 内幕交易限制外溢到同业 ⇒ sector 分组轴 + 同业溢出 |
| Is "Not Trading" Informative? (2021/2022, doi:10.1080/0015198x.2021.1984825) | 不交易本身含信息 ⇒ 事件稀疏性可作门控（`vec_count` 频率） |
| Trading Strategies of Corporate Insiders (2017, doi:10.1016/j.finmar.2017.04.001) | 内幕人交易策略异质性 ⇒ 多窗（5/22/66）聚合 |

---

## 10. 小结

- insiders12 = **GBR 本土（UK）内幕交易**、全 VECTOR 7 字段、insiders 塔 **0/3 未点亮**、覆盖 74%（同塔最高）。
- 主信号 = `insd12_positionchangetransactionamount`（天然双边）；`percent`/`sharesheld` 作规模/占比；`mktprice` 作门控；期权三个行权价字段**不作信号**。
- 六法裁决 → 模板白名单见 §6；六法批 `1nYMFH3L4549bHXjgSqoiid` 已收割（法1 覆盖：mktprice/percent/sharesheld 各 525、positionchange 520）。
- 历史天花板：纯 ATOM ~1.0（2026-11-14）、含 insd12 组合最高 S1.27；**塔未点亮，D2/D6 未穷尽 ⇒ 不判死（PROVISIONAL）**。

---

## 11. 批 C · 文献模板 10 臂实测（2026-11-21，SUBINDUSTRY/decay4/trunc0.08/nanON）

`multisimulation_id=1v7FJNcVx4xpbP01eYqcXPam`（10 臂）

| 臂 | 机制（文献锚） | 表达式核心 | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| gJaXRwwv | 群聚爆发 5d（LLS 2001） | `group_rank(ts_sum(vec_avg(positionchange),5),sector)` | **−0.58** | −0.22 | −0.32 | 2.9% |
| YPa82nnA | 群聚 22d | `...ts_sum(...,22),sector` | −0.66 | −0.27 | −0.16 | 2.6% |
| j2ao9WWe | 群聚 66d | `...ts_sum(...,66),sector` | −0.65 | −0.26 | +0.01 | 2.3% |
| omaR3AAk | 群聚 66d @industry | `...ts_sum(...,66),industry` | −0.65 | −0.26 | +0.04 | 2.5% |
| 1YWOa1Lk | 相对仓位调整（CMP 2012） | `ts_mean(divide(positionchange,abs(sharesheld)),66)` | −0.32 | −0.13 | −0.66 | 2.2% |
| QP0O2qj5 | 占比变化 22d | `group_rank(ts_delta(vec_avg(percent),22),industry)` | −0.13 | −0.03 | −0.37 | 9.9% |
| 58Jra39z | 利益绑定水平（LLS） | `group_rank(ts_mean(vec_avg(sharesheld),252),industry)` | −0.30 | −0.12 | −0.58 | 1.7% |
| pwaxVoE3 | 多笔聚合 66d | `group_rank(ts_sum(vec_sum(positionchange),66),sector)` | **−0.70** | −0.29 | −0.24 | 2.2% |
| qM7OPvzK | 时序标准化 252 | `group_rank(ts_zscore(ts_sum(vec_avg(positionchange),66),252),sector)` | −0.29 | −0.11 | −0.84 | 2.6% |
| E5QNgYaJ | 交易笔数频率 | `group_rank(ts_sum(vec_count(positionchange),66),sector)` | −0.17 | −0.05 | −0.40 | 1.7% |

**结论（本轮最重要）**：
1. **10/10 臂全负**（S −0.13 ~ −0.70）⇒ **文献方向（Laksonishok-Lee 买入正预测）在 GBR/UK 数据上不成立**——UK 内幕人「买入」在此区间预告**负**超额收益（或信号被 13F 类披露滞后/事件噪声淹没）。
2. **取反后天花板 ≈ +0.70**（最负臂 −0.70）⇒ 即便方向反转，距 S 闸 1.58 仍差 0.88；insiders12 的**信号强度上限 ~0.7**（在 D1 结构层）。
3. TO 极低（1.7–2.6%，仅 percent 变化臂 9.9%）= 季度/事件稀疏、持仓几乎不动 ⇒ 不是「快信号」而是「慢状态」。
4. 该集**未到判死**（S 0.5–1.0 属「信号带」），但本轮 D1 结构（10 模板）已尽；D2/D3/D4/D6 仍可再试（未穷尽）。
5. ⚠ **反向信号注意**：insiders12 若取反，需重新验证文献机制（UK 内幕人卖出/买入信息含量可能与美国相反——Fidrmuc et al. 2006 的英国样本已提示公告后反转）。