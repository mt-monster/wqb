# DEU 战役报告 — sentiment27 / sentiment7 / sentiment33

> 区域 / 宇宙 / Delay：**DEU / TOP500 / D1**｜目标塔：**DEU·D1·SENTIMENT**
> 战役目录：`tracking/DEU/campaign_deu_sentiment27_sentiment7_sentiment33/`
> 报告日期：2026-11-18｜性质：**产物型报告（不含数据库写入、不含任何提交动作）**
>
> **证据标注约定**：`[实跑]` = 本次会话内实际执行命令 / 调用 MCP 得到的结果；`[材料]` = 本次 ask 随附的
> CHECKS / PROFILES / PLANS / HARVEST / RESULTS / CORR / WAVES / STOP / SUBMIT 数据块；`[档案]` = 仓库内既有文件，
> 注明 `path:line`。**凡未实跑的检查一律标「未跑」，不写成通过。**

---

## 0. 一句话结论（先给判定，再给证据）

1. **三个数据集都属 SENTIMENT 单塔，塔未点亮（DEU·D1·sentiment = 1 颗 < 3）**，三集倍率同为 **1.8**（实读），
   本战役把它们按 ATOM 单集分别开波，不混腿、不跨集。
2. **RESULTS 实列 13 条读数全部未过闸**：最好一条 S **1.02**（A7-01），
   比 DEU 内部线 1.58 差 **35%**；`ts_ir` 结构维（波 2）在两个 dataset 上反向崩塌（A7-04 1.02→0.14、A27-05 0.78→0.22），
   波 2 最好只到 **0.81**。**第 3 波按停止规则不开口**——判定成立（`[材料]` STOP + `[实跑]` 复算）。
3. **零配额收割 3 颗，对本战役有效产出 = 0**：2 颗在 **EUR**（不进 DEU 塔），唯一那颗 DEU 的 `QPveY7Kg`
   虽然 S 2.03 / F 1.61，但**近十年闸不过**（2014–2018 五年 longCount=0，2020 年 pnl 为负，`[实跑]`），
   另一颗 EUR 件用了 `add()` 混两腿（违反 §7.7 铁律；`usable:true` 只代表**按平台线 0.70** 的 prod/self 数值过线，
   按仓库内部严线 prod 0.65 / self 0.50 它也不合格）。
4. **提交链：0 颗候选走完五道闸。** 波内最强臂 `A1x7E5KR` 由 `submit_verdict` 判 **BLOCKED**（4 个 RA fail + 1 个 PPA fail）；
   收割件 `QPveY7Kg` 由本次实跑 `submit_verdict` 判 **UNVERIFIABLE**（0 RA fail，但该结论**不是放行**），且被我实跑的
   逐年读数判死在第 ③ 闸。**本次未做任何提交动作。**
5. **口径告警（两条，都会影响整改动作）**：
   ① `LOW_SUB_UNIVERSE_SHARPE` 是**相对判据**，不是常数线——实读 5 条臂的 `checks.fail.limit` 分别是
   0.48 / 0.38 / 0.37 / 0.18 / 0.03，与该臂 S 之比稳定在 **0.43–0.49**（拟合 ≈0.475×S，见 §5.3）。
   ⇒ 本地 `tracking/DEU/config/thresholds.json` 的 `sub_universe_sharpe_min = 1.0` **不能"对齐 0.48"**，
   两者不是同一量纲；本报告一律以平台逐条 limit 为准。
   ② 本地 `src/wqb/config.py:531` 的内部严线含 `self_corr_max = 0.50`（不止 prod 0.65），
   按它 `WjOAJWxd` self 0.6446、`78LKlOw1` self 0.5368 **都超线**（原报告按 0.70 平台线写成"过线/贴线"是错的）。

---

## 0.1 本次实跑清单（可复现）

| # | 命令 / 调用 | 结果 |
|---|---|---|
| 1 | `for ds in sentiment27 sentiment7 sentiment33; do python tools/gates/field_profile_completeness_gate.py --profile tracking/DEU/reference/datasets/$ds.md; done` | 三份全 **exit 0 / PASS**（18/18、3/3、255/255 带读数）。⚠ 该闸 `--profile` **只收单值**（`--help` 实读 `--profile PROFILE`），写成 `--profile a b c` 会被 argparse 只保留最后一份、只验 sentiment33 —— 不能那样写 |
| 2 | `mcp__wq-brain-http__get_pyramid_alphas()` | `DEU.D1.sentiment = 1`（D0 全 0）→ 塔未点亮 |
| 3 | `mcp__wq-brain-http__get_pyramid_multipliers()` | `DEU.D1.sentiment = 1.8` |
| 4 | `mcp__wq-brain-http__get_alpha_details(WjOAJWxd / 78LKlOw1 / QPveY7Kg)` | 三件收割件的 settings / metrics / checks / pyramids 全文 |
| 4b | `mcp__wq-brain-http__get_alpha_details(A1x7E5KR / VkN3L5rY / j2arOJEj / ZYaKN9L0 / vRAvPb0r)` | 5 条臂的 `metrics.returns` 与 `checks.fail` 全文（SU 的相对 limit、CLUSTER_TEST warning 由此实读） |
| 5 | `mcp__wq-brain-http__submit_verdict(QPveY7Kg)` | `UNVERIFIABLE`（exit 10），`failed_ra = 0`，`robustness = CONDITIONAL` |
| 6 | `mcp__wq-brain-http__get_alpha_yearly_stats(QPveY7Kg / WjOAJWxd)` | 两件均 **2014–2018 零持仓**；`QPveY7Kg` 2020 年 pnl −7,823 |
| 6b | `python -I -c "import sqlite3; con=sqlite3.connect('file:data/wqb.db?mode=ro',uri=True); …"`（只读 URI 连接） | `stage='OS'` **25**、其中 `status='ACTIVE'` **13**（COMPLETE 6 / UNSUBMITTED 6）；`alpha_pyramids` DEU **3 行**（全 UNSUBMITTED） |
| 7 | 档案核对：`tracking/DEU/s1_sentiment7_wave1_template_pool.md`、`s1_sentiment27_wave1_template_pool.md`、`atom_orthogonal/DEATH_AUDIT_20261110.md`、`atom_orthogonal/DATASET_DISPOSITION_MAP_20261111.md`、`atom_orthogonal/SENTIMENT33_FULL_VERDICT_20261111.md`、`tracking/DEU/reports/deu_campaign_20261030.md:2704`、`config/thresholds.json`、`src/wqb/config.py` | 逐条引用见下文 |

**未跑（明确声明）**：本报告的 13 条回测读数、prod/self 相关性数值、`A1x7E5KR` 的五道闸体检均来自 `[材料]`，
**本次未重跑回测、未重跑 `check_correlation`、未重跑 `A1x7E5KR` 的 `submit_verdict`**（只对 `QPveY7Kg` 重跑了
`submit_verdict` 与 `get_alpha_yearly_stats`）。`wave_gate` / `pipeline` 未在本轮运行。

---

## 1. 数据集选定与塔位校验

### 1.1 三集身份卡（平台实读，`[材料]` CHECKS + `[档案]` 画像首行）

| 数据集 | 平台 name | category | coverage | 字段数 | alphaCount | 倍率 | 塔内已有 |
|---|---|---|---:|---:|---:|---:|---:|
| `sentiment27` | **Website Popularity Rankings** | sentiment | 0.9038 | 18 | 390 | 1.8 | 1 |
| `sentiment7` | **Webpage Views Data** | sentiment | 0.7418 | 3 | 114 | 1.8 | 1 |
| `sentiment33` | （文档槽 ×5 的 NLP 情绪集） | sentiment | **0.3221** | 255 | 67 | 1.8 | 1 |

> ⚠ **"塔内已有"列的三行是同一个数**：它来自塔级计数 `DEU.D1.sentiment = 1`，**不代表"每个数据集各有一颗"**。
> 该 1 颗的身份未核实（本地 `alpha_pyramids` 的 DEU 3 行全为 UNSUBMITTED，其中落 sentiment 塔的是 `QPveY7Kg`；
> 但平台塔计数是否计入它，本轮没有取证）。

⚠ **语义更正（两张档案都写了，容易被名字骗）**：
- `sentiment27` **不是新闻情绪**，是 Tranco 域名排名 / 网络关注度（`tracking/DEU/reference/datasets/sentiment27.md:7`）；
- `sentiment7` **不是新闻情绪**，是维基百科页面浏览量（`.../sentiment7.md:7`，平台原文 "tracks daily Wikipedia page views…"）；
- 只有 `sentiment33` 是真 NLP 情绪（5 个文档槽 × 46 信号位）。

⇒ 三者在机制上**互补而非同源**（网络可见度 / 关注度流量 / 文本情绪），这正是同时入场的唯一正当理由；
但也正因为分散在三个机制面，**每一面单独的天花板都会更低**（见 §5 归因）。

### 1.2 塔位校验（实读，不是引用旧档）

`[实跑]` `get_pyramid_alphas()`（无参数 = 当前季度）返回 `DEU.D1.sentiment = 1`；DEU 的 D0 全 0。
`[实跑]` `get_pyramid_multipliers()` 返回 `DEU.D1.sentiment = 1.8`。

