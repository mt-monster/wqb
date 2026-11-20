# KOR Regular Alpha 挖掘标准流程（SOP）

> 适用范围：KOR/TOP600/Delay=1 的 regular alpha 完整战役执行——选集 → 体检 → 结构设计 → 开波回测 → 收批判闸 → 交付回写。
> 不适用于：其他区域与跨区配方照搬（一切数值结论换区须重扫，`Claude/skills/wq-brain-ra-kor/SKILL.md:36`、`:124`）；非 regular 谱系（SUPER/PPA）。
> 本文件是流程正文；KOR 的方法细节与实证分别见 `Claude/skills/wq-brain-ra-kor/SKILL.md` 与其 `references/`，不在此重复。
> 带日期的当期指令与快照读数一律标 `as_of`，并按第 0 步被用户当期确认覆盖。

## 0. 开工第 0 步：用户当期确认（as_of 覆盖纪律）

每次开工先做三件事，做完才允许进入第 2 章：

1. **确认本文件附录的 `as_of`**（当前 2026-11-16）。附录中的全部读数、判死标记、prod 值是**当期快照**：
   用户在开工指令里重新点名的内容以用户指令为准；用户未点名的，按附录现状执行；
   与附录冲突且无法向用户求证的，按「只收紧、不放宽」执行（能停投的不放开，能标的照样标）。
2. **确认交付口径**是否仍是「failed_ra_count=0 且 prod<0.7（严格不等式，当日回源）」。
   该口径由用户 2026-11-16 定（final_report.md:3-6）；用户改口径则覆盖本章与 §5-R1。
3. **确认提交权**在用户：本 SOP 的任何产物都不含提交动作；提交须用户明确确认，之后才允许带
   `confirm_submit=True`（用户确认是唯一放行权威；AGENTS.md §3.5 步 8，代码硬闸 `wqb.workflow.executor.execute_chain`）。

实证数字必须带 `as_of` + alpha id / 波号（`Claude/skills/wq-brain-ra-kor/rules/README.md:15`）。

## 1. 适用范围与硬红线

- **区域 / 宇宙 / 延迟**：KOR / TOP600 / D1。换区不适用本文件，一切数值结论（闸值、prod、天花板、判死）须重扫。
- **谱系**：仅 regular alpha。SUPER / PPA 走各自入口，不套用本章杠杆与判死结论。
- **硬红线**（任何人批准都无效）：
  1. 提交 alpha 前的用户明确确认 + `confirm_submit=True`（不可逆动作不入自动链）；
  2. 凭据（`world-quant-brain-mcp/.env`）禁止读取、打印、提交、外发；
  3. 平台条款与限额（并发、配额）——并发参数只从 `wqb.config.CONCURRENCY`（src/wqb/config.py:626）与 `wqb-concurrency` skill 取，不在文档里复写数字；
  4. 判死结论在过六维穷尽闸（§F.1）之前一律是 PROVISIONAL，不得引用为邻接先验、不得据此宣布塔 / 宇宙关闭（AGENTS.md:431-444）；
  5. prod ≥ 0.7 一律不算合格交付（用户 2026-11-16 口径，final_report.md:3）；跳闸须走 waiver 协议（AGENTS.md §8.1.2，`wqb.waiver.GATE_POLICIES`）。

## 2. 选集与体检

1. **查表选集（S-PRE）**：按 `wq-brain-campaign-matrix` 选区域 × 类别组合；数据集画像唯一登记处是
   `tracking/KOR/reference/datasets/<平台 dataset_id>.md`（命名规则 final_report.md:148-149，每集一份、手工维护）。
   开新数据集前先查该目录与附录 C——已有画像 / 判死记录的集不重复开波。
2. **数据集层穷尽闸前置**：宣称「某 category 已穷尽 / 该面封盘」前必须跑
   `python tools/gates/category_coverage_audit.py --region KOR --universe TOP600 --delay 1 --category <CAT>`（AGENTS.md:915）；
   分母只认按 (region, universe, delay) 实取的平台 `/data-sets` 全表，本地 datasets 表与 field_coverage 快照都不算分母（AGENTS.md:912）。
3. **字段体检（L1）**：画像必含覆盖率 / alphaCount（下称 **aC**，平台字段上的 alpha 数，`get_datafields` 返回；
   用法见 `tracking/KOR/reference/datasets/analyst10.md:127-130`）/ 更新频率 / 分布形态 / VECTOR 性
   （insiders5 画像格式见 `datasets/insiders5.md` §1-§3）。扫全字段必须 `filter_sharpe=false`（否则成对字段的对侧腿被隐藏，final_report.md:149）。
4. **数据集级 `coverage` 不是数据存在性判据**（AGENTS.md:918，GBR `techindi_model` cov=0 实有 399 字段反例）。
   「该集无数据」只能由 field 级实查或探针 longCount 的 fail-closed 结论给出（§F.6），画像里引用 coverage 时必须标明层级。
5. **体检硬门**：候选过 `tools/field_inspect_gate.py`（经 wave_gate 编排，§6）；gate-mode 自 2026-10-12 起 enforce（AGENTS.md §8.1.1）。

## 3. 结构设计：机制优先与降 prod 两级杠杆

（实证基础：`tracking/KOR/campaign_20261115_unlit_towers/final_report.md` §3-§4，as_of 2026-11-16。）

