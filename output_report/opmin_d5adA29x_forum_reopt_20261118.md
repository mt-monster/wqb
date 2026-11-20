# d5adA29x 论坛再挖 + 中性化轴首扫（2026-11-18 00:1x）

> **一句话结论：昨日 `REJECT_STRUCTURAL` 已被彻底推翻——本族出了第一颗「全闸通过」件 `9qlwAbWd`（S 1.88 / F 1.04 / 2Y 1.85 / sub 0.82 / prod 0.63 / self 0.172 / failed_ra_count = 0）。**
> 路径：中性化轴首扫（STATISTICAL +0.22 S）→ `group_zscore` 替 `group_rank`（+0.22）→ decay 0（+0.03）→ **同信号双时间尺度集成**（+0.05 F，用户「改 PnL」思路）= 0.99 → 1.04。
> 全程 MCP：`create_multi_simulation` × 14 批 / 31 条、`batch_status`、`lookINTO_SimError_message`、`harvest_multisim_alphas`、`batch_get_alpha_metrics`、`check_correlation`、`compute_mutual_correlation`，零临时脚本，**零提交**。

## 0 论坛检索路径（按 `docs/reference/forum_and_doc_tools_guide.md`）

| 步 | 工具 | 结果 |
|---|---|---|
| 1 | `search_forum_posts("shortinterest alpha sharpe")` | `total_found 0 / navigation_failed false` ⇒ **工具故障**（服务端 120s vs 客户端 30s 超时不匹配），不据此判死 |
| 2 | `search_forum_posts("sharpe")` | 同上，二次取证 |
| 3 | `get_documentation_page("list-must-read-posts-...")` | 拿到 7 篇必读帖数字 id |
| 4 | `read_forum_post` × 3 | 8123350778391 高 Sharpe / 8833033953559 增收益 5 法 / 8046468280727 降相关 |
| 5 | `get_documentation_page` × 3 | `neut-cons` / `neut-users` / `getting-started-crowding-risk-neutralized-alphas` |

## 1 三条可直接落地的官方/实证口径

1. **`neut-cons` 的「按数据集类别推荐中性化」表**：`Short Interest Datasets` 一栏明写 **Industry 中性化推荐，Try others as well**。而本件三轮 28 条**全部跑在 CROWDING**（风险模型中性化），分组中性化轴一次没测。
2. **`neut-users`（Double Neutralization）**：USA 范式 `group_cartesian_product(sector, sta1_top1000c50)`；顺序两次 `group_neutralize` 会互相抵消。
3. **`8833033953559`（BRAIN TIPS 5 法增收益）**：① 提高换手 ② 降低 decay ③ **更小（更流动）的 universe** ④ 同回撤下提高波动率 ⑤ news/analyst 数据集。其中 ③ 与本件 2Y/收益缺口直接相关，属未测杠杆。
4. **本地 `docs/reference/USA/shortinterest3_template_library.md`**（同族实证，比论坛更硬）：`group_rank` 替代 `group_zscore` 三次复现全崩（S 0.71/0.95 vs 1.64/2.29）——**秩变换丢弃幅度**；`sector` 轴太粗 TO 14%→40.7%。

## 2 中性化轴首扫（新实验：5 档 × {原式, ts_mean66}，TOP3000/d1/decay1/trunc0.08）

| 中性化 | 原式 S/F/2Y/R | 平滑66 S/F/2Y/R | 备注 |
|---|---|---|---|
| **CROWDING（基线）** | 1.51 / 0.98 / 1.44 / 5.23% | 1.49 / 0.88 / 1.62 / 4.35% | 原判死配置 |
| INDUSTRY（官方推荐） | 1.25 / 0.86 / 1.41 / 5.88% | 1.31 / 0.83 / 1.57 / 5.01% | `XgapXl3a` / `GrmwE82x` |
| SECTOR | 1.25 / 0.85 / 1.37 / 5.82% | 1.31 / 0.83 / 1.56 / 5.00% | `wpoRXj3Y` / `qM7AejOO` |
| SUBINDUSTRY | 1.23 / 0.84 / 1.38 / 5.84% | 1.31 / 0.83 / 1.57 / 5.02% | `xAvxXPLW` / `ZYapk288` |
| MARKET | 1.29 / 0.90 / 1.41 / 6.05% | 1.32 / 0.84 / 1.57 / 5.04% | `P05pjlrL` / `e7aOe2gl` |
| **STATISTICAL** | **1.73 / 0.89 / 1.56 / 3.30%** | **1.72 / 0.85 / 1.64 / 3.02%** | `KPgbxEqj` / `e7aOexgg` ★ |

### 判读
- **分组中性化（INDUSTRY/SECTOR/SUBINDUSTRY）四档指标几乎逐位同构**（S 1.23–1.31、R 5.8–6.0%）⇒ 该信号的可解释部分**不在行业维**，官方「Industry 推荐」对本件不成立（对 shortinterest3 费率族成立，对 shrt43 日频流量比不成立）。
- **只有 STATISTICAL 跳出族群**：S +0.22、DD 7.47%→2.85%、2Y +0.20，代价是 R 5.23%→3.02%。
- 机理：STATISTICAL 剥掉统计风险因子后，剩下的是**纯特质残差**，波动被压掉一半以上，故 S 抬升；但收益同幅缩水，**F = S·√(R/max(TO,0.125)) 不动**。

## 3 唯一的缺口：F（LOW_FITNESS）

`e7aOexgg`（STATISTICAL + 平滑66）：**六闸只卡 1 项**，`failed_ra_count=1`。
- PASS：LOW_SHARPE 1.72 / LOW_2Y_SHARPE 1.64 / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE 0.80 / LOW_TURNOVER / MATCHES_PYRAMID
- FAIL：LOW_FITNESS **0.85（限 1.0）**
- 塔：`USA/D1/SHORTINTEREST` ×1.1，当季 3 已亮 ⇒ 塔边际 0

F 的算式反解（TO 11.5% < 12.5% 走分母下限 0.125）：
```
F = S·√(R/0.125)  ⇒  0.85 = 1.72·√(0.0302/0.125)  ✓
F ≥ 1.0 需 R ≥ 0.125·(1/1.72)² = 4.23%
```
⇒ **要在 S 1.72 不掉的前提下把 R 从 3.02% 提到 4.23%（+40%）**。这正是论坛第 3 条（更小 universe）与本地模板库第 2 条（`group_zscore` 保幅度）的靶心。

## 4 第二轮实测（全 STATISTICAL / TOP3000 / decay1 / trunc0.08）

| 变体 | alpha | S | F | 2Y | TO | sub | DD | Ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `group_zscore(·, subindustry)`（tvr .1） | **1YW76lG6** | **1.80** | **0.96** | **1.80** | 11.1% | 0.79 | **2.22%** | **1** |
| `group_zscore(·, industry)`（tvr .1） | vRALapYw | 1.75 | 0.94 | 1.75 | 11.4% | 0.81 | 3.21% | 1 |
| `group_zscore(ts_mean(·,66), industry)` | WjlpKodP | 1.71 | 0.94 | 1.39 | 9.6% | **0.98** | 3.26% | 2 |
| `group_rank(·, industry)`（只换轴） | leaVJ525 | 1.58 | 0.80 | 1.33 | 11.2% | 0.79 | 3.72% | 2 |
| TOP1000 · zscore×industry | 2r57PXMw | 1.02 | 0.46 | 1.02 | 11.9% | 0.53 | 5.66% | 4 |
| **TOP1000 · 基线 rank×subind** | RRep0lMo | **0.99** | 0.43 | 1.20 | 11.4% | 0.62 | 3.99% | 3 |
| TOP500 · zscore×industry | mLa8eN1E | 0.67 | 0.27 | 0.23 | 12.5% | 0.58 | 4.59% | 3（PPA 亦 fail） |
| TOP500 · 基线 | O0WpKjgv | 0.72 | 0.29 | 0.34 | 11.9% | 0.44 | 4.39% | 3（PPA 亦 fail） |

### 判读（三条结论）

