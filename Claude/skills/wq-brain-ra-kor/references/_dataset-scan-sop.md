# KOR 数据集筛选与字段画像 SOP（可复用）

> 2026-10-15 战役产出。适用于任何「KOR 全量扫数据集 → 选白名单 → 字段画像 → 开波」的循环。
> 配套脚本（**在仓库根执行**，`$WQ_PY` = `world-quant-brain-mcp/.venv` 的解释器）：
> `$WQ_PY tracking/KOR/scripts/kor_s0_scan.py`（评分）、`$WQ_PY tracking/KOR/scripts/kor_pool_rank.py <dump.json>`（候选池按剩余闸排序）。
> ⚠ 脚本不在技能目录里：它们读仓库内的 `template_families.json` / `tracking/KOR/reference/*.json`，
> 装到 `~/.claude/skills` 的副本跑不通（2026-10-15 起脚本已迁出技能目录，现居 `tracking/KOR/scripts/`）。

---

## 0 前置：已点亮判定（用户定义，勿改口径）

> **「已点亮」= 某数据集下已提交 ≥3 个 alpha。**

- 判定数据源：`get_user_alphas(region="KOR", stage="OS", status="ACTIVE")` → 解析 `code` 里的字段前缀 → 按数据集归组计数。
  ⚠ `results[].datasets` 字段在 KOR 返回为空，**必须解析 `code`**。
- 2026-10-15 快照：`shortinterest38`=5、`other466`=5 ⇒ 已点亮，排除。
- ⚠ **排除是数据集级，不是塔级**。KOR 的 FUNDAMENTAL 塔整体被 `other466` 点亮，但 `fundamental90`/`fundamental44`/`other395`/`other452`/`other401` 仍可选。

---

## 1 数据集评分模型

```
score = 2 × valueScore
      + 覆盖甜蜜区(0.35–0.97 → +1.5；<0.30 → −3.0；>0.97 → −0.5)
      + 字段富集度(≥20 → +2.0；≥8 → +1.5；<3 → −2.5)
      + 拥挤度反向(alphaCount ≤20 → +4；≤200 → +3；≤600 → +1.5；≤1500 → +0.5；≤3000 → −1；>3000 → −3)
      + 冷门度(userCount ≤10 → +2；≤60 → +1.5；≤300 → +0.5；>300 → −1)
```

**为什么这样加权**：`alphaCount` 是 **prod 墙密度最可靠的单因子代理**。
依据：d219–d232 战役在 5 个数据集造出 IS 全闸候选（S 1.5–2.5），prod 仅 `shortinterest38` 过关（0.60–0.67），其余一律 0.81–0.89。
⇒ **选集时先估 prod 拥挤度，再投入回测配额。** 高 alphaCount 数据集即使 IS 好看也难提交。

---

## 2 KOR 已排除清单（勿重复劳动）

| 类型 | 数据集 | 理由 |
|---|---|---|
| 已点亮 | `shortinterest38`、`other466` | 各 5 颗提交 |
| 字段数 <3 | `macro63`/`other100`/`socialmedia39`/`univ1`/`pv14`/`pv149`/`fundamental4`/`imbalance5` | 无法建多腿正交组合 |
| 结构性退化 | `other106`(KOSPI 成分 cov0.404 近静态)、`shortinterest5`(涨跌停，KOR 不适用→常量)、`pv29`(估值金字塔重复) | 实测 S ≤ 0 |
| 已知死族 | `pattern_scores`、`continuation_score` | 图表形态族三连死（RULES §G）|
| 饱和 | `pv1`(87k)、`fundamental23`(7.5k)、`dl_riskfree_returns`(7k)、`risk70`(7.9k) | prod 密墙 |
| 低频近静态 | `insiders5`(TO<0.31)、`fund_holdings_panel`(TO<0.1)、`pv37` | KOR 日频活跃信号源极少 |
| 双构型全灭 | `sentiment27`、`pv30` | d233–d235 |

---

## 3 字段画像：按 description 聚类，不按名字

**铁律（项目级）**：`description` 是唯一语义依据，字段名/数据集名会骗人。
KOR 实证：`analyst_count` 前缀横跨 151 个 desc 族；`fundamental90` 与 `other401` 字段名几乎相同（都是 `*_game_*`）但是**两个不同数据集、不同覆盖**。

