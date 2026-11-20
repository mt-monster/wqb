# MP69RYAk 双目标优化报告（2026-11-17 19:47 点名）

> 目标 A = 推到全闸；目标 B = 压算子。**判定：FOUND_BETTER_VARIANT——④d 盲区③（参数×设置交叉）挖出 decay 甜点，采纳 `d5aQjYaE`（decay60）全面碾压原件。零提交。**

## 一、原件画像

```
rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(quantity_institutional_shares_disposed, 252), 252, rettype=0))
```
IND/TOP500/d1/**decay126**/STATISTICAL/nanHandling OFF。**5 ops（3 distinct）**，与已提交 `O0Wkvqgd` 同残差骨架（`e7aeJoEd` 族），`rank`/`reverse`/`rettype=0` 承重已由该族实测确认 ⇒ **压缩通道关闭**。

| 项 | 原件值 | 判定 |
|---|---:|---|
| S / F / 2Y / sub | 2.98 / 2.25 / 2.79 / 1.64 | 全闸 PASS，Ra=0 |
| **self** | **0.6585** | 过闸但贴线（top `0mjk2ZQv` 为 ACTIVE 同族件 0.6585） |
| **prod** | **0.6699**（24h 缓存） | 过闸但贴线（余量 .03） |
| 塔 | IND/INSTITUTIONS ×1.0 + PV ×1.1（PV 12 已亮，INST 1→2 不点亮） | **边际 0** |
| 六维 | T1 −0.0043 / T2 −0.0022 / **T4 +1 新字段** | 软指标双降 + 新字段硬收益 |

族互相关：`0mjk2ZQv` 0.6585 / `RREnK5R1` 0.5706 / `O0Wkvqgd` 0.4356——全部非孪生，可共存。

## 二、④d 精调：decay 是主杠杆（本轮核心发现）

窗口变体（zscore/reg 126/504/混合）全测但**全部败于同窗 decay60 变体** ⇒ 窗口 252 已最优，**decay 才是主杠杆**。衰减曲线（表达式全程不变，纯设置层）：

| decay | alpha | S | F | 2Y | TO | prod | self | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 126（原） | MP69RYAk | 2.98 | 2.25 | 2.79 | 24.4% | 0.6699 | 0.6585 | 全闸但双贴线 |
| **60** | **d5aQjYaE** | **3.62** | **2.84** | **3.74** | 26.9% | **0.6585** | **0.6127** | **★ 全闸+双余量最优** |
| 30 | O0W9rYQp | 4.33 | 3.35 | 4.39 | 33.7% | 0.6993 | 0.5394 | prod 余量仅 .0007，极贴线 |
| 20 | E5QKpGqm | 4.60 | 3.40 | 4.72 | 40.2% | — | — | **HIGH_TURNOVER FAIL**（>0.40） |
| 15 | QP0Q333r | 4.73 | 3.34 | 4.82 | 45.9% | — | — | **HIGH_TURNOVER FAIL** |

**规律**：S/F 单调随 decay↓ 上升（信号原本未被足够平滑衰减），但 TO 同步↑，40% 闸在 decay<20 处断裂；prod 也随 TO↑ 走高（0.6585→0.6993）。**decay60 是「全闸 + 双余量」的唯一甜点**。

## 三、采纳判定

**`d5aQjYaE`（decay60）采纳，原件标 SUPERSEDED**（同表达式互相关必 >0.99，只能留一颗）：

| 维度 | 原件 decay126 | **采纳件 decay60** | Δ |
|---|---:|---:|---|
| S / F | 2.98 / 2.25 | **3.62 / 2.84** | **+0.64 / +0.59** |
| 2Y / sub | 2.79 / 1.64 | **3.74 / 1.87** | +0.95 / +0.23 |
| robust | 1.70 | 1.69 | −0.01（持平） |
| **prod** | 0.6699（余 .0301） | **0.6585（余 .0415）** | **−0.0114，安全边际 +38%** |
| **self** | 0.6585（余 .0415） | **0.6127（余 .0873）** | **−0.0458，安全边际 +110%** |
| 算子 / 塔 / 六维 | 5 ops / 边际 0 / T4+1 | 同 | 持平 |

