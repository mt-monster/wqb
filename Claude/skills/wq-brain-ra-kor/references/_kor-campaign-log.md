# KOR 战役日志（历史层 · 含已作废结论）

> 本文件是 `wq-brain-ra-kor` 的**历史层**：按日期倒序保存每轮战役的原始结论，并在被后续实测推翻处就地标注
> **⛔ 已作废 → 现行**。这样做的理由：这些结论不是「写错了」，而是**当时证据不足下的正确推断**，
> 删掉会让下一个人重走同一条路；但混在活文档里会让人照作废的那条执行。
>
> - **现行有效结论只在 SKILL.md 的 `profiles:manual` 块**（≤30 行，已裁决、去重、无星级噪声）。
> - **纯数值 / 配方 / 逐年表**在 [`_kor-gatebreak-evidence.md`](_kor-gatebreak-evidence.md)。
> - **带日期的一次性产出**（候选 alpha id、封顶颗数、波次 verdict）以台账为准 —— 见文末「查台账」。
> - 星级已折叠为三个语义标签（原 8 档 ★ 无法区分「违反即报废」与「值得看一眼」）：
>   **【硬闸】** 违反即整批报废 / 判死错误，无补救｜**【方法】** 流程要求，跳过会系统性漏信号｜**【实证】** 数值与战例，查证用。

---

## 0 裁决表（同主题前后结论，谁作废谁）

| # | 主题 | 旧结论（见本文件哪节） | 现行结论 | 作废依据 |
|---|---|---|---|---|
| A | **中性化默认档** | §4.3「MARKET 是 KOR 唯一 F 与 2Y 兼顾档」、§3.3「第 3 次实证 MARKET 是 2Y 钥匙」 | **不要默认 MARKET；换族 / 换结构必重扫 11 档** | §1.6 铁律 F：同一 `pv47` 族两次实测给出两个不同最优档（decay4 旧结构 → MARKET；decay3+sector 新结构 → REVERSION_AND_MOMENTUM）⇒ 最优档是**结构特异**的，不是区域恒量 |
| B | **`bucket(rank(cap))` 压 prod** | §3.5「唯一有效杠杆」、§3.6 三段配方链 | 三步处置**顺序**不变，但**每步必实测、不可跨族照搬** | §1.5：`oth695` 贸易流族 0.89→0.71 ✅；`pv47` 峰度族 0.73→**0.83** ❌（且 2Y 掉到 0.97）⇒ 反向 |
| C | **`fundamental44` 死因** | §2「烧 8 槽才发现『取值二值』」 | **不是二值**，是「单边恒正 + 有界小量纲」 | §1.1 六法体检：法 2 非零覆盖与法 1 **完全相同（312=312）⇒ 零占比 0**；法 6 `zscore>0` 占 52.2%、`>1` 占 16.4%（正态参考 50%/15.9%）⇒ 截面区分度充足、近正态 |
| D | **「已点亮」的口径** | §5.1「目前只有 fundamental 家族达到 3，其余都不算点亮」 | **数据集级** ≥3 颗提交；当前已点亮 = `shortinterest38` + `other466` | §3.7（2026-10-14 `shortinterest38` 达 3 颗）→ §1.7（2026-10-15 两个数据集各 5 颗）。旧句是 2026-10-13 的快照，被后续两次提交推进 |
| E | **「按塔排除」** | 区域面板曾写「分析师 / insiders / pv / … / risk 全红灯」 | **红的是「已试结构」，不是字段 / 塔**；只排除「该数据集已提交 ≥3」 | §4.1 结论 1：`pv47`/`pv103`/`pv13`/`pv14` 与 `risk59/60/68/71` 均**不在判死名单**；pv47+risk68 换构型即出 4 颗 `failed_ra_count=0` |
| F | **可提交封顶颗数** | §3.7「封顶 1 颗」、§1.4「封顶 2 颗」 | 这是**移动计数器**，不是结构结论 ⇒ 查台账，不在文档维护 | 三个数字分别是 2026-10-14 / 10-15 中午 / 10-15 晚的快照；结构性结论只有一条：**KOR 强信号与 prod 白空间互斥**（§1.8） |
| G | **探针多样性靠人工对照** | §2 前身（`_probe-sop.md` 旧 C 条）「手写批次无 wave 文件 ⇒ 需人工对照 A/B 两表」 | 已工具化：`tracking/KOR/scripts/scan_diversity.py --audit <batch>` | 2026-10-14 落地，脚本直读 A 表单一事实源与 B 表区域约束 |

---

## 1 2026-10-15 系统性战役（48 结构穷举）

> 完整 SOP 见 [`_dataset-scan-sop.md`](_dataset-scan-sop.md)；字段画像 `docs/reference/kor_dataset_field_profiling_20261015.md`。

### 1.1【方法】S0 扫描结论与三条新铁律

**S0**：全量 87 个数据集 → 已点亮 2（`shortinterest38` / `other466`，数据集级排除）→ 已判死 22 → **候选 63**。
**`alphaCount` 是 prod 墙密度最可靠的单因子代理**（d219–d232 实证）⇒ 选集第一优先是低拥挤，不是高 valueScore。
⚠ 但**低 alphaCount ≠ 白空间有价值**（见 §3.8「冷门 ≠ 有信号」，低拥挤池 6 个数据集全灭）。

**铁律 A（六法体检校正版）** —— `fundamental44` `fnd44_mscore`，17 条仿真，`reports/field_check_fundamental44_20261015.md`：

- 法 2 非零覆盖：法 1 与法 2 **完全相同（312 = 312）** ⇒ 零占比 0，**不是二值**；
- 法 6 形态：`zscore>0` 占 **52.2%**、`zscore>1` 占 **16.4%**（正态参考 50%/15.9%）⇒ 截面区分度充足、近正态；
- 法 4 范围：|x| ≤ 0.4，**74% 挤在 ±0.1**（有界小量纲 + 大量并列 ⇒ 裸 `rank` 信息量低）；
- **法 5 中心：1 年均值 > 0 占 92.6% ⇒ 单边恒正，这才是真死因。**
- **实测翻证**：裸水平 `reverse(ts_backfill(F,252))` S≈0 → `reverse(ts_delta(F,252))` **S 0.70 / F 0.40**（符号翻转 + 幅度翻倍）；
  `reverse(ts_delta(F,66))` 0.31；`reverse(ts_zscore(F,252))` 仅 0.22（**时序标准化无效**）；22 窗 0.09 已失效。

