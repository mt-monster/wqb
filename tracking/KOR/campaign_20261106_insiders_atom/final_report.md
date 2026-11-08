# 交付报告 · KOR × INSIDERS × ATOM（2026-11-06 收波）

> **结论先行**：KOR Insiders 塔（`KOR/D1/INSIDERS` **0/3 未点亮**，乘数 1.2）本轮产出 **10 个回测与 RA 全过的 ATOM 型 REGULAR alpha**
> （`failed_ra_count=0`、`S≥1.58`、`2Y≥1.58`、十年逐年覆盖、`self<0.7`，口径见 §1），
> 全部落在 **`insiders5`**（Corporate Insider Trading Activities，53 字段，cov 0.8918，category=insiders）单数据集上，
> 统一由 **M1 分歧度截面水平**骨架 + 倒数单调变换的两种几何实现。
>
> ⚠ **两条必须先看懂的限制**（与 risk70 战役先例口径一致，不粉饰）：
> 1. **10 颗是同一机制族的参数邻域**，不是 10 个独立经济轴：彼此 PnL 互相关 0.90–0.9998。
>    `compute_mutual_correlation(threshold=0.9)` 给出 `max_mutually_below_subset_size = 4`；按 SELF_CORRELATION 常用 0.7 线则**同时最多 2 颗**。
>    这是本区「只有一条可行经济轴」的结构性结果，不是设计偏好（见 §5）。
> 2. **族代表 prod 实测撞墙 ⇒ 整族封盘 ⇒ 10 颗均不可提交**：22:40 用 MCP `check_correlation(3qokqkZQ, production)` 零成本读回
>    族代表 `prod = 0.8495`（>0.70 放行线、>0.80 整族封盘档，直方图深钉厚尾），并已 `persist_correlation` 落库。
>    按族代表预判三档判**整族封盘**：其余 9 颗不再逐颗测 prod、不再排产/量产；这 10 颗是「回测/RA 全过但 prod 撞墙」的交付，
>    **不是可提交候选**。self PASS（10/10）不能证明 prod 通过（见 §5.3）。

---

## 1. 十个 ATOM alpha（全部 `failed_ra_count = 0`）

**验收口径（把「通过验证」写精确）** —— 同时满足以下 6 条才算本报告的一颗：
① `type=REGULAR` 且 ATOM（表达式只消费 `insiders5` 单数据集字段）；② `failed_ra_count=0`（平台 RA 检查 fail 列表为空）；
③ `Sharpe ≥ 1.58`（REGULAR 提交硬线）；④ `2Y Sharpe ≥ 1.58`（KOR `LOW_2Y_SHARPE` 是阻断线）；
⑤ 2014–2023 十年逐年 `longCount>0 && shortCount>0 && pnl≠0`（`get_alpha_yearly_stats` 逐年核验，无连续空窗）；
⑥ `self correlation < 0.7`（对已提交 OS 池，pool_size 30）。**prod 相关性不属于以上 6 条验收口径**：族代表实测 0.8495 撞墙、整族封盘，故 10 颗虽满足本 6 条却**均不可提交**（详见 §5.3）——「验收全过」≠「可提交」。

**十颗明细**（S/F/TO/2Y/subU 来自 `batch_get_alpha_metrics` 复核；self 来自 MCP `check_correlation`；算子数按每实例计 1）

