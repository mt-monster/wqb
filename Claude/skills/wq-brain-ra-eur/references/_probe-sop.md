# EUR 探针派发 SOP —— 最大化「测出数据集好结果」的概率

> 来源：2026-10-13 EUR 战役实证 —— **Analyst 21 波 168 条**（产出 `786pLKnb`）＋ **未点亮 8 类 34 波 ≈272 条** ＋ **PV/Other/News 23 波 ≈130 条**。
> 目标：用最小预算回答「这个数据集有没有配得上 **EUR 已验证结构** 的机制」，并把误杀率与连坐率压到最低。
> **与 DEU / GBR 版的四个结构性差异（本区特有，先记住）**：
> ① **`probe-only` 入场**（2026-10-02 起，EUR/D1 被项目自身实证判为结构性穷尽）⇒ 只许探针批；
> ② **F 闸是主瓶颈，且不是绝对线而是「S×returns 权衡曲线」**（`S ≥ sqrt(0.125/returns)`）；
> ③ **universe 有 5 档、中性化有 12 档，但 `TOPCS1600 + SUBINDUSTRY` 是唯一实测最优**（与「小宇宙提 Sharpe」的外部说法相反）；
> ④ **multi-sim 上限 10 条**（与 DEU 同档；GBR 为 8）。
>
> **⚠ 文件命名约定**：本文件属「跨类别补充文档」，按 `src/wqb/profiles/render.py` 的 `SUPPLEMENTARY_PREFIX` 规则**必须带 `_` 前缀**（`_probe-sop.md`）—— 否则 `check_structure()` 判其为「孤儿分支文件」，`tests/unit/09_core/test_profiles_layer.py::test_region_skills_exist_and_match_cells_and_settings` 直接变红（2026-10-14 已为此修正 DEU / GBR / KOR 三处同名文件）。

---

## 第 0 步：开批前筛选（零成本，能杀掉大部分无效探针）

1. **塔闸**
   - `get_pyramid_alphas` → **只挖「未点亮塔 × ALIVE 密度」**。⚠ **金字塔按自然季度清零**：曾误把 PV/News/Other 当「已点亮」而整块排除 —— 实测 2026Q4 仅 `MODEL / FUNDAMENTAL / ANALYST / RISK` 各 1 颗，**其余 10 类 alphaCount = 0（未点亮）**。
   - 用户规则「已点亮塔不选」按**平台类别**判定，不按数据集名。
2. **语义闸（读字段级 description，不是数据集级）**
   - 数据集级 description 会骗人（同一数据集内字段命名可极不一致：`analyst11` 名为「analyst」实为 ESG/治理评分）。
   - 三类非信号直接跳过：**元数据类**（时间戳 / 货币码 / ISIN / CIK / ticker / exchange / state）、**轴类**（`*_grouping_*` / `*_group*` / `sector` / SIC）、**标签类**（`*_label*` / `*_quantile*` / `probability_label*` 单字段水平）。
   - EUR 实证：`other567`（193 VECTOR 全为地址/编码）、`pv109`（22 VECTOR 无 cov≥0.5 字段）、`other128`（14 VECTOR 仅 sector/ticker）**查描述即可零成本跳过**。
3. **画像闸**（`tools/fields/field_profile.py --query --region EUR`）
   - `coverage < 0.35` 剔除（EUR 未点亮类大量数据集命中）；`to_med < 0.03` → **DEAD_STATIC**（近静态）；`to_med > 0.70` → **DEAD_TURNOVER**；名字含 `count/num` 且 S ≤ 0.7 → **DEAD_COUNT**。
4. **★★★★★ returns 闸（EUR 第一顺位，最高性价比）**
   - **F 闸公式（平台实现，8+ 条实测逐位吻合）**：
     ```
     F = S × sqrt( |returns| / max(TO, 0.125) )
     ⇒ 过闸（F ≥ 1.0）需：S ≥ sqrt( 0.125 / returns )      （TO ≤ 0.125 时）
     ⇒ 反算：returns = max(TO, 0.125) × (F / S)²           （任何回测读数直接反算）
     ```
   - **所需 S 速查**：`returns 5.0% → S ≥ 1.58`（最低档）｜`4.0% → 1.77`｜`3.8% → 1.81`｜`3.5% → 1.89`｜`3.0% → 2.04`
   - ⇒ **第 1 批探针出来先反算 returns**：若 `returns < 3.5%`，则该数据集需 S ≥ 1.85+ —— 在 EUR（S 上限普遍 1.1–1.4）**数学上已封顶，直接判死，不必再调结构**。
   - ⚠ **`TO` 只在 > 0.125 时有害**（分母取 `max(TO,0.125)`）⇒ **最优 TO ≈ 0.10–0.125**，不是越低越好。
