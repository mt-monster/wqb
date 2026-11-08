# S1 应急画像 · other553 Financial Opinion Mining（KOR / TOP600 / D1）

> 仅作 Wave1 forum 若全灭后的备选；category=sentiment，塔 0/3，乘数 1.6。
> 数据源：MCP get_datafields filter_sharpe=false。

## 字段表

| 字段 | type | cov | aC | uC | 描述 |
|---|---|---:|---:|---:|---|
| oth553_est_analyst | VECTOR | 0.7397 | 12 | 10 | Number of analysts providing estimates. |
| oth553_est_estvalue | VECTOR | 0.7397 | 36 | 25 | Value of current estimates. |
| oth553_est_isprevspeak | VECTOR | 0.7397 | 6 | 6 | Indicator if there was previous speech related to estimates. |
| oth553_est_preestvalue | VECTOR | 0.6555 | 11 | 7 | Value of current estimates. |
| oth553_est_yearspeakcnt | VECTOR | 0.7397 | 1 | 1 | Count of speeches related to estimates within the year. |
| oth553_horizon | VECTOR | 0.5838 | 0 | 0 | Time horizon for the data point. |
| oth553_preptgvalue | VECTOR | 0.5049 | 2 | 2 | Value of the previous price target. |
| oth553_prerecvalue | VECTOR | 0.4844 | 8 | 8 | Value of the previous recommendation. |
| oth553_ptg_analyst | VECTOR | 0.5838 | 1 | 1 | Number of analysts providing price target estimates. |
| oth553_ptg_isprevspeak | VECTOR | 0.5838 | 1 | 1 | Indicator if there was previous speech related to price targets. |
| oth553_ptg_yearspeakcnt | VECTOR | 0.5838 | 0 | 0 | Count of speeches related to price targets within the year. |
| oth553_ptgvalue | VECTOR | 0.5838 | 2 | 2 | Value of the current price target. |
| oth553_rec_analyst | VECTOR | 0.4844 | 4 | 4 | Number of analysts providing recommendation estimates. |
| oth553_rec_isprevspeak | VECTOR | 0.4844 | 1 | 1 | Indicator if there was previous speech related to recommendations. |
| oth553_rec_yearspeakcnt | VECTOR | 0.4844 | 1 | 1 | Count of speeches related to recommendations within the year. |
| oth553_recvalue | VECTOR | 0.4844 | 9 | 8 | Value of the current recommendation. |
| oth553_sal_analyst | VECTOR | 0.7485 | 8 | 8 | Number of analysts providing sales estimates. |
| oth553_sal_estvalue | VECTOR | 0.7485 | 11 | 11 | Value of current sales estimates. |
| oth553_sal_isprevspeak | VECTOR | 0.7485 | 7 | 6 | Indicator if there was previous speech related to sales. |
| oth553_sal_preestvalue | VECTOR | 0.6565 | 0 | 0 | Value of current sales estimates. |
| oth553_sal_yearspeakcnt | VECTOR | 0.7485 | 1 | 1 | Count of speeches related to sales within the year. |

## 初判
- 实际偏分析师估计/目标价/推荐意见挖掘，不是纯股吧流量；与 Social Media 字面更远。
- 论坛警告（2026-09）：「类目叫情绪，最挤的字段没一个是情绪」——部分 oth553 热门字段是句长/词数/数字位等文本形态，**勿当情绪分**。本应急池优先 est/ptg/rec/sal 数值腿。
- Wave1 equity_forum_data 未判死前不派发本集。
