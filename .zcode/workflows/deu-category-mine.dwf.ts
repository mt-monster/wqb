/* zcode-workflow
description: "DEU 类别挖掘战役：S0 盘点选目标集 → 每波（臂表设计≤10臂 → 预检/静态闸 → 串行 multi-sim 派发收割 → 逐臂归因落档）→ 条件触发（近闸 prod 探针、提交链五道闸、破闸网格精修≤3轮、卡点论坛取证、判死前覆盖审计+六维闸、杠杆入册）→ 日终矩阵。全闸通过候选停在「待用户确认」，提交 POST 不在工作流内执行。"
whenToUse: "要在指定区域按类别推进 alpha 挖掘波次，且必须遵守 multi-sim 并发≤2、相关性账号级单槽、每波≤10臂、提交需用户确认等账号级/红线约束时。"
args:
  region:
    type: string
    description: "战役区域，全程不换区（换区需新战役授权）"
    default: DEU
  category:
    type: string
    description: "S0 类别盘点的分母口径"
    default: FUNDAMENTAL
  dataset:
    type: string
    description: "指定目标数据集 id；留空由 S0 按机制先验+历史臂数+判死闸距离选定（换集须出具理由）"
    default: ""
  max_waves:
    type: number
    description: "波次上限（含网格精修轮；硬上界）"
    default: 5
*/

// 元数据块只收 description/whenToUse/args：name 由文件名（deu-category-mine.dwf.ts）给、
// scope 由所在目录给（.zcode/workflows/=project）——实测写 name/scope 会被 ListSavedWorkflows
// 以 invalid_metadata: Unrecognized key(s) 'name','scope' 拒收，整个文件静默失效（2026-11-14 修复）。
// ───────────────────── 参数收窄（args 值为 unknown，先收窄） ─────────────────────
const region = (String(args.region ?? "DEU").trim() || "DEU").toUpperCase();
const category = String(args.category ?? "FUNDAMENTAL").trim() || "FUNDAMENTAL";
const requestedDataset = String(args.dataset ?? "").trim();
const maxWavesRaw = Number(args.max_waves);
const maxWaves =
  Number.isFinite(maxWavesRaw) && maxWavesRaw >= 1 ? Math.min(Math.floor(maxWavesRaw), 10) : 5;
const ARCHIVE_DIR = `tracking/${region}/atom_orthogonal`;
const PROD_CEILING = 0.7; // 提交红线=config.PRODCORR_CEILING（src/wqb/config.py:502 实测 0.70）
const CHART_GATE = 1.58; // 图表参考线：DEU 提交路径 S 实例值，仅展示用
const MAX_SWITCHES = 3; // 换集上限（每次换集须出具理由）
const MAX_GRID_ROUNDS = 3; // 网格精修轮数上限
const GRID_DIMS = ["带宽", "std", "decay"]; // 收敛判据要求全维度扫完
const SETTINGS_LINE = `${region}/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nan_handling ON/maxTrade OFF/FASTEXPR（maxTrade 全域固定 OFF 不可开启——commit acd4452；TOP500/SUBINDUSTRY 为 DEU 标定缺省，其他区域先按区域 profile 核对）`;
const TOOL_LOADER =
  "先用 LocalToolSearch 以 select:<工具名逗号清单> 加载 MCP deferred 工具的 schema，再经 DeferredToolCall 逐个调用；不凭记忆猜参数名。";
const HONESTY =
  "若指令互相矛盾、闸无法通过或工具持续失败，escalate 并如实说明，不要绕过、不要编造读数或档案。";

// ───────────────────── 结果类型（全部带 JSDoc） ─────────────────────

/** S0 盘点结论。 */
interface SurveyResult {
  /** 选定的目标数据集 id（如 fnd90）；类别内无值得开的目标集时空串。 */
  targetDataset: string;
  /** 一句话机制假设，驱动臂表设计。 */
  mechanismHypothesis: string;
  /** 判读基准：S/2Y/sub/TO 预期、符号指纹（衰减对称=机制在/符号错）。 */
  readingBaseline: string;
  /** 本轮排除面：集 id + 排除理由（判死标记只作参考不作唯一依据）。 */
  excluded: string[];
  /** S0 产物文档路径（S0_DATASET_SCAN_*.md）。 */
  docPath: string;
  /** 类别内是否还有其他值得开的目标集。 */
  moreTargetsRemain: boolean;
}

/** 单臂规格。 */
interface ArmSpec {
  /** 臂序（1 起，收割归因键）。 */
  index: number;
  /** FASTEXPR 表达式。 */
  expression: string;
  /** 一句话：这臂检验什么（换轴/换分母/反号/乘法交互/bucket 条件化/存在性探针）。 */
  intent: string;
  /** 是否存在性探针臂（VECTOR vec_avg 包裹；只作存在性判断，不作覆盖度读数）。 */
  isProbe: boolean;
}

/** 每波臂表。 */
interface ArmTable {
  /** 目标数据集 id。 */
  datasetId: string;
  /** 固定设置行（原样随表达式派发）。 */
  settings: string;
  /** 本波臂表，硬上限 10 臂。 */
  arms: ArmSpec[];
  /** 设计说明：机制假设→臂的对应、ATOM 合规自检结论。 */
  designNotes: string;
}

/** 单臂平台读数。 */
interface ArmRead {
  /** 臂序。 */
  index: number;
  /** 表达式。 */
  expression: string;
  /** 平台 8 位 alpha id；未产出时空串。 */
  alphaId: string;
  /** S/F/2Y/sub/TO/DD/margin 读数摘要，原样转录。 */
  metrics: string;
  /** 平台 ERROR/CANCELLED 等状态；正常为空串。 */
  simStatus: string;
}

/** 派发与收割结局。 */
interface DispatchOutcome {
  /** dispatched=全臂过闸已派发并收割；rebuild_needed=被拦/塌方需等价几何重建；failed=无法派发。 */
  status: "dispatched" | "rebuild_needed" | "failed";
  /** multisim id；未派发时空串。 */
  multisimId: string;
  /** 按派发臂序的逐臂读数；未收割时空数组。 */
  armReads: ArmRead[];
  /** 被拦/塌方原因（如 [INACCESSIBLE_OP] …）；正常为空串。 */
  blockReason: string;
  /** 轮询/收割过程说明（含兜底通路是否启用）。 */
  harvestNote: string;
}

/** 近闸候选。 */
interface NearGateCandidate {
  /** 平台 alpha id。 */
  alphaId: string;
  /** 触发原因（如 S 1.35 ≥ 1.2 或距硬闸 ≤0.4）。 */
  trigger: string;
  /** 关键读数 S/F/2Y/sub，原样转录。 */
  metrics: string;
}

/** 波次归因结论。 */
interface WaveAttribution {
  /** 本波波号（原字符串）。 */
  wave: string;
  /** 逐臂归因条目（符号指纹/稀释铁律/跨区不外推核对）。 */
  armNotes: string[];
  /** 绿芽/活体结构清单。 */
  sprouts: string[];
  /** 死轴清单（2Y 死轴、S-2Y 跷跷板等）。 */
  deadAxes: string[];
  /** 本波最佳 S（无数值时 0）。 */
  bestSharpe: number;
  /** 本轮扫过的网格维度（带宽/std/decay/其他）。 */
  sweptDimensions: string[];
  /** 数据集终态裁决。 */
  datasetStatus: "active" | "provisional" | "data_excluded" | "dead_proposed" | "capped";
  /** 裁决依据（读数引用；判死依据=读数，不改写邻接集先验）。 */
  verdictEvidence: string;
  /** 是否需要卡点论坛取证（如 2Y 死轴驱动下波设计）。 */
  needsForumRecon: boolean;
  /** 跨波实证、可入册的新杠杆（须有归因对照）；无则空串。 */
  newLever: string;
  /** 近闸候选（最多 2 条，按 S 降序）。 */
  nearGateCandidates: NearGateCandidate[];
  /** 波次文档路径（<类型>_<主题>_<YYYYMMDD>.md）。 */
  docPath: string;
}

