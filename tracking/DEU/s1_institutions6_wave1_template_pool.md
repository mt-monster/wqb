# s1_institutions6_wave1 模板池（DEU / TOP500 / D1 / SUBINDUSTRY）

数据集：institutions6 Stake Ownership（institutions 塔，11 MATRIX，cov 1.0 / ac 270/127）。**单塔 ATOM 合法**（institutions 不在 trio，无塔混问题；institutions1 判死不跨集封杀）。

## 一、字段面（get_datafields 实拉，11 MATRIX 全 cov 1.0）

- 持仓水平族：aggregate_equity_value_all_owners / aggregate_equity_value_institutions / aggregate_share_count_all_owners / aggregate_share_count_institutions
- 买卖广度族：count_institutional_buyers_security / count_institutional_sellers_security / count_institutional_holders_security
- 交易流量族：market_value_institutional_shares_acquired/disposed、quantity_institutional_shares_acquired/disposed

**结构优势**：institutions6 直接观测「本期买入/卖出」流量，**无 institutions18 那类持仓差分的披露滞留重复问题**（金帖评论区 XM75236/FX25214 的核心质疑天然规避）。

## 二、金帖两读（2026-11-03 论坛取证）

### 金帖 A：institutions18 GLB 因子化（WY79095，11 票 20 评）
- **提交占位**：作者已提交 Sharpe 2.78 件（GLB/MINVOL1M/SLOW_AND_FAST/decay0）——institutions 机制线在 GLB 生产池有占位，但 DEU 是不同 region/设置档，指标不可比、机制可迁移。
- **核心机制**：① 股数差 >> 市值差（市值=价格×股数，价格污染会翻转信号；APAC 0.23→1.23 单步最大收益）② **ts_mean 20-40d 平滑后累积持仓变化 = 反转信号而非动量**（多数人读成动量跟随，alpha 在拥挤反转）③ 决定性腿 = 市值分桶 bucket + group_rank（消区域市值结构偏差）④ ATOM 对照：rank(cur_holding)≠rank(cap)，持仓水平≠规模。
- **开放问题（=差异化模板空间）**：2Y 第4年脆弱（~1.50）；区域不对称（**EMEA 1.83 强、APAC 1.03 边缘——DEU 属 EMEA，方向先验利好**）；模板迁移面。
- **评论区金矿**：JM/JR57542——生产池占住「变化量/流量」轴时差分类构造 PPAC 高，**水平类构造（渗透率水平）是正交第二命**；FX25214/XM75236——披露滞留混淆检验（ts_delta vs 事件 vs 平滑三版本对照）；ZZ10277——窗口三档并排+分桶粒度扫描。

### 金帖 B：institutions4 欧洲持仓随想（WL27618，28 票）
- **广度×深度共振**：持股比例↑ + 机构家数↑ 同向 = 信号质量最佳。
- **拥挤见顶**：同类型基金顶格买入 ⇒ 边际买家耗尽 ⇒ 见顶反转。
- 欧洲标的实证，与 DEU 直接同域。

### 论文侧（web_search 取证）
- **13FPulse 50 季度实证**：核心信号=持仓家数广度变化 d_holders（横截面排名）；**股数流量变化无预测力（略负）**——与 Chen, Hong & Stein (2002) breadth-of-ownership 一致。⇒ 广度为主、流量为辅/对照。
- OL Institutional Positioning 三分解：net flow / breadth / crowding proxy（holders 中位数）——与本集三字段族精确同构。
- 失效边界：breadth 趋势确认不抄底（V 型反转如 TSLA 2019 反读）；「熄灭+价弱」=退出信号。

## 三、模板池（12 个结构互异；照抄臂 1 / 开放问题臂 4）

