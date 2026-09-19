# WorldQuant BRAIN 中文论坛「挖掘经验」总览

> 汇总日期：2026-09-13 ｜ 全部结论来自**中文社区论坛实战帖**，非模型臆测。

## 0. 来源口径（重要前置说明）

⚠️ **本轮为本地语料汇总，非实时抓取**：`wq-brain-http` 的论坛 MCP 工具（`search_forum_posts` / `read_forum_post`）在**本会话不可用**，按 `brain-forum-browse` skill 的纪律不得用浏览器或静态语料"冒充实时论坛"，故本报告**明示为历史快照汇总**。

| 语料 | 规模 | 性质 |
|---|---|---|
| `reports/forum_alpha_research/` | 175 帖检索 → **深读 22 篇**（含评论） | 2026-08-17 MCP 抓取 |
| `reports/forum-experience/alpha_templates_forum_2026-08-05.md` | 50 帖 → **15 个可落地模板** | 2026-08-05 |
| `reports/forum-experience/glb_forum_experience_2026-08-05.md` | 160 命中 → **精读 22 篇** | 2026-08-05 |
| `reports/forum-experience/ppa_forum_experience_2026-08-07.md` | 327 命中 → **精读 42 篇** | 2026-08-07 |
| `brain-alpha-judge/data/forum_corpus/` | **20 篇 GM/PPAC/IQC 原帖** | 2026-04 抓取 |

合计去重后约 **100+ 篇高价值帖**（含 252 赞、216 赞、209 赞、171 赞级头部帖）。

---

## 1. 五条顶层铁律（跨所有语料压倒性共识）

| # | 铁律 | 最强证据 |
|---|---|---|
| ① | **低相关性是最宝贵的资产** | AK76468 实证：corr≈0 的 alpha base **6.07$**；同一人 corr=0.76 的"看起来更好"的 alpha 只有 **1.56$**。§5.3 引 24+ 资深顾问共识 + 官方"相关性越低 quality factor 越高" |
| ② | **ATOM 单数据集 / 单字段** | FL58960（VF 0.67→0.98→0.99）："只做 Single Data Set Alpha，找不到宁愿断粮"；LR93609（PPAC 月度双第一）27 个提交 26 个 PPA **全部 ATOM、无一混信号**，op avg 1–2 |
| ③ | **一阶优先，反对嵌套** | 鼠鼠实证：二阶套二阶使 VF 从 0.9 掉到 0.1，改只跑一阶 + op≤3 后 **VF→0.98、combined→3.13**；FL58960 自述三阶嵌套期 ops 达 **9.x** |
| ④ | **换壳/换方向 > 磨参数** | GLB 帖20、PPA §6.4 共同结论：family 长期卡同一窄区间 = 已进入 crowded neighborhood，继续抛光是无效劳动 |
| ⑤ | **OS 稳定 > IS 亮眼** | MH33574（PPAC 全球第三）：**IS 排名仅 48，靠 OS 稳定拿第三**；IQC 2025 **IS/OS 记分比已达 1:3** |

> LR93609 一句话总结：*"selfcorr 低，combine 就稳健；prodcorr 低，vf 就稳健。"*

---

## 2. 信号构建：模板 / 算子 / 骨架

### 2.1 通用抽象骨架（论坛反复出现的元范式）
```
<group_compare_op>( <diff_op>( <gco>(X_<a>), <gco>(Y_<b>) ), <group> )
```
- 起点范式：`group_rank(ts_rank(eps, 252), industry)`
- **行业中性化残差模板**（90 赞，泛用性最高）：
  `ts_zscore(A, 63) - ts_zscore(group_neutralize(A, sector), 63)`
  三层内涵：剥离时间趋势 → 剥离行业共性 → 保留行业内个体相对差异的纯 Alpha
- 模板简化原则（FL58960）：**只保留最核心 2–3 个操作符**，`op2(op1(field))`；"越简单出货概率越大"

