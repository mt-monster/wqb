# USA 信号挖掘工作流（EUR 文章的 USA 区域化版）

> **来源**：`docs/reference/EUR/signal_mining_workflow.md`（EUR，2026-10-21）。
> **本文只写 USA 怎么用**：EUR 的标定数字、工具假设、窗口档位**不直接照搬**；每处都标了「EUR 证据 / USA 待实测 / USA 已否证」。
> **与九步的关系**：本文是九步骨架里 S0–S6 的**取向补充**，不另起流程；冲突时以九步正文与本区锁定项为准。
> **as_of**：2026-10-21。

## 〇、一页总览

```
选集(EV) → 画维度地图(画像) → 配统计模板(频段×属性) → 派发(维度/模板族/边界三闸)
        → 收割归因 → 定向开发(四杠杆链) → 全闸验证(prod/self/robust) → 标绿/判死/存档
```

| 本文步 | 九步落点 | 产物 |
|---|---|---|
| 1 选集 | S0 数据集体检 | 白名单 + EV 排序 |
| 2 维度地图 | S1 字段扫描 | 字段画像 / 维度覆盖表 |
| 3 配模板 | S2 概念优先生成 | 候选表达式（带统计族标签） |
| 4 三闸派发 | S2→S3 门禁 + S3 回测 | gate 报告 + sim 批次 |
| 5 收割归因 | S3 收割 + S4 诊断 | 近闸表 / 失败归因 |
| 6 四杠杆链 | S4 改进 | 定向变体 |
| 7 全闸验证 | S4→S5 稳健闸 + 判定 | `submit_verdict` / 相关性 |
| 8 标绿判死 | S6 复盘回写 | GREEN/YELLOW / `dead_end` |

---

## 一、Step 1 选集：先算 EV，但 EV 不是信号强度

```bash
$WQ_PY tools/query_profile.py datasets --region USA --sort ev --limit 30
$WQ_PY tools/query_profile.py stats --region USA
```

**公式**（与 `full_template_campaign.py::all_datasets` 的 ORDER BY 同源）：

```
EV = value_score × 平均覆盖 × 未测占比 ÷ (1 + alphaCount/1000)
```

**硬排除**（任一命中不投主腿）：

| 排除项 | 判据 |
|---|---|
| 覆盖不足 | 字段 `coverage < 0.5` → 只可作条件 / 分组，不作主腿 |
| 平台不可用 | `get_datafields` 拿不到字段，或平台 `field_count=0`（画像有字段 ≠ 平台能用） |
| 同族全死 | 该语义维度同族字段全 `DEAD` 且 `max_S < 1.0`（**探针证据，不是数据集判死**） |
| 已点亮塔 | 本区用户指令：**已点亮塔的数据集先不回测** |
| 饱和族 | `value` / `quality` / `book` 及其线性变体；情绪域 prod 已饱和（见 [six-step-usa-override.md](six-step-usa-override.md) ①） |

**USA 的三条额外口径**：

1. **白名单只能用「未点亮塔 × 低 alphaCount」筛**。`score_datasets.py` 的 signal-score top20 全是 model 族，按 score 排序等于往已点亮塔堆料。
2. **EV 高 ≠ 能出活**。本轮在 DB 副本上实算：USA EV 榜首是 `news_sentiment_dl`（EV≈5.90），落在本区**已饱和**的情绪/新闻域。EV 只回答「先探谁」，不回答「能不能出」。
3. **先建画像再谈 EV**。USA 的 `dataset_profile` / `field_profile_full` 原本只有 EUR 行；一次性建库：

   ```bash
   $WQ_PY tools/load_field_profiles_to_db.py --region USA
   ```

   实测（2026-10-21，DB 副本）：**294 个数据集 / 85,184 个字段**入库；`sem_type` **100% 为 NULL**（`field_semantic_type` 无 USA 行）；数据集名/描述为空（loader 的 catalog 仍指向 EUR 文件）。**未跑 loader 前** `query_profile.py stats --region USA` 只会提示「无画像行」，`datasets --region USA` 返回空——这不是「USA 没有数据集」。

