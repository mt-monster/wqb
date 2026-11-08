# GLB 容量重算 + 点塔路线图（2026-11-04）

## 一句话结论

**GLB 当前真实可提交上限 = 9 颗（`exact=True`），prod 是唯一真瓶颈（10.3% 通过率）；9 颗已全部完成四审 + 覆盖核查，但因提交授权 8 次请示全部 `automatic_timeout`，尚未提交任何一颗。**

---

## 1. 推翻「合规上限 11 颗」

此前 cap=11 的根因是 **fRA 只审计过 19 颗**，拿其中 16 颗解最大团。本轮把 fRA 审计扩到全池 349 颗后：

| 分类 | 数量 |
|---|---:|
| 指标达标未提交 | 349 |
| 合规 + fRA=0 + 无禁用分组轴 | **177** |
| ├ 纯单塔（零配额） | 102 |
| ├ trio × 非 trio | 71 |
| └ 非 trio × 非 trio（零配额） | 12 |

互相关也不是瓶颈：100 颗池最大团 **28**、合并 39 颗得 **37**（`exact=False`，仅下界）⇒ 「cap=11」是「池子小」被误读成「机制饱和」。

## 2. 真瓶颈：prod

177 颗合规候选的 prod 分布：**<0.70 仅 13 颗 / ≥0.70 有 114 颗 / 未测 50 颗**。

13 颗 prod 通过件的精确最大团 = **9 颗**（`exact=True`），6 对冲突：

```
9qxR097o / N1NO9nRe   0.9864
xArnqeAw / Xg9rMdvl   0.8526
YP1rzw2J / RRE3O8r1   0.8503
npv9WLVE / qML1x6vK   0.8065
j2Yg2q9j / Xg9rMdvl   0.7815
YP1rzw2J / d5WqeQbx   0.7435
```

## 3. 9 颗的完整核验（提交前四审全过）

| alpha | S | 2Y | TO | prod | 组合 | 逐年覆盖 |
|---|---:|---:|---:|---:|---|---|
| npv9WLVE | 3.08 | 3.19 | 60.8% | 0.6638 | RISK+OTHER | 2015-2023（2014 空） |
| 9qxR097o | 2.56 | 2.72 | 9.6% | 0.6502 | EARNINGS+OTHER | 2014-2023 满 |
| leA0X7lA | 3.41 | 2.72 | 14.4% | 0.6022 | FUNDAMENTAL+OTHER | 2014-2023 满 |
| QPvJ6KVw | 3.19 | 3.43 | 29.0% | 0.6385 | RISK+OTHER | 2015-2023（2014 空） |
| RRE3O8r1 | 2.89 | 2.13 | 16.0% | 0.6479 | FUNDAMENTAL+OTHER | 2014-2023 满 |
| xArnqeAw | 2.74 | 2.36 | 21.2% | 0.6335 | SENTIMENT+OTHER | 2014-2023 满 |
| j2Yg2q9j | 2.73 | 2.85 | 14.7% | 0.6585 | SENTIMENT+OTHER | 2014-2023 满 |
| d5WqeQbx | 2.71 | 2.68 | 7.5% | 0.5846 | FUNDAMENTAL+OTHER | 2014-2023 满 |
| bl6qldJ6 | 2.59 | 2.02 | 35.3% | **0.5421** | SENTIMENT+OTHER | 2014-2023 满 |

- `submit_verdict` 9/9：`failed_any=0`、`sim_fails=[]`、`hard_gate_warnings=[]`；verdict 为 `UNVERIFIABLE_404` 仅因平台 `GET /submit` 是死端点，非缺陷。
- 塔归属 12 个字段逐一核验：信号腿全为 `dl_riskfree_returns`(OTHER) 或 `techindi_model`(OTHER)，门控腿 `risk60`/`earnings3`/`fundamental23`/`fundamental44`/`sentiment21` ⇒ **trio × 非 trio，合规**，用 4 种组合类型。
- 覆盖：7/9 在 2014-2023 逐年 `longCount>0 && pnl≠0`；2 颗仅 2014 单点空窗（risk60 数据起于 2015）。**不是连续空窗，通过。**
- `d5WqeQbx` 2020 年 pnl = −178,869，是唯一下跌年，不构成覆盖问题。

## 4. ★ 本轮新发现：互相关由 gate 决定，不是 signal 腿

`w194` 破墙波产出 `ZYQE3OW0`（ern3 门 + 60day 腿）：S 2.09 / F 1.13 / 2Y 2.70 / TO 9.3% / **prod 0.6966 通过**。
但它与 `9qxR097o` 的互相关是 **0.9643** ⇒ 同一 PnL 家族克隆，最大团仍 9 颗。

| 变更 | 互相关 |
|---|---:|
| 同 gate，换 signal 腿（20day→60day） | **0.9643** |
| 同 signal 腿（20day），换 gate（fund23 / ern3 / rsk60） | **<0.7** |