### 2.2 十个一阶模板骨架（LR93609，252 赞，可直接抄）
```python
ts_regression(ts_zscore(a,500), ts_step(1), 500, rettype=2)   # 斜率
ts_delta(ts_delta(a,252)/ts_delay(a,252), 252)                # 增长率
ts_regression(ts_delta(a,252), ts_delta(a,500), 500, rettype=2)# 自回归斜率
ts_mean(signed_power(ts_delta(a,252), 2), 500)                # 平方动量
ts_decay_linear(ts_delta(a,252), 500)                         # 衰减加权动量
reverse(ts_rank(ts_zscore(a,500), 500))                       # 排名反转
log(abs(ts_delta(a,500)) + 1e-6)                              # 对数平滑
signed_power(ts_delta(a,500), 2)                              # 符号保留幂
ts_delta(ts_delta(a,252), 500)                                # 差分层叠
```

### 2.3 分族模板速查（15 个，含 Power Pool 适配度）

| 族 | 代表表达式 | PP 适配 | 关键调参 |
|---|---|---|---|
| 反转 | `-ts_delta(A, 3)`（季频用 **66**，实测 Sharpe 0.5→1.2+） | ★★★ | 窗口、乘波动率 |
| 小而稳 | `-A * ts_std_dev(A, 30)` | ★★★ | 窗口、字段 |
| 期限结构 | `group_zscore(sub(gz(X_fp1,ind), gz(X_fp2,ind)), ind)` | ★★★ | **前缀必须一致** |
| 杜邦 ROE 分解 | `group_zscore(sub(ts_zscore(ROE,d), ts_zscore(margin,d)), ind)` | ★★★ | 窗口、算子 |
| 预期质量 | `if_else(greater(act_q_bps_surprisenum,5), ts_scale(act_q_ebi_surprisestd,60), 0)` | ★★★ | 阈值 3/5/8/10 × 窗口 30/60/90 |
| 波动调整 Z | `divide(ts_zscore(fnd,500), ts_std_dev(ts_zscore(fnd,63),252))` | ★★☆ | 双窗口 |
| 信念熵（ASI broker） | `signed_power(ts_entropy(field,144), 0.618)` | ★★☆ | 熵窗、幂次（**见 §12 矛盾项**） |
| 点亮 RISK | `vector_neut(x, risk70)` / `rank(current_market_cap_usd)` | ★★★ | risk70 多区可用 |
| 点亮 EARNING | `trade_when(ern3_next_interval < x, x, exit_e)` | ★★★ | 财报前清仓 |
| NIP news | `ts_corr(nip_field, returns, ndays)` + FAST neutralization | ★★★ | 短窗更敏捷 |
| 情绪稳定 | `-ts_std_dev(scl12_buzz, 10)` | ★★★ | 窗口 |
| PEG / GGM / 杠杆力 | `-group_zscore(P/E/G-1, industry)` 等 | ★★☆ | 除法 vs 减法差异大 |

> **关键洞察**：EARNING/RISK 类模板与原 ATOM 相关 **0.9+**（"换皮肤"），适合**点塔**或 PC 临界（0.71）时降 PC，但对组合多样化贡献有限。

### 2.4 算子工程要点
- **窗口规范**：`ts_*` 只用 **{5, 22, 66, 126, 255}**（周/月/季/半年/年）
- 鲁棒标准化输入：`zscore(winsorize(pasteurize({field}), std=4.0))`
- `hump(x)` 限制当日与前日变化幅度 → 降换手 + 控回撤；`pasteurize` 源头净化 INF/NaN
- **换 operator 家族比换字段更能扩出独立 alpha**（长窗 decay / 短窗 delta / 横截面 rank 三族轮换）
- 替换降相关：`group_zscore → group_neutralize + signed_power`；`ts_regression → ts_rank + ts_delta`

---

## 3. 相关性治理（论坛最高频主题）