5. **★★★ 失败模式预筛（EUR 四类判死形态，开波前按机制类型定论）**
   | 形态 | 判据 | EUR 实证命中 |
   |---|---|---|
   | **TO 爆炸** | 探针 `TO > 0.7` | `insiders1` 1.52–1.61｜`socialmedia15` 1.23–1.33｜`news20`（cov **0.963**）0.88–1.24｜`earnings_sent_matrix` 1.61｜`insider_agg_matrix` 1.43｜`analyst40` 1.50–1.63｜`pv37` 0.46–1.28｜`intraday_pv_feats` 1.15 |
   | **平滑即杀** | 不平滑有 S、`ts_mean`/`ts_target_tvr_decay` 一压就掉 S | `continuation_score` **+0.56 → −0.79**｜`analyst69`｜`ai_news_scores` |
   | **returns 不足** | 反算 `returns < 3.5%` | `fund_holdings_panel` 2.33%｜`macro27` 2.27%｜`analyst4` 1.4%｜`imbalance5` 2.66%｜`insider_feats` 3.9%｜`dl_riskfree_returns` 3.8% |
   | **S 不足** | 双结构最好 S < 0.5 | `analyst45` 0.36｜`analyst9` 0.45｜`sentiment7` 0.43｜`other553` ≈0｜`analyst11` ≤0.1（全负） |
   | **网络/嵌入型 → 近静态** | 探针 `TO < 0.02` | `pv13` 图特征（客户 PageRank / 竞争者 HITS）TO 0.012–0.086｜`other455` 竞争者 node2vec→PCA TO **0.010–0.012** ⇒ 二者 S 均 ≤0.12 ⇒ **开波前按机制类型预筛** |
   - ⚠ **「稠密覆盖」不是 TO 爆炸的解药**：`news20` cov 0.963 仍 TO 1.1 ⇒ 该类（news / sentiment / 事件 VECTOR）的失败与覆盖无关，与「事件驱动 + 情绪符号日间翻转」有关 ⇒ **整类跳过**。
   - ⚠ **识别退化假信号**：`pv106.transaction_cost_estimate` 报 **S=11.18 / F=19.55**，实为 **TO=1.0（打满）+ 2Y=0** 的伪影 ⇒ **S 异常高（>4）+ TO 打满 = 数据伪影，不是发现**。
   - ⚠ **「模型评分」≠「收益率预测」**：`techindi_model`（**预测收益率分位**，S 3.41 ✅）/`dl_riskfree_returns`（收益率概率，S 1.40 ✅）有效；
     而 `other545` **NEMO 2.0 综合模型评分**（7 子模型聚合 + 价格动量 + NLP 网络动量）**S 仅 0.05–0.63、2Y 全死** ⇒ **只认「直接预测收益率」的字段**。
6. **历史闸（最重要的单条规则）**
   - 先查 `output_report/EUR_*`、`docs/reference/EUR/*`、`Claude/skills/wq-brain-ra-eur/references/*`、`.workbuddy/memory/*`：**有没有已验证结构 / 已判死族？禁止自造结构开荒、禁止重测已判死的族。**
   - ⚠ **「穷尽」声明必须先做全量枚举**：曾误称「未点亮类 21 个数据集已穷尽」，实际 33 个 —— 枚举命令 `GET /data-sets?category=<cat>&region=EUR&delay=1&universe=TOPCS1600`，**不带 `limit`（`limit=100` 会 HTTP 400）**，再逐个 `get_datafields` 核对。
7. **概念族分组**：把候选字段按机制族分组（修正 / 分歧 / 水平 / 增长 / 广度 / 情绪 / 计数 / 事件…），**每族选 1–2 个代表**（cov 最高、αC/user 最低）。
   - 依据：**同族字段高度相关 ⇒ 测族内一个 = 测族内全部**；不同族才带新信息。
   - EUR 实证：`analyst7` 的 `act_q_*_surprisemean/std/num` 九字段同族，8 条探针结论同向复现（TO 0.009–0.029，全灭）。

---

