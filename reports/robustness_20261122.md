# 稳健性审计 · 2026-11-22

> brain-alpha-robustness Phase B/C 判定（闸门只读 `references/techniques.md`，阈值不随当日论坛变化）。

---

## P05zx7zx — KOR/TOP600/D1 · `KOR/D1/INSTITUTIONS`

**表达式**

```
trade_when(ts_mean(count_institutional_holders_security,90)<33,
  add(rank(ts_scale(divide(count_institutional_buyers_security,
                           ts_mean(count_institutional_holders_security,72)),1260)),
      rank(ts_scale(ts_decay_linear(divide(subtract(count_institutional_buyers_security,
                                                    count_institutional_sellers_security),
                                           ts_mean(count_institutional_holders_security,72)),42),1260))),
  -1)
```
设置：INDUSTRY · decay 16 · trunc 0.08 · nan OFF · pasteurize ON

### Phase B 归因

| 项 | 值 |
|---|---|
| IS 全期 | S **1.60** / F **1.36** / 2Y **1.74** / TO 3.47% / DD 7.17% / margin **5.19 bp** |
| 逐年 Sharpe | 0.69 / 0.77 / 2.11 / 2.12 / 0.95 / 1.46 / 2.42 / 1.96 / 1.33 / **2.09** |
| 逐年 PnL | **10/10 全正**，无零持仓年；long/short 每年 188–249 |
| 近 3 年 | 2021 1.96 · 2022 1.33 · 2023 2.09 |
| prod / self | **0.3879**（2026-11-22 02:12 实测 refresh）/ **0.2433**（pool 33） |
| 平台硬闸 | fail=[]；failed_RA=0；failed_PPA=0；subU 1.51；invest_S 1.60 |

### Phase C 判定表

| 检查项 | 读数 | 判定 |
|---|---|---|
| WebDataScope failed count | 0，无 PENDING | PASS |
| Recent-3yr Sharpe（主判定） | 均值 1.793 ≥ 1.58，且三年全正 | **PASS** |
| Recent-3yr CV_Sharpe | 0.227 < 0.40 | PASS |
| 衰减比（末年产/全期） | 2.09 / 1.60 = **1.31** | PASS |
| 平年（近 3 年） | 0 | PASS |
| max/min（近 3 年） | 2.09 / 1.33 = 1.57 ≤ 3 | PASS |
| 全历史早年疲软 | 2014 0.69 / 2015 0.77 / 2018 0.95 | 软标记（**不 REJECT**） |
| Sub-universe | `LOW_SUB_UNIVERSE_SHARPE` PASS | PASS |
| 算子数 | distinct **8** > 5 | 软标记（REGULAR 不据此 REJECT） |
| Margin @ turnover | 5.19 bp @ TO 3.47% | PASS（≥5 bp） |
| Top-5 集中度 | 未直接测；`CONCENTRATED_WEIGHT` PASS（单票上限 <10%，持仓 229/223） | 软标记（未测） |
| 经济可解释性 | 「机构持有人广度（买入家数占比 + 净买卖家数）在机构覆盖稀薄（<33 家）的韩国小盘上具领先性」 | PASS |

**结论：`PASS`**，软标记 3 条（ops=8 / 早年偏弱 / Top-5 未测）。

### 备注

- 本件与 `Jj8zG0Ye` **逐位同绩效**（pnl 9,302,642 / DD .0717 / TO .0347 / subU 1.51 全等），
  唯一差别是删掉了恒等层 `signed_power(…,1.0)`（distinct ops 9→8）。
- 方案 D v2：本件无「编辑前状态」（单次仿真直出），参照件 `Jj8zG0Ye` 与它逐位相同
  ⇒ ΔS=ΔF=ΔRet=ΔTO=ΔDD=**0** ⇒ **L0 放行**。
  （`performance_comparison` 返回的是 `EQUITY:KOR:1` 分区口径 S 6.06→6.06，非本件前后值，不作判据。）