### 3.1 硬闸与隐蔽卡点
- **ProdCorr < 0.7**（regular 硬闸）；**PPA 豁免 ProdCorr**，但受 **Power Pool 相关 ≤0.5** 约束
- ★ **最隐蔽卡点**（JR23144，91 赞）：当 PP 相关 >0.5（如 0.61）时，系统**不直接报 PP 超标**，而是"借用" ProdCorr 名义 FAIL：
  `Prod correlation 0.9311 is above cutoff of 0.7 and Sharpe not better by 10.0%`
  → 提交 PPA 收到 prodCorr FAIL，**先查与现有 PP alpha 的相关是否 >0.5**
- **可提前判定**：`/check` 返回的 `POWER_POOL_CORRELATION` 是**有条件出现**的，IS 阶段就能看够不够 PPA 资格
- 降级机制：PP 检测不过 → 系统按 regular 再判一次

### 3.2 降 PC 四方向（`[36680834830743]`）
调时间窗口（`ts_backfill(x,120)→60/90`；`ts_rank(x,66)→50/70`）｜放宽 winsorize（`std=4→5`）｜非线性变换（`signed_power(scale(x),2)`、`log(x)`）｜强化中性化（`group_neutralize(x, densify(industry))`）。
**组合使用最佳；迭代逐个调，勿一次改太多参数。**

### 3.3 本地预估（省算力神器）
- **本地 self-corr**：累计 PnL **必须先 `diff()` 成每日 PnL 再 `corr()`**，否则得伪相关≈1；分批 10–20 个避免超时
- **ProdCorr 下限预估**（相关性传递不等式），下限 >0.7 直接放弃 check：
  ```
  corr_min = y*know_corr - sqrt(1-know_corr²) * sqrt(1-y²)
  # y = 待检 alpha 与"已知 PC 的 alpha"的 PnL 相关系数
  ```
- **批量监测**：把 PC 写入 alpha 名称 + 颜色标记（<0.6 蓝 / 0.6–0.7 紫 / >0.7 黄），每 3h 循环筛可提交；RA 24h 可检 ~600 个
- **相关性剪枝**（HQ17963）：高相关的 1 阶因子变换后仍高相关 → 按阈值剪枝，USA 153384 个候选可剪去绝大部分

### 3.4 ⚠️ 反直觉：中性化切换不是降 PC 银弹
论坛实证：同一表达式 MARKET `pc=0.65`（过），换 SUBINDUSTRY 反而 `pc=0.72`（超标）。
**本人实证一致**：KOR 单 alpha 改 SUBINDUSTRY 后 0.7668→0.7654，几乎不变。
→ 中性化切档对**单 alpha** PC 影响有限且方向不定；**组合层（SA 10+ 成分）降相关是另一回事**。

---

## 4. Turnover / Fitness / Margin

- **公式**：`Fitness = Sharpe × sqrt(|Returns| / max(Turnover, 0.125))`；`return ≈ turnover × margin`
- **降 TVR 工具箱**（按论坛推荐度排序）：
  | 手段 | 实测 |
  |---|---|
  | `ts_decay_linear(x, n)` | **论坛首推**，n=5/22/44/63，降 30–50% |
  | `ts_target_tvr_decay(x, λmin, λmax, target_tvr)` | 直接定目标，GLB 实测 tvr 1.17%→4.66%/8.14%，同时 PC 0.90→0.77 |
  | `hump` / `ts_target_tvr_hump` | 对 Sub-universe Sharpe 更直接 |
  | `ts_decay_exp_window(signal,10,factor=0.5)` | 保留短期响应，比纯提 decay 更有效 |
  | `tradewhen` | 加开平仓条件 |
  | 增大 decay | 简单但过大破坏信号 |
- **坑**：`ts_target_tvr_decay` 的 `target_tvr` **必须关键字参数**；甜区极窄（~0.65 稳过 returns ratio 0.75，**>0.79 反 HIGH_TURNOVER FAIL**）
- **HTVR 主题**：真正筛子是 **`returns ratio > 0.75`**（非 TVR>20%）；coverage 非 100% 会产生 **5–8% noise turnover**，用短窗 `ts_backfill(3–5)` 或 minimum trade days 门控
- **廉价闸门（PC 等待前）**：Sharpe ≥1.58｜Fitness ≥1.00｜TVR ∈[5%,20%]｜Margin >5bp｜Returns >4%；**近 2 年 Sharpe 必看**（指标漂亮但 2y 不达标 = 信号快失效）
- **IS-Ladder（D1）**：Fail=1.59；2–5年≥2.38；6年≥2.22；7年≥2.06；8年≥1.90；9年≥1.74；10年≥1.59

