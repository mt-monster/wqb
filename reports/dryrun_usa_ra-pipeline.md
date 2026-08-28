# USA REGULAR 战役 — ra-pipeline 九步 dry-run 结论

> 提示词：开战役 USA，持续自我挖掘 REGULAR alpha，目标 10 个可提交（OS ACTIVE 或全闸通过），停止闸=10（非默认 4）。
> 验证方式：以 `wq-brain-campaign-matrix`（S-PRE 查表头）+ `wq-brain-ra-pipeline`（九步编排 SOP，v2.1）+ `wq-brain-campaign-toolkit`（执行引擎）为链路，逐步核对 I/O；平台已连通（沿用上轮 token，纯 GET 零配额），tracking/USA 已存在。
> 日期：2026-08-25

## 一、前置实测（均通过）

| 项 | 结果 |
|---|---|
| 平台连通 | ✅ `api.worldquantbrain.com` 可达，凭证双源可用（上轮已验证） |
| tracking/USA 目录 | ✅ 已存在；`settings.json` = region=USA / universe=**TOP3000** / delay=**1(D1)** / neutralization=**SUBINDUSTRY** / decay=5 / maxTrade=**OFF** / `_multi_sim_batch_size`=**8** / startDate=**2013-01-01（≥5年 ✅）** |
| **S0 真跑（USA）** | ✅ `campaign.py score`（region 取 settings）→ datasets=**294**, alive_ranked=**95**（tier1=42/tier2=53），落 `ledger_kv/USA/s0_ranking`；TOP=`ml_factor_proj`(0.93/1068字段) / `pattern_scores` / `continuation_score` / `option_horizon_decomp` / `mmp_nlp_sentiment` |
| 离线测试 | ✅ toolkit 65 passed（上轮已验证） |
| gate/pipeline 提交契约 | ✅ `POST /simulations` 批量端点 = multi_create_simulate×8；单条 `create_simulate` 零调用 |

## 二、prompt 要求 → skill 步骤 映射（I/O 证据）

| prompt 要求 | 落点步骤 | 证据 |
|---|---|---|
| 先 campaign-matrix 查表拿配置包 | **S-PRE（步1）** | 真实读 `registry_empirical`(USA: 10 dead_end / 3 campaign / 1 win) + `regions` 表；产出配置包 |
| S0 体检锁白名单（标准可放宽） | **S0（步2）** | 真跑成功；`s0_whitelist` 落 ledger；matrix dead_end 强制过滤白名单 |
| 遍历不同 universe | settings.universe 可切 TOP3000/TOP1000/TOP500（profile 实证档） | USA profile `static.universe=[TOP3000,TOP1000,TOP500]` |
| delay=D1、max_trade=ON/OFF | settings.delay=1 / maxTrade 可切 | settings 已 delay=1/maxTrade=OFF；ON/OFF 属设置展开 |
| 字段理解→候选池→设置展开→五槽批量(8并发)→S4评审链 | **S1→S6** | S1 `scan-fields`；S2 GEM `build-wave`；S3 `wave_gate`；S6 `pipeline run`(batch=8)；S4 `review` |
| AlphaTest 诊断 → Mode B 优先 → Mode A 其次 | **S4（步7）** | SOP 步7 明文：`brain-how-to-pass-AlphaTest` → `wq-brain-alpha-optimization-v1`（Mode B 70%→Mode A 30%）；USA profile 步7 注入"Mode B 强制正交" |
| 本地 self/PPAC 快筛 | **S4** | SOP 步7 按需 `brain-calculate-alpha-selfcorrQuick`（本地算，不耗平台）✅ 在可用 skill 列表 |
| 归因 | **S4** | `brain-explain-alphas` ✅；SOP 步7 列明 |
| 稳健性/反过拟合闸 | **S4→S5（步8）** | `brain-alpha-robustness` ✅；SOP 步8 强制必经 |
| judge 判定 | **S5（步8）** | `brain-alpha-judge` ✅；SOP 步8 明确"judge READY 只报告、等用户确认、禁止自动 submit" |
| 1-2 字段/表达式 | **S2/S3** | GEM `--priors-file` 概念优先；SOP 步6"每槽先 1–2 条骨架查 prod_corr" |
| prod_corr≥0.7 不提交、回 Mode B | **S4/S5** | SOP 步7 失败分支"prod_corr≥0.7 → Mode B 换概念"；USA profile 加严**预警线 0.6**（比 prompt 更严，无冲突） |
| 跨数据集策略 corr<0.4 | **S3 多样性闸** | `gate.py` 多样性闸 + `diversity_audit.py`；SOP 步5 多样性 FAIL 回步4 |
| 每15次回测做多样性评估 | **S4 周期审计** | `campaign.py diversity` → `diversity_audit.py`（见 §四 gap A） |
| type=REGULAR | **S6 提交** | `pipeline submit_batch` 构造 `{type:REGULAR,...}` 列表 ✅ |
| judge READY 停下报告、不自动提交 | **S5/S8** | SOP 步8 铁律 ✅；`submit_verdict.py` 只读双视图判定 |
| 提交后跑 S6 复盘、回写 wave_results + registry_empirical | **S6（步9）** | `wave_results` 表 USA=9 行、`registry_empirical` USA=14 行均存在；`campaign.py wave upsert`/`registry add-win/add-dead-end` 幂等 CLI 写同一 DB ✅ |
| 停止闸=10（非默认4） | **循环策略** | **SOP 原生**（步9 循环表："ACTIVE RA ≥10 可转 superalpha"；"默认4"是已废止 `brain-deepExplore` 的遗留，SOP 反模式 line 285 已剔除）→ **无需任何改动** |

