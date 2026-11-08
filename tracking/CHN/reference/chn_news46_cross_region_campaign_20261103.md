# CHN news46 跨区迁移战役记录（2026-11-03）

> 战役目标：把 GBR 的 NEWS 模板族迁移到 CHN，点亮 **CHN/D1/news 塔（当前 0/3）**。
> 靶位：**news46 Relevant News Analytics Data**（cov **1.0** / 数据集 aC=7 / 字段级 aC 0–4 / valueScore **6** / 37 字段全 VECTOR）。
> 设置档（既有）：`CHN/TOP2000U/D1/SUBINDUSTRY/decay4/trunc0.08/VERIFY/nanHandling OFF/pasteurization ON/maxTrade OFF/FASTEXPR`。
> 严闸：**LOW_SHARPE 2.07** / F≥1.0 / 2Y≥1.6 / TO 5–30% / fRA=0 / prod<0.7 / self<0.7。

## §1 波次总账

| 波 | 主题 | 条数 | 设置 | 结果 |
|---|---|---:|---|---|
| wave1 | 12 语义槽位模板（结构互异） | 12 | BASE 档 + 壳 | **12/12 全弱**（S −0.84 ~ +0.25），TO 塌到 4–7% |
| wave1b | A/B 2×6 因子（设置档 × 壳） | 12 | FAST15+壳 / BASE+裸 | **FAST 档一致放大 0.36–0.90**；壳不是主因 |
| wave1c | 正向几何换面（4 种几何） | 12 | FAST15 + 壳 | **4 几何一致 −1.06 ~ −1.24** ⇒ 注意力反转机制成立 |
| wave1d | 正向几何取负（验证翻正） | 12 | FAST15 + 壳 | 进行中 |
| 待发 | CHN news38（真·正负双通道） | 12 | BASE 档 + 壳 | 模板池 + preflight 已就绪 |
| 待发 | HKG news36 | 12 | HKG 档 SECTOR/decay4 | 模板池 + preflight 已就绪 |
| 待发 | AMR news73（per-entity vs story 双层 + fear/uncertainty） | 12 | AMR 档 SUBINDUSTRY/decay4 | 模板池 + preflight 已就绪 |

## §2 wave1 实测（BASE 档 + 壳）

| tag | alpha | S | F | TO | 归因 |
|---|---|---:|---:|---:|---|
| C1 密度反转 | `YP1vNmg6` | 0.18 | 0.05 | 5.6% | 逐年 S 0.84/1.40/−0.85，有残响 |
| C2 nip×returns corr | `LLMGn6d9` | −0.69 | −0.40 | 6.2% | 方向与 EUR 相反 |
| C3 nip×returns cov | `e753n2gp` | −0.51 | −0.25 | 5.7% | 与 C2 同机制面 |
| C4 双情绪协方差 | `npvNnzYz` | −0.46 | −0.25 | 4.1% | TO 低于闸下限 |
| C5 **GBR S1 结构直移植** | `MPYGbpe9` | **0.03** | 0.00 | 6.8% | ★ 几何/字段都对，是档位压平 |
| C6 注意力稀释 | `npvNnge3` | −0.30 | −0.11 | 5.8% | |
| C7 时间链年龄 | `leAW7jb2` | −0.37 | −0.17 | 5.9% | |
| C8 链位序 | `akK1N7q1` | −0.76 | −0.45 | 5.3% | 本批最强负 |
| C9 实体-故事偏离 | `9qxp9W3r` | **0.00** | — | **0.0%** | ⛔ 退化：`ess` 与 `storyid_ess` 同口径两层 |
| C10 全球vs本地新颖度 | `P0oGngbx` | −0.35 | −0.17 | 9.1% | TO 最高 |
| C11 社论观点分 | `d5WZnazJ` | **0.25** | 0.09 | 5.9% | 本批最正 |
| C12 冲击-相关价差 | `KPJGngQx` | −0.84 | −0.55 | 5.9% | 本批最强负 |

**逐年覆盖**：3 条实测全 10/10 年有 pnl + longCount 15–40 ⇒ 无 leading-gap。**fRA 全部 4–7**（含 WARNING 级）⇒ 全部不可入库。

## §3 wave1b A/B 配对（决定性）

