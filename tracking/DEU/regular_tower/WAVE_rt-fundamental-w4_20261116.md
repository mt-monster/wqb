# WAVE rt-fundamental-w4（精修波）— fundamental72 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-16；槽：regular_tower（纯本地归因；判读不改写邻接数据集先验，跨区不外推）
- 主集：`fundamental72`（目标塔 FUNDAMENTAL）；本波**无 insiders 臂**（10/10 单集件，全部只引用 fnd72 字段）
- 配置（平台回显，DB payload 逐臂一致）：DEU/TOP500/D1、neutralization=FAST、decay=0、truncation=0.08、nanHandling=ON、maxTrade=OFF、FASTEXPR；平台回显 `startDate=2014-01-01`、`endDate=2023-12-31`
  - 与 `tracking/DEU/config/settings.json:16-17`（2013-01-01 起）不同；`create_multi_simulation` 无 startDate/endDate 参数（`world-quant-brain-mcp/tools_sim.py:672-690`）。本档原样记录平台值。
- 派发/收割：**ask 未提供本波 multisim id、preflight、operator_audit、查重记录**——本档不虚构，相关盲区登记于 §11。读数来源 = ask 臂序转录 + 本槽 DB 只读核验。
- 判读基准（ask 给定）：S≥1.58 / F≥1.0 / sub≥1.0（本地 review 线；平台 LOW_SUB limit 动态，本波无 LOW_SUB fail）/ TO 0.01–0.70 / margin≥0.0005（5bp，`tracking/DEU/config/thresholds.json:7`）/ prod&self corr≤0.70；CW 用**平台 limit 0.1**（`thresholds.json:20` 的 0.5 只是本地 review 线）。
- 2Y 闸种：本波 **10/10 臂为单数据集件**（expressions `atom_flag=atom`、`atom_n_datasets=1`；DB `alphas.is_ladder_sharpe` 全 null），全部走 `LOW_2Y_SHARPE`（limit 1.58）；**无多数据集件**，IS_LADDER 三处一致条款本波不适用（非漏检）。
- 符号指纹：本波仍**无翻符号对照臂**（0 条 multiply(-1,…)；settings decay 固定 0）。⇒ 本波不对方向做裁定。

## §1 臂序读数表（原样转录，按臂序，勿按 alpha id 猜）

| # | alphaId | 结构（简） | S | F | 2Y（LOW_2Y） | sub | TO | DD | margin | LC/SC | 塔（effective） | RA fail（DB `ra_failed_checks`） |
|---|---|---|---|---|---:|---|---:|---:|---|---:|---|---|
| 1 | 0mPQJnWv | oper_inc 三年窗核 + `tail(0.05/0.95)` | 1.31 | 0.82 | 2.32 | 1.19 | 18.59% | 10.32% | 0.000775 / 7.75bp | 226/156 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, LOW_FITNESS] |
| 2 | wpozrXV5 | oper_inc 三年窗核 + `tail(0.08/0.92)` | 1.54 | 1.03 | **2.56** | 1.21 | 18.54% | 7.38% | 0.000889 / 8.89bp | 221/161 | FUNDAMENTAL×1.8（1） | 1：[LOW_SHARPE 1.54<1.58]；F/2Y/sub/CW/CLUSTER pass |
| 3 | qM7zReZj | oper_inc 三年窗核 + `tail(0.09/0.91)` | 1.54 | 1.03 | 2.47 | 1.21 | 18.48% | 7.64% | 0.000893 / 8.93bp | 220/162 | FUNDAMENTAL×1.8（1） | 1：[LOW_SHARPE]；其余 pass |
| 4 | omazdQeE | oper_inc 三年窗核 + `tail(0.11/0.89)` | 1.55 | 1.04 | 2.27 | 1.21 | 18.21% | 7.79% | 0.000903 / 9.03bp | 217/165 | FUNDAMENTAL×1.8（1） | 1：[LOW_SHARPE]；其余 pass |
| 5 | 1YWmM65R | oper_inc 三年窗核 + `tail(0.10/0.90)`，**subindustry** 分组 | 1.18 | 0.69 | 1.87 | 0.78 | 15.78% | 7.88% | 0.000692 / 6.92bp | 208/175 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, LOW_FITNESS] |
| 6 | d5a7Geq2 | oper_inc **两腿**（去 δ176，`rank(δ240)×ts_rank`）+ `tail(0.10)` | 1.29 | 0.80 | 1.85 | 0.90 | 18.02% | 7.71% | 0.000775 / 7.75bp | 219/164 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, LOW_FITNESS]；⚠ `checks.fail=[]`，两项在 warning |
| 7 | QP0l8meX | oper_inc **两腿**（去 δ176，`rank(δ240)×rank(ts_rank)`）+ `tail(0.10)` | 1.27 | 0.78 | 1.87 | 0.86 | 18.28% | 8.35% | 0.000754 / 7.54bp | 218/164 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, LOW_FITNESS]；⚠ `checks.fail=[]`，两项在 warning |
| 8 | WjlX5KkN | **EBIT** 三年窗核 + `tail(0.10/0.90)` | **1.56** | **1.05** | 2.30 | 1.04 | 17.30% | 7.14% | 0.000914 / 9.14bp | 214/168 | FUNDAMENTAL×1.8（1） | 1：[LOW_SHARPE 1.56<1.58（差 0.02）]；其余 pass |
| 9 | kqamAeRg | **EBIT 三年窗核 + `tail(0.08/0.92)`** | **1.62** | **1.12** | **2.54** | **1.16** | 17.40% | **6.15%** | 0.000948 / 9.48bp | 216/166 | FUNDAMENTAL×1.8（1） | **0：RA failed_ra_count=0 / ra_failed=false——LOW_SHARPE/LOW_FITNESS/LOW_TURNOVER/HIGH_TURNOVER/CW/LOW_SUB/CLUSTER/LOW_2Y/MATCHES_PYRAMID 全 pass；仅 MATCHES_COMPETITION/THEMES warning；SELF/PROD/DATA_DIVERSITY 仍 pending** |
| 10 | 2r5ZYPE6 | **EBIT** 三年窗核 + `tail(0.12/0.88)` | 1.51 | 1.00 | 2.17 | 1.00 | 17.13% | 6.94% | 0.000885 / 8.85bp | 212/170 | FUNDAMENTAL×1.8（1） | 1：[LOW_SHARPE 1.51<1.58]；其余 pass |

