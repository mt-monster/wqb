# KOR · shortinterest38 因子挖掘经验

> 手工整理（2026-09-29）。本文件按 `brain-dataset-mining-experience` 规范产出：
> 只记「字段搭配 + 结构 + 失败/成功指标」，不下"已死"结论。
> 数据源：`data/wqb.db` alphas 表（dataset_id=1149）+ 平台直轮询 `correlations/prod`。
> **注意**：以下为 IS 证据与实测 prod，不等于样本外收益；prod<0.7 仅表示未撞相关系数墙。

## 0. 数据集基本信息

| 项 | 值 |
|---|---|
| 数据集 | `shortinterest38`（平台简称 `shrt38`） |
| DB id | **1149**（region_id=2 KOR） |
| 类别 | SHORTINTEREST |
| 金字塔 | **KOR/D1/SHORTINTEREST**，multiplier **1.4** |
| 字段数 | **88**（VECTOR 为主，含 3 个 MATRIX 分组字段） |
| 合法 universe | **TOP600**（KOR 仅此一档；TOP400 报错 `Universe TOP400 is not available`） |
| 字段目录存档 | `tracking/KOR/reference/shrt38_fields.json` |

字段接口：`GET /data-fields?instrumentType=EQUITY&region=KOR&delay=1&universe=TOP600&dataset.id=shortinterest38&limit=50&offset=N`
**limit 必须 ≤50**（100 报 `Invalid query: pagination limit too high`），需 offset 分页。

## 1. ★★★ 核心结论：prod 由「分组轴」决定，与信号微结构几乎无关

本数据集是全库中**唯一把「降 prod」机制分离得如此干净**的样本。同一 sell/buy 信号概念下：

| 分组轴 | prod 区间（多种微结构实测） |
|---|---|
| `subindustry` | **0.56 – 0.58** |
| `industry` | 0.688 – 0.702 |
| `sector` | 0.75 – 0.79 |

**三重印证**：在 `subindustry` 轴下，三种完全不同的微结构给出几乎相同的 prod：

| 微结构 | alpha | prod |
|---|---|---|
| `vec_sum` 比值 | QPbxpJ8K / JjN9nG0n / qMxRnNkO | 0.5749 / 0.5753 / 0.5807 |
| `vec_avg` 比值 | e7bjnPk6 | 0.5759 |
| 净额差 `subtract/add` | vRrQ5Npr | 0.5695 |

⇒ **想在 KOR shrt38 上过 prod 闸，换分组轴（→ subindustry）比换表达式有效得多。**

配套两条次级规律：
- **窗口不敏感**：`ts_decay_linear` 窗 300/400/500/600/900/1260 在固定轴下 prod 差异 <0.01。
- **hump 不是 prod 杠杆**：dl250+sector 加 hump 后 prod 0.7682 → 0.7866（**反而略升**）。hump 的作用是压 turnover（0.19–0.20）与过 `CONCENTRATED_WEIGHT`，不是降 prod。

## 2. ★★★ 推荐配方（可直接复用）

```
表达式：hump(group_rank(ts_decay_linear(<去量纲卖空压力>, 500), subindustry), hump=0.0025)
设置  ：KOR / TOP600 / d1 / decay 20~30 / neutralization=SLOW_AND_FAST / truncation=0.02 / maxTrade OFF
```

其中 `<去量纲卖空压力>` 可任选（效果近似）：
- `divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt))`
- `divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))`
- `divide(subtract(vec_sum(sell), vec_sum(buy)), add(vec_sum(sell), vec_sum(buy)))`

**两条设置层的硬前置**：

| 设置 | 作用 | 证据 |
|---|---|---|
| `neutralization=SLOW_AND_FAST` | **绕开 `PURE_POWER_POOL_THEME` FAIL**（换轴到 subindustry 也可，但 SLOW_AND_FAST 最彻底） | 同表达式 SUBINDUSTRY/decay4 → 唯一 FAIL = PURE_POWER_POOL_THEME；换 SLOW_AND_FAST → 该 FAIL 消失 |
| `truncation=0.02` | 使 **`CONCENTRATED_WEIGHT` PASS**（此前所有腿 WARNING/FAIL） | 全部 SLOW_AND_FAST+trunc0.02 腿 CW 均 PASS |

## 3. 字段级证据

