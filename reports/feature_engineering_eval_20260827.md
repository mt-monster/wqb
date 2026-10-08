# 特征工程链路评估（2026-08-27）

**评估对象**：`brain-data-feature-engineering` skill（`~/.workbuddy/skills/`）+ `output_report/*_ideas.md` 22 份产物 + makeSomeGem 管线（`s2_*_d1_idea` → 8 模板实例化）+ `tools/scan_fields.py` 字段扫描。
**核心问题**：逻辑对不对？能否有效完成字段筛选、给出挖掘价值？

---

## 一、结论速览

| 维度 | 判定 | 一句话 |
|---|---|---|
| 设计层（SKILL.md 8 问框架） | ✅ 健全 | 第一性原理问题库 + 字段解构 + 透明推理，方法论正确 |
| 执行层（实际产物） | ❌ 严重走样 | 新一批 USA_1_*（8/26）是**一套骨架换皮**，违反 skill 自身"禁止通用模板"红线 |
| 准则合规 | ❌ 大规模违反 | 425 条 `add(multiply())` 混信号表达式入库（USA 14.6%），93 条已烧配额回测，201 条 pending 待烧 |
| 字段筛选 | ❌ 三处断链 | 筛选信号（coverage/userCount/alphaCount/金字塔）采集了但从未被 idea 生成消费 |
| 挖掘价值输出 | ⚠️ 部分 | 老一代产物（MEA fundamental6）有字段解构+金字塔意识；新一代只剩模板壳 |

**总评：方法论设计是对的，但当前执行已退化为"模板叉积枚举"，既没有完成字段筛选，也没有输出挖掘价值排序。混信号违规是在 2026-08-24 准则生效之后生成的。**

---

## 二、链路全景（实证还原）

```
brain-data-feature-engineering skill
  └─> output_report/<region>_<delay>_<dataset>_ideas.md   (22 份, 0.7–16KB)
        └─> makeSomeGem run_pipeline 读入 → s2_<dataset>_d1_idea (ledger_kv)
              └─> 8 个模板 × 字段组合叉积 → expression_list (每数据集 ~142 条)
                    └─> expressions 表 → 回测 → wave_gate 5 闸 (事后)
tools/scan_fields.py
  └─> reference/<region>_<dataset>_fields.json (含 coverage/userCount/alphaCount)
        └─> ❌ 未接入 idea 生成 —— 数据采了没人用
data/wqb.db fields 表 (45,079 行, 含 coverage/userCount)
  └─> ❌ 同样未接入
```

## 三、逻辑正确性逐层评估

### 3.1 设计层：8 问框架 —— 逻辑正确 ✅
SKILL.md 的核心方法论（"什么是不变的/变化的/异常的/组合的/结构的/累积的/相对的/本质的"）是合格的第一性原理问题库；OUTPUT_TEMPLATE.md 要求字段清单表、逐字段解构、Tier 1/2/3 优先级——这套要求本身是对的，且与用户 alpha 准则（含义优先、字段分组、group_*）兼容。

### 3.2 执行层：两代产物质量断崖 ❌
- **老一代**（MEA fundamental6 8/19、EUR 系列 8/23-25）：基本按模板走——真实字段名（`fundamental_current_assets_total` 等）、三大报表勾稽关系、8 问分类、金字塔未点亮 1.5x 标注。**这是特征工程**。
- **新一代**（USA_1_* 8 份，8/26）：**同一套 8 个概念骨架逐字复制，仅替换占位符词**。实证：`pattern_scores`（504 个技术形态字段）与 `nlp_news_scores`（情感字段）两份产物的概念列表完全同构（Multi-leg 0.4/0.3/0.3 → momentum → divergence → weighted → persistence → volatility → two-leg 0.6/0.4 → reversal）。无字段解构、无覆盖/竞争分析、无 Tier 优先级。**这是模板填空，不是特征工程**，直接违反 skill 自己"不应当：提供通用模板"条款。
- **占位符未解析**：`{pattern_field_1}` 等字面占位符留在产物里（下游 makeSomeGem 有自己的字段解析所以未泄漏入库，但 ideas 文档本身不可直接使用）。

### 3.3 管线层：模板叉积 = 组合枚举 ❌
以 `s2_pattern_scores_d1_idea` 为证：8 个模板（`quantile(subtract(ts_av_diff({A},66), ts_av_diff({B},66)))` 等）× 字段变体叉积（dynamic_/median_/min_/max_ × breakaway_/common_gap_…）= 142 条表达式/数据集。
- **可取处**：`subtract` 配对是价差型 atom 结构（好于 add）；窗口 66/22 在白名单内；实测 `ts_ir(...,60)` 非白名单窗口为 0 条（窗口纪律执行尚可）。
- **不可取处**：字段进入模板是**机械叉积**而非按字段语义/覆盖/竞争筛选——142 条里大量是同族冗余（这正是 pre_backtest_filter 第 1 层"同批 >60% 共享 exposure"要拦的东西，说明该闸没拦住生成端）。

