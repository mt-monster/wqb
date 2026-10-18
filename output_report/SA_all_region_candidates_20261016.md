# 全 Region SuperAlpha 候选汇总 v2（供挑选）

生成时间：2026-10-16（本地）
数据口径：**全部基于平台真实仿真 + 平台双闸实测**，无本地估算。
本轮**新派发 40 条真实 SUPER 仿真**（c1/c4/c5/c6/c7）+ 14 条复测探针（c3），叠加上一轮 b3/b4/b6，
去重后得到 **18 颗真 PASS**。
统一杠杆：`truncation = 0.02`、`componentActivation = "IS"`、`selection = (1+0*(prod_corr>0)) * (1 - self_corr)`。

> **只挖不提交**：下表全部为**待挑选候选**，未做任何提交动作。提交须你点名。

---

## 一、结论摘要：每 region 一颗最优（按闸余量排序）

| # | region / 档位 | alpha id | IS Sharpe | Fitness | Turnover | SELF | PROD | **闸余量** | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | **GLB / TOPDIV3000** | `npARO63x` | 3.21 | 1.53 | 0.2515 | **0.0000** | 0.5125 | **0.1875** | ⭐ **已提交 ACTIVE**（2026-10-15T20:28:48-04:00，name `GLB_S_10comp_ARO63x`） |
| 2 | DEU / TOP500 | `mLYLEm99` | 2.27 | 1.67 | 0.1667 | 0.6110 | 0.6108 | 0.0890 | 待提交 |
| 3 | USA / TOP1000 | `LL5aX6Y2` | 2.61 | 1.80 | 0.1852 | **0.0000** | 0.6601 | 0.0399 | 待提交（零占用档）<br>安全备选 `JjPlvGVj` IS 1.90 / 余量 **0.0656** |
| 4 | KOR / TOP600 | `58j0z3bk` | 3.50 | 4.73 | 0.0663 | 0.6568 | 0.6706 | 0.0294 | 待提交 |
| 5 | IND / TOP500 | `9qE1kR3o` | 3.53 | 4.27 | 0.0861 | 0.6818 | 0.6816 | 0.0182 | 待提交 |
| 6 | GBR / TOP700 | `LL5a3r6M` | 2.76 | 2.68 | 0.0845 | 0.6540 | 0.6849 | 0.0151 | 待提交 |

**已提交（不占本轮名额）**

| region / 档位 | alpha id | IS Sharpe | SELF | PROD | 提交时间 |
|---|---|---:|---:|---:|---|
| GLB / MINVOL1M | `LL5amzov` | **6.93** | 0.6009 | 0.6101 | 2026-10-14T20:16:36-04:00 ✅ ACTIVE |
| GLB / TOPDIV3000 | `npARO63x` | 3.21 | 0.0000 | 0.5125 | 2026-10-15T20:28:48-04:00 ✅ ACTIVE |
| USA / TOP2000 | `vROw5Rkd` | 4.01 | 0.3383 | 0.6217 | 2026-10-13T19:20:35 ✅ ACTIVE |

> **闸余量** = `0.7 − max(SELF, PROD)`。余量越大，提交后因平台重算而翻车的风险越低。
> **★ 选点原则变了**：本轮实证发现「同一 region/universe 档位只能提交一颗 SA」（同档第二颗 SELF → ~1.0），
> 所以**选 region 不如选「零占用档位」** —— 档位内没有已提交 SA 时 **SELF 恒为 0**，只需过 prod 一闸。

---

## 二、首选候选档案

### ⭐ `npARO63x` — GLB / TOPDIV3000（本轮最优）

| 项目 | 值 |
|---|---|
| 配置 | GLB / **TOPDIV3000** / delay 1 / **STATISTICAL** / **decay 1** / **lim 15** / trunc 0.02 / cp 1 |
| IS Sharpe / Fitness / Turnover | 3.21 / 1.53 / 0.2515 |
| SELF / PROD | **0.0000** / **0.5125** |
| **闸余量** | **0.1875（全场最厚，是第二名的 2.1 倍）** |

**为什么是它**：TOPDIV3000 是**零占用档位**（GLB 已提交的 SA 在 MINVOL1M ×2、TOP3000 ×1，TOPDIV3000 一颗都没有）
⇒ SELF 恒为 0.0000，等于**只剩 prod 一堵墙**，而它 prod 只有 0.5125。
对比同档 decay15 三兄弟全部卡死 `LOW_GLB_EMEA_SHARPE`（见 §四）⇒ **GLB 档的 decay 是硬开关**。

