# GLB 战役续篇报告 —— 提交收尾 + 新腿侦察 —— 2026-10-14

> **结论（三点）**
> 1. **dlrr/mdl239 腿已采尽**：`RR66gp2j` 提交后成为该腿第 1 颗（也是唯一可提交的 1 颗）；其余 3 条同腿近亲被 prod 相关推高至 0.86–0.89，**永久不可提交**。
> 2. **两个新腿候选数据集探针全灭**（`other327` 利率敏感度、`institutions6` 机构持仓流量）。
> 3. **★ 关键区域级发现**：GLB 的子区域闸（AMER/EMEA/APAC）本质是「**子区域有效信号闸**」，不是单纯的「覆盖闸」——`institutions6` 覆盖率 1.0、APAC 持仓 4400+ 只，APAC Sharpe 仍 ≈ 0。

---

## 1 提交终局（以 `get_alpha_details` 平台复核为准，非工具回执）

| 候选 | 设置 | 提交前 prod | **当前 prod** | 判定 |
|---|---|---|---|---|
| **`RR66gp2j`** | SUBINDUSTRY / decay10 / θ0.75 | 0.6331 | — | ✅ **ACTIVE**（`GLB_R_dlrrGate_01`，2026-10-08T04:03-04:00） |
| `omWWbQG5` | MARKET / decay10 / θ0.75 | 0.6436 | **0.89** | ❌ 挂（≥0.7） |
| `e7QQYeG6` | MARKET / decay10 / θ0.80 | 0.631 | **0.857** | ❌ 挂（≥0.7） |
| `P0ggRjYq` | MARKET / decay10 / θ0.65 | 0.8188 | 排队 | ❌ 早前已挂 |

**机制**：`omWWbQG5` 与 `RR66gp2j` 的表达式**逐字相同**（仅中性化 SUBINDUSTRY↔MARKET 之差），是同腿最极端情形。`RR66gp2j` 一旦 ACTIVE 进入生产池，同腿近亲的 prod 立刻被推过 0.7。

**与既有铁律吻合**：
- `SELF-CORR-FAMILY-CANNIBALISM`：该族已有 ACTIVE 后，同骨架变体默认判死。
- `SIGNAL-STRENGTH-AND-CROWDING-ARE-ONE-COIN`：GLB prod 检查实测集中在 **0.8174–0.8778**——本次 0.89 / 0.857 正落该区间。

⇒ **结论：一条腿只出 1 颗。** 该腿产出 = `RR66gp2j`（+ 账户此前同族 ACTIVE），无残余可提。

---

## 2 新腿侦察（2 组各 10 结构探针）

### 2.1 `other327` Sensitivity to Interest Rates Model —— **死**
- 字段：`oth327_sirc_lev`（曲线水平敏感度）、`oth327_sirc_sl`（曲线斜度敏感度），均 VECTOR，coverage 0.96，alphaCount 27/33（极低拥挤）。
- 域：美债利率敏感度 / 久期 —— 与 dlrr（收益预估）、mdl239（借贷）正交。

| 表达式（示例） | S | TO | 2Y | AMER | EMEA | **APAC** | CW |
|---|---|---|---|---|---|---|---|
| `-rank(vec_avg(lev))` | 0.22 | **1.02** | −0.40 | 0.43 | −0.31 | **0.18** | **1.0** |
| `rank(ts_delta(vec_avg(sl),20))` | 0.33 | 1.02 | 0.70 | 0.59 | 0.02 | **−0.24** | 1.0 |
| `subtract(rank(lev),rank(sl))`（最优） | **0.48** | 1.01 | 1.82 | 0.37 | 0.25 | **0.25** | 1.0 |
| `rank(ts_zscore(vec_avg(lev),60))` | −0.53 | 1.04 | −1.98 | 0.13 | −0.41 | **−0.64** | 1.0 |

**三面墙同时成立**：① APAC Sharpe 全体 ≈0（−0.64 ~ +0.25）；② 换手 ≈1.0（硬闸 0.7）；③ CW=1.0 单日爆表（2023-04-27）。

