# EUR REGULAR 战役 Dry-run（以 `wq-brain-ra-pipeline` 为编排头）

> **Head（编排头）**：`wq-brain-ra-pipeline` —— REGULAR Alpha 挖掘唯一 SOP（L-RA 层，v2.1，2026-08-25 落地），九步骨架 S-PRE→S0→S1→S2→S3→S4→S4→S5→S6。
> **输入的"头指令"**：用户 EUR REGULAR 战役提示词（region=EUR / delay=D1 / maxTrade=ON·OFF / REGULAR / multi×8 / 10 个风格迥异单数据集 alpha / 相关性<0.4 / 不自动提交）。
> **方法**：不实际挖矿/提交；逐步核对 SOP 命令是否真实存在、I/O 契约是否成立、提示词硬指标与 `GATES`/`settings` 是否对齐。本会话已实地验证（见 §1）。
> **结论**：**ra-pipeline 能编排 EUR 跑通九步；但提示词若干硬指标与 `GATES`/`settings`/EUR profile 存在 4 处硬性冲突 + 2 处缺口，须先对齐再正式开跑。**

---

## 一、就绪性实地验证（本会话已跑）

| # | 验证项 | 命令/动作 | 结果 |
|---|---|---|---|
| 1 | ra-pipeline 本体 | 读 `references/regions/EUR.md` | 存在，`entry_verdict: active`，win 配方 `0.4 慢 MODEL 残差 + 0.6 快 PV` |
| 2 | toolkit 子命令 | grep `.qoder-cn` 与 `.workbuddy` 两份 `campaign.py` | 8 子命令全一致：`scan-fields`/`score`/`build-wave`/`pipeline`/`review`/`ledger`/`registry`/`wave` ✅ |
| 3 | 步5 门禁入口 | 读 `tools/wave_gate.py` | 存在；先语法校验 → **子进程调用** `gate.py`（5闸+多样性）→ 结果回写 DB ✅ |
| 4 | gate I/O（上一轮复验） | 隔离目录烟测 `gate.py` | `all_pass=true/total=3/passed=3`，结构化 JSON 契约成立 ✅ |
| 5 | 提交契约（上一轮复验） | 读 `pipeline.submit_batch` | `POST /simulations` 批量端点（=multi_create_simulate×8）；单条 `create_simulation` 零调用 ✅ |
| 6 | GEM 生成器 | 查 `brain-makeSomeGem/scripts/headless_runner/run.py` | 存在 ✅ |
| 7 | 步6/8 工具 | `tools/batch_status.py`/`submit_verdict.py`/`sa_probe.py` | 全部存在 ✅ |
| 8 | 工具箱离线测试 | `pytest` 5 测试文件 | **65 passed** ✅ |

---

## 二、九步 Dry-run 追踪（每步 I/O 明细）

### 步 1（S-PRE）查表 / 区域 Profile 路由
- **目的**：读 EUR profile，按 `entry_verdict` 裁决入口；取 universe/delay/中性化/排除集/当前波号。
- **输入**：`$REGION=EUR`；`Read references/regions/EUR.md`（front-matter `entry_verdict=active` → 继续步 2）。
- **命令**：
  ```powershell
  mcp__wqb-db__get_campaign_summary  region=EUR
  mcp__wqb-db__get_dead_ends         region=EUR
  mcp__wqb-db__get_dead_datasets     region=EUR
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir tracking/EUR registry list
  ```
- **产物**：universe/delay/中性化/排除集/排除信号族/当前波号。
- **失败分支**：registry 全空 → 新区域进步 2 并在步 9 建 campaign；`get_dead_datasets` 覆盖全部候选 → 停止转 `brain-nextMove-analysis`。
- **提示词映射**：region=EUR、delay=D1、maxTrade=ON（profile 允许 delay 1/0）由此步锚定。