1. **一级杠杆 = 价差结构**（两条不同信息源的秩相减）。成立的形态是「广度/存量腿 × 噪声/分歧度腿」
   （`tnc − disp`、`label − disp`，final_report.md:125）；镜像对必须双向各测一条（W3：差一条腿符号 S 从 2.3 翻到 −2.5，waves.md:171-173）。
2. **第二腿的两个条件**：① 自身有信号；② 与第一腿**信息互补**。只有①不够——oth475 单独 S 1.61（有信号），
   与分歧度相减后掉到 1.00（waves.md:178）：出口额与内部人分歧度无互补结构，相减即抵消（final_report.md:89）。
3. **二级杠杆 = 中性化换 SLOW + decay 降到 1–2**：同一表达式只改设置，prod 0.839→0.663 实测（waves.md:217-219）；
   代价 TO 抬升、F 下降，**只对本身低换手的核成立**（label 核 d1 下 TO 60%、F 崩，waves.md:220-221）。
4. **被证伪的降 prod 手段**（不得复用）：hump + 300–900 日 `ts_decay_linear` 壳层（只削弱信号，10/10 全灭，waves.md:188-196）；
   同族分歧度相减（互相抵消，0.10/0.19）；`ghc_tr` 作第二腿（prod 抬到 0.7227，waves.md:274）。
5. **一族一席**：同机制（含同族窗口变体）只能交付 1 颗。窗口变体本质是同一信号——一颗上线，整族 prod 一次性抬到 0.7+
   （W9 实证：6 颗同时失效，waves.md:317-339）。这是交付纪律，不是建议。
6. **结构选型速查**（final_report.md §4）：中性化 SLOW、decay 1–2、分歧度第二腿 `vol_af` ≥ `vol_chg` ≫ `ghc_tr`、
   label 期限 5 日（20/60 日的 2Y 掉到 1.45–1.54）、分组轴 sector。

## 4. 开波与收批判闸

1. **每波三问**（铁律 G，waves.md:3）：继承（上一波结论）/ 准入（字段族白名单 + 禁入清单）/ 收窄（本波规模）。
   禁入清单逐子族写明依据（waves.md:104 形态），禁止整数据集一刀切。
2. **开波门禁**：`tools/wave_gate.py`（8 闸 + 体检硬门 + 多样性闸，参数见 §6）；区域闸（signal_floor / stop_rules / backlog）
   enforce 拦截 exit 2，放行须 waiver（AGENTS.md §8.1.1-8.1.2）。
3. **批量回测**：只用 MCP `create_multi_simulation(alpha_expressions=[...])`（参数名逐字，AGENTS.md §8.2）；
   ≥2 条一批，单条补 control。派发前过 `preflight_expressions(alpha_expressions=[...])`——
   ⚠ 它只查字段存在性与 VECTOR 包裹建议，**不查「裸 VECTOR 参与算术算子」**；一个算术算子的直接实参里出现未 `vec_*` 的
   VECTOR 字段必错，且 multisim 一条解析失败会把同批其余条目整批 CANCELLED（waves.md:64-72）。
4. **收批**：`batch_status(simulation_ids=[...])` → `batch_get_alpha_metrics` + `get_alpha_details`（后者拿平台 `code` 核对臂归属）。
   队列拥塞期 `harvest_multisim_alphas` 可能对刚跑完的 multisim 返回 404——不要重试等待，走 batch_status 回读（AGENTS.md §8.2）。
5. **判定口径**：`failed_ra_count` = `wqb.config.compute_webdata_failed_counts`（RA 18 项，result 非 PASS/PENDING 即计，
   **WARNING 也算 failed**——平台侧同样成立，`LOW_INVESTABILITY_CONSTRAINED_SHARPE` 1.99 vs 2.02 warning 实测 waves.md:34-35）。
   2Y 闸 = `PLATFORM_CHECK_LINES["low_2y_sharpe_min"] = 1.58`（src/wqb/config.py:545）；IS 闸 `LOW_SHARPE` 平台线 Delay-1 为 1.25（config.py:542）。
6. **prod 读数纪律**：缓存只保证 48h 不过期、不保证生产池没变；交付前必须 `refresh=True` 逐颗回源（W9：MP65Lx5k 2–5 小时内
   0.5285→0.9984，waves.md:338-339）。塔位 / 席位复核用 `get_pyramid_alphas()`（tools_account.py:112-113）。
7. **波次台账**：读数与归因落 `tracking/KOR/campaign_*/waves.md`（追加不覆盖）；结构化结论经 `upsert_wave_result` /
   `upsert_expressions` / `upsert_backtest_rows` 入库（AGENTS.md §8.6-8.8），禁止 Agent 直写 `tracking/*/candidates|results/*.json`。

## 5. 交付与回写

交付清单（`DELIVERY_*.md`）必须逐颗含 R1–R5：

- **R1 验收口径**：① 平台 `checks` 的 fail 与 warning 全空（`failed_ra_count=0`）；② `check_correlation(production, refresh=True)`
  当日回源实测 prod < 0.7（严格不等式）。两项缺一即不入清单。
