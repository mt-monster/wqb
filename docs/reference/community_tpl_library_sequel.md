# Alpha 模板手册 · 社区模板库篇（续集）

> 落盘：2026-08-31。来源：用户上传 `alpha模板.docx`（《Alpha模板手册》续篇，社区模板库 TPL 系列，作者 FF56620 原帖的论坛大模型总结）。
> 定位：**人读参考卡**。机器可读候选层在 `data/wqb.db` ledger_kv `KB/community_tpl_kb`（2026-08-31 已合并本册增量），读写协议见 [region_template_kb](../experience/region_template_kb.md)。
> 与第一册（行为经济学模板、官方 Templates & Inspirations）配套使用。

---

## 〇、来源与使用须知

- 原帖：《【Community Leader-因子构造】Alpha模板库：来自社区的馈赠——为你的72变添砖加瓦》（作者 FF56620），共 17 个部分、编号 TPL-001 至 TPL-1700+。
- **效果与风险**：作者实测出货率与 72 变内置模板相当甚至略优；但**部分社区模板存在过拟合风险和语法问题**，经典量价类易触发平台反转成分提示，使用前务必自行回测验证。
- **本工作区硬约束**：全部模板均为 `candidate_unverified`；凡骨架含**幽灵算子**（见 §十八 映射表）的模板，直接提交会整批 ERROR/CANCELLED，必须先换等价算子或实测确认。所有表达式入批前强制过 `tools/expr_lint.py`（REGULAR 83 算子白名单门禁）。
- **占位符规范**：原帖用 `<field/>` 尖括号风格，本工作区 KB 统一用 `{field}` 花括号风格，二者等价。`<field/>`=数据字段、`<d/>`=时间窗口、`<alpha/>`=主信号、`<group/>`=分组（industry/sector/subindustry）、`<ts_op/>`=时序算子、`<vec_op/>`=向量聚合算子。
- 部分编号区间（如 TPL-114120、209220、304320、403420 等）原帖检索未覆盖；◇ 标注处为原帖片段缺失参数。

---

## 一、基础结构模板 (TPL-001 ~ TPL-010)

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-001 | 基本面时序排名 | `<ts_op>(<group_op>(<field/>, <d/>), <group/>)` | ts_op∈{ts_rank,ts_zscore,ts_delta,ts_ir}；group_op∈{group_rank,group_zscore,group_neutralize}；field∈{eps,sales,assets,roe,roa}；d∈{66,126,252}。示例 `group_rank(ts_rank(eps, 252), industry)` |
| TPL-002 | 利润/规模比率 | `<ts_op>(<profit_field/> / <size_field/>, <d/>)` | profit∈{net_income,ebitda,operating_income,gross_profit}；size∈{assets,cap,sales,equity}；d∈{66,126,252} |
| TPL-003 | 向量数据处理（VECTOR 必用） | `<ts_op>(<vec_op>(<vector_field/>), <d/>)` | vec_op∈{vec_avg,vec_sum,vec_max,vec_min,vec_stddev}；anl4_/analyst_/oth41_ 前缀；d∈{22,66,126}。示例 `ts_delta(vec_avg(anl4_eps_mean), 22)` |
| TPL-004 | 双重中性化 | `a = <ts_op>(<field/>, <d/>); a1 = group_neutralize(a, bucket(rank(cap), range="<range/>")); group_neutralize(a1, <group/>)` | range∈{"0.1,1,0.1","0,1,0.1"}；group∈{industry,sector,subindustry} |
| TPL-005 | 回归中性化 | TPL-004 基础上 `b = ts_zscore(cap, <d/>); b1 = group_neutralize(b, <group/>); regression_neut(a2, b1)` | d∈{252,504} 长窗；**注意 `regression_neut` 不在 REGULAR 83 白名单，用前需实测/换替代** |
| TPL-006 | 基本面动量 | `log(ts_mean(<field/>, <d_long/>)) - log(ts_mean(<field/>, <d_short/>))` | anl4_{data}_{stats}；d_short∈{20,44}；d_long∈{44,126}。示例 `log(ts_mean(anl4_eps_mean, 44)) - log(ts_mean(anl4_eps_mean, 20))` |
| TPL-007 | 财报事件驱动 | `event = ts_delta(<fundamental_field/>, -1); if_else(event != 0, <alpha/>, nan)` | 扩展：`if_else(days_from_last_change(<field/>) == <d/>, ts_delta(close, <d/>), nan)` |
| TPL-008 | 标准化回填 | `<ts_op>(winsorize(ts_backfill(<field/>, <d_backfill/>), std=<std/>), <d/>)` | d_backfill∈{115,120,180}；std∈{3,4,5}；d∈{10,22,60}。示例 `ts_decay_linear(-densify(zscore(winsorize(ts_backfill(anl4_adjusted_netincome_ft, 115), std=4))), 10)`（=TPL-1624） |
| TPL-009 | 信号质量分组 | `signal = <ts_op>(<field/>, <d/>); credit_quality = bucket(rank(ts_delay(signal, 1), rate=0), range="<range/>"); group_neutralize(<decay_op>(signal, k=<k/>), credit_quality)` | range="0.2,1,0.2"；decay_op=ts_weighted_decay；k∈{0.5,0.3}。**ts_weighted_decay 未入白名单，需实测** |
| TPL-010 | 复合分组中性化 | `group_neutralize(<alpha/>, densify(<group1/>)*1000 + densify(<group2/>))` | group1∈{subindustry,sector}；group2∈{country,exchange} |

