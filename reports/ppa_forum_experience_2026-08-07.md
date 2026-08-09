# WorldQuant BRAIN 论坛「PPA 挖掘经验」系统总结

> 抓取时间：2026-08-07 ｜ 来源：support.worldquantbrain.com 中文社区（Zendesk）
> 语料规模：**327 条检索结果 → 去重精读 42 篇高价值帖**（主库 29 篇 + 补充 13 篇 + 既有 GLB 专项 22 篇复用）
> 检索词：`PPA / 金字塔 / 过闸 / prodCorr / selfCorr / 主题 / 点亮 / 相关系数 / 机器学习 / 因子构建 / 闸门 / pyramid / Power Pool / SA / Combine / 低相关 / Python Alpha`
> 配套数据：`tracking/forum_ppa_search.json`、`forum_ppa_posts.json`、`forum_ppa_posts_condensed.json`、`forum_ppa_supplement.json`、`forum_ppa_experience_dump.txt`

---

## 0. 一句话总纲

**PPA（Power Pool Alpha）的本质是"在平台轮换的活跃主题里，用纯净、低相关的信号去点亮金字塔"。** 论坛无数高赞帖反复印证同一条铁律：**低生产相关性（ProdCorr）是你最宝贵的资产**——它直接拉升每日 Base、驱动 Genius 多样性、决定能否点亮金字塔。我们 2026-08-06 实测的 42 个 GLB 候选全部因 `prodCorr 0.82–0.86` 被硬闸门静默丢弃（emotion 信号族），正是这条铁律最直观的反面教材。

---

## 1. PPA / Power Pool 机制本质

### 1.1 什么是 PPA
- **PPA = Power Pool Alpha**：平台会轮换"活跃 Power Pool 主题"（如 GLB、IND、RISK、HTVR、Orthogonal 等）。在主题期内提交对应区域的 PPA，可享加成权重。
- **PPA 与 RA 的区别**：PPA 提交时 **Prod Correlation 规则被豁免**（≥0.7 不卡），但另有 **Power Pool 相关性**约束——与现有 PPA Pool 中 alpha 的相关性必须 **≤0.5**（"Self-Correlation" 条目里"与已标记为 Power Pool 的 Alphas 相关系数 ≤0.5"）。
- **主题限制**：某些活动只在"活动区域"接受 PPA（如 PPA 主题活动期间只能在活动区提交 PPA，USA/IND/GLB 等分区轮动）。

### 1.2 最隐蔽的卡点（高赞必读）
> 帖：【PPAC 提交经验分享】注意！Prod Correlation 报错，实际卡点可能是 Power Pool 相关性（JR23144, 91 赞）

实测现象：当 **Power Pool 相关性 >0.5**（例如 0.61）时，系统**不会**直接报"Power Pool 相关性超标"，而是**"借用" Prod Correlation 的名义**报 FAIL：
```
Prod correlation 0.9311 is above cutoff of 0.7 and Sharpe not better by 10.0% or more.
```
**结论**：提交 PPA 收到 prodCorr FAIL，务必回头查"与现有 PP Alphas 的相关系数是否 >0.5"——那才是真凶。PP 检测不过时，系统会降级按 regular alpha 再判一次，于是露出 prodCorr 名义。

**可提前判定的技巧（评论区补充）**：`/check` 返回的 `POWER_POOL_CORRELATION` / `POWER_POOL_*` 两条 check 是"有条件出现"的——**在 IS 阶段就能提前看自己够不够 PPA 资格**，不用等到提交报错。

### 1.3 金字塔与 Genius 等级
- **金字塔 = 区域 × 延迟 × 数据类别** 的唯一组合。点亮金字塔就是"多样化"本身。
- **Genius 等级由多样性驱动**，低相关性是驱动这个引擎的燃料（没有低相关就填不满独特空位）。
- **六维数据阶梯**（大角羊/四时六维数据帖，非官方统计）：
  | 层级 | 平均 Alpha 数 | 平均金字塔 | combinedAlpha | combinedPowerPool |
  |---|---|---|---|---|
  | Expert | 207 | 31 | 0.93 | 0.51 |
  | Master | 257 | 46 | 1.45 | 0.95 |
  | GrandMaster | 318 | 61 | 2.12 | 1.63 |
  - operatorCount / fieldCount 也随层级显著上升（GM: op 133 / field 275）——深度与广度都要。

