# 在飞状态（2026-11-11 上午收盘）

## 仿真队列（平台当前排队拥塞，子代注册可滞后至 ~55 分钟）

| sim | 波 | 内容 | 臂数 |
|---|---|---|---:|
| 3AXvhf5Ll4C5ckcj54kCh8f | BE60 | fnd6 piq/ibq × 开放族（news/insiders/sentiment） | 8 |
| 3ZBsZF3IX4VWcInYe5Z02Yu | BE61 | piq 单窗 tvr 配方 + 开放族 / fnd45 X3 × news | 6 |

## 待发（槽位一空即派，表达式已预检通过）

- BE52：tail 增强版待授权篮子（8 臂，替换升级路径）—— waveBE52_design_tail_enhanced_basket_20261111.md
- BE53：option1 IV 面 7 臂（XZZ 文献臂）—— waveBE53_BE54_option1_pattern_20261111.md
- BE54：pattern_scores 10 臂（LoMW + 论坛 Peak 做空模板）—— 同上
- BE55：risk72 replicator 2 臂收口 —— 同上

## 交付状态

- 交付 11/20：6 ACTIVE + 5 待授权（全部七层验证齐备）；
- 本轮复核：self 池 17，最新 OS 仍是 11-10 的 78Yk8VR1 ⇒ **池未漂移**；
  qM7KxkQV self 0.5429 / 9qlz29Oe self 0.4552 均 PASS；
- prod 刷新值（本轮 08:5x 实测）：0.543 / 0.6124 / 0.6039 / 0.47（4 颗）+ RREPm361 0.6881（11-10 实测）；
- 提交动作继续冻结（待用户明确授权）。
## 追加（在飞更新）

| sim | 波 | 内容 |
|---|---|---|
| eyTXq2EF4PCb8rmeYwupI1 | BE65 | 3 字段瘦结构（NEWS×INSIDERS）+ ts_product 德国方言，8 臂 |
| PbmVp2k84R2b1Ra0S46iMu | BE66 | pv1 价格反转内核族（含 ts_product(relative volume,5) 德国方言），8 臂 |

已终结：BE62（EAT 原配方，8/8 ERROR 算子 inaccessible）、BE63（PEAD 全弱）、BE64（ts_zscore 重建全负）、BE65 待收。
⇒ EARNINGS 塔关闭（见 EARNINGS_TOWER_CLOSED_20261111.md）。
## 在飞最终状态（08:5x 更新）

- BE66（`PbmVp2k84R2b1Ra0S46iMu`）：pv1 价格反转内核族 8 臂 —— 平台队列中，下轮收割；
- 本日已终结 13 波（BE48/49/50/51/56/57/58/59/60/61/62/63/64/65）；
- 本日新增结论：**institutions1 信念族关闭**（自锁+预算）、**EARNINGS 塔关闭**（算子+覆盖）、
  **fnd6 piq 死**、**pattern/簇轴仅对弱信号有效**；
- 本日新增机制发现：pv30 GROUP 轴、tail 适用边界、连续权重重造并列块、DEU prod≈self、
  **DEU 算子有效性地图（仅 4 个有效算子）+ 双信号 Ladder 天花板 1.1-1.6**（外部两篇大报告归档）；
- 待发：BE52（tail 增强待授权篮子）/ BE53 option1 / BE54 pattern_scores / BE55 risk72。
## id 幽灵事件修正（2026-11-11 10:5x）

- 此前记录的 BE66 sim id `1kTIT9eoQ4E7cooSnNeQJvS` **平台 404**（从截断的工具输出手抄导致），
  且 IS 池最新 20 件中无任何 pv1 臂 ⇒ 该批实际未创建；
- 已重派并**当场回查验证**（progress 0.1）：BE66 = `PbmVp2k84R2b1Ra0S46iMu`；
- 纪律：**sim id 必须从工具返回对象读取并在派发后立即回查存在性，禁止手抄截断输出**。
## 在飞终态（2026-11-12 11:3x）

- **BE74a**（oi7b6d2s4WhaxW15CzROM2E）：nan OFF/decay4/SUBINDUSTRY 5 臂 — **已收割**：P05JM61x 0.18 / liq_only -0.91 ⇒ nan OFF 非普适解，分族结论入手册；
- **BE74b**（21gZUq7Dz53z92GoD9dw5Lc）：nan OFF/decay0/FAST 5 臂 — **已收割**：P05JM61x 0.54（TO 0.68 爆）/ liq_only -1.29 ⇒ RREPm361 的 2.02 是族专属适配；
- **BE75**（udnbL6oV5dq9LN1aQk2qapt）：正确符号版 8 臂 — **8/8 ERROR**（通用错误）⇒ 2 臂甄别批在飞（4htkURdTM4qG8Z99xAhjLMC，progress 0.35）；
- **BE72**（1FithJ10b4qIccP11mrsaVOc）：回填版内部人腿 8 臂 — **已收割全弱**（回填毁信号第三次复现）。

## 下轮动作

