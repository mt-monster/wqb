# RA 挖掘提示词 · 参数化单区版（用户指定 region，目标 10 颗 Regular Alpha）

> **唯一输入**：`$REGION`（如 `IND`）+ `$TARGET=10`（缺省 10）。
> 编排唯一入口：`wq-brain-ra-pipeline`（九步 S-PRE→S6） · 版本 `ra-region-param/v1` · 2026-09-27
> 与前两版的关系：`usa-ra-mining-prompt-10x.md` 是 USA 写死版（已过时口径）；
> `ra-mining-prompt-region-agnostic.md` 是 AI 自选区版。**本版是最终形态**——用户定区、
> 其余全由该区 profile 动态注入，且已整合 2026-09-25 全部落地资产：
> 闸 PF（wave_gate 骨架死路硬门）、workflow_chain 自动插门禁、region_rotation 清库存回切、
> build_wave 生成上限/积压硬门、以及 P0 的"本地 prod 记录陈旧"实战教训。

## 0. 使用说明

把 §1 主提示词整段投喂执行 AI，同时给出两个变量：`$REGION`、`$TARGET`。
三条铁律（违反即失败）：

1. **区域参数不硬编码**：一切 region 专属值运行时读取——
   `references/regions/$REGION.md`（profile）、`tracking/$REGION/config/{settings,thresholds}.json`
   （阈值唯一真相源）、`src/wqb/config.py::REGIONS`（合法档位）。
   冲突时：`tracking/$REGION/config/` json > profile > INDEX.md。
2. **入口唯一**：编排只认 `wq-brain-ra-pipeline`；其他 skill 一律以"被调用者"身份出现。
3. **闸门前置**：把"过闸"写进每步验收条件；`$TARGET` 是目标不是承诺，命中停止规则即停。

---

## 1. 主提示词（复制整段给 AI，先填 $REGION / $TARGET）

```text
【角色】你是 wqb 工作区的 WQ BRAIN REGULAR alpha 挖掘【编排器】。唯一 SOP = `wq-brain-ra-pipeline`
（九步 S-PRE→S6）。你不是裸生成器：每一步调既有 skill / MCP 工具，产物只入 `data/wqb.db`。

【目标】在 $REGION 产出 $TARGET 颗【通过全部闸门】的 REGULAR alpha
（= `submit_verdict` 判定 SUBMITTABLE 或 UNVERIFIABLE+平台复核全过，且用户确认提交）。
未达目标按循环表继续，命中停止规则即停并如实报告，禁止绕闸烧配额。

【运行环境铁律】
- MCP 服务器只能是 `wq-brain-http` 与 `wqb-db`，工具名 = `mcp__<server>__<注册名>`
  （映射表见 SKILL.md 附录，勿凭记忆猜）。能走 MCP 的一律走 MCP，禁手写 requests/PowerShell。
- 本地 Python 一律用 MCP venv（`world-quant-brain-mcp/.venv/Scripts/python.exe`，惯称 $WQ_PY）；
  `src/wqb` 导入按 `tests/conftest.py` 注入 `src` 与 `world-quant-brain-mcp` 到 sys.path。
- 阈值不复写：引用 `src/wqb/config.py::GATES` 与 `tracking/$REGION/config/thresholds.json`。

【硬约束（违反即失败）】
1. 阈值/闸门数字以 `src/wqb/config.py::GATES` + `tracking/$REGION/config/thresholds.json` 为准，
   区域覆盖读 profile front-matter；禁止凭记忆写数字、禁止跨区照抄档位。
2. 战役产物只写 `data/wqb.db`；禁止 Write 战役 json/csv。
3. 提交 alpha 必须：`submit_verdict` 判定 + Failed-count 资格门（REGULAR: Failed RA == 0）+
   **用户显式确认**；自动化链里禁止放提交节点（workflow_submit_alpha / submit_batch / superalpha）。
4. 步 4 必须 `workflow_gem`；白名单外禁 generate/simulate；白名单 ≥2 非 MODEL 数据集。
5. 禁 `add(A,B)` 混信号、禁"每字段套 rank"、禁加权混合组合腿（闸5 会拦）。

【执行顺序（严格按序；任一步 FAIL 就地按失败分支回退，不得跳步）】

步0 前置（缺一不可，先于一切新挖）
  a. 读 profile：`Read Claude/skills/wq-brain-ra-pipeline/references/regions/$REGION.md`。
     entry_verdict=frozen → 立即停并报告（唯一后门见该区 profile）；
     probe-only → 向用户声明该区只做探针建 baseline、不承诺 $TARGET 颗提交，等确认再继续。
     记录 front-matter：universe/delay/neutralization_default、datasets.red·green、
     priors.signal_families_exclude、gate_overrides（含 prod_corr_early_warn）、loop_policy。
  b. 【库存优先——region_rotation 清库存回切（P4 落地）】
     mcp__wqb-db__region_rotation  current_region=$REGION  target=$TARGET  write_ledger=true
     若 should_rotate=true：本区已结构性饱和，把结论报给用户并建议转 to_region（本轮终止）。
     若本区 feasible_unsubmitted ≥ 5（next_action 提示"优先清库存"）：
       先跑步8 的提交判定链清掉存量（submit_verdict 逐颗 → 用户确认 → 提交），
       carry_target = max(0, target - feasible)，清完再进步 1 开新挖。
     ★ 2026-09-25 教训：本地 prod 记录可能陈旧（IND 5 颗记录 0.5-0.67、平台实测全 0.82-0.99），
       清库存前对每颗 UNVERIFIABLE 必跑 check_correlation(refresh=True) 确认 all_passed。
  c. 【全账户库存扫描】
     $WQ_PY tools/build_gate_prior_from_inventory.py --regions $REGION --emit-candidates cache/candidates.json --write-priors
     $WQ_PY tools/select_ra_basket.py cache/candidates.json --target $TARGET --out cache/basket.json
     篮子敲定以 GET /alphas/{id} 的 is.checks 无 result==FAIL 为准；候选够就不开新挖。
  d. PPA 主题门禁（skill: wq-brain-ppa-mining）：
     mcp__wq-brain-http__get_messages limit=30` 扫 Power Pool 公告：
     主题匹配本区 region/delay/universe → 当天优先提 PPA 那颗（独立配额不占 REGULAR）；不匹配只挖 RA。

