# 步 7（S4）细则：诊断改进——预筛 · 评审 · 墙与池 · 辅助腿 · 组合形态

> 主 SOP 见 [`../SKILL.md`](../SKILL.md) 步 7。适用决策表：[`decision-table.md`](decision-table.md) D0 / **D0-P（prod 墙唯一处置表）** / D1 / D2 / D12 / D14。
> 词义（墙 / near / salvage / PARTIAL / READY·REVIEW·REJECT）见 [`GLOSSARY.md`](../../GLOSSARY.md) §1–§2；本文只在用到处给一句判据。
> 本步**只回答一个问题：这一波的候选下一步该去哪**（提交链 / 改进 / 判死）。失败分支在 §7.9（不夹在中间）。

## 7.1 S4 由哪几段组成（顺序即执行顺序）

```
S3 收批 → ① prod-first 探针 → ② s4-prescreen 预筛 → ③ review_wave 评审（workflow_campaign S4） → ④ 逐候选链 → 步 8
```

| 段 | 输入 | 输出 | 去向 |
|---|---|---|---|
| ① **prod-first**（定义见主文步 5b） | 本波 `backtest_results` | 族级 `EXPAND` / `STOP`；写 `alphas.prod_correlation` 与 ledger `prod_first_<wave>` | `STOP` 的族按 D0-P，**不扩变体** |
| ② **s4-prescreen** | 本波 alpha_id 清单 | 每条 `READY` / `REVIEW` / `REJECT` | `REJECT`（全灭）判死，**不进 ③④**；只有 READY / REVIEW 往下走（8 条从 8 次逐条评审压成 1 次预筛 + 仅存活者进链，约 8 倍效率） |
| ③ **review_wave** | 本波 alpha_id（节点自动从 `backtest_results` 解析） | 墙 / near / salvage 池、`expOS` 列、ledger `s4_walls_<region>_<wave>` | 评审通过者进 ④；未通过者按 §7.3 的墙决定去向 |
| ④ **逐候选链** | 评审通过的候选 | 逐条稳健 / 相关性 / 评审结论 | `brain-calculate-alpha-selfcorr-quick`（本地快筛）→ `check_self_correlation` → `compute_mutual_correlation`（候选集内两两）→ `check_correlation`（平台 prod）→ [`brain-alpha-robustness`](../../brain-alpha-robustness/SKILL.md) → [`brain-alpha-judge`](../../brain-alpha-judge/SKILL.md)（参考评审）；按需 `brain-explain-alphas`（Mode B 换概念前查概念重叠，非每候选必经） |

## 7.2 调用

```
# ① prod-first（S3 收批后第一件事；平台单并发，串行；--top-k 缺省 3，每族最强 1 条）
python tools/campaign_intel.py prod-first --region $REGION --wave $W --write-ledger
# ② 预筛
python tools/campaign_intel.py s4-prescreen --ids-file <本波 alpha_id 清单.txt>
# ③ 评审（节点先从 backtest_results 解析本波 alpha_id，再拼 review_wave.py --alphas … --tag <wave> --write-ledger）
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S4"  dataset=$DS  wave=$W
```

- ③ **解析不到本波 alpha_id 即 FAIL（干跑也 FAIL）并列出该区最近波次** → 用其中的**字符串波号**（如 `s2_<ds>_d1`）重试；不要手拼 alpha_id。
- ① 的「首探」口径与处置一律按 D0-P；本文不再复述 prod 阈值。**多候选时的 prod 排队**（串行泳道、48 小时结果缓存、`refresh` 终验）见 [`prod-corr-avoidance.md`](prod-corr-avoidance.md)「排队纪律」。

## 7.3 墙与池：判据 → 后果（RA-86 词汇）

