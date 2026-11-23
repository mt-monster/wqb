# fundamental23 字段画像与梯度（ASI / MINVOL1M / D1）

> 战役：ASI/D1 Power Pool Dec'26 theme。换集理由：price_signal_dl volume-shock 机制 JPN 60+ 臂钉死（见 price_signal_dl.md §8）。
> fundamental23 = 论坛帖 45201936320919 推荐三向通用集，JPN 覆盖 0.95–1.00（实测 cov=1.0 字段众多）。
> 拉取：get_datafields(dataset_id=fundamental23, ASI, MINVOL1M, D1, filter_sharpe=false, sort_by=coverage)。

## 数据集级
- 类别 fundamental（pyramid 1.1）× coverage 0.7543 × alphaCount 56524 × valueScore 1.0
- 经典三向通用财务字段：sales/assets/ebit/return_equity/operating_income/cashflow_op 等 cov=1.0
- 类卡禁令：禁裸 rank(fundamental_score)；禁加权混合；慢变经典单因子(value/quality/book 线性变体)跨区判死或 prod 饱和 ⇒ 必须做残差/比率/趋势形态

## 生效模板（论坛帖①模板1：同币种盈利效率 + 1 年趋势 + country 分组）
```
group_rank(ts_delta(ts_zscore(divide(<ebit>, <assets>), 252), 252), country)
```
机理：同币种相除规避多币种扭曲；252 日契合亚洲年报周期；外层 country 分组避免日本股票在泛亚全局排名中系统性偏低（直接抬 Japan Robustness）。
设置：SLOW 中性化 + decay4 + trunc0.08 + maxTrade ON（覆盖区域缺省 SUBINDUSTRY/decay6）。

## 梯度读数表

| alpha | 表达式骨架 | 设置 | S | F | 2Y | sub | JPN | Robust | failed_ra |
|---|---|---|---|---|---|---|---|---|---|
| **zqdLZQaG** | g_rank(Δ(zscore(ebit/assets,252),252), **country**) | SLOW | **2.36** | 1.35 | **1.82** | 1.07 | **0.94** | 2.11/2.12 | 2 |
| P05AWAnp | 同上但 industry 轴 | SLOW | 2.29 | 1.28 | 1.67 | 1.02 | 0.78 | ✓ | 1 |
| 2r5202vx | return_equity 分母 country | SLOW | 2.64 | 1.58 | 1.89 | 1.42 | 0.88 | 2.31/2.38 | 2 |
| KPg23qxx | 裸 ebit/assets country | SLOW | 0.88 | 0.34 | 0.18 | 0.47 | — | — | 6 |
| j2aMmXre | 双尺度快腿 add | SLOW | 2.08 | 1.16 | 1.35 | 0.89 | — | — | 2 |
| 1YW2ELpk | 双层 country z | SLOW | 1.78 | 0.87 | 1.15 | 1.29 | — | — | 3 |
| O0W2v72b | market 轴 | COUNTRY | 2.23 | 1.50 | 1.75 | 1.16 | 0.60 | 1.95/2.01 | 2 |
| P05AE7AM | country 轴 | COUNTRY | 2.18 | 1.45 | 1.67 | 1.14 | — | — | 2 |

**归因**：
1. **趋势差分是关键**：裸 ebit/assets S0.88 → 加 252 zscore + 252 delta 后 S2.36（Δ+1.48）
2. **country 轴 > industry 轴 对 JPN**（0.94 vs 0.78），印证论坛帖①"内层 country 对齐区域 Checks 口径"
3. **SLOW 中性化 > COUNTRY 中性化 对 JPN**（0.94 vs 0.60-0.88）
4. **S 越高 Robust limit 越高**（limit=0.9×主S）：return_equity S2.64 → Robust 2.31/2.38 反而更难，印证论坛帖③"主 S 别刷过 2.5"
5. 双尺度快腿/双层 z 在此集反而降 S/2Y（与 EMEA 场景不同——本集 JPN 有信号，只是边缘）

**当前最优 = zqdLZQaG**：只差 JPN 0.94→1.0（差 0.06）+ Robust 2.11→2.12（差 0.01）。全闸临门一脚。

## 待突破方向
- winsorize 外层压极端（论坛帖①Robust 修法）
- 换分子 operating_income / cashflow_op（日本覆盖/语义差异）
- decay 微调（论坛帖③）
- 内层 group_zscore(country) 单次（批 B 的双层 z 让 S 掉，需单独试内层）

## 9. prod/self 闸实测（2026-11-22，全走 MCP check_correlation）

| alpha | 骨架 | JPN | prod | 判定 |
|---|---|---|---|---|
| zqdLZQaG | ebit/assets country（无内层z） | 0.94 | **0.8336 FAIL** | 钉子型（[0.8,0.9) 1 条），主体健康 |
| 9ql261Px | +内层 group_zscore(·,exchange) | **0.98** | **0.6447 ✓** | 全池健康；但 S1.58/F0.74/2Y0.9 |

