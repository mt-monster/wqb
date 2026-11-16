# WAVE rt-fundamental-w3（精修波）— fundamental72 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-16；槽：regular_tower（纯本地归因；判读不改写邻接数据集先验，跨区不外推）
- 主集：`fundamental72`（目标塔 FUNDAMENTAL）；本波**无 insiders 臂**（10/10 单集件，全部只引用 fnd72 字段）
- 配置（平台回显，DB payload 逐臂一致）：DEU/TOP500/D1、neutralization=FAST、decay=0、truncation=0.08、nanHandling=ON、maxTrade=OFF、FASTEXPR；平台回显 `startDate=2014-01-01`、`endDate=2023-12-31`
  - 与 `tracking/DEU/config/settings.json:16-17`（2013-01-01 起）不同；`create_multi_simulation` 无 startDate/endDate 参数（`world-quant-brain-mcp/tools_sim.py:672-690`）。本档原样记录平台值。
- 派发/收割：**ask 未提供本波的 multisim id、preflight、operator_audit、查重记录**——本档不虚构，相关盲区登记于 §11。读数来源 = ask 臂序转录 + 本槽 DB 只读核验。
- 判读基准（ask 给定）：S≥1.58 / F≥1.0 / sub≥1.0（本地 review 线；平台 LOW_SUB limit 动态，本波 fail 清单未出现 LOW_SUB）/ TO 0.01–0.70 / margin≥0.0005（5bp，`tracking/DEU/config/thresholds.json:7`）/ prod&self corr≤0.70；CW 用**平台 limit 0.1**（`thresholds.json:20` 的 0.5 只是本地 review 线）。
- 2Y 闸种：本波 **10/10 臂为单数据集件**（expressions `atom_flag=atom`、`atom_n_datasets=1`；DB `alphas.is_ladder_sharpe` 全 null），全部走 `LOW_2Y_SHARPE`（limit 1.58）；**无多数据集件**，IS_LADDER 三处一致条款本波不适用（非漏检）。
- 符号指纹：本波仍**无翻符号对照臂**（0 条 multiply(-1,…)；settings decay 固定 0）。`ts_decay_linear(5/22)` 是算子内时间衰减，不是符号翻转，也不是 settings decay 扫描。⇒ 本波不对方向做裁定。

## §0 前置更正（w2 档 tail 归因）

w2 档 §9/newLever 写「w1 `LLKX7rxL` → w2 `d5a7PrpK` 唯一差异是 tail 壳」。**本波复核 expressions 原文后更正：该对照实际有两处差异**——
- w1 LLKX7rxL：`group_rank(multiply(rank(δ240), rank(δ176), **rank(ts_rank(p,1008))**), sector)`
- w2 d5a7PrpK：`tail(group_rank(multiply(rank(δ240), rank(δ176), **ts_rank(p,1008)**), sector), 0.12/0.88/0.5)`

即 w1→w2 同时（a）加了 tail 壳、（b）去掉了 `ts_rank` 外层的 `rank()`。**因此 w2 的「+0.09/+0.06/+0.37/+0.23 全部由 tail 贡献」不成立**（至少混入了 rank 包装层的贡献）。本波用 w2/w3 的干净带宽对照（三臂同为 raw `ts_rank`，只差带宽）重建结论（§3）；w2 档本文不回改，按「同一档案追加」原则在其末尾补更正条。

## §1 臂序读数表（原样转录，按臂序，勿按 alpha id 猜）

