# 从字段画像到产出 Alpha：完整作战思路（Playbook）

> 沉淀自 2026-10-08 会话（DEU 战役 S1.33→1.70 + 13 区画像建成）
> 定位：**长期方法论**，跨区域通用。区域特异实证见各区 skill 的 `profiles:manual` 块与 `RULES.md`。

---

## 全景图（七层链路）

```
第0层 选区域 ──→ 第1层 选字段族 ──→ 第2层 开批前三闸 ──→ 第3层 信号构造
                                                              │
第6层 闸门判定 ←── 第5层 参数微调 ←── 第4层 结构维度（★最大杠杆）
     │
     └──→ 第7层 闭环回填画像 ──→（回到第0/1层，资产复利）
```

**核心心法：链路不是线性的，是「资产复利循环」。每一波实测都回填画像，让下一波的筛选更准。**

---

## 第 0 层：选区域（用画像的 ALIVE 排行定优先级）

**判据**：`field_profile_perf` 的 `ALIVE` 数量 + 未测池规模 + 已测密度。

| 观测 | 含义 |
|---|---|
| ALIVE 多 + 未测池大 | **最优**（该区已验证有效字段多，且还有空间）→ 如 GLB(60 ALIVE / 1.96 万未测) |
| ALIVE 少 + 未测池小 | 已探明（DEU：2 ALIVE / 3,225 未测）⇒ 边际成本高 |
| 已测密度高 | 战役做得深，画像可信度高 |

```bash
$WQ_PY tools/fields/field_profile.py --list          # 一眼看全部 13 区
```

**★ 本会话实证**：DEU 只有 2 个 ALIVE（且唯一有效机制的腿已被占用）⇒ 见底；GLB/IND 各有 60/54 个 ALIVE 且未测池巨大 ⇒ 应优先投入。

---

## 第 1 层：选字段族（画像 verdict + 跨区对照）

### 1.1 九类 verdict 的处置表

| verdict | 判据 | 处置 |
|---|---|---|
| `UNUSABLE` | `coverage < 0.6` | **永久剔除**（DEU 占 77.6%） |
| `AXIS_ONLY` | `ftype == GROUP` | **只能当分组轴**，不进信号白名单 |
| `UNTESTED` | 通过上两关但 `n_tests == 0` | 可探（按机制族排优先级） |
| **`ALIVE`** | 单信号 S ≥ 1.58 | **过闸线 ⇒ 直接可做** |
| `WEAK` | 单信号 S ≥ 1.10 | **有信号但不够强 ⇒ 优先深挖**（本会话 DEU 主战场） |
| `DEAD` | 已测 S < 1.10 | 不再投入 |
| **`DEAD_STATIC`** | `to_med < 0.03` | **静态属性，任何骨架都无用** |
| **`DEAD_TURNOVER`** | `to_med > 0.70` | **被 HIGH_TURNOVER 闸直接拒** |
| **`DEAD_COUNT`** | 名字含 `num/count` 且 2Y≥1.3 且 S≤0.7 | **「2Y 有 S 无」判死形态** |

### 1.2 ★★★ 跨区对照（最强的筛字段手段）

**规则**：同机制在某区是 ALIVE、在另一区未测 ⇒ **优先在对它有效的区做，或回本区补测那个「形式」**。
**★ 但这是「提出假设」，不是结论** —— 见下表第一行 W199 的实测反例。

**本会话三个实证：**

| 发现 | 细节 |
|---|---|
| **★ 跨区可完全失效**（W199 实测） | `predicted_surprise_pct_*`：**EUR S2.06~2.09 ALIVE**，用**同一套框架**在 DEU 实测 **S0.69~1.04（全失败）** ⇒ **同字段同框架跨区可差 1.2~1.3 个 Sharpe** |
| **同机制跨区可反向** | `shortinterest` 在 KOR 是 ALIVE（S2.35）、在 DEU 族级否证（S 全负）；`analyst7` 计数类在 MEA 是 ALIVE、在 DEU 是 DEAD_COUNT |
| **⚠️ 高 S 陷阱** | `*_label*` / `*_bucket*`（分位数/概率桶标签）**不是信号** —— GLB/ASI 的 S4.65/S3.58 多来自此 ⇒ **开批前必核 `fields.description`** |

