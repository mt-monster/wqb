# board_gov_stats 字段画像（USA / D1 / TOP3000）

> 数据集：`board_gov_stats`｜category = **INSIDERS**｜data_type = **MATRIX**（无需 `vec_*` 聚合）
> 46 字段｜平均 coverage **0.9197**｜平台 alphaCount **177**（低拥挤）｜value_score 3｜multiplier 1.1
> 塔位实测：`pyramid_short = "insiders"`、`pyramids.list = [{name:"USA/D1/INSIDERS", multiplier:1.1}]`
> ⇒ **INSIDERS 单塔，合规**（不触碰 PV/MODEL/OTHER 禁混规则）
> 画像来源：MCP `get_field_catalog` 全量拉取 + 波 191 六条机制探针实测（multisim `1lm8aF4UY4VXcw6150DxzXGT`）

---

## 1. 数据集级判断

| 维度 | 值 | 判断 |
|---|---|---|
| 字段数 | 46 | 中等规模，一次性画像可行 |
| coverage 区间 | 0.5948 – 0.9482 | **高且齐**，无低覆盖陷阱字段（唯一例外 `surname_concentration_management` 0.5948） |
| alphaCount | 177 | **低拥挤**（对比 risk70 的 82,093、earnings4 的 13,771）⇒ prod 相关墙风险低 |
| 塔位 | USA/D1/INSIDERS | 未点亮塔，**点塔价值高** |
| 数据类型 | 全 MATRIX | 无需 `vec_*` 预处理，写法最简 |
| 更新频率 | 日频（治理快照） | 但字段本质是**慢变量**，TO 天然极低 |

**核心结构性特征**：探针六条的 **TO 全部落在 1.1%–3.1%、margin 5.5–7.0 bp**。
对比 RISK 塔 `88RAN85m` 的 61.77% / 2.86 bp、SHORTINTEREST 的 11–18% / 0.13–0.27 bp —— 这是**低换手高 margin 的稀缺结构**：
- 好处：永不受 `HIGH_TURNOVER` 闸威胁；
- 代价：`fitness = S · sqrt(R/TO)`，TO 被压到 1% 时 R 也极小，**fitness 反而更难达标**。本数据集的主要矛盾是 **S 不够高**，不是 TO 太高。⇒ 常规「压换手」动作在这是**反向的**。

---

## 2. 七族分类与实测状态

### A. 流动率族（18 字段）—— ✗ **判死**

| 字段 | cov | users | alphas | 实测 |
|---|---|---|---|---|
| `board_departure_rate_3m_management` | 0.9234 | 22 | 32 | **S 0.32 / F 0.09 / TO 3.10% / 2Y 0.78 / SUB 0.15 / risk_neut_S −0.52 / fRA 3** |
| `board_join_rate_3m_management` | 0.9234 | 18 | 21 | **S 0.33 / F 0.09 / TO 2.91% / 2Y 0.84 / SUB 0.08 / risk_neut_S −0.28 / fRA 4** |
| `board_departure_rate_1y_board` | 0.886 | 4 | 6 | 未测（同族，按判死处理） |
| `board_join_rate_1y_board` | 0.886 | 2 | 6 | 未测 |
| `board_departure_rate_6m_management` | 0.912 | 8 | 12 | 未测 |
| `board_join_rate_6m_management` | 0.912 | 3 | 3 | 未测（论坛帖 `43907846056599` 用过，写法 `group_rank(ts_rank(ts_backfill(board_join_rate_6m_management, 120), 252), industry) > 0.7`） |
| `personnel_departure_rate_1y_total` | 0.886 | 0 | 0 | 无人挖 |
| `personnel_departure_rate_3m_total` | 0.9234 | 6 | 10 | 未测 |
| `personnel_departure_rate_6m_total` | 0.912 | 4 | 5 | 未测 |
| `personnel_join_rate_1y_total` | 0.886 | 1 | 1 | 未测 |
| `personnel_join_rate_3m_total` | 0.9234 | 3 | 5 | 未测 |
| `personnel_join_rate_6m_total` | 0.912 | 1 | 1 | 未测 |
| `management_departure_rate_1y_management` | 0.8775 | 2 | 2 | 未测 |
| `management_departure_rate_3m_management` | 0.9149 | 5 | 6 | 未测 |
| `management_departure_rate_6m_management` | 0.9031 | 1 | 1 | 未测 |
| `management_join_rate_1y_management` | 0.8775 | 2 | 2 | 未测 |
| `management_join_rate_3m_management` | 0.9149 | 3 | 4 | 未测 |
| `management_join_rate_6m_management` | 0.9031 | 1 | 1 | 未测 |