## 二、量价类模板 (TPL-101 ~ TPL-113)

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-101 | 换手率反转 | `-<ts_op>(volume/sharesout, <d/>)` | ts_op∈{ts_mean,ts_rank,ts_std_dev}；d∈{5,22,66} |
| TPL-102 | 量稳换手率 (STR) | `-ts_std_dev(volume/sharesout, <d1/>)/ts_mean(volume/sharesout, <d2/>)` | d1,d2∈{20,22}；优化版外层加 `-group_neutralize(..., bucket(rank(cap), range="0.1,1,0.1"))` |
| TPL-103 | 价格反转 | `-<ts_op>(<price_field/>, <d/>)` | price∈{close,returns,close/open-1,open/ts_delay(close,1)-1}；d∈{3,5,22} |
| TPL-104 | 价格乖离率 | `-(close - ts_mean(close, <d/>))/ts_mean(close, <d/>)` | d∈{5,22,66} |
| TPL-105 | 量价相关性 | `-ts_corr(<price_field/>, <volume_field/>, <d/>)` | price∈{close,returns,abs(returns)}；volume∈{volume,volume/sharesout,adv20}；d∈{22,66,126}。与 T-KB-08 同族 |
| TPL-106 | 跳跃因子 | `-group_neutralize(ts_mean((close/open-1) - log(close/open), <d/>), bucket(rank(cap), range="0.1,1,0.1"))` | d∈{22,30,66}；成交量增强版乘 `ts_rank(volume, 5)` |
| TPL-107 | 指数衰减动量 | `-ts_decay_exp_window(<field/>, <d/>, factor=<f/>)` | ⚠ ts_decay_exp_window 为幽灵算子 → 用 `ts_decay_linear(<field/>, <d/>)` 替代；f 语义（越小衰减越快）对应窗口长短 |
| TPL-108 | 成交量周期函数 (VOC) | `m_minus = ts_mean(volume, <d_long/>) - ts_mean(volume, <d_short/>); delta = (ts_max(...) - m_minus)/(ts_max(...) - ts_min(...)); <w1/>*delta + ts_delay(delta, 1)*<w2/>` | ⚠ ts_max/ts_min 为幽灵算子 → 用 TPL-1601 替代公式；d_long∈{30,66}；d_short∈{10,22}；w1/w2∈{0.33/0.67, 0.5/0.5} |
| TPL-109 | 市场相关性因子 | `mkt_ret = group_mean(returns, 1, market); pt = ts_corr(returns, mkt_ret, <d/>); rank(1/(2*(1-pt)))` | d∈{10,22,66} |
| TPL-110 | 成交量趋势 | `ts_decay_linear(volume/ts_sum(volume, <d_long/>), <d_short/>)` | d_long∈{252,504}；d_short∈{10,22} |
| TPL-111 | VWAP 收益相关 | `returns > -<threshold/> ? ts_ir(ts_corr(ts_returns(vwap, 1), ts_delay(group_neutralize(<field/>, market), <d1/>), <d2/>), <d2/>) : -1` | threshold∈{0.1,0.05}；d1∈{30,60}；d2∈{90,120} |
| TPL-112 | 动量因子创建 | `ts_sum(winsorize(ts_backfill(<data/>, <day/>), std=4.0), <n/>*21) - ts_sum(..., <m/>*21)` | day∈{120,180}；n∈{6,12}；m∈{1,0.1*n} |
| TPL-113 | 线性衰减排名 | `-ts_rank(ts_decay_linear(<field/>, <d1/>), <d2/>)` | d1∈{10,22,150}；d2∈{50,126} |

