# sentiment7 开波设计：论坛金帖 + 论文取证 + 差异化模板池（2026-11-03）

## 一、论坛金帖取证（LC97552 post 43179860065303，72 赞/51 评，2026-09-02）

**获胜表达式 np7nn69l**（S 2.04 / F 1.92 / MG 24.2bps / 17 项全 PASS，DEU/D1/SENTIMENT x1.9）：
`vector_neut(quantile(ts_ir(ts_mean(ts_max(ts_backfill(vec_avg(snt7_all_languages_views), 22), 5), 5), 22), 120), ts_backfill(vec_avg(snl27_relpopularity08), 22))`

**机制共识**：注意力脉冲 = (窗口峰值 − 周期基线) / 历史波动，再剥离人气规模。信号空间在**突增动态**而非水平（Chalamandaris 2026：情绪水平只可测量不可交易）。

**★★★ 生产池占位警告（战略级）**：作者三代同线 alpha 已提交 OS——gen1 add 骨架 PC 0.319 / gen2 subtract PC 0.557 / gen3 vector_neut **0.6338**。同字段同结构换壳再挖**必撞 prod 且余量仅 0.07**。帖子原文复用警告：「直接复制会推高 PC 风险，模板的正确用法是换 ATTENTION_MEASURE 字段源，而非复制字段组合」。

**已实证教训（照抄即避坑）**：
- rank 包装中性臂一致性有害（每剥一层 F +0.3-0.65）
- ts_mean(ts_max) 双层是 F 主杠杆（+0.62）；ts_max(bf,5) 简化版 F −0.23 不划算
- `ts_ir` 换 `ts_zscore(x,252)` 全结构崩盘（S −0.33）——zscore 长窗外层在该字段族禁用
- 中性化：SUBINDUSTRY(2.18) > INDUSTRY(1.79) > SECTOR(1.53 FAIL)
- decay 甜点随结构重置：gen3 = decay16 / trunc 0.02（gen1/2 是 decay2/0.01）

**帖子留下的未解决面 = 我们的差异化挖掘空间**：
1. ts_arg_max 峰值年龄 vs 峰值强度（评论 ZW26474：峰值年龄独立臂+二维分组）
2. 突降反向（ts_min 同链路，**不要默认取负号**——反向不是镜像）
3. 回落时点/衰减幅度（脉冲后如何消化）
4. 第 4 骨架 group_neutralize 替代 vector_neut
5. 换 POPULARITY_PROXY 对照（snl27 后五年才有数据——覆盖需另核）

**评论区金句**：XC78928——有限注意力文献模板「突增之后往往先延续、再反转」，snt7 纯突增字段过得了反转模板，relpopularity 稳态字段挂模板（与「水平型 vs 时效型」判据互证：浏览量=时效型，ts 归一化受益）。

## 二、论文取证（web_search 2026-11-03）

| 文献 | 机制结论 | 对模板的启示 |
|---|---|---|
| Pyun (2024) Economics Letters 241, "The Wikipedia Effect" | Δviews（变化量）多空组合显著 alpha，周度调仓 > 月度（短期性） | T8 变化量横截面而非水平；窗口短 |
| SSRN 6637361 (Russell 1000, 2015-2024) | 注意力溢价 1/5/20 日显著；高波动期集中（t=2.86 vs 1.05）；散户重仓股溢价 2.1 倍 | 条件门控可用波动/散户倾斜分组 |
| Cergol & Omladič (2015) | 牛熊不对称：熊市正相关「merry frown」/ 牛市负相关「sour smile」（纠偏反向） | T9 状态条件臂；反向非镜像 |
| Da-Engelberg-Gao (2011) In Search of Attention | 搜索注意力预测短期量价 | 脉冲→量/波动先于收益 |
| Alphanume 方法综述 | 滚动 z-score 峰值（30-90d 基线）、注意反转 overreaction reversal、短持有期成本敏感 | T6 峰值-基线差；换手要低 |

