# CATEGORY_MATRIX — DEU × FUNDAMENTAL 日终矩阵（2026-11-15）

- 性质：日终收尾档案（只写档案，零平台调用、零 DB 写入；本 run 共 3 波 = fundamental72 w1/w2/w3）。
- 证据来源（全部本会话实读或本 run 回执）：
  ① 本 run 三份归因档（本会话所写）：`WAVE_w1_fundamental72_20261114.md` / `WAVE_w2_fundamental72_20261114.md` / `WAVE_w3_fundamental72_20261115.md`；
  ② `S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md`（目标集重开盘点，全文实读）；
  ③ `CATEGORY_MATRIX_FUNDAMENTAL_20261114.md`（他槽日终矩阵，全文实读——§2 逐集状态的携带源，本 run 未回改该档）；
  ④ DB 回执（本 run）：wave_results DEU/w1 行 id 2174（合并式追加）→ verdict=PARTIAL、DEU/w2 id 2183 → PARTIAL、DEU/w3 id 2188 → FAIL（三行 status=closed、source_file=pipeline:auto）；
  ⑤ 本槽只读核验（本轮实跑 `logs/_tmp_fnd72_dayclose_verify.py`，sqlite mode=ro）：三波 wave_results 行在位（上列 id）+ backtest 行数 w1=10(fnd72)+10(fnd86)、w2=8(fnd72)、w3=7(fnd72)、expressions 同键同数——与三份归因档逐波核验一致；
  ⑥ run 收尾 rollup 三行（ask 给定）：数据集终态=「本 run 无数据集终态变更」、待用户确认候选=`[]`、跨波待处理提交链候选=无。
- 未做/不做（如实）：平台相关性、prod 复测、年度分年、self-corr 均未跑（单槽边界 + 日终零平台调用约束）；本矩阵不新增判读，只汇总既有档案状态。

## §1 本 run 波次与产出（fundamental72，DEU/TOP500/D1，SUBINDUSTRY/decay4/trunc0.08 全臂一致）

| 波 | 臂 | bestSharpe | verdict（DB id） | datasetStatus | near | 特记 |
|---|---|---|---|---|---|---|
| w1 | 10/10 COMPLETE errors=0 | **0.68**（npawrjPw bucket(vol) 条件化，DD 8.82% 最低） | PARTIAL（id 2174，与 fnd86 早槽波**共享行**，契约合并式追加，fnd86 条目逐字保留） | provisional（判弱入档） | ×1：LLKO3vZ9（2Y 1.51 距 2Y 闸 1.58 差 0.07） | 臂1 平台撞件 E56VAa19=2026-11-05 既有件（零新仿真）；中性化轴对照 SUBINDUSTRY 0.20 vs FAST 1.42（RREALzx0，DB）=7x 缺口 |
| w2 | 8/8 COMPLETE errors=0 | 0.25（LLKbPm7M sales_rev 门控） | PARTIAL（id 2183，clean insert） | provisional（连续） | ×2：A1xJRr0l（2Y 1.20 距闸 0.38）、gJaqYgQl（2Y 1.53 距闸 0.05，全战役最近） | 门控-2Y 假设族级证伪（5/5 <1.58）；CW=0.5 恒定结构指纹 5/5；新杠杆「形态-2Y」入册 |
| w3 | 7/7 终态 errors=1（臂6 WARNING=UNITS 告警，非连坐，IS 在册） | 0.21（ZYaqYEzn group_neutralize(vol-bucket)） | **FAIL**（id 2188，clean insert；0 达标 0 near——臂4 2Y 1.16 距闸 0.42 出线 0.02） | provisional（连续） | **空** | gBF 修 CW 失败（2/2 仍 0.5）+ 纯退化 ⇒「gBF/CW 反证杠杆」入册；4 探针开门线全过（LC+SC 134–155）⇒ 波4 主臂前置满足；臂6 UNITS=数据格式层缺陷（tle 价格单位场），读数低可靠 |

三波累计：25 臂全 RA fail；S 面 @SUBINDUSTRY 格 best 0.68→0.25→0.21；修复路径两条证伪（门控推 2Y、gBF 修 CW）；2Y 裸锚形态跨波复现（a_ebit 1.51/a_is_oper_inc 1.53，S 面 0.07–0.11 死）；判死六维闸 D1（互异机制 ~5）/D3（比值/SNR 腿三波零实测）/D6（三波单配置）未达 ⇒ 三波均 provisional，无终态转换。

## §2 逐集终态矩阵（类别 12 集；11 集状态携带自 `CATEGORY_MATRIX_FUNDAMENTAL_20261114.md` §2 原行，本 run 未改写其先验；fnd72 行为本 run 焦点）

