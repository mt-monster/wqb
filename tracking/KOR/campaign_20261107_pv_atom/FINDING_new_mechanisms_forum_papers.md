# KOR 新机制侦察 · 论坛 + 外部论文（2026-11-09）

> 应用户要求「查论坛和外部金融论文，尽所有可能找新机制」。背景：本战役新挖 6/10，blocked 症结是「缺新机制 + 32 条存量 OS 池占满 prod 白空间」。
> 本轮**只做侦察与机制梳理，未跑 KOR 仿真**（目标 blocked，待 resume 后验证）。下列机制均正交于存量重镇 shrt38/oth466/MODEL/ANALYST。

## ★ 机制 1：MAX 彩票效应（韩国本土已证实，最优先）
- **论文**：Bali, Cakici & Whitelaw (2011) "Maxing Out: Stocks as Lotteries and the Cross-Section of Expected Returns", JFE 99:427-446。
- **韩国证据**：Asian Review of Financial Research「Lottery-Like Stocks and the Cross-Section of Expected Stock Returns in the Korean Stock Market」——高 MAX 股未来收益更低，最低/最高 MAX 五分位风险调整收益差 **1.39%/月**。KOR 散户占比高，彩票偏好强，机制适配。
- **逻辑**：散户偏愛「可能暴涨」的彩票股 → 推高价格 → 未来收益低；做空有借券/逼空成本，套利受限 → 错误定价持续。行为偏误+套利限制，与风险模型无关。
- **论坛**：post 43508107778711（JFE 完整复现，USA TOP3000 真实仿真附 Alpha ID）。
- **表达式**（波动率标准化主推版）：`-rank(divide(subtract(returns, ts_max_diff(returns,22)), ts_std_dev(returns,22)))`
- **关键算子技巧**：账号无 ts_max 时，`ts_max(x,d) = subtract(x, ts_max_diff(x,d))` 恒等式重建滚动最大值。
- **数据**：基础价量 returns（单数据集 ATOM）。波动率标准化是收益最大的一步（回撤 49%→5.7%）。
- **延伸**：评论指出可复用「极端值统计 + 波动率标准化 + 截面加权」三段骨架，把 MAX 换成单日跌幅/日内振幅/跳空 gap 批量试。

## ★ 机制 2：隔夜跳空累计反转（论坛 27 票，有 BRAIN 复现）
- **论坛**：post 40460201701015「隔夜跳空因子 - BRAIN平台复现详解」（27 票）。
- **逻辑**：过去 20 日累计隔夜跳空幅度大 → 过度反应 → 未来均值回归（收益差）。
- **表达式**：`ts_sum(abs(log(open / ts_delay(close,1))), 20)`；生产版 `-group_neutralize(ts_zscore(上式), densify(sector))`。
- **数据**：open/close（基础价量，ATOM）。

## ★ 机制 3：隔夜/日内「拉锯战」相关性（论文 + 论坛 13 票）
- **论文**：Akbas, Boehmer, Jiang & Koch "Overnight returns, daytime reversals, and future stock returns"。
- **逻辑**：隔夜收益与日内反转的相关性越低 → 多空拉锯越激烈 → 未来横截面收益越高（或反向，需 KOR 实证方向）。
- **论坛**：post 22174527569303（13 票，作者「只差 prod C 就可提交」）；算子 ts_mean/group_mean/ts_regression/rank；评论建议 trade_when 降换手。
- **数据**：Price Volume（open/close），可叠 Sentiment/Risk。

## ★ 机制 4：日内对隔夜涨跌的过度反应（论坛作者做到 prod≈0.5 可提交）
- **论坛**：post 25766755764631（8 票，详细迭代到可提交，prod corr≈0.5）。
- **逻辑**：日内套利者修正隔夜噪声交易者 → 过度修正 → 反转。用 high/low 比 close/open 更含过程信息。
- **表达式演进**：night=open/ts_delay(close,1)-1；inday=close/open-1；V1 `-regression_neut(inday,night)`（prod 高）→ V2 用 high/low 的 over_drop/over_rise + if_else(sign(night))→ V3 发现 low 腿(drop_lo/rise_lc)更优 → **V4 打开 nanHandling 即可提交** → V5 对隔夜做换手率中性化提纯。
- **关键经验**：nanHandling=ON 解决 open/close 含 0 的分母 NaN；low 价腿信号更稳。

## 机制 5（备选）：other323 盘前交易活动（论坛 29 票，数据集级）
- 论坛「晨光熹微时的脚步声：other323 盘前交易活动随想」（29 票）。other323 是独立数据集，盘前活动机制，若 KOR 可用则是 ATOM 白空间。**待查 KOR 字段覆盖**。

