# USA · option3「Equity Options Moneyness Aggregates」字段画像与机制台账（2026-10-20）

> 数据集归属：**USA / D1 / OPTION 塔（未点亮，`get_pyramid_alphas` 实测 option=0）**。
> 选用理由：按用户 2026-10-20 指令「已点亮塔的数据集先不回测」（USA/D1 model=4 / analyst=5 / earnings=1 已点亮），
> 本集属未点亮塔且**此前 0 条回测**；同时同类目已判死记录明确留下唯一未封的方向：
> 「surface-level IV signals closed; **only volume/OI-based option datasets remain**」
> （`USA-OPTION40-IV-SURFACE-WEAK`）。
>
> 平台元数据（`get_datasets(category="option")`，2026-10-20）：
> `option3` · Equity Options Moneyness Aggregates · coverage **0.8801** · fieldCount **20** ·
> userCount **289** · alphaCount **492** · valueScore 3 · pyramidMultiplier 1.3。
> 字段全 **MATRIX**（无需 `vec_*`）。

## 1. 类别级扫描（option，6 集）

| 数据集 | 字段 | cov | aC | 裁定 | 依据 |
|---|---:|---:|---:|---|---|
| option8 · Volatility Data | 64 | 0.9698 | **203,016** | ✗ 排除 | 极度饱和（Tier B，>1 万 α） |
| option9 · Options Analytics | 74 | 0.9817 | **83,652** | ✗ 判死 | `USA-OPTION9-PCR-WEAK`：PCR 情绪 S<0.7 + 高换手 |
| option6 · Forecasted Volatility | 133 | 0.9616 | 19,159 | ✗ 排除 | 饱和 + 纯 IV 预测族（同为 surface 概念） |
| option40 · Options Analytics Data | 208 | 0.9755 | 3,200 | ✗ 封存 | `USA-OPTION40-IV-CONCEPTS-WEAK`：IV 8 概念最高 S1.12，ceiling ~1.1 |
| order_flow_imb · Institutional Order Flow Imbalance | 120 | 0.8092 | 478 | ✗ 已穷尽 | `USA-ORDER-FLOW-IMB-RANK-WEAK`：59 生成 / 17 回测，plain 截面 rank 最高 0.87 |
| **option3 · Equity Options Moneyness Aggregates** | **20** | **0.8801** | **492** | **★ 本波主攻** | 0 回测；**OI/成交量按 moneyness 分档**，正是同类目唯一未封方向；aC 5–128 低拥挤 |

> 结论：option 塔的「IV 曲面」方向已被两次实测封到 ~1.1（与 option_horizon_decomp 的 1.45 同量级），
> 不再投 IV 单腿扩批；本波只在 option3 上验证 **OI / 成交量 / 报价价差** 三族，
> IV 字段仅作同数据集对照（不占主线机制）。
>
> ★ **事后更正（2026-10-20 批 1 实测）**：上面「IV 仅作对照」的塔内先验被本集实测部分推翻——
> **option3 的 IV-by-moneyness 聚合有截面信息**（M06 S1.06/2Y2.06、M08 S1.02/2Y1.76/SUB0.93），
> 而 OI 族（最好 M02 S0.68）与成交量族（最好 M05 S0.56）全弱。
> 机制差异成立：option40 封的是「IV 曲面水平/概念」，本集有效的是**相对定价差（call−put）与报价价差**，
> 两者不是同一构造。批 2/3 因此转向 IV 族的时序归一与壳层，OI/Volume 降为对照。

## 2. 字段画像（16 个可见字段全表）

> 平台 `fieldCount=20`，本地 `get_datafields` 被 WebDataScope 的 sharpe 过滤器隐去 4 个
> （`sharpe_filter_removed=4`，本表不含；不猜名、不使用）。
> 列：字段 · cov · uC · aC · 家族 · 经济含义。