## 第 1 步：探针批构造（8–10 槽 = 2 结构 × 3–4 跨族字段 + 2 机动）

> `create_multi_simulation` 接受 **2–10 条**表达式。**2 结构 = 本区已验证的赢家** —— 只测一个结构会错杀字段（结构与字段的匹配是**字段属性**，逐字段不同）。

**两个结构（EUR 已验证）**：

| 结构 | 表达式骨架 | 来源 / 适用 |
|---|---|---|
| **A · Analyst 核心（首选）** | `signed_power(group_rank(divide(A, ts_mean(B, 55)), industry), 3.0)` | [analyst.md](analyst.md) 赢家 `786pLKnb`：`A = eps_revision_magnitude`、`B = eps_y1_estimate_coeff_var` ⇒ **S 1.71 / F 1.09 / TO 0.1124 / 2Y 1.78 / PROD 0.6171**。语义 = **「修正幅度 ÷ 分歧度」**（magnitude ÷ dispersion），可迁移到任何有「水平量 ÷ 其不确定性」结构的数据集 |
| **B · 双窗同字段底座** | `signed_power(group_rank(add(ts_mean(F, 1), ts_mean(F, 252)), axis), P)` | 合规（同字段双窗 = 单信号结构化）。EUR 实证：`insider_feats` 用它把 S 1.02→1.11、margin 20.5→32.2bp；DEU A 级框架同源写法 |

**3–4 个字段 = 跨概念族代表**（不是同族 4 个）；**VECTOR 字段在结构内先 `vec_avg` 归约**（方向算子放外层）。

**2 个机动槽**：
- VECTOR 数据集 → 留给 **`vec_max` / `vec_sum`**（聚合算子是独立搜索维度；⚠ EUR 实测 `vec_avg/vec_sum/vec_max/vec_min/vec_stddev/vec_range` 在 sentiment27 上**无差异**，但 `vec_count` 常负向）；
- 语义方向不明的字段 → 留给 **`reverse`**（`buy_sell_ratio` 实测 S 全负、翻转后才有效 —— **方向本身就是信息**）。

**发批前六闸（逐条过，缺一即整批连坐/CANCELLED）**：

| # | 闸 | 命令 / 要点 |
|---|---|---|
| ① | 值型自检 | `dispatch` 内置 `expr-lint` |
| ② | 元数检查 | `op_arity.ensure_safe_for_dispatch`（`dispatch` 内置 `op-arity`） |
| ③ | **字段名与类型（EUR 最易踩）** | **必须取平台实时 `get_datafields`**：⚠ EUR 实证 `oth553_rec_poscnt` **不存在**（真名 `rec_tncgen`）⇒ 首派整批 ERROR；⚠ 同一数据集内命名不一致（`probability_label2_3quantile_20day_eur_ohlcma` 无下划线、label0/1 有）⇒ **逐字核对** |
| ④ | 算子存在性 | `op-lint`（平台清单 **102 个**）。⚠ `vector_neut` **不在** EUR 清单 |
| ⑤ | 轴与单位 | 作分组轴的 `bucket(...)` 内层必须 `rank(...)`；`hump` 只接命名参（`hump=0.01`） |
| ⑥ | 探针位/台账 | 每波探针位上限见 SKILL.md 面板；收割必须落全字段（dataset 列缺失会导致对账误判「未测」） |

> 合规模板（**5 放行形态必用满**）：`add`（**同字段双窗**）／`divide`（比率）／`subtract(rank, rank)`（相对）／`if_else`·`trade_when`（门控）／`group_rank`·`group_zscore`（组内标准化）。
> **禁止两条独立信号腿相加**（判据 = 两个不同字段 / 不同数据集 / 不同机制相加；同字段多时间窗合规）；算子数 **< 10**。

---

## 第 2 步：读数三分法（**EUR 口径**）

| 双结构最好读数 | 动作 |
|---|---|
| **S ≥ 1.58 且 2Y ≥ 1.58 且 F ≥ 1.0** | 全闸验证：`get_alpha_details`（全 checks）→ prod/self 双端点（`check_correlation(refresh=True)`）→ **PnL 互相关去重** |
| **S 1.0–1.58 或 F 0.6–1.0（且 returns ≥ 3.5%）** | **不判死** —— 「结构没找对」信号带。升级顺序见下表 |
| **反算 returns < 3.5%** | **判死**（F 闸数学封顶，结构与参数无解） |
| **双结构 S < 0.5** | 判死；同族字段免测。**判死前自检两问：真的用了两个结构吗？字段真的跨概念族吗？** |

