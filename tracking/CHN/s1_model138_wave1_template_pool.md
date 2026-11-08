# CHN `model138`（PDI 表现偏离指数）wave1 模板池 — 2026-11-06

> **场地**：CHN / TOP2000U / D1（CHN 唯一合法 universe，无 COUNTRY 中性化档）。
> **档位**：SUBINDUSTRY / decay4 / trunc0.08 / unit VERIFY / nan OFF / pasteurization ON / maxTrade OFF。
> **为什么开**：CHN 塔位 **0/3（12 塔全未点亮）** ⇒ 不受「已点亮塔不选」约束；`model138` 平台 **alphaCount 604**、**字段覆盖率 min 0.9985**（本区最高档），120 字段。

## ★ 零、头号陷阱：`model138` 字段是 **VECTOR**，必须 `vec_avg()` 包装

`get_datafields` 返回的 `type` 字段显示为 `VECTOR`。**`validate_expressions` 不校验字段类型**（只查存在性），所以裸字段能过校验但回测直接 ERROR：

```
Operator subtract does not support event inputs.
Operator ts_std_dev does not support event inputs.
extra_info: If fields is vector type should use vec_* operator with event input
```

**⇒ 铁律**：本数据集每个字段（含复合 `mdl138_3idpc`）都必须包一层 `vec_avg(...)`。首批批 `4hLQUha0...` 就是这样 2/2 全 ERROR 的，换成 `vec_avg` 版重派为 `2sUsdadzE5bAahpuXWXS5m7`。

## 一、字段画像（120 字段 = 4 套命名，覆盖率 0.9985–0.999，全部 VECTOR）

**PDI = Performance Deviation Index**：某个会计比率**相对其预期/趋势水平的偏离度**。语义上是「基本面意外/预期差」，不是水平值本身。

| 套 | 命名模式 | 数量 | 说明 |
|---|---|---:|---|
| 复合 | `mdl138_{3,4,5}idpc` | 3 | 复合 PDI（跨指标聚合） |
| 复合·质量调整 | `mdl138_{3,4,5}idpqc` | 3 | 质量调整复合 PDI |
| 原始指标 | `mdl138_{metric}_{3,4,5}idp` | 33 | metric ∈ dtl / epp / er / in / ofc / pa / pg / tvni / vcer / vd（10 个）+ **`aor` 例外：后缀是 `idpq`（`mdl138_aor_{3,4,5}idpq`）** |
| 质量调整指标 | `mdl138_qpdi{3,4,5}_{metric}` | 69 | 23 个 metric |
| 绝对水平偏离 | `mdl138_pdi{3,4,5}_{metric}` | 12 | metric ∈ caps / cash / ebitda / sale（**绝对金额级**，不是比率） |

**★ 三个命名陷阱（写表达式必踩）**：
1. **`aor` 是唯一后缀为 `idpq` 的原始指标**（其余 10 个是 `idp`）——写成 `mdl138_aor_3idp` 会 unknown。
2. **`qpdi` / `pdi` 的窗口在中间、指标在后面**（`mdl138_qpdi3_roic`），而 `idp` 族窗口在后面（`mdl138_er_3idp`）。两族顺序相反。
3. **`pdi{w}_{ebitda,sale,cash,caps}` 是绝对水平偏离**，与比率族（qpdi/idp）**量纲不同**，不能直接 `add`/`subtract` 混用（unit VERIFY 下会报单位不兼容）。

**23 个 qpdi 指标按经济含义分组**：

| 组 | 指标 |
|---|---|
| 盈利/现金流回报 | `roic` `roe` `rnoa` `cfroa` `cfroe` `cfrnoa` |
| 利润率 | `gross_margin` `op_margin` `net_margin` |
| 流动性 | `current_r` `quick_r` `cfo_curr_liab` |
| 杠杆结构 | `debt_equity` `debt_capital` `debt_mktcapital` `lt_dt_capital` `lt_dt_equity` `int_cover` |
| 营运资本周转 | `invent_to` `receiva_to` `payable_to` |
| 综合/其他 | `berry`（毛利率×周转）`sale_empl`（人均销售） |

## 二、文献与论坛先验（模板来源）

