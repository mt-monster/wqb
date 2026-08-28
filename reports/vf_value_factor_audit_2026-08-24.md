# 价值因子（Value Factor）现状审计与提升方案
> 生成时间：2026-08-24 ｜ 数据源：WQ BRAIN 生产 book（`get_user_alphas(stage=OS)` 全量 164 个，价值因子 26 个全部 ACTIVE）
> 价值因子判定：表达式含 `mdl177_*valuefactor/earningsquality/deepvalue/relativevalue`、`earnings_yield`、`book_to_market`、`to_price`、`valuation` 等价值/盈利字段。

## 一、当前 VF 现状（数字）

| 维度 | 数值 |
|---|---|
| 生产 book 总 alpha（OS 阶段） | 164 |
| **其中价值因子** | **26（全部 ACTIVE）** |
| 区域分布 | USA 21 / MEA 3 / EUR 2 |
| Sharpe（均值 / 中位） | 1.556 / 1.61 |
| Fitness（均值 / 中位） | 1.338 / 1.255 |
| **ProdCorr（中位）** | **0.0（无任何生产相关瓶颈）** |
| **SelfCorr > 0.7（内部冗余）** | **6 个** |
| 低 Sharpe 尾部（< 1.40） | 8 个（最低 dodNqlJ 1.26） |

**重要发现（与记忆不一致）**：记忆称「book ~145 ACTIVE、多 mdl177 价值/盈利主导」。实测价值因子仅 **26 个**，占 164 的 16%，并非多数派——其余为动量/情绪/分析师等风格。说明：① 记忆中 145 数字已过时或指更宽的「基本面」桶；② 当前价值因子已是**少数派且内部高度同质**，提升方向应是「提质 + 降冗余」而非「加量」。

**瓶颈定位（第一性原理）**：
- **不是生产相关**（prodCorr 中位 0，全部已过关）。
- **是内部 selfCorr 冗余 + 低 Sharpe 尾部**：26 个表达式可聚类为 5 类模板，其中 2 类模板的变体互相 selfCorr 高达 0.9+，等于把同一个想法反复提交。

## 二、模板聚类（26 个 → 5 类）

| # | 模板结构 | 代表 alpha | 数量 | selfCorr 风险 |
|---|---|---|---|---|
| A | `group_mean(ts_std_dev(V,20),1,subind) - ts_std_dev(V,20)` → `ts_mean(,60)`（估值离差残差） | 6JMmdrG / 1PzP10k / GxezqzQ / dodNqlJ | 4 | **极高**（0.54–0.96） |
| B | `-V * ts_std_dev(V,20)`，`vector_neut(a, abs(ts_mean(returns,252)/ts_std_dev(returns,252)))`（价值×波动中性） | gdolWn0 / z0oNEa1 / ev2q0Nd / orAkx3k / RzMOGR0 / EzWWGJP / zGMV9N8 | 7 | 高（0.69–0.97） |
| C | `ts_sum(earningsqualityfactor_*,252)` → `group_neutralize(...,cap bucket)` | Gze9QEO / vGJrvjz / 0gnPV9p | 3 | 中（0.59–0.78） |
| D | `group_rank(log(ts_mean(curep,44)) - log(ts_mean(curep,22)), industry)`（盈利增速对数比） | VmdG395 / K5rmVOx / 2XwomaY | 3 | **高**（0.67–0.92） |
| E | `group_rank(ts_zscore(salerec/chgsgasale,60), *)` | 7v1bE3v / m0X79vx / WodgzLO | 3 | 中高（0.51–0.83） |
| F | MEA/EUR 价值+技术形态混合 `add(0.4*value, 0.6*pattern)` | Wj7g2gAx / Wj71Q12o / LLG9EArv / gJ8QXEdv / 2rpOGr7P / N19r6q0L | 6 | 低（0.0–0.65） |

**关键洞察（因果推断）**：
- 模板 A/B/D 的变体几乎只换字段不换算子 → **selfCorr 0.9+ 是必然结果**（同一信号不同字段名）。
- **模板 F（价值+形态混合）反而 Sharpe 最高（1.65–1.92）、selfCorr 最低**——这直接验证了学术结论：价值因子单独持有长期跑输，与低相关因子（形态/质量/低波）组合才能抬升风险调整收益（Asness et al. 2013）。

## 三、6 个高 selfCorr 冗余项（优先处理）

| alpha | selfCorr | sharpe | 模板 | 建议 |
|---|---|---|---|---|
| zGMV9N8 | 0.974 | 1.70 | B | 与 EzWWGJP 近孪生，二留一 |
| GxezqzQ | 0.964 | 1.49 | A | 与 6JMmdrG 近孪生，二留一 |
| 6JMmdrG | 0.947 | 1.64 | A | 保留其一 |
| VmdG395 | 0.918 | 1.67 | D | 与 K5rmVOx 近孪生，二留一 |
| 7v1bE3v | 0.832 | 1.62 | E | 可换 sector→subindustry 降相关 |
| Gze9QEO | 0.777 | 1.76 | C | 质量腿本身不错，降相关即可 |