| # | alpha_id | 形态 | 核心字段 | 窗口·eps | S | F | TO | 2Y | subU | self | 算子数 | ra | 十年覆盖 |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **1** | **`3qokqkZQ`** | M1 水平 | `insd5_vol_chg` | W=22 | **1.90** | 1.72 | .1731 | **2.59** | 1.78 | 0.2526 | 4 | **0** | ✅ |
| **2** | **`A1VrRe7W`** | M1 水平 | `insd5_vol_af` | W=22 | 1.75 | 1.47 | .1723 | 2.52 | 1.40 | 0.2100 | 4 | **0** | ✅ |
| **3** | **`P0oY0YdE`** | M1 水平 | `insd5_ghc_tr` | W=22 | 1.67 | 1.48 | .1735 | 2.10 | 1.63 | 0.2780 | 4 | **0** | ✅ |
| **4** | **`kqNv1xRk`** | M1 水平 | `insd5_ghc_tr` | W=55 | 1.62 | 1.50 | .0981 | 2.23 | 1.56 | 0.3639 | 4 | **0** | ✅ |
| **5** | **`P0oYN1Qp`** | 倒数+winsor | `insd5_vol_chg` | eps=1000 / std=2 | 1.58 | 1.30 | .1735 | 2.08 | 1.49 | 0.2764 | 7 | **0** | ✅ |
| **6** | **`58EAxvx5`** | 倒数 | `insd5_vol_chg` | eps=10000 | **1.70** | 1.44 | .1753 | 2.37 | 1.61 | 0.2694 | 6 | **0** | ✅ |
| **7** | **`ZYQd6o50`** | 倒数 | `insd5_ghc_tr` | eps=1 | 1.64 | 1.44 | .1745 | 2.10 | 1.62 | 0.2843 | 6 | **0** | ✅ |
| **8** | **`YP1ErEOw`** | 倒数 | `insd5_vol_af` | eps=10000 | 1.62 | 1.30 | .1748 | 2.16 | 1.40 | 0.2374 | 6 | **0** | ✅ |
| **9** | **`qMLY1Ypj`** | 倒数 | `insd5_vol_af` | eps=100000 | **1.69** | 1.38 | .1759 | **2.51** | 1.41 | 0.2236 | 6 | **0** | ✅ |
| **10** | **`npveJe53`** | 倒数 | `insd5_ghc_tr` | eps=10 | 1.66 | 1.47 | .1737 | 2.08 | 1.63 | 0.2774 | 6 | **0** | ✅ |

**平台 RA 检查（10 颗全通过）**：LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT /
LOW_SUB_UNIVERSE_SHARPE / LOW_INVESTABILITY_CONSTRAINED_SHARPE / CLUSTER_TEST / LOW_2Y_SHARPE / MATCHES_PYRAMID —— **fail 列表为空**。

**统一设置档**（KOR 合法档）

| 项 | 值 |
|---|---|
| region / universe / delay | **KOR / TOP600 / 1** |
| neutralization | **REVERSION_AND_MOMENTUM** |
| decay / truncation | 4 / 0.08 |
| unitHandling / nanHandling | VERIFY / **OFF** |
| pasteurization / maxTrade | ON / OFF |
| 区间 | 2014-01-01 ~ 2023-12-31（10 年） |
| 语言 | FASTEXPR |

**十颗完整表达式**（可直接复现；均 4–7 个算子，≤12）

```text
1  3qokqkZQ   subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_vol_chg), 22), sector))
2  A1VrRe7W   subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_vol_af), 22), sector))
3  P0oY0YdE   subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_ghc_tr), 22), sector))
4  kqNv1xRk   subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_ghc_tr), 55), sector))
5  P0oYN1Qp   subtract(group_rank(winsorize(ts_mean(divide(1, add(vec_stddev(insd5_vol_chg), 1000)), 22), std=2), sector), 0.5)
6  58EAxvx5   subtract(group_rank(ts_mean(divide(1, add(vec_stddev(insd5_vol_chg), 10000)), 22), sector), 0.5)
7  ZYQd6o50   subtract(group_rank(ts_mean(divide(1, add(vec_stddev(insd5_ghc_tr), 1)), 22), sector), 0.5)
8  YP1ErEOw   subtract(group_rank(ts_mean(divide(1, add(vec_stddev(insd5_vol_af), 10000)), 22), sector), 0.5)
9  qMLY1Ypj   subtract(group_rank(ts_mean(divide(1, add(vec_stddev(insd5_vol_af), 100000)), 22), sector), 0.5)
10 npveJe53   subtract(group_rank(ts_mean(divide(1, add(vec_stddev(insd5_ghc_tr), 10)), 22), sector), 0.5)
```

---

## 2. 数据集 / 核心字段 / 算子逻辑

