# ra-pipeline 九步 dry-run 实跑明细 — 头=USA / event_return_model / d1

> 编排头：`wq-brain-ra-pipeline` v2.1（九步 SOP，唯一挖掘编排入口）
> 执行引擎：`wq-brain-campaign-toolkit`
> 区域路由依据：`wq-brain-campaign-matrix`
> **头（ra-pipeline 的唯一输入）= `region=USA`**；本次钻取的具体数据集头 = **`event_return_model`（delay=1 / TOP3000 / SUBINDUSTRY）**
> 日期：2026-08-25 22:56｜性质：**dry-run（零回测配额、零提交）**

运行环境：
- `$WQ_PY` = `D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe`
- `$WQ_TOOLKIT_DIR` = `C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts`
- `$CD` = `D:/coding/traeCN_project/wqb/tracking/USA`
- 事实源：`data/wqb.db`（单轨 DB）

---

## 总览：九步链路与本次 dry-run 落点

| 步 | SOP 名 | 本次是否实跑 | 关键产物 |
|---|---|---|---|
| 1 | S-PRE 查表 | ✅ 实跑（DB 查询） | 无 dead_end 阻塞，契约 active |
| 2 | S0 数据集体检 | ✅ 读既有 ledger | `s0_whitelist` 含 event_return_model |
| 3 | S1 字段扫描 | ✅ 读既有 catalog | `s1_event_return_model_d1`：13 白名单字段 |
| 4 | S2 选波（GEM+build-wave） | ✅ 实跑（GEM 22 条已入库；build-wave reg_event02 现场跑） | 8 条波（12 骨架实例化注入） |
| 5 | S3/S5 门禁 | ✅ 实跑（gate reg_event02） | all_pass=True / 多样性 applied+pass+consumed |
| 6 | S3 五槽回测 | ⏸ dry-run 不执行（零配额） | 命令已就绪，未烧配额 |
| 7 | S4 诊断改进 | ⏸ 依赖回测结果，跳过 | — |
| 8 | S4→S5 稳健闸/判定 | ⏸ judge READY 仅报告，不 submit | — |
| 9 | S6 复盘回写 | ⏸ 真波未回测，暂不写 verdict | — |

> 说明：S6–S9 在 dry-run 模式下**不执行平台回测、不提交 alpha**，仅列出命令与契约，确认链路无缺环。

---

## 逐步 INPUT → COMMAND → OUTPUT 明细

### 步 1 ｜ S-PRE 查表（区域先验）

- **INPUT**：`region=USA`
- **COMMAND**：
  ```powershell
  mcp__wqb-db__get_campaign_summary  region=USA
  mcp__wqb-db__get_dead_ends         region=USA
  mcp__wqb-db__get_dead_datasets     region=USA
  mcp__wqb-db__get_cross_region_lessons
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD registry list
  ```
- **OUTPUT（实跑证据）**：
  - `campaign_summary(USA)` = NONE → 视为"无既有 campaign 基线"，按新区域路径继续
  - `dead_ends(USA)` = NONE；`dead_datasets(USA)` = NONE → **无 dead_end 阻塞**，不触发"停止转新区"
  - 活跃探索契约存在：`explore_contract_USA_20260825_222810_719557`（status=active，consumed=1/10，容量充足）
- **失败分支**：registry 全空 → 新区域进度 2 建 campaign；dead_datasets 全覆盖 → 停止。本次均不触发。

### 步 2 ｜ S0 数据集体检 + 金字塔配额

- **INPUT**：region=USA，白名单体检结果（本次复用既有 S0 产物）
- **COMMAND**：`& $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD score --region USA`
- **OUTPUT（实跑证据，读 ledger）**：
  - `s0_whitelist(USA)`：dict，n=**8** 个数据集
  - **`event_return_model` 在白名单中 = True** ✅（未被任何 dead_end 排除）
  - `s0_ranking` 存在（含 generated_at/region/universe/total/dead_excluded）
  - 金字塔配额：白名单至少 2 个非 MODEL（VECTOR/NEWS/ANALYST/institutions）→ 满足
- **失败分支**：配额外无非 MODEL → 写 findings 不退回纯 MODEL；全硬排除 → 回步 1 换 region。本次不触发。