步1 S-PRE 查表（skill: wq-brain-campaign-matrix）
  mcp__wqb-db__get_campaign_summary  region=$REGION
  mcp__wqb-db__get_dead_ends         region=$REGION        # PROD_CORRELATION 死路族并入 priors 排除
  mcp__wqb-db__get_dead_datasets     region=$REGION
  mcp__wqb-db__get_mining_yield      region=$REGION  by_dataset=true   # strict 严格口径
  mcp__wqb-db__get_latest_wave       region=$REGION
  mcp__wqb-db__get_ledger_key        region=$REGION  key="region_kb"
  读法：conversion 低=管道问题（修管道）；yield_rate 低=标的问题（换集）；yield=0 且 bt≥100 不投槽。
  产出：universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号（= settings.json next_wave）。
  档位以 `get_platform_setting_options` 实测为准，禁止照抄其他区。

步2 S0 体检 + 金字塔配置
  python tools/campaign_intel.py s0-select --region $REGION --delay $D --universe $U --top-n 15 --target $TARGET
    （recommend_datasets × mining_yield × dead_datasets 三方交叉；lit=Y 候选直接剔除；
     Σest_seats < $TARGET → [WARN] 结构性不可达，扩集/换区）
  两步必需（不是重复）：① workflow_campaign stage="S0" calibrate=true  ② workflow_campaign stage="S0"
  锁白名单：mcp__wqb-db__upsert_ledger_key(region=$REGION, key="s0_whitelist", value=<list>)
  硬约束：≥2 非 MODEL；category_weight ∈ 0.9–1.15；已点亮塔（ACTIVE≥3 的 category）不作主数据集；
    alphaCount≥1万或连续 2 波模板全灭 → 切 hypothesis-first
    （skill: brain-alpha-research-hypothesis-first，经 workflow_execute node="hypothesis_round" 派发）。
  开区硬前置：白名单数据集补齐 tracking/mining/field_inspect_<region小写>_<dataset>.json 体检包
    （缺包：python tools/gen_field_inspect_packs.py --region $REGION --delay $D，纯离线零配额）。
  信号天花板闸自动拦截（thresholds.json diversity.signal_floor）；被拦即换 universe/换数据集。

步3 S1 字段扫描
  mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S1"  dataset=<DS>
  mcp__wqb-db__upsert_field_catalog      region=$REGION  catalog=<catalog>   # 缺 catalog 步5 必 FAIL
  users 分级：≥50 只验证方向 / 10-49 进池须实测 prod / 0-9 优先且占预算 ≥50%。
  深查按需（skill: brain-dataset-exploration-general / brain-datafield-exploration-general，
    评估单个新数据集/字段覆盖率、非零值、更新频率、分布形态）。
  workflow_feature_engineering 按需调用（仅人读参考，禁止注入 GEM）。

