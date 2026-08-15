# KOR 因子挖掘完整流程与经验总结（tracking/KOR 战役实录）

> 本文基于 `D:\coding\traeCN_project\wqb\tracking\KOR\` 的真实战役工程整理。
> 项目定位：**KOR/D1/TOP600** 区域因子（Alpha）挖掘战役。固定设置：`region=KOR, universe=TOP600, delay=1, neutralization=SECTOR, decay=4, truncation=0.08, maxTrade=ON, pasteurization=ON`。
> 资料来源：`tracking/KOR/scripts/*.py`（23 个脚本）、`candidates/*.json`（按 wave 组织的候选表达式）、`reference/*_whitelist.json`（字段白名单）、`reviews/*`（回测评审）、`kor_d1_campaign_state.json`（168 键战役台账）。
> 时间跨度：**2026-08-14 → 2026-08-15**，约 15+ 轮回测、上百表达式、0 达标（截至战役快照）。

---

## 一、KOR 战役流水线全景（端到端 9 步）

```
① 数据集体检（离线包 + 平台 get_datasets）
   → 双门槛 cov≥0.85 & alphaCount≤50，打破"零竞争 vs 高质量"互斥
   → 产出 reference/*_field_whitelist.json（白名单即数据清洗产物）

② 字段收割与类型预检
   → kor_scan_fields*.py 从平台缓存/离线包抽字段
   → 必查 type 列：MATRIX（常规算子）vs VECTOR/event（须 vec_* 聚合）

③ 候选表达式生成（LLM 批量 + 启发式）
   → 源 final_expressions.json（brain-makeSomeGem 产物）
   → batch_validate_kor.py 用 alpha-expression-verifier 做语法闸
   → 产出 candidates/kor_pattern_scores_valid_exprs.json

④ 分层抽样与 diversely 选波
   → select_wave1.py 按骨架风格分桶(C1-C9)，每桶最多 8、字段去重
   → 产出 candidates/kor_waveN_exprs.json（每波 ~8–49 式）

⑤ 提交前三道闸（Preflight）
   → kor_preflight_check.py：语法 / 字段白名单 / 类型&禁用算子
   → 退出码 0=全 PASS，1=禁提交

⑥ 回测提交与固化轮询
   → kor_poll_pipeline.py --multisim <id> [--wait N]
   → COMPLETE→自动调 kor_fetch_metrics.py 拉全量指标；ERROR→逐 child 取错

⑦ 指标评审与达标筛选
   → review_wave*.py：按门槛(sh>1.58/fit>1/2y>1.6/margin>5bp/TVR5–30%/RA全过)排序
   → 产出 reviews/kor_waveN_review.json（all/candidates/near）

⑧ 多样性复盘 + 数据集切换决策
   → kor_op_exploration_stats.py 算子探索率；kor_diversity_review_round10.md 量化评估
   → 纪律：模板穷尽(best<0.8 且 ≥40 式)+论坛无解 才允许切换数据集

⑨ 台账固化（战役记忆）
   → record_*.py 把每波 verdict/白名单/死路写回 kor_d1_campaign_state.json
   → 工具链冻结声明（polling_tooling_freeze）：战役唯一轮询入口
```

---

## 二、各环节实现细节与脚本清单

### 2.1 数据获取与清洗（Stage ①）
- **离线包主导**：WebData 离线镜像 KOR 仅含 `analyst25_TOP600_D1`（207 字段，cov 0.6–0.79，70% 季度更新），且 `analyst25` 平台 alphaCount=3231（高竞争）→ 排除。
- **平台实拉补充**：`record_whitelist_v2.py` 用 `get_datasets` 实时拉 KOR 合法 universe（TOP600）数据集，按 `cov≥0.85 且 alphaCount≤50` 双门槛筛出蓝海候选：
  - Tier1（三项全满）：`behavioral_signals`（cov0.87/alpha0/value9）、`equity_forum_data`（cov0.89/alpha0/value10）、`ai_equity_alpha`（cov1.0/582字段）、`price_signal_dl`、`model238`、`multi_source_model`、`model242`。
  - Tier2 探针：`predictive_starmine`、`global_seasonal_model`、`chart_cnn_alpha`（1010字段）、`model31`。
- **白名单即清洗产物**：`reference/kor_*_field_whitelist.json` 仅收录"平台回测 COMPLETE 验证过的字段"（如 `kor_chart_cnn_alpha_field_whitelist.json` 的 `verified_fields` 记 batch + best_alpha + note），后续表达式生成与预检都受此约束。

### 2.2 特征工程（Stage ②）
- **类型预检是生死线**：`kor_scan_fields*.py` 从平台缓存抽字段；但**字段类型（MATRIX/VECTOR/event）必须查 `get_datafields` 的 type 列**——本地 verifier 只查语法、查不出类型兼容。wave2 `acquisition_model` 因 event 类型字段直接套 `rank/ts_delta/ts_backfill` 导致 24/24 ERROR，浪费 48 次配额（见 §四 陷阱）。
- **信号风格分桶**（来自 `select_wave1.py` 的 C1–C9 骨架）：C1 突破动量、C2/C8 rank-diff、C3 逆向反转、C4 加速度、C5/C9 原始价差/线性混合、C6 信念 zscore。选型时按骨架分层抽样保证多样。

### 2.3 因子生成（Stage ③④）
- **LLM 批量生成**：`brain-makeSomeGem` 产 `final_expressions.json` → `batch_validate_kor.py` 调 `alpha-expression-verifier` 的 `ExpressionValidator` 做语法闸（valid/invalid 分流）。
- **分层抽样选波**：`select_wave1.py` 按表达式前缀算子分 9 桶，每桶 ≤8、字段集合去重（避免同字段重复），字段池不足再回填，单波上限 ~48。
- **实际表达式样例**：
  - wave1（pattern_scores，技术形态）：`ts_delta(adaptive_similarity_upward_breakaway_gap_120, 5)`
  - wave17V（收益）：`multiply(rank(five_day_total_return_dlr1), -1)`
  - wave22K（多腿加权）：`add(add(multiply(rank(vec_avg(recent_earnings_momentum_score)),0.4), multiply(rank(ts_av_diff(vec_avg(annual_price_peak),10)),0.3)), ...)`
  - 后期 wave 明显转向 `vec_avg` 事件聚合 + 多腿加权（0.4/0.3/0.35）组合，体现"换壳/组合优于磨参数"。

### 2.4 因子检验（Stage ⑤⑥⑦）
- **三道预检闸**（`kor_preflight_check.py`）：
  1. 语法（alpha-expression-verifier）；
  2. 字段白名单（表达式字段必须 ∈ verified_fields）；
  3. 类型/禁用：`MATRIX` 禁 `vec_*`；`VECTOR` 事件字段必须经 `vec_*` 聚合（否则 "does not support event inputs" 整批 ERROR）；`ts_min/ts_max` 不可访问（整批 CANCELLED 元凶）；`quantile` 仅 1 参；`banned_patterns` 正则拦截。
- **回测与轮询**（`kor_poll_pipeline.py` + `kor_fetch_metrics.py`）：
  - 直连 `api.worldquantbrain.com`（Basic Auth，凭证 `~/.brain_credentials`）。
  - `COMPLETE` → 自动拉每个 alpha 的 `is.sharpe/fitness/checks(LOW_2Y_SHARPE)/margin_bp/turnover_pct/riskNeutralized`。
  - `ERROR` → 逐 child `GET /simulations/{c}` 取 error 文本（用于定位批内毒表达式）。
- **评审门槛**（`review_wave1.py`）：`sharpe>1.58 & fitness>1.0 & two_year_sharpe>1.6 & margin>5bp & 0.05<turnover<0.30 & ra_failed_count==0`；不达标但 `sharpe>1.2` 进 near 池供增强。
- **战役级结果**：截至 `campaign_summary_2026_08_14`：20 批 / 121 表达式回测，**0 达标**；最强信号 `ml_factor_proj rank(change_6m_rating_revision) STATISTICAL d8`（sh0.85/2y2.26/margin12bp/tvr6% 但 fitness 仅 0.48）。

### 2.5 因子筛选与组合（Stage ⑧）
- **多样性量化**（`kor_diversity_review_round10.md`）：算子探索率 ≈12%（80+ 算子池仅用 10）、字段探索率极低（ml_factor_proj 333 字段仅用 15 但零竞争储备足）、模板骨架 8 种、信号风格 6 类。
- **数据集切换纪律**：模板穷尽（best<0.8 且 ≥40 表达式）+ 论坛无解 才允许切换；本战役 wave1→wave2→wave3 均符合，后续 wave 持续切换数据集（multi_source_model / model170 / acquisition_model 相继被判 dead）。
- **组合层（SuperAlpha）**：战役台账记录了 `model170_dead` / `acquisition_model_dead` 等"结构性不可修"结论；KOR SA 路线需 ≥10 合格 REGULAR 组件，当前 KOR book 0 ACTIVE → 路线封死，待 novel 信号族补齐。

### 2.6 落地应用（Stage ⑨ + 提交）
- **台账固化**：`record_p10.py` / `record_whitelist_v2.py` / `record_dayclose.py` / `record_cw_manual.py` 把每波 verdict、白名单 Tier、死路、CW（combination/跨腿）结论写回 `kor_d1_campaign_state.json`（utf-8-sig 编码，168 键）。
- **提交纪律**：REGULAR_SUBMISSION 配额 remaining 曾为 0 至 2026-08-15 → 达标 alpha 先做 `submit_ready` 验证、**不提交**；避免浪费周额度。
- **工具链冻结**（`polling_tooling_freeze`）：`kor_poll_pipeline.py` 定为战役唯一轮询入口，禁止再写临时 poll 脚本。

---

## 三、KOR 专属关键经验

1. **零竞争与高质量互斥是 KOR 第一瓶颈**：全候选池 os_is_sharpe 中位数 0.2–0.5；`model313` cov0.76 但信号弱、`other571` cov0.26；选集锁死上限 sh~1.0。数据集选择必须放首要位置（非算子调参）。
2. **双门槛破互斥**：`cov≥0.85 且 alphaCount≤50`（零竞争 + 高覆盖兼得）；优先打 `behavioral_signals`/`equity_forum_data`（三项全满）。
3. **SECTOR 是 KOR 经验默认中性化**，但论坛证据 `STATISTICAL + rank-diff` 上限更高 → 双轨对照制（STATISTICAL vs SECTOR 同批对照）。
4. **TOP600 是 KOR 唯一可用 universe**（Delay=1，无 COUNTRY 分组）。
5. **毒表达式定位法**：批内 ERROR 时逐 child 取 error，拆小批（如 batchB→batchB2）隔离定位 `6腿扩散/ts_mean10/ts_weighted_delay` 等元凶。
6. **CW（组合/跨腿）修复无效即判死**：model170 的 17+ 变体（参数/平滑/摊权/压尾/跨Category/稀释腿）全部 CW 失败 → 结构性不可修，及时放弃转蓝海字段。

---

## 四、常见陷阱（KOR 战役实证）

| 陷阱 | 后果 | 根因 | 防御 |
|---|---|---|---|
| event 类型字段套常规算子 | 24/24 ERROR，浪费 48 配额 | 未查 `get_datafields` type 列 | 表达式设计前必查 type；VECTOR/event 须 `vec_*` 聚合 |
| `ts_min/ts_max` 不可访问算子 | 整批 CANCELLED | 平台不存在 | `kor_preflight_check.py` 闸3b 拦截 |
| `quantile` 传 2 参 | Invalid number of inputs，级联 CANCEL | 仅 1 参 | 预检闸3c 计数参数 |
| MATRIX 数据集用 `vec_*` | 类型错误 | VECTOR 算子错用于 MATRIX | 预检闸3a 按 data_type 区分 |
| 单一数据集死磕 | 多批 0 达标 | 信号弱/被 arb | 模板穷尽+论坛无解才切换 |
| 达标即提交 | 浪费周额度 | 配额 remaining=0 | 先 submit_ready 验证、不提交 |
| `utf-8-sig` 编码 | json.load 默认 utf-8 报错 | 台账文件带 BOM | 用 `encoding='utf-8-sig'` 读 |

---

## 五、最佳实践

- **白名单即数据契约**：`reference/*_field_whitelist.json` 只收 COMPLETE 验证字段，表达式生成、预检、提交全链路受其约束，杜绝"未验证字段上平台"。
- **三道预检闸前移**：语法→字段白名单→类型/禁用，提交前本地全拦，避免回测配额浪费。
- **分层抽样保多样**：按骨架分桶 + 字段去重，单波覆盖多风格，最大化信息量。
- **固化唯一轮询入口**：`kor_poll_pipeline.py` 封装状态查询 + 指标拉取，禁止临时脚本，保证可复现。
- **战场记忆写回台账**：每波 verdict / 死路 / 白名单 Tier 落 `kor_d1_campaign_state.json`，跨会话延续决策（这正是本战役能跑 15+ 轮不重复的基石）。
- **零竞争优先**：`alphaCount=0` 字段族（如 ml_factor_proj `change_*`）优先于拥挤字段，PROD_CORR 风险天然低。

---

## 六、可复用优化思路

1. **数据集评分双门槛**（`cov≥0.85 & alphaCount≤50`）+ Tier 分层（三项全满→中竞争→高竞争备选），直接输出 `reference/*_whitelist.json` 供全链路消费。
2. **类型感知生成**：把 `get_datafields` type 列纳入生成约束，MATRIX/VECTOR 分流生成，从源头消除 event 盲废。
3. **算子探索率看板**：`kor_op_exploration_stats.py` 定期跑，识别盲区（ts_regression.resid / signed_power / trade_when / bucket 等未尝试），指导下一轮扩充。
4. **CW 修复失败快速判死**：同数据集多变体（≥10）仍 CW 失败 → 结构性不可修，立即转蓝海，不重复内耗。
5. **submit_ready 缓冲**：配额紧张时达标 alpha 先进 `submit_ready` 列表、不立即提交，错峰释放额度。
6. **偏好 novel 信号族**：后期 wave 转向 `recent_earnings_momentum` / `annual_price_peak` 等外推偏差、ML latent 风格，与现有 OS 池正交预期高，为将来 KOR SA（≥10 组件）铺路。

---

## 七、工具与脚本索引（tracking/KOR）

| 环节 | 脚本 | 作用 |
|---|---|---|
| 数据/字段 | `kor_scan_fields*.py` | 从平台缓存抽字段、按信号风格初筛 |
| 数据/白名单 | `record_whitelist_v2.py` | 平台实拉数据集、双门槛 Tier 分层写台账 |
| 生成/语法闸 | `batch_validate_kor.py` | alpha-expression-verifier 批量语法校验 |
| 生成/选波 | `select_wave1.py` | 按骨架分桶分层抽样，产出 waveN |
| 预检 | `kor_preflight_check.py` | 三道闸（语法/白名单/类型禁用），退出码门禁 |
| 回测/轮询 | `kor_poll_pipeline.py` | 唯一轮询入口：状态+自动拉指标/错误 |
| 指标 | `kor_fetch_metrics.py` | 直连 API 拉 alpha 全量 IS 指标 |
| 评审 | `review_wave*.py` | 按门槛排序筛选 candidates/near |
| 多样性 | `kor_op_exploration_stats.py` / `kor_diversity_review_round10.md` | 算子探索率 + 多样性量化评估 |
| 台账 | `record_p10.py` / `record_dayclose.py` / `record_cw_manual.py` | 每波 verdict/死路/CW 写回 campaign_state |
| 临时 | `_tmp_w22*.py` | 临时探针（应被固化脚本取代） |

**数据资产**：`candidates/`（18 个早期 wave + pattern_scores）、根目录 `kor_wave17V…wave34F_exprs.json`（约 120 个后期 wave 文件）、`reference/`（11 个数据集字段白名单）、`reviews/`（wave1/3/4/5 + 第10轮多样性复盘）、`kor_d1_campaign_state.json`（168 键总台账）。

---

## 八、战役现状与待解（截至 2026-08-15）

- **结果**：15+ 轮、121+ 表达式回测，**0 达标**；最强信号 fitness 卡 0.48、sharpe 上限 ~1.0（数据集瓶颈）。
- **已判死**：`acquisition_model`（event 盲废）、`model170`（CW 17+ 变体全失败）、`multi_source_model`（慢信号 TVR 结构性 3–4% < 5%）、`ai_factor_transfer`（零竞争字段全死）。
- **在飞/待验证**：`model170` 三腿批 K/L（双腿 best sh1.20/fit0.76/2y1.58）、`behavioral_signals` 蓝海（三项全满首要目标）。
- **KOR SA 路线**：封死（book 0 ACTIVE，组件不足 ≥10）；解锁需 novel 信号族补齐组件池。
- **待验证方向**：behavioral_signals 首打效果；STATISTICAL vs SECTOR 双轨对照上限；trade_when 拉 TVR 破 5% 下限；chart_cnn_alpha 1010 字段蓝海挖矿。

---

*本文档完全基于 `tracking/KOR/` 真实工程整理，覆盖数据体检→字段预检→LLM 生成→分层抽样→三道预检→固化轮询→指标评审→多样性复盘→台账固化 的端到端 KOR 因子挖掘流程，并提炼该战役实证的关键经验、陷阱、最佳实践与优化思路。*
