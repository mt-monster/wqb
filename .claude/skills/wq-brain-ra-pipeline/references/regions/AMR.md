---
region: AMR
entry_verdict: active
one_liner: "AMR（美洲）持续自我挖掘：TOP600 小宇宙 delay1，SUBINDUSTRY 跟 win，绿榜 analyst/insiders/pv 主攻 + Other/PV/Risk/ShortInterest 未点亮塔，8 探针快判死"
static:
  universe: [TOP600]
  universe_default: TOP600
  delay: [1]
  delay_default: 1
  neutralization_default: SUBINDUSTRY
  notes: "平台 get_platform_setting_options 实测（2026-09-16 / 2026-09-22）：AMR EQUITY 仅 TOP600（D0/D1 同）；中性化 7 选（NONE/STATISTICAL/MARKET/SECTOR/INDUSTRY/SUBINDUSTRY/COUNTRY），无 CROWDING/FAST/SLOW。AMR 实证仅 delay1，禁止 delay0 外推。"
datasets:
  red:
    - scope: family
      families: [chart_patterns, news_sentiment, ai_ml, credit_risk, glb_emotion]
      reason: "AMR 红榜（用户 2026-09-28 定案）：chart_patterns / news_sentiment / ai_ml / credit_risk / glb_emotion 一律排除；且 news/sentiment 在 USA/EUR/IND 跨区同型全灭（跨区负先验）。"
  green:
    - scope: family
      families: ["动态：绿榜 = analyst 系（评级/预期）/ insiders / pv 家族；S0 体检后落具体 dataset id"]
      note: "迁移自旧 green 行尾注释"
  yellow: []
priors:
  signal_families_include: [analyst, insiders, pv]
  signal_families_exclude: [chart_patterns, news_sentiment, ai_ml, credit_risk, glb_emotion]
  syntax_patterns: []
  win_recipes: []
gate_overrides:
  cw_gate: FAIL              # CW>0.5 = FAIL，判死不回炉（AMR 加严）
  longcount_min: 80          # longCount<80 = FAIL（AMR 加严，2026-09-28 用户口径 80）
  longcount_verdict: FAIL
  prod_corr_early_warn: 0.7
loop_policy:
  max_probes_per_wave: 8
  first_wave_probe_exemption: false
  fast_kill: "新数据集只给 8 条探针预算，无 |S|≥0.5 即写 dead_end 回写，不扩批、不换设置重试"
  stop_conditions: ["白名单被 dead_end 全覆盖", "连续 3 波全 FAIL 且无新 dead_end", "连续 3 波 gate 通过率=0"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(AMR)"
  last_verified: 2026-09-28
---

# AMR — 美洲持续自我挖掘区（处女地 → active）

## 定位与实证依据

AMR 是 config.REGIONS 14 区中最后补齐 profile 的区域（2026-09-28 补建）。静态层已实测：
**universe 仅 TOP600**（小宇宙，D0/D1 同档）、delay 仅 1（delay0 不外推）、中性化 7 选。
AMR 实证 **SUBINDUSTRY 中性化最优**（设置跟 win）；settings.json 静态档原为 MARKET，
2026-09-28 起按 win 实证改钉 SUBINDUSTRY。

目标（用户 2026-09-28 战役令）：持续自我挖掘 REGULAR alpha，**停止闸 = 20 个本次任务新挖的可提交 alpha**
（OS ACTIVE 或全部硬闸通过），不是默认 4 个。

## 数据集策略（金字塔优先）

- **绿榜优先**：analyst 系（评级/预期）、insiders、pv。
- **红榜排除**：chart_patterns / news_sentiment / ai_ml / credit_risk / glb_emotion。
- **点塔重点**：Other / PriceVolume / Risk / Short Interest 等未点亮类别；**禁用 MODEL 数据集**
  （白名单至少 2 个非 MODEL：PV/NEWS/ANALYST/institutions，优先 analyst 族上提）。
- 已点亮塔不进白名单主攻（其字段只能作辅助腿）。
- 命中死路族立即排除（**只认 registry_empirical 跨区 dead_end 的族级命中**），不抱"换参数复活"幻想。
  ⚠️ `campaign_intel s0-select` 的 `[跨区弱(参考):REG:maxS@bt]` **不是排除依据**（2026-09-30 实测无预测力，
  已移出排序键）；真正的跨区死路要走 `registry_empirical` 的 `dead_end` 族级检索。

## 流程变体（相对九步骨架）

### 步 1 注入：红黑榜 + 跨区死路硬排除

S-PRE 查表结果与红榜并集作排除集；候选数据集逐个做**不限 region 的跨区死路检索**
（risk70 教训：三区独立复现死族本可零成本排除）。

### 步 3 注入：VECTOR longCount 加严

typed catalog 必出 longCount + type；**longCount < 80 的 VECTOR 字段进观察名单，步 5 按 FAIL 处理**。
字段分级：users≥50 只做方向验证；users 10-49 进候选池、提交前实测 prod_corr；users 0-9 优先候选池（≥50% 批次预算）。

### 步 4 注入：事件形状替代 ts_event_*

事件类数据集不再生成 `ts_event_*` 裸 rank（103 算子清单未验证，event ops=[]）；
稀疏事件门控用 `trade_when` / `if_else` 趋势状态机 / `ts_arg_max` 时点 / `days_from_last_change` 新鲜度 /
`signed_power` 凸性等已验证形状。预设 **CW 必查**。

### 步 6 注入：设置跟 win + 8 探针预算

- 中性化钉 SUBINDUSTRY（win 实证）；decay/trunc 跟 settings.json（decay4 / trunc0.08）。
- **8 探针快判死**：新数据集只给 8 条探针预算，无 |S|≥0.5 即写 dead_end 回写，不扩批、不换设置重试。

### 步 7 注入：CW>0.5 判死不回炉

CW>0.5 的 alpha 直接判死（AMR 加严）；prod_corr ≥0.7 则 Mode B 换概念；
同一想法 >10 种结构仍不过则记 dead_end。

## 避坑清单

- 禁止 delay0 外推（AMR 实证仅 delay1）；TOP600 是唯一合法宇宙档，勿照抄 USA TOP3000 等档位。
- 事件类 `ts_event_*` 为未验证算子，直接用会整批 CANCELLED 连坐。
- CW>0.5 不回炉、longCount<80 不放行——两条加严闸不是 WARN。
- 新数据集 8 探针快判死不许"再换组设置试试"。
- 白名单外禁止 generate / simulate。

## priors
- 拥挤数据集 TOP3（避免重复挖）：analyst48(alphaCount=0, cov=None); pv17(alphaCount=0, cov=None); mfm_model_output(alphaCount=0, cov=None)
- 已判死（勿重试）：AMR-ANALYST48-DIVYIELD-GEOM-CEILING-WALL, AMR-PV37-TICKSTAT-SIGNAL-CROWDING-DEAD