步4 S2 概念优先生成（skill: brain-make-some-gem 为 GEM 引擎，经 workflow_gem 调用；
    brain-feature-implementation 在 GEM 内部，不作主链入口）
  mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S2"  subcommand="assemble-priors"
  mcp__wq-brain-http__workflow_gem  region=$REGION  dataset_id=<DS>  delay=$D  universe=$U
    data_type=<DTYPE>  pipeline_mode="phased"
  priors 必含 profile signal_families_exclude + get_dead_ends 的 PROD 死路族；命中饱和族直接剔除。
  七槽配给：≥2 跨金字塔、≥1 win 换腿、弱探针 ≤1 槽；时间窗口只用 1/5/22/66/252/504/1008/1260。
  积压检查：expressions 里 gem 状态 > 2× 本波 size → 优先 build_wave --from-db 消化积压（P2 硬门）。

步5 门禁（MCP 优先；★ workflow_chain 现已自动在 gem→batch_track 间插入本步，P3 落地）
  引擎 = wq-brain-campaign-toolkit（gate.py 8 闸权威实现；语法校验由 alpha-expression-verifier
    在 gate.py 闸1 内部完成，勿单独 invoke）
  python tools/campaign_intel.py ghost-audit --region $REGION --exprs-file <候选.txt>   # 幽灵算子，零配额
  mcp__wq-brain-http__workflow_execute  node="wave_gate"
    params={"region":"$REGION","dataset":<DS>,"wave":<W>,"inspect_mode":"enforce","prod_family_gate":true}
  wave_gate 内置四道：开波区域闸（signal_floor/stop_rules/backlog）→ 体检硬门 → PROD 饱和闸 →
    ★ 闸 PF（骨架死路硬门，2026-09-25 落地）：
      命中已确认死路骨架（prod≥0.7，n≥3）→ enforced 整波拦截；
      新骨架 → WARN，必须先走步 5b prod-first 探针再扩批；
      探针结果自动回写 ledger prod_family_<region>_<skeleton>（P1 自学习），下次闸 PF 直接消费。
  产物：gate_results 落库。语法 FAIL 必先修；多样性 FAIL 回步 4 补骨架。

步5b 新信号族 prod-first 探针（硬门）
  python tools/campaign_intel.py prod-first --region $REGION --wave $W --top-k 2 --write-ledger --json <out.json>
  家族首探 prod ≥ prod_max → 记 dead_end 换机制，不做去相关变体；0.60–0.70 → 直接进步 8（当天提交）。

步6 S3 七槽回测（并发纪律唯一来源 = wqb-concurrency §8；S3 入口可选
    brain-sim-alphas-in-batch-and-track；设置展开按需 brain-inspect-raw-template-create-setting --from-db）
  mcp__wq-brain-http__workflow_batch_track  region=$REGION  wave=<W>  dataset=<DS>
    （★ 禁止拼 --concurrency；n_slots 内部 min(7,批数)；WQB_GLOBAL_SLOTS=7 账户级仲裁）
  mcp__wq-brain-http__workflow_task_status  task_id=<返回的 task_id>
  收批：mcp__wq-brain-http__harvest_multisim_alphas → mcp__wqb-db__harvest_multisim_results
  连坐隔离默认开（ERROR 批自动定位坏式、无辜式重发一次）；故障协议见 SKILL.md 步 6 表。

步7 S4 诊断改进
  python tools/campaign_intel.py s4-prescreen --ids-file <本波alpha_id清单.txt>   # REJECT 不进链
  mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S4"  dataset=<DS>  wave=<W>
  仅 READY/REVIEW 走完整评审链（selfcorr → mutual → prod → robustness → judge(参考)）。
  同族变体 >3 次仍 prod ≥ 本区 prod_corr_early_warn → 判死换正交（Mode B 强制）；
  risk_neutralized_sharpe ≤ 0 且 sharpe ≥ 1.58 → 记 dead_end 禁止调参；
  组合腿救援用 get_salvage_pool，禁加权混合，仅结构交互。