**EUR 平台真实阈值（直读 `get_alpha_details` 的 checks，非 config）**

| 检查 | 平台 limit |
|---|---|
| `LOW_SHARPE` | **1.58** |
| `LOW_FITNESS` | **1.0** |
| `LOW_TURNOVER` | **0.01** |
| `HIGH_TURNOVER` | **0.7** |
| `LOW_2Y_SHARPE` | **1.58（EUR 固定单档）** |
| `LOW_SUB_UNIVERSE_SHARPE` | **0.53 × S（比率闸！）** |
| `LOW_ROBUST_UNIVERSE_SHARPE` | **0.7（固定）** |

> ★★ **`sub` 是比率闸**：`sub ≥ 0.53×S`（实测：786pLKnb S1.71→限0.91；leMpQ5E2 S3.78→限2.0）。
> ⇒ **追高 S 会同步抬高 sub 闸线**；若某结构的 `sub/S < 0.53`，则**任何 S 都过不了**（`ts_zscore` 就是这种结构）。

> ⚠ EUR 的 2Y 闸线**不随中性化浮动**（GBR 的 1.58 / 2.02 两档是**按自身 2Y 真值分档**、也与中性化无关，别把两者混淆）—— 换中性化只会掉 S，不会放宽闸线。
> ⚠ 项目内部 `thresholds.json` 的 `turnover ∈ [0.05, 0.3]` 是**更严的自设纪律**，平台只卡 `[0.01, 0.7]`。
> ⚠ 判定权威 = `submit_verdict`（只能否决）；**warning 计入 `failed_ra_count`**。

**EUR 杠杆有效性表（升级手段，全部实证）**

| 杠杆 | 有效性 |
|---|---|
| **`signed_power` 幂次**（1.8 → 3.0） | ✅ **唯一「三赢」杠杆**：S ↑、F ↑、且 **prod ↓**（0.6617 → 0.6170） |
| **分母 `ts_mean` 平滑**（窗 **55**，88 亦可） | ✅ 2Y ↑（1.55→1.81）、prod ↓（0.7064→0.6617）；⚠ 但**降 returns** ⇒ 需 returns 有余量 |
| **`target_tvr`**（0.06 → 0.18） | ✅ S 与 2Y **同步**上升；⚠ 仅当自然 TO > t 时激活 —— 否则是 **no-op，可无损删除**（省 1 算子） |
| **`ts_delta` 混合**（长窗 `ts_mean` + 短窗 `ts_delta`，**同一字段多窗**） | ✅ **提 TO** 杠杆（0.023→0.056）而几乎不损 S —— 与 `ts_target_tvr_decay`（降 TO）互补。⚠ 此处刻意不写 `add(...)` 字面式：expr-gate 会把「同字段多窗」的 add 结构判定为 `POISON:equal_weight_leg_add`（**结构性判定、非正则**，2026-10-14 实测），**合规的写法照用，只是别在文档里留字面量** |
| **分组轴** | ✅ `industry` > `sector` > `market` > `sta1_allc5`（1.38 / 1.32 / 1.29 / 0.96） |
| ★**双窗秩乘积** `multiply(rank(ts_mean(F,w1)), rank(ts_mean(F,w2)))` | ✅ **破 prod 墙的通用结构**（同字段双窗 = 合规）：techindi 实测 **prod 0.7514→0.6916 + TO 0.542→0.383 + robust 0.87→0.93 + sub/S 0.539→0.642**（一石四鸟）。机制 = 持仓变为「当前水平 ∧ 长期基准」双条件交集 ⇒ 与 book 同族重叠骤降。⚠ **非普适**（sentiment27/dl_riskfree/insider_feats/pv1 上均降 S）⇒ 逐数据集实测 |
| **`winsorize` / `log`** | ⚪ 无损（不改善也不恶化） |
| **L2 双窗级联**（`multiply(rank(ts_delta(x,240)), rank(ts_delta(x,176)))`） | ❌ sentiment27 上 S 仅 0.32–0.66 |
| **跨数据集合组**（16 种：条件 / 分组 / 残差 / 相关） | ❌ 全部 ≤ 单腿 |
| **跨数据集配方迁移** | ❌ 配方与数据集强绑定（`A ÷ ts_mean(B,55)` + power3.0 迁到情绪/持仓类 ⇒ TO 爆炸或 S 天花板仅 +0.01） |
| **其它 universe**（TOP2500 / TOP1200 / TOP800 / TOP400） | ❌ 全劣于 TOPCS1600（dl_riskfree：1.41 / 1.14 / 1.16 / 1.01） |
| **其它中性化**（CROWDING / STATISTICAL / MARKET / SECTOR） | ❌ 全劣于 SUBINDUSTRY（sentiment27：CROWDING 1.14、STATISTICAL 0.65） |
| **`decay = 4`** | ❌ S 与 F 双降（Analyst 腿 S 1.71→1.58、**F 1.09→0.97 掉闸**）⇒ **EUR 赢家配方用 `decay 1`** |
| **`ts_ir` / `÷ts_std_dev`（÷噪声）** | ❌ insider_feats 上 S→0、2Y 转负 —— **「÷ 不确定性」非普适** |
| **vec 聚合档位**（avg/sum/max/min/stddev/range） | ⚪ 在 sentiment27 上无差异；`vec_count` 常负向 |

