# DEU 字段画像 — analyst44（分析师预估台账型数据集）

> region=DEU / universe=TOP500 / delay=1　|　dataset_id=`analyst44`
> category=analyst（**禁混集合 {PV,MODEL,OTHER,FUNDAMENTAL} 之外** ⇒ 可单塔 ATOM，也可与集合内数据集组腿）
> dataset 级：coverage 0.5802 / fieldCount 72 / alphaCount **58**（低饱和，远未挖穿）/ userCount 46
> 全部字段类型 = **VECTOR（event 型）** ⇒ **必须先 `vec_avg` / `vec_sum` / `vec_count` 聚合成 MATRIX，再接任何 `ts_*` / `subtract` / `divide`**

---

## 一、结构：12 个会计域 × 5 个变体

每个会计域 `<X>` 有固定的 5 个字段：

| 后缀 | 含义 | 可用性 |
|---|---|---|
| `anl44_2_<X>_value` | **当前预测值** | ✓ 数值，核心 |
| `anl44_2_<X>_prevalue` | **前次预测值**（本次修订前） | ✓ 数值，核心 |
| `anl44_2_<X>_lastactvalue` | 上一次已实现/已公布值 | ✓ 数值，可作基准 |
| `anl44_2_<X>_lastactccy` | 币种代码（ISO 4217） | ✗ 字符串，不可运算 |
| `anl44_2_<X>_coveredby` | 覆盖 regime 标识 | ✗ 字符串，不可运算 |

### 12 个会计域与覆盖率

| 会计域 | 前缀 | coverage | 经济含义 |
|---|---|---:|---|
| EPS | `anl44_2_eps_` | **0.6912** | 每股盈利 |
| Sales | `anl44_2_sales_` | **0.6910** | 营业收入 |
| Net Profit | `anl44_2_netprofit_` | **0.6884** | 净利润 |
| DPS | `anl44_2_dps_` | **0.6798** | 每股股息 |
| EBITDA | `anl44_2_ebitda_` | **0.6642** | 息税折旧摊销前利润 |
| ROE | `anl44_2_roe_` | **0.6555** | 净资产收益率 |
| Net Debt | `anl44_2_netdebt_` | **0.6483** | 净负债 |
| EPSR | `anl44_2_epsr_` | 0.6112 | EPS 修订口径 |
| FCFPS | `anl44_2_fcfps_` | 0.5307 | 每股自由现金流 |
| TBVPS | `anl44_2_tbvps_` | 0.4101 | 每股有形账面价值 |
| Cash (csh) | `anl44_2_csh_` | 0.3692 | 现金 |
| Operating Profit | `anl44_2_operatingprofit_` | 0.3229 | 营业利润 |

### 另有 12 个「孤儿」币种字段（无法配对，无信息）

`cash_eps_currency_code_2` / `ebitda_currency_code` / `eps_currency_code_2` / `epsr_currency_code` /
`forecast_currency_dps` / `forecast_currency_fcfps` / `forecast_currency_netprofit` / `forecast_currency_roe` /
`forecast_currency_sales` / `forecast_currency_tangible_book_value_per_share` / `netdebt_currency_code` /
`operatingprofit_currency_code` —— 全为 ISO 4217 字符串，**不可作信号**。

---

## 二、有效信号维度：每域 2 个（水平 + 修订）

**可用数值字段 = 12 域 × 3 个（value / prevalue / lastactvalue）= 36 个**，但真正正交的信息只有两种：

1. **水平**（level）：`vec_avg(<X>_value)` —— 分析师对未来该会计科目的共识水平
2. **修订**（revision）：`subtract(vec_avg(<X>_value), vec_avg(<X>_prevalue))` —— 本次修订的方向与幅度
3. **实现偏差**（surprise）：`subtract(vec_avg(<X>_value), vec_avg(<X>_lastactvalue))` —— 相对已实现值的预期落差

★ **单位铁律**：`subtract` 的两个操作数必须同量纲。`vec_avg(value)` 与 `vec_avg(prevalue)` 同币种同口径 ⇒ 合法。
★ **禁止**直接 `subtract(anl44_2_roe_value, anl44_2_roe_prevalue)`（两个 VECTOR 之间相减会整批连坐）。

---

