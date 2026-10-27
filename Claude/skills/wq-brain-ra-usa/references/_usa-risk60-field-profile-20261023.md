# USA / risk60（借券费率与拥挤度）字段画像与机制实证

> 快照：2026-10-23（`get_field_catalog` region=USA dataset=risk60，5/5 字段实测）
> 状态：**在挖**（波 1 四臂 S≈2.2 / F≈4.0，唯一失败 `LOW_SUB_UNIVERSE_SHARPE`；波 2 定向修 SUB）
> 上游选集依据：`_usa-fundamental-universe-scan-20261023.md` 的 fundamental 塔耗尽后，
> 按「未点亮塔 × 零历史 USA 表达式 × 高覆盖」重选（见本文件 §1）

## 1. 为什么换到 risk60（不换 region，只换数据集）

fundamental 塔在 USA 已无可用靶位（逐条有证据）：

| 数据集 | 状态 | 证据 |
|---|---|---|
| other416 (fundamental 塔) | **停投** | 两波 20 臂最高 S 0.99，预注册判据（≥1.30 才算结构轴有效）命中，见 `_usa-other416-field-profile-20261023.md` §8.2 |
| fundamental1 | 判死 | 波 87 十臂 max S 1.17，`USA-FND1-GOVERNANCE-WEAK` |
| fundamental93 / other452 | 判死 | 波 85 十臂 max S 1.11，税应计族跨数据集共享拥挤 |
| fundamental69 / 91 | 判死 | 历史波次 |
| fundamental21 | 排除 | 覆盖 0.429，ESG 慢变量无稳健溢价 |
| fundamental22 / 72 | 排除 | 描述实为 RIC↔BBG 映射表，非信号 |
| fundamental110 | 排除 | 26 字段全是 VECTOR 事件元数据 |
| fundamental25 / 35 | 排除 | 覆盖 0.382 / 仅 1 字段 |
| fundamental2/3/6/7/13/14/17/23/28/other466 | 饱和 | aC 3e3 – 8.6e5 |

⇒ 这是任务约束里「确实无计可施才换数据集」的情形：**换的是数据集，不是 region**。

**risk60 入选的四个交集**：① 平台类别 `RISK`（塔未点亮，×1.1 倍率，USA/D1 计 0 条 ACTIVE）；
② **USA 历史零表达式**（`alphas.expression LIKE '%rsk60%' OR '%lending_fee%'` = 0），跨区 RA 干净（DEU 11 / GLB 12 条已过 RA）；
③ 字段覆盖 **1.000**（无 SUB 覆盖风险）；④ 字段少（5）但机制集中，适合 ATOM 单字段。

## 2. 字段全表（5/5）

平台 `data_type=MATRIX`，但**5 个字段逐个为 VECTOR**（硬约束见 §4）。

| 字段 | 类型 | 覆盖 | userCount | **aC** | 语义 |
|---|---|---:|---:|---:|---|
| `lending_fee_bid_rate` | VECTOR | 1.000 | 102 | **168** | 出借方可获得的综合年化借贷费率（lend 侧） |
| `rsk60_datatime` | VECTOR | 1.000 | 236 | 665 | 快照时间 HHMMSS，用于排 intraday 打印顺序（**元数据，非信号**） |
| `rsk60_crowding` | VECTOR | 1.000 | 377 | 936 | 有符号的日度做空活动指标（正 = 做空增加/拥挤，负 = 回补） |
| `rsk60_last` | VECTOR | 1.000 | 768 | 1969 | 快照时刻最近一次观察到的借/贷利率 |
| `rsk60_offer` | VECTOR | 1.000 | 919 | **2395** | 空方支付的综合借券费率（borrow 侧） |

**拥挤度读法**：数据集级 aC 1984 是「字段 aC 合计」量级；真正决定残余 alpha 的是字段级——
`lending_fee_bid_rate` 仅 168（**全 5 字段最低，且远低于同族 offer 2395**），
说明「lend 侧的出借报价」与「borrow 侧的借入成本」虽然经济上镜像，**被开采程度差 14 倍**。
波 1 实测两者性能几乎相同（S 2.21 vs 2.23）⇒ 低 aC 字段能吃到的溢价与高 aC 字段一样，本轮主用 `lending_fee_bid_rate`。

