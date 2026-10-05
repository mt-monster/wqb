# WQ BRAIN Skills 阶段展开 · 价值评估 · 模拟演练

> 生成时间：2026-10-01 | 审阅对象：`wq-brain-ra-pipeline`（九步主链 + 步 5b）及其支撑 skill 层
> 数据来源：`data/wqb.db` 只读快照 + skill 文档（`$HOME/.workbuddy/skills/wq-brain-ra-pipeline/`）
> 演练方式：**只读模拟**，未执行任何写库 / 提交 / 派发仿真动作

---

## 0. 范围界定与阅读说明

**"阶段"的口径**：本项目 40+ 个 skill 中，只有 `wq-brain-ra-pipeline` 定义了完整的**阶段化流水线**。其余 skill 是它在不同阶段调用的**能力件**（生成器、门禁、评审器、提交器）。因此本文以九步主链为骨架展开，在每个阶段内标注"调用了哪个 skill / 工具"，这样既覆盖全部阶段，又不把 40 个 skill 平铺成流水账。

**一句话定位**：`ra-pipeline` = when/what（编排），`campaign-matrix` = where（选区选集），`campaign-toolkit` = how（战役目录内执行引擎）。三者是同一条链的三段，不是三套流程。

**价值评估的判据**（先立标准，再打分，避免事后归因）：

| 判据 | 说明 | 权重倾向 |
|---|---|---|
| **A. 防不可逆损失** | 挡住提交错误 / 误判死 / 配额烧光这类**无法撤回**的后果 | 最高 |
| **B. 零成本前置** | 本地、秒级、不耗平台配额就能拦截 | 高 |
| **C. 有量化实证** | 文档里记载了具体数字收益（不是"应该有用"） | 高 |
| **D. 有代码执行** | 是机检（删了测试会红），还是纯文档准则（靠人自觉） | 中高 |
| **E. 无重叠** | 与别的闸 / 步骤是否判同一件事 | 中 |
| **F. 有读写双方** | 台账是否有写入方**和**读取方；孤儿即空转 | 中 |

评级：★★★ 保留并深化 · ★★ 保留维持 · ★ 精简/降级可选 · ✕ 删除或合并

---

## 1. 阶段总览

| 步 | 阶段 | 一句话目的 | 成本 | 评级 |
|---|---|---|---|---|
| 1 | S-PRE | 决定"先清库存还是开新挖"，并排除跨区死路 | 本地为主 | ★★★ |
| 2 | S0 | 选数据集白名单（点塔均匀 + 死路已排除） | 本地 + 少量平台 | ★★★ |
| 3 | S1 | 字段扫描 / 结构体检 / 语义归类 | 本地 + S1 扫描 | ★★★ |
| 4 | S2 | 概念优先生成表达式并选波 | LLM（有配额/费用） | ★★★ |
| 5 | S2→S3 | 门禁：在烧配额前拦下坏式与同质批 | 本地零配额 | ★★★ |
| 5b | S3 收批后 | prod-first 探针：先知道撞不撞 prod 墙 | 1 次平台实测 | ★★★ |
| 6 | S3 | 并发回测 | **最贵**：平台配额 | ★★ |
| 7 | S4 | 诊断：这一波候选下一步去哪 | 本地 + 相关性 | ★★★ |
| 8 | S4→S5 | 稳健闸 + 提交判定（**不执行提交**） | 平台实测 | ★★★ |
| 9 | S6 | 复盘回写，让下一波先验自动变新 | 本地 | ★★★ |

---

## 2. 逐阶段详细展开

### 步 1（S-PRE）查表与库存分流

**输入**
- `$REGION`（用户必填）+ 区域 profile（`entry_verdict`: active / probe-only / frozen）
- 账户内已回测的存量 alpha（IS 快照）

**处理过程（顺序即执行顺序）**
1. **读 profile**：`frozen` → 本步即拒，不进步 2（唯一后门写在 profile 里）
2. **库存盘点**（全流程最大分流点）
   ```
   tools/build_gate_prior_from_inventory.py --regions all --emit-candidates ... --write-priors
   tools/select_ra_basket.py cache/candidates.json --target 20 --out cache/basket.json
   ```
   资格门口径 = `Failed RA == 0`（比"无 FAIL"严格，WARNING/ERROR 也计）；`compute_mutual_correlation` 本地先去同族冗余与 OS 撞车
3. **查表**：`get_campaign_summary` / `get_dead_ends` / `get_dead_datasets` / `get_mining_yield`
4. **跨区死路**（必做）：`get_dead_ends` 不传 region + `get_cross_region_lessons` + `s0-select` 的 `[跨区弱]` 标记
5. **PPA 主题门禁**（仅含 PPA 分支）：实时重扫公告，**禁止复用 settings 快照**

**输出**
- 分流结论：篮子条数 ≥ target **且**覆盖 ≥ 3 座未点亮塔 → **跳步 7/8**；否则进步 2，只补缺口塔
- `settings.json`（universe / delay / 中性化 / 排除集 / 排除信号族）

**关键判据**：`conversion`（已回测/已生成）低 = **流水线**问题（修管道，别换区）；`yield_rate`（达标/已回测）低 = **标的**问题（换区换集，别加生成量）。两者不能混。

---

### 步 2（S0）数据集体检 + 金字塔配置

**输入**：步 1 分流为"进步 2"；`settings.json` 已有 universe/delay

**处理过程（有序，不可先锁白名单再读约束）**
| # | 动作 | 说明 |
|---|---|---|
| ① | `campaign_intel.py s0-select` | `recommend_datasets` × `get_mining_yield` × `get_dead_datasets` 三方交叉 |
| ② | `workflow_campaign(S0, calibrate=true)` | 反学 category 权重 + 拥挤甜区 → 写 `thresholds.json`，**不产排名** |
| ③ | `workflow_campaign(S0)` | 按新阈值产出 `s0_ranking`（②③ 都要，③ 非冗余） |
| ④ | 硬约束 0–7 筛 | 已点亮塔剔除、≥2 个非 MODEL、`*_dead` 排除… |
| ⑤ | `upsert_ledger_key("s0_whitelist", mode="merge")` | **禁整值覆盖**（2026-09-25 事故） |
| ⑥ | 体检包核对 | 白名单集须有 `field_inspect_<region>_<ds>.json` |

**输出**：ledger `s0_ranking` / `s0_whitelist` / `s0_calibrate_<region>`

**硬约束要点**：约束 0（已点亮塔不进白名单）与约束 1（win 族必进候选）冲突时**以 0 为准**。

---

### 步 3（S1）字段扫描 · 结构体检 · 语义归类

**输入**：步 2 白名单数据集

**处理过程**
1. `workflow_campaign(stage="S1", dataset=$DS)` → `fields` 表 + ledger `catalog_<ds>` / `s1_prefix_<ds>`
2. **铁律 ① 字段级覆盖审计**：`catalog_<ds>` 覆盖为空 → 写 `<ds>_dead` 防复用（`recommend_datasets` 不校验区域覆盖率）
3. **铁律 ② 验活幽灵字段**：新字段先 `create_multi_simulation(validate_fields=true)`——DB 有记录但平台报 unknown variable，提交层直接 COMPILE_ERROR
4. **闸 SEM**：`tools/field_semantic_classify.py --write-ledger`（本地、零配额、秒级、GEM 之前必做）
5. 字段分级：`users ≥ 50` 只做方向验证不打磨；`10–49` 进候选但提交前必实测 prod；`0–9` 优先

**输出**：`fields` 表 + ledger `catalog_<ds>` / `s1_prefix_<ds>` / `s1_semantic_<ds>`

**完成定义**：`catalog_<ds>` 里 coverage > 0 的字段数 ≥ 10，且 `s1_semantic_<ds>` 已写

**为什么 SEM 不可省**：KOR/fundamental17 首波跳过语义归类 → 348 条产物里 **49.4%** 落在货币代码 / 汇率叉乘这类非信号字段上（语法全对、语义全废，语法闸和 `gate.py` 都拦不住）。

---

### 步 4（S2）概念优先生成 + 选波

**输入**：步 3 完成；priors（`wins` ≤ 6 / `dead_ends` ≤ 12）；有胜绩则本波 ≥ 2 个位按机制换腿

**处理过程**
1. `workflow_campaign(S2, subcommand="assemble-priors")` → 写 DB 快照 `priors_snapshot_<region>`
2. **取骨架前必查** `ghost_operator_advisory`（幽灵算子如 sigmoid / ts_entropy / ts_median）
3. `workflow_gem(region, dataset_id, delay, universe, data_type, pipeline_mode="phased")`
4. `workflow_campaign(S2, dataset, wave)` → build-wave：去重 / 分桶 / 骨架配给（**不产表达式**）
5. 生成侧预闸自动修：`hump` 命名参数、`bucket` 补 range、非法 group 字段丢弃、窗口别名归一、同骨架封顶 12

**输出**：`expressions`（status `gem`/`enhanced`/`selected`）、ledger idea、`priors_snapshot_<region>`

**完成定义（硬）**：`list_expressions` 查到本波条目——**未验证 DB 有表达式，不得声称步 4 成功**

**四种选波情景**：A 普通探索 / B 预定实验（配对，需 `selection_w<W>` 契约）/ C 重建 / D 结果解读

---

### 步 5（S2→S3）门禁

**输入**：本波表达式已入库；含 VECTOR 字段先 `preflight_expressions(auto_fix_vector=true)`

**处理过程（一条路径）**
```
# ① 幽灵算子硬闸（本地、零配额，先拦）
tools/campaign_intel.py ghost-audit --region $R --exprs-file <txt>
# ①b 形状配额体检（只读、不入闸链）
tools/shape_quota_check.py --region $R --wave $W
# ② 每波门禁一键落盘
tools/wave_gate.py --campaign-dir tracking/$R --dataset $DS --wave $W --from-db
```

**闸清单**（执行点不同，粒度不同）：
- 语法 / 算子元数 / 字段白名单 / 区域非法 group / 类型（VECTOR 包裹）/ **毒模式（禁混信号加和）** / 批级多样性
- **闸 SEM**：缺 `s1_semantic_<ds>` → **exit 2 整波阻断**；命中黑名单字段的表达式直接剔出
- **闸 PF**：命中已死骨架 → 拦整波；新骨架 / 小样本 / 混合骨架 → 只 WARN
- **体检硬门**：低覆盖需 `ts_backfill`、高偏度需 `rank`/`winsorize`、稀疏事件需 `trade_when`
- 开波区域闸：signal_floor / stop_rules / backlog / catalog

**输出**：`gate_results`（`all_pass` / `fail_reasons`）

**完成定义**：`get_gate_result` 有本波记录且 `all_pass=1`（脚本崩溃 = ERROR 终态、退出码 2，**不是 FAIL**）

**为什么不能省**：整批 CANCELLED 连坐（一条坏式 ERROR 取消全部 8 条兄弟）。两个假绿要警惕：**干跑绿不证明 LLM 可达**、**体检包缺失时体检门不生效**。

---

### 步 5b prod-first 探针（S3 收批后必调）

**输入**：本波 `backtest_results`（族内最强 1 条，`--top-k` 缺省 3 个族）

**处理**：`tools/campaign_intel.py prod-first --region $R --wave $W --write-ledger`（平台实测、**串行**、只读）

**输出**：族级 `EXPAND` / `STOP`；`alphas.prod_correlation`；ledger `prod_first_<wave>`

**处置唯一表 = D0-P**（不接受区域改写）：

| 首探 prod | 动作 |
|---|---|
| < 0.60 | 正常扩变体，进步 7–8 |
| 0.60–0.70 | **不扩变体，当天进步 8**（外部同款 1 小时可把 prod 堵到 1.0） |
| 0.70–0.75 | 只允许 **1 次**结构性尝试（删腿/换广度轴 或 `group_neutralize` 包裹） |
| ≥ 0.75 或尝试失败 | 家族记 `dead_end`：先 `forum_recon` → `seal_dead_end` |

**红线**：**禁止用 `POST /submit` 探测 prod**（通过即提交，无撤回）

---

### 步 6（S3）并发回测

**输入**：步 5 `all_pass=1`；波内表达式

**处理**
- 入口：`workflow_batch_track`（先过三道开波闸，异步返回 `task_id`）→ `workflow_task_status` 跟踪
- 并发锁定为 `min(7, 批数)`，外部传非 7 只收 warning
- **设置层先验**（默认开）：`by_decay`/`by_neutralization` 里样本 ≥30 且过闸率 ≥ 当前 ×2 → 自动改写本波设置
- **连坐隔离已自动化**：定位真正报错的坏式 → 其余无辜表达式优先重发一次
- **QUICK/FULL**：QUICK 无 correlation/theme 检查，**产物不可提交**，必须 FULL 复测

**输出**：`backtest_results` / `wave_results` 暂定结论 / `salvage_pool`

**完成定义**：全部 multisim 到终态，且 `backtest_results` 行数 = 波内表达式数（含 ERROR/CANCELLED 标记行）

**故障处置原则**：**先归因再决定**重发/跳过/拆批——确定性 ERROR 重发只会烧配额

---

### 步 7（S4）诊断改进

**顺序**：S3 收批 → ① prod-first → ② s4-prescreen → ③ review_wave → ④ 逐候选链

| 段 | 输入 | 输出 | 关键价值 |
|---|---|---|---|
| ① prod-first | 本波回测 | 族级 EXPAND/STOP | 防整族报废 |
| ② prescreen | alpha_id 清单 | READY/REVIEW/REJECT | **8 条从 8 次评审压成 1 次预筛 + 仅存活者进链（约 8×）** |
| ③ review_wave | 本波 alpha_id | 墙/near/salvage + `expOS` 列 | 定去向 |
| ④ 逐候选链 | 通过者 | 稳健/相关性/评审结论 | 提交前终检 |

**墙的判据**
- `RN_EXPOSURE`：`risk_neutralized_sharpe ≤ rn_sharpe_min` → 不进候选，也**不进 near/salvage/组合腿**
  - 且 raw sharpe ≥ 1.58 → **停止调参**（它本身就是因子暴露，调参只会让暴露更纯）→ 想法级 dead_end
- `ROBUST_STRUCTURAL`：robust/limit < 0.5 → 不入 near（否则全灭波记成 PARTIAL，停止规则 B 永不触发）

**组合形态铁律**：禁止任何两条独立信号腿的加和（加权/**等权**/`add`/中缀 `+`）。允许清单只有一份（单信号结构、同源价差、换算子几何、事件门控、换概念、SA combo、协动对象 `ts_corr`）。**门禁通过 ≠ 合规**——判据是本质不是语法。

**辅助腿入场三式**：(a) 条件 `trade_when`【实证最强】/ (b) 分组 `group_rank`+`bucket`【不能破 prod 墙】/ (c) 中性化残差【证据弱】

**SUB 比值律**（提交层）：`LOW_SUB_UNIVERSE_SHARPE` 的 limit ≈ **0.571 × 本 alpha sharpe**。推论：**把 sharpe 压到刚过线会同步降低 SUB 要求**——"sharpe 越高越好"在提交层是错的。

---

### 步 8（S4→S5）稳健闸与提交判定（**本步不执行提交**）

**有序检查清单，任一步说"不"就停**

1. **资格门**：`Failed RA == 0`
2. `submit_verdict`（**否决权威**：exit 1 BLOCKED / 10 UNVERIFIABLE / 11 ALREADY_SUBMITTED）
3. prod 实测 `check_correlation(refresh=True)` < 0.7
4. **用户明确确认**
5. 才可 `workflow_submit_alpha(confirm_submit=True)`（**不可逆**，单独调用）

**输出**：候选清单 + 每条证据（资格门 / verdict 退出码 / prod 值）交用户

**完成定义**：用户确认后提交，`get_alpha_details` → `status == ACTIVE` 且 `dateSubmitted` 非空

**红线**
- `UNVERIFIABLE` **不是放行**
- `PASS_CHEAP` 只代表过了 IS 廉价闸，**绝不等于可提交**
- **没有零成本的 POST 探测**（通过即提交）
- 同日：prod 0.60–0.70 的候选**当天**请用户确认，不先做变体

---

### 步 9（S6）复盘回写

**有序流程（编号即执行顺序）**

| # | 动作 | 产物 |
|---|---|---|
| ① | `tools/step_funnel.py --region $R` | 瓶颈定位（只读推导） |
| ② | 判 verdict：PASS（≥1 条过全部评审闸）/ PARTIAL（0 达标但 ≥1 near）/ FAIL（0 达标 0 near） | 枚举值 |
| ③ | `campaign_intel.py pyramid` | 点塔进度行 |
| ④ | `upsert_wave_result`（③ 行与其它 findings **一次带齐**） | `wave_results.verdict` = **唯一结论源** |
| ⑤ | 判死 `seal_dead_end` / 胜绩 `upsert_registry_empirical(layer="win")` | `registry_empirical` |
| ⑥ | 全波撞 prod 墙 → `mark-saturated` | ledger `saturated_datasets` |
| ⑦ | 逐数据集 `dataset-experience` | `reports/dataset_experience/*_campain.md` |
| ⑧ | 再跑 `assemble-priors` | `priors_snapshot_<region>` 刷新 |

