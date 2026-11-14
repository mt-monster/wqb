# 可靠提交清单（终验后） · 2026-11-14 12:29 GMT+8

> **只读终验，未提交任何 alpha。** 本轮把所有「指标未验证/过期」项逐颗真重测：prod 走 `check_correlation(refresh=True)`（覆盖 48h 缓存）、self 走本地 OS PnL 池重算、平台 checks / 塔计数 / 稳健台账 / 配额全部重读。

## 0 结论

**主池 26 颗可执行候选：A 0 / B 4 / C 6 / U 16**（另有 2 颗同席后备、3 颗池外旧硬闸件，共 31 颗方案 D 放行件；这 5 颗同样未完成 prod 终验）。配额：ET 2026-11-13 REGULAR **2/4，剩 2 席**（SUPER 1/1 用尽）。

**✅ 已提交**：`wpo8olA6` 于 2026-11-13T22:59:27-05:00（ET 11-13 22:59）提交成功，平台回查 `status=ACTIVE` / `stage=OS`；已从可提交清单移出，`DEU/D1/OTHER` 塔 2→3 点亮。

| 级别 | 数量 | 含义 |
|---|---:|---|
| **A 零待办** | **0** | prod 刷新 <0.7、self <0.7、方案D 放行、平台 0 FAIL / CW PASS、稳健台账 PASS、免三问、**ops≤8** |
| **B 待动作** | **4** | 硬指标全过，但缺 self 实测 / 稳健审计声明 / 三问答复核 |
| **C 排除** | **6** | prod≥0.7、方案D 阻断、平台 FAIL 等 |
| **U 未终验** | **16** | 本轮未取得 `refresh=True` 实测值（账号级相关性熔断），fail-closed，**不得进提交清单** |

⚠ **平台熔断**：prod 相关性端点在连续 pending 后触发账号级保护，约 10 分钟内不触发计算；本轮共 10 颗拿到 `refresh=True` 实测值（含熔断解除后的慢速补测）。U 级候选的 `refresh=False` 复查值全是 11-11/11-12 的旧缓存（`computed=False`），按项目铁律**只许证伪、不许放行**，因此一律不进清单。

**推荐（若你决定提交，按此顺序、最多 3 席）**：`omEdka3v` → `6XdkW08J` → `pwdd7Za6`。仍需你点名，agent 不自行提交。

**★ 相对 prod 约束（软偏好，接口已更正）**：唯一基准 = `GET /consultant/boards/leader?stage=osmosis&user=<self_id>` 的 **`meanProdCorrelation` 0.6396**（REGULAR 账户均值，submissionsCount 232）；SUPER 同口径 `superAlphaMeanProdCorrelation` 0.6308 仅作参考。候选 `refresh=True` 实测 prod < 0.6396 标 ✓（全量评估 v2 +5 分），≥ 标 ✗ 但不排除。⛔ 上一版误用 `/users/self/alphas` 逐颗 `is.prodCorrelation`（最新件 .6788）当基准，已作废。

排序按「终验级别 → 稳健已闭环 → prod 余量 → self 余量 → 质量分」，不是纯分数；且 **ops>8 一律排除**（`leAmmre8` 9 / `Xg9dPpp0` 9 / `Jje6mrpO` 10 已移出）。唯一零待办是 `wpo8olA6`；`omEdka3v` 只差三问答复核；第三席 `6XdkW08J`（8 ops / 稳健 PASS / 五项全达标）。

## 1 ★ 刷新后推翻的结论（必须看）

| alpha | prod 旧值(12:20) | 本轮 refresh=True | 判定 |
|---|---:|---:|---|
| `ZYa6x531` | 0.6964 | **0.9229** | 超线排除 |
| `88NmN37X` | 0.5541 | **0.9540** | 超线排除 |

### self 重测修正（本地 OS PnL 池，28 颗全覆盖）

