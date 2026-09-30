# 步 9（S6）细则：复盘回写——顺序、写入契约、封存

> 主 SOP 见 [`../SKILL.md`](../SKILL.md) 步 9。**本文的编号就是执行顺序**（旧文把「完成定义」放在最前、「先看漏斗」放在最后，顺序与执行相反）。
> 完成定义在 §9.7：**缺任何一项 = 本波未完成**。GEM 对 stale 先验快照只 WARN 不阻断，所以第 ⑧ 步只能由本步兜底。

## 9.1 有序流程

| # | 动作 | 调用 | 产物 |
|---|---|---|---|
| ① | **看漏斗**（只读；回写结论前先跑，用数据定位「这一波 / 这个区在哪一跳掉得最狠」，别凭印象写 verdict） | `python tools/step_funnel.py --region $REGION [--wave $W] [--json]` | 瓶颈定位（§9.2） |
| ② | **判 verdict** | §9.3 判定表 | `PASS` / `PARTIAL` / `FAIL` |
| ③ | **点塔进度** | `python tools/campaign_intel.py pyramid --region $REGION --delay $DELAY`；取输出末尾的 `[key_findings]` 单行 | 供下一波 S0 直接消费平台真实塔状态 |
| ④ | **写波结论**（③ 的行与本波其它 key_findings **一次带齐**） | `mcp__wqb-db__upsert_wave_result`（§9.4） | `wave_results.verdict` = **唯一结论源** |
| ⑤ | **判死 / 胜绩** | 判死 → §9.5；胜绩 → §9.6 | `registry_empirical` |
| ⑥ | **饱和反馈**（本波候选**全部**被 prod 墙卡死时） | `python tools/campaign_intel.py mark-saturated --region $REGION --dataset $DS --reason "<原因>" --wave $W --prod-corr <值> --write-ledger` | ledger `saturated_datasets`（S0 打分读取，把该集降 `excluded`；不加 `--write-ledger` 只预览）。**旧做法**（往 `submit_ready_blocked` 追加饱和记录）已废止——S0 从未读过那个键，只有 `step_funnel` 计数 |
| ⑦ | **逐数据集经验沉淀** | 对本波**每个实际回测的数据集**：`workflow_campaign(stage="S6", subcommand="dataset-experience", dataset=$DS, extra_args=["--delay", str($DELAY)])`，收取后台任务终态，再补充块外的中文字段 / 机制复盘 | `reports/dataset_experience/<region>_<dataset>_campain.md`（只读 DB 生成，保留人工复盘块；默认累计该数据集历史，专门总结本次战役才传 `--waves`） |
| ⑧ | **刷新先验快照** | `mcp__wq-brain-http__workflow_campaign(region=$REGION, stage="S2", subcommand="assemble-priors")`（默认带 `--snapshot-ledger`） | `priors_snapshot_<region>` |

未回测、诊断中、待出相关性的不能记成已验证成果（步 7 → 步 8 的候选不是 win）。

## 9.2 漏斗怎么读（`tools/step_funnel.py`）

- **只读推导**：数据全部来自既有表 + ledger（`expressions` / `gate_results` / `backtest_results` / `wave_results`），不建表、不写库。
- 输出：S2 生成池（含 `unconsumed = gem+selected+pending+gated` 溢出比）/ S2→S3 门禁（批次粒度 + 表达式粒度双口径）/ S3 回测（含过廉价闸数、最佳 sharpe）/ S4→S5 就绪 / S6 verdict 分布 / 转化链 / **瓶颈定位**。
- ⚠ 各步取的是**各自表的存量**，时间窗不完全一致，链上数值**可能不单调**——只用来定位瓶颈，不作精确转化率引用（工具已自标）。
- ★ 五张 `step_*` / `*_summary` 表**恒 0 行且不应填充**（自动采集是 TODO 空壳、质量指标可从既有表推导、增益指标是反事实估算）。**要步级视图就用本工具，不要往那五张表写。**

