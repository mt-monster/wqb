# EUR REGULAR 战役 — 联网实测报告（ra-pipeline 为头，平台步骤真跑）

> 日期：2026-08-25 ｜ 目的：按用户要求"需平台的地方连一下再测"，把 S0/S1/S6 三个依赖平台的步骤用**真实平台连接**跑通，验证 I/O，并确认 S1→S3 闭环。

## 0. 连接建立（关键前提）

平台可达性：`api.worldquantbrain.com` 返回 401（主机在线、需鉴权）→ 沙箱有网络到平台。
凭证有**两条独立来源**，本会话均验证可用：

| 来源 | 读取者 | 加载方式 |
|---|---|---|
| `~/.brain_credentials`（email/password） | toolkit 脚本（`_lib/common.load_credentials`） | score / scan-fields / build-wave / wave_gate / pipeline |
| `world-quant-brain-mcp/.env`（`CREDENTIALS_EMAIL/PASSWORD`） | `brain_api.BrainApiClient` | submit_verdict（brain_config.load_config） |

实测：
- `_lib/api.Api.login()` → 成功（拿到 session cookie），`GET /users/self` 返回账户信息。
- `BrainApiClient.ensure_authenticated()` → JWT 注入成功，`get_user_alphas(region=EUR)` 返回真实 alpha（gJjMLb0Q/Wj7g2gAx/78jdv6b1 均 ACTIVE）。

## 1. S0 数据集体检（score）— 真实平台

```
INPUT : campaign.py score            # 注意：不接受 --region，region 取自 settings.json(EUR)
OUTPUT: datasets=178 alive_ranked=31 (tier1=27 tier2=8 floor_band=1) dead_skipped=4 mode=general method=quantile
        ranking -> db ledger_kv/EUR/s0_ranking   (EXIT=0)
TOP   : global_seasonal_model(1.06) / ai_equity_alpha(1.00) / analyst_earnings_ibes(0.998)
        / ai_factor_transfer(1.0,20f) / model238(0.87,22f) / continuation_score(0.99,560f) ...
```
- 纯 `GET /data-sets` + 本地评分，**零配额消耗**。
- 产物已落 `ledger_kv/EUR/s0_ranking`（实测：total=178, mode=general, top1=global_seasonal_model）✅

## 2. S1 字段扫描（scan-fields）— 真实平台

```
INPUT : scan_fields.py --dataset model238
OUTPUT: dataset=model238 fields=44 data_type=MATRIX types={'MATRIX':44}
        catalog -> db fields/EUR/model238 (44)   (EXIT=0)
```
- 纯 `GET /data-fields?dataset.id=model238&...`（分页拉字段），**零配额消耗**。
- 闭环验证（用 gate 的同一代码路径读回）：
  `CampaignStore.get_field_catalog("EUR","model238")` → `field_count=44`，sample:
  `country_relative_investment_rank` / `country_relative_investment_rank_d1` /
  `global_change_in_preference_rank` / `global_change_in_preference_rank_d1` ✅
- **结论：S1 写、S3(gate) 读，同一 CampaignStore，真实数据完全闭合。**

## 3. S6 提交层判定（submit_verdict）— 真实平台，只读

```
INPUT : tools/submit_verdict.py --alpha-id gJjMLb0Q
OUTPUT: === alpha gJjMLb0Q status=ACTIVE ===
        --- 模拟层 checks: 0 条 (FAIL 0 / WARNING 0) ---
        --- 提交层 GET /alphas/gJjMLb0Q/submit: HTTP 404 ---
        VERDICT: BLOCKED   (EXIT=0)
```
- 双视图：① `get_alpha_details` 模拟层 checks；② `GET /alphas/{id}/submit`（**零成本、不耗提交配额**）。
- 404 = 该 alpha 已 ACTIVE、不可重复提交，故 BLOCKED。**全程零 POST submit** ✅。
- 注：EUR 当前 UNSUBMITTED alpha 数 = 0（全已提交），故演示用 ACTIVE id；判定 I/O 与只读性质已证明。

## 4. S5 review — 本会话无输入（非流程缺陷）

`review_wave.py` 入参 `--multisim/--alphas`，读本地 `backtest_results`。当前 `backtest_results` EUR 行 = **0**（dry-run 不提交，无回测指标）。
→ S5 真实门限 = "需先有提交+回测的 alpha"，属设计预期；其 CLI 契约（`--multisim/--alphas`）已在上一轮 dryrun 核对。

## 5. 本次联网实测落库的副作用（可保留/可回滚）

| 产物 | 位置 | 性质 | 建议 |
|---|---|---|---|
| S0 ranking | `ledger_kv/EUR/s0_ranking` |  legitimate S0 产出 | 保留 |
| S1 catalog | `CampaignStore` model238(44f) | legitimate S1 产出 | 保留 |
| 上一轮 wave20 | `expressions/EUR/20`(5) + `gate_results EUR/20` | dryrun 探测产物 | 可回滚（见下） |

上一轮 dryrun 写入的 wave20（5 条跨数据集字段表达式 + gate_results）为探测残留，非真实挖掘产出；
若需回滚：`DELETE FROM expressions WHERE region='EUR' AND wave='20'; DELETE FROM gate_results WHERE region='EUR' AND wave='20';`

## 6. 最终结论

- **平台连接成功**，S0/S1/S6 三个"需平台"步骤用真实平台数据跑通，I/O 与设计一致。
- **S0→S1→S3 用真实数据闭环成立**（scan_fields 写、gate 读同一 CampaignStore）。
- 剩余待正式挖掘时才触发的：S5（需真实提交+回测）、S2/S3/S4 本地步骤（上一轮已真跑）。
- 凭证双源（~/.brain_credentials ↔ .env）均已验证，无单点失效。
- 仍维持上一轮 4 项阈值/缺口结论（margin 15bp / turnover 30% / self_corr 0.7 / 算子数<8 上限门 / prod_corr 真实相关性双闸），需正式开跑前拍板。
