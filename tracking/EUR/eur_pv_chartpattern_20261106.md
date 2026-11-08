# EUR / PV 面 图表形态相似度战役台账

日期：20261106｜区域：EUR TOP2500 D1｜category：PV（塔位 2，差 1 颗点亮）

## 1. 为什么选这里

全区域塔位实读（get_pyramid_alphas）：EUR 有 **6 个 category 停在 2**（pv/other/risk/sentiment 各差 1 颗点亮，news/insiders 停在 1），
而 analyst 已 10 颗严重超亮。点塔性价比上 EUR 是全盘最高，且必须避开 analyst/model/fundamental/imbalance 四个已点亮塔。

EUR/PV 候选集排序（本地覆盖缓存 EUR_d1_TOP1200，按 覆盖 x 字段数^0.35 / log(alphaCount)）：

| 数据集 | 覆盖 | 字段 | alphaCount | 判定 |
|---|---:|---:|---:|---|
| continuation_score | 0.9924 | 560 | **0** | 主攻 |
| pattern_scores | 0.9924 | 504 | **0** | 主攻 |
| intraday_pv_feats | 0.9548 | 585 | 1 | 备选 |
| pv37 | 1.0 | 251 | 406 | 拥挤，排除 |
| pv20 | 0.6915 | 1475 | 65 | 覆盖低 |

**alphaCount = 0 意味着这两个数据集在 EUR 从未被用来做过 alpha** ⇒ prod 相关性墙的先天风险最低，
这在此前 USA/DEU/GBR 反复撞 prod 的环境里很稀缺。

## 2. 字段结构

两个数据集都是 MATRIX 型（无 VECTOR，不需要 vec_avg），覆盖 0.979-0.998，本质是同一族：

  <形态名>_similarity_<统计量>_<窗口>

- 形态名：ascending_channel 上升通道 / ascending_staircase 上升阶梯 / ascending_scallop 上升扇贝 /
  ascending_triangle 上升三角 / falling_wedge 下降楔形 / rising_wedge 上升楔形 /
  symmetric_triangle 对称三角 / breakaway_gap 跳空 / support_resistance 支撑阻力 等；
- 统计量：average/mean、middle(中位)、maximum、minimum、dispersion/stddev、percentile_95、recent、dynamic、adaptive；
- 窗口：h40w（40 周）、h60（60 日）、120、lookback60/120。

含义：给定股票当前价格路径与某经典形态模板的**相似程度**。它不是价格水平、不是动量、不是波动率，
而是对「形状」的匹配度——与已用过的全部机制正交。

## 3. 机制来源（论坛 + 论文）

- 论文：**Lo, Mamaysky & Wang (2000), Foundations of Technical Analysis, Journal of Finance 55(4):1705-1765**
  （NBER WP 7613）。用核回归自动识别形态后检验其增量预测力，结论是部分形态（尤其头肩/倒头肩）
  在标准模型之外仍有增量信息 ⇒ **形态相似度是真信息载体，但强度有限**，与本族 alphaCount=0 却存在信号的可能性一致。
- 论坛证据（search_forum_posts，本轮检索到但正文未能打开，检索通道两次 compute_budget 超时）：
  ①《continuation_score 数据集因子模板分享》——专讲本数据集的模板帖；
  ②《看跌矩形做空 + 上升通道做多的跨数据集组合 Alpha》——说明本族形态被按**方向**分开使用（看跌形态做空、上升通道做多），
     与下面 T2 的方向合成思路一致，但其做法跨数据集组合（要占塔混配额），本战役改为**单数据集内合成**避开配额。

## 4. 模板池（12 个结构互异模板）

| # | 模板名 | 信息维度 | 骨架要点 | 来源 | 状态 |
|---|---|---|---|---|---|
| T1 | 主力形态水平 | 横截面水平 | group_rank(单形态 average, sector) | Lo-Mamaysky-Wang 2000 | 备料 |
| T2 | 多形态方向合成 | 方向合成 | 看多形态和 − 看空形态 | 论坛跨数据集帖的单数据集化 | **已派发** |
| T3 | 形态新近度 | 形成中 | recent − middle | 自建（形态正在形成 vs 早已存在） | 备料 |
| T4 | 形态决定性 | 分布尾部 | percentile_95 − middle | 自建（最强匹配相对典型匹配的落差） | **已派发** |
| T5 | 形态歧义度 | 离散 | dispersion / std 字段 | 自建（无明确形态 = 噪声） | 备料 |
| T6 | 形态一阶差分 | 变化 | ts_delta(similarity, 22) | 自建 | 备料 |
| T7 | 时序稀有度 | 与自身历史比 | ts_rank(similarity, 252) | 自建（罕见形态更可信） | 备料 |
| T8 | 窗口分歧 | 长短窗背离 | h40w 相似度 − h60/120 相似度 | 自建 | 备料 |
| T9 | 延续 vs 反转相对强度 | 跨数据集同名对比 | continuation_score vs pattern_scores 同形态差 | 自建 | 备料 |
| T10 | 形态广度 | 计数 | 高相似度形态个数 | 自建（breadth 型） | 备料 |
| T11 | 形态门槛取信号 | 条件 | 仅在高相似度子集内取方向 | 自建（condition 型） | 备料 |
| T12 | 相似度加权动量 | 加权 | similarity 作为近 N 日收益权重 | 自建 | 备料 |

