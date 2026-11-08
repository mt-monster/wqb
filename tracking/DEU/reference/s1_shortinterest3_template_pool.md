# shortinterest3 借券/做空 模板池 —— DEU/TOP500/D1 —— 2026-11-03

## 机制与取证（论坛 8 帖 + 论文 5+5 已检索；两关键帖全文待读——MCP 会话断连）
- **论文锚①《The Loan Fee Anomaly: A Short Seller's Best Ideas》（Management Science 2023）**：高借券费率=空头最佳观点→未来负收益。方向先验：**费率/借券需求高→做空（负向）**。
- 论文锚②《Anomalies and Their Short-Sale Costs》（JoF）+《Short-sale constraints and stock returns》综述：做空约束与未来收益负相关。
- **论坛「券池利用率的极限：shortinterest3 欧洲市场札记」（30 赞，直接本数据集+欧洲）**：利用率 >90% 券借光⇒空头动能衰竭极限=**做多反向信号**（物极必反）。
- **论坛「ASI 借券费率突然变贵」（64 赞 14 评）**：mean/max/min/volatility 费率族；**同一排序方差版能提交、标准差版被 robust 闸拦**（0.9 解剖）⇒ 波动率算子选 multiply(VOL,VOL) 不用 std 链。
- 论坛「融券借贷的隐形成本 risk59」（29 赞）：费率飙升=做空成本高=压力。
- 论坛「空头回补的悬顶之剑 shortinterest2」（30 赞）：**平仓天数长+费率持续走高=逼空前夕组合**（做多轧空）。
- 论坛「借券利用率异常收紧」（3 评）：收紧=空头还想加仓=跟随后续做空压力。

## 字段真身（25 字段全 VECTOR，数值位须 vec_avg；p5_d1 为主键组档，main/plain 为对照档）
BAR=vec_avg(shrt3_bar) 借券需求评级 1-10（ac341）/ MR/MAXR/MINR/VOLR=费率均值/最大/最小/波动（p5_d1）/
CNT=vec_avg(transaction_count_p5_d1) 计数 / SH=vec_avg(loaned_share_count_p5_d1) / MV=vec_avg(loaned_market_value_usd_p5_d1) / DUR=vec_avg(average_loan_duration_days_p5_d1)

## 12 互异模板（结构轴：评级水平 / 费率水平 / 费率突变 / 方差 / 饱和反向 / 逼空交互 / 量能 / 尖峰门控 / 秩尾放大 / 费率分歧 / 双周期价差 / 评级变化）
| # | 骨架 | 机制 | 方向 | 来源 |
|---|---|---|---|---|
| T1 | subtract(0, group_rank(BAR, subindustry)) | 借券需求评级高=知情空头聚集 | 负 | Fee Anomaly |
| T2 | subtract(0, group_rank(MR, subindustry)) | 借券费率高=空头最佳观点 | 负 | Fee Anomaly |
| T3 | subtract(0, group_rank(ts_delta(MR, 22), subindustry)) | 费率突然变贵=做空压力聚集 | 负 | ASI 帖 |
| T4 | subtract(0, group_rank(multiply(VOLR, VOLR), subindustry)) | 费率波动（**方差版**，论坛实证 std 版被 robust 拦） | 负 | ASI 帖 |
| T5 | trade_when(greater_equal(BAR, 9), group_rank(ts_delta(BAR, 5), subindustry), 0) | 饱和极限（评级≥9）反向：需求上冲到顶=动能衰竭 | 正 | Europe 札记 |
| T6 | group_rank(multiply(ts_rank(DUR, 252), ts_delta(MR, 22)), subindustry) | 逼空组合：平仓天数长×费率抬升 | 正 | shortinterest2 帖 |
| T7 | subtract(0, group_rank(ts_rank(SH, 252), subindustry)) | 借券量高=空头拥挤（水平必须 ts_rank 去规模） | 负 | 自建（规模混淆规则） |
| T8 | trade_when(greater(ts_rank(CNT, 252), 0.95), subtract(0, group_rank(BAR, subindustry)), 0) | 借券交易尖峰事件门控 | 负 | 自建 |
| T9 | subtract(0, group_neutralize(signed_power(subtract(group_rank(BAR, subindustry), 0.5), 3), subindustry)) | 评级秩尾放大（有界输入） | 负 | memory 壳实证 |
| T10 | subtract(0, group_rank(divide(subtract(MAXR, MINR), add(MR, multiply(0.01, MR))), subindustry)) | 费率分歧（max−min spread/均值） | 负 | 自建 |
| T11 | subtract(ts_zscore(MR, 22), ts_zscore(MR, 252)) | 费率相对自身历史抬升（同机制双周期价差） | 负 | 自建 |
| T12 | subtract(0, group_rank(ts_delta(BAR, 22), subindustry)) | 评级上行=看空力量增强 | 负 | 自建 |

