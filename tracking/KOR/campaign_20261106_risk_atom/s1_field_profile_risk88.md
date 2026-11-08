# S1 · risk88 全字段画像（64/64，KOR / TOP600 / Delay=1）

> 采集：MCP `get_datafields(dataset_id="risk88", region="KOR", universe="TOP600", delay=1, **filter_sharpe=false**)`
> → `count=64 / platform_count=64 / complete=true`
> 元数据：coverage **0.9727** · userCount 495 · alphaCount **1418** · valueScore 2.0 · 塔乘数 **1.3**
> 来源模型：**Axioma MFM / ASE1（ASI 区口径）** —— 与 risk70 的 **MFM2 / ASETRD 是两个独立 vendor 模型**
> ⇒ 本集的核心价值不是「重复一遍 risk70」，而是 **独立模型口径**（同一经济量的第二次测量）。

---

## 0. 名 vs description 差异表

| 族 | 名形态 | description 实义 | 按名字分类会犯的错 |
|---|---|---|---|
| 风格载荷 9 支 | `rsk88_mfm_ase1_ri_<style>` | 「… style factor loading in ASI region」 | `ri_` 前缀无文档，且与 risk70 的 `rsk70_mfm2_asetrd_<style>` **不是同一套因子定义**（Barra 经典 9 因子 vs Axioma 27 因子）⇒ **不能同名互换，也不能直接相减当作测量误差**（须先实测相关性） |
| 行业载荷 50 支 | `rsk88_mfm_ase1_ind_<industry>` | 「… industry factor loading in ASI region」 | 哑变量型，**只可作分组轴**；50 个行业比 risk70 的 20 个更细 |
| 特异量 2 支 | `rsk88_mfm_ase1_dsrt` / `_srisk` | 「Instrument specific returns / specific risk in ASI region」 | `dsrt` 与 risk71/72 **同量同名**；`srisk` 与 risk70 `srisk` **同义不同模型** ⇒ 视为**同一机制的第二档测量**，不构成独立腿 |
| 辅件 3 支 | `alternative_market_cap_usd` / `rsk88_mfm_ase1_market` | 市值 / 市场成员载荷 | 规模壳 / 哑变量 |

⚠ **本集全部字段的 description 都带 "in ASI region" 后缀，但 KOR 实测 coverage 0.967–1.0**
⇒ 与 risk68 的「European」标注同类问题（vendor 统一管线）。**以 coverage 为准，描述里的区域口径不可用于判断样本域。**

---

## 1. 全字段表（64/64）

### 1.1 风格载荷 `ri_*`（9）—— ✅ 主战场

| # | field | cov | aC | U | 形态 | 可用性 |
|---|---|---:|---:|---:|---|---|
| 1 | `rsk88_mfm_ase1_ri_value` | **1.0** | **247** | **121** | 零中心近正态 | ✅ **头部轴** |
| 2 | `rsk88_mfm_ase1_ri_volatility` | 1.0 | 98 | 67 | 零中心近正态 | ⚠ 与 risk70 `resvol` 同族（IVOL 已判死）；仅作正交化控制量 |
| 3 | `rsk88_mfm_ase1_ri_growth` | 1.0 | 85 | 54 | 零中心近正态 | ✅ 备选 |
| 4 | `rsk88_mfm_ase1_ri_divyield` | 1.0 | 73 | 53 | 零中心近正态 | ✅ 备选 |
| 5 | `rsk88_mfm_ase1_ri_momentum` | 1.0 | 53 | 35 | 零中心近正态 | ✅ 备选 |
| 6 | `rsk88_mfm_ase1_ri_size` | 1.0 | 52 | 31 | 零中心近正态 | 🅢 规模壳 |
| 7 | `rsk88_mfm_ase1_ri_beta` | 1.0 | 39 | 26 | 零中心近正态 | ⛔ beta 已实测无效 |
| 8 | `rsk88_mfm_ase1_ri_nonlsize` | 1.0 | 34 | 26 | 零中心近正态 | ✅ 备选（非线性规模，与 size 正交） |
| 9 | `rsk88_mfm_ase1_ri_leverage` | 1.0 | 30 | 22 | 零中心近正态 | ✅ 备选 |

### 1.2 行业载荷 `ind_*`（50）—— ▦ 仅分组轴

`advertising`(31) · `aerospace_defense`(24) · `agriculture`(70) · `airlines`(41) · `apparel`(37) ·
`automanufacturers`(13) · `banks`(28) · `beverages`(13) · `biotechnology`(12) · `buildingmaterials`(17) ·
`chemicals`(15) · `commercialservices`(9) · `computers`(22) · `cosmetics_personalcare`(9) ·
`distribution_wholesale`(6) · `diversifiedfinanserv`(9) · `electric`(19) · `electronics`(15) ·
`energy_alternatesources`(4) · `entertainment`(16) · `environmentalcontrol`(5) · `food`(9) · `gas`(15) ·
`hand_machinetools`(10) · `healthcare_products`(11) · `healthcare_services`(4) · `homebuilders`(15) ·
`homefurnishings`(12) · `householdproducts_wares`(3) · `insurance`(3) · `internet`(8) ·
`investmentcompanies`(3) · `iron_steel`(8) · `leisuretime`(7) · `lodging`(14) ·
`machinery_diversified`(13) · `media`(7) · `metalfabricate_hardware`(12) · `mining`(12) ·
`miscellaneousmanufactur`(37) · `officefurnishings`(12) · `pharmaceuticals`(7) · `privateequity`(4) ·
`realestate`(13) · `retail`(11) · `semiconductors`(12) · `shipbuilding`(9) · `software`(10) ·
`telecommunications`(15) · `textiles`(5) · `transportation`(16)
（全部 MATRIX / cov .967 / 哑变量型）