- DB 只读核验（sqlite `mode=ro`，零写入）：10 行 backtest 指标与 ask 逐值一致；`ra_failed_checks` 与平台 `ra.failed_ra_count`/名单一致（臂9 为 `[]`）；payload `settings` 逐臂 FAST/decay0/TOP500/D1/2014-01-01→2023-12-31；`pyramids` 10/10 = `DEU/D1/FUNDAMENTAL`×1.8（effective=1）。
- ⚠ **checks 表示不一致（平台原文）**：臂6（d5a7Geq2）与臂7（QP0l8meX）`checks.fail=[]`，但 `ra.failed_ra_count=2`、ra 名单含 LOW_SHARPE/LOW_FITNESS（在 `checks.warning` 带 value/limit）。本档以 `ra_failed_checks` 判 fail（AGENTS §8.7：RA 资格门失败含 WARNING/ERROR）；只看 `checks.fail=[]` 会误判臂6/7 通过。

## §2 逐臂归因条目

1. **臂1 0mPQJnWv（oper_inc 三年窗核 + tail 0.05）**：S 1.31/F 0.82/2Y 2.32/sub 1.19/TO 18.59%/DD 10.32%/margin 7.75bp/LC 226-156；RA fail 2。**vs w3 臂9（同核 tail 0.10，1.56/1.05/2.41/1.18）**：S **−0.25**/F −0.23/2Y −0.09/sub +0.01/TO +0.29pp/DD +2.30pp。⇒ 带宽收到 0.05 时 **S/F 塌陷**（尾部裁掉太多有效信息），虽然 sub 略升；0.05 不是可行方向。
2. **臂2 wpozrXV5（tail 0.08）**：S 1.54/F 1.03/**2Y 2.56（本波最高）**/sub 1.21/TO 18.54%/DD 7.38%/margin 8.89bp/LC 221-161；RA fail 1。**vs 0.10**：S −0.02/F −0.02/2Y **+0.15**/sub +0.03/TO +0.24pp/DD −0.64pp ⇒ 0.08 是"2Y/DD 补偿点"，S/F 只让 0.02；**vs 0.05**：S +0.23/F +0.21/2Y +0.24 ⇒ 0.05→0.08 是主升段，0.08 已进入平台区。
3. **臂3 qM7zReZj（tail 0.09）**：S 1.54/F 1.03/2Y 2.47/sub 1.21/TO 18.48%/DD 7.64%/margin 8.93bp/LC 220-162；RA fail 1。**vs 0.08**：S/F 持平、2Y −0.09、sub 持平、TO −0.06pp、DD +0.26pp；**vs 0.10**：S −0.02/F −0.02/2Y +0.06/sub +0.03。⇒ 0.08–0.10 之间是平台，0.09 无独立优势。
4. **臂4 omazdQeE（tail 0.11）**：S 1.55/F 1.04/2Y 2.27/sub 1.21/TO 18.21%/DD 7.79%/margin 9.03bp/LC 217-165；RA fail 1。**vs 0.10**：S −0.01/F −0.01/2Y −0.14/sub +0.03/TO −0.09pp ⇒ S/F 与 0.10 几乎持平、2Y 已开始回落；**vs 0.08**：S +0.01/F +0.01/2Y −0.29/sub 持平 ⇒ 0.08 与 0.10 之间的取舍是"2Y vs S/F"。
5. **臂5 1YWmM65R（同核 tail 0.10，sector→subindustry）**：S 1.18/F 0.69/2Y 1.87/sub 0.78/TO 15.78%/DD 7.88%/margin 6.92bp/LC 208-175；RA fail 2。**vs w3 臂9（同核 tail 0.10，sector，1.56/1.05/2.41/1.18）**：S **−0.38**/F **−0.36**/2Y **−0.54**/sub **−0.40**/TO −2.52pp。⇒ **分组轴是本波最大的单变量负杠杆：sector ≫ subindustry**；subindustry 省换手但把信号打散。与 w3 的 sector > industry（1.48 vs 1.39）方向一致，三轴排序为 **sector > industry > subindustry**（industry 是不同核的对照，subindustry 是同核直接对照）。
6. **臂6 d5a7Geq2（同核 tail 0.10，去 δ176 腿，两腿 raw ts_rank）**：S 1.29/F 0.80/2Y 1.85/sub 0.90/TO 18.02%/DD 7.71%/margin 7.75bp/LC 219-164；RA fail 2（checks.fail 空）。**vs w3 臂9（三腿 1.56/1.05/2.41/1.18）**：S **−0.27**/F **−0.25**/2Y **−0.56**/sub **−0.28**。⇒ **δ176 腿是承重腿**，在 tail 0.10 壳下不可减；两腿复合已降到单腿基准 1.29 持平（not below，但远低于三腿）。
7. **臂7 QP0l8meX（同臂6 但 `rank(ts_rank)`）**：S 1.27/F 0.78/2Y 1.87/sub 0.86/TO 18.28%/DD 8.35%/margin 7.54bp/LC 218-164；RA fail 2（checks.fail 空）。**vs 臂6（raw ts_rank）**：S −0.02/F −0.02/2Y +0.02/sub −0.04 ⇒ 两腿核上 rank 包装近中性/略负；**vs 单腿基准 1.29**：1.27 低 0.02 ⇒ **边际稀释（0.02）**，与 w3 在三腿核上"rank 包装 +0.03~0.04"相反 ⇒ rank 包装不是稳健杠杆，随核变。
8. **臂8 WjlX5KkN（EBIT 三年窗核 + tail 0.10）**：S 1.56/F 1.05/2Y 2.30/sub 1.04/TO 17.30%/DD 7.14%/margin 9.14bp/LC 214-168；RA fail 1（LOW_SHARPE 差 0.02）。**vs w3 臂9（oper_inc 同 tail 0.10，1.56/1.05/2.41/1.18）**：S/F 持平、2Y −0.11/sub −0.14、TO −1.00pp、DD −0.88pp、margin +0.08bp ⇒ EBIT 在 0.10 带宽下用 2Y/sub 换低换手/低回撤，S/F 无增益。
9. **臂9 kqamAeRg（EBIT 三年窗核 + tail 0.08）——本波/本族首个 RA 全闸 PASS**：S **1.62**/F **1.12**/2Y **2.54**/sub **1.16**/TO 17.40%/DD **6.15%**/margin **9.48bp**/LC 216-166；**ra_failed_count=0**，LOW_SHARPE/LOW_FITNESS/LOW_TURNOVER/HIGH_TURNOVER/CW/LOW_SUB/CLUSTER/LOW_2Y/MATCHES_PYRAMID 全 pass，只有 MATCHES_COMPETITION/THEMES warning。**vs 臂8（EBIT 0.10）**：S **+0.06**/F **+0.07**/2Y **+0.24**/sub **+0.12**/TO +0.10pp/DD −0.99pp/margin +0.34bp ⇒ **0.08 在 EBIT 核上全面优于 0.10**。**vs 臂2（oper_inc 0.08，1.54/1.03/2.56/1.21）**：S **+0.08**/F **+0.09**/2Y −0.02/sub −0.05/TO −1.14pp/DD −1.23pp/margin +0.59bp ⇒ EBIT 在 0.08 带宽上以 2Y/sub 的微小代价换 S/F/换手/回撤。**vs w3 最佳（oper_inc 0.10，1.56/1.05/2.41/1.18）**：S +0.06/F +0.07/2Y +0.13/sub −0.02/TO −0.90pp/DD −1.87pp/margin +0.42bp。⇒ **EBIT×0.08 是当前 fnd72 最优组合，且首次全闸通过**。⚠ SELF/PROD/DATA_DIVERSITY pending、年度分年未取 ⇒ **RA PASS ≠ 可提交**（§8/§9）。
10. **臂10 2r5ZYPE6（EBIT 三年窗核 + tail 0.12）**：S 1.51/F 1.00/2Y 2.17/sub 1.00/TO 17.13%/DD 6.94%/margin 8.85bp/LC 212-170；RA fail 1。**vs 臂8（EBIT 0.10）**：S −0.05/F −0.05/2Y −0.13/sub −0.04/TO −0.17pp/DD −0.20pp/margin −0.29bp；**vs 臂9（EBIT 0.08）**：S −0.11/F −0.12/2Y −0.37/sub −0.16/TO −0.27pp/DD +0.79pp。⇒ EBIT 核上带宽 0.08→0.10→0.12 **单调下降**（S/F/2Y/sub 全降），0.08 是已测最窄点、当前最优；是否还有更窄更优点需补 0.06/0.07。