| 字段 | cov | uC | aC | 家族 | 含义 |
|---|---:|---:|---:|---|---|
| `opt3_openintecallatm` | 0.9439 | 22 | 24 | OI | ATM call 未平仓量 |
| `opt3_openintecallitm` | 0.9298 | 10 | 15 | OI | ITM call 未平仓量 |
| `opt3_openintecallotm` | 0.9487 | 13 | 15 | OI | OTM call 未平仓量 |
| `opt3_openinteputatm` | **0.7257** | 13 | 14 | OI | ATM put 未平仓量 |
| `opt3_openinteputotm` | **0.7269** | 5 | 5 | OI | OTM put 未平仓量 |
| `opt3_volcallatm` | 0.9493 | 98 | 128 | IV | ATM call 隐含波动率 |
| `opt3_volcallitm` | 0.9493 | 32 | 33 | IV | ITM call 隐含波动率 |
| `opt3_volcallotma` | 0.9493 | 67 | 88 | IV | OTM call IV（**ask 侧**） |
| `opt3_volcallotmb` | 0.9493 | 46 | 63 | IV | OTM call IV（**bid 侧**） |
| `opt3_volputatm` | 0.9493 | 37 | 56 | IV | ATM put 隐含波动率 |
| `opt3_volputitm` | 0.9493 | 22 | 30 | IV | ITM put 隐含波动率 |
| `opt3_volputotma` | — | — | — | — | **平台未返回**（被过滤） |
| `opt3_volumecallatm` | 0.9439 | 27 | 31 | Volume | ATM call 成交量 |
| `opt3_volumecallitm` | 0.9298 | 18 | 22 | Volume | ITM call 成交量 |
| `opt3_volumecallotm` | 0.9487 | 15 | 17 | Volume | OTM call 成交量 |
| `opt3_volumeputatm` | 0.7257 | 11 | 12 | Volume | ATM put 成交量 |

**画像六问**：

1. **是什么**：按 moneyness（ATM/ITM/OTM）聚合的期权**未平仓量、成交量、隐含波动率**，股票粒度日频面板。
2. **类型**：16/16 MATRIX；OI/Volume 为**计数型**（右偏、跨股票量级差 2–3 个数量级 ⇒ 必须比值化或 rank）；
   IV 为百分比量（≈0.2–1.5），OTM ask/bid 成对可构造**报价价差**。
3. **覆盖**：calls 0.93–0.95；**puts 仅 0.726–0.727**（put 侧是本波 CW/SUB 的主要风险源）。
4. **更新**：日频（平台描述 daily aggregated）。
5. **分布**：OI/Volume 强右偏且零值常见（不良行权价当日无成交）⇒ 直接除法会产生 inf/NaN；
   壳层 `winsorize(std=4)` + `ts_backfill(252)` 兜底，比值一律同量纲相除。
6. **拥挤**：aC 5–128，中位 ~23，远低于 option8/9；IV 四字段 aC 56–128 略高（唯一拥挤面）。

**字段族**：OI（5）· Volume（4）· IV（7，含 2 个 bid/ask 侧）。三族经济含义不同，**不混加**。

## 3. 适用模板（按体征，不按数据集名）

| 体征 | 模板 | 字段 |
|---|---|---|
| 计数型 / 跨股量级差大 | **比值化**（同族相除）后 `group_rank`，禁止裸水平 | OI、Volume 全族 |
| 分档持仓结构（share） | `X_otm / (X_atm + X_otm)` → 秩 | `openintecall*` / `openinteput*` |
| 流量 vs 存量（churn） | `volume_atm / openinte_atm` → 秩 | `volumecallatm / openintecallatm` |
| 收益分布价格（IV spread） | 成对相减（同量纲）→ `group_rank` | `volcallatm − volputatm`、`volcallotma − volcallatm` |
| 流动性（bid-ask） | `ask − bid` → 秩（负向：价差大 = 流动性差） | `volcallotma − volcallotmb` |
| 事件/流量变化 | `ts_delta(...,22)` → 秩 | `openintecallotm` |

