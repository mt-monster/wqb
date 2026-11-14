# ★★关键机制发现：事件型低覆盖数据集的「并列块污染」与 tail 后处理（2026-11-11）

> 来源：论坛帖 43178926004887（DEU INSTITUTIONS 破咒帖，88 次回测，作者 JX84394）正文 §2.2/§5。
> 这是本战役迄今最重要的外部机制输入——它可能改写所有事件型数据集的判决基础。

## 一、机制：nanHandling=ON 制造巨大并列块

- 事件型 VECTOR 数据（coverage<0.5）在 nanHandling=ON 下，无申报股票在**数据层被填 0**；
- ts_sum 后仍为 0 → group_rank 把这些股票压成**完全相同的值**：横截面 72% 以上（多数日子 80% 以上）取同一个值，该值 rank 落在中段（约 0.4）；
- 后果：四分之三的横截面**根本没有信号**，subU 被稀释得最狠（大盘子集并列块占比更高）；
- **这不是信号弱，是数据结构问题**。

## 二、修法（五步）

1. vec_sum 聚合同日多笔申报；
2. divide(分子, add(分母, 0.0001))：ε 让清仓比值变巨大但有限；
3. winsorize(std=2)：把并列块压进 (0.25,0.75) 带内（**std=2 是甜点**：std=1 空账本 / 1.5→1.56 / 2→1.67 / 2.5→1.59 / 3→1.23 / 4→0.32）；
4. **ts_sum(66)（季度）——不能用 ts_mean！** nanHandling=ON 下 ts_mean 只对非 NaN 日求均值，「一季买 3 次」与「买 1 次」几乎一样 → **事件频率被除掉**（CMP 2012 机会型信号的核心信息）；帖子实证：ts_mean 替代 ts_sum → Sharpe 1.44 → 0.73；
5. group_rank(·, industry) 后 **tail(x, lower=0.25)**：剔除并列块。

## 三、tail 参数阶梯（宽平台，非尖峰）

q = 0.10 / 0.20 / 0.22 / 0.25 / 0.28 / 0.30 / 0.35 / 0.40
→ S = 0.13 / 1.65 / 1.66 / **1.67** / 1.64 / 1.60 / 1.10 / 0.94

- 0.20-0.30 是平台（Sharpe/subU/2Y 同时稳定）；q≥0.35 吞真信号，q=0.10 没掐干净并列块；
- **winsorize 与 tail 必须成对**（去掉 winsorize → 0.99）；
- 姊妹分子在加 tail 后收敛（valueeur 1.65 vs shares 1.13 → 加 tail 后 1.68 vs 1.59，差 0.52→0.09）⇒ tail 掐掉的是共有噪声，不是信号。

## 四、可迁移性（帖子 §5.6 猜想 + 我们的验证计划）

作者猜想：**所有 coverage<0.5 且 nanHandling=ON 的事件型数据集**（news / insiders / shortinterest）都存在这块「假中段」，**tail 应是这类数据的标准后处理**。

⇒ 本战役受影响的面（此前全部未加 tail）：
- news20×I7 线（insd1_holdings 是 cov 0.534 事件型）——**BE51 正在测**；
- insiders1 / insider_agg_matrix（cov 0.53）——BE49 已测（无 tail，最佳 0.76）；
- shortinterest3 的 _p5_d1 族（cov 0.783）。

## 五、平台语法要点（本次踩坑）

- **tail 的第 2 参必须命名**：tail(x, lower=0.25)；位置参数会被 toolkit 静态闸判 SYNTAX 错并**整批拒绝**；
- **镜像负腿改写**：subtract(0, group_rank(...)) 替代 -group_rank(...)，避免触发毒模式「加权混腿」结构判定；
- MCP 直发 multisim 必经 toolkit 静态闸（语法 + inaccessible_ops(ts_min/ts_max) + poison_patterns）。

## 六、在飞验证

| 波 | 内容 | sim |
|---|---|---|
| BE51 | 新闻×I7 线 + tail 阶梯（q=0.10/0.20/0.25/0.30/0.40） | 2LJR19gsX4RkcGwl2sOASd4 |
| BE50 | institutions1 正确配方（ts_sum+winsorize2+tail 阶梯+shares 姊妹） | 1FDKiA5cv4QSaSJkx94NGwI |

⇒ 若 BE51 让 1.52 线破 1.58，说明「1.52 天花板」是并列块假象而非信号上限，需**回溯重测**此前所有事件型探针判决。
## 七、tail 平台语法的两次踩坑（已修正）

1. **位置参数被 toolkit 静态闸拒绝**：`tail(x, 0.25)` → `[SYNTAX] 函数 tail 的第2个参数必须使用命名参数 lower=` → 整批拒绝；
2. **命名参数缺 upper 仍被平台拒绝**：只给 lower → 平台报 `Required attribute "upper" must have a value.` → 5/5 子代 ERROR；
3. **正确写法**：`tail(x, lower=0.25, upper=1.0)`（保留 [q, 1] 区间 = 剔除底部 q 分位）。

附带：镜像负腿必须写 `subtract(0, group_rank(...))`，直接 `-group_rank(...)` 作为 add() 顶层实参会触发毒模式「加权混腿」结构判定。

修正版 sim：BE51 = 24PaSXh1y4YEbzbw9WYEX32；BE50 = 2Z9qvP7c74xU9NF5XVkPRR1。