---

## 二、Step 2 画维度地图 + 读字段属性

```bash
$WQ_PY tools/query_profile.py fields --region USA --dataset <ds>
$WQ_PY tools/query_profile.py dims  --region USA --min-dim-cov 1.0
```

看三件事：① 语义维度（`semantic_family`）是否每个都被候选触及；② 字段属性 → 模板约束；③ 历史判定（`verdict`）：ALIVE 是金矿，UNUSABLE / DEAD 是雷区。

**属性 → 模板约束（USA 可用列已标注）**：

| 属性 | 判据 | 约束 | USA 取数 |
|---|---|---|---|
| 慢频 | `freq_hint` = quarterly / semi-annual | `ts_backfill` ≥252、平滑 ≥66，**禁 3–22 短窗** | ✅ `field_profile_full.freq_hint` |
| 稀疏 | `near_zero_ratio > 0.3` | 必须 backfill + 事件式 decay | ❌ DB 无此列，需 Labs / 原始统计 |
| 截断 | `shape = ceiling` | 先 `rank`，禁裸 zscore | ❌ 需外部统计 |
| 计数 | `integer = 1` | 用 spread / ratio，禁 level | ❌ 需外部统计（名称含 `_count`/`_length` 可先验） |
| 全正 | `pos_ratio ≈ 1` | 禁裸 zscore，先 `rank` | ❌ 需外部统计 |
| 有符号 | 0.1–0.9 双向 | 可直接用，**符号即方向** | ❌ 需外部统计 |
| 比率 | `sem_type = ratio` | 直接上模板 | ⚠ USA `sem_type` 全 NULL；用名称/描述 + `field_profile_perf.family` 代理 |
| 已是变化量 | `sem_type = revision_change` | **禁再套 `ts_delta`** | ⚠ 同上；名称含 `chg`/`delta`/`growth` 先验 |
| 有界噪声 | `sem_type = score` | 先 `rank` / `quantile`，或只作门控 | ⚠ 同上 |
| 规模水平 | `sem_type = level_amount` | **先做规模中性体检** | ⚠ 同上；规模字段名以 `get_datafields` 实测为准 |
| 标识符 | `sem_type = identifier` | 不可作信号 | ✅ 名称/描述可判 |
| VECTOR 事件型 | `field_type = VECTOR` | **必须先 `vec_*` 聚合**，禁事件层算术与 `ts_backfill` | ✅ `field_profile_full.field_type` |

**USA 补充**：`field_profile_perf.family` 是**字段前缀簇**（如 `fnd93_accruals_d1_*`），不是语义维度——它正好用来做「同族换字段」（杠杆④），不要拿它当维度覆盖的分组。

---

## 三、Step 3 配模板：8 个统计族（≠ 机制族）

**先分清两套词表，混用会虚报覆盖**：

| 词表 | 数量 | 用途 | 计数口径 |
|---|---|---|---|
| **8 统计模板族**（本文） | 8 | 对**已锁定字段**做变换覆盖，用于盲区清除 / 判死取证 | `full_coverage_gate` 闸 2 |
| **GEM 机制族** | 9 | 经济机制与组合结构（event_conviction_ratio / event_gated_signal / …） | `family_id`，绑定生成池 |
| 论坛 / 论文机制 | 不限 | 主体设计来源 | **不折算成统计族** |

> 用户指示：**经济机制模板不限于 8 个，应按字段与机制充分匹配**。8 统计族不是机制清单，也不得替代机制设计——它只保证「同一字段的常见变换面没有被漏掉」。

**决定统计模板的是频段，不是机制**（EUR 256 次标定矩阵；**USA 未复现，按先验处理**）：

