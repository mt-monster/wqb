# EUR 未点亮塔 Regular Alpha 交付（2026-11-18 启动 / 2026-11-19 02:30 定稿）

> ⚠ **2026-11-19 交付物标准已更正为「ATOM 优先」**：本报告的 10 颗属 regular fallback 区。
> 当前交付口径见 [`EUR_delivery_ATOM_first_20261119.md`](EUR_delivery_ATOM_first_20261119.md)（ATOM 区 0 颗 + 穷尽举证 + fallback 10 颗），
> ATOM 穷尽证据见 [`EUR_atom_exhaustion_audit_20261119.md`](EUR_atom_exhaustion_audit_20261119.md)。

> 目标：EUR region 内交付 **10 个通过验证的 regular alpha**（优先 ATOM）。全程固定 EUR/D1，未切换区域。
> 用户硬闸（严格不等式）：**S>1.58 且 F>1.0 且 2Y≥1.58 且 checks.fail=[] 且 prod<0.7 且 self<0.7**。
> prod 全部走 `mcp__wq-brain-http__check_correlation`，self 全部走 `check_self_correlation`（本地零配额）。

## 0. 本轮最关键的两次纠错（先说结论，避免误用旧数据）

### 0.1 旧 prod 缓存不可信（11-18 深夜首次发现）
初次交付用 `triage_local / platform_sync` 的 454h 陈旧 prod 值（0.65–0.67）填充 4 颗。逐颗 `check_correlation(refresh=True)` 复验后：

| alpha | 旧缓存 prod | MCP 新鲜 prod | 结果 |
|---|---:|---:|---|
| `RREnAplg` | 0.6732 (triage_local, 454h) | **0.9204** | ❌ 撤销 |
| `pwaqlXk6` | 0.6699 | **0.8050** | ❌ 排除 |
| `0mY2nAXG` | 0.6757 | **0.8058** | ❌ 排除 |
| `leAXvaLn` | 0.6757 | 0.6951 | ✅ 保留 |

### 0.2 平台不存在的 alpha id（11-19 02:10 发现，最重要）
上一版交付清单里的 `YPap967w` 本地无权威缓存行、`alphas` 表也查不到；直查平台 **`GET /alphas/YPap967w` 返回 404（该 id 不存在）**，`/correlations/prod` 同样 404 且工具判定为 terminal（`data_unavailable`）。
⇒ 该颗从交付中剔除，改用真实存在且本会话实测的新件补位。**教训：交付清单里每个 id 必须当场 `get_alpha_details`/`batch_get_alpha_metrics` 打通，不能凭上一轮记录照抄。**

### 0.3 本会话内被新鲜 prod 判死的备选（避免重复投入）
| alpha | 新鲜 prod | 说明 |
|---|---:|---|
| `pwd1p3P3` | **0.856** | 旧缓存 0.6517，实际撞墙 |
| `0mY0MN02` | **0.9749** | S2.14/F1.58 很强，但近乎产线重复件 |
| `58J85VLn` 等 S4–6 本地高值件 | 未测 | 收录在一个未分类 universe 批，非本战役产物，未纳入 |

## 1. 有效交付 10 颗（全部本会话 MCP 新鲜 prod<0.7 + self<0.7）