## 三、sentiment7 字段面（s1_news38_profile 同期画像）

- `snt7_all_languages_views`（VECTOR，cov 0.754 / ac 65）：全语言浏览量主源，先 vec_avg
- `snt7_views`（VECTOR，cov 0.736 / ac 34）：主语言子集，与主源高相关，做背离臂
- `snt7_timestamp`：元数据，不做信号
- 单数据集 ATOM；内建 fields（returns/adv20 等）当条件不占塔配额

## 四、模板池（12 个结构互异，正式波 ≥10 ✓）

骨架约定：`bf = ts_backfill(vec_avg(snt7_all_languages_views), 22)`；全波 SUBINDUSTRY / DEU / TOP500 / D1 / decay4 / trunc 0.08 基准档（gen3 甜点档 decay16/0.02 作设置对照臂另记）

| # | 骨架 | 表达式（bf 代入后） | 结构差异 | 来源 |
|---|---|---|---|---|
| T1 | 峰值年龄 | `group_rank(ts_arg_max(bf, 5), subindustry)` | 峰值时点而非强度 | forum ZW26474 |
| T2 | 突降反向 | `group_rank(ts_ir(ts_mean(ts_min(ts_backfill(vec_avg(snt7_views),22), 5), 5), 22), subindustry)` | ts_min 同链路（非取负） | forum「反向非镜像」 |
| T3 | 回落衰减 | `group_rank(ts_av_diff(ts_max(bf, 5), ts_last(bf), 5), subindustry)` | 峰值→当前消化度 | forum 疑问③ |
| T4 | 第 4 骨架 | `group_neutralize(quantile(ts_ir(ts_mean(ts_max(bf, 5), 5), 22), 66), subindustry)` | group_neut 替代 vector_neut | forum 疑问④ |
| T5 | 脉冲加速度 | `group_rank(ts_delta(ts_mean(bf, 5), 5), subindustry)` | 二阶（突增的突增） | 自建·脉冲动力学 |
| T6 | 峰值-基线差 | `group_rank(divide(ts_av_diff(ts_max(bf, 22), ts_mean(bf, 22), 22), ts_std_dev(bf, 22)), subindustry)` | 滚动 z 峰值 | paper Alphanume |
| T7 | 突增密度 | `group_rank(ts_sum(greater(ts_last(bf), ts_mean(bf, 22)), 22), subindustry)` | 事件密度计数 | 自建 |
| T8 | Δviews 横截面 | `group_rank(ts_av_diff(bf, 22), subindustry)` | 变化量直排（Pyun 核心） | paper Pyun 2024 |
| T9 | 注意-收益耦合 | `group_rank(ts_corr(bf, returns, 22), subindustry)` | 牛熊不对称耦合态 | paper Cergol 2015 |
| T10 | 衰减加权脉冲 | `group_rank(ts_decay_linear(ts_ir(ts_mean(bf, 5), 22), 5), subindustry)` | 时间衰减核 | 自建 |
| T11 | 短窗 zscore 对照 | `group_rank(ts_zscore(ts_mean(ts_max(bf, 5), 5), 22), subindustry)` | 短窗 z 外层（长窗禁用的对照臂） | forum 反例·自建 |
| T12 | 双源背离 | `group_rank(ts_av_diff(vec_avg(snt7_all_languages_views), vec_avg(snt7_views), 22), subindustry)` | 多语言 vs 主语言注意力背离 | 自建 |

**窗口取值理由**：5/22/66 均白名单；T4 的 66 替代原帖 120（120 非标，原帖有 IS_Ladder 甜点实测但本波先用白名单，留 120 作后手变体并附原帖证据）。

**派发前预检**：verify_expr.py 语法 + preflight_expressions 字段存在性（含 snt7_views / returns / subindustry 轴小写）；载荷三键 {type,settings,regular} 全必填；batch-size 2 / concurrency 1。

