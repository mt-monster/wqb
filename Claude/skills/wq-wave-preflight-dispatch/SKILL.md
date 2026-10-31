---
name: wq-wave-preflight-dispatch
layer: L-RA
description: WQ BRAIN 批量仿真发批前自查 SOP。判「族扫完了吗」前先做三件事：横向扫全史最优、字段笛卡尔积清点、设置档盲区清点；发批时过候选实测/覆盖率闸/字段存在性硬闸/禁混信号自检，断点续跑去重键须含全部设置档，扩设置维度时运行器三处同步。本地库不可判全闸通过与所属区（alphas.region_id/universe 混区）。含 SuperAlpha 发批与提交前自查（区域资格≥10 组件、SA 相关闸单独实测、同源自锁、余量=1−prod）。触发词：发批/跑一波/扫数据集/批量仿真/items.json/续跑/换数据集/判死/扫完了吗/查论坛/SuperAlpha/SA/组件池。
last_verified: 2026-10-30
agent_created: true
---

# WQ 批量仿真：发批前自查 + 续跑键设计

## 职责边界

- **本 skill 负责**：一批表达式**发出去之前**的自查（全史横向对比、字段笛卡尔积、设置档盲区、覆盖率/存在性/合规三闸）与**续跑基础设施**（去重键设计、运行器同步、断点续跑）。
- **本 skill 不做**：生成表达式（→ `brain-make-some-gem`）；逐个候选推指标（→ [`wq-alpha-gate-push-op-min`](../wq-alpha-gate-push-op-min/SKILL.md)）；prod/self 读数与降相关（→ [`wq-prod-corr-read`](../wq-prod-corr-read/SKILL.md) / [`wq-prod-lever-self-lock-guard`](../wq-prod-lever-self-lock-guard/SKILL.md)）；提交动作（→ [`worldquant-submit-alpha`](../worldquant-submit-alpha/SKILL.md)）。
- **上游 / 下游**：上游 = 已锁定的数据集与已生成的候选池；下游 = `workflow_batch_track` / `submit_batch` 派发 → 收批入库。

来源：2026-10-05 EUR 战役（wave320–330，约 180 条表达式）。
每道自查漏掉的实测代价都记在下面，读时注意「代价」那一项。

---

## 0. 判「这个族已经扫完」之前（★ 比任何发批动作都更前置）

### 0.0★★ 横向扫全史：这个指标的全史最优在哪

**这是用 6 波的代价换来的纪律。** 我连续 6 波（wave323–329）在
`multi_source_model` / `chart_cnn_alpha` 上扫杠杆，S 天花板卡在 1.39；
同期**从没做过一次「全 region 按指标排序」的横向对比**。
一次全史扫描的结果：2Y 过线的 149 条变体里，排前列的是**四个多月前就测过的**
`wave269_fincf_residual` 现金流残差族（S1.76 / F1.20 / 2Y2.05 / sub1.21），
**全部优于我最近 6 波的任何候选**。

```python
# ★ 所有字段一律 str() 兜底后再排序/格式化
#   —— None 参与比较会让整批统计崩（实测两种崩法，见 §0.0.3）
import json, glob, os
rows = []
for p in glob.glob('tracking/<R>/results/wave*_checkpoint.json'):
    try: d = json.load(open(p, encoding='utf-8')).get('results', [])
    except Exception: continue
    for r in d:
        v = r.get('<METRIC>')
        if v is None: continue
        try: vf = float(v)
        except Exception: continue
        if vf >= 1.58:
            rows.append((str(vf), str(r.get('sharpe')), str(r.get('fitness')),
                         str(r.get('two_year_sharpe')), str(r.get('sub_universe_sharpe')),
                         str(r.get('decay')), str(r.get('note') or '')[:40],
                         os.path.basename(p).replace('_checkpoint.json', '')))
rows.sort(key=lambda t: float(t[0]), reverse=True)
for t in rows[:20]:
    print('  2Y=%-5s S=%-5s F=%-5s %-16s %s' % t)
```

**纪律**：
1. **每挖到一个新族，先横向扫全史该指标的历史最优**，再决定投多少波次。
   否则可能在**次优族上死磕几十波**。
2. 这与「不要频繁换数据集」**不冲突**：横向扫是**读文件**（零成本、不占槽位），
   换数据集是**发批**（占槽位 ~10 分钟）。**该扫就扫，该发才发。**
3. 扫出来的历史最优要**回头核实 prod**——它可能已被判死。

### 0.0.1 判死要看**结构空间**，不是首个撞墙的那个点

实测反例：`wave269` 里 A2撞 prod 0.7071，我据此按「族判死」处理。
但 G1 是在 A2 上**再残差化一次**的不同结构——实测 **G1 的 prod 是 0.9859，比 A2 更差**。
⇒ 结论：**这次是我的猜测被证伪，族确实该判死**；但**过程说明判死前要看结构空间**。

⚠ 同时它**修正了一条既有经验**：「嵌套残差化破 prod 墙」**不是普适规律**——
在 `N1VnJjXg` 上有效，在 wave269 族上反而**加重** prod 拥挤。
⇒ **杠杆谱在 prod 侧同样族特异**，不要跨族假设。

### 0.0.2 改 JSON 按**数组下标**定位，不要靠 note 文本前缀

实测：wave330 的 items 里 V1/V10/V11/V12… 的 note **全以 "V1" 开头**，
按 `note[:2]` 前缀替换**漏掉了 V10/V11** ⇒ 违规表达式留在批里。
```python
# ✗ 靠文本前缀：同前缀是常态
for it in d:
    if it['note'].startswith('V1'): it['code'] = new
# ★ 按下标
d[10]['code'] = new_code
```

### 0.0.3 扫历史 checkpoint 做统计的容错纪律

`None` 参与比较会让**整批统计崩掉**，两种表现都实测到了：
- `sorted(rows, key=...)` 里 `None` vs `str` ⇒ `TypeError: '<' not supported between NoneType and str`
- `'{s:<5}'.format(s=None)` ⇒ `TypeError: unsupported format string passed to NoneType.__format__`
⇒ **所有字段一律 `str()` 兜底后再排序/格式化**（与「一个 None 毁掉整批」同类）。

### 0.0.4★★ 查 DB 台账时：先确认布尔列的取值（`IS NULL` 可能恒假）

`alphas.soft_deleted` 存的是 **`0` / `1`，不是 NULL**。写
`WHERE soft_deleted IS NULL` **恒为假**、**静默返回空集**、**不报错**——
我据此差点断言"库里一条存量都没有"。

```sql
-- ✗ 恒假（返回空集，不报错）
WHERE ... AND soft_deleted IS NULL
-- ✓ 正确
WHERE ... AND COALESCE(a.soft_deleted, 0) = 0
```
**自检**：查询返回 0 条时，**先验证条件不是恒假**——把该条件去掉再查一次，
或 `SELECT DISTINCT <bool_col>` 看真实取值。
⇒ **SQL 的「假绿灯」比Python 更隐蔽**（Python 至少会报格式错，SQL 直接给你空集）。

### 0.0.5★★ 登记候选前必查 `status` + `date_submitted`（否则会把已提交的算成存量）

实测：`JjQmx9nm` 四项指标全过、prod 0.6695，我据此登记为"待累积候选"——
**但它2026-10-03 就已提交（`status=ACTIVE`, `stage=OS`, `date_submitted` 有值）**。

```python
# ★ 登记前必查
r = cur.execute("""SELECT status, stage, date_submitted FROM alphas WHERE alpha_id=?""",(aid,)).fetchone()
if r and (r['date_submitted'] or r['status'] in ('ACTIVE','COMPLETE')):
    print('已提交，不计入存量')
```
⇒ **只看指标不足以判断"可累积"**；还要看提交态、软删态、prod 来源。

### 0.0.6★★★★★ 「积攒了多少 alpha」必须**三层口径**，否则数字差 20 倍

2026-06 EUR 实测：用户问"积攒了多少"，DB 里能捞出 **110 颗**指标过线的未提交候选，
**但真正可积攒的只有 5 颗**。差距来自 21 颗 prod 撞墙 + 85 颗 prod 从未测。

| 层 | 判据 | EUR 实测数量 | 能否说"可积攒" |
|---|---|---|---|
| ① 指标过线（本地四闸）| S≥1.4 / F≥0.9 / 2Y≥1.3 / sub≥0.8 | **110** | ❌ 只能叫**近候选** |
| ② 排除已提交 | `status='UNSUBMITTED'` **AND `date_submitted IS NULL`** AND `COALESCE(soft_deleted,0)=0` | 已含在①| ❌ 中间层（我踩过）|
| ③ **prod < 0.7 平台实测** | `alpha_corr_cache.prod_correlation < 0.7` | **5** | ✅ **只有这层算数** | <!-- from config.prod_corr_max -->

⇒★★ **报数时必须三行一起给**，否则单报 110 会严重误导（自己也容易被误导）。

```python
# ★ 权威核算模板（照抄，勿简化）
cache = {aid: float(p) for aid, p in cur.execute(
    "SELECT alpha_id, prod_correlation FROM alpha_corr_cache")
    if isinstance(p, (int, float))}     # ★ 见下方坑：表里混有非数值（源标签）
rows = cur.execute("""SELECT a.alpha_id, a.sharpe, a.expression
  FROM alphas a JOIN regions r ON r.id=a.region_id
  WHERE r.name=:reg AND a.sharpe>=1.4 AND a.fitness>=0.9
    AND a.two_year_sharpe>=1.3 AND a.sub_universe_sharpe>=0.8
    AND COALESCE(a.soft_deleted,0)=0          # ★ 该列是 0/1 不是 NULL（§0.0.4）
    AND a.status='UNSUBMITTED' AND a.date_submitted IS NULL""")
near  = rows
ok    = [r for r in near if cache.get(r['alpha_id'], 1.0) < 0.7]
print(f"近候选 {len(near)} → 真正可积攒 {len(ok)}")   # 110 → 5
```

⚠★★ **四个会让核算脚本崩/错/多算的坑（连踩）**：
1. **`alpha_corr_cache.prod_correlation` 混有非数值**（源标签字符串）⇒
   `isinstance(p,(int,float))` 过滤，否则 `p[0] < 0.7` 抛 `TypeError: must be real number`。
2. **逐条 `cur.execute(... WHERE alpha_id=?)` 循环会中断**（同一次连接上的游标状态）⇒
   **先把整表读进 dict** 再在内存里筛。
3. **`alphas.region_id` 会混区** ⇒ 上面模板里的 `JOIN regions r ON r.id=a.region_id` 给出的「区域」是**不可靠**的（详见 §0.0.6b）。
4. **`alphas` 表没有 pyramid / decay / truncation 列** ⇒ 想核「点了几座塔」「当时用的什么设置档」必须回平台，本地永远查不到。

⇒★★★ **最重要的一层：prod 未测的候选，期望极低。**
85 颗未测里挑了 3 个「指标最漂亮」的不同机制代表实测：

| alpha_id | S | 2Y | prod | 判定 |
|---|---|---|---|---|
| `zqbJY30o` | **1.97** | 2.00 | **0.8814** | ❌ 今日最差 |
| `786ajadx` | 1.92 | 2.08 | 0.7856 | ❌ |
| `78NoOeVx` | 1.67 | **2.42** | 0.7432 | ❌ |

⇒ **3/3 撞墙。** 这些是历史遗留的「指标过线但 prod 从未验证」的候选——
**指标越漂亮越容易误导**（它们没被 prod 筛过，所以看起来比实际更好）。
⇒ ★ 报"存量"时若第三层实测比例很低，**必须说明"未测的那批不要当成机会"**。

**积攒口径建议**：`status='UNSUBMITTED' AND date_submitted IS NULL AND COALESCE(soft_deleted,0)=0 AND prod_correlation<0.7`。 <!-- from config.prod_corr_max -->