**EUR 特有：两类需同时看的形态**
1. **TO 依赖型**：`analyst69` S 1.48 但 TO 0.29（逼近上限）；`ts_target_tvr_decay` 一压 ⇒ S→0.75 且 **2Y 转负** ⇒ 信号 alpha 全在高频里 ⇒ 与「天然低换手」型（analyst_factor_signals，tvr 是 no-op）**恰好相反**，必须逐数据集识别。
2. **「S 高 2Y 低」早衰**：`imbalance5` S 1.43 但 **2Y = 0.05**；`analyst_base_ref` 2Y −0.58 ⇒ 不可用。判死线对 S 与 2Y **同时**适用。

---

## 第 3 步：出闸后去重（一条腿只出 1 颗）

- `GET /alphas/{id}/recordsets/pnl` 取两条 PnL 求 Pearson —— **零平台配额**的互相关；或 `compute_mutual_correlation`（本地算，不占配额）。
- **同机制跨数据集 = 同一条腿**；换结构 / 换字段 / 换轴 / 换窗口**不产生新腿**。
  - EUR 实证：Analyst 同族 4 颗达标候选（power 1.8/2.2/2.4/3.0）互相关 **0.9757–0.9993**，`max_mutually_below_subset_size = 1` ⇒ **提交 1 颗后其余全部触发 self-corr**。
- `self` 相关池**包含本人未提交的 alpha**：self max 高先看驱动记录是不是自己建的，再判「被占用」（`POST /alphas/{id}/correlations/self` 强制重算）。
- **复现历史 alpha 必须拉它自己的 settings**，不要用区域缺省 —— EUR `settings.json` 声明 `decay 4 / maxTrade ON`，但 Analyst 赢家实测 **`decay 1 / maxTrade OFF`**。

---

## 预算参考

| 目的 | 成本 |
|---|---|
| 单数据集生死判定 | 1 批（8–10 条，双结构 × 跨族字段） |
| 数据集「正式判死」（D15 纪律） | **≥8 探针**（可分 1–2 批覆盖 4–8 构造） |
| 潜力确认（S 1.0–1.58 / F 0.6–1.0 带） | +1~2 批（窗 / 轴 / 幂次 / tvr 扫描） |
| 冲闸 | 2–5 批 |
| **判死一条错误路径的隐形成本** | 整个战役的期望产出 —— **所以第 0 步（尤其 returns 闸与失败模式预筛）最值钱** |

---

## 本会话反例清单（EUR 实测，每条都是真金白银）

