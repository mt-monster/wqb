# 探针派发 SOP —— KOR 版（最大化「测出数据集好结果」的概率）

> 来源：2026-10-09~14 KOR/D1 未点亮数据集战役（d18x–d218，约 300 条实证）。每一条规则背后都有真金白银的反例。
> 目标：用最小预算回答「这个数据集有没有配得上 **KOR 已验证构型** 的机制」，并把误杀率与连坐率压到最低。
>
> ⚠ **KOR 与 DEU 的三个结构性差异（决定了本 SOP 的写法）**：
> ① KOR 有两套**按字段形态分工**的已验证构型（PV 构型 / SH 构型），**不能互换**；
> ② KOR 有**两道机制级墙**（`LOW_INVESTABILITY` / `CONCENTRATED_WEIGHT`）+ **一道密墙**（`prod`）——
>    探针必须**直接命中「构型 + 破墙要素」**，否则信号再强也出不来（实证：shortinterest38 信号 S2.66 却全卡 CW）；
> ③ KOR D1 **只有 `TOP600`**，区域探针预算 **8 条/数据集**（比 DEU 的 10 条更紧）。

## 第 0 步：开批前筛选（零成本，能杀掉大部分无效探针）

1. **语义闸（读字段级 description，不是数据集级）**
   - 数据集级 description 会骗人（DEU `other532` 写「标识符映射」实为 Barra 残差收益）。
   - 元数据 / 代码 / 记账指示器直接跳过（`*_curcd`、SYMBOL 日期码、纯 index 代码）。

2. **画像闸**（`tools/fields/field_profile.py --query --region KOR`）
   - KOR 实测（`--build --region KOR`）：**33,618 字段** → ALIVE **18** / WEAK 19 / DEAD 112 /
     DEAD_STATIC 10 / AXIS_ONLY 3,008 / UNTESTED 23,239 / UNUSABLE 7,173。
   - 阈值：`coverage<0.6` 剔除（KOR 大头）；`to_med<0.03` → DEAD_STATIC；`to_med>0.7` → DEAD_TURNOVER；
     名字含 `count/num` 且 S≤0.7 → DEAD_COUNT。三类**开批前定论**。
   - **⚠ KOR 特有：不要用 ALIVE 过滤选集。** ALIVE 18 个**全部落在已点亮塔**
     （`other466`×10 [FUNDAMENTAL]、`shortinterest38`×7、`risk71`×1）—— 未点亮数据集里一个 ALIVE 都没有。
     **画像只看「单字段 S」，看不到「构型」**：`pv47_for_statssimple_only_spret` 连 ALIVE 都排不进，
     是构型把它做到 S1.90（4 颗 RA 全过）。⇒ **先判字段机制，再上构型。**

3. **历史闸（最重要的单条规则）**
   - 先查 `output_report/KOR_*`、skill `references/*`（`pv.md` / `shortinterest.md` / `analyst.md` / `risk.md`）、
     `.workbuddy/memory/*`：**有没有已验证构型？禁止自造结构开荒。**
   - 实证：analyst 族自造结构 5 个数据集全灭（S 天花板 ≈1.1）；pv47 换已验证构型后 S1.90。
     **「墙」常在「构型」不在「字段」。**
   - `field_profile` 的 S_sg 是历史最优回测行的读数——先反查那行用的什么构型，直接复用。

4. **概念族分组 + 形态判定（KOR 关键的一步）**
   - 把候选字段按机制族分组（水平量 / 变化率 / 计数 / 比率 / 评级 / 情绪…），**每族选 1–2 个代表**
     （cov 最高、α 最低）。依据：同族字段高度相关（同机制跨集 PnL **0.991**；同字段全结构变体 **0.9988+**）
     ⇒ **测族内一个 = 测族内全部**。
   - **先判字段形态再配构型**（KOR 特有，见第 1 步）：
     - **VECTOR 流量 / 比率型**（买卖量、成交额比、借券、资金流）→ **SH 构型**候选；
     - **MATRIX 日频收益分布型**（specific return、价量收益、残差收益）→ **PV 构型**候选。

## 第 1 步：探针批构造（8 槽 = 2 构型 × 3 跨族字段 + 2 机动）