### 0.0.6b★★★★★ `alphas.region_id` 会混区 ⇒ **本地库不可判「全闸通过」与「属于哪个区」**（2026-10-30 GBR 实测）

**这是本 SOP 里最容易让人把 EUR 的候选当成 GBR 候选提交上去的一条。** 本地 `wqb.db` 的 `alphas` 表有三个字段**全都不可靠**：

| 字段 | 问题 | 反例（实测） |
|---|---|---|
| `region_id` | **同一个 id 下混装多个区域** | `region_id=7` 同时装 GBR 与 **EUR** |
| `universe` | 不可靠 | 同一 `region_id` 下出现 `TOP700` 与 `TOPCS1600` |
| `long_count` / `short_count` | **不能反推区域** | `P0gvv5gE` 是 GBR/TOP700 但持仓 `909`；而 `YPxLWdpv` 持仓 `1400` 实为 EUR |

**决定性反例**：`YPxLWdpv` 在本地看是完美候选 —— S **3.36** / F **1.49** / TO **64.66%** / 2Y **1.89**，四项全过、`prod` 也不高。实读平台后：

- `settings.region = "EUR"` / `universe = "TOPCS1600"`；
- `longCount 575 + shortCount 825 = 1400`；
- **`failed_ra_count = 1`**，失败项 `LOW_SUB_UNIVERSE_SHARPE`：严格 limit 是 **1.78**（绝对下限），本颗只有 **1.63**。

⇒ ★ **本地"四闸全过"完全可能在平台上 fRA=1。** 本地没有 `ra` 字段，也没有 `checks` 结构。

**⇒ 本地近似闸口径作废。三条硬规矩**：

1. **全闸判据只认平台** `ra.failed_ra_count == 0` / `checks[].fail` 为空。本地 `sharpe/fitness/turnover/two_year_sharpe/sub_universe_sharpe` 只能当**粗筛**。
2. **区域只认平台 `settings.region`**（`get_alpha_details`）。`batch_get_alpha_metrics` 给 `failed_ra_count` 但**不给 region** ⇒ 两个工具都要：先批量过 `failed_ra_count`，再对活下来的逐条 `get_alpha_details` 核 region。
3. **`get_user_alphas(region="GBR", ...)` 不可用** —— 服务端不接受 `region` 参数，实测直接 `400 Bad Request`。别指望用它批量核区。

⇒ 配套纪律：**`submit_ready` 队列里的行，提交前必须逐条回平台核 `settings.region` + `ra.failed_ra_count`**，不能凭本地库直接提。跨区污染在 `submit_ready` 上尤其危险——它会让你把别区的 alpha 提交到本区的点塔目标上（塔位归属由平台按 `settings.region` 判，但你会算错自己的塔位进度）。

### 0.0.7★★★★★ catalog 覆盖体检（**做任何字段清点之前**，2026-10-06 事故后新增）

**为什么必须在 §0.1 之前**：§0.1「字段笛卡尔积清点」的**前提是本地 catalog 完整**。
它不完整时，你数出来的"该族字段 N 个"本身就是错的 —— 看不到的字段不会出现在笛卡尔积里。

**实测事故（GBR）**：本地 catalog 有 **131 个数据集字段行 = 0**（缺 13,158 个字段）。
后果有三个，都属于"静默出错"：
1. 逐 category 扫描时这些数据集**直接被跳掉**（`MATRIX 字段数=0`）；
2. 覆盖普查算出"2297 个可用字段"是**残缺分母**，补齐后变 **9160**；
3. 修复后**第一次看见两个池**（`model26` 161 未测 / `model25` 83 未测）——
   它们在修复前本地 0 行，任何本地筛选都**看不见**。

**前置三步（顺序不可颠倒）**

```bash
# ① 覆盖率体检（口径 = 真盲区，不是 field_count 差）
# ⚠ wqb_tools.py 是**仓库外的全局工具**（本仓无此文件，路径按本机实际填写）；本仓等价入口见下方三行表
$WQ_PY <外部工具目录>/wqb_tools.py catalog-coverage --region <R> --write-manifest
# ② 有"可行动盲区"就补
$WQ_PY <外部工具目录>/wqb_tools.py catalog-fill --region <R> --max-datasets 140
# ③ 补完再看一次；要当闸用就加退出码
$WQ_PY <外部工具目录>/wqb_tools.py catalog-gate --region <R> --max-blind 0   # 盲区>0 ⇒ exit 2
```

**已固化的三个入口（不用记命令，走到就会跑）**
| 入口 | 行为 | 位置 |
|---|---|---|
| **每波目录前置检查** | 新增两条检查：`catalog_dataset`（**本波数据集在本区本地 0 字段 ⇒ FAIL**）+ `catalog_coverage`（区级可行动盲区 ⇒ WARN） | `tools/preflight_wave.py::run_preflight`（第 3.5 步） |
| **派发动作本身** | 派发前打印 catalog 健康行；`--strict-catalog` 时**盲区 >0 直接 exit 2 拒绝派发** | `wqb_tools.py dispatch` |
| **候选报告** | 报告头部固定打印一行 `catalog 体检` | `wqb_tools.py report` |

**各区当前覆盖率（2026-10-06 快照，可作基线）**
GLB 97.9% / HKG 99.5% / EUR 96.2% / KOR 95.3% / IND 91.1% / **GBR 86.3%** / **USA 85.0%（52 个盲区，最差）**

**口径陷阱（都用血换的）**
- ❌ **别用 `本地行数 < datasets.field_count`** —— `field_count` **不是区级口径**。
  GBR 实测该口径 38 个报警里 **10 个是假阳性**（`analyst_consensus` 表面缺 1472，
  平台实测 GBR 只有 100–200；`model219`/`model230` 平台返回 0）。
- ✅ **用「真盲区」= 该区数据集在本地 `fields` 一行都没有**（读者完全看不见 ⇒ 选集必漏），
  再减去**平台已确认本区为空**的（`catalog-fill` 会自动打标到
  `cache/catalog/_platform_empty_verified.json`），得到**可行动盲区**。
- ⚠ **`datasets` 表混有伪数据集行**（`pv/model/other`、`model25+model38+behavior`、
  `model38_star_val`、`_unknown`…，GBR 14 个 `field_count=0` 且无字段）⇒
  **"该区有 N 个数据集"这个分母本身也要扣掉它们**。
- ⚠ **字段枚举必须带 `instrumentType=EQUITY`**：直连 `GET /data-fields` **漏该参数即恒返回 0**
  （会得出"本区无字段"的假结论）；走 MCP `get_datafields` 则被其 `max_fields=300` **硬截断**。
  正解 = 带全参数的**分页**直连（单页上限 `limit=50`，>50 报 HTTP 400）。
- ⚠ **`FROM fields` 必须永远带 region 过滤**：`fields` **无 region 列**，且**同名数据集跨区各有
  一个 dataset_id**（`model38` 有 9 个）⇒ 漏 region **静默串区**（曾据此误判"GBR model38 有
  star_val 字段"，又误读成"数据被并发重写"）。用 `wqb.region_catalog.RegionCatalog`。
  静态自查：`python ...\wqb_tools.py catalog-guard`。

### 0.1 字段笛卡尔积清点（该族字段 × 已测/未测）

**误判实例**：`multi_source_model` 的 M3（`long_term_quantile1_120d_pred`，S1.11/2Y2.31）
是EUR 唯一 2Y 过线的形态，我把它当孤立点反复攻设置档。
但回头核对全 60 字段后发现——**long_term 族的 120d 变体 7 个里只测了 1 个**
（`regime2_120d` / `regime4_120d` / `seasonal_120d` / `hedge3_120d` /
`quantile5_120d` / `confidence_120d` 全未测）。
补扫后 **`regime4_120d` 四项指标全部优于控制行**（S+0.06 / 2Y+0.03 / sub+0.05）。

**纪律**：报「已扫完」时必须附上这张表。**「我测过的」≠「平台允许的」**。
若清点表里有 ≥1 个未测字段，先补扫再说。

### 0.1.1★★★★★ 清点必须**按 `field_type` 分桶**（单一类型过滤会整体漏掉一类数据，2026-10-06 事故后新增）

**误判实例（GBR，代价：多轮空跑）**：全程用 `field_type='MATRIX'` 筛字段 ⇒ **VECTOR 整体不可见**。
GBR 实测：MATRIX 9160（cov≥0.6 **2576**）｜**VECTOR 4782（375）**｜GROUP 1470（1390）｜SYMBOL 110（11）。
被漏掉的 VECTOR 池里含**零拥挤**数据集：`news18`(ds_aCnt 5)｜`analyst9`(0)｜`news50`(0)｜`fund_holdings_panel`(0)。
更关键：**NEWS / SENTIMENT / SHORTINTEREST 这几类在 GBR 根本没有 MATRIX 字段** ——
用 MATRIX 过滤等价于「宣称这些塔不存在」。

**纪律**：
1. 清点可用字段时**必须枚举全部 `field_type`**（至少 MATRIX + VECTOR + GROUP），并分别报数。
2. **类型决定算子**：MATRIX/SYMBOL → 直接进标量算子；**VECTOR → 必须先用 `vec_*()` 降维**
   （合法：`vec_avg/vec_sum/vec_max/vec_min/vec_count/vec_stddev/vec_skewness/vec_kurtosis/vec_norm/vec_powersum/vec_choose/vec_percentage/vec_range`；
   **`vec_ir` 不存在**——平台校验会把它报成 unknown field）；GROUP → 只能当 `group_*` 的第 2 参数。
3. 某 category 若"可用字段 = 0"，先怀疑**类型过滤**，再断言"本区无数据"。
4. **同数据集内不同子族机制不同，不可外推判死**：`analyst7` 367 个可用 MATRIX = 231 个"计数"字段（死族）
   ＋ **180 个非计数**（`est_12m_<指标>_mean/high/low/median/std` = 分析师预测水平值，实测
   `est_12m_pre_mean` 修正动量 **S1.15/F0.59**，是未点亮塔最高 F）。**"计数死" ≠ "分析师族全死"**。

#### 0.1.1 ★★★★★ 「该数据集已扫尽」必须按【字段前缀 / 信息维度】分组判断，**不能只看数据集名**

2026-06 实测错判：我查 `quant_factor_lib` 发现高覆盖字段 19 个已测 17 个，
就断言「已扫尽」⇒ 转去别的数据集。**错在只按一个前缀看了字段。**

按前缀分组后才发现：

| 维度（字段前缀）| 字段数 | 平均 cov | 状态 |
|---|---|---|---|
| `qfl_cassie`（信用风险）| 32 | 0.697 | 已测 30/32，只有 `ocf_currliab` 存活 |
| ★★ **`qfl_nlp_calltranscript`（财报电话会议 NLP）** | **94** | 0.449 | ★★ **完全未测** |

⇒★★★★★ **换维度 ≠ 换数据集** —— 它是同一个数据集里的另一个独立机制来源。
⇒★★**一个数据集往往含多个独立信息维度**（不同供应商/不同字段族），
   只测其中一个就宣称"扫尽"是**最常见的挖矿失误**。

```python
# ★ 判「已扫尽」前必须做的分组清点
rows = cur.execute("""SELECT DISTINCT f.field_name, f.coverage FROM fields f
  JOIN datasets d ON d.id=f.dataset_id JOIN regions r ON r.id=d.region_id
  WHERE r.name=:reg AND d.name=:ds""").fetchall()
from collections import defaultdict
g = defaultdict(list)
for name, cov in rows:
    parts = name.split('_')
    prefix = '_'.join(parts[:3]) if name.startswith(('qfl_nlp',)) else '_'.join(parts[:2])
    g[prefix].append(cov)
for p, v in sorted(g.items(), key=lambda kv: -len(kv[1])):
    print(f"{p:44s} {len(v):3d} 字段  平均cov={sum(v)/len(v):.3f}")
# ★ 任何一组「未测」⇒ 数据集就没扫完
```
⇒ ★★ **配套纪律**：分组清点要**同时输出每组的平均覆盖率** ——
低覆盖组（cov<0.7）往往被"优先测高覆盖"的原则跳过，从而**整组漏掉**。
（本次的 `qfl_nlp_calltranscript` 平均 cov 0.449，正好在"可试区间"。）