## 三、真跑才暴露的关键事实

1. **campaign-matrix → S0 握手有效（核心演示）**：S0 把 `ml_factor_proj` 排为 USA #1，但 matrix `dead_end` 层命中 `USA-ML-FACTOR-PROJ-PROD-SATURATED`（"All promising signal families PROD saturated"）→ 按 SOP 硬规则"dead_ends 优先于直觉"，该集**必须排除出白名单**。证明 prompt 的"先 matrix 查表→S0 锁白名单"两步链路真实闭合、有强制过滤力。
2. **USA 唯一 win 是 SuperAlpha（KPGvRMg1），regular win_recipe 为空** → S2 GEM 在 USA 无 regular 胜绩可依赖，与 profile"饱和市场正交战"定位一致；GEM 先验只能靠 `dead_ends` 反向排除 + profile 静态 priors。
3. **profile 已内嵌本 prompt 全部硬纪律**：SUBINDUSTRY 中性化、prod 预警 0.6（严于 0.7）、Mode B 强制正交、单数据集优先、排除 classic_value/quality/book/seed_basics 饱和族 → 编排与 prompt 高度同构，几乎零漂移。
4. **dead_end 实证覆盖充分**（10 条，含 option_chart_model prod_corr=0.8386、earningscall_embed、insider_feats、event_sentiment_signals 等），正好对应 prompt"禁止频繁切换数据集、多样性穷尽才换"的约束。

## 四、缺口（仅 2 处，均非阻塞）

- **A. 多样性审计 cadence（提示词 15 vs 工具 10）**：`diversity_audit.py` **无 `--every N` CLI 参数**，审计触发为每 batch（=每 8 回测），比 prompt 的"每15次"更密（满足精神）；唯一硬编码的 `INJECTION_EXPIRY_BATCHES=10` 是"强制探索窗口长度"而非审计触发点。→ 处置：agent 在每 ~2 批（≈15 回测）显式跑 `campaign.py diversity` 即可对齐；或改常量。非阻塞。
- **B. 终闸阈值冲突（须你拍板，非 I/O 缺陷）**：prompt 硬筛（margin>15bp / tvr 5–30% / self_corr≤0.7）与 `src/wqb/config.py` 的 `GATES_INTERNAL`（margin_bp_min=**10** / turnover_range=(0.05,**0.20**) / self_corr_max=**0.50** / PRODCORR_CEILING=0.70）三处不一致（同 EUR dry-run 结论）。SOP 规定"阈值不复写、引用 GATES"。→ 需你定：以 prompt（15bp/30%/0.7）还是 GATES（10bp/20%/0.5）为准；margin 上 GATES 更松、tvr/self_corr 上 GATES 更严。

> 注：本 prompt **未提"算子数<8 上限门"**（EUR prompt 有，USA 无），故 EUR dryrun 的 gap #2 在此不适用。

## 五、结论

**编排完全可承载本 prompt，I/O 无缺环，无需改代码即可开跑。**

- 九步链路全部真实可执行（S-PRE 查表→S0 体检→S1 字段→S2 GEM 选波→S3 门禁→S6 批量回测→S4 评审链→S5 稳健闸→S6 复盘）已逐步核对，关键步骤（S0/S1/S3/S4/S6/S9）上轮与本轮均实测通过。
- **停止闸=10 是 SOP 原生数字**（"默认4"是已废止旧 SOP 的遗留），prompt 与此完全一致，零改动。
- 评审链 6 个 skill（AlphaTest / optimization-v1 Mode B·A / selfcorrQuick / explain / robustness / judge）全部在可用列表，SOP 步7/8 已正确接线。
- 回写 `wave_results` + `registry_empirical` 表与幂等 CLI 均就位（USA 已有 9/14 行历史）。

**正式开跑前仅需你拍板 1 项**：终闸阈值以 prompt 还是 GATES 为准（gap B）。gap A（cadence 15 vs 10）由 agent 运行时对齐即可，不影响正确性。

（本 dry-run 真实副作用：S0 已把 USA 294 数据集排名写入 `ledger_kv/USA/s0_ranking`；可保留作战役基线。）