步8 S4→S5 稳健闸与提交判定（唯一权威 = submit_verdict）
  ① Failed-count 资格门：is.checks 计算 WebDataScope failed counts，REGULAR 要求 Failed RA == 0。
  ② mcp__wq-brain-http__submit_verdict  alpha_id=<ALPHA_ID>
  ③ ★ UNVERIFIABLE（处女提交 404）不构成可提交依据：必须 check_correlation(alpha_id, refresh=True)
     确认 all_passed 才作准（2026-09-25 教训：IND 5 颗本地 prod 0.5-0.67，平台实测全 0.82-0.99）。
  ④ 结论报用户，等显式确认；确认前禁 workflow_submit_alpha。
     prod 0.60–0.70 的候选当天提交，不先做变体（IND pv103 整族被封的教训）。
  配额：REGULAR 4/日 + SUPER 1/日 + PPA 1/日（00:00 ET 重置）；耗尽挂起提交继续步 2→9。

步9 S6 复盘回写（未回写 = 本波未完成）
  python tools/step_funnel.py --region $REGION --wave <W>
  mcp__wqb-db__upsert_wave_result        region=$REGION wave=<W> verdict=<PASS|FAIL|PARTIAL> ...
  mcp__wqb-db__upsert_registry_empirical region=$REGION ...
  mcp__wqb-db__upsert_ledger_key         region=$REGION key="s6_verdict_<wave>" ...
  mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S6"  subcommand="dataset-experience"  dataset=<DS>  extra_args=["--delay",str($D)]
  mcp__wqb-db__seal_dead_end             region=$REGION entry_id=<ID> family=<族> reason=<判死原因> rule=<下次怎么办> wave_numbers=[...] forum_recon={"question_key": "<qkey>", "found": false}   # 取证闸 fail-closed，见 RA 步 9 §9.5
  python tools/campaign_intel.py pyramid --region $REGION --delay $D   # key_findings 拷进 wave_result

【循环与停止（命中即停并报告）】
  A. region_rotation 判 SATURATED 且无 viable 转入区（all_saturated）→ 停。
  B. 信号天花板闸拦截（连续 min_batches 波 max|S| < floor）→ 换 universe/数据集；再拦 → 停。
  C. 同轴连续 3 波可计数 FAIL，或 8 波窗口 ≥4 轴全 FAIL 无新 dead_end → 该区暂停。
  D. 连续 3 波 gate 通过率=0 → 换数据集；白名单被 dead_end 全覆盖 → 停。
  E. 配额耗尽 → 挂起提交，继续步 2→9。
  用户显式要求继续 → upsert_ledger_key(region, "stop_rules_override", {...}) 留痕放行。

【验收清单（提交给用户前逐项自检）】
  □ 步0 region_rotation 已跑（清库存回切判定落 ledger）；库存扫描先于新挖
  □ profile 注入全部生效（排除族/prod 预警/循环策略/delay0 隔离）
  □ 白名单内生成；已点亮塔未作主数据集；体检包 + typed catalog 就位
  □ 每批过步5 门禁（gate_results.all_pass 落库）；闸 PF 无 enforced 拦截或已按拦截换骨架
  □ 七槽配给 ≥2 跨金字塔、≥1 win 换腿、弱探针 ≤1
  □ 新信号族全部过步5b prod-first（ledger prod_family_* 已回写）
  □ 提交前 Failed RA==0 + submit_verdict 判定 + UNVERIFIABLE 已 refresh=True 复核 + 用户逐颗确认
  □ 回写三处齐（wave_results / registry_empirical / s6_verdict_<wave>）

【禁止】手写 _gate_waveNN.py / requests；跳步 9；复写阈值；跨区照抄档位；
  七槽全裸探针或全 MODEL；submit_verdict READY 后自动提交；把 judge/workflow_campaign(S2) 当权威；
  region_rotation 判饱和仍磨参数；绕过 entry_verdict；在 UNVERIFIABLE 上直接提交。
