# GLB 开波手册（全数据集 × 全模板族流水线）

> 2026-10-26 首波开启。参照 `docs/reference/ind_campaign_runbook_20261025.md` 的区域化模式。
> 引擎与托管器位置：`<安装位>/skills/wq-brain-ra-glb/scripts/`（入口 `glb_runner.py` / `glb_main.py`）。
> ⚠ **仓库内 `Claude/skills/wq-brain-ra-glb/scripts/` 只有 README**（与 IND 的「安装位独有」同病）⇒
> 本手册是唯一把 GLB 副本修复内容记录下来的地方，重装技能后必须重做 §1 的 4 处修复。

---

## 0 一句话启动

```bash
cd <仓库根>

WQB_REPO_ROOT=<仓库根> WQB_CAMPAIGN_REGION=GLB \
  world-quant-brain-mcp/.venv/Scripts/python.exe -X utf8 \
  <安装位>/skills/wq-brain-ra-glb/scripts/glb_runner.py \
  --datasets other455,pv30,pv37,techindi_model,model135,chart_cnn_alpha,predictive_starmine,risk70 \
  --min-cov 0.85 --require-ten-years --max-inflight 2 \
  --stall-sec 1800 --check-sec 60 --zero-alpha-stop 3
```

查进度（不拉起进程）：同一命令加 `--once`。

---

## 1 ★ 开波前必须做的 4 处修复（2026-10-26 实测，缺一条战役即空转）

| # | 文件 | 症状（不修的后果） | 修法 |
|---|---|---|---|
| 1 | `scripts/glb_runner.py:74` | `_SUF = "" if REGION == "GLB"` ⇒ **GLB 读 EUR 的无后缀断点**（`results/full_template_campaign_checkpoint.json`，EUR 战役在写）⇒ 互相覆盖、done 读数错 | 改成 `"" if REGION == "EUR" else f"_{REGION}"`，与 `wqb_campaign/config.py:53` 同口径 |
| 2 | `wqb_campaign/lit.py` | 旧版按「拉全部 `stage=OS` 历史累计、`>3` 判点亮」⇒ GLB 被误判 PV=10/OTHER=8/MODEL=4 已点亮，**把唯一有信号的类别全部降权** | 整文件替换为 `Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/wqb_campaign/lit.py`（平台当季 `>=3` 口径，区域参数化） |
| 3 | `wqb_campaign/config.py` | ① 缺 `DELAY` 常量（替换 lit.py 后 `ImportError`）<br>② `REGION_SETTINGS["GLB"]` 用面板值 TOPDIV3000/STATISTICAL/decay2 ⇒ **系统性 F 0.38–0.45、EMEA 0.41–0.56** | ① 加 `DELAY = 1`<br>② 改 `{"universe":"MINVOL1M","neutralization":"COUNTRY","decay":"8","truncation":"0.02","nan_handling":"OFF","max_trade":"OFF"}`（实测依据见 §2） |
| 4 | `wqb_campaign/transport.py` | `WQB_TOOLS = ~/wqb-scripts/wqb_tools.py` —— **该文件不存在**（仓库外、未跟踪）⇒ `dispatch` 全场 `sim_id=None`、每集静默判 `NO_DATA`（n_alphas=0），表面像「信号差」 | 整文件替换为 IND 版（走仓库 `tools/submit_batch.py` + `_sim_id_from_output()` 解析 `status=201 -> <Location>`，并带 `harvest_safe` 双路径兜底） |

**收官件**：`cache/_harvest_safe.py` 必须存在（`transport.harvest()` 子进程硬依赖）。缺失时每批 `state=error`、8×180s 后整集 `n_alphas=0`。
仓库无此文件时从 IND 包复制：`cp Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/harvest_safe.py cache/_harvest_safe.py`。

**症状速查**：日志出现 `[dispatch] 派发 N 条` 后几秒即 `verdict=NO_DATA max_S=-9.00 n_alphas=0` ⇒ **是链断了，不是集死了**（先查上面 #4 与收官件）。

---

## 2 区域设置：为什么不用面板缺省

`tracking/GLB/config/settings.json`（面板）= TOPDIV3000 / STATISTICAL / decay2 / trunc0.08。
但 2026-10-14 在 6 个同族 corr 字段上的实测：

| 设置 | S | F | EMEA | 三区 |
|---|---|---|---|---|
| TOPDIV3000/STATISTICAL/decay2 | 1.60–1.81 | **0.38–0.45 ✗** | **0.41–0.56 ✗** | 不全过 |
| MINVOL1M/COUNTRY/decay8/trunc0.02 | **2.11–2.70** | **1.04–1.30 ✓** | ✓ | 全过 |

后者产出 6 颗 `failed_ra_count=0` 候选（YPxrGndM / e76pa98J / d5KXzqbg / RRA3vNje / vROqo58r / omopkn7k）。
⇒ 战役基座用实测配置；面板值保留不动（面板仍是区域权威，仅战役口径覆盖）。

---

## 3 开波前 5 项检查（2026-10-26 实测值）