/** prod 前置探针单条读数。 */
interface ProdProbe {
  /** 平台 alpha id。 */
  alphaId: string;
  /** prod 相关性读数；未取得为 null。 */
  prodCorrelation: number | null;
  /** 读数来源与 refresh 口径。 */
  source: string;
  /** 是否成功取到读数。 */
  ok: boolean;
  /** 失败/排队/未决说明。 */
  note: string;
}

/** 提交链触发条目（脚本内部）。 */
interface ProdCleanCand {
  /** 平台 alpha id。 */
  alphaId: string;
  /** 所属目标数据集 id（跨波待处理补跑时，台账排除 rg 用它，不用当前波的数据集）。 */
  datasetId: string;
  /** 触发证据（MCP 读数或 CLI 兜底说明）。 */
  evidence: string;
}

/** 提交链①②③+robustness 结论。 */
interface GateCore {
  /** 平台 alpha id。 */
  alphaId: string;
  /** ①台账排除 ②RA+塔位 ③近十年 robustness 硬闸 逐条结论。 */
  gateNotes: string[];
  /** ②的平台实读 failed_ra 是否为 0；未取得为 null（本地快照不得当准）。 */
  failedRaZero: boolean | null;
  /** 塔位 pyramids 摘要。 */
  pyramids: string;
  /** ④⑤ 待共享相关性员查的项。 */
  correlationRequests: string[];
  /** 未跑/未取到的检查，如实列出。 */
  notCovered: string[];
}

/** ④⑤ 相关性读数（单槽串行取得）。 */
interface CorrReads {
  /** prod 相关性（提交链口径 refresh=False）；未取得为 null。 */
  prodCorrelation: number | null;
  /** self-corr；未取得为 null。 */
  selfCorrelation: number | null;
  /** self-corr 是否「未决」（超 30s 客户端窗不硬编，由平台提交时自算解除）。 */
  selfPending: boolean;
  /** 篮内互相关最大值；未取得为 null。 */
  maxMutualCorrelation: number | null;
  /** 读数来源与说明。 */
  notes: string[];
}

/** 提交链收口结论。 */
interface SubmitGateOutcome {
  /** 平台 alpha id。 */
  alphaId: string;
  /** 五道闸逐条结论。 */
  gateNotes: string[];
  /** 平台实读 failed_ra=0。 */
  failedRaZero: boolean;
  /** prod 读数；未取得为 null。 */
  prodCorrelation: number | null;
  /** 篮内互相关最大值；未取得为 null。 */
  maxMutualCorrelation: number | null;
  /** submit_verdict 判定原文（否决权威：BLOCKED 即不提交；UNVERIFIABLE≠放行）。 */
  verdict: string;
  /** 全闸通过判据：failed_ra=0 且 prod<0.7 且互相关<0.7 且 verdict 非 BLOCKED。 */
  allGatesPassed: boolean;
  /** await_user_confirmation=全闸通过停在待用户确认；blocked=被否决；missing_data=读数缺失。 */
  nextStep: "await_user_confirmation" | "blocked" | "missing_data";
  /** 未跑/未取到的检查，如实列出。 */
  notCovered: string[];
}

/** 论坛/文献取证结论。 */
interface ForumRecon {
  /** ok=可靠命中；no_result=可靠完成无命中；error=工具故障（不入档不作证据）。 */
  outcome: "ok" | "no_result" | "error";
  /** 检索并精读的帖子/文献清单（含 id 与要点）。 */
  sources: string[];
  /** 增量假设（直接驱动下波设计）。 */
  hypotheses: string[];
  /** 避坑情报（反例/已证伪路径）。 */
  pitfalls: string[];
  /** 覆盖审计场景下的未测模板清单；卡点取证时空数组。 */
  untestedTemplates: string[];
  /** 证据通道与其盲区说明（如 MCP 直连仿真不写 expressions 表）。 */
  evidenceBlindSpots: string;
}

/** 判死六维闸核对结论。 */
interface DeadAuditOutcome {
  /** 六维 D1–D6 是否每维都有实证。 */
  sixDimsComplete: boolean;
  /** 缺的维度与缺的证据。 */
  missingDimensions: string[];
  /** 检索覆盖矩阵是否补齐。 */
  coverageComplete: boolean;
  /** signal_dead/config_dead/data_excluded/provisional；缺任一维只能 provisional。 */
  layer: "signal_dead" | "config_dead" | "data_excluded" | "provisional";
  /** 是否已走 seal_dead_end（fail-closed 取证闸可能拒绝沉降——拒绝时如实留档，不 force）。 */
  sealed: boolean;
  /** 沉降/未沉降说明。 */
  note: string;
  /** 判死档案路径。 */
  docPath: string;
}

/** 杠杆入册结论。 */
interface LeverRegistration {
  /** 本次登记的杠杆/反模式条目名。 */
  levers: string[];
  /** 入册前置核查：归因对照读数（禁止无对照入册）。 */
  evidenceCheck: string;
  /** sync_skills 校验结果（应为全部安装位零漂移）。 */
  syncResult: string;
  /** 更新后的杠杆册路径。 */
  docPath: string;
}

/** 日终矩阵。 */
interface FinalMatrix {
  /** 类别终态矩阵文档路径。 */
  docPath: string;
  /** 本 run 各数据集终态一览。 */
  datasetStates: string[];
  /** 待用户确认的提交候选（alpha id + 关键读数 + 五道闸结论摘要）。 */
  awaitingConfirmation: string[];
  /** 日终结论两三句。 */
  summary: string;
}

/** 数据集终态注记（findings 的 status 按证据来源分：闸门沉降=verified，归因判断=unconfirmed）。 */
interface DatasetStateNote {
  /** 一句话终态描述。 */
  text: string;
  /** verified=seal_dead_end 闸门沉降证实；unconfirmed=归因判断（读数支持但未经独立确认）。 */
  status: "verified" | "unconfirmed";
}

/** 单条发现（最终报告形状）。 */
interface Finding {
  /** 位置：档案目录或平台对象（如 platform:<alphaId>）。 */
  where: string;
  /** 一句话：发现了什么。 */
  what: string;
  /** 依据：读数/命令/档案。 */
  evidence: string;
  /** verified=平台读数或闸门证实；unconfirmed=归因判断或未取得。 */
  status: "verified" | "unconfirmed";
  /** 影响量级；high 留给数据损坏/崩溃/错误结果。 */
  severity: "low" | "medium" | "high";
}

/** 工作流最终报告。 */
interface WorkflowReport {
  /** 两三句结论：本 run 挖了什么、停在什么确认点。 */
  conclusion: string;
  findings: Finding[];
  /** 本 run 实际执行过的检查与产物。 */
  verified: string[];
  /** 未覆盖/未取得的部分与原因。 */
  notCovered: string[];
}