- **R2 近十年闸**：逐颗 `get_alpha_yearly_stats` 核逐年 `longCount>0 && shortCount>0 && pnl>0`（AGENTS.md §7.5 闸3；
  final_report.md:136）。只看全期指标会把「数据不满十年」的 alpha 误当优质候选。
- **R3 席位表**：按机制族分席、每席标注颗数与提交首选（DELIVERY:25-34 形态）；同席其余件标「替补——首颗提交后 prod 将抬到 0.7+」（一族一席，§3.5）。
- **R4 贴线 / 池漂移风险件标注**：prod 在 (0.65, 0.70) 区间的件（内部预筛严线 `GATES_INTERNAL["prod_corr_max"]=0.65`，src/wqb/config.py:534；
  平台运行时闸 `GATES_PLATFORM["prod_corr_max"]=PRODCORR_CEILING=0.70`，config.py:512、:556）必须在交付清单中标注为
  **「贴线/池漂移风险件」**，字段：alpha id、prod 值、回源时间戳、距 0.65 的缓冲量。依据：config.py:532-533 注释
  （「挡住『提交时贴线过、48h 后池漂移翻闸』的件，实证 78LpqZYQ 0.697」）+ W9 池漂移实证。
- **R5 回写**：合格件经 `upsert_backtest_rows` / `upsert_expressions` 入库（stage、prod_corr_source、corr_checked_at 随行写；
  合并式写入，没带不等于清空，AGENTS.md §8.8）；判死 / 停投结论按 §F 落档。提交权归用户，清单不含提交动作。

## 6. 可执行清单（命令级）

```bash
# —— 选集 / 体检（第 2 章） ——
python tools/gates/category_coverage_audit.py --region KOR --universe TOP600 --delay 1 --category <CAT>
#   EXHAUSTED(exit 0) 才可宣称穷尽；argparse 实测 tools/gates/category_coverage_audit.py:444-448（--region 必填）
python tools/gates/audit_dataset_coverage.py --region KOR --universe TOP600 --delay 1 --cache <audit.json> --md <audit.md>
python tools/gates/category_coverage_audit.py --region KOR --universe TOP600 --delay 1 --category <CAT> --field-audit <audit.json>
#   field 级背书两命令成对跑（AGENTS.md:919）；只有 TESTED / NO_DATA 算已排除
python tools/probe/dataset_data_probe.py --region KOR --universe TOP600 --delay 1 --datasets <DS> --out <probe.json>
#   缺省 --neutralization NONE（longCount 直接等于有数据的股票数）；argparse 实测 tools/probe/dataset_data_probe.py:267-279

# —— 开波门禁（第 4 章） ——
python tools/wave_gate.py --campaign-dir tracking/KOR --dataset <DS> --wave <N> --candidates <json> [--from-db] [--gate-mode enforce]
#   argparse 实测 tools/wave_gate.py:889-912

# —— 批量回测（MCP wq-brain-http；参数名逐字） ——
# preflight_expressions(alpha_expressions=[...])
# create_multi_simulation(alpha_expressions=[...])          # ≥2 条一批，单条补 control
# batch_status(simulation_ids=[...])                        # 收批；404 兜底通路
# batch_get_alpha_metrics(...) + get_alpha_details(...)     # 指标 + 平台 code 核对臂归属

# —— prod 终验 / 塔位（第 4-5 章） ——
# check_correlation(alpha_id=..., correlation_type="production", refresh=True)
#   签名 world-quant-brain-mcp/tools_corr.py:8-13；refresh 跳缓存并跳预读 :36-37；
#   platform_unavailable / pending ⇒ 不判死、不写已通过，按 retry_after 重查 :39-46
# get_pyramid_alphas()   # 塔位/席位复核，tools_account.py:112-113
# get_alpha_yearly_stats(...)   # R2 近十年逐年核

# —— 判死（§F 全流程；两步顺序不可倒） ——
python tools/forum_recon.py --question "<判死决策问题>" --context "region=KOR,dataset=<DS>" --out negative --limit 3
#   负结果落 ledger `forum_recon_negative_<qkey>`（qkey=10 位 hex；tools/forum_recon.py:17、:537-546）
# seal_dead_end(region="KOR", entry_id="<id>", family="<族>", reason="<读数区间>", rule="<判据>",
#               wave_numbers=[...], forum_recon={"question_key": "<qkey>", "found": false, "status": "no_result"})
#   签名 wqb_db_mcp.py:2529-2540；闸按 question_key 回 ledger 核对，缺上游取证记录 ⇒ 拒绝且不沉降、不写库（AGENTS.md:907）

# —— 回写（MCP wqb-db） ——
# upsert_wave_result / upsert_expressions / upsert_backtest_rows
```

并发与批次常量只从 `wqb.config` 取：`CONCURRENCY`（src/wqb/config.py:626）、`BATCH_SIZE=4`（config.py:511）；
并发纪律见 `wqb-concurrency` skill。MCP 参数名速查：表达式数组一律 `alpha_expressions`、`batch_status` 要
`simulation_ids`、`harvest_multisim_alphas` 要 `multisimulation_location`（AGENTS.md §8.2，参数名错在本地 PTC 层即报错）。

## 7. 附录：已判死清单与 ATOM 结论