## 9.3 verdict 判定表（与 `pipeline.py --review` 自动判定的 GREEN / YELLOW / RED 同一规则）

按本波逐条**事实**判，不要写描述性文字（"无提交(…)"、"FULL_RED"、"✅ 提交成功" 一律会被拒）：

| verdict | 判据 |
|---|---|
| `PASS` | ≥ 1 条候选**过全部评审闸**（`review_passed`；已提交的必然达标） |
| `PARTIAL` | 0 条达标，但 ≥ 1 条进 near 池（接近闸门，可沿 Mode A / B 继续） |
| `FAIL` | 0 达标且 0 near（全灭 / 判死） |

- 「达标」在本库有三种口径，**别混**：`meets_internal_line`（Sharpe>1.58 且 Fitness>1.0；停止规则 A）/ `ra_clean`（Failed RA = 0；严格产出率）/ `review_passed`（评审闸全过；**本表用这个**）。词义见 [`GLOSSARY.md`](../../GLOSSARY.md)。
- 波结论只用 `PASS / PARTIAL / FAIL`，**不用颜色词**（GREEN / YELLOW / RED 属 alpha 提交标签，见 GLOSSARY §2.6）。
- 被拒时返回里的 `suggestion` 是按此表对原文的**建议**（带依据与置信度；low 置信通常是「无提交」——有 near 候选就该是 PARTIAL），**不会自动采用**：核对后显式传 `verdict=<枚举>`，原文放进 `key_findings`。补记旧波同理。
- 停止规则 B 的「最近 3 个 closed 波」按**波的开始时刻**（该波首次入库表达式的时间）取，补记结论 / 补写 findings 不会把旧波顶进窗口（2026-09-27 起；此前按 `updated_at`，补记旧波 PASS 会解除区域停波）。闸结果的 `evidence.recent_closed_waves` 列出窗口内的波号。

## 9.4 写入契约：`upsert_wave_result`

```
mcp__wqb-db__upsert_wave_result  region=$REGION  wave_number=$W  verdict=<PASS|PARTIAL|FAIL>  key_findings=[…]  [focus=…  candidates=…  status=…]
```

- **合并语义**（2026-09-27）：行已存在时只覆盖本次传入的字段；只补写 `key_findings` 不会再清空 verdict（此前会，停止规则 B 随之失效）。
- `key_findings` / `candidates` / `batches` / `full_payload` 一旦传入即**整列替换**：事后补写要带上原有条目——所以 ③ 的点塔行必须与其它 findings **在同一次调用里**传。
- `verdict` 只接受 `PASS / FAIL / PARTIAL`：`FAIL_xxx：…` / `CLOSED_DEAD_END_…` 这类前缀形态归一到枚举，并把原文搬进 `key_findings[0]`；无法辨认的直接拒绝。描述性结论请写 `key_findings`。
- `status='closed'`（新行缺省即 closed）**必须带 verdict**；结论未定传 `status='open'`。`wave_number` 可传字符串（如 `s2_<ds>_d1`）。
- `pipeline.py --review` 收批后自动刷新 `region_kb` 的 `recent_waves` / `gate_priors_local` / `updated_at`（手动部分只剩 win / dead_end / 饱和 / 点塔）。
- **不要**再写 `s6_verdict_<wave>` / `wave<N>_verdict` 这类旧键：结论只有 `wave_results.verdict` 一个来源（2026-09-28 去重；旧键已废止）。
- key_findings 里建议固定带的几条（供下一波与审计读）：点塔进度行；**本波是否跑过 prod-first**（漏跑是复盘要点，见 `docs/plans/2026-09-23-dryrun-audit-optimization-plan.md` P2-3）；用过 QUICK 模式的记 `simulationMode`；`forum_recon` 的结论。

## 9.5 判死封存：先沉降、再封存