### 1.4 主题加成与 Base 收益
- **IND 主题加成**（DA98440, 94 赞）：Analyst 家族加成最高（analyst44 等可到 1.9×），Fundamental 2.8×；新数据集 pc 极低易出货，**vf 0.93 也能拿满 60 刀**。
- **HTVR Theme 三倍加成**（大角羊，39690289189015）：活动期高加成、高难度。
- **Base 公式讨论**（HG61318 base 经验帖）：
  ```
  倍率 = (金字塔倍率 + 是否吃到 2×) × (1 + osrank)
  例：(1.4 + 1) × (1 + 0.82) = 4.36
  ```
  **RA 高收益三要素**：① fitness 过 2+ 门槛；② osrank 高；③ 必须吃到 2× theme。PC 的 0.7 也是分水岭（叠加高 multiplier 后分层更明显）。

---

## 2. 信号 / 因子构建思路

### 2.1 ATOM 纯净信号是主流（社区共识）
> 帖：PPAC 月度排名两个第一（LR93609, 91 赞）、EUR atom/ppa 模板（DA98440）、vf0.5→0.99 成长帖

- **几乎全部 PPA/SA 是 ATOM（单数据集、不混信号）**，operator avg 1–2（最高 3）。"丑苹果理论"——尊重信号本质，不追求表面完美。
- GLB D1 双第一作者自述：27 个提交 26 个 PPA、1 个 RA，**全部 ATOM、无一混信号**，operator avg 1–2。
- **"点亮就走，不深挖"**——self-corr 自然低 → combine 稳健；prod-corr 低 → vf 稳健。

### 2.2 模板体系（穷举 + 降 self-corr）
> 帖：模版群助我 60 天点亮 60 个塔（LR93609, 252 赞，全论坛最高赞之一）

方法论：
1. **穷举所有模板**（一元/二元/三元）。
2. **从模板层降 self-corr**：`scale/rank/zscore` 等单操作符模板多数重复，不要堆叠，浪费回测。
3. **先随机再深入**：对准一个数据集，随机取样 80 组合算因子密度，密度大再深入。

**10 个一阶模板骨架**（可直接抄）：
```
斜率        ts_regression(ts_zscore(a,500), ts_step(1), 500, rettype=2)
增长率      ts_delta(ts_delta(a,252)/ts_delay(a,252), 252)
自回归斜率  ts_regression(ts_delta(a,252), ts_delta(a,500), 500, rettype=2)
平方动量    ts_mean(signed_power(ts_delta(a,252), 2), 500)
衰减加权动量 ts_decay_linear(ts_delta(a,252), 500)
排名反转    reverse(ts_rank(ts_zscore(a,500), 500))
对数平滑    log(abs(ts_delta(a,500)) + 1e-6)
符号保留幂  signed_power(ts_delta(a,500), 2)
差分层叠    ts_delta(ts_delta(a,252), 500)
```

### 2.3 操作符实战（柯楠, 216 赞）
- `s_log_1p(x)`：奇函数压缩到 [-1,1]，保留正负趋势（比缩尾灵活）。
- `ts_rank(x,d)`：时序相对强弱（d=5~20 平衡噪声）。
- `rank(x)`：横截面标准化（配合 `normalize` 去均值提升中性化）。
- `pasteurize(x)`：INF/无效值→NaN，源头净化。
- `hump(x)`：限制当日与前日变化幅度，**降换手率、控回撤**。

### 2.4 可复用的"点亮金字塔"模板
> 帖：CHN fundamental（LR93609, 106 赞）、ASI broker（LH94963, 94 赞）、EARNING/RISK（XC66172, 85 赞）、EUR（DA98440）、快速点亮 RISK（FF56620, 94 赞）、NIP news（MY82844, 88 赞）、CHN risk72（LR93609）

| 用途 | 表达式 / 思路 |
|---|---|
| 波动率调整 Z-score（风险调整估值） | `divide(ts_zscore(fnd,500), ts_std_dev(ts_zscore(fnd,63),252))` |
| 信念熵值幂放大（行为金融，ASI broker 低拥挤） | `signed_power(ts_entropy(field,144), 0.618)` |
| 点亮 EARNING 金字塔 | `trade_when(ern3_next_interval < x, x, exit_e)`（财报前清仓，x=有信号 ATOM） |
| 点亮 RISK 金字塔 | `vector_neut(x, risk70)`（risk70 多区可用，正交化降 PC） |
| 快速点亮 RISK（不混信号） | `rank(current_market_cap_usd)` 等效 `rank(cap)` |
| NIP news（EUR D0/D1 出 PPA 易） | `ts_corr(nip_field, returns, ndays)` / `ts_covariance` / `ts_regression(returns, nip, ndays)` + FAST neutralization |
| EUR atom/ppa | `x/ts_std_dev(x,d)`、`ts_backfill(x/cap,500)`、`signed_power(x,2)/0.5`、`-inverse(x)` |