> KOR 区域预算 = **8 条/数据集**（`wq-brain-ra-kor` profile 硬约束，比 DEU 的 10 条更紧）。

- **2 个构型 = KOR 仅有的两套已验证赢家（缺一不可）**。**构型最优性是字段属性，逐字段不同** ——
  只测一个构型 = 重蹈「SH 构型测 pv47 死、PV 构型测 pv47 活」的覆辙。

  **① PV 构型（"S 型"，适用：日频收益分布型 MATRIX 字段）**
  ```
  BASE  = multiply(rank(multiply(-1, ts_kurtosis(X, 140))),
                   rank(multiply(-1, ts_rank(X, 132))),
                   rank(multiply(-1, ts_rank(X, 252))))
  ALPHA = vector_neut( trade_when(greater(rank(adv20), 0.1), scale(BASE, shortscale=0.5), -1),
                       power(rank(rsk68_weight_dadv), 0.5) )
  设置：KOR / TOP600 / D1 · decay 4 · neutralization=MARKET · trunc 0.08 · nanHandling ON
  验证字段：pv47_for_statssimple_only_spret（PV 塔，S1.90 / 4 颗 RA 全过）
  ```
  - 三要素**缺一不可**：`ts_kurtosis(X,140)`（2Y 钥匙，K 窗口直接决定 2Y）+ `trade_when(adv20>0.1)`/`scale(shortscale=0.5)`
    + `vector_neut(·, power(rank(rsk68_weight_dadv), 0.5))`（investability 钥匙，残差到 RISK 塔美元 ADV 轴）。

  **② SH 构型（"流量/比率型"，适用：VECTOR 比率/流量字段）**
  ```
  ALPHA = hump( subtract( group_rank( divide(vec_sum(<A>), vec_sum(<B>)), industry), 0.5),
                hump=0.003 )
  设置：KOR / TOP600 / D1 · decay 4 · neutralization=SECTOR · trunc 0.08 · nanHandling ON
  验证字段：shortinterest38 的 vec_sum(sell_amt)/vec_sum(buy_amt)（S1.99 / F1.04 / 2Y2.03 / prod 0.6663 全闸过）
  ```
  - 二要素**缺一不可**：**居中放进 `hump` 内层**（`hump(subtract(·,0.5))`）—— 这是 `CONCENTRATED_WEIGHT` 的唯一破法。
    ⚠ 直接 `subtract(group_rank(·),0.5)`（不加 hump）⇒ CW 仍 **1.0**；`hump(group_rank(·))`（不居中）⇒ CW 仍 **1.0**。
  - **`vec_sum` 守卫 `add(·,1e-4)` 冗余**（分母恒正）—— 删掉既省 1 算子又让 S/F/2Y 全升。

- **3 个字段 = 跨概念族代表**（不是同族 3 个）。每字段按**形态匹配**的构型跑主测（VECTOR 比率 → SH；MATRIX 收益分布 → PV）。

- **2 个机动槽**：
  - VECTOR 数据集 → 留给 `vec_max` / `vec_avg`（聚合算子是独立搜索维度；`vec_count` 常负向）；
  - 语义方向不明 → 留给 `reverse`（方向本身就是信息）；
  - 形态不确定 → 留给「对照构型」（MATRIX 字段同时试 PV 构型 vs 拆坏的 kurtosis 单腿，验钥匙适用性）。

- **发批前三闸（KOR 实测必过，一条错整批 CANCELLED）**：
  1. `preflight_expressions(alpha_expressions=[...], region="KOR", universe="TOP600", delay=1, dataset_id=...)`
     —— **必须带 `dataset_id`**，否则 VECTOR 检测失效（DEU 实证两次整批连坐）。
  2. `op_arity.ensure_safe_for_dispatch(exprs)` —— 元数违规**整批连坐**。
  3. 本地类型闸（VECTOR 必须 `vec_*` 包裹；作分组轴的 `bucket(...)` 内层必须 `rank(...)`）
     + 字段 `get_datafields` **实名逐字核对**
     + **KOR 不可用算子黑名单**：`ts_ir`、`ts_target_tvr_hump`（整批 FAIL 且**无报错**）；
       `ts_target_tvr_decay` 可用但压 TO 时**等比例杀 S**。