## 三、情绪/新闻类模板 (TPL-201 ~ TPL-208)

⚠ 本节大量使用幽灵算子 `sigmoid` → 等价替换：`sigmoid(x)` ≈ `multiply(x, inverse(add(1, abs(x))))`（x/(1+|x|)，单调压缩到 (-1,1)），或直接省去压缩层用 `zscore`/`rank`。

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-201 | 情绪差值 | `<ts_op>(rank(ts_backfill(<pos_sent/>, <d/>)) - rank(ts_backfill(<neg_sent/>, <d/>)), <d2/>)` | d∈{20,30} 回填；d2∈{5,22} 比较 |
| TPL-202 | 新闻情绪回归残差 | `sentiment = ts_backfill(ts_delay(<vec_op>(<sent/>, 1), <d1/>); vhat = ts_regression(volume, sentiment, <d2/>); ehat = -ts_regression(returns, vhat, <d3/>); group_rank(ehat, bucket(rank(cap), range="0,1,0.1"))` | sent∈{scl12_sentiment,snt_buzz_ret,nws18_relevance}；d1∈{20,30}；d2∈{120,250}；d3∈{250,750} |
| TPL-203 | 社交媒体情绪 | `rank(<vec_op>(scl12_alltype_buzzvec) * (scl12_sentiment))`；条件版 `trade_when(rank(sent_vol) > 0.95, -zscore(scl12_buzz)*sent_vol, -1)` | 热度极高反向交易 |
| TPL-204 | 条件情绪过滤 | `group_rank(sigmoid(if_else(ts_zscore(<sent/>, <d/>) > <threshold/>, ts_zscore(<sent/>, <d/>), 0)), <group/>)` | d∈{22,30,66}；threshold∈{1,1.5,2} |
| TPL-205 | 情绪+波动率复合 | `log(1 + sigmoid(ts_zscore(<sent/>, <d1/>)) * sigmoid(ts_zscore(<vol/>, <d2/>)))` | vol=option8_*；d∈{30,66} |
| TPL-206 | 指数衰减情绪 | `ts_decay_exp_window(vec_avg(<sent/>), <d/>, <factor/>)`；双源相加 | ⚠ 幽灵 → `ts_decay_linear` 替代；sent∈{mws85_sentiment,nws18_ber}；d∈{10,22} |
| TPL-207 | 新闻结果排名 | `percent = ts_rank(vec_stddev(<news/>), <d1/>); -ts_rank(ts_decay_linear(percent, <d2/>), <d1/>)` | news=nws12_prez_result2；d1∈{50,66}；d2∈{150,252} |
| TPL-208 | 分组行业提取情绪 | `scale(group_extra(ts_sum(sigmoid(ts_backfill(<data/>, <d1/>)), <d2/>) - ts_sum(...), 0.5, densify(industry)))` | d1∈{180,252}；d2∈{3,5}。**group_extra 未入白名单，需实测** |

## 四、期权类模板 (TPL-301 ~ TPL-303)

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-301 | 期权希腊字母差值 | `<group_op>(<put_greek/> - <call_greek/>, <group/>)` | greek∈{delta,gamma,theta,vega} |
| TPL-302 | 期权价格信号 | `group_rank(<ts_op>(<vec_op>(<opt_price/>)/close, <d/>), <group/>)` | ts_op∈{ts_scale,ts_rank,ts_zscore}；d∈{66,120,252} |
| TPL-303 | 期权波动率信号 | `sigmoid(<ts_op>(<opt_high/> - <opt_low/>, <d/>))` | ts_op∈{ts_ir,ts_stddev,ts_zscore,ts_mean}；⚠ sigmoid 幽灵见 §十八 |

