# EUR 战役波次台账（WAVE_LEDGER）

> 每波回收后追加一节；下一波开跑前必须先读「下一波决策」。OS ACTIVE=3（`Wj71Q12o` `78jdv6b1` `Wj7g2gAx`）。judge READY 只报告、禁止自动提交。

硬闸：Sharpe>1.58 · Fitness>1 · 2Y>1.6 · Margin>5bp · TVR 5–30% · RN Sharpe>1 · **PROD <0.7**
设置（Wave35/36/37）：EUR TOP2500 D1 COUNTRY decay6 truncation 0.08 nan_handling=ON max_trade=ON pasteurization=ON

## 累计

| 指标 | 值 | 更新 |
|---|---|---|
| OS ACTIVE RA | 3（`Wj71Q12o` `78jdv6b1` `Wj7g2gAx`）目标 10 | 2026-08-25 |
| READY / 自动提交 | 用户已提交两颗；池空 / 禁止自动 | 2026-08-25 |
| 最新关闭波 | Wave81 PARTIAL（FCF invert 廉价闸过但 prod0.73；EV invert `MP7Qo0gM` prod0.60 RN0.55） | 2026-08-25 |
| 在飞 | Wave82 Mode B invert 未用 MH 修订/成长慢腿 × common_gap_up | 2026-08-25 |

---

## 波1（2026-08-18）— news_sentiment_dl 探针

VECTOR 情绪文本 24 探针全弱判死。详见 `eur_d1_campaign_state.json.bak`。

## 波2（2026-08-18）— chart_cnn_alpha 探针

leapstar6 rn 失效判死。详见 `eur_d1_campaign_state.json.bak`。

## 波3（2026-08-18）— multi_horizon 基本面镜像 salvage

基本面全线负向，进入 FCF 镜像家族。后续 3b/3c/3d 与 wave4–35 结论在 `wave_results` / `results/wave*_results.csv`。

## 波36（2026-08-24）— FCF 少数腿稀释 + 非 FCF 残差 + model238 组合

### 批次

| 槽 | 内容 | multisim | 设置 |
|---|---|---|---|
| 1 | FCF 残差 0.35–0.45 × ebitda/EV、deep_value、NOA、estrev、sales、growth、ROE | `2PxaL0gUF4jPcFBeKRZazei` | COUNTRY/6 |
| 2 | 非 FCF 反号残差（ebitda/EV、deep_value、NOA、sales、estrev） | `4totI7q74GCcKuklUhYO8j` | COUNTRY/6 |
| 3 | 三腿稀释（FCF 0.30 + 价值/修订） | `4EQkQP8RB50sbxN1bnDVnE8m` | COUNTRY/6 |
| 4 | model238 change/screening/owner 组合 | `4EeYpvaCu4rbbpc1eU8fhafh` | COUNTRY/6 |
| 5 | model238 region/country 组合 | `2MvweZegG4HQa1hb6XUjDRB` | COUNTRY/6 |

槽 4 有 2 个子模拟解析到已有 starhold alpha（`j2jn0RRQ` / `78jx1bEQ`，wave35），不计入本波新样本。有效新 alpha **38** 条，0 ERROR。

### 闸门结论

| 槽 | max \|S\| | F | 2Y | prod | 备注 |
|---|---|---|---|---|---|
| 1 FCF 少数腿 | `np7n8Mgd` S1.17 | 0.69 | **2.03** | **0.8693** | 0.40 FCF 残差 + 0.60 ebitda 残差；相对纯 FCF `88lOQrdm` prod 0.938 只降到 0.87，**未破 0.7** |
| 2 非 FCF 残差 | `1YwozEAW` S**-1.48** | -0.99 | -1.10 | **0.7748**（min **-0.9477**） | estrev industry 残差有独立 IS；self vs Wj71Q12o **0.17** |
| 3 三腿 | `j2jnrlbQ` \|S\|1.14 | -0.68 | -0.52 | — | FCF 0.30 正号最大仅 S0.49，IS 被稀释死 |
| 4 m238 组合 | `lej73Xm7` S1.16 | 0.74 | 1.59 | **0.8851** | 未超过 wave26 单字段 screening S1.32 F0.87 |
| 5 m238 region | `1YwozLvz` S1.28 | 0.85 | 1.48 | **0.896** | country 残差；LOW_SUB 0.35 |

互相关系（本地 4y）：`1YwozLvz`×`lej73Xm7` **0.96**（同族）；estrev 残差 × m238 **-0.74 / -0.81**（反号后会对齐机构持仓拥挤方向）；FCF 少数腿对二者均 ~0（正交但自身 prod 墙）。

无 READY。无自动提交。

### 结构性发现

1. **FCF 少数腿不能把 prod 从 0.94 压到 <0.7**。与同属 to-price/价值的 ebitda/EV、deep_value 混合，prod 仍 0.87，Sharpe 从 1.66 掉到 1.17。三腿 0.30 进一步杀死 IS。禁止再对 FCF 残差做 Mode A，禁止继续用价值腿稀释 FCF。
2. **非 FCF 残差有独立 IS**：`long_term_estimate_revision_europe_rank` industry 残差 \|S\|1.48、self 0.17。但 **禁止把该残差整条反号当主导**——反号后 prod 会走向 ~0.95，并与 model238 同向（拥挤的机构/修订方向）。下一波只允许：换期限（mid_term estrev alphaCount=0）或把反号残差当 ≤0.30 少数腿、配 growth/FS（alphaCount=0）。
3. **model238 组合 vs wave26 单字段**：组合没有打过 `rank(mdl238_global_screening_rank)` S1.32；2Y 略升（1.48–1.59 vs 1.38），LOW_SUB 仍 0.35–0.42，prod 0.885–0.896。change/screening/industry/country **d1 rank 互配是同一拥挤族**，禁止再 Mode A 调 decay。

### 判死（本波）

- `EUR-FCF-MINORITY-VALUE-MIX-PROD`：FCF 残差 0.35–0.45 × 价值 to-price
- `EUR-M238-D1-RANK-COMBO-PROD`：model238 d1 rank 互配
- `EUR-MH-ESTREV-RESID-INVERT-CROWD`：long_term estrev industry 残差整条反号当主导

### 下一波决策（Wave37）

五槽全给已验证信号的单数据集组合 / 同集换概念，**弱探针 0 槽**。COUNTRY decay6。禁止：profit90d 主导、ARH surprise×primary、starhold screening gzscore、vol+alpha_score 主导、continuation、纯 invert FCF 残差、Wj71Q12o FCF×gap、estrev 残差整条反号主导。

1. mid_term estrev（alphaCount=0）残差/gzscore/与 growth 组合
2. long/mid growth + FS strength（alphaCount=0）单集组合
3. long_term estrev 反号残差仅 0.30 少数腿 × growth/FS/mid_term；另加 ts_av_diff 与 country gzscore
4. model238 **低竞争字段**：alignment_d1 / change_in_preference / industry_relative（非再配 screening/change/country d1 rank）
5. model238 Mode B 价差：screening−country、alignment−screening、group_neutralize；禁止再发 wave26 裸 screening

READY：无，等用户确认才提交 alpha。

Wave37 已五槽同提并回收（COUNTRY/6，40 COMPLETE，0 ERROR）：

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | mid_term estrev 残差/gzscore + growth | `4enk6XeNS4huaDc9VLIuBcd` |
| 2 | growth + FS strength 低竞争组合 | `618Za7Or50WakIkCkkPYIX` |
| 3 | estrev 反号残差仅 0.30 × growth/FS/mid | `2NYXUCdvy58A8Y618PKS0Kul` |
| 4 | m238 低竞争 alignment/preference/industry_rel | `AhTWb7w44DZ98QjaQeiEUH` |
| 5 | m238 价差 screening−country / neutralize | `2KRfyrdLA4LHciy3Aiw3XZS` |

### 闸门结论

| 槽 | max \|S\| | F | 2Y | prod | 备注 |
|---|---|---|---|---|---|
| 1 mid_term estrev | `88lOpzjm` S0.52 | 0.19 | -0.03 | — | 期限平移失败，不独立于 long_term 残差 |
| 2 growth+FS | `78jxzz0v` \|S\|0.89 | -0.43 | -0.26 | — | 反号 growth S0.61；mid mix S0.55 |
| 3 稀释 | `O07nGp8Y` S1.08 | 0.51 | 0.88 | **0.7057** | self vs Wj71Q12o **-0.07**；`wpj5aRbQ` \|S\|1.30 |
| 4 m238 低竞争 | `np7nNKow` S1.35 | 0.92 | 1.46 | `9qX9pVKe` **0.8787** | alignment `ZY7jE0qd` prod **0.8923** |
| 5 m238 价差 | `ak7N1db1` S1.35 | 0.92 | 1.46 | **0.8891** | 价差 S0.06；三腿 mix prod **0.8889** |

无 READY。无自动提交。

### 结构性发现

1. **mid_term estrev 不是独立信号**。相对 long_term 残差 \|S\|1.48，mid_term 最大仅 0.52。期限平移失败。
2. **estrev 反号残差 0.30–0.40 稀释仍过不了 prod 0.7**。O07nGp8Y prod 0.7057，禁止继续稀释这条腿。
3. **m238 低竞争字段没有低于 change/screening 的 prod 0.89**。industry_relative 0.8787、alignment 0.8923、三腿 mix 0.8889。离开 model238。

### 判死（本波）

- `EUR-MH-MIDTERM-ESTREV-WEAK`
- `EUR-MH-ESTREV-INVERT-DILUTE-PROD`
- `EUR-M238-UNCROWDED-ALIGN-INDREL-PROD`

### 下一波决策（Wave38）

五槽全给已验证信号的单数据集组合，**弱探针 0 槽**。COUNTRY decay6。离开 model238 / mid_term estrev / estrev 反号主导。禁止：profit90d 主导、ARH surprise×primary、starhold screening gzscore、vol+alpha_score 主导、continuation、纯 invert FCF 残差、Wj71Q12o FCF×gap、estrev 残差整条反号主导、m238 d1 rank 互配。

1. MH quality/accrual 未用字段：balance_sheet + capital_acquisition + price_adj_eps 残差
2. MH 非 FCF 价值残差组合：deep_value 反号残差 + ebitda 反号残差 + EV（wave36 单腿 S0.83/0.73）
3. AIEQ forensics + accruals（禁 vol/score 主导；accruals 曾 \|S\|0.83）
4. AIEQ analyst revision/target/opinion（禁 vol/score）
5. starhold owner/change/sector，**不含 screening gzscore**

Wave38 已五槽同提（COUNTRY/6）：

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | MH quality/accrual 残差 | `EOgobfd5dg9PEGS7Z1B4W` |
| 2 | MH 非 FCF 价值残差组合 | `2xo3lHdFz4hEaMjbAiytUso` |
| 3 | AIEQ forensics+accruals | `3qNEjA2Yn4EgcJhsiSUNGWl` |
| 4 | AIEQ analyst revision | `1MISnkawf4Bk8Je154J2QvIn` |
| 5 | starhold owner/change/sector 无 screening | `4pFEZqgBO51b93MytxWxYwm` |

Wave38 已回收 closed PARTIAL（见 `wave38_verdict`）。OS ACTIVE 仍 1。

### 下一波决策（Wave39）

五槽：4 槽已验证信号单数据集组合 + **弱探针 1 槽**。COUNTRY decay6。离开 model238 / starhold sector / FCF / estrev 反号主导。禁止：profit90d、ARH surprise×primary、vol+alpha_score 主导、continuation、纯 invert FCF、Wj71Q12o 克隆、`analyst_earnings_ibes`（EUR 实为价格面板）。

1. news85 DNN 情绪 MATRIX（白名单未挖正交集，S1 已入库）
2. MH 未用质量：NOA 变化 + management efficiency + IS rank + PEG
3. MH FY2/街修订（不是 long_term estrev 反号）
4. AIEQ forensic/accrual 继续（禁 vol/score）
5. MH 价值 country gzscore + sales_to_price

Wave39 已五槽同提（COUNTRY/6，gate 5/5 PASS）：

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | news85 情绪 MATRIX 探针 | `4gK7TKa6H4Mda8vKTM4T7h6` |
| 2 | MH NOA/管理效率/PEG | `3usYmbeK74kFaH2t6eYBTJ0` |
| 3 | MH FY2 修订/街修订 | `qcg5Z8hq4VmaQe14BbHTcTv` |
| 4 | AIEQ forensic 继续 | `31b8v78CP58v9ZSYwHC5jTn` |
| 5 | MH 价值 country + sales | `1kN6GI8pN4pnbiT15ly8Zx6C` |