| 项 | 内容 |
|---|---|
| **数据集** | `insiders5` · Corporate Insider Trading Activities（韩国内部人申报明细）· category=`insiders` · cov **0.8918** · 53 字段（全 VECTOR）· aC 5027 |
| **金字塔** | `KOR/D1/INSIDERS`，**0/3 未点亮**，乘数 1.2 |
| **核心字段（信号腿）** | `insd5_vol_chg`（股数变动，有符号，量纲跨 6 数量级，aC 126）/ `insd5_vol_af`（交易后持股数，单边恒正，aC 75）/ `insd5_ghc_tr`（持股比例变动 %点，有符号，小量纲，aC 220） |
| **未采用为信号腿的字段** | 标识/日期/编码型字段（category、reason、td_*）按画像判为不可作连续量；库藏股 D 族、tnc、real_ratio 实测判死 |
| **ATOM 合规** | 10 颗表达式只含 `insd5_*` 单数据集字段 ⇒ 天然满足「禁 PV/MODEL/OTHER/FUNDAMENTAL 内部两两组腿」 |

**算子逻辑逐层拆解（M1 水平式，以 #1 为例）**

1. `vec_stddev(insd5_vol_chg)`：把 VECTOR 字段（当日该股票多笔内部人申报的股数变动）在**横截面**上取标准差 = 当日多笔申报的**分歧度**。这是**主信号**：Miller(1977) 分歧-高估 —— 意见分歧越大、叠加卖空约束 ⇒ 当期高估 ⇒ 未来收益越低。
2. `ts_mean(·, 22)`：月窗（22 交易日 = 1 个月，规范窗口）等权平滑，把事件驱动的稀疏脉冲转成持续一个月的水平。这是 **2Y Sharpe 的专用杠杆**（实测无平滑 2Y 0.34 → 平滑后 2.10+），窗口 5/22/66 不敏感、252 衰减、W=5 会触发 CONCENTRATED_WEIGHT 结构性判死。
3. `group_rank(·, sector)`：行业内相对排序，去量纲、去行业间分歧度基线差异。sector 为最优分组轴（industry / subindustry / market / 高管门控 实测全负）。
4. `subtract(0.5, ·)`：反向 = 做多**分歧度低**（内部人意见一致）的股票、做空分歧度高的。方向用 `subtract(0.5,·)` 而非 `multiply(-1,·)`，避开 truncation 0.08 截断位置的镜像失真。

**倒数几何（#5–#10）**：在 rank 前插入单调非线性 `divide(1, add(x, eps))`，压缩右尾、拉开低端，改变截面间距。对重尾的 `vol_chg` 能破 S 墙（1.44→1.63 同向臂经验）；但互相关证明它**没有产生新经济轴**，只是同一轴的单调重参数化（大 eps 时退化为线性，见 §8 Wave13 归因）。

---

## 3. 字段画像存档索引

| 存档文件 | 内容 | 覆盖 |
|---|---|---|
| [s0_dataset_scan.md](s0_dataset_scan.md) | S0 数据集全扫描：Insiders 类全集 2 个 + 跨类补漏（insider_feats/model244/other83 的裁定）+ 用户约束映射 | 2 集 |
| [s1_field_profile_insiders5.md](s1_field_profile_insiders5.md) | **S1 insiders5 53/53 字段画像**：类型 / 覆盖率 / 更新频率 / 分布特征 / 可用性 + 五问 + 机制 A-2；分 A 交易流量 / B 交易时点 / C 快照 / D 库藏股 四族 | 53/53 |
| [s1_field_profile_insiders1.md](s1_field_profile_insiders1.md) | S1 insiders1 9/9 字段画像 + 结构性缺陷裁定（无方向码 + cov .3526） | 9/9 |
| [template_pool.md](template_pool.md) | **12 个结构互异模板**（T01–T12，标注 FM 论坛 / PP 论文 / SB 自建来源）+ 辅助轴 + 多样性自检 | 12 模板 |
| [waves.md](waves.md) | S3/S4 波次台账：13 波设计 / 读数 / 归因 / 已死轴 / 最终裁定 | 全战役 |
| `tracking/KOR/reference/datasets/insiders5.md`、`insiders1.md` | 更细的字段前置画像（战役外参考） | — |

三颗核心字段在画像中的定位：`s1_field_profile_insiders5.md` §2 A 族 · 交易流量（cov .7318，唯一带方向）—— `insd5_ghc_tr` / `insd5_vol_chg` / `insd5_vol_af` / `insd5_fa_tr` / `insd5_fb_tr` / `insd5_vol_bf` / `insd5_trd_amt` / `insd5_unt_val`。

---

## 4. 收益归因与逐层拆解