## §3 带宽 / 杠杆结论（本波重点）

### 3.1 oper_inc 核：带宽曲线 0.05–0.15（同核、同 raw `ts_rank`、同 sector，单变量）

| 带宽 | 臂（波） | S | F | 2Y | sub | TO | DD | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 0.05 | w4 臂1 0mPQJnWv | 1.31 | 0.82 | 2.32 | 1.19 | 18.59% | 10.32% | 7.75bp |
| 0.08 | w4 臂2 wpozrXV5 | 1.54 | 1.03 | **2.56** | 1.21 | 18.54% | 7.38% | 8.89bp |
| 0.09 | w4 臂3 qM7zReZj | 1.54 | 1.03 | 2.47 | 1.21 | 18.48% | 7.64% | 8.93bp |
| **0.10** | w3 臂9 O0WmdbPR | **1.56** | **1.05** | 2.41 | 1.18 | 18.30% | 8.02% | 9.06bp |
| 0.11 | w4 臂4 omazdQeE | 1.55 | 1.04 | 2.27 | 1.21 | 18.21% | 7.79% | 9.03bp |
| 0.12 | w2 臂7 d5a7PrpK | 1.51 | 1.00 | 2.33 | 1.14 | 18.11% | 7.47% | 8.69bp |
| 0.15 | w3 臂10 88N6Wa9W | 1.53 | 1.02 | 2.10 | 1.09 | 17.63% | 6.50% | 8.89bp |

