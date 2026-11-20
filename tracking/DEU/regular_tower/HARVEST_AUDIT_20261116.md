# HARVEST AUDIT — DEU 存量收割收口（2026-11-16）

- 性质：**只读收口档案**。用途=把「今天能交的那一颗」与「整族为什么不能交」钉在纸上，供下一个会话直接引用，不必重跑。
- 触发：用户指令「prod >0.7 不能交 / 收口 / 继续」。执行时战役Ⅱ（`dwfrun-0c8854dd`，insiders）处于 interrupted 状态，相关性单槽空闲。
- 证据来源与**通道盲区**（AGENTS §8.11 ⑦）：
  - 相关系数 = `check_self_correlation`（**本地** OS 池计算，pool 20 / full 24，排除 4 颗 PPAC）与 `check_correlation(production, refresh=False)`（**48h 缓存优先**，非当场回源）。
  - 指标/塔位 = `get_alpha_details`（平台实读）。
  - 逐年 = `get_alpha_yearly_stats`（平台实读）。
  - 本地 DB 队列 = `get_submit_ready(DEU, READY)`；**盲区**：该队列 `prod/self` 多为 null，且 `towers` 字段全为 `[]`（本地不做塔级归属）⇒ 塔位一律以平台 `pyramids.list` 为准。

## 一、可交付：`XgaGb3J1`（唯一一颗）

| 轴 | 读数 | 闸 | 判定 |
|---|---|---|---|
| S / F | **2.36 / 2.02** | 1.58 / 1.0 | ✅ |
| 2Y（单集件载体 IS_LADDER） | **2.71** | 1.58 | ✅ |
| sub | 1.51 | 1.0 | ✅ |
| TO / margin / DD | 17.38% / 14.66bp / 7.65% | 0.01–0.70 / ≥5bp | ✅ |
| RA | `failed_ra_count=0`、`checks.fail=[]` | — | ✅ |
| **塔位** | `[{DEU/D1/INSIDERS,1.6},{DEU/D1/MODEL,1.8}]`，**effective=2** | 禁混 | ✅ 两类别（MODEL+INSIDERS 非 trio 内部两两） |
| self | **0.6784**（vs `Vk65zLzG`） | <0.70 | ✅（余量仅 0.022） |
| prod | **0.6784**（缓存 `2026-11-16T17:18`） | <0.70 | ✅（余量仅 0.022） |
| robustness | 已记录 PASS（战役Ⅱ 链内） | 无 REJECT | ✅ |
| submit_verdict | `UNVERIFIABLE`（404 端点） | — | ⚪ 未提交件的**正常**结果，非失败 |

**提交后的塔位增量（条件式）**：若被平台计入 → insiders 1/3 → 2/3；MODEL 已亮（3），不再增值。

**交付前必做（未做，我不越权）**：
1. `check_correlation(refresh=True)` **当场终验 prod** —— 0.6784 距 0.7 仅 0.0216，而 prod 漂移实测上界 +0.43，缓存值不足以下结论；
2. 用户明确确认 + `workflow_submit_alpha(confirm_submit=True)`（不可逆）。

## 二、不可交付：整族 10 条（PV+MODEL 禁混，effective=0）

这一批是**并行会话**今天 11:03–13:17 产出的 insiders 家族（与 `XgaGb3J1` 同源）。指标普遍更高，但塔位被判死：

| alpha | S / F | 2Y | prod | self | pyramids | effective |
|---|---|---|---|---|---|---|
| `1YWnZ9rK` | 2.64 / 2.17 | 2.86 | 0.5485 | 0.5487 | PV + INSIDERS + MODEL | **0** |
| `2r5MO67Z` | 2.63 / 2.13 | 2.94 | 0.5534 | 0.5535 | PV + INSIDERS + MODEL | **0** |
| `O0W5JdMg` | 2.64 / 2.17 | 2.86 | — | — | 含 `bucket(rank(cap))` | 0（按 code 判） |
| `58JqE0kk` / `oma9apvk` | 2.64 / 2.17 | 2.86 | — | — | 同上 | 0（按 code 判） |
| `XgaYzWX1` / `Jj85zO52` | 2.60 / 2.11 | 2.77 / 2.94 | — | — | 同上 | 0（按 code 判） |
| `A1xOzwdR` | 2.53 / 2.08 | 2.52 | — | — | 同上 | 0（按 code 判） |
| `88NKJOav` | 2.60 / 2.12 | 2.77 | — | — | 同上 | 0（按 code 判） |
| `6XM7ARLE` | 2.37 / 2.11 | 3.14 | — | — | 同上 + oth455 第四塔 | 0（按 code 判） |

