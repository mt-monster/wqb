# KOR 字段画像 · 适用模板 · 回测结果总表

> **本文是「查表用」的实证汇总**，与 [`_kor-gatebreak-evidence.md`](_kor-gatebreak-evidence.md)（逐闸破法数值）
> 和 [`_kor-campaign-log.md`](_kor-campaign-log.md)（历史裁决）分工：
> 本文回答三个问题 —— **① 这个字段能不能用（画像）② 该套哪个模板 ③ 别人跑到过什么水平（基线）**。
>
> 数据来源：2026-10-17/18 单次战役（约 215 次仿真，KOR/TOP600/D1），台账
> `results/mining_ledger/alpha_ledger.jsonl`（507 行）。**所有 S/F/TO/2Y/prod/self 均为平台实测值，非推算。**
> ⚠ 区域锁定：本文全部结论仅对 **KOR/TOP600/Delay=1** 成立，换区须重扫。

---

## 一、字段画像

### 1.1 三条跨数据集通用律（先看这个，再看单表）

| # | 规律 | 证据 | 用法 |
|---|---|---|---|
| **F-1** | **只有「变化量 / 修正量 / 意外度」类字段有信号；水平量字段无信号** | `analyst_factor_signals`：change/revision 类 S 1.40–1.66，而 `cagr_*`/`*_consensus_value`/年份差分 0.88–1.06 全灭；`institutions6`：水平量 S 0.15–0.5，只有 `ts_delta` 类到 \|S\| 0.79 | 进新数据集**先筛变化类字段**，水平量直接跳过，省 1 次仿真/字段 |
| **F-2** | **覆盖率（coverage）不构成可用性保证** | `institutions6` cov **0.9996** 却全族 \|S\| ≤ 0.8；`sentiment21` os_is 0.7725 全区最高、实测 S 0.02；反之 `pv47` cov=0 信号最强（GBR） | `cov` 只判「能否回测」，**绝不作为信号判据** |
| **F-3** | **字段名自解释 ≠ 本区可用** | `analyst_factor_signals` 59 字段实测有效仅约 2 个；`eps_y1_estimate_change_3mo` 与 `eps_revision_magnitude` 描述几乎相同，S 差 0.26 | 必看 `description`，且必实测 |
| **F-4** | **KOR 里 S ≥ 1.58 只出现在 `analyst` 与 `shortinterest` 两个塔** | 本轮共实测 13 个数据集：analyst 1.66、shortinterest 2.09；其余 11 个最高仅 0.05–1.46（risk68 0.05、news_sentiment 0.07、pv106 0.38、fund_holdings 0.53、risk71 0.58、institutions6 0.80、analyst_consensus 0.93、other553 1.46） | **进新数据集先用 1 条探针试 \|S\| 能否到 1.0**；若 <1.0 且该集无同构强字段，直接弃，别扩批 |
| **F-5** | **「已被行业中性化消掉的信息」= 系统性弱** | institutions6(0.80) / fund_holdings_panel(0.53) / risk71(0.58) / risk68(0.05) 共同点：机构持仓、风险模型残差、波动率暴露——**这些正是 INDUSTRY 中性化 + sector 分组要消掉的东西** | 遇到描述含 ownership / residual / volatility / beta 的数据集，预期 S 上限 0.6–0.8，优先度下调 |

### 1.2 逐数据集画像（本战役实测）

#### ✅ analyst_factor_signals（analyst 塔 ×1.6，cov 0.7856）

| 字段 | 类型 | cov | uc/ac | 实测最高 S | 判定 |
|---|---|---|---|---|---|
| **`eps_y1_estimate_change_3mo`** | MATRIX | 0.7856 | **30/43（最挤）** | **1.66**（带门控）/ **1.55**（ATOM） | ✅ **唯一强信号**，已用于 2 颗提交 |
| `eps_y2_estimate_change_3mo` | MATRIX | 0.7856 | 16/24 | 1.53 | ⚠ 弱于 y1，2Y 更好(2.64) |
| `eps_revision_magnitude` | MATRIX | 0.7856 | 20/26 | 1.40 | ⚠ **prod 0.6952 ✅ 但 S 机制不足** |
| `eps_y1_consensus_value` | MATRIX | 0.7562 | 7/7 | 1.03 | ❌ 水平量 |
| `eps_y2_consensus_value` | MATRIX | 0.7967 | 7/8 | 1.06 | ❌ 水平量 |
| `eps_y1_estimate_skewness` | MATRIX | 0.7967 | 2/2 | 0.97 | ❌ |
| `eps_y1_cagr_2yr` | MATRIX | 0.688 | 1/1 | 0.94 | ❌ 水平量（增长率水平） |
| `eps_y1_estimate_coeff_var` | MATRIX | 0.5754 | 1/1 | — | ⚠ 只可作分母，**覆盖率太低会压多头**(181/445) |