⇒ **正确表述：不是「无区分度」，而是「单边恒正 + 有界小量纲」⇒ 禁裸水平做多空，取变化率（窗口 252 优于 66）。**
⇒ 与 `analyst25` 体检包 advice（「单边恒正 → 勿用原始水平做多空，先变化率/排名/与基准差」）**完全一致**。
⇒ 该族 12 字段同构（cov 0.898 + 同为舞弊/应计评分）⇒ 应先批量跑 `reverse(ts_delta(F,252))` 一轮再谈判死。
⚠ **元数据 `coverage` 不可信**：`fnd44_mscore` 元数据 0.8984 vs **实测 0.490（高估 1.8 倍）**。
⚠ **法 3 短窗失效**：`ts_std_dev(F, 5/22/66)` 读数非单调（492/313/497）⇒ 短窗被 NaN 污染，频率读数不可信，窗口下限按季频保守取 252。

**铁律 B：方向必须实测。** `icfroe_5y` 按语义猜正向 → 实测 **−0.62**（应 reverse）；`receivable_days` 猜 reverse → 实测 **−0.36**（应正向）。
⇒ 新字段族首波**正反双向各一条**（2 槽成本，省一整轮）。

**铁律 C：KOR 会计质量 / 财务基本面族 S 天花板 = 0.61**（`fnd90_qes_gamef_grossprofit_asset`，32 结构穷举）。
季频字段无论壳层 / 方向 / 组合都卡在 S 0.6、2Y ≤0.97 ⇒ 该机制族不值得再投配额；**KOR 出货必须走日频信号。**

### 1.2【方法】S1 必先六法体检（论坛共识，本轮曾跳过）

> 源：①《读一个数据字段,该看哪几项》(DA98440, 37 赞) ②《【方法】新数据字段的快速评估：6 个表达式》(LL46807, 22 赞)。
> 项目实现：`brain-datafield-exploration-general` / `brain-dataset-exploration-general` —— **本轮战役两个都没调用，是最大方法缺陷。**

六法 → 模板映射（体检完直接照表设计，不要再猜）：

| 法 | 表达式 | 映射决策 |
|---|---|---|
| 1 覆盖 | `F` | cov<0.4 → **必须** `ts_backfill` |
| 2 非零覆盖 | `F != 0` | 与法 1 差值大 = 稀疏事件型 → `trade_when` 事件门控，**禁裸 rank** |
| 3 更新频率 | `ts_std_dev(F, 5/22/66) != 0` | 季频 ⇒ 窗口 ≥63d；日频 ⇒ ≥22d |
| 4 取值范围 | `abs(F) > 1/10/100` | 量纲跨度大 → `rank`/`ts_zscore`；有界 [-1,1] → 直接 `rank` |
| 5 **中心趋势** | `F+1`、`rank(F)` | **单边恒正（skew≈+0.99）⇒ 禁原始水平做多空**，先 reverse / 变化率 / 与基准差 |
| 6 分布形态 | 直方图 + 分位数 | `zero_inflated` / `point_mass` ⇒ `ts_backfill` 或事件门控 |
| 7 数据集归属 | 查命名空间 | **同源字段相关性天然高，别当两个独立信号** |

设置：`Neutralization=None` / `Decay=0` / Test Period `P0Y0M0D`；单字段 ≈6 条仿真（一批）；**VECTOR 必须先套 `vec_*`**。

**本轮教训的代价（⛔ 已按裁决 C 更正措辞）**：`fundamental44` 烧了 8 槽才定性 —— 而**法 5/6 看分布即可零配额预判**
「单边恒正 + 有界小量纲」。旧文在此处写「才发现『取值二值』」，那是被法 2 证伪的错误定性，别再引用。

**KOR 特有约束：离线体检包 85% 退化。** `tracking/mining/field_inspect_kor_*.json` 1333 字段中 **1126 个 `_degraded`**
（skew/kurt/freq/shape 全 null）；根因 = WebData 包 `research-data/WebData_20260219_V0.10.9` 的 `dataSetList.json` 里
**KOR 只有 1 个组合**（`analyst25_KOR_TOP600_Delay1`），其余数据集不在包内。
⇒ KOR 绝大多数数据集必须走**在线**六法；唯一完整的 `analyst25` 包其 `advices` 可直接消费。

### 1.3【硬闸】铁律 E：报告期塌陷先做 raw vs risk-neutralized 分解

`get_alpha_pnl` **自带三列**（`pnl` / `risk-neutralized-pnl` / `investability-constrained-pnl`）⇒ **零额外成本**。
逐年增量算 `因子暴露贡献 = raw增量 − RN增量`：

| 形态 | 判读 | 处置 |
|---|---|---|
| **RN 增量 ≫ raw 增量**（因子贡献为负）| **因子暴露拖累**，纯 alpha 没坏 | **换中性化档** ✅ |
| raw 与 RN 同步走弱 | 信号本身衰减 | 换字段 / 换机制族 |

实证战例 `omoMKXbJ`：2021/2022 因子暴露 **+1.73M / +1.70M** 顺风 → **2023 −0.71M** 逆风（翻号约 2.4M）；
2023 的 **RN 增量 +934k 是 10 年第 4 好** ⇒ 纯 alpha 未失效。
⇒ 只换中性化档即把 **IS_LADDER 0.97 → 1.44（+0.47）**、**LOW_SHARPE 1.53 ❌ → 1.68 ✅**、**failed_ra 3 → 2**。

### 1.4【硬闸】铁律 F：中性化最优档是「字段族 + 结构」特异的，换族必重扫

⛔ **作废旧结论**：§4.3「MARKET 是 KOR 唯一 F 与 2Y 兼顾档」与 §3.3「第 3 次实证 MARKET 是 2Y 钥匙」。
两者都是**族内 + 结构内**的正确观察，被当成区域恒量后就变成了误导。

`pv47` 峰度/防御族实测（同一表达式只改 neutralization；结构已是 decay3 + sector + pow0.85 的新版）：

| 中性化 | S | F | 2Y | inv | failed_ra | failed_ppa |
|---|---|---|---|---|---|---|
| MARKET（旧默认）| 1.53 | 0.94 | 0.97 | 1.14 | 3 | 0 |
| **REVERSION_AND_MOMENTUM** | **1.68** | 0.92 | **1.44** | **1.21** | **2** | **0** |
| FAST | **1.84** | 0.88 | **1.55** | 1.09 ⚠ | 3 | 1 |
| SLOW | **1.94** | 0.94 | 1.01 | 1.01 ⚠ | 3 | 1 |
| SLOW_AND_FAST | 1.73 | 0.73 | 1.31 | 0.88 ⚠ | 3 | 1 |
| STATISTICAL | 1.53 | 0.74 | 0.91 | 0.83 ⚠ | 4 | 1 |

