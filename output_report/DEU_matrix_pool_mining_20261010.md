# DEU 未测 MATRIX 池系统性开采报告（2026-10-10）

> 执行依据：用户指令「系统性开采未测 MATRIX 池；没有灵感要及时查论坛和外部论文；用算子务必考虑所有可能情况」
> 范围：**锁死 DEU**（用户明令，已入 `MEMORY.md` 铁律区）

## 一、结论摘要

**五轮 40 条（W258–W262）零产出，但瓶颈已精确定位且唯一。**

| 轮次 | 对象 | 结构 | 结果 |
|---|---|---|---|
| W258 | model26 / pattern_scores / analyst7 代表 8 个 | `group_rank(字段, sector)` | S −0.75 ~ +0.50 |
| W259 | 同上 8 个 | `zscore` / `normalize`（无 rank） | S −0.90 ~ +0.88 |
| W260 | model264 裸字段 8 个 | **裸字段**（帖主方法第一步）| **8/8 全负（−0.36~−0.60）** |
| W261 | model264 翻转 8 个 | `reverse` + `group_rank` | **转正，但仅 0.22~0.64** |
| W262 | model264 两字段合规组合 8 个 | `subtract(rank,rank)` / `group_rank(·,bucket(rank(·)))` / `ts_corr` / `divide` | S −0.67 ~ +0.42 |

## 二、第一步：未测 MATRIX 池的系统分类（不盲扫）

**DEU 未测 MATRIX（cov≥0.9）= 1439 个字段**

| 数据集 | 字段数 |
|---|---|
| `pattern_scores` | **487**（形态相似度，cov 0.9996）|
| `model264` | **354**（未来趋势概率）|
| `predictive_starmine` | 222 |
| `analyst7` | 200 |
| `dl_riskfree_returns` / `pv29` / `analyst_earnings_ibes` | 42 / 40 / 37 |

**机制族分布**：价量形态 670、相似度 487、模型综合分 484、**预期修正 175**、增长/价值 164、**资金流/持仓 22**。

## 三、第二步：查论坛拿配方（用户要求）

### ★ 主来源：《理解模板与数据集：我将搜索空间缩小10万倍！》（**130 赞 / 27 评论**）

**帖主配方（`model264`）**：
1. `model264` = **"对未来趋势的预测"**字段族（全平台 2036 字段，**DEU 380**），值域 **0~1**
2. 模板 = **多个同类型字段 `add` 累加** → 更强更稳定的信号
3. **⚠ 用 `add` 不用 `multiply`**：0~1 值域三数相乘差距可达千倍 ⇒ 权重集中
4. **★ 必须先按「预测类型」分类（上涨 / 下跌 / 中性），同类型相加才有意义**
5. 流程：裸字段全量回测 → 剔除 `Sharpe<0.5` → 描述关键词分 4 类 → AI 按经济学维度细分 13 类 → 组内相关性>0.7 只留 3 个代表 → C(39,3)=9139 表达式
6. 产出：**1 万次回测 → 500+ 可交 PPA + 2 个 RA**

### 其他论坛收获
- 《GBR/DEU 新地区不出货？》（87 赞）：DEU 数据集热度含 **`pattern_scores(49)`**、`institutions6(63)`、`model216(53)` ⇒ **`pattern_scores` 在 DEU 是有效的**（与我们 W258/W259 失败矛盾 ⇒ 我们用错结构/方向）
- 《CHN 踩坑实录》：扫 `alphaCount=0` + MATRIX + 高覆盖的 virgin ATOM **结果分化很大** ⇒ 印证 W258
- 《数据集子分类与中性化匹配》：Analyst-Estimates 类**推荐 SECTOR / FAST**

## 四、第三步：发现的「方向陷阱」并修复（本轮最大技术收获）

**DEU `model264` 380 个字段的描述统一为 "Probability that the future trend of X **will be fall**"（下行概率）。**

| 方向分布 | fall | rise | 未标注 |
|---|---|---|---|
| 字段数 | **92** | **0** | 288 |

⇒ **W260 裸字段 8/8 全负（−0.36~−0.60）完全可解释**：字段是**下行概率**，裸用取正 rank = **做反向**。

**⇒ 正确用法 = 先翻转**（`reverse(x)` = −x，或 `subtract(1,x)`）**再 rank**。
**W261 验证有效**：同一批字段翻转后 S 从 −0.4 全部转正到 0.22~0.64。