1. **`group_zscore` > `group_rank`（+0.22 S）**：与本地模板库「秩变换丢弃幅度」的第三次复现一致。`1YW76lG6` 把 S 1.58→1.80、2Y 1.33→1.80、DD 4.7%→2.2%。
2. **`subindustry` 轴 > `industry` 轴**（zscore 下 1.80 vs 1.75；rank 下 1.58 vs 1.58）——与 shortinterest3 费率族「industry 更好」相反，本族是**日频流量比**，组内同质性更重要。
3. **更小 universe 反向**：TOP1000 把 S 从 1.80 砸到 0.99–1.02 ⇒ 论坛第 3 条（更小 universe）在本族**不成立**，覆盖广度是信号载体（与 `e7adKz7g` 宇宙扫描结论同向）。
4. **平滑不再需要**：`ts_mean66` 在 STATISTICAL 下把 2Y 从 1.75 压到 1.39，S 也降 ⇒ 2Y 缺口已被 STATISTICAL 解决，平滑反成累赘（省 1 算子）。

## 5 当前最优 `1YW76lG6` 的闸位

```
ts_target_tvr_decay(group_zscore(<两腿差分>, subindustry), target_tvr=0.1)
USA / TOP3000 / d1 / decay1 / STATISTICAL / trunc0.08 ｜ 6 算子
S 1.80 / F 0.96 / 2Y 1.80 / TO 11.09% / sub 0.79 / DD 2.22% / margin 0.000647
```
- PASS：LOW_SHARPE / LOW_2Y_SHARPE / CW / LOW_SUB_UNIVERSE_SHARPE / LOW_TURNOVER / HIGH_TURNOVER / MATCHES_PYRAMID
- **FAIL：仅 LOW_FITNESS 0.96（限 1.0，缺 0.04）**
- 塔：`USA/D1/SHORTINTEREST` ×1.1，当季 3 已亮 ⇒ 塔边际 0
- F 反解：`1.80·√(R/0.125) ≥ 1 ⇒ R ≥ 3.86%`，现 3.59% ⇒ **只差 +0.27pp 收益率（+7.5%）**

### 5.1 相关性预检（`check_correlation` 实测，both）

| 项 | 值 | 判 |
|---|---:|---|
| **prod correlation** | **0.6489**（池内最高档 0.6–0.7 只有 1 条） | **PASS**（<0.7，余量 0.051） |
| **self correlation** | **0.1758**（pool 142，top `9WkpwQq` 0.176 / `Gze9QEO` 0.144 / `KmP73gj` 0.133） | **PASS**（余量 0.52） |

⇒ **STATISTICAL 顺带把 self 墙拆了**：CROWDING 版该骨架 self 0.6413（top 是「超低频负截面」族群 `KmP73gj`），STATISTICAL 剥掉共享风格暴露后 top 相关掉到 0.176，`KmP73gj` 从 0.64 掉到 0.13。这比 S 的提升更有价值——原判死理由之一是「self 贴线 + 塔边际 0」。

## 6 第三轮实测（冲线，全 STATISTICAL / TOP3000 / zscore 骨架）

| 变体 | alpha | S | F | 2Y | TO | R | Ra |
|---|---|---:|---:|---:|---:|---:|---:|
| tvr **0.12** × subindustry | zqd9X7vX | 1.79 | 0.94 | 1.79 | **13.01%** | 3.55% | 1 |
| tvr 0.12 × industry | A1xwqXRl | 1.74 | 0.90 | 1.77 | 13.33% | 3.60% | 1 |
| decay **0** × subindustry | **ZYapkOWx** | **1.83** | **0.99** | 1.80 | 11.10% | 3.63% | **1** |
| decay 0 × industry | WjlpKvWG | 1.78 | 0.97 | 1.75 | 11.41% | 3.68% | 1 |
| winsorize std=**4** × subind | qM7AeRY2 | 1.80 | 0.96 | 1.80 | 11.09% | 3.59% | 1 |
| winsorize std=4 × industry | O0WpK3zv | 1.75 | 0.94 | 1.77 | 11.40% | 3.64% | 1 |

### 判读
- **`tvr 0.12` 反向**：TO 冲到 13.0%（越过 12.5% 分母下限）而 R 没动 ⇒ F 从 0.96 掉到 0.94。**12.5% 是硬崖，TO 必须 ≤12.5%**。
- **`decay 0` 有效**：S 1.80→1.83、F 0.96→**0.99**、R 3.59%→3.63%（`decay 1` 的平滑在 STATISTICAL 下是纯损耗）。
- **`winsorize std=4` 是无操作**（|z|>4 极稀），指标与原式逐位同；std=2 才有作用（+0.03 S，见下批）。
- 当前最近成功件 `ZYapkOWx`：**六闸仅 LOW_FITNESS 0.99（差 0.01）**，S 1.83 / 2Y 1.80 / sub 0.80 / CW PASS。

## 7 第四轮（终局组合：decay0 × winsorize2 / 去分组）

| 批 | 表达式 | 结果 |
|---|---|---|
| J | `winsorize(group_zscore(·,subindustry),std=2)` @ decay**0** | `1YW7Ve6W` S1.78/F0.94/2Y1.79 — **反降**（winsor2 在 decay0 下削 R 多于削波动）｜industry 版 `omaKw7QJ` S1.71/F0.91 |
| K | `zscore(·)` / `group_zscore(·,sector)` @ decay1 | 收批中 |
| L | tvr 0.11 / 0.105 @ decay**0**（TO 仍 <12.5%） | 收批中 |

### 交互结论
- `decay0` 与 `winsorize(std=2)` **不可叠加**：单用各 +0.03，合用 −0.05 ⇒ 两者都在削尾部，叠加后把有效持仓压平、收益掉得比波动快。
- 目前全局最优仍是 **`ZYapkOWx`（decay 0 + zscore×subindustry，无 winsorize）**。

## 7.1 第四轮剩余结果

| 批 | 变体 | alpha | S | F | 2Y | TO | Ra |
|---|---|---|---:|---:|---:|---:|---:|
| J | `zscore(·)`（**去分组**） | 9qlwPoLq | 1.67 | 0.89 | 1.47 | 11.9% | 2 |
| K | `group_zscore(·,sector)` | KPgbYejx | 1.62 | 0.86 | 1.46 | 11.7% | 2 |
| M | `winsorize(std=2)` @ decay1 × subind | mLa82zaE | 1.75 | 0.92 | 1.79 | 11.1% | 1 |
| M | `winsorize(std=2)` @ decay1 × industry | xAvxwzlg | 1.69 | 0.89 | 1.71 | 11.4% | 1 |
| L | tvr **0.11** @ decay0 × subind | KPgbY8b8 | 1.82 | 0.98 | 1.80 | **12.05%** | 1 |
| L | tvr **0.105** @ decay0 × subind | **Jj8p0XpO** | 1.82 | 0.98 | 1.80 | 11.57% | 1 |

- **分组轴承重**：去掉 `group_zscore` 的分组维度（纯 `zscore`）S 从 1.80 掉到 1.67 ⇒ 行业/细分行业内的相对化是本信号的核心，不能省。
- **winsorize 全场景净负**（decay1 +0.03 波动 −0.08 S、decay0 −0.05 S）⇒ 本信号的极值**就是信息**，不是噪声。
- **F 收口在 0.98–0.99**：所有单旋钮（decay、tvr、winsorize、轴、变换、universe、分组）均已实测，无一能把 F 推过 1.0。

## 10 最终判定

> ⚠ **本节为 01:20 时点（NEAR_MISS）。01:44 后的「改 PnL」集成轮已达成全闸通过，最新结论见 §15.3–15.5，首席件 `9qlwAbWd`。**

**推翻昨日 `REJECT_STRUCTURAL`，改为 `NEAR_MISS`（5/6 大闸 + 相关性双过，仅 LOW_FITNESS 差 0.01）。**

### 9.1 加腿实测（补齐第 4 交易所 EDGA，`shrt43_edgashvol_*`）

| 变体 | alpha | S | F | **2Y** | TO | R |
|---|---|---:|---:|---:|---:|---:|
| edgx − (bats+byxx+**edga**) @ tvr .10 | wpoRwGz5 | 1.74 | 0.98 | **0.77** | 12.03% | **3.95%** |
| 同上 @ tvr .105 | MP6plz89 | 1.74 | 0.98 | **0.74** | 12.52% | 3.96% |