**已穷尽验证（勿再投）**：
- `selectionLimit` 加到 **20 / 25** 后指标**一字不差**（`pwv0Kvn3` / `mLYOVQP9` 均 S 3.21 / F 1.53 / TO 0.2515 / PROD 0.5125）
  ⇒ 该档组件池本身不足 20，`npARO63x` 是**唯一最优解**，加组件数冲不动 IS。
- 同档 decay15 三变体（SECTOR / INDUSTRY / SUBINDUSTRY）**全部**卡 `LOW_GLB_EMEA_SHARPE`。

### `mLYLEm99` — DEU / TOP500（余量第二）

配置 DEU/TOP500/d1/**STATISTICAL**/**decay 1**/lim 10。IS 2.27/F 1.67/TO 0.1667，SELF 0.6110/PROD 0.6108。
DEU 另有 `j2eLrEMj`（STATISTICAL decay15 cp3）余量 0.1063 更厚但 IS 仅 1.87 ⇒ **弃 IS 换余量不划算，选 mLYLEm99**。

### `LL5aX6Y2` — USA / TOP1000（零占用档）

配置 USA/TOP1000/d1/STATISTICAL/decay1/lim15。SELF **0.0000**（USA 已提交 SA 只在 TOP2000/TOP3000）、PROD 0.6601。
同档另有一颗 **`JjPlvGVj`**（SUBINDUSTRY/decay15）IS 1.90 / F 1.56，SELF 0.0000 / **PROD 0.6344，余量 0.0656（厚 1.6 倍）**
⇒ **要稳选 `JjPlvGVj`，要 IS 选 `LL5aX6Y2`**。
（同档 `XgRq8KN0` SECTOR/decay15 卡 `IS_LADDER_SHARPE` 1.49 < 1.58，出局。）

### `58j0z3bk` — KOR / TOP600

配置 KOR/TOP600/d1/**SECTOR**/**decay 15**/lim10。IS 3.50/F **4.73**/TO 0.0663。
KOR 还有 `LL5e1Zq2`（INDUSTRY d15）IS 3.66 更高但余量仅 0.0150 ⇒ **余量是 58j0z3bk 的一半，选 58j0z3bk**。
KOR 已穷尽：INDUSTRY d15 **lim15**（`O0Jexdo7`）把 IS 推到 4.02 / F 5.69，但 corr 直接飙到 **0.7653** 撞墙
⇒ **KOR 加组件数 = 加 IS = 加 corr**，该区已到顶，只有 SECTOR·d15·lim10 一条解。

### `9qE1kR3o` — IND / TOP500

配置 IND/TOP500/d1/**SECTOR**/**decay 15**/cp5/lim10。IS 3.53/F 4.27。
IND 三兄弟里余量最厚的（0.0182 vs O0JPVa7d 0.0157 / qMEr7A2O 0.0130），IS 与最高的 qMEr7A2O 只差 0.04。

### `LL5a3r6M` — GBR / TOP700

配置 GBR/TOP700/d1/**SUBINDUSTRY**/**decay 15**/lim10。IS 2.76/F 2.68。
⚠️ GBR 的 `1YjbKNGX`(0.0041) / `78obm2wO`(0.0028) 余量不足 0.005，**提交后极易翻车，不推荐**。

---

## 三、配方规律（下次开波直接用，别再从零扫）

| region 族 | 赢家配方 | 死因配方 |
|---|---|---|
| **GLB / USA** | **STATISTICAL + decay 1** | decay 15（GLB 卡 EMEA 分区域闸） |
| **KOR / IND / GBR / DEU** | **SECTOR 或 SUBINDUSTRY/INDUSTRY + decay 15** | STATISTICAL（corr 飙到 0.72–0.84） |

- **`combo_power` 是零和杠杆，不是免费午餐**：GBR 上 cp3/cp5 把 SELF 从 0.65 压到 0.57，
  但 **PROD 反向抬到 0.6959 / 0.6972**（余量掉到 <0.005）。KOR 的 cp3/cp5 直接 0.7226/0.7282 撞墙。
  ⇒ **调 cp 必须同时看 SELF 和 PROD 两头**。
- **IS 越高 corr 越高，这个两难本轮再次验证**：KOR/USA3k/IND/GBR 的 STATISTICAL·decay1 分别冲到
  IS 4.87 / 4.73 / 5.39 / 4.25，corr 全部 0.74–0.84 撞墙。**过闸必须牺牲 IS**。

---

## 四、★ 零占用档位实测（本轮决定性发现）