## 第 1.5 步：族驱动扫描（防「模板单一」）—— 2026-10-14 新增，必读

> **背景（本会话实证）**：手写表达式只用 1–2 个模板会**系统性遗漏信号**。
> 实证：`insider_feats` 用 SH 构型只到 S1.23，换「裸 `multiply(rank(A),rank(B))`」到 **1.67**（全闸过）——
> 同字段换模板，差 0.44。工具里本有 `template_families.json`（9 族）+ `diversity_audit.py`（强制算子多样性）
> + `gate.py` 闸6，**但手写发批绕过 wave 文件 ⇒ 审计/注入/闸6 从未触发** ⇒ 固化发生在「绕过流程」这一步。
> **⇒ 手写扫描必须自查下三条，且优先用族骨架而非自造模板。**

### A. 骨架族目录（单一事实源：`wq-brain-campaign-toolkit/config/template_families.json`，9 族 + free_explore）

| 族 | 骨架 | 适用字段形状（`field_profile_match`）|
|---|---|---|
| `event_conviction_ratio` | `divide(流量, 存量)` → `ts_sum(signal, W)` → `group_rank` → `winsorize(std)` → `tail(q)` | 事件流量 |
| `event_gated_signal` | `trade_when(事件条件, 信号, -1)` | 稀疏事件（cov<0.6；news/insiders/institutions/earnings/shortinterest）|
| `continuous_spread_pair` | `subtract(rank(a), rank(b))` | 稠密连续（cov≥0.7、MATRIX）|
| `ceiling_suppress` | `winsorize(rank(字段), std=2/3/4)` | 截尾字段（[0.9,1] 占比>50%）|
| `discrete_score_bucket` | `group_rank(整数评分, group)` | integer 评分/计数（禁 `ts_delta`）|
| `low_freq_backfill` | `ts_backfill(字段, W≥更新周期)` | 月/季频（W∈{63,115,120,180,252}）|
| `analyst_revision_breadth` | `group_rank(ts_delta(vec_avg(计数), W), group)` | 分析师修正计数（VECTOR、spread）|
| `target_price_premium` | `group_rank(divide(vec_avg(目标价), close), group)` | 目标价（zero_inflated、cov≥0.5）|
| **`first_order_transform`** | **9 变体**（见下）| 连续序列（价格/收益/评分）|
| `free_explore` | LLM 自由探索（占比 ≤20%，不受 shape 约束）| — |

**`first_order_transform` 的 9 变体**（论坛帖「模版群助我 60 天点亮 60 个塔」252 赞；同字段 9 视角、经济同源但横截面低相关）：
```
slope            = ts_regression(ts_zscore(X,500), ts_step(1), 500, rettype=2)
growth_rate      = ts_delta(ts_delta(X,252)/ts_delay(X,252), 252)
ar_slope         = ts_regression(ts_delta(X,252), ts_delta(X,500), 500, rettype=2)
squared_momentum = ts_mean(signed_power(ts_delta(X,252), 2), 500)
decay_momentum   = ts_decay_linear(ts_delta(X,252), 500)
rank_reversal    = reverse(ts_rank(ts_zscore(X,500), 500))
log_smooth       = log(abs(ts_delta(X,500)) + 1e-6)        # 仅限非 ceiling 字段
signed_power     = signed_power(ts_delta(X,500), 2)
delta_stack      = ts_delta(ts_delta(X,252), 500)
```

### B. 本区未用算子清单（`tracking/KOR/reference/kor_generation_constraints.json` 实测）
**22 个从未用过**：`sqrt, if_else, delay, delta, ts_arg_max, ts_arg_min, ts_product, group_mean, group_sum,`
`group_zscore, pasteurize, vec_max, vec_min, vec_sum, vec_norm, bucket, range, abs, log, sign, exp, power`
**`injection_rules.force_explore_ops`（强制探索）**：`trade_when, bucket, winsorize, ts_ir, ts_corr, ts_product, if_else, ts_arg_max`
**`skeleton_quota`**：`linear_mix≤0.5 / event_gated 0.15 / group 0.15 / ratio 0.1 / other 0.1`

