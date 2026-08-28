# EUR REGULAR 战役 Dryrun 编排验证报告

> **目标**：用 `wq-brain-campaign-toolkit` skill 的编排，验证用户提示词（region=EUR / delay=D1 / multi×8 / 10 个风格迥异单数据集 alpha / 相关性<0.4 / 不自动提交）能否被正确输入输出。
> **方法**：① 解析提示词为结构化契约；② 跑工具箱自带离线测试；③ 用临时副本安全烟测 gate 的 I/O；④ 比对 prompt 要求与 toolkit 能力，列出缺口与拟办。
> **结论**：**编排骨架可承载 90% 要求；4 处需补强（1 配置、1 算子上限门、1 跨 skill robust/过拟合步骤、1 真实收益相关性把关）**，方可无损执行。
>
> **二次验证（2026-08-25 20:35 本会话重跑）**：离线测试 **65 passed**（新增 `test_enhance_v2.py`）；gate I/O 用全新隔离目录烟测 `all_pass=true / total=3 / passed=3`，结构化 JSON 契约不变；pipeline 提交契约源码复核确认 `POST /simulations` 批量端点（=`multi_create_simulate`×8）、单条 `create_simulate` 零调用。**4 处缺口原样成立，未改动。**

---

## 一、Dryrun 实测结果

| 验证项 | 命令/动作 | 结果 |
|---|---|---|
| 工具箱离线测试 | `pytest tests/test_enhance_v2.py scripts/test_rules.py scripts/test_diversity_extract.py scripts/test_operator_coverage.py scripts/test_platform_sync.py` | **65 passed** ✅ |
| gate I/O 烟测 | 临时副本（`logs/_dryrun_eur`）+ 3 条样例候选 + stub 白名单，跑 `gate.py --dataset eur_model238` | 输出结构化 JSON：`all_pass=true, total=3, passed=3`，含 `sanity_gates`/`diversity_gate`/`report[]` ✅ |
| pipeline 提交契约 | 读 `pipeline.submit_batch` 源码 | 构造 `{"type":"REGULAR","settings":s,"regular":expr}` 列表 → `POST /simulations`；返回 Location 即 multisim id ✅（即 multi_create_simulate，非单条） |

**关键编排依赖（实测坐实）**：`gate.py` 真正依赖 `scan_fields.py` 生成的白名单 `reference/EUR_<dataset>_field_whitelist.json`，typed catalog（`eur_<dataset>_fields.json`）**不足以**让 gate 启动（会 `FileNotFoundError`）。因此真实输入链是：
```
score_datasets.py → scan_fields.py(网络取字段覆盖) → gate.py(5闸) → pipeline.py(回测) → review_wave.py(评审/墙) → diversity_audit.py(多样性)
```

---

## 二、提示词要求 ↔ Toolkit 能力 映射

### ✅ 完全覆盖（无需改动）
| 要求 | Toolkit 落点 |
|---|---|
| region=EUR / delay=D1 / maxTrade=ON / REGULAR | `settings.json`（region 强制派生，非目录名猜） |
| multi_create_simulate ×8，禁用 create_simulate | `pipeline.submit_batch` 走 `/simulations` 批量端点；`settings._multi_sim_batch_size=8`；`create_simulation` 未被调用 |
| sharpe>1.58 / fitness>1 / 2Y>1.6 / tvr 5–30% / ra_failed=0 / rn_sharpe>1.0·rn_fitness>0.6 / prod_corr≤0.7 / self_corr≤0.7 | `thresholds.json` 的 `review` + `hard_gates`（prod/self 0.7） |
| 数据历史≥5年 | `settings.startDate=2014`（~10年），设置级约束 |
| 1–2 字段 / 单数据集 / 风格不同 | `ortho_prescreen.py` + `build_wave.py` 结构去同质 |
| 每 10 轮多样性评估 | `diversity_audit.py` / `diversity_extract.py`（手动节奏） |
| 不自动提交、交还用户 | `pipeline` 默认 `--dry-run`，显式 `--submit` 才烧配额 |
| 候选池 | `expressions` 表（status=ortho_kept）+ ledger |