### ★★★ 3.0 【必做前置】字段体检六法 —— 不可跳过

> 论坛两帖共识 + 项目 skill 实现。**先体检，再写表达式。**
> 源：①《📄 读一个数据字段,该看哪几项》(DA98440, 37赞) ②《【方法】新数据字段的快速评估：6 个表达式看清一个字段》(LL46807, 22赞)
> 项目实现：`skills/brain-datafield-exploration-general`（六法完整实现）+ `skills/brain-dataset-exploration-general`（数据集级审计）

| 法 | 表达式 | 读数 | 映射决策 |
|---|---|---|---|
| 1 覆盖 | `F` | Long+Short / 池大小 | cov<0.4 → **必须** `ts_backfill` |
| 2 **非零覆盖** | `F != 0` | 与法 1 差值 | 差值大 = 大量 0 ⇒ **稀疏事件型** → `trade_when` 门控 / 事件门控，**禁裸 rank** |
| 3 更新频率 | `ts_std_dev(F, N) != 0`，N=5/22/66 | N 越大越易为真 | 日频：三者都≈覆盖；季频：N=66 才≈覆盖 ⇒ **窗口下限** |
| 4 取值范围 | `abs(F) > X`，X=1/10/100 | 逐档放大至归零 | 量纲跨度大 → `rank`/`ts_zscore`；有界[-1,1] 评分型 → 直接 `rank` |
| 5 中心趋势 | `F + 1`、`rank(F)` | 量级与偏移 | **★ 单边恒正（如 skew≈+0.99）⇒ 禁原始水平做多空**，先 reverse / 取变化率 / 与基准差 |
| 6 分布形态 | 直方图 + 分位数 | 厚尾 / 稀疏 / 零值 | `zero_inflated` / `point_mass` ⇒ `ts_backfill` 或事件门控 |
| 7 **数据集归属** | 查命名空间 | 是否同源 | **同源字段相关性天然高，别当两个独立信号用** |

⚠ **VECTOR 必须先套 `vec_*` 再评估，否则测出来全是误导**（论坛明文 + 本项目 `dataType` 铁律）。

**体检设置**：`Neutralization=None`、`Decay=0`、Test Period `P0Y0M0D`；只看 IS Summary 的 Long/Short Count。
**成本**：单字段全六法 ≈ 6 条仿真（一批）。**别对整个数据集逐字段全跑** —— 只对 dataset-exploration 抽出的 Top-N 跑。

#### ⚠ KOR 的结构性约束：离线体检包 85% 退化（2026-10-15 实测）

`tracking/mining/field_inspect_kor_*.json` 共 1333 字段，**1126 个（85%）标记 `_degraded`**
（`skewness`/`kurtosis`/`frequency`/`distribution_shape` 全为 null）：

| 数据集 | 字段数 | 退化 | 元数据 |
|---|---|---|---|
| `analyst25` | 207 | **0** | ✅ skew/kurt/freq/shape 全有 |
| `fundamental17`/`other395`/`other466`/`shortinterest38`/`risk70`/`model56`/`other106` | 1126 | **全部** | ❌ 仅 `coverage_ratio` |

**根因**：WebData 包 `research-data/WebData_20260219_V0.10.9` 的 `dataSetList.json` 里
**KOR 只有 1 个组合**（`analyst25_KOR_TOP600_Delay1`）。其余数据集不在包内 ⇒ 生成器取不到 bin ⇒ 退化。
生成器入口：`tools/webdata_quality.py --zip <pack> --region KOR --fields <ds> --export-expr <out>`。

⇒ **KOR 绝大多数数据集必须走在线六法**（每字段 ≈6 条仿真）。这是 KOR 与其它区的差别，别以为「查离线包」能免掉体检。
⇒ 唯一完整包 `analyst25` 的 `advices` 字段可直接消费，样例：
`anl25_adj_oper_p_max` → 「单边恒正(正值0.99) → 勿用原始水平做多空，先变化率/排名/与基准差」+「大量 0 值(>50%) → 配合 ts_backfill 或事件门控」+「季度频率 → 时序窗口≥63d」。
**这三条正是「模型评分类为什么全灭」的判据 —— 事前可预判，不必事后烧 8 个槽位才发现。**

### 3.1 命名 → 语义解码表（KOR 财务类通用）

