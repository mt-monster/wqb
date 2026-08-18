# EUR 战役挖掘经验复盘：skill 流程 vs MCP 工具优化点

> 来源：2026-08-18 EUR D1 战役（wave1-wave6c + 并行会话 wave6_nlp/wave7-12），最终 Wj71Q12o ACTIVE/OS 破 prod 墙。
> 目的：从实战回测过程提炼可落地的工具/流程优化项，按"影响面 × 修复成本"排序。

---

## 一、本次战役关键路径回顾

| 阶段 | 动作 | 工具/skill | 结果 |
|---|---|---|---|
| S0 选集 | score_datasets 锁白名单 | toolkit | news_sentiment_dl 首发 |
| S2 预检 | gate 5 闸 | toolkit | wave5 拆 2 次跑（跨 dataset 限制） |
| S3 回测 | 五槽填槽 runner | toolkit runner | wave3d/4/5/6/6b/6c 全收割 |
| S4 诊断 | prod corr 曲线 + 互相关矩阵 | **MCP** | 破墙路径核心证据 |
| S5 提交 | quota + submit_alpha | **MCP** | Wj71Q12o ACTIVE |

**破墙核心机制（本次最大收获）**：FCF 镜像（IS 强 prod 高 0.9013）× pattern gap 镜像（IS 弱但与 FCF 相关 -0.02）稀释复合 → prod 单调降至 0.6847 过墙，IS 不降反升（1.79→1.81）。**该策略的设计输入完全来自 MCP `compute_mutual_correlation`（本地互相关矩阵，0 配额）**。

---

## 二、工具层明确 BUG（高优先级，立即可修）

### BUG-1：metrics_cache 抓 two_year_sharpe 失败率 100%（复合表达式）