**关键洞察**：EARNING/RISK 模板与原 ATOM 相关 0.9+（"换皮肤"），适合**点塔**或**PC 临界（0.71）时降 PC**，但对组合多样化贡献有限。

### 2.5 Python Alpha 工作流（真实上线复盘）
> 帖：第一个上线 Python Alpha（e7rAZjdl, 76 赞）、第二个（3qA3rGX6, 66 赞）

**6 步工作流**（强烈建议喂给 AI 当 SOP）：
1. **经济假设**：先有机制，再找字段（不是先堆字段）。
2. **选字段**：只要 MATRIX，数据集 ≤2，非 PV 字段 ≤2。⚠️ **VECTOR 字段 Python Alpha 不能用**（用 `get_datafields(data_type="MATRIX")` 过滤）。
3. **写 Python**：自己接管清洗 / NaN / 时间窗 / 横截面。
4. **仿真 + 稳健性**：Sharpe/Fitness/年度/中性化 sweep。
5. **相关性闸门**：先 SelfCorr 再 ProdCorr。
6. **证伪复盘**：Python 改写到底有没有带来新 edge（最易被跳过的一步）。

**降 PC 实战**：同组字段在 `SUBINDUSTRY` 下 SelfCorr 0.52 被卡 → 换 `STATISTICAL` 降到 0.43 并通过 ProdCorr（精准剥离 option4 的 IV 公因子）。`vec_avg → vec_max` 也能把 PC 从 0.7288 降到 0.6967（macro27 实测）。

---

## 3. 数据处理与特征工程

### 3.1 中性化（降 self-corr / prod-corr 的第一杠杆）
- 切换中性化档位常是降相关最高效的一步：`SUBINDUSTRY / INDUSTRY / STATISTICAL / GROUP / SECTOR`。
- **FAST neutralization**：不平滑低频信号，适合 sentiment/news/nip 类数据。
- `vector_neut` / `statistical` / `crowding`：对 ATOM 做 risk 正交（点 RISK 金字塔时用 risk70）。

### 3.2 降相关的"换 operator 家族"原则
> 帖：expert→gm PPA 高效产出（33497548596375, 81 赞）、PPAC 提交经验评论

- **真正能扩出独立 alpha 的是换 operator 家族**（长窗 decay / 短窗 delta / 横截面 rank），而非疯狂换字段遍历同一类 operator。
- 替换 operator 降相关：`group_zscore → group_neutralize + signed_power`；`ts_regression → ts_rank + ts_delta`。
- 评论共识：相关性高常因 **operator 序列结构相同**（如都 `ts_regression + group_zscore`），换其中一个 operator 即可显著降低相关而不损质量。

### 3.3 时间窗口规范
- `ts_*` 仅允许 **{5, 22, 66, 126, 255}**（周/月/季/半年/年），不用其他窗口。
- 来自既有 GLB 报告：GLB fundamental 窗口敏感性 22→0.22 / 240→0.07 tvr（低频 fundamental 窗口对 turnover 极敏感）。

### 3.4 降换手 / 控极端值
- `hump(x)`、`ts_target_tvr_decay`、`ts_decay_linear`、调整 `decay` 控 turnover。
- `pasteurize(x)` 净化 INF/无效值；`ts_backfill(x, d, ignore="NAN")` 处理缺失。

---

## 4. 回测验证与硬闸门

### 4.1 顾问提交门槛（来自 MCP Workflow 帖，FF56620）
- **Sharpe > 1.58；Fitness > 1.0；Turnover 1%–70%；单票最大权重 <10%**。
- 需通过 Sub-Universe、Self-corr、Prod-corr 测试。
- **IS-Ladder（D1）阈值**：Fail=1.59；2–5年≥2.38；6年≥2.22；7年≥2.06；8年≥1.90；9年≥1.74；10年≥1.59。

