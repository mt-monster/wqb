# BE225/BE226 fnd45 电话会情绪：臂序修正归因 + 定向升级（2026-11-13）

## 一、★臂序修正（重要方法论教训）

BE225 十臂读数最初被误读：`wpoVAZr1`（S 0.75 / **2Y 1.52** / sub 0.54 / TO 4.9% / margin 2.66bp）曾被当成「PR 陈述段情绪」，
实际核对派发臂序 = **臂9 `group_zscore(group_neutralize(group_zscore(ts_backfill(qa, 66), sector), subindustry), sector)` = 杠杆A × Q&A 情绪**。

**修正后的真归因**：
- **Q&A 情绪（LM2）+ 双层中性化 = fnd45 最强形态**（0.75 / 2Y 1.52，2Y 距闸 0.06）
- Q&A 裸 sector 排序 = -0.32（方向反）⇒ **双层中性化不仅放大且翻正**——SUBINDUSTRY 全仓中性化吃掉绝对水平，只留「行业内相对 + 次级分组内相对」的残差
- PR 陈述段裸 sector = -0.48（BE226 臂9 复测 0.32 确认弱）⇒ 与外部论文一致

**外部论文佐证（本轮现场取证）**：
1. 巴西 1640 场电话会研究（LM/VADER/FinBERT 分段测调）：**Q&A 段负面语气是唯一稳健的收益负相关载体**，prepared remarks 段统计不可靠
2. Fu-Wu-Zhang 2019 (J Business Ethics)：电话会语气预测崩盘风险，**Q&A 段经理语气（非分析师）驱动**
3. 韩国 KOSPI 2010-2024 (SSRN 5079964)：**Q&A 段比 prepared remarks 更能解释市场反应**
4. 论坛 WL27618《字里行间的底气》29 赞：earningscall_sentiment 管理层陈述与问答情绪分析
5. 论坛 FF45555 17 赞：**事件驱动字段禁盲用 ts_rank(252)，半衰期决定窗口**——电话会情绪衰减快，66 短窗优于 252

## 二、BE225/BE226 完整读数（两波 19 臂）

| 形态 | S | 2Y | 判定 |
|---|---:|---:|---|
| **杠杆A × qa w66** | **0.75** | **1.52** | ★唯一升级对象 |
| qa 裸 sector | -0.32 | -0.08 | 方向反 |
| qa 裸 subindustry (BE226 复测) | 0.32 | 0.08 | 弱正 |
| pr 裸 sector | -0.48 | -0.33 | 死 |
| pr 杠杆A (BE226) | -0.16 | -0.03 | 死——杠杆A 用错字段 |
| CEO 变化 / 可读性 / 数字密度 / LM2-Vader 分歧 / 综合 score / Δ66 | -0.53~0.23 | 全负或零 | 全灭 |

## 三、BE227 定向升级（xiz0UaWp4NNczMUrLGqSJl，10 臂在飞）

全部 = 杠杆A 骨架 × 变体（窗 66/126/252 阶梯、signed_power 1.3、winsorize、industry 轴、ts_mean 平滑、qa+pr 加和、qa−pr 差、score 替代）。

判读预案：
- S≥1.58 且 2Y≥1.58 → 全闸验证 + 17 颗篮互相关
- S 1.0-1.58 → 继续窗/幂扫描
- 全灭（<0.75 基线）→ fnd45 杠杆A 形态天花板记录，转 alpha_factor_lib / model238