Wave39 已回收 closed PARTIAL（40 COMPLETE，0 READY）。OS ACTIVE 仍 1。

### 闸门结论

| 槽 | max \|S\| | F | 2Y | prod | 备注 |
|---|---|---|---|---|---|
| 1 news85 | 0.32 | 0.08 | — | — | 镜像精确对偶；弱探针早停 |
| 2 MH quality | `vRj5O7kG` S1.00 | 0.53 | 0.79 | **0.8178** | invert mgeff industry gz；TVR 1.7% |
| 3 MH FY2 | `78jxLkAO` S0.95 / 残差 \|S\|1.11 | 0.69 | 0.78 | **0.9450** | FY2 反号 = estrev 同拥挤墙 |
| 4 AIEQ mix | `KP7nJl8g` S0.96 | 0.58 | **1.90** | **0.8161** | 0.6 forensic + 0.4 invert accruals；2Y 过线仍撞 prod |
| 5 MH value | `rKjbdxn1` S0.89 | 0.51 | 1.84 | — | neutralize invert deep_value；sales 无独立 IS |

无 READY。无自动提交。

### 结构性发现

1. **news85 DNN 情绪 MATRIX 无信号**。max \|S\|0.32，正负镜像对称。禁止第二轮裸探针。
2. **管理效率反号已是 EUR/D1/MODEL 墙**。`vRj5O7kG` prod 0.8178。禁止 Mode A，禁止再当主导。
3. **FY2 三月修订反号 = estrev 拥挤族**。`78jxLkAO` prod 0.945。禁止反号主导 / 再稀释。
4. **AIEQ forensic×accrual 组合 2Y 已过线仍 prod 0.82**。禁止再 Mode A 调 decay/权重微调当主导。
5. **MH 价值 country gz / sales_to_price 没有独立 IS**。max 0.89，勿再占槽。

### 判死（本波）

- `EUR-NEWS85-SENTIMENT-MATRIX-WEAK`
- `EUR-MH-MGEFF-INVERT-GZ-PROD`
- `EUR-MH-FY2-INVERT-CROWD`
- `EUR-AIEQ-FORENSIC-ACCRUAL-MIX-PROD`
- `EUR-MH-NOA-PEG-WEAK`
- `EUR-MH-VALUE-COUNTRY-SALES-WEAK`

### 下一波决策（Wave40）

五槽：4 槽白名单内**未挖概念**单数据集组合 + **弱探针 1 槽**。COUNTRY decay6。离开 news85 / FY2 反号 / mgeff 反号 / forensic×accrual 主导 / 价值 country gz。禁止：FCF、estrev 反号、m238、starhold screening/sector、vol/score、profit90d、model28/36 credit、`analyst_earnings_ibes`。

1. news84 迁移情绪 MATRIX（弱探针 1，概念 ≠ news85 DNN）
2. MH 未用杠杆/收益：management_leverage + OLL change + time_weighted_earnings_yield
3. MH 未用动量/衰减：price_momentum × short_term + rational_decay + 5d IR
4. starhold **owner/change/country/industry**，不含 screening/sector
5. AIEQ 未用资产质量：impairment / turnover / liquidity（禁 vol/score/forensic/accrual/analyst 主导）

READY：无，等用户确认才提交 alpha。

## 波40（2026-08-24）— 未挖概念收尾（COUNTRY/6）

### 批次

| 槽 | 内容 | multisim | 设置 |
|---|---|---|---|
| 1 | news84 迁移情绪 MATRIX | `1L4PlEglL4Ura5d1bfgB9LFz` | COUNTRY/6 |
| 2 | MH 杠杆/收益 | `h0T0db1A51998INAgs70PB` | COUNTRY/6 |
| 3 | MH 动量/衰减 | `1gfbMreH85eDcuTjb7OFitt` | COUNTRY/6 |
| 4 | starhold owner/change/country/industry | `2R9YXb4674i0aojfdxE1IFh` | COUNTRY/6 |
| 5 | AIEQ impairment/turnover/liquidity | `5eqwGemi51ocg1RgzHSjRM` | COUNTRY/6 |

### 闸门结论

| 槽 | max \|S\| | F | 2Y | prod | 备注 |
|---|---|---|---|---|---|
| 1 news84 | `KP7ngxpl` 0.35 | 0.08 | — | — | 镜像 `QP7n0moK` -0.32，弱探针 |
| 2 MH lev | `88lONkOV` **-1.58** | -0.87 | -2.68 | 未查（负号） | 杠杆 industry 残差有独立 IS；裸 invert `1YwoWVoX` S0.87 **2Y2.26** |
| 3 MH mom | `88lONd3a` \|S\|0.92 | 0.69 | — | — | 无近闸 |
| 4 starhold | `gJjma78O` **1.34** | **0.90** | **1.59** | **0.8787** | industry rank；country `xAjevXdp` S1.19 prod **0.8935** |
| 5 AIEQ asset | `A1lnxdGW` 0.72 | 0.31 | — | — | impairment 残差，无近闸 |

无 READY。无自动提交。

### 结构性发现

1. **starhold industry/country 与 screening/sector 同墙**。近闸 Fitness 0.90 仍 prod 0.88–0.89，纯 EUR/D1/MODEL。禁止再把 starhold rank 当主导。
2. **news84 = news85**：迁移情绪 MATRIX 无独立 IS，离开 EUR 新闻情绪探针。
3. **杠杆残差是本波唯一可带走的慢腿**：\|S\|1.58，但单金字塔。Wave41 槽 5 用 0.40 mix，不用主导。
4. **COUNTRY/6 六波零产出确认**：设置从本波起跟 win，回到 SUBINDUSTRY/4。

### 判死（本波）

- `EUR-NEWS84-SENTIMENT-MATRIX-WEAK`
- `EUR-STARHOLD-INDUSTRY-RANK-PROD`
- `EUR-STARHOLD-COUNTRY-RANK-PROD`
- `EUR-MH-LEVERAGE-RESID-DOMINANT`（主导禁用；0.40 慢腿仍可用）

### 下一波决策（Wave41）— 跨金字塔 win 换腿

设置跟 win：EUR TOP2500 D1 **SUBINDUSTRY decay4**。
每槽 **2 条骨架**（prod-first）。禁止克隆 `Wj71Q12o` 的 FCF×`median_similarity_breakaway_gap_upward`。
registry win：`EUR-WIN-SLOW-MODEL-X-FAST-PV`。

| 槽 | 慢腿 0.40 | 快腿 0.60 | 候选文件 |
|---|---|---|---|
| 1 | invert capacq industry residual | falling_wedge / v_reversal | `logs/_tmp_w41_s1_capacq_pv.json` |
| 2 | invert mgeff industry gz | common_gap_up / asc_triangle | `logs/_tmp_w41_s2_mgeff_pv.json` |
| 3 | 0.6 forensic + 0.4 invert accruals | downward triangle / falling_wedge | `logs/_tmp_w41_s3_aieq_pv.json` |
| 4 | invert deep_value / ebitda residual | v_reversal / common_gap_up | `logs/_tmp_w41_s4_value_pv.json` |
| 5 | **invert leverage residual**（Wave40 \|S\|1.58） | falling_wedge / common_gap_up | `logs/_tmp_w41_s5_lev_pv.json` |

槽 5 用杠杆残差替换原 yield/OLL（Wave40 最大仅 S0.58）。READY：无，等用户确认才提交 alpha。

## 波41（2026-08-24）— win 换腿 0.40 MODEL × 0.60 PV

设置：EUR TOP2500 D1 **SUBINDUSTRY decay4**。10 条 COMPLETE，0 READY。

### 闸门结论

| 槽 | 最佳 | S | F | 2Y | prod | 备注 |
|---|---|---|---|---|---|---|
| 1 capacq×PV | **`P07nzzrK`** v_reversal | **1.55** | **0.92** | 1.38 | **0.6958** | self 0.14；SUB 0.95；RN 1.12；双金字塔；2017 S-1.38 |
| 2 mgeff×PV | `GrlnzMoP` asc_triangle | 1.17 | 0.64 | 1.24 | — | 双金字塔，未近闸 |
| 3 AIEQ×PV | `1YwoKaLM` | 0.81 | 0.41 | — | — | 弱 |
| 4 value×PV | `qMjnGgJK` deep_value×v_reversal | 1.21 | 0.71 | **1.49** | **0.6857** | self 0.43；SUB 0.53 |
| 5 lev×PV | `Jj7nzg62` | 1.25 | 0.74 | **2.07** | **0.755** | 梯子过但 prod 墙，禁 Mode A |

### 结构性发现

1. **win 配方复现成功**：`P07nzzrK` 是 `Wj71Q12o` 之外第一颗 **prod&lt;0.7** 的 EUR mix，双金字塔 PV+MODEL，self 仅 0.14。
2. 缺口很小：S +0.03、F +0.08、2Y 梯子 +0.20。2017 负年是梯子主因。
3. `qMjnGgJK` 同样 prod 过（0.6857），可作对照设置轨。
4. 杠杆×wedge `Jj7nzg62` 2Y 已过但 prod 0.755 → 不 Mode A。

### 下一波决策（Wave42）— Mode A（prod 已过，允许调参）

冻结 `P07nzzrK` 字段（capacq 残差 + v_reversal）。禁止 Mode A `Jj7nzg62`。

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | 8 条 Mode A（权重 / signed_power / ts_mean / neutralize / gz / ts_rank） | `20VBjc9sz5cDbXzGMj0eN7l` |
| 2 | P07+qMjn **decay3** SUBINDUSTRY | `17xiftajq4VKcxJ19x3jcX66` |
| 3 | P07+qMjn **decay6** SUBINDUSTRY | `LPE0O3fS5a5c5aIFpD6cM7` |
| 4 | P07+qMjn **INDUSTRY** decay4 | `1j7prJa9V4TvbWg1dYibboeJ` |
| 5 | P07+qMjn **SECTOR** decay4 | `1RH6QZcqX4YAavpM1IrZ8k2` |

## 波42（2026-08-24）— Mode A 抬 `P07nzzrK`

S/F 已过线，**只剩 IS_LADDER**。无 READY。

| ID | 变体 | S | F | 2Y梯子 | prod | self |
|---|---|---|---|---|---|---|
| **`58lLeaen`** | 0.40 + ts_rank(v_reversal,66) | **1.67** | **1.02** | 1.45 | **0.525** | 0.32 |
| **`0mwA6ex6`** | 0.45/0.55 权重 | **1.65** | **1.00** | **1.53** | **0.6534** | 0.15 |
| `d5jnonJK` | 同式 INDUSTRY | 1.63 | 1.04 | 1.23 | — | — |

2017 仍为负年（`0mwA6ex6` S-1.43）。decay3/6 与 SECTOR 无增益。

### 下一波决策（Wave43）— 修梯子 / 2017

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | 0.45/0.55 + ts_rank 66/120 | `16z3VeE4VbcB5Q0l3luNO` |
| 2 | 三腿 capacq + v_reversal + wedge/gap | `2EfRM3ct455y9KKvvRNZNxY` |
| 3 | 最佳两式 × ILLIQUID_MINVOL1M | `2Z15pWaQd4gPce4Hm22F7bi` |
| 4 | 最佳两式 × TOPCS1600 | `4ihYvLfqv50P8HqQSLO71rR` |
| 5 | 最佳两式 decay5 | `Hg44xcKM57B9nJ19eYRKvLV` |

## 波43（2026-08-24）— 修梯子

ILLIQUID / TOPCS 无增益。无 READY。

| ID | 变体 | S | F | 梯子 | prod | 备注 |
|---|---|---|---|---|---|---|
| **`bljNAGQp`** | 0.35 capacq + 0.40 v_reversal + 0.25 wedge | **1.81** | **1.17** | **2.11 PASS** | **0.7028** | Failed RA=0；self vs Wj71 **0.02**；禁提交 |
| **`9qX9kLV1`** | 0.45/0.55 + ts_rank 66 | **1.71** | **1.06** | **1.56** | **0.5622** | self 0.30；只差梯子 0.02 |
| `88lOXd37` | ts_rank 120 | 1.77 | 1.11 | 1.44 | — | 梯子更差 |

### 下一波决策（Wave44）

轨 A：Mode B 降 `bljNAGQp` 的 MODEL 权重（prod≥0.7 禁 Mode A）。
轨 B：Mode A 抬 `9qX9kLV1` 梯子（prod 已过）。

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | 三腿 PV 加重 0.25 MODEL | `19UmCwfoK4BZaaysAlsasct` |
| 2 | 三腿换 wedge→gap/triangle | `4FDmH86cj4CV8zu1eAcZ4W34` |
| 3 | 三腿 + ts_rank | `VvuENdM152k91pg9pW6YsW` |
| 4 | ts_rank 90 / 0.40-0.60 | `2jK2fl4v24pkae015sP3uqZl` |
| 5 | `9qX9kLV1` decay3 | `2SMSsM6Zp4ke8VQBevtLQFH` |