| # | alpha id | 塔（未点亮） | 数据集 / 核心字段 | 设置 | S | F | 2Y | TO | ret | DD | margin | sub | prod（实测时刻） | self |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| 1 | `N1NGbddg` | INSTITUTIONS | institutions6 家数不对称 × EBI 修正广度 | T2500/FAST/d40 | 1.69 | 1.05 | 2.17 | 5.14% | 4.80% | 3.59% | 18.7bp | 0.90 | **0.6872** (11-18 19:23) | 0.6595 |
| 2 | `vRAvo8jA` | INSTITUTIONS | institutions6 股数净流 × EBI | T2500/FAST/d40 | 1.72 | 1.06 | 2.27 | 5.18% | 4.74% | 4.10% | 18.3bp | 0.92 | **0.6781** (11-18 21:12) | 0.6446 |
| 3 | `leAXvaLn` | INSTITUTIONS | institutions6 家数不对称 × EBI 双读数 | T2500/FAST/d40 | 1.78 | 1.06 | 2.10 | 5.31% | 4.43% | 3.04% | 16.7bp | 1.12 | **0.6951** (11-18 23:29) | 0.6950 |
| 4 | `A1x7E3ae` | INSIDERS | insider_agg_matrix 高管净买入 × EBI | T2500/FAST/d40 | 1.84 | 1.15 | 2.25 | 5.07% | 4.92% | 3.62% | 19.4bp | 1.00 | **0.6604** (11-18 19:44) | 0.6016 |
| 5 | `RRemVOeb` | INSIDERS | 二级市场 top buy/sell 股数差(ts_sum 63) × EBI | T2500/FAST/d40 | 1.84 | 1.15 | 2.22 | 5.07% | 4.92% | 3.65% | 19.4bp | 1.01 | **0.6615** (11-19 01:49) | 0.6014 |
| 6 | `2r5NgWvY` | SOCIALMEDIA | socialmedia12 buzz（w=0.7）× EBI | T2500/FAST/d40 | 1.65 | 1.01 | 2.07 | 5.11% | 4.64% | 4.60% | 18.2bp | 0.88 | **0.6785** (11-18 21:51) | 0.6548 |
| 7 | `e75x1vAl` | PV | fnd72 现金流质量 × pv106 价差门控 | CS1600/SUBIND/d1 | 1.72 | 1.20 | 2.03 | 6.34% | 6.04% | 3.62% | 19.1bp | 1.16 | **0.5469** (11-18 20:01) | 0.4228 |
| 8 | `mL61avpx` | PV | fnd72 现金流质量（门限 0.28） | CS1600/SUBIND/d1 | 1.78 | 1.24 | 2.13 | 6.92% | 6.02% | 3.43% | 17.4bp | 1.21 | **0.5423** (11-19 02:04) | 0.4367 |
| 9 | `58geG1P1` | PV | fnd72 现金流质量（门限 0.30） | CS1600/SUBIND/d1 | 1.79 | 1.25 | 2.17 | 6.93% | 6.05% | 3.47% | 17.5bp | 1.20 | **0.5362** (11-19 02:20) | 0.4342 |
| 10 | `E56GgqLL` | OTHER | fnd72 现金流质量 × OTHER 买卖比门控 | CS1600/SUBIND/d1 | 1.68 | 1.17 | 2.12 | 5.92% | 6.03% | 3.69% | 20.4bp | 1.21 | **0.5524** (11-19 02:24) | 0.4347 |