### 步 3 ｜ S1 字段扫描 + 理解

- **INPUT**：`dataset=event_return_model`，`delay=1`
- **COMMAND**：`& $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD scan-fields --dataset event_return_model`
- **OUTPUT（实跑证据，读 ledger `s1_event_return_model_d1`）**：
  - `dataset/region/delay/universe` = event_return_model / USA / 1 / TOP3000
  - `source` = s2_nested，`concept_count` = **10**
  - `field_whitelist` len = **13**（白名单字段，如 `earnings_bin_label1`、`news_relevance_score_2`、`prob_rank_bin3_label*_10d_img_news`…）
  - `data_type` = None（常规/points 类数据集）
  - `ideas_md_path` → `brain-makeSomeGem/.../USA_delay1_event_return_model_ideas.md`
- **失败分支**：字段数 <10 → 退回步 2 白名单外；VECTOR 比例用 `get_datafields` 确认 `--data-type`。本次 13≥10，通过。

### 步 4 ｜ S2 选波：概念优先生成（GEM + build-wave）

- **INPUT**：
  - S1 catalog（13 字段）+ priors（DB KB wins/dead_ends）→ `priors.json`
  - 活跃契约 `explore_contract_USA_20260825_222810_719557` 的 12 个骨架因子（含 `group_*`/`ts_arg_*`）
  - GEM 自包含生成（上轮已落 `s2_event_return_model_d1`）