## 3. 机制映射（学术锚 → 字段 → 构造）

| 机制 | 学术锚 | 字段 | 方向 | 波 1 实测 |
|---|---|---|---|---|
| **M1 借券费水平 = 卖空约束溢价** | D'Avolio (2002) *The market for borrowing stock*, JFE；Drechsler–Drechsler (2016) | `lending_fee_bid_rate` / `rsk60_offer` / `rsk60_last` | 高费率（难借、被卖空做空）= 未来跑输 ⇒ **取负** | **成立**：四臂 S 2.19–2.23 |
| M2 费率变化（收紧/放松） | 同上（约束的边际变化） | `ts_delta(fee, 22)` | 费率上升 = 卖空压力上升 ⇒ 取负 | **不成立**：S −0.50（符号反了且弱） |
| M3 自有史异常度 | 无 | `ts_zscore(fee, 252)` | 相对自身历史异常高 ⇒ 取负 | **不成立**：S 0.21 |
| M4 做空拥挤度流量 | Boehmer et al. (short selling) | `rsk60_crowding` 的 5/22 日均值与 zscore | 拥挤上升 = 看空 ⇒ 取负 | **全灭**：−0.11 / −0.30 / −0.17 |
| M5 粒度：更细分组 | — | `group_rank(..., subindustry)` | — | **破坏信号**：2.21 → 0.79，SUB 0.32 |

**核心结论（波 1）**：**只有费率的「水平」是信号；费率的变化、自有史归一、拥挤度流量全是噪声**
（四族 6 臂全部 |S| ≤ 0.5）。这与「卖空约束是慢变量」一致，也与本 book 在 USA 反复验证的
「慢变量水平项 > 变化项」同向。

## 4. 类型与预处理硬约束

- **5/5 全 VECTOR** ⇒ 任何 `ts_*` / `group_*` / `rank` 前必须先 `vec_*` 聚合；
  直接对 VECTOR 套 `ts_backfill` 会整批 `CANCELLED`（`does not support event inputs`）。
- **Aggregation choice**：`vec_avg` 是主口径（同日多打印取均值）；`vec_max` 作稳健性对照
  （实测与 `vec_avg` 性能等价：2.21 vs 2.21）。
- **补值**：`ts_backfill(..., 66)`；窗口白名单 `[1,5,22,66,252,504,1008,1260]`。
- **nanHandling 必须 ON**（VECTOR 批的强度闸；缺省 OFF 会静默塌成零持仓）。
- `rsk60_datatime` 是时间戳元数据，**不进任何表达式**（会引入纯噪声与 CW）。
- 单位：全部为年化费率（无量纲率），可直接相减/取负；`unitHandling=VERIFY` 下不要加常数。

## 5. 波 1（10 臂，预注册：单字段 ATOM × 5 机制族）

设置：USA / TOP3000 / D1 / **SUBINDUSTRY** / decay 8 / trunc 0.08 / nanHandling ON / 2014–2023。
multisim `1LyRWUeM44tw9XsoLZZ9DOn`；表达式 `tracking/USA/runs/usa_rsk60_w1.txt`。

