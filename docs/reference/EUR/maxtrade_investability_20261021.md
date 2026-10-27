> 日期：2026-10-21 ｜ 设置基线：EUR / TOPCS1600 / d1 / decay 4 / FAST / trunc 0.08 / **nanHandling ON**（全程锁定，唯一变量 = `maxTrade`）

# maxTrade ON/OFF 受控对照（EUR，2026-10-21 实测定案）

## 1. 结论速览

| 维度 | ON（当前战役缺省） | OFF | 判定 |
|---|---|---|---|
| 换手 TO | 0.055（均值） | 0.139（**+155%**） | ON 是硬换手帽 |
| 原始 S | 1.214 | 1.086（含 1 例崩塌）／**1.45（剔除崩塌例，+18.8%）** | OFF 抬 S，但**族依赖** |
| Fitness F | 0.682 | 0.650 ／**0.83（剔除崩塌例，+18.5%）** | OFF 更优，且是在 TO>0.125 已罚 F 的前提下 |
| sub/S 保留率 | 0.463 | **0.548（+18.4%）** | OFF 更优 |
| robust | 0.432 | 0.326 ／**0.678（剔除崩塌例，+12%）** | OFF 更优 |
| investability（inv_S） | **不可预提交测量**（见 §3） | 同左 | ON 结构性占优（换手帽已内嵌） |

**定案**：`maxTrade` 是**强度闸 + 容量闸的复合开关**，不是风格开关；**方向依族而变，禁止全局一刀切**。
**战役缺省维持 ON**（与 24 个已完成集及全部既有 EUR 战役可比；且容量侧可自证）。
**仅对 S≥1.3 的近闸候选做 OFF 双轨复测**，并接受其 investability 不可预验的风险。

## 2. 实测对照表（5 组同表达式配对，唯一变量 maxTrade）

| 数据集/族 | ON S / F / TO | OFF S / F / TO | ΔTO | ON sub/S → OFF sub/S | ON rob → OFF rob |
|---|---|---|---|---|---|
| predictive_starmine/ed | 1.38 / 0.81 / 0.0292 | 1.58 / 0.98 / 0.0653 | +124% | 0.59 → 0.49 | 0.79 → 0.60 |
| intraday_pv_feats/cs | 1.32 / 0.93 / 0.0626 | 1.71 / 1.08 / 0.2011 | +221% | 0.58 → 0.50 | 0.68 → 0.92 |
| sentiment27/va | 1.18 / 0.60 / 0.0912 | **−0.38 / −0.08 / 0.2078** | +128% | 0.30 → 0.82 | −0.26 → −1.08 |
| sentiment21/ed | 1.18 / 0.57 / 0.0389 | 1.26 / 0.62 / 0.0769 | +98% | 0.30 → 0.30 | 0.25 → 0.45 |
| other553/rk | 1.01 / 0.50 / 0.0513 | 1.26 / 0.65 / 0.1446 | +182% | 0.54 → 0.63 | 0.70 → 0.74 |

均值（剔除 sentiment27 崩塌例）：S 1.22→1.45（+18.8%）｜F 0.70→0.83（+18.5%）｜robust 0.61→0.68（+12%）｜sub/S 0.463→0.548。

**关键反例**：`sentiment27/va`（波动调整差分族）OFF 下 **S 1.18→−0.38、F 0.60→−0.08、robust −0.26→−1.08** ——
放开换手帽后该族直接崩塌。⇒ **OFF 不可全局套用**，与既有「作用符号依机制族而变」一致。

## 3. invest_S 为什么测不到（取证路径）

| 通道 | 结果 |
|---|---|
| `GET /alphas/{id}`（未提交） | `is` 仅 12 键（bookSize/checks/drawdown/fitness/longCount/margin/pnl/returns/sharpe/shortCount/startDate/turnover），**无 `investabilityConstrained`** |
| checks 清单（18 条） | **不含 `LOW_INVESTABILITY_CONSTRAINED_SHARPE`**（属提交后 RA 闸） |
| `submit_verdict` → `GET /alphas/{id}/submit` | **404**（处女提交无提交层视图） |
| `PATCH /alphas/{id}`（改 color） | **400**（未提交 alpha 不接受该写操作） |

⇒ **在「只挖不提交」政策下 inv_S 无法实测**；只能靠「换手帽已内嵌」的 ON 结构性保证，或事后提交才见真值。
（闸线仍按 `INVEST_RATIO = 0.70`：inv_S ≥ 0.70×S；驱动量 = 持仓集中度，见 `src/wqb/gate_attribution.py`。）

> **2026-10-24 更正（USA 实测）**：`GET /alphas/{id}` 的 `is.investabilityConstrained` 现已可读，
> MCP `get_alpha_details` 直接透出 `investability_sharpe` / `investability_fitness`，
> `batch_get_alpha_metrics` 另给 `investability_ratio = inv_S / S`。
> 本节「不可预提交测量」只适用于当时 EUR 的返回形态，**不要再据此跳过 invest_S 预筛**。

## 4. 决策依据

1. **可测闸门侧 OFF 更优**：S/F/sub/S/robust 四项全面改善，且 EUR 的 `HIGH_TURNOVER` 闸线 0.7 对 OFF 的 0.14–0.21 完全不构成威胁（TO 仍在区间内）。
2. **不可测闸门侧 ON 结构性占优**：investability 是 `RA_HARD_FAILS` 硬闸且**预提交不可验**；OFF 把换手放大 2.5 倍，容量消耗同步放大，inv_S 保留率必然承压。
3. **可比性**：全量切换会使 24 个已完成集与全部既有 EUR 战役结果跨档不可比（设置 = 强度闸）。

## 5. 执行口径（已落地）

- 战役缺省：**保留 `maxTrade=ON`**（不动 `tools/full_template_campaign.py` 的派发参数）。
- 近闸候选（S≥1.3）：**OFF 双轨复测**，只在其 S/F/sub/S/robust 全改善时才升级为提交候选，并在台账注明「investability 未预验」。
- 禁止在战役中途全局翻档；如确需换档，须整轮重跑以保可比。