| 命名模式 | 语义 |
|---|---|
| `*_d1_current_t` / `current_t` | **已自带时序标准化**的 t 统计量 → 裸 rank，**不要再套 ts_zscore** |
| `*_d1_dts` | 历史标准差（波动）→ reverse |
| `*_d1_mean/_max/_min/_length` | 历史分布统计 |
| `*_d1_accum_4q` | 四季累加（持续性） |
| `*_d1_asset_change` / `*_double_history` / `*_half_history` | 资产扩张速度（经典异象）→ reverse |
| `*_accrual_pct_*` | **可自由裁量应计占比**（舞弊核心）→ reverse |
| `*_accrual_r2_*` | 回归 R²（盈余管理代理）→ reverse |
| `*_nondiscretionary_*` | 非裁量应计 → 直取 |
| `*_score` / `*_probability` / `*_percentile` | **离散评分** → 禁 `winsorize`/`signed_power` |

### 3.2 机制 → 模板映射

| 字段形态 | 模板 | 依据 |
|---|---|---|
| 已自带标准化（`current_t`/percentile） | 裸 `group_rank(reverse?(F), 轴)` | 重复标准化杀信号 |
| 慢变水平比率（季频） | `ts_backfill(F, 252)` + `bucket(rank(cap))` 分组 | 不回填 NaN 过多 |
| 离散评分 | 禁 `winsorize`/`signed_power` | 无连续尾部 |
| 同向语义多模型 | `subtract(rank(A), rank(B))` **同源减法造分歧** | 同数据集 ⇒ 合规 |
| 正/反向计分对（mscore vs pscore） | `add(rank(A), rank(B))` 等权叠加 —— ⚠ **这是全局混信号 POISON 闸的违规形态**（`skill_lint` 的 `equal_weight_leg_add` 会拦），唯一可论证的例外是「同一机制的正反两套计分」，**用前须用户裁决、不得当默认模板** | d274c：rank 组合 S +56% |

---

## 4 ★★★ 本区三条新铁律（2026-10-15，48 结构实证）

### 铁律 A：「模型评分」类的默认构造是「变化率」，不是「水平值」
⚠ **旧版写「取值近乎二值 ⇒ 截面无区分度」，已被六法体检实测推翻（2026-10-15）。**
`fundamental44` `fnd44_mscore` 体检（17 条仿真，`reports/field_check_fundamental44_20261015.md`）真实读数：

| 法 | 实测 | 判定 |
|---|---|---|
| 法 2 非零 | 与法 1 **完全相同（312=312）** | **零占比 0 —— 不是二值**（旧版判断错误）|
| 法 6 形态 | `z>0` **52.2%**、`z>1` **16.4%**（参考 50%/15.9%）| **截面区分度充足、近正态** |
| 法 4 范围 | \|x\|≤0.4，**74% 在 ±0.1** | 有界小量纲 + 大量并列 ⇒ 裸 `rank` 信息量低 |
| **法 5 中心** | 年均值>0 占 **92.6%** | **★ 单边恒正 —— 真死因** |

**构造翻证**：裸水平 `reverse(ts_backfill(F,252))` S≈0 → **`reverse(ts_delta(F,252))` S 0.70 / F 0.40 / 2Y 0.29**（PPA 仅差 LOW_SHARPE）。
`ts_delta(66)` 0.31 ｜ `ts_zscore(252)` **0.22（时序标准化无效）** ｜ `ts_delta(22)` 0.09（短窗失效）。

⇒ **正确表述：「单边恒正 + 有界小量纲」，不是「无区分度」。** 与 `analyst25` 体检包 advice 完全一致。
⇒ **该族 12 字段同构 ⇒ 先批量跑 `reverse(ts_delta(F,252))` 一轮再谈判死。**
⚠ **元数据 coverage 不可信**：元数据 0.8984 vs **实测 0.490**（高估 1.8 倍）。
⚠ **法 3 短窗失效**：`ts_std_dev(F,5/22/66)` 非单调（492/313/497）⇒ 被 NaN 污染，**频率读数不可信**。

### 铁律 B：方向必须实测，不能靠语义推断
| 字段 | 按 description 猜的方向 | 实测 S | 正确方向 |
|---|---|---|---|
| `fnd90_qes_gamef_icfroe_5y` | 正向 | **−0.62** | reverse |
| `fnd90_game_receivable_days` | reverse | **−0.36** | 正向 |
| `fnd90_game_cash_flow_coverage` | 正向 | +0.31 ✅ | 正向 |
| `oth452_deferred_tax_liability_11` | reverse | +0.26 ✅ | reverse |

