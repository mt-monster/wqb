# option3（Equity Options Moneyness Aggregates）字段画像与首轮预注册（USA / D1 / TOP3000，2026-10-21）

> 用途：order_flow_imb（aC 478）Wave 1 把单集天花板打到 |S| 1.04 后，按预注册的切换条件启用本集。
> 选它的理由：**期权隐含波动率曲面与分析师族零重叠**——已交付 5 颗全是 analyst 族
> （analyst_factor_signals ×2 / analyst44 ×2 / analyst_consensus ×1），
> 期权面在 **prod 与 self 两条相关性上都是天然正交腿**，这是补足剩下 5 颗缺口最需要的属性，
> 而不是「S 更高的集」。
> 本档按「字段画像 → 机制 → 回测结果及归因」组织，回测完成后回填 §5。**本档不含提交动作。**

---

## 0. 数据集坐标（`get_datasets` / `get_datafields` 2026-10-21 实测）

| 项 | 值 | 备注 |
|---|---|---|
| dataset id | `option3` | "Equity Options Moneyness Aggregates" |
| 塔位 | USA / D1 / **option 塔**（`pyramidMultiplier` 1.3） | 本季 option 塔未点亮 |
| 平台字段数 | **20** | 本次可见 **16**（`sharpe_filter_applied=true`，移除 4） |
| 数据类型 | 全部 **MATRIX** | 无需 `vec_*` 聚合 |
| 覆盖率 | 主体 **0.9298–0.9493**；put 侧 OI / 成交量仅 **0.7257–0.7269** | put 腿必须 backfill，且是 CW 风险源 |
| 数据集 alphaCount | **492**（userCount 289） | 全 USA option 类别里第二冷（order_flow_imb 478） |
| 字段 alphaCount | **5–128**（中位 ~30） | `opt3_volcallatm` 128 已是本集最高 |
| valueScore | 3 / 5 | 与 order_flow_imb 同级 |
| 更新频率 | **日频**（OI / 成交量 / IV 均为每日聚合） | 换手是第一风险，不是覆盖 |

**字段全表（16 个可见）**

| 字段 | 含义 | cov | aC |
|---|---|---:|---:|
| `opt3_openintecallatm` | ATM call 未平仓量 | 0.9439 | 24 |
| `opt3_openintecallitm` | ITM call 未平仓量 | 0.9298 | 15 |
| `opt3_openintecallotm` | OTM call 未平仓量 | 0.9487 | 15 |
| `opt3_openinteputatm` | ATM put 未平仓量 | **0.7257** | 14 |
| `opt3_openinteputotm` | OTM put 未平仓量 | **0.7269** | 5 |
| `opt3_volcallatm` | ATM call 隐含波动率 | 0.9493 | **128** |
| `opt3_volcallitm` | ITM call 隐含波动率 | 0.9493 | 33 |
| `opt3_volcallotma` | OTM call 隐含波动率（ask） | 0.9493 | 88 |
| `opt3_volcallotmb` | OTM call 隐含波动率（bid） | 0.9493 | 63 |
| `opt3_volputatm` | ATM put 隐含波动率 | 0.9493 | 56 |
| `opt3_volputitm` | ITM put 隐含波动率 | 0.9493 | 30 |
| `opt3_volputotma` | OTM put 隐含波动率（ask） | 0.9493 | 85 |
| `opt3_volumecallatm` | ATM call 成交量 | 0.9439 | 31 |
| `opt3_volumecallitm` | ITM call 成交量 | 0.9298 | 22 |
| `opt3_volumecallotm` | OTM call 成交量 | 0.9487 | 17 |
| `opt3_volumeputatm` | ATM put 成交量 | **0.7257** | 12 |

**字段结构自带的三条正交轴**：价格（IV 曲面）、持仓（OI）、流量（volume）。三轴同由 moneyness × side 二维切分，
所以「同一机制可以换轴度量」是本集最大的算子空间，也是防 `add A,B` 混信号的天然替代品。

