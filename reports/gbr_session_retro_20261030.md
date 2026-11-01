# GBR D1 会话挖掘复盘：历程、欠账、skills 改动清单

> 生成日期：2026-10-30
> 范围：GBR / TOP700 / D1 的 REGULAR 提交线战役（2026-10-28 ~ 10-30）
> 目的：把本轮**推翻旧结论**的部分与**未沉淀的欠账**分开列清，避免下一轮照着过时的 skill 段落重踩。
> 状态：清单 **15 项已于 2026-10-30 全部施工完毕**，逐项落点见 §六；§一~§五 保留施工前的原始判断，被推翻处已就地标注。

---

## 一、挖掘历程（六阶段）

### 阶段 1 · 数据集重扫，推翻了「GBR 已挖穿」的旧裁决

`get_datasets(GBR, D1, TOP700)` 实读 **177 → 183 个数据集**，而非 skills 记录的 177。
关键推翻：`techindi_model` 被旧表记成「三字段同一条腿」，实读 **399 字段 / 25667 alphaCount / 1818 users / valueScore 2.0 / multiplier 1.6**。
**教训**：一条字段数事实错误足以翻掉整张「无空间」表。

### 阶段 2 · 电话会议语言数据 8/8 整体判死

- `analyst83`（345 个 VECTOR 字段）：6 个结构互异模板 / 5 机制族全灭，S ∈ {0.29, 0.07, −0.18, −0.18, −0.25, −0.26}，最佳 = 闸的 18.4%，F 上限 = 闸的 8.9%。
- `fundamental45`（同源姊妹集）：双模型分歧 S −0.57 / 双重差分 S −0.17，2 条探针亦全灭。

判死前曾误判「coverage 0.33 是硬伤」，用 `longCount 456 / shortCount 455` 排除 —— **覆盖不是问题，信号才是**。

### 阶段 3 · 塔位权威盘点，推翻三个认知

用 `get_pyramid_alphas(2026-10-01 ~ 12-31)` + `get_pyramid_multipliers()` 拿到唯一事实源：

| 塔 | GBR D1 现值 | D1 乘数 | 缺口 |
|---|---|---|---|
| model | 5 ✅ | 1.5 | — |
| analyst | 3 ✅ | 1.6 | — |
| pv | 1 | 1.4 | 2 |
| other | 1 | 1.6 | 2 |
| fundamental | 0 | 1.6 | 3 |
| sentiment | 0 | **1.7（最高）** | 3 |
| 其余 10 塔 | 0 | 1.2–1.6 | 3 |

**D0 全塔为 0 —— D1 才是战场。**

三个认知修正：

1. **信用/违约类归 MODEL，不归 RISK。** `3qVa2Lze`（`annualized_pd_2_year_jc7`）实测 `pyramid_short="model"`、`pyramids.list=[GBR/D1/MODEL, 1.5]`，且已 ACTIVE；`npPWX19w`（`mdl28_credit_structural_leverage`）同样归 MODEL。⇒ **GBR 的 RISK 塔（0/3）事实上被 MODEL 吞并，「找 RISK 数据集点 RISK 塔」是白做工。**
2. **塔位不可从 `dataset_id` 推断。** `ds=291` 一个槽位同时装两种塔位：`rKRkL9QE` / `WjOkLGWx` 是 PV+FUNDAMENTAL，`9qxQamje` 是 OTHER。
3. **本地近似闸口径作废。** `region_id=7` 会混入 EUR：`YPxLWdpv` 本地 S3.36/F1.49/TO64.66% 看似全过，实为 **EUR/TOPCS1600** + `LOW_SUB_UNIVERSE_SHARPE` 1.63 < 1.78。⇒ 全闸判据只认平台 `ra.failed_ra_count` / `checks.fail`，区域只认 `settings.region`。

### 阶段 4 · `fnd6_<科目> / cap` 族 = 唯一量产线（本轮最大增量）

骨架 `rank/group_rank(ts_quantile(ts_av_diff(divide(fnd6_<X>, cap), W), Q, driver=gaussian))`，设置 `INDUSTRY` + decay 10 + trunc 0.05 + nanHandling OFF + maxTrade OFF。
权威核出 **13 条 `failed_ra_count=0`**（施工前误记为 10 条，实为 S≥1.58 全量），S 1.59–2.21 / F 1.26–2.05 / TO 7.5–12.3% / 2Y 1.89–2.51。

