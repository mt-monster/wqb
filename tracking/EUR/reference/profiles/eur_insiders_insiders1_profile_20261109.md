# EUR × insiders1 字段画像（2026-11-09）

> 9/9 全量（complete=true）；Global Insider Trading Data（全球内部人交易）
> 塔位：INSIDERS(×1.1，2/3)；拥挤度：aC 394 / uC 191；os_is 0.3509

## 一、字段清单（9 字段，全 VECTOR，cov 0.5512）
insd1_shares（交易股数，uC 72 最热）、insd1_price（交易价）、insd1_value/valueeur（交易金额）、insd1_holdings（交易后持股）、insd1_tradesignificance（交易重要性 1-5 分）、max_trade_price、insd1_gvkey（标识）、transaction_currency_code

## 二、判定
1. **cov 0.5512 < 0.85 → 覆盖判死**（sub 闸结构性不可达）
2. 事件型 VECTOR → TO 爆炸风险（同族 insider_feats/insider_trx_matrix 均已 TO 判死）
3. **判定：覆盖判死 + 同族 TO 前科，排除**

## 三、2026-11-20 实测修订（覆盖判死被推翻）

按用户「实践大于约束」，对 insiders1 做 14 臂实测（论坛取证→preflight→3 批 multisim→逐年归因，全程 EUR/D1/TOP2500）：
- **旧判「cov 0.5512 < 0.85 覆盖判死」被推翻**：`ts_backfill(...,60~120)` 后 **LOW_SUB_UNIVERSE_SHARPE 全部 PASS**，TO 2.6%–10% 全部 PASS，CONCENTRATED_WEIGHT/金字塔全部 PASS ⇒ **覆盖不是瓶颈，信号强度才是**。
- **EUR 最好 S=0.64 / F0.27 / 2Y0.48 / sub0.52 / TO7.55%**（blaO528K = `rank(-ts_backfill(vec_sum(insd1_holdings),60))`，SECTOR/decay1）；全部 14 臂 REJECT，距 S1.58/F1.0/2Y1.58 差距极大 ⇒ **信号层天花板（PROVISIONAL，非数据集级死）**。
- **DEU 先验在 EUR 不成立**：70 赞「流量÷存量」三臂全败（S −0.21/0.18/−0.32）；真正有效的是**方向反转**——持股存量正向 S−0.43 → 反向 S0.64、金额 ts_mean 正向 S−0.63 → 反向 S0.55 ⇒ EUR 上 insider 存量/金额是**弱均值回复**（高暴露→低前瞻收益），不是动量。
- 逐年（blaO528K）：long/short 全年份>0，但 pnl>0 仅 8/10 年（2018 近平、2021 −321628）⇒ 近十年不干净，二次扣分项。
- **字段→合法模板白名单**：信号 = `insd1_holdings`(反向,最佳)/`insd1_price`(vec_avg 正向弱)/`insd1_valueeur`(反向)/`insd1_shares`(弱)；门控 = `insd1_tradesignificance`(合取机制成立但符号需核)；排除 = `insd1_value`(原币口径)、`transaction_currency_code`、`insd1_gvkey`(元数据)。降维 vec_sum/vec_avg，回填 ts_backfill 60–120。
- 论坛锚：post 43794123838615（GBR Insiders+PV，VECTOR 须降维/回填顺序/decay）、44731710962839（三信号对齐+right_tail 门控，实测 right_tail 在本平台 preflight 报 unknown 已剔除）、44177254293143（110 赞，ts_backfill 把稀疏覆盖 33%→近100%）。

### 3.1 标准流程补齐（2026-11-20）