// ───────────────────── 产物声明（顶层，先于任何 report 引用） ─────────────────────
artifact.chart("wave-sharpe", {
  title: "各波最佳 S 与提交闸参考线",
  x: { field: "wave", label: "波次" },
  y: { field: "bestS", label: "本波最佳 S" },
  baseline: { field: "gate", label: "提交路径 S 参考" },
});
artifact.table("submit-candidates", {
  title: "全闸通过候选（停在待用户确认，不提交）",
  key: "alphaId",
  columns: [
    { field: "alphaId", label: "alpha" },
    { field: "prod", label: "prod" },
    { field: "mutual", label: "篮内最大互相关" },
    { field: "verdict", label: "submit_verdict" },
    { field: "step", label: "下一步" },
  ],
});

// ───────────────────── 共享子代理 ─────────────────────
// 串行是刻意设计（§2 shared）：multi-sim 并发 ≤2 与相关性账号级单槽都是账号级约束，
// 单个共享子代理的 ask 队列 FIFO 把平台调用在结构上串起来，不靠口头纪律。
// 唯一并发例外：提交链内 ①②③（闸门员，只读平台指标）与 ④⑤（相关性员）互不依赖、
// 走不同子代理，两个 ask 同时发起一起收口（§7）——相关性账号级单槽仍由 corrOfficer 的 FIFO 保证。
const surveyor = agent("S0 盘点员", {
  system: `你是类别挖掘战役的 S0 盘点员：读本地台账先验，选目标集、定判读基准、落 S0 档案。
${TOOL_LOADER}
判据纪律：判死档/dead 标记不得单独作排除依据（AGENTS.md §7.5）——先看本地 prod-clean 池与历史臂数；排除面以本次从 DB 读到的台账先验为准（括号内是上一战役 2026-11-14 的事例，仅示形态、勿当现行事实重放：fnd45 QA 78 臂收敛 S≤1.04 不再加注、fnd22 映射表伪信号、digital_ad_spend 宽度塌缩）。每次换集必须出具理由。档案命名 <类型>_<主题>_<YYYYMMDD>.md。
${HONESTY}`,
});
const designer = agent("臂表设计师", {
  system: `你负责每波臂表设计（S1/S2）：字段确认、≤10 臂机制化排布、ATOM 合规自检。
${TOOL_LOADER}
硬约束：每波 ≤10 臂；存在性探针臂=VECTOR vec_avg 包裹（SUBINDUSTRY 下 longCount>0 即有数据——只作存在性判断，不作覆盖度读数）；ATOM=单数据集、group 字段豁免、无 add、乘法/bucket 无权重自由度。
反模式对照（命中即换设计，出处=杠杆册与战役归因）：同源同族两腿加/乘合成已证伪；设置级手段（decay/分组轴/平滑/锐化）破不了 S 闸（S-2Y 跷跷板）；裸 group_backfill 禁用（唯一正确用法=叠在 ts_backfill 之上）；文献/跨区先验只作假设、入批前区内小批符号指纹校验。
${HONESTY}`,
});
const dispatcher = agent("派发员（串行）", {
  system: `你是本战役唯一的回测派发员：预检→静态闸→派发→轮询→收割→落库，全程串行。
硬红线：multi-sim 全程并发 ≤2（账号级）。本工作流同一时刻只喂你一个波，你在途 multisim 不得超过 2，超限立即停止并如实上报。
${TOOL_LOADER}
参数名表（写错在本地 PTC 层即报错、打不到平台）：preflight_expressions/create_multi_simulation/operator_audit 的表达式数组参数=alpha_expressions；batch_status=simulation_ids（数组）；harvest_multisim_alphas=multisimulation_location。
纪律：臂序=收割归因键，逐臂读数禁止按 alpha id 猜；派发前查重（全同表达式平台返回同 id，跳过防浪费设计位）；判据顺序=toolkit 静态闸 > operator_audit 模式2 > 本地白名单 src/wqb/store/_field_patterns.py（:32 含 ts_min_diff）；[INACCESSIBLE_OP] 类拦截或平台 ERROR 连坐 ⇒ 返回 rebuild_needed，不要硬闯；收割 404 兜底=batch_status→children 8 位 id→batch_get_alpha_metrics+get_alpha_details（平台 code 核对臂归属）；读数原样转录，不猜不补。
相关性查询不归你管（单槽在相关性员）。
${HONESTY}`,
});
const corrOfficer = agent("相关性员（单槽）", {
  system: `你是本战役唯一的相关性员：prod/self/mutual 相关性全部经你串行执行——同一账号同时只允许一个相关性调用（ask 队列 FIFO 已保证；你自己绝不再并发，也不手写 requests，429 退避由客户端自带）。
${TOOL_LOADER}
口径：提交链步 8 一律 check_correlation(refresh=False)（48h 缓存优先不回源——红线）；近闸前置探针是提交链外探索动作，用 refresh=True 取新鲜读数。self-corr 全池计算超 30s 客户端窗 ⇒ 记「未决」不硬编（由平台提交时自算解除）。读数 [0,1]；取不到 ⇒ ok=false/note 如实，绝不编数。
${HONESTY}`,
});
const attributor = agent("归因员", {
  system: `你负责逐臂归因与数据集状态裁决，并把每波档案落盘（纯本地归因；判读不改写邻接数据集先验，跨区不外推）。
${TOOL_LOADER}
判据纪律：符号指纹校验（衰减对称=机制在/符号错）；复合形态稀释铁律（乘法/bucket 低于对应单腿=稀释）；数据层排除≠信号死（宽度塌缩+CONCENTRATED_WEIGHT 挂闸 ⇒ 登记口径必须区分）；终判死前置=检索覆盖审计+六维闸 D1–D6（≥10 结构互异模板/每字段族≥1 实测/矩全家四类各≥1/≥2 分组轴/≥1 非线性/≥2 配置），缺任一维只能记 provisional；探针（<10 条）不产生判死；判死依据=读数。
档案命名 <类型>_<主题>_<YYYYMMDD>.md，落 ${ARCHIVE_DIR}/（目录不存在先创建）。波次结论另经 mcp__wqb-db__upsert_wave_result 落库（source_file=pipeline:auto）。
${HONESTY}`,
});
const forumScout = agent("论坛取证员", {
  system: `你负责论坛+文献取证：卡点取证（增量假设驱动下波）与判死前检索覆盖审计。
${TOOL_LOADER}
取证三结局纪律（AGENTS §8.11）：ok（可靠命中）/no_result（检索可靠完成但无命中——如实入档）/error（工具故障——不入档、不作判死证据）。不占相关性槽。任何「未探/未测」清单必须标注证据通道与其盲区（MCP 直连仿真不写 expressions 表）。
${HONESTY}`,
});
const leverRegistrar = agent("杠杆入册员", {
  system: `你负责把跨波实证的杠杆/反模式登记进 Claude/skills/wq-brain-ra-deu/references/_effective-levers.md，并跑 python tools/sync_skills.py 同步全部安装位。
纪律：先读文件尾部再追加（并行写入者——禁止整文件覆写）；入册前置=归因对照（裸 vs 改造的对照读数，禁止无对照入册）；边界与失效反例一并写；已知缺口=gBF 三条规则（裸用禁 TO 47-60%/叠 ts_backfill 才修 CW/带宽随形态漂移）册内无条目，证据支持时补登记。
${HONESTY}`,
});

// ───────────────────── S0 类别盘点 ─────────────────────
log(`类别挖掘启动：region=${region} category=${category} max_waves=${maxWaves}${requestedDataset ? ` 指定集=${requestedDataset}` : ""}`);