3 条已测 prod：`rKRkL9QE` **0.6783** / `WjOkLGWx` **0.6577** / `0mYoANkv` **0.6932** —— 全过，但余量仅 0.007–0.042 ⇒ **薄余量族**。

经济学基础：`divide(基本面科目, cap)` 同时具备价值（PV）与基本面科目（FUNDAMENTAL）属性，**不是平台巧合，是可复用的「一鱼两塔」模式**。

### 阶段 5 · 四个族被判死

| 族 | 判据 | 关键数字 |
|---|---|---|
| `tm_16` + `tm_17`（techindi 时序模型） | prod 全族饱和 | 19+ 条落 **0.7343–1.0** |
| `annualized_pd_*`（ds=111） | 归 MODEL + prod 爆 | 7 条全闸通过里 4 条 prod **0.9893–0.9985** |
| `pv47_spret` | prod 饱和 | 13/13 prod ≥ 0.7 |
| `quant_factor_lib + risk60` | **权重混合违规** | `multiply(rank(B), 0.3/0.5/0.7)` + 只扫权重网格 |

### 阶段 6 · 数据集侧挖穿，收敛到单一动作

183 集交叉三方判死层（平台 `hard_excluded` 158 / 平台 `dead` 5 / 本地 `registry_empirical` 33）后：
**「既未判死又 coverage>0」的未点亮塔数据集 = 0 个。**

11 个真空塔逐个判无路径：

| 塔 | 无路径原因 |
|---|---|
| sentiment(1.7) / news / insiders / institutions / shortinterest / socialmedia | 对应 category 的 GBR 数据集已全判死 |
| earnings / macro / option | GBR coverage = 0 |
| imbalance | cov 0.16–0.18 且字段只有 2×2 自由度 |
| risk | 语义被 MODEL 吞并 |
| other | `tm_*` prod 饱和 + `other47/384/455` 判死 |

**唯一剩余路径**：提交 `rKRkL9QE` + `0mYoANkv` + `WjOkLGWx`，pv 1→4 + fundamental 0→3，一次点两塔。**用户已选「暂不提交」。**

---

## 二、产出盘点

| 类别 | 数量 | 位置 |
|---|---|---|
| 可提交候选（全闸 + prod<0.70 + self 全 PASS） | 10 条篮子 + 3 条双塔 | 台账 `gbr_basket_v2`、`reports/gbr_basket_v2_20261030.md` |
| `fnd6_/cap` 全闸通过弹药 | **13 条**（3 条已测 prod：0.6577 / 0.6783 / 0.6932） | `reports/gbr_pyramid_audit_20261030.md` §4 |
| 判死条目 | GBR `dead_end` **65 条**（其中 34 条带 `payload.dataset` 绑定） | `registry_empirical`，补齐过程见 §三 A3 |
| 判死信号族 | 6 族 | 本报告 §一 阶段 5 |
| 模板库 | 4 份（analyst83 / other384 / other47 / pv109）+ **索引** | `docs/reference/README.md`（本轮新建，一次索引全 47 份） |
| 字段画像 | 4 份（fundamental6 / news104 / news18 / shortinterest3） | `docs/reference/` |
| 数据集经验文档 | **新建 6 份 GBR**（analyst83 / fundamental45 / fundamental6 / other384 / other47 / techindi_model）+ README 升级为跨区索引 | `reports/dataset_experience/` |
| 报告 | 5 份（pyramid_audit / basket v1 / basket v2 / mining_experience / 本复盘） | `reports/` |
| 改动的核心代码 | `src/wqb/store/_pyramids.py` 重写（改读 `is.checks[MATCHES_PYRAMID]`）+ `src/wqb/towers.py` docstring 精确化 | 见 §六 A1 / A1b |

**10 条篮子的相关性证据**：self 0.2693–0.6364 全 PASS；10×10 互相关 `max_subset_exact: true`、最大配对 `0mYoANkv × WjOkLGWx = 0.5615`、`missing_pnl: []`、1021 个日收益点；`failed_ra` 全 0。

---

## 三、待完善项（非 skills）

### A1 · 【高】塔位列读不到，每轮被迫逐条回平台（已修：A1 + A1b）

`alphas` 表**没有** pyramid 列、没有 decay / truncation 列。后果：282 条候选池只能靠 `region_id` 粗筛，而 `region_id=7` 混 EUR ⇒ 大量时间烧在逐条 `get_alpha_details` 核 region 上（本轮约 4 次 GET 才推翻 1 条假候选）。