> **该数据集容量：只能出 1 颗。** 两两日收益相关实测：y1×y2 **0.8378**、y1×`eps_revision_magnitude` **0.8897**、
> y2 同字段换结构 **0.9936** ⇒ 换字段/门控/幂次**全部绕不开 self 闸 0.7**。

#### ✅ shortinterest38（shortinterest 塔 ×1.4，cov 0.9953）

| 字段 | 实测最高 S | 判定 |
|---|---|---|
| **`shrt38_stk_invactnet_buy_amt`** | **2.09**（ATOM + `ts_target_tvr_decay`） | ✅ **本战役最强，已提交** |
| 其余 gross / 家数 / 比率类 | ≤1.3 | ❌ **只有「净额」有效**（与 institutions6 同构：gross 买卖无信号） |

#### ❌ 其余已判死数据集

| 数据集 | 塔 | cov | 代表字段 / 表达式 | 最高 S | 死因 |
|---|---|---|---|---|---|
| `institutions6` | institutions ×1.4 | 0.9996 | `-count_institutional_sellers_security` / `quantity_*_acquired` / `ts_delta(aggregate_share_count,66)` | −0.50 / 0.15 / −0.79 | 全族 \|S\| ≤ 0.8；水平量=市值代理，变动量方向是反转、强度不足 |
| `risk68` | risk ×1.3 | 0.9914 | `rank(-rsk68_weight_volatility_short)`（低波动异象） | **0.05** | **INDUSTRY 中性化 + sector 分组已把波动/贝塔暴露消掉** |
| `pv106` | pv ×1.4 | 1.0 | `ts_delta(pv106_wli_spreadbp,22)` | **0.38**（TO 0.45） | 价差变动是纯噪声；**交易成本/滑点类字段整体无信号** |
| `other553` | sentiment ×1.6 | 0.6243 | `est_estvalue − preestvalue` | 1.46（门控）/1.34（ATOM） | **2Y 结构性弱 1.17–1.24**（ladder 多窗取最小） |
| `analyst_consensus` | analyst ×1.6 | 0.6382 | `avg_net_income_estimate − avg_net_income_3mth_prior` | 0.93 | **分析师只认 EPS，净收入修正远弱**；绝对额以 KRW 计价被规模主导 |
| `news_sentiment_transfer` | sentiment ×1.6 | **0.9654** | `ts_delta(sentiment_score_average,22)` | **0.07** | 新闻情绪变动是噪声（ATOM 形态已确认可产出，但无信号） |
| `fund_holdings_panel` | institutions ×1.4 | 0.887 | `vec_sum(boundary_transaction_total)` / `ts_delta(holder_account_total,66)` / `ts_delta(top_weighted_account_number,66)` | 0.10 / 0.53 / 0.53 | **3/8 探针，最高 0.53**。死因：边界交易把建仓与清仓加总、方向相消；广度量变动只到 0.53 |
| `risk71` | risk ×1.3 | 0.7592 | `ts_mean(dsrt,66)` / `-ts_mean(dsrt,22)` | **−0.60** / 0.58 | 残差收益在 KOR **反转而非持续**（与 Blitz-Huij-Martens 的美股结论相反），翻转后仍只到 0.58 |
| `earnings3` / `insiders5` / `other475` / `macro63` / `sentiment21` / `other571` | — | — | — | ≤1.3 | 见 `_kor-campaign-log.md` |

---

## 二、适用模板

### 2.1 主模板 P-ATOM-1（**首选**，可产出 atom）

```text
ts_target_tvr_decay(
    signed_power(
        group_rank(
            winsorize(rank(ts_backfill(F, {bf})), std={s}),
            {grp}
        ),
        {p}
    ),
    target_tvr={t}
)
```

**平台设置**：`KOR / TOP600 / delay 1 / decay 1 / neutralization INDUSTRY / truncation 0.04 / nanHandling ON`