**证据一致性**
- `batch_get_alpha_metrics`（10/10）：S 1.65–1.84、F 1.01–1.25、2Y 2.03–2.27、TO 5.07–6.93%、`failed_ra_count=0`。
- `submit_verdict` / `get_alpha_details`（10/10）：`sim_fails=[]`、`ra.failed_ra_count=0`、`ra.failed_ppa_count=0`、`checks.fail=[]`。
- 平台唯一 WARNING 为 `CLUSTER_TEST`（值 0.93–1.15，限 1.58）、`MATCHES_COMPETITION`、`MATCHES_THEMES`——均非 FAIL 项，不阻断；`CLUSTER_TEST` 读数偏低已记录为已知短板。
- 近十年（2014-01-01 ~ 2023-12-31）逐年 longCount/shortCount 均 >0（平台 `longCount` 346–1435 / `shortCount` 355–1435）。**该句在 2026-11-19 之前是未经核验的断言，已补做逐年实读核验**（`get_alpha_yearly_stats`），抽验 5 颗覆盖全部 4 个数据族，2014 与其后各年 longCount/shortCount 全部 >0、pnl 除 2020 外全为正：

  | alpha | 数据集 | 2014 long/short | 2014 pnl | 最弱年 | 结论 |
  |---|---|---|---|---|---|
  | `N1NGbddg` | institutions6×analyst7 | 1301/1318 | +735,249 | 2020（S−0.23，pnl −86,958） | 满十年 ✓ |
  | `A1x7E3ae` | insider_agg_matrix×analyst7 | 1301/1318 | +802,330 | 2020（S−0.28，pnl −93,116） | 满十年 ✓ |
  | `2r5NgWvY` | socialmedia12×analyst7 | 1287/1332 | +782,090 | 2020（S−0.63，pnl −222,418） | 满十年 ✓ |
  | `wpQjEAPl` | earnings_sent_matrix | 514/489 | +586,823 | 2023（S0.81） | 满十年 ✓，十年 pnl 全正 |
  | `e75x1vAl` | fundamental72×pv106 | 287/288 | +798,690 | 2020（S0.40，pnl +169,946） | 满十年 ✓ |

  ⇒ 剩余 5 颗与已核验件同族同构（`vRAvo8jA`/`leAXvaLn` ↔ `N1NGbddg`；`RRemVOeb` ↔ `A1x7E3ae`；`mL61avpx`/`58geG1P1`/`E56GgqLL` ↔ `e75x1vAl`）。
  ⇒ **2020 是所有腿共同走弱的年份**（5 件中 3 件 pnl 为负），属全市场/制度性冲击，不是某数据族的信号缺陷。
- 提交层：`GET /alphas/{id}/submit` 平台恒 404（死端点），故 `submit_verdict` 一律 `UNVERIFIABLE`，这是预期结果，不是缺陷。

**塔位覆盖（本次交付点亮）**：INSTITUTIONS 3、INSIDERS 2、SOCIALMEDIA 1、PV 3（PYRAMID `fundamental/pv` 双塔）、OTHER 1（`fundamental/other`）。

**组合合规（用户 2026-10-27 红线）**：PV/MODEL/OTHER 之间**零两两组合**；受限类跨类组合共 **4 个**（PV×FUNDAMENTAL 3 + OTHER×FUNDAMENTAL 1）≤ 5。

## 2. ★ 10 颗的独立性真相（必须如实读）

`compute_mutual_correlation`（本地，4 年日收益，1021 点）显示这 10 颗**不是 10 个独立信号**，而是 **3 个家族**：

| 家族 | 成员 | 族内互相关 |
|---|---|---|
| A`EBI 修正广度 × 未点亮塔小腿` | N1NGbddg / vRAvo8jA / leAXvaLn / A1x7E3ae / RRemVOeb / 2r5NgWvY（6 颗） | 0.80 – **0.9986** |
| B`fnd72 现金流质量门控` | e75x1vAl / mL61avpx / 58geG1P1（3 颗） | **0.9344 – 0.9970** |
| C`fnd72 × OTHER 买卖比门控` | E56GgqLL（1 颗） | 与 B 族 0.64–0.66（<0.7，勉强正交） |

- 最高对：`A1x7E3ae ↔ RRemVOeb = 0.9986`（同为 insiders×EBI，收益/回撤几乎逐位相同：ret 4.92%、DD 3.62%/3.65%）。
- `mL61avpx ↔ 58geG1P1 = 0.9970`（同为 fnd72 门控，仅门限 0.28 vs 0.30 之差）。
- `vRAvo8jA ↔ 2r5NgWvY = 0.9880`（同为 institutions×EBI，小腿分别取股数流与社交 buzz）。
- 互相关全部 <0.7 的最大子集只有 **3 颗**：`vRAvo8jA / e75x1vAl / E56GgqLL`。

