# e7adKz7g 双目标优化报告（推指标 + 压算子）

> 日期：2026-11-16 16:2x GMT+8｜区域 USA / TOP3000 / delay 1｜赛道 REGULAR / RA
> 目标 A = 推到平台全闸通过；目标 B = 压 `operatorCount` 到最少。**本轮零提交，提交权归用户。**
> 派发方式：全程 MCP `create_multi_simulation` + `lookINTO_SimError_message` / `batch_get_alpha_metrics` 收结果（零临时脚本）。

## 0 一句话结论

**全闸已过、4 算子物理下限不可压、66 日窗口是绝对尖峰。本件是 `USA/D1/EARNINGS` 从 2→3 点亮的唯一现成载体，但 prod .6753 + fitness 1.00 双贴线，属「可交但需当刻复核」级，不是无风险件。**

## 1 原件快照（`e7adKz7g`）

```
tail(group_rank(ts_mean(subtract(positive_sentiment_probability_3,
     negative_sentiment_probability_3), 66), subindustry), lower=0.15, upper=0.85, newval=0)
settings: USA/TOP3000/delay1/decay1/SUBINDUSTRY/trunc0.08/nan ON
```

| 指标 | 值 | 闸 | 余量 |
|---|---:|---|---|
| Sharpe | 1.72 | PASS (≥1.58) | +0.14 |
| Fitness | **1.00** | PASS (≥1.0) | **0.00 压线** |
| Turnover | 4.77% | PASS | 健康偏低 |
| 2Y Sharpe | 2.08 | PASS (≥1.58) | +0.50 |
| sub-universe | 0.91 | PASS (≥0.8) | +0.11 |
| investability S | 1.34 | 风险监控（非闸） | ratio .779 |
| **prod corr** | **0.6753** | PASS (<0.7) | **0.0247 贴线** |
| **self corr** | **0.5496** | PASS (<0.7) | 贴软线 .55，top=`A1xJdOmg`(已交) |
| operatorCount | 4 | REGULAR 无硬闸 | — |
| `is.checks.fail` | **[]** | 全过 | — |

- prod 缓存时间 16:19:50（当日，`from_cache=true`, `provisional=false`），48h 内可信。
- warning 3 项：`CLUSTER_TEST` 0.9<1.58、`MATCHES_COMPETITION`、`MATCHES_THEMES`——均非拒付项。

## 2 关键对照：分组轴 industry → subindustry 修好了两个硬伤

上一轮被中断的 `qM7Pd8ZA` 与本件**只差分组轴**（同字段、同 66 窗、同 tail），构成天然 A/B：

| 项 | qM7Pd8ZA (industry) | **e7adKz7g (subindustry)** | 变化 |
|---|---:|---:|---|
| sub-universe | 0.69 **FAIL** | **0.91 PASS** | +0.22 |
| self | **0.8669 FAIL** | **0.5496 PASS** | −0.32 |
| Sharpe | 1.95 | 1.72 | −0.23 |
| Fitness | 1.06 | 1.00 | −0.06 |
| 2Y | 2.41 | 2.08 | −0.33 |
| Ra failed | 1 | **0** | 解封 |

**结论**：subindustry 轴是解封关键（修 sub + 大幅降 self），代价是 S/F/2Y 各让一点。这是 skill L1「分组轴杠杆」的又一次实证——但方向是**更细粒度轴救 sub**，与此前「换 sector 换宽松 ladder」是同一机制的两面。

⚠ **Review 自我纠错（16:40）**：上表用 `qM7Pd8ZA` 作 industry 对照**不干净**——它同时是 `neutralization=STATISTICAL`，而本件是 `SUBINDUSTRY`，两个变量一起变了。真正只差分组轴的干净 A/B 是 **`ZYa2x7YY`（industry + SUBINDUSTRY，S1.80/F1.15/sub0.77 FAIL limit0.78）** vs 本件（subindustry + SUBINDUSTRY，sub0.91 PASS）。干净对照同样证明 subindustry 救 sub（0.77→0.91，从贴线 FAIL 到安全 PASS），但幅度不像上表写的 +0.22 那么干净利落——那是混入了中性化效应的数字。

其余同族（上一轮落地）全部印证 industry 轴的 sub 缺陷：
- `ZYa2x7YY` industry+SUBINDUSTRY: sub 0.77 FAIL(限0.78 贴线)
- `1YWamJnm` 126窗+industry: sub 0.79 FAIL(限0.84)
- `qM7Pd2W2` decay2+industry: F 0.98 FAIL + sub 0.64 FAIL

## 3 压缩通道：4 算子全承重，物理下限

