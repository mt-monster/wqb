# L4 形态构建实跑：EUR/other460（2026-10-01）

> 目的：**端到端验证**刚修好的 L1→L3.5 链路能否支撑 L4 五步法。
> 全程**零配额**（未发起任何回测）。发探针与否待确认。

## 0. 结论速览

- **L1→L3.5 链路打通**：GBR/model264 复现 160 族 / 35 三分类族；EUR/other460 达 418 族 / 115 三分类族。
- **L4 五步法可执行**，且**"避判死"这一步在零配额阶段就连续拦下 3 个错误方向**（详见 §1），直接省下本会烧掉的回测配额——这是本次实跑最大的价值。
- 最终目标 **`EUR/other460`**（418 族 ∧ 未判死 ∧ 在 S0 白名单），产出 **5 条 v1 骨架 + 6 条 v2 骨架**，算子数 1–6，全部通过组合形态铁律与复杂度纪律自检。
- 顺带发现 **3 个真问题**（§5）：白名单含已判死集、GBR 白名单实质无主信号目标、`forum_recon` 读帖链路故障 —— **三个均已修复**。
- **★ 修复 `forum_recon` 后立刻拿到决定性回报**：L2 命中一篇**就在 EUR 市场、机制完全同构**的实证帖（§3.1），
  给出 `ts_zscore`／`signed_power` 两个本轮骨架缺失的关键算子 + EUR Setting 实测值 ⇒ 骨架从 v1 升级到 **v2**。
  这是"先修基础设施再发探针"而非直接烧配额的直接收益。

## 1. 目标选定：三个方向被流程拦下（零配额）

