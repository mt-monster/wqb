# other106 数据集画像（KOR / TOP600 / Delay=1）

> 手工维护。数据源：**平台 `get_datafields(KOR, TOP600, D1, dataset=other106, filter_sharpe=false)` 实测 15/15 字段**（2026-10-30，权威）。
> 塔：**OTHER**（金字塔未点亮，倍率 1.6）。category 名 = other，**用户约束 5 的禁止组腿域**（PV/MODEL/OTHER 之间不得两两组腿）⇒ 本集只能做 **ATOM**。

## 0. 元信息

| 项 | 值 |
|---|---|
| dataset id | `other106` |
| category | **OTHER**（塔 0 点亮，乘数 1.6） |
| 字段数 | **15**，**全部 VECTOR**（必须先 `vec_avg` 降维） |
| 覆盖率 | **.4032–.4040**（全字段一致）⇒ 低于 0.4 线，**必须 `ts_backfill`** |
| 本质 | **KOSPI 指数成分 / 公司行为调整文件**（`ospi` = OSPI = KOSPI）：变动前(`_cls`, close-side/source) vs 变动后(`_nxt`, next) 成对 |
| 拥挤度 | **极低**：单字段 aC 9–55，最高 `index_share_nxt`=55 / `newshares_following_rightsissue`=41 |

⚠ **覆盖率 .404 的含义**：TOP600 含 KOSDAQ 股票，而本集只覆盖 KOSPI（`ospi`）成分 ⇒ 缺的 60% 是**结构性不在域**，不是数据稀疏。
⇒ 十年覆盖大概率 PASS（KOSPI 成分数据 2010s 就存在），但**首波必须用 `get_alpha_yearly_stats` 实核**（用户约束 4）。

## 1. 字段分类（按 description 语义）

### A. 成对「变动前 / 变动后」—— ★ 本集唯一有价值的资产

| 变动前 | 变动后 | 语义 | aC（cls/nxt） | 可用机制 |
|---|---|---|---|---|
| `oth106_ospi_ca_eq_free_float_factor_cls` | `..._nxt` | **自由流通比例因子** | 19 / 19 | 流通盘扩张 ⇒ 供给冲击 |
| `oth106_ospi_ca_eq_index_share_cls` | `..._nxt` | **指数内份额（权重）** | 23 / **55** | 被动资金权重再平衡 |
| `oth106_ospi_ca_eq_capping_factor_cls` | `..._nxt` | **权重封顶因子（CAP Rate）** | 19 / 13 | 封顶调整 ⇒ 强制减仓 |
| `oth106_ospi_ca_eq_adjusting_factor_cls` | `..._nxt` | **权重调整因子** | 20 / 30 | 同上，口径更粗 |
| `oth106_ospi_ca_eq_price_cls` | `..._nxt` | **变动前/后收盘价** | 27 / 17 | 除权/拆股/配股价格比 |

**关键未知（决定骨架，见 §3 双骨架）**：`_cls` / `_nxt` 是**每日快照**（大多数日子相等）还是**仅事件日有值**？
- 若每日快照 ⇒ `divide(nxt, cls)` ≈ 1 恒定、`ts_delta(free_float, N)` 有意义。
- 若仅事件日 ⇒ 比值在事件当天 = 调整幅度、其余日 NaN ⇒ 是**纯事件幅度**，必须 `ts_backfill` + 衰减。
⇒ **本集设计成「同一字段两种读法各一条」的判别实验**，不猜。

### B. 事件量（单侧字段）

| 字段 | aC | 语义 | 处置 |
|---|---|---|---|
| `oth106_ospi_ca_eq_newshares_following_rightsissue` | **41** | **配股新增股份数** | ⭐ 稀释事件幅度：配股 ⇒ 供给↑ ⇒ 负向。需 `ts_backfill` + 事件衰减 |

### C. 纯元数据（**禁作信号**）

`index_code1`(15) / `index_code2`(9) / `ksic_cls`(14，KSIC 六位分类码) / `slc_ciik`(11，KRX 行业码)
⇒ 分类码。**平台未标 GROUP 类型**（均为 VECTOR 浮点）⇒ **也不能当 `group_*` 分组轴**，只作去重识别。

## 2. 名 vs description 差异表（★ 陷阱）

| 字段 | 名字暗示 | description 实际 | 处置 |
|---|---|---|---|
| `..._capping_factor_*` | 上限因子 | "**CAP Rate** before/after change" | 是**封顶比率**不是市值上限；比值方向需实测 |
| `..._index_share_*` | 指数份额 | "INDEX SHARE before/after change" | 与权重同义，但分母未知 ⇒ **只取比值/差分，不取水平** |
| `..._price_cls` | 收盘价 | "Closing Price **before change**" | 是**调整前**价，不是复权价；`divide(nxt,cls)` = 调整比 |
| `ksic_cls` | 行业 | "Korea Standard classification **code (6digit)**" | 6 位码是序数不是数值 ⇒ **禁裸当连续值**，也非 GROUP 类型 |
| `newshares_following_rightsissue` | 新增股份 | 无 before/after 对 | 单侧事件流 ⇒ 只有**非零日**有信息 |