1. 收割甄别批 4htkURdTM4qG8Z99xAhjLMC（成交额+内部人 / 成交额+s27 两臂）；
2. 若甄别批通过（S≥1.2）⇒ 按 v2 L2 升级满波冲 1.58（pv20 流动性 × 内部人/情绪 3 字段结构）；
3. 若甄别批也 ERROR ⇒ 加 ε 排除除零后重试；
4. BE52 已收（tail 全面伤害待授权篮子，呈交包保持原版）；BE68 已收（pv20 1.03 发现）；
5. 交付包已补齐逐颗真实回测设置（RREPm361 = decay0/FAST/nan OFF）。
## 在飞（2026-11-12 11:5x 更新）

- **BE78**（JhAqvF4Esb3oprLmNkRK）：dir 腿全套 + tail 阶梯 8 臂（decay6）—— 平台队列中（progress 0.35），下轮收割；
- 本日累计 16 波（BE48-BE67 + BE74a/b + BE76/77v1/77v2/78）；
- **当前最有希望的活线：advcap×dir/insiders 族（BE77v2 全线 1.12-1.28，sub 0.56-0.65 已过线，2Y 最高 1.51）**；
- BE78 的 8 臂是针对剩余缺口（S 差 0.30 / 2Y 差 0.07）的定向设计。
## 收口（2026-11-12 12:2x）

- BE78 已收（dir 腿 1.00-1.15，2Y 1.34-1.52，弱于 I7 腿）；
- BE79 已收（族天花板 S1.29，四闸不达，pv20 流动性族关闭）；
- **本日 18 波全部收口，无在飞**。
## 在飞（2026-11-12 12:2x）

- **BE80**（1rkd0v8pG4h09lIbtaGLm10）：带通 tail 语义（lower=0.25/upper=0.75/newval=0.5 冠军版）× advcap/I7/s27/dir + 簇50 + 双流动性腿 + decay2，8 臂——progress 0.35 在飞；
- 待验证假设：① 双向带通（冠军 d5WwzRMY 语义）是否优于剪底（BE79 语义）；② decay2 是否优于 decay6；③ 簇50×W3 组合。
## 在飞（2026-11-12 13:4x）

- **BE86**（1b503D8Ps4xMa2VQ2to8dbg）：PV 单塔三字段（动量/形态/成交量）4 臂 — COMPLETE，子 sim 注册中（4 个 child sim ID 已回查）；
- BE67 的最后未收割波也已在飞。

下轮收割这两波，若 PV 三字段有臂 ≥1.4 ⇒ 继续冲闸；若 <1.0 ⇒ PV 单塔组合关闭，此时未点亮塔路径确认全部穷尽。

## 收割 + 补课波（2026-11-12 14:1x）

- **BE86 已收**（1b503D8Ps4xMa2VQ2to8dbg，4 臂，已入库暂定 PARTIAL）：pwaYovex **S 1.14**/F 0.59/sub 0.58✓/2Y −0.39（簇轴外层版，族内最佳，+0.23 vs market 外层）；LLKVq5w2 0.91；0mPO9j2p 0.54；O0WQqJXv 0.16。全部 REVERSION_COMPONENT warning，2Y 全弱。档案 WAVE_BE86_PV3FIELD_20261112.md。
- **BE67 遗留澄清**：在飞记录为陈旧——1QqiIw88V5g9cgCalTlSMLq 已在 WAVE_BE67 判决档内（8 臂 max S 0.75），重收一致，入库 verdict FAIL。
- **BE87 补课波在飞**（协议 v2 L2：pwaYovex 1.14 落 1.0-1.2 带 ⇒ 补定向 10 臂）：`14C7qM2a04Wkb7XILizxyG6`。
  - 10 臂：动量窗 252/756/1008、形态窗 504、量能窗 3/10、去形态双腿、簇轴内外互换、ts_scale 替换、动量腿翻号（预检 valid + audit safe）。
  - **收口判据：best <1.2 或较 1.14 无改善 ⇒ PV 三字段组合关闭，未点亮塔路径穷尽。**

## BE87 已收 + BE88 L3 在飞（2026-11-12 15:0x）

- **BE87 已收**（14C7qM2a04Wkb7XILizxyG6，10 臂，入库暂定 PARTIAL，9 条过 near 线 1.0）：best pwaYzX6g（量能窗3）**S 1.21**/F 0.58/2Y −0.19；动量窗1008 1.16；形态窗504 1.12；动量756 1.11；动量252 1.10；量能窗10 1.09；ts_scale 1.01；去形态双腿 1.02（2Y +0.25）；动量腿翻号 0.12（方向确证）。六维全平台期。档案 WAVE_BE87_BE88_PV_L3_20261112.md。
- **BE88 L3 收口波在飞**（协议 v2：1.21≥1.2 触发满波）：`oqw9FgzJ4jHcJtEKE3IxWi`（progress 0.1 已回查）。
  - 10 臂：tail带通双腿合成、双腿 close252/1008/vol10、簇轴互换复验、tail三分量去winsorize、量10 复现、ts_scale、动量+形态双腿、close1008×vol10。
  - **终判据：best S <1.4 或 best 臂 2Y ≤0 ⇒ PV 组合族关闭（全证书 24 臂九维），未点亮塔路径穷尽，升级决策给用户。**

