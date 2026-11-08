# 各 Region 最优 SuperAlpha 方案 — 全流程扫描报告（06:30 更新版）

**生成时间**: 2026-11-06 06:4x GMT+8（凌晨 02:05 版已备份为 `SA_best_per_region_plan_20261106_am.md`）
**工作目录**: `D:\coding\traeCN_project\wqb` ｜ **结果目录**: `results/sa_scan_20261106/`
**本轮增量**: ①清缓存重刷组件池/档位/pyramid ②补齐凌晨遗留 3 颗新席的 `refresh=True` 双闸终验 ③读平台官方 SA 三份文档，纠正「103 算子=全部」的审计错误 ④按官方 `in()` 语法新建 6 档 `configs_v2.json` 批次
**铁律**: **只挖不提交** —— 本报告全部为待执行配方，本轮无任何提交动作。提交权归用户且须点名。`prod ≥ 0.7` 为无豁免红线。

---

## 一、执行摘要

### 1.1 本轮七条结论

1. **★★★ 凌晨队列的 3 颗「prod 待终验」全部补齐，且全部 PASS**（`check_correlation(refresh=True)`）：
   `88RNX7la` **0.5856**（余量 0.114）｜`e75avmq6` **0.6373**（余量 0.063）｜`88RNY77v` **0.6647**（余量 0.035）。
   ⇒ 收入序前 3 名不再有数据缺口，**Day 1/2/3 队列可直接执行**（仍须用户点名）。
2. **★★★ 「self ≈ prod 恒等」被反例推翻**：`e75avmq6` self **0.4871** 但 prod **0.6373**，差 **0.1502**。
   self 是本地 OS 池相关、prod 是平台生产池相关；旧候选常相等只是巧合。**两闸必须各自实测，禁止互推**。
3. **★★★ 凌晨「103 个算子 = 平台全部、100% 覆盖」是错的**。权威《SuperAlpha Operators》附录列出 **≥180 个** SA 可用算子（`get_operators` 的 103 个只是 REGULAR 表达式全集）。
   SELECTION 栏官方标 x 的 **41 个** + `in` / `universe_size` ⇒ **≥43 个**（凌晨只算 27 个）。
   COMBO 栏还含大量 `get_operators` 未收录的 SA 专用算子：`combo_weight`、`ts_ir`、`ts_entropy`、`ts_weighted_decay`、`ts_theilsen`、`inst_pnl`、`inst_tvr`、`group_vector_neut`、`regression_neut`、`purify`、`sigmoid`、`tanh`、`nan_mask`… ≈160 个。
4. **★★ 官方《Selection Expression》给出 26 个 alpha 属性 + 19 个 `author_*` 属性，凌晨只列了 16+2**。
   新增可消费字段：`dataset`、`dataset_count`、`datacategories`、`datacategory_count`、`datafield_count`、`classifications`、`competitions`、`favorite`、`name`、`universe_size(universe)`、`os_start_date`。
   ⇒ **`author_*` 是作者级聚合量，同一作者的所有 alpha 恒为同一个值** —— 这才是论坛 §0.3 `author_fitness≥2` 在本账户不可消费的根因（不是"阈值太严"，是字段无方差）。
5. **★ 凌晨「字符串字段 `equal/not_equal` 不筛组件」归因不准**：`category` 官方合法值确实含 `"ANALYST"`，但 **自有 alpha 默认 `"NONE"`** ⇒ `category=="ANALYST"` 恒 0，只是**常数缩放**（单调、不换席）。
   真正带区分度的是平台自动打标的 **`datacategories`**（数据集类别），须用 `in(datacategories, "...")` 消费。
6. **★★★ `in()` 集合字段必须逐区验证「有方差」**：USA `in(datacategories,"analyst")` 真开新席（self **0.1576** 全表最低）但 **prod 0.7109 撞红线**（`refresh=True` 复核一致）；KOR `in(datacategories,"news")` 与旧席 **逐位相同**（互测 1.0000）⇒ 该字段在 KOR 自有池恒常数。⇒ 集合字段不是普适杠杆，先查池内分布。
7. **★★ `dataset_count==1` 分档是 IND 唯一双赢杠杆**：`3qoG6nEe` self 0.6101→**0.4714**、prod 0.6097→**0.4708**（`refresh=True` 确认），同时 S 4.43→4.45 / F 3.58→3.67 / 2Y 4.10→4.15 / Score 0.0219→**0.0237**。但与 `2rAOGKow` 互测 **0.788** ⇒ **同席替代升级**，不是新增独立席位；IND 队列 Day5 换颗。

### 1.2 优先队列（收入序，双闸终验后定稿）

> 排序判据沿用 11-05：**`Score = 2Y × F × margin × D1均值`**（仅序数代理；OS 表现不可预览）。收入序 ≠ 提交序。
> SUPER 配额 **账号级 1/ET 日（跨区共享）**；被 prod 闸拦下不消耗配额。

| 序 | Alpha ID | Region/Universe | S | F | 2Y | TO | margin | D1 | **Score** | self | **prod（本轮终验）** | 余量 | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ⭐**1** | **`88RNX7la`** | KOR/TOP600 | 4.45 | **5.28** | 3.91 | 0.135 | **0.002819** | 1.39 | **0.0809** | 0.5855 | **0.5856** ✓ | **0.114** | ✅ 可交付·Day1 |
| ⭐**2** | **`Xg9WNRg8`** | USA/TOP2000 | 4.74 | 4.10 | **5.46** | 0.166 | 0.001498 | 1.16 | 0.0389 | 0.6493 | 0.6493（16.6h 缓存） | 0.051 | ✅ Day2 |
| ⭐**3** | **`e75avmq6`** | USA/TOP2000 | 4.29 | 4.00 | 3.94 | **0.103** | 0.002103 | 1.16 | 0.0384 | **0.4871** | **0.6373** ✓ | **0.063** | ✅ 可交付·Day3 |
| 4 | `xAr1YZQb` | EUR/TOPCS1600 | 4.32 | 3.97 | 4.07 | 0.149 | 0.001694 | 1.20 | 0.0329 | 0.6007 | 0.6007 | 0.099 | EUR 唯一席 |
| ⭐**5** | **`3qoG6nEe`** | IND/TOP500 | 4.45 | **3.67** | **4.15** | 0.266 | **0.001364** | 1.14 | **0.0237** | **0.4714** | **0.4708** ✓ | **0.229** | 本轮替换升级·Day5 |
| — | ~~`2rAOGKow`~~ | IND/TOP500 | 4.43 | 3.58 | 4.10 | 0.277 | 0.001307 | 1.14 | 0.0219 | 0.6101 | 0.6097 | 0.090 | **被 #5 替代**（互测 0.788） |
| 6 | `P0oM2P8L` | DEU/TOP500 | 2.40 | 1.92 | 4.07 | 0.152 | 0.001279 | **1.62** | 0.0162 | 0.5526 | 0.5522 | 0.148 | 倍率第 1 |
| 7 | `xAr1Y5gg` | USA/TOP1000 | 2.80 | 2.05 | 2.98 | 0.146 | 0.001077 | 1.16 | 0.0076 | **0.3295** | 0.4777 | **0.222** | prod 最安全 |
| — | `88RNY77v` | USA/TOP1000 | 2.75 | 1.76 | — | 0.195 | — | 1.16 | — | 0.6647 | **0.6647** ✓ | 0.035 | ⚠ 余量薄且被 `xAr1Y5gg` 支配 |
| — | `GrWdQNq0` | GLB/TOP3000 | 3.51 | 1.58 | 2.43 | 0.286 | 0.000403 | 1.19 | 0.0018 | 0.5135 | 0.5864 | 0.114 | ❌ 建议剔除 |
| ✅ | `1YNjX03W` | USA/TOP3000 | 4.57 | 4.44 | 4.23 | 0.072 | 0.00328 | 1.16 | 0.0714 | 0.5632 | 0.6821 | — | 11-05 ACTIVE |