## 波44（2026-08-24）— 降 prod / 补梯子

换 PV 字段（gap/triangle）杀死 IS。无 READY。

| ID | 变体 | S | F | 梯子 | prod |
|---|---|---|---|---|---|
| `e7zrV7aM` | 0.25/0.45/0.30 三腿 | 1.68 | 1.05 | 1.53 | **0.6971** |
| `rKjW9Ne8` | 0.45/0.55 ts_rank decay3 | 1.69 | 1.04 | **1.58=限** | **0.5593** |
| `np7WmeOE` | 0.30 ts_rank 三腿 | 1.65 | 1.06 | 1.53 | 0.6198 |

对偶：0.35 MODEL 梯子过、prod 0.7028；0.25 MODEL prod 过、梯子掉。下一波插值 0.28–0.33。

### 下一波决策（Wave45）

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | 三腿 0.28 / 0.30 MODEL | `4BHUIi8y34Xy9QqnA1CVe5X` |
| 2 | 三腿 0.32 / 0.33 MODEL | `23AR2Cbxc5aXbOl7GJbPw97` |
| 3 | ts_rank decay2 | `3qzDJ28Vj4L59DO5hc5SRJr` |
| 4 | 三腿 0.25/0.28 **decay3** | `2g4iWY2ls4KQbZRq3QkuHRT` |
| 5 | ts_rank 三腿 0.30/0.32 | `ktmXy9yb54tbupVnQFzHS5` |

## 波45（2026-08-24）— 插值找到 READY

| ID | MODEL | S | F | 梯子 | prod | RA |
|---|---|---|---|---|---|---|
| **`78jdv6b1`** | 0.30/0.40/0.30 | **1.74** | **1.11** | **2.05** | **0.6945** | **0 FAIL** |
| `YP7AEMKq` | 0.28/0.42/0.30 | 1.72 | 1.09 | 2.05 | 0.6963 | 0 FAIL（同族，勿双提） |
| `mLjX0ad6` | 0.33/0.42/0.25 | 1.79 | 1.15 | 2.11 | **0.7055** | 0 FAIL但 prod 墙 |

`tools/submit_verdict.py`：**SUBMITTABLE**。self vs `Wj71Q12o` **-0.008**。稳健性 CONDITIONAL（2022 S0.79，2017 旧年 -1.68 不拒）。**等用户确认才 submit**。

### 下一波决策（Wave46）— 换慢腿，禁止再磨 capacq 权重

设置跟 win：EUR TOP2500 D1 **SUBINDUSTRY decay4**。把 0.30/0.40/0.30 三腿配方迁到未磨过的慢腿；槽 5 换未用 PV。

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | mgeff residual/gz × v_rev/wedge 三腿 | `1M3RVv8Y04E2920yBknz3Rq` |
| 2 | leverage residual 三腿（Wave41 两腿 prod 0.755） | `2KrpOD4Oy58daR3iePKKL2J` |
| 3 | deep_value residual 三腿（Wave41 两腿 prod 0.6857） | `3ItZ6sffr56vcvm56QCDPUu` |
| 4 | ebitda/EV residual × v_rev/wedge（不用 gap） | `4DOwkclN4pd8xrElZK9DcZ` |
| 5 | 新 PV：continuation_wedge / support-flat / v_continuation | `2pa646gEA4AZaDc1geRjJQPB` |

## 波46（2026-08-24）— 换慢腿

杠杆三腿硬闸能过，**prod 墙且降 MODEL 更糟**。无新 READY。

| ID | 慢腿 | S | F | 梯子 | RN | prod |
|---|---|---|---|---|---|---|
| `P071A7zL` | 0.32 lev | 1.80 | 1.13 | **2.27** | 1.02 | **0.7644** |
| `E5lK2l80` | 0.30 lev | 1.77 | 1.11 | 2.17 | 1.00 | **0.7867** |
| `d5jQPj3j` | 0.28 lev | 1.73 | 1.08 | 2.04 | 1.00 | **0.7958** |
| `RR7rvY50` | 0.30 deep_value | 1.79 | 1.16 | 2.03 | **0.89** | — |
| `qMjXwlQE` | 0.30 ebitda | 1.69 | 1.03 | 2.03 | **0.66** | — |
| `P071A1WL` | 0.30 mgeff | 1.51 | 0.96 | 1.01 FAIL | 0.77 | — |
| 槽5 新 PV | continuation/support | max 0.85 | — | — | — | 离开 |

判死：`EUR-MH-LEVERAGE-3LEG-VREV-WEDGE-PROD`。禁止再磨杠杆×v_rev×wedge。`78jdv6b1` 仍待确认。

### 下一波决策（Wave47）— 换 capacq 期限 + 未用慢腿

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | mid_term capacq × v_rev/wedge | `13RKJkg8G4mzbjQ1gHTdZoPb` |
| 2 | short_term capacq × v_rev/wedge | `2DCDnO8pS50Qc8W17MPDjJBo` |
| 3 | time_weighted earnings yield × PV | `2FnI9SgEi4qG91FjGEuehWH` |
| 4 | starhold change/owner 0.30 mix | `2Ijmrw4gx4Fcc59NX0lJW5T` |
| 5 | AIEQ liquidity/clarity 0.30 mix | `3gUjhy5Iz4xwbDWyniUFjQV` |

## 波47（2026-08-24）— 换期限 + yield 慢腿

槽 4 starhold 仍 80%，按 4 槽关账。

| ID | 慢腿 | S | F | 梯子 | RN | prod | 备注 |
|---|---|---|---|---|---|---|---|
| **`Wj7g2gAx`** | 0.30 yield_3 | **1.80** | **1.17** | **2.16** | 1.00 | **0.5463** | Failed RA=0；self vs `78jdv6b1` **0.486**；SUBMITTABLE |
| `RR7rwrm1` | 0.30 yield | 1.80 | 1.17 | 2.15 | 0.99 | — | 与 Wj7 互相关 1.0，勿双提 |
| mid capacq | — | 1.31 | 0.72 | — | — | — | 期限平移稀释 IS |
| short capacq | — | 1.16 | 0.60 | — | — | — | 离开 |
| AIEQ mix | liquidity | 1.42 | 0.85 | — | — | — | 比主导 0.72 有抬升，仍未过闸 |

`Wj7g2gAx` judge READY（RN=1.00 贴线）。近 3 年 2021–23 皆正（2.89 / 1.08 / 2.99）。2017–18 旧年负/平，不拒。**等确认才 submit。** 可与 `78jdv6b1` 同篮（互相关 0.486<0.5）。

### 下一波决策（Wave48）— 未用 MH 慢腿

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | FS strength | `2L6o8sgcW4tebULTzOlngGM` |
| 2 | growth analyst / flow-to-price | `2xGkFv1iG4YIbE4JU0RyGk2` |
| 3 | ROE | `2fhDrd9XC4DFa3ipCstiJSw` |
| 4 | OLL change + income statement | `yKpqOd5n4Xe8T7fDsCey8` |
| 5 | momentum analyst + EV + value | `3GQtwh6FT52QaJfgNy3o0LZ` |

## 波48（2026-08-24）— 未用 MH rank 慢腿 × v_rev/wedge

五槽 40 条 COMPLETE。过廉价闸 5 颗均硬闸/梯子过，**prod 0.81–0.91**。无新 READY。禁止 Mode A。

| ID | 慢腿 | S | F | 梯子 | RN | prod |
|---|---|---|---|---|---|---|
| `lej0ne0e` | value_analyst 0.30 | 1.99 | 1.33 | 2.14 | 0.90 | **0.9101** |
| `Grlo2az5` | growth_flow_to_price_2 0.30 | 1.91 | 1.25 | 2.20 | 0.87 | **0.8136** |
| `gJj3lp50` | income_statement_rank 0.30 | 1.90 | 1.22 | 2.05 | **0.74** | **0.8538** |
| `9qXReZ11` | FS_rank 0.30 | 1.75 | 1.13 | 2.13 | 0.92 | **0.9029** |
| `P071R0vK` | EV_rank 0.30 | 1.75 | 1.08 | 2.10 | 0.81 | null（CLUSTER 1.52 警告） |
| 槽3 ROE | ROE/ROE1 | max 1.47 | 0.93 | — | — | 未过 S/F |
| FS strength | — | max 1.21 | — | — | — | 离开 |
| OLL change | — | max 1.21 | — | — | — | 离开 |

判死：`EUR-MH-GROWTH-FLOW-3LEG-PROD`、`EUR-MH-VALUE-ANALYST-3LEG-PROD`、`EUR-MH-FS-RANK-3LEG-PROD`、`EUR-MH-INCOME-STMT-3LEG-PROD`、`EUR-MH-ROE-3LEG-WEAK`。禁止再磨这些 rank 慢腿 × v_rev/wedge 权重。READY 池仍 `78jdv6b1` + `Wj7g2gAx`。

### 下一波决策（Wave49）— 再换未用 MH 概念

仍 0.30/0.40/0.30 × v_rev/wedge，SUBINDUSTRY/4。禁止再占 FS/growth/ROE/OLL/income/value_analyst/EV/momentum_analyst 槽。

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | price_to_total_assets（long + short α=0） | `1Q2DEL91G4wlbDfAowK3Te9` |
| 2 | street_revision_magnitude FY1（mid/short α=0，非 FY2 invert） | `1EyZm467Y4Ouat0BYwdL6VO` |
| 3 | net_number_revisions_fy1（long/mid α=0） | `1BJi2meEF4lfbdfdTmy25q9` |
| 4 | price_momentum europe_rank | `3Xgq9I2Ms4QUbBSpNKUbrh8` |
| 5 | 弱探针 rational_decay_alpha（long α=0，覆盖 0.75） | `O7BFv5iL5jB9xkg616abgW` |

## 波49（2026-08-24）— 再换未用 MH 概念

五槽 40 条 COMPLETE。**无一过廉价闸**。无新 READY。

| 槽 | max S | F | 备注 |
|---|---|---|---|
| PTA | 1.00 | 0.54 | 离开 |
| street FY1 | 1.27 | 0.73 | 离开 |
| nrev FY1 | **1.54** | 0.97 | 近闸，禁止再磨权重 |
| pmom | 1.28 | 0.78 | 离开 |
| rational_decay | 0.46 | 0.18 | 弱探针离开 |

判死：`EUR-MH-W49-UNUSED-3LEG-WEAK`。READY 池仍 `78jdv6b1` + `Wj7g2gAx`。

### 下一波决策（Wave50）— 换数据集：未用 AIEQ VECTOR

禁止再占 Wave48/49 MH 慢腿。AIEQ 禁止 vol/score/forensic/accrual 主导。0.30 vec_avg 残差 × v_rev/wedge。

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | earnings_quality_score_4/5 | `VCjo2ecD5hyb8UvBXdAnhr` |
| 2 | information_opacity_score_2/3 | `18weLG7xZ4pe9Cg2CLcszAg` |
| 3 | liquidity_buffer / asset_liquidity_score_2 | `2Km1nVcvo4PHb8T1aAesIAgT` |
| 4 | business_model_clarity_score_2/5 | `1l1iG6bnK4Qt8Xr1aw4VKd57` |
| 5 | 弱探针 five_day_industry_relative_return | `1sOjjDsY4myc49195QtqftB` |

## 波50（2026-08-24）— 未用 AIEQ VECTOR

五槽 COMPLETE。**无一过廉价闸**。无新 READY。

| 槽 | max S | F | 备注 |
|---|---|---|---|
| earnings_quality | 0.72 | 0.31 | 离开 |
| opacity | 1.12 | 0.60 | 离开 |
| unused liquidity | **1.31** | 0.74 | 最好仍未过闸 |
| clarity | 0.88 | 0.42 | 离开 |
| five_day | 0.55 | 0.21 | 弱探针离开 |

判死：`EUR-AIEQ-W50-QOC-LIQ-CLARITY-WEAK`。自动续跑，无需 follow-up。

### 下一波决策（Wave51）— AIEQ 护城河/周转 + 1 槽 pspat

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | competitive_advantage_model / indicator | `4D7oHC9oD5bcaC3BZs1Jwnc` |
| 2 | moat_strength_score_4/3 | `kwiT73xp4Nwb1050OlvTpi` |
| 3 | asset_utilization / turnover | `6w8442yp4RXaXA10wPcPxaz` |
| 4 | asset_replacement_cost_factor_2/3 | `8gw9S7w14LdbuWgx1Lru4g` |
| 5 | 弱探针 price_signal_dl volume 0/5 | `1U16c81dc4Mg9OD4XJdmfFg` |
| 6 | AIEQ balance_sheet_trend | `20IbnGe2Q4hicwif7FlrOYp` |
| 7 | pspat trend 3/4 | `29yrLVcLf4IyaCA13hnuuJ6s` |