> as_of 2026-11-16；适用范围 KOR/TOP600/Delay=1（换区一律重扫，SKILL.md:36、:124）。本章所有平台读数转引自战役四文件
> （`tracking/KOR/campaign_20261115_unlit_towers/` 下 waves.md / final_report.md / DELIVERY_20261116.md / ATOM_20261116.md）
> 的自述读数，2026-11-16 会话未重新上平台复核；2026-11-17 落盘会话实跑过的机器核验（config 常量、MCP 签名、KOR metrics
> 缓存统计、判死工具 argparse、战役四文件行号抽查）在引用处标明。

**术语约定（本章通用）**：
- **「RA 全过」** = 平台 RA 闸无 fail 也无 warning（`failed_ra_count=0`）；
- **「全灭」** = 该批 0/N 条过闸（两个词不得混写；旧稿「全闸」两义，已按此拆分）；
- **aC** = alphaCount，平台字段上已存在的 alpha 数（`get_datafields`；用法 analyst10.md:127-130）；
- **prod** = `check_correlation(production)` 读数；**2Y** = `LOW_2Y_SHARPE` 读数（闸 1.58，config.py:545）。

## A. insiders5 内部已停投子族与读数

| 子族 | 字段 / 覆盖 | 读数（S 除非注明） | alpha id | 判决性质 |
|---|---|---|---|---|
| 库藏股 `insd5_trsy_*` | cov 0.8728（waves.md:46） | 四几何 −0.60…0.44：水平 0.29 / 126d 变化 0.44 / 分歧度 **−0.60（反向）** / ts_rank-504 0.28；叠加 wave185 `ts_delta(trsy_ratio,252)` max\|S\|=0.81 | `KPg892o1` / `XgalnO0X` / `akaPngpO` / `E5QaE2dR`（waves.md:78-81、92） | 信号层停投：本区库藏股无信号（waves.md:91-93）；分歧度是反向弱效应、强度不足以单独成腿 |
| 去重缺口 `source_real_ratio` / `source_ratio` | cov 0.9995（waves.md:46） | 比例口径与股数口径 4 条全部 **S=0.00 / TO=0.00 全空仓** | `vRAzloQb` / `rK7zlnZ3`（waves.md:82-83）、`9ql67YJx` / `gJaP963O`（waves.md:120-121） | **数据层排除**：KOR DART 不做父子/关联方去重、两列物理恒等（waves.md:94-96、130-131）——不是信号弱；⚠ 明写不可外推 IND/USA，去重逻辑不同须重测（waves.md:131） |
| 持有人结构（编码字段 `rpst_grp_typ` / `officer`） | — | 四臂 −0.21 / −0.60 / 0.29 / −0.84 | `E5Qae1qG` / `P05lONnL` / `pwazKm8g` / `A1xa79kw`（waves.md:116-119） | 机制层停投：编码类名义变量只作**分组轴或门控**、不做信号（waves.md:128-129） |
| 所有权变化（关系方家数变化率等） | — | 变化率最好 0.88（`KPg8E3bj`，waves.md:125）；`tnc` 存量 `Xg9vxXrb` S 1.59 **不在本行判决内**（见下） | waves.md:125、132 | 变化率几何不达闸（信号层停投） |

- **行 4 澄清**（回应「1.59 『有效』与『死』矛盾、去向不明」）：判死对象是**变化率几何**（0.88 不达 1.58）。
  `Xg9vxXrb` 是 `tnc` **存量**（非变化率）：S 1.59 过 IS 闸、2Y 1.84，但 **prod 0.9686 撞墙**（waves.md:22）⇒ 属 D 表
  「RA 全过但 prod 撞墙」库存，从未是判死对象；且 W3 归因 3 指出 tnc 正确形态是价差（单独 1.59 → 减分歧度后 2.03，
  waves.md:179-180）。tnc 价差族 6 颗窗口变体已因一族一席在 W9 集体失效（waves.md:317-339）——该 alpha 的现行状态 =
  库存（prod 撞墙 + 同族席位被占），既不在交付清单也不在待验清单。
- **粒度声明**（回应「与 F.3 六维闸矛盾」）：本表 4 行均为**子族级「停投」结论**（波次台账 PROVISIONAL 形态，
  waves.md:104），每行实测臂 4–5 条 < 六维闸 D1 的 ≥10 要求，**不构成数据集终判死**；insiders5 数据集层现状见 F.2
  （PROVISIONAL，仅「不再投仿真配额、仅保留收割」可引用）。B 表各行同理，是**机制级停投**（waves.md:184、385 台账
  「不再投」条目），不是 seal 终判死。
- **行 1 / 行 3 读数重复核实**（回应「疑似转写复制」）：行 1 四值与 waves.md:78-81、行 3 四值与 waves.md:116-119
  逐条相符（2026-11-17 落盘会话核验）；−0.60 与 0.29 两处重现是**不同 alpha id 的实测巧合**（`akaPngpO`/`P05lONnL`
  同为 −0.60，`KPg892o1`/`pwazKm8g` 同为 0.29），非转写复制。
- **覆盖声明**（回应「9 子族只枚举 4 个」）：本表只列**已停投**的 4 个子族。「9 子族 × 2 波」的完整子族清单与逐字段读数
  登记在 `tracking/KOR/reference/datasets/insiders5.md`（§2 五族分类 + §9 本轮补测，final_report.md:144），含未停投的
  交易流量族（唯一出货面，prod 已撞墙，见 D 表行 3）。
