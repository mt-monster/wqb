# WAVE w1（FAST 重派轮）— fundamental72 逐臂归因（DEU/TOP500/D1）

- 日期：2026-11-15；归因员：atom_orthogonal 单槽（纯本地归因；判读不改写邻接数据集先验，跨区不外推）
- 波标签：w1 重派轮（FAST 格）。w1 标签共享沿首轮处置（fnd86 早槽 16:19:51 / fnd72 SUBINDUSTRY 首轮 18:17:54 已合并于 wave_results 行 id 2174，`WAVE_w1_fundamental72_20261114.md` §9）；本档为 2026-11-15 的 FAST 格重设计轮独立档案，**不覆写 11-14 首轮档**（命名纪律同 S0 档：集名+日期后缀区分）
- 配置（收割自报，全臂一致，本轮**换格**）：DEU/TOP500/D1、**neutralization=FAST**、decay=4、trunc=0.08、nanHandling=ON、maxTrade=OFF、FASTEXPR——与 SUBINDUSTRY 三波（0.68/0.25/0.21 判弱，不复跑）的差别仅在分组格
- 派发链（收割自报）：① preflight 10 臂 valid=true、unknown_fields=[]、10/10 无 VECTOR 修复 → ② toolkit gate.py 静态闸 10/10 过（臂 1/2 重建式 12→9、臂 9 重建式 10→9 调用点，全部 <10 过 [OPS] 铁律；臂 1/2/9/3/4 [WINDOW] 176/240 非标告警不阻断，窗口逐字对齐近闸件 RREALzx0）→ ③ operator_audit 模式2（3 重建臂）safe=true 零幽灵算子 → ④ 查重双路：臂 3-8/10 七条与库内 expressions 逐字全同（id 108789-108795，status=backtested，今日 12:08:45 FAST 首轮派发已收割）→ 跳过不消耗仿真位；臂 1/2/9 三条重建式 vs 比对池 49 条无全同 → 派发 → ⑤ create_multi_simulation(3 臂) multisim id=7qtzrdPI53w9lgz1140D8l，在途 ≤1（≤2 红线内）→ ⑥ batch_status 90 秒轮询 3/3 COMPLETE 零 ERROR → ⑦ harvest_multisim_alphas 直接成功（未触发 404 兜底）、臂归属按平台 code 逐字核对（LLKqYgxn=q_ebit 双delta×bucket=臂1、ZYaqv2L0=q_is_oper_inc=臂2、gJawVRze=三腿取负=臂9）→ ⑧ upsert_backtest_rows(region=DEU, wave=w1, dataset=fundamental72, rows=3) n=3
- **本槽只读核验（本轮实跑 `logs/_tmp_fnd72_w1fast_attr_verify.py` / `_verify2.py` / `_verify3.py`，sqlite mode=ro，零写入）**：① 3 新臂 backtest 行逐值与臂序读数一致（S/F/2Y/sub/TO/margin/LC/SC/ra_failed_checks 全对；payload settings.neutralization=FAST、universe=TOP500、delay=1、decay=4 确认）；② 7 查重件 expressions id 108789-108795 与 ask 转录**逐字全同（verbatim=True ×7）**，3 重建式 id 108799-108801 同（verbatim=True ×3）；③ w1 fundamental72 累计 **20 backtest 行**（SUBINDUSTRY 10 + FAST 轮 10）无缺行；④ 锚读数在库吻合：RREALzx0 S 1.42/F 0.95/2Y 1.43/sub 0.83（TOP500/D1/FAST）、KPJmRpGN S 1.38/F 0.90/**2Y 1.58**/sub 0.92、裸锚 LLKO3vZ9 prod 0.4875 / gJaqYgQl prod 0.487（prod_corr_source=check_correlation）——ask 判读基准全部一手复核成立
- 判读基准（ask 给定 + 本槽一手复核）：S 近闸族天花板 **1.38–1.42**（KPJmRpGN 1.38 / RREALzx0 1.42，DB 读数）；新臂目标带 1.5–1.7；fnd45 基线 S 0.96 量级参照（waveBE242:35，非承诺）；**2Y 硬闸 = 1.58**（`tracking/DEU/config/thresholds.json:5`，:6 注记 RREALzx0 checks.fail limit=1.58、KPJmRpGN 1.58 恰过）；近闸族 2Y 1.43–1.58；裸锚 2Y 1.51/1.53 且 prod 已判净（0.4875/0.487 << PRODCORR_CEILING 0.70，`src/wqb/config.py:502`）；裸水平 2Y<1.0 记「机制需条件化」不记死；sub 近闸族 0.83–0.92、<0.75 稳健告警（平台 LOW_SUB_UNIVERSE_SHARPE limit=0.69 为另一口径）；TO 近闸族 14.5–14.8%、目标 <20%、>25% 结构告警、TVR 层禁用（死档 1575）；**SUBINDUSTRY 格三波死（0.68/0.25/0.21）不复跑**；符号指纹：盈利改善→做多（三 delta 同向乘积已证正向）、衰减对称=机制在/符号错、翻转保留；CW 挂=数据层指纹（宽度塌缩）不改符号重试