**判死依据（两条独立证据）**：
1. 实测 S 0.32 / 0.33，`fitness` 0.09（远低于 1.0），**`risk_neutralized_sharpe` 双双为负**（−0.52 / −0.28）⇒ 信号经风险中性化后反向，说明只是风格暴露的残渣。
2. 论坛帖 `43152032301591`（43 赞）明确写：董事会治理属**慢变量 fundamental**，与「行为反应不足」类机制在时间尺度上不匹配。

> ⚠ **不可整集判死**：同一数据集的任期族与网络族有真信号（见 B / C）。「流动率族判死」≠「board_gov_stats 判死」。

---

### B. 任期族（5 字段）—— ✓ **有真信号，主攻方向之一**

| 字段 | cov | users | alphas | 实测 / 状态 |
|---|---|---|---|---|
| **`ceo_tenure_days`** | 0.9334 | 11 | 13 | **✓ S 1.23 / F 0.70 / TO 1.16% / 2Y 1.75 / SUB 0.30 / invest_S 1.28 / risk_neut_S +0.81 / margin 7.03 bp / fRA 3** |
| `chairman_tenure_days` | 0.9364 | 7 | 14 | 未测（**波 192 未覆盖**） |
| `max_chief_officer_tenure_days` | 0.9353 | 6 | 9 | 未测 |
| `median_chief_officer_tenure_days` | 0.9353 | 6 | 7 | 未测 |
| `min_chief_officer_tenure_days` | 0.9353 | 5 | 5 | 未测 |

**经济含义**：CEO 任期长度 = **管理层固守（entrenchment）/ 治理稳定性** 的代理变量。
- 任期长 ⇒ 董事会监督弱、战略连续性强、短期盈余管理动机低；
- 任期短 ⇒ 新任 CEO 有「大洗澡」（big bath）与盈余冲刺动机。

**⚠ 算子约束（本族最关键的技术认知）**：`*_tenure_days` 是**单调递增计数器**（同一 CEO 在任期间每日 +1）⇒
- `ts_delta(F, W)`、`ts_av_diff(F, W)` 对长任期 CEO **恒等于 W**，是近似二元的「是否新任」哑变量；
- `ts_std_dev(F, W)` 对线性斜坡是常数 ⇒ 横截面无变异，**退化**；
- `ts_rank(F, W)` 对单调序列恒为 1 ⇒ **退化**。

⇒ **本族只能做「水平」信号**，变化必须靠**横截面算子 + 分组轴切换**获得，不能靠时序算子。这是与网络族（B 之外）的核心差别。

---

### C. 网络族（6 字段）—— ✓✓ **有真信号，最健康载体**

| 字段 | cov | users | alphas | 实测 / 状态 |
|---|---|---|---|---|
| **`board_external_connection_count`** | 0.9482 | 14 | 15 | **✓✓ S 1.17 / F 0.65 / TO 1.14% / 2Y 1.84 / SUB 0.58 / invest_S 1.14 / DD 7.88%（六条最低）/ risk_neut_S +1.09（六条最高）/ `checks.fail = []` / fRA 2** |
| `aggregate_external_connections` | 0.9482 | 9 | 10 | 未测 |
| `unique_external_company_board` | 0.9482 | 3 | 3 | 未测 |
| `unique_external_company_union` | 0.9482 | 3 | 3 | 未测 |
| `management_external_connection_count` | 0.9411 | 2 | 2 | 未测 |
| `unique_external_company_management` | 0.9411 | 3 | 3 | 未测 |

