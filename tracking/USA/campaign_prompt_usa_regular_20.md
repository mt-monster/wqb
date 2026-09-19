# USA REGULAR 20 颗挖掘战役 · 完整执行提示词（v2，2026-09-17 校准版）

> 本版对照 v1 做了三类修正：**① 接口/参数纠错**（原文有 4 处调用会直接失败）、
> **② 消除自相矛盾**（原文硬约束 #5 与 #6 互斥）、**③ 补齐编排优化后新接入的三道闸**。
> 详细对照见 §8。本提示词可整段粘贴进新会话直接执行。

---

## 0. 适用前提（先确认，不满足就地停）

- 工作区 `D:\coding\traeCN_project\wqb`；`main` 分支；遵循 `AGENTS.md`。
- 凭据三级链 `~/.brain_credentials` → `~/.brain_mcp_config.json` → 项目 `.env`。**禁止读取/打印/入库凭据**。
- MCP：本会话若已连 `mcp__wq-brain-http__*` 与 `mcp__wqb-db__*` 则优先用；未连则退回
  `$WQ_PY` + toolkit CLI（`$WQ_TOOLKIT_DIR` = `Claude/skills/wq-brain-campaign-toolkit/scripts`）。
  **不要为绕开 MCP 写临时脚本**；网络调用一律走 MCP venv 的 `BrainApiClient`（自带 429 退避），禁止手写 requests。
- ★ **改了 skill 必须同步**：`python tools/sync_skills.py`。解析顺序实测为
  `~/.claude/skills` > `~/.codex/skills` > `~/.qoder-cn/skills` > `~/.cursor/skills` > `~/.workbuddy/skills`
  > 仓库 `Claude/skills`（**仓库副本优先级最低**）→ 不同步则运行时仍读旧副本。
- ★ **纪律：任何闸门/口径的"是否生效"必须直接 import 调用被测函数核验，不得只读文档或只读 SQL。**
  本项目已多次因此得出相反结论。

---

## 1. 目标口径与停止闸

**目标**：产出 20 颗本次任务新挖掘的「过闸待提交」USA REGULAR alpha。

**「过闸」= 同时满足 4 条（全部可判定）**：

1. **Failed-count 资格门**：WebDataScope `Failed RA == 0`（WARNING/ERROR 也计数，比只看 `result=="FAIL"` 严格）。
   规则见 `Claude/skills/wq-brain-ra-pipeline/references/webdatascope-failed-gates.md`。
2. **提交层判定**：`tools/submit_verdict.py` 模拟层 checks 无 FAIL 且 `GET /alphas/{id}/submit` 返回 200。
3. **相关性双闸**：SELF < 0.7 且 PROD < 0.7（提交前 `refresh=True` 零成本重测）。
4. **隐形第四闸前置**：IS 阶段无 `CONCENTRATED_WEIGHT` WARNING（该闸 IS 只 WARNING、提交后才 403 且**无法预检** → 见即弃）。

**停止闸**：过闸计数 = 20 → 立即停止挖掘。

**挖掘与提交解耦**：提交受 REGULAR **4 颗/ET 日历日**限制（00:00 ET = **12:00 GMT+8** 重置），
20 颗真实提交需 ≥5 个 ET 日。**配额满时挂起提交、继续跑步 2→步 9**，提交慢不得拖停挖掘。

---

## 2. Phase 0｜全链路 dry-run 校准（先跑通，再铺量）

Phase 0 全程**不提交任何 alpha、不消耗提交配额**。

### P0.1 引擎 dry-run（零副作用）

- 对全部 **18 个 workflow 节点**各跑一次 `dry_run=True`（节点清单以 `workflow_list_nodes` / `registry.py` 为准，
  当前为：`auto_harvest auto_pyramid auto_review batch_track campaign feature_engineering field_understanding
  gem gem_wave hypothesis_round inventory_scan judge step_metrics structural_reconstruct submit_alpha
  superalpha unified_gate wave_gate`）。
- 验收：`dry_run=True` 时**零 brain 调用 / 零 subprocess / 零写库**；节点失败必须带得出 `error`
  （禁止 `success=False` + `error=None`）。
- 任一节点违反 → **阻断**，先修再进 P0.2。

### P0.2 三道开波闸 + CLI 干跑看 gate 通过率

```bash
CD=tracking/USA

# ① 体检包前置检查（缺包则步 5 体检硬门不生效）
ls tracking/mining/field_inspect_usa_*.json | wc -l     # USA 现有 104 个；白名单集缺失的按 ③ 生成

# ② S0 校准 = 2 步必需 + 1 步可选（不是三次重复！）
#    ①′ 可选：只预览不写盘（仅新区/校准结果可疑时做）
#    ①  必需：calibrate 反学 category 权重 + 拥挤甜区，写回 thresholds.json（此步不产出排名）
#    ②  必需：裸 score 按新阈值打分，产出 s0_ranking
#    ⚠ score 子命令【没有 --region】（region 由 --campaign-dir 派生）——写 --region 会 argparse 报错
python $WQ_TOOLKIT_DIR/score_datasets.py --campaign-dir $CD --calibrate --dry-run
python $WQ_TOOLKIT_DIR/score_datasets.py --campaign-dir $CD --calibrate
python $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD score --dry-run      # 人工审后去掉 --dry-run

# ③ 缺体检包则生成（纯离线：只读本地 WebData ZIP，不发平台请求、不耗配额、无 429）
python tools/gen_field_inspect_packs.py --all --dry-run
python tools/gen_field_inspect_packs.py --region USA --delay 1

# ④ 端到端干跑看 gate 通过率
#    ⚠ pipeline 有【位置子命令】run/quota：必须写 `pipeline run`，直接 `pipeline --dataset` 会报
#      invalid choice（曾把 --dataset 的值当成子命令名）
python $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD pipeline run --dataset $DS --wave $W --dry-run
```

