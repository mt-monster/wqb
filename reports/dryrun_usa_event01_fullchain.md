# USA REGULAR 战役 Dry-Run 执行报告（S-PRE → S3，全链路真实 I/O）

> 运行时间：2026-08-25 21:32–21:38 GMT+8
> 模式：**dry-run** —— S0/S1/S2/S3 走真实平台调用 + 真实 DB 读写；**S4 不提交回测（零配额消耗）**；judge 只报告不提交。
> 数据源：WorldQuant BRAIN REST（`api.worldquantbrain.com`）+ 本地 `data/wqb.db`（单一事实源）
> 工具链：`wq-brain-campaign-toolkit/scripts`（campaign.py 派发）+ `brain-makeSomeGem` headless runner + MCP venv python

---

## 0. 跑批对象
- 区域：USA / delay=D1 / universe=TOP3000 / neutralization=SUBINDUSTRY / decay=5 / maxTrade=OFF
- 目标：产 10 个可提交 REGULAR alpha（停止闸=10，SOP 原生，非默认 4）
- 代表数据集（绿牌方向 event/analyst/news）：**event_return_model**（本次真实跑完 S2→S3）

---

## 1. 各步真实 I/O

### S-PRE 查表（registry 实证层）
- `registry list`：USA 共 **14 条** = 3 campaign（mdl177 / option9 / pv1）+ **10 dead_end**（含 `USA-ML-FACTOR-PROJ-PROD-SATURATED`、`USA-OPTION-CHART-MODEL-PROD-SATURATED`、`USA-VALUE-PRODCORR` 等）+ 1 win（`USA-SA-KPGvRMg1`）
- USA profile：`entry_verdict=active`，饱和市场正交战（pv1/mdl177 红牌，option9/analyst/event/news 绿牌，prod 预警 0.6）
- 结论：先验与 profile 一致，排除集明确。

### S0 数据集体检 + 锁白名单（真实平台 `GET /data-sets`）
- `campaign.py score` → USA **294 数据集**全部评分，**95 个有效**（42 tier1 / 53 tier2 / 1 floor）
- 白名单构造（落 `ledger_kv USA/s0_whitelist`）：**40 个数据集**
  - 排除 2 个 PROD 饱和死路：`ml_factor_proj`、`option_chart_model`
  - 排除 profile 红牌：`pv1`（mdl177 未进排名）
  - 金字塔配额校验：24 个非 MODEL（pv/news/analyst/socialmedia/sentiment/other）→ **OK（≥2）**
- 注：`score --region` 被拒（region 从 settings.json 取，非 SOP 写法）→ 命令漂移 #1

### S1 字段扫描（真实平台 `GET /data-fields`）
- 对白名单代表数据集实跑：`pattern_scores`(504 MATRIX)、`event_return_model`(59 MATRIX)、`analyst_consensus`(3424 VECTOR) → 落 `fields/USA/`
- `event_return_model` 回写 S1 字段白名单（落 `ledger_kv USA/s1_event_return_model_d1`）：**13 字段**（source=s2_nested）

### S2 GEM 生成候选池（真实 DeepSeek 调用，落库不提交）
- `brain-makeSomeGem` headless runner，priors=DB 中 10 条 USA dead_ends
- 产出波次 `s2_event_return_model_d1`：**9 条表达式**（status=gem）
- 全部字段引用 ∈ 13 字段白名单 → **无 token-name 隐患**（关键，呼应历史 token-name 雷区）
- 9 条表达式（均为 1–2 字段，符合提示词约束）：
  1. `quantile(multiply(subtract(ts_backfill(prob_rank_bin3_label2_10d_img_news,66),ts_backfill(prob_rank_bin3_label0_10d_img_news,66)),subtract(1,ts_backfill(prob_rank_bin3_label1_10d_img_news,66))))`
  2. `quantile(multiply(ts_backfill(prob_rank_bin5_label4_10d_img_news,66),ts_backfill(earnings_bin_label1,66)))`
  3. `quantile(multiply(ts_backfill(prob_rank_bin5_label4_5d_img_news,66),ts_backfill(news_relevance_score_2,66)))`
  4. `quantile(subtract(divide(ts_backfill(rank_bin3_5d_img_news,66),2),divide(ts_backfill(rank_bin5_5d_img_news,66),4)))`
  5. `quantile(subtract(ts_backfill(prob_rank_bin5_label4_20d_img_news,66),ts_backfill(prob_rank_bin5_label4_5d_img_news,66)))`
  6. `quantile(subtract(ts_backfill(prob_rank_bin5_label4_5d_img_news,66),ts_backfill(prob_rank_bin5_label0_5d_img_news,66)))`
  7. `quantile(subtract(ts_backfill(prob_rank_bin5_label4_5d_img_news,66),ts_backfill(prob_rank_bin5_label3_5d_img_news,66)))`
  8. `quantile(subtract(ts_backfill(rank_bin5_5d_img_news,66),ts_backfill(rank_bin5_20d_img_news,66)))`
  9. `quantile(ts_delta(ts_backfill(prob_rank_bin5_label4_10d_img_news,66),5))`