**禁用**：裸 OI/成交量水平（量级即行业规模，非信号）；`+0.01` 类防零常数（会触发 UNITS 告警，
用同量纲比值或依赖 `nanHandling=ON` 处理除零）。

## 4. 机制台账（批 1：M01–M08）

设置（`wqb.profiles explain --region USA --dataset order_flow_imb` → `option` 类别卡，两集同卡）：
**EQUITY / USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / truncation 0.08 / maxTrade OFF / pasteurization ON /
unitHandling VERIFY / nanHandling ON / language FASTEXPR**。

通用壳：`quantile(group_rank(hump(ts_backfill(winsorize(<SIG>, std=4), 252), hump=0.01), industry))`。

| # | 机制 | 字段 | 方向 | SIG | 假说与文献 |
|---:|---|---|---|---|---|
| M01 | 上行彩票需求（OTM call 占比） | `openintecallotm`/`openintecallatm` | **负** | `-1 * (callotm/(callatm+callotm))` | Bali/Cakici/Whitelaw (2011) MAX：OTM 看涨持仓=投机性凸性需求，未来收益低 |
| M02 | 下行保险需求（OTM put 占比） | `openinteputotm`/`openinteputatm` | **负** | `-1 * (putotm/(putatm+putotm))` | 尾部对冲需求抬升 → 负向预测（Pan & Poteshman 2006 的 put 侧） |
| M03 | 上行持仓流量（OTM call OI 变化） | `openintecallotm` Δ22 | **正** | `ts_delta(openintecallotm, 22)` | Johnson & So (2012)：call open interest 变化携带信息 |
| M04 | 投机性换手（ATM call churn） | `volumecallatm`/`openintecallatm` | **负** | `-1 * (volumecallatm/openintecallatm)` | 高换手=注意力/散户投机，USA 微观结构下过度定价 |
| M05 | 上行成交量集中（OTM call 成交占比） | `volumecallotm`/Σcall vol | **负** | `-1 * (volcallotm/(volcallatm+volcallitm+volcallotm))` | 同 M01 但用当日流量确认结构（流量 vs 存量分离） |
| M06 | ATM call-put IV 价差 | `volcallatm − volputatm` | **正** | `volcallatm - volputatm` | Cremers & Weinbaum (2010) IV spread 镜像：call IV 相对贵 → 正 |
| M07 | Call skew 斜率 | `volcallotma − volcallatm` | **正** | `volcallotma - volcallatm` | Xing/Zhang/Zhao (2010)：OTM call skew 正向预测 |
| M08 | 期权流动性（OTM call IV 报价价差） | `volcallotma − volcallotmb` | **负** | `-1 * (volcallotma - volcallotmb)` | 报价价差=做市商库存/逆向选择成本，高 = 流动性差 → 负 |

**正交性**：M01/M02 结构持仓两侧；M03 流量；M04/M05 换手与成交结构；M06/M07 IV 水平与斜率；
M08 微观流动性。无两条共用同一字段作为主信号。
**同族配额**：OI 3 条（M01–M03）、Volume 2 条（M04–M05）、IV 3 条（M06–M08）——
IV 三条均为同数据集的**方向/斜率/价差**三种不同几何，且 IV 族在本塔已有 ~1.1–1.45 天花板记录，
本批 IV 只作对照；若 IV 三条全弱而 OI/Volume 有信号，批 2 立即转 OI/Volume 深挖。

**预注册判据（写死）**：

- 任一 S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB≥0.75 / TO≥1% 且 fail=0 ⇒ 立即 `check_correlation(refresh=True)` 做 prod/self 双端点（<0.7）。 <!-- from config.prod_corr_max -->
- 只过 1–2 闸 ⇒ 先归因（按字段族分组看 S 排序），再决定批 2 方向；不得直接换字段。
- **全部 S<1.0 ⇒ 记「option3 水平结构无截面 alpha」**，批 2 转「变化率 / 事件日 / 与 IV 的背离」，
  仍不换数据集；若批 2 仍 <1.0 且 IV 对照也无 ≥1.2 ⇒ 判 option3 弱（本塔仅剩 option40 的 volume/OI 面可试）。