| # | 核心 | alpha | S | F | TO | RET | 2Y | **SUB** | RN | L/S | RA 失败 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | `-gs(backfill(vec_avg(offer),66),sector)` | `Vkdm1WZM` | **2.23** | **4.09** | 5.13% | 42.0% | 3.18 | 0.87 | 2.23 | 2079/415 | SUB |
| 2 | `-gs(backfill(vec_max(fee_bid),66),sector)` | `QPYNZ8NK` | 2.21 | 4.02 | 5.19% | 41.3% | 3.18 | **0.88** | 2.21 | 2077/426 | SUB |
| 3 | `-gs(backfill(vec_avg(fee_bid),66),sector)` | `xA12OZVN` | 2.21 | 4.03 | 5.17% | 41.6% | 3.18 | 0.87 | 2.21 | 2080/427 | SUB |
| 4 | `-gs(backfill(vec_avg(last),66),sector)` | `58jAnXr1` | 2.19 | 3.93 | 7.12% | 40.3% | 3.21 | 0.82 | 2.14 | 2209/600 | SUB |
| 5 | `-group_rank(backfill(vec_avg(fee_bid),66),subindustry)` | `O0JMQ3M7` | 0.79 | 0.62 | 4.84% | 7.6% | 1.72 | 0.32 | 0.16 | 1871/740 | S/F/SUB |
| 6 | `-gs(ts_zscore(backfill(...),252),sector)` | `XgRvm0vm` | 0.21 | 0.06 | 14.2% | 1.3% | 0.03 | 0.29 | 0.21 | 1091/972 | S/F/2Y |
| 7 | `-gs(ts_mean(backfill(crowding,5),22),sector)` | `j2ePz7PQ` | −0.11 | −0.03 | 10.9% | −0.8% | −0.33 | −0.04 | −0.22 | 1983/848 | S/F/2Y |
| 8 | `-gs(ts_zscore(backfill(crowding,5),252),sector)` | `vROpwQpd` | −0.17 | −0.02 | 48.3% | −1.0% | −0.99 | −0.28 | −0.30 | 1523/1179 | 4 闸 |
| 9 | `-gs(ts_mean(backfill(crowding,5),5),sector)` | `qMEY9RYv` | −0.30 | −0.09 | 26.6% | −2.4% | −0.83 | 0.00 | −0.48 | 1866/919 | S/F/2Y |
| 10 | `-gs(ts_delta(backfill(fee_bid,66),22),sector)` | `MP0eMrdr` | −0.50 | −0.36 | 15.1% | −7.8% | −1.04 | −0.50 | −0.42 | 1095/1412 | 4 闸 |

## 6. 归因（逐条，先结论后证据）

1. **费率水平是可交易信号，且量级罕见地强**。四臂 S 2.19–2.23 / F 3.93–4.09 / 2Y 3.18–3.21 /
   TO 5.1–7.1% / RET 40–42%，同时 `risk_neutralized_sharpe`（RN）与原始 Sharpe **逐位相同**（2.21 = 2.21）
   ⇒ 不是风格/规模/行业伪装，是独立于风险模型的横截面 alpha。
2. **lend 侧与 borrow 侧等价**：`lending_fee_bid_rate`(aC 168) 与 `rsk60_offer`(aC 2395) 的 S 差 0.02。
   ⇒ 拥挤度差异**没有**转化为性能差异；低 aC 的收益是「更可能仍是 virgin」，不是「信号更强」。
3. **`vec_avg` 与 `vec_max` 等价**（2.21 vs 2.21）⇒ 同日多打印的聚合方式不是杠杆；
   数据本身在同一快照内高度一致（也说明 `rsk60_datatime` 无信息）。
4. **变化类构造系统性证伪**：`ts_delta`(−0.50)、`ts_zscore`(0.21)、crowding 三臂全负
   ⇒ 卖空约束是**慢变量**，信号全在水平项。这一条直接砍掉了「变化/流量」整族，后续不再发。
5. **更细分组破坏信号**：`group_rank@subindustry` 从 2.21 掉到 0.79，且 RN 从 2.21 掉到 0.16
   ⇒ 一旦按 subindustry 分组，剩余部分几乎全是风险暴露。**本信号必须在 sector 或更粗的组上做**。
6. **唯一失败项是相对闸** `LOW_SUB_UNIVERSE_SHARPE`：实测线 = 0.435×S（S2.21→0.96、S2.23→0.97、S2.19→0.95），
   实测 SUB/S = 0.394（0.87/2.21）⇒ **缺 10% 相对幅度**，不是信息量上限（对比 other416 的 SUB 是真上限）。
