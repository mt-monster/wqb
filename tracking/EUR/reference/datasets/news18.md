# news18 · EUR / TOPCS1600 / D1 字段画像（Ravenpack）

> 类型 VECTOR · 124 字段 · cov 0.36–1.0 · category = **news**（×1.3）· αC 655（拥挤）
> 采集：2026-11-06
> 来源：论坛帖 `43541109631895`（注意力密度模板 EUR 验证 S=1.60）/ `40847481080087`（nip × ts_corr × FAST）

## 0. 关键字段（按模板可用性）

| 字段 | cov | αC | 用途 |
|---|---|---|---|
| `nws18_sse` | .757 | 0 | 实体事件连续情绪 −1..1；可 `vec_count` 作密度 |
| `nws18_multiple_comp_ssc` | .991 | 4 | 多技术情绪；论坛原字段近亲 |
| `multi_entity_story_event_count` | .991 | 3 | **直接事件计数**（已是密度） |
| `nws18_multiple_comp_nip` | .991 | 5 | 新闻冲击投影——论坛 nip 模板主字段 |
| `nws18_multiple_comp_relevance` | .991 | 8 | 相关性 0–100——论坛 relevance 加权主字段 |
| `nws18_event_similarity_days` | .817 | 0 | 新颖度（天） |
| `nws18_mltpl_cmp_event_simildays` | 1.0 | 5 | 多实体新颖度 |
| `nws18_multiple_comp_qmb` | 1.0 | **93** | 社论情绪（拥挤） |

## 1. 机制

1. **注意力密度反转**（Da et al. 2011 → PW58059 EUR 验证）：`-ts_rank(ts_mean(vec_count(F), 60), 252)` @ FAST/decay15
2. **nip × 相关性**（MY82844）：`ts_corr(nip, returns, d)` @ FAST——待第二波

## 2. 实测

**密度模板 @ TOPCS1600（已终态,multisim `1sBrvy3v74Yu9Wd1b8rTqYLk`,FAST/decay15）——几乎归零**：

| 字段 | alpha id | S | F | 2Y | sub | robust |
|---|---|---|---|---|---|---|
| `nws18_sse` | `d5W3EPmv` | **0.66** | 0.22 | −0.04 | 0.25 | 0.25 |
| `nws18_multiple_comp_ssc` | `MPYeK288` | 0.06 | 0.01 | −1.94 | −0.01 | 0.03 |
| `multi_entity_story_event_count` | `E568g2aL` | 0.06 | 0.01 | −1.94 | −0.01 | 0.03 |
| `nws18_multiple_comp_nip` | `KPJ5X2wj` | 0.06 | 0.01 | −1.94 | −0.01 | 0.03 |
| `nws18_multiple_comp_relevance` | `akKQAgWx` | 0.06 | 0.01 | −1.94 | −0.01 | 0.03 |

**归因**：后四条读数逐位相同（同一天有多实体新闻则全非空 → `vec_count` 退化成 0/1）。论坛原版用 **TOP2500** 跑出 EUR S=1.60——宇宙差异可能是关键；已按论坛原设置（TOP2500）重提。另提 nip × ts_corr 模板（帖 `40847481080087`）。

**★★ 论坛原字段原设置复现成功（已终态,multisim `4hAAJB1dm5dr9etvFuhve1j`,TOP2500/FAST/decay15）**：

| 变体 | alpha id | S | F | TO | 2Y | sub | 卡闸 |
|---|---|---|---|---|---|---|---|
| 论坛原版 `group_neutralize(...sse..., densify(market))` | `akKQNQv9` | **1.61 PASS** | 0.76 | .0770 | 1.03 | 1.04 PASS | F/2Y |
| 裸 `-ts_rank(...sse...)` | `xAr2e2ag` | 1.59 | 0.74 | .0769 | 1.01 | 1.03 | F/2Y |
| + `ts_target_tvr_decay(target_tvr=0.05)` | `O0AMnMvp` | **1.60** | 0.75 | **.0614** | **1.21** | 1.00 | F/2Y |

