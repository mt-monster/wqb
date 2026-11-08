# AMR news73 跨区迁移战役（2026-11-03）

> 战役目标：把 GBR 的 NEWS 模板族迁移到 AMR，点亮 **AMR/D1/news 塔（当前 0/3）**。
> 靶位：**news73 Story by Story Sentiment**（cov 0.786 / 数据集 aC=27 / 字段级 aC 0–5 / valueScore 5 / 22 字段全 VECTOR）。
> 设置档（AMR 既有）：`AMR/TOP600/D1/SUBINDUSTRY/decay4/trunc0.08/VERIFY/nanHandling OFF/pasteurization ON/maxTrade OFF/FASTEXPR`。
> 闸线：**S≥1.58 / F≥1.0 / 2Y≥1.0**（全平台最松的 2Y 线）/ TO 1–70% / fRA=0 / prod<0.7 / self<0.7。

## §1 选靶理由

- AMR/D1 全 14 塔 news=0（`get_pyramid_alphas` 实测）。
- news73 是 **Dow Jones 分情绪**数据集：22 字段 = **per-entity 部分分**（`nws73_entitiessent_*partscr` 9 路：certainty/fear/findown/finhype/finup/finvolatile/negative/positive/uncertainty）+ **story-level 全局分**（`nws73_globalsent_*score` 9 路对应）+ 实体识别表。
- ⇒ **天然双层结构**：可以算「实体层情绪 vs 故事层情绪」的偏离，这是 GBR 五轴完全没有的新结构。
- 论坛帖 `43554159658647`「情绪通道的非对称：从 news85 看涨跌反应差」支持 fear/uncertainty 非对称轴；`43211291823511`（96 赞）支持双通道组合。

## §2 首波实测（6 组 SIG × 正负两极 = 12 条）

| tag | 轴 | 负极 alpha / S | 正极 alpha / S | 判读 |
|---|---|---|---|---|
| A_ent_vs_glob_pos | **实体分 vs 故事全局分（正情绪偏离）** | `JjeGOdPe` **−0.40** | `kqNP0KJO` **+0.40** | ✅ **严格对称，且是本轮跨区最强读数** |
| A_fear_axis | 恐惧部分分 | `O0AGZZGY` −0.02 | `3qopRRpe` +0.02 | ✅ 对称但**近乎无信号** |

**★★ 关键结论**：**「实体层 vs 故事层」的跨层偏离**是本轮跨区迁移挖出的**最强新结构**（|S| 0.40），
且 **GBR 五轴里完全没有它**（GBR 的 news17/news18 是单层聚合族，没有 entity↔story 两层可比）。

**对照**：
| region | 集 | 最强轴 | |S| | 闸线 | 差距 |
|---|---|---|---:|---:|---:|
| CHN | news46 | 密度 | 0.18（最优档） | 2.07 | 11.5× |
| HKG | news36 | 词数归一情绪 | 0.27 | 1.58 | 5.9× |
| **AMR** | **news73** | **实体-故事跨层偏离** | **0.40** | **1.58** | **4.0×** |

⇒ **三区都是「真但弱」，且 AMR 最强** ⇒ AMR 是三区里最有希望到达闸线的靶子。

## §3 wave2 增益波设计（11 条，已 preflight `valid=true`）

| tag | 杠杆 | 针对 |
|---|---|---|
| A2_dev_short | 短窗 22/66 | 情绪时效性 |
| A3_dev_long | 长窗 120/504 | 反向对照 |
| A4_dev_noshell | **去壳**（纯 rank） | 强度↑换手↑ |
| A5_dev_stat | 中性化 → STATISTICAL | 中性化族（CHN 已证因子型有毒，需独立验证） |
| A6_dev_fast | 中性化 → FAST | 同上 |
| A7_dev_d22 | decay 22 | 提 F |
| A8_devneg_pos | **负面跨层偏离轴（正极）** | 正负通道对照 |
| A9_devfear_pos | **恐惧跨层偏离轴** | fear 层的偏离（而非 fear 水平） |
| A10_devnet | 正负跨层偏离净额 | 双通道净值 |
| A11_dev_x_conf | 跨层偏离 × 确定性部分分 | 置信乘子 |
| A12_dev_delta | 跨层偏离的变化面 | 变化型信号 |

## §4 跨区参考

