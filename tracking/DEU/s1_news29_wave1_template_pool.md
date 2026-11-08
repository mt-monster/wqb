# s1_news29_wave1_template_pool — DEU/TOP500/D1 · Significant Developments Data（news29）

> 状态：探针 6 臂已设计、双预检全过，**待并发槽空出后派发**（当前 oth699 + analyst46 两 runner 占满 2/2）。
> 覆盖注意：get_datafields 全字段 cov=0.0（事件型常态），**覆盖判据以探针逐年 longCount/pnl 为准**（连续多年双零才排除）。

## 一、数据集画像（16 字段全 VECTOR）

| 面 | 字段 | 语义 | 用法 |
|---|---|---|---|
| 事件计数 | 任意事件字段 vec_count | 当日事件条数=注意力密度 | **主信号**（探针 P1/P2/P3/P6） |
| 重要度 | nws29_significance（1=High/2=Med/3=Low） | vec_avg=当日均重要度码 | 信号腿（P4，低码=重要） |
| 显著度 | nws29_frontpage（0/1 头条旗标） | vec_sum=当日头条事件数 | 信号腿（P5 prominence） |
| 分类码 | nws29_topic1/2/3、event_*_topic_code | 事件主题码（须 overlay 解码） | 暂不用（event 禁元素级过滤，聚合后语义丢失） |
| 文本 | company_event_*_text_full | 叙事文本 | 不可用（无数值面） |

禁信号面：无供应商元数据字段（该包干净）。event 型 VECTOR 禁元素级 power/multiply/abs/sign，本模板池只用 vec_count/vec_sum/vec_avg 聚合——合规。
塔混核对：news=非 trio category，单数据集单塔，表达式不含 returns/close 等 PV 内建字段 ⇒ 合规（不占 trio×非trio 配额）。

## 二、机制两读 + 外部文献先验

1. **《从「搜索量」到「新闻密度」》78 赞（43541109631895）**——Da-Engelberg-Gao 2011「In Search of Attention」迁移：异常注意力代理(vec_count) → ts_rank(252) 时序分位 → 反向持仓。GBR 已提交 S 1.97，EUR 迁移 1.60 方向不翻（窗 60 甜点：20<60>120 倒 U）。
   - 关键坑（评论区）：① vec_count 无事件日 0/NaN 语义会污染密度——ts_sum 版才是真密度（有复现者测 ts_sum 版 S 1.7）；② CONCENTRATED_WEIGHT 风险要在表达式层治；③ 拆年看 margin；④ 预定 vs 突发事件过滤可提纯。
2. **《不看幅度看显著性》SNR 模板 107 赞（43179521660823）**——divide(ts_zscore(a,W_long), ts_std_dev(ts_zscore(a,W_short),W_vol)) = t 统计量骨架，USA/GLB/EUR 三市场 S 1.83/1.85/2.59。五延伸：稳健秩/趋势 ts_delta/trade_when 事件对齐/tanh 有界/vec 入口。纪律：**方向由经济先验锁定不参与搜索**。
3. **文献先验**（web_search）：Fang & Peress 2009 低媒体覆盖溢价（低密度→高收益，与反转臂同向）；Barber & Odean 2008 注意力驱动买入；Hillert-Jacobs-Müller 2014 媒体覆盖强化动量（重要事件面动量先验，P4 取动量方向的依据）。

## 三、模板池（正式波 ≥10 结构互异；探针先跑 P1-P6）