**经济含义**：董事/高管在**外部公司**兼任席位数 = **社交资本 / 弱连接广度**。
- 连接多 ⇒ 信息渠道广、资源获取强（信息优势假说）；
- 连接过多 ⇒ 过度承诺（busy board）、监督稀释（overcommitment 假说）。

⇒ **方向不先验确定**，必须让回测定符号（这是与任期族的重要差别）。

**为什么这是最佳载体**：
- `checks.fail = []` —— 平台硬闸**零失败**，S/F 只是 warning 级；
- `2Y 1.84` 已过 1.58 闸，`SUB 0.58` 在闸线之上，`CW` 通过，`DD 7.88%` 六条最低；
- `risk_neut_S +1.09` 六条最高 ⇒ **不是纯风格暴露**；
- 唯一缺口：S 1.17 → 1.58（+26%）、F 0.65 → 1.00（+35%）。

**与任期族相反，网络计数不是单调递增** ⇒ **时序算子全部可用**（`ts_delta` / `ts_std_dev` / `ts_rank` / `ts_zscore` / `ts_av_diff` 都有真实变异）。这是波 192 把 6/10 个模板押在网络族上的原因。

---

### D. 治理 flag 族（4 字段，二元）

| 字段 | cov | users | alphas | 状态 |
|---|---|---|---|---|
| `ceo_chairman_duality_flag` | 0.9223 | 9 | 12 | 未测（两职合一 = 权力集中，经典治理指标） |
| `chief_officer_chairman_flag` | 0.924 | 2 | 2 | 未测 |
| `multiple_ceo_indicator` | 0.9482 | 1 | 1 | 未测（多 CEO 并存 = 治理混乱，稀有事件） |
| `ceo_gender_flag` | 0.9334 | 2 | 2 | 未测 |

**风险提示**：二元 flag 的横截面方差极小，`group_rank` 后会出现**大量并列（ties）**，秩型信号退化。若要使用，需配 `ts_mean(F, 252)` 之类的「过去一年占比」做平滑，把二元转成连续比例。

---

### E. 规模 / 构成族（4 字段）

| 字段 | cov | users | alphas | 实测 / 状态 |
|---|---|---|---|---|
| `board_member_count_2` | 0.9482 | 7 | 7 | 未测（董事会规模，与任期族可组结构比） |
| `management_team_size` | 0.9411 | 2 | 2 | 未测 |
| `total_personnel_count` | 0.9482 | 0 | 0 | **无人挖** |
| `independent_director_ratio` | 0.9482 | 4 | 4 | **✗ S 1.01 / F 0.57 / 2Y 1.10 / DD 6.69% / risk_neut_S +0.17 / fRA 4** |

**判断**：`independent_director_ratio` 单独无信号（`risk_neut_S` 仅 +0.17，接近风格残渣）。但**独立董事比例是天然的「治理制衡」乘子**，与姓氏集中度组合可能有效（波 192 T9 之外的候选方向）。

---

### F. 性别 / 学历族（6 字段）

| 字段 | cov | users | alphas | 状态 |
|---|---|---|---|---|
| `male_ratio_board` | 0.9482 | 7 | 7 | 未测 |
| `male_ratio_management` | 0.9411 | 2 | 2 | 未测 |
| `male_ratio_total_personnel` | 0.9482 | 2 | 2 | 未测 |
| `doctorate_share_board` | 0.9482 | 9 | 10 | 未测（学历构成，人力资本代理） |
| `doctorate_share_management` | 0.9411 | 1 | 1 | 未测 |
| `doctorate_share_total_personnel` | 0.9482 | 4 | 4 | 未测 |

**判断**：属「人口学构成」维度，与治理质量无直接因果链，且是**极慢变量**（年度级变化）⇒ 在日频 TO 结构下大概率无信号。**低优先级**，除非做「构成突变 = 战略转向」的事件型设计。

---

### G. 姓氏集中度族（3 字段）—— 家族控制代理