### 2.2 `institutions6` Institutions and Beneficial Stake Ownership —— **死**
- 字段：11 个（机构买入/卖出市值、买卖家数、持仓市值/股数），coverage 1.0，alphaCount ~500。
- 域：13F 型机构头寸流量 —— 正交。

| 表达式 | S | TO | 2Y | AMER | EMEA | **APAC** | 持仓 |
|---|---|---|---|---|---|---|---|
| `subtract(rank(买入值),rank(卖出值))`（最优） | **0.54** | 0.010 | 0.55 | 0.84 | 0.39 | **−0.25** | 4361/4529 |
| `rank(divide(机构持仓值,cap))` | 0.39 | 0.010 | 0.25 | 0.65 | 0.37 | **−0.32** | 4367/4522 |
| `rank(买入股数)` | 0.33 | 0.014 | 0.25 | 0.50 | 0.06 | **+0.04** | 4467/4423 |
| `-rank(机构持仓值)` | −0.62 | 0.007 | −0.77 | −1.01 | −0.43 | +0.22 | 4475/4415 |

**核心观察**：**持仓覆盖 4400+ 只（含 APAC），但 APAC Sharpe 全体 ≈0**，AMER 最高仅 0.84、EMEA 0.39，均远低于闸线 1.0。

### 2.3 已排除候选（不占配额）
| 数据集 | 排除理由 |
|---|---|
| `pv98` Intraday Tick | 字段实为 OHLCV + 滞后价（`close_price_current_day_lagged_0/1/2`），与 pv1 冗余；描述「market-implied fundamentals」名不副实 |
| `risk66` VEI risk model | 仅 2 字段且均为市值聚合（`*_cap_usd`）⇒ 无信号 |
| `risk68` Forecast Data | 字段描述明写 "for a European asset / European instruments" ⇒ 非全球，APAC 必不足 |
| `risk60` Securities Lending | 与 `model239` 同域，按跨域铁律 `GLOBAL-CROSS-DATASET-SAME-DOMAIN-LOCK` 互锁 |

---

## 3 ★ 关键发现：GLB 的 APAC 墙 = 「子区域有效信号闸」

原「覆盖闸」假说（来自 `hiring_trends` APAC 仅 9 只、`option_chart_model` 稀疏）**被本轮部分修正**：

- `institutions6` 覆盖率 **1.0**、APAC 持仓 **4400+ 只**（远超 model239 的 1905/953），APAC Sharpe 仍 **≈ 0**。
- ⇒ **coverage = 1.0 只能保证「有票」，不能保证子区域过闸。**

**判据升级**：只有「底层数据由**全球统一过程**生成」的类才有 APAC 有效信号——
1. **价格/成交量派生类**（dlrr 图表 OHLCV 派生、techindi 类）；
2. **全球借贷台类**（model239 / risk60 证券借贷）。

而**地域偏置类**（13F 机构持仓、利率久期、招聘、期权）在 APAC 无预测力。

---

## 4 结论与建议

**GLB regular 对当前账户实质饱和**：
- 可提交腿仅两类：① 价格/成交量派生类（= dlrr 已出 1 颗，且 prod 高度拥挤）；② 证券借贷类（与 model239 同域互锁，不可新增）。
- 本轮新腿侦察的 2 个正交候选均因 **APAC 无有效信号** 判死。

**建议路径（三选一，待用户定夺）**：
1. **接受 GLB 收官**：账户 GLB ACTIVE = 7（同族），本季不再新增；把配额转向 APAC 有效信号更丰富的区域。
2. **深挖价格/成交量派生类的正交变体**：唯一有 APAC 信号的域，但需先测与已提交 7 颗的持仓重叠（预期同腿风险高）。
3. **换子区域组合**：若平台允许，绕过 GLB 三区闸（需用户确认是否越界）。

---

## 5 落盘记录
- `upsert_registry_empirical`：
  - `GLB / campaign / other327`（status=exhausted + finding/rule/alpha_ids 10 颗）
  - `GLB / campaign / institutions6`（status=exhausted + finding/rule/alpha_ids 10 颗）
  - `GLB / cross_region / SUBREGION-SIGNAL-NOT-COVERAGE-GATE`（跨区铁律）
- 探针 20 颗 alpha id 见 registry payload（属探针批，不入 salvage 池）。
