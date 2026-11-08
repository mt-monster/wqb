# analyst44 / analyst9 字段画像 —— DEU/TOP500/D1 —— 2026-11-03

**来源**：MCP `get_datafields`（兜底通道）；§86 真新鲜池；ANALYST 塔已由 shrt3（同塔）出货证明「旧口径判死」失效。

## analyst44（anl44_*，估计修正事件集）
- **72 个 VECTOR 字段**，cov 0.37–0.69，alphaCount 合计 121、**43 字段零使用**，最挤 dps_value=18。
- 结构：**每指标（csh/dps/eps/ebitda/roe/…）× {value, prevalue, lastactvalue, coveredby, lastactccy}** 估计修正事件五元组。
- **机制箱**：估计修正 surprise / change ratio（自构 `divide(subtract(value,prevalue), abs(prevalue))` 类）；修正幅度、修正方向计数。
- **⚠ 家族克隆预警**：与 shrt3 赢家族（pwdl6ov6 的 `mean_estimate_change_pct` 腿 / predicted_surprise）**同为估计修正 PnL 家族**——同族 alpha 在 prod 检查上会撞家族克隆（家族内判死半径）。若用 anl44，信号须走**不同形态**（如 breadth 计数、修正持续性），避开 change-ratio 形态。

## analyst9（anl9_*，共识估计 + 修正广度集）
- **51 个 VECTOR 字段**，cov 0.56–0.62，alphaCount 合计 187、34 零使用；最挤 daily_numup=43 / s_numup=41 / daily_numdn=28（分析师上调/下调计数）。
- 结构：consensus（dataitemvalue/effectivetime/splitfactor/totime）+ **修正广度 numup/numdn/numanalysts**（daily_* 与 s_* 双口径）。
- **机制箱**：①**修正广度分歧** `subtract(numup, numdn)` / 比率——正对论坛《机构情绪分歧因子》（买/卖计数→趋势持续性）与分歧论文口径；②共识值变化；③覆盖广度 numanalysts。
- 广度计数是**水平型/事件型**：横截面 `group_rank(raw, g)` 优先，慎用逐股 ts 归一（灭活教训）；降换手用 trade_when/ts_delta。

## 选型对照（与 news50/other47 排队）
| 集 | 塔 | 主机制 | 新鲜度 | 风险 |
|---|---|---|---|---|
| news50 | NEWS | 情绪/新颖性/分歧 | ★★★（14 字段零使用） | 情绪差骨架出货率低（论坛负证据） |
| analyst9 | ANALYST | 修正广度分歧 | ★★ | 数数骨架需防水平型灭活 |
| analyst44 | ANALYST | 估计修正 surprise | ★★ | **与提交篮同家族克隆风险最高** |