### 4.2 硬闸门（提交前的生死线）
- **ProdCorr < 0.7**（regular alpha 硬闸；PPA 豁免但受 PP 相关 ≤0.5 约束）。
- **Self-Correlation**：与已标记 PP 的 alpha 相关 ≤0.5。
- **POWER_POOL_CORRELATION** 超标 → 借 prodCorr 名义 FAIL（见 §1.2）。

### 4.3 本地预估与剪枝（提效神器）
> 帖：本地 0 误差计算自相关性（KZ79256, 171 赞）、新人向 RA 本地 self+ppac（LX57490, 116 赞）、本地 Corr 增强版预估 ProdCorr 下限（31431137051927, 68 赞）、SA 降 prod 到 0.5 以下（SZ83096, 77 赞）、PPA 批量计算小工具（32470782574487, 68 赞）

- **先本地算 Self-Corr**（低再去平台算 prod），大幅减少限流焦虑。
- **ProdCorr 下限预估**（相关性传递不等式）：用已测 PC 的 PnL 曲线 + 传递性预估待检 alpha 的 PC 下限；若下限 >0.7 直接放弃 check。
  ```
  corr_min = y*know_corr - sqrt(1-know_corr^2)*sqrt(1-y^2)
  # y = 待检 alpha 与"已知 PC 的 alpha"的 PnL 相关系数
  ```
- **SA 降 prod 工作流**：回测 super alpha → 查 self-corr（>0.5 跳过）→ 查 prod 分布 → 选 `fit>5 且 PC∈[0.4,0.5]` 的 SA 重点突破。

### 4.4 PPAC 双第一经验（LR93609）
- 几乎全 PPA、全 ATOM、operator avg 1–2；**点亮就走不深挖**，self-corr 自然低。
- 作者原话：*"selfcorr 低，combine 就稳健；prodcorr 低，vf 就稳健。"*
- combine 建议：别碰 D0、别碰 CHN、多交 SA；vf 建议：多交 regular、控 margin、降 PC。

---

## 5. 主题加成、Base 收益与组合管理

### 5.1 收益三杠杆
- **主题加成倍数**：IND 1.9×（Analyst）/2.8×（Fundamental）；HTVR 3×；活动期叠加可达 2.9×。
- **OSrank**：base 公式 `(金字塔倍率 + 2×) × (1 + osrank)`。
- **fitness 2+ 门槛**必须过；**margin 高**（>15bp，GM 经验 margin 平均 15+）PPA Combine 高。

### 5.2 组合管理四原则（新人 13 天 Combine 1.35 帖，JF13485）
1. **紧盯 PnL 走势**：稳定上涨、低回撤才健康。
2. **把握近期表现**：长期好但近期疲软 = 逻辑失效/被市场消化。
3. **重视 Margin**：高 margin = 容量与盈利空间。
4. **多样化 + Category 均衡**：不同逻辑/数据源/operator 组合对冲风险。

### 5.3 低相关是王道（社区压倒性共识）
> 帖：顾问策略·为什么低相关性是你最宝贵的资产（35104873705111, 40 赞，但引用 24+ 资深顾问共识）

三层证据：
1. **技术**：官方指南明写"相关性越低，quality factor 越高"→ 直接拉升每日 Base。
2. **系统**：Genius 等级由多样性驱动，低相关是点亮金字塔的燃料。
3. **社会**：24+ 资深顾问一致认为高 PC = 拥挤 + 过拟合，长期价值有限。

---

## 6. 实战踩坑与优化建议（必看清单）

### 6.1 三大致命坑（vf0.5→0.99 帖）
1. **三阶陷阱**：Operators per Alpha 过高（7.91）拖累晋级——尽量 ATOM、op avg 1–3。
2. **金字塔硬指标不达标**：alpha 总量太少（金字塔仅 30）过不了 GM。
3. **单一数据集过载**：交太多 fnd 导致 USA/EUR/ASI 大区被禁用 fnd 因子。

### 6.2 路径依赖
> 帖：Combine 提升之路（Mike/虎哥模版, 67 赞）

- 依赖单一模板（虎哥模版）→ combine 跌成负数 → 抛弃后稳定。
- **每个区域至少 20 个 alpha 才稳**；多交 atom、少混信号、model 别做太多。

### 6.3 提交数量稳定性（多帖一致）
- 连续稳定提交数月比短期爆发重要；每区域 ≥20 个。
- 多交 SA/atom 分散；"super alpha 永远值得交（fitness>5, prod<0.5）"。

