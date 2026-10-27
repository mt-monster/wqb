# 各 Region 最优 SuperAlpha 方案（2026-10-23 夜巡 · 23:40–次日 00:30）

> **执行摘要 · 一句话**：本轮 14 档实测出 **2 颗安全可交付候选**：**EUR TOP2500 CROWDING d1 l10 = `kqJOQgnk`**（S3.92/F3.40，prod **0.6546** 余量 0.045 / self 0.5765）与 **USA TOP500 CROWDING d1 l10 = `LL5rpRY2`**（S1.74/F1.25/2Y1.86，prod **0.653** 余量 0.047 / **self 0.0000**）；**CROWDING 被证实为本工作区最强 SA 中性化族**——它把 USA TOP500 从 STAT 版的 S1.54（判死）抬到 S1.74（过关），**推翻昨日「USA TOP500 撞墙」结论**；**GLB TOP3000 / KOR TOP600 l14 / DEU TOP500 / EUR TOP1200 / USA TOPSP500 五档确认撞墙**（self/prod 0.73–0.94 或 2Y 1.50）。**剩余方案仅构建、不提交**，提交权归用户。
> **执行更新（2026-10-24 10:47）**：`kqJOQgnk` 已由用户点名提交并确认 **ACTIVE**（name `EUR_S_10comp_JOQgnk`，checks 8 项全 PASS）⇒ **EUR 封档**，SA 存量 36 → **37**。

### 优先队列（按价值排序）

| 序 | alpha | 区域 · 档位 | S / F | TO | self | prod | 双闸余量 | 状态 |
|---|---|---|---|---:|---:|---:|---:|---|
| **1** | **`kqJOQgnk`** | **EUR · TOP2500** | **3.92 / 3.40** | 0.148 | 0.5765 | **0.6546** | prod 0.045 / self 0.124 | ✅ **已提交 ACTIVE（2026-10-24 10:47）** |
| **2** | **`LL5rpRY2`** | **USA · TOP500**（零 OS 档） | **1.74 / 1.25** | 0.165 | **0.0000** | **0.6530** | prod 0.047 / self 0.700 | ✅ **可交付，待点名** |
| 3 | `Vkd5pK6M` | GLB · MINVOL10M（零 OS 档） | 4.25 / 2.66 | 0.240 | 0.0000 | 0.6917 | prod **0.008** | ⚠ 边缘，余量不足 |
| 4 | `1YjPdQJR` | GBR · TOP700 · SLOW | 3.95 / 3.29 | 0.171 | 0.6985 | 0.6983 | self **0.0015** | ⚠ 边缘，余量不足 |
| 5 | `gJWdxLbM` | EUR · TOPCS1600 | 3.73 / 3.41 | 0.150 | 0.6985 | 0.6988 | prod **0.0012** | ⚠ 边缘，余量不足 |
| 6 | `wp9P5Wld` | GBR · TOP700 · CROWDING | 3.27 / 3.18 | 0.153 | 0.626 | **0.7122** | −0.012 | ⛔ 超红线 |

> 提交配额 SUPER **1/天/区** ⇒ 序 1（EUR）与序 2（USA）**可在同一天分别提交**（跨区独立计数）。

---

## 0. 论坛指标标准（2026-10-22 调研定稿）

> 来源：《【新人入门】Super Alpha 从入门到入门！》78 赞/39 评论 ·《2024 super alpha 比赛心得》22 赞/15 评论 ·《Super Alpha 参数设置》12 赞（含 LY43440 实测回复）。本工作区实测佐证见 `.workbuddy/memory/2026-10-22.md` 与 `2026-10-23.md`。

### 0.1 组成数量（Selection Limit）

- **平台硬下限 = 10**（<10 直接 400：`Ensure this value is greater than or equal to 10`）
- 论坛 78 赞帖建议 **30–100 起测、≤500**；LY43440 实测 IND 取 300（long/short 各 ~250）
- **实际生效数 = min(limit, 组件池)**；**组件池是 region 级**（非 universe 级）⇒ SA 指标天花板由该 region 的 ACTIVE REGULAR 数决定
  - USA 44 / IND 38 / KOR 28 / MEA 19 / GBR 18 / EUR 14 / GLB 11 / DEU 10

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
- 小池区（EUR 14 / GLB 11 / DEU 10）**只能用宽松 selection** `(1 - self_correlation)`；论坛严格阈值仅适用于 IND/USA 等大池区