### 3.4 准则合规：混信号违规规模化 ❌（最严重）
用户 2026-08-24 强制准则第 1 条：**禁止混信号调参，警惕 `add(A,B)` 加权相加**。实证：
- `expressions` 表中 `add(multiply(...))` 模式 **425 条**（USA 2,912 条中占 14.6%）；
- 其中 93 条已回测烧配额、**201 条 pending 将继续烧**；
- USA_1_* ideas 文档的 **Concept #1 就是 `add(multiply(0.4,…), multiply(0.3,…))`**——准则生效（8/24）之后（8/26）生成，属明知故犯；
- 实测混信号 IS sharpe 均值 0.906（vs 干净表达式 0.234）、达标率 33/93=35%（vs 17/380=4.5%）——**IS 指标显著虚高恰恰印证了准则的立论**：混信号调参在样本内膨胀指标，但违背 atom 化与稳健性要求，OS/prod-corr 风险后置。这不是"混信号更好"，而是"混信号过拟合更狠"。

## 四、字段筛选有效性：不能，三处断链

1. **信号采集了没人用**：`scan_fields.py` catalog 含 coverage/userCount/alphaCount，`fields` 表 45,079 行同样有——但 idea 生成与模板实例化**零消费**这些信号，没有任何"按 coverage≥0.85、userCount 低、未点亮金字塔排序字段"的逻辑。
2. **ideas 文档无字段价值排序**：模板要求的 Field Inventory 表 + Tier 1/2/3 优先级在实际产物中全部缺失，下游无法据此决定先挖哪个字段。
3. **唯一闸门在事后**：wave_gate 5 闸与 pre_backtest_filter 都在回测前后端，**回测前的字段价值筛选只有 `low_stock_coverage` 一个警告 + `--zero-comp` 可选开关**，形同虚设。PPA 三硬门槛（coverage≥0.85 / alphaCount≤50 / fieldCount≥10）存在于 ppa-mining skill，但未接入本链路。

## 五、挖掘价值给出能力：部分

- 能给出：数据集级的故事线（老一代产物）、表达式批量供给（142 条/数据集）、事后闸门。
- 不能给出：**字段级的价值分层**（哪个字段值得深挖、哪个是拥挤区）、竞争度规避（prod-corr 教训完全没有前移到字段选择）、金字塔点亮导向（新一代产物连金字塔状态都不标了）。
- 结合当前实战瓶颈（GLB/USA prod-corr 全线 0.82+ 拥挤），**字段筛选的最大价值恰是"避开拥挤字段族"**——而这正是当前链路完全缺失的一环。

## 六、修复建议（优先级序）

1. **P0 作废重做 USA_1_* 八份换皮产物**：剥离/替换 add(multiply) 概念，按 OUTPUT_TEMPLATE 重生成（含真实字段名、覆盖表、Tier 分层）。
2. **P0 拦截混信号**：在 `expr_lint.py` 或 `pre_backtest_filter.py` 加 `add(multiply(` 检测 → FAIL/WARN；对已入库 201 条 pending 的混信号表达式先标记后放行，避免继续烧配额。
3. **P1 接通筛选信号**：idea 生成前先查 `fields` 表，按 `coverage≥0.85 AND userCount 低 AND alphaCount 低` 输出字段优先级清单，模板只实例化 Top-N 字段（如 20 个）而非全量叉积。
4. **P1 skill 加硬性 checklist**：产物必须含 ①字段覆盖/竞争表 ②Tier 优先级 ③窗口合规声明 ④无 add(A,B) 声明，缺一即不通过。
5. **P2 曝光多样性前置**：把 pre_backtest_filter 第 1 层（同批 >60% 同 exposure FAIL）从回测前移到生成端，截断同族冗余叉积。

---

## 附：实证 SQL 留痕

```sql
-- 混信号规模与结局
SELECT e.status, COUNT(*) FROM expressions e
WHERE e.expression LIKE '%add(multiply(%' GROUP BY e.status;
-- backtested=76, gem=99, selected=47, pending=201, mode_b=9, manual=2

-- IS 虚高对比（混信号 vs 干净）
SELECT AVG(b.sharpe) FROM expressions e JOIN backtest_results b ON b.expression_id=e.id
WHERE e.expression [NOT] LIKE '%add(multiply(%';
-- 混: n=93 avg=0.906 达标35% | 净: n=380 avg=0.234 达标4.5%

-- 换皮证据：对比 output_report/USA_1_pattern_scores_ideas.md
--   与 USA_1_nlp_news_scores_ideas.md 的 Concept 列表（骨架逐字相同）
```