差异落在信息维度（水平 / 方向 / 形成 / 尾部 / 离散 / 变化 / 稀有度 / 窗口 / 跨集 / 广度 / 条件 / 加权）上，不是换窗口。

## 5. 批次 A（mid = CZfW5fW359a9FHIiCYM2I4）

设置：EUR / TOP2500 / D1 / decay 8 / SLOW_AND_FAST / trunc 0.08 / unit VERIFY / nan ON / pasteurization ON / maxTrade ON。
（与 EUR 既有实测档一致，保证与 EUR 存量 8 颗候选可比。）

E1（T2 多形态方向合成，算子 1）：
group_rank(avg_similarity_ascending_channel + avg_similarity_ascending_staircase + avg_similarity_falling_wedge_pattern + avg_similarity_upward_breakaway_gap - avg_similarity_rising_wedge_pattern, sector)

方向依据（经典技术分析口径）：上升通道/上升阶梯/上升三角为看多延续；下降楔形为看多反转；
向上跳空为看多；上升楔形为看空反转 ⇒ 前四者相加、上升楔形相减。

E2（T4 形态决定性，算子 1）：
group_rank(ascending_channel_similarity_percentile_95 - ascending_channel_similarity_middle, sector)

gate：validate_expressions 在 EUR/TOP2500 返回 valid=true、unknown_fields=[]。

## 6. 待办

- [ ] 收批次 A：读 E1/E2 的 S/F/TO/2Y
- [ ] 若任一 S ≥ 1.0，沿该模板做窗口与分组轴扩展；若都 < 0.5，换 T5/T7/T10 三条不同信息维度
- [ ] 注意：本族 alphaCount=0 ⇒ prod 相关性风险低，一旦 S 过线应优先跑 prod 确认

## 7. 批次 A/B/C 结果：6 条结构互异骨架全灭 ⇒ 面级判死

| alpha | 模板 | S | F | TO | 2Y | sub | ret | vol=ret/S |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| mLoKrq85 | T2 多形态方向合成 | -0.17 | -0.03 | 8.70% | 0.28 | -0.31 | -0.33% | — |
| E56mgqwR | T4 形态决定性 (p95-中位) | -0.73 | -0.24 | 7.92% | 0.31 | -0.19 | -1.36% | 1.86% |
| leAgQYb8 | T3 形态新近度 (recent-中位) | **0.84** | 0.31 | 8.94% | **-0.16** | 0.01 | 1.67% | 1.99% |
| npv6ZlMa | T7 时序稀有度 ts_rank252 | -0.57 | -0.16 | 8.09% | -0.50 | -0.67 | -1.02% | — |
| qML5n8d1 | 峰值反转做空（论坛思路） | -0.68 | -0.22 | 7.49% | -0.14 | 0.11 | -1.27% | — |
| rKR0bYLo | T5 离散度/歧义度 | -0.17 | -0.02 | 7.69% | 0.22 | -0.11 | -0.27% | — |

### 7.1 判死依据（三条独立证据）

1. **六条骨架结构互异且全灭**：横截面水平合成、分布尾部、形态形成中、时序稀有度、峰值反转做空、离散度/歧义度——
   覆盖了「水平 / 尾部 / 变化 / 时序 / 反转 / 离散」六个正交互补维度，最强仅 0.84。
2. **唯一过 0.8 的那条 2Y 是负的**（leAgQYb8：S 0.84 但 2Y -0.16、sub 0.01）⇒ 信号集中在早期年份，近两年已消失，
   属于已被套利的老现象，不是可提交信号。这与 Lo-Mamaysky-Wang 论文本身「形态信息存在但强度有限」一致。
3. **波动率锁死 F**：vol ≈ 1.9-2.0%（ret/S），按闭式 F = S^1.5 x sqrt(vol/0.125)，
   即使 S 做到 1.58，F 也只有 1.58^1.5 x sqrt(0.0195/0.125) = 1.98 x 0.395 = **0.78** < 1；
   要 F=1 需 S ≥ 2.1。本族 6 条骨架最强 0.84 ⇒ **数学上不可能达标**，不是模板不够。

### 7.2 结论

**EUR/PV 图表形态相似度面封盘。** continuation_score 与 pattern_scores 两个 aC=0 数据集不再投入仿真预算。
EUR/PV 塔位维持 2（未点亮）。

**关键教训（已入 Agent Memory）**：alphaCount=0 只说明没人做过，**不说明有信号**。
零拥挤降低的是 prod 相关性风险，不提高信号强度；本轮两个 aC=0 数据集 6 模板全灭即是实证。
选派数据集时不能把「拥挤度低」当成「机会大」。

## 8. 本轮全量 alpha 清单

mLoKrq85 / E56mgqwR（批次 A）｜leAgQYb8 / npv6ZlMa（批次 B）｜qML5n8d1 / rKR0bYLo（批次 C）。
全部 S < 1.58，无一颗可提交。EUR 候选池维持 8 颗不变。