- dry-run 后人工审两处**校准异常**：甜区 `ac` 异常巨大（如 MEA 8560–21508 = 反向奖励超拥挤）/ `strong_acs` 空（无强信号）。
- **调 `mcp__wqb-db__get_ledger_key region=USA key=s0_ranking` 校验**：10 区有非空 `ranking[]`；USA 应有 294 条左右。

### P0.3 极小样本实跑探针（真平台）

- 每数据集 **≤8 探针**（USA profile `loop_policy.fast_kill`：「新数据集 8 探针无 `|S|≥0.5` 即判死」）。
- 注意区分两个不同维度的"探针上限"：`fast_kill` 是**单数据集累计 8 条**；USA `max_probes_per_wave: 1` 是
  **七槽里弱探针最多占 1 槽**。二者同时生效，不要混为一谈。
- 量化产出（**必须给数**）：每数据集「回测条数 → 过闸数」真实转化率、单条平均耗时、七槽吞吐（条/小时）。

**放大闸**

- 转化率 > 0 → 进 Phase 1，按 `20 ÷ 转化率` 反推所需回测规模。
- 转化率 = 0 → 回 S1/S2 换字段组合或模板，**最多迭代 3 轮**；仍为 0 才换数据集。
  遵守「**每轮验证 >10 种不同结构（变体/字段组合/模板/信号构建方式）后仍无效果，才转向**」纪律，
  不得只测 1–2 个字段就断言"信号方向无解"。
- **禁止在转化率未知时直接铺量。**

---

## 3. Phase 1｜规模化挖掘 S-PRE → S6（九步 + USA 注入）

任一步 FAIL 就地回退，不许跳过。**profile 与骨架冲突时 profile 优先**。

### 步 1（S-PRE）查表 —— USA 特化

1. 读 `Claude/skills/wq-brain-ra-pipeline/references/regions/USA.md`（`entry_verdict: active`）。
   USA 静态档：**universe TOP3000 / delay 1 / 中性化 SUBINDUSTRY**（`_alt_neutralization: SECTOR` 作 A/B 对照轨）；
   实际以 `tracking/USA/config/settings.json` 为准（含 `decay 5` / `truncation 0.08` / `_multi_sim_batch_size 8`）。
2. **算子审计 ghost-op guard（强制）**：`python tools/campaign_intel.py ghost-audit --region USA --delay 1`
   （底层 `wqb.expression.operator_audit` + `data/operators_verified.json`，当前 verified=103）。幽灵算子批次直接拒绝。
3. **PPA 主题门（强制）**：`get_messages(limit=30)` 扫 `type=="ANNOUNCEMENT"`、标题含 "Power Pool"，
   解析当期 region/delay/universe；USA 不匹配则标 `YELLOW + WAIT_THEME_ROTATION`（**RA 常规提交不受主题限制**）。
4. **跨区铁律逐条核对**（USA 升强制）：每条铁律标注「本波是否触碰」，触碰项必须给规避方案。
5. 查表：`get_campaign_summary` / `get_dead_ends` / `get_dead_datasets` / `get_cross_region_lessons`
   + `campaign.py registry list`。
6. USA 专属第 6 条：`search_alphas_by_sharpe(USA, min_sharpe=1.58)`，某族已达标 alpha ≥10 且风格同质
   → 标 `prod_saturation: likely`，该族硬排除。

- **产物**：universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号 → 写 `settings.json`。

### 步 2（S0）数据集体检 + 锁白名单（放宽档 + 补偿）

**放宽档（本次授权）**：`coverage ≥ 0.6` / `alphaCount ≤ 1500` / `fieldCount ≥ 10`。

**补偿三件套（因 alphaCount 50→1500 放松 30 倍，必须执行）**：

1. **字段级拥挤度分级**（用 `get_datafields` 的 `users`）：`users ≥ 50` 只做信号方向验证不投入打磨（prod_corr 必超）；
   `users 10–49` 进池但提交前必实测；`users 0–9` 优先，且**冷门字段占批次预算 ≥50%**。
2. **已知饱和族直接排除**：`techindi_model predicted_first_quantile_ten_day_return_*`（已穷尽）、USA emotion 系、
   anl15 8 条精确表达式（**sha1 精确比对，不用前缀通配**）。
3. **读历史饱和账**：查 ledger `submit_ready_blocked`，命中过 prod 饱和的数据集/信号族按拥挤降优先级（即使 alphaCount 达标）。

