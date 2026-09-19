# KOR insiders5 — S1 字段理解与信号假设（回填 2026-09-09）

> 数据集：`insiders5`（KOR / TOP600 / D1 / **VECTOR** 53 字段，signal 36 / scale 6 / metadata 4 / date 7）
> 目录快照：ledger_kv `KOR/catalog_insiders5`（fetched 2026-09-07）。
> 本文档回填自真实字段目录与 w177–w181 已过闸表达式设计，S2→S3 断链修复用。

## 一、特征字段分级（prod-corr 规避口径）

**users ≥ 50（不投入候选打磨，仅方向验证）**：
`insd5_rpst_grp_typ`(162)、`insd5_source_data`(201)、`insd5_source_real_data`(173)、
`insd5_source_real_ratio`(100)、`insd5_real_ratio`(57)、`insd5_ghc_tr`(69)

**users 10–49（进候选池，提交前必测 prod_corr）**：
`insd5_tnc`(132→超标，仅作分组/桶)、`insd5_source_ratio`(118)、`insd5_ratio`(46)、`insd5_fa_tr`(38)、
`insd5_vol_chg`(37)、`insd5_real_data`(52)、`insd5_fb_tr`(26)、`insd5_trd_amt`(22)、
`insd5_c_company_pyt_tkm`(22)、`insd5_trd_reason_b`(22)、`insd5_officer`(20)、`insd5_group_s`(19) 等

**users ≤ 9（理论 prod≈0，优先候选）**：`issuance_category`(8)、`security_type`(5)

**VECTOR 注意**：全部 VECTOR 字段消费前必须 `vec_avg/vec_stddev/vec_count`；
KOR 小宇宙 longCount<80 按 FAIL 处理（profile gate_overrides）。

## 二、机制假设（概念优先）

1. **内部人增减持动量/反转**：`insd5_vol_chg`（成交股数变化）、`insd5_ghc_tr`（持股比例变化），
   经 `ts_delta(…, 66)` 与 `ts_backfill(…, 22)` 平滑后做行业内排名 → 内部人净买入的行业相对强度。
2. **内部人集中度**：`insd5_tnc`（特殊关系方数量）与 `insd5_trsy_*`（库存股）作为**公司治理/股权结构**代理，
   高集中 + 库存股变化 → 信息不对称强度。
3. **成本/流动性交叉验证**：`pv106_lastspreadbp` / `pv106_wli_spreadbp` / `korean_market_slippage` /
   `bid_ask_price_gap`（PV 族辅助腿）——内部人信号在低交易成本股票上更可信（成本摩擦稀释假信号）。
4. **条件触发**：`if_else(greater(Δ(内部人比例,66), ts_mean(Δ,252)), 组合信号, 0)` ——
   仅在内部人行为显著超出自身一年常态时开仓，压 turnover 与 CW。

## 三、分组与骨架约定

- 行业分组：`pca_industry_grouping_method1_20clusters`（group_* 操作符消费）；
  成本桶：`bucket(rank(...), range="0,1,0.2")`。
- 主骨架（w177–w181 实际形态）：
  `rank(add(rank(group_rank(ts_delta(ts_backfill(vec_avg(<insider 字段>),22),66), <group>)), rank(rank(ts_backfill(<pv 价差字段>,22)))))`
- 辅助腿轮换：eps_estimate_4wk_change（analyst 上修，与 insider 双确认）。

## 四、门禁与设置

- 设置：TOP600 / D1 / SECTOR 或 STATISTICAL / trunc 0.08（跟 win 配方 STATISTICAL decay4 族）。
- 已过 wave_gate：`gate_w177..w181_insiders5`（ledger_kv，2026-09-07）。
- CW 风险：事件类字段（trd_amt/vol_chg）稀疏，表达式必须带 ts_backfill；
  步 7 review 时 CW>0.5 直接判死（KOR profile）。

## 五、挖掘建议（S2 生成与 S3 回测建议）

1. 主力槽给 `insd5_vol_chg / insd5_ghc_tr / insd5_trsy_ratio` 的 ts_delta(66) 行业内相对强度（内部人行为主信号）。
2. 每槽先 1–2 条骨架查平台 prod_corr：insiders 族在小宇宙用户数中等，期望 prod 可控，但 w179 的 analyst 上修腿有饱和风险（users 38+）。
3. CW 防线：事件类字段必须 ts_backfill + 组内 rank；步 7 review 时 CW>0.5 直接判死不回炉（KOR profile）。
4. 设置跟 win：STATISTICAL / SECTOR，decay 4–22，trunc 0.08；禁止 delay0 外推。
5. 8 探针快判死：新骨架 |S|<0.5 即回写 dead_end，不扩批。
