# GLB 战役：篮降 9 颗 + 死路清单复核（2026-11-02）

region=GLB / delay=1 / universe=MINVOL1M / REGULAR。目标 20 颗，已提交 0 颗。

---

## 一、本轮最重要的三件事

### 1. 篮从 11 降到 9（两颗判死）

| alpha | 塔组合 | S | F | 2Y | prod | 判定 |
|---|---|---|---|---|---|---|
| `6Xd8dgzL` | EARNINGS+OTHER | 2.67 | 1.56 | 3.31 | **0.7204 ❌** | 死（n([0.7,0.8))=2）|
| `O0AYlm2J` | OTHER 单塔 | 4.15 | 1.93 | 3.21 | **≈0.76 地板 ❌** | 死（见 §2 更正）|

**`6Xd8dgzL` 的死因是门控腿选错，不是骨架错**：它的门控 `ern3_pre_interval` 此前已实测 **0.7599**（即 `9qxvmnlq`），我在组篮时漏查了这条已知失败门控。
同骨架换成干净门控 `fnd44_jones_cf_accruals` 的 `d5WqeQbx` 只有 **0.5846** —— 同一信号腿、同一 `@country` 轴，仅门控不同，prod 差 0.14。

> **⇒ 纪律补充：往篮里加候选前，必须拿它的门控字段去比对"已知失败门控清单"，不能只看信号腿。**

| 已知干净门控 | prod |
|---|---|
| `fnd44_jones_cf_accruals` | 0.5846 |
| `fnd44_perc_accruals` | 0.6479 |
| `vec_avg(rsk60_crowding)`（22d / 5d） | 0.6385 / 0.6638 |
| `snt21_2neg_conf_low_394`（66d） | 0.6585 |

| 已知失败门控 | prod |
|---|---|
| `ern3_pre_interval` | 0.7599 → 本次复现 0.7204 |
| `snt21_2neg_conf_up` | 0.754 |
| `scl12_sentiment` | 0.719 |
| `nws73_headlines` | 0.8124 |
| `rsk60_offer` | 0.7954 |

### 2. 更正：`0.7724` 不属于 `O0AYlm2J`（registry 归因错误）

死路条目 `GLB-OTHER-TOWER-PROD-FLOOR-076-20261101` 的 evidence 写 `O0AYlm2J: prod 0.7724, n=10`。反查 `alpha_corr_cache` 定位到真正来源：

| alpha | 表达式差异 | prod | n([0.7,0.8)) | n_total |
|---|---|---|---|---|
| **`1YNbY6ek`** | 同骨架，`ts_zscore(..., 252)` | **0.7724** | **10** | 914451 |
| `xAr6JKVp` | 同骨架，`@ industry` | 0.762 | — | — |
| `3qoz2G9g` | `subtract(fifth, third)` @ 504 | 0.7607 | 6 | — |
| `O0AYlm2J` | `ts_zscore(..., 504)` @ `country` | **未实测** | — | — |

`(0.7724, n=10)` 与 `1YNbY6ek` 完全吻合 ⇒ registry 把 252 窗口件的实测值挂到了 504 窗口件头上。

**但结论不变**：`O0AYlm2J` 是 **OTHER 塔裸信号腿**，正是死路 rule ① 明令"未测即可按 0.76 地板预判为死"的那一类；同族四个实测兄弟 0.7607 / 0.762 / 0.7724 / 0.8009 无一例外越线，`n([0.7,0.8))` 均 ≥6（拥挤型，不扫窗口）。⇒ 按规则判死，不占用 prod 队列。

> **⇒ 纪律补充：registry payload 的 evidence 字典可能张冠李戴。引用前必须用 (prod 值, n_070_080) 这对数去 `alpha_corr_cache.prod_records` 反查真实 alpha_id。**

### 3. w168（analyst11 ESG 单塔）FAIL 0/6 —— 年频字段模板塌缩

6 条结构互异模板，全部 REJECT（S −0.17~0.52，fRA 7–8）：

| alpha | 模板 | S | F | TO | 2Y |
|---|---|---|---|---|---|
| `1YNg9RO6` | 水平·国家组内 | 0.15 | 0.01 | **9.21%** | 0.67 |
| `E56K7MNr` | 父子背离 | **0.52** | 0.07 | **9.24%** | −1.08 |
| `xArn6oVn` | E−G 洗绿价差 | −0.17 | −0.01 | **9.22%** | 0.74 |
| `QPvQJAOG` | `ts_delta(...,252)` 长期动量 | 0.00 | null | **0.00%** | null |
| `KPJL0pvg` | `ts_rank(...,252)` 长期分位 | 0.03 | 0.00 | **9.22%** | 1.06 |
| `Jjedwko2` | 子支柱尾部非线性 | 0.12 | 0.01 | **9.20%** | 0.71 |