- **产出物**：子族级禁入写进下一波「继承/准入」（waves.md:104 形态）；数据集层现状 = 不再投仿真配额、仅保留收割
  （waves.md:134-135）。
- **失败分支**：把去重缺口写成「信号弱」会错杀其它区的同族（该结论仅 KOR 成立）；把持有人结构编码字段拿去做算术会在
  经济上不成立（waves.md:128 已实测印证）。
- 复核判死标记（只取证据列表、不作终判）：`get_dead_datasets(region="KOR")`（wqb_db_mcp.py:499）、
  `get_dead_ends(region="KOR")`（wqb_db_mcp.py:333）。

## B. 机制级已证伪清单（不得再投任何配额）

| 机制 | 读数 | 证据 |
|---|---|---|
| PV×ANALYST 价差 | 3 条 S = **−0.12 / 0.05 / −0.03**（全灭） | `WjladrgZ` / `RRe2Yxpb` / `WjladrpZ`（waves.md:365-367、377；DELIVERY:57） |
| OTHER×ANALYST 价差 | 2 条 S = **1.00 / −0.07** | `78YaQP1x` / `1YWaL3dW`（waves.md:368-369、379；DELIVERY:58） |
| 同族分歧度相减 | S 0.10 / 0.19（互相抵消） | `mLaz5we5` / `xAvzNOXl`（waves.md:161-162、177-178、184） |
| oth475 作价差第二腿 | −1.05 / 1.00（**有信号但不互补**：oth475 单独 S 1.61 → 相减后 1.00） | `1YWmpkVk` / `KPg8GlYx`（waves.md:164-165、178；final_report.md:89） |
| hump + 300–900 日 `ts_decay_linear` 壳层 | **10/10 全灭**，S 0.38–1.40（最好 `leaR06x8` 1.40 / `Jj85d0lO` 1.36） | waves.md:188-196；DELIVERY:60 |
| anl10 换字段（sales/BPS/EBT/EBIT/DPS/capex/FY2/FQ1 等 10 字段） | **0/10 过闸（全灭）**；最好 `xAvmnWrq` S 1.63 / 2Y 1.41（2Y 差 0.17），其余 S 0.74–1.29；有信号的只有 `anl10_smartest_pre_fy1_pred_surps_v1` 本身 | waves.md:224-235；DELIVERY:61 |

- **hump 行读法**（回应「『label 核 2.82→0.58』无法解读」）：动作 = 给强核加 `hump + 长 decay` 壳层，对比加壳前后的 S。
  「2.82→0.58/0.76」= label 概率差核（dl_riskfree）加壳前 2.82、加壳后 0.58 与 0.76 两种壳层读数（waves.md:195）；
  2.82 的原始出处未在战役四文件内注明，转引时保留原样并注此处。「均 2 项 RA 未过」（`leaR06x8`/`Jj85d0lO`）——
  具体项名 waves.md 未记录，两 id 亦不在本地 metrics 缓存（2026-11-17 实查 95 份缓存无此二件），无法补列，转引时不得据此断言是哪两项。
- **oth475 行教训改写**（回应「『第二腿必须自身有信号』解释不了 1.61→1.00」）：该行原证据恰是**反例**——oth475 有信号
  （1.61 > 1.58）却仍拖累。正确规则 = §3.2 的两条件：第二腿须**自身有信号且与第一腿信息互补**（广度/存量 × 噪声/分歧度）；
  oth475（出口额）与 insd5 分歧度无互补结构，相减即抵消。
- **产出物**：波次台账「不再投」条目（waves.md:184、385）+ DELIVERY:53-61 判死记录表。
- **失败分支**：把 hump+长 decay 壳层当「降 prod 手段」复用——它只削弱信号、不是低 prod 的来源（waves.md:194-196）。
- 附带工程坑（同批连坐）：裸 VECTOR 字段进 `divide` ⇒ 同批 10 条整批 CANCELLED；`preflight_expressions(alpha_expressions=[...])`
  只查字段存在性与 VECTOR 包裹建议、不查「裸 VECTOR 参与算术算子」（waves.md:64-72）。

## C. ATOM 侧逐集判决（ATOM_20261116.md:35-41）