### 0.2 设置档盲区清点（该 region 合法档位全集 × 已用/未用）

先取平台权威合法档位，再统计自己历史用过哪些：

```
mcp__wq-brain-http__get_platform_setting_options()   # 权威来源：region×universe×neut 全集
```

```python
import json, glob
from collections import Counter
c = Counter()
for p in glob.glob('tracking/<R>/results/wave*_checkpoint.json'):
    try: d = json.load(open(p, encoding='utf-8'))['results']
    except Exception: continue
    for r in d:
        for k in ('neut', 'universe', 'maxTrade', 'decay', 'truncation'):
            if r.get(k): c[f'{k}={r[k]}'] += 1
print(dict(c))
```

**EUR 实测发现的盲区**：`maxTrade` 用了 **0 次**、`neut=COUNTRY` 与 `CROWDING` 各 **0 次**、
universe 只用了 TOPCS1600。⇒ 扫完后三个都有实质发现（见 §0.6）。

#### ★★★ 中性化是唯一「同时决定 2Y 与 prod」的档位轴 —— 必扫项，不是举例

GBR 合法中性化 **11 档**：`NONE / REVERSION_AND_MOMENTUM / STATISTICAL / CROWDING / FAST / SLOW / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / SLOW_AND_FAST`。

**同一条表达式只换中性化**（严格单变量，信号一个字不改）实测：

| 中性化 | 2Y | TO | prod |
|---|---|---|---|
| SUBINDUSTRY | **1.85** | 0.261 | 0.7736 ✗ |
| CROWDING | 1.77 | 0.259 | 0.8333 ✗ |
| INDUSTRY | 1.73 | 0.270 | 0.7919 ✗ |
| MARKET | 1.64 | 0.254 | 0.8719 ✗ |
| **STATISTICAL** | 1.73 | **0.830** | **0.6506** ✓ |

⇒ prod 0.65→0.87 **全由档位决定**。而且**「2Y 最高的档」往往正是「prod 最高的档」** —— 两者的最优解通常不在同一档，必须逐档看表而不是挑单一最优。

**纪律**：

1. 开波前数「本区这 11 档我试过几档」，**≤3 档即视为盲区**，必须先补扫再谈"挖不出东西"；
2. 中性化扫档不额外加钱（同表达式 × N 档 = N 条仿真），但它**改持仓** ⇒ 换档后**必须重测 prod 与 self**（见 `wq-prod-lever-self-lock-guard` §一）；
3. ⚠ **区域档案里的默认档是 IS 最优档，常常正是 prod 最差档**（GBR：档案 `SUBINDUSTRY` prod 0.7736 vs `STATISTICAL` prod 0.6506）⇒ **出货走双轨：IS 用档案档筛信号，prod 用低 prod 档定稿。**

⚠ **第二层检查：工具能不能表达？** 若运行器只映射
`decay/truncation/neut/universe` 四个键，**即使 items 里写了 `"maxTrade":"on"` 也不进 settings**。
发现盲区后必须同步扩运行器（§4.2），否则是「方法上学到了、工具层做不到」。

### 0.3 没有灵感时：查论坛，不要瞎试

**三条新杠杆全部来自论坛，且都是本工作区历史从未试过的**：

| 杠杆 | 来源 | 治什么 |
|---|---|---|
| `maxTrade = ON` | 论坛评论 XW23690 | robust（PnL 线与 Investability constrained 偏离） |
| `group_backfill(·, group_cartesian_product(country, subindustry), 126)` | XW90844（57 赞） | 股票数量 Coverage不足导致的 robust/CW |
| `if_else(rank(ts_mean(volume,20))>=0.20, signal, nan)` | 评论 AJ39409 | Weight concentration |

搜索关键词要具体：「LOW_2Y_SHARPE 提升方法」「全周期 sharpe 2y 对冲」
「<REGION> TOPCS1600 经验」「robust universe sharpe 解决」「换手率 decay 权衡」。

**读帖要点**：优先读**评论区**（往往比主贴更具体、给到可复制的表达式），
并注意作者自己写的适用边界（如「`group_backfill` 适合基本面类，情绪类要慎重」）。

★ **最高价值的一篇**（LL46807，23 赞）：《全周期 sharpe 和 2y sharpe 的强对冲》——
- 全周期与 2Y 呈**跷跷板**，调参只是在挪支点；
- **「批次设计阶段就分流两条车道」**（一条按全周期最优、一条按 2Y 最优：缩短窗口/加权近期）；
- **两条车道找不到交集 ⇒ 判历史型，及早归档**；
- 案例一的形态（「某分析师族信号」全周期 0.87 / 2Y 0.64→1.18 单调反向）
  与 `multi_source_model` 的 M1/M3 背离**完全同构**。

### 0.4 ★ 新增设置维度必须**先单条探路**，不能直接进批

平台对 settings 键的**取值形态**有约束，本地签名/文档/论坛处方都不保证可用。
**实测过的反例**：

| 键 | 合法 | **非法（HTTP 400）** |
|---|---|---|
| `maxTrade`（EUR/D1） | `"ON"` / `"OFF"` | 数值 `0.05` / `0.1` |
| `ts_zscore(x, d)` | `d` 为常数 | 把分组名塞进第 2 参 |

**探路写法**（文件名必须遵循 `eur_<tag>_items.json`，否则 `FileNotFoundError`）：
```bash
python - <<'PY'
import json
json.dump([{"code":"rank(<真实存在的字段>)","note":"PROBE","decay":40,
            "neut":"FAST","maxTrade":"ON"}],
          open('tracking/<R>/candidates/eur_probemt_items.json','w',encoding='utf-8'),
          ensure_ascii=False)
PY
$WQ_PY tracking/<R>/scripts/run_wave_single_fanout.py probemt --dataset <DS> --fresh --conc 1
```
看到 `[submit] <id>` = 受理；看到 `submit-fail ... 400` = 形态非法。

**★ 验证「键真的生效」不能用「和不设比」**：
- ❌ **错误比法**：拿 `maxTrade=ON` 与「同表达式不设 maxTrade」比，
  两者 **alpha_id 完全相同**——因为**平台默认就是 ON**（`SimulationSettings.maxTrade`
  默认 `"OFF"`，但我们平时不传时平台按默认组装）。"相同"只说明 ON 是默认值，
  **不能证明该键被忽略**。我据此误判"`maxTrade` 是 no-op"，差点丢掉一条真杠杆。
- ✅ **正确比法：构造 `ON` vs `OFF` 显式对照**，看是否**不同 alpha_id + 不同指标**。
  实测正确对照结论完全相反：

  | | maxTrade | alpha_id | S | F | 2Y | sub | TO |
  |---|---|---|---|---|---|---|---|
  | A | `OFF` | `Vk0OPkYG` | 1.02 | 0.46 | 2.00 | 0.92 | 0.0794 |
  | B | `ON` | `A1vk3R7W` | **1.17** | **0.58** | **2.34** | 0.85 | **0.0422** |

  ⇒ TO 腰斩 47%、S/F/2Y 全面上升 ⇒ **真杠杆**。

**纪律**：验证批的**第一条必须是显式的对照组**（把该键设成与默认不同的值），
不要浪费槽位在「看起来像基线」的重复行上。

### 0.4.1 ★★ 改函数返回结构时，**异常分支必须一起改**（实测整批报废）

把`submit()` 从 3 元组改成 4 元组时，我**只改了成功路径**：
```python
return it, None, msg                    # ❌ 异常路径还是 3 元组
return it, None, f"BAD_RESP:{...}"      # ❌
return it, None, f"API_ERR:{...}"       # ❌
return it, aid, None, body              # ✅ 只有这条是 4 元组
```
⇒ wave330 提交到第 2 条（撞 400 走异常路径）即崩，**ckpt 只落 1 条 / 16**。

**纪律**：
1. 改任一函数的 return 结构后，**`grep -n "return <fn名>("` 逐个核对所有分支**。
2. 更稳的做法：**统一返回固定形状**（始终 N 元组，错误时后续给 None），
   让解包永不失败。
3. ⚠ **平台刚创建 alpha 时指标可能还没算出来** ⇒ 拉指标要**短退避重试**
   （如 4 次、间隔 4→16s），否则会静默丢指标。
4. ⚠⚠ **指标有两种格式，两个都要认**（实测踩过：`metrics_unavailable` 排查了半天才找到）：
   | 来源 | 位置 | 命名 |
   |---|---|---|
   | **原始 API**（`brain_client.get_alpha_details` 直返） | `alpha["is"]` | 部分驼峰（`twoYearSharpe`） |
   | **MCP 工具**（`get_alpha_details` 返回） | `alpha["metrics"]` | snake_case（`two_year_sharpe`） |

   ```python
   m = a.get("metrics")
   if not isinstance(m, dict) or m.get("sharpe") is None:
       m = a.get("is") or {}          # ★ 回退，别只支持一种
   def pick(*names):
       for n in names:
           if m.get(n) is not None: return m.get(n)
       return None
   row["two_year_sharpe"] = pick("two_year_sharpe", "twoYearSharpe")
   ```
   ⇒ **判"指标就绪"时也要两个都查**，否则会误判成"平台没算出来"而白重试。

5. ⚠⚠⚠ **★ 2Y / sub / robust 三个指标不在指标段里，只在 `is.checks` 里**——
   这是最容易误判"平台没算出来"的地方（我为此白重试了一轮）：
   ```python
   # alpha["is"] 里只有 sharpe/fitness/turnover/returns/drawdown/margin/pnl/longCount…
   # ★ 但 2Y / sub / robust 要从 checks 按 name 取 value：
   checks = {c["name"]: c for c in (a.get("is") or {}).get("checks", []) if c.get("name")}
   row["two_year_sharpe"]        = checks["LOW_2Y_SHARPE"]["value"]            # 1.76
   row["sub_universe_sharpe"]    = checks["LOW_SUB_UNIVERSE_SHARPE"]["value"]  # 1.63
   row["robust_universe_sharpe"] = checks["LOW_ROBUST_UNIVERSE_SHARPE"]["value"]
   row["cluster_test"]           = checks["CLUSTER_TEST"]["value"]            # 常是 WARNING
   # ★ 就绪判据用 sharpe（两格式都有），**不要用 2Y 判就绪**——它天生就晚出现
   ```
   `checks[].result ∈ {PASS, FAIL, WARNING, PENDING}`：
   **只有 `FAIL` 算挂；`WARNING` 不是失败**（但也不是安全）。
   ⇒ `failed_ra_count` = FAIL 的个数，直接数出来即可。

### 0.4.2 ★ 重建/大改脚本后，**第一波必须先单条跑通**

2026-10-05 重建 `run_wave_single_fanout.py` 后**连续踩了3 个坑**：
导入路径（`_pyenv` 在 `tools/`）→ 返回元组不一致 → metrics 未就绪。
**每个坑都会让整批报废或丢指标。**

⇒ **纪律：重建/大改后的第一波，先用该波 items 里的第 1 条跑单条探针**，
确认「提交成功 + 指标齐全」再放批量。
（探针用 `json.dump([items[0]], ...)` 临时生成，不污染正式 items。）


### 0.5 逐条派发天然免疫连坐（与 batch-kill 的区别）