phase("S0 类别盘点与目标集选定");
const survey = await surveyor.ask<SurveyResult>(
  `S0 类别盘点：region=${region}，category=${category}。
1. 经 LocalToolSearch 加载只读工具面（select:mcp__wqb-db__get_dead_datasets,mcp__wqb-db__get_dead_ends,mcp__wqb-db__query_dataset_profile,mcp__wqb-db__query_field_profile,mcp__wqb-db__get_region_overview,mcp__wqb-db__get_campaign_summary），拿该类别各集台账先验（历史臂数、S 天花板、判死档、prod-clean 池）。
2. 排除面三型：已收敛 / 伪集 / 数据层排除——逐集以本次 DB 读数（历史臂数、S 天花板、判死档距离）重新认定，不照抄旧战役实例（上役 2026-11-14 例：fnd45 QA 78 臂收敛 S≤1.04、fnd22 映射表伪信号、digital_ad_spend 宽度塌缩——仅示形态）。⚠ 判死档/dead 标记不得单独作排除依据——实测仍在出货的集也曾被列为死集。
3. 目标集：${requestedDataset ? `用户指定 dataset=${requestedDataset}——核对其判死闸距离（六维 D1–D6 与历史臂数）并出具采用理由` : "按机制先验+历史臂数+判死闸距离选定（历史臂数少且六维未穷尽=远未到判死线）"}。
4. 判读基准：S/2Y/sub 预期与符号指纹（衰减对称=机制在/符号错）、TO 预期（量级参照：上一战役 fnd45 基线 S 0.96/2Y 1.73/sub 0.72——2026-11-14 事实，非现行承诺）。
5. 档案：写 ${ARCHIVE_DIR}/S0_DATASET_SCAN_${category}_<YYYYMMDD>.md（证据出处写 path:line）。
工具失败/档案缺失 ⇒ 如实写进 excluded，不要编造。`,
);
report({ runId: run.id, stage: "S0", target: survey.targetDataset, doc: survey.docPath, excluded: survey.excluded });
log(`S0 选定目标集：${survey.targetDataset}`);

// ───────────────────── 波次主循环（有界：max_waves） ─────────────────────
let dataset = requestedDataset || survey.targetDataset;
let mechHypo = survey.mechanismHypothesis;
let baseline = survey.readingBaseline;
let moreTargetsRemain = survey.moreTargetsRemain;
let waveNo = 0;
let switches = 0;
let done = dataset === "";
const cappedOrClosed: string[] = [];
const gatedIds: string[] = [];
const awaiting: SubmitGateOutcome[] = [];
const pendingSubmits: ProdCleanCand[] = []; // 跨波待处理提交链队列（每波 1 条名额，余量下波补跑）
const datasetStates: DatasetStateNote[] = [];
const verified: string[] = [];
const notCovered: string[] = [];
let designerFeedback = "";
let forumHypotheses: string[] = [];