## BE88 终判 + 尾巴补发（2026-11-12 15:4x）

- **BE88 已收，PV 组合族关闭**（终判据触发：best S 1.09 < 1.4）：合成假设全灭，S-2Y 跷跷板确证（S≥1.09 区 2Y 全负）。全证书 24 臂九维，族天花板 1.21。塔关闭清单已补行。未点亮塔路径穷尽（塔关闭清单以 v2 证书口径更新）。
- **BE53/54/55 尾巴补发**（11-11 设计档存在、预检通过、却从未派发——本次对账发现并补齐）：
  - A 扑（BE53+BE55 合并，9 臂）：option1 XZZ 文献臂 7 条 + risk72 replicator 2 条 ⇒ `34eOORbnc50rbKt16DAnIeuk`（decay4/SUBINDUSTRY/nan ON）；
  - B 批（BE54，10 臂）：pattern_scores LoMW 文献臂 + 论坛 Peak 模板 ⇒ `1WJxg9dAQ58YaGjFgoQKDQ8`（同设置）；
  - 两批存在性回查：batch_status 已确认受理（子代注册中）。

## BE53/54/55 已收 + BE89/90 复活探针在飞（2026-11-12 16:2x）

- **BE53+BE55 已收**（34eOORbnc50rbKt16DAnIeuk，9 臂）：option1 IV 面 lc 157 但 S 全负（-0.17~-0.39），risk72 replicator lc 74-98 |S|≤0.2 ⇒ OPTION 塔 10 臂证书关闭、risk72 终证。入库 verdict FAIL。
- **BE54 已收**（1WJxg9dAQ58YaGjFgoQKDQ8，10 臂）：max S 0.32（lc 150）⇒ pattern_scores 15 模板证书关闭。入库 verdict FAIL。
- **BE89 复活探针在飞**（3IUb7JdKG4HDac55ioZL4mo，10 臂）：risk68 beta/残差 ×2、risk71 特定收益 ×2、news81 头条计数 ×2 + 情绪 ×2、news23 融资额、news73 实体计数；
- **BE90 复活探针在飞**（gKDaC2xR5ilczxwRSYn8bF，8 臂）：pv103 买压/成交额、pv106 价差/滑点、pv13 中心度 ×2、digital_ad_spend ×2；
  - 判读线（协议 v2 L1）：|S|≥1.2 满波 / 1.0-1.2 定向补 / <1.0 判死+lc 证书（数据在不在一锤定音）。

## 终局（2026-11-12 16:5x）

- **BE89/BE90 已收，复活面 18 臂 L1 全灭**（max |S| 0.86；lc 45-161 全有数据 ⇒ 画像 cov=0 系统性证伪）。档案 WAVE_BE89_90_REVIVAL_VERDICT_20261112.md。
- **约束内全谱穷尽**：未冻结 12 塔 v2 证书齐备、4 塔冻结、D0 冻结、论坛无新机制。无在飞、无待发。
- **等待用户裁定**：提交授权（5+1 件 + QPveY7Kg 豁免）/ 约束放宽方向（解冻已点亮塔 / D0 / 算子预算 / 禁混配额 / 修目标数）。

## 用户恢复 goal → L1 补课波（2026-11-12 17:0x）

- 用户恢复 goal。复核：BE89/90 复活探针为存在性级（每集 1-2 臂），非协议 v2 L1 正交网格 ⇒ 三条活口线索补满 L1（pv103 0.86 / pv13 2Y 2.09 / news81 计数）。
- **BE91 在飞**（3L6m4efbL5779toT32gatXp，10 臂）：pv103_ivam_sum 矩×窗×轴×比值网格；
- **BE92 在飞**（3RPI7Pg6Q4nkcgxKC13cuc8，10 臂）：pv13 中心度 5 臂 + news81 计数/情绪 5 臂；
- 判读线：网格 max |S| ≥1.2 满波 / 1.0-1.2 定向补 / <1.0 出正式 v2 判死证书。

## L1 网格终判（2026-11-12 17:2x）——复活面闭环

- BE91/BE92 已收（各 10 臂，0 错误）：pv103 网格 max 0.79、news81 全矩一致负（翻号 ≤0.70）、pv13 max 0.51（2Y 2.07 复现但前段拖死）⇒ **38 臂全灭，复活面网格级闭环**。
- **无在飞、无待发。约束内全谱穷尽（网格级证据）。**
- **等待用户裁定**：①提交授权（RREPm361/9qlz29Oe/qM7KxkQV/Jj8VQwoe/d5a2vxzY + 88NmN37X 换防 + QPveY7Kg 豁免——submit_verdict 预演 7/7 干净）②约束放宽方向（解冻已点亮塔 / D0 / 算子预算 / 禁混配额 / 修目标数）。

## BE93 收（2026-11-12 20:xx）+ BE95/BE97 双批在飞

