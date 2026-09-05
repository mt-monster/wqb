---
region: MEA
entry_verdict: frozen
one_liner: "TOP400 全区判死：9 数据集全 exhausted，入口即拒，仅留用户强制的 probe-only 后门"
static:
  universe: [TOP400]
  universe_default: TOP400
  delay: [1]
  delay_default: 1
  neutralization_default: STATISTICAL
  notes: "小宇宙，CW/longCount 问题放大，已无白名单内候选"
datasets:
  red: [pv106, fundamental6, model25, news 系, analyst 系, risk 系, insiders 系, shortinterest 系, option 系]
  red_reason: "9 数据集 campaign 状态全部 exhausted（含 pv106 spread 族判死）"
  yellow: []
  green: []
priors:
  signal_families_include: []
  signal_families_exclude: [pv106_spread]
  syntax_patterns: []
  win_recipes:
    - "早期 3 颗 ACTIVE（fundamental6/model25 时代），配方已被后续死路覆盖，不可复用"
gate_overrides:
  cw_gate: FAIL
  longcount_min: 80
  prod_corr_early_warn: 0.7
loop_policy:
  max_probes_per_wave: 1
  fast_kill: "frozen 态不适用；probe-only 后门单波 8 探针上限"
  stop_conditions: ["默认停止：全区 exhausted"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(MEA)"
  last_verified: 2026-08-25
---

# MEA — 冻结区

## 定位与实证依据

MEA TOP400 小宇宙，9 个数据集 campaign 状态**全部 exhausted**——不是没挖，是每一个都挖到判死并回写（pv106 spread 族死路为代表）。虽有 3 颗早期 ACTIVE（fundamental6/model25 时代），但对应配方已被后续死路覆盖，不可复用。小宇宙还放大 CW/longCount 数据质量问题。继续投入的期望收益 < 配额机会成本（同配额投 ASI 处女地或 IND 长窗期望更高）。

## 流程变体（相对九步骨架）

### 步 1 注入：入口即拒绝（frozen 核心变体）

执行到步 1 查表时：

1. `get_campaigns(MEA)` 全部 exhausted 且 `get_dead_datasets(MEA)` 覆盖全部候选 → **不进步 2**；
2. 直接向用户报告："MEA 已全区判死冻结（9/9 exhausted），建议转区"；
3. 调 `brain-nextMove-analysis` 产出选区建议（ASI/GBR/HKG 等 probe-only 区优先）。

### 唯一后门：用户显式强制 → 降级 probe-only

用户明确说"继续挖 MEA"时：

- 只探**白名单外新上线数据集**（status=untried 且不在红榜）；
- 单波 8 探针上限，一波结束无论成败都回到 frozen；
- 事先向用户声明配额成本，确认后执行。

### 解冻触发器（自动）

S-PRE 查表发现以下任一条件，`entry_verdict` 自动回升 probe-only 并提示用户：

- 平台新上线 MEA 数据集（campaign 表出现 untried 项）；
- Power Pool 主题匹配 MEA（PPA 分支，走骨架 PPA 流程）。

## 避坑清单

- 禁止"再试一次已 exhausted 数据集换参数"——死路 rule 优先于直觉（matrix 硬规则 2）。
- 早期 3 颗 ACTIVE 不构成复挖理由：其配方族已判死。
- frozen 不是删除历史：registry 中 MEA 死路记录是跨区铁律的语料（如 CW 通病），保留供其他小宇宙区（HKG/TWN）引用。
