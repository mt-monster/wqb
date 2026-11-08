# Wave N6/N7 破墙全谱（0mYgpJzK 家族）— 2026-11-07

## prod 阶梯（全部 raFail=0 除注明外）

| 变体 | alpha | S | F | 2Y | prod |
|---|---|---:|---:|---:|---:|
| 基准 d5×lv22 (RM 中性化) | 0mYgpJzK | 1.89 | 1.28 | 2.21 | 0.8182 |
| d10×lv22 | ZYQz7XZx | 1.79 | 1.31 | 2.03 | 0.8271 |
| d5×lv22 winsorize 后置 | 2rA6OVWY | 1.88 | 1.30 | 2.35 | 0.8255 |
| d5×lv22 decay8 | JjezNgLA | 1.68 | 1.30 | 2.00 | **0.8468**（更差） |
| d10×lv60 | E56zvnxJ | 1.70 | 1.23 | 1.97 | 0.8039 |
| ts_rank(delta,66)×lv22 | 6Xd0A1ZE | 1.79 | 1.16 | 2.14 | 0.7986 |
| d5×lv60 | 6Xd0lGxE | 1.79 | 1.20 | 2.11 | 0.7946 |
| **d5×lv22 SECTOR** | 78Lmo5Y1 | **1.88** | **1.35** | **2.39** | **0.7813** |
| **d5×lv22 MARKET** | omEGEe5b | **1.88** | **1.37** | **2.43** | **0.7804** |
| d5×lv60 SECTOR | WjOzLZlj | 1.75 | 1.24 | 2.23 | **0.7779** ← 当前最优 |

## 杠杆效果总结
- 换合取腿 lv22→lv60：prod −0.02~0.03（唯一稳定有效的表达式杠杆）
- 中性化换基 RM→SECTOR/MARKET：−0.037（最大单杠杆，且读数同时变强）
- decay8：+0.03（反效果，弃用）；trunc04：不 binding；delta 窗口位移：无效
- winsorize 后置（乘积层）：无效；ts_rank 包装：−0.02
- vector_neut(delta, level)：与裸 delta 逐位相同 ⇒ delta 已与 level 正交，prod 撞的是激增信号本身

## N7 结构去相关臂（全部死路）
delta⊥level = 裸 delta（1.73）；level⊥delta 1.06；跨期相对信念 −0.81；期差动量 1.30；加速度 0.92。

## 当前离线差：0.7779 → 0.70 还差 0.078
N8 在飞：MARKET+lv60 组合、P(down) 反向构建（label0 与 label1 非完全互补=独立信息源）、3/4 分位桶变体。
若 N8 最优仍 >0.75，则判定 dl_riskfree 激增族被 prod 占据（同 tnc 族结论），转 honest verdict。