| SIG | FAST15+壳 | BASE+裸 | ΔS |
|---|---:|---:|---:|
| 密度 | −0.74 | +0.16 | **−0.90** |
| 稀释比值 | −1.03 | −0.26 | −0.77 |
| nip×cov | −1.19 | −0.53 | −0.66 |
| **乘性置信（GBR S1）** | −0.62 | **−0.01** | −0.61 |
| nip×corr | −1.19 | −0.71 | −0.48 |
| 双情绪协方差 | −0.82 | −0.46 | −0.36 |

⇒ **6/6 条 FAST 档放大** ⇒ 跨区迁移第一动作 = 换档。

## §4 wave1c 换面几何一致性（机制判决）

| 几何 | alpha | S | TO |
|---|---|---:|---:|
| `ts_rank(ts_mean(count,60),252)` | `YP1vQWwl` | −1.24 | 9.4% |
| `ts_zscore(ts_mean(count,60),252)` | `vR1NdJx3` | −1.17 | 10.0% |
| `ts_max_diff(ts_mean(count,22),5)` | `9qxpJpA2` | −1.09 | 10.1% |
| `ts_delta(ts_mean(count,22),5)` | `E56GkGr9` | −1.06 | 10.7% |

⇒ 四种几何一致给出负暴露 + returns/margin 同为负 ⇒ **「新闻事件密度高 ⇒ 未来收益低」在 CHN 真实成立**（Da et al. 2011 注意力反转的跨区复现）。
⇒ wave1d 在正向几何上取负（`−ts_zscore` / `−ts_rank`）验证翻正，同时满足 CHN「反转型必须换结构不取负」的死路。

## §5 待解的墙

1. **严闸 2.07**：wave1c 最强负暴露 −1.24 ⇒ 翻正后约 +1.2，**仍不够 2.07**。出路 = 强几何 + 字段组合增益（不是单字段单结构）。
2. **fRA 4–7**：所有件 RA 失败（含 WARNING）⇒ 需查具体 checks（大概率 LOW_SUB_UNIVERSE_SHARPE + LOW_SHARPE）。
3. **robust 墙**：CHN 既有死路提示情绪-关注度价差族有 robust 子宇宙墙；news46 机制不同但需实测。

## §6 跨区同源参考

- GBR 模板总结：`docs/reference/gbr_news_template_summary_quickref_20261103.md`
- 字段语义映射：`docs/reference/news_template_field_semantic_map_20261103.md`
- 完整归因：`docs/reference/gbr_news_template_summary_and_cross_region_migration_20261103.md`
- GBR 原始台账：`docs/reference/template_library_gbr_news_strong_geometry.md` §14/§15
## §5b ★★★ RA 明细实测（get_alpha_details，2026-11-03）

样本 `YP1vQWwl`（wave1c G1，正向 ts_rank 密度，FAST15 档）：

```
ra: { failed_ra_count: 5, failed_ppa_count: 2, ra_failed: true, ppa_failed: true,
      ra_failed_checks:  [LOW_SHARPE, LOW_FITNESS, LOW_RETURNS, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE],
      ppa_failed_checks: [LOW_SHARPE, LOW_SUB_UNIVERSE_SHARPE],
      pyramid_short: "news" }

checks.fail:    LOW_SHARPE -1.24 / 2.07 | LOW_FITNESS -0.77 / 1 | LOW_RETURNS -0.0482 / 0.08
                LOW_SUB_UNIVERSE_SHARPE -1.15 / -0.88 | LOW_2Y_SHARPE -1.83 / 2.07
checks.warning: CLUSTER_TEST -0.75 / 1.58 | MATCHES_THEMES
checks.pass:    LOW_TURNOVER | HIGH_TURNOVER | CONCENTRATED_WEIGHT
                LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO | LOW_ROBUST_UNIVERSE_RETURNS | MATCHES_PYRAMID
checks.pending: SELF_CORRELATION | DATA_DIVERSITY | PROD_CORRELATION | REGULAR_SUBMISSION
pyramids: { effective: 1, list: [{ name: "CHN/D1/NEWS", multiplier: 1.7 }] }
```

### 三条关键读数

1. **CHN 严闸双线确认**：LOW_SHARPE **limit 2.07**、LOW_2Y_SHARPE **limit 2.07**（比 GBR 的 1.58 严得多）。
   ⇒ 要出货必须 S≥2.07 **且** 2Y≥2.07；CHN 的 2Y 线与 S 线同高，比多数区域更难。
