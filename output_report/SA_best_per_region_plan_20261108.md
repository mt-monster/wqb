# 各 Region 最优 SuperAlpha 方案

> **[已执行 2026-11-08 11:50]** `vR1oxZA3`（DEU/TOP500 FAST d1 l10）已按用户点名提交，
> `status=ACTIVE`，IS 8 项全 PASS；prod 闸实测 0.5987 < 0.7 过闸（免查 prod = 走缓存值，闸未跳）。
> ⇒ **DEU/TOP500+l10 席位已占**，同席 `0mYak1nv` / `bl6K2Oor` 作废；下轮 DEU 产能须换 universe 或换 limit。（2026-11-08）

> 执行时刻：2026-11-08 06:30–07:40（GMT+8）｜工作区 `D:\coding\traeCN_project\wqb`
> 铁律：**只挖不提交**。本文全部为待执行配方，提交权归用户；`ALLOW_ALPHA_SUBMIT=False` 闸锁保持。
> 数据时点：组件池 / 档位 / pyramid 全部本轮平台实测（2026-11-08T06:31 刷新，已先清 `api_cache.user_alphas%`）。
> 双闸值全部 `check_correlation(refresh=True)` 实测，非台账。

---

## 一、执行摘要

本轮扫了 8 个 region × 10 档（9 档建成并双闸实测，1 档因并发上限未落地），**唯一新增产能 = DEU/TOP500 的三个未占中性化族**（FAST / CROWDING / SLOW），三颗全部双闸 PASS 且余量厚（0.10–0.24）。这**推翻了 10-24 起"DEU 全域停投"的结论**——DEU 组件池 11→14 后 prod 墙从 0.728 掉到 0.462–0.599。

其余七个 region 结论不变：**SA 线仍全域饱和**（8 个 GO 区所有可建 universe 全被 SUPER 占用；唯二空闲的合法 universe 是 USA/TOP200 与 EUR/TOP1200·TOP800·TOP400，前者 IS 不可达、后者结构性 prod 墙）。

### 优先队列（按「双闸余量 × pyramid 价值」排序）

| # | Alpha ID | 槽位 | 配方 | S | F | TO | prod | self | 余量(prod/self) | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| ⭐1 | `vR1oxZA3` | DEU/TOP500 | FAST d1 l10 cp1 | **3.27** | 3.09 | 0.1828 | **0.5987** | **0.5985** | 0.101 / 0.102 | ✅ B 档（S 最高） |
| ⭐2 | `0mYak1nv` | DEU/TOP500 | CROWDING d1 l10 cp1 | 2.86 | **3.11** | **0.1229** | **0.5165** | 0.4899 | **0.184 / 0.210** | ✅ 余量最厚 |
|  3 | `bl6K2Oor` | DEU/TOP500 | SLOW d1 l10 cp1 | 2.66 | 2.32 | 0.1462 | **0.4619** | 0.4622 | **0.238 / 0.238** | ✅ 最抗漂移 |
|  4 | `N1N2WRXo` | GBR/TOP700 | SUBINDUSTRY d1 l10 cp1 | 3.49 | 3.25 | 0.1578 | 0.6867 | 0.6766 | 0.013 / 0.023 | ⚠ 余量不足 0.02，仅备选 |
|  5 | `LLM2qe2M` | USA/TOP2000 | SECTOR d1 l10 cp3 | 3.73 | 4.02 | 0.1333 | 0.6957 | 0.6007 | **0.004** / 0.099 | ⚠ prod 贴墙，不建议 |

**推荐执行顺序**：`vR1oxZA3` → `0mYak1nv` → `bl6K2Oor`（同一席，任一颗提交即其余两颗作废；见 §五 DEU 同席说明）。
若求"一次过关、抗 48h 漂移"，选 `bl6K2Oor`（prod 0.4619，距红线 0.238）；若求指标，选 `vR1oxZA3`。

---

## 二、数据基线

### 2.1 组件池 eligibility（口径：ACTIVE + 已提交 REGULAR，IS 阶段不计）

