# Prod-Corr 规避机制（因子族记录与算力分配）

> 2026-08-05 建立。触发：GLB qMNZX1o1 提交被拒（PROD_CORRELATION 0.7686 > 0.7）——GLB pred 系与 USA 同遇 prod_corr 墙。
> 目的：识别已成功因子的类型特征 → 记录 → 后续同类挖掘直接规避 → 算力精准分配。

## 1. 已确认超标因子族（提交实测）

| alpha | 数据集/字段 | users | prod_corr | 信号结构 |
|---|---|---|---|---|
| qMNZX1o1 | techindi_model `first_quantile_ten_day_return_techindi6_2` | 97 | **0.7686** ❌ | country 分组 + ts_rank 300 窗 + winsorize/backfill + decay15 |
| 9qpQ0VQ2 | techindi_model `first_quantile_ten_day_return_41` | 62 | 未触发（同族高概率 >0.7）⚠ | 同上（250 窗 decay10） |

## 2. 因子类型特征（规避画像）

**高危信号族（GLB）**：`techindi_model` 的 `predicted_first_quantile_ten_day_return_*` 系——ML 预测收益信号本身与生产池大量同类 alpha 天然相关：
- **users ≥ 50 的字段 = prod_corr 高危**（qMNZX1o1 97 users → 0.77；pred10d_41 62 users → 高概率超）
- 信号强度与 prod_corr 正相关（强信号必被生产池套牢——USA other566/risk65 同验证）
- country 分组/长窗只修复子域与 margin，**不降 prod_corr**

**其他已证 prod_corr 墙**（跨区域）：
- USA：other566（prod 0.86）、risk65（0.98）、fnd91（0.73-0.89）、option40 skew 族（0.75+）
- 通用规律：**users>30K 饱和数据集与 users>50 热门字段的强信号 = prod_corr 高危**（WebDataScope 规则 15 同源）

## 3. 规避规则（挖掘前置检查）

1. **字段分级**（get_datafields 后立即执行）：
   - `users ≥ 50`：只做信号验证（确认方向/强度），**不投入候选打磨**（prod_corr 必超）
   - `users 10-49`：候选池，提交前必须实测 prod_corr（POST /alphas/{id}/submit 触发计算，或 check_correlation）
   - `users 0-9`：**优先候选池**（理论 prod_corr=0——生产池无同类 alpha），信号强度需实测
2. **批次预算分配**：冷门字段（users≤9）占批次 ≥50%；热门字段仅用于信号族方向验证（每族 ≤1 批）
3. **提交前门禁**：任何候选提交前先 GET /alphas/{id}/submit 或 POST 触发 prod_corr 计算；>0.7 立即放弃该字段族，转向冷门字段
4. **同族不重复投入**：已确认超标字段族（如 techindi ten_day first_quantile users≥50）不再投任何变体（decay/窗口/分组扫描全部跳过）

## 4. 已验证配方（算力复用，不再重复探索）

**GLB 黄金配方**：`group_rank(ts_rank(ts_backfill(winsorize(F, std=5), 60), W), country)` @ FAST/trunc0.04
- W=300 + decay15 → margin 5.0-5.1bp 全 PASS（qMNZX1o1 实证）
- 参数轨迹（techindi6_2）：margin 随 decay 单调（decay10 4.57 → 15 5.04 → 18 5.07 但 AMER 退化）——**decay15 + 300 窗是甜点**
- 新字段直接套配方，不再扫参数网格

## 5. 冷门字段信号衰减实测（2026-08-05 b18r）

**冷门字段（users 0-4）信号强度实测大幅衰减**：sharpe 0.91-1.65（vs 热门字段 1.8-2.9）——社区 userCount 与信号强度正相关（社区已筛选出优质字段）。`predicted_first_quantile_ten_day_return_*` 冷门版最佳 1.65（_23），仍远低于 1.58 达标线的安全裕度。