`run_wave_single_fanout.py` 是**逐条独立 POST `/simulations`**，
所以某条 400 **不会连带取消同批其他条**（实测：wave328 的 S3/S4 400，其余全部正常完成）。
⇒ **连坐铁律主要针对 `create_multi_simulation`（平台批量 multisim）路径**。
但失败条仍进 checkpoint，续跑会再试（无害但吵）——
已确认某形态恒被拒时，**从 items 里删掉它**，别靠 `--fresh` 掩盖。

### 0.6 ★ 已实测的「跨族通用」vs「族特异」杠杆（EUR，2026-10-05 三波实证）

**跨族通用（可直接复用，不必重扫）**：

| 杠杆 | 效果 | 备注 |
|---|---|---|
| **`maxTrade = ON`** | **TO 降 47–58%**，S/F/2Y 全升 | long_term 族 −47%、analyst 族 −58%，两族同向；**默认 ON，要测"关掉"须显式写 OFF** |
| **universe 越宽越好** | 单调 | TOPCS1600 > TOP2500 > TOP1200 > TOP800 > TOP400（两族同向；M1 族对窄池子更敏感，TOP1200 时 2Y 变负） |

**族特异（换族必须重扫）**：
`hump`（risk70 甜区 0.002 / analyst 0.001 最佳但整体有害 / CNN 仅 0.001）｜
`signed_power`（analyst 略降 / long_term 陡降）｜
`group_zscore`（C9 族最优 sub1.10 / analyst 族最优 sub0.91 / long_term 族降 S）｜
`ts_delta`（只对财务慢变量有效，模型预测类全灭）｜
`ts_mean`（long_term 族降 S）｜`truncation`（**M1 族 no-op**）｜
`neut`（EUR 用 `FAST`/`SUBINDUSTRY`，**`COUNTRY` 与 `CROWDING` 都降 S**）

**no-op 快速识别法**：若两条只有某设置不同的变体**逐位相同**（S/F/2Y/sub/TO 全等），
⇒ 该设置在此族是 **no-op**，直接排除，不必再排档位。
（实测：`winsorize(std=3/4/6)`、`truncation(0.08/0.20)` 在 M1 族、`nanHandling` 均属此类。）

### 0.6.1★★ 杠杆是【字段特异】的，不是通用的——必须在多个字段上实测增益

**这是比「族特异」更强的版本**：实测把 `group_zscore(·, subindustry)`
施加到 CASSIE 族 **15 个字段**（同族、同机制、同设置档，只有字段不同）：

| 增益 | 字段数 | 例子 |
|---|---|---|
| **正增益** | 3 / 15 | 短债增长率 +0.23、极度破产压力 +0.07、CASSIE综合分 +0.25 |
| **负增益** | 10 / 15 | 长债/权益变动 −0.28、循环信贷 −0.39、**债务加权利率 −0.81** |

⚠ **最大负增益恰好落在「裸形态最强」的那个字段上**（W9 裸S1.48 → 加杠杆后 0.67）。

⇒ ★★ **「杠杆在字段 A 上有效」完全不能推出「对同族字段 B 有效」。**

**实操纪律**：任何新杠杆都必须**在 ≥3 个「已知信号强度不同」的字段上实测增益**。
- 只测最强字段 ⇒ 会得出"杠杆无效"（错，W9 是被杠杆打残的）
- 只测弱字段 ⇒ 会得出"杠杆普遍有效"（错，3/15 只有 3 个受益）
⇒ **正确做法是取「裸形态 S 高/中/低」各一个字段做对照**，
   报告「增益分布」而不是「单个增益」。

### 0.6.2 副产品：跨波次逐位复现 = 设置档确定性的验证

`wave336` 的 G18 与 `wave337` 的 H16（不同波、不同 items 文件）
给出**逐位相同的指标**（S1.83/F1.29/2Y1.56/sub1.83）
⇒ **平台仿真在相同 (表达式, settings) 下是确定性的**。
这是「续跑/checkpoint 可信」的前提；若不成立，续跑与去重逻辑都要重估。
（可作为修复运行器后的**回归验证手段**：改动后重跑一条已知变体，比对是否逐位一致。）

---

## 1. 第一道：候选实测（`get_datafields`）

**本地 catalog 列出 ≠ 平台存在。** 实测 EUR 7 个候选中 **3 个平台侧 `count=0`**
（`model193` / `multi_horizon_alpha` 等），直接白丢。

### 1.0 ★★★ 信息类型判据（**换数据集前必问，比 coverage 更重要**）

2026-10-05 实测发现的两类信息在 EUR **方向相反**，跨 3 个独立数据源验证：

| 信息类型 | 定义 | EUR 方向 | 代表 |
|---|---|---|---|
| **客观基本面事实** | 已发生、可验证、**不含预期** | **正向** ✅ | CASSIE `ocf_currliab` 偿债覆盖率变化 → S1.94 |
| **主观预期 / 看多程度** | 关于「**别人怎么看**」 | **反向** ❌ | 并购可能性 −0.80、目标价上行空间 −0.53、净敞口 −0.62、估值分项 −0.48 |

**证据强度**：`acquisition_model`（18条，15条负）+ `analyst45`（18条）
= **3 个独立数据源、6 类分项、9 条独立信号方向全部一致为负**；
加 `reverse()` 后 **16/16 精确对称转正**（−1.13↔+1.13、−0.80↔+0.80）。

⇒ ★ **实操判据**：选字段时先问「**这是已发生的事实，还是关于预期的判断？**」
后者在 EUR **直接取反**再挖，比正向挖更省波次。
学术对应：过度乐观（overoptimism）/ 买入拥挤（crowded long）/ 预期过度定价。

⚠ **但反向信号有两个硬伤**（实测）：
1. **S 幅度不足**：反转后最高 1.13，距 1.58 差 0.45。
2. **2Y 全面恶化**：反转后 2Y 全部 0.00–0.86，**无一条过线**
   ⇒ **S 与 2Y 在此机制里是跷跷板**，要救必须走「2Y 车道」（上调 decay / 长窗口），
   而**不是继续调 S**。
⚠ 且今日最强杠杆 `group_zscore(·, subindustry)` 在此是**负增益**（+0.80 → +0.71）——
   再次印证「杠杆 × 信号方向也是耦合的」。

### 1.0.1 ★★★ 跷跷板判据：什么时候该停（**比继续扫更重要**）

反向机制救不回来，是因为 **S 与 2Y 是严格跷跷板**（实测 17 条）：

| 分组 | S | 2Y |
|---|---|---|
| 高 S 组（reverse44/88/132 × decay 250–400）| 1.04 – 1.17 | 0.55 – 0.71 |
| 高 2Y 组（水平值 × decay=400）| 0.59 – 0.61 | 0.85 – 0.88 |

⇒ **调任何设置档都只是在跷跷板上挪支点**，无法同时抬两端。
⇒ 判据：**扫完 3 条「2Y 车道」变体后，若仍是「S 高则 2Y 低 / 2Y 高则 S 低」，立即归档。**
**不要**继续扫第 4、5 条——那只是换个支点，不是解法。

**★★ 先分清「跷跷板」还是「死墙」—— 这是该不该扫 2Y 车道的开关**（2026-10-06 实测）：

| 形态 | 判据 | 动作 |
|---|---|---|
| **跷跷板** | 两端**各差 ≤0.5**（如 S 1.17 / 2Y 0.88，闸门均 1.58）| 值得扫 2Y 车道（调 decay 能挪支点）|
| **死墙** | **S 缺口 > 1.0**（如 S=0.20 / 2Y=1.50）| **直接归档**，不扫 2Y 车道 |
| **★换手–2Y 硬互斥（骨架特异）** | S 已过线、只卡 2Y；**≥2 种独立的降换手机制**（设置层 `decay` / 信号层 `ts_target_tvr_decay` / 外层 `hump`）把 2Y 一致压到同一水位，且线性外推的「2Y 过线所需 TO」与 `HIGH_TURNOVER` 上限**夹出 <0.01 的可行窗** | **判该骨架死，不再扫参数**；要救只能**换骨架形态** |

**第三种形态实证（2026-10-29 GBR tm_17，差分骨架）**：S 3.09–3.22 全过线，只卡 2Y。

| 机制 | TO | 2Y |
|---|---|---|
| 基线 `decay 0` | 0.8298 | 1.73 |
| 设置层 `decay 2` | 0.5971 | 1.47 |
| 信号层 `ts_target_tvr_decay 0.6` | 0.6008 | 1.47 |
| 外层 `hump=0.0012` | 0.3852 | 1.46 |

⇒ `d(2Y)/d(TO) ≈ 1.12`；要 2Y ≥ 1.58 需 TO ≥ 0.696，而硬线 TO ≤ 0.700 ⇒ **可行窗 ≈ 0.004**（三种机制殊途同归，不是参数没调对）。

⚠⚠ **但这条互斥是「骨架特异」的，不是字段固有的** —— 换骨架形态即可解除。同一字段换**水平值**骨架后：

| 骨架 | TO 区间 | 2Y 区间 | `d(2Y)/d(TO)` | RA |
|---|---|---|---|---|
| 差分 `ts_av_diff(·,22)` | 0.43 → 0.83 | 1.39 → 1.73 | **≈ 0.85** | 卡 LOW_2Y |
| **水平值 `winsorize(std=2)`** | 0.55 → 0.78 | **2.06 → 2.14** | **≈ 0.35** | **`failed_ra_count=0`** |

⇒ 水平骨架斜率只有差分的 40%，且 2Y 起点高 0.4 ⇒ RA 全过。
**所以判「换手–2Y 互斥」前必须先问：这是字段的属性，还是这个骨架的属性？** 默认先试水平值 / 比率形态（非线性变换、不做日频差分），再判族死。

⚠ **附带剪刀差（必须同时看）**：降换手会把 **prod 推高**（差分 TO0.83→prod0.65、TO0.60→prod0.70；水平 TO0.78→prod0.76、TO0.55→prod0.84）。
⇒ **在换手维度上 prod 与 2Y 反向**，靠 `decay` 同时降两者不可能；破 prod 只能走「改持仓」，见 `wq-prod-lever-self-lock-guard` §一。

实测对照：`institutions6` 的 `机构持股总量` 2Y 高达 **1.50**（距线只差 0.08），
看着像"只差一步"，但 **S=0.20（缺口 1.38）⇒ 死墙**。
⇒ **只看 2Y 会被"差一点点"骗进无效波次**；**必须两个缺口同时看**。

```python
# ★ 判断该不该救：算 S 与 2Y 各自距闸门的缺口
gap_s= 1.58 - sharpe
gap_2y = 1.58 - two_year_sharpe
if gap_s > 1.0:          # 死墙——S 几乎为零，调什么设置档都没用
    archive()# 直接归档，别发波
elif max(gap_s, gap_2y) <= 0.5:  # 跷跷板——值得扫 2Y 车道
    sweep_decay_and_window()
```

**三条 2Y 车道（通用，按优先级试）**：
1. `decay` 上调（40 → 160 → 250 → 400）——最快、成本最低；⚠ 但降换手会**同时把 prod 推高**（见上表剪刀差）
2. 长 `ts_delta` / `ts_rank` 窗口（44 → 88 → 132 → 176 → 252）
3. ★★★ **水平值代替变化量**（`rank(x)` 替代 `rank(ts_delta(x,d))` / `ts_av_diff`）—— **本条增益最大、也最容易被跳过**。2026-10-29 GBR 实测：同字段换水平骨架后 2Y 1.73 → **2.14**、斜率 0.85 → 0.35、`failed_ra_count=0`。**优先试它，再试 1 和 2。**

⚠ 若三条车道跑完两端仍不过线 ⇒ 归档「方向已定、强度不足」，
**但保留机制结论**（如 §1.0 的信息类型判据）——它对下一个数据集仍有用。


