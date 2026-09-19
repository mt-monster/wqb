# Findings & Decisions

## Requirements
- Region: KOR；type=REGULAR；目标 20 颗本次新挖掘可提交 alpha 后停止
- 完整 S-PRE→S6，不跳强制闸；campaign-matrix 查表 → S0 白名单（可放宽 cov≥0.6, α≤1500, f≥10）
- 重点 Other / PriceVolume / Risk / Short Interest 未点亮集（可先不体检）；不要 MODEL
- 1-2 字段/表达式；prod_corr≥0.7 不提交；跨策略相关 <0.4；多样性评估
- judge READY 停下来报告等确认；用户确认后按绩效最好先提
- 最后输出 skills/workflow/db/code 全面优化方案

## Research Findings
- KOR profile: entry_verdict=active；universe=TOP600；delay=1；neutralization=STATISTICAL
- 红灯：chart_patterns / news_sentiment / ai_ml / credit_risk（用户点名 Other/PV/Risk/SI 时：Risk 与 credit_risk 红灯冲突 → 用户指令优先，但 credit_risk 族仍按 dead_end rule 提示）
- 绿榜：analyst / insiders / pv
- win 配方：分析师评级修正 × SH（shortinterest/holders）混合（2 颗 ACTIVE）
- 闸门加严：CW>0.5 FAIL；longCount<80 FAIL
- 8 探针快判死：新数据集无 |S|≥0.5 即判死
- D11：KOR 探针波连续全灭，复杂跨数据集混合模板才出 RA
- 用户明确不要 MODEL、不要频繁换数据集、1-2 字段为主

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 停止闸=20 | 用户覆盖 D9 默认 |
| S0 放宽 + 重点类可先入候选 | 用户覆盖 D4 硬地板 |
| 并发：五槽填槽 + 8 并发 multi_create | 用户覆盖七槽默认；INDEX 注禁同账号≥8 齐射，执行时锁到平台实测 C |
| 规划文件在项目根 | planning-with-files |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
|       |            |

## Resources
- RA SOP: `~/.qoder-cn/skills/wq-brain-ra-pipeline/SKILL.md`
- KOR profile: `~/.qoder-cn/skills/wq-brain-ra-pipeline/references/regions/KOR.md`
- Matrix: `~/.qoder-cn/skills/wq-brain-campaign-matrix/SKILL.md`
- Toolkit: `~/.qoder-cn/skills/wq-brain-campaign-toolkit/`
- DB: `data/wqb.db`
- Campaign dir: `tracking/KOR`

## Visual/Browser Findings
-