⭐ **可复用判据**：**「整齐的全负 Sharpe」是方向标错的指纹**（8/8 整齐 −0.4），
不要误判为"无信号"—— 这是**可修复**的，而非判死依据。

## 五、瓶颈（唯一）：多维预测族与「禁 add」合规框架的结构性冲突

**帖主配方依赖 3 字段 `add` 累加** —— 实测验证该逻辑：model264 单字段翻转后**最高仅 S 0.64**，确实需要累加。

**但我方合规闸「禁 `add` 混信号」**（同一 `add` 内 ≥2 个不同信号字段即判混信号）。

**已尝试的 4 类合规替代通道（W262）全部失败**：
| 通道 | 表达式 | 结果 |
|---|---|---|
| 两字段差 | `subtract(rank(A),rank(B))` | −0.45 / +0.42 |
| 分组轴嵌套 | `group_rank(A, bucket(rank(B)))` | −0.39 / +0.15 |
| 时序相关 | `ts_corr(A,B,66)` | −0.67 / −0.54 |
| 比值 | `divide(A, add(B,ε))` | −0.50 / −0.27 |

**⇒ 需用户决策（三选一）**：
- **A**：对「多维预测型数据集」（`model264` / `pattern_scores` 等）**放宽合规判定**，允许**同数据集 + 同方向**字段的 `add`
- **B**：**放弃该池**，回到已验证有效的方向（`analyst_factor_signals` 族 S1.82 候选卡 2Y；`institutions1` 已用）
- **C**：继续找**单字段本身就强**的（需全量裸测 1439 字段，成本高、概率低）

## 六、算子纪律执行情况（用户重申项）

按 `tools/gates/operator_coverage_audit.py` 审计**本轮批次**：
**覆盖率仅 25%（21/84），63 个算子本轮未用**。

**本轮未用的高价值算子**（下批应补）：
- **Time Series 23 个**：`days_from_last_change`、`ts_delta`、`ts_delay`、`ts_arg_max/min`、`ts_av_diff`、`ts_ir`、
  `ts_scale`、`ts_sum`、`ts_covariance`、`ts_regression`、`ts_returns`、`ts_kurtosis`、`ts_max_diff`、`ts_product`、
  `kth_element`、`last_diff_value`、`ts_count_nans`、`ts_quantile`、`hump`、`ts_target_tvr_decay/hump`、`ts_step`
- **Arithmetic 11 个**：`log`、`signed_power`、`power`、`sqrt`、`abs`、`inverse`、`min`、`max`、`pasteurize`、`sign`、`densify`
- **Logical 11 个**：`and`、`or`、`not`、`if_else`、`is_nan`、`equal`、`greater`、`less`、`greater_equal`、`less_equal`、`not_equal`
- **Group 8 个**：`group_backfill`、`group_cartesian_product`、`group_neutralize`、`group_scale`、`group_std_dev`、`group_sum`、`group_mean`、`group_count`
- **Vector 8 个**：`vec_avg` / `vec_count` / `vec_max` / `vec_min` / `vec_range` / `vec_stddev` / `vec_sum` / `vector_neut`
- **Cross Sectional**：`scale`；**Transformational**：`trade_when`

**⇒ 待办：下一批必须先跑 `--checklist` 逐类过一遍，再设计表达式。**

## 七、工具与环境备注

- `tools/operator_coverage_audit.py` 已被并发会话移动至 **`tools/gates/operator_coverage_audit.py`**
  （且**未入 git** ⇒ 若再次被整理可能丢失。符合记忆铁律「`tools/` 会被并发会话重组成子目录 ⇒ 引用前先 `git ls-files`」）


---

## 八、续篇：2Y 墙的 11 类杠杆全败 + 两条纪律补强（W263–W265）

### 8.1 补做算子纪律（用户重申项）

按 `tools/gates/operator_coverage_audit.py` 审计发现**本轮批次覆盖率仅 25%（21/84）**，
于是**用 8 个本战役从未用过的算子去攻那颗 S1.82 候选的 2Y 墙**（W263）：

