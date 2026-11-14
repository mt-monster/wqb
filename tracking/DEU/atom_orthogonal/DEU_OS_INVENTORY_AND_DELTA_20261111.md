# DEU 已提交件权威清单与交付纠正（2026-11-11）

> 触发原因：提交前逐件重算 self 相关时，E569ZE7L 读出 **self=1.0000（pass=False）**，
> 对端 78Yk8VR1。追查后确认本轮台账的「2 颗 ACTIVE + 5 颗待提交」严重低估了已提交存量。

## 一、DEU 已提交（OS）全量 = 20 颗 ACTIVE

`get_user_alphas(stage="OS", region="DEU", limit=60)` 实测，按提交日期倒序：

| alpha | 提交日 | S | F | 2Y | 塔 |
|---|---|---:|---:|---:|---|
| **78Yk8VR1** | **2026-11-10** | 1.68 | 1.21 | 2.27 | SHORTINTEREST |
| rKRx2Alj | 2026-11-09 | 1.95 | 1.80 | 2.23 | MODEL+ANALYST |
| zq3eb7No | 2026-11-08 | 2.01 | 1.28 | 1.64 | ANALYST |
| bl6AvMkN | 2026-11-07 | 1.61 | 1.36 | 2.15 | MODEL+ANALYST |
| vR1oxZA3 | 2026-11-07 | 3.27 | 3.09 | 4.39 | （无塔标记） |
| GrW9OxmG | 2026-11-07 | 1.62 | 1.56 | 1.93 | ANALYST |
| bl6OWZ2M | 2026-11-04 | 2.03 | 1.61 | 2.54 | SENTIMENT |
| LLM93nGa | 2026-11-03 | 1.88 | 1.74 | 2.25 | SHORTINTEREST+ANALYST |
| xArzm3Mn | 2026-10-31 | 1.64 | 1.33 | 2.39 | SHORTINTEREST |
| mLYLEm99 | 2026-10-18 | 2.27 | 1.67 | 2.71 | （无塔标记） |
| 2rjrMZ25 | 2026-10-13 | 1.77 | 1.61 | 1.83 | ANALYST |
| Wje5K71x | 2026-10-12 | 1.73 | 1.37 | 1.87 | FUNDAMENTAL |
| 2rmGAPqN | 2026-10-09 | 1.81 | 1.48 | 2.55 | INSTITUTIONS+OTHER |
| 58gkLAkk | 2026-10-07 | 1.75 | 1.42 | 2.07 | MODEL+OTHER |
| JjxrYjre | 2026-09-14 | 1.68 | 1.47 | 1.69 | MODEL+OTHER |
| 2rOe10qY | 2026-09-14 | 2.10 | 1.98 | 2.19 | MODEL+OTHER |
| vRk6og8b | 2026-09-13 | 1.80 | 1.47 | 2.10 | SHORTINTEREST+MODEL |
| Vk65zLzG | 2026-09-13 | 1.79 | 1.69 | 2.07 | INSIDERS+MODEL |
| 883Y3bAW | 2026-09-13 | 2.17 | 1.24 | 2.09 | MODEL |
| blRnKEk6 | 2026-09-13 | 2.02 | 1.70 | 2.74 | SHORTINTEREST+MODEL |

⇒ self 池 `pool_size=17`、`full_os_pool_size=20`（扣除 3 个 power pool 件）。

## 二、★E569ZE7L 作废：它是 78Yk8VR1 的重复件

**证据（三重一致）**：
1. `check_self_correlation(E569ZE7L)` → **max_correlation = 1.0000，passes_check = False**，top = (78Yk8VR1, 1.0)
2. 78Yk8VR1 `get_alpha_details` → status=**ACTIVE**，dateSubmitted=**2026-11-10T05:16:33-05:00**
3. 指标逐项相同：E569ZE7L = S1.68 / F1.21 / TO0.1128 / sub0.86 / 2Y2.27；78Yk8VR1 = **完全相同**

⇒ 78Yk8VR1 已把该表达式提交上线，E569ZE7L 是平台上同一表达式的另一个 alpha 记录。
**处置：E569ZE7L 从交付篮子移除，永不提交（self 1.0 必然被拒）。**
**台账旧记「E569ZE7L self 0.544 / prod 0.5444 PASS」失效**——0.544 是另一对（对 xArzm3Mn）的历史读数，非当前最大值。

## 三、交付篮子修正：7 颗 → **6 颗**

| # | alpha | 塔 | S | F | 2Y | sub | TO | self | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | zq3eb7No | ANALYST | 2.01 | 1.28 | 1.64 | 1.00 | 0.226 | 0.364 | ✅ ACTIVE |
| 2 | bl6AvMkN | MODEL+ANALYST | 1.61 | 1.36 | 2.15 | 0.94 | 0.110 | 0.514 | ✅ ACTIVE |
| 3 | RREPm361 | ANALYST | 2.02 | 1.25 | 1.82 | **1.24** | 0.251 | 0.3275 | 🟡 待提交 |
| 4 | 1YNMAA8M | MODEL+ANALYST | 1.58 | 1.36 | 2.13 | 1.01 | 0.134 | **0.6946** | 🟡 待提交（贴线） |
| 5 | qM7KxkQV | SHORT+INSIDERS | 1.72 | 1.34 | 2.43 | 0.92 | 0.143 | 0.5429 | 🟡 待提交 |
| 6 | Jj8VQwoe | SHORT+OTHER | 1.65 | 1.24 | 2.42 | **1.22** | 0.147 | 0.5645 | 🟡 待提交 |

- 六件互相关全对 <0.7（最大对 zq3eb7No~RREPm361 = 0.6879）。
- **1YNMAA8M 的 self 0.6946 对端是 rKRx2Alj（已 ACTIVE，S1.95）**，余量仅 0.0054 ⇒ 平台池漂移即失效，提交前必须重算。
- 1YWqzPGQ（SHORT×OTHER，S1.59/2Y2.81，2016 -1.00）与 Jj8VQwoe 互相关 0.8924 ⇒ 只取 Jj8VQwoe（S/F/sub/TO/最差年均更优，仅 2Y 更低）。wpo8ZQN6 与 qM7KxkQV 0.935 ⇒ 备选存档。

## 四、塔位实况（按 20 颗 OS 反推）

| 塔 | 已提交 | 点亮 |
|---|---:|---|
| ANALYST | 8 | ✅ |
| MODEL | 7 | ✅ |
| OTHER | 4 | ✅ |
| SHORTINTEREST | 5 | ✅ |
| SENTIMENT | 1 | ❌ |
| FUNDAMENTAL | 1 | ❌ |
| INSTITUTIONS | 1 | ❌ |
| INSIDERS | 1 | ❌ |
| 其余（NEWS/EARNINGS/RISK/OPTION/PV/MACRO/IMBALANCE/SOCIALMEDIA） | 0 | ❌ |

⇒ 提交 qM7KxkQV 使 INSIDERS 1→2；提交 Jj8VQwoe 使 OTHER 4→5（OTHER 早已点亮）。
**旧的「OTHER 2→3 点亮」判断作废**——OTHER 实际已有 4 颗。

## 五、教训（写入方法论）

**提交前必须做「重复件核对」**：`get_user_alphas(stage="OS", region=<区域>, limit=60)` 拉全量已提交清单，
再用 `check_self_correlation` 逐件看 top 对端；**self=1.0 ⇒ 重复件，立即作废**。
只靠「模拟时 checks.pending 里的 SELF_CORRELATION」会漏掉存量重复，因为模拟时点自池可能不同。
