# GBR INSTITUTIONS 塔战役 survey（campaign4 · 锁定 institutions 挖 ATOM）

生成：2026-11-14　范围：GBR / TOP700 / D1（锁定）　前置：campaign3 risk 塔收口（`gbr_risk_tower_survey_20261114.md`）
目标：点亮 INSTITUTIONS 塔（现值 0/3，pyramidMultiplier 1.4）。旧判死（10-30/31）早于 11-10 六维闸（§7.6），本 survey 按现行规则逐集重审后重开。

## 1. 数据集清单与六维重审（field 级实拉 2026-11-14）

| 数据集 | cov | 字段 | 旧证据 | 重审结论 |
|---|---:|---:|---|---|
| **institutions6** | **1.0** | 11 MATRIX | 4 臂探针顶 0.56（GBR-INSIDERS-INST-SINGLE-SIGNAL-DEAD）| **重开主攻**：<10 臂 PROVISIONAL 不产生判死；流机制从未测 |
| fund_holdings_panel | 0.93 | 18 VECTOR | 24 臂判死（boundary 族 F 墙）| **备选**：D1 疑够但 Herfindahl/conviction/大单族疑未测（D2 缺口）|
| institutions1 | 0.31 | 7 | insider 同源克隆，3 独立维度 | 维持排除（数据层语义） |
| institutions4 | 0.39 | 6 | 标识符映射 | 维持排除（数据层） |
| institutions25 | 0.0 | 24 | 字段级 cov=0（11-08 实拉）| 维持排除（NO_DATA） |

## 2. institutions6 字段画像（11 MATRIX，cov 全 1.0，报告期聚合，覆盖 5 万+ 机构）

| 字段族 | 字段 | 机制 |
|---|---|---|
| **持仓存量**（4）| aggregate_equity_value_{all_owners,institutions} / aggregate_share_count_{all_owners,institutions} | 机构化水平（institutions/all 比值=机构持股占比）|
| **计数流**（3）| count_institutional_{buyers,sellers,holders}_security | 净买家-卖家 = 聪明钱方向；holders Δ = 持仓广度动量（Chen-Hong-Stein breadth）|
| **量值流**（4）| quantity/market_value_institutional_shares_{acquired,disposed} | 净流比率 (acq−disp)/(acq+disp) = 机构净流强度 |

MATRIX 无需折叠（campaign3 vec 陷阱不适用）；报告期数据 ts_backfill(66) 必带；ac 99-212 说明全平台高频使用。

## 3. 机制先验（本区已证定律迁移）

1. **量族活、价族死**（risk60 实证）：股数/计数流 > 费率/价格流 ⇒ institutions6 全量族构成是好先验
2. **借券/机构语义必须 FAST**（campaign2+3 双实证）：SUBINDUSTRY/STATISTICAL 档预期弱 2-3 倍 ⇒ Wave1 直接 @FAST/decay5/trunc0.1
3. **同字段多窗叠加 ρ≈0.8 增益≤0.05**（campaign3）：叠加臂只作增量微调不作破闸主力
4. **持仓广度动量**（Chen-Hong-Stein 2002）：breadth（持有人数）上升预测收益上升——holders Δ 是文献正方向
5. **机构流 herding**（Sias 2004 / Nofsinger-Sias 1999）：机构净买卖与收益正相关但拥挤；net flow 反向（高买→跑输）在 GBR 大盘蓝筹上待测双向

## 4. Wave 1 设计（8 臂流机制，institutions6 单集 ATOM @FAST/decay5/trunc0.1）

| 臂 | 机制 | 表达式骨架（MATRIX 无折叠）|
|---|---|---|
| 1 | 净买家-卖家计数（水平）| `group_rank(ts_backfill(subtract(buyers,sellers),66),subindustry)` |
| 2 | 净计数 z252 | 同 + ts_zscore |
| 3 | 净量流比率 | `(acq−disp)/(acq+disp+1)` backfill66 |
| 4 | 净值流比率 | 同（value 版）|
| 5 | 广度动量（正向）| `ts_delta(holders,66)` |
| 6 | 机构化水平 | `share_count_institutions / share_count_all_owners` |
| 7 | 机构化 Δ126 | 比值 ts_delta |
| 8 | 净计数多窗叠加（W3 定律微调）| z252+z504 add |

## 5. 塔位警示

fund_holdings_panel/institutions6 的 alpha 归属须候选出闸读 `pyramids.list` 验证（annualized_pd→MODEL 前科）；机构持股语义理论上归 INSTITUTIONS，但 MATCHES_PYRAMID 按字段语义判——测完第一批即验。