while (!done && waveNo < maxWaves) {
  waveNo += 1;
  const waveLabel = `w${waveNo}`;
  let prodClean: ProdCleanCand[] = [];
  let cliNote = "";
  let cliOk = false;
  let wallNote = "";
  let switchReason = "";
  let chainsThisWave = 0;
  log(`第 ${waveNo}/${maxWaves} 波（目标集 ${dataset}）`);

  // —— S1/S2 臂表 ——
  phase("设计本波臂表");
  const table = await designer.ask<ArmTable>(
    `设计第 ${waveNo} 波臂表（目标集 ${dataset}）。
字段确认：经 LocalToolSearch 加载 mcp__wq-brain-http__get_datafields 后核对本波字段存在性/覆盖形态，再排臂。
机制假设：${mechHypo}
判读基准：${baseline}
固定设置行（原样输出到 settings）：${SETTINGS_LINE}
臂表要求：≤10 臂（硬上限）；单腿换轴/换分母/反号/乘法交互/bucket 条件化；需要确认字段是否有数据时加存在性探针臂（VECTOR vec_avg 包裹，只作存在性判断不作覆盖度读数）；ATOM 合规自检写进 designNotes。
${designerFeedback ? `上一波反馈（禁止盲扫，归因驱动）：${designerFeedback}` : "首波：按机制先验排布。"}
${forumHypotheses.length > 0 ? `论坛增量假设（可入臂验证，须区内符号校验）：${forumHypotheses.join("；")}` : ""}`,
  );

  // —— 预检 + 派发 + 收割（最多两轮：塌方回预检重建再派） ——
  phase("预检并派发本波回测");
  let outcome = await dispatcher.ask<DispatchOutcome>(
    `预检并派发第 ${waveNo} 波（wave 标签 ${waveLabel}，region=${region}）。臂表：
${JSON.stringify(table)}
步骤（全串行，multi-sim 在途 ≤2）：
1. preflight_expressions(dataset_id=<集id>, alpha_expressions=<全臂表达式>)——参数名必须是 alpha_expressions；unknown 逐个甄别：「字段提取器把算子误当字段」类放行（白名单 src/wqb/store/_field_patterns.py 含 ts_min_diff 等），真缺字段 ⇒ 该臂回 rebuild。
2. toolkit 静态闸：本地可用入口（WQ_VALIDATOR_DIR validator / toolkit gate.py 静态模式）跑一遍；判据顺序=toolkit 静态闸 > operator_audit 模式2 > 本地白名单。被 [INACCESSIBLE_OP] 等拦截 ⇒ status=rebuild_needed、blockReason 写明被拦臂与原因。
3. 派发前查重：与本战役已派表达式全同的臂跳过（平台全同表达式返回同 id）。
4. create_multi_simulation(alpha_expressions=<过闸臂>) 单波派发，记录 multisim id 与派发臂序。
5. batch_status(simulation_ids=[...]) 轮询至 N/N COMPLETE（约 40 次上限或明确 ERROR 即停）。
6. 收割：harvest_multisim_alphas(multisimulation_location=...)；404 兜底=batch_status→children 8 位 id→batch_get_alpha_metrics+get_alpha_details（平台 code 核对臂归属）。
7. 读数落库：mcp__wqb-db__upsert_backtest_rows（region=${region}，wave=${waveLabel}），供 prod-first CLI 兜底与台账。
8. 按派发臂序逐臂读数（S/F/2Y/sub/TO/DD/margin），禁止按 alpha id 猜；平台 ERROR/连坐 CANCELLED ⇒ status=rebuild_needed 并在 blockReason 写明。
相关性查询不做（单槽在相关性员）。`,
  );
  if (outcome.status === "rebuild_needed") {
    phase("设计本波臂表");
    const rebuilt = await designer.ask<ArmTable>(
      `等价几何重建（第 ${waveNo} 波，塌方回预检）：被拦原因=${outcome.blockReason}
原臂表：${JSON.stringify(table)}
只重排被拦/塌方臂：同机制等价几何（先例：ts_min_diff→ts_scale/ts_av_diff/ts_zscore 第三派过闸），总臂数仍 ≤10，settings 不变，输出同结构臂表。`,
    );
    phase("预检并派发本波回测");
    outcome = await dispatcher.ask<DispatchOutcome>(
      `重派第 ${waveNo} 波（等价几何重建后）。臂表：
${JSON.stringify(rebuilt)}
同主波派发指令的步骤 1–8 全串行执行（wave 标签 ${waveLabel}，region=${region}）。`,
    );
  }
  if (outcome.status !== "dispatched") {
    log(`第 ${waveNo} 波未能派发：${outcome.blockReason || outcome.status}`);
    report({ runId: run.id, wave: waveNo, dataset, status: "dispatch_failed", reason: outcome.blockReason });
    notCovered.push(`第 ${waveNo} 波未派发：${outcome.blockReason || outcome.status}`);
    designerFeedback = `第 ${waveNo} 波派发失败：${outcome.blockReason}`;
    continue;
  }
  verified.push(
    `第 ${waveNo} 波经 preflight_expressions + toolkit 静态闸预检后派发（multisim=${outcome.multisimId}，${outcome.armReads.length} 臂读数）`,
  );

  // —— 逐臂归因 + 波次档案 ——
  phase("逐臂归因并写波次档案");
  const attr = await attributor.ask<WaveAttribution>(
    `逐臂归因第 ${waveNo} 波（目标集 ${dataset}，wave=${waveLabel}）。
判读基准：${baseline}
按臂序读数（原样，勿按 alpha id 猜）：
${JSON.stringify(outcome.armReads)}
收割说明：${outcome.harvestNote}
归因要求：
- 符号指纹校验；复合形态稀释铁律核对（乘法/bucket 低于对应单腿=稀释）；跨区不外推（TWN 经验在 DEU 无一致增益）。
- 识别绿芽/活体（sprouts）与死轴（deadAxes，如 2Y 死轴、S-2Y 跷跷板）。
- 数据层排除判读：longCount/shortCount 宽度塌缩+CONCENTRATED_WEIGHT 挂闸 ⇒ data_excluded（数据层排除≠信号死，登记口径必须区分）。
- datasetStatus 裁决：active=继续加注；provisional=判弱入档；data_excluded=数据层排除；dead_proposed=拟终判死（必须先过检索覆盖审计+六维闸，缺任一维只能 provisional）；capped=网格收敛封顶。判死依据=读数，不改写邻接集先验；探针（<10 条）不产生判死。
- bestSharpe=本波最佳 S（无数值填 0）；sweptDimensions=本轮实际扫过的网格维度（带宽/std/decay/其他）。
- 近闸候选：S≥1.2 或距任一硬闸 ≤0.4 的臂列入 nearGateCandidates（≤2 条，按 S 降序）——先测 prod 再扫参（prod 雷在核心不在搭档，同核变体共 prod 命运）。
- newLever：仅当跨波实证且带归因对照（禁止无对照入册），否则空串。
- 档案：写 ${ARCHIVE_DIR}/WAVE_${waveLabel}_${dataset}_<YYYYMMDD>.md（臂序读数表+归因条目+终态），并经 mcp__wqb-db__upsert_wave_result 落波结论。`,
  );
  const bestS = Number.isFinite(attr.bestSharpe) ? attr.bestSharpe : 0;
  report(
    {
      runId: run.id,
      wave: waveNo,
      dataset,
      bestS,
      gate: CHART_GATE,
      sprouts: attr.sprouts.length,
      status: attr.datasetStatus,
    },
    "wave-sharpe",
  );
  log(`第 ${waveNo} 波归因：最佳 S=${bestS}，终态=${attr.datasetStatus}，档案=${attr.docPath}`);

  // —— 近闸 prod 前置探针（先测 prod 再扫参；MCP 优先，CLI 兜底） ——
  if (attr.nearGateCandidates.length > 0) {
    phase("近闸 prod 探针");
    const cands = attr.nearGateCandidates.slice(0, 2);
    const probe = await corrOfficer.ask<ProdProbe[]>(
      `近闸 prod 前置探针（探索口径，refresh=True）：对下列候选逐个 check_correlation(production)，单槽串行跑，不逐臂重探——同核变体共 prod 命运，每个核心测 1 条即可。
候选：${JSON.stringify(cands)}
读数 [0,1]；取不到 ⇒ ok=false+note（排队/超时/未决），不要编数。每个候选返回一条 ProdProbe。`,
    );
    if (probe.some((p) => !p.ok)) {
      // CLI 兜底：prod-first 有进程锁 data/.prod_first.lock（平台 prod 单并发），退出码为值非异常
      try {
        const cli = await world.run(
          "world-quant-brain-mcp/.venv/Scripts/python.exe",
          ["tools/campaign_intel.py", "prod-first", "--region", region, "--wave", waveLabel, "--top-k", "2"],
          { timeoutMs: 600000, output: { tail: 16384 } },
        );
        cliOk = cli.exitCode === 0;
        cliNote = cliOk
          ? `CLI prod-first exit=0，prod 读数已落 alphas.prod_correlation：\n${cli.stdout.slice(-2000)}`
          : `CLI prod-first exit=${cli.exitCode}：\n${cli.stderr.slice(-1000)}`;
        if (!cliOk) notCovered.push(`第 ${waveNo} 波 prod-first CLI 兜底非零退出，部分 prod 读数可能缺失`);
      } catch (e) {
        cliNote = `CLI 兜底未能执行：${String(e).slice(0, 300)}`;
        notCovered.push(`第 ${waveNo} 波 prod-first CLI 兜底失败`);
      }
    }
    for (const p of probe) {
      if (!p.alphaId.trim()) {
        // 探针没带回 alpha id：空串进 prodClean 会让提交链找不到对象，按未取得如实登记
        notCovered.push(`第 ${waveNo} 波探针返回空 alphaId（ok=${p.ok}，note=${p.note}）——该候选无法进入提交链`);
        continue;
      }
      if (p.ok && p.prodCorrelation !== null && p.prodCorrelation < PROD_CEILING) {
        prodClean.push({
          alphaId: p.alphaId,
          datasetId: dataset,
          evidence: `MCP check_correlation prod=${p.prodCorrelation}（${p.source}）`,
        });
      } else if (!p.ok && cliOk && cliNote.includes(p.alphaId)) {
        prodClean.push({
          alphaId: p.alphaId,
          datasetId: dataset,
          evidence: `MCP 探针失败（${p.note}）；CLI prod-first 已跑并落库，由提交链经平台/DB 读数判定`,
        });
      } else if (!p.ok) {
        notCovered.push(`${p.alphaId} 的 prod 读数未取得：${p.note}`);
      } else if (p.prodCorrelation !== null && p.prodCorrelation >= PROD_CEILING) {
        wallNote = `prod ${p.prodCorrelation} 堵（${p.alphaId}）——雷在核心不在搭档：同核变体共 prod 命运，整族停手换核心，不逐臂重探`;
      } else {
        // ok=true 却没带读数：探针自称成功但没带数，兜底按未取得登记，不许静默丢弃
        notCovered.push(`${p.alphaId} 的探针报告成功但未带 prod 读数（prodCorrelation=null，来源 ${p.source}）——按未取得处理`);
      }
    }
    if (prodClean.length > 0) {
      verified.push(`第 ${waveNo} 波近闸 prod 探针（${prodClean.map((c) => c.alphaId).join("、")} 干净）`);
    }
  }

  // —— 提交链五道闸（仅 prod 干净候选；提交 POST 不在工作流内执行） ——
  // 跨波待处理队列先行：上波名额（每波 1 条）用完排队的候选在本波优先补跑，不静默丢候选；
  // 补跑候选的台账排除用其原属数据集（cand.datasetId），不跟当前波走。
  const chainCands: ProdCleanCand[] = [...pendingSubmits, ...prodClean];
  pendingSubmits.length = 0;
  for (const cand of chainCands) {
    if (gatedIds.includes(cand.alphaId)) continue;
    if (chainsThisWave >= 1) {
      pendingSubmits.push(cand);
      continue;
    }
    chainsThisWave += 1;
    gatedIds.push(cand.alphaId);
    phase("提交链五道闸");
    const gateOfficer = agent(`提交闸·${cand.alphaId}`, {
      system: `你是提交链闸门员：按固定顺序跑五道闸的①②③与 robustness 硬闸核对，收口时调 submit_verdict。
${TOOL_LOADER}
红线：①台账排除用 rg "<dataset_id>" docs reports Claude/skills（把已测骨架当排除表）；②RA+塔位以平台实读为准——本地 failed_ra_count 是旧快照不得当准；③近十年逐年核 longCount>0 && shortCount>0 && pnl>0（只看全期不算数；异常年份如实标注交用户裁量，不要美化）；④⑤相关性读数不归你——由共享相关性员（账号级单槽）负责，你只把待查项列进 correlationRequests；submit_verdict 是否决权威（BLOCKED 即不提交；它放行不了任何东西，UNVERIFIABLE≠放行——放行=prod 实测+用户确认，缺一不可）。
你绝对不调用任何提交 POST（workflow_submit_alpha / workflow_superalpha 一律不碰）。
robustness 口径：硬 REJECT 项 0 才算过；软标记（CV_Sharpe 0.40–0.60、max/min 3–5、算子数>5、早年疲软）不阻断判定但必须逐项落盘；未跑的检查如实写 notCovered。
${HONESTY}`,
    });
    // ①②③（闸门员，只读平台指标）与 ④⑤（相关性员，账号级单槽）互不依赖、走不同子代理：
    // 两个 ask 并发发起、一起收口（§7），省每条提交链一段墙钟时间；
    // 相关性账号级单槽仍由 corrOfficer 的 ask 队列 FIFO 结构性保证，不靠口头纪律。
    const [core, corr] = await Promise.all([
      gateOfficer.ask<GateCore>(
        `提交链五道闸（①②③+robustness 硬闸），候选 ${cand.alphaId}（触发证据：${cand.evidence}）。目标集 ${cand.datasetId}，波 ${waveLabel}。
1. LocalToolSearch 加载 mcp__wq-brain-http__batch_get_alpha_metrics,mcp__wq-brain-http__get_alpha_details,mcp__wq-brain-http__get_alpha_yearly_stats,mcp__wqb-db__get_alpha_corr_metrics。
2. ①台账排除：rg "${cand.datasetId}" docs reports Claude/skills（把已测骨架当排除表用）。
3. ②RA+塔位：batch_get_alpha_metrics+get_alpha_details 读平台 checks.fail 与 pyramids.list；failed_ra 是否=0 以平台实读为准（本地 failed_ra_count 是旧快照不得当准）。
4. ③近十年：get_alpha_yearly_stats 逐年核 longCount>0 && shortCount>0 && pnl>0；异常年份（如首年爬坡微亏）如实标注交用户裁量。
5. robustness 硬闸核对（brain-alpha-robustness 口径；软标记不阻断但逐项落盘）。
6. ④⑤相关性读数不做——列进 correlationRequests（prod refresh=False / self / mutual），由共享相关性员跑。
未跑的检查如实写 notCovered。`,
      ),
      corrOfficer.ask<CorrReads>(
        `提交链第④⑤步相关性读数（单槽串行，逐个跑）：候选 ${cand.alphaId}。
1. check_correlation(refresh=False)——提交链口径，48h 缓存优先不回源（红线）。
2. check_self_correlation——本区 OS 池；全池超 30s 客户端窗 ⇒ selfPending=true 记「未决」不硬编。
3. compute_mutual_correlation——取篮内最大值。
${cliNote ? `参考（探索口径已跑的兜底，读数以本次 refresh=False 为准）：${cliNote}` : ""}
每项未取得 ⇒ null+notes 说明，不要编数。`,
      ),
    ]);
    const verdictOut = await gateOfficer.ask<SubmitGateOutcome>(
      `相关性读数已回（来自相关性员）：${JSON.stringify(corr)}
收口五道闸（候选 ${cand.alphaId}；①②③与 robustness 结论：${JSON.stringify(core.gateNotes)}）：
- ⑤篮内互相关+塔位配额核对；
- submit_verdict（否决权威：BLOCKED 即不提交；UNVERIFIABLE≠放行）；
- 全闸通过判据（本工作流口径）：failed_ra=0（平台实读）且 prod<${PROD_CEILING} 且篮内互相关<0.7 且 verdict 非 BLOCKED。权威阈值=config.PRODCORR_CEILING（src/wqb/config.py:502=0.70），实读不一致时如实写 notCovered。
- nextStep 只能是 await_user_confirmation / blocked / missing_data。本工作流不执行提交：await_user_confirmation 仅表示「停在待用户确认」。
- 未跑/未取得的检查逐条写 notCovered，不得装作通过。`,
    );
    report(
      {
        runId: run.id,
        alphaId: verdictOut.alphaId,
        prod: verdictOut.prodCorrelation,
        mutual: verdictOut.maxMutualCorrelation,
        verdict: verdictOut.verdict,
        step: verdictOut.nextStep,
      },
      "submit-candidates",
    );
    if (verdictOut.nextStep === "await_user_confirmation") {
      awaiting.push(verdictOut);
      log(`★ ${verdictOut.alphaId} 全闸通过——停在「待用户确认」（提交不在工作流内执行）`);
    } else {
      log(`${verdictOut.alphaId} 未过全闸：${verdictOut.nextStep}（verdict=${verdictOut.verdict}）`);
    }
  }
  if (pendingSubmits.length > 0) {
    log(`本波提交链名额已用完（每波 1 条）：${pendingSubmits.map((c) => c.alphaId).join("、")} 已排队待后续波补跑`);
  }

  // —— 破闸深挖网格精修（≤3 轮；收敛=带宽/std/decay 全扫完且 S 不再抬升） ——
  if (attr.sprouts.length > 0 && attr.datasetStatus === "active") {
    const swept: string[] = [];
    for (const d of attr.sweptDimensions) if (!swept.includes(d)) swept.push(d);
    let familyBest = bestS;
    let gridCapped = false;
    for (let round = 1; round <= MAX_GRID_ROUNDS && waveNo < maxWaves; round++) {
      waveNo += 1;
      const gLabel = `w${waveNo}`;
      log(`网格精修第 ${round}/${MAX_GRID_ROUNDS} 轮（波 ${gLabel}，家族最佳 S=${familyBest}）`);
      phase("网格精修·设计变体臂表");
      const gtable = await designer.ask<ArmTable>(
        `网格精修（${dataset} 家族，第 ${round} 轮，波 ${gLabel}）：活体=${JSON.stringify(attr.sprouts)}
归因驱动变体设计（禁止盲扫）：带宽曲线/std 档位/decay 表达式级与设置级/分组轴，每维至少 2 点以判峰谷；双向回落证实是峰不是单调。总臂数 ≤10，settings 固定行不变。
家族最佳 S=${familyBest}；已扫维度=${JSON.stringify(swept)}。
${wallNote ? `prod 纪律：${wallNote}` : ""}`,
      );
      phase("网格精修·预检并派发");
      const gout = await dispatcher.ask<DispatchOutcome>(
        `预检并派发精修波 ${gLabel}（wave 标签 ${gLabel}，region=${region}）。臂表：
${JSON.stringify(gtable)}
同主波派发指令步骤 1–8 全串行执行（multi-sim 在途 ≤2）。`,
      );
      if (gout.status !== "dispatched") {
        log(`精修波 ${gLabel} 未能派发：${gout.blockReason || gout.status}`);
        notCovered.push(`精修波 ${gLabel} 未派发：${gout.blockReason || gout.status}`);
        break;
      }
      phase("网格精修·逐臂归因写档");
      const gattr = await attributor.ask<WaveAttribution>(
        `精修波 ${gLabel} 归因（目标集 ${dataset}）。
判读基准：${baseline}
按臂序读数：${JSON.stringify(gout.armReads)}
同主波归因要求；重点产出带宽曲线/杠杆结论；sweptDimensions 填本轮实际扫过的维度；newLever 仅在带归因对照时给。
档案 ${ARCHIVE_DIR}/WAVE_${gLabel}_${dataset}_<YYYYMMDD>.md + mcp__wqb-db__upsert_wave_result。`,
      );
      const gBest = Number.isFinite(gattr.bestSharpe) ? gattr.bestSharpe : 0;
      report(
        {
          runId: run.id,
          wave: waveNo,
          dataset,
          bestS: gBest,
          gate: CHART_GATE,
          sprouts: gattr.sprouts.length,
          status: gattr.datasetStatus,
        },
        "wave-sharpe",
      );
      for (const d of gattr.sweptDimensions) if (!swept.includes(d)) swept.push(d);
      const rose = gBest > familyBest;
      if (rose) familyBest = gBest;
      if (!rose && GRID_DIMS.every((d) => swept.includes(d))) {
        gridCapped = true;
        log(`网格收敛：${GRID_DIMS.join("/")} 全维度扫完且 S 不再抬升（峰值 ${familyBest}）——封顶不再加注`);
        break;
      }
    }
    if (gridCapped) {
      cappedOrClosed.push(dataset);
      datasetStates.push({
        text: `${dataset}：网格收敛封顶（峰值 S=${familyBest}）——家族转最高优先候选储备，待新结构灵感或跨族合成授权再启`,
        status: "unconfirmed", // 封顶是归因判断（读数支持，未经独立确认）
      });
      switchReason = `当前集 ${dataset} 网格收敛封顶（带宽/std/decay 全扫完且 S 不再抬升）`;
    }
  }

  // —— 卡点论坛取证（每波 ≤1 次，不占相关性槽） ——
  if (attr.needsForumRecon) {
    phase("卡点论坛取证");
    const recon = await forumScout.ask<ForumRecon>(
      `卡点论坛取证（驱动下波设计）：卡点=${JSON.stringify(attr.deadAxes)}（目标集 ${dataset}）。
检索+精读：每帖要点、赞数；产出增量假设（骨架算子/缩窗/中性化替换等，直接可入臂）与避坑情报。已知教训要带上：论坛「缩窗救 2Y」在 fnd89 连 S 一起单调杀；TWN「STATISTICAL>SUBINDUSTRY」在 DEU 无一致增益——假设须区内小批符号校验后才入批。
结局三选一如实：ok/no_result/error（error=工具故障，不入档不作证据；no_result 亦如实入档）。`,
    );
    if (recon.outcome === "error") {
      notCovered.push(`第 ${waveNo} 波卡点论坛取证工具故障，未取得增量假设`);
    } else {
      forumHypotheses = recon.hypotheses;
    }
  }

  // —— 判死前置：检索覆盖审计 + 六维闸（dead_proposed 才触发） ——
  if (attr.datasetStatus === "dead_proposed") {
    phase("判死前置·检索覆盖审计与六维闸");
    const cov = await forumScout.ask<ForumRecon>(
      `检索覆盖审计（终判死/入档硬前置）：目标集 ${dataset}。
补齐论坛+文献覆盖矩阵：论坛直接命中（每帖要点+赞数）；文献间接先验（该字段族对应教科书/经典文献，如 Piotroski/Mohanram/Novy-Marx/QMJ/CHS 视族而定）；零直接命中如实记 no_result。产出未测模板清单（直接驱动新波设计）与避坑情报，并标注证据通道盲区。`,
    );
    const audit = await attributor.ask<DeadAuditOutcome>(
      `六维闸核对（${dataset} 拟终判死）：归因证据=${attr.verdictEvidence}
覆盖矩阵=${JSON.stringify(cov)}
逐维核对 D1–D6：D1 ≥10 结构互异模板（换窗口/换常数/同假设正反两向均不算）；D2 每个可用字段族 ≥1 实测；D3 矩全家（水平/一阶差/二阶波动/比值或信噪比 各≥1）；D4 ≥2 分组轴；D5 ≥1 非线性（signed_power/ts_rank/ts_quantile/trade_when/bucket）；D6 ≥2 配置（宇宙×中性化×decay 至少变一维）。结合本 run 实测波次与台账历史臂数。
缺任一维 ⇒ layer=provisional（不得沉降、不得引用为邻接集先验）；全维齐+覆盖齐 ⇒ 按分层给 signal_dead/config_dead，并经 mcp__wqb-db__seal_dead_end 沉降（fail-closed 取证闸可能拒绝——拒绝时 sealed=false 如实留档，不要 force）。判死档案写 ${ARCHIVE_DIR}/DEATH_AUDIT_${dataset}_<YYYYMMDD>.md；判死依据=读数，不改写邻接集先验。`,
    );
    report({ runId: run.id, dataset, layer: audit.layer, sealed: audit.sealed, missing: audit.missingDimensions, doc: audit.docPath });
    datasetStates.push({
      text: `${dataset}：${audit.layer}${audit.sealed ? "（seal_dead_end 已沉降）" : "（未沉降，档案留痕）"}`,
      status: audit.sealed ? "verified" : "unconfirmed", // 沉降=fail-closed 取证闸证实；未沉降=归因判断
    });
    if (audit.layer === "signal_dead" || audit.layer === "config_dead") {
      cappedOrClosed.push(dataset);
      switchReason = `${dataset} 终判死（${audit.layer}，六维齐+覆盖齐）`;
    } else if (audit.layer === "data_excluded") {
      cappedOrClosed.push(dataset);
      switchReason = `${dataset} 数据层排除（≠信号死）`;
    }
    // provisional ⇒ 留在当前集继续
  } else if (attr.datasetStatus === "data_excluded") {
    cappedOrClosed.push(dataset);
    datasetStates.push({
      text: `${dataset}：数据层排除（宽度塌缩/覆盖不足——≠信号死，登记口径已区分）`,
      status: "unconfirmed", // 归因判断
    });
    switchReason = `${dataset} 数据层排除（数据层≠信号死）`;
  } else if (attr.datasetStatus === "capped") {
    cappedOrClosed.push(dataset);
    datasetStates.push({
      text: `${dataset}：网格收敛封顶（归因裁决）`,
      status: "unconfirmed", // 归因判断
    });
    switchReason = `${dataset} 网格收敛封顶（归因裁决）`;
  }

  // —— 杠杆/经验入册（每波 ≤1 次，须带归因对照） ——
  if (attr.newLever) {
    phase("杠杆/经验入册");
    const reg = await leverRegistrar.ask<LeverRegistration>(
      `杠杆入册：${attr.newLever}
归因对照证据：${attr.verdictEvidence.slice(0, 600)}
1. 读 Claude/skills/wq-brain-ra-deu/references/_effective-levers.md（先读尾部再追加，禁止整文件覆写）。
2. 条目含：模板、对照读数（裸 vs 改造）、边界与失效反例。
3. gBF 三条规则缺口（裸 gBF 禁用 TO 47-60%；必须叠 ts_backfill 之上才修 CW；带宽/std 峰值随形态漂移）——本波证据支持则一并补。
4. 跑 python tools/sync_skills.py（或 world-quant-brain-mcp/.venv 的 python）同步全部安装位并校验，结果写进 syncResult。`,
    );
    report({ runId: run.id, levers: reg.levers, sync: reg.syncResult, doc: reg.docPath });
    if (!reg.syncResult.includes("零漂移")) {
      notCovered.push(`sync_skills 校验结果异常：${reg.syncResult}`);
    } else {
      verified.push(`杠杆入册 ${reg.levers.join("、")} + sync_skills 零漂移`);
    }
  }

  // —— 波末反馈带往下一波 ——
  designerFeedback = `第 ${waveNo} 波归因：${attr.armNotes.slice(0, 5).join("；")}；死轴=${attr.deadAxes.join("、") || "无"}${wallNote ? `；${wallNote}` : ""}`;

  // —— 换集裁决（每次换集须出具理由；上限 MAX_SWITCHES） ——
  if (switchReason) {
    if (switches < MAX_SWITCHES) {
      phase("S0 类别盘点与目标集选定");
      const re = await surveyor.ask<SurveyResult>(
        `换集重选（换集须出具理由）：${switchReason}
已封顶/关闭：${JSON.stringify(cappedOrClosed)}
排除面同 S0（判死档不得单独作排除依据）。类别=${category}。按机制先验+历史臂数+判死闸距离选下一目标集，出具理由与判读基准；若类别内无值得再开的目标集 ⇒ targetDataset 空串+moreTargetsRemain=false。档案续写 S0_DATASET_SCAN（命名规则不变）。`,
      );
      moreTargetsRemain = re.moreTargetsRemain;
      if (re.targetDataset) {
        dataset = re.targetDataset;
        mechHypo = re.mechanismHypothesis;
        baseline = re.readingBaseline;
        switches += 1;
        log(`换集 → ${dataset}（第 ${switches}/${MAX_SWITCHES} 次）：${re.mechanismHypothesis}`);
      } else {
        log(
          moreTargetsRemain === false
            ? "盘点员判定类别内无更多目标集——结束波次循环"
            : "本轮盘点未给出新目标集（盘点员仍报告类别内有候选）——结束波次循环；如需继续，带 dataset 参数重跑",
        );
        done = true;
      }
    } else {
      log(`换集上限 ${MAX_SWITCHES} 次已达——结束波次循环`);
      done = true;
    }
  }
}

