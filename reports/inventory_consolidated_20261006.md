# 候选 alpha 可提交性盘点 · 2026-10-06 23:08（ET 2026-10-06 11:08）

**Base payment ∝ rank(提交数量, 提交质量, Value Factor, 自我成长) × Theme 倍数**
（Value Factor = (a) 单α表现 ＋ (b) 多样性 ＋ (c) 独特性）

> 本报告只盘点、不提交。配额口径：**REGULAR 4 颗 / ET 日 ＋ SUPER 1 颗 / ET 日（全账户，不分区）**，00:00 ET 重置。

---

## 一、影响 base 的收益点

### 1) 提交数量 · 连续性
- 可提交池：**RA 12 颗**（EUR 2 / GBR 3 / IND 6 / **DEU 1**）＋ **SA 9 颗**（全部 KOR，双闸实测 10 过 2 死，剔除已提交的 `9qWJv1do`）。
- **去重＋自锁后真实可提 ≈ RA 3 颗**（IND 1 ＋ EUR 1 ＋ DEU 1）；SA 因同源自锁只能提 **1–2 颗**。
- ⚠ DEU 那颗（`58gkLAkk`）此前**从未出现在任何盘点里**：它只存在于平台，本地库无此行（详见文末「漏扫根因」）。本轮已补录入队。
- 配额：工具 `quota_status.py` 恒显 0/4（已知不可信）；按 12:45 提交实测，ET 日 10-06 已用满 **4 REGULAR ＋ 1 SUPER ⇒ 当日剩余 R 0 / S 0**，下一窗口 **2026-10-07 00:00 ET（本地 10-07 12:00）**。
- 另有 **44 条** L1 达标候选（GLB 22 / EUR 11 / GBR 8 / USA 2 / ASI 1）已生成入队提案待裁决，未落库。

### 2) 提交质量 · 单α表现（VF-a）
- 平台 RA 检查 **全部无 FAIL**（failed_ra=0）；margin 已知项 **全 ≥ 7.2bp**（EUR `WjegEmQO` 40.9bp 最高）。
- **以「约束后 sharpe」为准**：本批衰减区间 —— IND **−60% ~ −74%**（IS 2.84–3.92 → 约束后 0.87–1.54）、GBR −26%~−39%、KOR −30%。**IS 越强的 IND 衰减越狠**。
- 单α最优：**`WjepYR7d`（IND）约束后 1.54**（IS S 3.92 / F 2.81 / 2Y 2.87 / 回报 16.9% / 回撤 3.44%）。
- turnover：EUR/GBR/KOR 候选 **0.031–0.144** 全在内控线内；**IND 6 颗 0.305–0.379 全部超 0.30 线**（平台 checks 仍干净，属内控偏好项）。

### 3) 多样性（VF-b）· 塔覆盖
- **条数 ≠ 多样性**：11 条里 **6 条被 IND 同一批同骨架独占**、**3 条被 GBR/D1/MODEL 独占且该塔已点亮**。
- 现队列覆盖 **6 塔 / 5 区**（EUR·GBR·IND·KOR·**DEU**）。
- **未点亮塔（点灯价值最高）**：**IND/D1/MODEL 2/3、IND/D1/PV 2/3、KOR/D1/MODEL 2/3 —— 均差 1 颗点亮**；其次 EUR/D1/MODEL、EUR/D1/FUNDAMENTAL、EUR/D1/RISK、USA/D1/EARNINGS、IND/D1/ANALYST、IND/D1/RISK、KOR/D1/SHORTINTEREST、ASI/D1/OTHER 各 0–1（差 2–3）。
- **已点亮（不优选）**：USA/D1/MODEL 4、GBR/D1/MODEL 4、KOR/D1/FUNDAMENTAL 3。

### 4) 独特性（VF-c）· 低 prod/self ＋ 低互相关
- **避雷族（已实测自锁）**：**GBR/MODEL 全族** —— `QPK26lQX` 提交节点实测 self **0.9985**，命中自家 ACTIVE `3qVa2Lze`（同波 `gb_rank_opt_20261005`），该族 3 颗 + `RR6NOlma` 全部不提。
- **避雷（重复登记）**：`omWVZ7lm` 表达式与 **已提交** 的 `N1VnJjXg` **逐字相同** ⇒ 提交必被 self 拦，不提。
- **可同日并行对**：`WjepYR7d`（IND/mdl37）与 `WjegEmQO`（EUR/qfl_cassie）跨区跨字段族，实测 prod/self 互不相干 ⇒ 可同日并行。
- **余量 < 0.03 不提**：`RR6NOlma` .0139、`786wl6b8` .0103、`A1vwrQVd` .0165、`LLZ6wZO2` .0238；SA 侧 `6XKzOx6Y` .0014、`3qVzZN3O` .0179、`O08oOMG7` .0262。
- ⚠ **prod / self 列均为台账快照值**，提交节点会用 `check_correlation(type="both")` 的 **max(prod, self)** 实测复核。

