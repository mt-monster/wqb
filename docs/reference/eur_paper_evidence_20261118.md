# EUR 未点亮塔机制 — 金融论文取证（2026-11-18）

> 目的：为交付的 10 颗 regular alpha 的三类经济机制提供**外部学术证据**，与论坛取证
> （`eur_forum_evidence_20261118.md`）互补。检索通道 WebSearch/WebFetch（论文线 EVID-PAPER，
> 不拿它当论坛通道）。所有条目均为真实可引文献，DOIs/URL 随条目给出；
> 部分出版商页面（ScienceDirect/Sage/CORE）直接 WebFetch 返回 403/超时，未证实在线解析但不影响引用真实性。

## 机制 1：分析师预期修正广度/扩散（强腿 est_12m_*_raisednum/lowerednum）

1. **Womack, K. (1996). "Do Brokerage Analysts' Recommendations Have Investment Value?" *Journal of Finance* 51(1): 137–167.**
   https://doi.org/10.1111/j.1540-6261.1996.tb05208.x
   发现评级变动的异常收益（买入 +3.0%、卖出 −4.7%/3日）**之外还有 post-recommendation drift**：买入后首月再涨 ~2.4%，卖出后 6 个月续跌 5–9%。
   ⇒ 市场对信息反应不足、逐步定价——支持"分析师修正广度变化先于后续收益"的强腿机制。

2. **Gleason, C. A., & Lee, C. M. C. (2003). "Analyst Forecast Revisions and Market Price Discovery." *The Accounting Review* 78(1): 193–225.**
   https://doi.org/10.2308/accr.2003.78.1.193
   记录沿预测修正方向的稳健 **post-revision 价格漂移**，且漂移集中在后续财报与**其他分析师的接下来 6 次修正**上。
   ⇒ 单个分析师的信息需被同行确认才充分定价——正是"修正广度（raisednum 减去 lowerednum）"而非单次幅度有效的直接证据。

3. **Jegadeesh, N., Kim, J., Krische, S. D., & Lee, C. M. C. (2004). "Analyzing the Analysts: When Do Recommendations Add Value?" *Journal of Finance* 59(3): 1083–1124.**
   http://csinvesting.org/wp-content/uploads/2016/08/Analyst-Recommendations-Do-they-add-value.pdf （2001 working paper 版）
   共识评级的**季度变化**是稳健收益预测因子，正交于动量/规模/价值；评级**水平**仅对特定股票有价值。
   ⇒ "变化/广度"携带预测内容而"水平"较弱——支持用 raisednum/lowerednum 的差分构造而非水平，也解释本轮 DPS/GPS 水平型读数失败。

## 机制 2：机构持仓/交易流（institutions6 家数不对称、资金流小腿）

4. **Nofsinger, J. R., & Sias, R. W. (1999). "Herding and Feedback Trading by Institutional and Individual Investors." *Journal of Finance* 54(6): 2263–2295.**
   https://scholar.google.com/scholar?q=Nofsinger+Sias+1999+Herding+and+Feedback+Trading
   机构持仓**变化**与收益同期正相关且之后无反转，机构买入的股票后续跑赢卖出的股票。机构羊群与滞后收益/动量正相关。
   ⇒ 机构家数/资金流变化（buyers−sellers 不对称）是有信息含量的信号，非噪声。

5. **Kirk, M. (2026). "Abnormal Institutional Ownership and Expected Returns." *Journal of Accounting, Auditing & Finance* 41(2): 524–546.**
   https://doi.org/10.1177/0148558X251319189
   将 13F 机构持仓（228 万 firm-months，1984–2022）拆为预期与**异常**两部分；异常持仓最高组次月跑赢最低组 **76bps**，且在 45 天披露滞后下仍持续。
   ⇒ 直接验证"异常机构持仓广度"的预测力——对应 `market_value_institutional_shares_{acquired,disposed}` 资金流小腿。

## 机制 3：内部人交易（insider_agg_matrix 高管净买入小腿）

6. **Lakonishok, J., & Lee, I. (2001). "Are Insider Trades Informative?" *Review of Financial Studies* 14(1): 79–111.**
   https://doi.org/10.1093/rfs/14.1.79
   用 1975–1995 全样本内部人交易，发现内部人可预测横截面收益，但预测力**集中在小盘、几乎完全由内部人买入驱动**（重仓小盘买入 → 12 个月 ~7.4% 异常收益），卖出无预测力。
   ⇒ 支持"买入-卖出不对称"构造（total_top_buy−total_top_sell），也提示卖出腿信息弱。

7. **Seyhun, H. N. (1986). "Insiders' Profits, Costs of Trading, and Market Efficiency." *Journal of Financial Economics* 16(2): 189–212.**
   https://doi.org/10.1016/0304-405X(86)90029-2
   奠基研究（~6 万笔交易，1975–1981）：内部人**买入后 100 天异常收益 +3%、卖出后 −1.7%**；越接近经营核心、交易越大、公司越小，预测越强。
   ⇒ 确立"内部人交易方向预测未来异常收益"的核心前提。

## 机制 4：财报/现金流质量应计（fundamental72 现金流质量门控）

8. **Sloan, R. G. (1996). "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?" *The Accounting Review* 71(3): 289–315.**
   https://www.jstor.org/stable/248144
   发现**应计异象**：盈余中应计部分比现金流部分持续性差，投资者"盯住"底线盈余而未能区分——高估应计、低估现金流。做多低应计/做空高应计获显著异常收益。
   ⇒ 直接支持"现金流质量门控"（`fnd72_pit_or_is_a_ebitda / cf_a_cf_net_inc`、`CFO/资产` 优于纯利润水平），是 #6/#7 两颗现金流质量 alpha 的经济根基。

## 落地状态

- 三篇强腿/小腿论文（Womack、Gleason&Lee、Nofsinger&Sias）直接支撑"修正广度强腿 + 机构流小腿"结构。
- Sloan(1996) 解释为何 fundamental72 现金流质量读数（而非利润水平）能出 #6/#7 两颗正交 alpha（与 EBI 家族互相关仅 0.05）。
- Lakonishok&Lee、Seyhun 支撑内部人买入-卖出不对称构造。
- ⚠ 论文只提供机制先验，不替代平台实测；prod/self/fitness 仍以 MCP 回测为准（与论坛证据同一纪律）。