## 五、分析师类模板 (TPL-401 ~ TPL-402)

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-401 | 分析师预期变化 | `◇(tail(tail(<field/>, lower=<low/>, upper=<high/>, newval=◇), lower=-<low/>, upper=-<high/>, newval=◇))` | field∈{oth41_s_west_eps_ftm_chg_3m,anl4_eps_chg}；low∈{0.25,0.1}；high∈{1000,100}；外层算子原帖缺失 |
| TPL-402 | 剥离动量的分析师因子 | `afr = <vec_op>(<analyst/>); short_mom = ts_mean(returns - group_mean(returns, 1, market), <d_short/>); long_mom = ts_delay(ts_mean(..., <d_long/>), ◇); regression_neut(regression_neut(afr, short_mom), long_mom)` | d_short∈{5,10}；d_long∈{20,22}。**regression_neut 未入白名单** |

## 六、中性化技术模板 (TPL-501 ~ TPL-502)

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-501 | 市值分组中性化 | `group_neutralize(<alpha/>, bucket(rank(cap), range="<range/>"))` | range∈{"0.1,1,0.1","0,1,0.1"} |
| TPL-502 | 双重中性化（行业+市值） | `a1 = group_neutralize(<alpha/>, bucket(rank(cap), range="<range/>")); group_neutralize(a1, <group/>)` | group∈{industry,sector,subindustry} |

## 七、条件交易模板 (TPL-601 ~ TPL-607)

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-601 | 流动性过滤 | `trade_when(volume > adv20 * <threshold/>, <alpha/>, -1)` | threshold∈{0.618,0.5,1}；反向版 `volume < adv20` |
| TPL-602 | 波动率过滤 | `trade_when(ts_rank(ts_std_dev(returns, <d1/>), <d2/>) < <threshold/>, <alpha/>, -1)` | d1∈{5,10,22}；d2∈{126,180,252}；threshold∈{0.8,0.9} |
| TPL-603 | 极端收益过滤 | `trade_when(abs(returns) < <entry/>, <alpha/>, abs(returns) > <exit/>)` | entry∈{0.075,0.05}；exit∈{0.1,0.095} |
| TPL-607 | 条件排名交易 | `a = <ts_op>(<field/>, <d/>); trade_when(rank(a) > <threshold_high/>, -zscore(<field2/>)*a, -rank(a))` | d∈{25,66}；threshold_low∈{0.03,0.1}；threshold_high∈{0.25,0.5} |

## 八、复合多因子模板 (TPL-701 ~ TPL-707)

- TPL-701 三因子乘积：原帖检索片段截断；完整式见 KB 中 TPL-406（`my_group = market; rank(group_rank(ts_decay_linear(volume/ts_sum(volume, 252), 10), my_group) * group_rank(ts_rank(vec_avg({fundamental}), {d}), my_group) * group_rank(-ts_delta(close, 5), my_group))`）。
- TPL-707 分组 Delta：`group_neutralize(ts_delta(<field/>, <d/>), sector)`；d∈{22,66,126}。

## 九、数据预处理模板 (TPL-801 ~ TPL-807)

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-801 | Winsorize 截断 | `winsorize(<field/>, std=<std/>)` | std∈{3,4,5} |
| TPL-802 | Sigmoid 归一化 | `sigmoid(<ts_op>(<field/>, <d/>))` | ⚠ sigmoid 幽灵见 §十八；d∈{22,66,252} |
| TPL-803 | 数据回填 | `ts_backfill(<field/>, <d/>)` | d∈{115,120,180,252} |
| TPL-804 | 条件替换 | `if_else(is_not_nan(<field/>), <field/>, <alternative/>)` | — |
| TPL-805 | 极端值替换 | `tail(tail(<field/>, lower=<low/>, upper=<high/>, newval=◇), lower=-<low/>, upper=-<high/>, newval=◇)` | low∈{0.25,0.1}；high∈{100,1000} |
| TPL-806 | 组合预处理 | `<ts_op>(winsorize(ts_backfill(<field/>, <d_backfill/>), std=<std/>), <d/>)` | d_backfill∈{120,180}；std=4；d∈{22,66} |
| TPL-807 | ts_min/ts_max 替代 | `ts_backfill(if_else(ts_arg_min(<field/>, <d/>) == 0, <field/>, nan), 120)` | d∈{22,66,126} |

