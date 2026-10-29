# 03 · 区域与数据集特性

> 来源：2026-09-05 ~ 09-29 工作日志实证提炼 ｜ 更新：2026-10-24（§4 增 USA 清单指针，新增 §9 USA 复盘读数）
> §2 的区域口径有 2026-10-04 增补，以各区 `regions/<R>.md` 的 `entry_verdict` 为准。
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
| **USA** | **47 个集**（fundamental 全线 / `risk60` / `other143` / `other635` / `pv106` / `chart_return_model` / `chart_model_alpha` …） | **不在此重复列举**：机读清单 [`tracking/USA/reference/usa_dead_datasets.md`](../../tracking/USA/reference/usa_dead_datasets.md)（每条带 `verdict` / `reason` / `evidence` / `as_of`，120 天过期；`campaign_intel s0-select` 自动剔除） |

### ★ 跨区死路检查（必做，已固化进 ra-pipeline 步 1）

> **教训**：跨区台账显示 `IND-RISK70-NO-SIGNAL` + `GLB-RISK70-STYLE-HF-MINVOL1M-FASTKILL`，
> risk70 是**跨三区独立复现的死族**，而 S-PRE 的死路检查只按 `region='KOR'` 查 → **漏掉跨区负先验，白烧 114 次回测**。
> 检索必须**统一 `.lower()` 归一**（旧临场检查大小写敏感，`shortinterest3` 命不中 `KOR-SHORTINTEREST3-DEAD` → 假阴性）。
> 工具：`tracking/KOR/scripts/kor_opportunity_scan.py`（四道过滤：未点亮类别 ∧ 非红榜族 ∧ 跨区死路 ∧ 字段≥5）。

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
- ⚠ **宇宙可用性是账号级的，论坛帖里的宇宙名不能照抄**（2026-10-24 USA/D1 实证）：
  `ILLIQUID_MINVOL1M` 对本账号 **不可用** —— 派发 10/10 条全部
  `400 {"settings":{"universe":["Universe ILLIQUID_MINVOL1M is not available."]}}`。
  同一帖作者（USA/D1 同区同 delay）却能用它把 SubU 从 0.7 抬到 2.14–2.28。
  两个预检口都不可靠：`/options/universes` 返回 **404**（无此端点），
  `get_datafields(universe="ILLIQUID_MINVOL1M")` 返回 **0 字段**（连 `pv1` 也是 0，所以 0 不代表宇宙非法）
  ⇒ **唯一判据是派发一次**。已知可用：USA/D1 的 TOP3000 / TOP2000 / TOP1000 / TOP500 / TOP200。
  推论：抄论坛的「宇宙杠杆」前先花 1 条仿真验证宇宙存在，别把整波压在未验证宇宙上。

---

## 7. 经济面规律

- **Base Payment 强次线性**：41 个有收入日累计 $63.98、日均 $1.56（区间 1.23–1.89）；
  Quantity 曲线 1→1.44 / 2→1.53 / 3→1.69 / 4→1.77 / 5→1.82，**5 颗仅比 1 颗 +26%，边际 ~6.5%/颗**；vf 恒 0.5 档位锁死。
  → **杠杆排序：退役负 OS（抬 vf）> 降 meanProdCorr > 跨区分散/踩 Theme > 提数量**。
- **VFT 诊断**：`S_P`（金字塔覆盖广度）是**唯一结构性瓶颈**（35/212 = 0.165；`S_H` 已饱和 0.91）。
  S_A 拉满到 1.0 总分也只到 0.152，而 P 由 35→70 可使分数近翻倍
  → **提 VFT 最大杠杆是扩覆盖面，不是提 Atom 占比**。

---

## 8. 数据集选池：看「开采度」，不看 category（2026-10-23）