| 算子 | S | 2Y |
|---|---|---|
| `pasteurize(E)` | **1.81** | **1.12** ← **no-op**（逐位相同）|
| `group_neutralize(E,sector)` | **1.81** | **1.12** ← **no-op**（SUBINDUSTRY 已含组内去均值）|
| `ts_ir(E,252)` | 1.17 | 0.59 |
| `ts_scale(E,252)` | 0.87 | 0.37 |
| `ts_delta(E,66)` | 0.95 | 0.73 |
| `subtract(E, ts_mean(E,252))` | 0.97 | 0.25 |
| `signed_power(E,0.5)` | 0.78 | 0.92 |
| `group_cartesian_product(sector, bucket(rank(E)))` | 0.99 | 0.65 |

### 8.2 论坛 2Y 配方验证（W264/W265）

**W264 全灭**：7 条 CANCELLED + 1 条 ERROR **`Operator rank does not support event inputs`**
⇒ 根因：批次混入 **`market_cap`（VECTOR 类型）** ⇒ **整批连坐**。

**W265（去掉 market_cap）**：论坛 13 赞帖的 `ts_rank(x, 120)` 配方 8 变体 ⇒
**S 0.74~1.05、2Y ≤0.53** ⇒ **配方在我方字段上失效**。

### 8.3 2Y 墙 11 类杠杆总表（终局）

| # | 杠杆 | 结果 |
|---|---|---|
| 1 | `tail` 边界（5 档） | 2Y 全降（0.43~1.06）|
| 2 | 中性化档（8 档） | STATISTICAL 2Y −0.10 |
| 3 | settings decay（6 档） | **decay 2 与 4 的 2Y 完全相同 ⇒ 零敏感** |
| 4 | truncation（3 档） | 零敏感 |
| 5 | 时序平滑（ts_mean 22/66/220/504） | 2Y 1.01~1.17 |
| 6 | 时序分位 `ts_rank`(252/504) | S 崩到 1.04 |
| 7 | `ts_backfill`(252) | **no-op** |
| 8 | 风险调整 / 换轴 / quantile | 全更差 |
| 9 | 未用算子 8 种 | 全降（2 个 no-op）|
| 10 | 论坛 `ts_rank(x,120)` 直接式 | S 0.74~0.82、2Y 0.07~0.09 |
| 11 | 论坛 `ts_rank` × 换轴 | S ≤1.05、2Y ≤0.53 |

**⇒ 结论：`eps_y1_estimate_change_3mo` + `group_rank(·,sector)` 的 2Y = 1.12 是硬上限。建议放弃此腿。**

### 8.4 ★★ 两条纪律补强（本日重复踩坑后固化）

**补强 1 · 论坛配方必须逐算子核验存在性**
70 赞帖《使用 `rank_by_side` 改善 2year_sharpe/ladder_sharpe》推荐的 `rank_by_side`
**不在平台 103 个算子目录中（已下线）** ⇒ 历史帖子引用的算子**不能假定仍可用**。

**补强 2 · 批次严禁混入「未验证类型/可跑性」的字段（本日第 2 次踩）**
| 次 | 字段 | 后果 |
|---|---|---|
| 1 | `directional_significant_value_1`（insider_agg_matrix） | 整批 FAIL |
| 2 | `market_cap`（**VECTOR 类型**） | `rank()` 报 `does not support event inputs` ⇒ **整批 CANCELLED** |

⇒ **发批前必须对批次内每个字段做「类型 + 单条可跑性」双重校验**（DEU 的 `market_cap` 是 VECTOR 而非 MATRIX）。

### 8.5 本轮（W258–W265）总账

**8 批 64 条 sim，0 颗新 alpha**；但拿下：
- **3 个硬结论**：①未测 MATRIX 池与「禁 add」合规框架结构性冲突 ②2Y 墙 11 类杠杆不可破 ③`model264` = 下行概率字段族（需翻转）
- **6 条可复用技巧**（见 §四 + Q49/Q51）
- **4 条纪律补强**：论坛配方验算子存在性 / 批次验字段类型与可跑性 / 「整齐全负 = 方向标错」/ 已归一化字段不再 rank


---

## 九、`multiply` 组合通道（用户提问驱动，W266–W267）

### 9.1 起因
用户问：「有没试过其它组合方式，`multiply` 或者论坛查一下经验」—— **`multiply` 此前确实没试过**。

### 9.2 论坛经验（3 篇直接相关）