与论坛帖 EUR 表（S=1.60/F=0.75）**逐位吻合**。字段必须是 `nws18_multiple_comp_sse`（其他字段 `vec_count` 退化）；宇宙必须 TOP2500（TOPCS1600 归零）。

**姊妹字段 @ TOP2500（multisim `1JQSgoaGk5hY8Iy5D59pnmd`）**：`nws18_sse` S=1.46–1.47；`ssc`/`nip` 密度 S=0.89——均弱于 `multiple_comp_sse`。

**nip × ts_corr（multisim `1S7D5qbpt582aDT3tuBJE5K`）**：最好 S=0.69（66d），且触发 PV+NEWS 双塔（含 returns）——弱且吃组腿预算，归档。

**当前缺口**：F 0.75→1.0（需 S≈1.75 或 returns↑）、2Y 1.21→1.58。已提交窗口 44/88 + 包装栈 + signed_power 杠杆批；另提 SLOW_AND_FAST 对照。

**杠杆批结果（已终态）——★★ SLOW_AND_FAST 修好 2Y，只剩 F**：

| 变体 | alpha id | neut | S | F | 2Y | sub | 卡闸 |
|---|---|---|---|---|---|---|---|
| tvr_decay 基线 | `O0AMnMvp` | FAST | 1.60 | 0.75 | 1.21 | 1.00 | F/2Y |
| 窗口 44 | `npve3XE8` | FAST | 1.48 | 0.68 | 1.10 | 0.96 | S/F/2Y |
| 窗口 88 | `vR1pdoQG` | FAST | 1.40 | 0.62 | 0.88 | 0.78 | S/F/2Y |
| +rank(group_scale) | `KPJ5k2Wj` | FAST | 1.54 | 0.70 | **1.46** | 0.91 | S/F/2Y |
| +signed_power(1.5) | `leA5rNo7` | FAST | 1.57 | 0.75 | 1.16 | 0.98 | S(0.01)/F/2Y |
| **tvr_decay @ SLOW_AND_FAST** | **`78Lvd8EZ`** | **SLOW_AND_FAST** | **1.58 PASS** | 0.71 | **1.72 PASS** | 0.87 | **仅 F** |
| +rank(group_scale) @ S&F | `KPJ5LPal` | S&F | 1.53 | 0.67 | **1.97** | 0.77 FAIL | S/F/sub |

**归因**：① 60d 仍是窗口峰（44/88 更差，与论坛一致）。② **SLOW_AND_FAST 把 2Y 从 1.21 抬到 1.72**——论坛「慢信号用 FAST」在本区不成立，S&F 同时保留慢轴信息。③ 包装栈抬 2Y 但伤 S/sub。④ Mode B：`78Lvd8EZ` 命中旁路 E（2Y≥1.2 ∧ S≥0.8），**eligible=true**。⑤ 已提交 S&F × signed_power / 分位窗 126/504 冲 F。

**跨机制互相关（`compute_mutual_correlation`, threshold 0.5）——与 insiders 席位正交**：

| | `leA5JeP7`（insiders） | `78Lvd8EZ`（news 密度） | `O0AMnMvp`（FAST） |
|---|---|---|---|
| `leA5JeP7` | 1 | **0.028** | 0.006 |
| `78Lvd8EZ` | | 1 | 0.896 |

最大互不相关子集 = `{leA5JeP7, 78Lvd8EZ}`（size=2）。**战役双席锁定**：insiders 高管显著金额 + news 注意力密度，机制正交、塔位不同（INSIDERS×1.1 / NEWS×1.3）。提交待用户确认。

**S&F 加压终态（multisim `3MH7XCdZ54gzaWiYnczru89`）——F 结构性天花板确认**：

| 变体 | alpha id | S | F | 2Y | returns |
|---|---|---|---|---|---|
| signed_power 1.5 | `xAr2xPJb` | 1.54 | 0.71 | 1.65 | .0262 |
| signed_power 2 | `E568wg9L` | 1.49 | 0.69 | 1.57 | .0270 |
| 分位窗 504 | `QPvNa2ww` | 1.58 | 0.71 | 1.27 | .0249 |
| 分位窗 126 | `WjOopNEk` | 1.33 | 0.54 | 1.73 | .0209 |

