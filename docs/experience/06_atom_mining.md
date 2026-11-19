# 06 · ATOM 挖掘经验（外部文章蒸馏 + 本仓校验）

> **来源**：微信公众号文章《为什么你现在应该多做 ATOM》（https://mp.weixin.qq.com/s/1nhN8rmGF-gFvHSSHr2Y6A），2026-11-17 抓取全文（标题实读，正文约 1.1 万字符，已存 `logs/_tmp_wechat_atom_article.txt`）。
> **效力**：**外部经验，非本仓实测**。凡标「⚠本仓校验」的段落，是本仓对照平台读数后补的差异/修正；
> 未标注的属原文主张，用前按项目既有纪律复核（`get_pyramid_multipliers` / `get_alpha_details` 实读）。
> **与本仓的关系**：本文是 [[atom-pyramid-rules]] 的外部佐证与补充，两者冲突时以本仓实测为准，冲突点见 §7。

---

## 1. ATOM 定义与豁免字段

**ATOM = 整个表达式只用一个数据集的字段**，额外只允许 6 个基础分组字段：
`country / exchange / market / sector / industry / subindustry`
（部分提交文档另提 `currency / split / adjfactor`；稳妥做法是只用这 6 个，或直接在 Settings 面板选中性化）。

---

## 2. 三大制度红利（这是 ATOM 优先的量化依据）

### 2.1 免除 2Y–10Y 的 IS-Ladder 阶梯测试

| 区域 / 类型 | 常规 Alpha 的 2Y 阈值 | SuperAlpha |
|---|---:|---:|
| 非 CHN，D1 | **1.59** | 2.38 |
| CHN，D1 | **2.08** | 2.38 |

- **低换手折扣（⚠ 本仓未复现，勿照用）**：外部文章称 `Turnover < 30%` 时阈值 ×0.85（⇒ 1.35）。**2026-11-17 判别件 `YP1ZvjWA`（TO 17.7% / 2Y 1.57 / limit 1.58）与 `gJaR5gov`（TO 5.39% / limit 仍 1.58）双双反例 ⇒ 近闸线一律按 **1.58**，不要用 1.34 / 1.35**（见 `01_platform_gates.md` §1 与本文件 §2.1）。
- 判据：回测后 `IS Testing Status` 出现 `2 year Sharpe of <value> is above cutoff of <limit>` 即过关。
- ⚠本仓校验（2026-11-17 升级为**两点实测**，见 [[atom-pyramid-rules]]）：
  1. **「2Y 阈值 1.59」实测为 1.58**——`gJaR5gov` 的 `LOW_SHARPE` 与 `LOW_2Y_SHARPE` 的 limit 都打印 **1.58**（平台 checks 原文），与本仓闸表 `src/wqb/config.py` 一致。文章的 1.59 与本仓读数差 0.01，**以平台 checks 实读为准**。
  2. **「TO<30% ⇒ ×0.85」在 DEU 被直接反例否掉**——`gJaR5gov` = **TO 5.39% / 2Y 1.08 / limit 仍 1.58**：换手远低于 30%，阈值却没有打 0.85 折。⇒ **不要把 1.35 当近闸线**（会把 2Y 1.36–1.57 的件误判达标）；n=1 反例，其它区/其它通道未测，别外推成「平台没这条规则」，但也**别照文章承诺**。
  3. 结论：**文章的 ATOM 红利阈值只能当「待实测的候选主张」，交付口径一律以 `get_alpha_details` 的 checks 实读为准**；本仓 S≥1.58 全期闸不变。

### 2.2 [Power Pool + ATOM] 不吃纯 Power Pool 的每日 1 个配额

纯 Power Pool Alpha 每天最多 1 个、单个排行榜每月 10 个；**同时满足 Power Pool + ATOM（双标签）不占这个 1 个**，走常规每日 4 个额度。

### 2.3 天然契合 Genius 六维 Tie-Breaker

平台同时考核：
- **每条 Alpha 平均使用的不同字段数（Avg distinct Fields/Alpha）** —— 越低越好，单字段 ATOM 可压到 **1**
- **累计使用的不同字段总数（Total distinct Fields）** —— 越高越好。⚠ 2026-11-18 复核修正：原文"全季度"是误记，实测**跨季累加不重置**（平台 `dataFieldsUsed` 在 10-06 读 256，而当季理论上限仅 47）

⇒ **用单字段 ATOM 批量扫新字段**，在这两个维度同时拿满优势。这是"单字段扫描"策略的制度基础。

---

## 3. ★ 木桶倍率律（本文最重要的一条，直接影响跨集决策）

