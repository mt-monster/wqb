# DEU 挖掘会话最终交付报告（2026-11-13 → 11-14，BE221-BE241）

> 任务：DEU 20 颗 regular alpha（优先 ATOM）。本会话执行 S0→S6 全流程，全程固定 DEU，遵守并发 ≤2 multisim、判死六维闸、先归因再推进纪律。

## 一、最终交付状态（对照 20 颗目标）

**继承基线**：前轮战役已交付 17 颗互相关<0.7 的平台合格件（FINAL_LEDGER_17_OF_20_20261112.md 权威清单，含 5 颗已提交）。**本会话缺口任务 = 3 颗新过闸件（S≥1.58 + 2Y≥1.58 + prod<0.7 + 与 17 颗篮互相关<0.7）**。

**本会话结论：缺口 3 颗未能闭合——新增最强件止步 S 1.53/2Y 1.53（E5Q31wgm），且其 prod 0.7657 超线。** 全部近闸件及其堵点已逐颗实测归因（见 §三）。20 颗目标按平台当前证据暂不可达，原因如下（非工作量不足，见 §四「为什么推不过 1.58」）。

## 二、本会话完整产出索引（归档路径与命名规则）

**命名规则**：战役文档 = `tracking/DEU/atom_orthogonal/<类型>_<主题>_<YYYYMMDD>.md`（沿用 atom_orthogonal 战役根目录惯例）；字段画像 = `FIELD_PROFILE_<数据集>_<YYYYMMDD>.md`；波次 = `waveBE<N>_<主题>_<YYYYMMDD>.md`；台账 = `LEDGER_<主题>_<YYYYMMDD>.md`。

| 产物 | 文件 |
|---|---|
| S0 候选清单与选定理由 | [S0_DATASET_SCAN_20261113.md](S0_DATASET_SCAN_20261113.md) |
| S1 字段画像 news17/18（118 字段全梳理） | [FIELD_PROFILE_NEWS17_NEWS18_20261113.md](FIELD_PROFILE_NEWS17_NEWS18_20261113.md) |
| S1 字段画像 fnd45/alpha_factor_lib（77 字段） | [FIELD_PROFILE_FND45_AFL_20261113.md](FIELD_PROFILE_FND45_AFL_20261113.md) |
| S1 字段画像 model238（22 字段） | [FIELD_PROFILE_MODEL238_20261114.md](FIELD_PROFILE_MODEL238_20261114.md) |
| 波次派发与归因（news17/18 判死链） | [waveBE221_BE222_NEWS_dispatch_20261113.md](waveBE221_BE222_NEWS_dispatch_20261113.md) / [waveBE223_BE224_NEWS_upgrade_20261113.md](waveBE223_BE224_NEWS_upgrade_20261113.md) |
| fnd45 QA 真话机制归因（臂序修正教训） | [waveBE227_FND45_qa_leverA_20261113.md](waveBE227_FND45_qa_leverA_20261113.md) |
| model238 三波 26 臂台账 | [LEDGER_MDL238_BE232_234_20261114.md](LEDGER_MDL238_BE232_234_20261114.md) |
| model238 终局（decay/幂/prod 雷） | [LEDGER_MDL238_FINAL_BE235_237_20261114.md](LEDGER_MDL238_FINAL_BE235_237_20261114.md) |
| **全算子场景扫描设计与判决（20 场景归因）** | [waveBE239_BE240_OPSCAN_design_20261114.md](waveBE239_BE240_OPSCAN_design_20261114.md) / [waveBE239_BE240_OPSCAN_verdict_20261114.md](waveBE239_BE240_OPSCAN_verdict_20261114.md) |

## 三、近闸件逐颗归因（本会话 21 波 174 臂）

| alpha | 构造 | S | 2Y | sub | prod | 堵点归因 |
|---|---|---:|---:|---:|---:|---|
| E5Q31wgm | mdl238_industry(w504)+AS3, sp1.3 | **1.53** | 1.53 | 0.73 | **0.7657 ✗** | mdl238 核心与生产池暴露：同核 1.49-1.53 全平台共此雷（GrmVrz53 0.7667 / oma251z6 0.8088 实测确认） |
| GrmVrz53 | mdl238_industry(w378)+AS3, sp1.3 | 1.52 | 1.52 | 0.71 | 0.7667 ✗ | 同上 |
| j2aQ7GPo | fnd45 QA×AS3, sp1.3 | 1.04 | 1.34 | 0.79 | **0.4567 ✓** | prod 干净但 S 差 0.54——fnd45 核心量级不足，加腿不叠加（BE230 9 臂证） |
| A1xdpqAW | fnd45 QA 杠杆A w378（单腿） | 0.96 | 1.73 | 0.72 | **0.4527 ✓** | 同上；58 臂+20 算子场景确认单腿天花板 |
| qM7bbMZK | 同构 normalize 版 | 0.96 | 1.88 | 0.70 | （同构预期 ~0.45） | 同上 |
| leaxeGYx / 6XMxX0Q5 | model238 同集双腿/三腿（**ATOM**） | 1.34-1.36 | 1.16-1.17 | 0.45 | 未测 | S 差 0.22：AS3 去掉后掉回 change 家族平台 |