**判死取证闸（fail-closed，最高价值之一）**

| 传入的 `forum_recon` | 判死 |
|---|---|
| `found=false` + ledger 有可靠负结果 | ✅ 允许 |
| `found=true` 或最新是"有货" | ❌ 拒绝（转 salvage/Mode B） |
| `found=null`/`status=error` | ❌ 拒绝——**工具故障 = 未取证，故障 ≠ 论坛无解** |
| 缺失或缺 `question_key` | ❌ 拒绝 |

**为什么必须 fail-closed**：判死是**永久**封存。2026-09-29 实证 5 条 recon 记录里 **2 条是工具故障**，被记成 `found=false` → 等于"工具坏了 ≡ 论坛无解"→ 误把活路判死。

---

## 3. 价值评估总表

### 3.1 ★★★ 核心保留并深化

| 项 | 所在步 | 评判依据 |
|---|---|---|
| **库存盘点优先** | 1 | **C**：2026-09-07 实证——会话前半段跨四区 170 次新回测产出 0 条可提交 RA；后半段一次库存扫描产出 **20 条**。A+B：本地、零配额 |
| **跨区死路检查** | 1 | **C**：KOR 选 risk70 跑完 114 条回测才发现 IND/GLB 早已判死。本次演练**仍抓到 risk70 在白名单内**（详见 §4） |
| **闸 SEM（语义归类）** | 3 | **C+D**：49.4% 非信号字段实证；代码 fail-closed（删闸测试即红）；**B**：本地秒级 |
| **ghost-audit 幽灵算子硬闸** | 5 | **B+C**：本地零配额；含幽灵算子整批 CANCELLED 连坐。`validate_expressions` **不查**幽灵算子（对 `ts_median` 返回 valid=true），所以必须显式跑 |
| **prod-first 探针 + D0-P** | 5b | **A+C**：IND intraday_pv_feats 连投 3 波 24 条后才查 prod（0.79–0.92）→ 整族报废。统一 6 套矛盾处置为一张表 |
| **判死取证 fail-closed** | 9 | **A+C**：判死永久不可逆；实证 5 条 recon 里 2 条是工具故障却被当"论坛无解" |
| **提交前用户确认 + fail-closed** | 8 | **A**：提交不可逆，且没有零成本探测。红线不可豁免 |
| **RN_EXPOSURE 墙** | 7 | **C+D**：HKG w4 七条里六条 RN 在 −0.33~−0.57 而 raw 非零；w3 的 `O0roWEM7`（RN 0.96≈raw 1.17）是约 150 次回测中唯一真信号 |
| **SUB 比值律** | 7/8 | **C**：三处独立一致（1.03/1.80、1.12/1.96、0.89/1.55 ≈ 0.571）。**破除"sharpe 越高越好"的错误直觉**，这是认知层面的收益 |
| **连坐隔离自动化** | 6 | **C**：JPN w7/w8 一条坏式连坐，10 批丢 8 批 64 条 |
| **prescreen 预筛** | 7 | **C**：约 8× 效率（8 条从 8 次评审压成 1 次预筛 + 存活者进链） |
| **assemble-priors 刷新** | 4/9 | **F**：有写有读；GBR 实测快照落后 8 天 → 本波结论不回流。步 9 第 ⑧ 步兜底 |

### 3.2 ★★ 保留维持（有价值但有条件）

| 项 | 所在步 | 评判依据 |
|---|---|---|
| S0 三方交叉选集 | 2 | **D+C**：`recommend_datasets` 真实点塔 × 历史产出率 × 判死清单；但 `recommend_datasets` **不校验区域覆盖率**，需铁律①兜底 |
| calibrate ②③ 双调用 | 2 | 文档已澄清"③ 非冗余"（② 写阈值不产排名，③ 按新阈值产排名）。**保留但需靠文档防误删** |
| typed catalog + 两条铁律 | 3 | **D**：缺目录 stage_gate 直接 FAIL；铁律② 防提交层 COMPILE_ERROR |
| GEM 概念优先生成 | 4 | **C**：反"每个字段套 rank"退化；但**依赖 LLM 通道**，402 余额不足会伪装成"no meta.json" |
| 批级多样性闸 6 | 5 | **D**：唯一执行口径 `gate.py:check_batch_diversity`；60%/2/3 是经验值 |
| 体检硬门 | 5 | **D**：五条判据明确；但**缺包时不生效**（默认 `warn` 放行），新数据集首波才自动升 `enforce` |
| 开波四道闸 | 循环 | **B+D**：零配额、干跑也走；但 CLI 直调有**日期豁免**（2026-10-11 前只告警） |
| IS→OS 衰减基线 | 7 | **C（反向价值）**：Spearman 秩相关仅 +0.086，各桶存活率平坦 70–80%。它的价值是**防止被误用**（不抬高 IS 阈值、不作排序依据），而非提供正向排序 |

### 3.3 ★ 精简 / 降级为可选

| 项 | 所在步 | 评判依据 | 建议 |
|---|---|---|---|
| `workflow_feature_engineering` 深查 | 3 | **E+C**：产出是**确定性模板渲染**（非 LLM 推理），注入 GEM 会让 GEM 一行 LLM 都不调、整波退化为模板展开（GBR 实证）。已禁注入、已非必做 | 明确降级为"人读参考"，不进主链检查项 |
| **形状配额 `shape_quota_check`** | 4/5 | **E**：**不入闸链**，与闸 6 判据不同（通过一个不代表通过另一个），两套口径并行 | 合并进闸 6 的多样性判据，或明确为"人可读体检"并停掉退出码语义 |
| `structural_reconstruct` | 7 | **C**：实测仅 1 行产出 | 已降为实验性；建议从推荐路径移除 |
| `brain-explain-alphas` | 7 | 文档已标"按需，非每候选必经" | 维持按需 |
| PPA 主题门禁 | 1 | **情境性**：仅含 PPA 分支时执行；且 PPA 与 RA 是两条独立配额通道 | 维持分支，不进主链 |
| `diversity-extract` | 4 | 文档标"可选，不替代 GEM，不强制先行" | 维持可选 |

### 3.4 ✕ 建议删除 / 合并 / 补接（空转与死重）

| 项 | 所在步 | 问题 | 建议 |
|---|---|---|---|
| **五张 `step_*` / `*_summary` 表** | 9 | **F**：**恒 0 行且不应填充**（自动采集是 TODO 空壳）。文档明令"不要往那五张表写" | 删表或移除 schema，避免误以为有数据 |
| **`seat_model` 台账** | 2 | **F**：`docs/ledger_keys.json` 登记为 **orphan**，无写入方；缺省每集按 2 座位估是**占位值不是实测** | 接写入方或删键 |
| **`template_kb`（validated/failed）** | 9 | **F**：orphan，**无脚本写入方**，靠人工维护 | 接写入方或删键 |
| **"语义字段重排回 GEM 字段池"**（`s2_field_pool_<ds>`） | 3 | **F+风险**：**没有任何命令实现**，纯人工约定；文档自承"最容易被绕过的一处" | 要么实现，要么从文档删除（留着会让人误以为有安全网） |
| **OS 表现监控与重着色** | 9 | **F**：**没有承接者**（旧脚本已归档，`sync_platform_alphas.py` 只同步基线不重着色） | 已登记为声明-实现缺口；应明确补接责任人或正式关闭 |
| **`s0_whitelist` 与 `s0_whitelist_v2` 并存** | 2 | **F+风险**：KOR ledger 实测两键并存（`s0_whitelist` 7257B / `s0_whitelist_v2` 27295B）。文档有 `normalize` 归一，但两键并存是分叉源 | 合并为一键，v2 若已废弃则归档 |
| **CLI 日期豁免（2026-10-11 前只告警）** | 循环 | **风险**：CLI 直调与 workflow 节点口径不一致（节点一律拦截） | 到期后清理该分支，统一口径 |

---

## 4. 完整流程模拟演练（只读，未做任何修改）

**演练设定**：在 **KOR** 开新一波 `w202`（delay=1 / universe=TOP600）。所有数字取自 `data/wqb.db` 只读快照。

### 演练前置：KOR 真实基线

| 指标 | 实测值 | 来源 |
|---|---|---|
| expressions 总量 | 1975（dropped 1239 / gem 261 / backtested 208 / pending 143 / superseded 88 / fail 15 / gated 13 / selected 8） | `expressions` |
| **unconsumed**（gem+selected+pending+gated） | **425 / 1975 = 21.5%** | 计算 |
| **conversion**（已回测/已生成） | **208 / 1975 = 10.53%** | 计算 |
| backtest_results 行数 | 467（max\|sharpe\| = 2.37） | `backtest_results` |
| registry_empirical | dead_end 77 / campaign 26 / win 9 / orphan 6 | `registry_empirical` |
| `*_dead` 数据集键 | 16 个（model109/model170/news79/sentiment21/shortinterest3/…） | `ledger_kv` |
| submit_ready 队列（⚠ 2026-10-01 修正：须按 status 拆开，总数含墓碑） | KOR 共 40 行 = DEAD 24 + SUBMITTED 10 + SUPERSEDED 5 + PROD_BLOCKED 1 → **READY=0**；IND 共 132 行 = DEAD 85 + SUBMITTED 22 + EXPIRED 13 + PROD_BLOCKED 9 + SUPERSEDED 3 → **READY=0** | `submit_ready` |
| 最近 8 波 verdict | w201 PASS / w197 PASS / w196 PASS / w195 PASS / w184·183·182·179 PARTIAL | `wave_results` |
| 各集回测量 top | analyst10 105（max 1.62）/ analyst44 42（1.78）/ other466 28（**2.37**）/ risk71 16（2.20） | `backtest_results` |

⚠ **演练中顺带发现的数据一致性问题**：`backtest_results` 467 行 vs `expressions.status='backtested'` 208 条，两者差 259。步 6 完成定义是"行数 = 波内表达式数"，口径分叉会让完成定义无法核验。建议作为独立问题核查。

---

### 步 1（S-PRE）演练

**输入**：`$REGION=KOR`；profile `entry_verdict` 假设为 active（未 frozen，可继续）

**处理 → 输出**

| 动作 | 模拟结果 | 价值判断 |
|---|---|---|
| ① 库存盘点 | ⚠ 修正：`submit_ready` 是**全生命周期台账**，KOR 40 行里 READY=**0**（DEAD 24 / SUBMITTED 10 / SUPERSEDED 5 / PROD_BLOCKED 1）→ **数量关就不过，分流失败，进步 2**。（初版误把含墓碑的总数当活体库存）且 READY 行也非可提交——篮子须经 select_ra_basket 四道处理 + 塔覆盖核验 | ★★★（分流逻辑本身；本区当前无库存可用） |
| ② 覆盖塔数核验 | 需查平台 `get_pyramid_alphas`。KOR 已点亮 = analyst6/fundamental3/model4/other6/pv3 → 若篮子 40 条集中在这 5 座**已点亮**塔 → **覆盖未点亮塔 < 3** | ★★★（这一步决定跳不跳 7/8，**不能省**） |
| ③ 查表 | KOR dead_end **77** 条、win **9** 条 → 先验充足 | ★★ |
| ④ **跨区死路** | **命中**：`IND-RISK70-NO-SIGNAL`（IND）+ `GLB-RISK70-STYLE-HF-MINVOL1M-FASTKILL`（GLB）+ `ASI-...RSK70-CORRGATE-WEAK`（ASI，弱）→ **risk70 属跨区死族（≥2 区独立复现）→ 应排除** | ★★★ **本次演练的最高价值产出** |
| ⑤ conversion 读法 | 10.53% > 10% → backlog 闸不拦；unconsumed 21.5% < 30% → 只报不拦。但**两项都逼近阈值** | ★★ |

**步 1 输出**：分流 = 进步 2（篮子覆盖未点亮塔不足 3 座）；**排除集追加 `risk70`**；只补缺口塔

> **价值判断结论**：跨区死路这一步在本次演练中**立刻抓到一个尚未付出成本的漏洞**——`risk70` 当前**就在 KOR 的 `s0_whitelist` 里**（见步 2），而 KOR 在 risk70 上**已回测 0 条**（`n=0`）。现在排除的沉没成本为零；若不查，按步 2 生成的波次会重演 KOR 114 条的教训。**这是"零成本前置拦截"的教科书案例 → 保留并深化。**

---

### 步 2（S0）演练

**输入**：步 1 排除集（含 risk70）；`settings.json` = TOP600 / delay 1

**处理 → 输出**

| 动作 | 模拟结果 | 价值判断 |
|---|---|---|
| ① `s0-select` | 三方交叉；需剔除 `lit=Y`（已点亮：analyst/fundamental/model/other/pv）与 16 个 `*_dead` | ★★★ |
| ② `calibrate=true` | 反学 category 权重 → 写 `thresholds.json`。**审两处异常**：甜区 `ac` 是否异常巨大、`strong_acs` 是否为空 | ★★（异常则**不要 apply**，先查 `ac` 来源） |
| ③ 打分 | 产出 `s0_ranking` | ★★ |
| ④ 硬约束筛 | **约束 0**：已点亮塔剔除 → fundamental* 类需复核<br>**约束 4**：16 个 `*_dead` 排除<br>**跨区死族**：**risk70 剔除** | ★★★ |
| ⑤ 锁白名单 | **现行白名单**（generated_at 2026-09-28T17:40）= `["fundamental17", "risk70", "fundamental6", "risk68", "insiders1"]` → **修订为移除 risk70** | ★★★ |
| ⑥ 体检包 | 需 `ls tracking/mining/field_inspect_kor_*.json` 核对 | ★★ |

**发现的第二个问题（白名单与实际挖掘脱节）**：

KOR 实际回测量 top 是 `analyst10`(105) / `analyst44`(42) / `other466`(28，max S **2.37**) / `risk71`(16，2.20)，而现行白名单 5 集里**一个都不在其中**。同时 KOR 在 risk70 上回测 **0 条**——说明白名单自 09-28 锁定后基本未被消费，或消费走了旁路。

若白名单确实未被遵守（硬约束 5：**白名单外禁止 generate/simulate**，闸 2 执行），那 209 条 off-whitelist 回测是**违规产出**；若白名单仅是 stale，则它已失去指导意义。

> **价值判断结论**：`s0-select` 三方交叉 + 硬约束筛 ★★★ 保留；但**白名单与实际执行的对齐需要一次审计**——否则步 2 的全部产出（ranking/calibrate/whitelist）都是空转，这是典型的"有写入方、无消费方"。

---

### 步 3（S1）演练

**输入**：修订后白名单（以 `fundamental17` 为例，白名单内 `field_count=373, coverage=0.8896, platform_alpha_count=3328, lit=false, need_to_light=2`）

**处理 → 输出**

| 动作 | 模拟结果 | 价值判断 |
|---|---|---|
| `workflow_campaign(S1)` | 产出 `fields` + `catalog_fundamental17` / `s1_prefix_fundamental17` | ★★★ |
| 铁律① 覆盖审计 | coverage 0.8896 ≠ 空 → **不写 `_dead`** | ★★★（防"只信 `recommend_datasets` 选到空集"） |
| 铁律② 验活 | 新字段先 `validate_fields=true` 单探针 | ★★★（防提交层 COMPILE_ERROR） |
| **闸 SEM** | `field_semantic_classify.py --write-ledger` → `s1_semantic_fundamental17`。373 字段中按黑名单口径剔除货币/汇率/标识符/分类码… | ★★★（不做的代价：49.4% 产物落在非信号字段） |
| 字段分级 | `users` 0–9 优先；冷门字段占批次预算 ≥ 50% | ★★ |
| `workflow_feature_engineering` | **跳过**（确定性渲染，禁止注入 GEM） | ★ 降级可选 |

**完成定义核验**：coverage>0 字段数 373 ≥ 10 ✅；`s1_semantic_<ds>` 已写 ✅

---

### 步 4（S2）演练

**输入**：白名单 + `priors_snapshot_KOR`；本波若 KOR 有 win（9 条）→ **≥2 个位按机制换腿**

**处理 → 输出**

