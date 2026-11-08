# S0 · KOR × Insiders 数据集全扫描

> 口径：`get_datasets(region=KOR, universe=TOP600, delay=1, category=insiders)`，2026-11-06。

## 1. 全集（只有 2 个）

| 数据集 | 名称 | cov | 字段数 | userCount | alphaCount | 乘数 | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| `insiders5` | Corporate Insider Trading Activities（韩国内部人申报明细） | 0.8918 | 53 | 820 | 5027 | 1.2 | ✅ **主攻** |
| `insiders1` | Global Insider Trading Data（Compustat Global 口径） | 0.3526 | 9 | 202 | 549 | 1.2 | ⚠ **备选**（无方向码 + 覆盖 .35） |

## 2. 候选裁定

### insiders5 —— 主攻
- **字段结构完整**：交易流量（有符号）+ 持仓快照 + 库藏股 + 标识，四族齐全。
- **覆盖可接受**：快照组 .9996 / 库藏股组 .8728 / 交易组 .7318。
- **已有全闸实证**：分歧度族两颗（S 1.62 / 1.76，failed_ra 0）。
- **拥挤度分层清晰**：`source_data` aC 744（拥挤）/ `ghc_tr` aC 220（中）/ `unt_val` aC 45（白）。

### insiders1 —— 备选降级
- 9 字段**全 VECTOR**，且**无买卖方向码**（无 acquired/disposed），只能用 `holdings` 差分代理方向 ⇒ 代理噪声大。
- cov **.3526** ⇒ 2/3 股票无读数，横截面排序在噪声上排序（论坛实证：cov<0.7 字段直接不用）。
- 与 insiders5 同塔同机制、且更弱 ⇒ **留作最后手段**，本轮不派主力波。

## 2b. 检索补漏（`get_datasets(search="insider")`，2026-11-06）

Insiders **类别**下只有 2 个数据集；但按关键词检索还能捞到 3 个「内部人题材但归类在其它 category」的集：

| 数据集 | category | 字段 | cov | aC | 说明 | 处置 |
|---|---|---:|---:|---:|---|---|
| `insider_feats` | **other** | 31 | .6636 | 2058 | Global Insider Transaction Features（`buy_sell_ratio_*` 族，论坛帖 S 1.94/AMR 用的就是这个） | ⚠ **备用**：属 OTHER 塔，点亮的是 OTHER 不是 INSIDERS；且 aC 2058 已被大量使用 |
| `model244` | **model** | 30 | .4589 | **17** | Insider Transaction Analytics | ⚠ 备用（MODEL 塔）；aC 极低=白，但 cov .46 |
| `other83` | **model** | 15 | .375 | 171 | Insider Transaction Analytics（另一厂商口径） | ⚠ 备用（MODEL 塔） |

**裁定**：本轮**不启用**——用户明确要求「Insiders 下」，且这三个属 OTHER/MODEL 塔（点亮后不计入 INSIDERS）。
仅在 insiders1/insiders5 完全榨干（10 颗交不出）时启用，并在波次台账写明切换理由（约束：「确实无计可施时才换」）。

## 3. 用户约束映射

| 约束 | 落地 |
|---|---|
| region 固定 KOR | 全部仿真 `region=KOR` |
| 不频繁换数据集 | 主攻 insiders5 到底；insiders1 仅在其后 |
| 近十年都有数据 | 每颗候选交付前跑 `get_alpha_yearly_stats`，逐年 longCount>0 且 pnl≠0；连续空窗即弃 |
| 并发 ≤2 | 每轮最多 2 个 multisim 在飞 |
| 禁混腿 | ATOM ⇒ 表达式只含单数据集字段 |
| 算子 ≤12 | 全部候选算子数 ≤12，目标 ≤8 |