| # | alphaId | 结构（简） | S | F | 2Y（LOW_2Y） | sub | TO | DD | margin | LC/SC | 塔（effective） | RA fail（DB `ra_failed_checks`） |
|---|---|---|---|---|---:|---|---:|---:|---|---:|---|---|
| 1 | qM7z2P1Z | **C0 对照**：`group_rank(multiply(rank(δ(oper_inc,240)÷ts_mean(assets,240)), ts_rank(p,1008)), sector)`（增量 ROA 核，raw ts_rank） | 1.48 | 1.02 | 1.64 | 0.95 | 15.05% | 8.86% | 0.000942 / 9.42bp | 185/198 | FUNDAMENTAL×1.8（1） | 1：[LOW_SHARPE 1.48<1.58]；⚠ 平台 `checks.fail=[]`，在 warning 桶 |
| 2 | O0WmdbYp | C0 + `tail(0.12/0.88/0.5)` | 1.35 | 0.86 | 1.71 | 0.84 | 17.89% | 6.60% | 0.000808 / 8.08bp | 215/167 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, LOW_FITNESS] |
| 3 | ZYalV250 | C0 + `tail(0.15/0.85/0.5)` | 1.43 | 0.93 | 1.77 | 0.96 | 17.47% | 7.89% | 0.000855 / 8.55bp | 211/172 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, LOW_FITNESS] |
| 4 | 6XMq6a8G | C0 + `winsorize(std=1.5)` | 1.42 | 0.95 | 1.72 | 0.96 | 14.77% | 10.98% | 0.000896 / 8.96bp | 189/193 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, LOW_FITNESS] |
| 5 | N1PjEgwE | C0 + `winsorize(std=1.0)` | 1.34 | 0.87 | 1.80 | 0.94 | 14.65% | 12.53% | 0.000851 / 8.51bp | 196/186 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, LOW_FITNESS] |
| 6 | j2awk9RE | C0 + `ts_decay_linear(5)` | 1.43 | 1.02 | **1.56** | 0.90 | 13.51% | 8.57% | 0.001012 / 10.12bp | 185/197 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, **LOW_2Y 1.56<1.58（差 0.02）**] |
| 7 | A1xaXgZY | C0 + `ts_decay_linear(22)` | 1.35 | 0.97 | **1.53** | 0.82 | 12.67% | 8.05% | 0.001027 / 10.27bp | 186/197 | FUNDAMENTAL×1.8（1） | 3：[LOW_SHARPE, LOW_FITNESS, **LOW_2Y 1.53**] |
| 8 | 1YWm3abz | C0 换分组轴 `industry`（sector→industry） | 1.39 | 0.90 | 1.64 | 0.90 | 15.18% | 8.85% | 0.000830 / 8.30bp | 185/197 | FUNDAMENTAL×1.8（1） | 2：[LOW_SHARPE, LOW_FITNESS]；⚠ `checks.fail=[]`，CLUSTER 0.86 在 warning |
| 9 | O0WmdbPR | **三年窗核 + tail(0.10/0.90)**：`tail(group_rank(multiply(rank(δ240), rank(δ176), ts_rank(p,1008)), sector), 0.10, 0.90, 0.5)` | **1.56** | **1.05** | **2.41** | **1.18** | 18.30% | 8.02% | 0.000906 / 9.06bp | 218/164 | FUNDAMENTAL×1.8（1） | **1：[LOW_SHARPE 1.56<1.58（差 0.02）]**；F/2Y/sub/CW/CLUSTER 全 pass |
| 10 | 88N6Wa9W | 三年窗核 + tail(0.15/0.85) | **1.53** | **1.02** | **2.10** | **1.09** | 17.63% | 6.50% | 0.000889 / 8.89bp | 211/171 | FUNDAMENTAL×1.8（1） | **1：[LOW_SHARPE 1.53<1.58（差 0.05）]**；F/2Y/sub/CW/CLUSTER 全 pass |

- DB 只读核验（sqlite `mode=ro`，零写入）：10 行 backtest 指标与 ask 逐值一致；`ra_failed_checks` 与平台 `ra.failed_ra_count`/名单一致；payload `settings` 逐臂为 FAST/decay0/TOP500/D1/2014-01-01→2023-12-31；`pyramids` 10/10 = `DEU/D1/FUNDAMENTAL`×1.8（effective=1）。
- ⚠ **checks 表示不一致（平台原文）**：臂1（qM7z2P1Z）`checks.fail=[]` 但 `ra.failed_ra_count=1`、ra 名单含 LOW_SHARPE；臂8（1YWm3abz）`checks.fail=[]` 但 ra 名单含 LOW_SHARPE/LOW_FITNESS（CLUSTER 0.86 在 warning）。本档判「0 达标」以 `ra_failed_checks` 为准（AGENTS §8.7：RA 资格门失败含 WARNING/ERROR），`checks.fail` 原文照录；只看 `checks.fail=[]` 会把臂1/8 误判成通过。

## §2 逐臂归因条目