**互测（本地 `compute_mutual_correlation`，不占 prod 槽，本轮 9 颗 NxN）**：最大独立子集 **5 颗** = `88RNX7la`(KOR) + **`3qoG6nEe`**(IND) + `xAr1Y5gg`(USA/TOP1000) + `e75avmq6` + `Xg9WNRg8`(USA/TOP2000)，两两全 <0.7（详见 §10.2）。
USA 内部 0.268–0.818；跨区 KOR/IND ↔ USA 仅 −0.05~0.07 ⇒ **USA 是唯一能连续供颗的 region，KOR / IND 各可再供 1 颗**。
⚠ 同席对：`3qoG6nEe`↔`2rAOGKow` 0.788｜`omEPzg3m`↔`xAr1Y5gg` 0.818｜`0mYGQo1q`↔`9qxVG66r` 1.0000。

### 1.3 实际可提交队列（去同席后）

| 天序 | Alpha | Region | 理由 | 风险 |
|---|---|---|---|---|
| Day 1 | `88RNX7la` | KOR | Score 0.0809 全场第 1，F 5.28 最高；prod 余量最厚 | 与 `9qxVG66r` 同席（0.9158），二选一 |
| Day 2 | `Xg9WNRg8` | USA/TOP2000 | 2Y 5.46 全表最高 | prod 台账 16.6h，提交前按纪律再 refresh |
| Day 3 | `e75avmq6` | USA/TOP2000 | TO 0.103、margin 0.002103，费后强 | 与 Day2 互测 0.482 ⇒ 可共存 |
| Day 4 | `xAr1YZQb` | EUR | EUR 唯一席 | prod 0.6007 |
| Day 5 | **`3qoG6nEe`** | IND | `dataset_count==1` 分档；prod 余量 **0.229** 全场最厚、Score 0.0237 | TO 0.266、D1 倍率最低；与 `2rAOGKow` 同席（0.788），二选一 |
| Day 6 | `P0oM2P8L` | DEU | D1 1.62 最高 | S/F 偏低 |
| Day 7 | `xAr1Y5gg` | USA/TOP1000 | prod 0.4777 最安全 | 收入序倒数 |

---

## 二、数据基线（06:32 重刷，与 02:05 逐位一致）

### 2.1 组件池 eligibility（ACTIVE 已提交 REGULAR，region 级）

| Region | ACTIVE 组件 | 未提交 IS | 可建性 | vs 02:05 |
|---|---|---|---|---|
| USA | **47** | 27 | GO | 持平 |
| IND | **47** | 0 | GO | 持平 |
| KOR | **30** | 36 | GO | 持平 |
| GBR | **24** | 522 | GO | 持平 |
| EUR | **22** | 100 | GO | 持平 |
| MEA | 19 | 0 | **BLOCKED（平台关闭）** | 持平 |
| GLB | **18** | 0 | GO | 持平 |
| DEU | **13** | 0 | GO | 持平 |
| ASI | 9 | 0 | **BLOCKED（差 1 颗）** | 持平 |
| HKG | 7 | 12 | **BLOCKED（差 3 颗）** | 持平 |

> 双源交叉：MCP `get_user_alphas(stage=OS,type=REGULAR,status=ACTIVE)` 三页去重 **236 颗** = 上表 region 合计。
> 口径：组件池按 **region 级**（非 universe 级）；GLB/TOP3000、USA/TOP1000 的 REGULAR 计数为 0 但 `selectionLimit≥10` 仍能建 SA。
> **ASI 解锁成本最低**：9/10，点名提交 1 颗 RA 即解锁；HKG 需 3 颗。MEA 不在 `get_platform_setting_options` 合法组合内。
> 4.5 小时内组件池无变化 ⇒ 用户未在 02:05–06:32 提交新 RA。

### 2.2 档位占用分类（47 颗 ACTIVE SUPER / 16 个已占档）

| 档位 | REGULAR | SUPER | 分类 | 已用中性化族 |
|---|---|---|---|---|
| USA/TOP3000 | 38 | **6** | 双占用（最饱和） | FAST10 / STAT30 / SUBIND10 / MARKET1000 / SLOW10 ×2 |
| USA/TOP2000 | 5 | 1 | 双占用 | STAT15 |
| USA/TOP1000 / TOP500 / TOPSP500 | 0 | 各 1 | 仅 SA 占用 | STAT15 / CROWDING10 / STAT38 |
| USA/ILLIQUID_MINVOL1M | 4 | 0 | 非平台 options | 不可新建 |
| IND/TOP500 | 47 | **11** | 双占用 | STAT×6 / SUBIND×3 / INDUSTRY / R&M |
| KOR/TOP600 | 30 | **10** | 双占用 | STAT×6 / SUBIND×2 / CROWDING / R&M |
| GBR/TOP700 | 24 | 5 | 双占用 | STAT×2 / SLOW / FAST / R&M |
| GLB/MINVOL1M 2、TOPDIV3000 1、MINVOL10M 1、TOP3000 1 | 17/1/0/0 | 各 1–2 | 双占用/仅 SA | STAT / SUBIND / SLOW / R&M |
| EUR/TOP2500 2、TOPCS1600 1 | 13 / 9 | 各 1–2 | 双占用 | STAT10 / CROWDING10 / STAT10 |
| DEU/TOP500 | 13 | 1 | 双占用 | STAT10 |
| MEA/TOP400 | 19 | 2 | 平台关闭 | SUBIND×2 |

- **零 OS 档**：`USA/TOP200`、`EUR/TOP1200/800/400`、`CHN/TOP2000U`、`AMR/TOP600`。
  EUR 三档 10-31/11-03 实测 prod 0.7117–0.7783 **结构性撞墙**，非本轮新发现。
- **仅零 SA 占用档**：`ASI/MINVOL1M`(6)、`ASI/MINVOL10M`(3)、`HKG/TOP800`(7) —— 组件池 <10，硬下限卡死。
- ⚠ **「零 OS 档 ⇒ self 恒 0」已证伪**：self 池按 region 聚合，USA/TOP1000 的 REGULAR 计数为 0 但 `A1V0L9KQ` self 仍 0.6331。
- 最近提交仍为 `1YNjX03W`（2026-11-04 20:27 ET）⇒ **02:05 之后无新 SUPER 提交**。

### 2.3 Pyramid 倍率（本轮 MCP 复核）

| Region | D1 均值 | 最高类别 | 最低类别 |
|---|---|---|---|
| DEU | **1.62** | model/news/other/analyst/fundamental 1.8 | imbalance 1.2 |
| CHN | 1.61 | other 1.9 | socialmedia 1.1 |
| AMR | 1.55 | sentiment 1.7 | pv 1.4 |
| GBR | **1.41** | sentiment 1.7 | imbalance 1.0 |
| HKG | 1.41 | analyst/model/other 1.7 | imbalance 1.0 |
| KOR | **1.39** | analyst/fundamental/model/news/sentiment/other 1.6 | imbalance 1.0 |
| EUR | 1.20 | other 1.5 | risk/imbalance 1.0 |
| GLB | 1.19 | fundamental/analyst/sentiment 1.4 | pv/risk 1.0 |
| ASI | 1.18 | analyst 1.5 | imbalance/macro 1.0 |
| USA | **1.16** | other/sentiment 1.4 | institutions/imbalance 1.0 |
| IND | 1.14 | analyst 1.4 | risk/institutions 1.0 |