- **BE93 已收**（iWpF37Q45fMbEHi77EQGAr，10 臂，0 错误，10/10 REJECT）：**macro27 / pv47 / news52 三集全灭**；max |S| 1.01（E5QOe759 pv47_for_statssimple spret，负向）。档案 WAVE_BE93_VERDICT_20261112.md。
  - macro27 jobsactive/jobscreated：|S| 0.00-0.09（TO 4.6-15%，数据在）；pv47 spret：zscore −0.35 / Δ66 −0.11 / for_stats −1.01；news52 电话会议：0.07-0.13（TO 2.6%，事件极稀疏）。
- **BE95 在飞**（4CiApp4s24H18HjZkPJdBgD，10 臂）：alpha_factor_lib 65 字段（cov=0 画像但 BE89/90 已证不可信）行业基本面；设置 decay4/SUBINDUSTRY/nan ON。预检 valid + 字段 10/10 存在。
- **BE97 在飞**（3cjgRo95W4FcbCP3uXtEInI，10 臂）：**pv20×insiders 冠军族 nan_handling=OFF 设置档扫描**——族终判档「穷尽清单」里 nan ON/OFF 与 truncation 从未列入，这是 62 臂结构穷尽后唯一未扫的设置轴（记忆实证：nan OFF 在事件/缺失型字段可差 1.5 个 Sharpe）。设置 decay2/SUBINDUSTRY/nan OFF。
  - 10 臂：冠军基线（测 nan OFF 增益本身）、I7 窗 66/154、LIQ 窗 660/252、tail 0.25-0.75 / 0.20-0.80、winsorize std 2/4、内层轴 sector→subindustry。
  - 判读线：任一臂 S ≥1.58 且 2Y ≥1.58 ⇒ 族破闸（PV+INSIDERS 双塔）；S 1.45-1.58 ⇒ 定向补；全 <1.37（不如 nan ON 冠军）⇒ nan 轴判死，族维持 PROVISIONAL 天花板 1.37。

### 更新（2026-11-12 21:xx）：BE95 收 + BE98 在飞

- **BE95 已收**（4CiApp4s24H18HjZkPJdBgD）：max |S| 0.49，**10/10 REJECT**，TO 0.9-6.6% ⇒ alpha_factor_lib 判死（慢变量）。档案 WAVE_BE95_VERDICT_20261112.md。
- **BE98 在飞**（18yeS7YB5c5bNLCRX5h8yo，10 臂）：NEWS 塔事件**流量计数**面（news50 rp_story_event_count / news18 multi_entity_story_event_count cov 0.98 / story_event_record_count）。这是「同数据不同字段维度」的真空档：news50 在 BE38 只按情绪通道判死，计数面从未测；EUR 同源机制 S 2.72/prod 0.64 是唯一非模型胜件。预检 valid、无 unknown。设计档 WAVE_BE98_NEWS_FLOW_20261112.md。
- **BE97 仍在飞**（3cjgRo95W4FcbCP3uXtEInI，pv20×insiders nan OFF）：子代注册滞后（children 0）。
- 塔照亮表更新：insiders 类仅 2 个数据集（insiders1 29 ac / insider_agg_matrix 182 ac）——塔面已穷尽；fundamental 25 institutions25 实为 manager 空头持仓（CONC 结构性墙）。

### BE97 收 + BE99 在飞（2026-11-12 22:xx）

- **BE97 已收**（3cjgRo95W4FcbCP3uXtEInI，10 臂，10/10 REJECT）：**nan OFF 是本族毒药**——S 1.37 → **0.16**（冠军基线），10 臂全在 0.13-0.38，TO 几乎不变（11-15%）⇒ 配置层整体抹平信号，不是结构失效。族终判维持 S1.37/2Y1.56 PROVISIONAL。档案 WAVE_BE97_NAN_OFF_VERDICT_20261112.md。
  - **连带纠错**：记忆里「稀疏 VECTOR 必设 nan OFF」外推被推翻。RREPm361 族（analyst 预估 dense MATRIX）nan OFF → S 2.02；pv20×insiders（稀疏 VECTOR 持仓）nan ON → 1.37 / nan OFF → 0.16。判据升级为「**缺失是无事件（0 为真值 ⇒ ON）还是无覆盖（0 为伪值 ⇒ OFF）**」，两档必测。已改写入 agent memory。
- **BE99 在飞**（41QKFV9924OJ9N0DSVJTBIo，10 臂）：**earnings6 EPS surprise 批**。起因是核对发现 **RREPm361 实际属 ANALYST 族**（`est_12m_ebi_median`，pyramid=DEU/D1/ANALYST），此前把它记作 earnings6 成果是错的 ⇒ EARNINGS 塔（金字塔 0）与用户 11-12「放宽近十年约束试 earnings6」的指令**并未真正被采过**。
  - 10 臂机制：标准化 surprise / 裸 surprise / surprise 持续性(252) / 累计 surprise / EPS 同比 / 股息水平 / 股息变化 / 初步 EPS 区间宽度（不确定性，负向）/ surprise 时序 z(504) / 累计 surprise + tail。
  - 设置：decay4/SUBINDUSTRY/nan ON（新族按新判据：earnings 缺失=无事件，取 ON 起手）。预检 valid、无 unknown、算子 3-10。
