# KOR 会话挖掘经验总结（2026-10-30 ~ 10-31）

> 定位：**区域经验层**（`tracking/KOR/reference/`），不是共享 KB。
> 本文件只收「下次能直接照着做 / 照着不做」的判据，每条带实测出处；
> 逐波原始读数仍在 [`unlit_towers_roadmap_20261030.md`](unlit_towers_roadmap_20261030.md)（下称 roadmap）与 `datasets/<ds>.md`。
> ✅ **双轨同步已履行（2026-10-31）**：本文件的跨区可迁移结论已提升到共享 KB ——
> `docs/experience/01_platform_gates.md` §14/§15/§16、`02_signal_patterns.md` §17、`04_engineering.md` §15/§16；
> 机器层新增全局 4 条 + KOR 区域 1 条规则（清单见 §6.10）。
> ⚠ KOR 那条**已写进运行期真相源 DB `ledger_kv`**（只改文件等于白改，见 §6.11），
> 文件镜像已回填为 DB 全量 9 条；`AGENTS.md` §5 第 0 条同步了写入口径。
> 守护已跑绿：`test_experience_kb_refs.py` + `test_methodology_rules_consistency.py` + 等价替换闸共 **33 passed**，
> 镜像回填后相关守护 **637 passed**（另 3 条红属并行会话 HEAD 存量，已归属见 §6.10），
> `sync_skills.py --check` 五个安装位零漂移，`doc_path_refs.py` exit 0（无新增死指针）。
> **功能级已验证**：`apply_rules(...,"strategy",KOR/TOP600)` 返回 18 条，新增 5 条全部命中并会被打印。

---

## 0. 总量口径（DB 实测，不是估算）

**本会话**（`list_wave_results(region=KOR, limit=70)`，按 `created_at ≥ 2026-10-30` 过滤）：

| 项 | 数 | 备注 |
|---|---:|---|
| 落库波次 | **70** | wave 189 → 271（区间内缺 208/217–222/240/246–250，属未落库或并入他波） |
| verdict | FAIL **57** · PARTIAL **10** · PASS **3** | PASS = wave 225 / 251 / 253 |
| status | closed 67 · open 3 | open 含 wave 265（零配额库存复核波） |
| 候选行 | **125** | |
| 过硬闸（S≥1.58 & F≥1.0 & 2Y≥1.58） | **5 + 1** | harvest 自动判 5（`leAk66xx` / `rKRLLzRa` / `leA22za2` / `3qoxag8z` / `d5WmEarw`）+ 人工终验 1（`LLZ6wZO2`，wave 265，`tag=submit_verified`，无 `pass_hard_gate` 键故不计入自动 5） |
| 会话最高 S | **1.99** | `LLZ6wZO2`（wave 265）与 `d5WmEarw`（wave 253）并列 |

**全 KOR 战役累计**（`get_mining_yield(region=KOR)`，非本会话独占）：
expressions 2931 · consumed 1240 · backtested 1009 · conversion 42.31% · passed 177 ·
ra_clean 80 · **prod_clean 14** · **prod_blocked 15** · ra_unknown 310 ·
yield_rate **7.93%** · **prod_wall_ratio 51.72%**。

> **读数**：`prod_wall_ratio ≈ 0.52` 意味着**过 RA 闸的候选里有一半死在 prod**，
> 不是死在信号强度。这决定了本会话后半段的重心从「再挖一条」转向「先把 prod 取到手」（§2）。