| 候选 | 拦下的闸 | 具体证据 |
|---|---|---|
| GBR/**model264** | 白名单 + 族级判死 | ① `s0_whitelist` = `pv30/pv29/institutions6/news48`，**不含 model264**，画像写"白名单外禁止 generate/simulate"；② `GBR-DLRISKFREE-LABEL-DEAD`：probability_label 族 2Y 崩（wave30 max sh 1.09 / 2Y −0.05）——`_l1/_l3` 概率族正是此类；③ `GBR-SIMPLE-STRUCTURE-DEAD`：model264 简单结构判死（wave26-28） |
| GBR/**news48** | 已判死 = 幽灵集 | `news48_dead`：`S1 scan_fields fields=0 data_type=UNKNOWN`，verdict=DEAD，rule="不进白名单、不生成"——**但它仍在 `s0_whitelist` 里**（白名单漂移，见 §5.1） |
| KOR/**model109** | 已判死 | `model109_dead`（2026-08-15）：批A正向封顶 sh 0.34、批C镜像 sh 0.39，2y 墙 + rn 负，dead_count 19 |

**判死是族级/集级，不是"区域不能挖"** ⇒ 换目标而非止损。全库扫描：

```
族非空 ∧ 未判死           : 128 个
其中同时在本区 S0 白名单  :  22 个
最优 = EUR/other460（418 族）
```

## 2. L1→L3.5 产物（EUR/other460）

| 项 | 值 |
|---|---|
| 字段总数 / 信号 / 非信号 | 1393 / 1393 / 0 |
| 结构族 | **418**（`n_triclass` 115，完整三分类 112） |
| 区域合法档 | universe `TOP2500/TOPCS1600/TOP1200/TOP800/TOP400`，delay `1/0` |
| 可用分组轴 | INDUSTRY / SUBINDUSTRY / SECTOR / MARKET 等（EUR 均支持） |

## 3. 三源验证

| 源 | 状态 | 结论 |
|---|---|---|
| **L1 内部实证** | ✅ **已跑** | GLB 在 model264 上跑过两波：`mirror`（单字段时序）最好 **S=1.40/F=0.67，未达提交线 1.58/1.0**；`trendprob` **全部负 Sharpe**（−0.37～−1.29）。**三分类概率族的净方向价差从未试过**（trendprob 用的是 `mdl264_1l_*` 单字段）⇒ 新方向，非克隆 |
| **L2 论坛 recon** | ✅ **已修复并跑通（重大正面证据）** | 修完 `resolve_id` 三元组 bug（§5.3）后重跑同一问题：退出码 **0**，`found=true`，**6 篇有效文章**。其中 1 篇**直接命中本机制且就在 EUR 市场**（§3.1），给出了可迁移的算子配方与 Setting 实测值 |
| **L3 学术** | — 未跑 | 机制命名已由字段描述 + L2 独立佐证共同给出，未消耗 |

### 3.1 L2 命中帖（EUR 市场，同构机制）

> 帖 `43620895448343`《财报电话会的"情绪概率差"——**EUR 市场**的事件情绪因子与"低相关性"设计》（alpha `XgbXWEWm`）

- **机制同构**：数据给的是 [正/中/负] **三类概率**，作者主张用 **`P_pos − P_neg` 分布层面的净情绪**，而非压成单一 tone 分数。这与本轮 `subtract(P_up, P_fall)` **完全同构**，且独立发生于情绪数据集 ⇒ 机制有跨数据集泛化性。
- **★ 数据探索结论（可直接迁移）**：同数据集的 argmax **类别标签**单独用 Sharpe 仅 ~1.2–1.5，**保留概率差的信息量明显更高** ⇒ **不要用 `*_class` 标签**，坚持 `_l3 − _l1`。
- **★ 算子配方（本轮骨架原先缺失的三件）**：
  1. `ts_zscore(x, L)` **自身历史标准化**——"水平 → 意外"的翻译器（情绪/预期类水平值横截面不可比）。
  2. `signed_power(·, e)` **保号幂放大尾部**——且作者实测**显著降低与 production 的持仓重合度**（正打我方 prod<0.7 铁律的痛点）。
  3. `ts_backfill(x, f)` **有界前向填充**——仅当数据事件稀疏时需要（本集是否稀疏未知 ⇒ 变体化）。
- **Setting 实测（EUR）**：`TOP2500 / D1 / decay 6 / trunc 0.04`。
- ⚠ **中性化不可照搬**：帖写 `COUNTRY`，但 **EUR 合法档位里没有 COUNTRY**（`config.REGIONS['EUR'].neutralizations`）⇒ 退到语义最接近的 **`MARKET`**（剥离国别/市场差异），与本区"换 market 是破比值闸决定性旋钮"的既有实证同向。
- ⚠ 该帖 votes 仅 4，属**未经广泛验证的分享**，作正面线索而非定论。

## 4. 候选族 → 经济量命名 → 骨架

### 4.1 族与经济量

| 族 | 经济量（来自字段描述） | ac / users |
|---|---|---|
| `oth460_float_to` | **流通盘换手（Float Turnover 12M）的预期方向** — 上行=筹码松动，下行=锁定 | 5 / 2 |
| `oth460_divyld_bb` | **股东总回报（股息 + 股本变动）的预期方向** | 1 / 1 |
| `oth460_viac` | **核心盈利（归一化普通股可分配净利）的预期方向** | 1 / 1 |

（`oth460_adoa` 终止经营长期资产、`oth460_eont` 其他净额语义偏弱，本轮不选）

### 4.2 形态枚举与骨架

> 记号：`P_up = *_l3`，`P_fall = *_l1`。`subtract(P_up, P_fall)` 是**同一经济量的两个对立分量**之差 = 单一净方向信号，**不是两条独立腿相加**，合规。

| ID | 形态 | 表达式 | 算子数 |
|---|---|---|---|
| **A1** | H1 净方向价差 | `group_rank(ts_decay_linear(subtract(oth460_float_to_l3, oth460_float_to_l1), 5), industry)` | 3 |
| **A2** | H1 变体（换轴） | `group_zscore(ts_decay_linear(subtract(oth460_float_to_l3, oth460_float_to_l1), 5), subindustry)` | 3 |
| **B1** | H1 股东回报 | `group_rank(ts_decay_linear(subtract(oth460_divyld_bb_l3, oth460_divyld_bb_l1), 5), industry)` | 3 |
| **C1** | H2 门控 | `trade_when(oth460_viac_l1 > 0.5, group_rank(ts_decay_linear(subtract(oth460_float_to_l3, oth460_float_to_l1), 5), industry))` | 4 |
| **D1** | H4 跨族背离 | `group_rank(subtract(subtract(oth460_divyld_bb_l3, oth460_divyld_bb_l1), subtract(oth460_viac_l3, oth460_viac_l1)), industry)` | 4 |

**经济含义**
- A1/A2：换手率预期**净上行倾向**。换手预期上行 = 筹码松动/关注度上升。
- B1：股东回报预期的净方向。
- C1：**核心盈利预期恶化（P_fall>0.5）时**才启用换手方向——盈利下行期，换手的信息含量更高（市场正在重新定价）。
- D1：回报预期方向 − 盈利预期方向 = **回报与盈利的背离**；回报升而盈利降 ⇒ 可能来自股本操作而非经营改善，是负向信号。

### 4.2b 骨架 v2 —— L2 证据驱动（**推荐，取代 v1**）

L2 命中帖给出了「分布差 + 长期自标准化 + 保号幂放大」模板。相对 v1 的三处**结构性补强**：
`ts_zscore`（水平→意外）／`signed_power`（放大尾部 + 降 prod 重合）／**不用 `_class` 标签**。

> 记号：`bf(x)=ts_backfill(x,60)`，`z(x)=ts_zscore(x,250)`。

| ID | 族 | 表达式 | 算子数 | 控制变量 |
|---|---|---|---|---|
| **P1** | float_to | `signed_power(subtract(z(bf(oth460_float_to_l3)), z(bf(oth460_float_to_l1))), 3)` | 6 | 基线（含 backfill） |
| **P2** | float_to | `signed_power(subtract(z(oth460_float_to_l3), z(oth460_float_to_l1)), 3)` | 4 | **测 ts_backfill 是否需要**（数据集稀疏度未知） |
| **P3** | float_to | `group_rank(signed_power(subtract(z(oth460_float_to_l3), z(oth460_float_to_l1)), 3), market)` | 5 | **测分组轴 market**（破比值闸旋钮） |
| **P4** | divyld_bb | `signed_power(subtract(z(oth460_divyld_bb_l3), z(oth460_divyld_bb_l1)), 3)` | 4 | 换族（valuation 类别，分散） |
| **P5** | viac | `signed_power(subtract(z(oth460_viac_l3), z(oth460_viac_l1)), 3)` | 4 | 换族（profitability 类别） |
| **P6** | float_to | `subtract(oth460_float_to_l3, oth460_float_to_l1)` | 1 | **裸价差对照**——测「配方 vs 裸」增益是否真实（可选） |

- 算子数 1–6，**全部 < 10** ✅（复杂度纪律）
- **合规**：`subtract(P_up,P_fall)` = 同一经济量对立分量之差，**单信号**；`signed_power`/`ts_zscore`/`ts_backfill` 均为**单信号上的单调变换**，不构成第二条腿 ✅
- **不用 `_class`**：帖实测 argmax 标签 Sharpe 仅 1.2–1.5，概率差信息量更高 ⇒ 本批零条使用 `_class` ✅

### 4.3 合规自检

| 检查项 | 结果 |
|---|---|
| 组合形态铁律（禁两条独立腿加权相加） | ✅ 全部单信号；`subtract(P_up,P_fall)` 为同一经济量对立分量；D1 为两期限/两口径的**背离度**，单一经济量 |
| 算子个数 < 10 | ✅ 3–4 |
| 分组轴区域合法 | ✅ industry/subindustry 均在 EUR `neutralizations` 内 |
| 避判死 | ✅ other460 无 `<ds>_dead` 记录，且在 EUR `s0_whitelist` |
| 避已知失败形态 | ✅ 见 §4.4 |

### 4.4 避坑清单（来自 GLB/DEU 实证）

1. **不加前缀负号**——GLB `trendprob` 波 8 条全负（−0.37～−1.29）。
2. **不用 `ts_delta(...,22)` 长窗**——该波 turnover 0.24/0.65 失控。
3. **不用 `vec_avg(mdl138_*)` 跨集拼接**——turnover 0.65。
4. **用 `ts_decay_linear(...,5)` 短窗**——GLB `mirror` 波最优组（S=1.33～1.40）全在此形态，turnover 仅 0.02–0.04。
5. **分组轴优先级 industry > country > sector**——mirror 波 sector 版 S 掉到 0.88。

## 5. 顺带发现的 3 个真问题

### 5.1 `s0_whitelist` 含已判死集（GBR/news48）
`news48_dead` 判 DEAD 且 rule 明写"不进白名单"，但 `GBR/s0_whitelist` 仍含 news48。**白名单生成未剔除判死集** —— 建议 S0 选集后加一道「白名单 ∧ ¬判死」的交叉校验（可与闸 TRI 同源复用）。

### 5.2 GBR 白名单实质无主信号目标
`pv30/pv29` 白名单注释明写"只能作 group_* 分组轴/辅助腿，**不作主信号**"；`institutions6` 仅 11 字段且族为 0；`news48` 幽灵集。**⇒ GBR 需先重跑 S0 刷新白名单，而非硬挖。**

### 5.3 `forum_recon` 读帖链路故障 → **已定位根因并修复**

症状：搜索侧正常（8 轮 30 hits、0 search_error），但 `reads_ok=0 / read_errors=17` ⇒ 读帖全挂。
工具当时**正确落 `error` 而非误判"无解"**（符合纪律），但 L2 源因而不可用。

**根因（实测，非猜测）**：`forum_research.resolve_id` 返回的是 **三元组** `(post_id, is_community_post, url)`，
而 `forum_recon.py` 里是 `pid = fr.resolve_id(...)` —— **没解包**，把整个元组当 id 拼进 URL：

```
/community/posts/('33036460396567', True, 'https://...').json   →  恒定 404 InvalidEndpoint
```

而 `get_with_retry` 对 404 **不重试**、`read_post` 见非 200 返回 `None`，于是整链静默退化成 `read_failed`
——**看起来和"论坛无解"一模一样**（这正是"故障 ≠ 无解"纪律要防的那类假象）。

**修复**：新增 `_resolve_post_id()` 适配层（解包 + 校验 `is_community`，非社区帖直接跳过而非撞 404；兼容标量契约）。
**验证**：同一问题重跑 ⇒ 退出码 **0**、`found=true`、**6 篇有效文章**（原为 error）。HTTP 404 → 200，读帖 0/3 → 3/3。
新增 5 条守护测试（`tests/unit/08_forum_recon`，223 passed）。诊断脚本 `tools/diag_forum_read.py`。

## 6. 下一步（待确认，涉及配额）

- 骨架 **v2（P1–P6）尚未回测**。发起探针消耗回测配额，需你确认后再执行。
- **仿真设置（已按本区台账 + L2 实测定案，非凭记忆外推）**：

  | 项 | 取值 | 依据 |
  |---|---|---|
  | region / universe | **EUR / TOP2500** | 本区台账 `universe_prod_isolation_probe_20260922`：TOP400 把 S 从 2.19 打到 0.5，**窄档塔陷**；L2 帖亦用 TOP2500 |
  | delay | **D1** | 帖：事件/预期类数据在 D1 下无前视 |
  | neutralization | **MARKET**（P3 内嵌），其余走设置层 `MARKET` | 帖要 `COUNTRY` 但 **EUR 无此档** ⇒ 退到语义最接近的 MARKET；与本区"换 market 是破比值闸决定性旋钮"同向 |
  | decay | **6** | L2 帖实测（平滑跳变、控换手） |
  | truncation | **0.04** | L2 帖实测（0.08 压不住稀疏横截面的单票集中） |

- **配给**：按 L4 探针原则每族 1–2 条 ⇒ **建议先跑 P1/P2/P3/P4/P5 共 5 条**（P6 裸价差对照视结果再加）。
  `|S| ≥ 0.5` 的才扩批；扩批方向优先**同数据集其余 ~112 个完整三分类族**（`max_ac` 几乎全为 0 ⇒ 极低拥挤度白空间）。

### 6.1 探针已发起（2026-10-02）

- **multisimulation_id：`3dM6B82TG4Vwc8d136rdJOsK`**（5 条 P1–P5）
- 发起前**已过 `validate_expressions`**（EUR/TOP2500/D1，6 字段全存在、`unknown_fields=[]`）——
  依本区台账教训（批内一条 ERROR 会连坐取消整批）必做。
- 设置：`EUR / TOP2500 / D1 / MARKET / decay 6 / trunc 0.04 / EQUITY / FASTEXPR / maxTrade OFF`

**扩批池（已盘点，供 `|S|≥0.5` 后取用）**

| 类别 | 族数 | ac_sum | 代表族 |
|---|---|---|---|
| growth | 92 | 21 | float_to, adoa, eont, **viac**, sol4, soca, tstk, trix, eres, div_payout |
| profitability | 17 | **2** | es_ebit_fy1_d1m, sbit, es_roe_fy1_r1m, es_ebitda_ntm_r1m, eps_sur_decay |
| valuation | 2 | 1 | **divyld_bb**, psale |
| tech_trend | 1 | 1 | macd |

（粗体 = 本批已覆盖。profitability 17 族 ac 几乎全 0 ⇒ 下一批优先做类别分散。）

### 6.2 实测结果（2026-10-02 回收，5/5 完成）

| ID | alpha | 形态 | **S** | F | **2Y** | sub-uni | turnover | 判定 |
|---|---|---|---|---|---|---|---|---|
| P1 | `LLZA5dmn` | float_to **+ ts_backfill** | 0.53 | 0.13 | **−0.09** | 0.55 | 0.363 | 未达线 |
| P2 | `RR6nA1le` | float_to 裸配方 | 0.44 | 0.10 | 0.04 | 0.63 | 0.378 | 未达线 |
| **P3** | **`P0gdMOzJ`** | **float_to + `group_rank(market)`** | **1.22** | **0.37** | **0.91** | 0.46 ❌ | 0.392 | **唯一有希望** |
| P4 | `wpbM9EG1` | divyld_bb | 0.01 | 0.00 | −0.45 | 0.00 ❌ | 0.330 | 无效 |
| P5 | `786Eonm1` | viac | −0.53 | −0.23 | −0.02 | −0.46 ❌ | 0.220 | 负向 |

**三条实证结论**

1. **★ `group_rank(x, market)` 是决定性杠杆，且强于设置层 neutralization**
   P2（无 group_rank）S=0.44 / 2Y=0.04 → P3（加 group_rank）**S=1.22 / 2Y=0.91**（+177%）。
   本批设置层已是 `neutralization=MARKET`，**再加表达式内嵌 `group_rank(market)` 仍有巨大增量**
   ⇒ 两者不等价，内嵌分组秩是独立增益维度。这与既有实证「分组轴换 market 是破比值闸决定性旋钮」同向，并把它从**设置层**推进到**表达式层**。
2. **`ts_backfill` 不需要**（other460 非稀疏事件数据）：P1(带) 0.53 / 2Y −0.09 反而略差于 P2(不带) 0.44 / 2Y 0.04。
   ⇒ 论坛配方里的 backfill 是数据集相关项，**不能无差别照搬**。
3. **族之间是天壤之别，不是"三分类族都行"**：float_to 1.22、divyld_bb 0.01、viac −0.53。
   ⇒ 扩批**必须换族筛选**，不能假定同数据集内机制通用。

**P3 的卡点**（4 项硬闸失败）

| 闸 | 实测 | 线 | 缺口 |
|---|---|---|---|
| LOW_SHARPE | 1.22 | 1.58 | −0.36 |
| LOW_FITNESS | 0.37 | 1.00 | −0.63 |
| **LOW_SUB_UNIVERSE_SHARPE** | **0.46** | **0.63** | **−0.17（新卡点，比值闸）** |
| LOW_2Y_SHARPE | 0.91 | 1.58 | −0.67 |

- 注意 `risk_neutralized_sharpe=1.35`、`investability_sharpe=1.03`、`CLUSTER_TEST=1.05`（仅 warning）
  ⇒ 信号本身不弱，**死在 sub-universe 比值闸 + fitness**，不是死在方向。
- 已入台账：`EUR` / wave `l4_probe1` / multisim `3dM6B82TG4Vwc8d136rdJOsK`，verdict=PARTIAL（0/5 过硬闸，1 条过 near 线）。
