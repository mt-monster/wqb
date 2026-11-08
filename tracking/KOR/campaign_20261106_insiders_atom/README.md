# KOR × INSIDERS × ATOM 战役（2026-11-06 起）

> **目标**：KOR / TOP600 / Delay=1，从 **Insiders 类数据集**产出 **10 个 ATOM（单数据集）REGULAR alpha**。
> **用户约束**：① region 固定 KOR；② 不频繁换数据集；③ 阻塞时查论坛/论文；④ 覆盖可动态调整但**近十年都要有数据**；
> ⑤ 开波并发 `create_multi_simulation` **限 2**；⑥ 能用 MCP 不写临时脚本；⑦ prod 必须用 MCP 查；
> ⑧ 禁 PV/MODEL/OTHER/FUNDAMENTAL 内部两两组腿（可与非禁混类组腿但总量 ≤5）；⑨ 算子数 ≤12、越少越好。
> **ATOM 定义**：表达式只消费一个数据集的字段（本战役 = insiders5 或 insiders1），天然满足约束 ⑧。
> **设置档**：KOR / TOP600 / Delay=1 / **REVERSION_AND_MOMENTUM** / decay 4 / trunc 0.08 / unit VERIFY / nanHandling OFF / pasteurization ON / maxTrade OFF
> （decay 与中性化按波次分档对照，理由见 waves.md）

## 文档索引

| 文件 | 内容 |
|---|---|
| [s0_dataset_scan.md](s0_dataset_scan.md) | **S0**：Insiders 类全量数据集扫描（2 个）+ 候选裁定 + 用户约束映射 |
| [s1_field_profile_insiders5.md](s1_field_profile_insiders5.md) | **S1**：insiders5 **53/53 字段画像**（类型 / 覆盖 / 频率 / 分布 / 可用性）+ 五问 + 机制 A-2 |
| [s1_field_profile_insiders1.md](s1_field_profile_insiders1.md) | **S1**：insiders1 **9/9 字段画像** + 结构性缺陷裁定 |
| [waves.md](waves.md) | **S3/S4 波次台账**：设计 / 读数 / 归因 / 准入禁碰 |
| [final_report.md](final_report.md) | **交付**：10 颗 ATOM 清单（数据集 / 核心字段 / 算子逻辑 / 指标 / 画像索引） |

## 入场状态（S-PRE）

| 项 | 值 |
|---|---|
| 金字塔 | `KOR/D1/INSIDERS` **0/3 未点亮**，乘数 **1.2** |
| 数据集 | 仅 **2 个**：`insiders5`（53 字段，cov .892，aC 5027）/ `insiders1`（9 字段，cov .353，aC 549） |
| 既有候选 | `kqNv1xRk` S 1.62 / 2Y 2.23 / fails 0；`RRE9NkVj` S 1.76 / 2Y 2.77 / fails 0（均 insiders5 分歧度族） |
| 起点 | 已有 **2 颗全闸**，本战役需补 **8 颗** |
## 结算（2026-11-06 收波）

| 项 | 结果 |
|---|---|
| 交付 | **10 个 ATOM 型 REGULAR alpha**，全部 `insiders5`，`failed_ra_count=0` / S≥1.58 / 2Y≥1.58 / 十年逐年有数据 / self<0.7 |
| 报告 | [final_report.md](final_report.md)（数据集 / 核心字段 / 算子逻辑 / 指标 / 画像索引 / 相关性与失效风险） |
| 机制 | 唯一出货轴 = M1 分歧度截面水平；倒数几何是同轴的单调重参数化，非独立第二轴 |
| 限制 | 10 颗为同族参数邻域，互相关 0.90–1.0 ⇒ 按 0.7 线最多同时提交 2 颗；**族代表 `3qokqkZQ` prod 实测 0.8495（>0.70 红线、>0.80 整族封盘）⇒ 10 颗均不可提交**（22:40 MCP `check_correlation` 零成本读回并 `persist_correlation` 落库，详见 final_report.md §5.3） |
| 备选集 | `insiders1` 作为「最后手段」已用尽（W11 取负臂 6/6 全灭），不贡献交付件 |
| 去重 | Wave12 winsorize 幂等 4 颗 + Wave13 退化等价件 `O0AMYMXg` 全部排除，不凑数 |
| 算子数 | 每条 4–7 个，均 ≤12 |