2. ★★ **失败项全部是「负号造成」**：五个 fail 的 value 全为负（−1.24 / −0.77 / −0.0482 / −1.15 / −1.83）⇒ **wave1d 取负后五项全部翻正**，fRA 预计从 5 → 0 或仅剩 magnitude 不足。
3. ★★★ **CHN/D1/NEWS 塔倍率 = 1.7**（`pyramids.effective=1`）⇒ **点亮 NEWS 塔的实际收益是 1.7 倍**，是 CHN 14 塔里高价值目标之一（vs OTHER 1.9 / MODEL 更高但禁混）。
4. ⚠ **CLUSTER_TEST warning −0.75（limit 1.58）**：CHN 的主题簇检查不通过（= 无主题簇重叠，是好事，但值 < 1.58 会被记 warning）。⇒ 候选入库时 WARNING 级也要算 fRA 失败（用户口径），但这条与收益无关，属可接受噪声，需在终验时确认平台是否计入 fRA。

## §5c 出货判据修订（基于 RA 明细）

CHN news46 要出货需同时满足：**S ≥ 2.07 且 2Y ≥ 2.07 且 F ≥ 1.0 且 returns ≥ 0.08 且 SUB ≥ −0.88**。
当前最强负暴露 −1.44（G6 avdiff，TO 28.3%）⇒ 翻正后 S≈1.44 **仍差 0.63**。
⇒ **必须叠增益**：① 换更强字段组合（news38 真双通道 / news73 双层）；② 换 universe（CHN 仅 TOP2000U，无档可换）；③ 换中性化档（FAST 已用，SLOW/SLOW_AND_FAST/CROWDING 未测）；④ 提高 decay 降换手（TO 28%→<15% 可提升 margin 与 F）。

**下一波（wave1e）方向已定**：SLOW_AND_FAST + decay 22/30 的高换手抑制档 × 胜出几何（zscore/avdiff）× 高强度字段组合。
## §6 wave1f 单因子隔离结果（部分，2026-11-03 13:4x）

基准 SIG = `-ts_rank(ts_mean(vec_count(mws46_story_count), 60), 252)`；基准档 = CHN/TOP2000U/D1/SUBINDUSTRY/decay4/壳/带 group（wave1 C1 = **+0.18**）。

| tag | 剥离的因子 | alpha | S | F | TO | 判读 |
|---|---|---|---:|---:|---:|---|
| F3 | 去 `group_neutralize(market)` | `N1NbO7NL` | **+0.18** | 0.05 | 5.6% | 与基准一致 ⇒ 分组轴**非**拖累源 |
| F4 | 去壳 + 去组 | `mLo5Xjap` | **+0.17** | 0.05 | 9.4% | 与基准一致 ⇒ 壳 + 分组轴**都非**拖累源 |
| F7 | 中性化改 FAST + 去壳（decay 仍 4） | `e753r1Jl` | **+0.16** | 0.05 | 9.4% | ★ **FAST 中性化本身非拖累源**（此前 FAST 与 decay15 混在一起） |
| F10 | 中性化改 MARKET（decay 4） | `YP1vNmg6` | **+0.18** | 0.05 | 5.6% | 与基准同值 ⇒ 中性化档在该轴无影响 |

### ★ 隔离结论（收敛中）

**拖累源 = `decay` 档，不是中性化档、不是壳、不是 group_neutralize。**

证据链：BASE(decay4) = +0.18；FAST+**decay4**+裸 = +0.16（FAST 单独无影响）；而 wave1b 的 FAST**15** = −0.74（BASE 裸仅 +0.16）。
⇒ **decay 4→15 这一步把 +0.18 变成 −0.74**。

**这与 GBR 的出货档（FAST + **decay 15**）直接冲突** ⇒ 说明「decay15 是 GBR 出货档」是**区域特异**的，不是普适参数。
⇒ **跨区迁移的第三条铁律（新增）：设置档不能照抄源区，必须在目标区做单因子隔离**（中性化 / decay / 壳 / 分组轴各一格）。