### C. ★ 发批前「算子/骨架多样性」自检（手写扫描必过，否则重写批次）
1. **族数 ≥2**：本批**不得只用 1 个骨架族**（SH 构型 ≠ 唯一解）；
2. **未用算子 ≥2**：本批至少引入 **2 个不在 `operator_stats.used` 里的算子**（优先 `force_explore_ops`）；
3. **算子数 <10**（合规上限，**按单条表达式计**）+ 仍过第 1 步的三闸。

**上面三条已工具化，不要再人工对照 A/B 两表**（2026-10-14 落地；本节旧文写「需人工对照」已作废）：

```bash
# 仓库根执行。$WQ_PY = world-quant-brain-mcp/.venv 的解释器
$WQ_PY tracking/KOR/scripts/scan_diversity.py --audit <手写批次.txt>   # 逐条打三闸 PASS/FAIL
$WQ_PY tracking/KOR/scripts/scan_diversity.py --build <field> --all-families   # 反过来：按 9 族生成网格
```

它直接读 A 表的单一事实源（toolkit `config/template_families.json`）与 B 表的
`tracking/<REGION>/reference/<region>_generation_constraints.json`，所以 A/B 两表更新后无需改脚本。

> **与 toolkit `diversity_audit.py` 的分工（别混用、也别当重复清掉）**：
> `diversity_audit.py --campaign-dir <DIR>` 吃**战役目录的 wave 产物**，写台账并产 `next_round_injections`
> （gate.py 闸 6 消费的契约）；`scan_diversity.py` 吃**手写批次文本**，只往 stdout 打判定、**不落库**。
> 手写发批绕过 wave 文件 ⇒ 闸 6 从不触发 ⇒ 这一层自查是唯一防线。

### D. 判死前的「模板充分性」两问（比第 0 步更严）
**这个数据集的 S < 1.0，是「没信号」还是「模板不对」？** 自检：
- 用了 **≥2 个骨架族**（含 `first_order_transform` 的至少 2 个变体）吗？
- 用了 **≥2 个未用算子** 吗？
- 若「否」⇒ **不许判死**，补一轮族驱动扫描。

## 第 2 步：读数三分法（KOR 版）

| 双构型最好读数 | 动作 |
|---|---|
| **S≥1.58 且 2Y≥1.58** | 进全闸验证：`get_alpha_details`（全 checks，**重点看 `LOW_INVESTABILITY` + `CONCENTRATED_WEIGHT`**）→ prod/self（直连 API 可用 `cache/verify_alpha.py`）→ **PnL 互相关去重** → `submit_verdict` |
| **S 1.0–1.58** | **不要判死 —— 这是「构型没找对」的信号带**。升级：K 窗（132/140/150/160）、分组轴（sector/industry）、POW（0.25/0.5/0.75/1.0）、hump 档（0.003/0.004/0.005）。实证 pv47 从 2Y1.47 一路推到 **2.02**（K=140）；shortinterest38 从 CW 卡死推到全闸过 |
| **S<0.5（双构型都）** | 判死；同族字段免测。判死前自检两问：这批真的用了**两个**构型吗？字段真的**跨概念族**吗？ |

- **KOR 特有：三道墙要在「探针阶段」就预判**（不是出闸才看，否则读数失真）：
  - **`LOW_INVESTABILITY` 限 = 0.70×S** ⇒ 若 S≈1.9，investability 需 ≥1.33（保留率 ≥70%）。
    **未套 `vector_neut(·, dadv)` 的 PV 族探针几乎必挂这一项** ⇒ 探针就用完整构型（含破墙要素）。
  - **`CONCENTRATED_WEIGHT`（KOR 特化 `cw_gate=FAIL`）** ⇒ 任何 `group_rank` 族**必须**用
    `hump(subtract(·,0.5))` 形态；已提交的 2 颗是 CW 闸升级前通过的，**照抄其表达式已不再可用**。
  - **`prod` 密墙**：pv47 族同构型 prod 恒 **0.727–0.734**（窗/POW 微调全无效）⇒ 探针阶段不必测 prod，
    但要知道「同族构型 prod 天生 0.72+，需 `industry` 轴（→0.6663）或 `hump=0.005`（→0.604）才过」。