**缺口（必须记，别当全集）**：可见面里**没有 `opt3_volputotmb`（OTM put bid）**，也没有 `opt3_volumeputotm`。
因此「put 侧买卖价差」「OTM put 成交量占比」两条路本集走不通——要用请转 option40。

---

## 1. 机制地图（先立机制，再谈算子）

| 机制 | 一句话 | 主字段 / 构造 | 符号假设 |
|---|---|---|---|
| **M0 波动率水平（对照，非 alpha）** | 低波股跑赢 = BAB 风格 | `opt3_volcallatm` | 负 |
| **M1 Smirk 偏斜** | 下行保护越贵 → 未来越差 | `volputotma − volcallatm` | **负** |
| **M2 对称偏斜（分布三阶矩）** | put 翼与 call 翼的斜率差 = 风险中性偏度 | `[(volputitm+volcallotma) − (volcallitm+volputotma)]/2` | **负** |
| **M3 彩票偏好** | OTM call 相对 ATM call 的溢价 = 投机需求 | `volcallotma − volcallatm` | **负** |
| **M4 put 翼陡峭度** | 只取下行翼，剥离 call 侧定价 | `volputotma − volputatm` | **负** |
| **M5 ATM put-call 价差** | 同档同期限的方向情绪 | `volcallatm − volputatm` | 待验 |
| **M6 期权市场做市不确定性** | OTM call ask−bid = 报价者不敢定价的程度 | `volcallotma − volcallotmb` | **负**（不确定性溢价反向）｜待验 |
| **M7 持仓结构** | put/call OI 比 = 仓位拥挤方向 | `openinteputotm / openintecallotm` | 待验（反向/顺向都说得通） |

**M0 是控制腿不是候选**：P1–P6 全都含 IV 水平腿，若它们的 S 与 M0 相近，说明这一批测的是
「波动率水平」这个风格而非偏斜——那就不是新机制，是 BAB 的变装，必须换归一化形式重做。

---

## 2. 论坛实证（2026-10-21 读取，两条源帖）

### 2.1 《Individual Option Volatility Smirk》（JY72168，23 赞 / 9 评论）

论文结论：**波动率微笑越陡，风险调整后年化收益低约 10.9%**，可预测性持续 ≥6 个月，陡峭组下一季度盈利冲击最严重。

作者的实操链（字段来自另一套 option 数据，非本集）：

```
skew  = rank(winsorize(ts_backfill(IV_call_10 − IV_put_10, 5), std=4))
alpha = −ts_kurtosis(skew, 120)
group_neutralize(alpha, bucket(rank(volume), range="0,1,0.1"))
```

可复用结论：

1. **`ts_kurtosis` 是 Consultant 专属算子**，user 级报 `unknown operator`（YJ86883 实测）。**不得进候选池。**
2. 替代路径实测（USA/TOP3000）：原始 smirk `S 0.83 / F 0.74 / TO 49.8%` →
   **`ts_decay_linear 120d` 后 `S 0.80 / F 1.39 / TO 1.75%`**。⇒ **换手压下来 F 反而翻倍**，
   这是本区 F 墙（`F/S = 0.365`）最直接的对症药：换手在 12.5% 以下时 F 只由 |returns| 决定。
3. **同桶作差是保测量干净的底线**（JR57542）：两边必须同一到期/档位桶，否则差值混入期限结构噪音。
4. **IV 差值是快变量**，顺序是「先 `ts_decay_linear` / 拉长窗口压日频抖动，再谈凸形变换」。
5. 覆盖率问题会直接变成 weight concentrate；`ts_backfill` 参数调大常把 alpha 表现调坏 ⇒ 短 backfill（5–20）起步。

### 2.2 《Option-Implied Volatility Measures and Stock Return Predictability》（YW27566）

给出六种价差构造，本集可完整映射前五种（第六种 RV−IV 存在年化单位与 IV 报价单位的量纲问题，先不做）：