| 字段 | cov | users | alphas | 实测 / 状态 |
|---|---|---|---|---|
| **`surname_concentration_total_personnel`** | 0.9482 | **0** | **0** | **S 0.87 / F 0.45 / TO 1.21% / 2Y 1.90（六条最高）/ margin 5.52 bp / SUB 0.14 ✗ / risk_neut_S +0.78 / fRA 3** |
| `surname_concentration_board` | 0.9482 | 2 | 2 | 未测 |
| `surname_concentration_management` | **0.5948** | 2 | 2 | 未测（**全数据集最低覆盖**，慎用） |

**经济含义**：全员姓氏集中度 = **家族控制 / 裙带（nepotism）程度**。高集中 ⇒ 家族企业、代理冲突结构不同。
- **`surname_concentration_total_personnel` 全平台 0 人使用、0 个 alpha** —— 完全无人挖的独立维度；
- 2Y **1.90** 是六条探针最高，且 `risk_neut_S +0.78` 证实不是风格残渣；
- 唯一硬伤：**SUB 0.14** 破子宇宙闸 ⇒ 需要**换分组轴**（subindustry → market / sector）或换骨架救子宇宙。波 192 T10 就是这条救援线。

---

## 3. 波 191 六条探针全表（机制族判别基准）

统一骨架 `group_rank(ts_backfill(F, 120), subindustry)`，设置 TOP3000 / D1 / SUBINDUSTRY / decay 0 / trunc 0.08 / nanHandling ON。

| # | 字段 | alpha | 族 | S | F | TO | 2Y | SUB | invest_S | DD | risk_neut_S | fRA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `board_departure_rate_3m_management` | `kqNR8MOd` | 流动率 | 0.32 | 0.09 | 3.10% | 0.78 | 0.15 | 0.65 | 11.73% | **−0.52** | 3 |
| 2 | `board_join_rate_3m_management` | `vR10Yb6d` | 流动率 | 0.33 | 0.09 | 2.91% | 0.84 | 0.08 | 0.51 | 12.23% | −0.28 | 4 |
| 3 | `surname_concentration_total_personnel` | `ZYQZX9MQ` | 姓氏 | 0.87 | 0.45 | 1.21% | **1.90** | 0.14 ✗ | 0.89 | 11.01% | +0.78 | 3 |
| 4 | `ceo_tenure_days` | `MPYwgnZr` | 任期 | **1.23** | 0.70 | 1.16% | 1.75 | 0.30 | **1.28** | 11.88% | +0.81 | 3 |
| 5 | `board_external_connection_count` | `2rAEGxeP` | 网络 | 1.17 | 0.65 | 1.14% | 1.84 | 0.58 | 1.14 | **7.88%** | **+1.09** | 2 |
| 6 | `independent_director_ratio` | `E563mMxK` | 独立性 | 1.01 | 0.57 | 1.21% | 1.10 | 0.37 | 1.00 | 6.69% | +0.17 | 4 |

**田口式切分**：`risk_neutralized_sharpe` 把六条干净地分成两簇 —— 流动率族（−0.52 / −0.28）vs 其余四族（+0.81 / +1.09 / +0.78 / +0.17）。
⇒ **`risk_neutralized_sharpe` 应作为新数据集的第 3 号筛查指标**（排在 S 与 margin 之后），它比裸 S 更能区分「真信号」与「风格暴露」。

---

## 4. 波 192 十模板库（结构互异，已派发）

multisim `3nRYbmgZu4VhcmIyCfCb7xY`｜设置同波 191｜**差异维度标注**：

