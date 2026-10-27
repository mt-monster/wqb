# ASI 挖掘进展与判死结论（2026-10-22）

## 一、ASI 塔位现状（平台权威，`get_pyramid_alphas`）

| 塔 | alphaCount |
|---|---:|
| **Other** | **2 / 3** |
| 其余 15 塔（PV / News / Model / Analyst / Sentiment / Insiders / Fundamental / Risk / Social Media / Broker / Imbalance / Earnings / Macro / Institutions / Short Interest） | **全 0** |

已提交 9 颗 ACTIVE：`E5ReEnpP`(1.93) `j28nKkQo`(2.18) `E5R56EbR`(2.96) `1YZYj5QQ`(2.59)
`P02wbJAM`(2.30) `88jaV5lv`(2.35) `LLNgdpw2`(1.98) `rKjY5vGj`(2.01) `qMNMbeGj`(1.72)

> 塔位按自然季度清零；9 颗中仅 Q4 提交的 2 颗计入，其余 Q3 的已失效 ⇒ 本季度实质从 2/3 起步。

---

## 二、本轮测试的三条线：全部判死

### 2.1 `other455` 图聚类（1500 字段，321 GROUP + 79 MATRIX，大量 aCnt=0）
10 条探针（含 `group_rank` / `group_neutralize` 用图聚类键当轴）：

| 结构 | S |
|---|---:|
| 无轴对照（最优） | **0.33** |
| `group_neutralize(K20)` | 0.32 |
| `group_rank(K20)` | 0.28 |
| 其余 7 条 | −0.24 ~ −0.13 |

**判死。** 机理：`pca_fact*_value` 是**图嵌入坐标**（结构性），设计用途是当分组轴而非独立信号体；
ATOM 约束下无法「别集当信号 + other455 当轴」。

### 2.2 `mmp_nlp_sentiment` 情绪/目标价价差（521 字段，cov 1.0、aCnt 1~2）
10 条探针：

| 结构 | S | 2Y |
|---|---:|---:|
| 情绪价差（pos vs neg）W22（最优） | **0.73** | 0.14 |
| 目标价价差 W5 / W22 / W66 | 0.59 / 0.58 / 0.40 | −0.29 / −0.22 / −0.55 |
| 单场对照 | −0.64 / −0.65 | 0.09 / 0.15 |

**判死。** 价差构造确实优于单场（+1.4 量级差异），但绝对值不足，且 2Y 系统性为负。

### 2.3 `dl_riskfree_returns`（OTHER 塔首两颗粒的来源）
- **23 条 ATOM 历史存量**（S≥2.0，S 最高 3.58 / 2Y 4.44）prod 全部 0.78~0.87 ⇒ DEAD
- 同批表达式换 universe 后 robust 转 PASS，但 **prod 同步恶化到 0.76~0.93** ⇒ DEAD

**判死**（详见第三节）。

---

## 三、核心发现：universe 档位在 `robust` 与 `prod` 之间是跷跷板

| alpha | universe | S | robust 比例（需 ≥0.90） | prod（需 <0.70） |
|---|---|---:|---:|---:|
| `npdZX3Zx` | MINVOL1M | 3.58 | **0.824** ✗ | 0.8285 ✗ |
| `Vkad52Ab` | MINVOL1M | 3.07 | **0.870** ✗ | 0.7917 ✗ |
| `bl86Al0Z` | MINVOL10M | 3.16 | **0.918** ✓ | **0.8619** ✗ |
| `1YjN0YR6` | MINVOL10M | 2.39 | **0.950** ✓ | **0.9284** ✗ |
| `78oLl8r5` | MINVOL10M | 2.22 | **0.959** ✓ | 0.7625 ✗ |

**MINVOL1M：robust 挂、prod 略好；MINVOL10M：robust 过、prod 更差。两侧都过不了 ⇒ 该族在 ASI 不可交付。**

---

## 四、本轮唯一「全闸仅差 prod」的候选（记录备查）

```
bl86Al0Z = subtract(group_rank(subtract(probability_label4_5quantile_20day_ohlcv,
                                        probability_label0_5quantile_20day_ohlcv), country), 0.5)
ASI / MINVOL10M / D1 / decay 5 / SECTOR / trunc 0.08
```
| 指标 | 值 | 限 |
|---|---:|---|
| Sharpe | 3.16 | 1.58 |
| Fitness | 2.95 | 1.00 |
| 2Y | 3.35 | 1.58 |
| sub-universe | 2.52 | 0.86 |
| robust | 2.90 | 2.84（比例 0.918） |
| self | **0.3195** | 0.7 |
| **prod** | **0.8619** ✗ | 0.70（n[0.7,0.8)=**49**，极拥挤） |

**语义**：桶 4（看涨）概率 − 桶 0（看跌）概率 = **净置信度方向**，按 country 归一。
结构本身（probability 族两端做差的合规价差 + country 轴）值得迁移到其它字段族。

---

## 五、结论与下一步建议

1. **OTHER 塔（2/3）在现有三条数据线上无解** ⇒ 应转攻**另一个空塔**。
2. 首选 **`intraday_pv_feats` → PV 塔**：ASI 历史 396 条记录 / maxS 3.11 / avgTO 0.277，是本区最富矿。
   但已有 9 颗 ACTIVE 多颗出自该集 ⇒ 新 alpha 必须换机制（preclose 反转之外的日内结构）。
3. ⚠ 该集 avgTO 0.277 偏高，需同时守 TO 闸（≤0.7）与 F 闸（TO 进 F 分母）。
4. 资源现状：**REGULAR 配额今日剩 1 颗**；**平台日仿真余量 ~388 条**。

---

*数据来源：`get_pyramid_alphas`、`get_user_alphas`、`get_alpha_details`、`check_self_correlation`、`prod_bucket_scan`；*
*批次：wave601 `35knncgmq4V6amf9mCXyj4E`、wave602 `zD7qP3vI59RcvhvQ4X7k48`、wave603 `mGuT74dI5ctbJPp4lsMsCa`。*
