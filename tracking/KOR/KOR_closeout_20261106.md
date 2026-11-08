# KOR 战役收尾（2026-11-06）· 实产 2 颗

> 目标原为 KOR ATOM/REGULAR 10 颗。全探结论：**KOR D1 ATOM 空间实际只产出 2 颗达标件**，其余全部判死。
> 本文件是这 2 颗的最终验收材料，也是本战役的结项依据。

## 一、最终候选（均 UNSUBMITTED，未提交）

| # | alpha | 塔 | S | F | 2Y | TO | 收益 | 回撤 | sub_S | L/S |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `qMLOooX1` | KOR/D1/ANALYST ×1.6 | **1.94** | 1.74 | **1.76** | 9.72% | 10.05% | 5.61% | 1.71 | 238 / 397 |
| 2 | `RRE9NkVj` | KOR/D1/INSIDERS ×1.2 | **1.76** | 1.63 | **2.77** | 9.68% | 10.70% | 7.08% | 1.70 | 317 / 318 |

### 表达式

```
#1 qMLOooX1 (analyst10, 中性化几何)
group_neutralize(
  multiply(
    group_rank(ts_av_diff(anl10_smartest_sal_fy2_pred_surps_v1,250),sector),
    group_rank(ts_av_diff(anl10_smartest_net_fy1_pred_surps_v1,250),sector)),
  industry)

#2 RRE9NkVj (insiders5, 交易流量横截面分歧度)
subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_vol_chg), 55), sector))
```

### 设置（逐字段实测值）

| 设置 | #1 | #2 |
|---|---|---|
| region / universe / delay | KOR / TOP600 / 1 | KOR / TOP600 / 1 |
| neutralization | REVERSION_AND_MOMENTUM | REVERSION_AND_MOMENTUM |
| decay / truncation | 4 / 0.08 | 4 / 0.08 |
| nanHandling | **ON** | **OFF** |
| pasteurization / unitHandling / maxTrade | ON / VERIFY / **OFF** | ON / VERIFY / **OFF** |
| startDate – endDate | 2014-01-01 – 2023-12-31 | 同 |

## 二、★ 闸的真实状态（不要误称「全闸通过」）

两颗原本 FAIL = 0 / PASS = 10 / PENDING = 6；**现已把 self 与 prod 两条硬线全部测出，结果均通过**。

| 状态 | 检查项 |
|---|---|
| FAIL（空） | — |
| **已实测通过** | `SELF_CORRELATION`、`PROD_CORRELATION` |
| 仍 PENDING（不影响资格判定） | `DATA_DIVERSITY`、`REGULAR_SUBMISSION`、`POWER_POOL_CORRELATION`、`MATCHES_THEMES` |
| WARNING | `MATCHES_COMPETITION`、`MATCHES_THEMES` |

### ★ 两条硬线实测结果（2026-11-06 18:50 前后）

| alpha | SELF max | PROD max | 判定 |
|---|---:|---:|---|
| `qMLOooX1` | **0.3939** | **0.6941** | 双线通过（prod 余量仅 0.006） |
| `RRE9NkVj` | **0.3104** | **0.6605** | 双线通过 |
| `kqNv1xRk`（备选） | 0.3639 | 待读 | self 通过 |

`qMLOooX1` 的 prod 直方图 `[0.6,0.7)` 有 **4 个**产品 alpha、max 0.6941；`RRE9NkVj` `[0.6,0.7)` 有 **8 个**、max 0.6605。都不是深钉，但都贴近 0.70 上限。

⚠ **self 的口径要看清**：`check_self_correlation` 只跟**已提交（OS）池**（本次 pool 29 条）比。`RRE9NkVj` 与 `kqNv1xRk` 都还是 UNSUBMITTED，所以两颗都「通过」——它们是同机制（仅字段不同：`insd5_vol_chg` vs `insd5_ghc_tr`），**先提交的那颗会把另一颗的 self 推向 1.0**，实际只能取一颗。
**prod 的读取路径（覆盖此前「结构性取不到」的结论）**：MCP `check_correlation` 固定 120s 超时，但超时**不会**取消服务端已派出的计算；等本机 inflight 标记（`logs/_dblock/correlation.inflight.json`，默认 300s TTL）过期后**重查同一个 alpha**，即可读到已完成的值。若 `retry_after` 恒为 240，是该账号唯一 prod 槽被另一条工作线占着（看 inflight 里的 id 与 pid），让路等释放即可，不要杀进程、不要反复 refresh。
**⇒ 提交前的硬线前置已全部满足**；剩余风险只有 `qMLOooX1` 的 prod 余量 0.006，产品池一变就可能越线。

## 三、逐年覆盖（判据：longCount>0 且 pnl≠0）

| 年 | #1 S | #1 pnl | #1 L/S | #2 S | #2 pnl | #2 L/S |
|---|---:|---:|---|---:|---:|---|
| 2014 | 1.12 | 472,640 | 230/348 | 0.52 | 302,278 | 283/295 |
| 2015 | **0.63** | 357,060 | 239/371 | 1.41 | 903,740 | 306/304 |
| 2016 | 2.63 | 1,223,579 | 244/375 | 0.76 | 437,537 | 309/310 |
| 2017 | 1.43 | 624,668 | 240/379 | 2.51 | 1,247,867 | 313/306 |
| 2018 | 1.26 | 790,195 | 247/403 | **0.42** | 255,317 | 314/336 |
| 2019 | 2.11 | 1,032,917 | 239/406 | 1.63 | 967,108 | 331/314 |
| 2020 | 2.98 | 1,613,723 | 241/403 | 1.27 | 862,337 | 325/319 |
| 2021 | 3.66 | 2,318,694 | 237/442 | 3.23 | 2,222,929 | 339/340 |
| 2022 | 2.95 | 1,560,738 | 235/418 | 3.54 | 2,148,253 | 325/328 |
| 2023 | **0.69** | 406,158 | 231/423 | 2.21 | 1,725,754 | 329/324 |