| 帖 | 要点 |
|---|---|
| **《多源信号组合的经济学尝试和感悟》** | 「**最朴素的组合——直接相乘或相加——往往适得其反**：一个信号强、一个弱（甚至无独立预测力），**相乘只会用废信号污染好信号**。**组合方式必须由经济学原理决定，而不是从数据里试出来**」+「每个信号都有**身份**与**极性**」 |
| **《【Alpha Idea】双字段 Sentiment》（94 赞）** | 双字段组合 4 种**语义化**用法：当前值−均值 / **`ts_covariance`（判协动）** / 同类字段相减 / 极端时相加 |
| 《MCP 综合优化工作流》 | 算子表明确列 **`multiply(a,b)` = 信号组合** |

### 9.3 ★★ 合规闸实测 —— `multiply` 一直可用而我从未试过

| 组合 | `is_multileg` |
|---|---|
| `add(A,B)` | **True（禁）** |
| **`multiply(A,B)` / `multiply(rank,rank)`** | **False（合规）** |
| `min` / `max` / `divide` / `subtract(rank,rank)` / `ts_covariance` | False（合规）|

⇒ **我方闸只拦 `add`**。`multiply` 是**全新的合规通道**。

### 9.4 W266 实测（已验证字段 A/B 组合）

| 变体 | S | fit | TO | 2Y |
|---|---|---|---|---|
| **`min(rank(A),rank(B))`** | **1.71** | 1.49 | 0.075 | 1.12 |
| **`multiply(rank(A),rank(B))`** | **1.68** | 1.44 | 0.074 | 0.92 |
| `max(rank(A),rank(B))` | 1.69 | 1.45 | 0.078 | 0.88 |
| `multiply(rank,rank,rank)` | 1.60 | 1.37 | 0.073 | 0.88 |
| **`multiply(A,B)` 原始值** | **0.61** | 0.31 | 0.100 | 0.48 |
| `ts_covariance(A,B,66/252)` | 0.46 / 0.27 | — | — | 0.28 / 0.20 |

★ **帖主的「千倍差距」警告被实测验证**：`multiply` **原始值**相乘 ⇒ S 崩到 **0.61**；**必须先 `rank` 再乘**。
⚠ 但 **2Y 仍 0.88~1.12，未突破** ⇒ 组合方式不是 2Y 的钥匙。

### 9.5 W267 实测（把 `multiply` 用到 model264 池）

| 变体 | S | 2Y |
|---|---|---|
| `reverse(multiply(group_rank(A),group_rank(B)))` | **0.77** | 0.58 |
| `reverse(multiply(A,B,C))` | 0.75 | 0.71 |
| `reverse(multiply(min(A,B),min(C,D)))` | 0.69 | 0.56 |
| 其余 5 条 | 0.47~0.66 | — |

⇒ 对比 W261 的**单字段** 0.22~0.64 ⇒ **组合有提升（+0.10~0.15）但远未达 1.58**。

### 9.6 ★★★ 自我诊断：与 130 赞帖帖主的方法差距

| 环节 | 帖主 | 我 | 差距 |
|---|---|---|---|
| ① 裸字段筛选 | 全量裸测，剔除 `Sharpe<0.5` ⇒ **707/2036（35%）** | 只抽测 16 个 | **样本严重不足** |
| ② 分类 | 描述关键词 4 类 → **AI 按经济学维度细分 13 类** | 按"指标名"粗分（首轮还漏了"方向"维度）| **缺经济学维度细分** |
| ③ 剪枝 | **同分类内相关性>0.7 ⇒ 每类留 3 个代表** | 无 | **缺剪枝** |
| ④ 组合 | C(39,3)=**9139** 表达式 | 4 字段随机组合 | **空间未展开** |
| ⑤ 产出 | 1 万次回测 → **500+ 可交 PPA + 2 个 RA** | 16 条 | — |

**⇒ 结论修正：不能说 model264 池"打不出"，应说「在我的粗放方法下打不出」。**
**真正缺的是「按经济学维度精细分类 + 相关性剪枝」这一步。**

### 9.7 「组合方式」完整结论表（回答用户提问）

| 组合方式 | 合规 | model264 上实测 S | 判断 |
|---|---|---|---|
| `add(A,B)` | ❌ 禁 | — | 不可用 |
| **`multiply`（先 rank）** | ✅ | 0.57~0.77 | **新通道，可用** |
| **`min` / `max`（先 rank）** | ✅ | **0.65~0.77** | **最优** |
| `ts_covariance(A,B,d)` | ✅ | 0.27~0.46 | 弱 |
| `subtract(rank,rank)` | ✅ | −0.45~+0.42 | 弱 |
| `group_rank(·, bucket(rank(·)))` | ✅ | −0.39~+0.15 | 弱 |
| `divide(A,B)` | ✅ | 单位受限（CSPrice/CSShare 不能加无单位 ε）| 受限 |

