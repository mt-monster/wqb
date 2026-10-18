# DEU 字段名「是否变化」四维验证报告

> 生成时间：2026-10-10T14:26:12 ｜ region=DEU ｜ 本地库=wqb.db
> categories：MODEL(8173), ANALYST(4312), OTHER(3921), PV(2877), FUNDAMENTAL(2146), NEWS(523), SENTIMENT(276), INSTITUTIONS(66), RISK(52), INSIDERS(42), EARNINGS(25), SHORTINTEREST(25), OPTION(22), SOCIALMEDIA(19), MACRO(13), IMBALANCE(2), (none)(0)

## T1 本地目录内部一致性

- DEU 数据集总数：193
- 平台声明字段总数（Σ dataset.field_count）：22,504
- 本地实际字段行总数：22,494
- **整库缺失数据集（declared>0 但 local=0）：9 个** → 这些数据集的字段本地一条都没存
- 孤儿/超量数据集（local > declared）：14 个
- 部分缺失数据集（0<local<declared）：14 个

缺失数据集清单（declared>0 & local=0，按 declared 降序）：
  - `mmp_nlp_sentiment` 声明 72 ｜类别 OTHER
  - `model50` 声明 52 ｜类别 MODEL
  - `analyst45` 声明 38 ｜类别 ANALYST
  - `news48` 声明 22 ｜类别 NEWS
  - `news46` 声明 19 ｜类别 NEWS
  - `risk59` 声明 16 ｜类别 RISK
  - `chart_return_model` 声明 8 ｜类别 PV
  - `model242` 声明 5 ｜类别 MODEL
  - `univ1` 声明 1 ｜类别 PV

### 按 category 汇总（声明 vs 实际 vs verified=-1）
category          数据集      声明字段      本地字段      缺口 verified=-1    缺失ds
MODEL              51      8084      8173     -89        1842       2
ANALYST            19      4343      4312      31           0       1
OTHER              43      3978      3921      57         333       1
PV                 18      2885      2877       8           0       2
FUNDAMENTAL        13      2146      2146       0          48       0
NEWS               19       531       523       8           0       2
SENTIMENT           3       276       276       0           0       0
INSTITUTIONS        5        57        66      -9           0       0
RISK                6        68        52      16           0       1
INSIDERS            2        42        42       0           0       0
EARNINGS            2        25        25       0           0       0
SHORTINTEREST       1        25        25       0           0       0
OPTION              1        22        22       0           0       0
SOCIALMEDIA         2         7        19     -12           0       0
MACRO               1        13        13       0           0       0
IMBALANCE           1         2         2       0           0       0
(none)              6         0         0       0           0       0

### DEU 字段命名族分布（family_of：去数字/期限后缀）
  - `oth#_customer_n#v_p#_q#_w#_pca_fact#_cluster_#` ：180 个字段
  - `oth#_partner_n#v_p#_q#_w#_pca_fact#_cluster_#` ：180 个字段
  - `oth#_relation_n#v_p#_q#_w#_pca_fact#_cluster_#` ：180 个字段
  - `oth#_competitor_n#v_p#_q#_w#_pca_fact#_cluster_#` ：180 个字段
  - `tm_#_r#_r#_r#_rh_glb_d#_r#_q#_p#` ：168 个字段
  - `tm_#_r#_r#_r#_rh_ah#_glb_d#_r#_q#_p#` ：126 个字段
  - `fnd#_asset_#_#` ：98 个字段
  - `oth#_relation_n#v_p#_q#_w#_kmeans_cluster_#` ：60 个字段
  - `oth#_competitor_n#v_p#_q#_w#_pca_fact#_value` ：60 个字段
  - `oth#_customer_n#v_p#_q#_w#_pca_fact#_value` ：60 个字段
  - `oth#_customer_n#v_p#_q#_w#_kmeans_cluster_#` ：60 个字段
  - `oth#_competitor_n#v_p#_q#_w#_kmeans_cluster_#` ：60 个字段
  - `oth#_relation_n#v_p#_q#_w#_pca_fact#_value` ：60 个字段
  - `oth#_partner_n#v_p#_q#_w#_pca_fact#_value` ：60 个字段
  - `oth#_partner_n#v_p#_q#_w#_kmeans_cluster_#` ：60 个字段
  - `tm_#_r#_r#_r#_rh_glb_d#_r#_q#` ：60 个字段
  - `pv#_ebi_indicator_#_feature#` ：52 个字段
  - `pv#_sal_indicator_#_feature#` ：52 个字段
  - `pv#_roe_indicator_#_feature#` ：52 个字段
  - `pv#_bps_indicator_#_feature#` ：52 个字段
  - `pv#_nav_indicator_#_feature#` ：52 个字段
  - `pv#_pre_indicator_#_feature#` ：52 个字段
  - `pv#_gps_indicator_#_feature#` ：52 个字段
  - `pv#_eps_indicator_#_feature#` ：52 个字段
  - `pv#_net_indicator_#_feature#` ：52 个字段
  - （共 15066 个不同命名族）

