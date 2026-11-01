# insiders1 数据集画像（KOR / TOP600 / Delay=1）

> 手工维护。数据源：`get_datafields(KOR, insiders1, filter_sharpe=false)`，2026-10-30。
> 只测不决策；结论交波次设计。

## 0. 元信息

| 项 | 值 |
|---|---|
| dataset id | `insiders1` |
| category | **INSIDERS**（塔 **0 点亮**，乘数 **1.2** —— 全库最低档之一） |
| 字段数 | **9，全 VECTOR**；coverage **.3526**（四舍五入后 9 个字段完全一致 ⇒ 同一份报表的并列列） |
| aC 分布 | `gvkey` 178 / `shares` 111 / `value` 107 / `holdings` 57 / `price` 45 / `valueeur` 45 / `tradesignificance` 40 / `transaction_currency_code` 15 / `max_trade_price` 5 |
| 性质 | Compustat Global 口径的**内部人交易明细**（一次交易 = 向量中一个元素） |

## 1. 字段分类（按 description，不按名字）

### A. 交易量纲（可作强度信号）

| 字段 | 说明 | 备注 |
|---|---|---|
| `insd1_shares` | 本笔交易股数 | 无符号 |
| `insd1_value` | 本笔交易金额（**原币**） | 无符号；KOR = KRW |
| `insd1_valueeur` | 同上，欧元 | 与 `value` 同源换算 ⇒ **两者只能取一**（同源重复） |
| `insd1_price` / `max_trade_price` | 每股价格（区间报价取最低 / 取最高） | 二者构成同一笔的**价格区间** ⇒ 可做同源价差 |

### B. 持仓与重要性（★ 唯一可能带方向的字段）

| 字段 | 说明 | 备注 |
|---|---|---|
| `insd1_holdings` | **该内部人交易后的持股总数** | ⭐ 唯一有方向的量：同一内部人前后两笔之差 = 该人净买入/卖出 |
| `insd1_tradesignificance` | 交易重要性 1/2/3 | 平台给的**先验权重**，可作加权或门槛（非信号本身） |

### C. 元数据（禁作信号）

`insd1_gvkey`（公司 ID）· `transaction_currency_code`（币种代码）。

## 2. 名 vs description 差异表（★ 本集最大坑）

| 字段 | 名字暗示 | 实际 | 处置 |
|---|---|---|---|
| **（整集）** | "insiders" 通常含 buy/sell 标识 | **9 个字段里没有任何买卖方向码**（无 `acquired/disposed`、无 `transaction_code`） | ⛔ 不能直接构造「净买入」；只能走 §3 的持仓差分代理 |
| `insd1_holdings` | 可能是「本次变动股数」 | 是**交易后该内部人的持股总数** | 用 `ts_delta`/相邻笔差分才有方向；直接 `vec_avg` 是「当日活跃内部人的平均仓位」= 无经济含义 |
| `insd1_value` vs `insd1_valueeur` | 两个量 | 同一笔的两种币种 | 只取 `value`（原币），取 `eur` 会引入汇率噪声；**同源不可叠加** |
| `insd1_price` vs `max_trade_price` | 两个价 | 区间报价的下/上界 | 可做 `divide(max_trade_price, price)` 的**区间宽度**（流动性/议价代理），但覆盖率仅 .35 |
| `insd1_tradesignificance` | 可能是收益预期 | 平台给的 1–3 重要性分 | 当**门控/权重**，不当收益来源 |

## 3. 字段画像五问（A-1）

1. **时间维度**：**事件流**（每笔一条）。任何「水平」都无意义，必须聚合到股票-日（`vec_sum(shares)` / `vec_avg(holdings)`）或取差分。
2. **相对性**：只能用**排序**（`rank`/`group_rank`）；量纲跨股票差 6 个数量级（KRW 金额）。
3. **被定价的是谁**：内部人（大股东/高管）的**信息优势**。买 ⇒ 后续涨（信息+信号效应）；卖 ⇒ 弱预测（流动性/分散化动机混杂）。
4. **有无博弈**：有。KOR 家族控股普遍、内部人交易受披露约束但**跟风盘极强** ⇒ 需行业/规模中性化。
5. **事件性**：**强事件型 + 稀疏**（cov .35、非事件日为空）⇒ 铁律：**禁裸 rank，必须 `ts_backfill` 或 `trade_when` 门控**。
   ⚠ 本区前科：`insiders5` 实测「单腿负向、被 backfill 制造伪触发」 ⇒ 首波必须做 **backfill vs 门控 的对照腿**。

## 4. A-2 收益来源声明（主机制：内部人净买入的信息含量）

