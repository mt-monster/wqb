# FINDING P102–P112（2026-11-08 夜 → 11-09）

## 一、本轮判死清单（新增 4 个集 + 1 个族）

| 目标 | 依据 | 结论 |
|---|---|---|
| **intraday_pv_feats · corr 族** | rKR8wXZE S1.93/F1.62/2Y1.95 全闸，但 prod **0.7827**；换 ts_mean 66 → prod **0.8965** | 族封死（墙 0.78，门 0.70） |
| **intraday_pv_feats · 非 corr 族** | P103 十条（slippage / momentum2-3 / std / skew / num）最高 S **0.68** | 判死 |
| **analyst44**（修订事件，520 字段） | WA1+WA2 十条最高 S **0.92**（breadth），ROA 0.45 / 交互 0.72 / 分歧度 0.10 | 判死（第 7 次证伪「aC 低 ⇒ 有信号」） |
| **fundamental93**（应计/递延税，37 字段） | FC1+FC2 十条 longCount **46–61** ⇒ 仪器覆盖率仅约 10%；S 全负，CONCENTRATED_WEIGHT 全中 | 判死（结构性覆盖不足） |

## 二、★关键铁律（本轮新增，跨区通用）

### 铁律 G：算子几何换不掉 prod 墙，只有信息内容能换
同一信号 `group_rank(ts_mean(X,22), industry)` vs `group_zscore(ts_mean(X,22), industry)`：
prod = **0.7827 vs 0.7869**（差 0.004），而 S 从 1.93 → 1.91。
⇒ 想把 prod 从 0.78 拉到 0.70，换 rank↔zscore／换 group 轴／换衰减都是白费；必须换字段族或换正交腿。
（与既有记忆「换平滑窗口不能破 prod 墙」一致，本轮把「算子几何」也一并证否。）

### 铁律 H：窗口拉长对 prod 通常是**反向**的
同一 X：ts_mean 22 → prod 0.7827；ts_mean 66 → prod **0.8965**（+0.11）。
短窗 ts_rank(10/22/66) 直接把 S 打到 0.6/0.0/0.97 并触发 HIGH_TURNOVER。
⇒ 长窗 = 更靠近生产池的慢变共同分量 ⇒ prod 升高。破墙要往「非常规信息」走，不是往「更平滑」走。

### 铁律 I：`get_datafields` 的 coverage 不是仪器覆盖率，必须看 longCount
fundamental93 的 coverage = 0.589–0.909，看着像全覆盖；实跑 longCount 只有 **46–61**（TOP600 的 10%）。
⇒ coverage 约等于**时间覆盖率**。判定数据集可用性只能靠实测 `metrics.longCount`，不能靠画像里的 coverage。

## 三、other455 画像（KOR / TOP600 / D1，1500 字段）

- 结构：`oth455_{relation}_{embedding}_w{1..5}_pca_fact{1,2,3}_value`（MATRIX，300 个）
  + 对应的 `kmeans_cluster_{5,10,20}` 标签（GROUP，1200 个）。
- relation ∈ {competitor, customer, partner, relation}；embedding ∈ {n2v_p10_q200, n2v_p50_q200, roam}。
- coverage 0.791，alphaCount 中位 **0**（几乎无人使用）。
- 机制：供应链/竞争关系图的 Node2Vec / Roam 嵌入 → PCA 潜在维度得分。
- 用法要点：MATRIX 得分当信号；GROUP cluster 标签当 `group_rank / group_zscore` 的**自定义分组轴**。
- 判读：与本区 prod 池（价量 / 财务 / 分析师 / 风险）正交，是本轮最有希望的新机制。

## 四、仍在飞的批次

| 批 | multisim id | 内容 |
|---|---|---|
| G1 | `1MgpNcUJ4pX91B1c8PlolLk` | 图嵌入：水平 / 三因子合成 / 跨关系 / 跨窗口 / 跨嵌入 |
| G2 | `30vbmo7tu4XjazE1bWzwcxY8` | 图嵌入：时序变化 / 簇内 rank / 簇内 z / 跨因子价差 / 时序位置 |