**关键机理**：内层 `group_zscore(divide(ebit,assets), exchange)` 是"一击两得"变换——既把 JPN 从 0.94 推到 0.98（论坛帖①"内层 exchange 去均值 +0.58"复现），又把 prod 从 0.8336 压到 0.6447（换信号横截面分布形态逃逸近重复件）。代价：S 2.36→1.58、2Y 1.82→0.9。

**核心矛盾**：无内层 z = 高 S/2Y 但撞 JPN+prod；有内层 z = 过 JPN+prod 但 S/2Y 掉。解 = 论坛帖①双尺度（两条腿 add：高S腿 + exchange-z载体腿）。

## 10. 工程坑（本会话实测，务必登记）

1. **multisim 通道 bead 失败**：ASI 上 `create_multi_simulation` 多次 6/6 全 FAIL（无错误详情），同表达式同设置单发 POST `/simulations` 却 COMPLETE。诊断为 multisim 序列化问题。应急链路 = brain_client 单发（已用，产 XgaMajj8 等）。
2. **平台去重伪影**：不同表达式（trend_i vs volume_i、group_zscore vs group_neutralize 变体）提交返回同一 alpha id，实读 code 只认先到者。**归因必须逐个 get_alpha_details 读 code，不能信提交映射**。
3. **排队拥塞常态**：multisim 长期卡 progress 0.35、children 空。用轮询脚本 + 20s sleep 等，不要重派（重派触发 429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED）。
4. **winsorize 空操作**：group_rank 之后套 winsorize(std=4) 读数逐位不变（leaNxrGe ≡ zqdLZQaG），单调变换恒等陷阱再次复现，已排除此族。

## 11. ★ 首颗 RA 全闸件（2026-11-22）

**pwaplg5g** = `add(multiply(group_rank(ts_delta(ts_zscore(divide(ebit,assets),252),252),country), 1.5), group_rank(ts_delta(ts_zscore(group_zscore(divide(ebit,assets),exchange),252),252),country))`
设置：ASI/MINVOL1M/D1/SLOW/decay4/trunc0.08/maxTrade ON

| 闸 | 值 | 线 | 判 |
|---|---|---|---|
| Sharpe | 2.28 | 1.58 | ✓ |
| Fitness | 1.28 | 1.0 | ✓ |
| 2Y | 1.64 | 1.58 | ✓ |
| sub | 1.19 | ✓ | ✓ |
| margin | 13.5bp | ✓ | ✓ |
| TO | 5.85% | [5%,30%] | ✓ |
| **JPN** | ✓ | 1.0 | ✓ |
| **Robust S/Ret** | ✓ | 90% | ✓ |
| failed_ra_count | **0** | 0 | ✓ |

**配方（可复制）**：双尺度 add = 1.5×高S腿(country 外层, 无内层z) + 1×exchange-z载体腿。
- 1:1 版 Grm7oV9P：2Y 1.55 差 0.03、prod 0.778 FAIL
- 1.5:1 版 pwaplg5g：2Y 1.64 过、RA 全闸——加权把 2Y 抬过闸
- 权重方向关键：1.5×高S腿（不是 exchange 腿），加重 exchange 腿版 gJa0Mzb0 2Y 反而掉到 1.44

**待终验**：prod/self（check_correlation，corr 槽被并行任务占用，等 240s 重查）。

**塔位**：fundamental 当前 0/3（未点亮）——若 prod/self 过，是有效交付件。

## 12. 配方复制测试（2026-11-22）—— 分子决定 JPN 上限

双尺度 1.5:1 配方复制到不同分子：

| alpha | 分子/分母 | 权重 | S | F | 2Y | JPN | failed_ra |
|---|---|---|---|---|---|---|---|
| **pwaplg5g** | ebit/assets | 1.5 | 2.28 | 1.28 | 1.64 | **✓过** | **0 全闸** |
| 1YW2z3NJ | ebit/equity | 1.5 | 2.30 | 1.30 | 1.71 | 0.92 | 1 |
| P05AGMnW | ebit/equity | 1.2 | 2.26 | 1.27 | 1.66 | 0.93 | 1 |
| MP62LvYz | operating_income/assets | 1.5 | 2.35 | 1.34 | 1.60 | 0.88 | 1 |
| akag1VN1 | operating_income/assets | 1.2 | 2.32 | 1.31 | 1.53 | 待测 | 2 |

**结论**：JPN 上限由**分子经济含义**决定，非权重微调可达。ebit/assets（盈利/资产=ROA 类效率）日本定价力最强（过 1.0）；ebit/equity（ROE 类）0.92 天花板；operating_income/assets 0.88 天花板。要凑多颗全闸件需换**不同经济机制**的分子（现金流质量、杠杆变化、margin 轨迹），而非同族换分母。

