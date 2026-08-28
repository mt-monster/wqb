# Findings: EUR REGULAR 战役（2026-08-24 重启）

## Requirements
- 区域：EUR；类型：REGULAR
- 完整 S-PRE→S6，白名单外不 generate/simulate
- 10 个可提交（OS ACTIVE 或硬闸全过）后停止
- judge READY 后报告等确认，不自动提交
- prod_corr ≥ 0.7 不提交，回 Mode B
- 不同数据集策略相关 < 0.4
- 每 10 次回测做多样性评估

## S-PRE 配置包（2026-08-24）

```
region=EUR  universe=TOP2500  delay=1
neutralization=SUBINDUSTRY decay=4（win 配方主轨）/ COUNTRY decay=6 已离开
truncation=0.08  maxTrade=ON  pasteurization=ON  nanHandling=ON
intent=REGULAR 挖矿（PPA 跳过：Power Pool=GLB Liquid TOPDIV3000）
campaign-dir=tracking/EUR/
```

合法档（平台实测，勿套用 USA）：
- Universe: TOP2500 / TOP1200 / TOP800 / TOP400 / ILLIQUID_MINVOL1M / TOPCS1600
- Neutralization 含 COUNTRY / SUBINDUSTRY / INDUSTRY / SECTOR / STATISTICAL ...
- Delay: 0 和 1 均合法；本战役 D1

## 进度基线
| 项 | 值 |
|---|---|
| OS ACTIVE RA | 3（`Wj71Q12o`，`78jdv6b1`，`Wj7g2gAx`）目标 10 |
| submit_ready | 用户已提交两颗；池空 |
| 最新关闭波 | Wave73 无 READY（surprise S1.04 2Y=0.95 salvage mix） |
| 在飞 | Wave74 surprise×未用 PV win mix 七槽回测中 |
| 缺口 | 7 颗到停止闸 10 |


`Wj71Q12o` 骨架：0.40×(0.65 长窗 FCF-to-price 反号 + 0.35 短窗 trailing FCF 反号) + 0.60×breakaway_gap_upward 反号。禁止再克隆该 mix。

## 排除（dead_ends 命中的信号族）
- FCF 纯 invert 残差 / FCF 少数腿×价值 to-price / Wj71Q12o FCF×gap 克隆
- MH mid_term estrev；long_term estrev 整条反号主导；estrev 反号稀释
- MH capacq invert 残差主导；BS / price_adj_eps 残差探针
- model238 d1 rank 互配；alignment/industry_relative/preference 低竞争字段（仍 prod~0.89）→ **离开 model238**
- model36 credit/default_risk 主导与残差
- ARH profit90d 主导 / primary mix / surprise×primary / surprise 残差
- starhold screening gzscore/residual；starhold sector/industry/country rank 主导
- AIEQ vol/score 主导；AIEQ analyst revision 无 vol/score（|S|0.57）
- continuation_score 复合；pattern_scores breakaway 单独残差
- 跨区：emotion 族、稀疏事件未 backfill、同骨架变体自相残杀、本地 prod 系统性低估

## Wave38 关键发现（最新关闭波）
- MH quality：capacq invert 残差 S1.28 F0.69 2Y1.80 **prod 0.8851** → 判死
- MH 非 FCF 价值残差：`O07n78kJ` S1.04 F0.49 2Y1.44（未过廉价闸但有信号）
- AIEQ forensic/accrual：max S0.87；combo 被 cancel
- AIEQ analyst 无 vol/score：max |S|0.57 弱集
- starhold sector：`9qX9XMNq` S1.28 F0.91 2Y1.43 **prod 0.8992** → 判死

## 仍有信号、未整集判死
- `multi_horizon_alpha`：非 FCF 价值残差仍有 IS（S~1.0）；腿禁用 ≠ 整集判死
- `ai_equity_alpha`：forensic/accrual 黄区且 prod 墙；禁止 vol/score 主导。Wave50 改测 quality/opacity/unused liquidity/clarity × PV
- 其余填槽必须等 S0 白名单；禁止五槽同时打 5 个未证明信号的新数据集

## 跨区铁律（开局必遵）
1. 饱和风格调参无效 → Mode B 换概念
2. 本地 prod 是下限，接近 0.7 必须走平台判定
3. 单字段探针是有无信号，不是找 alpha
4. 慢×快跨周期混合才是已验证配方；同周期互混无效
5. 反向取号写 `-rank(...)` 不要 `reverse(rank(...))`

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 配置包不替代 S0 实时体检 | matrix 存快照；generate 白名单 = S0 tier1 |
| 甜区 ac 91–318 优先 | EUR thresholds crowd_sweet_spot；零竞争多为伪白空间 |

