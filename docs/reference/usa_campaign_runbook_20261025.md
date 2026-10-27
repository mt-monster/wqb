# USA 开波手册（全数据集 × 全模板族流水线）

> 2026-10-25 由 IND 开波手册（`ind_campaign_runbook_20261025.md`）迁移而来。
> 引擎从 `Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/` 复制为
> **`Claude/skills/wq-brain-ra-usa/scripts/usa_campaign/`**，区域在模块级硬钉为 USA。
> 用户 2026-10-25 定稿约束：**并发 2**、**覆盖率门槛可动态调整**、**候选必须十年都有数据**。

---

## 0 一句话启动

```bash
cd <仓库根>

<venv> -X utf8 Claude/skills/wq-brain-ra-usa/scripts/usa_campaign/usa_runner.py \
  --datasets institutions6,earnings4,other566,pv1,fundamental13,news81 \
  --min-cov 0.6 --require-ten-years --max-inflight 2 \
  --stall-sec 1200 --check-sec 60 --zero-alpha-stop 3
```

`<venv>` = `world-quant-brain-mcp/.venv/Scripts/python.exe`

`usa_runner.py` 在 import 前硬钉 `WQB_CAMPAIGN_REGION=USA`；隔离如下（已实测）：

| 项 | EUR（默认） | IND | **USA** |
|---|---|---|---|
| 断点 | `..._checkpoint.json` | `..._checkpoint_IND.json` | `..._checkpoint_USA.json` |
| 结果 | `..._results.json` | `..._results_IND.json` | `..._results_USA.json` |
| digest | `campaign_digest.md` | `..._IND.md` | `..._USA.md` |
| 点塔缓存 | `cache/eur_lit_counts.json` | `..._ind_...` | `..._usa_...` |
| universe | TOPCS1600 | TOP500 | **TOP3000** |
| neutralization | FAST | STATISTICAL | **SUBINDUSTRY** |
| decay | 4 | 4 | **5** |
| nanHandling | ON | OFF | **ON** |
| maxTrade | ON | OFF | **OFF** |

### ★ 从 IND 复制时必须改的 5 处（这次全改了，下次复制照抄）

| # | 位置 | 改法 |
|---|---|---|
| 1 | `usa_main.py:36` / `usa_runner.py:67` | `os.environ["WQB_CAMPAIGN_REGION"] = "USA"` |
| 2 | `usa_runner.py:79` | `REGION = "USA"` |
| 3 | `usa_runner.py:75` | `CAMPAIGN = .../usa_main.py`（**漏改 symptom：子进程 rc=2 + "can't open file ...ind_main.py"**） |
| 4 | `wqb_campaign/config.py` | `REGION_SETTINGS["USA"]` 与 `tracking/USA/config/settings.json` 对齐（原表 INDUSTRY/decay4/maxTrade ON 是错的） |
| 5 | `wqb_campaign/pipeline_usa.py` | sub 闸：USA 是**比率闸 0.435×S**（照 IND 的绝对 1.0 判会全部误判「sub 已过」） |

`report.py` 同口径同步：`_SUB_GATE = {"IND": ("abs",1.0), "USA": ("ratio",0.435), "EUR": ("ratio",0.53)}`。

---

## 1 开波前 5 项检查（缺一项就别开）

| # | 检查 | 命令 / 判据 | USA 实测（2026-10-25） |
|---|---|---|---|
| 1 | USA 数据集画像已入库 | `SELECT count(*) FROM dataset_profile WHERE region='USA'` | **294**（`n_fields>=3` 的池 280） |
| 2 | 字段库有 USA 数据 | `field_profile_usa` | **85,184** |
| 3 | 黑名单干净 | `cache/bad_tokens.json` | `["earnings_volatility_trend"]`——字段名，非结构算子 ✓ |
| 4 | 断点不存在（新跑） | `results/full_template_campaign_checkpoint_USA.json` | 首次为空 ✓ |
| 5 | 并发余量 | **账户级**并发被多个战役共享 | ⚠ USA 2 + IND 2 已达上限，再加手工批会 `429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED` |