- GBR 模板总结速查：`docs/reference/gbr_news_template_summary_quickref_20261103.md`
- 字段语义映射：`docs/reference/news_template_field_semantic_map_20261103.md`
- 迁移 SOP：`docs/reference/cross_region_template_migration_sop_20261103.md`
- 完整归因：`docs/reference/gbr_news_template_summary_and_cross_region_migration_20261103.md`
## §2b 首波 12 条全收齐：六轴全部严格对称（真信号）

| tag | 轴 | 负极 alpha / S | 正极 alpha / S | \|S\| | 判读 |
|---|---|---|---|---:|---|
| A_uncertainty_axis | **不确定度部分分** | `d5WZ0Pvw` **−0.44** | `VkxGPRe8` **+0.44** | **0.44** | ✅ **本轴最强** |
| A_ent_vs_glob_pos | **实体分 vs 故事全局分** | `JjeGOdPe` −0.40 | `kqNP0KJO` +0.40 | 0.40 | ✅ |
| A_finhype_axis | **金融炒作度（finhype）** | `E56GENKL` −0.30 | `JjeGOopm` +0.30 | 0.30 | ✅ |
| A_finvolatile_axis | 金融波动强调 | `QPvG9ZVX` −0.18 | `Xg9o8mnb` +0.18 | 0.18 | ✅ |
| A_fear_axis | 恐惧部分分 | `O0AGZZGY` −0.02 | `3qopRRpe` +0.02 | 0.02 | ✅ 对称但近零 |
| A_entities_count | 实体识别计数 | `kqNPZdk8` −0.00 | `d5WZRpgX` +0.00 | 0.00 | ✅ 对称但无信号 |

**★★ 六组全部严格对称（|S| 完全相等、符号相反）⇒ AMR news73 的六个情绪通道轴全部是真信号**；
强度阶梯：**uncertainty 0.44 > 跨层偏离 0.40 > finhype 0.30 > finvolatile 0.18 >> fear 0.02 ≈ entities 0.00**。

### ★ 三个新轴（GBR 五轴完全没有）

| 轴 | 经济含义 | 机制 |
|---|---|---|
| **uncertainty（不确定度）** | 媒体对事件结果的确定性评估 | 「不确定 → 后续修正 → 收益漂移」；不确定性溢价（Miller + Barber-Odean 路径） |
| **finhype（金融炒作）** | 金融话题的炒作强度 | 过度反应 → 反转（Da et al. 注意力反转的变体） |
| **finvolatile（波动强调）** | 新闻中强调波动 | 波动预期传导到实际波动 → 后续收益偏负 |

### ⇒ wave3 窗口阶梯波（12 条，已派）

HKG 实测证明**窗口是主杠杆**（60/252 → 22/66 带来 2.4×），而 AMR 首波用的正是长窗 60/252 ⇒ **wave3 全面改短窗**：

| 格 | 内容 |
|---|---|
| 1-4 | 跨层偏离轴 × {5/66, 22/66, 22/126, 5/126} |
| 5-8 | finhype 轴 × 同四格 |
| 9-10 | **uncertainty 轴** × 22/66、5/66 |
| 11-12 | finhype × 22/66 + 中性化族对照（STATISTICAL / FAST） |

**判读口径**：找 S ≥ 1.0 的格；AMR 2Y 闸线 1.0（最松）⇒ S 过 1.0 即有机会。

## §5 ★★★★ wave3 窗口阶梯波收批（12 条，2 条 SUBMISSION_FAILED）

| tag | 轴 | 窗口 | alpha | S | F | TO |
|---|---|---|---:|---:|---:|---:|
| A3_dev_w22_66 | **跨层偏离** | **22/66** | `e753x5GO` | **−0.61** | −0.29 | 5.8% |
| A3_dev_w22_126 | 跨层偏离 | 22/126 | `wpQaEGRl` | −0.57 | −0.26 | 5.9% |
| A3_dev_w5_126 | 跨层偏离 | 5/126 | `E56GezwL` | −0.40 | −0.19 | 13.7% |
| A3_dev_w5_66 | 跨层偏离 | 5/66 | `zq3NR32E` | −0.18 | −0.06 | 14.1% |
| A3_hype_w5_66 | finhype | 5/66 | `2rApNgN5` | +0.17 | 0.05 | 12.9% |
| A3_hype_w5_126 | finhype | 5/126 | `vR1NvQ6A` | +0.04 | 0.01 | 12.6% |
| A3_hype_w22_66 | finhype | 22/66 | `O0AGxLGq` | −0.04 | −0.00 | 5.8% |
| A3_hype_short_d22 | finhype | 22/66 dec22 | `gJe88vE0` | −0.08 | −0.01 | 5.2% |
| A3_hype_short_stat | finhype | 22/66 STAT | `vR1NN03v` | −0.10 | −0.02 | 8.3% |
| A3_hype_w22_126 | finhype | 22/126 | `Xg9o80el` | −0.25 | −0.08 | 5.9% |
| A3_dev_short_stat | 跨层偏离 | 22/66 STAT | — | SUBMISSION_FAILED | — | — |
| A3_dev_short_fast | 跨层偏离 | 22/66 FAST | — | SUBMISSION_FAILED | — | — |