| Region | eligible | 本地库 universe 分布（近似） | verdict |
|---|---|---|---|
| USA | 47 | TOP3000 40 / TOP2000 5 / ILLIQUID_MINVOL1M 4（非法档） | GO |
| IND | 47 | TOP500 42 / NONE 6 | GO |
| KOR | 34 | TOP600 36 | GO |
| GBR | **24**（21→24 ↑3） | TOP700 20 | GO |
| EUR | **23**（19→23 ↑4） | TOP2500 13 / TOPCS1600 11 | GO |
| MEA | 19 | TOP400 20 | GO（**平台已下架，不可建**） |
| GLB | 18（17→18 ↑1） | MINVOL1M 17 / TOPDIV3000 1 | GO |
| DEU | **14**（11→14 ↑3） | TOP500 14 | GO |
| ASI | 9 | MINVOL1M 6 / MINVOL10M 3 | BLOCKED（差 1） |
| HKG | 7 | TOP800 7 | BLOCKED（差 3） |

> 组件池较 11-07 全面增长：GBR +3、EUR +4、DEU +3、GLB +1。**但只有 DEU 的增长转成了产能**（见 §五）。
> 本地库 universe 分布与服务端口径有 ±2 偏差（`platform_status` 缓存滞后），仅作结构参考；totals 一律以 probe 为准。

### 2.2 档位占用分类（49 颗 ACTIVE SUPER，按 region×universe）

| Region | Universe | SUPER | 已占中性化族 | 档位类型 |
|---|---|---|---|---|
| USA | TOP3000 | 6 | FAST、MARKET(l1000)、SLOW×2、STATISTICAL(l30)、SUBINDUSTRY | 🔴 已占 |
| USA | TOP2000 | 1 | STATISTICAL(l15) | 🔴 已占（SECTOR 本轮测，prod 墙） |
| USA | TOP1000 | 1 | STATISTICAL(l15) | 🔴 已占 |
| USA | TOP500 | 1 | CROWDING(l10) | 🔴 已占（封档） |
| USA | TOPSP500 | 1 | STATISTICAL(l38) | 🔴 已占 |
| USA | TOP200 | 0 | — | ⚪ 零 SA 占用（历史 IS 不可达 S≤1.28） |
| IND | TOP500 | 12 | STAT×5(+l20)、SUBIND×2(+l1000)、INDUSTRY、SLOW、RAM(l30) | 🔴 饱和 |
| KOR | TOP600 | 11 | STAT×3(+l12/l30)、SUBIND×2、CROWDING、SLOW、RAM(l30) | 🔴 饱和 |
| GBR | TOP700 | 5 | STAT×2、FAST、RAM、SLOW | 🔴 饱和（本轮补 SUBIND） |
| GLB | MINVOL1M | 2 | STATISTICAL、SUBINDUSTRY | 🔴 已占 |
| GLB | MINVOL10M | 1 | SLOW | 🔴 已占 |
| GLB | TOP3000 | 1 | RAM | 🔴 已占 |
| GLB | TOPDIV3000 | 1 | STATISTICAL(l15) | 🔴 已占 |
| EUR | TOP2500 | 2 | CROWDING、STATISTICAL | 🔴 已占 |
| EUR | TOPCS1600 | 1 | STATISTICAL | 🔴 已占 |
| EUR | TOP1200/TOP800/TOP400 | 0 | — | ⚪ 零 SA 占用（结构性 prod 墙） |
| DEU | TOP500 | 1 | STATISTICAL | 🟢 **本轮开挖成功（3 个空族全部可建）** |
| MEA | TOP400 | 2 | SUBINDUSTRY(l10/l20) | ⛔ 区域已下架 |

**合法 universe 权威清单**（`get_platform_setting_options`）复验：
- USA d1：TOP3000/TOP2000/TOP1000/TOP500/TOP200/TOPSP500（**无 ILLIQUID_MINVOL1M**）
- GLB d1：TOP3000/MINVOL1M/MINVOL10M/TOPDIV3000（**无 TOP2000**）
- DEU d1：仅 TOP500（**无 TOP300**）
- EUR d1：TOP2500/TOP1200/TOP800/TOP400/TOPCS1600
- **MEA 不在任何 region 列表** ⇒ 确认永久不可建

### 2.3 Pyramid 倍率（D0/D1 覆盖的 datacategory 均值与最大值）

