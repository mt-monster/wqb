# Task Plan: EUR D1 三个可提交 RA

## Goal
在 EUR Delay=1 Regular 上挖到 **3 个硬闸门可提交** Alpha（当前 PPA 主题是 GLB/D1 TOPDIV3000，EUR **不能**当 PPA）。只在体检白名单甜点区挖掘。不 POST 提交（配额 remaining=0，且由用户手动提交）。

## Current Phase
Phase 2 generate：白名单下一集 `ai_factor_transfer` MATRIX GEM

## Phases

### Phase 1: 诊断与体检
- [x] 当日 nextMove（已完成，NY 2026-08-13）
- [x] EUR TOP1200 体检白名单 19 集
- [x] 跳过已证伪：nsnlp / mlfp / dl_riskfree / ibes
- **Status:** complete

### Phase 2: GEM → inspect → batch sim（ai_factor_transfer）
- [ ] makeSomeGem MATRIX
- [ ] inspect 8 条 + INDUSTRY/STATISTICAL
- [ ] simAlphasinBatch batch-size 8
- **Status:** in_progress

### Phase 3: 闸门与稳健性
- [ ] Sharpe≥1.58 Fitness≥1 TVR 5–20% 2Y>1.58 PROD<0.7 SELF<0.5 CW
- [ ] 到 3 个可提交（不同数据集优先）
- **Status:** pending

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 不重跑 nsnlp/mlfp/dl_riskfree/ibes | 本战役 max Sharpe≤0.48，再 GEM 浪费配额 |
| 下一集 ai_factor_transfer | 白名单第 4：cov=1.0, alphaCount=0, 20 个 MATRIX 字段 |
| 体检 MCP 失败自动直连 | 8876 拒绝连接曾卡住选集 |
| 配额=0 仍回测 | 先攒可提交，8/15 ET 后再谈提交 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| health_check MCP 8876 ConnectionRefused | 1 | 脚本自动回退 --mode direct |