| 档位 | alpha | SELF | PROD | 结果 |
|---|---|---:|---:|---|
| USA / TOP500 | `1YjvdNAR` | **0.0000** | 0.6794 | ❌ `LOW_SHARPE` 1.41 < 1.58 |
| USA / TOP200 | `RRAX8lP1` | **0.0000** | 0.7412 | ❌ IS 0.80 / F 0.53 |
| USA / TOPSP500 | `VkdnPRYw` | **0.0000** | 0.7189 | ❌ IS 1.28 / F 0.90 |
| GLB / MINVOL10M | `zqraRwZO` | **0.0000** | 0.8210 | ❌ PROD 撞墙 |
| GLB / TOPDIV3000 | `npARO63x` | **0.0000** | **0.5125** | ✅ **过闸** |

**结论**：零占用 ⇒ SELF 恒 0（5/5 全中，假设完全成立）。
但**零占用只保 SELF、救不了 IS 和 PROD** —— 三个小 universe 的组件质量太差，IS 直接不过 1.58。
⇒ **零占用是必要条件，不是充分条件**；真正稀缺的是「零占用 + 组件质量够」的组合，本轮只有 GLB/TOPDIV3000 命中。

---

## 五、Region 可用性定案（勿再投）

| region | 结论 | 实测证据 |
|---|---|---|
| GLB / USA / KOR / IND / DEU / GBR | ✅ 可建 | 各有 ≥1 颗 PASS |
| **EUR** | ❌ **判死** | TOPCS1600 ×2、TOP2500、TOP1200 **共 4 次** `At least 10 component alphas are required`（池显示 85 颗也没用） |
| **MEA** | ❌ **平台不支持** | HTTP 400 `Region MEA is not available.` + `Neutralization STATISTICAL is not available ... region MEA` |
| **ASI** | ❌ | MINVOL1M `At least 10 component alphas` |
| **HKG** | ❌ | TOP800 `At least 10 component alphas` |
| JPN / TWN / CHN / AMR | ❌ | 上一轮已判死 |

**★ 组件池计数不可信**：`sa_pool_review.py` 统计的是**我名下**的 REGULAR alpha，
而 GLB/TOPDIV3000 我只有 **n=1** 颗，平台照样选出 10+ 组件建成 `npARO63x`。
⇒ **能不能建只能 POST 一次实测**，池计数只能看相对拥挤度。
（另：UNSUBMITTED 分页 hard_cap=1000 会截断，同一脚本两次跑同档计数会漂。）

---

## 六、撞墙档案（勿重复投）

| alpha | 档位 | IS Sharpe | SELF | PROD | 死因 |
|---|---|---:|---:|---:|---|
| `VkdjR3JA` | GLB/MINVOL1M | **6.89** | **0.9987** | 0.6091 | 同档第二颗，SELF 爆表 |
| `rKdmGg1j` | KOR/TOP600 | **4.87** | 0.7400 | 0.7400 | 双闸同撞 |
| `Vkdjzndb` | USA/TOP3000 | **4.73** | 0.7418 | 0.7422 | corr + `LOW_SUB_UNIVERSE_SHARPE` 2.00<2.05 |
| `omo5Eqzl` | IND/TOP500 | **5.39** | 0.8316 | 0.8316 | corr 严重 |
| `E5VWmNXK` | GBR/TOP700 | 4.25 | 0.8413 | 0.8412 | corr 严重 |
| `9qEorzmK` / `78oO1bq1` / `leMxlzAN` | GLB/TOPDIV3000 | 2.70 / 2.67 / 2.65 | 0.0 | 0.62 | `LOW_GLB_EMEA_SHARPE` 0.91/0.85/0.89 < 1 |
| `gJWvMd1M` / `O0JeZ6mv` | IND/TOP500 | 4.16 / 4.17 | 0.7003 / 0.7010 | 0.7005 / 0.7011 | **差 0.0005 撞墙**（STATISTICAL d15 cp3/cp5） |
| `O0JeZGnp` | KOR/TOP600 | 3.77 | 0.7301 | 0.7299 | SUBINDUSTRY 撞墙 |
| `j2eRV2pe` | DEU/TOP500 | 2.32 | 0.7530 | 0.7529 | SECTOR 撞墙 |
| `1Yjvdllm` | USA/TOP3000 | 3.24 | 0.7209 | 0.7707 | SUBINDUSTRY 撞墙 |
| `O0Jexdo7` | KOR/TOP600 | 4.02 | 0.7655 | 0.7653 | INDUSTRY d15 **lim15**，IS 涨但 corr 跟着涨 |
| `XgRq8KN0` | USA/TOP1000 | 1.84 | 0.0000 | 0.6782 | `IS_LADDER_SHARPE` 1.49 < 1.58 |