**结论（oper_inc）**：**0.05 塌陷**（S 1.31，比 0.08 低 0.23）⇒ 带宽过窄裁掉有效信息；**0.08–0.11 是平台区**（S 1.54–1.56、F 1.03–1.05、sub 1.18–1.21、2Y 2.27–2.56）；**0.10 是全期 S/F 峰**，**0.08 是 2Y/DD 峰**（2.56/7.38%）；0.12/0.15 回落到 1.51/1.53。⇒ **w3 的"0.10 是边界值"缺口本波关闭：0.05/0.08 已补测，0.10 是内点峰（S/F 面）**，但 0.08 与 0.10 的差异很小（S −0.02、2Y +0.15），选择取决于"要 S 还是要 2Y/DD"。

### 3.2 EBIT 核：带宽曲线 0.08–0.12（同核同字段，单变量）

| 带宽 | 臂 | S | F | 2Y | sub | TO | DD | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **0.08** | 臂9 kqamAeRg | **1.62** | **1.12** | **2.54** | **1.16** | 17.40% | 6.15% | 9.48bp |
| 0.10 | 臂8 WjlX5KkN | 1.56 | 1.05 | 2.30 | 1.04 | 17.30% | 7.14% | 9.14bp |
| 0.12 | 臂10 2r5ZYPE6 | 1.51 | 1.00 | 2.17 | 1.00 | 17.13% | 6.94% | 8.85bp |

**结论（EBIT）**：0.08→0.10→0.12 **单调下降**（S 1.62→1.56→1.51、F 1.12→1.05→1.00、2Y 2.54→2.30→2.17、sub 1.16→1.04→1.00）⇒ **EBIT 核的带宽最优在已测最窄点 0.08**，且 0.08 已全闸通过；是否还有 0.06/0.07 更优点**未测**，不得断言 0.08 是全局峰（但它是当前已测最优且首个 PASS）。

