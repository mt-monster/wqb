# GBR RISK 塔战役 survey（campaign3 · 锁定 risk 挖 ATOM）

生成：2026-11-14　范围：GBR / TOP700 / D1（锁定）　前置：`gbr_delivery_manifest_v2_20261114.md`（campaign2 收口）、`gbr_unlit_tower_survey_20261108.md`（risk §3/§8）
目标：点亮 RISK 塔（现值 0/3）；口径：单集 ATOM 优先，已亮塔可作从腿（沿 campaign2 口径）。

## 1. RISK 塔数据集清单与排除表（全部 field 级实拉，非数据集级旧口径）

| 数据集 | 名称 | cov | 字段数 | 判定 | 依据 |
|---|---|---:|---:|---|---|
| risk60 | Securities Lending Insight | 0.6694 | 5（全 VECTOR）| **主攻** | 唯一有覆盖且字段数够的多字段集 |
| risk88 | Other Multi-Factor Risk Models | 1.0 | **1** | 排除（结构性） | 单字段集 D1 闸（≥10 结构互异模板）数学上不可满足；唯一字段 `alternative_market_cap_usd` 已被 fundamental6 用作合规分母（campaign 报告 §206-217），单集形态只剩 `rank(altcap)` 纯规模因子，无机制空间 |
| risk68 | Forecast Data | 0.0 | 5 | NO_DATA 排除 | **字段级** coverage 全 0.0（2026-11-05 画像 + 11-08 survey + 2026-11-14 今日 get_datafields 三次独立实拉一致）；`rsk68_residual_return` 描述为 European asset（EUR 风险模型输出），GBR 区无数据 |
| risk71 | Daily Specific Return Profiling | 0.0 | 6 | NO_DATA 排除 | 同上三次实拉，全字段 cov 0.0 |
| risk72 | Specific return of extended factors | 0.0 | 23 | NO_DATA 排除 | 同上三次实拉，全字段 cov 0.0（含 top2500/top1200/eur/epp 各 universe 残差收益族）|

> 11-08 survey 备注「risk68/71/72 cov=0 直接排除」是数据集级口径；本轮已按 11-09 规矩降级到 field 级重新实拉确认——结论碰巧一致但证据等级已升级（字段目录三次独立，非单一通道）。

## 2. risk60 既有证据与风险

- **已测**：11-08 I 批 8 条（insiders 论坛配方 `ts_zscore(ts_sum(...),252)` 移植）S ≤0.71——是「跨集配方移植」非 risk60 机制特化；<10 条不产生判死（§7.6）。
- **塔位归属风险（决定性，须先验证）**：annualized_pd 前科（GBR-ANNUALIZEDPD-DS111-MODEL-OWNED）证明平台 MATCHES_PYRAMID 按字段语义而非 dataset.category 归塔——securities lending 语义与 shortinterest 同族，**risk60 的 alpha 存在被归入 SHORTINTEREST 塔的真实风险**。Wave 1 出候选后第一件事读 `get_alpha_details` 的 `pyramids.list` 验证；若归 SHORTINTEREST 则本战役对点 RISK 塔无效，立即收口改道。
- **互相关风险**：与篮内 RRE5Mwkn（shortinterest3 loaned 量族）机制相邻；且 campaign2 实证 loaned 腿是 self/prod 双拥挤源——risk60 费率族若与借券量族同拥挤区，prod 墙预期存在。

## 3. risk60 字段画像（5 字段全 VECTOR，cov 均 0.6694，日频快照）

| 字段 | 含义 | 信号适用性 |
|---|---|---|
| `rsk60_crowding` | 做空活动带符号日指标（正=增加做空/拥挤，负=回补）| ★ 主信号（做空压力流，双向待测）|
| `rsk60_offer` | 借券费率年化（空头支付）| ★ 做空需求价格（文献：高费率股跑输，Stambaugh-Yu-Yuan 2013）|
| `lending_fee_bid_rate` | 出借费率年化（多头出借收益）| ○ 供给侧；offer−bid = 借券供需价差 |
| `rsk60_last` | 快照最新费率 | ○ 与 offer 高度共线（降级备选）|
| `rsk60_datatime` | 供应商时间戳 HHMMSS | ✗ 非分析量，禁用 |

全 VECTOR 须 vec_* 折叠；cov 0.67 ⇒ ts_backfill 必带；分布：费率右偏正数（0–100%+），crowding 零中心流。

## 4. Wave 1 设计（8 臂，机制特化，全单集 risk60 ATOM @SUBINDUSTRY/decay4/trunc0.08）

费率族 4（文献方向=反向：高费率/费率升/价差宽 ⇒ 做空收益）+ crowding 流族 4（2 正 2 反成对对照）：