---

## 七、18 颗真 PASS 全表（含备选，按闸余量排序）

| alpha | 档位 | 配方 | IS S | F | TO | SELF | PROD | 余量 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `npARO63x` | GLB/TOPDIV3000 | STAT d1 lim15 | 3.21 | 1.53 | 0.2515 | 0.0000 | 0.5125 | **0.1875** |
| `j2eLrEMj` | DEU/TOP500 | STAT d15 cp3 | 1.87 | 1.44 | 0.1031 | 0.5937 | 0.5935 | 0.1063 |
| `LL5amzov` | GLB/MINVOL1M | STAT d1 | **6.93** | 4.18 | 0.2404 | 0.6009 | 0.6101 | 0.0899 ✅已提交 |
| `mLYLEm99` | DEU/TOP500 | STAT d1 | 2.27 | 1.67 | 0.1667 | 0.6110 | 0.6108 | 0.0890 |
| `kqJrL9ld` | DEU/TOP500 | STAT d1 lim15 | 2.27 | 1.67 | 0.1667 | 0.6110 | 0.6108 | 0.0890 |
| `kqJrvP0g` | GLB/TOP3000 | STAT d1 | 3.61 | 1.65 | 0.2566 | 0.6207 | 0.6196 | 0.0793 |
| `vROw5Rkd` | USA/TOP2000 | STAT d1 lim15 | 4.01 | 3.33 | 0.1706 | 0.3383 | 0.6217 | 0.0783 ✅已提交 |
| `JjPlvGVj` | USA/TOP1000 | SUBINDUSTRY d15 | 1.90 | 1.56 | 0.0754 | 0.0000 | 0.6344 | 0.0656 |
| `LL5aX6Y2` | USA/TOP1000 | STAT d1 lim15 | 2.61 | 1.80 | 0.1852 | 0.0000 | 0.6601 | 0.0399 |
| `58j0z3bk` | KOR/TOP600 | SECTOR d15 | 3.50 | **4.73** | 0.0663 | 0.6568 | 0.6706 | 0.0294 |
| `88v9P5LV` | KOR/TOP600 | SECTOR d18 | 3.44 | 4.61 | 0.0624 | 0.6532 | 0.6736 | 0.0264 |
| `9qE1kR3o` | IND/TOP500 | SECTOR d15 cp5 | 3.53 | 4.27 | 0.0861 | 0.6818 | 0.6816 | 0.0182 |
| `O0JPVa7d` | IND/TOP500 | SECTOR d15 cp3 | 3.55 | 4.30 | 0.0854 | 0.6843 | 0.6841 | 0.0157 |
| `LL5a3r6M` | GBR/TOP700 | SUBINDUSTRY d15 | 2.76 | 2.68 | 0.0845 | 0.6540 | 0.6849 | 0.0151 |
| `LL5e1Zq2` | KOR/TOP600 | INDUSTRY d15 | 3.66 | 4.73 | 0.0687 | 0.6850 | 0.6850 | 0.0150 |
| `qMEr7A2O` | IND/TOP500 | SECTOR d15 | 3.57 | 4.34 | 0.0839 | 0.6870 | 0.6867 | 0.0130 |
| `1YjbKNGX` | GBR/TOP700 | SECTOR d15 cp3 | 2.82 | 2.92 | 0.0810 | 0.5691 | 0.6959 | 0.0041 ⚠️ |
| `78obm2wO` | GBR/TOP700 | SECTOR d15 cp5 | 2.81 | 2.90 | 0.0812 | 0.5660 | 0.6972 | 0.0028 ⚠️ |

> 另有 `pwv0Kvn3`(lim20) / `mLYOVQP9`(lim25) 两颗与 `npARO63x` 指标**完全相同**（同档同配方，组件池不足 20 导致 limit 失效），
> 属重复解，不单列。

---

## 八、产物路径

- 批次明细：`C:\Users\MENGTAO\wqb-scripts\c1\ c3\ c4\ c5\ c6\ c7\`（`res*.jsonl` + `run.log`）
- 组件池扫描：`C:\Users\MENGTAO\wqb-scripts\c1\pool_review_v2.txt`
- 驱动脚本：`sa_run.py`（耐心轮询 90×10s，解决 `super_build.py select` 的假失败）、`sa_pool_review.py`、`sa_settings.py`
- 记忆：`D:\coding\traeCN_project\wqb\.workbuddy\memory\2026-10-16.md`