**★ W199 实测验证（重要修正）**：我曾据此推断「DEU 只测过绝对版，补测 `_pct_` 版就有戏」，
**实测后全部失败（10 条，S −0.12~1.04）**：
`predicted_surprise_pct_f12m_earnings_5` **EUR S2.06 → DEU S0.82**；`..._pct_f12m_revenue_4` **EUR S2.09 → DEU S0.69**。

**⇒ 跨区对照是「提出假设」的工具，不是结论** —— 它能高效指出候选，但**必须实测验证**。
它的价值也包括「**用低成本实验排除一个方向**」。

### 1.3 「字段名骗人」铁律

**必须读 `description`，前缀不可信**（本会话实证）：
- `iv_projected_*` **不是**隐含波动率，是**股息预测 DPS**
- `liquidity_money_flow_alignment` 实为 Relative Turnover
- `volume_anomaly_price_positioning_2` 实为 DPO
- `dl_riskfree_returns` 实为**分位数桶标签**

**★ 另注意**：**后缀判类型会翻车**（`_tribes` 有 MATRIX 也有 VECTOR）⇒ 以 `get_datafields` 的 `type` 为准。

---

## 第 2 层：开批前三闸（零成本，跳过则整批 CANCELLED）

**这一步的价值是「避免整批报废」，成本几乎为零，必须每次执行。**

```bash
# ⓪ 查画像换手：to_med < 0.03（静态）或 > 0.70（闸拒）⇒ 跳过；未测字段用「同族外推」
$WQ_PY tools/fields/field_profile.py --query --region <R> --verdict UNTESTED --limit 40

# ① preflight_expressions（MCP）：校验字段名/类型（含 VECTOR 提示）
# ② op_arity.ensure_safe_for_dispatch(exprs)：校验算子元数
```

**★ 本会话实战价值**：
- `preflight` 拦下 1 个错误字段名（`..._fq1_earnings_14d_5` 应为 `_14d_4`）
- `op_arity` 首次拦下 `group_mean(x, group)` 两参错（应为三参 `group_mean(x, weight, group)`）
- 另新发现：**平台不支持科学计数法**（`1e-6` 报 `Unexpected character 'e'`）⇒ 须写 `0.000001`

**发批工具现状**（`wqb_tools.py dispatch`）已有 **6 道自检**：
`catalog` ｜ `expr-lint`（值型）｜ `field-type-lint`（VECTOR）｜ **`op-arity`** ｜ **`probe-slot`**（探针位闸）｜ `op-lint`

---

## 第 3 层：信号构造（合规形态的骨架库）

### 3.1 铁律：禁混信号

**合规只走 Mode B**：换字段 / 换概念 / 换算子几何 / 换分组轴 / 单信号结构化。

**放行的 5 形态**（必须用满，不可只用一种）：

| 形态 | 表达式 | 经济学含义示例 |
|---|---|---|
| `add`（双窗） | `add(ts_mean(F,1), ts_mean(F,120))` | 快慢双窗：短期变化 + 中期水平 |
| `divide` | `divide(A, B)` | 信息比率、标准化 |
| `subtract(rank,rank)` | `subtract(rank(A), rank(B))` | 相对强弱、**行业内相对** |
| `if_else` / `trade_when` | `trade_when(cond, sig, -1)` | 事件门控、条件筛选 |
| `group_rank` / `group_zscore` | `group_zscore(x, group)` | 组内标准化（非保序 ⇒ 独立杠杆） |

**算子数 < 10**（超了会被判复杂）。

### 3.2 ★★★★ 本会话最大教训：结构维度 > 参数维度

**我最初只扫「参数」（窗长/gran/decay），卡在 S1.33。用户两次质疑后扫「结构」，两次都大突破：**

| 质疑 | 我扫的维度 | 效果 |
|---|---|---|
| 「没用**复杂经济学模板**？」 | 「**行业内相对**」模板 `subtract(rank(SIG), rank(group_mean(SIG,1,industry)))` | 失败项 **2→1**，2Y **+0.31** |
| 「**换算子**看有没有效果？」 | 外层换 `ts_decay_linear` | **S +0.17、F +0.33、sub +0.18**，TO 不变 |