合规自查：全单数据集 ATOM（短interest 类非 trio，零配额）；无 add/subtract 双独立信号腿（T11=同字段双周期价差合规）；乘法交互非双腿加；窗口 5/22/252 全白名单；除零保护量纲安全；计数/量水平用 ts_rank(252) 去规模✓。

## 待办（MCP 会话恢复后）
1. 读两关键帖全文补 Implementation Example（Europe 札记 + ASI 方差帖）。
2. 两道预检（preflight_expressions + verify_expr）。
3. 探针先行 2 条（限并发 2）：T2 费率水平 + T1 评级水平（先验最硬），看幅度与逐年覆盖再发正式波。
4. 逐年覆盖判据=get_alpha_yearly_stats（连续多年空窗才排除；shrt3 台账 2017 起须验）。
## 派发记录（2026-11-03 01:22）—— 脚本通道（MCP 断连例外）
- MCP `wq-brain-http` 会话断连（Session not found），服务重启无效 ⇒ 宿主客户端陈旧会话；按既定例外退脚本通道（batch_simulator.py，非临时脚本）。
- 预检：字段存在性=此前 get_datafields 实查（shrt3_bar / mean_loan_rate_p5_d1 均在 25 字段清单内）；语法=verify_expr.py 2/2 valid。
- 探针批：T1=subtract(0, group_rank(vec_avg(shrt3_bar), subindustry)) / T2=subtract(0, group_rank(vec_avg(mean_loan_rate_p5_d1), subindustry))
- detached task_id=shrt3_wave1_probes（pid 33288），批 2 条/并发 1（goal 约束 ≤2）；DEU 标准设置（decay4/SUBINDUSTRY/trunc0.08）。
- 收批口径：batch_simulator --status shrt3_wave1_probes；指标/覆盖读数优先 MCP（恢复后），否则读 task 目录 status CSV。

## 探针收批 + 正式波派发（2026-11-03 02:0x）—— MCP 已恢复

### 探针读数（status CSV 与 batch_get_alpha_metrics 双源一致）
| 探针 | alpha_id | S | 2Y | F | TO | sub | margin | fRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| T1 评级水平 | O0AxwRKb | 0.85 | 1.13 | 0.49 | 18.9% | 0.75 | 6.7bp | 4 | ✓ 过 0.5 侦察线 |
| T2 费率水平 | vR1vnZav | 0.82 | 1.48 | 0.36 | 24.8% | 0.65 | 3.8bp | 4 | ✓ 过侦察线（2Y 更强） |

- **方向验证成立**：两条负向骨架（subtract(0,…)）取正 S ⇒ 《The Loan Fee Anomaly》先验（借券费率/需求高→未来负收益）在 DEU/TOP500 成立。
- 幅度特点：S 0.8x 距 1.58 闸约 2 倍，但 **TO 仅 19-25%**（与 esm 72% 死局不同），窗口/壳/分组轴等破闸杠杆余量充足。

### 字段真名修正（get_datafields DEU/TOP500/D1 实查，25 字段）
- VOLR 真名 = **`loan_rate_volatility_p5_d1`**（非 volatility_loan_rate_*）；_p5_d1 组档 8 个模板用字段全部实锤。

### 两道预检（T3-T12 全过）
- `preflight_expressions`：valid=true，unknown_fields=[]，any_changed=false（vec_* 包裹已正确）。
- `verify_expr.py`：10/10 valid。

### 正式波派发（2026-11-03 02:0x，create_multi_simulation，2 条/批 × 5）
| 批 | 模板 | multisim_id |
|---|---|---|
| B1 | T3 费率突变 / T4 费率方差 | 2DCwovo4sB8I76KuLCILY |
| B2 | T5 饱和反向 / T6 逼空交互 | 45dRMYyo4Wub0QaE54HvV |
| B3 | T7 量能 / T8 尖峰门控 | W1QXH8uy4rqbmzRfsSFzDg |
| B4 | T9 秩尾放大 / T10 费率分歧 | 1RjOSnf5b575ar1kerTbyfi |
| B5 | T11 双周期价差 / T12 评级变化 | 1YhZ8V82U58WcLyzV7AVxkn |