### 1.3 特异量（2）+ 辅件（3）

| # | field | cov | aC | 裁定 |
|---|---|---:|---:|---|
| 1 | `rsk88_mfm_ase1_dsrt` | .967 | 297 | ⛔ `KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD`（同一量） |
| 2 | `rsk88_mfm_ase1_srisk` | .967 | 102 | ⚠ 未测；与 risk70 `srisk` 同机制但**独立模型** ⇒ 只作**第二档测量对照**，不当新腿 |
| 3 | `rsk88_mfm_ase1_market` | 1.0 | 12 | ⛔ 市场成员哑变量 |
| 4 | `alternative_market_cap_usd` | 1.0 | 44 | 🅢 规模壳（属本数据集 ⇒ `vector_neut` 不破坏 ATOM） |

---

## 2. 五问（A-1）

| # | 问 | 答 | 决策 |
|---|---|---|---|
| 1 | 时间维度 | 全为**存量水平**（载荷逐日重估）；`dsrt` 为流量 | 载荷禁裸水平，先秩化 |
| 2 | 相对性 | 排序差异 | `group_rank` |
| 3 | 被定价的是谁 | 强度（因子敏感度） | 排序；变化率另立轴 |
| 4 | 有无博弈 | `ri_value` 121 users / 247 αC（中高拥挤） | 首颗即查 prod |
| 5 | 事件性 | 否（cov 1.0 连续） | 禁 `trade_when` 门控 |

## 3. 预处理决策

| 体征 | 决策 |
|---|---|
| `ri_*` 全部 cov **1.0**（比 risk70 的 .967 更完整） | `ts_backfill(F,22)` 仍保留（防止早期年缺值）；**十年覆盖预期更好** |
| 载荷厚尾（论坛实证） | `winsorize` 或 `ts_zscore` 前置 |
| 9 支载荷同族（value/growth/divyield 同属价值维度；size/nonlsize 同属规模维度） | **一条腿只出 1 颗**；`value − growth` 是「价值纯度」差分（同源单一含义，合规） |
| 50 个行业载荷 | 只可作分组轴，且与 risk70 的 20 个行业分类**不同源**（不可混用分组） |

---

## 4. 机制（A-2）

### M5 · 价值维度纯度（`ri_value` − `ri_growth`）

| 声明项 | 内容 |
|---|---|
| **谁在被定价** | 按 Barra 风格标签配置的资金 |
| **为什么会被错** | 「价值」与「成长」在 Barra 模型里是**两个独立载荷**；同时高价值 + 高成长 = 「合理价格成长（GARP）」⇒ 最优；高价值 + 低成长 = 价值陷阱 |
| **错了多久修复** | 1–2 季 |
| **预期方向** | `value − growth` 越高（越纯价值、越少成长）⇒ 若价值陷阱假说成立则**跑输**；反向则跑赢 ⇒ **正反各测** |

### M6 · 跨模型载荷分歧（risk70 `btop` vs risk88 `ri_value`）

| 声明项 | 内容 |
|---|---|
| **谁在被定价** | 依赖单一风险模型的量化资金 |
| **为什么会被错** | 两个 vendor 对「价值」的测量不同（账面/现金流/股息口径混用）；**分歧大 = 估值口径不确定**，市场对不确定的股票要求折价 |
| **错了多久修复** | 1 季 |
| **预期方向** | 分歧越大 ⇒ 后续跑输（折价假说）⇒ 需反测 |
| **可行性** | ⚠ **跨数据集（risk70 × risk88）⇒ 非 ATOM**（`classify_atom` 会判 combined）。本轮**只登记不投**，除非主攻线全灭且用户接受 combined |

---

## 5. 双通道取证

| 通道 | 状态 | 内容 |
|---|---|---|
| **A 论坛** | ✅ 已查 | post `43621466539671`（30 赞）：risk70 的 5 组组合方向可直接迁移（载荷单点无信号、组合才有）；post `36064174250519`（20 赞）：**SLOW 风格中性化下 RISK 数据集出货率很高**、prod 相关性普遍 <0.6 ⇒ **中性化档是本塔的关键杠杆** |
| **B 文献** | ✅ 已有 | Barra/Axioma 风格载荷的价值/成长/规模维度有成熟文献（Fama-French 三因子→五因子；Asness-QMJ）。⚠ 均为美股样本，KOR 小宇宙须实测 |

**裁决**：A、B 指向同一机制（风格载荷 = 系统性暴露，须组合 + 风格中性化后才有残余 alpha）。
⇒ 本轮沿用 risk70 的结论（`anlystsn` 水平胜出），risk88 作为**独立模型复现**：若 `ri_value` / `ri_growth` 在
同模板下也给出 S > 1.0，则「载荷轴在 KOR 可交易」得到**跨模型验证**；否则说明 risk70 的 `anlystsn` 是**单字段特例**。

---

## 6. 实测记录

（待 wave R3 派发；本集历史上只有 `ri_*` 裸横截面的 dead_end `KOR-RSK88-STYLOAD-WEAK`，无分波读数。）