| 论文编号 | 构造 | option3 映射 |
|---|---|---|
| (1) | `IVatm,call − IVatm,put` | `volcallatm − volputatm` → **P5** |
| (2) | `IVotm,put − IVatm,call` | `volputotma − volcallatm` → **P1** |
| (3) | `[(IVitm,put+IVotm,call) − (IVitm,call+IVotm,put)]/2` | 四个字段齐备 → **P2** |
| (4) | `IVotm,call − IVatm,call` | `volcallotma − volcallatm` → **P3** |
| (5) | `IVotm,put − IVatm,put` | `volputotma − volputatm` → **P4** |

**该帖的负面情报同样重要**：两位跟帖者（YW93864 / YJ86883）明确反馈这套 IV 价差**prod_corr 普遍偏高**，
且「把 volume 中性化换成别的 model data 中性化」才拿到可提交版本。⇒ 本集**必须 prod 前置**：
任何形态 S ≥ 1.2 立即 `check_correlation(refresh=True)`，不等 F/2Y 都调好再测。

---

## 3. 与已交付 5 颗的关系（为什么要开这一集）

| 维度 | 已交付 5 颗 | option3 |
|---|---|---|
| 数据类别 | 全部 analyst（三个数据集） | option（IV 曲面） |
| 收益来源 | 预期修正 / 盈利偏度 / 背离加速度 | 风险中性分布形状 / 期权报价不确定性 |
| self 相关风险 | 同族之间已实测 < 0.7 | 与 analyst 无共同字段，结构性正交 |
| prod 相关风险 | 已靠 RAM/CROWDING 剥离 | **未知，论坛警告偏高** ⇒ prod 前置 |

---

## 4. Wave 1 预注册（9 条 = 1 控制 + 7 机制 + 1 归一化）

设置：USA / TOP3000 / EQUITY / D1 / decay 5 / truncation 0.08 / nanHandling ON / maxTrade OFF /
pasteurization ON / unitHandling VERIFY / neutralization **SUBINDUSTRY** / 2014-01-01 → 2023-12-31
（与 order_flow_imb 同口径，保证两集的读数可比）。

| # | 机制 | 表达式 | 假设 |
|---|---|---|---|
| **C0** | M0 波动率水平（**对照**） | `-group_rank(ts_mean(ts_backfill(opt3_volcallatm, 20), 5), subindustry)` | 负 |
| P1 | M1 Smirk | `-group_rank(ts_mean(ts_backfill(opt3_volputotma - opt3_volcallatm, 20), 5), subindustry)` | 负 |
| P2 | M2 对称偏斜 | `-group_rank(ts_mean(winsorize(ts_backfill((opt3_volputitm + opt3_volcallotma - opt3_volcallitm - opt3_volputotma) / 2, 20), std=4), 5), subindustry)` | 负 | <!-- lint:counterexample: 对称偏斜定义式（四期权量线性组合） -->
| P3 | M3 彩票偏好 | `-group_rank(ts_mean(ts_backfill(opt3_volcallotma - opt3_volcallatm, 20), 5), subindustry)` | 负 |
| P4 | M4 put 翼 | `-group_rank(ts_mean(ts_backfill(opt3_volputotma - opt3_volputatm, 20), 5), subindustry)` | 负 |
| P5 | M5 ATM 方向 | `-group_rank(ts_mean(ts_backfill(opt3_volcallatm - opt3_volputatm, 20), 5), subindustry)` | 待验 |
| P6 | M6 报价不确定性 | `-group_rank(ts_mean(ts_backfill(opt3_volcallotma - opt3_volcallotmb, 20), 5), subindustry)` | 待验 |
| P7 | M7 持仓结构 | `-group_rank(ts_mean(ts_backfill(opt3_openinteputotm, 20) / (0.001 + ts_backfill(opt3_openintecallotm, 20)), 5), subindustry)` | 待验 |
| P8 | M1 归一化 | `-group_rank(ts_mean(ts_backfill((opt3_volputotma - opt3_volcallatm) / (0.001 + opt3_volputatm), 20), 5), subindustry)` | 负 |