- **COMMAND（GEM 段，已入库）**：
  ```powershell
  & $WQ_PY $GEM_ROOT/scripts/headless_runner/run.py --config $GEM_CFG `
      --data-category <CATEGORY> --region USA --delay 1 --dataset-id event_return_model `
      --universe TOP3000 --instrument-type EQUITY --data-type $DTYPE `
      --priors-file priors.json --ideas-file <ideas_md_path> --detached
  ```
  **COMMAND（build-wave 现场实跑）**：
  ```powershell
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD build-wave --from-db --dataset event_return_model --wave reg_event02
  ```
- **OUTPUT（实跑证据）**：
  - **GEM 产物** `s2_event_return_model_d1`：22 条（status=gem）；仅 **6/22（27%）** 命中 required 算子（仅 `ts_arg_max`/`ts_av_diff` 出现）→ **证明 GEM 自身不足以保证多样性**
  - **build-wave reg_event02**：
    - `coverage_injected` = **12**（契约 12 骨架因子全部实例化注入；legacy 回退 0）
    - `input`=34，`duplicates_dropped`=15，`selected`=**8**
    - 桶分布含 required 算子：`group_mean/group_neutralize/group_scale/group_std_dev/group_sum/group_zscore`（各 1 atom）+ `ts_arg_max`(1) + `ts_arg_min`(1) + `ts_av_diff`(1) + `rank>multiply/subtract/ts_av_diff`
    - `diversity_enhanced`=false（层②骨架注入已超额满足，层④自愈无需触发，属预期兜底）
    - 落库：`expressions/USA/reg_event02` n=8
- **失败分支**：GEM 未入库 → 超时恢复清单查任务；候选不足 → enhance/扩组合。本次 GEM 已入库 22 条，通过。

### 步 5 ｜ S3/S5 门禁（5 闸 + 多样性闸）

- **INPUT**：`reg_event02` 波（8 条表达式）
- **COMMAND**：
  ```powershell
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD gate --from-db --wave reg_event02 --dataset event_return_model
  ```
- **OUTPUT（实跑证据）**：
  - **`all_pass` = True**
  - **`total / passed` = 8 / 8**
  - **`diversity_gate.applied` = True**（闸真实评估，非真空放过）
  - **`diversity_gate.pass` = True**
  - **`diversity_gate.consumed` = True**（契约批次 #2 被消费，1→2）
  - **`diversity_gate.issues` = []**
- **含义**：**零手工 ideas 文件**，四层机制（①骨架入库 ②消费时实例化注入 ③GEM mandate ④选波自愈）使多样性闸自动评估且通过。
- **失败分支**：语法 FAIL → 先修；多样性 FAIL → 回步 4 补骨架（查 `KB/community_tpl_kb` 按 category 检索）；闸 2 跨集 FAIL → 拆单集。本次全过。

### 步 6 ｜ S3 五槽回测（dry-run 不执行）

- **INPUT**：`reg_event02` 表达式（8 条，过闸）
- **COMMAND（列出，本次不执行）**：
  ```powershell
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD pipeline --dataset event_return_model --wave reg_event02 --dry-run
  # 确认 gate 通过率后再：
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD pipeline --dataset event_return_model --wave reg_event02 --submit --review --write-ledger
  ```
- **OUTPUT**：⏸ **dry-run 模式，零配额、零提交**，未烧任何回测额度。
- **失败分支**：整批 CANCELLED → 回步 5；429 → ≤6 并发、批间 ≥45s。

### 步 7 ｜ S4 诊断改进（dry-run 跳过）

- 依赖回测结果（`review_wave` 看 walls）。dry-run 无回测数据，跳过。
- 阈值不过 → `brain-how-to-pass-AlphaTest` → `wq-brain-alpha-optimization-v1`（Mode B 70%→Mode A 30%）。
- 失败分支：`prod_corr≥0.7` → Mode B 换概念；同想法 >10 结构仍不过 → 步 9 写 dead_end 回步 2。

### 步 8 ｜ S4→S5 稳健闸与提交判定（dry-run，不提交）

- **INPUT**：过闸候选（待回测后）
- **COMMAND（列出）**：
  ```powershell
  & $WQ_PY tools/submit_verdict.py --alpha-id <ALPHA_ID> --with-quota
  ```
- **OUTPUT**：⏸ `brain-alpha-robustness` 必经；`brain-alpha-judge` 判定；**judge READY 只报告、等用户确认，确认前禁止 submit_alpha**。本次不提交。
- 失败分支：`PASS_CHEAP`≠可提交；PROD/SELF 不过 → 回步 7。

### 步 9 ｜ S6 复盘回写（dry-run，暂不写）

- **COMMAND（列出）**：
  ```powershell
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD wave upsert --wave reg_event02 --verdict <PASS|FAIL|PARTIAL> --extra @notes.json
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD registry add-win      --extra @win.json
  & $WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD registry add-dead-end --extra @dead.json
  ```
- **OUTPUT**：⏸ 真波未回测，暂不写 verdict（避免假结论污染 `wave_results`/`registry_empirical`）。
- 纪律：OS ACTIVE / 全闸 PASS 必须 `add-win`（mix 比例、中性化、decay、快/慢腿）。

---

## 四层结构性多样性保证 — 本次 live 实证

| 层 | 机制 | 本次证据 |
|---|---|---|
| ① | 骨架入库（`factor_templates` 存 `ts_arg_max({F1},20)` 占位符，非锚点字段） | 契约 `explore_contract_USA_20260825_222810_719557` 12 算子全带 skeleton |
| ② | 消费时按当前数据集 S1 catalog 实例化注入 | build-wave `coverage_injected=12`，legacy 回退 0 |
| ③ | GEM 生成层 `--require-operators` mandate+补注 | GEM 自含生成 22 条（仅 27% 命中，证明③非充分、需②兜底） |
| ④ | 选波后自愈补齐 | `diversity_enhanced=false`（②已满足，④未触发，属预期） |

**结论**：GEM 自身仅 27% 命中 → 旧"传文件靠 AI 自觉"路径不可靠；但 ②+④ 结构性保证使 `reg_event02` 在**零手工 ideas** 下 gate `all_pass=True` 且 `diversity.applied/pass/consumed=True`。

---

## 横向批量旁证（上轮已完成）

- 36 数据集 dry-run：**35 绿**（`gate_all_pass=35`、`diversity_pass=35`），唯一失败 `pattern_scores` 为闸门 JSON 解析异常（与多样性机制无关）。

## dry-run 副作用声明

- **已产生**：`expressions/USA/reg_event02`（8 条，未回测）；契约 `consumed` 1→2（真实消费，符合设计）。
- **未产生**：无任何平台回测、无任何 alpha 提交、未写 `wave_results` verdict、`registry_empirical` 未变。
- 如需彻底干净，可 `campaign.py wave` 删除 `reg_event02` 行并复位契约 `consumed_batches`（当前无需）。