| 数据集 | 终态 | 类型 | 状态依据 |
|---|---|---|---|
| fundamental1 | capped（已收割） | A 已收敛 | 11-14 矩阵 §2（pwaQ0bx3 S 1.60/F 1.40/2Y 2.01/prod 0.6821 已提交 ACTIVE，waveBE242:441-461）；本 run 无动作 |
| fundamental6 | capped | A 已收敛 | 11-14 矩阵 §2（ATOM 天花板 1.15；oiadpq 单点 1.73 被 Wje5K71x 占用）；本 run 无动作 |
| fundamental17 | 浅探排除（非判死依据） | A 已收敛 | 11-14 矩阵 §2（台账 10 臂 0 passed + 拥挤；AGENTS §7.5 实证在案）；本 run 无动作 |
| fundamental22 | pseudo（伪集，永不复检） | B 伪集 | 11-14 矩阵 §2（RIC↔BBID 映射表，waveBE242:265）；本 run 无动作 |
| fundamental45 | converged（保留量级参照） | A 已收敛 | 11-14 矩阵 §2（QA 78 臂收敛 S≤1.04；基线 S 0.96/2Y 1.73/sub 0.72 = 本 run 三波的量级参照，waveBE242:35）；本 run 无动作 |
| **fundamental72** | **provisional（三波连续判弱入档；本 run 无终态转换）** | 本 run 焦点 | 本 run 三波（§1）+ S0 FND72 档 §3.2（11-14 死档 DEU-FND72-NARROW-BREADTH 不满足六维只能 PROVISIONAL 级；D2/D5/D6 未达，本 run 后 D1 互异性/D3/D6 仍未达）⇒ 起点与终点均 provisional，无转换；数据面无宽度塌缩（三波 LC 59–104/SC 57–157）无 data_excluded 集；**不外推为邻接集先验** |
| fundamental86 | active（11-14 判定；本 run 无动作） | — | 11-14 矩阵 §1/§2（w1 十臂 bestSharpe 0.91/近闸×2/insider 字段数据层排除）；其 w1 行与本 run fnd72 w1 **共享 wave_results 行 id 2174**（契约合并式追加，两槽条目并存：fnd86 条目逐字保留 + [fnd72] 前缀 8 条，verdict=PARTIAL 两槽同值） |
| fundamental89 | dead（六维终判死，2026-11-14） | A 已收敛 | 11-14 矩阵 §2（waveBE242:240-251 + 死档 id 1576）；**不外推为 fnd72 先验**（waveBE242:251 明文）；本 run 无动作 |
| fundamental90 | capped（塔位储备已入册） | A 已收敛 | 11-14 矩阵 §2（42 臂 S 平台 0.84–0.88；2Y 塔位 ×4）；本 run 无动作 |
| fundamental93 | converged（实质关闭） | A 已收敛 | 11-14 矩阵 §2（12 臂水平 ≤0.53 + 论坛 no_result）；本 run 无动作 |
| alpha_factor_lib | data_excluded | C 数据层排除 | 11-14 矩阵 §2（BE251 超窄账户签名）；本 run 无动作 |
| digital_ad_spend | data_excluded | C 数据层排除 | 11-14 矩阵 §2（探针 lc 25/sc 25 + CW 0.5 挂；数据层排除非信号死）；本 run 无动作 |

排除面小结：12 集中 11 集三型排除状态与 11-14 矩阵一致（无变更）；fnd72 为本 run 唯一动过的集（3 波 25 臂，provisional 维持）。

### §2.1 fnd72 行的两处更正登记（不回改他槽档案）

1. **WjOLdO7o 归属误记**：11-14 矩阵 §2 fnd72 行引「EBIT 主面近闸件 WjOLdO7o 1.42/2Y 1.82」——该件是 **fundamental45 电话会 NLP 的 LDA 主题臂**，非 fnd72（`S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md` §七更正，引 s2_nearmiss_rescue_20261104.md:4930/:4941 原文「对比 fundamental72 的 KPJmRpGN」）；**fnd72 的近闸资产 = KPJmRpGN（S 1.38/2Y 1.58 已触闸）/RREALzx0（S 1.42/2Y 1.43），均 FAST 格，DB 原值（get_alpha_by_id，S0 档 §3.1）**。
2. **「主面不再加注」处置被取代**：11-14 矩阵引 waveBE242:421 处置——11-14 后半用户指定 fnd72 为目标集重开 S0（S0 FND72 档 §七明文「两档并存」），本 run 三波即在该授权下执行；旧处置仅对「11-14 上午槽期望值判断」成立。

## §3 本 run 产物索引（atom_orthogonal/）