**实证**：wave6/6b/6c 共 24 行 `two_year_sharpe=None`（100% 缺失）；wave5 16 行全有值。
**根因**：[metrics_cache.py:31](file:///C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts/metrics_cache.py#L31) 只从 `is.checks` 找 `LOW_2Y_SHARPE` 的 value：
```python
two_y = next((c.get("value") for c in checks if c.get("name") == "LOW_2Y_SHARPE"), None)
```
但平台对**跨 dataset 复合表达式**的 `is.checks` 不含该项（或命名不同），而 `get_alpha_details` 返回的 `metrics.two_year_sharpe` 有值（Wj71Q12o 实证 2.47）。
**影响**：runner 的 `passes_user_thresholds` 因 2y=None 直接判 False → candidates=0 漏报，且 TOP 日志 2y=0.00 误导判读。本次 wave6c 差点因 2y 缺失误判。
**修复**：加 fallback 链：
```python
two_y = next((c.get("value") for c in checks if c.get("name") == "LOW_2Y_SHARPE"), None)
if two_y is None:
    two_y = i.get("two_year_sharpe") or (a.get("metrics") or {}).get("two_year_sharpe")
```

### BUG-2：runner 的 rn_fitness 闸硬编码 0.7，不读 thresholds.json

**实证**：wave5 runner `passes_user_thresholds` 写死 `rn["fitness"] > 0.7`，而用户已授权放宽至 0.6（thresholds.json 已改）→ wave6 起才修复为 `t.get("rn_fitness_min", 0.7)`。
**影响**：wave5 及之前所有波次的 candidates 统计按旧闸过滤，可能漏报达标者。
**修复**：已修（wave6 模板），但需回归检查历史 runner 是否同步。

---

## 三、skill 流程优化点（结构性，中优先级）

### OPT-1：gate 跨 dataset 白名单强制拆分 → 支持合并校验

**实证**：wave5（price_signal_dl + pattern_scores）被迫拆 2 次跑 gate；wave6/6b/6c 手写临时脚本合并 3 dataset 白名单后 `check_one` 8/8 过。
**现状**：[gate.py](file:///C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts/gate.py) `--dataset` 单值必填，`load_whitelist` 只载单 dataset catalog。
**优化**：`--dataset` 支持逗号分隔多值，内部合并 verified/field_types 后统一 `check_one`。本次手写 `_run_wave6_gate.py` 已验证可行性（合并 158+28+504 字段无冲突）。
**收益**：复合表达式（破墙核心武器）的 gate 从"手写临时脚本"升级为原生支持。

### OPT-2：runner 与 settings.json 强耦合 → 启动前 universe 校验锁

**实证**：settings.json 14:52:57 被**并行会话**改为 TOP800，wave6b 14:58 启动读到 → 8 条全崩（sh 0.46-1.07）；wave6 14:49 读 TOP2500 正常。
**现状**：runner `main()` 直接 `ctx.settings` 读全局配置，无波次锁、无启动前校验。
**优化**：
1. runner 启动时打印并断言 universe 与 items.json 声明一致（items.json 已含 `"universe": "TOP2500"` 字段）；
2. 或 runner 支持 `--universe` 显式覆盖，优先级高于 settings.json。
**收益**：杜绝并行会话/外部修改导致的整波误跑（本次浪费 8 条配额 + 1 轮时间）。

### OPT-3：并行会话台账/配置冲突 → 文件锁或会话命名空间

**实证**：台账显示本会话外的 wave6_nlp/wave7-12（news_nlp/ai_news/model193/ml_factor_proj/shortinterest6），全 RED/AMBER_NEAR_RN；settings.json 被并行会话改 universe。
**现状**：LedgerStore 有原子写，但 settings.json 无锁；多会话共享同一 campaign-dir。
**优化**：短期靠"启动前校验"（OPT-2）兜底；长期考虑 campaign-dir 内 `.lock` 或会话级 settings 覆盖文件。
**注意**：这是**多会话并发**场景的系统性风险，非单次失误。

---

## 四、MCP 工具 vs skill 流程：职责边界与增强点

### 本次 MCP 工具的不可替代价值（skill 做不到）

| MCP 工具 | 本次作用 | skill 能否替代 |
|---|---|---|
| `compute_mutual_correlation` | 本地算 17 alpha 互相关矩阵，0 配额，锁定 gap 镜像（corr=-0.02）为稀释分量 → **wave6 设计核心输入** | ❌ skill 无本地 PnL 互相关能力 |
| `check_correlation` | prod 池比对生死关：0.9013→0.8686→0.8235→0.758→0.6847 全曲线 | ❌ 必须平台端 |
| `get_multisimulation_children` + `lookINTO_SimError_message` | wave5 ERROR 批 8 children FAIL 定位 + wave6b TOP800 异常发现 | ⚠️ runner 轮询能发现 ERROR 但无法下钻 children |
| `get_alpha_details` | 2y/rn/sub_universe 完整指标（补 metrics_cache 抓不全） | ⚠️ 部分（修复 BUG-1 后需求降低） |
| `get_submission_quota` / `submit_alpha` | 配额确认 + 提交 + 全检查回执 | ❌ 必须平台端 |

**结论**：MCP 在 **S4 诊断（互相关/prod corr）与 S5 提交** 环节不可替代；skill runner 在 **S3 批量回测** 环节主力。两者是"批量执行"与"精准诊断/提交"的互补关系。

### MCP 工具可增强点

1. **`compute_mutual_correlation` 应前置到 S2 选波**：本次破墙策略的设计输入（找与 FCF 低相关的分量）完全靠它。建议在 `brain-deepExplore` 的 S2→S3 之间加"分量互相关预筛"步骤——对候选分量先本地算互相关，挑 |corr|<0.3 的做复合，避免盲目烧配额试复合。
2. **`check_correlation` 结果应回写台账**：本次手动把 prod corr 曲线写进 wave6/6b/6c verdict。可在 runner 收割后自动对 top-N 候选调 `check_correlation` 并落台账，形成"IS 达标 → prod 验证"的自动闭环。

---

## 五、流程层方法论沉淀（本次最大经验）

### 破 prod 墙的标准化路径（本次验证有效）

```
IS 强信号撞 prod 墙（如 FCF 0.9013）
  → ① compute_mutual_correlation 找 |corr|<0.3 的异质分量（0 配额）
  → ② 梯度稀释复合（0.80/0.20 → 0.70/0.30 → 0.50/0.50 → 0.40/0.60）
  → ③ 每档 check_correlation 验证 prod（生死关）
  → ④ 分散化红利使 IS 不降反升时继续加深稀释
  → ⑤ 定位 prod<0.7 且 IS 达标的甜点（本次 0.40/0.60）
```

**关键认知**：
- 稀释分量不需要自身 IS 强（gap 镜像单跑 sh=0.69），只需要与主信号**低相关**。
- prod corr 随稀释深度**单调下降**（本次 6 个数据点拟合边际 -0.033/10% 权重），可外推定位阈值区间，减少试探次数。
- universe 宽度决定 prod 池大小（EUR TOP2500 池 150 万 vs GBR TOP700 池 1.6 万），但窄池 IS 先崩（wave4/wave6b 双重实证）——**universe 杠杆不可用，信号层稀释才是正解**。

---

## 六、优化项优先级汇总

| 优先级 | 项 | 类型 | 影响面 | 修复成本 |
|---|---|---|---|---|
| P0 | BUG-1 metrics_cache 2y fallback | 工具 bug | 所有复合表达式波次 candidates 漏报 | 低（3 行） |
| P0 | OPT-2 runner 启动前 universe 校验 | 流程防呆 | 杜绝整波误跑（本次已发生） | 低 |
| P1 | OPT-1 gate 多 dataset 合并校验 | 工具增强 | 复合表达式 gate 原生支持 | 中 |
| P1 | MCP 互相关前置 S2 选波 | 流程增强 | 破墙策略标准化，省试探配额 | 低（改 skill 文档） |
| P2 | BUG-2 历史 runner rn 闸回归 | 工具一致性 | 历史波次 candidates 准确性 | 低 |
| P2 | OPT-3 并行会话配置锁 | 系统性防呆 | 多会话场景 | 高 |
| P2 | check_correlation 自动回写台账 | 流程闭环 | 省手动操作 | 中 |