闭式验算：S=1.58 × √(0.025/0.125) ≈ 0.71，与实测吻合。**F=1.0 需 returns≈0.05 或 S≈2.2**——本机制 returns 天花板 ~0.027，RA 硬闸 F 不可达；Mode B 旁路 E 仍成立。席位定稿 `78Lvd8EZ`（S&F tvr_decay，2Y 1.72 最优结构）。

**relevance 加权密度（已终态,multisim `2VZMpgdzh5ekbRGTffkc8Sj`）——S 抬到 1.64，2Y 压线 1.57**：

| 变体 | alpha id | S | F | 2Y | sub |
|---|---|---|---|---|---|
| relevance 水平密度 | `j2YP0WkE` | 0.16 | 0.02 | 0.35 | 0.06 | 无信号 |
| **sse×relevance 加权密度** | **`xAr2k97l`** | **1.64 PASS** | 0.75 | **1.57（差 0.01）** | 0.85 |
| tvr=0.08 | `YP1E0nVq` | 1.56 | 0.69 | 1.47 | 0.82 |
| tvr=0.03 | `E568EYjR` | 0.96 | 0.34 | 0.71 | 0.48 | 过压 |

**归因**：`vec_count(sse) × vec_avg(relevance)` 是论坛「relevance 加权」在密度模板上的正确落地——比裸 sse 多 +0.06 S，2Y 从 1.72→1.57（略降）。tvr=0.05 是甜点，0.03 过压崩盘。已提交 signed_power / 窗 66 / tvr=0.04 冲 2Y 过闸。

**★★ 加压批终态（multisim `2smjaFaon4TPbwAPEDDw4FT`）——窗口 66 是新峰，`N1NJRNWL` 升级为 news 席位代表**：

| 变体 | alpha id | S | F | 2Y | sub（闸） |
|---|---|---|---|---|---|
| signed_power 1.5 | `1YNlzNVm` | 1.65 | 0.78 | 1.55 | 0.80 FAIL |
| **sse×relevance 窗 66** | **`N1NJRNWL`** | **1.73 PASS** | **0.81** | **1.69 PASS** | 0.86 FAIL（0.90） |
| tvr=0.04 | `zq32R3QK` | 1.43 | 0.61 | 1.45 | 0.73 FAIL |
| institutions6 buyers @TOP2500 | `QPvN9vq5` | 0.36 | 0.08 | −0.54 | 0.43 |

**归因**：① 平滑窗 66（季）优于 60——注意力积累周期在 EUR 是完整季度而非「2 个月+2 周」；S +0.15、2Y 1.57→1.69 过闸。② sub 0.86 vs 闸 0.90 差 0.04——TOP2500 老问题。③ **Mode B 判定：`N1NJRNWL` 主闸直接通过（S 1.73≥1.25 ∧ F 0.81≥0.8），eligible=true，verdict=main_gate**——比 `78Lvd8EZ`（旁路 E）更强。④ 互相关：与 insiders 席 0.024 正交；与 `78Lvd8EZ` 0.924 同机制（60d vs 66d 变体），**news 席位归属 `N1NJRNWL`**。⑤ institutions6 buyers @TOP2500 反而崩（0.36 vs TOPCS1600 0.88）——机构字段吃窄宇宙，与 news 密度相反，再次验证 MATRIX 宇宙二分法需按数据集实测。

**战役席位现状（3 席，全部 Mode B eligible，互相关 ≤0.03）**：

| 席位 | alpha | 数据集/塔 | S | F | 2Y | Mode B |
|---|---|---|---|---|---|---|
| 1 | `leA5JeP7` | insider_agg_matrix / INSIDERS ×1.1 | 1.76 | 0.94 | 2.32 | main_gate |
| 2 | `N1NJRNWL` | news18 / NEWS ×1.3 | 1.73 | 0.81 | 1.69 | main_gate |
| 3 | `78Lvd8EZ` | news18 同机制 60d 变体（与席 2 互斥，备用） | 1.58 | 0.71 | 1.72 | bypass_E |