| 字段频段 | 最佳 | 次佳 | 最差 |
|---|---|---|---|
| 慢频文本 / 事件 | 一阶 / 二阶差分 | 事件衰减 | 双窗秩乘积 |
| 慢频分析师预期 | 双窗秩乘积 | 横截面秩 | 二阶差分 |
| 高频价量 | 双窗秩乘积 + 横截面秩 | 时序秩 | 差分族 |
| 慢频基本面（比率） | 横截面秩 / 冠军栈 | 双窗 | 二阶差分 |

**8 个统计族（判死必须全试；`F` = 单字段，先做 `vec_*` / backfill）**：

| # | 族 | 表达式 |
|---|---|---|
| 1 | 冠军栈 | `signed_power(ts_zscore(ts_backfill(F,BF),ZW), 1.5)` |
| 2 | 横截面秩 | `rank(ts_backfill(F,BF))` |
| 3 | 一阶差分 | `ts_delta(ts_backfill(F,BF),W1)` |
| 4 | 二阶差分 | `ts_delta(ts_delta(ts_backfill(F,BF),W1),W1)` |
| 5 | 双窗秩乘积 | `multiply(rank(ts_mean(ts_backfill(F,BF),WS)), rank(ts_mean(ts_backfill(F,BF),WL)))` |
| 6 | 时序秩 | `ts_rank(ts_backfill(F,BF),ZW)` |
| 7 | 事件衰减 | `ts_decay_linear(ts_backfill(F,252),66)` |
| 8 | 波动调整 | `divide(ts_delta(ts_backfill(F,BF),W1), add(ts_std_dev(ts_backfill(F,BF),ZW), 0.0001))` |

**窗口一律落到 `config.STANDARD_WINDOWS`**（锁定项：1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260）。EUR 标定表里的 **21 / 63 / 126 不是合法档**，不得为复刻标定而破例；映射时保持 WS < WL，并把你实际用的窗口写进本波 `key_findings`。一组可用起点（日频）：`BF=22 / WS=5 / WL=66 / ZW=252 / W1=22`；季频：`BF=252 / WS=66 / WL=252 / ZW=504 / W1=66`。

**USA 既有算子证据（优先于 EUR 标定）**：`ts_av_diff` > `ts_zscore(ts_backfill(...))`（慢变量，实测 S 2.07 vs 1.78）；`reverse` 必须与原方向成对发批；`winsorize` 必须具名 `std=`；`2Y` 高且 `TO > 0.5` 多为假强（详见 [six-step-usa-override.md](six-step-usa-override.md) ⑤）。

---

## 四、Step 4 派发：三闸先过（USA 有两处 fail-open）

```bash
$WQ_PY tools/full_coverage_gate.py --region USA --dataset <ds> \
    --exprs-file cache/_cand.txt --campaign-dir tracking/USA --gate-mode enforce
# 需要字段级 100% 时加 --coverage-mode field；历史 n_tests 全 0 时加 --dim-tested-by verdict
```

| 闸 | 语义 | 判据 | USA 现状（2026-10-21 实测） |
|---|---|---|---|
| 1 维度覆盖 | 每个语义维度至少被 1 条候选触及 | `coverage ≥ 1.0`；字段数 <3 的族并入「其他」；≤10 字段的小集退回字段级 | **未跑 loader ⇒ `SKIP`**（不是 PASS）；跑完 loader 后正常判 |
| 2 模板族 | 本数据集历史已试 ≥`--min-families`（默认 3）个统计族；判死需 8 族全试 | 读 `expressions.family` ∪ 战役目录文件 ∪ `WQ_TEMPLATE_FAMILY` | **USA `expressions.family` 全 NULL** ⇒ 历史恒 0；只带当前波环境变量时最多 1/3 ⇒ 恒 WARN |
| 3 边界算子 | 算子参数在 `boundary_ops_<region>.json` 合法档内 | 非法档 / 近闸未穷举 | **USA 无该文件** ⇒ 配置为空 ⇒ **恒 PASS** |

