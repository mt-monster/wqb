# ra-pipeline Dry-Run 真实阶值 + 因子质量评估

> 头（head）：`USA`（ra-pipeline 唯一输入）；本次钻取数据集 = **`multifactor_return_pred`**（delay=1 / TOP3000 / SUBINDUSTRY）
> 运行模式：**dry-run（S6 回测跳过，零配额、零提交）**
> 关联前序修复：四层多样性保证 + P0-2 过期 fail-closed（本报告验证其在真实波上仍生效）

---

## 1. 每一步真实阶值（INPUT → COMMAND → OUTPUT）

### S-PRE — 区域先验查表 ✅（实跑）
- **INPUT**：`region=USA`
- **OUTPUT（真实值）**：
  - `dead_ends`：NONE（无阻塞数据集概念）
  - `dead_datasets`：NONE
  - **活跃契约**：`explore_contract_USA_20260825_231235_769479`，`status=active`，`consumed=2/10`，`ft=Y`（骨架因子齐备）
  - 旧 4 个契约全部 `deprecated / 10/10` → **证明 P0-2 自动续约闭环已生效**（过期 → 自动续约新契约）

### S0 — 数据集体检 ✅（实跑）
- **INPUT**：USA 白名单（n=40）
- **OUTPUT（multifactor_return_pred 真实阶值）**：
  | 指标 | 值 | 判读 |
  |---|---|---|
  | score | **0.917** | 高（>0.85 健康线） |
  | category | model | ML 预测类数据集 |
  | tier | tier1 | 一等 |
  | coverage | **0.969** | 96.9% 覆盖，优秀 |
  | usableFieldCount | **669** | 字段极丰富 |
  | alphaCount | **77** | 已被挖 77 个，未饱和（<100 警戒） |
- 白名单元信息：`pyramid_non_model=24`（≥2 ✓）、`pyramid_ok=True`、`excluded_PROD_saturated=[ml_factor_proj, option_chart_model]`、`excluded_profile_red=[pv1]`
- → 通过 S0 健康闸，进入 S1

### S1 — 字段扫描 ✅（实跑，免 API，复用已有目录）
- **INPUT**：`multifactor_return_pred, d1`
- **OUTPUT（真实值）**：
  - `field_whitelist` = **75 字段**（从 669 可用字段筛出）
  - `concept_count` = 9（analyst_*/_*hedge_*/price_volume_*/regime*/event_* 等）
  - `universe=TOP3000`，`delay=1`
  - 真实字段样例：`analyst_120d_5bucket_class_pred_solar`、`alt2_short_hedge_5d_q5_confidence_score`、`long_hedge_quantile5_r60_pred`、`event_embedding_quantile1_r5_pred`、`regime4_quantile5_r5_pred`

### S2 — 概念优先选波 ✅（实跑，零 API，契约驱动）
- **INPUT**：S1 目录 75 字段 + 活跃契约 12 骨架 + GEM 自含 s2 池（s2_multifactor_return_pred_d1）
- **OUTPUT（reg_mf01 真实值）**：
  - 选出 **48 条**表达式
  - **契约注入 12 骨架因子**（group_*/ts_arg_*），legacy 回退 0
  - 算子频次（top）：`rank`×82、`ts_backfill`×77、`multiply`×32、`subtract`×22、`add`×11、`trade_when`×11、`less_equal`×11、`days_from_last_change`×11、`group_backfill/cartesian/count/mean` 各 ×1
  - **46 个不同字段**被使用
  - 表达式长度：min=39 / max=229 / avg=140；嵌套深度：min=1 / max=8 / avg=5

### S3/S5 — 5 闸 + 批级多样性闸 ✅（实跑，零 API）
- **INPUT**：`reg_mf01`（48 条）
- **OUTPUT（真实值）**：
  - `all_pass = True`，**48/48**
  - `diversity.applied = True`、`diversity.pass = True`、`diversity.consumed = True`、`issues = []`
  - 批内 (算子,字段) 组合：12 required 算子中 **4 个命中**（group_backfill / group_cartesian_product / group_count / group_mean，各 1 次）→ 组合数 ≥ per_batch_min(2) → 过闸
  - 逐项闸：0 失败

### S6 回测 ⏸（dry-run 跳过）
- **真实值**：N/A（零回测配额、零提交）
- **重要诚实声明**：S3/S5 闸门**只校验结构/语法/字段可用性/算子多样性**，**不度量** IS/OS Sharpe、fitness、turnover、sub-universe、self-corr、prod-corr。因此 **"48/48 通过" = "结构合法、可送回测"，不等于"好因子"**。真实挖掘质量必须等 S6。

### S4 诊断 / S8 稳健闸 / S9 复盘 ⏸（dry-run 跳过）
- 依赖 S6 回测结果，本次不跑。

---

## 2. 48 条表达式的因子质量评估

按结构家族归类（每条给出经济直觉判读 + 改进建议）。

### 家族 A — 分组算子（骨架注入，#4849–4852）
| # | 表达式 | 判读 |
|---|---|---|
| 4849 | `group_backfill(alt2_short_hedge_5d_q5_confidence_score, sector, 20)` | 板块内回填对冲置信度。**情境性**：字段若已填满则空操作；若有缺口则有意义。**中等** |
| 4850 | `group_cartesian_product(sector, sector)` | ⚠️ **退化 / 需改进**：sector×sector=sector，纯骨架填充产物，无信号。应剔除 |
| 4851 | `group_count(alt2_short_hedge_5d_q5_confidence_score, sector)` | 板块内非空置信度计数，横截面密度代理。**弱**（信息量低） |
| 4852 | `group_mean(alt2_short_hedge_5d_q5_confidence_score, alt2_short_hedge_60d_q5_confidence_score, sector)` | 板块内对冲置信度均值。**有益**：横截面相对处理，语义清晰 |

