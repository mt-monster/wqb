# 战略转向：从 insiders 核心转向非 insiders 核心（补最后 3 颗）

日期：2026-11-12

## 一、为什么必须转

| 事实 | 数据 |
|---|---|
| insiders 数据集可交付上限 | **17 颗**（互相关<0.7 的最大独立集，已验证加入更多候选仍是 17）|
| 已探尽的信息维 | holdings 存量变化 + SV1 集中度（其余 10+ 维度全部判死）|
| 有效搭档族 | 仅 4 个（analyst-MODEL / analyst7-ANALYST / other455-OTHER / news104-NEWS）|
| 缺口 | **3 颗** |

⇒ insiders 核心与搭档族的组合空间已穷尽，继续在 insiders 内部投入的边际收益趋近 0。

## 二、转向依据（Goal 自带授权）

Goal 第 1 步原文：**「数据集全面扫描：针对当前 deu region 下的数据集逐一扫描，评估其潜力并筛选出候选数据集」**

⇒ 扫描 DEU 全部数据集是 Goal 明确要求的动作，不是越界。
⇒ 「不得换 region」的约束是区域锁定，不是数据集锁定。

## 三、合规性（关键）

非 insiders 组合的合规性反而**更宽松**，因为可选的非 trio 类别更多：

| 组合 | trio 成员数 | 合规 |
|---|---:|---|
| ANALYST + OTHER | 1（OTHER）| ✅ |
| ANALYST + NEWS | 0 | ✅ |
| ANALYST + SHORTINTEREST | 0 | ✅ |
| ANALYST + SENTIMENT | 0 | ✅ |
| ANALYST + INSTITUTIONS | 0 | ✅ |
| OTHER + NEWS | 1（OTHER）| ✅ |
| OTHER + SHORTINTEREST | 1（OTHER）| ✅ |
| OTHER + INSTITUTIONS | 1（OTHER）| ✅ |
| NEWS + INSTITUTIONS | 0 | ✅ |
| ❌ PV + MODEL / PV + OTHER / MODEL + OTHER | 2 | **违规** |

⇒ 只要**避开 PV/MODEL/OTHER 的两两组合**，其余任意搭配都合规。
⇒ 非 insiders 的核心天然与现有 17 颗（8 颗含 INSIDERS 塔）低相关。

## 四、两波设计

**BE169**（`4AvBRBaei4Tgb13HdvhF1bF`，10 臂）— analyst7 作核心

| 臂 | 构造 | trio |
|---|---|---|
| Z1-Z3 | 调用广度 / 净上调比 / 评级净上调 × OTHER(O4) | 1 |
| Z4-Z5 | 调用广度 / 净上调比 × NEWS | 0 |
| Z6-Z7 | 调用广度 / 净上调比 × SHORTINTEREST | 0 |
| Z8-Z10 | 双 analyst 腿 × OTHER / NEWS | 1 / 0 |

**BE170**（`v9wObdFp4JC9q2jcRyDW7u`，10 臂）— OTHER / NEWS 作核心

| 臂 | 构造 | trio |
|---|---|---|
| Y1-Y4 | O4 / O1 × NEWS 变体 | 1 |
| Y3 | O4 × analyst | 1 |
| Y5-Y7 | O4 × SHORT / SENTIMENT / INSTITUTIONS | 1 |
| Y8-Y9 | NEWS × INSTITUTIONS / SHORT | 0 |
| Y10 | O4 + NEWS + SHORT 三腿 | 1 |

## 五、预期

这两波完全不含 insd1_* / significant_value_* 字段 ⇒ PnL 驱动因子与现有 17 颗无关
⇒ **预期互相关很低（可能 <0.3），天然满足入篮条件**。

关键不确定性是**能否独立过 S 1.58 闸**。历史经验：单数据集因子很少单独过闸，
需要 2-3 腿组合。所以每波都配了单腿与多腿版本。