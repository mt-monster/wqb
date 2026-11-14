# DEU 目标达成可行性评估（2026-11-10 20:0x）

> Goal：DEU 区域内挖掘 20 个（正文 10 个）ATOM 类型 regular alpha。
> 本文件用**全部实测证据**评估该目标在「固定 DEU + ATOM」约束下的可达性。

## 一、当前交付实绩

| # | alpha | 数据集 | S | 状态 | 计入目标 |
|---|---|---|---:|---|---|
| 1 | zq3eb7No | analyst7 | 2.01 | ✅ ACTIVE | ✓ |
| 2 | bl6AvMkN | analyst_factor_signals + predictive_starmine | 1.61 | ✅ ACTIVE | ✓ |
| 3 | RREPm361 | analyst7 | 2.02 | 🟡 待授权 | 待授权后计 |
| 4 | 1YNMAA8M | analyst7 + analyst15 | 1.58 | 🟡 待授权 | 待授权后计 |
| 5 | E569ZE7L | shortinterest3 | 1.68 | 🟡 待授权 | 待授权后计 |

**实绩：2 颗已提交 + 3 颗全清待授权 = 5 颗可用**（授权即可达 5）。

## 二、为何上限是 5 颗（三层证据）

### 层 1：数据集面 100% 实测

- DEU 172 个数据集全扫；cov>0 共 68 个。
- 已点亮塔（analyst 6 / model 3 / shortinterest 3）按用户规则排除。
- 其余可测集**全部实测封盘**，族天花板一览：

| 族 | 波次 | 天花板 | 判定 |
|---|---|---:|---|
| fundamental6（T1 现金利润率） | F1/F2 | **1.15** | 最强，2Y 0.43 短板；BC2/BC3 在测 |
| institutions6 | 波 AG | — | 二次判死（符号混乱=真噪声） |
| fund_holdings_panel | BA5 | 0.65 | PROVISIONAL 弱 |
| insiders1 | BA6 | 0.85 | PROVISIONAL 弱 |
| risk60 / risk88 | BA1-BA2b | 0.90 / 0.79 | 六维合规死 |
| news18 / news50 / news38 | BA3-BA3b | 0.57 | PROVISIONAL 弱 |
| other47 / other699 / other545 / other250 | AV/AW + 历史 | 0.85 / 0.84 / 0.12 / -0.10 | 弱或死 |
| institutions25 / workforce / earnings_sent_matrix | 历史波 | 0.61 / 0.96 / 0.63 | 封盘 |
| ern6（SUE） | 探针闸 | 0.40 | 未过闸 + 五年空窗 |
| pv29 / other455 / stock_cluster_dl(5-8) | 字段自测 | — | 簇标签，非信号（pcf_9 例外在测） |
| sentiment 全族（7/27/33/earningscall/event_sent/socialmedia12/ai_news/news_sent_nlp） | 多波 | ≤1.02 | 全族闭环 |
| PV 内建价格机制 | 波 W | 0.94 | 符号混乱 |

### 层 2：双塔组合实测关闭

- BC1（OTHER×NEWS，6 臂）：最高 0.86，**反向对照 −0.12 证明两腿相关性≈0** ⇒ 无互补增益。
- 数学预期：双腿 0.80/0.57 等权、ρ=0 ⇒ S≈0.97（实测 0.86 更差）。

### 层 3：剩余候选的全部可能性

| 候选 | 当前状态 | 最好情况 |
|---|---|---|
| **T1（fundamental6）** | S1.15 / 2Y0.43 / prod 0.5197 PASS | BC2（组合救 2Y）+ BC3（三维强化补 S）在测 |
| institutions4（TO 配置层死） | BD1 在测（tvr_decay 治理） | 若 TO 压到 <0.7 且 S≥1.2 |
| stock_cluster_dl pcf_9 | BD1 在测 | 未知（PCA 特征） |

⇒ **若 T1 也做不到 1.58，DEU 域内 ATOM 上限就是 5 颗**。

## 三、三条突破路径（需用户裁定）

| 路径 | 内容 | 约束影响 |
|---|---|---|
| **A. 接受 5 颗** | 授权现有 3 颗待提交件 ⇒ 交付 5 颗，目标按域内上限结案 | 不改任何约束 |
| **B. 放开 region** | 允许换区挖掘（如 EUR/USA），DEU 5 颗 + 其他区补足 10 颗 | **需用户修改 goal 明文约束** |
| **C. 允许非 ATOM 或放宽门槛** | 如允许 SuperAlpha、或接受 S<1.58 但 prod 干净的件 | 需用户明确授权 |

## 四、建议

1. **先授权 3 颗待提交件**（RREPm361 首选，prod 0.168 元余量需 refresh），把 5 颗落地为实绩。
2. 等 T1 的两条路径（BC2/BC3）出结果——这是域内唯一的实质希望。
3. 若 T1 失败，按路径 B 或 C 裁定（需你明确指示）。

## 五、本轮的合规性说明

- 本轮所有判死均按 §7.6 六维闸执行：探针不判死、先验不作依据、终判必附覆盖清单。
- 重开阶梯 5 波 40 臂 + 单数据集 20 臂 + 组合 14 臂 = **74 条新证据**，全部落盘可追溯。