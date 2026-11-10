# PPA 标签治理与 Combined Power Pool Alpha Performance 提升方案 · 2026-11-10

> 触发：用户问「已提交 alpha 的 PPA 标签打得对不对、应该怎么打」，目标 = **提高 CPPAP**。
> 证据：平台全量标签池实测（66 颗逐颗）+ 本地 11-07 PATCH 记录 + 4 篇平台论坛实证。

## 0 结论速览

1. **打得不对**，但不是「该打没打」，而是**池子成分从未治理**：301 颗 ACTIVE 中 66 颗带 `PowerPoolSelected`，其中 **24 颗只有这一个标签**（缺 `CH_*`/`SRC_*`，不合规），至少 **13 颗是 11-07 我们自己 PATCH 上去的**——本地文档「36 颗均为平台所打」的结论**是错的**。
2. **标签是 CPPAP 的成分开关**：带标签 = 计入 Power Pool 组合；摘掉 = 不计入。提高 CPPAP 的直接杠杆不是「给好货打标签」，而是**把拖后腿的摘掉**；且**可逆**（加回后下一次刷新即生效）。
3. 现行池里 **27/66 颗 margin<10bp**，其中 **18 颗同时 TO>0.15** —— 正是论坛实证中该摘的那类；另有 9 颗低 margin 但低换手，**论坛明确说别摘**。
4. 操作纪律：**一次只动一条**，等约 6 小时榜单刷新读 BC/AC，涨了留、跌了改回；禁止用本地 PnL 近似挑「最好的 N 条」。

## 1 现状盘点（平台 `tag=PowerPoolSelected` 实查，66 颗）

数据源：`results/ppa_tag_pool_20261110.json`（逐颗 id/region/tags/S/F/margin/TO）。

| 类别 | 颗数 | 判定 |
|---|---:|---|
| 只有 `['PowerPoolSelected']` | **24** | ❌ 不合规：缺 `CH_*` / `SRC_*`；且被 `_is_ppa` 误判为 PPA 通道 |
| `CH_PPA` + `PowerPoolSelected` | **28** | ✅ 真 PPA 通道（历史 PPA 提交，合规） |
| `CH_REG` + `PowerPoolSelected` | **9** | ✅ 平台自动追加（含今日 `P0obGoQJ` / `akK9ooZv`） |
| 其它（自定义标签 / `CH_SUPER`） | **5** | ⚠ 部分标签数超 5 上限 |

同次 `tools/alpha_properties.py audit`（301 颗 ACTIVE）：**148 颗有合规告警** —— 98 无标签、50 缺 `SRC_*`、37 缺 `CH_*`、3 标签数 6 超限。

**关键纠错**：`results/ppa_tag_20261107/patch_tags.py` 明写「PATCH tags -> `['PowerPoolSelected']` only (user instruction: remove original tags)」，`patch_results.json` 13/13 成功，ids =
`omEMRpWb` `e75pvoNz` `LLM5eAMn` `0mjk2ZQv` `A1vzEm9g` `A1QQ0q8d` `bl69VL5M` `e76xGOQO` `6XA8AGjL` `3qowjY0Z` `RREnK5R1` `LL5VwgO1` `JjeGEzaE`。
⇒ 这 13 颗的标签**是我们打的，不是平台自动追加**。`docs/alpha_properties_spec.md` §3.5 与 `MEMORY.md` §9 的「平台行为 / 逐颗核实均为平台所打」需修正。

补充：`rKRx2Alj`（今日 02:18 提交）Step 6 记 `power_pool_selected=false / disposition=absent`，提交后 8 分钟复查仍无标签；而 `P0obGoQJ`（ET 02:41 提交）确实带标签 ⇒ **平台自动追加是有条件的，不是每颗必打**（论坛：需有 PP 资格 / 命中当期主题）。

## 2 机制：论坛四篇实证