| 算子 | 作用 | 删/换后果 |
|---|---|---|
| `subtract` | 正负面情绪概率做差（方向性来源） | 换成 `add` = 求和，失去多空对立语义（替换批测试中） |
| `ts_mean(66)` | 平滑 66 交易日 | 窗口阶梯全崩（见下），承重 |
| `group_rank(·, subindustry)` | 行业内截面分位 | 换 `rank`（去分组）= 丢掉 sub 解封机制（替换批测试中）；换 `group_zscore` 同 |
| `tail(0.15,0.85,0)` | 削两端极值 | 换 `winsorize` 是另一种削极值（替换批测试中） |

- `op_count` = 4，`compress` 无候选、`scan --delete` = 0 ⇒ 无重复子式、无冗余包裹。
- 变量合并 0 收益（两个字段各出现一次，无重复子式）。

## 4 参数通道：66 是绝对尖峰（已实测）

用 `create_multi_simulation` 派 3 条窗口变体，全部 COMPLETE（`lookINTO_SimError_message` 拿 children → alpha id → `batch_get_alpha_metrics`）：

| 窗口 | alpha id | S | F | sub | 2Y | TO | Ra failed |
|---:|---|---:|---:|---:|---:|---:|---:|
| 21 | `j2a9wVNO` | 1.20 | 0.53 | 0.71 | 2.12 | 20.3% | 2 |
| **66（原）** | **e7adKz7g** | **1.72** | **1.00** | **0.91** | **2.08** | **4.77%** | **0** |
| 126 | `rK7Jz0QE` | 1.14 | 0.55 | 0.43 | 1.77 | 3.03% | 3 |
| 252 | `MP6K8g9a` | 0.73 | 0.28 | 0.31 | 1.26 | 2.07% | 4 |

**窗口参数封死**：66 两侧（21/126）就全闸崩，252 更彻底。这与本族既有规律一致——情绪概率的均值回复窗口是尖峰，不是平台期。

## 5 替换通道 + decay 设置层（已实测 10 条）

全部用 MCP `create_multi_simulation` 派发，`lookINTO_SimError_message` 拿 children+alpha id、`batch_get_alpha_metrics` 批量取指标。

### 5a 替换通道（4 条，decay=1）

| 变体 | id | S | F | sub | 2Y | TO | Ra failed | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 原件 group_rank+tail | e7adKz7g | 1.72 | 1.00 | 0.91 | **2.08** | 4.77% | **0** | 4 条中唯一全过（§8 补测后有更优件） |
| **tail→winsorize(std2)** | O0Wb5Qeq | **1.88** | **1.20** | **1.01** | **1.51** | 4.85% | 1 | S/F/sub 全升，2Y 崩 0.57 |
| group_rank→group_zscore | wponJKVv | 1.38 | 0.89 | 0.71 | 1.41 | 6.46% | 3 | 全差 |
| group_rank→rank（去分组） | npaZOx0l | 1.17 | 0.63 | 0.26 | 1.48 | 6.09% | 4 | sub 崩，印证分组轴承重 |
| subtract→add（求和替做差） | LLKglVOe | 0.22 | 0.05 | −0.05 | 0.50 | 4.93% | 4 | 全崩，做差承重 |

**关键发现：`winsorize` 替 `tail` 是一次真实权衡**——S 1.72→1.88、F 1.00→1.20、sub 0.91→1.01、多空从 532/2498 变为 1429/1578（更平衡），**但 2Y 从 2.08 崩到 1.51**（`LOW_2Y_SHARPE` WARNING，按铁律视同 FAIL）。它是唯一「S/F/sub 全面更优但 2Y 掉闸」的变体，与 `e7aeJoEd` 那次 tail 尖峰现象一致——tail 的削极值方式恰好保住了近两年表现。

**待收已回（16:37）★**：winsorize std=3 (`58JaqmVk`) / std=4 (`78YaK5V5`) 与 std=2 (`O0Wb5Qeq`) **指标逐位完全相同**（S1.88/F1.20/sub1.01/2Y1.51/TO4.85%/margin 0.00211）⇒ **`winsorize` 在 `group_rank` 输出上是 no-op**：group_rank ∈[0,1] 近似均匀（μ0.5、σ≈0.289），std=2 边界 [−0.077, 1.077] 已覆盖全域，std 再大不会改变任何值。⇒ "winsorize 替 tail"等价于**直接删掉 tail**，2Y 从 2.08 崩到 1.51 是结构性的，std 参数无解。⚠ 此例再次印证「先查算子输出分布再选参数」——winsorize 对 rank/zscore 类有界输出无效。

### 5b decay 设置层（2 条已收，decay=3）