用户问「按标准流程开了回测没」→ 核对发现论坛/preflight/multisim/归因均已做，缺两项，已补：
1. **外部金融论文（EVID-PAPER 多样闸）**：`tools/research/paper_search.py --query "insider trading stock returns predictability, insider ownership change returns, insider buying selling anomaly, corporate insiders transactions information" --diverse` → **diverse_ok=True，20 篇/14 作者**（≥5 篇 ∧ ≥3 作者 达标）。代表题录：*The Forecasting Properties of Insiders' Transactions*（1964, JF, 10.1111/j.1540-6261.1964.tb02901.x）、*Insider trading and future stock returns in firms with concentrated ownership levels*（2018, 10.1080/1351847x.2018.1487312）、*Insider Trading in Germany*（2008, 10.1007/bf03343533）、*Short Interest, Insider Trading, and Stock Returns*（2009）。**Crossref 仅题录、摘要多不可得**——按项目规则题录级多样闸通过。
2. **campaign 流水线 dry-run**：`campaign.py --campaign-dir tracking/EUR pipeline run --dataset insiders1 --wave insiders1_eur_20261120 --no-from-db --file <exprs> --dry-run --fresh` → **dead-guard OK（insiders1 不在死表）｜gate total=4 passed=4 failed=0｜batch_gates ok=True｜n_slots=1（batch=8）｜未提交**。踩坑记录：① `--file` 不带 `--no-from-db` 会被忽略（默认从 DB 读 wave=1 的 16 条别的表达式）；② 同 wave 重跑必须加 `--fresh`，否则 checkpoint 复用上次失败的 passed=0。

### 3.2 按画像全标准流程重跑（2026-11-20）

用户「按字段画像重跑一遍标准流程回测」→ 完整走：论坛（新证据 group_backfill 补覆盖 / ts_backfill250 / F 规则 TO≤ret·S²）→ **EVID-PAPER 多样闸（20 篇/14 作者）** → 基于 §3 字段白名单设计 10 条新形态（group_backfill、长回填250、tradesignificance 门控——均非上轮测过）→ preflight 10/10 通过 → **2 批 create_multi_simulation（SECTOR/decay1 + SUBINDUSTRY/decay4）**→ 收割 + 流水线 dry-run（gate 5/5、n_slots=1、dead-guard OK）→ 归因。

**结果：10 臂全 REJECT，未突破上轮 S0.64 天花板**（最好 RRe6L32d = `rank(-ts_sum(ts_backfill(vec_sum(valueeur),60),63))` S0.88/F0.39/2Y1.18；SECTOR 批最好 pwa5gV5v S0.74）。

| 新形态 | 读数 | 判定 |
|---|---|---|
| `group_backfill(ts_rank(holdings,252),subindustry,63,std=2)` 反向 | SECTOR S0.14 / SUBIND S0.88 | 补覆盖但信号仍弱 |
| `ts_backfill(holdings,250)` 反向 | S0.45 | 长回填无效（晚申报不增信息） |
| `ts_rank(-backfill(holdings,120),252)` | S−0.39 | 时序相对化翻负 |
| `trade_when(significance>0.7, holdings反向, -1)` | S−0.38 | **门控合取在 EUR 失败**（与论坛 USA 帖前提不符——EUR 内部人申报更稀疏） |
| `ts_decay_linear(-backfill(holdings,120),5)` | S0.74 | 平滑小幅有效但不质变 |

**结论加固**：insiders1 是**信号层天花板**（两轮 24 臂，最好 S0.64→0.88，均 ≪1.58）；覆盖/TO/sub 全 PASS，`ts_backfill`/`group_backfill` 只补覆盖不造信号。**不判数据集死（PROVISIONAL）但停止投入**；该集 9 字段已全测、形态空间已穷尽。

### 3.3 分批不足质疑 → 设置轴 + 骨架补充（2026-11-20）

用户质疑「只派 2 批是不是太少」→ 复盘发现两处遗漏，已补 2 批 9 臂：
1. **设置轴遗漏**：历史 76 臂中 `TOPCS1600×SUBINDUSTRY` 有 40 臂（最多），我前两轮从未覆盖；补 `TOPCS1600×SECTOR/decay1` 5 臂 → **全 REJECT**（最好 P05gevAp S0.38）。
2. **骨架遗漏 + 风险线误读**：DB 历史 S1.20 的 6 层复杂骨架 `group_scale(tail(winsorize(group_zscore(流量÷存量×重要性)))` 此前没测过；补 4 变体到 `TOP2500×SUBINDUSTRY` → **S0.49–0.56，全 REJECT**；**根因：那 76 臂的 S1.20 其实来自 `TOPCS1600×SLOW_AND_FAST`（风险线，另一把尺子），不可作交付基准**——同骨架搬到标准档只剩 0.49。这是「读历史最优读数前先查 `risk_neutralized_sharpe` 签名」的又一实证。
3. **方向对照**：`-group_scale(...)`（骨架取反）S−0.49，对称翻转确认真实但极弱。

