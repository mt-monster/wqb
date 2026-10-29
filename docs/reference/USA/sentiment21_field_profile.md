# USA · `sentiment21` 字段画像

> 由 `tools/fields/profile_dataset_fields.py` 生成，输入为 `get_datafields` 原始返回。零平台配额。

## 1 规模与完整性

| 项 | 值 |
|---|---|
| 本次返回字段数 | 258 |
| 平台声明数 `platform_count` | 258 |
| 返回 `count` | 258 |
| 是否完整 `complete` | True |
| 类型分布 | {'MATRIX': 258} |
| 平均 coverage | 0.9994 |
| 判定 | ✅ 完整 |

## 2 可用性分档

### 2.1 coverage

| 档 | 字段数 |
|---|---|
| ≥0.90（可直接做尽） | 258 |

### 2.2 拥挤度（决定 prod 相关性风险）

| 档 | 字段数 |
|---|---|
| 低拥挤（≤50 alpha） | 253 |
| 中拥挤（51–500） | 5 |

零竞争字段（`userCount==0`）：**0** / 258；描述带单位标注：0

## 3 语义结构

| 语义族 | 字段数 | 示例字段 |
|---|---|---|
| 未归类 | 236 | `snt21_2dts_gen_165`, `snt21_2dts_sop_168`, `snt21_2dts_tuen_149`, `snt21_2neg_conf_low` |
| 规模/水平 | 22 | `snt21_4neg_conf_low`, `snt21_4neg_conf_up`, `snt21_4neg_max`, `snt21_4neg_mean` |

**时间朝向**（`forecast`=前瞻/预测，`realized`=已实现/事后，`mixed`=差值构造）：

| 朝向 | 字段数 |
|---|---|
| unknown | 198 |
| forecast | 60 |

## 4 名字前缀聚类（前 15）

| 前缀 | 字段数 |
|---|---|
| `snt21_2neg` | 13 |
| `snt21_2neut` | 13 |
| `snt21_2pos` | 13 |
| `snt21_3neg` | 13 |
| `snt21_3neut` | 13 |
| `snt21_3pos` | 13 |
| `snt21_4neg` | 13 |
| `snt21_4neut` | 13 |
| `snt21_4pos` | 13 |
| `snt21_5neg` | 13 |
| `snt21_5neut` | 13 |
| `snt21_5pos` | 13 |
| `snt21_6neg` | 7 |
| `snt21_6neut` | 7 |
| `snt21_6pos` | 7 |

## 5 候选短名单（Top 20，按打分排序）

打分 = 覆盖 40 + 低拥挤 25 + 语义可解释 20 + 前瞻 5（非信号 −30）。**只做排序参考**，仍须过单位闸与机制假设。

| # | 字段 | 类型 | cov | user | alpha | 语义族 | 朝向 | 分 | 描述（截断） |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `snt21_4neg_conf_low` | MATRIX | 1.000 | 3 | 3 | 规模/水平 | - | 80.0 | Lower bound of the approximate 95% confidence interval for the daily mean negative sentim… |
| 2 | `snt21_4neg_conf_up` | MATRIX | 1.000 | 4 | 4 | 规模/水平 | - | 80.0 | Upper bound of the approximate 95% confidence interval for the daily mean negative sentim… |
| 3 | `snt21_4neg_max` | MATRIX | 1.000 | 4 | 4 | 规模/水平 | - | 80.0 | Daily maximum of negative sentiment scores from TRNA equity-linked news linked to the sto… |
| 4 | `snt21_4neg_mean` | MATRIX | 1.000 | 4 | 4 | 规模/水平 | - | 80.0 | Daily mean negative sentiment score from TRNA equity-linked news linked to the stock, com… |
| 5 | `snt21_4neg_median` | MATRIX | 1.000 | 9 | 9 | 规模/水平 | - | 80.0 | Daily median negative sentiment score from TRNA equity-linked news linked to the stock in… |
| 6 | `snt21_4neg_min` | MATRIX | 1.000 | 3 | 3 | 规模/水平 | - | 80.0 | Daily minimum of negative sentiment scores from TRNA equity-linked news linked to the sto… |
| 7 | `snt21_4neg_std` | MATRIX | 1.000 | 8 | 8 | 规模/水平 | - | 80.0 | Daily standard deviation of negative sentiment scores from TRNA equity-linked news linked… |
| 8 | `snt21_4neut_conf_low` | MATRIX | 1.000 | 12 | 15 | 规模/水平 | - | 80.0 | Daily lower bound of the approximate 95% confidence interval for the mean neutral sentime… |
| 9 | `snt21_4neut_conf_up` | MATRIX | 1.000 | 4 | 4 | 规模/水平 | - | 80.0 | Daily upper bound of the approximate 95% confidence interval for the mean neutral sentime… |
| 10 | `snt21_4neut_max` | MATRIX | 1.000 | 10 | 13 | 规模/水平 | - | 80.0 | Daily maximum of neutral sentiment scores from TRNA equity-linked news linked to the stoc… |
| 11 | `snt21_4neut_mean` | MATRIX | 1.000 | 12 | 13 | 规模/水平 | - | 80.0 | Daily mean neutral sentiment score from TRNA equity-linked news linked to the stock, comp… |
| 12 | `snt21_4neut_median` | MATRIX | 1.000 | 8 | 11 | 规模/水平 | - | 80.0 | Daily median neutral sentiment score from TRNA equity-linked news linked to the stock in … |
| 13 | `snt21_4neut_min` | MATRIX | 1.000 | 11 | 15 | 规模/水平 | - | 80.0 | Daily minimum of neutral sentiment scores from TRNA equity-linked news linked to the stoc… |
| 14 | `snt21_4neut_std` | MATRIX | 1.000 | 3 | 4 | 规模/水平 | - | 80.0 | Daily standard deviation of neutral sentiment scores from TRNA equity-linked news linked … |
| 15 | `snt21_4pos_conf_low` | MATRIX | 1.000 | 4 | 4 | 规模/水平 | - | 80.0 | Daily lower bound of the approximate 95% confidence interval for the mean positive sentim… |
| 16 | `snt21_4pos_conf_up` | MATRIX | 1.000 | 6 | 6 | 规模/水平 | - | 80.0 | Daily upper bound of the approximate 95% confidence interval for the mean positive sentim… |
| 17 | `snt21_4pos_max` | MATRIX | 1.000 | 4 | 6 | 规模/水平 | - | 80.0 | Daily maximum of positive sentiment scores from TRNA equity-linked news linked to the sto… |
| 18 | `snt21_4pos_mean` | MATRIX | 1.000 | 9 | 11 | 规模/水平 | - | 80.0 | Daily mean positive sentiment score from TRNA equity-linked news linked to the stock, com… |
| 19 | `snt21_4pos_median` | MATRIX | 1.000 | 3 | 4 | 规模/水平 | - | 80.0 | Daily median positive sentiment score from TRNA equity-linked news linked to the stock in… |
| 20 | `snt21_4pos_min` | MATRIX | 1.000 | 9 | 10 | 规模/水平 | - | 80.0 | Daily minimum of positive sentiment scores from TRNA equity-linked news linked to the sto… |