| 项 | 内容 |
|---|---|
| **谁在被定价** | 内部人（controlling family / 高管）相对外部投资者的**信息不对称** |
| **为什么会被错** | 内部人买入是**自利且高成本的信号**，市场对 KOR 小盘内部人买入反应不足（信息摩擦 + 披露滞后） |
| **错了多久修复** | 1–6 个月（Lakonishok & Lee 2001：买入后 12 个月仍有显著异常收益，前 3 个月最强）⇒ **窗口 66 主、252 辅** |
| **预期方向** | **净买入 ⇒ 后续涨**（做多腿）；净卖出**不构成可靠的做空腿**（动机混杂）⇒ 只做多侧，或长期/短期不对称处理 |
| **失效条件** | ① 无方向码 ⇒ 代理失真；② 家族传承式内部人交易（非信息驱动）；③ 覆盖率 .35 ⇒ 只有 1/3 股票有读数 |

## 5. 双通道取证

**通道 A（论坛）** —— ✅ **已取证（2026-10-30 04:31:40）**：`tools/forum_recon.py`，`question_key=e9c3384e7f`，`found=true / status=ok`，3 篇有效，写入 `KB/community_tpl_kb.forum_recon_entries[11..13]`。检索式 `insider trading`（0 篇有效）→ `insider buying`（3 篇，命中即收束）。

| post_id | 标题 | 票 | 可用性 |
|---|---|---|---|
| `35238443276567` | Alpha灵感-小公司的内幕新闻情绪因子 | 1 | ⭐ **唯一机制帖**：明写「增持 ⇒ 内部看好 ⇒ 利好；减持 ⇒ 利空」，与通道 B 的 Lakonishok-Lee 同向；但作者**自己没拿到字段**（"我目前的权限…没有找到"），**无模板、无回测** ⇒ 只能当方向句，不能当表达 |
| `43534263049239` | 【Alpha Idea】同源披露节奏差：insider × institution 残差对冲的周频化 | 57 | ⚠ **本区结构性不可用**：要求 insider × institution 双腿交叉（两套披露节奏做差）。KOR 的 institutions 塔**双数据集全死**（institutions6 死集 + `fund_holdings_panel` 判死）⇒ **无对侧腿可交叉**。仅继承一条几何纪律：两同源通道做差（`subtract`）而非相加 |
| `36944089777047` | 零预算网页端 LLM + notebook + markdown 指令交互流程 | 26 | ⛔ 与机制无关（工作流帖），不入设计 |

**裁决**：**A 有方向句、无模板** ⇒ 按 ②.d 属「B 有机制、A 无对应表达」⇒ **自建骨架**（本次 §7 已是自建形态）。与 insiders5 前科的关系见 §7 纪律④。

> ⚠ **不要重复同一检索式**：`insider trading` / `insider buying` 已跑完（status=ok）。若需再查，换 `"insd1"` / `"tradesignificance"` / `"transaction significance"` / `"10% shareholder"`。

**通道 B（论文）**：

| 文献 | 可证伪结论 | 可迁移性 |
|---|---|---|
| Lakonishok & Lee (2001, RFS) | 内部人**买入**组合随后 12 个月显著超额收益，卖出无显著负向 | ⭐ 主依据：只做多侧 |
| Jeng, Metrick & Zeckhauser (2003, REStat) | 买入-卖出组合年化 ~6% 异常收益，**收益主要来自买入腿** | 佐证「单侧」形态 |
| Cohen, Malloy & Pomorski (2012, JF) | **机会型**内部人交易可预测，**例行型**不可 | 本项目无 routine 标识 ⇒ **只能降级为假说**；用 `tradesignificance=3` 作机会型代理 |
| Fidrmuc, Goergen & Renneboog (2006, JBF) | 英国：董事买入的预测力显著强于卖出 | 非美样本，制度更近 KOR |

⚠ **文献偏误**：USA/UK 样本，披露制度与 KOR 不同；KOR 内部人交易多为家族内部转让 ⇒ **先当假说**。

## 6. 近十年覆盖验证（用户约束 4）

cov .3526 是横截面覆盖率，**不代表年份缺失**。Compustat Global 的内部人明细在 KOR 通常可回溯到 2000s，但平台从 2014 起算。
**判定法**：首波 2 条落地后立刻 `get_alpha_yearly_stats`；**首 3 年中任一为空 ⇒ 整集退出**（wave 189 sentiment27 就是这样判死的：2014–2018 全 0）。

## 7. 波次设计（wave 193，8 条；已 `preflight_expressions` 全清 `valid:true / unknown_fields:[]`，前 2 条为批 1）

⚠ **必要条件**：✅ ① 通道 A 取证完成（2026-10-30，`question_key=e9c3384e7f`，见 §5）；② 覆盖率探针（见 §6）——**首波批 1 落地后立刻读 `get_alpha_yearly_stats`**，2014 起任一空年 ⇒ 整集退出。

