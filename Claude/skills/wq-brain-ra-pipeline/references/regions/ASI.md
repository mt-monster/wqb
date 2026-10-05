---
region: ASI
entry_verdict: probe-only
one_liner: "处女地：未开垦，analyst94 近闸（OS 0.666）/ analyst81 untried，全量探针建 baseline"
static:
  universe: []  # 必须 get_platform_setting_options 实测，禁止照抄任何区域
  universe_default: null
  delay: []     # 实测
  delay_default: null
  neutralization_default: SUBINDUSTRY
  notes: "static 层未建立，步 1 强制实测合法档位"
datasets:
  red: []
  green:
    - scope: family
      families: [analyst94, analyst81]
      note: "族级方向（2026-10-01 迁移自旧文本形态；逐数据集绑定待实证补齐）"
  yellow: []
priors:
  signal_families_include: [analyst]
  signal_families_exclude: []
  syntax_patterns: []
  win_recipes: []
gate_overrides:
  cw_gate: WARN
loop_policy:
  max_probes_per_wave: 5
  first_wave_probe_exemption: true
  fast_kill: "缺省（决策表 D15：新数据集 8 探针无 |S|≥0.5 即判死）；本区无额外规则"
  stop_conditions: ["白名单被 dead_end 全覆盖", "连续 3 波全 FAIL 且无新 dead_end"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(ASI)"
  last_verified: 2026-08-25
---

# ASI — 处女地全量探针区

## 定位与实证依据

ASI 基本未开垦：无 win 层、无死路记录，registry 接近空白。已有线索两条：analyst94 探出 OS Sharpe 0.666（近闸候选）、analyst81 在推荐榜且 untried。处女地的核心任务不是"出 ACTIVE"，而是**用最少的波次建立区域实证 baseline**：哪些档位合法、哪些数据集有信号、金字塔配额怎么落。

## 流程变体（相对九步骨架）

### 步 1 注入：static 层强制实测

`get_platform_setting_options(region=ASI)` 实测合法 universe 档 / delay / instrumentType，**禁止照抄 USA 或任何区域档位**（matrix 硬规则 3）。实测结果回写 regions 表 static 层后再进步 2。

### 步 2 注入：全量探针模式

- 全部候选数据集过 `score_datasets.py` 三灯评分（步 2 见 [`../step2-s0.md`](../step2-s0.md)；旧的 `dataset_health_check.py` 兜底脚本已归档），按分数排探针优先级；
- 金字塔配额照旧（≥2 非 MODEL），但无 win 层可读，候选顺序 = 三灯分数 × 已知线索（analyst94/analyst81 优先）。

### 步 6 注入：首波探针豁免（一次性）

首波允许 **波内全探针**（豁免「弱探针最多 1 个波内配额位」约束一次），目的建 baseline；第二波起恢复正常约束，`max_probes_per_wave` 回落 1。

### 步 9 注入：强制回写加倍

处女地每个结论都是高价值实证：每波 verdict、每个数据集的探针结果（包括失败）必须回写 registry/ledger，**未回写视为本波未完成**（骨架已有，ASI 严格执行）。

## 避坑清单

- 禁止照抄他区 universe 档（CHN 默认档返空类事故的前科）。
- analyst94 近闸不等于可提交：OS 0.666 离闸还有距离，按 Mode A 微调路径走，不提前庆祝。
- 首波探针豁免仅一次：第二波仍全槽探针 = 违反填槽纪律。

## priors
- 拥挤数据集 TOP3（避免重复挖）：pv1(alphaCount=1419, cov=1); dl_riskfree_returns(alphaCount=350, cov=1); fundamental23(alphaCount=303, cov=0.75)
- 白空间候选（未测 + 覆盖≥60% + 低 alphaCount）：pv103(cov=1, alphaCount=0); pv149(cov=1, alphaCount=0); univ1(cov=1, alphaCount=0); socialmedia39(cov=0.94, alphaCount=0); other100(cov=0.88, alphaCount=0)
- 已判死（勿重试）：ASI-ANALYST11-ESG-DEAD, ASI-DL-ALT-GATES-ROBUST-WALL-20260921, ASI-EVNTWRK-MULTIDS-DEAD, ASI-IPV-INTRADAY-MOMENTUM-WEAK-20260924, ASI-PSM-VALUE-PSD-CNN-WEAK-20260921, ASI-S2IPV-NOCORESIG-SECTOR-DEAD, ASI-S2IPV-ROBUSTASIJPN-DEAD, ASI-SI5-MCR63-RSK70-CORRGATE-WEAK-20260921
- 实证笔记：analyst94: sharpe0.666最高Analyst数据集 | analyst81: score0.692推荐榜,OS sharpe0.653