| 名称 | 判据（代码位置） | 后果 |
|---|---|---|
| `RN_EXPOSURE`（墙） | `risk_neutralized_sharpe ≤ rn_sharpe_min`（`review_wave.walls()/passes()`；缺省 0，区域 `thresholds.review.rn_sharpe_min` 可覆盖，EUR 为 1.0） | 不进候选，**也不进 near / salvage 池、不作组合腿**（此前照样被 Mode A/B 取来调参，还会把全灭波记成 PARTIAL） |
| `ROBUST_STRUCTURAL`（墙） | sharpe 过 near 线，但 `robust_universe_sharpe / limit < near.robust_min_ratio`（缺省 0.5，`thresholds.json` 可调） | 不入 near。IND w172 四条 raw 1.76 / robust 0.24 曾按 sharpe 入 near → 全灭波记 PARTIAL → 停止规则 B 永不触发；metrics 行现带 `robust_sharpe / robust_limit / sub_universe_sharpe` |
| **near 池** | 没达标，但接近闸门（YELLOW），且不带上面两种墙 | 可沿 Mode A / B 继续；波结论 `PARTIAL` |
| **salvage 池** | 失败候选中达「辅料线」者（`seal_dead_end` / 收批级联沉降，收集宽） | 只作 Mode B 组合腿辅助来源（§7.6）；动用仍守各区 `mode_b_qualification`（动用严） |

## 7.4 RN_EXPOSURE 的处置表（条件 → 对单条 → 对想法 → 记录）

| 条件 | 对该条 alpha | 对想法 / 族 | 记录 |
|---|---|---|---|
| `risk_neutralized_sharpe ≤ rn_sharpe_min` | 墙：不入候选 / near / salvage / 组合腿 | — | review payload 的 `walls` |
| 同上，**且 raw sharpe ≥ 1.58** | 它**就是**自己声称的那个因子暴露，不是暴露之上的超额 → **停止调参**（调参只会让暴露更纯） | 同想法下其余变体也读 `risk_neutralized_sharpe`：**全部** ≤ 0 → 想法级 `dead_end`；有变体为正 → 只对该条继续 | 步 9：`seal_dead_end`；并与 GEM 声明的 `Expected Exposure` 比对，回写 `template_kb`（兑现进 `validated`，未兑现进 `failed`） |

实证：HKG w4 七条里六条 `risk_neutralized_sharpe` 在 −0.33 ~ −0.57，raw sharpe 却非零；w3 的 `O0roWEM7`（RN 0.96 ≈ raw 1.17）是约 150 次回测中唯一的真信号特征。`risk_neutralized_sharpe` 已入 `backtest_results`。

## 7.5 IS→OS 衰减校准（`src/wqb/research/os_decay.py`）——以及**不能拿它做什么**

`review_wave.py` 评审时读 DB 的 OS 衰减基线（`alphas.os_*`，由 `tools/sync_platform_alphas.py` 同步平台 OS 池），给每行追加 `os_calibration`（预期 OS 水位 + 存活率），评审表多一列 `expOS`。基线不可读或样本不足（< 30）时 fail-open，评审照常。

```
python tools/sync_platform_alphas.py --baseline     # 查看 / 刷新基线（--dry-run 只报告差异）
```

- **用途**：只给「这颗值不值得占配额」的期望值参考：`expOS = IS sharpe × 0.358`（USA 124 例实测衰减比；历史存活率约 78%，OS 过 1.58 仅 11%）。
- **不能用来**：① **不抬高 IS 阈值**——IS 与 OS 的 sharpe **Spearman 秩相关仅 +0.086**，IS 各桶的 OS>0 存活率平坦（70–80%），抬高 IS 线不会提高 OS 存活率；② **不作单候选排序依据**（代码在 `caveat` 字段里已写明）。

## 7.6 卡闸找辅助腿：`get_salvage_pool`

主信号卡某闸、常规想法层改进 2–3 轮仍过不去时，从 salvage 池找**跨数据集正交**的辅助腿，替代人工翻历史波次：

```
mcp__wqb-db__get_salvage_pool  region=$REGION  boost_dim=<见下表>  exclude_dataset=<主信号数据集>  min_sharpe=1.0
```

| 主信号卡在 | `boost_dim` |
|---|---|
| 2Y 闸 | `boost_2y` |
| CW / 子宇宙 | `boost_cw` |
| 换手 | `boost_tvr` |
| 信号弱 | `boost_sharpe` |