| # | 家族 | 骨架 | 窗口 | 方向 | 来源 |
|---|---|---|---|---|---|
| P1/T1 | A 注意力反转 | group_rank(-ts_rank(ts_mean(vec_count(sig),66),252), sub) | 66/252 | 反转 | 照抄臂·78赞帖（60→66 季度白名单映射） |
| P2/T2 | A 注意力反转 | group_rank(-ts_rank(ts_sum(vec_count(sig),66),252), sub) | 66/252 | 反转 | 78赞帖评论修正（NaN 语义开放问题①） |
| P3/T3 | A' 自身基线 | group_rank(-zscore(ts_mean(c,22) vs 504 自身基线), sub) | 22/504 | 反转 | oth699 T2 金型（S 0.84）迁移 |
| P4/T4 | B 重要度 | group_rank(-ts_rank(ts_mean(vec_avg(sig),22),252), sub) | 22/252 | 动量(重要事件漂移) | Hillert 2014 + 78赞帖「预定事件易出动量」（开放问题②） |
| P5/T5 | C prominence | group_rank(-ts_rank(ts_mean(vec_sum(frontpage),66),252), sub) | 66/252 | 反转 | 78赞帖三步模板换代理（frontpage=编辑显著度） |
| P6/T6 | D SNR | group_rank(-divide(ts_zscore(a,66), ts_std_dev(ts_zscore(a,5),22)), sub) | 66/5/22 | 反转 | 107赞 SNR 骨架（Alpha A 窗映射 63→66/33→22） |
| T7 | C' 占比 | group_rank(divide(vec_sum(frontpage), vec_count(sig)), sub) | — | prominence 占比 | 自建（比值>差值纪律） |
| T8 | D' 趋势 | group_rank(-ts_delta(ts_mean(c,22),22), sub) | 22 | 加速度反转 | SNR 延伸二 |
| T9 | E 稳健秩 | group_rank(-ts_rank(ts_delta(ts_mean(c,22),5),252), sub) | 5/252 | 反转 | SNR 延伸一（厚尾治理） |
| T10 | F 峰值衰减 | group_rank(ts_max_diff(ts_mean(c,5),22), sub) | 5/22 | 距峰回落 | ts_max_diff 恒等式（事件面峰值；oth699 T3 教训=水平面勿用峰值） |
| T11 | G 条件化 | trade_when(ts_mean(vec_avg(sig),22)>ts_quantile(ts_mean(vec_avg(sig),22),252), P1_core, -1) | 22/252 | 反转+重要度过滤 | 78赞帖「预定/突发过滤」迁移（trade_when 槽序：条件,核心,-1） |
| T12 | H 新近度 | group_rank(multiply(ts_arg_max(ts_mean(c,22),252),-1), sub) | 22/252 | 峰龄反转 | 自建（ts_arg_max=距峰天数） |

探针 6 臂 = P1-P6（六个机制面各一，单边方向——oth699 实证 ± 臂严格对称，不双跑）。
正式波 12 臂 = T1-T12，探针读数定方向后可翻个别臂的符号。

## 四、开放问题（≥3）

① vec_count 无事件日返回 0 还是 NaN？P1(ts_mean) vs P2(ts_sum) 分位差=覆盖污染幅度。
② 重要事件（低码）是动量还是反转？P4 单边动量先验；若读数为负则翻向再验。
③ news29 全字段 cov=0.0 是事件型常态还是 DEU 真空窗？探针逐年 longCount/pnl 双零判据（≥连续 3 年双零才排除）。
④ 头条旗标是「注意力强度」还是「重要度代理」？P5 vs P4 读数分离两假设。

## 五、PC/SC 占位（提交前必查）

- PC（prod）：未测。
- SC（self）：未测。
- 家族互撞：与 oth699 T2（zscore 自身基线家族）可能同族——P3 若出货须先查互相关。

## 六、探针派发实录

- 双预检：verify_expr 6/6 valid；preflight_expressions valid=true / unknown_fields=[] / platform_field_count=2（nws29_significance + nws29_frontpage 在册）。
- 派发：待并发槽（当前 oth699 pid 68604 余 2 臂 + analyst46 pid 60552 余 6 臂）。

- **已派发**：2026-11-04 pid 66480 / task_id news29_probe_20261104（6 臂探针，batch-size 2 / concurrency 1，runner 2/2 = analyst46 pid 60552 + 本探针）。

- **T12 方向修正（2026-11-03）**：峰龄臂 = 刚到峰(ts_arg_max 小)做空/久未爆发做多（Fang-Peress 低关注溢价）⇒ 信号取 **+ts_arg_max 不取负**（原文档 -1 笔误已改，JSON 草稿按修正版落）。T10 峰值衰减 = 距峰越远做多 ⇒ -ts_max_diff 与原文档一致。
- **正式波 JSON 草稿就绪**：news29_wave1_templates.json（T1-T12；T1-T6=探针 P1-P6，T7-T12 双预检 6/6 全过）。派发前按探针读数定/翻方向后重跑 verify+preflight。