### 步 2（S0）数据集体检 + 金字塔配额
- **目的**：`score_datasets.py` 评分选 1 个未点亮金字塔数据集；锁白名单写 ledger。
- **输入**：`$REGION=EUR`；EUR profile `datasets.green=[model 系/pv 系/analyst 系]`；提示词"仅本季未点亮金字塔数据集挑 1 个"。
- **命令**：
  ```powershell
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir tracking/EUR score --region EUR
  mcp__wqb-db__get_ledger_key region=EUR key=s0_ranking
  ```
- **产物**：`ledger s0_ranking` / `s0_whitelist` / `*_dead`；≥2 个非 MODEL（pyramid_quota）。
- **失败分支**：无非 MODEL → 写 findings 不退回纯 MODEL；全硬排除 → 回步 1 换 region。
- **提示词映射**："挑 1 个金字塔数据集 + 禁止频繁切换"在此步落实（EUR 已知 returns 反转拥挤 prod 0.95 墙，优先 `alphaCount=0` 零竞争集）。

### 步 3（S1）字段扫描 + 理解
- **目的**：生成 typed catalog；字段理解回写 `s1_<ds>_d<delay>`。
- **输入**：`$DS`（步2选定）、`$DELAY=1`、`$DTYPE`（catalog.data_type）。
- **命令**：
  ```powershell
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir tracking/EUR scan-fields --dataset $DS
  ```
- **产物**：`fields` 表 + ledger S1 决策；**gate.py 后续依赖此 `EUR_<ds>_fields.json`**。
- **失败分支**：字段数<10 → 退回步2白名单外；VECTOR 比例须 `get_datafields` 确认，步4 传对 `--data-type`。

### 步 4（S2）选波：概念优先生成（GEM 强制）
- **目的**：`brain-makeSomeGem` 产表达式；`build-wave` 只去重/分桶/配给。
- **输入**：`priors.json`（DB KB `region_kb.win_recipes` + `template_kb`）；EUR profile 硬约束"每波 ≥2 槽按 win 机制换腿"。
- **命令**：
  ```powershell
  mcp__wqb-db__get_ledger_key region=EUR     key=region_kb
  mcp__wqb-db__get_ledger_key region=KB      key=template_kb
  Set-Location "$WQ_GEM_ROOT/scripts/headless_runner"
  & $WQ_PY run.py --config config.json --data-category <CATEGORY> `
      --region EUR --delay 1 --dataset-id $DS --universe $UNIVERSE `
      --instrument-type EQUITY --data-type $DTYPE --priors-file priors.json --detached
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir tracking/EUR build-wave --from-db --dataset $DS --wave $W
  ```
- **产物**：`expressions` 表（status=`gem`/`enhanced`）；ledger idea。
- **失败分支**：GEM 未入库 → 查任务恢复清单，确认失败才回退；候选不足 → enhance/扩组合，仍不足换数据集。
- **提示词映射**："1–2 字段、优先单数据集"在此步落实；⚠️ **张力**：EUR win 配方本身是 `0.4 MODEL + 0.6 PV` 的**两数据集 combo**，与提示词"优先单数据集、双数据集须论文支撑"冲突（见 §4-6）。

### 步 5（S2→S3）门禁
- **目的**：语法 + 5 闸 + 批级多样性。
- **输入**：`--from-db`（读 `expressions` 表本波候选）；或 `--candidates` JSON。
- **命令**：
  ```powershell
  & $WQ_PY tools/wave_gate.py --campaign-dir tracking/EUR --dataset $DS --wave $W --from-db
  ```
  VECTOR 加 `--fix`；repair 批加 `--skip-diversity-gate`。
- **产物**：`cache/gate_wave<W>_<DS>.json` + `.out.txt`；DB `gate_results/EUR/<W>/<DS>`（`all_pass`/`passed`/`total`/每候选 `issues`）。
- **失败分支**：语法 FAIL 先修；多样性 FAIL → 回步4补骨架；闸2跨集 FAIL → 拆回单集组合。
- **提示词映射**：**算子数<8 上限门缺失**（见 §4-2，gate.py 仅校验 `required_operators`/`per_batch_min_operators`，无上限计数）。