每日收入里的 **Dynamic Pyramid Multiplier**（Quality Factor 的核心组成）按金字塔拥挤度动态给：越冷门越高（1.3x / 1.5x / 1.8x），最拥挤的 `pv1` 常年垫底 **1.0x**。

**混用多个类别时，倍率按其中最低的那个结算（木桶短板效应）**：

| 写法 | 结算 |
|---|---|
| 纯 ATOM 用 1.8x 稀缺集（仅配豁免分组字段） | **1.8x 满额**，完整点亮对应金字塔 |
| 1.8x 稀缺集 **顺手混入 pv1 的 close/returns/cap** | 按 **1.0x** 结算，稀缺红利瞬间蒸发 |
| **≥3 个数据集** | 倍率拉最低，且 Genius 金字塔评定**直接计 0 个 Pyramid** |

⚠本仓校验：这条对现有跨集候选有直接后果——
`Xga1Ae00`（imbalance5 × PV，见 `GBR/wf_gbr_imb5_cross_20261117`）= `IMBALANCE×1.0 + PV×1.4`，
按木桶律**实际按 1.0x 结算**（不是 1.4x），即：它确实点亮 IMBALANCE 塔，但**拿不到 PV 的 1.4x 红利**；
而 GBR D1 的 `imbalance` 倍率本身只有 **1.0x**（全区最低档），所以这颗的倍率收益为 0。
历史批次里那些 7~9 个数据集的组合（`fund_holdings_panel+institutions6+news104+…`），按本条应计 **0 个 Pyramid**。

---

## 4. 隐形破 ATOM 的三个坑（最容易踩）

| 坑 | 为什么丢 ATOM | 保纯替代 |
|---|---|---|
| `inst_pnl()` / `convert()` | 底层自动调 pv1 的价格/汇率 | 不用；改 `ts_rank` / `ts_zscore` + `trade_when` 做过滤和平滑 |
| 用 `cap` / `close` / `returns` / `vwap` 做 `bucket()` 分组 | 这几个全是 **pv1** 字段 | 只用 6 个豁免分组字段，或用**本数据集自带**的规模/辅助字段造桶 |
| `vector_neut(x, cap)` / `vector_neut(x, returns)` | 直接引入 pv1 | 用同数据集内部市值字段（如 `model26` 的 `mdl26_market_cap_u`），或 Settings 选 Subindustry / Slow+Fast 中性化 |

⚠本仓已有同源清单：[[atom-pyramid-rules]]「隐形破 ATOM 清单」（`vector_neut(x,rank(cap))`、`bucket(rank(<非本集字段>))`、`returns/close/volume/vwap/cap/adv20`、`inst_pnl()/convert()`）——两处一致，互相印证。

---

## 5. 混数据的两个代价（不是风格问题，是钱）

1. **倍率木桶**（§3）：混 1.0x 就按 1.0x 结算；≥3 集直接 0 Python。
2. **IS 高、OS/VF 崩**：不同数据集的更新频率/覆盖度/滞后完全不同，硬拼 + 多层算子 = 样本内凑数。
   文章引用的论坛复盘（可直接 grep 本仓论坛缓存或 `read_forum_post`）：
   - Post `40018929254935`《我在 2025 IQC 期间到底做了什么，才导致既没挣到钱、赛后 VF 又暴跌》——IS 排名进前 40，OS 惨烈、VF 掉档；第一条忠告就是「尽量选单字段、能出 ATOM 的模板」。
   - 《VF 0.97 掉到 0.39 后的痛定思痛》——「VF 下跌不是从某条 alpha 的 Fitness 变低开始的，而是从**提交集合里 ATOM 变少**开始的」。

---

## 6. ★ 核心秘籍：按 onboard 时间找字段，而不是按 alphaCount==0

**为什么不能只挑 `alphaCount == 0`**：老数据集里如果某字段上线多年仍是 0，大概率已被全平台脚本犁过无数遍——它是 0 是因为**数据全是缺失值或没有预测信号（死字段）**。按它升序挑，跑一天全是 S≈0.2 的废票。

**真正的无人区**：先把 `dateCreated`（`/data-fields` 的 onboard 时间）**降序**，再按 `alphaCount` 升序，并加 `coverage ≥ 0.80` 过滤。刚 onboard 的字段有三个降维优势：

1. **prod 相关性极低**（先发优势，不用奇技淫巧就能过 0.70 闸）——直接对治本仓最痛的 prod-locked 问题
2. **Dynamic Pyramid 倍率极高**（新集常处冷门金字塔，1.3x ~ 1.8x）
3. 最简单的二阶/三阶单字段模板即可过检（叠加 ATOM 免 IS-Ladder）