| # | 来源 | 迁移到 PDI 的结论 |
|---|---|---|
| L1 | Dechow & Dichev (2002) | 盈余**相对现金流**的偏离度越大，盈余质量越差、持续性越低 ⇒ PDI 高的公司未来应跑输 |
| L2 | Beneish (1999) M-score | 比率**异常偏离**是财务操纵的指纹，市场反应滞后 ⇒ 背离可交易 |
| L3 | Piotroski (2000) F-score | **多指标同向改善**才有效，单指标改善易噪声 ⇒ 支持合成类模板 |
| L4 | Fairfield, Whisenant & Yohn (2003) | 长期经营资产**增长**预示低收益（投资异象）⇒ `pdi{caps,sale,ebitda}` 绝对偏离族应取负向 |
| L5 | Richardson, Sloan, Soliman & Tuna (2005) | 应计可靠性越低，均值回复越快 ⇒ **一阶差分/二阶方差**类模板有独立信息 |
| L6 | Novy-Marx (2013) | 毛利率是最高质量的盈利指标 ⇒ `qpdi*_gross_margin` 应单独建腿 |
| L7 | Hirshleifer et al. (2004) | 净经营资产膨胀预示低收益 ⇒ 营运资本三角（存货+应收−应付）值得单独测 |
| L8 | **CHN 本地实证（model36，2026-11-06）** | **A 股是低质量溢价，方向与美股系统性相反** ⇒ **PDI 的符号不可先验假定，必须由 wave1 实测锚定** |
| L9 | **本次会证实证（§290.7/290.8）** | **在表达式前加一元负号不会翻转 alpha 方向** ⇒ 不要用 `-group_rank(...)` 做方向修正，改用语义相反的字段或改几何 |

## 三、13 个结构互异模板（四维 = 骨架 / 算子几何 / 矩 / 分组轴 / 非线性）

下文 `V(...)` 是 `vec_avg(...)` 的简写；实际表达式必须显式写 `vec_avg`。

| # | 模板 | 表达式核心 | 骨架 | 矩 | 分组轴 | 非线性 | 算子 | 文献 |
|---|---|---|---|---|---|---|---:|---|
| T1 | 质量调整盈利背离（单腿水平） | `group_rank(vec_avg(mdl138_qpdi3_roic), subindustry)` | 单腿 | 水平 | subindustry | 无 | 2 | L1/L6 |
| T2 | **PDI 期限结构（短−长）** | `group_rank(subtract(vec_avg(mdl138_3idpqc), vec_avg(mdl138_5idpqc)), subindustry)` | 双腿价差 | 水平差 | subindustry | 无 | 4 | L2/L5 |
| T3 | 质量调整 − 原始背离 | `group_rank(subtract(vec_avg(mdl138_qpdi3_roic), vec_avg(mdl138_er_3idp)), subindustry)` | 双腿价差 | 水平 | subindustry | 无 | 4 | L2 |
| T4 | 盈利 vs 杠杆方向冲突 | `group_rank(subtract(vec_avg(mdl138_qpdi3_roic), vec_avg(mdl138_qpdi3_debt_equity)), subindustry)` | 双腿反向 | 水平 | subindustry | 无 | 4 | L1/L7 |
| T5 | **背离的二阶方差（不稳定度）** | `group_rank(ts_std_dev(vec_avg(mdl138_3idpc), 252), subindustry)` | 单腿 | **二阶方差** | subindustry | 无 | 3 | L5 |
| T6 | 背离加速（一阶差分） | `group_rank(ts_delta(vec_avg(mdl138_qpdi3_gross_margin), 66), subindustry)` | 单腿 | **一阶差分** | subindustry | 无 | 3 | L3/L6 |
| T7 | 现金×资本双绝对偏离交互 | `group_rank(multiply(rank(vec_avg(mdl138_pdi3_cash)), rank(vec_avg(mdl138_pdi3_caps))), subindustry)` | 双排序乘积 | 水平 | subindustry | 交互项 | 6 | L4/L7 |
| T8 | 极端复合背离门控 | `trade_when(greater(ts_rank(vec_avg(mdl138_3idpc), 252), 0.9), group_rank(vec_avg(mdl138_qpdi3_roic), subindustry), 0)` | 门控 | 水平 | subindustry | 极值截断 | 6 | L2 |
| T9 | 去掉复合成分后的残差 | `group_rank(ts_regression(vec_avg(mdl138_qpdi3_roic), vec_avg(mdl138_3idpc), 252, 0, 2), subindustry)` | 回归残差 | 水平+趋势 | 无→subindustry | 正交化 | 4 | L3 |
| T10 | 凸性变换 | `group_rank(signed_power(group_zscore(vec_avg(mdl138_qpdi3_roic), subindustry), 1.4), subindustry)` | 单腿 | 水平 | subindustry | **signed_power 1.4** | 5 | EUR 实证 |
| T11 | 极值截尾 | `tail(winsorize(group_rank(vec_avg(mdl138_qpdi3_roe), subindustry), std=2), lower=0.05, upper=0.95, newval=0.5)` | 单腿 | 水平 | subindustry | 截尾 | 4 | 稳健性 |
| T12 | 行业相对超额（双层轴） | `group_rank(subtract(vec_avg(mdl138_qpdi3_roic), group_mean(vec_avg(mdl138_qpdi3_roic), industry)), subindustry)` | 双腿 | 水平 | **industry→subindustry** | 无 | 5 | L1 |
| T13 | 营运资本三角（存货+应收−应付） | `group_rank(subtract(add(vec_avg(mdl138_qpdi3_invent_to), vec_avg(mdl138_qpdi3_receiva_to)), vec_avg(mdl138_qpdi3_payable_to)), subindustry)` | 三腿 | 水平 | subindustry | 无 | 5 | L7 |

