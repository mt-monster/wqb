# KOR 破闸工作流管线（可复用 SOP，2026-10-15 定稿）

> 把「S0 选集 → S1 体检 → S2 归因 → S3 破闸 → S4 算子穷举 → 终验」固化成一条标准管线。
> 每一步都给「输入 → 动作 → 判定 → 产物」。**勿再即兴。**

---

## 0 流程总览

```
S0 选集     低 alphaCount 优先（prod 墙代理）→ 解析 code 前缀排除已点亮数据集
   ↓
S1 六法体检  先离线包（KOR 85% 退化 ⇒ 多数要在线六法）；先看分布再写表达式
   ↓
S2 归因     时期归因 + raw vs risk-neutralized 分解 → 判「因子暴露」还是「信号衰减」
   ↓
S3 破闸     每闸一根杠杆，单变量对照（杠杆图谱见 §3）
   ↓
S4 算子穷举  对照 103 算子目录，覆盖未试家族
   ↓
终验       prod/self 实测 + Phase C 反过拟合 → 提交权归用户
```

---

## 1 S0 选集

- **判据**：`alphaCount`（prod 墙密度最可靠代理）低拥挤优先，**不是**高 valueScore。
- **已点亮判定**（数据集级，勿改口径）：`get_user_alphas(region, stage=OS, status=ACTIVE)` → **解析 `code` 字段前缀**归组计数（`results[].datasets` 在 KOR 为空）。
  ⚠ `get_user_alphas` **不支持** `order=-sharpe`（400）⇒ 只能 `-dateCreated`，自己排序。
- **产物**：`<repo>/logs/_kor_s0_whitelist.json`（评分脚本 `$WQ_PY tracking/KOR/scripts/kor_s0_scan.py`）。

---

## 2 S1 六法体检（先离线后在线）

**离线优先**：`tracking/mining/field_inspect_<region>_<ds>.json`。
⚠ **KOR 离线包 85% 退化**（skew/kurt/freq/shape 全 null）⇒ 根因 = WebData 包 `dataSetList.json` 里 KOR 只有 1 个组合 ⇒ **绝大多数 KOR 数据集必须走在线六法**。

**在线最小集**（每字段 6 条仿真，`Neutralization=None`/`Decay=0`/`P0Y0M0D`）：

| 法 | 表达式 | 判读 → 决策 |
|---|---|---|
| 1 覆盖 | `F` | cov<0.4 → **必须** `ts_backfill` |
| 2 非零 | `F != 0` | 与法 1 差值大 = 稀疏事件型 → `trade_when` 门控，**禁裸 rank** |
| 3 频率 | `ts_std_dev(F,5/22/66) != 0` | 季频 ⇒ 窗口 ≥63d；⚠ 短窗可能被 NaN 污染 ⇒ 频率读数不可信时按季频保守取 252 |
| 4 范围 | `abs(F) > 1/10/100` | 量纲跨度大 → `rank`/`ts_zscore`；有界 [-1,1] → 直接 `rank` |
| 5 **中心趋势** | `ts_mean(F,252) > 0` | **★ 单边恒正（>90% 恒正）⇒ 禁裸水平做多空，取 `ts_delta` 变化率** |
| 6 形态 | `zscore(F) > 0/1` | 近正态 ⇒ 无预处理；`zero_inflated`/`point_mass` ⇒ 事件门控 |

**铁律 A（体检校正）**：单边恒正 + 有界小量纲 ⇒ 禁裸水平，取变化率（窗口 252 优于 66）。
**铁律 B**：方向必须正反各测一条（`reverse()` 与正向**不精确反号**，截断+decay 与符号交互）。
**VECTOR 必先套 `vec_*`**（否则裸用报错）。

---

## 2.5 ★ S1.5 字段 → 表达式组装（骨架怎么用，本段新增）

> **体检做完，不是直接回测。先把字段按体检结论「装进骨架」，再发批。**

### 2.5.1 骨架的两层结构（先分清「核心信号」vs「壳层」）

```
ALPHA = vector_neut( trade_when(greater(rank(adv20), 0.1),            ← 壳层②：流动性门控
              tail(group_rank(group_neutralize(核心, sector),        ← 壳层③：行业去均值 + 市值分桶排名
                   bucket(rank(cap), range="0,1,0.25")),
                   lower=0.3, upper=0.7, newval=0.5), -1),            ← 壳层④：尾部裁剪
        power(rank(rsk68_weight_dadv), 0.85) )                        ← 壳层①：美元流动性轴残差化
```

| 层 | 作用 | 何时动它 |
|---|---|---|
| **核心信号** | 真正的 alpha 源（峰度×反转等）| **换字段/换概念时动** |
| 壳层① `vector_neut(·, dadv)` | 剥离流动性暴露，抬 investability | pow 幂次调保留率 |
| 壳层② `trade_when(adv20>0.1)` | 流动性过滤门 | **门控阈值别动**（0.1 最优，调高崩 S）|
| 壳层③ `group_neutralize(·, sector)` + `bucket(rank(cap))` | 剥行业暴露 + 市值分桶 | **sector 中性化是把 IS 推全过的关键** |
| 壳层④ `tail(..., 0.3, 0.7, 0.5)` | 尾部裁剪，压极端 | 0.2/0.8 → 0.3/0.7 纯改善 |