七槽同提均 **201 接受、无 429**。后续波默认 7 槽。

## 波51（2026-08-24）— AIEQ 护城河/周转 + pspat

7 槽：槽 1 competitive **ERROR**（平台 generic，不当样本）；槽 2–7 COMPLETE 48 条。**无一过廉价闸**。无新 READY。

| 槽 | max S | F | 备注 |
|---|---|---|---|
| competitive | ERROR | — | 禁止原样重提 |
| moat | 0.77 | 0.34 | 离开 |
| utilization | **1.09** | 0.57 | 最好仍未过闸（`Vk7pkbzG`） |
| replacement | 0.78 | 0.34 | 离开 |
| pspat volume | 0.99 | 0.54 | 离开 |
| BS trend | 0.61 | 0.23 | 离开 |
| pspat trend | 1.05 | 0.55 | 离开 |

判死：`EUR-AIEQ-W51-MOAT-UTIL-REPL-PSPAT-WEAK`。READY 池仍 `78jdv6b1` + `Wj7g2gAx`。

### 下一波决策（Wave52）— 未用 AIEQ 利润率/增长/现金流 VECTOR

禁止再占 Wave50 quality/opacity/liq/clarity、Wave51 moat/util/replacement/BS、pspat volume/trend、competitive 原样。other571 / acquisition_model 覆盖 <0.85，不占槽。0.30/0.40/0.30 × v_rev/wedge，7 槽。门禁 56/56 PASS，七槽同提均 201。

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | operating_profit_margin_factor / _2 | `W4qkDh0W54PbzKiBtns7yN` |
| 2 | profit_margin_stability / operating_margin_trend | `1Iq2iRdxk4qrcg915B8LX28e` |
| 3 | earnings_per_share_growth_metric / _2 | `3jimypfEK5cx9pqXuSlx8yH` |
| 4 | revenue_growth_consistency_score / _2 | `33J2xfeCe59e8Em6qIMH5Vc` |
| 5 | cash_conversion_efficiency_score_2 / ocf_stability | `34hlGWdTq4NgbAH1a6FdK5zM` |
| 6 | operating_cashflow_growth_metric_2 / cashflow_trend_analysis_2 | `2Vql8hcWn4PF9NU19ziMgiL` |
| 7 | earnings_growth_rate_analysis / shareholder_equity_growth_rate_2 | `20CH2CH94Z9bRWBbfh3wUD` |

## 波52（2026-08-24）— 未用 AIEQ 利润率/增长/现金流

七槽 56 条 COMPLETE。**无一过廉价闸**。无新 READY。

| 槽 | max S | F | 备注 |
|---|---|---|---|
| operating profit margin | 0.82 | 0.37 | 离开 |
| profit margin stability | 1.17 | 0.63 | 离开 |
| EPS growth | 0.39 | 0.15 | 离开 |
| revenue growth consistency | **1.20** | 0.66 | 最好仍未过闸（`Jj7pqZ6m`） |
| cash conversion | 0.69 | 0.29 | 离开 |
| OCF growth | 0.54 | 0.20 | 离开 |
| earnings growth | 0.96 | 0.47 | 离开 |

判死：`EUR-AIEQ-W52-MARGIN-GROWTH-CASH-WEAK`。READY 池仍 `78jdv6b1` + `Wj7g2gAx`。

### 下一波决策（Wave53）— 未用 AIEQ 杠杆/估值/股东回报/physics

禁止再占 W50 quality/opacity/liq/clarity、W51 moat/util/replacement/BS/pspat、W52 margin/growth/cash、MH ROE rank（Wave48 prod 墙，本波也不用 AIEQ ROE trend）。news36/38 覆盖不足，不占槽。0.30/0.40/0.30 × v_rev/wedge，7 槽。门禁 56/56 PASS，七槽同提均 201。

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | debt_to_equity_ratio_factor / metric_17 | `hzbat1lp4GqbaUuw5r9pSV` |
| 2 | debt_servicing_capacity / debt_coverage | `3O5DGdpr4KCcM01eg3aL1ks` |
| 3 | relative_valuation_comparison / _2 | `2hY1qLgOU4occBP2zAjF0WF` |
| 4 | intrinsic_valuation_estimate / _3 | `2VwxA35hE4shaeOKYoyLyvB` |
| 5 | valuation_model_suite / _2 | `42zCSSbGr4VHbjLTO06q08E` |
| 6 | shareholder_yield_metric_2 / _4 | `1kIGNA6C357VcmVM8w5tt4H` |
| 7 | present_physics_model_2 / company_physics_model_2 | `14V9C6gFK4B0bMnL8oMShzq` |

## 波53（2026-08-24）— AIEQ 杠杆/估值/股东回报/physics

七槽 56 条 COMPLETE。**无一过廉价闸**。无新 READY。

| 槽 | max S | F | 备注 |
|---|---|---|---|
| D/E | 0.79 | 0.38 | 离开 |
| debt servicing | 0.57 | 0.24 | 离开 |
| relative valuation | 0.84 | 0.39 | 离开 |
| intrinsic valuation | 0.44 | 0.14 | 离开 |
| valuation suite | **1.02** | 0.52 | 最好仍未过闸（`omqK5Okk`） |
| shareholder yield | 1.00 | 0.48 | 离开 |
| physics | 0.66 | 0.26 | 离开 |

判死：`EUR-AIEQ-W53-DEBT-VAL-YIELD-PHYS-WEAK`。READY 池仍 `78jdv6b1` + `Wj7g2gAx`。

### 下一波决策（Wave54）— 未用 AIEQ 股息/相关风险/技术估值/均值回复

禁止再占 W50–W53 已测族。starhold / news54 时间戳 / IBES 价格面板不占槽。0.30/0.40/0.30 × v_rev/wedge，7 槽。门禁 56/56 PASS，七槽同提均 201。

| 槽 | 内容 | 批次 ID |
|---|---|---|
| 1 | dividend_policy_analysis / _2 | `1KZjTG5Yk4pb9UiwXGdfKeC` |
| 2 | dividend_consistency / payout_ratio | `3Dgxz5eLo4tFbtZNJ9rnPQ6` |
| 3 | financial_yield_analysis / _2 | `15KkDy2Xz4WfcaDexPbfdc0` |
| 4 | correlation_risk_factor_2 / _3 | `1aaDtt1F34ybahhpnZtrYOU` |
| 5 | ROA consistency / dividend_policy_stability | `3r0puvbvP4Z8azyf8aGSXg1` |
| 6 | short/long technical valuation | `3lukhd9vj5dPaZv1eM1UfvLr` |
| 7 | reversion_score / medium technical valuation | `SnZIRceb4RIa8hY0TiMGUO` |

## 波54（2026-08-24）— AIEQ 股息/相关风险/技术估值/均值回复

七槽 56 条 COMPLETE。**无一过廉价闸**。无新 READY。

| 槽 | max S | F | 备注 |
|---|---|---|---|
| dividend policy | 1.15 | 0.63 | 离开 |
| dividend consistency | 0.32 | 0.10 | 离开 |
| financial yield | **1.18** | 0.65 | 最好仍未过闸（`xAjx0L1J`） |
| correlation risk | 0.87 | 0.40 | 离开 |
| ROA consistency | 0.67 | 0.29 | 离开 |
| technical valuation | 0.59 | 0.25 | 离开 |
| reversion | 0.84 | 0.44 | 离开 |

判死：`EUR-AIEQ-W54-DIV-YIELD-CORR-TVAL-WEAK`。READY 池仍 `78jdv6b1` + `Wj7g2gAx`。

### 下一波决策（Wave55）— 未用 AIEQ 股东待遇/预测离散/资金流/PE

禁止再占 W50–W54 已测族、analyst revision、earnings_quality、vol/score、PEG、model28 credit。0.30/0.40/0.30 × v_rev/wedge，7 槽。

| 槽 | 内容 | 批次 |
|---|---|---|
| 1 | shareholder_treatment_metric / _2 | `4D5DEz3AY4pXayOOtyVAMyl` |
| 2 | forecast_dispersion / forecast_error_magnitude | `4tbFU6eoX5dea4xPkGmxtFs` |
| 3 | forecast_value_accuracy / forecast_accuracy_variance | `45F3FO4f65bqb8x63dcB5SM` |
| 4 | fund_flow_prediction_metric_2 / _4 | `4azj9F8mv4PpaDtQZDCPo22` |
| 5 | pure_alpha_generation_metric_2 / _3 | `8RB3i5JN4h9bwZYKsQ6OUF` |
| 6 | perception_trend / combined_technical_indicators_2 | `1Z9sEaZI4wT9Pa88PBupva` |
| 7 | price_to_earnings_ratio / price_momentum_reversal | `3SqmFXcl94Nwbz0Qp84ZVAr` |

设置：EUR TOP2500 D1 SUBINDUSTRY decay4 truncation 0.08 nan_handling ON max_trade ON。门禁 56/56 PASS，七槽均 201。约 10 分钟后自动收割。

## 波55（2026-08-24）— AIEQ 股东待遇/预测离散/资金流/PE

七槽 56 条 COMPLETE。**无一过廉价闸**。无新 READY。

| 槽 | max S | F | 备注 |
|---|---|---|---|
| shareholder treatment | 0.78 | 0.34 | 离开 |
| forecast dispersion | 0.62 | 0.27 | 离开 |
| forecast accuracy | **1.20** | 0.65 | 最好仍未过闸（`bljL3bal`） |
| fund flow | 0.73 | 0.33 | 离开 |
| pure alpha | 0.67 | 0.27 | 离开 |
| perception / technical | 1.12 | 0.62 | 离开 |
| PE / momentum reversal | 0.75 | 0.32 | 离开 |

判死：`EUR-AIEQ-W55-SHTR-FDISP-FACC-FFLOW-WEAK`。READY 池仍 `78jdv6b1` + `Wj7g2gAx`。

### 下一波决策（Wave56）— 未用 AIEQ 回购/buzz/融资/规模/NLP/不确定性

禁止再占 W50–W55 已测族、physics、credit、technical trend、ROE、impairment、vol/score。0.30/0.40/0.30 × v_rev/wedge，7 槽。

| 槽 | 内容 | 批次 |
|---|---|---|
| 1 | share_buyback_activity_analysis / _2 | `45AwCPc3T4WRbMu13cGn0Zsd` |
| 2 | buzz_intensity_score / _2 | `1qJ9nB6VZ50Pc0xzcl77wiu` |
| 3 | financing_structure_analysis_2 / _4 | `1Kp2aZ8ep4Vjc3t4HIeQTUo` |
| 4 | company_size_factor_2 / _3 | `3iW4unao1573cjZNv39NLGn` |
| 5 | income_statement_trend_metric / _2 | `4B2Z5S7eH4OPcDn7IuTWovd` |
| 6 | nlp_sentiment_alpha_factor_2 / _3 | `1y76EA3eV4AKbz218xofFEul` |
| 7 | medium_term_business_uncertainty / _2 | `1vSzPJ1fu4v5aJ3Kr4S8Brq` |

设置：EUR TOP2500 D1 SUBINDUSTRY decay4 truncation 0.08 nan_handling ON max_trade ON。门禁 56/56 PASS，七槽均 201。约 10 分钟后自动收割。

## 波56（2026-08-24）— AIEQ 回购/buzz/融资/规模/NLP/不确定性

七槽 56 条 COMPLETE。**无一过廉价闸**。无新 READY。

| 槽 | max S | F | 备注 |
|---|---|---|---|
| buyback | 1.05 | 0.53 | 离开 |
| buzz | 0.71 | 0.29 | 离开 |
| financing structure | 0.77 | 0.36 | 离开 |
| size | 0.71 | 0.30 | 离开 |
| income statement trend | 0.82 | 0.41 | 离开 |
| NLP sentiment | 0.56 | 0.25 | 离开 |
| business uncertainty | **1.35** | 0.79 | 最好仍未过闸（`pwj6Q0Yv`） |

判死：`EUR-AIEQ-W56-BUYB-BUZZ-FIN-SIZE-WEAK`。READY 池仍 `78jdv6b1` + `Wj7g2gAx`。

### 下一波决策（Wave57）— 未用 AIEQ 权益资产比/财务趋势/经营波动/账面价值/费用/资本结构

禁止再占 W50–W56 已测族、physics、creditworthiness、technical trend、ROE、impairment、vol/score、FCF、nlp/buzz。0.30/0.40/0.30 × v_rev/wedge，7 槽。

