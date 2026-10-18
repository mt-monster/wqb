# Osmosis Scope 资格重算（平台真实数据）— 2026-10-09

## 背景
用户指出上一轮 Osmosis 刷新（0.695 exclude）只产出 4 个达标范围（IND/MEA/KOR/USA），缺少 GBR/DEU，
并纠正：**不应从本地 DB 取数，应从平台拉真实提交的 alpha 再归类重算**。
此前基于本地 DB 的 `_scope_diag.py` 给出 GBR D1「差 2 颗」、DEU D1「差 5 颗」的诊断 —— 已被证伪。

## 方法（平台真相）
- `brain_client.get_user_alphas(stage="OS")` 全量分页（跟随 `next`，**不用 status 客户端过滤**以规避其 1000 条扫描上限）。
- 本地过滤 `status=="ACTIVE"` 且 `type=="REGULAR"`。
- 按 `(region, delay)` 归类；delay 实测**全部为 1**（156 颗全 D1，无 D-1/其他）。
- 合格口径与刷新一致：`prod` 非 None 且 `< 0.695`（排除模式）。

## 平台真实结果（OS 池 291 → ACTIVE+REGULAR 156）

| Scope | active | eligible(<0.695) | 排除(prod≥0.695) | 达标(≥10) |
|-------|-------:|-----------------:|-----------------:|:---------:|
| IND D1 | 27 | 27 | 0 | ✅ |
| USA D1 | 38 | 34 | 4 | ✅ |
| MEA D1 | 19 | 18 | 1 | ✅ |
| KOR D1 | 24 | 15 | 9 | ✅ |
| **GBR D1** | **13** | **10** | **3** | **✅（边界）** |
| GLB D1 | 10 | 9 | 1 | ❌ (9) |
| ASI D1 | 8 | 8 | 0 | ❌ |
| HKG D1 | 6 | 6 | 0 | ❌ |
| DEU D1 | 6 | 6 | 0 | ❌ |
| EUR D1 | 5 | 5 | 0 | ❌ |

**平台侧达标范围 = 5 个**：IND D1 / USA D1 / MEA D1 / KOR D1 / **GBR D1**。

## GBR D1 逐颗（确认边界安全）
被排除 3 颗（全部仅略高于阈值）：`E5p2r7VL=0.6967`、`A1G7o1EE=0.6971`、`rKO0GOVj=0.6986`。
合格 10 颗最高 `WjAV89jG=0.6882` → 阈值 0.695 与两侧各有 ~0.009 缓冲，达标稳健（但正好卡在 ≥10 边界，任何 1 颗失效即跌出）。

## 纠正：上一轮 4 范围刷新为什么漏了 GBR
- 刷新脚本 `osmosis_allocate.py` 的 `load_candidates()` 从**本地 DB**（`alphas`/`alpha_corr_cache`）取候选，而非平台。
- 本地 DB 把 GBR D1 漏记：DB 口径 ACTIVE=10 / eligible=8（差 2 才到门槛）→ 刷新据此判定 GBR 不达标剔除。
- **平台真相**：GBR D1 ACTIVE=13 / eligible=10 → 实际达标，应纳入。
- 这是「本地 catalog 是时点快照、存在性只信平台」纪律的又一次实证。

## 附带发现：刷新用的计数本身也是 stale DB
刷新落盘计数的本地 DB 合格数与平台对照（差距显著，说明候选池不完整）：

| Scope | 刷新用(本地DB) | 平台真实 | 差异 |
|-------|---------------:|---------:|-----:|
| IND D1 | 24 | 27 | -3 |
| USA D1 | 18 | 34 | **-16** |
| MEA D1 | 19 | 18 | +1 |
| KOR D1 | 17 | 15 | +2 |

→ USA 尤其被严重低估，意味着 0.695 刷新的点数分配基于错误候选集，需重做。

## DEU：确实不达标（两边一致）
DEU D1 平台仅 6 active（6 eligible），无论平台还是 DB 都远低于 10 → 没进是正确的，无需纳入。

## 建议的修复路径（需用户确认后再执行）
1. `python tools/sync_platform_alphas.py` —— 先把平台 OS 池同步进本地 DB（补齐缺失 GBR 等、校正 prod）。
2. 重跑 `python tools/data-repair/osmosis_allocate.py --prod-policy exclude --prod-max 0.695 --apply` —— 此时候选池正确，应产出 **5 范围**（含 GBR D1），且 USA/IND 计数更准。
3. 注意：重新 `--apply` 为平台真实 PATCH 动作（改 Osmsosis 点数、把非计划 alpha 零化），属用户决策项，不自动执行。