| 动作 | 模拟结果 | 价值判断 |
|---|---|---|
| `assemble-priors` | wins ≤6 / dead_ends ≤12（从 77 条倒序取）→ 写快照 | ★★★ |
| 查 `ghost_operator_advisory` | 取 KB 骨架前必做 | ★★★ |
| `workflow_gem(phased)` | 产表达式 → `expressions` status `gem` | ★★★ |
| `build-wave` | 去重/分桶/骨架配给 → 波号 `w202` | ★★★ |
| 同骨架封顶 | 12/骨架；触顶 = 机制枯竭信号 → `forum_recon` | ★★ |
| `shape_quota_check` | ≥3 形状族、`trade_when` ≤40%；**退出码 1 不产生 gate_results** | ★（与闸 6 双口径，建议合并） |

**完成定义核验**：须 `list_expressions` 查到 `w202` 的 gem/selected 条目——**未验证 DB 不得声称成功**

**风险提示**：KOR 现存 `gem` 261 + `pending` 143 + `gated` 13 = **417 条未消费**。在这些存量被消化前再生成新表达式，会把 unconsumed 从 21.5% 推向 30% 的告警线。

---

### 步 5（S2→S3）演练

**处理 → 输出**

| 动作 | 模拟结果 | 价值判断 |
|---|---|---|
| ① `ghost-audit` | 本地零配额，命中则隔离到独立小批 | ★★★ |
| ①b `shape_quota_check` | 只读体检 | ★ |
| ② `wave_gate.py --from-db` | 语法/字段/类型/毒模式/闸6/SEM/体检/PF/区域闸 → `gate_results` | ★★★ |
| **闸 PF** | 查本区 `prod_family_KOR_<骨架指纹>`：同骨架 ≥3 条实测且 prod ≥0.7 → 拦整波 | ★★★ |

**完成定义核验**：`get_gate_result(KOR, w202, $DS)` 有记录且 `all_pass=1`

⚠ **演练中发现的第三个问题**：KOR `gate_results` 最近 5 条全部是 `wave='mcp_direct_*'` 且 `dataset='mcp_direct'`（all_pass=1）。这说明**近期的门禁记录走的不是正规战役波通道**——用 `mcp_direct` 作 dataset 占位会让"哪个数据集过了哪一波门禁"无法追溯，步 9 的按数据集回写与 `stop_rules` 的 region×dataset 轴计数都会失效（**轴推不出来 → 回落旧口径**）。

> **价值判断结论**：门禁本体 ★★★；但**产物标识不规范会反向架空依赖它的下游闸**（步 9 / 停止规则 B1 的 dataset 轴）。建议对 `mcp_direct` 类记录做一次归因清理。

---

### 步 5b prod-first 演练

**输入**：`w202` 族内最强 1 条（top-k=3 个族）

**处理 → 输出**：`check_correlation` 只读实测 → 假设首探 **prod = 0.66**

**D0-P 查表**：0.66 落在 **0.60–0.70** → **不扩变体，当天进步 8**（提交前仍须 `refresh=True` 终验）

> **价值判断结论**：★★★ 保留。反事实：若不做 prod-first 而直接扩变体，按 IND pv103 实证（1 小时内外部同款把 prod 从 0.6997 顶到 1.0000），整族会被封死。**这一步用 1 次实测换掉整波的沉没成本。**

---

### 步 6（S3）演练

**输入**：`w202` 通过门禁的表达式（假设 24 条 = 3 批 × 8）

**处理 → 输出**

| 动作 | 模拟结果 | 价值判断 |
|---|---|---|
| 三道开波闸 | catalog ✅ / signal_floor（KOR 最近两波 max\|S\|：w196/w197 PASS → 不拦）/ stop_rules（最近 3 波非连续 FAIL → B1 不触发） | ★★★ |
| `workflow_batch_track` | 并发 `min(7, 3)`；异步返回 task_id | ★★ |
| 设置先验 | 若 `by_decay` 某格样本 ≥30 且过闸率 ≥ 当前 ×2 → 自动改写并打印 `[settings-prior]` | ★★（GBR 实证 decay 14 28.3% vs decay 4 3.9%） |
| 连坐隔离 | 坏式 → `status='fail'`，无辜者优先重发一次 | ★★★ |
| 模式 | 必须 FULL（QUICK 产物不可提交） | ★★★ |

**完成定义核验**：`backtest_results` 行数 = 24（含 ERROR/CANCELLED 标记行）

**演练后状态推演**：+24 条 → backtested 232 / 1999 = **11.6%**（conversion 改善）；unconsumed 425/1999 = 21.3%

---

### 步 7（S4）演练

**输入**：24 条回测结果（假设 best：sharpe 1.72 / fitness 1.31 / 2Y 1.61 / turnover 0.08）

**处理 → 输出**

| 段 | 模拟结果 | 价值判断 |
|---|---|---|
| ① prod-first | 已在 5b 做（prod 0.66 → STOP 扩变体） | ★★★ |
| ② prescreen | 24 条 → 假设 5 READY / 7 REVIEW / 12 REJECT → **仅 12 条进评审链**（约 2× 压缩） | ★★★ |
| ③ review_wave | 逐条判墙：假设 3 条 `RN_EXPOSURE`（RN ≤0）、2 条 `ROBUST_STRUCTURAL`（robust/limit<0.5）→ 均**不入 near/salvage** | ★★★ |
| ④ 逐候选链 | 存活者：selfcorr-quick → `check_self_correlation` → `compute_mutual_correlation` → `check_correlation` → robustness → judge | ★★★ |
| SUB 比值律 | 若 sharpe=1.72 → SUB 需 ≥ 0.98（=1.72×0.571）。假设实测 SUB=1.05 → **比值 0.61 ✅** | ★★★ |
| IS→OS 衰减 | `expOS = 1.72 × 0.358 ≈ 0.62` → **仅作期望值参考，不抬高 IS 阈值、不用于排序** | ★★（反向价值） |

**输出**：本波每条候选都有去向 → 1 条进步 8 / 4 条 near / 2 条 salvage（带墙名）/ 17 条判死或留观

---

### 步 8（S4→S5）演练

**输入**：1 条达标候选 `alpha_id = <模拟>`

**有序检查清单 → 输出**

| # | 检查 | 模拟结果 | 价值判断 |
|---|---|---|---|
| ① | 资格门 `Failed RA == 0` | 假设 0 ✅ | ★★★ |
| ② | `submit_verdict` | exit 0（未 BLOCKED） | ★★★（**只有否决权，放不了行**） |
| ③ | `check_correlation(refresh=True)` | prod 0.66 < 0.7 ✅ | ★★★ |
| ④ | **用户明确确认** | **演练在此停止**——不模拟确认 | ★★★ **红线** |
| ⑤ | `workflow_submit_alpha(confirm_submit=True)` | **不执行**（演练约定） | ★★★ 不可逆 |

**同期约束**：REGULAR 配额 4/ET 日。⚠ 修正：KOR `submit_ready` 的 **READY=0**（40 行全是 DEAD/SUBMITTED 等终态墓碑），**当前没有库存积压可清**——L.4 的"清库存优先"分支不触发。（初版误按总数 40 判断；IND 同理 132 行里 READY=0，DEAD 高达 85——那是高流失坟场，不是可清库存。）

> **价值判断结论**：★★★ 保留且不可简化。整条链里唯一不可逆的动作被三重闸门 + 用户确认包住；且文档明确**没有零成本 POST 探测**（`PASS_CHEAP ≠ 可提交`、`UNVERIFIABLE ≠ 放行`）。

---

### 步 9（S6）演练

**输入**：步 7 去向 + 步 8 结论

**有序流程 → 输出**

| # | 动作 | 模拟结果 | 价值判断 |
|---|---|---|---|
| ① | `step_funnel` | 定位瓶颈：KOR unconsumed 21.5% / conversion 10.53% → 瓶颈在 **S2→S3**（生成远超回测吞吐） | ★★★（**用数据而非印象写 verdict**） |
| ② | 判 verdict | 有 1 条过全部评审闸 → **PASS**（KOR 最近 4 波 w195/196/197/201 均 PASS，本波延续） | ★★★ |
| ③ | `campaign_intel.py pyramid` | 取 `[key_findings]` 单行（点塔进度） | ★★ |
| ④ | `upsert_wave_result` | **③ 行与其它 findings 一次带齐**（整列替换语义）；verdict=PASS，status=closed | ★★★ |
| ⑤ | 判死/胜绩 | 假设判死 1 族 → **先取证**：传 `question_key`，闸 fail-closed 核对（若 recon 记录是 `error` → **拒绝判死**）；胜绩 1 条 → `upsert_registry_empirical(layer="win")`，**只记"信号概念+设置"，不记混合比例** | ★★★ **最高价值** |
| ⑥ | `mark-saturated` | 本波非全族撞 prod 墙 → 跳过 | ★★（条件触发） |
| ⑦ | `dataset-experience` | 对**本波每个实际回测的数据集**逐个生成（不是只对判死/win 集） | ★★ |
| ⑧ | `assemble-priors` | 刷新 `priors_snapshot_KOR`，确保不早于本次回写 | ★★★（防 GBR 式落后 8 天） |

**完成定义核验（缺一 = 本波未完成）**：wave_results 有记录 ✅ / key_findings 含点塔行+prod-first ✅ / dead_end 已封存 ✅ / win 已写 ✅ / 本波非全撞墙故 mark-saturated n/a ✅ / dataset-experience ✅ / assemble-priors 已再跑 ✅

---

## 5. 演练结论汇总

### 5.1 三个在演练中暴露的真实问题（按严重度）

| # | 问题 | 证据 | 影响 | 建议 |
|---|---|---|---|---|
| **P1** | **跨区死族 `risk70` 仍在 KOR 白名单内** | 白名单 `s0_whitelist` 含 risk70（09-28）；`IND-RISK70-NO-SIGNAL` + `GLB-RISK70-...-FASTKILL` 判死；ASI 弱 | KOR 在 risk70 上**已回测 0 条** → 现在排除**零沉没成本**；不排除将重演 114 条浪费 | 立即从白名单移除（走 `mode="merge"`） |
| **P2** | **白名单与实际挖掘严重脱节** | 白名单 5 集 vs 实际回测 top（analyst10 105 / analyst44 42 / other466 28）无一重合 | 硬约束 5"白名单外禁止 simulate"（闸 2）若生效 → 209 条 off-whitelist 回测违规；若不生效 → 步 2 产出空转 | 审计白名单是否被消费；二选一修正 |
| **P3** | **`gate_results` 被 `mcp_direct` 占位污染** | KOR 最近 5 条 gate_results 全为 `dataset='mcp_direct'` | 步 9 按数据集回写、`stop_rules` B1 的 region×dataset 轴**推不出来** → 回落旧口径 | 归因清理 `mcp_direct` 记录 |

附带发现（供独立核查）：`backtest_results` 467 行 vs `expressions.status='backtested'` 208 条，口径分叉 259；`s0_whitelist` 与 `s0_whitelist_v2` 两键并存。

### 5.2 价值评估一句话总结

- **最该保留深化**的：一切**零成本前置拦截**（跨区死路 / 闸 SEM / ghost-audit / prod-first）与一切**不可逆动作的守门**（判死取证 fail-closed / 提交前用户确认）。它们的共同点是：**用一次廉价检查换掉整波或永久性的沉没成本**。
- **最该精简**的：三类空转——**孤儿台账**（`seat_model`、`template_kb`、`s2_field_pool`）、**恒空表**（五张 `step_*`）、**双口径体检**（`shape_quota_check` 与闸 6 并行却互不通气）。
- **最该警惕**的：文档里"**有声明无实现**"的条目。它们比明文的缺口更危险，因为读的人会以为有安全网（典型：`s2_field_pool_<ds>` 文档自承"最容易被绕过的一处就是这里"）。

---

## 5.3 补充核查：步 1「读 profile」的更新机制（用户提问引发）

### 结论先行

**profile 既没有自动更新机制，也没有新鲜度守护。** 这不是推测，是四重实证：

| # | 查证项 | 结果 |
|---|---|---|
| 1 | 有没有工具**写** profile | **0 个**。全仓 `tools/*.py` 里只有 `region_status.py` / `index_tables.py` **读** `references/regions/*.md`，无写入方 |
| 2 | 契约怎么说的 | `region-profile-contract.md` §2：「其余区域**在下次被编辑时随手整理**」——等于承认靠人碰巧，无机制 |
| 3 | 有没有新鲜度测试 | **有测试，但双重不覆盖**（详见下表） |
| 4 | 实际有多旧 | **8/13 个停在 2026-08-25（37 天前）**，含本次演练用的 KOR |

### 唯一的新鲜度测试为什么不覆盖 region profile（双重失效）

`tests/unit/07_docs_skills/test_docs_consistency.py:437` 的 `test_last_verified_not_older_than_last_commit`：

```python
def _skill_md_files() -> list[Path]:
    return sorted(p for p in SKILLS_DIR.glob("*/SKILL.md"))   # ① 只取各 skill 顶层 SKILL.md

m = re.search(r"^last_verified:\s*(\d{4}-\d{2}-\d{2})", text, re.M)  # ② 要求行首无缩进
```

- **① 范围不含**：`references/regions/*.md` 不在 `*/SKILL.md` 的 glob 里 → 参数化根本没这些文件
- **② 正则不认**：即使纳入，profile 的 `last_verified` 是 `empirical_anchor:` 下**缩进 2 空格**的 `  last_verified: 2026-08-25`，`^last_verified:` 匹配不到 → 会直接报"缺 last_verified"

→ **region profile 的 `last_verified` 处于零守护状态**。

### 现状快照（as_of 2026-10-01）

| last_verified | 区域 | 龄期 |
|---|---|---|
| 2026-09-29 | IND、USA | 2 天 |
| 2026-09-28 | AMR | 3 天 |
| 2026-09-15 | JPN | 16 天 |
| 2026-09-11 | DEU | 20 天 |
| 2026-08-26 | GBR | 36 天 |
| **2026-08-25** | **ASI、CHN、EUR、GLB、HKG、KOR、MEA、TWN** | **37 天** |

这正是契约 §3 **自己警告过的失效模式**：「旧版 13 个 profile 里一半是同一天的批量戳（2026-08-25），掩盖了正文已被 09-19 用户定案改写而 front-matter 没跟上」。**契约写了警告，但现象到今天仍在。**

### 会不会影响正确性？——要分键看，不是一刀切

判断依据是契约 §1 的「谁读」列，这决定了过期后果的严重度：

| 键 | 谁读 | 过期后果 | 严重度 |
|---|---|---|---|
| **`entry_verdict`** | **代码**：`region_rotation.py`（`_VERDICT_MULT` 乘数、`frozen` 直接排除）、`region_status.py:_entry_verdict` 正则 `^entry_verdict:` | **机器判定直接错**：frozen 区被漏挖 / unknown 降权到 0.35 / 该拒的没拒 | **高** |
| `priors` | **代码**：`assemble_priors._profile_fallback`，**仅 DB KB 为空时兜底** | 只影响新区/空 KB；KOR 这类 KB 满的区不触发 | 中低 |
| `gate_overrides` / `loop_policy` / `datasets` / 正文 | **文档**（agent 读了照办，代码不消费） | 靠人自觉，错了无闸拦 | 中 |

**所以准确的说法是**：profile 过期**不会**让流水线崩溃，但会让**唯一被代码消费的那个键（`entry_verdict`）成为静默错误源**——它不报错、不告警，只是安静地给出一个过期的准入结论。这比崩溃更危险。

### 与 P1 的咬合：KOR 是最该先修的那个

KOR profile `last_verified: 2026-08-25`，而它是 **active + 挖得最深（wave 95+）+ 本次演练用的区**。对照看：

- 正文写「评级修正 × SH 混合已产 2 颗 ACTIVE」、`datasets.green: [analyst 系, insiders, pv]` → **green 里没有 `other466`**，而 other466 是 KOR max\|S\| = **2.37** 的来源（出过 `wpZkk1Mp` / `A1NXddRw`）
- 正文 `loop_policy.fast_kill` 明写：「新数据集 8 探针无 \|S\|≥0.5 即判死回写，**不扩批（小宇宙烧不起配额）**」

这就和 P1 咬合了：profile 自己写着「烧不起配额、8 探针即判死」，而 `risk70` 在 IND/GLB 已判死、ASI 弱。**若 profile 是新鲜的，risk70 本不该出现在白名单里**。白名单 09-28 生成时读到的是一个 37 天未核对的 profile——P1 不是孤立的手误，是这个缺口的 downstream 症状。

### 修复建议（按投入产出排序）

1. **把 region profile 纳入新鲜度测试**：`_skill_md_files()` 增加 `references/regions/*.md`，正则放宽为 `^\s*last_verified:`。
   ⚠ **一改就会红 8 个**（37 天前的那批）。契约明令「不要放宽断言」→ 正确顺序是**先人工复核这 8 个 profile、bump 戳，再上测试**，否则会重演「批量机械刷新」被禁止的那一幕。