1. **臂1 qM7z2P1Z（C0 对照，增量 ROA 核 + raw `ts_rank`）**：S 1.48/F 1.02/2Y 1.64/sub 0.95/TO 15.05%/DD 8.86%/margin 9.42bp/LC 185-198；RA fail 1=LOW_SHARPE（checks.fail 空，§1 注）。**vs w2 arm5 YPak9o6q**（同核但 `rank(ts_rank)`，1.52/1.05/1.67/0.98）：S −0.04/F −0.03/2Y −0.03/sub −0.03 ⇒ `ts_rank` 外层 `rank()` 是**小幅正贡献（约 +0.03~0.04）**；C0 是干净的壳层对照基线（臂2-8 与它逐项同核）。
2. **臂2 O0WmdbYp（C0 + tail 0.12）**：S 1.35/F 0.86/2Y 1.71/sub 0.84/TO 17.89%/DD 6.60%/margin 8.08bp/LC 215-167；RA fail 2。**vs C0**：S −0.13/F −0.16/**2Y +0.07**/sub −0.11/TO +2.84pp/DD −2.26pp。⇒ **tail 0.12 在增量 ROA 核上伤害 S/F/sub**，只小幅拉 2Y；与"tail 在三年窗核上增益"方向相反 ⇒ **tail 杠杆依赖核心几何，不可外推**（§3）。
3. **臂3 ZYalV250（C0 + tail 0.15）**：S 1.43/F 0.93/2Y 1.77/sub 0.96/TO 17.47%/DD 7.89%/margin 8.55bp/LC 211-172；RA fail 2。**vs C0**：S −0.05/F −0.09/2Y +0.13/sub +0.01；**vs 臂2（0.12→0.15）**：S +0.08/F +0.07/2Y +0.06/sub +0.12。⇒ 在增量 ROA 核上，**宽 tail（0.15）优于窄 tail（0.12）**，但两者仍低于裸 C0 的 S/F；tail 在本核上只能换 2Y，不能提 S。
4. **臂4 6XMq6a8G（C0 + winsorize std=1.5）**：S 1.42/F 0.95/2Y 1.72/sub 0.96/TO 14.77%/DD 10.98%（本波最高）/margin 8.96bp/LC 189-193；RA fail 2。**vs C0**：S −0.06/F −0.07/2Y +0.08/sub +0.01/TO −0.28pp。⇒ winsorize 1.5 是"S/F 换 2Y"的小幅压缩器，DD 反而升。
5. **臂5 N1PjEgwE（C0 + winsorize std=1.0）**：S 1.34/F 0.87/2Y 1.80/sub 0.94/TO 14.65%/DD 12.53%/margin 8.51bp/LC 196-186；RA fail 2。**vs 臂4（1.5→1.0）**：S −0.08/F −0.08/2Y +0.08/sub −0.02；**vs C0**：S −0.14/F −0.15/2Y +0.16/sub −0.01。⇒ 收紧 winsorize 更伤 S/F、多换 2Y；**std=1.5 是本核较优点，但裸 C0 在 S/F 面仍最优**。
6. **臂6 j2awk9RE（C0 + ts_decay_linear 5）**：S 1.43/F 1.02/2Y **1.56**/sub 0.90/TO **13.51%**（本波最低）/DD 8.57%/margin **10.12bp**/LC 185-197；RA fail 2（LOW_SHARPE + **LOW_2Y 1.56<1.58，差 0.02**）。**vs C0**：S −0.05/F 0.00/**2Y −0.08**/sub −0.05/TO −1.54pp/margin +0.70bp。⇒ `ts_decay_linear(5)` 确实压换手、提 margin，但**把 2Y 从 1.64 压到 1.56、刚好跌破 1.58 闸**，且 S 不升 ⇒ **decay 不是 S 工具，且会破坏 2Y 闸**（与族内 settings decay 0/2/4 负杠杆同向）。
7. **臂7 A1xaXgZY（C0 + ts_decay_linear 22）**：S 1.35/F 0.97/2Y **1.53**/sub 0.82/TO 12.67%/DD 8.05%/margin 10.27bp/LC 186-197；RA fail 3（LOW_SHARPE, LOW_FITNESS, LOW_2Y）。**vs 臂6（5→22）**：S −0.08/F −0.05/2Y −0.03/sub −0.08/TO −0.84pp ⇒ **decay 长度 5→22 单调负**（本波两档）；margin 再 +0.15bp 但 S/2Y 双跌。⇒ `ts_decay_linear` 路线在本核上**死轴**。
8. **臂8 1YWm3abz（C0 换分组轴 sector→industry）**：S 1.39/F 0.90/2Y **1.64（与 C0 相同）**/sub 0.90/TO 15.18%/DD 8.85%/margin 8.30bp/LC 185-197；RA fail 2（checks.fail 空）、CLUSTER 0.86 warning。**vs C0 sector**：S −0.09/F −0.12/2Y 0.00/sub −0.05。⇒ **sector 严格优于 industry**（S/F/sub 全高、2Y 不变）；industry 只省 0.05pp 换手。与 NEARGATE §B3「industry −0.11」方向一致（那是三年窗核，本波是单变量直接验证）。
9. **臂9 O0WmdbPR（三年窗核 + tail 0.10）**：S **1.56**/F **1.05**/2Y **2.41**/sub **1.18**/TO 18.30%/DD 8.02%/margin 9.06bp/LC 218-164；RA fail **1=LOW_SHARPE（差 0.02）**，F/2Y/sub/CW/CLUSTER 全 pass。**本波最佳、fnd72 历史最佳 S（破 w2 1.52、族峰 1.50）**。与 mLaALJX2（1.50/1.04/2.30/1.12/TO 16.31%/margin 9.55bp）读数对比：S +0.06/F +0.01/2Y +0.11/sub +0.06，但 TO +1.99pp、margin −0.49bp——**mLaALJX2 带 winsorize(std3)+hump(0.003)+tail0.12，本臂只有 tail0.10，多个变量不同，只作读数对照、不作单变量归因**。
10. **臂10 88N6Wa9W（三年窗核 + tail 0.15）**：S **1.53**/F **1.02**/2Y **2.10**/sub **1.09**/TO 17.63%/DD **6.50%**（本波最低）/margin 8.89bp/LC 211-171；RA fail **1=LOW_SHARPE（差 0.05）**，F/2Y/sub/CW/CLUSTER 全 pass。**vs 臂9（0.10→0.15）**：S −0.03/F −0.03/**2Y −0.31**/sub −0.09/TO −0.67pp/DD −1.52pp ⇒ 放宽带宽换低 DD/略低换手，代价是 2Y/sub 大幅下降。**vs w2 arm7（0.12）**：S +0.02/F +0.02/2Y −0.23/sub −0.05——0.15 相对 0.12 是 S 微升、2Y/sub 下降的混合。