| # | 模板 | 表达式 | 字段 | 差异维度 | 机制来源 |
|---|---|---|---|---|---|
| T1 | 任期水平·industry 轴 | `group_rank(ts_backfill(ceo_tenure_days, 120), industry)` | 任期 | **分组轴**（subind → ind） | 自建 |
| T2 | 任期水平·market 轴 | `group_rank(ts_backfill(ceo_tenure_days, 120), market)` | 任期 | **分组轴**（→ 全市场） | 自建 |
| T3 | 任期水平·短 backfill | `group_rank(ts_backfill(ceo_tenure_days, 22), subindustry)` | 任期 | **覆盖/响应速度**（120 → 22） | 自建 |
| T4 | 网络水平·industry 轴 | `group_rank(ts_backfill(board_external_connection_count, 120), industry)` | 网络 | **分组轴** | 自建 |
| T5 | 网络一阶差分 | `group_rank(ts_delta(ts_backfill(board_external_connection_count, 22), 252), subindustry)` | 网络 | **矩：一阶变化**（社交资本扩张速率） | 自建 |
| T6 | 网络二阶 | `group_rank(ts_std_dev(ts_backfill(board_external_connection_count, 22), 252), subindustry)` | 网络 | **矩：二阶波动**（兼任不稳定度） | 自建 |
| T7 | 网络长窗时序秩 | `group_rank(ts_rank(ts_backfill(board_external_connection_count, 22), 504), subindustry)` | 网络 | **非线性：时序分位**（抗噪） | 自建 |
| T8 | 网络自身异常度 | `group_rank(ts_zscore(ts_backfill(board_external_connection_count, 22), 504), subindustry)` | 网络 | **非线性：标准化偏离**（保留幅度） | 自建 |
| T9 | 网络/任期密度比 | `group_rank(divide(ts_backfill(board_external_connection_count, 120), add(ts_backfill(ceo_tenure_days, 120), 1)), subindustry)` | 网络×任期 | **两字段结构比**（单位任期的社交资本效率） | 自建 |
| T10 | 姓氏集中·market 轴 | `group_rank(ts_backfill(surname_concentration_total_personnel, 120), market)` | 姓氏 | **分组轴（救 SUB 0.14）** | 自建 |

**为什么不是「同一骨架换 10 组参数」**：10 个模板落在 6 个不同维度上 —— 分组轴 4 次（T1/T2/T4/T10）、算子矩 3 次（T5 一阶 / T6 二阶 / T3 覆盖）、非线性时序变换 2 次（T7 / T8）、多字段结构比 1 次（T9）。
**T3 是必需的对照**：backfill 120 → 22 会显著改变覆盖与信息流，是「该字段信号能否被更快捕获」的唯一检验。

---

## 5. 下一步优先级

| 优先级 | 动作 | 依据 |
|---|---|---|
| **P0** | 波 192 收批，按模板族归因，判网络族的时序算子路线是否提得动 S | 网络族 `checks.fail=[]`、`risk_neut_S +1.09`、`DD 7.88%` 是最健康的结构 |
| **P1** | 若 T10 把 SUB 从 0.14 救到 0.5+，则姓氏集中度是**全平台无人挖**的独立维度（2Y 1.90），价值最高 | alphaCount = 0 |
| **P2** | 任期族剩下的 4 个字段（`chairman_tenure_days` / `max`/`median`/`min_chief_officer_tenure_days`）做同骨架扫描 —— 不同字段 = 不同 prod 相关，是低拥挤下的免费分散 | 5 个字段只测了 1 个 |
| **P3** | 治理 flag 族需先做 `ts_mean(F, 252)` 连续化，否则并列退化 | 二元 flag 的秩型陷阱 |
| **P4** | 性别 / 学历族最后考虑（年度级慢变量，与日频结构不匹配） | 低先验 |

---

## 6. 复用警示

1. **别把「流动率族判死」外推成「board_gov_stats 判死」** —— 同集内 5 个族里有 3 个有信号。
2. **别对 `*_tenure_days` 用时序算子**（`ts_delta` / `ts_std_dev` / `ts_rank` 全部退化成二元或常数）。
3. **别用常规「压换手」思路** —— 本数据集 TO 已低至 1.1%，矛盾在 S 与 margin，不在 TO。
4. **`group_rank` / `group_zscore` 会吃掉其内部的一切单调变换**（`signed_power` / `log` / `sqrt` / 内层 `rank`）⇒ rank 内部只允许非单调变换。
5. **覆盖率无陷阱**：46 字段里唯一低于 0.87 的是 `surname_concentration_management`（0.5948），其余全在 0.8775–0.9482 ⇒ 本数据集可放心做全字段笛卡尔积扫描。