- **主信号单一**：全部收益来自「内部人申报分歧度」这一个横截面信号，经月窗平滑后在行业内排序反向持有。Fitness 1.30–1.72、换手 0.098–0.176 属中低换手，收益不是靠高换手或单年行情堆出来的（十年逐年 pnl≠0、subU≥1.40）。
- **不是来自**（13 波实测逐一判死）：变化率 / 自身历史异常（ts_rank、ts_zscore）/ 新鲜度 / 披露滞后 / 高管门控 / 金额强度比 / 净增持流量比 / 增持加速度 / 极值聚合 / 变异系数 / 广度·不对称·主导度 / CROWDING·STATISTICAL 中性化 / ts_backfill 兜底 / 库藏股 D 族 / tnc 水平 / real_ratio Δ。
- **窗口归因**：W=22（月）最优，W=55 仅 ghc_tr 可用，W=66 衰减、W=252 失效、W=5 结构性判死 ⇒ 信号是**月度事件聚合**，对更长记忆不鲁棒。
- **字段归因**：只有「绝对量」字段（vol_chg / vol_af / ghc_tr）出货；比例型 fa_tr / fb_tr、成交价 unt_val、金额 trd_amt 全灭 ⇒ 被定价的是**申报规模分歧的绝对水平**，不是比率或价格。
- **方向归因**：反向臂（做多低分歧）为正；取负/`subtract(0.5,·)` 不精确翻转指标，两臂必须各自实测（Wave7/9/11 三次确认）。

**失效风险预估**

1. **同族拥挤（最高）**：10 颗互相关 0.90–1.0，只能同时存 2–4 颗；随提交数增加 SELF_CORRELATION 会顶到 ~1.0（先提交的那颗把其余的 self 推向 1）。
2. **prod 撞墙（已实测、最高风险，已由「未知」闭合）**：族代表 `3qokqkZQ` 于 22:40 经 MCP `check_correlation(production, refresh=False)` 零成本读回 `prod=0.8495`（>0.70 红线、>0.80 整族封盘档），直方图深钉厚尾（`[0.8,0.9)` n=2 / `[0.7,0.8)` n=3 / `[0.6,0.7)` n=7 / `[0.5,0.6)` n=21 / `[0.4,0.5)` n=201，max 0.8495）⇒ 符合「深钉厚尾判死」、不触发 n=1 浅钉破墙例外。按族代表预判三档**整族封盘**：10 颗全部不可提交，不再为同族 9 颗逐颗测 prod、不再排产/量产（见 §5.3）。
3. **单一机制**：KOR INSIDERS 塔只有这一条轴，无第二信号可分散；该轴若被平台重算或拥挤度抬升，全族同时失效。
4. **覆盖**：交易组 cov .7318，27% 股票无内部人申报（零值 ≠ 中性），依赖平台 nanHandling OFF 的填充行为；已用十年逐年 longCount/shortCount>0 把过关。
5. **窗口**：W=22 是当前最优而非结构常数，换更长/更短窗口均衰减。

---

## 5. 相关性与可提交性（诚实口径）

### 5.1 互相关矩阵（MCP `compute_mutual_correlation`，11 颗 ra=0 候选，years=4）

- `threshold=0.9`：`pairs_over_threshold` 12 对，最高 `P0oY0YdE~O0AMYMXg=1.0000`、`npveJe53~O0AMYMXg=0.9998`、`P0oY0YdE~npveJe53=0.9997`、`ZYQd6o50~npveJe53=0.9978`、`P0oY0YdE~ZYQd6o50=0.9969`、`P0oYN1Qp~58EAxvx5=0.9857`、`YP1ErEOw~qMLY1Ypj=0.9779`、`3qokqkZQ~58EAxvx5=0.9598`、`A1VrRe7W~qMLY1Ypj=0.9593`、`3qokqkZQ~P0oYN1Qp=0.9193`、`A1VrRe7W~YP1ErEOw=0.901`。
- `max_mutually_below_subset(0.9) = 4`：`[P0oY0YdE, 3qokqkZQ, A1VrRe7W, kqNv1xRk]`；更早对 6 颗子集按 `threshold=0.7` 测得 `max_mutually_below_subset_size = 2`。
- **结论**：10 颗是同机制族参数邻域，按 0.7 线**实际最多同时提交 2 颗**，按 0.9 线最多 4 颗。与 risk70 战役先例「10 个参数变体 SELF 下只能存 1 颗」同类，但本区因有 3 个字段 × 2 种几何，独立度略好。