2. **给 profile 接一个更新钩子**：步 9 回写时，若本波新增 win / dead_end 与 profile 的 `datasets.green` / `red` 冲突 → 提示刷新 profile。把 profile 从静态文档接回流水线，才治本。
3. **优先修 KOR**：active + 最深 + 37 天未核 + 已暴露 P1。

> 注：本轮只做只读核查，**未修改任何 profile / 测试**。第 1 项会使全量测试转红 8 处，属需你决策的改动，故未动手。

---

## 6. 附：演练未覆盖的分支

以下分支在本次演练中被跳过（非 RA 主链或条件未触发），评估时不应据此认为"不存在"：

- **PPA 分支**（步 1 主题门禁、独立配额 1/ET 日、web UI 交接）
- **SuperAlpha 分支**（KOR ACTIVE REGULAR ≥10 时 `sa_probe` → GO）
- **hypothesis-first 路由**（数据集 alphaCount ≥1 万或连续 2 波模板全灭时切换）
- **QUICK 模式探针**（产物不可提交，须 FULL 复测）
- **`forum_recon` 取证触发**（表 #1–#4；波级默认取证已落地）

---

## 7. 落地记录：profile 精确化与漂移钩子（2026-10-01 已实施）

针对 §5.3 暴露的「profile 无更新机制」缺口，用户定案走治本路线（步 9 回写钩子）。已落地：

### 7.1 改了什么

| 文件 | 变更 |
|---|---|
| `src/wqb/region_profile.py`（新） | profile front-matter **唯一解析器**（收口此前 4 套简易解析；不依赖 PyYAML，支持嵌套 map / inline+block list / dict 项 / 行尾注释） |
| `src/wqb/profile_drift.py`（新） | 漂移检测核心：profile green/red 精确层 ↔ DB 实证的**集合运算**；两档死亡证据严格分开（ledger `*_dead` 整集判死 = high 级判据；registry dead_end 的 payload.dataset 族级死 = medium） |
| `wqb_db_mcp.py` | `upsert_registry_empirical` 挂钩子：`layer ∈ {win, dead_end}` 写入成功后自动跑漂移检查，报告幂等落 ledger `profile_drift`，摘要随返回值带出；**fail-open 不阻断回写** |
| `tools/profile_drift_check.py`（新） | 全区体检 CLI（`--all` / `--json` / `--write-ledger`；high>0 退出码 1） |
| `tools/migrate_profile_datasets.py`（新） | 一次性迁移工具（不留兼容层） |
| 14 个 profile | `datasets.green/red` 全部迁移为结构化形态：精确层只放实证绑定（red ← ledger `*_dead` ∪ 旧文本 id；green ← win 层绑定），族级原文保留为 `scope: family` |
| `tests/unit/01_store_db/test_profile_drift.py`（新） | 24 条：解析器（含 14 个真实 profile 全量可解析）+ 集合判定 + 钩子触发/fail-open |
| `docs/ledger_keys.json` | 登记 `profile_drift` 键（78 条） |
| `region-profile-contract.md` §5 | 机制契约与判据表指针（判据唯一来源 = `profile_drift.py` docstring） |

### 7.2 迁移即发现

- **DEU**：`analyst44` 同时在旧 green 与 ledger 判死清单 → 判死胜出，已从 green 移除
- **IND**：`pv106` 旧 red 文本判死 vs registry win 层胜绩（`IND-PV106-COST-FRAGILITY-WIN`）→ 保守留 red，漂移检查持续挂 HIGH 待人工裁定
- **JPN**：旧 green 10 项仅 6 项落在本区 datasets 表（其余 4 项转族级，疑似同步缺口）

迁移后全区体检：14 区 high 级冲突仅 1 处（IND pv106，即上述已知张力）。

### 7.3 设计要点（为什么这样判）

- **族死 ≠ 整集死**：GBR 初版把 registry 族级判死抬成 HIGH 会一次报 6 处假冲突（如 `GBR-INST6-HOLDINGS-CEILING` 只是 holdings 族死，institutions6 整集未死）。分档后 GBR 归零 HIGH，信噪比成立。
- **不补绑的条目永远停在 advisory 层**：registry 存量 win/dead_end 大量缺 `payload.dataset`（KOR 55 条 / IND 71 条）——检查只会计数提示，不猜。精确层的覆盖度随新回写补齐而单调上升。
- **`last_verified` 不自动 bump**：迁移只重核了 datasets 块，正文未通读——契约 §3 禁批量刷新的规则不变，stale 提示持续存在直到人工复核。

### 7.4 回归

受影响套件 665 passed / 3 failed——3 个失败经 `git stash` 验证全部为并行会话存量（`submit_queue` 行为变更、gem NodeMeta 漂移），与本次无关。`tools/sync_skills.py` 已同步 4 安装位（KOR/契约/step9 抽查一致）。

### 7.5 机制首次裁决行动（2026-10-01 晚，"按最佳方案决策推进"）

**IND pv106 red∩win 张力 → 裁决落地**。读全实证后确认 pv106 整集"既没全死也没全活"：
- 活的一族 = 成本分布形状（transaction_cost max/median 尾部脆弱度，win `Wj7YP5JN` S=1.85/prod 0.3051 全闸 PASS；且 `IND-TOP500-CEILING` dead_end 实为引用该 win 的自我纠正条目）
- 死的数族 = spread/slippage 水平值（09-17 "do not probe"）+ 流动性冲击族（w188 八探针 max\|S\| 1.01 + CW）
- 无 ledger `pv106_dead` → 无整集判死

**裁决：pv106 两边精确层都不进，拆成两条族级条目**（red 族级记死族、green 族级记活族并标注该 win 的 add 加权架构属禁止形态须换合规结构）。正文"pv106 判死"的过时表述同步修正。裁决后 IND 漂移 HIGH 清零（残留 1 条 medium `win_not_listed` 属诚实棘轮：族级认领不构成整集绿）。

**KOR 白名单 P1 → 真相比评估更深并已修复**：`s0_whitelist_v2` 的 `supersedes` 显示旧 5 集（fundamental17/risk70/fundamental6/risk68/insiders1）**经跨区死路检查后早已全部淘汰**（fnd17 六区死、risk70 三区死等），但修正写进了**零代码读取、未登记的平行键**，注册为 active 的 canonical 键 `s0_whitelist` 仍留整份淘汰名单且标"主攻（wave 2）"。已通过 MCP `upsert_ledger_key`（read-modify-write，旧值留 `_legacy` 可回滚）将 canonical 键回写为跨区检查后可挖集 `[other466, fundamental31, model56, other395, other106]`，v2 键标 `_deprecated` 并保留其 blocked 清单供审计。**全区漂移复检：high 级冲突 14 区归零。**

遗留（诚实标注）：① KOR profile 的 `datasets.red` 精确层仍未含 risk70——risk70 的死证在**跨区**（IND/GLB/ASI），本机制查的是本区实证；跨区死族 → 白名单的拦截是步 1 §1.4 的职责，已在本次白名单修正中落实，profile 红榜增补属内容复核（下次人工通读时一并做）。② 塔点亮状态随时间变（KOR fundamental 在 09-28 后新增 ACTIVE），白名单 `_doc` 已注明下次 S0 必须 `get_pyramid_alphas` 复核。

---

## 8. 步 1 五步序列的评估（2026-10-01 晚，用户提问引发）

**结论：顺序骨架合理，不重排；发现一处数据流断流（已补文档，代码补丁待议）。**

评估标准 = 短路成本梯度 × 依赖关系 × 分叉价值。

| 位次 | 步骤 | 评判 |
|---|---|---|
| ① 读 profile | ✅ 零成本一票否决，必须最先 |
| ② 库存盘点 | ✅ 价值优先于成本：篮子够格时 ③④ 直接失去意义（判死约束新挖、不约束已有 alpha） |
| ③④ 查表 / 跨区死路 | ✅ 本地秒级，步 2 排除集输入 |
| ⑤ PPA 主题门禁 | ✅ 条件分支放最后；实时重扫公告防复用快照 |

**P1 断流（实证 + 已修复）**：`select_ra_basket.py` 零引用 dead/saturated/registry——② 选篮子不吃 ③④ 的判死产物。后果：「IS 过闸但所属族已撞 prod 墙判死」的候选会带进篮子，烧完步 7 诊断链到步 8 才被挡。**这是数据流问题不是顺序问题**（提前 ③④ 会破坏篮子的短路价值）。

修复（2026-10-01 晚落地，用户确认"默认走到才落地"）：核实到 workflow `inventory_scan` 节点以**固定命令行**调 `select_ra_basket`（不传任何标志），故排除做成**默认开启 + opt-out**（`--exclude-dead` 默认 True / `--no-exclude-dead` 仅调试），CLI 与节点两条路径都自动生效。规则与 `wqb.profile_drift.dead_dataset_index` 同源：候选字段经 `fields` 表回填数据集名（region 作用域），命中整集判死 ∪ 饱和 → 剔除；族级死保留但计数；查不到归属 fail-open 保留。回归 `tests/unit/01_store_db/test_select_ra_basket_exclude_dead.py`（4 条，含「默认开启」钉死防退回 opt-in）。

**P2 口径钉死（本会话事故直接固化）**：「篮子条数」= select_ra_basket 四道处理后的产物条数，**严禁用 submit_ready 队列行数代替**（该表是全生命周期台账，READY=0 时按总数会得出反向结论）。已写入 `step1-inventory.md` §1.2。

**P3 配额检查**：不动——配额只闸提交不闸挖掘，「配额耗尽挂起提交」已在步 8 前置，位置正确。
**P4 PPA 分支位次**：可选（低频），现状代价小。

---

## 9. 步 2（S0）逻辑评估（2026-10-01 晚，用户提问引发）

**在做什么**：回答「这一仗打哪几个数据集」——三源交叉（平台点塔 × 历史产出率 × 判死清单）→ calibrate 反学权重 → 打分产 `s0_ranking` → 硬约束 0–7 筛 → merge 锁白名单 → 体检包核对。

**结论：设计判断成立**（多源防偏见 / 点塔战略与信号强度分榜 / 硬-准则分层），**但本会话实证暴露两个结构缺口**：

- **失效点 A（写入侧）**：硬约束 4 的 `*_dead` 排除只查本区台账。KOR 白名单（09-28）rationale「KOR dead_end 台账零命中」= region 作用域查询，违反步 1 §1.4 跨区必查 → 跨三区死族 risk70 标着「主攻（wave 2）」进名单；而做过跨区检查的修正被写进零读取方的 `s0_whitelist_v2` 孤儿键。**跨区检查做了，但做在了没人读的地方。**
- **失效点 B（消费侧）**：白名单锁定后无对账——名单 5 集与实际回测 top 零重合；闸 2「白名单外禁 simulate」存在但无人审计名单是否被消费/已腐烂。

**优化方案（已落地，2026-10-01 晚）**：在 `upsert_ledger_key` 对 `s0_whitelist` 的写路径上挂了**非阻断守卫**——写完后自动把 datasets 与判死证据求交，命中即在返回值带 `dead_intersection`（本区整集死/饱和/跨区 ≥2 区 = high，1 区 = medium，族级死 = low；fail-open 不阻断写入）。跨区证据走两路：`payload.dataset` 干净绑定 + `entry_id` 词元精确匹配（补「只写 family 文本没绑 dataset」的召回缺口——risk70 正是靠词元匹配从 medium 抬回 high）。实现：`wqb.profile_drift.whitelist_dead_intersection` + `wqb_db_mcp._whitelist_dead_guard`；回归 `tests/unit/01_store_db/test_whitelist_write_guard.py`（5 条，含非阻断与 fail-open）。

**真实数据端到端验证**：09-28 旧名单（含 risk70）过守卫 → 4 high + 1 medium（fundamental17 四区死 / fundamental6+insiders1 两区死 / risk70 两区死）；今天修正后的新名单 → 全干净零命中。失效点 B（消费侧对账）留给 `tools/profile_drift_check.py` 后续加项。受影响套件 667 passed / 3 failed（全是 stash 验证过的并行会话存量）；安装位已同步并抽查。

---

## 10. 步 3（S1）原理评估与断流修复（2026-10-01 深夜，用户提问引发）

**在做什么**：步 3 被写成一个阶段，实际回答**三个互不替代的问题**，用三种成本递增的工具：

| 问题 | 回答者 | 成本 | 产物 |
|---|---|---|---|
| ① 这字段是什么类型 / 覆盖多少？ | `workflow_campaign S1` 平台扫描 | 网络往返 | `fields` 表 + `catalog_<ds>` |
| ② 这个集**能不能挖**？ | D13 结构体检 + `field_inspect` 包 | 本地 + 一次探针仿真 | 预处理约束 |
| ③ 这个字段**能不能当信号**？ | `field_semantic_classify` 语义归类 | 本地·零配额·秒级 | `s1_semantic_<ds>` |

**设计原理成立的证据**：①② 都回答不了语义——`currency_code` 在 ① 里类型对、覆盖 100%；在 ② 里结构无异常；只有 ③ 说它是恒等式。KOR/fundamental17 首波跳过 ③ 直接生成 348 条，**49.4%** 落在货币代码 / 汇率叉乘上而黑名单字段仅占全集 **9.9%**（37/373）——**用 0.5 秒本地脚本换掉 49.4% 无效仿真**，这是全步最高投入产出比。分层（语法→结构→语义、越贵越后跑）合理。

### 10.1 实测发现三处断流（比文档描述的更严重）

1. **生成侧完全不读语义台账（结构性错配）**：`gem.py:346` / `_field_catalog.py` 的建池逻辑不消费 `s1_semantic_<ds>`。实测 `IND/insiders1` 的字段池含 **`transaction_currency_code` + `insd1_gvkey`**（池 9 个字段里 2 个是垃圾，22.2%）——非信号字段照样进表达式，直到步 5 闸 SEM 才被剔，生成配额已烧掉。文档 `step3-s1-semantic.md` 自认「最容易被绕过的一处就是这里」。
2. **语义台账覆盖率仅 4.7%（文档未记）**：实测全库 catalog **697** 个 vs `s1_semantic` **33** 个；EUR/IND/GLB/JPN 全为 **0**，GBR 6.1%、USA 9.0%、KOR 14.8%。⇒ 闸 SEM 的 fail-closed 在多数区域只能靠**阻断**生效，而非**过滤**；一旦 waiver 放行，非信号字段全线裸奔。
3. **`s2_field_pool` 有消费但非语义池**：`run_pipeline.py:894-911` 确实读 `s2_field_pool`（155 个，12 区），2026-09-26「消费一致性修复」真实生效。但池的构建源（经济大类分簇 / 主体 token 分簇）**都不过语义黑名单**。文档「没有任何命令实现」已过时——缺口是「语义→池」这条边，不是「池→GEM」这条边。

**体检包反而是好消息**：文档 `field_inspect_gate.py` 头记载「现存两份且 fields 全为空」（2026-09-06），实测 **501 个包 / 79186 字段 / 空包仅 2 个**（最大 `usa_analyst_consensus` 3424 字段）。数据供给已跟上，缺包默认 `warn` + 新集首波自动升 `enforce`（`gates_inspect.py:37-41`）策略正确。

### 10.2 落地修复（用户「按最佳方案推进决策落地」，2026-10-01 深夜）

**止血 A——字段池消费语义台账**（`campaign.py` + `_field_catalog.py`）：
- 新增 `CampaignStore._drop_semantic_blocked(region, dataset, fields)`：读 `s1_semantic_<ds>.blocked_fields` 剔除非信号字段，返回 `(fields, meta)`。
- 接入两条建池路径：`build_economic_field_pool`（首选）与 `build_candidate_field_pool`（回退）——**回退路径也必须过滤**，否则经济学池不可用时过滤被静默绕过。
- payload 带 `semantic_filter: {ledger, blocked_n, dropped_n, dropped}` 元数据（可诊断）。
- **fail-open 是契约定的一部分**：台账缺失 / 解析失败 / 空黑名单 → 原样返回，不阻断生成（过滤是减负，不是新把关点；把关在步 5 闸 SEM）。
- **`POOL_BUILDER_VERSION` 3→4**：这是**内容**变化不是算法变化，v3 旧池含垃圾字段（实测 IND/insiders1），不升版本则旧池继续被 GEM 消费、过滤形同虚设。

**通气 B——S1 默认附带语义归类**（`workflow/nodes/campaign.py`）：
- 新增 `_semantic_coverage_check(region, dataset)`：S1 跑完检查 `s1_semantic_<ds>`，缺则自动调 `field_semantic_classify.py --write-ledger`（本地零配额秒级），已有则跳过；干跑输出 plan 不执行。
- 让「跑 S1」=「typed catalog + 语义归类」一次做完，把语义归类从**人工记忆的可选动作**变成 **S1 默认产物**，直击 4.7% 覆盖率。
- fail-open：脚本失败只记 warning，不阻断 S1。