## 三、与已用数据集的**重叠风险评估**（关键！）

| 已交付件 | 用的信号 | analyst44 的相关风险 |
|---|---|---|
| QPvzNNGG / LLMzYrZe | `mean_estimate_change_pct_f12m_*`（predictive_starmine 的**修正百分比**） | **高** —— analyst44 的 revision 维度同属「分析师修正」，务必改用**水平**或**跨域比率**，不要做纯修正 |
| MPY9VNY9 | `shrt3_bar`（空头持仓） | 低 |
| mLox6Mg2 | sentiment7/27 浏览量 + relpopularity | 低 |
| E56pROb9 | mdl216 修正百分比 + predicted_surprise | **高** —— `predicted_surprise` 与 analyst44 的 surprise 维度同源 |

⇒ **analyst44 的正确切入点不是「修正」，而是「跨会计域的构造比率」**：单域修正已被 predictive_starmine 占满，而 **12 个域之间的比率（估值/质量/杠杆/现金转化）在 DEU 尚无对应件**。

---

## 四、机制假设目录（供 S1 台账）

| # | 机制 | 构造 | 经济学依据 |
|---|---|---|---|
| H1 | **预期质量**（ROE 水平） | `group_rank(vec_avg(anl44_2_roe_value), sector)` | 高 ROE 预期 = 优质公司，质量溢价 |
| H2 | **预期杠杆**（净负债/EBITDA 反向） | `group_rank(divide(vec_avg(anl44_2_ebitda_value), add(vec_avg(anl44_2_netdebt_value), 1)), sector)` | 低杠杆 = 低财务风险 |
| H3 | **预期现金转化**（FCFPS/EPS） | `group_rank(divide(vec_avg(anl44_2_fcfps_value), vec_avg(anl44_2_eps_value)), sector)` | 高现金转化 = 盈利质量高 |
| H4 | **预期股息率代理**（DPS/EPS 派息率） | `group_rank(divide(vec_avg(anl44_2_dps_value), vec_avg(anl44_2_eps_value)), sector)` | 高派息 = 成熟稳健，股东回报 |
| H5 | **预期利润率**（NetProfit/Sales） | `group_rank(divide(vec_avg(anl44_2_netprofit_value), vec_avg(anl44_2_sales_value)), sector)` | 高净利率 = 定价权 |
| H6 | **预期账面价值**（TBVPS 水平） | `group_rank(vec_avg(anl44_2_tbvps_value), sector)` | 账面价值溢价 / 价值股 |
| H7 | **跨域一致性**（修订方向是否一致） | 建 4–5 个域的 signed 修订 rank 再求和 | 多域同向修订 = 真实景气改善，单域修订 = 噪声 |
| H8 | **预期分歧度**（value 相对 prevalue 的域间离散） | `ts_std_dev` over 各域修订 | 分歧 = 不确定性折价 |
| H9 | **预期兑现偏差**（value vs lastactvalue，EBITDA） | `group_rank(subtract(vec_avg(anl44_2_ebitda_value), vec_avg(anl44_2_ebitda_lastactvalue)), sector)` | 预期高于已实现 = 乐观情绪（PEAD 起点） |
| H10 | **覆盖广度**（参与预测的 event 数） | `group_rank(vec_count(anl44_2_eps_value), sector)` | 关注度效应（仅作辅助/门控，DEU 实测广度常无效） |

---

## 五、可用性判读

- **覆盖率**：核心域 EPS/Sales/NetProfit/DPS/EBITDA/ROE 在 0.65–0.69，**高于 analyst93（0.6373）**，做 TOP500 截面足够（约 345 只有值）。
- **近十年数据**：analyst44 为分析师预估台账，DEU 卖方覆盖持续存在；**开波后必须用 `get_alpha_yearly_stats` 逐查 longCount>0 且 pnl≠0，防连续空窗**。
- **拥挤度**：alphaCount 58（12 个域里最高的是 dps_value 18），**远低于 analyst93 的 193 和 analyst7 的 3993** ⇒ 相关性与 prod 撞墙风险低，是本候选最大的优势。
- **风险**：与 predictive_starmine 的修正信号重叠 ⇒ 必须走跨域比率路线（第四节 H2–H6），不要走单域修正。
