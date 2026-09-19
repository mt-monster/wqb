# GEM 生成链路评估与改进方向（2026-09-17，全数据实测）

> **一句话结论**：GEM 现在**无法被评估**——它的产出与所有其他生成器混在一起、无法区分；
> 而链路里有一处**写库断言错误**让 `gem_wave` 节点的"去重/分桶/骨架配给"三项能力**每次运行都失败并被丢弃**。
> 在这两条修好之前，讨论"GEM 生成质量好不好"没有依据。

---

## 0. TL;DR

| # | 发现 | 证据强度 |
|---|---|---|
| **A** | **`expressions.source` 没有任何代码路径在写** → GEM 产出不可辨识 | 强（3 个写入点全查） |
| **B** | **`gem_wave` 的写回 INSERT 引用 3 个不存在的列 → 每次运行必失败** | 强（已实测复现） |
| **C** | 近 3 天产出复用率 **12.6**、**89.2%** 落在 ≥8 条的大簇里（与 8 月 GEM 产出的 13.7/89.2% 同级） | 强（骨架聚类） |
| **D** | 规则 6（复杂度）**达标且优于全库**；规则 7/8 因 `expected_exposure` 不落库**无法验证**；规则 4（窗口）**违规 33.1%** | 强 |
| **E** | `tracking/USA/ideas_gen/*_v2.md`（35 份，8-25）是自述"非语义模板脚手架"的文档，生产者已不在仓库内 → 沉寂但**存在再注入风险** | 中 |

---

## A. 元问题：GEM 产出根本无法度量

### A.1 `source` 列：存在但没人写

`expressions` 有 `source` 列。全仓只有 **3 个 `INSERT INTO expressions` 写入点**：

| 写入点 | 是否设置 `source` |
|---|---|
| `src/wqb/store/_expressions.py:132`（**规范写入器**） | ❌ INSERT/UPDATE 列清单里都没有它 |
| `src/wqb/workflow/nodes/gem_wave.py:172` | ❌ 没有（而且这处本身是坏的，见 §B） |
| `tools/mcp_batch_writer.py:298` | ❌ 没有 |

**全仓搜不到任何把 `source` 写成 `'gem'` 的代码**。

### A.2 后果：按 source 切分会得到"假象"

| `source` | 条数 | 时间分布 |
|---|---|---|
| `gem` | 1,663 | **全部在 2026-08-25/26/28** |
| `NULL` | 19,777（89.8%） | 含**全部 9 月** |
| 9 月新表达式 | 14,511 | `(NULL)` 14,511（+ `workflow_gem_manual` 134）|

→ **`source='gem'` 里一条 9 月数据都没有**。任何"GEM 产出质量"的统计，
只要按 `source` 过滤，实际看到的都是**一个月前**的语料。

> ⚠ 这也解释了为什么上一轮我按 `source='gem'` 得出的"GEM 95.4% 只有两个算子"，
> **不能代表当前 GEM** —— 那是 8-25 的语料。

### A.3 附带后果：无法做 A/B 与回归
GEM 有 `phased` / `skeleton` / `single` 三种模式（§D.1），但产出不落模式标签，
所以**无法回答"换成 skeleton mode 有没有更好"**。这是当前最贵的一个空白。

---

## B. ★★★ `gem_wave` 节点的写回是坏的（已实测复现）

`src/wqb/workflow/nodes/gem_wave.py:172` 的写入语句：

```sql
INSERT OR REPLACE INTO expressions
   (id, region, wave, dataset, expression, status, bucket, skeleton, selected, created_at, updated_at)
```

而 `expressions` 实际列里 **没有** `bucket` / `skeleton` / `selected`：

```
实际列：id, wave_id, expression, fingerprint, status, alpha_id, sharpe, fitness, margin,
        turnover, created_at, updated_at, region, wave, dataset, settings_json, source
缺失：  bucket, skeleton, selected
```

**实测**：执行该 INSERT →

```
OperationalError: table expressions has no column named bucket
```

### 为什么这件事重要
该 INSERT 位于 `gem.run()` **成功之后**（调用顺序：`gem.run()` → SELECT 生成结果 →
`_auto_dedup` → `_auto_bucket` → `_auto_skeleton` → **写回** → `conn.commit()`），
所以：

1. **表达式本身已由 `gem.run()` 落库**（生成是好的）；
2. **但节点宣称的三项能力每次都在写回处崩掉**：
   `_auto_dedup` / `_auto_bucket` / `_auto_skeleton` 在内存里算完 → 抛异常 → **全部丢弃**；
3. `except` 只把 `result["error"]` 填上（**没有静默吞掉**，这点是好的一面），
   但 `result["success"]` 保持 False → 每次 `gem_wave` 都是失败终态。