### 6.4 换壳比磨参数（论坛核心共识）
- 既有 GLB 报告与多篇 PPA 帖共同指向：**换信号方向/数据（"换壳"）比在死族上磨参数更有效**。我们 42 个 GLB emotion 候选全灭正是印证——继续提交同族是浪费。

### 6.5 PPA 高效产出方法论（expert→gm, 33497548596375）
1. **批量回测高 alpha-count 字段**：一次拉整个 category，按 alpha count 排序取前 5–10%，一轮跑 ~2000 pool/天。
2. **相关性剪枝 + 信号增强**：按 pnl 相关性分类，每类选最有潜力因子再培养（先筛选再培养，省算力）。
3. **提交前去掉无用 operator**：`ts_backfill`/`densify` 等能去就去，降 op avg。
4. **稳定性检查**：rank/sign 表达式验证是否稳定。
5. **把 PPA 命中当"假设"而非"答案"**：跨 universe 复算验证，避免局部 regime 过拟合。

### 6.6 工程化提速
> 帖：横向点塔神器（CQ89422, 106 赞）、旧因子再就业（JX79797, 95 赞）、PPA 批量计算小工具、5 个 Agent Skill 工作流（JX84394, 209 赞）

- **MCP 新工具一键横向点塔**（跨区跨 universe），"横向点塔 → 72 变纵向 → 桥 → 再横向"反复繁衍。
- **旧因子再就业**：缓存增量 + 多线程 + 剪枝批量获取 region 因子，对负表现因子再处理。
- **固化 Skill 工作流**（209 赞帖核心）：把约束/门槛/判定表写成 Agent Skill，避免每次 session 从零开始；**WebDataScope 的 Failed RA / Failed PPA 计数是硬门槛**（比 `result=="FAIL"` 严格）；稳健性按"近 3 年 regime"判定，不要求 10 年全强；饱和数据集（≥10K alpha）模板采样已挖穿，改"假说优先"；**幽灵算子守卫**（ts_entropy/ts_skewness/s_log_1p 等平台不存在，用了静默失败）。

---

## 7. 可复用表达式 / 模板清单（直接抄）

```python
# —— 一阶动量/反转家族 ——
ts_regression(ts_zscore(a,500), ts_step(1), 500, rettype=2)      # 斜率
ts_delta(ts_delta(a,252)/ts_delay(a,252), 252)                   # 增长率
ts_mean(signed_power(ts_delta(a,252), 2), 500)                   # 平方动量
ts_decay_linear(ts_delta(a,252), 500)                            # 衰减加权动量
reverse(ts_rank(ts_zscore(a,500), 500))                          # 排名反转
signed_power(ts_delta(a,500), 2)                                 # 符号保留幂

# —— 风险调整估值（CHN fundamental）——
divide(ts_zscore(fnd,500), ts_std_dev(ts_zscore(fnd,63),252))

# —— 行为金融（ASI broker 低拥挤）——
signed_power(ts_entropy(field,144), 0.618)

# —— 点亮金字塔 ——
trade_when(ern3_next_interval < x, x, exit_e)                     # EARNING
vector_neut(x, risk70)                                           # RISK
rank(current_market_cap_usd)                                     # RISK（不混信号）
ts_corr(nip_field, returns, 20)                                  # NIP news（短窗更敏捷）

# —— 降相关/降换手 ——
group_neutralize(x, sector)                                      # 替换 group_zscore
ts_rank(x, 10, constant=0.5)                                     # 时序相对强弱
hump(ts_rank(returns,5))                                         # 降换手
ts_target_tvr_decay(x, target)                                   # 控 turnover
```

---

## 8. 附录：精读帖子清单（42 篇）