文章给的 USA/TOP3000/D1 实测样例（`dateCreated` 2026-03/04、cov 0.87-0.93、ac 0-3、倍率 1.2-1.3x）：
`mdl109_vf_alt_1_am` / `mdl109_vf_alt_2_roe` / `mdl109_vf_prof_3_fcfroic` / `ern4_sue_ner` / `ern4_V_sue_eps`

⚠本仓校验（2026-11-17 实测，两个必须知道的边界）：
- **`max_fields` 与 `sort_by` 组合曾失效，2026-11-17 已修**：原实现把 `max_fields` 下传给平台 API 当 `limit`，
  即**先截断再排序**（实测 `model109 + sort_by=dateCreated + max_fields=8 + min_coverage=0.5` → `returned=0`）。
  修复后 dataset 级调用改为「全量拉 → 排序/过滤 → 再截断」，返回 `cap_applied_after_ordering=true`
  （已验证 `pages_fetched=11 / complete=true / returned=5`）；unscoped 仍平台侧截断并带 `ordering_warning`。
  回归 `world-quant-brain-mcp/tests/test_datafields_ordering.py`（12 例）。
- **unscoped 列表是跨区全量**：不带 `dataset_id` 时 `platform_count=10000`（全平台所有区域），
  不能当成"本区最新字段"用。**按区找蓝海要先枚举该区 dataset，再逐集排序**。
- **GBR 的 `dateCreated` 无区分度（2026-11-17 全量实测：177 数据集 / 341 候选）**：GBR/TOP700/D1 字段的
  `dateCreated` **全部是 `2026-07-01`**（整区目录一次性批量 onboard）⇒ 文章"按 onboard 排序"在 GBR 退化成
  「alphaCount 升序 + 倍率降序」。**该方法适用于 onboarding 分批的区（如 USA），GBR 只能用另两轴。**
- **覆盖率元数据大面积报 0（已知盲区，非无数据）**：GBR 很多集字段级 `coverage=0`（`analyst15` 533 字段全 0）。
  工具按「cov≤0 = 未知」保留（`--drop-unknown-coverage` 才严格剔除）；文章口径 `coverage≥0.80` 在 GBR 会整区过滤为空。
- **硬写 `data_type=MATRIX` 会把 VECTOR 集清空**：实测 `order_book_imbalance` / `news17` 在 MATRIX 过滤下显示 0 字段。
  工具已默认全类型 + 只剔除 SYMBOL。

---

## 7. 四套单字段 ATOM 模板（原文照录，可直接改 `{field}`）

```text
模板1 长短周期均值比（基本面/模型预期的近期边际变化）
group_rank(ts_mean({field}, 20) / ts_mean({field}, 120), subindustry)

模板2 时序标准化 + 行业内中性化排名
group_neutralize(ts_zscore({field}, 60), subindustry)

模板3 一年期时序分位均值回归（低换手；⚠ TO<30% 的 0.85x 折扣**本仓未复现**，近闸仍按 1.58）
ts_decay_linear(-ts_rank({field}, 252), 10)

模板4 时序差分除以自身波动率（纯单字段信噪比）
group_rank(ts_delta({field}, 20) / ts_std_dev({field}, 60), sector)
```

建议设置（原文）：`delay=1`、`decay=6`、`neutralization=SUBINDUSTRY`、`truncation=0.08`、
`pasteurization=ON`、`unit_handling=VERIFY`、`nan_handling=ON`。

⚠本仓校验：模板 1/4 用除法，**分母为稀疏事件字段时会产生跳变**（本仓实证：sentiment33 稀疏事件套平滑族 ⇒ 8/8 臂 TO 0.57、DD 0.95）。
⇒ 模板只适用 **dense（日更稠密）** 字段；sparse 事件字段必须先 `ts_backfill(≥250)` 再聚合（见 [[gbr-unlit-tower-exhausted]] 的密度判别）。

---

## 8. 与项目现行规则的对应 / 冲突（用前必读）