**为什么 P8 单列**：IV 价差带着个股 IV 水平（水平越低价差天然越小），
除以自身 ATM put IV 后得到无量纲的「相对偏斜」——这是把 M1 从「波动率水平变装」里择出来的唯一写法。
P1 与 P8 的 ΔS 就是**水平污染量**。

**为什么没有 ATOM 混腿**：C0–P8 每条只用一个数据集，非豁免字段全部来自 `option3`，
分组字段只用 `subindustry`（六个豁免分组字段之一）⇒ **全部满足 ATOM 口径**。
P7 的两条 OI 腿同集同构造，是比率不是混信号。

### 4.1 结构判据（先于指标判定）

1. **水平污染**：若 `|S_P1 − S_C0| < 0.2` 且 `|S_P8 − S_C0| < 0.2`，说明本集在 TOP3000 上只是 BAB 变装 ⇒ 整族不作候选。
2. **换手**：若 TO 全部 > 30%，说明 `ts_mean 5` 不够，Wave 2 直接换 `ts_decay_linear(60/120)`（论坛实证的 F 杠杆），不再试窗口。
3. **覆盖率**：P7 若出现 CW（>10%）或 SUB/|S| < 0.43，先改 `group_backfill` 再判，不要直接判死。
4. **同源对照**：P1 vs P2 vs P4 三条都含 put 腿，若三者的 S 差 < 0.15，说明「取哪一档」不承载信息，只保留一条。

### 4.2 判死线（先写再跑，防止事后找理由）

- 若 C0–P8 的 **max |S| < 1.0** ⇒ 判「本集 TOP3000/SUBINDUSTRY 下无可提交信号」，转 option40（aC 3200、208 字段）。
- 若 **P1 / P8 相对 C0 的增量 < 0.2** ⇒ 判「本集信号 = 波动率水平」，M1–M4 全部作废，只留 M6/M7 两条非方向机制。
- 若某条 **|S| ≥ 1.2** ⇒ **立即** `check_correlation(refresh=True)`；prod ≥ 0.70 即该机制判死，不投入抬 S。
- 若某条 **S ≥ 1.58 但 F < 1.0** ⇒ 按论坛实证只做一件事：`ts_decay_linear(120)` 压换手（1 条 sim），仍不过判死。

## 5. Wave 1 实测（multisim `2mZb7OeLU4w3aoEBDD7g6tg`，9/9 COMPLETE，2026-10-21）

| # | 机制 | α | S | F | TO | ret | 2Y | SUB | rns |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| C0 | M0 波动率水平（对照） | `WjLe1mAo` | **0.02** | 0.00 | 0.0673 | 0.20% | 0.42 | 0.00 | −0.33 |
| P1 | M1 Smirk | `mLY6wkj2` | 0.85 | 0.31 | 0.1961 | 2.57% | 0.81 | 0.15 | 0.79 |
| P2 | M2 对称偏斜 | `xA1bOajn` | **−0.38** | −0.08 | 0.2154 | −1.02% | −1.21 | 0.04 | −0.05 |
| P3 | M3 彩票偏好 | `MP03MA7n` | 0.30 | 0.07 | 0.1795 | 0.94% | 0.81 | 0.27 | 0.23 |
| P4 | M4 put 翼 | `A1Qvjd0Y` | 0.17 | 0.03 | 0.1857 | 0.62% | 0.81 | 0.04 | 0.28 |
| **P5** | **M5 ATM 方向** | `rKdepm58` | **−1.33** | −0.84 | 0.1677 | **−6.66%** | **−2.13** | −0.58 | −0.53 |
| P6 | M6 报价不确定性 | `akVxj3bO` | 0.37 | 0.10 | 0.1773 | 1.18% | 0.87 | 0.37 | 0.43 |
| P7 | M7 持仓结构 | `0mjrOWrq` | −0.35 | −0.12 | 0.0967 | −1.54% | −0.77 | −0.08 | −0.13 |
| P8 | M1 归一化 | `akVxj3xO` | 0.87 | 0.33 | 0.1937 | 2.80% | 0.64 | 0.27 | **0.95** |