术语（旧文「沉降 / 封存 / seal」三词并用）：**沉降** = 把该想法涉及波次的失败候选放进 `salvage_pool`（收集宽）；**封存** = 写 `dead_end` 条目并把残值列表回填 `payload.salvage`；**动用** = Mode B 取用残值（仍守各区 `mode_b_qualification`，动用严）。判死按粒度：候选 / 字段搭配 / 家族（`dead_end`）/ 数据集（`<ds>_dead`）/ 波（`FAIL`），见 GLOSSARY。

1. **前置取证**（判死前）：`python tools/forum_recon.py --question "<数据集/信号族> 有无解法" --context region=$REGION,dataset=$DS,family=<族> --out negative`。结果记入 `dead_end.payload.forum_recon`（含 `question_key` / `found`）。**设计**（2026-09-29，见下「现状」）是把它做成 fail-closed 的硬闸：

   | `payload.forum_recon` | 判死 |
   |---|---|
   | `found=false` | ✅ 允许（decision-table D2「论坛无解」取证成立）；退出码 2，负结果已入 `forum_recon_negative_<qkey>` |
   | `found=true` | ❌ 拒绝——配方转 salvage / Mode B 武器，**不得直接判死** |
   | `found=null` / `status=error` | ❌ 拒绝——**工具故障 = 未取证，故障 ≠ 论坛无解** |
   | 缺失 | ❌ 拒绝——未取证 |

   - ⚠ **为什么必须 fail-closed**：判死是永久封存一条路。2026-09-29 实证 5 条 recon 记录里 **2 条是工具故障**（`load_creds` TypeError、`No module named 'requests'`），被记成 `found=false` 落 `forum_recon_negative_*`，等于「工具坏了 ≡ 论坛无解」→ 误把活路判死。
   - **现状（2026-09-30 合并 main 时核对代码）：闸与配套修复都没有落地。** `seal_dead_end` 没有 `force_seal` / `require_forum_recon` 参数，不看 `payload.forum_recon`；`tools/forum_recon.py` 在**论坛鉴权失败**时仍把 `found=false` + `error` 字段写进 `forum_recon_negative_<qkey>`、进 7 天缓存，并打印「可作『论坛无解』判死证据」，**退出码也是 2**（与真无解无法区分）。所以**目前靠人**：判死前读输出 JSON 与那条 `forum_recon_negative_<qkey>` 记录，**带 `error` 字段的不是取证**（要重查须先删 `tracking/FORUM/forum_recon_cache.json` 里该问题的条目，否则 7 天内回放同一个故障结果）；没有记录就先跑；`found=true` 不得直接判死。
   - **波级默认取证**（收批时 `forum_recon_wave` 节点自动取证落 ledger，`forum_recon_error_<qkey>` 记故障）同样是设计：节点**未注册、无实现文件**——见 [`forum-recon-triggers.md`](forum-recon-triggers.md) 末节。
   - prod 墙的判死分支同样先过这一步（D0-P：≥ 0.75 或踩线带尝试失败 → `forum_recon` → 封存）。
2. **封存**：

```
mcp__wqb-db__seal_dead_end  region=$REGION  entry_id=<ID>  family=<族名>  reason=<判死原因，带数据>  rule=<下次怎么办>  wave_numbers=[W1,W2,…]
```

   - **`entry_id` 由你命名，不需要先创建**：`seal_dead_end` 本身就是 upsert（沉降残值 → 读现有 payload → 回填 `payload.salvage` → 写 `dead_end` 层）。命名约定 `<REGION>-<数据集或族>-<症状>`，全大写连字符，区域内唯一（如 `KOR-WAVE99-XXX-DEAD`）。
   - **`family` / `reason` / `rule` 新建时必填**（与 CLI `add-dead-end` 同一份校验，`wqb.registry_contract`）：缺任一项返回 `status=error` 且**不沉降、不写库**；条目已存在时可省，已有的 `rule` 会保留。`rule` = 下次怎么办（配置包排除该族时引用它）。
   - `wave_numbers` **只识别整数波号**：字符串波号（`s2_<ds>_d1`）会被跳过、不沉降；这类波的残值已在收批级联里入池，需要补池用 `mcp__wqb-db__backfill_salvage_pool`。
   - 封存后 `registry_empirical` 的 `dead_end` 层进入下一次 assemble-priors 的 `dead_ends`（倒序，新封存者靠前）。
