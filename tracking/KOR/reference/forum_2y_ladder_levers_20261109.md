# 论坛取证：LOW_SHARPE / LOW_2Y_SHARPE / IS_LADDER 破法（2026-11-09 KOR W14 前置调研）

来源：中文论坛三帖（均 Advisory 区实测帖+评论区一手数据点）
- 帖 41262095695127「几个提高LOW_SHARPE和LOW_2Y_SHARPE的方法」(LC69991)
- 帖 39050410166807「关于IS ladder sharpe优化的一点实践经验」(LH63566)
- 帖 42187744015767「使用rank_by_side改善2year_sharpe/ladder_sharpe」+ 30 评论实测

## 可用的杠杆（已对账 known_ops/幽灵账本）
1. **signed_power(x, 0.5) 外层幂压缩**：S 在 1.5~1.55 的近线件「轻松过」；0.5 最稳，0.7 弱信号会压过头（评论 QQ68782）。适合 mLoGN5Mx(1.53)。
2. **外层 group_neutralize(x, industry)**：GLB 一手 1v1 对照（评论，同内核单变量）：2Y 1.15→2.04、S +29%、margin 仅 −5%。本族最强 2Y 杠杆，**未试过**。
3. **truncation 0.08→0.05**：2Y 差 0.1~0.2 时配合尾部压缩用（评论 QQ68782）。
4. **中性化 RAM/CROWDING 系**：同内核只换 setting——STATISTICAL/FAST/SLOW 的 2Y 全崩，RAM/CROWDING 一次过（评论 6，GLB 高换手线）。与本战役 W13 实测一致（STAT 崩）。**CROWDING 对 KOR 本族未试**。
5. **慢化子腿抬 2Y**：拉长回看窗口是「目前唯一让 2Y 单独改善的变量」；TO 地板 0.125 以下慢化对 fitness 无增益。
6. power(ts_rank(alpha))：IS ladder 提升但对基本面集有效、news 集反例（改走 STAT+group_zscore）——本族暂不用。
7. 阶梯 decay（按换手给 decay）：本族 TO~0.09 低档，暂不动。

## 不可用（幽灵/未解锁）
- **rank_by_side：inaccessible**（operator_availability_ledger 实登；论坛作者称赛季解锁件）——禁用，连坐整批。

## 风险与边界
- rank_by_side/GN 类「润色」杠杆会啃 margin：贴 floor 的候选慎上（本族 margin 未卡线，可用）。
- signed_power 前提=长尾分布；近对称信号上纯亏 margin。
- 所有杠杆须单变量对照（一臂只动一个杠杆），否则归因失效。

## 应用（W14 设计）
- W14_EXPR（RAM/d4/trunc0.08）：杠杆{GN-industry, signed_power0.5} × 基座{126/Δ22, 300/Δ66, 150/Δ22} 6 臂
- W14_SET（CROWDING/d4/trunc0.08）：两基座裸式，setting 单变量
- W14_TR（RAM/d4/trunc0.05）：两基座裸式，trunc 单变量（排队）


## 第二轮取证（21:40，四帖全文）
- **帖 43583615602711【结构认知】全周期/2Y 强对冲（23 赞）**：S↔2Y 跷跷板是结构不是参数；正确用法=**双车道分流**（一车道全周期最优、一车道专配 2Y），**两车道找不到交集 ⇒ 历史型信号早归档**；「全车道闭合且 2Y 结构性不达标→整理证据链上报裁决，不换批继续磨」。⇒ W14 属「外层杠杆轴」补轴（非全车道闭合），若 W14 全灭则车道闭合成立、§28 终判顶。
- **帖 44349557269655【踩坑复盘】修 2Y 五反直觉**：换宇宙/换 STATISTICAL 修 2Y 越改越差（EUR 实例 2Y 1.37→0.07/0.78/0.97 全劣化）——与 W13 崩盘互证；方向=抬信号本身近年活性，不是套 setting。
- **帖 43644505975959【Alpha Idea】分析师预期修正「水平×交叉指标动量」**（一次打通 Sharpe 与 2Y）：核心发现=**水平与动量必须用不同指标交叉**（同源则信息高度相关 2Y 提升有限；「水平用指标 A、动量用指标 B」后 2Y 明显跳升）。⇒ anl10 白空间探针（W15 候选）：sal 水平 × net 动量 / net 水平 × sal 动量 交叉构型 + rsk68 门控。
- **帖 38979392093591【10 个救法】**：与第一轮杠杆清单一致（signed_power/decay 阶梯/trunc 微降），无新增硬杠杆。

## W15 预铺（若 W14 命中或需要第 8 颗备份）
- 探针=anl10 交叉构型（水平A×动量B，同数据集 ATOM 几何，单式≤12 算子）×2 + E56 基座 GN-industry 壳 ×1 + 弱臂对照 ×1；发波前查「组合类型配额+塔点亮表」。