### ★ 三条结论

1. **跨层偏离轴短窗放大 1.5×**：长窗 60/252 = −0.40 → 短窗 22/66 = **−0.61**。
2. **窗口最优在 22 附近，不是越短越好**：5/66 = −0.18（过短反而弱），22/126 = −0.57。
   ⇒ 与 HKG 的 22/66 最优**独立同值**，两个 region 互相印证。
3. **AMR 不支持 STATISTICAL / FAST 中性化**（dev 轴上两条 SUBMISSION_FAILED，报错 `Neutralization FAST is not available for ... region AMR`）
   ⇒ **AMR 只能用分组型中性化**（SUBINDUSTRY / MARKET / SECTOR / INDUSTRY），与 CHN 同类；与 HKG（因子型是增益）相反。

### ⇒ wave2 重设计（11 条，原设计含 2 条会失败的中性化 + 2 条重复，已废弃）

原 §3 的 wave2 设计（A2_dev_short … A12_dev_delta）**已废弃**，原因：
- 含 STATISTICAL / FAST 中性化各 1 条 ⇒ AMR 会 SUBMISSION_FAILED（wave3 已实证）；
- 含 22/66、120/504 两格 ⇒ 与 wave1/wave3 结果重复。

**新 wave2（11 条，全分组型中性化，已 preflight `valid=true`）**：

| tag | 内容 | 针对 |
|---|---|---|
| A2_unc_w22_66 | **uncertainty 轴 22/66** | **最高优先**：uncertainty 是 AMR 已验证最强轴（±0.44），从未做短窗 |
| A2_unc_w10_66 | uncertainty 10/66 | 窗口细扫 |
| A2_unc_w15_66 | uncertainty 15/66 | 窗口细扫 |
| A2_unc_w22_30 | uncertainty 22/30 | 分位短 |
| A2_unc_w22_126 | uncertainty 22/126 | 分位长 |
| A2_dev_w10_66 | 跨层偏离 10/66 | 窗口细扫 |
| A2_dev_w15_66 | 跨层偏离 15/66 | 窗口细扫 |
| A2_dev_w30_66 | 跨层偏离 30/66 | 窗口细扫 |
| A2_dev_w22_30 | 跨层偏离 22/30 | 分位短 |
| A2_dev_w22_66_d8 | 跨层偏离 22/66 **decay 8** | HKG 实测 decay8 有增益（0.64→0.69） |
| A2_ndev_w22_66 | **负向跨层偏离** 22/66 | 正负通道对照 |

**判读口径**：uncertainty 若按 HKG 的 2.4× 窗口增益放大（0.44 → ~1.06），即进入可提交区间边缘；
dev 若 22/66 取正（+0.61）后继续细扫窗口，是第二条路径。

## §6 ★★★★ wave2 收批（11/11）：uncertainty 短窗单调放大