## 3. 字段画像五问（A-1）

1. **时间维度**：**事件 / 存量快照混合**。`free_float`/`index_share` 是存量（水平变化慢），`price`/`newshares` 是事件。
2. **相对性**：**全部是「自身历史」相对量**（调整前 vs 调整后、当期 vs 上期）⇒ `ts_delta`/比值 优先于横截面 `rank`。
3. **被定价的是谁**：**被动 / 指数跟踪资金**。成分与权重变动迫使它们机械买卖，与基本面无关。
4. **有无博弈**：有。权重调整是公开日历事件 ⇒ 存在抢跑（front-running）与事后退潮两段。
5. **事件性**：**是**（除 free_float 水平外）⇒ `trade_when` 或 `ts_decay_linear` 门控，**禁裸 rank 事件幅度**。

## 4. A-2 收益来源声明（主机制：指数机制 → 供给冲击 → 反转）

| 项 | 内容 |
|---|---|
| **谁在被定价** | **指数跟踪 / 被动资金**（KOSPI200 跟踪盘 + 全球 ETF 的韩国腿）。它们对成分与权重变动**无弹性**：权重上升必须买入，下降必须卖出。 |
| **为什么会被错** | **需求曲线向下倾斜**（Shleifer 1986）——被动买压不是信息，是机械调仓 ⇒ 价格暂时偏离基本面，随后回吐。这是**制度约束**造成的错误定价，不是行为偏差。 |
| **错了多久修复** | 事件窗口 5–22 日：调整生效日前后买压达峰，之后 2–6 周回吐（Harris–Gurel 1986 的 temporary vs permanent 分解）。⇒ 主窗 22，辅助 66。 |
| **预期方向** | **权重 / 自由流通 / 指数份额上升 ⇒ 生效后短期上涨、随后反转 ⇒ 做空反转腿**；份额下降 ⇒ 做多修复。**方向必须正反各测**（铁律 B）。 |
| **失效条件** | ① 事件极稀疏（若一年只有几次全市场调整，截面几乎全 0/1 ⇒ S 不可信）；② 调整幅度极小（比值≈1）时是纯噪声；③ 若 `_cls`/`_nxt` 实为同日两份快照而非事件对，则本机制无对象。 |

## 5. 双通道取证

**通道 A（论坛）** —— ✅ **已检索（2026-10-30 04:18，`tools/forum_recon.py`，question_key `a4c9cbfeb8`，结果入 `KB/community_tpl_kb`）**：
`found=true` / 6 篇，但**逐条核读后判定：没有一篇是「指数权重调整 / 纳入调出」专属配方** —— 关键词命中是宽匹配（帖子正文含 index/weight 等词）。

| 命中帖 | 与 other106 的关系 |
|---|---|
| 「10 个超级高效好用的 ARC/GLB 模板」142 赞 | 通用骨架库；⚠ 其首条主模板用 `vector_neut` —— **REGULAR 不可用**（顾问专属，见 KB ghost 清单），照抄即整批 ERROR |
| 「如何统计得到的字段数 / 多地区因子一起检验」 | 工具向，无机制 |
| 「用节点和边组成的 graph 直观对比 alpha」 | 事后去重法，与机制无关 |
| 「如何拯救高 turnover 因子」179 赞 | ⭐ 唯一可用纪律：`return = turnover × margin` ⇒ 企业行动类低频信号必须把 TO 压到底（decay / hump / 长窗），否则 margin 撑不住 |

⇒ **诚实结论：A 通道对本机制「无专属表达」**（不是工具故障；`status=ok`），下波不应再用同样检索式空转。
**可继承的非机制纪律**：① `vector_neut` 禁用；② 低频企业行动信号优先压 TO（本波已用 `ts_rank(…,504)` 长窗 + 第 7 条 `hump`）。

**通道 B（论文）**：