**注**：P5 的 S 是负号形态（`-group_rank`）。**取正号即 S +1.33**，Wave 2 #1 已实测确认（`N1eV0ngE`，见 §7）。

### 5.1 读数（对照 §4.1 结构判据逐条）

1. **水平污染 = 无**。C0 = 0.02 / F = 0 / rns −0.33 —— 纯粹的 ATM call IV 水平在 USA/TOP3000/SUBINDUSTRY
   下**没有任何可提取的方向**（2.0% 年化、0.0673 换手）。这是本集最关键的一次对照：后续所有价差读数
   **不是波动率水平变装**，不必再怀疑。
2. **P1 / P8 的增量**：|S_P1 − S_C0| = 0.83、|S_P8 − S_C0| = 0.85，**双双越过 0.2 门槛** ⇒ M1 有真内容。
   但归一化只抬了 0.02（0.85 → 0.87），说明「除以自身 ATM put IV」几乎不改变排序 ——
   分子（翼部−ATM 价差）本身已经弱相关于水平，**P8 相对 P1 的 0.02 就是水平残余量**。
3. **换手**：无一条 > 30%（最高 0.2154），故 §4.1 第 2 条不触发，**不需要**靠 `ts_decay_linear` 救。
   反过来看，TO 落在 0.10–0.22 —— 恰好是 F 分母难过的地方（见 §7.2 算术）。
4. **同源对照**：P1 / P2 / P4 的 S 分别为 0.85 / −0.38 / 0.17，**极差 1.23 ≫ 0.15** ⇒
   「取哪一档」**承载全部信息**。进一步：P4（put 翼 − put ATM）= 0.17 而 P1（put 翼 − call ATM）= 0.85
   ⇒ **信息在「翼部相对 call ATM」这个跨式对比里，不在 put 侧自身的期限/执行价结构里**。
   这条直接指向 P5（纯 ATM 的 call − put），也解释了为什么它最强。
5. **P2 是负的（−0.38）**：对称偏斜（call 翼 − put 翼 / 2）与 P1/P8 反号 ⇒ 两侧翼的偏斜互相抵消后
   剩下的是噪声。M2 作废。
6. **rns 的两个极端**：P8 = 0.95、P1 = 0.79（**风格剥离后仍在**），而 P5 = −0.53（**只有 40% 留存**）
   —— P5 的强读数里有一大半是风格暴露。这个先兆在 prod 实测里被证实（§7.1）。

### 5.2 与预注册假设的偏差

预注册把 P1/P2/P4/P8 都写成「负」，实测只有 P2 为负；P1/P4/P8 在 `-group_rank` 形态下为正
⇒ **等价于「正向 rank」为负**。即：翼部 IV 相对 ATM 越高 / put-call 偏斜越陡的股票，**未来跌**。
这与「偏斜陡 = 尾部风险定价 = 事后负收益」的文献方向一致（Xing-Zhang-Zhao 2010 的个股期权偏斜预测），
属于**方向被预注册写反、机制本身被证实**，不是噪音拟合。P5 也是同一方向（call−put 越大越跌）。

---

## §6 Wave 2 升级协议（**先写死，Wave 1 出结果后照表执行，不许临场改判**）

Wave 1 是**机制探针**（medium 平滑、SUBINDUSTRY、decay 5），目标是回答「哪条机制有信号」，不是交付。
任何一条进入升级的前提是 **|S| ≥ 1.2**；未达者按 §4.2 判死线处理，不升级。