```
mcp__wq-brain-http__get_datafields(region=<R>, dataset_id=<DS>, delay=1,
                                   universe=<U>, filter_sharpe=false)
```
- `filter_sharpe=false` **必须显式传**（默认 true 会按 OS/IS Sharpe<0 过滤掉字段）。
- 返回 `count=0` ⇒ 平台侧没有该数据集，**立刻淘汰，不要发批**。
- **覆盖率是硬信息**：EUR 实测 `option_chart_model` 0.44（可用）、
  `workforce_flow_skills` 0.24、`order_book_imbalance` 0.19–0.30
  （80% 无数据 ⇒ CONCENTRATED_WEIGHT / sub 必挂 ⇒ 直接跳过）。

### 1.0.2 ★★★ 「客观事实」只是**必要条件**——还要问「这个事实被市场定价充分了吗」

2026-10-06 前瞻检验**部分证伪**了 §1.0 的信息类型判据。三类「客观事实」实测：

| 机制 | 信息类型 | 更新频率 | 定价充分度 | EUR 实测 |
|---|---|---|---|---|
| CASSIE `ocf_currliab` 偿债覆盖率 | 客观事实 | **季频**（披露稀疏）| 不充分 | ✅ **S1.94** |
| 内部人交易（`insider_feats`）| 客观事实 | 低频 | 不充分 | ❌ S=0.04 |
| **量价技术指标（`price_signal_dl`）** | 客观事实 | **日频/连续公开** | **完全充分** | ❌ **最高 0.55** |
| 持仓 / 目标价 | 主观预期 | 季频 | **过度定价** | ❌ 反向 |

⇒ ★★★ **完整判据= 信息类型（定方向）× 更新频率（定有无增量）**：
- **日频/连续公开的数据（价格、成交量、价量衍生指标）** ⇒ 已被完全定价
  ⇒ **任何变换都是噪声**，不要因为"覆盖 1.0 + alphaCount 低"就发批（我踩过）。
- **低频/披露稀疏的数据（季度财务、持仓申报）** ⇒ 市场反应不足 ⇒ **首选方向**。
- **主观预期类** ⇒ 直接取反，比正向挖省一半波次（§1.0）。

⚠ 排序优先级：**低频客观事实 > 主观预期（取反） > 日频公开量价（基本跳过）**。

### 1.0.3 ★★ 平台可能把**不同表达式合并成同一个 alpha** ⇒ 波次样本量静默打折

实测（2026-10-06 wave344）：`normalized_trend_indicator_0` 与
`normalized_volume_indicator_0` **字段名不同、表达式不同**，但平台对两者返回
**同一个 alpha id `786w7LXv`** —— 7 对全部如此。
**MCP `get_alpha_details` 核实**：平台侧 `code` 只保留第一个表达式（趋势版）。

⚠⚠ **平台不给任何提示**：两个请求都成功、指标逐位相同、无 warning。
⇒ 不做本地比对就会以为「14 个字段都测了」，实际只有 7 个独立信号
⇒ 进而错误判断「这个族覆盖充分、可以下结论了」。

⇒ ✅ **运行器已内置检测**（`run_wave_single_fanout.py::report_id_collisions`），
波次收尾自动打印「落点数 / 唯一表达式数 / **唯一 alpha id 数**」并列出被共享的 id。
实测输出：`落点 17 / 表达式 17 / 唯一 id 9` ⇒ 一眼看出打折。

⇒ ★ **评一个数据集的搜索空间大小，要用「平台侧有效独立信号数」，不是 DB 字段数**：
`price_signal_dl` 的三层漏斗 = DB 168（跨 delay 重复）→ 去重 14 → **平台合并后 7**。

### 1.1 ★★ 覆盖率闸要查「**你要用的那个字段**」，不是数据集级 coverage

