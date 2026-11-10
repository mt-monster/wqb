# 提交参数草案（2026-11-09 22:40 · 等用户逐颗确认后由 workflow_submit_alpha 执行）

> ⛔ **23:40 更新（§39）**：d5Wvpmbx prod 漂移至 **0.9081 深墙出局**，其草案段落作废；ZYQ/omER 快照 prod 读数额外待复证（平台重算中，~23:55）；**当前唯一全链就绪 = QPvx8M1W（prod 0.6687 今晚实测）**。

> ⚠ 本文件仅为参数预案，**未执行任何提交**。真提交=confirm_submit=true，不可逆，每颗需用户明确指令。
> 命名已核 docs/alpha_properties_spec.md §二：KOR_R_<family>_<seq>，禁 PROD 数值；KOR_R_insd5vol55_01(RRE9NkVj) 已占不冲突。
> 软标记披露行来自 robustness 台账（skill Phase D 要求三段描述如实带上）。

## 1. d5Wvpmbx（优先级最高：ΔS+0.47，2023 逐年增强）
- name: `KOR_R_r68voldadv_01`
- color: 缺省（BLUE，待 OS 挣 GREEN）；tags: ["campaign_20261107", "risk68", "spread"]
- descriptions 三段:
  - Idea: 风险模型权重中「短期波动权重」与「日内活跃度权重」的 22 日变化价差——波动定价 vs 流动性定价的相对迁移赚拥挤出清的钱（KOR 2023 逐年 S=4.69 增强）。
  - Data(risk68): weight_volatility_short / weight_dadv 均 MATRIX 高覆盖，同数据集同源双腿，单一经济含义合规价差。
  - Operators: ts_delta(22) 取权重迁移一阶动量 → group_rank(sector) 截面化 → subtract 同源价差；5 算子无装饰。
  - 披露行: robustness CONDITIONAL（近3年 CV=0.515、max/min=4.99 边界系 2023 走强方向，非衰减）；self 0.2023/prod 0.6906/ΔS+0.47。

## 2. QPvx8M1W（第 7 颗，全链闭环）
- name: `KOR_R_anlr68gn_01`
- tags: ["campaign_20261107", "analyst10", "risk68", "cross-dataset"]
- descriptions:
  - Idea: 分析师销售预期惊喜的长窗均值回归水平（300d）− 风险模型活跃度权重迁移（66d）= 预期修复 vs 拥挤漂移的分歧对，行业中性化残差。
  - Data: anl10 smartest_sal_fy2_pred_surps_v1（cov 0.83）× rsk68 weight_dadv，ANALYST×RISK 合法两塔组合（禁混集合外）。
  - Operators: 外层 group_neutralize(industry)（论坛实证 2Y 杠杆）+ hump 平滑 + sector 组内价差；7 算子。
  - 披露行: robustness PASS（CV0.264/衰减0.91）；prod 0.6687/self 0.6447/ΔS+0.28；篮子全对<0.7。

## 3. ZYQ116ln
- name: `KOR_R_bidcorr_01`
- tags: ["campaign_20261107", "pv", "reversal"]
- descriptions:
  - Idea: 买价-买量相关性高 = 流动性压力/报价黏滞 → 反转；做多低相关、做空高相关。
  - Data: intraday_pv_feats corr_bid_price_with_bid_size（日内微观结构聚合特征）。
  - Operators: ts_mean(22) 平滑 → group_rank(industry) → subtract(0.5,·) 真反臂；3 算子全池最简。
  - 披露行: robustness CONDITIONAL（CV0.459、衰减比0.527贴线）；prod 0.6981/self 0.1426/ΔS+0.24；SLOW/d2 系降 prod 先例。

## 4. omERn83n
- name: `KOR_R_r70analyst_01`
- tags: ["campaign_20261107", "risk70", "orthogonal"]
- descriptions:
  - Idea: 风险模型「分析师情绪载荷」对「动量载荷」做 vector_neut 正交后的纯情绪残差，signed_power 压尾 + 目标换手控制。
  - Data: rsk70 mfm2_asetrd_anlystsn × momentum 双腿同源正交（RISK 数据集内构型）。
  - Operators: rank→vector_neut→winsorize→signed_power(2.5)→group_rank(sector)→ts_target_tvr_decay(0.22)；9 算子偏多已如实标注。
  - 披露行: robustness CONDITIONAL（CV0.581、max/min3.82，2022=3.74 单峰驱动）；prod 0.6898/self 0.4211/ΔS+0.10。

## 5. 9qxnYPjd（第 8 颗 · 待 prod 终测，<0.70 才启用本参数）
- name: `KOR_R_preinsd_01`
- tags: ["campaign_20261107", "analyst10", "insiders5", "cross-dataset", "E56-rescue"]
- descriptions:
  - Idea: 分析师税前利润预期惊喜（pre_fy1，3-4 季前瞻）长窗水平 vs 内部人申报量分歧度——预期修复 × Miller-1977 分歧，sector 价差；E56jA0AP 同机制换 pre 字段面破 prod 钉（归因 §35）。
  - Data: anl10 smartest_pre_fy1_pred_surps_v1 × insd5 vol_chg(vec_stddev 55)；ANALYST×INSIDERS 合法组合。
  - Operators: ts_av_diff(250)/ts_mean(vec_stddev,55) 两腿 group_rank(sector) subtract + hump；7 算子。
  - 披露行: robustness PASS（CV0.322 优于母件）；self 0.5078/ΔS+0.14/prod=<待 22:41 读数>。

## 执行序（用户逐颗说「提交 N」后）
workflow_submit_alpha(alpha_id, name, color=null, tags, descriptions, confirm_submit=true, robustness_audited=true) → 提交后按 worldquant-submit-alpha 链核对 GET /alphas 状态 + 台账置 ACTIVE。**qMLOooX1/LLZ6wZO2 不在本草案**（REJECT/阻断未裁定）。