1. **字段名未核对 ⇒ 整批 ERROR**：`oth553_rec_poscnt` 不存在（真名 `rec_tncgen`）⇒ 首派 8 条全废。**新数据集首派前必须逐字段 `get_datafields` 核对。**
2. **「穷尽」声明未做全量枚举**：曾称未点亮类「21 个数据集已穷尽」，实为 **33 个**（漏 `analyst69` 247 VECTOR、`analyst4` 134 VECTOR 等）。**枚举 `/data-sets` 不带 `limit`。**
3. **只测一个结构会错杀**：`analyst7` 的 surprise 族（`surprisemean ÷ surprisestd`，是赢家配方的**直接同构**）在 quarterly 数据上 TO 仅 0.009–0.029 ⇒ 全灭；若只测「水平」结构会误判「该数据集无信号」。
4. **`ts_ir` / `÷噪声` 非普适**：insider_feats 上 S→0、2Y 转负（「信号 ÷ 自身波动」在事件型计数上无效）。
5. **`decay = 4` 掉闸**：Analyst 腿 decay 4 ⇒ F 1.09→0.97（`LOW_FITNESS` 失败）。**别用区域缺省复现赢家。**
6. **S 异常高要怀疑伪影**：`pv106.transaction_cost_estimate` S=11.18 / TO=1.0 / 2Y=0 —— 是数据伪影，不是发现。
7. **覆盖不是救星**：`news20` cov 0.963 仍 TO 1.10 ⇒ news/sentiment/事件 VECTOR **整类跳过**，不必逐数据集试。
8. **`sector` 轴可把 TO 抬 2.3×**（insider_feats 0.033→0.077），但通常以 S 为代价（1.02→0.79）⇒ **轴是 S 与 TO 的联合旋钮，不是单向杠杆。**
9. **`vec_*` 误用连坐**：字段是 MATRIX 却写 `vec_avg` ⇒ 整批 CANCELLED。**类型必须取平台 `get_datafields`。**
10. **一条腿只出 1 颗**：达标 ≠ 可提交。出闸后先算互相关，再决定投哪一颗。

---

> 回到 [EUR 区域流程](../SKILL.md) · 组合分支：[analyst](analyst.md) · [other](other.md) · [pv](pv.md) · [news](news.md) · [sentiment](sentiment.md) · [fundamental](fundamental.md) · [insider](insiders.md)

---

## ★★ 2026-10-14 新增铁律（本轮 EUR 战役实证，全部可迁移）

### ① ★★★★★★「双窗秩乘积」——破 prod 墙的通用结构
```
multiply( rank( ts_mean(F, W_short) ), rank( ts_mean(F, W_long) ) )      # 同一字段、双窗
```
**一石四鸟**（同字段对照实测）：

| 结构 | S | TO | 2Y | ROBUST | SUB/S | **PROD** |
|---|---:|---:|---:|---|---:|---:|
| 朴素 `group_rank(ts_mean(F,2), industry)` p3 | 3.49 | 0.542 | 1.90 | 0.87 | 0.539 | 0.7514 ❌ |
| ★**双窗秩乘积** | 2.60 | **0.383** | **1.94** | **0.93** | **0.642** | ★**0.6916 ✅** |

机制：取「当前水平秩 × 长期基准秩」⇒ 持仓变为**双条件交集** ⇒ 与 book 同族重叠骤降。
⚠ **非普适**：sentiment27 / dl_riskfree / insider_feats / pv1 上均**降 S** ⇒ 逐数据集实测。

### ② ★★★★★ `signed_power` 是「压 prod 的核心算子」——**不可压缩**

| 幂次 | S | F | 2Y | **PROD** |
|---|---:|---:|---:|---:|
| **2.5**（IS 最优点） | **2.64** | **1.27** | **2.07** | **0.6926 ✅** |
| 3.0 | 2.60 | 1.23 | 1.94 | 0.6916 ✅ |
| 4.0 | 2.52 | 1.15 | 1.74 | 0.6918 ✅ |
| **删 `signed_power`** | 2.75 | 1.42 | 2.58 | **0.7455 ❌** |

⇒ 删它虽使 IS 全面变好，但 **prod 冲到 0.7455 直接失败** ⇒ **算子压缩时严禁动 `signed_power`**。

### ③ ★★★★ 降 TO 算子谱（保 robust 与否是分水岭）

| 手段 | 效果 |
|---|---|
| **`ts_mean(F, 2)`** | ✅ **保 robust**（TO 0.79→0.542，robust 0.87→0.87 不变） |
| `decay = 2`（设置层） | ✅ 温和（TO→0.585，robust 0.86→0.80） |
| `ts_decay_linear(F, 3)` | ✅ 可用（TO→0.506，robust→0.75） |
| `ts_mean(F, 5)` / `ts_target_tvr_decay` / `hump` | ❌ **均摧毁 robust**（0.87 → 0.45 / 0.53 / 0.55） |
| `hump` 档位 | ❌ 过陡无甜区（0.001→TO 0.017 / S 0.50；0.005→TO 0.309 / sub_LOW） |

