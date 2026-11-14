# ★OS 占用图谱（v2 第一道筛：族级正交性）— 2026-11-11 从 20 颗平台原始表达式提取

> 依据：DEU 的 prod 相关性 ≈ 一次 self 检查（10-30 战役报告 §64.4-64.5）——
> prod 直方图几乎全在 [-0.1,0.2]，唯一 [0.9,1] 那条就是自家 alpha。
> ⇒ **新候选必须先做「与自家 OS 族级正交性」筛查，再做 IS 波**（v2 协议新增筛）。

## 一、已占家族（20 颗 ACTIVE）

| 家族 | 占用 | 关键字段 | 占用者 |
|---|---:|---|---|
| analyst 预估族 | **9** | est_12m_ebt_mean / eps_y1_estimate_change_3mo / predicted_surprise_f12m_ebitda_4 / mean_estimate_change_pct_f12m_* | rKRx2Alj, zq3eb7No, bl6AvMkN, LLM93nGa, 2rjrMZ25, vRk6og8b, Vk65zLzG, 883Y3bAW, blRnKEk6 |
| shortinterest3 `mean_loan_rate_main` | **3** | mean_loan_rate_main | LLM93nGa, vRk6og8b, blRnKEk6 |
| OTHER `oth455_*` 聚类/关系字段 | **3** | oth455_partner/relation_*_cluster_20 | 2rmGAPqN, 58gkLAkk, 2rOe10qY |
| shortinterest3 `shrt3_bar` + tvr_decay | 2 | shrt3_bar | 78Yk8VR1, xArzm3Mn |
| institutions1 信念比值 | 1 | inst1_valueeur/holdings/tradesignificance | 2rmGAPqN（20 算子） |
| insider_agg `directional_indicator` | 1 | directional_indicator | Vk65zLzG |
| sentiment snl27+snt7 | 1 | snl27_relpopularity08, snt7_all_languages_views | bl6OWZ2M |
| fundamental fnd6 oiadpq | 1 | fnd6_newq_oiadpq | Wje5K71x |
| model starmine 多腿 | 1 | predicted_surprise_f12m_ebitda_4 | bl6AvMkN |
| analyst profitability estimator | 1 | anl93_recprofitabilityprev_* | GrW9OxmG |
| （未标塔 2 颗） | 2 | — | vR1oxZA3, mLYLEm99 |

## 二、★仍然完全开放的族（= 新候选应该去的地方）

| 族 | 数据集 | 塔 | 状态 |
|---|---|---|---|
| **nws20 事件情绪** | news20 | NEWS | OS 0 件（9qlz29Oe 待授权未提交） |
| **oth47 网站流量** | other47 | OTHER | OS 0 件（Jj8VQwoe 待授权未提交） |
| **insd1_holdings** | insiders1 | INSIDERS | OS 0 件（qM7KxkQV 待授权未提交） |
| **max/mean_loan_rate_p5_d1** | shortinterest3 | SHORTINTEREST | OS 0 件（d5a2vxzY 待授权未提交） |
| **pv30 聚类簇轴** | pv30 | PV | OS 0 件，且 285 字段全是 GROUP 类型 cov=1.0 |
| option1 IV 面 | option1 | OPTION | OS 0 件 |
| risk / earnings / macro / imbalance / socialmedia | 各 | 各 | OS 0 件 |
| fundamental 除 oiadpq | fundamental* | FUNDAMENTAL | OS 仅 1 件（oiadpq） |

## 三、使用规则（写进 v2 协议）

1. 派波前先查该波第一腿是否落在上表「已占家族」——落在已占家族 ⇒ 预期 self/prod 撞墙，除非第二腿能显著改变结构；
2. 落在「开放族」⇒ 优先；
3. 特别地：**anl93/est_*/eps_y1/predicted_surprise/mean_loan_rate_main/oth455_*/directional_indicator 这七个字段族在 DEU 已饱和**，任何新候选应避开；
4. 候选若 self >0.9，先看 top 对端是不是自家件（DEU 的 prod 直方图唯一那条 [0.9,1] 就是自家 alpha）。