# KOR analyst 类别 Wave11–13 实证（2026-11）

> 结论一句话：**KOR analyst 全类别在 TOP600/D1 下是低频近静态区，横截面排序动不了收益。**
> 本轮 4 个数据集、3 种机制、10 条结构，最好 S=0.47，闸线 1.58。全灭不是结构问题，是**类别级 TO 死因**。

## 一、死因指纹（开波前应预筛）

| 读数 | 全部候选区间 | 判读 |
|---|---|---|
| turnover | **0.027 – 0.094** | 铁律 A/B：TO 远低于 0.125 ⇒ F 闸不吃紧，但**TO 低到 0.03–0.09 = 信号近乎静态**，横截面重排无法产生收益 |
| longCount+shortCount | 274 – 341 / 600 | 有效持仓仅一半，coverage 0.63 上限的必然结果 |
| risk_neutralized_sharpe | 普遍 ≈ raw 或更高 | RN 不背锅 ⇒ 死因是**信号自身无信息**，不是因子暴露拖累 |
| 逐年 S | 未逐年拆，但 2Y 闸全灭（0.24–1.08） | 近静态信号的 LADDER 必然塌 |

**预筛判据（下次开波前先跑）**：若候选族在 KOR 的 TO 上限 < 0.10，**不要扫窗口谱** —— 窗口只会改变幅度，改变不了「静态」这件事本身。

## 二、已判死的数据集与机制

| 数据集 | 机制 | 实测 | 死因 |
|---|---|---|---|
| `analyst_consensus` | 覆盖广度（水平） | S=-0.11 | 被规模/流动性完全吸收 |
| `analyst_consensus` | 覆盖广度（4wk/3m 变化） | S=0.47 / 0.30 / 0.06 | KOR 分析师覆盖**更新节奏极慢**，差分后有效变动稀疏 |
| `analyst_factor_signals` | 分歧度（coeff_var / asymmetry） | S=-0.09 / 0.26 | 同上，低频 |
| `analyst10` innovation | 创新性修正（Gleason-Lee） | S=0.22 / 0.43 | 论文机制在 KOR 迁移失效（TO 0.072） |
| `analyst11` | ESG 评分 | 未测 | **字段名骗人**：名为 analyst，实为 E/S/CIT 支柱 + OWL KPI 的 ESG 全集，低频状态量，预判死 |
| `analyst39` / `analyst15` / `analyst25` | — | 未测 | 扫描显示 alphaCount=0 / 13 / 24，已高度或完全拥挤 |

## 三、双通道取证结论（可复用）

### 通道 A：论坛（已修好，见下）

- **`search_forum_posts` 在长查询串下会 `fetch failed` / `internal_error`，短关键词（如「覆盖度」）正常** ⇒ 中文长 query 先砍短再试。
- `read_forum_post` `include_comments=true` 会 30s 超时，**false 正常** ⇒ 默认传 false，评论按需再补。
- 帖子 `34506025416087-Alpha灵感-分析师覆盖度因子`（LZ70706, 2025-08-28）
  骨架：`group_zscore(ts_mean(log(anl4_epsr_number+1),120), densify(bucket(rank(cap), range='0.1,1,0.1')))`
  USA/TOP3000 下 S=1.48→优化后成功提交。**在 KOR 直接符号翻转（S=-0.11）** ⇒ 论坛模板必须本区实测。
  作者给的破 sub-universe 手法：`base - group_mean(base,1,industry)` 取残差 + 中性化改 Sector。
- 帖子 `35417197662615-Alpha灵感-规避分析师覆盖中的羊群效应`（DW88214, 2025-10-05）
  来源：广发金工「如何利用聪明钱改进分析师预期因子」。要点：覆盖度只数数量不看质量，羊群会过度推高热门股覆盖。
  实证有效的修正：用**成交额/换手率过去半年分位**识别过热股，
  `if_else` 硬剔除 >95% 分位个股的覆盖度（S 1.63→1.85、F 1.09→1.34），或温和惩罚 `×(1-分位)/0.05`。
  ⚠ **回归取残差法实测不理想**，别走那条。

### 通道 B：外部论文（domain_search）

- **Gleason & Lee (2003, TAR)**：修正分「创新性」（新预测同时高于自身旧预测**与**一致预期）与「羊群性」（向共识靠拢）。市场对**创新性修正反应不足** ⇒ 后续漂移更大；羊群性修正几乎无漂移。低覆盖股漂移更强。
- **华泰金工（2024）**：普通修正幅度因子 2021 后衰落；改用「高创新性修正」+ 剔除 3 个月动量残差后，RankIC 3.99%、TOP 年化超额 9.55%。
- **Mill Street**：修正**方向**一个月后仍维持约 83%（收益本身仅 50%）⇒ 修正有持续性，这是可交易性的来源。breadth（上调占比）比 magnitude 更稳健，窗口约 100 天。
- **Jung, Keeley & Ronen (2019, JAAF)**：**未缩放**的 EPS 修正有效，缩放后失效；低覆盖股更强。
- **同济 Decomposing Analyst Consensus Revision**：sticky 分析师修正 FF6 alpha 0.85%/月（t=4.55），non-sticky 无。
- **Clement & Tse (2005)**：herded 预测**更不准**、含更少分析师私有信息。
- **反方**：Chan/Hwang/Mian 等认为「聚簇预测 = 共享信息」而非羊群，且共同基金追风会导致**反转**而非漂移。⇒ 方向需本区实测。

## 四、工程坑（省配额）

1. **`negate` 算子在 KOR 不可用**（`Attempted to use inaccessible or unknown operator "negate"`），整批 2 条直接 ERROR。
   ⇒ 一元负号必须写 `-x`。
   ⚠ **`preflight_expressions` 不拦它** —— 它把 `negate`/`densify`/`range` 当"未知字段"报出来，混在 `unknown_fields` 里极易误读成字段问题。**必须逐条自己判读 `unknown_fields` 属于字段还是算子。**
2. VECTOR 字段必须 `vec_avg`/`vec_max` 包裹；VECTOR 裸用 `rank`/`ts_*` 秒拒，**一条语法错 ⇒ 整批 CANCELLED**。
3. `count_net_income_*_4wks_prior` 这类「当前值 vs N 周前值」是**同一字段族的多时间窗**，属单信号结构化减法，合规（不触发禁混信号铁律）。

## 五、下一步转向建议

analyst 类别已按转向纪律判死。候选方向（均仍在 KOR/TOP600/D1，不换 region）：

- **回 KOR 已点亮塔的存量机制**：fundamental(3) / model(2) / shortinterest(2) / other(1) / pv(1) —— 历史 8 颗合规 REGULAR 提交即来自这些类别，说明本区**已验证可过闸**。
- 或本区**尚未点亮**的塔（若 `get_pyramid_alphas` 显示有缺口）。

⚠ 回存量机制前必先查 `tracking/KOR/kor_mining_full_workflow_and_lessons.md`：该文档记录 **2026-08-14→15 的 15+ 轮回测、上百表达式、0 达标**，说明纯靠盲扫在 KOR 已很难 —— 必须带机制假设开波，不能扫参。