## T2 时间点快照对比（current vs 备份）

### bak_1005 → current（DEU 字段名集合对比）
- 新增字段（平台有、备份无）：**0**
- 删除字段（备份有、平台/本地无）：**0**
- 维持不变：22,494
- 发生变化的数据集数：0

变化最大的数据集（按 |新增|+|删除| 降序，前 25）：

### bak_1006 → current（DEU 字段名集合对比）
- 新增字段（平台有、备份无）：**0**
- 删除字段（备份有、平台/本地无）：**0**
- 维持不变：22,494
- 发生变化的数据集数：0

变化最大的数据集（按 |新增|+|删除| 降序，前 25）：

## T3 跨 region 一致性（同名 category）

category           DEU字段       其它区并集      交集  Jaccard  说明
> 注：Jaccard=交集/并集，因其它区并集远大于 DEU，Jaccard 偏低不代表 DEU 字段名独特；
> 关键看「交集/DEU」——DEU 字段名有多大比例也存在于其它区。
MODEL               8172       40728    7805    0.190  DEU名95%+也存在于其它区（高度共享）
ANALYST             4312       22279    4275    0.192  DEU名95%+也存在于其它区（高度共享）
OTHER               3921       14241    3917    0.275  DEU名95%+也存在于其它区（高度共享）
PV                  2877       17229    2848    0.165  DEU名95%+也存在于其它区（高度共享）
FUNDAMENTAL         2146       19320    1870    0.095  DEU名95%+也存在于其它区（高度共享）
NEWS                 523        3201     523    0.163  DEU名95%+也存在于其它区（高度共享）
SENTIMENT            276        1984     276    0.139  DEU名95%+也存在于其它区（高度共享）
INSTITUTIONS          66         123      66    0.537  DEU名95%+也存在于其它区（高度共享）
RISK                  52        1657      48    0.029  DEU名95%+也存在于其它区（高度共享）
INSIDERS              42         263      42    0.160  DEU名95%+也存在于其它区（高度共享）
EARNINGS              25         730      25    0.034  DEU名95%+也存在于其它区（高度共享）
SHORTINTEREST         25         242      25    0.103  DEU名95%+也存在于其它区（高度共享）
OPTION                22         662      22    0.033  DEU名95%+也存在于其它区（高度共享）
SOCIALMEDIA           19         296       7    0.023  DEU名仅部分共享
MACRO                 13         180      13    0.072  DEU名95%+也存在于其它区（高度共享）
IMBALANCE              2           2       2    1.000  DEU名95%+也存在于其它区（高度共享）
(none)                 0           0       0    0.000  DEU名仅部分共享

## T4 本地 vs 平台实时（get_datafields 实时比对）

### 方法
- 对 25 个目标数据集（每 category 最大有数据数据集 16 个 ＋ 本地「声明>0 但本地=0」的 9 个缺失数据集）逐一调平台
  `get_datafields(region='DEU', universe='TOP500', delay=1, filter_sharpe=False, search=<数据集名>)`。
- 平台返回的字段名集合与本地基准 `deu_field_baseline_20261010.json` 逐名 diff（改名 / 删除 / 新增）。
- 原始字段名证据存于 `deu_t4_platform_20261010.json`；diff 脚本 `reports/diff_t4_20261010.py`。
- 工具约束：① 非定向 dump 上限 **100 字段**（大集被截断）；② search-by-name 对歧义/大型数据集**可能未精确命中目标数据集**（见下「作用域歧义」）。

### 结论速览
- **9 个「缺失」数据集：平台 search 两次确认返回 0 字段** → 这些数据集已从平台下架（或 search 不可见）。本地 catalog 仍声明它们有字段，属 catalog 完整性问题，**非改名**。
- **9 个 FULL 数据集（平台返回数 ≤100 且未截断）逐名比对：0 改名、0 删除** → 字段名与本地 100% 一致。
- **3 个截断样本（news23 / other455 / pv20）的 100 字段样本：0 改名** → 样本内未发现改名。
- **4 个数据集因 search 作用域歧义无法可靠逐名验证**：sentiment33、fundamental72、analyst_consensus、model219（见下）。