**结论：`exit 0` 不等于过闸。** 三道闸里两道在 USA 当前是「未启用」形态：

- **闸 1**：先跑 `load_field_profiles_to_db.py --region USA`，否则 `SKIP`；
- **闸 2**：族账要**手工记**——每波派发时设 `WQ_TEMPLATE_FAMILY=<统计族>`，并在数据集档案里列出「已试族」；`expressions.family` 未落库前，闸 2 的 WARN 不是「没试过 3 族」的证据；
- **闸 3**：要么先在 `tracking/USA/reference/` 下建 `boundary_ops_usa.json`（该文件当前不存在；以 EUR 同名文件的 schema 为模板，但每个档位需 USA 实测背书），要么用 `--boundary-config` 指向一份已标定配置；**文件不存在时的 PASS 不入判死证据**。

**`full_template_campaign.py` 不能直接用于 USA**：它硬编码 `region='EUR'`、`TOPCS1600`、`decay 4`、`neutralization FAST`、`max_trade ON`，并调用仓库外的 `C:/Users/MENGTAO/wqb-scripts/wqb_tools.py`。USA 只借它的 **EV 公式与 8 族模板**；派发走 `workflow_batch_track` / `tools/submit_batch.py`，按本区设置（`explain --region USA`）逐项显式传参。

**派发纪律**：模板优先派发（每批只含一个统计族，收割顺序才不会映射错）；`delay 0` 探针单独成批；multisim 2–10 条共享设置、按表达式去重。

---

## 五、Step 5 收割 + 归因（先归因再推进）

| 情况 | 判据 | 动作 |
|---|---|---|
| 全波 max_S < `thresholds.near.sharpe_min` | 信号弱 | 先看 8 族覆盖是否真做完；未做完不得换集 |
| S 过近闸线但未过主闸 | 近闸 | 进定向开发（Step 6），不扩同形态批 |
| S 过但 2Y 不过 | `get_alpha_yearly_stats` | 查死年 → 中性化（杠杆②） |
| S 过但 prod 不过 | prod 直方图 | 单钉 → 换字段；密墙 → 换持仓域（见 [gate-and-submit-discipline.md](gate-and-submit-discipline.md)） |
| 1–2 闸不过 | `failed_ra_count ∈ {1,2}` | **先跑 `tools/gate_attribution.py`**（零仿真），按 D16 路由；不得无诊断盲扫 |
| ≥3 闸不过 | — | 不属近闸机制，回常规诊断 / `s4-prescreen` |

**prod 直方图定性**（决定处方，不是调参）：贴线桶（0.70–0.80）只有 1–2 颗 → 换字段 / 换分组轴可破；同桶几十颗 → 密墙，必须换持仓集合，换字段无效。处置一律按决策表 D0-P，禁止同族磨参数。

---

## 六、Step 6 定向开发：四杠杆链（USA 改写）

| 杠杆 | 形态 | 负责闸 | 证据 |
|---|---|---|---|
| ① 双窗秩乘积 | `multiply(rank(ts_mean(ts_backfill(F,BF),WS)), rank(ts_mean(ts_backfill(F,BF),WL)))` | **SUB** | EUR 0.62→1.00；USA 待实测 |
| ② 中性化 | EUR：`neutralization=FAST`；USA：`SECTOR` 破 fitness/margin，`REVERSION_AND_MOMENTUM` / `CROWDING` 破 prod | 2Y / prod | EUR 2Y 1.46→2.09；USA prod 0.70+→0.648（RAM） |
| ③ `signed_power` 0.7–0.8 | 外层压缩 | S | EUR +0.06；USA 未复现，先小批验证 |
| ④ **换字段 / 换测量面** | 同族 `_pct`/`fy1`/`fy2` 变体；或换 `ts_rank` 长窗等测量面 | **prod（且常同时保 SUB）** | EUR prod 0.77→0.685；USA `board_gov` 的 SUB 墙由 `ts_rank(·,504)` 测量面打破，而非后处理 |

