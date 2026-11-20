# EUR 未点亮塔 ATOM 穷尽审计（2026-11-19，ATOM 优先标准下的交付物重定）

> 触发：用户 2026-11-19 更正交付物标准「ATOM 优先」——前一轮 10 颗跨集 regular 不满足修正后标准，须重新按 ATOM 先挖、穷尽举证后才能 fallback regular（AGENTS §7.7）。
> 本档案记录**本轮新增的 ATOM 证据**（全部本会话平台实测），与 `EUR_atom_priority_assessment_20261119.md`（03:0x 版）合并构成完整穷尽举证。
> 全程 EUR/D1，未提交任何 alpha。

## 0. 本轮新增的四条决定性证据（先看结论）

| # | 数据集（塔） | 新证据 | 判定 |
|---|---|---|---|
| 1 | **pv47**（PV，未点亮） | EUR 首测 24+ 臂、六维闭合：S 1.68–1.99、F 可过（1.01–1.06）、sub 可过、TO 可过、十年满仓 ✓——**唯独 2Y 天花板 1.05–1.27 < 1.58**，逐年定位 2018（S0.35）/2022（S0.87） | 信号层·2Y 时效死（PROVISIONAL 族级） |
| 2 | **earnings_sent_matrix**（EARNINGS，1/3） | 换信息源成功：`method1`/`method2` 从未作过方向信号，本轮各出**全闸 ATOM**（S1.99/F1.42/2Y1.98/RA0；S1.91/F1.36/2Y1.82/RA0）——但 **prod 0.9229/0.8797 撞墙**。全数据集 4 颗全闸件 prod 0.871–0.923 | 信息源级 prod 墙（PROVISIONAL） |
| 3 | **fund_holdings_panel**（INSTITUTIONS，0/3） | 复核确认：除 prod 外全闸 1 颗（zq378ELo prod 0.8887）+ 2014 全年零持仓（数据 2015–2023 九年，**用户 2026-11-19 已放宽年限约束，数据层不再排除**） | **prod 墙**（唯一缺口 0.19，算术不可达） |
| 4 | **pv13**（PV，未点亮） | rel_ret 关联溢出族（Cohen & Frazzini 2008 机制）6 臂探针全灭（\|S\|≤0.28，TO 17–40% 且无方向） | 探针级判死（唯一信号族；其余 70 字段为分组轴/映射元数据/静态图分） |

## 1. pv47 验尸（本轮最大新增投入，六维闭合）

**数据集**：`pv47`，2 字段（`pv47_spret` / `pv47_for_statssimple_only_spret`，均为 UBER 风险模型日度特异残差收益、cov 1.0、MATRIX）。EUR 此前**零回测**（DB 无行；GBR 有 68 臂但多在 STATISTICAL 档，只作机制先验）。
**画像**：`tracking/EUR/reference/profiles/eur_pv_pv47_profile_20261119.md`（完整性闸 2/2 PASS）。

### 1.1 探针波（6 臂，TOP2500/SUBINDUSTRY/decay4）

| 臂 | alpha | S | F | 2Y | sub | TO% | 读法 |
|---|---|---:|---:|---:|---:|---:|---|
| P1 截面22 反转 | 0mPXv6Xq | 1.41 | 0.76 | 0.87 | 0.74 | 18.2 | 有信号 |
| P2 时序22 反转 | 78YN9MN1 | 1.67 | 0.96 | 0.83 | 0.87 | 17.8 | 时序族更强 |
| P3 截面5 反转 | A1xNKmNE | 1.91 | 0.79 | 1.12 | 1.04 | 40.3 | S 最高、TO 过高 |
| P4 方向对照（不取反） | ZYabGMA3 | **−1.41** | — | — | — | — | **对称翻转 ⇒ 真因子** |
| P5 截面66 反转 | Xgab6eJ8 | 0.68 | 0.33 | 0.96 | 0.50 | 11.1 | 长窗衰减 |
| P6 量纲对照字段 | E5QpJLRP | 1.69 | 1.00 | 0.98 | 0.89 | 18.2 | 同源一致 |