> 倍率决定塔位分不决定可行性：**DEU 倍率最高但池最小；USA/IND 倍率最低但池最大**。KOR 1.39 是 `88RNX7la` 登顶收入序的关键乘数。MEA 已不在倍率表。

### 2.4 双闸实测（本轮 `refresh=True` 权威值）

| Alpha | self | prod | 余量 | 判定 |
|---|---|---|---|---|
| **`88RNX7la`** | 0.5855 | **0.5856** | 0.1144 | ✅ 双过，self≈prod |
| **`e75avmq6`** | **0.4871** | **0.6373** | 0.0627 | ✅ 双过，**self 与 prod 分离 0.15** |
| **`88RNY77v`** | 0.6647 | **0.6647** | 0.0353 | ✅ 薄过，被支配 |
| `9qxVG66r` | 0.6370 | 0.6370（凌晨 refresh） | 0.0630 | ✅ 被 #1 替代 |
| `Xg9WNRg8` | 0.6493 | 0.6493（缓存 16.6h <48h） | 0.0507 | ✅ |
| **`3qoG6nEe`**（v2 新增） | **0.4714** | **0.4708** ✓ `refresh=True` | **0.229** | ✅ 本轮最厚余量 |
| `YP1lkK0A`（v2 新增） | **0.1576** | **0.7109** ✗ `refresh=True` | — | ❌ **低 self 但 prod 撞墙** |
| `xAr1YZQb` / `2rAOGKow` / `P0oM2P8L` / `xAr1Y5gg` / `GrWdQNq0` | 见 §1.2 | 台账 <48h | — | ✅ |

> ⚠ **prod 账号级单并发**：本轮 `e75avmq6` 首试返回 `correlation_busy`（并行会话占槽），隔一次调用即成功。⇒ 遇 busy **不要重派**，隔时重查即可。
> ⚠ 台账 prod >48h 作废，交付前必 `refresh=True`。

---

## 三、选点原则

1. **档位占用类型 > 组件池大小**；「仅 SA 占用」档在 self 上无豁免（region 级池）。
2. **指标 = 约束优化**：`max S ∧ max F  s.t. self<0.7 ∧ prod<0.7`，优选 `prod<0.6 ∧ TO<0.30`。余量 ≥0.02 才算安全；`prod≥0.7` 无豁免。
3. **★★ 席位由「选中的组件集合」决定，集合由 selection 权重的排序决定**：
   - **单调变换**（幂次 / sqrt / log / 线性缩放 / 常数乘子）⇒ 排序不变 ⇒ **不换席**；
   - **非单调**（硬过滤 `turnover<x`、`if_else` 分档、`in(集合字段, …)` 软偏好、字段偏好阶跃）⇒ 排序改变 ⇒ **可能换席**；
   - 换 universe / 扩池 ⇒ 组件覆盖变化 ⇒ 换席。
4. **★ 新增判据：字段必须「有方差」才能开席**。`author_*`（作者级）、`category`（自有池默认 NONE）、`favorite` 这类在自有池恒为常数的字段，只能做常数缩放，不换席。**优先用平台自动打标的 `datacategories` / `datasets` / `datafields` / `dataset_count`**。
5. **combo 层整形不换席**：cp 幂次 / `reduce_*` / `rank(w)` 历史全部 self>0.9，只当 IS/prod 微调旋钮。
6. **组件数↑ ⇒ self↑ 且 prod↑**：l10 是唯一甜点；l12 多次打穿 2Y 或推高 prod，GLB l12 是死档。
7. **S 与 2Y 负相关；收入序优先看 2Y / margin / F / D1 倍率**，不看裸 S。

---

## 四、论坛指标标准（2026-10-22 定稿，本轮沿用并实测校验）

### 4.1 组成数量（Selection Limit）
- **平台硬下限 = 10**（<10 直接 400 `Ensure this value is greater than or equal to 10`）；官方《Selection Expression》确认「required min value … is 10」。
- 论坛 78 赞帖建议 **30–100 起测、≤500**；LY43440 实测 IND 取 300。
- **实际生效数 = min(limit, 组件池)**；池是 region 级。
- **本账户实测 l10 双闸综合最优**；凌晨保留 l30 作对照（`gJea0x5J` S6.31/F6.64 但 self 0.7025 越线）。

### 4.2 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.6** |
| C 比赛/优秀档 | **5.6–7.0** | **5.6–8.9**（冲 >10） | 0.20–0.27 | <0.5 |

凌晨 C 档候选 `mLoa7lbE`(S6.18/F6.33)、`O0AWVrzd`(S6.37/F7.04) 均 self 0.7838 / 0.9999 同席 ⇒ **指标达 C 档 ≠ 可交付，席位先于指标**。
本轮 `88RNX7la` TO 0.135 / prod 0.5856 落 B 档；`e75avmq6` TO 0.103 / prod 0.6373 落 A 档（prod 未达 B）。