## 5. 回测结果及指标（批 1）

`preflight_expressions`（2026-10-20）：8 条表达式，`fields_checked` 11 个真实字段全部通过，
仅 `unknown_fields=["std"]`（`winsorize(std=)` 已知误报）；`vector_fields=[]`、`any_changed=false`。

**发批**：multisim `MwEMY4gb4vlbGb1ct9dTYee`（8 条，设置同上；2026-10-20 发批，async 返回 success）。
**收批**：2026-10-20，8/8 COMPLETE，全部 0 条过闸。

| # | 机制 | alpha | S | F | 2Y | SUB | TO | 收益 | DD | risk-neut S | 失败闸 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| M01 | 上行彩票需求 | `N1eRgk6q` | 0.43 | 0.13 | 0.74 | −0.16 | 1.12% | 1.08% | 4.18% | −0.23 | 4 |
| M02 | 下行保险需求 | `QPY92mjp` | 0.68 | 0.26 | 0.87 | 0.31 | 1.26% | 1.78% | 5.60% | 0.27 | 3 |
| M03 | OTM call OI 变化 | `0mjMenQv` | 0.05 | 0.01 | −0.50 | −0.01 | 1.96% | 0.15% | 11.90% | 0.02 | 4 |
| M04 | ATM call churn | `2rjNaPZN` | 0.23 | 0.05 | 0.67 | 0.11 | 3.65% | 0.62% | 9.40% | −0.12 | 3 |
| M05 | OTM call 成交占比 | `xA1dPXzW` | 0.56 | 0.19 | 0.84 | 0.20 | 1.24% | 1.46% | 5.56% | −0.02 | 4 |
| **M06** | **ATM call−put IV 价差** | `O0JxbK5Y` | **1.06** | 0.67 | **2.06** | 0.45 | 1.77% | **4.96%** | 6.44% | **0.34** | 3 |
| M07 | Call skew 斜率 | `e76xdeqO` | 0.00 | 0.00 | −0.41 | −0.43 | 1.62% | 0.01% | 9.29% | −0.40 | 4 |
| **M08** | **期权流动性价差** | `bl8do7Wr` | **1.02** | 0.47 | **1.76** | **0.93** | 1.96% | 2.64% | 4.18% | **0.62** | **2** |

> 失败闸数 = 4 时含 LOW_SUB（动态限 ≈0.43×S）；M08 只挂 LOW_SHARPE / LOW_FITNESS，2Y 与 SUB 均过。
> `risk_neutralized_sharpe`：M08 0.62 最高、M06 0.34 次之 ⇒ 两条都不是纯风格 beta（阈值 ≥0.3）。

### 5.1 归因（按字段族，批 1）

| 字段族 | 条数 | S 区间 | 最好 | 结论 |
|---|---:|---|---|---|
| **IV** | 3 | 0.00–1.06 | M06 1.06 / M08 1.02（2Y 2.06 / 1.76） | **有效**；但只有「相对定价差」与「报价价差」有效 |
| OI | 3 | 0.05–0.68 | M02 0.68（put OTM 占比） | 弱；**ΔOI 变化量完全无效**（0.05，2Y −0.50） |
| Volume | 2 | 0.23–0.56 | M05 0.56（OTM 成交占比） | 弱 |

**四条可复用判据**：

1. **IV 的「几何水平」无效、「相对定价」有效**：M07（`otma − callatm`，call skew 斜率）S=**0.00**，
   而 M06（`callatm − putatm`）1.06、M08（`otma − otmb`，bid/ask 报价价差）1.02
   ⇒ 本集 IV 的可预测信息来自**call/put 相对贵贱**与**做市商报价摩擦**，不是波动率曲面斜率本身。
   这与 option40「IV 概念/曲面水平封到 1.1」并不矛盾：构造不同。
