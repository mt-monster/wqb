# 候选 Alpha 可提交性盘点 · 整合报告（2026-10-05）

> 工具链：`tools/submit_inventory.py`（RA / REGULAR）+ `tools/probe_sa_candidates.py`（SA / SUPER）
> 口径：只盘点、不提交。全局 `wqb.config.ALLOW_ALPHA_SUBMIT=False`（未触碰）；配额 REGULAR 1/天/区、SUPER 1/天/区，提交权归用户。
> RA 数据快照 `results/submit_inventory_20261005-214030.json`（`--no-csv`，**无 CSV**，退出码 0）；SA 数据源自本地缓存 `results/sa_probe_cache.json`（种子 = `sa_candidates_20261005-203751.json`，generated_at 20:22:50，TTL 6h 内命中秒回；本日另有一次 21:20 起跑的全量探针 `sa_candidates_20261005-213329.json`，见 §6d）。

---

## 0. 本次执行摘要

| 项 | 结果 |
|---|---|
| RA 七分类 | SUBMIT_NOW **7** / THIN_MARGIN **2** / PROD_WALL 0 / HARD_BLOCKED 0 / ALREADY_SUBMITTED 0 / CORR_UNKNOWN 0 / ERROR 0 |
| SA 组件池 | GO 6 区（USA/IND/KOR/GBR/MEA/GLB）· BLOCKED 4 区（DEU/EUR/ASI/HKG） |
| SA 总量 | 47 颗 SUPER（21 ACTIVE + 26 未提交候选） |
| 相关性限流 | **无**（RA 全走 checkpoint 复用，零 live 调用；SA 走缓存，零平台翻页） |
| 台账盘前=盘后 | 是（READY=9 无变动） |
| 状态变化 | 相对上一份 `214013`（21:40:13）**零变化**（仅 `generated_at`/`started_at` 时间戳不同）；自 19:53 起 6 轮（195357/211903/212043/213809/214013/214030）桶计数与关键字段全同 |
| 产物 | `results/submit_inventory_20261005-214030.json`（`--no-csv` 生效，同时段**未生成任何 .csv**）+ `results/sa_candidates_20261005-214043.json` + 本报告 |
| 退出码 | RA=0，SA=0（缓存命中 ~2.4s） |

**SA 探针缓存改进（本日已落地）**：脚本原本每次都重翻平台（~14min）却从不复用历史文件。现已加固定主缓存 `results/sa_probe_cache.json`（**TTL 默认 6h**，env `SA_PROBE_CACHE_TTL_HOURS` 可覆盖；`--cache-ttl-hours` 临时覆盖）+ `--refresh` 强制刷新 + 首次无主缓存自动提升最近 TTL 内全量探针为缓存。本日验证：14min → **2.4s**，且数据仅在提交/新建时变化（盘点全程只读），安全。提交/新建 SA 后须 `--refresh` 才能拿新状态。

---

## 1. RA（REGULAR）七分类计数

| 桶 | 计数 | 含义 |
|---|---|---|
| SUBMIT_NOW | **7** | 全闸通过且 prod/self 余量充足，可提交 |
| THIN_MARGIN | **2** | 全闸通过但 prod 余量 < 0.03，建议不提 |
| PROD_WALL | 0 | 撞 prod 相关性墙（≥0.7） |
| HARD_BLOCKED | 0 | RA/Failed-count 硬闸 |
| ALREADY_SUBMITTED | 0 | 已提交 |
| CORR_UNKNOWN | 0 | 相关性缺失（未能实测） |
| ERROR | 0 | 取数/解析错误 |
| **TOTAL** | **9** | submit_ready READY 行全部入列 |

⚠ 默认口径只覆盖 `submit_ready` 入队候选（77 颗 PROD_BLOCKED 不在内，需 `--include-prod-blocked --skip-corr` 另跑）。GBR 游离 UNSUBMITTED 中仍有未入队项（见 §6）。

---