| 字段 | 类型 | 用途 | 已验证结果 |
|---|---|---|---|
| `shrt38_stk_invactsell_amt` | VECTOR | **主信号**：违规卖空额（分子） | ★★★ 全部有效候选的来源 |
| `shrt38_stk_invactbuy_amt` | VECTOR | **主信号**：违规买入额（分母） | ★★★ |
| `shrt38_stk_invactnet_buy_amt` | VECTOR | 违规净买入额 | ✗ 直接使用 S=-2.05（符号反）；取反后 **2Y 崩**，不可交易 |
| `shrt38_stk_invactnet_buy_qty` | VECTOR | 违规净买入量 | ✗ 同上（-1.59） |
| `shrt38_stk_invactsell_qty` / `invactbuy_qty` | VECTOR | 违规卖/买**量** | ✗ 量价背离 S=0.23 |
| `shrt38_stk_short_sellshort_sell_amt` | VECTOR | **真卖空额** | ✗ S=0.39/F=0.15（无效） |
| `shrt38_stk_short_sellshort_sell_qty` | VECTOR | 真卖空量 | ✗ S=0.39 |
| `shrt38_stk_short_sellshort_sell_amt_wgt` | VECTOR | 卖空成交额权重 | ✗ S=0.12 |
| `shrt38_amt_wgt` / `shrt38_tot_amt_wgt` | VECTOR | 卖空成交额权重（全） | ✗ S=-0.05 ~ 0.12 |
| `shrt38_accum_{buy,sell,net_buy}_{amt,qty}` | VECTOR | 累计买/卖/净 | 未充分测 |
| `shrt38_ytq` | VECTOR | 总做空股数 | 未测 |
| `shrt38_sector` / `shrt38_industry` / `shrt38_subindustry` | MATRIX | 分组字段（平台提供） | 见 §1（轴选择） |

**结论：只有一个信号概念成立 —— 违规卖空额 / 违规买入额的比值。** 真卖空、净买压、量价、权重四类概念在 KOR 全部无信号。

## 4. 算子级证据

| 算子/结构 | 效果 |
|---|---|
| `divide(vec_sum(S), vec_sum(B))` | ★★★ 主力结构 |
| `divide(vec_avg(S), add(vec_avg(B), 1e-4))` | ★★★ 等效（需加小量防零除） |
| `divide(subtract(vec_sum(S),vec_sum(B)), add(vec_sum(S),vec_sum(B)))` | ★★★ 净额差，等效 |
| `ts_decay_linear(x, W≥300)` | ★★★ 长窗平滑 —— **唯一能同时保 F 又压 prod 的时序算子** |
| `ts_rank(x, W)` | ✗ prod 0.78–0.87（超阈） |
| `ts_delta(x, W)` | ✗ F 崩（0.41–0.78） |
| `ts_mean(ts_zscore(x,W),5)` | △ F 高（2.2–2.4）但 prod 0.79–0.94；**在 SLOW_AND_FAST 下加 hump 后全崩（S 0.38–0.91）** |
| `ts_mean(ts_rank(x,W),5)` | ✗ 同上，S=0.38 |
| `winsorize(ts_backfill(x,20),std=4)` | ✗ S=1.47 不合格 |
| `group_rank(x, 轴)` | ★★★ 分组轴是 prod 的决定性变量（§1） |
| `hump(x, hump=0.002~0.003)` | ★★ 压 turnover 至 0.19–0.20、过 CW；**不降 prod** |
| `signed_power(x,0.5)` | 未产生独立收益 |
| `subtract(1, group_rank(x))` / `multiply(-1, ...)` | ✗ 取反后 2Y 崩（净买压方向已废） |

## 5. 已完成候选逐条记录（prod 实测）

### 5.1 已 ACTIVE（2 颗，均归属 KOR/D1/SHORTINTEREST ×1.4）

| Alpha | 表达式核心 | 设置 | 指标 |
|---|---|---|---|
| `omLjG1M5` | `group_rank(ts_mean(ts_zscore(divide(vec_sum(S),vec_sum(B)),1260),5), sector)` | SLOW_AND_FAST / dec30 / trunc0.02 / maxTrade ON | — |
| `KPNo2lgl` | `hump(group_rank(divide(vec_sum(S),vec_sum(B)), sector), hump=0.003)` | SLOW_AND_FAST / dec30 / trunc0.02 | S=2.57 / F=2.09 / 2Y=2.18 / prod=0.5504 |

### 5.2 prod<0.7 待提交池（18 颗 UNSUBMITTED + 1 颗 ACTIVE，共 19 条已测）

