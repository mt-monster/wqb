# EUR S0 扫描：Institutions category（2026-11-09，goal eur15 启动波）

> 数据源：MCP 实时（authenticate / get_pyramid_alphas / get_datasets / get_datafields，均 2026-11-09 11:2x 拉取）。
> 口径：目标=15 颗本战役新挖验证的 REGULAR alpha；只算 goal 启动（2026-11-09 11:19）后新仿真验证的件，存量不计。

## 一、EUR D1 塔点亮表（本季度实时，get_pyramid_alphas）

| category | 已提交数 | 状态 | 选集资格 |
|---|---:|---|---|
| analyst | 10 | ★已点亮 | ❌ 排除（含 analyst7——旧组合载体禁用于新波） |
| model | 3 | ★已点亮 | ❌ 排除 |
| fundamental | 3 | ★已点亮 | ❌ 排除 |
| imbalance | 3 | ★已点亮 | ❌ 排除 |
| **institutions** | **0** | 未点亮 | ✅ 本波目标（×1.1） |
| earnings | 0 | 未点亮 | ✅ 后备 |
| macro | 0 | 未点亮 | ✅ 后备 |
| socialmedia | 0 | 未点亮 | ✅ 后备 |
| news | 1 | 未点亮 | ✅ 后备（差2） |
| insiders | 2 | 未点亮 | ✅ 后备（差1） |
| other | 2 | 未点亮 | ✅ 后备（差1） |
| pv | 2 | 未点亮 | ✅ 后备（差1） |
| risk | 2 | 未点亮 | ✅ 后备（差1） |
| sentiment | 2 | 未点亮 | ✅ 后备（差1） |

EUR D0 全 0（本战役固定 D1，不切换）。

## 二、Institutions 候选清单与潜力评估

平台共 2 集（get_datasets count=2，无遗漏）；字段目录全量复核 complete=true（11/11 与 30/30，filter_sharpe=false 不抽样）。

| 数据集 | 字段 | cov | aC/uC | 历史结论 | 本战役处置 |
|---|---:|---|---|---|---|
| institutions6 | 11 MATRIX | 0.9307–0.999 | 106/50（字段级 aC 1–24 极冷） | ATOM 主信号判死（S≤0.95、2Y 断档）；小腿形态实证有效（leAXvaLn/N1NGbddg） | 平台已重算⇒旧判死按 goal 条款复核：W1 全字段全模板再验证；若仍死→转未点亮塔载体小腿 |
| fund_holdings_panel | 30 VECTOR | 0.843–0.918 | 36/21（**25 字段 aC=0 纯白地**） | ATOM F 闸数学封顶（returns 2.33%）；**但历史探针仅覆盖 5/30 字段，覆盖闸未过，判死程序不合法** | W1 补全 30 字段全量探测后才允许维持/作废判死 |

### 选定理由
1. **塔位**：INSTITUTIONS 0/3 未点亮 ×1.1，两集均在选集资格内（goal 首要扫描对象）。
2. **拥挤度**：字段级 aC 0–24，本区几乎无人开采；institutions6 数据集级 aC 6h +7（今日新鲜分析）说明开始被关注，时效窗口收窄。
3. **覆盖**：institutions6 cov 0.9976 达标；FHP base 族 0.908–0.918 达标（_active 族 0.843–0.857 贴线，按 goal「覆盖率可动态调整」以 base 族为主、_active 作散度对照）。
4. **机制文献**：Gompers-Metrick(2001 QJE) 机构持股定价；Bennett-Sias-Starks(2003 RFS) **变动**预测收益；Sias(2004 RFS) 羊群持续；LSV(1992 JFE) 交易冲击不立即反转。详见 eur_institutions_holdings_20261106.md §3。
5. **过期结论作废条款**：平台重算后历史指标失真（goal 明示）；institutions6 ATOM 旧判死建立在旧口径，W1 以当前平台重测为准。

### 关键约束（本波新增）
- **analyst7 载体禁用**：ANALYST 塔已点亮（10 颗）⇒ 旧「analyst7×inst6」组合形态不再用于新波。小腿载体只能来自未点亮塔：首选 insider_agg_matrix（INSIDERS 2/3，leA5JeP7 形态 S1.76/2Y2.32）、次选 news18 密度（NEWS 1/3，mLo7pMwx S1.69/2Y1.81）。
- 组腿禁混集合 {PV,MODEL,OTHER,FUNDAMENTAL}（2026-11-03 用户第四次澄清，EUR 适用）；INSTITUTIONS×INSIDERS / ×NEWS 均合法，两塔组合候选 ≤3，trio×非trio 组合类型总量 ≤5。
- 算子数 ≤12，越少越好；模板库 ≥10 结构互异；multi-sim 并发 =2。

## 三、决策与波次计划

- **W1（本波）**：两数据集全量覆盖复核波。批A=institutions6 10 表达式（11 字段全覆盖，8 结构族）；批B=FHP 10 表达式（30 字段全覆盖，6 结构族）。设置按 profiles explain 生效档逐项显式传。
- **判定分支**：
  - institutions6 ATOM 出现 S≥1.2 近闸 → 进 S4 破闸（边界算子穷举）；
  - 仍 |S|<1.0 → ATOM 维持判死，转「未点亮载体 × inst6 小腿」组合波（W2）；
  - FHP 三闸全过且全波 |S|<0.5 → seal_dead_end（此次程序合法）；否则按最好读数进 S4。
- **后备队列**（Institutions 确实无计可施时启用，需说明原因）：news21（os_is 0.8275 未点亮类最高，未测，TO 风险需先控）> earningscall_sentiment（×1.5，os_is 0.4719）> pv47（冷门低倍率）。依据：platform_dataset_fresh_analysis_20261109.md。

## 四、归档路径与命名规则（goal 要求说明）

| 产物 | 路径规范 | 本战役实例 |
|---|---|---|
| 字段画像 | tracking/EUR/reference/profiles/eur_<category>_<dataset>_profile_<YYYYMMDD>.md | eur_institutions_institutions6_profile_20261108.md（本日复核加签） |
| S0 扫描 | tracking/EUR/s0_<category>_scan_<YYYYMMDD>.md | 本文 |
| 模板池 | tracking/EUR/s1_<dataset>_wave<N>_template_pool.md | W1 两份（派发前落盘） |
| 波次台账 | tracking/EUR/WAVE_LEDGER.md 追加节 | W1 收批后 |
| 战役报告 | tracking/EUR/reports/campaign_eur15_2026-11.md | 里程碑更新 |