## 6. Wave 读数台账

### Wave 1（`2SWb5Ubsc4Zt9jF1f1nlKG7r` @FAST，6/8 有效 + 2 量纲拒）
净计数流正向弱（0.23-0.39，多窗叠加最高）；机构化Δ **-0.78 负向**（机构占比升→跑输=拥挤）；广度动量 -0.27 反文献；量纲陷阱：`quantity_institutional_shares_*` 分母加常数被拒（Unit[CSShare]）。

### Wave 2（`qgQl0g6d4s3cHP16kVx2NJH` @FAST，7/8）
机构化Δ 反向版全弱（2Y 全负）⇒ W1 的 -0.78 是 fluke；**价值版（市值比）反向 z252 +0.64** 新面孔；计数比归一版 +0.42/2Y0.63。

### Wave 3（`4k3vlGgST4PxbTacS9VYaGF` @FAST，8/8）
**价值版 ts_rank252 反向 0.82/2Y0.66/sub0.74**（ts_rank > zscore 0.64）；跨族叠加 0.76 不超最强单腿（ρ 仍高）；计数比 z504 2Y0.90 近年强。

### Wave 4（`13czsyTV4hZbSZf8DQQgzB` @FAST，8/8）
**跨族双 rank 叠加 0.97/2Y1.15**（0.82+0.50→0.97 超最强单腿——跨族 ρ 低，叠加定律的同族/跨族分界实证）；价值版 backfill252 单腿 0.90。

### Wave 5（`2Du3ykejM4LBblYntwIhd3f` @FAST，8/8）★顶点
**rK7QwdrJ 三腿叠加 S1.19/F0.57/2Y1.84/sub0.72/TO0.131/ra=2**（价值反向+净买卖比+广度动量等权）；塔位验证 pyramids.list=[GBR/D1/INSTITUTIONS×1.4] ✓；计数腿窗1008 1.03/2Y1.50 次优。

### Wave 6（`VmZKFasP5k18SWzI3AnwDZ` @FAST，7/8 + 1 量纲拒）参数盆地实锚
全变体塌回 0.13-0.73（窗/轴/腿替换/长窗全套）——三腿组合是**窄峰非平台**，(126,252)+(66,504)+(66,66)+subindustry+FAST 唯一峰值。

### Wave 7（`1akXiQ6Fm5dabR2yB445S2p` @SUBINDUSTRY/decay4/trunc0.08，2 臂去重为 1）
同式 **0.53**（vs FAST 1.19）——机构语义必须 FAST 三度复证，D6 配置对照补齐。

## 8. 归因勘误（2026-11-14 深夜，W8 发现）+ Wave 8/9

### ★勘误：W5 顶点结构错标（children 顺序错位映射）

W5 收口时把 1.19 归给了「三腿叠加」——错。逐字核对提交回显：**rK7QwdrJ 真身 = 双腿混轴**：

```
group_rank(reverse(ts_rank(ts_backfill(机构市值比,252),252)),subindustry)   ← 价值腿 @sub
+ group_rank(ts_rank(ts_backfill(净买卖比,66),504),industry)               ← 计数腿 @industry 混轴
```

三腿版（+广度动量，sector）真身是 mLaeNYz1 = **0.50**；W6 整批「参数盆地」扫的是错误骨架（三腿本底 0.50，变体 0.13-0.73 全部正常）；W3「sector 单腿 0.60」结论同样错位——W5 真次强臂是 YPaXOxkA（**全 sector 双腿 1.03/2Y1.50**）。真实爬升链：0.97（双腿 sub）→ 1.03（双腿 sector）→ **1.19（双腿混轴）**——杠杆 = backfill 126→252 + 计数腿换 industry 轴。

### Wave 8（`1H9aXS3sx4kj9Cm5S4DMcRD`）：错误骨架上验证（读数作对照层保留）

三腿基线 0.50 复现；三腿+组合腿 0.47-0.65（全不超错误基底）；**臂8 e7aeP6q6 0.85 用了 volume/adv20 破 ATOM，仅作参照不入交付**。

### Wave 9（`3ZXHZO4Q84Yp9tQ172picajd`）：真顶点邻域 + 组合腿（全出）