## §1 臂序读数表（原样转录，按臂序，勿按 alpha id 猜）

| # | 臂（缩写） | alphaId | S | F | 2Y | sub | TO | DD | margin | LC/SC | invest_S | RA fail / 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 双delta×bucket 减腿重建 δ240×δ176 (q_ebit)，bucket(rank(ts_std_dev(·,252)),range 0,1,0.25) | LLKqYgxn | **1.45** | **1.02** | 1.12 | 0.66 | 14.51% | 6.66% | 0.000992 | 191/192 | 1.08 | 3 项=[LOW_SHARPE(1.45<1.58), LOW_SUB_UNIVERSE_SHARPE(0.66<0.69), LOW_2Y_SHARPE(1.12<1.58)]；**LOW_FITNESS PASS（F 1.02≥1.0）**、CLUSTER_TEST PASS；新派 |
| 2 | 同臂1 换 q_is_oper_inc | ZYaqv2L0 | **1.47** | **1.03** | 1.16 | 0.74 | 14.29% | 6.37% | 0.000991 | 190/192 | 1.14 | 2 项=[LOW_SHARPE(1.47<1.58), LOW_2Y_SHARPE(1.16<1.58)]；LOW_FITNESS/LOW_SUB_UNIVERSE/CLUSTER 全 PASS；**本波最佳**；新派 |
| 3 | 三腿 δ240×δ176×ts_rank1008 (net_income)，sector | ZYaq1X8Y | 1.26 | 0.84 | 1.20 | 0.88 | 13.14% | 6.75% | 0.000894 | 186/197 | 1.22 | 3 项=[LOW_SHARPE, LOW_FITNESS, LOW_2Y]；查重跳过（id 108789） |
| 4 | 同臂3 换 q_ebitda | 0mP9aGVk | 1.17 | 0.75 | 1.30 | 0.68 | 12.57% | 10.52% | 0.000818 | 180/202 | 1.10 | 3 项；查重跳过（id 108790） |
| 5 | divide(rank(OCF),1+rank(net_income))，sector | YPan9lVW | 0.45 | 0.18 | 1.24 | 0.69 | 12.68% | 15.57% | 0.000324 | 188/195 | 0.48 | 3 项；查重跳过（id 108791）；**D3 比值腿首测** |
| 6 | divide(rank(ebit),1+rank(sales_rev_turn))，sector | j2aWMVpj | 0.43 | 0.17 | 1.23 | 0.48 | 13.57% | 24.54% | 0.000318 | 185/197 | 0.45 | 3 项；查重跳过（id 108792） |
| 7 | divide(rank(ebit),1+rank(ebitda))，sector | mLaJlKGK | 0.21 | 0.06 | **1.48** | 0.29 | 13.24% | 27.25% | 0.000156 | 183/199 | 0.25 | 3 项（含 LOW_2Y 1.48<1.58）；查重跳过（id 108793）；**2Y 全波最接近闸（距 0.10）但 S 0.21 严重背离** |
| 8 | divide(rank(ts_mean(ebit,252)),1+rank(ts_std_dev(ebit,252)))，sector（SNR 形） | E5QY2mjL | 0.26 | 0.08 | 1.13 | 0.41 | 13.46% | 26.03% | 0.000199 | 185/197 | 0.26 | 3 项；查重跳过（id 108794）；**D3 SNR 腿首测** |
| 9 | multiply(-1, 三腿 δ240×δ176×ts_rank1008 (q_ebit), sector)（**反向臂**） | gJawVRze | -1.36 | -0.94 | -1.34 | -0.80 | 13.00% | 66.67% | -0.00096 | 200/182 | -1.31 | 4 项=[LOW_SHARPE, LOW_FITNESS, LOW_SUB(-0.8<-0.65), LOW_2Y]；新派；符号指纹臂（§2.9） |
| 10 | rank(q_net_income) 裸水平探针 | xAv9ElLp | 0.08 | 0.01 | 0.83 | 0.22 | 14.41% | 27.07% | 0.00006 | 195/187 | -0.05 | 3 项；查重跳过（id 108795）；存在性探针：LC 195/SC 187 全宽非塌缩（sub/TO/DD/invest_S/margin 为 DB 补充读数） |