| Alpha | 分组轴 | 微结构 | S | F | 2Y | prod |
|---|---|---|---:|---:|---:|---:|
| `d5bMPkWY` | subindustry | vec_avg 比值 + hump0.003 | 1.71 | 1.19 | 2.28 | **0.4365** |
| `gJb2oWeO` | subindustry | vec_sum 比值 dl500 h0.003 | 1.60 | 1.04 | — | **0.5599** |
| `vRrQ5Npr` | subindustry | 净额差 dl500 | 1.76 | 1.18 | — | **0.5695** |
| `JjN9nG0n` | subindustry | vec_sum 比值 dl300 | 1.72 | 1.14 | — | **0.5749** |
| `QPbxpJ8K` | subindustry | vec_sum 比值 dl500 | 1.73 | 1.15 | — | **0.5753** |
| `omLd9oEJ` | subindustry | vec_sum 比值 dl500 h0.002 | 1.86 | 1.27 | — | **0.5755** |
| `e7bjnPk6` | subindustry | vec_avg 比值 dl500 | 1.80 | 1.22 | — | **0.5759** |
| `omLd3vPm` | subindustry | vec_sum 比值 dl600 | 1.73 | 1.15 | — | **0.5778** |
| `E5pdgOn1` | subindustry | vec_sum 比值 dl900 | 1.74 | 1.16 | — | **0.5803** |
| `qMxRnNkO` | subindustry | vec_sum 比值 dl1260 | 1.74 | 1.16 | — | **0.5807** |
| `wpZrn19l` | subindustry | vec_sum 比值 dl400 | 1.73 | 1.15 | — | **0.5813** |
| `E5pjx9q0` | industry | vec_avg 比值 h0.0025 dec20 | 2.50 | 1.85 | 2.37 | **0.6002** |
| `mLmGQEq9` | sector | vec_avg 比值 h0.0025 dec20 | 2.72 | 2.12 | 2.35 | **0.6011** |
| `akbpAj99` | industry | vec_sum 比值 dl900 | 2.27 | 1.70 | — | **0.6886** |
| `A1Np5AXd` | industry | vec_sum 比值 dl750 | 2.17 | 1.60 | — | **0.6918** |
| `rKOxJLd1` | industry | vec_sum 比值 dl400 | 2.30 | 1.74 | — | **0.6932** |
| `VkaWXGmb` | industry | 净额差 dl500 | 2.35 | 1.79 | — | **0.6932** |
| `2rwYaR5x` | industry | vec_sum 比值 dl600 | 2.28 | 1.71 | — | **0.6914** |
| `JjNAkqbn` | industry | vec_sum 比值 dl500 | 2.31 | 1.75 | — | **0.6958** |

### 5.3 prod ≥ 0.7 拒绝清单（勿再重复计算）

| Alpha | 结构 | prod |
|---|---|---:|
| `qMxRnp8K` | vec_avg dl500 industry | 0.7026 |
| `rKOqwxa9` | dl250 sector h0.004 | 0.7521 |
| `RRbOoMNg` | dl250 sector | 0.7682 |
| `Vkarb9WM` | dl630 sector | 0.7701 |
| `58zm1RMX` | ts_rank(RS,500) industry | 0.7785 |
| `xA3LoZ7m` | dl1000 sector | 0.7845 |
| `E5pjMdnG` | dl250 sector h0.003 | 0.7866 |
| `VkarLnO5` | ts_rank(RS,250) sector | 0.8689 |
| `e7bYP29g` | 净额差 industry | 0.8704 |
| `E5pjMalL` | 净额差 sector | **0.9655** |

**★ 反向规律**：`sector` 轴下 **IS 越强 prod 越高**（E5pjMalL S2.76 → prod 0.9655）。短兴趣数据集中，"最强信号"往往就是存量因子本身。

## 6. 提交链证据

- 四闸实测：`LOW_SHARPE ≥1.58` / `LOW_FITNESS ≥1.0` / `LOW_2Y_SHARPE ≥1.58` / `LOW_SUB_UNIVERSE_SHARPE`（比值闸 ≈0.571×S）。
- `CONCENTRATED_WEIGHT`：SLOW_AND_FAST + trunc0.02 下全 PASS。
- `PURE_POWER_POOL_THEME`：仅在使用普通 nu（SUBINDUSTRY/MARKET）时出现；SLOW_AND_FAST 下消失。
- `REGULAR_SUBMISSION limit=4`：**ET 日配额**。配额满时该 FAIL 排在最前，**遮挡 PROD/SELF_CORRELATION（恒 PENDING）** → 配额满期间零成本 POST 预检失效，必须改 `GET /alphas/{id}/correlations/prod` 直轮询。
- `MATCHES_PYRAMID`：本数据集全部命中 `KOR/D1/SHORTINTEREST ×1.4`（multiplier 1.4 与 DB datasets 表一致）。

## 7. 待验证 / 下一步

- `shrt38_ytq`、`shrt38_accum_*` 字段尚未系统测试。
- `subindustry` 轴的有效性未在其它 SHORTINTEREST 数据集（`shortinterest3` id=1322、`shortinterest5` id=1323）上验证 —— **若成立则为通用规律，价值极大**。
- 明文未测：`vector_neut`、`regression_neut` 等 VECTOR 专用中性化与 subindustry 轴的交互。
- 本数据集池内 prod<0.7 已 18 颗，**短期挖矿收益递减**；后续应优先把「subindustry 轴降 prod」迁移到同区域其它数据集验证泛化性。