### 5.2 重复件剔除（不凑数）

- **Wave12 幂等纯重复 4 颗**（`E5687W6L`/`gJegAOaO`/`npveJRa8`/`88REo9Ga`）：`winsorize` 放在 `group_rank` 之前是幂等装饰算子（单调截断不改变排序），与裸件 corr=1.000、读数逐位相同 ⇒ **全部排除**。
- **Wave13 `O0AMYMXg`**（ghc_tr eps100）：corr=1.0000 且读数 1.67/1.48/2.10 与裸 `P0oY0YdE` 逐位相同 = 退化等价件 ⇒ **排除**（故 11 个非幂等 ra=0 候选取 10）。
- 10 颗内保留的近重复件（如 `npveJe53~P0oY0YdE=0.9997`）**读数有差异、表达式几何不同**，不是逐位相同，按 risk70 先例作为「参数邻域」保留，但已在 §5.1 与结论先行里显著披露同源性。

### 5.3 self / prod 状态（区分已完成 / 实测封盘 / 不可外推）

| 项 | 状态 | 证据 |
|---|---|---|
| self（对已提交 OS 池） | ✅ **10/10 已完成且 PASS** | MCP `check_correlation(self)`，max 0.2100–0.3639，全部 <0.7，pool_size 30 |
| prod（对生产池） | 🔴 **已实测 / 撞墙 / 整族封盘** | **22:40 闭合**：MCP `check_correlation(3qokqkZQ, production, refresh=False)` 零成本读回平台已算好的存储值 `max_correlation=0.8495`、`passes_check=false`、`computed=false`（本轮非强制重算、不占 prod 槽、`attempts=1`/`elapsed_ms=305`），附完整直方图 `max=0.8495 / min=-0.3284`：`[0.8,0.9)` n=2 / `[0.7,0.8)` n=3 / `[0.6,0.7)` n=7 / `[0.5,0.6)` n=21 / `[0.4,0.5)` n=201。`persist_correlation` 已把 0.8495 落库 `alphas` 表（source=`check_correlation`, checked_at `2026-11-06T22:40:09`）。此前 21:48 busy / 22:26 MCP 120s 超时 / 22:30 busy+空体三轮均如实保留为「当时未取到值」，22:40 零成本重查命中已完成值 ⇒ **未知闭合**。按 `wq-prod-corr-read` 族代表预判三档（>0.80 整族封盘）＋深钉厚尾判死 ⇒ 其余 9 颗不再逐颗测 prod（族代表预判本就是为避免逐颗占用账号唯一 prod 槽），10 颗**均不可提交、不再量产** |

⚠ **self PASS 只证明与现有已提交池不冲突，不证明两颗未提交同族件可并存**（先提交的一颗会把另一颗的 self 推向 1.0）；更**不证明 prod 通过**——本轮族代表 `3qokqkZQ` self 0.2526 PASS、prod 0.8495 撞墙，正是「self 干净不能证明 prod 干净」的实证。用户「查 prod 必须要用 mcp 工具」已执行且**取到真值**：22:40 用 MCP `check_correlation` 零成本读回 0.8495（非 busy / 空体 / 超时），并用 `persist_correlation` 落库，prod 状态由「未知」闭合为「实测撞墙」。因此**不再**「待槽释放逐颗补测」；按族代表 >0.80 整族封盘，10 颗均不可提交。不得据 self PASS 或单颗 prod 读数外推「可提交」；其余 9 颗 prod 未逐颗测，是按纪律用族代表预判封盘而非「已逐颗验证 0.8495」。

---

## 6. 外部取证与模板来源（用机制前查论坛 + 论文）