（臂 1/2/9 = 本轮新派重建式；臂 3-8/10 = 今日 12:08:45 FAST 首轮已派已收割件，本轮查重命中跳过、读数转录引用，非重复仿真。）

## §2 逐臂归因条目

1. **臂1 LLKqYgxn**（双delta×bucket 减腿重建，q_ebit）：**跨形同字段对照（vs 近闸原形 RREALzx0：三腿 sector，DB S 1.42/F 0.95/2Y 1.43/sub 0.83）**——S 1.42→1.45（+0.03）、F 0.95→1.02（+0.07，**破 fitness_min 1.0**）、2Y 1.43→1.12（-0.31）、sub 0.83→0.66（-0.17，平台 0.69 闸下差 0.03 实挂）。减腿重建显著优于近闸原形（ask 判读：S 1.42→1.45、F 破 1.0），但 2Y 由 1.43→1.12 下滑——**bucket 增益代价显现于近期**。稀释铁律：1.45 > 原形三腿 1.42 ⇒ 相对原形不稀释反升；对应动量单腿（rank(ts_delta(·,240)) 裸）零实测，严格判定沿 w1 纪律挂起（如实登记）。TO 14.51% ∈ 近闸族带 14.5–14.8%。LOW_FITNESS PASS = 本战役（fnd72 四波）**首次 F 过闸**。
2. **臂2 ZYaqv2L0**（同臂1 换 q_is_oper_inc）：**跨形同字段对照（vs 近闸件 KPJmRpGN：同字段三腿 sector，DB S 1.38/F 0.90/2Y 1.58/sub 0.92）**——S 1.38→1.47（+0.09）、F 0.90→1.03（+0.13，破 1.0）、2Y 1.58→1.16（-0.42）、sub 0.92→0.74（-0.18；平台 0.69 闸上 PASS，本地 <0.75 稳健告警触发）。本波最佳：全期 S 1.47/F 1.03 **双破两个近闸件**（S 1.47>RREALzx0 1.42>KPJmRpGN 1.38；近闸族 F 0.90–0.95 从未破 1.0），距 S 闸 0.11、距 2Y 闸 0.42。**字段×几何交互**：三腿形下 q_ebit(1.42)>q_is_oper_inc(1.38)，双delta×bucket 形下反转 q_is_oper_inc(1.47)>q_ebit(1.45)——字段排序随几何反转，不可脱离几何单轴外推。2Y 1.58→1.16 下滑，bucket 增益未能跨字段维持 2Y（ask 原文转录）。
3. **臂3 ZYaq1X8Y**（三腿 net_income，sector，查重跳过）：同形四字段排序链补全：**q_ebit 1.42 > q_is_oper_inc 1.38 > net_income 1.26 > ebitda 1.17**（DB 近闸件 + 本波两臂）。sub 0.88 ∈ 近闸族带 0.83–0.92。三轴近闸触发（S 1.26≥1.2 ✓；2Y 1.20 距 1.58 差 0.38 ≤0.4 ✓；F 0.84 距 1.0 差 0.16 ≤0.4 ✓）——但 nearGate ≤2 按 S 降序排第 3 出局（边界如实登记，§6）。
4. **臂4 0mP9aGVk**（三腿 ebitda，查重跳过）：四字段最弱（1.17，距 S≥1.2 差 0.03 出 S 触发线）；2Y 1.30 距 2Y 闸 0.28 ≤0.4（2Y 轴触发）。DD 10.52% 波内次高。字段排序尾部确认。
5. **臂5 YPan9lVW**（divide(OCF, 1+NI) 现金流质量比值，查重跳过）：**D3 比值腿首测**。S 0.45 弱。形间对照（同分母字段 net_income）：乘法复合 1.26（臂3）vs 比值 0.45 ⇒ **比值几何 S 面大弱于乘法几何**（-0.81）；对照水平单腿（臂10 同字段裸 rank 0.08）：比值 0.45 > 0.08 ⇒ 相对水平单腿不稀释。2Y 1.24 >1.0 活（比值形 2Y 面与乘法形 1.20 同量级）。TO 12.68% 健康。
6. **臂6 j2aWMVpj**（divide(ebit, 1+sales_rev_turn) 利润率比值，查重跳过）：第二比值字段确认 S 弱（0.43，与臂5 0.45 同带）⇒ 比值弱非字段特异而是几何属性。sub 0.48 波内次低、DD 24.54% 高。
7. **臂7 mLaJlKGK**（divide(ebit, 1+ebitda) 同族内部比值，查重跳过）：S 0.21 比值臂最低、**2Y 1.48 全波最接近 2Y 闸（距 0.10）**但 S 仅 0.21——**S-2Y 跷跷板比值形极端样本**（|Δ|=1.27 全波最大背离，ask 原文「近期与全期严重背离」）。ebit/ebitda 为同族两口径，内部比值信息含量低（S 0.21 印证）。LOW_2Y_SHARPE(1.48<1.58) 仍 fail。按 S 降序排第 5 不入 nearGate（2Y 载体形态与 w1 首轮 LLKO3vZ9 同类，登记不占位）。
8. **臂8 E5QY2mjL**（divide(ts_mean,1+ts_std_dev) SNR 形，查重跳过）：**D3 SNR 腿首测**，S 0.26 弱——SNR 形与比值形同弱带。**至此 D3 矩全家四类腿（水平/一阶差/二阶波动/比值+SNR）全部实测**（§8）。2Y 1.13。
9. **臂9 gJawVRze**（反向臂 multiply(-1, 三腿 q_ebit sector)，新派）：**符号指纹实测完成，三波累计缺口关闭**（w1/w2/w3 §3 连续登记「衰减对称未实测」）。**衰减对称成立**：|S| 1.36 vs 正向 1.42（差 0.06 同量级）、|2Y| 1.34 vs 1.43（差 0.09 同步翻转）、|sub| 0.80 vs 0.83（差 0.03）——三指标同步翻转同量级 ⇒ **机制在且符号对称，非事件型**（2Y 同步翻转而非 |2Y| 塌缩，排除早期事件驱动）。**正向保留判定**：正向读数 1.42 > 反向 |1.36| 且正向为库内近闸方向 ⇒ 符号正确（盈利改善→做多），非符号错（若符号错，反向臂应出正读数）——正向原形 RREALzx0 在库为保留方向，翻转无增益（翻转后与库内既有近闸原形同构、零增量）。变参乘积与嵌套三乘同值（ask 自报，对照锚 RREALzx0 正向原形实证）。DD 66.67% 为负收益 alpha 镜像回撤，仅作指纹读数非结构告警。**无 CW fail**（RA fail 4 项里无 CONCENTRATED_WEIGHT）。反向臂不占近闸候选位（§6）。
10. **臂10 xAv9ElLp**（rank(q_net_income) 裸水平探针，查重跳过）：存在性探针通过（LC 195/SC 187 全宽非塌缩，FAST 格宽度远超 SUBINDUSTRY 轮年报字段 73–79）。S 0.08 近零弱正 ⇒ **三腿几何 S 1.26（臂3 同字段）主要来自动量结构（delta×delta×rank 腿）而非字段水平值**（ask 归因读数）。**本波唯一「复合 vs 对应单腿（水平腿）」实测对照**：复合 1.26 >> 水平单腿 0.08 ⇒ 不稀释。2Y 0.83 <1.0 ⇒ 按 S0 基准记「机制需条件化」指纹不记死。DB 补充读数：sub 0.22、TO 14.41%、margin 0.00006、invest_S -0.05。