**核心教训**：**别把「壳层」当「信号」**。本轮实证：只换核心字段、壳层不动 ⇒ S 崩；只调壳层、核心不动 ⇒ 能把 IS 推到全过。

### 2.5.2 核心信号怎么组装（单字段 → 三腿乘积）

KOR 唯一活的核心构型（pv47 峰度族）：
```
multiply(rank(multiply(-1, ts_kurtosis(X, 140))),      ← 腿1：尾部风险反向（140 日峰度）
         rank(multiply(-1, ts_rank(X, 132))),          ← 腿2：中期反转（132 日排名）
         rank(multiply(-1, ts_rank(X, 252))))          ← 腿3：长期反转（252 日排名）
```

| 规则 | 原因 |
|---|---|
| **三腿缺一不可** | 单腿 0.89 崩（去掉一条就掉到 S<1）|
| **峰度腿不可替换** | 换 `ts_std_dev`（波动率版）2Y 差 0.13；换 `ts_max_diff`（回撤版）崩；全换 std_dev 崩 |
| **同字段多时间窗 = 单信号结构化** | 合规（`ts_kurtosis/ts_rank` 同字段不同窗口，不属混信号）|
| **rank 乘积 = 横截面排序** | 每个 `rank(multiply(-1, ...))` 把一条腿归一到 [0,1]，乘积取三腿共振 |

### 2.5.3 多字段组合（合规三形态，**禁混信号**）

| 形态 | 合规性 | 实证 |
|---|---|---|
| `trade_when(条件, 信号, -1)` / `if_else` | ✅ 放行 | pv47×fnd44 **组合实测崩**（AND 门 S 0.57 / if_else S 0.81）|
| `subtract(rank(A), rank(B))` 同源 | ✅ | 价差腿不带系数 |
| `divide` / `ts_corr` 同源 | ✅ | — |
| **`add/multiply` 两不同字段相加** | ❌ **违规**（混信号）| **禁** |

**⚠ 跨字段组合的正确入口**：不是相加，而是**条件门控**（`trade_when` / `if_else`）。
且**条件字段与被控字段必须机制正交**（pv47 日频防御 × fnd44 季频质量，属性差太远 ⇒ 实测稀释）。

### 2.5.4 方向怎么定（铁律 B 的落地）

- **不要靠 description 猜方向**（`icfroe_5y` 猜正向 → 实测 −0.62）。
- **新字段族首波正反各测一条**：`reverse(ts_delta(F, 252))` 与 `ts_delta(F, 252)` 各一条，取优。
- **`reverse()` 与正向不精确反号**（截断 0.08 + decay 与符号交互）⇒ 推断只能当线索，**必须真跑**。

### 2.5.5 组装顺序（从上往下装，别反过来）

```
① 核心信号（字段 + 时序变换）   ← 决定信号强弱
② 壳层③ group_neutralize(sector) + bucket(rank(cap))   ← 剥行业暴露（推 IS 全过的关键）
③ 壳层④ tail(0.3, 0.7, 0.5)     ← 尾部裁剪
④ 壳层② trade_when(adv20>0.1)  ← 流动性门控
⑤ 壳层① vector_neut(·, dadv)   ← 美元流动性轴残差化（pow 0.80–0.85 甜蜜区）
```

**⚠ 顺序敏感**：`group_neutralize` 必须在 `group_rank` **之前**（先剥行业再排名）；`tail` 在 `group_rank` **之后**。
装反了（如把 group_neutralize 放 group_rank 外）⇒ 语义改变，S 崩。

### 2.5.6 本族可直接套用的「成品骨架」

```
vector_neut(trade_when(greater(rank(adv20), 0.1),
  tail(group_rank(group_neutralize(
    multiply(rank(multiply(-1, ts_kurtosis(<X>, 140))),
             rank(multiply(-1, ts_rank(<X>, 132))),
             rank(multiply(-1, ts_rank(<X>, 252)))), sector),
       bucket(rank(cap), range="0,1,0.25")), lower=0.3, upper=0.7, newval=0.5), -1),
  power(rank(rsk68_weight_dadv), 0.85))
```
设置：`KOR / TOP600 / D1 · decay 3 · REVERSION_AND_MOMENTUM · trunc 0.08`
实测：`X = pv47_for_statssimple_only_spret` → **S 1.99 / F 1.10 / 2Y 1.91 / failed_ra=0**（`E5VAZ5pr`）。

**适用前提**（先体检再套）：X 是**日频收益分布型**字段（有连续分布、非单边恒正）。
若 X 是**季频/单边恒正**（如 fnd44 类）⇒ 别套本骨架，先按 S1 体检映射改走 `ts_delta` 变化率路线。