---

## 5. 中性化（Neutralization）

| 档位 | 适用 / 禁忌 |
|---|---|
| NONE | **基本无法通过 check**，新手避坑 |
| MARKET | 去市场贝塔 |
| SUBINDUSTRY / INDUSTRY / SECTOR / GROUP | 按分组粒度选 |
| FAST neutralization | **不平滑低频信号** → 适合 sentiment / news / nip 类 |

- **新兴市场**（IND/KOR）：MARKET 后仍残留行业暴露 → 叠加 `group_neutralize` 做 double neutralization
- **小盘 universe**（TOP500/MINVOL1M）：SUBINDUSTRY 分组过细样本不足 → **优先 INDUSTRY**
- **GLB 国家偏差**：只做 INDUSTRY 中性化会暴露 country bias → 加 country 分组或用 COUNTRY 中性化；用可视化 "average size by country" 识别偏离
- **提交前必须在目标中性化下重查 corr**

---

## 6. 数据集 / 区域 / 金字塔

- **战役前置体检硬门槛**（不可跳过）：`coverage ≥ 0.85`、`alphaCount ≤ 50`、`fieldCount ≥ 10`
- **区域节奏**：ASI/TWN 起步（数据完备、竞争温和）→ GLB/KOR（字段重叠高、需精细稳健化）→ **EUR（被低估的增长点，TOP2500+STATISTICAL 实测 IS Sharpe 3.6–4.5）**
- **KOR 铁律**：`vector_neut`（风险因子向量中和）；KOR D1 TOP600 SECTOR delay=1 实测 **multiplier 1.7–1.8**
- **六维数据阶梯**（社区非官方统计）：
  | 层级 | 平均 alpha 数 | 平均金字塔 | combinedAlpha | combinedPP |
  |---|---|---|---|---|
  | Expert | 207 | 31 | 0.93 | 0.51 |
  | Master | 257 | 46 | 1.45 | 0.95 |
  | GrandMaster | 318 | 61 | 2.12 | 1.63 |
- ⚠️ **零竞争数据集 ≠ 高价值**：FL58960 明确"Alpha 那一项是 0 就不要考虑"；**甜区是 ac 50–1000**（与本人 `zero_competition_no_signal_v1` 规则完全一致）
- **饱和数据集（≥10K alpha）模板采样已挖穿 → 改"假说优先"**（与本人刚挂接的 `hypothesis_round` 节点同向）
- 数据集推荐：GLB D1 TOP3000 → ANL11 / ANL14_part1-2 / ANL15；PPA USA D1 热门 → option22/23、analyst4/7、fundamental6、news12、model26

---

## 7. 过拟合防护（最重要纪律）

**4 个早期信号**：
1. **Sharpe 随 decay 断崖下跌**（decay=5 即 1.8→0.8）
2. **年份间 Sharpe 方差 > 1.0**（正常 0.3–0.5）
3. **去掉 top/bottom 10% 后 Sharpe 腰斩**（赌 outlier）
4. **相邻两年信号相关性跳变 > 0.4**（训练窗口覆盖独特 regime，只看汇总 Sharpe 看不出）

**提交前验证**：换同类型 datafield（崩了 = 是数据特征在赚钱而非因子逻辑）｜随机打散 stock-level 信号重 rank（不降反升 = 中性化有问题）
**其它**：一阶优先、op avg 1–3；可提交后遍历微调参数，变化大 = 不健壮不提交；覆盖极端行情（VIX 飙升月）需格外谨慎
**易漏的一条**（GY71341）：`trade_when` 类开仓次数过少 = 过拟合风险——"8 年中交易 50 次，其中错 10 次对 40 次，你敢用吗？"大数定理没显现。

---

