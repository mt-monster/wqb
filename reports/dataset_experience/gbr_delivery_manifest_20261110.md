# GBR REGULAR 交付清单（滚动更新 · 2026-11-10）

> **口径声明**：本清单只列 **prod < 0.7 且 self < 0.7 且 RA checks fail=[] 且逐年无空窗** 的件。
> prod 一律为 MCP `check_correlation(production)` 实测的**平台真值**（`source=platform / provisional=false / from_cache=false`），
> 不是平台详情缓存值。**未测 prod 的候选不进本清单**，只记在战役报告 §13。
> 更新时机：每颗新件通过全闸后立即追加。

## 一、已确认可交付（10 颗，2026-11-10 现场重核，allGate=true）

| # | alpha | 族 / 结构 | 中性化 | S | F | 2Y | TO | fails | self | **prod** |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **`rKRx0M2m`** | risk 特质残差 × 借券 | SUBINDUSTRY | 2.29 | 1.56 | 2.84 | 0.144 | 0 | 0.443 | **0.6232** |
| 2 | **`pwdd7Za6`** | 换手强度 ATOM | SUBINDUSTRY | 1.69 | 1.04 | 2.49 | 0.105 | 0 | 0.416 | **0.6238** |
| 3 | **`pwdLp9z6`** | tm_16 × 借券 | SUBINDUSTRY | 2.26 | 1.19 | 2.09 | 0.296 | 0 | 0.430 | **0.6483** |
| 4 | **`O0A6Qz7p`** | oth47 自然流量 × 借券 | SUBINDUSTRY | 2.18 | 1.52 | **3.27** | 0.114 | 0 | — | **0.6984** |
| 5 | **`leAmmre8`** | tm_17 × 借券 | STATISTICAL | **2.97** | 1.40 | 2.29 | 0.346 | 0 | 0.262 | **0.6887** |
| 6 | **`omExeqLb`** | starval 股息率 × 借券 | **REVERSION_AND_MOMENTUM** | 2.43 | 1.78 | 2.12 | 0.170 | 0 | 0.420 | **0.6143** |
| 7 | **`RREGX1kd`** | est 分析师修正 × 借券 | **REVERSION_AND_MOMENTUM** | 1.65 | 1.09 | 2.05 | 0.149 | 0 | 0.369 | **0.5940** |
| 8 | **`LLM0e20m`** | nws17 语义 × 借券 | **REVERSION_AND_MOMENTUM** | 1.75 | 1.17 | 2.12 | 0.117 | 0 | 0.404 | **0.5386** |
| 9 | **`Xg9dPpp0`** | fnd6 营业现金流 × 借券 | **REVERSION_AND_MOMENTUM** | 1.97 | 1.44 | **2.91** | 0.149 | 0 | 0.279 | **0.4000** |
| 10 | **`Jje6mrpO`** | **fnd6 留存收益 × 借券（冷腿 0.5）** | **REVERSION_AND_MOMENTUM** | 2.37 | 1.58 | 2.34 | 0.154 | 0 | 0.329 | **0.5565** |

**S 总和 21.56**｜平台 `max_mutually_below_subset_size = 10`、`all_below_threshold = true`、max 相关 **0.4633**（`O0A6Qz7p`×`RREGX1kd`）
**9 个族**：risk 特质残差 / 换手 ATOM / tm16 / oth47 / tm17 / starval / est / nws17 / fnd6（2 科目：oancf、re）
**中性化分布**：SUBINDUSTRY 4 / STATISTICAL 1 / **REVERSION_AND_MOMENTUM 5**
全部 fails=0、逐年 2014-2023 十/十无空窗无负年、算子 ≤12、组腿外×外（组腿配额 0 消耗）。
**prod 区间 0.4000–0.6984**，最佳 `Xg9dPpp0`（余量 0.30）。

### 第 9、10 席表达式（其余 8 条见 §13.48 版本）

```
Xg9dPpp0  add(group_rank(ts_zscore(divide(fnd6_newa2_oancf, alternative_market_cap_usd), 252), subindustry),
          reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_share_count_main), 250), 504), subindustry)))   # REVERSION_AND_MOMENTUM
Jje6mrpO  add(group_rank(ts_zscore(divide(fnd6_newa2_re, alternative_market_cap_usd), 66), industry),
          multiply(0.5, reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_share_count_main), 250), 504), industry))))  # REVERSION_AND_MOMENTUM
```

## 二、已剔除（prod 撞墙，不交付）