## §3 带宽 / 杠杆结论（本波重点）

### 3.1 三年窗核：tail 带宽曲线（0.10 / 0.12 / 0.15 为干净对照——三臂均为 raw `ts_rank`，只差带宽）

| 带宽 | 臂（波） | S | F | 2Y | sub | TO | DD | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 裸（无 tail）* | w1 LLKX7rxL | 1.42 | 0.94 | 1.96 | 0.91 | 15.28% | 9.30% | 8.69bp |
| **0.10** | w3 臂9 O0WmdbPR | **1.56** | **1.05** | **2.41** | **1.18** | 18.30% | 8.02% | 9.06bp |
| 0.12 | w2 臂7 d5a7PrpK | 1.51 | 1.00 | 2.33 | 1.14 | 18.11% | 7.47% | 8.69bp |
| 0.15 | w3 臂10 88N6Wa9W | 1.53 | 1.02 | 2.10 | 1.09 | 17.63% | 6.50% | 8.89bp |

\* 裸臂含 `rank(ts_rank)`，与三条 tail 臂的 raw `ts_rank` 不同 ⇒ **裸列不作单变量锚**（§0 更正）。

**干净带宽对照（同核同 raw ts_rank）**：
- **0.10 vs 0.12**：S **+0.05**、F +0.05、2Y **+0.08**、sub **+0.04**、TO +0.19pp、DD +0.55pp、margin +0.37bp ⇒ 0.10 全面优于 0.12。
- **0.10 vs 0.15**：S **+0.03**、F +0.03、2Y **+0.31**、sub **+0.09**、TO +0.67pp、DD +1.52pp ⇒ 0.10 全面优于 0.15（除 DD 更高）。
- **0.15 vs 0.12**：S +0.02、F +0.02、2Y **−0.23**、sub −0.05、TO −0.48pp ⇒ 0.15 只在 S 微胜 0.12，2Y/sub 更差。

**结论（带宽）**：在本核已扫范围内，**0.10 是最优点**；2Y/sub 随带宽放宽**单调下降**（2.41→2.33→2.10、1.18→1.14→1.09），S 非单调（0.15>0.12）。⚠ **0.10 是扫描边界值，不是已证内点峰**——NEARGATE §四 记的「0.12–0.15 峰」是在 `winsorize(std3)+hump(0.003)` 包装核上测的；本波裸核上 0.10 反超 ⇒ **带宽峰随核心/包装层变化，不是常数**。下一波必须补 **0.05/0.08**（同核同 raw ts_rank，单变量）再判定峰位；在补测前不得把 0.10 写成"全局最优带宽"。

