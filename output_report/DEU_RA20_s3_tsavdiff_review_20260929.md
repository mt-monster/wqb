# DEU RA20 战役 S3 复盘 — tsavdiff 探针批判定（2026-09-29）

## 1. 结论先行

| 信号线 | 状态 | max\|S\| | 判定依据 |
|---|---|---|---|
| pattern_scores | **判死** | 0.43（30 条） | < 0.5 快判死线；2Y 结构性衰减（EUR 同源线 diag8 亦证实 2Y 硬墙） |
| pv30 | **判死** | 0.35（20 条） | < 0.5；multiply 门控族全部 CONCENTRATED_WEIGHT FAIL（longCount 4-7 ≪ 80） |
| other455 | **存活（弱）** | **0.77**（18 条） | ≥ 0.5；ts_av_diff 均值回归主线确认，但距可提交（S≥1.58）极远 |

**S3 总判定：三线两死一弱，0 颗可提交。** other455 主线方向成立但强度不足，需 S4 Mode B 改造或按纪律转向（用户裁决，见 §5）。

## 2. tsavdiff 8 探针批逐条结果（DEU/TOP500/d1/decay4/SUBINDUSTRY/trunc0.08）

| 候选 | 结构 | alpha | S | F | T | 2Y | SUB(闸) | 备注 |
|---|---|---|---|---|---|---|---|---|
| 50001 | `subtract(ts_mean(F,22),F)` | A1NoNvNE | **+0.77** | 0.44 | 0.043 | 0.98 | 0.17 FAIL(0.37) | **主线正式** |
| 50002 | `multiply(-1,ts_av_diff(F,22))` | ZYbObAA3 | **+0.77** | 0.44 | 0.044 | 0.98 | 0.17 FAIL(0.37) | 与 50001 同一信号反号验证 |
| 50003 | `group_rank(subtract,subindustry)` | rKOZOeO3 | +0.70 | 0.34 | 0.040 | 0.99 | 0.48 **PASS** | 分组轴包裹有效 |
| 50004 | `ts_rank(subtract,252)` | N1aYaVap | +0.51 | 0.18 | 0.167 | -0.02 | 0.23 FAIL(0.24) | KOR 已验证形态在 DEU 弱化 |
| 50005 | fact2(w1) 变体 | 0mX1XrrK | +0.63 | 0.34 | 0.037 | -0.33 | 0.51 PASS | 字段衰减 |
| 50006 | customer 变体 | LLN0NeJ9 | -0.16 | -0.04 | 0.023 | 0.40 | PASS | 该字段无信号 |
| 50007 | partner 变体 | VkaAanJ5 | **-0.61** | -0.32 | 0.043 | -0.43 | PASS | **反向信号**，翻向即 +0.61 预期 |
| 50008 | `subtract(ts_mean(F,66),F)` | 58zPzRWX | +0.63 | 0.33 | 0.031 | 0.82 | 0.15 FAIL(0.30) | 窗稳健性成立（66 略衰） |

（F = `oth455_relation_n2v_p10_q200_w4_pca_fact1_value` 主字段；全部 CONCENTRATED_WEIGHT PASS，longCount 124-151）

## 3. 关键实证

1. **翻向验证精确命中**：原式 `ts_av_diff(F,22)` S=-0.77（e7bX02Ll，救援批）→ `multiply(-1,·)` S=+0.77（ZYbObAA3）。均值回归方向确认：**偏离滚动均值 → 回归**。
2. **SUB 是比值闸，比例随区域变化**：DEU 实测 limit ≈ **0.47–0.48 × S**（0.37/0.77、0.24/0.51、0.30/0.63），**低于 GBR 记忆值 0.571**——不可跨区外推。
3. **持仓健康**：tsavdiff 平滑族 100% CONCENTRATED_WEIGHT PASS，与 pv30 multiply 门控族（longCount 4-7 全 FAIL）形成干净对照——**multiply 门控 = 持仓集中**再次互证。
4. **字段方向异质**：relation fact1 正向 0.77 / fact2 0.63 / customer 无信号 / **partner 反向 -0.61**——同数据集内均值回归方向按字段族翻转，S4 的翻向变体有明确标的。
5. 全部 8 条 LOW_SHARPE（≤0.77 ≪ 1.58）+ LOW_FITNESS + LOW_2Y_SHARPE 三杀，Mode B 线门槛（S≥1.25 & F≥0.8）未达。

## 4. 工程修复（本场战斗的前置障碍，已根治）

- **SAFE_DELETE 守卫截杀 pipeline**（秒退 exit 1、stderr 仅守卫 JSON、targets 指认 `dbwrite.lock.json`）：根因 = 写锁/七槽 token 用 `os.unlink` 放锁，同 turn 删除数越阈值 100 被沙箱守卫截杀。**根治**：三文件（`src/wqb/db_write_lock.py`、toolkit `_lib/dblock.py`、`_lib/slots.py`）共 8 处 unlink/remove → `os.replace(…, ….stale)` 退役（文档规定姿势），sync 5 安装位，零删除冒烟全绿。
- probe_batch_mode 三修复：失败输出全文回显（3000 字符）/ cwd 仓库根 / `_fetch_batch_results` 只看本批表达式（陈旧行判定污染根治——PROBE_DEAD "无回测结果"即此机制诚实报信，实为待 harvest）。
- **收批纪律**：pipeline 结果只落 checkpoint，`harvest_multisim_alphas`（平台）→ `harvest_multisim_results`（DB）两步收批后方可判定。本批 8 条已收（linked 5+3）。
- 残留清理项：25 条 cluster GROUP 坏式被再派发再隔离（dispatch 池污染，建议永久标 fail/dropped）；`gem.py:1449`、`gen_field_inspect_packs.py`、`campaign_intel.py:1001` 三处同型 unlink 地雷待清；`tools/_tmp_*.py` 一次性脚本已入回收站。

## 5. S4 方向（待用户裁决）

| 选项 | 内容 | 预期 |
|---|---|---|
| **A. other455 Mode B 改造** | ① 价差结构 `subtract(rank(relation),rank(partner))`（关系动量 vs 合作伙伴动量价差，单一价差信号合规、有经济含义）② market/exchange 分组轴破 SUB 比值闸 ③ partner 翻向变体（预期 +0.61）④ 事件门控 trade_when | S 0.77→1.25+ 需结构性增强；方向已验证，边际期望中等 |
| **B. 转向新数据集** | tsavdiff 族已测 18 种结构（10 救援 + 8 探针），按"10 结构无果才转向"纪律已过线；DEU 绿榜剩余（analyst 系/insiders）开新线 | 重开快判死循环，边际期望未知 |
| **C. A+B 并行** | 8 探针配额对半分：4 条 A 价差结构 + 4 条 B 新数据集首探 | 分散风险 |

（提交配额不受影响：本轮 0 颗进入提交判定；ET REGULAR 配额仍为 4/日）