### S3 选波 + 八闸预检（真实，dry-run 不回测）
- **S3a 选波** `build-wave --from-db --dataset event_return_model --wave event01`
  - input=21 / 去重 12 / 选 **8**；分桶 `quantile>subtract`(5)+`quantile>multiply`(3)+`quantile>ts_delta`(1)
  - `diversity_enhanced=false`（警告 `No module named 'wqb'` → 该 venv 缺 wqb 包，多样性增强降级，非阻塞）
- **S3b 八闸** `gate --from-db --wave event01 --dataset event_return_model`
  - 字段闸（闸2）：**passed=8/8，全部 PASS，issues=[]** ✅
  - 多样性闸（diversity_gate）：`applied=true, pass=false` ❌
    - 失败原因：`explore_contract_USA_20260825_185321` 契约要求每批 ≥2 条使用 `group_*`/`ts_arg_*` 算子，实际 **0/2 命中**
    - 根因：GEM 9 条表达式算子全为 `ts_backfill`/`ts_delta`/`multiply`/`subtract`/`divide`/`quantile`，**无 group 族算子**；且 `diversity_enhanced` 降级导致 build-wave 未注入达标算子
  - **`all_pass=false` → 在实跑模式下会拦截进入 S4 回测**

---

## 2. 核心发现

| # | 发现 | 性质 | 处置 |
|---|------|------|------|
| A | FIELD 闸 8/8 PASS，9 条表达式字段全部 ∈ 白名单 | 好消息 | 无 token-name 隐患，GEM 字段引用可靠 |
| B | **多样性闸 FAIL（0/2 group/ts_arg 算子）** | 实跑阻塞点 | GEM 算子单一化（ts_backfill/ts_delta 族）；需 Mode B 引入 group_*/ts_arg_* 算子或修复 diversity_enhanced |
| C | `diversity_enhanced=false`（venv 缺 `wqb` 模块） | 环境降级 | 非阻塞，但使 coverage 注入失效，放大 B |
| D | SOP→工具漂移：`tools/wave_gate.py`（SKILL 行168）不存在 | 文档漂移 | 真实入口 = `build-wave` + `gate`（campaign.py 派发） |
| E | `score --region` 被拒 | 命令漂移 | region 从 settings.json 取 |
| F | gate.py 文档"8 闸" vs campaign.py 派发注释"5 闸" | 文档不一致 | 不影响运行 |

---

## 3. S4 / S5 / S6 在 dry-run 下的行为（未实跑，说明边界）

- **S4 评审链**：AlphaTest 诊断 / Mode B-A / 本地 self·PPAC 快筛 / 归因 / 稳健性闸 / judge 判定 —— 这些**依赖回测数据**。
  本次 S3 多样性闸失败 → 在纪律流程中**不进入 S4 回测**（不耗配额）；judge 判 READY 也只报告不提交（符合提示词提交纪律）。
- **S5 review**：顶层 `review` 命令（CLI `--multisim/--alphas`），依赖回测结果，dry-run 下 N/A。
- **S6 submit_verdict**：只读 `GET /alphas/{id}/submit` + 模拟层检查，**零 POST、零配额**（已在前次 EUR dryrun 验证 BLOCKED 安全）；仅"提交完成后"才跑复盘回写，dry-run 不提交故不触发。

---

## 4. 结论

1. **编排完全可承载 USA 战役**：S-PRE→S3 真实闭环跑通（平台体检→字段扫描→GEM 生成→选波→八闸），DB 单一事实源读写一致（`ledger_kv` + `expressions` + `fields`）。
2. **唯一真实阻塞 = 多样性闸（B 项）**：GEM 生成的 event 族表达式算子过于单一（无 group/ts_arg），撞上 `explore_contract` 契约。这是**信号设计问题，非编排/SOP 阈值问题**——解决路径是 Mode B 换算子骨架（引入 `group_rank`/`group_neutralize`/`ts_arg_max` 等），或修复 venv 的 `wqb` 模块让 `diversity_enhanced` 生效自动注入，无需改动任何 SOP 阈值。
3. **停止闸=10 为 SOP 原生**（非默认 4），无需拍板。
4. **未提交任何 alpha、未消耗回测配额**；所有产出仅落本地 DB / `tracking/USA/`。

---

## 5. 待用户决策（非阻塞，等确认再正式开挖）

- 是否针对 B 项让 GEM 下一轮强制引入 `group_*`/`ts_arg_*` 算子（Mode B 信号层），或先修复 venv `wqb` 模块恢复 `diversity_enhanced` 自动注入？
- 是否继续对白名单其余 39 个数据集按同样 S2→S3 流程批量 dry-run（验证横向可扩展性）？
- S3 失败波次 `event01` 与中间波 `s2_event_return_model_d1`（9 条）已落库，是否需要清理或保留作样本？