### 4.3 组件筛选阈值（论坛 §0.3）
`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。

> **本账户 3 条不可用根因（本轮官方文档坐实）**：
> ① `author_*` 是**作者级聚合属性**（`author_fitness` = 作者平均 fitness 等），同一作者全部 alpha **恒为同一值** ⇒ 无方差，只能整体缩放，不换席；加严则触发 `At least 10 component alphas are required`。
> ② `prod_correlation` 作排序量是毁灭性负杠杆（S 1.77→1.04），必须留在 `self_correlation`。
> ③ `TO<0.10` 只在 USA/TOP3000 成立，IND(47)/KOR(30)/GLB(18) 组件全部 <10。
> ⇒ 本账户只保留 **turnover 一类硬约束 + 非单调字段分档**。

### 4.4 中性化族规律
- 社区 Fitness 排序（IND）：CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3；选族规则 `TO<0.10 → SLOW`、`TO>0.20 → FAST`。
- 区域族基线：GLB/USA/DEU/EUR 走 STATISTICAL + decay 1；KOR/IND/GBR 走 SECTOR/SUBINDUSTRY + decay 15（须逐区验证）。
- **本账户实测反例**：IND CROWDING 撞墙（0.7255）、**SLOW 才是 IND 真解**；GBR/KOR SLOW 跑赢 CROWDING；GLB/MINVOL10M 甚至 **SLOW(0.560) < STAT(0.639) < CROWDING(0.698) < INDUSTRY(0.748)**。
- **换族是 prod 杠杆不是席杠杆**：同一 selection 下换族，日收益相关 0.70–0.93。

### 4.5 其他实证
- truncation 0.02 vs 0.08 对 SA 几乎无差异；本轮全用 0.02。
- 论坛推荐 `Selection Handling = Non-Zero`；本账户 47 颗 SA 全用 **POSITIVE** 均成功。官方提醒：若表达式含负值，须切 Non-Zero / Non-NaN。
- **decay 在 SA 组合层完全无效**（d0 与 d1 逐字相同）；`componentActivation=OS` 在本账户无产出（组件 OS 起点 2024-01-01 落在仿真窗口 2014–2023 之外）。
- **官方 operator limit = 8000**：组合内所有组件算子总数超限会自动截断组件数（只 WARNING 不报错）⇒ 用 `operator_count` 做分档还有「避免截断」的工程价值。

---

## 五、分 Region 方案

### 5.1 总表（最优配方 + 双闸实测 + 余量）

| Region | 池 | 最优配方 | Alpha ID | S | F | 2Y | TO | self | prod | 余量 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **KOR** | 30 | TOP600 SLOW l10 cp7 + `if_else(operator_count>=5,…)` | **`88RNX7la`** | 4.45 | **5.28** | 3.91 | 0.135 | 0.5855 | **0.5856** | **0.114** | ⭐ 收入序 #1，B 档 |
| **USA** | 47 | TOP2000 SLOW l10 cp3（DEF） | `Xg9WNRg8` | 4.74 | 4.10 | **5.46** | 0.166 | 0.6493 | 0.6493 | 0.051 | ✅ A |
| USA 2nd | — | TOP2000 SLOW l10 cp3 + `if_else`/`operator_count` | **`e75avmq6`** | 4.29 | 4.00 | 3.94 | **0.103** | **0.4871** | **0.6373** | **0.063** | ⭐ 与 ↑ 互测 0.482 |
| USA 3rd | — | TOP1000 SLOW l10 cp3 + `TO<0.22` | `xAr1Y5gg` | 2.80 | 2.05 | 2.98 | 0.146 | **0.3295** | **0.4777** | **0.222** | ✅ B 档最安全 |
| **DEU** | 13 | TOP500 SLOW l10 cp3 + `TO<0.22` | `P0oM2P8L` | 2.40 | 1.92 | 4.07 | 0.152 | 0.5526 | **0.5522** | 0.148 | ✅ B 档 |
| **IND** | 47 | TOP500 SLOW l10 cp3 + `dataset_count==1` 分档 | **`3qoG6nEe`** | 4.45 | **3.67** | 4.15 | 0.266 | **0.4714** | **0.4708** | **0.229** | ⭐ 本轮替换升级 |
| **EUR** | 22 | TOPCS1600 FAST l10 cp1 + `TO<0.22` | `xAr1YZQb` | 4.32 | 3.97 | 4.07 | 0.149 | 0.6007 | 0.6007 | 0.099 | ✅ B 边界 |
| **GLB** | 18 | TOP3000 SLOW l15 cp3（DEF） | `GrWdQNq0` | 3.51 | 1.58 | 2.43 | 0.286 | 0.5135 | 0.5864 | 0.114 | ⚠ 建议剔除 |
| **GBR / MEA / ASI / HKG** | — | 无新增席 | — | — | — | — | — | — | — | — | ❌ 停投 |

### 5.2 KOR（池 30，10 颗 SUPER 已占）—— 收入序第 1

| 配方 | ID | S | F | 2Y | margin | self / prod | 判定 |
|---|---|---|---|---|---|---|---|
| SLOW l10 cp7 + `if_else(operator_count>=5, …)` | **`88RNX7la`** | **4.45** | **5.28** | 3.91 | **0.002819** | 0.5855 / **0.5856** | ⭐ 全 IS 闸 PASS |
| SLOW l10 cp7（DEF，11-04） | `9qxVG66r` | 3.95 | 4.55 | 3.09 | 0.002652 | 0.6370 / 0.6370 | 被替代（互测 0.9158） |
| SLOW l10 cp7 + `TO<0.22` | `Xg9RblQb` | 3.95 | 4.55 | 3.09 | — | 0.6370 | ❌ 逐位相同（KOR 全员低 TO） |

> KOR 已 10 颗 SUPER 仍能靠非单调 selection 挤出更强席 ⇒ **瓶颈不是池深，是 selection 的非单调性**。

### 5.3 USA（池 47，10 颗 SUPER 已占）—— 唯一能连续供颗

| 配方 | ID | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| TOP2000 SLOW l10 cp3 + `if_else`/`operator_count` | **`e75avmq6`** | 4.29 | 4.00 | **0.103** | **0.4871** | **0.6373** | ⭐ 新席 |
| TOP2000 SLOW l10 cp3（DEF） | `Xg9WNRg8` | 4.74 | 4.10 | 0.166 | 0.6493 | 0.6493 | ✅ 2Y 5.46 |
| TOP3000 SLOW l10 cp3 + `signed_power(1-self,2)` | `mLoa7lbE` | 6.18 | 6.33 | 0.156 | 0.7838 | — | ❌ 逐位复现 `vR1kAQmr` |
| TOP3000 SLOW l10 cp3 + `category`/`neutralization` | `O0AWVrzd` | 6.37 | 7.04 | 0.118 | 0.9999 | — | ❌ 常数缩放，同席 |
| TOP1000 SLOW l10 cp3 + `abs(long-short)<=100` + `log` | `88RNY77v` | 2.75 | 1.76 | 0.195 | 0.6647 | 0.6647 | ⚠ 新席但被支配 |
| TOP3000 SLOW l10 cp1 + `combo_a(alpha,250,"algo1")` | — | — | — | — | — | — | ❌ `Invalid number of inputs: 3, should be exactly 1`（见 §9.4） |

> **USA 可作 2 个独立 TOP2000 席**：`e75avmq6` ↔ `Xg9WNRg8` = **0.482**；再加 TOP1000 的 `xAr1Y5gg` ⇒ **单区可连供 3 天**。
> `TO<0.22` 不跨 universe 外推（TOP3000 降 prod、TOP2000 反升）⇒ 每换 universe 必重测。

### 5.4 IND / EUR / DEU / GLB

- **IND（本轮升级）**：**`3qoG6nEe`** = SLOW l10 cp3 + `if_else(dataset_count == 1, 2, 1) * (1 - self_correlation)`，S4.45/F3.67/2Y4.15/TO0.266，self **0.4714** / prod **0.4708**（refresh 确认）、`failed_ra=0`、Score **0.0237**。
  对照旧席 `2rAOGKow`（4.43/3.58/4.10、self 0.6101 / prod 0.6097）：**双闸各降 ~0.14 而 S/F/2Y 全升**，是严格支配。
  ⚠ 两者互测 **0.788 ≥0.7** ⇒ **同席，只能二选一**；`vR1OrVb3`（`TO<0.22`，prod 0.5170）亦同席。D1 1.14 全区最低 ⇒ Day 5。
- **EUR**：`xAr1YZQb` 唯一席（S4.32/F3.97/2Y4.07，prod 0.6007）。本轮 v1 补测 **`O0AWggov`**（TOPCS1600 FAST l10 cp1 + combo `winsorize(w, std=2)`）：S **4.78** / F 3.90 / TO 0.2071 / self 0.5803，IS 全闸 PASS，但 ↔ `xAr1YZQb` 互测 **0.9206** ⇒ **combo 层算子只改 IS/TO、不换席**，且 TO 升破 0.20 ⇒ EUR 仍只出 1 颗。三颗候选互测 0.7366–0.9655。三个零 OS 空档 prod 0.7117–0.7783 结构性撞墙。
- **DEU**：池 11→13 使 prod 0.6923→0.5522（`P0oM2P8L`），2Y 4.07、D1 1.62 全场最高 ⇒ 池深是 DEU 天花板。
- **GLB**：`GrWdQNq0` margin 0.000403 / F 1.58 全表最差 ⇒ 剔除。备选 `0mYpnMr1`（prod 0.5010）同席（0.9551）。**l12 是死档**（2Y 1.14）。

### 5.5 GBR / MEA / ASI / HKG

| Region | 状态 | 依据 |
|---|---|---|
| GBR | **停投** | 唯一 universe TOP700，SLOW 已占（`QPvGdLYQ` ACTIVE），CROWDING 0.7486 撞墙 |
| MEA | **平台关闭** | options 18 个合法组合无 MEA；新建 400；倍率表亦无 MEA |
| ASI | 组件 9/10 | 差 1 颗 RA（解锁成本最低） |
| HKG | 组件 7/10 | 差 3 颗 RA |

---

## 六、停投区

| Region / 档 | 理由 | 依据 |
|---|---|---|
| **MEA** | 平台关闭 | options 复核无该区；11-04 四档全 400 |
| **GBR** | 新增席 = 0 | CROWDING+`TO<0.22` 0.7486 与已提交同席 |
| **EUR 三零档** | prod 墙结构性 | TOP1200 0.7117 / TOP800 0.7783 / TOP400 0.7783 |
| **ASI / HKG** | 组件 9 / 7 < 10 | 平台硬下限 |
| **CHN / AMR** | 账户零组件 | 无 REGULAR 持仓 |
| **USA/TOP3000** | 6 颗 SUPER，2 颗 SLOW 已 ACTIVE | 本轮 2 档新 selection 全部 self>0.78 同席 |
| **USA/TOP200 / TOPSP500 / TOP500** | 历史判死 | S 不可达 / Ladder FAIL / 已封档 |
| **IND / KOR / EUR / DEU** | 已有席饱和，每区仅剩 1 席 | 见 §5 |

---

## 七、撞墙档案（勿重复投入）

### 7.1 同席墙
| 组合 | 相关 | 判定 |
|---|---|---|
| `mLoa7lbE`(USA w²) ↔ `vR1kAQmr`(DEF) | 指标逐位相同 | 单调权重整形不换席 |
| `akKaGYKv`(IND w²) ↔ `2rAOGKow`(DEF) | 指标逐位相同 | 跨区复现 |
| `O0AWVrzd`(category/neutralization) ↔ 已提交 SLOW | self 0.9999 | 自有池常数缩放 |
| `88RNX7la` ↔ `9qxVG66r` | 0.9158 | 取前者 |
| `9qxVG66r` ↔ `Xg9RblQb` | 1.0000 | KOR `turnover` 过滤非约束 |
| `e7569r26` ↔ `A1V0eZne` | 1.0000 | `TO<0.18` 与 `TO<0.22` 同子集 |
| `omEo6o5J` ↔ `A1V0eZne` | 0.9938 | `reduce_avg` 不换席 |
| `2rAOGKow` ↔ `vR1OrVb3` | 0.7245 | IND 同席 |
| `GrWdQNq0` ↔ `0mYpnMr1` | 0.9551 | GLB 换 limit 不换席 |

### 7.2 prod 墙（≥0.7）
`qMLEWjrP` USA/TOP3000 CROWDING 0.7708｜`YP1x5lzA` USA/TOP2000 `TO<0.22` 0.7077｜`pwdvRn8X` GBR CROWDING 0.7486｜`vR1kAQmr` 0.7838｜`mLovnvXx` 0.8418｜EUR 三零档 0.7117/0.7783/0.7783｜GLB/MINVOL10M MARKET 0.762｜DEU `QPv3Ww9p` 0.6923（擦线）

### 7.3 IS 闸墙
`YP1xbMKw` GLB l12 → IS_LADDER 1.14/1.58｜`omE6ad7E` EUR SLOW → 1.50/1.58｜`MPY1gw08` USA/TOP500 → S1.48 + F0.74｜`gJea0x5J` USA l30 → self 0.7025

### 7.4 组件不足墙（`At least 10 component alphas are required`）
USA `author_fitness≥2`｜IND/KOR/GLB `TO<0.10`｜USA/TOP500 `d0`（池是 (region, delay) 双键）

### 7.5 负向判据（累计）
- **selection 权重单调变换**（`signed_power(w,2)` / `sqrt` / `log` / `power`）⇒ 不换席，禁止再扫。
- **自有池常数字段**（`author_*` / `category` / `favorite`）⇒ 只能缩放，不换席；字符串 `equal/not_equal` 本身语法合法。
- **`reduce_*` 全家** ⇒ 不换席，只当 IS/prod 微调（±0.03）。
- **`combo_a(alpha, 250, "algo1")`** ⇒ 硬错 `Invalid number of inputs: 3, should be exactly 1`；修正写法 `combo_a(alpha)` 本轮 v2 实测中。
- **`componentActivation=OS`** ⇒ 全零，别再试。

### 7.6 本轮 v2 新增撞墙（勿重复）
| 配方 | ID | 卡点 |
|---|---|---|
| USA/TOP2000 `in(datacategories,"analyst")` | `YP1lkK0A` | **prod 0.7109 ✗**（refresh 复核一致）；虽 self 0.1576 全表最低 |
| KOR/TOP600 `in(datacategories,"news")` | `0mYGQo1q` | 与 `9qxVG66r` **互测 1.0000** ⇒ 字段在 KOR 池恒常数、不换席 |
| USA/TOP1000 `universe_size>=2000` | `omEPzg3m` | 与 `xAr1Y5gg` **互测 0.818** ⇒ 同席且 prod 更差（0.6283 vs 0.4777） |
| USA/TOP3000 `ts_ir(stats.returns,250)` | `gJerPe7e` | `LOW_SUB_UNIVERSE_SHARPE` 2.15 < 2.26 + prod 0.699 贴线 |
| USA/TOP3000 `combo_a(alpha)` | `VkxMlzgG` | `LOW_SUB_UNIVERSE_SHARPE` FAIL + self 0.6994 / prod 0.6996 双贴线 |
- **`combo_a` 语法修正成功**：凌晨 `combo_a(alpha, 250, "algo1")` 报 `Invalid number of inputs: 3, should be exactly 1`；单输入 `combo_a(alpha)` 可建成，但指标不可用。
- **sa_run verdict 标签 bug**：有 IS `fails` 时仍标 `BLOCKED-CORR`（应为 `BLOCKED-IS`）⇒ 读结果必须看 `fails` 字段，不能只看 verdict。

---

## 八、执行清单

### 8.1 构建命令（可复现）

```bash
cd D:/coding/traeCN_project/wqb
# 1. 清 7 天 user_alphas 缓存（本轮清 60 条，不清会漏当日提交）
world-quant-brain-mcp/.venv/Scripts/python.exe -c "
import sqlite3; c=sqlite3.connect('data/wqb.db')
c.execute(\"delete from api_cache where cache_key like 'user_alphas%'\"); c.commit(); c.close()"
# 2. 全量池盘点（--json 必须用绝对路径，相对路径有 results/results 拼接 bug）
world-quant-brain-mcp/.venv/Scripts/python.exe -u tools/probe/probe_sa_candidates.py --refresh \
  --json "D:/coding/traeCN_project/wqb/results/sa_plan_20261106.json"
# 3. 本轮 6 档（后台，日志重定向，勿用管道）
world-quant-brain-mcp/.venv/Scripts/python.exe -u C:/Users/MENGTAO/wqb-scripts/sa_run.py \
  --configs results/sa_scan_20261106/configs_v2.json \
  --out results/sa_scan_20261106/res_v2.jsonl > results/sa_scan_20261106/run_v2.log 2>&1
# 4. 双闸终验（MCP，禁写临时脚本）
# check_correlation(alpha_id=<ID>, correlation_type="production", refresh=True)
```

**v1 配方原文（凌晨 9 档，已落盘 8 + 1 档 combo_a 报错）**见 `configs_v1.json`；核心：
```
DEF   = (1 + 0 * (prod_correlation > 0)) * (1 - self_correlation)
POW2  = (1 + 0 * (prod_correlation > 0)) * signed_power((1 - self_correlation), 2)
IFOP  = if_else(operator_count >= 5, (1 - self_correlation) * (1 + 0.5 * (turnover < 0.2)),
                0.1 * sqrt(1 + self_correlation))
combo = stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500);
        ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic);
        w = 1 - maxCorr; {w | winsorize(w,std=2) | combo_a(alpha,250,"algo1")}