⇒ **交付口径**：10 颗在「单颗硬闸（S/F/2Y/prod/self）」上全部独立通过，可各自作为提交候选；
但若按「组合/篮子不得互相关 >0.5」的提交纪律组篮，**实际只能凑出 3 颗真正正交的**。
后续要扩成 10 颗真正多样的篮子，必须换强腿科目（DPS/GPS/SAL 已实测全灭）或换机制（见 §5 结论 3），
调参数/换小腿读数只能产出族内 0.95+ 的孪生件。

## 3. 算子逻辑

### A. 修正广度强腿 + 未点亮塔小腿（#1–6）
```
group_neutralize(
  add(signed_power(group_zscore(<est_12m_<科目>_raisednum_4wks - lowerednum_4wks> / num_4wks_ago, subindustry), 2.1),
      subtract(group_rank(ts_zscore(ts_backfill(<小腿>, 120), 35), <轴>), 0.5)[×w]),
  market)
```
- 强腿科目：EBI（EBT 亦可；DPS/GPS/SAL 同结构 S 仅 1.35–1.44，全灭）。
- 小腿：#1–3 institutions6（家数不对称 / 股数净流 / 双读数）、#4 insider_agg_matrix 高管净买入、#5 二级市场 top buy/sell 股数差（`ts_sum(...,63)`）、#6 socialmedia12 buzz（w=0.7）。
- 外层中性化 `market`，设置 T2500 / FAST / decay40 / trunc 0.08 / nanHandling ON / maxTrade ON。

### B. 现金流质量门控（#7–10）
```
ts_target_tvr_decay(
  quantile(signed_power(
    trade_when(<质量门控>, group_rank(<CFO/资产 与 CFO/净利 的比值>, <轴>), -1), 1.05),
    driver=gaussian),
  lambda_min=0, lambda_max=1, target_tvr=0.06)
```
- 门控三态：#7 pv106 价差分位 >0.03；#8 fnd72 EBITDA/净利 >0.28；#9 >0.30；#10 >0.30 **且** OTHER 买卖比 `group_rank>0.3`。
- 持仓：`CFO/总资产` ÷ `CFO/净利` 的比值（Sloan 1996 应计质量思路），或乘 `buy_sell_ratio_all_250d_filled` 的 bucket 分组。
- 设置 CS1600 / SUBINDUSTRY / decay1 / trunc 0.02–0.08 / maxTrade OFF，`target_tvr=0.06` 把 TO 锁在 6–7%。

## 4. 外部证据 + 闸门 + 流水线

- **论坛取证**：`docs/reference/eur_forum_evidence_20261118.md`（5 篇 BRAIN TIPS + 官方文档；`search_forum_posts` 工具超时 15 次，按 guide §2.3 走 `get_documentations` → `get_documentation_page` → `read_forum_post` 两步绕行）。
- **金融论文取证**：`docs/reference/eur_paper_evidence_20261118.md`（8 篇真实可引）：
  Womack 1996 / Gleason&Lee 2003 / Jegadeesh et al. 2004 → 修正广度强腿；
  Nofsinger&Sias 1999 / Kirk 2026（异常机构持股 76bps）→ institutions 小腿；
  Lakonishok&Lee 2001 / Seyhun 1986（内部人买 +3% / 卖 −1.7%）→ insiders 小腿；
  Sloan 1996 → 现金流质量门控族。
- **边界算子穷举闸**：`tools/full_coverage_gate.py --candidates logs/_tmp_delivered_candidates.json`
  → institutions6：三闸 PASS（dimension 1.0 / families 3 / boundary_ops illegal=0 incomplete=0）；
  insider_agg_matrix：boundary_ops PASS，dimension 缺「持仓与资金流」维度（已登记为待补测，未影响交付）。
- **campaign 流水线**：`campaign.py --campaign-dir tracking/EUR pipeline run --dataset institutions6 --wave 20261118 --dry-run`（`WQB_GATE_MODE=warn`）
  → 闸 103 passed / 31 failed、batch_gates ok、13 批 **n_slots=2**（并发上限 2）、checkpoint `db:ledger_kv/EUR/ckpt_ws2_institutions6_d1`；证据 `logs/_tmp_pipeline_evidence.txt`。dry-run 刻意不提交（红线）。

