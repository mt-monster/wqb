# 候选 Alpha 可提交性盘点（整合报告）· 2026-10-07

> **快照**：RA `submit_inventory_20261007-014636` / SA `sa_candidates_20261007-014927`（01:49 refresh）/ 双闸 `sa_unsubmitted_probe_20261007-015935` / 区域OP `region_op_verify_20261007-015429` / 入队提案 `enqueue_proposal_20261007-014236` / 补扫 `backup_ra_candidates_20261007` / 塔 `pyramid_latest`（fetched 01:41）
> **只盘点、不提交**：全程零 `POST /submit`、零 `--apply`；`ALLOW_ALPHA_SUBMIT` 未触碰。⚠ 本表 prod/self 均为**台账/checkpoint 快照值**，提交前须 `check_correlation(refresh=True)` 终验。

**Base payment ∝ rank(提交数量, 提交质量, Value Factor, 自我成长) × Theme 倍数**（VF = 单α表现 + 多样性 + 独特性）

---

## 第一部分 · 影响 base 的收益点

### 1. 提交数量 · 连续性
- **RA**：名义 SUBMIT_NOW 12 颗，但自锁/重复/同骨架比对后**真可提 2 颗（骨架干净）＋ 条件 2 颗（须终验）**（见 §二）。
- **SA**：有效未提交 10 颗 = KOR 9（剔已提交 `9qWJv1do`）＋ GLB 新建 1（`MP3Q160n`）。
- **配额**：REGULAR 4/ET 日、SUPER 1/ET 日（全账户、不分区，两条独立线）。⚠ `quota_status.py` 显「R 剩余 4 / S 剩余 1」是**已知失真**（`activities/submissions` 缺 today 快照）；ET 日 2026-10-06 实际已用尽 4R+1S ⇒ **当前窗口剩余 0/0**，下一窗口 2026-10-07 00:00 ET。

### 2. 提交质量 · 单α表现（VF-a）
- 4 颗 shortlist checks **无 FAIL、margin≥4bp、ra_failed=0**。margin：`WjegEmQO` **40.9bp**（本批最优）＞ `58gkLAkk` 13.2bp ＞ `WjepYR7d` 10.3bp ＞ `E5RwxR1P` 8.4bp。
- ⚠ **以「约束后 sharpe」为准**（investability/robust）：IND 原始 S 3.6–3.9 → 约束后 **1.22–1.54（衰减 ≈2.5×）**；EUR/DEU 原始 ~1.8–1.9 → 约束后 ~1.1–1.4。原始 sharpe 高≠质量高。
- ⚠ `WjepYR7d` TO **0.329**、`E5RwxR1P` TO **0.379** 超内控 0.30。净质量最优 = `WjegEmQO`（低 TO 0.031 + margin 40.9bp + prod 余量 0.199）。

### 3. 多样性（VF-b）· 塔覆盖
- **条数 ≠ 多样性**：IND family A（6 颗 `WjepYR7d/E5Rwn8Om/P0gpYMMM/Vk0pQmkA/ZYA2NNKQ/A1vwrQVd`）全指向 **同两塔 IND/D1/PV＋MODEL**，且命中自家 ACTIVE `LLZg3XWa` ⇒ 有效点亮仅 1、且自锁。
- 现可提队列覆盖：`58gkLAkk`→**DEU/D1/MODEL＋DEU/D1/OTHER（均 0/3 打地基，×1.8）**；`WjegEmQO`→EUR/D1/MODEL（1/3 差2，×1.3）；`E5RwxR1P/WjepYR7d`→IND/D1/PV＋MODEL（2/3 差1，×1.1/×1.2）。
- **未点亮塔（点灯价值最高）**：DEU 全塔（0/3 ×1.8）、GLB 全塔（0/3，见 §三 22 颗 GLB/D1/PV 白空间）、IND 双塔差1。