⚠⚠★ **先看这条：本地四闸 `S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥1.0` 比平台严**。
2026-10-06 实测 `zqb9M1e8`（Piotroski F-Score，S1.54/2Y1.63/**sub 0.84**）：
**平台 `checks.fail = []`**，`LOW_SUB_UNIVERSE_SHARPE(0.84)` 被判**PASS**，
唯一阻塞是 `LOW_SHARPE`（1.54 vs 1.58）。
⇒ ★ **本地四闸只是"快速筛"，不是平台口径**。候选判定必须回到：
```python
det = get_alpha_details(aid)          # MCP 或 brain_client
if det["checks"]["fail"]:             # ① 平台硬挂清单
    reject()
elif det["ra"]["ra_failed"]:          # ② ★ 最容易漏的一条！
    fix(get=det["ra"]["ra_failed_checks"])
else:
    # ③ 还要 prod/self 平台实测（check_correlation refresh=True）
    accumulable()
```
⚠ **别把 sub=0.84 当成过不了闸** —— 平台线比 1.0 低。
⚠★ **别只看 `checks.fail` 就以为能提交** —— `ra_failed=true` 时仍不可提交。

#### 1.1.1 ★★★★ 「可提交」的**三条硬条件，缺一即不可**（2026-06 实测踩坑）

| # | 条件 | 取值来源 | 最易漏 |
|---|---|---|---|
| ① | `checks.fail == []` | `get_alpha_details` | ✅ 容易查 |
| ② | ★ `ra.ra_failed_checks == []` | `get_alpha_details` | ❌ **最容易漏** |
| ③ | `prod < 0.7` **且** `self < 0.7` | `check_correlation(refresh=True)` | ❌ 常只测 prod |

**实测反例（三颗全过①③，但卡②）**：

| alpha_id | S | 2Y | prod | self | `checks.fail` | `ra_failed_checks` | 可提交? |
|---|---|---|---|---|---|---|---|
| `qM0Aqp3A` | 1.65 ✅ | 1.38 ❌ | 0.6924 ✅ | 0.454 ✅ | `[]` | **`["LOW_2Y_SHARPE"]`** | ❌ |
| `e7QORW9z` | 1.65 ✅ | 1.39 ❌ | 0.6899 ✅ | 0.451 ✅ | `[]` | **`["LOW_2Y_SHARPE"]`** | ❌ |
| `vR2LgZ83` | 1.63 ✅ | 1.40 ❌ | 0.6832 ✅ | 0.445 ✅ | `[]` | **`["LOW_2Y_SHARPE"]`** | ❌ |

⇒ ★★★ **本地 `fail_reasons` 字段不能代替 `ra.ra_failed_checks`**：
本地字段为空 ≠ 平台通过。本地提取器读的是 `checks.fail`，而 `ra_failed_checks` 是**另一层**。
⇒ ★ **报"可提交数"前必须逐条过这三关**，否则会多报（我今天差点多报 3 颗）。
⇒ ★★ **而且同族要折算**：上面三颗只差 `std`（0.25/0.35/0.40）⇒ **同族，只计 1 颗**。


**实测教训（2026-10-05，整波 18 条全灭）**：选 `analyst_base_ref` 时看到
数据集级 `coverage=0.832`（看起来很好），就过了闸；发完 18 条波才发现
**信号字段 `consensus_*` / `num_estimates_*` 的覆盖率只有 0.3158**
（68% 股票无数据）⇒ 论坛三条金标准（PEAD / 修正>水平 / 广度>幅度）全部失效，最高 S 仅 0.61。
**数据集级 0.832 是被 `last_close_price`(0.968)、`dilution_adjustment_ratio`(0.968)
这类高覆盖但无信号的辅助字段拉高的。**

```sql
-- ★ 正确做法：按【字段】查覆盖，不是按数据集
SELECT f.field_name, f.coverage FROM fields f JOIN datasets d ON d.id=f.dataset_id
WHERE d.name = '<DS>' ORDER BY f.coverage DESC;
```

**阈值判据**：
| 字段覆盖 | 裁决 |
|---|---|
| **< 0.32** | ❌ 必跳过（68% 无数据 ⇒ 无横截面区分度，**任何杠杆都救不回来**）|
| 0.32–0.55 | ⚠ 可试（`analyst_factor_signals` 覆盖 0.5458 却产出 S1.66 全闸）|
| 0.55–0.85 | ✅ 正常 |
| > 0.95 | ✅✅ 优先 |

**选集时用「字段平均覆盖」排序，不用 `datasets.coverage`**（后者被辅助字段稀释）：

### 1.1.2 ★★★★ 「弱信号」vs「信号不存在」—— 用**正反对称性**判别，决定换构造还是归档

2026-06 实测（EUR `qfl_nlp_calltranscript`，cov≈0.45）——首探 15 条 S 最高仅 0.68，
初看该归档。但**同波内8 对 `reverse` 对照全部完美对称**：

| 正向 S | 反向 S | 对称? |
|---|---|---|
| +0.34（CEO 问答正面情绪）| **−0.34** | ✔ |
| +0.34（买方提问数）| **−0.34** | ✔ |
| +0.26 / −0.26（VADER 正面）| ✔ | |
| +0.24 / −0.24（回答阅读难度）| ✔ | |
| −0.08 / +0.08（平均评级）| ✔ | |
| +0.38（管理层-问答余弦距离）| **−0.38** | ✔ |

⇒★★★★★ **判别法（先看对称性，再看幅度）**：

| 形态 | 特征 | 裁决 |
|---|---|---|
| **信号不存在** | S ≈ 0，**且正反双向都≈0** | ❌ **直接归档**，别再投槽位 |
| **弱信号** | S 0.2–0.8，**正反完美对称** | ★★ **换构造再试**（方向已定，只差幅度）|
| 强信号 | S > 1.5 且正反对称 | ✅ 可进生产 |

⇒ ★ **为什么对称性是可靠证据**：`reverse(X)` 的 S 必然是 `-S(X)`（同一持仓反向），
**若数值逐位相等 ⇒ 说明该alpha 确实有方向性信息**（而非噪声）。
反过来若正反**都≈0**，说明连噪声方向都没有。
⇒ ★ **纪律：任何"看起来很弱"的候选，必须先看它的 `reverse` 对照**，
   **没测 reverse 就没有资格判死**（本会话四次实证：wave341/345/351/354）。
⇒ ⚠ 例外：`sub 0.4`（cov 0.45 的小子宇宙劣势）可能使该维度**永远过不了 sub 闸**，
   即使 S 够高——这是**结构性劣势**，不是调参能解决的。

### 1.2 ★★★ `field_type = 'UNIVERSE'` 的字段**不是信号**，是选股池定义（2026-10-06 实测）

**筛选优先级：优先「低频 + 离散 + 多因子合成 + 高覆盖」的字段。**

2026-10-06 EUR 实测：连续测死10 类机制（信用绝对水平 / 新闻情绪 / 季节 /
分析师预期 / idea目标价 / 并购概率 / 内部人 / 日频量价 / 机构持仓），
**唯一新活机制是 `oth401_qes_gamef_pscore`（Piotroski F-Score）**，
S1.54 / 2Y1.63 / F1.07 / `checks.fail=[]`，只差 S 0.04。

它凭什么活下来，而前9 类死了：

| 特征 | Piotroski F-Score | 已死的9 类 |
|---|---|---|
| **更新频率** | **季频**（市场反应不足）| 日频/连续（已完全定价）|
| **形态** | **离散评分**（0–9 整数，横截面区分度强）| 连续值（rank 后区分弱）|
| **信息维度** | **合成 9 个会计异象** | 单一原始字段 |
| **覆盖** | 0.854（小宇宙不掉）| 0.32–1.0 参差 |

⇒ ★ **实操选集排序**：
1. 找**评分/分数/综合指数**类字段（`pscore` / `cscore` / `score` / `mohanram`）——
   它们天然把多个弱信号压成一个强信号，**比单个原始字段有效得多**。
2. 覆盖 ≥0.8（保证 sub universe 不掉）。
3. 确认它**不是**日频量价衍生（否则按 §1.0.2 跳过）。

⚠ 同一机制内其他评分字段（现金流覆盖 1.41 / 综合 Score 1.31 / Mohanram 1.23）
**方向一致但强度不够** ⇒ 强度逐字段不同，**不能假定"同机制都有效"**，
但**方向一致本身就是证据**（可据此选下一个尝试对象）。

**陷阱数据集 `univ1`**：在 EUR 未测数据集排序里（按 aCnt 升序）**排第1 名**——
`alphaCount=1`（极低拥挤）、`coverage=1.000`（满分）、6 个字段。
**但它的字段全是 `top500` / `top2000` / `top1200` / `minvol1m` / `topdiv3000`…**
`field_type = UNIVERSE`、`description = "No field description"`
⇒ **这是 universe 定义（选哪些股票进池），不是 alpha 信号**，发批必全灭。

⚠ **为什么特别危险**：cov 1.0 + aCnt=1 这两个指标在任何自动排序里都是最优值
⇒ 不查 `field_type` **必踩**，且踩了很难自查（字段名看起来像正常因子）。

```sql
-- ★ 选集时必须先排掉 UNIVERSE 类型
SELECT f.field_name, f.coverage, f.field_type
FROM fields f JOIN datasets d ON d.id = f.dataset_id
WHERE d.name = '<DS>' ORDER BY f.coverage DESC;
-- 见到 field_type='UNIVERSE' ⇒ 整个数据集直接淘汰，不要逐个字段看
```

#### 1.2.0 ★★★★★ 【整批失败】先诊断是「设计问题」还是「平台故障」—— 否则会把故障误判成死信号

2026-06 实测：wave357 32 条**已过四道闸**（arity 32/32、无重复、禁混信号、字段全存在），
跑出**成功 0 / DROP 25**，`API_ERR:Failed to create simulation | MSG:None`。

### ★★★ 决定性诊断：**拿一条【已知成功过】的表达式单条复测**
```python
# wave356 刚跑出 S=0.99 的同一条表达式，10 分钟后复测
code = "group_zscore(winsorize(hump(rank(vec_avg(accounting_forensics_factor_2)), "
       "hump=0.002), std=0.4), country)"
→ FAIL | err=Failed to create simulation | msg=None       # ★ 平台故障
```
**同一条刚成功的表达式也失败 ⇒ 纯平台侧故障（限流/过载），与设计无关。**

| 现象 | 诊断步骤 | 裁决 |
|---|---|---|
| 整批 DROP + `MSG:None` | ★ **拿一条已知成功过的表达式单条复测** | 复测也失败 ⇒ **平台故障，停手** |
| 整批 DROP + `MSG` 有具体文本 | 直接读 `message` | 平台已告诉你原因（如 `does not support event inputs`）|
| 部分 DROP + 部分成功 | 对比成功/失败的表达式 | 设计问题，逐条归因 |

⇒★★★★★ **纪律：遇整批失败，先诊断再改设计。**
否则会把平台故障写进"实证结论"—— 本波若不诊断，**就会把法证会计族 7 个变体
全部误判为"这族没信号"而错误归档**（而它其实是 S0.99 的活机制）。
⇒ ★ **其他"看起来像故障"的信号**：日志里出现 `Simulation created with ID: xxx`
**之后才fail** ⇒ 平台已接受请求、失败发生在后续阶段 ⇒ 几乎不是表达式问题。
⇒ ★★ 这是本工作区第 4 次「信息在别处」（`checks.fail` vs `ra.ra_failed_checks`
→ `two_year_sharpe` 只在 `is.checks` → `error` vs `message`
→ ★ **「全部失败」时用「已知成功表达式」做对照实验**）。

### 1.2.1★★★★★ `field_type = 'VECTOR'`：**必须先 `vec_avg` 归约，且归约要在最外层**

2026-10-06 实测（EUR `qfl_nlp_calltranscript_*`，94 字段全部 `VECTOR`，cov≈0.45）：
**不包 `vec_avg` ⇒ 整批 15 条全部失败**。

★ **逐算子实测（平台真实响应）**：

| 形态 | 平台响应 |
|---|---|
| `rank(X)` | ❌ `Operator rank does not support event inputs` |
| `ts_delta(X, 22)` | ❌ `Operator ts_delta does not support event inputs` |
| `ts_backfill(X, 252)` | ❌ `Operator ts_backfill does not support event inputs` |
| 裸 `X` | ❌ FAIL |
| `vec_avg(reverse(X))` | ❌ `Operator reverse does not support event inputs` |
| ★ **`vec_avg(X)`** | ✅ 成功 |
| ★★ **`reverse(vec_avg(X))`** | ✅ 成功（id=`1YZ7OeGm`） |

⇒★★★★★ **两条硬规则**：
1. **VECTOR 字段必须先用 `vec_avg` 归约**，否则任何时序/截面算子都会撞
   `does not support event inputs`。与 CASSIE `ocf_currliab` 同构（也是 VECTOR）。
2. ★★ **归约算子必须在【最外层】**：`reverse` 等方向变换放在 `vec_avg` **之后**。
   写成 `vec_avg(reverse(X))` 会失败——**`reverse` 也被平台当 event 处理**。

```python
# ★ 正确形态
reverse(hump(rank(vec_avg(X)), hump=0.002))          # 反向
hump(rank(vec_avg(X)), hump=0.002)                   # 正向
subtract(rank(vec_avg(A)), rank(vec_avg(B)))# 两腿都要归约
```

⇒★★★★★ **平台失败响应的三层结构（务必读 `message`）**：
```python
{"error": "Simulation failed or returned no alpha ID",   # ← 无信息量，一律相同
 "message": "Operator rank does not support event inputs. <linkToCommonErrorMessages>…"}
```
**只读 `error` ⇒ 所有失败长得一样 ⇒ 完全无法归因。** 运行器必须拼上 `message`：
```python
msg = "API_ERR:%s | MSG:%s" % (str(res.get("error"))[:80], str(res.get("message"))[:260])
```
⚠⚠ **这是本工作区今天第 3 次「信息在响应里但没读」**（前两次：`checks.fail` vs
`ra.ra_failed_checks`；`two_year_sharpe` 只在 `is.checks` 里）⇒ **固化纪律：平台响应的每个字段都要读。**

⇒★★ **四类字段类型的算子约束汇总（本工作区已全部实测）**：
| `field_type` | 处理方式 | 实测案例 |
|---|---|---|
| `MATRIX` | 直接用 | `oth401_*`（41 字段）|
| **`VECTOR`** | ★ **必须 `vec_avg` 归约，且归约最外层** | `qfl_cassie_convention_ocf_currliab`、`qfl_nlp_calltranscript_*`（94）|
| `UNIVERSE` | ❌ 不是信号，整字段排除 | `univ1`（`top500`/`minvol1m`）|

### 1.3 ★ 同一 dataset 名在**不同 region 下字段集不同** ⇒ 字段闸是唯一可靠防线

实测：`institutions6` 在 DB 里有 **22 个唯一字段**，但加 `WHERE r.name='EUR'` 联表后
**只剩 11 个**（`inst6_num_of_*` / `inst6_value_*` / `inst6_total_*` 全系列在 EUR 不存在）。

⇒ ★ **`SELECT DISTINCT field_name WHERE dataset_name=X` 会跨 region 混入他区字段**，
DB 查询结果**不可直接用于构造表达式**。
⇒ ✅ **唯一可靠防线：`check_wave_fields.py <items> --region <REGION>`**
（它查 `regions.id → datasets.region_id → fields.dataset_id` 三段联表，
与 §90 重建时踩过的 `region_catalog` 坑同一根因）。
⚠ 本地DB 字段名也不等于平台存在 —— 仍以字段闸 + `get_datafields` 为准。
```sql
SELECT d.name, d.alpha_count, AVG(f.coverage) cov_avg
FROM datasets d JOIN regions r ON r.id=d.region_id JOIN fields f ON f.dataset_id=d.id
WHERE r.name='<REGION>' AND d.name LIKE '<prefix>%'
GROUP BY d.id ORDER BY cov_avg DESC;
```
（EUR 实测：`analyst45` cov_avg **1.000**/a=635、`analyst_earnings_ibes` 0.998/a=220
是分析师类最优；而 `analyst_base_ref` 只有 0.552 且信号字段 0.316。）

## 2. 第二道：市场级/ 日历级字段退化判据 ★

`global_seasonal_model` 覆盖率中位 **0.997**、269/300 字段 alphaCount=0
——各项都是全 EUR 最好。但排最前的字段是
`iso_week_number` / `month_indicator_code` / `market_regime_2phase` /
`market_regime_4phase_*` / `future_event_update_flag`……
**这些是【市场级/日历级】变量—— 同一时刻所有股票取值完全相同。**
⇒ 在横截面口径下 `rank()` / `quantile()` 作用其上**退化为常数（无区分度）**，
提交就是「全市场同权重」⇒ 天然无 Sharpe 且必挂 CONCENTRATED_WEIGHT。

**判据：发批前必须分清字段是【个股级】还是【市场级】**；市场级字段只能走
① 时序交互（`ts_delta`/`ts_zscore` 相对自身历史）② 与个股信号交互（`multiply`/`subtract`）。

**落地做法**：按描述里的语义判定 —— 含 `market_regime` / `week` / `month` /
`calendar` / `iso_week` / `quarter` / `future_event` / `next_event` 的都是市场级。
（这可能解释了历史 seasonal 族普遍无信号的根因，不只是"季节性无效"。）

### 2.1 ⚠⚠ 实测修正：`group_zscore` **不退化**（原判据在此算子下是错的）

2026-10-05 实测（EUR，同一骨架只换分组轴）：

| 分组轴 | S | 2Y | sub |
|---|---|---|---|
| **subindustry** | **1.94** | 1.59 | **1.96** |
| industry | 1.64 | 1.75 | 1.58 |
| sector | 1.61 | 1.71 | 1.61 |
| **market** | **1.62** | 1.75 | 1.62 |
| country | 1.47 | 1.49 | 1.43 |

⚠ **`group_zscore(·, market)` 竟拿到S1.62，完全不退化**——
而 `market` 分组内所有股票同值，组内 std=0，z-score 数学上应无定义。
**实测说明平台在组内 std=0 时回退到原值** ⇒ 等价于「没分组」。

⇒ **两条修正**：
1. **原判据只对 `rank()` 成立，对 `group_zscore()` 不成立** ——
   `group_zscore` 有 std=0 回退机制，市场级字段在它下面**不会**退化成常数。
   ⇒ 别因为字段是市场级就排除 `group_zscore` 形态。
2. **更重要的规律：分组轴的【粒度】决定效果，粗粒度之间无差异。**
   `industry` / `sector` / `market` 三者几乎相同（1.61–1.64），
   只有 **`subindustry`（最细）显著更好（1.94，Δ+0.30）**。
   ⇒ **扫分组轴时，真正要测的是"更细的粒度"，而不是横着换不同名字的粗粒度。**
   经验序：`subindustry` > `industry` ≈ `sector` ≈ `market` > `country`。
   ⚠ `country` 在 EUR **降 S**（与「EUR 是多国市场、应剔除国别暴露」的直觉相反）。

### 2.2 ★★★★ 【最强反例】「粒度决定效果」只在 CASSIE 族成立，**换机制后完全反转**

2026-10-06 实测（EUR，`hump(rank(X), hump=0.001)` 骨架，只换分组轴）：

| 分组轴 | **CASSIE `ocf_currliab`** | **FUNDAMENTAL `pscore`** |
|---|---|---|
| **subindustry** | **1.94（+0.29 最强）** | **1.29（−0.25 最差）** ❌ |
| country | 1.47（−0.07） | **1.73（+0.19 最强）** ✅ |
| market | 1.62 | 1.54 |
| sector | 1.61 | 1.52 |
| industry | 1.64 | — |

