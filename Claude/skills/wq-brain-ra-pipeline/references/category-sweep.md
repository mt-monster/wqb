# 步 1b · 类别普查（category_sweep + category_probe）

> 「指定 region → 遍历所有 category → 挖字段 → 发现苗子就深挖」的实现细则。
> 建立在2026-10-06 DEU 193 集 + 全库 13 区回测史的实测之上；所有数字可复算。

## 0. 为什么不用既有的三个工具直接实现

落地前先review 了三个既有工具，结论是**都不能直接承担「遍历 + 苗子」**：

| 工具 | 层级 | 为什么不用它当主入口 |
|---|---|---|
| `category_field_triage.py` | 数据集级**判死** | ★判据与真实产出**矛盾**：DEU `model28` 甜点=0 却出 12 条 RA-clean；`predictive_starmine` 被「族连坐」判死却出 **27 条（全区最高）**。存活 22 集里只有 **4 集**真有产出（18%）。另有 `shortinterest3`（sweet=11/荒地 0%/cov 0.711 各项合格）因 `--top 60` 全局截断被埋。 |
| `score_datasets.py`（步 2 S0） | 数据集级**排名** | 入口是数据集不是 category；category 只是 `category_weight` 排序维度，不驱动遍历。 |
| `field_signal_mine.py` | 字段级历史先验 | 方法论可复用（从表达式文本反挖字段 |sharpe|），但输出是字段榜、不是类别普查。 |

⇒ `category_sweep.py` **只借鉴 `field_signal_mine` 的字段先验方法论**，判级与
`category_field_triage` 完全不同（见§2铁律）。`category_field_triage` 仍可作为
「族连坐/拥挤」的**辅助提示**查，但不是主入口。

## 1. 两层结构

```
步 1b  L0  category_sweep.py     零回测零API   →  results/cat_sweep_<R>.json
       │   按 category 全遍历（含 NULL 兜底桶）
       │   每类出：字段数 / 荒地率 / 历史达标数 / 种子字段池 / 判定
       ↓
       L1  category_probe.py       零配额       →  results/probe_<R>.txt
           按骨架×字段生成机制多样探针（一条探针 = 一个新机制）
           派发 QUICK 仿真 → 收割 → --classify 判苗头（宽召回）
       ↓
       L2  现有九步S1→S9（RA 全清在 这一层 才筛）
```

**L1/L2 判据分离是本设计的关键**：探针只要「这个类有没有活的东西」（宽召回），
严格闸门留到深挖。若 L1 就用 RA-clean 严筛，ASI 有 314 条 `sharpe>=1.58` 但只13 条 <!-- lint:const-ok -->  <!-- 1.58/1.30 = L1 探针自定实测判据，非 config 门槛 -->
RA-clean（通过率 4%），整类会被误杀。

## 2. 三条铁律（违反即失效）

### 铁律 ① `alpha_count` 只做拥挤排除闸，不做入选判据

它衡量的是**拥挤度 / prod 墙风险**，不是信号强度。实测：

| 证据 | 数字 |
|---|---|
| DEU `model28` | `alpha_count∈[10,50]` 的甜点数 **0**，却产出 **12 条** RA-clean 高 S |
| DEU 字段分布 | 22494 字段中 **85% 是 `alpha_count=0` 荒地**，甜点仅 **301** 个 |
| 全库「次强」条 | `1.30<=sharpe<1.58` 共 **851 条**，严格口径（>=1.58 + RA 清）会全扔 |
| 拥挤闸有效性 | `alpha_count>1000` 判拥挤与 prod 墙实测吻合 → **这条保留** |

⇒ 只保留 `--crowd-ac`（默认 1000）作**排除闸**（命中不删、排末位）。

### 铁律 ② 必须有 NULL 兜底桶

`datasets` 表全库 **184 行 `category IS NULL`**。但要分两种情形（`category_sweep`
自动区分，判定值 `已枯(归他类)`）：

1. **平台真数据集漏分类** → 真机会，必须扫。
2. **本地组合/合成集**（DEU 的 `mix_2leg` / `mix_2leg_resid` / `grtransform` /
   `lean_le89` / `model25_model216` / `_unknown`）→ `datasets` 行存在但
   `fields` 表**零行**、`field_count` 为 NULL，字段本就归属别的具名类。
   ⇒ 判「已枯(归他类)」，**不占探针位**（否则白跑一个位）。

### 铁律 ③ 族连坐只降权不判死

假阳性代价远高于漏检代价：`predictive_starmine` 与被判死的 `model26` 同族
（预测类分析师数据），连坐判死 → **封掉 27 条已产出的alpha（DEU 全区最高）**。
⇒ `category_sweep` 只给种子打 `family_risk` 标签并**排到末位**，不剔除。