| Region | D0 均值 | D0 最高 | D1 均值 | D1 最高 |
|---|---|---|---|---|
| **DEU** | **1.85** | **1.9** | **1.61** | **1.8** |
| GBR | 1.68 | 1.9 | 1.41 | 1.7 |
| HKG | — | — | 1.41 | 1.7 |
| KOR | — | — | 1.39 | 1.6 |
| EUR | 1.41 | 1.7 | 1.20 | 1.5 |
| USA | 1.53 | 1.8 | 1.18 | 1.4 |
| GLB | — | — | 1.18 | 1.4 |
| ASI | — | — | 1.18 | 1.5 |
| IND | — | — | 1.14 | 1.4 |

> **DEU 是全域 pyramid 价值最高的 region（D0 1.85 / D1 1.61）**，此前却被列入停投 —— 本轮最大的结构性错配修正。
> DEU 最优五类：news 1.8 / model 1.8 / analyst 1.8 / other 1.8 / fundamental 1.8（D1）。

---

## 三、选点原则（本轮验证后更新）

1. **档位占用类型 > 组件池大小**：零 OS 档（self 恒 0）只在对的 region 有价值；DEU 属于"已占 1 席但空 10 个族"的第三种形态——**族级空位（family vacancy）是被长期忽略的产能来源**。
2. **指标 = 约束优化**：`max IS(F, 其次 S) s.t. prod<0.7 ∧ self<0.7 ∧ 余量≥0.02`；优选 B 档（prod<0.6 ∧ TO<0.30）。
3. **族速度阶梯（本轮 DEU 实测复现）**：`FAST > CROWDING > SLOW` 在 S 上单调，在 prod 上反向（0.599 / 0.517 / 0.462）。
   ⇒ **先用 FAST 摸 S 天花板，再退 CROWDING/SLOW 换余量**。与 11-07 "族越快 S 越高 prod 越脏" 完全一致。
4. **池子增长只对"有族空位"的 region 有效**：EUR 池 19→23 仍 prod 0.7342，DEU 池 11→14 直接破墙 —— 差别在 DEU 有空族可选，EUR 的空档是 universe 级空档（成分池仍薄）。
5. **cp（combo_power）不是普适杠杆**：GBR cp1→cp3 双闸同时恶化（0.6867→0.6980 / 0.6766→0.6976）；USA cp1→cp3 仅把 prod 从 0.7032 压到 0.6957。⇒ **cp 只在自席已确定后做微调，不能救墙**。
6. **同 universe 的不同族 ≠ 独立席**：DEU 三颗同 universe 同 l10，只有中性化不同。任一颗提交后，其余两颗的 self 会跳到 ~1。**一个 universe 一次只交一颗**。

---

## 四、论坛指标标准（固化引用，2026-10-22 定稿，不需重复调研）

来源：《【新人入门】Super Alpha 从入门到入门！》78 赞 / 39 评论、《2024 super alpha 比赛心得》22 赞 / 15 评论、《Super Alpha 参数设置》12 赞（含 LY43440 实测回复）。

### 4.1 组成数量（Selection Limit）
- **平台硬下限 = 10**（<10 直接 400：`Ensure this value is greater than or equal to 10`）
- 论坛建议 30–100 起测、≤500；LY43440 在 IND 实测取 300
- **实际生效数 = min(limit, 组件池)**；本工作区实证 **l10 为甜点**（l12/l14 普遍推高 prod 与 self）

### 4.2 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.6** |
| C 比赛/优秀档 | **5.6–7.0** | **5.6–8.9**（冲>10） | 0.20–0.27 | <0.5 |

> 本轮 3 颗 DEU 全部落在 **B 档**（prod 0.46–0.60，TO 0.12–0.18）；C 档需要 S≥5.6，DEU 池 14 撑不起（高 S 只在 GLB/MINVOL1M 出现过，见 §七）。