| 槽 | 内容 | 批次 |
|---|---|---|
| 1 | shareholder_equity_to_assets_ratio_metric_2 / _3 | `49vWdd3Rc4AqbCtG68MmhHG` |
| 2 | financial_change_trend_analysis / _2 | `4F50CDdSX4xqbGYq8CuU27K` |
| 3 | operating_income_variability_score_2 / base | `XLtauaga4lHaGWMfl1CTxD` |
| 4 | price_to_book_ratio_metric_2 / base | `VFNV2g6Y59dcrI19CgMOhEn` |
| 5 | operating_expense_ratio_factor / operating_income_score_3 | `1paFnsTk54Ec4Sz8725qZv` |
| 6 | debt_to_capital_ratio_metric_11 / debt_to_enterprise_value | `1gooCK1H45kgcBE18MMudzI` |
| 7 | debt_maturity_profile_score_11 / debt_to_assets | `2t2P1ffaY4rRbnTKYaTsia9` |

设置：EUR TOP2500 D1 SUBINDUSTRY decay4 truncation 0.08 nan_handling ON max_trade ON。门禁 56/56 PASS，七槽均 201。约 10 分钟后自动收割。

## 波57（2026-08-24）— AIEQ leftover 权益资产/趋势/PTB/资本结构

七槽 56 条 COMPLETE。**无一过廉价闸**。无新 READY。最好 Sharpe **0.82**，弱于 W50–W56。**离开 AIEQ leftover 3leg 路径。**

| 槽 | max S | F | 备注 |
|---|---|---|---|
| equity/assets | 0.78 | 0.34 | 离开 |
| financial change trend | **0.82** | 0.41 | 最好（`3ql7Ymoe`） |
| op income variability | 0.65 | 0.27 | 离开 |
| price to book | 0.71 | 0.30 | 离开 |
| opex / op income | 0.50 | 0.18 | 离开 |
| debt/capital | 0.80 | 0.37 | 离开 |
| debt maturity / D/A | 0.65 | 0.26 | 离开 |

判死：`EUR-AIEQ-W57-EQA-FCHG-PTB-DEBT-WEAK`。READY 池仍 `78jdv6b1` + `Wj7g2gAx`。

### 下一波决策（Wave58）— MH 未用分析师成长/动量/预测离散/EBITDA-EV

禁止再占 AIEQ leftover、capacq/yield 已提交骨架、FCF、FS、value_analyst、PTA、leverage、nrev/street/pmom。MATRIX `vec=False`。0.30/0.40/0.30 × v_rev/wedge，7 槽。

| 槽 | 内容 | 批次 |
|---|---|---|
| 1 | long_term_growth_analyst / mid_term_growth_analyst | `LbueE1qc4Ae9dajoJZWC3z` |
| 2 | long_term_momentum_analyst / mid_term_momentum_analyst | `3XUWI245I4nGcf7g77Uskha` |
| 3 | stddev_fy1_eps_estimates_to_price LT / MT | `BBg1M6Fh4yeaHZ48lFLyRX` |
| 4 | ebitda_to_enterprise_value_ratio LT_2 / ST | `2oGrqSfYR4qd96g3q7Dws4U` |
| 5 | enterprise_value_europe_rank / enterprise_value_rank_europe | `QVppH7Lp4yMclAHu9hlpQd` |
| 6 | short_term_momentum_analyst / short_term_growth_rank | `2yYG2xePq4uWbLbJzokey6e` |
| 7 | mid_term_enterprise_value_europe / short_term_enterprise_value_europe | `2uJF3R2xq5cz9i8i7u79jjp` |

设置：EUR TOP2500 D1 SUBINDUSTRY decay4 truncation 0.08 nan_handling ON max_trade ON。MATRIX vec=False。门禁 56/56 PASS，七槽均 201。约 10 分钟后自动收割。

## 波58（2026-08-24）— MH EV/EBITDA/分析师成长动量

七槽 COMPLETE。**6 条过廉价闸**，全部 **RN 0.65–0.82 < 1**，EV rank prod **0.9285**，EBITDA/EV prod **0.8461**。无新 READY。Mode B，禁止磨权重。

| 槽 | max S | 备注 |
|---|---|---|
| growth_analyst | 1.49 | 未过廉价闸 |
| momentum_analyst | 1.53 | 2leg 贴线但梯子 0.51、RA 失败 |
| stddev fy1 | 0.82 | 离开 |
| ebitda/EV | **1.69** | 过廉价闸；RN 0.66 prod 0.85 |
| EV rank | **1.75** | 过廉价闸；RN 0.81 prod 0.93（`P071R0vK`） |
| short mom/growth | 1.18 | 离开 |
| EV europe levels | 1.16 | 离开 |

判死：`EUR-MH-EV-EBITDA-3LEG-RN-PROD`。READY 池仍 `78jdv6b1` + `Wj7g2gAx`。

### 下一波决策（Wave59）— Mode B 换快腿 PV（rising wedge / 对称三角 / continuation）

禁止再占 EV/EBITDA x v_rev/wedge、AIEQ leftover、capacq/yield 克隆。AFT 仅 1 槽弱探针。0.30/0.40/0.30。

| 槽 | 慢腿 | 快腿 | 批次 |
|---|---|---|---|
| 1 | growth_analyst LT/MT | rising_wedge + v_continuation_top | `42wkwTcJd4AM8xUyGtOGXi7` |
| 2 | growth_analyst LT/MT | up/down symmetrical triangle | `1ULNdgc8z4Lganm1f1GdvHlH` |
| 3 | momentum_analyst LT/MT | rising_wedge + v_continuation_top | `21mvS05KF4uNchH5tAZ5evA` |
| 4 | AFT money_flow / CMF | rising_wedge + v_continuation_top | `3bZm4tglp4Np8JIxH1XkVsW` |
| 5 | short_term_growth_rank | up/down symmetrical triangle | `31L0kYbid4vPaSoVlz5o3Oa` |
| 6 | stddev fy1 LT/MT | continuation_falling_wedge + rising_support | `3XyaYbdKa4poaa9Fwf1v6Ix` |
| 7 | growth_analyst LT/MT | continuation_falling_wedge + rising_support | `10RJOZfl656ocojcPKBGvkX` |

设置：EUR TOP2500 D1 SUBINDUSTRY decay4 truncation 0.08 nan_handling ON max_trade ON。门禁语法 56/56、gate 54/54 PASS，七槽均 201。约 10 分钟后自动收割。

## 波59（2026-08-24）— Mode B 换快腿 PV

七槽 COMPLETE。**无一过廉价闸**。新快腿（rising wedge / 三角 / continuation）把同慢腿从 W58 的 S1.49 打到 **0.84**。AFT 整槽为负。**收回 v_rev + falling_wedge。**

| 槽 | max S | 备注 |
|---|---|---|
| growth × rising_wedge | 0.61 | 离开 |
| growth × triangle | **0.84** | 最好（`rKjorxE3`） |
| momentum × rising_wedge | 0.71 | 离开 |
| AFT money_flow | **-0.19** | 整槽为负，离开 AFT×新 PV |
| growth_rank × triangle | 0.49 | 离开 |
| stddev × continuation | -0.32 | 离开 |
| growth × continuation | 0.52 | 离开 |

判死：`EUR-PV-RISING-WEDGE-TRIANGLE-CONT-FAST-WEAK`。READY 池仍 `78jdv6b1` + `Wj7g2gAx`。

### 下一波决策（Wave60）— model193 具名字段 × 收回的 v_rev/wedge

禁止 mdl193_* 低覆盖、CDS 违约主导、EBITDA/EV、杠杆。MATRIX vec=False。0.30/0.40/0.30 × v_rev/wedge。

| 槽 | 内容 |
|---|---|
| 1 | analyst_eps_estimate_dispersion / forecast_revision_count |
| 2 | annual_cashflow_asset_change / cashflow_vs_eps_change |
| 3 | cash_conversion_cycle / cash_burn_rate_ratio |
| 4 | implied_loan_fee / borrowed_to_lendable |
| 5 | industry_relative_5d_return_zscore / quarterly_roe_zscore |
| 6 | earnings_revision_magnitude_3m / earnings_surprise_std_adjusted |
| 7 | current_ratio_liquidity_2 / liquidity_to_current_liabilities |

Wave60 已七槽同提（MATRIX vec=False，0.30/0.40/0.30 × v_rev/wedge）。门禁语法 56/56、gate 56/56 PASS，七槽均 201。

| 槽 | 慢腿 | 快腿 | multisim |
|---|---|---|---|
| 1 | analyst_eps_estimate_dispersion / forecast_revision_count | v_rev + falling_wedge | `4rYR39fy24Tu9281dEoelWKP` |
| 2 | annual_cashflow_asset_change / cashflow_vs_eps_change | v_rev + falling_wedge | `3LkYhr5Sc4kMbmq14WNYh62y` |
| 3 | cash_conversion_cycle / cash_burn_rate_ratio | v_rev + falling_wedge | `14IKoW64P4PjazYjhTrr0f6` |
| 4 | implied_loan_fee / borrowed_to_lendable | v_rev + falling_wedge | `nDugpcvY53a9XDxAF9ATq2` |
| 5 | industry_relative_5d_return_zscore / quarterly_roe_zscore | v_rev + falling_wedge | `2A9cuHgek4Obc64KM059grz` |
| 6 | earnings_revision_magnitude_3m / earnings_surprise_std_adjusted | v_rev + falling_wedge | `3xi8tB5Xh4JCbIjXVWLeADl` |
| 7 | current_ratio_liquidity_2 / liquidity_to_current_liabilities | v_rev + falling_wedge | `Z3HOS3lM4nHaCLvwkojGcm` |

设置：EUR TOP2500 D1 SUBINDUSTRY decay4 truncation 0.08 nan_handling ON max_trade ON。约 10 分钟后自动收割。

## 波60（2026-08-25）— model193 具名字段 × v_rev/wedge

七槽 COMPLETE，**无一过廉价闸**。七槽指标完全相同：max **S1.03 F0.53 TVR 6.4%**。慢腿无分化，信号只剩 PV。离开 `model193` 具名 × win 配方。判死：`EUR-M193-NAMED-SLOW-INERT`。

### 下一波决策（Wave61）— analyst45 交易想法（真 Analyst）

跳过 `analyst_earnings_ibes`（EUR 是 OHLC/回报面板）。`analyst45` VECTOR，cov 1.0，alphaCount ~221。`vec_avg` + 66 日回填 + industry 残差反号 × v_rev/wedge。禁止价格/FX/时间戳/Non-Functional 字段。

| 槽 | 慢腿 |
|---|---|
| 1 | probability / new_value（信念） |
| 2 | jensensalpha / treynor_ratio（风险调整） |
| 3 | net_market_exposure / current_inv（仓位） |
| 4 | days_since_inception / avg_dur（想法年龄） |
| 5 | idea_count / ang_inv（广度） |
| 6 | ad_rel_ret_per / rel_index_ret_per（相对基准） |
| 7 | unreal_ret / real_ret（想法 PnL） |

Wave61 已七槽同提（VECTOR `vec_avg`，0.30/0.40/0.30 × v_rev/wedge）。门禁语法 56/56、gate 56/56 PASS（`--fix`），七槽均 201。

| 槽 | 慢腿 | 快腿 | multisim |
|---|---|---|---|
| 1 | probability / new_value | v_rev + falling_wedge | `4dJR0efNX57G8Yo54ePH7vv` |
| 2 | jensensalpha / treynor_ratio | v_rev + falling_wedge | `3psRxB6mR5iscii1hDir5Nxo` |
| 3 | net_market_exposure / current_inv | v_rev + falling_wedge | `3zutY7ML4ilbysFwqj9CoH` |
| 4 | days_since_inception / avg_dur | v_rev + falling_wedge | `3DenZO77d4ih9mamCTMOxs4` |
| 5 | idea_count / ang_inv | v_rev + falling_wedge | `4BhwqZbQ84L8c5WERIoOtCv` |
| 6 | ad_rel_ret_per / rel_index_ret_per | v_rev + falling_wedge | `3CD7fSccf4NpaodAIQea55z` |
| 7 | unreal_ret / real_ret | v_rev + falling_wedge | `25SfyAvt4Jc9d9fdpdiFw1` |

设置：EUR TOP2500 D1 SUBINDUSTRY decay4 truncation 0.08 nan_handling ON max_trade ON。约 10 分钟后自动收割。

## 波61（2026-08-25）— analyst45 交易想法