## 3. 探针条数：为什么「8 条够」但「机制必须多样」

历史命中率（RA-clean 高 S ÷ 已回测，全库13 区实测）：

| 区 | 命中率 | 区 | 命中率 | 区 | 命中率 |
|---|---|---|---|---|---|
| ASI | **1.6%** | KOR | 6.8% | DEU | 10.4% |
| USA | **2.2%** | DEU | 10.4% | HKG | 10.4% |
| EUR | 3.1% | HKG | 10.4% | GLB | 12.9% |
| GBR | 3.7% | GLB | 12.9% | IND | 14.9% |
| | | | | MEA | 19.9% |

**中位约 7%。** 8 条的检出概率 `P(>=1)=1-(1-p)^8`：

| 条数 | DEU | GBR | EUR | USA | ASI | IND | MEA |
|---|---|---|---|---|---|---|---|
| 8 | 58% | 26% | 22% | 16% | 12% | 72% | 83% |
| 24 | 93% | 60% | 53% | 41% | 32% | 98% | 100% |

⇒ **8 条会丢掉54% 的活类别**（ASI/USA/EUR 几乎等于没探）。
反向：要 `P(>=1)>=90%` 需 —— p=10% → 22 条；p=5% → 45 条；p=2% → **114 条**。


<!-- 下列 1.58 / 1.30 不是抄 config 门槛，而是 L1 探针**实测判据**：1.58 = 与提交线同口径的IS 强信号下限，1.30 = 「次强」召回线（实测各区命中率提升 1.4~2.2倍）。两者是本机制的自定参数，可按区调。 -->

| 数据集 | 达标条 | 独立表达式 | 去重比 |
|---|---|---|---|
| DEU 合计 | 164 | **73** | 2.2x |
| `grtransform` | 10 | **1** | **10x** |
| `model216` | 8 | 1 | 8x |
| `other455` | 14 | 2 | 7x |
| `model28` | 12 | 2 | 6x |

⇒ 8 条里若掺设置变体，**独立机制样本可能只剩 3 个**，统计上无意义。
**真正的杠杆是两个**（已同时落地）：

1. **判据放宽**：L1 用 `sharpe>=1.58` **或** `2Y>=1.58` **或** `sharpe>=1.30`。 <!-- lint:const-ok -->  <!-- 1.58/1.30 = L1 探针自定实测判据，非 config 门槛 -->
   各区命中率提升 1.4~2.2 倍（DEU 10.4%→19.8%、IND 14.9%→21.3%、
   KOR 6.8%→17.5%、GBR 3.7%→9.3%、USA 2.2%→7.8%）。
2. **机制多样**：一条探针 = 一个新骨架（`skeleton_key` 去重），字段按**数据集**
   均衡轮转（避免退化成单数据集探针）。

**分区配额**：命中率 ≥10% 的区（DEU/GLB/IND/MEA/HKG）`--n 8` 够；
<5% 的区（USA/EUR/GBR/ASI）**`--n 20~24`**，或先跑本地三闸预筛
（`two_year_sharpe>=1.58 AND sub_universe_sharpe>=1.0`——实测可砍 78% 候选）。 <!-- lint:const-ok -->  <!-- 1.58/1.30 = L1 探针自定实测判据，非 config 门槛 -->

## 4. 探针骨架库

`PROBE_SKELETONS`（`category_probe.py`）10 个**几何互异**的骨架，刻意不含
两腿相加（禁混信号）：

| 骨架 | 表达式 | 探的机制 |
|---|---|---|
| `xs_rank` | `rank(f)` | 截面相对位置 |
| `ts_zscore` / `ts_zscore_s` | `ts_zscore(f, 252)` / `(f, 66)` | 长/短窗时序标准化 |
| `ts_delta` | `ts_delta(f, 22/66)` | 变化量 |
| `ts_pctchg` | `ts_delta(f,22) / ts_delay(f,22)` | 变化率 |
| `ts_rank_w` | `ts_rank(f, 1260)` | 窗口内分位 |
| `decay` | `ts_decay_linear(f, 22)` | 线性衰减加权 |
| `quantile` | `quantile(f)` | 稳健截面标准化 |
| `winsor` | `winsorize(f, 4)` | 极值裁剪 |
| `zscore_xs` | `zscore(f)` | 截面 z |

**合规**：无任何 `add`/`multiply` 两腿；每字段包一层 `rank` 允许（探针是测量仪器，
不是提交候选池——与「每字段套rank」禁令的适用范围一致，见 `field_signal_mine` 同款声明）。