**建议**：新增 `alpha_pyramids(alpha_id PK, region, delay, universe, tower, multiplier, effective, verified_at)`，harvest 时从 `get_alpha_details` 一次写入；或给 `alphas` 加 `pyramid_towers TEXT`（逗号分隔）+ `settings_fingerprint TEXT`。

**施工结果（已按此建表并跑通）**：`src/wqb/store/_schema.py` 加 `alpha_pyramids`（18 列 + 索引），`src/wqb/store/_pyramids.py` 全量重写（14497 B）。回填 6 条 → 8 个塔位相关列 **0 个 NULL**。

**但真正的根因不是"没建表"，是"建了也写不进"**：旧 `_pyramids.py` 去读 `detail["pyramids"]` 与 `detail["ra"]`，而 REST `GET /alphas/{id}` 里 **`pyramids` 恒为 `None`、`ra` 键根本不存在** —— 塔位实际藏在 `is.checks[]` 的 `MATCHES_PYRAMID` 项（MCP 的 `ra` / `pyramids` / `checks.fail|pass` 全是 `mcp_core.py:187-223` 从 `is.checks` 归一化出来的）。所以任何走 REST 原样字段的采集都会静默写 NULL，且表面上"采集成功"。⇒ 同类问题的排查顺序应是**先确认字段在平台响应里的真实路径**，再怀疑"表缺列"。

`src/wqb/towers.py` 的模块 docstring 同步改成"位置找错了，不是平台没给"，并给 `infer_tower()` 标注「⚠ 兜底专用」+ 两个系统性偏差（只返回一条腿、倍率用数据集级值 1.4 而实际 3.0，少算 2.14 倍）。

### A2 · 【中】`submit_ready` 混区行 + 失效行（已修正）

初读结论「60 行 = DEAD 55 / SUBMITTED 5 / READY 0，队列已空」**是把 ASI 切片当成了全表**。全表实读 **1948 行 = DEAD 1428 / SUPERSEDED 204 / READY 186 / SUBMITTED 80 / EXPIRED 41 / PROD_BLOCKED 7 / SELF_BLOCKED 2**。

对 GBR 的 79 条 READY 逐条 `GET /alphas/{id}` 复核（不占 prod 槽）：

| 分类 | 条数 | 处置 |
|---|---:|---|
| 平台实为 **EUR**（`region_id=7` 混区） | **41** | `region: GBR → EUR` |
| 真 READY（region=GBR、`fRA=0`、仍 UNSUBMITTED） | **31** | 保留 |
| `fRA>0`（闸已失效） | **7** | `status → DEAD`、`gate=FAIL:RA:<项名>` |

修正后 **GBR READY 79 → 31**、EUR READY 48。可回滚备份 `logs/a2_submit_ready_rollback_20261030.json`（41 条 region_fixes + 7 条 dead_marked）。

31 条 REAL_READY 的结构：pv 系 10 条、analyst 5 条、MODEL 4 条（全 STATISTICAL/decay12）、OTHER 1 条（`P0gxk2dx` SUB **1.75**）、**FUNDAMENTAL 0 条** —— 唯一 FUNDAMENTAL 路径仍是回填的那 3 条 `PV+FUNDAMENTAL`。另有 4 条指标逐位相同（`WjLqPzpQ` = `RRA3AnPg` = `e76p6oWd` = `zqrMr1LG`，均 2.02/1.03/20.31%/1.44），属同表达式重复落库，不可当 4 个独立候选。

**原建议「加 `archived` 列」已作废**：`submit_ready` **没有 `archived` 列**，MCP `get_submit_ready` 也不按它过滤 ⇒ 加列对读数零收益。真正的病是**混区行**与**闸已失效行**，已按 `region` / `status` 原地修正，未动表结构（`UNIQUE(alpha_id, region)` 允许同 id 跨区并存，事前已确认无 EUR 副本冲突）。

### A3 · 【高】判死数据集未落 `registry_empirical`（已补 9 条）

初读时 GBR `dead_end` 只有 56 条，本轮对话里判死的集大半没进表。**已补 9 条，GBR `dead_end` 56 → 65 条**（其中 34 条带 `payload.dataset` 绑定）。

12 个待补项逐个回表核对后有两个反转：

- `pv109` / `other455` **本来就在库** —— 初读漏掉是因为我用 `payload.dataset` 做过滤，而部分历史条目不带该字段（属"条目缺 dataset 绑定"，不是"条目不存在"）。
- `pv47_spret` 不必单列 —— 已被 `pv47` 条目覆盖。