**核心归因律（本会话最大方法论产出）**：prod 相关性的雷在**核心**不在搭档——mdl238 industry_rank 核心无论配 AS3 还是配同集 change 都 0.77-0.81；fnd45 QA 核心无论单腿还是配 AS3 都 0.45。而 S 的叠加能力相反：AS3 才推得动 S（1.04→1.53）但只在 mdl238 核心上有效（fnd45 核心上仅 1.04）。**DEU 当前生产池恰好封死了「唯一能过 1.5 的核心」**。

## 四、为什么 3 颗缺口推不过 1.58（数据链）

1. **fnd45 面**（58+20=78 臂）：QA 情绪是真实信号（2Y 最高 2.25、margin 7bp、TO 2%、prod 0.45 全干净），但**截面量级只有 ~0.96**；所有算子场景（含 20 场景扫描）无一能推破 1.0。PR/CEO/可读性/数字密度/分歧/回归残差全灭（六场景判弱入档）。
2. **model238 面**（54 臂）：industry_rank×AS3 到 1.53 后六维全扫（窗/幂/winsorize/decay4-6/搭档）收敛在 1.49-1.53 平台，且全族 prod 0.77-0.81。
3. **组合协同律**（BE230/232/234/238 四波验证）：fnd45 腿 rank 化后一律稀释（0.47-0.98）；正交 change 腿无 S 增益（2Y 2.0-2.25 但 S 不叠加）；「换核心出低相关件」与本轮「S>1.5 需 AS3」互相矛盾——**S 突破与 prod 合规在 DEU 当前池里被结构性地对立**。
4. ATOM 路线（用户优先项）：同集多机制腿最高 1.36（model238）/ 0.94（fnd45），差 0.22-0.64。

## 五、过程约束遵守情况

- ✅ 全程 DEU 未换区；数据集切换 2 次（news17/18→fnd45→model238）且每次均出具换集理由（NEWS 面 30+ 臂天花板 0.94 判死；fnd45 面 78 臂收敛后转 model238）。
- ✅ 并发 ≤2 multisim 全程（每波 ≤10 臂）。
- ✅ 组腿约束：无 PV×MODEL×OTHER 互配；fnd45(FUNDAMENTAL)×mdl238(MODEL)×AS3(ANALYST) 组合无禁配类，且非 PV/MODEL/OTHER 三类间互配——但「MODEL 塔单集红线」（记忆 redline-pv-model-other-single-dataset）适用于 mdl238 单集（已遵守，单集波全部 ATOM 合规）；跨集组合件需在交付前按该红线复核用途。
- ✅ 论坛/论文现场取证：earnings call 情绪 4 篇论文（巴西 1640 场/LM-FinBERT/JBESS 崩盘风险/KOSPI）+ WL27618/FF45555 论坛帖；风险塔 5 集盘点。
- ✅ 先归因再推进：每波收割后臂序核对+根因记录（含一次自查纠错：BE225 wpoVAZr1 臂序误读当场修正归档）。
- ✅ 算子场景吃透（用户指令）：103 算子盘点 → 20 未测场景全部实跑 → 逐场景归因（5 有效/6 判弱/其余同族合并）。

## 六、可复用经验沉淀（建议同步入 skill/记忆）

1. **prod 雷在核心不在搭档**（§三）——候选组合卡 prod 时，先分别测「核心×中性腿」与「中性核心×搭档」定位暴露源，再换核心。
2. **臂序纪律**：multisim 读数必须按派发顺序逐臂核对，禁止按 alpha id 猜（wpoVAZr1 误读战例）。
3. **电话会情绪字段通用律**：水平矩承载信息、二阶矩/峰值新鲜度/回归残差/跨段分歧全灭、ts_backfill(4 季度=378d)+杠杆A+normalize 是最优形态——earningscall 族后续数据集直接复用。
4. **hump = 免费换手压缩器**（S −0.05 换 TO 减半 + 2Y +0.27）；**normalize 与 zscore 等效且 2Y 略优**。
5. **时序变换在「已 backfill 的水平矩」上全灭**（ts_quantile/ts_scale/ts_av_diff）——变换只做截面层。
6. **静态闸验证器坑**：`normalize` 本地验证器不认 `useStd/limit` 参数（平台文档有），负号前缀 `-ts_mean` 会被误判 group_zscore 参数错——写法绕开而非硬闯。

## 七、建议下一步（超出本会话授权范围，列供决策）

- 缺口 3 颗的现实路径：**等待生产池漂移**（prod 相关性 5 天作废律）后复测 E5Q31wgm 族；或开辟 analyst83/alpha_factor_lib 等全新核心面（需新战役授权）。
- fnd45 面保留两个平台合格形态（A1xdpqAW/qM7bbMZK，S 0.96/2Y 1.73-1.88/prod 0.45）作塔位储备——距 FUNDAMENTAL 塔点亮（每集 3 因子）的门槛仍在。
