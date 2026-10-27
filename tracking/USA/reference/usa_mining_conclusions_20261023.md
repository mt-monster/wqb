# USA 战役结论层（2026-10-23 全量复盘归档）

> **定位**：区域层结论（USA 专属读数与判据）。跨区通用规律在 [`docs/experience/03_region_dataset.md`](../../../docs/experience/03_region_dataset.md) §9，
> 本文只保留「下次开 USA 波次必须先知道」的部分。
> **上位来源**：[`reports/usa_mining_history_review_20261023.md`](../../../reports/usa_mining_history_review_20261023.md)
> （1698 回测行 / 110 波；附录 A 为只读复现命令）。
> **配套机读件**：[`usa_dead_datasets.md`](usa_dead_datasets.md)（47 集判死清单，S0 自动剔除）、
> [`usa_dataset_mechanisms.md`](usa_dataset_mechanisms.md)（机制排序键）。
> **过期口径**：本文读数 `as_of = 2026-10-23`；用户已裁定「以前的画像与数据证据不能作证」，
> 复用前先看 `as_of`，超 120 天的按过期处理（与死集清单同口径）。

---

## 1. 一页结论

> **USA 的瓶颈从头到尾只有一个：prod。IS 侧的 10 倍努力换不来 1 颗可提交 alpha。**

| 指标 | 值 |
|---|---|
| 回测行 / 波次 | 1698 / 110（FAIL 58 · PARTIAL 43 · PASS 9） |
| RA 硬闸全过 | **177（11.6%）**（`payload_json.failed_checks ∩ RA_CHECK_NAMES` 口径） |
| 走到 prod 实测 | 26（14.7%） |
| **prod<0.7 且 self<0.7** | **4 颗 ⇒ 转化 15.4%** |
| prod 分布（n=92） | `≥0.8` **44.6%** · `[0.7,0.8)` 12.0% · `<0.7` 43.5%（`<0.5` 仅 1 颗） |
| 严格口径交付 | **5 / 10**（另 5 颗属已点亮的 MODEL 塔，2026-10-23 作废） |

**三条判据（按优先级）**

- **A｜选集不看「RA 全过率」**：它衡量信号强度，交付卡口是「机制在生产池里拥不拥挤」，两者在 USA **反向**。
  RA 全过率最高的三个集：`web_traffic_engage` 80%（prod 0.9908）、`other143` 59.6%（0.9206）、
  `institutions18` 30.4%（0.9636）⇒ **全部撞墙**。选集问「机制是否经典异象」，不问「数据集是否冷门」。
- **B｜max S < 1.58 的集直接出局**：`pv106` 0.00、`shortinterest29` 0.79、`other596` 0.91、
  `multi_horizon_alpha` 1.16、`fundamental14` 0.84、`chart_return_model` 1.46。
  ⇒ 开波前 1 条裸探针（`|S|<0.5` kill，0.5–1.0 需改机制）。
- **C｜prod 探针前移到第 1 波**：每族 1 颗探针的 prod 额度（不占回测槽），`prod ≥0.75` 即封族。
  历史代价：`other143` 用 8 波、`risk60` 用 3 波才测出撞墙 ⇒ **13/110 波（11.8%）白投**。

---

## 2. 闸频次（行级 n=1525）与读法

| 闸 | 失败行占比 |
|---|---:|
| `LOW_FITNESS` | 84.2% |
| `LOW_SHARPE` | 82.4% |
| `LOW_2Y_SHARPE` | 76.5% |
| `LOW_SUB_UNIVERSE_SHARPE` | 42.1%（**比值闸**，USA 系数 ≈0.433） |
| `CONCENTRATED_WEIGHT` | 14.6%（唯一的数据品质型） |
| `HIGH_TURNOVER` | 4.8% |
| `LOW_TURNOVER` | 3.5% |
| `IS_LADDER_SHARPE` | 1.3%（分组轴是最大杠杆） |

- 前 3 项高度共现 ⇒ **一次修好一个闸没有意义，必须换机制或换字段族**。
- **SUB 靠「加 S」修是错路**：抬 S 会同步抬它的要求（见 `docs/experience/01_platform_gates.md` §2）。
- **换手只占 4.8%**，复盘里却被过度关注（27% 的波次提到）；仍按 **[0.03, 0.70]** 标注，
  越界行不进 prod/self 队列（2026-10-24 起收批自动标注）。

---

## 3. 数据集层（USA 专属）