| 参数 | 甜区 | 作用方向（实测） |
|---|---|---|
| `{bf}` 回填窗口 | **22–55** | ↑ ⇒ **prod 单调降**、S 非单调（该腿甜点 50–55，60 越界） |
| `{s}` winsorize std | **0.20–0.26** | ↑ ⇒ S 与 prod **同向升**（用来补偿幂次带来的 S 损失） |
| `{p}` 幂次 | **3.5–4.0** | ↑ ⇒ **prod 单调降**、S 近似平坦（4.0 后 S 开始掉） |
| `{t}` target_tvr | **0.22** | 精确压换手；**仅当 TO > t 时有利**，TO 已低时反而伤 S |
| `{grp}` 分组轴 | `sector`（默认）/ `industry` | 每次外层中性化**严格粗于**内层分组 |

**为什么这个模板能出 ATOM**：`ts_target_tvr_decay` 是**同表达式算子**，用来替代会引入
`BASE_MARKET` 的 `volume` 门控。实测该腿去掉门控后 S **1.60 → 1.91**、2Y **1.56 → 1.69**，
再加 `ts_target_tvr_decay(0.22)` 后 S **→ 2.09**、F **0.81 → 1.44**。
⇒ **门控不是必需品，它一直在拖累该腿。**

### 2.2 备选模板 P-COMB-1（会判 combined，**仅在 ATOM 不是目标时用**）

```text
trade_when(greater(volume, ts_mean(volume, {W})), <P-ATOM-1 的核心>, -1)
```

- `W` 对 S **严格单调递减**：66→1.41 / 22→1.51 / 10→1.57 / **6→1.60** / 5→1.60（拐点 W≈6）
- ⚠ **`volume` 属 BASE_MARKET**，只要用它就是 `combined`。判定器：`wqb.expression.atom.classify_atom`
- ⚠ 在 shortinterest 腿上该门控**有害**（S −0.31、2Y −0.13），只在分析师腿上有利

### 2.3 禁用清单（全部本战役实测，命中即省 1 次仿真）

| 禁用项 | 实测结果 | 原因 |
|---|---|---|
| `hump` | 0.0025→S 1.91；**0.006→S 0.91** | 极敏感，无中间档；只在 TO 0.28 的腿有效，TO<0.15 时**反升 prod**（0.7008→0.7331） |
| 保序变换（`quantile`/`winsorize`/`normalize`/换分组/缩窗） | prod 钉在 **0.6989–0.7081** | PC 比的是 **PnL 曲线形状**，保序变换不改排序 ⇒ 形状不变 |
| 掺腿稀释 prod | prod **先升**到 `√(a²+b²)` 再降 | 闭式：需掺入腿 **PC<0.3** 才有意义（我们的腿 0.46 会抬高） |
| `group_zscore` 代替 `group_rank` | S **0.77** | 无界权重，尾部失控 |
| `neutralization = NONE` | S 0.39，longCount 492/short 0 | 变成纯多头 |
| `nan_handling = OFF` | S **0.92** | 缺失值按 0 处理摧毁信号 |
| `vector_neut` 全正交（对高相关同族字段） | S **1.20** | 剥掉共同成分后信号所剩无几 |
| `days_from_last_change` / `is_nan` 门控 | S 0.63 / 0.84 | 限制在「真有新值」的股票后信号崩塌 ⇒ **回填覆盖本身就是信号强度来源** |
| `group_backfill` | S 1.03 + **UNITS 硬警告** | 要求 index 0 为 `Unit[]`，带量纲字段必须先 `rank` 再喂 |
| 跨区照搬配方 | IND 的「分歧度分母」在 KOR S 1.20 | 配方是**该字段专属**的，`(bf×std×pow×tvr)` 必须逐数据集重搜 |

---

## 三、回测结果及指标

### 3.1 已提交 alpha（基线）

| alpha / 名称 | 类型 | 表达式要点 | S | F | TO | 2Y | prod | self |
|---|---|---|---|---|---|---|---|---|
| **`KOR_R_eps_revision_001`**（`RRA2eE70`） | **combined** | 分析师修正 + `bf55`/`std0.26`/`pow4.0` + `volume` 门控 6 | **1.64** | 1.31 | 0.093 | 2.10 | 0.6636 | 0.4617 |
| **`pwvndZJ3`** | **atom**（shortinterest） | 做空净买额 + `bf66`/`std0.20`/`pow3.5` + `tvr_decay 0.22` | **2.09** | 1.44 | 0.2213 | 1.93 | 0.6406 | 0.4589 |