| alpha | S | prod | 原因 |
|---|---:|---:|---|
| `wpQwjWn6` | 2.10 | **1.0000** | 与生产池完全相关 |
| `1YN6MJw6` | 2.07 | **0.8311** | 撞墙 |
| `QPVeQvOg` | 2.06 | 0.8701 | 深钉 |
| `P0oALL17` | 1.74 | 0.8384 | 撞墙 |
| `Xg9A6rGl` | 1.91 | 0.8255 | 撞墙 |
| `j2Y7AbzQ` | 1.71 | 0.7645 | RISK 单集残差反转族墙 |
| `9qxOJJ1d` / `d5Wr8mzw` | 2.15 / 1.99 | 0.7640 / 0.7634 | 中钉（破墙失败） |
| `QPvRYJGr` / `mLonY3jE` / `vR17O093` | 1.96 / 1.91 / 1.66 | 0.7423 / 0.7400 / 0.7123 | d5 族墙（窗口微调无效） |
| `A1VArNzY` | 1.82 | 0.7168 | risk68 残差族墙 |

## 三、待 prod 确认（16 颗，平台账号级单并发被外部占用，队列阻塞中）

`88jV1LEW` `mLomxW71` `bl6avAXp` `3qoXwW1z` `d5W9EeKK` `O0A6Qz7p` `Xg9b5ZX0` `gJeq8XbQ` `rKRQbPPE` `9qWa6r8x`
`2rAw9o7J` `P0gv3AO7` `vR11n3xQ` `omEaWgwv` `78L9Lwrv` `pwdd7Za6`

> 这 16 颗已通过：全闸（S/F/2Y/TO/fails=0）、self <0.7、与已确认件的互相关 <0.5、逐年 10/10 无空窗。
> 只差 prod 一项。

## 四、备选池

| 备选 | S | F | 2Y | self | 障碍 |
|---|---:|---:|---:|---:|---|
| `KPJer3Z1` | 1.69 | 1.06 | 2.53 | 0.490 | 与 `pwdd7Za6` 相关 0.5047（超线 0.0047） |
| `ZYQJd133` | 1.89 | 1.26 | 2.63 | 0.444 | RISK；与 `rKRx0M2m` 0.7649 |
| `xAr3OvXm` | 1.78 | 1.01 | 2.97 | 0.225 | 与篮 0.618 |
| `9qWJr2rq` | 1.59 | 1.02 | 1.96 | 0.389 | 与 `P0gv3AO7` 0.9691 |
| `A1VN00GX` | 1.62 | 1.12 | **1.38** | 0.557 | 2Y 不足 |

## 五、口径与方法学要点（供复用）

1. **候选池分母**必须是 `db:expressions` 全量 ∪ `get_user_alphas` 实拉——单用后者会漏 90% 产量（§13.15）。
2. **入篮顺序**：全闸筛（2Y 是关键闸）→ self 本地筛（免费）→ 互相关 → prod 实测。顺序反了会浪费平台队列。
3. **prod 无法预判**：`risk_neutralized_sharpe/sharpe` 保留率与 prod 无关（15 样本证伪，§13.19）。
4. **CW 唯一解** = `ts_backfill(稀疏 VECTOR 冷腿, 250)`（§13.7）。
5. **同骨架参数变体点不亮塔**：换窗口/分组/std/decay/数据集，相关仍 0.68-0.93（§13.10）。

## 六、逐年覆盖终验（10 席全部通过 · 2026-11-11 现场重拉）

| alpha | 年数 | 区间 | 空窗年 | 负 pnl 年 | 最弱年 S | 最少持仓 |
|---|---:|---|---:|---:|---:|---:|
| `rKRx0M2m` | 10 | 2014-2023 | 无 | 无 | 0.76 | 275 |
| `pwdd7Za6` | 10 | 2014-2023 | 无 | 无 | 0.13 | 380 |
| `pwdLp9z6` | 10 | 2014-2023 | 无 | 无 | **1.58** | 270 |
| `O0A6Qz7p` | 10 | 2014-2023 | 无 | 无 | 0.03 | 426 |
| `leAmmre8` | 10 | 2014-2023 | 无 | 无 | 0.45 | 396 |
| `omExeqLb` | 10 | 2014-2023 | 无 | 无 | 1.14 | 403 |
| `RREGX1kd` | 10 | 2014-2023 | 无 | 无 | 0.48 | 370 |
| `LLM0e20m` | 10 | 2014-2023 | 无 | 无 | 0.56 | 380 |
| `Xg9dPpp0` | 10 | 2014-2023 | 无 | 无 | 0.13 | 402 |
| `Jje6mrpO` | 10 | 2014-2023 | 无 | 无 | 0.19 | 407 |

> **注**：`leAPWGX2`（原 7 席版在列）已因 IS 漂移失效（2Y 1.54 < 1.58、fails=1）于 2026-11-10 除名；`leAmngjA` 亦不在最终 10 席内。两行已删除。