---

## 3 S3 破闸杠杆图谱（每闸一根，全部实测）

| 闸 / 症状 | 杠杆 | 实证（pv47 族）|
|---|---|---|
| 报告期塌陷 | **先 raw vs RN 分解** | RN≫raw ⇒ 因子暴露 → 换中性化档 |
| **中性化档** | **REVISION_AND_MOMENTUM 全族最优**；**换族必重扫 11 档** | MARKET→REVMOM：failed_ra 3→2 |
| LOW_FITNESS | tail 收紧（0.2/0.8→0.25/0.75）**纯改善** | 0.92→0.95 |
| IS_LADDER（2Y）| **decay 降**（S↔2Y 权衡，**峰值在 decay=3**）| d3 给 2Y 1.58 |
| **IS 推全过** | **★ group_neutralize(·, sector)**（剥行业暴露）| **F 0.98→1.10、2Y 1.56→1.91、failed_ra 2→0** |
| INVESTABILITY | vector_neut 幂次 0.5→0.85；**pow ≥0.9 触发 ladder window 2→4 跳变，2Y 崩** | 0.80–0.85 甜蜜区 |
| prod | **n 判据**：`[0.7,0.8)` 桶 n≥1 ⇒ **密墙，别扫窗口**；n=0 ⇒ 扫 W | 本族 n=3 ⇒ 封顶 |

**F 公式反推缺口**：`F = S × √(returns / max(TO, 0.125))` ⇒ 缺口归属 S / TO / returns 哪一档。

---

## 4 S4 算子穷举

对照 103 算子目录，覆盖未试家族。**正确顺序 = 先中性化/分组轴，再时序平滑，最后幂次**。

| 算子 | 实测效果（pv47 族）|
|---|---|
| **group_neutralize(sector)** | **★ 突破**：F 0.98→1.10、2Y 1.56→1.91、failed_ra 2→0 |
| group_zscore | **有害**（2Y 崩到 1.02）⇒ 剥行业有效、标准化有害 |
| signed_power | **no-op**（rank 积上无效）|
| ts_mean / ts_decay_linear | **毁 S**（1.79→1.35/1.50）⇒ 时序平滑在本族有害 |
| trunc 0.06 vs 0.08 | **完全等价**（no-op）⇒ 可删 |

**算子覆盖图**：已实测 ts_kurtosis/ts_rank/rank/vector_neut/tail/group_rank/group_neutralize/group_zscore/bucket/trade_when/power/signed_power/reverse/multiply/ts_delta/ts_mean/ts_decay_linear。
**未覆盖但与缺口相关**：ts_corr/ts_regression（第二时间尺度）、ts_arg_max/min、if_else、normalize、ts_scale——**但这些对「IS 全过 + prod 墙」格局无新杠杆 ⇒ 别继续在族内穷举**。

---

## 5 终验

- `check_correlation(alpha_id)`（prod）+ `check_self_correlation(alpha_id)`（self，本地不占配额）。
- **Phase C 反过拟合**（`brain-alpha-robustness`）：Recent-3yr 强度 / CV_Sharpe / 衰减比 / 平年 / max-min 比。
- **prod n 判据**：`[0.7,0.8)` 桶 n≥1 ⇒ 结构性密墙。
- **提交权归用户**（`worldquant-submit-alpha` 确认后才走 `POST submit`）。

---

## 6 当前 KOR 结算（2026-10-15 终局）

| 项 | 状态 |
|---|---|
| IS 全过候选 | **2 颗**：`E5VAZ5pr`（S1.99/F1.10/2Y1.91）、`A1Qd18Kd`（S1.97/F1.11/2Y1.90）|
| prod | 0.7446 / 0.7497（n=3 密墙，结构性）|
| self | 0.26（干净）|
| Phase C | CONDITIONAL（CV 0.485 / 衰减比 0.43，均落条件带）|
| **结论** | **强信号与 prod 白空间互斥**：pv47 IS 强但 prod 拥挤；fnd44 prod 干净但 S 天花板 0.93。**KOR 单独封顶，全破需换 region 或机制正交第二族。** |

---

## 7 工程坑（本轮新增）

1. **batch 工具 `nan_handling` 参数被静默忽略**（提交 ON、回读恒 OFF）⇒ 该维度不可经此工具调。
2. **比较不同 pow 的 2Y 必须先核对 ladder window 是否同档**（pow≥0.9 把 window 2→4），否则比较无效。
3. **长批后 `lookINTO` 报 HTTP 401** ⇒ `authenticate` 重认证即恢复。
4. **trunc 0.06/0.08 完全等价** ⇒ 做算子压减时可安全删除其一。
5. **`performance_comparison` 不是风险因子归因工具**（端点是 merged performance check）⇒ 风险因子暴露归因子走 `get_alpha_pnl` 的 `risk-neutralized-pnl` 列。