**选型偏好**：Other / Risk / ShortInterest 等**未点亮**类别优先（但须先过三件套）。
USA profile green = `option9 / analyst 细分集 / news 高级情绪集 / event·earnings 集`；
profile red = `pv1 / mdl177`（exhausted，seed basics 全族死）。实测不达标则回退 green 名单。

**其余硬约束照旧**：白名单至少 2 个非 MODEL；`category_weight` 限 0.9–1.15（禁 1.3 vs 0.7 抹掉整座金字塔）；
`*_dead` 仍排除（主导腿禁用 ≠ 整集判死）；白名单外禁止 generate / simulate。

**★ 三道开波闸已存在且默认启用，不要重复"建议新增"**（挂在 S2/S3，`dry-run` 也走）：

| 闸 | 默认阈值 | 缺配置行为 |
|---|---|---|
| `signal_floor` 信号天花板 | 最近 `min_batches=2` 波 `max\|sharpe\| < max_sharpe_floor` 即拦；**USA = 0.9**（实证回填）/ 全局 0.5 | **fail-closed**：回落默认继续判定 + warning；**仅显式 `enabled:false` 才放行** |
| `backlog_gate` 积压闸 | `conversion_min=0.10`、`pending_gated_ratio_max=0.30`、`unconsumed_ratio_max=0.30`、`min_expressions=200` | 默认 enabled=True |
| `stop_rules` 停止闸 | `yield_min_backtests=100`、`consecutive_fail_waves=3`、`sharpe_min=1.58`、`fitness_min=1.0` | 默认 enabled=True |

- 阈值节位置唯一权威 = `tracking/<REGION>/config/thresholds.json` 的 `diversity.{signal_floor,backlog_gate,stop_rules}`。
- 灰度控制：`--gate-mode {off,warn,enforce}` 或环境变量 `WQB_GATE_MODE`（**warn = 灰度默认放行，enforce = fail-closed**）。
- ★ 报数前**直接调用**核验现状：`python logs/_tmp_gate_probe.py`。
  USA 实测（2026-09-17）：`conversion=8.8% (312/3549)`、`unconsumed=3197/3549 (90%)` → **拦截**（灰度下打 `[灰度·未拦截]` 告警）。

- 锁白名单后必须 `upsert_ledger_key(region="USA", key="s0_whitelist", {...})`。
  规范化键形：`{"datasets": [...], "universe": "...", "delay": 1, "entries": [...], "_schema_from": ...}`
  （读取统一走 `wqb.ledger_whitelist.normalize`，勿再假设只有 `candidates`/`whitelist` 一种形态）。

### 步 3（S1）字段扫描 + 理解

- `python $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD scan-fields --dataset $DS`（**typed catalog 必做**）；
  VECTOR 比例用 `get_datafields` 确认（步 4 必须传对 `--data-type`）。
- ★ **字段理解走 `brain-data-feature-engineering`，但按需 / 仅人读参考 / 禁注入 GEM**：
  该节点产出是**确定性模板渲染**（8 问框架 + `rank(ts_mean({f},66))`），**不含 LLM 推理**。
  注入 GEM 会让 GEM 一行 LLM 都不调、整波退化为模板展开（GBR `intraday_pv_feats` 实证）。
  ideas 回写 `s1_<ds>_d<delay>`（`source=standalone`）仅供人读。
- **预处理决策：区分初始信号 vs 进阶信号**
  - **初始信号**（裸字段/一阶）→ 重预处理：`cr<0.4` 必须 `ts_backfill`；`|skew|>2` 必须 `rank`/`winsorize`/`signed_power`；
    `kurt>8` 必须 `rank`/`winsorize`；单边恒正/负不可直接用原始水平；稀疏事件（`zero_inflated`/`point_mass`）必须 `trade_when`。
  - **进阶信号**（group 残差 / bucket 中性化后的二阶）→ 预处理已在上游完成，重点转 `group_*` 与 bucket 自定义分组；
    **避免重复平滑导致信号衰减**。
- **失败分支**：字段数 < 10 → 退回步 2。

### 步 4（S2）概念优先生成

- **生成器强制 GEM**（`brain-make-some-gem` 的 headless runner），**禁止「每字段套 rank」**。
- **强制 `assemble-priors`（确定性 CLI，DB 单一事实源）**：

  ```bash
  python $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD assemble-priors --snapshot-ledger
  ```
  ⚠ 参数名是 **`--snapshot-ledger`**（不是 `--snapshot`）；另有 `--print` / `--sha-only` / `--restore`。
  priors 只消费 `wins`(≤6) 与 `dead_ends`(≤12)。
  ★ 键口径：**真实 payload 键是小写** `priors_snapshot_<region>`（`ctx.prefix == region.lower()`，GEM 两个消费点都读小写）；
  大写 `assemble_priors_cache_<REGION>` 是 campaign 节点的**缓存标记**（不含 wins/dead_ends），勿混用。
- **USA 注入**：anl15 封禁的精确表达式进生成黑名单（**sha1 比对，非前缀通配**）；emotion 系全排除。
- **七槽配给**（Token-Bucket C≈7；USA `_multi_sim_batch_size=8`）：≥2 跨金字塔 / ≥1 win 换腿 /
  **弱探针最多 1 槽**（已有近闸字段时为 0）。禁止七槽纯 MODEL、禁止七槽裸探针。