---

## 2 三条常用命令

```bash
# ① 干跑校验：零仿真，验证 region/universe 接线（改完引擎必跑）
<venv> -X utf8 .../usa_campaign/usa_main.py --audit institutions6

# ② 正式托管（前台；含停滞/熔断看护）
<venv> -X utf8 .../usa_campaign/usa_runner.py --datasets <ds,...> --min-cov 0.6 \
  --require-ten-years --max-inflight 2 --stall-sec 1200 --check-sec 60 --zero-alpha-stop 3

# ③ 只查一次进度（不拉起进程）
<venv> -X utf8 .../usa_campaign/usa_runner.py --once
```

可选：`--datasets a,b`｜`--only-cats OTHER,PV`｜`--limit N`｜`--max-inflight N`｜`--sweep-done`｜`WQB_CAMPAIGN_FRESH=1`。

### 2.1 覆盖率门槛（用户：可动态调整）

- `--min-cov` 覆盖 `pipeline.py` 里 **两处并列字面量**（`priority_min_cov` 与 `eff_min ... else 0.6`），只改一处无效。
- 默认 0.6；处女地（`alphaCount<=10` 且 `valueScore>=5`）自动取 `min(eff_min, 0.35)`。
- 闸比的是 `dataset_profile.avg_field_coverage`（别名 `cov`），**不是**平台 API 的 `coverage`。

### 2.2 十年硬要求（用户：必须十年都有数据）

`--require-ten-years` ⇒ 候选必须 `n_years>=10` 且 `first_year<=start_year`，否则 verdict 改判
`INSUFFICIENT_HISTORY`（不是 DEAD，是样本不足）。
⚠ `year_profile` 只在 `max_s>=1.2` 时计算 ⇒ 只能做**候选级否决**，无法预筛数据集。

---

## 3 USA 闸门（与 IND 的关键差异）

| 项 | EUR | IND | **USA** |
|---|---|---|---|
| LOW_SHARPE | 1.58 | 1.58 | **1.58**（严格不等式） |
| LOW_FITNESS | 1.0 | 1.0 | **1.0**（唯一 ≥） |
| LOW_2Y_SHARPE | 1.58 | 1.0 | **1.58** |
| LOW_SUB_UNIVERSE_SHARPE | 0.53×S | 绝对 1.0 | **0.435×S（比率闸）** |
| TO | 0.05–0.3 | 0.01–0.7 | **0.01–0.7**（⚠ 原记 0.4 已订正，见下） |
| prod / self | <0.7 | <0.7 | **<0.7（死线）** |
| investability | N/A | N/A | **N/A**（不测） |

**USA 0.435×S 的实测校准**（三点）：S1.43→限 0.62／S1.99→限 0.87／S2.01→限 0.87 ⇒ 比值恒 0.433–0.435。

### ★ 2026-10-26 两处实测订正
1. **TO 上限不是 0.4**：`QPY81NKQ` TO=**0.6227**，`HIGH_TURNOVER` 判 **pass**（fail 串里只有 `LOW_FITNESS`）。
   ⇒ USA 换手上限 ≥0.6227，按 BRAIN 通用档位记 **0.01–0.7**。**别用 0.4 误杀高换手候选。**
2. **F 闸闭式（USA 实测吻合到小数点后 2 位）**：
   ```
   F = S × sqrt(|returns| / max(TO, 0.125))
   ```
   QPY81NKQ：2.02 × sqrt(0.0922/0.6227) = 2.02 × 0.3848 = **0.777**（平台实测 0.78 ✅）。
   ⇒ **F 不靠提 S 单解**：F 只与 `returns/TO` 的比值挂钩，S 是线性因子。
   ⇒ 达标换算：QPY81NKQ 需 **TO ≤ 0.376**（ret 不变）或 **returns ≥ 0.1525**（TO 不变，需 +65%）。
   ⇒ **提 returns 与降 TO 等价，优先降 TO（杠杆是 1/sqrt，降 40% TO 即达标）**。