### 5) 自我成长
- 基准是你自己历史：**已点亮 3 个塔（USA·GBR·KOR 各 1）**，继续堆 GBR/MODEL 不产生增量 ⇒ **优先把 IND/D1/MODEL 或 IND/D1/PV 从 2 补到 3**（差 1 颗，本批现成候选即可点亮）。
- 反向证据：GBR 那 3 颗是同一波同骨架换字段，重复优化不产生新塔、不产生新 VF。

### 6) Theme 倍数
- 本批 RA 候选 `tags` **未见主题命中 ⇒ 0**；SA 候选 `tags` 亦空 ⇒ 未见 Super Alpha Themes 加成。这是唯一可主动争取的外挂收益项，目前无抓手。

---

## 二、推荐提交序（执行用）

### RA（REGULAR）

排序键：① 未点亮塔优先 ② 未点亮内缺口小者优先（差1 > 差2 > 0/3）③ 同档按业绩。
**余量 = 0.7 − max(prod, self)**。prod/self 为**台账快照值，提交前以节点 `both` 实测为准**。

| 序 | alpha_id | 区 | S | 2Y | prod | self | 余量 | 塔（点亮判定 ACTIVE≥3） | 说明 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **WjepYR7d** | IND | 3.92 | 2.87 | .6573 | .6562 | **.0427** | IND/D1/MODEL **2/3 差1 未点亮** | 同骨架 6 选 1 代表（另 5 颗：`E5RwxR1P` 余量 .1035 最厚备选、`Vk0pQmkA`、`ZYA2NNKQ`、`E5Rwn8Om`、`P0gpYMMM`）；约束后 S **1.54** 本批最优；TO .329 超内控 .30 |
| 2 | **WjegEmQO** | EUR | 1.94 | 1.59 | .5012 | .1616 | **.1988** | EUR/D1/PV **0/3 未点亮** | 余量最厚；2Y 1.59 贴 1.58 线（真值须 ≥1.585）；⚠ 上一轮提交实测曾 **ROBUSTNESS_REJECT**，提交前须复核；与已提交 `N1VnJjXg` 同字段不同包装，提交前必测 self |
| 3 | **58gkLAkk** | DEU | 1.75 | **未回填** | .5381 | .5153 | **.1619** | DEU/D1/OTHER **0/3 未点亮** | 本轮**补录入队**（此前只存在于平台）；平台实测 2Y=2.07 / sub=1.22 / TO .1457 / margin 13.2bp / **failed_ra=0**；⚠ 台账 2Y 为 None，提交前须 refresh 终验 |
| 4 | omWVZ7lm | EUR | 1.75 | 1.76 | .5378 | .1954 | .1622 | EUR/D1/MODEL 1/3 差2 | ⛔ **不提** —— 表达式与已提交 `N1VnJjXg` **逐字相同** |
| 5 | QPK26lQX | GBR | 1.68 | 2.12 | .5385 | .4951 | .1615 | GBR/D1/MODEL **4 已点亮** | ⛔ **不提** —— 同族 3 颗代表（`QPKErLvX` / `j289xaxO` 逐位近似，仅差 target_tvr .13/.15）；实测 self **.9985** 命中自家 ACTIVE `3qVa2Lze` |
| 6 | LLZ6wZO2 | KOR | 1.99 | 2.24 | .6762 | .6760 | .0238 | KOR/D1/FUNDAMENTAL **3 已点亮** | ⛔ **不提** —— THIN_MARGIN < .03 ＋ 塔已点亮 |

- **THIN_MARGIN（全部不提）**：`RR6NOlma` .0139 / `786wl6b8` .0103 / `A1vwrQVd` .0165 / `LLZ6wZO2` .0238。
- **HARD_BLOCKED**：`786ajadx`（EUR，平台 `LOW_SUB_UNIVERSE_SHARPE`）。
- **PROD_WALL 9 颗（不提）**：`6XjaQrkO`(ASI .958) `GrO3d8bZ`(EUR .827) `A1vg2KnX`(GBR **.999**) `E5RK5RKR`(GBR .724) `rKeEMmq9`(GLB .808) `xA3ep2pq`(GLB .795) `0mXx9d38`(HKG .958) `gJQbllqO`(HKG .911) `leKLRA1N`(USA .939)。
- **跨区建议提交顺序**：**先 IND `WjepYR7d`（差 1 颗点亮 IND/D1/MODEL，是本批唯一能立刻点灯的因子，且约束后 sharpe 最高）→ 再 DEU `58gkLAkk`（DEU 金字塔全空、这是该区第一颗，×1.8 倍率打地基；余量 .1619、TO .1457 本批最健康）→ 再 EUR `WjegEmQO`（余量最厚，但上轮 ROBUSTNESS_REJECT 须复核）**。三者跨区跨族，可同日并行。GBR/KOR 全部跳过：塔已点亮且 GBR 全族已实测自锁。