### 逐数据集明细
dataset | category | 状态 | 本地 | 平台 | 改名/新增 | 删除/完整移除 | 可靠性
---|---|---|---|---|---|---|---
mmp_nlp_sentiment | OTHER | PLATFORM_EMPTY | 0 | 0 | — | — | 下架
model242 | MODEL | PLATFORM_EMPTY | 0 | 0 | — | — | 下架
model50 | MODEL | PLATFORM_EMPTY | 0 | 0 | — | — | 下架
analyst45 | ANALYST | PLATFORM_EMPTY | 0 | 0 | — | — | 下架
chart_return_model | PV | PLATFORM_EMPTY | 0 | 0 | — | — | 下架
univ1 | PV | PLATFORM_EMPTY | 0 | 0 | — | — | 下架
news46 | NEWS | PLATFORM_EMPTY | 0 | 0 | — | — | 下架
news48 | NEWS | PLATFORM_EMPTY | 0 | 0 | — | — | 下架
risk59 | RISK | PLATFORM_EMPTY | 0 | 0 | — | — | 下架
macro27 | MACRO | FULL | 13 | 13 | 0 | 0 | ✅ 可靠
option1 | OPTION | FULL | 22 | 22 | 0 | 0 | ✅ 可靠
earnings6 | EARNINGS | FULL | 18 | 18 | 0 | 0 | ✅ 可靠
imbalance5 | IMBALANCE | FULL | 2 | 2 | 0 | 0 | ✅ 可靠
insider_agg_matrix | INSIDERS | FULL | 34 | 34 | 0 | 0 | ✅ 可靠
institutions25 | INSTITUTIONS | FULL | 24 | 24 | 0 | 0 | ✅ 可靠
shortinterest3 | SHORTINTEREST | FULL | 25 | 25 | 0 | 0 | ✅ 可靠
risk72 | RISK | FULL | 31 | 31 | 0 | 0 | ✅ 可靠
socialmedia12 | SOCIALMEDIA | FULL | 18 | 18 | 0 | 0 | ✅ 可靠
sentiment33 | SENTIMENT | FULL(但错位) | 255 | 18 | (18) | (255) | ⚠ 作用域错位，无效
news23 | NEWS | TRUNCATED_100 | 116 | 100 | 样本内 0 | N/A | ✅ 样本可靠
other455 | OTHER | TRUNCATED_100 | 1500 | 100 | 样本内 0 | N/A | ✅ 样本可靠
pv20 | PV | TRUNCATED_100 | 681 | 100 | 样本内 0 | N/A | ✅ 样本可靠
fundamental72 | FUNDAMENTAL | TRUNCATED_100(错位) | 1031 | 100 | (80) | N/A | ⚠ 作用域错位
analyst_consensus | ANALYST | TRUNCATED_100(错位) | 1972 | 100 | 样本内 0 | N/A | ⚠ 作用域错位
model219 | MODEL | SEARCH_AMBIGUOUS_ZERO | 1172 | 0 | — | — | ⚠ 不可靠

> 说明：FULL = 平台返回数 ≤100 即全量；TRUNCATED = 工具 100 上限截断；括号内数字为作用域错位导致的伪差，不计为真实改名。

### search 作用域歧义（重要限制）
- `search="sentiment33"` 返回的 18 个字段（sentiment_* / scl12_* / entity_*）与 `search="socialmedia12"` 返回的**集合完全相同**
  → 说明 search 命中了 socialmedia12（或同名语义数据集），并非本地 sentiment33 的 255 个字段。本地 sentiment33 的 255 字段未能验证。
- `search="fundamental72"` 与 `search="analyst_consensus"` 返回了**几乎完全相同**的 estimate_count_* 字段集
  → 两者 search 命中了同一分析师一致预期数据集，至少其一作用域错位。fundamental72 本地 1031 / analyst_consensus 本地 1972 字段均未能可靠验证。
- `search="model219"` 本回合返回 0（上一回合曾返回 71 个「model38 类」字段）
  → 大型 MODEL 数据集 search 不可靠，需改用平台 **dataset_id** 精确比对。
- 工具非定向 dump 上限 100 字段，使 other455(1500)/analyst_consensus(1972)/fundamental72(1031)/pv20(681) 等大集无法一次性全量验证。

### 与 pattern_scores 事故的关系
- 本回合在**可可靠验证**的数据集上**未复现**「本地名与平台名漂移导致整批 ERROR」的事故（9 个 FULL 集 0 改名、3 个截断样本 0 改名）。
- 但 **9 个「平台已下架」数据集** ＋ **4 个作用域歧义数据集**，正是发批时潜在的「用本地名 → 平台查无 → ERROR」陷阱。
- 建议：发批前对目标字段一律以平台 dataset_id 实拉字段名（而非本地名），并排除上述 9 个已下架数据集。