**核心机理**：ESG 字段年度更新 ⇒ 六种**结构完全不同**的模板给出**同一个周转率** 9.2%，`ts_delta(...,252)` 更直接退化为 turnover 0.00。周转率一致 = 六种经济假设最后都塌缩到同一份"年频变动"信息 —— 模板多样性被数据频率抹平。

> **⇒ 可迁移判据：年频字段做日频 alpha，会出现"多模板同 turnover"的指纹。turnover 在多结构模板间几乎相同（差异 <0.05%）即可直接判死，不必等全部回测。**

---

## 二、π型结构：能过 prod 的候选长什么样

篮内 5 颗已过 prod 的候选，表达式形状**全部**是：

```
trade_when(rank(ts_mean(<非trio门控字段>, W)) > 0.7,
           signed_power(subtract(group_rank(<OTHER 图像信号>, <轴>), 0.5), 0.5),
           <退出条件>)
```

| alpha | 门控腿 | 信号腿 | 轴 | neut | prod |
|---|---|---|---|---|---|
| `QPvJ6KVw` | `vec_avg(rsk60_crowding)` @22 | `single_bucket_20day_..._2` | market | FAST | 0.6385 |
| `npv9WLVE` | `vec_avg(rsk60_crowding)` @5 | `single_bucket_20day_..._2` | market | SUBIND | 0.6638 |
| `RRE3O8r1` | `fnd44_perc_accruals` @22 | `single_bucket_5day_...` | country | FAST | 0.6479 |
| `d5WqeQbx` | `fnd44_jones_cf_accruals` @22 | `single_bucket_20day_..._2` | country | FAST | 0.5846 |
| `j2Yg2q9j` | `snt21_2neg_conf_low_394` @66 | `probability_label1_2quantile_20day` | country | SUBIND | 0.6585 |

**机理**：`trade_when` 把持仓切成稀疏（大部分时间空仓）⇒ 与生产池的低维重叠被削掉。这是目前唯一实测有效的降 prod 手段。

对照反例（裸信号、无门控）：
- `O0AYlm2J` OTHER 裸信号 → 0.76 地板
- `kqNrmA9g` PV 裸信号 → prod 待测

---

## 三、覆盖核查（三颗待验，全部十年无空窗）

| alpha | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 判据 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `kqNrmA9g` | 5406 | 5622 | 5416 | 5744 | 6193 | 5731 | 5907 | 7347 | 6989 | 6184 | ✅ 全 pnl>0 |
| `mLoqmkd5` | 4337 | 4530 | 4407 | 4598 | 4957 | 4600 | 4915 | 5967 | 5792 | 5054 | ✅ 全 pnl>0 |
| `xArnqeAw` | 3946 | 4054 | 3895 | 4222 | 4633 | 4266 | 4417 | 5430 | 5208 | 4549 | ✅ 全 pnl>0 |

（表内数字为各年 `longCount`；三颗 10/10 年 pnl 均为正，无连续空窗。）

### `kqNrmA9g` 推翻了一条死路结论

死路 `GLB-PVPRECLOSE-RECOMPUTE-2Y-KILL-20261027` 断言「PV pre_close 30m 价格路径族天花板 S 2.05，fitness 与 2Y 双闸结构性不过」。

但它测的是**正向** `group_zscore(ts_decay_linear(x,3), country)`。`kqNrmA9g` 是**负号**版本：

```
-group_zscore(ts_decay_linear(mean_high_price_return_30m_pre_close_2, 3), country)
S 3.00 / F 1.40 / TO 47.33% / 2Y 2.65 / sub 1.74 / returns 10.34% / dd 3.17% / fRA 0（12 项全 PASS）
2014 sharpe 4.86 → 2023 sharpe 2.62，十年全正
```

**经济含义**：尾盘最后 30 分钟创高后回落 = 收盘前买盘衰竭 ⇒ 次日跑输。是反转信号，不是动量信号。

> **⇒ 纪律补充：判死"某族天花板"时必须记录测试的**方向（sign）**。有方向性的族可能一个方向死、另一个方向活。**

---

## 四、当前库存：9 颗（5 确认 + 4 待验）