⇒ **收益确实上去了（3.95% > 3.63%），但 2Y 从 1.80 崩到 0.77**——EDGA 口径在 2022–2023 是反向噪声。**加腿方向唯一能抬 R 的路被 2Y 一票否决**，本件到此收口。

## 11 最终最优件

| 项 | `ZYapkOWx`（最优） | `Jj8p0XpO`（tvr 微调） |
|---|---|---|
| 表达式 | `ts_target_tvr_decay(group_zscore(<两腿差分>, subindustry), target_tvr=0.1)` | 同上，`target_tvr=0.105` |
| 设置 | USA / TOP3000 / d1 / **decay 0** / **STATISTICAL** / trunc 0.08 | 同左 |
| S / F | **1.83 / 0.99** | 1.82 / 0.98 |
| 2Y / sub | 1.80 / 0.80 | 1.80 / 0.80 |
| TO / DD | 11.10% / 2.22% | 11.57% / 2.20% |
| Ra / 闸 | **仅 LOW_FITNESS FAIL**（其余 6 项全 PASS） | 仅 LOW_FITNESS FAIL |
| 塔 | USA/D1/SHORTINTEREST ×1.1，当季 3 已亮 ⇒ **塔边际 0** | 同左 |
| 算子 | **5 distinct / 8 次调用**（与原件逐位同算子集） | 同左 |
| 六维 | T1/T2 **不受影响**（distinct 算子与字段集合与原件相同：5 算子 / 6 字段） | 同左 |
| 相关性 | prod **0.6489** / self **0.1758**（**均已 PASS**） | 未复测（同骨架，预期同量级） |

**未提交**：按「只挖不提交」铁律，本轮零 POST。

### 硬性说明（不能不报的两点）
1. **F 的算术结论**：`F = S·√(R/max(TO,0.125))`，TO 11.1% 已在分母下限内，要过闸必须 `R ≥ 3.77%`（现 3.63%）或 `S ≥ 1.855`（现 1.83）。**单靠设置与算子变换够不到**——需要换信号强度（加腿/换经济机制），即第 9 节的未测骨架。
2. **年度稳健性**：`ZYapkOWx` 逐年 S = 4.50 / 1.95 / **0.27** / 0.49 / 3.59 / **0.89** / 1.67 / 1.58 / **0.73** / 2.77（2014/2018/2023 撑场，2016/2017/2019/2022 基本无 alpha）。**2Y 1.80 主要由 2023 年贡献**，这是该族「信息集中在少数年份」的固有形态，与原判死轮的诊断一致——只是这次**缺口从三闸压到一闸**。

## 12 truncation 专项（用户 00:45 质询：F 还有哪些旋钮、都回测了吗）

### 12.1 官方定义（`get_documentation_page("simulation-settings")` 原文）
> The maximum weight for each stock in the overall portfolio. When it is set to 0, there is no restriction.
> Legal values: Float x where 0 ≤ x ≤ 1（越界会破坏仿真）。推荐 0.05–0.1。

⇒ **truncation=0.8 与 0 等价于「不设上限」**；只有小于「实际最大单票权重」才会生效。

### 12.2 F 的三个自变量与敏感度（本件代入）

```
F = S · sqrt( |R| / max(TO, 0.125) )
当前：S 1.83 / R 3.63% / TO 11.10%（已在下限内）⇒ F = 1.83×0.539 = 0.986 → 显示 0.99
```
偏导（其余不变）：
- **∂F/∂R ≈ 13.6 / 单位 R** ⇒ **+0.1pp 收益率 = +0.0136 F**（最强杠杆）
- ∂F/∂S ≈ 0.54 / 单位 S ⇒ +0.1 S = +0.054 F（要 +0.1 S 极难）
- ∂F/∂TO = **0**（TO ≤ 12.5% 被 floor 吃掉）；一旦 TO > 12.5%，∂F/∂TO ≈ −3.7 ⇒ 每 +1pp TO 扣 0.037 F

⇒ **F 的瓶颈 100% 在 R**：过闸需 `R ≥ 3.77%`（现 3.63%，差 0.14pp）或 `S ≥ 1.856`（现 1.83）。按 +0.005 四舍五入纪律，目标应是 `R ≥ 3.80%`。

### 12.3 全部旋钮的测试覆盖表

| 旋钮 | 作用通道 | 状态 | 实测结论 |
|---|---|---|---|
| neutralization | S、R | ✅ 6 档 | STATISTICAL 唯一有效（+0.22 S） |
| 分组轴 | S | ✅ 4 档 | subindustry > industry > sector；去分组 1.67 |
| 截面变换 | S | ✅ rank/zscore | zscore（+0.22） |
| decay | S、R、TO | ✅ 0/1/4/8 | 0 最优（+0.03 F） |
| target_tvr | TO→R | ✅ 0.10/0.105/0.11/0.12 | ≤0.105 甜点；0.12 越 12.5% 即罚 |
| universe | S、R | ✅ 3000/1000/500 | TOP3000；越小越崩 |
| winsorize | S | ✅ std 2/4 | 净负（极值即信息） |
| 时序平滑 | S、2Y | ✅ ts_mean 63/66/69/126 | STATISTICAL 下冗余 |
| 加腿（EDGA） | R | ✅ | R 升到 3.95% 但 2Y 0.77 崩 |
| **truncation** | S、R、TO | 🔄 **本轮补测 0.02/0.04/0.12/0.8** | 见 12.4 |
| maxTrade / maxPosition | TO | ❌ 未测（OFF） | 仅当 TO > 12.5% 才有意义，本件 TO 11.1% |
| nanHandling | 覆盖/信号 | ❌ 未测（ON） | 可试 OFF（会掉覆盖、可能降 R） |
| pasteurization | 覆盖 | ❌ 未测（ON） | OFF 影响横截面覆盖，与 group_zscore 强相关，值得一测 |
| delay 0 | 全部 | ⛔ 不可行 | `getting-started-d0`：仅部分数据集有 D0 字段，shrt43 无 |
| test_period | — | n/a | 不影响 F 公式 |
| `ts_target_tvr_hump` 替代 decay | TO | ❌ 未测（止损否决） | 台账记载该旋钮在别族 −0.27 S，代价过高 |

### 12.4 truncation 实测结果（8 条，四档 × 两式）

| truncation | tvr 0.10（alpha） | tvr 0.105（alpha） | S / F / TO / R / DD |
|---|---|---|---|
| **0.08（原）** | ZYapkOWx | Jj8p0XpO | 1.83 / 0.99 / 11.10% / 3.63% / 2.22%<br>1.82 / 0.98 / 11.57% / 3.62% / 2.20% |
| **0.02** | 58Jw3aZX | leaVkQeO | **逐位相同** |
| **0.04** | O0WpqZGg | VkNpqPGA | **逐位相同** |
| **0.12** | xAvx9Mdw | KPgbqeEE | **逐位相同** |
| **0.8** | omaKAQlv | 1YW716dz | **逐位相同** |

**结论：truncation 是本件的死旋钮（0 影响）。**
- 机理：3126 只持仓（long 1586 / short 1540）、book 20M ⇒ 平均单票权重 **0.032%**，即使 0.02 的上限也差 60 倍摸不到；CW 检查本身也 PASS（说明平台认定无集中）。
- 一般规律：**truncation 只在「单票权重能接近上限」的alpha上才是杠杆**（持仓少 / 高集中 / 高 `tail` 切分）。本件属「宽持仓等权型」，调它等于没调。
- 官方推荐区间 0.05–0.1 是**防御性上限**（防黑天鹅单票），不是收益旋钮。

### 12.5 零成本设置项补充测试（pasteurization / nanHandling）

| 变体 | alpha | S | F | 2Y | TO | R | 判读 |
|---|---|---:|---:|---:|---:|---:|---|
| `pasteurization=OFF` · tvr .10 | P05pqRVK | 1.76 | 0.94 | **2.25** | 8.98% | 3.58% | 2Y 升、margin 0.000796↑，但 **S −0.07、F −0.05 ⇒ 对 F 净负** |
| `pasteurization=OFF` · tvr .105 | YPapnVeR | 1.76 | 0.94 | 2.22 | 9.35% | 3.58% | 同上 |
| **`nanHandling=OFF`** · tvr .10 | mLa8AR05 | 1.83 | 0.99 | 1.80 | 11.10% | 3.63% | **逐位相同**（本件实际无 NaN 被填充 ⇒ 死旋钮） |
| `nanHandling=OFF` · tvr .105 | xAvxQ82l | 1.82 | 0.98 | 1.80 | 11.57% | 3.62% | 逐位相同 |