**铁律**：同一信号族里，任何「改后处理」都是**用一个闸换另一个闸**；只有**换字段 / 换测量面**能同时保住两个（同族字段的 prod 钉子互不相关）。这也是「扩批前先按族查 prod-first」的原因。

---

## 七、Step 7 全闸验证（以平台返回为准）

| 闸 | 线（来源） |
|---|---|
| `LOW_SHARPE`（D1） | `config.PLATFORM_CHECK_LINES['low_sharpe_min']['delay1']` |
| `LOW_FITNESS`（D1） | `config.PLATFORM_CHECK_LINES['low_fitness_min']['delay1']` |
| `LOW_2Y_SHARPE` | `config.PLATFORM_CHECK_LINES['low_2y_sharpe_min']` |
| `LOW_TURNOVER` / `HIGH_TURNOVER` | `config.PLATFORM_CHECK_LINES['turnover_range']` |
| `LOW_SUB_UNIVERSE_SHARPE` | **比率闸 ≈0.43×S**（USA 实测；EUR 文章的 0.53×S 不适用） |
| `LOW_ROBUST_UNIVERSE_SHARPE` | 以 `submit_verdict` 的 RA 明细为准 |
| prod / self | `config.GATES_PLATFORM['prod_corr_max']` / `['self_corr_max']` |
| `CONCENTRATED_WEIGHT` | 人工判（本区 `cw_gate=WARN`，代码未读取） |
| `CLUSTER_TEST` | 平台返回为准；WARNING 非阻塞 |

```bash
# 判定否决权（只拦不放行）
$WQ_PY tools/submit_verdict.py --alpha-id <id>
# 相关性：prod 与 self 双端点，提交前必须刷新
mcp__wq-brain-http__check_correlation(alpha_id=<id>, refresh=True)
mcp__wq-brain-http__check_self_correlation(alpha_id=<id>)
# 逐年归因
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id=<id>)
```

**提交铁律**：`submit_verdict` 通过只是「没被否决」，**放行权威 = 用户明确确认 + `confirm_submit=True`**；`PC` 只向上漂，提交前必须重测；同族逐个提交、每提交一颗就重测剩余候选（互残 >0.9 立即放弃）。

---

## 八、Step 8 标绿 / 判死 / 存档

- **全闸过** → `set_alpha_properties(color=GREEN, name, tags, descriptions)`，等用户决定提交。
- **近闸**（仅差 1–2 闸）→ `YELLOW` + `near-gate` 标签 + 写明唯一失败闸与归因。
- **存档**：单集字段档案写 `../references/_usa-<字段前缀>-field-profile-<asOf>.md`（见 [fnd67](../references/_usa-fnd67-field-profile-20261019.md) / [fnd93](../references/_usa-fnd93-field-profile-20261019.md)）；台账只经 MCP 写入（`upsert_wave_result` / `upsert_registry_empirical` / `seal_dead_end`），不手写战役 JSON。

**判死升级（2026-10-21 起）**：

1. **数据集级 `dead_end`** 必须同时满足：**三闸全过 + 8 个统计族全试 + 全波次 `|S|` 低于判死线**。任一闸未过 = 未做尽，不允许判死。
2. **D15 的 `fast_kill`（8 探针无 `|S| ≥ 0.5`）只到字段 / 探针级**，不再单独支撑数据集级判死。
3. **旧档追认**：`fundamental67`（8 条，最高 S 0.64）、`fundamental93`（12 条，最高 S 0.99）、`fundamental91`（4 类机制全 ≤0.58）都是**探针级**结论——可作「暂不优先」，不得再当「该集已死」的依据。已在类别扫描顶部加追记。
4. 判死前先 `forum_recon`，再 `seal_dead_end`（取证闸 fail-closed，见决策表 D15）。

---