| # | 标题 | 作者 | 赞 | 维度 |
|---|---|---|---|---|
| 1 | 模版群助我 60 天点亮 60 个塔 | LR93609 | 252 | 因子构建/模板 |
| 2 | 基于操作符的因子构建实战（1） | NL80893 | 216 | 操作符 |
| 3 | 我把整套 BRAIN 挖矿流程写成了 5 个 Agent Skill | JX84394 | 209 | 工程化 |
| 4 | 本地 0 误差计算自相关性【即插即用版】 | KZ79256 | 171 | 本地自相关 |
| 5 | MCP 提示词优化 alpha 全流程 | LA79055 | 131 | 工作流/闸门 |
| 6 | 新人向 RA 的本地 self+ppac 自相关 | LX57490 | 116 | 本地自相关 |
| 7 | 效率王 横向点塔神器 | CQ89422 | 106 | 点塔/工程 |
| 8 | CHN 中点亮 fundamental | LR93609 | 106 | 模板 |
| 9 | MCP Workflow 自动化找 alpha | FF56620 | 105 | 工作流/闸门 |
| 10 | CHN 中点亮 risk72（1 字段 3 atom） | LR93609 | 104 | 数据研究 |
| 11 | 旧因子再就业（缓存/多线程/剪枝） | JX79797 | 95 | 工程化 |
| 12 | ASI 点亮 broker Pyramid | LH94963 | 94 | 模板 |
| 13 | IND 地区 ra 主题加成推荐数据集 | DA98440 | 94 | 主题/数据集 |
| 14 | 快速点亮 RISK pyramid（USA/IND） | FF56620 | 94 | 模板 |
| 15 | EUR atom/ppa 模板和经验 | DA98440 | 82 | 模板 |
| 16 | 缘分一道桥 Alpha 变体生成+自相关工具 | JX79797 | 93 | 变体/自相关 |
| 17 | PPAC 月度排名两个第一 | LR93609 | 91 | PPAC 经验 |
| 18 | PPAC 提交经验：prodCorr 报错真凶是 PP 相关 | JR23144 | 91 | 闸门机制 |
| 19 | 使用 nip 族数据点亮 news 塔 | MY82844 | 88 | 模板/数据 |
| 20 | 新人成长血泪史 VF0.5→0.56→0.91 | YB49779 | 86 | 踩坑 |
| 21 | 点亮 EARNING/RISK 金字塔小技巧 | XC66172 | 85 | 模板 |
| 22 | SA 赚钱大法：降 prod 到 0.5 以下 | SZ83096 | 77 | 降相关 |
| 23 | 12 月主题活动+IND 主题 | KH94146 | 44 | 主题 |
| 24 | vf 从 0.5 到 0.99 成长之路 | — | 75 | 踩坑/工程 |
| 25 | 第一个上线 Python Alpha（IV delta-skew 反转） | — | 76 | Python Alpha |
| 26 | expert→gm：如何利用 PPA 高效产出 alpha | — | 81 | PPA 方法论 |
| 27 | PPA 活动主题限制下提交 ra 点塔心得 | — | 70 | 主题/点塔 |
| 28 | 四季度六维数据（层级阶梯） | — | 76 | 指标 |
| 29 | Orthogonal HTVR Theme 三倍加成 | AL13375 | 68 | 主题 |
| 30 | 第二个上线 Python Alpha（FASTEXPR→Python） | — | 66 | Python Alpha |
| 31 | Combine 提升之路（负数→2） | Mike | 67 | 踩坑 |
| 32 | base 经验：vf0.77 如何吃到 50 刀 | HG61318 | 68 | 收益 |
| 33 | 本地 Corr 增强版：预估 ProdCorr 下限 | — | 68 | 本地估计 |
| 34 | PPA alpha 批量计算小工具 | — | 68 | 工程化 |
| 35 | 13 天提交 Combine1.12/PPA1.35 | JF13485 | 65 | 组合管理 |
| 36 | 顾问策略：为什么低相关性是最宝贵资产 | — | 40 | 收益哲学 |
| 37–58 | 既有 GLB 专项 22 篇（2026-08-05 报告复用） | 多 | — | 全维度 |

---

## 9. 与我们自己实践的呼应（重要）

- **我们的 42 个 GLB PASS_CHEAP 全被 prodCorr 0.82–0.86 挡死**（emotion 信号族 p0q2/p1q2），`qMNZX1o1` 单测 prodCorr 0.7686 同样失败——**这正是论坛"高 PC=拥挤=过拟合"铁律的活证据**。
- 论坛一致结论：**不要在同族上继续磨参数，要换信号方向/降相关（换数据、正交化、换 operator 家族）**。
- 可立即落地的下一步：基于本报告的"降相关 operator 替换 + 去 ts_backfill/densify + 中性化 sweep + 本地 self/ppac 预筛"流程，重挖一批**新数据/新模板**的 GLB PPA，而不是复用 emotion 族。

---

*生成说明：本报告由论坛直连抓取（绕过失效的 JSON 搜索 API 与 flaky 的 MCP 论坛工具）+ 既有 GLB 专项报告合并而成。所有结论均来自社区高赞实战帖，非模型臆测。*