| 数据集 | 实测臂 | 读数 | 判决 |
|---|---|---|---|
| other496（ARD 年报 104 字段） | 10 条（ATOM:35） | 最好 `gJaRVP3g` S 1.54 / F 0.81（3 项 RA 未过，项名未记录）；其余 S −0.8…0.24 | 不达闸（最好 1.54，差 0.04）——**非「无信号」**，与 fa_tr 1.56 同一定性口径 |
| other545（NEMO 2.0 网络动量） | 10 条（ATOM:36） | S 0.16–0.49 | 无信号（\|S\| 近零） |
| other327（美债收益率敏感度） | 10 条（ATOM:37） | S 0.16 / −0.34 | 无信号（\|S\| 近零） |
| other436（股息削减概率/股息率） | 10 条（ATOM:38） | S ≤0.26 | 无信号（\|S\| 近零） |
| news59 | 字段构成核查（非信号臂） | 只有「财年」「事件时间」2 个日历字段；aC 1458–1628（平台重度使用） | 不可行（字段构成） |
| news73（Dow Jones 情绪） | 字段核查（非信号臂） | **数据集级** coverage 0.269（ATOM:40 转引）+ 塔级已判死 | 不可行；⚠ 数据集级 coverage 不可单独作「无数据 / 截面太薄」判据（AGENTS.md:918、§F.6），此处只作塔级判决的佐证 |
| earnings3 | 前序波次（wave186） | max\|S\|=0.94 / F 0.49，机制性衰减（unlit_tower_category_profile.md:36）；天花板 0.95（composite_route_20261030.md:4——**「0.95」的出处**） | 前序判死（per-dataset 档案指针见下） |
| sentiment26 | 前序波次（wave216） | max\|S\| 0.20 + 数据 2017 起（datasets/sentiment26.md §7.2） | 前序判死 |
| macro63 | 前序波次 | 恒空仓（10/10 年 longCount=0，kor_session_lessons_20261031.md:223） | 前序判死 |
| imbalance5 | 前序波次 | 2Y 结构性不可达（3 形态 2Y≈0.17，unlit_tower_category_profile.md:42） | 前序判死（未 seal，待走 §F 流程） |
| socialmedia* | — | ATOM:41 转引「前序波次已判死」 | ⚠ 2026-11-17 落盘会话未在 `tracking/KOR/reference/` 下定位到 socialmedia 逐集判死档案指针；引用前先回 `unlit_towers_roadmap_20261030.md` / `unlit_tower_category_profile.md` 核对该塔关闭证据 |
| PV 数据集内部 `corr_*_with_slippage` 6 字段 | 6 条 | S −0.94…0.17（全灭） | 同一数据集内配对必须「价格侧 × 深度侧」、不能「价格侧 × 滑点」（ATOM:50） |

- **通配符行拆分说明**（回应「跨集外推」）：原稿把 earnings3/sentiment*/macro*/imbalance5/socialmedia* 并成一行「已死」，
  现按 F.4「回读实测行」拆出逐集指针如上；各集判死依据不同（信号衰减 / 覆盖起步晚 / 恒空仓 / 2Y 不可达），不得互相外推。
  socialmedia* 因指针缺失单独降级为「待核」。
- **产出物**：逐集判决行追加进 `ATOM_20261116.md` §三（追加不覆盖，`Claude/skills/wq-brain-ra-kor/references/_field-profile-and-templates.md:188` 维护约定）。
- **失败分支**：把 news59/news73 的「不可行」写成「判死信号」——news59 是字段构成不可行（仅 2 个日历字段），news73 是
  薄截面佐证 + 塔级已判死的组合，两者都不是信号层证据；「该集无数据」必须走 §F 的 field 级命令。

## D. 「死」与「拥挤」必须分开（不得互相归并）

| 对象 | 读数 | 定性 | 正确动作 |
|---|---|---|---|
| dl_riskfree_returns | S/2Y 达标（最好 2.33–3.00），**RA 全过但 prod 0.82–0.87**（ATOM:33）；⚠ 该族部分件 investability 落 warning ⇒ failed_ra=1（waves.md:35、100），「RA 全过」仅指 ratio 高的子集（waves.md:106） | prod 撞墙：有信号、席位被占 | 按 investability 逐颗筛（只有 ratio 高的才 RA 全过）；**不得归入判死** |
| oth475 | RA 全过，但 prod 0.83（`rKRLLzRa` 实读 **0.8284**，waves.md:18；ATOM:34） | 同上 | 转「只收割」（价差路线已被 B 表证伪） |
| insiders5 纯分歧度族 | RA 全过，但 prod 0.84–0.97（`3qokqkZQ` 0.8495 / `xArVj27g` 0.9532 / `akKQjYR5` 0.8400，waves.md:19-22） | 同上 | **只收割；新仿真配额停投（A 表）**。⚠ 原「换杠杆降 prod（价差/SLOW+低 decay）」两条路线均已被本轮实测证伪：壳层 B 表 10/10 全灭、同族相减 0.10/0.19；tnc 席已被占（W9）、label 席已交付（DELIVERY A 席）——分歧度作第二腿的出路只剩与 PV 相关腿组合（W11 已交付，DELIVERY B 席），分歧度单腿族本身无新杠杆 |

- **W0「46 条」澄清**（回应「W0 未定义、46 条无出处」）：W0 = 收割波（waves.md:7），首批把本地 343 条 KOR RA 全过件去重成
  164 族、取 **18 条**上平台复验（waves.md:9-10）；**46 条**是全战役平台核验总数（waves.md:312）。
  「prod 撞墙但 RA 全过」库存是收割优先的来源（AGENTS.md §7.5 收割先于重挖）。
- 混淆后果：把拥挤写成判死 ⇒ 永久放弃仍在出货的族；把判死当拥挤 ⇒ 对 −0.60…0.44、S=0.00 空仓这类无信号面反复烧仿真配额。
- **产出物**：台账里两列分记——判死走 §F 的 seal 流程；拥挤只记 prod 读数 + 「待杠杆/只收割」状态（waves.md:134-135 的配额结论形态）。
- **失败分支**：引用他人台账时只看 `dead`/`family_dead_datasets` 标记不复核实测（AGENTS.md:428 明令不得单独作依据；
  waves.md:18 与 ATOM:33-34 就是必须回读的实测）。