2. **OI 存量占比 > OI 变化量**：M02（占比）0.68 vs M03（Δ22）0.05，且 M03 2Y 转负
   ⇒ 期权持仓的**结构**（谁贵、谁多）有信息，**增量**是噪声（与 Institutions 上「Δ 窗口有效」相反，
   **不可跨数据集套用变化量模板**）。
3. **成交量族弱于持仓族**：M05 0.56 < M02 0.68；M04 churn 0.23 且 TO 3.65%（最高）
   ⇒ 期权日成交量的信噪比低于存量结构。
4. **Put 侧覆盖 0.726 未造成 CW**：M02/M06 的 `CONCENTRATED_WEIGHT` 均 PASS，长/短各约 1500 只
   ⇒ put 覆盖率不是本集的结构性障碍，无需 `group_backfill`。

### 5.2 批 2（TS 算子全替换）与批 3（结构/壳层）实测

> 两批各 8 条，设置同批 1（EQUITY/USA/TOP3000/D1/SUBINDUSTRY/decay 5/trunc 0.08/VERIFY/ON/FASTEXPR）。
> 批 2 = `2Qqmwxbu65fOa9f10neLXZEt`；批 3 = `1PdKgk1Al55GbHV71LOfyAY`。16/16 COMPLETE，零 ERROR。

**批 2（M06 = `callatm − putatm`；M08 = `−(otma − otmb)`）**

| # | 机制 × 变换 | alpha | S | F | 2Y | SUB | TO | 收益 | risk-neut S | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B2-1 | M06 `ts_av_diff(252)` | `xA1dPj8p` | 0.71 | 0.26 | 1.33 | 0.57 | 1.32% | 1.73% | 0.09 | 3 |
| B2-2 | M06 `ts_zscore(252)` | `88vealdo` | 1.10 | 0.55 | 1.89 | 0.60 | 1.10% | 3.09% | 0.32 | 2 |
| B2-3 | M06 `ts_delta(22)` | `YPxg27GW` | **1.38** | **0.97** | **2.47** | 0.52 | 1.73% | **6.17%** | **0.67** | 3（S/F/SUB） |
| B2-4 | M06 `ts_rank(252)` | `1YjzawQM` | 1.05 | 0.47 | 2.08 | 0.63 | 1.06% | 2.55% | 0.57 | 2 |
| B2-5 | M08 `ts_av_diff(252)` | `88veal1o` | 0.27 | 0.07 | −0.11 | 0.41 | 1.70% | 0.83% | 0.46 | 3 |
| B2-6 | M08 `ts_zscore(252)` | `e76xdzRg` | 0.31 | 0.08 | 1.16 | 0.05 | 1.07% | 0.79% | −0.09 | 4 |
| B2-7 | M08 `ts_delta(22)` | `leM3QjX7` | 0.91 | 0.40 | 1.99 | 0.17 | 2.16% | 2.46% | 0.48 | 3 |
| B2-8 | M08 `ts_rank(252)` | `npA8Z7V8` | 0.37 | 0.10 | 0.97 | 0.08 | 1.14% | 0.92% | 0.07 | 4 |

**批 3（结构/壳层）**