## 8. PPA / Power Pool 机制

- **PPA 准入门槛**：Sharpe ≥1.0｜唯一 operator ≤8（ts_backfill/group_backfill 不计）｜唯一 field ≤3｜**Power Pool 相关 <0.5**｜TVR/Sub-universe/Robust-universe 必 PASS
- ★★ **PPA 有「轮动区域主题」闸门**：平台按赛季把 PP 开放给某一区域/主题，只有当期活跃区域的 PPA 能提交；非活跃区域提交必报 `does not match any Power Pool Theme`
  - 主题轮动通知看**平台右上角铃铛**（无公开静态时间表）
  - 也可从 `api.worldquantbrain.com/competitions/consultant/boards/power-pool` 推断当前赛季主题
- **PPA 描述三段是硬性要求**（idea / 数据字段 / 操作符），61 赞帖建议用 ChatGPT 生成
- ⚠️ **MCP `submit_alpha` 无法提交 PPA**：它套用常规 RA 闸门（Sharpe>1.3 / Fitness>0.75 / Margin>15bp），对合法 PPA 也照拦，**打 `PowerPoolSelected` 标签后仍不切换** → 合法 PPA 只能走 web UI
- PPA 提交**不检查 prod correlation**，Sharpe>1 且 self corr<0.5 即达标准 → 这是 corr=0 的 alpha base 异常高的机制原因

---

## 9. SuperAlpha / Combine / 组合管理

- **Selection** = 筛选 + 打分函数，按分排序取前 N（Selection Limit 30–100）
- **低 PC 的 SA selection 公式**（GLB 实战）：
  ```
  (1-prod_correlation) × (neutralization ∈ [SLOW/FAST/STATISTICAL/...])
  × (prod_correlation<0.4) × (datafield_count<2) × (prod_correlation>0.27) × (turnover<0.35)
  ```
- **Combo 演进**：等权 `1` → `combo_a(alpha,252,'algo1')` → 多周期 `signed_power(scale(w40)+scale(w160)+scale(w252), 2)`
- **SA 组合公式**：`1 - maxCorr`（自相关减分加权，奖励日收益独立组件，压住 SELF_CORRELATION）；变体 `1-maxCorr²` / `reduce_mean` / 窗口 250–750
- **组合管理四原则**：紧盯 PnL 走势（稳定上涨 + 低回撤）｜把握近期表现（长期好但近期疲软 = 逻辑失效）｜重视 Margin（高 margin = 容量与盈利空间）｜多样化 + Category 均衡
- **每区域至少 20 个 alpha 才稳**；连续稳定提交数月 > 短期爆发
- `prod_corr` 直接写进组合公式目前**论坛无成熟方案**（开放问题）

---

## 10. 收益机制与晋级路径

- **Base 公式（社区推导）**：`倍率 = (金字塔倍率 + 是否吃到2×) × (1 + osrank)`，例 `(1.4+1)×(1+0.82) = 4.36`
- **RA 高收益三要素**：① fitness 过 2+ 门槛 ② osrank 高 ③ **必须吃到 2× theme**
- **主题加成**：IND Analyst 1.9× / Fundamental 2.8×；**HTVR 3×**；活动期叠加可达 2.9×
- **Margin 是拉开排名的关键**：PPAC 全球第 11 实测 Sharpe 1.93 / Returns 10.33% / TVR 4.96% / **Margin 54.42‱** / Fitness 1.70，覆盖 7 个金字塔
- **VF 提升真实路径**（FL58960，0.67→0.98→0.99）：核心动作只有一条 = **只交 Single Data Set Alpha**
- **晋级节奏实例**（HP65370，IQC 后 6 个月 Gold→GM）：7 月 EUR/USA 55 个（一二三阶，最多二阶）→ 8 月 GLB/EUR/ASI 73 个（**舍弃二阶、改一阶模板**）→ 9 月 USA 23 个（**压操作符和字段为主**）
- **升 GM 最难条件 = combine > 2**；金字塔总数也是硬指标（GM 平均 61）

---

## 11. 工程化与自动化