⚠ 待验证：F5（decay 4→22）与 F6（FAST + decay4 + 壳）尚未收齐；若 F5 同样负向，decay 假设置信；
若 F5 仍为正，则真正的负漂来自 decay 与 FAST 的**交互**（FAST+15 才有，FAST+4 无）。
### ★★ 隔离波定位结果（修正：拖累源 = FAST 中性化 × 壳 的交互）

| tag | 设置 | alpha | S | TO |
|---|---|---|---:|---:|
| F1 | SUBINDUSTRY / decay4 / 壳 / 带组（基准） | `YP1vNmg6` | **+0.18** | 5.6% |
| F2 | 同上，**去壳** | `e753r1Jl` | +0.16 | 9.4% |
| F3 | 同上，**去 group_neutralize** | `N1NbO7NL` | +0.18 | 5.6% |
| F4 | 同上，**去壳 + 去组** | `mLo5Xjap` | +0.17 | 9.4% |
| F5 | SUBINDUSTRY / **decay 22** / 壳 / 带组 | `9qxpRM6q` | +0.09 | 4.7% |
| F6 | **FAST** / decay4 / 壳 / 带组 | `1YNpgKmm` | **−0.67** | 9.9% |
| F7 | **FAST** / decay4 / **去壳** / 带组 | `e753r1Jl` | **+0.16** | 9.4% |

### 判决（改写先前的 decay 推断）

1. **FAST 中性化单独就是拖累源**：F6 = **−0.67**，而同结构 SUBINDUSTRY = +0.18。
2. **但 FAST 只在「带壳」时有害**：F7（FAST + 去壳）= **+0.16**，与 BASE 裸几何同值 ⇒
   ⇒ **真正的拖累源 = FAST 中性化 × `ts_target_tvr_decay` 壳 的交互**。
3. **壳单独无害**（F2 去壳 +0.16、F4 去壳去组 +0.17）；**分组轴单独无害**（F3 +0.18）；**decay 单独升档无害**（F5 +0.09）。
4. ⇒ **最初的 FAST15 波（−0.74…−1.44）应归因于「FAST+壳+decay15」三件套**，而非任一单件。

### ★★★ 由此产生的跨区迁移铁律（第四条，替换此前「换档放大」的错误读法）

> **设置项不是独立的，是有交互的。** 「A 档 vs B 档」的 S 差**不能**归因给 A 或 B 单方；
> 换区时必须做 **单因子隔离波**（基准 → 去壳 → 去分组 → 换中性化 → 换 decay → 换 target_tvr），
> **每次只动一格**，找出真正的拖累源（含交互对）。

**为什么这条最重要**：GBR 出货档 = FAST + decay15 + 壳（换手目标 0.05），在 GBR 全绿；
同一套搬到 CHN 全负。若只做「换档 A/B」，会把 **FAST×壳的交互**误读成「FAST 是放大器」，进而错误地沿负方向去取负 —— 那正是 wave1c/wave1d 走偏的原因。

### 对后续波的直接指示

- CHN 的**可用基底 = SUBINDUSTRY/decay4 或 SUBINDUSTRY/decay22 + 去壳或 FAST + 去壳**（F1/F2/F3/F4/F5/F7 全部 ≈ +0.1…+0.18）。
- 由于 F1–F7 全部只到 **+0.18**（离 CHN 严闸 2.07 差一个数量级），⇒ **news46 密度轴在 CHN 几无横截面定价力**，应判死该轴，转 news38（真双通道）/ news73（双层+恐惧轴）/ 或闸线更松的 HKG / AMR。
- 后续波**统一用「无壳 + SUBINDUSTRY/decay4」基底**（F2/F4 已验证无拖累，且换手可控）。
### ★★★★★ wave1f 单因子隔离波 12/12 全收齐 —— 毒档定位闭环

基准 SIG = `-ts_rank(ts_mean(vec_count(mws46_story_count), 60), 252)`；除指定项外其余设置全同（CHN/TOP2000U/D1/decay4/壳 target_tvr=0.05/带 group_neutralize(market)）。

