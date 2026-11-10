# DEU 数据集挖掘总结报告（2026-11-09 21:40）

## 一、总量账

| 维度 | 数量 |
|---|---|
| 平台数据集全量 | 172 个（实时拉取确认） |
| 已画像（字段级 CSV 存档） | **35 个**（含 salvage 与 wave 扫描） |
| 已开波机制扫（10+ 模板/集） | **20+ 个** |
| 未扫原因 | cov=0 无供数（44 个）/ 字段过少（<5）/ 域外类目（PV/MODEL/OTHER 禁混） |

## 二、已画像数据集清单（35 个，按类目）

### Analyst 族（6 集，4260 字段）
- analyst_consensus（1972）/ analyst_revision_horizons（1095）/ analyst7（608）/ analyst_factor_signals（合并）/ analyst10（合并入 consensus）/ intraday_pv_feats（585）

### Fundamental 族（9 集，2335 字段）
- fundamental72（1031）/ fundamental89（407）/ fundamental90（66）/ fundamental93（46）/ fundamental86（7）/ fundamental45（12）/ fundamental1（123）/ digital_ad_spend（9）/ alpha_factor_lib（65）

### Model 族（8 集，1913 字段）
- model26（548）/ model109（544）/ model25（217）/ model262（159）/ model135（137）/ model30（14）/ model110（8）/ pv20（681，跨 PV）

### Other/PV 族（8 集，1795 字段）
- multifactor_return_pred（648）/ continuation_score（560）/ order_book_imbalance（256）/ pv30（285）/ techindi_model（399）/ search_interest（3）/ workforce_flow_skills（10）/ socialmedia12（18）/ stock_search_trends（6）/ risk68（5）/ imbalance5（2）/ pv106（8）/ macro27（13）

## 三、机制扫描结论（按族）

| 族 | 扫描集 | 结论 |
|---|---|---|
| Analyst 修正 | analyst7 / afs / revision_horizons / consensus | **唯一出货通道**：预期面（修正广度+预测惊喜）——已交付 2 颗 ACTIVE + 候选池 3 颗全绿 |
| 微观结构 | order_book_imbalance / pv106 / imbalance5 | 无信号（AQ：盘口/日内流没有截面预测力） |
| 基本面水平 | fundamental1/6/17/45/72/86/89/90/93 | **系统性零 alpha**（应计/治理/水平/文本/广告/预测模型全灭） |
| Compustat 预测 | model262 / model109 / model25 | 预测误差不定价（Wave 50/62） |
| 通胀/利率 | model140 / macro27 | 未扫（低优先） |
| 破产/质量 | model36 / model28 / risk60 / risk68 | 死 |
| 社媒/搜索 | socialmedia12 / search_interest / stock_search_trends | 无信号 |
| 劳动力 | workforce_flow_skills | 无信号 |
| ML 复合 | multifactor_return_pred / continuation_score / techindi_model | 与应计三连死互证 |

## 四、结构性结论（判据 AO-BL）

1. **「预期面 vs 基本面」分野**是 DEU 的市场结构特征：只有分析师预期修正/预测惊喜出货，财报基本面全灭。
2. **coverage 不可信**：alpha_factor_lib 65 字段 cov 全 0 实为无供数；fundamental45 cov 0.269 却有部分可挖——判数据有无必须探针仿真。
3. **边际闸与 IS 优化反向**（BL）：OS 组合 Sharpe 3.30 饱和后，任何同区新增件都是稀释（ΔSharpe -0.02~-0.05），候选侧无解。
4. **切面多样化撑大族容量但不扩席**（AU）：同族切面互相关 0.95→0.24 可撑 3 席上限，但底层信号数决定总席位。
5. **视界/口径替换破族钉**（BJ）：F12M→FY1 视界替换使 prod 从 0.7676→0.5834。

## 五、交付状态

- ✅ ACTIVE 2 颗：zq3eb7No（S 2.01）、bl6AvMkN（S 1.61）
- 💎 优质候选池 3 颗（全绿但被边际稀释闸拦）：RREOz5qn（prod 0.5834 最净/ΔS -0.02）、QPvzNNGG（0.6777/ΔS -0.05）、RREwqrNa（0.6684/待 CV 豁免）
- 📄 全部证据：segment_verdict_w34w37_20261108.md + 35 个 *_fields.csv + robustness_20261108.md

## 六、出路（需用户裁定）

1. 接受稀释提交候选池任一颗（RREOz5qn -0.02 代价最小）
2. 先撤/降级某颗现有 ACTIVE 腾位
3. 换区域开新战役（DEU 已穷尽）