## Wave39 关键发现（最新关闭波）
- news85 DNN 情绪：max \|S\|0.32，镜像对称 → 离开
- invert mgeff `vRj5O7kG` S1.00 F0.53 **prod 0.8178** → 判死主导
- invert FY2 `78jxLkAO` S0.95 F0.69 **prod 0.945** → 与 estrev 同墙
- AIEQ forensic×accrual `KP7nJl8g` S0.96 F0.58 **2Y 1.90** 仍 **prod 0.8161**
- MH 价值 country/sales max S0.89，无独立 IS

## Wave40 关键发现（最新关闭波）
- news84：max \|S\|0.35，镜像对称 → 离开新闻情绪探针
- starhold industry `gJjma78O` S1.34 F0.90 2Y1.59 **prod 0.8787**
- starhold country `xAjevXdp` S1.19 **prod 0.8935** → 与 screening/sector 同墙
- MH 杠杆 industry 残差 `88lONkOV` \|S\|1.58：有独立 IS，禁止主导；Wave41 作 0.40 慢腿
- MH mom max 0.92、AIEQ asset max 0.72：无近闸

## Wave41 关键发现（配方复现）
- **`P07nzzrK`**：0.40 invert capacq 残差 × 0.60 invert v_reversal。S1.55 F0.92 2Y1.38 SUB0.95 RN1.12 **prod 0.6958** self 0.14。双金字塔。**允许 Mode A**。
- `qMjnGgJK` deep_value×v_reversal S1.21 **prod 0.6857**
- `Jj7nzg62` 杠杆×wedge 2Y2.07 但 **prod 0.755** → 禁 Mode A
- Wave42 Mode A：`58lLeaen` S1.67 F1.02 **prod 0.525**；`0mwA6ex6` S1.65 F1.00 梯子 **1.53** prod 0.6534。只卡 IS_LADDER（2017 负年）。
- Wave43：`bljNAGQp` 三腿 **硬闸全过**（S1.81 F1.17 梯子 2.11）但 **prod 0.7028**，self 0.02，禁提交。`9qX9kLV1` prod **0.5622** 梯子 **1.56**。
- Wave44：`e7zrV7aM` **prod 0.6971** 梯子 1.53；`rKjW9Ne8` prod 0.5593 梯子 **刚好 1.58**（未过）。0.25 vs 0.35 MODEL 对偶。
- Wave45：**`78jdv6b1` judge READY**（S1.74 F1.11 梯子 2.05 prod **0.6945** self **-0.008**）。提交层 SUBMITTABLE。等确认。
- 同族 `YP7AEMKq` prod 0.6963 勿双提；0.33 MODEL `mLjX0ad6` prod 0.7055 禁提。
- Wave47：**`Wj7g2gAx` judge READY**（S1.80 F1.17 梯子 2.16 prod **0.5463** self vs `78jdv6b1` **0.486**）。RN 1.00 贴线。mid/short capacq 弱。
- Wave48：FS/growth/ROE/income/value_analyst 三腿过闸后 **prod 0.81–0.91**。禁止再磨这些 rank 慢腿。
- Wave49：PTA/street/nrev/pmom/decay 全未过廉价闸（nrev 近闸 S1.54 F0.97）。离开这些 MH 概念。
- Wave50：AIEQ quality/opacity/liq/clarity + five_day 全未过闸（最好 liquidity S1.31）。
- Wave51：AIEQ moat/util/replacement/BS + pspat volume/trend 全未过闸（最好 utilization S1.09）；competitive 槽平台 ERROR。
- Wave52：AIEQ 利润率/增长/现金流全未过闸（最好 revenue growth consistency S1.20）。
- Wave53：AIEQ 杠杆/估值/股东回报/physics 全未过闸（最好 valuation suite S1.02）。
- Wave54：AIEQ 股息/收益率/相关风险/ROA/技术估值/均值回复全未过闸（最好 financial yield S1.18）。Wave55 改测股东待遇/预测离散/资金流/PE。

## Wave41
按 win `EUR-WIN-SLOW-MODEL-X-FAST-PV`：0.40 慢 MODEL × 0.60 快 PV，**SUBINDUSTRY/4**，每槽 2 骨架。槽 5 = invert leverage residual × PV（不用 yield）。

## S0 白名单（23 tier1，generate 仅此）
优先未挖：news85（已探）、news84/38。离开：model238、IBES 价格面板、news_sentiment_nlp RED。
deprioritize 历史 RED：gsm/m354/aft/mlfp/m193/oth571/acq/starmine/pspat/cnn。