返回里 `unknown_provenance` > 0 表示有条目来源数据集未知——**来源未知不能作为跨集正交证据**，传 `exclude_dataset` 时这些条目被排除。
取到辅助腿之后**怎么用**，见 §7.7 的「辅助腿入场三式」——不是把它加进去。

### 7.6.1 卡在提交层四闸时：SUB 比值律 · 零成本定位卡点（2026-09-28 实证，跨区通用）

- **提交层实际四闸** = `LOW_SHARPE` / `LOW_FITNESS` / `LOW_2Y_SHARPE` / `LOW_SUB_UNIVERSE_SHARPE`，**均为严格不等式**；前三闸的线取 `config.PLATFORM_CHECK_LINES`，SUB **没有固定线**——它的 limit = 0.75 × sqrt(子宇宙规模 / 宇宙规模) × 本 alpha 的 sharpe（公式见 `brain-how-to-pass-alpha-test` §5），**系数随宇宙变化**：KOR（TOP600）实测 ≈ 0.571，USA（TOP3000 → TOP1000）≈ 0.433（2026-10-01 两处直查 0.4335 / 0.4333）。KOR 实测：`wpZkk1Mp` SUB limit = 1.03 / sharpe = 1.80 → 0.572；`2rwoAp8b` 1.12 / 1.96 → 0.571；`6XjLAaWO` 0.89 / 1.55 → 0.574（三处独立一致）。**DEU profile 记的是 ≈ 0.47（另一批实测），比例以本区 `get_alpha_details` 里 `LOW_SUB_UNIVERSE_SHARPE` 的 limit / sharpe 为准，不要把 0.571 当常数。**
- **推论**：SUB 是**比值闸**——把 sharpe 压到刚过 `LOW_SHARPE` 线会**同步降低** SUB 要求（按 KOR 系数 0.571，sharpe = 1.62 时只需 SUB ≥ 0.93；USA 系数 0.433 时只需 ≥ 0.70）。所以「sharpe 越高越好」在提交层是错的，目标是 `SUB / sharpe ≥ 该比例` 且 `LOW_2Y_SHARPE`、`LOW_SHARPE`、`LOW_FITNESS` **同时成立**。
- **破比值闸的合规旋钮**（实测有效）：换分组轴到 `market` / `exchange`（效果不同：`market` 给比值、`exchange` 给 2Y）、`signed_power` 压尾（⚠ 须先查持仓对称性：压尾造成多空不对称会触发 `LOW_INVESTABILITY_CONSTRAINED_SHARPE`，实测 `quantile` 替 `signed_power` 后多空完全对称（LC319 / SC319），所以优先换等价的非压尾包装算子，见 `brain-how-to-pass-alpha-test` §5b）、`ts_decay_linear` / 长窗 `ts_rank` 平滑。KOR / other466 实证：`group_rank(R, market)` 把比值从 0.55 抬到 0.59，是过闸的决定性一步。
- **零成本定位卡点**：`submit_verdict` 在处女提交（`GET /submit` 404）时仍返回**模拟层完整 checks**（`模拟层 checks: N 条 (FAIL x / WARNING y)` + `Failed RA / PPA` 计数），足以定位唯一卡点——**不要等真 POST 才知道卡在哪一闸**。
- 该实证的软层全文与佐证见 [`docs/experience/01_platform_gates.md`](docs/experience/01_platform_gates.md)。

## 7.7 组合形态：允许清单（唯一一份）· 辅助腿入场三式 · 为什么闸不是许可证

### 7.7.1 规则（CLAUDE.md「禁止混信号调参，尤其警惕 add(A,B)」的落地）

**禁止任何两条独立信号腿的加和**——加权、**等权**、`add(...)`、中缀 `+`、价差再加第三腿一律属同一违规族；也不得靠增删腿数、扫描混合权重去修不达标的信号。**任何含混表述都不构成本规则的例外。**
判据是**本质**（是不是两条独立信号腿相加），不是**语法**（有没有命中正则）。

### 7.7.2 允许的形态（全库唯一一份清单；其它文档只引用本节）

