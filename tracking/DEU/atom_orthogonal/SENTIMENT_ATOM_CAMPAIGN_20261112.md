# SENTIMENT 塔 ATOM 攻坚（进行中）

日期：2026-11-12　用户指令：「转到 sentiment 下同样去组 atom」

## 一、数据集盘点（DEU sentiment 类共 3 个，全部同属 DEU/D1/SENTIMENT 塔 ⇒ 组合保 ATOM）

| 数据集 | 字段数 | 覆盖率 | 用户/alpha 数 | 机制 |
|---|---:|---:|---|---|
| **sentiment33** | 255 | **0.3258** | 34 / 51 | 情感模型得分 + 正/负/中性计数 |
| **sentiment27** | 18 | **0.9038** | 134 / 344 | 关注度排名、峰度、偏度、来源广度 |
| **sentiment7** | 3 | **0.7418** | 55 / 99 | 浏览量（关注量）|

**三者机制互补**：33 = 情感方向，27 = 关注度/来源广度，7 = 关注量。

## 二、sentiment33 字段族（255 个，全 VECTOR）

### 情感模型得分（20 个）
`sentiment_model7_score1[_fkw1..4]`、`sentiment_model9_score4[_fkw1..4]`、`sentiment_model6_negative_score_fkw2/3/4`、`sentiment_model8_score_fkw2/3`、`sentiment_model9_score2/3`

### 正/负/中性计数（method 1-6 × fkw1-4）
`snt33_sefke1v1_fkw{1..4}_method_{1..6}_{pos,neg,neut}`
过滤版：`..._method_N_filtered_{pos,neg,neut,obj}`

### 其他
`snt33_N_{event_title,headline,true_timestamp,...}`（文本/时间戳，无信号）

## 三、sentiment27 字段（18 个，全 VECTOR，cov 0.90）
`snl27_avgranking`、`snl27_topranking`、`snl27_top50pctranking[avg]`、`snl27_top75pctranking[avg]`、`snl27_kurtosis`、`snl27_skewness`、`snl27_relpopularity08`、`snl27_relpopularity1`、`snl27_totaldomains`、`snl27_totalcountrydomains`、`snl27_wq_pit`、`snt27_rank`

## 四、已跑波次与读数

### SE1（sentiment33 单族，ts_mean 水平型）6 臂
| 构造 | S | F | Y2 | sub | TO |
|---|---:|---:|---:|---:|---:|
| 净情感 method1 | 0.29 | 0.17 | 0.79 | 0.24 | 4.0% |
| 净情感 m1+m2+m3 | 0.21 | 0.11 | 0.60 | 0.40 | 4.0% |
| 模型得分 model9 | 0.20 | 0.10 | 0.78 | 0.41 | 4.0% |
| 模型得分 model7 | 0.19 | 0.09 | 0.78 | 0.42 | 4.0% |
| 净情感+model7+model9 | 0.10 | 0.03 | 0.14 | 0.25 | 3.4% |
| 净情感 method2 | 0.09 | 0.03 | 0.21 | 0.21 | 3.5% |

### SE2（事件型正确后处理：winsorize + ts_sum + tail）6 臂
| 构造 | S | F | Y2 | sub |
|---|---:|---:|---:|---:|
| 正计数 Σ66 + tail | 0.36 | 0.23 | −0.03 | 0.49 |
| 净情感 Σ66 + tail | 0.35 | 0.22 | −0.10 | 0.47 |
| 净情感+model7 Σ66 | 0.28 | 0.17 | −0.32 | 0.31 |
| 负计数 Σ66 + tail | 0.26 | 0.15 | 0.08 | 0.36 |
| 净情感 Σ252 + tail | 0.15 | 0.07 | −0.05 | 0.29 |
| model7 Σ66 + tail | −0.12 | −0.05 | −0.40 | 0.50 |

### SE3（三数据集同塔组合）6 臂
| 构造 | S | F | Y2 | sub |
|---|---:|---:|---:|---:|
| 33×27 交互（情感×关注度）| 0.39 | 0.19 | 0.53 | −0.17 |
| 33+27+7 等权 | 0.31 | 0.12 | 0.74 | −0.49 |
| 33×7 交互 | 0.14 | 0.06 | 0.58 | 0.27 |
| 27×7 交互 | −0.08 | −0.02 | 0.31 | −0.16 |
| 三集三重交互 | −0.16 | −0.04 | 0.60 | −0.77 |
| 33+27B+7 | −0.18 | −0.05 | 0.38 | −0.78 |

### SE4（sentiment27 全字段方向扫描）6 臂
| 构造 | S | F | Y2 | sub |
|---|---:|---:|---:|---:|
| kurtosis 正 | **0.69** | 0.43 | 1.35 | 0.01 |
| skewness 反向 | 0.63 | 0.35 | 0.90 | −0.14 |
| avgranking 正 | 0.10 | 0.02 | 0.21 | −0.90 |
| avgranking 反向 | −0.10 | −0.02 | −0.21 | **0.90** |
| relpopularity08 | −0.41 | −0.19 | −1.50 | −0.77 |
| topranking | −0.82 | −0.49 | −0.99 | −0.56 |

**累计 24 臂，最高 S 0.69（snl27_kurtosis）。**

## 五、初步判读

1. **单族信号极弱**：sentiment33（cov 0.33）净情感/模型得分全部 ≤0.29，TO 仅 3.5-4%。
2. **事件型后处理不救**：winsorize+ts_sum+tail 只到 0.36。
3. **三集组合无效**：等权/交互全在 −0.18~0.39，且 sub 频繁为负。
4. **唯一有形态的是 kurtosis（0.69）与 skewness 反向（0.63）** —— 但这属于「关注度分布形态」而非情感。
5. **avgranking 反向的 sub = 0.90 是全塔最高 sub**，但 S 为负（−0.10），说明方向反了但横截面结构有效。

## 六、待验证

SE5（来源广度 + 关注度异常）6 臂在跑，含 `snl27_totaldomains`、`totalcountrydomains`、`snt7_views` z-score、多语言浏览量差。

## 七、AI 引擎处理状态
