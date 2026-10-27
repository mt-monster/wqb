# IND 开波手册（全数据集 × 全模板族流水线）

> 2026-10-25 由 EUR 战役（169 集 / 41 个真开采 / 15 颗近交付）总结而来。
> 代码已**区域参数化**，IND 开波不需要改任何代码，只需设环境变量。
> 配套模块：`Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/wqb_campaign/`（13 模块，编排入口 `pipeline_ind.py`）；
> 托管器：`.../ind_campaign/ind_runner.py`。
>
> **2026-10-25 迁移**：引擎与托管器已从 `tools/` 移入 IND skill 自带（`scripts/ind_campaign/`），
> `tools/campaign_supervisor.py` / `tools/wqb_campaign/` 均已不存在；旧入口归档在
> `attic/ind_legacy_launchers_20261025/`。区域硬钉在脚本内（`os.environ["WQB_CAMPAIGN_REGION"]="IND"`），
> 不再依赖外部环境变量。

---

## 0 一句话启动

```bash
cd <仓库根>

# 推荐：唯一启动器（已含 7 类别 + 十年硬要求 + 并发 2 + region 硬钉）
Claude\skills\wq-brain-ra-ind\scripts\run_ind.cmd

# 等价直接调用（<venv> = world-quant-brain-mcp/.venv/Scripts/python.exe）
<venv> -X utf8 Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/ind_runner.py ^
  --only-cats EARNINGS,IMBALANCE,INSIDERS,MACRO,OPTION,SENTIMENT,SHORTINTEREST ^
  --min-cov 0.35 --require-ten-years ^
  --max-inflight 2 --stall-sec 900 --check-sec 60 --zero-alpha-stop 3
```

⚠ **ATOM 优先（2026-10-26 用户口径）**：IND 一律按 §4.3.2 执行「ATOM 先、残差/组腿后」。
需要**纯 ATOM 波次**（不派发含 PV `returns` 的残差族）时，启动前加环境变量：

```powershell
$env:WQB_ATOM_ONLY=1   # 只对本进程生效；已在跑的波次不热加载（长驻进程模块级常量）
```

不设 = 保留残差族（旧行为）。第三波（2026-10-26 00:37 启动）未带此开关，在飞不中途改。

`ind_runner.py` 已在模块级硬钉 `WQB_CAMPAIGN_REGION=IND`（**在 `import wqb_campaign` 之前**），
它自动完成下列隔离（已实测）：
| 项 | EUR（默认） | IND |
|---|---|---|
| 断点 | `results/full_template_campaign_checkpoint.json` | `..._checkpoint_IND.json` |
| 结果 | `..._results.json` | `..._results_IND.json` |
| digest | `results/campaign_digest.md` | `campaign_digest_IND.md` |
| 点塔缓存 | `cache/eur_lit_counts.json` | `cache/ind_lit_counts.json` |
| universe | TOPCS1600 | **TOP500** |
| neutralization | FAST | **STATISTICAL** |
| nanHandling | ON | **OFF** |
| maxTrade | ON | **OFF** |

⚠ **断点必须按区域隔离**，否则 IND 会与 EUR 共用 `done` 列表直接互相覆盖。已内置。

---

## 0.1 ⚠ 2026-10-25 更正：「不需改代码」不成立，已修 5 处写死 EUR

首次真跑 IND 时暴露，**全部已修**，但下次开别的区（USA/HKG/JPN…）要按同一份清单复核：

> 下表路径与行号是**迁移前**（`tools/` 时代，2026-10-25 上午）的位置，保留作历史定位；
> 同名模块现位于 `scripts/ind_campaign/campaign_semantics.py` 与
> `scripts/ind_campaign/wqb_campaign/fields.py`，行号已随拆包变化，**要按符号名搜、不要按行号跳**。

| # | 文件:行 | 问题 | 症状 |
|---|---|---|---|
| 1 | `tools/campaign_semantics.py:78` | `select_fields` 查询写死 `r.name='EUR'` | 选字段查到 EUR 库 |
| 2 | `tools/campaign_semantics.py:96` | `all_datasets` 写死 `dataset_profile WHERE region='EUR'` | **拿 EUR 的集名去跑 IND 库，全错** |
| 3 | `tools/campaign_semantics.py:441` | `load_s1_preprocessing(region="EUR")` 默认值 | S1 预处理台账读错区 |
| 4 | `tools/wqb_campaign/fields.py:50` | `platform_fields(universe="TOPCS1600")` 写死 EUR 宇宙 | **IND 下平台查不到字段 ⇒ 整集被误判「幽灵字段」（本地 N → 平台认证 0）⇒ 全判 SKIPPED_TOO_FEW_FIELDS** |
| 5 | `tools/campaign_supervisor.py` | `CKPT` / `RESULTS` / `DIGEST` / `TOTAL=169` 写死 EUR | 托管器显示 `done=107/169`、空转熔断读 EUR 结果会误熔断、子进程跑完无限重启空跑 |

**判据速查**：日志出现 `[plat] <ds>: 过滤幽灵字段 N 个（本地 N → 平台认证 0）` ⇒ **不是数据集没字段，是 universe/region 参数错了**，别据此判集死。

### 新增的两个 campaign 参数（配合本手册使用）

| 参数 | 作用 |
|---|---|
| `--min-cov 0.5` | **全局**覆盖率门槛，覆盖 `pipeline.py` 里 `priority_min_cov` 与 `eff_min ... else 0.6` **两处字面量**（只调 `--priority-min-cov` 对非优先类别无效，就是 §4.2 那个坑） |
| `--require-ten-years` | 候选必须 **10 年都有持仓**（`year_profile.n_years>=10` 且 `first_year<=start_year`），否则改判新判定 `INSUFFICIENT_HISTORY`。⚠ `year_profile` 在仿真后才算 ⇒ 只能做**候选级否决**，不能预筛数据集 |

托管器 `ind_runner.py`（原 `campaign_supervisor.py`）已支持透传：`--datasets` / `--only-cats` / `--min-cov` / `--require-ten-years`（更早的版本只传 `--max-inflight`）。

### 开波前必查：IND 画像要先建

`dataset_profile` 的 IND 行不是自带的。首次开波前：

```bash
python tools/load_field_profiles_to_db.py --region IND    # 144 集 / 14 334 字段
```

否则 §1 检查 #1 直接为 0，`all_datasets` 返回空池。

---

## 1 开波前 5 项检查（缺一项就别开）

| # | 检查 | 命令 / 判据 |
|---|---|---|
| 1 | IND 数据集画像已入库 | `SELECT count(*) FROM dataset_profile WHERE region='IND'`，应为 ~185 |
| 2 | 字段库有 IND 数据 | `SELECT count(*) FROM fields f JOIN datasets d ON f.dataset_id=d.id JOIN regions r ON d.region_id=r.id WHERE r.name='IND'` |
| 3 | 黑名单干净 | `cache/bad_tokens.json` 必须是 `[]` 或不含结构算子（`ts_backfill` 等 46 个受保护） |
| 4 | 断点文件不存在 | 首次开波应为空；若存在，确认是要续跑而不是新跑（新跑加 `WQB_CAMPAIGN_FRESH=1`） |
| 5 | 平台并发余量 | IND 定稿 `--max-inflight 2`（用户 2026-10-25 指定；平台上限约 10，但与 EUR 战役并行时仍受账户级限流约束，撞了就会 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`） |

---

## 2 三条常用命令

```bash
# ① 干跑校验：只打印字段×族覆盖矩阵，零仿真（改完引擎必先跑这个）
<venv> -X utf8 Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/ind_main.py --audit <dataset>

# ② 正式托管（前台会被 stall/熔断看护；等价于直接跑 run_ind.cmd）
<venv> -X utf8 Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/ind_runner.py \
  --only-cats EARNINGS,IMBALANCE,INSIDERS,MACRO,OPTION,SENTIMENT,SHORTINTEREST \
  --min-cov 0.35 --require-ten-years --max-inflight 2 \
  --stall-sec 900 --check-sec 60 --zero-alpha-stop 3

# ③ 随时查进度（不拉起进程）
<venv> -X utf8 Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/ind_runner.py --once
```

可选参数：

| 参数 | 用途 |
|---|---|
| `--datasets a,b` | 只跑指定的集 |
| `--limit N` | 只跑 EV 榜前 N |
| `--only-cats OTHER,PV` | 锁定类别（硬过滤，非排序） |
| `--max-inflight N` | 在飞上限（与开发波并行时设 4） |
| `--sweep-done` | 只对已判完的近闸集补扫设置轴 |
| `WQB_CAMPAIGN_FRESH=1` | 忽略断点全新跑 |

---

## 2.1 塔位口径与「未点亮优先」（2026-10-25 实测；同日已把流水线改成同一口径）

平台「塔」= **本季度**已提交 alpha 按 `category × region × delay` 计数，**满 3 颗点亮**。
证据：`get_pyramid_alphas()` 不带日期时默认取当季（`world-quant-brain-mcp/brain_mixin_correlation.py:1021-1040`），
`tools/campaign_intel.py pyramid` 直接调它 ⇒ 输出是**季度口径**，不是历史累计。

| 口径 | 来源 | 用途 |
|---|---|---|
| 流水线 `[lit]`（2026-10-25 起） | `compute_lit()` → `get_pyramid_alphas()`（默认当季），取 `pyramids[REGION]["D1"]`，`>=3` 判点亮 | 选集降权 |
| 平台塔位 | 同上 | 点塔进度 |

⚠ **2026-10-25 修正（用户裁定）**：旧 `compute_lit` 拉 `stage=OS` **全量历史累计**、`>3` 判点亮，
与平台口径不一致 —— IND/D1 实测 FUNDAMENTAL 历史 5 / 当季 2、RISK 6 / 1、INSTITUTIONS 4 / 1
⇒ 这三类被误判「已点亮」而排除在第一波 `--only-cats` 之外，**实际分别还差 1 / 2 / 2 颗**。
现实现要点（`wqb_campaign/lit.py` + `campaign_semantics.lit_set()`）：

- 只认平台当季 `pyramid-alphas`，`>= LIT_THRESHOLD(=3)` 即点亮（`lit_set()` 是唯一判定点，
  调用方不再写 `>3` / `>=3`）；
- 解析同时兼容客户端原始 **list** 形态与 MCP `_slim_pyramids()` 重排后的 **dict** 形态；
- 缓存带 `metric=pyramid_alphas_quarter_v1` + `delay=D1`，**旧历史累计缓存自动失效**；
- 抓取失败返回 `{}`（按「无点亮」处理）且不写缓存，避免一次网络抖动在 12h 内被当成事实。

2026-10-25 IND/D1 实测（`compute_lit("IND", refresh=True)` 输出，与平台一致）：

- 平台塔位 **5/15** 已点亮：`analyst 3 / model 3 / news 4 / other 4 / pv 8`。
- 未点亮：`macro 2`、`fundamental 2`、`earnings 1`、`risk 1`、`institutions 1`，其余 5 类为 0。

**第一波（2026-10-25 运行中）覆盖 11 集**：EARNINGS 3 集、SENTIMENT 4 集、OPTION 2 集、INSIDERS 1 集、SHORTINTEREST 1 集。
⚠ 它的 `--only-cats` 是按**旧口径**定的（不含 FUNDAMENTAL/RISK/INSTITUTIONS），
**不改在跑进程**；下一次开波起按新口径排序。
`MACRO` / `IMBALANCE` 在本区**无法用本引擎挖**：`dataset_profile` 里 `macro63` 仅 1 字段、`imbalance5` 仅 2 字段，
被 `n_fields>=3` 的结构门槛挡在池外（市场级单字段横向退化，要挖只能另走单字段方案）。

**第二波建议**（第一波跑完后；先 FUNDAMENTAL，差 1 最接近点亮）：

```bash
<venv> -X utf8 Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/ind_runner.py \
  --only-cats FUNDAMENTAL \
  --min-cov 0.35 --require-ten-years --max-inflight 2 \
  --stall-sec 900 --check-sec 60 --zero-alpha-stop 3
