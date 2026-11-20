# sentiment27 判死档案 — prod-locked（2026-11-16）

**Region**: GBR / TOP700 / D1　**Dataset**: `sentiment27`（Website Popularity Rankings / Tranco）
**塔位**: sentiment 0/3（未点亮）　**判死类别**: **prod-locked（新类别）**

---

## 一、判词

sentiment27 的**唯一强信号** = 「当前 top75% 排名 − 自身 top75% 平均排名」的慢速水平 pair-diff。

它在 GBR **三项全绿**（S/F 过闸、RA 零失败、self-corr 0.15），但 **prod = 0.9394 FAIL**
（阈值 0.7，红线无豁免）⇒ **不可提交**。

死因**不是**信号弱、**不是**数据层、**不是**配置层，而是：

> 该信号与平台生产池中**某一颗母件**实质同源（直方图 [0.9,1) 桶 n=1，其余最高 0.5-0.6 桶 n=2）。

与 `GBR-ERN6-LOANLEG-LOCK`（借券腿被 OS 件占位）**同型**：信号可用但已被占位。

**复活条件**：① 该母件退役 ② 平台 prod 池变化 ③ 出现与母件正交的新字段对（本轮已验证替代字段对全部走弱，见 §四）。

---

## 二、最优读数（`LLKg15Xa`）

```text
group_rank(ts_mean(ts_decay_linear(vec_avg(snl27_top75pctranking)
                                  - vec_avg(snl27_top75pctrankingavg), 60), 5),
           subindustry)
GBR / TOP700 / D1 / MARKET / decay 8 / trunc 0.04
```

| 项 | 读数 |
|---|---:|
| Sharpe | **1.66** |
| Fitness | **1.16** |
| 2Y | **2.68** |
| sub-universe | 1.35 |
| Turnover | 0.0342 |
| Margin | **35.4 bps** |
| Drawdown | 6.33% |
| lc/sc | 326 / 325 |
| checks.fail | **[]** |
| RA 失败 | **0** |
| self-corr | 0.1542 ✅ |
| **prod-corr** | **0.9394 ❌** |
| pyramid | GBR/D1/SENTIMENT ×1.7（Single Dataset ATOM）|

同族稳健：55d `2r5apQn8` S1.65/F1.15、65d `QP02Gq5Q` S1.58/F1.07，均零 RA 失败（同族⇒同 prod）。

**逐年**（数据 2019 起步）：2014-2018 lc/sc=0；2019 S2.08 / 2020 **S−0.50** / 2021 S1.93 / 2022 S3.08 / 2023 S2.22。

---

## 三、配置阶梯（本塔唯一有效杠杆）

| 中性化 | 平滑 | S | F |
|---|---|---:|---:|
| **MARKET** | **60d + mean5** | **1.66** | **1.16** |
| MARKET | 60d | 1.63 | 1.12 |
| MARKET | 40d | 1.45 | 0.95 |
| INDUSTRY | 20d | 1.33 | 0.83 |
| SUBINDUSTRY | 10d | 1.25 | 0.76 |
| FAST | 5-10d | 0.52 | 0.19 |

- 平滑窗 45/55/60/65/75/80/120 全扫：**60d 峰值**（55-65 全区间零 RA 失败）
- `group_rank` 必频（裸信号 0.94）
- **集中度修法**：trunc **降到 0.04** + decay_linear 外**再叠 ts_mean(5)** → CONCENTRATED_WEIGHT 转 PASS（trunc 0.15 反而升成 fail）

---

## 四、替代信息源（全部走弱）

| 替代 | S |
|---|---:|
| avgranking − topranking | 0.95 |
| top50 配对 | 0.78 |
| totaldomains − totalcountrydomains | 0.56 |
| relpopularity1 − relpopularity08 | 0.51 |
| kurtosis − skewness | −0.23 |
| avgranking 单水平 / skewness 单水平 | 0.15 / 0.02 |

⇒ 换字段对不能绕开母件。

---

## 五、机制结论（可复用）

1. **短窗变化摧毁慢速水平**：同字段对加 `ts_delta(5)+hump+signed_power²`（97 赞 USA 原版模板）只有 0.28，去掉后 1.17。
2. **自相对化摧毁**：`ts_zscore(diff,252)` −0.50、`ts_quantile` −0.58；有效成分是「当前 vs 自身均值的绝对偏离水平」。
3. **FAST 档崩塌**（0.32-0.62）⇒ 第 6 次复证「注意力族不适用 FAST 定序」。
4. **配置/结构不可跨塔迁移**：同配置套 insiders12 1.06→0.63、institutions6 0.95→0.51、risk60 0.80→0.04；pair-diff 套 institutions6 全配对 −0.87~0.21（MARKET 与原生 FAST 两档皆灭）。
5. **self 低 ≠ prod 低**：self 0.15 与 prod 0.94 同时存在，只有 prod 才是平台全局池。

---

## 六、波次索引（DB）

| wave | 内容 | 结果 |
|---|---|---|
| `s2_sentiment27_forum_tpl_20261115` | 论坛+论文模板批（F1/F5/F3/F2/F4） | 全灭 max 0.31 |
| `s2_sentiment27_levelpair_20261115` | 水平化突破（去 delta） | **S1.17** |
| `s2_sentiment27_push_20261115` | 冲闸变体 | **S1.22** |
| `s2_sentiment27_fast_sweep_20261115` | FAST 档 | 0.32-0.62 |
| `s2_sentiment27_combo_20261115` | 组合腿（借券B） | 1.62 但**命中毒模式 §0，作废** |
| `s2_sentiment27_conc_fix_20261115` | trunc 0.15 修集中度 | 失败（读数不变/更差） |
| `s2_sentiment27_compliant_20261116` | 纯单集合规冲闸 | 1.25 |
| `s2_sentiment27_cfg_industry_20261116` | INDUSTRY 档 | 1.33 |
| `s2_sentiment27_cfg_market_20261116` | MARKET 档 | 1.45 |
| `s2_sentiment27_cfg_market_long_20261116` | 长窗 40-160d | **1.63** |
| `s2_sentiment27_conc_clear_20261116` | trunc0.04+mean5 | **1.66 / RA=0** |
| `s2_sentiment27_window_cfgxfer_20261116` | 55/65d + 跨塔迁移 | 邻域稳健；迁移全灭 |
| `s2_sentiment27_prodgate_20261116` | **prod 终验** | **0.9394 FAIL ⇒ 判死** |
| `s2_sentiment27_altpair_20261116` | 换信息源 | 全弱 |

累计约 **18 波 / 110+ 臂**。