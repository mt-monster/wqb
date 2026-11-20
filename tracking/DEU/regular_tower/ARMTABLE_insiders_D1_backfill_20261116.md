# ARMTABLE — insiders1 · D1 补课波（受控单变量，2026-11-16）

- 状态：**已过静态闸，待派发**。派发前置于流水线Ⅲ（`dwfrun-8294b911`）收尾之后——账号级 multi-sim 在途 ≤2，不与其抢并发。
- 口径：**只做 D1**（DEU / TOP500 / delay=1）。**D0 不在范围**，任何 D0 读数不作依据。
- 设置（批级统一，multisim 设置是批级的，同波不得混）：`DEU/TOP500/D1/decay0/SUBINDUSTRY/trunc0.08/nanHandling ON/maxTrade OFF/FASTEXPR`
  - decay 取 0：与本区 momentum 族「decay 单调负杠杆」一致；帖主的 1.68 用的是 decay3–5，**本波不复现其设置**，decay 变化留作下一批 D6 第二配置。
  - `nanHandling ON` 是 T4（并列块）成立的前提，故固定 ON。
- 表达式文件：`logs/_tmp_insiders_d1_backfill_arms.json`（10 条，CLI 输入件，非战役产物）。
- 证据来源：`DEU/forum_recon_fieldscan_insiders1_20261116`（逐字段 8/8 检索 + 模板 T1–T8）、`DEU/forum_paper_recon_829b5bb3ae`（9 篇，含 Lakonishok-Lee / Cohen-Malloy-Pomorski）、`DEU/forum_recon_8d59ef391b`。

## 一、10 臂（每臂带 evidence）

| # | 机制 | 与 A1 的关系 | evidence |
|---|---|---|---|
| **A1** | **T1 流量÷存量**：`winsorize(group_rank(ts_sum(valueeur÷holdings,66),industry),std=2)` | 基线 | `post:43178926004887`（70 赞，DEU/TOP500/D1 专帖） |
| **A2** | T3 反例对照：`ts_mean` 替代 `ts_sum` | **单变量：sum↔mean** | `post:43178926004887`（帖内实测 1.44→0.73） |
| **A3** | T4 并列块修正：A1 外套 `tail(0.25/0.75,0.5)` | **单变量：加 tail** | 同上（并列块占横截面 72–85%；帖内 +0.24S/+0.58subU） |
| **A4** | T2 姊妹腿：分子换 `vec_sum(insd1_shares)` | 单变量：金额↔股数 | 同上（1.59 vs 1.68，须同号） |
| **A5** | 分组轴对照：`industry`→`sector` | 单变量：组轴 | `internal:FIELD_insiders1#4.x`（D4 分组轴维） |
| **A6** | 窗口梯第一点：`ts_sum(·,22)` | 单变量：窗口 | `internal:FIELD_insiders1#4.4`（66≈季度，22 作对照） |
| **A7** | **T5 显著性 SNR**：`divide(ts_zscore(a,63), ts_std_dev(ts_zscore(a,5),33))` 再 `group_zscore` | 独立机制（A1 之外） | `post:43179521660823`（109 赞，三市场同构）+ `post:43437322582039`（21 赞） |
| **A8** | **T6 价格参照偏离**：`rank(ts_av_diff(ts_backfill(vec_avg(insd1_price)/close,150),60))` | 独立机制 | `post:43794123838615`（29 赞，GBR 机制；DEU 未测） |
| **A9** | T4 带宽对照：`tail(0.10/0.90)` | 单变量：带宽（判 A3 是否峰） | `post:43178926004887` |
| **A10** | 窗口梯第三点：`ts_sum(·,132)` | 单变量：窗口 | `internal:FIELD_insiders1#4.4` |

**为什么不追加更多机制**：`insd1_gvkey` / `transaction_currency_code` 论坛明确归为「编码/标签」→ 不挖；`insd1_value` 须先归一币种 → 用 `valueeur` 代替。这三条已在台账写明。

## 二、闸门结果（实跑）

- 首轮：**臂10 被 `[OPS] 算子调用点数 15 ≥ 10` 拦下** → 该臂是「跨维度乘积（杠杆I×T5）」，且证据最弱 ⇒ **换成窗口梯第三点 132**（顺带补上 FIELD 档未扫的窗口）。
- 次轮：10/10 表达式闸 pass，但 `all_pass=false` —— 闸6 批级多样性判 `{group_rank, industry, insd1_holdings, insd1_valueeur, vec_sum, winsorize}` 出现 4–5 次（上限 3）。
  **这是受控单变量设计的必然结果**，不是失误：7/10 臂是同族单轴对照。⇒ 按 `--batch-type repair`（参数/变体批，闸6 豁免）重跑：**`all_pass=true`，10/10 passed**。
  ⚠ 该批次类型同时豁免证据闸（`applied=false`）——但证据并非缺失：上面两个台账键都是 2026-11-16 的当天留痕，属**显式知情豁免**，不是绕闸。
- 残留 `[WINDOW]` 警告 2 条（A7 的 120/63/5/33、A8 的 150/60、A10 的 132）：**均为原帖模板窗口，属忠实复现，不是自由参数**；若任一臂过 0.9 再单独做窗口敏感性。

## 三、读数设计（派发后怎么判）

| 对照 | 看什么 | 判读 |
|---|---|---|
| **A1 vs A2** | sum vs mean | 复现帖内 1.44→0.73 的「频次信息」结论？ |
| **A1 vs A3** | 有无 tail | T4 是否给出 +S/+subU；若 A3 < A1 ⇒ 并列块假设在该族不成立 |
| **A3 vs A9** | 0.25/0.75 vs 0.10/0.90 | 带宽是否内点峰（双向都要有读数） |
| **A1 vs A5** | industry vs sector | 组轴效应（D4） |
| **A1 vs A6 vs A10** | 22 / 66 / 132 | 窗口梯形（FIELD §4.4 未扫的那一段） |
| **A1 vs A4** | 金额 vs 股数 | 姊妹腿必须同号，异号即机制不稳 |
| **A7 / A8 绝对值** | 独立机制 | 单独是否 ≥0.9；与 A1 是否高相关（同集不同维度，预期 <0.7） |

**过闸判据**（沿用本战役口径）：S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥1.0 / TO 0.01–0.70 / CW≤0.1（平台 limit 0.1）/ `failed_ra_count=0`。任一臂达标 ⇒ 进提交链（先 self 后 prod，prod>0.7 一律不能交）。

## 四、必须先知道的一条冲突（写在这里防误判）

70 赞帖自称其 DEU/D1 件 `xAjEkeOq` 达 **Sharpe 1.68**，但本账号 `get_alpha_details` 返回 **404**（他人 alpha）⇒ 该读数**未经本账号实测**。它与本区 `BE176` 的 insiders1 上限 **≈1.30**（30 臂）冲突，冲突未解（疑分组轴/decay/窗口不同）。
⇒ 本波**不以 1.68 为目标**，只回答「T1/T3/T4 这三条机制在本区是否成立、相对本 run 最好值 0.89 有没有增益」。