七槽 COMPLETE。**无一过廉价闸**。槽有分化（0.37–0.71），不是 W60 那种慢腿失效。最好想法年龄 `78jwwme2` **S0.71 F0.31**。离开 analyst45 × v_rev/wedge。判死：`EUR-ANL45-TRADE-IDEAS-WEAK`。

| 槽 | max S |
|---|---|
| conviction | 0.43 |
| jensen/treynor | 0.43 |
| exposure | 0.39 |
| idea age | **0.71** |
| idea count | 0.64 |
| vs index | 0.37 |
| idea PnL | 0.62 |

### 下一波决策（Wave62）— analyst39 财务比率/EPS（MATRIX）

跳过 IBES 价格面板、analyst45 leftover 价格/FX、拥挤 `rygnhcspe`、杠杆 `qtotd2eq` 主导。0.30/0.40/0.30 × v_rev/wedge，vec=False。

| 槽 | 慢腿 |
|---|---|
| 1 | EPS YoY / TTM 变动 |
| 2 | 年报 vs 季报 EPS（含非常项目） |
| 3 | 剔除非常项目 EPS |
| 4 | 毛利率 |
| 5 | 有形账面/每股账面 |
| 6 | TTM EPS |
| 7 | 上季 EPS 变动 |

Wave62 已七槽同提（MATRIX vec=False，0.30/0.40/0.30 × v_rev/wedge）。门禁语法 56/56、gate 56/56 PASS，七槽均 201。

| 槽 | 慢腿 | 快腿 | multisim |
|---|---|---|---|
| 1 | EPS YoY / TTM 变动 | v_rev + falling_wedge | `3zDbm56MS4CpaDU11sJOAkVU` |
| 2 | 年报 vs 季报 EPS | v_rev + falling_wedge | `c068sgi15008I35s5WIBRk` |
| 3 | 剔除非常项目 EPS | v_rev + falling_wedge | `4nvXQ93Ip4Jfcsf4Z9KERym` |
| 4 | 毛利率 | v_rev + falling_wedge | `1Ys6rvbpI4hPb8oDefU8k55` |
| 5 | 有形账面 / 每股账面 | v_rev + falling_wedge | `1uCI7xgif4iG9Qx136iqNBUx` |
| 6 | TTM EPS | v_rev + falling_wedge | `1WxXAm4dd5dD8QRlw0XRyty` |
| 7 | 上季 EPS 变动 | v_rev + falling_wedge | `12TKdD7Uo4QNbEhsD0qPEAc` |

设置：EUR TOP2500 D1 SUBINDUSTRY decay4 truncation 0.08 nan_handling ON max_trade ON。约 10 分钟后自动收割。

## 波62（2026-08-25）— analyst39 EPS/毛利率/账面

七槽 COMPLETE。**无一过廉价闸**。最好上季 EPS 变动 `6Xlwe9bP` **S0.88 F0.41**；YoY EPS 0.85、毛利率 0.76、账面 0.74。离开该配方。判死：`EUR-ANL39-EPS-GM-BOOK-WEAK`。

### 下一波决策（Wave63）— analyst_consensus 一致预期/surprise

跳过 actuals、低覆盖季报、IBES 价格面板、analyst45 leftover。高覆盖年报 VECTOR surprise/共识 + MATRIX 目标价。`vec_avg` 仅 VECTOR。0.30/0.40/0.30 × v_rev/wedge。

| 槽 | 慢腿 | 快腿 | multisim |
|---|---|---|---|
| 1 | 年报 EPS 共识 / 离散 | v_rev + falling_wedge | `3FA6L9f9H5bK9wE1bHCwPAAX` |
| 2 | 年报 EPS surprise | v_rev + falling_wedge | `2iLSG81mb4CbaNH16irY1rEg` |
| 3 | EPS 估计家数 / 最高估计 | v_rev + falling_wedge | `j7J1MbrX4RU8VBOA0AxUo0` |
| 4 | 营收 surprise | v_rev + falling_wedge | `3yczHrbq57Y9DC1gPeDFMAl` |
| 5 | FCF surprise | v_rev + falling_wedge | `hdfSeaej4w08J812hsWKUDs` |
| 6 | EBIT surprise | v_rev + falling_wedge | `KuLr3974qKcmXxILphz8O` |
| 7 | 目标价共识 / 离散（MATRIX） | v_rev + falling_wedge | `sNS9iem74KP9xUo2KmffYI` |

门禁语法 56/56、gate 56/56 PASS（`--fix`），七槽均 201。约 12 分钟后自动收割。

## 波63（2026-08-25）— analyst_consensus surprise/目标价（最后一轮三腿模板）

七槽 COMPLETE。**无一过廉价闸**。最好 EBIT surprise `Xg7pogXl` **S0.97 F0.48**；营收 surprise 0.95。判死：`EUR-CONSENSUS-SURPRISE-TP-WEAK`。**停止 resid×v_rev×wedge 模板研磨。**

用户已提交 `78jdv6b1` + `Wj7g2gAx` → OS ACTIVE **3**（含 `Wj71Q12o`）。缺口 7。

### 下一波决策（Wave64）— news38 GEM（RA 正轨）

跳过 news84/85（已死）。`news38` VECTOR，未走过 GEM。概念优先 + priors；稀疏新闻强制 densify（`vec_avg`/`ts_backfill`/`trade_when`）。禁止 entitlement/time 元数据。产物入库后再 gate/选波，**禁止手写 resid 模板顶替 GEM**。

## 波64（2026-08-25）— news38 概念化（GEM 402 fallback）

GEM `eur-w64-news38` **402 Insufficient Balance**；改 agent 概念化（纯新闻 densify，**无** resid×PV）。门禁 56/56 PASS，七槽均 201。约 10–12 分钟后自动收割。

| 槽 | 概念 | multisim |
|---|---|---|
| 1 | densified tone invert/windows | `CaBCz7gj4w69SAZ6Olx4bZ` |
| 2 | pos−neg score imbalance | `2DQhXW7zx4Wic5C5ojt5afG` |
| 3 | pos−neg freq imbalance | `4tyMrR5IY4OQ99lxaHqzob` |
| 4 | relevance-gated tone | `iMJ4wbCv55I98skiwCKFD2` |
| 5 | relevance − market heat | `2W2V7h9aE4tx8H0p2EgZ43F` |
| 6 | related_num × inverted tone | `2dQuXt6z84OtcnUTr478K7r` |
| 7 | analytics metric − news score | `4pv6GB7Kw4wNaXcaEKnQ2lJ` |

七槽 COMPLETE。**无一过廉价闸**。最好 densified tone invert `ak7dLe55` **S0.61 F0.20**；heat `RR7pVoZj` S0.53 F0.36。慢腿 |S|<1，禁止混 PV。判死：`EUR-NEWS38-CONCEPT-WEAK`。跳过 news54 时间戳/标题文本。

### 下一波决策（Wave65）— news36 novelty/短语情绪

白名单内剩余 NEWS。机制正交于 news38（novelty + phrase/word/confidence，非 sg_tone）。densify `vec_avg`+`ts_backfill`。禁止 resid×PV。跳过 timestamp/title/`event_effect_magnitude`。

## 波65（2026-08-25）— news36 概念化（GEM 402 fallback）

门禁 56/56 PASS，七槽均 201。

| 槽 | 概念 | multisim |
|---|---|---|
| 1 | densified novelty invert | `1XleQnG54Z0bkAy8rUX6te` |
| 2 | pos−neg phrase imbalance | `1hzxZM3fi4YxaUSkyIjpWKC` |
| 3 | pos−neg word imbalance | `lwS1WfKG591bQo19d50LA8Y` |
| 4 | sentiment confidence imbalance | `XuVbMcZo4kX9Pm1ceTh7eBB` |
| 5 | relevance-gated novelty | `2HyPqRe7k4XWb4iwH2amtKV` |
| 6 | relevance-gated inverted neg phrases | `cT9H1fEr57yboD13XH4LewX` |
| 7 | length-normalized phrase sentiment | `1I2MpT6484hOcx31hIUt8kX4` |

七槽 COMPLETE。**无一过廉价闸**。最好 `rKjodQr9` **S0.60 F0.19**。判死：`EUR-NEWS36-NOVELTY-SENT-WEAK`。NEWS 白名单概念轨耗尽（38/36/84/85；54 时间戳跳过）。

### 下一波决策（Wave66）— model354 估值 VECTOR

离开 NEWS。`model354` group 侧低竞争估值：FY2/NTM 盈利收益率、FCF/CFO/股利收益率、Sales/EV、FY1 vs LTM 分歧。densify `vec_avg`+`ts_backfill`。禁止 resid×PV；禁止 `pt1d1ntr` returns。

## 波66（2026-08-25）— model354 估值概念（GEM 402 fallback）

门禁 56/56 PASS，七槽均 201。

| 槽 | 概念 | multisim |
|---|---|---|
| 1 | FY2 earnings yield invert | `3BM4w98UC4FC8OJn25lCRT5` |
| 2 | NTM earnings yield invert | `5Gk2l4n85dXbK1NHAo2z6h` |
| 3 | trailing FCF yield invert | `2lLizL1y54QF8IyuKI7tHW3` |
| 4 | forward CFO yield | `12Rcec9la4PcaEKgc4H8gM2` |
| 5 | trailing dividend yield invert | `1vPCKk93y5geakvQ11f1rYI` |
| 6 | sales/EV invert | `1y697N6MK4AM8C9tnNa7tZv` |
| 7 | FY1 vs LTM EY disagreement | `cTJ3t4Gn4ze9LEk9oAJzXw` |

七槽 COMPLETE。**无一过廉价闸**。最好 `KP7bgexN` **S0.26 F0.07**；Sales/EV 0.23。多数 TVR 2–4%。判死：`EUR-M354-VALUATION-YIELD-WEAK`。

### 下一波决策（Wave67）— ml_factor_proj 0-alpha 非收益

离开 NEWS / model354。不重复 Wave9 EPS/价格/FCF/应计。覆盖/评级/离散、CCC、异常 capex、ATO、capex/sales。MATRIX，无 resid×PV。

## 波67（2026-08-25）— ml_factor_proj 0-alpha 概念（GEM 402 fallback）

门禁 56/56 PASS，七槽均 201。

| 槽 | 概念 | multisim |
|---|---|---|
| 1 | analyst coverage change | `2nThgEe0B5gm9qdLUf6hdop` |
| 2 | consensus rating change | `lGrWo1Uj5dxbzBsvqT9sLf` |
| 3 | FY2 EPS dispersion change | `NVH5cfn54pOc5r9mIoSYhs` |
| 4 | cash conversion cycle change | `4vrPusNA4QKcHjqLKHF5np` |
| 5 | abnormal capex change | `1Y1nK33wb4oTbjS2ZKJthM4` |
| 6 | asset turnover growth | `W83MY5gM4Qy9J0jTkljgWu` |
| 7 | capex/sales change | `1nwZsf3IR56V9iZWgiy5dAW` |

七槽 COMPLETE。**无一过廉价闸**。最好 abnormal capex `E5lwN5WJ` **S0.70 F0.23**。判死：`EUR-MLFP-0ALPHA-OPS-WEAK`。

### 下一波决策（Wave68）— predictive_starmine 高覆盖未用组件

不重复 Wave21 ARM/RelVal **global rank** / FY1 earnings surprise。改 ARM secondary、RelVal EV/EBITDA 组件、F12M EBITDA surprise、SmartEstimate 增长、隐含 vs 投影 CAGR、warranted PE。cov≥0.85。无 resid×PV。

## 波68（2026-08-25）— predictive_starmine 高覆盖概念（GEM 402 fallback）

门禁 56/56 PASS，七槽均 201。

| 槽 | 概念 | multisim |
|---|---|---|
| 1 | ARM secondary earnings component | `uM8pc74q4Qi8Nf14NiS6j1O` |
| 2 | RelVal EV/EBITDA component | `1ZMCKodzN5fba9MTFyl8Kex` |
| 3 | F12M EBITDA predicted surprise | `itRnW3Cm4IfadP10xapJULx` |
| 4 | SmartEstimate EBITDA growth | `1Rh5wS4XB4Pncze16J2T7oA5` |
| 5 | SmartEstimate earnings growth | `OWTUU19U59D9XW1gJlHV8AX` |
| 6 | implied vs SmartGrowth 5y CAGR | `1pTMVifdM4UeavlHzVgRSDd` |
| 7 | warranted forward PE invert | `4yVXStaFk56W9JUpSvYHFjX` |

七槽 COMPLETE。**无一过廉价闸**。最好 `wpjR2ovp` **S1.09 F0.42 TVR16.5**（RelVal EV/EBITDA ts_delta5）。慢腿 |S|≥1，可混 PV。

### 下一波决策（Wave69）— RelVal×PV win 0.4/0.6