### 3.3 字段 × 带宽交互（本波最重要的杠杆结论）

- **同带宽 0.08**：EBIT（臂9 1.62/1.12/2.54/1.16）vs oper_inc（臂2 1.54/1.03/2.56/1.21）⇒ **S +0.08 / F +0.09 / 2Y −0.02 / sub −0.05 / TO −1.14pp / DD −1.23pp / margin +0.59bp**。
- **同带宽 0.10**：EBIT（臂8 1.56/1.05/2.30/1.04）vs oper_inc（w3 臂9 1.56/1.05/2.41/1.18）⇒ **S/F 持平、2Y −0.11 / sub −0.14 / TO −1.00pp / DD −0.88pp**。
⇒ **EBIT 的优势只在窄带宽（0.08）兑现**；带宽放宽到 0.10 后 S/F 优势消失、只剩换手/回撤优势。⇒ **字段选择不能脱离带宽**；"EBIT > oper_inc"不是无条件结论（w2 在 0.10 三腿核上 EBIT 也只 +0.04/+0.04/2Y −0.10/sub −0.05，本波在 0.08 上放大到 +0.08/+0.09，方向一致量级不同）。
- **带宽峰随字段核移动**：oper_inc 峰 0.10（S/F），EBIT 峰 0.08（已测最窄）⇒ **不存在"全族统一最优带宽"**；带宽必须与字段/核联合调。

### 3.4 分组轴（同核 0.10 oper_inc）

- sector（w3 臂9 1.56/1.05/2.41/1.18）vs subindustry（w4 臂5 1.18/0.69/1.87/0.78）⇒ **S +0.38 / F +0.36 / 2Y +0.54 / sub +0.40**（同核同带宽，单变量）。
- 结合 w3 的 sector vs industry（1.48/1.02/1.64/0.95 vs 1.39/0.90/1.64/0.90，不同核但同 C0）：**sector > industry ≫ subindustry**。⇒ 保持 sector；subindustry 即使在中性化设置上"可换换手"，作为**信号内分组轴**是强负杠杆。

### 3.5 减腿 / 包装

- **δ176 腿承重**：三腿（w3 臂9 1.56/1.05/2.41/1.18）→ 两腿去 δ176（w4 臂6 1.29/0.80/1.85/0.90）：S **−0.27**/F −0.25/2Y −0.56/sub −0.28 ⇒ 不可减。
- **rank(ts_rank) 在两腿核上近中性/略负**（臂6 1.29 → 臂7 1.27；S −0.02、sub −0.04），与三腿核上 +0.03~0.04 相反 ⇒ rank 包装不是稳健杠杆。
- **无 bucket**：本波零 bucket 臂，稀释铁律中的 bucket 分支不适用。

### 3.6 首个 RA 全闸 PASS

**臂9 kqamAeRg（EBIT × 三年窗三腿 × tail 0.08 × sector）**：S 1.62（≥1.58）、F 1.12（≥1.0）、2Y 2.54（≥1.58）、sub 1.16（≥1.0）、TO 17.40%（∈0.01–0.70）、margin 9.48bp（≥5bp）、CW pass、CLUSTER pass、LOW_TURNOVER/HIGH_TURNOVER pass、MATCHES_PYRAMID pass；**ra_failed_count=0**。这是 fnd72 在 DEU 的**首个 RA 全闸通过件**（w1–w3 最高 1.56 仍差 LOW_SHARPE 0.02）。**但 SELF/PROD/DATA_DIVERSITY 仍 pending，且年度分年未取** ⇒ 只是 RA 层达标，**不是提交授权**。

## §4 符号指纹 / 稀释铁律 / 跨区核对

- **符号指纹：未测**。无整式反号臂；settings decay 固定 0；tail/带宽变换均不改变符号。⇒ 不能按「衰减对称=机制在/符号错；单向=事件型」判定；本波不对方向做裁定。近闸/PASS 件推进前应补反号对照（w1–w3 连续登记该缺口，本波仍未补）。
- **稀释铁律**：本波**零 bucket**。乘法复合相对单腿基准（w1 `omazqreb` 1.29）：三腿/两腿主流臂 1.51–1.62 > 1.29，不触发；**仅臂7（1.27）低于单腿 1.29 0.02**，记边际稀释（与 rank 包装不稳健同源）。另「两腿 < 三腿」（1.29/1.27 < 1.56）属**减腿负杠杆**，不是严格意义的"乘法低于单腿"，分开登记。
- **跨区不外推**：零 TWN/KOR 引用；对照全部 DEU 域内（w1–w3 臂、mLaALJX2、本波同核波内）。fnd45/fnd86/fnd89/fnd90 邻接集先验未改写；insiders1 本波未测、状态不变（沿用 w1/w2：不判死、无可推进结构）。