## E. ATOM 活矿脉、天花板与待验件

**唯一活脉 = PV 日内价量相关**（ATOM:8-15）：

- 机制模板：`subtract(0.5, group_rank(ts_mean(corr_X_with_Y, 22), industry))`——日内「价格 × 挂单深度」相关性取反；
  价量同向度高 = 追价需求冲击、同向度低则后续强（修复期数日–数周）（ATOM:14-15）。
- 设置统一：SLOW · decay 2 · trunc 0.08 · nan OFF（ATOM:25）。
- 已交付 1 颗：`ZYQ116ln`（`corr_bid_price_with_bid_size`）S 1.86 / F 1.10 / TO 22.1% / 2Y 1.80 / **prod 0.6981**（DELIVERY:21、ATOM:19）。
- 待验 4 颗：`E5QgnpaG` 1.98 / `RRe2xbYa` 1.91 / `0mPeZXQ1` 1.85 / `npaZGdOw` 1.84（S 区间 **1.84–1.98**，ATOM:20-23），
  prod **「待验」**——平台相关性服务熔断未测（ATOM:57）⇒ **不得写成「已通过」**。「DELIVERY 里 PV 单腿只有 1 颗」
  指席位表 D 席（PV 单腿）仅 `ZYQ116ln` 一颗（DELIVERY:32、:40）；B 席 6 颗是 PV×INSIDERS 价差，不属单腿席。
- 一族一席：5 颗 price × depth 同族，实际只能提交 1 颗、其余为替补（ATOM:26）。
- **贴线件标注**：`ZYQ116ln` 0.6981 与 `78LpqZYQ` 0.6970 两件过平台闸 0.70 但超内部严线 0.65
  （`PRODCORR_CEILING = 0.70`，src/wqb/config.py:512；`GATES_INTERNAL["prod_corr_max"] = 0.65`，config.py:525、:534，
  注释原文以「78LpqZYQ 0.697」为池漂移实证——**78LpqZYQ 不是历史例证，是本战役 DELIVERY 第 10 颗**
  （C 席·分析师惊奇−分歧度，DELIVERY:20；W0 收割表 waves.md:16；W9 回源 0.6970 稳定 waves.md:325））
  ⇒ 交付清单中必须按本 SOP **R4** 条目（§5）标注为「贴线/池漂移风险件」，字段：alpha id、prod 值、回源时间戳、距 0.65 缓冲量。
  0.65 当前是研究期本地预筛口径（config.py:524「内部严线——研究仿真阶段即要求，用于省配额的本地预筛」），
  运行时提交闸消费的仍是 0.70（`GATES_PLATFORM["prod_corr_max"] = PRODCORR_CEILING`，config.py:556）。
- `insd5_fa_tr` 分歧度族天花板：两轮 20 臂（窗口谱 + decay）**≈ S 1.56**（`ZYajReQx`，REV&MOM · d12 · 55/sector，
  F 1.34 / 2Y 2.15；基线 `9qx8OzXe` d4·55/sector 1.54，ATOM:67-68），距 KOR `LOW_SHARPE = 1.58` 差 **0.02** ⇒
  作为 ATOM 不达闸；**不应继续扫窗/扫 decay 硬凑（属曲线拟合，ATOM:74）**；prod 未测且因 S 不过闸测得无意义（ATOM:78）。
- **1.58 的机器核验**（2026-11-17 落盘会话，python 结构化统计 `tracking/KOR/cache/metrics/*.json` 共 **95 份**）：
  `LOW_SHARPE limit=1.58` ×**95**（全部）；`LOW_2Y_SHARPE limit=1.58` ×**88**；`IS_LADDER_SHARPE` ×**7**
  （其中 limit=1.58 ×4、limit=None ×3——None 是缓存行缺 limit 字段，非闸值不同）。
  ⚠ 88 + 7 = 95：**每份缓存恰有 LOW_2Y_SHARPE 与 IS_LADDER_SHARPE 之一**（7 份无 LOW_2Y 者正是 7 份有 IS_LADDER 者，
  实查清单 `3qoYN0e0/JjeR9wNA/LLMOYEq2/LLMbQKd1/P0ojRYJp/npvwje1q/xArwZvdw`）⇒ **2Y 闸 1.58 在 95/95 份中成立**
  （经两个检查名之一），B 表 anl10 行「2Y 差 0.17」以 1.58 为前提是安全的。
- 待验件转正的唯一途径（产出物 = 回源 prod 值记入 DELIVERY/ATOM）：
  `check_correlation(alpha_id="E5QgnpaG", correlation_type="production", refresh=True)`（入参名与
  world-quant-brain-mcp/tools_corr.py:8-13 签名一致，2026-11-17 实读核验；refresh=True 跳缓存并跳预读，tools_corr.py:36-37）。
  **失败分支**：返回 `status=platform_unavailable` / `pending` ⇒ 不判死、不写已通过，按 `retry_after` 稍后重查（tools_corr.py:39-46）。
  塔位/席位复核用 `get_pyramid_alphas()`（tools_account.py:112-113）。

## F. 引用判死结论的纪律