- **窗口白名单**：只用 `1/5/22/66/252/504/1008/1260`；其他窗口必须给明确解释或实测证据。
- ★★ **信号构造形态（本轮最重要修正，见 §8-②）**：
  **禁止任何加权混合**——`add(A,B)`、`0.4*rank(A)+0.6*rank(B)`、`add(multiply(0.4,A),multiply(0.6,B))`
  **两种写法都会被 gate 闸5 硬 block**（毒模式 `weighted_signal_mix` / `weighted_leg_mix_func_prefix|suffix`）。
  跨腿组合**只能走 5 类结构交互**：

  | # | 形态 | 例 |
  |---|---|---|
  | ① | `ts_corr` 共振腿 | `ts_corr(rank(慢), rank(快), 20)` |
  | ② | `divide` 比值/价差 | `divide(rank(A), rank(B))` |
  | ③ | `subtract` 排序差 | `subtract(rank(A), rank(B))` |
  | ④ | 条件门控 | `if_else(rank(快)>0.5, ..., ...)` / `trade_when(事件, 腿, -1)` |
  | ⑤ | 分组 | `group_zscore(A, sector)` / `group_rank(A, subindustry)` |

  或走 SuperAlpha combo（步 8）。**不允许**用调权重/增删腿数的方式修不达标的信号。
  ⚠ 历史 EUR win「0.4 慢 MODEL 残差 + 0.6 快 PV」的**加权形态已废止**，
  可继承的只有其**跨数据集补腿意图**，落地必须改写成上表结构交互。
- **点塔策略**：USA 多点位未亮。**优先选 3–4 座塔各打 3–5 颗**（每塔 3 颗点亮），避免摊薄到 10+ 塔。
  塔位状态须**运行时取**：`recommend_datasets(region="USA", delay=1, universe="TOP3000", top_n=20)`
  （它用 pyramid-alphas / pyramid-multipliers 端点给未点亮塔优先），**不要在提示词里硬编码塔数**。
- `build-wave --from-db --dataset $DS --wave $W`。
  ★ `--wave` 全链路为**字符串**（支持 `97` 与 `s2_xxx_d1` 两种形态）。
  ★ **波号禁止用裸 Unix 时间戳**（`time.time()` 顶替）——已发过 20 行此类脏数据（DEU）。
  契约：`src/wqb/wave_id.py`；写入侧护栏在 `tools/mcp_batch_writer.py::_normalize_wave`；
  存量修法 `python tools/normalize_wave_ids.py`（dry-run 默认）。
- ★★ **USA 开波须用 `--gate-mode enforce`**（2026-09-17 实测）：
  USA 区域级信号天花板已触发——最近 2 批 max|sharpe| = **0.88 < signal_floor 0.9**
  （`tracking/USA/config/thresholds.json`），且近 7 天 582 次回测 **0 达标**
  （sharpe 48% 为负、fitness 无一 ≥1.0）。region-gates 默认 `warn` 只告警不阻断，
  会导致继续烧槽位；USA 必须显式 `--gate-mode enforce`（或 `WQB_GATE_MODE=enforce`），
  让 signal_floor 真正拦住新波。要放行须写台账
  `mcp__wqb-db__upsert_ledger_key(region='USA', key='stop_rules_override', value={'reason': '...'})` 留痕。
- **未验证 DB 有表达式，不得声称步 4 成功**。

### 步 5（S2→S3）门禁（双硬门，回测前必过）

1. **多样性守卫（唯一执行口径 = toolkit `gate.py:check_batch_diversity`，即闸6）**：由 `wave_gate.py` 自动调用。判据三源：
   ① **自学习契约** `explore_contract`（`rules.get_active_contract`；`repair` 类默认豁免；**契约过期 FAIL-CLOSED** 并自动续约）；
   ② **收益来源多样性**（读 DB idea ledger 的 `expected_exposure`：同批 >60% 共享同一 exposure 且字段族相同 → FAIL；
   无 exposure 元信息 → WARN 不阻断）；
   ③ **家族天花板预检**（主导腿信号族占比 ≥2/3 → WARN，wave94/95/98/104 实证 SELF≥0.9 必死）。
   ⚠ **不要再把 `wqb.expression.validator.check_batch` 当判据**：它只实现 **4** 条形状闸
   （`shape_signatures`/`outer_wrappers`/`group_vars`/`windows` 各 ≥2），**全仓零调用方**，与上述执行口径判据不同。
   它现在只作**方法论参考**（形状维度自检），不构成门禁。
2. **体检硬门 `check_expr_against_inspect`（5 条）**：见步 3 预处理规则，任一 `ok=False` 拒绝。
   ★ **前置：白名单数据集须有体检包** `tracking/mining/field_inspect_usa_<dataset>.json`。
   缺包时本闸**不生效**（约束裸奔到仿真）——步 2 的 P0.2-①③ 已把它列为开区硬前置。
   缺包行为可切换：`tools/wave_gate.py --inspect-mode {off,warn,enforce}`
   （或 `WQB_INSPECT_MODE`；节点 `wave_gate` 同名参数透传）。**`enforce` = 缺包即整波 fail-closed**，
   开新数据集建议用 enforce。实测无包时：`warn`→EXIT 0 PASS、`enforce`→EXIT 1 FAIL。
   另注：**本地 WebData ZIP 只覆盖 ASI/CHN/EUR/GLB/JPN/KOR/USA 七区**——USA 在覆盖内，可正常生成。