### 11.1 基础设施（HQ17963，Gold→GM 4 个月）
回测器（加载因子列表 + 缓存跳过已回测 + 占满所有槽 + 24h 运行）｜因子信息数据库（30 min 自动更新、多进程 + 缓存）｜**PNL 数据库**（按 id 批量取 PnL，30 min 更新）｜家用 Windows Server（700 元，远程桌面）

### 11.2 方法论工程化（209 赞帖，与本仓方向高度同构）
- 把**约束 / 门槛 / 判定表写成 Agent Skill**，避免每 session 从零开始
- **WebDataScope 的 `Failed RA` / `Failed PPA` 计数是硬门槛**（比 `result=="FAIL"` 更严格）
- 稳健性按**"近 3 年 regime"**判定，不要求 10 年全强
- 饱和数据集（≥10K alpha）改**"假说优先"**
- **幽灵算子守卫**（见 §12）

### 11.3 点塔与复用
- **横向点塔神器**（106 赞）：MCP 一键跨区跨 universe，"横向点塔 → 72 变纵向 → 桥 → 再横向"反复繁衍
- **旧因子再就业**（95 赞）：缓存增量 + 多线程 + 剪枝批量取 region 因子，对负表现因子再处理
- 跨区域映射：`APAC→ASI`、`EMEA→EUR`、`AMER→USA`；优先同 `dataset_id`，否则同 category + 语义搜索；候选字段池 **3–8 个**一次 multiSim 跑完；ASI 必须开 `max_trade=ON`

### 11.4 LLM / Python Alpha
- **分步引导 > 从零生成**：模型提逻辑 → 人工/规则翻译 FastExpr → 模型做语法检查
- **算子幻觉治理**：新对话先让模型"学"`data/operators.csv`（约 66 ops），基本消除幻觉
- **合法性预检**：LLM 输出立刻用 `operators.csv` + `fields.csv` 比对 → 无意义 422 从 ~10% 压到 **<1%**
- **工厂模式省 55–60% token**（已验证信号模板化时，只把"创意环节"交给 LLM）
- **Python Alpha 铁律**：**信号互补性 > 信号强度**——两子信号 Sharpe 1.2/1.0、相关 0.1→0.9 时融合 1.6→1.25；IND 上两 Sharpe 1.0 相关 0.2 融合得 1.4，而两 Sharpe 1.3 相关 0.8 仅得 1.35
- **⚠️ VECTOR 字段 Python Alpha 不能用**（须 `get_datafields(data_type="MATRIX")` 过滤）

---

## 12. ⚠️ 待核验的语料内部矛盾（重要）

**`ts_entropy` / `ts_skewness` / `s_log_1p` 是否为"幽灵算子"？**

| 来源 | 说法 |
|---|---|
| PPA 报告 §6.6（209 赞帖归纳） | "**幽灵算子守卫**：`ts_entropy`/`ts_skewness`/`s_log_1p` 等**平台不存在**，用了静默失败" |
| alpha_templates 报告 T13（94 赞原帖） | `signed_power(ts_entropy(field,144), 0.618)` 是**已验证可用的** ASI broker 点亮模板 |

两份语料直接冲突。**本仓已有权威判据**：`data/operators_verified.json` 的 `verified`（103 个，平台 `get_operators` 实测）+ ledger `KB/community_tpl_kb.ghost_operator_advisory`（10 个 ghost）。→ **建议以本仓对账结果为准，不要用论坛口径**（本仓已于 2026-09-12 完成三表对账并加守护测试）。

**2026-09-13 复核扩大（重要）**：本仓 `platform_constraints.ghost_ops` 实测为
`group_normalize / sigmoid / **ts_decay_exp_window** / **ts_entropy** / ts_max / ts_median / ts_min /
ts_min_max_cps / ts_percentage / **ts_skewness**`（另 `ts_min`/`ts_max` 同时属 inaccessible）。

