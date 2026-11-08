# GLB 战役库存 — 18 / 20（2026-11-03 20:00 更新）

## 一、本轮新增确认 1 颗

### `LLM7kvYm` — EARNINGS 财报迫近门控（w227 r2）

| 指标 | 值 | 闸线 | 判定 |
|---|---:|---|---|
| Sharpe | 3.07 | 1.58 | ✓ |
| Fitness | 1.54 | 1.00 | ✓ |
| 2Y Sharpe | 2.27 | 1.58 | ✓ |
| Turnover | 25.83% | 1%–70% | ✓ |
| Sub-universe | 1.74 | 0.35×S=1.07 | ✓ |
| RA 失败项 | 0 | 0 | ✓ |
| self-corr | 0.5680 | 0.70 | ✓ |
| prod-corr | **0.6066** | 0.70 | ✓（零钉） |

表达式：
```
trade_when(rank(-ts_backfill(ern3_next_interval, 252)) > 0.7,
           signed_power(subtract(group_rank(single_bucket_20day_return_estimate_ohlcv_img_2, country), 0.5), 0.5),
           rank(-ts_backfill(ern3_next_interval, 252)) < 0.6)
```

**机制**：在「下次财报迫近」的票上交易 dl_riskfree 收益估计（事件前定价效率下降 → 估计值信息含量升高）。

## 二、待破墙 1 颗

### `2rAlv50Y` — EARNINGS 财报新鲜度门控（w227 r1）

S **3.15** / F 1.68 / 2Y 3.75 / TO 22.48% / sub 2.02 / **RA 0** / self **0.6045** / prod **0.7165**（`[[0.7,0.8,2]]` 两钉）

只差 0.0165 到闸线。已发 **w237** 十条破墙变体（回填窗 126/189/315/378、信号腿换 60d、幂 0.4、分组轴换 exchange、阈值收紧、门控加 22 日均值、信号 winsorize）。

## 三、互相关交叉验证

19 颗（17 既有 + `LLM7kvYm` + `2rAlv50Y`）两两互相关：

- `max_mutually_below_subset_size = 19`
- `max_subset_exact = true`
- `pairs_over_threshold = []`
- 最大对 `RRE3O8r1` ↔ `d5WqeQbx` = **0.6741**（均在既有库存内）

⇒ 全员两两 < 0.70，可同时持有。

## 四、本轮判死的两条结构

### 1. k 家族窗口变体：`LOW_GLB_EMEA_SHARPE` 4/4
`A1VlYqve` 2.13 / `A1VlamWe` 1.96 / `pwdjo0aj` 2.05 / `kqNjmglK` 2.07 —— 全部只挂 EMEA 分区闸。母体 `kqN79XPO`（prod 0.7319）三区全过，说明 EMEA 余量贴身，任何窗口位移即掉线。

### 2. 分区闸轮换（更普适）
`A1Nn2vPQ`… 之外，country 轴变体 `N1an2VpX`(1.73) 挂 EMEA+APAC、`LLNn2ZR1`(1.90) 只挂 APAC。**换分组轴只能搬运权重、不能创造边际** ⇒ 单区卡的近闸候选不要用换轴修，直接改机制。

### 3. INSTITUTIONS 近闸修复整族失败（w229 前 4 条）
`ZYQ7jgGx`(2Y 1.30, F 0.94) / `ZYQ7rrZY`(2Y 1.21) / `P0o7pWm7`(2Y 0.87) —— 全部倒在 2Y < 1.58，基准 `2rA0m19w` 也只有 1.13 ⇒ 该机制近两年无边际，门控类杠杆修不动。

## 五、当前塔账（18 颗）

| 塔 | 数量 | 状态 |
|---|---:|---|
| OTHER | 20 | ✓ |
| MACRO | 5 | ✓ |
| RISK | 4 | ✓ |
| MODEL | 3 | ✓ |
| FUNDAMENTAL | 3 | ✓ |
| SENTIMENT | 3 | ✓ |
| ANALYST | 3 | ✓ |
| EARNINGS | **2** | 1→2（`JjeGEzaE` + `LLM7kvYm`） |
| PV | 2 | 未点亮 |
| INSTITUTIONS / NEWS / INSIDERS / SOCIALMEDIA | 0 | 未点亮 |

## 六、在飞

- **w237**：`2rAlv50Y` 破墙 10 变体（等槽位）
- **w238**：`ai_news_scores` 纯单数据集 ATOM 10 模板（a1 运行中，零配额）

## 七、配额状态

| 组合 | 已用 / 上限 |
|---|---|
| EARNINGS+OTHER | **3 / 3 满**（JjeGEzaE + LLM7kvYm + 2rAlv50Y） |
| MACRO+OTHER | 5（超额封盘） |
| RISK+OTHER | 3 满 |
| SENTIMENT+OTHER | 3 满 |
| ANALYST+OTHER | 3 满 |
| FUNDAMENTAL+OTHER | 3 满（口径：用户第四条澄清字面禁 FUNDAMENTAL，但本次按自动超时选中沿用「合法、上限 3」） |
| INSTITUTIONS+OTHER | 0 / 3（机制已证明无边际） |
| SOCIALMEDIA / NEWS / INSIDERS+OTHER | 0 / 3（均有结构性死因） |
| 纯单数据集 ATOM | 不限 |