### 完整覆盖建议
- 当前 T4 受远程 HTTP MCP（无本地凭据、无法脚本化 193 次循环）限制，只能抽样验证。
- 如需对 DEU 全部 193 数据集、每个字段名做全量实时比对，需：
  1. 取得平台 API 凭据后脚本化，使用 **dataset_id**（非 search）避免作用域错位；
  2. 分页拉全（绕过 100 上限）；
  3. 以 `get_datafields` 返回的实时字段名作为发批唯一权威，本地 catalog 仅作参考。

---

## 总体结论（四维验证）

1. **字段名本身是否变化？** 在可可靠验证的范围（9 个 FULL 数据集 ＋ 3 个大集的 100 字段样本）内，**DEU 字段名与平台实时一致，无改名、无删除** → 字段名是稳定的。
2. **跨时间点是否变化？** T2：current vs 两个备份（10-05 / 10-06）**0 增 0 删 22,494 字段零 churn** → 近期本地目录稳定。
3. **跨 region 是否一致？** T3：DEU 字段名 95%+ 也存在于其它区 → 高度共享，字段名非 region 专属。
4. **本地 catalog 完整性？** T1：193 数据集中 **9 个整库缺失**（平台已下架）、14 个孤儿、14 个部分缺失、2,223 个 verified=-1 → catalog 有完整性问题，**但这属于「缺字段/数据集下架」，而非「改名」**。
5. **最大风险点**：不是「字段改名」，而是「本地 catalog 还声明着平台已下架的数据集（9 个）与字段数严重漂移的数据集（model219 等）」。发批时若用这些本地名，会触发查无字段的 ERROR（同 pattern_scores 事故机理）。

> 一句话：**DEU 字段名本身没有在变（稳定）；会变/已变的是 catalog 的「数据集下架」与「字段数漂移」，需要用平台 dataset_id 实拉字段名来兜底防错。**

---

### 产物清单
- `output_report/deu_field_name_verification_20261010.md`（本报告，T1–T4 ＋ 总体结论）
- `output_report/deu_field_baseline_20261010.json`（本地字段名基准，193 数据集）
- `output_report/deu_t4_targets_20261010.json`（T4 目标数据集清单；原名 `deu_t4_targets.json`，2026-10-10 第四轮治理按 §8.13 补日期后缀改名）
- `output_report/deu_t4_platform_20261010.json`（T4 平台实时字段名原始证据）
- `reports/diff_t4_20261010.py`（T4 名称级 diff 脚本；原在 `output_report/`，按 S16 规则⑤「产物目录不得混入脚本」迁出，证据语义不变）

### T4 已执行：本地 catalog 同步（2026-10-10 15:18）
- 备份：`data/wqb.db.bak_before_deu_t4_update_20261010_151842`
- 已对 DEU（region_id=10）下 **9 个平台已下架数据集** 在 `datasets` 表执行同步：
  `mmp_nlp_sentiment, model242, model50, analyst45, chart_return_model, univ1, news46, news48, risk59`
  → `field_count` 由原声明值（72/5/52/38/8/1/19/22/16）统一置 **0**，`status` 置 **`platform_empty`**，`updated_at` 刷新为当前时间。
- 这 9 个数据集本地 `fields` 表本就 0 行（T1 的「缺失」），故无需删字段行；仅校正声明计数与状态，使 catalog 与平台实时一致。
- 未改动其余 184 个 DEU 数据集（含 4 个作用域歧义集 sentiment33/fundamental72/analyst_consensus/model219，待 dataset_id 精确复核后再议）。
- 回滚方式：以备份库覆盖 `data/wqb.db` 即可。

---

### 扩展同步：GBR / KOR / EUR（2026-10-10 15:35）
按用户指令「先做 GBR, IND, GLB, KOR, EUR」，将 DEU 同款「平台已下架数据集同步」扩展到这 5 个 region。同步口径严格对齐 DEU：**仅 sync phantom 类**（声明 `field_count>0` 但本地 `fields` 表 0 行、且平台 `search` 实拉返回 `count=0` 确证下架），不含 orphan / partial 漂移。