3. **一键门禁**：

   ```bash
   python tools/wave_gate.py --campaign-dir $CD --dataset $DS --wave $W --from-db        # VECTOR 用 --fix
   ```

- **流程**：`check_batch → check_expr_against_inspect → wave_gate → 步 6 create_multi_simulation`。
- **失败**：语法 FAIL 先修；多样性 FAIL 回步 4 补骨架（可查 `KB/community_tpl_kb` 按 category 换腿）。

### 步 6（S3）七槽回测

- 七槽（Token-Bucket C≈7），**`create_multi_simulation`**（≥2 条/批，USA 批大小 8），即收即补保持槽位常满。
  ⚠ 工具名是 **`create_multi_simulation`**（不是 `multi_create_simulate`）。
- **prod-first（USA 命门，省算力最多的一招）**：每槽先 1–2 条骨架查 `prod_corr`。
  ★ **USA 预警线是 0.6（不是全局 0.7）** —— profile `gate_overrides.prod_corr_early_warn: 0.6`，
  USA 的 0.6→0.7 区间几乎必然继续恶化，**≥0.6 即停扩换腿**。
- **USA 注入**：新信号族首波 `delay=1`，次波探 `delay=0` 对照；设置差异单独成批。
- 空槽补**组合批**，不用裸探针凑数；**断点续跑 checkpoint 必做**。
- **积压清理（每波末）** —— 口径已更新（见 §8-③）：

  ```sql
  SELECT status, COUNT(*) FROM expressions WHERE region='USA' GROUP BY status;
  ```
  新口径 **`unconsumed = gem + selected + pending + gated`**（旧口径只算 `pending+gated`，漏计 `gem`/`selected`）。
  判定：`unconsumed / total > 0.30` 或 `conversion = backtested/total < 0.10` 即 **S2→S3 断链**，
  优先把近闸积压纳入下一波，不再开新波。
  ★ 该判定**已有自动闸**（`_run_backlog_gate`，挂 S2/S3 且 dry-run 也走），无需自己重写 SQL 判断；
  上面的 SQL 只用于人工复核。想要硬拦就加 `--gate-mode enforce`。
- **批次故障协议**：8 子模拟全 ERROR → 重发同表达式；`CROWDING` 连续 2 次全 ERROR → 跳过该中性化；
  fatal operator 级联 CANCEL → 隔离到独立小批；瞬态 "try again" → 拆 5 条/批；429 → 指数退避；
  "took too much resource" → 去 backfill 或缩短窗口。

### 步 7（S4）诊断改进

- `python $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD review --dataset $DS --wave $W`。
- **Mode B（想法层 70%）优先 → Mode A（参数层 30%）**。
- 本地快筛 `brain-calculate-alpha-selfcorr-quick`（self / PPAC）→ 归因（`brain-explain-alphas`）
  → `brain-alpha-robustness` 反过拟合四查。
- **失败分支**：`prod_corr ≥ 0.7`（USA ≥0.6）→ Mode B 换概念；
  同一想法 **>10 种不同结构**仍不过 → 步 9 记 `dead_end` 回步 2。

### 步 8（S4→S5）稳健闸与提交判定（两层链）

1. **Failed-count 资格门**：`is.checks` 算 WebDataScope failed counts，REGULAR 要求 `Failed RA == 0`
   （WARNING/ERROR 也计数）；非零 → 回步 7，不进提交。
2. **`submit_verdict` 零成本判定（唯一权威）**：`tools/submit_verdict.py` 模拟层 checks + `GET /alphas/{id}/submit`
   双视图；无 FAIL 且提交层 200 = READY。
   ★★ **提交层阈值严于 IS 层，禁用 IS 层 checks 推断可提交性**：`_SUBMIT_HARD_GATE_WARNINGS = {LOW_FITNESS,
   LOW_SHARPE, LOW_2Y_SHARPE}` —— 这些在 IS 视图只显示 WARNING，**提交层直接 FAIL**
   （提交层限：`LOW_SHARPE 1.58` / `LOW_FITNESS 1.0` / `LOW_2Y_SHARPE 1.58`）。
   ★ `GET /alphas/{id}/submit` 返回 **404 不代表可提交**；**唯一可靠的提交层预检 = 直接 `POST /alphas/{id}/submit`**
   —— 失败即**同步 403 = 零成本**（不扣配额），且回带全部提交层 checks。
   ★ `POST` 同步 403 也是**读配额真值**的可靠手段（看 `REGULAR_SUBMISSION` 的 `limit/value`）。
   ★ 每候选**只发 1 次 submit**；201 后只轮询（4 分钟仍 `UNSUBMITTED` 再补发）。