**禁止** 0.30/0.40/0.30 resid 三腿。用 Wave68 原样慢腿 + `v_rev`/`falling_wedge`。跳过 AFT（已有近闸，弱探针=0）。

## 波69（2026-08-25）— RelVal×PV win mix

门禁语法 56/56、gate 去重后 PASS，七槽均 201。

| 槽 | 概念 | multisim |
|---|---|---|
| 1 | RelVal d5 × PV invert 0.4/0.6 | `1Zz7jybL25ixcLjvEJ0xZFz` |
| 2 | RelVal d5 结构变体 | `18sIwUaJi5fJ9sSI84JtcUK` |
| 3 | RelVal d22 × PV | `2vcIDI9gU4OPcgpnORpUiMv` |
| 4 | F12M EBITDA surprise × PV | `3uWqjn3Dw4zdbNT15EDcp0Cd` |
| 5 | CAGR disagreement × PV | `3eEx8QdfB4q58P7ouS5ahM5` |
| 6 | 行业中性 / 权重扫描 | `23aG2x2XM4rX8yu12tUwTH7q` |
| 7 | v_rev vs wedge 拆分 | `4mOm254yW4FM9lWXGUJ3GTx` |

七槽 COMPLETE。最好 `mLj81962` **S1.34 F0.77 TVR9.6%**，prod 0.645 过闸，self 0.64 vs `78jdv6b1`。**2Y=0.02**（裸腿 0.10）梯子墙。判死：`EUR-STAR-RELVAL-EVEBITDA-2Y-DEAD`。禁止再加深 v_rev/wedge。

### 下一波决策（Wave70）— ai_factor_transfer `_2` 未测字段

跳过 Wave18 已测 williams_r/RSI/volume_trend/RTN/BB/PVR。用 anomaly/DPO/liq_2/PVO/ADL/CCI/BPO_2。禁止 return-momentum。无 PV mix。

## 波70（2026-08-25）— ai_factor_transfer `_2` 概念

门禁 56/56 PASS，七槽均 201。七槽 COMPLETE。**无一过廉价闸**。最好 `mLj8QY2X` **S0.58 F0.16**（liq_2）。慢腿 |S|<1 禁止混 PV。判死：`EUR-AFT-OSC2-WEAK`。离开 AFT。

| 槽 | 概念 | multisim | max \|S\| |
|---|---|---|---|
| 1 | volume anomaly vs price | `sVrWccDD4CP9gL13VBm6oCs` | 0.21 |
| 2 | DPO | `4C0pMIfro4Xacf3vpk0PCrW` | 0.51 |
| 3 | liquidity–money-flow _2 | `18d5JmaeW4TWbZkPkZbLSq8` | **0.58** |
| 4 | PVO / BB-2 | `1GP3xHd6U4NbbG93C2cFgui` | 0.43 |
| 5 | ADL trend _2 | `egfWs2OC5k0cbSwoCCdYBA` | 0.56 |
| 6 | CCI | `4aT1uWcq44V88OzJBzHhtFK` | 0.42 |
| 7 | BPO_2 | `3LbmwyahG5hr8ZZ1b050MUd2` | 0.39 |

### 下一波决策（Wave71）— GSM 股票特定事件字段

跳过 Wave20 已测 `trading_days_to_next_event` / analyst_meta / pv_weekly 收益预测。跳过日历常数（iso_week/month/quarter/weekday/month_end/regime 横截面无差异）。用 last/next event confirmation、update、transcript、days-since。无 PV mix。无 return-quantile。

## 波71（2026-08-25）— GSM 股票特定事件概念

门禁 56/56 PASS，七槽均 201。七槽 COMPLETE。**无一过廉价闸**。最好 `GrlwNE33` **S0.68 F0.29 TVR4.9%**（days-since）。慢腿 |S|<1 禁止混 PV。判死：`EUR-GSM-EVENT-WEAK`。离开 GSM（含日历常数与 return-quantile）。

| 槽 | 概念 | multisim | max \|S\| |
|---|---|---|---|
| 1 | last-event confirmation | `1hn96n8xr4qvaTlbXxhn80m` | 0.12 |
| 2 | next-event reschedule/cancel | `10UyTA7hB4i8ccrvAqmZCbc` | 0.54 |
| 3 | last-event update | `1wO0HbbX957i8ZIE31FiEPH` | 0.51 |
| 4 | next-event confirmation | `4t0P782lF5g6c7jZ32RWY0q` | 0.25 |
| 5 | last-event transcript | `FpK1dd4e4Ktc3nOK4Kq2zJ` | 0.28 |
| 6 | days since last event | `1bTliN8mk4oKaoEzQ6IeaKq` | **0.68** |
| 7 | next-event transcript | `37YQ9H9vX4SF8M7oPoIokmu` | 0.39 |

### 下一波决策（Wave72）— starmine 修订广度（非 RelVal）

跳过 RelVal EV/EBITDA、Wave68 ARM secondary / SmartEstimate / CAGR / warranted PE。用 0-alpha upgrade/up/down revision counts + unused ARM recommendations/activity。无 PV mix。pspat trend/volume 已离开，不回 price_signal。

## 波72（2026-08-25）— starmine 修订广度

门禁 56/56 PASS，七槽均 201。七槽 COMPLETE。**无一过廉价闸**。最好 `vRjLXZdA` **S0.97 F0.30 TVR23.9%**（ARM new-activity ts_delta）。慢腿 |S|<1 禁止混 PV。判死：`EUR-STAR-REVCOUNT-ARM-WEAK`。model28 整集是 structural credit，禁止开挖。

| 槽 | 概念 | multisim | max \|S\| |
|---|---|---|---|
| 1 | upgrades 30d | `2bFn2i6Q24u5cEWStExMqsE` | 0.48 |
| 2 | FQ1 EPS upward 14d | `1VhXt86u53DcmEIGFedkEs` | 0.27 |
| 3 | FQ1 EPS downward 14d | `6zR7a9sn4KPbczdFZFwCfC` | 0.35 |
| 4 | FY1 EPS upward 7d | `11CKlEfKU4JD9EHVCZCjG6n` | 0.51 |
| 5 | FQ1 revenue upward 14d | `9QT1G8Lt4PUaNRS86VHldz` | 0.66 |
| 6 | ARM recommendations component | `k53NN5yx5dw93x11HdwmlR4` | 0.20 |
| 7 | ARM new-activity flag | `EaBvL874QQ8CIu6OsksSg` | **0.97** |

### 下一波决策（Wave73）— starmine rec-change + smest 水平

跳过 revision counts / ARM rec-activity / RelVal / smest **growth** / forward PE / P/IV。用 recommendation_mean_change 7/30/90d + SmartEstimate F12M/FY1 **levels** + last-year earnings surprise%。无 PV mix。

## 波73（2026-08-25）— starmine rec-change / smest 水平

门禁 56/56 PASS，七槽均 201。七槽 COMPLETE。**无一过廉价闸**。rec-change 最好 S0.90 但 2021–23 Sharpe ~0.15 塌缩。smest 水平弱。surprise `ak7d0ZKR` **S1.04 F0.40 TVR2.1% 2Y=0.95 RN0.38**（`rank(ts_mean(surprise_pct_last_year_earnings_3, 22))`）— |S|≥1 且 2Y 非年段事故。判死：`EUR-STAR-REC-SMEST-WEAK`。salvage：surprise 作慢腿混未用 PV。

| 槽 | 概念 | multisim | max \|S\| |
|---|---|---|---|
| 1 | rec mean change 7d | `3VDVM83cC4Bmc98HGNtGlnI` | 0.66 |
| 2 | rec mean change 30d | `4zS3RASE51Tb8J13Aj42wDn` | 0.80 |
| 3 | rec mean change 90d | `4p8lOQ8704ySagRf5lgd6MJ` | 0.90 |
| 4 | smest F12M earnings | `3ikEkGeT24YmbtBxYINunPT` | 0.39 |
| 5 | smest F12M revenue | `3QQt1Dd244rf9elcpccfqN8` | 0.21 |
| 6 | smest FY1 earnings | `29jRNY6bb4ND9DBgCGeE9ly` | 0.76 |
| 7 | last-year EPS surprise % | `4lgynh2f74xNbwJka2SbsBL` | **1.04** |

### 下一波决策（Wave74）— surprise×未用 PV win 0.4/0.6

**禁止** v_rev / falling_wedge / breakaway / rising_wedge / 对称三角 / continuation。用 common_gap 与 desc_triangle。慢腿冻结 `rank(ts_mean(surprise_pct_last_year_earnings_3, 22))`。无 0.30/0.40/0.30 三腿。

## 波74（2026-08-25）— surprise×未用 PV win mix

门禁语法 56/56、gate 54/54 PASS，七槽均 201 COMPLETE。**近闸** `zqk9VQ6X`：surprise22 × common_gap_up ts_delta5，**S1.67 F0.94 TVR11.3% 2Y=2.08 SUB1.28 RN0.60 prod0.63 self0.16**。LOW_FITNESS 仅 warning；逐年全正。其余槽弱（desc_triangle 最好 S0.98）。**不要判死**该 mix。禁止换成 v_rev/wedge。

| 槽 | 概念 | multisim | max \|S\| |
|---|---|---|---|
| 1 | surprise × common_gap up | `2jMJXQ48v4Tmcmy1fBkaU6bA` | **1.67** |
| 2 | surprise × common_gap down | `2lLY6p1YA4MPblC36BOJ5fP` | 0.67 |
| 3 | surprise × desc triangle | `3FByexfot5bVbe3169ECBTbv` | 0.80 |
| 4 | surprise × downward price gap | `1STvPr9ek5dJ9H2JJsZbery` | 0.51 |
| 5 | surprise × desc triangle upward | `2vMEEE3Qz4QCaQObQ7ck8M9` | 0.71 |
| 6 | surprise × desc triangle 60 | `2vA3sK7hA4yj9U5L9dWtEH9` | 0.98 |
| 7 | surprise × gap+triangle 0.5/0.5 | `f5gMz4hk4TdceDBLaFbLaJ` | 0.63 |

### 下一波决策（Wave75）— Mode A 冻字段提 F/RN

冻结 `surprise_pct_last_year_earnings_3` × `common_gap_up_mean_simscore_lookback120`。变 ts_delta 3/10/22、slow 10/44、权重 0.35/0.45、industry group_neutralize；七槽扫 decay 2/4/6/8、INDUSTRY/SECTOR、truncation 0.05。禁止 Mode A 破 prod（prod 已过）。禁止换成 v_rev/wedge。

## 波75（2026-08-25）— Mode A surprise×common_gap_up

门禁 8/8 PASS，七槽 COMPLETE。F 已过闸，**RN 仍 <1**。胜出表达式 ts_delta **10**。平台 `checks.fail=[]`。SECTOR `j2jZqgbj` RN0.79 但 **prod 0.74 禁提**。INDUSTRY `mLj8EXp9` S1.86 F1.13 prod **0.6993 贴墙** 不提。安全近闸 `gJj1nxLM` SUB d4 S1.81 F1.04 RN0.66 prod0.67 self0.15，逐年全正。CONDITIONAL：若忽略战役 RN>1，平台硬闸已过。禁止再粗中性化。

| 槽 | 设置 | multisim | 最佳 |
|---|---|---|---|
| 1 | SUB decay4 | `29DA8a1GM4qOcAR2tEQYuhv` | `gJj1nxLM` S1.81 F1.04 RN0.66 |
| 2 | decay 2 | `4DfUQvbls4kGbR7qFVJwUiu` | `xAjxJR2l` S1.81 F1.05 RN0.64 |
| 3 | decay 6 | `3KpdLd2bp52ybf2G98KPwvo` | F≥1 多条，RN~0.7 |
| 4 | decay 8 | `W7SGIaz34IWbJ9pZ6OrDa1` | `1Yw7rJ8R` S1.82 F1.05 RN0.71 |
| 5 | INDUSTRY | `2CvZupa8X4CIalyn8UxJ3TH` | `mLj8EXp9` S1.86 F1.13 RN0.73 prod0.699 |
| 6 | SECTOR | `yjg42f7Y4D99jI1aaIxklr9` | `j2jZqgbj` RN0.79 **prod0.74** |
| 7 | trunc 0.05 | `1GXdC23X44xT8RsU7Yxpsro` | 与槽1同构 |

### 下一波决策（Wave76）— 因子中性化冲 RN

冻结 ts_delta10 0.4/0.6。七槽：STATISTICAL / CROWDING / FAST / SLOW / SLOW_AND_FAST / REVERSION_AND_MOMENTUM / STAT decay8。禁止 MARKET/COUNTRY/SECTOR 设置（prod 墙）。失败则 Mode B 换未用 PV 快腿（asc_triangle 等），勿再 Mode A 磨同一 mix。