> 这 6 个占用「新颖度预算」却不增加多样性。**原则 #3（均匀点塔）要求：同质模板只保留 1–2 个最优，其余改用异质结构替换**。

## 四、论坛 + 学术：提升价值因子的 6 条路径

**来源**：WQ 中文论坛/SCSNN 教程（提 Sharpe/中性化/降 turnover）、Asness-Moskowitz-Pedersen (2013) *Value and Momentum Everywhere*、Asness-Frazzini-Pedersen (2019) *Quality Minus Junk*、Fama-French 5-factor、McLean-Pontiff (2016) 因子衰减。

1. **价值 + 质量/低波 组合（QMJ 思路）**：价值单独在 2010–2020 美股显著跑输十余年；与盈利能力（ROE/毛利率）、低杠杆、低波动组合可抬升 Sharpe 且负相关对冲。→ 模板 A/B 不要只换字段，应加一条**质量或低波腿**（如 `group_rank(low_leverage_residual)`）。
2. **中性化升级**：CSDN 教程共识——行业/子行业中性化通常**提升** Sharpe（同时略降收益）。当前 USA 价值 alpha 几乎全用 `MARKET` 中性化 → 试 `SUBINDUSTRY`/`SECTOR`，既是提 Sharpe 杠杆，也是**降 selfCorr** 杠杆（不同模板因此发散）。
3. **长期反转 + 估值离差**：EUR 冠军 `Wj7g2gAx` 用 `earnings_yield_3` 减 `group_mean(...,industry)`（价值相对行业均值反转），Sharpe 1.8。可复制：价值信号减其行业/子行业长期均值。
4. **换操作符降相关（原则 #12）**：对拥挤模板做算子替换——
   - `group_rank(X, market)` → `ts_rank(X, 22)` 或 `group_rank(X, subindustry)`
   - `ts_std_dev(X,20)` → `ts_zscore(X,20)` / `decay_linear(X,20)`
   - 减法（离差）→ 除法（相对比）
5. **控制过拟合（原则 #10/#11）**：警惕 `add(0.4*A, 0.6*B)` 式加权拼信号。区分两类：① **同信号加权调参（禁止）**；② **异质风格组合（鼓励，即 QMJ）**。MEA 模板 F 属②（价值+形态），应推广而非照搬权重。
6. **窗口有意义（原则 #5）**：当前窗口 20/30/44/60/66/126/252。其中 **44 非标准**（应≈2 月），模板 D 用 44 vs 22 对数比——建议改为 22×2=44 可解释为「双月增速/月增速」，或统一为 66（季）以符合惯例，避免被判定随意。

## 五、针对您这 26 个的具体改造清单

**立即可做（提质，不新增）**
- 低 Sharpe 尾部 8 个（dodNqlJ 1.26 / 1PzP10k 1.27 / gdolWn0 1.28 / 0gnPV9p 1.29 / ev2q0Nd 1.30 / RzMOGR0 1.31 / WodgzLO 1.39 / m0X79vx 1.40）：优先把 `neutralization: MARKET` 改为 `SUBINDUSTRY` 重测，预期 Sharpe 提升。
- 6 个高 selfCorr：每类模板保留 1 个最高 Sharpe，其余 4 个用第 4 节算子替换降相关后**另作新 alpha**（而不是原样占坑）。

**结构升级（仿 MEA 模板 F）**
- 将 USA 模板 A/B 的纯价值残差，加一条**低波/质量腿**：`add(0.6 * value_residual, 0.4 * lowvol_residual)`，复制模板 F 的成功路径（已证 Sharpe 1.65–1.92、selfCorr 低）。
- 区域均衡：当前 USA 21 / MEA 3 / EUR 2，价值因子在 MEA/EUR 远未铺满 → 把 USA 验证过的模板平移到 MEA/EUR（原则 #3 均匀点塔）。

## 六、推荐实验（可运行探针，待您确认后启动）

1. **中性化扫描**：对 8 个低 Sharpe 尾部，分别跑 `MARKET / SUBINDUSTRY / SECTOR` 三档，确认哪档 Sharpe 最高（预计 SUBINDUSTRY 胜出）。
2. **降相关算子矩阵**：对模板 A（4 个）与模板 D（3 个）做 `group_rank↔ts_rank↔ts_zscore` × 窗口 22/66 组合，挑 selfCorr<0.4 且 Sharpe>1.5 的变体。
3. **价值+质量混合**：选 2 个 USA 纯价值模板，各配一条质量腿（毛利率/低杠杆残差），验证 Sharpe 与 selfCorr 是否同时改善。

> 以上探针各约 3–8 次仿真。确认后我可批量发起（带断点续跑），跑完给最终「保留/替换/新增」判定与收益归因。
