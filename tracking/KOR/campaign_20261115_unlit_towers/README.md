# KOR × 未点亮塔 × 10 颗全闸 REGULAR alpha（2026-11-15 起）

> **目标（用户 2026-11-15 指令）**：KOR 区固定不换，交付 **10 个通过验证的 regular alpha**，优先 ATOM；
> 逐 category 检查数据集、排除已点亮塔；全字段探测；画像归档；论坛+论文双通道取证；
> 并发 `create_multi_simulation` 上限 2；禁 PV/MODEL/OTHER 两两组腿；跨类组腿 ≤5。
>
> **本次结论**：Institutions 类别经两轮实测判为**结构性不可达**（见 §1），按用户批准的
> 「确实无计可施时换集并说明原因」切到 **INSIDERS（insiders5，1/3 未点亮）** +
> **PV / OTHER 两个未点亮塔的旁证腿**。

## 1. 为什么离开 Institutions（判决留档，非印象）

| 证据 | 读数 | 来源 |
|---|---|---|
| 类别内数据集数 | **2 个**（`institutions6` 11 字段 / `fund_holdings_panel` 30 字段），无第三个可换 | 平台 `get_datasets(KOR, institutions, D1, TOP600)` |
| 全字段探测 | **11/11 + 30/30**（`filter_sharpe=false`） | 平台 `get_datafields` |
| 本地库最强件 | `institutions6` max **S=0.60**；`panel` max **S=0.56** | `data/wqb.db` 只读扫描 8+10 条 |
| 上一轮战役（2026-11-07） | **110 次模拟**、2 数据集、41 字段、6 类结构族、4 中性化档 ⇒ 最强 `MPYee1r6` **S=0.97** | `campaign_20261107_institutions_atom/final_report.md` |
| 唯一 S≥1.58 的构型 | `ts_regression` 残差动量（S 2.05）但 **TO 80.03%**（限 0.7）+ **2Y −0.56**（限 1.58）⇒ 4 闸 FAIL | `qML5kxVv` 平台 checks 实读 |
| KOR 全闸线 | S≥1.58 · F≥1.0 · TO∈[1%,70%] · **IS_LADDER(2Y)≥1.58** · 其余 RA 全 PASS | `qML5kxVv` 的 `checks.fail[].limit` |

⇒ Institutions 的全部信号族（净广度 / 净额 / 份额差分 / 户均 / 均价价差 / 换手 / 行业中性化 /
门控 / 分位窗 / 凸化 / 平滑）两轮扫完，**距 S 闸差 0.61、回归构型被 2Y 与 TO 双杀**。
**类别内无第三个数据集**，故按「确实无计可施」换集。

## 2. 换到哪里（按「未点亮塔 × 现成证据」排序，不看印象）

判据：① 金字塔未点亮（平台 `get_pyramid_alphas` 实读）；② 本地存在 **failed_ra_count=0** 的现成件；③ 信息源不在 OS 池里（决定 prod）。

| 塔 | 点亮态 | 选中理由 | 本轮角色 |
|---|---|---|---|
| **insiders** | **1/3** | `insiders5` 有 **53 字段全字段画像**（`reference/datasets/insiders5.md`）；本地 103 条回测、**56 条过 S/2Y/TO 三闸**、其中 **15 条平台 failed_ra=0**；且 OS 池只用过 1 条 insd5 ⇒ 仍有 prod 白空间 | 主攻（ATOM） |
| **pv** | **2/3** | 距点亮只差 1 颗；`ZYQ116ln`（`corr_bid_price_with_bid_size`）S 1.86 / 2Y 1.80 / **prod 0.698** | 补 1 颗（ATOM） |
| **other** | 1/3 | `oth475`（出口额）/`oth496`（涨跌停状态）/`oth695`（进口额）各有全闸件 | 旁证 + 新机制 |

排除：news（wave 211 五轴全死）、sentiment（wave 189/192/216 三连死）、macro（无截面）、
socialmedia（仅连接键）、risk（2026-11-15 实读已 3/3 点亮）、earnings（S 天花板 0.95）、
institutions（本轮判决）、analyst / fundamental / model / shortinterest（均已点亮）。

## 3. 交付口径（三档，不混写）

| 档 | 判据 | 用途 |
|---|---|---|
| **A. 全闸 + prod 干净** | `failed_ra_count=0` **且** prod<0.7 **且** self<0.7 | 可直接提交（提交权仍归用户） |
| **B. 全闸、prod 撞墙** | `failed_ra_count=0`，prod≥0.7 | 作组合腿 / 待 prod 漂移；**不得提交** |
| **C. 近闸** | 1 项 RA 未过且缺口 <10% | 记入修配清单 |

## 4. 文件索引

| 文件 | 内容 |
|---|---|
| [s0_dataset_scan.md](s0_dataset_scan.md) | S0 全类别数据集扫描 + Institutions 判决 + 选定理由 |
| [waves.md](waves.md) | 波次台账：设计 / 读数 / 归因 / 继承-准入-收窄 |
| [final_report.md](final_report.md) | 交付：10 颗明细（数据集 / 字段 / 算子逻辑 / 指标 / 相关性）|
| `tracking/KOR/reference/datasets/<ds>.md` | **字段画像归档**（命名规则见 §5）|

