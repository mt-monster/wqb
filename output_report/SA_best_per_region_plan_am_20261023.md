# 各 Region 最优 SuperAlpha 方案（2026-10-23）

> **执行摘要 · 一句话**：8 个可建区（USA/IND/KOR/GBR/MEA/GLB/DEU/EUR）今日 SA 配额全空，推荐**优先投 EUR+USA**（宽 universe、池深、无自相关干扰）；USA TOP500 已撞墙证伪（S=1.42–1.54 双闸全红）；KOR/GBR/IND/DEU/MEA 已成型，仅补「不同中性化族」小增量即可；**所有方案仅构建、不提交**，提交权归用户。

---

## 0. 论坛标准（2026-10-22 调研定稿，来源标注）

> 来源：《【新人入门】Super Alpha 从入门到入门！》78 赞/39 评论 ·《2024 super alpha 比赛心得》22 赞/15 评论 ·《Super Alpha 参数设置》12 赞（含 LY43440 实测回复）。本工作区实测佐证见 `.workbuddy/memory/2026-10-22.md`。

### 0.1 组成数量（Selection Limit）

- **平台硬下限 = 10**（<10 直接 400：`Ensure this value is greater than or equal to 10`）
- 论坛 78 赞帖建议 **30–100 起测、≤500**；LY43440 实测 IND 取 300（long/short 各 ~250）
- **实际生效数 = min(limit, 组件池)**；**组件池是 region 级**（非 universe 级）⇒ SA 指标天花板由该 region 的 ACTIVE REGULAR 数决定
  - USA 44 / IND 38 / MEA 19 / KOR 28 / GBR 18 / EUR 14 / GLB 11 / DEU 10

### 0.2 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.6** |
| C 比赛/优秀档 | **5.6–7.0** | **5.6–8.9**（冲 >10） | 0.20–0.27 | <0.5 |

### 0.3 组件筛选阈值

