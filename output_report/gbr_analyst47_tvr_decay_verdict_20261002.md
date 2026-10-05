# GBR analyst47 顶点修复：ts_target_tvr_decay 三源验证与穷尽定案

> 日期：2026-10-02 ｜ 区域：GBR ｜ 目标 alpha：`A1v1MKmW`
> 起因：用户问「`ts_target_tvr_decay` 和查论坛经验或开源金融经验都尝试了吗」

---

## 0. 结论（一句话）

**全部尝试完毕，`ts_target_tvr_decay` / `ts_target_tvr_hump` 救不了 F。**
`A1v1MKmW` 的 **F = 0.97 是该信号的全局峰值**，35+ 种配置无一达到 `F ≥ 1.0`（门槛）。

---

## 1. 基线（差 0.03，即 3%）

| 指标 | 值 | 闸 | 判定 |
|---|---|---|---|
| Sharpe | 1.96 | ≥1.58 | ✅ |
| **Fitness** | **0.97** | **≥1.0** | ❌ **唯一失败** |
| Turnover | 0.1896 | — | ✅ |
| Returns | 0.046 | — | ✅ |
| 2Y Sharpe | 1.73 | ≥1.58 | ✅ |
| Sub-Universe | 1.32 | — | ✅ |
| prod / self | 0.47 / 0.04 | <0.7 | ✅ 双净 |

设置：`GBR / TOP700 / d1 / decay2 / STATISTICAL / trunc0.08 / maxTrade ON / nanHandling ON`
表达式：`signed_power(ts_quantile(anl47_rawsentiment, 504), 0.3)`

**定量靶心**：`F = S × √(|R| / max(T, 0.125))`。保 S=1.96 时只需 **T ≤ 0.1767**（换手降 6.8%、夏普不掉）即可过闸。

---

## 2. 三源验证（L1 项目实证 / L2 论坛 / L3 论文）

### L2 论坛（`search_forum_posts`，30 条高票实证）
| 帖子 | 赞 | 关键证据 |
|---|---|---|
| 如何拯救高 turnover 因子 | 179 | `ts_target_tvr_decay(expr, lambda_min=0, lambda_max=1, target_tvr=0.05)` 实战降换手 |
| 降换手 ≠ 稳健 | 45 | **「无脑加 `ts_decay_linear` 压换手 → sharpe 没保住、base 反而更难看」** |
| GLB Labs 实战 | 91 | tvr_decay 可把换手 1.17% **反向提**到 4%（双向可调） |
| JPN Cluster Alpha（2.8% 换手） | 16 | **「仿真层 Decay=0，换手控制全交给表达式内这条栈」** |
| 换手率是隐形天花板 | 23 | 公式原文 `fitness = sharpe × sqrt(ret / max(tvr, 0.125))` |
| PPAC 优化 Turnover | 34 | 用后「Turnover 27%、Margin 10%、**Fitness/Drawdown 也略有提高**」 |

### L3 arXiv（`arxiv_api.py -c q-fin`）
命中机制命名：**2502.04284《On the Effect of Alpha Decay and Transaction Costs on the Multi-period Optimal Trading Strategy》**
→ 机制 = **交易成本下的多期最优交易 = 部分调整**，调整速度由 **α 衰减率 / 成本比** 决定。
与论坛一致：**平滑只在「衰减损失 < 成本节省」的区间内为正收益**。

### L1 项目实证
- 设置层全谱（decay / 窗 / 中性化 / trunc / trade_when）已穷尽，F=0.97 为局部最优。
- 本仓历史 17 条 `ts_target_tvr_*`（跨 CHN/IND/USA/JPN/DEU）**几乎全 `dropped`**，仅 4 条有分、最高 F=0.47 → **无正先例**。

---

## 3. 实测结果（3 条 multisim，15 个 alpha，全部 COMPLETE）

### A 批：设置 `decay=0`（论坛最佳实践）
| 表达式 | S | **F** | T | R | 2Y |
|---|---|---|---|---|---|
| 对照 base（无算子） | 1.92 | 0.90 | 0.2053 | 0.0454 | 1.70 |
| tvr_decay 0.125 | 1.28 | 0.65 | 0.1209 | 0.0324 | 0.61 |
| tvr_decay 0.15 | 1.49 | 0.76 | 0.1400 | 0.0362 | 0.87 |
| tvr_decay 0.175 | 1.68 | 0.84 | 0.1584 | 0.0397 | 1.08 |
| tvr_decay 0.19 | 1.75 | 0.87 | 0.1685 | 0.0412 | 1.22 |
| tvr_hump 0.15 | 1.31 | 0.63 | 0.1424 | 0.0330 | 0.29 |
| tvr_hump 0.175 | 1.40 | 0.64 | 0.1621 | 0.0341 | 0.39 |
| tvr_decay 0.15（λmax=5） | 1.49 | 0.76 | 0.1405 | 0.0362 | 0.87 |