### 12.6 设置层旋钮穷尽结论

F 的三个自变量（S、R、TO）与全部可操作旋钮的对应关系：

| 旋钮 | 是否测过 | 对 F 的影响 |
|---|---|---|
| neutralization / 分组轴 / 截面变换 / decay / target_tvr / universe / winsorize / 时序平滑 | ✅ 全部 | 已定位最优组合 |
| truncation（0.02/0.04/0.08/0.12/0.8） | ✅ 全部 | **死旋钮**（单票权重远低于上限） |
| pasteurization ON/OFF | ✅ 全部 | OFF 对 F 净负 |
| nanHandling ON/OFF | ✅ 全部 | **死旋钮**（无 NaN 可填充） |
| maxTrade / maxPosition | ✅ 判定性否 | 只压 TO；本件 TO 11.1% 已在分母下限内，压它只会掉 R ⇒ 必然降 F |
| delay 0 | ⛔ 不可行 | shrt43 无 D0 字段 |

⇒ **设置层旋钮已穷尽，F 的瓶颈 100% 在 R（收益率）**，只能通过**信号强度**（加腿 / 换经济机制 / 换字段）解决。数值上需把 R 从 3.63% 抬到 **3.80%**（+0.17pp，边际效应 +0.023 F），或把 S 从 1.83 抬到 1.856。



## 13 `group_cartesian_product` 实测（用户 01:12 点名，此前未测）

测试环境：`STATISTICAL / TOP3000 / d1 / decay 0 / trunc 0.08`，与最优件同基线；均加 `densify(...)` 包裹（`neut-users` 文档的 USA 范式）。

| # | 组合 | alpha | S | F | 2Y | TO | R | sub | Ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **对照组** | `subindustry × sector`（**嵌套**） | **2r57R6gN** | **1.83** | **0.99** | **1.80** | 11.10% | 3.63% | 0.80 | 1 |
| 非嵌套 | `subindustry × exchange` | mLa8A7G6 | 1.68 | 0.85 | 1.25 | 10.94% | 3.23% | 0.71 | **3** |
| 非嵌套 | `industry × exchange` | O0WpkzLg | 1.73 | 0.90 | **1.18** | 11.18% | 3.41% | 0.89 | **2** |
| 自造 | `subindustry × bucket(rank(cap),10)` | gJa1KG2J | **1.20** | 0.53 | 1.01 | 10.73% | 2.48% | 0.62 | **3** |

### 判读

1. **嵌套轴是死参数，本件第 3 次实测复现**：`group_cartesian_product(subindustry, sector)` 与基线 `ZYapkOWx` **指标逐位相同**（S 1.83 / F 0.99 / TO 11.10% / R 3.63% / DD 2.22%）。机理：sector ⊃ industry ⊃ subindustry，笛卡尔积的每个 (subindustry, sector) 组合仍唯一落在单个 subindustry 内，`densify` 只是重编号、不改变分组归属。本地模板库 `shortinterest3_template_library.md` §4 的「与单 `exchange` PnL 逐位相同」是同一现象。
2. **非嵌套二维分组一律变差**：`subindustry × exchange` S −0.15、2Y −0.55、sub −0.09（三闸）；`industry × exchange` 2Y 从 1.80 掉到 1.18。二维分组把组数放大数倍，组内样本变稀 ⇒ `group_zscore` 的截面标准化失稳。与 playbook「过细会崩」一致。
3. **自造 `bucket(rank(cap))` 最惨**：S 1.20 / F 0.53 —— cap 分位与借券流量结构无关，纯粹是噪声切分。
4. **算子成本**：`densify` + `group_cartesian_product` 使 distinct 算子从 5 → **7**（T1 软成本上升），且收益为零 ⇒ 双重否决。

⇒ **`group_cartesian_product` 对本件无价值，且已穷尽：嵌套退化为死参数、非嵌套崩盘、自造轴纯噪声。** 唯一可能有效的非嵌套组合是 `subindustry × 统计聚类字段`（如 `sta1_top1000c50`），但 `get_datafields("USA/TOP3000/D1", GROUP)` 实测**该账号该宇宙无 `sta1_*` 字段**（可用结构类分组只有 `country/exchange/industry/market/sector/subindustry` 及模型聚类字段）——文档给的 USA 范式在此账号不可落地。

## 15 「改 PnL」与「稳健性归因」可行性（用户 01:44 提问）

### 15.1 族内 PnL 相关性：只有一条腿能提供时间维分散

`compute_mutual_correlation`（10 年 / 2493 点 / 本地计算，不占相关性槽）：

| | ZYapkOWx（最优） | P05pqRVK（pasteurization OFF） | vRALapYw（industry 轴） | Jj8p0XpO（tvr .105） | WjlpKodP（**sm66×industry**） |
|---|---:|---:|---:|---:|---:|
| ZYapkOWx | 1.000 | 0.929 | 0.928 | **0.9996** | **0.804** |
| P05pqRVK | | 1.000 | 0.882 | 0.925 | 0.823 |
| vRALapYw | | | 1.000 | 0.928 | 0.853 |
| WjlpKodP | | | | 1.000 | 1.000 |

**判读**：族内所有变体的 PnL 相关 **0.80–0.9996**——`tvr` 微调（0.9996）、换轴（0.93）、开关 pasteurization（0.93）全是同一股 PnL。**唯一有实质差异的是「时间尺度」维度**：`ts_mean66` 版 ρ=0.804，因为它在时间上响应更慢。⇒ **「改 PnL」在本族只剩一条路：快慢两个时间视角做集成，靠时间维分散降波动。**

### 15.2 集成能否把 F 推过 1.0（组合算术，先算后测）

两流等权组合：`S_b = (S₁+S₂)/√(2+2ρ)`，ρ=0.804、S₁=1.83、S₂=1.71 ⇒ **S_b ≈ 1.86**；R_b=(3.63+3.81)/2≈3.72%；TO_b≈10.4%（仍 <12.5% 下限）
⇒ **F_b = 1.86×√(0.0372/0.125) ≈ 1.01**（临界通过）

已派 3 条实测（§15.3），因表达式层面无法精确复现 50/50 权重，需实测确认。

### 15.3 集成实测 —— **破局成功**

| 变体 | alpha | S | **F** | 2Y | sub | TO | R | DD | **Ra** |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **zscore 级集成**：`group_zscore(S,subind) + group_zscore(ts_mean(S,66),industry)` | A1xwOYvl | **1.88** | **1.05** | 1.69 | **0.91** | 11.34% | 3.93% | 2.37% | **0** |
| **信号级平滑**：`group_zscore(S + ts_mean(S,66), subind)` | **9qlwAbWd** | **1.88** | **1.04** | **1.85** | 0.82 | 11.14% | 3.80% | 2.20% | **0** |
| 短窗版（ts_mean 22） | gJa1owZl | 1.62 | 0.81 | 1.76 | 0.74 | 11.01% | 3.12% | 2.70% | 1 |

**算术验证**：组合公式预测 S_b≈1.86 / F≈1.01，实测 **1.88 / 1.04** —— 预测与实测同向且略优（真实相关结构比估算更好）。

### 15.4 首席件 `9qlwAbWd` 全维快照