3. **参考核对（可选，不产出决策）**：PPA 主题匹配 / 相关性门控 / 点塔优选。
   `workflow_judge` 是**参考评审层**（`brain-alpha-judge` 同），**不是提交权威且不执行提交**。
   其返回 `verdict`(READY/REVIEW/BLOCK) **只是摘要**，请优先读 `checklist`（逐闸事实）与 `degraded_gates`；
   **`degraded_gates` 非空 ⇒ verdict 不可作提交依据**（降级闸此前会静默凑出 READY）。
- **READY 只报告、等用户确认**；确认前**禁止** `submit_alpha` / `submit_batch.py`。
- IS 阶段出现 `CONCENTRATED_WEIGHT` WARNING → **直接不提**（提交后必 403 且无法预检）。
  ★ 修法是**表达式结构层的时间平滑**（`ts_mean(事件计数字段, 10)` / `ts_decay_linear`），
  **不是调参数**（实测换 neutralization 四档、truncation 0.08→0.01 均无效；末端再套 `rank` 反而更差）。
  USA profile `gate_overrides.cw_gate: WARN`，但**操作纪律按"见即弃"执行**（因为提交层无法预检）。

### 步 9（S6）复盘回写（**未回写视为本波未完成**）

**开步先看漏斗**（`tools/step_funnel.py`，只读推导，数据源=既有 4 表 + ledger，不建表不写库）：

```bash
python tools/step_funnel.py --region USA              # 定位"这一波在哪一跳掉得最狠"
python tools/step_funnel.py --region USA --json       # 机器可读
```

> ★ 五张 `step_*_metrics` / `wave_summary` / `campaign_summary` 表**恒 0 行且不应填充**
> （评估结论：自动采集是 TODO 空壳、质量指标可从既有表推导、增益指标是反事实估算无客观来源）。
> **要步级视图就用 `step_funnel.py`，不要往那五张表写。**
> ⚠ 漏斗口径局限：各步取各自表存量，时间窗不一 → 链上数值可能不单调，仅用于定位瓶颈。

```bash
# wave upsert：无 --extra；补充信息用可重复的 --finding，或用 --candidates @file.json
python $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD wave upsert \
  --wave $W --verdict <PASS|FAIL|PARTIAL> --status closed \
  --finding "本波要点1" --finding "本波要点2"

# registry 写实证：--id/--family/--reason/--rule 是【必填】，只给 --extra 会 argparse 报错
python $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD registry add-dead-end \
  --id <dataset_id> --family <signal_family> --reason "<vs:PROD_CORRELATION>" --rule "<一句话死因规则>" \
  --extra @dead.json
python $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD registry add-win \
  --id <alpha_id> --what "<胜绩摘要>" --key <registry_key> --extra @win.json

# ledger 写波结论：签名是 `set-verdict [--json JSON] <wave>`（wave 是位置参数）
python $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD ledger set-verdict \
  --json '{"verdict":"PASS"}' $W
```

> ★ 以上三个子命令都支持 `--dry-run`（先校验再落库），首次用建议先加。

- OS ACTIVE / 全闸 PASS 必须 `add-win`（记录 mix 比例、中性化、decay、快/慢腿）。
- **prod 饱和反馈 S0**：本波全被 `prod_corr ≥ 0.7`（USA 0.6）卡死 → 除 `add-dead-end` 外，
  在 ledger `submit_ready_blocked` 追加饱和记录 → 下一轮步 2 把该数据集按拥挤处理。
- **USA 注入（死路外溢评估）**：判死族是否跨区普适？是 → `upsert_registry_empirical(region="GLOBAL",
  layer="cross_region", ...)`，其他区 S-PRE 自动读到。
- ★ `wave_results.verdict` 必须是干净枚举（PASS/FAIL/PARTIAL）。**空 verdict 会静默关闭停止闸规则 B**
  （`all(v=="FAIL")` 因 `str(None or "")==""` 恒 False）——属**假安全**，务必写入真实结论。

---

## 4. 硬约束（可判定清单）

| # | 约束 | 判定 |
|---|---|---|
| 1 | 每条表达式只用 1–2 个 dataset 的字段（catalog 内可多字段组合，不强制） | 不频繁切换数据集，除非无计可施 |
| 2 | `prod_corr ≥ 0.7`（**USA 预警 0.6**）一律不提交 | 回 Mode B 换字段组合；提交前 `refresh=True` 零成本重测 |
| 3 | 不同数据集策略间相关性 < 0.5 | `brain-calculate-alpha-selfcorr-quick` 本地实测判定 |
| 4 | 多样性（算子/字段/骨架/预处理/收益来源/失败风险六维） | = 步 5 `gate.py:check_batch_diversity` 闸6，FAIL 不进回测 |
| 5 | **组合形态：只用 5 类结构交互，禁一切加权混合** | 闸5 正则硬拦（`weighted_signal_mix` / `weighted_leg_mix_func_*`）；跨腿用 `ts_corr`/`divide`/`subtract(rank,rank)`/`if_else`·`trade_when`/`group_*` |
| 6 | 禁止清单 | `add(A,B)` 及任何加权混合 / emotion 系 / anl15 精确表达式 / 手写 requests / 跳过步 9 / READY 后自动提交 |
| 7 | 波号必须为字符串且**非裸时间戳** | `--wave` 支持 `97` 与 `s2_xxx_d1`；契约 `src/wqb/wave_id.py` |
| 8 | 缺体检包不得静默通过 | 步 2 先补包；否则显式 `--inspect-mode warn` 并在台账记因 |

