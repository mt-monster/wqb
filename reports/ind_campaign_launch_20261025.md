# IND 开波记录 — 2026-10-25

> 依据 `docs/reference/ind_campaign_runbook_20261025.md`。
> 用户约束：① 找到有潜力的数据集；② 对近闸候选按 skill SOP 定向挖掘；③ **并发上限 2**；④ **覆盖率可动态调整，但必须十年都有数据**。

---

## 一、开波前 5 项检查

| # | 检查 | 结果 | 处置 |
|---|---|---|---|
| 1 | IND `dataset_profile` | ❌ **0 条**（应为 ~185） | 已跑 `tools/load_field_profiles_to_db.py --region IND` ⇒ **144 集 / 14 334 字段** |
| 2 | IND 字段库 | ✅ 14 334 | — |
| 3 | `bad_tokens.json` | ⚠ 1 条 `earnings_volatility_trend` | 非结构算子，不阻断 |
| 4 | IND 断点 | ✅ 不存在（全新） | — |
| 5 | 并发 | ✅ `--max-inflight 2` | 已在日志确认 `[gate] 同时在飞作业上限 = 2` |

---

## 二、⚠ 手册未覆盖：5 处「假区域化」写死 EUR，导致首轮全废

手册称「代码已区域参数化，IND 开波不需改代码」——**实测不成立**。首轮 6 个集全部被判 `SKIPPED_TOO_FEW_FIELDS`，日志写：

```
[plat] analyst_earnings_ibes: 过滤幽灵字段 26 个（本地 26 → 平台认证 0）
```

**这不是数据集没字段，是 universe 参数错。** 已修 5 处：

| # | 文件 | 问题 | 后果 |
|---|---|---|---|
| 1 | `campaign_semantics.py:78` | `select_fields` 写死 `r.name='EUR'` | 选字段查 EUR 库 |
| 2 | `campaign_semantics.py:96` | `all_datasets` 写死 `region='EUR'` | **拿 EUR 集名跑 IND 库，全错** |
| 3 | `campaign_semantics.py:441` | `load_s1_preprocessing` 默认 `region="EUR"` | S1 台账读错区 |
| 4 | `wqb_campaign/fields.py:50` | `platform_fields(universe="TOPCS1600")` | **IND 下平台认证 0 ⇒ 6 集全 SKIP** |
| 5 | `campaign_supervisor.py` | `CKPT/RESULTS/DIGEST/TOTAL=169` 全写死 | 显示 `done=107/169`、空转熔断读 EUR 结果、跑完无限重启 |

**修复验证**：`platform_fields` 改为 `REGION_SETTINGS["universe"]`（IND=TOP500）后，
`analyst_earnings_ibes / model238 / analyst_revision_horizons` 平台字段数恢复为 **28 / 44 / 1026**，与本地画像一致。

**判据**：以后看到 `本地 N → 平台认证 0`，先查 region/universe，不要据此判数据集死刑。

---

## 三、用户两条自定义要求的落地

### 3.1 覆盖率可动态调整 ⇒ 新增 `--min-cov`
`pipeline.py` 原有两个并列字面量：`priority_min_cov`（只对 `--priority-cats` 生效）与 `eff_min = ... else 0.6`。
只调前者对普通集无效（正是手册 §4.2 的坑）。新增 `--min-cov` 覆盖**两处**。

**IND 覆盖率分布**（130 个 n_fields≥3 的集）：

| 门槛 | 集数 |
|---:|---:|
| ≥0.8 | 59 |
| ≥0.7 | 86 |
| ≥0.6 | 103 |
| **≥0.5** | **108** |
| ≥0.4 | 117 |

⇒ 本次设 **0.5**（0.6→0.5 只多纳 5 个集，说明门槛不是瓶颈；时间才是）。

### 3.2 十年都要有数据 ⇒ 新增 `--require-ten-years`
verdict 阶段新增硬否决：`year_profile.n_years < 10` 或 `first_year > start_year` ⇒ 改判 **`INSUFFICIENT_HISTORY`**，并打印 `[10y] ✗`。

⚠ `year_profile` 是仿真后从逐年统计算出的 ⇒ **只能做候选级否决，无法预筛数据集**。
已知会被此闸杀掉：`quant_factor_lib`（`first_year=2020`、`n_years=4`、`late_start=True`）。

---

## 四、第 1 步：选有潜力的数据集

**IND 目标池 = 130 个数据集**。按 skill 的「经济锚 > 覆盖率 > 拥挤度」筛选（**禁止按 aCnt 排序**）：

| 数据集 | 类别 | 字段 | cov | 入选理由 |
|---|---|---:|---:|---|
| `analyst_revision_horizons` | MODEL | 1026 | 0.782 | 分析师修订 = IND **唯一已验证机制**（PEAD 锚）|
| `predictive_starmine` | MODEL | 638 | 0.925 | StarMine 预期；历史曾产出 prod 0.5437 |
| `analyst_earnings_ibes` | MODEL | 28 | 0.996 | IBES 预期，覆盖近满 |
| `model238` | MODEL | 44 | 0.983 | MODEL 是本区最强类别（168 回测/25 RA 全过）|
| `model28` | MODEL | 114 | 0.970 | 同上，字段多、暴露 4 种 |
| `other128` | OTHER | 14 | 0.742 | vs=5.0，高管绩效因子（新维度）|