## §3 指纹 / 铁律 / 跨区核对汇总

- **符号指纹**：衰减对称三波缺口本轮实测关闭（臂9，§2.9）——机制在、符号正确（正向）、非事件型。**CW 零挂闸**：本波 10 臂 RA fail 清单里零 CONCENTRATED_WEIGHT 项——与 SUBINDUSTRY 三波 trade_when 门控臂 CW 恒挂 0.5 形成配置/形态对照：CW 挂闸是门控形×慢变量的指纹，FAST 格动量复合形无此问题（登记口径沿 §5 区分：结构层 vs 数据层）。符号方向：全部正向臂读数与 IS delta 符号先验（盈利改善→做多）一致。
- **稀释铁律**：**零稀释触发**。①乘法复合 vs 水平单腿实测对照：臂3 1.26 >> 臂10 0.08（同字段 net_income）不稀释；②减腿 bucket 重建 vs 近闸原形：1.45/1.47 > 1.42/1.38（跨形同字段 2/2）不稀释反升；③比值复合 vs 水平单腿：0.21–0.45 > 0.08 不稀释；④动量单腿（rank(ts_delta(·,240)) 裸）四波零实测 ⇒ 乘法复合对该腿的严格判定沿 w1 纪律挂起（如实登记，不造对照）。比值形 vs 乘法形的 0.45 vs 1.26 属形间对照非铁律范畴。
- **跨区不外推**：零 TWN 引用；全部对照 DEU 域内（DB 近闸件 RREALzx0/KPJmRpGN、本波波内/跨形/跨字段）。fnd45/fnd86/fnd89/fnd90 邻接集先验未因本波改写。
- **波级聚合**：sub 0.22–0.88——臂3 0.88/臂2 0.74 入近闸族带（0.83–0.92 下沿附近），臂1 0.66 平台 sub 闸差 0.03 实挂；<0.75 本地稳健告警 8/10 臂（FAST 格较 SUBINDUSTRY 三波 25/25 全告警明显改善，但未系统性过线）。TO 12.57–14.51% 全部 <20% 目标、≤近闸族带（14.5–14.8%）上沿，无结构告警；**TVR 层未用**（死档 1575 遵守）。margin：臂 1–4 ≥0.000818 过 review.margin_min 0.0005（thresholds.json:7）；臂 5–8/10（0.00006–0.000324）低于该线，与 LOW_SHARPE/LOW_FITNESS 同向弱（比值/裸水平臂），平台 RA 清单无 margin 项、随主弱不另立告警。

