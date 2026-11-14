# Wave BA2 dispatch — risk60 十模板池（MG 翻转升级）+ risk88 收尾（2026-11-10）

> 触发：BA1 探针费率/拥挤面 6/7 同号（翻转 +0.55 天花板）⇒ 按 shortinterest3 冠军骨架升级模板池（判据 MX：换骨架重测判死族）。
> 这是「撤判重开」阶梯第二步：BA1 探针（不判死）→ BA2 模板池（六维证据）→ 才能对 risk60 出合规终判。

设置：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nanON/maxTradeOFF（全战役统一档）

| # | 模板 | 表达式要点 | 算子 |
|---|---|---|---:|
| P1 | offer 费率 x 冠军骨架（tvr_decay 双窗 264/132 x 翻转） | -group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(bf264)), rank(ts_delta(bf132))), tvr=0.03), sub) | 11 |
| P2 | bid 费率 x 冠军骨架 | 同上，字段 lending_fee_bid_rate | 11 |
| P3 | crowding x 冠军骨架 | 同上，字段 rsk60_crowding | 11 |
| P4 | 费率水平 x industry 轴 | -group_rank(ts_mean(bf,66), industry) | 4 |
| P5 | 费率长窗 zscore 252 | -group_rank(ts_zscore(bf,252), sub) | 4 |
| P6 | crowding 单窗 delta66 x tvr_decay | -group_rank(ts_target_tvr_decay(ts_delta(bf,66), tvr=0.03), sub) | 6 |
| P7 | bid 费率 delta132 x tvr_hump x industry | -group_rank(ts_target_tvr_hump(ts_delta(bf,132), tvr=0.03), industry) | 7 |
| P8 | 费率 ts_rank 252（非线性）x industry | -group_rank(ts_rank(bf,252), industry) | 4 |
| P9 | risk88 市值 delta66 反转 | -group_rank(ts_delta(alt_mc,66), sub) | 3 |
| P10 | risk88 市值 52w 位置 x industry | group_rank(ts_rank(alt_mc,252), industry) | 3 |

六维对照：D1 互异模板 10 条 ✓ / D2 四字段族（offer/bid/crowding/市值）✓ / D3 矩全家（水平/一阶差/二阶波动）✓ / D4 sub+industry ✓ / D5 非线性（ts_rank/tvr_decay/tvr_hump）✓ / D6 单配置（若池内出现 ≥1.2 活件再补第二配置）。

预期与出口：池天花板 <1.58 ⇒ risk60 合规终判死（证据归档）；≥1.5 ⇒ 逐闸破墙（与 E569ZE7L 借券族互相关是第一道坎，同机制先查 self/prod）。
派发状态：后台退避重试（cache/_watchBA2_retry.ps1，429 时 90s 间隔），成功后 sim id 落 cache/_out_BA2_dispatch_ok.json。

---

## BA2 收割（sim 4zZbZXgO94kg9Me1df9E0bqg，10/10 COMPLETE，0 error）

| # | 模板 | alpha | S | 2Y | sub | TO |
|---|---|---|---:|---:|---:|---:|
| P1 | offer x 冠军骨架 | 9qlzYKwr | **0.90** | 0.49 | 0.69 | 0.033 |
| P2 | bid x 冠军骨架 | 1YWqeL7K | **0.84** | 0.30 | 0.67 | 0.033 |
| P3 | crowding x 冠军骨架 | gJaY6K1l | -0.08 | — | — | — |
| P4 | offer 水平 x industry | e7almK0p | 0.65 | 0.81 | 0.53 | 0.025 |
| P5 | offer zscore 252 | leaLd2lx | 0.76 | 0.87 | 0.45 | 0.087 |
| P6 | crowding delta66 x tvr_decay | blaYXMqN | -0.11 | — | — | — |
| P7 | bid delta132 x tvr_hump x industry | A1xR9bPl | 0.47 | -0.14 | 0.49 | 0.022 |
| P8 | offer ts_rank x industry | O0W1OkZR | 0.54 | 0.76 | 0.13 | 0.114 |
| P9 | risk88 市值 delta66 反转 | KPgK3691 | 0.75 | 0.45 | 0.30 | 0.106 |
| P10 | risk88 市值 52w rank x industry | XgajGL8X | 0.43 | 0.34 | 0.39 | 0.138 |

**归因**：
1. 冠军骨架确实抬升族天花板（探针 +0.55 → 池 **0.90**，判据 MX 再验证），但 0.90 距 1.58 差 0.68。
2. **信号全部长在费率面**（offer/bid：0.90/0.84/0.76/0.65/0.54/0.47）；**crowding 字段两读数全灭**（-0.08/-0.11）——有符号流量读数无定价力。
3. **2Y 全档偏弱**（0.30-0.87）：费率信号近年衰竭，与 shortinterest3 费率变体 2023 崩塌同构——即使 S 过线 2Y 闸也过不去。
4. risk88 单字段族三维读数（level 0.11 / delta 0.75 / ts_rank 0.43），天花板约 0.75。

