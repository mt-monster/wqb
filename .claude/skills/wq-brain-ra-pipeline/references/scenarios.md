# RA 情景卡

> 情景卡 = 把一条规则落成「前置状态 → 步骤 → 分支 → 产物 → 完成定义 → 反例」，用来回答「这种情况下我具体做什么」。
> 规则本身在各步细则里；这里只放**会反复遇到、且最容易做错**的场景。数字例来自历史实证（带出处），命令以代码 argparse 为准。
> 主 SOP 见 [`../SKILL.md`](../SKILL.md)；快捷入口（发批 / 一键战役）也在这里。

---

## 情景 RA-01　库存盘点：够不够，不够补哪

- **前置状态**：新战役 / 新会话开工；`cache/basket.json` 由 `select_ra_basket.py` 产出（可丢弃的中间文件，不是事实源）。
- **步骤**：步 1 §1.2 的两条命令 → 数篮子条数与覆盖的**未点亮塔**数（一座塔要 3 颗点亮，CLAUDE.md）。
- **分支**（以 `target = 20` 为例）：

| 篮子 | 判定 | 动作 |
|---|---|---|
| 22 条，覆盖 4 座未点亮塔 | 够（≥ target 且 ≥ 3 座） | **直接跳步 7 / 8**（对篮子做稳健与提交判定），不开新挖 |
| 22 条，但只覆盖 2 座 | 条数够、塔数不够 | 进步 2，**只补缺口塔**（把已点亮塔的集排除，`s0-select` 默认已剔） |
| 9 条 | 条数不足 | 进步 2；篮子里已有的先做步 7 / 8，不等新挖 |

- **产物与落点**：`data/wqb.db`（`alphas` / `submit_ready`）；`cache/*.json` 用完可删。
- **完成定义**：分流结论写进本次会话的 `task_plan`（`planning-with-files`）或 `wave_results.key_findings`。
- **反例**：不要因为「库存里都是旧的」就跳过盘点——2026-09-07 会话前半段跨四区 170 次新回测产出 0 条可提交 RA，后半段一次库存扫描产出 20 条。篮子敲定以**资格门 `Failed RA == 0`** 为准，不是「无 FAIL」（WARNING / ERROR 也计）；`submit_verdict` 对处女候选只会给 `UNVERIFIABLE`，不构成可提交依据。

---

## 情景 RA-02　用户已给表达式列表：发批（快捷入口）

- **前置状态**：用户给出一批表达式 + 区域 / 数据集；不需要生成，但**不等于不需要前置**。
- **步骤**（跳过步 2 的选集与步 4 的生成，保留这三件）：
  1. 每个涉及的数据集有 typed catalog（没有 → `workflow_campaign(stage="S1", dataset=$DS)`；闸 2 / 3 缺目录直接 FAIL）；
  2. `python tools/field_semantic_classify.py --region $REGION --dataset $DS --write-ledger`（**秒级、零配额**）——闸 SEM 缺省 enforce，缺 `s1_semantic_<ds>` 即 **exit 2** 整波阻断；
  3. 体检包：缺包时体检门缺省只告警不生效（步 5 §5.6），新数据集首波自动升 enforce。
  然后：`ghost-audit` → `wave_gate --exprs-file <txt>`（表达式不在库时）→ 步 6 `workflow_batch_track`。
- **分支**：SEM exit 2 → 跑 classify（**不要**用 `--skip-semantic-gate` 蒙混，那需要 `semantic` waiver）；区域被停波 → 情景 RA-07；含幽灵算子 → 隔离到独立小批；缺 catalog → 补 S1。
- **产物与落点**：`gate_results`、`backtest_results`、`wave_results`（步 5 / 6 细则）。
- **完成定义**：步 5 `all_pass=1`、步 6 全部 multisim 终态。
- **反例**：「直接走步 5，跳过 S0–S2」的旧说法漏了上面三件前置——跳过 S1 的用户表达式必然被自家闸拦下。发批仍要过三道开波闸（`workflow_batch_track` 自己会跑）；CLI 直调 `build_wave.py` / `tools/wave_gate.py` 时，开波闸缺省 2026-10-11 及以前只告警，**2026-10-12 起拦截**（exit 2）——要放行停波区域写 waiver，别靠 `--gate-mode warn`。

---

## 情景 RA-03　一键战役 / auto campaign