符合 skill ④b 采纳判据三条全中：指标更好 + prod 不更高 + 算子不变。且这正是 **④d 盲区③（参数×设置交叉）** 的教科书案例——decay126 是历史遗留值，从未在最终 settings 下重扫。

## 四、提交权衡（交用户定）

- **推荐提交 `d5aQjYaE`**：全闸 + prod 余量 .0415 + self 余量 .0873，均为家族内最安全。
- **塔边际 0**（INSTITUTIONS 1→2 不点亮、PV 已亮）：不产生新点亮，但 T4 新字段 `quantity_institutional_shares_disposed` 是确定性六维收益。
- 提交前必做：稳健审计（近三年/负年检查）、方案 D、同席互相关（已测 0.6585 <0.7 OK）、ET 配额。

台账 `opmin_MP69RYAk`（IND, FOUND_BETTER_VARIANT）；全程 MCP 6 批 20 条，零临时脚本，零提交。

---

# 21:18 ATOM 化尝试（returns→institutions6 内部价格代理）⇒ 失败

> 用户问：能否找到 `returns` 的替换，变成 ATOM（IND/INSTITUTIONS ×1.0 单塔）。附加动机：本轮全部新仿真均报 `returns` Overused data 警告（PV 过度使用），换掉可顺带解除。

## 字段盘点（institutions6 全 11 字段，全 MATRIX，cov 0.992）

数据集内**无 returns/close**，但有天然价格代理：`market_value ≈ quantity × 成交价`。设计「value-on-quantity 回归取残差」= 机构行为未解释的价格漂移——金融含义与原信号近似。

## 实测 4 对（decay60 同 settings）

| 替换对 | S | 判定 |
|---|---:|---|
| market_value_disposed vs quantity_disposed（npaWqY28） | **0.37** | 崩 |
| aggregate_equity_institutions vs aggregate_share_institutions（3q0AP3eQ） | **−0.28** | 崩 |
| market_value_acquired vs quantity_acquired（N1POzqRg） | **−0.66** | 崩 |
| aggregate_equity_all_owners vs aggregate_share_all_owners（bla9zVdR） | **−0.58** | 崩 |
| （对照）d5aQjYaE 原信号 | 3.62 | — |

## 结论

**ATOM 化失败，`returns` 是承重腿**。原始信号的强度来自「市值回报 vs 机构处置量」的**跨源信息差**——机构自己成交的 value/quantity 一致性没有截面信息。这与 `E5Qrx2JG` 的 cap 去混失败同一教训：**语义近似替代 ≠ 指标等价，跨源信息差正是信号本体**。

附带发现：Overused data 是 WARNING 非硬闸（4 条新件 Ra 计数不含它），不构成提交障碍；`d5aQjYaE`（decay60）维持采纳建议，提交时带上该软标记即可。

零提交。

---

# 21:20 / 00:0x 「Overused data 警告怎么处理」——按 `docs/reference/forum_and_doc_tools_guide.md` 重查

> ⚠ **口径自纠**：21:20 首查时把「`search_forum_posts` 返回 0 命中」当成「论坛无讨论」——**违反指南 §2.2 取证纪律**。
> 该工具服务端总超时 120s、客户端仅 30s，且本次 7 次调用全部**瞬时返回空**（`navigation_failed=false`）——
> 属**工具故障**，不得解释为「论坛确认无解」。00:0x 已按指南规定的绕行路径重查。

## 一、按指南走通的路径（`get_documentation_page → 提取 posts/<id> → read_forum_post`）