| alpha | 12:20 值 | 本轮实测 | 影响 |
|---|---:|---:|---|
| `omEdka3v` | 0.492 | **0.416** | 数值校正 |
| `RREPm361` | 0.688 | **0.327** | 旧缓存高估，实测解除分散度风险 |
| `pwdd7Za6` | 缺失 | **0.416** | 补齐缺口 |
| `wpo8olA6` | 缺失 | **0.578** | 补齐缺口 |
| `ZYa6x531` | 缺失 | **0.199** | 补齐缺口 |
| `88NmN37X` | 缺失 | **0.954** | self≥0.7 硬闸排除 |
| `Xg9dPpp0` | 缺失 | **0.279** | 补齐缺口 |
| `Jje6mrpO` | 缺失 | **0.329** | 补齐缺口 |
| `leAmmre8` | 0.450 | **0.262** | 数值校正 |
| `1YNMAA8M` | 缺失 | **0.695** | 补齐缺口 |
| `mLaLllmK` | 0.301 | **0.100** | 旧缓存高估，实测解除分散度风险 |
| `d5apEYRx` | 缺失 | **0.231** | 补齐缺口 |
| `2r5MqmVJ` | 缺失 | **0.239** | 补齐缺口 |
| `Jj8qXO5m` | 缺失 | **0.245** | 补齐缺口 |
| `rKRx7v6m` | 0.428 | **0.338** | 数值校正 |
| `RREGX1kd` | 缺失 | **0.369** | 补齐缺口 |
| `LLM0e20m` | 缺失 | **0.404** | 补齐缺口 |
| `E56GgqLL` | 缺失 | **0.435** | 补齐缺口 |
| `78L5GaeZ` | 缺失 | **0.461** | 补齐缺口 |
| `O0A6Qz7p` | 缺失 | **0.678** | 补齐缺口 |
| `zq3Yrb3G` | 缺失 | **0.687** | 补齐缺口 |
| `pwdLp9z6` | 0.475 | **0.420** | 数值校正 |
| `xAvK73Qg` | 缺失 | **0.557** | 补齐缺口 |

最典型：`RREPm361` 旧缓存 .6879 → 实测 **.3275**（旧值高估 .36），`88NmN37X` 实测 **.9540** 与 prod .954 互相印证 ⇒ 双闸同时排除；`wpo8olA6` 的 self 缺口补为 .5784。

**塔计数也漂移了**：`get_pyramid_alphas` 当季实读 `EUR/D1/RISK = 3`（12:20 报告记 2）⇒ 该塔**已点亮**，本轮交 RISK 候选不再产生塔边际增量；`DEU/D1/SHORTINTEREST = 4`（原记 3）。⇒ 本轮实际可新点亮只剩 **GBR/D1/OTHER、DEU/D1/OTHER 两座**，KOR/D1/PV 仍为 2 且唯一点亮候选已被方案 D 拦下。

**主题资格**：31 颗平台 checks 全部带 `MATCHES_THEMES` WARNING（6 颗另带 `CLUSTER_TEST`），即**均不满足当期主题资格**；不影响 RA 提交，但计入 CPPAP 评奖的条目不会增加。`CONCENTRATED_WEIGHT` 31/31 全 PASS、`is.checks` FAIL 0、状态全 UNSUBMITTED、无 `PowerPoolSelected` 标签。

## 2 A 级：零待办（可直接点名提交）

| # | alpha | 区/分 | S/F | ops | prod 旧→新(✓<0.6396) | self 旧→新 | 稳健 | 三问 | D 裁决 | 塔归属→现值→交后→新点亮 | 塔增量 |
|---:|---|---|---|---|---|---|:---:|:---:|:---:|---|:---:|
| — | 无 | | | | | | | | | | |

## 3 B 级：硬指标全过，缺人工动作

| # | alpha | 区/分 | prod 旧→新(✓<0.6396) | self 旧→新 | 稳健 | 三问 | 塔归属→现值→交后→新点亮 | 塔增量 | 待办 |
|---:|---|---|---|---|:---:|:---:|---|:---:|---|
| 1 | `omEdka3v` | GBR/92 | 0.6026→**0.6026✓** | 0.492→**0.416** | PASS | 需答 | SHORTINTEREST 4→5 否（已亮） / OTHER 2→3 点亮 | 1 | 2–3 腿三问答复核 |
| 2 | `6XdkW08J` | GBR/71 | 0.6267→**0.6267✓** | 0.340→**0.339** | PASS | 需答 | SHORTINTEREST 4→5 否（已亮） / MODEL 6→7 否（已亮） | 0 | 2–3 腿三问答复核 |
| 3 | `RREPm361` | DEU/49 | 0.6881→**0.6881✗** | 0.688→**0.327** | PASS | 需答 | ANALYST 6→7 否（已亮） | 0 | 2–3 腿三问答复核；prod 贴线（提交前再 refresh） |
| 4 | `pwdd7Za6` | GBR/52 | 0.6238→**0.6238✓** | —→**0.416** | 台账无记录 | 免 | SHORTINTEREST 4→5 否（已亮） / PV 4→5 否（已亮） | 0 | 稳健审计待补/需显式声明 |