> 来源：2026-10-23 EUR 全池战役（169 集 / ~1700 条仿真）+ DEU 平台实扫。
> 全文与脚本：`Claude/skills/wq-brain-ra-deu/references/_dataset-scan-method.md`、
> `Claude/skills/wq-brain-ra-deu/scripts/dataset_scan.py`（区域通用，`--region` 可换）。
>
> ⚠ 2026-10-24：这两个文件此前**只存在于宿主安装位**（`~/.workbuddy/skills/...`），仓库没有 ——
> 违反「不允许源码/结论只存在于工作区」（AGENTS.md §7）。已回灌到 `Claude/skills/`。
> **写 skill 一律改仓库 `Claude/skills/`**，改完 `python tools/sync_skills.py` 推送到安装位，别反过来。

### 8.1 category 不等于开采进度（EUR 反例）

EUR 画像池 178 集（可挖 169）。按 `INSTITUTIONS / EARNINGS / INSIDERS / MACRO` 四类轮转，
实际池内只有 **9 个集，且全部已跑完** ⇒ 一整轮 category 轮转 **0 产出**。
每个 category 在 `dataset_profile` 里往往只有 1–3 个集，**按类目轮转必然空转**。

### 8.2 选池四档

```
X  不可挖   n_fields < 3 ／ platform_empty ／ coverage 恰为 0
V  处女地   alpha_count <= 10 且 value_score >= 5
U  未点亮   我方该 category 已提交 <= 3
L  已点亮   我方该 category 已提交 > 3
```

平台 `alpha_count` = 全站该数据集产出的 alpha 数（所有人），2026-10-23 EUR 逐集核对 13/13 与本地一致。

### 8.3 两条最容易踩的语义

1. **`coverage == 0` ≠「覆盖低」**，而是**该 region×universe 没有任何数据**。DEU/TOP500 平台 92 个集里 **63 个是 0**（68%），可挖只剩 29 个。不区分会把废集当处女地。
2. **覆盖率闸必须分两级**：集级 0.8（处女地放宽 **0.35**）决定「开不开这个集」；字段级 0.6（DEU 实证值）决定「用哪些字段」。**用字段级门槛筛数据集 = 整批误杀处女地**（EUR 21 个集被 0.8 一刀切掉）。

### 8.4 处女地的共性

EUR 实测：`alpha_count ≈ 0` 且 `value_score ≥ 5` 的集**覆盖率普遍低**。
它们空着不是没信号，是**没人愿意处理脏数据** —— 典型 `equity_forum_data`（VS 6.0／全站 0 alpha／cov 0.41）、
`workforce_flow_skills`（VS 6.0／0 alpha／cov 0.25）、`news_sentiment_dl`（VS 6.0／2 alpha／cov 0.76）。

### 8.5 本地表不可直接用于选池

本地 `datasets` 表的 `coverage` / `value_score` 大面积缺失或写死占位：
DEU 193 行里 **121 行 coverage 为空/0**、`value_score` 大量写死为 10。
离线选池会把 104 个集标成处女地（平台真值 = 5 个）。
⇒ **选池必须走平台实时画像**（`get_datasets(region, universe, delay)`）。

### 8.6 区域入场状态以各区 skill 面板为准

本表 §1 的 DEU 行写「停投（2026-09-29）」，但 2026-10-08 DEU 战役已产出 2 颗**合规单信号** alpha
（`58gkLAkk` MODEL S1.75/2Y2.07 已提交 ACTIVE；`9qWX78vX` ANALYST S1.65/F1.47 0 失败），
skill 面板据此改为 **probe-only**（真瓶颈是「合规字段稀缺」，22494 字段里单信号过线仅 1 个）。
**判区状态以 skill 生成面板的 `entry_verdict` 为准，本表用于横向对照。**

---

## 9. USA 复盘读数（2026-10-23，1698 回测行 / 110 波）

> 来源与复现：`reports/usa_mining_history_review_20261023.md`（附录 A 为只读复现命令）；
> 区域层归档：`tracking/USA/reference/usa_mining_conclusions_20261023.md`。

### 9.1 规模与转化

| 指标 | 值 |
|---|---|
| RA 硬闸全过 | **177 / 1525（11.6%）**（`payload_json.failed_checks ∩ RA_CHECK_NAMES` 口径） |
| 走到 prod 实测 | 26（14.7%） |
| prod<0.7 **且** self<0.7 | **4 颗 ⇒ IS→可提交转化 15.4%** |
| prod 分布（n=92） | `≥0.8` **44.6%** / `[0.7,0.8)` 12.0% / `<0.7` 43.5% |