**A 依赖 B**：`semantic_filter.ledger=False` 的地方过滤不生效——必须先把该集语义台账跑出来。两者互补，缺一不可。

### 10.3 验证

- 新增回归：`tests/unit/01_store_db/test_semantic_field_pool_filter.py`（7 条：剔除 / 回退路径 / 缺台账 fail-open / 空黑名单 / 损坏 JSON / helper 契约 / 版本护栏）+ `tests/unit/02_workflow/test_s1_semantic_autoclassify.py`（6 条：已有跳过 / 旧版无 families 提示 / 缺台账触发 / 失败 fail-open / 异常 fail-open / 无 ds 空操作）。**13 条全绿**。
- **真实数据端到端**：`IND/insiders1` 实跑语义归类 → 识别 `insd1_gvkey`(标识符) + `transaction_currency_code`(币种码) 为非信号（22.2%）；池过滤前 9 字段 → 过滤后 7 字段，`dropped=[insd1_gvkey, transaction_currency_code]`。
- 版本护栏实测：v3 旧池读取返回 `None`（强制重建）。
- 顺带修复并行会话遗留的 `gem` NodeMeta 漂移（`dataset_ids` 漏登记，`audit_node_registration.py` 五处审计现全绿）。
- 受影响套件：`01_store_db + 02_workflow` 632 passed / 2 failed（stash 验证过是并行会话存量：`test_submit_queue_gates.py` 的 PROD_BLOCKED 语义）；`skill_integrity + workflow + mcp 节点` 135 passed。
- 文档已同步 `step3-s1-semantic.md` §3.5/§3.6（断流表改写为「已修复 + 两处生成侧消费」）；安装位 4 个位置抽查命中。

### 10.4 步 3 价值评估总表

| 环节 | 价值 | 判据 |
|---|---|---|
| ① typed catalog + 闸 TRI | **高，保留** | 阻断有牙（exit 2）；TRI 台账 13 区域已预生成；拦掉打在已证伪集上的 49% 无效回测 |
| ② D13 结构体检 | **中高，保留** | 拦**结构性死路**（伪白空间 / 稀疏事件），回测前最后的零成本拦截；但检查项是人工清单，无工具强制 |
| ② field_inspect 包 | **中高，保留并加厚** | 数据已就绪（501 包 / 79186 字段）；缺包默认 warn 是唯一遗憾，首波自动 enforce 补上 |
| ③ 语义归类（闸 SEM） | **最高，落地最弱→已修** | 单点收益最大（49.4%）但覆盖率 4.7%、生成侧不消费；本次 A+B 修复后接通 |
| `workflow_feature_engineering` 深查 | **低，仅人读** | 确定性模板渲染、无 LLM；注入 GEM 会让整波退化（GBR 实证）。文档已禁注入，正确 |
| 字段分级风险筛查（users 阈值） | **中，保留** | ≥50 只做方向验证、0–9 优先；prod-corr 规避的**事前**手段，成本为零 |

**剩余诚实缺口**：语义覆盖率的提升依赖每次 S1 实跑（B 只在 `workflow_campaign(stage="S1")` 路径生效，不走 CLI 直调 `scan_fields.py`）。

**（已补）批处理入口**：`field_semantic_classify.py` 已加 `--all`（只跑「有 catalog 键 ∧ `fields` 表有行 ∧ 未判死」的活跃集，顺带滤掉 249 个 `cache_*` 幽灵键）。历史欠账已清：**覆盖 33 → 414 台账（4.7% → 100% 活跃集）**，13 区跑完 0 失败。见 §10.5。

### 10.5 清欠账时实测揪出的真 bug：标识符正则裸子串误杀 733 字段

- **症状**：`--all` 全量跑完后按区抽检，发现 `DEU/JPN pattern_scores` 的 `blocked` 数量异常高，且被拦字段名里根本没有标识符字样。
- **根因**：标识符黑名单正则用的是**裸子串** `isin`，而 `rising_wedge` 里 r+`isin`+g 恰好包含 `isin` → 被判为「标识符/国别交易所代码」。
- **影响面**：`pattern_scores`（52 集 × 6 区）+ `analyst_revision_horizons`（76 集 × 5 区）共 **733 个正当信号字段被误杀**，直接后果是这些字段永远进不了 GEM 字段池。
- **修复**：正则改为 **token 锚定** `(?:^|_)(?:gvkey|cusip|isin|sedol|ticker)(?:$|_)`（须落在 `_` 边界或串首尾才算命中）。
- **复验**：`--force` 重跑全 13 区，非信号字段总数 **2171 → 1435（剔除 736 误杀，与估算 733 吻合）**；抽检 `DEU/JPN pattern_scores` blocked=0 / signal=504、`IND/model238_anlrev` blocked=0。
- **同族教训**：文件自己在 2026-09-28 已因 `is_` / `indicator` 误伤过一次 —— **凡「短 token 可能藏在长单词里」的规则，一律必须 token 锚定，不能用裸子串。**
- **回归护栏**：`tests/unit/09_core/test_field_semantic_classify.py` 新增 2 条 —— `test_identifier_rules_are_token_anchored_not_substring`（`rising_wedge` 不被误杀）+ `test_true_identifiers_still_blocked_after_anchoring`（gvkey/isin/ticker/cusip/sedol/iso 仍被拦）。

---

## 11. 步 4（S2）机制评估与缺陷诊断（2026-10-01 深夜，用户提问引发）

> 本节为**只读评估**，未做任何代码修改。所有结论均有代码行号或 DB 实数支撑。

### 11.1 步 4 的运行机制（拆成 4 个动作）

| # | 动作 | 实现锚点 | 性质 |
|---|---|---|---|
| 4-A | **组装先验** `assemble-priors` | `nodes/campaign.py:316-328` → `campaign.py assemble-priors` | 本地 KB→priors 文件 + DB 快照，**零配额、不开波、不受开波闸约束** |
| 4-B | **概念优先生成** `workflow_gem` | `nodes/gem.py` 全文件 | 调 `brain-make-some-gem` 的 `headless_runner/run.py`，LLM 按 priors+ideas 生成表达式 |
| 4-C | **质量预估 + prod 预筛** | `gem.py:1014-1059`（`_run_quality_estimation` / `_run_prod_first_prescreen`） | 零配额预检；`qp` 预估 + 字段族级 prod-corr 前置 |
| 4-D | **选波** `build_wave` | `nodes/campaign.py:329-379` → `build_wave.py`（1159 行） | 从 DB 的 `gem`/`enhanced` 状态行里按配额挑出本波 `selected` |

**4-B 生成管道**（`pipeline_mode` 自动识别，`gem.py:52-123`）：字段数 <50 → `single`；可分层 → `skeleton`；>100 或需族级叙事 → `phased`（缺省）。`phased` 三阶段：structure→mapping→render，`batch_size=100` 防拆散同族。**关键输入**：`_resolve_ideas_from_ledger`（S1 ledger 注入 ideas，模板渲染文档**主动不注入**防退化）+ `_load_field_context`（字段池：经济学归类池优先，`cross_cluster` 回退）。

**4-D 选波核心**（`build_wave.py:863-918`）：轮转分桶抽样，五重配额 —— ① 总量 `--size` ② 每桶 `--per-bucket` ③ `linear_mix` 骨架 cap ④ **每族 `max(2, size//6)`** ⑤ `econ_option` 族 cap `size//8`；外加 `--max-field-repeat` 字段重复上限。

### 11.2 评估结论：机制设计合理，但有 **3 个真实断流**

#### 断流 ① 【最严重】选波的「族维度」在 DB 路径上**完全失效**

- **证据链（三层铁证）**：
  1. `build_wave.py:852` `family_map = load_family_map(a.file, a.meta_file)`；而 `--from-db` 路径下 `a.file=None`（`--file` 是「已废弃」参数），`--meta-file` 缺省 `None`（`:443`）→ `load_family_map` 的两个候选路径都空 → **返回 `{}`**。
  2. `family_map={}` ⇒ `build_wave.py:897` `family_map.get(norm_expr(e))` 恒为 `None` ⇒ `fam_key=None`（`:907`）⇒ **族封顶分支 `:901-905` 永不进入**。
  3. DB 实测：`expressions` 表**没有 family 列**（列清单：…`bucket`/`skeleton`/… 无 family）；15650 条 `gem` 行里 **`bucket` 非空 0/15650、`skeleton` 非空 15650/15650**；`settings_json` 含 family 的 0 条。
- **后果**：库里 15650 条 gem 候选，选波时**族配额形同虚设**，只靠 `bucket_key(expr)` 算子树分桶兜底。「从族出发、每族限量」这条步 4 的核心纪律，在 `--from-db` 主路径上**没有任何代码保证**。
- **注**：2026-09-18 的修复（`:866-873`）只解决了「无标签被误当 unknown 而截断波」的 bug（结果是**放行**），但**没有解决 family 标签本身的来源问题** —— 修复后是「正确地不封顶」，而不是「正确地按族封顶」。

#### 断流 ② 「探针先于扩批」**无机检**

- **证据**：`atom_flag` 列存在但 **gem 15650 条 / selected 856 条 / backtested 6357 条，`atom_flag=1` 全为 0**。`build_wave.py` 里搜不到任何 `probe`/`探针`/`atom_flag` 的选波逻辑（仅 `--qp-keep` 的「校准探针」是另一回事）。
- **后果**：步 4 完成定义明文要求「探针先于扩批」，但**选波层完全无法区分探针条与扩批条** —— 全靠操盘手自律，无代码兜底。

#### 断流 ③ 「概念优先」的落点仍偏软

- **证据**：`_load_field_context`（`gem.py:306-381`）给 GEM 的是**字段池**（economics 归类池 → cross_cluster 回退），priors 经 `--priors-from-db` 注入 prompt（`run_pipeline.py:198`）。**字段池只到「经济学归类」粒度，未带「信号形态/族假设」**（即 L3.5/L4 产物不进字段池）。
- **后果**：「概念优先」实质靠 LLM 读 priors 自由发挥 + 字段池约束；步 3 刚打通的语义台账（`s1_semantic_<ds>`）在**本次 A 修复后**已能过滤字段池，但**族/形态级假设仍未结构化传给 GEM**。

### 11.3 合理性判定

| 维度 | 判定 | 说明 |
|---|---|---|
| 4-A 组装先验 | **合理** | 零配额、缓存（ledger `assemble-priors` 缓存）、干跑也走，边界清晰 |
| 4-B 概念优先生成 | **基本合理** | `pipeline_mode` 自动识别、同族同批、防模板退化（不注入模板文档）都对；缺口是字段池粒度不到族 |
| 4-C 质量预估 + prod 预筛 | **合理且高价值** | prod-corr 从 S4 前置到 S2，实测可省 80% 回测配额；`mode_b_required` 触发 Mode B 闭环 |
| 4-D 选波 | **⚠ 设计合理、实现断流** | 五重配额的**意图**完全正确，但族配额/探针纪律两条**在主路径上失效** |

**总评**：步 4 的**设计意图**（概念优先、从族出发、探针先于扩批、五位配额）是整条 pipeline 里最成熟的一段；问题**不在设计而在实现**——设计所依赖的「family 标签」这个数据契约**在 DB 路径上从未建立**，于是最核心的两条纪律（族封顶、探针优先）**静默降级为摆设**。

### 11.4 优化建议（按 ROI 排序）

| 优先级 | 建议 | 依据 | 成本 | 状态 |
|---|---|---|---|---|
| **P0** | **把 family 标签落库**：GEM 产出时把 `final_expressions_meta.json` 的 `expr→family` 写进 `expressions` 表（新增列或写 `settings_json.family`）；`build_wave --from-db` 从 DB 读 family_map | 断流①：族配额现在 100% 失效，是最有价值的选波约束 | 中 | **✅ 已落地**（见 §11.6） |
| **P1** | **给探针装机检**：该族「全库尚无已回测行」→ 本波该族 cap 收紧为 1（探针）；有回测行则扩批 | 断流②：完成定义的硬要求现在无代码支撑 | 中 | **✅ 已落地** |
| **P2** | **字段池带上族结构**：把 L3.5 族注入 `s2_field_pool_<ds>` 的 `families` 段，供 GEM 概念优先消费 | 断流③：让「概念优先」从 LLM 自由发挥变成按族结构生成 | 中 | **✅ 已落地** |
| **P3** | `--from-db` 显式告警：`family_map` 为空但库里有 family 数据时打 WARN，防静默降级 | 防回归 | 低 | **✅ 已落地** |

### 11.5 需澄清的一点（避免误判）

本节的「族配额失效」结论基于 **`--from-db` 路径**（步 4 主路径）。若走 `--file <final_expressions.json>`（旧路径，已标「废弃」），同目录有 `final_expressions_meta.json` 时 family_map 能载入 —— 但**步 4 的 SKILL 命令走的就是 `--from-db`**（`campaign.py:376` `cmd.append("--from-db")`），故主路径断流成立。

### 11.6 落地记录：P0–P3 已全部实施（2026-10-01 深夜，用户批准）

| # | 改动 | 文件 | 关键点 |
|---|---|---|---|
| **P0** | `expressions` 加 `family` 列（幂等 ALTER） | `src/wqb/store/_expressions.py` | SQL 按「atom_ready × family_ready」拼装；UPDATE 段用 `family=COALESCE(?, family)` **保底**——10+ 调用点（回测/gate/选波回写）不带 family 时**不覆盖原值**，否则每次回测就把 family 清空 |
| **P0** | GEM 落库带 family | `run_pipeline.py`（`st.upsert_expressions` 前） | 读 `final_expressions_meta.json` 建 `expr→family`，构造 dict items 落库；无 meta（非 skeleton 模式）则不带，行为同前 |
| **P0** | 选波从 DB 读 family | `build_wave.py::load_family_map` | 新增 `conn`/`region` 参数；`--from-db` 时从 `expressions.family` 兜底读取。**另修一处真 bug**：选波回写 selected 时原来只传 `expression/status/dataset`，UPDATE 会把 family 覆盖为 NULL → 已补带 family |
| **P1** | 探针先于扩批 | `build_wave.py` 选波循环 | 该族**全库无已回测行**（`alpha_id` 非空）→ 本波 cap 收紧为 `WQB_PROBE_CAP`（默认 1）；`meta.probe_limited_families` 可查；`WQB_PROBE_GATE=off` 可关。**「全库」而非「本波」**：本波候选普遍未回测，只看本波会把所有族都判成未验证 |
| **P2** | 族结构进字段池 | `campaign.py::_extract_families` + `build_economic_field_pool` / `_field_catalog.py::_families_payload` + `build_candidate_field_pool` | `s2_field_pool_<ds>` payload 增 `families`/`family_stats`（**只含池内族**，池外族不带以免稀释 prompt）；主路径与回退路径口径一致 |
| **P2** | 版本 bump | `_field_catalog.py` | `POOL_BUILDER_VERSION` 4→5（内容变更，旧池无族段必须重建） |
| **P3** | 静默降级告警 | `build_wave.py` | `family_map` 为空但库内有 family 数据 → 打 `[family] ⚠ WARN`，防回归 |

**验证**：新增 `tests/unit/01_store_db/test_build_wave_family_probe.py`（10 条：族 cap 生效 / 无 family 不炸不误报 / 探针收紧 / `PROBE_GATE=off` 恢复旧行为 / 有回测行可扩批 / family 落库往返 / COALESCE 保底 / family 列存在 / 经济学池带族 / 回退池带族 / 无语义台账 fail-open）。**`01_store_db + 02_workflow` 643 passed / 11 skipped；`07_docs_skills` 781 passed / 4 skipped**。

**诚实缺口（文档已如实标注）**：`family` 由落库带入，**2026-10-01 之前生成的存量表达式 family 列为空**，无法从 `skeleton` 列反推（`skeleton`∈{single,group,ratio,linear_mix,event_gated} vs `family`∈{cs_rel,ts_chg,anomaly,...}，维度不同）。**存量波次的族 cap/探针不生效，新波次起生效**。若要存量也生效，需重跑 GEM（重新生成带 family 的表达式）。


---

## 12. 步 5（S2→S3）门禁评估与优化落地（2026-10-01 深夜，用户提问引发）

### 12.1 步 5 的运行机制（核实后）

唯一入口 `tools/wave_gate.py`（2026-09-30 已拆为 `wave_gate_pkg/`，入口 shim 保留 argparse 字面以过 `validate_argv` 静态解析）。顺序：

开波区域闸(exit 2) → GEM 池校验 → 机制形状软闸 → S1 字段校验 → **闸 SEM**(fail-closed / 剔式) → 语法+元数 → **`gate.py` 8 闸 + 批级多样性**（子进程） → 体检硬门 → PROD 饱和闸 → **闸 PF** → 质量预估+变体聚类 → 三处 `all_pass` 聚合 → **落 `gate_results`**。