```

`FUNDAMENTAL` 池内 10 集满足 `n_fields>=3`（`fundamental25` cov 0.298 会被 0.35 门槛跳过）。
排序上 `fundamental93` 是零开采处女地（`aCnt=1 且 VS=5`，32 字段）最优先；
`fundamental90`（aCnt=81、53 个未测字段）、`fundamental1`（VS=4、118 字段）次之。

> ⚠ **闸门口径别读错（2026-10-25 21:50 核代码）**：覆盖率闸比的是 `dataset_profile.avg_field_coverage`
> （`all_datasets()` 里别名为 `cov`），**不是**平台 API 的 `coverage` 字段。`fundamental93` 的平台 `coverage=0.3285`
> 看着过不了 0.35，但它的 `avg_field_coverage=0.5362` ⇒ **实际会被选中**，不需要为它调低 `--min-cov`。
> `VIRGIN_MIN_COV=0.35` 只对处女地做 `eff_min = min(eff_min, 0.35)`，不是无条件放行。
> 排序键 = 未点亮类别优先 → 处女地优先 → `--priority-cats` 顺序 → 暴露多样性 → `VS×cov`，
> 所以 `--only-cats FUNDAMENTAL` 时处女地 `fundamental93` 天然排第一。

⚠ **实际第二波（2026-10-25 23:11 启动，supervisor PID 32676）跑的是 3 集**：
`--datasets fundamental93,fundamental94,risk70`（fundamental93 已判 DEAD，见 §2.3.1；risk70/fundamental94 在飞）。
其后**不要再按 `--only-cats INSTITUTIONS,RISK` 开波**：INSTITUTIONS 已有 2 颗干净库存等确认（§2.2），
再挖是重复投入；RISK 的 risk71 族已被 prod 墙判死（§2.3）。下一波的高价值目标见 §2.3 结论第 2 条（EARNINGS ladder 修复）。
⚠ 真正能点亮塔的是**提交**，而 REGULAR 提交受 ET 日配额约束（4/4）——塔位差 1 时不要一次挖几十颗，
够 1 颗可提交即可（`submit_verdict` 只拦不放，提交仍需用户确认）。

---

## 2.2 未点亮塔的可提交库存（2026-10-25 21:45 实测；提交仍需用户明确确认）

> 口径：平台 `get_alpha_details`（metrics/checks/pyramids）+ `submit_verdict`（RA 否决）+ `get_alpha_yearly_stats`（十年）
> + DB `prod/self`（2026-10-23 平台同步，7 天缓存内）。三颗均 `RA failed=0`、2014–2023 **逐年 PnL 全正**。

| 当季塔位 | alpha | 表达式要点 | S / F / TO | 2Y / sub / robust | prod / self | 塔归属 |
|---|---|---|---|---|---|---|
| INSTITUTIONS (1/3，差 2) | `E5VNe67L` | `institutions6` 处置占比 → PV 残差 | 3.20 / 2.52 / 0.2497 | 3.00 / 1.64 / **1.80** | **0.6643** / 0.3437（10-26 00:47 refresh） | institutions + pv（eff=2） |
| INSTITUTIONS | `KPmvEYeE` | `institutions6` 处置量 → PV 残差 + industry 中性 | 3.07 / 2.36 / 0.2387 | 3.14 / 1.65 / **1.49** | **0.6162** / 0.3094（10-26 00:56 refresh） | institutions + pv（eff=2） |
| MACRO (2/3，差 1) | `vRO9nG3w` | PV 残差（`ts_std_dev(returns,20)`）+ `mcr63_membership` | 2.90 / 2.16 / 0.2579 | 3.14 / 1.69 / **1.78** | **0.6804** / 0.6806（10-26 01:05 refresh，余量 0.0196） | macro + pv（eff=2） |

- 三颗 settings 一致：IND/TOP500/D1、decay **126**、STATISTICAL、truncation 0.08、nanHandling OFF、maxTrade OFF、2014-01-01→2023-12-31。
- **两两相关性**（2586 个共同交易日的 PnL 差分 Pearson，本机实测）：`E5VNe67L↔KPmvEYeE` **0.6615**、
  `E5VNe67L↔vRO9nG3w` 0.6733、`KPmvEYeE↔vRO9nG3w` 0.6245 ⇒ 三颗可**依次**提交（均 <0.7）；
  ⚠ `E5VNe67L↔9qEPO5K2` = **0.7235**，这两颗不可配对提交。
- **未就绪**：RISK 的 `mLjnnzKE`（robust 0.82）与 `xAj77zlg`（robust 0.91）被 `LOW_ROBUST_UNIVERSE_SHARPE` 拦
  （`submit_verdict=BLOCKED`）；`3qjKgeAX` 已 ACTIVE（DB 状态未同步，**勿重提**）。
  EARNINGS 的 `wp9d6xLd`（`rank(-ts_regression(ts_zscore(returns,252), ts_zscore(ern3_pre_interval,252),252,rettype=0))`）
  其余闸全过：S 2.34 / F 1.69 / TO 0.2226 / sub 1.85 / **robust 1.70** / investability 1.54，
  唯一缺项 **`IS_LADDER_SHARPE` WARNING：2Y=1.29 < limit 1.58（year 3）**⇒ RA failed=1，BLOCKED。
  修复方向 = 抬近三年 Sharpe（不是抬全期）：`group_rank` 腿变换 / 种子长窗 / `hump` 平滑
  （见记忆 `alpha-ladder-group-rank`）；EARNINGS 当季 1/3，仍差 2 颗。
- **稳健性已落台账（2026-10-25 21:49；报告 `reports/robustness_20261025.md`）**：
  `E5VNe67L` **PASS**（近 3 年 CV 0.18）、`KPmvEYeE` **PASS**（CV 0.36，贴线软标记）、
  `vRO9nG3w` **CONDITIONAL**（CV 0.42，2021 年 S=1.33 拖累；不拦截提交，但 skill 要求先 repair ≤2 轮再请确认）。
  季度回撤因认证 429 未逐季算，年度最大回撤 3.43% / 4.01% / 4.12%；`submit_verdict` 三颗均 `failed_ra=0`、
  `hard_gate_warnings=[]`（`MATCHES_THEMES` / `OSMOSIS_ALLOCATION` 是信息型 WARNING）。
- **提交前置**（缺一不可）：台账 `robustness_<id>` 已有记录（上述三颗无需再声明 `robustness_audited=True`）；
  提交前再跑一次 `check_correlation(refresh=True)` 确认 prod<0.7；REGULAR 受 ET 日配额 4 颗约束；**用户明确确认后才可 POST**。
- 备选：institutions6 另有 `JjP0Ja5l`(prod 0.665) / `9qEPO5K2`(0.628) / `bl8210Wq`(0.670) 等满足 prod<0.7，可换配。

---

## 2.3 近闸候选全景（2026-10-25 实测；只读扫 `backtest_results` + `submit_ready`）

口径：四道数值闸 = S≥1.58 / F≥1.0 / 2Y≥1.0 / sub≥1.0（IND 区域例外 `_G2Y=_GSUB=1.0`）。
⚠ **`backtest_results.ra_failed_checks IS NULL` 表示「未核验」，不是「RA 全过」**——
能否提交只能看 `submit_ready.gate`（本表右列即据此修正，两张表逐条对过）。

| 类别（当季塔位） | 命中 | 代表 alpha | 数值闸 | 真实拦阻 |
|---|---|---|---|---|
| EARNINGS (1/3) | 9 条 ≥3/4 | `wp9d6xLd` / `MP0EwRQM` / `58jmR0vJ` | 4/4 | `IS_LADDER_SHARPE`：2Y 1.29–1.45 < 1.58（year 3） |
| EARNINGS | | `pwv2QYMX` | 3/4（2Y 0.92） | 同上 + 2Y 不足 |
| INSTITUTIONS (1/3) | 31 条 4/4 | `E5VNe67L` / `KPmvEYeE` | 4/4 + RA 0 | 无 —— **2 颗即可点亮，等用户确认提交** |
| RISK (1/3) | 8 条 4/4 | risk71 族 `Xg7ZZlNa`(S 3.52) … `A1lXXaxe`(S 1.83) | 4/4 | **全灭**：5 条 prod 0.86–0.99（`FAIL:PROD` / `FAIL:ADD_MIX`）；另 3 条 prod 虽 <0.7 但 `LOW_ROBUST_UNIVERSE_SHARPE` FAIL（`1Yw33mO6` 0.65 / `xAj77zlg` 0.91 / `mLjnnzKE` 0.82，`submit_verdict` 实跑全 `BLOCKED`） |
| OPTION (0/3) | 1 条 3/4 | `blb2MvqK`(option30, w187s) | F 0.83 / TO 41% | `LOW_FITNESS`+`HIGH_TURNOVER`；本波 option30 模板族只到 S 0.18（旧波能到 1.83 ⇒ 模板族差异，非数据死） |
| FUNDAMENTAL (2/3) | 0 | — | — | 差 1；等第二波 `fundamental94` |
| MACRO (2/3) | `vRO9nG3w`（§2.2） | — | 4/4 + prod 0.6695 | 无 —— 等确认提交；`macro63` 仅 1 字段，本引擎无法再挖 |
| ANALYST / MODEL（**已点亮**） | 多条 sub 差 0.01–0.18 | `LLNOLZe6` / `mLjlQzk5` | 3/4 | `LOW_ROBUST_UNIVERSE_SHARPE`（robust 0.58–0.99）；塔已点亮，不再投入 |

**结论（按用户「未点亮塔优先 + ATOM 优先」口径）**

1. **能点亮塔的最近动作只有提交**：INSTITUTIONS 2 颗（`E5VNe67L`/`KPmvEYeE`）+ MACRO 1 颗（`vRO9nG3w`）；
   三者相关性见 §2.2，提交前仍需 `check_correlation(refresh=True)` 与用户确认。
2. ~~定向挖掘唯一高价值目标 = EARNINGS ladder 修复~~ **已证伪（2026-10-25 23:5x）**：
   `MP0EwRQM` 的表达式与已 ACTIVE 的 `3qjKgeAX` **逐字相同**
   （`rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(ern3_all_delay_1_pre_interval, 252), 252, rettype=0))`），
   `wp9d6xLd` / `58jmR0vJ` 只是同一信号的字段变体/窗口变体 ⇒ 自身相关性 ≈1.0，**一颗都提交不了**，
   ladder 修好也无用。⇒ 未点亮塔上的「近闸候选定向挖掘」**已无可用目标**（纯 ATOM 全灭 + EARNINGS 是重复信号），
   增量只能来自新数据集（§2.4 波 3）。
3. **RISK 的 risk71 族已被 prod 墙判死**（0.86–0.99），不要再从该族取候选；新证据只能等 `risk70`（第二波在飞）。
4. `analyst_consensus` / `model252` 的 sub 贴线候选属**已点亮塔**，按用户优先级不再投入。
5. **纯 ATOM 在未点亮塔上已无可用目标**（2026-10-25 23:4x 实测：PV 词表正则扫全部未点亮塔上
   3/4+ 且 S≥1.4 的候选，**48 条**）。纯 ATOM 只有 **8 条，全部是 risk71 `ws3_risk71_wallbreak`** —— 正是上表那一族，
   prod 0.5496–0.9868 + robust 0.65–0.91，`submit_verdict` 实跑三条 prod<0.7 的全 BLOCKED ⇒ **一条都不通**。
   其余 **40 条全部含 PV `returns`**（earnings3 9 条 / institutions6 31 条），
   按用户口径只能算**残差/组腿**。⇒ objective「对近闸候选定向挖掘」的增量只在
   **EARNINGS ladder 修复（残差口径）**；若坚持纯 ATOM，只能靠新数据集（`risk70`/`fundamental94` 第二波正在给答案）。

### 2.3.1 第一/二波已判结果（2026-10-26 00:40 实测，`results/full_template_campaign_results_IND.json`，11 键）

> 文件是**嵌套**结构 `{"results": {<ds>: {...}}}`，读数要先取内层（`persist.load_results()` 不解包，pipeline 按 `res["results"][ds]` 用）。

| 数据集 | 类别 | verdict | S | F | 2Y | sub | n | 关键证据 |
|---|---|---|---|---|---|---|---|---|
| **risk70** | RISK/PV | **ALIVE** | **4.74** | — | **5.25** | — | 55 | 全波最强；`n_joint=9`（pp 预处理族的市值残差动量）；已派生 `ZYmJYx30`（S 3.89 / 2Y 3.59 / sub 1.73 / tvr 0.228，**prod 0.723 越 0.7 红线 ⇒ 不可提交**，直方图 [0.7,0.8) 桶 n=1）与 `e76j7Kmz`（S 3.68 / 2Y 3.63 / sub 1.70 / margin 14.9bp，稳健闸 **CONDITIONAL**：近 3 年 CV 0.42；prod 待测，同族近似 ⇒ 先验偏低） |
| option1 | OPTION | INSUFFICIENT_HISTORY | 2.90 | 2.75 | 0.00 | 2.33 | 56 | 持仓仅 2017 一年（`n_years=1`/`top_share=1.0`/`late_start`）⇒ 十年闸否决**正确**（僵尸数据） |
| insiders1 | INSIDERS | DEAD | 1.20 | 0.34 | 1.71 | 0.79 | 48 | 十年齐备 `fragile=false`，但 F 差 0.66、sub 差 0.21（季度内幕持仓低收益，结构性） |
| shortinterest5 | SHORTINTEREST | NO_DATA | — | — | — | — | 0 | 未产出任何 alpha |
| option30 | OPTION | DEAD | 0.18 | 0.05 | 0.23 | 0.25 | 26 | 本波模板族全面不达标（旧波 w187s 另有 S 1.83 候选） |
| earnings11 | EARNINGS | DEAD | 0.98 | 0.24 | 0.79 | 0.86 | 62 | 全面不达标 |
| fundamental93 | FUNDAMENTAL | DEAD | 0.58 | 0.24 | 0.64 | **-0.46** | 19 | 处女地（aCnt=1/VS=5）但信号弱且 sub 为负 ⇒ 处女地≠有信号 |
| sentiment26 | SENTIMENT | DEAD | 0.40 | — | 1.00 | — | 36 | 覆盖达标但信号弱 |
| news_sentiment_transfer | NEWS | DEAD | 0.72 | — | 0.57 | — | 33 | 低暴露（1 种），2Y 也不足 |
| sentiment21 | SENTIMENT | DEAD | 1.12 | — | 2.16 | — | 38 | 本波模板族 S 最高但仍不足 1.58 |
| sentiment23 | SENTIMENT | DEAD | 0.49 | — | 0.68 | — | 48 | 全面不达标 |

> 后四行（sentiment26 / news_sentiment_transfer / sentiment21 / sentiment23）曾在两波并行时被覆盖丢失，
> 2026-10-26 00:37 从覆盖前快照 `cache/_snap_results_IND_0018.json` 回填（见 §5 第 17 条）。
> `fundamental94` 第二波派发 48 条后进程中断，已并入第三波重跑。

### 2.4 第三波候选池（2026-10-25 23:5x 实测，只读 `dataset_profile`）

口径：IND/D1、**未点亮类别**、`n_fields>=3` 且 `avg_field_coverage>=0.35` ⇒ **24 集**；
排序 = 塔差优先 → 低 `alphaCount`（未开采）→ 覆盖。已判死/已试的按证据排除。

| 优先 | 数据集 | 类别（差几颗） | 字段 / 覆盖 | alphaCount | 未测字段 | 依据 |
|---|---|---|---|---|---|---|
| 1 | `fundamental90` | FUNDAMENTAL（差 1） | 65 / 0.721 | 81 | **53** | 未测过半、最接近点亮 |
| 2 | `fundamental1` | FUNDAMENTAL（差 1） | 118 / 0.563 | 180 | 0 | VS=4，历史无回测 |
| 3 | `risk68` | RISK（差 2） | 5 / 0.979 | 193 | 4 | bestS 2.26 / best2Y 1.29（该集历史有信号） |
| 4 | `fundamental23` | FUNDAMENTAL（差 1） | 39 / 0.895 | 1585 | 37 | 拥挤但仍有未测 |
| 5 | `sentiment21` | SENTIMENT（0/3） | 105 / 0.968 | 687 | **90** | bestS 3.01 / best2Y 2.07（**需 3 颗才点亮，ROI 低，备选**） |
| 6 | `sentiment26` | SENTIMENT（0/3） | 18 / 0.532 | 462 | 0 | 本波未试、覆盖达标（备选） |

排除项（不复挖）：`fundamental93`（第二波已判 DEAD）、`fundamental94`/`risk70`（第二波在跑）、
`earnings3`（走 ladder 修复，不走新集；另 2 颗靠修复后的残差候选）、`earnings6`（cov 0.357 贴下限、十年数据风险高）、
`option30`/`option1`（§2.3.1 已判 / 僵尸数据）、`insiders1`/`shortinterest5`（DEAD / 数据集级 NO_DATA）、
`macro63`/`imbalance5`（字段 1–2，结构门槛外）。

**第三波已启动（2026-10-26 00:37）**：`--datasets fundamental94,fundamental90,fundamental1,fundamental23,risk68 --min-cov 0.35 --require-ten-years --max-inflight 2 --stall-sec 1800 --check-sec 60 --zero-alpha-stop 0`。
单进程独占 state（不要再叠第二波，见 §5 第 17 条）；启动前已从快照回填 4 个 sentiment 结果并重算 `done`（11/16）。
`fundamental94` 是第二波未跑完的重跑项，`risk70` 已完成不再入列。

启动命令（**等第二波释放账户槽位后**；并发仍为 2、十年硬闸不变）：

```bash
<venv> -X utf8 Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/ind_runner.py \
  --datasets fundamental90,fundamental1,fundamental23,risk68 \
  --min-cov 0.35 --require-ten-years --max-inflight 2 \
  --stall-sec 900 --check-sec 60 --zero-alpha-stop 3