→ 净效果：**"生成期去重 / 分桶 / 骨架配给"这条 S2 质量防线，事实上从未生效过。**

### 修法（二选一）
- **a) 补列**：给 `expressions` 加 `bucket` / `skeleton` / `selected`（并按写入器语义回填）——
  这同时也是 §C 生成期骨架去重的**落点**；
- **b) 去掉这三列**：改成写进 `settings_json`，并把 dedup/bucket/skeleton 的**产物真正用起来**
  （目前即便不崩，也没看到有下游消费）。

**推荐 a**：`skeleton` 落库是"生成期去重"的前提（见 §C 的改进 5）。

---

## C. 产出退化：可测部分（近 3 天）

用**骨架签名**（把字段名统一替换为 `F`、数字为 `N`，算子保留）做聚类：

| 组 | 条数 | 唯一骨架 | **复用率** | Top 骨架占比 | **≥8 条大簇覆盖** |
|---|---|---|---|---|---|
| 8月 `source=gem` | 1,663 | 121 | **13.7** | 15.9% | **89.2%** |
| 8月 全部 | 7,353 | 998 | 7.4 | 6.7% | 77.7% |
| 9月 全部 | 14,671 | 2,002 | 7.3 | 2.8% | 79.8% |
| **近 3 天（9-14 起）** | **8,317** | **661** | **12.6** | 5.0% | **89.2%** |

**读法**：近 3 天的复用率（12.6）与 8 月 GEM 语料（13.7）**基本同级**，
**89.2%** 的产出落在"同一骨架 ≥8 条"的大簇里 —— 即**当前产出与当初被认为退化的那批一样单调**。

近 3 天 Top3 骨架：

| 条数 | 占比 | 骨架 |
|---|---|---|
| 412 | 5.0% | `ts_corr(F,F,N)` |
| 144 | 1.7% | `rank(group_neutralize(subtract(rank(ts_backfill(F,N)),rank(ts_backfill(F,N))),bucket(...)))` |
| 130 | 1.6% | `divide(subtract(F,F),add(abs(F),abs(F)))` |

**一个正面信号**：Top3 全是**结构交互类**形态（`ts_corr` / `subtract(rank,rank)` / `divide`），
说明上一轮建议的"只用 5 类结构交互"**形状指导被执行了**。
问题不在"用错形状"，而在**同一形状内部的骨架过度复用**——即"形状对了，但只用了 3 个具体骨架"。

### 生成期的两个可用杠杆（已存在但未接线）
- `--max-expressions`（default **24**，"Cap expressions per template"）—— 每模板上限；
- `--batch-size`（default **50**，"Fields per batch in phased mode"）—— **这个很可能就是字段替换引擎**：
  按 50 个字段一批 → LLM 出概念 → 模板跨 50 个字段展开 → 直接产出同骨架兄弟变体。
- `--require-operators` / `--require-count`（多样性强制）**未从 `gem.py` 透传**（gem.py 只透传 `--pipeline-mode`）。

---

## D. 规则合规实况（对 SKILL.md 的 8 条概念优先铁律逐条查）

### D.1 规则 6（复杂度预算 2–5 算子）：✅ **达标且优于全库**

| 组 | 中位算子数 | ≤4 算子占比 |
|---|---|---|
| `source='gem'` | **4** | **74.4%** |
| 全库 | 4（均值 5.3）| 53.7% |

全库有 **2,831 条 ≥10 算子**、**127 条 0 算子**（规则 6 违例者），而 GEM 标注产出里 ≤4 算子占 74.4%
→ **规则 6 是有效的，且 GEM 是执行得较好的那一部分。**

### D.2 规则 7 / 8：⚠ **无法验证**（缺标签）
规则 7 要求"按**语义维度**判多样性：≥3 个 Expected Exposure、≥3 个字段族、≥2 个分组轴、≥2 个时间尺度"；
规则 8 要求用 `risk_neutralized_sharpe` 验证 Exposure 声明。

**全表扫描结果：没有任何表存储 `expected_exposure`** ——
`gate.py::_extract_exposure_from_idea` 在生成期从 idea 文本里**提取了它，然后丢掉**。
→ 规则 7、8 是这套 skill 里**最精致的机制**，却**没有可度量的输入**。

> 注：`risk_neutralized_sharpe` **有**落库（`backtest_results`），所以规则 8 的**验证侧**数据在，
> 缺的是**声明侧**（expected_exposure）。

### D.3 规则 4（窗口白名单）：❌ **GEM 侧违规 33.1%**
| 组 | 非标准窗口占比 |
|---|---|
| `source='gem'` | **33.1%** |
| 全库 | 21.1% |