**⇒ 纪律：卡住时，先问「结构维度扫过了吗」，再问「参数扫过了吗」。**

**且**：9 个复杂模板里**只有「行业内相对」有效**（其余 8 个崩到 S −0.77~1.07）⇒ **不是越复杂越好，是找对经济含义。**

### 3.3 无效结构的记录（别重复踩）

| 结构 | 结果 |
|---|---|
| 修正 ÷ 分歧度（信息比率） | S 0.09~1.07 ❌ |
| 修正 ÷ 自身波动 | −0.47 ❌ |
| 修正 × 价格相关（`ts_corr`） | −0.77 ❌ |
| 分歧收敛门（`trade_when`） | −0.01~0.21 ❌ |

---

## 第 4 层：结构维度探索清单（每项独立杠杆）

| 维度 | 扫描范围 | 结论/案例 |
|---|---|---|
| **合成模板** | 双窗 / 差值 / 比率 / 行业内相对 / 门控 … | **「行业内相对」是本会话最大单次增益** |
| **外层算子** | `rank` / `ts_decay_linear` / `signed_power` / `group_zscore` / `winsorize` / `ts_rank` … | **`ts_decay_linear` 大有效**（不牺牲 TO）；`signed_power` 给 2Y 但压 S |
| **残差化轴** | `vector_neut(SIG, rank(axis))` | DEU 实测无效（但它是「改持仓」类杠杆，值得在别区试） |
| **分组轴粒度** | `subindustry` / `industry` / `sector` / `market` | **轴越细 S 越高、PROD 也越高** ⇒ 核心取舍 |
| **分桶变量** | 不同 `ts_mean` 窗 / `ts_std_dev` | 与 gran 联合调 |
| **算子叠加** | `signed_power(ts_decay_linear(...))` | **叠加无效**（2Y 反降）⇒ 单算子最优 |

---

## 第 5 层：参数微调（**必须在结构确定之后**）

**★ 为什么必须在后**：换结构后参数最优值会漂移。本会话的窗长/gran 都是在旧结构（`rank` 外层）下找到的。

| 旋钮 | 对 S | 对 TO | 对 PROD | 结论 |
|---|---|---|---|---|
| **窗长** | **强**（120~150 最优） | 弱 | — | 主 S 旋钮 |
| **桶 gran** | 中（0.015~0.02 是峰） | 弱 | — | 次 S 旋钮 |
| **轴深**（加关系轴） | **负** | 弱 | — | 不要加 |
| **decay** | **极弱**（+0.01） | **强**（0.110→0.065） | — | **换手旋钮，非 S 旋钮** |
| **分组轴粒度** | 细轴更高 | — | 细轴更高 | **取舍型杠杆** |
| `neutralization` 档 | 跌（STATISTICAL 到 0.62~0.81） | — | 真杠杆 | 代价 2Y 塌 |
| `nanHandling` | 几乎不变 | — | — | 是**强度闸**不是风格开关 |
| `truncation` | — | — | — | 多区实测 no-op |

**★ S↔2Y 普遍此消彼长**（本会话每次扫参数都重现）⇒ 找**联合最优**而非单指标极值。

---

## 第 6 层：闸门判定（三层，逐层收紧）

### 6.1 IS 层闸门（平台 checks）

```
LOW_SHARPE ≥ 1.58 ｜ LOW_FITNESS ≥ 1.0 ｜ TO ∈ [0.01, 0.7]
LOW_SUB_UNIVERSE_SHARPE ≥ 0.78 ｜ CLUSTER_TEST ≥ 1 ｜ LOW_2Y_SHARPE ≥ 1.58
```

**★ 判定方法论**：
- **回执/工具输出不可信** —— 任何单点观测只是「上界估计」；提交回执必看 `status=`
- **2Y 检查项名按区域变**（IND 用 `IS_LADDER_SHARPE`）⇒ 先枚举 checks
- **平台把 ladder 四舍五入到 2 位再与 limit 严格比较** ⇒ 真值须 ≥ limit+0.005
- **`sub_universe` 是比值闸**（limit ≈ 0.47 × IS sharpe）⇒ S 高了自动过；不可拿低分批的实测值当墙