- **BE98 仍在飞**（18yeS7YB5c5bNLCRX5h8yo，NEWS 计数面）：children 仍 0。

### BE98 收 + BE100 在飞（2026-11-12 23:xx）

- **BE98 已收**（18yeS7YB5c5bNLCRX5h8yo，10 臂，10/10 REJECT）：**NEWS 流量计数面判死**——max |S| **0.40**（臂2 A 窗66+tail，2Y 1.15），其镜像臂9 −0.40 方向干净；**TO 仅 1.4%-5.7%** 是决定性证据（EUR 同源机制 TO 33.6% 才赚得到钱）⇒ EUR→DEU 计数型配方不可迁移（事件密度差一个量级）。NEWS 塔现为**情绪面 BE38/BE43B + 计数面 BE98 双面证书**。档案 WAVE_BE98_NEWS_FLOW_VERDICT_20261112.md。
- **BE100 在飞**（3c4zKb7iU4uxb0L38oMCOaA，10 臂）：**pv20×insiders 冠军族 truncation=0.15 + 算子封装轴**。这是族终判「穷尽清单」里另一条从未出现的轴（truncation 一直是 0.08 常数）。
  - 臂1 = 冠军基线（测 trunc 0.15 相对 0.08 的 ΔS，锚 1.37）；臂2-6 = 封装算子（hump 0.01 / ts_decay_linear 5、10 / signed_power 0.5、2）；臂7-10 = 窄 tail 0.25-0.75 / 0.30-0.70 / I7 154 / LIQ 660。
  - **坑**：`hump(x, 0.01)` 位置参数被 toolkit 静态闸整批拒（`必须使用命名参数 'hump='`），改 `hump(x, hump=0.01)` 后通过。已写入 agent memory。
- **BE99 在飞**（41QKFV9924OJ9N0DSVJTBIo，earnings6 EPS surprise）：children 仍 0。

### BE99 收（2026-11-12 23:xx）

- **BE99 已收**（41QKFV9924OJ9N0DSVJTBIo，10 臂，10/10 REJECT）：**earnings6 四面封闭**。真实天花板 **S 0.80 / 2Y 0.19**（累计 surprise 252，lc 91/127 健康）；表面上最强的臂 5 报 S −1.25，但 **longCount=0 / shortCount=0 ⇒ 空心件，已作废**（差点错误触发协议 v2 的 L2）。
- **归因纠错**：RREPm361（S2.02）经详情核对是 **ANALYST 族**（`est_12m_ebi_median`，pyramid=DEU/D1/ANALYST），此前记作 earnings6 成果有误——这也是「earnings6 从未真正被采」的根因。
- 纪律沉淀：**|S|≥1.2 必须回读 longCount/shortCount**，0/0 或 >1:3 失衡 → 空心/偏置件，不下架不得进 L2。已写入 agent memory。
- 档案 WAVE_BE99_EARNINGS6_VERDICT_20261112.md；塔关闭清单 EARNINGS 行已升级为四面证书。

### BE100 / BE101 双批在飞（2026-11-12 23:xx）

- **BE100**（3c4zKb7iU4uxb0L38oMCOaA）：pv20×insiders 冠军族 **truncation=0.15 + 封装算子轴**（族穷尽清单外的两条轴）。
  - 注意：TOP500 下权重多为 ~0.2%，truncation 0.08 很可能根本不 binding ⇒ 臂1 预期复现 1.37；真正的内容在臂2-6（hump / ts_decay_linear 5,10 / signed_power 0.5,2）。
- **BE101**（3wR1Guc274m69sSrUpL3You）：**pv20 流动性腿 × earnings6 EPS surprise 组合**（10 臂）。结构模板沿用族冠军（group_zscore∘add∘双 tail 腿），只把 insd 腿换成 earnings 腿；设置同冠军（decay2/SUBINDUSTRY/nan ON/trunc0.08）以保证可比。
  - 臂1-6 = earnings 腿六变体（mean252 / sum252 / latest / 标准化 / ts_z 504 / 股息Δ）；臂7-8 = tail/窗口扰动；**臂9 = 纯 pv20 腿、臂10 = 纯 earnings 腿**（单腿对照，用于归因：组合必须显著高于两单腿才算有效）。
  - 若组合臂 S ≤ max(单腿) ⇒ 判「两腿不互补」，PV×EARNINGS 组合面关闭。

### BE101 幽灵批重派（2026-11-12 23:5x）

- 原 BE101 批 `3wR1Guc274m69sSrUpL3You` 在平台侧 **HTTP 404**（`lookINTO_SimError_message` 与 `batch_status` 双确认，children 恒 0）——派发返回 ok:true 但平台根本没收到，属**幽灵派发**（区别于 BE66 的手抄错 id：这次 id 直接取自返回对象且存在性回查当时还是 404 判定不了的注册滞后态；以后派发回查要连续两轮 children=0 + 404 才判幽灵）。
- **重派**：`1sQwdzddl4OWbzzxxu8BXnC`（同表达式 10 臂，同设置 decay2/SUBINDUSTRY/trunc0.08/nan ON），派发后立即回查 exists=true。