**验收预锁**：prod<0.7（**本波重点防线**：预计 0.5-0.65 撞作者族，浅钉不判死走归因破墙）+ self<0.70 + S≥1.58 + 2Y≥1.58 + RA=0 + 覆盖无连续多年空窗。

## 五、派发实录与修正（2026-11-03）

- 首发 `sentiment7_wave1`（pid 57052）首批全灭：T2 用了**平台非法算子 ts_min**（子仿真 ERROR: unknown operator），T1 被连坐 CANCELLED；且 CANCELLED 不在 runner 轮询终态白名单 → runner 干挂（30 分钟超时线）。
- 修正：T2 等价改写 `ts_min(x, 5)` -> `subtract(0, ts_max(subtract(0, x), 5))`（min 恒等于 -max(-x)，机制语义不变），verify_expr 通过；杀 pid 57052 后以 `sentiment7_wave1r`（pid 55536）重启，resume recognized 0/12 干净重发，首批 3qm6dO9Te4iTbE33RW1U5ov 已在飞。
- **工具教训**：verify_expr.py 的算子白名单与平台不一致（ts_min 过本地语法校验但平台报 unknown operator）——冷门算子以平台为准，或先单探针再开波。

## 六、ts_max 幽灵算子事件与二次重写（2026-11-03 06:15）

- wave1r 首批再报 **`ts_max` 也是平台不可访问算子**（T2 修复臂 ERROR + T1 连坐 CANCELLED）。get_operators 精确名单（103 算子）：**ts_max / ts_min / ts_median / ts_skewness 全不存在**；operator_audit 对此假阴性（报 safe）。
- 平台真算子 `ts_max_diff(x,d) = x - ts_max(x,d)` ⇒ 恒等式 **max(x,w) ≡ subtract(x, ts_max_diff(x,w))**；min 走双重取反。ts_arg_max=峰值年龄（合法）。
- 毒臂 5 条（T2/T3/T4/T6/T11）全部按恒等式重写，verify_expr 5/5 过、其余算子逐一比对 get_operators 名单在册；T1/T5/T7/T8/T9/T10/T12 不动。
- 06:18 以 `sentiment7_wave1s`（pid 55068）三度重启，12 臂重发。**论坛获胜式里的 ts_max 是伪代码**——照抄外部表达式前必须先过 get_operators 名单换算。

## 七、quantile 1 参陷阱与批 2 重发（2026-11-03 06:3x）

- 批 2（T3/T4）真终态：T4 `ivnmP9gl` **ERROR**（Invalid number of inputs : 2, should be exactly 1）+ T3 `3mJ3Tt8l` 连坐 **CANCELLED**。
- 真因：`quantile(x, driver=gaussian, sigma=1.0)` 是**横截面 1 位置参**算子，T4 原写法 `quantile(ts_ir(...), 66)` 多传了窗口参。报错 location start=17 精确指向 `group_neutralize(` 后的 `quantile`，毒臂定位无歧义。
- 修复：`quantile(` → `ts_quantile(`（`ts_quantile(x, d)` 才是带窗口的概率变换，d=66 在窗口白名单）。verify + preflight 双绿，ts_quantile 在 get_operators 103 名单内。
- 处置：杀 runner 55068（CANCELLED 不在轮询白名单会干挂）→ 同 task-id resume（新 pid 57000），T3 连坐重发 + T4 修复版，T1/T2 指纹在 CSV 自动跳过。