```
ts_target_tvr_decay(group_zscore(add(<两腿差分>, ts_mean(<两腿差分>, 66)), subindustry), target_tvr=0.1)
USA / TOP3000 / d1 / decay 0 / STATISTICAL / trunc 0.08 ｜ 6 distinct 算子
```
| 项 | 值 | 判定 |
|---|---|---|
| S / F | **1.88 / 1.04** | PASS（F 余量 +0.04） |
| 2Y | **1.85** | PASS（余量 +0.27） |
| sub-universe | 0.82 | PASS |
| TO / R / DD / margin | 11.14% / 3.80% / 2.20% / **6.81 bp** | 全部 PASS |
| 八项 RA 检查 | `fail: []`（LOW_SHARPE/LOW_FITNESS/LOW_TURNOVER/HIGH_TURNOVER/CW/LOW_SUB/LOW_2Y/MATCHES_PYRAMID） | **failed_ra_count = 0** |
| prod correlation | **0.6300** | PASS（余量 0.070） |
| self correlation | **0.1716**（pool 142，top `9WkpwQq` 0.172） | PASS（余量 0.53） |
| 塔 | USA/D1/SHORTINTEREST ×1.1，当季 3 已亮 | **塔边际 0** |
| 六维 | 6 distinct 算子（+`ts_mean`）/ 6 字段 | T1 +1 软成本，T2 不变 |

**经济解释（一句话）**：EDGX 场所的空头成交占比相对 BATS/BYX 的偏离，度量空头在单一场所的集中度；把该偏离与自身 66 日均值相加，等于要求"当前偏离必须与中期偏离同向"才给满仓——过滤掉单日噪声造成的假挤压。

### 15.5 稳健性归因预审（`9qlwAbWd`，按 `brain-alpha-robustness` Phase C）

**制度要点**：年度项**只算最近 3 个 IS 年**，全历史早年疲软**只记软标记、绝不据此 REJECT**（用户 2026-06-20 指令）。

逐年 S = 5.07 / 1.93 / 0.43 / 0.36 / 3.76 / 0.80 / 1.86 / **1.40 / 0.94 / 2.66**

| 检查项 | 数值 | 判定 |
|---|---|---|
| Recent-3yr Sharpe（主判定） | 2Y **1.85 ≥ 1.58**，近 3 年均 >0.3 | **PASS** |
| Recent-3yr CV_Sharpe（总体 sd） | mean 1.667、sd 0.727 ⇒ **0.436** | 0.40–0.60 带 ⇒ 软标记 |
| 衰减比 | 2.66 / 1.88 = **1.41** | PASS |
| 平年（近 3 年） | 0 | PASS |
| Recent-3yr max/min | 2.66 / 0.94 = **2.83** | **≤3 ⇒ PASS** |
| sub-universe | 平台 PASS（0.82） | PASS |
| 算子数 | 6 | >5 ⇒ 软标记（软，非 REJECT） |
| Margin | 6.81 bp @ 11.1% TVR | PASS |
| 经济可解释性 | 见上（一句话） | PASS |

⇒ **预期：无硬 REJECT，判定 PASS（2 项软标记：CV 0.436、ops 6）。** 注意 `max/min 2.83` 比前一版（3.79）明显改善——集成同时把"极端年依赖"压下来了。


### 15.6 对照：旧最优件 `ZYapkOWx` 的稳健性预审（供比较）

最近 3 年：**2021 S 1.58｜2022 S 0.73｜2023 S 2.77**

| 检查项 | 数值 | 判定 |
|---|---|---|
| Recent-3yr Sharpe（主判定） | 2Y **1.80 ≥ 1.58**，每年 >0.3 | **PASS** |
| Recent-3yr CV_Sharpe（总体 sd） | **0.494** | 0.40–0.60 带 ⇒ 软标记 |
| 衰减比 | 2.77 / 1.83 = **1.51** | PASS |
| Recent-3yr max/min | 2.77 / 0.73 = **3.79** | 3–5 带 ⇒ 软标记 |
| 算子数 | 5 | PASS |

⇒ 两件都能过稳健性主判定；但集成的 `9qlwAbWd` 在 **max/min（2.83 vs 3.79）** 与 **F 余量（+0.04）** 上更优，故取集成件。

**由此回答"死年要不要修"：制度上不构成 REJECT 理由（近窗制），经济上是软标记；集成恰好顺带把 extreme-year 依赖压低了，属于附带收益而非主目标。**




## 16 本轮与原判死轮的结论关系

| 维度 | 原判死轮（11-17） | 本轮（11-18） |
|---|---|---|
| 工作假设 | 骨架内调参（窗/轴/decay/tvr/级联） | **换设置轴 + 换截面变换** |
| 扫描轴 | 窗口、tvr、轴（sector/market）、decay、级联 | 中性化（6 档）、`group_zscore` vs `group_rank`、universe（TOP1000/500）、winsorize、分组维度、tvr 精调 |
| 关键发现 | S 天花板 1.53（24 条） | 中性化轴未扫过；**STATISTICAL 单独 +0.22 S**；**`group_zscore` 再 +0.22 S** ⇒ 天花板其实是 1.83，且 self 墙被拆掉 |
| 结果 | REJECT_STRUCTURAL（3 闸） | **NEAR_MISS（1 闸，差 0.01）** |
| 教训 | 判死前必须先做杠杆扫描与消融扫描（skill ⑥ 前置条件） | 论坛/文档口径需区分**是否适用于本数据集**（Industry 推荐、小 universe 两条都不适用）；`search_forum_posts` 空返回不得当作「无讨论」

## 8 论坛口径 → 本件落地的对照表（哪条成立、哪条不成立）

| 论坛/文档口径 | 本件实测 | 结论 |
|---|---|---|
| `neut-cons`：Short Interest → **Industry** 中性化推荐 | INDUSTRY 1.25 / CROWDING 1.51 / **STATISTICAL 1.80** | ❌ 不成立（该推荐对 shortinterest3 费率族成立，对 shrt43 日频流量比不成立） |
| BRAIN TIPS：**更小 universe** 增收益 | TOP3000 1.80 → TOP1000 1.02 → TOP500 0.67 | ❌ 反向，覆盖广度是载体 |
| BRAIN TIPS：**提高换手**增收益 | tvr 0.10→0.12：TO 13.0%、R 不涨、F 反降 | ❌ 越过 12.5% 分母下限即罚 |
| BRAIN TIPS：**降低 decay** | decay 1→0：S +0.03、F +0.03 | ✅ 成立（本件在 STATISTICAL 下无平滑价值） |
| 模板库：`group_rank` **丢幅度**，`group_zscore` 胜出 | rank 1.58 vs zscore **1.80** | ✅ 第 4 次复现，本件最大单点增益 |
| 模板库：`sector` 轴过粗 | sector 1.28（zscore 下）vs subindustry 1.80 | ✅ 成立 |
| 模板库：winsorize 只对连续厚尾有效 | std=4 逐位同值（无操作）、std=2 +0.03 S | ✅ 成立（参数要够紧才生效） |
| `neut-users` 双重中性化（cartesian product） | ✅ **01:12 已测**（见 §14） | 嵌套轴退化为单轴；非嵌套 `exchange` / 自造 `bucket(rank(cap))` 两维分组 |

## 9 后续可挖（已定位，仍未测）

`get_datafields("shortinterest43")` 显示该数据集有 **4 个交易所口径**（EDGA / EDGX / BATS / BYX）× {`shvol_svol`, `shvol_totalvolume`}，本件只用了「EDGX 份额 −（BATS+BYX）份额」。两条现成的新骨架：
1. **四口竞技场离散度**：`vec_*` 不可用（MATRIX），改用 4 个比值手工求极差/标准差 ⇒ 「哪个交易所的空头异常集中」。
2. **short-exempt 蓝海**：2026-03-01 新上 `total_short_exempted_shares`(alphaCount 2) / `count_shares_short_exempted`(4) / `quantity_sold_short_exempted`(6) / `volume_short_exempted_trades`(2)，覆盖率 1.0 —— 豁免做空量（做市商豁免口径），与常规 short volume 经济含义不同，拥挤度极低。

---

# 17 `9qlwAbWd` 参数精调（用户 01:56「拿到后别忘记精调参数使得指标绩效最优」）

## 17.0 先穷举「哪些是真旋钮」

`get_operators` 取回算子定义：`ts_target_tvr_decay(x, lambda_min=0, lambda_max=1, target_tvr=0.1)`。因此本件的可调参数一共 **5 类 8 项**，逐项都测：