分层：`wave_gate.py` = **编排/聚合**；`gate.py` = **逐条判定**。完成定义 = `get_gate_result.all_pass=1`。

### 12.2 评估结论：机制合理，但有 1 处真断流 + 2 处可优化

| # | 性质 | 结论 |
|---|---|---|
| ① | **★ 真断流** | **闸 SEM 结论从不落 `gate_results`**：`cli.py` 算出 `sem_report` 只用于打印 + 剔式，**全文无 `report["semantic"]`**；实测 846 条非 mcp 记录含 `semantic` 键 = **0 条**。与步 4 的 family 断流**同型**（内存生效、写入端沉默） |
| ② | 待优化 | **闸 PF 从未真正拦过波**：历史 65 条含 PF 的记录里 `enforced` 仅 2 条（均 09-25 前后）；拆分后 6 条真实波**全 `warn`**，`n_unknown_families` 高达 31/15/6/9/5/8 → 判据覆盖过窄，名义最硬、实际只在"看" |
| ③ | 待优化 | `probe_mode` 分支在 gate 阶段只做 **dry_run 结构预判**、`saved_quota` 恒 0，却写 `status=PROBE_ASSIGNED`，易误读为"探针已跑/已省配额" |

**澄清（避免误判）**：`gate_results.all_pass` 与 report 内层 `gate.all_pass` 历史 508/776 不一致——是 **2026-09-28 前**「首次落库时 all_pass 未算出」的遗留，**09-28 后已归零**（09-28:34→2；09-29/30:0；拆分后 6 条全对）。**非现患**。

### 12.3 落地记录：P0–P3 已实施（2026-10-01 深夜，用户批准）

| # | 改动 | 文件 | 关键点 |
|---|---|---|---|
| **P0** | 闸 SEM 结论落 `gate_results` | `tools/wave_gate_pkg/cli.py` | 新增 `report["semantic"] = {mode, region, dataset, ledger_missing, blocked_field_count, n_removed, n_kept, dropped_in_db, removed_sample(前10)}`；`--skip-semantic-gate`/`off` 也落 `{"mode":"off","skipped":true}`。**removed 只落样本**（全量撑爆 `report_json`）。含 `_sem_mode`/`sem_report` 为空时的兜底分支 |
| **P1** | 闸 PF 增设未探明骨架 enforce 档 | `gates_pf.py::check_prod_family_gate(unknown_mode=)` + `cli.py` + `tools/wave_gate.py` | 新参数 `unknown_mode`（缺省 `warn` = 历史行为逐字不变）；`enforce` 时把 UNKNOWN/WARN_LOW_CONF/WARN_MIXED 三类**升级为 violations**、`status=enforced`、`passed=False`；report 增 `unknown_mode` 字段。CLI `--pf-unknown-mode {warn,enforce}` > `WQB_PF_UNKNOWN_MODE` > 缺省 warn。`all_pass` 聚合沿用 `status==enforced and violations`，消息按"未探明 vs 已死路"分列 |
| **P2** | gate 阶段探针语义修正 | `cli.py` | `PROBE_ASSIGNED` → **`PROBE_PLANNED`**，explanation 写明"仅规划不回测，真探针见步 5b"；新增 `executed: False`；删去恒不触发的 `saved_quota>0` 分支。保留 `PROBE_DEAD` 判定并注明其为"外部注入接口"（`probe_batch_mode.py` 真回测终态） |
| **P3** | 文档与环境变量登记 | `references/step5-gates.md`、`SKILL.md`、`docs/env_registry.json` | 新增 §5.1.1「闸 SEM 留痕」；补 **PASS 只看外层 `all_pass`**（与 `gate.all_pass` 语义不同的说明）；PF 行补 `--pf-unknown-mode`；注册 `WQB_PF_UNKNOWN_MODE` 并 `index_tables.py --apply` |

**验证**：
- 新增/扩展测试 **8 条**：`04_gates/test_pf_family_aggregation.py` +4（unknown_mode 四态）；`04_gates/test_semantic_gate_failclosed.py` +4（SEM 落痕源码契约 ×2、probe 状态 ×1、**E2E 真跑 wave_gate 读库验 `semantic.n_removed==1`** ×1）。
- **全量 `tests/unit/` → 2826 passed / 24 skipped / 0 failed**（无排除；较上轮 2694 → +8 为本轮新增，其余为并行会话已修的 `test_se_docs` 124 条回归绿）。

**诚实边界**：
- P1 的 `enforce` 档**不改变默认行为**（缺省仍 `warn`），是否在饱和区启用需按区决定；`unknown_families` 偏高的根因是 `prod_family_*` 探针记录覆盖率低，强制前建议先补 prod-first 回写。
- P0 修复只解决**新波次**的 SEM 留痕；存量 1859 条 `gate_results` 的 `semantic` 键**永久缺失**（历史不可追补，因 removed 明细已随进程丢失）。

---

## 13. 步 6（S3）并发回测：机制与评估（2026-10-01）

> 评估口径：读真实代码（`pipeline.py` / `_lib/slots.py` / `config.CONCURRENCY`）+ 真实数据（`data/wqb.db`：`backtest_results` / `wave_results` / `ledger_kv` ckpt + `logs/_async_tasks/batch_track_*` 119 份 stdout）。**只读评估，未改代码。**

### 13.1 运行机制

**入口三选一，同一内核**（`step6-backtest.md` §6.1）：MCP `workflow_batch_track`（推荐，先过三道开波闸）/ toolkit `pipeline.py run --submit` / `workflow_campaign(stage="S3")`。

**七槽填槽（两阶段）**：
1. **Phase 1 并行提交**：`ThreadPoolExecutor(max_workers=n_slots)`，`n_slots = min(7, 批数)`（`--serial` 时 =1）。每批提交前 `slots_mod.acquire()` 拿**账户级槽位 token**。
2. **Phase 2 事件驱动轮询 + 即收即补**：`concurrent.futures.wait(FIRST_COMPLETED)`，每完成一批立即 `release()` 槽位 → `_refill()` 补下一批（**`_retry_queue` 重发批优先于 `_pending`**）。这是 2026-09-17 的 P0 优化，取代"两个独立 ThreadPool 全完才进下一轮"（消除早完成槽位的空等）。

**三层并发控制**：
- 进程内：`n_slots = min(7, 批数)`；`CONCURRENCY = {slots:7, burst_capacity:7, safe_instant_submits:6, min_batch_interval_sec:45, refill_sec_per_token:(20,40)}`。
- **跨进程账户级**：`_lib/slots.py` 在 `logs/_slots/` 下写 token 文件（内容 `pid|label|ts`），`acquire()` 数活 token ≥ cap（`WQB_GLOBAL_SLOTS` 缺省 7）即轮询等待；陈旧 token（进程死或 >6h）自动回收；**任何异常降级为不仲裁**（绝不阻断提交）。
- **连坐隔离**（`isolate_errors` 缺省开）：某批 ERROR → 解析子模拟定位坏式 → 坏式回写 `expressions.status='fail'` → 无辜兄弟作为"重发批"优先重发**一次**（防死循环）。

**收批级联**：`stage_review` → `save_backtest_results`（写 `backtest_results`）→ `auto_upsert_from_review(..., multisim_ids=ms_ids)`（写 `wave_results` + `region_kb` 刷新 + L1 规则提取）。

### 13.2 评估结论

| # | 级别 | 结论 | 证据 |
|---|---|---|---|
| **F1** | **P0 真实缺陷** | **提交期失败批次零重试 → 静默丢表达式** | `_run_round` L614-616：`submit_batch` 抛异常（429/网络）即写 `status='SUBMIT_FAIL'` 后**丢弃**，不进 `_retry_queue`（只连坐隔离填充）。`SUBMIT_FAIL ∉ TERMINAL`，仅跨轮重跑才补。全库 ckpt **42 批 = 330 表达式**；batch_track 日志 **62/119 含 429**；GBR `s2_institutions6_d1` gate=93 但入库=83（24 批 = 12 SUBMIT_FAIL + 12 COMPLETE） |
| **F2** | P1 | **完成度无自动闸** | §6.5「`backtest_results` 行数 = 波内表达式数」纯文档约定；`stage_review` 不比对 planned 即写 `wave_results` verdict。F1 的丢批因此零告警 |
| **F3** | P2 | **文档断流** | §6.2「`multisim_id` 写进每条回测行」为假——`backtest_results` 无此列；msid 实际进 `wave_results.batches` |
| **F4** | P2 | 数据卫生（非活代码） | `br.status='backtested'` 80 行（09-29 HKG）无任何活写入者产生，属历史遗留；`logs/_slots/` 残留 78 个 `.slot.stale`（`live_tokens()` 只认 `.slot`，无害） |

### 13.3 落地记录：P0–P2 已实施（2026-10-02 凌晨，用户批准）

| # | 改动 | 文件 | 关键点 |
|---|---|---|---|
| **P0** | 提交期失败自动重发 | `pipeline.py` | 新增 `MAX_SUBMIT_RETRY=2` / `_is_retryable_submit_error`（429·5xx·网络类可重发，4xx 其余不可）/ `_batch_key`（批指纹）。`_retry_queue`·`_submit_attempts`·`_isolation_retry` 前移到 Phase 1 之前；Phase 1 与 `_refill` 的提交失败统一走 `_queue_retry_or_fail`（可重发入队、超限/不可重发落 SUBMIT_FAIL）。**关键修正**：主循环改 `while futures or _retry_queue or _pending:` + `_fill_slots()`（补满 n_slots），修复"引导补批全失败→`while futures` 退出→剩余重发被静默丢弃"。队列元素升级三元组 `(batch, origin, kind)`；连坐隔离判据改 `_isolation_retry`（提交期重发批首次 ERROR 仍走隔离）。汇总行加 `⚠ SUBMIT_FAIL 累计=N 批` 告警 |
| **P1** | 波末完成度闸 | `pipeline.py` | 新增纯函数 `check_backtest_completeness(ck, n_saved, tolerance)` + `_count_wave_backtest_rows`（读库里本波真实行数）+ `_report_completeness`。两处 `save_backtest_results` 后调用，打印 `[complete] 完成度 OK/⚠ 不达标`，结果落 `ckpt.stages.review.completeness`。口径用**库里行数**而非本次 upsert 数，避免既往行/同 alpha 合并误判 |
| **P2** | 文档修正 | `step6-backtest.md` §6.2/§6.4/§6.5 | §6.2 更正「multisim id 写 `wave_results.batches`，非 `backtest_results` 行」；§6.4 429 行补提交期丢批说明 + 重跑指引；§6.5 补 P1 自动校验 |
| **P2** | slot 残留清理 | `_lib/slots.py` + `logs/_slots/` | 新增 `_prune_stale_files()`（只删 >24h 的 `*.slot.stale`，`live_tokens()` 顺带调用）；手工清 78 个历史 `.slot.stale`，目录已空 |

**验证**：新增测试 **15 条**（`tests/unit/02_workflow/test_pipeline_submit_retry_completeness.py`：可重发分类 / 批指纹 / 429 重发成功 / 重发上限落 SUBMIT_FAIL / 400 不可重发直落 / Phase1 全败引导补批 / serial 单槽不死锁 / 提交重发批仍可隔离 / 完成度纯函数四态 / 源码契约 / 库不可达降级）。`02_workflow` 目录 265 passed；**全量 `tests/unit/` 2845 passed / 24 skipped / 0 failed**。`sync_skills.py --check` 全绿。

**诚实边界**：P0 重发上限 2 为经验值（持续 429 仍会落可见的 SUBMIT_FAIL，可由重跑续命，不再静默）；P1 是 WARN 非硬闸（不阻断写 `wave_results`，只告警 + 落 checkpoint）；F3/F4 的 `backtested` 历史 80 行**未回改**（无活写入者，影响仅统计口径，改数据得不偿失）。

## 14. 步 7（S4）诊断改进：机制与评估（2026-10-02 凌晨，用户提问引发）

> 只读评估，未改任何代码。结论：**机制设计合理（4 段职责清晰、判据集中、fail-open 到位），但有 1 处真断流（P0）+ 3 处口径分裂（P1）+ 2 处卫生问题（P2）**。

### 14.1 运行机制（四段，顺序即执行顺序）

```
S3 收批 → ① prod-first 探针 → ② s4-prescreen 预筛 → ③ review_wave 评审 → ④ 逐候选链 → 步 8
```

| 段 | 实现 | 写台账 | 真实执行现状 |
|---|---|---|---|
| ① **prod-first** | `tools/campaign_intel.py _cmd_prod_first`（1367 行文件） | `prod_first_<wave>` + `prod_family_<region>_<skel>` | ✅ 活（`pipeline.py --prod-first` 子进程调，2026-09-19 自动化） |
| ② **s4-prescreen** | `campaign_intel.py _cmd_s4_prescreen`（打平台 `get_alpha_details`，逐条） | 无（只打 stdout） | ⚠️ **零编排调用点**（全库仅文档引用，见 F2） |
| ③ **review_wave** | `review_wave.py`（406 行）由 `workflow_campaign(stage="S4")` 驱动 | `review_<tag>` + `wave_results` | ✅ 活（但 `s4_walls_*` 断流，见 F1） |
| ④ **逐候选链** | 人审 / 各 skill（selfcorr-quick → check_self_correlation → compute_mutual_correlation → check_correlation → robustness → judge） | `submit_ready` / `salvage_pool` | ✅ 活 |

**三层判据集中度（设计优点，核实无误）**：
- 硬闸唯一源 `config/thresholds.json`（review / near 两节），`review_wave.py:254` 读；
- 墙判据纯函数化（`walls()` / `rn_exposure()` / `structurally_dead()` / `near_block_wall()`），**被 `review_wave` 与 `pipeline.stage_review` 共用**（pipeline L1068 显式调 `review_mod.near_block_wall`）——这是 2026-09-19 / 09-27 两次审计的成果，确实落地；
- 指标 NULL 一律走 `*_UNKNOWN`（`walls()` L64-84），**不误判**；
- OS 衰减校准 fail-open（`_os_baseline` 异常返回 None，评审照常），已在真实数据上跑通（USA `review_s2_order_book_imbalance_d1` 的 `os_calibration.annotated=30`）。

### 14.2 评估结论

| # | 级别 | 结论 | 证据（真实数据） |
|---|---|---|---|
| **F1** | **P0 真实断流** | **`s4_walls_<region>_<wave>` 在当前 SOP 路径上不写** | ① 唯一写者 = `campaign.py:715`（`workflow_campaign(stage="S4")` 路径）；SOP 主路径 `pipeline.py --review` 只算 `r["walls"]` 进 `wave_results`，**从不写该键**（`stage_review` 全文核实）。② 近 21 天 **25 个 `s2_%` 波，0 个有 `s4_walls` 键**；最后一个键停在 **2026-09-29**，而同期 `review_*` 键持续更新。③ `step_eval.py:350` 的 S4 质量指标 `walls_coverage = s4_walls_* 键数 / wave_results 波数` → **实测恒为 0** |
| **F1b** | **P0（F1 根因）** | **已写出的 `s4_walls` 内容还不可信** | 唯一写者 `campaign.py:_extract_walls_summary`（L2096）是**对子进程 stdout 做全文关键词匹配**（`kw in lower`）。实测：喂全 PASS 的 `review_wave` 输出 → 返回 `None`（漏报）；喂含 "structural"/"robust" 字样的告警行 → 产出 `{structural:True, robust:True}`（误报）。全库 15 个 `s4_walls` 键中 **8 个是这种 bool 关键词产物**，仅 7 个是结构化 payload。该值下游是 `step_eval` 指标 + 人读 |
| **F2** | P1 | **`s4-prescreen` 从未被编排调用** | `grep -rn "s4-prescreen"` 全仓：调用点仅 `auto_review.py` 注释（说明已废弃该子进程调用）与文档。SKILL.md 步 7 明写「调用：`s4-prescreen`（全灭直接判死）」→ **文档承诺的 8× 预筛压缩实际由人手工执行**，自动链里不存在。`workflow_campaign(stage="S4")` 直接跑 `review_wave`，不预筛 |
| **F3** | P1 | **三套预筛口径不一致（同一批 alpha 三种结论）** | ① `s4-prescreen`：`sharpe≥1.58 / fitness≥1.0 / 2Y≥1.58 / prod≤0.7 / self≤0.7` + `tvr∈[0.04,0.40]`；② `auto_review._prescreen`：同前四闸但**无 prod/self**（表里无列）、`tvr∈[0.04,0.40]`；③ `review_wave.walls()`：`sharpe_min` **取各区 `thresholds.json`**（USA 1.25 而非 1.58！）、turnover 与 near 线也按区。实测 GBR `s2_institutions6_d1` 77 条 → `auto_review` 口径全判 **REJECT**（0 READY / 0 REVIEW ），而同批 `review_wave` 会在 USA 阈值下产出候选 |
| **F4** | P1 | **NULL 指标被当 0（口径方向与 `walls()` 相反）** | `s4-prescreen` 用 `m.get("sharpe") or 0`、`auto_review._prescreen` 用 `bt.get("two_year_sharpe") or 0` ——全库 **1200 行 `two_year_sharpe IS NULL`，其中 222 行 sharpe≥1.58 且 fitness≥1.0**（本应 READY/REVIEW）会被静默判 REJECT。而 `review_wave.walls()` 同列缺失走 `2Y_UNKNOWN`（不判败）。同一数据两种相反处置 |
| **F5** | P2 | `salvage_pool.dataset` 字段 79% 为 None | `_salvage_entry` 的 `dataset` 正则白名单（`anl\d+|fnd\d+|pv\d+…`）不覆盖 `insd1_` / `count_institutional_*` / `mean_flash_*` 等真实前缀 → 1019 条中 803 条提不出。**但功能无损**：消费端 `get_salvage_pool` 先走 `resolve_salvage_entries`（按 `alpha_id` 回查 `backtest_results`/`expressions`）→ 实测 unknown 从 79% 降到 **3%**（32/1019），`exclude_dataset` 过滤有效。属**记账冗余**，非断流 |
| **F6** | P2 | `near.shb_min` 区域分裂无文档 | `near.sharpe_min`：6 区 = 1.0（AMR/DEU/IND/JPN/KOR/USA），6 区 = 1.2（ASI/CHN/EUR/GBR/GLB/HKG/MEA）。这是**有意的区域校准**（写在各区 `thresholds.json`），但 `step7-diagnose.md` §7.3 只写「YELLOW」未提分区值 → 读者易误以为全局统一 |