### 0.4 中性化族规律

- **Fitness 排序**（IND 实测）：**CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3**
- **选族规则**：**TO<0.10 → SLOW；TO>0.20 → FAST**
- **区域族基线（本轮修正）**：**CROWDING + decay 1 + l10 是跨区通用最优族**（KOR S4.11/F5.94、EUR S3.92/F3.40、USA S4.03/F4.73 均为该族给出各区最高 F）；STATISTICAL 退居次选
- ⚠ **组件数↑ ⇒ self↑ 且 prod↑**（本轮 GBR l10→l14：self 0.626→0.689、prod 0.712→0.740；KOR l10→l14：0.673→**0.935**）⇒ **l10 是唯一甜点，不要加大 limit**

### 0.5 其他实证

- truncation 0.02 vs 0.08 对 SA 几乎无差异（S 3.74 vs 3.73）
- 论坛推荐 `Selection Handling = Non-Zero`；本工作区历史 36 颗 SA 全用 POSITIVE 均成功

---

## 1. 数据基线（2026-10-23 23:45 实时）⚠ 本轮已清 `api_cache` 强制回源

> **踩坑记录**：`probe_sa_candidates.py --refresh` 仍会命中 `data/wqb.db::api_cache`（OS 池 7 天缓存），导致昨日 08:08 提交的 `RRA9EZKz` 缺失（报 34 颗 vs 实际 36 颗）。**刷新前必先** `DELETE FROM api_cache WHERE cache_key LIKE 'user_alphas%'`（本轮清掉 105 条）。

### 1.1 组件池 eligibility（ACTIVE 已提交 REGULAR；IS 阶段 UNSUBMITTED 不计入）

| 区域 | ACTIVE 已提交 | UNSUBMITTED IS | verdict | 本轮状态 |
|---|---:|---:|---|---|
| USA | **44** | 277 | **GO** | ⛔ 停投（prod 天花板 0.74–0.84） |
| IND | **38** | 127 | **GO** | ⚠ 降权（TOP500 已 11 颗 SA） |
| KOR | **28** | 0 | **GO** | ⛔ 饱和（l14 撞 0.935；昨日已投 l10） |
| MEA | **19** | 0 | **GO** | ⛔ **平台已下线**（不在 EQUITY 选项） |
| GBR | **18** | 0 | **GO** | ⚠ 边缘（CROWDING l10 prod 0.7122，差 0.012） |
| EUR | **14** | 546 | **GO** | ✅ **本轮最优**（CROWDING l10 PASS） |
| GLB | **11** | 0 | **GO** | ⚠ 压线（TOP3000 已撞 0.864） |
| DEU | **10** | 0 | **GO**（压线）| ⛔ 撞墙（self/prod 0.764） |
| ASI | 9 | 0 | ⛔ **BLOCKED（差 1 颗）** | — |
| HKG | 6 | 0 | ⛔ **BLOCKED（差 4 颗）** | — |

### 1.2 已提交 SUPER 档位占用（**36 颗 ACTIVE**，实时）

| 区域 | SA 数 | universe 分布 | 今日配额（ET 10-23） |
|---|---:|---|---|
| USA | 5 | TOP3000×3, TOP2000×1, TOP1000×1 | ✅ 可投（但指标不可达） |
| IND | 11 | TOP500×11 | ✅ 可投 |
| KOR | **9** | TOP600×9（含昨日 `RRA9EZKz`） | ⚠ **可能已用**（RRA9EZKz 于 ET 10-22 20:08 提交，UTC 已跨日 ⇒ 需当场核） |
| GBR | 2 | TOP700×2 | ✅ 可投 |
| GLB | 4 | TOPDIV3000×1, MINVOL1M×2, TOP3000×1 | ✅ 可投 |
| DEU | 1 | TOP500×1 | ✅ 可投 |
| EUR | 2 | TOP2500×1（`GrgGkV1o`）, TOPCS1600×1（`vROOONwd`） | ✅ 可投 |
| MEA | 2 | TOP400×2 | ⛔ 已下线 |