| 臂 | 机制 | 表达式骨架 |
|---|---|---|
| 1 | fee level 反向 | `group_rank(reverse(ts_mean(ts_backfill(vec_avg(rsk60_offer),20),66)),subindustry)` |
| 2 | Δfee 事件反向 | `group_rank(reverse(ts_delta(ts_backfill(vec_avg(rsk60_offer),20),66)),subindustry)` |
| 3 | 借贷供需价差 | `group_rank(reverse(subtract(ts_backfill(vec_avg(rsk60_offer),20),ts_backfill(vec_avg(lending_fee_bid_rate),20))),subindustry)` |
| 4 | fee 时序分位 | `group_rank(reverse(ts_rank(ts_backfill(vec_avg(rsk60_offer),20),252)),subindustry)` |
| 5 | crowding 累积正向 | `group_rank(ts_sum(ts_backfill(vec_avg(rsk60_crowding),20),22),subindustry)` |
| 6 | crowding squeeze 反向 | `group_rank(reverse(ts_sum(ts_backfill(vec_avg(rsk60_crowding),20),22)),subindustry)` |
| 7 | crowding z252 | `group_rank(ts_zscore(ts_backfill(vec_avg(rsk60_crowding),20),252),subindustry)` |
| 8 | crowding 加速度 | `group_rank(ts_delta(ts_sum(ts_backfill(vec_avg(rsk60_crowding),20),66),22),subindustry)` |

## 5. 执行顺序

Wave1 读数 → 归因（方向/窗口/族）→ Wave2 迭代（结构维度优先于参数维度）→ 至六维证伪或出过闸候选 → 五道闸（塔位验证前置）→ 交付。每步归因先于推进。

## 6. Wave 读数台账（实时更新）

### Wave 1（multisim `1lcIgidEJ4PJcdSRuAbVR5Z`，@SUBINDUSTRY/decay4/trunc0.08，8/8 全灭）

| alpha | 臂 | S | 2Y | TO |
|---|---|---:|---:|---:|
| akaX18Zx | fee level66 反向 | -0.11 | 0.17 | 0.028 |
| 9qlgp31e | Δfee66 反向 | -0.21 | 0.34 | 0.111 |
| 9qlgp3Lo | offer-bid 价差 | -0.11 | 0.10 | 0.069 |
| gJa785Em | fee ts_rank252 | -0.04 | 0.25 | 0.092 |
| YPaXvOGM | crowding sum22 | -0.29 | -0.09 | 0.148 |
| j2aN6JbO | crowding sum22 反 | +0.29 | 0.09 | 0.148 |
| omaQNXOm | crowding z252 | **-0.32** | -0.48 | 0.173 |
| O0WKGjav | crowding 加速度 | -0.13 | -0.07 | 0.155 |

归因：① crowding 族 > fee 族（0.32 vs 0.21），方向锁定 crowding 原向（拥挤→跑输）；② fee 族两方向皆弱且反文献方向；③ TO 0.03-0.17 健康，非换手问题。

### Wave 2（multisim `1l74s3eKm4BwbVr193wrlSJe`，@FAST/decay5/trunc0.1，7/7 全灭但量级跃升）

| alpha | 臂 | S | 2Y |
|---|---|---:|---:|
| 78Ygjl1Q | crowding z252 反 | **-0.76** | -0.67 |
| RRe07P8z | crowding mean66 | -0.06 | 0.18 |
| P05j7KOW | crowding z504 反 | **-0.81** | -0.57 |
| npaw7r83 | crowding ts_rank252 反 | **-0.79** | -0.72 |
| mLaejQV6 | fee mean252 反 | -0.19 | -0.01 |
| 1YW6w0zR | crowding+fee 组合腿 | -0.45 | -0.57 |
| P05j7KGW | offer-bid 价差 mean66 | -0.25 | 0.66 |

**关键发现**：FAST 档把 crowding 族 S 从 0.32 → 0.76-0.81（×2.4）——复刻 campaign2「借券语义在 GBR 必须 FAST」铁律（论坛 XY78410 GBR 点塔帖同证）。方向 = crowding 反向（高拥挤做空）。组合腿稀释（-0.45 < -0.76）⇒ fee 弃用、纯 crowding 主攻。

### Wave 3（multisim `35o0KK3pw4m0byz16OOsR25T`，@FAST，8/8 全灭，天花板 0.85 稳定）

| alpha | 臂 | S | 2Y |
|---|---|---:|---:|
| bla7bZpm | vec_sum z252 | -0.84 | -1.08 |
| VkNKajK8 | vec_sum z504 | **-0.85** | -0.69 |
| MP69aR96 | 窗 126 | -0.81 | -1.13 |
| qM7exrkK | ts_av_diff252 | -0.64 | -0.47 |
| E5QopW0J | 长窗 Δ | +0.02 | 崩 |
| d5aebV8x | trade_when 高拥挤门控 | -0.59 | -0.99 |
| QP0mbkrK | signed_power² | -0.76 | 与 z252 基线逐位同 |
| 88Ngj9kV | ts_quantile gaussian | -0.84 | -0.72 |