| # | 形态 | 边界 / 判据 |
|---|---|---|
| ① | 单信号结构 | 如 `ts_scale`；同一形态仅窗口不同的多窗平滑（`ts_mean(x,22)+ts_mean(x,66)`）＝单信号 |
| ② | **同源价差** `subtract(A, B)` | A、B 必须是**同一经济量的对偶两侧**（买 / 卖、已实现 / 隐含、实际 / 预期）且**同数据集**（闸 5 `spread_cross_dataset` 拦跨集；带数值系数触发 `SPREAD_WEIGHTED` 警告）；须在 idea 里声明 Expected Exposure（准则，无代码检查）。`subtract(a,b)` 与 `add(a,-b)` 数学等价——所以「有经济含义」是硬前提，不是措辞 |
| ③ | 换算子几何 | `group_rank` / `group_zscore` / `ts_quantile` / `bucket` |
| ④ | 事件门控 | `trade_when` / `if_else` |
| ⑤ | 换字段组合或换信号概念 | Mode B 想法层 |
| ⑥ | SuperAlpha combo | 在 [`wq-brain-superalpha`](../../wq-brain-superalpha/SKILL.md) 层，不在表达式层 |
| ⑦ | **协动对象** `ts_corr(rank(主), rank(辅), W)` / `ts_covariance(主, 辅, W)` | 取两序列的**关系统计量**作信号，不是水平相加；辅助腿只经关系统计量进入（形态库 F5，2026-09-13 路线 A 已列入；本表此前漏列）。完整的 F1–F6 形态、入场方式的可检判据与卡点映射见 [`optimization-v1 形态库`](../../wq-brain-alpha-optimization-v1/references/structural-interaction-forms.md) |

### 7.7.3 辅助腿入场三式（回答「取到辅助腿之后能怎么用」）

辅助腿（来自 §7.6 或其它数据集的正交信号）**只能**以下面三种身份入场，**不得作加法项**：

| 身份 | 做法 | 适用 / 证据强度 |
|---|---|---|
| (a) **条件** | `trade_when(慢开关, 主腿, …)`：用**慢变量**（月 / 季频）把宇宙切掉约一半，进 >0.5 / 出 <0.4 的滞回带 | **实证最强**：IND 用税前利润预期修正 rank<0.5（analyst）门控，prod 0.54（ZYbqREW1）；机构持股比例 rank>0.5（institutions6）prod 0.55（levk5JYN）。两边为空的门控（成员标志、价带比例）→ 全 0 持仓，先查字段取值分布 |
| (b) **分组 / 分桶** | `group_rank(主腿, 分组字段)` / `bucket(rank(辅助), range="0,1,0.1")` 自定义分组 | 用于稳健性 / 分散化（CW、子宇宙；D6 的 CW 修法顺序把「换算子几何」排在换字段之前）。⚠ **不能破 prod 墙**：`group_rank(主腿, bucket(慢变量))` 保留全部持仓、只重排，IND w198/w199 prod 仍 0.79–0.83 |
| (c) **中性化 / 残差** | `group_neutralize(主腿, 分组)`、`vector_neut(主腿, 辅助)`、`ts_regression` 取残差 | **证据弱**：KOR wave113 `group_neutralize(同信号, sector)` prod 0.7003→0.6993（n=1、差值在测量噪声内），只作 D0-P 踩线带的那 1 次尝试，不是规则 |

**已知无效**：快变量门控（情绪 5 日比值、期权成交量 z、新闻计数）→ 换手 0.46–0.65 且 robust 掉到 0.5–0.9；同主腿同门控换阈值 / 窗口的兄弟 self-corr >0.9，只能提一颗（同主腿不同慢门控之间 0.46，可并存）。区域画像见 [`regions/IND.md`](regions/IND.md)「组腿配方」。

### 7.7.4 门禁通过 ≠ 合规