### 1.3 档位占用分类（决定 self 预期）

| 类别 | 定义 | self 预期 | 本轮实例 |
|---|---|---|---|
| **零 OS alpha 档** | 该 region×universe 无任何已提交 alpha | **恒 0.0000** | USA TOP500 / TOP200 / TOPSP500；**GLB MINVOL10M**；EUR TOP1200 / TOP800 / TOP400 |
| **仅零 SA 占用档** | 有 REGULAR OS 但无 SUPER | 非零偏低 | —（本账户无此档） |
| **同档换配方** | 同 universe 已有 SA | 视堆叠数，越高越险 | KOR TOP600（9 颗，self 已 0.673） |

**平台合法 universe 全集**（`get_platform_setting_options`）：
USA `TOP3000/2000/1000/500/200/TOPSP500`｜GLB `TOP3000/MINVOL1M/MINVOL10M/TOPDIV3000`｜EUR `TOP2500/1200/800/400/TOPCS1600`｜**KOR `TOP600`（唯一）｜IND `TOP500`（唯一）｜DEU `TOP500`（唯一）｜GBR `TOP700`（唯一）**｜ASI `MINVOL1M/MINVOL10M/TOP500`｜HKG `TOP800/TOP500`

> ★ **结构性约束**：KOR / IND / DEU / GBR 只有**唯一 universe** ⇒ 所有 SA 必然堆在同一档 ⇒ self 随颗数单调上升 ⇒ **这四区的可投颗数有硬上限**（KOR 已到顶）。

### 1.4 Pyramid 倍率（`get_pyramid_multipliers`）

| 区域 | D0（PV/Analyst/News/Model/Fund） | D1（同序） | 备注 |
|---|---|---|---|
| USA | 1.5 / 1.7 / 1.7 / 1.6 / 1.5 | 1.1 / 1.2 / 1.2 / 1.3 / 1.1 | 双阶段均衡 |
| EUR | 1.4 / 1.6 / 1.5 / 1.6 / 1.3 | 1.1 / 1.3 / 1.3 / 1.3 / 1.1 | 双阶段均衡 |
| GBR | 1.5 / 1.9 / 1.9 / 1.7 / 1.9 | 1.4 / 1.6 / 1.6 / 1.5 / 1.6 | Analyst/Fund 溢价高 |
| DEU | 1.8 / 1.9 / 1.9 / 1.9 / 1.9 | 1.7 / 1.8 / 1.8 / 1.8 / 1.8 | **全场倍率天花板** |
| KOR | — | 1.4 / 1.6 / 1.6 / 1.6 / 1.6 | 仅 D1 |
| IND | — | 1.1 / 1.4 / 1.3 / 1.2 / 1.2 | 仅 D1 |
| GLB | — | 1.0 / 1.4 / 1.3 / 1.3 / 1.4 | 仅 D1，PV 无溢价 |
| ASI | — | 1.0 / 1.5 / 1.2 / 1.2 / 1.1 | 仅 D1 |
| HKG | — | 1.5 / 1.7 / 1.6 / 1.7 / 1.6 | 仅 D1 |
| MEA | — | — | **已下线** |

---

## 2. 选点原则（本轮修正）

1. **先判「该 universe 已被几颗 SA 堆过」> 组件池大小**：唯一 universe 区（KOR/IND/DEU/GBR）随颗数 self 单调上升，**KOR TOP600 已到顶（9 颗，self 0.673）**
2. **零 OS 档 self=0，S 的天花板由中性化族决定**：USA TOP500 用 STAT 只有 S1.54（判死），换 **CROWDING 后 S1.74 过关** ⇒ **零档的 S 不足不是死因，中性化族选错才是**。但 CROWDING 也救不了 TOPSP500（S1.70 但 2Y 仅 1.50）。
3. **指标 = 约束优化**：`max IS s.t. self<0.7 且 prod<0.7`，优选 `prod<0.6 且 TO<0.30`（社区合格档 B）
4. **中性化族首选 CROWDING + decay 1 + l10**（本轮跨区验证：KOR / EUR / GBR / USA 各自的最高 F 都由该族给出）
5. **limit 恒取 10**（l14 实测 self/prod 双升，KOR 直接 0.673 → 0.935）
6. **prod ≥ 0.7 = 合规红线**，无豁免入口；**余量 <0.02 视为不可交付**