## 2. SUBMIT_NOW 清单（7 颗）

| alpha_id | region | tower | prod | self | min余量(prod) | sharpe | fitness | 2Y | turnover |
|---|---|---|---|---|---|---|---|---|---|
| O08EjLVp | USA | USA/D1/MODEL ×1.3 | 0.5626 | 0.1301 | 0.1374 | 2.45 | 1.55 | 2.55 | 0.1511 |
| N1VnJjXg | EUR | EUR/D1/MODEL ×1.3 | 0.5378 | 0.1954 | 0.1622 | 1.75 | 1.17 | None⚠ | 0.0411 |
| QPK26lQX | GBR | GBR/D1/MODEL ×1.6 | 0.5385 | 0.4951 | 0.1615 | 1.68 | 1.03 | None⚠ | 0.123 |
| j289xaxO | GBR | GBR/D1/MODEL ×1.6 | 0.5380 | 0.4839 | 0.1620 | 1.66 | 1.00 | None⚠ | 0.1282 |
| JjQbYdGW | GBR | GBR/D1/MODEL ×1.6 | 0.6072 | 0.3620 | 0.0928 | 1.62 | 1.00 | None⚠ | 0.1312 |
| omWVV6Y2 | GBR | GBR/D1/MODEL ×1.6 | 0.6579 | 0.5007 | 0.0421 | 1.62 | 1.02 | None⚠ | 0.1283 |
| QPKErLvX | GBR | GBR/D1/MODEL ×1.6 | 0.6593 | 0.5015 | 0.0407 | 1.59 | 1.00 | None⚠ | 0.1284 |

`min余量` = 0.7 − prod（prod 余量）。self 余量 = 0.7 − self（均充足）。

---

## 3. THIN_MARGIN 清单（2 颗，建议不提）

| alpha_id | region | tower | prod | self | min余量(prod) | sharpe | fitness | 2Y |
|---|---|---|---|---|---|---|---|---|
| RR6NOlma | GBR | GBR/D1/MODEL ×1.6 | 0.6861 | 0.6348 | **0.0139** | 1.70 | 1.02 | None⚠ |
| LLZ6wZO2 | KOR | KOR/D1/FUNDAMENTAL ×1.6 | 0.6762 | 0.6760 | **0.0238** | 1.99 | 1.53 | 2.24 |

两颗粒 prod 余量均 < 0.03（贴 0.7 墙），提交性价比低，**建议不提**。

---

## 4. RA 塔位（towers）指向

全部 9 颗均指向金字塔 **MODEL** 类塔（D1 档）。倍率：

| 塔 | 倍率 | 命中 alpha |
|---|---|---|
| USA/D1/MODEL | ×1.3 | O08EjLVp |
| EUR/D1/MODEL | ×1.3 | N1VnJjXg |
| GBR/D1/MODEL | ×1.6 | JjQbYdGW / QPK26lQX / QPKErLvX / j289xaxO / omWVV6Y2 / RR6NOlma |
| KOR/D1/FUNDAMENTAL | ×1.6 | LLZ6wZO2 |

`tower_dataset` 字段本批全为 null（塔位取自 submit_ready 台账，未回填具体塔数据集名）。GBR 倍率 1.6 高于 USA/EUR 的 1.3，提交 GBR 候选的塔收益更优。

---

## 5. RA 汇总（按 sharpe 降序 · 按 region 分组）

### 5a. 全局按 sharpe 排名

