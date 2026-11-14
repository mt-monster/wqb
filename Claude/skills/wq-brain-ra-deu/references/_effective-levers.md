# DEU 有效杠杆册（实测入册，勿凭理论新增）

> 回到 [DEU 区域流程](../SKILL.md)。本册只收**DEU 实测过、有读数对照**的结构杠杆；
> 跨区不可外推（每条都注明实测区）。新增杠杆必须附：实测前→后读数、适用结构边界、失效反例。
> 权威实测档案在 `tracking/DEU/atom_orthogonal/` 对应 wave 文件。

## 杠杆 A — 双层中性化（破 2Y）

`group_zscore(group_neutralize(group_zscore(X, sector), subindustry), sector)`

- 实测：S 1.57→1.63（DEU，2026-11-12 前轮战役）
- **边界**：仅对「单层 sector 排序 + 多腿相加」的 **MODEL 结构**有效；单腿/非 MODEL 未证实
- 失效先验：单腿机构/内部人数据上无效（见 [['_basket-and-atom']] §四无效搭档族）

## 杠杆 B — 反转 × 应计质量乘法交互（破 IS_LADDER）

`multiply(reverse, accruals)`（**乘法**；加性并入崩到 0.50）

- 实测：2Y 1.47→1.77（DEU，杠杆B 原始定义波）
- **边界**：跨集反转腿 × 应计腿；ATOM 内不可复制（反转腿在 PV）——同集版见 BE242 归因「乘法稀释」

## 杠杆 C — 自身动量条件化 trade_when（质量分族 S/2Y 双升，2026-11-14 入册）

```
trade_when(ts_delta(ts_backfill(质量分, 66), 66) > 0, group_rank(ts_backfill(质量分, 66), sector), -1)
```

只在该质量分自身 66 日改善时持仓，否则维持前值。经济含义：**质量信号只在边际改善期被定价**
（QMJ 式条件化；裸质量分在大盘已定价，条件化解锁其信息）。

- 实测（DEU/TOP500/D1/SUBINDUSTRY，BE244→BE248/249，`waveBE242_FND89_ACCRUAL_ATOM_20261114.md` §十二-十三）：

| 结构 | 裸跑 S/2Y | 条件化 S/2Y |
|---|---|---|
| fnd90 GP/TA（grossprofit_asset） | −0.13 / −0.39 | **0.75 / 1.71（2Y 过闸）** |
| fnd90 pscore（Piotroski） | 0.02 / −0.49 | 0.88 / 1.12（gate22 最优 S） |
| fnd90 cash_flow_coverage | 0.08 / −0.84 | 0.82 / 0.54 |

- **边界**：① 质量分/评分类字段族（GAME/评分/报告类）通用，事件/情绪类未验证；② 门控窗 22 最优 S、66 最优 2Y；
  ③ `ts_decay_linear` 外层平滑不增益（0.70 vs 0.71）；④ group_zscore 与 group_rank 等效略低；
  ⑤ 信号 TO 降至 1.4-2.5%，margin 0.4-0.7bp。
- **增强子（BE250 实测）**：`tail(winsorize(<杠杆C>, std=2), lower=0.25, upper=0.75, newval=0.5)` 包装再 +0.09 S
  （0.75→0.84，2Y 保持 1.68）；阈值升级（Δ>自身 252 均值）+0.03。
- **失效反例**：icfroe_5y 条件化 2Y 0.23（5 年窗太慢，动量门控无意义；1y/3y 全窗亦死）；fnd93 税应计族整体无信号，
  条件化救不了无信号字段；**同源合成无效**——杠杆 C 两腿等权加/乘法在 fnd90 内全稀释（同族质量分，BE250）；
  **杠杆 A 单腿无效**（gated pscore 双层中性化 0.70 vs 0.71，A 边界坐实）。

## 杠杆 D — group_backfill 叠加修 CW（2026-11-14 入册，用户配方）

```
group_backfill(ts_backfill(vec_avg(F), 250), sector, 250)   // ✅ 唯一正确用法：叠加在 ts_backfill 之上
group_backfill(vec_avg(F), sector, 66)                       // ❌ 裸用禁止
```

组内 winsorized 均值填充缺失值，把覆盖率铺开直接稀释 CONCENTRATED_WEIGHT。