```

> ⚠ **塔必须由「互不相关的 3 颗」点亮，不是同一信号的 3 个变体**：EARNINGS 的 3 颗 ladder 候选
> （`wp9d6xLd`/`MP0EwRQM`/`58jmR0vJ`）与已 ACTIVE 的 `3qjKgeAX` 同族，其中 `MP0EwRQM` **逐字相同** ⇒
> 修过 ladder 也交不了（self-corr ≈1.0），**不是「+1 颗」而是 0 颗**；EARNINGS 点亮只能另找 earnings 系不同信号
> （`earnings6` cov 0.357 贴线）或换塔。
> 同理：波 3 若在 FUNDAMENTAL 内连挖 3 集，须先确认候选间 self/prod 互相关 <0.7，否则只算 1 颗。

### 2.5 第四波候选池（S0 重扫 2026-10-26 01:07，`campaign_intel.py s0-select --region IND --delay 1 --universe TOP500`）

口径：平台推荐 31 → 剔除已点亮塔 0 → 剔除判死 4（`sentiment21`/`option30`/`earnings11`/`news_sentiment_transfer`）⇒ **存活 27**。
下表只留「未点亮塔 + `n_fields>=3` + 未被第三波覆盖 + 未判死」的集；`yield` = 该集历史回测产出率，`maxS` = 历史最高 Sharpe。

| 优先 | 数据集 | 类别（当季缺口） | 字段 | alphaCount | yield / bt / maxS | 判据 |
|---|---|---|---|---|---|---|
| 1 | `fundamental89` | FUNDAMENTAL（差 1） | 195 | 3697 | — / 0 / — | 字段最多、本波未试；拥挤度中等 |
| 2 | `fundamental44` | FUNDAMENTAL（差 1） | 12 | 4031 | — / 0 / — | 会计质量模型，字段精而少，适合机制驱动 |
| 3 | `fundamental25` | FUNDAMENTAL（差 1） | 6 | **202** | — / 0 / — | **低竞争**（ac 仅 202），同池唯一「零拥挤」的多字段集 |
| 4 | `earnings6` | EARNINGS（1/3，差 2） | 20 | 621 | — / 0 / — | 跨区 RA-clean `GBR:8`；EARNINGS 塔只能靠它这类**不同信号**，不能再交 ladder 同族（§2.4 尾注） |
| 5 | `fundamental86` | FUNDAMENTAL（差 1） | 7 | 6647 | — / 0 / — | **ATOM 复制第一顺位**：`MP7gw71r` 已 ACTIVE（同集 fnd86 单字段 ATOM，S3.05/prod 0.6272/RA 0，见 §2.6）；另有 72 条未回测库存，先查再发波 |
| 6 | `fundamental17` | FUNDAMENTAL（差 1） | 350 | 30587 | — / 0 / — | 最拥挤（跨区弱 GBR/GLB），仅在 1–5 全灭时动 |

**排除项（附证据，避免重复投入）**：
`earnings3`（yield 0.048@42bt、maxS 2.37 —— 仍是 EARNINGS 最强现货，但按 §2.4 走 **ladder 修复路线**，不开新集）；
`risk71`（prod 0.86–0.99 族级判死）、`risk88`/`macro63`/`imbalance5`/`fundamental4`（字段 1–2，结构门槛外）、
`institutions6`（本波正在交付 `E5VNe67L`/`KPmvEYeE` 两颗，先看提交结果再决定是否加挖）、
`fundamental90`/`fundamental1`/`fundamental23`/`fundamental94`/`risk68`（第三波在飞）。

> 判据提醒：**缺强度证据不开波**——`yield`/`bt` 为空表示该集在 IND 从未回测过，属「未开采」而不是「已验证」；
> 开波前先用最小探针（16–20 条骨架）验信号，不要直接上 50+ 条模板族。

### 2.6 ATOM 库存盘点（2026-10-26 01:1x 实测：只读 `alphas` + `fields`/`datasets`）

口径：`expression` 非空、**不含 `returns`**（⇒ 单数据集 ATOM）、未软删、非 ACTIVE/SUBMITTED，
且 S≥1.58 / F≥1.0 / 2Y≥1.0 / sub≥1.0 / tvr≤0.40（平台 `HIGH_TURNOVER` 上限）。

**结果：18 颗数值闸全过，但 100% 落在已点亮塔**：

| 数据集 | 塔 | 颗数 | 最好 S | 说明 |
|---|---|---|---|---|
| `intraday_pv_feats` | PV（已亮） | 8 | 4.68 | `corr_*_with_volume` 族，高换手历史多，prod 拥挤（0.72–0.98） |
| `analyst_consensus` | ANALYST（已亮） | 16 | 2.35 | `mean_flash_estimate_*` 族，2Y 普遍 2.1–3.6，prod **全部未测** |
| `model252` | MODEL（已亮） | 2 | 2.37 | `defensiveness_composite_score`，tvr 0.10 / margin 18bp，质量最好 |
| `pv103` | PV（已亮） | 1 | 3.38 | 单颗 |

最高质量的五颗（prod 均未测，需先实测才谈提交）：
`omLwErNm`（PV, S3.51/2Y1.44/sub1.34/tvr0.371）、`vRrnJjaw`（pv103, S3.38/2Y2.15/sub1.57/tvr0.242）、
`vRjoLR63`（model252, S2.37/2Y3.10/sub1.08/tvr0.104/mg 18bp）、`npd9ENpw`（model252, S2.36/2Y3.11/sub1.11）、
`XgbX3Vq0`（analyst_consensus, S2.35/2Y2.66/sub1.38/tvr0.109）。

**三条结论（决定下一波怎么打）**：

1. **未点亮塔的 ATOM 库存 = 0**。要「ATOM 优先 + 点新塔」，只能靠新挖——具体就是第三波正在跑的
   `fundamental*`（塔 2/3）与 `risk68`（塔 1/3），它们的主批 57 条/集天然是纯 ATOM。
2. **已亮点塔的这 18 颗不是白扔**：它们是「无塔压力下的配额填充 / SUPER 组件 / ATOM 配方模板」，
   但提交前必须先 prod 实测（全部 None，不能按未测放行）。⚠ 不要因为它们分数高就挤掉点塔候选的配额。
3. **`fundamental86` 的优先级上调**：`MP7gw71r`（`group_neutralize(ts_zscore(subtract(add(fnd86_earnings_score,
   fnd86_fundamental_score), fnd86_price_momentum_score), 315), industry)`）**已 ACTIVE/OS（2026-08-28，PPA 通道，
   color GREEN，S3.05 / F2.72 / 2Y2.77 / sub1.39 / tvr0.156 / prod 0.6272 / RA failed 0 / 塔 IND/D1/FUNDAMENTAL）**
   ⇒ 该集已证明「单字段 ATOM 能过全部平台闸 + prod 墙」，是**复制 ATOM 的第一顺位**（7 字段 + 72 条未回测库存）。

> 复查口径（只读、零平台请求）：`alphas`（`region_id=5`、`expression NOT LIKE '%returns%'`、排除
> ACTIVE/SUBMITTED/DECOMMISSIONED、S/F/2Y/sub/tvr 五闸）+ `fields`（`field_name → dataset_id`）+
> `datasets`（`id → name/category`）。不做持久化脚本——查询口径写在这里，临时脚本用完即删。
> 判据注意：**prod 为 `None` ≠ 合格**，只是「还没测」。平台 `check_correlation` 是唯一合规取数口。

---

## 3 闸门与门槛：EUR vs IND 差异（**这是最容易踩错的地方**）

| 项 | EUR | IND | 说明 |
|---|---|---|---|
| LOW_SHARPE | 1.58 | **1.58** | 严格不等式（`1.58==1.58` 判 FAIL） |
| LOW_FITNESS | 1.0 | **1.0** | 唯一用 `≥` 的闸 |
| LOW_2Y_SHARPE | 1.58 | **1.0**（config） | ⚠ 以平台 `checks[].limit` 为准 |
| LOW_SUB_UNIVERSE_SHARPE | **0.53×S**（比率闸） | **1.0 绝对** | 口径完全不同：EUR 高 S 更难，IND 固定 1.0 |
| LOW_ROBUST_UNIVERSE_SHARPE | 0.7 | **1.0 固定** | ★ IND 的真正瓶颈 |
| TO | 0.05–0.3 | **0.01–0.7** | IND 宽容得多 |
| margin | ≥0.0005 | ≥0.0005 | |
| prod / self | <0.7 | <0.7 | 死线，无豁免 |
| investability | N/A | **N/A** | 只对 ASI/JPN/HKG/TWN/KOR 生效；IND 不测，评估表写 N/A |
| signal_floor | — | max_sharpe 1.2 / 连续 2 批 | 低于即判信号天花板，停生成 |
| mode_b | 1.25 / 0.8 | **1.5 / 1.0** | IND 是 robust 墙区，提门槛 |

### ★★★★★ IND 特有的两条硬约束

1. **robust ≥ 1.0 是绝对闸，且与 S 严格负相关**。
   实测规律：首个过闸结果常是 `rob < 1.0` 且 `S/rob > 2.5` ⇒ 不可交付。
   ⇒ **不要追最高 S**，要在 (S, robust) 联合可行域里找点，先最大化 robust 再抬 S。
2. **`maxTrade=OFF`（区域缺省）的代价**：TO 会升到 0.18–0.23、越过 F 的分母平台、margin 塌约 4×。
   ⇒ 不要为了"拿 investability 指标"去改 maxTrade（IND 本来也不测该项）。

---

## 4 流水线内部规则（与区域无关，照抄即可）

### 4.1 目标池
`dataset_profile` 中该区域 `n_fields >= 3` 的集数即分母（EUR 是 169）。

### 4.2 覆盖率门槛（两处并列，改一处无效）
- 普通集：**0.6**
- 处女地集（`alphaCount<=10` 且 `valueScore>=5`）：`min(0.6, 0.35)` = **0.35**
- ⚠ 代码里是 `priority_min_cov` 与 `eff_min = ... else 0.6` **两个字面量**，只改一个不生效。

### 4.3 字段选择
每语义维取 `PER_DIM` 个代表（族键去数据集前缀+去窗口数字）→ 全族裁剪到 `FULL_FIELD_CAP=8` → 其余进 probe 层（上限 `PROBE_FIELD_CAP=12`，只跑 1 条最便宜探针）→ 收割后 `carrier_expand()` 把最强结构补跑所有 probe 字段。

### 4.3.1 残差化族（2026-10-25 接入；IND 唯一被证实能过 prod 墙的配方）

- 结构（`generate.RESIDUAL_TPL`）：`rank(-ts_regression(ts_zscore(returns,252), ts_zscore(<F>,252), 252, rettype=0))`；
  `reslag` 变体先把字段 `ts_delay(F,21)`（wave232 实测 2.98→3.10）。
- 覆盖：**每个非探针字段 2 条**（探针仍只跑 1 条 `lvl_rk`，守成本纪律）。若本集最强族是
  `res/reslag`，`carrier_expand` 会把该结构补跑全部 probe 字段（`build_one_family` 已支持这两个族名）。
- **设置必须 `decay=126`**（`generate.RESIDUAL_DECAY`）：IND 基础 `decay=4` 复现不了实测结果
  （wave232 的 10 颗全部 decay 126）⇒ 残差化**单独一批派发**（断点键 `<ds>@res`），不混进主派发批。
- 合规：`src/wqb/profiles/locked.py` 的 `mixed_signal_ban` 明确允许「第二个数据集只以条件 / 分组 / **残差**入场」。
  ⚠ **归类**：`returns` 是 PV 字段 ⇒ 残差化族是**跨数据集**结构，不是纯 ATOM（§4.3.2）；它在主批之后单独派发，符合「ATOM 优先」。
- 回归：`tests/unit/11_campaign/test_campaign_package.py` 已把 17 个族（13 L1×L2 + dw + pp + res/reslag）的括号平衡与 ≤10 调用点钉住。

### 4.3.2 路线优先级：ATOM 优先，组腿次之（2026-10-25 用户指令）

- **ATOM**（单数据集）：一条表达式只取**同一个数据集**的字段。`returns` 属 **PV** 数据集，
  用它的表达式（含残差化族）**不是** ATOM（用户 2026-10-25 明确：`kqJweZQz` 用了 PV 的 returns，不算 ATOM）。
- **跨数据集**（按优先级从高到低）：① 纯 ATOM（只用本集字段，campaign 主族 13 L1×L2 + dw + pp）；
  ② 残差结构（PV `returns` 对本集字段回归，本文件的 `res` / `reslag`）；③ 组腿（两条独立信号腿
  `add` / `+` / 加权相加，受 `locked.py::mixed_signal_ban` 约束）。组腿只在 ATOM 与残差都用尽后作救援。
- 执行口径：campaign 引擎的主批天然是纯 ATOM（单字段 × 模板族），残差化是**主批之后**的单独一批
  （断点键 `<ds>@res`），顺序已符合本优先级。判断「某集是否值得挖」先看能否独立产出 ATOM 候选，
  **不要指望组腿救活一个 ATOM 全灭的集**；提交顺序同理，纯 ATOM 候选优先。
- **纯 ATOM 模式开关（2026-10-26 落地）**：`WQB_ATOM_ONLY=1` ⇒ `generate.build_residual()` 直接返回空，
  pipeline 的 `[res]` 段整段跳过，日志首屏打 `[res] WQB_ATOM_ONLY=1 ⇒ 跳过残差化族`。
  缺省（不设）= 保留残差族（旧行为）。**默认关的理由**：残差族是 IND 目前唯一被证实能过 prod 墙的配方
  （E5VNe67L 0.6643 / KPmvEYeE 0.6162 / vRO9nG3w 0.6804 三颗实测），关掉等于放弃已验证通路；
  是否只用 ATOM 由**波次口径**显式决定，不由引擎替人做取舍。
  用法：`WQB_ATOM_ONLY=1 <venv> -X utf8 .../ind_runner.py --datasets ...`（Windows PowerShell 先 `$env:WQB_ATOM_ONLY=1`）。
  ⚠ 长驻进程**不热加载**：已在跑的波次不受影响，开关只对下一次启动生效。
- **审查/评审排序（按本条执行）**：收批后先按「是否 ATOM」分两栏——ATOM 栏按 S/2Y/sub 排序出提交候选，
  残差/组腿栏单独标注 `route=residual` 或 `route=combo`，只在 ATOM 栏不足以点塔时才动用（并且必须过
  prod 实测 + 稳健闸）。`backtest_results.tpl` 里 `res` / `reslag` / `pp` 前缀可直接用来分栏。

### 4.4 判定
| 判定 | 含义 | 后续动作 |
|---|---|---|
| `ALIVE` | S/2Y 双高 | 进定向开发 |
| `BORDERLINE` | 有信号但缺闸 | 看 `year_profile` 再决定 |
| `DEAD` | 挖过，S 不足 | 封存 |
| `NO_DATA` | **跑了但零 alpha** | ⚠ 管道故障，不是信号差 → 立刻查 `bad_tokens.json` |
| `SIM_FAIL` | 仿真异常 | 看错误 |
| `SKIPPED_LOW_COV` | 覆盖率不足 | 未开采 |
| `SKIPPED_TOO_FEW_FIELDS` | 可挖字段 <3 | 未开采 |

### 4.5 样本有效性（**第 0 步，先于一切闸位判断**）
`year_profile` = `{first_year, n_years, top_share, ex_top_ret, last2_ret, late_start, recent_break, fragile}`

- `fragile = late_start 或 n_years<6 或 top_share>0.5 或 ex_top_ret<=0`
- **两类必须分开报**：
  - **A 类 数据太新**（`late_start`/`n_years<6`）→ 出路是换覆盖更早的字段，**不是调参**
  - **B 类 最近失效**（`recent_break`，`last2_ret<0`）→ 信号已死，**直接封存**
- 触发阈值：`max_s >= 1.2`（与 prod 检测同档）

### 4.6 开波后必看的 4 个信号

| 信号 | 正常 | 异常含义 |
|---|---|---|
| 单集耗时 | ~60 min | 远超 → 卡在 `wait_slot` 或 harvest（看 `[gate]` 心跳） |
| `n_alphas` | >0 | **=0 且非 SKIP ⇒ 管道坏了**（熔断会拦） |
| `done` 增长速度 | 1 集/小时 | 10 分钟涨几十个 ⇒ 全在 SKIP 或丢光，查 `n_alphas` |
| `frag=?` | 不应出现 | 出现 = `year_profile` 没算（阈值/异常） |

---

## 5 已知坑清单（17 条，全部来自 2026-10-24/25 实战）

1. **`year_profile` 触发阈值曾写 1.4**（高于 prod 的 1.2）→ `fragile` 一票否决被静默绕过。已改 1.2。
2. **覆盖率门槛是两个并列字面量**，只改一处无效。
3. **处女地门槛 0.35 更松**：看到"cov 0.58 低于 0.6 却在跑"属正常。
4. **`BAD_TOKENS` 绝不能含结构算子**。`ts_backfill` 被误拉黑 ⇒ 所有模板族全被丢 ⇒ 72 个集判 `NO_DATA`。
5. **`filter_bad` 有批量否决护栏**：会全丢 / 丢 ≥50% 时拒绝过滤并告警。
6. **`sims_terminal` 是三态**（True/False/**None=查不到**）。异常不能当"还在跑"。
7. **`wait_slot` 每 60s 打心跳**，`GATE_TIMEOUT=900`，连续 3 次 None 即放行。
8. **看门狗 `stall-sec` 用 900**：判据是日志 mtime，正常静默不可能超 15 分钟。
9. **空转熔断 `--zero-alpha-stop 3`**：连续 3 个非 SKIP 集零 alpha 即停并退出码 2。
10. **n=1 的批必是空批**（`COMPLETE children=0`）⇒ 派发按族**均分**，杜绝单条批。
11. **`validate_expressions` 不查 arity**：`quantile(x, 5)` 能过校验但平台报 `Invalid number of inputs`，整批 5 取消。没跑过的算子先查签名。
12. **`pp` 形态 = 3+2×dw = 21 个调用点**，超"≤10"约束；而 `dw` 只有 9 个。EUR 实证：SENTIMENT 去掉门控 S 从 1.54 掉到 0.98 ⇒ **≤10 与这类稀疏信号互斥**，IND 上要么放弃该形态，要么接受 >10。
13. **`harvest()` 曾返回三元组 + 对 None 取 len**（2026-10-25 修）：异常分支 `return None, [], "error"` 与主流程四元组不一致，且 `_harvest_until_done_impl` 里 `len(rows)` 直接崩 ⇒ 批在 `running/partial` 时**每次都被判 error**，3 次 partial 重试根本跑不到。修法 = 统一四元组 + `len(rows or [])`（`wqb_campaign/transport.py:246,304,316`）。
    ⚠ **第一波在跑进程从未加载这份修复**：它跑的是历史安装位（`wq-brain-ra-eur` 技能目录）下**未入库的旧副本**。所以日志里的 `[harvest-error] <tag> TypeError: object of type 'NoneType' has no len()` 是**旧代码症状，不等于平台没结果**——平台侧用 sim ID 查 `batch_status` 即可确认。
14. **`shortinterest5` 在 IND/TOP500 无持仓（数据集级 NO_DATA，非收割故障）**：3 个字段全是 price 形态，17 颗跑完后 `sharpe=turnover=longCount=shortCount=0`、RA 六项失败。判据 = `batch_get_alpha_metrics` 全 0 且 `turnover=0`（有效信号不会长这样），此后不必再为该集重派。
15. **第二波起只用仓库 IND 启动器**：`Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/ind_runner.py`。两份代码已分叉——仓库 IND 副本有「塔位当季口径」+「harvest 修复」，EUR 安装位是旧快照（**仓库 `Claude/skills/wq-brain-ra-eur/scripts/` 只有 README.md，campaign 代码只存在于安装位，未入库**）。用错启动器会把 §2.1 的新口径和 13 条的修复一并绕开。
16. **`cache/_harvest_safe.py` 不是流水线自带件，缺了整个收割链条静默归零**（2026-10-25 23:5x 实战）。`transport.harvest()` 每批都 `subprocess.run([VENV_PY, <repo>/cache/_harvest_safe.py, sim_id, ds, "camp"])`；该文件不在仓库里（历史上只以未入库的一次性脚本存在于某个工作区），缺失时 `FileNotFoundError` 被 `except Exception` 吞成 `state=error`，日志只留 `[harvest] <tag> error（已收 0/None）第 N 次重试`，**8×180s 后该批作废、整集以 `n_alphas=0` 收场——这是管道故障，不是信号差**。判据：日志出现连续 `error（已收 0/None）` 且 `cache/dispatch_camp_<ds>_*.log` 里批次其实 `status=201` 成功。
    现件已重建（`cache/_harvest_safe.py`，2026-10-25），stdout 契约与三个易踩点：
    - 末行必须 `status=<COMPLETE|ERROR|UNKNOWN> children=<N>`；**排队中平台只回 `{"progress":x}`（无 status）⇒ 打 `UNKNOWN`**，打 `None` 会被 transport 的 `\w+` 正则判成查询失败；
    - **单条批平台不写 children**，只给父响应 `alpha` ⇒ 必须按 `children=1` 报，否则判 `empty` 永久丢结果；
    - **CANCELLED/FAILED 要归一成 `ERROR`**（transport 只认 ERROR/FAIL 为终态，否则白等 8×180s 且毒化表达式自愈不触发）；零交易 alpha（`fitness=null`）要出**行**（sentinel -99），不能出 `x`——否则 rows<children 被打成 partial 白等 3×20s。
    自检：`<venv> -X utf8 cache/_harvest_safe.py <sim_id> <ds> camp`，正常输出 `+ <id> S=… F=… tvr=… 2Y=… sub=…` 每子任务一行 + 末行 `status=COMPLETE children=<N>`。
17. **两波 campaign 并行 ⇒ 同一个 `results/full_template_campaign_results_<R>.json` 后写覆盖前写**（2026-10-26 00:0x 实测，00:40 修正证据）。`pipeline_ind.py` 在每个数据集收尾时 `save_ckpt(ck); save_results(res)`（:159/:190/:664），而 `res` 是**进程启动时 load 的整份 JSON** + 本进程产出 ⇒ 两个 pipeline 同时活着（第一波还在跑 `sentiment23`、第二波在跑 `risk70`）时，后收尾的把另一个刚写的条目**整份覆盖**。
    **实测证据（修正版）**：① 文件是**嵌套结构** `{"results": {<ds>: {...}}}`，`persist.load_results()` **不解包**，pipeline 按 `res["results"][ds]` 用 —— 读数不对内层会误判成「文件只有 1 个键」；② 真正丢的是**第一波最后 4 个 sentiment 集**（`sentiment26` / `news_sentiment_transfer` / `sentiment21` / `sentiment23`）：覆盖前快照 `cache/_snap_results_IND_0018.json` 里有这 4 键，live 文件里没有，而 `checkpoint_IND.done` 里有 ⇒ 后收尾的第二波把它们抹掉了；③ `earnings11` / `fundamental93` / `risk70` **没有丢**（初期误判源于没取内层）。00:37 已从快照回填，results 恢复 11 键。
    连带后果：`ind_runner.zero_alpha_streak()` 读的正是这份 results，**丢条目 = 该集被当成 `n_alphas=0`**（缺键 → `v={}` → 0）⇒ 连击数虚高（当时 done 尾部两条都缺 ⇒ streak=2/3），再丢一个就触发「空转熔断」退出码 2 —— **那是账本假警报，不是管道坏了**（00:31 第二波托管器正是这样误熔断的，日志写「连续 4 个非 SKIP 集 n_alphas=0」而当时 `dispatch_ids.jsonl` 里 sim 全部 `ok=true`）。
    处置：① 两波同时活着时**不要相信** `zero_alpha_streak` 的读数；② 撞到熔断先用 `--zero-alpha-stop 0` 重启（代码里 `if args.zero_alpha_stop > 0` 才判，0 = 关闭），真判据看 `cache/dispatch_ids.jsonl` 的 `ok` 与 `[harvest]` 行；③ 真要并行，给后开的那波设 `WQB_CAMPAIGN_STATE_DIR=<独立目录>`（ckpt/results/digest/heartbeat 全按它走）再启动；④ 已经丢了就从 `cache/_snap_results_IND_*.json` 回填**内层**并重算 `done` 并集，别重跑整集。

---

## 6 成本估算（按 EUR 实测外推）

| 项 | 数值 |
|---|---|
| 单集耗时 | 约 60 min（多字段多族集可到 90 min） |
| 集均表达式 | 20–60 条（`FULL_FIELD_CAP=8` × 13 族 + probe） |
| 覆盖率 < 门槛的集 | 秒级跳过，不耗仿真 |
| EUR 实测 | 169 集 → 41 个真开采（24%），约 6.7 小时/轮（含 72 个作废重跑） |
| IND 预期 | 集数需先查；`TOP500` 更窄，单集更快，但 `robust 1.0` 会让**近闸率远低于 EUR** |

---

## 7 与 EUR 的关键差异总结（给决策用）

- **EUR 的主要瓶颈是 prod 墙**（近交付颗 prod 已测的全 ≥0.78）。
- **IND 的主要瓶颈是 robust ≥1.0 固定**，且与 S 负相关 ⇒ **EUR 的"提 S 优先"策略在 IND 会适得其反**。
- EUR 的 `sub` 是比率闸（0.53×S），高 S 反而更难；IND 的 sub 是绝对 1.0，高 S 相对容易。
  ⇒ **IND 上应该反向操作：先求 robust，再求 S**。
- EUR 有 57/169 因覆盖率 <0.6 被跳过；IND 若 `dataset_health.coverage_min=0.8`，跳过率可能更高，
  **开波前建议先把门槛按 IND 实测分布重定**（`tracking/IND/config/thresholds.json::dataset_health` 已有分位分带参数）。

---

## 8 第三波（全模板 campaign）结果与 S6 回写（2026-10-26 01:40）

### 8.1 12 个已完成数据集（`results/full_template_campaign_results_IND.json`）

| 数据集 | 类目 | cov | 字段 | alphas | max_s | max_2Y | ATOM 最高 | 残差/pp 最高 | verdict |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| risk70 | RISK | 1.00 | 35 | 55 | 4.74 | 5.25 | **0.58** | 4.74(pp=returns 残差) | ALIVE→PARTIAL |
| insiders1 | INSIDERS | 0.39 | 9 | 48 | 1.20 | 2.00 | **1.19** | — | DEAD→FAIL |
| option1 | OPTION | 0.40 | 28 | 56 | 2.90 | 0.00 | 2.90(单年) | — | INSUFFICIENT |
| earnings11 | EARNINGS | 0.50 | 35 | 62 | 0.98 | 1.37 | 0.94 | 0.55 | DEAD |
| fundamental93 | FUNDAMENTAL | 0.54 | 32 | 19 | 0.58 | 0.92 | 0.58 | 0.49 | DEAD |
| fundamental1 | FUNDAMENTAL | 0.56 | 118 | 69 | 0.19 | 1.05 | 0.19 | 0.00 | DEAD |
| sentiment21 | SENTIMENT | 0.97 | 105 | 38 | 1.12 | 2.16 | 1.12 | — | DEAD |
| sentiment23 | SENTIMENT | 0.70 | 105 | 48 | 0.49 | 0.68 | 0.49 | — | DEAD |
| sentiment26 | SENTIMENT | 0.53 | 18 | 36 | 0.40 | 1.00 | 0.40 | — | DEAD |
| news_sentiment_transfer | NEWS | 0.94 | 23 | 33 | 0.72 | 0.57 | 0.72 | -0.80(pp) | DEAD |
| option30 | OPTION | 0.36 | 12 | 26 | 0.18 | 0.28 | 0.18 | — | DEAD |
| shortinterest5 | SHORTINTEREST | 1.00 | 3 | 0 | — | — | — | — | NO_DATA |

S6 已回写（每集一条 `wave_results`，波号 `tpl_<dataset>_d1`，`source_file=results/full_template_campaign_results_IND.json`）：
`risk70=PARTIAL(0 pass / 9 near)`，其余 `FAIL`（`option1` 因仅 2017 单年持仓被判 INSUFFICIENT，`shortinterest5` 零 alpha）。

### 8.2 本轮最重要的三条结论

1. **risk70 的 4.74 不是 ATOM**：`pp = signed_power(rank(-ts_regression(ts_zscore(returns,252),…)),0.7)` 含 PV `returns`；
   ATOM 最高仅 0.58。且平台 `HIGH_TURNOVER 0.7879>0.4` FAIL、prod 因 corr-lock 争用 11 s 超时未取到；
   同族 `ZYmJYx30` 实测 prod=0.723 已越线 ⇒ **risk70 残差族先测 prod 再谈修 turnover**。
2. **未点亮塔没有可提交 ATOM**：五闸全过未提交的 72 颗中有 36 颗 ATOM，**全部落在已点亮塔**
   （intraday_pv_feats / pv103 / analyst_consensus / model252）；未点亮塔（insiders/earnings/risk/institutions）
   的强候选一律是 returns 残差组腿。
3. **insiders1 是唯一「ATOM + 未点亮塔 + prod 余量充足」的集**：`prod_top=0.178`、10 年齐备、逐年不 fragile；
   但最好那颗 `O0JLn561 = ts_scale(vec_avg(insd1_holdings),504)` 实测 **turnover 124.6%、CW 0.256、Fitness 0.34**
   ⇒ 要能提交必须同时解决换手与集中度，且 9 个字段全是 VECTOR（必须先 `vec_*` 聚合）。

### 8.3 下一波队列（等 `fundamental94/90/23/risk68` 收尾后自动接力）

接力脚本 `logs/_tmp_chain_next.py`（已 detached 运行，判据 = checkpoint done 覆盖上述 4 集）→
`WQB_CAMPAIGN_REGION=IND tools/campaign_supervisor.py --datasets fund_holdings_panel,shortinterest3,sentiment27,sentiment7 --min-cov 0.35 --require-ten-years --max-inflight 2`。

选这 4 集的理由（都是**未点亮塔 + 未测过**）：
- `fund_holdings_panel` INSTITUTIONS 18f cov0.89 **alphaCount=0（处女地）**，塔 1/2 差 1；
- `shortinterest3` SHORTINTEREST 12f cov0.87 aCnt29，塔 0/3；
- `sentiment27` SENTIMENT 18f cov0.80 aCnt295、`sentiment7` SENTIMENT 3f cov0.58 aCnt5，塔 0/3。
- 被 cov 门槛挡掉的（cov=0）：`earnings6` / `insiders12` / `institutions25` / `imbalance5` —— 先查字段真实覆盖率再决定是否放宽。

### 8.4 insiders1 ATOM 修复批（已预检通过，待槽位释放后派发）

账户级并发 `config.CONCURRENCY.slots=2`，campaign 常驻占满 2/2 ⇒ **本批不得与 campaign 同时派发**。
设置与 `O0JLn561` 对齐：IND / TOP500 / D1 / STATISTICAL / decay 4 / truncation 0.08 / pasteurization ON / nanHandling OFF。
9 个字段全部 VECTOR（`preflight_expressions` 已确认），表达式已按 `vec_*` 预聚合、`preflight` 返回 `valid=true`、无未知字段：

1. `rank(ts_backfill(vec_avg(insd1_holdings), 60))`
2. `rank(ts_mean(ts_backfill(vec_avg(insd1_holdings), 60), 120))`
3. `rank(ts_mean(ts_backfill(vec_avg(insd1_valueeur), 60), 120))`
4. `rank(ts_mean(ts_backfill(vec_sum(insd1_valueeur), 60), 60))`
5. `rank(ts_delta(ts_mean(ts_backfill(vec_avg(insd1_holdings), 60), 60), 120))`
6. `group_rank(ts_mean(ts_backfill(vec_avg(insd1_valueeur), 60), 120), subindustry)`
7. `rank(ts_zscore(ts_mean(ts_backfill(vec_avg(insd1_tradesignificance), 60), 60), 252))`
8. `rank(ts_mean(ts_backfill(vec_avg(insd1_holdings), 60), 250) / (1 + ts_mean(ts_backfill(vec_avg(insd1_shares), 60), 250)))`

目的：把 124.6% 换手压到 ≤40%、CW 0.256 压到 <0.1，同时保住 ATOM 与 prod 0.178 的余量。
派发后按 `FAILED`/`CANCELLED` 归一 ERROR、零交易出 sentinel 行的既有纪律收割（`cache/_harvest_safe.py`）。

## 九、ATOM 口径（官方锚定）与交付优先级（2026-10-26 用户指令）

> 触发：用户要求「查平台论坛和官方对 ATOM 的定义和说法，纠正项目口径并遵守；因子挖出来后优先给 ATOM，其他只作备选」。

### 9.1 官方原文（不是论坛经验，是平台文档）

来源：`get_documentation_page("single-dataset-alphas")`，标题 **"❗ Single Dataset Alphas"**，
`category=Creating Alphas`、`sequence=150`、`lastModified=2026-09-18`。两条属性逐字引用：

> ①「Single Dataset Alphas must utilize data fields from **only one dataset**, with exceptions for the
> following **6 permitted grouping fields** – country, exchange, market, sector, industry and subindustry.」
>
> ②「The use of **`inst_pnl()` and `convert()`** operators is considered as utilizing the **pv1** dataset
> since these operators rely on pv1 data for calculations.」

放宽的提交条件（同页）：

> 「These Alphas don't need to pass the **IS Ladder Sharpe Test**. Instead, only the **last two year Avg IS
> Sharpe** of the Alpha must clear the following thresholds」——文档表：**Delay-1 = 2.38 / Delay-0 = 3.96**；
> 「If the turnover of Alpha is less than 30%, the IS Sharpe Ladder PASS_THRESHOLDS are multiplied by a factor of 0.85.」
> 平台在 IS Testing Status 里会写「2 year Sharpe of `<value>` is below/above cutoff of `<limit>`」。

**"ATOM" 这个词本身不是平台术语**：平台叫 **Single Dataset Alpha**；"ATOM" 是论坛高赞帖
MH33574《【新人科普】BRAIN 平台上的四类 Alpha（RA, ATOM, PPAC, SA）》(199 赞) 的简称。
⇒ 以后写"ATOM"时，判据一律回指上面那两条原文，不要引论坛转述。

⚠ **文档表 2.38 / 3.96 与平台实际回报的 limit 不一致（本轮再次实证）**：IND/D1 的 `O0JLn561`
（`ts_scale(vec_avg(insd1_holdings), 504)`，单数据集 insiders1、无 pv1 字段）的 checks 里是
**`LOW_2Y_SHARPE` PASS**，而它 `two_year_sharpe = 1.73` ⇒ 实线 ≤ 1.73，绝不是 2.38。
**裁决：以平台 `checks` 里回报的 value/limit 为准**，本文档表格只当全局缺省；本区沿用
`config.PLATFORM_CHECK_LINES`（1.58）。

### 9.2 项目口径的三处纠正（已改代码，不是只改文档）

| # | 旧口径 | 纠正后 |
|---|---|---|
| a | 基础行情（returns/close/cap…）记为**伪数据集 `BASE_MARKET`** | 基础行情属 **`pv1`** 数据集 ⇒ `pv1 字段 + returns` 是**同一数据集**，仍是 ATOM（旧写法会误判 combined） |
| b | 只看字段，**不看算子** | `inst_pnl()` / `convert()` **视为引用 pv1**（官方明文）⇒ 非 pv1 集上用了即破 ATOM（旧写法假阳） |
| c | 豁免分组键含 `region`/`asset`/`group`/`supersector`… | 官方**恰好 6 个**：`country` / `exchange` / `market` / `sector` / `industry` / `subindustry`；多写的不豁免（若数据集恰有同名字段，旧写法会把它当豁免） |
| d | 按**模板族**判：`res`/`reslag`/`pp` 一律不算 ATOM | 那是**代理，不是判据**。判据是字段级 dataset id 唯一。`res`/`reslag` 通常因为吃 `returns` 才破 ATOM，`pp` 继承底座——**一律以字段为准**，模板族只作发批前的预警标签 |

实现（单一口径源）：`src/wqb/expression/atom.py::classify_atom`（纯函数）；
批量重算库内标记：`python tools/atom_labeler.py --backfill --apply`。
回归：`tests/unit/01_store_db/test_atom_labeler.py`（含 a/b/c 三条纠正用例、`vector_neut(x, rank(cap))` 破 ATOM 用例）。

### 9.3 平台侧怎么确认一颗候选真是 ATOM（一行判据）

- `get_alpha_details` 的 `checks`：出现 **`LOW_2Y_SHARPE`**、且**没有** `IS_LADDER_SHARPE` ⇒ 平台认它是单数据集；
- `pyramids.effective == 1` 只说明塔归属（同类别跨数据集也能保 1），**不能**单独用来证明 ATOM。

### 9.4 交付优先级（用户明令：ATOM 优先，其他只作备选）

1. 汇报任何候选池，**ATOM 区在前、非 ATOM 备选区在后**，不得混排；每颗必须带 `ATOM` 标签与依据
   （非豁免字段的 dataset id 数 / 是否引 `returns`·`cap`·`inst_pnl`·`convert`）。
2. ATOM 卡 2Y 时，优先用合规三杠杆：**同集换字段换机制 / 6 个豁免分组 / 本集自带 size 字段**
   （`vector_neut(x, rank(cap))` 属破 ATOM，禁用）。
3. 目前本区（截至 12 集 S6）ATOM 台账（**全部用 `get_alpha_details.code` + `checks` 逐颗核实过**，
   `checks` 里出现 `LOW_2Y_SHARPE` 即平台认定单数据集）：

   | 排序 | 数据集 | alpha | 表达式 | S | F | 2Y | sub | 卡在哪 |
   |---:|---|---|---|---:|---:|---:|---:|---|
   | **1** | **insiders1（未点亮，INSIDERS 1/3）** | `O0JLn561` | `ts_scale(vec_avg(insd1_holdings),504)` | **1.19** | 0.34 | **1.73** | 0.74 | F / TO 124.6% / CW 0.256 |
   | 2 | sentiment21（已点亮） | `akVmz2P6` | `rank(ts_backfill(snt21_4neut_min,22))` | 1.12 | 0.39 | **0.02** | 0.17 | 2Y 已死（ATOM 线就是 2Y） |
   | 3 | earnings11（未点亮，EARNINGS 差颗） | `xA1Lv9KW` | `ts_rank(vec_avg(ern11_document_sentiment),504)` | 0.94 | 0.22 | 0.95 | 0.93 | S/F/TO 126% |
   | 4 | risk70（已点亮） | `pwv2bQZg` | `rank(ts_backfill(hedge_fund_number_owners,22))` | 0.58 | 0.24 | **1.54**（差 0.04） | **0.00** | S/sub 双死，2Y 只差 0.04 但救不动前两项 |
   | 5 | fundamental93（已点亮） | `3qjKQ07e` | `multiply(rank(ts_mean(...fnd93_liability_d1_length...)))` | 0.58 | 0.24 | 0.64 | −0.46 | 全面不足 |

   **非 ATOM 备选（不得与上表混排）**：risk70 的 9 颗近闸全是 `res`/`reslag`/`pp` ——
   实测 `0mjV1N68`（S 4.74 / 2Y 5.25）表达式含 `returns` + `apacm6_total_market_cap_usd`
   ⇒ 两个数据集，`checks` 里是 `IS_LADDER_SHARPE`、`pyramids.effective=2`（RISK+PV），**平台也判它 RA**。
   option1 `gJWlvd0v`（S 2.90 / 2Y 0.00、只有 7 年）已被十年规则排除。
4. 非 ATOM（`res`/`reslag`/`pp`/跨数据集）只能进备选区，且**不得用加权混信号**（`atom_workflow_and_attribution_20261013.md` §8.9 硬禁）。
5. **每波收割后第一件事**：按上表格式出一份「ATOM 优先」候选单 —— 不要只说"最高 Sharpe"，
   因为本区最高 Sharpe（4.74）恰恰是非 ATOM。

### 9.5 ATOM 路线实证更新（2026-10-26，campaign fundamental90 / risk68 双集）

**塔位现状（`campaign_intel pyramid --region IND --delay 1`）**：已点亮 5/15
（analyst / model / news / other / pv）；未点亮 10，按"差几颗"排序：
**fundamental 差 1、macro 差 1**；earnings / institutions / risk 各差 2；
option / sentiment / insiders / imbalance / shortinterest 各差 3。

**单数据集 ATOM 在两座未点亮塔上全灭，且死因一致**：

| 数据集 | 纯数据集 ATOM 最好 | 死因 | 唯一全闸通过者（非 ATOM） |
|---|---|---|---|
| fundamental90 | `zqrVzQ0E` S1.28 / TO 0.064 | **LOW_ROBUST_UNIVERSE_SHARPE 0.17**（limit 1） | `MP0rlg59` S1.77/F1.34，`returns`×fnd90，仅差 IS_LADDER 0.04 |
| risk68 | 纯 `rsk68_*` S −4.35～0.27 | **每颗都带 LOW_ROBUST_UNIVERSE_SHARPE FAIL** | `A1QAgJzW` S5.05/F2.74，`returns`×rsk68，**TO 0.8332 硬 FAIL** |

结论：**会计/风险因子 level 类数据集的 alpha 边际来自 `returns` 腿，数据集只作条件变量**；
这类集合不要再作为 ATOM 目标集投入（fundamental23/94 同族，预期相同）。
ATOM 产出应集中到自带时间结构的单数据集，以及台账里唯一已实证可行的
**`intraday_pv_feats` 降换手路线**（`A1NJVm3e` 0.4722 / `WjbwO0Gk` 0.464 / `vRjoZW6Q` 0.478
→ 目标 TO ≤ 0.40；同族 prod 墙风险高，修复后必须实测 prod）。
详见 `reports/robustness_20261026.md` §5–§6.2。

#### 9.5.1 fundamental23 补齐（2026-10-26 04:05 收波）：ATOM 第三集全灭 + 找到同族降换手配方

fnd23 的 16 个字段中 13 个无概念（全为 other / level 型会计科目）。纯 ATOM 9 颗
（`if_else` 分位条件式）**全部为负**：S −0.02～−0.83、2Y 缺失 ⇒ 与 fnd90 / rsk68 同因，
**会计/风险 level 类 singleton 已连续三集全灭，不要再投 ATOM 波次**。

同一 `rank(-ts_regression(ts_zscore(returns,252), ts_zscore(<field>,252),252,rettype=0))` 结构，
差别只在 **decay 与外壳**，结果差一个量级：

| alpha | 字段 | decay / 外壳 | S | F | TO | RA |
|---|---|---|---|---|---|---|
| `npAENWJd` | voting_beneficial_equity_shares | 4 / `signed_power(...,0.7)` | 5.02 | 2.72 | 0.8253 | HIGH_TURNOVER FAIL |
| `qMER6Y2E` | voting_beneficial_equity_shares | **126 / 裸 rank** | **2.75** | **2.04** | **0.2387** | **failed_ra=0** |
| `YPxevMdw` | share_dividend_equity | 4 / `signed_power(...,0.7)` | 4.88 | 2.58 | 0.8110 | HIGH_TURNOVER FAIL |
| `E5Vde8nL` | share_dividend_equity | **126 / 裸 rank** | **2.56** | **1.86** | **0.2268** | **failed_ra=0** |

**降换手配方（同族通用，非 ATOM 备选区）**：`decay 4 → 126` + **去掉 `signed_power(...,0.7)` 外壳**
（只留 `rank`）⇒ TO 0.83 → 0.23（−72%），S 仍 2.56~2.75。两颗均十年（2014–2023）、
2Y 2.34 / 2.36、robust 1.45 / 1.63、sub 1.33 / 1.70、margin 11.0 / 10.6 bp；
**prod 实测 0.6127 / 0.5525**（均过 0.7 红线）；SELF 未测（需在提交规划时按同族互相关一并核）。
**立即套用到另外两集**：`A1QAgJzW`（rsk68，S5.05 / TO0.8332）与 `MP0rlg59`
（fnd90，S1.77 / 差 IS_LADDER 0.04）先按此配方重跑再判生死，不要直接判死。
两颗均为 PV+FUNDAMENTAL 双塔（`effective=2`），提交可同时计入 FUNDAMENTAL 塔（差 1 颗）。

#### 9.5.2 fundamental94 收波（2026-10-26 05:1x）：第四集 ATOM 同因死；非 ATOM 同族一次 8 颗 RA 全过

**ATOM 侧（纯 fnd94，53 条命中里 11 条）**：最好 `qMERWwY2` / `6XAkr2oE`
（`ts_rank(ts_backfill(fnd94_q_q_qipspe|qxpspe,252),504)`）S **1.62** / F1.14 / TO 0.075，
唯一 FAIL = **LOW_ROBUST_UNIVERSE_SHARPE**；`ts_scale` 变体 1.39–1.41 同 FAIL；其余 <1.0。
⇒ **四集（fnd90 / rsk68 / fnd23 / fnd94）ATOM 全部同因死**：level / ratio 型会计科目的
单字段信号在 TOP500 子宇宙不稳健，这不是个别数据集的问题，而是该类字段的结构性上限。

**非 ATOM 侧：`decay 126 + 裸 rank` 配方批量生效，一次出 8 颗 RA 全过**：

| alpha | 字段 | S | F | TO |
|---|---|---|---|---|
| `3qjNodeX` | fnd94_q_q_qta | 2.74 | 2.01 | 0.2435 |
| `N1eZNMRE` | fnd94_q_ppentq_q | 2.73 | 1.99 | 0.2381 |
| `akVpK3pv` | ts_delay(qta,21) | 2.60 | 1.86 | 0.2445 |
| `O0J3Av3p` | ts_delay(ppentq,21) | 2.59 | 1.84 | 0.2412 |
| `d5KGWqZE` | fnd94_q_q_qipspe | 2.45 | 1.73 | 0.2349 |
| `zqrV3aNX` | fnd94_q_q_qxpspe | 2.37 | 1.64 | 0.2345 |
| `MP0rYArn` | ts_delay(qipspe,21) | 2.11 | 1.39 | 0.2383 |
| `88vwRqwv` | ts_delay(qxpspe,21) | 2.07 | 1.35 | 0.2378 |

（同结构 `decay 4 + signed_power(...,0.7)` 版本一律 S≈4.9 / TO≈0.83 硬 FAIL，如 `YPxe15Ro`。）

⚠ **同族互相关是这条线唯一的致命风险**：以上 8 颗 + fnd23 的 `qMER6Y2E` / `E5Vde8nL` +
fnd90 的 `MP0rlg59` + rsk68 的 `A1QAgJzW` **共享同一 alpha 空间**
（都是 `rank(-ts_regression(ts_zscore(returns,252), ts_zscore(<level field>,252),252))`），
彼此相关性预计 >0.9。⇒ 提交规划只能取 1–2 颗代表，**必须实测彼此互相关 + prod + self**，
不能按"8 颗都能提交"理解。ATOM 路线仍只剩 `intraday_pv_feats` 降换手三颗。

### 9.6 第四波启动事故与「数据集可跑性」三条硬前置（2026-10-26 05:30 修正）

**事故**：05:21 接力脚本打印 `[chain] launch fund_holdings_panel,shortinterest3,sentiment27,sentiment7` 后
无声结束——`ind_r*` 进程数 0。两个独立成因叠加：

1. **入口路径写错**：接力脚本指向 `tools/campaign_supervisor.py`，该文件**不存在**（托管器早已搬到技能目录）。
   detached 启动把 stdout/stderr 全丢 DEVNULL ⇒ 「python 起来又秒退」被吞成一行成功日志。
   **正确入口只有一个**：`Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/ind_runner.py`
   （区域硬钉 IND、自带 `InstanceLock` 单实例、日志 `logs/campaign_sup_IND_<YYYYMMDD_HHMM>.log`）。
2. **数据集名不在目录里**：那 4 个名字在 `dataset_profile` 中**查无此集** ⇒ campaign 解析出 0 个集，
   打印 `[campaign] 数据集总数 0` 后正常退出。

**可跑性三条硬前置**（`all_datasets` + 主循环实测，缺一条即 0 集/SKIP）：

| # | 判据 | 代码位置 | 反例 |
|---|---|---|---|
| 1 | 集名必须出现在 `dataset_profile(region='IND')` | `campaign_semantics.all_datasets` | `fund_holdings_panel` / `shortinterest3` / `sentiment27` / `sentiment7` 全部不存在 |
| 2 | `n_fields >= 3` | 同上（SQL 里写死） | `fundamental22`(2) / `risk88`(1) / `insiders5`(1) 被直接排除 |
| 3 | `avg_field_coverage >= --min-cov`（0.35）且字段级覆盖率达标 | `pipeline_ind` 主循环 + `select_fields` | `fundamental25`(0.30) 会被 `SKIP` |

⚠ **`datasets` 表与 `dataset_profile` 表不是同一回事**：名字先在 `datasets` 里存在、但没进
`dataset_profile`（无字段画像），campaign **一样跑不了**。选集只认后者。

**自查一条命令**（只读）：`mcp__wqb-db__query_dataset_profile(region="IND")` —— 列的
`n_fields / avg_field_coverage / alpha_count` 直接对应上表三条判据；拿不到 MCP 时读
`data/wqb.db` 的 `dataset_profile` 表同样口径（**不要**改读 `datasets` 表）。

**当前实况（05:30 起）**：第四波实跑 `earnings6`（9 个代表字段 × 模板族 = 48 条已派发，14 族未覆盖），
`logs/_tmp_chain_wave5.py` 在其收波后接力 `institutions6,fundamental44,earnings3,fundamental86`
（四个都满足上表三条；INSTITUTIONS / EARNINGS / FUNDAMENTAL 均为未点亮塔）。
未点亮塔里 `IMBALANCE / MACRO / SENTIMENT / SHORTINTEREST / OPTION` 已无「n_fields>=3」的可用集
（`imbalance5` 2 字段、`macro63` 1 字段），故本区剩余可挖面就是上表这几集 + 已判死的 fundamental 族。

⚠ **进程计数会翻倍**：本机 venv python 是 wrapper→real 两段式，`ind_runner`/`ind_main` 各出现两个 PID 属正常；
判「是否双实例」看 `cache/lane_IND_supervisor.lock` 里的 PID 是否等于真实 runner 的 PID（当前 40028）。

### 9.7 全模板 campaign 收尾：21 集终表 + ATOM 728 颗零通过（2026-10-26 09:5x 实测）

> 数据源：`results/full_template_campaign_results_IND.json`（21 键）+ `logs/campaign_sup_IND_20261026_0633.log`（done=21/21）。
> 台账键：`IND/campaign_21_datasets_20261026`。**§8.1 的 12 集表是中途快照，以本节为终。**

**总账**：`done=21/21`｜`ALIVE 8 / DEAD 10 / BORDERLINE 1 / INSUFFICIENT_HISTORY 1 / NO_DATA 1`｜
`deliverable=true` 仅 **4 集**：`earnings3` / `fundamental44` / `fundamental94` / `institutions6`
（四集 `prod_top` 均 <0.7：0.6614 / 0.6112 / 0.6766 / 0.677）。

| 数据集 | 类目 | cov | 字段 | alphas | max_s | max_2Y | n_joint | **ATOM 最高** | prod_top | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| risk68 | RISK | 0.98 | 5 | 52 | 5.05 | 6.40 | 14 | **0.27** | — | ALIVE |
| fundamental23 | FUND | 0.89 | 39 | 80 | 5.02 | 4.99 | 10 | **1.16** | — | ALIVE |
| institutions6 | INST | 0.99 | 11 | 51 | 5.00 | 5.39 | 14 | 0.95 | **0.677** | ALIVE ✅ |
| fundamental94 | FUND | 0.93 | 38 | 83 | 4.93 | 5.25 | 12 | **1.62** | **0.6766** | ALIVE ✅ |
| risk70 | RISK | 1.00 | 35 | 55 | 4.74 | 5.25 | 9 | 0.58 | — | ALIVE |
| fundamental90 | FUND | 0.72 | 65 | 95 | 3.45 | 4.53 | 8 | **1.28** | — | ALIVE |
| fundamental44 | FUND | 0.78 | 12 | 65 | 3.10 | 5.07 | 11 | 1.17 | **0.6112** | ALIVE ✅ |
| earnings3 | EARN | 0.79 | 8 | 76 | 5.20 | 5.30 | 10 | 0.57 | **0.6614** | ALIVE ✅ |
| fundamental86 | FUND | 0.80 | 7 | 44 | 2.97 | 2.46 | 0 | **2.92** | **0.8382** | BORDERLINE |
| insiders1 | INSD | 0.39 | 9 | 48 | 1.20 | 2.00 | 0 | 1.19 | 0.1777 | DEAD |
| sentiment21 | SENT | 0.97 | 105 | 38 | 1.12 | 2.16 | 0 | 1.12 | — | DEAD |
| earnings11 | EARN | 0.50 | 35 | 62 | 0.98 | 1.37 | 0 | 0.94 | — | DEAD |
| earnings6 | EARN | 0.36 | 20 | 79 | 0.98 | 1.46 | 0 | 0.98 | — | DEAD |
| news_sentiment_transfer | NEWS | 0.94 | 23 | 33 | 0.72 | 0.57 | 0 | 0.72 | — | DEAD |
| fundamental93 | FUND | 0.54 | 32 | 19 | 0.58 | 0.92 | 0 | 0.58 | — | DEAD |
| sentiment23 | SENT | 0.70 | 105 | 48 | 0.49 | 0.68 | 0 | 0.49 | — | DEAD |
| sentiment26 | SENT | 0.53 | 18 | 36 | 0.40 | 1.00 | 0 | 0.40 | — | DEAD |
| fundamental1 | FUND | 0.56 | 118 | 69 | 0.19 | 1.05 | 0 | 0.19 | — | DEAD |
| option30 | OPT | 0.36 | 12 | 26 | 0.18 | 0.28 | 0 | 0.18 | — | DEAD |
| option1 | OPT | 0.40 | 28 | 56 | 2.90 | 0.00 | 0 | 2.90 | — | INSUFFICIENT |
| shortinterest5 | SHORT | 1.00 | 3 | 0 | — | — | 0 | — | — | NO_DATA |

- **十年要求已核**：所有 ALIVE 集 `year_profile = n_years 10 / first_year 2014 / fragile false`（含 4 个 deliverable）。
  唯一例外 `option1` 持仓只有 2017 一年（`n_years=1 / fragile=true`）⇒ `--require-ten-years` 判 INSUFFICIENT **正确**（僵尸数据）。
- `fundamental86` 的 `prod_top=0.8382` 已越 0.7 红线 ⇒ 即使 ATOM 指标最好也**不可提交**，`deliverable=false`。

**ATOM 侧：728 颗 ATOM 模板 alpha，四道数值闸通过 0 颗。**

```
atom_tpl_alphas = 728        # per_template ∈ {lvl_rk,lvl_zs,lvl_qt,lvl_tr,lvl_sc,d1_rk,d1_va,d2_rk,ed_rk,ir_pl,lvl_qc,d2_qc,dw,rep}
atom_tpl_pass_4gates = 0     # S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥1.0
```

> ⚠ **分类口径**：`results` JSON 的 alpha 条目只有 `{alpha,tpl,s,f,y2,sub,batch}`、**没有 code**，
> 且 `data/operators_verified.json` 在本仓不存在（真实路径是 `research-data/operators_platform_*.json`）
> ⇒ 表达式级 token 分类跑不通（首版把 1115 条全判成 ATOM 是无效结果）。
> 有效分类器只能是 **`tpl` 模板名**（ATOM 形 = 14 个模板，残差形 = `res/reslag/pp`，后者必含 `returns`）。
> 单颗确认仍走平台：`get_alpha_details().pyramids.effective == 1`。

**两颗最好的真 ATOM（均 `pyramids.effective=1`，均已用 `get_alpha_details().code` 核对表达式）**：

| alpha | 数据集 | 表达式 | decay | S | F | TO | 2Y | sub | **robust** | RA 唯一 FAIL |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `GrgRj9mZ` | fundamental86 | `rank(ts_decay_linear(ts_backfill(fnd86_average_score,252),63))` | 4 | 2.92 | 2.87 | 0.0684 | 2.37 | 0.92† | **0.53** | `LOW_ROBUST_UNIVERSE_SHARPE` |
| `LL5QVGR6` | fundamental94 | `ts_quantile(ts_backfill(fnd94_q_q_qxpspe,252),504)` | 4 | 1.62 | 1.17 | 0.085 | 1.77 | 0.72 | **0.41** | `LOW_ROBUST_UNIVERSE_SHARPE` |

†`GrgRj9mZ` 的 `sub=0.92` 低于本仓 campaign 的 1.0 口径（故计入"四闸未过"），但平台 RA 只报 robust 一项 FAIL
⇒ 两个口径分开说，别混成"平台四闸都没过"。

**结论（与 §9.5 / §9.5.1 / §9.5.2 / `reports/robustness_20261026.md` §7 合并成一条）**：
**IND 的 ATOM 是双墙，两端都已实测封死**。

1. **未点亮塔（会计/风险 level 类）→ robust 墙**：fnd90 / rsk68 / fnd23 / fnd94 / fnd86 五集
   纯 ATOM 同因死，robust **0.41–0.53 < 1.0**。这是 level / ratio 型单字段在 TOP500 子宇宙的
   结构性上限，不是参数没调好 ⇒ **不送 repair**。
2. **已点亮塔（PV 价量反转）→ prod 墙**：`leMm5QRO` / `1YjMln26` / `P0MVx2oW` 三颗经
   `ts_target_tvr_hump` 修好换手（TO 0.31–0.33）、RA **零 FAIL**、十年齐备，但 prod
   **0.8636 / 0.8757 / 0.8379** 全部越 0.7 红线（`[0.7,0.8)` 桶 n=8/6/7，按族级判据**不可救**）。
   ⇒ 「`intraday_pv_feats` 降换手三颗」这条唯一 ATOM 路线**已证伪**，不要再投入。

**IND 现在没有可提交的 ATOM**。要拿到 ATOM 只能换信号概念/数据集类（不同机制、未被已提交池占据），
或者接受非 ATOM 组腿（§9.7 上表 4 个 deliverable 集全部走 `returns` 残差口径）。

**定向挖掘唯一产出：earnings3 ladder 修复（残差口径，非 ATOM）**

本轮「对近闸候选定向挖掘」的高价值目标只有 earnings3（当季塔 1/3，其余未点亮塔已无近闸候选）。
修复钥匙 = **`decay 4 → 126` + `group_rank(..., industry|subindustry)` 分组**：

| alpha | S | F | TO | margin | 2Y | sub | robust | RA | prod | self |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| `vROWRWrz` | 2.25 | 1.56 | 0.2234 | 9.67 bp | 2.10 | 1.64 | 1.36 | failed=0 | **0.5527** | **0.3432** |
| `VkdAkAa0` | 2.04 | — | — | — | 2.24 | — | 1.42 | failed=0 | **0.5687** | **0.3004** |

两颗均 **`pyramids.effective=2`（PV returns × earnings3）⇒ 非 ATOM**，只能作 EARNINGS 塔的组腿备份；
台账 `IND/robustness_vROWRWrz` / `robustness_VkdAkAa0`，波次 252（PASS）。
⚠ 旧写法 `decay 4 + signed_power(...,0.7)` 同族是 **TO 0.81 硬 FAIL**（wave 253 反模式）；
`ts_target_tvr_hump` 救不了快信号（decay 4 下 target 0.30/0.25 → 2Y 掉到 0.01–1.44）。

**并发与未派发**：本轮全程 `--max-inflight 2` 遵守账户级 2 槽。earnings3 ladder 修复批 C
（`logs/_tmp_earn3_ladderC.txt`，10 行）**至今未派发** —— 并行 campaign
（`logs/campaign_sup_20261026_0219.log`，26 集）常驻占满 2/2；早前返回的 multisim id
`2lON8AdSx4p1c1CiKkpl9n3` 实测 `batch_status` 0 子任务 + `get_alpha_details` 404 ⇒ **从未创建**（429 吞掉）。
**本区未提交任何 alpha**，全部候选等用户明确确认。

### 9.8 ATOM 728 颗为何全灭：三层死因 + 全部高 Sharpe 都在 returns 残差（2026-10-26 10:2x 归因）

> 数据源：`results/full_template_campaign_results_IND.json`（全 1115 颗）+ 平台 `GET /alphas/{id}`
> 批量实测 10 颗（含 `robust_universe_sharpe` / `checks` / `pyramids`）。模板体见
> `tools/full_template_campaign.py:120-155`（`L1_EXTRACT` × `L2_NORM` + `FREQ_WIN`）。

**第 1 层 —— level 族在 18/20 个集里连 S 线都摸不到（不是差一点，是没有信号）**

| 口径 | 数 |
|---|---|
| ATOM 模板 alpha（14 模板） | 728（其中 `lvl_*` 448 = 61.5%） |
| S < 0 | **362（49.7%）** |
| S = 0 | 86 |
| 0 < S < 0.5 | 180 |
| S ≥ 1.58（平台 S 线） | **11（1.5%）** |
| 全 728 颗 Sharpe 中位数 | **0.00** |
| level 族「每集最高 S ≥ 1.58」的集数 | **2 / 20**（fnd86 2.64、fnd94 1.62；其余 18 集 ≤ 1.28） |

⇒ 多数集的问题不是闸位，而是**单字段会计/风险水平量在 IND TOP500 没有方向性 alpha**。

**第 2 层 —— 摸到 S 线的 7 颗，全部只差 `LOW_ROBUST_UNIVERSE_SHARPE`（平台实测）**

| alpha | 集 | tpl | S | F | 2Y | sub | **robust** | robust/S | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `GrgRj9mZ` | fundamental86 | rep | 2.92 | 2.87 | 2.37 | 0.92 | **0.53** | 18% | 1 |
| `88vwWlN7` | fundamental86 | lvl_rk | 2.06 | 1.59 | 2.03 | 0.67 | **0.76** | 37% | 1 |
| `LL5QVGR6` | fundamental94 | lvl_qt | 1.62 | 1.17 | 1.77 | 0.72 | **0.41** | 25% | 1 |
| `kqJAEPK6` | fundamental94 | lvl_qt | 1.62 | 1.16 | 1.72 | 0.71 | **0.44** | 27% | 1 |
| `6XAkr2oE` | fundamental94 | lvl_tr | 1.62 | 1.14 | 1.80 | 0.71 | **0.42** | 26% | 1 |
| `qMERWwY2` | fundamental94 | lvl_tr | 1.62 | 1.14 | 1.79 | 0.71 | **0.45** | 28% | 1 |
| `xA1ZOwRW` | fundamental94 | lvl_zs | 1.61 | 1.19 | 1.75 | 0.84 | **0.62** | 39% | 1 |

阈值算术：robust 线**固定 1.0**、S 线 1.58 ⇒ 等价于要求 **robust/S ≥ 0.63**（或基数够高：S ≥ 2.7 时保留 ≥ 37%）。
这 7 颗保留率 18%–39%，**结构性不够**，不是调参能补的零头。

**第 3 层 —— 本轮模板库没有破 robust 的几何**

模板体 = `L2_NORM(L1_EXTRACT(field))`：L1 只有 `ts_backfill / ts_delta / ts_decay_linear(…,252),63) / ts_ir`，
L2 只有 `rank / ts_zscore / ts_quantile / ts_rank / ts_scale`；`FREQ_WIN` 对 quarterly/annual 把 **BF 定 252**。
**全过程没有 group 算子**。而 fnd86 史册的唯一有效杠杆（短 bf、`group_rank(·, sector)`、连续 z 上 `signed_power(·,3)`）
一个都没进来；`pp` 电池只套在「每集最佳构造」上，且用的是 `signed_power(code, 0.7)`（**凹**，实证有效方向是 ≥1.5 **凸**）。
叠加 CW 与 robust 同谱互斥（fnd86 上限 0.99）、IND 9 档中性化全劣化 ⇒ 这套几何被锁在失败角。

**第 3 层已处置（2026-10-26）**：引擎 `wqb_campaign/generate.py` 的 robust 几何族由 7 条扩到 11 条，
新增的正是上面缺的三把钥匙中可复用的两条半：

| 模板 | 结构 | 平台实证（IND/TOP500/D1/STATISTICAL） |
|---|---|---|
| `rg_grdev_p3` | `signed_power(subtract(group_rank(dev, industry), 0.5), 3)` | analyst_consensus decay6 → S1.53 F1.11 2Y1.95 sub1.48 **rob1.24** CW PASS prod **0.4486** self 0.3994；唯一 FAIL `LOW_SHARPE` 1.53 vs 1.58 |
| `rg_grdev_p3_sec` | 同几何，分组轴 industry→**sector** | analyst_consensus decay6 → S**1.64** F1.27 TO0.1142 2Y**2.23** sub**1.55** rob**1.12** CW PASS prod **0.5354** self 0.4843，`checks.fail=[]` ⇒ **全闸 pass**（成品 `58jPrvZ1`） |
| `rg_lvvol` | `rank(ts_mean(ts_backfill(F·(1+ts_std_dev(F,65)), 22), 5))` | fnd86 → S2.18 F1.75 2Y2.03 **rob1.06**，但 CW WARNING |
| `rg_lvvol_sec` | 上式套 `group_rank(·, sector)` | fnd86 → S2.10 F1.65 2Y1.97 sub0.90 **rob0.99** **CW PASS** prod **0.6989**；唯一 FAIL `LOW_ROBUST` 0.99 vs 1.00 |

两条对照定死了因果，别再退回旧几何：

- **居中再凸**才是 robust 的钥匙。同族不居中的 `group_rank(dev, industry)`（`A1NJqbPw`）S **1.73** 但 rob **0.77**；
  居中外加凸幂后 S 降到 1.49–1.53、rob 升到 1.22–1.24。S/rob 是明确的对价，不是调参噪声。
- **除以 |ts_mean| 的 dev** 才是 prod 的钥匙。z 版 `group_rank(ts_zscore(·,252), sector)` 同族 prod **0.7672 ✗**，
  dev 版 0.6709–0.6989 ✓；代价是 dev 形式算子调用点 10（+居中凸 12），已按 `rg_grdev_p3` 单模板例外登记，
  理由：REGULAR 无算子数硬上限，成品 `MP0JYmL8` 平台 FULL 仿真通过。
- **CW 与 robust 不是同谱互斥，是 backfill 位置互斥**：两者之差只在 `ts_backfill(22)` 打在乘积上还是字段上
  （21/21 fnd86 成品核对：bf22 ⇒ CW PASS；无 bf / bf5 / bf66 ⇒ WARNING）。sector 分组同时补 rob（+0.04）与 prod（−0.0117），
  所以「bf22 + sector」是目前唯一的交集点，rob 只差 0.01。

**★ 第 3 层收口：fnd86 ATOM 全闸通过成品 `gJWnrZgg`（2026-10-26，平台实测）**

```
group_rank(ts_mean(ts_backfill(multiply(fnd86_earnings_score,
            add(ts_std_dev(fnd86_earnings_score, 65), 1)), 22), 2), sector)