⇒ KOR 全区 **11 档中性化合法**（清单见 SKILL.md ④）。
⇒ `FAST` 给最高 2Y、`SLOW` 给最高 S、`REVERSION_AND_MOMENTUM` 给最干净 investability + 最小 failed_ra。
⇒ **关键读法**：同一个 `pv47` 族，旧结构（decay4）下 MARKET 最好、新结构（decay3+sector）下 REVMOM 最好
—— 所以「最优档」随结构漂移，**任何一次实测都不能外推到改了壳层的下一版**。

### 1.5【实证】`bucket(rank(cap))` 破 prod 墙**不是**普适杠杆（裁决 B）

先前「换连续桶是唯一压 prod 有效」**只在 `oth695` 贸易流强度族成立**；在 `pv47` 峰度族实测**反而变差**：
`pv47` 基准 prod 0.7275 → `+bucket(0.2)` **0.8321**（S 1.53 但 2Y 掉到 0.97）；`+trade_when(adv20)>0.85` → **S 崩塌 1.90→0.42**；
`+hump=0.005` → S 1.53→0.76；`+盈利腿` → S 0.83（跨族稀释）；`+tail newval 0.6/0.65` → S 1.13/1.18（低于基准）。
⇒ **三步处置顺序不变，但每步必须实测、不可跨族照搬。** 判族级命运用 `check_correlation` 直方图：`[0.7,0.8)` 桶 n≥1 ⇒ 密墙。

### 1.6【实证】`performance_comparison` 不是风险因子归因工具

- 端点 = `GET /{users/self|teams/{id}|competitions/{id}}/alphas/{id}/before-and-after-performance`；
  docstring 明写「merged performance check」⇒ 用于 **SuperAlpha 合并前后对比**，普通 IS alpha 返回空 ⇒ 报错。
- ⇒ 风险因子暴露归因走 `get_alpha_pnl` 的 `risk-neutralized-pnl` 列自行分解（铁律 E）。
- 相关 skill：`brain-alpha-robustness`（Phase B 归因 B.1–B.5 + Phase C 反过拟合闸）。
  ⚠ 按 Phase C 现档，`omoMKXbJ`(MARKET) 会被判 REJECT：CV_Sharpe 0.82 / 衰减比 0.05 / max-min 28。

### 1.7【实证】S0 选集与「已点亮」实测口径（裁决 D）

- **已点亮判定**（数据集级，勿改口径）：`get_user_alphas(region, stage=OS, status=ACTIVE)` → **解析 `code` 字段前缀**归组计数
  （`results[].datasets` 在 KOR 为空）。⚠ `get_user_alphas` **不支持** `order=-sharpe`（400）⇒ 只能 `-dateCreated`，自己排序。
- 2026-10-15 实测：已点亮 = `shortinterest38`(5) + `other466`(5) ⇒ 本轮全程排除；其余 63 个数据集为候选。
- **同族近亲提交后 self 会冲 0.99+** ⇒ 同数据集内一次只提 1 颗，提完必测 self。
- KOR 类别分布（数据集数，2026-10-13 快照）：MODEL 62 / OTHER 27 / NEWS 24 / (null) 21 / PV 18 / FUNDAMENTAL 18 /
  ANALYST 17 / RISK 7 / SENTIMENT 6 / SHORTINTEREST 3 / SOCIALMEDIA 2 / MACRO 2 / INSTITUTIONS 2 / INSIDERS 2 /
  IMBALANCE 1 / EARNINGS 1。

### 1.8【实证】终局结算：KOR 强信号与 prod 白空间互斥

pv47 族 IS 全过 2 颗（`E5VAZ5pr` / `A1Qd18Kd`，S 1.99/1.97、F 1.10/1.11、2Y 1.91/1.90、failed_ra=0）
但 prod 0.74/0.75（`[0.7,0.8)` 桶 n=3 密墙）；fnd44 族 prod 0.34 干净但 S 天花板 0.93 不过闸。
⇒ **KOR 单独封顶，全破需换 region 或机制正交第二族。**
⚠ **此为单轮结论，非 KOR 永久天花板** —— 换数据集族须重走六步。

### 1.9【方法】字段画像只看单字段 S，看不到「构造」

`field_profile --build --region KOR`（33,618 字段）显示 ALIVE **仅 18 个**，且全在已点亮塔
（other466×10 / shortinterest38×7 / risk71×1）；未点亮塔只有 WEAK 级（`analyst10` surprise 1.44–1.52、`other532` 1.25、`pv106` 1.12）。
**但 `pv47_spret` 单字段也弱，是构型把它变成 S1.90。**
⇒ **选集时不要被 ALIVE/WEAK 二分法挡住；先看字段机制是否「收益分布型」，再上构型。**

### 1.10 算子穷举实测（d282，峰度族）

把 IS 推到全过的**不是** decay/tail/pow 微调，而是**加一层「行业去均值」**：`group_neutralize(·, sector)`
（F 0.98→1.10、2Y 1.56→1.91、failed_ra 2→0）。`group_zscore` 有害（2Y 崩到 1.02）、`ts_mean`/`ts_decay_linear` 毁 S、
`signed_power` 在秩积上 no-op、**trunc 0.06/0.08 完全等价（可删）**、门控阈值上调毁 S。
⇒ **算子穷举的正确顺序 = 先中性化/分组轴，再时序平滑，最后幂次。**

---

## 2 2026-10-14 流程优化：「模板单一」不是工具固化，是「绕过流程」

> 触发：用户质疑「全程只用 2 套构型扫描，会不会遗漏信号、模板单一？」—— **质疑成立。**

### 2.1【方法】根因（三层）

| 层 | 事实 |
|---|---|
| **工具层** | 本来就有完整多样性系统：toolkit `config/template_families.json`（**9 骨架族 + free_explore**）、`kor_generation_constraints.json` 的 `skeleton_quota`/`force_explore_ops`、`diversity_audit.py`（审计 + 签发 `next_round_injections`）、`gate.py` **闸 6** |
| **执行层** | 用 `tools/submit_batch.py` **手写表达式发批、不写 wave 文件 ⇒ 审计/注入/闸 6 全部从未触发** ⇒ 固化发生在「绕过流程」这一步 |
| **文档层** | 本 skill 手写区只记了 2 套构型（SH/PV），**强化了单一模板倾向** |