### 4. 独特性（VF-c）· 低 prod/self ＋ 低互相关
- **可同日并行对**：`WjegEmQO`(EUR) × `58gkLAkk`(DEU) —— 不同区/不同塔/骨架干净/prod 0.50·0.54 余量大。
- **避雷族（prod/self 撞墙或自锁）**：GBR/MODEL 4 颗（命中 ACTIVE `3qVa2Lze` ＋ 已提交 `JjQbYdGW/omWVV6Y2`，`QPK26lQX` 曾实测 0.9985）；IND famA（prod≈self 命中 `LLZg3XWa`）；`omWVZ7lm`（与已提交 `N1VnJjXg` 表达式**逐字相同**）。
- **余量<0.03 不提**：`RR6NOlma` 0.0139 / `786wl6b8` 0.0103 / `A1vwrQVd` 0.0165 / `LLZ6wZO2` 0.0238（THIN）。

### 5. 自我成长
基准 = 自身历史 ⇒ 优先补新塔：`58gkLAkk`（DEU 两颗 0/3 ×1.8，边际收益最高）＞ `WjegEmQO`（EUR 差2），而非重复 GBR/MODEL 同族（该塔已 4/3 点亮）。

### 6. Theme 倍数
`WjegEmQO`/`WjepYR7d`/`E5RwxR1P`/`58gkLAkk` checks 均含 `MATCHES_THEMES`（当前 pending）⇒ 提交时确认主题命中；未命中 = 0 倍率，可主动争取。

---

## 第二部分 · 推荐提交序（执行用）

### RA 表（塔规则：未点亮优先 → 缺口小者优先 → 业绩；★ prod/self 均快照值）

| 序 | alpha_id | 区 | S | 2Y | prod | self | 余量 | 塔 | 说明 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `WjegEmQO` | EUR | 1.94 | 1.59 | 0.5012 | 0.1616 | 0.199 | EUR/D1/MODEL(1/3)×1.3 | ✅ 骨架干净 · margin 40.9bp · TO 0.031 · 净质量最优 |
| 2 | `58gkLAkk` | DEU | 1.75 | **2.07**(平台) | 0.5381 | 0.5153 | 0.162 | DEU/MODEL+OTHER(0/3)×1.8 | ✅ 骨架干净 · 打地基 2 塔 · 台账 2Y=NULL 已纠为 2.07 |
| 3 | `E5RwxR1P` | IND | 3.61 | 2.54 | 0.5965 | 0.5964 | 0.103 | IND/PV+MODEL(2/3)×1.1/1.2 | ⚠ 条件：prod≈self 暗示近亲、TO 0.379 超内控；提交前须 refresh 终验 |
| — | `WjepYR7d` | IND | 3.92 | 2.87 | 0.6573 | 0.6562 | 0.043 | IND/PV+MODEL(2/3) | ⚠ 同骨架命中 ACTIVE `LLZg3XWa` ⇒ 大概率自锁，非 clean，须 refresh |
| — | THIN 4 颗 | GBR/IND/KOR | — | — | — | — | <0.03 | — | **不提**：`RR6NOlma`/`786wl6b8`/`A1vwrQVd`/`LLZ6wZO2`（`LLZ6wZO2` 另命中 ACTIVE `gJZ7AvZO/0mrnWojG`） |
| — | PROD_WALL 9 颗 | 多区 | — | — | ≥0.7 | — | 负 | — | **不提**：`6XjaQrkO`/`GrO3d8bZ`/`A1vg2KnX`/`E5RK5RKR`/`rKeEMmq9`/`xA3ep2pq`/`0mXx9d38`/`gJQbllqO`/`leKLRA1N` |
| — | HARD_BLOCKED 1 | EUR | 1.92 | 2.08 | — | — | — | EUR/D1/PV | **不提** `786ajadx`：SIM_FAIL `LOW_SUB_UNIVERSE_SHARPE` |
| — | GBR 3 ＋ `omWVZ7lm` | GBR/EUR | — | — | 快照<0.7 | — | — | — | **不提**：自锁/重复（见 §一.4） |