| 文献 | 可证伪结论 | 本区可迁移性 |
|---|---|---|
| **Shleifer (1986, JF) "Do Demand Curves for Stocks Slope Down?"** | S&P500 纳入 ⇒ 公告后 +2.79%，且**永久不回落** ⇒ 需求曲线向下倾斜 | 机制核心。但原文是**纳入事件**（本集是权重变动）⇒ 迁移到「份额变化」需降级为假说 |
| **Harris & Gurel (1986, JFE)** | 纳入效应分解为 temporary（指数买压，约 +3.5%）+ permanent（约 +2%）⇒ **temporary 部分会反转** | ⭐ 本波主依据：给出「事件后反转」的时间窗与方向 |
| **Greenwood (2008, RFS)** | Nikkei 225 权重变动 ⇒ 非基本面共动（excess comovement），权重↑的股票随后跑输 | ⭐ **最贴本集**：同属权重调整 + 亚洲市场 + 给出反转方向 |
| **Kaul, Mehrotra & Morck (2000, JF)** | 加拿大 TSE300 权重调整 ⇒ 需求曲线向下倾斜的直接证据 | 佐证权重（而非仅纳入）也有效 |
| **Petajisto (2011, JFQA)** | 指数溢价随指数化程度上升 | 解释 KOR 外资 ETF 占比高 ⇒ 效应可能更强 |

⚠ **文献偏误**：全部是 **USA / JPN / CAN 大市值**样本；KOR 的 KOSPI 指数化程度低、散户占比高 ⇒ **被动买压的比例可能小得多**，效应可能被噪声淹没。**先当假说，本区实测定生死**。

**双通道裁决**：目前 **B 有机制、A 无表达** ⇒ 按 ②.d 这是「最有价值」情形 —— **按 A-1 五问自建骨架**，用论文的机制句定形态（比值/差分 → 时序自归一 → 反向）。

## 6. 近十年覆盖验证（用户约束 4）

⚠ 覆盖率 .404 是**结构性不在域**（非 KOSPI 成分），不代表时间上缺。
**判定法**：首波回测后立刻 `get_alpha_yearly_stats`，逐年 `longCount` 是否非零；**首 3 年任一为空 ⇒ 本集不满足十年约束，整集退出**。

## 7. 波次设计（wave 191 拟）

**断言**：本集只有 1 个机制（指数/流通盘供给冲击），所以波次是**判别实验 + 方向对照**，不是「8 个不同想法」。

| 序 | 表达式（草） | 判别目标 |
|---|---|---|
| 1 | `group_rank(ts_delta(vec_avg(oth106_ospi_ca_eq_free_float_factor_cls), 22), sector)` | **读法 A（每日快照）**：流通盘扩张 → 供给 → 后续跌（正向臂应为负） |
| 2 | `group_rank(multiply(-1, ts_delta(vec_avg(oth106_ospi_ca_eq_free_float_factor_cls), 22)), sector)` | 同式反号（铁律 B） |
| 3 | `group_rank(ts_backfill(divide(vec_avg(oth106_ospi_ca_eq_index_share_nxt), vec_avg(oth106_ospi_ca_eq_index_share_cls)), 22), sector)` | **读法 B（事件幅度）**：份额调整幅度 → 被动再平衡 |
| 4 | `group_rank(ts_backfill(divide(vec_avg(oth106_ospi_ca_eq_capping_factor_nxt), vec_avg(oth106_ospi_ca_eq_capping_factor_cls)), 22), sector)` | 封顶调整 ⇒ 强制减仓 |
| 5 | `group_rank(ts_backfill(vec_avg(oth106_ospi_ca_eq_newshares_following_rightsissue), 22), sector)` | 配股稀释幅度 → 供给↑ → 负向 |
| 6 | `group_rank(ts_backfill(divide(vec_avg(oth106_ospi_ca_eq_price_nxt), vec_avg(oth106_ospi_ca_eq_price_cls)), 22), sector)` | 除权/拆股调整比 → 事件强度 |
| 7 | `group_rank(ts_decay_linear(ts_backfill(divide(vec_avg(oth106_ospi_ca_eq_index_share_nxt), vec_avg(oth106_ospi_ca_eq_index_share_cls)), 22), 66), market)` | 事件回吐窗口 66 + market 轴（对照 sector） |
| 8 | `group_rank(ts_rank(vec_avg(oth106_ospi_ca_eq_index_share_nxt), 504), sector)` | **阴性对照**：份额水平（应无信号，若这支出信号 ⇒ 是规模因子泄漏，整波作废） |

**第 8 条是护栏**：水平读数若出强信号，说明本集在偷市值/规模暴露，前面的「事件」读数一律不可信。

**准入（继承 188/189 的铁律）**：
- 分组轴 **只用 `sector` / `market`，禁 `industry`**（三星+海力士 >50% KOSPI ⇒ 退化成 0/1）。
- 每批 2 条串行；批 1 落地后**第一件事读 `get_alpha_yearly_stats` 验十年覆盖**。
- 事件型 ⇒ **CW 是默认故障**，先看 CW 再看 S（roadmap §2）。

### 7.1 wave 190 实测（2026-10-30，**本波 = FAIL，机制性**）

