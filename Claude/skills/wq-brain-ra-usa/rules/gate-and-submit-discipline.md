# USA 闸门与提交纪律

> 本区最贵的一课：**分析师族的墙不在 IS 指标，在 prod**；破墙靠**换中性化**，不是磨算子。
> 全部结论附实测数字；as_of 2026-10-18。

## 一、选集铁律（开工前判定，省掉整轮无效努力）

| 维度 | 硬判据 | 反例（实测判死） |
|---|---|---|
| **频率** | 日更字段直接跳过（TO 结构性爆表）；季频**存量**差分跳过 | `short_interest_pred` 日更 ⇒ TO 0.66 ⇒ fitness 结构性不可达 |
| **形态** | 要**流量/变化率**，不要**存量/水平值** | `institutions18` 季频存量 ⇒ TO 0.037–0.143 达标但 S ≤ 0.92 |
| **更新粒度** | 同机制优先取更新频率更高的集 | `workforce_flow_skills`（日更）S 2.13 vs `macro27`（周更）S 0.92 |
| **塔** | 白名单 = 未点亮塔 × 低 alphaCount，**不按 signal-score 排序** | score top20 全是已点亮的 model 族 |
| **覆盖** | cov < 0.65 反是优势（换手低）；cov < 0.5 视为毒字段 | `operatingprofit` cov 0.21–0.31 |
| **TO 下限** | TO < 0.01 会触发 `LOW_TURNOVER` 闸（太慢也是罪） | `best_eps_numest` / `4wk_chg` |

## 二、破 prod 墙：本区最有效的旋钮是 neutralization

| 手段 | 效果（实测） | 备注 |
|---|---|---|
| **`REVERSION_AND_MOMENTUM`** | 同信号 prod 0.70+ → **0.648**；同时 S/SUB 最高档 | 破墙第一杠杆，成本 1 条 sim |
| **`CROWDING`** | 同信号 prod → **0.644–0.676** | 水平背离族有效；**加速度族无效（0.772）** |
| `SECTOR` | 破 fitness / margin（F +0.13、margin ×2.7） | **prod 0.703–0.72 全挂**，别用它破 prod |
| STATISTICAL / MARKET / INDUSTRY | IS 侧就崩（F 0.89 / SUB 0.53 / 2Y 1.02） | 本区不适用 |
| `hump` | SUB +0.18、TO 减半 | **参数不敏感**（0.01–0.05 同效）；但 prod +0.012 |

**机理**：RAM/CROWDING 剥掉风格因子（反转动量 / 拥挤度）暴露后，与生产池分析师 alpha 的重叠大幅下降，
且残余信号更纯 ⇒ SUB 同步升高。**一举解开「SUB 要低换手、prod 要高换手」的两难。**

## 三、决策表 D0-P 在本区的落地

```
IS 八闸全过
  ├─ prod 与 self 均低于阈值（见 `PLATFORM_CHECK_LINES`）且 self 未超线  → 稳健性闸（brain-alpha-robustness）→ 用户确认 → 提交
  ├─ prod 0.70–0.75（贴线区间）      → 换 RAM 重跑（当日进步 8）
  ├─ prod ≥ 0.75 或踩线失败    → dead_end，换正交概念（禁止同族磨参数）
  └─ self > 0.7                → 同族互残，查已提交同族（同机制互相关常 0.9+）
```

## 四、提交三条铁律（2026-10-18 实测，两条血泪）

1. **MCP `workflow_submit_alpha` 报 `fetch failed` ≠ 未提交**——实测 POST 已送达、状态在 ~240s 后翻转。
   **fetch failed 后等满 flip 窗口再判；换路径重试前必须复查**（否则 403 重复提交）。
2. **提交即改变相关格局**——新 alpha 同时进 prod 池与 self 池 ⇒ 同族候选 PC/self 暴涨
   （实测 0.696 → 0.978）。**同族必须逐个提交，每提交一个即重测剩余候选**；互残 >0.9 立即放弃。
3. **PC 只向上漂**（生产池单调增长）——早上 0.64 的候选下午可能 0.71。**提交前必须重测。**

## 五、base payment 选型（提交目标是 base payment 时）

论坛 4 帖互证：**高 fitness + 低 PC** 是版本答案；self < 0.3 是 BP > 1.5 的强信号；
**`returns` 只影响 OS 特许权使用费、不影响 BP 档位**；VF 是账号级乘数、同批无差异。

选型链：`F×(1−PC) 粗排 → robustness 近 3 年 Sharpe 均值 ≥ 平台 2Y 线且每年 >0.3 → 提交前 PC 重测 → self 互残检查 → 提交`。

## 六、单数据集同族的硬上限

analyst44 三种机制变体（水平背离 / 加速度 / 秩背离）在 PnL 层高度共线：同机制互相关 **0.98**、
跨机制 0.68–0.94。⇒ **单数据集同族最多提交 2–3 颗**，第 N 颗必被 self 闸顶爆。
要更多提交数必须换数据集或换机制族。

实证数字与候选清单见 [`../references/_usa-mining-playbook-20261018.md`](../references/_usa-mining-playbook-20261018.md) §3。