**唯一可交付**：`LLZ6wZO2`（S 1.99 / F 1.53 / 2Y 2.24 / subU 1.21 / TO .144 / dd .0387 /
CLUSTER .94 / prod **.6762** / self **.6760**，`checks.fail=[]`，塔 KOR/D1/**FUNDAMENTAL 3/3 已满**）
⇒ 提交它**不点新塔**，且需用户确认。**60 颗目标在现有攻击面上结构性不可达**（§5）。

---

## 1. 平台事实（不可协商；设计前先查，别靠猜）

| # | 事实 | 实测出处 | 对设计的约束 |
|---|---|---|---|
| 1.1 | **IS 窗由平台硬定 2014-01-01 → 2023-12-31，只能变窄不能平移** | roadmap §7.5：显式传 `2015-01-01/2024-12-31`，**HTTP 201** 且回执 `settings_source=explicit`、`settings_used` 逐字回显 2015/2024，但**子 alpha 落库被改写成 2014/2023** | 「十年不够就移窗」这条路**不存在**；任何时段判定直接按 2014–2023 计年数 |
| 1.2 | **`coverage` 是横截面覆盖率，不是时间覆盖** | wave 216：`sentiment26` cov .356 但数据 2017 起 = **7/10 年**；`macro63` cov **1.0** 却 **10/10 年 `longCount=0`** | 约束 4 只能用 `get_alpha_yearly_stats` 的逐年 `longCount` 判，**不能用 coverage 预判** |
| 1.3 | **2Y 闸 = 1Y 闸 = 1.58** | roadmap §5.1：wave 214 六条 `LOW_2Y_SHARPE.limit` 恒 1.58，双侧自洽（2Y 1.62/1.60 落 pass，0.17/−1.94/0.08 落 fail） | 本地 `thresholds.json` 的 `two_year_sharpe_min: 1.0` 是**早期筛选线不是平台线**；按它判「2Y 已过」会系统性高估近闸程度 |
| 1.4 | universe 唯一合法 **TOP600**；`decay` 单独扫只动 TO 不动 returns；`truncation` 零杠杆 | KOR 已死轴清单（roadmap §4） | 这三条**禁入 quota**，不是「再试一档」 |
| 1.5 | **塔票跟 `pyramids.list`，不跟 category 标签** | `other496`/`other695` → OTHER ×1.6；`oth466` → **FUNDAMENTAL** | 跨类别组腿**借不到塔位**；点塔前必须读 pyramids 而不是看数据集前缀 |
| 1.6 | 点亮 = **当季 ≥3 颗提交**，`get_pyramid_alphas` 是季度口径 | 2026-10-31 实读：fundamental 3 / model 3 / shortinterest 4 = lit；analyst 2 / pv 2 近冻结；other 1 | 跨季会熄灭；「上季点过」不等于本季已点亮 |
| 1.7 | **高分簇未必是 REGULAR** | wave 265：`ds=1150` 簇 S **3.62–4.98**、本地 `alpha_type=NULL`，实为 COMBO/SELECTION（`combo_a(alpha)` / `generate_stats`+`self_corr`、`selectionHandling=POSITIVE`/`selectionLimit=10`）；`3qoWQKJg` 是 **SUPER** | 盘点 REGULAR 供给时**必须先按表达式形态与 settings 剔掉 COMBO/SELECTION/SUPER**，否则会把 4.98 当成「已有高分可提交」 |
| 1.8 | 平台按**表达式 + 设置逐字相同**去重，返回同一 alpha id | roadmap §7.5 佐证 1：wave 214 E1 与既有基线同返 `QPvr1vPM` | 设置对比波会被 multisim 去重吃掉 ⇒ 对比实验必须让表达式或设置**真的不同** |

---

## 2. 判定纪律（本会话最大的一类事故来源）

### 2.1 ★ prod 墙先于一切「只差某条自设限制」的争论

三个独立实测案例，形态完全相同——**指标全闸 + 纯格 + ATOM，然后 prod 判死**：

| alpha | S | prod 实读 | 曾被记成的「唯一卡点」 | 结局 |
|---|---:|---:|---|---|
| `leA22za2` | 1.92 | **0.8377** | 覆盖率 / 约束 | D0-P 判死 |
| `d5WmEarw` | 1.99 | **0.8395** | 同上 | D0-P 判死 |
| `leAk66xx` | 1.77 | **0.8711** | **「只差用户约束 4（2018 前无数据）」** | D0-P 判死，**约束 4 之争就此 moot** |

`leAk66xx` 是本战役**首条 `fail=[]` 的纯格 OTHER ATOM**
（`hump(group_rank(ts_sum(ts_backfill(vec_avg(oth695_import_value_4),66),20),sector),hump=0.0025)`，
F 2.11 / 2Y 2.24 / subU 1.68 / TO .0306，OTHER ×1.6 effective 1），
prod `checked_at=2026-10-31T18:11:46`、age 5.4h、`stale=false`。

> **铁律**：在向用户请求任何「放宽覆盖率 / 放宽约束 4」之前，**先把新鲜 prod 取到手**。
> 「指标全闸」不蕴含「只差一条自设限制」——缺的那一道往往是**还没去取的那一个数**。
> 出处：roadmap §8.1，以及 §5.92.6 保留原文的推翻性批注（留痕，不删旧结论）。

### 2.2 本地 prod 缓存 < 0.70 ≠ prod clean

- 队列里 **19 行**本地 prod 落在 **.57–.70**，同族新鲜读数却是 **.81–.935**。
- **文档值也会被证伪**：`mLmGQEq9` 文档记 .6011 → 实测 **.935**（2026-10-30T19:45）；
  `E5pjx9q0` 文档记 .6002 → 实测 **.8105**（2026-10-31T13:34）
  ⇒ roadmap §5.6 所称「shortinterest 真正可承重 2 颗」**全灭**。

### 2.3 无源 / 过期的 prod 一律不可作闸

- **16 行**「prod clean」的 `prod_corr_source=NULL` / `corr_checked_at=NULL` ⇒ **无源旧值**。
- `stale=true`（>48h）不可用于判定；prod 漂移猛，**48h 作废**。

### 2.4 刀锋档必须 `refresh=True`

6 行落在 **.6886–.6958**（余量 **.004–.011**）⇒ 不重测就等于没测。

### 2.5 ★ 族级直方图判据：一次平台读判整族

`[0.7,0.8)` 桶 **n ≥ 1 ⇒ 整族必死**（不是「这一条不行」）：

| 族代表 | prod | 直方图 | 处置 |
|---|---:|---|---|
| `leAk66xx`（other695） | .8711 | [0.7,0.8) **n=5** / [0.8,0.9) n=2 | 整族不可救，`j2YWRzXW` **不再费 prod 槽** |
| `pwdoY39V`（pv106 唯一过闸） | .8507 | [0.7,0.8) **n=1** / [0.8,0.9) n=2 | 族级必死，PV 格（2/3）存量无补席 |
| shortinterest38 族 | .935 / .8105 | [0.7,0.8) **n=5** | 整族死（且塔 4/3 已满） |

### 2.6 ★ `submit_ready.status` 是本地队列态，不是平台裁决

`EXPIRED` + `gate=IS_ONLY` + `towers=[]` 的真实含义 =
**「从未做过提交层核验、从未做过塔位归属」**——**既不是候选，也不是死**。

收口手法（零配额）：**抽样 + TO 签名聚类**。
163 行队列里 25 行 prod<0.70，用 **4 次** `get_alpha_details` + TO 签名（.1744–.189）
与同形 EXPIRED/IS_ONLY 判掉 **19 行**（6 行直接取证、13 行签名聚类）⇒ **省 19 次平台读**。
最终 25 行 = shrt38 死族 19 + RA 可投资性 DEAD 2（`A1vOb5pE` S2.54 / `ZYAWx9J3` S2.26）
+ SELF_BLOCKED 2 + SUPERSEDED 重复 1（`A1NXddRw`）+ READY 1（`LLZ6wZO2`）。
出处：roadmap §8.2。

### 2.7 标签与数值不一致时，信数值

`wpb1GXEd` / `9qWK21rd` 标 `SELF_BLOCKED`，但 self 仅 **.1967 / .1970**（远低于 0.7）
⇒ 真问题是 **prod .6946 / .6929 贴线（且 stale）+ 塔已满**，不是 self。

### 2.8 判定只走平台

合规只看 `get_alpha_details().code`；RA 只看 `is.checks`。
本地 `alphas.failed_ra_count` 是**旧快照**（AGENTS.md §7.5 实测：本地记 0、平台实读 3 闸）。
原始指标在 **`is` 下直接展开**（`is.sharpe` / `is.checks`），**不是 `is.metrics.*`**。

---

## 3. 探针设计：等价性判据（省配额的核心）

| # | 判据 | 实测 | 用法 |
|---|---|---|---|
| 3.1 | **秩不变性**：`rank`/`group_rank` 吸收严格单调变换 ⇒ rank 壳内换聚合算子**不是新探针** | wave 214 #5（`ts_sum`）vs wave 270 E1（`ts_mean`）**逐位相同**：S −0.64 / TO .2104 | 发批前先做等价性自查；`ts_sum`↔`ts_mean`↔`ts_av_diff` 在 rank 壳内只算**一条** |
| 3.2 | **`hump` ≠ `ts_decay`**：hump 作用于**换仓成本**，不是信号均值 | risk59 去掉 hump：S 1.02→**0.90** / F .67→.53 / 2Y 1.80→1.60 ⇒ **hump=0.003 值 +0.12 S，不可压掉** | 「时序平滑在费率族零和」**不能推广成「所有平滑器无效」**；压算子前必须逐算子消融 |
| 3.3 | **`reverse()` 差额 = 2×成本**，不是精确反号（截断 × decay × 符号交互） | roadmap §5.89.3 | 铁律 B：方向**正反各测一条**，猜方向系统性错 |
| 3.4 | `winsorize(rank(...))` 是 **no-op**；`investS` 是**相对闸**；多格记**半分**；镜像分解法 | roadmap 六条平台事实修正（line ~5909） | 别把 no-op 当杠杆；别把相对闸当绝对线 |
| 3.5 | **fitness 分母有 `.125` 换手下限** ⇒ 极低 TO 反而帮 fitness | `docs/experience/01_platform_gates.md` §12（`fitness ≈ Sharpe × sqrt(margin)`） | 「低 TO = 无杠杆」只否定**时序类**修法，**不否定水平型截面溢价** |
| 3.6 | 单变量对照必须**冻结其余全部设置** | roadmap §5 多处（pasteurization / nanHandling / unitHandling / decay / trunc 全列） | 否则不是对照，是换了个实验 |
| 3.7 | 无 `close` 时可用 `divide(uplimit, ts_delay(uplimit,1))` **反推毛日收益** | wave 270 E2；与 PV 内置 `returns` **不同源**故天然正交 | 构造技巧可复用；但**2015 限幅 ±15%→±30% 会留 +13% 假跳变**（1.30/1.15=1.13）⇒ 已知**人为噪声源**，不是市场效应（roadmap §7.3） |

---

## 4. 机制 / 经济结论（KOR TOP600 特异，**不外推到其它区**）

### 4.1 教科书年度变化率异象已被完全定价

| 机制 | 波次 | 最好读数 | 判读 |
|---|---|---|---|
| 资产增长（ARD） | 269 | 0.13 / −0.46 | 截面残余≈0 |
| **RMW**（留存收益/总资产，Novy-Marx 2013 / Fama-French） | **271** | 正向 **−0.34** / 反向 **+0.10**，反向 2Y **−0.57**，TO .0648 双向逐位相同 | **不是方向选错**：翻正也不具备近两年一致性；季频存量比率天然低频，**无时序杠杆可施** |

⇒ 600 只大盘股截面上，公开异象没有残余。**「换个方向再试」不是救援，是重复烧配额。**

### 4.2 分析师三面全灭

- **分歧度**：wave 245 CV 口径 S −0.14 / −0.05 ⇒ **毛 Sharpe 0.05**，机制为零。
- **修正幅度**：wave 216 / 230 / 232 / 267 **四波**判死。
- **覆盖广度**：wave 267（analyst9 修正广度）判死。
- ANALYST 格（2/3）存量补席不可行：全池最高 S **1.19**（`YP1nn09l`，analyst44），距闸 0.39，
  且池内 ANALYST **无任何 prod 实测值**。

### 4.3 ★「同族所以有信号」是倒因为果

`other496` 的 VECTOR 共识族（cov .61–.69）曾被列为 OTHER 塔补席的**首选后备**，
理由是「同族的 `aftercons_percentage` 已出 S 1.61 的 ACTIVE alpha」。
**零配额机制反查后撤销**：逐条映射全落在已死轴上——
`aftercons_stddev`/`beforecons_stddev` = 分歧度（§4.2 毛 S 0.05）；
`aftercons_difference` = 修正幅度（四波死）；`aftercons_numitems` = 覆盖广度（267 死）；
唯一活的 `aftercons_percentage` **已被 `xAY86Mkl` 收割**（S 1.61 / 2Y 1.17，在台 ACTIVE，self .2535 / prod .54）。
出处：[`datasets/other496.md`](datasets/other496.md) §7。

> **可复用手法**：待投字段先**逐条映射到已判死的机制轴**，映射得上就撤销，不必回测。
> 「未测」≠「未死」。

### 4.4 低覆盖注意力数据集：强度 / 换手 / 集中度**三面同时**不达标

`other571`（Wikipedia Viewing Data，wave 268，2 探针，roadmap §7.2）：
23 字段全 MATRIX，cov **.2593–.2660 ≈ 159/600 只**。

| 探针 | 形态 | S | TO | CW |
|---|---|---:|---:|---|
| P1 `GrWMApMJ` | `group_rank(ts_delta(divide(viewstodaymobile, viewstoday),22), sector)` | −0.32 | **.4746** | ⛔ **FAIL 0.633 @2021-02-10** |
| P2 `mLorRMrx` | `reverse(group_rank(divide(views14d, views28d), sector))` | −0.58 | **.6404** | PASS（但 subU ⛔ −0.45） |

三条结构结论（比「判死」本身更有用）：

1. **turnover 是结构性杀手**：.4746 / .6404 是 KOR 全战役最高档
   （对比 analyst 族 .03–.05、risk59 .135）。注意力数据日频抖动 ⇒ 换手天然高 ⇒
   **fitness 被 TO 分母压死，即使 S 到 1.0，F 也上不去**。
2. **CW 0.633 是 KOR 首见的非 1.0 型 CW 值** ⇒ 不是单日权重 1.0 那种极值，
   而是**截面只有 ~159 只可交易导致分散度天然不足**。P2 躲过 CW 是因为占比类背离更分散，代价是 TO .64。
3. **翻正不改变 turnover**（TO 由形态决定，与符号无关）⇒ 铁律 B 的正反对照
   **只能救方向，救不了换手**；别把「翻正」当降 TO 杠杆。

**附带的两条字段画像教训**（0.1 / 0.2 步的产出，零配额）：

- **头部轴 ≠ 直觉轴**：按 alphaCount 降序，`views28dmobile`(a20/u17) > `views7dmobile`(a18/u16)
  ≫ `views28d`/`views7d`(a2–4)，**差 10 倍** ⇒ 该集最强经济轴是**移动端注意力**，不是总浏览量。
- **量纲陷阱**：`views28dmobile` 是**单日**（28 天前那天），`views28d` 是**28 日窗求和**
  ⇒ 直接相除 = 真实占比的 **1/28**，还引入该日特有时间噪声，**不是干净占比**。
  干净占比只能用 `today` 族（有同日总量），或先把 4 个时段桶求和得到该日总量。
  另：`views7d`/`views14d`/`views28d` 是**三段互不重叠的连续历史块**（14d/28d 是「截至 N 天前」），
  不是嵌套窗 ⇒ 可做「近期热度 / 一个月前基线」的加速度比。

### 4.5 regime 依赖：2Y 高 ≠ 全期高

`other496` E2（`j2Y9Ro3Z`）2Y **1.87 已过 1.58**，但全期 S 仅 **0.65**
⇒ 低波动效应只在近两年成立，**不是可提交形态**。
另：韩国 **2020-03~2021-05** 与 **2023-11~2025-03** 两度全面禁空，与 IS 窗重叠
⇒ 借券 / 做空类数据集**必须逐年核 `longCount` 与分段 S**，整体 cov .9806 不能证明分段没退化。

### 4.6 本会话关闭的塔 / 轴（命中即禁入 quota）

| 塔 / 集 | 关闭依据 | 最好读数 |
|---|---|---|
| **risk59** | 三形态轴（水平 / 方差 / delta）+ 聚合×3 + 分组轴×3 全试完 | **1.04**（2Y 2.02），距闸 −34% |
| risk68 | 低波水平 / beta 特征轴（wave 242，预注册分支 (b) 命中） | — |
| risk70 | IVOL 正向 0.57 / 反向 −0.73 | 0.73 |
| **news**（第七个死轴） | 关注度 / 标题计数 = 数据集特异噪声（wave 239） | news85 0.67 / news20 0.25 |
| **macro**（第八个死轴） | `macro63` 恒空仓（10/10 年 longCount=0）+ `other106` 关闭 ⇒ 2/2 不可用 | other106 0.75 |
| earnings3 | 日历距离 3 种几何（zscore / ts_rank252 / tail） | 0.95（2Y 2.17） |
| insiders5 | 库存股轴**真但弱**，方向在**处置侧** | 毛 S≈0.48 |
| sentiment26 | 数据 2017 起 = 7/10 年，违反约束 4 | 0.20 |
| other496 | 四轴全死（ARD 增长 / 涨跌停状态 / 板价倒推波动 / 留存收益水平） | 0.65 |
| other571 / 327 / 424 / 323 | wave 268 / 263 / 264 + 字段级 triage | — |
| **other78 / other323** | **字段级判死，0 配额**（见 §7 手法 4） | 未派探针 |
| shortinterest38 | prod 族死（.935 / .8105），且塔 **4/3 已满** | S 2.35（`VkaWXGmb`）也不可交 |
| other695 | 仅 3 字段 / 1 信号 / cov .4057 ⇒ **无换字段空间**，换几何撞 self；prod .8711 | 1.77 |

### 4.7 分组轴粗细**不是单调**

risk59 三次实测：**sector 1.02 > industry 0.96 > subindustry 0.70**。
⇒ 换粗轴是**无损轴**可优先试；但**别假设越细越好**（本区细轴三次更差）。

---

## 5. 天花板与止损：为什么 60 颗不可达

| 路径 | 定量上界 | 距闸 1.58 | 出处 |
|---|---:|---:|---|
| 单塔单字段 ATOM | **1.04** | **−34%** | wave 213 `vec_avg(rsk59_last_rate)` |
| 2 腿组合（最优权） | **1.238** | −22% | ρ=**0.1978** 实测（1023 日度点，本地计算零配额） |
| **3 腿组合（现存全部可用腿）** | **1.292** | **−18%** | 腿 = [1.02, 0.89, 0.67] |
| 反解：要摸 1.58 | 需 **4 条均 1.0** 或 **7 条均 0.9** | — | [`composite_route_20261030.md`](composite_route_20261030.md) §3.1 |

**两条关键教训**：

1. **机制正交 ≠ 收益不相关** —— 这是原估「risk59 + 0.9 腿 ≈ 1.37」失真的根因。
   组腿前必须 `compute_mutual_correlation` 实测 ρ，不能按机制直觉估。
2. **9/9 未点亮集已测，死法分三类，没有一类是「再加点参数就能过」**：
   ① 信号强度不足（7 个，十年覆盖全 PASS，max|S| 0.25–1.04）；
   ② 恒空仓（`macro63`）；③ 时间覆盖不足（`sentiment26`）。

**存量补席也已穷尽**（wave 265，全库 **691** 条未提交 REGULAR 按 category 盘点）：
FUNDAMENTAL 106（prod 已知 5 条全脏，塔 3/3 满）· SHORTINTEREST 105（塔 4/3 满）·
OTHER 97（其中 45 条属已死 `dl_riskfree` 族）· RISK 72（唯一 prod-clean `QPvr1vPM` S 1.02 / F 0.67 不过闸）·
ANALYST 17（maxS 1.19）· PV 2 · NEWS/INSTITUTIONS/SENTIMENT/INSIDERS/MACRO/EARNINGS 合计 118（maxS 均 <1.0）
⇒ **analyst 2 / pv 2 / other 1 三格补席供给 = 0**。

> **止损结论**：剩余全部是**用户裁决项**（§8），agent 不再自主开波。
> 继续派波只会重复已判死的轴——这正是铁律 F/G 要拦的事。

---

## 6. 工程纪律（本会话实际踩到的）

| # | 坑 | 处置 |
|---|---|---|
| 6.1 | **本地 field catalog 会漂**：`oth496_ard_retained_earn_acc_deficit` 平台**有**（cov 1.00 / u2 / aC2）、本地 catalog **无** | **本地快照不能判「无此字段」**；发批前必过**字段存在性 + 算子存在性 + `op_arity`** 三闸 |
| 6.2 | 一条语法错 ⇒ **整批 CANCELLED**（连坐）；右嵌套三腿 `add` 会**静默** CANCEL | 发批前 `validate_expressions` / `op_arity.ensure_safe_for_dispatch`；禁混信号（`add(rank(A),rank(B))` 同样被拦，**秩化≠豁免**） |
| 6.3 | MCP 大输出溢出落临时文件（`get_submit_ready(status=ALL)` ~241KB、`list_wave_results(limit=70)` ~125KB） | 用 `logs/_tmp_*.py` 解析持久化文件；**不内联 `python -c` 带中文/JSON/嵌套引号**（AGENTS.md §5） |
| 6.4 | 参数名陷阱 | `batch_status` 要 **`simulation_ids`**；harvest 要 **`/simulations/<id>`** 位置形式（裸 id → 404）；`get_wave_result` 要 **`wave_number`**（不是 `wave`） |
| 6.5 | **prod 单槽是账号级、跨会话竞争**（`holder: corr:get_production_correlation(...)`，retry 240s） | 读 `last_known`，**不重复触发**；**仿真槽独立于 prod 槽**，prod 被占不影响派波 |
| 6.6 | 并发上限 **2**（用户约束 3，`create_multi_simulation`） | 填槽不超 2；429 先查僵尸轮询进程 |
| 6.7 | 战役产物落盘 | **只入库（MCP upsert_*）**，禁 `Write`/`Copy-Item` 落 `tracking/*/candidates\|cache\|results\|reviews/*.json\|*.csv` |
| 6.8 | 大文件读取 | roadmap 682KB > Read 上限 256KB ⇒ **必须带 offset/limit** 或用 grep 定位 |
| 6.9 | **共享 KB 双轨义务（已履行）** | 改 `docs/experience/*.md` 必须同步 `Claude/skills/wq-brain-campaign-toolkit/config/methodology_rules.json` + `tracking/<R>/reference/methodology_rules.json`，跑 `test_experience_kb_refs.py` + `test_methodology_rules_consistency.py`，再 `tools/sync_skills.py`（`--check` 零漂移）。**本次落地清单见 §6.10** |

### 6.10 双轨落地清单（2026-10-31，本次实际写入）

**人读层（`docs/experience/`）**：

| 篇 | 新增节 | 内容 |
|---|---|---|
| `01_platform_gates.md` | §14 | prod 读数可信度五级（A–E）+ 三例 refresh 翻案 + 族直方图 + 单并发槽 |
| 同上 | §15 | `submit_ready.status` 是本地队列态；抽样 + TO 聚类收口；高分簇可能是 COMBO/SUPER |
| 同上 | §16 | IS 窗平台硬定（只能变窄不能平移，回执回显 ≠ 落库生效）；`coverage` 是截面口径不是时间口径 |
| `02_signal_patterns.md` | §17 | 探针等价性（rank 不变性 / hump≠ts_decay / reverse=2×成本且翻正不改 TO / fitness .125 地板 / 天花板代数） |
| `04_engineering.md` | §15 | 规则库消费点实测：`inject_rules` 不存在、`emit`/`when` 无人读，只有 `strategy` 型有常驻提示 |
| 同上 | §16 | 区域规则真相源在 DB（文件只是镜像）；`merge` 不保护 list；整值手转录静默改坏 7/8 条 + 修法（见本文件 §6.11） |
| `AGENTS.md` §5 第 0 条 | — | 同步上述写入口径（活文档权威源，非经验 KB，不触发机器规则义务） |

**机器层（规则库）**：

| 文件 | 新增 rule_id | type |
|---|---|---|
| 全局 `methodology_rules.json` | `prod_fresh_before_constraint_relaxation_v1` | strategy |
| 同上 | `submit_ready_status_is_local_queue_state_v1` | strategy |
| 同上 | `rank_shell_aggregator_swap_is_not_new_probe_v1` | strategy |
| 同上 | `ten_year_data_judged_by_yearly_longcount_v1` | strategy |
| **DB `ledger_kv` KOR/`methodology_rules`**（运行期真相源） | `kor_is_window_hard_pinned_v1` | strategy（区域专属，硬窗日期不外推） |
| `tracking/KOR/reference/methodology_rules.json`（镜像） | 同上 | 已回填为 DB 全量 9 条 |

全局 24 → **28** 条；KOR 区域 **DB 8 → 9** 条（文件镜像原为 1 条陈旧快照，现已同步为 9 条，见下）。
每条都带 `action.params.doc`（指向人读层，受 `test_rule_declared_docs_exist` 校验）与
`region_evidence`（指向本文件或 roadmap）。

**验证证据（全部实跑）**：`test_experience_kb_refs.py` + `test_methodology_rules_consistency.py` +
`test_operator_complexity_and_equiv_substitution.py` = **33 passed**；镜像回填后复跑前两个守护
= **18 passed**；`test_audit_fixes.py -k sync_skills` = **1 passed**；`sync_skills.py --check`
五安装位零漂移；`doc_path_refs.py` **exit 0 / 无新增死指针**（本文件尚未 git add，被列为
UNTRACKED 提示，属预期）。

**★ 功能级验证（不只是 JSON 合法）**：`RuleStore(tracking/KOR).load()` 实测
`global=28 / region=9 / merged=37`；`apply_rules(ctx,"strategy",{region:KOR,universe:TOP600})`
返回 **18 条**，本次新增的 **5 条全部命中并被打印**（4 全局 + 1 KOR）⇒ 确认它们会真的出现在
`build_wave.py:789` / `pipeline.py:1499` 的常驻提示里，不是「写了但永不生效」的死规则。

**⚠ 同期 3 条红不是本次引入的（已归属，别误修）**：`test_docs_consistency.py::test_last_verified_not_older_than_last_commit`
对 `wq-alpha-gate-push-op-min` / `wq-operator-playbook-by-gate` / `wq-wave-preflight-dispatch` 三个 skill 报红。
归属证据：三者最后一次内容提交都是 **`38b287e`（2026-10-31，并行会话的治理收尾提交，即本会话开始时的 HEAD）**，
而 frontmatter 仍是 `last_verified: 2026-10-30` ⇒ **HEAD 本身就红**，与本次改动无关（本次只动
toolkit config / `docs/experience/` / `AGENTS.md` / `tracking/KOR/`，这三个 skill 目录零改动）。
其中 `wq-alpha-gate-push-op-min` 还带着**另一会话的在途未提交件**（`SKILL.md`、`references/scan-protocol.md`
已改、`scripts/scan.py` 未跟踪）⇒ 按「不跨会话代改」纪律**不动它**，留给写入会话复核内容后自行 bump。
排除这 3 条后本次相关守护 **637 passed / 3 deselected**；`sync_skills.py --check` 五安装位零漂移 exit 0；
`doc_path_refs.py` exit 0、无新增死指针。

**★ 选 `type=strategy` 不是随意的**：实测只有 `strategy` 型会被
`build_wave.py:789` 与 `pipeline.py:1499` 的常驻提示循环打印 `action.message`；
`diagnosis` 型只在 `recommend_next_wave` 的四个特定 `action.op` 分支里被消费
（`gradient_dilute` / `warn_rnf_drop` / `dead_universe` / `classify_failure_nature`）。
本次五条都是**咨询性判据、无自动拦截**，故走 strategy 常驻提示，并在 `params.consumption`
里显式写明 `advisory_only`，避免后来者误以为它们会拦批。详见 `04_engineering.md` §15。

### 6.11 ★ 区域规则的真相源是 DB，不是文件；MCP 整值转录会静默改数据（本次踩到并修复）

**（1）只改文件 = 白改。** `RuleStore._use_db()`：战役目录路径含 `tracking` ⇒ **区域规则读
`ledger_kv` 的 `KOR/methodology_rules`**，文件只在「DB 为空」时作一次性迁移源
（`WQB_RULES_FILE_ONLY=1` 才强制走文件，那是测试隔离用）。`AGENTS.md` §3.5 早就写了「区域，存 DB」，
本次是**操作没跟上文档**：先把新规则写进 `tracking/KOR/reference/methodology_rules.json`，
运行期完全读不到。实测 DB 里已有 **8 条**（6 条 explore_contract + 1 diagnosis + 1 universe_lever），
而文件只有 **1 条**陈旧快照（同一条 explore_contract 在 DB 里已 `deprecated`、文件里还标 `active`，
`consumed_batches` 8 vs 10、`times_applied` 8 vs 10）⇒ **两边早已分叉，且分叉方向是文件落后**。

**（2）MCP 没有「规则专用」工具，也没有 JSON-path 补丁。** `mcp_list(keyword="rules")` 只返回
`get_competition_agreement`；`wqb_db_mcp.py` 里 `methodology` 零命中。唯一通道是
`get_ledger_key` / `upsert_ledger_key`（region=KOR, key=`methodology_rules`）。
⚠ **`mode="merge"` 救不了列表**：merge 只对 dict 递归，`rules` 是 list ⇒ **整列覆盖**。
只传 `{"rules":[新规则]}` 会把既有 8 条全部抹掉。必须传**完整 9 条**。

**（3）整值手转录 = 静默数据损坏（本次实测 7/8 条被改坏）。** 把 6KB payload 重新打一遍传进
`upsert_ledger_key` 后，逐条 canonical-JSON 比对发现 **8 条里有 7 条与写前不一致**：

| 损坏类型 | 实例 | 条数 | 危害 |
|---|---|---|---|
| **长十六进制串被截断** | `e1bf6fb2764de70ffb69182a043b380633c1d739`（40）→ `e1bf6fb2764de70ffb6918e4b7b739`（30） | 1 | 批次指纹失配，`expires_after_batches` 计数去重失效 |
| **float 被写成 int** | `confidence: 1.0` → `1`；`max_sharpe: 2.0` → `2` | 6 + 1 处 | JSON 类型漂移，任何按 `== 1.0` / 类型敏感的读方行为改变 |

**两条都不报错、`{"action":"updated"}` 照常返回** ⇒ 回执成功 ≠ 数据正确。

**（4）正确修法（已执行并验证）**：不要第二次手转录。从**会话 transcript 的写前工具结果**里
取回原始 payload 作权威基线（`logs/_tmp_*.py`：逐行 `json.loads` → 递归取 str → 命中特征哈希
再 `json.loads` 还原 dict），拼上「新规则从文件镜像读」，经**既定写入方**
`store.upsert_methodology_rules(region, data)`（= `RuleStore._save_region_db` 同一条路径）写回，
再 read-back 断言：① 8 条既有规则 canonical-JSON **逐字节等于写前**；② 59 个批次哈希**全为 40 字符**；
③ 坏哈希已消失、好哈希已恢复。**全部通过**。

**（5）顺手把文件镜像回填成 DB 全量 9 条**：`data/` 整体 gitignore ⇒ **DB 里的区域规则不受版本控制**，
文件是唯一的可回溯记录。让它继续躺在 1 条陈旧快照上，等于区域规则没有历史。回填后复跑守护 **18 passed**。

**可复用判据（下次照做）**：
- 改区域规则 → **先 `get_ledger_key` 看 DB 有没有值**；有 ⇒ 必须写 DB，文件只作镜像。
- 任何「整值覆盖」型 MCP 写入（`replace` / `merge` 带 list）→ **写后必须逐条 diff 写前快照**，
  别只看 `action=updated`。优先让脚本做 read-modify-write，**不要让模型重打一遍长 JSON**。
- 长哈希 / 浮点常量是手转录的两个高危面；比对要按 **canonical JSON（`sort_keys=True`）**，
  肉眼看不出来。

---

## 7. 四条可复用的「零配额收口」手法（本会话验证有效）

1. **机制反查**：把待投字段逐条映射到已判死的机制轴 ⇒ 映射得上就撤销后备，不回测（§4.3，other496）。
2. **族代表 prod + 直方图**：`[0.7,0.8)` n≥1 ⇒ 一次平台读判整族（§2.5，省掉逐条 prod）。
3. **抽样 + TO 签名聚类**：关整片本地队列态（§2.6，4 次读判 19 行）。
4. **字段级判死**：拉全字段（**必须 `filter_sharpe=false`**，否则会隐藏低夏普的对侧腿）后，
   若全部字段都是**事件元数据 / 标志位 / 字符串 / 证券主表**，则构不出多空数值信号 ⇒ **不派探针**。
   实证：`other78`（11 字段全是 cancelledflag / estimatedtimeflag / fiscalyear / `sourcetypename`**字符串**，
   aCount 70 全落在标志位上 = 别人把「事件日存在性」当哑变量挖过的痕迹，不是可复用机制）；
   `other323`（证券主表）同型。出处 roadmap §7.1。

> 共同前提：**手法 1/3/4 完全零配额、零仿真、零 prod**；手法 2 用 1 次 prod。
> 在「配额贵、prod 单槽被抢」的约束下，它们比再开一波的价值高得多。
> ⚠ 但**字段级判死只适用于「构不出信号」**，不适用于「看起来弱」——
> 后者仍须实测（`analyst_factor_signals` 59 字段里有效仅约 2 个，名字自解释 ≠ 本区可用）。

---

## 8. 待用户裁决（本会话结束时未变，agent 不代决）

| # | 事项 | 为什么不能自主做 |
|---|---|---|
| 1 | 提交 `LLZ6wZO2` | 提交不可逆，须用户明确确认 + `confirm_submit=True`；且 FUNDAMENTAL 3/3 已满，**不点新塔** |
| 2 | risk59 约束 4 放宽到 **9 年**（2015–2023） | 2014 空缺是数据起点事实，**任何表达式杠杆都造不出 2014**；移窗已被平台否决（§1.1） |
| 3 | 批量 `seal_dead_end` | 取证闸 fail-closed，需 `forum_recon` 可靠「无解」证据；`force_seal=True` / `require_forum_recon=False` **须人工确认** |
| 4 | sentiment 禁令裁决 | 属用户约束解释范围 |
| 5 | 授权平台新数据集 | 现有面已全扫（15 category / 185 集普查，roadmap §5.78） |
| 6 | 60 颗目标的路径 A–D | 现有攻击面结构性不可达（§5），须用户选换区 / 换形态 / 降目标 / 授权新数据 |

---

## 9. 一句话总结

> 本会话 70 波、125 条候选，只产出 **1 颗可交付**（`LLZ6wZO2`，且塔已满）；
> 真正的产出是**把「还能挖」的幻觉逐条关掉**——
> 3 颗「指标全闸纯格 ATOM」死在 prod（.8377 / .8395 / .8711）、
> 19 行「本地 prod clean」死在族级新鲜读数（.81–.935）、
> 1 个「首选后备」死在零配额机制反查、
> 组合腿路线死在实测 ρ=0.1978 给出的代数上界 1.292。
> **下一步的价值不在再开一波，而在用户裁决 §8。**