⇒ 想在同一组合类型里补第 2/3 颗，**必须换 gate 字段本身**；换窗口、换信号腿都救不了。这直接否定了 w194 的设计假设（6 个变体全用 `ern3_pre_reptime`）。

## 5. ★ 到 20 颗的可行路线图

规则算术：每两塔组合 ≤3 颗、组合类型 ≤5 种、纯单塔零配额。

| 组合类型 | 现有 | 上限 | 缺口 |
|---|---:|---:|---:|
| SENTIMENT+OTHER | 3 | 3 | 0（封盘） |
| FUNDAMENTAL+OTHER | 3 | 3 | 0（封盘） |
| RISK+OTHER | 2 | 3 | **1** |
| EARNINGS+OTHER | 1 | 3 | **2** |
| ANALYST+OTHER | 0 | 3 | **3** |
| **组合类合计** | **9** | **15** | **6** |

再加 **5 颗纯 OTHER 单塔**（零配额）= **20**。

纯 OTHER 来源（唯一未测正交集）：
- `other455`：300 个 MATRIX，供应链/竞争/伙伴网络的 Node2Vec+PCA 嵌入，cov 0.83–0.97，**全未测**
- `other496`：400 个 MATRIX，含 FF 因子与 beta-to-index，可用字段 cov 1.0，全未测

## 6. 门控字段容量（决定某类别能贡献几颗）

| 类别数据集 | 字段数 | 可作门控的语义互异字段 | 实际容量 |
|---|---:|---|---|
| `sentiment21` | 210 | 多 | 高（但配额已满 3/3） |
| `fundamental23` | 500 | 多 | 高（已满 3/3） |
| `fundamental44` | 12 | `score`/`yoon_wc_accruals`/`factor_benford` 等 | 中（已满 3/3） |
| `analyst10` | 174（97 MATRIX，cov 0.95） | 共识/意外/覆盖度/毛利率四大族 | **高（0/3，主战场）** |
| `risk60` | **5** | `offer`/`lending_fee_bid_rate`/`last` | 低（最多 1-2 颗） |
| `earnings3` | **8**（`_interval` 全 DEAD，只剩 `_reptime` 系） | `pre_reptime`/`next_reptime` | **低（1-2 颗，已用 `pre_reptime`）** |

## 7. 本轮在飞波次

| 波次 | 内容 | 状态 |
|---|---|---|
| w194 | 6 变体破 `d5W0RQZv` 0.7023（EARNINGS 第 2 颗） | 2 完成 / 2 在飞 / 2 未发 |
| w195 | 14 模板 ANALYST+OTHER（新类型，乘数 1.4） | 在飞（1/14 完成） |
| w196 | 12 模板 other455 纯 OTHER 单塔（零配额，已校验待发） | 待发 |
| w197 | 7 模板换 gate 字段填 RISK+1 / EARNINGS+2 | 在飞 |

w194 已完成件：

| tag | alpha | S | F | 2Y | TO | prod | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| T1 闸22+60day腿 | `ZYQE3OW0` | 2.09 | 1.13 | 2.70 | 9.3% | **0.6966** | 指标+prod 全过，但与 9qxR097o 0.9643 克隆 ⇒ 不可入团 |
| T2 闸22+5day时序平滑 | `VkxGjzPM` | 2.25 | 1.30 | 2.60 | 8.7% | 0.7138 | 单钉（n=1）未破 |

⇒ **EARNINGS 门族（gate 固定为 `ern3_pre_reptime`）在 prod 0.70–0.72 一带已饱和**，换腿无效（0.7023→0.7138），必须换 gate 字段（w197 的 `ern3_next_reptime`）。

## 8. 阻塞项

1. **提交授权未获得**：8 次 `ask_user` 全部 `responseSource=automatic_timeout`、`explicitUserConfirmation=false` ⇒ 按既定规则不执行提交。9 颗就绪、今日额度闲置。
2. **20 颗需先补 6 个组合类空槽 + 5 颗纯 OTHER**，全部依赖 prod 通过（10.3% 基线）。
3. **单钉子未破**：`d5W0RQZv`(0.7023, n=1)、`VkxGjzPM`(0.7138, n=1)、`P0oWMg6x`(0.7793, n=2)、`D5W0RQZv` 同族。
4. **平台并发 2**，prod 账号级单并发，单波次产出受限于墙钟。

## 9. 工具事实（本轮新增）

- `batch_create_simulations` **在无空槽时不会快速失败**：14 条单批调用挂 15 分钟无返回；6 条（有空槽时）5 秒返回。正解 = 「发 N 条 → 轮询终态 → 再发下一批」，0 接受必须 sleep。固化脚本 `results/_wave2.py`。
- `get_operators` 返回 `{"results":[...]}`，103 个算子含 signature。
- `get_alpha_yearly_stats` **经 MCP** 返回 `records` 是 **dict 列表**（非 raw API 的列表的列表），按索引取会 `KeyError(0)`。
- `batch_status` 对 REGULAR 仿真仍报 `kind=multisim, child_count=0`（已知误判），须直连 `/simulations/{id}` 看 `progress`。