| rank | region | alpha_id | tower | mult | sharpe | fitness | 2Y | turnover | prod | self | min_margin | bucket | tower_dataset |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | USA | O08EjLVp | USA/D1/MODEL | 1.3 | 2.45 | 1.55 | 2.55 | 0.1511 | 0.5626 | 0.1301 | 0.1374 | SUBMIT_NOW | （空） |
| 2 | KOR | LLZ6wZO2 | KOR/D1/FUNDAMENTAL | 1.6 | 1.99 | 1.53 | 2.24 | 0.1440 | 0.6762 | 0.6760 | 0.0238 | THIN_MARGIN | （空） |
| 3 | EUR | N1VnJjXg | EUR/D1/MODEL | 1.3 | 1.75 | 1.17 | None | 0.0411 | 0.5378 | 0.1954 | 0.1622 | SUBMIT_NOW | （空） |
| 4 | GBR | RR6NOlma | GBR/D1/MODEL | 1.6 | 1.70 | 1.02 | None | 0.1224 | 0.6861 | 0.6348 | 0.0139 | THIN_MARGIN | （空） |
| 5 | GBR | QPK26lQX | GBR/D1/MODEL | 1.6 | 1.68 | 1.03 | None | 0.1230 | 0.5385 | 0.4951 | 0.1615 | SUBMIT_NOW | （空） |
| 6 | GBR | j289xaxO | GBR/D1/MODEL | 1.6 | 1.66 | 1.00 | None | 0.1282 | 0.5380 | 0.4839 | 0.1620 | SUBMIT_NOW | （空） |
| 7 | GBR | JjQbYdGW | GBR/D1/MODEL | 1.6 | 1.62 | 1.00 | None | 0.1312 | 0.6072 | 0.3620 | 0.0928 | SUBMIT_NOW | （空） |
| 8 | GBR | omWVV6Y2 | GBR/D1/MODEL | 1.6 | 1.62 | 1.02 | None | 0.1283 | 0.6579 | 0.5007 | 0.0421 | SUBMIT_NOW | （空） |
| 9 | GBR | QPKErLvX | GBR/D1/MODEL | 1.6 | 1.59 | 1.00 | None | 0.1284 | 0.6593 | 0.5015 | 0.0407 | SUBMIT_NOW | （空） |

`tower_dataset` 本批全为 `null`（塔位取自 `submit_ready` 台账 + 平台 `get_pyramid_multipliers`，均未回填塔数据集名；塔名已含 `region/delay/family`）。

### 5b. 按 region 分组（含 rank_in_region）

**USA（1 颗）**
| region | rank_in_region | alpha_id | tower | tower_multiplier | sharpe | fitness | two_year | turnover | prod | self | min_margin | bucket | tower_dataset |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| USA | 1 | O08EjLVp | USA/D1/MODEL | 1.3 | 2.45 | 1.55 | 2.55 | 0.1511 | 0.5626 | 0.1301 | 0.1374 | SUBMIT_NOW | （空） |

**EUR（1 颗）**
| region | rank_in_region | alpha_id | tower | tower_multiplier | sharpe | fitness | two_year | turnover | prod | self | min_margin | bucket | tower_dataset |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EUR | 1 | N1VnJjXg | EUR/D1/MODEL | 1.3 | 1.75 | 1.17 | None | 0.0411 | 0.5378 | 0.1954 | 0.1622 | SUBMIT_NOW | （空） |

**KOR（1 颗）**
| region | rank_in_region | alpha_id | tower | tower_multiplier | sharpe | fitness | two_year | turnover | prod | self | min_margin | bucket | tower_dataset |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KOR | 1 | LLZ6wZO2 | KOR/D1/FUNDAMENTAL | 1.6 | 1.99 | 1.53 | 2.24 | 0.1440 | 0.6762 | 0.6760 | 0.0238 | THIN_MARGIN | （空） |