### 4.3 组件筛选阈值
`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。

⚠ **两条不可消费的修正（本工作区实测）**：
- 加严约束后组件 <10 ⇒ `At least 10 component alphas are required`；本轮小池区（DEU 14 / GBR 24）只能用宽松 `(1 - self_correlation)`。
- **`author_*` 是作者级聚合量，在自有池恒为常数**（同一作者全部 alpha 同值）⇒ 论坛 `author_fitness≥2` 阈值在本账户**无区分度**，照抄只会得到常数缩放。

### 4.4 其他实证
- truncation 0.02 vs 0.08 对 SA 几乎无差异（S 3.74 vs 3.73）
- `Selection Handling = Non-Zero` 论坛推荐；本工作区历史 49 颗 SA 全用 `POSITIVE` 均成功
- **`(prod_correlation > 0)` 在 USA 是模型层强校验**：`super_build.py` 直接抛 pydantic `Value error, USA SUPER simulations require selection to include (prod_correlation > 0)`（不是平台 400）。修法：`(1 - self_correlation) * (1 + 0 * (prod_correlation > 0))`

---

## 五、分 Region 方案

### 5.1 DEU / TOP500（🟢 本轮唯一新产能 — 推荐）

**为什么现在能建**：组件池 11→14（+3，越过 l10 的余量区），且 TOP500 只被 STATISTICAL 一族占位，FAST / CROWDING / SLOW 三个族全部空置。

| 配方 | ID | S | F | TO | 2Y | SUB | prod | self | IS checks |
|---|---|---|---|---|---|---|---|---|---|
| **FAST d1 l10 cp1** | `vR1oxZA3` | **3.27** | 3.09 | 0.1828 | 4.39 | 1.99 | 0.5987 | 0.5985 | 8 项全 PASS，fail=[] |
| **CROWDING d1 l10 cp1** | `0mYak1nv` | 2.86 | 3.11 | 0.1229 | 3.35 | 2.08 | 0.5165 | 0.4899 | 8 项全 PASS，fail=[] |
| **SLOW d1 l10 cp1** | `bl6K2Oor` | 2.66 | 2.32 | 0.1462 | 4.30 | 2.02 | 0.4619 | 0.4622 | 8 项全 PASS，fail=[] |

- **预期**：B 档达标（prod<0.6、TO<0.30）；DEU pyramid D0 1.85 / D1 1.61 为全域最高，同等 IS 下 OS 分配最高。
- **双闸实测值均为 `refresh=True`**，测试时刻 2026-11-08 07:00±20min。
- 三颗同 universe 同 l10 ⇒ **同席互斥**，只交一颗。建议 `vR1oxZA3`（S 最高）或 `bl6K2Oor`（余量最厚）。

### 5.2 GBR / TOP700（⚠ 仅备选）

| 配方 | ID | S | F | TO | prod | self | 余量 |
|---|---|---|---|---|---|---|---|
| SUBINDUSTRY d1 l10 cp1 | `N1N2WRXo` | 3.49 | 3.25 | 0.1578 | 0.6867 | 0.6766 | 0.013 / 0.023 |
| SUBINDUSTRY d1 l10 **cp3** | `vR1oxrld` | 3.47 | 3.20 | 0.1564 | 0.6980 | 0.6976 | 0.002 / 0.002 |

- SUBINDUSTRY 是 GBR 唯一未占族，S 3.49 尚可，但 **prod/self 双贴墙**，余量均 < 0.02 安全线。
- cp3 是**负杠杆**（两闸同时恶化 0.011 / 0.021）⇒ 该族在 GBR 无优化余地，除非生产池漂移让 prod 回落。
- GBR 现有 5 颗 SUPER（STAT×2/FAST/RAM/SLOW），本身就是全域最满的小池区。

### 5.3 USA / TOP2000（⚠ 不建议）

| 配方 | ID | S | F | TO | prod | self |
|---|---|---|---|---|---|---|
| SECTOR d1 l10 cp1 | `E56208rR` | 3.69 | 3.85 | 0.1431 | **0.7032 FAIL** | —（早退未算） |
| SECTOR d1 l10 cp3 | `LLM2qe2M` | 3.73 | 4.02 | 0.1333 | **0.6957**（余量 0.004） | 0.6007 |

- SECTOR 族在 USA/TOP2000 结构性贴墙（两种 cp 都落在 0.695–0.703）。
- 唯一亮点：**self 仅 0.6007**（对 `vROw5Rkd`），说明 SECTOR 确实是独立席 —— 缺的是 prod，不是席位。
- 若要救，只能换更低 prod 的族（INDUSTRY / MARKET / SLOW 未测），但 USA 全域历史上族越细 prod 越高（CROWDING 0.6246 → MARKET 0.694 → SUBINDUSTRY 0.7479），预期不乐观。

### 5.4 EUR（❌ 结构性墙，第 4 次确认）

| 配方 | ID | S | F | TO | prod |
|---|---|---|---|---|---|
| TOP1200 SLOW d1 l10 | `QPvoroQM` | 2.20 | 1.19 | 0.2258 | **0.7342 FAIL** |
| TOP800 SLOW d1 l10 | `kqNYkg1g` | **1.47** | **0.67** | 0.2393 | 未测（IS 已不足） |

- 池 19→23 完全无效；换族（历史 CROWDING 0.7117/0.7337/0.7783，本轮 SLOW 0.7342）同样无效。
- TOP800 连 IS 底线都不到（S 1.47 < 1.58，F 0.67 < 1.0）⇒ EUR 空档从"墙"退化为"无信号"。

### 5.5 GLB（❌ 仍死，但有一条待验）

- 历史未提交高 S 档已批量验尸（见 §七）：`O0Am5P3q`（MINVOL1M STAT l12，S7.65/F4.57/2Y7.0）**prod 0.8728 FAIL**；MINVOL1M SLOW S6.82 → 0.72（11-07 实测）。
- 本轮 GLB/MINVOL1M SLOW 重建两次撞 429（并发上限），第三次平台已受理但本地进程被回收、未落盘；同席存量 `e75G8KZl` / `xArd7rVn`（S6.82/F3.71/TO0.3449）11-07 实测 prod 0.72 ⇒ SLOW 族在 MINVOL1M 亦撞墙。
- **GLB 四个 universe 全部已被占**，且 MINVOL10M 的 SLOW 席已由 `LLMVPag1` 提交 ⇒ 封档。

### 5.6 IND / KOR / MEA / ASI / HKG

- **IND（47 池，12 席）**：全域最饱和。CROWDING 0.7733、FAST 0.6467（历史）均在墙边；无空族可挖。
- **KOR（34 池，11 席）**：FAST 0.8209 双撞（11-07），CROWDING/SLOW/STAT/SUBIND 全占 ⇒ 封档。
- **MEA**：`Region MEA is not available`，platform options 与 pyramid 均无 MEA ⇒ **永久停投**（历史 2 颗仍 ACTIVE，不影响新建）。
- **ASI（9）/ HKG（7）**：池差 1 / 差 3，**无法建 SA**。唯一催产能路径 = 提交更多 REGULAR（ASI 有 56 颗 IS 阶段存量，HKG 0 颗）。

---

## 六、停投区（更新）

| 区域 | 状态 | 理由 |
|---|---|---|
| EUR 全域 | ⛔ 停投 | 空档 IS 不足（TOP800 S1.47）+ prod 墙（TOP1200 0.7342 / TOP2500·TOPCS1600 已占）；池增长 19→23 无效 |
| IND | ⛔ 停投 | 12 席饱和，CROWDING/FAST 均撞墙 |
| KOR | ⛔ 停投 | 11 席饱和，FAST 0.8209 |
| GBR | ⚠ 冻结 | 5 席饱和；SUBINDUSTRY 余量 0.013 不足，cp3 更差 |
| GLB | ⛔ 停投 | 4 universe 全占；MINVOL1M 高 S 档 prod 0.87 |
| USA-TOP3000 | ⛔ 停投 | 6 席；CROWDING 0.7690（rank(w)）、cp3 0.842 |
| USA-TOP500 / TOPSP500 / TOP1000 / TOP200 | ⛔ 停投 | 已占或 IS 不可达（TOP200 S≤1.28） |
| USA-TOP2000 | ⚠ 观察 | SECTOR 贴墙 0.6957；self 0.6007 说明有独立席，待更低 prod 的族验证 |
| MEA / ASI / HKG / CHN / JPN / TWN / AMR | ⛔ 停投 | 区域下架 / 池 <10 |
| **DEU** | 🟢 **解除停投** | 本轮三族双闸全 PASS，余量 0.10–0.24 |

---

## 七、撞墙档案（本轮 + 关键历史）

| 候选 | 槽位/配方 | 指标 | 撞哪一闸 |
|---|---|---|---|
| `O0Am5P3q` | GLB/MINVOL1M STAT l12（历史存量） | S7.65 / F4.57 / 2Y7.0 / TO0.3084 | **prod 0.8728** |
| `E56208rR` | USA/TOP2000 SECTOR cp1 | S3.69 / F3.85 | prod 0.7032（+0.0032） |
| `LLM2qe2M` | USA/TOP2000 SECTOR cp3 | S3.73 / F4.02 | prod 0.6957（余量 0.0043 < 0.02） |
| `QPvoroQM` | EUR/TOP1200 SLOW | S2.20 / F1.19 | prod 0.7342 |
| `kqNYkg1g` | EUR/TOP800 SLOW | S1.47 / F0.67 | IS：LOW_SHARPE + LOW_FITNESS |
| `vR1oxrld` | GBR/TOP700 SUBIND cp3 | S3.47 / F3.20 | prod 0.6980 / self 0.6976（双贴墙，cp3 负杠杆） |
| GLB/MINVOL1M SLOW（本轮重建） | 平台受理但本地进程回收，未落盘 | 同席存量 S6.82 | 历史 prod 0.72（11-07） |
| GLB/MINVOL1M FAST | S6.34 | — | self 0.7384 / prod 0.7486（11-07） |
| DEU/TOP500 STATISTICAL | 已占（`mLYLEm99`） | — | 历史 prod 0.728（池 11 时）；**池 14 后同族未重测** |

---

## 八、算子利用审计（平台 SA 可用算子 vs 本工作区实用）

**权威口径**：官方《SuperAlpha Operators》附录 **161 个** SA 可用算子（其中 COMBO 侧 160、SELECTION 侧 43）。`get_operators` 返回的 103 个是 **REGULAR 全集**，不是 SA 全集 —— 不可用它判断 SA 覆盖率。

**本账户 49 颗 ACTIVE SUPER 的实际使用**：

| 侧 | 用到的算子 | 去重数 | 覆盖率 |
|---|---|---|---|
| COMBO | `generate_stats` `self_corr` `if_else` `reduce_max` `subtract` `multiply` `equal` `rank` | 8 / 160 | **5.0%** |
| SELECTION | `greater` `multiply` `subtract` `add` `less` `if_else` `sqrt` `or` | 9 / 43 | **20.9%** |
| 合计去重 | — | **14 / 161** | **8.7%** |

**本轮 12 档新增使用算子 = 0**：全部走规范模板 `(1 - self_correlation)` + `w = 1 - maxCorr`（8 个算子内），USA 另加 `(1 + 0*(prod_correlation>0))` no-op 门（仍是既有算子）。

**已证伪、不必再试的算子/形变**（累计 4 轮）：
`zscore(w)`（S −1.14）、`sqrt(w)`（同席 0.9917）、`ts_mean(w,20)`（0.7837）、`rank(w)`（USA 撞 0.712 / GLB 0.6617 边际）、`reduce_avg` / `reduce_percentage`（Ladder FAIL）、`combo_power≥6`（2Y == 1.58 恰 FAIL）、`decay`（SA 层完全无效）、`in(...)` 硬过滤（组件 <10）、`author_*`（恒常数）、`dataset_count` 分档（仅 IND 有效）。

**尚未利用且值得一测（P0–P2）**：
- **P0 `combo_weight`** —— 平台唯一"显式给权重"入口，语义至今未摸底（可能是唯一能绕过"权重由 1−maxCorr 决定"的算子）。
- **P1 `tanh` / `signed_power(x,3)` 保号整形** —— 顺序统计已证伪，保号非线性未测。
- **P2 `ts_target_tvr_decay` / `hump`（SA 侧）压 TO** —— 可把 A 档高 TO 候选推进 B 档（TO<0.30）。
- **不建议**：`zscore` / `normalize`（破保号）、`bucket`/`group_*` 类截面算子（SA 的 combo 输入是 alpha 收益序列，不是截面字段）。

---

## 九、执行清单

### 9.1 构建命令（本轮实际执行，可复现）

```bash
cd D:/coding/traeCN_project/wqb
PY=world-quant-brain-mcp/.venv/Scripts/python.exe
SEL='(1 - self_correlation)'
SEL_USA='(1 - self_correlation) * (1 + 0 * (prod_correlation > 0))'
O=results/sa_scan_20261108