```
IND/TOP500/D1 · decay **2** · STATISTICAL · trunc 0.08 · 2014-01-01→2023-12-31 · nanHandling OFF

| 指标 | 值 | 闸 |
|---|---|---|
| S / F | 2.14 / 1.70 | 1.58 / 1.00 ✓ |
| Turnover | 0.1072 | ≤0.40 ✓ |
| 2Y Sharpe | 1.99 | ≥1.58 ✓ |
| sub / robust | 0.93 / **1.02** | ✓ / ≥1.00 ✓（余量 0.02） |
| CW | PASS | ✓ |
| prod / self | **0.6998** / 0.4478 | <0.70 ✓ / ✓（`all_passed=true`） |
| pyramid | IND/D1/FUNDAMENTAL ×1.2，effective **1** | ATOM ✓ |
| `checks.fail` | `[]`（`failed_ra_count=0`） | 零 FAIL |

**平滑长度是刀锋，只有 s=2 落在双闸交汇点**——同一几何只改 `ts_mean` 的 N（decay 2 固定）：

| N | 0（无平滑） | **2** | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| robust | 1.05 | **1.02** | 0.98 | 0.97 | 0.99 |
| prod | 0.7056 ✗ | **0.6998 ✓** | — | — | 0.6989 ✓ |
| S | 2.18 | 2.14 | 2.11 | 2.08 | 2.10 |

⇒ rob 与 prod 沿同一根旋钮**反向**移动、且交叉点几乎重合；N=2 是唯一同时过线的整数点。
副产物：把 bf 从 22 挪到 30（不顺滑）rob 1.04 但 prod **0.7057 ✗** ⇒ bf 位置不是 prod 杠杆，平滑长度是。
逐年 10/10 为正（最差 2016 S1.20，最好 2015 S3.23），换手 0.103–0.114 十年稳定，多空 250/245 平衡。

⇒ 第 3 层的「结构上锁死」结论**不再成立**：两条线都只剩 0.01–0.05 的零头，且余量项各不相同
（analyst 差 S 0.05 而 prod 富余 0.25；fnd86 差 rob 0.01 而 S 富余 0.52）。

**★ analyst 线同日收口：`58jPrvZ1` 全闸 pass（ATOM ANALYST ×1.4）**

`rg_grdev_p3_sec` 同批四臂（decay 6）把「凸幂 × 分组轴」扫完：
industry pow2 → S1.56/rob1.19/sub1.49；industry pow5 → S1.44/rob1.26；`rank` 无分组 pow3 → S1.60/rob1.05/sub1.45；
**sector pow3 → S1.64/rob1.12/sub1.55/2Y2.23**。凸幂 3 是峰值（2 与 5 都掉 S），分组轴 sector 比 industry 全面更优
⇒ 「dev + 居中凸 3 + sector」= 该族最优点，prod 还有 0.165 余量。

**★ 关键对照：本轮所有高 Sharpe 都来自 returns 残差，平台口径不是 ATOM**

抽查 3 颗 S 4.87–5.20 的 `pp` 幸存者，同一条式子：

```
signed_power(rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(<field>, 252), 252, rettype=0)), 0.7)
```

| alpha | 集 | S | TO | robust | pyramids.effective | 唯一 FAIL |
|---|---|---:|---:|---:|---:|---|
| `rKdZK8JJ` | earnings3 | 5.20 | 0.8127 | 2.13 | **2**（PV+EARNINGS） | HIGH_TURNOVER |
| `A1QAgJzW` | risk68 | 5.05 | 0.8332 | 2.28 | **2**（RISK+PV） | HIGH_TURNOVER |
| `RRAgoxQo` | institutions6 | 5.00 | 0.8285 | 2.06 | **2**（INSTITUTIONS+PV） | HIGH_TURNOVER |

⇒ 4 个 `deliverable=true` 集（S 4.9–5.2）**全部由这条回归残差贡献**；同样是这 4 集，ATOM 最高 S 只有
0.57 / 1.17 / 1.62 / 0.95。也就是说：**IND 的收益主体长在 `-returns` 反转上，字段只是被剔除的回归自变量**；
ATOM 约束恰好把这块切掉，剩下的是薄弱的会计水平效应。
⚠ `deliverable` 判定式（`full_template_campaign.py:1770`）只含 S/F/2Y/prod，**不含 sub / robust / RA** ⇒ 不是"可提交"标签。

**ATOM 不是死区：IND 已有两颗 RA 全过的单集动量**

| alpha | 表达式（model32 单集） | S | 2Y | robust | sub | RA | prod |
|---|---|---:|---:|---:|---:|---|---:|
| `RR7v9gV0` | `subtract(ts_backfill(global_momentum_rank_float,66), ts_backfill(industry_momentum_score_float,66))` | 1.83 | 1.69 | **1.08** | 1.07 | 0 fail，**已 ACTIVE** | 0.6837 |
| `RR7vlM2o` | 三腿动量乘积（同集三字段） | 3.31 | 1.98 | **1.24** | 1.64 | 0 fail | 0.8219（墙） |

⇒ 能全过的是**动态信号（动量）+ 短 bf**，不是水平量。另 `option1/gJWlvd0v`（`d1_rk`）S 2.90 / robust 1.43 但
`2Y=0`（只有 2017 一年持仓，僵尸数据）⇒ 十年要求一票否决，与 robust 无关。

**结论与不再做什么**

1. **不再投 fnd / risk 的 level 型 ATOM 波次**：18/20 集天花板 ≤1.28，且 7 颗近闸全灭于 robust 保留率。
2. ATOM 若还要产出，候选必须先满足「自带时间结构（动量 / 修正 / 事件计时）+ bf ≤ 66 + 带 group 轴」，
   发批前先算 `robust/S ≥ 0.63`——算不过就别烧配额。
3. ATOM 之外的 returns 残差组腿路线（S 4.4–5.2）**先解 HIGH_TURNOVER 0.81→≤0.40**，否则一律停在 TO 闸。

### 9.9 未点亮塔清单与 sentiment 双线探针（2026-10-26 11:1x 派发）

**平台口径的未点亮塔（IND / D1，`get_pyramid_alphas` 当季）**：insiders 0、imbalance 0、option 0、
sentiment 0、shortinterest 0；其余 10 塔已点亮（news 4 / other 4 / pv 8 / analyst 3 / model 3 / macro 2 /
fundamental 2 / earnings 1 / risk 1 / institutions 1）。

**逐塔排除依据（查库+死路表，非猜测）**

| 塔 | 数据集 | 判决 | 依据 |
|---|---|---|---|
| insiders | insiders5 | 排除 | 唯一字段 `insd5_nm_kor`="Insider's Korean name"（VECTOR 姓名）⇒ 无信号 |
| insiders | insiders1 | 死路 | `IND-INSIDERS1-NODIRECTION-DEAD`：cov 0.3877、6 条长窗全灭 max 0.68 |
| shortinterest | shortinterest5 | 死路 | `IND-SHORTINTEREST5-PRICEBAND-DEAD`（wave173，7 探针，**family 明确含 `price_limit_condition`**，4 条 sharpe=0/tvr=0）⇒ 不再复测，省配额 |
| option | option30 | 死路 | `IND-OPTION30-OS-SURPRISE-FITNESS-CEILING`：fitness 天花板 ~0.85 结构性 |
| option | option1 | 排除 | `gJWlvd0v` S2.90/robust1.43 但 **2Y=0**（仅 2017 有持仓，僵尸数据）⇒ 十年要求一票否决 |
| imbalance | imbalance5 | **已关闭（wave261）** | 原「暂缓」只凭拥挤度（2 字段、alphaCount 16500）；§9.9.6 补 6 臂实测：三臂 ATOM 形态其余闸全过，唯一未过项均 `LOW_ROBUST_UNIVERSE_SHARPE`（0.69/0.68/0.92 vs 1.0）⇒ 预登记线触发关闭 |
| sentiment | sentiment21 / sentiment26 | **已关闭（wave254–260）** | 见 §9.9.5：44 臂 + 反向，唯一近闸 `fitness 0.84`，窗口/decay/nanHandling 三杠杆实测均无效 |

> **塔位清单已按平台 `get_datasets`（IND/D1/TOP500，2026-10-26 复核）逐类核过**：SENTIMENT 类共 4 集
> （sentiment21/23/26 + news_sentiment_transfer）。`sentiment23`（105 字段、cov 0.70）与
> `news_sentiment_transfer` **不是漏测**——第三波全模板 campaign 覆盖过（§8.1：48 / 33 alphas，
> max S 0.49 / 0.72，均 DEAD）。⚠ `dataset_profile` 缓存里 `sentiment23.n_backtests=0` 是**陈旧读数**，
> 证据是 campaign 结果与 `wave_results tpl_sentiment23_d1`，别据此重开。

**sentiment21 的关键复核（推翻了我原先的构造选择）**：wave172 那 48 条里 S 最高的 4 条**不是**净情感
`pos-neg`，而是**共识强度比 `divide(pos_mean, pos_max)`**（bf5）：module 1/2/4/5 分别
S1.76/1.69/1.74/1.70、F0.61–0.65、**TO 0.5104–0.5105**、2Y1.78–1.93，三条 FAIL 完全一致
（`LOW_FITNESS / HIGH_TURNOVER / LOW_ROBUST`）。四模块指标几乎重合 ⇒ 是同一信号复制，不是四个信号。
⇒ 该族真正待修的就是这三维，而这正是本轮新几何（慢化 + 凸幂）要修的东西。

| 批 | multisim | 臂 | 假设 |
|---|---|---|---|
| A（净情感 2×5） | `1rskr1IT56A9XMUL7ymMUI` | 5 个 provider 模块 × [慢水平 `group_rank(ts_mean(ts_backfill(net,22),66),industry)` / 中心凸 dev `group_rank(sector)`] | 净情感是独立信息轴；若成立，fitness 靠慢化抬 |
| B（sentiment26 关注度） | `3zI5kGbRR4VDbXLO7ZOGDRU` | DNS/Web 关注度 10 臂（neglect 水平 / 关注度变化 / 顶级域排名 / 域数量扩张 / 峰度偏度 / 关注度冲击反转） | 全 VECTOR 但**每日连续**（多域向量≠稀疏事件），IND 从未回测过（0 行） |
| C（比值慢化，待槽位） | 未派发 | `divide(pos_mean,pos_max)` 的慢水平 66/126/252 + 凸 dev 126/252 × sector/industry + 跨模块 + neg 镜像 + `-ts_zscore` | 直接修已知 S1.76 信号的三条 FAIL |

**A/B 批设置**：IND/TOP500/D1/STATISTICAL/decay4/trunc **0.08**/nanHandling OFF/FULL/2014-01-01→2023-12-31。
发批前已过 `expr_lint`（10/10）+ `validate_expressions`（字段零 unknown）+ `preflight_expressions`
（sentiment26 的 `vec_avg` 包裹经平台确认为 no-op，`any_changed=false`）。

**判死线（预先登记，防事后合理化）**：sentiment 两数据集合计 30 臂内若无一条达
**S≥1.4 且 TO≤0.30 且 robust≥1.0**，封 sentiment 塔并写 `seal_dead_end`（证据含本表与两条 multisim）。
反向：若某臂过线但 fitness<1.0，允许一轮 decay/窗口加固（fitness 是慢化的单调受益项），
但**不换信号概念**。

#### 9.9.1 A/B 收割结论 + 派生反向批（2026-10-26 11:2x）

**A 批（wave 254，net emotion 2×5，decay4）—— 慢水平臂全噪声，dev 臂强负**

| alpha | 模块 | 几何 | S | F | TO | 2Y | sub | robust |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `leALrkE8` | 1 | 慢水平 | −0.21 | −0.05 | 0.087 | 1.31 | 0.01 | −0.45 |
| `O0A1oqMY` | 2 | 慢水平 | 0.21 | 0.05 | 0.095 | 1.46 | 0.33 | −0.44 |
| `58EZM3AM` | 3 | 慢水平 | −0.49 | −0.18 | 0.094 | 0.47 | −0.08 | 0.07 |
| `78LkJ0v2` | 4 | 慢水平 | −0.31 | −0.09 | 0.094 | 0.84 | −0.09 | −0.17 |
| `A1VRkYzd` | 5 | 慢水平 | 0.11 | 0.02 | 0.094 | 1.08 | 0.18 | −0.39 |
| `1YNqJ1KJ` | 1 | 中心凸 dev | −1.10 | −0.39 | 0.366 | −1.39 | −0.55 | −0.52 |
| `JjeVbYzW` | 2 | 中心凸 dev | **−1.58** | −0.66 | 0.393 | **−3.40** | −0.99 | **−1.05** |
| `mLoPZJ19` | 3 | 中心凸 dev | 0.21 | 0.03 | 0.391 | 1.54 | 0.29 | 0.39 |
| `9qxzJbm9` | 4 | 中心凸 dev | 0.54 | 0.14 | 0.375 | 1.21 | 0.58 | 0.68 |
| `0mYbz96G` | 5 | 中心凸 dev | **−1.80** | −0.84 | 0.372 | **−2.35** | **−1.25** | **−1.38** |

判读：① **净情感水平量不是信号**（5 臂 |S|≤0.49、robust 全在 ±0.45 内）；② dev 几何下 5 臂中
3 负（m1/m2/m5）2 正（m3/m4 小值），负侧量级远大于正侧 ⇒ **反向才是信号方向**：
m5 反向 = S **1.80** / F 0.84 / TO 0.372 / 2Y **2.35** / sub **1.25** / robust **1.38**（仅 F 未过 1.0）；
m2 反向 = S **1.58** / F 0.66 / TO 0.393 / 2Y **3.40** / sub 0.99 / robust **1.05**（仅 F 未过）。
经济含义 = **情绪过度反应反转**（异常高涨的正面净自信新闻 → 后续跑输），与 IND 已证的反转主导一致，
且是单数据集 ATOM（模块内 pos/neg 同属 sentiment21）。

**B 批（wave 255，sentiment26 DNS 关注度）—— 10 臂全灭**：S 区间 −0.40…+0.37、F ≤0.15、
TO 0.072–0.317、2Y −0.92…+0.61；无任何方向性结构（最好 `JjeVbQ8m` S0.37 但 2Y −0.91）。
⇒ sentiment26（cov 0.5318、此前 0 条回测）判**无信号**，不再投入；该集不需要 `seal_dead_end` 到塔级
（塔级由 sentiment21 的结论统一定夺）。

**C 批已派发**：`1SMyXn6So50c94XGLtKHqU8`（10 臂，ratio `pos_mean/pos_max` 慢水平 66/126/252 +
凸 dev 126/252 × sector/industry + 跨模块 + neg 镜像 + `-ts_zscore`；设置同 A）。

**派生 D 批（反向 dev 加固）**：`48065PeWM4W1aaUblfsTH6`，6 臂，设置与 A 完全一致（decay4/STAT/trunc0.08/
nanHandling OFF/FULL）：
`SIGNED_POWER(SUBTRACT(0.5, GROUP_RANK(dev, AXIS)), 3)`，dev 同 A 式。臂 = m5 smooth 22/66/126（sector）
+ m2 smooth 22/66（sector）+ m5 smooth 22（industry）。靶 = **fitness 0.84→≥1.0** 且 S≥1.58、TO≤0.40、robust≥1.0。

⚠ **口径诚实说明**：反向臂不是预先派发的 30 臂之一，且 TO 0.372 **超过**我预登记的 0.30 质量线
（但仍低于平台 0.40 硬线）。因此这里**不宣布"过线"**，只按预登记的第二条（某臂 S/robust/sub 达标但
fitness<1.0 ⇒ 允许一轮同概念窗口/decay 加固）执行一次。D 若仍达不到 F≥1.0 或 TO 明显恶化 ⇒ 按原判死线封塔。

#### 9.9.2 C 批收割（wave 256）：比值构造慢化后全部弱于 1.1

| alpha | 构造 | S | F | TO | 2Y |
|---|---|---|---:|---:|---:|---:|
| `QPv1EAxQ` | 慢水平 ratio 66 | **1.06** | 0.58 | 0.094 | 1.21 |
| `wpQ8LA06` | 慢水平 ratio 126 | 0.97 | 0.51 | 0.073 | 1.55 |
| `npv1351w` | 慢水平 ratio（模块2） | 0.74 | 0.34 | 0.082 | 1.05 |
| `RREJdwJb` / `P0oJvbVL` | 慢水平 ratio 252 / 模块4 | 0.69 / 0.69 | 0.31 | 0.082 | 0.92 / 0.99 |
| `O0A1oX1d` | 慢水平 neg 镜像 | 0.59 | 0.25 | 0.082 | 0.71 |
| `zq3vOElO` / `1YNqJRrW` / `0mYbzL11` / `WjOE92jk` | 凸 dev 126/252/industry/zscore | 0.42 / 0.53 / 0.48 / −0.38 | ≤0.13 | 0.339–0.380 | 0.29–0.85 |

**判读**：wave172 的 S1.76 是 `divide(ts_backfill(pos_mean,5), ts_backfill(pos_max,5))` **快信号**（TO 0.51）
的产物；一旦按本项目标准几何慢化到 TO 0.07–0.09，S 掉到 ~1.0、F 0.51–0.58，**比原版更远离 fitness 线**。
⇒ 比值构造在「低换手可提交」形态下不成立。C 批 10 臂同样 0 达判死线。

**至此预登记的 30 臂（A10+B10+C10）全部未达 S≥1.4/TO≤0.30/robust≥1.0。**
唯一仍在射程内的是 A 批 dev 的**反向**（派生臂，见 D 批），D 是预登记允许的最后加固轮。

#### 9.9.3 D 批（wave 257，窗口加固）：窗口不动换手，fitness 卡在 0.86

| alpha | 臂 | S | F | TO | 2Y |
|---|---|---|---:|---:|---:|---:|
| `1YNqgaoX` | m5 s22 sector p3（=A 批 0mYbz96G 的镜像） | 1.80 | 0.84 | 0.372 | 2.35 |
| `ZYQRo2j8` | m5 s66 sector p3 | 1.80 | 0.85 | 0.355 | 2.40 |
| `0mYb8ezv` | m5 s126 sector p3 | 1.80 | 0.86 | 0.354 | 2.38 |
| `j2Y5g91Z` | m2 s22 sector p3 | 1.58 | 0.66 | 0.393 | 3.40 |
| `d5W2QEdY` | m2 s66 sector p3 | 1.49 | 0.61 | 0.376 | 3.44 |
| `6XdnEaE7` | m5 s22 **industry** p3 | 1.66 | 0.72 | 0.381 | 1.74 |

**判读**：把基础平滑从 22 拉到 126，S 一点没掉（1.80 三条几乎逐位重合），TO 只从 0.372 降到 0.354，
**fitness 0.84→0.86**。⇒ 该族换手**不由基础字段平滑决定**，由 `signed_power(...,3)` 的极端放大 +
STATISTICAL 中性化的日频重排决定。窗口这条杠杆在此几何上已证无效（这也解释了为何 analyst 族同几何能到
F1.27：analyst 基础字段本身是慢变量，凸幂后换手天然低；sentiment 是日频新闻，凸幂后换手天然高）。

**最后加固轮 = decay 阶梯（同概念，不改几何）**：
`hIqKn2oZ4m7baYspB7CCS1`（decay **126**，6 臂 = m5 s22/s66 sector p3 + m5 s22 industry p3 +
m2 s22 sector p3 + **p 阶消融** m5/m2 的 p1 无凸幂臂）
+ `xQCupfG84nn9EA1bpdQRcrR`（decay **30**，同族 4 条 p3 臂）。
这是**真正的最后一轮**：若 decay 126 仍不能把 F 抬到 ≥1.0（或把 S 压到 <1.58），按原判死线封 sentiment 塔。

#### 9.9.4 最后加固轮（wave 258/259）：decay 是纯杀手，sentiment 塔判死

| 批 | alpha | 臂 | S | F | TO | 2Y |
|---|---|---|---:|---:|---:|---:|
| decay126 | `A1VR3oKX` | m5 s22 sector p3 | 0.31 | 0.10 | 0.134 | 0.27 |
| decay126 | `QPv1QwdX` | m5 s66 sector p3 | 0.20 | 0.05 | 0.107 | 0.27 |
| decay126 | `WjOEgvmN` | m5 s22 industry p3 | 0.33 | 0.11 | 0.136 | −0.12 |
| decay126 | `kqNxKz5g` | m2 s22 sector p3 | 0.15 | 0.03 | 0.137 | 0.49 |
| decay126 | `78LkdeV2` | m5 s22 sector **p1** | 0.40 | 0.15 | 0.129 | 0.31 |
| decay126 | `LLMPR0eL` | m2 s22 sector **p1** | 0.30 | 0.09 | 0.133 | 0.78 |
| decay30 | `Vkxv8rmb` | m5 s22 sector p3 | 0.73 | 0.32 | 0.163 | 0.92 |
| decay30 | `58EZvm5n` | m5 s66 sector p3 | 0.75 | 0.36 | 0.143 | 0.97 |
| decay30 | `Xg9jK3zX` | m5 s22 industry p3 | 0.72 | 0.31 | 0.165 | 0.42 |
| decay30 | `j2Y5gpG9` | m2 s22 sector p3 | 0.63 | 0.25 | 0.167 | 1.42 |

**decay 响应曲线单调下降**：decay 4 → S **1.80** / F 0.84；decay 30 → S 0.75 / F 0.36；decay 126 → S 0.40 / F 0.15。
由 decay30 反推 returns ≈0.031（decay4 为 0.080）：**收益降幅 2.5× 大于换手降幅 2.3×**，`ret/TO` 不升反降
⇒ decay 在此族**不是 fitness 提拉杆，是纯杀手**。p1 消融同样 S≤0.40 ⇒ 与凸幂无关，是日频新闻 edge 被平均掉。
经济上自洽：该族赚的是**数日内**的情绪过度反应修正，任何 ≥30 的 decay 都会把 edge 平滑没。

**sentiment 塔终判（按 9.9 预登记判死线执行）**

- 累计 **40 臂**（A10 + B10 + C10 + D6 + E6 + F4）＋派生反向臂，**没有一条**达到预登记线
  （S≥1.4 且 TO≤0.30 且 robust≥1.0）；最好成绩是反向 dev 的 S1.80 / 2Y2.35 / sub1.25 / robust1.38 / TO0.372，
  **唯一未过项 LOW_FITNESS 0.84**，而 fitness 的两条杠杆（窗口、decay）已双双实测无效。
- 两个数据集分别的结论：`sentiment26`（DNS 关注度）10 臂 \|S\|≤0.40 无信号；
  `sentiment21` 只有「净情感反向 dev」一处在射程内，但 fitness 结构性差 ~0.15。

⚠ **判死前必须先过强档复测（工具纪律，不是我的新增）**：本节全部 40 臂都跑在 `nanHandling=OFF`，
而 `tools/submit_batch.py` 对 OFF 的告警原文是「若本批结论用于选族/判死，请先用强档复测」。
本项目已有实证：IND behavioral_signals 在 decay8 下 **ON 2.19 vs OFF 0.46（4.8×）**。
fitness 与 S 近似线性 ⇒ ON 只要把 S 抬 ~20%，F 0.84→1.0 即可过闸。
⇒ 先派 **ON 复测批** `3bCnfSffE4sAbRl9rvVzpAs`（4 臂，decay4，其余设置不变）：
m5 s22/s66 sector p3 + m5 s22 industry p3 + m2 s22 sector p3。
**该批结果决定封塔还是出成品**——ON 若仍无可提交臂，则按判死线封塔，不再追加任何轮次。

**封塔处置（已执行，2026-10-26 结案）**：IND 五个未点亮塔（insiders / imbalance / option / sentiment /
shortinterest）至此**全部有实测依据地关闭**，未点亮塔空间**清零**（imbalance 由 §9.9.6 wave 261 补上实测）。
反向 dev 六颗（wave257）作**存档候选**不提交，表达式与设置固化在 `logs/_tmp_snt21_inv*.txt` 与本表，
将来平台 fitness 口径或数据更新可复用。

**判死闸为什么没有 `dead_end` 条目（口径，不是遗漏）**：首轮读帖全灭是工具故障（`read_failed`，
48 命中/37 读失败/正文 0 条，ledger `IND/forum_recon_error_de0c172cfd`）；读帖链路修好后
（根因与修复见 §9.9.5）重跑同一问题得 **`found=true`——但 3 条命中全是泛泛建议、不是本问题的答案**，
属机械相关性假阳性。按 §8.11，`seal_dead_end` 见 `found=true` 一律以 `recon_found` 拒绝，
`force_seal` 需人工确认 ⇒ **本轮不动**。封塔结论落在可复核的两层：
`wave_results` 254–260（六条 FAIL）+ 261（imbalance FAIL）、registry `campaign` 层
`sentiment21/sentiment26/imbalance5 = exhausted`；`dead_end` 层留空。

#### 9.9.5 强档复测（wave 260）：nanHandling ON 不翻盘，sentiment 塔关闭

**先修读帖链路（工程项，已闭环）**：根因是 `forum_recon.live_search_round` 把
`forum_research.resolve_id()` 的 **三元组** `(post_id, is_comment, url)` 整个当 pid 拼进
`/community/posts/{pid}.json` ⇒ 平台一律非 200，表现为「搜到 N 条、读 0 条」。
修法 = 新增 `forum_recon._resolve_post_id()` 收敛成 `str | None`（含 None / 异常 / 空 href 四条退路），
`live_search_round` 改走它；回归用例 `test_click_href_resolution_unwraps_resolve_id_tuple` +
`test_resolve_post_id_returns_none_on_failure`（`tests/unit/08_forum_recon/test_forum_recon.py`，36 passed）。
**实测验证**：`tools/diag_forum_read.py --probe-n 3` → `读到正文 3/3 帖`（修复前 0/3）。

**ON 复测批 `3bCnfSffE4sAbRl9rvVzpAs`（4 臂，decay4，其余设置不变，仅 nanHandling=ON）**

| alpha | 臂 | S | F | TO | 2Y | sub | robust | RA fail |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `YP1j0ZoW` | m5 s22 sector p3 | 1.46 | 0.64 | 0.321 | 2.68 | 1.23 | 1.30 | 2 |
| `bl6Yqp1R` | m5 s66 sector p3 | 1.42 | 0.62 | 0.324 | 2.58 | 1.50 | 1.62 | 2 |
| `d5W20qrv` | m5 s22 industry p3 | 1.58 | 0.72 | 0.326 | 2.62 | 1.53 | 1.63 | 1 |
| `QPv1VeRr` | m2 s22 sector p3 | 1.28 | 0.50 | 0.337 | 3.72 | 1.01 | 0.99 | 3 |

**判读**：ON 不是强档而是**弱档**（同臂 OFF 为 S1.80/F0.84/TO0.372）——本项目
behavioral_signals 那条「ON 4.8×」的先例**不具普适性**，不能拿它当跨族预期。
最好臂 `d5W20qrv` S 恰好踩到 IND 的 1.58 线，但 **F 0.72 距 1.0 差 0.28**；4 臂 RA fail 1–3 条，
全部落在 LOW_FITNESS（及其派生）。⇒ **强档复测未翻盘，且没有任何一条达到「可提交」**。

**sentiment 塔终判（累计 44 臂：A10+B10+C10+D6+E6+F4+ON4，另加派生反向臂）**

- **没有一条**达到预登记线（S≥1.4 ∧ TO≤0.30 ∧ robust≥1.0）：最好成绩是反向 dev OFF 的
  S1.80 / robust1.38 / TO0.372（TO 超标 0.072），且 F0.84 是全体最高——**仍低于平台 LOW_FITNESS 1.0**。
- fitness 的三条候选杠杆（窗口 22→126、decay 4→30→126、nanHandling OFF→ON）**全部实测无效或反向**。
- 结论：**sentiment 塔（sentiment21 / sentiment26）关闭**，不再为该塔烧配额；
  反向 dev 六颗（wave257）作**存档候选**，表达式与设置固化在 `logs/_tmp_snt21_inv*.txt` 与本表。

**取证闸的最终处置（没有强封）**：读帖链路修好后重跑同一问题，`tools/forum_recon.py` 返回
`found=true / n_useful=3`——三篇都是**通用贴**（单数据集金字塔乘数瓶颈、单数据集建 α 技巧、数据集地图），
内容不构成对「sentiment 反向 dev 的 fitness 破法」的回答（贴中 `新闻/情绪超过一个季度基本没用` 与本文实测同向）。
按 §8.11 的机械判据，这属于 `recon_found`，`seal_dead_end` 会拒绝；`force_seal` 需人工确认，**本轮不使用**。
⇒ 塔的关闭落在**可复核的非永久层**：
① wave_results 254–260 七条 FAIL（本表 + §9.9.1–9.9.4）；
② `registry_empirical` 的 `campaign` 层标 `sentiment21` / `sentiment26` = `exhausted`；
③ 本节。
**重开条件（写死，防无证据复活）**：平台 fitness 公式 / IND 的 `LOW_FITNESS` 线下调，或出现新的
sentiment 数据集（当前 IND 仅这两集）。

#### 9.9.6 imbalance5 探针（最后一颗未实测的未点亮塔）

sentiment 关闭后，IND 未点亮塔里**只剩 imbalance 没有回测证据**（其余四塔见 §9.9 逐塔表：
insiders 无有效字段/已判死、shortinterest 价格带死路、option fitness 天花板/zombie、
sentiment 刚关闭）。原表把 imbalance 标「暂缓」，依据是拥挤度而非实测 ⇒ 补一轮探针把这条也变成实测。

**平台字段（IND/TOP500/D1，`get_datafields` 实测 2/2 完整）**

| 字段 | 类型 | 覆盖 | alphaCount |
|---|---|---:|---:|
| `imb5_score` | MATRIX | 0.7876 | **16287** |
| `imb5_mktcap` | MATRIX | 0.7876 | 3993 |

**预登记判死线（先写后跑，防事后合理化）**：6 臂内若无一条达 **S≥1.4 且 TO≤0.30 且 robust≥1.0**，
imbalance 塔关闭、不再追加轮次。两个字段 × 三种几何已覆盖该集全部可用结构（慢水平 / 中心凸 dev / 反向 dev /
比值水平），再挖只能换设置，而设置杠杆在 sentiment 塔已证无效。
**直接跑强档**（`nanHandling=ON`）：这是判死结论要用的档位，避免 sentiment 那样「先 40 臂 OFF 再补 ON」。

6 臂 = `imb5_score` 慢水平66/industry、`imb5_mktcap` 慢水平66/industry、
`imb5_score` 中心凸 dev p3/sector、`imb5_mktcap` 中心凸 dev p3/sector、
`score/mktcap` 比值水平66/industry、`imb5_score` 反向 dev p3/sector。
设置同战役基线：IND/TOP500/D1/STATISTICAL/decay4/trunc0.08/FULL/2014-01-01→2023-12-31。
发批前 `preflight_expressions` 已过（6/6，字段 2/2，`any_changed=false`）。

**结果（wave 261，multisim `1AFgOU6704knbcJRlfwoQ42`，6/6 COMPLETE）**

| alpha | 几何 | S | F | TO | 2Y | robust | 判 |
|---|---|---:|---:|---:|---:|---:|---|
| `kqNxZl8L` | score/mktcap 比值水平66 / industry | **1.80** | **1.38** | 0.0978 | 1.71 | 0.69 | ✗ robust |
| `E56ZeJQm` | score 中心凸 dev p3 / sector | 1.68 | 1.22 | 0.1179 | 0.57 | 0.68 | ✗ robust |
| `e75lxR5M` | score 慢水平66 / industry | 1.58 | 1.08 | 0.0636 | **2.67** | **0.92** | ✗ robust |
| `A1VR7Kxg` | mktcap 慢水平66 / industry | 0.00 | 0.00 | 0.0668 | −0.83 | 0.25 | ✗ 无信号 |
| `gJeY9prJ` | mktcap 中心凸 dev p3 / sector | −0.29 | −0.10 | 0.0981 | −0.41 | 0.30 | ✗ 反向 |
| `omE1gOPE` | score 反向 dev p3 / sector | −1.68 | −1.22 | 0.1179 | −0.57 | −0.68 | ✗ 镜像 |

**判决：预登记线触发，imbalance 塔关闭。** 6 臂无一条达 S≥1.4 ∧ TO≤0.30 ∧ robust≥1.0；
三颗「其余闸全过、pyramid effective=1（ATOM 形态）」的臂**唯一未过项都是
`LOW_ROBUST_UNIVERSE_SHARPE`（limit 1.0）**：0.69 / 0.68 / 0.92。最近的 `e75lxR5M` 差 0.08，
但预登记线不做事后放宽——差 0.08 是「近墙未过」，不是「过了」；且该臂 2Y 2.67 而 robust 0.92 的
反差本身说明强项集中在主宇宙/近年，跨宇宙稳健性没有。`imb5_mktcap` 单字段双几何均为零/负
（慢水平 S0.00、dev S−0.29），反向 dev 是 `E56ZeJQm` 的严格镜像（S−1.68），无独立信号。
设置杠杆（窗口 / decay / nanHandling）在 sentiment 塔已逐一实测无效，本轮不再重复。

**处置**：`wave_results` 261 = FAIL（n_pass 0 / n_near 3，batches `1AFgOU6704knbcJRlfwoQ42`）；
registry `campaign` 层 `imbalance5 = exhausted`；`dead_end` 层留空（取证口径见 §9.9 封塔处置段）。
**⇒ IND 未点亮塔空间清零**：insiders / imbalance / option / sentiment / shortinterest 五塔全部有实测依据关闭。
重开条件（两塔通用）：平台 `LOW_ROBUST_UNIVERSE_SHARPE` 或 fitness 口径变化，或出现新的
imbalance / sentiment 数据集；届时可直接复用本表表达式与设置重跑，不必重做几何探索
（六条原文在 `logs/_tmp_imb5_A.txt`，sentiment 系在 `logs/_tmp_snt21_inv*.txt`，均已入库 wave 261 / 257）。