## 十、高级统计模板 (TPL-901 ~ TPL-910)

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-901 | 高阶矩 | `◇(◇(ts_moment(<field/>, <d/>, k=<k/>)))` | k∈{2方差,3偏度,4峰度}；d∈{22,66,126}。**ts_moment 未入 102 算子目录，需实测；平台已验证同类仅 ts_kurtosis(2,2)** |
| TPL-907 | 向量中性化 | `ts_vector_neut(<alpha/>, <risk_factor/>, <d/>)`；分组版 `group_vector_neut(<alpha/>, <risk_factor/>, <group/>)` | ⚠ group_vector_neut/vector_neut 为顾问专属（FORBIDDEN），REGULAR 报 inaccessible；勿用于 REGULAR 批次 |
| TPL-908 | 加权衰减 | `group_neutralize(ts_weighted_decay(<alpha/>, k=<k/>), <group/>)` | k∈{0.3,0.5,0.7}；**ts_weighted_decay 未入白名单，可用 ts_decay_linear 替代** |
| TPL-909 | 回归斜率 | `ts_regression(ts_zscore(<field/>, ◇), ts_step(1), <d/>, rettype=2)` | d∈{252,500}；rettype=2 返回斜率（已验证算子） |
| TPL-910 | 最小最大压缩 | `ts_min_max_cps(<field/>, <d/>, f=<f/>)` ≡ `x - f*(ts_min(x,d) + ts_max(x,d))` | ⚠ ts_min_max_cps 与 ts_min/ts_max 均幽灵；需先实测或放弃 |

## 十一、事件驱动模板 (TPL-1001)

- 数据变化天数：`if_else(days_from_last_change(<field/>) == <days/>, <alpha/>, nan)`；days∈{1,2,5}；alpha 如 `ts_delta(close, 5)`。
- 动态衰减版：`<alpha/> / (1 + days_from_last_change(<field/>))`。

## 十二、信号处理模板 (TPL-1101 ~ TPL-1110)

⚠ 本节除 `signed_power`（已验证）外，其余算子（right_tail/left_tail/clamp/fraction/nan_out/purify/keep/truncate/group_normalize）**均不在平台 102 算子目录**，使用前必须先 `validate_expressions` 实测；`group_normalize` 有已验证等价式：`alpha / group_sum(abs(alpha), group)`（=TPL-1603）。

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-1101 | 黄金比例幂变换 | `signed_power(<alpha/>, 0.618)` | 其他幂次 0.5（平方根）/2（平方增强）✅已验证 |
| TPL-1102 | 尾部截断 | `right_tail(<alpha/>, minimum=<min/>)`；左尾 `left_tail(<alpha/>, maximum=◇)` | min∈{0,0.1} |
| TPL-1103 | Clamp 边界限制 | `clamp(<alpha/>, lower=<low/>, upper=<high/>)` | low∈{-1,-0.5}；high∈{1,0.5}；**可用 tail 近似** |
| TPL-1104 | 分数映射 | `fraction(<alpha/>)` | 映射到分布内相对位置（≈rank 语义） |
| TPL-1105 | NaN 外推 | `nan_out(<field/>, lower=<low/>, upper=<high/>)` | [-3,3]/[-5,5]；**可用 if_else+比较组合等价** |
| TPL-1106 | Purify 数据清洗 | `purify(<field/>)` | 自动清洗 |
| TPL-1107 | 条件保留 | `keep(<field/>, <condition/>, period=◇)` | 原帖参数不完整 |
| TPL-1109 | Truncate 截断 | `truncate(<alpha/>, maxPercent=<percent/>)` | percent∈{0.01,0.05}；设置层 truncation 可替代 |
| TPL-1110 | 组合 Normalize | `group_normalize(<alpha/>, <group/>)` ≡ `alpha / group_sum(abs(alpha), group)` | 等价式全已验证 ✅ |

## 十三、Turnover 控制模板 (TPL-1201)

- `ts_target_tvr_hump(<alpha/>, lambda_min=0, lambda_max=1, target_tvr=<target/>)`；target∈{0.1,0.15,0.2}。✅ 已验证（同族还有 ts_target_tvr_decay，救援武器库常备）。

