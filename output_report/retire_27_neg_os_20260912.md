# 27 颗负 OS alpha 退役清单（控制台用）

生成时间：2026-09-12 | 账号 `MT38799`
数据来源：实时 `GET /users/self/alphas?stage=OS`（210 颗，OS Sharpe<0 共 27 颗，100% USA、100% ACTIVE）
`s60`（近 60 日 OS Sharpe）、`fam`（因子族）、`dec`（decay）、`neut`（中性化）来自 `research-data/neg_os_diagnosis_2026-08-28.md`（**08-28 快照，已两周**）

---

## 0. 为什么这份清单要手工执行

已实证：**研究 API 无法退役 alpha**。

| 尝试 | 结果 |
|---|---|
| `POST /alphas/{id}/retire` · `/decommission` · `/deactivate` · `/withdraw` · `/unsubmit` · `/archive` · `/hide` | **全部 404**（基线 `POST /alphas/{id}` → 405，证明路由解析正常，404 确系端点不存在） |
| `PUT /alphas/{id}` | 405 Method not allowed |
| `PATCH /alphas/{id} {"status":"DECOMMISSIONED"}` | **200，但响应体与后续 GET 的 status 仍为 ACTIVE** → 服务端静默忽略 |
| `PATCH /alphas/{id} {"status":"RETIRED"}` | 400 `"RETIRED" is not a valid choice`（合法值只有 UNSUBMITTED / ACTIVE / **DECOMMISSIONED**） |
| `PATCH /alphas/{id} {"hidden":true}` | 200，可写且可逆 —— 但 **hidden 只是 UI 眼睛按钮**（官方 Alphas 页说明：点眼睛隐藏，再点恢复），**不改变 status，不停止实盘** |

→ **真退役只能在 BRAIN 控制台操作。**

---

## 1. 执行方式（控制台）— 22 颗已打标签，可直接过滤

**已完成：22 颗建议退役的 alpha 全部打上标签 `RETIRE_20260912`**（`logs/_tmp_tag_retire_22.py`，22/22 成功，checkpoint `logs/_retire_tag_checkpoint.json`）。标签可写、可逆、零实盘影响。

控制台操作：

1. 打开 **Alphas → Submitted**，列设置加勾 **Status / Tags / Sharpe**
2. **Filter → Tags = `RETIRE_20260912`** → 列表收敛到这 22 颗
3. 全选（表头复选框）→ 点 **Retire**（**不是眼睛按钮**）
4. 退完把下表 ✅ 标上；标签事后可用同脚本反向清除

> 若你的控制台 Tags 过滤器不支持多选全选，退回按下方 ID 逐个搜索。

---

## 2. 清单（按 OS 由差到好排序）

图例：**退役** = 建议立即退；**观察** = 近 60 日已转正，原报告建议再看 1–2 个月

| # | id | OS Sharpe | s60@08-28 | IS Sharpe | fam | dec | neut | 当前 hidden | 建议 | 完成 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | kGzKZzl | −1.37 | −2.84 | 1.36 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 2 | nqkbYpz | −1.27 | −2.69 | 1.29 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 3 | vGJrvjz | −1.05 | −2.32 | 1.70 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 4 | vRVNZqrz | −1.01 | −2.40 | 2.26 | fund | 5 | SUBIND | True | **退役** | ☐ **[已打标]** |
| 5 | N19r6q0L | −0.97 | −2.50 | 1.74 | fund | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 6 | Nzqpk1p | −0.91 | +0.07 | 1.32 | mdl177 | 5 | MARKET | False | 观察 | ☐ |
| 7 | eGKGo3O | −0.84 | −0.07 | 1.88 | mdl177 | 5 | MARKET | False | **退役** | ☐ **[已打标]** |
| 8 | vGAagoA | −0.79 | −1.89 | 1.42 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 9 | vGnEQOQ | −0.78 | −0.77 | 1.64 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 10 | l5MdLdx | −0.78 | −2.69 | 1.37 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 11 | 9GpO8or | −0.78 | −1.21 | 1.44 | fund | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 12 | eGrbE7p | −0.76 | −1.05 | 1.53 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 13 | gdolWn0 | −0.71 | −3.29 | 1.28 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 14 | 60qLZ17 | −0.66 | +2.25 | 1.90 | mdl177 | 5 | MARKET | False | 观察 | ☐ |
| 15 | Lr6OvE2 | −0.55 | −2.72 | 1.39 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 16 | KQ6x7El | −0.51 | +3.85 | 1.57 | mdl177 | 5 | MARKET | False | 观察 | ☐ |
| 17 | OM2V3r1 | −0.46 | −0.44 | 1.74 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 18 | ER9rrG1 | −0.42 | +0.31 | 1.86 | fund | 0 | SUBIND | False | 观察 | ☐ |
| 19 | rGOdX8E | −0.39 | −1.75 | 1.74 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 20 | wPnkbWY | −0.33 | −1.27 | 1.38 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 21 | 5eqrE56 | −0.29 | −0.10 | 1.37 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 22 | WLmep9j | −0.29 | +1.82 | 1.65 | fund | 0 | SUBIND | False | 观察 | ☐ |
| 23 | LrqYWGn | −0.23 | −0.25 | 1.44 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 24 | bnMgg1N | −0.21 | −1.28 | 1.27 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 25 | zGabalR | −0.20 | −0.57 | 1.51 | mdl177 | 5 | MARKET | False | **退役** | ☐ **[已打标]** |
| 26 | Amao0qd | −0.14 | −2.02 | 1.67 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |
| 27 | z0oNEa1 | −0.11 | −0.99 | 1.41 | mdl177 | 5 | MARKET | True | **退役** | ☐ **[已打标]** |

**小计：退役 22 颗 / 观察 5 颗（#6 Nzqpk1p、#14 60qLZ17、#16 KQ6x7El、#18 ER9rrG1、#22 WLmep9j —— s60 已转正）**

---

## 3. 一个必须先纠正的认知

**20/27 现在已经是 `hidden=True`，但这没有用。**

这 20 颗正好等于 08-28 报告建议退役的那批 —— 说明此前已经执行过"隐藏"。但：

- hidden 只是 Alphas 列表里的**眼睛按钮**（官方说明：勾选后点眼睛隐藏，再点一次恢复）
- **status 仍是 ACTIVE**，OS Sharpe 仍是负的 → **它们仍在 production book 里跑，仍在拖 CAP/CSAP/vf**
- 所以这 20 颗**仍然需要真正的 Retire**

`hidden` 与 `Retire` 是两个完全不同的动作，别把前者当成后者。

---

## 4. 复算脚本

| 脚本 | 用途 |
|---|---|
| `logs/_tmp_retire_recon.py` | 刷新负 OS 清单（只读） |
| `logs/_tmp_retire_capability.py` | 写能力探测（幂等） |
| `logs/_tmp_endpoint_scan.py` | 退役端点扫描（404/405 判别） |
| `logs/_tmp_decommission_probe.py` / `_probe2.py` / `_put.py` | status 写入验证 |

运行：`world-quant-brain-mcp/.venv/Scripts/python.exe logs/_tmp_xxx.py`