⇒ ★★★ **同一杠杆、同一波、同一设置档，两个字段上跨度 0.54（+0.29 ↔ −0.25）。**
⇒ ★★★ **所以「细粒度总是最好」是错的。正确说法**：
**分组轴的效果由该轴与「字段经济含义」的重合度决定**——
- `pscore`（财务质量评分）按 `subindustry` 标准化 = **过度标准化**：
  把同一细分行业内最有信息量的质量差异全抹掉（行业内财务质量本来就该有差异）。
- `pscore` 按 `country` 标准化 = 剥离**真实噪声**：
  欧洲各国会计制度/汇率/披露差异本就污染跨国可比性 ⇒ country 剥离的正是噪声。

⇒ ★★★ **可操作：分组轴不是「越细越好」，而是「找与字段经济含义正交的尺度」**。
| 字段类型 | 优先试的分组轴 | 原因 |
|---|---|---|
| 财务/质量/评分类 | **`country`** | 剥离制度/汇率/披露差异 |
| 现金流/偿债类（横截面行业内可比）| `subindustry` | 剥离行业景气度 |
| 技术/量价类 | 通常无需分组（§1.0.2 已证该类无增量）| — |
⚠ **不要照搬别的字段测出的最优轴**——这是最容易白扫一整波的错误。

### 2.3 ★★ `decay` 对【离散/阶梯式】字段几乎无效，不要扫

2026-10-06 实测（EUR，`pscore` = Piotroski F-Score，**0–9 整数评分，季度更新**）：

| decay | 40 | 80 | 100 | 160 | 200 | 250 | 400 |
|---|---|---|---|---|---|---|---|
| S | 1.55 | 1.54 | 1.51 | 1.54 | 1.53 | 1.54 | 1.55 |

⇒ **跨度仅 0.04，等于什么都没发生。**
⇒ 对比 CASSIE（`ocf_currliab` **连续比率**）：decay 40→160 让 2Y 1.76→1.81（§91.1）。

#### 2.3.1 ★★★★★ 【统一判据·推广】**所有 `ts_*` 时序算子对「时序变异不足」的字段一律无效**

同一字段上又测了 `ts_rank` / `ts_mean` / `ts_zscore`（本应是最强的 2Y 车道）：

| 算子 | 同族连续字段（CASSIE） | **同一离散字段（pscore）** |
|---|---|---|
| `decay` 细网格 | 2Y 1.76→1.81 ✅ | S 1.51–1.55 ≈ 不变 ❌ |
| `ts_rank(·,132)` | **2Y 1.88（全波最高）** ✅ | **S 1.63 → 0.43** ❌ |
| `ts_mean(·,132)` | — | S 1.63 → 1.21 ❌ |
| `ts_zscore(·,132)` | — | S 1.63 → 0.13 ❌ |

⇒ ★★★★ **统一根因：时序算子需要信号有足够的【时序变异】。**
- **连续比率**（偿债覆盖率、收益率）逐日跳动 ⇒ `ts_*` 有东西可算。
- **0–9 整数评分 / 季频指标**：132 日内值几乎不变 ⇒ `ts_rank` 得到**大量并列**
  ⇒ **区分度归零** ⇒ S 崩塌。

⇒★★★★★ **选字段后先问一句：它有足够的时序变异吗？**
```python
# 判断依据（读字段描述即可）
低频离散 = 描述含 score/rating/grade/level，或更新频率 ≤ 季频
if 低频离散:
    skip = ["decay 细网格", "ts_rank", "ts_mean", "ts_zscore", "长 ts_delta"]
    # 一个都不要扫——实测 4 个全灭，浪费 15+ 槽位
```
⇒ ★ **对这类字段唯一有效的方向是【横截面维度】**：分组轴（§2.2）、
与其他信号做 `divide` / `subtract(rank,rank)` 组合、以及**换子成分字段**。
⇒ ★ **别用"论坛说这条是 2Y 车道"就照搬** —— 车道有效性**是字段特异的**。

### 2.3.2 ★★★ 2Y 缺口要诊断**逐年**，而不是扫杠杆

2Y =最近两年平均，**一年的塌点就能拖垮它**。用
`get_alpha_yearly_stats(alpha_id)` 定位是哪一年，再决定怎么修。

实测两个案例（EUR）：

| 机制 | 2020 | 2021 | 2022 | 2023 | 2Y |塌点 |
|---|---|---|---|---|---|---|
| CASSIE `ocf_currliab` | 0.99 | 2.13 | 2.48 | **0.88** | 1.76 | **2023** |
| FUNDAMENTAL `pscore` | 1.29 | 2.09 | **0.22** | 2.68 | 1.40 | **2022** |

⇒ ★★★ **两条机制塌的年份不同 ⇒ 不是数据/工具问题，是各自的风险暴露不同。**
⇒ ★ 诊断出塌点年后，**先看该年是否同时也是 `returns` 异常低**
（pscore 2022 returns 仅 **0.81%**，vs 2023 的 9.60% ⇒ 确认是那一年本身没赚）。

#### 2.3.2.1 ★★★★ 【必做·分水岭诊断】再跑一遍 `reverse` 版比逐年 —— 区分「信号消失」vs「方向反转」

**这是判断"该不该继续修"的唯一可靠依据。** 实测（EUR pscore，`reverse` 版 `786wO73Z`）：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | **2022** | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| **正向** S | +3.28 | 0.01 | +1.39 | +1.48 | +3.13 | +1.83 | +1.29 | +2.09 | **+0.22** | +2.68 |
| **反向** S | −3.54 | 0.03 | −1.32 | −1.53 | −3.21 | −1.84 | −1.36 | −2.09 | **−0.22** | −2.68 |
| 归一化 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |

⇒ ★★★★ **逐年逐位取反 ⇒ 该年是「信号消失」而非「方向反转」。**
反向版那年也是 ≈0 ⇒ **正反两版都无信息 ⇒ 任何表达式变换都不可能造出信息。**

| 诊断结果 | 含义 | 动作 |
|---|---|---|
| 反向版该年**符号相反、幅度相当** | 方向反转，信号仍在 | ✅ **可修** —— 换轴 / 换子成分 / 调窗口 |
| 反向版该年**也 ≈0** | **信号消失** | ❌ **不可修** —— 停止投入，换机制 |

⇒ ★★★★★ **为什么必须先做这一步（我的实测代价）**：我先假设
「2022 塌是营运资本分项造成」⇒ 发了 **19 条对冲波**
（`subtract(rank(pscore), rank(毒分项))` / `divide(pscore, 毒分项)` 等）
⇒ **全部比裸 pscore 更差**（S −0.29~−0.71，2Y −0.78~−1.21）。
根因：**合成评分的各分项已相互抵消，不是正交的毒源**，
拆出来单测等于「用噪声去减有信息信号」。
⇒ ★★ **教训：不要假设"合成评分里的某个分项是毒源"，先做反向版逐年诊断。**
⇒ ★ 顺带：`reverse` 版还顺带确认了**方向确定性**（本 skill §1.0 的做法第四次生效）。

## 3. 第三道：字段存在性硬闸

**本工作区的语法检查器只查算子、不查字段**，字段名笔误会**静默发批 → 平台返回
ERROR → 白跑一条槽位**。实测被抓过两次：`qa_vader_neg`（漏 `ceo_`）、
`long_term_regime2_quantime1_120d_pred`（漏 `l`）。

`tracking/<R>/scripts/check_wave_fields.py`：
```bash
$WQ_PY tracking/<R>/scripts/check_wave_fields.py tracking/<R>/candidates/eur_<tag>_items.json \
    --region EUR --strict [--cartesian --dataset <DS>]
```
它做三件事：① 算子语法（复用 `op_arity`）② **把表达式里所有标识符与该 region
全量字段并集比对** ③ 顺带查「同表达式+同设置档」的重复变体。

**两个必须知道的实现细节**：
- ★ 字段并集走 `data/wqb.db` 三段联表：
  `fields JOIN datasets ON dataset_id JOIN regions ON region_id WHERE regions.name=?`。
  字段名在 **`fields.field_name`**（不是 `id`）；`region_id` 是**数字外键**。
  猜错任一处 ⇒ **闸报假警报**（实测曾把真实存在的字段全报"不存在"，16 条全红）。
  ⚠ **可信度分层**：`fields` / `datasets` 的 `region_id` **可信**（一个数据集归属一个区域，同名数据集在各区是不同行）；**不可信的是 `alphas.region_id`**（同一 id 下混装多区，见 §0.0.6b）。两处都叫 `region_id`，行为完全不同，别混为一谈。
- ★ **并集为 0 时必须返回非 0 拒绝放行**（防"假绿灯"）。
  **永远绿灯的闸比没有闸更危险；永远红灯的闸会让人直接绕过它——两种一样坏。**
- 回归验证：故意写错字段（如 `..._ocf_currlib`）必须被抓出，且正确字段不误报。

### 3.1 ★★ 本地 catalog 会**反向骗人**：它列出的字段，平台可能根本没有（2026-10-06 KOR 实证）

⚠⚠ 与 §1「本地列出 ≠ 平台存在」是**同一类坑的加强版**：
`ml_factor_proj`（KOR/OTHER 塔）本地 `datasets` 表标 **`coverage=1.0` / 333 字段 / alphaCount=24**，
看起来是最优质的白空间候选；实际 **平台完全不存在 `change_free_cashflow_to_equity`**
⇒ 报 `Attempted to use unknown variable`。

**代价**：一条 unknown variable ⇒ **整个 multisim 被连坐 CANCELLED**（实测 8 条只跑 1 条 ERROR，其余 7 条全 CANCELLED），白占一轮槽位（~10 分钟）。

★ **`ensure_safe_for_dispatch(exprs)` 是 `op_arity` 现行接口**（抛 `ArityError`；旧的
`check_unknown_operators` 已移除）——**它只查算子与元数，不查字段存在性**，
所以这类错误**离线三闸全绿也会发射到平台**。

⇒ **纪律**：对**陌生的、从未产出过成功 alpha 的数据集**（尤其是 `other*` / `model*` 这类
编号数据集），**发批前必须先 `get_datafields(region, dataset_id, filter_sharpe=false)` 实地核字段名**。
对**已验证过高产的数据集**（字段集稳定）可省这一步。

> 补充自 2026-10-06 KOR 0 塔扫描：`ml_factor_proj` 是被这一步漏掉、白烧 1 波的实例；
> 同批其余 4 个数据集因先 `get_datafields` 核验，字段全部命中。

## 4. 第四道：断点续跑去重键必须含全部设置档 ★

**踩过的坑**：设计一波要扫 `rank(x)` × {decay 10/40/100/160, neut FAST/SLOW}——
**5 条表达式完全相同，只有设置档不同**。而运行器当时是：
```python
done = {r["code"] for r in carried ...}          # ❌ 只按 code 去重
todo = [it for it in items if it["code"] not in done]
```
⇒ **一旦断点续跑，这 4 个设置档会被静默跳过**（fresh 不受影响，因 `carried=[]`）。
- 已核实 `submit()` **不**按 code 去重，每条独立 `POST /simulations` 且带各自 settings
  ⇒ 平台侧会正常返回不同 alpha_id，**是本地续跑逻辑单方面丢变体**。

### 4.2 扩展新设置维度时：运行器**三处同步**（缺一不可）

| # | 位置 | 改法 | 漏了会怎样 |
|---|---|---|---|
| 1 | `submit()` 的设置映射 | 加 `("maxTrade","maxTrade")` 等 | items 里写了但不进 settings，**杠杆完全无效** |
| 2 | ★ `_key()` 去重键元组 | 加对应位置 | 同表达式不同该维度的变体**续跑时被静默跳过** |
| 3 | ★ 记录行落盘（成功行 **和** DROPPED 行**两处**） | 加 `"maxTrade": it.get("maxTrade")` | `_key(r)` 读记录行得 `(code,None,…)` ⇒ **每次续跑重跑全部**（比丢变体更糟） |

