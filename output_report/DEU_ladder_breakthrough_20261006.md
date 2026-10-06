# DEU ladder 攻关结果（2026-10-06 · W86–W89）—— ladder 闸已破

## 一、结论

**拿到本战役（前 89 波 0 颗可提交）的第一颗「全闸通过 + 相关性双闸通过」的可提交 REGULAR。**

| | **`58gkLAkk`**（首选） | **`akxENQE9`**（备选） |
|---|---|---|
| Sharpe | **1.75** | 1.60 |
| Fitness | **1.42** | 1.17 |
| Turnover | 0.1457 | 0.1377 |
| **IS_LADDER_SHARPE (2Y)** | **2.07** ✅ | **2.04** ✅ |
| SUB_UNIVERSE | 1.22 ✅ | **1.30** ✅ |
| margin / returns / drawdown | 0.001316 / 0.0959 / 0.0781 | 0.001064 / 0.0733 / — |
| 塔 | **MODEL×1.8 + OTHER×1.8（双 ×1.8）** | 同 |
| **`failed_ra_count`** | **0** ✅ | **0** ✅ |
| `checks.fail` | **`[]` 空** | **`[]` 空** |
| **prod / self** | **0.5381 ✅ / 0.5153 ✅**（`all_passed: true`） | prod 平台计算中 |

`blOdNrqR` 之前的全场最佳 `j28rN6YZ`（2Y 1.58 == limit → FAIL）**已可退役**：同一骨架第 4 层轴一换，ladder 从 1.58 → **2.07**。

---

## 二、突破口：第 4 条**正交分组轴族**

```
group_neutralize(
  group_neutralize(
    group_neutralize(
      group_neutralize(quantile(add(ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 1008), 8),
                                    ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 1008), 252))),
                        oth455_relation_n2v_p10_q50_w1_pca_fact1_cluster_20),
      oth455_relation_n2v_p10_q200_w1_pca_fact3_cluster_20),
    subindustry),
  bucket(rank(ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 1008), 252)), range="0,1,0.1"))
                                                                       ↑★ 新增：字段"慢分量"的十分位桶
```

设置：`DEU / TOP500 / D1 / decay=8 / SUBINDUSTRY / truncation=0.08 / nanHandling=OFF / maxTrade=OFF`

**四层轴各剥一种共性**：
① 图聚类轴（文本图关系）→ ② 图聚类轴 → ③ 行业族 `subindustry` → ④ **慢分量分位桶（"水平/久期"代理）**。
前三层各自剥掉一种共性后，收益仍可被"字段长期水平"这一维主导；第 4 层把它也剥掉 ⇒ **收益来源被强制分散到各水平层内**。
这正是论坛 `rank_by_side` 帖讲的「**降低单层极端贡献**」原理，但用**本账号可用且合规的 `bucket`** 实现。

---

## 三、同批单变量对照（证明是"这个轴"在起作用，不是巧合）

| 变体 | 2Y | FAIL 数 | 结论 |
|---|---:|---:|---|
| 桶按 **字段慢分量** `ts_mean(bf,252)`（首选） | **2.07** | **0** | ✅ |
| 桶按 **信号自身** `rank(T3)` | 0.91 ~ 1.29 | 2 | ❌ **桶必须按"信号之外的东西"分** |
| 桶粒度 0.05（二十分位） | 0.16 | 3 | ❌ 组内样本不足 |
| 桶粒度 0.2（五分位） | 0.51 | 3 | ❌ |
| 中位数两半 `buckets="0.5"` | 0.51 | 4 | ❌ |
| 外层换 `group_rank` | **2.04** | **0** | ✅ 亦过闸（sub 更高 1.30） |
| 桶内 `group_zscore` | −0.10 | 3 | ❌ |

---

## 四、论坛调研的产出（用户要求"没灵感查论坛"后的实际结果）

| 论坛线索 | 本账号/本族实测 | 处置 |
|---|---|---|
| **`rank_by_side(x)`**（70 赞帖，该作者 ladder 0.28→2.44） | 平台报 **`inaccessible or unknown operator`** ⇒ **无权限**；其"等价写法" `group_rank(x, sign(x))` 报 **`Incompatible unit at index 1`** | ❌ 不可用 ⇒ **改用 `bucket` 自造轴（成功）** |
| `power(ts_rank(alpha, 180), 2)`（13 赞帖，JPN 1.24→≥1.58） | S 1.69→**1.44**、ladder 1.58→**1.52** | ❌ 数据集特异，本族伤 |
| 「CROWDING / RAM 修 2Y」（评论区，GLB 基本面） | CROWDING 2Y 1.25 / NONE 1.52 / MARKET 1.56 / REVERSION 崩 | ❌ 不迁移到本区本族 |
| 「内层 GN 会被外层 setting 吸收成恒等变换」 | NONE 下删掉外层 GN：2Y 1.52→**1.12** ⇒ **未被吸收，我的结构有效** | ✅ 假设被证伪（反向确认） |
| `multiply(alpha, add(1,alpha))` / `signed_power(alpha,2)` / `group_zscore(alpha, densify(market))` | 1.10 / 1.14 / 1.58(=基线，`densify(market)` 只有 1 组 ⇒ 退化) | ❌ |

---

## 五、状态与下一步

- **零提交**：本会话未提交任何 alpha；两颗候选均为平台 `UNSUBMITTED`。
- **`58gkLAkk` 已具备提交条件**（RA 全过 + prod/self 双过）。提交不可逆，**等用户明确确认**。
- `akxENQE9` 的 prod 仍在平台单并发队列中计算（`max_correlation: null`），出结果后可作同族第二方案——
  ⚠ 但**同族铁律：一条腿只出 1 颗**，两者高度同构（仅外层 `group_neutralize` vs `group_rank`），
  若要都提交须先测两者互相关。
- 该第 4 层轴已回写 skill `wq-operator-playbook-by-gate` §4.1，可迁移到其它区域/数据集验证。
