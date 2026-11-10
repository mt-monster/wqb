# EUR eur15 战役报告（goal 启动 2026-11-09 11:19 · 14:45 突破版）

> 目标：15 颗本战役新挖并通过验证的 REGULAR alpha｜EUR 锁定｜multi-sim 并发=2｜算子 ≤12｜模板 ≥10｜篮子互相关 <0.5
> **进度：0 / 15（首颗全闸候选仅差 prod）**｜约 3.1 小时 / 400+ requests

## ★★★ 全闸候选（本役首个，风险 60 族）

| 项 | 值 |
|---|---|
| 主推（族内选定） | **`2rAVV7ew`** = `ts_mean(group_zscore(multiply(vec_avg(rsk60_last),-1),country),5)` |
| 备选 | `1YN33726` = `ts_mean(group_zscore(signed_power(multiply(vec_avg(rsk60_offer),-1),1.5),country),5)` |
| 设置 | EUR / **TOP2500** / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / maxTrade OFF / nan ON |
| 主推指标 | S **1.56** / F **1.31** / TO 6.74% / 2Y **2.28** / sub 1.29 / ret 8.84% / fRA=1 / **fail=[]** |
| 备选指标 | S **1.58** / F **1.41** / TO 6.10% / 2Y 2.12 / sub 1.28 / ret **10.0%** / **fRA=0** / **fail=[]** |
| self | 0.4599（19 颗池）PASS |
| 逐年 | **2014–2023 全部 10 年 longCount>0 且 pnl>0**，零空窗零负年 |
| **prod** | **平台计算中（唯一缺口）** |

**机制**：`rsk60_offer/last`（借券卖空报价费率）翻号后正向 = 「费率越低 → 未来收益越高」；经济含义：费率飙升 = 空头挤压临近 = 未来下跌。**ret 8.8–10% + TO 6–7% ⇒ F 1.31–1.41，本役首次越过 F 闸**。
**族容量**：0.5 与 0.7 两口径均 **只能提 1 颗**（offer×bid_rate = 0.9998）。

## 一、14 集判定总表（全字段覆盖 + 三闸 PASS）

| # | 数据集 | 最强 | 死因 |
|---|---|---|---|
| 1 | fund_holdings_panel | 全 IS 闸 S1.61/F1.02/2Y2.58 | **prod 0.8881 族墙** |
| 2 | sentiment26 | 全 IS 绿 S1.19/F0.99 | **prod 0.8264 族墙** |
| 3 | insider_matrix | S1.03/F0.52（43 式 33/33） | **F 天花板 0.54** |
| 4 | news7 | max|S| 0.98 | 信号弱 + F 墙（含 news18 同源机制） |
| 5 | news31 | max|S| 0.86 | 信号弱 + F 墙 |
| 6 | news50 | max|S| 0.81 | 信号弱 + F 墙 |
| 7 | news21 | max|S| 0.73 | 信号层死 |
| 8 | news29 | max|S| 0.36 | 信号层死 |
| 9 | risk68 | |S| 1.04（反转） | F 墙（risk 塔系统性） |
| 10 | institutions6 | S1.03 | 2Y 结构塌 |
| 11 | other424 | max|S| 0.66 | 信号死 + 2Y 断档 |
| 12 | earningscall_sentiment | 预核 | cov 0.5115 + aC 1676 + S≤0.21 |
| 13 | pv47 | 语义核验 | 区域错配 |
| 14 | **risk60（翻号+TOP2500）** | **S1.56–1.58 / F1.31–1.41 / 2Y2.28** | **存活 → 全闸候选** |

## 二、七条结构性定律（实证）
1. **prod 池全球拥挤**：论坛公开信号已被占位（0.8881 / 0.8264 两次全 IS 闸撞墙）；本地 aC 冷 ≠ prod 干净。
2. **F = S×sqrt(ret/max(TO,0.125))**，ret/TO 比是信号不变量，换几何不改 F。
3. **投波前先算 F 天花板**：低 ret 族（≤5%）S 天花板 1.1 时 F 封顶 0.3–0.55 ⇒ 结构性不可达。
4. **稀疏事件字段正确几何 = ts_sum + 整形栈**（TO 170%→3%），只解 TO 不解 F。
5. **EUR news 塔事件型数据 ret ≤5%，F 系统性死**（五集全证，含已证机制同源者）。
6. **覆盖闸 dimension_coverage 是粗判** ⇒ 必须字段级自检。
7. **★ 负向强族翻正三件套（本役突破）**：① 符号校正需族内 ≥3 独立读数同向；② **宇宙平移 TOPCS1600→TOP2500** 是修复 sub/rob 与抬 S 的最强单招（本役 6/6 全 fail=[]）；③ `signed_power 1.5` 在 ret 厚的族上能一次动多闸（S 1.55→1.58、F 1.28→1.41、fRA 1→0、ret 8.56%→10.0%）。**三者只修方向/宇宙/整形，不破 ret 天花板**。

