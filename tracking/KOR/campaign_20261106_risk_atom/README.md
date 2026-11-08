# KOR × RISK × ATOM 战役（2026-11-06）

> **目标**：在 KOR 区域、固定 TOP600 / Delay=1，从 **Risk 类数据集**产出 **10 个 ATOM 类型 REGULAR alpha**。
> **用户约束**：① region 固定 KOR；② 不频繁切数据集；③ 阻塞时查论坛/论文；④ 数据集覆盖可动态调整但**近十年都要有数据**；
> ⑤ 开波并发 `create_multi_simulation` **限 2**；⑥ 能用 MCP 不写临时脚本；⑦ prod 必须用 MCP 查；
> ⑧ 禁 PV/MODEL/OTHER 两两组腿（跨 category 组合总量 ≤5）。
> **设置档**：KOR / TOP600 / Delay=1 / decay 1 / trunc 0.04 / unit VERIFY / nanHandling ON / pasteurization ON / maxTrade OFF
> （中性化按波次分档对照：STATISTICAL / INDUSTRY / CROWDING / SLOW）

## 文档索引

| 文件 | 内容 |
|---|---|
| [s0_dataset_scan.md](s0_dataset_scan.md) | **S0**：7 个 Risk 数据集全量扫描 + 候选裁定 + 用户约束映射 |
| [s1_field_profile_risk70.md](s1_field_profile_risk70.md) | **S1**：risk70 **96/96 字段画像**（类型 / 覆盖 / 频率 / 形态 / 可用性）+ 五问 + 4 条机制 A-2 声明 |
| [s1_field_profile_risk88.md](s1_field_profile_risk88.md) | **S1**：risk88 **64/64 字段画像**（独立 vendor 模型口径）+ 机制声明 |
| [s1_field_profile_other_risk.md](s1_field_profile_other_risk.md) | **S1**：risk59 / 60 / 68 / 71 / 72 **全字段画像**与逐字段裁定 |
| [waves.md](waves.md) | **S3/S4 波次台账**：每波设计、读数、归因、准入/禁碰、中性化档扫描 |
| [final_report.md](final_report.md) | **交付**：按用户澄清口径重建的 **10 颗 ATOM 候选池**（self<0.7 / prod<0.7 / 两两互相关<0.7）+ 数据集 · 核心字段 · 算子逻辑 · 回测指标 · 画像索引 · 排除名单 |

## 关键进展（滚动更新）

| 阶段 | 结论 |
|---|---|
| S0 | risk70（96 字段 / aC 8018）+ risk88（64 字段）为主攻；risk59 因 **2014 空年**（仅 9 年）降级；risk60/68/71/72 继承判死 |
| S1 | risk70 头部轴 = **`anlystsn`（分析师情绪风格载荷，αC 2922）**；wave 214 只打过 IVOL 轴（0.73）⇒ 方向纠偏 |
| R1 | **`anlystsn` 水平 + P-ATOM-1 / INDUSTRY = S 1.11 / 2Y 1.78 / 10 年覆盖 PASS**（risk 塔史上首颗 S>1 且 2Y 过闸） |
| R2 | 参数级微调天花板 ≈1.14；**STATISTICAL 档全灭（0.66–0.88）** ⇒ 中性化档是第一杠杆 |
| R3 | **CROWDING + `vector_neut(resvol)` = S 1.23 / F 0.86 / 2Y 2.13 / subU 1.09 / inv 1.05** |
| R8 | 正交化目标扫描：`momentum` **1.29** ≫ resvol 1.23 ≫ size/beta/ltreversl 0.10–0.15（归零） |
| R12 | **中性化 = `REVERSION_AND_MOMENTUM` ⇒ S 1.49 / F 1.08（F 首次过闸）** |
| R13/R14 | `winsorize std` 甜区 0.32–0.42 + pow 甜区 1.5–3.0 ⇒ **10 颗 RA 全闸通过**，最佳 `E56Nk0wL` S 1.63 / F 1.25 / 2Y 2.23（⚠ 同参数族，按用户澄清**不构成交付池**） |
| 终验 | 按「self<0.7 / prod<0.7 / 两两互相关<0.7」重建候选池：**10/10 合规**；self max 0.4247、prod max 0.6898、池内互相关 max 0.6007（`compute_mutual_correlation` 4y/1023d） |
| 交付 | [final_report.md](final_report.md)：**10 颗 ATOM 候选池**（4 数据集 / 9 字段 / 6 几何）+ 字段画像索引 + 机制声明 + 排除名单 + prod 排队台账。提交权归用户，本轮不提交 |