**结论加固**：累计三轮 33 臂（14+10+9），跨 TOP2500/TOPCS1600、SECTOR/SUBINDUSTRY/NONE、decay1/4、简单+6层复杂骨架，标准档最好仍 **S0.88**，INSIDERS 塔信号层天花板坐实。PROVISIONAL 停止投入。

### 3.4 三段式设置策略验证重跑（2026-11-20）

用户「重回测流程验证机制有无生效」→ 按 EUR skill `rules/settings-axis-strategy.md` 三段式实测：

**段0 档位净化（实际查证）**：历史 S1.20 = `1YNl3o7R` @ TOPCS1600×**SLOW_AND_FAST**，`get_alpha_details` **无 `risk_neutralized_sharpe` 字段** ⇒ 正确识别为风险线并剔除；标准档最好 `vR1poWNz` @ TOPCS1600×SUBINDUSTRY S1.14 **有 RN=1.39** ⇒ 正确保留，并记录「RN≫S = 风险拖累线索」（该发现已回写规则 §2 段0）。

**段1 历史分布+跨宇宙并行**：取历史 S1.14 复杂骨架（`group_scale(tail(winsorize(group_zscore(流量÷存量×重要性)))`）× {TOP2500, TOPCS1600} × {INDUSTRY, COUNTRY}，每格含方向对照（正/反），8 臂：
| 格 | S | F | 2Y |
|---|---:|---:|---:|
| TOP2500×IND | 0.41 | 0.13 | 0.33 |
| TOP2500×COUNTRY | 0.59 | 0.21 | 1.34 |
| **CS1600×IND** | **0.94** | **0.51** | 0.57 |
| **CS1600×COUNTRY** | **1.01** | **0.52** | **1.30** |

**段2 三分支判定（实测生效）**：最优 CS1600×COUNTRY S1.01/F0.52/2Y1.30 ⇒ gap_S=0.57、gap_F=0.48、gap_2Y=0.28、spread=0.07、S_required=1/√(0.033/0.125)=1.94，**best_S+spread=1.08 < 1.94 ⇒ C 分支否决 → 停止**，A/B 均不满足。未进段3 全设置。

**验证结论**：三段式机制 4 处全部生效——①档位净化剔除风险线（避免 S1.20 假基准）；②宇宙轴优先（CS1600 两格 0.94/1.01 ≫ TOP2500 两格 0.41/0.59，与 0.63–0.86 摆幅先验一致）；③A/B 不放行；④C 数学否决。累计 41 臂标准档最好 S1.01（复杂骨架），简单骨架历史最好 S0.88 ⇒ **insiders1 天花板不变，停止投入**。另修复机制落盘缺陷：规则文件磁盘名与 README 链接曾不一致（内容改名但文件未改），已修正 + sync 5 安装位。

## §3.5 同类别算子全替换轮（2026-11-20，用户新规则首次实盘）

基线 `blaO2YVN`（六层骨架 ts_sum44，CS1600×COUNTRY×decay4）S1.01/F0.52/TO4.18%/2Y1.30。替换轴 = `ts_sum`，工具 `tools/operator_swap_matrix.py` 产出 16 合法替换（6 个 arity/no-op 跳过，`ts_product` 撞 UNITS 闸）。设置与基线逐项对齐（nanHandling ON；实测 ON/OFF 在本族逐位相同，空操作）。