### 9.2 闸频次（行级 n=1525）

`LOW_FITNESS` 84.2% > `LOW_SHARPE` 82.4% > `LOW_2Y_SHARPE` 76.5% > `LOW_SUB_UNIVERSE_SHARPE` 42.1%
> `CONCENTRATED_WEIGHT` 14.6% > `HIGH_TURNOVER` 4.8% > `LOW_TURNOVER` 3.5% > `IS_LADDER_SHARPE` 1.3%。
前 3 项高度共现 ⇒ **一次修好一个闸没意义，必须换机制或换字段族**；
SUB 是比值闸（USA 系数 ≈0.433），**抬 S 会同步抬它的要求**。

### 9.3 三条选集判据（本轮新增）

- **判据 A（最重要）**：**「RA 全过率」不能用作选集指标**。它衡量信号强度，交付卡口是「机制在生产池里拥不拥挤」，
  两者在 USA **反向**（RA 全过率 80%/59.6%/30.4% 的三个集 prod 分别 0.9908/0.9206/0.9636）。
  ⇒ 选集问**机制是否经典异象**，不是数据集是否冷门。
- **判据 B**：**max S < 1.58 的数据集直接出局**（`pv106` 0.00 / `shortinterest29` 0.79 / `other596` 0.91 /
  `multi_horizon_alpha` 1.16 / `fundamental14` 0.84 / `chart_return_model` 1.46）。
  ⇒ 开波前用 1 条裸探针验强度（`|S|<0.5` kill，0.5–1.0 需改机制）。
- **判据 C**：**prod 探针前移到第 1 波**（每族 1 颗探针的 prod 额度，不占回测槽，`prod ≥0.75` 即封族）。
  历史代价：`other143` 用 8 波、`risk60` 用 3 波才测出撞墙 ⇒ **13/110 波（11.8%）白投**。

### 9.4 未点亮塔的 category × 数据集实测产出（2026-10-28，16 条 ATOM 探针）

平台实扫 USA/D1 塔位（`get_pyramid_alphas`）：**只点亮 model 4 / analyst 6 / earnings 1**，
其余 **13 座塔全为 0** —— 这是本轮"未点亮塔优先"的出发点。

| 数据集 | 平台 category | 探针数 | 最好 S | 最好 2Y | 判定 |
|---|---|---:|---:|---:|---|
| **`risk65`** | **RISK** | 3 | **1.98** | **2.18** | ✅ **唯一过结构性双墙**（sub 1.75），参数层可修 |
| `option3` | OPTION | 2 | 1.61 | 1.34 | ⚠ 有信号但 4 项 FAIL（含 sub 0.61） |
| `short_interest_pred` | SHORTINTEREST | 2 | 0.89 | 1.87 | ⚠ 2Y 强、S 不足 |
| `institutions6` | INSTITUTIONS | 3 | 0.07 | −0.15 | ❌ 持股计数族全灭 |
| `news46` | NEWS | 3 | 0.51 | 0.33 | ❌ RavenPack 情绪型评分全灭 |
| `sentiment22` | SENTIMENT | 2 | −0.04 | 1.52 | ❌ |
| `fundamental93` | FUNDAMENTAL | 1 | −0.53 | −0.96 | ❌ 且卡 CW |
| `mfm_model_output` | RISK | 1 | −0.92 | −0.81 | ❌（符号反，取正 0.92，仍不足） |

**跨轮合成判据（与 §9.3 判据 A/B/C 并用）**：

- **判据 B 的补充**：`max S < 1.58` 的数据集出局 —— 本轮 `institutions6` / `news46` /
  `sentiment22` / `fundamental93` 四集**一轮即出局**，与历史判死清单一致。**一条 ATOM 探针就能
  给一个数据集定生死**，这是 ATOM 形态最大的流程价值（比模板批便宜 8–10 倍）。
