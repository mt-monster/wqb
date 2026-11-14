# GBR delay1 insiders12 GEM Ideas（TOP700 / SUBINDUSTRY / decay4）

**Dataset**: insiders12
**Region**: GBR
**Delay**: 1

数据集：insiders12（7 字段，真信号字段 = insd12_percent / insd12_positionchangetransactionamount / insd12_sharesheld / insd12_mktprice）。六法在线评测 2026-11-14（批 `1nnNiH8w44Rxbwp19oeaIYfv` @NONE/dec0/nanOFF）：
- 法1 覆盖：**insd12_percent 524/700（74%）**、`positionchangetransactionamount` 516/700（74%）——在本塔内**是唯一高覆盖集**（对比 insider_agg_matrix 实测仅 14-24 只）
- 法2 非零：`divide(percent, percent)` 524 = 覆盖同数 ⇒ 零值可忽略
- 法3 频率：percent N=22 变化 **446/524（85%）** ⇒ **日更偏高**；变动额日更
- 形态：`positionchangetransactionamount` **lc/sc = 275/241 天然双边**（自带多空结构，见下）

★关键结构差异（本集最重要）：`insd12_percent` 裸用 **524/0 单边多头**（规模暴露）；`positionchangetransactionamount` 裸用 **275/241 双边**。⇒ 变动额字段天然对称，是主信号首选；percent 须行业中性化后再用。

死路规避：
- 不用 insider_agg_matrix（同塔，实测仅 14-24 只覆盖，S 0.66-0.87 无统计意义）
- 不用 earnings_sent_matrix（实测 14 只）
- 不做长窗平滑（同塔 insider_matrix 实证：ts_mean21 把 TO 从 1.46 压到 0.216 但 2Y 从 1.64 塌到 0.46 ⇒ 内部人信息集中在事件当日，平滑即磨平）
- 不用 ts_zscore 自身历史标准化（insider_matrix 实证：zscore 形式把 S 砍半 1.32→0.66）

文献锚：
- **Lakonishok & Lee (2001, RFS)**：聚合内部人**买入**预测正异常收益；**群聚（multiple insiders within a tight window）信息量最高**；卖出预测力弱（流动性/分散化需求）。
- **Cohen, Malloy & Pomorski (2012, JF)**：预测力**集中在「机会型」交易**（无固定交易模式的内部人），**常规型（Routine, 10b5-1 计划）交易无信息含量**。⇒ 不能用原始买卖总量，须用变化/异常形式。
- Seyhun (1986)：内部人买入的信息含量高于卖出。
- 本法域限制：平台无「常规/机会型」分类字段 ⇒ 用**变化形式**（本次交易额 vs 历史）近似剔除常规交易。

**Concept**: 内部人净交易额（net transaction value）
- **Mechanism**: 内部人净买入额 = 知情交易方向（LLS 2001）；变动额字段天然双边（275/241），不需符号翻转
- **Fields**: `insd12_positionchangetransactionamount`
- **Implementation Example**: `group_rank(ts_sum({insd12_positionchangetransactionamount}, 66), sector)`
- **Direction**: 正
- **expected_exposure**: insider net buying

**Concept**: 内部人买入集中度（cluster intensity）
- **Mechanism**: LLS 2001 群聚模式：短期内多人买入 > 单人大额买入。用变动额的 5 日窗求和再截面排序，捕捉爆发式买入
- **Fields**: `insd12_positionchangetransactionamount`
- **Implementation Example**: `group_rank(ts_sum({insd12_positionchangetransactionamount}, 5), sector)`
- **Direction**: 正
- **expected_exposure**: insider cluster buying

**Concept**: 持仓百分比变化（position percent change）
- **Mechanism**: 内部人持仓占组合比重的变化 = 相对自身规模的加仓强度（剔除绝对金额的规模效应）；CMP 2012 的「机会型」近似代理
- **Fields**: `insd12_percent`
- **Implementation Example**: `group_rank(ts_delta({insd12_percent}, 22), industry)`
- **Direction**: 正
- **expected_exposure**: insider position sizing

**Concept**: 持股水平（shares held level）
- **Mechanism**: 内部人持股水平 = 利益绑定强度（Skin in the game）；高持股内部人的公司治理质量溢价
- **Fields**: `insd12_sharesheld`
- **Implementation Example**: `group_rank(ts_mean({insd12_sharesheld}, 252), industry)`
- **Direction**: 正
- **expected_exposure**: insider alignment level

**Concept**: 交易额相对规模（scaled transaction）
- **Mechanism**: 交易额除以内部人持股基数 = 相对自身仓位的调整幅度（用小仓位表达大信号 vs 大仓位微调）；去掉公司规模效应
- **Fields**: `insd12_positionchangetransactionamount`, `insd12_sharesheld`
- **Implementation Example**: `group_rank(divide(ts_sum({insd12_positionchangetransactionamount}, 66), add(abs(ts_mean({insd12_sharesheld}, 252)), 1)), sector)`
- **Direction**: 正
- **expected_exposure**: relative insider adjustment

**Concept**: 买卖方向一致性（directional consistency）
- **Mechanism**: 连续多期净买入 = 持续信心（>单期爆发）；用 22 日窗口内变动额符号的持续性构造
- **Fields**: `insd12_positionchangetransactionamount`
- **Implementation Example**: `group_rank(ts_mean(divide({insd12_positionchangetransactionamount}, add(abs({insd12_positionchangetransactionamount}), 1)), 22), sector)`
- **Direction**: 正
- **expected_exposure**: persistent insider direction

**Concept**: 卖出冲击（sell pressure，对照臂）
- **Mechanism**: Seyhun 1986：卖出信息含量低于买入，但极端卖出（大额减持）有负向预测力；作为净额信号的对照
- **Fields**: `insd12_positionchangetransactionamount`
- **Implementation Example**: `multiply(-1, group_rank(ts_sum({insd12_positionchangetransactionamount}, 5), sector))`
- **Direction**: 负（对照）
- **expected_exposure**: insider selling pressure

多样性自检：Expected Exposure 6 种 ✓；字段族 2（变动额、percent/sharesheld）✓；分组轴 sector/industry ✓；时间尺度 5/22/66/252 ✓；算子数 3-5 全部 ≤8 ✓。
⚠ 强制检查：每臂须报 lc/sc（本塔已有两个集因覆盖不足被判死），lc/sc < 150 即判覆盖不足。