# DEU 三族（本轮唯一新产能）
$PY tools/super_build.py select --region DEU --universe TOP500 --delay 1 --decay 1 \
  --neutralization FAST     --selection-limit 10 --selection "$SEL" --json $O/res_deu_t500_fast.json
$PY tools/super_build.py select --region DEU --universe TOP500 --delay 1 --decay 1 \
  --neutralization CROWDING --selection-limit 10 --selection "$SEL" --json $O/res_deu_t500_crowd.json
$PY tools/super_build.py select --region DEU --universe TOP500 --delay 1 --decay 1 \
  --neutralization SLOW     --selection-limit 10 --selection "$SEL" --json $O/res_deu_t500_slow.json

# USA 修法（必须带 no-op prod 门，否则 pydantic 直接拒）
$PY tools/super_build.py select --region USA --universe TOP2000 --delay 1 --decay 1 \
  --neutralization SECTOR --combo-power 3 --selection-limit 10 --selection "$SEL_USA" --json $O/res_usa_t2000_sector_cp3.json
```

### 9.2 配额与技术约束

| 约束 | 值 | 说明 |
|---|---|---|
| **并发仿真上限** | **2** | 第 3 颗必返 `429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED`（本轮实测 3 次）。**批量派发必须串成 2 路**。 |
| SUPER 提交配额 | 1 / 天 / region | 与 REGULAR 4/天/region 独立计数 |
| 平台硬下限 | limit ≥ 10 | 组件池 <10 返 `At least 10 component alphas are required` |
| prod 红线 | < 0.7（无豁免） | 余量 ≥ 0.02 才算安全；B 档 < 0.6 |
| prod 台账保鲜 | 48h | 提交前必须 `check_correlation(refresh=True)` |
| prod 队列 | 账号级单并发 | busy 时按 `retry_after` 重查，**不要重派**；新建 SA 首次查 prod 多为 `data_unavailable`，等 2–5 min |

### 9.3 建议执行顺序

1. **Day 1**：`vR1oxZA3`（DEU，S 3.27）→ 提交前 `refresh=True` 复测双闸（prod 0.5987 余量 0.101，能扛 48h 漂移）
2. 若 `vR1oxZA3` 因漂移跌破：**同席换** `0mYak1nv`（prod 0.5165）或 `bl6K2Oor`（prod 0.4619）—— 三颗不能同时交，交任一颗即 DEU/TOP500 封档
3. **Day 2+**：无第二区可交。下一轮产能只能来自：① ASI/HKG 池过 10（需先提交 REGULAR）② 生产池漂移让 GBR/USA-TOP2000 的 prod 回落 ③ `combo_weight` 算子摸底出新结构
4. **禁止**：本轮不加严 selection（会掉到 <10 组件）、不扫 decay、不再扫 cp≥6、不对 EUR/GLB/IND/KOR 重复建同席。

### 9.4 提交命令（仅当用户点名）

```bash
cd D:/coding/traeCN_project/wqb && WQB_ALLOW_ALPHA_SUBMIT=1 \
  world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py submit \
  --alpha-id <ID> --region DEU