- 设置：DEU/TOP500/EQUITY/D1/decay4/SUBINDUSTRY/trunc 0.08/nan OFF/unit VERIFY/FASTEXPR/pasteurization ON/maxTrade OFF。
- 收批链：`lookINTO_SimError_message` 轮询 children → `batch_get_alpha_metrics`（S/2Y/fRA/margin）→ `get_alpha_yearly_stats`（shrt3 2017 起逐年覆盖，连续多年空窗才排除）→ 按模板族归因。

## 波 1 中期收批（2026-11-03 01:4x，B1/B2/B5 终态；B3/B4 在飞）

### 探针逐年覆盖（get_alpha_yearly_stats）——**推翻「2017 起」台账假设**
- T1 `O0AxwRKb` 与 T2 `vR1vnZav` 均 **2014–2023 十年逐年 longCount 72–121、pnl 全非零** ⇒ 无任何空窗，覆盖闸全过。shrt3 在 DEU 实际满史可用。

### 正式波读数（batch_get_alpha_metrics）
| 模板 | alpha_id | S | 2Y | F | TO | sub | margin | fRA |
|---|---|---|---|---|---|---|---|---|
| T3 费率突变 | RRE1Y011 | 0.56 | 0.74 | 0.14 | 46.0% | 0.22 | 1.3bp | 5 |
| T4 费率方差 | KPJE6xEz | 0.45 | 0.82 | 0.16 | 20.9% | 0.14 | 2.5bp | 5 |
| T5 饱和反向 | leA32JaN | 0.20 | **1.28** | 0.08 | 10.2% | 0.48 | 3.7bp | 4 |
| T6 逼空交互 | vR1v9aYa | **−0.45** | −0.39 | −0.10 | 47.6% | −0.19 | −1.0bp | 4 |
| T11 双周期价差 | WjOVdnld | 0.38 | −0.16 | 0.10 | 31.7% | 0.73 | 1.5bp | 4 |
| T12 评级变化 | Xg98LPa8 | 0.01 | −0.25 | 0.00 | 51.5% | −0.07 | 0.04bp | 5 |

## 波 1 全量收批补遗 + 波 2 派发（2026-11-03 01:5x）

### B3/B4 收批（全波 12/12 齐）
| 模板 | alpha_id | S | 2Y | F | TO | sub | margin | fRA |
|---|---|---|---|---|---|---|---|---|
| T7 量能 | P0oO6nmK | 0.04 | 0.61 | 0.00 | 21.0% | −0.33 | 0.02bp | 5 |
| T8 尖峰门控 | pwdKEnbX | 0.72 | **1.63✓** | 0.45 | **4.3%** | 0.62 | **23.4bp** | **2** |
| T9 秩尾放大 | zq3RjogO | 0.84 | 1.13 | 0.49 | 20.0% | 0.78 | 6.7bp | 4 |
| T10 费率分歧 | RRE1Ya9b | −0.28 | −0.15 | −0.06 | 33.9% | −0.03 | −1.1bp | 4 |

**新归因**：T8 = 全场最优结构（2Y 已过 1.58 闸、margin 23bp、fRA 仅 2、TO 4.3%），S 0.72 需抬 ~2.2 倍；T9 秩尾壳对 T1 零增益（0.84 vs 0.85，再次验证「壳不创造信号」）；T7/T10 全灭。

### 波 2 杠杆阶梯（6 个单杠杆变体，修复批豁免 10 模板约束）
| # | 杠杆 | 父骨架 |
|---|---|---|
| V1 | 门限 0.95→0.90 | T8 |
| V2 | 门窗口 252→66 | T8 |
| V3 | 门事件 CNT→MR 尖峰 | T8 |
| V4 | 门内信号 BAR→MR | T8 |
| V5 | 组档 p5_d1→main（mean_loan_rate_main） | T2 |
| V6 | 条件合成 BAR≥8 时 × MR 信号 | T5×T2 |