## §4 绿芽（sprouts）/ 死轴（deadAxes）

**绿芽**：
1. **双delta×bucket 减腿重建形（臂1/2）**：S 1.45/1.47 **双破 FAST 近闸族天花板 1.42**、F 1.02/1.03 **本战役首次破 fitness_min 1.0**（LOW_FITNESS PASS；近闸族 F 0.90–0.95 四波从未破）——距 S 闸 0.11–0.13，本战役最接近全闸达标的几何。
2. **q_is_oper_inc × 双delta×bucket（臂2）五维健康**：S 1.47 全波最佳 + F 1.03 + sub 0.74 平台 sub 闸 PASS + TO 14.29% + DD 6.37% 全波最低——唯 2Y 1.16 距闸 0.42 为剩余缺口。
3. **F 破 1.0 的几何路径实证**：减腿（去 ts_rank 第三腿）+ bucket 分组首破 F——S/F 权衡曲线移动的机制解释 = 去噪声腿 + 波动分组提纯（跨形同字段 2/2 一致）。
4. **字段×几何交互活体**：字段排序随几何反转（三腿形 q_ebit>q_is_oper_inc；双delta×bucket 形反转）——设计含义：字段排序不可脱离几何单轴外推，下波字段选择绑定几何评估。
5. **符号指纹确证（臂9）**：机制在、正向保留、非事件型——为 S 突破读数提供机制层背书（非数据假象/非早期事件驱动）。
6. **D3 矩全家四类腿全部实测**（比值 3 臂 + SNR 1 臂本轮补上）——判死引用的矩缺口关闭（§8）。