## 十四、回填与覆盖模板 (TPL-1301 ~ TPL-1305)

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-1301 | 分组回填 | `group_backfill(<field/>, <group/>)` | group∈{sector,industry,market} ✅ |
| TPL-1302 | 嵌套回填排名 | `rank(group_backfill(<field/>, <group/>))` | — |
| TPL-1303 | 覆盖度过滤 | `group_count(is_nan(<field/>), market) > <threshold/> ? <alpha/> : nan` | threshold∈{40,50}；三元写法入表达式须改 if_else |
| TPL-1304 | NaN 替换 | `if_else(is_not_nan(<field/>), <field/>, <default/>)` | default∈{0,0.5,nan} |
| TPL-1305 | 综合数据清洗 | `<ts_op>(winsorize(group_backfill(ts_backfill(<field/>, <d1/>), <group/>), std=<std/>), <d2/>)` | d1∈{120,180}；std=4；d2∈{66,126} |

## 十五、组合提取模板 (TPL-1401 ~ TPL-1405)

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-1401 | group_extra 填补 | `group_extra(<alpha/>, <weight/>, densify(<group/>))` | **group_extra 未入白名单，需实测** |
| TPL-1403 | PnL 反馈 | `if_else(inst_pnl(<alpha/>) > <threshold/>, <alpha/>, nan)` | threshold∈{0,-0.05}；**inst_pnl 未入白名单，需实测** |
| TPL-1404 | 流动性加权 | `<alpha/> * log(volume)` | 仓位偏向高流动性 |
| TPL-1405 | 市值回归中性化 | `regression_neut(<alpha/>, log(cap))` | **regression_neut 未入白名单** |

## 十六、百分位与分位数模板 (TPL-1501 ~ TPL-1505)

| 编号 | 名称 | 骨架 | 参数要点 |
|---|---|---|---|
| TPL-1501 | 时序百分位 | `ts_percentage(<field/>, <d/>, percentage=<p/>)` | ⚠ ts_percentage 幽灵 → **用 `ts_quantile(<field/>, <d/>, <p/>)` 替代（已验证）** |
| TPL-1502 | 分位数 | `<ts_op>(ts_quantile(<field/>, <d/>, <q/>), <d2/>)` | q∈{0.25,0.5,0.75}；d∈{66,126}；d2=22 ✅ |
| TPL-1503 | Max-Min 比率 | `ts_max_diff(<field/>, <d/>) / ts_av_diff(<field/>, <d/>)` | d∈{22,66} ✅ |
| TPL-1504 | 中位数 | `<field/> - ts_median(<field/>, <d/>)` | ⚠ ts_median 幽灵 → **用 `ts_quantile(<field/>, <d/>, 0.5)` 替代** |
| TPL-1505 | 累积乘积 | `ts_product(1 + <ret_field/>, <d/>)` | d∈{5,22,66} ✅ |

## 十七、实战表达式模板 (TPL-1601 ~ TPL-1658)

社区高票帖子实测验证过的表达式格式：