| 序 | 表达式（草） | 机制腿 | 目的 |
|---|---|---|---|
| 1 | `group_rank(ts_backfill(ts_delta(vec_avg(insd1_holdings), 66), 22), sector)` | 净买入代理（持仓变化） | 主腿正向 |
| 2 | `multiply(-1, <1>)` | 同上反向 | 铁律 B |
| 3 | `group_rank(ts_backfill(ts_delta(vec_avg(insd1_holdings), 22), 22), sector)` | 短窗差分 | 窗口对照（22 vs 66） |
| 4 | `group_rank(ts_rank(ts_backfill(vec_sum(insd1_shares), 22), 252), sector)` | **活动强度**（无方向） | 判别「方向」还是「关注度」在定价 |
| 5 | `group_rank(ts_rank(ts_backfill(divide(vec_sum(insd1_value), add(1, vec_sum(insd1_shares))), 22), 252), sector)` | 单笔均价（金额/股数 = 同源比率） | 同源比率几何 |
| 6 | `group_rank(ts_rank(ts_backfill(divide(vec_max(max_trade_price), vec_avg(insd1_price)), 22), 252), sector)` | 报价区间宽度 | 议价/流动性代理（⚠ 字段真实 id = `max_trade_price`，**无 `insd1_` 前缀**，2026-10-30 预检实测） |
| 7 | `trade_when(greater(vec_sum(insd1_tradesignificance), 2), group_rank(ts_backfill(ts_delta(vec_avg(insd1_holdings), 22), 22), sector), -1)` | 重要性门控 | 事件门控替代 backfill（对照腿 1/3） |
| 8 | `group_rank(ts_rank(ts_backfill(vec_sum(insd1_tradesignificance), 22), 252), sector)` | 加权活动强度 | 强度×重要性 |

**设计纪律**：① 全部 `insiders1` 单集 ATOM；② `industry` 禁用（KOR 铁律）；③ 1 vs 4 是**方向 vs 活动**的判别实验；
④ 1 vs 7 是 **backfill vs 门控**的对照（insiders5 前科的正面回答）。

### 7.1 实测结果（wave 193，2026-10-30 收批）

**结论：⛔ 数据集判死，insiders 塔判死。** 8 腿只发了批 1 的 2 条，预注册判死条件触发后剩 6 条未发即 kill（已 `dropped`）。

| alpha | 表达式核心 | S | F | 2Y | TO | DD | CW |
|---|---|---:|---:|---:|---:|---:|---:|
| `O0AK2nz7` | `ts_delta(vec_avg(insd1_holdings),66)` 正向 | −0.11 | −0.02 | +0.20 | .3035 | .4378 | **1.00** ❌ |
| `gJe70mGg` | 同式 `multiply(-1, …)` | +0.01 | 0.00 | −0.26 | .3037 | .4804 | **1.00** ❌ |

**四路归因**：

1. **【方向已双测】** 两腿同字段同窗、仅符号相反 ⇒ 铁律 B 完成。`max|S| = 0.11`、`max|2Y| = 0.26`，**两侧皆零信号**，不是方向猜错。
2. **【CW 结构性塌陷】** `CONCENTRATED_WEIGHT = 1.00 @2018-02-06`，与 S 符号无关。机理：`insd1_holdings` 是季频 VECTOR，`vec_avg` 后绝大多数标的为 0/NaN，
   有效档位极少 ⇒ `group_rank(sector)` 在稀疏面上退化成近二值 ⇒ 权重天然塌到单票。**这是数据形态缺陷，参数无解**。
3. **【逐年符号不稳】** `O0AK2nz7` 逐年 S：2014 0.00 / 2015 −2.13 / 2016 +0.18 / 2017 +1.42 / 2018 +1.59 / 2019 −1.62 / 2020 −0.10 / 2021 +0.06 / 2022 −0.40 / 2023 −0.72
   ⇒ 正负翻转 5 次、**S<1.0 年份 7/10** ⇒ 2Y 闸结构性不可达，且是 regime 依赖（换机制才行，不扫参数）。
4. **【TO 超带】** `.3035/.3037` = KOR 获胜带（.075–.136）的 2.2–4.0 倍。季频披露字段却给 0.30 换手 ⇒ 稀疏面抖动。
   按 `F = S·√(returns/max(TO,0.125))`，实测 returns −0.0129 / +0.0014 ⇒ **F 天花板 0.02**，与实测一致。

**覆盖**：PASS。longCount 248–323/年、shortCount 245–320/年，2014–2023 无空年 ⇒ **死因是机制+数据形态，不是覆盖**。

**继承（下一波准入）**：
- ⛔ 禁碰 insiders 塔（insiders5 天花板 1.05 + 本集 max|S| 0.11 ⇒ 塔死）。
- ⛔ 禁对 VECTOR 季频稀疏字段用 `vec_avg + group_rank(sector)` 裸形态（CW 必塌 1.0）。
  未来碰 VECTOR 类**必须先跑法 2 非零率体检**，非零率 <0.3 直接跳过。

## 8. 禁区

- **无买卖方向码** ⇒ 不许声称构造了「净买入」（只有持仓差分代理），A-3 概念块 `Logical Meaning` 必须写明。
- `insd1_value` 与 `insd1_valueeur` 同源，**禁同时入式**。
- `insd1_gvkey` / `transaction_currency_code` 禁作信号。
- VECTOR 必须先 `vec_*` 降维（`vec_avg`/`vec_sum`/`vec_max`）。
- 乘数仅 1.2 ⇒ 本集**优先级排在 news46 / risk 之后**；若前两波同类事件型仍 0 产出，考虑整类跳过。
