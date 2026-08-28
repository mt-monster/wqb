# Task Plan: EUR REGULAR 持续挖掘 → 10 个可提交

## Goal
在 EUR 走完整 S-PRE→S6，产出 **10 个可提交 REGULAR alpha**（OS ACTIVE 或全部硬闸通过）后停止。judge READY 只报告、禁止自动提交。停止闸是 10 不是默认 4。

## Current Phase
Phase 5: S3 Wave40 五槽待提交（Wave39 已 closed PARTIAL，0 READY）

## Phases

### Phase 1: S-PRE campaign-matrix 查表
- [x] 区域静态档位（平台实测）
- [x] dead_ends / 跨区铁律 / 现有战役进度
- [x] OS ACTIVE / 配额 / Power Pool 主题
- **Status:** complete

### Phase 2: S0 体检锁定白名单
- [x] `score_datasets.py`：178 集，tier1=23，已入库 `s0_ranking`
- [x] `s0_whitelist` 锁定 23 个 tier1
- [x] 白名单之外不 generate、不 simulate
- **Status:** complete

### Phase 3: S1 字段理解 + 预处理决策
- [x] 跳过 `analyst_earnings_ibes`（EUR 实为 OHLC/回报面板，returns 墙）
- [x] 选定未挖正交集 `news85`（DNN 新闻情绪，MATRIX+VECTOR）
- [x] ideas：`output_report/EUR_delay1_news85_ideas.md`；ledger `s1_news85_d1`
- **Status:** complete

### Phase 4: S2 / S2-D / S2' 候选池 + 设置展开
- [x] S2-D news85：18 条模板式表达式（缺 backfill，未直接入槽）
- [x] S1 推荐 8 条 + MH/AIEQ 组合 32 条，wave_gate 5/5 PASS
- [ ] GEM news85 detached `gem_1787505326_a068a0`（供下一波）
- **Status:** in_progress

### Phase 5: S3 五槽填槽批量回测
- [x] 5×8 create_multi_simulation 已提交（COUNTRY/6）
- [ ] 盯盘回收 → S4
- **Status:** in_progress

### Phase 6: S4 评审链
- [ ] AlphaTest → Mode B 优先 / Mode A 其次 → 本地 self/PPAC → 归因 → 稳健性 → judge
- [ ] prod_corr ≥ 0.7 不提交、回 Mode B
- [ ] 跨数据集策略相关 < 0.4；每 10 次回测多样性评估
- **Status:** pending

### Phase 7: S5 提交纪律 + S6 复盘
- [ ] judge READY 后停下来报告，等用户确认
- [ ] 提交完成后 S6 回写 wave_results + registry_empirical
- [ ] 可提交数 ≥ 10 停止
- **Status:** pending

## Key Questions
1. 当前 OS ACTIVE 几颗？→ 1（`Wj71Q12o`），目标 10，缺口 9
2. 白名单是否覆盖未耗尽信号集？→ S0 后回答
3. Wave38 后下一波填槽内容？→ 必须先过 S0 白名单再定

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 只挖 Regular，不挖 PPA | 当前 Power Pool 主题是 GLB Liquid / TOPDIV3000，与 EUR 不匹配 |
| universe=TOP2500 delay=1 | 平台合法档；FCF 家族仅宽池有效；与已提交 `Wj71Q12o` 同档 |
| 中性化沿用 COUNTRY decay6 作主轨 | Wave35–38 实证近闸骨架；settings.json 默认 SUBINDUSTRY/4 作对照 |
| 禁止自动提交 | 用户铁律；judge READY 只报告 |
| prod≥0.7 → Mode B 换字段组合 | 禁止 Mode A 调参硬过；跨区铁律 PRODCORR-SATURATION |
| 停止闸 10 | 用户覆盖默认 4 |
| S0 标准按 EUR thresholds 放宽 | cov_hard_min=0.65、ac_max=1000、sweet_spot 开启；用户允许按实际情况放宽 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| `get_region_config("EUR")` region not found | 1 | 改用 `get_platform_setting_options` + `tracking/EUR/config/settings.json` |
| `get_campaigns("EUR")` 空 | 1 | 从 dead_ends + wave_results 重建候选/耗尽状态 |
