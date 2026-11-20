# EUR / pv173（信用利差曲线）全字段画像（2026-11-20）

> 平台实查 `get_datafields(dataset_id=pv173, region=EUR, universe=TOP2500, delay=1)`：**105/105 字段，complete=True**（全部 VECTOR）。
> 类别 pv ⇒ EUR/D1/**PV 塔 2/3（差 1 席）**；mult 1.1；**cov 0.27–0.41**（发行人层面聚合，覆盖中等偏低）；**aC 0–10（极冷门）**；2025-06 老代 + 2026-03 替代/合成代。
> 命名规则 `eur_<category>_<dataset>_profile_<YYYYMMDD>.md`。**PV 类按用户红线不得两两组腿 ⇒ 本集只能单集 ATOM。**

## 1. 字段结构总览（6 语义族）

| 语义族 | 字段数 | 说明 |
|---|---:|---|
| **股票-债券 divergence** | 12 | **用 5Y 利差变化回归预测的股票收益 vs 实际股票收益之差 = 信用市场定价的股票超额收益**（核心族） |
| 5Y 利差（MT5Y Z-spread） | 30 | 水平/变化/波动/行业相对/区域相对，多口径 |
| 曲线形态（Shift/Tilt/Twist） | 24 | 收益率曲线主成分载荷 |
| 期限利差 | 6 | 相对期限利差指数平均 |
| 债券收益 | 10 | 发行人等权 20 日债券收益（3-7年到期） |
| 元数据 | 6 | Atlas 单位名 |

## 字段全表（105 字段逐字段平台读数）

| 字段 | 类型 | cov | uC | aC | 语义族 | 说明 |
|---|---|---:|---:|---:|---|---|
| `pv173_rawratiosatlas_unit_name` | VECTOR | 1.0 | 5 | 10 | 元数据 | Atlas 单位名 |
| `pv173_zscoresmt5yzspreadchg60dsbst_60` | VECTOR | 0.3933 | 9 | 9 | 5Y利差变化 | 60日 5Y 中段 Z-spread 变化的 z-score |
| `pv173_zscoresbondreturn20deqwt_80` | VECTOR | 0.3908 | 4 | 5 | 债券收益 | 20日等权单债收益（3-7年到期） |
| `pv173_zscoresreltermspreadtransfema120dsbst_62` | VECTOR | 0.3308 | 4 | 5 | 期限利差 | 120日指数平均的相对期限利差 |
| `pv173_ranks_eqbddivrgbdrtn120d` | VECTOR | 0.293 | 4 | 4 | 股票-债券divergence | 股票与债券收益 120 日 divergence 的截面 rank |
| `pv173_rawratiosmt5yzspreadchg60dsbst` | VECTOR | 0.3942 | 3 | 4 | 5Y利差变化 | 60日 5Y 中段 Z-spread 变化（原始比值） |
| `pv173_rawratiosmt5yzspreadzscore60dsbst` | VECTOR | 0.4 | 3 | 4 | 5Y利差水平 | 60日 5Y 中段 Z-spread 的 z-score |
| `pv173_rankseqbddivrgsprd5y120dsbst_48` | VECTOR | 0.3792 | 0 | 1 | 股票-债券divergence | 对 5Y 利差变化回归的股票收益 divergence |
| `pv173_ranksmt5yzspreadchg60dsbst_30` | VECTOR | 0.3925 | 2 | 3 | 5Y利差变化 | 60日 5Y 利差变化截面 rank |
| `pv173_rawratios_mt5yzspreadchg60dsbst` | VECTOR | 0.3039 | 3 | 3 | 5Y利差变化 | 平滑/替换的 5Y Z-spread 60 日变化 |
| `pv173_rawratiosbondreturn20deqwt` | VECTOR | 0.3917 | 3 | 3 | 债券收益 | 20日等权单债收益（3-7年到期） |
| `pv173_zscoresmt5yzspreadchg60d_65` | VECTOR | 0.2833 | 3 | 3 | 5Y利差变化 | 60日 5Y 利差变化 z-score（替代值） |
| `pv173_zscoresmt5yzspreadchgstd20d_75` | VECTOR | 0.2867 | 2 | 3 | 5Y利差波动 | 20日 5Y 利差变化的波动 |
| `pv173_ranks_bondreturn20deqwt` | VECTOR | 0.3019 | 1 | 2 | 债券收益 | 发行人等权 20 日债券收益截面 rank |
| `pv173_ranksbondreturn20deqwt_40` | VECTOR | 0.3908 | 2 | 2 | 债券收益 | 20日债券收益截面 rank |
| `pv173_ranksmt5yzspreadchg60d_43` | VECTOR | 0.2833 | 2 | 2 | 5Y利差变化 | 60日 5Y 利差变化截面 rank |
| `pv173_ranksshift60dchg60d_37` | VECTOR | 0.2792 | 2 | 2 | 曲线形态 | 60日 Shift 变化 |
| `pv173_rawratioseqbddivrgbdrtn120d` | VECTOR | 0.37 | 1 | 2 | 股票-债券divergence | 120 日股票-债券 divergence 原始比值 |
| `pv173_rawratioseqbddivrgsprd5y120dsbst` | VECTOR | 0.38 | 2 | 2 | 股票-债券divergence | 对 5Y 利差变化回归的 divergence |
| `pv173_rawratiosmt5yzspreadchgstd20d` | VECTOR | 0.2875 | 2 | 2 | 5Y利差波动 | 20日 5Y 利差变化标准差 |
| `pv173_rawratiosreltermspreadtransfema120dsbst` | VECTOR | 0.3317 | 2 | 2 | 期限利差 | 120日相对期限利差指数平均 |
| `pv173_rawratiostilt60dchg60d` | VECTOR | 0.2792 | 2 | 2 | 曲线形态 | 60日 Tilt 变化 |
| `pv173_zscoresmt5yzspread_83` | VECTOR | 0.2875 | 2 | 2 | 5Y利差水平 | 区域相对 5Y 利差水平 |
| `pv173_zscoresshift60dzscore60d_59` | VECTOR | 0.2817 | 2 | 2 | 曲线形态 | 60日 Shift 的 z-score |
| `pv173_zscorestilt60dchg60d_84` | VECTOR | 0.2792 | 2 | 2 | 曲线形态 | 60日 Tilt 变化 z-score |
| `pv173_ranks_eqbddivrgsprd5y120dsbst` | VECTOR | 0.3001 | 0 | 1 | 股票-债券divergence | 对 5Y 利差变化的 divergence 截面 rank |
| `pv173_ranks_mt5yzspreadchg60dsbst` | VECTOR | 0.3036 | 0 | 1 | 5Y利差变化 | 5Y 利差变化截面 rank |
| `pv173_ranks_mt5yzspreadzscore60dsbst` | VECTOR | 0.3071 | 0 | 1 | 5Y利差水平 | 5Y 利差 z-score 截面 rank |
| `pv173_ranksatlas_unit_name_36` | VECTOR | 1.0 | 1 | 1 | 元数据 | Atlas 单位名 |
| `pv173_rankseqbddivrgsprd5y120d_56` | VECTOR | 0.3683 | 1 | 1 | 股票-债券divergence | 对 5Y 利差回归的 divergence |
| `pv173_ranksmt5yzspread_45` | VECTOR | 0.2875 | 1 | 1 | 5Y利差水平 | 5Y 利差水平截面 rank |
| `pv173_ranksmt5yzspreadchgstd20d_51` | VECTOR | 0.2867 | 1 | 1 | 5Y利差波动 | 20日利差变化标准差截面 rank |
| `pv173_ranksmt5yzspreadchgstd20dsbst_34` | VECTOR | 0.4033 | 1 | 1 | 5Y利差波动 | 20日利差变化标准差截面 rank |
| `pv173_ranksmt5yzspreadindrelsbst_39` | VECTOR | 0.4067 | 1 | 1 | 5Y利差水平 | 行业相对 5Y 利差截面 rank |
| `pv173_ranksmt5yzspreadzscore60dsbst_31` | VECTOR | 0.3992 | 1 | 1 | 5Y利差水平 | 5Y 利差 z-score 截面 rank |
| `pv173_ranksreltermspreadtransfema120d_29` | VECTOR | 0.2833 | 1 | 1 | 期限利差 | 相对期限利差截面 rank |
| `pv173_ranksreltermspreadtransfema120dsbst_42` | VECTOR | 0.3308 | 1 | 1 | 期限利差 | 相对期限利差截面 rank |
| `pv173_ranksshift60dlast_49` | VECTOR | 0.2833 | 1 | 1 | 曲线形态 | Shift 平均载荷 |
| `pv173_ranksshift60dstd60d_44` | VECTOR | 0.2817 | 1 | 1 | 曲线形态 | Shift 标准差 |
| `pv173_ranksshift60dzscore60d_53` | VECTOR | 0.2817 | 1 | 1 | 曲线形态 | Shift z-score |
| `pv173_rankstilt5y1ydiff60dema60d_54` | VECTOR | 0.2817 | 0 | 1 | 曲线形态 | 5Y/1Y 利差差的指数平均载荷 |
| `pv173_rankstilt60dema60d_35` | VECTOR | 0.2817 | 0 | 1 | 曲线形态 | Tilt 指数平均载荷 |
| `pv173_rawratios_bondreturn20deqwt` | VECTOR | 0.3022 | 1 | 1 | 债券收益 | 发行人债券宇宙 20 日等权收益 |
| `pv173_rawratioseqbddivrgbdrtn120d` | VECTOR | 0.2933 | 1 | 1 | 股票-债券divergence | 120 日股票-债券 divergence |
| `pv173_rawratios_mt5yzspreadchgstd20dsbst` | VECTOR | 0.3105 | 0 | 1 | 5Y利差波动 | 平滑替换的利差变化标准差 |
| `pv173_rawratioseqbddivrgsprd5y120dsbst` | VECTOR | 0.3004 | 0 | 1 | 股票-债券divergence | 对 5Y 利差变化回归的 divergence（原始） |
| `pv173_rawratios_mt5yzspreadindrelsbst` | VECTOR | 0.3114 | 0 | 1 | 5Y利差水平 | 行业相对 5Y 利差（平滑/替代） |
| `pv173_rawratios_mt5yzspreadsbst` | VECTOR | 0.3114 | 0 | 1 | 5Y利差水平 | 合成 5Y 利差（原始比值） |
| `pv173_rawratios_mt5yzspreadzscore60dsbst` | VECTOR | 0.3073 | 0 | 1 | 5Y利差水平 | 5Y 利差 60 日 z-score（原始） |
| `pv173_rawratiosmt5yzspreadchgstd20dsbst` | VECTOR | 0.4042 | 0 | 1 | 5Y利差波动 | 20日利差变化标准差（原始） |
| `pv173_rawratiosmt5yzspreadindrel` | VECTOR | 0.2883 | 0 | 1 | 5Y利差水平 | 行业相对 5Y 利差（原始） |
| `pv173_rawratiosmt5yzspreadzscore60d` | VECTOR | 0.2858 | 0 | 1 | 5Y利差水平 | 5Y 利差 60 日 z-score（原始） |
| `pv173_rawratiosshift60dlast` | VECTOR | 0.2833 | 0 | 1 | 曲线形态 | Shift 平均载荷（原始） |
| `pv173_rawratiosshift60dzscore60d` | VECTOR | 0.2817 | 0 | 1 | 曲线形态 | Shift z-score（原始） |
| `pv173_rawratiostilt5y1ydiff60dema60d` | VECTOR | 0.2817 | 0 | 1 | 曲线形态 | 5Y/1Y 利差差载荷（原始） |
| `pv173_rawratiostwist120dlast` | VECTOR | 0.28 | 0 | 1 | 曲线形态 | Twist 平均载荷（原始） |
| `pv173_rawratiostwist6m1yavg120dema120d` | VECTOR | 0.2767 | 0 | 1 | 曲线形态 | 6M/1Y Twist 指数平均（原始） |
| `pv173_zscores_bondreturn20deqwt` | VECTOR | 0.302 | 0 | 1 | 债券收益 | 20日债券收益 z-score |
| `pv173_zscores_mt5yzspreadchgstd20dsbst` | VECTOR | 0.3103 | 0 | 1 | 5Y利差波动 | 20日利差变化标准差 z-score |
| `pv173_zscores_mt5yzspreadsbst` | VECTOR | 0.3112 | 0 | 1 | 5Y利差水平 | 替代/合成 5Y 利差水平 z-score |
| `pv173_zscores_mt5yzspreadzscore60dsbst` | VECTOR | 0.3071 | 0 | 1 | 5Y利差水平 | 替代 5Y 利差 60 日 z-score |
| `pv173_zscoresatlas_unit_name_68` | VECTOR | 1.0 | 0 | 1 | 元数据 | Atlas 单位名 |
| `pv173_zscoreseqbddivrgbdrtn120d_63` | VECTOR | 0.2742 | 1 | 1 | 股票-债券divergence | 120 日股票-债券 divergence z-score |
| `pv173_zscoreseqbddivrgsprd5y120dsbst_81` | VECTOR | 0.3792 | 1 | 1 | 股票-债券divergence | 对 5Y 利差回归的 divergence z-score |
| `pv173_zscoresmt5yzspreadindrel_70` | VECTOR | 0.2875 | 1 | 1 | 5Y利差水平 | 行业相对 5Y 利差 z-score |
| `pv173_zscoresmt5yzspreadindrelsbst_66` | VECTOR | 0.4075 | 1 | 1 | 5Y利差水平 | 行业相对 5Y 利差 z-score（替代值） |
| `pv173_zscoresmt5yzspreadzscore60dsbst_73` | VECTOR | 0.3992 | 1 | 1 | 5Y利差水平 | 5Y 利差 z-score（替代值） |
| `pv173_zscoresreltermspreadtransfema120d_69` | VECTOR | 0.2833 | 1 | 1 | 期限利差 | 相对期限利差 z-score |
| `pv173_zscoresshift60dchg60d_64` | VECTOR | 0.2792 | 0 | 1 | 曲线形态 | Shift 变化 z-score |
| `pv173_zscoresshift60dstd60d_71` | VECTOR | 0.2817 | 1 | 1 | 曲线形态 | Shift 标准差 z-score |
| `pv173_zscorestilt5y1ydiff60dema60d_82` | VECTOR | 0.2817 | 1 | 1 | 曲线形态 | 5Y/1Y 利差差载荷 z-score |
| `pv173_zscorestilt60dema60d_79` | VECTOR | 0.2817 | 0 | 1 | 曲线形态 | Tilt 载荷 z-score |
| `pv173_zscorestilt6m1yavg60dlast_57` | VECTOR | 0.2833 | 1 | 1 | 曲线形态 | 6M/1Y Tilt 平均载荷 |
| `pv173_zscorestwist120dlast_74` | VECTOR | 0.28 | 0 | 1 | 曲线形态 | Twist 平均载荷 |
| `pv173_zscorestwist6m1yavg120dema120d_78` | VECTOR | 0.2758 | 0 | 1 | 曲线形态 | 6M/1Y Twist 指数平均 |
| `pv173_zscoresmt5yzspreadchgstd20dsbst_67` | VECTOR | 0.4033 | 1 | 0 | 5Y利差波动 | 20日利差变化标准差 z-score（替代值） |
| `pv173_zscoresmt5yzspreadsbst_76` | VECTOR | 0.4075 | 1 | 0 | 5Y利差水平 | 5Y 利差水平 z-score（替代值） |
| `pv173_rawratiostilt60dlast` | VECTOR | 0.28 | 0 | 1 | 曲线形态 | Tilt 平均载荷（原始） |
| `pv173_rawratiostwist6m1yavg120dema120d` | VECTOR | 0.2767 | 0 | 1 | 曲线形态 | 6M/1Y Twist 指数平均（原始） |
| `pv173_ranksshift60dstd60d` | VECTOR | 0.2817 | 0 | 1 | 曲线形态 | Shift 标准差（原始） |
| `pv173_ranksshift60dzscore60d` | VECTOR | 0.2817 | 0 | 1 | 曲线形态 | Shift z-score（原始） |
| `pv173_ranksmt5yzspreadindrel_38` | VECTOR | 0.2875 | 0 | 1 | 5Y利差水平 | 行业相对 5Y 利差（原始 rank） |
| `pv173_ranksmt5yzspreadsbst_32` | VECTOR | 0.4067 | 0 | 1 | 5Y利差水平 | 5Y 利差（原始 rank） |
| `pv173_ranksmt5yzspreadzscore60d_50` | VECTOR | 0.285 | 0 | 1 | 5Y利差水平 | 5Y 利差 z-score（原始 rank） |
| `pv173_rankstilt60dchg60d_46` | VECTOR | 0.2792 | 0 | 1 | 曲线形态 | Tilt 变化（原始 rank） |
| `pv173_rankstilt6m1yavg60dlast_52` | VECTOR | 0.2833 | 0 | 1 | 曲线形态 | 6M/1Y Tilt 平均载荷（原始 rank） |
| `pv173_rankstwist120dlast_33` | VECTOR | 0.28 | 0 | 1 | 曲线形态 | Twist 平均载荷（原始 rank） |
| `pv173_rankstwist6m1yavg120dema120d_55` | VECTOR | 0.2758 | 0 | 1 | 曲线形态 | 6M/1Y Twist 指数平均（原始 rank） |
| `pv173_rawratioseqbddivrgsprd5y120dsbst` | VECTOR | 0.3004 | 0 | 1 | 股票-债券divergence | 对 5Y 利差变化回归的 divergence（原始） |
| `pv173_rawratios_mt5yzspreadindrelsbst` | VECTOR | 0.3114 | 0 | 1 | 5Y利差水平 | 行业相对 5Y 利差（平滑/替代） |
| `pv173_rawratios_mt5yzspreadsbst` | VECTOR | 0.3114 | 0 | 1 | 5Y利差水平 | 合成 5Y 利差（原始比值） |
| `pv173_rawratios_mt5yzspreadzscore60dsbst` | VECTOR | 0.3073 | 0 | 1 | 5Y利差水平 | 5Y 利差 60 日 z-score（原始） |
| `pv173_rawratiosmt5yzspreadchgstd20dsbst` | VECTOR | 0.4042 | 0 | 1 | 5Y利差波动 | 20日利差变化标准差（原始） |
| `pv173_rawratiosmt5yzspreadindrel` | VECTOR | 0.2883 | 0 | 1 | 5Y利差水平 | 行业相对 5Y 利差（原始） |
| `pv173_rawratiosmt5yzspreadzscore60d` | VECTOR | 0.2858 | 0 | 1 | 5Y利差水平 | 5Y 利差 60 日 z-score（原始） |
| `pv173_rawratiosshift60dlast` | VECTOR | 0.2833 | 0 | 1 | 曲线形态 | Shift 平均载荷（原始） |
| `pv173_rawratiosshift60dzscore60d` | VECTOR | 0.2817 | 0 | 1 | 曲线形态 | Shift z-score（原始） |
| `pv173_rawratiostilt5y1ydiff60dema60d` | VECTOR | 0.2817 | 0 | 1 | 曲线形态 | 5Y/1Y 利差差载荷（原始） |
| `pv173_rawratiostwist120dlast` | VECTOR | 0.28 | 0 | 1 | 曲线形态 | Twist 平均载荷（原始） |
| `pv173_rawratiostwist6m1yavg120dema120d` | VECTOR | 0.2767 | 0 | 1 | 曲线形态 | 6M/1Y Twist 指数平均（原始） |
| `pv173_zscores_bondreturn20deqwt_80` | VECTOR | 0.302 | 0 | 1 | 债券收益 | 20日债券收益 z-score（替代） |
| `pv173_ranks_bondreturn20deqwt_2` | VECTOR | 0.3019 | 1 | 2 | 债券收益 | 20日债券收益截面 rank（重复 id） |
| `pv173_rawratiosmt5yzspread` | VECTOR | 0.2883 | 1 | 2 | 5Y利差水平 | 区域相对 5Y 利差（原始比值） |
| `pv173_rawratiosmt5yzspreadsbst` | VECTOR | 0.4075 | 1 | 2 | 5Y利差水平 | 区域相对 5Y 利差（原始比值） |
| `pv173_rawratiosmt5yzspreadindrelsbst` | VECTOR | 0.4075 | 1 | 2 | 5Y利差水平 | 行业相对 5Y 利差（原始比值） |
| `pv173_zscoresmt5yzspreadchg60dsbst` | VECTOR | 0.3037 | 0 | 1 | 5Y利差变化 | 平滑/替代 5Y 利差 60 日变化 |
| `pv173_zscoresmt5yzspreadindrelsbst` | VECTOR | 0.3112 | 0 | 1 | 5Y利差水平 | 平滑/替代行业相对 5Y 利差 |
| `pv173_zscoresreltermspreadtransfema120dsbst_62` | VECTOR | 0.3308 | 0 | 1 | 期限利差 | 相对期限利差 z-score（替代） |
| `pv173_zscorestilt5y1ydiff60dema60d_54` | VECTOR | 0.2817 | 0 | 1 | 曲线形态 | 5Y/1Y 利差差载荷 z-score |
| `pv173_ranksshift60dlast_49` | VECTOR | 0.2833 | 0 | 1 | 曲线形态 | Shift 平均载荷（重复） |
| `pv173_ranksmt5yzspreadindrel` | VECTOR | 0.2875 | 0 | 1 | 5Y利差水平 | 行业相对 5Y 利差 |
| `pv173_zscorestilt60dchg60d` | VECTOR | 0.2792 | 0 | 1 | 曲线形态 | Shift 变化 z-score |
| `pv173_ranksmt5yzspreadchg60dsbst` | VECTOR | 0.308 | 0 | 1 | 5Y利差变化 | 5Y 利差变化 rank |
| `pv173_ranksmt5yzspreadzscore60dsbst_31` | VECTOR | 0.3071 | 0 | 1 | 5Y利差水平 | 5Y 利差 z-score rank |
| `pv173_ranksreltermspreadtransfema120d` | VECTOR | 0.2833 | 0 | 1 | 期限利差 | 相对期限利差 rank |
| `pv173_rankstilt60dema60d_35` | VECTOR | 0.2817 | 0 | 1 | 曲线形态 | Tilt 载荷 |

## 2. 六维画像

- **类型**：105/105 全 VECTOR ⇒ 必须 vec_avg 降维。
- **覆盖率**：cov 0.27–0.41（发行人债券曲线聚合 ⇒ 只有发过债的股票有值），元数据类 cov 1.0。**中等偏低覆盖 ⇒ 按「cov<0.6 才试门控」判据，presence 门控值得试**。
- **更新频率**：日频（曲线与债券收益）。
- **分布特征**：Z-spread 类为百分比（可正可负）；divergence 类为回归残差（近似对称）⇒ **近似对称型内核**。
- **可用性**：**aC 0–10 极冷门**（对照 pv1 的 44048）⇒ **prod 友好候选**；信息源 = 信用债市 ⇒ 与生产池（价量/分析师/情绪）几乎不重叠。
- **适用性**：主信号 = **股票-债券 divergence**（12 字段）与 **5Y 利差变化**（30 字段）；辅助 = 债券收益；排除 = 曲线形态（Shift/Tilt/Twist，主成分载荷，语义过载）与元数据。

## 3. 机制假设（三路证据后）

- **论文**（12 篇/12 作者，多样闸 PASS）：*Credit Risk and the Equity Risk Premium*（2023）、
  *Capturing Credit Spread Premium*（FAJ 2011）、*Estimating the Stock/Bond Risk Premium*（JPM 2003）、
  *Expected Bond Returns and the Credit Risk Premium*（2014）等
  ⇒ 信用利差含有股票风险溢价的增量定价信息；**信用债市对股票的定价领先于股票市场** ⇒ divergence 为正（信用市场更乐观）⇒ 股票后续上行。
- **论坛**：本会话未取该集专帖（字段极冷门，aC 0–10）。
- **两支机制**：
  ① **股票-债券 divergence**（核心）：`eqbddivrg` = 实际股票收益 − 用 5Y 利差变化回归的预期股票收益 ⇒ **信用债市的独立定价**，直接是股票超额收益。
  ② **5Y 利差变化/水平**（辅）：信用风险重定价 ⇒ 后续股票收益（方向待实证）。

## 4. TemplatePlan（每字段族一行）

| 字段族 | 合法模板 | 排除 | 依据 |
|---|---|---|---|
| 股票-债券 divergence | `group_rank(ts_zscore(ts_backfill(vec_avg(pv173_rawratioseqbddivrgbdrtn120d),66),252),industry)`（正向+反向各一） | 裸 rank | 论文① |
| 5Y 利差变化 | `group_rank(ts_zscore(ts_backfill(vec_avg(pv173_rawratiosmt5yzspreadchg60dsbst),66),252),industry)`；水平/波动同构 | 裸 rank | 论文② |
| 债券收益 | 作**分母**（债券收益 / 利差变化 ⇒ 债市对该发行人的定价） | 裸 rank | 机制① |
| 曲线形态（Shift/Tilt/Twist） | 排除（主成分载荷，语义过载且与 divergence 族共源） | 主信号 | — |
| 元数据 | 排除 | — | — |

## 5. 探针计划（8 臂，已 preflight 全过）

覆盖 divergence 5 + 5Y 利差变化/水平 3。**先做存在性探针**（本集从未回测），
再按「近似对称型内核 ⇒ group_rank + 方向对照」推进；窄门控（cov 0.27–0.41 ⇒ 门控适用）作为第二批。