⇒ **任何新字段族，首波必须正反双向各测一条**（成本 2 槽，省一整轮 6–8 槽）。
⇒ ⚠ **加强版（2026-10-15 实证）：`reverse()` 与正向不是精确反号，不能用推断代替实测。**
`fundamental44` 实测：`jones_cf_accruals` reverse **−0.31** vs 正向 **+0.23**；`score` **+0.05** vs **−0.12**。
（原因：truncation 0.08 + decay 4 与符号交互。）⇒ **正反两条都必须真跑。**

### ★ 铁律 D（2026-10-15 新增）：**同族多腿组合是负贡献，跨族才正交**
`fundamental44` 全族闭环实测（12/12 字段）：
| 构型 | S | 2Y |
|---|---|---|
| `mscore` 单腿 + 破 prod 壳层 | 0.57 | **1.08** |
| `mscore + wc_accruals`（同族 2 腿等权 rank）| 0.61 | **0.16** ↓ |
| `mscore + wc + yoon`（同族 3 腿）| 0.53 | **0.14** ↓↓ |

⇒ **同族字段（同为应计/舞弊质量）机制不正交**，等权 rank 叠加**把 2Y 从 1.08 压到 0.16**。
⇒ 对「单边恒正型」字段族：**破 prod 壳层三件套（`trade_when(adv20>0.6)` 门控 → `tail` 裁剪 → `group_rank(bucket(rank(cap)))` 分组，逐层嵌套而非相加）可把 2Y 抬 +0.79（0.29→1.08）但压 S（0.70→0.57）** —— 又一个 S↔2Y 权衡（与 pv47 族同构）。
⇒ **结论：这类族要出货必须引入「非本机制族」的正交腿**（如 `oth695` 贸易流 / `pv47` 峰度），族内调参已无空间。

### 铁律 C：KOR 会计质量/财务基本面族的 S 天花板 = 0.61
`fnd90_qes_gamef_grossprofit_asset` S 0.61 / F 0.44 / 2Y 0.71 是全族最强。
**2026-10-15 补充**：`fundamental44` 全族闭环也落在同一量级 —— 天花板 **S 0.70**（`mscore`，裸 252 窗）/ **0.61**（套壳层，2Y 1.08）；
族内 3 条 S ≥0.5。32 + 22 结构穷举后确认：
**季频财务字段无论壳层、方向、组合都卡在 S 0.6–0.7，2Y 最高 1.08。**
⇒ 该机制族**不判死**（有活腿）但**单独不可提交**，归「需跨族正交腿」池。
⇒ KOR 要出货仍须走**日频**信号（日频特定收益 / 贸易流强度 / 内部人交易）。

---

## 5 ★★ `bucket(rank(cap))` 破 prod 墙**不是普适杠杆**（重要修正）

先前结论「`bucket(rank(cap), range="0,1,0.2")` 唯一压 prod 有效」**只在 `oth695` 贸易流强度族成立**。
在 `pv47` 峰度族上实测反而**变差**：

| 构型 | IS 侧 | prod | 判定 |
|---|---|---|---|
| `oth695` + bucket | S1.91/2Y2.27 | 0.7098→**0.6977** ✅ | 有效 |
| `pv47` 基准（无 bucket） | S1.90/2Y1.92 | 0.7275–0.7716 | 基线 |
| `pv47` + bucket(0.2) | S1.53/2Y0.97 | **0.8321** ❌ | **变差** |
| `pv47` + bucket(0.1) | — | 族级 [0.7,0.8) 桶 n=35 | 密墙 |
| `pv47` + `trade_when(rank(adv20))>0.3/0.5/0.7/0.85` | S 1.90→**0.42**（0.85 档）| — | **S 崩塌** |
| `pv47` + `hump=0.005` | S 1.53→**0.76** | — | S 崩塌 |
| `pv47` + 盈利腿 rank 组合 | S 0.83/0.94 | — | 跨族稀释 |
| `pv47` + tail newval 0.6/0.65 | S 1.13/1.18 | — | 低于基准 1.53 |

