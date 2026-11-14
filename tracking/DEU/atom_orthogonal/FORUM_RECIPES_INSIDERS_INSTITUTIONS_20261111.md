# 论坛配方挖掘：DEU insiders/institutions 三帖拆解（2026-11-11 上午）

## 一、帖子 43178926004887（DEU INSTITUTIONS 破咒帖，88 次回测，已提交 xAjEkeOq S1.68/F1.34/TO7.36%/2Y2.40/prod0.52/self0.11）

**核心机制：信念强度 conviction ratio = inst1_valueeur ÷ inst1_holdings**（交易金额 ÷ 交易后总持仓 = 占仓位比例）。
- 文献链：Jeng-Metrick-Zeckhauser 2003（买入有信息卖出没有）+ Lakonishok-Lee 2001（规模标准化）+ Cohen-Malloy-Pomorski 2012（机会型 vs 例行）
- 四步处理：vec_sum 聚合同日多笔 → divide(分子, add(分母, 0.0001)) → winsorize 压清仓爆炸 → 时间平滑（TO 7.36%）
- **数据画像修正**：coverage 0.23 不可读作日覆盖 23%；有效样本 2018 起（MAR/MiFID II 后标准化），2014-2017 极薄——**此前 BE45 探针 -0.35/0.41 很可能被前段空窗拖垮**
- 平台已提交件 xAjEkeOq 占 INSTITUTIONS 塔第 1 颗；姊妹构造（股数比/显著性加权）与主信号同机制，self 端点将主要是它

## 二、帖子 43583576215447（DEU Insiders/Imbalance 模板骨架帖）

- **设置实证**：Insiders 偏 INDUSTRY 中性化（非 SUBINDUSTRY）、decay 3-5、trunc 0.06-0.10、低换手 <0.2
- INS-DEU-01 主力骨架：多腿 **max 归并**（"一条腿强就强"，非 add）+ 五窗同构 10/105/120/180/250 + 外套 ts_mean(40)
- INS-DEU-02：ts_max 极值族同构
- INS-DEU-03 单腿 conviction：winsorize(group_rank(ts_sum(field1,66),industry),std=2)
- VECTOR 字段先降维（vec_stddev/vec_percentage）再与 MATRIX 同框

## 三、帖子 43467688159511（insider_agg 观察帖）+ 43615381230871（怎么用 insiders）

- 买入纯度 > 卖出；多人协同增持置信度倍增；相对占比 > 绝对金额
- insider_agg_matrix = insiders 类里最冷的真成交（u96/a182）；买侧已写烂，仓位变动/卖侧更新鲜

## 四、对假阴性判死的定性（v2 协议验证案例）

BE45（institutions1 2 臂）与 BE44 的 insider_agg 5 臂是**假阴性**：
1. 矩错误——没测「流量÷存量」比值面（conviction ratio 是主信号）
2. 中性化档错误——SUBINDUSTRY vs 论坛实证 INDUSTRY
3. 窗口结构错误——单窗 vs 五窗同构 max 归并
4. 前段空窗未隔离（2014-2017）

⇒ BE48/BE49 已按论坛配方重构 L1 网格派发（sim 218THQ6H25iNcMjfFblkdVs / 2gjOc31ty4Q7a18t2UO5Lha）。
这也是「文献前置」制度的价值实证：v2 的 L1 文献臂直接给出了别人 88 次回测的答案。