settings = delay1 / decay1 / truncation 0.02 / POSITIVE / componentActivation IS / maxTrade OFF
```

**v2 配方（本轮 6 档，官方语法）**见 `configs_v2.json`：
```
in() 软偏好   = (1 - self_correlation) * (1 + 2 * in(datacategories, "analyst"|"news"))
dataset_count = if_else(dataset_count == 1, 2, 1) * (1 - self_correlation)
universe_size = (1 - self_correlation) * (1 + 0.5 * (universe_size(universe) >= 2000))
combo ts_ir   = stats = generate_stats(alpha); ts_ir(stats.returns, 250)
combo_a 修正  = combo_a(alpha)
```
> 全部用**软偏好乘法**而非硬过滤，保证 POSITIVE 下组件数 ≥10（硬过滤 `in()` 会触发组件不足墙）。

### 8.2 配额与并发约束

| 项 | 限制 | 影响 |
|---|---|---|
| SUPER 提交 | **账号级 1/ET 日（跨区共享）** | 7 颗队列 = 7 天 |
| REGULAR 提交 | 4/天/区（与 SUPER 独立） | 解锁 ASI(+1) / HKG(+3) 不受影响 |
| prod 相关性 | **账号级单并发** | 本轮实测 `correlation_busy`；终验必须排在批次结束后，遇 busy 隔时重查不重派 |
| 仿真并发 | 平台限流 | `sa_run.py` 内置 90×10s 轮询；单档 4–8 分钟 |
| 组合算子总数 | **8000** | 超限自动截断组件数（WARNING）⇒ `operator_count` 分档有工程价值 |

### 8.3 建议执行顺序
1. **先停后台 `sa_run.py` 批次**，再逐颗 `check_correlation(..., refresh=True)` 做提交前终验（本轮已完成 3 颗）。
2. 按 §1.3 收入序提交；被 prod 闸拦下不消耗配额，直接降级。
3. 每颗提交后等满 flip 窗 ~250s，`tools/super_build.py status --alpha-id <id>` 确认 `status=ACTIVE`，**不只看 POST 回执**。
4. 提交后 osmosis 点数需另行分配（新 SA 默认 0 点；每 scope 恰好 100,000 点，周锁 + 7 天生效）。

### 8.4 提交命令（**仅用户点名后**）
```bash
cd D:/coding/traeCN_project/wqb
WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py submit --alpha-id <ID> --region <REGION>
```
内置 prod 闸 0.7 fail-closed，无豁免参数。本轮**未执行**。

---

## 九、平台组 SA 算子全覆盖审计（用户强调项，本轮重做）

### 9.1 三个权威来源（凌晨只用了 1 个，结论偏差）

| 来源 | 内容 | 数量 |
|---|---|---|
| A. MCP `get_operators` | REGULAR 表达式算子全集（带 `scope`: COMBO/SELECTION/REGULAR） | **103** |
| B. 官方《SuperAlpha Operators》附录（`appendix-operators`） | **SA 专用可用算子**，按 Selection / Combo 两栏标注 | **≥180**（含 reduce_* 14 个合并为 1 行） |
| C. 官方《Selection Expression》 | alpha 属性 **26 个** + `author_*` 属性 **19 个** + 5 条官方示例表达式 | 45 字段 |

> **★ 更正凌晨结论**：103 个不是「平台 SA 算子全部」，只是 `get_operators` 返回的 REGULAR 全集。
> 官方附录里 SELECTION 栏标 x 的 **41 个**（`abs/add/and/arc_cos/arc_sin/arc_tan/ceiling/clamp/divide/equal/exp/floor/frac/greater/if_else/inverse/is_finite/is_nan/is_not_finite/is_not_nan/less/log/max/min/multiply/nan_mask/nan_out/negate/not/or/power/purify/reverse/round/s_log_1p/sign/signed_power/sqrt/subtract/tanh/to_nan`）+ `in` + `universe_size` ⇒ **≥43 个**（凌晨只算 27 个）。
> COMBO 栏另有大量 A 未收录算子：`combo_weight`、`ts_ir`、`ts_entropy`、`ts_theilsen`、`ts_weighted_decay`、`ts_partial_corr`、`ts_poly_regression`、`inst_pnl`、`inst_tvr`、`group_vector_neut`、`group_vector_proj`、`regression_neut`、`regression_proj`、`purify`、`sigmoid`、`tanh`、`nan_mask`、`nan_out`、`left_tail`、`right_tail`、`rank_by_side`、`hump_decay`、`jump_decay`、`scale_down`、`truncate`、`unit`、`count`、`convert`、`filter`、`keep`、`one_side`、`position_safeguard`、`replace`、`round_down`、`log_diff`、`is_finite/is_not_finite/is_not_nan`、`arc_*`、`ceiling/floor/frac/round/exp/s_log_1p`… ⇒ **COMBO 可用约 160 个**。

### 9.2 官方 selection 字段全集（凌晨漏 10+ 个）

| 类别 | 字段 |
|---|---|
| 字符串/集合 | `category`、`color`、`dataset`(`datasets`)、`name`、`neutralization`、`tags`、`universe`、`os_start_date`、`datafields`、`datacategories`、`classifications`、`competitions` |
| 数值 | `decay`、`favorite`、`long_count`、`short_count`、`operator_count`、`truncation`、`turnover`、`self_correlation`、`prod_correlation`、`dataset_count`、`datacategory_count`、`datafield_count` |
| 专用算子 | `universe_size(universe)`、`in(集合字段, "值")` |
| 作者级（**恒常数**） | `author_yield_rate`、`author_quarter_yield_rate`、`author_tenure`、`author_activity`、`author_distinct_count_*`(regions/datasetcategory/dataset/datafield/operator)、`author_distinct_quarter_count_*`、`author_prod_correlation`、`author_self_correlation`、`author_sharpe`、`author_turnover`、`author_fitness`、`author_returns_to_drawdown` |

**官方 `in()` 语法（凌晨 guessed 错）**：
`in(datasets, "analyst6")`｜`in(tags, "my_tag")`｜`in(datafields, "returns")`｜`in(datacategories, "fundamental")`｜`in(classifications, "POWER_POOL")`｜`in(competitions, "HCAC2025")`；可组合 `not(in(...))`、`||`。
**官方示例**：`(in(datasets,"analyst6") || color=="RED") * (long_count-short_count)`（Selection Handling = Non-Zero, limit 10）。

### 9.3 本轮利用率（诚实口径）

| 维度 | 可用 | 本轮（v1+v2）用到 | 利用率 |
|---|---|---|---|
| SELECTION 算子 | ≥43 | `add multiply subtract abs log sqrt signed_power greater less equal not_equal less_equal greater_equal if_else` + **`in` `universe_size` `ts_ir`(combo)** ⇒ **15** | **≈35%** |
| COMBO 算子 | ≈160 | `generate_stats self_corr if_else reduce_max winsorize combo_a ts_ir` ⇒ **7** | **≈4%** |
| 合计去重 | ≥180 | **≈21** | **≈12%** |
| selection 字段 | 26 + 19 author | 用到 `self_correlation / prod_correlation(占位) / turnover / operator_count / long_count / short_count / category / neutralization / universe / dataset_count / datacategories` ⇒ **11** | ≈25% |
| 基线（11-05） | — | 10 算子 | ≈6% |

> **利用率低本身不是缺陷**：SA combo 的输入是 (A×D×I) 矩阵、`w` 是 (D×A) 标量权重，绝大多数 group/vector/时序算子语义不适用。
> **真正决定席位的是 SELECTION 层**（本轮覆盖 ≈35%，凌晨 14/27 的口径本身也低估了分母）。
> 本轮反而**证伪**了两类算子：单调整形（`signed_power`/`sqrt`/`log`）与常数字段比较（`category`）。**多用一个算子不产生价值，非单调分档才产生价值。**

### 9.4 未测算子 ROI 排序（下轮）

| 优先级 | 算子/字段 | 判定 |
|---|---|---|
| ⭐⭐⭐ | **`in(datacategories/datasets/datafields, …)` 软偏好** | 唯一能消费集合字段且**有方差**的算子；本轮 v2 已派发 2 档，结果见 §10 |
| ⭐⭐⭐ | `dataset_count` / `datacategory_count` / `datafield_count` 分档 | 区分 ATOM / 多字段 alpha，本轮 v2 已派发 1 档 |
| ⭐⭐ | **`ts_ir(stats.returns, 250)`** | 官方 combo 示例，按近 1 年信息比率加权，历史从未用过；本轮 v2 已派发 |
| ⭐⭐ | **`combo_a(alpha)`** | 修正 `combo_a(alpha,250,"algo1")` 的 3 输入硬错；本轮 v2 已派发 |
| ⭐⭐ | `combo_weight` | COMBO 专用（A 未收录）；语义=返回当前组合权重，可能改变权重结构 |
| ⭐⭐ | `winsorize` / `quantile` / `zscore` / `tail` / `left_tail` / `right_tail` | combo 权重整形；历史 `rank(w)` 撞墙 ⇒ 只动 IS/TO，不换席 |
| ⭐ | `universe_size(universe)` | SELECTION 专用，本轮 v2 已派发 1 档 |
| ⭐ | `classifications` / `competitions` / `favorite` / `name` | 自有池多半恒常数，先验低 |
| — | `author_*` 全套 19 个 | **恒常数，不可消费**，禁止再扫 |
| — | 全部 30+ 个新 `ts_*`、`group_*`、`vector_*` | SA combo 无天然 group/vector 输入；`decay` 在 settings 层已证无效 ⇒ 适用性低 |

### 9.5 结论
**平台 SA 可用算子 ≥180 个（不是 103），本轮实测纳入 ≈21 个（≈12%）**，其中决定席位的 SELECTION 层覆盖 ≈35%。
凌晨的「100% 覆盖」应作废；但结论方向不变：**席位只由「选中组件集合」决定，能改变集合的只有非单调 selection、换 universe、扩池**。算子多样性的价值在于找到更多「有方差的字段」与「非单调分档」，不在于堆数量。

---

## 十、本轮 v2 批次结果（6 档全部完成，06:36–06:52）

> 产物 `configs_v2.json` / `res_v2.jsonl` / `run_v2.log`。全部采用**软偏好乘法**（非硬过滤）保证组件 ≥10。
> prod 为平台首次计算；`3qoG6nEe` 与 `YP1lkK0A` 另做 `refresh=True` 复核，逐位一致。

| # | tag / ID | 区域/档 | 新算子 | S | F | TO | self | prod | IS fails | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `YP1lkK0A` | USA/TOP2000 | `in(datacategories,"analyst")` | 2.32 | 1.59 | 0.1076 | **0.1576** | **0.7109 ✗** | 0 | ❌ prod 墙；**真新席**（self 全表最低） |
| 2 | `0mYGQo1q` | KOR/TOP600 | `in(datacategories,"news")` | 3.95 | 4.55 | 0.1281 | 0.6370 | 0.6370 | 0 | ⚠ 与 `9qxVG66r` **互测 1.0000**，不换席 |
| 3 | **`3qoG6nEe`** | IND/TOP500 | `dataset_count==1` 分档 | **4.45** | **3.67** | 0.2657 | **0.4714** | **0.4708 ✓** | 0 | ⭐ **同席替代升级**（余量 0.229） |
| 4 | `omEPzg3m` | USA/TOP1000 | `universe_size(universe)>=2000` | 2.88 | 2.01 | 0.1774 | 0.6284 | 0.6283 | 0 | ⚠ 与 `xAr1Y5gg` **互测 0.818**，被支配 |
| 5 | `gJerPe7e` | USA/TOP3000 | `ts_ir(stats.returns,250)` combo | 5.23 | 5.02 | 0.1629 | 0.6391 | 0.6990 | **1**（sub 2.15<2.26） | ❌ 相对闸反杀 |
| 6 | `VkxMlzgG` | USA/TOP3000 | `combo_a(alpha)` 修正 | **5.72** | **5.59** | 0.1430 | 0.6994 | 0.6996 | **1**（sub） | ❌ 双闸贴线 + 相对闸 |

### 10.1 五条新增判据

1. **★★★ `in()` 集合字段必须逐区验证「有方差」**：USA 上 `analyst` 有方差 ⇒ 真换席；KOR 上 `news` 恒常数 ⇒ 逐位复现旧席。⇒ 用前先查该区组件池的 `datacategories` 分布，不能跨区照搬。
2. **★★ 「低 self ≠ 可交付」再次坐实**：`YP1lkK0A` self 0.1576（全表最低）却 prod 0.7109（refresh 一致）⇒ 新席可能自带 prod 墙，**两闸必须各自实测**。
3. **★★ `dataset_count==1` 是 IND 的双赢杠杆**（唯一同时降双闸且升 S/F/2Y 的配方），但与旧席互测 0.788 ⇒ 属于「换颗升级」而非「新增独立席位」。
4. **★★ SA 层同样遵守「S↑ 抬高相对闸」**：两颗 combo 换算子把 S 推到 5.23 / 5.72，均触发 `LOW_SUB_UNIVERSE_SHARPE`（limit ≈0.52×S）。⇒ 靠 combo 堆 S 会被 sub 反杀，且 prod 同步贴到 0.699。
5. **`combo_weight` / `universe_size` 结论**：`universe_size` 不换席；`combo_a(alpha)` 单输入语法确认可用（修正凌晨 3 输入硬错），但建成后双闸不可用。

### 10.2 互测矩阵摘要（9 颗，`compute_mutual_correlation`，threshold 0.7，1023 点）

| Pair | 相关 | 结论 |
|---|---|---|
| `0mYGQo1q` ↔ `9qxVG66r` | **1.0000** | KOR 逐位复现 |
| `88RNX7la` ↔ `9qxVG66r` | 0.9158 | KOR 同席，取前者 |
| `omEPzg3m` ↔ `xAr1Y5gg` | **0.818** | USA/TOP1000 同席，取后者 |
| `3qoG6nEe` ↔ `2rAOGKow` | **0.788** | IND 同席，取前者 |
| `Xg9WNRg8` ↔ `e75avmq6` | 0.482 | USA/TOP2000 两独立席 |
| `Xg9WNRg8` ↔ `omEPzg3m` | 0.5771 | 独立 |
| 跨区（KOR/IND ↔ USA） | −0.0505 ~ 0.0741 | 天然低相关 |

**最大互相 <0.7 子集仍为 5 颗**，且可全部换成各席最优版本：
`88RNX7la`(KOR) + `3qoG6nEe`(IND) + `xAr1Y5gg`(USA/TOP1000) + `e75avmq6` + `Xg9WNRg8`(USA/TOP2000)。
⇒ **本轮未新增独立席位，但把 IND 席升级为 prod 余量 0.229 的更优颗**。

### 10.3 下轮 ROI
① 把 `dataset_count` 分档迁移到 **KOR / USA / DEU**（同字段、不同池，先验「有方差」）；② `in(datacategories, …)` 换类别值（USA 用 `model`/`news`/`sentiment`）；③ `ts_ir` / `combo_a` 压 S 修 sub（换 limit/族，而非堆 S）；④ `combo_weight` 语义摸底。**不再扫**：单调整形、`author_*`、硬过滤致组件<10、limit 轴、decay、EUR 全域。

---

## 十一、收入口径（沿用 11-05）

- `Score = 2Y × F × margin × D1均值`（序数代理）；OS 表现不可预览（平台 `os` 段只回 `startDate`）。
- 收入三乘数：OS 表现 × pyramid 倍率 × osmosis 点数；**每 scope（region×delay）恰好 100,000 点**，账户已启用 6 scope = 600,000，周锁 + 7 天生效。
- 昨日 base payment $1.59；日付是账号级合计不拆单颗 ⇒ 新 SUPER 的边际日收入是分级量级。
- **收入第一杠杆是 scope 选择而非 SA 分层**；不要为收入牺牲 RA 主线。

---

## 附录 A：本轮产物索引

| 文件 | 内容 |
|---|---|
| `results/sa_plan_20261106.json` | 组件池 + SUPER 全量（06:32 refresh）；凌晨版备份 `results/sa_scan_20261106/sa_plan_20261106_am_backup.json` |
| `results/sa_scan_20261106/probe_refresh_am.log` | 本轮清缓存+盘点日志 |
| `results/sa_scan_20261106/configs_v1.json` / `res_v1.jsonl*` | 凌晨 9 档配方与 8 颗结果 + combo_a 报错 |
| `results/sa_scan_20261106/configs_v2.json` / `res_v2.jsonl*` / `run_v2.log` | 本轮 6 档官方语法配方与结果 |
| `results/sa_scan_20261106/super_slots.json` / `regular_slots_full.json` / `is_super_inventory.json` | 47 颗 ACTIVE SUPER、236 颗 ACTIVE REGULAR、IS SUPER 库存 |
| `results/sa_scan_20261106/op_audit_full.py` / `.json` | 凌晨 103 算子审计（**口径已更正，见 §9.1**） |
| `output_report/SA_best_per_region_plan_20261106_am.md` | 凌晨 02:05 版备份 |

## 附录 B：本轮相对凌晨版的差异

| 项 | 凌晨 02:05 | 本轮 06:30 | 原因 |
|---|---|---|---|
| 双闸终验 | 3 颗「待终验」 | **全部补齐**（0.5856 / 0.6373 / 0.6647，均 PASS） | `refresh=True` 实测 |
| self≈prod | 「常态」 | **被 `e75avmq6` 反例推翻**（差 0.15） | 两闸不同池，不可互推 |
| 算子总数 | 103，宣称 100% 覆盖 | **≥180**，`get_operators` 只是 REGULAR 全集 | 官方《SuperAlpha Operators》附录 |
| SELECTION 可用 | 27 | **≥43**（官方 41 + `in` + `universe_size`） | 同上 |
| `in()` 语法 | 未验证、猜测 | **官方 6 种用法确认**，v2 已派发 2 档 | 官方《Selection Expression》 |
| `author_*` 判死理由 | 「自有池恒常数」观察 | **根因坐实：作者级聚合属性，同一作者全 alpha 同值** | 官方字段表 |
| `category` 判死理由 | 「字符串比较无效」 | **修正：字段合法但自有池默认 NONE ⇒ 常数缩放** | 官方合法值表 |
| `combo_a` | 「本轮 C1 档实测，见 §10 补录」（§10 空） | **补录 = 硬错 `3 inputs should be exactly 1`**；`combo_a(alpha)` 修正版已派发 | 读取 `res_v1.jsonl.usa_t3000_combo_a.json` |
| 官方示例 combo | 未提 | **`ts_ir(stats.returns,250)` 首次派发** | 官方《Combo Expression》 |
| v2 批次 | 无 | **6 档全部完成**，1 颗升级可交付 | `configs_v2.json` / `res_v2.jsonl` |
| IND 队列 Day5 | `2rAOGKow`（prod 0.6097） | **`3qoG6nEe`（prod 0.4708，余量 0.229）** | `dataset_count==1` 分档换颗升级 |
| `in()` 效果 | 猜测「下轮第一优先」 | **USA 真换席但 prod 0.7109 撞墙；KOR 恒常数逐位复现** | 逐区验证有方差 |
| combo 堆 S | 未测 | **ts_ir / combo_a 把 S 推到 5.23/5.72 均被 `LOW_SUB_UNIVERSE` 反杀** | S↑ 抬高 0.52×S 相对闸 |
| `combo_a` | 「C1 档实测，见 §10」（空） | **3 输入硬错已定位；`combo_a(alpha)` 语法确认可用但双闸贴线** | §7.6 / §10 |

---

## 附录 C：执行记录（用户点名提交）

| 时间 | 动作 | 结果 |
|---|---|---|
| 2026-11-06 08:10 | 用户点名「提交队列第一个」→ `WQB_ALLOW_ALPHA_SUBMIT=1 … tools/super_build.py submit --alpha-id 88RNX7la --region KOR` | prod 闸 **0.5856 < 0.7 过** → POST 201 → **status=ACTIVE / stage=OS**，name `KOR_S_10comp_RNX7la`，全部 IS checks PASS、pending=[] |

- 前置复核：`get_alpha_details` UNSUBMITTED/IS、`failed_ra=0`、`checks.fail=[]`；`check_correlation(refresh=True, both)` prod **0.5856** / self **0.5855**。
- 连带：**KOR/TOP600 封档**，`9qxVG66r` / `0mYGQo1q` 等同席候选作废；ACTIVE SUPER 47→48；**SUPER 配额 1/ET 日已用**，队列下一颗顺延次日。
- 队列顺延：~~Day1 `88RNX7la`~~ 完成 → `Xg9WNRg8`(USA/TOP2000) → `e75avmq6` → `xAr1YZQb`(EUR) → `3qoG6nEe`(IND) → `P0oM2P8L`(DEU) → `xAr1Y5gg`(USA/TOP1000)。

**报告主体配方仍为待执行；仅上表 1 颗由用户点名提交，其余均未提交。**