### 3.2 增量 ROA 核：壳层杠杆全部为负（C0 为基线）

| 壳 | 臂 | S | F | 2Y | sub | TO | DD | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 无（C0） | qM7z2P1Z | **1.48** | **1.02** | 1.64 | 0.95 | 15.05% | 8.86% | 9.42bp |
| tail 0.12 | O0WmdbYp | 1.35 | 0.86 | 1.71 | 0.84 | 17.89% | 6.60% | 8.08bp |
| tail 0.15 | ZYalV250 | 1.43 | 0.93 | 1.77 | 0.96 | 17.47% | 7.89% | 8.55bp |
| winsorize 1.5 | 6XMq6a8G | 1.42 | 0.95 | 1.72 | 0.96 | 14.77% | 10.98% | 8.96bp |
| winsorize 1.0 | N1PjEgwE | 1.34 | 0.87 | 1.80 | 0.94 | 14.65% | 12.53% | 8.51bp |
| ts_decay_linear 5 | j2awk9RE | 1.43 | 1.02 | 1.56 | 0.90 | 13.51% | 8.57% | 10.12bp |
| ts_decay_linear 22 | A1xaXgZY | 1.35 | 0.97 | 1.53 | 0.82 | 12.67% | 8.05% | 10.27bp |
| industry 轴 | 1YWm3abz | 1.39 | 0.90 | 1.64 | 0.90 | 15.18% | 8.85% | 8.30bp |

**结论（杠杆）**：
1. **tail 杠杆不可跨核外推**：在三年窗核上 0.10/0.12/0.15 均高于裸臂（但因 rank 包装混淆，净增益幅度不可精确归因）；在增量 ROA 核上 **tail 0.12/0.15 均低于裸 C0 的 S/F**（−0.13/−0.16 与 −0.05/−0.09）⇒ tail 是**核相关杠杆**，不是通用免费增益。
2. **winsorize**：std 1.5 > std 1.0（S/F 面）；两者均低于裸 C0 的 S/F，但 2Y 分别 +0.08/+0.16 ⇒ 只宜作"2Y 补偿件"，不宜作 S 工具；std 1.0 的 DD 12.53% 过高。
3. **ts_decay_linear**：5 > 22（S/F/2Y/sub 全高），但**两档均低于裸 C0 的 S 与 2Y**；5 档把 2Y 压到 1.56（跌破 1.58 闸，差 0.02），22 档 1.53。⇒ **decay 路线在本核为死轴**，与族内 settings decay 0/2/4 负杠杆、以及"加 decay 提 S 的臂一律不派"的纪律同向；本次是**算子内 decay（ts_decay_linear）**的独立确认。
4. **分组轴**：sector > industry（S +0.09/F +0.12/sub +0.05，2Y 相同）⇒ 保持 sector；industry 不构成替代轴。
5. **C0 的 rank 包装**：`rank(ts_rank)` 相对 raw `ts_rank` 约 +0.03~0.04（从 w2 arm5 vs w3 C0 的四项差推得）——小正贡献，但足以说明 w2 的 tail 归因必须扣除这项。

### 3.3 全局最优结构

**三年窗核 + tail 0.10（臂9）**：S 1.56 / F 1.05 / 2Y 2.41 / sub 1.18 / TO 18.30% / margin 9.06bp / DD 8.02%，**唯一 FAIL=LOW_SHARPE（差 0.02）**。这是 fnd72 在 DEU 的历史最佳 S（前高 w2 1.52、族峰 1.50）。离全闸只差 0.02，且 2Y/sub 均有厚余量。

## §4 符号指纹 / 稀释铁律 / 跨区核对