- **塔未点亮**：需 ≥3 颗才亮塔（`[材料]` CHECKS 的 note 同口径），现只有 1 颗 ⇒ 本战役的正当目标就是给该塔补件。
  ⚠ 该"≥3 才亮塔"的阈值来自 `[材料]` 的 note，**平台工具只返回计数，本轮无法独立确认阈值定义**。
- **倍率是动态值，旧档不可当凭证**：`tracking/DEU/s1_sentiment27_wave1_template_pool.md:14` 记的是
  `DEU/SENTIMENT 金字塔×1.9`，今天实读 **1.8**。⇒ 任何以倍率做的收益估算都必须现读，不能抄旧数。
- **木桶倍率律**（`docs/experience/06_atom_mining.md:48-60`）：三集都是 1.8，单集 ATOM 可拿满 1.8；
  一旦混入 1.0x 集（如 pv1）按 1.0 结算，**≥3 集直接计 0 个 Pyramid**。
  ⇒ 本战役三集**分别单集开波**是对的；任何"把三集拼一起"的写法会把 1.8 打到 0 塔，禁止。
- **ATOM 优先**（AGENTS.md §7.7）：三集各自在本集内穷尽几何后才允许跨集，且跨集只许
  gating / grouping / residual / ratio 四形态。本战役 13 臂**全部单集**，符合。
- 注意 `pyramids.effective == 1` **不是** ATOM 判据（AGENTS.md §7.7 明写）；收割件 `QPveY7Kg` 实读
  `effective 1 / list=[DEU/D1/SENTIMENT ×1.8]`，只说明它落在单塔，不证明它是 ATOM 单集。

### 1.3 历史处置状态（决定"这波该不该开"）

| 数据集 | 既有判定 | 出处 |
|---|---|---|
| `sentiment27` | ✅ **维持判死**（双十模板池 20 条读数 S≤0.64） | `atom_orthogonal/DEATH_AUDIT_20261110.md:21` |
| `sentiment27` | ❌ 水平面有效但强度不足，**S 天花板 0.95** | `atom_orthogonal/DATASET_DISPOSITION_MAP_20261111.md:17` |
| `sentiment7` | ⚠️ 维持判死（作为主腿），**只能做正交腿** | `tracking/DEU/reports/deu_campaign_20261030.md:2704`；`DEATH_AUDIT_20261110.md:20` |
| `sentiment33` | 📁 **PROVISIONAL 待复核**：原判"CW 结构性"，但属**配置层死**，须先测 rank/sector 替代几何（D6） | `DEATH_AUDIT_20261110.md:22,45,52` |
| `sentiment33` | ❌ 小样本幻觉（四波 32 臂，lc 12→139 时 R 从 +0.1125 掉到 +0.0214） | `atom_orthogonal/SENTIMENT33_FULL_VERDICT_20261111.md:39-55` |

⚠ **两处台账数字互相矛盾，必须登记**：`sentiment27` 的 S 天花板在 DEATH_AUDIT 记作 **0.64**、在
DATASET_DISPOSITION_MAP 记作 **0.95**（本波实测最好 0.78，落在两者之间）。结论方向一致（都远低于 1.58），
但数字口径没统一（见附录 A2）。**本报告不据此改写任一档案。**

⚠ **`sentiment7` 同样有三档冲突，且本波读数超过了全部三档——这一点必须正面回答**：

| 出处 | 记的 S 天花板 |
|---|---:|
| `tracking/DEU/reports/deu_campaign_20261030.md:2704` | **0.85** |
| `atom_orthogonal/DEATH_AUDIT_20261110.md:20` | **0.77** |
| `atom_orthogonal/DATASET_DISPOSITION_MAP_20261111.md:18` | **0.66** |
| **本波 A7-01（实读 `metrics.sharpe`）** | **1.02** |

⇒ A7-01 的 1.02 **高于既有三档全部读数**（高 0.17–0.36），所以"sentiment7 作为主腿判死"这句话在本波之后
**不能原样引用**。正确处理是：**天花板记录作废、改为"已知最好 1.02"**，但判死结论仍维持——
因为 1.02 距 S 线 1.58 差 **35%**、距 F 线 1.0 差 65%、距 2Y 线 1.58 差 82%（`[实跑]` A1x7E5KR 全闸原值）。
即：**"过不了闸"是硬的，"天花板 0.85"这个数是软的**，两者不要混说。

⇒ 本战役的合法性来自 `sentiment33` 的 **PROVISIONAL 待复核**（必须补 rank/sector 替代几何）；
`sentiment27` / `sentiment7` 属"已判死但按用户指令可复核"的低优先池（`DEATH_AUDIT:52` 的 BA3 列表点名
`sentiment33（CW 替代几何）`、`sentiment7/27 的 D6 补测`）。

---

## 2. 全字段画像分母与路径

### 2.1 分母与路径（三份档案，全部本次实跑闸门复核）

| 数据集 | 画像档案 | 平台字段数 | 画像字段数 | 完整性闸（本次实跑） |
|---|---|---:|---:|---|
| `sentiment27` | `tracking/DEU/reference/datasets/sentiment27.md` | 18 | 18 | **PASS / exit 0**（18 个 id，18 个带读数，无通配分母） |
| `sentiment7` | `tracking/DEU/reference/datasets/sentiment7.md` | 3 | 3 | **PASS / exit 0**（3 / 3） |
| `sentiment33` | `tracking/DEU/reference/datasets/sentiment33.md` | 255 | 255 | **PASS / exit 0**（255 / 255） |

实跑命令与原始输出节选：

```
python tools/gates/field_profile_completeness_gate.py --profile tracking/DEU/reference/datasets/sentiment33.md
  [field-completeness] tracking\DEU\reference\datasets\sentiment33.md
    字段全表 id 数: 255
    带实测读数的字段: 255
    ✅ PASS：全字段均有实测读数，且分母无通配占位   (exit=0)
```

分母不是靠"画像自己说有 255 个"成立的，但**三份档案的对账方式并不相同，不能混写**：

| 数据集 | 分片情况 | 对账依据 |
|---|---|---|
| sentiment27 | **未分片**：单页 `complete=true / pages_fetched=1 / platform_count=18 / returned=18` | `sentiment27.md:4`（**三处**一致：`platform_count` / 字段全表 18 行 / `get_datasets fieldCount=18`） |
| sentiment7 | **未分片**：单页 `complete=true / pages_fetched=1 / platform_count=3 / returned=3` | `sentiment7.md:4`（明写"四路一致"：platform_count / returned / `get_datasets fieldCount` / 本地 `field_catalog`） |
| sentiment33 | **不是单页**：整集一次拉取约 182 KB，被工具结果预算截断（`originalBytes=181900`），**改为 14 个前缀分片逐片实读**；各分片 `count == returned`，加总 44+39+39+41+44+3+5+2+13+5+5+5+5+5 = 255 = `platform_count` | `sentiment33.md:6-9` 与 `:20`；⚠ 该档案**没有**写 `get_datasets fieldCount` / `field_catalog` 的对账 |

⇒ 原报告把"单页 returned=255 且三路/四路对账"套到 sentiment33 上是**错的**：它是 14 分片，
且该集只做了 `platform_count` + 分片加总 + 画像 255 行三者对账。

### 2.2 画像的实质内容（决定模板只能用哪些字段）

**sentiment27（18 字段 = 14 VECTOR + 4 SYMBOL，`:11-21`）**
- 可用性三分：**信号可直接用 11**（61.1%）/ **计数需归一化 2** / **元数据不可用 5**（`sentiment27.md:102-129`）。
- 排名类是"越低越热门"，**进表达式必须取负**；`snl27_wq_pit` 是内部 PIT 标记（描述明写 not an analytical metric），
  与 4 个 SYMBOL 日期戳一起被排除。
- coverage 只有两档：0.9022（15 个）/ 0.9118（3 个）；`dateCreated` 全 2026-07-01（同日 onboard）。拥挤度：`relpopularity08` aC 67 最热，`top75pctranking` aC 10 最冷。

**sentiment7（3 字段 = 3 VECTOR，`:17-22`）**
- **可直接裸用的信号 = 0 个**（`sentiment7.md:89-93`）：两个浏览量字段都是无界正计数，必须 rank / ts_zscore / 比值；
  `snt7_timestamp` 是"内容日期 YYYYMMDD"，平台无日期算子，**不可作信号**（`:108-114`，其 aC=6 推断为误用，不构成可用性证据）。
- 两字段是**同一度量的两层聚合**（全语言合计 vs project×access-type 拆分），只能取一席，或做"合计÷分项"的单一含义比值（`:104-106`）。
- 另有**本地目录陈旧**的实测：`field_catalog` 的 uC/aC 是 1/1、1/2、3/3，平台是 6/37/76 等 ⇒ 拥挤度只能读平台（`:52-62`）。

**sentiment33（255 字段 = 5 槽 × (46 信号 + 5 元数据)，`:74-104`）**
- 三分：**有界 0–1 评分 90**（35.3%，唯一开箱可用）/ **计数需归一化 140**（54.9%，必须先
  `divide(·, valid_tokens_total)` 或 rank/zscore）/ **元数据 25**（9.8%，原始文本与时间戳，算子无定义）（`:389-421`）。