**GLB 双墙困境（结构性）**：
| 字段类型 | users | 信号 | prod_corr | 结论 |
|---|---|---|---|---|
| 热门 | ≥50 | 2.2-2.9 ✅ | >0.7 ❌ | 不可提交 |
| 中间 | 18-49 | 1.9-2.2 ⚠ | 未验证（各带 AMER/2Y 缺口） | 打磨成本高 |
| 冷门 | 0-9 | 0.9-1.65 ❌ | 理论 0 ✅ | 信号不足 |

**待验证实验**：中间地带（users 18-40，如 techindi17_1/ten_day_5）打磨至全 PASS 后实测 prod_corr——若 <0.7 则中间地带是候选来源（批量推进）；若 >0.7 则 GLB 达标 10 个 PPA 在当前约束下不可达（信号强度与 prod_corr 的 trade-off 为平台结构性）。

## 6. 中间地带决定性实验（2026-08-05 b19 实测）——失败

**techindi16_1（users 40）全窗口/decay 扫描**（300-450 窗 × decay14-16）：全部 sh 2.0-2.07 但 **fit 0.96-0.98（差 0.02-0.04）、AMER fail、2Y 1.43-1.51（差 0.09-0.17）**——三项结构性缺口与窗口/decay 无关。

**GLB 双墙最终结论（信号族系统穷尽）**：
| 字段层级 | users | 结果 |
|---|---|---|
| 热门（6_2/41/19_1） | 60-97 | 全 PASS 可打磨但 **prod_corr >0.7**（6_2 实测 0.7686） |
| 中间（16_1/17_1/5/25） | 18-40 | **fit/AMER/2Y 结构性缺口**（窗口/decay 不可修） |
| 冷门（_4/tech1_1/24/23/3/22） | 0-4 | 信号弱（0.9-1.65） |

**结论**：GLB 的 pred 系信号族（techindi_model first_quantile_ten_day）在 prod_corr<0.7 约束下**无候选来源**——信号强度、可打磨性、prod_corr 三者不可兼得（平台结构性 trade-off，同 USA other566/risk65 验证）。**10 个 PPA 达标目标在 GLB 当前不可达**；已投入批次 b10-b19 全部存档，规避机制确保不再重复投入此信号族。

**算力重新分配建议**：GLB pred 系信号族标记为"已穷尽-规避"；后续挖掘转向：① 新 PPA 主题窗口（非 GLB pred 系主题）② 新数据包灌入的冷门数据集 ③ 其他区域（KOR/ASI 等）的 PPA 主题匹配。

## 7. Prod 验证排队调度纪律（2026-09-01）

> 触发：平台 prod 计算为异步排队（候选 vs 全平台生产池 4 年日收益相关，通常 1–5 分钟，
> 前几次查询返回空 body 属正常）且**每账户仅允许 1 个在飞**——多候选串行等待是 S4 链主要时间黑洞。
> 客户端现状：`check_correlation` 内置 30s 轮询/最长 1h，`correlation_busy` fail-fast；**同 alpha 已决结果缓存 7 天**（Redis `prod_corr:<alpha_id>`，`pending`/`busy`/`data_unavailable` 不缓存）。
> 提交前终验用 `refresh=True` 强制回源平台。
>
> **批量候选调度（串行泳道 + 本地并行，强制）**：
> 1. 全批先跑完本地检查（selfcorrQuick / mutual / yearly 归因——不占平台队列，可并行）。
> 2. 仅本地预过者排入 prod 泳道，队列永远保持**恰好 1 个在飞**：提交 A → 等待期做 A 的归因/稳健性材料 → A 回来（自动入缓存）立即提交 B。
> 3. 必挂候选（本地 self/mutual 已 >0.7）禁烧平台队列；全批回收后统一进 judge。
> 4. 会话压缩/重开后重验同 alpha 先查缓存（响应含 `from_cache: true`），命中则不重新排队。