// ───────────────────── 日终收尾与类别终态矩阵 ─────────────────────
if (!done) {
  log(`已达 max_waves=${maxWaves} 波次上限，循环结束${moreTargetsRemain ? "；盘点员报告类别内仍有值得开的目标集（本轮未及）" : ""}`);
}
if (pendingSubmits.length > 0) {
  // 跨波队列到 run 结束仍非空：候选 prod 已判净却没跑上提交链，必须进 notCovered，不许不可见
  notCovered.push(
    `run 结束仍有 ${pendingSubmits.length} 条 prod-clean 候选未跑提交链（每波 1 条上限、波次已尽）：${pendingSubmits
      .map((c) => `${c.alphaId}（目标集 ${c.datasetId}）`)
      .join("、")}——prod 读数已干净，可直接进提交链`,
  );
}
phase("日终收尾与类别终态矩阵");
const matrix = await attributor.ask<FinalMatrix>(
  `日终收尾：region=${region}，category=${category}，共 ${waveNo} 波。
数据集终态：${JSON.stringify(datasetStates.length > 0 ? datasetStates.map((s) => s.text) : ["（本 run 无数据集终态变更）"])}
待用户确认候选：${JSON.stringify(
      awaiting.map(
        (a) => `${a.alphaId}（prod=${a.prodCorrelation}，互相关=${a.maxMutualCorrelation}，verdict=${a.verdict}）`,
      ),
    )}
跨波待处理提交链候选：${pendingSubmits.length > 0 ? JSON.stringify(pendingSubmits.map((c) => `${c.alphaId}（目标集 ${c.datasetId}，prod 已判净未跑链）`)) : "无"}
写类别终态矩阵到 ${ARCHIVE_DIR}/（如 CATEGORY_MATRIX_${category}_<YYYYMMDD>.md）：逐集终态+今日波次与产出索引；只写档案，不做平台调用。summary 两三句。`,
);