> 两者互相相关 **−0.036**（近零），可共存。但**提交后前者进入 prod 池**，
> 使分析师内核的兄弟变体 prod 直接升到 **0.9652** ⇒ 同内核彻底关闭。

### 3.2 单闸最优点（用于校准「还差多少」）

| 场景 | alpha | S | F | TO | 2Y | prod | 说明 |
|---|---|---|---|---|---|---|---|
| 分析师 + 门控，S 最高 | `wp9JM0Ll` | **1.67** | 1.36 | 0.0841 | 2.38 | 0.7003 | prod 差 0.0003 |
| 分析师 ATOM，S 最高 | `YPxNpLmR` | 1.55 | 1.21 | 0.1035 | 1.92 | 未测 | 差 0.03 过闸 |
| 分析师 ATOM + `hump` | `A1QnQXGE` | 1.55 | 1.25 | 0.0806 | 1.92 | **0.9652** | prod 被已提交自己封锁 |
| shortinterest 无门控 | `O0JnAeMg` | 1.91 | 0.81 | 0.5512 | 1.69 | — | 只差 F |
| shortinterest + tvr_decay | **`pwvndZJ3`** | **2.09** | **1.44** | 0.2213 | 1.93 | **0.6406** | 全过 |
| 分析师 prod 最低 | `e76dQQzJ` | 1.58 | 1.24 | 0.0936 | 2.41 | **0.6571** | S 恰在闸线，无余量 |

### 3.3 ATOM / combined 判定实测（`classify_atom`）

| 表达式特征 | verdict | datasets | base_fields |
|---|---|---|---|
| 含 `volume` 门控 | **combined** | `BASE_MARKET` + 目标集 | `['volume']` |
| 无 `volume` 门控（仅目标集字段 + 分组轴） | **atom** | 目标集 | `[]` |
| 仅目标集字段 + `ts_target_tvr_decay` | **atom** | 目标集 | `[]` |

> 关键：`sector` / `industry` / `subindustry` 属 **grouping_keys，不计入 base_fields**，
> ⇒ **分组轴与中性化档可自由调，不破坏 ATOM**。

### 3.4 KOR D1 塔状态（2026-10-18，`get_pyramid_alphas` 实测）

| 塔 | 已提交 RA | 塔 | 已提交 RA |
|---|---|---|---|
| **fundamental** | **3（点亮）** | institutions / macro / news / risk / sentiment | 0 |
| **shortinterest** | **3（点亮）** | insiders / earnings / imbalance / socialmedia | 0 |
| model / pv | 2 | analyst / other | 1 |

**未点亮塔倍数**：news 1.6 ＝ sentiment 1.6 ＝ other 1.6 > macro 1.4 ＝ institutions 1.4 > risk 1.3 > insiders 1.2 > earnings 1.1 > imbalance 1.0。

> ⚠ 与 SKILL.md 硬闸第 3 条的口径差异：SKILL.md 写「已点亮 = **数据集级** ≥3，不要按塔排除」。
> 按塔排除是**用户偏好**（降低优先级），不是平台规则；两者并存时以用户偏好优先，但**数据集级判据仍须单独查** `get_submit_ready`。

---

## 四、优先级建议（下次开工直接照此排）

1. **先查 `get_submit_ready(region="KOR")` 确认数据集级未点亮名单**，再叠用户偏好的塔排序。
2. **目标塔**：institutions（`fund_holdings_panel`，cov 0.8093、30 字段、完全未碰）→ risk（`risk71`）→ macro（`macro63` 事件型）。
3. **进新数据集只做三件事**：① 按 `alphaCount` 降序看 TOP30 定位最强经济轴 ② 按 description 分类 ③ **只测变化类字段**。
4. **首测就用 P-ATOM-1**，参数取 `bf 40 / std 0.24 / pow 3.5 / tvr 0.22`，一条仿真即可判断该数据集有无 \|S\|>1.3 的潜力。
5. **判死门槛**：单字段首测 \|S\| < 1.0 ⇒ 该字段弃；同数据集 3 个变化类字段全部 <1.3 ⇒ 整个数据集弃。

---

*维护约定*：本文数值随新战役追加，**不覆盖历史**；新结论若与本文冲突，在对应行加 `⚠ 已更新见 <日期>` 而非直接删改。