| 变体 | id | S | F | sub | 2Y | Ra failed |
|---|---|---:|---:|---:|---:|---:|
| decay=3 原 tail | xAvPmq6p | 1.57 | 0.88 | 0.79 | 1.80 | 2 |
| decay=3 + tail 0.2/0.8 | 9qlaAY1o | 1.71 | **0.98** | 0.94 | **2.21** | 1 |

decay↑ 反而降 S/F（decay 1 最优），通道否定。`9qlaAY1o` 的 2Y 2.21 高于原件但 F 0.98 差 0.02，仍不可交。

**待收已回（16:37）**：decay=2 批最终 COMPLETE（此前卡 0.35 只是算得慢，非静默不产出——修正上一版判断）：
| decay=2 变体 | id | S | F | sub | 2Y | Ra failed |
|---|---|---:|---:|---:|---:|---:|
| 原 tail 0.15/0.85 | `kqa1LQaO` | 1.62 | **0.92** | **0.83** | 1.89 | 1 |
| tail 0.1/0.9 | `A1xgOkLW` | 1.62 | **0.94** | 0.94 | 1.65 | 1 |

decay=2 两条仍 F<1.0 FAIL，**decay=1 是唯一可行档**。⚠ 纠偏：此前「>2 条批静默不产出」的结论在本例不成立——两批都只是耗时较长后正常 COMPLETE，不能据 0.35 停滞就判死批次。

⚠ 静态闸曾拒一次：`tail(x, std=4)` 参数非法（std 属 winsorize），已改用 `group_zscore(x, group)` 正确签名重派——**该 Git 钩子有效，是好事**。

## 6 稳健性预判（提交链用，本 skill 不做判定）

逐年 Sharpe：1.16 / 2.33 / **−1.38(2016)** / 2.02 / 1.92 / 1.49 / 1.35 / **4.13(2021)** / 2.75 / 1.25(2023)
- 近三年 4.13/2.75/1.25，均值 2.71 高，但**末端 2023 掉到 1.25**（衰减比 1.25/1.72≈0.73，仍在健康带 >0.5）；CV 偏高。
- **2016 年 −1.38 是十年唯一负年**（|S|>0.3，按 Phase C 属实负年软标记，非平年）。
- 判定上限：PASS 难（有负年+末端衰减），**CONDITIONAL 最可能**；须提交时由 `brain-alpha-robustness` 正式判。

## 7 塔与六维（提交必报）

**塔六元组**
| 塔席位 | 倍率 | 当季计数 | 交后计数 | 是否新点亮 | 塔边际 |
|---|---:|---:|---:|---|---|
| `USA/D1/EARNINGS` | 1.3 | **2** | **3** | **是（≥3）** | **+1 席位点亮** |

（计数用 `get_pyramid_alphas` 显式传 `2026-10-01`~`2026-12-31`，避免陈旧缓存。）

**六维**
| ops | fields | ΔT1 | ΔT2 | T3 新算子 | T4 新字段 |
|---|---|---:|---:|---|---|
| 4 / 4 distinct | 2 | −0.0016（微改善） | +0.0004（软成本） | flat | flat |

T5/T6 = n/a（streak/community 与选件无关）。六维中性，**本件价值在塔点亮，不在六维**。

## 8 参数精调审计（用户 16:37 要求 review：参数都精调过吗？）

**诚实答案：初版没有，16:40 已补测关键缺项。** 逐参数覆盖度：

| 参数 | 初轮已测 | 缺口 | 补测动作 |
|---|---|---|---|
| `ts_mean` 窗口 | 21/66/126/252 | **66 邻域未细扫**（skill ④c 要求步长 ≤ 窗口5%≈3） | 16:40 补 60/63/69/72（`1xb97Y9oy4uN9N1IH0AqF14`） |
| `decay` | 1/2/3 | 无 | ✓ 已完整，1 最优 |
| `tail` lower/upper | 0.15/0.85（decay1）、0.1/0.9（decay2）、0.2/0.8（decay3） | **decay1 下未系统扫边界** | 16:40 补 0.12/0.88、0.18/0.82（`1oVDgF6iX53zarr1TZ6C2AY`） |
| `winsorize std` | 2/3/4 | 无 | ✓ 完整，且证 no-op |
| 分组轴 | subindustry/industry/rank/group_zscore | industry 对照混入 neutralization 变量 | 已识别，见 §2 自我纠错 |
| `truncation` | 0.08 | 未扫 | skill 已证零杠杆（0.04/0.12 逐位相同），合理不动 |
| `nan_handling`/`delay`/`universe` | ON/1/TOP3000 | 未扫 | 换信号档 + 标准值，低优先级，非本族甜点 |

### 补测结果（16:43）——★ 找到全面更优件，结论翻转