| tag | 变动的设置 | alpha | S | F | TO | 归因 |
|---|---|---|---:|---:|---:|---|
| F1 | 基准（SUBINDUSTRY / decay4 / 壳 / 带组） | `YP1vNmg6` | **+0.18** | 0.05 | 5.6% | 基准 |
| F2 | 去壳 | `e753r1Jl` | +0.16 | 0.05 | 9.4% | 壳**非**拖累源 |
| F3 | 去 group_neutralize | `N1NbO7NL` | +0.18 | 0.05 | 5.6% | 分组轴**非**拖累源 |
| F4 | 去壳 + 去组 | `mLo5Xjap` | +0.17 | 0.05 | 9.4% | 二者都非拖累源 |
| F5 | decay 4→22 | `9qxpRM6q` | +0.09 | 0.02 | 4.7% | decay 单独升档**非**拖累源 |
| F6 | **中性化 → FAST** | `1YNpgKmm` | **−0.67** | −0.31 | 9.9% | ⛔ **因子型中性化 = 毒档** |
| F7 | **FAST** + 去壳 | `j2Y6gKk9` | **−0.76** | −0.36 | 13.1% | ⛔ 去壳救不回 FAST |
| F8 | **中性化 → STATISTICAL** | `RREmrwxe` | **−0.74** | −0.33 | 7.8% | ⛔ 同族同负 |
| F9 | **中性化 → SLOW** | `wpQaerj6` | **−0.76** | −0.35 | 7.8% | ⛔ 同族同负 |
| F10 | **中性化 → MARKET** | `E56GKdlG` | +0.08 | 0.02 | 4.8% | ✅ 分组型安全 |
| F11 | 分组轴 market→industry | `2rAp7MAZ` | +0.18 | 0.05 | 5.1% | ✅ 换组轴无害 |
| F12 | target_tvr 0.05→0.15 | `QPvGaMvW` | +0.16 | 0.05 | 9.8% | ✅ 壳目标换手无害 |

### ★★★ 判决：拖累源 = **因子型中性化**（FAST / STATISTICAL / SLOW），不是壳、不是分组轴、不是 decay、不是 target_tvr

| 中性化 | 族 | S |
|---|---|---:|
| SUBINDUSTRY | 分组型 | +0.18 |
| MARKET | 分组型 | +0.08 |
| FAST | 因子型 | −0.67 |
| STATISTICAL | 因子型 | −0.74 |
| SLOW | 因子型 | −0.76 |

**机理**：因子型中性化剥离的是**风格/因子暴露**；「新闻事件到达率」这类信号**本身就是因子暴露**，剥离后留下与原信号**反向**的残差 ⇒ 系统性负漂。分组型只减组均值，不制造符号翻转。

### ★ 跨区迁移铁律（第四条，替换此前「换档放大」的错误读法）

> **设置项之间存在交互，不能把 S 差归因给单方。** 「A 档 vs B 档」必须用**单因子隔离波**（基准 → 去壳 → 去组 → 换中性化 → 换 decay → 换 target_tvr），每格只动一项，才能定位真正的毒档（含交互对）。

**为什么这条最关键**：GBR 出货档 = **FAST** + decay15 + 壳，在 GBR 全绿；同一套搬到 CHN 全负。
若只做「换档 A/B」，会把结果误读成「FAST 是放大器」，进而沿负方向去取负 —— 那正是 wave1c/wave1d 走偏的根源。

### news46 密度轴终局判决

**最优档（SUBINDUSTRY/decay4）也只有 S = +0.18**，离 CHN 严闸 2.07 差一个数量级；
且 6 种换面几何在 FAST 档的 −1.06…−1.44 全是中性化毒档造成，不是信号。
⇒ **news46 密度轴在 CHN 判死**（无横截面定价力）。后续转：
1. **CHN news38**（真·正负双通道，`mws38_positive_score`/`negative_score`）—— 已派正负两极波；
2. **HKG news36**（闸线 1.58/1.6，字段级 aC 0–14，含 novelty 时间链 + 正负置信 + 词数归一分母）—— 已派正负两极波；
3. **AMR news73**（per-entity 分情绪 vs story 全局分双层 + fear/uncertainty/finhype 新轴）—— 模板池已就绪待发。

### ★ CHN 的可用设置档（供后续所有波复用）

**分组型中性化（SUBINDUSTRY / MARKET / SECTOR / INDUSTRY）+ decay 4–22 + 壳 target_tvr 0.05–0.15**；
**禁用 FAST / STATISTICAL / SLOW / CROWDING / SLOW_AND_FAST**（因子型，会制造负漂）。