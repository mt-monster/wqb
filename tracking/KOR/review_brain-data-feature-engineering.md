# Review：`brain-data-feature-engineering` 对「机制→形态」主线的覆盖度

> 触发：用户指出 KOR skill ② 的主线约束是
> **骨架核心形态由 ① 六法体检体征决定 / 壳层每层由经济机制决定 / 实时查论坛取证 / 说不出收益来源不许组装**，
> 问：这个被复用为 ②.a 复用对象的 L1 skill，是否真的承载这条主线？
> 复核对象：安装位 `~/.workbuddy/skills/brain-data-feature-engineering/SKILL.md`（= 仓库源 `Claude/skills/` 下同名文件，diff 一致）。
> 日期：2026-10-16

---

## 一、逐条核对结果

| # | 主线约束 | L1 是否有落点 | 证据 |
|---|---|---|---|
| 1 | **核心信号形态由 ① 体检体征决定** | ❌ **只有采集，无消费契约** | 步 2（L61）确实取 `coverage / userCount / freq / shape`，但全文再无一处说"读数如何决定形态"。coverage 只进了画像表，**没有任何下游读它做决策** |
| 2 | **壳层每层是否存在由经济机制决定** | ❌ **无「壳层」抽象** | L1 的产物是单层线性 `Implementation Example`（L85/94/103 三例全是 `rank(...)` / `trade_when(rank(...), -rank(...))` 一层）。**没有"核心 vs 壳层"的分层概念**，也就无处表达"这层要不要加" |
| 3 | **实时查论坛取证** | ❌ **完全缺失** | frontmatter `allowed-tools` 只有 Read/Grep/Glob/Write + 3 个 mcp，**无 `search_forum_posts`**；正文零次提及论坛。全 100+ 个 skill 中只有 `brain-forum-browse` 与 `wq-brain-ra-kor` 有此能力 |
| 4 | **说不出「收益从哪来」不许组装**（硬门） | ⚠️ **弱化为必填文本，不是 gate** | 概念块有 `**Logical Meaning**` 与 `**Expected Exposure**`（L81/84），但**没有任何否决判据**。且 `Expected Exposure` 的真实消费方是 `tools/pre_backtest_filter.py` 闸1「同批 >60% 共享同一 exposure ⇒ FAIL」——那是**事后去重**，不是**事前准入** |

---

## 二、结论：复用方向对，但复用对象只能覆盖「机制概念」这一步

L1 真正提供的是：**分档 → 字段画像 → 8 问 → 概念块 → S1 台账**，落点是**一段文字 + 一个单层模板**。

它**不提供**主线的三件事：体征→形态的映射、壳层选层、论坛取证。

⇒ **KOR skill 保留 ②.b（体征查表定核心形态）/ ②.c（按机制选壳层）/ ②.d（论坛取证）是正确的，不是"重复造轮子"。**
把它们误判为"应复用 L1"并删掉，等于把主线约束的三根支柱抽掉。

**⇒ 上一轮整改的措辞需要修正**：②.a 写「机制概念复用 L1」是对的（那一步 L1 确实更完整），
但**不能暗示"组装整体已复用 L1"**。L1 是 ②.a 的上游，不是 ②.b~②.d 的替代。

---

## 三、连带发现：L1 分档判据缺区域有效率维度（KOR 实测已暴露）

L1 第 0 步（L47–53）分档判据只看**字段名标准度**（是否含 eps/revenue/estimate 等标准财务词）与描述覆盖率，
**不看该字段在本区的实测有效率**。

KOR 实证反例：`analyst` 类 59 个字段全部落在**透明档** ⇒ 按 L1 规则**跳过 8 问**，
但本区实测**有效字段仅约 2 个**。⇒ 分档判据与区域现实脱钩。

这不是 KOR 特例，是设计缺口：**「名字自解释」≠「在本区可用」**。

---

## 四、连带发现：仓库级死指针（非本 skill 独有问题，但影响它）

`SKILL.md` L62 引用 `s1_semantic_<ds>` 并标注来源为「步 3 的 `field_semantic_classify.py`」：

- **该脚本文件当前不存在**：`tools/field_semantic_classify.py` 已不在磁盘（仅余 `tools/__pycache__/field_semantic_classify.cpython-313.pyc`）。
- git 历史无删除记录 ⇒ 属「从未入库 / 已流失」，非有意删除。
- **步号也错**：L1 的步 3 是「8 问」，语义分类不在步 3。
- 同类死指针共 **5 个 skill** 引用它：`brain-data-feature-engineering` / `brain-alpha-research-hypothesis-first` /
  `brain-alpha-research-news-sentiment` / `brain-dataset-exploration-general` / `wq-brain-campaign-toolkit`。

消费方仍在（`tools/wave_gate_pkg/gates_semantic.py` 读 `s1_semantic` 键），
所以**闸 SEM 功能没坏，坏的是"怎么生成它"的指引**——照文档执行会找不到命令。

---

## 五、建议（按优先级，均需用户确认后再动手）

### P0｜修正 KOR skill 措辞（防误删）
②.a 补一句边界声明，防止后续把 ②.b~②.d 当"重复 L1"清理掉：

> **②.a 复用 L1 ≠ 组装整体复用 L1。** L1 提供「机制概念 + 单层模板」；
> **体征→核心形态映射（②.b）、壳层选层（②.c）、论坛取证（②.d）三件 L1 不承载，必须留在本 skill。**
> 依据：L1 无 `search_forum_posts` 权限、无「壳层」抽象、体征读数无下游消费方。

### P1｜给 L1 补两条契约（跨 14 区生效，需谨慎）
1. **体征消费契约**：在步 2 与步 3 之间加一小节，把体征读数**显式映射**到形态决策
   （参考 KOR ②.b 查表：cov<0.4/zero_inflated ⇒ `ts_backfill`/`trade_when` 门控；季频 ⇒ 窗口下限；单边恒正 ⇒ `ts_delta`）。
2. **分档判据加「区域有效率」维度**：把「名字自解释」降为**必要非充分**条件，
   透明档仍需跑一次最小可用性体检（本区有效字段 <5% 时不得直接跳过 8 问）。

### P2｜修仓库级死指针
`field_semantic_classify.py` 要么找回、要么把 5 处引用改指到实际生成方（`wave_gate_pkg` 一侧）
或标注为「由 S0 阶段产出」。同时修正 L1 的步号错误。

---

## 六、本次 review 未改动任何文件

所有结论均来自只读核对（Read / Grep / 逐条证据定位），未对 L1 或 KOR skill 落笔。
P0–P2 待用户裁决后再执行。