因此论坛**还有一处误用**：§4 与 GLB 报告 §3.1 都推荐用 **`ts_decay_exp_window(signal,10,factor=0.5)`** 降 turnover —— 该算子在本仓判定中**不存在**，抄用会静默失败。→ 降 turnover 请改用已验证的 `ts_decay_linear` / `hump` / `ts_target_tvr_decay`（后两者亦在 verified 内）。**论坛对降 turnover 的推荐清单里，实际只有 `ts_decay_linear`/`hump`/`trade_when` 可用。**

→ 已把 10 个幽灵算子写入新落地的 `first_order_transform` 族的 `forbidden_operators`，并由
`tests/unit/test_docs_consistency.py::test_template_families_only_use_verified_operators` 守护。

---

## 13. 踩坑清单（合并去重）

| # | 坑 | 来源 |
|---|---|---|
| 1 | self/prod 过了 ≠ 进库：margin / robust / ladder 任一不稳都远未完成 | GLB 帖20 |
| 2 | family prod 长期卡窄区间（如 0.73x）→ **尽早停手**，是 crowded neighborhood | GLB 帖20 |
| 3 | 纯 settings 修法 = 按下葫芦浮起瓢（修 margin 掉 robust，修 robust 冒 ladder）→ 优先怀疑**壳本身**不对 | GLB 帖20 |
| 4 | winner 提交后周围 family 变 self wall → 不做近邻修补，做更远的 field-level move | GLB 帖20 |
| 5 | **warning 不是小问题**：`LOW_ROBUST_UNIVERSE_SHARPE` / `IS_LADDER_SHARPE` 反复卡住 = 结构短板 | GLB 帖20 |
| 6 | submitted 状态有滞后，不要只信一个状态源 | GLB 帖20 |
| 7 | **三阶陷阱**：ops 7.91 拖累晋级；金字塔硬指标不达标；**单一数据集过载**（交太多 fnd 致 USA/EUR/ASI 被禁用 fnd 因子） | vf0.5→0.99 帖 |
| 8 | 路径依赖单一模板 → combine 跌成负数 | Mike/虎哥模板帖 |
| 9 | PPA 不筛选、有就交 → OS 表现很差 | GY71341 |
| 10 | GLB 回测**明显偏慢**（跑了快一天不到 1500）→ 优先低流动性数据集 + multi-sim 批量 | GLB §5.2 |
| 11 | GLB fundamental **低 turnover 陷阱**：长窗 240 的 tvr 仅 0.016–0.07，可能过低影响 osmosis → 用 `ts_target_tvr_decay` 主动拉到 5–10% | GLB §5.2 |
| 12 | PPAC 提交收到 prodCorr FAIL → 真凶常是 **PP 相关 >0.5** | JR23144 |

---

## 14. 与本人 `wqb` 仓库实证的交叉验证

| 论坛结论 | 本人仓库实证 | 判定 |
|---|---|---|
| 零竞争数据集（ac=0）不要碰；甜区 ac 50–1000 | `zero_competition_no_signal_v1` 规则：ac<50 降权 0.15，甜区满分 0.30 | ✅ 完全一致 |
| 中性化切档对单 alpha PC 影响有限且方向不定 | KOR 实测 0.7668→0.7654；"换 neutralization 档位是 SA 最有效差异化手段"（组合层） | ✅ 一致 |
| 饱和数据集（≥10K）模板已挖穿 → 假说优先 | 已挂接 `hypothesis_round` 第 9 节点 + ra-pipeline 步 2 饱和路由 | ✅ 同向，本人已更系统 |
| PPA 有"轮动区域主题"闸门，"OTHER" 非数据集类别 | 实测 `PURE_POWER_POOL_THEME` 当期 "OTHER" 指区域组（KOR/HKG） | ✅ 一致 |
| 换壳/换方向 > 磨参数；结构性失败要早停 | fail-fast 判据已落地（`classify_failure`，2026-09-13） | ✅ 一致，本人已机器化 |
| 幽灵算子清单 | 本仓已有 `operators_verified.verified`(103) + KB advisory(10 ghost) 权威判据 | ⚠️ **论坛口径与本仓冲突，以本仓为准** |
| MCP `submit_alpha` 无法提交 PPA | 已固化进 `worldquant-submit-alpha`「PPA 通道」节 | ✅ 一致 |
| 每区域至少 20 个 alpha 才稳 | 点塔规则：90 天窗口 ACTIVE≥3 点亮；0 亮区域需凑满 3 颗 | 🔶 量级不同（个人经验 vs 点亮机制），不冲突 |

