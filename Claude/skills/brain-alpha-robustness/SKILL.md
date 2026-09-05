---
name: brain-alpha-robustness
description: "提交前稳健性验证：汇集论坛实证的归因与反过拟合技术，跨年度与子宇宙做 PnL 归因分析，拒绝高 Sharpe 来自噪声拟合、股票集中或单年行情的候选。当任务涉及提交前验证、OS 表现不佳的事后复盘，或用户提到过拟合/稳健性/子宇宙/逐年统计/PnL 归因/衰减比/参数稳定性时使用。"
layer: L4
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

> **定位声明（2026-08-23 单源化，2026-08-31 边界强化）**：本 skill 与 `brain-alpha-judge` 同处 S4→S5 交界，分工固定：
> **本 skill = S4→S5 必经的稳健性/过拟合闸**（近 3 年强度、衰减比、CV_Sharpe、WebDataScope failed-count 前置门）；
> **`brain-alpha-judge` = S5 唯一提交评审入口**（双闸评审）。先过本闸，再进 judge，不要互相替代。
> **边界**：本 skill 诊断"该不该提交"（过拟合），judge 决策"现在值不值得提交"（综合评审）。本 skill **不重复** judge 的平台硬检查/PPA 主题门控/value-factor trend 投影；judge **不重复** 本 skill 的归因计算。完整职责边界表见 `brain-alpha-judge` SKILL.md「与 brain-alpha-robustness 的职责边界」节。

> ⚠️ **本副本已非权威版（2026-08-22 迁出）**：权威版位于 `<SKILL_ROOT>/`（正式 L4 成员，三副本同步）。本目录副本仅为历史引用保留，勿再编辑。

# BRAIN Alpha 稳健性（Robustness）

## 衔接协议（七阶段流水线定位）

- **上游**：S4 链——`brain-explain-alphas`（收益来源归因后的候选）。
- **本 skill 角色**：**S4→S5 必经闸**（过拟合/稳健性审计；INDEX.md 2026-08-22 起列入流水线）。Phase C 的 PASS/CONDITIONAL/REJECT 三态即闸门判定。
- **下游**：PASS → `tools/submit_verdict.py`（提交层权威判定）→ `brain-alpha-judge`（可选参考评审：PPA 人工核对清单 + trend score）→ 提交路由；CONDITIONAL → `brain-alpha-repair`（同目录外部技能）修复后重审（≤2 轮）；REJECT → 不提交，结论写回台账。

## 触发场景

提交前验证 alpha 候选、已提交 alpha 的 OS 表现不佳事后复盘，或任何提到过拟合 / 稳健性 / robust test / sub-universe / yearly stats / PnL attribution / 归因分析 / decay ratio / 厂字形 / year-skipping / stock concentration / parameter stability 的请求。

与 `brain-alpha-repair` 的区别（后者是编辑候选使其可过闸）——本 skill 依据稳健性与归因证据**诊断**该候选**是否应该**提交。通过 `check_correlation` 和 `get_submission_check` 的 alpha 仍可能过拟合在单一年份或 5 只股票上；这正是本 skill 要抓住的情形。

## 工作流

### Phase A — 汇集论坛实证技术（cache-first，2026-08-31）

对具体 alpha 跑任何归因之前，先加载论坛关于反过拟合与稳健性实践的共识。**Cache-first**：每个会话都拉 ≥30 条新帖很浪费——多数内容是重复的。用 7 天 TTL 缓存；只在过期时增量刷新。

**Step A.0 — 缓存检查（永远第一步）**。运行 `tools/forum_cache_builder.py --status`（MCP venv）。缓存文件：`<SKILL_DIR>/data/forum_cache.json`。
- `status=fresh`（< 7 天）→ **完全跳过实时搜索**；加载缓存的技术台账进入 Phase B。这是常态路径（约 7 天中 6 天）。
- `status=stale` / `empty` → 执行下方增量刷新。