---

## 3. 本轮实测

### 3.1 v6 六档（2026-10-23 23:57–00:25）— 零 OS 档 + 换族/换 selection

| # | tag | alpha | 配方 | S | F | TO | self | prod | 判定 |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | glb_minvol10m_crowding_d1_l10 | `Vkd5pK6M` | CROWDING·d1·l10（**零 OS 档**） | **4.25** | 2.66 | 0.240 | **0.0000** | **0.6917** | ⚠ PASS，**余量 0.008 不足** |
| 2 | **usa_top500_crowding_d1_l10** | **`LL5rpRY2`** | CROWDING·d1·l10（**零 OS 档**） | **1.74** | 1.25 | 0.165 | **0.0000** | **0.6530** | ✅ **PASS，余量 0.047** |
| 3 | usa_tops500_crowding_d1_l10 | `KPmQbJ1l` | CROWDING·d1·l10（零 OS 档） | 1.70 | 1.16 | 0.157 | 0.0000 | 0.6246 | ⛔ **2Y=1.50 <1.58** |
| 4 | eur_top1200_crowding_d1_l10 | `npAQgjYM` | CROWDING·d1·l10（零 OS 档） | 2.06 | 1.47 | 0.163 | 0.0000 | **0.7337** | ⛔ prod 超 0.034 |
| 5 | gbr_top700_slow_d1_l10 | `1YjPdQJR` | **SLOW**·d1·l10 | 3.95 | 3.29 | 0.171 | **0.6985** | **0.6983** | ⚠ PASS，**双闸余量均 <0.002** |
| 6 | gbr_top700_crowding_d1_l10_prodsel | — | CROWDING + `selection (prod_correlation<0.6)*(1-self_correlation)` | — | — | — | — | — | ⛔ **sim ERROR: At least 10 component alphas are required** |

**`LL5rpRY2` 完整指标**（`get_alpha_details` 复核）：2Y **1.86**（ladder window 7）｜sub-universe 1.22｜investability S **1.58** / F 1.15｜`failed_ra_count=0`、`failed_ppa_count=0`｜`checks.fail=[]`（LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / IS_LADDER_SHARPE / CLUSTER_TEST 全过）｜`check_correlation(refresh=True)`：prod **0.6530** / self **0.0000** / `all_passed=true`。

**`kqJOQgnk` 复核**：`check_correlation(refresh=True)` prod **0.6546** / self **0.5765**（top-1 自相关 = `GrgGkV1o` 0.576，其余 ≤0.32）/ `all_passed=true`。

### 3.2 v5 八档（2026-10-23 23:44–00:10）— CROWDING 跨区铺开

| # | tag | alpha | 配方 | S | F | TO | self | prod | 判定 |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | gbr_top700_crowding_d1_l10 | `wp9P5Wld` | CROWDING·d1·l10 | 3.27 | 3.18 | 0.153 | 0.626 | **0.7122** | ⛔ prod 超 0.0122 |
| 2 | gbr_top700_crowding_d1_l14 | `MP0ZkM0L` | CROWDING·d1·l14 | 3.09 | 3.21 | 0.134 | 0.689 | **0.7399** | ⛔ 双闸逼近红线 |
| 3 | deu_top500_crowding_d1_l10 | `MP0ZkqKz` | CROWDING·d1·l10 | 2.42 | 2.24 | 0.139 | **0.7642** | **0.7640** | ⛔ **DEU 撞墙** |
| 4 | **eur_top2500_crowding_d1_l10** | **`kqJOQgnk`** | CROWDING·d1·l10 | **3.92** | **3.40** | **0.148** | **0.5765** | **0.6546** | ✅ **PASS（prod 余量 0.045）** |
| 5 | eur_topcs1600_crowding_d1_l10 | `gJWdxLbM` | CROWDING·d1·l10 | 3.73 | 3.41 | 0.150 | 0.6985 | **0.6988** | ⚠ 名义 PASS，**余量 0.0012 ⇒ 不可交付** |
| 6 | glb_top3000_crowding_d1_l10 | `88vYL9dV` | CROWDING·d1·l10 | 3.71 | 2.11 | 0.243 | **0.8642** | **0.8638** | ⛔ **GLB TOP3000 撞墙** |
| 7 | usa_top3000_crowding_d1_l10 | `QPYgQlWM` | CROWDING·d1·l10 | 4.03 | 4.73 | 0.141 | 0.6510 | **0.7433** | ⛔ prod 超 0.0433 |
| 8 | kor_top600_crowding_d1_l14 | `0mj68xwG` | CROWDING·d1·l14 | **4.89** | **6.24** | 0.190 | **0.9351** | **0.9351** | ⛔ **KOR 饱和撞墙** |

