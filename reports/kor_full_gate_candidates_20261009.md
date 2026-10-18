# KOR/D1 挖掘状态报告（2026-10-09 17:00 更新）

> 判定依据：MCP `get_alpha_details`（`ra.ra_failed_checks` + `checks`）与
> `brain.check_correlation(id, correlation_type="production", refresh=True)`（prod 真值）。
> **提交权在用户**；本报告不含未授权动作。

---

## 一、当前可提交候选 = **0 颗**

| 族 | alpha | S | F | 2Y | self | **prod** | 判定 |
|---|---|---|---|---|---|---|---|
| SHORTINTEREST（**已点亮**）| 6XKw22MJ | 2.87 | 2.78 | 2.69 | 0.33 | **0.982** | ❌ prod |
| | JjQp22ee / LLZ1V5b9 / 58gw22Ao | 2.65/2.63/2.68 | 2.40/2.38/2.45 | — | .46/—/.47 | **0.876/0.866/0.861** | ❌ prod |
| | 0mr7aagv / 786w22GQ / KPr9lmeN | 2.30/2.55/2.01 | 1.91/2.35/1.60 | — | .46/.51/.28 | **0.818/0.815/0.710** | ❌ prod |
| FUNDAMENTAL（**已点亮**）| RR6EEngd / wpbQoJ3l | 1.65/1.64 | 1.44/1.42 | 1.62/1.67 | .49/.50 | **0.799/0.783** | ❌ prod |
| | P0goodLp / WjeOO6ZG / 3qVooZK6 / 0mrYPKxk | 1.64~1.49 | 1.39~1.23 | — | .47~.49 | **0.818/0.818/0.799/0.776** | ❌ prod |

**全部 13 颗 prod ≥ 0.7** ⇒ 按用户铁律不可提交。
其中 **6XKw22MJ（prod 0.982）是论坛已提交 alpha 的近重复** —— 复刻公开配方必然撞 prod。

## 二、已提交（3 颗，OS 池内）
`O08kz5Mv`(SHORTINTEREST) · `gJZR9XNm`(MODEL) · `0mre68gv`(MODEL)

## 三、未点亮塔（12 个）本轮全扫 —— 无一产出

| 0 塔 | 本轮/历史最强 | 死因 |
|---|---|---|
| **ANALYST** | 单腿 S 1.07 | 加价格腿 2Y 0.28–1.21；加新闻腿 TO 1.2；`group_zscore` 更弱（0.92）|
| **RISK**（`dsrt`）| **S 2.01** | **TO 0.83**；慢设置 → TO 0.30 但 S 0.48 |
| **PV**（`pv47_spret`）| **S 2.75** | **TO 恒 0.82**（462/1008/2016 窗口均不降）；decay20 → TO0.44/S1.10/2Y−0.17 |
| **INSTITUTIONS**（`institutions6` 流量 + `fund_holdings_panel`）| 0.97 / 0.46 | 全弱 |
| INSIDERS | 1.07 | 弱 |
| IMBALANCE | 1.24 | 仅 2 字段，换档更弱 |
| EARNINGS / MACRO / SOCIALMEDIA / SENTIMENT / NEWS / OTHER | ≤0.72 | 全弱 / 覆盖低 |

## 四、两条结构性障碍（本会话实证）

1. **TO 墙**：KOR 唯一强信号族「特质收益反转」（RISK 与 PV 同源）**结构性高换手 TO≈0.82**，
   任何窗口 / 平滑 / 设置手段**都不能同时保住 S** ⇒ 三闸（S≥1.58 / TO≤0.7 / 2Y≥1.58）互斥。
2. **prod 墙**：KOR 是全球重度挖掘区，**13/13 候选 prod ≥ 0.7**。IS 全过 ≠ 可提交。

## 五、建议下一步（待用户决策）
1. **`trade_when` 门控降 TO** —— 唯一未试的 TO 杠杆（只在信号极端时交易，理论上压 TO 而保留 S）。
2. **跨塔组合**（特质收益 × 慢信号）用慢腿压 TO —— 注意跨塔名称会融合、且须重验 prod。
3. **下调 KOR 产出预期**（或换区，但用户当前锁定 KOR）。