### 步 6（S3）五槽回测
- **目的**：五槽填槽并发回测（multi×8）。
- **输入**：`expressions` 表 READY 候选；并发模型 `wqb-concurrency` §8（五槽填槽）。
- **命令**：
  ```powershell
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir tracking/EUR pipeline --dataset $DS --wave $W
  & $WQ_PY tools/batch_status.py --ids <id1> <id2> ... --watch
  ```
- **产物**：`backtest_results` / `wave_results` / checkpoint；multisim id（Location）。
- **失败分支**：整批 CANCELLED → 回步5；429 → ≤6 并发、批间≥45s。
- **提示词映射**：`pipeline.submit_batch` 走 `POST /simulations`（=multi_create_simulate×8），**禁用单条 create_simulate** ✅ 与提示词一致。

### 步 7（S4）诊断改进
- **目的**：walls 诊断，阈值不过则优化。
- **输入**：本波 `wave_results`。
- **命令**：
  ```powershell
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir tracking/EUR review --dataset $DS --wave $W
  ```
- **产物**：诊断报告；不达标转 `brain-how-to-pass-AlphaTest` → `wq-brain-alpha-optimization-v1`（Mode B 70% + Mode A 30%）。
- **失败分支**：`prod_corr≥0.7` → Mode B 换概念；同想法>10 种结构仍不过 → 步9 写 `dead_end`，回步2。
- **提示词映射**："ra_failed_count=0 / risk neutralization 至少一条风险因子中心化良好"在此步逐 alpha 核对 `thresholds.review`。

### 步 8（S4→S5）稳健闸与提交判定  ★关键
- **目的**：稳健性 + 过拟合 + 提交判定。**SOP 强制经 `brain-alpha-robustness`**。
- **输入**：每 alpha id（步6/7 产出）。
- **命令**：
  ```powershell
  # 强制步骤（覆盖上一轮 dryrun 的 gap #3）：
  #   brain-alpha-robustness skill → earnings/PnL 归因 + anti-overfit
  & $WQ_PY tools/submit_verdict.py --alpha-id <ALPHA_ID> --with-quota
  ```
- **产物**：稳健报告 + judge  verdict（READY / 不达标）。
- **失败分支**：`PASS_CHEAP`≠可提交；PROD/SELF 不过 → 回步7；配额耗尽按最早+48h。
- **提示词映射**："每找到一个 alpha 立即 test robust + 严格过拟合测试" → **此步已被 ra-pipeline 原生覆盖**（上一轮 toolkit-only dryrun 的 gap #3 在此解决 ✅）。`judge READY 只报告、等用户确认` → 与提示词"不自动提交、交还用户"一致 ✅。

### 步 9（S6）复盘回写
- **目的**：未回写视为本波未完成。
- **命令**：
  ```powershell
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir tracking/EUR wave upsert --wave $W --verdict <PASS|FAIL|PARTIAL> --extra @notes.json
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir tracking/EUR registry add-win --extra @win.json
  ```
- **产物**：`wave_results.verdict` + `registry_empirical`；OS ACTIVE/全闸 PASS 必须 `add-win`。
- **提示词映射**：每 10 轮回测做一次多样性评估（`diversity_audit.py`）在此步归集；10 个合格 alpha 达标后停。

---

## 三、阈值冲突矩阵（用 ra-pipeline 作头才暴露）

ra-pipeline 规定"阈值不复写，引用 `src/wqb/config.py` 的 `GATES`"。当下对齐状态：

| 指标 | 提示词要求 | `GATES_INTERNAL` | `thresholds.json`(EUR) | 冲突 |
|---|---|---|---|---|
| sharpe | >1.58 | 1.58 | 1.58 | ✅ 一致 |
| fitness | >1.0 | 1.0 | 1.0 | ✅ 一致 |
| 2Y sharpe | >1.6 | —（GATES 无） | 1.6 | ⚠️ 仅 thresholds 有 |
| **margin** | **>15bp** | **10bp** | **5bp** | ❌ 三处不一致（10/5 均比 15 松） |
| **turnover 上限** | **30%** | **20%** | 30% | ❌ GATES 比提示词更严，25–30% 会被 GATES 拒 |
| **self_corr** | **≤0.7** | **0.50** | 0.7 | ❌ GATES 比提示词更严 |
| prod_corr | ≤0.7 | 0.70(PLATFORM) | 0.7 | ✅ 一致 |
| ra_failed_count | =0 | — | 0 | ⚠️ 平台级检查，GATES 无字段 |
| operators | <8 | — | — | ❌ 无上限门（gate.py 缺失） |