| alpha | 结构 | S | 2Y | sub | 备注 |
|---|---|---:|---:|---:|---|
| rK7QwdrJ | 真顶点锚 | 1.19 | 1.84 | 0.72 | 同 id 同值复现 ✓ |
| QP0m8QNr | +news50_ess 腿 | 1.20 | 1.45 | 0.88 | |
| **P05jV1Yp** | **+anl47_indicator 腿** | **1.21** | 1.40 | **1.09** | ★双塔 effective=2 |
| kqaeAKW8 | +news50_aes 腿 | 1.12 | **2.15** | 0.58 | 2Y 最佳 |
| qM7eRXY2 | +ern6 SUE 腿 | 1.19 | 1.43 | 0.71 | |
| WjlK5g3k/78Ygpd3L/1YW6MgOM | 混轴反排/全 industry/长窗 | 0.74-0.99 | — | — | 混轴方向确认（sub主+ind辅） |

**P05jV1Yp 尽调**：机构双腿 + anl47_indicator z252 第三腿（analyst47 已亮塔作从腿，口径允许；**pyramids effective=2：INSTITUTIONS×1.4 + ANALYST×1.6**）。十年逐年：9/10 年 pnl 正、仅 2017 弱负（-0.33/-68k）、2018-2023 六连正、2023 S2.62；lc447/sc462 健康。挂三闸：S 1.21<1.58 / F 0.55<1.0 / IS_LADDER 1.40<1.58@4Y；SUB 1.09 / TO 0.173 / CW 全过。self-corr 测算中（OS 池下载超时重试）。

**W9 结论**：组合腿方向全胜（四腿全部 ≥1.12 且不破 ATOM 外规则——已亮塔作从腿合法），但增益 +0.01-0.02 不足以破 S/F 闸；混轴杠杆确认（industry 计数腿 +0.22 是唯一显著结构增益）。**institutions 主线 S 天花板 1.19-1.21 实锚**，破 1.58 需要新的正交强腿或配置层突破，本批未找到。

## 9. ★★★ 违规格检（2026-11-14 深夜，用户质询命中毒模式）

**用户质询「add(A,B) 不是毒模式吗」命中组合形态铁律 §0**（docs/experience/02_signal_patterns.md §1：禁止独立信号腿等权相加，含 add(rank(A),rank(B)) 全族；事故先例 QPbp025Q S2.11 已作废；"门禁通过≠合规，判合规看本质"）。

**逐条核验结果**：

| 候选 | 结构 | 判定 |
|---|---|---|
| P05jV1Yp 1.21 / rK7QwdrJ 1.19 / W4 双腿 0.97 / 组合腿四臂 1.12-1.21 | add(独立腿A, 独立腿B[, C]) = 0.5A+0.5B | **全部违规作废** |
| risk60 z252+z504 | 同形态仅窗口差异 | 合规（白名单：单信号多窗平滑）|

**整条"叠加爬升链"从 W4 起作废**。合规沉淀：
- 单腿读数真实有效：**价值腿 backfill252 ts_rank252 反向@sub = 0.90**（合规天花板）、计数腿 ts_rank504 = 0.50、广度动量 = 0.11；
- institutions6 合规天花板修正为 **0.90**（距闸 0.68），PROVISIONAL 判死维持、证据链改单腿基准；
- 后续合规重构方向 = Mode B（ts_scale / subtract(rank,rank) 须有经济含义 / group_rank 单信号 / trade_when·if_else 门控）——**不得再走 add 多腿路线**（registry 已改写）。

wave_result `campaign4_inst_compliance_20261114` FAIL closed（违规格检记录）。

## 7. 收口（W7 时点；§8 勘误与 §9 违规格检后，结论已并入）


- **天花板 S1.19**（ra=2，只差 S/F/2Y 三闸），GBR 未点亮塔战役最接近的线（risk60 0.88 / ern6 纯 SUE 反号 / obk 0.57）。
- 55 臂 7 批，六维闸全闭合（D1 结构模板 ✓ D2 三字段族 ✓ D3 矩全家 ✓ D4 三轴 ✓ D5 非线性 ✓ D6 两配置）⇒ **PROVISIONAL 判死**（窄峰到顶，参数盆地证明继续微调无望）。
- registry `GBR-INST6-TRILEG-CEILING`（复活条件：跨塔组合腿/数据更新/backfill 邻域）。
- ★方法论产出：**跨族叠加有效（0.82+0.50→0.97）与同族叠加无效（+0.03）的分界 = 腿间相关性**——三字段族（存量比/净买卖比/广度动量）是 institutions6 内天然的低相关腿组，这解释了为什么本集能到 1.19 而 risk60 单机制只能 0.88。
- 回写：wave_result `campaign4_inst_tower_20261114` PARTIAL closed。
