# ★合规铁律的第二次拦截：OTHER + analyst 组合必然违规

日期：2026-11-12

## 一、事件

BE163 做出 `Jj8q3XJ2`（O4×2 + AS3 + A）：**S 1.87 / F 1.62 / 2Y 2.06 / sub 1.34 / fail=[]**，
与篮子的最大相关仅 **0.5778**（vs npa9PKWw），独立集可达 16。

但塔归属是 **INSIDERS + MODEL + OTHER** ⇒ **MODEL 与 OTHER 两个 trio 成员并存 ⇒ 违规**。

这是合规约束**第二次**拦截高指标件（第一次是 `6XM7ARLE` S 2.37，塔含 PV+OTHER）。

## 二、提炼出的合规铁律（第三次验证）

**一个表达式里最多只能出现一个 trio 成员（PV / MODEL / OTHER）。**

因此**合规的跨类组合只有以下形态**：

| 形态 | 例子 | 合规 | 塔 |
|---|---|---|---|
| insiders + OTHER（**不含 analyst/MODEL**）| npa9PKWw | ✅ | INSIDERS+OTHER |
| insiders + analyst/MODEL（**不含 OTHER**）| d5apW38x, d5ap9Akx | ✅ | INSIDERS+MODEL |
| insiders + cap(PV) + analyst | WjlMlWJd | ✅ | PV+INSIDERS+ANALYST |
| insiders + cap(PV) + OTHER | ❌ | **PV+OTHER 违规** | |
| insiders + OTHER + analyst | ❌ | **MODEL+OTHER 违规** | |
| insiders + cap + OTHER + analyst | ❌ | 双重违规 | |

## 三、操作检查清单（派发前必查）

1. 列出表达式用到的所有字段 → 反查每个字段属哪个塔
2. 统计 trio 成员个数（PV / MODEL / OTHER）
3. **>1 ⇒ 不派发**（省一个 multisim 配额）
4. 特别注意：
   - `cap` = **PV**（最容易被无意引入）
   - `predicted_surprise_*` / `mean_estimate_change_*` / `est_12m_*` = **MODEL**
   - `oth455_*` = **OTHER**
   - `est_12m_ebi_raisednum_*` / `rec_rawnum_*`（analyst7）= **ANALYST**（非 trio，安全）
   - `insd1_*` / `significant_value_*` = **INSIDERS**（非 trio，安全）
   - `nws*_*` / `mws50_*` = **NEWS**（非 trio，安全）
   - `count_institutional_*` = **INSTITUTIONS**（非 trio，安全）
   - `shrt3_*` / `max_loan_rate_*` = **SHORTINTEREST**（非 trio，安全）

## 四、这个约束的实际代价（本战役累计）

| 被拦截的件 | S | 违规原因 |
|---|---:|---|
| 6XM7ARLE | **2.37** | PV + OTHER |
| Jj8q3XJ2 | **1.87** | MODEL + OTHER |
| 2r5MO67Z | **2.63** | PV + MODEL |
| d5apOzxj | 1.59 | PV + MODEL |

**四颗 S≥1.59 的强件全部因 trio 冲突作废**，合计损失约 8.5 的 S 值潜力。
⇒ 这条约束是当前最大的产出瓶颈之一。