### ★★ USA 的真正瓶颈是 **prod 墙**（不是 robust，也不是 S）
- USA 是最深最饱和的市场：value/quality/book 必死（book/value 单族 145 颗同族 ACTIVE）。
- 判据：`submit_ready.gate` 为准；`backtest_results.ra_failed_checks IS NULL` = **未核验**，不等于 RA 全过。
- 开波前探针（skill P0-1）：`$WQ_PY tools/campaign_intel.py prod-probe --region USA --dataset <ds>`（prod ≥0.75 封族）。

---

## 4 第一波选集（2026-10-25）

### 4.1 塔位（当季口径，`campaign_intel.py pyramid --region USA`）
**已点亮 2/16**：`analyst 6`、`model 4`。
**未点亮 14 类**：earnings(1，差2)、other、sentiment、option、news、fundamental、insiders、macro、pv、risk、shortinterest、imbalance、institutions、socialmedia。
倍率最高：`other 1.4` / `sentiment 1.4` / `option 1.3` / `news 1.2` / `earnings 1.2`。

### 4.2 选集口径（未点亮优先）
`dataset_profile`（280 集）→ 剔已点亮（ANALYST/MODEL）→ 剩 **186** → 剔 `usa_dead_datasets.md`（47 条 + 我自判的 10 条）→ **141**。
排序键：**暴露多样性（≥3）→ 覆盖率 → 经典异象机制 → 塔差**。

### 4.3 第一波 6 集

| 数据集 | 类别（塔差·倍率） | 字段 / cov | 入选理由 |
|---|---|---|---|
| `institutions6` | INSTITUTIONS（0/3，1.0） | 22 / 1.000 | 机构持股变化＝经典异象；IND 战役该集出过最强 alpha |
| `earnings4` | EARNINGS（**1/3，1.2**） | 375 / 0.969 | 唯一已有点亮进度、差 2 颗，ROI 最高 |
| `other566` | OTHER（0/3，**1.4**） | 51 / 1.000 | 倍率最高；图像化金融预测＝新机制，低拥挤 |
| `pv1` | PV（0/3，1.1） | 24 / 1.000 | 经典价量；`returns` 属本集 ⇒ 残差化族仍算 ATOM |
| `fundamental13` | FUNDAMENTAL（0/3，1.1） | 87 / 0.757 | 综合基本面，未测 66 字段 |
| `news81` | NEWS（0/3，1.2） | 23 / 1.000 | 新闻事件，未测 23 字段 |

已剔除（判死/我实测判死，不复挖）：`chart_return_model`、`pv103/106/115/149`、`insider_matrix`、
`insider_trx_matrix`（未判死，但已有 2 颗验证 ATOM，见 §5）、`institutions18`、`other143/571/635`、
`risk60`、`sentiment21/26`、`intraday_pv_feats`、`techindi_model`、`shortinterest3/29`、
`us_short_sale`、`short_interest_pred`、`fundamental91`、`option40`、`insiders3/4`、`web_traffic_engage` 等。

---

## 5 近闸候选定向挖掘（skill SOP）

流程：`wq-brain-ra-usa` 的六步纵深骨架（体检 → 组装 → **归因** → 破闸杠杆 → **算子穷举** → 终验），
归因必须先于调参（`tools/gate_attribution.py --alpha-id <id> --prod-corr <实测>`，零仿真）。

### 5.1 2026-10-25 已验证的 USA ATOM（UNSUBMITTED，等用户确认）