**GBR（6 颗）**
| region | rank_in_region | alpha_id | tower | tower_multiplier | sharpe | fitness | two_year | turnover | prod | self | min_margin | bucket | tower_dataset |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GBR | 1 | RR6NOlma | GBR/D1/MODEL | 1.6 | 1.70 | 1.02 | None | 0.1224 | 0.6861 | 0.6348 | 0.0139 | THIN_MARGIN | （空） |
| GBR | 2 | QPK26lQX | GBR/D1/MODEL | 1.6 | 1.68 | 1.03 | None | 0.1230 | 0.5385 | 0.4951 | 0.1615 | SUBMIT_NOW | （空） |
| GBR | 3 | j289xaxO | GBR/D1/MODEL | 1.6 | 1.66 | 1.00 | None | 0.1282 | 0.5380 | 0.4839 | 0.1620 | SUBMIT_NOW | （空） |
| GBR | 4 | JjQbYdGW | GBR/D1/MODEL | 1.6 | 1.62 | 1.00 | None | 0.1312 | 0.6072 | 0.3620 | 0.0928 | SUBMIT_NOW | （空） |
| GBR | 5 | omWVV6Y2 | GBR/D1/MODEL | 1.6 | 1.62 | 1.02 | None | 0.1283 | 0.6579 | 0.5007 | 0.0421 | SUBMIT_NOW | （空） |
| GBR | 6 | QPKErLvX | GBR/D1/MODEL | 1.6 | 1.59 | 1.00 | None | 0.1284 | 0.6593 | 0.5015 | 0.0407 | SUBMIT_NOW | （空） |

> `region` 单列于行内、`rank_in_region` 为组内 sharpe 降序名次；`prod` 单列（不与 self 合并）。

---

## 6. SA（SUPER）情况

### 6a. 组件池 eligibility 分区（硬前置 ≥10 颗 ACTIVE 已提交 REGULAR/区）

> 两种「active」口径（**本次新增 `tools/verify_region_op.py` 扫 OS+IS 阶段、读 `status`+`osmosisPoints` 逐区核验，与探针 `active` 全 10 区逐一吻合**；数据 `results/region_op_verify_20261005-215357.json`）：
> - **ACTIVE（放宽 = `status=ACTIVE`）**：SA 组件池 eligibility 实际采用的口径，也是 SA 构建器选组件的计数口径。
> - **OP>0（严格 = `status=ACTIVE` 且 `osmosisPoints>0`）**：本报告 §8 此前定义的「平台 active 精确定义」（排除 DECOMMISSIONED）。OP 是分配/收益层概念，**不决定一颗 ACTIVE alpha 能否被选为 SA 组件**——所以「可建 SA」仍以放宽口径为准（GO=6）。但该列揭示：GBR/GLB 大量 ACTIVE 尚未累积 OP（多为 2026 新提交），是健康/分配视角而非构建门槛。

| 状态(放宽) | 区域 | ACTIVE(status=ACTIVE) | 其中 OP>0(严格) | no_OP | DECOM | 严格口径(<10?) |
|---|---|---|---|---|---|---|
| GO | USA | 37 | 16 | 21 | 101 | GO(16) |
| GO | IND | 27 | 21 | 6 | 4 | GO(21) |
| GO | KOR | 24 | 14 | 10 | 2 | GO(14) |
| GO | GBR | 11 | 8 | 3 | 0 | ⚠ **BLOCKED(8)** |
| GO | MEA | 19 | 18 | 1 | 0 | GO(18) |
| GO | GLB | 10 | 9 | 1 | 0 | ⚠ **BLOCKED(9)** |
| BLOCKED | DEU | 6 | 6 | 0 | 0 | BLOCKED(6) |
| BLOCKED | EUR | 4 | 4 | 0 | 6 | BLOCKED(4) |
| BLOCKED | ASI | 8 | 8 | 0 | 0 | BLOCKED(8) |
| BLOCKED | HKG | 6 | 6 | 0 | 0 | BLOCKED(6) |

- **放宽口径（SA 构建实际用）**：GO=6 区（USA/IND/KOR/GBR/MEA/GLB）可建 SA；BLOCKED=4 区（DEU/EUR/ASI/HKG）组件不足，需先把攒着可提交的 RA 提交（IS 阶段不计入）。
- **严格口径（OP>0）的重要提示**：若改按 §8 的「active=OP>0」定义，**GBR(8) 与 GLB(9) 跌破 10 → GO 仅剩 USA/IND/KOR/MEA 4 区**。但如前注，SA 构建器按 `status=ACTIVE` 计数，故实际可建性不受影响；此列仅提示这两区 ACTIVE 中近 1–3 颗尚未分配 OP（多为新提交、OP 逐日累积），属正常现象而非告警。
- **DECOM 佐证**：USA 101 颗 DECOMMISSIONED 被严格排除（与 §8「138=37+101」一致），证明探针未把 decommission 算进 ACTIVE。

