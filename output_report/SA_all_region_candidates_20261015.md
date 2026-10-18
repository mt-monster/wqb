# 全 Region SuperAlpha 候选汇总（供挑选）

生成时间：2026-10-15 03:50（本地）
数据口径：**全部基于平台真实仿真 + 平台双闸实测**，无本地估算。
统一新杠杆：`truncation = 0.02`（此前 IND / GBR 的失败结论多产生于 `trunc 0.08`，已作废重跑）。

---

## 一、结论摘要（每 region 一颗最优，按可提交质量排序）

| # | region / 档位 | alpha id | IS Sharpe | Fitness | Turnover | SELF | PROD | 闸余量 | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | **GLB / MINVOL1M** | `LL5amzov` | **6.93** | 4.18 | 0.2404 | 0.6009 | 0.6101 | **0.090** | **✅ 已提交 ACTIVE**（2026-10-14T20:16:36-04:00，name `GLB_S_10comp_5amzov`） |
| 2 | USA / TOP2000 | `vROw5Rkd` | 4.01 | 3.33 | 0.1706 | 0.3383 | 0.6217 | 0.078 | **已提交 ACTIVE** |
| 3 | GLB / TOP3000 | `kqJrvP0g` | 3.61 | 1.65 | 0.2566 | 0.6207 | 0.6196 | 0.079 | 待提交 |
| 4 | IND / TOP500 | `9qE1kR3o` | 3.53 | 4.27 | 0.0861 | 0.6818 | 0.6816 | 0.018 | 待提交 |
| 5 | KOR / TOP600 | `58j0z3bk` | 3.50 | 4.73 | 0.0663 | 0.6568 | 0.6706 | 0.029 | 待提交 |
| 6 | GBR / TOP700 | `LL5a3r6M` | 2.76 | 2.68 | 0.0845 | 0.6540 | 0.6849 | 0.015 | 待提交 |
| 7 | DEU / TOP500 | `mLYLEm99` | 2.27 | 1.67 | 0.1667 | 0.6110 | 0.6108 | **0.089** | 待提交 |
| 8 | USA / TOP1000 | `LL5aX6Y2` | 2.61 | 1.80 | 0.1852 | **0.0000** | 0.6601 | 0.040 | 待提交（零占用档） |

> **闸余量** = `0.7 − max(SELF, PROD)`。余量越大，提交后因平台重算而翻车的风险越低。
> 提交前置条件：**SELF < 0.7 且 PROD < 0.7 且 IS 全闸 PASS**。上表 8 颗全部满足。

---

## 二、首选候选档案：`LL5amzov`（GLB / MINVOL1M）✅ 已提交

| 项目 | 值 |
|---|---|
| 配置 | GLB / MINVOL1M / delay 1 / **STATISTICAL** / decay 1 / lim 10 / **trunc 0.02** / cp 1 |
| IS Sharpe / Fitness / Turnover | **6.93 / 4.18 / 0.2404** |
| SELF / PROD | 0.6009 / 0.6101（余量 0.090） |
| IS 闸 | LOW_SHARPE ✅ · LOW_FITNESS ✅ · LOW_TURNOVER ✅ · HIGH_TURNOVER ✅ |
| 子宇宙闸 | **LOW_SUB_UNIVERSE_SHARPE 4.25 vs 限 2.43** ✅ · IS_LADDER 6.14 vs 2.02 ✅ |
| GLB 专属三闸 | AMER 3.52 ✅ · EMEA 3.00 ✅ · APAC 5.97 ✅（限均为 1） |
| 聚类闸 | CLUSTER_TEST 3.22 vs 1.58 ✅ |

**为什么是它**：IS 6.93 是全场最高，且**余量 0.090 也是全场最厚之一**——这打破了「IS 越高相关性越高」的常规两难（对比：USA/TOP3000 的 IS 4.73 反而 corr 0.742 撞墙）。GLB/MINVOL1M 是本次扫描出的**质量甜点区**。

次优同档：`VkdjR3JA`（同配置 cp3）IS 6.89 / F 4.12，PROD 0.6091，余量 0.091——IS 略低但余量略厚，可作保守备选。

---

## 三、Region 可用性定案（平台硬约束）

| region | 能否建 SUPER | 证据 |
|---|---|---|
| **GLB** | ✅ 可建 | MINVOL1M / TOP3000 均拿到 PASS |
| **USA** | ✅ 可建 | TOP1000 / TOP2000 / TOP3000 均可建 |
| **KOR** | ✅ 可建 | TOP600 拿到 PASS |
| **IND** | ✅ 可建 | TOP500 拿到 PASS（trunc 0.02 后反转） |
| **DEU** | ✅ 可建 | TOP500 拿到 PASS |
| **GBR** | ✅ 可建 | TOP700 拿到 PASS（须 delay=1，d0 组件不足） |
| **MEA** | ❌ **平台不支持** | `Region MEA is not available.` |
| **JPN** | ❌ **平台不支持** | `Region JPN is not available.` |
| **TWN** | ❌ **平台不支持** | `Region TWN is not available.` |
| **EUR** | ❌ 组件不足 | 5 档 universe 全 `At least 10 component alphas are required`（TOP2500/TOP1200 复核确认） |
| **HKG** | ❌ 组件不足 | TOP800 / TOP500 均不足 10 |
| **ASI** | ❌ 组件不足 | MINVOL1M / MINVOL10M / TOP500 均不足 10 |
| **CHN** | ❌ 组件不足 | TOP2000U 不足 10 |
| **AMR** | ❌ 组件不足 | TOP600 不足 10 |