**处置**：BA2b 补 D6 第二配置（universe 变维 TOP800 x3 + CROWDING 中性化 x1，get_platform_setting_options 已确认 DEU D1 可用）⇒ 之后 risk60/risk88 出六维合规终判。

## BA2b 派发（D6 补测，双 multisim）

- 首派两连拒：① TOP800 invalid，报错提示 Valid:[TOP500,TOP300] 但 **TOP300 照样被拒**（平台两层校验自相矛盾）⇒ **DEU D1 EQUITY 实际仅 TOP500**，宇宙变维不可用；② 单条 multisim 被拒（**最少 2 条**）。首派 CROWDING 单条疑成孤儿（id 未捕获，不追踪）。均记 Agent Memory。
- **最终 BA2b v3**：单 multisim 4 条（P1/P2/P5/P9）@ TOP500/**STATISTICAL**（中性化变维，满足 D6「至少变一维」）。
- watcher：cache/_watchBA2B.ps1 v2（部分派发成功也可追踪）。

---

## BA2b 收割（sim 4z4UH36EM4n7avEctlWf8tz，4/4 COMPLETE，0 error）

| # | 表达式 | alpha | 配置 | S | 2Y | sub | TO |
|---|---|---|---|---:|---:|---:|---:|
| Q1 | P1 offer 冠军骨架 | pwaqX6QX | TOP500/STATISTICAL | 0.40 | 0.01 | 0.23 | 0.084 |
| Q2 | P2 bid 冠军骨架 | 78YkAwgQ | TOP500/STATISTICAL | 0.35 | -0.13 | 0.18 | 0.084 |
| Q3 | P5 offer zscore 252 | d5a2Xxex | TOP500/STATISTICAL | 0.59 | 0.85 | 0.30 | 0.132 |
| Q4 | P9 risk88 市值 delta 反转 | vRAKqLaA | TOP500/STATISTICAL | 0.79 | 0.09 | 0.39 | 0.151 |

**D6 结论（配置层判读）**：换 STATISTICAL 中性化后全部**降级**（P1 0.90→0.40、P2 0.84→0.35、P5 0.76→0.59；P9 0.75→0.79 持平）⇒ SUBINDUSTRY 配置下的读数不是配置放大产物，但**信号在更干净的中性化下反而更弱**，进一步坐实「天花板远离 1.58」。无配置层救法。

## risk60 / risk88 六维合规终判（2026-11-10，新闸首例结案）

| 维度 | risk60 | risk88 |
|---|---|---|
| D1 结构互异模板 | ✓ 22 条跨 3 波（BA1 探针 9 + BA2 池 10 + BA2b 变维 3） | ✓ 6 条跨 3 波 |
| D2 字段族自测 | ✓ offer / bid / crowding 三族实测（crowding 全灭 0/4） | ✓（单字段族，level/delta/ts_rank 全测） |
| D3 矩全家 | ✓ 水平/一阶差/二阶波动/费差/IR | ✓ level/delta/rank |
| D4 分组轴 | ✓ subindustry + industry | ✓ subindustry + industry |
| D5 非线性 | ✓ ts_rank / tvr_decay / tvr_hump | ✓ ts_rank |
| D6 配置 | ✓ TOP500/SUBINDUSTRY vs TOP500/STATISTICAL（全降级） | ✓ 同 |
| **族天花板** | **0.90**（P1，SUBINDUSTRY；STATISTICAL 下 0.40） | **0.79**（Q4） |
| **终判** | **信号层死（六维合规）**——距 1.58 差 0.68 且 2Y 全档 0.30-0.87 弱 | **信号层死（六维合规）**——单字段族天花板 0.79 |

**判据升级**：MH「risk60 是同机制更弱源」由先验升级为实测事实（证据链：22 条探针/池 + 2 配置）。shortinterest3 的冠军骨架在 risk60 费率面上只能出 0.90，且 2Y 结构性偏弱（与借券费率变体 2023 崩塌同构）——即使过 S 线也过不了 LOW_2Y_SHARPE。
**波 N 原判死结论维持，但证据基础已从「~5 条无 backfill 探针 + MH 先验」升级为六维合规证据链；本次撤判-重开-复判闭环用时约 1.5 小时、4 波。**

⇒ RISK 塔结案：risk60/risk88 信号层死（合规），risk68/71/72 数据层排除（无供数）。塔内 0 颗，无遗漏矿脉。