- coverage **只有 5 个取值、每个恰好 51 字段**（0.3152–0.3258，极差 0.0106，`:24-38`）⇒ **没有任何高覆盖字段**，
  任一股票日约只有 1/3 历史窗口有数据；表达式必须显式处理"无文档 = NaN"。
- 冗余：230 个信号 → **48 个语义位**，**182 个是同语义跨槽副本（79.1%）**（`:433-441`）；
  `sentiment_model6/7/8/9_*` **不是独立信号族**，只是同一语义在别的槽的命名空间补位（`:443-452`）。
- 槽 4 特例：层级计数是 `group_level_2/4`，其余槽是 `3/5` ⇒ 跨槽对齐必须按"层级计数位"，**不能按 level 编号**（`:104`）。

### 2.3 画像的能力边界（必须写进结论，否则会被误当实测）

三份档案都在末尾自限：**本轮零回测、零配额，coverage 是平台声明值，不等于逐日横截面宽度**，
且**未做六法动态实测**（`sentiment27.md:141-146`、`sentiment7.md:137-142`）。
⇒ 画像能支撑的是"哪些字段能进表达式、该怎么归一化、哪些同源不能当两条腿"，
**不能支撑"这个字段有信号"**。信号有无只能靠回测（§5）与收割池（§4）。

---

## 3. 字段模板方案（含论坛 / 论文证据）

`[材料]` PLANS 共 **40 条字段级方案卡**（sentiment27 15 条 / sentiment7 2 条 / sentiment33 23 条），
每条含 `templates`（骨架草稿 + 机制）+ `excluded`（禁用法）+ `evidence`（证据指针）。

### 3.1 按数据集归纳的模板骨架（不是"每字段一条"的复述，而是机制归并）

| 数据集 | 机制族 | 代表骨架 | 关键约束 |
|---|---|---|---|
| sentiment27 | ① 排名水平（取负 + 时序标准化 + 横截面） | `group_rank(-1 * ts_zscore(vec_avg(snl27_avgranking), 22), sector)` | 排名"越低越热门"，**不取负则符号与假设相反** |
| | ② 一阶差 / 边际变化 | `group_rank(-1 * ts_delta(vec_avg(snl27_topranking), 5), sector)` | 差分消规模共线，抓"正在变热" |
| | ③ 自身历史分位 | `-1 * ts_rank(vec_avg(snl27_avgranking), 66)` | 抗长期水平漂移，用于 rank 型组合 |
| | ④ 分布形状（偏度 / 峰度） | `group_rank(ts_mean(vec_avg(snl27_skewness), 22), sector)` | 无界实数**必须 rank/zscore 包裹**；偏度方向未定，须正负各测 |
| | ⑤ 计数比值（单一含义） | `divide(vec_sum(snl27_totalcountrydomains), vec_sum(snl27_totaldomains))` | 裸用计数 = 规模因子；比值须防零 |
| | ⑥ 事件闸门 | `trade_when(vec_avg(snl27_kurtosis) > ts_mean(..., 66), <水平臂>, -1)` | 第三参 −1 = 维持持仓 |
| sentiment7 | ① 浏览量短窗跳变 | `group_rank(ts_delta(vec_sum(snt7_all_languages_views), 5), subindustry)` | 必须 vec_* 归约；裸水平 = 规模因子 |
| | ② 相对自身年度基准 | `group_rank(divide(vec_avg(A), ts_mean(vec_avg(A), 252)), industry)` | 比值天然去规模 |
| | ③ 合计÷分项（唯一允许双字段） | `group_rank(divide(vec_sum(all_languages), vec_sum(snt7_views)), sector)` | 单一含义"未被拆分覆盖的语言份额" |
| | ④ 事件闸门 + 低换手 | `trade_when(vec_count(snt7_views) > 0, group_rank(ts_rank(vec_avg(...), 66), subindustry), -1)` | 只在有浏览记录时改仓 |
| sentiment33 | ① 计数÷同槽 token 总量（密度） | `group_rank(divide(vec_sum(method_1_pos), vec_sum(valid_tokens_total)), subindustry)` | **分母必须同槽**，跨槽混用会引入覆盖差 |
| | ② 净语调（同一引擎两极性合成单腿） | `divide(vec_sum(pos) - vec_sum(neg), vec_sum(pos) + vec_sum(neg) + 0.001)` | 单一含义，不是两条腿；+0.001 防零 |
| | ③ 有界评分水平 / 一阶差 | `group_rank(ts_delta(vec_avg(method_2_pos), 22), subindustry)` | 90 个有界评分是唯一开箱可用族 |
| | ④ 客观性 / 中性占比作**闸门** | `trade_when(ts_rank(vec_avg(method_2_filtered_obj), 66) < 0.5, <方向臂>, -1)` | 客观性度量信息含量，**不是多空方向** |
| | ⑤ 排版长度作**控制变量** | `vector_neut(<情绪臂>, vec_avg(max_token_length))` | 句长反映排版，不作主信号 |
| | ⑥ 过滤存活率 | `divide(filtered_pos, pos + 0.001)` | 度量信号纯度，不做"两条腿"解释 |

**语法层面已做的预检**（`[材料]` PLANS 的 evidence）：`preflight_expressions(DEU/TOP500/D1)` 对 sentiment27 /
sentiment7 / sentiment33 的代表式均返回 `valid=true, unknown_fields=[], any_changed=false`（4 条明文记录：
`snl27_relpopularity1` 差分式、`totalcountrydomains/totaldomains` 比值式、`method_1_pos/token_total` 密度式、
`method_2_pos` 的 trade_when 式）。⚠ 预检只验"字段名 + 语法合法"，**不验信号**。

### 3.2 明确排除项（这些"不写"比"写"更重要）

- **元数据一律不进模板**：sentiment27 的 4 个日期戳 + `snl27_wq_pit`（5 个）、sentiment7 的 `snt7_timestamp`（1 个）、
  sentiment33 的 25 个 `headline/event_title/true_timestamp(_epoch)/time_ingested_epoch`。
- **同源不得当两条独立腿**：`snl27_*` 与 `snt27_rank` 同属 Tranco 排名体系；`top50pctranking` 与
  `top75pctranking` 同子族；`relpopularity08` 与 `relpopularity1` 只差复合参数；sentiment7 两浏览量字段是同一度量两层聚合；
  sentiment33 跨槽 182 个副本。这些同用属"重复买同一条信息"，且受 `mixed_signal_leg_ban_v1` 约束。
- **裸计数 / 裸无界实数不横截面**：权重集中风险（`CONCENTRATED_WEIGHT`）——这一条在第 5 节被实测证实（§5.3）。
- 一处**笔误留档**：sentiment33 `method_1_neg` 的第一条草稿写成了双 `divide` 嵌套，卡片自己标注"笔误，保留以便追溯，
  不采用；以第二条为准"。本报告沿用其第二条（净语调式）。

### 3.3 论坛证据（本轮模板卡的 evidence 字段）

| article_id | 用在哪 | 支撑的具体主张 |
|---|---|---|
| `15053280147223` | sentiment27 一阶差 / 计数差分 | 用一阶差分消掉与规模相关的水平项，抓增速而非存量 |
| `8046468280727` | sentiment27 分位截断族；sentiment33 降相关 | 降相关靠换字段/算子/分组，**不靠扭曲原想法** |
| `15233993197079` | 偏度 / 峰度 | 偏度定义（负偏→极端负结果概率高）；正峰度 + 负偏 → 极端回撤概率高 |
| `14431641039383` | 无界实数包裹 | rank / ts_rank / zscore / ts_zscore 防权重过度集中 |
| `8360363631127` | 全部 `trade_when` 骨架 | `trade_when(Event, Alpha, -1)`：事件型/低换手，第三参 −1 = 维持持仓 |
| `doc:vector-datafields` | VECTOR 归约 | `vec_avg / vec_sum / vec_count` 的语义；情绪向量的密度示例 |
| `doc:getting-started-sentiment1-dataset` | sentiment33 窗长 | 情绪类高 turnover → 用 decay 平滑；**回看 >63 天开始失真**（故窗口上限取 66） |

### 3.4 论文证据（来自既有模板池档案，不是本轮新增检索）

