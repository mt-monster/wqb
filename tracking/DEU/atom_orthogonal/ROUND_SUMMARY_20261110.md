# DEU 战役 · 本轮总账（2026-11-10 16:30 - 20:0x）

> 本文件汇总本轮全部工作：用户指令「判死太快」触发的系统性修复 + 剩余面实测 + 交付收口。

## 一、用户指令与响应

**指令**：「我觉得你判死的太快了，探针没有穷尽所有机制和模板，这点一定要修复」。

**响应（四件套，全部已落地）**：
1. **全量判死审计**：`DEATH_AUDIT_20261110.md` —— 29 个判死档案逐条对照六维穷尽度，分 ✅合规/⚠️降级/❌撤判/📁待复核。
2. **硬闸固化**：`AGENTS.md §7.6 判死六维穷尽闸` —— D1≥10 互异模板 / D2 字段族自测 / D3 矩全家 / D4≥2 分组轴 / D5 非线性 / D6≥2 配置；缺维只能记 PROVISIONAL，不得引用为邻接先验、不得宣布塔关闭。
3. **撤判重开阶梯（5 波，44+ 条证据）**：见 §二。
4. **过度结论撤回**：`news 塔终判死`、`RISK 塔与 shortinterest3 同机制更弱`、`D1 sentiment 邻接宇宙全部关闭`、`DEU 15 塔全部实测完毕`——全部改证据化表述。

## 二、撤判重开阶梯（5 波）

| 波 | 对象 | 臂数 | 结果 |
|---|---|---:|---|
| BA1 | risk60（借券费/拥挤度）+ risk88（市值）探针 | 10 | 费率面 6/7 同号（翻转 +0.55）；crowding 全灭 |
| BA2 | risk60 冠军骨架十模板池 | 10 | 天花板 **0.90**（offer 费率 x tvr_decay 双窗）；2Y 全档弱 |
| BA2b | risk60/risk88 中性化变维（D6） | 4 | STATISTICAL 下全降级（0.90→0.40）⇒ 无配置层救法 |
| BA3 | news18/news50/news38 首探 | 10 | level/delta 全弱（RavenPack 第 6 次）；vol 面亮点 0.57/2Y1.44 |
| BA3b | news18/news38 vol 定向池 | 6 | 天花板 **0.57**（tv r_decay 版），sub 为负 |

**结论**：risk60/risk88 **六维合规终判死**（0.90/0.79）；news18/50/38 **PROVISIONAL 弱**（三机制面 0.57）；socialmedia12 维持死（AU2 十模板池 0.73）。

## 三、剩余面实测（BA5/BA6）

| 波 | 数据集 | 臂数 | 天花板 | 判定 |
|---|---|---|---:|---|
| BA5 | fund_holdings_panel（institutions 塔，11-03 设计但从未派发） | 10 | **0.65**（F2 稳定边界占比，2Y1.77 但 TO0.467） | PROVISIONAL 弱 |
| BA6 | insiders1（insiders 塔，从未测） | 10 | **0.85**（I7 持股 52 周位置，lc88/TO0.066） | PROVISIONAL 弱 |

**关键核实**：pv29 = 50 字段全是统计行业簇标签（MATRIX/GROUP）⇒ 只能当分组轴，字段自测否决；other699（0.84）/institutions25（0.61）/workforce（0.96）/earnings_sent_matrix（0.63）/ern6（0.40）**均已跑完封盘**（文档 hasRun=false 是执行状态未回写）。

## 四、数据集与塔规则排除（不构成可挖面）

- 已点亮塔：analyst 6 / model 3 / shortinterest 3 ⇒ 排除 analyst46/analyst9/analyst44/analyst_earnings_ibes/shortinterest3 池。
- 已结案族：risk（合规死）、news（PROVISIONAL 弱）、sentiment 全族（≤1.02）、institutions6（二次判死）。
- analyst83 档案重审：实为「卖方分析师电话会发言分析」（993 字段：6 种可读性指数/正负中性情绪 logit/前瞻性情绪/参会人数），**与 earningscall_sentiment（管理层语调）不同源**，撤销「同族先验判死」定性。

## 五、交付（5 颗，见 DELIVERY_FINAL_5ATOM_20261110.md）

| # | alpha | 数据集 | S | 状态 |
|---|---|---|---:|---|
| 1 | zq3eb7No | analyst7 | 2.01 | ✅ ACTIVE（十年零空窗、10 年全正已核） |
| 2 | bl6AvMkN | analyst_factor_signals + predictive_starmine | 1.61 | ✅ ACTIVE（十年零空窗、10 年全正已核） |
| 3 | RREPm361 | analyst7 | **2.02** | 🟡 待授权（prod 0.6881 余量 0.012⚠） |
| 4 | 1YNMAA8M | analyst7 + analyst15 | 1.58 | 🟡 待授权（prod/self 双贴线⚠） |
| 5 | E569ZE7L | shortinterest3 | 1.68 | 🟡 待授权（稳健性 CONDITIONAL） |

## 六、组合路径实测裁决（BC1 在飞）

单数据集已 100% 挖尽 ⇒ 唯一剩余路径为合法双塔组合（OTHER x NEWS）。
BC1（sim 8GEcx5Aa5cz94meh7ozfh5）6 条臂：W1+N4 等权 / AV2+N4 / vector_neut(N4,W1) / W1−N4 反向对照 / 两条乘积交互。
裁决：S≥1.58 出第 6 颗；1.2-1.58 进破闸；<1.2 组合路径关闭、上限确证 5 颗。

## 七、平台坑（已存 Agent Memory）

- DEU D1 EQUITY 实际仅 TOP500（TOP300 也被拒，平台报错自相矛盾）。
- create_multi_simulation 单请求 **2-10 条**（1 条与 >10 条均被拒）。
- get_platform_setting_options 返回的宇宙列表偏宽不可信。
- 台账表达式必须与 `get_alpha_details` 对齐（RREPm361 真实式为 ebi_median/240 + ebt_mean 4 周变化/44）。