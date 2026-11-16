# USA 未点亮塔数据集扫描（S0 候选清单）· 2026-11-14

> 全程固定 USA / TOP3000 / D1。塔位快照（`get_pyramid_alphas` 当季）：
> **已点亮（排除）**：analyst=6、model=4。**差 1 颗点亮**：other=2、risk=2。
> **差 2 颗**：institutions=1、earnings=1。**全 0**：pv/fundamental/news/sentiment/shortinterest/insiders/option/socialmedia/macro/imbalance。D0 全 0（未启用）。

## 1. 扫描总表（13 category / 87 集 → 硬筛）

硬筛四条（来自 `_unlit-tower-campaign-20261014.md` §10/§18 + 台账）：
① 月频/季频流量优先，日更快变量直接跳过（TO 结构性破 fitness）；
② 排除台账 47 死集；③ 排除已点亮塔（analyst/model）主数据集；
④ 低拥挤（alphaCount 甜点 20–300，ac=0 警惕）+ 覆盖率可用（处女地集级 0.35 线）。

## 2. 分类处置

### ❌ 判死台账命中（不投）
acquisition_model、other571、other545、other635、other699、other685、stock_search_trends、
web_traffic 类（sentiment26/27 同族）、workforce_flow_skills（2Y 硬顶已证）、hiring_trends、
institutions18（prod 封）、risk60/risk59（prod 封）、shortinterest29、option3、pv47/pv103/pv115/pv106/pv149/pv20、
insiders4、board_gov_stats、earnings_risk、news_sentiment_transfer、sentiment26、fundamental1/2/14/21/22/25/35/69/72/91/93/110、other416/452、chart_return_model、chart_model_alpha、news_transformer_scores、multi_horizon_alpha、continuation_score、order_flow_imb、intraday_pv_feats、dl_volume_pred、macro63（3 flag 不能当信号）、other551（日频 β）。

### ❌ 结构性排除
- **高拥挤**：socialmedia12（aC 63676）、socialmedia8（17694）、news18（60874）、option8（227691）、option9（92964）、macro38（16289）、fundamental13（15448）、sentiment1（15057）、insiders1（3980）、institutions6（3825）、earnings6（4997）、other335（4962）、shortinterest3（4856）、risk72（2634）、other566（2287）、insider_trx_matrix（1424，且与 insider_matrix 同族副本）、macro10（1280）、earnings_chart_dl（1280）、news3（1029）、socialmedia5（1102）、macro4（1372）、pv104（8247）、pv53（1458）、pv141（1403）、insiders4（1459）。
- **日更快变量高频事件型**（五次判死先验：社媒/文本注意力）：sentiment7（Wikipedia，cov 0.089 太低）、option6（19k 日频预测）、news22/76/48（direct-feed 事件流）、event_return_model（DL 日频，同 chart_return_model 判法存疑但 cov 0.999 日频）。
- **低覆盖**：other335/other424/other436（dividend 族 cov<0.46）、fundamental25（cov 0.38）、macro17（cov 0.5 单字段）、pv109（cov 0.30）、shortinterest24（cov 0.257）、pv141/pv53（cov 0.5）、univ2（单字段 universe）、earnings27（cov 0.27）。

### ✅ 候选清单（按塔收益 × 拥挤度排序）

| 优先 | 数据集 | 塔/mult | cov | fc | aC | 选定理由 | 风险 |
|---|---|---|---:|---:|---:|---|---|
| **P1** | `insider_agg_matrix` | insiders/1.1 | 0.77 | 17 | **190** | **USA 零回测 virgin**、valueScore 4、拥挤极低；台账点名「开波前必做 prod 探针」 | directional_* 曾报毒字段（longCount=0）；金额量级需尺度归一 |
| **P2** | `insider_matrix` | other/1.4 | 0.77 | 33 | 1995 | 台账「族内 3/4 颗 prod<0.7 有余量」；d5KzLo7v prod 0.6964/self 0.24 在 READY；runs/usa_insd_w1 十臂已预注册 | 族内同机制只能再出 1 席（一腿一席）；需避开已占轨道 |
| **P3** | `earnings_sent_matrix` | earnings/1.3 | 0.70 | 7 | 1999 | **earnings 塔差 2 颗点亮**；台账「未验证」正面列名；omWMO06n（earnings_sent）S2.50/F1.52 已有 ACTIVE 先例 | 文本情绪族在 USA 已多集判死，需避文本极性重复机制 |
| **P4** | `news97` | news/1.2 | 0.98 | 105 | 276 | transformer 日度情绪**统计量**（非极性裸值）、低拥挤、valueScore 3 | 同 news_transformer_scores 判死接近（那个是「分数」族 S≤0.50）；statistics 族或不同 |
| **P5** | `institutions20` | institutions/1.0 | 0.98 | 17 | 1358 | Short Sale Volume 日频量——⚠ 日更先验负，但**日度做空量占比**是月频 SHORT_INTEREST 的日度前身，量比型可能低换手 | 短卖日频族此前「噪声」判法（03_region） |
| **P6** | `other623` | other/1.4 | 0.99 | 6 | **38** | 全库最低拥挤之一、text blob NLP 增强、valueScore 5 | 6 字段需查语义；新闻文本族负先验 |
| **P7** | `cre_exposure_model` | other/1.4 | 0.79 | 2 | 7 | 已判弱封存（max S 0.99）——**不投**，仅登记 | — |
| **P8** | `risk65` | risk/1.1 | 0.97 | 6 | 551 | ETF 级风险模型——ETF 覆盖有限（universe 是股票），先验弱 | ETF 字段在股票 universe 大多 NaN |
| **P9** | `other327` | other/1.4 | 0.79 | 3 | 229 | 利率敏感度模型，3 字段小面；cre 档案说「ts_rank504 对回归 β 无效」 | 小面一次穷尽 |
| **P10** | `macro10` | macro/1.1 | 1.0 | 1 | 1280 | 单字段（利率/国债收益率族）——单字段难出横截面信号 | 大概率排除 |

### 主攻路线（节省配额的收敛）

1. **P1 `insider_agg_matrix`**（virgin、1.1 塔）→ prod 探针 → 十臂波。
2. **P2 `insider_matrix`**（1.4 塔、族内余量）→ 复用预注册十臂骨架（runs/usa_insd_w1）未跑部分。
3. **P3 `earnings_sent_matrix`**（1.3 塔差 2 颗）→ 7 字段全量画像后开波。
4. **P4/P6** 新闻统计量低拥挤族备胎（news97 statistics / other623）。
5. institutions20 仅在 P1–P3 全灭后投（日频先验负）。

**约束执行**：全部单数据集 ATOM（PV/MODEL/OTHER 禁组腿令）；零组腿则 5 个跨界组合配额不受影响。
并发 2（create_multi_simulation 每批 ≤2 条；≥2 条/批的 n=1 拒批规避）。