## 4 C 级：排除（含逐颗塔信息）

| alpha | 区/分 | prod 旧→新 | self | D 裁决 | 排除原因 | 塔归属→现值→交后→新点亮 |
|---|---|---|---|:---:|---|---|
| `wpo8olA6` | DEU/88 | 0.6306→0.6306 | 0.578 | 放行 | 已于 2026-11-13T22:59:27-05:00 提交 ACTIVE（ET 11-13），不可重复提交 | SHORTINTEREST 5→6 否（已亮） / OTHER 3→4 否（已亮） |
| `ZYa6x531` | EUR/49 | 0.6964→0.9229 | 0.199 | 放行 | prod 0.9229 ≥ 0.7 | EARNINGS 1→2 否 |
| `88NmN37X` | DEU/62 | 0.5541→0.9540 | 0.954 | 放行 | 算子数 9 > 8（≤8 才合格）；prod 0.9540 ≥ 0.7；self 0.9540 ≥ 0.7 | SHORTINTEREST 5→6 否（已亮） / INSIDERS 1→2 否 |
| `Xg9dPpp0` | GBR/60 | 0.4000→0.4000 | 0.279 | 放行 | 算子数 9 > 8（≤8 才合格） | SHORTINTEREST 4→5 否（已亮） / RISK 0→1 否 / FUNDAMENTAL 3→4 否（已亮） |
| `Jje6mrpO` | GBR/53 | 0.5565→0.5565 | 0.329 | 放行 | 算子数 10 > 8（≤8 才合格） | SHORTINTEREST 4→5 否（已亮） / RISK 0→1 否 / FUNDAMENTAL 3→4 否（已亮） |
| `leAmmre8` | GBR/72 | 0.6887→0.6887 | 0.262 | 放行 | 算子数 9 > 8（≤8 才合格） | SHORTINTEREST 4→5 否（已亮） / OTHER 2→3 点亮 |

## 4b U 级：prod 未终验（不得进提交清单）

| alpha | 区/分 | 12:20 旧 prod | 本轮状态 | self 重测 | 塔归属→现值→交后→新点亮 |
|---|---|---:|---|---:|---|
| `rKRRjM51` | IND/53 | 0.6752 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.653 | INSTITUTIONS 1→2 否 / PV 11→12 否（已亮） |
| `1YNMAA8M` | DEU/48 | 0.6951 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.695 | MODEL 3→4 否（已亮） / ANALYST 6→7 否（已亮） |
| `mLaLllmK` | EUR/60 | 0.6579 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.100 | OTHER 3→4 否（已亮） |
| `d5apEYRx` | EUR/41 | 0.6887 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.231 | EARNINGS 1→2 否 |
| `2r5MqmVJ` | EUR/45 | 0.6740 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.239 | EARNINGS 1→2 否 |
| `Jj8qXO5m` | EUR/45 | 0.6663 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.245 | EARNINGS 1→2 否 |
| `rKRx7v6m` | EUR/52 | 0.6756 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.338 | SENTIMENT 3→4 否（已亮） / OTHER 3→4 否（已亮） |
| `RREGX1kd` | GBR/54 | 0.5940 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.369 | SHORTINTEREST 4→5 否（已亮） / ANALYST 3→4 否（已亮） |
| `LLM0e20m` | GBR/53 | 0.5386 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.404 | SHORTINTEREST 4→5 否（已亮） / NEWS 3→4 否（已亮） |
| `omExeqLb` | GBR/59 | 0.6143 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.420 | SHORTINTEREST 4→5 否（已亮） / MODEL 6→7 否（已亮） |
| `E56GgqLL` | EUR/43 | 0.5524 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.435 | FUNDAMENTAL 3→4 否（已亮） / OTHER 3→4 否（已亮） |
| `rKRx0M2m` | GBR/48 | 0.6232 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.443 | SHORTINTEREST 4→5 否（已亮） / RISK 0→1 否 |
| `78L5GaeZ` | EUR/43 | 0.6662 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.461 | ANALYST 10→11 否（已亮） / OTHER 3→4 否（已亮） |
| `WjOeNE6O` | EUR/56 | 0.6411 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.641 | IMBALANCE 3→4 否（已亮） / OTHER 3→4 否（已亮） |
| `O0A6Qz7p` | GBR/64 | 0.6984 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.678 | SHORTINTEREST 4→5 否（已亮） / OTHER 2→3 点亮 |
| `zq3Yrb3G` | EUR/61 | 0.6872 | prod 未取得 refresh=True 实测值（账号级熔断，fail-closed） | 0.687 | RISK 3→4 否（已亮） / ANALYST 10→11 否（已亮） / SENTIMENT 3→4 否（已亮） |