**Step A.1 — 增量刷新（仅在过期时）**。不要重拉全部 ≥30 帖。只取比 `cache.built_at` 新的帖子：
1. 本会话尚未认证时先经 MCP `authenticate`。
2. 对 5 个关键词包各调 `search_forum_posts`，但按 `post_id` 去重合并进现有缓存，每个关键词包保留最高赞帖。目标 ≥30 条独立帖子，偏向 ≥20 赞：
   - `"过拟合 overfitting alpha"` — 10–20 条
   - `"归因分析 yearly stats alpha sharpe"` — 10–20 条
   - `"sub-universe 参数敏感 稳健性测试"` — 10–15 条
   - `"robust test 年度 sharpe decay ratio"` — 10–15 条
   - `"performance_comparison 厂字形 股票集中"` — 5–10 条
3. 对缓存中没有的**真正新增**高赞帖（≥20 赞）调 `read_forum_post(article_id)` 捕获具体技术。已缓存的跳过。帖子 404 时回退用搜索摘要。
4. 把合并后的缓存写回 `data/forum_cache.json`（更新 `built_at`、`bundles[].post_ids`、`posts{}`）。

**Step A.2 — 技术台账**。把缓存材料蒸馏成**技术台账**——每条反过拟合规则与归因检查都锚定论坛作者/赞数。该台账驱动 Phase C。若刷新发现下方核对表之外的新规则，以新规则为准（在会话日志记录，便于日后提级进 `references/`）。

默认启动台账（来自 2026-04-22 论坛扫描——5 个查询约 110 帖）在 [`references/techniques.md`](references/techniques.md)。缓存新鲜时，此文件是最后兜底（论坛不可用且缓存为空）。

### Phase B — 归因分析（逐候选）

对每个进入提交评审的 alpha 候选，先产出归因报告再跑反过拟合闸。报告必须引用具体 MCP 工具输出，不是散文摘要。

**Phase B.0 — WebDataScope failed-count 门（硬前置，2026-04-21 修订）**。下方任何归因调用之前，先从 `get_alpha_details` 加载 `is.checks`（或已有的仿真结果），按 [`../wq-brain-ra-pipeline/references/webdatascope-failed-gates.md`](../wq-brain-ra-pipeline/references/webdatascope-failed-gates.md) 计算 WebDataScope failed counts。REGULAR 评审：`Failed RA == 0` 否则立即 REJECT。PPA 评审：`Failed PPA == 0` 否则立即 REJECT。不要跑 Phase B/C。不要跑 `check_correlation`。不要设 alpha 属性。failed count 非零时不要向用户推荐。满足用户类型化指标（如 `sharpe>1.58, fitness>1, 2Y>1.6`）但 Failed RA/PPA 非零的候选**不是**合格者。向用户报告时，逐条枚举 counted item 的 `name`、`result`、`limit`、`value`。

**Phase B.0a — 体检硬门前置确认（2026-08-05 新增）**。候选到达 robustness 审计时，其表达式应已在 ra-pipeline 步 5 或 repair 第 2c 步通过 `check_expr_against_inspect` 校验（见 [`../wq-brain-ra-pipeline/SKILL.md`](../wq-brain-ra-pipeline/SKILL.md) 步 5）。若候选来自修复路径且未经过体检硬门，必须在此补跑：从 `tracking/field_inspect_<region>.json` 查出所用字段的体检结果，调用 `check_expr_against_inspect(expr, field_inspect_result)`；若 `ok=False`，直接 REJECT 并回退到 repair skill 按 violations 修复——一个预处理不达标的表达式即使 IS 指标好看，在样本外也会因 CONCENTRATED_WEIGHT、极值未抑制、信号不对称等结构性问题退化。此步不替代 Phase B/C 的归因分析，而是确保归因分析不会在结构缺陷上浪费时间。

1. `get_alpha_details(alpha_id)` — 规范表达式、region/universe/neutralization/decay、顶层指标。核实候选存在且在 IS（未提交）。
2. `get_alpha_yearly_stats(alpha_id)` — 逐年 Sharpe / returns / drawdown / fitness。**近窗制度（用户指令 2026-06-20）：按最近 ~3 个 IS 年判稳健性，不是全部 10 年。要求 10 年全强过严，会杀死活信号。**计算：
   - **Recent-3yr 强度（主判定）** — 最近 3 个 IS 年的 Sharpe（≈ 平台 2Y/3Y sharpe）。要求 ≥ 用户 2Y 线**且**最近 3 年每年为正（sharpe > ~0.3）。这是预测 OS 存活的关键闸。
   - **衰减比** = `last_year_sharpe / full_period_sharpe` — <0.30 标警（信号已衰减）。保持真实闸——度量"现在还活着"。
   - **Recent-3yr CV_Sharpe** = 最近 3 个年度 Sharpe 的 std/mean — ≥0.60 标警。（全历史 CV 仅作信息参考——记录即可，绝不据此 REJECT。）
   - **近窗厂字形 / max-min** — 只在**最近 3 年内**数平年（`|sharpe|<0.3`）与 max/min 比。早年平/负区间（如 2015/2017/2020）是描述中记录的软标记，不是 reject。