- **2Y 要单独看，且要判「钥匙是否适用」**：S 高 2Y 低 = 早衰或**钥匙失配**。
  实证：`risk71` 的 `dsrt` 字段套 PV 构型 **S1.88 / F1.07 但 2Y 恒 0.91–1.16**（K 全扫 8 档）⇒ 判死。
  **`ts_kurtosis` 钥匙只对「日频收益分布型」字段有效** —— 同为 specific return 族，`spret` ✔（2Y2.02）、`dsrt` ✘。
  ⇒ **换族前先用 2 条探针验 K=140 的 2Y。** 判死线对 S 和 2Y **同时**适用。

## 第 3 步：出闸后去重（一条腿只出 1 颗）

- `GET /alphas/{id}/recordsets/pnl` 取两条 PnL 求 Pearson —— **零平台配额**的互相关。
- 同机制**跨数据集 = 同一条腿**（pv47 ↔ other532 同机制字段；shortinterest38 同族结构变体 0.9988+）；
  换构型 / 换数据集**不产生新腿**。
- **KOR 特有：同一数据集内一次只提 1 颗**（同族近亲提交后 self 会冲 0.99+；台账最早 2 颗均出自 `shortinterest38`）。
- `self` 相关池**包含自己未提交的 alpha**：self max 高先看驱动记录是不是自己建的，再判「被占用」。

## 预算参考

| 目的 | 成本 |
|---|---|
| 生死判定 | 1 批（8 条 = 2 构型 × 3 跨族字段 + 2 机动） |
| 潜力确认（1.0–1.58 带） | +1~2 批（K 窗 / 轴 / POW / hump 扫描） |
| 冲闸（investability / CW / prod） | +1~3 批（各墙已各有一条破法，见第 2 步） |
| **判死一条错误构型的隐形成本** | 整个战役的期望产出 —— 所以第 0 步零成本筛选最值钱 |

## 本会话反例清单（每条都是实测教训）

1. **自造结构**：analyst 族自造结构 5 个数据集全灭（S 天花板 ≈1.1，`analyst9`/`base_ref`/`consensus`/`analyst14`/`analyst39` 复现）；
   换已验证构型后 `pv47` S1.90（**先查历史产物**）。
2. **只测一个构型**：`pv47_spret` 用 SH 构型死、用 PV 构型活（**构型最优性是字段属性**）。
3. **钥匙误用**：`ts_kurtosis` 只对收益分布型有效；`risk71 dsrt`（同为 specific return）K 全扫 2Y 恒 ≤1.16；
   换 `ts_kurtosis(波动率)` 腿 ⇒ 2Y 崩到 0.49。
4. **发批三闸**：一条 ERROR（d188 ESG 的 `sustainability_positive_corr_score`）**连坐整批 CANCELLED**（8 条全废）
   ⇒ **拆小批 + 逐条实名核对**。
5. **僵尸误判**：`children=0` 且 progress 非空（0.35/0.9）**只是慢**，实测卡 0.35 约 25 分钟后自行 COMPLETE；
   multi-sim location 约 **24h 过期 ⇒ 当天收割**。
6. **画像盲区**：ALIVE 只看单字段 S，看不到构型（`pv47_spret` 不在 ALIVE，构型做出 S1.90）。
7. **CW 假阴性**：直接 `subtract(group_rank(·),0.5)` 不加 hump ⇒ CW 仍 1.0；
   `normalize`/`scale`/`winsorize`/`quantile`/换轴/换中性化档 **全部 CW 1.0**（23 条对照）。
8. **prod 误判**：`ts_mean` 平滑反而把 prod 推高（0.76）；只有 `industry` 轴 / `hump=0.005` 降 prod。
9. **工具失效**：论坛 `search_forum_posts` 已失效（连续 4 次 `unexpected error`）⇒ 改 **WebSearch** 外部检索
   （用户明令：遇到困难或没灵感要及时查论坛/外部论文或数据）。
10. **写脚本只用 ASCII 引号**（全角引号混入 heredoc 已致两次 SyntaxError）。