### 6b. 全部 SUPER alpha（平台口径）

- **总计 47 颗**
- **ACTIVE（已上线）= 21**（跨 GLB / IND / KOR / MEA / USA）
- **UNSUBMITTED（已建未提交候选）= 26**（IND 13 + KOR 13）

⚠ 本地 `alphas` 表仅存 6 颗 SUPER（陈旧子集），**SA 必须以平台为准**。

### 6c. 未提交 SA 候选清单（26 颗，按 IS sharpe 降序，含优先级）

优先级 = 按 sharpe 降序；P1(sharpe≥5.0) / P2(≥4.5) / P3(<4.5)。提交前须逐颗 `super_build.py probe` 验 prod/self<0.7（平台 prod 闸），并消耗 SUPER 配额 1/天/区。区域归属以平台探针为准（IND 13 + KOR 13）。

| 优先级 | alpha_id | region | selLimit | IS sharpe | IS fitness |
|---|---|---|---|---|---|
| P1 | LLZnG5ZM | IND | 30 | 6.13 | 5.89 |
| P1 | A1vnG78Y | IND | 30 | 6.10 | 5.81 |
| P1 | wpb5jv1l | IND | 30 | 5.20 | 5.07 |
| P1 | omWnl7Km | IND | 30 | 5.13 | 4.84 |
| P1 | ZYAjnYv3 | IND | 30 | 5.13 | 4.86 |
| P2 | 88PO30eX | IND | 12 | 4.91 | 4.61 |
| P2 | 6XKRrEmP | IND | 20 | 4.85 | 4.72 |
| P2 | akxN1bV6 | IND | 30 | 4.85 | 4.72 |
| P2 | xAbeYeWn | IND | 15 | 4.85 | 4.68 |
| P2 | P0gn2w3J | IND | 11 | 4.81 | 4.35 |
| P2 | WjeNP9WG | IND | 10 | 4.61 | 3.96 |
| P2 | MP3b7e88 | IND | 10 | 4.70 | 4.12 |
| P2 | O08oOMG7 | KOR | 12 | 4.52 | 5.67 |
| P2 | vR25EJmG | KOR | 10 | 4.52 | 5.63 |
| P2 | 1YZJQpNm | KOR | 10 | 4.69 | 5.64 |
| P2 | wpbLgkql | KOR | 10 | 4.60 | 5.64 |
| P2 | YPMQXxXq | KOR | 10 | 4.89 | 5.41 |
| P2 | 1YZJENmJ | KOR | 10 | 4.79 | 5.60 |
| P2 | 6XKzOx6Y | KOR | 10 | 4.28 | 5.29 |
| P2 | 3qVzZN3O | KOR | 10 | 4.36 | 5.45 |
| P2 | 9qWJv1do | KOR | 10 | 4.45 | 5.54 |
| P2 | leKrd9Y2 | KOR | 10 | 4.42 | 5.49 |
| P3 | Vk0O9ZPY | KOR | 10 | 3.96 | 5.27 |
| P3 | mL6Z35qE | KOR | 10 | 3.74 | 5.12 |
| P3 | E5Rk18lK | KOR | 10 | 3.87 | 4.99 |
| P3 | 0mrAwgV1 | IND | 30 | 4.47 | 4.74 |

---

### 6d. 两份 SA 探针的差异说明（数据可比性）

| 探针 | generated_at | 来源 | 10 区 GO | ACTIVE SA | 未提交 SA 候选 |
|---|---|---|---|---|---|
| `sa_candidates_20261005-203751.json`（缓存种子，本轮命中） | 20:22:50 | 全量翻平台 | 6 | 21 | 26 |
| `sa_candidates_20261005-213329.json`（本日后台全量） | 21:20:24 | 全量翻平台 | 6 | 21 | 26 |