| 论文 / 研究 | 结论 | 落到哪个模板 | 出处 |
|---|---|---|---|
| **Pyun (2024)** | Δviews 横截面变化量 | sentiment7 的 T8 `group_rank(ts_av_diff(bf,22), subindustry)`（本战役 A7-01 的直接祖先） | `s1_sentiment7_wave1_template_pool.md:58`（T8 行；`:56` 是 T6） |
| **Cergol (2015)** | 注意力-收益耦合在牛熊不对称 | sentiment7 的 T9 `ts_corr(bf, returns, 22)` | 同文件 `:59`（T9 行） |
| **Da-Engelberg-Gao (2011) / Liu-Peng (2015)** | 注意力突增后 1–2 周延续、年内反转；AbnAttention = 对过去一年基线的偏离 | sentiment27 的"基线偏离"臂（`ts_av_diff(relpop08, 252)`）与短窗反转窗口 | `s1_sentiment27_wave1_template_pool.md:26-27`（§三 论文取证） |
| **Chalamandaris (2026)** | 情绪状态真实影响横截面定价，但**水平不可交易**，只有动态面有 alpha | 三集的"禁做水平面"纪律 | `s1_sentiment27_wave1_template_pool.md:31` |
| **Tetlock (2007) / Loughran-McDonald (2011)** | 媒体悲观词推价后反弹；LM 词典优于 Harvard IV | sentiment33 的正/负词密度与净语调 | `SENTIMENT33_FULL_VERDICT_20261111.md:28` |
| **Tone disagreement (MDPI)** | 语气分歧预测的是**隐含波动率**，不是收益率 | sentiment33 改走"门控/风险用法"而非方向 | `SENTIMENT33_FULL_VERDICT_20261111.md:25` |

⚠ **证据等级声明**：上述论文只支撑"机制假设合理"，**不支撑"该机制在 DEU/TOP500/D1 可交易"**。
sentiment33 自己的 32 臂读数已经反过来否证过一次（R 随覆盖扩大而衰减翻负，`:39-55`）——
所以论文在这里的角色是"决定先测哪一格"，不是"证明能出货"。

---

## 4. 零配额收割

### 4.1 收割池三条（`[材料]` HARVEST；metrics/pyramids 由 `[实跑]` `get_alpha_details` 复核）

| alpha | 区域 / 宇宙 | 表达式形态 | S | F | TO | 2Y | prod | self | pyramids | 形态合法性 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `WjOAJWxd` | **EUR / TOP2500 / D1** | `vector_neut(analyst 腿, group_rank(ts_mean(vec_avg(snt27_relpopularity1),66)))` | 2.36 | 1.61 | 0.0795 | 2.67 | 0.6806 | 0.6446 | EUR·D1·ANALYST ×1.3 + EUR·D1·SENTIMENT ×1.4（`effective 2`） | ✅ residual 形态（§7.7 四形态之一） |
| `78LKlOw1` | **EUR / TOP2500 / D1** | `add(signed_power(analyst 腿,1.5), multiply(1.2, group_rank(vec_avg(snl27_kurtosis))))` | 1.90 | 1.09 | 0.0428 | 2.37 | 0.6433 | 0.5368 | 同上（`effective 2`） | ❌ **`add()` 混两条独立腿**，违反 §7.7 |
| `QPveY7Kg` | **DEU / TOP500 / D1** | `vector_neut(snt7 突增腿, ts_backfill(vec_avg(snl27_relpopularity08)))` | 2.03 | 1.61 | 0.161 | 2.54 | 0.6671 | 0.0242 | **DEU·D1·SENTIMENT ×1.8**（`effective 1`） | ✅ residual 形态 |

三件的 `status` 均为 `UNSUBMITTED` / `stage=IS`（`[实跑]` get_alpha_details），即"零仿真配额、直接可读"。

### 4.2 逐条结论

**① 对本战役（DEU 塔）的有效收割 = 0 条。**
- `WjOAJWxd` / `78LKlOw1` 是 **EUR/TOP2500**，进的是 EUR 塔，不进 DEU·SENTIMENT。材料里没写区域，只有 `[实跑]` 的
  `settings.region` 才看得出来——**这是本轮最容易误判的一处**（若按 `snl27` 字段是 DEU 数据集就假设"这三颗都是 DEU 件"，
  会把 EUR 的两颗错记成 DEU 收割收益）。
- `QPveY7Kg` 是唯一 DEU 件，但见 ②。

**② `QPveY7Kg` 近十年闸不过（`[实跑]` `get_alpha_yearly_stats`）。**
| 年 | long/short | pnl | sharpe |
|---|---|---|---:|
| 2014–2018 | **0 / 0** | **0** | 0 |
| 2019 | 84 / 82 | +996,227 | 2.27 |
| **2020** | 114 / 115 | **−7,823** | **−0.02** |
| 2021 | 148 / 145 | +1,335,884 | 2.66 |
| 2022 | 161 / 158 | +2,043,476 | 4.22 |
| 2023 | 105 / 103 | +686,412 | 1.18 |

⇒ 两条独立的不合格：**① 前五年零持仓**（真实可交易期只有 2019–2023 共 5 年）；**② 2020 年 pnl 为负**。
这正是 AGENTS.md §7.5 第 3 条点名的陷阱——全期 S 2.03 / 2Y 2.54 很好看，逐年一读就露。
对照：同字段的 `A1x7E5KR` 在 2014 年就有持仓（`[材料]` SUBMIT 闸③表，2014 年 lc 98 / sc 112），
所以**不是 sentiment7 数据起点在 2019**——同一字段 `snt7_all_languages_views` 在 2014 就有台账。
**"为何 2019 才开始"本轮未归因**，只登记两个待验候选解释（都不构成结论）：
① 该式的 `ts_quantile(…, 252)` + `ts_ir(...,22)` 复合结构需要更长预热，且 `vector_neut` 的分组腿
`ts_backfill(vec_avg(snl27_relpopularity08),22)` 若早期稀疏会把整列打成 NaN；② `decay 2 / trunc 0.02`
这套激进配置对早期样本更敏感。要判定必须逐日看持仓（`get_alpha_pnl` 或逐年 `longCount` 明细），本轮未做。

**③ `78LKlOw1` 的 `usable: true` 与仓库铁律冲突，必须按更严的判。**
HARVEST 的 `usable` 判据是**平台线（0.70）**下的 prod/self 数值，不覆盖内部严线；但它的表达式是 `add(独立腿A, 1.2×独立腿B)`，
属 AGENTS.md §7.7 明令禁止的"等权/加权混腿"（与 ATOM 无关的独立铁律）。⇒ **即便 prod 0.6433 是三条里最优的，也不可提交。**

**④ prod / self 两条内部严线会再筛掉两条（不只 prod）。**
`src/wqb/config.py:534` 的 `GATES_INTERNAL.prod_corr_max = 0.65`（2026-11-16 用户指令，留 0.05 缓冲挡"贴线过、48h 后翻闸"），
同一字典 `:531` 的 `self_corr_max = 0.50`（原报告漏了这条）。逐条套：

| alpha | prod（严线 0.65） | self（严线 0.50） |
|---|---|---|
| `WjOAJWxd` | 0.6806 ❌ | 0.6446 ❌ |
| `78LKlOw1` | 0.6433 ✅ | 0.5368 ❌ |
| `QPveY7Kg` | 0.6671 ❌ | 0.0242 ✅ |

⇒ 按平台线 0.70 三条都"过"，**按仓库内部严线没有一条全过**；再加上形态与区域，
`78LKlOw1` 的"prod 最优"这个卖点也就不成立了。
⇒ **三条收割件没有一条能同时过"形态 + prod 严线 + self 严线 + 区域 + 近十年"五关。**

**⑤ self 侧按内部严线（0.50）两条都不合格**：`WjOAJWxd` 0.6446、`78LKlOw1` 0.5368 均 **> 0.50**
（表见 ④）。即使按平台线 0.70 看，`WjOAJWxd` 也只剩 0.055 余量，属"贴线件"，即便其他闸过了也应重查。

---

## 5. 逐波处方、臂表与归因

### 5.1 逐波处方（先看"这波想验什么"，再看读数）

| 波 | 处方（结构维） | 覆盖 | 目的 | 结果 |
|---|---|---|---|---|
| 波 1 | **跨三集的水平 / 一阶差 / 信噪比几何**：排名反向水平（ts_zscore）、Δ22、净额（两字段相减）差分、密度差分 | sentiment27（4 臂：A27-01…04）、sentiment7（3 臂：A7-01…03）、sentiment33（3 臂：A33-01…03）＝ 10 臂 | 在三个机制面各取"最标准"的几何，量出各自天花板 | 最好 **S 1.02**（A7-01） |
| 波 2 | **`ts_ir` 包裹（信噪比结构维）**：在波 1 最优臂外套 `ts_ir(x, w)` | A7-04、A7-05、A27-05 | 检验"用信息比率压噪"是否是跨数据集可搬运的结构杠杆 | 最好 **S 0.81**（A7-05）< 波 1 |
| 波 3 | **未开波** | — | 停止规则触发：波 2 未达 +0.02 改善门槛，且机制天花板已量到 | 判停手（`[材料]` STOP） |

**停止规则是怎么算的（`[材料]` STOP，我复算一致）**：
- 波 2 最好 0.81 < 波 1 最好 1.02 ⇒ 未达预设 +0.02（⚠ 此判定依赖"1.02 属波 1、0.81 属波 2"的归属，
  见 §5.2 末的依赖声明）。