### 2.2【实证】代价：同字段换模板差 0.44

`insider_feats`：SH 构型 **S1.23**（且 CW 不触发）→ 换「裸 `multiply(rank(A),rank(B))`」**S1.67**（全闸过）；
`first_order_transform` 族在 `pv47_spret` 上：`rank_reversal` S1.49（其余 8 变体 S −0.98~0.09）——
**同一字段 9 个变体是横截面低相关的独立结构**（论坛帖「模版群助我 60 天点亮 60 个塔」252 赞）。

### 2.3【方法】四条新铁律

1. **手写扫描必过「多样性三闸」**：① 族数 ≥2；② 引入 ≥2 个未用/force 算子；③ **单条**表达式算子数 <10。
   ⇒ 用 `$WQ_PY tracking/KOR/scripts/scan_diversity.py --audit <batch>` 自查（⛔ 旧文写「需人工对照 A/B 两表」，已工具化，见裁决 G）。
2. **判死前先自问**：「S<1.0 是『没信号』还是『模板不对』？」—— 若未用 ≥2 族 / ≥2 未用算子 ⇒ **不许判死**。
3. **优先用族骨架，少自造模板**：`first_order_transform`（9 变体）尤其适合「同一强字段拆多颗低相关 alpha」。
4. **自造构型（SH/PV）不在 9 族库内** —— 有效但**不能当唯一模板**（审计会判 0 族）。

### 2.4【实证】族驱动扫描战果

`event_conviction_ratio` 族在 `oth695`（韩国进口）上给出「S/F/2Y/CW 全过」新结构（10+ 变体）：

```
tail(winsorize(group_rank(ts_sum(vec_avg(oth695_import_value_4), W), sector), std=2),
     lower=0.2, upper=0.8, newval=0.5)   # KOR/TOP600/D1 · decay4 · MARKET · trunc0.08
W=20: S1.82/F1.85/2Y1.81 ; W=66: S1.76/F1.77/2Y1.71 ; W=88: S1.77/1.79/1.65（9qEYgWVV 全闸过）
```

- 三重机理：① 该族 **2Y↔S 权衡**（SECTOR 2Y1.30 → MARKET 2Y1.71 —— ⛔ 此条曾当作「MARKET 是 2Y 钥匙」的第 3 次实证，见裁决 A）；
  ② **prod 直方图 `[0.7,0.8)` 恒空谷**、仅单 outlier @0.80 ⇒ 可救；③ 相比 SH 构型 prod 0.8885，本族降至 0.79–0.81。
- **判决修正**：`oth695` 此前被判「prod 0.89 被挡」是**模板单一**所致 —— 换族后 prod 降 0.08 且 S/F/2Y 全过。
  ⇒ **「prod 被挡」的判死必须附「已试 ≥2 族」的前置条件**（已写入 `_probe-sop.md` 第 1.5 步 D 条）。
- ⚠ `bucket` 只能作 `group_rank` 分组参（独立成 alpha ⇒ ERROR 连坐）；`range` 不可含空格。

---

## 3 2026-10-14 破 prod 墙（d219–d235，约 112 探针）

> 目标「10 颗可提交」；结论：**IS 侧可达、prod 侧封死**。报告 `output_report/KOR_campaign_10alpha_20261014.md`。

### 3.1【实证】判决修正：KOR 的支配性障碍是 prod 墙，不是 IS 闸

本战役在 **5 个不同数据集**上造出 IS 全闸通过候选（S 1.5–2.5、2Y 1.6–2.2），
但 **prod 仅 `shortinterest38` 族过关（0.60–0.67）**；其余新腿 prod 一律 **0.81–0.89**。
⇒ **选数据集时先估 prod 拥挤度，再投入预算。**

### 3.2【实证】三条新腿（IS 全闸通过，仅 prod 超线）

| 腿 | 数据集（塔） | 配方 | S/F/2Y | prod |
|---|---|---|---|---|
| 内部人买卖比 | `insider_feats`（OTHER）| `multiply(rank(buy_sell_tx_count_ratio_all_60d_filled), rank(buy_sell_ratio_top20_250d_filled))`｜MARKET 档 | 1.67/1.78/1.68 | **0.8527** ❌ |
| 韩国进口值 | `oth695`（OTHER）| `hump(subtract(group_rank(vec_avg(oth695_import_value_4), industry), 0.5), hump=0.003)`｜SECTOR | 1.79/1.81/1.95 | **0.8885** ❌ |
| 韩国出口值 | `oth475`（OTHER）| 同上换 `oth475_export_value`｜SECTOR | 1.52/1.42/1.74 | **0.8691** ❌ |

### 3.3【实证】中性化档 = 2Y 的开关（insider 族）⛔ 已被裁决 A 收窄

同一构型：**SECTOR 档 2Y 1.18 → MARKET 档 2Y 1.68**（全闸通过）。
⇒ 当时结论「凡新族，先并行跑 SECTOR + MARKET 两档」；**现行**：先并行跑 **11 档里成本可接受的几档**，
MARKET 只是候选之一，不是先验赢家。

### 3.4【实证】第三套赢家形态：裸 `multiply(rank(A), rank(B))`

不套 `group_rank`/`hump`，与 ①SH 构型、②PV 构型并列。
⚠ **合规待判**（同数据集同机制异窗口）；合规形态 `subtract(rank,rank)` 实测仅 S 0.10、`divide(A,B)` 仅 0.65 ⇒ 该形态不可替代。

### 3.5【实证】破 prod 墙铁律：连续桶分组 `bucket(rank(cap))` ⛔ 已被裁决 B 收窄为「族特异」

同数据同机制下 **prod 0.8885 → 0.7098（−0.18）**：

```
tail(winsorize(group_rank(ts_sum(vec_avg(oth695_import_value_4), 20),
                           bucket(rank(cap), range="0,1,0.2")), std=2),
     lower=0.2, upper=0.8, newval=0.5)      # MARKET · decay4 · trunc0.08
⇒ S1.91 / F2.18 / TO0.0367 / 2Y2.27 / CW✅ / prod 0.7098（差 0.0098）
```