**结论口径完全一致**（eligibility 分区、ACTIVE 数、SUPER 总数、未提交候选数均相同）。

⚠ **唯一差异**在「未提交 IS 组件候选」计数与 `total_regular`（非硬闸输入，仅供参考）：

| 区 | 20:22 缓存 | 21:20 全量 |
|---|---|---|
| USA | 37（total 175） | 3（total 141） |
| IND | 37（total 68） | 0（total 31） |
| KOR | 78（total 104） | 61（total 87） |
| EUR | 203（total 213） | 249（total 178） |

差异方向不一致（有的增有的减），**不是单向截断**，最可能是两次翻页各自的分页/限流噪声。**该字段不参与 eligibility 判定**（硬前置只看 `ACTIVE 已提交 REGULAR` 数），故不影响 GO/BLOCKED 结论；正式报告以缓存口径为准，此差异仅登记备查。

---

## 7. 历史对比（vs 上一份 `submit_inventory_20261005-214013.json`）

| 项 | 上一份 214013（21:40:13） | 本轮 214030（21:40:30） | 变化 |
|---|---|---|---|
| SUBMIT_NOW | 7 | 7 | 无 |
| THIN_MARGIN | 2 | 2 | 无 |
| 其余五桶 | 0 | 0 | 无 |
| 九颗 alpha 集合（新晋/退出） | 9 颗 | 同 9 颗 | **新晋 0 / 退出 0** |
| 桶位 / prod / self / 余量 / 绩效 / 塔位 / verdict | — | — | **逐字段零差异**（唯一差异 = `generated_at`、`started_at` 两个时间戳） |
| `corr_age_h` | 1.2–15.0h | 3.0–15.3h | 仅相关性年龄自然增长（未触发 48h 重测） |
| submit_ready 台账 | READY=9 | READY=9 | 盘前=盘后，无异常 |

**向后追溯**：195357（19:53）→ 211903 → 212043 → 213809 → 214013 → **214030** 六轮，七分类计数完全一致（7/2/0/0/0/0/0），关键字段（bucket、prod、self、min_margin、sharpe、fitness、two_year、turnover、tower、tower_multiplier、verdict）**零变化**，仅 `corr_age_h` 随真实耗时递增。

**结论：账户可提交候选组合自 19:53 全量修复验收以来持续稳定，无晋级、无降级、无退出。**

---

## 8. 相关性限流 / 平台 active 核验

- **correlation_busy / pending 限流**：本轮 RA 九颗相关性**全部命中 checkpoint 复用**（`corr_source=checkpoint`，新鲜度 3.0–15.3h，均 < 48h 阈值），**零 live `check_correlation` 调用** ⇒ 无任何 correlation_busy / pending，无候选落入 CORR_UNKNOWN / ERROR；SA 走本地缓存，零平台翻页。
- **「平台 active」精确定义**（供用户口径对齐）：`status=ACTIVE` 且 `osmosisPoints>0`（已分配 OP），**排除 DECOMMISSIONED**（独立 status 值）。核验法：扫 OS 阶段 `get_user_alphas(stage="OS", alpha_type="REGULAR")` 读 `status`+`osmosisPoints`；平台不支持 region/status 服务端过滤（客户端过滤 + max_scan 默认 1000；单请求 offset 上限≈1000，超出报 400）。
  - ⚠ **口径区分（与 §6a 联动）**：SA 组件池 eligibility 与 SA 构建器的组件选择均按**放宽口径**（仅 `status=ACTIVE`）计数，故 GO=6 区；本报告此前称「active=OP>0」为严格定义，仅供对齐用户 tracking 视图。按严格口径（见 §6a 表）GBR(8)/GLB(9) 会跌破 10，但**不影响实际可建性**——OP 是分配/收益层概念，不决定一颗 ACTIVE alpha 能否被 SA 选为组件；该列仅提示这两区部分 ACTIVE 尚未累积 OP（多为新提交），属健康/分配视角。两口径全 10 区数值已由 `tools/verify_region_op.py` 逐区核验（与探针 `active` 完全一致）。
