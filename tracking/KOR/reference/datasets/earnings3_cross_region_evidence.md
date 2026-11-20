# earnings3 跨区模板证据汇总（2026-11-20，全区域检索）

> 补全 §8.11 论坛/跨区取证缺口。来源：全库 DB 检索（backtest_results 48851 行 / alphas 49104 / expressions 111706）+ docs/reference + 全部 tracking/<REGION>/ 目录。检索词：`ern<N>_interval` / `ern<N>_reptime` / `next_ed` / `announcement` / `财报日历`。日历类判定 = 表达式真含 interval/reptime/next_ed/announcement 时点字段；EPS/股息/情绪类与 intraday_pv_feats 盘中 interval 已剔除。

## 各区域实测汇总

### GLB —— 最强读数在「日历作 trade_when 门控腿」（MINVOL1M/D1/FAST，wave 115/117 + mcp-20261103）

| alpha | 表达式要点 | S | F | TO | 2Y | prod |
|---|---|---|---|---|---|---|
| xArN8G7J | `trade_when(rank(ts_mean(ern3_pre_reptime,22))>0.6, signed_power(subtract(group_rank(<dlrf-img>,country),0.5),0.5), 0)` | 3.21 | 2.05 | 9.9% | 2.97 | 0.7549 撞墙 |
| QPv79Xg5 | `trade_when(rank(ts_backfill(ern3_pre_interval,126))>0.7, <20day img>, rank(...)<0.6)` | 3.19 | 1.70 | 22.5% | 4.12 | 未回读 |
| **LLM7kvYm** | `trade_when(rank(-ts_backfill(ern3_next_interval,252))>0.7, <20day img>, rank(...)<0.6)` | 3.07 | 1.54 | 25.8% | 2.27 | **0.6066/self 0.5682 双过** |
| wpQjevQ5 | 同构，门控腿= `ts_delta(ern3_pre_interval,66)` | 2.78 | 1.30 | 24.3% | 2.52 | — |
| LLMGAM66 | 门控腿=`ts_mean(ern3_pre_reptime,66)`，5day img | 2.90 | 1.79 | 9.7% | 2.45 | — |

要点：门控方向 = 「距上次财报久」或「下次财报临近」时开仓；**reptime 也能当门控腿**。GLB w16 反教训：硬门控在弱基底上砸 fitness（F 0.36–0.81）；上面成立是因为基底信号本身 S 3+。

### IND —— 日历作主信号的唯一成功形态 = 对 returns 的残差回归（TOP500，wave 174→250→251）

| alpha | 表达式 | S | F | TO | 2Y | 备注 |
|---|---|---|---|---|---|---|
| MP0EwRQM | `rank(-ts_regression(ts_zscore(returns,252), ts_zscore(ern3_all_delay_1_pre_interval,252),252,rettype=0))` | 2.37 | 1.73 | 22.3% | 1.33 | STATISTICAL/decay126；卡 IS_LADDER |
| **kqJweZQz** | 同构，`ern3_pre_interval` 直连 | 2.24 | 1.92 | 19.0% | **2.93** | SUBINDUSTRY/decay126；w251 记 prod 0.5262/self 0.265/fRA=0（⚠ alphas 表另记 0.7937，两处不一致，引用前重验） |
| 3qjKgeAX | 同构 all_delay_1 | 2.12 | 1.78 | 19.0% | 2.03 | SUBINDUSTRY；prod 0.4049 |
| blbproEK | `(-1)*(rank(ts_delta(ts_delta(ern3_pre_interval,5),5)))` 二阶 delta | 0.70 | 0.24 | 47.2% | 1.48 | w174 判「主信号死、只作条件腿」 |
| E5pbM7Nm | `trade_when(less(ern3_pre_interval,-5), rank(-ts_mean(corr_vwap_with_volume,5)), greater(ern3_pre_interval,-2))` | 4.49 | 3.25 | 36.3% | — | 日历门控 PV；**prod 0.981 判死** |

关键杠杆：**SUBINDUSTRY 中性化修 ladder、decay126（decay252 实测恶化）**；残差化能吃掉 delay 损耗（all_delay_1 与直连版同强 2.12 vs 2.24，而 KOR 水平形态 delay 版掉 0.2）。

### MEA —— 日历单信号全灭，只作组合腿（TOP400/D1，w99 + w81/82/83）

- 单信号 9 条全灭（w99 verdict 原文「earnings3日历族MEA无独立信号全灭」）：`ts_delta(ern3_next_interval,63)` S 0.34、reptime 差 S 0、`pre-next` 差 S −0.13 等。首轮设计稿 `tracking/MEA/wave1_earnings3_exprs_v2.json`（ts_zscore 20/60、pre*next、next/(pre+1)）无果。
- 组合腿有效：`rank(ts_mean(ern3_next_interval,5))` 0.35–0.4 权重混入 fnd72+analyst（kqjN3zqz S 1.69/F 2.03、d5W0jgx S 1.71/F 2.10），**prod 0.853/0.857 全撞墙**。
- 字段档案：`tracking/MEA/reference/mea_earnings3_fields.json`（cov 0.43–0.52，与 KOR 同款字段）。

### USA —— 零 interval/reptime 字段；announcement「定价溢价」类两轮判死（TOP3000）