**席位再精修（multisim `1YXE814vk4jh9ykI3xJcD0Y`）——`ZYQdErnd`（+sector 包装栈）只剩 LOW_FITNESS 一道**：

| 变体 | alpha id | S | F | 2Y | sub | 卡闸 |
|---|---|---|---|---|---|---|
| 基线 66/252 | `N1NJRNWL` | 1.73 | 0.81 | 1.69 | 0.86 FAIL | F/sub |
| 分位窗 504 | `zq32NOmO` | 1.71 | 0.79 | 1.36 | 0.91 | F/2Y |
| **+rank(group_scale(·,sector))** | **`ZYQdErnd`** | 1.68 | 0.76 | **1.81 PASS** | **0.90 PASS（压线）** | **仅 F 0.76** |
| qcm×relevance | `58EApMOX` | 1.57 | 0.69 | 1.20 | 0.80 | 全弱于 sse |

**归因**：sector 包装栈把 sub 0.86→0.90 压线 PASS、2Y 1.69→1.81——「先修结构后加强度」顺序在 news 席同样成立,代价是 S −0.05。qcm 弱于 sse（供应商情绪算法差异）。**news 席位代表切换为 `ZYQdErnd`（结构最干净,仅 F一道）,`N1NJRNWL` 备用（S/F 更高但 sub FAIL）**——两者互相关必然 >0.9,只能选一。

**fund_holdings_panel 首探针（multisim `32UNtU69s4w8c1e1nYPSULm`）——全噪声**：

| 变体 | alpha id | S |
|---|---|---|
| boundary_total 密度 | `leA5WrW7` | −0.12 |
| stable_boundary 21d | `9qxdpJpe` | −0.12（逐位同上——字段冗余） |
| top_weighted_account | `WjOoA97k` | −0.20 |
| reverse HHI holdings | `pwdMN8j6` | 0.48 |
| holder_account_total | `A1VrGkle` | −0.20（与 top_weighted 逐位同） |

**归因**：`vec_count` 在本集退化为 0/1（日更非稀疏事件）；HHI 反向 0.48 是唯一有读数的——「机构持仓集中度异常低→后续跑赢」的分散化溢价,但强度不足。**fund_holdings_panel 按快判死归档（5 探针 max |S|=0.48 <0.5）**;institutions 类别两集（institutions6 max 0.95 / fund_holdings_panel max 0.48）均未达闸,该塔转出。

**news 席位互相关定稿（2026-11-07）**：`ZYQdErnd` vs `N1NJRNWL` 互相关 **0.989**（同一信号的不同包装）——只留一席。最大互不相关子集 = `{leA5JeP7, ZYQdErnd}`。**席位定稿**：

| 席位 | alpha | 塔 | S | F | 2Y | sub | Mode B | 剩余卡点 |
|---|---|---|---|---|---|---|---|---|
| 1 | `leA5JeP7` | INSIDERS ×1.1 | 1.76 | 0.94 | 2.32 | 1.07 | main_gate | 无（RA 全 warning 级） |
| 2 | `ZYQdErnd` | NEWS ×1.3 | 1.68 | 0.76 | 1.81 | 0.90 | 旁路 E | RA 硬闸仅 F 0.76 |

两席互相关 0.023,机制正交。提交决策留给用户（Mode B 旁路 E 的 `mode_b_action` 载明：补短期腿或换中性化域提 IS）。

**F 终局分析**：F=1.0 需 S≈2.23（returns 0.026 闭式解）或 returns≈0.043（S=1.68 时）。本机制 returns 天花板 0.026–0.028,S 峰 1.73——**RA 硬闸 F 在本机制结构性不可达**（与 insiders 席 F 0.94 同为 warning 级）。交付口径以 Mode B 为主闸,RA warning 缺口如实记录。
