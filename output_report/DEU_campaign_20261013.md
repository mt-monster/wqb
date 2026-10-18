# DEU 战役状态报告

**时间**：2026-10-13 00:55（跨 10-12 夜场）
**区域**：DEU ｜ TOP500 ｜ D1 ｜ decay4 ｜ FAST ｜ trunc0.08 ｜ nanHandling ON
**目标**：产出可提交 REGULAR alpha（用户锁定 DEU；只挖不提交）

---

## 一、平台核实：DEU 破闸确认

### ★ 冠军（已 ACTIVE）
**`Wje5K71x`** — 7 算子
```
group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(fnd6_newq_oiadpq,240)),
                                         rank(ts_delta(fnd6_newq_oiadpq,176))),
                               target_tvr=0.03), sector)
```
| 闸 | 值 | 门槛 | 结果 |
|---|---|---|---|
| LOW_SHARPE | **1.73** | 1.58 | PASS |
| LOW_FITNESS | **1.37** | 1.0 | PASS |
| LOW_TURNOVER / HIGH_TURNOVER | 0.123 | 0.01 / 0.7 | PASS |
| LOW_SUB_UNIVERSE_SHARPE | 1.14 | 0.75 | PASS |
| LOW_2Y_SHARPE | **1.87** | 1.58 | PASS |
| CONCENTRATED_WEIGHT / MATCHES_PYRAMID | — | — | PASS |
| **PROD_CORRELATION** | **0.4305** | 0.7 | **PASS（大步余量）** |
| **SELF_CORRELATION** | 0.1879 | 0.7 | **PASS** |

> 关键杠杆（本战役新发现）：**去掉分母**。原始科目 level 的双窗差分（`ts_delta(oiadpq,W)`）
> 优于 ROE 比率形式（`ts_delta(oiadpq/seqq,W)`）——S 1.56 → 1.73，且算子 10→7。

---

## 二、互相关实证：13 颗「全闸」实为 2 条腿

`compute_mutual_correlation`（本地零消耗，13 颗候选 N×N）：

- fnd6 OIADP 族 12 颗**内部互相关 0.84 ~ 1.00**（近亲变体）
- `JjQ9ZQpW`（shrt3 TC×BAR）与它们 **0.01 ~ 0.03**（完全独立）
- **最大互不相关子集 = 2 颗**：`Wje5K71x` + `JjQ9ZQpW`

⇒ **「13 颗 IS 全闸」并不等于 13 颗可提交**（同腿只出 1 颗）。

### 但第 2 条腿撞 prod 墙
| alpha | 腿 | prod | self |
|---|---|---|---|
| `Wje5K71x` | fnd6 盈利动量 | **0.4305 ✅** | 0.1879 ✅ |
| `JjQ9ZQpW` | shrt3 TC×BAR（S1.59/2Y2.69）| **0.7879 ❌** | 0.2112 ✅ |

⇒ **DEU 实质只有 1 条可提交腿。**

---

## 三、本轮三波新批次（共 24 条）

### W373 — 把冠军模板迁移到 fnd6 的其它会计科目 → **全弱**
| 科目 | S | 2Y |
|---|---|---|
| 营收/资产 | 1.03 | 1.76 |
| 现金/资产 | 0.95 | 2.14 |
| 应收/资产 | 0.54 | 0.98 |
| 资本支出/资产 | 0.38 | 0.49 |
| 存货/资产 | 0.15 | 0.44 |
| 折旧/资产 | 0.12 | 1.32 |
| 费用/资产 | 0.05 | 1.42 |
| 长期负债/资产 | −0.08 | 1.46 |

⇒ **冠军模板不可迁移**：盈利动量的信息**只存在于利润表营业利润行**。

### W374 — tvr target 档位调优 × 4 条腿
| 腿 / 档 | S | F | 2Y |
|---|---|---|---|
| fnd6 oiadpq raw，tvr **0.02** | **1.74** | 1.39 | **1.41 ❌** |
| fnd6 oiadpq raw，tvr 0.03（冠军档）| 1.73 | 1.37 | **1.87 ✅** |
| shrt3 TC×BAR，tvr 0.03 | 1.59 | 1.13 | 2.69 ✅（prod 墙）|
| anl93 corrrev×recprof，tvr 0.03 | 1.31 | 0.93 | 0.95 |
| fnd6 ibq/seqq 双窗，tvr 0.03 | 1.27 | 0.86 | 1.32 |
| inst1 掩码，tvr 0.03 | 1.24 | 0.74 | 1.20 |
| inst1 双窗差分，tvr 0.03 | 0.94 | 0.48 | 1.05 |

⇒ tvr target 是 **S ↔ 2Y 权衡旋钮**（0.02 过冲伤 2Y）；inst1/anl93 是机制级不足。

### W375 — model 族（分析师预期修正 / model238 rank）→ **高 S 但 2Y ≈ 0**
| 字段 | S | F | 2Y |
|---|---|---|---|
| F12M EBITDA 预期变化 | **1.56** | **1.22** | **−0.01 ❌** |
| FY1 earnings 预期变化 | **1.51** | **1.16** | **−0.08 ❌** |
| FY1 earnings 14d | 1.45 | 1.07 | 0.03 ❌ |
| F12M revenue 预期变化 | 1.36 | 0.99 | 0.14 ❌ |
| mdl238_global_rank | 1.31 | 0.91 | 0.30 ❌ |
| mdl238 其余 3 个 | ≤0.63 | | ≤1.07 |

⇒ 与 GBR `smest_price_ratio_*` **同型假象**：近期一致预期修正在 DEU 是短命信号。

---

## 四、结论与可选方向

**DEU 事实上只有 1 条可提交腿（fnd6 盈利动量）。10 颗可提交 REGULAR alpha 在 DEU 不可达。**

| 方向 | 波次 | 结果 |
|---|---|---|
| fnd6 其它会计科目 | W373 | 全弱（≤1.03）⇒ 模板不可迁移 |
| fnd6 tvr 档位 | W374 | S 1.74 但 2Y 1.41 ⇒ 过冲 |
| shrt3 tvr 档位 | W374 | IS 全闸但 prod 墙 |
| inst1 / anl93 | W374 | 1.24~1.31，机制级不足 |
| model / 预期修正 | W375 | S 1.36~1.56 但 2Y ≈0 ⇒ 死 |

**可选下一步**：
1. 接受现状：DEU 交付 = `Wje5K71x`（ACTIVE）+ 一批 IS 级储备；
2. 继续挖 DEU 未探数据集（analyst45/25/15、news/pv/risk——历史多为死区，命中率低）；
3. 换 region（与「永久锁定 DEU」冲突，需用户明示）。
