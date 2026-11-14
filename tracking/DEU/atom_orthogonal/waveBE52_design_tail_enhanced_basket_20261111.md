# BE52 预设计：tail 增强版待授权篮子（替换升级路径，2026-11-11）

> 触发条件：BE51/BE50 证实 tail 对事件型腿有效。
> 性质：**替换**而非新增——tail 版与原版同机制、未提交件不进 self 池，但篮子内只能取一。

## 一、5 颗待授权件的事件型腿盘点（用平台原始表达式核实）

| alpha | 腿 1 | 腿 1 数据集覆盖 | 腿 2 | 腿 2 覆盖 | 受污染 |
|---|---|---|---|---|---|
| qM7KxkQV | shrt3_bar Δ220 | shortinterest3 0.71-0.78 | insd1_holdings rank252 | insiders1 0.534 | **两腿** |
| 9qlz29Oe | max_loan_rate_p5_d1 Δ220 | shortinterest3 0.783 | nws20 情绪 Δ66+mean11 | news20 0.919 | 腿 1 |
| d5a2vxzY | max_loan_rate_p5_d1 Δ220 | 0.783 | mean_loan_rate_p5_d1 Δ132 | 0.783 | **两腿** |
| Jj8VQwoe | shrt3_bar Δ220 | 0.71-0.78 | oth47_organic_traffic ts_quantile | other47 0.577 | **两腿** |
| RREPm361 | est_12m_ebi_median zscore240 | analyst MATRIX | est_12m_ebt_mean 变化 | analyst MATRIX | 不受影响 |
| 78Yk8VR1（已 ACTIVE） | shrt3_bar tvr_decay | 0.71-0.78 | — | — | 已提交，tail 版会撞 self，不做 |

## 二、8 臂设计（全部 ≤12 算子，表达式从平台原始 code 逐字复制后加 tail 包裹）

1. qM7KxkQV + tail(I7 腿, lower=0.25)
2. qM7KxkQV + tail(I7 腿, lower=0.35)
3. qM7KxkQV + tail(shrt3 腿, lower=0.25)
4. 9qlz29Oe + tail(nws20 腿, lower=0.25)
5. d5a2vxzY + tail(两腿, lower=0.25) —— 算子 12
6. Jj8VQwoe + tail(oth47 腿, lower=0.25)
7. Jj8VQwoe + tail(shrt3 腿, lower=0.25)
8. 9qlz29Oe + tail(nws20 腿, lower=0.35)

## 三、验收

- 替换判据：tail 版 S ≥ 原版 S **且** sub/2Y 不退化 **且** 平台 fail=0 → 进替换候选池；
- 替换后仍需 self/prod 终验（prod 48h 保鲜，提交前 refresh）；
- 与篮子其余成员互相关 <0.7（tail 改变信号结构，预期相关下降，是加分项）。