| tag | 轴 | 窗口 | alpha | S | F | TO |
|---|---|---|---:|---:|---:|---:|
| **A2_unc_w10_66** | **uncertainty** | **10/66** | `QPvG76xg` | **−0.79** | −0.44 | 8.0% |
| A2_unc_w22_30 | uncertainty | 22/30 | `1YNpxY3M` | −0.73 | −0.38 | 5.6% |
| A2_unc_w15_66 | uncertainty | 15/66 | `KPJGOaPj` | −0.65 | −0.33 | 6.4% |
| A2_unc_w22_126 | uncertainty | 22/126 | `rKR25KqE` | −0.63 | −0.32 | 5.9% |
| A2_dev_w22_66_d8 | 跨层偏离 | 22/66 dec8 | `j2Y6AlgE` | −0.61 | −0.29 | 5.7% |
| A2_dev_w22_30 | 跨层偏离 | 22/30 | `WjOAbw9o` | −0.53 | −0.23 | 5.7% |
| A2_dev_w10_66 | 跨层偏离 | 10/66 | `leAW8Xe7` | −0.49 | −0.22 | 7.6% |
| A2_unc_w22_66 | uncertainty | 22/66 | `d5WZjvME` | −0.46 | −0.20 | 5.8% |
| A2_dev_w30_66 | 跨层偏离 | 30/66 | `npvNK5Wq` | −0.41 | −0.16 | 5.6% |
| A2_ndev_w22_66 | 负向跨层偏离 | 22/66 | `P0oG2G5M` | −0.34 | −0.13 | 5.8% |
| A2_dev_w15_66 | 跨层偏离 | 15/66 | `3qop9vA6` | −0.16 | −0.04 | 6.3% |

### ★★★ 三条结论

1. **uncertainty 轴：窗口越短越强，单调** —— 22/66 −0.46 → 15/66 −0.65 → **10/66 −0.79**。
   **uncertainty 取代跨层偏离成为 AMR 最强轴**（原长窗 60/252 为 ±0.44）。
2. **分位维度非单调**：22/30 = −0.73 > 22/126 = −0.63 > 22/66 = −0.46 ⇒ **分位 30 附近最优**，不是越短越好。
3. **跨层偏离轴 22/66 是峰值**（−0.61，decay8 同值 −0.61）；负向通道（ndev −0.34）弱于正向。

### ★ 与 HKG 的对称对照

| region | 轴 | 窗口趋势 | 峰值 |
|---|---|---|---|
| HKG | 词数归一情绪 | 22/66 峰（5/66 崩，TO 28.8%） | +0.64 |
| **AMR** | **uncertainty** | **10/66 仍上升** | **−0.79** |

⇒ **同一「窗口是主杠杆」的规律在两区都成立，但最优点不同**（HKG 22 日 vs AMR 10 日）
⇒ 不能用一个区的最优点去推另一个区，**每区每轴都要独立扫窗口**。

### ⇒ wave3（12 条，已 preflight `valid=true`，在飞）

沿 10/66 继续往 **5/7/8 日**推进，并测 10/30、10/126、10/252 的分位维度；
另加 **2 条正极镜像**（10/66、22/30）验证「取正」是否成立（双极判据）。

**判读口径**：若 5/66 或 7/66 超过 −0.9，则 AMR 距闸线 1.58 只差 1.6×，
届时可考虑「取正 + 换数据集（news59 / news85）」两条路并行。## §7 ★★★★ wave3 全收（12/12）：uncertainty 峰值在 10/126–10/252（**−0.92**）

| tag | 轴 | 窗口 | S | F | TO |
|---|---|---|---:|---:|---:|
| **A3_unc_w10_126** | **uncertainty** | **10/126** | **−0.92** | −0.55 | 8.1% |
| **A3_unc_w10_252** | **uncertainty** | **10/252** | **−0.92** | −0.60 | 8.0% |
| A3_unc_w10_66_POS | uncertainty（正极） | 10/66 | **+0.79** | 0.44 | 8.0% |
| A3_unc_w22_30_POS | uncertainty（正极） | 22/30 | +0.73 | 0.38 | 5.6% |
| A3_unc_w8_66 | uncertainty | 8/66 | −0.35 | −0.14 | 9.2% |
| A3_unc_w7_66 | uncertainty | 7/66 | −0.34 | −0.14 | 9.7% |
| A3_unc_w10_30 | uncertainty | 10/30 | −0.34 | −0.13 | 7.4% |
| A3_unc_w10_66_d8 | uncertainty | 10/66 decay8 | −0.28 | −0.09 | 7.5% |
| A3_unc_w5_66 | uncertainty | 5/66 | −0.24 | −0.09 | 12.4% |
| A3_dev_w10_30 | 跨层偏离 | 10/30 | −0.33 | −0.13 | 7.8% |
| A3_dev_w10_66_POS | 跨层偏离（正极） | 10/66 | +0.49 | 0.22 | 7.6% |
| A3_ndev_w10_66 | 负向跨层偏离 | 10/66 | −0.11 | −0.02 | 7.6% |