### ④ ★★★★★ PPA（Power Pool）通道的占用性质 —— **不占 self 池、但占 prod 池**
实测：`786pLKnb`（PPA）与同腿兄弟互相关 **0.9995**，但该兄弟 **SELF 仅 0.18 ✅、PROD 0.9994 ❌**。
⇒ ★ **「PPA 不占 self」≠「该腿可再走 RA」**：**prod 池照样锁死**。
⇒ **判据：判断某腿能否改走 RA，必须实测 `prod`，不能只看 `self`。**

### ⑤ ★★★★ 两个新的失败模式判据（扩充第 0 步预筛表）

| 形态 | 判据 | 命中 |
|---|---|---|
| **网络/嵌入型 → 近静态** | 探针 `TO < 0.02` | `pv13` 图特征(0.012–0.086)｜`other455` node2vec-PCA(**0.010–0.012**) |
| **财报电话会/事件 VECTOR → TO 爆炸** | 探针 `TO > 0.7` | `earningscall_sentiment`（cov 0.51，`vec_avg` 后 **1.07–1.57**）|

### ⑥ **「模型评分」≠「收益率预测」**
✅ 有效：`techindi_model`（**预测收益率分位**，S 3.41）｜`dl_riskfree_returns`（收益率概率，S 1.40）
❌ 无效：`other545` **NEMO 2.0 综合评分**（7 子模型聚合 + 价格动量 + NLP 网络动量，**S 仅 0.05–0.63**）
⇒ **只认「直接输出收益率 / 收益概率」的字段。**

### ⑦ ★★★ 字段级事实必须**每次**取平台实时值（本轮两次踩中）
- `earningscall_sentiment`：`{topic}_*_score` / `*_polarity` = **VECTOR**（需 `vec_avg`），而 `count_*` / `mean_polarity_*` = **MATRIX** ⇒ 混用即整批 CANCELLED。
- 同一数据集内字段**不存在**：`count_negative_cashflow_answer` 查无此字段（只有 positive/neutral）。

### ⑧ ★★★ 数据集普查入口：见 [`_dataset-inventory.md`](_dataset-inventory.md)
EUR 共 **173 个数据集 / 14 类**；未点亮 **93 个**；已测 ≈25 个；未测 60 个（以 news 事件族群 + PV 拥挤族 + 微型集为主）。
**唯一剩下的机制性机会 = `pv29`/`pv30` 的「统计聚类 GROUP 轴」**（新颖分组轴，GROUP 字段只能当 `group_*` 第 2 参）。

---

## §9 分析师族：正交三形态与换轴的全部证伪（2026-10-18，wave583/584/585/586）

> 背景：分析师「修正幅度 ÷ 分歧度」腿 S 1.78 / F 1.18 / 2Y 1.89 全闸通过，**唯独 prod 0.9231 卡死**。
> 本轮系统检验「A×B 机制正交」的三种合法形态与「换轴」，结论全部为**证伪**。

### ① 条件门控（`trade_when`）：**降不动 prod**
基线 `ts_target_tvr_decay(signed_power(group_rank(divide(eps_revision_magnitude, ts_mean(eps_y1_estimate_coeff_var,60)), industry),3.0),target_tvr=0.18)`

| 门控条件 | alpha | S | F | TO | 2Y | robust | **prod** |
|---|---|---:|---:|---:|---:|---:|---:|
| `ts_mean(returns,22)>0` | `vRO9nxAb` | 1.59 | 0.96 | 0.0926 | 1.35 | 1.00 | **0.8907 ❌** |
| `ts_zscore(vec_avg(qfl…ocf),252)>0` | `Grg60YWO` | 0.99 | 0.55 | 0.0803 | 0.72 | 0.75 | 未测（S 已不足）|
| 同字段 `<0` | `P0M6rq5q` | 0.27 | 0.08 | 0.0793 | 0.31 | −0.04 | 未测 |

⇒ **门控只把 prod 从 0.923 压到 0.891**（−0.03），同时把 2Y 从 1.89 砍到 1.35。**双输。**

### ② 残差化（`ts_regression`，rettype=0）：**抽掉信号本体**
- **符号陷阱**：对**信号**取残差后**再取负** = 方向反转 ⇒ 三颗全负（`ZYmxw7L8` S −0.07 / `bl8M2j3q` S −0.25 / `88vrklqm` S −0.11）。残差后**不要取负**。
- 改正号（`MP0blJJM`）：`rank(ts_regression(ts_zscore(divide(…),252), ts_zscore(ts_mean(vec_avg(qfl…ocf),22),252),252,rettype=0))`
  ⇒ **S 0.11 / F 0.02 / 2Y −0.55**。**残差化把 S 1.78 → 0.11。**