### SA 段（四步）

**① 区域资格**（组件池 ≥10 eligible ACTIVE，SA 独有硬前置）
- ✅ 可建：**USA 37 ｜ IND 27 ｜ KOR 24 ｜ MEA 19 ｜ GBR 11 ｜ GLB 10**
- ⛔ 不可建：DEU 6 ｜ EUR 4 ｜ ASI 8 ｜ HKG 6 —— 组件池不足 ⇒ SA 面结构性关闭
- 严格 OP>0 口径：GBR 8、GLB 9 <10（分配视角，非门槛；GO 仍按放宽口径）

**② 候选相关闸**（逐区 prod/self 实测，线 0.7）
- KOR 12 颗 → **10 过 / 2 死**（`Vk0O9ZPY` 0.796、`mL6Z35qE` 0.729）；剔已提交 `9qWJv1do` ⇒ **9 有效**
- IND SA 池 **判死**（历史 13/13 撞墙，现 0 未提交）；GLB 新建 `MP3Q160n` → **prod 0.6872 PASS**（余量 0.0128）
- USA 3 颗 SA 全 ACTIVE、新 SA PROD>0.82 ⇒ PROD 堵死，暂不组

**③ 推荐序表**（序 / alpha_id / IS S / IS F / 余量=0.7−prod）

| 序 | alpha_id | 区 | IS S | IS F | 余量 |
|---|---|---|---|---|---|
| 1 | `leKrd9Y2` | KOR | 4.42 | 5.49 | 0.0498 |
| 2 | `YPMQXxXq` | KOR | 4.89 | 5.41 | 0.0463 |
| 3 | `1YZJENmJ` | KOR | 4.79 | 5.60 | 0.0426 |
| 4 | `wpbLgkql` | KOR | 4.60 | 5.64 | 0.0396 |
| 5 | `1YZJQpNm` | KOR | 4.69 | 5.64 | 0.0404 |
| 6 | `E5Rk18lK` | KOR | 3.87 | 4.99 | 0.0448 |
| 7 | `O08oOMG7` | KOR | 4.52 | 5.67 | 0.0262 |
| 8 | `3qVzZN3O` | KOR | 4.36 | 5.45 | 0.0179 |
| 9 | `MP3Q160n` | GLB | 3.30 | 2.03 | 0.0128（新建，self 待复测） |
| — | `6XKzOx6Y` | KOR | 4.28 | 5.29 | **0.0014 不提** |
| — | `Vk0O9ZPY`/`mL6Z35qE` | KOR | 3.96/3.74 | — | 撞墙 不提 |

⚠ **同源自锁警告**：12 颗 KOR 由 2026-10-05 同批 ~40min 生成（selLimit 10/12 相同）；prod 测于 10-06 00:22–01:26，**早于 `9qWJv1do` 提交（12:45 CST）⇒ 9 颗 self 全过期**。`9qWJv1do` 现已进 self 池 ⇒ 提 1–2 颗后必须逐颗 `--id` 复测其余 self。`MP3Q160n` 本次 self=0 系「OS 组件池空」伪值，非真实 self。

**④ 各 base 维度的 SA 落法（只列与 RA 不同处）**

| 维度 | SA 落法 |
|---|---|
| ① 数量 | 1 颗/ET 日（全账户 SA 线，独立于 RA）；先吃有现成候选的区（KOR）＋ 新建 GLB |
| ③ 多样性 | **换区建 SA**：本轮已为 GLB 组出 `MP3Q160n`（SUBINDUSTRY，§七 参数），GLB 首次有 SA 抓手 |
| ④ 独特性 | 每区只留 1–2 颗代表，提后复测（KOR 同源自锁） |
| ⑥ Theme | Super Alpha Themes —— 候选 `tags` 全空 ⇒ 未见主题加成 |
| — 塔 | **不适用**（SA 出自已 ACTIVE 组件池，不点亮新 RA 塔）；以「换区」维替代 |
| turnover | SA 提交口径 2%–40% |