⇒ **10/10 年满覆盖，无连续空窗**，长短期持仓数对称（无 CW 结构性风险）。

## 四、失效风险（自查结论）

1. **年份集中**：#1 的 pnl 集中在 2020–2022（三点合计 5,493,155 / 全期 10,400,372 = **52.8%**），2023 只有 S 0.69。
   ⇒ 若近年分析师惊喜定价效率提升，收益可能衰减。
2. **#2 的 2Y 由近三年扛起**（2021–2023 S 3.23/3.54/2.21），2018 仅 0.42。2Y 2.77 不代表中期稳定；
   按全期十年看 S 1.76 才是它的真实水平。
3. **#1 的字段版本敏感**：wave297 实测同一字段的 v0/v2 版本只有 S 1.11–1.13，**只有 v1（稳定化核心层）能到 1.94**。
   ⇒ 这既是它的强度来源，也是它的脆弱点：版本口径一变信号即消失。
4. **prod 未知**：分析师族在 KOR/USA/DEU 有「普遍撞 prod 墙」的历史记录（analyst44 prod 0.93）。
   #1 用的正是 analyst 族，prod 风险高于 #2。

## 五、KOR 判死登记（本战役新增，勿重开）

| 数据集 / 族 | 判死依据 | 结论 |
|---|---|---|
| `insiders5` 库藏股族 | wave290 批 A：8/8，max\|S\| 0.88 | 死 |
| `insiders5` 控制权集中度（source_ratio） | wave290–296：45+ 条，天花板 S 1.45 / 2Y 1.69（跨 decay 2/4/6、窗口 5/22/66/252、分组 sector/market/industry/subindustry、vec_avg/max/sum、倒数/平方/ts_rank/ts_scale、eps 0.001/0.01、nanH ON/OFF 全部稳定） | 死（距 1.58 差 0.13） |
| `analyst10` smartest 族（除 net_fy1_v1/sal_fy2_v1 一对） | wave297：12/12，max S 1.18 | 死（见 §四.3） |
| `news` 全塔 | `datasets/news20.md` §7 五条轴全落 .25–.67 | 死 |
| `sentiment` 塔 | sentiment27 / other106 / other553 三连死 | 死 |
| `earnings3` | KOR S 0.83 天花板 + IND/MEA/GLB 三区判死 | 死 |
| `institutions` 全类 | fund_holdings_panel + institutions6 均无 ATOM 路 | 死 |
| `imbalance5` | 三机制 2Y 均 ≈0.17，结构性不可达 | 死 |

## 六、待办（唯一未完成项）

## 七、平台提交闸 dry-run（`confirm_submit=false`，2026-11-06 18:58）

| alpha | submit_gate | blocked_reasons | failed_ra | failed_any | hard_gate_warns | 边际 ΔSharpe | 是否稀释 |
|---|---|---|---:|---:|---|---:|---|
| `qMLOooX1` | **passed: true** | [] | 0 | 0 | [] | **+0.23** | 否 |
| `RRE9NkVj` | **passed: true** | [] | 0 | 0 | [] | **+0.29** | 否 |

基线分区 `EQUITY:KOR:1:POWER_POOL`：S 4.41 / F 3.22 / TO 18.9% / ret 10.05% / DD 1.56%。

⇒ 计入后：`qMLOooX1` → S 4.64 / F 3.48 / DD 1.46%；`RRE9NkVj` → S 4.70 / F 3.54 / DD 1.36%。两颗都**不是稀释件**。

> 刷新核验（19:05）：对 `qMLOooX1` 发 `refresh:true` 重算，回读仍为 **0.6941 / passes**，直方图 `[0.5,0.6) 91`、`[0.6,0.7) 4` 与 14:58 缓存逐项一致；但 `cachedAt` 未更新为当前时间，**无法确认是真的重算过还是又读了旧缓存**。该值至少在本轮两次独立读取下稳定。

⇒ **平台自己的提交闸判定为可提交**；叠加 §二 的 self（0.3939 / 0.3104）与 prod（0.6941 / 0.6605）全部实测通过，
本战役两颗的提交前置验证**已全部完成**。

## 八、待办（唯一剩余项）

**提交**：两颗均未提交，需用户明确授权。剩余动作：
1. **唯一需要你决定的**：提交哪一颗。`RRE9NkVj` 与 `kqNv1xRk` 同机制互斥（只能取其一），`qMLOooX1` 无同族竞争者
2. ⚠ `qMLOooX1` 的 prod 余量只有 0.006（0.6941 vs 上限 0.70），且该值是 14:58 的缓存；若离提交隔得久，建议先重算一次再按确认
3. 你确认后执行 `workflow_submit_alpha(confirm_submit=True)`；`kqNv1xRk` 的 prod 因账号唯一 prod 槽被另一条工作线反复抢占，仍未读出（备选件，不影响主决定）

**备选（同为 insiders5 分歧度机制，只能取一）**：`kqNv1xRk` S 1.62 / F 1.50 / 2Y 2.23，与 `RRE9NkVj` 仅字段不同（`insd5_ghc_tr` vs `insd5_vol_chg`）。