**结论**：若严格按 ra-pipeline 走 `GATES`，提示词中 **turnover 25–30% 段**与 **self_corr 0.5–0.7 段**的 alpha 会被自动拒（GATES 更严），而 **margin<15bp** 的 alpha 会漏过（GATES 只卡 10bp）。需决定"以谁为准"。

---

## 四、缺口与张力（ra-pipeline 框架下重估）

| # | 项 | 性质 | 处理 |
|---|---|---|---|
| 1 | **margin 三处不一致**（15/10/5bp） | 配置冲突 | 须拍板统一为 15bp（最严），并同步 `GATES_INTERNAL.margin_bp_min` 与 `thresholds.json` |
| 2 | **算子数<8 无上限门** | gate.py 缺失 | `gate.py` 增加 operator-count 校验（已源码确认无此逻辑） |
| 3 | **test robust + 过拟合** | ✅ 已解决 | ra-pipeline 步8 强制 `brain-alpha-robustness`，无需额外补 |
| 4 | **prod_corr>0.7 提交前无自动把关** | 缺自动门 | `hard_gates.prod_correlation_max=0.7` 仅为配置；建议最终 10 候选用平台相关性 API 做 return-corr<0.4 + prod_corr≤0.7 双闸 |
| 5 | **turnover 上限冲突**（提示词 30% vs GATES 20%） | 阈值冲突 | 须选：放宽 GATES 至 30%，或接受 20–30% 段被排除 |
| 6 | **self_corr 冲突**（提示词 0.7 vs GATES 0.50） | 阈值冲突 | 须选：放宽 GATES 至 0.7，或接受 0.5–0.7 段被排除 |
| 7 | **universe 冲突**（profile TOP1600 / settings TOP2500 / 提示词"遍历"） | 配置+策略 | 提示词"遍历不同 universe"无内置 sweep；须先定基准 universe（TOP2500 或 profile TOP1600）并记录 ledger 防重蹈 TOP800 覆辙 |
| 8 | **EUR win 配方是两数据集 combo** vs 提示词"优先单数据集、双数据集须论文" | 策略张力 | win 配方 `0.4 MODEL+0.6 PV` 本身无显式论文背书；若严格守提示词，需补论文或改走单数据集换腿 |

---

## 五、最终判定

**编排层（I/O）**：ra-pipeline 九步全部命令真实存在、调用链闭环（`wave_gate.py`→`gate.py`→`pipeline`→`review`→`submit_verdict`）、离线测试 65 passed、gate/pipeline 契约已实证。**编排能正确输入输出。**

**策略层（对齐）**：在正式开跑前，须由你拍板 4 项：
1. margin 统一为 **15bp**（改 `GATES_INTERNAL` + `thresholds.json`）；
2. turnover 上限（20% vs 30%）与 self_corr（0.50 vs 0.70）以谁为准；
3. 基准 universe（TOP2500 沿用 / 切 profile TOP1600）；
4. EUR win 两数据集 combo 是否需补论文（或改单数据集换腿）。

补完 ②算子数<8 上限门、④真实收益相关性双闸后，即可按 ra-pipeline 从步 1 正式开跑，目标 10 个风格迥异、未提交、彼此 corr<0.4 的单数据集 EUR alpha，候选交还你手动提交。

*附：本轮新核查 `tools/wave_gate.py`（步5 真实入口，包装 gate.py）、`src/wqb/config.py GATES`（阈值冲突源）。上一轮 `reports/dryrun_eur_report.md` 的 gap #3 在本框架下已原生解决。*