---

## 第三部分 · 全闸未入队候选（展示口径）

**A. `scan_backup_ra --all-regions`（dry-run）= 240 条（待核 62）**
按区：ASI 111 ｜ GLB 68 ｜ GBR 44 ｜ EUR 16 ｜ USA 1。
（默认已移除同骨架过滤；`2Y/sub NULL`=待核仍列出；`--apply` 由用户决定，本轮未入队。）

**B. `enqueue_propose` 三层裁决（dry-run）：S0 8172 → L1 142 → 提案 46；content_hash `518518321625bdd0`**

**★ L2 同族去重 = 96 条 / 20 组**（按骨架组列「代表 won_by ＋ 被去重成员」，让被去重候选现形）：

| 区 | 代表(won_by) | 被去重成员（alpha_id） |
|---|---|---|
| GBR | `npPWX19w` | blO9AeKp, 58gv2Va1, vR2L80P3, akxOgKR9, **P0gv3AO7**, O089k78g, E5RK2Z1G, vR2mPWod, blO9K3Np, e7Qx8Pdg, blOdVR1m, 3qV7Q2dO, XgJKL7Rl, 6XKe3rQp, pw5KoPpj, xAbd9YEJ, P0gvv5gE, d51ddaWX, akxAgvNw, KPrX2R0j, 2rmJJ5jw, 0mrzzPPp, 9qWJr2rq, omWKpjgJ, 6XKw7x2J, 58gMMJEk, LLZg2Jk6, N1VAAQn8, JjQpqQom（29） |
| GBR | `leK3rkYn` | omWgVAkm, **npP83YQq**, wpbELOAp, e7QxLgEz, QPK9EqoG, d51RdgrK, wpbEl9oY, kqgZ0JNk（8） |
| GLB | `qM0vJZQE` | wpb1qWQp, 9qWKYkGd, A1vb9Exl, N1V608Po, blOMGZzm, ZYAx6NQ1（6） |
| GLB | `58g9qMJX` | A1vbOkLw, 9qWKAJGx, RR6Ykdea, E5RbrkQG, O08k5oWJ, 3qVxnz0P（6） |
| EUR | `XgWxwWRl` | le8Y68K2, om6X2QnJ, QP3Aemnw, 1YxRVxZR, pwPkONwo, YP5OZXQW（6） |
| GLB | `ZYbjlbX0` | mLmqzmaE, rKObJ653, npdnZkKd, N1angWQp, pwRnVJjj（5） |
| EUR | `vR2ekNGr` | 88PapZKa, LLZg9Ko6, npPZPw6x, LLZg9bEa, A1vglbve（5） |
| GBR | `9qWwZ3oe` | 9qWwZ3go, mL68wNOK, wpbRKA6l, 6XKwmQgE, XgJpmxXa（5） |
| GLB | `VkaXa9dA` | VkaX5dM5, mLmq77vp, LLNnr5K6, XgbkeRV5（4） |
| GBR | `MP3LgOM9` | zqbRAZK8, xAbdjvRq, vR2vjAdQ, 2rmNl5vN（4） |
| GLB | `akbWK6V5` | xA3mrqrw, vRrJZMoA, e7Q7MAMz（3） |
| GLB | `YPMnode6` | blOV13wM, vR2xXVQv, 1YZ1A5MM（3） |
| GLB | `88jO2Pem` | 2rwvoXV8, YPbN9Mgw（2） |
| GLB | `88jKRbRz` | YPbW161l, 6XjYZVQ7（2） |
| EUR | `786Jellx` | blO97pAZ, 88PLAMnX（2） |
| GBR | `6XKw8e6O` | vR2LqvXG, XgJprrw0（2） |
| ASI | `pwRVlg3j` | vRrelx1w（1） |
| GLB | `LLNlZKMa` | 3qXn1rJN（1） |
| USA | `GrOq3WLP` | JjQV5ep2（1） |
| GBR | `XgJ8vdm5` | ZYAK7aoZ（1） |