### BE101 收（2026-11-12 深夜）—— 约束内全谱出清

- **BE101 已收**（重派批 1sQwdzddl4OWbzzxxu8BXnC，10 臂）：**PV×EARNINGS 组合面关闭**——组合 max S 1.18（裸 surprise 腿），纯 pv 腿对照 1.05、纯 earnings 腿对照 0.55（lc 70/135 偏置）；协同 +0.13 远低于 insd 腿的 +0.37。全臂 0.95-1.18，无一带进定向补带。档案 WAVE_BE101_PV_EARNINGS_COMBO_VERDICT_20261112.md。
- **pv20×insiders 族 92 臂封顶 1.37/2Y1.56**（62 结构 + 10 nan + 10 trunc/封装 + 10 earnings 换腿）。
- **无在飞、无待发。约束内（≤12 算子 + TOP500/D1 + 未点亮塔 + 禁混≤5）可探明信号面全部出清**：12 未点亮塔 v2 证书齐备、D0 冻结、已点亮塔冻结、172 集处置图谱全落账。
- 等待用户裁定：①提交授权（5 颗待授权 + 88NmN37X 换防 + QPveY7Kg 豁免 → 合计 18/20）②约束放宽方向（算子预算 >12 / 分析师腿入场 / 解冻已点亮塔 / 开 D0）③或认可 18 为约束内上限、目标改 18。

### BE102 在飞（2026-11-12 深夜）—— 全谱出清终检发现的最后一个真实漏洞

- 终检处置图谱发现：news21/29/3/54/76 五个 cov=0 集只有先验排除。字段画像核实：
  **news76（deprecated 恒 0）/ news54（纯时间戳元数据）/ news29（纯文本/主题码）零成本否决**；
  **news3 的 19 个词频情绪分数字段与 news21 的 8 个词频/语气字段从未实测** ⇒ 派 BE102。
- **BE102 在飞**（1xr0ITbpU4AVbFg1dHxfPeRN，10 臂）：news3 情绪谱系 7 臂（恐惧/乐观/炒作/不确定性/悲观/确定性 水平 + 恐惧 Δ66）+ news21 词频语气 3 臂（净语气/正词/负词）。预检 valid、无 unknown。设计档 WAVE_BE102_NEWS3_WORDFREQ_20261112.md。
  - 定性：news3 词频面 ≠ sentiment7/27/33（打分模型）≠ BE38 事件情绪通道（news17/18/38/50/104）——三个不同的情绪供应商维度，无重试。

### 四类深挖战役启动（2026-11-12 深夜）——用户指令：INSIDERS/INSTITUTIONS/SENTIMENT/RISK 逐集回测

- **BE102 终判**：news3 max 0.62（finup）/ news21 max 0.27 ⇒ NEWS 词频面判死（第四面证书）。全 FAIL 根因 = news21 MATRIX 被 vec_avg 包裹（类型错连坐），修正拆批后正常出料。档案 WAVE_BE102_NEWS3_WORDFREQ_VERDICT_20261112.md。
- **BE103 在飞**（3nIvC3gYa4CNanOmJswGDgt，10 臂）：institutions6 机制波（净流量/广度/conviction/持仓波动负号）。MATRIX 直接裸用。
- **BE104 在飞**（3udRMT95j4o0bjzrTkCx3vM，10 臂）：insider_agg_matrix 机制波（高管−董事分离 CMP2012/买卖流量比/方向×量级/卖侧）。
- 战役总设计：CAMPAIGN_FOUR_CATEGORIES_20261112.md（论坛 6 条高赞机制 + 论文 6 篇模板映射；BE105-111 排队）。

### BE103/104 收 + BE105/106 在飞（2026-11-12 深夜 2）

- **BE103 收**（institutions6 首轮 10 机制）：max |S| 0.29 全噪声；3 臂 unit ERROR（add(count,0.0001) 单位闸）——**count 型字段分母禁加纯数 epsilon**，首轮误伤。2Y 亮点：人均买入强度 1.46。二轮补存量族后出证书。
- **BE104 收**（insider_agg_matrix 首轮 10 机制）：max **0.85 = Jj8MPPGe（significant_value_1 Σ66）S 0.85 / 2Y 1.57 / TO 4.7% 全健康**——事件强度族首个双高读数，进定向补带边缘。directional_indicator 参与臂全 TO 60%+ 偏置（已知供应商指标行为）。**BE104b 定向补**设计围绕 significant_value 族。
- **BE105 在飞**（3bh3V1cq75bt9BXvNPiXozY，10 臂）：sentiment27 网站热度关注度波（排名动量/尖峰/偏度/低关注溢价）。
- **BE106 在飞**（4cgl1baBO4Z8cBiYnQ8f7aB，10 臂）：fund_holdings_panel 流量集中度波（稳定新仓 21d/HHI/大额/conviction）。

### BE105c 收（2026-11-12 深夜 4）——四类首轮普查 5/9 完成