### 14.3 合理性判定（哪些**不该**改）

- **四段顺序**（prod-first 前置）正确：prod 是全区绑定约束（库存 22/22 撞墙），先探族再扩变体，比"烧满回测槽再查"省一整波。P0 无异议。
- **`near_block_wall` 共用**是正确设计：RN_EXPOSURE / ROBUST_STRUCTURAL 同时拦 `passes()` 与 `near`/`salvage`（否则全灭波被记 PARTIAL、停止规则 B 永不触发）。核实两处调用一致。
- **OS 校准 fail-open + caveat 标注**（秩相关仅 +0.086，不作单候选排序）正确且已在 `caveat` 字段声明，不构成缺陷。
- **`salvage_pool` 的 79% unknown 不必修数据**：消费端已自愈（F5），只需修 `_salvage_entry` 的字段名提取口径（下次入池生效）。

### 14.4 优化建议（按 ROI 排序，待批准）

| 优先级 | 动作 | 目标文件 | 预期效果 |
|---|---|---|---|
| **P0** | `stage_review` 增写 `s4_walls_<region>_<wave>` 键，值取**结构化** `{"walls": {每墙命中数}, "reviewed_at", "region", "wave", "per_alpha": {...}}`（用现成的 `r["walls"]` 聚合，不扫 stdout） | `pipeline.py stage_review` | F1+F1b 一并消除；`walls_coverage` 指标从恒 0 恢复可读 |
| **P0** | `campaign.py:_extract_walls_summary` 改为**优先读子进程结构化产物**（`review_<tag>` ledger 键），仅在拿不到时降级到关键词扫描（且加 `# 降级路径` 注释） | `campaign.py` | 消除 stdout 关键词误报/漏报 |
| **P1** | 抽出**单一预筛口径函数** `s4_prescreen(rows, thresholds) -> {READY/REVIEW/REJECT}`，三处（`campaign_intel` 在线版 / `auto_review` 离线版 / `review_wave`）共用；在线版仅多 prod/self 两个平台的附加字段 | 新增 `_lib/prescreen.py` + 三处改调用 | F3 口径归一，消除"同批三种结论" |
| **P1** | 预筛的 NULL 语义改为与 `walls()` 一致：`*_UNKNOWN` 不判败（走 REVIEW 而非 REJECT） | 同 P1 上一项 | F4，222 行高分候选不再被静默判死 |
| **P1** | 把 `s4-prescreen` 挂进 `workflow_campaign(stage="S4")` 前置（REJECT 全灭则跳过 `review_wave` 直接判死），或明确把 SKILL.md 的「调用」改为「人工执行」 | `campaign.py` + `SKILL.md` 步 7 | F2，兑现 8× 预筛压缩（或至少消除文档与现实的落差） |
| **P2** | `_salvage_entry` 的 dataset 提取改为**字段名最长前缀启发式**（去掉硬编码白名单）或直接留空由消费端 resolve | `review_wave.py` | F5，账本可读性 |
| **P2** | `step7-diagnose.md` §7.3 补一行各区 `near.sharpe_min` 取值表（1.0 / 1.2 两档），并在 §7.7 注 `s4_walls` 写者路径 | `step7-diagnose.md` | F6 + F1 文档面 |

**验证方式（落地后）**：① 新单测覆盖 `s4_prescreen` 四态（含 NULL）+ `stage_review` 写键契约（`src.count(...) == 1`）；② 用 GBR `s2_institutions6_d1` 真实行回归，断言三处口径对同一批给出一致分层；③ `step_eval` S4 `walls_coverage` 在跑过一波后 > 0。

### 14.5 落地记录（2026-10-02，用户批准「帮我落地」）

全部 P0–P2 已落地，改动文件 9 个 + 新增 2 个；新增回归测试 `tests/unit/06_wave_pipeline/test_s4_walls_prescreen_20261002.py`（18 例全绿）；相关 4 个测试目录 **984 passed / 16 skipped / 0 failed**，文档目录 **780 passed**（其中 1 例为本次收紧的护栏，见下）。

| 项 | 文件 | 落地内容 |
|---|---|---|
| **P0-a** | `Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py` | 新增纯函数 `build_s4_walls_payload(region, wave, rows)`（聚合 `r["walls"]` → `{walls:{墙名:计数}, per_alpha, n_rows, n_candidates, reviewed_at}`）+ `_write_s4_walls(ctx, ck, rows)`；在 `stage_review` 的 **normal 与全灭快速通道两条路都调用**（此前全灭通道连 `walls` 都没算，现已补填）。 |
| **P0-b** | `src/wqb/workflow/nodes/campaign.py` | `_extract_walls_summary` 改**结构化优先**：先读 ledger `s4_walls_<region>_<wave>`（`_source="ledger"`），拿不到才 fallback 扫 stdout（`_source="stdout_scan"`）。旧漏报（全 PASS→None）与误报（"structural" 告警→假墙）仅在 fallback 保留并显式标注。 |
| **P1** | 新增 `_lib/prescreen.py` + 改 `auto_review.py` / `tools/campaign_intel.py` | 三处预筛口径收敛到唯一源 `prescreen(rows, thresholds)→{READY/REVIEW/REJECT}` + `prescreen_row`。**NULL 语义改为 `*_UNKNOWN` 不判败**（仅 sharpe 缺失→`NO_SHARPE` 判死）。三处调用方均"仓库副本优先"。 |
| **P1-b** | `src/wqb/workflow/nodes/campaign.py` | `s4-prescreen` 进 S4 编排：`resolve_s4_alphas` 后调离线 `_s4_prescreen_local`（零平台 API）；全灭 → 早退判死、跳过 `review_wave`。 |
| **P2** | `review_wave.py` | `_salvage_entry` dataset 提取：正则补 `insd\d*/insider/institutional/flash/sentiment` 等族 + 新增 `default_dataset` 兜底（本波数据集）。 |
| **P2** | `step7-diagnose.md` | §7.3 补 `near.sharpe_min` 两档表（1.0：AMR/DEU/IND/JPN/KOR/USA；1.2：ASI/CHN/EUR/GBR/GLB/HKG/MEA）；§7.1 补 ②③ 段"已编排/写者路径"；§7.10 补 `s4_walls_` 归零旧缺陷说明。 |
| 附带 | `src/wqb/workflow/_common.py` | 新增 `resolve_toolkit_file(relpath)` —— **仓库副本优先**的 toolkit 文件定位器，修掉底层 off-by-one（见"踩坑"）。 |
| 附带 | `docs/ledger_keys.json` | `s4_walls_<region>_<wave>` 条目补 `pipeline.py` 写者 + 结构化 payload 说明（此前只登记 campaign.py，正是 F1 的文档面）。 |
| 附带 | `tests/unit/07_docs_skills/test_se_docs.py` | 收紧 FQ 护栏正则（原 `prescreen_` 过宽，会误伤 S4 预筛；改为主体 token `prescreen_gate` + 独有 ledger key 字面量）。 |

**踩坑（值得记）**：`src/` 代码定位 toolkit 的仓库副本时，首版用固定 `".."×5` 上溯（`src/wqb/workflow/nodes/` 只需 ×4），off-by-one 落到仓库**父目录** → 永远命不中仓库副本 → 退回安装位 `~/.claude/skills`（当时缺 `prescreen.py`）→ 静默用旧口径。**根因是 `_skill_roots()` 把安装位排在仓库副本之前**，故新增 `resolve_toolkit_file` 强制"仓库副本优先"。教训：跨目录定位一律走上溯搜索或 `REPO_ROOT`，**不写死层级**。

**验证结果**：GBR `s2_institutions6_d1`（77 条，sharpe 0.44–0.64 / fitness 0.14–0.26，无 NULL）三处口径现一致给 `{READY:0, REVIEW:0, REJECT:77}`（诚实判死，非旧口径的"静默 NULL 判死"）。该波确为死波。

---

## 15. 步 8（S4→S5）稳健闸与提交判定：机制与评估（2026-10-02 凌晨，用户提问引发）

> 结论先行：**判定层（谁拦谁放）设计良好且已收敛到唯一实现；动作层（真提交）是新发现的最大风险面——存在一条「绕过 robustness REJECT」的路径，且 prod<0.7 / 配额两个「前置」在 REGULAR 路径上无任何代码执行。附带三处文档-代码不符（`pre_submit_check` 已死但文档仍在教）。**

### 15.1 运行机制（四段，顺序即执行顺序）

步 8 不是一段代码，而是**两条独立的链**共用同一套判定语义：

```
                       ┌──────────── 判定层（否决权威，只能拦）────────────┐
候选 ──①资格门──▶ ②submit_verdict ──▶ ③prod 实测 ──▶ ④用户确认 ──▶ ⑤真提交
  Failed RA==0     CLI/MCP/批量三入口共用      手动           红线      动作层
                   submit_verdict_core.decide                          │
                                                                       ├─▶ A. workflow_submit_alpha → submit_alpha 节点
                                                                       └─▶ B. super_build.py submit（SUPER 专用）
```

| 段 | 实现（唯一源） | 输入 → 输出 | 语义 |
|---|---|---|---|
| **① 资格门** | `wqb.config.compute_webdata_failed_counts`（`config.py:396`）| `is.checks` → `failed_ra/failed_ppa` + pending 名单 | `result != PASS and != PENDING` 计入失败（WARNING/ERROR/缺失都算）；**PENDING 不计失败但须等算完再判** |
| **② 判定** | `wqb.submit_verdict_core.decide`（`submit_verdict_core.py:91`）| `(detail, submit_status, submit_checks, robustness)` → `verdict + exit_code` | 三入口（CLI `tools/submit_verdict.py` / MCP `tools_ops.py:202` / 批量 `tools/batch_submit_verdict.py`）共用；**否决权威**。`SUBMITTABLE=0 / BLOCKED=1 / UNVERIFIABLE=10 / ALREADY_SUBMITTED=11` |
| **③ prod** | `mcp check_correlation(refresh=True)` | alpha → prod 值 | **不在 ② 内**；`decide` 的 docstring 明写"放行还需 prod<0.7 实测 + 用户确认，均不在本模块内" |
| **④ 确认 / ⑤ 提交** | `submit_alpha` 节点（`submit_alpha.py:96`）/ `super_build.py submit` | → `status=ACTIVE` + `dateSubmitted` | 不可逆；SUPER 强制走 B（节点内 `submit_alpha.py:231` 显式拒绝 SUPER） |

**robustness 台账的衔接（步 8 的核心新机制，2026-09-29 落地）**：`brain-alpha-robustness` Phase D 把结论写 ledger `robustness_<alpha_id>`（**唯一写方 = agent**，`upsert_ledger_key`）；`decide` 经 `robustness=read_record(...)` **被动读取**，映射：

| 台账 verdict | `decide` 反应 |
|---|---|
| `REJECT` | **BLOCKED**（`reason_code: ROBUSTNESS_REJECT`，fail-closed） |
| `CONDITIONAL` | 不改判，`next_step` 提示先 repair 重审 |
| `PASS` | 不改判、不加提示 |
| **无记录** | 不改判，仅 `next_step` 提示——**fail-open** |

### 15.2 评估结论（F 清单，全部经代码/数据实测）

**F7（P0，真实绕行——本次最重要发现）：`submit_alpha` 节点不读 robustness 台账，`REJECT` 拦不住 `workflow_submit_alpha`。**
- 证据：`submit_alpha.py` **无 `robustness_record` / `read_record` 引用**（grep 为空）；它用的是**人工布尔** `robustness_audited`（`:103 / :218`）。
- 后果：一个台账已 `REJECT` 的 alpha，`tools/submit_verdict.py` 报 BLOCKED（拦），但 `workflow_submit_alpha(confirm_submit=True, robustness_audited=True)` **照提不误**——两个入口对同一份证据给出相反结论。
- 这条正是 SKILL.md 自称"robustness 是 S4→S5 必经闸"的**实现缺口**：必经只在 `submit_verdict` 侧成立。

**F8（P0）：prod<0.7 在 REGULAR 路径无代码执行。**
- 证据：`submit_alpha.py:229` 注释直书"**本节点没有 prod 闸**"；`grep check_correlation` = 0；`decide` 也不含 prod。
- 后果：本仓最高频铁律「prod<0.7 才提」在 REGULAR 路径上**纯靠 agent 自觉 + 用户确认**。SUPER 侧有硬闸（`super_build.py:105 _prod_gate_verdict`，≥0.7 拒绝），**REGULAR 侧没有**——两条通道把关强度不对称。

**F9（P0）：REGULAR 配额（4/ET 日）无代码前置。**
- 证据：`submit_alpha` 节点与 `decide` 均无 quota 调用（grep 空）。SKILL.md:30 把"当日 REGULAR 配额未满（`quota_status.py`）"列为**前置**，报告 §2 也这么写——但它是**人工步骤**，不满足"缺一不得进入步骤 2"的强制语义。
- 后果：配额耗尽只会在 POST 后以 `403 REGULAR_SUBMISSION: FAIL` 回带（`SKILL.md:65` 已正确处置），即"先撞墙才知"。配额真实值在 `tools/quota_status.py`，未接入提交路由。

**F10（P1）：`pre_submit_check` 已是死代码，但文档/测试仍在教它。**
- 证据：`pre_submit_check` 定义在 `world-quant-brain-mcp/brain_mixin_simulation.py:849`，**生产调用点为 0**（唯一 caller 是它自己的单测 `test_brain_api_unit.py`）；`submit_alpha` 节点 2026-09-29 已改用 `_submit_gate`（`submit_alpha.py:204-207` 注释明记"替代旧的弱启发式 pre_submit_check"）。
- 但仍有 3 处在教它：`worldquant-submit-alpha/SKILL.md:93`（失败分支表"预检 blocked → `pre_submit_check` 未过"）、`references/ppa-handoff.md:8-10`、`tests/unit/01_store_db/test_threshold_relations.py:51,62,76`（把它当活机制钉阈值）。
- 后果：**PPA 路由表建立在过时前提上**。`ppa-handoff.md:8` 称节点"**不是 PPA 感知的**、内置宽松本地筛（Sharpe>1.3…）"——而 `_submit_gate` 既不宽松（fail-closed）、也**部分 PPA 感知**（按 `is_ppa` 选 `failed_ppa`），前提已变。

**F10b（P1）：`is_ppa` 判定两处不一致。**
- `submit_verdict_core.is_ppa_alpha`（`:66`）：`type==PPA` **或** 带 `PowerPoolSelected` 标签 → True。
- `submit_alpha._submit_gate`（`:407`）：**只认 `type==PPA`**，漏了标签。
- 实测：`{type:REGULAR, tags:[PowerPoolSelected]}` → `core.is_ppa_alpha=True` 但 `_submit_gate.is_ppa=False`。后果：标签型 PPA 的 Failed-count 资格门**按 RA 的 18 项名单算，而非 PPA 的 7 项名单**（`config.py:374-388`），口径错配。