- **RISK 塔此前从未被当作 USA 候选**（`risk60` 已在死路清单、`risk70` 是三区死族），
  但 `risk65` 的**特异性收益（dsrt）中间期限分量**是全新机制。
  ⇒ **「riskXX 死过」不等于「RISK 塔死过」** —— 死路清单的粒度是数据集，不是 category。
- **排除清单（零成本预筛，勿再投入）**：`fundamental110` / `fund_holdings_panel` /
  `news29` / `shortinterest3` 全 VECTOR；`macro4` country 级 ⇒ 横截面零离散。
- **数据集名不可作塔位与语义依据**：`other416/452/466/551/553` 实际落在
  fundamental / macro / sentiment（详见 `05_antipatterns.md`）。

### 9.5 「近十年有数据」的验证口径

`submit_batch` 按区域档案派发的 `startDate` 为 **2013-01-01**，但回测结果的 alpha 详情
`metrics.startDate` 实测为 **2014-01-01** ⇒ 差额说明**该数据集自身首行数据从 2014 起**，
可作为"近十年有数据"的**间接**证据。
要**直接**验证须用 `get_alpha_yearly_stats` 逐年核（本轮未做，勿把间接证据当直接结论）。

### 9.6 RISK 塔（USA D1）的可用供给地图与定案配方（2026-10-28 实查 / 2026-10-29 定案）

**点亮口径**：同塔**本季度累计 3 颗**，且三颗之间**两两互相关 < 0.5**（塔计数每季度首日清零）。

**★ 关键机制更正（2026-10-29）**：点亮某塔**不要求信号腿来自该塔的数据集**。平台按「表达式引用到的所有数据集字段」登记塔位，因此只要把 RISK 字段放进**分组轴**（`group_neutralize` / `bucket(rank(...))`），`ra.pyramid_short` 就会出现 `risk`。
⇒ RISK 塔的正解是**「外部信号腿 + RISK 分组锚」**，不是在 risk* 数据集里硬找信号。定案三颗的信号腿全部来自 `ai_equity` 与 `earningscall_sentiment`。

（`risk*` 数据集自身的信号供给仍然值得知道，但下表要按「能不能当信号腿」读）

| 数据集 | 字段 | 类型 | 覆盖 | alphaCount | 判定 |
|---|---|---|---|---|---|
| `risk70` | 约 20 个真因子字段：`financial_leverage_factor`(aC 10) / `systematic_risk_beta_factor`(3) / `residual_volatility_factor`(14) / `market_capitalization_factor`(4) / `price_momentum_factor_score`(9) / `trading_liquidity_factor` / `earnings_yield_factor`(110) / `news_sentiment_factor`(35) / `downside_risk_factor`(6) / `short_interest_factor_2`(10) / `earnings_quality_factor`(15) / `relative_valuation_factor`(100) / `growth_characteristic_factor`(29) | MATRIX | 1.0 | — | ★**本轮主力用途 = 分组锚**（bucket 原料）；当信号腿未见强读数 |
| `risk70` | 110+ 个 `*_sector_score` / `*_industry_score` | MATRIX | 1.0 | 114789（整集） | ⛔ 近静态横截面暴露表，只配当分组原料；当信号腿 S −0.92 |
| `risk65` | `rsk65_mfm_etfm4_dsrt_intermediate` | MATRIX | 0.9743 | 538 | 历史最强单点（S 2.94 / F 1.09 / invest 比 0.867，只卡换手 0.7559）；**`dsrt` 族后续判死** |
| `risk72` | `rsk72_top3000_dsrt` | MATRIX | **1.0** | 1649 | 与 `risk65` 同属特异性收益概念 ⇒ 同族；**按结论 35 特异性收益族永久跳过** |
| `risk59` | 16 字段（`shortinterestpct` / `s3utilization` / `squeeze_risk` / `offer_rate` / `daystocover*`） | 全 VECTOR | 0.9303 | 5319 | ⛔ 证券借贷族**已判死** |
| `risk60` | 5 字段（`rsk60_offer` / `rsk60_last` / `rsk60_crowding` / `lending_fee_bid_rate` / `rsk60_datatime`） | 全 VECTOR | 1.0 | 5693 | ⛔ 同上；`rsk60_datatime` 是元数据（时间戳），不可作信号 |
| `risk62` | 636 字段 | — | — | 24130 | ⛔ 拥挤度极高，已判死 |