| # | 检查 | 命令 | 实测 |
|---|---|---|---|
| 1 | GLB 数据集画像入库 | `SELECT count(*) FROM dataset_profile WHERE region='GLB'` | **143** ✅ |
| 2 | 字段库有 GLB 数据 | `fields ⋈ datasets ⋈ regions WHERE r.name='GLB'` | **28,465** ✅ |
| 3 | 黑名单干净 | `cat cache/bad_tokens.json` | `["earnings_volatility_trend"]`（字段名，非结构算子）✅ |
| 4 | 断点隔离 | `ls results/full_template_campaign_*GLB*` | 首次应为空；有则确认续跑 |
| 5 | 平台并发余量 | `--max-inflight 2`（用户 2026-10-26 指定） | 账户级 2 槽，campaign 独占 |

---

## 4 数据集池（GLB，2026-10-26 实测 137 集 n_fields≥3）

**塔位口径**：`get_pyramid_alphas` GLB/D1 当季**全 0**（Q4 无提交）⇒ 「未点亮塔优先」当季**不排除任何类别**；
排除集只按「已占用通道 / 已判死」定，不按类别定。

**筛选口径**：`n_fields>=3` 且 `avg_field_coverage>=0.85` 且 `category ∈ {PV, OTHER, MODEL, RISK}`
（这四类历史 RA 通过数 68 / 79 / 1 / 13，其余类别全 0）⇒ **26 集**，按 `alpha_count/n_fields`（拥挤度）升序：

| 优先 | 数据集 | 类别 | 字段 | cov | aC | aC/nf | 判据 |
|---|---|---|---|---|---|---|---|
| 1 | `chart_cnn_alpha` | MODEL | 1041 | 0.936 | 41 | 0.0 | ❌ **已判死**：信号真实（S 1.81–1.97 / F 1.11–1.28 / 2Y 2.24–2.76），但 10 变体 EMEA 全 0.43–0.55（结构性地板，美/亚强欧洲弱） |
| 2 | `macro_equity_signals` | MODEL | 180 | 0.867 | 19 | 0.1 | 极低拥挤 |
| 3 | `global_seasonal_model` | MODEL | 690 | 0.988 | 90 | 0.1 | 低拥挤 + 高覆盖 |
| 4 | `predictive_starmine` | MODEL | 543 | 0.950 | 113 | 0.2 | DEU 全区最高产出族 |
| 5 | `other455` | OTHER | 1500 | 0.897 | 529 | 0.4 | OTHER 历史 79 RA 通过 |
| 6 | `model219` | MODEL | 1008 | 0.920 | 501 | 0.5 | — |
| 7 | `model135` | MODEL | 137 | 1.000 | 93 | 0.7 | 覆盖率满分 |
| 8 | `pv30` | PV | 150 | 0.859 | 110 | 0.7 | PV 历史 68 RA 通过 |
| 9 | `model36` | MODEL | 21 | 0.914 | 17 | 0.8 | 小集快跑 |
| 10 | `techindi_model` | OTHER | 1818 | 0.974 | 1576 | 0.9 | 仅 1 字段被占，空间最大 |

**排除项（附证据，避免重复投入）**：
`intraday_pv_feats`（120 结构挖尽：2 条有效通道已被自家 Q3 alpha 占位，prod 0.78–0.86）、
`dl_riskfree_returns`（6 颗 ACTIVE 占位）、`tech_chart_model`（GLB skill 明令排除）、
`model239` / `risk60`（证券借贷域被 RR66gp2j 门控占用）、
`institutions6` / `institutions18`（APAC 信号闸 + 季频换手墙）、
`analyst10` / `analyst15` / `analyst69`（一致预期族天花板 0.96–1.07 + anl15 精确表达式封禁）、
`other327`（利率敏感度，APAC≈0）、`risk68`（字段明写 European-only）、`pv98`（字段实为 OHLCV，与 pv1 冗余）、
`model140`（3 字段，通胀 beta，弱）、`pv1` / `univ1` / `risk66`（基础行情/市值聚合，无信号）。

**第一波（2026-10-26 13:59 启动，8 集）**：
`other455, pv30, pv37, techindi_model, model135, chart_cnn_alpha, predictive_starmine, risk70`
（引擎按自身优先级重排：未点亮 → 处女地 → 暴露多样性 → VS×cov，实际首跑 `chart_cnn_alpha`）。
`--min-cov 0.85`（用户授权动态调整；后续可按实测分布降到 0.75/0.65 纳入
`model170`(0.739) / `other546`(0.661) 两处女地）。

---

## 5 十年硬闸（用户 2026-10-26 第 4 条）

`--require-ten-years`：候选必须 `year_profile.n_years>=10` 且 `first_year<=start_year`（2014），
否则改判 `INSUFFICIENT_HISTORY`。⚠ 该画像在**仿真后**才算 ⇒ 只能做候选级否决，不能预筛数据集。
已知反例：`option1` 只有 2017 一年持仓（僵尸数据）⇒ 十年闸正确否决。

---

## 6 收割后必做（S6）

1. `campaign_year_audit.py` 补算逐年画像，按样本有效性分层（未开采 / 样本无效 / 样本健康）。
2. 近闸候选先**归因**再谈降 prod（`compute_mutual_correlation` 对自持 ACTIVE 复现平台 prod，误差 <0.001）
   —— 2026-10-26 实证：GLB 六颗 RA 全净候选的 prod 对手 100% 是自家 `gJboYLRl` / `mLmxKN12`。
3. 判定用 `submit_verdict`（只拦不放），提交需用户明确确认。
