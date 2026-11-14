# F72 探针结论：fundamental72 在 DEU 数据稀疏、信号为负（2026-11-11 23:19）

## 一、三次探针的排查过程

| 次 | 表达式 | 结果 | 判定 |
|---|---|---|---|
| 1 | 裸字段（无 vec 包裹） | 2/2 ERROR | 字段类型不兼容 |
| 2 | 裸字段重试 | 2/2 ERROR | 排除平台瞬断，确认类型问题 |
| 3 | `vec_avg()` 包裹 | **2/2 成功** | 确认是 VECTOR 类型 |

## 二、第三次（正确写法）的结果

| alpha | 字段 | S | F | TO | longCount | R | 2Y |
|---|---|---:|---:|---:|---:|---:|---:|
| KPgKMpWj | accounts_payable_trade_amt | **-0.56** | -0.31 | 0.0559 | **68** | -0.0394 | -0.67 |
| XgajAxd1 | accumulated_depreciation_value | **-0.61** | -0.42 | 0.0966 | **26** | -0.0582 | 1.30 |

## 三、判定：fundamental72 不可用

两个致命问题：
1. **数据极度稀疏**：longCount 仅 68 / **26**，而满覆盖组合件是 149-160（TOP500 的 30-53%）；
2. **信号为负**：S -0.56 / -0.61，R 为负，说明这个骨架下这些字段在 DEU 无预测力。

## 四、由此确立的规律：fundamental 的 coverage=0 该如何解读

| 数据集 | 平台 coverage | 实测 longCount | 实测 S 天花板 | 判定 |
|---|---:|---:|---:|---|
| **fundamental6** | 0.4923 | 正常（~150+） | **1.73**（oiadpq 单点） | ✅ 可用 |
| fundamental89 | 0.0 | 78-94 | 0.69 | ❌ 弱 |
| **fundamental72** | 0.0 | **26-68** | **-0.56** | ❌ **不可用** |
| fundamental17 | 0.0 | 未测 | 未测 | ⚠ 推测同 89/72，数据稀疏 |

**结论**：
1. **只有 fundamental6（coverage 0.49 非零）在 DEU 有实数据**；三个 coverage=0 的 fundamental 集数据都稀疏；
2. **coverage=0 基本等价于「该区域数据缺失」**，不是面板口径问题——先前我把 fundamental89 的 coverage=0 解读为「口径不可信」是过度纠正；
3. 正确判据仍是 **longCount**：< 100 即视为数据不足以支撑交付件。

## 五、DEU D1 数据集面全部走完

本战役已实测/审计的数据集：**32 个**，其中：

| 类别 | 数量 | 代表 |
|---|---:|---|
| **有效（出过交付件）** | **4** | shortinterest3、analyst/anl93、insiders1（第二腿）、other47（第二腿） |
| 单点有效 | 1 | fundamental6（仅 `fnd6_newq_oiadpq`） |
| 弱（S 1.0-1.5，结构可用但强度不足） | 6 | nws20/loan_rate_volatility/rsk60/inst25/其他 news 族 |
| 死（S < 1.0 或信号为负或数据稀疏） | 21 | opt1 族、fundamental72/89、pv29/30、ern6、socialmedia12 等 |

⇒ **DEU D1 的可用信号面已全部探明**，剩余未被证否的只有 fundamental17（135 字段）与 oth384（电话会），
但按 89/72 的模式推断其 coverage=0 同样数据稀疏，预期收益极低。