### 9.8 下一步
按帖主方法补两步：① **全量裸测 model264 高覆盖字段**（380 个，筛 `Sharpe>0.5`）
② **按经济学维度精细分类**（描述里引号中的指标 → 归并为类别）+ 组内相关性剪枝 ⇒ 每类 3 代表 ⇒ 再组合。


---

## 十、「都尝试一下」—— 帖主方法三步全走完（W268–W269）

### 10.1 Step 2 · 精细分类（此前跳过的关键步）

380 个 `model264` 高覆盖字段按**经济学维度分 10 类**：

| 类别 | 字段数 | 类别 | 字段数 |
|---|---|---|---|
| 其它 | 149 | 均线/趋势 | 23 |
| **估值/盈利** | **62** | 动量/收益 | 20 |
| 成交量/资金 | 41 | 波动/通道 | 11 |
| 财务结构 | 32 | 技术指标 | 10 |
| 情绪/预期 | 26 | 宏观/汇率 | 6 |

★ **方向修正**：并非全为 "fall" —— 存在 `rise` 类字段（如 `mdl264_eps_sur_decay_l3`）
⇒ **方向必须逐字段读 description**（修正了此前"全为下行概率"的说法）。

### 10.2 Step 1 · 8 类代表裸测（W268）

| 类 | 字段 | 方向处理 | S | 2Y |
|---|---|---|---|---|
| 动量/收益 | `mdl264_3l_d0252ntr` | 直接用 | **0.73** | 0.77 |
| 财务结构 | `mdl264_3l_m1r_mtn_spd_se` | 直接用 | 0.59 | 0.57 |
| 波动/通道 | `mdl264_vol_vo_p_1m_l2` | 直接用 | 0.58 | 0.73 |
| 技术指标 | `mdl264_2l_rw` | 直接用 | 0.50 | 0.70 |
| 宏观/汇率 | `mdl264_1l_acf` | `reverse` | 0.27 | 0.13 |
| 均线/趋势 | `mdl264_1l_57_03_am` | `reverse` | 0.22 | −0.42 |
| 情绪/预期 | `mdl264_es_vol_r1m_l3` | 直接用 | −0.02 | −0.32 |
| 估值/盈利 | `mdl264_3l_m1r_mtn_spe_se` | 直接用 | −0.12 | 0.20 |

⇒ **S −0.12~0.73**（4 个 <0.5）⇒ **弱信号**，与帖主分布（筛 `Sharpe<0.5` 后剩 707/2036 = 35%）一致。

### 10.3 Step 3 · 同类内组合（W269）

类内各取 3 代表做 `multiply(rank,rank)` / `min(a,b,c)`，+ 1 条跨类对照 ⇒ **S −0.11~0.72（未提升）**。

### 10.4 ★★★★ 决定性判断：model264 池「够 PPA，不够 RA」

**帖主自述产出**：「1 万次回测 → **500+ 能交的 PPA** + **2 个 RA**」
⇒ **RA 命中率 = 2 / 10000 = 0.02%**

| 通道 | Sharpe 门槛 | 其它 |
|---|---|---|
| **PPA** | **≥ 1.0** | 算子 ≤8、字段 ≤3、PPAC<0.5 |
| **RA（我方目标）** | **≥ 1.58** | + 2Y/ladder/sub/Fitness 等 9 项硬闸 |

**我方实测（组合后最佳 0.72~0.77）与帖主分布完全吻合** ⇒
**model264 池的裸字段与组合信号普遍落在 S 0.5~1.0** ⇒ **够 PPA，不够 RA**。

**⇒ 对「10 颗 regular alpha」目标的直接含义**：
`model264` 池在 DEU 内**不适合作为 RA 猎场**（理论性价比 0.02%，需 1 万次回测换 2 颗）。

### 10.5 组合方式的最终完整账（7 类全试）