### 6.2 判定权威：`submit_verdict`

**唯一否决权威**（只能拦不能放）。`failed_ra: 0` + `failed_ppa: 0` + `sim_fails: []` = IS 层全过。
`UNVERIFIABLE_404` = **处女提交的真实形态，不是 BLOCKED**。

### 6.3 ★★★★★ 相关性双端点（**最容易漏、代价最大**）

```bash
# 必须查两个端点，都取顶层 max
GET /alphas/{id}/correlations/prod     # PROD ≤ 0.70
GET /alphas/{id}/correlations/self     # SELF ≤ 0.70
```

**盲目自信之外的三条铁律：**

1. **一条腿（机制）只产 1 颗** —— 同族一旦提交一颗，该族同持仓变体的 PROD/self 会被推爆。
   **本会话实证**：`58gkLAkk` 提交时 prod 0.5381 / self 0.5153（干净）；**提交后**同机制新候选 PROD 涨到 **0.8037**。
2. **提交前必须双端点复测**（我全程只看 prod、漏了 self ⇒ 这是本会话最大方法漏洞）。
3. **降 PROD 的杠杆分两类，选错会爆 self**：
   | 类型 | 例 | prod | self |
   |---|---|---|---|
   | **改持仓** ✅ | 换残差轴/字段/概念/`trade_when` 分层 | ↓ | 影响小 |
   | **只改时序** ⚠️ | `hump` / `decay` / `ts_mean` 慢化 | ↓↓ | **↑↑ 爆** |

**拥挤层诊断**：换 2–3 种结构 prod 会动（>0.01）= **结构层**（改持仓仍可用）；换 ≥5 种纹丝不动 = **机制层**（弃族）。

---

## 第 7 层：闭环回填（资产复利）

**每批收割后立刻回填画像**，让下一波筛选更准：

```bash
$WQ_PY tools/data-repair/backfill_deu_from_platform.py --region <R> --stage IS   # 平台 → 本地
$WQ_PY tools/fields/field_profile.py --build --region <R>                    # 重建画像
```

**效果**：本会话 DEU 的 `netprofit_y1_estimate_change_3mo` 从 n_sg=3 涨到 188，画像 verdict 从 WEAK 升为 **ALIVE**（字段级证据闭环）。

---

## 五条铁律（贯穿全链路）

| # | 铁律 | 来源 |
|---|---|---|
| 1 | **结构维度优先于参数维度** | 本会话两次大突破都在结构 |
| 2 | **一条腿只产 1 颗**（提交前查双端点 + 目标区该族占用） | `58gkLAkk` 自锁同族 |
| 3 | **画像是「存在性证明」不是「复现证明」** | `avg_estimate_...90d` 画像 2Y1.33、同框架实测 0.63 |
| 4 | **框架与机制耦合，不可跨机制外推** | 同框架对 estimate 族 +0.31、对 anl93 族 −0.38 |
| 5 | **回执/工具输出不可信，只信实测** | 多次踩坑（`ALL SUBMITTED` 实为 400 整批被拒） |

---

## 附：本会话 DEU 完整实战轨迹（作为参照系）

| 波次 | 维度 | 最佳结果 |
|---|---|---|
| W170 | 同机制新载体探针 | S1.33 |
| W171–W172 | 轴深 + 窗长 + gran | S1.45 |
| W173 | decay | S1.46 |
| W174 | 换字段 | 失败（1.24） |
| **W175/W176** | **★ 合规模板「行业内相对」** | **S1.49 / 2Y1.61 / 失败项 2→1** |
| W177/W179 | gran 细扫 | S1.52 |
| **W180/W181** | **★ 算子 `ts_decay_linear`** | **S1.69 / F1.52 / sub1.05** |
| **W184** | 窗 × gran × d 联合 | **S1.64 / 2Y1.59 / 0 失败项** 🎉 |
| W185–W191 | 降 PROD（换轴/换 universe/中性化档） | PROD 0.8037 → 0.763，但 S 掉到 1.54 |
| W192–W198 | 换腿/换机制/新机制族 | 全部失败 ⇒ 确认 DEU 见底 |

**⇒ 从 S1.33 到「IS 全闸通过」共 15 波；两个决定性跳跃都来自「结构维度」。**
