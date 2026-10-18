# zqrj0bzK 优化到极致 — 最终报告（2026-10-17）

> 使用 skill：`wq-alpha-gate-push-op-min`｜区域/宇宙：IND / TOP500｜类型：REGULAR
> 判定口径：IS 全闸 PASS（含 2Y，显示值须 ≥ limit+0.005） + self<0.7 + prod<0.7

## ① 最终达标表达式

```
group_rank(
  if_else(
    greater(vec_avg(anl44_best_eps_numest), 2),
    ts_delta(anl44_eps_best_eeps_cur_yr, 66),
    0
  ),
  sector
)
```
- alpha id：**`E5VbMKER`**（A_t2）
- settings：delay=1, decay=4, neutralization=STATISTICAL, truncation=0.08, nanHandling=OFF, maxTrade=OFF

## ② 指标全景（优化前 → 优化后）

| 闸门 | limit | 原 zqrj0bzK | **A_t2 (E5VbMKER)** | 余量 |
|---|---:|---:|---:|---:|
| LOW_SHARPE | 1.58 | 1.66 | **1.90** | +0.32 |
| LOW_FITNESS | 1.0 | 1.17 | **1.44** | +0.44 |
| LOW_ROBUST_UNIVERSE_SHARPE | 1.0 | 1.02 ⚠️ | **1.08** | **+0.08** |
| LOW_2Y_SHARPE | 1.58 | 2.33 | **2.35** | +0.77 |
| LOW_SUB_UNIVERSE_SHARPE | ~0.56 | 1.09 | **1.20** | +0.64 |
| LOW_TURNOVER | 0.01 | 0.0979 | **0.0986** | — |
| HIGH_TURNOVER | 0.4 | 0.0979 | **0.0986** | — |
| **SELF_CORRELATION** | <0.7 | PENDING | **0.448 ✅** | — |
| **PROD_CORRELATION** | <0.7 | PENDING | **0.704 ❌** | — |

**IS 全闸 PASS，且 binding 闸（robust）余量从 0.02 → 0.08（×4）。**

## ③ 算子数（压缩前后）

| 阶段 | 算子 | 列表 |
|---|---:|---|
| 压缩前（原 zqrj0bzK） | **5** | group_rank, if_else, greater, vec_avg, ts_delta |
| 压缩后（A_t2） | **5** | 同上（仅常量 3→2） |

**压缩结论：算子已 minimal，无法再压。** 去掉 `if_else/greater` 掩码（NF 版，2 算子）虽少 3 算子，但 robust 从 1.08 暴跌到 **1.02（余量 0.02，极薄）**——掩码（分析师覆盖数 ≥2 过滤）是 robust 余量的**唯一来源**，属结构必需，不能消融。

## ④ 参数扫描结论（18 变体实测）

| 旋钮 | 最优 | 证据 |
|---|---|---|
| 分析师覆盖阈值 T | **2** | T=2→robust1.08/S1.90；**T=1→S2.10 但 robust 反降到 1.04**；T≥3→robust 卡 1.02/S 跌破 1.58 |
| 窗口 W | **66** | 44→robust0.61 FAIL；88→0.92 FAIL；120→S1.17 FAIL；仅 66 过闸 |
| decay（T=2 下） | **4** | 4→S1.90/robust0.08；6→1.88/0.08；8→1.86/0.08（decay↑仅降 S，robust 不变） |
| winsorize | 无效 | 同 S/robust，且 +1 算子 |
| 双窗秩乘积 / 掩码乘 | 无效 | E1 S1.94 但 robust0.93 FAIL；E2 S0.88 FAIL |

## ⑤ ★ 唯一未决闸 = PROD（机制层墙）

| 变体 | 信号 | prod | 判定 |
|---|---|---:|---|
| **A_t2**（T=2, decay4） | 掩码≥2 | **0.704** | ❌ |
| A_t2_d6（T=2, decay6） | 掩码≥2·更平滑 | 0.7086 | ❌ |
| A_t2_d8（T=2, decay8） | 掩码≥2·更平滑 | 0.7109 | ❌ |
| A_t1（T=1, decay4） | 掩码≥1 | 0.7239 | ❌ |
| NF（无掩码） | 原始 | 网络失败未定 | —（IS robust 仅 0.02 不作首选） |

**A_t2(T=2) 已是该族最低 prod（0.704）；任何 decay↑ 或阈值↓ 都抬高 prod（0.704→0.724）。参数层面无法压到 0.7 以下。** 与文档「analyst(eps) 族 prod 天花板 0.7000–0.7058，机制层不可达」完全吻合。

## ⑤-b 换字段降 prod 实测（9 个 anl44 兄弟字段，全用 A_t2 结构 T=2/W=66/decay4）