## §5 塔位判读（点塔相关性）

平台 payload `pyramids` 原文（逐臂回读）：10/10 臂 = `DEU/D1/FUNDAMENTAL` ×1.8、effective=1。

- **目标塔 FUNDAMENTAL 出现 10/10 臂归属**（无 insiders 臂、无双塔件、无多数据集件）。
- **点位与点亮**：常规 RA 口径下 10/10 臂中**仅臂9 全闸通过**（ra_failed_count=0）⇒ 臂9 具备**塔位点亮资格**（前提：prod/self/data-diversity 过关 + 用户确认提交）。本波**实际点亮 0**（未提交；SELF/PROD/DATA_DIVERSITY pending）。其余 9 臂未过全闸，不点亮。
- 单塔件（effective=1）占满全波 ⇒ 本波不涉及双塔配位/配额问题。

## §6 数据层判读（data_excluded 与信号死分开）

- **本波零 data_excluded 臂**：LC/SC 156–226 全宽，无 LC/SC≤5；无宽度塌缩。
- **CW 10/10 全 pass**：本波无 insiders 腿，CW 挂闸（数据层指纹）未出现；与 w1/w2 的 insiders 臂形成对照，进一步支持「CW 挂由 insiders 持仓宽度驱动」的判读。
- **无判死**：本波 10 臂但结构互异 <10（§7），按探针条款不判死；fundamental72 不 data_excluded、不判死。首个 PASS 也不改变"数据层未排除"的结论（只是候选层突破）。

## §7 判死六维闸盘点（D1–D6；本波自身口径）

| 维 | 本波现状 | 判定 |
|---|---|---|
| D1 结构互异模板 ≥10 | 名义 10 臂，互异机制 ~4：oper_inc 三年窗核带宽扫描（0.05–0.11）、EBIT 三年窗核带宽扫描（0.08–0.12）、两腿减腿（2）、subindustry 轴（1）——大部分是同一核的带宽/字段变体 | **✗ 未达** |
| D2 字段族自测 | 本波只碰 **2 个 fnd72 字段**（oper_inc、ebit）+ tot_asset；fnd72 共 1031 字段 | **✗ 远未达** |
| D3 矩全家 | 一阶差（δ240/δ176）✓、比值（oper_inc/ebit ÷ assets）✓；**缺**二阶波动、信噪比、纯水平腿 | **✗ 未达** |
| D4 分组轴 ≥2 | sector（臂1-4/6-10）、subindustry（臂5）；历史另有 industry（w3） | ✓ |
| D5 非线性 ≥1 | ts_rank、group_rank、tail、multiply | ✓ |
| D6 配置 ≥2 | 本波固定 FAST/decay0/TOP500/D1 **一套** | **✗ 本波自身未达**（跨槽累计有 SUBINDUSTRY 三波，非本波读数） |

⇒ 缺 D1/D2/D3/D6：**不得判死、不得封集、不得作为邻接集先验**（AGENTS §7.6）。**PASS 是候选层事件，不是数据集终态**。

## §8 近闸候选（≤2，按 S 降序；先测 prod 再扫参）

> **臂9 `kqamAeRg` 已 RA 全闸通过，不占 near 位**（它是 PASS 候选，见 §3.6/§9）；以下为未过闸中距闸最近的 2 条。

| 序 | alphaId | S | 触发原因（读数引用） |
|---|---|---|---|
| 1 | `WjlX5KkN` | **1.56** | S≥1.2；距 S 硬闸 1.58 差 **0.02**≤0.4；唯一 FAIL=LOW_SHARPE；F 1.05/2Y 2.30/sub 1.04/CW pass/CLUSTER pass/margin 9.14bp/TO 17.30% |
| 2 | `omazdQeE` | **1.55** | S≥1.2；距 S 硬闸差 **0.03**≤0.4；唯一 FAIL=LOW_SHARPE；F 1.04/2Y 2.27/sub 1.21/CW pass/CLUSTER pass/margin 9.03bp/TO 18.21% |