**平台实拉验证**（region + `search`，TOP500 / delay=1 / filter_sharpe=False / dataset_id=null）：
- **GBR（region_id=7）**：14 个疑似下架集全部返回 `{"results":[],"count":0}` → 确证下架。列表：`chart_return_model, fundamental31, ml_factor_proj, mmp_nlp_sentiment, model193, model219, model230, model242, model50, multi_horizon_alpha, news46, other532, risk59, univ1`。（注：other532 首轮 `offset=0` 瞬态分页报错 `failed after 6 attempts`，重试后正常返回 0。）
- **KOR（region_id=2）**：`pv1` 平台返回 `count=0` → 确证下架（本地声明 24 字段、alpha_count=67041）。
- **EUR（region_id=6）**：`chart_return_model`、`other459` 平台均返回 `count=0` → 确证下架。
- **IND（region_id=5）**：全库漂移扫描 0 个 phantom → 无需同步，已干净。
- **GLB（region_id=8）**：全库漂移扫描 0 个 phantom → 无需同步，已干净。

**执行同步（2026-10-10 15:35）**：
- 备份：`data/wqb.db.bak_before_gbr_kor_eur_sync_20261010_153512`。备份前先 `PRAGMA wal_checkpoint(TRUNCATE)` 将 WAL 合并进主库（合并后 WAL=0 字节，备份含 DEU 同步结果，单一文件即可还原），备份大小 424,734,720 字节。
- 语句：`UPDATE datasets SET field_count=0, status='platform_empty', updated_at=CURRENT_TIMESTAMP WHERE region_id IN (7,2,6) AND name IN (...)`。
- 命中行数：GBR 14 / KOR 1 / EUR 2 = **合计 17 行**，`rowcount` 与预期逐一一致，`commit` 后复核 `status='platform_empty'` 全部就位。

**同步后漂移复核**（phantom = 声明>0 且本地 `fields`=0）：
- GBR phantom 14→0、KOR 1→0、EUR 2→0；IND / GLB 维持 0。
- 全库 phantom 由 132 降至 **115**（剩余 115 全在 ASI=113 与 USA=2，**不在本次范围**）。
- 仍存在的非 phantom 漂移（**不在本次范围**，与 DEU 同口径只修「下架」类）：DEU orphan 14；EUR orphan 19 / partial 3；GBR orphan 14 / partial 10；USA orphan 60 / partial 4 / phantom 2；ASI phantom 113。

**回滚方式**：以 `data/wqb.db.bak_before_gbr_kor_eur_sync_20261010_153512` 覆盖 `data/wqb.db` 即可（备份已含 WAL 合并，单文件还原，无需附带 -wal/-shm）。

### 扩展同步：USA（2026-10-10 15:42）
按用户指令「把 USA 的也做了」，将同款「平台已下架数据集同步」补到 USA。

**定位 phantom**：`datasets` 中 `region_id=1 AND field_count>0` 且本地 `fields` 表 0 行的数据集共 **2 个**：`dl_equity_signal`（声明 1，alpha_count=13）、`other476`（声明 125，alpha_count=1030）。

**平台实拉验证**（region=USA，universe=TOP3000 / delay=1 / filter_sharpe=False / dataset_id=null）：
- `dl_equity_signal` 平台返回 `{"results":[],"count":0}` → 确证下架。
- `other476` 平台返回 `{"results":[],"count":0}` → 确证下架。

**执行同步（2026-10-10 15:42）**：
- 备份：`data/wqb.db.bak_before_usa_sync_20261010_154200`（先 `wal_checkpoint(TRUNCATE)` 合并 WAL，单一文件 425,041,920 字节，含此前全部同步结果）。
- 语句：`UPDATE datasets SET field_count=0, status='platform_empty', updated_at=CURRENT_TIMESTAMP WHERE region_id=1 AND name IN ('dl_equity_signal','other476')`。
- 命中 **2 行**，`rowcount=2`，复核 `status='platform_empty'` 全部就位。

**同步后漂移复核**：USA phantom 2→0；全库 phantom 由 115 降至 **113（剩余 113 全在 ASI，不在本次范围）**。仍存在的非 phantom 漂移（不在本次范围）：DEU orphan 14；EUR orphan 19 / partial 3；GBR orphan 14 / partial 10；USA orphan 60 / partial 4；ASI phantom 113。

**回滚方式**：以 `data/wqb.db.bak_before_usa_sync_20261010_154200` 覆盖 `data/wqb.db` 即可（单文件，无需 -wal/-shm）。

> 至此，用户点名的 DEU / GBR / KOR / EUR / IND / GLB / USA 共 7 个 region 的「平台已下架」类同步全部完成。仅剩 ASI（113 个 phantom）未处理，且 ASI 不在本次挖矿范围（仅 DEU）。