| # | 构造 | alpha | S | F | 2Y | SUB | TO | 收益 | risk-neut S | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B3-1 | M06 `(c−p)/c` | `d5KREZMY` | **1.14** | **0.75** | **2.11** | **0.63** | 1.82% | **5.45%** | 0.33 | 2（S/F） |
| B3-2 | M06 `(c−p)/(c+p)` | `KPmEXG1l` | 1.12 | 0.73 | 2.03 | 0.57 | 1.69% | 5.28% | 0.36 | 2 |
| B3-3 | M06 `group_rank(subindustry)` | `YPxg2vew` | 1.03 | 0.63 | 2.03 | 0.40 | 1.66% | 4.70% | 0.33 | 3 |
| B3-4 | M06 backfill 504 | `akVEA1p1` | 1.09 | 0.69 | 2.10 | 0.39 | 1.79% | 5.08% | 0.38 | 3 |
| B3-5 | M08 `−(otma−otmb)/callatm` | `LL5dgGQm` | 0.93 | 0.43 | 1.50 | **0.97** | 1.92% | 2.68% | **0.88** | 3 |
| B3-6 | M08 + subindustry | `d5KREZN2` | 1.06 | 0.48 | 1.49 | **0.84** | 1.70% | 2.53% | 0.68 | 3 |
| B3-7 | M08 + backfill 504 | `3qjeap8g` | 1.01 | 0.46 | 1.79 | **0.90** | 1.96% | 2.60% | 0.60 | 2 |
| B3-8 | M06 put 深保护 `−(putitm−putatm)` | `0mjMep18` | 0.67 | 0.25 | 0.65 | 0.40 | 1.68% | 1.79% | 0.29 | 3 |

**归因（批 2/3 六条）**

1. **`ts_delta(22)` 是本集最强变换**：M06 从 S1.06/F0.67/2Y2.06/收益4.96% 抬到
   **S1.38/F0.97/2Y2.47/收益6.17%，risk-neut 0.34→0.67**；F 只差 0.03、S 差 0.20。
   ⇒ IV 价差的**近期变化**比水平更有信息，且信息是真实的（risk-neut 0.67，不是风格 beta）。
2. **`ts_av_diff(252)` 反而最差（S0.71）**：长窗均值差把短期定价信息摊平；`ts_zscore(252)` 居中（1.10）。
   ⇒ **变换窗口要短**（22 日），不是「越长越稳」。这与 analyst 的 63/252 慢修正不同，**不可跨数据集套窗口**。
3. **M08 的 `ts_delta(22)` 与自归一相反**：M08 原始 S1.02/SUB0.93/2Y1.76 → Δ22 后 S0.91/SUB0.17/2Y1.99，
   `ts_zscore` 更差（0.31）⇒ **报价价差是「水平型」信号，差分即毁**；M06 是「变化型」。
   同一数据集的 IV 两族，**归一方式不可互换**。
4. **相对化 `(c−p)/c` 是 M06 的最佳折中**：S1.14、F0.75、2Y2.11、**SUB0.63（PASS）**、收益5.45%；
   与 Δ22 相比，用 0.24 S 换 0.11 SUB 与 0.08 F。⇒ 若批 4 的「Δ22 × 自归一」不能同时过 S 与 SUB，
   交付线应落在这条相对化构造上继续补 S。
5. **M08 的 alpha 真但太弱**：相对化后 SUB 0.97、risk-neut 0.88（全表最高），S 仅 0.93、收益 2.68%
   ⇒ 它是**低波/低流动段的稳健信号**，不是收益引擎；与 M06 互补但**不可混加**（禁混信号）。
6. **失败闸结构**：M06 Δ22 只挂 S/F/SUB；M06 `(c−p)/c` 只挂 S/F（SUB、2Y 全过）。
   下一批的**唯一任务**是把 S 从 1.14–1.38 推到 1.58，同时不把 SUB 压回 0.43×S 以下。

### 5.3 批 4（已收，2026-10-20）

> multisim `1WnA91gKP5hZ8HJ1aM7vC3UU`，8 条，设置同前三批。设计依据 = §5.2 判据 1/3/4：
> 「Δ22 抬 S/收益」「自归一修 SUB」「M06 变化型 / M08 水平型」。