⇒ **「加 bucket / 加门控」不是通用 prod 解法**。正确顺序仍是三步（换族 → 换连续桶 → 加门控），
但**每一步都必须实测**，不能跨族照搬结论。**用 `check_correlation` 的直方图判族级命运**：`[0.7,0.8)` 桶 n≥1 ⇒ 密墙。

---

## 6 本轮最优候选（未提交，提交权归用户）

### `omoMKXbJ` — S1.53 / F0.94 / 2Y0.97 / PPA 全过 / self 0.3212，**prod 0.8321 未过**

```
vector_neut(trade_when(greater(rank(adv20), 0.1),
  tail(group_rank(multiply(rank(multiply(-1, ts_kurtosis(pv47_for_statssimple_only_spret, 140))),
                       rank(multiply(-1, ts_rank(pv47_for_statssimple_only_spret, 132))),
                       rank(multiply(-1, ts_rank(pv47_for_statssimple_only_spret, 252)))),
                   bucket(rank(cap), range="0,1,0.2")), lower=0.2, upper=0.8, newval=0.5), -1),
  power(rank(rsk68_weight_dadv), 0.5))
```
KOR/TOP600/D1 · decay4 · **MARKET** · trunc0.08 · nanHandling OFF

| 闸 | 值 | 限 | 判定 |
|---|---|---|---|
| LOW_SHARPE | 1.53 | 1.58 | ✗ 差 0.05 |
| LOW_FITNESS | 0.94 | 1.0 | ✗ 差 0.06 |
| IS_LADDER_SHARPE | 0.97 | 1.58 | ✗ 差 0.61 |
| sub-universe | 1.39 | 0.53×S | ✓ |
| investability | 1.14 | 0.70×S | ✓ |
| risk-neutralized | 1.86 | — | ✓ |
| CONCENTRATED_WEIGHT / TURNOVER / CLUSTER | — / 0.38 / 0.97 | — | ✓ |
| PPA 检查 | — | — | ✓ 全过（failed_ppa_count=0）|
| SELF_CORRELATION | 0.3212 | 0.7 | ✓ |
| PROD_CORRELATION | 0.8321 | 0.7 | ✗ |

**这是 KOR 至今 `failed_ra_count` 最小（3）、且 PPA 全过的最佳候选。**
剩余障碍：IS 侧差 0.05/0.06/0.61 + prod 0.8321。

---

## 7 KOR 出货能力总账（2026-10-15 结算）

| 项 | 状态 |
|---|---|
| 已提交 ACTIVE | **2 颗**：`xA16pzQJ`（`oth695` 进口强度，2026-10-14）、`rKdK2vLE`（`shortinterest38`）|
| 已点亮数据集 | `shortinterest38`、`other466` |
| 可提交产出判定 | **封顶 2 颗**。三方向穷尽（低拥挤 / 结构独特 / 日频收益）+ 会计质量族 48 结构穷举后无新增。|
| 结构性原因 | ① TOP600 小宇宙配额紧；② prod 墙在 pv47/risk 峰度族是密墙；③ 剩余白空间（`other395` 等应计网格）S 天花板 0.61。|

---

## 8 工程坑（本轮新增）

- **`get_user_alphas` 返回体积极大**（KOR IS 池 50 条 ≈ 155 KB）⇒ 必须让 MCP 落盘再用脚本解析，直接读会超 token 上限。
- **`get_user_alphas` 不支持 `order=-sharpe`**（400 Bad Request）⇒ 只能 `order=-dateCreated`，排序要自己做。
- **`results[].datasets` 在 KOR 为空** ⇒ 数据集归组必须解析 `code` 的字段前缀。
- **`batch_get_alpha_metrics` 对刚创建的 alpha 返回全 null** ⇒ 逐个 `get_alpha_details` 才拿得到。
- **`preflight` 会把算子名（`tail`/`greater`/`vector_neut`/`shortscale`/`std`）误报为 `unknown_fields`** ⇒ 这是已知假阳性，只要 `unknown_soft` 为空且真实字段都在 `fields_checked` 里即可放行。
- 平台队列拥塞时 `progress: 0.35` **不是僵尸**（实测卡 0.35 约 25 分钟自行 COMPLETE）⇒ 不要提前补发。
- 单批 18 条会被并发限流截断（10 条上限附近）⇒ 分批 6–8 条更稳。