# 03 · 区域与数据集特性

> 来源：2026-09-05 ~ 09-29 工作日志实证提炼 ｜ 更新：2026-09-29（§2 的区域口径有 2026-10-04 增补，以各区 `regions/<R>.md` 的 `entry_verdict` 为准）
> 所有结论限定实测时的设置与时间范围，跨区迁移前须重新验证。

---

## 1. 区域画像速览

| 区域 | 画像 | 主绑墙 | 结论 |
|---|---|---|---|
| **MEA** | 不在金字塔体系（212 格中 0 格）；投了 33 颗 = 365 天 REGULAR 的 41%；SUPER 通道已关闭 | — | ❌ **停投**（66/18.2% CI[0.11,0.29]） |
| **IND** | universe 仅 TOP500；中性化最优 = STATISTICAL；ACTIVE 20 条**全是冷门数据集** | `LOW_ROBUST_UNIVERSE_SHARPE`（limit 1.0） | ❌ **停投**（53/15.1%） |
| **DEU** | 6 颗 ACTIVE 共享 starmine 修订动量共腿（精确最大互斥集）；测了 42 颗 prod、**0 颗 <0.7** | prod + SELF 墙 | ❌ **停投**（16/**0%**） |
| **KOR** | 分析师族已饱和（prod 0.9+）；SA 首选（12 REGULAR + 仅 2 SUPER，"池子新鲜度"最高） | prod | ✅ 主攻（过闸率 **72.7%** 最高） |
| **GLB** | 绑定约束是"三区域检查 + 2Y"，比 prod 更早生效（AMER/EMEA/APAC 子宇宙各 ≥1.0 且 2Y ≥1.58） | 子宇宙 + 2Y | ✅（过闸率 58.8%） |
| **ASI** | **最大机会池**：370 颗未提交存量中占 95 颗且从未测 prod（已测 2 颗均 ~0.51）；用 `MINVOL1M` | prod（头部 3 颗 0.80~0.83） | ✅（过闸率 55.6%） |
| **USA** | ACTIVE REGULAR 133（09-11 口径）；**PROD 独立卡死 0.86**；582 条回测 sharpe **48% 为负** | **PROD 结构性** | ⚠️（过闸率 54.2%） |
| **GBR** | 180 波 / 180 条 **0 过**，max|S|=1.04 天花板；fundamental 域结构性无超额 | 信号强度 | ⚠️ 维护模式（过闸率 46.7%） |
| **EUR** | 141 波仅 4% 命中率；消化率 2%；候选池 52 颗中 **75% 是 PROD 饱和的 label 族** | PROD 饱和 | ⚠️（过闸率 29.4%） |
| **JPN** | **不支持 sector/subindustry/industry 分组**；**转化率 1.6%（15,185 生成仅 238 回测，全区域最差）** | 无可用分组轴 | ⚠️ 最差 |
| **HKG** | 仅 7 波（A 档塔欠投入）；已验证新信号族 = VWAP 双层动量 × 做空比率制度腿 × `trade_when(volume>adv20)` | — | 可打（一次点亮 SHORTINTEREST + PV 两塔） |

---

## 2. ★ 停投结论（两口径一致，唯一稳健）

**MEA / IND / DEU 停投。**（09-29 口径；各区之后的变化见下方增补，**以区域 profile 的 `entry_verdict` 为准**）

> **2026-10-04 增补**（来源：WorkBuddy 记忆 2026-10-02 / 10-03；`entry_verdict` 是代码读取的字段，区域轮转与步 1 都用它）
> - **IND**：10-02/03 的 20 批 / ~170 表达式 / 14+ 族系统扫描后，可提交空间判定穷尽，`entry_verdict` = `probe-only`（`regions/IND.md`）；上表「中性化最优 = STATISTICAL」与 profile 的 `neutralization_default` 已对齐。
> - **EUR**：10-02 调查（库存 47/47 族 prod ≥ 0.70、7 个战役全 exhausted、可提交新增 = 0）后 `entry_verdict` = `probe-only`（`regions/EUR.md`）。
> - **DEU**：**10-02 起不再是停投**——用户裁决「先修 profile + 降目标到 1–2 颗」，`regions/DEU.md` 升 `active`（升档三条件实测满足；原「sub_universe 结构性墙」是伪墙）。真墙是「合规形态天花板 0.69 vs ladder 1.58」，`active` 不等于能开波，复产前置见 DEU.md。
> - **MEA**：仍 `frozen`。

| 区域 | 样本 | 过闸率 | 95% CI |
|---|---|---|---|
| MEA | 66 | 18.2% | [0.11, 0.29] |
| IND | 53 | 15.1% | [0.08, 0.27] |
| **DEU** | 16 | **0%** | [0.00, 0.19] |

### 过闸率（alpha_id 权威键口径）

```
KOR 72.7%(11) > GLB 58.8%(17) > ASI 55.6%(9) > USA 54.2%(24)
> GBR 46.7%(15) > IND 34.2%(149) > EUR 29.4% > MEA 28.7% > DEU 12.5%(48)
整体 34.6%（128/370）
```

### 回测转化率（已回测 / 总数）

```
MEA 54.5% / GLB 24.2% / IND 24.1% / CHN 14.2% / ASI 12.2% / DEU 12.2%
KOR 10.5% / GBR 7.1% / HKG 6.7% / USA 5.2% / EUR 2.0% / JPN 1.6%
```

---

## 3. 区域细节

### DEU

- **三条独立证据堵死**：① 库存侧 79 候选经互相关撞车剔 42/44，仅 `6XrJ5OvE` 存活但 prod **0.996**；
  ② 结构侧 SELF 墙占满（新增须对 6 颗 ACTIVE 全 <0.7）；③ **测了 42 颗 prod、0 颗 <0.7**。
- **DEU 是精确最大互斥集**：6 颗（`blRnKEk6`/`883Y3bAW`/`Vk65zLzG`/`vRk6og8b`/`2rOe10qY`/`JjxrYjre`）共享 starmine 修订动量共腿
  → **换数据集 ≠ 换信号域，现域无解**。
- **历史 `sub_universe` 结构性墙**（limit ≈ 0.47×sharpe，需 0.8，实测 0.30）；但 09-13/14 实测突破——analyst4 族 + insider + SI 在 DEU 生产池 **PROD 仅 0.54–0.64（方向未拥挤）**，连续点亮 DEU/D1/MODEL(1.8)、SI 2/3、INSIDERS 1/3、OTHER 2/3。
  ⚠ 约束：**同族第 4 颗起 SELF 三面贴边不可再提**。
- `entry_verdict: probe-only`。

### IND

- universe **仅 TOP500**、delay 仅 1 → **无档可换**（勿靠换 universe 救 IND 候选）。
- **中性化最优 = STATISTICAL**（SUBINDUSTRY 最差，极差 0.199）。
- **SA 曾成功**（`QPbjxMYw` 20 组件 0.65），**但 09-22 池子已见顶**（22 颗池实测 0.86–0.97 全不过，4 颗既有 SUPER 硬化了池子）。
- **75 条 pc_null 全量补测：67 WALL / 8 PASS，撞墙率 89%**（PC 0.7117–0.9958）；最干净字段组 3 条 probe 也全撞（0.8245/0.8577/0.8736）
  → **撞墙是结构级/信号级饱和，非字段级**。
- 未点亮塔（09-19）= earnings / imbalance / insiders / institutions / macro / news / option / sentiment / shortinterest。
- `signal_floor = 1.2`（`thresholds.json`，11 区最严）。

### GLB

- **设置格实测过闸率**：`TOP3000` / `SUBINDUSTRY` / `decay4` **全 0%**（n=25/53/15）；
  替代格 **`TOPDIV3000` 27.5% / `STATISTICAL` 77.6% / `decay2` 90.9%**。
- 全球组合极易在 EMEA/APAC 塌方（`E5pYL2rP` EMEA 0.44 / APAC 0.92 / 2Y 1.06 被 BLOCKED）。
- 7 颗 REGULAR，组不了 SA（差 3）。

### USA

- **PROD 独立卡死**（恒 0.86 不随 SELF 下降）；582 条回测 sharpe **48% 为负**、仅 2 条 ≥1.58、fitness 无 ≥1.0 → **0 达标**；测 6 颗 prod **0 颗 <0.7**。
- 33 颗 REGULAR，可组 SA。**USA 是唯一有 OS 数据的区域**。
- 五变体全废而 KOR 一发即中，差别在于 **KOR 的 STATISTICAL 档还没被用过**。

### GBR

- **fundamental 域结构性无超额**（`fundamental6` + `fundamental72` 双集实证，best|S|=0.55，CONCENTRATED_WEIGHT 结构性超闸）。
- `fundamental72` 552 字段（396 VECTOR + 156 MATRIX），**MATRIX 全为低频年报报表行项（users≥50=0）→ CW 墙**。
- **GBR 漏斗实测**：8710 表达式 → 门禁放行 913 → 回测完成 722 → 过廉价闸 65 → 就绪 4；**未消化 86.3%**
  → 瓶颈 = 过廉价闸→就绪（保留率 6.15%）→ **步 4 GEM 在 GBR 当期边际价值为负**。
- 点塔价值最高：`WjAV89jG`(OTHER 1.9 + MODEL 2→3)、`A1G7o1EE`(PV 1.8)。

### EUR

- 141 波仅 **4% 命中率**；候选池 52 颗 sharpe≥1.58 中 **75% 是 PROD 饱和的 label 族**
  （`quantile_label_1bucket_20day_ohlcv` 27 条 PROD≈0.80、`probability_label4_5quantile_20day_ohlcv` 8 条 2.43）。
- 有效信号来源：盈利惊喜 / 多周期基本面 / 图表形态相似度（`avg_similarity_v_reversal_bottom` 等）/ ravenpack 新闻计数 / 风险模型 earnyild。
- **门禁筛失败 74.6%**，主因结构加权混合 1,430 条 + FIELD 1,426（高度重叠）。

### KOR

- **分析师族深挖已饱和**（prod 0.9+）；`insiders5` 族信号天花板 **~1.05**（w177–w181 五波共 30 条，0 达标）。
- SA 的 PROD 是 **0.78 结构性地板**（与评分/decay 无关，V7 0.7821 / V8 0.7832）。
- **KOR 库存 989 条实测**：过闸 94 条（9.5%）；**STATISTICAL 14.63%(n=205) 最优**，**SUBINDUSTRY 仅 1.64%(n=61) 为全场最差**。
  ⚠ 与旧 profile「KOR 实证 SUBINDUSTRY 最优」**相反**，以实测为准。
- 算子数：**≤4 算子 14.34%** > 5-8 8.88% > >8 6.53% → **表达式越简越好**。
- decay：**14 → 33.3%(n=21)**、4 → 14.07%(n=327)、16 → 12.5% → 主力 decay4，可探 14。
- 字段族过闸率：**probability 59.1% > global 38.1% > short 23.8% > eps 22.7% > anl 5.6%**。
- **KOR/D1 塔点亮实测（2026-09-28 平台）**：
  - 已点亮 = analyst 6 / fundamental 3 / model 4 / other 6 / pv 3
  - 未点亮 = shortinterest 0~1、earnings / imbalance / insiders / institutions / macro / news / socialmedia / sentiment / risk 全 0
  - ⚠ 与旧指令「重点 Other / PriceVolume 未点亮」**不符**（other/pv 已点亮）。

### ASI

- **最大机会池**：370 颗未提交存量中占 **95 颗且从未测 prod**（已测 2 颗均 ~0.51，明显低于 0.7）。
- 用 `MINVOL1M` universe，delay 12 档实测可行（SECTOR 中性化）。
- **绑定墙是 prod 不是 self**：头部 3 颗 probe（npdZX3Zx 0.8285 / gJbR0xRl 0.8005 / levQYLNN 0.8282）全 >0.7，而 self 0.6617/0.6506/6630 **全过**。

### JPN / HKG / TWN

- **JPN**：不支持 sector/subindustry/industry 分组；wave1 是空壳行；转化率 1.6% 全区域最差；无 `s0_ranking` 行。
- **HKG**：仅 7 波（A 档塔欠投入）；现有池 16 颗不可提交（最强 `YP5pZ8gA` S1.11 且带 LOW_SHARPE/FITNESS/2Y 三项硬 FAIL）。
- **TWN 永不补**：DB 无 datasets/fields 且 WebDataScope 包内 0 源 → 任何补包手段无效，**TWN 绝不能开 enforce**。

---

## 4. ★ 已判死数据集清单（勿再投入）

| 区域 | 数据集 | 死因 |
|---|---|---|
| IND | `insiders1` | 两波 28 条真实回测 0 达标（直接用法 + 事件窗重平滑） |
| IND | `sentiment23` | alpha 密度 3958，最饱和 |
| GLB | EMOTION `ohlcv_img` 族 | PROD 0.82–0.86 |
| GLB | `predicted_first_quantile_ten_day_return_*` | prod 0.9989 墙 |
| GLB | `techindi_model` | — |
| DEU | `option1` / `pv20` / `fundamental17` | **字段级 coverage 全 0.0 = 空集** |
| DEU | `risk60` | best|S|=0.29 全灭 |
| DEU | `other699` | best|S|=0.48（<0.5 判死）；**零竞争 ≠ 有信号**（users=0 只是弱先验） |
| GBR | `fundamental6` / `fundamental72` / `macro27` | fundamental 域结构性无超额；macro27 fast_kill（best|S|=0.81） |
| KOR | `insiders5` | 天花板 ~1.05（dead_end `KOR-INSIDERS5-CEILING-20260909`） |
| HKG | `pv14` 期货基差 | sh −0.01~0.46、ladder ≤1.03 |
| HKG | `mdl110_score` 族 | `KP6mqrQ1`/`WjdLwJ8x` 双双 `CLUSTER_TEST ERROR` + SELF/PROD 全 PENDING |
| 跨区 | **risk70（风险模型因子载荷）** | 三区独立复现死族（IND/KOR/GLB）；best S=0.87 |
| 跨区 | fundamental17 | 六区死（含 `IND-FND17-ANNUAL-DEAD`） |
| 跨区 | fundamental6 / risk68 / insiders1 | 多区死 |
| — | `shortinterest3`（KOR） | 死路（`KOR-SHORTINTEREST3-DEAD`） |

### ★ 跨区死路检查（必做，已固化进 ra-pipeline 步 1）

> **教训**：跨区台账显示 `IND-RISK70-NO-SIGNAL` + `GLB-RISK70-STYLE-HF-MINVOL1M-FASTKILL`，
> risk70 是**跨三区独立复现的死族**，而 S-PRE 的死路检查只按 `region='KOR'` 查 → **漏掉跨区负先验，白烧 114 次回测**。
> 检索必须**统一 `.lower()` 归一**（旧临场检查大小写敏感，`shortinterest3` 命不中 `KOR-SHORTINTEREST3-DEAD` → 假阴性）。
> 工具：`tools/kor_opportunity_scan.py`（四道过滤：未点亮类别 ∧ 非红榜族 ∧ 跨区死路 ∧ 字段≥5）。

---

## 5. 塔点亮状态与选区

- **已点亮塔不再优先提交 REGULAR**，其候选最多作为 SuperAlpha 组腿；优先提交归属**未点亮塔**的候选（新塔点亮收益最大）。
- **KOR 真实可打集合 = 5 个**（穷举扫描 159 个候选数据集后）：
  `other466`(FUNDAMENTAL, 177 字段, cov 0.827, **平台 4597 条验证**) / `fundamental31`(99) / `model56`(9) / `other395`(368) / `other106`(MACRO, 15)。
- **区域 multiplier 分层（同等投入回报差 1.3–1.7 倍）**：
  DEU 30 格 1.4–2.0（全空白）、CHN 20 格 1.1–1.9（全空白）、GBR 30 格 1.0–1.9、USA 31 格 1.0–1.8、
  EUR 27 格 1.0–1.7、KOR/HKG 各 15 格 1.0–1.7、ASI/GLB 16/13 格 1.0–1.4、IND 15 格 1.0–1.4。
  → **最高 multiplier 的 DEU/CHN 几乎全空白，投入与回报严重错配**。
- **SA 组件池（09-25）**：USA33 / IND23 / MEA19 / KOR13 / GLB10 可组；ASI5 / DEU6 / GBR4 / HKG4 / EUR2 **不够 10**。
  → **能否组 SA 看"池子新鲜度"（REGULAR 数 vs SUPER 数），不只看绝对数量**。
- **账号 `meanProdCorrelation` 已达 0.669**（逼近 0.7 硬闸）→ 这是近期新候选普遍卡 PROD 的**结构性原因，不是选品差**。

---

## 6. 数据可得性

- **WebDataScope 包仅覆盖 7 区**：USA112 / EUR19 / CHN13 / ASI7 / GLB6 / JPN2 / KOR1；**无** DEU/IND/GBR/MEA/TWN/HKG/AMR。
- **体检包缺口（DB 集 ≥5 字段 vs 已有包）**：HKG 172/172 **满**；缺包 GLB 119 / USA 207 / EUR 129 / KOR 153 / IND 115 / DEU 154 / GBR 31 / MEA 11 / JPN 15 / ASI 26 / CHN 6。
- **`entry_verdict` 实测**：DEU=probe-only、IND=active、GBR=active、MEA=frozen、TWN=probe-only → 真正 active 只有 **IND / GBR**。
- ⚠ **`--inspect-mode enforce` 绝不能全局开**：它是 **fail-closed（缺体检包即整波拦截）**，"5 区直接开 enforce" = 把那些区每一波全拦死。
  零写入验证：IND/sentiment21、GBR/pv29、GLB/model264 全 `status=unavailable` → enforce 下拦截。
  **正解：逐波/逐集手动档**，顺序 = 先补包 → 再对新波显式 enforce；当前仅 IND/GBR 有降级包可安全用。

---

## 7. 经济面规律

- **Base Payment 强次线性**：41 个有收入日累计 $63.98、日均 $1.56（区间 1.23–1.89）；
  Quantity 曲线 1→1.44 / 2→1.53 / 3→1.69 / 4→1.77 / 5→1.82，**5 颗仅比 1 颗 +26%，边际 ~6.5%/颗**；vf 恒 0.5 档位锁死。
  → **杠杆排序：退役负 OS（抬 vf）> 降 meanProdCorr > 跨区分散/踩 Theme > 提数量**。
- **VFT 诊断**：`S_P`（金字塔覆盖广度）是**唯一结构性瓶颈**（35/212 = 0.165；`S_H` 已饱和 0.91）。
  S_A 拉满到 1.0 总分也只到 0.152，而 P 由 35→70 可使分数近翻倍
  → **提 VFT 最大杠杆是扩覆盖面，不是提 Atom 占比**。