| 字段 | alpha | type | cov | uc/ac | S | robust余量 | minmargin | IS | prod |
|---|---|---|---:|---|---:|---:|---:|---|---:|
| `eps_best_eeps_cur_yr`（基线） | E5VbMKER | MATRIX | 0.894 | 360/1486 | 1.90 | 0.08 | 0.08 | ✅ | **0.704** |
| `dps_best_eeps_cur_yr` | JjPXaaGA | MATRIX | 0.894 | 472/1691 | 1.90 | 0.08 | 0.08 | ✅ | 0.704（同腿） |
| **`eps_best_eeps_nxt_yr`** | LL5XoO7L | MATRIX | 0.895 | 590/2051 | **2.17** | **0.37** | **0.37** | ✅ | **0.8493** |
| `dps_best_eeps_nxt_yr` | e762Mp16 | MATRIX | 0.895 | 699/2304 | 2.17 | 0.37 | 0.37 | ✅ | 0.8493（同腿） |
| `best_eps_4wk_chg` | rKdzavE8 | VECTOR | 1.0 | 401/1479 | 0.91 | — | 0.33 | ❌ | 未测 |
| `best_eps_hi` | d5K7Jebg | VECTOR | 1.0 | 111/209 | 1.35 | — | 0.31 | ❌ | 未测 |
| `best_eps_lo` | 1Yjm3Qak | VECTOR | 1.0 | 218/650 | 1.37 | — | 0.55 | ❌ | 未测 |
| `best_eps_median` | P0MlRz9w | VECTOR | 1.0 | 225/673 | 1.56 | — | 0.03 | ❌ | 未测 |
| `best_eps_stddev` | RRAax6zn | VECTOR | 1.0 | 53/77 | −0.03 | — | 0.04 | ❌ | 未测 |

**两个关键发现**：
1. **下一年度 EPS（`eps_nxt_yr`）IS 显著更强**（S 2.17 / robust 余量 0.37 = 全家族最厚，比基线 S+14%、robust 余量 ×4.6），但 **prod 0.8493 反而更挤**（uc/ac 590/2051 vs 360/1486）⇒ IS 强度与 prod 新颖度负相关的又一实证。
2. **`eps_cur_yr` 与 `dps_cur_yr` prod 逐位相同（0.704）= 同一条腿**（同数据不同命名上下文，同腿判据再次应验）；`eps_nxt_yr`/`dps_nxt_yr` 同理（0.8493）。

⇒ **换字段无法降 prod**：anl44 EPS 家族里最不挤的投影就是当年度（uc/ac 最低 360/1486），prod 0.704 即该族地板。

## ⑥ 结论与下一步

1. **IS 已优化到极致**：A_t2（`E5VbMKER`）是该信号族在 IS/self 维度的最优解（S 1.90 / robust 余量 0.08 / self 0.448）。若只看 IS，`eps_nxt_yr`（`LL5XoO7L`，S 2.17 / robust 余量 0.37）更强，但 prod 0.8493 更不可行。
2. **anl44 EPS 家族 prod 墙**：已穷尽 4 类杠杆共 21+ 个结构（参数级 T/W/decay/winsorize/双窗 + 字段级 4 MATRIX + 5 VECTOR），A_t2(T=2) 的 0.704 是参数面最低；换字段（nxt_yr）IS 更强但 prod 0.8493 更挤。
3. **若要走出 prod 墙，必须换机制/换数据集**（文档结论）：anl44 内 EPS 估计族已封闭；IND 区可选方向 = analyst_factor_signals 的修正幅度族（KOR 实证 prod 0.6952 但 S 仅 1.39）、或换未点亮塔的「直接预测收益率」型数据集。这是新战役立项，不属于「优化 zqrj0bzK」范畴。

## ⑥-b ★ 提交落库记录（用户点名授权 2026-10-17 22:56）

**提交前实测 zqrj0bzK 自身双闸（此前一直 PENDING，从未实测）**：
- **self = 0.4220 ✅**｜**prod = 0.6664 ✅**（双双 < 0.7）
- IS 全闸 PASS：S 1.66 / F 1.17 / TO 0.0979 / 2Y 2.33 / robust 1.02 / sub 1.09

**执行**：`WQB_ALLOW_ALPHA_SUBMIT=1 python tools/super_build.py submit --alpha-id zqrj0bzK --region IND --probe-timeout 120`
- 内置 prod-gate 自判 0.6664 < 0.7 → 过闸（**未使用** `--allow-prod-above-07` 绕过；该豁免开关已于 2026-10-18 按用户判定「不合规」彻底移除，现已无此入口）
- POST `/alphas/zqrj0bzK/submit` → HTTP 201 异步受理
- 轮询复核：**status=ACTIVE / dateSubmitted=2026-10-17T10:56:13-04:00** / name=`IND_S_10comp_rj0bzK`

**★ 关键修正与可迁移教训**：本轮早期据同族 A_t2（T=2，prod 0.704）推断 zqrj0bzK 也会 prod 爆线——**该推断错误**。阈值 T 从 2→3 使 prod 从 0.704 降到 **0.6664（差 0.038，直接决定可提交性）**。「优化到极致」找到的 A_t2（IS 更强）反而不可提交，而原始 zqrj0bzK 可提交。⇒ **铁律：同族变体的 prod 不可互相推断；提交前必须实测目标 alpha 自身的 self/prod。**

## ⑦ 交付物（脚本/数据）

- 扫描脚本：`wqb-scripts/opt_zqr.py` / `opt_zqr2.py` / `opt_zqr3.py` / `opt_zqr_swap.py` / `swap_resume.py`
- 探针脚本：`prod_probe.py` / `prod_probe_multi.py` / `prod_probe_swap.py`
- 结果数据：`opt_zqr_results.json` / `opt_zqr2_results.json` / `opt_zqr3_results.json` / `opt_zqr_swap_results.json` / `opt_zqr_prod_multi.json` / `opt_zqr_swap_prod.json`
- 候选 alpha id：基线 `zqrj0bzK`｜A_t2=`E5VbMKER`（prod 0.704）｜A_t1=`pwvE3awg`｜A_t2_d6=`LL560qMe`｜A_t2_d8=`MP0XJ1Wo`｜NF=`ZYmxX3ad`｜**eps_nxt_yr=`LL5XoO7L`（IS 最强，prod 0.8493）**｜dps_cur_yr=`JjPXaaGA`｜dps_nxt_yr=`e762Mp16`