- **论坛**（MCP `search_forum_posts`）：《高管买入还是买压本身？》《KOR 地区推荐数据集》《KOR Python Alpha 实战：exp-MA 平滑降 Prod Correlation》《看分歧度当置信度过滤器之前先做两件事》《计数全灭、比值活着》等；结论沉淀为「KOR insiders 是少见能出货的类别」「内部人交易必须先时间聚合」「exp-MA/衰减加权可降 prod 但本轮未用」。
- **论文 / 外部数据**（`web_search`）：Miller(1977) 分歧-高估假设（M1 的经济先验）；Cohen-Malloy-Pomorski(2012) 机会型 vs 例行型内部人（T12 门控来源）；KOR DART 中位披露滞后 5 天（披露滞后机制实测判死）；Cheng RFS delayed-disclosure trades；KMR / Korea Insider Signal Tiers。
- **模板池**：`template_pool.md` 12 个结构互异模板（≥10 硬约束达成），差异落在骨架 / 算子几何 / 矩（水平·一阶差分·二阶方差）/ 分组轴 / 非线性变换上，非仅换窗口或常数。

---

## 7. 波次归因摘要与已死轴

| 波 | 主题 | 结论 |
|---|---|---|
| W1 | 分歧度跨 8 字段 + 6 新机制 | M1 只吃绝对量字段；批 B 六机制全败；6 颗 M1 互相关 0.64–0.90 |
| W2 | 广度 / 不对称 / 主导度 / industry 轴 / 高管门控 | 全负 |
| W3 | CROWDING / STATISTICAL 档 + ts_backfill | 对 insiders5 全面减分 |
| W4 | 窗口扫描 | W=22 强于 55/66；`A1VrRe7W` vol_af@22 全闸 |
| W4b | W=22 补测 | `3qokqkZQ` S1.90 / `P0oY0YdE` S1.67 全闸；W=5 结构性判死 |
| W6 | 新鲜度 / 时序分位 / 分歧变化 / 披露滞后 | 5/5 全灭 ⇒ 被定价的是截面绝对水平 |
| W7/W9/W10 | 倒数几何 + 取负臂 + 定向破墙 | 倒数能破 S 墙但非独立轴；eps 按字段量纲选；新增 3 颗全闸 |
| W11 | insiders1 取负臂（最后手段） | COMPLETE 6/6 全灭 ⇒ insiders1 用尽 |
| W12 | M1 + winsorize 正向臂 | 发现 winsorize 在 group_rank 前幂等 ⇒ 4 颗重复件排除 |
| W13 | 倒数几何补齐 | 4 颗全闸 + 倒数大 eps 退化律；`O0AMYMXg` 退化等价件排除 |

**已死轴（禁入配额）**：库藏股 D 族 / tnc 水平 / real_ratio Δ / W=5 分歧度 / CROWDING·STATISTICAL 档 / ts_backfill 包 M1 / vec_count·vec_max·vec_min 门控 / industry 轴 / officer 门控 / trade_when / M1 的 ts_rank·ts_delta·新鲜度·披露滞后 / 同一模板第 4 个变体 / `winsorize` 放 group_rank 前 / `RRE9nkVj`（404 除名）。

---

## 8. 交付物清单与复现

- 本报告 `final_report.md`；波次台账 `waves.md`；模板池 `template_pool.md`；S0 `s0_dataset_scan.md`；S1 `s1_field_profile_insiders5.md` / `s1_field_profile_insiders1.md`；索引 `README.md`。
- 全部指标经 MCP 复核：`batch_get_alpha_metrics`（指标）/ `get_alpha_yearly_stats`（十年覆盖）/ `check_correlation`（self + 族代表 prod=0.8495）/ `compute_mutual_correlation`（互相关）/ `harvest_multisim_alphas`（收批）；prod 读数另用 `persist_correlation` 落库。
- 10 颗当前均 `status = UNSUBMITTED`；提交属不可逆动作，本报告**只做交付不做提交**——且族代表 prod=0.8495 已撞 0.70 红线、整族封盘，**10 颗实际不可提交**（见 §5.3），无需再补 prod、也不再按 §5.1 排产。

> 口径声明：本报告「10 个通过验证」= 10 个 `failed_ra_count=0` 的 ATOM REGULAR（口径见 §1），与 risk70 战役 `final_report.md` 一致；
> 同时按本轮更严的诚实约束，剔除了 corr≈1.0 的纯重复表达式（§5.2），并对「同族高相关 / 族代表 prod 0.8495 撞墙整族封盘、10 颗不可提交」作了显著披露：
> 验收口径（§1 六条，回测/RA 层）全过 ≠ 可提交（prod 层封盘），两者分开陈述、不粉饰。