- **已核验实例（20:53/21:07 双核验）**：USA REGULAR OS 全量 = 138 = ACTIVE 37 + DECOMMISSIONED 101；ACTIVE 37 中 OP>0 = 16。本地 `alphas.platform_status` 未同步（USA 本地 ACTIVE=34，比平台少 3），**任何 ACTIVE/eligibility 计数以平台探针为准**。

---

## 9. 待用户决策项（提交前须知，不替用户决定）

1. **提交闸门已知死端点**：平台 submit 层对本批恒返回 404（已知死端点），verdict 靠模拟层 + Failed-count，已通过。提交前仍须 `check_correlation(alpha_id, refresh=True)` 终验 prod/self<0.7。
2. **2Y 缺失须终验**：GBR 5 颗（JjQbYdGW/QPK26lQX/QPKErLvX/j289xaxO/omWVV6Y2）+ N1VnJjXg 的 is 层 `two_year=None`（平台未回传），提交前须 refresh 终验 2Y 达标。
3. **余量贴墙建议不提**：RR6NOlma（0.0139）、LLZ6wZO2（0.0238）prod 余量 < 0.03，建议不提。
4. **SA 提交前逐颗验闸**：26 颗未提交 SA 候选提交前须 `super_build.py probe` 验 prod/self<0.7（平台 prod 闸铁律），并消耗 SUPER 配额 1/天/区（独立于 REGULAR）。
5. **GBR 游离盲区**：仍有未入队 UNSUBMITTED（仅 11 颗已测相关性已入队）；其余游离项如需纳入后续盘点，须 `tools/submit_queue.py add --alpha-id <id>` 入队 + `submit_verdict.py` 取平台终判。

---

## 10. 纪律遵守确认

- 全程**只盘点不提交**；未调用任何 submit / POST；`wqb.config.ALLOW_ALPHA_SUBMIT=False` 未触碰。
- SA 探针新增缓存层后，仍**只读不提交**；`--refresh` 仅影响取数来源，不改变只读性质。
- 配额：REGULAR 1/天/区、SUPER 1/天/区，提交须用户逐次明示授权。

---

## 11. 本轮产出物（md + json，**无 CSV**）

| 文件 | 说明 |
|---|---|
| `results/inventory_consolidated_20261005.md` | 本整合报告 |
| `results/submit_inventory_20261005-214030.json` | RA 盘点原始数据（`--no-csv`，退出码 0，10s） |
| `results/sa_candidates_20261005-214043.json` | SA 探针产物（缓存命中 ~2.4s） |
| `results/sa_probe_cache.json` | SA 主缓存（TTL 6h，`SA_PROBE_CACHE_TTL_HOURS` 可覆盖） |

`--no-csv` 已验证生效：21:40 时段（214013/214030）**未生成任何 `submit_inventory_*.csv`**；目录内最后一份 CSV 为 21:20:43 的历史产物（旧口径遗留）。

**本轮本地游离候选核对**（RA 盘点盲区补充，零平台配额）：本地 `alphas` 表 `platform_status='UNSUBMITTED'` 且未入队者 1394 条，**属正常 IS 回测池**（从未过闸），非漏盘；当日 GBR 11 颗 free-floater 与 EUR `N1VnJjXg` 均已入队。⚠ 顺带发现 `submit_ready` 有 15 个 alpha_id 在本地 `alphas` 表无对应行（`N1VnJjXg`·`O08EjLVp`·`LLZ6wZO2`·`d51A3nqY`·`A1v9YxKR` 等）——盘点取数走 `submit_ready` + 平台，**不影响本轮结论**，但属本地 DB 登记缺口。