## 波76（2026-08-25）— 因子中性化冲 RN

门禁 8/8 PASS，七槽 COMPLETE。**无一过廉价闸 F≥1**。FAST `E5lEZx2K` 最好 S1.79 F0.92 2Y=1.54 **梯子失败**。STAT/CROWDING/SLOW/RAM/SAF 相对 SUB 掉 F。判死 `EUR-STAR-GAP-FACTOR-NEUT-WEAK`。禁止再 Mode A 磨 common_gap_up mix。CONDITIONAL 父代 `gJj1nxLM` 仍有效（S1.81 F1.04 RN0.66 prod0.67）。

| 槽 | 设置 | multisim | max \|S\| |
|---|---|---|---|
| 1 | STATISTICAL d4 | `1IJyNI3k94Anbchqz4i2nJs` | 1.39 |
| 2 | CROWDING d4 | `45F2hecd25kc9j2S1ZFzDNj` | 1.59 |
| 3 | FAST d4 | `4rJHU63i84Gjbs9YwLrPJDC` | **1.79** |
| 4 | SLOW d4 | `175djq6t5i5cx31dBqgYrbV` | 1.08 |
| 5 | SLOW_AND_FAST d4 | `31Ql866ig4x9aiHpiF8TE8M` | 0.87 |
| 6 | REVERSION_AND_MOMENTUM d4 | `1ePTdu9j45jZb0n15R6QBrf6` | 1.02 |
| 7 | STATISTICAL d8 | `3uNFjueXC4Mc9nibHIzSVyD` | 1.29 |

### 下一波决策（Wave77）— Mode B 未用 PV 快腿

冻结 surprise 22d 慢腿。换：asc_triangle / 支撑阻力 / 趋势线收敛发散 / regular gap。禁止 v_rev/wedge/breakaway/symm/continuation/common_gap/desc_triangle。设置跟 win：SUB decay4。

## 波77（2026-08-25）— Mode B surprise×未用 PV

门禁 56/56 PASS，七槽 COMPLETE。**无一过廉价闸**。最好 `Vk7Pkm30` asc_triangle_down S1.46 F0.75。支撑阻力/趋势线/regular gap 均 <0.81。判死 `EUR-STAR-PV-ASCT-TREND-WEAK`。CONDITIONAL 父代 `gJj1nxLM` 仍有效。禁止再 Mode A common_gap_up、禁止因子中性化。

| 槽 | 概念 | multisim | max \|S\| |
|---|---|---|---|
| 1 | asc_triangle | `3yycahdlG4mqbCIIrd2k6BZ` | 1.10 |
| 2 | asc_triangle down | `2RSOHr4Kw4h6bXA13RwHCDf2` | **1.46** |
| 3 | falling support / flat resistance | `2fokg999j4vQa4X1bRB2ZNXk` | 0.74 |
| 4 | rising support / flat resistance | `3BacbndBk5i79dCKBIkqQs0` | 0.51 |
| 5 | trendline divergence | `6ZwMqfM74It8xMvhP8leMT` | 0.71 |
| 6 | trendline convergence | `1SZX4BbCU56Hcne1bnbmXHEO` | 0.81 |
| 7 | regular downward gap | `2SvRSodYJ4uFa7A9F9W7Pkz` | 0.56 |

### 下一波决策（Wave78）— 换未用 starmine 慢腿

冻结快腿 `rank(ts_delta(common_gap_up_mean_simscore_lookback120, 10))`。慢腿：upgrade/downgrade count、actual last-year/quarter earnings、ARM country rank、last-year revenue。跳过 RelVal/P/IV/revision counts/smest/surprise。SUB decay4。

## 波78（2026-08-25）— 未用 starmine 慢腿 × 已验证 PV

门禁 56/56 PASS，七槽 COMPLETE。**无一过廉价闸**。最好 `Xg7nmZ90` last-year EPS S1.56 F0.85。新慢腿稀释 surprise×gap。判死 `EUR-STAR-ACTUAL-UPGDNG-ARMCOUNTRY-WEAK`。CONDITIONAL `gJj1nxLM` 仍有效。禁止 Mode A common_gap_up / 因子中性化 / W77 PV / 这批 actual/upgrade 慢腿。

| 槽 | 慢腿 | multisim | max \|S\| |
|---|---|---|---|
| 1 | upgrade 30d | `19Nvrlglk4GAbDuz7fGfqPx` | 1.41 |
| 2 | downgrade 30d | `b7a2lbkg4ne8L5XRaKrdFN` | 1.46 |
| 3 | actual last-year EPS | `2Iuglh7y55cFbG63XfD7aHN` | **1.56** |
| 4 | actual last-quarter EPS | `2BLODx9aZ4su9m1XR1xVmNO` | 1.40 |
| 5 | ARM country rank | `pQzKR5yb4gybCXMYf5pZVs` | 1.40 |
| 6 | actual last-year revenue | `dMJPG2vZ4t6bEIplBoudkF` | 1.48 |
| 7 | upgrade 7d | `2AK3Yr6NW4OFbHn1cu3ZD7ft` | 1.47 |

### 下一波决策（Wave79）— ARM 组件 + surprise×regular_upward_gap

跳过 rec-activity / country rank / revision。用 preferred earnings、revenue component、score change 7d/30d、region/global rank。第 7 槽 surprise × regular_upward_gap_mean。SUB decay4。

## 波79（2026-08-25）— ARM 组件 + surprise×regular_upward_gap

门禁 56/56 PASS，七槽 COMPLETE。**无一过廉价闸**。最好 ARM score change 30d `d5j0pJpx` S1.55 F0.78。regular_upward_gap 仅 S1.04。判死 `EUR-STAR-ARM-LEFTOVER-WEAK`。starmine 换腿已穷尽。CONDITIONAL `gJj1nxLM` 仍有效。禁止 Mode A common_gap_up / 因子中性化 / W77–W79 已死路径。

| 槽 | 概念 | multisim | max \|S\| |
|---|---|---|---|
| 1 | ARM preferred earnings | `4nC43C2t754Gaja3yjiQVRZ` | 1.35 |
| 2 | ARM revenue | `1hFPIt7dq4VT8AAgJOx2rFl` | 1.34 |
| 3 | ARM score change 7d | `IG1rs7h4Ir9kdxE5OvaJF` | 1.48 |
| 4 | ARM score change 30d | `3NVXbhg964RZa9G12u5o8g12` | **1.55** |
| 5 | ARM region rank | `1Nga0Qchf59Fcfj1fgeOJYFU` | 1.44 |
| 6 | ARM global rank | `3cOnw5c8k5fybgi14JRtg846` | 1.42 |
| 7 | surprise × regular_upward_gap | `2KlGhwaex4Ud9I2IdrDeVMj` | 1.04 |

### 下一波决策（Wave80）— 离开 starmine，换 MH 未用慢腿

冻结快腿 common_gap_up ts_delta10。慢腿：balance sheet / deep value / mgmt efficiency·leverage / PEG / rational decay / sales-to-price。跳过已用 capacq/yield/FS/ROE/OLL/momentum。SUB decay4。

## 波80（2026-08-25）— 未用 MH 慢腿 × common_gap_up

门禁 56/56 PASS，七槽 COMPLETE。**PARTIAL**：invert 慢腿过廉价闸，RN 墙。最好 `3qlRb8xg` invert mgmt leverage S **1.68** F **1.00** TVR 8.8% 2Y **2.56** SUB 1.22 RN **0.41** prod **0.592** self 0.15。deep value invert `j2j0R5Zo` S1.61 F1.0 **prod 0.712 禁提**。RN 劣于 CONDITIONAL `gJj1nxLM`（0.66）。禁止 Mode A leverage / deep_value；禁止因子中性化 / SECTOR/INDUSTRY。

| 槽 | 慢腿 | multisim | max \|S\| |
|---|---|---|---|
| 1 | balance sheet | `2EBqbzdeG4qi9GW14rKuQBD5` | 0.74 |
| 2 | deep value invert | `2dgluXeok4XLbx41eiPcayT3` | **1.61** prod墙 |
| 3 | mgmt efficiency | `1tVPOAez14KYaKY18KJHXJk6` | 1.55 |
| 4 | mgmt leverage invert | `20Qplmd9m53fa26Ndf9ihQh` | **1.68** RN0.41 |
| 5 | inverse PEG | `1MNUgebzY56p98vhgZFUcsM` | 1.17 |
| 6 | rational decay | `4qgmyC6gT4qEbtfYA9ymGlD` | 0.93 |
| 7 | sales to price | `2HlpEGHP4X49vsOQXfENYF` | 1.03 |

### 下一波决策（Wave81）— invert 其他未用 MH

冻结快腿 `rank(ts_delta(common_gap_up_mean_simscore_lookback120, 10))`。慢腿 invert：IS rank / EV / trailing FCF-to-price / value analyst / NOA / P/TA / value momentum。跳过 leverage / deep_value / BS / PEG / rational decay / sales-to-price。SUB decay4。

## 波81（2026-08-25）— invert 未用 MH × common_gap_up

门禁 56/56 PASS，七槽 COMPLETE。**PARTIAL**。FCF invert 过廉价闸+梯子+2Y，但 **prod 墙禁提**。EV invert 过 prod，RN 仍墙。

最好禁提：`6Xl9vj9O` invert trailing FCF-to-price（裸 rank）S **2.15** F **1.46** TVR 8.9% 2Y **2.36** SUB 1.48 RN **0.67** **prod 0.734** self vs `Wj71Q12o` 0.36。逐年全正（2017=0.70 最弱）。同族 `E5lEXpwL` prod **0.731**。与 `3qlRb8xg` 互相关 **0.85**。

次优 CONDITIONAL：`MP7Qo0gM` invert EV ts_delta5 S **1.72** F **1.04** TVR 11.5% 2Y **2.29** SUB 1.38 RN **0.55** prod **0.596** self 0.22。RN 劣于 `gJj1nxLM`（0.66）。逐年全正（2017=0.69、2014=0.82）。

禁止 Mode A FCF invert 破 prod；禁止 Mode A EV/leverage 破 RN；禁止因子中性化。`gJj1nxLM` 仍是最佳可提交方向 CONDITIONAL。

| 槽 | 慢腿 | multisim | max \|S\| |
|---|---|---|---|
| 1 | IS rank invert | `3PWiNx6w44SRaGVfyxGPRiP` | 1.32 |
| 2 | EV invert | `3MNVkZfI14Ul98RP1BrVC7M` | **1.72** RN0.55 prod0.60 |
| 3 | trailing FCF invert | `3REphrgOD4QW9HNsZI27kfd` | **2.15** prod墙 |
| 4 | value analyst invert | `2yrBIB2Y84RjaJhIzx0IWlX` | 1.28 |
| 5 | NOA invert | `3JNUZ9fiI4Lrapx24EvQRpj` | 1.03 |
| 6 | P/TA invert | `1fnSpQ7rN4w2cCYVxQbczg8` | 1.53 |
| 7 | value momentum invert | `1Ej2Pid2U4JXcuzitePoILi` | 1.14 |

### 下一波决策（Wave82）— invert 未用 MH 修订/成长（离开价值/FCF）

冻结快腿 `rank(ts_delta(common_gap_up_mean_simscore_lookback120, 10))`。慢腿 invert：growth analyst / ΔEPS / net revisions / street revision mag / FY2 3m revision / FY1 EPS stddev-to-price / trailing growth-flow-to-price。跳过 FCF/EV/leverage/deep_value/yield/FS/ROE/OLL/momentum/capacq 及 alias。SUB decay4。

## 波82（2026-08-25）— invert 未用 MH 修订/成长 × common_gap_up 在飞

门禁语法 56/56、gate 56/56 PASS。七槽均 201。约 12 分钟后自动收割。

| 槽 | 慢腿 | multisim |
|---|---|---|
| 1 | growth analyst invert | `2NQKWR9dh4jxcj6MGeq8LXr` |
| 2 | Δ price-adj EPS invert | `2ifZS26RJ50xcfDIBK2R1p3` |
| 3 | net FY1 revisions invert | `3Hw7w191J4wf8Pn1fm3I0EuI` |
| 4 | street revision magnitude invert | `1027Oga84Z7cbynaFaXVri` |
| 5 | FY2 3m revision invert | `4oMJ9g5Yd56h94013Ns6Dc51` |
| 6 | FY1 EPS stddev-to-price invert | `7Yihx5uJ4tqaWxBXXPhSfY` |
| 7 | trailing growth-flow-to-price invert | `4iCjxoe0B4Vqc7F8cuIz6SM` |


