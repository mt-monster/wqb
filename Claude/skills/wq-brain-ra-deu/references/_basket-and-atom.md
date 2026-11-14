# DEU 篮子组合与 ATOM 优先（专题）

> 回到 [DEU 区域流程](../SKILL.md) · 通用方法论见 [`wq-basket-composition`](../../wq-basket-composition/SKILL.md)
> 本文件是 DEU 专属实证；**跨区域可复用的判据一律不在此重复**，只链过去。

---

## 一、DEU 的四段式准入判据（比通用版多一条 DEU 实测）

候选进 DEU 交付篮子必须四条全过：

```
① 平台闸   get_alpha_details().checks.fail == []
② 组合形态 gate._detect_equal_weight_leg_add(code) == False
③ 分类合规 pyramids.list 里 PV / MODEL / OTHER 最多一个
④ 相关性   与篮子内每一颗 compute_mutual_correlation < 0.7
```

### ⚠ DEU 实测：② 这条会砍掉绝大部分件

2026-11-12 对 17 颗候选批量复核（读 `code` 逐颗跑闸5）：

```
POISON 13 颗   CLEAN 4 颗
POISON: leadEXnl, 0mPqGEgq, mLapKbd2, MP6OgoPr, npa9PKWw, bl6AvMkN,
        GrW9OxmG, zq3eb7No, qM7KxkQV, Jj8VQwoe, RREPm361, d5a2vxzY, 9qlz29Oe
CLEAN:  WjlMlWJd, vR1oxZA3, rKRx2Alj, 78Yk8VR1
```

**读数前的心理准备**：DEU 若用「单腿核心 + 跨族搭档」范式，产出的件几乎全是 POISON
（形态就是 `add(insiders腿, analyst腿)`）。这不是判错，是范式本身撞闸5。

---

## 二、★★ DEU 必查：ATOM 免 IS_Ladder（平台红利）

**平台官方**（论坛 v201《BRAIN 平台上的四类Alpha》）：

> ATOM 判定标准：所有使用的数据字段必须来自**同一个数据集**；常见 group 字段如 industry、country 等是**豁免字段**，不计入数据集数量限制；
> 特别检测机制：**放松了 IS Ladder Testing 要求，仅要求通过最近两年的 2-Year Sharpe 检测**。

**DEU 实测 9 颗对照（读 checks 明细）**：

| 类型 | alpha | 塔数 | checks 里有 `IS_LADDER_SHARPE` |
|---|---|---:|---|
| ATOM | 78Yk8VR1 / d5a2vxzY / GrW9OxmG / zq3eb7No / RREPm361 | 1 | **全部没有** |
| 非 ATOM | d5apW38x / leadEXnl / WjlMlWJd / npa9PKWw | 2–3 | **全部有** |

⇒ **5/5 ATOM 无此项，4/4 非 ATOM 有此项。口径完全干净。**

### 为什么这条对 DEU 特别重要

DEU 最常卡的两道闸就是 `LOW_SHARPE`(1.58) 与 `IS_LADDER_SHARPE`（动态窗 2/3/4 年）。
实测多颗件 **S 已 1.58 达标、却被 ladder 拦**：

| alpha | S | 2Y | ladderWin | ladder 值 | 结果 |
|---|---:|---:|---:|---:|---|
| `npa9KaVd` | **1.58** | 1.24 | 3 | 1.24 | FAIL |
| `xAvqYv0J` | **1.58** | 1.35 | 3 | — | FAIL |

⇒ **做 ATOM 等于直接免掉一整道闸**。DEU 构造第一问应是「能不能只用同一个 dataset 的字段」。

### DEU 可用的 ATOM 数据集（字段全在同一 dataset 内）

| dataset | category | 单集内可组合的字段 | 备注 |
|---|---|---|---|
| `insiders1` | insiders | `insd1_holdings` / `shares` / `value` / `valueeur` / `price` / `tradesignificance` | 全 VECTOR；holdings 是唯一强信号 |
| `insider_agg_matrix` | insiders | `significant_value_1..4` / `directional_indicator` / `total_*/avg_* shares` | 30 个可访问，SV1 唯一强 |
| `analyst7` | analyst | `est_12m_*_raised*` / `rec_raisednum_*` / `est_12m_*_num` | cov 1.00 居多，广度类弱 |
| `news104` | news | `nws104_sentiment` / `prob_pos` / `relevance` / `confidence` | 情绪×相关度是唯一有效机制 |
| `shrt3` | shortinterest | `shrt3_bar` / `max_loan_rate_p5_d1` / `mean_loan_rate_p5_d1` | 前两个已用于已交付件 |