## 三、投波前二验纪律
`create_multi_simulation` 返回 success+id **不等于**平台真建了批次（本役两次实证：15 条>10 上限静默失败；9 条返回 id 但 batch_status 404）⇒ **发批后必须立即 batch_status 二验**。

## 四、剩余路径
1. **prod 通过即呈交**（本颗，族容量 1 席）。
2. prod 撞墙 ⇒ S4 降杠杆（换读数 offer→last/bid、换轴 country→industry、hump/decay、幂次档）
3. 库存件：仅 `leA5JeP7` 过 S/2Y（2Y 2.32），F 0.94 差 0.06；**其余 3 颗 2Y 1.22–1.51 全部阻断**（此前按 Mode B bypass 记为全闸是错的）。提交可点亮 INSIDERS 2/3→3/3，不计入 15 新件、需你确认。
4. 15 颗的机制族数量：本役证明 EUR 未点亮塔里 F 可达的族极少（仅 risk60 一类），**15 颗需跨区或新数据集**。

## 五、归档索引
画像：reference/profiles/eur_*｜字段全集：reference/eur_*_fields.json（8 集）｜模板池：s1_*｜候选：candidates/*.json（14 集共 ~200 式）｜台账：WAVE_LEDGER.md 波 eur15-W1…R60W1（含 IMW1/N50W1 勘误、三件套拆解、族内选颗判据）｜registry：14 集 campaign 状态全落库｜skill 修正 2 条｜记忆沉淀 3 条（prod 全球拥挤 / F 天花板 / 负向强族翻正三件套）

---

## 六、终局更新（2026-11-09 22:50，覆盖上文「0/15」状态）

### 交付：2 颗完整验证通过（UNSUBMITTED，待用户逐颗确认提交）

| # | alpha | 配方 | S | F | 2Y | TO | margin | self | prod | 逐年 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `P0oR7vYw` | 三腿等权（techindi概率×analyst修正×insider信号）+CROWDING | 2.28 | 1.61 | 2.42 | 9.24% | 13.48bp | 0.5347 | **0.6881** | 10年无空窗 |
| 2 | `leAnKOEA` | 同族四腿/平滑变体 | 2.05 | 1.39 | 2.48 | 7.15% | 16.13bp | 0.4625 | **0.6476** | — |

⚠ 二者互相关 **0.7837 > 0.7** ⇒ **只能提交其中一颗**（先提一颗，另一颗 self 必爆）。推荐 `leAnKOEA`（prod 余量 0.0524 更安全）。

### 待 prod 验证 3 颗（其余全过，margin 已核）

`O0ALVWmJ`（S2.37/margin9.38bp/度数0）→ `MPYEEwj8`（S3.83/margin8.92bp/sub2.37）→ `LLMvveP2`（S2.21/margin6.20bp）。`58EmKpkk` margin 4.77bp **低于 5bp 线，降为最后顺位**。

### 容量终判

- **0.5 口径最大独立集 = 4 席**（精确解）：`MPYEEwj8` / `58EmKpkk` / `O0ALVWmJ` / `LLMvveP2`；margin 修正后实际可提交约 **3 席**。
- **容量 = 独立底层信号数**：`techindi_model` 含 2 个独立模型族（`probability_*` 294 字段 / `tm_*` 399 字段，跨族互相关 0.13–0.24）⇒ 2 族 × ~2 席 = 4 席。89 个切面（分位×horizon×命名×模型变体）只能把互相关从 0.95 降到 0.24，**不增席**。
- **数据集判定终数：38 个实测，出货 1 个**。4 个 0 塔位 category（macro/socialmedia/earnings/institutions）物理不可达；已点亮塔 44 集按规则排除；risk 类 6 结构族 47 条探针判死（最强 S 0.84）。
- ⇒ **15 颗在 EUR 内不可达**，需换区或调整目标。

### 方法论沉淀（10 条，均已入记忆 + skill override）

1. **prod 与 S 是 U 形**（7 点：0.8175→**0.6476**→0.7240↑，极小值 S≈2.0–2.3）；2. **跨塔稀释**（秩空间等权，prod −0.064，前提三缺一不可）；3. **CROWDING 压 prod / INDUSTRY·MARKET 抬 F**；4. **容量定律**；5. **选集排序 ret 量级先验 > aC > cov**；6. **真·伪预测型判据**（percentile/score/similarity ⇒ TO<5% 排除）；7. **族级判死**（换维度不改 F 天花板）；8. **状态量家族补全**（风格 beta/暴露载荷）；9. **RISK 6 结构族穷尽**；10. **prod 读取三类阻塞 + ts_skewness 幽灵算子**。

### 归档新增（相对上文第五节）

- 交付：`deliverables/DELIVERY_01_P0oR7vYw.json`、`DELIVERY_02_leAnKOEA.json`、`BASKET_4SEATS_verification.md`、`DELIVERY_SNAPSHOT_2_verified.md`
- 专项研究：`eur15_zero_tower_feasibility_20261109.md`、`eur15_facet_capacity_20261109.md`、`eur15_tm_family_20261109.md`、`skill_update_20261109.md`、`candidates/RISK_structural_exhaustion_20261109.md`
- 挖掘地图：`reference/EUR_CATEGORY_MINING_MAP.md`（173 集/14 类 + 5 处 category 勘误）
- skill：`wq-brain-ra-eur` SKILL.md 286→354 行（8 节 override）；边界算子档双轨补录（ts_delay 合法 / ts_skewness 幽灵 / ts_max 不可访问）
- 记忆：新增 10 条方法论

### 阻塞与技术事实

- **prod 测试按用户指令暂停中**（2026-11-09 21:36 起）。恢复后按优先级测 3 颗，本役可达 3–5 颗。
- prod 计算的系统性阻塞：MCP 120s 硬上限 vs 平台 4–8 分钟 ⇒ 超时即丢弃；加锁模式与自身/其它进程争抢账号级单并发槽。
- `ts_skewness` 幽灵算子（单条即 mid=null，废整批）、`ts_max` 平台不可访问 ⇒ 已录入边界算子档禁忌区。

## 七、4 席篮子 prod 终测（2026-11-10 02:40，覆盖上文「待 prod 3 颗」）

| 成员 | 信号族 | S | margin | **prod** | 判定 |
|---|---|---:|---:|---:|---|
| `MPYEEwj8` | tm_ | 3.83 | 8.92bp | **0.8785** | ❌ |
| `LLMvveP2` | tm_ | 2.21 | 6.20bp | **0.8161** | ❌ |
| `O0ALVWmJ` | probability | 2.37 | 9.38bp | **0.7388** | ❌ |
| `58EmKpkk` | tm_ | 2.64 | **4.77bp** | 未测 | ❌ margin 先出局 |

### ★ 族际 prod 地板定律（第 3 版容量定律）

- **probability 族地板 = 0.6476**（leAnKOEA，S2.05）：S2.28→0.6881 / S2.37→0.7388 / S2.90→0.7289 / S4.29→0.8175，U 形成立。
- **tm_ 族地板 = 0.8161**：S2.21→0.8161 / S3.83→0.8785，两点均高、无极小可采 ⇒ **整族不可提交**。
- ★ **互相关正交 ≠ prod 正交**：tm_ 与 probability 族互相关仅 0.13–0.24，但 prod 地板差 0.17。**族际 prod 地板必须实测**（族内 2 个 S 档即可估计）。
- **容量定律第 3 版**：可提交席位 = Σ 各信号族 max(0, prod 地板 <0.7 的席数)。本例 probability 2 席（互相关 0.7837 只能提 1）+ tm_ 0 席 ⇒ **EUR 实际可提交 = 1**。

### 最终交付（2 颗验证通过，互相关 0.7837 只能提一颗）

`P0oR7vYw`（prod 0.6881）与 `leAnKOEA`（prod 0.6476，**推荐**：prod 余量 0.0524 / self 0.4625 / margin 16.13bp 三项均优）。

**挑新信号族的强制动作**：先测该族 prod 地板（族内 2 个 S 档），地板 ≥0.8 整族放弃。
