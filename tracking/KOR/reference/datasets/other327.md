# other327 · KOR / TOP600 / D1 字段画像

> 类型 MATRIX · **3 字段** · cov 0.7778–0.791 · get_datafields(filter_sharpe=false) 2026-11-08 complete=true
> category = **other**（未点亮塔）· 名 Sensitivity to Interest Rates Model
> 派发审计：`oth327_sirc/oth327_mktcap` 在 _args 零命中 ⇒ 本战役 IR327 波首次实测（§5.114 曾标"未挖高潜力"）

## 0. 全字段清单（3/3，αC 降序）
| # | 字段 | αC | cov | desc |
|---|---|---|---|---|
| 1 | `oth327_mktcap` | 17 | .7778 | 市值（USD），只作规模轴 |
| 2 | `oth327_sirc_lev` | 14 | .791 | 对**美债收益率曲线平行（level）移动**的敏感度数值 |
| 3 | `oth327_sirc_sl` | **2** | .791 | 对**收益率曲线斜率（twist/steepening/flattening）变化**的敏感度数值 |

## 1. 名 vs description 差异
- `sirc_lev` = 利率**水平**久期暴露（类债券 duration），不是杠杆/level 水平因子；
- `sirc_sl` = 曲线**斜率**敏感度，aC2 极冷。

## 2. 五问
1 存量敏感度（beta 型暴露，非流量）；2 排序 ⇒ group_rank(sector)；3 强度（利率久期）；4 极冷 aC2–14；5 非事件，cov.79 ⇒ ts_backfill(10)。

## 3. 预处理
- cov .79 → ts_backfill(10)；mktcap 只作规模轴（vector_neut）。
- ⚠ 静态敏感度是**风险暴露**，level 可能是特征非信号（acquisition §5.23 先例）⇒ level/change/zscore 多几何并测，方向正反各测（铁律 B）。

## 4. 机制（A-2）
- **谁被定价**：对个股利率久期暴露定价不足的投资者；
- **为什么错**：D.E. Shaw《Divergent Interests》——个股/行业/风格利率敏感度近年显著分化，不再是单一股债相关，组合相对历史出现非预期表现 ⇒ 截面利率敏感度分化产生可交易错价；
- **修复期**：利率 regime 切换数周–数季（66/252）；
- **方向**：regime 依赖（降息高久期受益 / 加息受损）⇒ 正反实测；
- **Boundary**：KOR 利率 regime 与美债联动弱则无截面预测力；静态暴露可能只是风险溢价非 alpha。

## 5. IR327 波模板（10 结构互异，RAM/d4/trunc0.08）
lev/sl 水平正·反 · lev Δ66 · lev zscore252 · lev mean66 · lev 规模残差 · sl Δ66 · lev power2
multisim `Wym2Bbnz4YZbuFbBIHB6BB`（2026-11-08 派发，在飞）

## 6. 实测记录（IR327 收割 2026-11-08，10/10 COMPLETE，RAM/d4/trunc0.08）

| 臂 | alpha | S | F | 2Y | raF |
|---|---|---:|---:|---:|---:|
| **lev mean66** | A1V8qNnl | **0.75** | 0.45 | 1.21 | 3 |
| lev 水平 | xArpX3Pn | 0.65 | 0.37 | 1.04 | 3 |
| sl 水平 | QPvpmb2g | 0.56 | 0.30 | 0.61 | 3 |
| lev 反向 | E56PopgR | −0.84 | −0.53 | −1.41 | 5 |
| sl 反向 | WjO2KbNj | −0.76 | −0.47 | −0.99 | 5 |

**判定：弱死**（天花板 S≈0.75，缺口 0.83；正向确证）。利率敏感度是**风险暴露非可交易 alpha**（§5.23「level=特征非信号」同型）；KOR 与美债利率 regime 联动弱，截面预测力不足。封盘。