7. **多空极度不对称**：L/S = 2080/427（83% 多头）。低费率 = 易借 = 大多数股票，所以长腿自然宽。
   这解释了 SUB 的脆弱：小市值宇宙里空腿（高费率难借名）的构成变化大。

## 7. 波 2（LOW_SUB_UNIVERSE_SHARPE 定向修复，12 臂 = 2 批 × 6 壳）

底座：`-group_zscore(ts_backfill(vec_avg(lending_fee_bid_rate), 66), sector)`，**字段与方向固定，只动壳与设置**。

**2A（中性化轴，`3bSzzH3K44EQbTwvTXOHaeX`）**：USA/TOP3000/D1/**MARKET**/decay 8/trunc 0.08
**2B（宇宙轴，`34uoeb2We4HmaM7SOF7YFqX`）**：USA/**TOP2000**/D1/SUBINDUSTRY/decay 8/trunc 0.08

两批共用同一组六个壳（`tracking/USA/runs/usa_rsk60_w2a.txt` / `..._w2b.txt`）：

| # | 壳 | 假设 |
|---|---|---|
| 1 | `-ts_backfill(vec_avg(fee),66)` | 裸水平 + 平台中性化（最贴近纯信号） |
| 2 | `-rank(ts_backfill(vec_avg(fee),66))` | 秩壳，压制小市值极值 |
| 3 | `-group_zscore(..., sector)` | 波 1 冠军（对照） |
| 4 | `-group_rank(..., sector)` | 组内秩（有界） |
| 5 | `-winsorize(..., std=4)` | 去极值（小市值费率尖峰） |
| 6 | `-rank(ts_backfill(vec_max(fee),66))` | vec_max 稳健性对照 |

**预注册判据（发批前写死）**：任一组 `SUB/S ≥ 0.435` 且 `S ≥ 1.58` 且 `F ≥ 1.0` ⇒ SUB 墙破，进 prod 探针；
若 12 臂全部 `SUB/S < 0.435` ⇒ 判定本字段在 TOP3000/TOP2000 的 SUB 墙**不可用设置层修复**，
转「换字段（`rsk60_offer` 已在波 1 同分，不算新信息）」或「换数据集」，不再加波。

**为什么不用 TOP1000**：宇宙下移的代价是样本外泛化（本书其余 USA alpha 全在 TOP3000）；
TOP2000 是中点探针，只有它也不行走才考虑 TOP1000。

### 7.1 波 2 实测结果（2026-10-23 收批）

**SUB 墙被破**：3 个 TOP3000/MARKET 臂 + 1 个 TOP2000 臂 `ra_failed_checks = []`（18 项 RA 全过）。

| 批 | alpha | 壳 | S | F | TO | RET | 2Y | SUB | SUB/S | RA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 2A MARKET | `A1Qr9Y8W` | **裸水平** `-ts_backfill(vec_avg(fee),66)` | **2.39** | **5.24** | 2.91% | 60.06% | 3.88 | **1.12** | 0.469 | **[]** |
| 2A MARKET | `1Yjle1Am` | `group_zscore(sector)` | 2.10 | 3.88 | 3.56% | 42.68% | 3.22 | 1.07 | 0.510 | **[]** |
| 2A MARKET | `MP0eOqN6` | `winsorize(std=4)` | 1.87 | 3.16 | 2.50% | 35.73% | 3.62 | 1.05 | 0.561 | **[]** |
| 2A MARKET | `LL5mWqYe` | `rank` | 0.75 | — | — | — | — | 0.34 | — | S/F/2Y |
| 2A MARKET | `npAe9Y5l` | `rank(vec_max)` | 0.75 | — | — | — | — | 0.34 | — | S/F/2Y |
| 2A MARKET | `gJWg6wVM` | `group_rank(sector)` | 0.67 | — | — | — | — | — | — | S/F/2Y |
| 2B TOP2000 | `WjLoMW0x` | `group_zscore(sector)` | 1.69 | 2.94 | 5.79% | 37.86% | 2.52 | 0.99 | 0.586 | **[]** |
| 2B TOP2000 | `vROp8J6d` | 裸水平 | 1.88 | 4.03 | 5.54% | 57.40% | 2.79 | 0.79 | 0.420 | SUB |
| 2B TOP2000 | `GrgKP39J` | `winsorize` | 1.68 | 2.92 | 4.78% | — | 2.67 | 0.75 | 0.446 | SUB |
| 2B TOP2000 | `LL5mWl31`/`ZYmd6WMQ`/`leM5dR1e` | rank/rank/group_rank | 0.59/0.58/0.50 | — | — | — | — | 0.29–0.31 | — | S/F/2Y |