1. **六维穷尽闸 D1–D6 是前置门**（AGENTS.md:431-444）：D1 结构互异模板 ≥10 / D2 字段族自测 / D3 矩全家 / D4 分组轴 ≥2 /
   D5 非线性 ≥1 / D6 配置 ≥2；缺任一维 ⇒ 只能记 **PROVISIONAL**，不得引用为邻接数据集/族的先验，不得据此宣布塔/宇宙关闭
   （AGENTS.md:433）。判死结论必须写「结构性 / 可修复 / 数据层排除」分层（AGENTS.md:444①；
   `Claude/skills/wq-brain-ra-kor/rules/README.md:15`）。
2. **insiders5「9 子族 × 2 波穷尽 ⇒ 封盘」现只能记 PROVISIONAL**（as_of 2026-11-16）：waves.md:134-135 只有陈述、
   无 D1–D6 逐维举证；可以引用的正确表述是「不再投仿真配额、仅保留收割」，不是「数据集终判死」。
3. **探针（<10 条）只输出「继续/停止加注」，不产生判死**（AGENTS.md:444②）；DEU 首例 risk60「探针不判死」
   （`tracking/DEU/atom_orthogonal/DEATH_AUDIT_20261110.md:67`）。与 A/B 表的关系见 A 表粒度声明：2–5 条臂只能支撑
   **子族/机制级停投（PROVISIONAL）**，不能支撑 seal 终判死。
4. **台账 `dead` / registry `family_dead_datasets` 标记不得单独作依据**（AGENTS.md:428）；判死标记是检索起点，
   动作前必须回读实测行（本附录 A–D 各表即实测行）。
5. **撤判在同一档案追加、不得新开口径**（AGENTS.md:444④）；先例 = DEU atom_orthogonal 的 risk60/risk88 撤判重开
   （DEATH_AUDIT_20261110.md:11-12）。
6. **「该集无数据」必须是 field 级实查或探针 longCount 的 fail-closed 结论**（AGENTS.md:918、:923）：读不到
   `longCount/shortCount` ⇒ `data_present=null` + `PROBE_FAILED`，绝不许写成「没数据」。

固定命令面（按序执行；第 1 步是第 2 步的前置取证，缺第 1 步第 2 步必被闸拒绝）：

1. **论坛取证（上游，必须先跑）**：`python tools/forum_recon.py --question "<判死决策问题>" --context "region=KOR,dataset=<DS>" --out negative --limit 3`
   ——负结果（`found=false` / `status=no_result`）落 ledger `forum_recon_negative_<qkey>`（qkey = 10 位十六进制，
   由问题文本派生；tools/forum_recon.py:17、:537-546，2026-11-17 argparse 实测）。故障结局（`status=error`）不落负缓存、不入判死。
2. **正式判死唯一入口（fail-closed）**：`seal_dead_end(region="KOR", entry_id="<id>", family="<族>", reason="<读数区间>",
   rule="<判据>", wave_numbers=[...], forum_recon={"question_key": "<qkey>", "found": false, "status": "no_result"})`
   （签名 wqb_db_mcp.py:2529-2540；闸按 `question_key` 回 ledger 核对——**`<qkey>` 就是第 1 步返回并写入台账的那条记录的键**，
   缺上游取证记录时闸拒绝且**不沉降、不写库**，AGENTS.md:907）。绕过只有 `force_seal=True` / `require_forum_recon=False`，
   必须人工确认并留痕。
3. **数据集层穷尽性闸**：`python tools/gates/category_coverage_audit.py --region KOR --universe TOP600 --delay 1 --category <CAT>`
   → `EXHAUSTED`(exit 0) 才可宣称穷尽（AGENTS.md:915；argparse 实测 tools/gates/category_coverage_audit.py:444-448，--region 必填）。
4. **field 级背书（两命令成对跑）**：`python tools/gates/audit_dataset_coverage.py --region KOR --universe TOP600 --delay 1 --cache <audit.json> --md <audit.md>`，
   再 `python tools/gates/category_coverage_audit.py --region KOR --universe TOP600 --delay 1 --category <CAT> --field-audit <audit.json>`
   （AGENTS.md:919）；只有 `TESTED` / `NO_DATA` 算已排除。
5. **探针执行器**：`python tools/probe/dataset_data_probe.py --region KOR --universe TOP600 --delay 1 --datasets <DS> --out <probe.json>`
   （缺省 `--neutralization NONE`，argparse 实测 tools/probe/dataset_data_probe.py:267-279）；产物经
   `audit_dataset_coverage.py --probe-results <probe.json>` 回灌为 `TESTED` / `NO_DATA`。
6. **绝对措辞门**：报告出现「穷尽 / 上限 N 席 / 不再有未探轴」时附近 4 行内必须有 scope，否则
   `python tools/gates/audit_dataset_coverage.py --lint-report <报告.md>` exit 1（AGENTS.md:920）。
- **产出物**：判死档案（含 D1–D6 逐维举证表）+ `seal_dead_end` 沉降记录；未过六维闸的只落波次台账 PROVISIONAL 行。
- **失败分支**：跳过 `seal_dead_end` 用低层写入口判死（闸不覆盖）；用「cov<0.6 剔除」类数据集级判据（已被 GBR 实证证伪并被
  `python tools/gates/audit_dataset_coverage.py --lint-skills` 登记为历史欠账，AGENTS.md §8.11 ⑥）；把 PROVISIONAL 行当邻接先验
  引用到下一数据集。
