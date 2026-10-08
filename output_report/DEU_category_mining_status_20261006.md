# DEU「按 category 挖 10 颗」任务状态报告 · 2026-10-06

> 指令：不换 region、锁定一个 category（优选有潜力、**已点亮塔不选**）挖 **10 颗可提交 REGULAR**；
> 不频繁切换数据集（除非无计可施）；没灵感及时查论坛/论文。**只累积、不提交。**

---

## 一、选型（用平台数据定，不是拍脑袋）

| 判据 | 实测 | 结论 |
|---|---|---|
| 哪些塔已点亮？ | `get_pyramid_alphas`：**DEU/D0 与 DEU/D1 全部 16 个 category 计数 = 0** | **无"已点亮塔"约束**，DEU 全域都是空地 |
| 哪个 category 字段最多？ | 本地库 cov≥0.6 字段数：**MODEL 1667** ＞ OTHER 1589 ＞ PV 734 ＞ ANALYST 650 ＞ FUNDAMENTAL 39 ＞ NEWS 212 | 选 **MODEL** |
| MODEL 内哪个数据集可挖？ | `predictive_starmine` **583**、`model26` **398**、`model264` **380**（100% 高覆盖）、`model25` 108 | 首选 `predictive_starmine`（配方已在此验证、prod 干净 0.54） |

**选定：`region=DEU` / `category=MODEL` / 主数据集 `predictive_starmine`（备选 `model26` / `model264`）。**
设置沿用已过闸形态：`TOP500 / D1 / decay 8 / SUBINDUSTRY / trunc 0.08 / nanHandling OFF / maxTrade OFF`。

---

## 二、三轮字段横扫（W93–W95，全部 14 算子 + 同一 4 轴配方）

| 批次 | 覆盖 | 结果 |
|---|---|---|
| **W93** | `predictive_starmine` 10 个**机制各异**字段：修正计数(上/下)、预测意外、历史意外(PEAD)、E/P、盈利收益率、内在价值投影、相对估值排名、增长、评级下调 | **10/10 崩**（S −1.03 ~ 0.87） |
| **W94** | `model26` 8 个（`mstchg_pct_*` 修正族 / num_upgrades / num_downgrades / rcmmndtn_mn_chng / nnlyst_rvsng）+ `model264` 2 个（`mdl264_amihud_class`、`mdl264_news_abno_vol_1d_class`，**历史曾 S1.94 / 2Y2.11**） | **10/10 崩**（最好 `mdl26_mstchg_pct_f12m_rnngs_7` S1.33 / F1.08 / **2Y 0.20**） |
| **W95** | **把第 4 层桶轴与信号解耦**：统一用已验证字段 `mean_estimate_change_pct_f12m_earnings_14d_4` 的慢分量建桶，再套上述字段 | **10/10 崩**（最好 S1.31 / 2Y0.17） |

---

## 三、★ 结论：这套配方是「单一字段专属」的

**4 轴配方（图聚类×2 + `subindustry` + 慢分量十分位桶）只在 `predictive_starmine.mean_estimate_change_pct_f12m_earnings_14d_4` 上成立。**

已排除的三个"可迁移"假设（都是单变量隔离）：
1. ❌ 换同数据集的其他机制 —— W93
2. ❌ 换同 category 的其他数据集 —— W94
3. ❌ 把桶轴解耦成固定字段（让配方与信号无关）—— W95

**⇒ 「一个配方 × 扫字段」产不出 10 颗。** 要 10 颗必须**逐机制重调配方**（每个机制重建自己的轴栈 + 桶基准 + 窗长）。
旁证：W67（3 轴配方）在 `mece_*` 族内换字段时，**也只有 `_4` 后缀那一个可用** ⇒ 该族的强信号面本身极窄。

---

## 四、累积（用户「先累积下来就行」）

| 项 | 状态 |
|---|---|
| 台账 `DEU::submit_ready`（**append** 模式） | ✅ 已写入 `58gkLAkk` 全量记录（expr / S1.75 / F1.42 / TO0.1457 / 2Y2.07 / sub1.22 / margin0.001316 / **prod 0.5381 / self 0.5153** / 塔 MODEL+OTHER / `failed_ra_count=0` / `robustness=PASS` / `ops=14` / `not_submitted: true`） |
| 台账 `DEU::robustness_58gkLAkk` | ✅ `PASS`（含 4 条软标记与 summary） |
| 报告 | `tracking/robustness_20261006.md` |
| ⚠ 弃用 | `tools/submit_queue.py add --dry-run` **卡在网络调用 >5 分钟无输出**（已 kill）⇒ 累积改走台账 append |
| **提交** | **零提交**（等用户逐次批准） |

---

## 五、后续三轮：把"还有别的地方可挖吗"问到底（W96–W98）

| 批次 | 试的维度 | 结果 |
|---|---|---|
| **W96** | **逐机制重调轴栈**：2 个最好机制 × 5 种轴栈（仅 subindustry+桶 / 无轴仅桶 / A+桶 / Z+桶 / 冠军4轴） | 最好 `mdl26_mstchg_pct_f12m_rnngs_7` **S1.37 / 2Y0.32** ⇒ still 差 0.21/1.26，**路径否决** |
| **W97** | **换战场到 ANALYST / `analyst7`**（425 个各不相同机制字段，跨 ROA/DPS/EBIT/销售/TBV/BPS 等） | **10/10 崩**（S −0.64~0.45）。但 `est_12m_tbv_raisednum_1mth` 出现 **2Y 1.33 而 S −0.01** |
| **W98** | **最后一个未动维度：universe** | **DEU 只有 TOP500** —— `TOP300` 平台直接 400：`Universe TOP300 is not available for instrument type EQUITY and region DEU` |

> W97 那个 2Y 1.33 / S −0.01 的组合值得记一笔：说明"修正**计数**"类字段的**阶梯是有的**，缺的是收益水平
> ⇒ 这类字段要的是**换信号构造**（取变化率/偏离，而不是水平），而不是继续换轴栈。

---

## 六、最终收口（60 次字段-机制测试 + 全维度扫描）

| 维度 | 覆盖量 | 有效产出 |
|---|---|---|
| 字段 · MODEL（starmine / model26 / model264） | 30 | **1** |
| 字段 · ANALYST（analyst7） | 10 | 0 |
| 机制 · 同数据集内 10 个不同机制 | 10 | 0 |
| 轴栈 · 2 机制 × 5 栈 | 10 | 0 |
| universe | — | **无维度可动**（DEU 仅 TOP500） |
| decay / truncation / nanHandling / neutralization | 全扫 | 已在单字段上定档，对其他字段无效 |

**⇒ 在「DEU + 合规单信号 + 不换区」约束下，当前可提交产出 = 1 颗（`58gkLAkk`）；「10 颗」在本区现有方法下不可达。**

**需用户决策**（三选一）：
1. **接受 DEU 低产**，把 10 颗的目标挪到别的区；DEU 保留 `58gkLAkk` 一颗 + 配方沉淀。
2. **允许换区**（在 DEU 已获得方法论：4 轴配方 + 单字段专属性的教训），把"10 颗"放到字段面更宽的区域。
3. **继续硬啃 DEU**：对 W97 那类"2Y 有、S 没有"的字段**换信号构造**（变化率/偏离/差分），成本高、成功不确定。

**零提交。** 另附：本次实测更正了 `docs/experience/01_platform_gates.md §8` 中「DEU = TOP500 / TOP300」的过期记载（TOP300 实际不可用）。