- earnings4 announcement 族最优 `A1VMrQbw`：`hump(group_neutralize(group_rank(ts_zscore(ts_backfill(eighth_historical_announcement_percent_move,126),504), subindustry), industry), hump=0.0001)` S 1.14/F 0.67/TO 2.9%/2Y 1.91。w334/w339 两轮 22 模板 0 过闸 ⇒ DEAD_MECHANISM（premium_ratio 面 S≈0.83 即 USA/D1 上限；group_backfill 不改排序）。
- 结构教训（w124A）：**「信号强度由数据集本身决定，骨架不是瓶颈」**——同一冠军骨架在 earnings_sent_matrix S 2.14、earnings4 只 0.82、earnings6 只 0.46。
- USA 从未测过 ern3 系（ern6/ern7 全是 EPS/股息 VECTOR）。

### DEU —— ern6_next_ed 直接作信号弱；GLB/IND 日历候选已进口未测

- 最优 `MP6Wn0e8` `group_rank(ts_mean(vec_count(ern6_next_ed),252),sector)` S 0.71；`days_from_last_change` 版 S −0.10/−0.23；`conferencecalltime` 0.59/0.42/−0.17。
- `tracking/DEU/candidates/cross_region_pool_20261030.json` 收了 GLB 门控 4 条 + IND 残差 1 条进待测池，**本地未实测**。

### EUR / GBR —— earnings6 日历字段直接信号失败

- EUR 唯一实测 `O0AZpdnb`：`group_rank(ts_delta(ts_backfill(vec_avg(ern6_next_ed_216),120),22), subindustry)` S 0.25；`ern6_time_of_day_220`（盘前/盘中/盘后，cov 1.0）**未测**。
- GBR：`days_from_last_change(vec_avg(ern6_next_ed))` S −0.10/−0.23；`bl6xlvrR`（conferencecalltime）S −0.17。

### 其余区域

| 区域 | 结论 |
|---|---|
| HKG | inventory 只列塔倍率 1.3、候选 2 集，无波次；DB 0 行 |
| ASI / JPN | 命中的 `*_interval` 全是 intraday_pv_feats 盘中字段，无 ern 测试 |
| CHN / TWN | 零行、零命中 |
| AMR | 1 条失败探针 `rank(vec_avg(ern6_time_zone_371))` S=0 |

## 可迁移模板清单（去重，按 KOR 适配度排序）

1. **残差回归（最强，直击 KOR 的 F 0.49 墙）**：`rank(-ts_regression(ts_zscore(returns,252), ts_zscore(ern3_pre_interval,252),252,rettype=0))`｜IND S 2.24–2.37/F 1.73–1.92｜配 SUBINDUSTRY + decay126；⚠ IND 两处 prod 读数矛盾先重验。残差几何下 all_delay_1 与直连同强 ⇒ KOR 的 delay 损耗可能被吃掉。
2. **财报临近门控（双阈值）**：`trade_when(rank(-ts_backfill(ern3_next_interval,252))>0.7, <强基底>, rank(...)<0.6)`｜GLB S 3.07 prod/self 双过｜基底必须换 KOR 自有强信号（KOR akKXKJOR 把日历自身当门控对象 S −0.17 的失败 = 门控对象不能是日历本身；GLB w16 = 弱基底别硬门控）。
3. **财报后窗口门控（PEAD 窗）**：`trade_when(less(ern3_pre_interval,-5), rank(<信号>), greater(ern3_pre_interval,-2))`｜IND S 4.4–4.5 但 prod 0.98 死（结构成立，死因是 PV 基底拥挤）｜KOR 须换非 PV 基底。
4. **reptime 门控变体**：`trade_when(rank(ts_mean(ern3_pre_reptime,22/66))>0.6/0.7, <信号>, 0)`｜GLB S 3.21/2.90｜reptime 作信号全库皆弱（MEA 0、IND 0.86），作门控腿有效——**reptime 唯一已证用法**。
5. **组合腿（机制参考，不可直接抄）**：MEA 0.35–0.4 权重混腿 S 1.69–1.92——⚠ 违反现行 mixed_signal_leg_ban_v1（§7.7），合规替代是 1/2/3 的门控或残差形态。
6. **二阶 delta**：IND S 0.70（KOR 已知，未再展开）。

## KOR 平移注意事项

① 符号：next_interval 为正倒数（KOR 最优 S 0.94 = `-rank(next)`，与 GLB 门控方向一致）；pre_interval 恒非正。
② 覆盖：MEA 同款字段 cov 仅 0.43–0.52；KOR 先 `ts_backfill(x,126/252)`（GLB 全部这么做）。
③ all_delay_1 变体：KOR 水平形态掉 0.2 S，但 IND 残差形态下与直连同强 ⇒ 残差化可能吃掉 delay 损耗。
④ 行业轴结论不可跨族外推（§7.6 ①-bis）：IND 的 SUBINDUSTRY-ladder 结论只对「残差几何」成立；KOR 水平形态实测最优轴仍是 sector。
⑤ USA 结构教训适用：同一骨架跨数据集读数由数据集本身决定 ⇒ KOR 水平形态 S 封顶 0.95 时应**换角色（门控/残差）而非换骨架**。

## 反证记录（不要平移的形态）

- `ern6_next_ed`/`conferencecalltime` 的 `vec_count/vec_sum/ts_mean/days_from_last_change` 直接作信号：DEU/EUR/GBR 全弱或负。
- `ts_count_nans(reptime,3)` 门控（IND vRr0pxzr S 0.86）不达闸。
- 平滑族（IND wave393 S 0.03）：事件时钟被抹平。
- USA announcement premium 族：DEAD_MECHANISM（22 模板 0 过闸）。