**判死清单不在此重复**：见 [`usa_dead_datasets.md`](usa_dead_datasets.md)（47 集，`verdict` ∈
`dead_end` / `prod_sealed` / `signal_short` / `structural`，120 天过期）。

仍在途 / 有余量的集：

| 数据集 | 状态 | 说明 |
|---|---|---|
| `insider_matrix` | 有余量 | 冠军 `zqrGqVXo` S 9.25 / prod 0.8092；族内 3/4 颗 prod<0.7；`d5KzLo7v`（market，prod 0.6964 / self 0.2438）已在 READY，**待用户确认** |
| `insider_agg_matrix` | virgin | USA 零回测；17 字段全是「金额量级」+ 唯一方向量 `directional_indicator_2`；**开波前必做 prod 探针** |
| `earnings_sent_matrix` / `fundamental110` / `fund_holdings_panel` | 未验证 | earnings 塔差 2 颗即点亮（×1.2）；`institutions18` prod 0.9636 ⇒ **换族不换机制** |
| `techindi_model` | 在途 | RA 全过 10/49；prod 0.7947；tm_w3 仍在跑 |

**塔层**：当季 platform 塔位 = analyst LIT(6)、model LIT(4)、earnings 1、其余 13 类 0。
**已点亮塔的集不做主挖掘目标**（2026-10-23 用户裁定）；`ai_equity_alpha` 虽可交付但属 MODEL 塔，只作 SA 组件。
⚠ 判塔位看**平台类别**，不看 DB 行的 `pyramid_multiplier`（`insider_agg_matrix` 的 DB 值 1.5 是 D0，USA/D1 insiders 真值 1.1）。

---

## 4. 机制层：USA 已验证 / 已证伪

**已验证有效**（有 RA 级读数支撑）

| 机制 | 证据 | 关键条件 |
|---|---|---|
| 平行模型对同一目标的分歧 | `ai_equity_alpha` 5 颗 S 2.19–2.67 / prod 0.64–0.69 | 两条腿都是「对收益的预测」（MODEL 塔已点亮） |
| 分析师修正的量级 / 偏度结构 | 前 5 颗交付 S 1.61–2.05 | 单数据集、单概念、非加权混腿 |
| decay 5→8 的换手杠杆 | `fhp` 波 3：TO 0.7628→0.6221，S 仅 −8%，F/2Y/SUB 不动 | 只在**已过强度线**的族上用 |
| universe / 中性化轴重排 | `usa_cma_w3`：MARKET 优于 SUBINDUSTRY | 逐档实测，**非单调**；分组轴是 USA 最有效的 prod 杠杆 |

**已证伪**（详见 `docs/experience/05_antipatterns.md` §7 与死集清单）
同模型多配置分歧（`chart_return_model`）· 跨供应商文本分类器分歧（`other635`）·
新闻语气 / 极性方向（`news_transformer_scores`）· D1 上 1-bar 期限的预测字段 ·
fundamental 域全线（`fundamental1/2/14/21/22/25/35/69/72/91/93/110` + `other416/452`）·
「冷门 + 经典异象」= 低相关（`risk60` 0.9917、`pv106` 空列）。

---

## 5. 复盘质量（已固化的改造）

110 波复盘的注意力错配：prod 只 15% 提到（客观 56.5% 淘汰主因）、2Y 29%（客观 76.5%）、
换手 27%（客观 4.8%）、分组轴 8%（唯一有效的 IS_LADDER 杠杆）。

**2026-10-24 已落地**：`wave_results.key_findings` 固定四列
（① 强度上限 max|S| 及其来源 + 正负向极值 + 2Y ／ ② 机制方向与证伪条件 ／ ③ prod 读数，未测显式标注 ／
④ 闸缺口按 `(门槛−实测)/|门槛|` 排序）+ TO 越界标注。
`review_wave.py` 与 `pipeline.py` 首屏都打印这四列；`--mechanism/--falsifier` 可显式登记 ②。

---

## 6. 下一步（按当前状态）

1. **`d5KzLo7v`**：RA 全过、prod 0.6964 / self 0.2438，已在提交队列 READY ⇒ **只差用户确认**（零新增回测）。
2. **`insider_agg_matrix`**：INSIDERS 塔未点亮（×1.1）、USA 零回测 ⇒ 先 1 颗 prod 探针，再开十臂波。
3. **earnings 塔**（`earnings_sent_matrix` 等）：差 2 颗点亮，塔收益最大（×1.2）。
4. `other`（×1.4）/ `sentiment`（×1.4）/ `option`（×1.3）：需避开已撞墙的 `other143` / `other635` 机制。