`risk72` 三个 `_dsrt` 变体按宇宙切分：`top3000`（覆盖 1.0）/ `top2000`（0.7194）/ `top1000`（0.3674）⇒ **只有 `top3000` 覆盖达标**，另两个在 TOP3000 宇宙下覆盖率不足。

**定案三颗（3/3，两两互相关 0.0596–0.389，全部 < 0.5）**

| alpha | 信号腿（数据集） | 塔位 | S | F | tvr | 2Y | sub | invest 比 | fRA | self |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `9qxLOPxr` | `buzz_intensity_score_2 − 11`（`ai_equity`） | `risk/model` | 2.69 | 1.67 | 0.159 | 2.24 | 1.44 | **1.0112** | 0 | 0.2866 |
| `88RdZ61v` | `credit_risk_model_score_5 − 7`（`ai_equity`） | `risk/model` | 2.65 | 1.46 | 0.159 | 2.07 | 1.64 | **0.9434** | 0 | 0.2612 |
| `E56XvX90` | `assetutilization_sentiment_polarity`（`earningscall_sentiment`） | `risk/other` | 1.75 | 1.13 | 0.033 | 2.39 | 1.05 | **0.9314** | 0 | 0.5457 |

**正解形态（第 3 颗用的慢速 hump + 三重风险 bucket）**

```text
hump(
  group_neutralize(
    group_neutralize(
      group_neutralize(
        group_rank(ts_zscore(ts_backfill(vec_avg(<信号>), 126), 504), subindustry),
        bucket(rank(market_capitalization_factor), range="0,1,0.1")),
      bucket(rank(trading_liquidity_factor), range="0,1,0.1")),
    bucket(rank(price_momentum_factor_score), range="0,1,0.1")),
  hump=0.0001)
```

设置：TOP3000 / delay 1 / decay 5 / **CROWDING** / trunc 0.08 / nan ON / 2014-01-01~2023-12-31。三层分组分别对应 **tvr / 2Y / invest** 三闸。

**配方中四条实证**

1. **锚字段选择 > bucket 粒度**：`financial_leverage_factor` / `systematic_risk_beta_factor` 能把 2Y 抬到 2.13–2.24；`residual_volatility_factor` 只保基线 1.52。
2. **族内取哪一颗按 `sub_universe_sharpe` 排，不按 fitness 排**（fitness 高的那颗 sub 常更差）。
3. **同族变体互相关 0.927–0.973**（四变体实测）⇒ 一个经济概念只出得起 1 颗；「3 颗」= 3 个正交经济概念。
4. **挂靠只允许外挂**：把 RISK 字段放进 `group_neutralize` 的分组轴即可，**不要用零权重乘法**（`add(signal, multiply(rank(f), 0))` 会被判套利规则）。反过来，想只登记单塔 ⇒ 表达式里不能有别的数据集字段（内置 `returns` / `close` 会顺带登记 PV 塔）。

**两塔组合配额（派发前闸）**：`python tools/gates/tower_quota.py --region USA`。截至 2026-10-28 实测：`model/risk` 已 **6 颗**（超配封盘）、`other/risk` 占满 **3 颗**（封盘）、`analyst/risk` 1 颗。**配额是派发前闸，不是事后盘点**——这一轮两个组合都是挖完才数出来的。

**`mfm_model_output` 不适合当信号源（重要排雷）**：117 个字段里约 **110 个是行业/板块因子暴露 score**（`*_sector_score` / `*_industry_score`），是**近静态横截面暴露表**，做 alpha 信号没有预测力、彼此高度共线（只适合当分组的原料，不是信号腿）；真因子只有 `hedge_fund_ownership_factor0`（users 210）、`systemic_risk_factor_score` 等少数。该集**已用冠军骨架探针过，S −0.92**，与上述结构判断一致。
另：字段描述错位再次确认 —— `discount_store_retail_score` 的描述写成「Daily specific (idiosyncratic) returns for stocks」，与该字段名毫无关系。