| 触发器 | 唯一允许的动作 | 条数 | 判据 |
|---|---|---:|---|
| 某机制 S ≥ 1.2 但 **F < 1.0** | 该机制 × `ts_decay_linear(60 / 120)`（外层，包住整个 rank 前信号） | ≤2 | 若 |returns| 跌破 5% ⇒ 停，说明该机制收益太薄，不是噪声问题（§7.2 算术） |
| 某机制 **TO > 30%** | `ts_decay_linear(120)` **或** `ts_mean(·, 66)`，二选一不叠加 | 1 | 只压换手不动信号时 S 跌幅 > 0.25 ⇒ 信号是短周期，判死 |
| 某机制 **SUB/\|S\| < 0.43** | 先 `group_backfill(..., subindustry, 66)` 补覆盖；仍不足再换 `industry` | ≤2 | 覆盖率是原因（put 侧 0.73）才值得补 |
| 某机制 **S ≥ 1.2 且 F ≥ 1.0** | **立即 `check_correlation(refresh=True)`** | 1 | prod ≥ 0.70 ⇒ 该机制判死，不抬 S |
| 某机制 **prod < 0.70 且 S ≥ 1.2** | 才允许换中性化（RAM / CROWDING）做最后一跳 | ≤3 | 换完 S 掉超 0.2 或 prod 反升 ⇒ 停 |

**明确禁止**（本区已付学费的路径）：
- **不许**在 option3 上做 `add(A, B)` 混腿或任何权重调参；
- **不许**用 `ts_kurtosis`（Consultant 专属，user 级 unknown operator）；
- **不许**用 `bucket(rank(volume), ...)` 做分组中性化——`volume` 非 ATOM 豁免字段，且换手会爆；
- **不许**在没有 prod 读数的情况下把某条从 1.2 磨到 1.58（PC 只向上漂，磨完可能白做）。

**若 Wave 1 的 max |S| < 1.0** ⇒ 按 §4.2 判死，整个 option3 封存，转 **option40**（208 字段 / aC 3200），
切换理由只需一句：本集 16 个可见字段的信号上限已实测不足，而 option40 多出 192 个字段、且含期限结构维度。

## 7. Wave 2 实测与 M5 判死（multisim `1nh2Qf7s54DN8UT3kfjSvhh`，5/5 COMPLETE）

Wave 2 只针对 P5 的正号形态（`group_rank(ts_mean(ts_backfill(opt3_volcallatm - opt3_volputatm, 20), W), subindustry)`）。

| # | 形态 | α | S | F | TO | ret | 2Y | SUB | rns |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `W=5`（**确认镜像**） | `N1eV0ngE` | 1.33 | 0.84 | 0.1677 | 6.66% | 2.13 | **0.58** | 0.53 |
| 2 | `W=22` | `mLY6pqq2` | 1.33 | **0.97** | **0.0749** | 6.71% | **2.23** | **0.50 ❌** | 0.55 |
| 3 | `W=5` + `ts_decay_linear(60)` | `3qjVwEEX` | 0.75 | 0.32 | 0.0406 | 2.21% | **0.24** | 0.06 | 0.23 |
| 4 | `W=5` + `ts_decay_linear(120)` | `GrgOPnkP` | 0.69 | 0.28 | 0.0305 | 2.09% | **0.34** | 0.21 | 0.06 |
| 5 | `W=5` + 除以 `0.001+putatm` | `1YjZeoJz` | 1.27 | 0.79 | 0.1662 | 6.35% | 2.13 | 0.56 | 0.54 |

### 7.1 `decay_linear` 这条路在本机制上**反着走**（与论坛示例相反）

`ts_decay_linear(60)` 把 S 从 1.33 打到 0.75、2Y 从 2.13 打到 **0.24**，`120` 同样（0.69 / 0.34）。
收益同步从 6.66% 掉到 2.2% —— **不是噪声被平滑掉，是信号本身被抹掉**。
对照 order_flow_imb §7.1 的同一结论（平滑杀短周期信号），这是本战役**第二次**得到「平滑不是通用 F 杠杆」。