实补的 9 条：`analyst93`、`pv30`、`other47`、`other384`、`institutions1`、`institutions4`、`fundamental45`、`techindi_model`（tm_16 / tm_17 全族）、`annualized_pd`（ds=111）。

**残留**：33 条历史条目缺 `payload.dataset`（本轮原计数里的"33 条 registry"即指这批），它们进不了 `profile` 精确层；补绑定是独立活，需逐条读表达式里的字段名反推数据集。

### A4 · 【中】`reports/dataset_experience/` GBR 0 个（已补 6 份）

该目录实读 10 个文件：`deu_shortinterest3` / `eur_×7` / `kor_shortinterest38` / `usa_analyst_consensus` / README —— **GBR 一个都没有**，而 `brain-dataset-mining-experience` 明确要求每波 S6 后按数据集产出 `<region>_<ds>_campain.md`。

**施工结果**：新建 6 份（`gbr_analyst83` / `gbr_fundamental45` / `gbr_fundamental6` / `gbr_other384` / `gbr_other47` / `gbr_techindi_model`），并把 README 由「EUR D1 单区索引」重写为**跨区索引**（GBR 6 行 + EUR 7 行 + KOR/DEU/USA，带「结论类型」列区分量产线 / 判死）。目录现为 17 份。

### A5 · 【中】prod 单并发无排队机制（并入 P1-6）

账号级单并发 + 兄弟会话共享。本轮实测 holder 连续轮换 `1Yj08nb6 → XgRM3Yra → 1Yj08nb6 → XgRM3Yra → LL522ZRe → 0mjaa2Ev`，仅在 lock 释放的短暂窗口抢到 2 次。抢到后平台常算 >120s ⇒ MCP 客户端超时、结果不落缓存、本机 inflight 残留 300s。

**建议**：加「待测队列 + 优先级」而不是随机抢；约定「同族先测族代表」（见 skills 改动 P1-6）。

**施工结果**：已随 P1-6 一起写进 `wq-prod-corr-read`（族代表先测 / 排队顺序 / 3 条反模式），未新增独立排队机制 —— 单并发是平台侧约束，本地队列只能决定**测谁**，不能提高吞吐。

---

## 四、skills 改动清单

> 清单总计 **15 项** = skills 侧 11 项（P0 4 / P1 2 / P2 3 / P3 2）+ 工程与数据侧 4 项（A1 / A1b / A2 / A3）。逐项施工结果见 §六。

### P0 —— 现有表述已被本轮实测推翻，会直接误导下一轮（4 项）

#### P0-1 `wq-brain-ra-gbr/SKILL.md:281` 与 `:290` —— tm_17「干净新枝」结论反了

**现有文本**：
> `tm_17` 与已提交的 `tm_16` self 相关仅 **0.0238**，是干净新枝，2026-10-29 已推到 `failed_ra_count=0`

**本轮实测**：tm_17 族（ds=291）19+ 条全闸通过，**prod 落 0.7343–1.0**：
`N1NogQ87` 0.8439 / `O0Av1nZd` 0.8333 / `kqNlzEAK` 0.8719 / `88R1XNo7` 0.7736 / `3qoLJb16` 0.7945 / `rKRX8Jd1` 0.7919 / `YP1qR9wA` 0.7716 / `npvVQ8WE` 0.7343 / `XgJzLbl1` 0.8413、0.8891、1.0。

**根因**：`self` 与 `prod` 回答的是**两个不同问题**。self 只说明「不撞自己已提交池」，prod 才说明「不撞整个生产池」。tm_17 与自家 tm_16 self 干净，但在生产池里同机制 alpha 已经很多。

**改法**：原句后插入推翻块 —— `⛔ 2026-10-30 推翻：tm_17 族 prod 实测 0.7343–1.0（19+ 条），OTHER 塔在 techindi 上仍无第 2 条腿。self 0.0238 只证明它不撞自家 tm_16，不证明它不撞生产池。`

#### P0-2 `wq-brain-ra-gbr/references/risk.md` —— 缺「RISK 塔被 MODEL 吞并」

现文件判死记录只有 1 条（`GBR-DELAY0-INFEASIBLE`），**完全没有**本轮这条铁律。

