# 模板拼接的两个致命 bug（本轮连犯两次）

日期：2026-11-12

## Bug 1：裸变量名混入表达式 ⇒ `unknown variable"

**现象**：BE166 那批 3 臂报 `Attempted to use unknown variable "h"`，另 7 臂被连坐 CANCELLED。

**根因**：我用 JS 模板字符串拼表达式时，某条腿写成了：
```js
const F = `group_rank(divide(1,add(days_from_last_change(h),1)),sector)`;   // ❌ 裸 h
```
本应是 `days_from_last_change(${H})`。裸 `h` 让表达式里出现字面量变量名 `h`，
而表达式本身没有 `h=...` 的赋值语句 ⇒ 平台报 `unknown variable "h"`。

**修法**：模板变量必须写 `${H}`（带美元符和花括号），不能写 `h`。

**防护**：派发前跑正则自检：
```js
const bad = arms.filter(([k,e]) => /[^_\w]h[^_\w]|\(h\)|,h\)/.test(e));
if (bad.length) return { blocked: bad.map(b=>b[0]) };
```

## Bug 2：字段塔归属未查 ⇒ 整批违规

**现象**：BE163 做出 `Jj8q3XJ2`（S 1.87 / F 1.62 / sub 1.34 / 相关性仅 0.5778），
却因塔含 `INSIDERS+MODEL+OTHER`（MODEL 与 OTHER 两个 trio）而违规作废。

**根因**：派发前没查「表达式用到的字段各属哪个塔」。

**防护清单（每次派发前必查）**：

| 字段前缀 / 名 | 塔 | trio？ |
|---|---|---|
| `cap` | **PV** | ✅ trio |
| `predicted_surprise_*` / `mean_estimate_change_*`（predictive_starmine）| **MODEL** | ✅ trio |
| `oth455_*` | **OTHER** | ✅ trio |
| `est_12m_*_raisednum_*` / `est_12m_*_raised_*` / `rec_raisednum_*`（analyst7）| ANALYST | ❌ 安全 |
| `insd1_*` / `significant_value_*` | INSIDERS | ❌ 安全 |
| `nws*_*` / `mws50_*` | NEWS | ❌ 安全 |
| `count_institutional_*` / `market_value_institutional_*` | INSTITUTIONS | ❌ 安全 |
| `snl27_*` / `snt27_*` | SENTIMENT | ❌ 安全 |
| `shrt3_*` / `max_loan_rate_*` / `rsk60_*` | SHORTINTEREST / RISK | ❌ 安全 |

**规则**：`PV` / `MODEL` / `OTHER` 三者**最多出现一个**。

**⚠ 关键陷阱**：`predictive_starmine` 的字段**名字像 analyst，实际属 MODEL**。
所以 `oth455_*(OTHER) + predicted_surprise_*(MODEL)` 必然违规，
而 `est_12m_ebi_raised_*(ANALYST) + oth455_*(OTHER)` 合规。

## 累计损失

因这两个 bug 作废的波次：BE151（group_rank 参数错）、BE161 首派（字段名错）、
BE165（拼写/塔混用）、BE166 首派（裸 h）、BE163 的 Jj8q3XJ2（塔违规）。

⇒ **每个 bug 都浪费一个 multisim 配额**。全批连坐是主要损失来源：一条错、十条死。