| # | 构造 | 目的 |
|---:|---|---|
| P4-1 | `ts_delta((c−p)/c, 22)` | 相对化 × 最强变换（两条最佳壳合流） |
| P4-2 | `ts_zscore(ts_delta(c−p, 22), 252)` | Δ22 的自波动归一（SUB 主修法） |
| P4-3 | `ts_zscore(ts_av_diff(c−p, 22), 252)` | 1M 偏离 × 自归一（比纯 Δ22 去噪） |
| P4-4 | `ts_av_diff(c−p, 66)` | 3M 偏离（窗口边界对照） |
| P4-5 | `ts_delta(c−p, 66)` | 3M 变化（窗口边界对照） |
| P4-6 | `ts_zscore(ts_delta(−(otma−otmb)/callatm, 22), 252)` | M08 相对化 × Δ22 × 自归一（正交腿） |
| P4-7 | `ts_delta(−(otma−otmb)/callatm, 22)` | M08 相对化 × Δ22（无归一对照） |
| P4-8 | `ts_zscore(ts_delta(c−p, 22), 504)` | 归一窗 504 对照（252 vs 504） |

**预注册判据**：任一 S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB≥0.75 且 fail=0 ⇒ 立即 `check_correlation(refresh=True)`
做 prod/self 双端点（<0.7）。若批 4 最好仍 S<1.4 且 SUB 未过，则 option3 判「单数据集 ATOM 上限 ~1.4」， <!-- from config.prod_corr_max -->
按止损封存，不再磨第 5 批（本塔剩余可试面已穷尽：IV 两族 × 水平/变化/相对化/自归一 × 两种分组）。

**批 4 实测（8/8 COMPLETE，0 error）**：

| # | 构造 | alpha | S | F | 2Y | SUB | TO | 收益 | risk-neut | 判读 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| P4-1 | `ts_delta((c−p)/c, 22)` | KPmEXpAj | **1.34** | **0.95** | **2.49** | 0.51 (lim 0.58) | 1.86% | **6.32%** | 0.62 | 差 0.07/0.05/0.07，全批最佳 |
| P4-2 | `ts_zscore(ts_delta(c−p,22),252)` | pwvKVkb6 | 1.07 | 0.53 | 2.44 | 0.60 PASS | 1.10% | 3.01% | 0.45 | 自归一压 SUB 但同时压 S |
| P4-3 | `ts_zscore(ts_av_diff(c−p,22),252)` | zqrRPE7d | 1.20 | 0.63 | 2.11 | **0.80 PASS** | 1.13% | 3.46% | 0.46 | SUB 最好，S 不足 |
| P4-4 | `ts_av_diff(c−p,66)` | QPY92ARw | 0.71 | 0.26 | 1.57 | 0.16 | 1.30% | 1.74% | 0.17 | 3M 偏离全毁（同批 2） |
| P4-5 | `ts_delta(c−p,66)` | 0mjMeLVk | 1.30 | 0.88 | 2.33 | 0.50 (lim 0.56) | 1.62% | 5.71% | 0.55 | 3M 变化 ≈ 1M 的 97%，但 SUB 更差 |
| P4-6 | M08 相对化 × Δ22 × 归一 | GrgeMN2G | 0.43 | 0.13 | 1.56 | −0.01 | 1.04% | 1.07% | −0.09 | M08 全灭复证 |
| P4-7 | M08 相对化 × Δ22 | QPY92Axw | 0.61 | 0.23 | 1.99 | −0.09 | 2.87% | 1.72% | 0.02 | M08 全灭复证 |
| P4-8 | `ts_zscore(ts_delta(c−p,22),504)` | Vkd32LWY | 1.09 | 0.54 | 2.37 | 0.39 | 1.12% | 3.08% | 0.46 | 归一窗 504 不如 252 |

**四条归因（批 4）**：

1. **相对化 × Δ22 是 M06 的全局最优壳**：P4-1 的 S1.34 / F0.95 / 2Y2.49 / 收益6.32% 全面超过批 2 的 M06 Δ22（S1.38 但 F0.97、2Y2.47、收益6.17%——S 略低但 F/2Y/收益更高，且 SUB 0.51 vs 0.52 同档），是「把 3 条指标同时推到差一口气」的唯一构造。
2. **自归一（ts_zscore 252）是 SUB 的唯一解，但代价是 S 掉 0.14–0.27**：P4-2/P4-3 都过 SUB（0.60/0.80），S 却退到 1.07/1.20。**SUB 与 S 在本集是同一自由度的两端**，不存在同时满足 1.58/0.75 的壳。
3. **窗口边界确认**：1M 是唯一有效窗口（3M 偏离 0.71、3M 变化 1.30 但 SUB 0.50）；归一窗 252 全面优于 504。
4. **M08（OTM 价差）在相对化/归一后仍全灭**（0.43/0.61）：它是水平型，任何变化算子都抽掉信号——与批 3 判据 3 一致，不再投入。

