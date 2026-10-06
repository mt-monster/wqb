# DEU · OTHER 类别 + 图聚类分组轴（2026-10-06 续）

> 设置：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 ｜ 探针：W46–W47（累计 47 波 ~330 条）｜**全部 UNSUBMITTED**

## 一、OTHER 类别盘点（×1.8）

43 个数据集，但**多数 cov=0 不可用**：`ai_news_scores`(105f) / `mmp_nlp_sentiment`(72f) / `news_sentiment_nlp`(23f) /
`event_sentiment_signals`(52f) / `other696`(220f) / `other78`(104f) 全部无覆盖；`order_book_imbalance`(256f) 仅 cov 0.227。

**唯一大而可用 = `other455`**：**1500 字段 / cov 0.9535 / aCnt 仅 22**（逐字段近乎未开发）。其构成为：

| 类型 | 数量 | 用途 |
|---|---:|---|
| `oth455_*_value` | **300**（MATRIX） | 图嵌入数值 → 可作单信号 |
| `oth455_*_cluster_N` | **1200**（GROUP） | **聚类归属键 → 可作分组轴** |

命名 = `oth455_<关系>_<方法>_<参数>_<输出>`：关系 ∈ {relation, customer, partner, competitor}（关系/客户/伙伴/竞对图）、
方法 ∈ {n2v=node2vec, roam}、参数 = p10/50/200 × q50/200 × w1~5 游走、输出 = `pca_fact{1,2,3}_value` 或 `*_cluster_{5,10,20}`。

## 二、W46：图嵌入作单信号 —— 弱

8 条全部归入 `DEU/D1/OTHER ×1.8`。最佳 `oth455_relation_n2v_p10_q50_w1_pca_fact2_value` **S0.60**（tvr 仅 **0.012**、margin 6.0bp）；
其余 −0.41~0.38。⇒ **嵌入值单信号不可用**（静态坐标，经济含义稀释）。

## 三、W47：★ 图聚类分组轴 —— 本战役首个让 prod materially 松动的杠杆

形态 = `group_rank / group_neutralize(‹信号›, oth455_*_cluster_N)`（记忆 §0「**换分组轴**」明文放行）。

| alpha | 表达式（简写） | S | F | tvr | 2Y | sub | CW | **prod** | 塔数 |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| **qM0lKnvj** | `group_neutralize(vm_sector_pct, ‹relation…cluster_20›)` | **1.67** | **1.61** | 0.097 | 1.41 | 0.70 | ❌ | **0.896** | 2 |
| **RR68JNYj** | `group_rank(ts_backfill(vm_sector_pct,66), ‹同轴›)` | 1.61 | 1.51 | 0.121 | 1.26 | 0.66 | **✅** | 队列 | 2 |
| blOqYN2q | `group_rank(vm_sector_pct, ‹同轴›)` | 1.62 | 1.53 | 0.122 | 1.30 | 0.65 | ❌ | 队列 | 2 |
| leKlL7RN | `group_rank(vm, ‹customer…kmeans_cluster_20›)` | 1.46 | 1.30 | 0.104 | 0.50 | 0.72 | ❌ | — | 2 |
| leKlL728 | `group_rank(vm, ‹competitor…kmeans_cluster_20›)` | 1.08 | 0.84 | 0.102 | 0.98 | 0.60 | ❌ | — | 2 |
| QPKV1n2Q | `group_rank(vm, ‹competitor…cluster_10›)` | 1.12 | 0.93 | 0.115 | 1.34 | 0.59 | ❌ | — | 2 |

### 三条结论

1. **prod 首次 materially 松动**：裸 `rank(value_momentum_sector_percentile)` = **0.9653** →
   `group_neutralize(·, 图聚类)` = **0.896（−0.07）**。
   机制成立：**图聚类（客户/伙伴/竞对关系网）与行业分类正交**，中性化改变了持仓结构，与 prod book 的重叠随之下降。
2. **代价明确**：RA 三闸同时变差 —— 2Y 1.66→1.26~1.41、sub 0.86→0.65~0.72、CW 挂（裸 rank 时全过）。
   `ts_backfill(·,66)` 版 **修好了 CW**，只剩 sub(0.66 vs 0.76) 与 2Y(1.26 vs 1.58)。
3. **★ 双 ×1.8 塔红利**：含跨数据集字段的表达式 ⇒ `pyramid_short:"model/other"`、`effective = 2`
   ⇒ **同时点亮 MODEL ×1.8 + OTHER ×1.8**（塔覆盖率收益最大的一类结构）。

### 旋钮

- **粒度**：`cluster_20` **优于** `cluster_10`（后者 S 1.12、sub 0.59）；
- **关系类型**：`relation`（关系图）**远优于** `customer`（2Y 崩到 0.50）与 `competitor`（2Y 0.98）。

## 四、当前态势

| 类别 | 状态 |
|---|---|
| MODEL | `value_momentum_*` 全 RA 通过 / **prod 0.9653**；model238 prod 0.7274 / 强度不足 |
| NEWS | **判死**（S ≤0.57） |
| ANALYST | 净修正广度 S1.18 / sub 0.60 ✅ / **CW 挂（仅 23 只持仓）** |
| OTHER | 嵌入值弱；**图聚类轴 = 真降 prod 杠杆（−0.07）但破坏 RA 三闸** |

**结论未变**：DEU 单信号仍未产出可提交 alpha。但本轮新增了一个**结构性新杠杆**（图聚类正交分组轴），
它把「prod 墙」从**纹丝不动**变成**可调**——这是后续最有希望继续深挖的方向。

## 五、PV 类别（×1.7）：`pattern_scores` 判死（W48）

`pattern_scores` = **504 个图表形态相似度字段**（cov 0.99~0.999，user 几乎全 0）：
`dynamic_similarity_<形态>` / `{max,min,median,mean,std,quantdev,quantile95}_similarity_<形态>_<Nd>`，
形态含 asc/desc/symm_triangle、rising/falling_wedge、reversal_v_bottom·top、continuation_*、breakaway_gap 等。

实测 8 条单信号（V形/楔形/三角/缺口，含取负）⇒ **S 全在 −0.19~+0.17**（换手 0.21~0.31）⇒ **判死**。
（`pv29` 另有 50 个 cov=1.0 的**备选行业分组键**，尚未使用 —— 与 oth455 图聚类同类的潜在分组轴。）

## 六、待攻类别

`FUNDAMENTAL`（×1.8）、`RISK`（×1.5，`risk60` 借券族 / `risk88` alt-mktcap）、
`INSIDERS`+`INSTITUTIONS`（低拥挤：`insider_agg_matrix` / `fund_holdings_panel`）、
`EARNINGS` / `OPTION` / `MACRO` / `SHORTINTEREST`（`shortinterest3` 已测 S≤0.92）。