## 4.5 L2 深挖队列：registry 闭环 + 产出率配额

L2 不需要新引擎，但**需要两个代码缺口**，两者都已补：

### 缺口① 「已判死」不参与遍历 —— 闭环断裂（实测 11 个已死集被重推）

初版 `category_sweep` **完全不读 `registry_empirical`**，实测 DEU/KOR 共 **11 个**已在
registry 判死的数据集仍被推为可探候选：

| 区 | 类| 已死却被重推 |
|---|---|---|
| DEU | SENTIMENT ★苗头 | `sentiment33`, `sentiment7`（后者 dead_end 写明「6 波 48 探针 / 天花板 0.71」） |
| DEU | RISK ★苗头 | `risk60` |
| DEU | INSTITUTIONS 待探 | `fund_holdings_panel` |
| KOR | FUNDAMENTAL / ANALYST / RISK / OTHER / SENTIMENT / INSIDERS | `other466`, `analyst14`, `risk88`, `other496`, `other553`, `insiders5` |

⇒ 现在 `load_registry_dead()` 读 `dead_end` 层，从种子池剔除，类全死则判 **「已枯(registry)」**。
DEU 实测：**强排除 49 个数据集 → 剔除 3746 个字段**；EARNINGS/MACRO/OPTION/… 不再占探针位。

**★ 两个必须知道的提取坑（都是实测踩出来的）**：

1. **数据集名常只写在 `family` 文本里**，不在结构化键里。实测
   `DEU-PATTERN_SCORES-PROBE-DEAD-20261002` 的 payload 键只有
   `id/family/reason/rule/...`，`family="pattern_scores 图表形态相似度"`
   ⇒ 结构化键一个都没有。**必须**再走「已知数据集名全值子串匹配」。
2. **子串匹配必须跳过说明性键**。`DEU-EMPTY-COVERAGE-S0-PICKS-20260919` 的
   `control_group` 里写着「shortinterest3 字段级 coverage 0.63-0.98（对照组）」——
   扫 payload 全文会把**对照组**误判成死集（它实际列的是 option1/pv20/fundamental17）。
   ⇒ 显式跳过 `control_group/method/risk/note/reason/rule/evidence/…`。

**★★ 只有带 `rule` 的 dead_end 才做强排除**（与 registry 契约一致：dead_end 必须带
「下次怎么办」）。实测 `DEU-SI3-CW-STRUCTURAL`（`shortinterest3` CW 墙）的 `rule`
**是空的** ——记录了现象但没给行动指引。若把它当硬排除，会把 DEU 产出最好的集之一
（`shortinterest3` **25 条 RA-clean、25/25 全区最高**）判成「已枯(registry)」。
⇒ 无 `rule` 的条目**降级为提示**（排末位 + `weak` 标签）。DEU 实测：强排除 49 个、
弱提示 23 个，`SHORTINTEREST` 正确保留为 `★苗头`。

复查已判死集用 `--keep-dead`（全部保留、排在末位）。

### 缺口② 深挖配额按产出率分配，不均分

实测各类产出率相差 25 倍（MEA 19.9% vs ASI 1.6%），均分会把配额压在无产出的类上。
`allocate_quota(rows, budget, mode)` 两种模式：

- `--quota-mode yield`（默认）：权重 = `历史达标数`（0 产出的给保底权重 1，否则处女地
  永远拿不到探针）+ `0.5 × 有历史强信号字段`；按比例分配，每类保底 1 条，总额不超预算。
- `--quota-mode equal`：均分，**仅作对照**（用来量化 yield 模式的价值）。

DEU 实测（预算 64、11 个可探类）：`MODEL=28, SHORTINTEREST=11, OTHER=9,
SENTIMENT=5, RISK=4, FUNDAMENTAL=1, INSIDERS=1, ANALYST=1, NEWS=1, PV=1,
INSTITUTIONS=1`。均分时每类 5.8 条——**MODEL 少拿 22 条、RISK 多拿 2 条**。

L1/L2 消费配额：`category_probe.py --use-quota` 读 `sweep["quota"]` 逐类生成，
不再统一 `--n`。

**⚠ 骨架耗尽问题**：配额高时（如 MODEL=28）10 个骨架出尽就 `break`，实际只出 11 条、
**浪费 17 条预算**。已修：骨架用尽后按（骨架 × 窗口）展开新变体
（`skeleton_key` 含 `<N>`，窗口不同 ⇒ key 不同 ⇒ 真的换了机制参数）。
骨架表也补了窗口候选（`ts_zscore` 252/66/504、`ts_delta` 22/66/252 等）
并新增 `ts_mean`、`ts_std_norm`（双占位符，`{w2}` = 4×`{w}`）。