## 共性骨架与落地要点
1. **极端值统计 + 波动率标准化 + 截面加权**三段式（MAX 帖评论提炼），可套到涨幅/跌幅/振幅/gap。
2. **ts_max_diff 倒推 ts_max**；算子受限时找「差分亲戚」。
3. **nanHandling=ON** 常是 open/close 分母类因子的过闸关键。
4. 这些机制都用**基础价量 open/close/high/low/returns**——需确认 KOR 哪个单数据集承载（pv1 在排名里 hard_excluded/aC 极高，须查 intraday_pv_feats 或其它 PV 集是否含这些字段做 ATOM；PV 塔已亮，objective 允许单集 ATOM 但要过 prod）。

## 下一步（待 goal resume）
- 优先 KOR 实测 **机制1 MAX** 与 **机制2 隔夜跳空**（表达式现成、机制正交、韩国有证据）。
- 先确认承载数据集与字段覆盖，再按 SOP 10 模板 + 归因；prod 用 MCP 实测。
- 风险：这些是价量衍生，KOR 的 prod 未必低（论坛是 USA 结果）；须实测，别假设。

---

## ★ pv1 实测（goal resume 后，2026-11-09）：MAX 弱、隔夜有真信号
**承载确认**：pv1 = KOR 基础价量单数据集（open/high/low/close/returns/vwap 全 cov1.0，ATOM）。

### MAX 彩票效应（6 模板）→ KOR 弱
- 最佳 MPYn5wdz 裸 MAX22：S **0.81**/F0.57/2Y1.32；波动率标准化版反而更弱（S0.02–0.63，与 USA 相反）。
- ⇒ MAX 单因子在 KOR 不足 1.58，**不作主交付**；「极端值+波动标准化」骨架留作配料。

### 隔夜/日内（6 模板）→ 近线，方向对
| alpha | 机制 | S | F | 2Y | raF |
|---|---|---:|---:|---:|---|
| **e75PqeeJ** | 隔夜收益反转 ts_mean22 | 1.17 | 0.82 | **2.04** | 2(S,F) |
| **9qx3AgQ2** | 隔夜跳空累计反转 20 | 1.18 | **1.03** | 1.44 | 2(S,2Y) |
| GrWN3E0Q | 隔夜跳空累计 66 | 1.03 | 0.94 | 1.51 | 3 |
- **归因**：隔夜反转 2Y 强（2.04）但 F0.82 被 TO0.158 拖累；跳空累计 F 过但 S/2Y 欠。
- **精修已收（8 条）**：decay12/20 压 TO 到 0.11–0.12，但 S 反降（1.04/0.96）；窗口 10/44、subindustry 组轴均更弱。最佳仍是基线：
  - e75PqeeJ 隔夜反转 w22/sector/d4：S **1.17** / F0.82 / **2Y2.04**；
  - 9qx3AgQ2 跳空累计 20/sector/d4：S **1.18** / **F1.03** / 2Y1.44；
  - 9qx3Annd 跳空 20/d12：S1.16 / F1.09 / 2Y1.32。

### 结论：论坛/论文新机制在 KOR 均不足交付（诚实负结果）
- **MAX**：最佳 0.81，波动率标准化在 KOR 反而伤（与 USA 相反）→ 不作主交付。
- **隔夜/日内**：机制真实且正交（2Y 最高 2.04），但 **S 结构性封顶 ~1.2**，decay/窗口/组轴全扫尽也到不了 1.58 → 近线 park，非交付件。
- 共投 20 仿真（MAX6+隔夜6+精修8），**未新增可交付颗**。交付仍 **6/10**。
- 启示：KOR 对这类「价量行为」单因子给的 Sharpe 上限低；要破 1.58 需更强机制或组合，但 ATOM+算子≤12+禁混腿约束下空间极窄。

### 补测：日内对隔夜过度反应（论坛唯一可提交机制）→ KOR 仍封顶
- 论坛 Version5 靠 `regression_neut` 提纯做到可提交；**本地算子目录无 regression_neut**（仅 group_neutralize/ts_regression/vector_neut）。
- 基础门控反转 6 式：最佳 vR1b50pQ S**1.16**/2Y1.6；裸 multiply 版高换手全崩。
- 用 vector_neut 替代提纯 2 式：S**0.95/0.66**，更弱（vector_neut≠regression_neut）。
- ⇒ 隔夜/日内机制在 KOR **S 封顶 ~1.2**，提纯也救不动，**非交付件**。

## 最终结论（本轮新增 26 仿真后）
MAX(0.81) / 隔夜跳空·反转(~1.18) / 日内过度反应(~1.16) / vector_neut 提纯(0.95) **全部 <1.58**。
论坛/论文价量行为新机制在 KOR 系统性够不到交付线；**交付仍 6/10**。KOR 现实上限 ~6 颗已被「全数据集 + 全部新机制 + 各救援/第二席」三重实测钉死。