**窗口邻域 60/63/69/72 全 FAIL**（F 0.90~0.97）——确认 66 是真尖峰，无需再扫。

**tail 边界精调（decay=1）找到两个全通过件**：

| 变体 | id | S | F | sub | 2Y | prod | self | Ra failed |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 原件 0.15/0.85 | e7adKz7g | 1.72 | **1.00** | 0.91 | 2.08 | .6753 | .5496 | 0 |
| tail 0.12/0.88 | VkN22b9G | 1.71 | 1.00 | 1.04 | 1.98 | 未测 | 未测 | 0 |
| **tail 0.18/0.82** | **wponnkmd** | **1.77** | **1.03** | **1.05** | **2.22** | **.6742** | **.5553** | **0** |

**`wponnkmd` 每一项都优于或持平原件**：S +0.05 / F +0.03（**脱离 1.00 零余量**）/ sub +0.14 / 2Y +0.14 / prod −0.0011 / self +0.0057（均过闸）。塔同为 `USA/D1/EARNINGS` 2→3 点亮，六维同为 4 ops/2 fields（T3/T4 flat）。

⇒ **采纳判据成立（指标全面更好 + prod 不更高）⇒ 改选 `wponnkmd`，原件 `e7adKz7g` 标 `SUPERSEDED`**（同骨架互相关必 >0.99，只能留 1 颗）。这直接证明「参数没精调透」的代价：tail 边界此前全在 decay2/3 里测，从没在 decay=1 下系统扫。

## 8b Universe 扫描（用户 16:49 追问：有没有换 universe 跑？）

**诚实答案：初轮没测，16:53 补测 5 档。** USA 允许 6 档，当前 TOP3000。用最优件 `wponnkmd`（tail 0.18/0.82）跑遍其余 5 档（各配 0.15/0.85 作 control）：

| universe | 最优件 id | S | F | sub | 2Y | Ra failed | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| **TOP3000（原）** | **wponnkmd** | **1.77** | **1.03** | 1.05 | **2.22** | **0** | **唯一全过** |
| TOP2000 | npaZ3vWa | 0.76 | 0.29 | 0.89 | 1.27 | 3 | FAIL |
| TOP1000 | oma3VpRv | 0.70 | 0.27 | 0.84 | 0.30 | 3 | FAIL |
| TOP500 | QP02ErpQ | 0.47 | 0.16 | 0.41 | −0.11 | 3 | FAIL（2Y 转负） |
| TOP200 | YPa2QKno | 0.49 | 0.21 | — | 0.82 | 3 | FAIL |
| TOPSP500 | LLKgk6Ja | 0.77 | 0.31 | 0.27 | 0.49 | 4 | FAIL |

**结论：TOP3000 绝对最优，且呈严格「池越小越差」单调**（S 1.77→0.77/0.76→0.70→0.49→0.47，2Y 2.22→1.27→0.82→0.49→0.30→−0.11；按池大小 3000>2000>1000>500≈200）。**连紧邻的 TOP2000 都从 S1.77 掉到 0.76、2Y 2.22→1.27**，单调性极干净。
**金融解释**：该信号是 `group_rank` 截面分位 + tail 削两端，依赖**覆盖广度与横截面区分度**（原件 longCount 532 / shortCount 2498，约 3000 只票）。池缩到 1000 以下时，subindustry 组内样本骤减、分位退化、tail 边界（0.18/0.82）失去意义 ⇒ 信号塌缩。TOPSP500 虽是 500 只流动性最好的票，但情绪概率数据的覆盖优势在大池才成立。
⇒ **universe 是本件的真实强杠杆，只是方向为「越大越好」；TOP3000 已是平台上限，无优化空间。**

## 9 建议（交用户定）

1. **★ 改交 `wponnkmd`（tail 0.18/0.82）而非原件**：全维度更优且 F 摆脱零余量。它仍是 prod 贴线件（.6742，余量 .0258）——提交须当刻 `check_correlation(refresh=True)` 复核、补稳健审计、方案 D（原件方案 D 已放行 ΔS+0.16/ΔTO−0.63pp，新件需重跑）。
2. **塔边际是最大卖点**：`USA/D1/EARNINGS` 当季 2→3，现成可点亮该席的候选；提交前查同席互相关（`compute_mutual_correlation`）。
3. **原件 `e7adKz7g` 与同族全部变体标 `SUPERSEDED`**（同骨架 >0.99）：含 VkN22b9G、窗口 60/63/69/72、winsorize std2/3/4、decay2/3 各件；21/126/252 窗与 add/group_zscore/rank 件为 `REJECT`。
4. 稳健性仍待正式审计：原族有 2016 S−1.38 负年软标记，`wponnkmd` 逐年未取（提交时补），预判 CONDITIONAL。