## 5. 字段画像归档路径与命名规则

- 路径：`tracking/KOR/reference/datasets/<dataset_id>.md`（**每数据集一份，手工维护，文件名 = 平台 dataset id**）。
- 必备区块：① 数据集体征（type / coverage / aC / 更新频率）② **按 description 分类**的字段族表
  ③ 覆盖率分级与预处理决策 ④ 十年覆盖实测 ⑤ 已判死机制清单 ⑥ 本区实测记录（alpha id + 读数）。
- 本轮更新：`insiders5.md`（新增库存股/去重缺口两族的实测）、`institutions6.md`（补天花板判决）、
  `fund_holdings_panel.md`（补天花板 + 2014 空年）。
- ⚠ 扫全字段时**必须显式 `filter_sharpe=false`**，否则成对字段的对侧腿被隐藏（本区 `institutions6` 实测 4/11 vs 11/11）。

## 6. 结算（2026-11-15 收波）

| 项 | 结果 |
|---|---|
| 交付 | **10 颗全闸 REGULAR alpha**（`failed_ra_count=0`，fail 与 warning 全空） |
| 强度 | S **1.61 – 2.82**，全部 ≥ KOR 闸线 1.58；2Y **1.80 – 3.11**，全部 ≥ 1.58 |
| 塔 | 全部未点亮：INSIDERS 1/3、PV 2/3、OTHER 1/3 |
| ATOM | **8/10**（2 颗为价差型双数据集） |
| A 档（prod<0.7，可提交） | **2 颗**：`78LpqZYQ` 0.697、`ZYQ116ln` 0.698 |
| B 档（全闸但 prod 撞墙） | 5 颗实测 0.828–0.953 |
| 待测 prod | 3 颗（`Xgalomw8`/`pwazNYQo`/`vRAzNwab`，平台相关性服务账号级熔断） |
| 新模拟 | **30 条**（W1 10 + W2 10 + W3 10），其中 3 条成为交付件 |
| 收割 | 36 条平台核验，7 条成为交付件 |
| 判死 | insiders5 的库藏股 / 去重缺口 / 持有人结构 / 所有权变化 四族（20 条臂） |
| 报告 | [final_report.md](final_report.md) |

**一句话**：Institutions 判死（110+ 次模拟天花板 S 0.97）后切到 INSIDERS/PV/OTHER 三个未点亮塔，
用「收割 + 价差型组合」拿到 10 颗全闸件；**KOR 的真墙是 prod（平台全局池）而不是 RA**，
目前 2 颗可提交、3 颗待测、5 颗撞墙。

## 7. 验收线收紧后（2026-11-16 用户指令：prod>0.7 不算合格交付）

用户把验收线改为 **全闸 + prod<0.7（严格不等式）**。据此重挖，已确认 **5 颗合格**：

| alpha | 机制 | S | 2Y | prod |
|---|---|---:|---:|---:|
| `wpoJRxW5` | label 概率差 − 内部人分歧度（SLOW·d2） | 2.04 | 2.55 | **0.504** |
| `KPgwLqX8` | 关系方家数 − 内部人分歧度（SLOW·d1） | 1.73 | 2.27 | **0.663** |
| `qM7mArVj` | 同上（SLOW·d2） | 1.74 | 2.26 | **0.665** |
| `78LpqZYQ` | 分析师 FY1 惊奇 − 内部人分歧度（REV&MOM·d4） | 2.12 | 2.59 | **0.697** |
| `ZYQ116ln` | 日内买价×买量相关反向（SLOW·d2） | 1.86 | 1.80 | **0.698** |

**本轮新增的两条方法论**（已写入 `docs/experience/01_platform_gates.md` 与记忆）：
1. **prod 的两级杠杆**：① 换信息源（价差结构，0.84→0.50–0.70）；② **中性化 SLOW + decay 1–2**（同表达式 0.839→0.663）。
2. **证伪清单**：hump+长 decay 壳层、换 anl10 字段、insd5 四个子族 —— 三条都不产出合格件。

## 8. 终态（2026-11-16 收口）

用户把验收线定为 **prod<0.7** 后，又跑 4 波（W5 SLOW/d1、W6 anl10+SLOW/d2、W7 价差变体、W8 tnc 窗口全扫），
最终交付 **10 颗全闸 + prod<0.7** 的 REGULAR alpha（prod 0.504–0.698）。

**核心方法论**（详见 final_report §3）：
1. **价差结构**（两条不同信息源秩相减）是唯一稳定把 prod 从 0.84 压到 0.50–0.70 的一级杠杆；
2. **中性化换 SLOW + decay 降到 1–2** 是二级杠杆（同表达式再压 0.15–0.18）；
3. 被证伪：`hump`+长 decay 壳层、换 anl10 其它字段、insders5 四个未挖子族。

**可复用模板**（10/10 全闸）：
`subtract(group_rank(ts_mean(vec_avg(insd5_tnc), W1), sector), group_rank(ts_mean(vec_stddev(insd5_vol_af), W2), sector))` @ SLOW / decay 2。