### 1.2 扩波（8 臂）与设置轴（6 臂）

| 构造 | 最优 alpha | S | F | 2Y | sub | TO% |
|---|---|---:|---:|---:|---:|---:|---:|
| ts_rank11 反转（TOP2500/SUBIND/d4） | rK7OmaOd | 1.94 | 1.00 | 1.06 | 1.22 | 25.4 |
| ts_rank11 @ TOP2500/INDUSTRY | RReb00J1 | 1.87 | 0.99 | 0.93 | 1.23 | 24.7 |
| ts_rank11 @ TOPCS1600/SUBIND | XgabqZGa | 1.60 | 0.79 | **0.47** | 0.92 | 25.6 |
| winsorize(0.3)+rank22（TOP2500/SUBIND/d8） | Wjlbmrbx | 1.76 | 0.95 | 1.02 | 1.02 | 19.1 |
| **winsorize+rank11 @ decay8** | **P052jb8J** | **1.86** | **1.01** | **1.10** | **1.34** | 20.1 |
| 同上 @ TOP2500/INDUSTRY | 6XMjggX7 | 1.61 | 0.87 | 0.84 | 0.96 | 18.5 |
| 同上 @ TOPCS1600/SUBIND | E5Qp3n71 | 1.53 | 0.82 | **0.46** | 0.91 | 19.0 |

- **TOPCS1600 是把 2Y 砍半的宇宙**（0.46–0.47）⇒ 反转信号住大盘，TOP2500 必要。
- **decay 8 是 F 的修复档**（P052jb8J F 1.01 过闸，TO 25%→20%）。
- S 1.94 臂与 2Y 1.06 臂同族，**S 越高 2Y 越弱**（与 SOP「S⊃2Y 跷跷板」一致）。

### 1.3 六维补齐（8 臂）：残差动量/波动/SNR/非线性/多轴

| 臂 | 构造 | S | F | 2Y | 判定 |
|---|---|---:|---:|---:|---|
| 残差动量正向（ts_sum252） | O0WNw60d | **−0.32** | — | — | Blitz 残差动量在 EUR pv47 **方向反了** |
| 长窗反转（252） | QP0brWPw | 0.32 | — | — | 长窗无效 |
| 波动率（ts_std_dev66） | xAv3wlOg | 0.32 | — | — | 无效 |
| ts_quantile 非线性 | ZYabwXPx | 1.78 | 1.02 | 0.98 | 过 S/F |
| signed_power 后置 | KPgNYVlk | 1.78 | 1.01 | 1.01 | 过 S/F |
| country 轴 | 0mPXkGOp | 1.67 | 0.92 | 1.07 | 轴无效 |
| market 轴 | N1PaWKxe | 1.61 | 0.92 | 1.04 | 轴无效 |
| **SNR（11日求和÷66日波动）** | **wpoZwNK2** | **1.85** | **1.06** | 1.05 | 最佳均衡 |

### 1.4 六维闭合核对（AGENTS §7.6）

| 维 | 要求 | 本轮实测 |
|---|---|---|
| D1 结构互异模板 | ≥10 | **12+**（group_rank/ts_rank/ts_zscore/ts_quantile/signed_power/winsorize×3/group_neutralize/SNR/ts_delta/长窗/波动） |
| D2 字段族自测 | 每字段 ≥1 | **2/2** |
| D3 矩全家 | 水平/一阶差/二阶波动/比值 | **4/4**（sum / ts_delta22 / ts_std_dev / SNR） |
| D4 分组轴 | ≥2 | **4**（subindustry/industry/country/market） |
| D5 非线性 | ≥1 | **2**（ts_quantile / signed_power） |
| D6 配置 | ≥2 | **4**（TOP2500×SUBIND、TOP2500×IND、TOPCS1600×SUBIND、decay4/8） |

### 1.5 逐年拆解（P052jb8J，S1.86/F1.01 那颗）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | 3.53 | 2.29 | 1.25 | 1.97 | **0.35** | 2.53 | 2.84 | 2.97 | **0.87** | 1.50 |
| 持仓 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