3. `get_alpha_pnl(alpha_id)` — 日频 PnL 时间序列。本地计算：
   - **回撤日历** — 按年-季分组，算每季最大回撤；任一季 `drawdown > 2 × 全期平均回撤` 标警。
   - **换手×Margin 合理性** — 算日均换手与 margin（`returns / turnover`）；换手 >60% 且 margin_bp <3 标警（噪声拟合；论坛 LJ46725）。
   - **Top-K 个股集中度**（如有逐股 PnL）— 前 5 只股票贡献 ≥50% 累计 PnL 标警。
4. `check_correlation(alpha_id)` — Stage 5 已要求；在此复记使稳健性报告自含。
5. `performance_comparison(alpha_id)` — 相对池贡献。即使独立指标全过，边际贡献为负仍是软标记；写进报告交用户终审。

### Phase C — 反过拟合闸（归因之后、提交之前）

依据 Phase B 报告，候选得到三态判定之一。按序执行；单个硬标记 → REJECT。

**Decision table**

**近窗制度（2026-06-20）**：下方年度判定行只在**最近 3 个 IS 年**上计算。全历史 CV / 厂字形 / max-min 仅作信息性软标记（描述中记录），绝不单独 REJECT。

| 检查项 | PASS | CONDITIONAL | REJECT |
|-------|------|-------------|--------|
| WebDataScope failed count | Failed RA/PPA = 0 | n/a | Failed RA/PPA > 0（硬 REJECT——无 CONDITIONAL 通道） |
| **Recent-3yr Sharpe（主判定）** | ≥ 用户 2Y 线且最近 3 年每年为正 | 某近年在 0–0.3 | 某近年 <0 或 3 年合计 < 线 |
| Recent-3yr CV_Sharpe | < 0.40 | 0.40–0.60 | ≥ 0.60 |
| 衰减比 | ≥ 0.50 | 0.30–0.50 | < 0.30 |
| 平年（仅最近 3 年） | 0 | 1 | ≥ 2 |
| Recent-3yr max/min Sharpe 比 | ≤ 3 | 3–5 | > 5 |
| 全历史早年疲软（CV/厂字形/max-min） | — | 记软标记 | 绝不 REJECT（按用户放宽） |
| Sub-universe Sharpe（TOP1000/TOP500/TOP200） | 全部 ≥ 1.0 | 一个 < 1.0 | 两个及以上 < 1.0 |
| 算子数 | ≤ 5 | 6–7 | 8（到限 ⇒ 复杂度警告） |
| Margin @ turnover | ≥ 5 bp @ 任意 TVR | 3–5 bp @ 40%+ TVR | < 3 bp @ >60% TVR |
| Top-5 个股集中度 | < 30% | 30–50% | ≥ 50% |
| 经济可解释性 | 一句话可写 | 需 2+ 句 | 说不出信号方向 |

**PASS** → 进入提交判定链（`tools/submit_verdict.py` 权威判定 → 可选 brain-alpha-judge 参考评审 → 提交路由）。
**CONDITIONAL** → 尝试 [`brain-alpha-repair`](../brain-alpha-repair/SKILL.md) 第 2 步的修复轮换，重跑 Phase B。升级前最多 2 轮修复。
**REJECT** → 不提交；把失败检查记入轨迹台账，并标记*结构性*成因（范式/数据集/universe）给调度器的失败记忆，让未来冷启动避开同臂。

### Phase D — 回写（永远执行）