### 3.3 四条硬结论

1. **CROWDING 是本工作区最强 SA 中性化族，且能抬 S**：USA TOP500 STAT 1.54（判死）→ CROWDING **1.74**（过关）；GBR TOP700 CROWDING 3.27/3.18 → SLOW 3.95/3.29（F 更高）。**它是唯一能突破「窄 universe S 天花板」的杠杆。**
2. **CROWDING 不改 prod 上限**：同一族下 USA TOP3000 prod 0.743、GBR TOP700 0.712、EUR TOP2500 0.655、USA TOP500 0.653 ⇒ **prod 上限由「region × universe 的既有堆叠密度」决定**。CROWDING 的作用是把 S/F 推到该档天花板，**让本来就够得着 0.7 的档够得着**。
3. **l10 是唯一甜点且窗口极窄**：KOR l10→l14 self 0.673→**0.935**、GBR l10→l14 0.626→0.689 ⇒ **唯一 universe 区每加一颗 SA，下一颗 self 抬一档**，KOR 已无第 10 颗空间。
4. **零 OS 档 self 恒 0，但救不了 prod**：USA TOP500 / GLB MINVOL10M / EUR TOP1200 三个零档 self 都是 0，prod 却分别是 0.653 / **0.692** / **0.734** ⇒ **零档只消除「自己的历史堆叠」，不消除「别人在该 universe 的堆叠」**，USA TOP500 能过是因为该档竞争少，EUR TOP1200 过不了是因为拥挤。

---

## 4. 撞墙档案（已验证不可用，勿重试）

| 档位 | 配方 | 最好结果 | 死因 |
|---|---|---|---|
| USA TOP3000 | CROWDING d1 l10 | S4.03 F4.73 prod **0.7433** | prod 不可降（宽 universe 天花板 0.74–0.84） |
| USA TOP3000 | STAT d22 l30 / l50、SUBIND d10 l100 | prod 0.799–0.835 | prod 红 |
| **USA TOP500** | STAT d1 l10 / l15 | S 1.54 / 1.46 | ⚠ **仅 STAT 判死；换 CROWDING 后 S1.74 过关** ⇒ 不算撞墙 |
| USA TOP200 | STAT d1 l10 / l15、CROWDING d1 l10 | S 0.94–0.96 | S 天花板 <1.0，真死 |
| USA TOPSP500 | STAT d1 l15 / **CROWDING d1 l10** | S1.46 / **S1.70，2Y 1.50** | **2Y 差 0.08**，CROWDING 也救不回 ⇒ 撞墙 |
| EUR TOP1200 | STAT d1 l10 / **CROWDING d1 l10** | S2.15（2Y 0.89）/ **S2.06 prod 0.734** | 窄 universe 拥挤，prod 不可降 |
| GLB TOP3000 | CROWDING d1 l10 | self **0.864** / prod 0.864 | 档位堆满 |
| KOR TOP600 | CROWDING d1 **l14** | self **0.935** / prod 0.935 | 档位饱和 |
| DEU TOP500 | CROWDING d1 l10 | self **0.764** / prod 0.764 | 池=10 全量入选，self 无稀释空间 |
| IND TOP500 | CROWDING d1 l10 / d15 l10 | prod **0.822** / 0.725 | 11 颗 SA 堆叠 |
| EUR TOP800 / TOP400 | STAT d1 l10 | S 1.34–2.15、2Y 0.77–0.89 | S / 2Y 双不足 |
| **GBR TOP700** | selection `(prod_correlation<0.6)*(1-self_correlation)` | **sim ERROR** | ⚠ 池 18 中 prod_corr<0.6 的组件 **<10** ⇒ 触发 §0.3 硬错，**小池区禁用严格 selection** |
| MEA | — | — | **平台已下线**，无法新建 |
| ASI / HKG | — | — | 组件池 9 / 6 < 10 |