- 十年满仓（longCount/shortCount 全 >0、pnl 全正）✓ **满足近十年约束**。
- 2Y 短板定位到 **2018（S0.35）+ 2022（S0.87）** 两个熊市年；2023 已恢复 1.50。
- ⇒ 按 SOP #4 定律（2Y 是信号时效闸）：任何窗口/平滑/设置均救不回，已跨 6 设置档 × 12 结构验证。

### 1.6 pv47 判定

**信号层·2Y 时效死**：S/F/sub/TO 四闸可过、十年满仓，唯 2Y 结构性天花板 1.05–1.27（缺口 0.3–0.5）。
**PROVISIONAL / 族级**（不判数据集死：prod 未测、产线池与市场制度会漂移）。**不投入第三波。**

## 2. earnings_sent_matrix 验尸（换信息源的最后一搏）

### 2.1 本轮新增：两个从未作过方向信号的读数

| alpha | 表达式 | S | F | 2Y | sub | TO | RA | prod（新鲜实测） |
|---|---|---:|---:|---:|---:|---:|---|---:|
| **KPgNqaEk** | `-ts_zscore(ts_backfill(sentiment_weighting_method1,60),250)` | **1.99** | **1.42** | **1.98** | 1.52 | 9.0% | **0/0** | **0.9229** ❌ |
| **78YN09n5** | `-ts_zscore(ts_backfill(sentiment_weighting_method2,60),250)` | **1.91** | **1.36** | **1.82** | 1.43 | 9.0% | **0/0** | **0.8797** ❌ |
| pwaRoOl6 | `ts_zscore(ts_backfill(overall_sentiment_score,60),250)` | 1.69 | 1.07 | 0.72 | 1.27 | 8.9% | 1 | 未测（2Y 不过） |
| 对照组 | wpQjEAPl（prob_3 组合） | 1.93 | 1.37 | 1.70 | 1.49 | 9.0% | 0 | 0.8713 ❌ |
| 对照组 | d5Wj0Nx2（prob 比值） | 1.90 | 1.35 | 1.81 | 1.44 | 9.0% | 0 | 0.8809 ❌ |

### 2.2 归因（决定性）

- **4 颗全闸 ATOM 全部撞 prod 墙**（0.871–0.923）。method1/method2 是同一份电话会转录本的不同加权口径 ⇒ **同信息源、同墙**。
- prod 墙的数学：唯一有效杠杆（换宇宙）量级 −0.03（SOP #57 实测）；缺口 0.18–0.22 ⇒ **结构性不可达**，不再烧配额。
- 判 **信息源级 prod 墙（PROVISIONAL）**：产线拥挤是池状态，会漂移；不判数据集死。
- 该数据集 7 字段已全部实测（覆盖 7/7：prob_pos/neg/neutral、overall、method1/2、intraday_delay_indicator 元数据）。

## 3. 其余塔的既有证据（合并 03:0x 版评估，全部有读数）