- **前置状态**：用户说「一键战役 / auto campaign」；可能只给了 REGION。
- **步骤**（编号流程；旧文那一行长句语法不通、「配置包」未定义）：
  1. **步 1**：用户已给 REGION → 不调 matrix；用户说「挖点什么 / 哪个区好」→ 先 [`wq-brain-campaign-matrix`](../../wq-brain-campaign-matrix/SKILL.md)；matrix 返回多区并列 → **回问用户**；matrix 失败即停。
  2. **步 2** 体检（**不可跳过**）：配置包（matrix 产出的 region / universe / delay / 中性化 / 排除集）写回 `settings.json`，白名单写 ledger `s0_whitelist`。
  3. **步 3 → 4 → 5**：先用**一个小波**（8 条 = 一批）**真跑**，看步 5 的闸通过率与步 6 的产出。⚠ **干跑无从得出通过率**（没有 GEM 产物）；`workflow_chain(dry_run=true)` 只验命令链能构建（见 [`tool-index.md`](tool-index.md) T.2）。
  4. 确认小波结果后再扩批。
- **分支**：用户说「自动发起回测」= 可跳过步 6 前的二次确认（那是**派发仿真**，dispatch）；**提交 alpha 仍要步 8 用户明确确认**（submit，不可逆）。词义见 [`GLOSSARY.md`](../../GLOSSARY.md)。
- **完成定义**：本波走完步 9 的完成定义（`step9-writeback.md` §9.7）。
- **反例**：不要把「提交回测」与「提交 alpha」混为一谈；不要因为用户说「一键」就跳过步 2 体检。

---

## 情景 RA-04　prod 墙首探：五个数值例（决策表 D0-P 的落地）

- **前置状态**：S3 收批后，`prod-first` 对本波每个信号族最强 1 条实测了平台 prod（串行，单并发）。**判死 / 换机制的表只有 D0-P 一张。**
- **数值例**（首探 prod → 动作）：

| 首探 prod | 出处 | 落在 D0-P 的哪一行 | 动作 |
|---|---|---|---|
| 0.16–0.50 | IND w172 sentiment21 三族（prod 干净，墙在 robust 0.24 / limit 1.0 而非 prod） | < 0.60 | 正常扩变体，进步 7–8；墙不在 prod，要靠 robust 判定分清「prod 墙」与「结构墙」 |
| 0.6997 | IND pv103 尾盘反转 `mLm2xG1K`（S 3.83、IS 全过） | 0.60–0.70 | **不扩变体，当天进步 8**；提交前 `check_correlation(refresh=True)` 终验。先做变体的代价：1 小时后外部同款把 prod 堵到 1.0000，整族封死（`incidents.md` I-2） |
| 0.716 | MEA `9qXoJge2` | 0.70–0.75（踩线带） | 只许 **1 次**结构性尝试：删腿 / 换广度轴 → 0.6525，落回 0.60–0.70 行 → 当天进步 8 |
| 0.7003 | KOR wave113 | 0.70–0.75（踩线带） | 1 次尝试：表达式层 `group_neutralize(同信号, sector)` 包裹 → 0.6993。**证据强度：n=1、差值 0.001 在测量噪声内**，只算「可试」不算规则；仍 < 0.70 按 0.60–0.70 行处理，但当天提交 |
| 0.79–0.92 | IND intraday_pv_feats 价量相关反转（连投 3 波 24 条后才查，整族报废） | ≥ 0.75 | 家族记 `dead_end`：先 `forum_recon`（`found=true` 不得直接判死）→ `seal_dead_end`；下一步**换机制 / 换白名单里不同的数据集**，不磨同腿变体 |

- **产物与落点**：`alphas.prod_correlation`、ledger `prod_first_<wave>`、`prod_family_<region>_<骨架>`（闸 PF 下次读到）。
- **完成定义**：本波每个信号族有 `EXPAND` / `STOP` 结论。
- **反例**：**禁止用 `POST /submit` 探测 prod**——通过即提交，无撤回；prod 一律用 `check_correlation`（只读 `GET correlations/prod`）。踩线带里**不许**无诊断的盲扫（decay / 中性化设置 / 窗口逐档扫）、bucket / 门控 / 平滑（option8 IV 族 0.83–0.91 全参数空间实证无效）、镜像稀释或任何腿相加；有诊断指向分母 / 设置档 / 分组轴时按 D0-P「诊断前置」做那 1 次尝试。区域 profile 不得另设「预警线」改写这张表。

---

## 情景 RA-05　体检包缺失：什么时候要 waiver

- **前置状态**：白名单数据集在 `tracking/mining/` 下没有 `field_inspect_<region>_<dataset>.json`；本地 WebData 快照不含该集（JPN 白名单 12 集中 0 集、DEU 9 集中 0 集落在快照内，as_of 2026-09-17）。
- **步骤**：① `python tools/gen_field_inspect_packs.py --all --dry-run` 看能不能生成；② 能 → 生成，收工；③ 不能 → 先更新 WebDataScope 导出包再跑；④ 一时更新不了、又必须继续 → 写 waiver。
- **分支**：