- **符号指纹：未测**。无整式反号臂；`ts_decay_linear` 不改变符号；settings decay 固定 0。⇒ 不能按「衰减对称=机制在/符号错；单向=事件型」判定；本波不对方向做裁定。近闸件（O0WmdbPR / 88N6Wa9W）推进前应补反号对照（w1/w2 已连续登记该缺口）。
- **稀释铁律**：本波**零 bucket、零多腿加法复合**；两腿乘法核（rank(δROA)×ts_rank）相对单腿基准 w1 `omazqreb` 1.29 全在 1.34–1.56（均 ≥ 单腿）⇒ **不触发乘法稀释**。壳层（tail/winsorize/decay）低于裸核属于"包装层负杠杆"，与"乘法/bucket 低于单腿=稀释"是不同判据，分开登记（§3.2），不混写为稀释命中。
- **跨区不外推**：零 TWN/KOR 引用；对照全部 DEU 域内（w1/w2 臂、mLaALJX2、本波 C0）。fnd45/fnd86/fnd89/fnd90 邻接集先验未改写；insiders1 本波未测、状态不变（沿用 w1/w2：不判死、无可推进结构）。

## §5 塔位判读（点塔相关性）

平台 payload `pyramids` 原文（逐臂回读）：10/10 臂 = `DEU/D1/FUNDAMENTAL` ×1.8、effective=1。

- **目标塔 FUNDAMENTAL 出现 10/10 臂归属**（本波无 insiders 臂、无双塔件、无多数据集件）。
- **点位≠点亮**：10/10 臂 RA fail≥1，无一条过全闸；本波塔位实际贡献 = 0。但臂9 距全闸 0.02（唯一 LOW_SHARPE），是 fnd72 塔最接近点亮的单件。
- 单塔件（effective=1）占满全波 ⇒ 本波不涉及双塔配位/配额问题。

## §6 数据层判读（data_excluded 与信号死分开）

- **本波零 data_excluded 臂**：LC/SC 164–218 全宽，无 LC/SC≤5；无宽度塌缩。
- **CW 10/10 全 pass**：本波无 insiders 腿，CW 挂闸（数据层指纹）未出现；与 w1/w2 的 insiders 臂形成对照，进一步支持「CW 挂由 insiders 持仓宽度驱动」的判读。
- **无判死**：本波 10 臂但结构互异 <10（§7），按探针条款不判死；fundamental72 不 data_excluded、不判死。
- fundamental72 `coverage=0` 仍是平台元数据退化（`FIELD_fundamental72_20261115.md` §2），不作可用性判据。

## §7 判死六维闸盘点（D1–D6；本波自身口径）

| 维 | 本波现状 | 判定 |
|---|---|---|
| D1 结构互异模板 ≥10 | 名义 10 臂，互异机制 ~4：增量 ROA 两腿核（C0 + 壳层 8 变体）、三年窗核 + tail 带宽（0.10/0.15）、winsorize/decay/industry 轴——大部分是同一核的包装层变体 | **✗ 未达** |
| D2 字段族自测 | 本波只碰 **2 个 fnd72 字段**（oper_inc、tot_asset）；fnd72 共 1031 字段 | **✗ 远未达** |
| D3 矩全家 | 一阶差（δ240/δ176）✓、比值（oper_inc÷assets）✓；**缺**二阶波动、信噪比、纯水平腿 | **✗ 未达** |
| D4 分组轴 ≥2 | sector（臂1-7/9/10）、industry（臂8） | ✓ |
| D5 非线性 ≥1 | ts_rank、group_rank、tail、winsorize、ts_decay_linear、multiply | ✓ |
| D6 配置 ≥2 | 本波固定 FAST/decay0/TOP500/D1 **一套** | **✗ 本波自身未达**（跨槽累计有 SUBINDUSTRY 三波，非本波读数） |

⇒ 缺 D1/D2/D3/D6：**不得判死、不得封集、不得作为邻接集先验**（AGENTS §7.6）。

## §8 近闸候选（≤2，按 S 降序；先测 prod 再扫参）

| 序 | alphaId | S | 触发原因（读数引用） |
|---|---|---|---|
| 1 | `O0WmdbPR` | **1.56** | S≥1.2；距 S 硬闸 1.58 差 **0.02**≤0.4；**唯一 FAIL=LOW_SHARPE**；F 1.05/2Y 2.41/sub 1.18/CW pass/CLUSTER pass/margin 9.06bp/TO 18.30%；fnd72 历史最佳 S |
| 2 | `88N6Wa9W` | **1.53** | S≥1.2；距 S 硬闸差 **0.05**≤0.4；**唯一 FAIL=LOW_SHARPE**；F 1.02/2Y 2.10/sub 1.09/CW pass/CLUSTER pass/margin 8.89bp/TO 17.63%；DD 6.50% 本波最低 |