### SA（SUPER）

#### ① 区域资格 —— SA 独有硬前置（组件池须 ≥10 颗 eligible ACTIVE）
- ✅ **可建区**：USA **37** ｜ IND **27** ｜ KOR **24** ｜ MEA **19** ｜ GBR **11** ｜ GLB **10**
- ⛔ **不可建区**：ASI **8** ｜ DEU **6** ｜ HKG **6** ｜ EUR **4** ⇒ **组件池不足，SA 面在这 4 区结构性关闭**
- ★ 「可建」≠「有得提」：6 个 GO 区里 **只有 KOR 有现成候选**，其余 5 区候选数 = 0。

#### ② 候选相关闸（已实测 prod/self，gate 0.7）
- KOR：**12 颗 → 过 10 / 死 2**。判死：`Vk0O9ZPY` prod **.7960**、`mL6Z35qE` prod **.7291**（这两颗恰是 IS sharpe 最低的 3.96 / 3.74 —— 再证 IS 对 prod 无预测力）。
- IND：**SA 池判死**（13/13 撞墙，历史结论，无新增）。
- 其余 GO 区（USA / MEA / GBR / GLB）：**0 颗现成候选 ⇒ 要 SA 须现场建**。
- ⚠ 本轮 GLB 组出（`super_build.py select`，RAM/decay1/sl10/sg0.70/pc0.90 与 pc1.0 两个变体）**两次均失败**：平台返回 `Failed to create simulation / None`。GLB 新建 SA 通道本轮不可用。

#### ③ 推荐序表（余量 = 0.7 − prod，与 RA 同口径）
> 剔除已提交的 `9qWJv1do`；prod/self 为**台账快照值，提交前须逐颗复测**。

| 序 | alpha_id | IS S | IS F | prod | 余量 | 说明 |
|---|---|---|---|---|---|---|
| 1 | **YPMQXxXq** | 4.89 | 5.41 | .6537 | **.0463** | IS 最强且余量够；首选 |
| 2 | leKrd9Y2 | 4.42 | 5.49 | .6502 | .0498 | 余量最厚 |
| 3 | 1YZJENmJ | 4.79 | 5.60 | .6574 | .0426 | 备选 |
| 4 | 1YZJQpNm | 4.69 | 5.64 | .6596 | .0404 | 备选 |
| 5 | wpbLgkql | 4.60 | 5.64 | .6604 | .0396 | 备选 |
| 6 | E5Rk18lK | 3.87 | 4.99 | .6552 | .0448 | IS 偏弱 |
| — | O08oOMG7 | 4.52 | 5.67 | .6738 | .0262 | 余量 < .03，**不提** |
| — | 3qVzZN3O | 4.36 | 5.45 | .6821 | .0179 | 余量 < .03，**不提** |
| — | 6XKzOx6Y | 4.28 | 5.29 | .6986 | **.0014** | 贴墙最脆，**不提** |
| — | Vk0O9ZPY / mL6Z35qE | 3.96 / 3.74 | 5.27 / 5.12 | .7960 / .7291 | 负 | **撞墙，不提** |

- ⚠ **同源自锁警告（必读）**：这 12 颗全部由 2026-10-05 同一批次生成（selectionLimit 10/12），且 **缓存的 prod/self 测于 02:29，早于 12:45 的 `9qWJv1do` 提交** ⇒ 该次提交已进你的 self 池，**表中所有 self 值均已过期**。提 1 颗后必须对其余逐颗 `--id` 复测，最多提 1–2 颗。

#### ④ 各 base 维度的 SA 落法（只列与 RA 不同处）

| 维度 | SA 落法 |
|---|---|
| ① 数量 | 配额 **SUPER 1 颗/ET 日（全账户）** × 6 个 GO 区 ⇒ 瓶颈不是区数而是日配额 1；先吃 KOR 现成候选 |
| ③ 多样性 | **换区建 SA**（GO 区里现成候选 = 0 的：USA / MEA / GBR / GLB）＋ selection 用 `OR` 多条件扩组件覆盖；GLB 组出本轮两次失败，须先修通道 |
| ④ 独特性 | prod/self 实测；**每区只留 1–2 颗代表**；提交后复测其余 |
| ⑥ Theme | Super Alpha Themes（候选 `tags` 空 ⇒ 未见加成） |
| — 塔 | **不适用**（SA 出自已 ACTIVE 组件池，不点亮新 RA 塔），SA 的「塔」维替换为「**换区**」维 |
| — 口径 | SA 唯一不同提交口径 = turnover **2%–40%**（RA 无此区间约束） |