| 塔 | 数据集 | ATOM 最好读数（标准档） | 卡在哪 | 结论 |
|---|---|---|---|---|
| institutions | institutions6 | **买家比例内核 GrmbwmmO S1.32/F0.67/2Y1.48/sub1.00/TO7.3%（40 臂 2026-11-19 新测；旧记 S0.16 系家数不对称变体）** | S −0.26 / F −0.33（数学约束）/ prod 0.8257 | 限投（PROVISIONAL，见 `EUR_institutions6_atom_campaign_20261119.md`） |
| institutions | fund_holdings_panel | zq378ELo S1.64/F1.05/2Y2.61/sub1.17 全闸除 prod（0.8887）；2015–2023 九年满仓（**2026-11-19 用户放宽年限 ⇒ 数据层排除撤销**） | prod（0.8887，缺口 0.19） | **prod 墙** |
| insiders | insider_agg_matrix | S 0.43/F0.14/2Y−0.21（S2.0 仅存于不可用的 SLOW_AND_FAST） | S+2Y | 死；裸净买入 prod 0.76–0.80 |
| insiders | insiders1 / insiders12 | cov 0.55 / 0.20 | cov<0.85 ⇒ sub 结构性不可达 | 覆盖排除 |
| earnings | earnings6 | S 0.91 | S | 死 |
| earnings | earnings_sent_matrix | 4 颗全闸（S1.90–1.99）| **prod 0.871–0.923** | 信息源级 prod 墙 |
| pv | pv47 | S1.99/F1.06 可过，**2Y ≤1.27** | 2Y 时效 | 时效死（PROVISIONAL） |
| pv | pv37 | S1.98/F0.63/2Y0.54/TO58% | F/sub/2Y | 死（2026-11-13 五族 25 臂已闭合） |
| pv | pv13 | rel_ret 族 6 臂 \|S\|≤0.28 | 无信号 | 探针死（其余字段为分组轴/元数据） |
| pv | pv20 | P05EONAK S1.76/F0.72/2Y0.92/TO68% | F/2Y | 死（crowding 族 3 字段同源） |
| pv | pv149/univ1/univ2/pv103/pv109/pv173/pv87/chart_return_model | 元数据（状态码/宇宙定义）或 cov<0.5 或 EUR 未注册或平台空集 | 非信号集/覆盖 | 结构性排除 |
| socialmedia | socialmedia12 | S 0.46 | S | 死 |
| socialmedia | socialmedia15 | cov 0.34 | 覆盖 | 排除 |
| macro | macro10 | 单标量（无横截面） | 结构性 | 排除（非抽样：字段数=1 全表） |
| macro | macro27 | cov 0.33 | 覆盖 | 排除 |

## 4. ATOM 穷尽判定（对照 §7.7）

1. **EUR 未点亮塔 ATOM 今日不可交付 = 0 颗**。六个未点亮塔、合计 30+ 数据集逐一有读数，最近的三条死路分别是：
   - sent_matrix 4 颗全闸但 prod 信息源级墙（0.87–0.92，缺口 0.18+，形状杠杆量级 0.015–0.03 不可达）；
   - pv47 六维闭合、四闸可过但 2Y 时效天花板 1.05–1.27（2018/2022 衰减）；
   - fund_holdings_panel 除 prod 全闸，但 prod 0.8887（缺口 0.19）；**2014 零持仓（九年数据）已按用户 2026-11-19 放宽口径接受，数据层不再是排除理由**。
2. **ATOM 穷尽举证成立** ⇒ 按用户 2026-11-17 裁定与 AGENTS §7.7，允许 regular fallback（跨集），且只许 gating/grouping/residual/ratio 四形态。
3. **regular fallback 交付 = 前一轮 10 颗**（`EUR_regular_alpha_delivery_20261118.md`）：全部本会话新鲜 prod<0.7 / self<0.7、10/10 平台打通、逐年满仓实读核验。ATOM 穷尽举证（本档案）补上其合规前提。
4. **新增记录**：pv47 = 信号层 2Y 时效死（PROVISIONAL）；pv13 = rel_ret 族探针死（PROVISIONAL）；sent_matrix = 信息源级 prod 墙（PROVISIONAL）；fund_holdings = prod 墙（数据层排除已按 2026-11-19 放宽口径撤销）。均**不判数据集级死**（prod 会漂移、产线池会变）。

## 5. 本轮臂数与配额记录

- pv47：6 探针 + 8 扩波 + 2 TOP2500/IND + 2 TOPCS1600 + 5 decay8 细网格 + 8 六维补齐 = **31 臂**（全 COMPLETE）
- sent_matrix：6 臂（3 字段 × 双方向；全 COMPLETE）
- pv13：6 臂（全 COMPLETE）
- **合计 43 臂，零失败，全走 `create_multi_simulation`（n_slots=2 并发上限）**
- prod 实测：KPgNqaEk 0.9229、78YN09n5 0.8797（本会话新鲜）
- 未提交任何 alpha。