---

## 15. 使用建议

**可直接复用**：§2.2 十个一阶模板骨架、§3.3 本地 PC 下限预估公式、§4 降 TVR 工具箱、§7 过拟合 4 信号、§11.1 基础设施范式。

**需谨慎**：
- §12 的幽灵算子矛盾 → 一律以本仓 `operators_verified.json` 为准
- §10 的 Base 公式是**社区推导**，非平台公开公式
- 所有"推荐数据集"有强时效性（多为 2026-08 前），用前必须 `get_datasets` 复核

**明显缺口（论坛未覆盖）**：PPA 之外的**顾问级硬闸细节**（点塔精确规则、VFT 多样性分数、alpha 退役/DECOMMISSIONED 机制、PPAC 独立日配额）——这些正是本仓相对公开中文资料的信息优势区。

---

*生成的来源均为本地语料快照（非实时 MCP）。原始数据：`reports/forum_alpha_research/{search_results.json, read_posts.json, digest.txt}`、`reports/forum-experience/`（3 份）、`Claude/skills/brain-alpha-judge/data/forum_corpus/`（20 篇原帖 + `references/corpus-manifest.md`）。*

---

## 16. 已落地到本仓的内容（2026-09-13）

| 论坛来源 | 落地形式 | 位置 |
|---|---|---|
| `[31431137051927]`(68 赞) ProdCorr 下限预估 | `prod_corr_lower_bound()` / `should_skip_prod_check()` | `src/wqb/diagnostics.py` |
| `[42018671130391]` 过拟合四信号 | `overfit_signals()`（decay 断崖 / 年际方差 / 去头尾腰斩 / 逐年 corr 跳变） | `src/wqb/diagnostics.py` |
| HQ17963 相关性剪枝 | `iter_prune()`（贪心按指标取、剪掉高相关） | `src/wqb/diagnostics.py` |
| LR93609(252 赞) 一阶模板骨架 | **`first_order_transform` 族**（9 条 `skeleton_variants` + placeholders + 幽灵算子禁用清单） | `wq-brain-campaign-toolkit/config/template_families.json`（8→9 族） |
| 上表四组 | 18 个单元测试 | `tests/unit/test_diagnostics.py`(16) + `test_docs_consistency.py`(2) |

> **未落地（已有等价物，避免重复）**：IS-Ladder 阈值（`src/wqb/store/_schema.py` 已有 `is_ladder_sharpe`）、Sharpe 1.58 门槛（`src/wqb/config.py`）、PPA 准入与 MCP 限制（`worldquant-submit-alpha`「PPA 通道」节）、WebDataScope failed-count 硬门（`mcp_core._slim_checks` 的 `ra` 块）。

### 16.1 一阶变换族落地细节

- **原帖计数勘误**：LR93609 帖称"10 个一阶模板骨架"，但正文实际只列出 **9 条** → 本族按实际 9 条落地（已在 `evidence` 字段注明）。
- **算子核验**：9 条涉及 **12 个算子**（`ts_regression / ts_zscore / ts_step / ts_delta / ts_delay / ts_mean / signed_power / ts_decay_linear / reverse / ts_rank / log / abs`）**全部在 `operators_verified.verified`(103) 内**。
- **防复发**：族内 `forbidden_operators` 显式列出 10 个幽灵/不可访问算子；`mechanism_premise.forbidden_shape` 设为 `zero_inflated / point_mass / ceiling`（离散计数类勿平滑、ceiling 型字段 `log` 有爆炸风险）。
- **守卫**：`test_template_families_only_use_verified_operators` 对**全部 9 个族**的 skeleton/variants 做算子真值校验（实测提取 44 次算子调用，**非真空通过**）。