**改法**：在 risk.md 顶部加：
> ⛔⛔ **GBR 的 RISK 塔（0/3）事实上不存在**：信用/违约类字段被平台 `MATCHES_PYRAMID` 统一并入 MODEL。
> 实证：`3qVa2Lze`（`annualized_pd_2_year_jc7`）`pyramid_short="model"`、`pyramids.list=[GBR/D1/MODEL,1.5]`，已 ACTIVE；`npPWX19w`（`mdl28_sm_structural_multiple_credit_structural_leverage`）同样归 MODEL。
> ⇒ 不要为「点 RISK 塔」去找 RISK category 数据集；该塔在 GBR 实际由 MODEL 通道吸收。

#### P0-3 `wq-brain-ra-gbr/references/fundamental.md:88` —— `GBR-FUNDAMENTAL6-CEILING` 与本轮实证冲突

**现有 dead_end**：
> `GBR-FUNDAMENTAL6-CEILING` … fundamental6 质量/价值族（atq/revt/oancf/oiadp/gpy/**capxy**/dpy 等）不再生成 —— GBR TOP700/**SUBINDUSTRY** 下规模因子暴露主导，无超额信号

**本轮实测**：`fnd6_<科目> / cap` 族 S≥1.58 共 **13 条**，**全部 `failed_ra_count=0`**，S 1.59–2.21 / F 1.26–2.05 / 2Y 1.89–2.51；其中 3 条已测 prod 0.6577–0.6932 全过。设置是 `INDUSTRY` + decay 10 + trunc 0.05 + nanHandling OFF + maxTrade OFF。

**根因（施工时修正过一次）**：初判是「该 dead_end 缺设置档指纹，判死当时用 SUBINDUSTRY、本轮换 INDUSTRY 档复活」。回读原 payload 证据后发现**真正变量是分母**：原判死证据全是 `X/Y` 同量纲会计比率（如 `atq/revt`），**从未覆盖 `X/cap` 跨量纲形式**。⇒ 不是"换档复活"，是原结论的适用范围本来就不包含 `divide(科目, cap)`。

**改法（已落）**：给该条加 `scope_correction_20261030`，把禁用范围**收窄**为「`X/Y` 同量纲会计比率」，**不**采用"换设置档复活"的口径 —— 否则下一轮会以为换档就能救活任何被判死的族。
**并加通用规则**：`dead_end 条目必须带设置档指纹（中性化/decay/truncation/nanHandling/maxTrade）；本条另证明「分母形式」（X/Y vs X/cap）是同等重要的适用范围维度。`

#### P0-4 `wq-brain-ra-gbr/SKILL.md:240` —— 塔位判定条款只否掉了 category，未否掉 dataset_id

**现有**：
> ⚠ **塔位判定不要用数据集的 `category` 猜**：`techindi_model` 的 category 是 `other`，但塔位只能读 alpha 详情 `is.checks` 的 `MATCHES_PYRAMID`（或 `pyramids.list`）

**缺的两层**：
1. `dataset_id` 同样不可推断 —— `ds=291` 一个槽位同时装 PV+FUNDAMENTAL（`rKRkL9QE`/`WjOkLGWx`）与 OTHER（`9qxQamje`）。
2. **盘塔位有零成本权威入口**，现有文本没给：`get_pyramid_alphas` + `get_pyramid_multipliers`。

**改法**：拆成三条 —— ① category 不可猜 ② `dataset_id` 不可推断（举例 ds=291）③ 盘塔位用 `get_pyramid_alphas(start,end)` + `get_pyramid_multipliers()`，零仿真成本；单条核塔位读 `ra.pyramid_short` 与 `pyramids.list`。

### P1 —— 新增本轮高价值资产（2 项；原列 3 项，P1-7 已并入 P1-6）

#### P1-5 `wq-brain-ra-gbr/references/fundamental.md` —— 补 `fnd6_<科目>/cap` 双塔族

现文件**零提及** `fnd6_*`（grep 无匹配）。这却是本轮唯一能量产 FUNDAMENTAL 塔（0/3）的线。

**补入内容**：13 条全表（alpha / 字段 / S / F / TO / 2Y / SUB / margin / prod）+ 「一鱼两塔」归因 + 薄余量警告（余量 0.007–0.042）+ 扩招纪律（**必须换财务科目，不许换窗口**；换窗口是伪多样性）。

#### P1-6 `wq-prod-corr-read/SKILL.md:49` —— 补「量产前测族代表」例外

**现有**：
> 终验只测**马上就要提交的那一颗**。测完不提交的，48h 后作废，等于白占槽。

这句本身对，但缺另一半：**在量产一个族之前，应先花一次 prod 测「族代表」，用它的值决定要不要量产**。两者是不同阶段，不冲突。

**本轮证据**：
- `shortinterest3`（USA）族代表 `kqNRbvJP` prod **0.8463** ⇒ 同族 `Xg9qjVOz` / `gJezNxjg` 优先级直降，省下 2 次 prod 时隙。
- GBR `fnd6_/cap` 三条已测 0.6577–0.6932 ⇒ 薄余量，第 4 条起撞墙概率不低 ⇒ 扩招需谨慎。

**改法**：在 :49 后加一段「族代表预判（与终验是两件事）」，含上述两个证据 + 决策规则「族代表 ≥0.80 ⇒ 同族其它候选优先级降到最低，不逐颗花 90–240s 验」。

#### P1-7（合并进 P1-6，不单列）

### P2 —— 跨区通用教训（3 项）

#### P2-8 `wq-prod-lever-self-lock-guard` —— 补「self 干净 ≠ prod 干净」的机理段

现有「双端点取 max、都过线才可提」的**结论正确**，但缺机理说明，导致 P0-1 那类误用（把 self 0.0238 当成整体干净）。

**补入**：两端口径对照表 + tm_17 反例（self 0.0238 / prod 0.7343–1.0）+ 一句话判据：**self 干净只排除了「撞自家池」，prod 必须单独测。**

#### P2-9 `wq-operator-playbook-by-gate` —— 补 `vector_neut` 第二参必须无量纲

skills 全库搜 `vector_neut.*无量纲` **无匹配**（只有 shortinterest scan 里一条 hump 的 unit 警告）。

**本轮 DEU 实测**：`vector_neut(主体, <股数/金额字段>)` 报
`Incompatible unit for input of "vector_neut" at index 1, expected "Unit[]", found "Unit[TSShare:1]"`。
命中字段：`total_sell_shares` / `vec_sum(num_jobs_removed)` / `vec_sum(loaned_share_count_p5_d1)`（全带 `Unit[TSShare:1]`），三条配对残差同批全废。
**修法**：第二参外先包 `rank()`（输出 [0,1] 无量纲）。

#### P2-10 `wq-wave-preflight-dispatch` —— 补 `region_id` 混区污染

现有只写了「`region_id` 是**数字外键**」「三段联表」，是**结构层面**的正确提醒，但缺**数据层面**的陷阱：

`alphas.region_id=7` 会同时装 GBR 与 EUR。实测反例 `YPxLWdpv`：`region_id=7`、S3.36/F1.49/TO64.66%/2Y1.89 看似全过，实为 **EUR/TOPCS1600**、`failed_ra_count=1`（`LOW_SUB_UNIVERSE_SHARPE` 1.63 < 1.78）。

**改法**：在 region_id 说明处加「★ `alphas.region_id` 不能单独判区：同一 id 会混多区（GBR 与 EUR 实测同为 7）。从 `alphas` 表筛候选后必须回 `get_alpha_details.settings.region` 复核。」

### P3 —— 流程欠账（2 项）

#### P3-11 `brain-dataset-mining-experience` —— 本轮交付 0

该 skill 要求每波 S6 后产出 `reports/dataset_experience/<region>_<ds>_campain.md`。实读目录 **10 个文件里 GBR 0 个**，而本轮 GBR 判死 14+ 数据集。

**动作**：补产出，优先 `gbr_analyst83` / `gbr_fundamental45` / `gbr_techindi_model` / `gbr_other47` / `gbr_other384` / `gbr_fundamental6`（这 6 个有完整实测数字）。

#### P3-12 模板库缺索引

`docs/reference/` 下 4 份 `template_library_*.md` + 4 份 `field_profile_*.md`，**无 README 索引**。下一轮不知道该读哪份、哪份已被后续实测修正。

**动作**：加 `docs/reference/README.md`，列 `文件名 / 数据集 / 生成日期 / 结论（判死·存活）/ 被哪份报告修正过`。

---

## 五、优先级建议

> 表为施工前拟定顺序，**状态列**于收尾时回填。

| 序 | 项 | 理由 | 状态 |
|---|---|---|---|
| 1 | **P0-1 tm_17 结论** | 唯一会**主动误导**下一轮去挖一条已判死的路 | ✅ |
| 2 | **P0-2 RISK 吞并** | 防下一轮为点 RISK 塔白开波 | ✅ |
| 3 | **A3 补 9 条 dead_end** | 补齐后 `get_dead_ends("GBR")` 才是完整事实源 | ✅ 56→65 |
| 4 | **P0-3 设置档指纹** | 通用性最强：影响所有区域的 dead_end 可信度 | ✅ |
| 5 | **P1-5 fnd6_/cap 入库** | 唯一可复用的量产线，不写就丢 | ✅ |
| 6 | **P1-6 族代表预判** | 直接省 prod 时隙（本轮最稀缺资源） | ✅ |
| 7 | P0-4 / P2-8 / P2-9 / P2-10 | 补齐后能少踩 4 类具体坑 | ✅ |
| 8 | A1 / A2 / A4 / P3-11 / P3-12 | 结构性改善，收益在下一轮 | ✅ |

---

## 六、施工结果（2026-10-30 收尾，15 项全落地）

skills 根有两份：主 `C:/Users/MENGTAO/.claude/skills/`、仓库镜像 `D:/coding/traeCN_project/wqb/Claude/skills/`。本表落点均指**仓库镜像**（本会话实际读写的那份）。

| # | 项 | 落点 | 验证 |
|---:|---|---|---|
| 1 | P0-1 tm_17 推翻 | `wq-brain-ra-gbr/SKILL.md:281` 插入 `⛔ 2026-10-30 推翻` 块；`:290` 表格该行加删除线 | 19+ 条 prod 0.7343–1.0 已写入正文 |
| 2 | P0-2 RISK 吞并 | `wq-brain-ra-gbr/references/risk.md` 顶部新增整节 | 证据 `3qVa2Lze` / `npPWX19w` 均 `pyramid_short="model"` |
| 3 | P0-3 收窄 CEILING | registry `GBR-FUNDAMENTAL6-CEILING` payload 加 `scope_correction_20261030` | 原证据全是 `X/Y` 同量纲会计比率，从未覆盖 `X/cap` ⇒ 真正变量是**分母**，不是设置档 |
| 4 | P0-4 塔位三铁律 | `wq-brain-ra-gbr/SKILL.md:240` 拆三条（category 不可猜 / `dataset_id` 不可推断-举例 ds=291 / 盘塔位用 `get_pyramid_alphas`+`get_pyramid_multipliers`） | 零仿真成本入口已写入 |
| 5 | P1-5 双塔族弹药库 | `wq-brain-ra-gbr/references/fundamental.md` 新增 `fnd6_<科目>/cap` 整节 | 13 条全表 + 薄余量 0.007–0.042 + 扩招纪律（换科目、不换窗口） |
| 6 | A3 补 dead_end | `registry_empirical` GBR `dead_end` **56 → 65** | 本表 §三 A3；9 条新条目 |
| 7 | P1-6+A5 族代表预判 | `wq-prod-corr-read/SKILL.md` §四·1 族代表预判 / §四·2 排队顺序 / 另加 3 条反模式 | `kqNRbvJP` 0.8463 代表撞墙、`fnd6_/cap` 0.6577–0.6932 薄余量 |
| 8 | P2-8 self≠prod | `wq-prod-lever-self-lock-guard/SKILL.md` 新增整节 + 决策速查 1 行 | tm_17 self 0.0238 / prod 0.7343–1.0 对照 |
| 9 | P2-9 量纲规则 | `wq-operator-playbook-by-gate/SKILL.md` §2.7 | `vector_neut` 第二参 `Unit[TSShare:1]` 报错原文 + `rank()` 修法 |
| 10 | P2-10 混区污染 | `wq-wave-preflight-dispatch/SKILL.md` §0.0.6b + 坑 #3/#4 + §3 可信度分层 | `YPxLWdpv`（region_id=7 实为 EUR/TOPCS1600） |
| 11 | A1 塔位解析 | `src/wqb/store/_pyramids.py` 全量重写（14497 B），改读 `is.checks[MATCHES_PYRAMID]` | 回填 6/6 成功，8 个塔位列 **0 个 NULL** |
| 12 | A1b docstring | `src/wqb/towers.py` 模块 docstring + `infer_tower()` 标「⚠ 兜底专用」 | 记录 `j["pyramids"]→None` / `j["ra"]→KeyError` 实读对照 |
| 13 | A2 队列修正 | `submit_ready`：41 条归 EUR、7 条降 DEAD | GBR READY 79→31；备份 `logs/a2_submit_ready_rollback_20261030.json` |
| 14 | A4/P3-11 经验文档 | `reports/dataset_experience/` 新建 **6 份 GBR** + README 由「EUR 单区索引」重写为跨区索引 | 目录实读 17 份，其中 `gbr_*` 6 份 |
| 15 | P3-12 模板库索引 | `docs/reference/README.md` 新建（12737 B） | 索引 47 份，**逐文件读首行核对**，非凭猜测 |

### 施工中新查到、原报告没有的事实

1. **`6XKwmQgE` 是 ANALYST 塔候选**（`pyramids.list=[GBR/D1/ANALYST, 1.6]`、`fRA=0`）。此前盘点把它混在 pv 系里，A1 修好后才显形。
2. **`fnd6_/cap` 族 S≥1.58 实为 13 条**（原报告写 10 条），**全部 `failed_ra_count=0`**：`rKRkL9QE` 2.21 / `QPveQvOg` 2.06 / `N1NM5WK8` 2.05 / `P0oerpjp` 1.98 / `0mYoANkv` 1.89 / `RREXA1qn` 1.77 / `6XdxzNb5` 1.75 / `0mYo9Ok1` 1.73 / `WjOkLGWx` 1.72 / `kqNRXm5k` 1.70 / `88RAnmAX` 1.67 / `P0oeqZap` 1.64 / `9qxoa3mx` 1.59。
3. **`alphas.dataset_id` 是第三层元数据污染**（继 `region_id`、`universe` 之后）：该 13 条全记成 `dataset_id=291`，真实 `fundamental6` 是 **368**、`techindi_model` 是 579。⇒ 归集候选只能靠 `backtest_results.dataset` 或表达式里的字段名。
4. **`backtest_results` 里 `analyst83` / `fundamental45` / `other47` / `other384` 各 0 行** —— 这几个集的判死证据只存在于 skill 文档与 registry payload，**没有回测流水**。下一轮若只信库会被"无记录"误导成"没测过"；这也是为什么要落 dead_end 条目而不是只写文档。
5. **A2 的 41 条混区行此前持续污染候选池**：`region_id=7` 同时装 GBR 与 EUR，任何"从 `alphas` 表筛 GBR 候选"的查询都会带进 EUR 假候选（本轮实测每条假候选要 ~4 次 GET 才能推翻）。
6. **`persist_correlation(rKRkL9QE, prod=0.6783)` 已补落库**，此前只有 `WjOkLGWx` 0.6577 / `0mYoANkv` 0.6932 在库 ⇒ 三条双塔候选的 prod 证据现在齐了。
7. **registry `GBR-FUNDAMENTAL6-CEILING` 的示例列只存了 10 个 alpha id**（缺 `RREXA1qn` / `0mYo9Ok1` / `P0oeqZap`），而同一 payload 的 `sharpe_range` 写的是全 13 条的区间 1.59–2.21 —— **这正是本轮"10 条 vs 13 条"漂移的源头之一**。已补全为 13 条并加 `n_alphas` 字段，旧 payload 备份 `logs/registry_fnd6_ceiling_payload_backup_20261030.json`。教训：**列举证据时"示例 N 条"必须显式标注是示例还是全量**，否则下一个人（或下一轮的我）会把示例数当全量数。

### 仍然没做的（诚实列出）

- **33 条历史 dead_end 缺 `payload.dataset` 绑定**：进不了 `profile` 精确层，需逐条读表达式字段名反推数据集，属独立活。
- **`6XKwmQgE` 未做进一步确认**：只见塔位，未核 2Y / SUB / prod，也未与 pv 系候选算互相关。
- **没有提交任何 alpha**：用户已选「暂不提交」，3 条双塔候选（pv 1→4、fundamental 0→3）仍挂在 `submit_ready` 里。
- **11 个真空塔仍无路径**：本轮只证明「GBR 现有数据集里没有」，没证明「这几个塔在 GBR 挖不出来」。

---

## 七、一句话结论

本轮真正的产出不是「10 条候选」，而是**三个认知修正**（塔位不可推断 / RISK 被 MODEL 吞并 / 本地近似闸作废）、**一个可复用模式**（`divide(基本面科目, cap)` 一鱼两塔）、和**一条写作纪律**（dead_end 条目必须带设置档指纹，否则只在原档内成立）。

收尾前的欠账是「只有一鱼两塔进了 skills」；**本轮已把三条认知修正与设置档指纹纪律全部写入 skills + registry**，并顺带修掉两个会让下一轮白做功的工程缺陷（塔位列解析错、候选池混区）。剩下的欠账是数据侧的：33 条 dead_end 缺 dataset 绑定、4 个已判死数据集缺回测流水。