- sentiment27 attention 面：**skewness 0.90 / kurtosis 0.88（2Y 1.1+）二阶矩族显著强于一阶矩（≤0.35）**——关注度结构有信号、关注度水平无信号。BE105d 定向补（二阶矩族扩展）。
- 首轮普查 5 集完成：insider_agg_matrix 0.85（事件强度族双高）、sentiment27 0.90（二阶矩族）、fund_holdings 0.54（三族近端正）、institutions6 0.29（存量族待二轮）、news3/21 词频面已判死（0.62）。
- 无在飞。下一轮派发：BE104b（significant_value 定向）+ BE105d（二阶矩定向）——两个 0.85+ 定向补带候选。

### BE105d/BE104b 收（2026-11-12 深夜 5）——两集出正式证书

- sentiment27 attention 面判死：天花板 0.93（skew mean132，TO 2.1%/2Y 1.13），20 臂收敛。关注度结构有信号但量级只有线的一半。
- insider_agg_matrix 主体机制面判死：天花板 0.86（SV1/adv20 规模中性版），20 臂。SV1 Σ132 的 2Y 1.86 是 insider 族近端最高，但 S 跷跷板。
- 无在飞。待派：BE103b（institutions6 存量族）+ BE106b（fund_holdings 长窗定向）。

### BE108b/BE109 收（2026-11-12 深夜 8）

- insiders1 定向收口：天花板 **1.06**（ts_delta(ts_mean(H,66),66)，F 0.88/lc 63/124 全健康）。裸 ts_delta 全 TO 50%+ 空心——**事件字段先聚合再差分**（43 赞纪律）复证。单数据集按证书判死；Δ66 平滑版留作组合腿候选（1.06 + 协同结构）。
- institutions4/1 判死（8 有效臂 max 0.23，cov 太薄）。
- 四类 8 集完成普查：6 判死 + 1 组合腿候选 + sentiment7/institutions25/risk 五集待普查（BE110/111）。

### BE111 收 —— 四类深挖战役终局（2026-11-12 深夜 10）

- risk60 借券费族判死（天花板 0.95，level+Δ 合成 2Y 1.27）；risk72 残差/IVOL 判死（≤0.22）。
- **战役总计：9 集 / 134 臂 / 11 证书 / 1 组合腿候选**（insiders1 Δ66 平滑版 1.06，F 0.88）。
- 结构性结论：四类单数据集天花板 0.42-1.06 全部 <1.2；唯一未试破线方向 = insiders1 Δ66 为腿的组合面（需跨类配额确认）。
- 无在飞、无待发。档案 WAVE_BE111_FOURCAT_FINAL_20261112.md。

### 四类战役收口后记（2026-11-12 深夜 11）

- 核心臂已入库（wave=BE103-111_FOURCAT，10 条代表臂，1 条过 near 线 1.0 = insiders1 Δ66）。
- 战役结论已固化 agent memory（跨区默认先验）。
- **唯一后继路径**：insiders1 Δ66 平滑版（1.06）作为 pv20×insd 族冠军的换腿/第三腿——属跨类组腿，受禁混配额约束，需用户确认后开波。

### BE112 在飞（2026-11-12 深夜 12）—— 换腿救援

- **配额澄清**：PV×INSIDERS 是冠军族既有配对，INSIDERS 不在禁混清单内 ⇒ 换腿不耗新配额。
- 首批 `2Wg4lhaSv4VccoXZF1LPy5` 幽灵（children 恒 0 + location 404）⇒ 重派 `Mi3Sq13Q4Fw92v6XGO7tLj`（10 臂，同表达式）。
- 设计档 WAVE_BE112_DELTA66_LEGSWAP_20261112.md。判读：≥1.58 双闸 ⇒ 族破闸进提交预演；<1.37 ⇒ 换腿判死。

### BE112 收（2026-11-12 深夜 13）—— 换腿路径实测收口

- **族新天花板 1.41**（aka6YEe9：pv20 + Δ132 腿，F 1.08 / 2Y 1.49）；三腿 1.39/F 1.11；Δ 腿全部「S 涨 2Y 跌」——跷跷板在腿级复现。
- 族 **102 臂封顶 S 1.41 / 2Y 1.56**，双闸差 0.17/0.02。**约束内正式无破闸路径。**
- 2 臂 unit ERROR（IAM 腿 add(adv20,0.0001) 单位闸复现）。
- **无在飞、无待发、无未试路径。** 塔点亮等待：PV+INSIDERS 双塔（若用户放宽）。

### ★INSIDERS 类收档（2026-11-11 深夜）

- 用户指令「专注 INSIDERS 深入挖掘一步步走」执行完毕：**6 波 / 60 臂 / 2 数据集 / 全机制族 + 全设置轴**。
- **天花板 S 1.07**（乘法双腿，单腿 1.06），距 1.58 差 **0.51**；2Y 最高 1.60（SV2 单腿）。
- 三条机制结论：① 持仓维度 > 金额维度 ② **第二笔大额 SV2 的 2Y 1.60 全类最高** ③ 事件字段水平时序化必空心（第三次复现）。
- 设置轴：nan ON≫OFF、分组轴不敏感、decay 无益；唯一未扫轴 = 平台中性化（±0.1，填不了 0.51）。
- **正式收档**，证书 INSIDERS_TOWER_CERTIFICATE_20261111.md；塔关闭清单已更新两行。
- 无在飞、无待发。