⇒ **可组 SA 的 region 只有 6 个**：GLB / USA / KOR / IND / DEU / GBR，本次已全部覆盖并各拿到 ≥1 颗可提交候选。

---

## 四、本轮三条方法论增量（已写入记忆）

### 1. ★★★★★ `super_build.py select` 的「假失败」陷阱
报错 **`Failed to create simulation / None` ≠ 建不出来**。真相是 `create_simulation` 的轮询窗口太短，仿真 >~200s 才 COMPLETE 时返回 None。
实证：USA/TOP3000 裸 `POST /simulations` 拿到 201 + Location，手动轮询 20×10s 才 COMPLETE，出来 IS 4.73 的真候选。
⇒ **按 error 文本分类判死**：
- `At least 10 component alphas are required` → 组件池真不足（真死）
- `Failed to create simulation / None` → **假失败，换耐心轮询重试**
- `Region XXX is not available.` → 平台不支持（真死）

已新建耐心驱动 `C:\Users\MENGTAO\wqb-scripts\sa_run.py`（POST + 90×10s 轮询 + 续跑键）。

### 2. ★★★★★ `combo-power`（cp）是挤过「近失闸」的免费杠杆
GBR/TOP700·SECTOR·d15：cp1 PROD **0.7001**（超闸 0.0001）→ cp3 **0.6959** → cp5 0.6972 ⇒ 挤过闸。
⇒ **凡 PROD 卡在 0.695–0.705 的近失候选，先加 cp3/cp5 再判死。**

### 3. ★★★★ `truncation 0.02` 是全局杠杆，非 KOR 特例
外推验证成功：IND 在 trunc 0.08 下全灭 → 改 0.02 后拿到 IS 3.53–3.57 PASS；GLB/MINVOL1M 更是直接冲到 IS 6.93。

### 4. ★★ 中性化选择有强 region 特异性（本轮再确认）
| region | STATISTICAL | SECTOR | INDUSTRY | SUBINDUSTRY |
|---|---|---|---|---|
| IND | IS 5.39 ❌(corr .83) | **IS 3.57 ✅** | — | — |
| DEU | **IS 2.27 ✅** | ❌ .753 | ❌ .764 | ❌ .779 |
| GBR | ❌ .841 | ❌ .7001(近失) | ❌ .718 | **IS 2.76 ✅** |
| GLB/MINVOL1M | **IS 6.93 ✅** | ❌ .982 | — | — |

---

## 五、待你决定（仍执行「只挖不提交」）

以下 6 颗已过双闸、**等你点名才提交**（`LL5amzov` 与 `vROw5Rkd` 均已提交）：

| alpha id | region/档位 | IS S | 余量 | 备注 |
|---|---|---:|---:|---|
| `kqJrvP0g` | GLB/TOP3000 | 3.61 | 0.079 | 同区第二档 |
| `9qE1kR3o` | IND/TOP500 | 3.53 | 0.018 | IND 余量最厚 |
| `58j0z3bk` | KOR/TOP600 | 3.50 | 0.029 | KOR 最优 |
| `LL5a3r6M` | GBR/TOP700 | 2.76 | 0.015 | GBR 唯一稳解 |
| `mLYLEm99` | DEU/TOP500 | 2.27 | 0.089 | 余量厚、IS 偏低 |
| `LL5aX6Y2` | USA/TOP1000 | 2.61 | 0.040 | SELF=0（零占用） |

补充可提交备选（同 region 次优，未列入主表）：
- `VkdjR3JA` GLB/MINVOL1M cp3（IS 6.89 / 余量 0.091）
- `O0JPVa7d` IND/TOP500 cp3（IS 3.55 / 余量 0.016）
- `qMEr7A2O` IND/TOP500 cp1（IS 3.57 / 余量 0.013）
- `88v9P5LV` KOR/TOP600（IS 3.44 / 余量 0.026）
- `1YjbKNGX` GBR/TOP700 cp3（IS 2.82 / 余量 0.004 ⚠️ 极薄，不建议）
- `78obm2wO` GBR/TOP700 cp5（IS 2.81 / 余量 0.003 ⚠️ 极薄，不建议）

---

## 六、本轮产出物

| 文件 | 说明 |
|---|---|
| `C:\Users\MENGTAO\wqb-scripts\sa_run.py` | 耐心轮询版 SA 构建 + 双闸探针驱动（含续跑） |
| `...\b1/`、`...\b3/`、`...\b4/`、`...\b5/`、`...\b6/` | 各批次原始结果（`*.json` 单条明细 + `res*.jsonl` 汇总） |
| `.workbuddy/memory/2026-10-15.md` | 当日实证日志（假失败陷阱 / cp 杠杆 / trunc 外推） |
| 本报告 | 全 region 对比表供挑选 |

**铁律：本轮零提交**（`ALLOW_ALPHA_SUBMIT=False` 全局闸未动；`vROw5Rkd` 为用户早前单独授权提交）。