⚠ 实发版与上表草稿有改动（加 `ts_backfill(·, 22)` 解覆盖、第 3 条改 `ts_delta(比值)` 取**变化**而非水平、第 5–8 条改 `ts_rank(·, 504)` 归一）——**实发式以 ckpt_w190 为准**，8 条全过 gate、probe 批豁免闸 6。

| 批 | 腿 | alpha | S | F | TO | 2Y | 结论 |
|---|---|---|---|---|---|---|---|
| 1 | 1 | `d5WeomjK` | **−0.75** | −0.32 | .4051 | 0.01 | 本波最高 \|S\|，**十年单调阴跌**（PnL −7.83M） |
| 1 | 2 | `QPvmgj7g` | 0.58 | 0.22 | .4051 | **−0.08** | 反向后 2Y 转负 ⇒ 只是 2015–2019 单段 |
| 2 | 3 | `wpQXPbql` | −0.24 | −0.06 | .42 | −0.43 | **核心假设（同源比值 Δ）无信号** |
| 2 | 4 | `LLMOrZW2` | 0.04 | 0.00 | .42 | 0.15 | 反向零信号 |
| — | 5–8 | — | — | — | — | — | **未发即 kill**（预置判据） |

**判据触发（预置于开波前）**：批 1 落地后 max|S| < 1.0 且 max|2Y| < 1.0 ⇒ 剩余腿不发。实测批 1 = 0.75 / 0.08、批 2 = 0.24 / 0.43 ⇒ **两批均触线**，批 3–4 kill，pipeline 终止。

**⭐ 覆盖闸首次 PASS（本区本轮唯一正面读数）**：`get_alpha_yearly_stats(d5WeomjK)` 2014–2023 `longCount` 逐年 **267–347**，无空年 ⇒ other106 **满足用户约束 4**。对照 sentiment27（2014–2018 连续 5 年 longCount=0，wave 189 判死）⇒ **本波死因是机制，不是数据**，这条读数对后续任何 other106 尝试都成立、不需复验。

**归因（铁律 E 分解，不是因子拖累）**：
- `d5WeomjK` raw PnL 十年单调阴跌至 **−7.83M**，仅 2014/2020 横盘；同一条的 `investability-constrained-pnl` 终值 **+0.51M** ⇒ 两条曲线大幅背离，但**两者都没有单调上行** ⇒ 判「信号自身无 alpha」，不判「换中性化档可救」。
- 反向腿 `QPvmgj7g` S +0.58 但 2021 +0.25 / 2022 +0.26、2Y −0.08 ⇒ 反号捡到的是 **2015–2019 单段行情**，不构成稳定机制。
- 核心腿（`index_share_nxt/cls` 的 22d 变化）S −0.24 / 反向 +0.04 ⇒ **同源比值并未抵消噪声**，指数份额变动在 KOR D1 上已被套利定价。
- **TO 是第一性死因之一**：4 腿 TO .4051/.42，是 KOR 成功配方带（.075–.136）的 3–5 倍；但降 TO 只修 F，**不能把 |S| 0.75 拉到 1.58** ⇒ 本波刻意**不做** hump/decay 平滑实验（不把参数杠杆当第一根杠杆）。
- **CW 仍硬伤**：批 1 两条 `CONCENTRATED_WEIGHT=1.0 @2016-03-04`（批 2 .567），是本区事件类数据通病；即使 S 达标也须先解 CW。
- **金字塔归属已实证**：harvest 返回 `KOR/D1/MACRO ×1.4` ⇒ 与 roadmap「macro→other」的归属一致。

**继承（写进后续波的准入条件）**：
1. other106 的「指数供给冲击」机制在 KOR D1 **关闭**，不再投主攻槽。
2. 若再碰本集，只剩「成分变更 `trade_when` 事件 + 属性差分」一条未测轴，且**必须先解 CW**。
3. 文献（USA/JPN/CAN 大市值）的被动买压结论**在 KOR 不可迁移**：KOSPI 指数化程度低 + 散户占比高 ⇒ 被动买压被噪声淹没（与 §5 的文献偏误预判一致）。

## 8. 禁区

- `index_code1/2`、`ksic_cls`、`slc_ciik` **禁作信号**（分类码；且非 GROUP 类型 ⇒ 也不能当分组轴）。
- `_cls` / `_nxt` **禁跨字段相加**（`add(nxt, cls)` = 混信号铁律违规）；**只允许比值 / 差分**（同源单信号）。
- 本集属 **OTHER** ⇒ **不得与 PV / MODEL / OTHER 字段组腿**（用户约束 5）；与其它 category 组腿全库 ≤5 且本集暂不动用。
- 全 VECTOR ⇒ 每个字段必须 `vec_avg`，**禁裸字段**。
- 覆盖率 .404 ⇒ 未 `ts_backfill` 的裸式覆盖不足，勿当成「信号弱」误判。