**死轴**：
1. **比值/divide 几何 S 面 @FAST 格**：臂5–8 S 0.21–0.45 四臂一致弱（同字段乘法复合 1.17–1.47）⇒ 比值形 S 面死轴；**2Y 面 1.13–1.48 活**——S-2Y 跷跷板比值形（臂7 极端样本 S 0.21/2Y 1.48）。记 S 死 2Y 活，非全轴死。
2. **裸水平 S 面（q_net_income 0.08）**：水平值无 S 信号，载荷在动量结构——跨格与三波 SUBINDUSTRY 年报面「水平 S 死」结论一致（水平轴跨两格收敛）；2Y 0.83<1.0 记「机制需条件化」不记死。
3. **2Y 轴的 bucket 减腿代价（跷跷板非死轴）**：臂1/2 2Y 1.12/1.16 vs 近闸原形 1.43/1.58——「bucket 增益全期兑现、代价在近期」（ask 读数）。距闸 0.42–0.46 未到死；登记为下波设计取舍约束（S/F 突破形 vs 2Y 保闸形不可兼得于当前参数）。

## §5 数据层排除判读（口径区分）

- **本波零宽度塌缩、零 data_excluded 臂**：LC 180–200 / SC 182–202 全宽（FAST 格），10 臂 RA fail 清单零 CONCENTRATED_WEIGHT 项——与 SUBINDUSTRY 轮门控臂 CW 恒挂形成对照。
- 7 数据字段（q_ebit/q_is_oper_inc/q_net_income/q_ebitda/cf_q_cf_cash_from_oper/q_sales_rev_turn/q_is_q_ebitda）存在性全正向（LC>0）。
- 登记口径：比值弱读数归**几何层**（信号结构选择），非数据层；死档 1573「宽度≤5 必挂」形态四波累计未出现。
- 探针（臂10）per 协议只作存在性判断，不作覆盖度读数。

## §6 nearGateCandidates（≤2，按 S 降序；先测 prod 再扫参——prod 雷在核心不在搭档，同核变体共 prod 命运）

| alphaId | 臂 | 触发 | 读数（原样） |
|---|---|---|---|
| ZYaqv2L0 | 臂2 | S 1.47 ≥1.2 ✓；距 S 硬闸 1.58 差 **0.11** ≤0.4 ✓；F 1.03 已过 fitness_min 1.0；2Y 1.16 距 2Y 闸 0.42 | S=1.47, F=1.03, 2Y=1.16, sub=0.74, TO=14.29%, DD=6.37%, margin=0.000991, LC=190/SC=192, invest_S=1.14；RA fail 2 项=[LOW_SHARPE(1.47<1.58), LOW_2Y_SHARPE(1.16<1.58)] |
| LLKqYgxn | 臂1 | S 1.45 ≥1.2 ✓；距 S 硬闸 1.58 差 **0.13** ≤0.4 ✓；F 1.02 已过 fitness_min；sub 0.66 距平台 sub 闸 0.69 差 0.03（LOW_SUB_UNIVERSE_SHARPE 实挂） | S=1.45, F=1.02, 2Y=1.12, sub=0.66, TO=14.51%, DD=6.66%, margin=0.000992, LC=191/SC=192, invest_S=1.08；RA fail 3 项=[LOW_SHARPE, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y] |