参考实现（2026-10-05 一次放开 `maxTrade`/`nanHandling`/`pasteurization` 三个）：
```python
def _key(it):
    # 加任何设置维度都必须同步加这里，否则续跑会静默跳过（同 code-only bug）
    return (it["code"], it.get("decay"), it.get("truncation"), it.get("neut"),
            it.get("universe"), it.get("maxTrade"), it.get("nanHandling"),
            it.get("pasteurization"))

def settings_row(it):
    # ★ 记录行必须落盘设置档，否则 _key 两侧对不上
    return {"code": it["code"], "note": it.get("note", ""),
            **{k: it.get(k) for k in ("decay", "truncation", "neut", "universe",
                                     "maxTrade", "nanHandling", "pasteurization")}}
```

**离线验证**（不碰平台）：fresh ⇒ 待跑 N；部分完成(新格式) ⇒ N−已完成；
**旧格式 ckpt ⇒ N（如实暴露"每次重跑全部"）**。

## 5. 禁混信号合规自检（发批前必做）

项目铁律：**禁混信号（含等权两腿 `add`）**。合规只 Mode B；放行 5 形态：
`ts_corr` / `divide` / `subtract(rank,rank)` / `if_else·trade_when` / `group_rank·group_zscore`；
算子数 < 10。**门禁通过 ≠ 合规。**

```python
import re
bad = [it['note'][:4] for it in d if re.search(r'(?<![a-z_])add\(', it['code'])]
print('add 两腿违规:', bad if bad else '无 ✅')
```
⚠ 实测：写「长短窗口相加」时很自然会写 `rank(add(短, 长))` ⇒ **发批前必查**。
换成放行形态即可（`divide(短, 长)` 还能顺带满足「长窗口作分母」的经验）。

## 6. items.json 格式约定

```json
[
  {"code":"rank(x)", "note":"A1 控制行", "decay":40, "neut":"FAST", "universe":"TOPCS1600"},
  {"code":"rank(x)", "note":"A2 decay=10", "decay":10, "neut":"FAST", "universe":"TOPCS1600"}
]
```
- 文件名约定（硬性）：`tracking/<REGION>/candidates/<region小写>_<tag>_items.json`。
- **同表达式 + 不同设置档是允许且必要的**（靠 §4 的去重键支撑）。
- **不要留「同表达式+同设置档」的重复行**（白占槽位；`check_wave_fields.py` 会报出来）。

## 7. 扫完一轮后的判据（避免无限续跑）

### 7.0 ★★★ 机制层穷尽判据（**何时该换 region，而不是继续扫数据集**）

**问的不是「还剩几个数据集没扫」，而是「还有哪类机制没被证伪」。**
数据集可以有很多个，但**机制类型是有限的**。把已证死的机制列出来，
如果**主要机制都被证伪**，继续扫剩余数据集的边际期望≈0。

**EUR 实测（2026-10-05，79 波：历史 62 + 当日 17）**：

| # | 机制 | 死因 | 证据强度 |
|---|---|---|---|
| 1 | 信用风险绝对水平/距离/评级 | 机制层无预测力 | ★★ 2 个独立数据源（违约距离 **0.22** / StarMine **0.68**）|
| 2 | 新闻情绪（4 个数据集）| 无信号 | ★ 最高 0.61 |
| 3 | 季节 / 市场级变量 | 横截面退化为常数 | ★ `group_zscore` 也不退化（§2.1）|
| 4 | 分析师预期（低覆盖源）| 字段覆盖 0.32 | ★ 字段级覆盖实测（§1.1）|
| 5 | 投资 idea / 目标价 | 反向但强度不足 | ★★ 跨源精确对称（§1.0）|
| 6 | 并购概率 | 反向但强度不足 | ★★ 跨源精确对称 |
| 7 | **内部人交易**（Jensen / Lakonishok 经典）| **无信息** | ★ **标准构造 S=0.04**（不是弱，是没有）|
| ★ | CASSIE `ocf_currliab` 变化量 | **唯一存活** | S1.94 / prod 0.50，但 2700 组合已扫尽 |

⇒ **7 类主流机制全灭 + 1 类存活且扫尽 = 机制层穷尽**。
剩余 65 个「合格」数据集的**边际期望 ≈ 0.3 条**。

⚠ **内部人交易这一条尤其值得记住**：它是学术上最稳健的横截面信号之一
（Lakonishok & Lee 2001 的经典结论），在 EUR 上 S=0.04。
⇒ **「学术上有效」不等于「这个 region 有效」**。别因为文献支持就跳过实测，
也别因为一个 region 失败就断定机制无效（**要多个 region 交叉才能否定机制**）。

**报告「该 region 穷尽」时必须附这张表** —— 只说"扫完了"没有信息量。


**先算期望收益，再决定发不发**：
设计完波次、发批前**必须先算一条「该波能改善哪个指标、幅度多少」**。
实测反例：我设计完 M1 族的 decay 细网格才发现在算曲线时，
**2Y 在所有 decay 档都是 0.96–0.99（距 1.58 差 0.61）⇒ 细网格救不了 ⇒ 该波期望收益 ≈ 0**，
于是删掉了整批 items。**算不出正收益就别发。**

**判死判据（结构层）**：换 ≥5 种结构（字段 / 算子几何 / 设置档 / 分组轴）后该指标纹丝不动。
**注意区分**：
- **有梯度**（同族不同字段/设置档指标有单调差异）⇒ **活墙**，继续扫杠杆；
- **无梯度 + 多轴全灭** ⇒ **死墙**，整理证据链上报裁决，别再磨。

**⚠ 报告「判死」时必须附证据链**：扫过哪些轴、每轴的最优值、与阈值的差距。
**证据链不完整时不要宣称"无计可施"**——那会让真正有价值的族被误杀。

### 7.0.1 ★★★★★ 判死前的**三个数字自检**（2026-10-31 GBR 事故后新增，最易犯）

「换 ≥5 种结构」管的是**结构轴广度**，但**样本量与字段覆盖**是另一条独立的门。缺了它，就会把「没测够」当成「测过了」，**永久封掉一片搜索空间**。

写判死结论前，必须报出这三个数字：

| # | 数字 | 门槛 | 不达标时的正确表述 |
|---|---|---|---|
| ① | **探针数** | **≥8** | `PROBE-KILLED`（不可信，进待补课清单）|
| ② | **字段覆盖率** | **≥50%** 或「已覆盖全部机制族」 | 「仅在 N/M 字段上无信号」——**不得称「数据集判死」** |
| ③ | **结构数** | **≥2**（双结构是保底，≥5 是判死门槛）| 「单结构未出信号」——未测结构 B 就没资格判死 |

**★★ 「批宽度」≠「样本量」**：用户级并发限制（如「每批 ≤2 条」）只约束**单批宽度**。正确适配是**多批串接**（2 条 × 4 批 = 8 探针），**不是缩批后照样下结论**。本区事故：`other250` 12 字段只看 2 个（17%）就记「判死」，同轮另有 5 个数据集同样 2 探针即封盘 ⇒ 一起汇总成「OTHER 塔 13 数据集全灭」这个**多数不可信的结论**。

**★★★ 栖息地缺失是第四种死法（独立于前面三条）**：同一表达式在 USA `ILLIQUID_MINVOL1M` **S 2.89** / GBR `TOP700` **S 0.95**（差 3.0×），根因是「信号住非流动小票」。**`get_platform_setting_options()` 查一次 universe 全集就能在 0 仿真成本下判死**——这类判死要单独打 `STRUCTURAL-DEAD` 标签并注明「仅本区限定，不外推」。

**台账写法**：「判死」三个字单独成行 = 无效台账。每行必须带 `探针数 / 字段覆盖率 / 结构数 / 最好读数 / 标签`。

---

## 8. ★★★ SA（SuperAlpha）发批/提交前自查 —— 「区域资格」是最前置的一刀（2026-10-06 实证）

**适用**：要建 / 提交 SuperAlpha，或要把 SA 候选写进盘点报告时。

### 8.0 ★★★ 第一道永远是「区域资格」，不是信号质量

SuperAlpha 只能从**你已提交（ACTIVE）的 REGULAR 组件池**里选，
**硬前置 = 该区 eligible ACTIVE 组件 ≥ 10 颗**。低于 10 ⇒ **SA 根本不能建**
（不是信号问题，是组件池不够）⇒ 白扫、白排推荐序。

```python
# 数据源：results/sa_candidates_<ts>.json（由 probe_sa_candidates.py 产出）
d["min_eligible"]                               # = 10
d["regions"][R]["eligible_active_submitted"]    # 逐区组件池大小
# GO: >=10 ；BLOCKED: <10（SA 面结构性关闭）
```
**2026-10-06 实测**：GO = USA 37 ｜ IND 27 ｜ KOR 24 ｜ MEA 19 ｜ GBR 11 ｜ GLB 10；
BLOCKED = ASI 8 ｜ HKG 6 ｜ DEU 6 ｜ EUR 4。
⇒ ★ **「EUR 还有新塔没点亮」这类 RA 判断对 SA 无效**——EUR 连 SA 都建不了。
⇒ 报告里这一条必须放 SA 段**最前面**，不能塞进备注。

### 8.1 ★★ SA 的「相关闸」必须单独实测，且**不能从 IS 推断**

`probe_sa_candidates` 的 `unsubmitted_candidates` 里 **`prod` 恒为 None**
⇒ 必须跑 `tools/probe_sa_unsubmitted.py`（纯 GET、默认增量、⛔禁 `--all`）实测 prod/self。

**实测反例（IS 对 prod 无预测力，在 SA 上同样成立）**：
KOR IS 最低的两颗（3.96 / 3.74）反而撞墙；**IND 13 颗候选 → 13/13 撞墙**，
连 IS S 6.13 的 `LLZnG5ZM` 也 prod 0.798 / self 0.798 ⇒ **整个 IND SA 池判死**。
⇒ 纪律：**IS sharpe 高 ≠ 可交**；一区一测，不得把「IS 排名」当推荐序先验。

### 8.2 ★★ SA 的「同源自锁」比 RA 更凶（同批生成 = 高危）

SA 的 self 池 = **你已提交的全部 alpha**。同一天同批生成的 SA 候选天然高度相似
（看 `dateCreated` 是否聚集在同一小段时间 + `selectionLimit` 是否相同），
**提 1–2 颗后，其余候选的 self 会被立刻抬高**。
⇒ 纪律：**每区只留 1–2 颗代表先提，提完立刻重测其余 self**；不要按 IS 排名一口气排 10 颗。

### 8.3 ★ 四个口径别记错

| 项 | 正确口径 |
|---|---|
| **余量（报告列）** | **0.7 − prod_max**（与 RA 同口径 = 距闸线的距离；SA 的 prod 已 ≥ self，故 max 即 prod）。⚠ 别用 `1 − prod`——1 不是闸线，无判别意义 |
| **提交门槛** | 与 regular alpha **逐条相同**，唯一差异 = **turnover 2%–40%** |
| **提交配额** | **REGULAR 4 颗/ET 日 ＋ SUPER 1 颗/ET 日**（00:00 ET 重置、全账户不分区域）；实况 `python tools/quota_status.py`。⚠ 不是「1 次/天/区」 |
| **塔规则** | **不适用**（SA 出自已 ACTIVE 组件池、不点亮新塔）；SA 的「塔」维换成「**换区**」维 |
| **Theme** | **Super Alpha Themes**（与 Dataset / Region Themes 并列，SA 专属） |

> 完整 SA 报告四步（区域资格 → 候选相关闸 → 推荐序表 → 各 base 维度落法表）
> 见自动化大纲 `.workbuddy/memory/automations/b975c750-.../memory.md` §六。