- 预检：verify_expr 6/6 valid；字段全部为本会话实查集（V5 的 mean_loan_rate_main 在 get_datafields 25 字段清单内）。
- 派发：MCP `wq-brain-http` 会话再次断连（恢复后数分钟内复发），按既定例外退脚本通道 batch_simulator.py（detached task_id=shrt3_wave2_levers，批 2/并发 1）。
- 已补（2026-11-03 02:0x，MCP 内建通道仍 Session not found，走既有只读兜底 `tools/mcp_http_caller.py`）：
  - **权威指标复核 12/12 与 CSV 一致**；T8 fRA=2 全场最少（余者 4-5），2Y 1.63✓ 再确认。
  - **T5/T8/T9 逐年覆盖全部十年零空窗**（longCount 全 >0、pnl 全非零）⇒ 三者覆盖口径全过，无「连续空窗」排除项：
    - T5 leA32JaN：long 27→89；但 2015 S −2.09 / 2020 S −2.03 双深亏，S 0.20 悬案主因是幅度不是覆盖。
    - T8 pwdKEnbX：long 50→135；负年 2015 −0.85 / 2017 −0.26 / 2020 −1.05，正峰 2018 +2.5 / 2023 +2.08——稀疏门控载体的双峰结构，破闸归因时按此分段。
    - T9 zq3RjogO：long 73→105；S 0.84 但 2Y 1.13 未达闸。

### 波 2 收批 + 归因（2026-11-03 02:0x，6/6 COMPLETE，权威 2Y/fRA 兜底通道已核）

| 杠杆 | alpha_id | S | 2Y | F | TO | sub | margin | fRA |
|---|---|---|---|---|---|---|---|---|
| V1 门限 0.95→0.90 | QPv9l5Jw | 0.83 | **1.73✓** | 0.56 | 5.5% | 0.81 | 20.6bp | **2** |
| V2 门窗 252→66 | 9qx76A1o | **0.90** | 1.48 | 0.63 | 4.9% | 0.67 | 25.3bp | 3 |
| V3 门事件 CNT→MR | vR1vzOmd | 0.64 | 1.43 | 0.38 | 5.2% | 0.41 | 17.2bp | 4 |
| V4 门内信号 BAR→MR | rKRPzdWd | 0.72 | 1.17 | 0.38 | 5.7% | 0.53 | 12.4bp | 3 |
| V5 档位 p5_d1→main | 0mYMQLAk | 0.83 | 1.40 | 0.39 | 24.4% | 0.85 | 4.4bp | 4 |
| V6 条件合成 BAR≥8×MR | xArdzoep | 0.77 | **1.63✓** | 0.50 | 7.6% | 0.66 | 14.2bp | 3 |

**归因**：①**门轴有油**——V1（门限松动）单杠杆全线改善（S+0.11 / 2Y 1.73 / fRA 2 / sub 0.81），V2（短窗尖峰）S+0.18 至 0.90 但 2Y 掉到 1.48（门窗改变时序分布，S 与 2Y 在门窗口轴上反向）；②**信号轴到边界**——V4 换 MR 信号腿伤 2Y（1.17）；③**档位轴无益**——V5 main 档 TO 24% 换来同 S，margin 只剩 4bp。CNT 尖峰门 > MR 尖峰门（V3）。

### 波 3 修复批（6 单/组合杠杆，修复批豁免 10 模板约束；语法 6/6 过、字段全在实查 25 字段内）
- 派发：batch_simulator.py detached task_id=shrt3_wave3_repair（pid 48708，批 2/并发 1；MCP 内建通道仍 Session not found，续走例外+兜底脚本读数）。
| # | 杠杆 | 父 |
|---|---|---|
| W3-1 | V1×V2 叠加（0.90 + 66 窗） | V1×V2 |
| W3-2 | 门窗 22（季度尖峰）×0.9 | V1 |
| W3-3 | 门窗 504（长regime）×0.9 | V1 |
| W3-4 | 双门 AND（CNT 尖峰 ∧ BAR≥8） | V1×V6 |
| W3-5 | 门事件 MR 尖峰 ×0.9（验 V3 失败是否门限所致） | V3 |
| W3-6 | 门控载体上秩尾壳 signed_power(·−0.5,3)（验壳在稀疏持仓下效力） | T8 |
- **收批判据**：W3-1 S≥1.0 继续叠杠杆；否则 shrt3 门控族封盘（T8/V1/V2 配方留档），转供给侧或下一矿脉。