| 项目现行规则 | 本文主张 | 怎么处理 |
|---|---|---|
| [[redline-pv-model-other-single-dataset]]：PV/MODEL/OTHER/FUNDAMENTAL 四类之间禁组腿，跨界组合全账号 ≤5 | 混任何一集都触发木桶降倍率，≥3 集计 0 塔 | **方向一致且更严**。本仓的「跨界 ≤5」是硬约束，本文补上"即使合规也不划算"的量化依据 |
| [[atom-pyramid-rules]]：ATOM 免 IS-Ladder、只查 2Y | 同（阈值 1.59 / ×0.85） | **部分被实测推翻**：1.59 → 实读 1.58；×0.85 折扣被 `gJaR5gov`（TO 5.39% / limit 仍 1.58）直接反例 ⇒ 见 §2.1 |
| **§7.7 ATOM 优先与 regular 回退（2026-11-17 顶层规范）**：ATOM 穷尽后才允许 regular 跨集（gating/grouping/residual/ratio 四形态 + `atomExhaustedEvidence` 举证） | 混集降倍率、伤 VF | **互为表里**：文章给"为什么不划算"（钱），§7.7 给"什么时候才允许"（纪律）。regular 回退是"能交付"的路，不是"同样划算"的路；回退前先算倍率损失（取 min）与塔位占用 |
| 本仓主张 S≥1.58 全期闸 | ATOM 只看 Last-2Y ≥1.59 | 两套口径并存：**平台放行**看 2Y 通道（实读 limit），**本仓交付**仍按 S≥1.58（更严，保持不变） |
| [[redline-no-invest-in-lit-towers]]：已点亮塔不再投入 | 未涉及 | **新增约束**：ATOM 的倍率红利只在新塔上兑现；挑数据集时先按塔位实读过滤，已亮塔名下的新字段即使 ac=0 也不投入 |

---

## 9. 可执行行动清单（本仓版）

1. **找字段先按 onboard 排**：`get_datafields(dataset_id=…)` **省略 max_fields**，配 `sort_by="dateCreated"`、`min_coverage=0.8`；数据集级扫完再跨集比较，不要用 unscoped 列表当本区全集。
2. **先用 4 模板做首轮筛**（dense 字段），再进机制研究；sparse 字段先 backfill。
3. **ATOM 优先不解释**：任何"顺手乘个 volume / 除个 close"都会触发木桶降倍率——想用 PV 就单独开一颗 ATOM/PV 单集件，别混。
4. **prod 前置闸依旧**：新字段虽然是先发优势，仍要实测（本仓已有 S1.66 / prod 0.94 的教训）。
5. **提交前本地自相关筛查**（同批新字段容易彼此高相关），本仓 `compute_mutual_correlation` 已是本地零配额。

---

## 10. 脚本与工具入口（原文四入口，本仓对照）

| 原文入口 | 内容 | 本仓对应 |
|---|---|---|
| **ACE (Alpha Creation Engine)** 官方库：`ace_lib.py` + `helpful_functions.py` + `how_to_use.ipynb`（Help Center Article 20786107171351，zip 附件 38760475882263） | 官方 API 封装，ipynb 第 2 节即单数据集遍历生成 ATOM 的现成脚本 | 本仓已有 vendored `ace_lib.py`（GEM 内嵌），⚠ `ace.start_session()` 会把口令明文写 `~/secrets/platform-brain.json`，调用前必须覆盖（`test_sf_docs` 守） |
| 社区批量脚本：《网页回测很卡，摆脱网页手搓》(Post 39785152862999)、AI 工作流 (Post 39925324948119) | 批量回测 + 遍历中性化 + AI 批量扫描 | 本仓 workflow v2 / `submit_batch` 已覆盖同类能力，不必照搬 |
| `machine_lib.py` + 本地零误差自相关：《IQC 晋升顾问》(Post 40196228270103) | 批量跑出高分 ATOM 后卡 Self-Corr 的解法 | 本仓 `check_self_correlation`（self+powerpool 双口径）+ `compute_mutual_correlation` 已是本地零配额实现，且口径更全 |
| 官方指南：`[UK Consultants] A BRAIN platform guide for LLM research agents` (Post 42665863146007)、`Pyramids in practice: pick the dataset before the idea` (Post 43712961725335) | LLM 研究代理指南 / 「先选数据集再想 idea」 | 后者与本仓「查表选区选集」（wq-brain-campaign-matrix）同构，可作为佐证引用 |

## 11. 工具（2026-11-17 已落地）

- ✅ `tools_data.get_datafields` 的「先截断后排序」已修（见 §6），回归 12 例全绿。
- ✅ 新 CLI `tools/fields/atom_fresh_fields.py`（已登记 `tools/README.md`）：
  `python tools/fields/atom_fresh_fields.py --region GBR --universe TOP700 --delay 1 --top 30`
  —— 枚举数据集 → 逐集实拉 → `dateCreated` 降序 + `alphaCount` 升序 + 覆盖率过滤 → 汇总（带倍率/类型/ac）；
  缓存 `cache/_scratch/atom_fresh_<R>_<U>_d<D>.json`（TTL 24h，`--refresh` 强制重拉）。
  区域适配参数：`--min-coverage`（缺省 0.5）、`--data-type`（缺省全类型）、`--exclude-types`（缺省 SYMBOL）、
  `--category`、`--max-datasets`（快速试跑）、`--json`。
