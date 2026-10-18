# 「画像驱动骨架选择」整改方案（待审核）

> 缘起（2026-10-09 用户明令）：「你为什么总是用同一套骨架，一定要看多样性」+
> 「我一直的意思是针对不同的字段的画像用不同的骨架」+「你先给我做好方案，从画像开始一步步我还要审核」。
>
> **现状铁证**：GBR 1,004 个被测字段中 **64%（645 个）只见过 1 种骨架**；606 个 DEAD 中 **69% 是单骨架单次测量**。
> ⇒ 「DEAD」实际只是「这套骨架下不行」——判死证据不足。

---

## 〇、核心原则（本方案的总纲）

> **字段画像（sem_type / field_type / coverage / 波动属性）决定该字段配哪一族骨架；
> 判一个字段「死」之前，必须让它见过与其画像匹配的全部骨架族。**

- **初筛（screening）**：每字段 ≥2~3 个**不同族**骨架，且必须是「它没见过的族」；
- **深挖/参数扫**（已锁定字段扫同族变体）：允许同模板，但发批时须显式声明 `--param-sweep`；
- **判死升级**：`n_skeletons == 1` 的 DEAD 不再是终局判定，降级为「低置信」，进入复活候选池。

---

## 一、Phase 0 —— 画像层补齐（纯本地计算，零回测成本，~30 分钟）

**目标：让画像能直接回答三个问题 —— 这字段该配哪几族骨架？见过哪几族？还差哪几族？**

| 步骤 | 动作 | 产出 |
|---|---|---|
| 0.1 | `field_profile_perf` 增加 `n_skeletons` / `skeletons_seen` 两列 | 从 `backtest_results.code` 做模板归一（算子保留、字段/数字/分组名占位化）后按字段去重统计 |
| 0.2 | DEAD 系列加置信度：`n_skeletons==1` ⇒ 标 `low_conf` | 不改 verdict 值，先加列；报表侧把 DEAD 拆成「高置信死 / 低置信死」 |
| 0.3 | 每字段计算 `required_families`（由 `sem_type` × `field_type` 查映射得）与 `skeleton_gap = required − seen` | 画像新增「骨架缺口」视图 |

**🔍 审核点①（Phase 0 完成后停下）**：
- 抽样报表：`analyst7` / `pv47` / `techindi_model` / `pattern_scores` 各 5 行，展示「字段 → 语义 → 应配骨架族 → 已见 → 缺口」全链；
- DEAD 置信度重分布（预计 606 → 高置信 ~190 / 低置信 ~419）。

**验收标准**：任意字段可机读回答「该用什么骨架试过没有」；不改变任何现有 verdict 数值。

---

## 二、Phase 1 —— 骨架面板与「语义→骨架族」映射审核（制度的地基，必须你过目）

**已完成的部分**：`tools/fields/skeleton_panel.py`（治理校验已通过，FAIL=0），内含 **10 族骨架**：

| 族 | 一句话 | 适用画像 |
|---|---|---|
| `level_rank` | 水平直排（house 基准） | ratio / percentile / probability / score |
| `delta` | 时序差分 ts_delta(·,66) | estimate_level / sentiment / 事件型 |
| `ts_rank` | 时序分位 ts_rank(·,252) | 有自身历史定位意义的量 |
| `ts_zscore` | 时序标准化 | level_amount（价格/金额等非平稳量） |
| `decay_linear` | ts_decay_linear(rank,5) | ratio / percentile（替代换手压法） |
| `gn_first` | 原始信号先 group_neutralize | **count**（家数类必须先去共同成分） |
| `av_diff` | ts_av_diff(·,22) 偏离自身均值 | 通用补充 |
| `double_window` | add(ts_mean 1, ts_mean 120) | percentile / ratio（合规五形态之一） |
| `hump` | ts_target_tvr_hump | genius 族换手压法对照 |
| `quantile` | ts_quantile(·,252) | score / 分布型 |

**语义→优选骨架族映射（`SEM_PREFERRED`，按 GBR 实证初拍）**：