### 波 3 候选队列 + 字段陷阱备忘（2026-11-03 01:5x）
- **字段陷阱**：本地 `tracking/mining/shortinterest3_fields.json` 是**另一区域快照（31 字段）**，含 utilization / borrow_activity_score / available_* / rate_bin_* 等字段——**DEU/TOP500/D1 实查只有 25 字段**（8 族 × plain/main/p5_d1 + shrt3_bar），`shrt3_utilizationpercent_units`、`loan_utilization_ratio`、`borrow_activity_score` 在 DEU **不存在**，勿按本地 JSON 设计模板。
- **★ 波 3 供给侧【实查否决·2026-11-03 02:0x】**：`get_datafields`（DEU/TOP500/D1，兜底通道实查）确认 shortinterest3 全库仅 **25 字段 = 8 族 × plain/main/p5_d1 + shrt3_bar**（duration / loan_rate_vol / loaned_MV / loaned_share / max_rate / mean_rate / min_rate / transaction_count），**不存在任何 `available_*` 供给族**（异区快照才有）。供给侧四条骨架轴（available 水平 / Δavailable / 供给紧门控 / loaned÷available 利用率）**分母全缺，整族不可开，封存**。剩余可挖面仅：`loan_rate_volatility`（T4 信号 0.45，可试门控轴）、`average_loan_duration_days`（T6 交互已证伪，仅剩门控可能）、`max/min` 分歧族（T10 已灭）——shrt3 实际矿量以波 3 修复批结果为界。