### 家族 B — 0.7/0.3 加权混合两个预测分位（#4853–4860, 4885, 4889, 4893，共 13 条）
- 形式：`rank(0.7*rank(A) + 0.3*rank(B))`
- ⚠️ **违反项目硬性规则**：`alpha_search_principles.md` 明确禁止"混信号调参"——`add(0.7*rank(A),0.3*rank(B))` 正是点名反模式，须拆成 atom alpha。
- 经济直觉：多模型预测集成是合理思路；**但意图有益、方法违规**。
- 额外问题：固定 0.7/0.3 权重是手调（过拟合风险）；13 条结构完全相同 → **家族内高度冗余**。
- **结论：需改进 / 应重构为 atom alpha**（如分别送 `rank(A)`、`rank(B)` 两条，再由 SUPER 复合）。

### 家族 C — 两个 ts_backfill 预测分位相乘（#4861–4868, 4886, 4890, 4894）
- 形式：`rank(multiply(rank(ts_backfill(A,66)), rank(ts_backfill(B,66))))`
- **有益（中等）**：乘法交互 = "两模型同向认同"因子，与简单混合是不同信号。
- 注意：`ts_backfill(.,66)` 出现 77 次；对慢变预测，回填多为直通，徒增延迟/噪声；66 属平台允许窗口（1/5/22/66/252/504/1008/1260）✓。
- 保留但需盯过拟合。

### 家族 D — 两个 ts_backfill 回归预测相减（#4869–4876, 4887, 4891, 4895）
- 形式：`rank(subtract(ts_backfill(A,66), ts_backfill(B,66)))`
- **有益（最强价差家族）**：模型分歧/价差因子。当 A、B 来源真正独立时信号强：
  - #4869 `short_horizon_hedge3_60d_regression_pred − analyst_120d_regression_pred`（对冲模型 vs 分析师模型，不同数据 → 真实分歧）✓
- ⚠️ **需改进**：#4874/4875/4876 用 `long_term_*` vs `long_term_regime2_*` / `long_term_seasonal_*` —— 同源 long_term 家族，价差多捕估计噪声而非真实分歧 → 冗余/弱。

### 家族 E — 事件门控 trade_when（#4877–4884, 4888, 4892, 4896）
- 形式：`rank(trade_when(subtract(ts_backfill(event_X,10), ts_backfill(Y,10)), less_equal(days_from_last_change(ts_backfill(event_X,10)),5), 0))`
- **最有益（经济直觉最高）**：事件信号 + 比较目标 + **时间新鲜度门控**（仅当事件近 5 日刷新才交易），并用 0 中性化。是真正的"事件时点"alpha。
- ⚠️ **需谨慎**：复杂度最高（N=8 嵌套、L=212–229）→ 过拟合风险；`days_from_last_change ≤ 5`、`ts_backfill(.,10)` 为魔法阈值；须 S6 验证。
- **最佳候选，但必须先过回测**。

---

## 3. 综合结论

### 有益挖掘因子（建议优先送 S6 回测的子集）
- **家族 E（事件门控）**：经济直觉最强，4–9 条为首选。
- **家族 D 跨源价差**（#4869–4873 等，非同源对）： proven 分歧因子。
- **家族 C（交互相乘）**：与混合不同的信号维度。
- **家族 A #4852**（板块均值对冲置信度）：横截面相对处理清晰。

### 需改进
- **家族 B（13 条加权混合）**：违反项目"禁混信号调参"硬规则 → 重构为 atom alpha 再复合。
- **#4850 `group_cartesian_product(sector,sector)`**：退化产物，直接剔除。
- **家族 D 同源价差**（#4874–4876）：捕噪声，降权/弃。
- **魔法参数**：固定 0.7/0.3 权重、66/10/5 窗口需做敏感性 / 实证（原则要求窗口有意义或有实测证据）。

### 结构性观察（方法论层面）
- 48 条**语义高度集中于本数据集的预测分位字段**——单数据集波次内"深挖不广撒"是预期且合理的。
- 但**算子复用极端**：`rank`×82、`ts_backfill`×77；48 条实为 5 个结构家族、家族内近乎克隆 → **思想多样性低**，尽管过了 (算子,字段) 组合闸。
- 12 个骨架 group_*/ts_arg_* 因子大多在选波中被弃，**仅 4 个 group_* 各出现 1 次**，且含 1 条退化（#4850）。即"多样性保证"守住了闸门，但产出的 group 因子偏薄、含噪声。

### 闸门通过 ≠ 因子好（关键提醒）
S3/S5 `48/48` 仅证明**结构合法、可送回测**。真实挖掘价值 = S6 回测的 IS/OS Sharpe、fitness、turnover、sub-universe、self-corr、prod-corr——本次 dry-run 全部跳过。**建议下一步只把"有益子集"（E + D跨源 + C + A#4852，约 20 条）送 S6，而非 48 条全跑**，既省配额又聚焦。

---

## 4. 本次运行副作用
- 落库：`expressions/USA/reg_mf01`（48 条，未回测）
- 契约：`231235` consumed 2→（reg_mf01 消费后）维持 active，未过期
- 全程零回测配额、零提交
