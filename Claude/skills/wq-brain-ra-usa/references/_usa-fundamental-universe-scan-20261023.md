# USA / D1 / TOP3000 — Fundamental 全集扫描（2026-10-23）

> 目标第 1 步「全部 Fundamental 数据集逐一扫描」的交付件。
> 取数：`mcp__wq-brain-http__get_datasets(region=USA, delay=1, universe=TOP3000, category=fundamental)`
> 返回 **23 个**数据集（`count=23`，单页全量）。拥挤度一律用**数据集级** `alphaCount`（附录 H 的教训：字段级 aC 会系统性低估）。

## 1. 全量表（按 aC 升序）

| 数据集 | 名称 | 覆盖 | 字段 | 用户 | **aC** | value | 裁决 |
|---|---|---:|---:|---:|---:|---:|---|
| fundamental67 | Predictive Sales | 0.500 | 12 | 30 | **52** | 4 | ✗ 描述明写 accruals-based 预测模型 —— 与 fnd93 同一构造（已证无信号） |
| fundamental35 | US Financial Institutions | 1.000 | 1 | 33 | **71** | 3 | ✗ 只有 1 字段，不构成 ATOM；且仅覆盖金融机构（TOP3000 内有效覆盖远低于 1.0） |
| fundamental25 | Company Operating Metrics | 0.382 | 8 | 52 | **72** | 3 | ✗ 覆盖 0.382，与 other596 稀疏覆盖墙同形；8 字段不足以组 ATOM |
| fundamental22 | Environmental and Social Governance | 0.723 | 14 | 45 | **81** | 4 | ✗ 实际内容是 RIC↔Bloomberg ID 映射（描述与名称不符），非信号 |
| fundamental93 | Earnings Tax Data | 0.631 | 46 | 44 | **85** | 4 | ✗ **本波判死** `USA-FND93-TAX-WEAK`（见附录 AP §E） |
| fundamental21 | ESG Scores | 0.429 | 142 | 61 | **154** | 4 | △ 低拥挤 + 字段足，但覆盖 0.429 且为慢变量评分；ESG 水平项在文献中无稳健溢价，留作后备 |
| other452 | Earnings Tax Data | 0.530 | 46 | 52 | **165** | 4 | ✗ 与 fundamental93 **同主题同字段数**（46）—— 税机制判死可直接外推，不重复烧配额 |
| fundamental69 | Quarterly Fundamental Data | 0.611 | 12 | 137 | **231** | 2 | ✗ 已判死 `USA-FND69-WEAK` |
| fundamental1 | Management and Executive Data | 0.412 | 205 | 163 | **359** | 4 | △ 高管履历，字段足但属事件/分类型，覆盖 0.412；留后备 |
| fundamental91 | Quantitative Filings Data | 0.605 | 407 | 189 | **475** | 4 | ✗ 已登记判死（fnd91） |
| fundamental110 | Press Release Data | **0.821** | 26 | 365 | **773** | 1 | ✗ 实测 7 个可用字段**全是 VECTOR 事件元数据**（日历/期间/XBRL 标签/修订号），值列跨指标混在同一向量里不可辨识，做不了 ATOM |
| other416 | Quantitative Filings Data | 0.560 | 371 | 225 | **1711** | 4 | ✓ **选中**（见 §3 与字段画像） |
| fundamental72 | Comprehensive Fundamental Data | 0.746 | 1852 | 805 | 3082 | 2 | ✗ 描述实为 RIC↔BBG 映射；且 aC 3082 |
| other466 | Aggregated Fundamental Data | 0.827 | 565 | 566 | 3781 | 2 | ✗ aC 3781，且是多家 vendor 聚合（构造与已死的比率族高度重叠） |
| fundamental14 | Audit Analytics Directors | 0.886 | 248 | 1478 | 7574 | 2 | ✗ 饱和 |
| fundamental13 | Comprehensive Fundamentals | 0.758 | 87 | 1578 | 15273 | 1 | ✗ 饱和 |
| fundamental3 | Fundamentals for US Equities | 0.643 | 788 | 1276 | 16603 | 1 | ✗ 饱和 |
| fundamental7 | Comprehensive Fundamentals | 0.742 | 311 | 2096 | 20980 | 1 | ✗ 饱和 |
| fundamental23 | Fundamental Point in Time | 0.771 | 1637 | 1824 | 28238 | 1 | ✗ 饱和 |
| fundamental17 | Direct Fundamental | 0.835 | 402 | 2473 | 34771 | 1 | ✗ 饱和 |
| fundamental28 | Global Fundamental | 0.500 | 2209 | 1929 | 38879 | 1 | ✗ 饱和 |
| fundamental2 | Report Footnotes | 0.439 | 766 | 37408 | **141883** | 1 | ✗ 饱和（全 fundamental 第二高） |
| fundamental6 | Company Fundamental for Equity | 0.500 | 886 | **89702** | **860417** | 1 | ✗ 饱和（全 fundamental 最高）；且本 book 的 `WjLekJQO` 已被其规模/资本开支腿吸收（self 0.7718） |

