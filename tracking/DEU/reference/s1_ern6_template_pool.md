# ern6（earnings6）SUE/PEAD 模板池 —— DEU/TOP500/D1 —— 2026-11-03

## 机制与取证
- 机制：SUE（标准化意外盈余）+ PEAD（盈余公告后漂移）——Ball & Brown 1968 / Bernard & Thomas 1989：正意外→公告后持续正收益。
- 论文：SSRN 3577132《Valuation ratios, surprises, uncertainty or sentiment: How does financial ML predict returns from earnings announcements》（论坛主帖引用源）。
- 论坛 29158873481111（QQ68782，35 赞）：cap 分组中性化 + 60 天漂移窗 + 成长股加权增强；star_* 字段无权限，本池用 ern6 自算 SUE 替代。
- 论坛评论（AS53518）：小盘股对意外反应更猛（市值交互）；乘 ts_rank(预期偏差) 权重增强。
- 修正动量文献：分析师预期上修 → 持续正收益（Earnings Revision Momentum）。

## 字段真身（2026-11-03 平台实查，18 字段全 VECTOR，数值位须 vec_avg）
A=vec_avg(ern6_actual_eps) / E=vec_avg(ern6_estimated_eps) / U=vec_avg(preliminary_eps_range_upper_bound) / L=vec_avg(preliminary_eps_range_lower_bound) / DIV=vec_avg(ern6_x_dividend) / C=vec_avg(ern6_conferencecalltime)（事件时间）/ next_ed 等日历族。
SUE = divide(subtract(A, E), add(abs(E), multiply(0.01, abs(E))))  ← 量纲安全除零保护（禁裸常数）
REV = divide(subtract(E, ts_delay(E, 252)), add(abs(ts_delay(E, 252)), multiply(0.01, abs(ts_delay(E, 252)))))  ← 修正动量（YoY 位移）

## 12 互异模板（结构轴：截面 / cap 分组 / 漂移窗 / 市值交互 / 不确定性折扣 / 修正动量 / 事件门控 / 意外持续 / 秩尾放大 / 分红变化 / 双维确认 / 论坛完整复刻）
| # | 骨架 | 机制 | 来源 |
|---|---|---|---|
| M1 | group_rank(SUE, subindustry) | SUE 截面基线 | Ball-Brown / PR1 在飞 |
| M2 | group_neutralize(SUE, bucket(rank(cap), range="0,1,0.5")) | 市值桶内意外中性化 | 论坛主模板 / PR2 在飞 |
| M3 | group_rank(ts_mean(SUE, 66), subindustry) | PEAD 漂移窗（论坛 60→白名单 66） | 论坛 |
| M4 | multiply(group_rank(SUE, subindustry), subtract(1, ts_rank(cap, 252))) | 小盘反应更猛（市值交互） | 论坛评论 |
| M5 | multiply(group_rank(SUE, subindustry), subtract(1, group_rank(W, subindustry)))，W=divide(subtract(U,L), add(abs(E), multiply(0.01, abs(E)))) | 初值区间宽=不确定→意外打折 | SSRN 3577132 uncertainty 维度 |
| M6 | group_rank(REV, subindustry) | 分析师修正动量 | Revision Momentum 文献 |
| M7 | trade_when(not_equal(SUE, ts_delay(SUE, 1)), group_rank(SUE, subindustry), 0) | 新意外事件日稀疏入场（降 TO 避 CW） | 自建（esm 事件型实证） |
| M8 | group_rank(multiply(SUE, ts_delay(SUE, 252)), subindustry) | 意外持续性（同号=PEAD 增强） | Bernard-Thomas |
| M9 | group_neutralize(signed_power(subtract(group_rank(SUE, subindustry), 0.5), 3), subindustry) | 秩尾放大壳（有界秩输入） | memory 实证 |
| M10 | group_rank(divide(subtract(DIV, ts_delay(DIV, 252)), add(abs(ts_delay(DIV, 252)), multiply(0.01, abs(ts_delay(DIV, 252))))), subindustry) | 分红同比变化（股利信号） | 自建 |
| M11 | multiply(group_rank(SUE, subindustry), group_rank(REV, subindustry)) | 意外×修正双维确认（交互乘，非双腿加） | 论坛评论（乘预期偏差权重） |
| M12 | group_neutralize(ts_mean(group_rank(SUE, bucket(rank(cap), range="0,1,0.1")), 66), bucket(rank(cap), range="0.1,1,0.1")) | 论坛完整复刻（漂移+双层 cap 桶） | 论坛增强版 |

方向先验：SUE/REV/分红增加 → 做多（PEAD/修正动量/股利信号先验）。
窗口：252/66/1 全白名单；60 天漂移按论坛实测折算 66（差异 <10%，如需复刻 60 须单独解释）。
合规自查：SUE/REV=同机制净额或单字段位移✓；M4/M5/M8/M11=乘法交互非 add/subtract 双腿✓；cap 只作分组轴不计腿✓；除零保护量纲安全✓；无 GROUP 入数值算子✓。

## 启动条件（探针闸）
PR1（裸截面,3gsTbgD5）/ PR2（cap 分组,JcXbW2ue）在飞。**S≥0.5 量级才发正式波**；同时查 get_alpha_yearly_stats 逐年覆盖（判据=连续多年空窗；ern6 台账 2012 起，须验 EPS 实值/预期族逐年 longCount）。
两道预检（preflight_expressions + verify_expr）发波前必跑。
## 探针闸结果（2026-11-03 01:10）—— **不启动正式波**
| 探针 | alpha | S | 2Y | fRA | 判定 |
|---|---|---|---|---|---|
| PR1 SUE 裸截面 | WjOVkv5Q | 0.40 | 0.13 | 5 | S<0.5 侦察线 |
| PR2 cap 分组（论坛主模板） | 9qx7onXr | 0.26 | −0.35 | 5 | 更弱 |

**逐年覆盖（get_alpha_yearly_stats）**：2014-2018 **五年全空**（longCount=0/pnl=0），2019 起才有 pnl。EPS 实值/预期族=起始晚型 5 年空窗（台账「2012 起」指日历族，EPS 族不跟）。

**终判**：SUE 机制在 DEU/TOP500 双杀（幅度 + 覆盖），ern6 开矿终止，模板池留档备查（若 leading-gap 裁定松动且后续发现全覆盖子族再议）。