- 排序外登记（如实）：`qM7z2P1Z` S 1.48（距 0.10、唯一 LOW_SHARPE）、`ZYalV250` 1.43、`j2awk9RE` 1.43（2Y 1.56 距 0.02 也近，但 S 更低）、`6XMq6a8G` 1.42、`1YWm3abz` 1.39、`O0WmdbYp` 1.35、`A1xaXgZY` 1.35、`N1PjEgwE` 1.34——均满足 S≥1.2 或距某硬闸 ≤0.4，按 S 降序全部出局（全量读数见 §1）。
- **prod/self 未测（本波全 null，相关性查询按分工未做）**：两条候选均为 fnd72 核心件（无搭档/insiders 腿）——按「prod 雷在核心不在搭档」，先测 prod 再决定扫参。族内先验 mLaALJX2 prod 0.5444（<0.70）是利好但不同表达式，不构成保证。
- **年度分年未取** ⇒ 2018/2019/2020 时间集中度**未验证**。族级既有读数（`S0_TOWER_SCAN_20261115.md:130`：mLaALJX2 2018 0.80/2019 0.80/2020 −0.35，2021–2023 3.03/2.60/1.96）提示该族存在时间集中风险。**推进前必须补分年**；若 2018/2019/2020 仍全 <1.0 而总 S 靠 2021–2023 撑起，按「时间集中度风险」登记，**不得按可提交推进**。
- **mode_b_qualification**（`thresholds.json:23-27`）：臂9 S 1.56≥1.25 且 F 1.05≥0.8、臂10 S 1.53/F 1.02 均过线 ⇒ 有资格进 Mode B 组合增强/继续优化。

## §9 datasetStatus 裁决 + 波 verdict

**datasetStatus = active（继续加注；维持 w2 的 active，无终态转换）**。依据：

1. **S 面再破纪录**：臂9 S 1.56（距 S 闸 0.02）、臂10 1.53；双双高于 w2 best 1.52、族峰 mLaALJX2 1.50、11-15 atom 槽 best 1.47。F 1.05/1.02、2Y 2.41/2.10、sub 1.18/1.09 全部过线。
2. **无数据层排除**：LC/SC 164–218 全宽、CW 10/10 pass、无宽度塌缩 ⇒ 不满足 data_excluded。
3. **不得判死/封集**：D1/D2/D3/D6 未达（§7），AGENTS §7.6 六维闸禁止终判死；本波亦不作邻接集先验。
4. **未到 capped**：0 达标（全部 RA fail≥1），无一条过全闸；active 不是终态，仍需补 prod/分年与 S 侧 0.02。
5. **insiders1**：本波未测（零 insiders 臂），状态沿用 w1/w2（不判死、无可推进结构）；本波不对其做新判读。

**波 verdict = PARTIAL**（判定表 `src/wqb/wave_results_contract.py:79-90`：0 达标 + ≥1 近闸 ⇒ PARTIAL；`n_pass=0 / n_near=2`）。禁止自造枚举。

## §10 newLever 登记（带宽精修，带归因对照）

**tail 带宽 0.10（三年窗核）为已扫最优点；带宽杠杆随核心几何变化，不可外推**：
- **干净带宽对照（同核同 raw `ts_rank`，仅带宽变）**：0.10（O0WmdbPR 1.56/1.05/2.41/1.18）vs 0.12（d5a7PrpK 1.51/1.00/2.33/1.14）⇒ **S +0.05 / F +0.05 / 2Y +0.08 / sub +0.04**；0.10 vs 0.15（88N6Wa9W 1.53/1.02/2.10/1.09）⇒ **S +0.03 / F +0.03 / 2Y +0.31 / sub +0.09**。2Y/sub 随带宽放宽单调下降，S 非单调。
- **几何依赖反证（同波干净对照）**：在增量 ROA 核上，tail 0.12（1.35/0.86/1.71/0.84）与 tail 0.15（1.43/0.93/1.77/0.96）**均低于裸 C0（1.48/1.02/1.64/0.95）的 S/F**（−0.13/−0.16 与 −0.05/−0.09）⇒ **tail 不是通用杠杆**；在三年窗核上增益、在增量 ROA 核上害 S。
- **caveat（必须随杠杆一起记）**：① 0.10 是扫描边界值，**不是已证内点峰**；NEARGATE §四 的 0.12–0.15 峰是在 winsorize(std3)+hump(0.003) 包装核上测的，本波裸核上 0.10 反超 ⇒ **带宽峰随核心/包装层变化**；下一波须补 0.05/0.08 单变量再定峰；② w1→w2 的裸/壳对照混入 `rank(ts_rank)` 包装变化（§0），本档不沿用其"单变量 tail"结论；③ 0.10 的 TO 18.30% 高于裸臂 15.28%（+3.02pp），margin 9.06bp 仍 ≥5bp，但换手上升是带宽收窄的代价。