**F11（P1）：文档-代码不符（`worldquant-submit-alpha` 3 处）。** 归并 F10 的文档面：SKILL.md:93 / ppa-handoff.md:8,10 描述的是已退休机制。

**F12（P2）：`mark_verified` 的 CLI 分支是死代码。**
- 证据：`tools/submit_verdict.py` 仅在 `SUBMITTABLE` 时调 `mark_verified` 升级 `submit_ready.gate`；而 `SUBMITTABLE` 现实中**永不出现**（平台 `GET /submit` 恒 404 → 恒走 UNVERIFIABLE，`submit_verdict_core.py:23-24`）。实际升级由**批量版 Phase2**（`batch_submit_verdict.py:289`）承担。
- 影响：低（不影响正确性），但 CLI 单条路径的 gate 升级是空想。

**F13（P2）：robustness 无记录 = fail-open 的边界未在步 8 文档写死。** `robustness_record.py:13` 明说"无记录 → 只提示不拦（旧候选与非 RA 链候选不应被一刀切挡死）"——这是**有意**的 fail-open，但步 8 的"有序检查清单"（SKILL.md:178）里 robustness 只以"前置"一句带过，没有"RA 链候选必须跑过"的硬规定 → 实操上可用"不写台账"绕过稳健闸。

### 15.3 合理性判定（哪些**不该**改——避免过度设计）

| 设计 | 判定 | 理由 |
|---|---|---|
| `submit_verdict` **只有否决权、放行需用户确认** | ✅ 保留 | 提交不可逆，放行权交人是对的；`UNVERIFIABLE` 是现实最好结果，**不得当放行** |
| 退出码四态（0/1/10/11）分列 | ✅ 保留 | 2026-09-29 X-2 整改成果：修掉"0 同时代表三种语义"的旧坑 |
| `decide` 三入口共用唯一实现 | ✅ 保留 | 已收敛，勿再各自复写 |
| robustness 无记录 fail-open | ✅ 保留（但需写死边界） | 一刀切会挡死非 RA 链候选；正确做法是**在 RA 步 8 侧把它变必查**，而非把 `decide` 改 fail-closed |
| `_submit_gate` fail-closed（无 `is.checks` 即阻断） | ✅ 保留 | 修掉旧 `pre_submit_check`"预检异常即放行"的 fail-open |
| `force=True` 跳过本地预检 | ✅ 保留（PPA/SUPER 合法用途） | 只跳本地筛、不放行平台检查；文档已限定两类场景 |
| SUPER 强制走 `super_build.py`（带 prod 闸） | ✅ 保留 | 两通道把关强度不对称的**正确方向**，应把 REGULAR 也补齐而非拆掉 SUPER 的闸 |

### 15.4 优化建议（按 ROI 排序，待批准）

| 优先级 | 动作 | 目标文件 | 预期效果 |
|---|---|---|---|
| **P0** | `_submit_gate` 增加 **robustness 台账读取**：`read_record(alpha_id, region)`，`REJECT` → 加入 `blocked_reasons`（`robustness_audited` 声明闸降为辅助） | `src/wqb/workflow/nodes/submit_alpha.py` | 消除 F7 绕行——两个入口对同一证据口径一致 |
| **P0** | REGULAR 提交前**自动查 prod**：`submit_alpha` 节点在 `confirm_submit=True` 时先 `check_correlation(refresh=True)`，`>= 0.7` → blocked（可经显式 `allow_prod_above_07` + force 豁免，留痕） | `submit_alpha.py` | 补上 F8——把最高频铁律焊进路由（与 SUPER 对齐） |
| **P0** | 提交前**自动查配额**：`tools/quota_status.py` 的取数接入 `_submit_gate`（REGULAR 满 4 → blocked 提示次日；`force` 不放行） | `submit_alpha.py` + `tools/quota_status.py` | 补上 F9——避免"先撞 403 才知" |
| **P1** | `_submit_gate` 的 `is_ppa` 改用 `submit_verdict_core.is_ppa_alpha`（含标签） | `submit_alpha.py:407` | 修 F10b，Failed-count 用对名单 |
| **P1** | 更新 `worldquant-submit-alpha`：SKILL.md:93 的 `pre_submit_check` → `_submit_gate`；`ppa-handoff.md:8-15` 重写路由前提（节点已 fail-closed 且部分 PPA 感知） | 两个 md | 修 F11，文档与代码同步 |
| **P1** | `test_threshold_relations.py:51-76`：把 `pre_submit_check` 的守护改为标注"**已退休、仅 client mixin 保留**"，或删该两测（改为守护 `_submit_gate` 的口径） | 测试 | 修 F10 的测试面，防止"守护活机制"的误读 |
| **P2** | 步 8 文档（`01_platform_gates.md` / SKILL.md:178）明写：**RA 链候选在进步 8 前必须已写 `robustness_<alpha_id>`**（无记录 → 视为未审计、应回跑 skill），把 fail-open 面在流程层收紧 | 文档 | F13：不改 `decide` 语义，只在 RA 链加必查 |
| **P2** | 清理 `mark_verified` 的 CLI 死分支（或注释说明"仅在批量 Phase2 生效"）；`pre_submit_check` 若确认无生产用途，评估删除（含 `gbr_pre_submit_check.py`） | `tools/submit_verdict.py` / `brain_mixin_simulation.py` | F12 + F10 的代码面 |

**验证方式（落地后）**：① 新增单测：`_submit_gate` 对 `robustness REJECT` 台账 → blocked；prod 0.75 → blocked；配额满 → blocked；标签型 PPA → `is_ppa=True`。② 端到端：造一个台账 REJECT 的 alpha，断言 `workflow_submit_alpha(confirm_submit=False)` 即 blocked（不再需要真提交验证）。③ 文档一致性：`grep pre_submit_check Claude/skills/` 应只剩"已退休"说明。

### 15.5 与步 7 落地的关系

步 7 刚落地的 `_lib/prescreen.py` 是**候选分层**（进场），步 8 的 `decide` 是**提交判定**（放行/否决），两者语义不同、**不得合并**（与步 7 的 `review_wave.passes()` 边界同理）。本次评估**未改任何代码**，仅产出 F7–F13 与建议，待用户批准后落地。

### 15.6 落地记录（2026-10-02，用户批准「落地」后执行）

§15.4 的 P0–P2 建议已**全部落地**。核对表（动作 → 文件 → 状态）：

| 优先级 | 动作 | 目标文件 | 状态 |
|---|---|---|---|
| **P0** | `_submit_gate` 读 robustness 台账，`REJECT` → blocked（F7） | `src/wqb/workflow/nodes/submit_alpha.py` | ✅ 已落地 |
| **P0** | REGULAR 提交前自动 prod 闸 `_prod_gate`（`check_correlation(production, refresh=True)`，≥0.7 或未出数 → blocked，fail-closed；`allow_prod_above_07` 显式豁免，force 不豁免）（F8） | `submit_alpha.py` + `registry.py` | ✅ 已落地 |
| **P0** | 提交前配额闸 `_quota_gate`（ET 今日 OS 池，满 4 → blocked，fail-open）（F9） | `submit_alpha.py` | ✅ 已落地 |
| **P1** | `_submit_gate` 的 PPA 判定统一走 `submit_verdict_core.is_ppa_alpha`（含 `PowerPoolSelected` 标签）（F10b） | `submit_alpha.py` | ✅ 已落地 |
| **P1** | 文档同步：`worldquant-submit-alpha/SKILL.md`（:30/:45/:93）+ `references/ppa-handoff.md` §1 + `submit-chain.md` §0/§2；`ra-pipeline/decision-table.md` D9 | 3 skill 文件 | ✅ 已落地 |
| **P1** | `test_threshold_relations.py`：`pre_submit_check` 改为「已退休」守护 + 新增 `_submit_gate`/配额/prod 阈值守护 + `is_ppa` 同口径守护 | 测试 | ✅ 已落地 |
| **P2** | 步 8 文档写死「RA 链候选进步 8 前须落 `robustness_<alpha_id>` 台账」（首次在前置块与 §2 表下方） | `submit-chain.md` | ✅ 已落地 |
| **P2** | 清理 `submit_verdict.py` 的 `mark_verified` 死分支（`SUBMITTABLE` → 并含 `UNVERIFIABLE`）；`pre_submit_check` 加 RETIRED 标记 | `tools/submit_verdict.py` / `brain_mixin_simulation.py` | ✅ 已落地 |

**实现要点（与 §15.4 计划的差异）**：
- prod 闸与配额闸**不并入 `_submit_gate`**（那是纯函数、不触网），而是作为 `run()` 里独立的 Step 1.6 / 1.4；`_submit_gate` 只新增「读台账」一处的可注入 I/O（`robustness=` 显式传入优先，否则按 `alpha_id`+`region` 读库）。
- `force` 的语义边界被明确拆开：**豁免** `_submit_gate` 与 robustness 声明闸；**不豁免** prod 闸 / 配额闸（用户红线须显式 `allow_prod_above_07=True`；配额满无需绕过）。
- robustness 声明闸降为辅助：台账已有记录（PASS/CONDITIONAL）即视为审计已过，不再强制调用方重复声明 `robustness_audited=True`。

**验证证据**：
- 新增 `tests/unit/05_submit_quota/test_submit_gate_p0_20261002.py`（**18 项全过**）：三闸纯函数判定 + `run()` 集成（台账 REJECT / prod 0.81 / 配额满 / force 不豁免 prod / SUPER 跳过配额闸）。
- `tests/unit/01_store_db/test_threshold_relations.py`（8 项全过）：新增 `_submit_gate` 阈值钉死、`_is_ppa_alpha` 与 core 同口径、`pre_submit_check` 退役守护。
- 回归：`tests/unit/{07_docs_skills,05_submit_quota,01_store_db,02_workflow}` 合计 **1630 passed / 15 skipped / 0 failed**。
- `tools/sync_skills.py --check`：4 个安装位全部 OK。
- 端到端：`test_run_robustness_ledger_reject_blocks` 断言 `workflow_submit_alpha(confirm_submit=True, robustness_audited=True)` 在台账 REJECT 时即 blocked（无需真提交验证 F7 已闭合）。

**顺带修复**：`Claude/skills/wq-brain-superalpha/references/selection-playbook.md`（前序会话新建的未跟踪文件）被 `skill_lint` 的 `expr-gate` 误判 `infix_leg_sum`——该表达式是 SuperAlpha **selection** 语言（合法算术 `+`/`/`），非 alpha 组合，加 `<!-- lint:counterexample -->` 豁免标记。

### 15.7 收尾删除记录（2026-10-02，用户「确认删除」后执行）

§15.6 里 P2 只给 `pre_submit_check` 打了 RETIRED 标记（**代码未删**）。用户确认后，本轮执行了**物理删除**并清理全部残留引用：

| 删除对象 | 说明 |
|---|---|
| `world-quant-brain-mcp/brain_mixin_simulation.py::pre_submit_check`（91 行） | 生产调用方 = 0；替换为 6 行注释说明（指向 `_submit_gate`） |
| `world-quant-brain-mcp/tests/test_brain_api_unit.py` 的 `_details` 助手 + 6 个 `test_pre_submit_*` | 随方法删除；保留 `make_shell()` |
| `tools/gbr_pre_submit_check.py`（261 行） | 独立 GBR 检查器，是 `pre_submit_check` 的配套工具 |
| `tools/validate_gbr_fields.py`（216 行） | 仅被上述脚本以子进程调用（`validate_fields_batch.py` 是它的通用替代，已保留） |
| `tools/test_gbr_batch_isolation.py`（320 行） | 仅被上述脚本以子进程调用；`from main import brain_client`，非 pytest 用例 |

**残留引用清理**（这些是「文档在教一个已不存在的方法」）：
- `tests/unit/01_store_db/test_threshold_relations.py`：退役守护 → **删除守护**（`test_pre_submit_check_is_removed_and_never_reintroduced`）：断言 `brain_mixin_simulation.py` 无 `def pre_submit_check`、`src/` 全树无调用形态、3 个 GBR 脚本不回流。
- `tests/unit/05_submit_quota/test_submit_alpha_super_guard.py`：`_FakeClient` 删掉 `pre_submit_check` 桩（已无调用方）。
- `src/wqb/workflow/nodes/submit_alpha.py`：两处历史注释补「2026-10-02 已物理删除」。
- `tools/validate_fields_batch.py`：docstring 里对 `validate_gbr_fields.py` 的提及补「已删除」。
- 文档：`Claude/skills/worldquant-submit-alpha/SKILL.md:94` + `references/ppa-handoff.md:8`、`docs/reference/CODE_QUALITY_SUMMARY.md`（长函数清单）、`docs/plans/2026-08-18-wqb-optimization-plan.md`（mixin 职责表）同步。

**验证**：`tests/unit/01_store_db/test_threshold_relations.py` + `tests/unit/05_submit_quota/` **191 passed**；`world-quant-brain-mcp/tests/test_brain_api_unit.py` **4 passed**；`tests/unit/07_docs_skills/` **782 passed**；`grep pre_submit_check src/ tools/ tests/ world-quant-brain-mcp/` 仅剩说明性注释与守护测试；`sync_skills.py --check` 4 安装位 OK；`index_tables.py --check` OK。
> 全量 `tests/unit/`：**2883 passed / 24 skipped / 0 failed**（后续复跑出现 29 个 `build_wave`/`wave_gate` 红，经查是宿主 `safe-delete` 钩子的 turn 累计文件操作数超阈值（>100）阻断子进程写锁文件所致——**同 turn 隔离复跑 34 passed**，非回归；判据：STDOUT 空 + STDERR 只有 safe-delete 一行）。

**保留项（有意不删）**：`attic/`、`reports/skills_review_20260929*.md`、`docs/skills_review_decisions.md`、`output_report/skills_stage_review_20261001.md` 里的历史提及——它们是审查留痕，反映当时状态，不属于「在教活机制」。

---

## §16 步 9（S6）复盘回写评估（2026-10-02，用户点名）

**结论**：设计层成熟、执行层有缺口。完整评估见 [`step9_s6_evaluation_20261002.md`](step9_s6_evaluation_20261002.md)。

**原理**：步 9 = 九步链唯一闭环点，把本波结论写回库让下一波先验自动变新；单一结论源 = `wave_results.verdict`；八步有序（①漏斗 ②verdict ③点塔 ④写波结论 ⑤判死/胜绩 ⑥饱和 ⑦逐数据集经验 ⑧刷先验快照）。

**做得好的**：verdict 归一化**写入方与停止规则 B 共用单一实现**（无双真相源）；判死取证闸 **fail-closed**（`recon_evidence.verify_evidence`，故障 ≠ 论坛无解）；`profile_drift` 钩子幂等 fail-open；`dataset-experience` 只读 DB + 原子写 + 保留人工块（sha256 证零写入）；`mark-saturated` 先预览后落库且 S0 已接线。

**发现的缺口**：
| 级别 | 问题 | 证据 |
|---|---|---|
| **P1** | 完成定义（§9.7 六项）**无机器校验** | grep `src/wqb/workflow/nodes/` 无 step9 完成度节点；GEM 对 stale 快照只 WARN（`gem.py:489`）；GBR 快照落后 8 天即此后果 |
| **P1** | `suggest_verdict` **不读 near 池**，纯文本启发式 | 签名 `(verdict)` 无 conn（`wave_results_contract.py:93`）；证据版 `verdict_from_counts`（`:84`）**零调用方**。注意：自动路径 `auto_upsert_from_review`（`_lib/wave_results.py:278`）**用真实计数**推 verdict，只有手写兜底是启发式 |
| **P2** | 方案 B（step_events）**S6 埋点空缺** | 12 类事件 9 类无写入方；`region_kb_refreshed`（第⑧步）与 `salvage_collected`（`seal_dead_end`）全无埋点 → S6 gain 恒 `n/a` |
| **P2** | `_recent_closed_waves` 缺独立回归测试 | R22 修正（按波的开始时刻取窗口）价值高，仅间接覆盖（`campaign.py:1401`） |
| **P3** | 产物文件名拼写 `campain`（少 g） | `dataset_experience.py:223`；已固化 8 产物 + 测试断言 |

**建议优先级**：P1 `tools/step9_audit.py`（只读校验 §9.7 六项，可先 `--enforce warn`）> P1 `suggest_verdict` 可选接收 near 计数 > P2 补 `_recent_closed_waves` 回归测试 > P2 S6 埋点 > P3 文档标注拼写。
**最值得先做**：`step9_audit.py`——问题 A/B/D/E 都是局部低风险，唯独「无机器校验」是结构性：整个闭环价值押在 agent 自律上，GBR 8 天延迟已证明会静默退化。
