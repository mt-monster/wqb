# BE122 判决：market 外层突破 1.2（S 1.24 / F 0.92 / sub 0.61）（2026-11-11）

## 十臂结果

| # | 变体 | S | F | TO | 2Y | sub | lc/sc |
|---|---|---:|---:|---:|---:|---:|---|
| **6** | **market 外层中性化** | **1.24** | **0.92** | 5.8% | 1.32 | **0.61** | 110/155 |
| 1 | 簇中性基线（复现） | 1.11 | 0.77 | 6.8% | 1.49 | 0.35 | 116/155 |
| 2 | ts_ir 双窗（+ir110） | 1.08 | 0.76 | 6.4% | 1.40 | 0.37 | 116/157 |
| 3 | Top2 份额替代 Top1 | 1.07 | 0.74 | 6.8% | **1.50** | 0.41 | 115/156 |
| 8 | subindustry 外层 | 1.05 | 0.69 | 5.2% | 1.47 | 0.61 | 109/153 |
| 10 | 纯 group_rank 外层 | 1.03 | 0.67 | 5.2% | **1.51** | 0.43 | 122/143 |
| 5 | TopGap 替代 HHI | 1.01 | 0.69 | 7.2% | 1.31 | 0.29 | 108/154 |
| 3 | valueeur 信噪比 | 0.91 | 0.55 | 7.0% | 1.17 | 0.24 | 119/153 |
| 8 | HHI 门控 | 0.40 | 0.20 | 4.5% | 0.71 | 0.14 | 87/101 |
| 9 | ts_ir 门控 | 0.12 | 0.03 | 4.7% | −0.36 | −0.43 | 58/61 |

## 关键突破：外层中性化阶梯

| 外层 | S | F | sub |
|---|---:|---:|---:|
| 无（纯 group_rank） | 1.03 | 0.67 | 0.43 |
| subindustry | 1.05 | 0.69 | 0.61 |
| **sector（簇中性，G=group50_top800）** | 1.11 | 0.77 | 0.35 |
| **market** | **1.24** | **0.92** | **0.61** |

**机理**：三腿信号都是**个股级**（内部人交易是公司特定事件，与行业无关）。簇中性/行业中性会**剥离掉共同成分**（大市值公司内部人交易更活跃的规模效应），而 market 中性只剥离市场整体，保留更多个股alpha ⇒ S +0.13、F +0.15、sub +0.26。

**门控全灭**（HHI 门控 0.40 / ts_ir 门控 0.12）：把持仓压到 87/101 与 58/61，横截面太窄 ⇒ 与之前 trade_when 失败的规律一致。

## 胜出臂完整表达式（wpoqXXMx）

```
group_zscore(add(add(
  group_rank(ts_delta(ts_mean(vec_avg(insd1_holdings),66),66), sector),
  group_rank(ts_ir(vec_avg(insd1_holdings),66), sector)),
  group_rank(ts_mean(divide(significant_value_1,
    add(add(significant_value_1,significant_value_2),add(significant_value_3,significant_value_4))),66), sector)),
market)
```
设置：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nan ON

| 指标 | 值 | 闸 |
|---|---:|---|
| S | **1.24** | 1.58 ❌ 差 0.34 |
| F | **0.92** | 1.0 ❌ 差 0.08 |
| TO | 5.8% | ✓ |
| 2Y | 1.32 | 1.58 ❌ 差 0.26 |
| sub | **0.61** | ✓（要求 0.474×S=0.59） |
| investability S | 1.19 | — |

## 判定：≥1.2 触发继续冲（BE123 已派发）

**BE123（4ak4zu8j54C9nNy10Zlv，10 臂）**以 market 外层为核心做五维扩展：
1. 基线复现（market 外层）
2. market + ts_ir 双窗（第四腿 ir110）
3. market + Top2 份额替代 Top1（2Y 打法）
4. **嵌套双层中性化**（sector 内 → market 外）
5. market + ts_ir 窗换 44
6. market + Δ 窗换 110（与 ir 一致）
7. market + 冠军腿型（三腿全 tail+winsorize）
8. market + valueeur 信噪比
9. market 基线（设置档对照）
10. market + 仓位占比第四腿

**判读线**：≥1.4 ⇒ 定向补（窗/腿组合）；1.24-1.4 ⇒ 边际，记录最优；<1.24 ⇒ market 外层已达最优，INSIDERS 定型 1.24。