**分布事实**：aC 跨 **4 个数量级**（52 → 860,417）。可挖窗口只剩 aC < 500 的 11 个，而其中 4 个已判死、3 个是映射表或元数据、2 个覆盖 < 0.42。

## 2. 覆盖率与拥挤度不相关

`fundamental2` 覆盖 0.439 却 aC 141,883；`fundamental93` 覆盖 0.631 而 aC 85。**覆盖率不是拥挤度的代理**，两者必须分别取数。前者决定 SUB_UNIVERSE 风险，后者决定残余 alpha。

## 3. 为什么选 other416

筛选交集 = 未判死 × aC < 2,000 × 覆盖 ≥ 0.55 × 字段足以组 ATOM × 机制与已交付 5 条正交：

1. **aC 1711**：是 `fundamental2` 的 1.2%、`fundamental6` 的 0.2%；在「未判死」组里只高于 `fundamental21/1/25/35/22`，而后四者的覆盖或字段结构都不合格。
2. **371 字段**，且实测是**逐段 NLP 特征**（14 个 CAT 段 × 语言计数/相似度/情绪 + 文档级可读性/复杂度），不是财务比率快照 —— 与已交付的 5 条分析师修正 alpha、与已判死的 fnd93 税构造**零共享字段、零共享机制**。
3. **有具体学术锚**：Cohen–Malloy–Nguyen《Lazy Prices》(JF 2020) —— 10-K/10-Q 文本**变动**预测未来收益。这是唯一一个能由本数据集字段直接机械表达的论文级构造（`cat*_metric0_*` = 对比上季，`metric1_*` = 对比去年同季）。
4. **覆盖 0.560 不在稀疏区**（other596 的墙出现在字段级有效覆盖远低于数据集级）。

**为什么不是 fundamental21（ESG，aC 154 更低）**：覆盖 0.429，且 ESG 是慢变量评分，水平项在 2014–2023 美股大盘无稳健溢价；本 book 已有一次「低拥挤但无信号」的教训（fnd93），不再用最低 aC 当唯一理由。

## 4. 三条可复用结论

1. **同主题双份数据集**：`other452`/`fundamental93` 都叫 Earnings Tax Data 且同为 46 字段，`other416`/`fundamental91` 都叫 Quantitative Filings Data。判死一个不能自动外推另一个 —— 但**字段数与语义同构时可外推**（other452 与 fnd93 是 vendor 镜像，按同机制处理）。
2. **name ≠ content**：`fundamental22`（"ESG"）与 `fundamental72`（"Comprehensive Fundamental"）的描述都是 RIC↔BBG 映射表。选数据集必须读 `description` 与实测字段，不能只看名字与 valueScore。
3. **低 aC 的正确读法**：aC 低只证明「这个数据集没人用」，不证明「这个构造不拥挤」。拥挤度按**机制**计（如 accruals 是跨数据集共享的论文级构造，fnd93 aC 85 仍然挖不出东西）。