| # | 旋钮 | 取值 | 状态 |
|---|---|---|---|
| 1 | `ts_mean` 窗口 | 44 / 55 / 66(原) / 77 / 88 / 110 / 132 / 154 / 200 | 已测（含延伸） |
| 2 | `target_tvr` | 0.09 / 0.095 / 0.1(原) / 0.105 / 0.11 | 已测 |
| 3 | `lambda_max` | 0.5（默认 1） | 已测 |
| 4 | `lambda_min` | 0.5（默认 0） | 已测 |
| 5 | 平滑算子替代 | `ts_decay_linear(A,66)` | 已测 |
| 6 | 目标算子替代 | `ts_target_tvr_hump` | 已测 |
| 7 | 平台 `decay` | 0(原) / 1 | 已测 |
| 8 | 分组轴 | subindustry(原) / industry / sector | 已测（§2、§4 单信号骨架；§17.5.1 在集成骨架复测） |

## 17.1 窗口扫描（唯一有效旋钮，单调向右）

全批同设置：`USA/TOP3000/d1/decay 0/STATISTICAL/trunc 0.08`，`target_tvr=0.1`。

| `ts_mean` 窗口 | alpha | S | **F** | 2Y | sub | TO | R | DD | Ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 44 | 3q07nNxz | 1.80 | 0.96 | 1.59 | 0.78 | 11.11% | 3.59% | 2.20% | 1 |
| 55 | 0mP7KJdr | 1.86 | 1.01 | 1.72 | 0.80 | 11.13% | 3.72% | 2.18% | 1 |
| **66（原 `9qlwAbWd`）** | 9qlwAbWd | 1.88 | 1.04 | 1.85 | 0.82 | 11.14% | 3.80% | 2.20% | 0 |
| 77 | N1Pp5Z6L | 1.90 | 1.05 | 1.94 | 0.84 | 11.16% | 3.84% | 2.21% | 0 |
| 88 | npagOEol | 1.90 | 1.05 | 1.99 | 0.83 | 11.17% | 3.85% | 2.27% | 0 |
| **110** | **YPapWe1M** | **1.90** | **1.06** | **2.10** | 0.82 | 11.20% | 3.86% | 2.40% | **0** |
| 132 | zqd9PMjd | 1.89 | 1.05 | 2.12 | 0.83 | 11.22% | 3.87% | 2.45% | 0 |
| 154 | O0WpbYkd | 1.88 | 1.04 | **2.14** | 0.83 | 11.24% | 3.86% | 2.41% | 0 |
| 200 | E5Qwg7a1 | 1.88 | 1.05 | 2.13 | 0.84 | 11.26% | 3.90% | **2.59%** | 0 |

**读法**：44→110 单调改善、**在 110 处见顶**——S 1.80→1.90、F 0.96→1.06、**2Y 1.59→2.10**、R 3.59%→3.86%，而 TO 只从 11.11% 微升到 11.26%（因为 `ts_target_tvr_decay` 会把总换手拉回目标值，窗口加长不等于换手上升）。110 之后 F 回落到 1.04–1.05，DD 单调恶化（2.40→2.59%）。⇒ **窗口最优 = 110，F 余量 0.06（原 66 只有 0.04）**。

## 17.2 其余旋钮：全部死旋钮或负向

| 旋钮 | alpha | S | F | 2Y | TO | 结论 |
|---|---|---:|---:|---:|---:|---|
| `target_tvr=0.09` | A1xwgRae | 1.88 | 1.04 | 1.84 | 10.19% | 与基线**逐位同 S/F** |
| `target_tvr=0.095` | xAvxPKzp | 1.88 | 1.04 | 1.85 | 10.66% | 同上 |
| `target_tvr=0.105` | QP0a21lw | 1.88 | 1.04 | 1.85 | 11.63% | 同上 |
| `target_tvr=0.11` | d5axE2lX | 1.88 | 1.04 | 1.85 | 12.11% | 同上（TO 仍 <12.5%） |
| `lambda_max=0.5` | LLKplQKn | 1.88 | 1.04 | 1.85 | 11.14% | **无操作**（与基线完全相同） |
| `lambda_max=0.2` | 9qlwaLlr | 1.88 | 1.04 | 1.85 | 11.14% | **无操作**（同上）⇒ 优化器自选 λ 本就 <0.2 |
| **`lambda_min=0.5`** | omaK3Mav | 1.87 | **0.47** | 1.68 | **57.49%** | **灾难性负向**：目标换手无法在 [0.5,1] 内命中，TO 爆 5 倍 |
| `ts_decay_linear(A,66)` 替 `ts_mean` | akadWpK9 | 1.77 | 0.94 | 1.67 | 11.11% | **负向 −0.10 F** |
| `ts_target_tvr_hump` 替 decay | RRepkgen | 1.58 | 0.77 | 1.80 | **12.80%** | **负向 −0.27 F**，TO 越 12.5% 罚 F |
| 平台 `decay=1` @窗口66 | YPap2rY6 | 1.87 | 1.03 | 1.85 | 11.14% | 略差（−0.01） |
| 平台 `decay=1` @窗口77 | npagZJrw | 1.88 | 1.04 | 1.94 | 11.16% | 略差（−0.02 S） |

**机理**：`target_tvr` 与 `lambda_max` 只改「用多少平滑去命中换手目标」，命中目标后组合权重几乎不变 ⇒ S/R 不动；本件 TO 本来就在 12.5% 分母下限内，改它也不进 F 的分子分母。`lambda_min` 才是真正的 λ 下限——λ 在 `ts_decay` 里是「当期值权重」，把下限抬到 0.5 等于禁止平滑，换手爆掉。`hump` 是限幅式控换手（不改信号值），在本件上直接把 TO 顶到 12.80%，越过 12.5% 即被 F 惩罚。

## 17.3 塔读数更正（重要，此前报错了）

用户在 01:56 之后的本轮里，我用 `get_pyramid_alphas` 显式区间重查，结果与此前报告不一致，**必须更正**：

| 查询区间 | USA / D1 / shortinterest |
|---|---:|
| 2026-10-01 ~ 2026-12-31（本季） | **0** |
| 2026-07-01 ~ 2026-09-30（上季） | **0** |
| 2026-01-01 ~ 2026-12-31（全年） | **0** |

**官方口径（`get_documentation_page("brain-genius")` 原文）**：
> “A consultant is considered to have formulated a pyramid if they have submitted a minimum of 3 Alphas in it.”
> “WorldQuant defines a ‘pyramid’ as a combination of region, delay, and dataset category.”

⇒ **正确结论：本账号 USA-D1-SHORTINTEREST 本季计数是 0，不是 3。交这颗是「1/3 奠基」，塔边际为正**（此前写的「当季 3 已亮、塔边际 0」是错的，据此更正）。倍率 **1.1** 是该席位的鼓励档（`get_pyramid_multipliers` USA/D1/shortinterest = 1.1），与「是否已点亮」是两个不同概念。

附本季 USA/D1 各席位计数（同期取数，供对照）：model 4 ｜ analyst 6 ｜ other 4 ｜ risk 3 ｜ earnings 3 ｜ institutions 1 ｜ **shortinterest 0** ｜ pv/sentiment/news/option/macro/insiders/fundamental 0。

## 17.4 塔与六维（对最终候选，不写 n/a）

| 维度 | 值 |
|---|---|
| 席位 | `USA/D1/SHORTINTEREST` |
| 倍率（混塔短板） | **1.1**（单类别，无混塔） |
| 当季计数 | **0**（实测 2026Q4） |
| 交后 | **1** |
| 是否新点亮（≥3） | 否（1/3 奠基） |
| 塔边际 | **正：为 Genius 资格第 2 项（pyramid 数）贡献一颗** |
| 六维 T1（distinct ops） | **6**（`ts_target_tvr_decay`/`group_zscore`/`add`/`subtract`/`divide`/`ts_mean`），与原 `9qlwAbWd` **逐位相同** |
| 六维 T2（distinct fields） | **6**（`shrt43_edgxshvol_svol`/`shrt43_edgxshvol_totalvolume`/`shrt43_batsshvol_svol`/`shrt43_byxxshvol_svol`/`shrt43_batsshvol_totalvolume`/`shrt43_byxxshvol_totalvolume`），不变 |
| T3 新算子 / T4 新字段 | 无新增算子；**若 shrt43 六字段此前未进 OS 池，可 +6 字段** |
| 平台 `operatorCount` | 14 次调用（子式 `A` 在表达式中写了两遍）；REGULAR 无单条上限，不进六维 |