- **gBF 三定律（BE259/261 实测，`waveBE242_FND89_ACCRUAL_ATOM_20261114.md` §十七）**：
  1. **裸 gBF 对慢变量灾难**：填充值随组均值日漂移，季度/年度字段被变成日频信号——TO 47–60%，5 臂全灭；
  2. **唯一正确用法 = 叠加在 ts_backfill 之上**：先 ts_backfill(250) 锚定自身历史，再 gBF 铺组内覆盖——
     实证 CW warning 0.25 → **PASS**（KPgxRLG8）且指标无损（1.55 ≈ 1.56）；
  3. **修 CW 不损指标**：pwaQ0bx3 = gBF ±0.95 std4 = **S 1.60/F 1.40/2Y 2.01/sub 1.25，failed_ra=0，已提交 ACTIVE**。
- **边界**：慢变量（年度/季度更新）专用；带宽峰随形态漂移——rank-tail 峰 0.15/0.85=1.53、非 gBF zscore ±1=1.56、
  **gBF zscore ±0.95+std4=1.60**（双向回落证峰非单调，精修须扫 ±0.85~±1.1）。
- **失效反例**：fnd1 上 5 臂裸 gBF 全灭（waveBE242 §十七 BE259）。

## 杠杆 E — group_zscore 量级形态（rank 会扔掉量级信息，2026-11-14 入册）

`group_zscore(ts_backfill(vec_avg(F), 250), sector)` 替代 `group_rank(...)` ——保留「25 年 vs 8 年 CEO」的量级差。

- 实测（fnd1 CEO 任期，BE257）：zscore **1.38**/F1.08/sub1.32 > rank 裸跑 1.26-1.35；配合 tail(winsorize(±带宽)) 后
  达 **1.56-1.60**（BE258-261，pwaQ0bx3 提交 ACTIVE）。
- **边界**：① vec_avg 聚合最优（vec_max 1.17 更弱——平均值比最长者信息量大）；② 输出无界，tail 带宽语义变为
  zscore 对称带（±1 ≠ rank 的 0.15/0.85），须重扫；③ 符号必须区内指纹校验——CEO 任期文献先验「壕堑」负号，
  **DEU 实证「经验」正号**（BE251 −1.26 翻正，跨区不外推又一例）。
- **失效反例**：ratchet 变量（任期只涨）上 ts_zscore 动量 0.68 死、trade_when 门控 0.98<1.26 裸跑——
  杠杆 C 的门控与动量类变换对单调爬升变量全部无效。

## 反模式（实测证伪，勿再投）

| 反模式 | 实测证据 |
|---|---|
| **同源合成**（等权 add / 乘法把同数据集两腿拼一起） | BE250/BE242#9/BE257/BE252 四证全稀释（fnd90 0.84→0.49、fnd1 1.26→1.17）；闸5 同源豁免的 corr<0.7 假设在同族字段上不成立 |
| **S-2Y 跷跷板**（设置级手段破不了 S 闸） | decay12/轴切换/平滑/锐化在 fnd1 上无一抬 S（1.43-1.49 反降），fnd1 靠结构跃迁（zscore 量级）破闸——S 卡壳先换结构再动设置 |
| **宽度塌缩入场**（平台集级 cov=0 或 lc<50 的集不开波） | digital_ad_spend lc25/sc25+CW 挂、alpha_factor_lib DD 71-199% 超窄账户签名——**数据层排除≠信号死**，登记口径见判死分层 |

## 通用纪律

- **近闸 prod 前置（用户 2026-11-14 明令）**：候选达到**近闸**（S≥1.2 或距任一硬闸 ≤0.4）时，**先 `check_correlation(production, refresh=True)` 探 prod，再决定是否继续网格扫参**——prod 雷在核心不在搭档，同核变体共 prod 命运；prod 堵则整族停手换核，prod 净才烧扫参配额（model238 54 臂后才发现 0.77 堵的反例；wpoXmKGv 1.35 时即探得 0.6805 净的正例）。
- 每个杠杆先做**归因对照**（裸跑 vs 加杠杆同批）再入册，禁止无对照入册。
- 跨区移植前 2 槽小批先验方向（TWN/KOR/DEU 符号翻转先例见 [['_basket-and-atom']] §四）。
- 同一经济腿只贡献 1 颗（clone 相关 self 0.96 实例）。