---

## 5. 提交纪律

- type = **REGULAR**。
- `submit_verdict` 判 READY → **停下来报告，等逐颗确认**，不得自动提交。
- 确认后走 `worldquant-submit-alpha` skill：三段式 description **≥100 字**
  （不足会被**静默丢弃**，POST 返 201 但停留 `UNSUBMITTED`）。
- ET 配额 **4 颗/日历日**（00:00 ET = 12:00 GMT+8 重置）；配额满 → **挂起提交、继续挖掘**。
- **同族连测＝自相残杀**：同字段仅权重/decay 微调的变体只有第 1 颗能过 SELF 闸，**一族只留最优 1 颗**。
  ★ 同波"兄弟变体"（同骨架换字段）也是同族，SELF 仍 0.9+。
- ★ **提交一颗，全池相关性即重排 → 队列必须复核**（曾发生候选被新入池 alpha 锁死 0.8748）。
- 提交后跑步 9 复盘，沉淀 `registry_empirical` / `methodology rules` / wave ledger。

---

## 6. 上下文与持久化（ledger-first）

- 战役产物**只入 `data/wqb.db`**，禁止 Write 战役 json/csv。
- 每步即时入库：S0 `s0_ranking`/`s0_whitelist` → S1 `s1_<ds>_d<delay>` → S2 `expressions`
  → S3 `backtest_results`/`wave_results`/checkpoint → S6 `wave_results.verdict` + `registry_empirical`。
- 因此**上下文压缩随时安全**——不依赖"不压缩"，而是"压缩也不丢"。
- 每波结束给一份**高信号 I/O 明细**（只列影响决策的：白名单与淘汰理由、gate 通过率、
  prod/self 分布、过闸计数进度、点塔进度），**不要全量流水**。

---

## 7. 提速杠杆与止损规则

**提速杠杆（按 ROI 排序）**

1. **prod-first**（USA 命门，省算力最多；预警线 0.6）
2. **fast_kill**：8 探针无 `|S|≥0.5` 即判死（USA `loop_policy`）
3. 七槽即收即补，槽位常满；`create_multi_simulation` 批量（USA 批 8）
4. **挖掘/提交解耦**：提交不阻塞挖掘
5. **点塔集中**：3–4 座塔各打 3–5 颗，避免摊薄（20 颗理论可点亮 ~6 塔）
6. 复用已有结构信息（含 42 个历史 `PASS_CHEAP` 的结构洞察），但**已知被 prod_corr 卡死的不重复提交**

**止损 / 转向**

| 条件 | 动作 |
|---|---|
| P0.3 转化率 = 0，迭代 3 轮仍 0 | 换数据集（先确认已试 >10 种不同结构） |
| 连续 3 波全 FAIL 且无新 `dead_end` | USA 暂停，转 `brain-next-move-analysis` |
| 白名单被 `dead_end` 全覆盖 | 停止 |
| 连续 3 波 gate 通过率 = 0 | 换数据集 / 换信号族 |
| **`signal_floor` 闸拦截**（最近 2 波 `max\|S\|` < 0.9） | 换 universe / 换数据集 / 换区域，**不要绕过** |
| **`backlog_gate` 闸拦截** | 先消化近闸积压（`gem`/`selected` 也算），再开新波 |
| 过闸计数 = 20 | 立即停止 |

---

## 8. 对照修正表（v1 → v2，供复核）

### ① 接口/参数纠错：共 **9 处**（v1 原文照抄会直接失败；均已实测复现）

| # | v1 原文 | 报错 / 实际 | 正确写法 |
|---|---|---|---|
| 1 | `assemble-priors --snapshot` | argparse exit=2 | **`--snapshot-ledger`**（另有 `--print` / `--sha-only` / `--restore`） |
| 2 | `multi_create_simulate` | 工具不存在 | **`create_multi_simulation`** |
| 3 | "7 个 workflow 节点各跑 dry_run" | 实测 **18 个** | 按 `workflow_list_nodes` / `registry.py` 全量跑 |
| 4 | `wqb operator-audit` | 命令不存在 | **`tools/campaign_intel.py ghost-audit --region USA --delay 1`** |
| 5 | `score --region USA` | `error: unrecognized arguments: --region USA`（实测） | **去掉 `--region`**，region 由 `--campaign-dir` 派生 |
| 6 | `pipeline --dataset $DS --wave $W` | `error: argument cmd: invalid choice: 'pv63'`（实测） | **`pipeline run --dataset $DS --wave $W`**（`run` 是必需位置子命令） |
| 7 | `wave upsert ... --extra @notes.json` | `wave upsert` **无 `--extra`** | 用可重复的 **`--finding "..."`**，或 `--candidates @file.json` |
| 8 | `registry add-dead-end --extra @dead.json`（仅 extra） | 缺必填 → argparse 报错 | 必填 **`--id --family --reason --rule`**（`add-win` 必填 `--id --what --key`） |
| 9 | `ledger set-verdict --wave $W --verdict <...>` | 签名不符 | **`ledger set-verdict [--json JSON] <wave>`**（wave 是位置参数） |