## 5 后备 / 池外

**同席让位（后备，仅当对应主候选被排除才启用）**：

| alpha | 让位原因 | prod 刷新 | self 刷新 | 稳健 | 塔归属→现值→交后→新点亮 |
|---|---|---:|---:|:---:|---|
| `pwdLp9z6` | 同席 ρ≥0.7 | — | 0.420 | — | SHORTINTEREST 4→5 否（已亮） / OTHER 2→3 点亮 |
| `xAvK73Qg` | 同席 ρ≥0.7 | — | 0.557 | CONDITIONAL | SHORTINTEREST 5→6 否（已亮） / OTHER 3→4 否（已亮） |

**原 11 颗排除件中方案 D 放行、但旧硬闸仍在的 3 颗**：`ZYQv7j2Q`（prod/self 双超线）、`LLMv6joe` 与 `zqdvb0YE`（prod 未闭环；`zqdvb0YE` 另属 qM7 同族 ρ=1.0）——本轮 prod 已重测，仍不进主清单。`d5a2aO7v` 端点 400，未取得 prod 值。

## 6 终验口径与边界

- **prod**：全部走 `refresh=True` 真重测（账号级单并发，串行；cooldown busy 已按 retry_after 补测），`refresh=False` / 预读 / 48h 缓存值一律不作为放行依据；`≥0.7` 无豁免。
- ⚠ **补测受限**：熔断到期后按 20s 间隔慢速重测，前 2 颗仍被 `correlation_busy / Another production correlation check is already running` 挡下（账号级槽被并行会话占用），后台任务随后被会话回收 ⇒ 25 颗保留 U 级。恢复后跑 `py results/_final_verify_prod_after_cooldown_20261113.py`（断点续跑），再跑 `py results/_reliable_submit_list_20261113.py` 重生成清单；期间不轰炸平台。
- **self**：`check_self_correlation` 本地 OS PnL 池重算；未取到值的候选只能进 B，不能进 A。
- **方案 D、ΔS**：沿用 20:1x 全篮子实测（`performance_comparison`），本轮未重复触发。
- **稳健台账**：`robustness_<id>` 读 `ledger_kv`；`REJECT` 硬拦，`None` / `CONDITIONAL` 列为待办（提交需 `robustness_audited=True` 显式声明或补审计）。
- **塔**：`get_pyramid_alphas` 当季 ACTIVE 计数（季度重置），点亮线 ≥3；增量按最终顺位贪心扣重。
- **ΔS 禁跨分区横比**；`MATCHES_THEMES` WARNING 属评奖资格，不属 RA 提交闸。
- **算子数硬闸（21:09 用户明令）**：只认 `regular.operatorCount` 平台实值，**≤8 才合格**；>8 一律排除（`leAmmre8` 9 / `Xg9dPpp0` 9 / `Jje6mrpO` 10 等），同等绩效下越少越好。
- **相对 prod 为软偏好**（用户措辞「最好小于」）：只把 `refresh=True` 实测值与 board 的 `meanProdCorrelation` 比较；缓存/预读值不参与。该值是 N=232 已提交件的**账户均值**，无分辨率、不进提交闸（`tools/gates/prod_gate_audit.py` 定案），仅作评估软偏好与口径校准。
- **只挖不提交**：本清单是「可提交」判定，不含 POST；提交权归用户点名。提交前仍须按 A/B 待办完成签核，并对贴线 prod 再 `refresh=True` 一次。

## 7 产物

- `results/final_verify_prod_20261113.json`（逐颗 refresh=True 实测值 + 时刻 + 来源）
- `results/final_verify_self_20261113.json`（self 重测）、`results/final_verify_meta_20261113.json`（checks / 塔 / 稳健 / 当季计数）
- `results/reliable_submit_list_20261113.json`（本清单机读版）
- 脚本：`results/_final_verify_prod_20261113.py`、`_final_verify_prod_retry_20261113.py`、`_final_verify_meta_20261113.py`、`_final_verify_self_20261113.py`、`_reliable_submit_list_20261113.py`