| 算子 | S | F | TO | 2Y | ΔS |
|---|---:|---:|---:|---:|---:|
| **ts_sum（基线）** | **1.01** | **0.52** | 4.2% | **1.30** | — |
| ts_arg_min | 0.54 | 0.20 | 17.2% | 0.09 | −0.47 |
| ts_max_diff | 0.49 | 0.13 | 145.8% | 0.36 | −0.52 |
| ts_arg_max | 0.36 | 0.11 | 17.3% | 0.39 | −0.65 |
| ts_ir | 0.32 | 0.11 | 16.8% | 0.82 | −0.69 |
| ts_mean | 0.20 | 0.05 | 10.2% | 0.14 | −0.81 |
| ts_returns | 0.17 | 0.05 | 38.6% | 1.05 | −0.84 |
| ts_av_diff | 0.08 | 0.01 | 135.5% | 0.63 | −0.93 |
| ts_std_dev | 0.02 | 0.00 | 13.1% | −0.78 | −0.99 |
| ts_rank | −0.04 | 0.00 | 153.4% | 0.16 | −1.05 |
| ts_zscore | −0.09 | −0.01 | 147.4% | 0.18 | −1.10 |
| ts_delta | −0.16 | −0.04 | 38.0% | 0.01 | −1.17 |
| ts_quantile | −0.20 | −0.04 | 133.9% | −0.17 | −1.21 |
| ts_kurtosis | −0.24 | −0.08 | 23.3% | −0.50 | −1.25 |
| ts_scale | −0.31 | −0.07 | 145.3% | −0.72 | −1.32 |
| ts_decay_linear | 0.00 | 0.00 | 152.1% | 0.11 | −1.01 |

**内核定性：本族 alpha 在「内部人累计买入的截面水平」上，不在时序形状上。**
- 时序相对化族（ts_rank/ts_zscore/ts_quantile/ts_scale）全灭 ⇒ 扔掉 level 就扔掉 alpha。**与 institutions6「买家比例是内核」相反**（那里 ratio 是本，这里是 level）。
- `ts_mean` ΔS −0.81：稀疏事件流下按有效观测数归一 ⇒ **`ts_mean ≠ ts_sum/44`**（§17.1 的 no-op 只在窗内有效数恒定时成立）；「申报频次」本身是信息。
- `ts_decay_linear` 归零且 TO 152%：平滑**存量**型信号只制造换手 —— 与 GBR news50（噪声型族）结论相反。
- 判定：**算子轴已穷尽，ts_sum 不可替代**；剩余缺口（S 1.01→1.58、F 0.52→1.0）只能靠换信息源/换经济机制（buy·sell 分向、稀释 vs 增持），非算子替换可解。按 §2.1 C 分支不进设置轴扩网格。
- 详档 `output_report/EUR_insiders1_operator_swap_20261120.md`。

### §3.5.1 ts_product UNITS 解法补测（2026-11-20）

上一轮 `ts_product(divide(multiply(vec_sum(insd1_valueeur), vec_avg(insd1_tradesignificance)), vec_sum(insd1_holdings)), 44)` 撞 UNITS 闸（`expected Unit[], found Unit[CSPrice:1]`）。
**根因**：内层 valueeur/holdings 量纲 = EUR/股 = CSPrice（价格）；`ts_product` 逐日连乘会放大量纲幂次，平台要求输入**无量纲 Unit[]**——连乘比加减对量纲严格得多（ts_sum/ts_mean 对加法只查可加性，乘法对幂次零容忍）。

**正确用法两条路（实测均跑通）**：
1. **rank 包裹（几何累积形态）**：`ts_product(rank(x), d)` —— rank 输出 [0,1] 无量纲，连乘 ≈ 对数空间累积，惩罚窗内低值日；
2. **复利形态**：`ts_product(add(1, ts_returns(x, 1)), d)` —— 日变化复合增长因子，天然无量纲。

3 臂读数（设置同基线 CS1600×COUNTRY×decay4×nanHandling ON）：

| 形态 | alpha | S | F | TO | 2Y | ΔS vs ts_sum 基线 |
|---|---|---:|---:|---:|---:|---:|
| rank 包裹 · 44d | pwa57eOq | 0.14 | 0.03 | 4.5% | 0.46 | −0.87 |
| 复利形态 · 44d | d5a1QrLE | −0.06 | −0.01 | 9.0% | 0.16 | −1.07 |
| rank 包裹 · 66d · 简骨架 | QP0KQpXG | −0.50 | −0.15 | 3.8% | −1.24 | −1.51 |

**归因**：连乘机制与「累计买入水平」内核相斥——rank 连乘惩罚窗内低值日（申报稀疏日直接把乘积打到≈0），复利形态连乘的是噪音比率。**insiders1 算子替换至此 19/19 全劣化，ts_sum 最优结论加固**。
