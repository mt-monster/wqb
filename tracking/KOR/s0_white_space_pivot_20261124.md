# KOR S0 决策：从「Institutions / Insiders」转向未测白空间（2026-11-24）

> 用户任务原指定「优先未点亮塔，比如 Institutions、Insiders」；本轮开波前用平台实读 + 档案
> 复核后确认这两条线在本区已结构性关闭，按 SOP「确实无计可施才换集，并说明原因」条款转向。

## 1. 平台实读（`get_pyramid_alphas`，2026-11-24）

KOR/D1 塔位：`analyst 4 / fundamental 3 / model 3 / insiders 3 / pv 3 / risk 3 / shortinterest 4`
（均已亮）；`institutions 1 / imbalance 1 / other 2`（部分亮）；
`earnings / macro / news / socialmedia / sentiment 0`（未亮）。

- **Insiders 3/3 已满**：按用户「排除已点亮塔数据集」约束，insiders1 / insiders5 一律不进候选。
  且档案记录 insiders5 天花板 S≈1.05 / prod 地板 0.7185（`insiders5.md` §6、wave289 清单）。
- **Institutions 1/3**：仅 2 个 KOR 集。`institutions6` 的两条互异信息机制均已穷尽
  （计数家数核已提交 `P05zx7zx`；连续型流量/存量核 8 臂全灭最高 S0.39，
  2026-11-23 见 memory `kor-institutions6-continuous-fields-dead-20261123`）；
  `fund_holdings_panel` 数据集级判死（wave289 引用 `KOR-FUND-HOLDINGS-PANEL-DEAD`）。
- **Insiders 邻近 OTHER 集 `insider_feats`**：`KOR-INSIDER-PROD-SATURATED`，
  30+ 条 prod ≥0.75，地板 0.7185 不可修（wave289 清单）。
- **全库严格产出率**（`get_mining_yield`）：KOR 5304 回测 / 424 ra_clean / 63 prod_clean；
  prod_clean 几乎全落在已亮塔或未亮塔的信息源级 prod 墙（dl_riskfree_returns prod_wall_ratio=1.0）。

## 2. S0 扫描（`tracking/KOR/scripts/kor_s0_scan.py`）

白名单 Top：`other546`（全 VECTOR peer-network，cov 0.44–0.67，非个股信号 ⇒ 数据层排除）、
`mmp_nlp_sentiment`（**OTHER 塔 2/3 有名额**；521 字段，2026-04-01 onboard，几乎全部 alphaCount=0）、
`equity_forum_data`（已测判死）、`other78`（事件日历集，规约判死）、
`news_sentiment_dl/nlp`（cov 0.259 < 地板，数据层排除）、
`other335`（弱但活：S1.14，仅 RAM 中性化扫过）、`other545`（4 字段，已测 S≤0.49，机制窄）。

## 3. 决策

按用户「Fresh white space, honest results」裁定：主攻 **`mmp_nlp_sentiment`**，
以「revision / surprise topic」为机制轴（KOR 唯一有信号的 news 形态，见
`_field-profile-and-templates.md` F-1）；`other335` 作备选（近闸但中性化 11 档未扫）。
不承诺 10 颗——按实测交付并诚实写天花板。

## 4. 组腿约束遵循

`mmp_nlp_sentiment` = OTHER 类 ⇒ 只做单集 ATOM，禁止 PV / MODEL / OTHER 两两组腿
（用户约束三）；NEWS 等其它类组腿累计 ≤5（本轮暂无组腿）。

## 5. 归档路径与命名规则

- S0 决策：`tracking/KOR/s0_white_space_pivot_20261124.md`（本文件）
- 字段画像：`tracking/KOR/reference/datasets/<dataset_id>.md`（每数据集一份，手工维护）
- 波次报告：`tracking/KOR/waves/<wave>_<dataset>_20261124.md`
- 梯度 Δ 表：波次报告内嵌「梯度 Δ 表」小节（`tools/research/operator_swap_matrix.py` 逐层同类别替换）