| 你想做的 | 需要 waiver 吗 |
|---|---|
| 缺省 `--inspect-mode warn`（缺包告警放行，打印「体检硬门未生效」） | **不需要**——但这一波的预处理约束没人把关（低覆盖 / 厚尾 / 稀疏事件裸奔到仿真） |
| `--inspect-mode off` | **需要 `inspect` waiver** |
| `--inspect-mode enforce`（缺包整波拦） | 不需要；新数据集首波自动升 enforce |

- **写法**：`python tools/waiver.py new --gate inspect --region $REGION --reason-code NO_INPUT_AVAILABLE --reason "<无法生成的原因>" --evidence "<尝试过的命令与输出摘要>" --approved-by agent --days 3 --write`（`inspect` 闸批准人 user 或 agent，最长 7 天；`NO_INPUT_AVAILABLE` **必须带 evidence**）。协议见 `AGENTS.md` §8.1.2。
- **完成定义**：波次报告的 `waivers` 里可见这条 waiver；到期前补齐体检包。
- **反例**：不要「静默通过」——缺包又不留痕，等于这一波没有体检门。

---

## 情景 RA-06　判死：粒度与前置核对

- **前置状态**：某想法 / 族 / 数据集多轮不过，想判死。
- **步骤**：① 确定**粒度**——候选（淘汰）/ 字段搭配（禁配）/ 家族（`dead_end`）/ 数据集（`<ds>_dead`）/ 波（`FAIL`）；② 判死前取证——收批时 `forum_recon_wave` 已默认问过（读 ledger `forum_recon_wave_<wave>`）；要针对族再查：`forum_recon --out negative`（触发表 #5）；③ `found=false`（退出码 2 = 可靠的无解；**退出码 1 = 工具故障，不是无解**）→ `seal_dead_end(…, forum_recon={"question_key": …, "found": false})`（fail-closed 闸，按 `question_key` 回 ledger 核对）；`found=true` → 转 salvage / Mode B 武器；④ 步 9 §9.5 封存。
- **分支**：只有 RN 墙（`risk_neutralized_sharpe ≤ 0`）→ 步 7 §7.4（想法级 dead_end 须**全部**变体都 ≤ 0）；prod 墙 → 情景 RA-04；机制枯竭而非判死 → 触发表 #2（回补 KB）。
- **完成定义**：`registry_empirical` 有 `dead_end` 条目且 `payload.salvage` 已回填、`payload.forum_recon_gate` 有留痕（`verified` / `forced` / `waived`）；key_findings 里写了 `forum_recon` 结论。
- **反例**：**未选、未回测不能写成 dead_end**（选波清单里的延后项不是判死）；不要拿一颗候选的失败给整个数据集判死（粒度错位）。

---

## 情景 RA-07　用户要求继续挖被停手的区域

- **前置状态**：开波被停止规则 / 积压闸拦下（`success=false`，error 里点名规则）；用户明确说「继续」。
- **步骤**：`python tools/waiver.py new --gate stop_rules --region $REGION --reason-code USER_INSTRUCTION --reason "<用户指令原话>" --approved-by user --days <≤30> --write`（`backlog` 闸同理）。然后照常开波；横幅与报告会带 `waiver`。
- **分支**：被拦的是 `signal_floor` 或 `catalog` → **没有专门的 waiver 闸**：换 universe / 数据集 / 区域，或按 `loop-and-stop.md` L.3 处理；区域是 `frozen` → 情景 RA-08。
- **完成定义**：waiver 生效期内每次开波都能在 gate 结果里看到 `waiver` 字段；到期不续 = 自动恢复拦截。
- **反例**：不要靠 `--gate-mode warn` / `WQB_DISABLE_*` 绕过（后者仅测试隔离用）；不要写永久放行（旧键缺 `until` 会被识别为永久并告警 `NO_EXPIRY`）。

---

## 情景 RA-08　frozen 区域（如 MEA）

- **前置状态**：区域 profile `entry_verdict: frozen`；用户说「继续挖 MEA」。
- **步骤**：步 1 即拒，向用户报告冻结原因与「建议转区」；**只有**该区 profile 写明的后门可走——MEA：降级 `probe-only`，只探白名单外新上线数据集（`status=untried` 且不在红榜），**单波 8 探针上限，一波结束无论成败都回到 frozen**，先向用户声明配额成本、确认后执行。
- **完成定义**：本波结束后区域恢复 frozen；结果写 `wave_results` 与 dead_end / win。
- **反例**：不要因为用户说了「继续」就当作常规区处理（走完整九步）；`probe-only` 的默认含义见步 1 §1.1 的三态表，profile 只写与默认不同的部分。