- 对 `A7-05` 这一条另有更硬的算术：它的 TO **0.1246 已低于 F 分母地板 0.125** ⇒ 再降换手对它 **F 零收益**；
  实际收益 `R = 3.27%`（`[实跑]` `metrics.returns = 0.0327`，与 `(F/S)²×0.125 = 3.2%` 吻合），
  要在该 R 下把 F 推到 1.0 需 `S = sqrt(0.125/R) ≈ 1.96`（现 0.81 的 **2.4 倍**）。
  ⇒ **对这条臂**，窗口 / 分组轴 / decay / 中性化 / 截断任何单步都补不上 2.4 倍。
  ⚠ **这条不能外推到全波**：其余 10 条臂 TO > 0.125，降换手**是**有效杠杆（全波口径见 §5.3 第二层）。

### 5.2 臂表（13 条读数全列，`[材料]` RESULTS）

| 编号 | alpha | 数据集 / 字段 | 结构 | S | F | TO | 2Y | SU | RA fail | 卡在哪（材料 `blockedBy` 原串） |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| A27-01 | `j2arOJEj` | snl27 `relpop08 − relpop1` | 净额 Δ252 | 0.78 | 0.39 | 0.073 | 0.28 | −0.21 | 4 | S/F/2Y |
| A27-02 | `KPgEZpdk` | snl27 `avgranking` | **−1×**Δ22 | 0.16 | 0.03 | 0.2009 | 0.12 | −0.24 | 4 | S/F/2Y |
| A27-03 | `2r5Nexzx` | snl27 `relpopularity08` | Δ22 | 0.23 | 0.06 | 0.1484 | **−0.52** | −0.07 | 4 | S/F/2Y |
| A27-04 | `0mPM5L0p` | snl27 `avgranking` | −1×ts_zscore22 | 0.01 | 0.00 | 0.2301 | −0.01 | −0.19 | 4 | S/F/2Y |
| A27-05 | `wpoEAPd2` | snl27 净额 | **ts_ir(Δ252, 252)** | 0.22 | 0.06 | 0.0256 | −0.09 | **−0.81** | 4 | S/F/2Y/SU |
| A7-01 | `A1x7E5KR` | snt7 `all_languages_views` | Δ22 | **1.02** | 0.35 | 0.4065 | 0.28 | 0.32 | 4 | S/F/2Y/SU |
| A7-02 | `1YWz0REz` | snt7 `views` | Δ22 | 0.90 | 0.28 | 0.4054 | **−0.32** | 0.15 | 4 | S/F/2Y/SU |
| A7-03 | `j2arOJQE` | snt7 `views` | ts_zscore22 | 0.68 | 0.18 | 0.4442 | −0.22 | −0.12 | 4 | S/F/2Y/SU |
| A7-04 | `akaE8wm9` | snt7 `all_languages_views` | **ts_ir(Δ22,22)** | 0.14 | 0.03 | 0.1274 | −0.45 | −0.39 | 4 | S/F/2Y/SU |
| A7-05 | `VkN3L5rY` | snt7 `views` | **ts_ir(Δ22,22)** | 0.81 | 0.41 | 0.1246 | 0.94 | 0.05 | 4 | S/F/2Y/SU |
| A33-01 | `ZYaKN9L0` | s33 `method_1_pos / token_total` | 密度 Δ22 | 0.37 | 0.12 | 0.4049 | −0.05 | −0.03 | **5** | S/F/2Y/SU/**CW** |
| A33-02 | `kqaZ9M5z` | s33 `method_3_neg` | −1×Δ22 | 0.42 | 0.15 | 0.4043 | 0.14 | 0.03 | **5** | S/F/2Y/SU/**CW** |
| A33-03 | `vRAvPb0r` | s33 `method_1_pos / token_total` | 密度 ts_zscore22 | 0.07 | 0.01 | 0.4086 | **−0.92** | 0.00 | **5** | S/F/2Y/SU/**CW** |

（"卡在哪"列 = `[材料]` RESULTS 的 `blockedBy` **原串**——它只含 `SHARPE / FITNESS / 2Y`，A33 另加 CW，
**从不含 SU**。`/SU` 是本报告按 SU 值补的：`[实跑]` 5 条臂的 `checks.fail` 全部含
`LOW_SUB_UNIVERSE_SHARPE`，其余 8 条按同一判据（SU < 该臂平台的 ≈0.475×S，见下）判定，故不是"原串"。
RA fail 数为平台 `failed_ra_count` 口径。CW = `CONCENTRATED_WEIGHT`，limit 0.1，三臂实测 0.5，
命中日 2018-10-19（A33-03）/ 2019-09-13（A33-01、A33-02，`[实跑]` checks 原值）。）

⚠ **波归属是推断，不是材料标注，且"结论不变"有依赖条件**：RESULTS 未带波号，本表按 STOP 文本
"上一轮的结构维 = `ts_ir` 包裹"把 3 条 `ts_ir` 臂（A7-04 / A7-05 / A27-05）归到波 2、其余 10 条归到波 1。
- 这个 10 是 `[材料]` WAVES 所称 "wave1 15" 的**子集**（15 条里有 5 条没有行级明细，见 §5.4 / 附录 A3）。
- **关键依赖**：+0.02 门槛的"未达"判定依赖 "1.02 属于波 1、0.81 属于波 2"。若实际归属相反，门槛会翻向"已超 +0.02"，
  停止理由就只剩"天花板算术"那一条（§5.1 第二条）。本报告采信 WAVES 的显式表述（"w1：最佳 S 1.02"、"w2：最佳 S 0.81"），
  但**这条依赖必须写出来**，不能只说"读数不变"。

### 5.3 归因（三层，从"哪道闸"到"为什么"到"能不能补救"）

**第一层：闸门分布**
- `LOW_SHARPE`：**13/13 全灭**（最高 1.02 vs 1.58）。
- `LOW_FITNESS`：**13/13 全灭**（最高 0.41 vs 1.0）。
- `LOW_2Y_SHARPE`：**13/13 全灭**（最高 0.94 vs 1.58）。
- `LOW_SUB_UNIVERSE_SHARPE`：**13/13 不过**，但**该闸的 limit 是相对量，不是常数 0.48**。`[实跑]` 5 条臂的
  `checks.fail` 原值：

| alpha | S | SU 值 | 平台 limit | limit / S |
|---|---:|---:|---:|---:|
| A1x7E5KR | 1.02 | 0.32 | 0.48 | 0.471 |
| VkN3L5rY | 0.81 | 0.05 | 0.38 | 0.469 |
| j2arOJEj | 0.78 | −0.21 | 0.37 | 0.474 |
| ZYaKN9L0 | 0.37 | −0.03 | 0.18 | 0.486 |
| vRAvPb0r | 0.07 | 0.00 | 0.03 | 0.429 |

  ⇒ 5/5 拟合 **limit ≈ 0.475 × S**（样本仅 5 条、平台未给公式，属**经验拟合，不是确证**）。
  按此判，13 条臂的 SU 实测值全部低于自身 limit（≈0.475×S），故"13/13 不过"成立，但**理由不是"低于 0.48"**。
- `CONCENTRATED_WEIGHT`：**仅 sentiment33 三臂 3/3 中招**（0.5 > 0.1）。
- `CLUSTER_TEST`（**warning，不是 fail**，不改变"全灭"结论，但属"卡在哪"的完整画像）：`[实跑]` 5 条臂中
  **4 条报 warning**——j2arOJEj 0.82<1、VkN3L5rY 0.48<1、ZYaKN9L0 0.16<1、vRAvPb0r 0<1；只有 A1x7E5KR 通过。
  收割件里 `78LKlOw1` 也是 warning（1.29<1.58），`QPveY7Kg` 通过。⇒ 除 A7-01 外，本轮候选在"聚类集中度"上
  普遍偏弱，这与 `CONCENTRATED_WEIGHT` 的结论同向（信号集中而非分散）。
- `TURNOVER`：**13/13 全过**（0.0256–0.4442，线 0.01–0.70）。⚠ **这不等于"换手不是瓶颈"**——
  F 的分母是 `max(TO, 0.125)`，10/13 条臂 TO > 0.125，**压低换手在 R 不变时按 `1/√TO` 抬 F**。
  实测口径：A7-01 若 TO 0.4065→0.125，F 0.35→**0.62**（+78%）；A33-01 同理 0.12→**0.22**。
  ⇒ 正确表述是：**降换手有效，但封顶也到不了 1.0**（A7-01 要在现 R 下 F=1，需 TO≈4.9%，即约 8 倍削减）。
  原报告"降换手方向从一开始就是错的"是**错的**，已撤回。

**第二层：为什么 S 提不上去——收益缺口（`[实跑]` 平台 `metrics.returns`，其余推导）**
口径：平台 `F = S · sqrt(|Ret| / max(TO, 0.125))` ⇒ `R = (F/S)²·max(TO,0.125)`；
达到 `F=1.0` 需 `R_need = max(TO, 0.125) / S²`；两者之比恒为 **`1/F²`**（与 TO 无关，这是本轮最干净的一条）。

| 臂 | S | F | TO | R（实际） | R_need（在该 S 下） | 缺口 |
|---|---:|---:|---:|---:|---:|---:|
| A27-01 | 0.78 | 0.39 | 0.073 | 3.06% ★ | 20.5% | 6.6× |
| A27-02 | 0.16 | 0.03 | 0.2009 | 0.71% | 784.8% | **1111×** |
| A27-03 | 0.23 | 0.06 | 0.1484 | 1.01% | 280.5% | 278× |
| A27-04 | 0.01 | 0.00 | 0.2301 | 0% | ∞ | ∞ |
| A27-05 | 0.22 | 0.06 | 0.0256 | 0.93% | 258.3% | 278× |
| A7-01 | **1.02** | 0.35 | 0.4065 | **4.68%** ★ | **39.1%** | **8.2×** |
| A7-02 | 0.90 | 0.28 | 0.4054 | 3.92% | 50.0% | 12.8× |
| A7-03 | 0.68 | 0.18 | 0.4442 | 3.11% | 96.1% | 30.9× |
| A7-04 | 0.14 | 0.03 | 0.1274 | 0.58% | 650.0% | **1111×** |
| A7-05 | 0.81 | 0.41 | 0.1246 | **3.27%** ★ | 19.1% | 5.9× |
| A33-01 | 0.37 | 0.12 | 0.4049 | **4.33%** ★ | **295.8%** | **69.4×** |
| A33-02 | 0.42 | 0.15 | 0.4043 | 5.16% | **229.2%** | **44.4×** |
| A33-03 | 0.07 | 0.01 | 0.4086 | **0.85%** ★ | 8339% | 10000× |

★ = 平台 `metrics.returns` 实读；其余由 `R=(F/S)²·max(TO,0.125)` 推导（该式对 5 条实读件复算误差 <3%）。

**读数含义（原报告的"两类死因"已撤回）**：
- **13/13 都是"收益不够"**，缺口 5.9×–10000×（A27-04 的 F=0、R=0，缺口发散），**没有一条属于"收益够、只是波动大"**。
- 原报告说 "A33-02 的 R 5.2% 已高于 S=1.58 达标线 5.01%" 是把 TO 当 0.125 算的**错误结论**：
  它的 TO 是 0.4043，F=1 且 S=1.58 时需 R = **0.4043/1.58² = 16.2%**，它只有 5.2%，**差 3.1 倍**；
  同口径下把这颗的 S 换成 1.58，F 也只有 **0.56**。
- 相对而言 sentiment33 是**最差档**（缺口 44×/69×），sentiment7 是**最好档**（5.9×/8.2×）——
  与"sentiment33 收益够"相反。
- ⇒ 处方也随之一致：**要动就只能动收益/波动比本身**（换机制或换配置），不存在"压波动就够了"的快捷路径。

**第三层：结构维为什么反复失败（这轮最有价值的三条）**

1. **`ts_ir` 不是可搬运的杠杆，且方向会翻**：波 2 三条里，A7-04（同字段 A7-01）S **1.02→0.14**、2Y **0.28→−0.45**；
   A27-05（同字段 A27-01）S **0.78→0.22**、SU **−0.21→−0.81**。只有 A7-05 把 2Y 从 −0.32 抬到 **0.94**（+1.26）、
   TO 0.4054→0.1246，但代价是 S 0.90→**0.81**、SU 0.15→0.05。
   ⇒ **同一结构在同一数据集的不同字段上结论相反**，说明它是"配置×字段"的交互项，不是机制级杠杆。按 §7.6 纪律，
   这属于"配置层"证据，不能升格成"信号层死"。
2. **裸 rank/密度仍压不住 `CONCENTRATED_WEIGHT`**：sentiment33 三臂**已经用了** `group_rank(...)` + SUBINDUSTRY，
   CW 仍报 0.5 > 0.1（命中日 2018-10-19 / 2019-09-13）。`DEATH_AUDIT:22` 要求的"CW 替代几何（rank/sector）"
   在本波**只完成了 rank 一半、sector 完全没测** ⇒ 该维**未闭合**，sentiment33 仍是 PROVISIONAL。
3. **外层变换能把读数打掉一个量级（但原报告把对照写错了）**：同字段、同 22 窗、只换外层变换的**唯一**干净对照是
   A27-02（`−1×ts_av_diff(avgranking, 22)`，S **0.16**）vs A27-04（`−1×ts_zscore(avgranking, 22)`，S **0.01**），
   差 **0.15**。原报告写的"净额 0.78 vs 净额 ts_zscore 0.01、差 0.77"是**不存在的臂**（A27-04 的输入是 `avgranking`，
   不是 relpop 净额；窗口也不同），量级被夸大 5 倍，已更正。
   对"该字段族对外层变换敏感"这个方向仍成立：同字段只换外层，最好 0.16 与最差 0.01 差一个数量级；
   与 `s1_sentiment27_wave1_template_pool.md:15` 的金帖教训（"ts_zscore 外层在该字段族禁用，全结构崩盘 SH −0.33"）同向。
   ⇒ 但要克制解读：这属"算子选择主导"，**不是**"机制被验证/被否证"。

### 5.4 数据一致性告警（必须登记，不要按单一口径引用）

`[材料]` WAVES 最后一段写"累计 28 条读数（wave1 15 + … + 本轮 13）"，但 RESULTS 只实列 **13 行**，
`stop` 里又说"逐闸看三条臂"（= 波 2 的 A7-04/A7-05/A27-05）。**15 + 13 = 28 与 13 行明细无法对齐**。
本报告的可引用集合以 **RESULTS 的 13 行**为准；`28` 这个数若要进台账，必须先补齐缺失的行级明细（见附录 A3）。

⚠ **这条直接限制"停手"结论的置信度**：缺失的 15 条波 1 读数本轮无法核，**理论上可能包含 >1.02 的臂**。
已知约束只有 WAVES 的文本断言（"w1：最佳 S 1.02"）——若采信它，停手成立；若不采信，停手理由只剩
§5.1/§5.3 的天花板算术（对已有的 13 条成立，对未知 15 条不成立）。**本报告不把 WAVES 的断言当成已核实事实。**

---

## 6. prod + self 相关性

| 对象 | prod | self | 判定（平台线 0.70 / 内部严线 prod 0.65、self 0.50） | 来源与确认状态 |
|---|---:|---:|---|---|
| `A7-01 (A1x7E5KR)` | **0.3742** | **0.1032** | ✅ 两条线全过 | `[材料]` CORR + SUBMIT 闸④；**来源=平台 self 工具**（`local_calculation=true`），本轮未重跑 |
| `WjOAJWxd`（EUR） | 0.6806 | 0.6446 | ❌ **prod 0.6806 > 0.65 且 self 0.6446 > 0.50**（按平台 0.70 才"过"） | `[材料]` HARVEST，**预读值，非平台确认** |
| `78LKlOw1`（EUR） | 0.6433 | 0.5368 | ⚠️ prod 过 0.65，但 **self 0.5368 > 0.50**（另形态违规，见 §4.2③） | `[材料]` HARVEST，**预读值，非平台确认** |
| `QPveY7Kg`（DEU） | 0.6671 | **0.0242** | ⚠️ self 极干净，但 **prod 0.6671 > 0.65**（平台线 0.70 下过） | `[材料]` HARVEST，**预读值**；`[实跑]` `submit_verdict` 明确要求先跑 `check_correlation`，本轮未跑 |

**必须说清楚的边界**：
- **其余 12 条波内臂没有做 prod/self 取数**——它们在 S/F/2Y 三闸就已判死，未进入提交候选；
  **不要把这 12 条当成"相关性干净"**，它们的状态是"未测"。
- `QPveY7Kg` 的 prod/self 是 `[材料]` 给定值；`[实跑]` 的 `submit_verdict` verdict_note 明写
  "PROD_CORRELATION / SELF_CORRELATION 未经平台确认…提交前必须另跑 `check_correlation(alpha_id)` 并确认 all_passed"。
  ⇒ **本轮未跑 `check_correlation`**，上表 `QPveY7Kg` 一行只能算"预读值"，不构成放行依据。
- 阈值口径：`src/wqb/config.py:512` `PRODCORR_CEILING = 0.70`（平台硬线）；内部严线在 `GATES_INTERNAL`
  的 `:531` `self_corr_max = 0.50` 与 `:534` `prod_corr_max = 0.65`（原报告把这两条都记成 `:532`，且漏了 self 那条）。
  `tracking/DEU/config/thresholds.json` 的 `self_corr_max` / `prod_corr_max` 都是 **0.7**，**未同步两条内部严线** ⇒ 附录 A1 一并登记。

---

## 7. 提交链五道闸

### 7.1 闸 ①–⑤ 的判据（AGENTS.md §7.5）

① 台账排除（骨架是否已测/已判死）→ ② `submit_verdict`（否决权威，只拦不放）→ ③ 近十年逐年 `longCount>0 && shortCount>0 && pnl>0`
→ ④ self 相关 → ⑤ 篮内互相关 + 塔位配额。

### 7.2 波内最强臂 `A1x7E5KR`（S 1.02）— **BLOCKED**（`[材料]` SUBMIT，本轮未重跑）

| 闸 | 结论 | 证据 |
|---|---|---|
| ① 台账排除 | **FAIL** | 骨架逐字就是 sentiment7 模板池 **T8**：`s1_sentiment7_wave1_template_pool.md:58` 的 `group_rank(ts_av_diff(bf,22), subindustry)`（`bf` 定义在同文件 `:47`）；本条只是去掉 `ts_backfill` 外层，属换包装。T8 读数 "S +0.90 / TO 0.60、全波最强" 见同文件 `:110`；上层判死见 `tracking/DEU/reports/deu_campaign_20261030.md:2704`（"sentiment7 判死（作为主腿）…只能做正交腿"） |
| ② 否决权威 | **BLOCKED**（exit 1） | `reason_code: SIM_FAIL:LOW_SHARPE,LOW_FITNESS,LOW_SUB_UNIVERSE_SHARPE,LOW_2Y_SHARPE`；`failed_ra=4`、`failed_ppa=1`（LOW_SUB_UNIVERSE_SHARPE）；`submit_status=404`、`submit_layer_view=dead_endpoint_404`。**本轮已用 `[实跑]` 的 `checks.fail` 复核**：4 项与材料逐字一致（SU 的 limit 为 0.48，仅该臂如此，见 §5.3） |
| ③ 近十年 | **FAIL** | `get_alpha_yearly_stats` 2014–2023 十年 long/short 全正，但 **2023 年 pnl −123,788、sharpe −0.21、DD 0.0846**（`[材料]` SUBMIT；本轮未重跑逐年） |
| ④ self | **PASS** | `max_correlation = 0.10318259611662818`，`passes_check=true`；池 21/25（排 4 个 power pool）、最大相关者 `pwaQ0bx3` —— 取自 `[材料]` SUBMIT 块，**给出的 CORR 块只有 alpha/prod/self/passes 四字段，池与最大相关者本轮无法复核** |
| ⑤ 互相关 + 塔位 | **不可判定** | `compute_mutual_correlation(["A1x7E5KR"])` 返回 `{"error":"Provide at least 2 distinct alpha ids."}`（工具要求 2+）⇒ 未产出任何数值；塔位可读（`DEU/D1/SENTIMENT ×1.8`、`effective 1`），但**该塔已有几颗的底数有一半不可核**：本地 `alpha_pyramids` DEU 只有 **3 行且全为 UNSUBMITTED**，属陈旧/部分快照——同一时点 `[实跑]` 只读 SQL 得到 `alphas` 表 DEU **`stage='OS'` 25 条、其中 `status='ACTIVE'` 13 条**（另 COMPLETE 6 / UNSUBMITTED 6）。原报告写"25 条 ACTIVE OS"**读错了列**，已更正 |

⇒ 决定性是 ②（4 RA + 1 PPA）与 ③（2023 年负）。①进一步说明该骨架已被判死作主腿。

### 7.3 收割件 `QPveY7Kg`（S 2.03）— 本次实跑，**未通过**

| 闸 | 结论 | 证据（本次实跑） |
|---|---|---|
| ① 台账排除 | ⚠️ **与已提交件高度同宗** | 表达式 = `vector_neut(ts_quantile(ts_ir(ts_mean(max(ts_backfill(vec_avg(snt7_all_languages_views),22), ts_delay(...,5)),5),22),252,driver="gaussian"), ts_backfill(vec_avg(snl27_relpopularity08),22))`。论坛金帖作者获胜式 `np7nn69l` 是同一五层骨架（`s1_sentiment27_wave1_template_pool.md:14`，S 2.04/F 1.92/TO 9.11%），差异仅在 `quantile` 换 `ts_quantile(252)` 且 `ts_max` 换成 `max(x, ts_delay(x,5))`（因平台无 `ts_max`，见同文件 `:15`）⇒ 属"同骨架换算子"，非新骨架 |
| ② 否决权威 | **UNVERIFIABLE（exit 10）** — **不是放行** | `failed_ra=0 / failed_ppa=0`、`sim_fails=[]`；但 `submit_status=404 / dead_endpoint_404 / prepost_unverifiable=true`；`robustness = CONDITIONAL`（recorded 2026-10-31，无 failed_checks；verdict_note 要求先按 `brain-alpha-repair` 修复并重审 ≤2 轮，**不拦截**） |
| ③ 近十年 | **FAIL** | **2014–2018 五年 longCount=0/shortCount=0**，2020 年 pnl −7,823（sharpe −0.02）；仅 2019/2021/2022/2023 四年为正 |
| ④ self / prod | ⚠️ **预读值，非平台确认** | prod 0.6671 / self 0.0242（`[材料]` HARVEST）；按内部严线 **prod 0.6671 > 0.65 超线**（self 0.0242 合格）；`submit_verdict` 明写须另跑 `check_correlation` 确认（**本轮未跑**） |
| ⑤ 互相关 + 塔位 | **不可判定** | 单件篮同样无法算互相关；塔位实读 `DEU/D1/SENTIMENT ×1.8`、`effective 1` |

### 7.4 五道闸总账

| 候选 | ① | ② | ③ | ④ | ⑤ | 可提交？ |
|---|---|---|---|---|---|---|
| `A1x7E5KR`（波内最强） | FAIL | BLOCKED | FAIL | PASS | 不可判定 | **否** |
| `QPveY7Kg`（收割最佳） | 同骨架 | UNVERIFIABLE | FAIL | 未确认 | 不可判定 | **否** |
| `WjOAJWxd` | — | — | FAIL（5 年零持仓） | **FAIL（self 0.6446 > 内线 0.50；prod 0.6806 > 0.65）** | 未测 | **否**（且 EUR，非本塔） |
| `78LKlOw1` | — | — | 未测 | **FAIL（self 0.5368 > 0.50）** | 未测 | **否**（`add()` 混腿违规） |

**本次未执行任何提交动作**：`submit_verdict` 是只拦不放的判定工具（`[实跑]` 的 verdict_note 亦如此写），
放行仍需"平台 prod<0.7 + 用户明确确认 + `workflow_submit_alpha(confirm_submit=True)`"。

---

## 8. 结论与下一步

### 8.1 本战役结论（按证据强度分层）

**A. 成立（有 13 条实测读数支撑）**
1. **本波 13 条单集几何读数没有一条接近闸线**：最好 S **1.02**、最好 F **0.41**、最好 2Y **0.94**（三者分属不同臂，
   最好 S 的那条 F 只有 0.35）。分数据集看最好臂的 S 缺口：sentiment7 1.02（距 1.58 差 **35%**）、
   sentiment27 0.78（差 **51%**）、sentiment33 0.42（差 **73%**）。
   ⚠ 这不等于"三集的几何已穷尽"——本波只测了 5 类结构（§5.3），穷尽性另见 §8.1-B4 的 D 维核算。
2. **停止加注成立（三条独立支撑，前两条只对特定臂成立，第三条对全波成立）**：
   ① 波 2 未改善（0.81 < 1.02）——**依赖波归属**（§5.2 末的依赖声明）；
   ② `A7-05` 的 TO 0.1246 已低于换手地板 ⇒ 对它降换手零收益，且需 S≈1.96（现 0.81 的 2.4 倍）才能补上；
   ③ **全波口径的封顶论证**（这条不依赖波归属）：把 TO 压到 0.125 地板后，A7-01 的 F 由 0.35 只升到 **0.62**、
   A33-01 由 0.12 只升到 **0.22**，**全部仍 < 1.0**；A7-01 要在现收益下 F=1 需 TO≈**4.9%**（约 8 倍削减）。
   ⇒ 降换手是有效但**有上限**的杠杆，补救空间不足以翻闸；真正缺的是收益/波动比本身。
3. **13 条臂的死因同属"收益不够"，只是程度不同（原报告的"两类死因"已撤回）**：
   按 `R_need = max(TO,0.125)/S²` 与实测 R 比，缺口 **5.9×–10000×**（A27-04 的 F=0，缺口发散），且缺口恒等于 `1/F²`。
   **最好档是 sentiment7（5.9×/8.2×）、最差档是 sentiment33（44×/69×）**——与"A33-02 收益够"相反。
   A33-02 在 S=1.58 口径下需 R=16.2%（它只有 5.2%），同口径 F 仅 **0.56**。
   ⇒ "压波动/提覆盖"不是 sentiment33 的快捷处方；三集都只能靠换机制/换配置改收益结构。

**B. 只能记 PROVISIONAL（证据维不全，按 AGENTS.md §7.6）**
4. 本战役 13 臂**只用了 SUBINDUSTRY 一个分组轴、一套配置**（decay/trunc 固定）⇒ **D4（≥2 分组轴）与 D6（≥2 配置）在本波内不满足**。
   叠加历史档案后：sentiment27 的 D1 已足（15 臂结构互异，`s1_sentiment27_wave1_template_pool.md:33-51`）、
   sentiment7 的 D1 已足（12 模板，`s1_sentiment7_wave1_template_pool.md:45-62`）、sentiment33 的 D1 已足（32 臂，`SENTIMENT33_FULL_VERDICT:5-19`）；
   但 sentiment33 的 **D6 只做了 rank 一半、sector 未测**（§5.3 第 2 条）。
   ⇒ **不得**用本报告宣布"sentiment33 终判死"，也不得据此关闭 D1 sentiment 邻接宇宙（`DEATH_AUDIT:45` 已撤回过一次同类结论）。

**C. 与既有台账的冲突（不改档案，只登记）**
5. sentiment27 的 S 天花板：DEATH_AUDIT 记 **0.64** vs 处置图谱记 **0.95**（本波 0.78 落在两者之间，附录 A2）。
6. **sentiment7 的天花板三档冲突且本波全部超过**：0.85（`deu_campaign:2704`）/ 0.77（`DEATH_AUDIT:20`）/ 0.66（`DISPOSITION_MAP:18`）
   vs 本波 **1.02**。⇒ "天花板"记录须作废重记，但"不能做主腿"的结论仍由"距 1.58 差 35%"支撑（§1.3 已展开）。
7. `LOW_SUB_UNIVERSE_SHARPE` **不是常数线**：实读 5 条 limit = 0.48/0.38/0.37/0.18/0.03，拟合 ≈0.475×S
   （样本 5 条，公式未确证）。本地 `sub_universe_sharpe_min = 1.0` 与之**不可直接比较、更不可"对齐 0.48"**（附录 A1）。
8. 收割池 `usable:true` 与 §7.7 混腿禁令冲突（§4.2③）；且内部 self 严线 0.50 会让 `WjOAJWxd` / `78LKlOw1` 双双不过（§4.2④）。

### 8.2 下一步（按优先级，均可零配额完成）

1. **台账回写（必须由有写权限的会话做，本报告不写库）**：
   - 波结论 → `wave_results`（走 `wqb.wave_results_contract.upsert_wave_result`，波号用原字符串）；
   - 停手原因 → `seal_dead_end` **前**必须先过论坛取证闸（`wqb.recon_evidence`）——本战役**没有做过论坛 recon**，
     所以现在不能 `seal_dead_end`；要么补一次 `forum_recon_wave`，要么按 `force_seal` 留痕（须人工确认）。
   - 若要把 sentiment33 的"CW 结构性"升级为结论，**先补 sector 轴实验**再写（见第 2 条）。
2. **若继续 sentiment 面（唯一有 D6 缺口可补的方向）**：
   - **sentiment33 补 D6**：同骨架换 `sector` 分组 + 换 neutralization（如 MARKET / INDUSTRY）/ 换 universe（TOP500→TOP200 或 TOP1000），
     **至少一维**，且要专门验 CW（当前 0.5 > 0.1）。这是 `DEATH_AUDIT:22` 点名要求、本波未闭合的一项。
   - **sentiment7/27 不建议再投**：它们最好臂的 R 也只有 3.1% / 4.7%（与 sentiment33 同属薄档，只是缺口小 5.9×–8.2×），
     补分组轴只会重测同一批薄收益；
     若要动，只按 `DEATH_AUDIT:52` 的"D6 补测兜底"最低优先级做，且必须换机制（例如把 `trade_when` 的条件换成
     跨字段的注意力分歧），不是换窗口。
3. **收割池的处置建议（零配额、可立即执行）**：
   - `QPveY7Kg`：**不要提交**（近十年闸硬性不过）。若要救，唯一方向是把持仓起始期往 2014 推（去掉 252 长窗或改
     `ts_quantile` 窗口），属新仿真、需配额，且要重新过 §7.5 五闸。
   - `WjOAJWxd` / `78LKlOw1`：属 EUR 塔，交 EUR 战役处置；`78LKlOw1` 建议直接标"形态违规，不得提交"，
     免得后续被 `usable:true` 误导。
4. **口径修正（一次性，各自独立提交）**：
   - `LOW_SUB_UNIVERSE_SHARPE`：**不要**把 `thresholds.json` 的 `sub_universe_sharpe_min` "对齐 0.48"——
     平台是**相对**判据（实测 limit≈0.475×S）。本地若要表达，应改成比值键（如 `sub_universe_sharpe_ratio_min ≈ 0.475`）
     或在键上注明"绝对线，**不映射**平台 SU 检查"；并注明该拟合只有 5 个样本、平台未公布公式。
   - 内部严线：`prod_corr_max = 0.65`（`src/wqb/config.py:534`）与 `self_corr_max = 0.50`（`:531`）
     是否同步进 `tracking/DEU/config/thresholds.json`（现两者都是 0.7）。
   - 统一 sentiment27 的 S 天花板口径（0.64 / 0.95 二选一，写清是哪一批读数）；同理把 sentiment7 的
     0.66 / 0.77 / 0.85 三档并档、并以"本波 1.02"作新纪录重记。
5. **报告可复用件（已按审读更正）**：判"薄收益类死案"的正确算式是
   `R_need = max(TO, 0.125) / S²`，**缺口恒等于 `1/F²`**（与 TO 无关）。
   原报告用的 `0.125/S²` 只在 TO ≤ 0.125 时成立；对其余 10 条臂会把所需收益低估 **TO/0.125 倍**，
   即 **1.02×–3.55×**（对应 TO 0.1274–0.4442）。

### 8.3 一句话给下一个会话

**DEU·SENTIMENT 塔本轮补件失败，死因是"收益/R 相对于风险太低"（13/13 缺口 5.9×–10000×，缺口恒为 1/F²），
不是参数没调对；零配额池里没有可用件（区域 / 形态 / 近十年三关各挡一颗）。
要继续就只补 sentiment33 的 sector+配置维（D6），否则应把资源移出该塔。**

---

## 附录：数据口径差异与待裁决项

| # | 差异 | 两侧数字 | 处置建议 |
|---|---|---|---|
| A1 | `LOW_SUB_UNIVERSE_SHARPE` 线的形态 | 平台**逐条不同**：0.48 / 0.38 / 0.37 / 0.18 / 0.03（对应 S 1.02 / 0.81 / 0.78 / 0.37 / 0.07），拟合 **≈0.475×S**（5 样本，未确证）；本地 `tracking/DEU/config/thresholds.json` `sub_universe_sharpe_min = 1.0` | **不要对齐 0.48**（那是单条实例）。平台闸相对化，本地 1.0 若为"绝对内部线"须改键名（如 `…_ratio_min` 或用注释声明"不映射平台 SU"），否则会误判候选"该过没过" |
| A2 | sentiment27 S 天花板 | `DEATH_AUDIT_20261110.md:21` = **0.64**（20 条读数）；`DATASET_DISPOSITION_MAP_20261111.md:17` = **0.95** | 统一到"读数批次 + 最大值"口径，两档案互指；本波实测 0.78 只作补充不覆盖 |
| A2b | sentiment7 S 天花板（**审读新增**） | `deu_campaign_20261030.md:2704` = **0.85**；`DEATH_AUDIT_20261110.md:20` = **0.77**；`DATASET_DISPOSITION_MAP_20261111.md:18` = **0.66**；**本波 A7-01 = 1.02（三档全超）** | 三档并档、以 1.02 作新纪录；"作为主腿判死"的**依据换成"距闸 35%"**，不要再引天花板数字 |
| A3 | 本战役读数总数 | WAVES 称"累计 28（wave1 15 + 本轮 13）"，RESULTS 实列 **13 行** | 入台账前补齐行级明细，否则只引用 13 行；并注明"停手"结论对缺失 15 条的置信度受限（§5.4） |
| A4 | `usable` 字段语义 | HARVEST 的 `usable:true` 只覆盖 prod/self 阈值（且当时按 0.70 平台线）；不覆盖 §7.7 形态禁令、内部 self 0.50、近十年闸 | 建议在收割工具输出里拆成 `corr_ok` / `form_ok` / `span_ok` 三列，避免单一布尔误导 |
| A5 | 倍率漂移 | `s1_sentiment27_wave1_template_pool.md:14` 记 `DEU/SENTIMENT ×1.9`；今日实读 **1.8** | 倍率一律现读（`get_pyramid_multipliers`），旧档只作历史 |
| A6 | 收割件区域 | 材料未标区域；`[实跑]` 读出两件在 **EUR/TOP2500** | 收割池输出应带 `region/universe/delay`，否则会被错记为本地战役收益 |
| A7 | SU 闸的拟合依据（**审读新增**） | 5 条实读 limit/S = 0.471 / 0.469 / 0.474 / 0.486 / 0.429 | 若要写进代码/文档，先补样本（≥10 条、跨 region/universe）再定公式；当前只能当"经验比例" |
| A8 | DEU ACTIVE 计数口径（**审读新增**） | `alphas` 表 DEU：`stage='OS'` **25**、其中 `status='ACTIVE'` **13**（COMPLETE 6 / UNSUBMITTED 6）；`alpha_pyramids` DEU **3 行全 UNSUBMITTED** | 引用"DEU 有多少 ACTIVE"时必须写清是 `stage` 还是 `status` 口径；塔位底数仍不可用该表推定 |

---

*本报告不含数据库写入、不含 alpha 提交。所有 `[实跑]` 项可在同一环境重放；所有 `[材料]` 项均标注来源块。
本版（v2）按审读意见修订：6 项 P0（SU 相对 limit、R 表口径、A33-02 结论、换手结论、ACTIVE 计数、闸命令）、
7 项 P1（blockedBy 原串、报告路径、4 处行号、config 行号、sentiment33 分片、self 0.50、同字段对照）、
5 项 P2（sentiment7 三档天花板、CLUSTER_TEST、塔计数同指一颗、波归属依赖、读数总数限制）；原结论未被推翻。*