| # | alpha | 塔组合 | S | F | TO | 2Y | sub | prod | 状态 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `QPvJ6KVw` | RISK+OTHER | 3.19 | 1.59 | 28.97% | 3.43 | 1.84 | **0.6385** | ✅ |
| 2 | `npv9WLVE` | RISK+OTHER | 3.08 | 1.42 | 60.83% | 3.19 | 2.38 | **0.6638** | ✅ |
| 3 | `RRE3O8r1` | FUND+OTHER | 2.89 | 1.73 | 16.02% | 2.13 | 1.71 | **0.6479** | ✅ |
| 4 | `d5WqeQbx` | FUND+OTHER | 2.71 | 1.43 | 7.55% | 2.68 | 1.64 | **0.5846** | ✅ |
| 5 | `j2Yg2q9j` | OTHER+SENT | 2.73 | 2.02 | 14.69% | 2.85 | 2.22 | **0.6585** | ✅ |
| 6 | `9qxJgv5x` | OTHER 单塔 | 2.38 | 1.36 | 5.10% | 3.01 | 1.60 | 测量中 | ⏳ |
| 7 | `mLoqmkd5` | INST+OTHER | 2.76 | 1.89 | 13.76% | 2.73 | 2.10 | 未测 | ⏳ |
| 8 | `xArnqeAw` | OTHER+SENT | 2.74 | 1.42 | 21.24% | 2.36 | 1.87 | 未测 | ⏳ |
| 9 | `kqNrmA9g` | **PV 单塔** | 3.00 | 1.40 | 47.33% | 2.65 | 1.74 | 未测 | ⏳ |

去掉：`E5672lMG`（0.7811）、`LLMaXwv6`（0.8723）、`6Xd8dgzL`（0.7204）、`O0AYlm2J`（0.76 地板）
最紧两对：`RRE3O8r1↔d5WqeQbx` = 0.6741（余量 0.0259）、`j2Yg2q9j↔xArnqeAw` = 0.6555（余量 0.0445）⇒ 必须相邻提交并立即读回平台 self。

### 配额账

| 两塔组合 | 已用 | 上限 | 余量 |
|---|---|---|---|
| RISK+OTHER | 3（含 1 死 `E5672lMG`） | 3 | **0 满** |
| FUND+OTHER | 2 | 3 | 1 |
| OTHER+SENTIMENT | 2 | 3 | 1 |
| EARNINGS+OTHER | 1（死 `6Xd8dgzL`） | 3 | 2 |
| INST+OTHER | 1 | 3 | 2 |
| **组合名** | **5** | **5** | **0 满** |

单塔免配额：`9qxJgv5x`、`kqNrmA9g`（以及已死的 `O0AYlm2J`）。

---

## 五、20 颗的算术账（本轮修正后）

```
两塔：现有 9 席 + 余量 6 席 = 15 席上限（5 组合名 × 3）
单塔：kqNrmA9g(PV) 1 颗 + 其他单塔若干（免配额，但需与 15 席互相关 <0.7）
```

**结论：要靠单塔路径才能突破 15。** 而本轮把两条单塔路径各证伪一条：

| 单塔路径 | 状态 | 依据 |
|---|---|---|
| OTHER 单塔裸信号 | **死** | prod 地板 0.76，9 颗实测无一过线 |
| ANALYST 单塔（analyst11 ESG） | **死** | w168 0/6，年频塌缩 |
| PV 单塔 | **待验** | `kqNrmA9g` prod 未测（本轮最关键的单个未知数）|
| PV/MODEL/RISK 单塔（其他字段族） | **未试** | 尚未开波 |
| 非 trio 塔单塔（MACRO/INSTITUTIONS/NEWS/INSIDERS/FUNDAMENTAL） | **未试** | 字段覆盖普遍薄 |

**⇒ 下一步派发的判据全部押在 `kqNrmA9g` 的 prod 上**：
- 若 <0.7 ⇒ PV 单塔可行 ⇒ 立刻开 PV 单塔波（`intraday_pv_feats` 586 字段，且已知"负号反转"这一有效方向）
- 若 ≥0.7 ⇒ PV 裸信号也饱和 ⇒ 单塔路线基本封死，20 颗必须先把组合名上限从 5 放宽到 ≥7

---

## 六、本轮仍未解决

1. **提交授权**：2026-11-01 起 5 次问卷全部 `explicitUserConfirmation=false`（Goal 模式 60s 超时自动选中）⇒ 在正文请示，不再发问卷
2. **组合名上限 5**：已满，不放开则两塔封顶 15
3. **`leading gap` 口径**：更严口径下篮会再降（`QPvJ6KVw`/`npv9WLVE` 2014 空窗）
4. `mLoqmkd5` investability_ratio = 0.4565（容量衰减过半，软指标）
5. `npv9WLVE` 双薄：TO 60.83%（距 70% 仅 9.2 点）、self 0.6644（距 0.7 仅 0.036）
6. `9qxJgv5x` 2020 年全年亏损（sharpe −1.41）