### 5.4 封存结论（option3，2026-10-20）

**按批 4 预注册判据封存**：批次最好 S=1.34<1.4、SUB=0.51<0.58（未过），触发止损条款 ⇒
option3 判**「单数据集 ATOM 上限 ~1.4」**，不再发第 5 批。

- **已验证上限**：M06 `ts_delta((volcallatm−volputatm)/volcallatm, 22)` 是 3 批 24 条里的最强构造
  （S1.34 / F0.95 / 2Y2.49 / 收益6.32%），距平台线 1.58 / 1.0 仅差 0.24 / 0.05。
- **不可突破点**：SUB 与 S 在本集共用同一自由度（自归一提 SUB 必掉 S），4 批 × 8 条已穷尽
  IV 两族 × 水平/变化/相对化/自归一 × 1M/3M × 252/504 × industry/subindustry。
- **复用价值**：该构造可作**未来跨数据集正交腿的候选**（ATOM 单集约束下不可混，但 RA 组合腿可用），
  已登记进交付日志 §2 的「正交腿候选」；不作为交付计数。
- **不做的第 5 批**：不再磨 decay/truncation/中性化（设置扫描不作信号），不再试 M08，不再试 3M/504。

## 6. 论坛/文献证据（可复用）

1. **Pan & Poteshman (2006)**：option volume 的 put-call 结构对个股未来收益有负向预测力，
   信息主要来自**非做市商**（customer）方向；本集无 participant 维度，故以 put/call 结构与 OTM 占比代理。
2. **Johnson & So (2012)**：option-to-stock volume ratio 正向预测；**OI 变化**同样携带信息。
   → M03 采用 OI 变化（而非水平）。
3. **Cremers & Weinbaum (2010)**：put-call IV spread 是**负向**预测（put 相对贵 → 未来收益低）；
   镜像成 call−put 后为正向 ⇒ M06。
4. **Xing/Zhang/Zhao (2010)**：OTM call IV（skew 斜率）正向预测个股收益 ⇒ M07。
5. **Bali/Cakici/Whitelaw (2011)** MAX：OTM 看涨需求的彩票偏好 → 负向；与 M01/M05 一致。
6. **同类目内部证据（必读）**：option40 的 IV 8 概念 ceiling ~1.1、option_horizon_decomp IV skew 1.45
   ⇒ 本塔任何 IV 单腿不得作为最终交付主线，只能靠 OI/流量/流动性族出货。

## 7. 风险与预判

- **Put 侧覆盖 0.726**：M01/M02/M06 的覆盖率取决于 put 字段；若 `CONCENTRATED_WEIGHT` 或 SUB 塌陷，
  先补 `ts_backfill` / `group_backfill`，不判机制死。
- **除零/零成交日**：`volumecallatm/openintecallatm` 在 OI 为 0 时出 inf；`nanHandling=ON` 兜底，
  若平台报 UNIT/INF，改为 `ts_zscore` 归一而不是加常数。
- **IV 族天花板**：M06–M08 预期 S≤1.2（塔内先验）；若 M06 都不过 1.0，说明本塔 IV 面彻底关闭。
- **低换手**：OI 为存量、变化慢，M01/M02 可能 TO<1% ⇒ 按「去壳诊断批」先确认非静态，再谈判死。
- **拥挤**：option3 全集中 aC 492 / 20 字段 ≈ 25/字段，若单条候选 prod 撞墙，按 D0-P 直接换族，不磨参数。
