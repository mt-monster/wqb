# 判死：analyst7（ANALYST 类）不能作主核心，只能作辅助腿

日期：2026-11-12
BE169 multisim 4AvBRBaei4Tgb13HdvhF1bF（10 臂，完全不含 insiders 字段）

## 实测全灭

| 臂 | 构造 | alpha | S | F | 2Y | sub | fail |
|---|---|---|---:|---:|---:|---:|---:|
| Z2 | 净上调比 + OTHER | kqadWd2P | **1.29** | 1.01 | 1.14 | **1.27** | 2 |
| Z1 | 上调广度 + OTHER | 1YWeleQk | 1.03 | 0.72 | 1.28 | **1.29** | 3 |
| Z8 | 双 analyst + OTHER | 1YWele5m | 0.96 | 0.67 | 0.57 | **1.36** | 3 |
| Z3 | 评级净上调 + OTHER | mLap0pM1 | 0.86 | 0.55 | 0.83 | 0.85 | 3 |
| Z5 | 净上调比 + NEWS | P05NYN9q | 0.73 | 0.44 | −0.20 | 1.05 | 3 |
| Z9 | 双 analyst + OTHER | Jj8qWqLe | 0.69 | 0.41 | 0.40 | 1.16 | 3 |
| Z10 | 双 analyst + NEWS | vRA8p803 | 0.65 | 0.39 | −0.12 | 1.18 | 3 |
| Z4 | 上调广度 + NEWS | 9qlYdY0q | 0.52 | 0.27 | −0.14 | 1.01 | 3 |
| Z7 | 净上调比 + SHORT | d5ap3pLJ | −0.01 | 0.00 | −1.32 | 0.39 | 3 |
| Z6 | 上调广度 + SHORT | wpoq2qgY | **−0.17** | −0.05 | −1.17 | 0.43 | 3 |

**最高 1.29，10/10 fail≥2。**

## 判死结论

**analyst7（ANALYST 类）字段不能作主核心，只能作辅助腿。**

### 证据链（跨波次一致）

| 用法 | 读数 | 结论 |
|---|---|---|
| analyst7 单腿 | S 0.39-0.68（BE145）| 自身无 alpha |
| **analyst7 作核心 + 非 insiders 搭档** | **S 0.52-1.29（本波）** | ❌ 不能作核心 |
| analyst7 作辅助腿 + insiders 核心 | S 1.62-2.14（BE145/BE158）| ✅ 有效 |
| **predictive_starmine 作辅助腿（AS3+AS4）** | **S 2.20**（leadEXnl）| ✅ **最强辅助腿** |

### 机理

analyst7 的「上调/下调分析师数量」是**广度计数**，区分度低（多数股票同期为零或小数）；
而 predictive_starmine 的 `mean_estimate_change_pct` 是**修正幅度百分比**，连续且有量级信息。

⇒ **analyst 族内部分层明确：幅度类 ≫ 广度类。**
⇒ 广度类（analyst7）只适合当「确认信号」叠加在强核心上，不能自己当核心。

## 附带判死

| 搭档 | 与 analyst7 核心配合 | 结论 |
|---|---|---|
| OTHER（other455 关系PC2）| 0.86-1.29 | 相对最好但仍不够 |
| NEWS（news104 情绪×相关度）| 0.52-0.73 | ❌ |
| SHORTINTEREST（shrt3_bar）| −0.17 ~ −0.01 | ❌ 负 |

## 对补缺的启示

**非 insiders 核心这条路走不通**——至少在「analyst7 + 单一搭档」这个形态上是。
剩下的非 insiders 核心候选（OTHER / NEWS / 机构）需要更强的组合，
或者放弃「纯非 insiders」而采用「**其他数据集核心 + analyst 幅度腿**」（即把 predictive_starmine 当辅助）。