---

## 提交前铁律（提示，不替你决定）

1. 平台 submit 层**恒 404**（已知死端点），verdict 靠模拟层 + Failed-count。
2. `two_year=None` 的候选（`xA3ep2pq` 等）提交前须 refresh 终验 2Y。
3. **余量 < 0.03 建议不提**。
4. SA 提交前**逐颗**验 prod/self < 0.7；且因同源自锁，提 1 颗后其余必须复测。
5. ★ **台账 prod/self 只是历史快照** —— 提交节点以 `check_correlation(type="both")` 的 **max(prod, self)** 复核。若候选命中自家近期**同波同族**已提交 alpha，self 会冲到 0.9+（实证：`QPK26lQX` 台账 prod .5385、余量看似 .16，实被 self .9984 拦）。本批必须自查的两条：`omWVZ7lm` ↔ 已提交 `N1VnJjXg`（表达式相同）、GBR 全族 ↔ ACTIVE `3qVa2Lze`。
6. SUPER **不得**走 `workflow_submit_alpha`（回 `super_requires_super_build`）⇒ 授权时走
   `python tools/super_build.py submit --alpha-id <ID> --name <R_S_...> --region <R>`（内置 prod-gate），并以 `WQB_ALLOW_ALPHA_SUBMIT=1` 前缀放行全局锁。**ID 随批次变化，勿照抄历史 ID。**

---

## 附：为何 `58gkLAkk` 此前从没被扫到（已修，两层根因）

**第一层 · 数据缺口**：所有盘点工具（`submit_inventory` / `scan_backup_ra` / `enqueue_propose`）**只扫本地 SQLite**。
`58gkLAkk` 是平台上有、本地 `alphas`/`submit_ready`/`backtest_results` 三张表**均无**的 alpha
（DEU 本地最后入库停在 10-02，整整 4 天没同步；其他活跃区都同步到 10-06 18:25）。
⇒ 修法：本轮已 `submit_queue.py add` 补录入队，现为 READY / SUBMIT_LAYER_VERIFIED，盘点已能扫到。
**同类风险仍在**：任何走直连/客户端路线、未经 harvest 的 alpha 都不会进本地库。

**第二层 · 工程 bug（已修）**：补录时 `tools/submit_queue.py` 卡死 13 分钟零输出。根因是环境残留
`WQ_PY=D:/coding/hw_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe`（**另一份仓库副本**）。
- `tools/_pyenv.py::venv_python()` 只校验 `os.path.isfile()`，不校验归属 ⇒ 串仓的 venv 一路放行。
- `submit_queue.py` / `alpha_properties.py` / `prod_blocked_recheck.py` 还**各抄了一份**候选列表，没走 `_pyenv`。
- Windows 上 re-exec 是「父进程 `subprocess.call` 等子进程」，串仓后三层进程互相等待 ⇒ 卡死。

**修复（4 处代码 + 1 处测试）**：
1. `tools/_pyenv.py` 新增 `is_foreign_wqb_python()`：候选路径祖先里含 `world-quant-brain-mcp`
   但非本仓 MCP 目录 ⇒ 判串仓，**忽略并回退本仓 venv** + stderr 告警（合法自定义解释器不受影响）。
2. `tools/submit_queue.py`、`tools/alpha_properties.py`、`tools/prod_blocked_recheck.py`
   的 `_mcp_venv_python()` 改为复用 `_pyenv.venv_python()`，不再各抄一份。
3. `src/wqb/workflow/_common.py::wq_py()` 内联同一判据（src 层不 import tools）。
4. `tests/unit/09_core/test_pyenv.py` 新增 2 条回归（串仓忽略 / 普通自定义不误伤）。

**验证**：`tests/unit/09_core` + `tests/unit/02_workflow` **737 passed**；三闸全绿（doc_path_refs BROKEN 17 = 基线 17 无新增；destructive-default 无新增）；
带毒 `WQ_PY` 实测 3 处均正确回退本仓 venv，`submit_queue add` 端到端不再卡死。
⚠ **彻底消除请在 shell 里 `unset WQ_PY`** —— 代码层已能自保，但环境变量本身仍是脏的。

---

*本轮只盘点、未提交、未触碰 `ALLOW_ALPHA_SUBMIT`；仅对 `58gkLAkk` 一颗按你点名做了入队补录。
入队提案（44 条）与补扫（238 条，待核 62）均为 dry-run，待你裁决。*