> 典型：`npP83YQq`（GBR S1.83/F1.31/2Y2.27，L1 通过）被同骨架代表 `leK3rkYn`（S1.90/F1.38）挤掉 —— 现于报告**现形**，非隐形。GLB/D1/PV 0/3 打地基是最大白空间。

### §三 候选如何合理入选 §二 推荐提交序
> §三 是**未入队 / 被同族去重**的池子，天然不在 §二（§二 只从 `submit_ready` READY 行经 `submit_inventory` 产出）。三者分治：
> - **提案 46（L2 代表）** = 符合入队条件的种子；只有它们该谈「入选」。
> - **被去重 96** = 同族非代表，按**同族只留 1**铁律本就不该各自入序（现形只为透明，不为提交）。
> - **scan_backup_ra 240** = 更宽的展示口径（含同骨架变体），非入队口径。

**唯一合规链路（全链 dry-run 由自动化做，`--apply`/入队由用户裁决）**：
1. **补齐指标**：`2Y/sub=NULL` 的「待核」行先 `tools/data-repair/backfill_alpha_metrics_from_platform.py --ids <id> --apply`（或 refresh）落库，否则 L1 判据不全；
2. **入队**（三选一）：`enqueue_propose.py --apply --proposal results/enqueue_proposal_20261007-014236.json --approved-by <人> [--approve id1,id2]`（L3 哈希校验+重跑 L1）／单颗 `tools/submit_queue.py add --alpha-id <id>`；
3. **平台终判**：`tools/submit_verdict.py --alpha-id <id>`（取 ra_failed_checks、模拟层、升 READY）；
4. **重跑盘点**：`submit_inventory.py --no-csv` → 它们才在 SUBMIT_NOW/THIN 现形；
5. **按 §一 排序键定序**：未点亮塔优先 → 缺口小者优先 → 业绩；**入序前必须过自锁全库比对**（`sq._sig` 命中 ACTIVE/已提交同骨架 → 拦）＋ prod/self `check_correlation(refresh=True)` 终验 ＋ checks 无 FAIL ＋ margin≥4bp ＋ TO≤0.30 内控。

**实操倾向（已实测推翻初判）**：本想优先入队 §三 的 **GLB/D1 0/3 打地基族**（账户层面 22 代表中 19 颗骨架与自家 ACTIVE 不碰撞）——但 `check_correlation(refresh=True)` 实测 **8 颗代表全挂 prod**（0.754–0.879，见 `results/glb_prod_recheck_20261007.json`）：GLB 的 0/3 是**本账户**白空间、非**平台**白空间，production book 拥挤 ⇒ **勿入队**（详 `results/enqueue_glb_batch_20261007.md`，已标作废）。GBR/EUR 族代表同理大概率撞自家 ACTIVE（`3qVa2Lze`/`N1VnJjXg`）＋平台 prod。**结论：§三 无一批能凭“骨架干净”直接入选 §二；真可提仍以 §二 已 refresh 的 `WjegEmQO`/`58gkLAkk` 为限（其 refresh 本轮异步未回源=null，提交前需确认 checkpoint 0.50/0.54 仍成立）。**

---

### 提交前须知（提示用户，不替用户决定）
1. 平台 submit 层本批恒 404（已知死端点，verdict 靠模拟层 + Failed-count）；
2. **凡列 prod 余量者，提交前必须 `check_correlation(refresh=True)` 终验**（台账 prod 仅快照，`QPK26lQX`/GBR/IND famA 已实证被自家 ACTIVE 拉高）；
3. IND `WjepYR7d/E5RwxR1P` TO 超内控 0.30；
4. SA 提交前逐颗验 prod/self<0.7，且同批 KOR 提 1–2 颗后复测 self。