> 机理：`ts_mean(·, 5)` 之后再做线性衰减，等于把已聚合的 5 日信号又按 60/120 天加权平均，
> 信号自相关结构被彻底改变；本机制的预测窗口就是 1–4 周（`W=22` 时 S 不降），**再长就出了有效区**。

### 7.2 换手地板 0.125 是真的，且 `W=22` 已经踩进去了

平台口径 `F = S × sqrt(|ret| / max(TO, 0.125))`。用本批两条同日对照验算：

- `W=5`：`1.33 × sqrt(0.0666/0.1677) = 0.838` ≈ 实测 0.84 ✓（TO > 0.125，用真实值）
- `W=22`：`1.33 × sqrt(0.0671/0.125) = 0.975` ≈ 实测 0.97 ✓（TO 0.0749 < 0.125，**被地板托住**）
- 若误用真实 TO：`1.33 × sqrt(0.0671/0.0749) = 1.259` ✗ —— 与实测差 0.29，证明地板确实生效。

推论两条，写进选集纪律：
1. **TO 压到 12.5% 以下不再给 F 任何奖励**，`W=22` 在此已是浪费（多出来的平滑只换来 SUB 从 0.58 掉到 0.50）；
2. **在 S=1.33 时 F=1.0 需要 ret ≥ 0.125/1.33² = 7.07%**，本机制只有 6.7% ⇒ 差 5.4%。
   而 S 若要上 1.58，则只需 ret ≥ 5.01% —— 即**卡点在 S，不在 F**。

### 7.3 M5 的 prod 实测：0.8567，`[0.7,0.8)` 桶 n=273 ⇒ 结构性判死

对 `N1eV0ngE` 跑 `check_correlation(refresh=True)`：

| 项 | 值 |
|---|---|
| prod max_correlation | **0.8567**（线 0.70） |
| 直方图 `[0.7,0.8)` 桶 | **n = 273**（D0-P 判据：n ≥ 1 即不可救） |
| 直方图 `[0.8,0.9)` 桶 | n = 172 |
| 负侧最深 | −0.6469 |

**D0-P 判定：dead_end**。理由不是「这次 0.8567 太高」，而是 `[0.7,0.8)` **有 273 个邻居** ——
PC 只向上漂，微调窗口/算子只会在 273 个同族里换一个，不可能穿越到 0.70 以下。
§6 协议里「prod < 0.70 才允许换中性化」的前置因此**不成立**，M5 不再抬 S。

与 §5.1 第 6 条的先兆一致：`rns = 0.53`（留存 40%）早就说明这条价差有大半是风格暴露，
而风格暴露正是 prod 高相关的来源。**Cremers-Weinbaum 的 call−put IV 价差在平台 prod 书里已被充分交易**。

### 7.4 本集裁定

- **M5（唯一 |S| ≥ 1.2 的机制）：dead_end**（prod 0.8567 / n=273）。
- **其余机制上限 0.87**（P8，rns 0.95；P1 0.85，rns 0.79），距 S 1.58 差 0.71，
  且在 S 1.33 处已证实会撞 prod 墙 ⇒ **不值得为 0.87 的两条花仿真**。
- **C0 = 0.02** 已排除「本集只是波动率水平」的可能，故上述判死**不是**「数据集没信号」，
  而是「**有信号但全在 prod 书里**」—— 这两者对后续选集的启示完全不同：
  option 类数据集整体面临 prod 墙，不是字段质量问题。

⇒ 按 §4.2 与 §6 的切换条款，**option3 封存**。切换目标**不是** option40（见 §8.3）。

## 8. 中性化杠杆实测（6 条 2×3 因子，`batch_create_simulations`）

设置：USA/TOP3000/D1、decay 5、trunc 0.08、分组固定 `subindustry`，只换 `neutralization` × `W`。
表达式同 §4 P5 镜像：`group_rank(ts_mean(ts_backfill(opt3_volcallatm - opt3_volputatm, 20), W), subindustry)`。