| 编号 | 名称 | 骨架 | 参数/备注 |
|---|---|---|---|
| TPL-1601 | ts_max/ts_min 替代公式 | 等效 ts_max：`{data} - ts_max_diff({data}, {d})`；等效 ts_min：`(({data} - ts_max_diff({data}, {d})) * ts_scale({data}, {d}) - {data}) / (ts_scale({data}, {d}) - 1)` | d∈{22,66,126} ✅ 平台不支持 ts_max/ts_min 时的标准替代 |
| TPL-1607 | 偏度因子 | `-group_rank(ts_skewness(returns, {d}), {group})` | ⚠ ts_skewness 幽灵 → 候选替代 `ts_moment(returns, {d}, k=3)`（需实测）；负偏度股票往往表现更好 |
| TPL-1608 | 熵信号 | `ts_zscore({field}, {d1}) * ts_entropy({field}, {d2})` | ⚠ ts_entropy 幽灵 → 不确定性代理候选 `ts_std_dev`/`ts_kurtosis`（需实测）；d∈{14,22} |
| TPL-1609 | 分析师动量短长差 | `log(ts_mean(anl4_{data}_{stats}, {d_short})) - log(ts_mean(anl4_{data}_{stats}, {d_long}))` | data∈{eps,revenue,netprofit}；stats∈{mean,low,high}；d_short∈{20,44}；d_long∈{44,126}。与 TPL-006 同骨架 ✅ |
| TPL-1623 | 老虎哥回归 | `group_rank(ts_regression(ts_zscore({field1}, {d}), ts_zscore(vec_sum({field2}), {d}), {d}), densify(sector))` | field1=MATRIX(Y)；field2=VECTOR(X)；d∈{252,504} ✅ |
| TPL-1624 | 综合数据清洗 | `ts_decay_linear(-densify(zscore(winsorize(ts_backfill({field}, 115), std=4))), 10)` | 低频字段如 anl4_adjusted_netincome_ft ✅（=TPL-008 实例） |
| TPL-1625 | 延迟最大值位置 | `ts_max({field}, {d}) ≡ ts_delay({field}, ts_arg_max({field}, {d}))` | d∈{22,66}；ts_max 幽灵时的等效写法 ✅ |
| TPL-1641 | ts_entropy 信号检测 | `ts_entropy({field}, {d})` | ⚠ 幽灵；d∈{14,22,66}；高熵=更多随机性 |
| TPL-1642 | 熵+ZScore 组合 | `ts_zscore({field}, {d}) * ts_entropy({field}, {d})` | ⚠ 幽灵；d∈{14,22}；RSI 超买超卖 + 熵不确定性，捕捉修正 |
| TPL-1643 | ts_ir+ts_entropy 组合 | `signal = ts_ir({field}, {d}) + ts_entropy({field}, {d}); group_rank(signal, {group})` | ⚠ ts_entropy 幽灵；d∈{22,66} |
| TPL-1656 | macro 泛化 | `group_rank(ts_delta(ts_zscore({macro_field}, {d1}), {d2}), country)` | d1∈{126,252}；d2∈{5,22}；基于 Labs 分析 macro ✅ |
| TPL-1657 | ASI broker | `signal = group_rank(ts_rank({broker_field}, {d}), market); trade_when(volume > adv20, signal, -1)` | d∈{22,66}；ASI 区域 broker 因子，**需设置 max_trade=ON** ✅ |
| TPL-1658 | Earnings 超预期 | `surprise = (actual_eps - est_eps) / abs(est_eps); group_rank(ts_zscore(surprise, {d}), industry)` | d∈{66,126} ✅（与 GLOBAL/region_kb SUE 模板同族） |

## 十八、幽灵算子 → 已验证等价映射表（本工作区增补，2026-08-31）

数据源 `data/operators_verified.json`（known_ghosts 17 个）+ `tools/expr_lint.py`（REGULAR 83 白名单）。**凡含左列算子的模板骨架，入批前必须替换或实测。**

| 幽灵算子 | 涉及模板 | 已验证等价/替代 |
|---|---|---|
| `sigmoid` | TPL-203/204/205/208/303/802/1635 | `multiply(x, inverse(add(1, abs(x))))`（x/(1+\|x\|)）或直接省去压缩层 |
| `ts_entropy` | TPL-1608/1641/1642/1643 | 无精确等价；代理：`ts_std_dev`/`ts_kurtosis` 度量不确定性（需实测） |
| `ts_skewness` | TPL-1607 | 候选 `ts_moment(x, d, k=3)`（ts_moment 亦未入目录，需实测） |
| `ts_percentage` | TPL-1501/1637/1653 | `ts_quantile(x, d, p)` ✅ |
| `ts_median` | TPL-1504 | `ts_quantile(x, d, 0.5)` ✅ |
| `ts_min` / `ts_max` | TPL-108/910/1625 | TPL-1601 替代公式 ✅；`ts_max ≡ ts_delay(x, ts_arg_max(x, d))` |
| `ts_decay_exp_window` | TPL-107/206/1638 | `ts_decay_linear(x, d)` ✅（语义近似） |
| `ts_min_max_cps` | TPL-910 | 无等价（展开后依赖 ts_min/ts_max，慎用） |
| `group_normalize` | TPL-1110 | `alpha / group_sum(abs(alpha), group)` ✅（=TPL-1603） |
| `tanh` / `s_log_1p` / `neutralize` 等 | — | 见 operators_verified.json known_ghosts 全表 |

**未入 102 目录、状态不明的社区算子**（用前必须 `validate_expressions` 实测）：`regression_neut`、`ts_weighted_decay`、`group_extra`、`inst_pnl`、`ts_moment`、`ts_vector_neut`、`purify`、`fraction`、`nan_out`、`keep`、`truncate`、`clamp`、`right_tail`、`left_tail`。
**FORBIDDEN（REGULAR 不可用）**：`group_vector_neut`、`vector_neut`（顾问专属）。