| alpha | 表达式 | 数据集（effective） | S / F | 2Y / sub | TO | prod / self | 备注 |
|---|---|---|---|---|---|---|---|
| `XgRM3Yra` | `ts_zscore(ts_sum(total_buy_transaction_count, 126), 252)` | insider_trx_matrix（**1 ⇒ ATOM**，塔 OTHER ×1.4） | 1.66 / 1.19 | 2.27 / 0.97 | 0.087 | **0.5803** / −0.091 | RA 0、fail=[]；DD 7.1%；RN 2.01 |
| `LL53QVvn` | `ts_zscore(ts_sum(mean_top_buy_transaction_count, 63), 252)` | 同上（ATOM，OTHER ×1.4） | 1.61 / 1.39 | 2.75 / 1.00 | 0.112 | **0.6163** / −0.036 | RA 0、fail=[]；CLUSTER 1.26 WARN；RN 1.84 |

- 两者互相关 **0.5421**（<0.7 ⇒ **两颗独立席位**）；同族 `1Yj08nb6`(0.857 与 XgRM3Yra)、
  `1Yj03w9m`(0.9995 与 LL53QVvn)、`XgRM3YGa`(0.72 与 LL53QVvn) **全部挤掉**，不可另计席位。
- 设置：USA / **TOP2000** / D1 / decay 5 / SUBINDUSTRY / nanHandling ON / maxTrade OFF（不是区域默认 TOP3000）。
- **十年逐年（2014–2023）PnL 全正** ✓（满足本次"十年都要有数据"）。
  弱年同为 **2021**（Sharpe 0.24 / 0.01），2022（2.92 / 3.24）与 2023（1.59 / 2.12）强
  ⇒ 稳健性审计的 `每年>0.3` 与 `max/min≤3` **不达标**，提交前须走 `brain-alpha-robustness` 并按用户裁决。

### 5.2 定向挖掘方向（insider_trx_matrix 第三席位）
该集 **29 字段**里 `usd_*` 共 16 个、**alphaCount=0 的零拥挤字段 12 个**
（`usd_direct_signal_value_1..4`、`usd_top_direct_signal_value_1..4`、`usd_top_primary/secondary/tertiary/quaternary_signal_value`、
`total_secondary_sell_transaction_count`、`total_top_secondary_sell_transaction_count`）。
⇒ 按「文献口径优先」纪律（美元**成交额**比笔数更贴近内幕交易文献的标准测量），
候选骨架沿用赢家形态 `ts_zscore(ts_sum(F, w), 252)`，w∈{63,126}，并试净买卖差
`subtract(buy_usd, sell_usd)`。⚠ 需先确认与上述两颗的互相关 <0.7。

---

## 6 已知坑（USA 特有）

1. **子进程 rc=2 + `can't open file ...ind_main.py`** ⇒ `usa_runner.py` 的 `CAMPAIGN` 常量没改（§0 表 #3）。
2. **sub 闸照 IND 判** ⇒ USA 候选会被误判「sub 已过」（§0 表 #5 已修）。
3. **区域设置照抄 config 原表** ⇒ USA 会是 INDUSTRY/decay4/maxTrade ON，与 `settings.json` 不一致（§0 表 #4）。
4. **账户级并发共享**：USA(2) + IND(2) 即触顶，此时手工 `create_multi_simulation` 直接
   `429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED` ⇒ 手工批要等槽位，不要重试刷。
5. **`year_profile` 缺失时** `[10y]` 打印「无法验证十年数据」，verdict 保留原判、结果里 `ten_years=None`。
6. **`NO_DATA` ≠ 信号差**：多为管道故障（先查 `bad_tokens.json` 是否误伤结构算子）。
7. **`ra_failed_checks IS NULL` = 未核验**，不能当 RA 全过。

---

## 7 成本与进度

| 项 | 数值 |
|---|---|
| 单集耗时 | USA/TOP3000 比 IND/TOP500 慢，估 60–120 min |
| 集均表达式 | 20–60 条（`FULL_FIELD_CAP=8` × 15 族 + probe 12 + 残差化单独一批 `<ds>@res`） |
| 第一波 | 6 集，并发 2 ⇒ 约 3–6 h |
| 进度查询 | `results/full_template_campaign_checkpoint_USA.json` 的 `done` 列表；`results/campaign_digest_USA.md` |