| 帖子 | 赞 | 关键结论 |
|---|---:|---|
| `44230497234839` LZ90942《PP 主题榜实测：摘标签、加回、裁到 10 条》 | 1 | ①有 PP 资格的货交上去**自动带标签**，去掉就不计入；②**加回去下一次刷新全进**（推翻「加回当期不算」）；③榜约 **6 小时刷新**；④**摘高换手/低 margin 有用，低换手边缘货别摘**（摘 7 条 BC 反掉 .053）；⑤BC−AC 差值固定 .159–.177，只能靠换货；⑥**本地 PnL 近似不可信**（挑「最好 10 条」上榜从 +.023→−.039）；⑦条数不决定 AC |
| `38846510482967` MZ45384《CPPAP 持续稳定 2.12→2.67》 | 74 | ①提交标准 S/F>1（F≥0.6）、**margin 目标 15‱ 最低 10‱**；②曲线不低头、尾年不差；③每月专注 2 区 + 月底点满塔 + 区域多样性；④**为点塔交的难看 alpha 删 `PowerPoolSelected` 保护 CPPAP**；⑤**tag 管理只是权宜之计，只能保护 CPPAP，对 Combined Alpha Performance 于事无补**；⑥正道是多交高质量 alpha |
| `33099321751447` ZX58901《如何在 Power Pool 中添加或移除 Alpha》 | 28 | 官方操作：Properties 点叉移除 / Tags 下拉重新勾选；**移除标签后仍在 self-correlation pool**，仍参与相关性校验 |
| `4341192092519` LT20707（搜索摘要） | 1 | 平台主题列表的「符合主题的提交数」数的是**带标签**的 Alpha，不是 themes 匹配数；**匹配 ≠ 参赛，删 tag = 停赛** |

另：`43284541539991`（121 赞）提供 OSMOSIS 工具思路——「把当前有分数但没带标签的因子分数清零，只对真正带标签的因子等权赋分」；`44819524884247` 给「每组 ≥10 或整组撤出」的池治理协议。

## 3 「应该怎么打」——分阶段规范

| 阶段 | 动作 | 依据 |
|---|---|---|
| **提交前** | **绝不主动打** `PowerPoolSelected`。只打 `CH_REG`/`SRC_<dataset>`/`CORR_*`（≤5 个）。 | 预置会让平台按 `PURE_POWER_POOL_THEME` 审本次提交，合法 REGULAR 可能被拒；`_derive_tags` 已强制剔除；`set_alpha_properties` 工具描述明确「PPA 通道专有，普通提交不要打」 |
| **提交后 T+0** | 平台自动打上的**不要清**（它就是 PP 池入口）。Step 6 `tag_disposal` 只留痕。 | 清掉 = 该颗退出 CPPAP 成分；用户既以 CPPAP 为目标，就不该默认清 |
| **池治理（随时，可逆）** | 按质量**摘差货的标签**；把未带标签的好货**补打**标签（PATCH 追加，注意 ≤5 上限）。 | 论坛 4 篇一致；官方帖证明可增删，LZ90942 证明加回当期生效 |
| **属性合规** | 用 `tools/alpha_properties.py normalize --apply` 给 24 颗单标签补 `CH_*`/`SRC_*`；**不要删** `PowerPoolSelected`（工具设计无条件保留）。 | 解决 148 颗合规告警 |

⚠ 旧结论需修正：过去写「清掉 = 放弃 CAP 四口径中的 PP 一条，因取最大且 PP 系统性最低，损失≈0」——这在**以 CAP 总分为目标**时成立；**当目标就是 CPPAP 本身时不成立**：标签直接决定 CPPAP 成分，清/留是核心杠杆，不是可忽略项。

## 4 提高 CPPAP：可执行清单

### 4.1 优先摘标签（18 颗，margin<10bp **且** TO>0.15）

论坛双判据交集。按 margin 升序（完整数据在 `results/ppa_tag_pool_20261110.json`）：