| 文件 | 内容 |
|---|---|
| S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md | 目标集重开 S0：判死闸距离核对（六维）+ 12 集排除面 + 判读基准 + WjOLdO7o 归属更正（§七） |
| WAVE_w1_fundamental72_20261114.md | w1 十臂逐臂归因（provisional / 0.68 / near×1 / 平台撞件 / 配置 7x 对照 / w1 共享行合并写入 §9） |
| WAVE_w2_fundamental72_20261114.md | w2 八臂逐臂归因（provisional / 0.25 / near×2 / 门控-2Y 假设证伪 / 形态-2Y 杠杆入册 / w2 clean insert） |
| WAVE_w3_fundamental72_20261115.md | w3 七臂逐臂归因（provisional / 0.21 / near 空 / verdict FAIL / gBF-CW 反证杠杆入册 / UNITS 缠绕臂低可靠登记） |
| CATEGORY_MATRIX_FUNDAMENTAL_20261115.md | 本档 |

- DB 侧：wave_results 三行（id 2174 合并更新 / 2183、2188 插入，全部 closed、pipeline:auto）；backtest_results fnd72 共 25 行（w1 10 + w2 8 + w3 7）+ expressions 25 行（本槽聚合核验 `logs/_tmp_fnd72_dayclose_verify.py` 实跑）。
- 同期他槽产物（非本 run，仅列名）：`CATEGORY_MATRIX_FUNDAMENTAL_20261114.md`、`S0_DATASET_SCAN_FUNDAMENTAL_20261114.md`、`WAVE_w1_fundamental86_20261114.md`（fnd86 w1 十臂，其 backtest/expressions 10 行与本 run w1 共享标签、以 dataset 列区分）。
- 一次性核验脚本（logs/，用完可删）：`_tmp_fnd72_w1_attr_verify.py` / `_tmp_fnd72_w1_merge_diff.py` / `_tmp_fnd72_w2_attr_verify.py` / `_tmp_fnd72_w3_attr_verify.py` / `_tmp_fnd72_dayclose_verify.py`。

## §4 提交链与待确认

- **待用户确认候选：[]（rollup 给定，本 run 无）**。本 run 三波 25 臂无一条进入提交链语境（全部 RA fail；近闸载体均为 2Y 轴载体非 S 候选）。
- **跨波待处理提交链候选：无（rollup 给定）**。⚠ 状态差异如实登记：11-14 矩阵 §4 曾登记跨波候选 1YW6xk3W（fnd86，prod 已判净未跑链）——其后续处置不在本 run 范围，本 run rollup 未列，**现状本槽无读数、不作推断**。
- 本 run 内「先测 prod 再扫参」待办（下一槽，非提交候选）：波1–2 近闸载体 LLKO3vZ9（2Y 1.51）/gJaqYgQl（2Y 1.53）/A1xJRr0l（2Y 1.20）的 prod/self 均未测（三波归因档均登记「相关性查询未做（单槽在相关性员）」）；fnd72 在册近闸资产 KPJmRpGN/RREALzx0 的 prod/self 亦未测（S0 档 §3.3.2，零仿真配额即可判定）。
- 波 4 前置已满足：4 探针开门线全过（cf_cash_from_oper/cf_net_inc/bs_q_1_tot_asset/季度水平格，LC+SC 134–155 ≥50，死档 1573 协议）。

## §5 变更声明

- **本 run 无数据集终态变更**（rollup 给定；fnd72 三波均 provisional——起点即 provisional 级（S0 §3.2：11-14 死档不满足六维只能 PROVISIONAL），终点 provisional，无 dead_proposed/data_excluded/capped 转换）。
- fnd72 standing state（供下一槽引用）：**provisional，判弱入档**——S 面 @SUBINDUSTRY 格三波死（best 0.68/0.25/0.21），2Y 裸锚活体（1.51/1.53）+ 未扫自由度（FAST 配置轴/比值·SNR 腿/宇宙·delay/裸 rank 门控形未派发）= 下波设计输入；判死引用前必须先补 D3 比值腿 + D6 第二配置（AGENTS §7.6）。
- 本 run 判死动作：无。data_excluded 动作：无（臂级/字段级均无新增；w2 的 insider 字段排除属 fnd86 他槽波）。

## §6 盲区与证据通道声明

- DEU 的 query_dataset_profile / query_field_profile 全 0 行（S0 FND72 档 §6 本会话实读）⇒ 逐集状态不走 profile 表，全部以 S0 盘点 + 11-14 矩阵 + 本 run 三档四通道为准。
- expressions/backtest_results 表不含 MCP 直连仿真盲区已知（AGENTS §8.11 ⑦）；本 run 25 臂由收割步骤⑥⑦回执 + 本槽逐波只读核验覆盖（logs/_tmp_fnd72_w{1,2,3}_attr_verify.py，10/8/7 行级一致）。
- wave_results 无 dataset 列：w1 标签被 fnd86（早槽）/fnd72（本 run）共用，行 id 2174 按契约合并式追加（fnd86 条目逐字保留已写后 diff 核验）；w2/w3 clean insert。双集共享单行是结构性限制，遗留风险已在 WAVE_w1 档 §9 登记（建议区域配置治理立项）。
- 本矩阵零平台调用、零 DB 写入（唯一 DB 交互为本 run 三波的 wave_results/backtest 写入，回执已录 §1/§3）。