- **排序外登记（如实）**：臂3 ZYaq1X8Y 三轴触发（S 1.26≥1.2、2Y 1.20 距闸 0.38、F 0.84 距闸 0.16）按 S 降序排第 3 出局；臂4 0mP9aGVk（2Y 1.30 距闸 0.28）、臂7 mLaJlKGK（2Y 1.48 距闸 0.10，S 0.21 载体）——本波满足触发的臂 5 条，≤2 截断。
- **反向臂9 排除说明**：|S| 1.36 机械上距 S 闸 0.22，但全指标为负不可提交；翻转后=库内既有近闸原形 RREALzx0 同构（零增量）——符号校验臂不占候选位。
- prod 测序意义：臂2/臂1 为同核变体（同几何异字段）——按「同核变体共 prod 命运」，先测其一 prod 即可预判族占用；裸锚 prod 0.4875/0.487 判净为族内利好先验（不同形不构成保证，如实区分）。

## §7 datasetStatus 裁决 + 波 verdict

**datasetStatus = active（继续加注）**。依据（全部为本波读数 + DB 近闸对照，判死依据=读数）：
1. **S 面突破**：臂2 1.47/臂1 1.45 双破 FAST 近闸族天花板 1.42（RREALzx0 DB）——本战役首个突破既有天花板的读数；F 1.02/1.03 首破 fitness_min 1.0。距 S 全闸达标仅 0.11–0.13。
2. **机制层背书 + 数据层全宽**：臂9 衰减对称证明机制在（非假象/非事件型）；10 臂零塌缩零 CW ⇒ 突破读数非数据层伪影。
3. **加注方向明确且未扫维度仍多**：2Y 补偿几何（近期窗口腿/decay 扫描/混合形）、bucket range 变体、decay（固定 4）/trunc（固定 0.08）/宇宙/delay——与 w1–w3 provisional 判弱依据（best S 0.68→0.25→0.21 递降、设计假设逐一证伪）**方向反转**（本轮减腿假设证实、best 1.47），provisional 不再成立。
4. **mode_b_qualification 首次正达标**（thresholds.json:23-27）：本波最强 ZYaqv2L0 S 1.47≥1.25 且 F 1.03≥0.8 **双过资格线**——有资格进 Mode B 组合增强/继续优化；前三波「不采用其判死分支」的张力登记（w1 §7.5/w2 §7.5/w3 §7.5）在本波转为放行依据，无冲突。
5. 判死方向与读数相反：不判死、不 data_excluded、不改写邻接集先验；六维闸 D1 互异性仍未审计（§8），但不构成本波任何降档依据。

**波 verdict = PARTIAL**（判定表 `src/wqb/wave_results_contract.py:79-90`：0 达标 + ≥1 near ⇒ PARTIAL；n_pass=0 / n_near=2：ZYaqv2L0、LLKqYgxn）。与 w1 行现值（fnd86/fnd72 首轮均 PARTIAL）同值，合并写入不改变单元格语义。

## §8 判死六维闸盘点（四波累计 + 本轮增量）