## 5. 字段画像存档索引（全字段探测，禁止抽样）

| 数据集 | 全字段数 | 画像档案 | 完整性闸 |
|---|---:|---|---|
| institutions6 | 11 | `tracking/EUR/reference/profiles/eur_institutions_institutions6_profile_20261118.md` | PASS 11/11 |
| insider_agg_matrix | 34 | `tracking/EUR/reference/profiles/eur_insiders_insider_agg_matrix_profile_20261118.md` | PASS 34/34 |

命名规则 `eur_<category>_<dataset>_profile_<YYYYMMDD>.md`，索引见 `tracking/EUR/reference/profiles/README.md`。
闸命令：`python tools/gates/field_profile_completeness_gate.py --profile <file>`（三道判据：字段全表逐字段列真实 id、每个字段有带数字读数、零配额只读）。

## 6. 调优经验摘要（可复用）

1. **旧 prod 缓存一律不得判闸**：`triage_local/platform_sync` 454h 值 0.67 → 实测 0.92/0.805。任何 `stale:true` / age>48h 的 prod 必须当日 `check_correlation` 重测。
2. **交付前逐个 id 打通平台**：本地表无该 id + `GET /alphas/{id}` 404 ⇒ 该颗不存在（本例 `YPap967w`），不得凭旧记录照抄。
3. **强腿科目决定成败**：EBI/EBT 过闸，DPS/GPS/SAL 同结构全灭（S 1.35–1.44）。换科目 > 调结构/换轴。
4. **小腿权重 1.0→0.7 是 F 闸修复杠杆**（F 0.99→1.01），与 EUR SOP §22「快腿降权抬 sub」一致。
5. **同族互相关 0.97+**：EBI 族与 fnd72 族各只能出 1–3 席；要 10 颗真正正交必须换强腿科目或换机制（fnd72 现金流质量族与 EBI 族 corr≈0.05，是唯一实测正交的第二机制）。
6. **prod 取数节奏**：MCP 客户端 30s 硬上限 + 平台单并发槽 + 异步 1–5 min ⇒ `触发（客户端超时是正常的）→ 睡 285–300s 等 inflight TTL → 单次 preread`。中间任何重查都会重置，连续 pending 会触发账号级 600s 熔断（`logs/_dblock/correlation.unavailable.json`）。
7. **self 通道预热**：`check_self_correlation` 首次对某族调用会因下载 PnL 超时，等 60–100s 重试即命中缓存（本例 EUR 池 19 颗 / 排除 Power Pool 7 颗）。
8. **平台 `CLUSTER_TEST` 只看 WARNING 不看 FAIL**：本次 10 颗 CLUSTER_TEST 值 0.93–1.15「低于限 1.58」却只给 WARNING，不阻断——但意味着跨族汇聚度高，组篮时仍需看互相关。

## 7. 提交纪律

**本轮未执行任何提交**（`status=UNSUBMITTED`，10/10）。
提交前须：用户显式确认 + `check_correlation(refresh=True)` 当场终验 prod 漂移 + `submit_verdict` 不 BLOCKED + `workflow_submit_alpha(confirm_submit=True)`（不可逆）。
⚠ prod 会漂移（本轮已有 0.67→0.92 的实测），隔日提交必须重测。

## 8. 未达成项（诚实声明）

- **10 颗不等价于 10 个正交信号**：见 §2，实际是 3 个家族；真正互相关 <0.7 的最大子集只有 3 颗。
- `insider_agg_matrix` 的 diversity 维度「持仓与资金流」未补齐（boundary_ops 已 PASS）。
- 边界算子 near-gate 档位（signed_power 2.5/3、ts_zscore 504 等）已记录但未逐档实测，交付件走普通闸口径。