| W | neutralization | α | S | F | TO | ret | 2Y | SUB | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 5 | STATISTICAL（Wave 2 基线 `N1eV0ngE`） | — | 1.33 | 0.84 | 0.1677 | 6.66% | 2.13 | 0.58 | prod 0.8567（n=273）⇒ dead |
| 5 | CROWDING | `3qjVbMEg` | 1.22 | 0.80 | 0.1624 | 6.93% | 1.64 | **0.68** | S −0.11，未测 prod |
| 5 | REVERSION_AND_MOMENTUM | `88vPbMk7` | 1.11 | 0.61 | 0.1946 | 5.89% | 1.47 | 0.50 | 三闸不过 |
| 22 | STATISTICAL | `gJWZAqJM` | 1.23 | 0.71 | 0.1008 | 4.16% | 1.99 | 0.46 ❌ | SUB 破 |
| 22 | CROWDING | `JjPQqAKm` | 1.27 | **0.96** | 0.0734 | **7.10%** | **1.78** | **0.70** | prod **0.7915**（n=218）⇒ dead |
| 22 | REVERSION_AND_MOMENTUM | `qME01zKj` | 1.18 | 0.83 | 0.1076 | 6.21% | 1.60 | 0.48 ❌ | SUB 破 |

### 8.1 三读

1. **CROWDING 是唯一有效的中性化**（同 W=22 对比 STATISTICAL）：S 1.23→1.27、ret 4.16→7.10%、
   SUB 0.46→0.70，2Y 1.99→1.78；prod 0.8567（`[0.7,0.8)` n=273）→ **0.7915（n=218）**。
   方向对，但**两个桶都很厚**。
2. **RAM 与 STATISTICAL 都伤 S**：RAM 在 W=5/22 分别 1.11/1.18、SUB 0.50/0.48 双破；
   STATISTICAL W=22 SUB 0.46 破。⇒ 本集的 SUB 只有 **CROWDING** 抬得动（0.58→0.68/0.70），
   这也是唯一同时抬 ret 与 SUB 的旋钮。
3. **中性化不是 prod 墙的解**：CROWDING 把 prod 压了 0.065、桶数减 55，但 `[0.7,0.8)` n=218 仍 ≫ 1
   ⇒ 族级饱和，按 D0-P 判死。**prod 墙的成因是机制饱和，不是风格暴露**——
   与 `JjPQqAKm` 的 rns 读数（≈0.55，非纯 beta）一致。

### 8.2 本集最终裁定（第二独立确认）

- 两次独立战役给出同一上限：旧 4 批 32 条最好 `KPmEXpAj` S **1.34**；本次 16 条最好
  `N1eV0ngE` S **1.33**。⇒ **单数据集 option3 的 S 天花板 ≈ 1.33–1.34，与 §4.2 预注册的
  「判死线 1.0 / 切换线」无关，是硬上限。**
- 唯一够格机制 M5 在 S 1.33 处 prod 0.8567 ⇒ **dead_end**；能压 prod 的 CROWDING 版 S 只 1.27
  且仍在 0.8 桶 ⇒ **两条腿都断**。
- ⇒ **option3 封存（第二确认）**，不再发批。本集最强三条登记为 SUPER 组合腿候选：
  `N1eV0ngE`（S 最高）/ `JjPQqAKm`（ret 7.10%、SUB 0.70）/ `akVxj3xO` P8（rns 0.95）。
  组合层另测 prod。

### 8.3 为什么不转 option40

option40 是 **IV 曲面 / 希腊字母**（208 字段，无成交量/OI）。本次归因的结论是
「**机制饱和在 prod 书里，不在字段数量上**」——option40 与 option3 共享同一个底层
（隐含波动率），prod 池对 vol 类机制已厚到 `[0.7,0.8)` n=273。加 192 个同底层字段
只会把同一机制测得更细，不会长出**新机制**。按「说不出与 prod 书不同的收益来源不许组装」，
option40 **不投**；期权塔整体按已饱和处理（本季 `USA/D1/OPTION` 塔位 multiplier 1.3 已亮）。