// 发布日终矩阵（发布拒绝是修复机会：补写后重试一次，再失败则以 markdown 摘要兜底）
const MATRIX_TITLE = `${region} ${category} 类别挖掘·日终矩阵`;
try {
  await artifact.file("campaign-report", matrix.docPath, { title: MATRIX_TITLE, primary: true });
} catch {
  log("矩阵档案发布失败——请归因员补写后重试");
  const fixed = await attributor.ask<FinalMatrix>(
    `刚写的矩阵档案发布失败（路径：${matrix.docPath}）。检查文件确实存在于仓库工作区内、内容完整后重写，再返回 docPath。`,
  );
  try {
    await artifact.file("campaign-report", fixed.docPath, { title: MATRIX_TITLE, primary: true });
  } catch {
    await artifact.markdown(
      "campaign-report-md",
      `# ${region} ${category} 类别挖掘·日终摘要\n\n${fixed.summary}\n\n数据集终态：\n${datasetStates.map((s) => `- ${s.text}`).join("\n")}\n`,
      { title: `${region} ${category} 类别挖掘·日终摘要` },
    );
  }
}

// ───────────────────── 汇总返回 ─────────────────────
const findings: Finding[] = [];
for (const s of datasetStates) {
  findings.push({
    where: ARCHIVE_DIR,
    what: s.text,
    evidence:
      s.status === "verified"
        ? "seal_dead_end 沉降回执（fail-closed 取证闸核对过证据）+ 波次归因档案"
        : "波次归因读数与判死档案（归因判断，未经独立确认——见波次/判死文档）",
    status: s.status,
    severity: "low",
  });
}
for (const a of awaiting) {
  findings.push({
    where: `platform:${a.alphaId}`,
    what: `全闸通过候选，停在待用户确认（verdict=${a.verdict}）`,
    evidence: `五道闸结论：${a.gateNotes.join("；").slice(0, 500)}`,
    status: "verified",
    severity: "medium",
  });
}
for (const n of notCovered) {
  findings.push({ where: region, what: n, evidence: "运行期如实登记", status: "unconfirmed", severity: "low" });
}

const result: WorkflowReport = {
  conclusion: `共跑 ${waveNo} 波（换集 ${switches} 次）。${!done && moreTargetsRemain ? "已达波次上限收束，类别内仍有值得开的目标集未及开波。" : ""}${
    awaiting.length > 0
      ? `${awaiting.map((a) => a.alphaId).join("、")} 已过全部五道闸（failed_ra=0、prod<0.7、篮内互相关<0.7、verdict 非 BLOCKED），按红线停在「待用户确认」——提交不在工作流内执行，待用户确认后另行提交。`
      : "本 run 无全闸通过候选，未触发提交确认点。"
  } 日终矩阵：${matrix.docPath}`,
  findings,
  verified,
  notCovered,
};
return result;