## 十九、附加模板一：IND 情感数据模板

来源：《【Alpha 模板】基于情感数据的 IND 模板》。

```
S1 = ts_mean(ts_backfill({sentiment}, 250), 22);   # 月平均情感分数
R1 = ts_product(1+returns, 22);                     # 月度收益率（原文注：本应 -1，不影响结果）
alpha = ts_quantile(S1-R1, 5, driver='cauchy');     # 归一化并加重极端值权重（gaussian 也可）
```

- **信号逻辑**：原始情感信号减去市场已 price-in 的收益部分，做多情感分数相对收益高的股票；`{sentiment}` 可换任意 sentiment 字段（API `search='sentiment'` 拉清单）。
- **初始 Setting**：IND / TOP500 / Delay 1 / Decay 10 / Truncation 0.01 / Neutralization Industry / Pasteurization On / NaN Handling Off。
- **社区反馈要点**：① 情感分数与收益率量纲不同直接相减有混信号嫌疑；② 建议拟合 `S1 - k*R1` 剥离 R1 均值回复相关性，或用 if_else 条件替代 R1 步骤；③ sentiment 多为日更，回填 250 天可能太长，可缩短或去掉 ts_backfill；④ 作者建议新手/断粮/点塔时使用；⑤ 经济学参考文献《Tomorrow's Fish and Chip Paper? Slowly incorporated News and the Cross-section of Stock Returns》。
- **算子检查**：ts_mean/ts_backfill/ts_product/ts_quantile 均已验证 ✅（driver 为命名参数）。

## 二十、附加模板二：速度/加速度差分预处理模板

来源：《【alpha模板】有关速度加速度模板的处理》（作者 YZ70114）。

对字段按多周期算一阶差分（速度）与二阶差分（加速度），生成基础字段后套其他算子回测：

```
days = [5, 22, 66, 240]
# 速度: ts_delta(field, day)
# 加速度: ts_delta(ts_delta(field, day), day)
```

社区建议：可嵌入一阶模板联合回测；先做特征筛选（相关性/重要性排序）再取舍；调周期组合（加 10/30 天）、按字段分组（量价字段用不同周期）；顾问建议小回看期试 PV 数据，或以 `days_from_last_change(datafield)` 替换固定 days。

## 二十一、附录：模板群动态管理经验（方法论，已吸收进 GLOBAL/region_kb.methodology）

来源：《【Alpha模板】模板群管理：动态优化淘汰低效模板》。

- 方法：对抽象生成的模板**标记来源**，**统计各模板的 alpha 通过率**，按通过率持续**剔除低效模板**，可细化到数据集层次减少无效回测。
- 效果：优化后每日平均可提交 alpha 通过率约 1%，只需挑选最优者进一步提交。
- 启示：**模板不是越多越好**，建立"模板产出追踪 → 通过率统计 → 动态淘汰"闭环，比盲目堆模板更能提升效率。
- 本工作区落点：对应 `KB/community_tpl_kb` 的 validated/failed 回写协议（见 [region_template_kb](../experience/region_template_kb.md) §4.2）——每次战役回测后把模板区域证据回写，跨区双验证晋升 `KB/template_kb`，长期全 failed 的候选从库中降级/剔除。

---

## 与挖掘流程的集成点（速查）

| 流程环节 | 本册如何介入 |
|---|---|
| S2 GEM priors 注入 | **不进 priors**（候选未实证）；仅经 region_kb.forum_templates/win_recipes 蒸馏后的实证模板进 |
| ra-pipeline 步 4/5 补骨架 | `get_ledger_key("KB", "community_tpl_kb")` 按 category 检索，占位符按 `{field}` 规约替换 |
| Mode B Step B1 找骨架 | 同上；优先 `KB/template_kb`（validated），无匹配再退候选层 |
| 入批前门禁 | 强制 `tools/expr_lint.py`（REGULAR 83 白名单）；§十八 幽灵算子必须先替换 |
| 回测验证后 | 证据回写该模板 validated/failed；≥2 区实证晋升 template_kb（T-KB-NN） |
| 采用审计 | 论坛模板纪律：读完模板必须逐条对照入批或登记"不适用理由"，禁止读完即路过 |