- 杠杆排序（**仅 `oth695` 族实测**）：① 换分组轴为连续桶（粒度 0.25→0.2 单调降）；② `trade_when` 门控抬 2Y 但不压 prod；
  ③ `vector_neut` 残差化**杀 S（0.27–1.04）禁用**；④ `ts_rank`/`ts_zscore`/`ts_decay_linear` **TO 爆或 CW=1.0 禁用**；
  ⑤ `quantile` 与 `ts_sum` 等价。
- 出口腿 `oth475` 同族亦活（S1.52/2Y1.96）⇒ 进口/出口双腿。

### 3.6【实证】第二颗全闸通过 alpha `88voYna7`：三段配方链

```
88voYna7 = trade_when(greater(rank(adv20), 0.6),
              tail(winsorize(group_rank(ts_sum(vec_avg(oth695_import_value_4), 20),
                                        bucket(rank(cap), range="0,1,0.2")), std=2),
                   lower=0.2, upper=0.8, newval=0.5), -1)
KOR / TOP600 / D1 · decay 4 · MARKET · trunc 0.08 · pasteurization ON · nanHandling ON
```

**S1.86 / F2.19 / TO0.0269 / SUB1.82 / 2Y2.10 / inv1.86 / CW✅ / CLUSTER✅ / prod 0.6977✅ / self 0.2305✅**
**`failed_ra_count=0` · `all_passed=true` · 塔 PV(1.4)+OTHER(1.6) 双塔 effective 2**

| 段 | 内容 | prod 效果 |
|---|---|---|
| ① 结构 | `event_conviction_ratio` 族骨架 | 基线 0.8885 |
| ② **分组轴 = 连续桶 `bucket(rank(cap), range="0,1,0.2")`**（不是 sector/industry）| 0.8885 → **0.7098** |
| ③ **第二维度门控 `trade_when(greater(rank(adv20), 0.6), <信号>, -1)`** | 0.7098 → **0.6977** ✅ |

门控阈值曲线：`>0.3`→0.7064 ｜ `>0.5`→0.7017 ｜ **`>0.6`→0.6977 ✅破闸** ｜ `>0.7`/`>0.8` 未测。
⚠ `trade_when(volume>0)`（无阈值）只抬 2Y 不压 prod ⇒ **门控必须用相对阈值 `rank(adv20)`**。
⚠ `group_rank(x,g,weight)` 三参**平台 ERROR**；`bucket` 只作 `group_rank` 分组参。

### 3.7【实证】饱和判定与迁移测试 7 条腿（⛔ 封顶颗数见裁决 F）

破墙配方系统性迁移测试：

| 腿 | 结论 |
|---|---|
| **`oth695`（韩国进口强度）** | ✅ **已提交 `xA16pzQJ`**（唯一同时过 2Y + prod 的字段）|
| `oth475` 出口 | 两难：sector 保 2Y(1.96) 但 prod 0.844；bucket 降 prod 但 2Y 1.33 |
| `insider_feats` | 单腿 top20_10d 1.43；**两腿组合全负**（divide/ts_corr/subtract −0.11~−0.41）|
| `dl_riskfree_returns` | probQ3 S1.63 但 prod 0.867 |
| `pv47_spret` | −0.26（收益序列 × 累积求和 = 噪声）|
| `other72` | 0.82–0.97 弱 |
| `other106`（指数权重因子）| −0.32~0.04 **判死**（cov 0.404、仅调仓日变 ⇒ 近静态型）|

⇒ **配方仅在「慢变强度型字段（贸易流/持仓强度）」上同时过 2Y 与 prod；KOR 只有 `oth695` 满足。**
⇒ 继续在 KOR 换数据集的边际收益已趋零；新增产出需换 region。
⚠ **MATRIX 字段误套 `vec_avg` ⇒ 整批 CANCELLED**（混合批次里每个字段的 `vec_*` 必须按该数据集 `dataType` 逐个确认）。
⚠ 同一机制的不同腿**最优分组轴不同**（进口腿 bucket 保 2Y、出口腿只有 sector 保 2Y）⇒ **判死前必须逐腿实测**。

本区当时状态（2026-10-14）：`shortinterest38` 已达 3 颗 ACTIVE ⇒ 点亮（`rKdK2vLE` 2026-10-13 提交；兄弟颗 `d5K508qg` 等 self 0.988 封锁）。

### 3.8【实证】三方向穷尽仍无新增（d233–d235）

按 **① 低拥挤度（alphaCount 升序）+ 高覆盖**、**② 结构独特**、**③ 日频收益** 三方向各探一轮，全部无果。

**`ts_kurtosis`（PV 构型 2Y 钥匙）的字段类型边界**：

| 字段类型 | 钥匙有效？ | 实证 |
|---|---|---|
| 日频**特定**收益（`pv47_for_statssimple_only_spret`）| ✅ | 2Y 1.92（全闸过）|
| 日频**总**收益（`analyst_earnings_ibes.one_day_total_return_dlr1`，cov 1.0）| ❌ | **S 0.14**（d233）|
| % 单位 reproducible specific return（`rsk71/rsk72_*_dsrt`）| ❌ | 2Y ≤1.27 |
| 内部人买卖比 / 波动率 / 情绪 | ❌ | d226 / 前序 |

⇒ **钥匙只吃「日频特定收益序列」**；`analyst_earnings_ibes` 的日频收益族虽 cov 1.0、aCnt 0，仍不可用。

**「冷门 ≠ 有信号」（低拥挤池全灭）**：`price_signal_dl`（cov 0.99，aCnt 0）最高 **0.99**（`normalized_trend_indicator_4`，TO 0.037）；
`model313` 0.36/0.37；`acquisition_model` −0.17；`quant_factor_lib` 0.10；`model170` −0.08；`behavioral_signals` 0.57。

**「结构独特 ≠ 可用」（常量退化陷阱）**：`shortinterest5` 的 `price_limit_condition` / `max_price_increase_ratio` /
`max_price_decrease_ratio`（KOR 涨跌停制度）与 `macro63.mcr63_membership`（指数成分）⇒ **S=0.0、TO=0.0 ⇒ 常量 / 退化信号**。
⇒ **发批前用 `field_profile` 的 `to_med` 与取值分布先排除常量字段。**

---

## 4 2026-10-09~13：未点亮数据集第一套「RA 全闸通过」构型

> 背景：区域面板原写「分析师/pv/risk…全红灯」。本轮实证 **该判决是「已试结构」的红，不是「字段」的红**（裁决 E）——
> 换构型后 PV 塔 + RISK 塔各出 2 颗 `failed_ra_count = 0` 的 alpha（两颗均点 2 个 0 计数塔，effective 2）。