### L2 收尾：全灭类别写 registry

L1 `--classify` 判出「已枯」的类别，**写 `registry_empirical` 的 `dead_end` 层**
（`seal_dead_end` / `campaign.py registry add-dead-end`，必填 `rule`），
下轮 L0 自动把它排除 ⇒ 闭环。**这是 `rule` 必须写的原因**——
没有 `rule` 的条目下轮只会降级为提示，白写。

## 5. 实测验证（2026-10-06）

L0 · DEU 17 类 / 180 集 / 22493 字段 → 种子 86，11 个可探类：

| category | 集 | 字段 | 荒地 | 历史达标 | 判定 |
|---|---|---|---|---|---|
| MODEL | 50 | 8172 | 87% | 63 | ★苗头 |
| SHORTINTEREST | 1 | 25 | **0%** | 25 | ★苗头 |
| OTHER | 42 | 3921 | 86% | 21 | ★苗头 |
| SENTIMENT | 3 | 276 | 91% | 12 | ★苗头 |
| RISK | 5 | 52 | 38% | 11 | ★苗头 |
| FUNDAMENTAL | 13 | 2146 | 82% | 3 | ★苗头 |
| INSIDERS | 2 | 42 | 45% | 1 | ★苗头 |
| ANALYST / INSTITUTIONS / NEWS / PV | 19/5/17/16 | — | 85/53/77/87% | 0 | 待探 |
| (未分类) | 0 | 0 | — | 19 | **已枯(归他类)** |

**关键验证**：被旧 triage 排除的 8 个历史赢家，**4 个经种子池重新捕获**——
`shortinterest3`（`mean_loan_rate_main` hist_hit=18 / max|S|=2.02）、
`other455`、`risk60`、`sentiment7`。

L1 · DEU 11 类 × 8 条 = **88 条探针 / 8 个不同骨架**，每类 `diversity=1.0`；
探针字段 100% 存在于本地 DEU catalog（22492 个字段）。

**平台实测**：`validate_expressions`（DEU/TOP500/D1）→ `valid: true`、
`unknown_fields: []`（7 字段全通过）；`operator_audit` → `safe: true`、
`violations: []`。

## 6. 常见坑

| 现象 | 根因 | 处置 |
|---|---|---|
| 某类 `0 集 0 字段` 但历史达标 > 0 | 本地组合集桶（铁律②情形 2） | 工具已判「已枯(归他类)」；若确认是平台真集漏分类，先补 `datasets.category` |
| 类明明有产出却被判「已枯(registry)」 | 该类数据集的 dead_end **无 `rule`**却仍被强排除 | **已修**：只有带 `rule` 的才强排除，无 `rule` 降级为提示（实测 `shortinterest3` 25 条 RA-clean 曾被误杀）。用 `--keep-dead` 复查 |
| 每类只出 4 条而非 `n` | `skeleton_key` 把不同算子抽成同一 key | **已修**：改为「参数位标识符→`<F>`，保留算子名」的深度扫描归一化（旧版把 `ts_zscore(f,22)` 与 `ts_delta(f,22)` 抽成同一个，10 骨架塌成 4） |
| 探针集中在单数据集 | 该类种子池本就来自字段最多的集 | 工具会打`⚠ 数据集集中` 警告；结论只代表该集；要覆盖多集先扩L0 `top` |
| 探针报幽灵算子 | 模板用了平台未验证算子 | `operator_audit(expressions=[...])` → 改 `PROBE_SKELETONS` |
| QUICK 结果不可提交 | QUICK 缺 correlation / theme 检查 | 纪律同主流程：QUICK 仅探针，**必须 FULL 复测**才进提交链 |

## 7. 边界

- **点塔状态不在此判定**：`datasets.category` ≠ 金字塔塔归属。开波前仍须 `get_pyramid_alphas`
  （同步主流程步 2「已点亮塔不进白名单」规则）。
- **产物是字段池，不是 ideas**：禁止直接注入 GEM；机制仍须走L4 形态构建五步法。
- **本地 catalog 是快照**：存在性只信平台 `get_datafields`；类型/拥挤度可本地粗筛。
- **`category` 口径**：只信平台 `get_datasets` 的 `category` 字段，勿按内容语义推断
  （如 `model50` 内容是下行风险评估打分，但平台分类为 `model`）。
- **本工具零配额**：只读库（`readonly=True`），不派发仿真、不写台账。要落账走步 9。