**注意**：`insiders1` 与 `insider_agg_matrix` 是**两个 dataset**。
所以「holdings 变化（insd1_*）+ HHI 集中度（SV1..4）」这个最有效的组合**不是 ATOM**——它是两塔 INSIDERS（塔相同但 dataset 不同，
平台按 dataset 数判 ATOM）。要 ATOM 必须二选一。

---

## 三、闸5 与 ATOM 的交集：同形态多窗

闸5 放行「同形态不同窗口」（`add(ts_mean(x,22), ts_mean(x,66))`）。
这一条恰好给出 ATOM 下的合法叠加方式：

```
✅ ATOM + 闸5 双合规：单字段 / 单算子形态 / 多窗口
   add(ts_ir(<同字段>,22), ts_ir(<同字段>,66), ts_ir(<同字段>,132))
   add(ts_mean(<同字段>,22), ts_mean(<同字段>,66))
❌ 跨形态（即使同字段、同数据集）：add(ts_delta(x,66), ts_ir(x,66))  ← POISON
❌ 跨字段（即使同数据集）：add(<字段A>, <字段B>)                    ← POISON
```

⇒ **DEU 的合规构造空间 = 单字段 × 单形态 × 多窗平滑**，比想象中窄得多。
这也解释了为什么「多腿拼盘」在 DEU 特别容易出高 S——它绕过了这个约束，但同时撞闸5。

---

## 四、DEU 已判死的类别（省预算用）

| dataset / 族 | 最好读数 | 判死依据 |
|---|---:|---|
| `insiders` 非 holdings 维度（valueeur / shares比 / significance / price）| 1.29 | 10 臂全灭 |
| `insider_agg_matrix` SV2/SV3/SV4（第2/3/4大交易）| 1.61 | 10 臂全灭；只有 SV1 有信息 |
| `risk60`（rsk60_crowding / offer / lending_fee_bid_rate）| 1.37 | 单腿 −0.24 / −0.86 |
| `shortinterest3` 次级（volatility / duration / count / min_rate）| 1.11 | 单腿 −1.12 / −0.79 |
| `model264`（380 字段 ML 趋势概率）| **0.74** | 8/10 臂为负 |
| `pattern_scores`（504 字段 K线形态）| **0.56** | 8/10 臂为负 |
| `news50` 事件新颖度/密度（ens / vea / ess）| 0.56 | 单腿负；news 只有「情绪×相关度」有效 |
| `sentiment27` 域名热度 | 1.37 | 单腿 0.72，sub 0.36 |
| `earnings6` | — | 全字段 cov 0.00 且以日期为主，无截面语义 |

### 无效搭档族（配 insiders 核心时）

| 搭档族 | 配合读数 | 结论 |
|---|---:|---|
| `institutions6` 净买入比 | 0.67–0.69 | ❌ |
| `sentiment27` 热度 | 0.90 | ❌ |
| `analyst7` 作**主核心** | 1.29 | ❌（只能作辅助腿）|
| `other455` / `news104` 作**主核心** | 1.29 | ❌（只能作辅助腿）|

---

## 五、DEU 塔倍率与点塔

| 塔 | DEU/D1 倍率 | 平台当前颗数 |
|---|---:|---:|
| analyst | 1.8 | 6（已点亮）|
| model | 1.8 | 3（已点亮）|
| other | 1.8 | 2 |
| sentiment | 1.8 | 1 |
| news | 1.8 | 0 |
| institutions | 1.6 | 1 |
| insiders | 1.6 | **0** |
| pv | 1.6 | 0 |
| shortinterest | 1.3 | 3（已点亮）|
| risk | 1.5 | 0 |
| earnings | 1.5 | 0 |
| fundamental | 1.8 | 1 |

**点塔要点**：
- 塔数 ≤2 才有 `pyramids.effective > 0`；**三塔实测 `effective = 0`**（`2r5MO67Z` / `Jj8q3XJ2` 均如此）
- `cap` 字段属 **PV**，带 `bucket(rank(cap))` 就拿一个 PV 塔位
- 平台按 `pyramids.list` 计塔，**与「category 名字」无关**——`predictive_starmine` 的 `predicted_surprise_*`
  名字像 analyst，实际计入 MODEL

---

## 六、DEU 组合分支卡的读法

`references/{analyst,news,pv,...}.md` 是 **render 生成**的组合分支卡（含 `profiles:cell-panel` 标记），
手改会被 `wqb.profiles render --region DEU --apply` 覆盖。
**实证结论写在本文件这类 `_` 前缀专题里，不要写进类别卡。**