### B 批：设置 `decay=2`（与基线同）
| 表达式 | S | **F** | T |
|---|---|---|---|
| tvr_decay 0.125 | 1.23 | 0.62 | 0.1178 |
| tvr_decay 0.15 | 1.43 | 0.73 | 0.1354 |
| tvr_decay 0.175 | 1.60 | 0.80 | 0.1515 |
| tvr_hump 0.15 | 1.31 | 0.65 | 0.1357 |
| tvr_decay 0.15（λmax=5） | 1.43 | 0.73 | 0.1355 |

**读法：F 随 `target_tvr` 单调递增，且 13 条无一条超过基线 0.97。**

### 机理裁决（可复用）
1. **F 随 target_tvr 单调递增** ⇒ 换手降得越狠、S 掉得比 `√(R/T)` 涨得快 ⇒ **平滑净损失**。
2. **算子只会"加平滑"、无法放松**：`target_tvr=0.19` 高于自然值 0.1896，实际仍被压到 T=0.1685。
3. **decay 设置与算子叠加 = 双重平滑**（B 批同 target 全略差于 A 批）。
4. **2Y 与 T 同向崩塌**（1.70 → 0.61）⇒ 抹掉的是**真实预测力**，不是噪声 ⇒ 不可救。
5. **⭐ 可复用判据**：**当平滑导致 2Y sharpe 同步崩塌时，decay / tvr 类旋钮必然无效**；只有换**信号结构 / 字段**才有救。

---

## 4. 穷尽清单（35+ 配置，无一达 F ≥ 1.0）

| 杠杆 | 测试档位 | 最优 / 结论 |
|---|---|---|
| settings decay | 0 / 2 / 12 / 25 / 100 | **2**（F 0.97） |
| ts_quantile 窗 | 378 / 504 / 756 | **504** |
| truncation | 0.02 / 0.08 / 0.15 | **三档完全同值（零影响）** |
| neutralization | STATISTICAL / SECTOR / MARKET / REVERSION_AND_MOMENTUM / CROWDING | **STATISTICAL**（余 0.65~0.67） |
| delay | 0 / 1 | **1**（D0 门槛×1.7，见下） |
| universe | 仅 TOP700 合法 | **无杠杆** |
| trade_when 门控 | < −0.01 / < −0.02 | ✗ 毁夏普（1.07 / 0.91） |
| **ts_target_tvr_decay** | 0.125/0.15/0.16/0.175/0.19 × λmax(1/5/10) × decay(0/2) | ✗ 最优 0.87 |
| **ts_target_tvr_hump** | 0.14/0.15/0.175 | ✗ 最差（0.63~0.65） |
| signed_power 指数 | 0.2 / 0.3 / 0.5 / 0.7 | **0.3**（0.5→0.94） |
| group_rank(subindustry/industry) | — | ✗ 摧毁（0.24 / 0.30） |
| ts_backfill(252) | — | ✗ 0.80 |
| winsorize(std=4) | — | = no-op（量子化信号无 4σ 离群） |
| 同族字段 | `anl47_indicator`(cov1.0) / `totalrawsignal` / `rawalphadecay` | ✗ 0.76 / 0.79 / −0.60 |

---

## 5. 两个重要新事实

1. **`delay=0` 不是捷径，是「高倍率 + 高门槛」档**：D0 的闸门阈值**整体 ×1.7** ——
   `LOW_SHARPE` 限 1.58 → **2.69**、`LOW_FITNESS` 限 1.0 → **1.5**、pyramid 倍率 1.6 → **1.9**，且多一个 `D0_SUBMISSION` 检查。
   ⇒ **D0 要求 F ≥ 1.5，比 D1 难得多**，不要当成"绕开 F 闸"的通道。
2. **GBR 只有唯一合法 universe = TOP700**（`config.REGIONS['GBR'].universes == ['TOP700']`）⇒ universe 不是 GBR 的杠杆（对比 EUR 5 档 / USA 6 档）。

---

## 6. 定案与建议

- **`A1v1MKmW` 的 F=0.97 是全局峰值，无杠杆可破**；与项目台账 `gbr_campaign_final_20260930`「唯一存活资产=analyst47 顶点族（F 差 0.03）」完全一致。
- **GBR 新挖掘可提交 = 0**（203 集全图处置完毕）；`region_kb:GBR` 指出 **prod 才是 GBR 真高墙**（star_val 族 S 2.0+ 也全被 prod 0.84–0.90 锁死）。
- 决策选项（`gbr_pinnacle_disposition` 已记）：
  1. **HOLD 挂起**，等平台阈值变化或 F 手段更新（原台账推荐）；
  2. **用户放宽口径**授权提交（差 0.03）；
  3. **换区**：KOR（17 颗现成）/ GLB（38 颗）/ ASI（4 颗）。

### 沉淀
- 已写入 `Claude/skills/wq-brain-alpha-optimization-v1/references/structural-interaction-forms.md` F6 节：
  **目标换手族的适用边界 = 「平滑时 2Y sharpe 是否同步崩塌」**，并已 `sync_skills.py`（4 安装位一致）。
- 工作日志：`.workbuddy/memory/2026-10-02.md`。