| 维 | 累计现状 | 判定 |
|---|---|---|
| D1 结构互异模板 ≥10 | 名义 ~14 形（三重乘裸跑/trade_when 门控乘/bucket(vol) 条件化/年报裸 rank/年报 group_rank 形/门控 group_rank 形/裸 rank 探针/gBF 修复形/vol-bucket 中性化/CF·BS 主线裸 rank/**双delta×bucket 减腿/比值 divide 族/SNR 形**/反向校验形） | 互异机制 ~6–7（动量 delta 复合/水平排位/波动条件化/门控事件子集/中性化收尾/比值-SNR/减腿重建）——**互异性待审计，不单方面宣布达标** |
| D2 字段族自测 | 累计 14 字段（q 族 6 + a 族 4 + tle + cf_a 2 + bs_q_1） | 主线覆盖 ✓；VECTOR 684 等仍零实测 |
| D3 矩全家 | **本轮补齐比值腿（臂5/6/7）+ SNR 腿（臂8）** ⇒ 水平✓ 一阶差✓ 二阶波动✓ 比值/SNR✓ | **四类全测，D3 关闭**（w1–w3 缺口清账） |
| D4 分组轴 ≥2 | sector/bucket/SUBINDUSTRY/FAST 配置 | ✓ |
| D5 非线性 ≥1 | ts_rank/trade_when/bucket/group_neutralize/divide-SNR ≥5 类 | ✓ |
| D6 配置 ≥2 | SUBINDUSTRY（三波）+ **FAST（本轮实测，非 DB 既有点复读）** = 2 套中性化；decay/宇宙/delay 仍单值 | 中性化轴 ✓（decay/宇宙/delay 仍缺） |

结论：D1 互异性未达 ⇒ 判死仍不可能（本波亦不判死，方向相反）；D3/D6 相对 w1 §8 的缺口本轮关闭。

## §9 newLever 登记（跨波实证 + 归因对照链）

**减腿×bucket 重建杠杆（本波新入册，S/F↑ 换 2Y↓ 的取舍杠杆）**：
- 跨波实证：近闸原形三腿 sector（2026-11-05 mcp-20261105 波，DB 在册 RREALzx0/KPJmRpGN）→ 本波双 delta×bucket 减腿形，**同字段跨形对照 2/2 同向**：q_ebit（1.42/0.95/1.43 → 1.45/1.02/1.12）、q_is_oper_inc（1.38/0.90/1.58 → 1.47/1.03/1.16）。
- 归因对照：同字段、全指标转录、双字段复现；增量 S +0.03/+0.09、F +0.07/+0.13（首破 1.0）、2Y -0.31/-0.42、sub -0.17/-0.18。
- **caveat 两条（如实）**：①减腿（去 ts_rank 第三腿）与分组换轴（sector→bucket）**两变量捆绑、单变量未拆**——严格归因需下波拆分臂（三腿×bucket / 双delta×sector）；②2Y 代价真实存在——**取舍杠杆非纯增益**，2Y 闸位设计不可直接沿用。
- 设计含义：S/F 攻坚用减腿 bucket 形；2Y 保闸须在该形上追加近期补偿（近期窗口腿/decay），或回三腿形补 S。

## §10 证据通道与盲区登记

- 本档读数来源：ask 转录臂序读数（收割步骤⑦臂归属按平台 code 逐字核验）+ 本轮实跑只读核验 `logs/_tmp_fnd72_w1fast_attr_verify.py` / `_verify2.py` / `_verify3.py`（sqlite mode=ro 零写入）：3 新臂行级一致（FAST 配置确认）、10 表达式逐字全同（7 查重件 id 108789-108795 + 3 重建式 108799-108801）、锚读数（RREALzx0/KPJmRpGN/裸锚 prod）在库吻合、w1 fnd72 累计 20 行无缺行。
- 查重跳过臂读数有效性：7 条为今日 12:08:45 FAST 首轮派发收割落库件（expressions status=backtested），本轮转录引用为同日新鲜读数，非跨日复读。
- 相关性查询未做（单槽在相关性员）；臂2/臂1 的 prod/self 未测（先测 prod 再扫参，归下槽）；裸锚 prod 0.4875/0.487 为 ask 给定且 DB prod_corr_source=check_correlation 吻合。
- 沿 ask 盲区：expressions 表不含 MCP 直连仿真——本轮 3 重建臂经 upsert_backtest_rows 落库（核验在位）；query_dataset_profile/query_field_profile 对 DEU 全 0 行（S0 档 §6）。
- 判读不改写邻接数据集先验：fnd45/fnd86/fnd89/fnd90 结论未因本波变动；DEU 2Y 硬闸 1.58 引用 thresholds.json 原值。
