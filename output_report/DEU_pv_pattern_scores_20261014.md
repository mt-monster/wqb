# DEU × Price Volume（pattern_scores）战役报告 —— 按探针 SOP 的完整复核（2026-10-14）

**区域**：DEU / TOP500 / delay=1　**类别**：PV（DEU 未点亮塔 ✅）　**数据集**：`pattern_scores`（504 字段、cov 0.989）
**结论摘要**：按探针 SOP 完成 2 批 20 条（双结构 × 未测概念族 + 文献构造）。**max S = 0.65**（需 1.58）⇒ **PV 类别在 DEU 无可用信号面，与 skill 既有判死记录一致，且本轮用更严的协议再次确认。**

---

## 一、PV 类别资源画像（第 0 步筛选）

| 数据集 | 字段(cov≥0.6) | 性质 | 判定 |
|---|---|---|---|
| `pv29` | 50 | **纯分组轴**（`industry_grouping_level*_*` / `sta1_top*`） | 规则排除（不得进信号白名单） |
| `pv30` | 180 | **纯分组轴**（`factor*_grouping*_score*` / `sta2_top*fact*`） | 规则排除 |
| **`pattern_scores`** | **504** | **形态相似度信号**（全 MATRIX，α 总计 238） | 唯一信号数据集 ⇒ 本轮主攻 |
| `pv109` | 26 | cov 0.467 | <0.6 剔除 |
| `pv1` | 23 | cov 0.0（DEU 无数据） | 不可用 |

## 二、概念族拆解（SOP 的「跨概念族」要求）

`pattern_scores` 504 字段的族分布与**历史探测覆盖**：

| 概念族 | 字段数 | 历史是否测过 |
|---|---|---|
| `max_similarity_*` / `mean_similarity_*` / `median_similarity_*` / `min_similarity_*` / `dynamic_similarity_*` | 61 | ✅ 已测（WANL12 等，max 0.09~0.42） |
| **`std_similarity_*`（离散度）** | **≥8** | ❌ **从未测过** |
| **`quantile95_similarity_*`（高分位强度）** | 多个 | ❌ **从未测过** |
| **`symmetry_triangle_*`** | 多个 | ❌ 从未测过 |
| 其余形态族（triangle/wedge/gap/v_shape…）的 `*_std_similarity_40d` 变体 | 多个 | ❌ 从未测过 |

**⇒ 历史判死只覆盖了「相似度水平量」一个概念维度；「相似度离散度 / 分位强度」维度是全新的。**

## 三、外部文献依据（用户要求「查外部论文」）

1. **Chart Library（16M 图表、实盘前瞻测试）**：形态匹配方向准确率仅 **50–55%**（接近抛硬币）；但 **相似度 >90% 的匹配方向准确率显著更高**；**最大边际在风险识别——高方差匹配（宽扇形）可靠预测未来高波动**。
2. **Fuzzy-logic TA（Financial Analysts Journal, 2004）**：**pattern membership（模糊度）与后续异常收益直接相关**；membership ≤0.7 的头肩形态反而显著跑赢（弱形态方向相反）。
3. **KNN chart similarity（Applied Economics, 2017）**：相似度分类可识别有预测力的形态，但市场接近有效。

**⇒ 文献明确指向两件事**：① 相似度「水平」的边际有限；② **离散度/清晰度维度是独立信息（且主要预测波动而非方向）**——本轮据此设计了 `std_similarity` 族与门控构造。

## 四、实测（WANL33–34，20 条合规表达式）

### 4.1 WANL33：双结构 × 未测概念族（SOP 标准批）

| 字段 | A级框架 S | DEU核心 S |
|---|---|---|
| `v_shape_reversal_bottom_std_similarity_40d` | — | **−0.65** |
| `std_similarity_continuation_rising_wedge` | −0.37 | **−0.55** |
| `std_similarity_continuation_falling_wedge` | −0.35 | **−0.48** |
| `quantile95_similarity_desc_triangle` | **+0.23** | (−0.15) |
| `symmetry_triangle_downward_std_similarity_40d` / `dynamic_similarity_continuation_v_top` / `max_similarity_sym_triangle_upward` | ≤0.06 | ≤0.05 |

**⇒ `std_similarity`（离散度）族一致负向**（−0.35~−0.65），TO 0.18–0.36。
**⇒ 这与文献预测吻合：离散度预测的是「波动」而非「方向」**——它在截面排序里表现为负向，本质是「低离散度（形态清晰）→ 表现更好」。

### 4.2 WANL34：文献构造（门控 / 时序秩 / 反向 / 形状）

| 构造 | S | 2Y |
|---|---|---|
| 反向·清晰度优先（v_shape, DEU核心） | **0.65** | 0.07 |
| 反向时序秩（v_shape, 框架） | 0.57 | −0.01 |
| 反向·清晰度优先（std_rising, DEU核心） | 0.55 | 0.95 |
| 门控（`trade_when(ts_rank>0.9, …, −1)`，文献构造） | 0.16 | 0.08 |
| 形态新鲜度 `ts_delta(20)` / 自身异常度 `ts_zscore(252)` / `signed_power` | ≤0.29 | — |

**⇒ 即便用文献指定的门控构造，也只有 0.16。反向把负号翻正后上限 0.65，仍差 0.93。**

## 五、裁定

| 判据 | 值 |
|---|---|
| 双结构最好读数（20 条） | **S 0.65**（阈值 1.58） |
| 历史判死复核（40 条 + WANL12 10 条） | max 0.46 / 0.09 |
| 换手 | 0.16–0.37（偏高，margin 受压） |
| 概念族覆盖 | 本轮补齐「离散度 / 分位强度 / 对称三角」三个从未测维度 |
| 算子覆盖 | `ts_rank` / `ts_zscore` / `ts_delta` / `reverse` / `trade_when` / `quantile` / `signed_power` / `hump` 同级构造 |

**⇒ PV 类别（`pattern_scores`）在 DEU 判死，且本次是「按 SOP 的严格协议 + 跨概念族 + 文献构造」三重覆盖后的判死，可信度高于既有记录。**

**⇒ 根因（有文献支持）**：形态相似度的方向边际本就很弱（50–55%），其价值在**波动预测**而非截面收益——这在「追求 Sharpe 的 alpha」框架下不可转化。**这也解释了为什么 `pattern_scores` 有 504 个高覆盖、零竞争字段却零产出。**

## 六、本轮方法论收获（已回写 skill）

1. **「零竞争 504 字段」的最终解释**：不是「没人发现」，而是**该数据的可提取信息类型（波动）与 alpha 目标（方向性 Sharpe）不匹配**。
2. **概念族拆解法的价值**：历史探测只覆盖了一个维度（水平量），本轮靠族拆解发现并补齐了三个未测维度——**这是「探针太少」质疑的正确打开方式**（不是多跑同族，而是补新族）。
3. **文献构造必须实测**：文献说「>90% 相似度门控有效」，实测 0.16——**文献结论不能直接移植到本平台的截面/中性化框架**。