### ★INSIDERS 最终定型 1.27（2026-11-11/12）—— 收档

- 用户指令链执行完毕：BE113-123 共 **80 臂**，天花板从 1.06 抬到 **S 1.27 / F 0.95 / 2Y 1.37 / sub 0.64**（wpoqw87Q，嵌套 sector→market 外层三正交排序）。
- 判读：BE123 max 1.27 落 1.24-1.4 边际档 ⇒ 按判读线**出收档报告**，停止追加波次。
- 距闸：S 差 0.31 / F 差 0.05 / 2Y 差 0.21 —— 三闸同差，信号真实但量级不足。
- 五条机制结论已固化 memory：持仓维度>金额维度、单调变换空操作、三正交排序协同、个股级信号禁用行业中性、门控全灭。
- 报告 INSIDERS_FINAL_REPORT_20261111.md；塔关闭清单已更新。
- **无在飞、无待发。**

### MCP 会话故障（2026-11-11 21:20）

- 现象：所有 wq-brain-http MCP 调用返回 `{"code":-32600,"message":"Session not found"}`，含 authenticate。
- 诊断：**服务本身正常运行**（`python tools/start_wq_mcp.py --check` → exit 0，http://127.0.0.1:8000/mcp）；失效的是**宿主侧 MCP 会话 token**。
- 影响：BE128 重派批（RzRb6aZ94OO8RPFQr5elXU）在平台侧应仍在跑，但本地无法查询/收割。
- 处置：需**重启宿主会话**（或重建 MCP 会话）后恢复；已挂 10 分钟重试提醒。
- 说明：这解释不了之前的幽灵批（那些是平台侧 404），是**独立故障**。

### MCP 会话故障·诊断结论（2026-11-11 21:2x）

| 检查 | 结果 |
|---|---|
| `wqb-db` MCP（8001） | ✅ **正常**（get_campaigns 返回 OK）|
| `wq-brain-http` MCP（8000） | ❌ 全部调用 `Session not found`（含 authenticate）|
| 端口 8000 监听 | ✅ 有进程（PID 36540）|
| .mcp.json 配置 | ✅ 正确（8000→wq-brain-http，8001→wqb-db）|
| `start_wq_mcp.py --check/--service` | 报“已在运行” |

**结论**：服务进程与端口正常，**服务端 session 表丢失**（进程可能重启/会话过期），宿主仍持旧 session ID。
**与幽灵批无关**（那是平台侧 404），是独立的宿主↔server 会话故障。
**处置**：只能**重启宿主会话**（新会话会重新 initialize）；服务端重启无效（宿主仍送旧 ID）。会话重启后直接查 `RzRb6aZ94OO8RPFQr5elXU`。
**BE128 重派批状态未知**（派发已确认受理，平台侧应仍在跑或已完成），本地不可查。

### BE129 派发异常（2026-11-11 21:3x）

- 首批 `3pEa9y33P4traYTQeSAbKwN` 幽灵（404）→ 重派 `3GnBZM2qs5gkaKU1a9SYv3Dr` **再成幽灵**（children 恒 0 + location 404）。
- **平台通道本身是通的**：单条 `create_simulation` 能跑到 120s 墙钟超时（说明请求已送达并执行）。
- 判定：**10 臂 multisim 的子代注册链路当前不稳定**，非账号/语法问题。
- 应对：拆小批（5 臂）重派 `1XniIHe1o5cpcKSLTcF5DG7`，观察是否注册。
- 备选通道：`batch_create_simulations`（参数 `items[]`，每项需 base_region/base_universe/base_delay 等 base_* 字段，本 MCP 未暴露默认值）。

### ★新通道打通：batch_create_simulations（2026-11-11 21:4x）

**契约（实测）**：
```
{
  base_region:'DEU', base_universe:'TOP500', base_delay:1, base_decay:4,
  base_neutralization:'SUBINDUSTRY', base_truncation:0.08,
  base_nan_handling:'ON', base_pasteurization:'ON', base_unit_handling:'VERIFY', base_language:'FASTEXPR',
  items: [{ expression: '<alpha expr>' }, ...]
}
```
- **base_* 必须放在顶层**（放 items 里会报"base_region 必填"）
- **items[].expression** 是表达式字段名（不是 alpha_expression）
- 返回 `{submitted:n, results:[{index, location, simulation_id, ok}]}`，**每条独立 sim**，不走 multisim 注册链路

**用途**：multisim 幽灵批高发时（今日已 6 次）的替代通道。BE129d 五臂即由此提交：
16zUs88X14Oxbdb55Dm7ZOh / 422el0f9F4AkaUC118WMPb6o / 2DoDmMaYS4iKcLjk9gXzvdq / 2YOqnEeFo4So8QSuuNKY1gi / xzwDX6Es4rGckLpptfB4Z7
提交后即刻 404（注册延迟中），已挂 15 分钟复查。