| 步骤 | 结果 |
|---|---|
| `get_documentation_page("consultant-submission-tests")` | **权威取到全部提交测试清单**（10 项 criteria + 9 条 status message 表）——**无任何 data-usage / overuse 测试项** |
| `get_documentation_page("data")` | 「**Dataset Value Score** = 数据集**欠使用**度量，顾问应优先研究 Value Score 高的数据集」——即 usage 机制的**正向激励面** |
| `get_documentation_page("brain-genius")` | Genius 三级指标 = 提交数 / pyramid 数 / Combined OS 表现，**无 usage 惩罚项**；数据访问按等级开放 |
| `get_glossary_terms()` | 术语表**无「Overused data」条目**；有 `Dataset Value Score` / `Value Score`（= underutilization 激励）、`Grouping Field`（分组字段不计 pyramid/ATOM 惩罚） |
| `read_forum_post("8209806533015")`（How to avoid overfitting，8 条评论） | 工具**正常可用**（秒回全文+评论）；该帖未涉及 overused data |
| `search_forum_posts`（再试 2 次，含 data diversity） | **仍瞬时返回 0**（工具故障态，非证据） |

## 二、查证结论（基于文档权威 + 本仓实证）

| 渠道 | 结果 |
|---|---|
| **官方提交测试清单**（consultant-submission-tests，MCP 实读） | **无 data-usage 项** ⇒ Overused 不是提交闸门 ✅ 权威确认 |
| 术语表（get_glossary_terms，MCP 实读） | 无该条目；**Value Score = 欠使用激励** ⇒ 机制性质=引导数据多样性，非惩罚 |
| 论坛 | **search 工具故障（7 次瞬时空返回），按纪律记为工具故障**；read 通道可用但无相关帖被检出 ⇒ **结论记为「论坛未获证据」，不写「论坛确认无解」** |
| 官方帮助中心文章（警告内嵌链接） | 需 SSO 登录，WebFetch 不可达 |

## 实证口径（本仓自有数据，价值高于外部资料）

1. **位置与性质**：`Overused data` 不出现在 `is.checks`（18 项里没有对应项），而是**仿真回执的 status=WARNING 消息**（`ALPHA_DATA_CATEGORY_DIVERSITY` 事件，`property=regular`）——属于**元数据层提示**，不是闸门。
2. **不影响指标与提交链**：4 条报警告的新件 Ra failed 全为 0（`failed_ra_checks` 不含它）、指标完整产出；本仓已提交 ACTIVE 的 `O0Wkvqgd`（同样报过该警告）11-15 顺利 `201→ACTIVE`，其 IS checks 终值里 **DATA_DIVERSITY 已消失**（提交后该检查不保留），OS 期无任何 usage 相关惩罚。
3. **本仓先例**：11-15 `e7aeJoEd` 轮已实测记录「`Overused data` WARNING 不影响指标产出，可忽略」。

## 处理建议（按官方链接的语义 + 实证）

1. **当前处理正确：不阻断，记录为软标记**。它是平台对「该 PV 字段全网使用量过高」的提示（鼓励数据多样性），非账号配额、非提交闸。
2. **若要主动解除**，三条路（按代价排序）：
   - 换**同族低用量字段**（如 `quantity` 族换 `count` 族——但本轮已证 returns 不可换，见上节）；
   - 该字段在**其它 region/universe** 使用（usage 按 region+field 计）；
   - 等待**月度/季度使用量窗口重置**（官方链接名为 Usage **Management**，暗示周期性额度，但具体周期登录墙内无法核实）。
3. **提交侧动作**：在 description 的 data rationale 里如实披露（"the price-volume field carries a platform over-usage advisory, retained because it is load-bearing"）——与本仓软标记惯例一致。

**结论：官方提交测试清单无该测试 + 术语表把它归入「欠使用激励」（Value Score 反向）+ 本仓三轮实证（WARNING 不进 checks、不拦提交、ACTIVE 件无事后惩罚）⇒ 维持「记录软标记、不处理」；论坛一栏因 search 工具故障记为「未获证据」，不作否定结论。唯一值得做的主动动作是 description 披露。**

> **流程纪律（本次教训）**：以后任何论坛查证必须先读 `docs/reference/forum_and_doc_tools_guide.md`——
> `search_forum_posts` 有 30s/120s 超时不匹配，空返回一律记工具故障；正确路径是
> `get_documentation_page → 提取 posts/<数字> → read_forum_post`。