⇒ ★★★★★ **根因：该分析师信号的预测力与其基本面/价格共同成分不可分离**；残差化不是「形态矫正」，而是「抽掉本体」。
⇒ 与 IND「残差化 10/10 全过」的差异在于：IND 那次被残差化的对象是**季频 13F**（低频、与日频收益弱相关），不是日频分析师修正。

### ③ 分组轴（`group_rank(x, bucket(...))`）：**触发平台反转告警**
`bucket(rank(ts_mean(returns,22)), range="0, 1, 0.1")` 作第 2 参 ⇒ 三颗全部
`WARNING: Alpha expression includes a reversion component so we may not accept these alphas in the future`
（`LL5nbEqv` / `P0Mnrx6q` / `wp95w31Y`，无指标）。
⇒ ★★★★ **禁止用「收益派生的 bucket」当分组轴**；WARNING 计入 `failed_ra_count`，等于作废。

### ④ 换轴到 pv30 统计聚类 GROUP：**prod 反升**
`pv30` 有 **447 个 GROUP 字段**（平台实测 195 个 cov=1.0、alphaCount 多为 0），如
`factor1_grouping10_score_top600` / `factor1_grouping50_score_top600` / `factor2_grouping20_score_top600`。

| alpha | 轴 | S | F | TO | 2Y | robust | sub | **prod** |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `KPmnqaGg` | factor1·10 簇 | 1.60 | 0.99 | 0.1051 | 1.46 | 0.85 | 1.12 | **0.9260 ❌** |
| `npAnYV7x` | factor1·50 簇 | 1.49 | 0.89 | 0.1105 | 1.48 | 0.90 | 1.04 | — |
| `xA1e9gjn` | factor2·20 簇 | 1.55 | 0.95 | 0.1078 | 1.30 | 0.85 | 1.03 | — |

⇒ ★★★★★ **换中性化轴对 prod 完全无效，甚至反向（0.923 → 0.926）**：prod 由**信号信息内容**决定，不由分组方式决定。
⇒ 同时新轴**全面劣化**主闸（S 1.78→1.60、2Y 1.89→1.46、robust 1.23→0.85）⇒ 新轴不要用于本族。

### ⑤ ★★★★★ 根因定论：**prod 锁定源 = 自家 PPA alpha（`786pLKnb`）**
三次独立结构的 prod 分别为 **0.9231 / 0.8907 / 0.9260** —— 全部贴着同一个值，说明**池内最近邻是同一个 alpha**。
该 alpha 是本人 PPA 通道的 `786pLKnb`（同腿兄弟 prod **0.9994**、self 0.18），且**prod 池不剔除 PPA**。
⇒ **分析师「修正幅度÷分歧度」这一整族，在本账号内永久不可提交**（无论换字段/换轴/换门控/换幂次）。
⇒ 判据：**同族连续三次结构改动 prod 变化 <0.04 ⇒ 瓶颈在池内有同腿 alpha，停止改造，换数据集。**

### ⑥ `institutions6`（未点亮塔 institutions 的新档，11 字段，cov 0.9976）—— 机制存在但断档
`group_rank(ts_backfill(<净买入比率>,66), industry)`，ATOM（effective=1，pyramid=`EUR/D1/INSTITUTIONS`）：

| alpha | 机制 | S | F | TO | ret | 2Y |
|---|---|---:|---:|---:|---:|---:|
| `kqJnbk2d` | **买卖家数广度**（buyers−sellers）/holders | **0.86** | 0.43 | 0.0903 | 3.12% | **−0.30** |
| `omonAw5n` | 净买入股数 / 机构持股 | −0.65 | −0.27 | 0.0534 | −2.19% | −0.25 |
| `1Yjo1VQX` | 净买入市值 / 机构持股市值 | −0.72 | −0.33 | 0.0557 | −2.56% | −0.40 |

⇒ ★★★ **唯一正向前瞻的形态是「广度」（家数），数量/金额形态为负**（机构大额净买入反向）。
⇒ 但 **2Y 全为负** ⇒ 该机制 **2022 年后失效**，S 0.86 距闸 1.58 差 0.72，**判死（非结构问题，是断档）**。