---

## 5. 分 Region 方案（按价值排序）

### 5.1 可交付候选（双闸余量 ≥0.02）

| 区域 | 档位 | 配方 | alpha | S | F | TO | 2Y | self | prod | 双闸余量 | 达标档 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| **EUR** | TOP2500 | **CROWDING · d1 · l10 · trunc0.02** | **`kqJOQgnk`** ✅已提交 | **3.92** | **3.40** | 0.1481 | ladder 3.81 | 0.5765 | **0.6546** | prod 0.045 / self 0.124 | A 底线 + TO 达 B 档 |
| **USA** | TOP500（**零 OS 档**） | **CROWDING · d1 · l10 · trunc0.02** | **`LL5rpRY2`** | 1.74 | 1.25 | 0.165 | **1.86** | **0.0000** | **0.6530** | prod 0.047 / self 0.700 | A 底线 + TO 达 B 档 |

**`kqJOQgnk` 提交实录（2026-10-24 10:47，用户点名）**：停后台 campaign → prod 闸 max 0.6546 过闸 → props name `EUR_S_10comp_JOQgnk` → POST 201 → 等 flip 250s → **status=ACTIVE**。checks 8 项全 PASS（含 LOW_SUB_UNIVERSE_SHARPE **2.71/2.04**、IS_LADDER_SHARPE **3.81/2.02**、CLUSTER_TEST **2.31/1.58**），唯一 WARNING = OSMOSIS_ALLOCATION（不影响通过）。
**EUR 后续**：TOP2500 已占 GrgGkV1o + kqJOQgnk，TOPCS1600 已在 0.699 ⇒ **EUR 封档，不再有可交付空档**（今日配额亦已 1/1 用尽）。
**USA 后续**：TOP500 是零 OS 档，投完 `LL5rpRY2` 后该档 self 不再为 0；USA 其余档（TOP3000 / TOPSP500 / TOP200）全部撞墙 ⇒ **USA 也只有这一颗**。

### 5.2 边缘候选（平台 PASS 但余量 <0.02，不建议交付）

| 区域 | 档位 | alpha | S / F | TO | self | prod | 卡点 |
|---|---|---|---:|---:|---:|---:|---|
| GLB | MINVOL10M（零 OS 档） | `Vkd5pK6M` | 4.25 / 2.66 | 0.240 | 0.0000 | 0.6917 | prod 余量 0.008 |
| GBR | TOP700 · SLOW | `1YjPdQJR` | 3.95 / 3.29 | 0.171 | 0.6985 | 0.6983 | self 余量 0.0015 |
| EUR | TOPCS1600 | `gJWdxLbM` | 3.73 / 3.41 | 0.150 | 0.6985 | 0.6988 | prod 余量 0.0012 |

> prod/self 会随平台池变动漂移，**余量 <0.02 的候选在提交 flip 窗内可能被抬过红线** ⇒ 一律不交付；如需使用，必须 `check_correlation(refresh=True)` 当场复测后再决策。

### 5.3 下一轮待探（本轮未覆盖的高价值空档）

| 区域 · 档位 | 配方建议 | 依据 |
|---|---|---|
| EUR TOP800 / TOP400（零 OS 档） | CROWDING · d1 · l10 | TOP1200 已证 CROWDING 可把 S 抬到 2.06（STAT 版 2.15 但 2Y 0.89），窄档需逐档实测 |
| GLB TOPDIV3000 | CROWDING · d1 · l10 | 该档已有 1 颗 STAT SA（self 0.328 / prod 0.513，余量大） |
| USA TOP1000 / TOP2000 | CROWDING · d1 · l10 | 各有 1 颗 STAT SA 占用，self 0.6217–0.6601，余量薄 |
| IND TOP500 | 无（唯一 universe，11 颗 SA） | — |

---

## 6. 停投区