### 4.1【实证】PV 构型（三要素缺一不可）

```
BASE = multiply(rank(multiply(-1, ts_kurtosis(<X>, 140))),
                rank(multiply(-1, ts_rank(<X>, 132))),
                rank(multiply(-1, ts_rank(<X>, 252))))
ALPHA = vector_neut( trade_when(greater(rank(adv20), 0.1), scale(BASE, shortscale=0.5), -1),
                     power(rank(rsk68_weight_dadv), 0.5) )
设置 KOR/TOP600/D1 · decay 4 · neutralization=MARKET · trunc 0.08 · nanHandling ON
X（KOR 已验证）= pv47_for_statssimple_only_spret；旁证同机制字段：other532_emerging_daily_specificreturn、risk71_residualized_return_*
```

| 要素 | 作用 | 实证 |
|---|---|---|
| ① `ts_kurtosis(X, 140)` 防御腿 | **2Y 钥匙**；K 窗口直接决定 2Y | K=132→1.50、**140→2.02**、150→2.00、160→1.47、180→1.40 |
| ② `trade_when(rank(adv20)>0.1)` + `scale(shortscale=0.5)` | 流动性过滤 + 空端缩放 | — |
| ③ `vector_neut(·, power(rank(rsk68_weight_dadv), 0.5))` | **investability 钥匙**（残差到 RISK 塔美元 ADV 轴）| 保留率 **57–65% → 70–73%** |

POW 档位 ↔ 两闸（K=140，investability 限 = 0.70×S）：
0.25 → 2Y 2.02 / 保留率 67.2% ❌｜**0.5 → 2Y 1.92 / 70.0% ✅（交点）**｜0.75 → 1.80 / 71.7% ✅｜1.0 → 1.56 / 73.2% ❌
⚠ 此为**旧结构（decay4）**下的档位；新结构（decay3 + sector + tail 0.25/0.75）下甜区移到 **0.80–0.85**，≥0.9 触发 ladder window 2→4 跳变、2Y 崩。

产出（`failed_ra_count = 0` × 4）：`zqrqpZX8`（S1.90/F1.16/2Y1.92/inv1.33/self0.397/prod0.729）、`KPmPa3xl`、`1YjY5A6m`、`kqJq56RO`；
另 `j2e2NQ9j`/`zqrqXz5V`（leg 换 `idiosyncratic_return_fraction`）。唯一剩余：prod 0.7275–0.7716（限 0.70）。

### 4.2【硬闸】八条硬结论（其中第 3 条已被裁决 A 收窄）

1. **面板「pv/risk 全红灯」应修正为「已试结构红」**（裁决 E）：`pv47`/`pv103`/`pv13`/`pv14` 与 `risk59/60/68/71` 均**不在判死名单**。
2. **`ts_kurtosis` 钥匙只对「日频收益/价量分布型」字段有效**（峰度=收益尾部风险=2022–23 防御轴）。
   4 个跨族数据集证伪（情绪/观点/M&A/动量）；换 `ts_kurtosis(波动率)` 也失效（2Y 崩到 0.49）。
3. ⛔ **「MARKET 是 KOR 唯一 F 与 2Y 兼顾档」**（同族对照：STATISTICAL F0.85/2Y1.51、INDUSTRY 1.10/1.20、SECTOR 1.09/1.50、
   MARKET 1.03/1.59；CROWDING F1.02/2Y1.42/保留率 59%、REVERSION_AND_MOMENTUM F0.82/1.50/57%）
   —— **数值仍有效，但「唯一」这个推广已被 §1.4 推翻**：同一族换个结构，REVMOM 反超 MARKET。
4. **`LOW_INVESTABILITY_CONSTRAINED_SHARPE` 限 = 0.70×S** ⇒ 需保留率 ≥70%。**KOR D1 只有 `TOP600`**；
   **`maxPosition` 对 KOR 不可用**、**`maxTrade=ON` 会把 S 从 1.88 打到 1.28**。115 条实验：过滤（移除/加权/条件翻转）、
   幂变换、纯多纯空、11 档中性化、市值/流动性中性化、外部通用配方**全部无效**；**唯一有效 = `vector_neut` 到 RISK 美元 ADV 轴**。
5. **「字段画像」只看单字段 S，看不到构造**（详见 §1.9）。
6. **prod 墙已定性为「密墙」**：窗（`ts_rank` 66/100/110/150/180/462）× POW（0.5/0.55/0.6/0.75）微调 ⇒ prod 恒 **0.7275–0.7344**；
   换腿语义（→`idiosyncratic_return_fraction`）⇒ **0.7715（更差）**。同族内无解 ⇒ **必须引入第二个经济维度**
   （合规形态：`trade_when` 条件 / `group_rank`+`bucket` 分组 / `vector_neut` 残差到非流动性轴）。
7. **钥匙适用性 = 字段的「分布形态」，不是「字段类别」**：同为「specific return」族，
   pv47 `spret` ✔（2Y 2.02）但 risk71 `dsrt`（% 单位 reproducible）✘（K 全扫 2Y 恒 0.91–1.16）；
   波动率峰度 ✘（0.49）、情绪/事件 ✘。**换族前先用 2 条探针验 K=140 的 2Y。**
8. **构型移植实测（勿重试）**：`rsk71_eqy_asi_supported_minvol1m_dsrt` S1.88/F1.07 但 2Y ≤1.16 ❌；
   `oth532_emerging/global_daily_specificreturn` TO **1.03**（日频 specific return 换手爆）❌；
   `anl10_smartest_*_pred_surps_*`（4 个 surprise 字段）S −1.03~0.26 ❌。
   ⇒ **PV 构型目前只在 `pv47_for_statssimple_only_spret` 上验证成功。**

### 4.3【实证】SH 构型（第二套已验证构型）

| 构型 | 适用字段形态 | 核心 | 验证字段 |
|---|---|---|---|
| **PV 构型**（S 型） | 日频收益分布型 MATRIX | 见 §4.1 | `pv47_for_statssimple_only_spret`（S1.90 / 4 颗 RA 全过） |
| **SH 构型**（流量/比率型） | VECTOR 比率/流量 | `hump(subtract(group_rank(divide(vec_sum(A),vec_sum(B)), industry), 0.5), hump=0.003)` | `shortinterest38` 买卖额比（S1.99 / prod0.6663 全闸过） |