### ★★★ 四条结论

1. **分位拉长反而更强**：10/66 = −0.79 → **10/126 = −0.92、10/252 = −0.92**。
   与 HKG「分位缩短更敏感」（22/126 0.56 < 22/66 0.64）**方向相反** ⇒ 再次印证「每区每轴的最优窗口/分位不同」。
2. **平滑窗不是越短越好**：10/66 −0.79 是峰值；8/66 −0.35、7/66 −0.34、5/66 −0.24 全部更弱。
3. **decay8 是毒档**：10/66 从 −0.79 掉到 −0.28（HKG 上 decay8 反而是增益 0.64→0.69）⇒ **decay 档同样区域特异**。
4. **正极镜像成立**：10/66 正极 +0.79（vs 负极 −0.79，严格对称）、22/30 正极 +0.73（vs −0.73）
   ⇒ 双极判据确认 uncertainty 是**真信号**，取正可得 +0.79。但 **10/126 / 10/252 的正极未测**（预期 ≈ +0.92）。

### ⇒ wave4（12 条，已 preflight `valid=true`，已派）

测**乘子结构**（L6 线索：GBR 上 `event_similarity_days` 当乘子 S 1.85、当本体 −0.33）：
uncertainty × {跨层偏离, finhype, finvolatile, certainty, 全局正/负情绪}，窗口 10/66 与 22/66。


---

## §8 wave4（乘子结构）全收 12/12 —— 乘子轴判死

| 表达式 | S | 备注 |
|---|---:|---|
| M3_unc_x_finvol | −0.68 | 同族稀释 |
| M4_unc_x_cert | −0.62 | 同族稀释 |
| M5_unc_x_globpos | −0.65 | 同族稀释 |
| M6_unc_x_globneg | −0.37 | 同族稀释 |
| M7_dev_x_hype | −0.23 | 同族稀释 |
| M8_dev_x_vol | −0.49 | 同族稀释 |
| M9_dev_x_cert | −0.25 | 同族稀释 |
| M10_unc_x_dev | −0.49 | 同族稀释 |
| M1_hype_x_unc | −0.18 | 同族稀释 |
| M2_unc_x_hype | −0.46 | 同族稀释 |

**结论（已写入主记忆）**：基座 uncertainty 10/66 = −0.79，10 个乘子**全部稀释**（−0.18…−0.68）。
⇒ **乘子字段必须与信号不同源**；同族打分类字段相乘只是放大噪声。
对照 GBR L6：`event_similarity_days` 当乘子 S 1.85（有效）是因为它与信号**正交**，不是同族。

## §9 wave7（峰值回差 ts_max_diff）全收 12/12 —— 判死

- 最优 **−0.23**（JjeG1VrA），次 −0.21（xArN5M7b），其余 |S| ≤ 0.13。
- **换手 0.57–1.02（57%–102%）**，是全 AMR 最高的一批 —— `ts_max_diff` 几何天然制造高换手。
- 结论：**峰值-回差几何在 AMR 无效**（源帖 EUR/earnings S 1.69 的结果未能迁移）。

## §10 wave8（ts_covariance 情绪模板）全收 12/12 —— 弱

| alpha | S | F | TO |
|---|---:|---:|---:|
| qMLNw1rZ | **+0.52** | 0.29 | 3.81% |
| e753Gm1E | +0.45 | 0.22 | 5.68% |
| zq3N0g3o | −0.35 | −0.16 | 3.66% |
| npvNQVlw | +0.33 | 0.14 | 3.82% |
| rKR28Eja | +0.30 | 0.12 | 7.27% |
| 其余 7 条 | ≤ +0.25 | | |

- 结论：`ts_covariance(负向, 正向, d)` 在 AMR 只到 **+0.52**，远低于 uncertainty 的 0.92 ⇒ **该模板不是 AMR 的主杠杆**。

## §11 在飞 / 待派（2026-11-03 16:10）

- **在飞**：HKG wave10（峰值回差，链式第二段）、HKG wave12（ts_zscore 分布概率差）。
- **待派**：AMR wave9（ts_zscore 分布概率差）、HKG wave13（sign 持续性）、AMR wave5/6、HKG wave6/7/8/11、EUR news36。
- **当前 AMR 最强仍是 uncertainty 10/126 / 10/252 = −0.92**（距闸 1.58 差 1.7×）。
