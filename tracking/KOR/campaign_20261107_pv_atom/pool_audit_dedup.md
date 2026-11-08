# 存量池达标件审计 · 去重后才是真实交付数（2026-11-07）

## 方法
`get_user_alphas(KOR, IS, REGULAR, limit=100)` 全池拉取，按 S≥1.58 且 2Y≥1.58 且 F≥1.0 过滤，**再按指标指纹去重**。

## 结果：15 条「达标」→ 去重后 6 组
| 指标指纹 (S/F/2Y/TO) | 条数 | 判定 |
|---|---:|---|
| 1.68 / 1.33 / 2.22 / 0.1206 | 1 | distinct（`zq322JzK`） |
| 1.65 / 1.31 / 2.28 / 0.1312 | 1 | distinct（`9qxddA0K`） |
| 1.64 / 1.27 / 2.27 / 0.1308 | 1 | distinct（`akKQQz6w`） |
| **1.62 / 1.23 / 2.27 / 0.1319** | **10** | **同一 PnL，仅 1 颗有效（= `omERn83n` 族）** |
| 1.61 / 1.21 / 2.20 / 0.1328 | 1 | distinct（`d5W33lwx`） |
| 1.58 / 1.15 / 2.25 / 0.1359 | 1 | distinct（`9qxddAQK`） |

那 10 颗 ID：`1YNlKYGK` `gJeggG6K` `QPvNNzMX` `E5688zO9` `2rAXX686` `MPYeezML` `P0oYYzQw` `xAr22GOq` `bl6rrW5m` `N1NJJ5vL`
全部形如 `ts_target_tvr_decay(signed_power(group_rank(winsorize(vector_neut(rank(ts_backfill(rsk70_mfm2_asetrd_anlystsn, 40)), rank(...)), std=0.38), sector), 2.5), target_tvr=...)`。

## 结论（口径纪律）
1. **`failed_ra_count=0` 的行数 ≠ 独立 alpha 数**。必须先按指标指纹与族内互相关去重，否则会把同一表达式的单调改写当成 10 颗交付。
2. 该族 6 组互异读数全部来自同一机制（risk70 分析师情绪载荷 `rsk70_mfm2_asetrd_anlystsn` 对风险因子正交化），族内互相关预计 >0.97 ⇒ 实际只能取 1 颗。
3. **真实交付盘仍为 3 颗**（`omERn83n` / `qMLOooX1` / `RRE9NkVj`），缺口 7 颗，必须靠**新机制**补，不能靠刷同族变体。

## 由此定下的下一阶段纪律
- 新波次必须换**数据集 / 机制轴**，而不是换正交腿字段或窗口。
- 收波后立即对达标件做族内互相关去重，再去汇报条数。