| 组合方式 | 合规 | model264 上限 | 判断 |
|---|---|---|---|
| `add(A,B)` | ❌ 禁 | — | 不可用 |
| **`multiply(rank,rank)`** | ✅ | 0.64 | **可用（新通道）** |
| **`min` / `max(rank,rank)`** | ✅ | **0.72~0.77** | **组合族最优** |
| `ts_covariance(A,B,d)` | ✅ | 0.46 | 弱 |
| `subtract(rank,rank)` | ✅ | 0.42 | 弱 |
| `group_rank(·, bucket(rank(·)))` | ✅ | 0.15 | 弱 |
| `divide(A,B)` | ✅ | 单位受限 | 受限 |

⇒ **组合方式已系统覆盖；但组合无法把弱字段（S<1.0）救成 RA 级（S≥1.58）。**

### 10.6 建议转向（DEU 内）

1. **`pattern_scores`(487 字段)** —— 论坛 87 赞帖显示它在 DEU 是**热门且有效**（49 颗提交），
   而我 W258/W259 只测了 2 个字段（且用错结构/方向）
2. `predictive_starmine`(222) / `analyst7`(200) / `pv29`(40) / `analyst_earnings_ibes`(37)
3. `analyst_factor_signals` 的 S1.82 候选（卡 2Y，12 类杠杆全败）—— 需用户决定是否放弃


---

## 十一、`pattern_scores` 首探（W270–W271）—— 两条新教训

### 11.1 W270 全灭 → 定位到**本地库字段名不可信**

W270（8 条）全 CANCELLED/ERROR：`Attempted to use unknown variable "continuation_upward_wedge_median_similarity_40d"`

| 来源 | `pattern_scores` 字段数 |
|---|---|
| 本地库 `fields` 表（时点快照） | **504** |
| **平台 `get_datafields`（实时）** | **300** |

⇒ 本地库含**旧名/异名**（平台**没有** `continuation_upward_wedge_median_similarity_40d`，只有 `continuation_downward_wedge_median_similarity_40d`）。

**★ 教训（已入 `MEMORY.md` 铁律）**：**发批前必须用 `get_datafields` 拉平台实时字段名逐个核对**
（不能只核对数据集存在性）—— 这是「本地 catalog 是时点快照 ⇒ 存在性只信平台」的具体执行。

### 11.2 ★★ 教训：`pattern_scores` 的 `alphaCount` 是**正向**信号

| 字段 | alphaCount | userCount |
|---|---|---|
| `min_similarity_continuation_falling_wedge` | **27** | 19 |
| `max_similarity_reversal_v_bottom_pattern` | 11 | 4 |
| `max_similarity_v_reversal_top` | 11 | 8 |
| `breakaway_gap_down_mean_simscore_lookback60` | 9 | 3 |

⇒ 与 `model264`（高 alphaCount = 信息已被开采）不同，**这里高 alphaCount 证明字段确实能出 alpha**。

### 11.3 W271 实测（10 条，全部平台真实字段名，10/10 无 error）

| 变体 | 字段（alphaCount）| S | 2Y |
|---|---|---|---|
| Z3 | `max_similarity_v_reversal_top` (11) | **0.59** | 0.29 |
| Z1 | `min_similarity_continuation_falling_wedge` (**27**) | 0.46 | 0.32 |
| Z7 | `dynamic_similarity_reversal_v_top` (2) | 0.13 | −0.54 |
| Z4 | `breakaway_gap_down_mean_simscore_lookback60` (9) | 0.09 | −0.06 |
| Z8 | `continuation_downward_wedge_max_similarity_40d` (0) | −0.48 | −0.69 |
| Z9 | `reverse(max_similarity_rising_wedge)`（帖子1方向洞察）| −0.37 | 0.10 |
| Z10 | `subtract(max,min)_continuation_falling_wedge`（帖子2配方）| **−0.78** | −0.88 |

**⇒ 高 alphaCount 字段（27/11/9）裸用 S 也只 0.46~0.59 ⇒ 别人用的是更复杂的结构，不是裸用。**
**帖子两个配方（方向反转 / max−min spread）在 DEU 上均未奏效。**

### 11.4 结论

**`pattern_scores` 与 `model264` 同型**：**字段本身是弱信号（S<0.7），必须靠结构/组合加工**；
裸用 + 单层 `winsorize` 远远不够。

### 11.5 下一步（待决）

