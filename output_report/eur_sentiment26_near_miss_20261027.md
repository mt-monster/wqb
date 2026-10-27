# EUR 最接近交付的一颗：`JjejYA3e`（8 门过 7 门）

> 2026-10-27 02:40｜数据集 `sentiment26`（SENTIMENT）｜**唯一卡点 = prod 0.7534**
> 这是 EUR 迄今最接近 RA 交付的一颗（此前 123 集全部卡在样本 / F / 2Y / prod）

---

## 1 构造与成绩

```
if_else(greater(rank(dw), 0.85), dw, 0)
dw = multiply(rank(ts_mean(ts_backfill(vec_sum(snt26_relpopularity1), 22), 3)),
              rank(ts_mean(ts_backfill(vec_sum(snt26_relpopularity1), 22), 66)))
```

设置：EUR / **TOPCS1600** / delay 1 / **decay 1** / FAST / trunc 0.08 / nanHandling ON / maxTrade ON

| 闸 | 值 | limit | 结果 |
|---|---:|---:|---|
| LOW_SHARPE | **1.60** | 1.58 | **PASS** |
| LOW_FITNESS | **1.18** | 1.00 | **PASS** |
| LOW_2Y_SHARPE | **1.92** | 1.58 | **PASS** |
| LOW_SUB_UNIVERSE_SHARPE | **1.21** | 0.85 | **PASS** |
| LOW_ROBUST_UNIVERSE_SHARPE | **0.98** | 0.70 | **PASS** |
| LOW_TURNOVER | 3.98% | 1% | **PASS** |
| HIGH_TURNOVER | 3.98% | 70% | **PASS** |
| CONCENTRATED_WEIGHT | — | — | **PASS** |
| MATCHES_PYRAMID | — | — | **PASS** |
| CLUSTER_TEST | 1.44 | 1.58 | WARNING（非 FAIL） |
| **SELF_CORRELATION** | **0.275** | 0.70 | **PASS** |
| **PROD_CORRELATION** | **0.7534** | 0.70 | **FAIL（唯一）** |

TO 3.98% ｜ returns 6.85% ｜ margin **34.5bp** ｜ PnL 单期约 0.3%

---

## 2 prod 是「单点对手」

直方图（阈值 0.7）：

```
0.7–0.8 :  1 颗   ← 唯一对手 0.7534
0.6–0.7 :  6 颗
0.5–0.6 : 29 颗
0.4–0.5 : 338 颗
```

按 memory §13：「histogram 只有极少数分桶有计数 ⇒ **单点对手，去相关可行性高于整段抬升**」。
所以本轮针对它做了三条真降法的穷举。

---

## 3 三条真降法全部试尽

### 3.1 改读数方式（16 个变体）

| 杠杆 | 取值 → S |
|---|---|
| **稀疏门控 q** | 0.80 → 1.46｜**0.85 → 1.54**｜0.875 → 1.38｜0.90 → 1.21｜0.925 → 0.51｜无门控 → 0.98 |
| **短窗 WS** | 5 → 1.54｜**3 → 1.60**｜2 → 未测 |
| 长窗 WL | 66 → 1.60｜126 → 1.53 |
| **decay** | 4 → 1.54｜2 → 1.55｜1 → **1.56**（配 w3 到 1.60）｜0 → 1.56 |
| truncation | 0.08 → 1.54｜0.04 → 1.55｜0.02 → 1.55（**死参数**） |
| universe | TOPCS1600 → 1.60｜TOP2500 → 1.17 |

**两个关键发现：**
1. **门控 0.85 是尖峰**：±0.025 就掉 0.16（0.85→0.875 是 1.54→1.38）。以后细扫必须按 ±0.01。
2. **短窗 5→3 是决定性一步**：S 1.54→1.60，且 F/2Y/rob/sub 同步改善（不是此消彼长）。

### 3.2 换字段（19 个字段试了 9 个）

| 字段 | S | prod |
|---|---:|---:|
| `snt26_relpopularity1` | **1.60** | **0.7534** |
| `snt26_relpopularity08`（同源副本） | 1.55 | **0.7657**（更差） |
| `snt26_dltcc` | 1.27 | — |
| `snt26_skewness` | 0.85 | — |
| `snt26_kurtosis` | 0.45 | — |
| `snt26_avgranking` | −0.49 | — |
| `snt26_top25pctranking` | −0.63 | — |
| `snt26_top50pctrankingavg` | −0.39 | — |
| `snt26_top10pctranking` | −0.30 | — |

排行族全部**负向**（说明它们度量的是拥挤度而非热度，方向相反）。
同源副本 prod 0.7657 比原字段更高 ⇒ **换字段不降 prod**。

### 3.3 改何时交易（4 个变体）

用同数据集内的 `totaldomains` / `avgranking` 做 `trade_when` 门控（保住 ATOM=1）：

| 变体 | S |
|---|---:|
| `tw_domvol`（域数量波动率 > 0.3） | 1.50 |
| `tw_domlvl`（域数量水平 > 0.4） | 1.49 |
| `tw_rkvol`（ranking 波动率 > 0.3） | 1.32 |
| `tw_domvol4`（> 0.45） | 1.47 |

**全部掉出闸**（S < 1.58）⇒ 改时机要付 S 的代价，此路不通。

---

## 4 判定：机制级 prod 地板，封闭

两个可过 S 的形态（relpopularity1 / relpopularity08）prod 分别是 **0.7534 / 0.7657**，
**Δ = 0.012**，落在 memory §6 的「同族 ±0.02 ⇒ 字段结构性 prod 地板」判据内。

⇒ **同一个生产 alpha 与整个「相对热度」机制相关**，换读数 / 换字段 / 换时机都动不了。
`sentiment26` 封闭。

---

## 5 可复用的三条产出

### 5.1 闭式判死：`S_req = S × (1/F)^(2/3)`

由 `F ∝ S^1.5` 推出。零仿真就能判断 F 轴是否可达：

| 集 | 当前 (S, F) | S_req | 实测上限 | 判定 |
|---|---|---:|---:|---|
| `analyst45` | 1.40 / 0.65 | **1.87** | 1.40 | **一眼死**（今天白跑 3 批） |
| `kqNxoL5d`（other335） | 1.82 / 1.02 | 1.79 | 1.82 | F 本来就能过 ✓ |

**用法**：候选进入设置轴扫描**之前**先算 S_req；超过该集实测可达上限的直接跳过。

### 5.2 短窗是 dw 结构里被低估的轴

`dw(WS, WL)` 的 **WS（短窗）** 在 sentiment26 上是决定性的（5→3 让 S +0.06 且五项指标同步改善），
而我在 campaign 模板里把 WS 固定成 5。**建议把 WS ∈ {3,5} 纳入默认扫描**。

### 5.3 稀疏门控的甜点极窄（再次确认）

0.80 → 1.46、**0.85 → 1.54**、0.875 → 1.38。±0.025 掉 0.16。
⇒ 门控细扫必须 **±0.01 步长**，且**不可跨形态复用**（memory 早有记录，这次是其第二次实证）。

---

## 6 复现

```bash
python tools/_snt26_probe.py --dry-run   # 看计划（6 轮 28 条）
python tools/_snt26_probe.py             # 断点续跑
```
台账：`results/_snt26_ledger.json`｜候选：`JjejYA3e`
