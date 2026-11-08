# risk59 判死 · 转向 fundamental44 / analyst16（2026-11-07）

## 1. risk59 封盘（S 天花板 1.02，缺口 0.56）

数据集 risk59 = 韩国借券/空头拥挤度数据（16 VECTOR 字段，cov 0.9806）。
累计 10 条几何全部实测，最强 +1.02：

| alpha | 几何 | S | F | 2Y | sub | TO |
|---|---|---:|---:|---:|---:|---:|
| 9qxMnXg1 | `group_rank(vec_avg(rsk59_daystocover90day), sector)` | **+1.02** | 0.82 | 1.28 | 0.98 | 0.0864 |
| kqNOxzXz | `group_rank(multiply(dtc90, squeeze_risk), sector)` | 0.94 | 0.59 | 1.53 | 0.91 | 0.1701 |
| 78LMkNd8 | `group_rank(vec_avg(rsk59_short_interest), sector)` | 0.75 | 0.48 | 0.88 | 0.67 | 0.0683 |
| A1VzAdYX | `-group_rank(vec_avg(rsk59_short_interest), sector)` | −0.97 | −0.69 | −1.21 | −0.94 | 0.0682 |
| leAGoax8 | `-group_rank(vec_avg(rsk59_short_momentum), sector)` | −0.62 | −0.19 | −0.67 | −0.48 | 0.4325 |
| zq3GVzQ8 | `-group_rank(vec_avg(rsk59_shortinterestpct), sector)` | −0.53 | −0.28 | −1.15 | −0.51 | 0.0709 |
| leAGmjJ8 | `-group_rank(vec_avg(rsk59_s3utilization), sector)` | −0.49 | −0.24 | −0.79 | −0.23 | 0.0715 |
| xArWKJQn | `group_rank(ts_zscore(dtc90, 250), sector)` | 0.36 | 0.15 | **1.61** | 0.41 | 0.0999 |
| 58E5PJRM | `-group_rank(vec_avg(rsk59_crowded_score), sector)` | −0.18 | −0.05 | −0.18 | 0.00 | 0.0786 |
| QPvg1bQ5 | `trade_when(ts_arg_max(dtc90,90)<33, signed_power(ts_quantile(dtc90,840,driver="gaussian"),1.6), -1)` | 0.13 | 0.03 | 1.20 | 0.19 | 0.1439 |

**关键结论**
1. **取负非镜像再次证实**：short_interest 正向 +0.75 vs 负向 −0.97 —— 同一字段两臂差 0.22，必须各自实测，不能靠翻符号省批次。
2. **ts_arg_max 门控在 risk59 上失效**（0.13），与「作信号=摧毁器、作门控=冠军」的既有记忆矛盾 ⇒ 该结论**绑定 institutions6 类披露计数数据**，不可跨族外推。
3. 唯一 2Y 过线的是 `ts_zscore(dtc90,250)`（2Y 1.61）但 S 仅 0.36 —— 印证既有的「平滑/标准化算子压 S、抬 2Y」反向关系。
4. **封盘判据达成**：5 个机制面（水平 / 变化 / 标准化 / 交互乘积 / 门控）全撞墙，最强 1.02 距 1.58 差 0.56，与 dl_riskfree 同型 —— 机制性上限，不是模板不够多。

## 2. analyst11 排除（KOR 仅 1 字段）

`get_datafields(analyst11, KOR)` 只返回 1 个字段 `pollution_prevention_industry_rank`（cov 0.6813）⇒ 无法构成 ATOM 多字段组合，直接排除。

## 3. analyst44 观察（暂缓，非判死）

520 字段全 VECTOR，cov 仅 0.40–0.63；每条指标有 `{value, prevalue, lastactvalue}` 三元组可构造**修正量**（`value - prevalue`），机制正确但覆盖率偏低（TOP600 里仅 240–380 只有值）。排在 fundamental44 / analyst16 之后。

## 4. 本轮新方向（最高 EV）

### P16 — fundamental44「会计质量模型」12 MATRIX 字段，cov **0.8984**
十年级覆盖最好的一批字段（memory 纪律：cov 是下限筛，防连续空窗）。
族：Beneish M-Score / F-Score / Jones 与修正 Jones 应计 / 现金流应计 / 营运资本应计 / Yoon 应计 / Benford 法证分 / 财报重述概率。
学术先验（应计异象 Sloan 1996、Beneish 1999 M-Score、Dechow 2011 F-Score）：**高应计 / 高 M 分 / 高重述概率 → 未来收益差**，故 9/10 条取负号，仅 F-Score 方向存疑保留正向做对照。

### P17 — analyst16「Real Time Estimates」cov 0.58–0.72，VECTOR
机制与已出货的 analyst10（S 1.94）同族但**信息加工方式不同**：
- 修正幅度（`afterest_percentage` / `aftercons_percentage` / `afterest_difference`）—— 事件型
- **分析师分歧**（`eststddev_normal / |meanest_normal|`）—— 横截面离散，非修正
- 实际超预期情绪分 `actsuescore`
- 推荐分布（`meanrec`、`1scermun/scermun` 强买占比）—— 意见面
- 覆盖广度（`numests`）、预估区间宽度（`highest−lowest`）
6 个互异加工面 ⇒ 满足模板多样性 ≥10（本条 10 个模板覆盖 6 个面）。

## 5. 交付进度

3/10（omERn83n / qMLOooX1 / RRE9NkVj），本轮未新增可提交件。