- `turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）
- `author_returns_to_drawdown>2`（官方建议 1–4）
- ⚠ **筛选强度必须匹配池子规模**：加严约束后组件 <10 ⇒ `sim ERROR: At least 10 component alphas are required`
- 小池区（EUR 14/GLB 11/DEU 10）**只能用宽松 selection** `(1 - self_correlation)`；论坛严格阈值仅适用于 IND/USA 等大池区

### 0.4 中性化族规律

- **Fitness 排序**（IND 实测）：**CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3**
- **选族规则**：**TO<0.10 → SLOW；TO>0.20 → FAST**
- **区域族基线**：GLB/USA/DEU/EUR 走 STATISTICAL + decay 1；KOR/IND/GBR 走 SECTOR/SUBINDUSTRY + decay 15（须逐区扫描验证，不可跨区照搬）
- ⚠ **组件数↑ ⇒ self↓ 但 prod↑**（EUR 实测 l10: self0.33/prod0.56 → l12: self0.29/prod0.61 → l30: self0.28）⇒ **l10 双闸综合最优、prod 余量最大**，不要盲目加大 limit

### 0.5 其他实证

- truncation 0.02 vs 0.08 对 SA 几乎无差异（S 3.74 vs 3.73）
- 论坛推荐 `Selection Handling = Non-Zero`；本工作区历史 35 颗 SA 全用 POSITIVE 均成功

---

## 1. 数据基线

### 1.1 组件池 eligibility（ACTIVE 已提交 REGULAR；IS 阶段 UNSUBMITTED 不计入）

| 区域 | ACTIVE 已提交 | UNSUBMITTED IS | 总计 | verdict |
|---|---:|---:|---:|---|
| USA | **44** | 277 | 422 | **GO** |
| IND | **38** | 127 | 169 | **GO** |
| KOR | **28** | 0 | 30 | **GO** |
| MEA | **19** | 0 | 19 | **GO** |
| GBR | **18** | 0 | 18 | **GO** |
| EUR | **14** | 546 | 566 | **GO** |
| GLB | **11** | 0 | 11 | **GO** |
| DEU | **10** | 0 | 10 | **GO**（压线）|
| ASI | 9 | 0 | 9 | ⛔ **BLOCKED（差 1 颗）** |
| HKG | 6 | 0 | 6 | ⛔ **BLOCKED（差 4 颗）** |

**GO 区域（可建 SA）：USA, IND, KOR, GBR, MEA, GLB, DEU, EUR**
**BLOCKED（需先提交攒着的 RA 补到 10）：ASI, HKG**

### 1.2 已提交 SUPER alpha 档位占用（34 颗 ACTIVE，+ 1 颗 vROOONwd 新入未写入探针缓存）

按 region 汇总（数据源：`get_user_alphas(stage=OS,type=SUPER,limit=200)` @ 2026-10-23T02:38）：

| 区域 | ACTIVE SA 数 | 已占用 universe | 今日已提交 | 今日配额 |
|---|---:|---|---|---|
| USA | 5 | TOP3000 (2), TOP2000 (1), TOP1000 (1) | 0 | ✅ **1 空** |
| IND | 11 | TOP500（单 universe × 11 SA） | 0 | ✅ **1 空** |
| KOR | 8 | TOP600（单 universe × 8 SA） | 0 | ✅ **1 空** |
| GBR | 2 | TOP700（单 universe × 2 SA） | 0 | ✅ **1 空** |
| GLB | 4 | TOPDIV3000 (1), MINVOL1M (2), TOP3000 (1) | 0 | ✅ **1 空** |
| DEU | 1 | TOP500（单 universe × 1 SA） | 0 | ✅ **1 空** |
| EUR | **2**（GrgGkV1o + vROOONwd） | TOP2500 (1), TOPCS1600 (1) | 0 | ✅ **1 空** |
| MEA | 2 | TOP400（单 universe × 2 SA） | 0 | ✅ **1 空**（MEA 已下线但存量 SA 保留） |

**⚠ 平台状态更新**：`get_platform_setting_options` 显示 MEA 已不在 EQUITY 支持区域列表，但存量 2 颗 SA 保留 ACTIVE；新 SA 无法在 MEA 构建。

**⚠ 探针差异**：`probe_sa_candidates.py` 缓存显示 EUR 只有 1 颗（GrgGkV1o），**未捕获 vROOONwd**（`_is_super` 判定或 `_fetch_stage` 分页边界问题，不影响方案构建，仅提示下次刷新时补跑一次）。

### 1.3 零占用档判定（决定 self 预期，勿混淆）

| 类别 | 定义 | self 预期 | 例 |
|---|---|---|---|
| **零 OS alpha 档** | 该 region×universe 无任何已提交 alpha（REGULAR+SA） | **恒 0.0000** | USA TOP500 |
| **仅零 SA 占用档** | 无 SUPER 占用但已有 REGULAR OS alpha | **非零但偏低（0.28–0.33）** | EUR TOPCS1600 首投时 |
| **同档换配方** | 同 universe 已有 SA，换 limit/中性化/decay/combo 制造不同 self | 视差异度 | IND TOP500 × 11 SA |

**优先选点顺序**：零 OS alpha 档 > 仅零 SA 占用档 > 同档换配方

### 1.4 Pyramid 倍率（`get_pyramid_multipliers` @ 2026-10-23）

| 区域 | D0 主力（PV/Analyst/News/Model/Fundamental） | D1 主力 | 备注 |
|---|---|---|---|
| USA | 1.5 / 1.7 / 1.7 / 1.6 / 1.5 | 1.1 / 1.2 / 1.2 / 1.3 / 1.1 | 双阶段均衡 |
| EUR | 1.4 / 1.6 / 1.5 / 1.6 / 1.3 | 1.1 / 1.3 / 1.3 / 1.3 / 1.1 | 双阶段均衡 |
| IND | — | 1.1 / 1.4 / 1.3 / 1.2 / 1.2 | 仅 D1 |
| KOR | — | 1.4 / 1.6 / 1.6 / 1.6 / 1.6 | 仅 D1 |
| GBR | 1.5 / 1.9 / 1.9 / 1.7 / 1.9 | 1.4 / 1.6 / 1.6 / 1.5 / 1.6 | Analyst/Fundamental 溢价最高 |
| GLB | — | 1.0 / 1.4 / 1.3 / 1.3 / 1.4 | 仅 D1，PV 无溢价 |
| DEU | 1.8 / 1.9 / 1.9 / 1.9 / 1.9 | 1.7 / 1.8 / 1.8 / 1.8 / 1.8 | 全场倍率天花板 |
| MEA | — | — | 已下线 |

> SA 本身无 pyramid 分类，但**成分 alpha 的 pyramid 归属**决定 SA 的 PV 分配；SA 提交后按成分加权分配。

---

## 2. 选点原则

1. **档位占用类型 > 组件池大小**：先选「零 OS alpha 档」（self 恒 0.0，prod 余量最大）
2. **组件池大小**：≥10 才可能（DEU 10 压线）；池越大上限越高，但需 selection 匹配
3. **指标 = 约束优化**：`max IS_s.t. self<0.7 且 prod<0.7`，优选 `prod<0.6 且 TO<0.30`（社区合格档 B）
4. **中性化族规律**：IND/KOR/GBR 走 SECTOR/SUBINDUSTRY + decay 15；USA/EUR/GLB/DEU 走 STATISTICAL + decay 1
5. **limit 从 10 起测**（l10 双闸综合最优、prod 余量最大）；池 <15 只用宽松 selection `(1 - self_correlation)`
6. **prod ≥ 0.7 = 合规红线**，无豁免入口

---

## 3. 论坛指标标准章节（引用 §0）

- **A 平台底线**：S≥1.58 · F≥1.0 · TO 0.01–0.7 · prod<0.7
- **B 社区合格档**：TO<0.30 · prod<0.6
- **C 比赛档**：S 5.6–7.0 · F 5.6–8.9 · TO 0.20–0.27 · prod<0.5

**筛选阈值**：`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`
**selection 强度必须匹配池子规模**：EUR/GLB/DEU 只能宽松 `(1 - self_correlation)`

---

## 4. 分 Region 方案

### 4.1 USA — 优先级 ★★★★★（池深 44、今日配额空、TOP500 已撞墙证伪）

**已占档位**：TOP3000 (2 SA) · TOP2000 (1 SA) · TOP1000 (1 SA)  
**可尝试 universe**：TOP500 · TOP200 · TOPSP500  
**今日配额**：✅ 1 空

#### 4.1.1 ⛔ TOP500 撞墙档案（2026-10-23 实测，本轮 SA 扫描已证伪）

| tag | 配方 | S | F | TO | self | prod | verdict | 死因 |
|---|---|---:|---:|---:|---:|---:|---|---|
| usa_top500_stat_d1_l10 | STAT · d1 · l10 · cp1 | **1.54** | 0.76 | 0.209 | 0.0000 | 0.6218 | ⛔ BLOCKED | LOW_SHARPE + LOW_FITNESS + 2Y (1.32) |
| usa_top500_sector_d15_l10 | SECTOR · d15 · l10 · cp1 | **1.42** | 1.14 | 0.075 | 0.0000 | 0.6741 | ⛔ BLOCKED | LOW_SHARPE + 2Y (1.20) |

**结论**：USA TOP500 池虽 44 颗，但**窄 universe 组件稀疏、Sharpe 天花板 1.54**，达不到 1.58 底线；即使 self 恒 0、prod 达标，双闸全红。**TOP500 判死**（除非后续攒到新的强 RA 补池）。

#### 4.1.2 推荐方案（按优先级）

| # | tag | universe | 中性化 | decay | limit | 预期 S | 预期 prod | 依据 |
|---|---|---|---|---:|---:|---:|---:|---|
| 1 | usa_top200_stat_d1_l10 | TOP200 | STATISTICAL | 1 | 10 | 3.5–4.5 | <0.6 | TOP200 更窄更集中，信号强度放大（类比 IND TOP500 出 S=4.4–5.4） |
| 2 | usa_tops500_stat_d1_l10 | TOPSP500 | STATISTICAL | 1 | 10 | 3.0–4.5 | <0.6 | TOPSP500 是 S&P 500 官方 universe，组件覆盖最优质池 |
| 3 | usa_top3000_crowding_d1_l10 | TOP3000 | CROWDING | 1 | 10 | 4.0–5.5 | 0.55–0.65 | 已占 TOP3000 但 CROWDING 是 IND 最高 Fitness 族，USA 尚未试 |

**推荐首选**：**USA TOP200 · STAT · d1 · l10**（自相关 0.0000 + prod 预期 <0.6 + 池深够）

### 4.2 EUR — 优先级 ★★★★★（池 14、今日配额空、新入 vROOONwd 有参考意义）

**已占档位**：TOP2500 (GrgGkV1o S=4.21) · TOPCS1600 (vROOONwd S=3.74)  
**可尝试 universe**：TOP1200 · TOP800 · TOP400  
**今日配额**：✅ 1 空

| # | tag | universe | 中性化 | decay | limit | 预期 S | 预期 prod | 依据 |
|---|---|---|---|---:|---:|---:|---:|---|
| 1 | eur_top800_stat_d1_l10 | TOP800 | STATISTICAL | 1 | 10 | 3.5–4.5 | <0.6 | 中档 universe，宽于 TOP2500/CS1600，未占 |
| 2 | eur_top1200_stat_d1_l10 | TOP1200 | STATISTICAL | 1 | 10 | 3.0–4.0 | <0.6 | 中间档 |
| 3 | eur_top400_stat_d1_l10 | TOP400 | STATISTICAL | 1 | 10 | 2.8–4.0 | <0.6 | 窄档，信号集中但风险高 |
| 4 | eur_top2500_subind_d15_l10 | TOP2500 | SUBINDUSTRY | 15 | 10 | 3.5–4.5 | 0.55–0.65 | 同 universe 换中性化，制造差异化 self |

**推荐首选**：**EUR TOP800 · STAT · d1 · l10**（宽 universe 保证 S 天花板，池 14 也够 l10）

### 4.3 IND — 优先级 ★★★（池 38，SA 已成型 11 颗，仅补增量）

**已占档位**：TOP500（单 universe × 11 SA，limit 从 10 到 1000 全扫过）  
**可尝试 universe**：无（IND 仅 TOP500）  
**今日配额**：✅ 1 空

**IND 现状**：SA 已覆盖 d0/d1/d5/d10/d30/d90/d100、STAT/SUBIND/SECTOR/RAM、l10/20/30/1000，**配方空间接近饱和**。剩余可尝试：CROWDING / MARKET / INDUSTRY 中性化族。

| # | tag | universe | 中性化 | decay | limit | 预期 S | 预期 prod | 依据 |
|---|---|---|---|---:|---:|---:|---:|---|
| 1 | ind_top500_crowding_d1_l10 | TOP500 | CROWDING | 1 | 10 | 5.0–7.0 | 0.55–0.65 | CROWDING 是 IND 实测 Fitness 天花板族（8.9），从未试过 |
| 2 | ind_top500_crowding_d15_l10 | TOP500 | CROWDING | 15 | 10 | 4.5–6.5 | 0.55–0.65 | CROWDING + decay 15 组合，未试 |
| 3 | ind_top500_market_d1_l10 | TOP500 | MARKET | 1 | 10 | 4.0–5.5 | 0.55–0.65 | MARKET 族从未在 IND 试过 |

**推荐首选**：**IND TOP500 · CROWDING · d1 · l10**（新中性化族，未撞墙风险最低）

### 4.4 KOR — 优先级 ★★★（池 28，SA 8 颗，可补增量）

**已占档位**：TOP600（单 universe × 8 SA，limit 10/12/13/30 全扫过）  
**可尝试 universe**：无（KOR 仅 TOP600）  
**今日配额**：✅ 1 空

| # | tag | universe | 中性化 | decay | limit | 预期 S | 预期 prod | 依据 |
|---|---|---|---|---:|---:|---:|---:|---|
| 1 | kor_top600_crowding_d1_l10 | TOP600 | CROWDING | 1 | 10 | 5.0–6.5 | 0.55–0.65 | CROWDING 在 KOR 从未试 |
| 2 | kor_top600_market_d1_l10 | TOP600 | MARKET | 1 | 10 | 4.5–6.0 | 0.55–0.65 | MARKET 从未试 |
| 3 | kor_top600_crowding_d15_l10 | TOP600 | CROWDING | 15 | 10 | 4.0–5.5 | 0.55–0.65 | CROWDING + d15 组合 |

**推荐首选**：**KOR TOP600 · CROWDING · d1 · l10**

### 4.5 GBR — 优先级 ★★（池 18，SA 2 颗，可补增量）

**已占档位**：TOP700 (2 SA: STATISTICAL, RAM)  
**可尝试 universe**：无（GBR 仅 TOP700）  
**今日配额**：✅ 1 空

| # | tag | universe | 中性化 | decay | limit | 预期 S | 预期 prod | 依据 |
|---|---|---|---|---:|---:|---:|---:|---|
| 1 | gbr_top700_crowding_d1_l10 | TOP700 | CROWDING | 1 | 10 | 3.5–5.0 | 0.55–0.65 | CROWDING 未试 |
| 2 | gbr_top700_sector_d15_l10 | TOP700 | SECTOR | 15 | 10 | 3.0–4.5 | 0.55–0.65 | SECTOR 未试（GBR 历史 SA 走 STAT+RAM） |

**推荐首选**：**GBR TOP700 · CROWDING · d1 · l10**

### 4.6 GLB — 优先级 ★★（池 11 压线，SA 4 颗，可补余量）

**已占档位**：TOPDIV3000 (1) · MINVOL1M (2) · TOP3000 (1)  
**可尝试 universe**：MINVOL10M（唯一空档）  
**今日配额**：✅ 1 空

| # | tag | universe | 中性化 | decay | limit | 预期 S | 预期 prod | 依据 |
|---|---|---|---|---:|---:|---:|---:|---|
| 1 | glb_minvol10m_stat_d1_l10 | MINVOL10M | STATISTICAL | 1 | 10 | 3.0–4.5 | <0.6 | 唯一未占 universe，池 11 够 l10 |

**推荐首选**：**GLB MINVOL10M · STAT · d1 · l10**

### 4.7 DEU — 优先级 ★（池 10 压线，SA 1 颗，风险高）

**已占档位**：TOP500 (mLYLEm99 S=2.27)  
**可尝试 universe**：无（DEU 仅 TOP500）  
**今日配额**：✅ 1 空

**⚠ 风险**：池 10 压线，任何 selection 加严都会 → `sim ERROR: At least 10 component alphas are required`。仅可用最宽松 selection `(1 - self_correlation)`。

| # | tag | universe | 中性化 | decay | limit | 预期 S | 预期 prod | 依据 |
|---|---|---|---|---:|---:|---:|---:|---|
| 1 | deu_top500_crowding_d1_l10 | TOP500 | CROWDING | 1 | 10 | 2.5–3.5 | 0.55–0.65 | CROWDING 是 DEU 倍率最高族（1.8-1.9） |
| 2 | deu_top500_crowding_d15_l10 | TOP500 | CROWDING | 15 | 10 | 2.0–3.5 | 0.55–0.65 | 备选 |

**推荐首选**：**DEU TOP500 · CROWDING · d1 · l10**（倍率最高族，但池压线，风险高）

### 4.8 MEA — 优先级 ⛔（平台已下线）

**⛔ MEA 已不在 EQUITY 支持区域列表**，但存量 2 颗 SA 保留 ACTIVE。不推荐构建新 MEA SA。

### 4.9 ASI — 优先级 ⛔（组件不足）

**⛔ ASI 组件池 9（差 1 颗）**，需先把攒着的 RA 提交补到 10 颗。**停投**。

### 4.10 HKG — 优先级 ⛔（组件严重不足）

**⛔ HKG 组件池 6（差 4 颗）**，短期无法补齐。**停投**。

---

## 5. 停投区

| 区域 | 原因 |
|---|---|
| ASI | 组件池 9/10，差 1 颗 ACTIVE REGULAR |
| HKG | 组件池 6/10，差 4 颗 ACTIVE REGULAR |
| MEA | 平台 EQUITY 已下线，仅存量 SA 保留 |

---

## 6. 撞墙档案（已验证不可用）

| 候选 | 区域 · universe | 死因 | 数据 |
|---|---|---|---|
| usa_top500_stat_d1_l10 | USA · TOP500 | LOW_SHARPE + LOW_FITNESS + 2Y | S=1.54, F=0.76, 2Y=1.32, prod=0.6218, self=0 |
| usa_top500_sector_d15_l10 | USA · TOP500 | LOW_SHARPE + 2Y | S=1.42, F=1.14, 2Y=1.20, prod=0.6741, self=0 |
| eur_topcs1600_sector_d15_l10 | EUR · TOPCS1600 | 未跑（sa_run.py 中断于第 3 颗） | — |
| glb_topdiv3000_sector_d15_l10 | GLB · TOPDIV3000 | 未跑（同上） | — |

**核心发现**：USA TOP500 的窄 universe 天花板 S≈1.54，即使 self=0、prod<0.7 也无法过 LOW_SHARPE 底线。**判 USA TOP500 为撞墙 universe**，短期不可救（除非攒更多强 RA 补池）。

---

## 7. 执行清单

### 7.1 关键约束（铁律）

- **只挖不提交**：所有方案全部为待执行配方，**默认不做任何提交动作**（提交权归用户）
- **prod ≥ 0.7 = 合规红线，无豁免入口**
- **组件池只看 ACTIVE 已提交 REGULAR**（IS 阶段 UNSUBMITTED 不计入）
- **SUPER 配额 1/天/区**，与 REGULAR 4/天/区独立计数
- **台账 prod > 48h 不可信**，必须 `check_correlation(refresh=True)` 重测
- 提交前先停掉后台 sa_run.py 批次（并发会加剧代理不稳，导致 `_probe_prod_max` 抛 ProxyError 中止）

### 7.2 建议今日执行顺序（若用户决定执行构建）

按优先级从高到低，每区最多 1 颗（配额约束）：

```bash
# 前置：先停 RA campaign 避免 API 争用（可选）
# taskkill /PID <full_template_campaign PID> /F   # 视情况