> 上表 5/6 已实测复现（`score --region USA` → `unrecognized arguments`；
> `pipeline --dataset pv63 ...` → `invalid choice: 'pv63' (choose from 'quota','run')`），
> 修正后的写法也已实测跑通（`score --dry-run` 出排名、`pipeline run ... --dry-run` 走完闸门）。

### ② 消除自相矛盾（**最严重**，v1 硬约束 #5 与 #6 互斥）

v1 同时写了：
- 硬约束 #5「主辅信号权重显式分配，默认 **0.6 主 + 0.4 辅**，禁止 50/50 无差别 add」
- 硬约束 #6「禁止 `add(A,B)` 混信号」
- 步 4「参照 EUR win『**0.4 慢 MODEL 残差 + 0.6 快 PV**』机制换腿」

→ 这等于一边给加权配比、一边禁加权。**实测结论（2026-09-17，`logs/_tmp_gate_mix_probe.py` 直调
`gate.py::check_one`）**：**7 种加权混合写法全部被闸5 block**（星号中缀/加号中缀/func 权重在前/func 权重在后/
等权/旧 D6 CW 方子/旧 GBR 案例形），**7 种结构交互全部 PASS**。
即：按 v1 的 #5 和步 4 生成，会产出**必被闸5 拒绝**的整批表达式。

→ v2 处置：**只保留 #6（禁加权混合）**，并把"主辅配合"改写为 §3 步 4 的 **5 类结构交互表**；
EUR 配方的加权形态标注为**已废止**（2026-09-13「路线 A」），只继承其"跨数据集补腿意图"。

### ③ 补齐编排优化后新接入的闸与口径

| # | v1 缺项 | v2 补齐 |
|---|---|---|
| 5 | 步 6 积压口径 `pending+gated > 2×` | 新口径 **`unconsumed = gem+selected+pending+gated`**，阈值 `unconsumed_ratio_max=0.30`；且**已有自动闸** `_run_backlog_gate`（挂 S2/S3，dry-run 也走），不需自己重写 SQL 判断 |
| 6 | 未提 `signal_floor` | 三道开波闸表（`signal_floor` / `backlog_gate` / `stop_rules`）+ 灰度三档 `--gate-mode`；**USA floor=0.9**；缺节 **fail-closed** |
| 7 | 未提体检包前置 | 步 2 P0.2-①③ + 步 5-2：`field_inspect` 包为**开区硬前置**；`--inspect-mode {off,warn,enforce}`（enforce=缺包 fail-closed）；本地 ZIP 七区覆盖说明 |
| 8 | 步 5 用 `validator.check_batch` 的 5 条判据 | 收敛为**唯一权威** `gate.py:check_batch_diversity`（自学习契约 + exposure 多样性 + 家族天花板）；`validator.check_batch` 是 4 条形状闸且**零调用方**，降为方法论参考 |
| 9 | 未提提交层阈值 | 步 8-2：`_SUBMIT_HARD_GATE_WARNINGS={LOW_FITNESS,LOW_SHARPE,LOW_2Y_SHARPE}` 在 IS 只 WARNING、**提交层 FAIL**；**同步 403 = 零成本**且是读配额真值的手段；每候选只发 1 次 submit |
| 10 | 未提波号契约 | 硬约束 #7：`--wave` 字符串 + **禁裸时间戳**（已有 20 行脏数据先例） |
| 11 | 未提 priors 键大小写 | 步 4：真实 payload = **小写** `priors_snapshot_<region>`；大写是缓存标记 |
| 12 | 未提 skill 同步 | §0：`python tools/sync_skills.py`（仓库副本解析优先级最低） |
| 13 | CW 闸只说"见即弃"，未给修法 | 步 8：修法是**时间平滑**（`ts_mean`/`ts_decay_linear`），**调参数实测全无效** |
| 14 | USA prod 预警线写 0.7 | **0.6**（profile `prod_corr_early_warn`） |
| 15 | 未提 judge 只是参考层 | 步 8-3：`workflow_judge` 参考层，读 `checklist`/`degraded_gates`；**`degraded_gates` 非空 ⇒ verdict 不可用** |
| 16 | "USA 13 塔 0 亮" | 改为**运行时取**（`recommend_datasets` 用 pyramid 端点给未点亮塔优先），不在提示词硬编码塔数 |
| 17 | 未提空 verdict 危害 | 步 9：空 verdict 静默关闭停止闸规则 B（**假安全**） |
| 18 | 未提"提交后相关性重排" | §5：提交一颗全池重排 → 队列必须复核 |

---

## 附：可直接粘贴的启动指令（最短版）

```
按 tracking/USA/campaign_prompt_usa_regular_20.md 执行 USA REGULAR 20 颗挖掘战役。
先跑 Phase 0（P0.1 全部 18 节点 dry-run → P0.2 三道开波闸+校准+体检包 → P0.3 极小样本探针拿转化率），
把 P0.3 的转化率与七槽吞吐报给我，等我确认放大后再进 Phase 1。
全程遵守：禁加权混合（只用 5 类结构交互）、prod 预警线 0.6、体检包缺失不静默通过、
submit_verdict 为唯一提交权威、READY 等我逐颗确认、每波末回写步 9。
```