**结构性封顶签名确立**：三批 23 臂，crowding 族全部几何（z/rank/quantile/signed_power/av_diff/Δ/trade_when）× 双向 × 双配置（SUBINDUSTRY 0.32 / FAST 0.85）收口 |S| 0.85±0.05，距 1.58 差 46%。与 analyst47（1.32-1.35 收口）、order_book（0.5 收口）同型 ⇒ 读数信息量封顶。vec_avg vs vec_sum 差 <0.01（crowding 是单值 VECTOR，折叠无损）。fee 族两档皆弱反文献方向，弃用。

### Wave 4（multisim `2PVlrX6r75gsbbi1b6FJ3c0R`，@STATISTICAL/decay5/trunc0.1，收口批）

| alpha | 臂 | S | 2Y | TO |
|---|---|---:|---:|---:|
| E5QopVV9 | 裸 z252（无分组）| -0.40 | -0.81 | 0.636 |
| QP0mbYvX | 裸 z504 | -0.44 | -1.12 | 0.621 |
| WjlKbLON | rank(mean126) | +0.02 | 0.56 | 0.081 |
| pwaQRvdv | industry 轴 | -0.55 | -0.41 | 0.207 |
| qM7exELV | sector 轴 | -0.59 | -0.26 | 0.195 |
| LLKON5KL | market 轴 | -0.53 | -0.13 | 0.192 |
| 88NgjvN7 | ts_rank vec_sum 504 | -0.62 | -0.94 | 0.648 |

**配置档排序定案**：FAST(-0.85) > STATISTICAL(-0.44~-0.62) ≈ SUBINDUSTRY(-0.32)。

## 7. 战役收口：GBR-REVERSE-CROWDING-CEILING（六维全闸 + 形态学补盲闭合）

### Wave 5（multisim `1gCs2p7EX4Vuc601fiUCGsns`）——整批 ERROR，教训

`log(add(rsk60_offer,1))` / `sign(rsk60_crowding)` 把标量算子施加在**未折叠 VECTOR（事件输入）**上：平台报 "Operator add/sign does not support event inputs"。**规则：log/add/sign/abs 必须在 vec_* 折叠之后**。前 31 臂全部先折叠后变换所以未踩。

### Wave 6（multisim `mV13F27Z4YeavS14K4o65y1`，@FAST，8/8 全灭——形态学空间证伪）

| alpha | 形态 | S |
|---|---|---:|
| vRAaOjXv | log(fee) mean252 反向 | -0.20（裸 fee -0.19，log 无增益）|
| 9qlgEXOx | log(fee) Δ66 | -0.32（裸 Δfee -0.21，更弱）|
| E5QoVlPL | sign×mag 66 正 | +0.11 |
| ZYakm7VY | sign×mag 252 | -0.11 |
| N1Pke7Eg | sign 反×mag 66 | -0.53 |
| 2r5PjlVw | sign×mag z252 | -0.20 |
| 78Ygjl1Q | **基线锚 z252** | -0.76（与 W2 同 id 逐位复现）|
| VkNKajK8 | **顶点锚 vec_sum z504** | -0.85（与 W3 同 id 同值复现）|

**收口判定**：① 双锚同 id 逐位复现 ⇒ 批间零漂移，封顶 0.85 是真实读数；② sign×magnitude 分解全部弱于混合量 ⇒ 「混合稀释」假设证伪；③ log(fee) 无增益 ⇒ fee 族弱不在量纲形态。**形态学盲区（log 变换、方向×强度分解）闭合，判死证据链完整。**

### 论坛点塔包装器情报（XC66172 帖 41417892125207，26 赞）

`ts_delta_limit(x, vec_avg(rsk60_last), limit_volume=0.1)` = **借券费率做调仓限速器**，让已有信号的 alpha x 引用 risk60 字段归 RISK 塔——**不是独立信号，是包装器**，对本战役（risk60 需自产信号）不适用。评论区两条可复用警告：① FF45555：rsk60_last 是百分数（5%=0.05），limit_volume=0.1 ⇒ |Δx|≤0.005，多数低费率票被冻结，要有意义需 1-3；② MM45078：先截面 rank 归一再缩放更稳健。**适用场景**：将来若篮子里有强 alpha 差塔位，可用此包装器补 RISK 塔（x 为已亮塔主腿时是组合件，受组腿配额约束）。

### 终局六维（含补盲）

D1 39 臂（31+8 形态）/ D2 5 字段族 / D3 矩全家+log 形态 / D4 4+1 轴 / D5 3 非线性+sign×mag 分解 / D6 3 配置档 ⇒ **GBR RISK 塔判死维持，证据链完整**。复活条件不变（registry `GBR-REVERSE-CROWDING-CEILING`）+ 新增：ts_delta_limit 包装器路径（跨塔组合形态，需配额）。