## 七、探针收批归因（6/6 全收 · 2026-11-03）

| 臂 | 面 | S | 结论 |
|---|---|---|---|
| P1 | 照抄密度反转(ts_mean 66) | 0.06 | 弱 |
| P2 | ts_sum 密度反转 | 0.32 | NaN 语义修正方向对（论坛经验复现） |
| P3 | zscore 自身基线(oth699 金型) | -0.02 | **金型不跨数据集——oth699 增益是机制面专属** |
| **P4** | **重要度面(-ts_rank 均码)** | **-0.54** | **翻向 +0.54 全场最强＝重要事件反转（非动量）** |
| P5 | 头条 prominence 反转 | 0.36 | 弱正 |
| P6 | SNR 密度显著性 | 0.18 | 弱 |

**方向定案**：重要度面取 **非负向**（高均码=低重要度事件主导 → 做多）；反转族维持取负。

## 八、正式波 W1-W12 收批归因（2026-11-03，12/12 全落，max|S|=0.76 判弱封盘）

| W | 形态 | S | TO | alpha_id | 读法 |
|---|---|---:|---:|---|---|
| W1 | 密度 zscore 翻转 | -0.07 | 25.0% | RREmLVz1 | 探针 P2 的 0.32 在正式波长窗下耗尽 |
| W2 | 重要度 × zscore 自身基线 | 0.44 | 19.6% | VkxGo6zM | **无 oth699 式跳变**，再次证实金型不跨集 |
| **W3** | **重要度长窗 ts_rank(66/504)** | **0.76** | **6.9%** | RREmX37z | 全场领跑，低换手 |
| W4 | 重要度 SNR | -0.37 | 26.1% | 3qopdblN | 显著性面标准化反而破坏 |
| W5 | 头条占比比值 | 0.11 | 3.0% | RREmX2d0 | 弱正 |
| W6 | 头条 × zscore | -0.01 | 8.0% | 9qxpoaJK | 归零 |
| W7 | 计数 ts_delta(22) | -0.14 | 29.8% | KPJGeG7k | 高换手噪声 |
| W8 | 计数 ts_rank(ts_delta,5) | -0.23 | 28.5% | 0mYpopwp | 高换手噪声 |
| W9 | 计数 ts_max_diff | -0.31 | 55.3% | P0oGe5OJ | 换手爆炸 |
| W10 | 双面 gate 交互 | 0.04 | 4.8% | j2Y6Lar9 | 交互无增益 |
| **W11** | **计数 ts_arg_max(252)** | **0.74** | **4.6%** | d5WZq6XY | 第二领跑，换手极低 |
| W12 | frontpage gate | 0.09 | 7.8% | A1VG65WX | 无增益 |

**模板级归因（三条结构性结论）**：
1. **「重要度水平 × 长窗」是本数据集唯一有效面**（W3 0.76 / W11 0.74），且都靠**低换手（4.6–6.9%）**实现——与 workforce 波「长窗 > 短窗」完全同构，构成 DEU/TOP500 的**慢变量定律**第二条实证。
2. **计数/密度族（W1/W7/W8/W9）在正式波全面转负且换手 25–55%**：探针 P2 密度反转 0.32 是短窗假象，拉长即耗尽 ⇒ 新闻「有多少条」无 alpha，「有多重要」才有微弱 alpha。
3. **frontpage prominence 全线归零（0.11/-0.01/0.09）**：头条位置信息在 DEU/TOP500 无定价残余。

**封盘判定**：max|S|=0.76 < LOW_SHARPE 1.58 的 48%，且最强臂仍属「微弱慢变量」，无破闸路径 ⇒ **news29 判弱封盘**，不追投。

**正式波重设计**（W1-W12）：弃 P1/P3 重跑，换结构升级臂——重要度×zscore 自身基线(W2，探针未测结构=oth699 跳变0.47→0.84 的同构希望)、重要度×SNR(W4)、头条×zscore(W6)、prominence 占比(W5)、双面交互 gate(W12) 等。