**GEM 比全库更严重**。根因同上一份报告：`_lib/operator_coverage.py::_DEFAULT_WINDOWS = [20,60,120,5,10,252]`
（6 个里 4 个不在 SOP 白名单内），而 SOP 只把这条例写成**散文**、零机械守护。

### D.4 规则 2（必须带 priors，fail-closed）：✅ 已在 `gem.py:145` 实现模板源拦截
`is_template_ideas_source()` 守卫存在，会在 `source ∈ {feature_engineering_node, standalone*}` 时跳过自动注入。

---

## E. 陈旧模板的再注入风险

`tracking/USA/ideas_gen/*_v2.md`（**35 份，2026-08-25**，29/35 含未填充的 `ts_backfill({F})` 占位符）
自述是模板脚手架，例如 `news97_v2.md`：

> **Concept**: Recency of peak conviction on nws97_2dts_gen (ts_arg_max, 20d)
> **Mechanism**: **Generic Path-1 diversity concept for dry-run extensibility validation** on dataset news97.
> The operator topology (ts_arg_max/ts_arg_min timing features plus level/difference probes) is what matters here,
> **not signal semantics**.

其 Implementation Example `quantile(-ts_arg_max(ts_backfill({F}, 66), 20))`
**正好对应** §C 里 162 条（9.7%）的那个骨架簇 —— 即这批文档就是 8 月退化的来源之一。

**当前状态**：生产者已不在仓库内，**也没有任何代码读取该目录** → 目前**沉寂**。
**风险**：`--ideas-file` 是显式覆盖通道，`is_template_ideas_source` 只拦自动注入；
若有人把该目录当 ideas 源传进去，会**原样重演** 8 月的退化。

---

## F. 改进方向（按 ROI 排序）

| # | 动作 | 收益 | 成本 | 风险 |
|---|---|---|---|---|
| **1** | **修 `expressions.source` 写入**（规范写入器 + GEM 侧写 `gem_phased`/`gem_skeleton`/`gem_single`） | **解锁一切度量与 A/B**；这是其他所有优化的前提 | 小 | 低（新增字段值） |
| **2** | **修 `gem_wave` 写回**（补 `bucket`/`skeleton`/`selected` 三列，并让 dedup/bucket/skeleton 真正生效） | 恢复生成期去重/分桶/骨架配给；结束"每次运行必失败" | 小–中 | 低 |
| **3** | **落 `expected_exposure`**（idea→生成期→DB） | 解锁规则 7/8（语义多样性 + Exposure 验证） | 中 | 低 |
| **4** | **窗口白名单机械化 + `_DEFAULT_WINDOWS` 对齐** | 消掉 GEM 侧 33.1% 违规的产生源 | 很小 | 低 |
| **5** | **生成期骨架去重**（按骨架签名，目标复用率从 12.6 → ~7） | 直接抑制兄弟变体自残（SELF 最高 0.9445） | 中（依赖 #2 的 `skeleton` 列） | 低 |
| **6** | **接线 `--require-operators`/`--require-count`**（现未从节点透传） | 让已有的多样性强制真正生效 | 小 | 低 |
| **7** | **隔离 `ideas_gen/*_v2.md`**（移入 attic 或加只读标记） | 消除再注入风险 | 很小 | 低 |

**顺序建议**：**1 → 2 → 4 → 6**（都是小改动、低风险、且 1/2 是解锁后续的前提），
再评估 3/5。

---

## G. 附：本轮验证方法（可复用）

1. **按 `source` 切分** → 发现"gem 标签只有 8 月"，从而避免把历史语料当现状；
2. **骨架签名聚类**（字段→`F`、数字→`N`、算子保留）→ 把"看起来像兄弟变体"变成复用率数字；
3. **实测 INSERT 语句**（BEGIN → 执行 → ROLLBACK）→ 复现 `no such column` 而不是靠读代码推断；
4. **全仓搜写入点**（`grep "INTO expressions"`）→ 只需查 3 处就确定 `source` 无人写；
5. **全表扫描列名**（`pragma table_info` 遍历所有表找 `exposure`）→ 确认 `expected_exposure` 不存在。

> ★ 教训延续上一轮：**不要用"看起来像"下结论**。本轮我第一版按 `source='gem'` 得出
> "GEM 95.4% 只有两个算子、加权混合 0%"，按日期切分后发现那全部是 **8-25 的语料**；
> 且我的"顶层 add"检测器**漏掉了 `quantile(add(multiply(0.7,...)))` 这类嵌套形态**
> （用真闸复测：结构判定 1,547 条加权混合，真闸只拦 **19%**，漏 **81%** —— 与上一轮报告口径一致的修正）。