## 七、字段画像存档索引

| 内容 | 路径 | 覆盖 |
|---|---|---|
| **字段画像总表** | `reports/dataset_experience/gbr_field_profiles_survey_20261109.md` | **16 个 category 全覆盖** + 关键字段级明细 + `coverage` 不可信三条铁律 |
| RISK 专项画像 | 本目录 `gbr_regular_campain_20261109.md` §13.1 | risk 5 集 40 字段全量 |
| 覆盖度审计 D1 | `gbr_coverage_audit_20261109.md` | 177 集逐集实查，`--gate both` PASS |
| 覆盖度审计 D0 | `gbr_coverage_audit_d0_20261109.md` | 73 集，28 集真未探（已搁置） |

## 七点五、裁决状态（2026-11-11，三项均为超时自动选中，待你确认或推翻）

| 议题 | 自动选中项 | 性质 | 我的执行 |
|---|---|---|---|
| 20 席目标口径 | 接受 10 席结项 | **需你确认** | 未把目标标记为完成——原定 20 席、实交 10 席，目标未达成；等你明确后再定 |
| 是否提交这 10 席 | 暂不提交 | 安全项 | 已执行：10 颗维持 UNSUBMITTED，未调用任何 submit 接口 |
| 塔混配额读法 | 按「组合类型 ≤5」 | 需你确认 | 按此读法现有 10 席合规（4 类）；按件数读则为 7 件超配 2 件 |

**注意**：IS 指标存在漂移先例（`leAPWGX2` 当日 2Y 2.38→1.54、fails 0→1）。若日后决定提交，**必须逐颗重核**当次 S/F/2Y/fails，不得引用本清单的历史读数。

**命名规则**：`<region小写>_<dataset或主题>_<campain|survey|manifest>_<YYYYMMDD>.md`（历史沿用 `campain` 拼写不改）。
**目录约定**：报告 → `reports/dataset_experience/`；审计/探针产物 → `data/dataset_assets/`。

## 八、调优经验摘要

### 8.1 结构决定 prod

| 结构 | prod 过墙率 | 证据 |
|---|---:|---|
| 主腿 × 借券冷腿（`ts_backfill(vec_sum(loaned_share_count_main),250)`） | **4/4** | prod 0.6232-0.6984 |
| 换手强度 ATOM（`transaction_count ÷ volume`） | **1/1** | prod 0.6238 |
| 其它纯 ATOM（tm_* / imb5 / nws* / est） | **0/7** | 0.7068-1.0000 |

真因 = 信息源在生产池的**稀疏度**（必要）+ **经济含义成立**（充分）。

### 8.2 四条扩席杠杆

| # | 杠杆 | 效果 | 备注 |
|---|---|---|---|
| 1 | 窗口 + 分组轴**同时**改 | 相关 −0.5 量级 | 单改无效（0.68-0.93） |
| 2 | 冷腿权重微调（0.3-0.7） | 相关 −0.01~−0.03 | 连续旋钮，S 代价小 |
| 3 | **换中性化档**（5-7 档） | **prod −0.12** | ★ 把 0.77 压到 0.699 |
| 4 | 三腿（×imb5/news） | 失败 | CW / 相关拉不开 |
| — | 换冷腿字段 | 失败 | 全部崩（S 1.38-1.69） |

### 8.3 三个反直觉（必须记住）

1. **prod 与 IS 指标负相关**：S 最高的 `QPv8xWe5`(3.02) prod 最差(0.8199)；S 最低的 `leAmngjA`(2.66) prod 最好(0.6990)。按 S 挑版本会选到最差的。
2. **相关达标 ≠ prod 过墙**：`O0A33RW7` 相关 0.4805 达标但 prod 0.8079 撞墙（同日 3 次实证）。
3. **每族只容 1 席**（不是 2）：6 个族的第 2 席全部 0.607-0.9596。

### 8.4 CW（CONCENTRATED_WEIGHT）的唯一解

`ts_backfill(稀疏 VECTOR 冷腿, 250)` 填稠密。truncation 0.15 / group_neutralize(densify()) / 冷腿降权 0.5-0.3 / hump=0.005 **全部无效**（CW 是布尔判定，无阈值余量）。

### 8.5 覆盖度判据（不要重犯）

- `coverage` 三层都**不可判**数据存在性；反例 `techindi_model` cov=0 却有 399 字段、贡献 2 席。
- 判存在性看 `/data-fields` 目录 + 探针 `longCount/shortCount`。
- 判死看**连续多年空窗**（`leAgVON2` 因 2014-2016 三年空窗剔除），不是「不满 10 年」。