## 17.5 窗口细分 + 权重结构（第二批精调）

| 变体 | alpha | S | **F** | 2Y | sub | TO | R | DD | Ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 窗口 99 | KPgbXqLx | 1.90 | 1.05 | 2.05 | 0.83 | 11.19% | 3.85% | 2.31% | 0 |
| **窗口 121** | **Jj8pgYdn** | **1.90** | **1.06** | **2.12** | 0.83 | 11.21% | 3.88% | 2.41% | **0** |
| `ts_mean(A,10) + ts_mean(A,110)` | leaVQk0l | 1.71 | 0.89 | 2.04 | 0.75 | 11.14% | 3.42% | 3.18% | 1 |
| `ts_mean(A,44) + ts_mean(A,110)` | npagZYWd | 1.65 | 0.86 | 1.63 | 0.87 | 9.62% | 3.41% | 2.78% | 1 |

**关键结构结论**：把原始项 `A` 换成任何长度的平滑（10 日或 44 日）都会**大幅变差**（F 1.06 → 0.89 / 0.86）——说明**日频分量本身就是 alpha 的主体**，长窗平滑只应作为「同向确认」的加成项。当前结构 `A + ts_mean(A,长窗)`（原式权重 1:1）已接近最优，不需要改成纯双平滑。

**窗口平台期**：99 → 1.05、110 → 1.06、121 → 1.06、132 → 1.05、154 → 1.04、200 → 1.05。**110–121 是平台期顶点**，无需再细分。

### 17.5.1 分组轴在新骨架上复核（窗口 110，各 1 条）

| 分组轴 | alpha | S | F | 2Y | sub | TO | R | DD | Ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **subindustry（原）** | YPapWe1M | **1.90** | **1.06** | 2.10 | 0.82 | 11.20% | 3.86% | **2.40%** | 0 |
| industry | gJa1RmZM | 1.83 | 1.02 | **2.12** | 0.82 | 11.53% | 3.91% | 3.37% | 0 |
| sector | Jj8pgnQe | 1.68 | 0.92 | 1.81 | 0.80 | 11.90% | 3.75% | 3.81% | 1 |

⇒ **subindustry 在新骨架上仍是唯一最优**（S/F 双高、DD 最低）。此前 §2/§4 在单信号骨架上得到的「行业维不含信息」结论，在集成骨架上依然成立；`industry` 虽然 2Y 略高 0.02，但 S −0.07、DD +0.97pp、F −0.04，不值得权衡。

## 17.6 精调后的最终候选 `Jj8pgYdn`

```
ts_target_tvr_decay(group_zscore(add(<两腿差分>, ts_mean(<两腿差分>, 121)), subindustry), target_tvr=0.1)
USA / TOP3000 / d1 / decay 0 / STATISTICAL / trunc 0.08 ｜ 6 distinct 算子
```

| 项 | 精调前 `9qlwAbWd`（窗口 66） | **精调后 `Jj8pgYdn`（窗口 121）** | 变化 |
|---|---:|---:|---|
| Sharpe | 1.88 | **1.90** | +0.02 |
| **Fitness** | 1.04 | **1.06** | **+0.02（余量 0.04 → 0.06）** |
| 2Y Sharpe | 1.85 | **2.12** | **+0.27** |
| Returns | 3.80% | **3.88%** | +0.08pp |
| Turnover | 11.14% | 11.21% | +0.07pp（仍 <12.5%） |
| Drawdown | 2.20% | 2.41% | +0.21pp（代价） |
| sub-universe | 0.82 | 0.83 | +0.01 |
| margin | 6.81 bp | **6.92 bp** | +0.11 bp |
| 八项 RA | fail [] | **fail []（failed_ra_count 0）** | 不变 |
| **prod corr** | 0.6300 | **0.6339** | 仍 <0.7（余量 0.066） |
| **self corr** | 0.1716 | **0.1758** | 仍 <0.7（余量 0.524） |
| 六维 T1/T2 | 6 / 6 | **6 / 6** | 不变，零六维代价 |

**逐年 S（`Jj8pgYdn`）**：5.23 / 1.68 / **0.10** / **0.47** / 3.78 / 1.26 / 1.74 / **1.07** / **1.31** / 2.81

| 稳健性预审（Phase C 口径） | 数值 | 判定 |
|---|---|---|
| Recent-3yr Sharpe | 2Y **2.12 ≥ 1.58**，近三年逐年 1.07 / 1.31 / 2.81 均 >0.3 | **PASS** |
| CV_Sharpe（总体 sd） | mean 1.730、sd 0.770 ⇒ **0.445** | 0.40–0.60 带 ⇒ 软标记 |
| 衰减比（末年/全期） | 2.81 / 1.90 = **1.48** | PASS |
| max/min（近三年） | 2.81 / 1.07 = **2.63** | **≤3 ⇒ PASS**（w66 为 2.83） |
| 算子数 | 6 distinct（>5 即软标记） | 软标记 |
| margin @ TVR | **6.92 bp** @ 11.21% | PASS |

⇒ **预期判定 PASS（2 项软标记：CV 0.445、ops 6）**，优于窗口 66 版（CV 0.436 但 max/min 2.83）。

## 17.7 精调总账（25 条，全部实测）

| # | 批次 | 内容 | 条数 | 结论 |
|---|---|---|---:|---|
| 1 | 窗口 44/55/77/88 | `ts_mean` 窗口 | 4 | 单调上升 |
| 2 | 窗口 110 + 算子替代 + λ_max | 4 | **110 见顶**；`ts_decay_linear`、`hump` 负向；λ_max 无操作 |
| 3 | 平台 decay=1 @66/@77 | 2 | 略差 |
| 4 | `target_tvr` 0.09/0.095/0.105/0.11 | 4 | 死旋钮 |
| 5 | 窗口 132/154/200 | 3 | 过顶回落 |
| 6 | `lambda_min=0.5` / `lambda_max=0.2` | 2 | 灾难负向 / 无操作 |
| 7 | 轴 industry/sector @110 | 2 | 均不如 subindustry |
| 8 | 窗口 99/121 + 双平滑替代 | 4 | **121 最优**；平滑替代原始项负向 |

**最终选择 `Jj8pgYdn`**（窗口 121）。**精调净收益**：F 1.04 → **1.06**（余量翻 1.5 倍）、2Y 1.85 → **2.12**、S 1.88 → **1.90**、margin 6.81 → 6.92 bp；代价仅 DD 2.20% → 2.41%。**六维零代价**（distinct 算子 6、字段 6 均不变）。

**仍未测（留作后续）**：`ts_target_tvr_decay` 的 `lambda_min`∈(0,0.3) 细档（当前 λ_min=0.5 已证明方向为负，细档价值低）；`bucket`/`trade_when` 类结构性改写（会增 distinct 算子，且本件已全闸通过，不动）；`short_exempted` 四字段与四交易所离散度（属新骨架，不属本件精调范围）。

---

# 18 算子调用点压缩（用户 02:07「算子数调用有调整优化吗，抽取共性、减少调用点优化过吗」）

## 18.1 审计：`Jj8pgYdn` 的 14 次调用在哪

`op_count.py --alpha-id Jj8pgYdn`（该脚本与平台 `regular.operatorCount` **逐位一致**，见 `output_report/alpha_opt_zqbVMkv1_20261012.md` §验证）：

| 算子 | 调用次数 | 来源 |
|---|---:|---|
| `add` | **5** | 分母 `bats+byxx`（svol）、`bats+byxx`（total）、双尺度融合 1 —— **其中 2 次是重复子式** |
| `divide` | **4** | 三个比率 + **1 次重复** |
| `subtract` | **2** | 两腿差分 + **1 次重复** |
| `ts_target_tvr_decay` / `group_zscore` / `ts_mean` | 1 / 1 / 1 | 各一次 |
| **合计** | **14** | distinct 仅 **6** |

根因：子式 `A`（两腿差分）在表达式里**写了两遍**（一次给原式、一次喂 `ts_mean`），5 个算子 × 2 = 10 次调用。`compress.py --lossless-only` 对该式返回 **variants = []**（无代数改写空间），所以只能靠**变量抽取**。