## 13. ★★ 互相关终判（2026-11-22）—— fundamental ebit 系只能交 1 颗

compute_mutual_correlation（4 年日收益，本地不占 corr 槽）5 颗 ebit 系候选：

| 对 | ρ |
|---|---|
| pwaplg5g ↔ blaKRQxN | **0.7973** |
| 1YW2z3NJ ↔ P05AGMnW | 0.9985 |
| pwaplg5g ↔ 1YW2z3NJ | 0.9308 |
| pwaplg5g ↔ MP62LvYz | 0.9257 |
| blaKRQxN ↔ MP62LvYz | 0.7542 |
| **最大互不相关子集（ρ<0.7）** | **1 颗** |

**结论**：所有 ebit 系全闸/近闸件共用 `ts_delta(ts_zscore(divide(ebit,X),252),252)` + 双尺度骨架，即使换分子（assets/equity/sales）ρ 仍 0.75–0.99。**fundamental 类别 ebit 机制只能交付 1 颗**。要凑多颗低相关件必须换**数据类别**（analyst 1.5x / shortinterest 1.3x / model），且新类别要重新走"近闸→破 JPN+prod"流程。

**换集理由（合规，用户"确实无计可施才换"）**：fundamental23 内已挖 20+ 臂、覆盖 ebit 全部合法分子 + 现金流 + 毛利率 + 杠杆机制，全闸件互相关钉死 ≥0.75，同塔只能 1 席；继续在集内投入无法增加交付数。转 analyst69（ASI 1.5x 最高乘数，JPN 高覆盖，论坛帖①推荐，ANALYST 塔 0/3 未点亮）。

## 14. 现金流/毛利率/杠杆机制实测（均不达标）
- cashflow_op 水平双尺度 P05A5jrM：S1.53/F0.70/2Y0.4 failed_ra=3 ✗
- fnd23_ppgs 毛利率 mLalaeJ9：S−0.14 ✗
- debt/assets 杠杆变化 KPg2OGg1：S−0.21 ✗
⇒ fundamental 类只有 ebit 分子（ROA 效率 / 利润率轨迹）有 JPN 定价力。

## 15. ★★ prod 钉子墙 vs 强度 —— ebit 系双墙夹击（2026-11-22 终判）

| 骨架 | S | F | 2Y | JPN | RA | prod |
|---|---|---|---|---|---|---|
| 高S腿 only (zqdLZQaG) | 2.36 | 1.35 | 1.82 | 0.94 | ✗ | **0.8336 FAIL** |
| 纯 exchange-z (9ql261Px) | 1.58 | 0.74 | 0.90 | 0.98 | ✗ | **0.6447 ✓** |
| 1:1 add (Grm7oV9P) | 2.21 | 1.22 | 1.55 | ✓ | ✗2Y | **0.778 FAIL** |
| **1.5:1 add (pwaplg5g)** | **2.28** | **1.28** | **1.64** | **✓** | **✓0** | **0.8018 FAIL** |
| 纯ex-z 504长窗 (MP6228j6) | 1.55 | 0.72 | 1.17 | — | ✗ | — |
| 纯ex-z avdiff (vRAoozR3) | 1.42 | 0.64 | 0.55 | — | ✗ | — |

**结构性结论**：ebit 系存在"**强度 ↔ prod 干净**"的严格对立：
- 高 S 腿提供 S/2Y/JPN，但携带 prod 钉子（0.83）
- exchange-z 腿 prod 干净（0.64），但 S/2Y 天然不足（1.58/0.9）
- 双尺度 add 落在中间，**prod 恒 0.78–0.80 FAIL**

prod 直方图形态：bucket [0.8,0.9) 仅 1 条、[0.7,0.8) 2 条，主体 [−0.1,0.2] 健康 ⇒ **典型钉子型**（平台有 1–2 颗已提交的近重复件），不是密墙。按 D0-P 诊断：钉子型要**换信息源**（换分子/分母/加第二条正交信息腿），换形态（窗口/算子）不逃逸。

**JPN 与 prod 双墙夹击**：JPN 达标需要 ebit/assets 这个分子；而 ebit/assets 在 ASI 已有人做过近重复件。⇒ fundamental23 ebit 机制**提交级不可达**（RA 全闸但 prod 撞钉子）。

**下一步方向（诚实）**：
1. 换分子经济含义（非 ebit）→ 掉 JPN（已验证 ebit/equity 0.92、operating_income 0.88、cashflow 弱）
2. 换数据集类别（shortinterest/model/analyst）→ 需重走完整流程，且 analyst 已证 rating JPN 0.52
3. 收口为"1 颗 RA-clean 候选（prod 待破）"，如实交付