**读数三分法（KOR 版）**：

| 双构型最好读数 | 动作 |
|---|---|
| S≥1.58 且 2Y≥1.58 | 全闸验证（**重点看 INV / CW**）→ prod/self → PnL 互相关去重（一条腿 1 颗） |
| S 1.0–1.58 | **不判死** —— 「构型没找对」；升级 K 窗/轴/POW/hump（实证 2Y 1.47→2.02） |
| S<0.5（双构型都） | 判死；同族免测 |

**KOR 特有：三道墙必须在探针阶段就预判** —— `LOW_INVESTABILITY` 限=**0.70×S**（PV 族必须套 `vector_neut(·,dadv)`）/
`CONCENTRATED_WEIGHT`（`group_rank` 族**必须** `hump(subtract(·,0.5))`，照抄旧表达式已不可用）/
`prod` 密墙（同族恒 0.727–0.734 ⇒ 靠 `industry` 轴或 `hump=0.005` 破）。

**探针批形状**：8 槽 = 2 个已验证构型 × 3 个跨概念族代表字段 + 2 机动（`vec_max`/`reverse`）。

**反例驱动的四条铁律**：① 先查历史构型再设计（自造结构 analyst 族全灭 vs 已验证构型 pv47 S1.90）；
② 只测一个构型会错杀（同字段换构型生死反转）；③ 发批前三闸 + KOR 不可用算子黑名单（一条错整批 CANCELLED）；
④ 判死前自检「真的双构型？真的跨族？2Y 单看是否钥匙失配？」。

### 4.4【实证】KOR「日频活跃」信号源极少（SH 构型的适用前提）

`shortinterest38`（TO 0.42–0.55）、`pv47`（TO 0.44）为已验证活跃者；
`shortinterest3`/`insiders5`/`fund_holdings_panel`/`ai_equity_alpha` 等 TO 全 < 0.31（多数 <0.1）⇒ SH 构型失效。
**判据：发批前用 `field_profile --query` 的 `to_med` 先排「低频近静态」字段。**

---

## 5 早期流程差异（S0–S5，来源 KOR profile）

- **S0 选集**：白名单只留绿榜与 untried 新集；按「信息维度是否已在 prod book 里」排序，别只看 coverage / alphaCount / valueScore
  （稀疏覆盖的高 valueScore 是陷阱）。红榜数据集即使用户点名，也先提示死路出处。
  ⛔ 旧句「analyst 族不再作主数据集」与「白名单只留绿榜（other466）」已被裁决 E 收窄：other466 现已点亮 ⇒ 反而要排除。
- **S1 字段**：typed catalog 双查，每个字段都要 longCount 与 type；longCount 低于 80 的 VECTOR 字段进观察名单
  （profile 要求按 FAIL 处理，代码里闸 7 仍是 WARN，由执行者把关）。**必须先做六法体检再写信号表达式**（§1.2）。
- **S2 生成**：⛔ 旧句「从 KOR × fundamental 出发（当前唯一活路）」已作废（fundamental 塔内的 other466 已点亮）；
  事件类数据集平台没有 `ts_event_*`，先单条探针确认字段能进标准算子。
- **S3 回测**：新数据集只给 **8 条探针预算**，没有 |S| 达 0.5 的就判死回写，不扩批、不换设置重试（小宇宙烧不起配额）；
  实证只有 delay 1，**不外推 delay 0**。
- **S4 改进**：判「不可能 / 天花板」前先扫等价算子替换（KOR 的「不可能三角」就是 `signed_power` 造成的）；
  CW 超过 0.5 判死不回炉（profile 要求，步 7 人工执行）；输入频率决定 2Y 与 IS 此消彼长 ——
  只有 `shortinterest38` 一个族的证据，作选区先验。
- **S5 提交**：同族一次只提 1 颗（兄弟连提会把后来者 prod 顶高）；prod 与 self 两个端点都实测。

---

## 6 工程坑补遗（不在 SKILL.md 通用「工程坑」里的本区特有项）

- `ts_target_tvr_decay` 可用但压 TO 时**等比例杀 S**（`ts_ir` / `ts_target_tvr_hump` 是连坐 FAIL，见 SKILL.md）。
- **僵尸批次判据修正**：`children=0` 且 `progress` 非空（0.35/0.9）**只是慢，不是僵尸**（实测卡 0.35 约 25 分钟后自行 COMPLETE）。
  multi-sim location 约 **24h 过期 ⇒ 当天收割**。
- **写脚本只用 ASCII 引号**（全角引号混入 heredoc 已致两次 SyntaxError）。
- **论坛工具 `search_forum_posts` 曾连续 4 次 `unexpected error`** ⇒ 当时改走 WebSearch 外部检索（工具可能已恢复，用前先单条试）。
- **平台算子目录过期**：`research-data/operators_platform_20260904.json` **缺 `vector_neut`**，但平台实际可用 ⇒ 以实测为准；
  `preflight` 会把算子名（`vector_neut`/`greater`/`shortscale`）误报为 `unknown_fields`（已知假阳性）。
- **论坛/网络类数据集**（`other545/546`、`equity_forum_data`、`other571`）2026-10-14 战役**整批平台 ERROR**（无报错信息），暂不可用。
- **单批 18 条会被并发限流截断 ⇒ 分批 6–8 条更稳。**

---

## 查台账（带日期的一次性产出一律以此为准，不在本文件维护）

| 要什么 | 命令 | 2026-10-15 实测覆盖 |
|---|---|---|
| **已提交颗数**（判「该数据集点亮没有」的当前真值）| `mcp__wqb-db__get_submit_ready(region="KOR", status="SUBMITTED", limit=200)` | ⚠ **12 颗，最新 2026-10-04**（缺 10-13 的 `rKdK2vLE`）|
| 待提交队列 | `mcp__wqb-db__get_submit_ready(region="KOR")`（缺省就是 `status="READY"`）| ⚠ **仅 1 行**：`LLZ6wZO2` S1.99 / prod 0.6762 / self 0.6760（2026-10-04 入队）|
| 判死记录与取证 | `mcp__wqb-db__get_dead_ends(region="KOR")` | ⚠ 最新 2026-10-05 |
| 波次结论 | `mcp__wqb-db__list_wave_results(region="KOR")` / `get_latest_wave` | ⚠ 最新 2026-10-04 |
| 单颗 alpha 的全 checks | `mcp__wq-brain-http__get_alpha_details(alpha_id=…)` | ✅ 平台侧（**本地 `alphas` 表查不到 10-09 后的 id**）|
| 跨区铁律（**全库，无区域参数**）| `mcp__wqb-db__get_cross_region_lessons()` | ⚠ 最新 2026-09-13 |
| 数据集级经验文档 | `reports/dataset_experience/kor_<ds>_campain.md`（区域码**小写**，`dataset_experience.py:223` 用 `region.lower()`；`campain` 是既定文件名，非笔误）| ⚠ KOR 仅 1 份（`kor_shortinterest38_campain.md`）|