- **根因**：`bucket(rank(cap), …)` 把 `cap`（PV）挂进塔位，与 `predicted_surprise_* / mean_estimate_change_*`（平台归 MODEL）组成 **PV+MODEL** ⇒ 违反用户 Goal 约束第 7 条（trio 内部两两禁混）。同一形态在 `COMPLIANCE_PV_MODEL_REDLINE_20261112.md` 已作废过 7 颗 fail=0 件（BE138）。
- **三层代价**：①合规上不能交；②即使硬交，`effective=0` ⇒ 点塔计数归 0（白烧配额）；③与 `XgaGb3J1` 两两 0.906–0.983，`max_mutually_below_subset` 仅 1 条 ⇒ **同族只可能交一颗**。
- **判定口径**：`1YWnZ9rK`/`2r5MO67Z` 为平台实读；其余 8 条按 **code 文本含 `bucket(rank(cap)`** 判定（**未逐条实读 pyramids**，属代码级推断——若要动用其中任何一条，必须先 `get_alpha_details` 复核）。

## 三、不可交付：`kqNRX1ZP`（sentiment 塔唯一存量件）

| 轴 | 读数 | 判定 |
|---|---|---|
| S / F / 2Y / sub | 2.06 / 1.86 / 2.37 / 1.49 | ✅ |
| RA | `failed_ra_count=0` | ✅ |
| 塔位 | `[{DEU/D1/SENTIMENT,1.8}]`，effective=1 | ✅ 纯单塔 |
| **self** | **0.7936**（vs `bl6OWZ2M`） | ❌ **撞墙，不再测 prod** |
| 近十年 | **2014–2018 五年 LC/SC=0、pnl=0**；2019–2023 有仓，2020 S 0.47、2023 S 0.60 | ❌ 严格口径；且 2.06 实为 2021(2.96)+2022(4.55) 两年扛起 |

- 双重否：self 0.79 已足够枪毙；「5 年数据」这一条本身另有先例（论坛 USA/EUR/HKG 用 5 年数据提交 ACTIVE），但**不影响结论**——self 先死。

## 四、口径提醒（写下来防下一次踩）

1. **`get_submit_ready.towers` 恒为 `[]`**，不能用来判塔；`alphas` 表也不能做塔级统计。
2. **`bucket(rank(cap))` 是隐形 PV 挂靠**：点塔场景里它是污染源，不是中性化工具；要市值条件化改用 `group_neutralize(..., bucket(rank(<本集内字段>)))` 或直接换分组轴。
3. **prod/self 同时等于同一个值**（本例 0.6784）是正常的：`Vk65zLzG` 同时在 OS 池与生产池里，两个口径各自的最大值都来自它。
4. 缓存值只用于排序与初筛；**提交前必须 refresh=True 终验**。

## 五、战役Ⅱ 跑完后的复核（2026-11-16 22:33，本节推翻/限定上面 §一 的乐观结论）

战役Ⅱ（`dwfrun-0c8854dd`，4 波 40 臂，best S 0.81/0.89/0.78/0.89）把 `XgaGb3J1` 送进提交链，链上给出的**篮内互相关 = 0.9936**，据此判 `blocked`。

**但这个 0.9936 我复现不出来**，实测（`compute_mutual_correlation`，4y，1021 点）：

| 对照集 | 与 `XgaGb3J1` 的相关 |
|---|---|
| `1YWnZ9rK` / `2r5MO67Z` | 0.906 / 0.9157 |
| `d5aE63Ew` / `gJaR5gov` / `LLKnekRL` / `MP6bwkGM`（本 run 四波候选） | 0.5999 / 0.5664 / 0.4316 / 0.4741 |
| `max_mutually_below_subset`（XgaGb3J1 + 本 run 四候选） | **{gJaR5gov, XgaGb3J1, LLKnekRL}，size=3** |

- 本 run 里唯一 >0.7 的近重复是 **`d5aE63Ew × gJaR5gov` = 0.9636**（0.9936 很可能是这项的误抄/另一对的错配，**报告正文没有记录它的对照对象**，`CAMPAIGN_REPORT_INSIDERS_20261116.md` 明确声明「`XgaGb3J1` 不在本 run 40 臂内，不转录不作依据」）。
- ⇒ `XgaGb3J1` 的**篮内互相关仍未取得可信读数**；它既未被证实可交，也**没有被 0.9936 正当地否掉**。
- 要收口，需一步：对**已提交篮**跑 `compute_mutual_correlation([XgaGb3J1] + <18 席篮>)`，并同时 `check_correlation(refresh=True)` 终验 prod。

**同批其余状态（run 结论原文）**：
- `MP6bwkGM`（塔 insiders+institutions）prod 干净但因「每波 1 条链名额」**未入链** ⇒ 从未做过塔位/RA 复核。
- `0mPKr3bq`：self 0.6714（过）但 **prod 取不到**——5 轮 pending 触发账号级熔断 `platform_unavailable`，期间平台单并发槽被他会话占（`leaQ2MN5` / `blaoQ6Kq` / `gJaR8e0J`）⇒ 属可用性故障，需稍后重跑，**不是闸门结论**。