**主动排除**：

| 数据集 | 原因 |
|---|---|
| `pv70` | 关系图近静态，画像接近死 |
| `quant_factor_lib` | `n_years=4`（2020 起）⇒ 会被十年闸杀 |
| `news54` / `news29` / `news38` / `news_sentiment_nlp` / `other567` | 新闻情绪属本区「8 类无收益锚」，实测 0 达标 |

---

## 五、第 2 步：近闸候选的定向挖掘（待战役产出）

当前账上唯一的近闸资产是 option1 的 **`d5K6GQWJ`**（S 1.37 / F 0.97 / rob 1.37 / 2Y 1.12）。
它的问题已定性：2Y 地板是硬的（官方 ladder 要求 2Y ≥ 1.59），13 条杠杆 + 6 类假设全部否证 ⇒ **不是参数问题**。
⇒ 该候选不再投入，等本轮战役产出**新的**近闸候选后，再按 skill SOP 做定向挖掘（归因 → 靶点 → 单变量对照）。

---

## 六、启动命令与当前状态

```bash
WQB_CAMPAIGN_REGION=IND python tools/campaign_supervisor.py \
  --datasets analyst_earnings_ibes,model238,analyst_revision_horizons,predictive_starmine,model28,other128 \
  --min-cov 0.5 --require-ten-years --max-inflight 2 \
  --stall-sec 900 --check-sec 60 --zero-alpha-stop 3
```

| 项 | 状态 |
|---|---|
| 托管器 | ✅ 已区域化（`done=0/6`）|
| 并发 | ✅ 2（日志确认）|
| 当前数据集 | `model28`（MODEL，114 字段，cov 0.97）|
| 已派发 | **37 条 / 8 批**（10 族未覆盖 ⇒ 走全交叉）|
| 断点 | `results/full_template_campaign_checkpoint_IND.json` |
| digest | `results/campaign_digest_IND.md` |

预计 6 个集 × 约 60 min ≈ **6 小时**（并发 2）。

---

## 七、2026-10-25 15:15 改向：切到「未点亮塔」

按用户指示，战役从已点亮的 MODEL/ANALYST 切换到 **8 个未点亮塔**。

### 7.1 未亮类别盘点（IND，`n_fields>=3`）

| 类别 | 集数 | 塔位价值 |
|---|---:|---|
| **FUNDAMENTAL** | 10 | ★★★ **2/3，差 1 颗就点亮，multiplier 1.2** ⇒ 最高优先 |
| EARNINGS | 3 | ★★★ `earnings3` 有画像 ALIVE 字段（`ern3_pre_interval` S 4.49）|
| INSTITUTIONS | 1 | ★★ 残差族已证 8/8 RA 全过（非 ATOM）|
| SENTIMENT | 4 | ★ 本区无收益锚（实测 0 达标）|
| OPTION | 2 | ✗ `option1` 已证 S 1.37 天花板、2Y 硬地板 |
| INSIDERS | 1 | ✗ 画像 DEAD_STATIC |
| SHORTINTEREST | 1 | ✗ 恒常字段、零信号 |
| IMBALANCE | 0 | 无 `n_fields>=3` 的集 |

合计 **22 集**，其中 cov≥0.5 的 **15 集**。

### 7.2 派发清单：14 集（排除两个已证死集）

**纳入**：`fundamental17/23/94/86/44/90/1/93`（8）｜`earnings3`（1）｜`institutions6`（1）｜`sentiment21` / `news_sentiment_transfer` / `sentiment23` / `sentiment26`（4）

**排除**（省约 2 小时仿真）：
- `option1` —— 2Y 硬地板，13 条杠杆 + 6 类假设全部否证
- `shortinterest5` —— 3 字段恒常，零信号

### 7.3 启动命令

```bash
WQB_CAMPAIGN_REGION=IND python tools/campaign_supervisor.py \
  --datasets fundamental17,fundamental23,fundamental94,fundamental86,fundamental44,fundamental90,fundamental1,fundamental93,earnings3,institutions6,sentiment21,news_sentiment_transfer,sentiment23,sentiment26 \
  --only-cats INSTITUTIONS,SHORTINTEREST,INSIDERS,FUNDAMENTAL,OPTION,SENTIMENT,EARNINGS,IMBALANCE \
  --min-cov 0.5 --require-ten-years --max-inflight 2 \
  --stall-sec 900 --check-sec 60 --zero-alpha-stop 3
```

托管器新增 `--only-cats` 透传，并按类目从 `dataset_profile` 自动计算 TOTAL（本次 14）。

### 7.4 状态

| 项 | 值 |
|---|---|
| 并发 | ✅ `[gate] 同时在飞作业上限 = 2` |
| 目标 | 14 集（`done=0/14`）|
| 首个集 | `sentiment26`（SENTIMENT，cov 0.53）已派 **30 条** |
| 幽灵字段 | 6 个（本地 17 → 平台 11），属正常范围 |

### 7.5 ⚠ 一次并发编辑事故

拉起时 `argparse` 报 `--only-cats` 冲突——该文件正被**另一个会话/进程同时编辑**（我加了一份定义，对方也加了一份），数分钟后被重整、冲突消失。

**教训**：改 `tools/` 下被多会话共用的脚本前，先确认无其他 agent 在写；改完先跑一次 `--once` 验证参数解析，再拉起长任务。