`pattern_scores` 有 **300 个平台字段**、**42 种形态**、**6 种统计量**（max/mean/median/min/std/q95/dynamic）、
**3 种窗口**（默认 / 60d / 120d / 40d）。要真正打开它需要：
1. **用平台 `get_datafields` 拉全 300 字段 + alphaCount**（已有）
2. 按 **alphaCount 高**的字段（证明有效）取 **同一形态的多个统计量面板**（如 max/mean/min/std）
3. 做 **面板间价差**（如 `subtract(max_similarity, min_similarity)` —— 本题中 Z10 失败，但可换形态/窗口）
4. 或做 **形态间对比**（如 "上升楔形相似度 − 下降楔形相似度"）


---

## 十二、战略终局（2026-10-09 ~ 10-10）

### 12.1 `pattern_scores` 判死 —— 外部文献提供决定性依据

**★ Lo, Mamaysky & Wang (2000, Journal of Finance)《Foundations of Technical Analysis》**（形态类信号最权威研究）：
- 用 **kernel regression** 自动识别 10 种经典形态（NYSE/AMEX + NASDAQ，1962–1996）
- **发现**：部分形态**携带增量信息**；**形态出现频率不符随机游走**；对 Nasdaq 股票尤其明显
- **⚠ 关键限定**：效应量小 · **声明期越后越弱** · **扣交易成本后基本消失** · **流动性较差的证券上效应更强**

**★ Marshall, Young & Rose (2006, JBF)**：K线形态在 DJIA 成分股上**与随机假数据无法区分**。
**★ 18 篇 K线形态文献汇总：7 支持 / 11 反对。**

**★★★ 文献共性：形态可靠性 ∝ 1 / 市场效率。**
**⇒ DEU 只有 TOP500（德国大盘 = 高效市场）⇒ 结构上必然不利** —— 与实测完全吻合：

| 批次 | 结构 | 最高 S |
|---|---|---|
| W271 | 平台真名 + `alphaCount` 最高（27/11/9）字段，裸用 | 0.59 |
| W272 | **文献洞察**：频率累积 `ts_sum/ts_mean(66)` · 相对化 `ts_rank(252)` · 形态间对比 `subtract` · 面板价差 · 方向反转 | **0.69** |

### 12.2 2Y 墙第 13 类杠杆（settings 组合）也失败

| 设置 | S | 2Y | sub |
|---|---|---|---|
| SUBINDUSTRY / d4 / t0.08（基线）| **1.82** | **1.12** | **1.06** |
| **FAST / d4 / t0.08**（论坛建议档）| 1.78 | **0.81** ↓ | **0.68** ❌FAIL |

⇒ **2Y 墙累计 13 类杠杆全败** ⇒ S1.82 候选**结论性放弃**。

### 12.3 DEU 可挖空间完整盘点

| 方向 | 状态 |
|---|---|
| 分析师修正族 | **6 颗已提交 ⇒ 饱和** |
| `institutions1` + 伙伴图谱簇 | **1 颗已提交 ⇒ 自锁** |
| `insider_agg_matrix`(304) | **判死**（DEU S0.69 / EUR S0.57）|
| `model264`(354) | **判死**（RA 命中率 0.02%；组合 S≤0.77）|
| `pattern_scores`(487) | **判死**（S≤0.69 + 文献证大盘无效）|
| S1.82 候选（`eps_y1_estimate_change_3mo`）| **13 类杠杆全败 ⇒ 放弃** |
| **DEU VECTOR 未测池（4939）** | **尚未开采 ← 唯一剩下的大池** |
| `predictive_starmine`(222) / `pv29`(40) / `analyst_earnings_ibes`(37) | 未系统开采 |

### 12.4 本日总账

- **提交成功 1 颗**（`2rmGAPqN`：S1.81 / prod 0.6292 / self 0.0327 / ACTIVE）
- **回测 23 批 ~180 条 sim，新 alpha 0 颗**
- **判死 4 个池/数据集**（合计 1145 字段）
- **新增 6 条铁律**：字段名取平台实时值 · 发批验字段类型与可跑性 · 论坛配方验算子存在性 · 整齐全负=方向标错 · 已归一化字段不再 rank · `multiply/min/max` 是合规组合通道
- **沉淀 12 条方法论**（杠杆 13 类 + 组合 7 类 + 结构须匹配字段原生形态 + PPA/RA 天花板判据 + 文献「形态可靠性 ∝ 1/市场效率」）