# 内置 prod 闸（0.7）fail-closed；提交前先停掉任何后台仿真批次
# 复核：等 flip 窗 ~250s 后 tools/super_build.py status --alpha-id <ID> 确认 ACTIVE
```

---

## 十、本轮新增工程事实（写入记忆）

1. **并发上限 = 2**：`create_simulation` 第 3 路必 429；`super_build.py select` 不打印 status_code，只显示 `[error] Failed to create simulation / None` —— 极易误判为池不足。诊断必须看 MCP `create_simulation` 返回体。
2. **USA SUPER 的 selection 强校验在 pydantic 层**：缺 `(prod_correlation > 0)` 时抛 `ValidationError`，不是平台 400；`super_build.py` 会以 traceback 结束，日志里没有 `[error]` 行，grep 时容易漏。
3. **`super_build.py select` 缺少 `--selection-handling`**（硬编码 POSITIVE）；`--truncation` 缺省会写 0.08（不是 0.02），对 SA 指标影响可忽略但会与历史档不一致。
4. **`C:/Users/MENGTAO/wqb-scripts/sa_run.py` 已不存在**（整目录缺失）⇒ 本 SOP 的"构建"步骤改用 `tools/super_build.py select` 循环，功能等价。
5. **DEU 池 11→14 是分水岭**：池 <12 时 DEU/TOP500 prod 恒 0.728（10-24 判死），池 14 时三个族全部 0.46–0.60 ⇒ **"池太小导致 prod 墙"是可逆的**，停投结论必须带池规模标注。

---

*本文档由定时任务自动生成；所有候选均为 UNSUBMITTED，未执行任何提交动作。*