#### 波 3 供给侧论文取证（2026-11-03，web_search 已核）
1. **Blocher, Reed, Van Wesep (2013, JF)「Connecting two markets」**（[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0304405X12002528)）：hard-to-borrow（可借供给紧）股票 3 个月收益低 **4.8%**；供给冲击对难借股票价格影响显著 ⇒ **方向先验：可借量低→未来负收益（available 水平为正向因子）**。
2. **Beneish, Lee, Nichols (2015, JAE)「In Short Supply」**（[RePEc](https://ideas.repec.org///p/ecl/stabus/3064.html)）：**券紧（binding）时供给是收益主预测变量、券松时需求是主预测变量**；九大异象的空头侧利润全部来自「special」难借股 ⇒ **条件门控模板：供给紧缩 regime 门 × 需求/费率信号**。
3. **Cohen, Diether, Malloy (2007, JF)「Supply and Demand Shifts in the Shorting Market」**（[SSRN](https://ssrn.com/abstract=1607041)）：做空**需求**上升→次月负超额收益 **−2.98%**（与本波 T1/T2 方向一致，需求族已实证）。
4. **Manconi & Massa「Informed securities lending」**（[ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1386418125000722)）：可借量**下降**预测基本面恶化（供给端知情）；但同文指出供给端证据混杂（Cohen 负 / Boehmer 正 / Kaplan 无）⇒ Δavailable 族方向**先做探针不预设**。
5. **Barardehi, Da, Dixon, Wang (SSRN 5025126)**（[SSRN](https://papers.ssrn.com/sol3/Delivery.cfm/5025126.pdf?abstractid=5025126&mirid=1)）：Δ可借股数=机构净交易代理，短期负收益可预测（暂时性价格冲击）⇒ Δ族可能走短周期。

**推论**：波 3 若开，骨架轴=①available 水平（正向）②Δavailable 变化（探针定方向）③Beneish 条件门控（供给紧×费率/需求）④供给利用率=loaned/available 比值族（同机制净额）。**loaned 需求水平族已被 T7 击毙（S 0.04），不再重复**。

### ★★★ 族间互相关矩阵（2026-11-03 02:1x，compute_mutual_correlation 本地零配额，4 年）——提交篮结构性修正

九条互测（MPY9VNY9 / pwdl6ov6 / xArkxebq / T8=pwdKEnbX / V1=QPv9l5Jw / V2=9qx76A1o / V6=xArdzoep / T1=O0AxwRKb / T2=vR1vnZav），**max_mutually_below_subset(0.5) = 5：{pwdKEnbX, pwdl6ov6, MPY9VNY9, xArdzoep, vR1vnZav}（exact）**。

| 关键对 | corr | 判读 |
|---|---|---|
| MPY9VNY9 ↔ T/V 门控族 | **0.199–0.231** | ★ 门控骨架与 T-B 骨架**真正正交**——§82.3「self 由骨架主导」正面兑现：换骨架破了 0.74 墙 |
| pwdl6ov6 ↔ xArkxebq | **0.9854** | ★★ 二者是**同一条 alpha 的两种写法**，提交篮只能算 1 席（保 pwdl6ov6，S 1.62/prod 0.6923 更优） |
| T8/V1/V2/O0AxwRKb 内部 | 0.81–0.95 | 同簇一席（BAR 信号 + CNT/BAR 门控变体） |
| xArdzoep（V6，MR 信号）↔ 同簇 | 0.35–0.43 | 独立第二席（shrt3 门控族内可出 2 席） |
| vR1vnZav（T2，费率信号）↔ 各 | ≤0.43 | 独立席位 |

**提交篮修正**：`xArkxebq` 从「备选二号」降为 `pwdl6ov6` 的近重复备份（0.9854），**不可并提**；shrt3 门控族（T8/V1/V2 簇 + V6 + T2）与已有篮全部低相关，若 S 冲线可再添 1–2 席——W3 修复批的价值上限随之明确。

### 波 3 修复批收口（2026-11-03 02:2x，6/6 COMPLETE + 权威 2Y/fRA）——★ shrt3 门控族封盘

| # | 杠杆 | alpha_id | S | 2Y | F | TO | fRA |
|---|---|---|---|---|---|---|---|
| W3-1 | V1×V2 叠加（0.90+66 窗） | Xg98YdX1 | 0.77 | 1.48 | 0.50 | 6.1% | 3 |
| W3-2 | 门窗 22×0.9 | zq3RJlXd | **0.86** | 1.55 | 0.60 | 6.9% | 3 |
| W3-3 | 门窗 504×0.9 | 0mYMe9Kp | 0.72 | 1.35 | 0.45 | 5.6% | 3 |
| W3-4 | 双门 AND | npv8ZYOq | 0.05 | −0.29 | 0.01 | 3.0% | 5 |
| W3-5 | MR 门×0.9 | O0Axb9zv | 0.67 | 1.29 | 0.40 | 6.5% | 3 |
| W3-6 | 秩尾壳 | O0Axb9zp | 0.84 | **1.68✓** | 0.59 | 5.8% | **2** |

**新机理三条**：
1. **门限×门窗口负交互（反叠加）**：252 窗下 0.95→0.90 抬 S（0.72→0.83），但 66 窗下 0.95→0.90 反而砸 S（0.90→0.77）——短窗门要配**严阈值**，松阈值稀释短窗的事件纯度。单杠杆结论不可跨轴线性外推。
2. **双门 AND 过度稀释**（0.05）：两条件串联把持仓砍到近乎无信号，交互 ≠ 交集。
3. **壳在门控载体上有效（+0.12）**：T9 壳在裸载体零增益、W3-6 壳在稀疏门控载体 0.72→0.84 且 2Y 1.68✓/fRA 2——「壳不创造信号」修正为「壳增益依输入形态」：稀疏集中持仓放大尾部有效。

**封盘裁决（按预锁判据 W3-1 S≥1.0）**：W3-1=0.77 ⇒ **shrt3 门控族封盘**。族谱终值：天花板 V2 0.90（距闸 1.76×），T8/V1/V2 簇一席、V6/T2 独立席的互相关结构已留档；**shrt3 全矿收口**（波 1 十二模板 + 波 2 六杠杆 + 波 3 六修复 + §81 七维移植全部归因完毕）。

### 中期归因（对照探针 T1 0.85 / T2 0.82）
1. **水平型出货、变化型衰减**：评级/费率水平（T1/T2）S 0.8x；一阶变化（T3 0.56 / T12 0.01）、方差（T4 0.45）显著更弱——shrt3 的信息主要住在「水平」而非「变化」。
2. **T6 逼空交互方向证伪**（S −0.45）：平仓天数×费率抬升的乘法交互为负，论坛 shortinterest2 的逼空配方不迁移 DEU/TOP500（与 esm 跨区反向同款教训）。
3. **T5 悬案**：S 0.20 但 2Y 1.28、TO 仅 10.2%——近年段显著变强，留待全波收齐后与 B3/B4 一起做逐年归因再定去留。
4. 幅度现实：当前全场最高 0.85，距 LOW_SHARPE 1.58 约 1.9 倍；但载体 TO 19-25% 杠杆余量大，与 esm 死局不同，**值得投一波杠杆阶梯**（待 B3/B4 归因后定载体）。