| # | 骨架 | 机制 | 来源 |
|---|---|---|---|
| T1 | rank(ts_delta(holders, 22)) 广度变化 | 持仓家数净变化=共识扩散 | 13FPulse/CHS2002（论文） |
| T2 | −group_rank(ts_mean(净流量 q_acq−q_disp, 22)) 平滑反转 | 拥挤反转（平滑翻转符号） | 金帖A 照抄改造（股数流量替代持仓差分） |
| T3 | +净流量未平滑对照臂 | 检验「平滑翻转」vs 披露滞留 | 金帖A 评论区开放问题 |
| T4 | divide(subtract(buyers, sellers), holders) 买卖广度失衡 | 净买家占比 | 金帖B/IVA-MFM-CNI |
| T5 | multiply(净流比率, 净广度) 深度×广度共振 | 同向交互放大 | 金帖B 核心 |
| T6 | 拥挤反转：holders 水平分位极值反向 | 边际买家耗尽见顶 | 金帖B/金帖A |
| T7 | trade_when(拥挤门控, 净流反转) | 拥挤态才反转 | 金帖A 机制二 |
| T8 | ts_delta(divide(share_count_inst, share_count_all), 22) 渗透率变化 | 价格无关渗透 | JR57542 正交命 |
| T9 | 价值增长−股数增长 分歧（价格驱动 vs 真需求） | 价值涨股数不涨=价格行情→反向 | 13Foresight 分解（开放问题） |
| T10 | divide(净流量价值, 持仓价值) 流量/存量速度 | 仓位周转速度 | OL net-flow/position |
| T11 | divide(buyers, holders) 新买家占比 | 边际发现速度 | 13Foresight（开放问题） |
| T12 | ts_sum(buyers>sellers, 66) 买方连续性 streak | 一致性确认 | 13Foresight buying streak |

差异维度覆盖：矩（水平/一阶差分/交互乘积/比率）、加工（平滑/未平滑/门控/连续计数）、方向（动量/反转对照）。

## 四、DEU 适配与硬闸提醒

- 金帖设置档（GLB/MINVOL1M/SLOW_AND_FAST/decay0）≠ DEU 标准档（TOP500/SUBINDUSTRY/decay4）：指标不可比，机制可迁移；不用 cap 分桶腿（会点亮 PV！金帖的 bucket(cap) 在 DEU 塔混禁令下必须改造为 subindustry 分组或集内比率）。
- 量纲安全：T4/T5/T8/T10 全用同族字段做 add/subtract 后再 divide；禁 add(带量纲,裸常数)；比较两端同字段不同时点。
- 稀疏事件警报：count/value 字段是「本期累计」型 MATRIX（稠密），非事件稀疏型，可用 ts_delta；但 T3 对照臂若大面积 nan 会按空仓诊断特征处理。
- 派发前双预检：preflight_expressions（alpha_expressions）+ verify_expr；算子硬闸=get_operators 精确名单。
- 生产池克隆预警（JR57542）：变化量/流量轴提交前必查 PPAC/self；水平轴 T8 是正交备胎。

## 五、执行状态

- 表达式 12 臂已落：`institutions6_wave1_templates.json`。
- **双预检全绿（2026-11-03 06:5x）**：preflight 12/12 valid（10 字段全存在、any_changed=false；warning 仅分页重试失败，holders/sellers 两字段已被 get_datafields 直拉独立证实存在）；verify_expr 12/12 valid（`"errors": []`）。
- 待 news20_wave1 / other250_wave1 收完释放槽位后派发（task-id `institutions6_wave1`），batch-size 2 / concurrency 1。

## 六、全波收口（2026-11-03 07:3x，12/12 全 COMPLETE 零 ERROR，task `inst6w1_20261103`）

| # | 臂（JSON 序） | S | TO | 备注 |
|---|---|---|---|---|
| 0 | T1 持有人数广度变化 `ts_delta(ts_mean(d_holders,22),22)` | +0.41 | 0.069 | 13FPulse 核心面 |
| 1 | T2 净流取反 | −0.32 | 0.017 | 与 T3 符号互证 |
| 2 | T3 净流量 `ts_mean(net_shares,5)` | +0.35 | 0.019 | 机构净流入正向 |
| 3 | T4 买卖广度失衡 | +0.21 | 0.050 | |
| 4 | T5 净流量×广度交互 | +0.29 | 0.062 | |
| 5 | T6 holders 水平取反 | −0.23 | 0.014 | |
| 6 | T7 trade_when 门控净流 | −0.34 | 0.016 | 门控反噬 |
| 7 | T8 机构持仓占比变化 | −0.45 | 0.077 | |
| 8 | T9 价值vs数量背离取反 | −0.63 | 0.038 | 全波最弱 |
| 9 | T10 净流/权益价值 | −0.32 | 0.031 | |
| 10 | T11 买家占比 | +0.45 | 0.065 | 次优 |
| 11 | T12 买入广度持续性 `ts_sum(greater(buyers,sellers),66)` | **+0.48** | 0.028 | 全波最强 |

**判弱收口**：max|S|=0.48，距 LOW_SHARPE 闸 1.58 差 70%。符号自洽成立（净流量 +0.35 / 取反 −0.32 互证）= 机构净流入正向机制在 DEU 真实存在但幅度极弱。最强两面（买入广度持续性 0.48、买家占比 0.45）都是**广度结构**而非流量——若后续迁移他集，优先广度轴。按机制×数据集二维律只封 institutions6×DEU 组合。