## 八、resume 批 1 再败与重试管线（2026-11-03 06:4x）
- resume 批 1（T3 重发 + T4 ts_quantile 修复版）**双双 ERROR**，报错均为平台通用运行错「There was an error while running the simulation. Please try again」，同秒落地（疑批级瞬时故障/连坐），非语法错（T4 修复版语法已过）。
- 对照面：T5（ts_delta 动量）S **0.49** / T6（min-identity w=22 + zscore 几何）S **−0.42** 正常出数 ⇒ min-identity 结构本身无毒；w=5 版本（T2 negated 形态 S 0.40 也活过）差异点待重试分辨。
- 重试管线：`sentiment7_t3t4_retry.json`（2 臂原式，独立 CSV），等主波 T7-T12 收完再派（并发纪律：≤2 波在飞）。若二败 ⇒ 判结构性，T3 改写/放弃、T4 换 ts_zscore 或去 group_neutralize 重写。
- **06:47 更新**：T7/T8 也双双 ERROR（同文案）——平台拍摆窗口延续（06:38-06:47 间 6 走 6 败，中间仅 T5/T6 一批成功 S 0.49/−0.42）。T8 与已成功的 T5 结构近似同败 ⇒ 再证瞬时故障非表达式。重试池扩为 `sentiment7_err_retry.json`（T3/T4/T7/T8 四臂），等平台稳定后补发；runner 不杀，让 T9-T12 继续掷硬币。

## 九、全波收口：T9-T12 也批双死，重试池扩至 8 臂（2026-11-03 06:5x）
- T9（ts_corr×returns）/T10（ts_decay_linear）同秒双死（0.4s 内），T11（ts_zscore）/T12（跨字段净额 ts_ir）同秒双死——四对批全灭签名一致，文案同为「Please try again」。
- **全波 12 臂定格：4 成 8 败**。成功臂 T1 −0.70 / T2 +0.40 / T5 +0.49 / T6 −0.42，全弱（max|S| 0.70）；snt7 views 族在 DEU 当前骨架下无信号实证面继续薄弱。
- 重试池 `sentiment7_err_retry.json` 扩为 **8 臂**（T3/T4/T7/T8/T9/T10/T11/T12 原式，独立 CSV）；runner（pid 57000）已自然退出，槽位释放。
- 判定纪律不变：批双死签名=平台瞬时故障判别式，二败才判结构性。等干净批（任意 2 臂成功）出现后补发。

## 十、重试批全收：8/8 零 ERROR，瞬时故障定案终证 + views 族浮出 +0.90（2026-11-03 07:1x）
- 07:06 派发 `sentiment7_err_retry.json`（pid 53768 / task snt7retry20261103，独立 CSV），07:1x 全 8 臂落地，**全部 COMPLETE 零 ERROR**（原式一字未改）⇒ 8/8 复活 = 瞬时故障定案的决定性终证（结构性问题不可能全过）。

| 臂 | 机制 | S | TO | 判定 |
|---|---|---|---|---|
| T3 | 回落衰减（backfill−max_diff−现值） | −0.03 | 0.66 | 弱 |
| T4 | 信噪比 ts_quantile | +0.30 | 0.18 | 弱 |
| T7 | 事件计数（>均值天数） | +0.43 | 0.13 | 弱 |
| **T8** | **22 日变化 ts_av_diff** | **+0.90** | 0.60 | 全波最强，TO 偏高 |
| T9 | 量价相关 ts_corr(returns) | +0.13 | 0.19 | 弱 |
| T10 | 衰减信噪比 | +0.55 | **0.11** | 次优，TO 干净 |
| T11 | zscore 回落 | +0.15 | 0.27 | 弱 |
| T12 | 跨字段净差（all_languages−views） | −0.14 | 0.05 | 弱 |

- **views 族修正判定**：主波 4 臂正负混杂判「无方向」，重试批 6 正 2 负 + max **0.90**（超主波最优 0.70）⇒ 有弱信号面（一阶矩/信噪比类几何有效），但距闸 1.58 仍差 75%，**本波不续挖**（资源转 institutions6/fundholdings 强机制面）。T8/T10 记为 views 族最强臂，供跨集迁移参考（sentiment27 POPULARITY_PROXY / news20 密度字段同机制换集，机制×数据集二维律不许跨集封杀）。
- 全波最终账：主波 12 臂（4 成 8 平台故障）+ 重试 8 臂全成 = **20 读数，max 0.90**。snt7（views 计数族）在 DEU/TOP500 判弱收口。

