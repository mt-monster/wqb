# EUR REGULAR 战役 — ra-pipeline 九步 dry-run 执行追踪

> 日期：2026-08-25 | 编排头：`wq-brain-ra-pipeline` v2.1（L-RA）
> 目的：以 ra-pipeline 为头，把 EUR REGULAR 提示词作"头指令"灌入，逐九步**真实执行**命令、展示每步 I/O。
> 环境：本地 `data/wqb.db`（12MB，当日 20:38 更新）在位；MCP（:8876 / wqb-db / wq-brain-http）**未运行**；GEM headless runner 走 deepseek API（需网络，config 已配密钥）。

## 一、九步执行追踪（命令 → 输入 → 输出 → 状态）

| 步 | SOP 命令 | 真实执行 | 关键输出 | 状态 |
|---|---|---|---|---|
| **S-PRE 步1 查表** | `registry list` + `mcp__wqb-db__*` | ✅ 真跑 `registry list` + 直读 DB | EUR 81 条（6 campaign + dead_ends）；settings: TOP2500/D1/SUBINDUSTRY/decay4/maxTrade=ON/startDate=2014；当前波≈**wave19**；`entry_verdict=active` | ✅ 本地可执行 |
| **S0 步2 score** | `campaign.py score --region EUR` | 🔌 需平台 | 命令+契约展示；产物 `eur_dataset_ranking.json` 已在场（178 数据集，TOP=continuation_score 0.9012）；`datasets` 表 coverage/alphaCount 全 NULL（score 写 ledger 非该表） | 🔌 联网 |
| **S1 步3 scan-fields** | `campaign.py scan-fields --dataset $DS` | 🔌 需平台 | 产物 `eur_model238_fields.json` 已在场（field_count=44，fields=[id/coverage/alphaCount]） | 🔌 联网（产物已落盘） |
| **S2 步4 build-wave** | `build-wave --file … --wave 20` | ✅ 真跑 | input=12→selected=5；自动签覆盖契约（12 算子）；注入 5 条 SOP 规则；写 `db expressions/EUR/20 n=5` | ✅ 本地可执行（有 DB 副作用） |
| **S3 步5 wave_gate** | `tools/wave_gate.py --from-db --wave 20` | ✅ 真跑 | 语法 5/5 PASS；**gate all_pass=False, passed=0/5 → FAIL**（EXIT=1）；根因 `[FIELD] 未验证字段` | ✅ 本地可执行 |
| **S4 步6 pipeline** | `pipeline run --wave 20 --dry-run` | ✅ 真跑 | gate 过 0 式；`batch=8` 七槽填槽 n_slots=0；**未提交**；ckpt→`ledger_kv/EUR/ckpt_w20` | ✅ 本地可执行（dry-run 不提交） |
| **S5 步7 review** | `campaign.py review` | 🔌 需提交+联网 | `review_wave.py` 真实 CLI=`--multisim/--alphas`；本地 `backtest_results` EUR 行=0（指标在平台侧）；无输入可评 | 🔌 联网 |
| **S6 步8 submit_verdict** | `tools/submit_verdict.py --alpha-id X --with-quota` | 🔌 需平台 | 真实 CLI=`--alpha-id [--with-quota]`；做 `GET /alphas/{id}/submit`+配额双视图；judge READY 只报告不提交 | 🔌 联网 |
| **S9 步9 复盘回写** | `wave upsert` / `registry add-*` | ✅ 真跑（`--dry-run`） | `wave upsert --dry-run` → `[DRY] wave20 校验通过，未写入 -> EUR/open`；`add-dead-end`/`add-win` 均带 `--dry-run` | ✅ 本地可执行 |

✅ = 本沙箱真实执行；🔌 = 依赖 MCP/平台网络，沙箱不可跑（产物/契约已呈现）。

## 二、过程中暴露的真实问题（执行才看得到）

### A. SOP 命令语法与 toolkit 实况漂移（3 处，须修 SOP）
1. **`pipeline` 是 `{quota, run}` 子命令结构**：SOP 写 `pipeline --dataset $DS --wave $W` 实际应为 `pipeline run --dataset $DS --wave $W`（否则 `invalid choice`）。
2. **`review` 是顶层子命令，且 CLI 不符**：SOP 写 `pipeline review --dataset/--wave`；实际 `campaign.py review`→`review_wave.py`，入参为 `--multisim/--alphas/--tag`，**无 `--dataset/--wave`**。
3. **`build-wave --file` 已废弃**：SOP 示例用 `--file`，help 标注"已废弃，请 --from-db"；且直跑 campaign.py 会 WARN `No module named 'wqb'`（多样性增强降级，不致命）。

### B. S3 FIELD 闸正确拦截跨数据集字段（0/5）
喂入 `EUR_mining_candidates.json` 的 5 式引用 `long_term_five_day_industry_relative_return` / `long_term_balance_sheet_rank_europe` / `long_term_return_on_equity` 等，均**不在 `ml_factor_proj` typed catalog** → 全部 `[FIELD] 未验证字段` FAIL。这正面验证了 SOP"单数据集 alpha"纪律被 gate.py 硬性执行；修复路径=回步4 用字段归属同一数据集的表达式重选波。

### C. S4 `--dry-run` 行为符合预期
gate 0 过闸 → `batch_gates 无表达式通过闸1-5，跳过批级闸` → `[dry-run] 将分 0 批（batch=8）` → **不 POST `/simulations`**。即"multi_create_simulate×8"批量逻辑已就位，但被闸挡住时无副作用，绝不偷偷提交。

### D. 本地 DB 副作用（本次 dry-run 写入，可回滚）
- `build-wave` 向 `expressions` 表写入 **EUR/20 共 5 条**；
- `wave_gate.py` 写入 `gate_results/EUR/20/ml_factor_proj`；
- `pipeline --dry-run` 写入 `ledger_kv/EUR/ckpt_w20`。
回滚（如需）：
```sql
DELETE FROM expressions WHERE region='EUR' AND wave='20';
DELETE FROM gate_results WHERE region='EUR' AND wave='20' AND dataset='ml_factor_proj';
DELETE FROM ledger_kv WHERE region='EUR' AND key='ckpt_w20';
```

## 三、结论
- **编排 I/O 正确性**：所有**本地可执行步骤**（S-PRE / S2 / S3 / S4 / S9）均按 SOP 真实跑通，输入→产物链闭合，无缺环。
- **网络步骤**：S0 score / S1 scan-fields 重跑 / S5 review / S6 submit_verdict 依赖 MCP（:8876），沙箱未起故未实跑；但其产物已落盘、契约已核对，联网后即可接上。
- **一处须先修**：SOP 的 `pipeline`/`review` 命令写法已与 toolkit 实况漂移（见 A），建议在 `wq-brain-ra-pipeline` SKILL.md 改正，否则照抄 SOP 会直接 argparse 报错。
- **未做"补代码"**：按你的要求，未改任何 gate.py / config.py / thresholds；4 处原缺口（margin/turnover/self_corr 阈值冲突、算子数<8 上限门、prod_corr 真实相关性双闸）维持上一轮结论，本次仅验证流程。