## 16. prod 破墙三法实测全灭（2026-11-22 终局）

| 杠杆 | 骨架 | S | F | 2Y | 结论 |
|---|---|---|---|---|---|
| ① 子集门控 trade_when(rank(cap)>0.2) | 双尺度+门控 | 1.79 | 0.91 | **0.76** | 2Y 崩（1.64→0.76）|
| ① 门控 >0.5 | 同上 | 0.90 | 0.34 | −0.33 | 全崩 |
| ② vector_neut(双尺度, rating) | 残差化 | 0.88 | 0.31 | 0.78 | 强度崩 |
| ② vector_neut(高S腿, rating) | 残差化 | 1.01 | 0.38 | 0.99 | 强度崩 |

**机制原因**：
- 子集门控（只在大票持仓）把日股/小票排除 → JPN 与收益同时受损，2Y 崩
- analyst rating 与 ebit 同属"优质公司"因子（相关高），残差化连主信号一起削掉

**★ 本会话 final 判定**：fundamental23 ebit 机制在 ASI 撞 **JPN 墙 + prod 钉子墙双夹击**，三法（门控/残差/换形态）全灭 ⇒ **提交级（prod<0.7）本会话不可达**。最优件 pwaplg5g：RA 全闸（failed_ra=0，含 JPN/Robust）但 prod 0.8018 FAIL。

**下次会话可行方向（按优先级）**：
1. **shortinterest**（1.3x，日韩台融券约束独特 alpha，与 ebit 财务机制正交，论坛帖①推荐）—— 唯一还没试的、有独立信息源特征的类别
2. 找 ebit/assets 在 ASI 的 prod 钉子件是谁（用 get_user_alphas 查自己已提交的 ASI fundamental alpha），若钉子是自己旧件，可考虑换形态逃逸；若是他人件则不可破
3. 换 ASSET 相关但不是 ebit 的分子 + 重新跑 JPN 打标（如 ebitda/assets），验证 JPN 是否仍能过 1.0

## 17. prod 钉子归属诊断（2026-11-22，零配额）

用 get_user_alphas(region=ASI, stage=OS) 实读本账号 ASI 已提交 12 颗（2 SUPER + 10 REGULAR），全部 failed_ra_count=0：

| alpha | 类别塔 | 已提交 prod | S | 备注 |
|---|---|---|---|---|
| QPv88bJW | SUPER | 0.5023 | 3.61 | MINVOL10M/COUNTRY |
| d5WGG5bg | SUPER | 0.51 | 5.38 | MINVOL1M/STATISTICAL |
| P0obGoQJ | OTHER 1.4x | 0.5973 | 3.06 | dl_riskfree label |
| E5ReEnpP | OTHER 1.4x | 0.6932 | 1.93 | PowerPoolSelected |
| j28nKkQo | OTHER 1.4x | 0.6325 | 2.18 | — |
| E5R56EbR | PV+SENT | 0.6918 | 2.96 | pre-close 30m 反转 |
| 1YZYj5QQ | PV+SENT | 0.5732 | 2.59 | pre-close 60m |
| P02wbJAM | PV+SENT+OTHER | 0.6715 | 2.30 | news gate |
| 88jaV5lv | PV+SENT | 0.5093 | 2.35 | — |
| LLNgdpw2 | PV+SENT | 0.6467 | 1.98 | — |
| rKjY5vGj | RISK+MODEL | 0.6327 | 2.01 | cnn 三字段 |
| qMNMbeGj | OTHER 1.4x | 0.62 | 1.72 | other36 空头持仓 |

**决定性结论**：本账号 ASI **无任何已提交的 fundamental 类 alpha** ⇒ pwaplg5g 的 prod 钉子（0.80）**来自他人已提交件，不可控**。按 D0-P 诊断：他人钉子 + 三破法（子集门控/残差正交/换形态）全灭 ⇒ **fundamental23 ebit 机制在 ASI 提交级不可达**，本会话 final。

**塔位实读**（get_pyramid_alphas）：ASI 当季 other=3（已满）、其余 14 类全 0。⇒ fundamental/analyst/model/news 等塔都还空着，有价值，但需要找到**prod 干净**的机制。

**★ 可复用的正面情报**：已提交的 ASI 件里 OTHER 塔 4 颗（P0obGoQJ/E5ReEnpP/j28nKkQo/qMNMbeGj）prod 0.59-0.69 全在红线内，机制集中在 **dl_riskfree probability_label 分位族** 和 **other36 空头持仓变化**。这两族是 ASI 已验证能过 prod 的信息源，可作为下一次挖未满塔的起点（但需注意 other 塔已 3/3 满，同样信息源换塔需走 ATOM/跨类组合）。
