# INSIDERS 深挖 · Step 2 结果 + Step 3 在飞（2026-11-11）

## BE115 字段可访问性探针（4aBhqTgaS4MVbtMlDQI444R，4 臂 4 FAIL）

**结论：4 字段平台不可访问**（子 sim location 亦 404，错误详情不可见）：
- top_significant_value_1
- directional_significant_value_1
- directional_indicator_2
- top_directional_significant_value_1

⇒ 已写入 memory：**任何从未跑过的字段首次使用必须 ≤4 臂小批探针**（preflight 会判 valid，但平台执行整批连坐 FAIL）。
⇒ BE114 十臂全灭的根因确认，非机制问题。

## BE116 insiders1 nan OFF 设置档（4xbS2Jfxw4SkaC21a9j4HtW，10 臂 0 错误）

| 臂 | 构造 | S | 2Y | lc/sc |
|---|---|---:|---:|---|
| blaXElNl | Δ66 平滑（基线构造） | 0.54 | −0.81 | 31/31 |
| xAvqgAem | Δ(mean110,66) | 0.38 | −0.07 | 45/46 |
| gJa6pJmQ | Δ(mean66,110) | 0.16 | 0.06 | 29/30 |
| XgaG6gkx | 仓位占比 Σ66 | −0.17 | 0.03 | 47/47 |
| mLap9LZ9 | conviction mean66 | −0.13 | −0.07 | 47/47 |
| A1x9K1kw | 双腿相加 | 0.09 | −0.53 | 31/31 |
| ZYa6GYrd | sig×Δ66 | 0.33 | 0.27 | 33/33 |
| leadXe0O | Δ132 | 0.00 | 0.32 | 43/44 |
| A1x9K13w | Σ66 仓位占比 | 0.07 | 0.15 | 47/47 |
| gJa6pJ30 | valueeur/holdings | −0.03 | 0.15 | 47/47 |

**判定：nan OFF 是 insiders1 的毒药**——最优臂 0.54 vs nan ON 的 1.06（差 −0.52），且 **lc/sc 变成完全对称的小数（31/31、45/46、47/47）**，说明 nan OFF 把无申报股票整批剔除后，横截面只剩少数申报股，组合退化。
⇒ **insiders1 与 pv20×insd 同向：必须 nan ON**（缺失=无内部人交易=真值 0）。设置轴正式关闭。

## 累计设置/机制结论（insiders1）

| 轴 | 结论 |
|---|---|
| nan_handling | **ON（1.06）≫ OFF（0.54）** ❌ OFF 关闭 |
| 分组轴 | sector 1.06 / market 1.04 / subindustry 0.86 ⇒ 个股级信号，轴不敏感 |
| decay | 4 基准；decay22 平滑 0.94 < 1.06 ❌ 无增益 |
| 水平时序化 | ts_rank/ts_zscore(holdings) 全空心（TO 58-62%）❌ |
| tail 去并列 | 0.36，sub −0.30 ❌ 反噬 |
| 门控 | sig==3 硬门控 S 0.33 但 **2Y 1.34**（近端信号）|

## Step 3 在飞

- **BE117**（1ge6Y4fPA4jIcyOByim6ayj，10 臂）：**Δ66 × 真实仓位占比** 双腿组合（两字段同属 insiders1，不涉禁混）。几何：等权 group_zscore+簇中性（冠军式）/ 纯 group_rank / 2:1 权重 / 冠军腿型 tail+winsorize / 乘法一致 / 裸值相加 / decay22 / market 轴 / Δ66×sig门控 / 三腿（Δ66+仓位占比+sig门控）。
- **BE114b**（3uM4j7C3573aDbn5I3ACcq，10 臂）：agg_matrix 用**已验证字段**重建未测机制——鲸鱼集中度 avg/total、买入笔数代理 total/avg、股数口径买卖比、SV1 时序分位/z、SV2 单测、direct/exec 买卖比、SV1/adv20 锚点、方向×量级。

## 判读线

|S| ≥1.2 满波 / 1.0-1.2 定向 / <1.0 换机制。BE117 若任一臂 >1.06（insd1 单腿天花板）则双腿组合有效；若 >1.4 则 INSIDERS 单塔有破闸希望。