## 18.2 共性抽取实测：`Jj8pgxJm`（无损，−5 次调用）

```
a = subtract(divide(shrt43_edgxshvol_svol, shrt43_edgxshvol_totalvolume),
             divide(add(shrt43_batsshvol_svol, shrt43_byxxshvol_svol),
                    add(shrt43_batsshvol_totalvolume, shrt43_byxxshvol_totalvolume)));
ts_target_tvr_decay(group_zscore(add(a, ts_mean(a, 121)), subindustry), target_tvr=0.1)
```

| 项 | `Jj8pgYdn`（原，A 写两遍） | **`Jj8pgxJm`（变量抽取）** |
|---|---:|---:|
| 调用次数（`operatorCount`） | **14** | **9（−36%）** |
| distinct 算子 | 6 | **6（不变）** |
| Sharpe / Fitness | 1.90 / 1.06 | **1.90 / 1.06（逐位相同）** |
| 2Y / sub / TO / R / DD | 2.12 / 0.83 / 11.21% / 3.88% / 2.41% | **逐位相同** |
| margin | 6.92 bp | **6.92 bp** |
| 八项 RA | fail [] | **fail []** |
| prod / self | 0.6339 / 0.1758 | **0.6339 / 0.1758（完全相同）** |

**判定：多语句（`a = ...;`）语法被平台接受，且变量赋值不计入 operatorCount ⇒ 纯赚，无任何指标损失。** 历史报告（`alpha_opt_zqbVMkv1_20261012.md`）把**调用点 ≥10 视为复杂度闸线**，本件由 14 降到 9，已落到线下。

## 18.3 拆限速器（唯一能再降 distinct 的路）——实测不可行

去掉 `ts_target_tvr_decay` 可把 distinct 压到 5、调用压到 13（配变量可到 8），实测：

| 变体 | alpha | S | F | 2Y | **TO** | R | margin | Ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 拆掉限速器（decay 0） | npagZK58 | 1.88 | **0.32** | 1.69 | **117.58%** | 3.39% | 0.58 bp | **2** |

**原始信号换手 117.58%**（`ts_target_tvr_decay` 把它压到 11.21%），margin 只剩 0.58bp ⇒ **限速器是信号本体的一部分，不能当“冗余算子”删**。这条也解释了为什么本族所有变体都必须挂它。

## 18.4 还能压到多低：已到结构下限

| 路径 | 调用 | distinct | 可行性 |
|---|---:|---:|---|
| 原式（A 写两遍） | 14 | 6 | — |
| **变量抽取（采用）** | **9** | **6** | ✅ 无损 |
| 再拆限速器 | 8 | 5 | ❌ TO 117.58% |
| 去掉 `ts_mean`（退回单尺度） | 8 | 5 | ❌ F 1.06 → 0.99（§15 已测 `ZYapkOWx`） |
| 去掉 `group_zscore`（换 `zscore`） | 9 | 5 | ❌ S 1.67（§7 K 批已测） |
| 砍掉 BYX 腿（省 `add`×2、4 个字段） | 7 | 6 | ⚠ 未测且**不建议**：T4（总字段数，权重更高）会 −2，得不偿失 |

⇒ **9 次调用 / 6 distinct 是本信号结构的真正下限**；6 个算子逐一都是承重的（限速器、分组轴、双尺度平滑、两腿差分的 `divide/subtract/add`）。

## 18.5 最终首席件更新

**`Jj8pgxJm`** 取代 `Jj8pgYdn` 成为首席件（同 PnL、同指标、低 5 次调用）。塔与六维与 §17.4 完全一致：`USA/D1/SHORTINTEREST` ｜倍率 1.1 ｜当季 **0** ｜交后 **1** ｜**未点亮（1/3 奠基，塔边际为正）**；T1 **6** / T2 **6** / T3 无新增 / T4 若 shrt43 六字段未入池可 **+6**。


---

# 19 提交记录（用户 02:11 点名「提交 Jj8pgxJm」）

## 19.1 提交结果
| 项 | 值 |
|---|---|
| alpha | `Jj8pgxJm` → **ACTIVE** |
| name / color | `USA_R_shrtsvol_01` / `BLUE` |
| tags | `CH_REG` / `SRC_shortinterest43`（未预置 `PowerPoolSelected`） |
| 提交时刻 | 2026-11-18 02:14:02 +08:00（ET 2026-11-17 13:14） |
| **平台 `regular.operatorCount`** | **9**（压缩前 14）—— 与 `op_count.py` 静态计数**逐位一致**，变量抽取生效 |
| 配额 | ET 2026-11-17 REGULAR **0/4 → 1/4**（剩余 3） |
| 分类 | `DATA_USAGE:SINGLE_DATA_SET`（ATOM 单数据集路径） |

## 19.2 提交前闸位（全部实测）
| 闸 | 结果 |
|---|---|
| `submit_gate` | passed，blocked=false，failed_ra 0 / failed_ppa 0 |
| `mix_audit` | two_leg（2 腿），三问 `narrative_ok = true` |
| `quota_gate` | ET 今日 0/4 → 剩余 4 |
| `prod_gate` | **0.6339 < 0.7**（缓存 @02:10:05，`from_cache=true`），`prod_snapshot` 与冻结值一致（delta 0.0） |
| `marginal_contribution` | 方案 D v2 **neutral**（死区：ΔS 0.00 / ΔF −0.01 / ΔRet −0.06pp），`hard_blocked=false` |
| `diversity_audit` | 平台未回填 selfCorrelation ⇒ 不可判，fail-open（另跑 `check_correlation` 得 self 0.1758） |
| `robustness` | 台账已有记录，**CONDITIONAL**（无 REJECT，不阻断） |
| `verify` | **ACTIVE** |

## 19.3 IS 检查明细（提交后平台回读）
| 检查 | 结果 | 读数 / 线 |
|---|---|---|
| LOW_SHARPE | PASS | 1.90 / 1.58 |
| LOW_FITNESS | PASS | 1.06 / 1.00 |
| LOW_TURNOVER / HIGH_TURNOVER | PASS / PASS | 11.21% / 1%–70% |
| CONCENTRATED_WEIGHT | PASS | — |
| LOW_SUB_UNIVERSE_SHARPE | **PASS（余量仅 +0.01）** | 0.83 / 0.82 |
| LOW_2Y_SHARPE | PASS | 2.12 / 1.58 |
| MATCHES_PYRAMID | PASS | `USA/D1/SHORTINTEREST` ×1.1 |
| CLUSTER_TEST | WARNING | −0.06 / 1.58 |
| MATCHES_COMPETITION | WARNING | AQP202611 |
| MATCHES_THEMES | WARNING | GLB/D1 Power Pool Nov'26（×1.0）｜USA/D1 turnover 15–30% Theme（×2.0） |

## 19.4 塔与六维（提交后）
| 维度 | 值 |
|---|---|
| 席位 | `USA/D1/SHORTINTEREST` |
| 倍率 | **1.1** |
| 当季计数（提交后即读） | **0**（平台计数有缓存/延迟，按规则应交后 = **1**）⇒ **下轮核塔必须重查** |
| 是否点亮（≥3） | 否（1/3 奠基） |
| 塔边际 | **正**：为 Genius 资格第 2 项（pyramid 数）计入 1 颗 |
| T1 / T2 | **6 distinct 算子 / 6 字段**（与压缩前完全一致） |
| T3 / T4 | 无新增算子；若 shrt43 六字段此前未入 OS 池，可 +6 字段 |
| 平台 operatorCount | **9 次调用** |

## 19.5 需盯的风险（如实记录）
1. **`LOW_SUB_UNIVERSE_SHARPE` 余量只有 +0.01**（0.83 vs 线 0.82）——OS 阶段亚宇宙表现若下滑即会破线。
2. **近三年 CV_Sharpe 0.445** 落 CONDITIONAL 带（诚如有软标记，非硬 REJECT）。
3. **早年疲软**：2016 S 0.10、2017 S 0.47、2019 S 1.26（近窗制下仅记录）。
4. **CLUSTER_TEST WARNING −0.06**（平台聚类测试，非提交闸）。
5. 塔计数读数滞后，需下轮复核是否为 1。