- 排序外登记（如实）：`wpozrXV5` 1.54（2Y **2.56** 本波最高、F 1.03、sub 1.21）、`qM7zReZj` 1.54（2Y 2.47）也满足 S≥1.2 且唯一 FAIL=LOW_SHARPE，按 S 降序第 3/4 出局；arm1 1.31、arm5 1.18、arm6 1.29、arm7 1.27、arm10 1.51 等按 S 降序出局（全量读数见 §1）。
- **prod/self 未测（本波全 null；臂9 平台显示 SELF/PROD/DATA_DIVERSITY pending）**：PASS 候选与两条 near 均为 fnd72 核心件——按「prod 雷在核心不在搭档」，**先测臂9 的 prod/self/data-diversity**，再决定 near 件是否扫参。族内先验 mLaALJX2 prod 0.5444（<0.70）是利好但不同表达式，不构成保证。
- **年度分年未取** ⇒ 2018/2019/2020 时间集中度**未验证**。族级既有读数（`S0_TOWER_SCAN_20261115.md:130`：mLaALJX2 2018 0.80/2019 0.80/2020 −0.35，2021–2023 3.03/2.60/1.96）提示该族存在时间集中风险。**臂9 推进提交链前必须补分年**；若 2018/2019/2020 仍全 <1.0 而总 S 靠 2021–2023 撑起，按「时间集中度风险」登记，**不得按可提交推进**。
- **mode_b_qualification**（`thresholds.json:23-27`）：臂9 S 1.62/F 1.12、臂8 S 1.56/F 1.05、臂4 1.55/1.04、臂2/3 1.54/1.03 均过 S≥1.25/F≥0.8 资格线。

## §9 datasetStatus 裁决 + 波 verdict

**datasetStatus = active（继续加注；维持 w2/w3 的 active，无终态转换）**。依据：

1. **首个 RA 全闸 PASS**：臂9 S 1.62/F 1.12/2Y 2.54/sub 1.16/TO 17.40%/margin 9.48bp，ra_failed_count=0；这是 fnd72 在 DEU 的历史首次全闸通过（w1–w3 最高 1.56 仍差 LOW_SHARPE 0.02）。
2. **带宽峰确认**：oper_inc 0.05→0.08→0.10→0.12→0.15 呈现"塌陷→平台→回落"，0.10 为 S/F 内点峰；EBIT 0.08→0.10→0.12 单调下降，0.08 为已测最优；带宽峰随字段核移动。
3. **无数据层排除**：LC/SC 156–226 全宽、CW 10/10 pass、无宽度塌缩 ⇒ 不满足 data_excluded。
4. **不得判死/封集**：D1/D2/D3/D6 未达（§7），AGENTS §7.6 六维闸禁止终判死；PASS 只是候选层事件，不是数据集终态。
5. **insiders1**：本波未测（零 insiders 臂），状态沿用 w1/w2（不判死、无可推进结构）；本波不对其做新判读。

**波 verdict = PASS**（判定表 `src/wqb/wave_results_contract.py:79-90`：有臂过 RA 全闸 ⇒ PASS；`n_pass=1 / n_near=2`；PASS 臂 = `kqamAeRg`，RA failed_ra_count=0）。⚠ **PASS 的 scope 是 RA 层**：SELF/PROD/DATA_DIVERSITY pending、年度分年未取 ⇒ 不是提交授权；提交仍须用户明确确认 + `confirm_submit=True`（AGENTS §7 五道闸见 `Claude/skills/wq-brain-ra-gbr/rules/gate-and-submit-discipline.md`，本档只做归因，不推进提交）。

## §10 newLever 登记（带宽 × 字段交互 + 首个全闸组合，带归因对照）

