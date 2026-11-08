# CHN NEWS 塔跨区迁移终局（2026-11-03）

> 2026-11-08 整理：本段原被误追加到 `tracking/CHN/config/cells.json` 末尾，
> 导致配置文件 JSON 解析失败。现剥离为独立文档，cells.json 只保留配置。

## §7 跨区迁移战役的 CHN 侧终局（2026-11-03 14:0x）

**结论：CHN 的 NEWS 塔（CHN/D1/NEWS，倍率 1.7）在本轮「GBR 模板迁移」框架下判为结构不可达。**

判据（全部实测，非推测）：

| # | 证据 | 读数 |
|---|---|---|
| 1 | news46 首波 12 模板（BASE 档 + 壳） | S −0.84 ~ +0.25，TO 塌到 4–7% |
| 2 | news46 逐年覆盖（3 条实测） | 10/10 年有 pnl + longCount 15–40 ⇒ 数据无问题 |
| 3 | news46 四种换面几何（FAST 档） | −1.06 ~ −1.44（看似强信号） |
| 4 | ★ news46 正负两极配对（6 组） | **全部同号同负** ⇒ 非方向信号 = 伪影 |
| 5 | ★ news46 单因子隔离波（12 格） | 分组型中性化 +0.08…+0.18；**因子型（FAST/STATISTICAL/SLOW）−0.67…−0.76** |
| 6 | news46 最优档（SUBINDUSTRY/decay4） | **S = +0.18** |
| 7 | news38 首批正负两极（真·正负双通道） | spread −0.54/−0.58；neg_heat −0.97/−0.67 ⇒ 同负 |
| 8 | CHN 严闸 | LOW_SHARPE **2.07** + LOW_2Y_SHARPE **2.07**（`get_alpha_details` 实读） |

⇒ 最优档 S=+0.18 距严闸 2.07 差一个数量级；两个最高质量 NEWS 集（news46 cov 1.0 / news38 正负双通道）均证无方向信号。
⇒ 连续多波 max|S| < 0.5，触发 `diversity.signal_floor`（floor 0.5 / min_batches 2，fail-closed）。

**⇒ dead_end 登记（CHN/news46 + CHN/news38）**：

```
id: CHN-NEWS46-CROSSREGION-SETTINGS-NEUTRALIZATION-DEAD
family: news46 Relevant News Analytics / 事件到达率密度轴
text: CHN news46 迁移 GBR 的密度反转模板族（12 模板 + 4 几何换面 + 6 组正负两极 + 12 格单因子隔离）
      ⇒ 判死。最优档（SUBINDUSTRY/decay4）仅 S=+0.18，距 CHN 严闸 2.07 差一个数量级；
      且 4 种几何在因子型中性化下的 −1.06~−1.44 全是「FAST/STATISTICAL/SLOW × 事件到达率」
      的负漂伪影（正负两极同号同负 + 隔离波证实），不是可取负的真信号。
      ⚠ 附带结论：CHN 禁用因子型中性化（FAST/STATISTICAL/SLOW），只用分组型
      （SUBINDUSTRY/MARKET/SECTOR/INDUSTRY）；这是 CHN 专属，不可外推到其它区。
      除非：换到 cov 1.0 之外的新字段族（如 storyid_* 之外的层级），或 CHN 严闸放宽。
dataset: news46
bound: payload
```

```
id: CHN-NEWS38-DUALCHANNEL-NOSIGNAL-DEAD
family: news38 News Analytic Model / 正负情绪双通道
text: CHN news38 的 mws38_positive_score/negative_score 是全平台少见的真·正负双通道（字段级 aC 0-2，cov 0.938），
      但正负两极配对实测同负（价差 −0.54/−0.58；负面热度 −0.97/−0.67）⇒ 无方向信号，非方向问题。
      判死。注：CHN news38 的 sg_/tc_ 前缀是 story-global / time-cross 层通道，
      后续若要挖「层级差」轴可另立模板族（本轮未测）。
dataset: news38
bound: payload
```