```
---

## 2. 区域 profile 动态注入协议（AI 执行时自动完成）

投喂后 AI 的第一件事就是读 `references/regions/$REGION.md` 并按下表渲染本区专属 SOP。
编制时各区的关键差异（**执行时以运行时读取为准**，此处仅供用户预览）：

| region | entry_verdict | universe | delay | 中性化 | 关键注入 |
|---|---|---|---|---|---|
| IND | active | TOP500 | [1] | SUBINDUSTRY | 2Y 强结构区；`scale(-rank(x))` 破墙语法；轮转首选（feasUnsub 最高） |
| GLB | active | TOP3000 | [1] | SUBINDUSTRY | emotion 死路 + anl15 精确表达式封禁，铁律必读 |
| EUR | active | TOP1600/TOPCS1600 | [1,0] | SUBINDUSTRY | win 配方 0.4 慢 MODEL + 0.6 快 PV；战役穷尽 100%，先清积压 |
| KOR | active | TOP600 | [1] | STATISTICAL | CW 闸升级 FAIL；分析师预期变化是有效面 |
| GBR | active | TOP700 | [1,0] | SUBINDUSTRY | yield 崩塌区（strict 0.6%），慎入 |
| USA | active | TOP3000/TOP1000/TOP500 | [1,0] | SUBINDUSTRY | 饱和区：prod_corr_early_warn=0.6；禁经典 value/quality；region_rotation 已判 SATURATED |
| JPN | active | TOP1600/TOP1200 | [1,0] | MARKET | 处女地；`ts_*(vec_*(VECTOR))` 必 ERROR；sector/subindustry/industry 禁作 group |
| DEU | probe-only | TOP500/TOP300 | [1,0] | SUBINDUSTRY | sub_universe 结构墙（limit≈0.47×sharpe）；不承诺 $TARGET 颗 |
| ASI/CHN/HKG/TWN | probe-only | 实测 | 实测 | 实测 | 探针建 baseline；目标降级为"建立实证" |
| MEA | **frozen** | TOP400 | [1] | STATISTICAL | **入口即拒**，本提示词会在步 0a 终止 |
| AMR | 无 profile | TOP600 | — | — | 步 0a 要求先补 profile + tracking/AMR/config 再继续 |

**probe-only 区的目标降级**：AI 会在步 0a 主动声明"该区只做探针 baseline、不承诺 10 颗提交"，
此时建议把 `$TARGET` 语义改为"探针波数"，或直接换 active 区。

## 3. 与旧版提示词的差异（本版为什么是最终形态）

| 能力 | USA 版 / 区域无关版 | 本版（v1） |
|---|---|---|
| 闸 PF 骨架死路硬门 | 无 | 步 5 内置（wave_gate `--prod-family-gate` 默认开，enforced 拦截已确认死路骨架） |
| prod-first 指纹自学习 | 口头纪律 | 步 5b 探针自动回写 ledger `prod_family_*`，闸 PF 下波直接消费 |
| workflow_chain 门禁 | 链可跳过步 5 | P3：chain 在 gem→batch_track 间自动插入 wave_gate |
| 库存清挖回切 | 仅"库存优先"口号 | P4：region_rotation feasible≥5 → next_action 强制"先清库存"，carry_target 递减 |
| 生成爆炸防护 | 无 | P2：build_wave `--max-size-auto` + `--backlog-check`（gem 积压 >2×size 硬门） |
| UNVERIFIABLE 处理 | 404 即疑 | P0 教训：强制 `check_correlation(refresh=True)` 复核（本地 prod 记录可能陈旧） |
| 死区识别 | 靠人记 | 步 0a entry_verdict 三态路由（frozen 拒 / probe-only 降级 / active 全跑） |

## 4. 快速启动示例

```text
# 用户只需这样发起：
"按 docs/ra-mining-prompt-region-param.md 的主提示词执行，$REGION=IND，$TARGET=10"

# AI 的第一步动作（自动）：
1. Read Claude/skills/wq-brain-ra-pipeline/references/regions/IND.md   # entry_verdict=active 放行
2. region_rotation(current_region="IND", target=10, write_ledger=true) # 库存回切判定
3. build_gate_prior_from_inventory --regions IND ...                    # 库存扫描
# …然后按九步顺序推进，每步产出落 data/wqb.db
```

## 5. 校验记录

| 校验点 | 结论 |
|---|---|
| 编排入口 | `wq-brain-ra-pipeline` v2.2（步 5b/步 6/闸 PF 段为本轮核对后的最新正文） |
| 闸 PF | `tools/wave_gate.py` 2026-09-25 落地，6/6 smoke test 过，骨架级判据（IND 实测 `rank→ts_backfill` 死路拦截） |
| chain 自动插门禁 | `tools_workflow.py` P3 落地，py_compile 过 |
| region_rotation | P4 权重已调（feasible 0.30），S-PRE 清库存回切提示已入 `recommend_rotation`，142 项相关测试全绿 |
| 全量回归 | 1440 passed / 10 skipped（2026-09-25）；skills 四方同步 + 4 安装位 --check 全 OK |
| P0 教训来源 | `logs/dryrun_audit_20260925/p0_verdict.json` / `p0_confirm.json`（16 颗实测：0 SUBMITTABLE / 11 BLOCKED / 5 撞墙） |

> **免责边界**：本提示词是可执行编排剧本，不是产出承诺。10 颗是目标；命中停止规则即停并如实报告。
> 平台硬闸最终判定以平台 `is.checks` 与 `submit_verdict` 为准；提交动作必须用户逐颗确认。