**四维覆盖自检**：骨架 6 类（单腿 / 双腿价差 / 双腿反向 / 三腿 / 门控 / 回归残差）；矩 4 阶（水平 / 一阶差分 / 二阶方差 / 水平差）；分组轴 3 种（subindustry / industry→subindustry 双层 / 无）；非线性 4 种（交互项 / 极值截断 / 正交化 / signed_power）⇒ 满足「≥10 个结构互异」的验收口径（不是 13 条同构变体）。

## 四、wave1 首批（已重派）

批 `2sUsdadzE5bAahpuXWXS5m7`（首派 `4hLQUha0C4uLayUhLhcmizh` 因缺 `vec_avg` 2/2 ERROR）：

| tag | 模板 | 表达式 | 算子 |
|---|---|---|---:|
| W1-E1 | T2 PDI 期限结构 | `group_rank(subtract(vec_avg(mdl138_3idpqc), vec_avg(mdl138_5idpqc)), subindustry)` | 4 |
| W1-E2 | T5 二阶方差 | `group_rank(ts_std_dev(vec_avg(mdl138_3idpc), 252), subindustry)` | 3 |

**选这两条的理由**：① 矩阶完全不同（水平差 vs 二阶方差），互相关预期低；② T2 检验「背离的时间期限结构」是否被定价，这是 PDI 家族的独有结构（普通比率数据没有多窗口版本）；③ T5 检验「基本面稳定性溢价/折价」，即使水平无效也可能独立成立；④ 两条都不是单腿水平，避开「PDI 水平可能已被 aC 604 的存量件吃干」的风险。

## 五、执行记录

- 2026-11-06 04:45：字段画像完成（120 字段 / 4 套命名 / 3 个命名陷阱）。
- 2026-11-06 04:46：wave1 首批 `4hLQUha0...` 派发 → **2/2 ERROR（VECTOR 字段缺 vec_avg）**。
- 2026-11-06 04:48：修正为 `vec_avg` 版，重派 `2sUsdadzE5bAahpuXWXS5m7`。
- 2026-11-06 04:52：wave1 收批。

## 六、wave1 实测（CHN/TOP2000U/SUBINDUSTRY/decay4，批 `2sUsdadzE5bAahpuXWXS5m7`）

| tag | 模板 | alpha | S | F | TO | 2Y | 判定 |
|---|---|---|---:|---:|---:|---:|---|
| W1-E1 | T2 PDI 期限结构 | `qML5qeZv` | **−1.51** | −0.87 | 5.5% | **+2.03** | 量级可观但**方向为负**，且 2Y 与全期**符号相反** ⇒ 信号在近两年翻转，不稳定 |
| W1-E2 | T5 二阶方差 | `E56mJoAK` | **−1.01** | −0.48 | 2.6% | −1.41 | 负向一致但量级不足 |

**⇒ 三条结论**：
1. **PDI 期限结构（T2）是这个数据集里最强的腿**：|S| 1.51、TO 仅 5.5%，比二阶方差（1.01）强 50%。远端−近端复合 PDI 之差承载了真实的「背离加速」信息。
2. **但 T2 的 2Y（+2.03）与全期（−1.51）符号相反** —— 这条腿在样本内前后段方向翻转，属于**结构不稳定**，即使能翻正也不该直接提交，必须先做分段归因（哪一年开始翻转、为什么）。
3. **方向仍为负，且本环境加负号不翻号**（见台账 §290.8）⇒ T2 不能靠 `-` 修正。
   - **下一步的判别性测试**：把窗口对调写成 `subtract(vec_avg(5idpqc), vec_avg(3idpqc))`。**注意这在代数上就是 T2 的负号**，所以它不是一个「新信号」，而是一个**机制探针**：若平台在该写法下仍然给负 S ⇒ 符号不敏感发生在**权重/中性化层**（表达式怎么写都没用，只能换字段）；若这次翻出了正 S ⇒ 说明问题出在**表达式层的负号解析**，那就可以继续用「值域内取负」改写一切方向。这一条结论会决定整个 CHN 后续策略。
   - 真正能改变方向的替代：T3（质量调整 − 原始背离）与 T4（盈利 − 杠杆）用的是**减法两侧的不同字段**，不是同一信号的取负，属于合法换几何。

- **下一批建议**：`5idpqc − 3idpqc`（窗口对调，检验「换几何能否翻号」）+ T6 一阶差分（`ts_delta(qpdi3_gross_margin,66)`，新矩阶）。