闸是兜底，不是许可证。KOR wave189/190 有 7 条 `add(group_rank(腿A), group_rank(腿B))`（含 S=2.11 / F=1.80 / 2Y=1.89 的漂亮结果）漏过闸 5——因为当时的判定明文豁免等权——**已全部作废**；此后补了 `equal_weight_leg_add`、中缀加号、跨集价差判定与覆盖矩阵测试。事故全文见 [`incidents.md`](incidents.md) I-1。判合规先问「是不是两条独立信号腿相加」，再看它有没有命中正则。

## 7.8 未编排的批量变体器：护栏

`workflow_execute(node="alpha_booster")`（通用短板提升：2Y / sub_universe / turnover 变体）与 `node="modeb_improve"`（Mode B 四阶段：条件化 / 残差 / 交互 / 时间结构）作为**按需机械变体生成器**保留；`structural_reconstruct` 实测仅 1 行产出，降为实验性、不再主动推荐。
- **分工**：[`wq-brain-alpha-optimization-v1`](../../wq-brain-alpha-optimization-v1/SKILL.md) 是人审驱动的改进入口；这两个节点只在 S4 需要**成批**变体时调用。
- **护栏（防「混信号调参」在批量下放大）**：产出入库后**仍走步 5 全部闸**；同骨架换参沿用每骨架封顶（`WQB_GEM_MAX_PER_SKELETON`，缺省 12）；变体必须落在 §7.7.2 的允许形态内。
- **先想法后参数**：Mode B（换信号概念 / 字段组合）在前，Mode A（冻结想法，在 8 候选严格批里收敛 decay / 窗口 / 中性化 / truncation）在后。「Mode B 70% / Mode A 30%」是**精力（预算）分配的经验比**，不是次数配额；次数上限是每个 alpha 3–5 个周期。

## 7.9 失败分支（症状 → 判据 → 动作 → 回哪步）

| 症状 | 判据 | 动作 | 回 |
|---|---|---|---|
| 首探 prod 偏高 | 按 D0-P 的阈值表 | 查 D0-P：不扩变体 / 当天进步 8 / 踩线带 1 次结构性尝试 / dead_end | 步 8 或步 9 |
| 同一想法 > 10 种结构仍不过 | 计数。**10 是经验上限，没有统计推导**——意图是防「对同一想法无限换壳」；更硬的判据是 §7.4 / D0-P 的机检墙，能用它们判就不要靠计数 | 步 9 记 `dead_end`（先 `forum_recon` 软核对） | 步 9 → 步 2 |
| Mode B 常规改进 2–3 轮仍卡墙（prod / 2Y / CW / tvr / robust）且未到判死 | 每轮都有新结构、指标仍不过 | **找武器**：`tools/forum_recon.py --question "<墙名+数据集> 破墙配方" --context region=$REGION,dataset=$DS,wall=<WALL> --out ledger`（触发表见 [`forum-recon-triggers.md`](forum-recon-triggers.md)），命中配方入 idea 池供 Mode B Step B3；**先读本波默认取证已落的结论**：收批时 `forum_recon_wave` 已自动问过一次（`pipeline.py --forum-recon`，`batch_track` 缺省带上），ledger `forum_recon_wave_<wave>` → `question_key` → `forum_recon_<qkey>` / `_negative_` / `_error_`（故障先修工具，不是无解），见触发表「波级默认取证」 | 本步 |
| 全灭 | ② 预筛全 `REJECT` | 判死该批，不进 ③④ | 步 9 |
| 候选全部被 prod 墙卡死 | `submit_verdict` BLOCKED 原因含 PROD_CORRELATION | 除 `dead_end` 外，在步 9 登记数据集饱和（`mark-saturated`），下一轮 S0 才会降级该集 | 步 9 |

未编排项与本步相关的按需工具：`brain-alpha-repair` 只作配方查表；单条表达式修复走 [`wq-brain-alpha-optimization-v1`](../../wq-brain-alpha-optimization-v1/SKILL.md)；阈值不达标的修法族见 [`brain-how-to-pass-alpha-test`](../../brain-how-to-pass-alpha-test/SKILL.md)。

## 7.10 完成定义

本波每条候选都有去向：进步 8（过 ④）/ 留在 near / salvage（带墙名）/ 判死（进步 9 的封存）；`s4_walls_<region>_<wave>` 已写。
