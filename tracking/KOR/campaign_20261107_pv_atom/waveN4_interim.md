# Wave N4 中期台账（acquisition_model 估值精修，4/5 批已收）— 2026-11-07

| 模板 | alpha | S | F | 2Y | TO | raFail |
|---|---|---:|---:|---:|---:|---:|
| 估值 W66 | 88RJnnmW | 1.03 | 0.83 | 1.27 | 0.0688 | 3 |
| 估值 W10 | JjezbbjE | 1.15 | 0.98 | 1.27 | 0.0697 | 3 |
| ts_rank 新鲜度 | vR1Gd7WA | 1.00 | 0.71 | 1.21 | 0.1169 | 3 |
| 估值×小盘 合取 | 9qxMJ5N2 | 0.06 | 0.01 | 0.95 | 0.0908 | 3 |
| 估值×信用 合取 | 6Xd0EEoY | -0.31 | -0.12 | 0.06 | 0.0596 | 5 |
| 估值 delta66 | N1NzOOJ7 | 0.92 | 0.56 | 1.18 | 0.1580 | 3 |
| **估值 subindustry** | KPJzL2eE | **1.28** | **0.94** | 1.18 | 0.0602 | 3 |
| W66×W22 自合取 | e75GrWA6 | 1.08 | 0.87 | 1.24 | 0.0660 | 3 |

要点：**subindustry 轴把估值臂从 1.15 抬到 1.28**（本战役 sector 铁律首次被打破的轴）；
但 2Y 卡 1.18-1.27 结构性偏弱；W10/W22 平台 1.15。第5批（region-subindustry / 散度）在飞。

## N5（dl_riskfree 置信度激增精修，10 条）排队中
基线 wpQG55Pv：S **1.73**（越线）/ F 0.89 / 2Y 1.50 / TO 0.3611，raFail 3
（LOW_FITNESS + LOW_INVESTABILITY_CONSTRAINED_SHARPE + LOW_2Y_SHARPE）。
精修杠杆：ts_mean 平滑 delta（降 TO 提 F）/ delta 窗口 10/22 / 换 20d·60d 概率源 /
winsorize 后置 / industry·subindustry 轴 / delta×P20 水平合取。

## 深夜场四轴总结（N1-N4）
- other545 NEMO：封盘（天花板 1.14，2Y 系统性弱）
- acquisition_model 似然分数：死；**估值成分活**（1.15→1.28 subindustry，2Y 弱）
- dl_riskfree 水平族：1.05-1.18；**激增臂 S 1.73 全场唯一越线**（N5 精修中）
- 会话 401 过期一次：`authenticate` 工具重登后恢复（已记 memory）