# 步骤 1: USA TOP200 (最高价值 - 池深 + 未占 universe)
python C:/Users/MENGTAO/wqb-scripts/sa_run.py \
  --configs results/sa_20261023_configs.json \
  --out results/sa_20261023/res.jsonl

# 步骤 2: EUR TOP800 (新 universe)
# ... (修改 configs.json)

# 步骤 3: IND TOP500 CROWDING (新中性化族)
# 步骤 4: KOR TOP600 CROWDING
# 步骤 5: GBR TOP700 CROWDING
# 步骤 6: GLB MINVOL10M
# 步骤 7: DEU TOP500 CROWDING (池压线风险高，最后跑)
```

### 7.3 今日 configs.json 建议（7 颗，每区 1 颗）

```json
[
  {"tag":"usa_top200_stat_d1_l10",   "region":"USA","universe":"TOP200",     "delay":1,"neutralization":"STATISTICAL","decay":1, "combo_power":1,"selection_limit":10,"truncation":0.02},
  {"tag":"eur_top800_stat_d1_l10",   "region":"EUR","universe":"TOP800",     "delay":1,"neutralization":"STATISTICAL","decay":1, "combo_power":1,"selection_limit":10,"truncation":0.02},
  {"tag":"ind_top500_crowding_d1_l10","region":"IND","universe":"TOP500",    "delay":1,"neutralization":"CROWDING",   "decay":1, "combo_power":1,"selection_limit":10,"truncation":0.02},
  {"tag":"kor_top600_crowding_d1_l10","region":"KOR","universe":"TOP600",    "delay":1,"neutralization":"CROWDING",   "decay":1, "combo_power":1,"selection_limit":10,"truncation":0.02},
  {"tag":"gbr_top700_crowding_d1_l10","region":"GBR","universe":"TOP700",    "delay":1,"neutralization":"CROWDING",   "decay":1, "combo_power":1,"selection_limit":10,"truncation":0.02},
  {"tag":"glb_minvol10m_stat_d1_l10","region":"GLB","universe":"MINVOL10M",  "delay":1,"neutralization":"STATISTICAL","decay":1, "combo_power":1,"selection_limit":10,"truncation":0.02},
  {"tag":"deu_top500_crowding_d1_l10","region":"DEU","universe":"TOP500",    "delay":1,"neutralization":"CROWDING",   "decay":1, "combo_power":1,"selection_limit":10,"truncation":0.02}
]
```

**超时控制**：每批后台跑（nohup 写日志文件，勿用管道），10 分钟检查落盘文件 `res.<tag>.json`。

### 7.4 提交命令（仅在用户明确点名某颗 alpha 时执行）

```bash
cd D:/coding/traeCN_project/wqb && \
WQB_ALLOW_ALPHA_SUBMIT=1 \
<venv python> tools/super_build.py submit --alpha-id <id> --region <REGION>
```

**⚠ 提交前置**：先停掉后台 sa_run.py 批次（并发加剧代理不稳 → `_probe_prod_max` ProxyError）  
**内置 prod 闸**：0.7 fail-closed，**无豁免参数**  
**复核**：等满 flip 窗（~250s）后 `tools/super_build.py status --alpha-id <id>` 确认 `status=ACTIVE`，**不只看 POST 回执**

---

## 8. 附：本轮 SA 扫描实际执行摘要

- **执行时间**：2026-10-22 23:41（数据快照）→ 2026-10-23 02:38（API 直连刷新）
- **sa_run.py 状态**：中断于第 3 颗（qMEOAmqv = usa_top500_subind_d15_l10）后 PC 等待超时
- **完成 2 颗**：usa_top500_stat_d1_l10 (BLOCKED)、usa_top500_sector_d15_l10 (BLOCKED)
- **未跑 4 颗**：usa_top500_subind_d15_l10、usa_illiq_stat_d1_l10、eur_topcs1600_sector_d15_l10、glb_topdiv3000_sector_d15_l10
- **探针 vs API 差异**：vROOONwd（EUR TOPCS1600 l10 S=3.74，2026-10-21 提交）在 API 存在但探针缓存缺失，下次 `--refresh` 时应排查 `_is_super` 判定