## 九、已知陷阱

**文章 10 条（通用）**：

| 陷阱 | 现象 | 解法 |
|---|---|---|
| VECTOR 事件层算术 | `multiply does not support event inputs` | 先 `vec_*` |
| VECTOR + `ts_backfill` | `ts_backfill does not support event inputs` | 先 `vec_*` |
| 全正字段裸 zscore | 极端值主导 | 先 `rank` |
| 已是变化量再差分 | 信号被毁 | 用 level 或累积 |
| level 类不做规模体检 | 正交后归零 | 先做规模中性体检 |
| 收割顺序 ≠ 提交顺序 | 模板映射错 | 模板优先派发（每批一个族） |
| 只测 3 个模板就判死 | 误判 | 8 族全试（铁律） |
| EV 高 = 能出活 | 错 | EV 只反映拥挤度 / 覆盖 / 未测占比 |
| 同族后处理调参 | 一闸换一闸 | 换字段 / 换测量面 |
| 把 8 统计族当机制族 | 覆盖虚报 / 机制缺失 | 两套词表分开记 |

**USA 追加（都是本区实测）**：

| 陷阱 | 现象 | 解法 |
|---|---|---|
| 三闸 fail-open | `exit 0` 但维度 `SKIP`、族 `WARN 0/3`、边界 `PASS` | 见 Step 4；缺省 PASS 不入判死证据 |
| `expressions.family` 全 NULL | 族闸永远读不到历史 | 手工族账 + `WQ_TEMPLATE_FAMILY` |
| 无 `boundary_ops_usa.json` | 边界闸形同虚设 | 先建配置，或明确声明「闸 3 未启用」 |
| `full_template_campaign.py` | 硬编码 EUR / TOPCS1600 / 外部路径 | 只借公式与模板，USA 用 `workflow_batch_track` |
| `winsorize` preflight 误报 | `unknown_fields:["std"]` | 以 toolkit 静态闸 + 平台为准 |
| `reverse` 单发 | 负 Sharpe 被误判死 | 与原方向成对发批 |
| 2Y 高 + TO 高 | 假强 | 先看 `turnover_range` 与 reverse 后读数 |
| 判毒看 coverage | 元数据 cov 高但 `longCount=0` | 看 `longCount` |
| `query_profile.py stats` | 未建画像时曾抛 `NoneType.__format__` | 已修为提示；仍要先建画像 |

---

## 十、命令速查

```bash
# 一次性建 USA 画像（294 集 / 85,184 字段；sem_type 仍为 NULL）
$WQ_PY tools/load_field_profiles_to_db.py --region USA

# 选集 / 看集 / 维度
$WQ_PY tools/query_profile.py datasets --region USA --sort ev --limit 30
$WQ_PY tools/query_profile.py fields   --region USA --dataset <ds>
$WQ_PY tools/query_profile.py dims     --region USA --min-dim-cov 1.0

# 派发前三闸（注意 USA 的 SKIP / WARN / PASS 含义）
WQ_TEMPLATE_FAMILY=<stat_family> $WQ_PY tools/full_coverage_gate.py \
  --region USA --dataset <ds> --exprs-file cache/_cand.txt \
  --campaign-dir tracking/USA --gate-mode enforce

# 回测 / 收割 / 详情
$WQ_PY tools/submit_batch.py --path <exprs.txt> --region USA ...   # 其余参数按 explain 逐项显式传
mcp__wq-brain-http__harvest_multisim_alphas(multisimulation_location=<multisim 位置>)
mcp__wqb-db__harvest_multisim_results(region="USA", wave="<W>", alphas=<上一步返回>)
mcp__wq-brain-http__get_alpha_details(alpha_id=<id>)

# 判定 / 相关性 / 逐年
$WQ_PY tools/submit_verdict.py --alpha-id <id>
mcp__wq-brain-http__check_correlation(alpha_id=<id>, refresh=True)
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id=<id>)
```