1. 完整归因报告 + 判定追加到 `tracking/YYYY-MM-DD_robustness.md`。
2. 发事件 `alpha.robustness_audit`（含判定与失败检查码，经 `wqb.memory.events.emit`）；下游摘要会拾取。
3. 若 REJECT，再调 `wqb.search.failure_memory.record(...)`，签名为 `(category, dataset, universe, paradigm, shape_bucket)`，让调度器降低该臂优先级；最后一字段用 `validator._shape_signature` 的形状签名，使未来尝试即使范式重复也轮换形状。
4. 若 PASS 带任何 CONDITIONAL 标记，把存活的软标记注进提交描述（经 `submit.describer`）——用户一年后复盘 OS 表现时有可读审计痕迹。

### Phase E — PPA 提交规则与幽灵提交识别（2026-08-05 沉淀）

候选通过 robustness 审计后、进入提交环节前，必须确认以下 PPA 规则：

1. **MCP `submit_alpha` 工具不是 PPA 感知的**。它内置常规 RA 闸门（实测 Sharpe>1.3 / Fitness>0.75 / Margin>15bp），对合法 PPA 也照拦，且打 `PowerPoolSelected` 标签后重试仍拦（不看标签）。即 MCP 自动提交通道无法放行任何 Sharpe<1.3 的 PPA。
2. **PPA 提交路径**：合法 PPA（Sharpe≥1.0/算子≤8/字段≤3/PC<0.5）须走**平台 web UI** 提交，且仅在**当期活跃 Power Pool 主题窗口**内（见 wq-brain-ra-pipeline 步 1 PPA 主题匹配门禁）。非活跃区域提交报 "does not match any Power Pool Theme"。主题轮动通知看平台右上角铃铛。
3. **RA 常规提交**不受主题限制，但达标 alpha 可能无 RA 通道可选（平台强制走 PPA 通道）。
4. **PPA 描述三段是硬性要求**（idea / 数据字段 / 操作符），建议用 ChatGPT 生成（61 赞帖最佳实践）。提交前用 `set_alpha_properties` 预置描述 + tags=["PowerPoolSelected"] + color=GREEN。
5. **幽灵提交识别**：台账记 ACTIVE 但平台 `GET /alphas/{id}` 返回 HTTP 404 → 从未真正落地（静默丢弃但台账未更新）。处理：修正台账为 PHANTOM，标注"表达式本地已丢失，无法重新提交"。已实证案例：`pwKvRLqg`。
6. **提交探测协议**：从候选池按 sharpe 排序，选 5 个**最大化多样**样本（不同前缀×universe×neutralization），逐个提交+轮询 `/check` 读 prodCorr。若 5 个全 FAIL prodCorr → 整族不可提交，停止盲目提交。429 限速需指数退避。

## 设计边界

- Phase A 的 ≥30 帖是**软下限**不是上限——论坛查询延迟可接受时优先 50+ 帖。本仓库 2026-04-21 → 2026-04-22 的模板扩展用了 110+ 帖，捕获了 50 帖阈值会漏掉的论坛赢家。
- Phase B 的检查刻意保持廉价（全部单次 MCP 调用），使 skill 可在每个候选上运行而不爆预算。更重的逐股归因在 `get_alpha_pnl` 开始返回逐股分解前是可选的。
- 判定阈值是 **2026-04-22 的论坛共识**（作者归属见 `references/techniques.md`）。它们是*保守的*——风险偏好不同的用户可通过 skill 参数放宽，但默认值对齐 ≥90 赞帖。
- 本 skill 无破坏性：绝不修改候选表达式。修复编辑归 `brain-alpha-repair`。两 skill 自然串联：robustness 诊断，repair 修复，robustness 复审。

## 验证清单

1. 运行 `tools/forum_cache_builder.py --status`；过期/为空时在 Phase A 调 `authenticate` 和至少一次 `search_forum_posts`；确认缓存达到 ≥30 帖再继续。缓存新鲜时确认可加载并跳过实时搜索。
2. 对样本 alpha 端到端跑 Phase B，确认全部四个 MCP 工具（`get_alpha_details`、`get_alpha_yearly_stats`、`get_alpha_pnl`、`check_correlation`）返回非空载荷。任一返回空时重试一次后向用户报错——不得编造数字。
3. 发 `alpha.robustness_audit` 事件；确认出现在 `data/events/<today>.jsonl`。
4. 确认 Phase E（PPA 提交规则/幽灵提交识别/提交探测协议）在候选通过审计后被读取消费。