### △ 部分覆盖 / 代理（需注意）
| 要求 | 现状 | 风险 |
|---|---|---|
| **彼此相关性<0.4 / 提交前相关性<0.4** | `ortho_prescreen.py` 用 **结构相似度**（Jaccard 字段/算子 + difflib，默认 `max-sim=0.4`），**非真实收益相关性** | 结构不同 ≠ 收益不相关；真实 return-correlation<0.4 需平台相关性 API 逐对计算（贵、需 alpha 已存在） |
| **本季度未点亮的金字塔数据集挑 1 个** | `score_datasets.py` + `dataset_health.pyramid_quota` 评分；"本季已点亮"靠 ledger dead/历史推断，**无显式"本季点亮"标记** | 可能重复选已用数据集 |
| **遍历不同 universe** | `settings.universe` 固定 `TOP2500`；切换需 per-batch `item_overrides`（pipeline 支持）或换 config；**无内置 sweep 命令** | EUR 历史：TOP800 曾致 wave6b 全崩（已回滚 TOP2500）。随意扫 universe 高危 |

### ✗ 缺失 / 需补强（执行前必须处理）
| # | 缺口 | 性质 | 拟办 |
|---|---|---|---|
| 1 | **margin 阈值 5bp vs 提示词 15bp** | 配置偏差 | `thresholds.json` `review.margin_min: 0.0005 → 0.0015`（⚠️ 覆盖 2026-08-18"放宽"授权，需你确认） |
| 2 | **算子数 < 8 无上限门** | gate 缺失 | `gate.py` 增加 `operators_max=8` 校验（统计表达式算子调用数，≥8 即拒） |
| 3 | **"test robust" + "严格过拟合测试" 不在 toolkit** | 跨 skill 缺口 | 落在 **`brain-alpha-robustness` skill**（earnings/PnL 归因、anti-overfit）。需在每个 alpha 回测完成后显式调用该 skill 作为步骤 |
| 4 | **prod_corr>0.7 提交前无自动把关** | 缺自动门 | `hard_gates.prod_correlation_max=0.7` 仅是配置；pipeline 提交前未自动查平台相关性。建议在最终 10 候选上用平台相关性 API 做提交前 0.4/0.7 双闸 |

---

## 三、执行前必须完成的 4 项拟办（按优先级）

1. **【需你确认】margin_min 0.0005 → 0.0015**：直接决定筛选严格度，且覆盖既往授权，先确认再改。
2. **【加代码】算子数<8 上限门**：在 `gate.py` 增加一行计数校验，10 分钟级改动。
3. **【加步骤】每 alpha 调 `brain-alpha-robustness`**：在 `per_alpha_workflow` 插入该 skill 调用（robust + 过拟合），否则"严格过拟合测试"落空。
4. **【定策略】真实收益相关性把关**：先用 `ortho_prescreen`（结构代理）做日常去同质；对最终 10 候选再用平台相关性 API 做 return-correlation<0.4 + prod_corr≤0.7 双闸，避免"结构不同但收益高相关"漏网。

## 四、关于"遍历 universe"与"未点亮数据集"的建议
- **universe**：维持 `TOP2500`（已修复），仅当某数据集在 TOP2500 表现系统性差时，经 per-batch override 试 `TOP3000`/`MINVOL`，且必须记录回 ledger 防重蹈 TOP800 覆辙。
- **数据集**：先用 `score_datasets.py --probe-plan` 在当前 **未 dead** 的金字塔数据集中挑 1 个 `alphaCount` 低、覆盖达标的（EUR 已知 returns 反转拥挤 prod 0.95 墙，优先 `alphaCount=0` 零竞争集）；确认"本季是否点亮"靠 `campaign.py ledger` 查 `dead`/历史 wave。

## 五、编排 I/O 契约小结（验证通过）
```
输入：candidates(list[str]) + config/settings.json(region) + reference/EUR_<ds>_field_whitelist.json(scan_fields产出)
  ↓ gate.py (5闸: 语法/语义/算子/事件/VECTOR包裹 + 多样性)
输出：{all_pass, total, passed, sanity_gates, diversity_gate, report:[{index,fields,issues,pass}]}
  ↓ pipeline.py --dry-run (构造 REGULAR 批量 payload → POST /simulations，dry-run 不提交)
输出：multisim id (Location) → 轮询 → review_wave.py 读指标 vs thresholds → ortho_prescreen 去同质 → diversity_audit 评估
```

---
*附：解析契约 `dryrun_eur_campaign_spec.json`；烟测产物 `logs/_dryrun_eur/`（临时，可删）；工具箱测试 51 passed。*