| 区域 | 判定 | 理由 |
|---|---|---|
| **USA** | ⚠ **仅剩 TOP500 一颗** | 宽 universe（TOP3000/2000/1000）prod 天花板 0.743–0.835；TOP200 S<1.0；TOPSP500 2Y 1.50 ⇒ **只有 TOP500 零档 + CROWDING 可过，投完即封** |
| **KOR** | ⛔ 停投 | 唯一 universe 已堆 9 颗 SA，l10 已吃到 0.673；l14 直接 0.935 ⇒ 无第 10 颗空间 |
| **DEU** | ⛔ 停投 | 池=10 ⇒ l10 = 全量入选，self 0.764 无稀释空间 |
| **IND** | ⚠ 降权 | TOP500 已 11 颗 SA，CROWDING 仍 prod 0.822；唯一 universe 无法换档 |
| **MEA** | ⛔ 不可建 | 平台已下线 |
| **ASI / HKG** | ⛔ 不可建 | 组件池 9 / 6 < 10；需先提交攒着的 RA |

---

## 7. 执行清单

### 7.1 构建（可立即执行）

```bash
# v5（已完成，8 档）
D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe \
  C:/Users/MENGTAO/wqb-scripts/sa_run.py \
  --configs D:/coding/traeCN_project/wqb/results/sa_20261023_night/configs_v5.json \
  --out     D:/coding/traeCN_project/wqb/results/sa_20261023_night/res.jsonl

# v6（6 档：零 OS 档 + 换族 / 换 selection 降 prod）
  ... --configs .../configs_v6.json --out .../res_v6.jsonl
```

configs 字段：`tag / region / universe / delay / neutralization / decay / combo_power / selection_limit / truncation [/ selection]`
默认 selection = `(1 + 0 * (prod_correlation > 0)) * (1 - self_correlation)`，combo = `w`（按 self-corr 归一后的等权组合）。

### 7.2 提交（**仅当用户明确点名某颗 alpha**）

```bash
cd D:/coding/traeCN_project/wqb
# ① 先停掉后台 sa_run.py 批次（并发会加剧代理不稳）
# ② 提交（内置 prod 闸 0.7，fail-closed，无豁免参数）
WQB_ALLOW_ALPHA_SUBMIT=1 \
  D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py submit --alpha-id <id> --region <REGION>
# ③ 等满 flip 窗 ~250s 后复核，不只看 POST 回执
  ... tools/super_build.py status --alpha-id <id>     # 必须看到 status=ACTIVE
```

### 7.3 配额约束

- SUPER **1/天/区**，与 REGULAR 4/天/区**独立计数**
- 本轮可投区：EUR / GBR / GLB / USA / IND / DEU（KOR 需当场核 UTC/ET 计日）
- 每区每天最多落 1 颗 ⇒ 队列需按「一天一区一颗」排期

### 7.4 建议执行顺序

1. **EUR `kqJOQgnk`**（TOP2500，S3.92/F3.40，余量 0.045）与 **USA `LL5rpRY2`**（TOP500，S1.74/2Y1.86，余量 0.047）→ **两颗可同日提交**（跨区配额独立），需用户逐颗点名
2. 投完这两颗后，EUR 与 USA 均封档；转 §5.3 待探空档（EUR TOP800/TOP400、GLB TOPDIV3000）
3. 边缘候选（§5.2）**不主动交付**；确需使用必须先 `refresh=True` 复测且余量回到 ≥0.02

---

## 8. 铁律

- **只挖不提交**：方案全部为待执行配方，**默认不做任何提交动作**（提交权归用户）
- **prod ≥ 0.7 = 合规红线，无豁免入口**
- 组件池只看 ACTIVE 已提交 REGULAR（IS 阶段 UNSUBMITTED 不计入）
- 台账 prod > 48h 不可信，提交前必须 `check_correlation(refresh=True)` 当场终验
- **刷新池盘点前必先清缓存**：`DELETE FROM api_cache WHERE cache_key LIKE 'user_alphas%'`，否则 7 天缓存会漏掉刚提交的 SA（本轮实测：漏 `RRA9EZKz`）
- 方案文档产物：`output_report/SA_best_per_region_plan_20261023.md`（上午版已备份为 `SA_best_per_region_plan_am_20261023.md`）
- 构建产物：`results/sa_20261023_night/`（configs_v5/v6.json、res.jsonl、res_v6.jsonl、slots.json、run_v5/v6.log）