**两条形状铁律（跨数据集可复用）**：

1. **`rank` / `group_rank` 会杀死本信号**（2.39 → 0.75 / 0.67）。费率水平的收益来自尾部（极难借的贵票），
   秩变换把尾部压平成均匀分布 ⇒ 收益归零。这与「排名壳更稳健」的直觉相反。
2. **中性化轴比宇宙轴更有效**：同在 TOP3000 下 MARKET（SUB 1.12）远好于 SUBINDUSTRY（波 1 的 0.87）；
   TOP2000 只到 0.79–0.99。SUB 本质是「小市值残余暴露」，**去掉行业中性化反而救活 SUB**。

### 7.2 裁决：PROD 死（2026-10-23）

`check_correlation(A1Qr9Y8W, refresh=True)`：

```
production.max_correlation = 0.9917   passes_check = false
histogram: [0.9,1] n=116   [0.8,0.9] n=390
```

`[0.9,1]` 桶 116 颗 ⇒ 生产池里已有**上百颗**同机制 alpha。按键位（D0-P）：≥0.75 即 dead_end，
0.9917 属结构性墙，**不做任何救援**（不试 hump / 不试窗口 / 不换 TOP 宇宙）。

**本数据集全线（rsk60_offer / rsk60_avg / rsk60_last / lending_fee_bid_rate）判死**：
它们共享同一个 `lending_fee` 水平机制，波 1–波 2 共 16 臂已覆盖该机制的水平 / 变化量 / zscore / 拥挤度 /
细分组的全部形态，**没有第二个正交机制可挖**。

**由此得到本波最重要的一条跨区结论**：

> **数据集的 aC / userCount 低，不代表 prod 低。决定 prod 的是「机制」在生产池里的拥挤度。**
> `lending_fee_bid_rate` 平台 aC = 168（同数据集 `rsk60_offer` 为 2395，差 14 倍），
> 且此前零条 USA 表达式用过它 —— 仍是 prod 0.9917。
> 空头约束 / 借券费率 / 流动性溢价 / 交易成本这类**经典异象**在生产池里已被挖尽，
> 「冷门数据集」在这类机制上不提供任何相关性优势。

同一轮 `other143` 冠军 `RRA97Wo0`（波 82 曾破 F 墙，但从未测过 prod）也补测：
**prod 0.8658，fail** ⇒ other143 一并判死（[0.8,0.9] 桶 n=2）。

## 8. 存档索引

- 本文件：`Claude/skills/wq-brain-ra-usa/references/_usa-risk60-field-profile-20261023.md`
- 波 1：`tracking/USA/runs/usa_rsk60_w1.txt`，multisim `1LyRWUeM44tw9XsoLZZ9DOn`，结果 `backtest_results` wave=`rsk60_w1`
- 波 2：`tracking/USA/runs/usa_rsk60_w2a.txt` / `usa_rsk60_w2b.txt` / `usa_rsk60_w2_spec.json`，结果 wave=`rsk60_w2a` / `rsk60_w2b`
- prod 实测：`check_correlation(A1Qr9Y8W, refresh=True)` = 0.9917（fail）；`RRA97Wo0`（other143）= 0.8658（fail）
- 交付报告：`output_report/USA_regular_alpha_delivery_20261021.md`（§8 起为未点亮塔补挖段）
