# EUR 数据集平台最新状态分析（2026-11-09 09:03）

> 方法：MCP recommend_datasets 全量枚举（EUR/TOPCS1600/D1，未点亮类 97 候选）× 本地目录（eur_dataset_catalog.json，2026-09-25 拉取，173 集）差异比对 + 新鲜统计刷新。

## 一、结论速览

1. **平台无新增数据集**：平台总数 173 = 本地目录 173，top40 差异 = 0。自 2026-10-14 普查（173 集）以来平台未新增任何数据集。「等新数据集」不是可执行策略。
2. **news23 名称澄清**：本地目录记录即为 "MnA Deals Data"（并购交易数据）——普查表中「PE/VC 创投数据」是标注错误；本战役 W18 探针（融资轮注意力 S −0.47）的判死结论适用于其事件族读数，但 MnA 主题字段（deal 属性）本身未单独穷尽。
3. **拥挤度 6 小时变化**（当日 16:59 → 次日 09:03）：
   - pv1：aC 44312 → 44579（**+267/6h**，最拥挤集仍在加速）
   - institutions6：aC 99 → 106（+7）、uC 48 → 50——**我方 N1NGbddg 所在族正被关注，提交时效性优先**
   - socialmedia12：aC 1085 → 1088
   - risk60 / news46：aC 不变（669 / 259）
4. **pv47（Specific Return Dataset）/ pv103（Interval and MOO&MOC）**：存在于本地目录（非新增），当前未进 top40 排名（排名抖动）。pv103 已判死（近静态价差水平）；pv47 未测——特定收益分解类，os_is 0.4236，aC 84 冷门，唯一值得留档的残余候选（×1.1 低倍率，优先级低）。

## 二、未点亮类 97 集的当前格局（对照战役判死清单）

- **已判死/封顶**（本战役 16 族 + 普查历史判死）：techindi_model、risk60、news46、pv1、pv37、pv103、pv109、pv173、socialmedia12、other460、insider_matrix、other128、other250、other296、other567、other571、other635、event_relation、insiders12、news52、news23(事件族)、sentiment7(低cov)、sentiment21、sentiment27(天花板1.33)、macro27、earnings6、earnings_sent_matrix、institutions6(ATOM)、fund_holdings_panel、investor_activity、stock_search_trends、search_interest、workforce_flow_skills、euro_equity_imbalance、other315/327/384/401/452/455/545/546/567/571、dl_riskfree_returns、global_seasonal_model、ai_equity_alpha、analyst45/9/11/4/40/69(信号层)…（详见 _dataset-inventory.md 与战役日志）
- **os_is 质量分领先且未判死的残余**：earningscall_sentiment（os_is 0.4719，other ×1.5，aC 4805 拥挤——VECTOR 事件流 TO 风险，未探针）、news21（os_is 0.8275！未点亮类最高，aC 1312，事件型 TO 风险）、sentiment26（0.5536，cov 0.75 贴线）。
- **建议**：若继续挖，优先级 = news21（质量分最高但需先控 TO）> earningscall_sentiment（×1.5 塔位 + 质量分中上）> pv47（冷门低倍率）。三者均为「历史未判死 + 平台质量分可看」的残余池。

## 三、对当前战役的直接含义

- N1NGbddg（institutions6 族）的拥挤度正在上升（+7/6h），**提交时效窗口收窄**——prod 0.6872 余量 0.013 经不起同族新提交冲击，建议尽快走提交流程（待用户确认）。
- 无新数据集 ⇒ 库存「结构性穷尽」结论维持；增量只能来自①已点亮塔放开②新季度塔清零③平台未来上新。


## 四、全量清点补遗（2026-11-09 09:59，97 候选逐条核对）

拉取全部 97 个未点亮类候选，与战役判死清单 + 普查表历史判定逐条比对：**仅 3 个集合此前无明确结论**，现已补齐画像：

| 数据集 | 画像 | 结论 |
|---|---|---|
| **risk62** | 100+ 字段多因子风险模型（MATRIX，cov 全 1.0），因子暴露 Val1-100 无语义描述，仅 ksrs（特质风险）有语义 | 唯一有体量的残余候选；但 RISK 塔已 2/3 且 ×1.0 倍率，无塔增益；字段需语义映射才能用——**留档待语义映射** |
| acquisition_model | 15 字段 VECTOR，cov 0.7484 | **<0.85 覆盖判死**（sub 闸不可达），排除 |
| event_sentiment_signals | 26 字段 VECTOR，cov 0.3567 | **覆盖判死**，排除 |

其余 32 个非战役判死集合全部有普查表历史判定（TO 爆炸/近静态/覆盖低/信号层死/微型零使用）。

## 五-b、残余池清空补记（2026-11-09 eur15 战役实测收束）

§四建议的三个残余候选已全部实测/预核完毕：
1. **news21**：47/47 字段 30 式三批实测（13 结构族+夺冠几何+半衰期纪律，三闸过）——max |S| 0.73，信号层死。campaign exhausted 已入 registry。
2. **earningscall_sentiment**：预核判死未投波——167 字段 cov 全域 0.5115（无≥0.85，fundamental28 先例同型 sub 结构死）+ 字段级 aC 1676/1145 极拥挤 + 历史 S≤0.21。三重死因。
3. **pv47**：拉字段目录即死——2 字段语义为 **US security / Asia-region security**（区域错配，stock_search_trends 同型死法），EUR 上无经济意义，不投。
⇒ **「未点亮类残余池」正式清空**。风险62 此前已实测封顶（W29 |S|≤1.34）。EUR 未点亮塔剩余可挖性见 s0_eur15_residuum_assessment_20261109.md。

## 五、最终答案：「数据集都分析完了吗」

**是——97 个未点亮类候选 + 76 个已点亮类（含在本战役排除约束内）全部有明确分析结论，无遗漏。**
- 全验证席位 1（N1NGbddg）；近闸库存 88Rx7beX（2Y 待修复）
- 唯一新增留档：risk62（cov 1.0 完美但字段无语义，需映射后才能评估）
- 平台 20h 内零新增数据集