⚠ **两个签名坑（`skill_lint` 2026-10-16 抓到，别再照旧写法调）**：
① `get_cross_region_lessons` **不收任何参数**（`inputSchema.properties = {}`，读的是 `registry_empirical` 的
`layer='cross_region'` 全库行）—— 写 `region="KOR"` 是凭空加参数。
② `get_submit_ready` 的 `status` **缺省是 `READY` 而不是全部**，且 `limit` 缺省 50 ⇒
数「已提交几颗」必须显式传 `status="SUBMITTED"` + 抬 `limit`，否则读到的是待提交队列。
另：该工具的 `status` 白名单是 `READY|SUBMITTED|DEAD|EXPIRED|SUPERSEDED|ALL`，
而 KOR 表里实际还有 **`PROD_BLOCKED`(2) / `SELF_BLOCKED`(2)** 两种状态**不在白名单里**
⇒ 那 4 行只能用 `status="ALL"` 取到，点名查会返回 `invalid status`。

### ⚠ 台账覆盖边界（2026-10-15 只读实测，别把「查台账」当成「一定有」）

**本文件 2026-10-09 ~ 10-15 的全部内容（d219–d282、六法体检三铁律、PV/SH 构型、`88voYna7` 配方、
prod 墙战役）在本地台账里没有任何对应行 —— S6 回写自 2026-10-04/05 之后就断了。**

| 表（KOR 口径）| 行数 | 最新时间戳 | 10-09 之后的战役 |
|---|---|---|---|
| `wave_results` | 121 | `created_at` 2026-10-04T03:01:54 | `wave_number LIKE 'd2%'` → **0 行** |
| `backtest_results` | 676 | `created_at` 2026-10-04T03:40:55 | 波号最大 `s2_*_d34` / `s2_xfam_d12` |
| `expressions` | 2267 | `created_at` 2026-10-04T18:12:39 | 波号最大 `d72_cond_vneut` |
| `registry_empirical` | 130 | `created_at` 2026-10-05T03:05:31 | 关键词 `88voYna7`/`d219`/`d232`/`oth695`/`pv47` → **0 命中** |
| `submit_ready` | 163 | `added_at` 2026-10-04T08:39:45 | `status` 分布 DEAD 108 / EXPIRED 34 / **SUBMITTED 12** / SUPERSEDED 4 / PROD_BLOCKED 2 / SELF_BLOCKED 2 / READY 1 |
| `alphas` | — | — | **id 级实证见下** |

**`alphas` / `submit_ready` 的 id 级核对**（本文件正文点名的 5 颗，2026-10-15 只读实测）：

| alpha id | 正文说它是什么 | `alphas` 表 | `submit_ready` 表 |
|---|---|---|---|
| `KPNo2lgl` | shortinterest38 已提交 S2.57 | ✅ `ACTIVE` | ❌ 无行 |
| `omLjG1M5` | shortinterest38 已提交 S2.28 | ✅ `ACTIVE` | ❌ 无行 |
| `rKdK2vLE` | **2026-10-13 提交的第 3 颗（点亮 shortinterest38 的那颗）** | ❌ 查不到 | ❌ 无行 |
| `88voYna7` | PV 构型配方代表颗 | ❌ 查不到 | ❌ 无行 |
| `zqrqpZX8` | 2026-10-09~13 战役 `failed_ra=0` 产出 | ❌ 查不到 | ❌ 无行 |

⇒ **断点就卡在 10-04/05**：连「shortinterest38 已点亮」这个**改变选集决策**的事实
（正文的「已提交 3 颗」）在库里也只有 2 颗有据，第 3 颗 `rKdK2vLE` 两表皆无。
⇒ 因此上面「查台账」表里**只有走平台的那一行（`get_alpha_details`）对 10-09 之后的战役有效**；
其余各行对那段都是空的或过期的，**这时以本文件的正文为唯一记录**。
⇒ 反过来：**「库里查不到」不等于「没提交过 / 不存在」**——本文件的 id 有 3/5 属这种形态。
判「某数据集点亮没有」时，两边都要看，冲突以平台 `get_alpha_details` + `get_user_alphas` 为准。

**复现本表**（只读，不写库）：结论行用 MCP 工具核——
`get_latest_wave(region="KOR")` / `list_wave_results(region="KOR")` / `get_dead_ends(region="KOR")` /
`get_submit_ready(region="KOR", status="ALL", limit=200)` / `get_alpha_by_id(alpha_id=…)`；
⚠ `get_cross_region_lessons()` **不带 region**（全库表）。
行数与最新时间戳走只读连接 `wqb.db_conn.connect(readonly=True)` +
`SELECT COUNT(*), MAX(created_at) FROM <表> WHERE region='KOR'`。
⚠ **两处列名坑**（都实测踩过）：① `alphas` 表没有 `region` 列（是 `region_id`，外键指向 `regions`），
照抄上面那句会报 `no such column: region`，查单颗直接用 `get_alpha_by_id`；
② `submit_ready` 表既没有 `created_at` 也没有 `updated_at` / `submitted_at`，
时间列是 **`added_at` 与 `verified_at`**。

**补齐动作属独立任务，不在 skill 治理范围内**：需要 ① 恢复被并行会话未暂存删除的
`tools/sync_platform_alphas.py`（当前**磁盘不存在**，AGENTS.md §8.4 第 10 条：处置归写入会话或用户）；
② 按平台日期区间重新收割 d219–d282 的 multisim 结果 → `harvest_multisim_results` / `upsert_alpha_from_platform`；
③ 再 `upsert_wave_result` 补波次结论。**不要手工把本文件的数字誊进库** —— 指标必须以平台回读为准。

*来源：KOR 2026-10-09 ~ 2026-10-15 全部战役（d219–d282），200+ 条回测实证。2026-10-15 从 SKILL.md 的
`profiles:manual` 块迁出（原 446 行，占该文件 67%）。*