3. **写入路径**：MCP 可用时用上面的调用；无 MCP 或批量回写时用 toolkit 的带校验 CLI：`python Claude/skills/wq-brain-campaign-toolkit/scripts/campaign.py --campaign-dir tracking/$REGION registry add-dead-end --id … --family … --reason … --rule …`（`id / family / reason / rule` 必填，`--dry-run` 可先校验）——两条路径写同一张表、同一份校验，任选其一，**不要两边各写一遍**。

## 9.6 胜绩回写

OS ACTIVE / 全闸 PASS 的候选**必须**回写胜绩：

```
mcp__wqb-db__upsert_registry_empirical  region=$REGION  layer="win"  entry_id=<ID>  payload={"id": …, "what": <信号概念>, "key": <设置与骨架>, "evidence": …}  family=<族>
```

（无 MCP 时 `campaign.py … registry add-win --id … --what … --key …`。）**`what` / `key` 只记「信号概念 + 设置」，不再记录混合比例**——已验证配方不含腿相加（主文步 7、步 4 约束 1）。下一次 assemble-priors 把它读进 `wins`（见 [`assemble-priors-internals.md`](assemble-priors-internals.md)）。
判死与胜绩之外，`template_kb`（兑现进 `validated`、未兑现进 `failed`，对照 GEM 声明的 `Expected Exposure`）目前**没有脚本写入方**，靠人工 / agent 维护（`docs/ledger_keys.json` 登记为 orphan）。

## 9.7 完成定义（缺一 = 本波未完成）

- [ ] `wave_results` 有本波记录，`status='closed'` 且 `verdict` 为枚举值（`mcp__wqb-db__get_wave_result` 或 `step_funnel --wave` 可核）
- [ ] 该 wave 的 key_findings 含点塔进度行、prod-first 是否跑过
- [ ] 有判死 → `dead_end` 已封存（含 salvage 回填）；有胜绩 → `win` 已写
- [ ] 本波候选全被 prod 墙卡死 → 已 `mark-saturated`
- [ ] 每个实际回测的数据集都已 `dataset-experience`
- [ ] **assemble-priors 已再跑**：`priors_snapshot_<region>` 不早于本次回写（GBR 实测：快照停在 09-19，而 `region_kb` 已 09-25、`registry_empirical` 已 09-26 → 落后 8 天，本波结论不回流）

产物归属见 [CONTRACT §4 共享产物归属](../../CONTRACT.md)。

## 9.8 提交之后：本 SOP 覆盖什么、不覆盖什么

| 事项 | 状态 |
|---|---|
| **提交多样性监控**（防同质化降权） | 每提交 3–5 颗后调 `mcp__wq-brain-http__value_factor_trendScore(start_date=<本季初>, end_date=<今天>)`。**没有机检阈值、也没有自动切换**：判据 = 同一区间内后一次读数低于前一次 → 由 agent 在下一波 S0 把目标塔改到未点亮塔（`s0-select` 已默认剔除已点亮塔） |
| **IS→OS 衰减归因**（可选，反哺 IS 阈值校准） | 提交后 T+1 调 `mcp__wq-brain-http__performance_comparison(alpha_id=<ID>)`，把结论作为一条 `key_findings`（「OS 归因：…」）写进该 alpha 所属波——**无专用字段**，key_findings 整列替换，要带上原有条目 |
| **OS 表现监控与重着色**（BLUE → GREEN / YELLOW / RED） | **没有承接者**（旧的 OS 回流脚本已归档；`tools/sync_platform_alphas.py` 只把平台 OS 池数据同步进本地台账供衰减基线用，不重着色）。这是已登记的声明-实现缺口（审查 X-18 / T0-18），**不要假设有人在做** |