```
count           → gn_first / level_rank / delta
ratio           → level_rank / ts_rank / decay_linear
percentile      → level_rank / decay_linear / gn_first
level_amount    → ts_zscore / ts_rank / delta
score           → level_rank / ts_rank / quantile
probability     → level_rank / ts_rank / decay_linear
sentiment       → delta / ts_zscore / level_rank
estimate_level  → delta / level_rank / ts_zscore
revision_change → level_rank / delta / ts_rank
dispersion      → level_rank / ts_rank / decay_linear
unknown         → level_rank / delta / ts_rank（兜底三族）
```

**🔍 审核点②（最关键的一处审核）**：这张映射表就是「什么画像配什么骨架」的规则本体。
其中 `count→gn_first`、`level_amount→ts_zscore` 有 GBR 实证支撑；其余是按量型性质推断。
**请你裁决：是否认可此映射，或指出要调整的格子。**（Phase 3 的复活补测将严格按这张表配骨架。）

---

## 三、Phase 2 —— 发批制度接入（已就位，待你确认阈值）

发批流程新增**第 7 闸：骨架多样性审计**（在 op-arity / expr-lint 之后）：

```bash
$WQ_PY tools/fields/skeleton_panel.py audit --path <wave.txt>          # 初筛波：强制
$WQ_PY tools/fields/skeleton_panel.py audit --path <wave.txt> --param-sweep  # 深挖波：显式豁免
```

已实测：多样化初筛波（8 模板）✓ 通过 ｜ 同模板参数扫波（1 模板 100%）✗ 正确拦截。

**🔍 审核点③**：阈值 `min-families ≥ 3`、`单模板占比 ≤ 60%` 是否合适（8 条一批的口径下）。

---

## 四、Phase 3 —— 复活补测（唯一有回测成本的阶段，分批、逐批给你过目）

按「骨架缺口」从小到大、价值从高到低排序执行：

| 批次 | 对象 | 配对方式 | 规模估算 |
|---|---|---|---|
| **3a** | **WEAK 47 个**（最接近闸线，复活期望最高） | 每字段配 2 族「它没见过的」优选骨架 | 94 条 ≈ **12 波 ≈ 1 小时** |
| 3b | DEAD 中 best_s ∈ [0.9, 1.10) 的（临界线） | 同上 | 待 Phase 0 统计（估 ~60–90 个字段） |
| 3c | UNKNOWN_COVERAGE 中 coverage 待复核但语义有效的 | 沿用 §190 的实测裁决路径 | 另立方案 |
| 3d | 其余单骨架 DEAD（419 个） | 每字段 1 族最匹配骨架抽检 | 按 3a/3b 复活率决定是否推进 |

**🔍 审核点④**：3a 的完整配对清单（47 字段 × 各 2 族骨架，逐条列出）+ 波数预算，**确认后才发批**。

---

## 五、Phase 4 —— 回归与固化（~20 分钟）

1. 重建画像，出**复活率报告**：单骨架 DEAD/WEAK 在匹配骨架下的复活比例（这是「骨架错配假死」规模的首次直接测量）；
2. 用实测结果**回归校正 SEM_PREFERRED**（产出「sem_type × 骨架族」真实产出矩阵，替换我拍脑袋的格子）；
3. 写入 skill `_field-profile-playbook.md §11` + `RULES.md`，并同步 6 个安装位。

---

## 六、本方案已完成的先行项（不再重复做）

- ✅ `tools/fields/skeleton_panel.py`（10 族面板 + audit + gen），治理 FAIL=0，已登记 README；
- ✅ 顺手修复并发会话遗留的治理 FAIL×2：`operator_coverage_audit.py` 迁位 `tools/gates/` 并修正 5 处引用（迁移后冒烟测试通过）；
- ✅ 骨架偏差量化：645/1,004 字段（64%）只见过 1 种骨架（本方案 Phase 0 将把它落成画像列）。

## 七、执行节奏约定

**每个审核点我都会停下等你裁决**：① → ② → ③ → ④（④确认后才烧回测配额）。
Phase 0 零成本，可随时推翻；Phase 3 是唯一烧波次的阶段，放在你确认映射表之后。