**tail 带宽峰随字段核移动；EBIT×tail0.08 为当前全闸组合**：
- **带宽精修（同核单变量，跨 w3/w4）**：oper_inc 核 0.05（1.31/0.82/2.32/1.19）→ 0.08（1.54/1.03/2.56/1.21）→ 0.09（1.54/1.03/2.47/1.21）→ **0.10（1.56/1.05/2.41/1.18）** → 0.11（1.55/1.04/2.27/1.21）→ 0.12（1.51/1.00/2.33/1.14）→ 0.15（1.53/1.02/2.10/1.09）。**0.05 塌陷、0.08–0.11 平台、0.10 S/F 峰、0.08 2Y/DD 峰、≥0.12 回落**。⇒ w3 "0.10 边界值"缺口关闭（0.10 为内点峰）。
- **字段×带宽交互（同带宽单变量）**：0.08 上 EBIT vs oper_inc = **S +0.08/F +0.09/2Y −0.02/sub −0.05/TO −1.14pp/DD −1.23pp/margin +0.59bp**；0.10 上 EBIT vs oper_inc = S/F 持平、2Y −0.11/sub −0.14 ⇒ **EBIT 优势只在窄带宽兑现**，不能写成无条件的"EBIT 优于 oper_inc"。
- **全闸组合（PASS）**：EBIT 三年窗三腿 + tail(0.08/0.92) + sector = **S 1.62/F 1.12/2Y 2.54/sub 1.16/TO 17.40%/margin 9.48bp，RA failed_ra_count=0**；对照 EBIT×0.10（1.56/1.05/2.30/1.04）与 oper_inc×0.08（1.54/1.03/2.56/1.21）→ 两条单变量归因同时成立。
- **caveat（必须随杠杆一起记）**：① EBIT 0.08 的**更窄带宽 0.06/0.07 未测**，故 0.08 是"已测最窄点"而非已证全局峰；② SELF/PROD/DATA_DIVERSITY pending、年度分年未取 ⇒ 全闸 PASS 不代表可提交；③ 本波无 insiders/多数据集件，不能外推到双塔或多集件；④ 跨区零引用，TWN/KOR 经验未用于本波。

## §11 证据通道与盲区

- **读数来源**：ask 转录的臂序读数 + 本槽 DB 只读核验（sqlite `mode=ro`，零写入）：10/10 行 backtest 指标与 ask 逐值一致；`ra_failed_checks` 与平台 `ra.failed_ra_count`/名单一致（臂9 `[]`）；payload `settings` 逐臂 FAST/decay0/TOP500/D1/2014-01-01→2023-12-31；`pyramids` 10/10 FUNDAMENTAL×1.8、effective=1；`alphas.is_ladder_sharpe` 全 null、prod/self 全 null。
- **IS_LADDER**：本波 10/10 单数据集件（`atom_n_datasets=1`），全部走 LOW_2Y_SHARPE；DB `two_year_sharpe` 与 checks 值 10/10 一致 ⇒ 三处一致条款不适用（非漏检）。
- **checks 表示不一致**：臂6/臂7 `checks.fail=[]` 但 `ra.failed_ra_count=2` 且 ra 名单含 LOW_SHARPE/LOW_FITNESS（warning 桶带 value/limit）——本档以 ra 名单判 fail（AGENTS §8.7）；`checks.fail` 原文照录。若只看 checks.fail，臂6/7 会被误判通过。
- **盲区（如实登记，不猜不补）**：
  1. **ask 未提供本波 multisim id / preflight / operator_audit / 查重记录**——本档不填写、不虚构；派发链证据缺口登记在此。
  2. 年度分年未取 → 2018/2019/2020 时间集中度未验证（§8）；臂9 提交前必补。
  3. prod/self 相关性未测（臂9 平台 SELF/PROD/DATA_DIVERSITY pending；其余 9 臂全 null）。
  4. 符号指纹未测（无翻符号对照臂）。
  5. create_multi_simulation 不暴露 startDate/endDate（`tools_sim.py:672-690`），平台回显 2014-01-01→2023-12-31 与 settings.json 2013-01-01 不同——原样记录平台值。
  6. 本波结构互异 <10，按探针条款不产生判死；六维 D1/D2/D3/D6 未达。

## §12 终态

- **波**：PASS；1 达标（`kqamAeRg` RA 全闸）+ 2 近闸（`WjlX5KkN` 1.56、`omazdQeE` 1.55）；best S **1.62**（kqamAeRg）/ best 2Y **2.56**（wpozrXV5）。
- **数据集**：fundamental72 = **active**（维持，无终态转换；首个 RA 全闸 PASS，D1/D2/D3/D6 未达 → 不判死、不封集）；insiders1 本波未测、不判死（沿用 w1/w2）。
- **提交链**：**未推进**（PASS 仅 RA 层；SELF/PROD/DATA_DIVERSITY pending、年度分年未取、无用户确认）。下一步：① 测 `kqamAeRg` 的 prod/self/data-diversity + 补 2018–2020 分年；② 若全过，按五道闸（台账排除 / RA+塔位 / 近十年 / self-corr / 篮内互相关+塔位配额）走提交前检查；③ near 件 `WjlX5KkN`（1.56/0.02）与 `omazdQeE`（1.55/0.03）可作 backup，但同样先测 prod；④ 带宽补测 EBIT 0.06/0.07，确认 0.08 是否全局峰；⑤ 不要动 settings decay（族内 0/2/4 负杠杆），不要用 subindustry 信号内分组（同核 −0.38 S），不要减 δ176 腿（−0.27 S）。