| id | 区 | S/F | margin | TO |
|---|---|---|---:|---:|
| `JjeMlmXA` | GLB | 3.04/1.11 | **2.66bp** | .319 |
| `gJboYLRl` | GLB | 2.67/1.13 | **3.58bp** | .416 |
| `A10wOvAe` | HKG | 1.06/**0.47** | **4.00bp** | .261 |
| `P0obGoQJ` | ASI | 3.06/1.39 | **4.12bp** | .291 |
| `xAY86Mkl` | KOR | 1.61/**0.75** | **4.32bp** | **.550** |
| `akK9ooZv` | GBR | 3.10/1.48 | **4.59bp** | .411 |
| `LL5VwgO1` | EUR | 2.64/1.27 | 4.62bp | .377 |
| `GrlGJnPJ` | USA | 2.02/1.01 | 4.97bp | .236 |
| `6XA8AGjL` | GBR | 2.16/1.11 | 5.31bp | .191 |
| `E5ReEnpP` | ASI | 1.93/1.06 | 5.99bp | .314 |
| `3qVP6pNO` | GBR | 1.84/1.02 | 6.13bp | .209 |
| `LLM5eAMn` | EUR | 3.48/1.95 | 6.30bp | .198 |
| `mLmxKN12` | GLB | 2.99/1.69 | 6.37bp | .389 |
| `883Y3bAW` | DEU | 2.17/1.24 | 6.58bp | .342 |
| `MPQVZRnk` | USA | 2.23/1.44 | 8.32bp | .180 |
| `levk5JYN` | IND | 3.34/2.20 | 8.71bp | .328 |
| `1YzLbZzQ` | IND | 1.81/1.24 | 9.42bp | .187 |
| `A1vzEm9g` | IND | 2.84/1.97 | 9.58bp | .287 |

⚠ **今日新交的 `P0obGoQJ` / `akK9ooZv` 也在名单里**：IS 很强（S3.06/3.10）但 margin 仅 4bp、TO 29%/41%，按论坛标准正是拖 CPPAP 的货。这正是「为点塔交难看 alpha」的典型（MZ45384 第 4 条）。
⚠ 但**不要一次摘 18 颗**：LZ90942 实测低换手批次摘了 BC 反掉，必须逐条对照。

### 4.2 明确别摘（9 颗：margin<10bp 但 TO≤0.15）

`1YZQJKwR` `Xgojww1X` `JjeGEzaE` `9qWwZ3oe` `gJj1nxLM` `786pLKnb` `Wje6pdqN` `3qowjY0Z` `d51A3nqY`
⇒ 论坛：「摘高换手、低 margin 的有用，**低换手的边缘货别摘**」。

### 4.3 池内高质量锚（14 颗 margin≥15bp 且 TO≤0.15）

`e7z1vG06`(54.97bp) `gJj7rnxQ`(50.78) `3qlYKAaO`(47.56) `9qXoJge2`(43.19) `xAdL5vmN`(34.62) `e76xGOQO`(25.37) `E56oYEkL`(19.73) `omLjG1M5`(18.68) `Vk65zLzG`(18.46) `KPrGMXZ8`(17.64) `O0xagXjd`(17.33) `pwjpKGJ3`(16.74) `ZY0R0mL8`(16.10) `e75pvoNz`(15.15)
⇒ 这些是 CPPAP 的正贡献锚，标签**必须保留**。

### 4.4 补标签方向（增量，未带标签的 235 颗）

筛「ACTIVE + margin≥15bp + TO≤0.15 + 尾年不差 + 区域多样性」的未带标签件，用 `set_alpha_properties` **追加** `PowerPoolSelected`（保留原有 CH_/SRC_，总数≤5）。注意**只能在提交后补**，提交前预置会触发 `PURE_POWER_POOL_THEME`。

### 4.5 提交端标准（治本）

MZ45384 原口径：S/F>1（F 最低 0.6）、margin 目标 15‱ / 最低 10‱、曲线不低头或尾年不差、每月专注 2 个区域并在月底前点满塔。
本工作区现状：今日清单里大量候选 margin<10bp（如 `mLovqRV6` 13.5bp、`rKRx2Alj` **17.08bp** 达标）。⇒ **把 margin≥10bp 加进挖掘闸门**，比事后摘标签更有效。

## 5 操作节奏（照 LZ90942 的对照法）

1. 期初读一次 PP 榜 BC/AC 作基线。
2. **一次只 PATCH 一条**标签，等约 6 小时刷新（ET 2 点 / 8–9 点 / 15:30 / 20 点前后）读榜。
3. AC 涨了保留，跌了用 Tags 下拉**加回**（实测当期生效，可逆）。
4. 最后两三天还在交货就停手，避免新货进榜污染对照。
5. 别用本地日 PnL 穷举挑组合——实测上榜反而变差。
6. 别指望改标签能缩小 BC−AC（该差值固定 .159–.177），要缩小只能换货。

**边界提醒**：tag 管理只能保护 CPPAP；Combined Alpha Performance / Selected 两个口径不受益。正道是提高提交质量。

## 6 需同步修正的本地结论

| 位置 | 旧结论 | 修正 |
|---|---|---|
| `docs/alpha_properties_spec.md` §3.5 | 「36 颗逐颗核实均为平台所打」 | 至少 13 颗是 11-07 我们自己 PATCH；现全量 66/301 |
| 同上 | 「清掉 = 放弃 PP 口径，取最大故损失≈0」 | CAP 视角成立；**以 CPPAP 为目标时，标签是成分开关，损失不≈0** |
| `MEMORY.md` §9 | 「平台提交后自动追加」「无标签不出 POWER_POOL_CORRELATION」 | 自动追加有资格条件（`rKRx2Alj` 提交后 8 分钟仍无）；`rKRx2Alj` 无标签却仍挂 `POWER_POOL_CORRELATION` pending |
| `alpha_properties.py` `tag_notes` | 「平台提交成功后自动追加」（对 24 颗单标签不成立） | 文案保留为信息项，但审计结论不再据此判定来源 |

**未执行任何 PATCH / 标签增删**（本轮只做只读盘点与方案），等用户点名再动。

---

# 补章（2026-11-10 02:4x）：执行 → 证伪 → 回滚 → 判据前移

用户指令「按最佳方案决策推进」。**结果：两条标签实验动作全部回滚，平台状态零净变化；但发现并纠正了一个方向性错误，把 CPPAP 判据前移到平台 `themes`。**

> 本文原第 123 行「未执行任何 PATCH」由本补章取代。

## 1 执行轨迹（append-only 台账 `results/ppa_tag_governance_log.jsonl`）

| seq | 动作 | alpha | 结果 | 验证 |
|---:|---|---|---|---|
| 1 | 摘 `PowerPoolSelected` | `JjeMlmXA`（GLB，2.66bp / TO .319，单标签） | tags `[]` | desc 1484→1484、name/color 不变 |
| 2 | 补 `PowerPoolSelected` | `O07AMoKR`（MEA，92.46bp / TO .036，`CH_REG`+`SRC_analyst7`） | tags 3 个 | desc 4→4、name/color 不变 |
| 3 | **回滚 seq1** | `JjeMlmXA` | 恢复 `['PowerPoolSelected']` | ✅ |
| 4 | **回滚 seq2** | `O07AMoKR` | 恢复 `['CH_REG','SRC_analyst7']` | ✅（首次平台瞬时非 JSON，重试完成） |

PATCH 载荷统一 `{tags:[...], regular:{description: <原样回显>}}`，避免 2026-09-20 那次 name/description 被清空的事故；每次回读验证四项，失败自动回滚。

## 2 ★ 决定性反证：`themes` 才是当期资格，`tags` 只是开关

| 实证 | 结果 |
|---|---|
| 给 `O07AMoKR` **补标签**后 | `themes` 仍为 `[]` ⇒ 补标签**不能创造主题归属** |
| 摘掉 `JjeMlmXA` **标签**后 | `themes` 仍含 `GLB/D1 Power Pool Nov'26` ⇒ 摘标签**不移除主题归属** |
| `POWER_POOL_CORRELATION` | 摘标签后仍 `PENDING`；无标签的 `rKRx2Alj` 也挂 ⇒ **与标签无关，不能当开关指示器** |

全账户 301 颗 ACTIVE 的 `themes` 分布（`results/ppa_theme_scan_20261110.json`）：

| 主题 | 颗数 | 性质 |
|---|---:|---|
| `GLB/D1 Power Pool Nov'26` | **1** | **当期**（即 `JjeMlmXA`） |
| `OTHER/D1 Power Pool Sept'26` | 10 | 往期 |
| `D1 Power Pool Oct'26` / `Oct'26 2` | 2 | 往期 |
| `GLB/D1 Power Pool Aug'26` | 1 | 往期 |
| `themes=[]` | 287 | 无主题归属 |

⇒ **66 颗带标签货里，绝大多数挂的是往期主题或压根无主题，对当期 CPPAP 不起作用**。论坛 `44230497234839` 原话：「带了标签却没挂主题的，是类别不在这期里，或者带了 sector 分组」。判定顺序必须是 **当期 `themes` ∧ 带标签 ∧ 质量**。

## 3 为什么必须回滚

- **seq1 摘错对象**：`JjeMlmXA` 是账户里**唯一**命中当期 Nov'26 主题的 alpha。摘掉后当期池从 1 颗变 0 颗，而论坛明确「交满 5 条才够评奖」「摘掉高换手货后条数越多 BC 越高（8→17 条：.103→.200）」。去掉一个 2.66bp 差货的收益，远小于清零当期参赛资格。
- **seq2 补了无效货**：`O07AMoKR` `themes=[]`，补标签进不了当期榜；且会触发本地通道误判（见 §5）。
- 两条都基于「66 颗带标签池＝CPPAP 成分」这个**错误前提**。按「实测 > 推理」纪律，全部回滚，不留半成品。

## 4 最终方案（修正版，回答「如何提高 CPPAP」）

1. **标签治理对当前账户几乎无杠杆**：当期只有 1 颗命中主题，且不足 5 条评奖线。论坛 MZ45384 原话「tag 管理只是权宜之计，只能保护 CPPAP，正道是多交高质量 alpha」——在这里是字面成立。
2. **正道 = 新提交命中当期主题的高质量 alpha**。当期主题是 `GLB/D1 Power Pool Nov'26` ⇒ 需 GLB/D1、**单一类别**（论坛：带 sector 分组会多算一个 PV 类，就不是单类别了）、margin≥10bp（目标 15bp）、TO≤0.15、S/F>1。提交权仍归用户（`ALLOW_ALPHA_SUBMIT=False`）。
3. **提交后 Step 7（规范，不改挖掘闸）**：先看 `themes` 是否命中当期主题 → 命中则**保留平台自动追加的 PP 标签**；只有「命中当期主题 + margin<10bp + TO>0.15」才考虑摘，且一次一条、等约 6h 读 BC/AC 对照。
4. **不要动挖掘闸门**：把 margin≥10bp 写进提交闸与 `MEMORY.md` §8「margin 不是独立信息、两提案已否决」冲突（那条否决针对 OS/CAP 预测，而 CPPAP 是扣成本后组合 IR，口径不同）。**此冲突交用户裁决，未擅自改。**
5. **待办**：`/consultant/boards/power-pool?user=MT38799` 当前 `count=0`，BC/AC 读不到；需下一期开榜或端点参数确认后才有对照基线。已安排一次性复核。

## 5 代码修复（本轮唯一净交付）

| 文件 | 旧行为 | 修正 |
|---|---|---|
| `src/wqb/submit_verdict_core.py::is_ppa_alpha` | `PowerPoolSelected` 子串命中即判 PPA | 只认 `type=PPA` 或 `CH_PPA` 标签；否则平台自动追加标签的 RA alpha 全被误标成 PPA，违反「只认 RA 全闸」 |
| `tools/alpha_properties.py` normalize | 带 PP 标签 ⇒ 产出 `CH_PPA` | 只认已有 `CH_PPA`；避免给补标签的 `CH_REG` 货错打通道 |
| `src/wqb/alpha_properties.py::tag_notes` | 「平台自动追加、按 PPA 政策清除」 | 改为「PP 池成分开关，非通道证据；themes 与标签是两个独立条件」 |

`src/wqb/config.py::merge_failed_items` 与 `submit_alpha.py` 早在 10-27 就用「RA 为下界」绕过过该误判，但 `is_ppa` / `ppa_tag_only` 报告字段与 `ppa_bonus` 仍是错的，本次从根上修。

新增守护测试 `tests/unit/05_submit_quota/test_ppa_channel_vs_pool_tag_20261110.py`。
验证：`05_submit_quota` 四文件 **64 passed**；完整 venv 下 `02_workflow` + 新测试 **42 passed**（系统 Python 缺 `requests` 导致的 7 failed/14 errors 是环境问题，换 venv 即全绿）。

## 6 净状态

- 平台：**零净变化**（66 颗带标签、`JjeMlmXA`/`O07AMoKR` 标签均已恢复）。
- 本地：3 处代码修正 + 1 个测试文件 + 4 步台账 + 主题扫描 + 三队列文件 + 规范/记忆更新。
- 未提交任何 alpha；未执行任何不可逆动作；未改挖掘闸与提交开关。
