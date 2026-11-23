# ASI/D1 theme 战役汇总（2026-11-22 ~ 11-23）

> 目标：ASI/D1 Power Pool Dec'26 theme（11-23~12-20），交付全闸 regular alpha。
> 口径：每数据集 ≥10 结构互异模板、模板来自论坛/论文（可指 post id / DOI）、每模板全梯度。
> **提交状态：0 颗**（只挖不提交，红线）。

## 一、三个数据集的终判

| 数据集 | 类别/塔 | 模板数 | 总臂数 | 天花板 S | 卡点 | 判定 |
|---|---|---:|---:|---|---|---|
| price_signal_dl | model / MODEL 0/3 | 8（4 族×2 形态，去重后 7 独立信号） | ~60 | 1.61（双尺度） | **JPN 0.01–0.22** | PROVISIONAL 机制层死 |
| **institutions6** | institutions / **INSTITUTIONS 0/3** | **10** | **~38** | **1.86** | **JPN 0.50** | **除 JPN 外全闸完美** |
| analyst69 | analyst / ANALYST 0/3 | 4（rating 族 + 广度 + 离散度） | ~10 | 1.91 | JPN 0.52 | PROVISIONAL |
| shortinterest5 | shortinterest / SHORTINTEREST 0/3 | 4 | 4 | 0（**零持仓**） | 数据层 | **数据层排除**（塔结构性不可点亮） |

## 二、最强件 `ZYaVVR01`（institutions6）

```
trade_when(ts_mean(count_institutional_holders_security, 90) < 33,
  signed_power(add(
    group_rank(ts_scale(divide(count_institutional_buyers_security,
                 ts_mean(count_institutional_holders_security, 72)), 1260), country),
    group_rank(ts_scale(ts_decay_linear(divide(subtract(
                 count_institutional_buyers_security, count_institutional_sellers_security),
                 ts_mean(count_institutional_holders_security, 72)), 42), 1260), country)),
  1.0), -1)
```
`ASI / MINVOL1M / D1 / INDUSTRY / decay16 / trunc0.08 / maxTrade ON`

| 闸 | 值 | 门槛 | 判 |
|---|---|---|---|
| Sharpe | 1.86 | ≥1.58 | ✅ |
| Fitness | 1.35 | ≥1.0 | ✅ |
| 2Y | 2.94 | ≥1.58 | ✅ 余量 +1.36 |
| Sub-universe | 0.80 | 动态 | ✅ |
| Turnover | 1.95% | [1%,70%] | ✅ |
| Margin | 67.8bp | — | ✅ |
| Robust S / Ret | 过 | 90% 保留 | ✅ |
| **prod_corr** | **0.6083** | <0.70 | ✅ |
| **self_corr** | **0.1837** | <0.70 | ✅ |
| 逐年 | **10/10 PnL>0、无零持仓年** | — | ✅ |
| **JPN Sharpe** | **0.50** | ≥1.0 | ❌ **唯一缺口** |

## 三、JPN 墙：8 维度证伪（信号层，非结构/参数）

| 维度 | 尝试 | JPN 范围 |
|---|---|---|
| 分组轴 | country / industry / exchange / market | 0.43–0.50 |
| 分组结构 | 单轴 / 交叉（country+industry） / `densify(group_cartesian_product)` | 0.39–0.50 |
| 门控阈值 | 绝对 33 / 60 / 100 | 0.25–0.50（**放宽反而更低**） |
| 门控形态 | 相对分位（country 内 0.3 / 0.5） | 0.33 |
| 内层标准化 | exchange z（fundamental23 上把 JPN 0.94→0.98 的解药） | S 崩 1.86→1.30，不迁移 |
| 中性化 | INDUSTRY（最优）/ SLOW | SLOW 崩 1.86→1.08 |
| 窗口 | 1260 / 840 | 840 更弱 |

**三数据集独立复现**：price_signal_dl 0.01–0.22、analyst69 rating 0.52、institutions6 0.50。
⇒ ASI 的 JPN 硬闸是**跨信息源的普遍墙**，平台严禁屏蔽日本（论坛 45201936320919："提交审核会直接报错"）。

## 四、可复用结论（4 条，均有跨区/跨集证据）

1. **流量÷存量铁律（第 3 次复现）**：分母 `buyers/(buyers+sellers)` 流量总和 → S0.63；改 `buyers/ts_mean(holders,72)` 流量÷存量 → **S1.54（+0.91）**。
2. **外层 `rank`→`group_rank(country)` 是 institutions 的最大单杠杆**：S+0.32 / F+0.30 / 2Y+0.60。
3. **`group_cartesian_product` 在 ASI 中等宇宙劣于单轴**：25 个「行业×国家」格 × 门控后 ~1900 票 ⇒ 每格 70 只、小格个位数 ⇒ 组内噪声压过信号。price_signal_dl 0.87<0.95、institutions6 1.68<1.86 两集一致。**GLB/大宇宙才用**。
4. **institutions6 只有计数类字段有信号**（KOR + ASI 跨区复现）：计数家数核 S1.60/S1.86；连续型（渗透率/金额/股数/卖出压力）全部 ≤0.44 或负。

## 五、平台工程坑（本战役新增，已入 memory）

- ASI `create_multi_simulation` 偶发全 FAIL（空 FAIL 无详情），同表达式单发 POST 即 COMPLETE。
- 孪生字段去重伪影：不同表达式返回同一 alpha id，归因只认 `get_alpha_details` 实读 `code`。
- 排队常态：multisim 卡 `progress 0.35`，用轮询 + 20s sleep，**勿重派**（触发 429）。
- `winsorize` 套在 `group_rank` 之后是恒等空操作（读数逐位相同）。
- 制度参数（涨跌停幅度/状态）作信号 ⇒ **零持仓**（longCount=0），判定法 = 1 臂 `group_rank(field, market)`。

## 六、下一步（供决策）

| 选项 | 说明 |
|---|---|
| A. 接受 0 交付结项 | JPN 三集独立验证为普遍墙；ZYaVVR01 留档待 JPN 机制变化 |
| B. 换未满塔继续 | ASI 仍有 12 个塔 0/3（fundamental/model/news/earnings/insiders/macro/risk/pv/broker/imbalance/socialmedia/analyst） |
| C. 专攻 JPN 有定价力的信息源 | 线索：earnings 事件类（日本财报事件）、macro（东证宏观敏感度）——未验证 |
| D. 转 regular 跨集 | ATOM 已穷尽 institutions 单集；跨集需 `atomExhaustedEvidence`（已有） |

## 归档
- `tracking/ASI/reference/datasets/institutions6.md`（19 节：字段全表/14 模板/梯度/审计/归因）
- `tracking/ASI/reference/datasets/price_signal_dl.md`（8 节）
- `tracking/ASI/reference/datasets/analyst69.md`
- `tracking/ASI/reference/datasets/shortinterest5.md`
- memory：`asi-d1-theme-campaign-20261122`、`regulatory-constants-not-signals`、`outer-op-choice-by-signal-type`（补 cartesian 反例）