## §11 证据通道与盲区

- **读数来源**：ask 转录的臂序读数 + 本槽 DB 只读核验（sqlite `mode=ro`，零写入）：10/10 行 backtest 指标与 ask 逐值一致；`ra_failed_checks` 与平台 ra 名单一致；payload `settings` 逐臂 FAST/decay0/TOP500/D1/2014-01-01→2023-12-31；`pyramids` 10/10 FUNDAMENTAL×1.8、effective=1。
- **IS_LADDER**：本波 10/10 单数据集件（`atom_n_datasets=1`），全部走 LOW_2Y_SHARPE；DB `alphas.is_ladder_sharpe` 全 null ⇒ 三处一致条款不适用（非漏检）；DB `two_year_sharpe` 与 checks 值 10/10 一致。
- **checks 表示不一致**：臂1/臂8 `checks.fail=[]` 但 `ra.failed_ra_count=1/2` 且 ra 名单含 LOW_SHARPE（臂8 另含 LOW_FITNESS）——本档以 ra 名单判 0 达标（AGENTS §8.7）；`checks.fail` 原文照录。若只看 checks.fail，臂1/8 会被误判通过。
- **盲区（如实登记，不猜不补）**：
  1. **ask 未提供本波 multisim id / preflight / operator_audit / 查重记录**——本档不填写、不虚构；派发链证据缺口登记在此。
  2. 年度分年未取 → 2018/2019/2020 时间集中度未验证（§8）。
  3. prod/self 相关性未测（10 臂全 null）。
  4. 符号指纹未测（无翻符号对照臂）。
  5. create_multi_simulation 不暴露 startDate/endDate（`tools_sim.py:672-690`），平台回显 2014-01-01→2023-12-31 与 settings.json 2013-01-01 不同——原样记录平台值。
  6. 本波结构互异 <10，按探针条款不产生判死；六维 D1/D2/D3/D6 未达。

## §12 终态

- **波**：PARTIAL；0 达标 / 2 近闸；best S **1.56**（O0WmdbPR）/ best 2Y **2.41**（O0WmdbPR）；臂9 仅差 LOW_SHARPE 0.02，臂10 差 0.05。
- **数据集**：fundamental72 = **active**（维持，无终态转换；S 1.56 破 fnd72 历史纪录，D1/D2/D3/D6 未达 → 不判死、不封集）；insiders1 本波未测、不判死（沿用 w1/w2）。
- **提交链**：无（0 达标，无候选进入提交语境）。
- **下一波输入**：① 先测 `O0WmdbPR`/`88N6Wa9W` 的 prod/self，补 2018–2020 分年；② **带宽补测 0.05/0.08**（同三年窗核、raw ts_rank、单变量）以判定 0.10 是否为边界峰；③ 若要补 S 的 0.02，优先在 0.10 核上加 `rank(ts_rank)`（约 +0.03~0.04，需单变量验证）或试 0.08 与 rank 包装组合；④ **不要**在增量 ROA 核上叠 tail/winsorize/ts_decay_linear（本波全部低于裸 C0）；⑤ 不要动 settings decay（族内 0/2/4 负杠杆），`ts_decay_linear` 5/22 已证明压 2Y 且不升 S。

## §13 后续闭合（2026-11-16，w4 档）

- w4 已补 0.05/0.08 带宽（同三年窗核、raw ts_rank、sector、单变量）：0.05 **塌陷**（S 1.31/F 0.82），0.08 为 1.54/1.03/2Y 2.56/sub 1.21；⇒ **0.10（1.56/1.05/2.41/1.18）确认为 S/F 内点峰**，0.08 是 2Y/DD 峰；本档 §3「0.10 是扫描边界值」缺口关闭。
- w4 另证 **EBIT 核 0.08 为 RA 全闸 PASS**（1.62/1.12/2.54/1.16，failed_ra_count=0），且 EBIT 带宽 0.08→0.10→0.12 单调下降 ⇒ 带宽峰随字段核移动（oper_inc 峰 0.10 / EBIT 峰 0.08，已测最窄点）。
