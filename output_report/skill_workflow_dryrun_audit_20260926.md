# skills / workflow dry-run 体检与挖掘优化方案

> 日期：2026-09-26（ET 日 2026-09-25） · 账号 MT38799 · 视角：资深量化工程
> 目标：诊断"为什么挖不出可提交因子"，并给出可执行的优化方案

---

## 0. 结论先行

1. **工程管道本身是健康的，但它是"空转的健康"**。19 个 workflow 节点 dry-run **18 通过 / 1 失败**，静态四处同步无漂移，110 个权威单测全绿。管道没有崩，但也没有产出可提交因子——问题不在"能不能跑"，在"跑的方向"。

2. **真正的瓶颈是相关性，不是产量**。存量池 prod 相关 **中位数 0.7606、均值 0.7554，整体落在 0.7 闸门的错误一侧**；已测 prod 的 363 颗中 **64.7% 被闸门淘汰**。继续加大 S2 表达式吞吐，边际收益趋近于零。

3. **算力配置与过闸率反向**（⚠ **2026-09-26 02:00 已大幅修正，见 §3**）：可信的只有**止损侧**结论——**MEA / IND / DEU 停投**（两口径一致，MEA 66 例 18.2% CI[0.11,0.29]；IND 53 例 15.1% CI[0.08,0.27]；DEU 16 例 0% CI[0.00,0.19]）。初版"ASI 87.5% / HKG 60% / GLB 58.8% 过闸率最高"**已撤回**——那是 `JOIN ON expression`（关联键覆盖率仅 40%）造成的假象，且高过闸率区域样本量根本不足以支撑选区决策。

---

## 1. dry-run 体检结果

### 1.1 静态一致性（全绿）

| 检查项 | 结果 |
|---|---|
| `tools/audit_node_registration.py` | registry 19 = test_workflow 19 = `_DRY_RUN_CASES` 19 = INDEX 19，**无漂移** |
| `tools/sync_skills.py --check` | 4 个安装位（claude / codex / cursor / workbuddy）**全部与仓库一致** |
| `pytest tests/unit/test_skill_integrity.py tests/unit/test_workflow.py` | **110 passed** |

### 1.2 节点级 dry-run（19 个）

`execute(node, params, dry_run=True)` 全量执行，读取 `WorkflowResult.output`：

| 节点 | 结果 | 构建出的计划（摘要） |
|---|---|---|
| campaign | ✅ | `pipeline.py score_datasets.py --campaign-dir tracking/KOR` |
| inventory_scan | ✅ | `build_gate_prior_from_inventory.py --regions all …` ⚠️ 见 D4 |
| batch_track | ✅ | `campaign-toolkit/scripts/pipeline.py … --max-rounds 3 --review --write-ledger --submit` ⚠️ 见 D8 |
| gem | ✅ | `headless_runner/run.py --config … --data-category other --region KOR --delay 1 …` ⚠️ 见 D5 |
| gem_wave / feature_engineering / field_understanding | ✅ | 各阶段步骤计划正常 |
| wave_gate / unified_gate / structural_reconstruct | ✅ | 闸序列计划正常 |
| judge / submit_alpha / superalpha | ✅ | 请求计划已构建，**未调平台**（契约正确） |
| auto_harvest / auto_review / auto_pyramid / alpha_booster / modeb_improve | ✅ | 步骤计划正常 |
| **hypothesis_round** | ❌ | `假设目录不存在：data/hypothesis_catalog/_test_hypotheses.json` ⚠️ 见 D7 |

**判定**：dry-run 契约（走完零成本前置 → 构建命令 → 到此为止，不 subprocess / 不写库）**执行到位**。管道"能跑"。

---

## 2. 为什么挖不出可提交因子：漏斗量化

```
expressions   64,982  ████████████████████████  100%
alphas(回测)   8,169  █████                      12.6%
已测 prod        363  ▊                           0.56%
prod ≤ 0.7       128  ▏                           0.20%
已提交            65  ▏                           0.10%
```

三个致命观察：

| 观察 | 数值 | 含义 |
|---|---|---|
| **prod 预检覆盖率** | 363 / 8,169 = **4.4%** | 95.6% 的回测结果**从未进入闸门判定**，算力大量沉没在不可能过闸的候选上 |
| **prod 分布位置** | 中位 0.7606 / 均值 0.7554 | 分布中心**在闸门之外**，不是尾部问题而是**整体问题** |
| **闸门淘汰率** | 235 / 363 = **64.7%** | 相关性是唯一的最大漏斗颈，远超 IS 指标 |

**推论**：优化 IS（Sharpe/Fitness）对过闸没有帮助——相关性是**结构性**的，由信号与生产池的相似度决定，与信号强度弱相关。

---

## 3. 区域过闸率：核心发现（**2026-09-26 02:00 已修正，原表撤回**）

> ⚠ **修正说明**：本节初版用 `alphas JOIN expressions ON expression`（表达式文本匹配）统计，
> 复核发现该 join 存在**跨区重复匹配**与**区域误归因**。改用两种口径交叉验证后，
> 区域样本量相差 **2.6 倍**（表达式文本 join = 391 行 / `alpha_id` 权威键 join = 仅 148 行），
> 且 GLB 34→15、KOR 12→4、HKG 5→0 —— **原表的高过闸率区域大多是 join 假象**。原表撤回。

### 3.1 两种口径下都成立的部分：**停投结论（稳健）**

| 区域 | 口径A n/率 | 口径B n/率 | Wilson 95%CI（口径B） | 判定 |
|---|---|---|---|---|
| **MEA** | 78 / 16.7% | 66 / 18.2% | [0.11, 0.29] | **显著低 → 停投** |
| **IND** | 156 / 27.6% | 53 / 15.1% | [0.08, 0.27] | **显著低 → 停投** |
| **DEU** | 52 / 15.4% | 16 / 0.0% | [0.00, 0.19] | **显著低 → 停投** |

三种口径一致指向同一结论：**MEA / DEU / IND 的存量信号与生产池高度同质化，继续投入的边际产出显著低于池均值**。这是本次审计**唯一统计上站得住**的区域结论，也是最有操作价值的一条（止损）。

### 3.2 不成立 / 证据不足的部分：**"哪里值得投"（撤回）**

- **GLB**：初版报 n=34 / 58.8%，修正后 **n=15 / 60.0%，CI [0.36, 0.80]** —— 区间过宽，属"需扩样"，**不能**称为"确定性最高的边际投入区"。
- **ASI / HKG / KOR / USA**：n 分别仅 6 / 0 / 4 / 2，**HKG 在权威口径下样本归零**（初版的 60% 是纯 join 假象）。全部不可用于决策。
- **GBR**：n=11 / 27.3%，CI [0.10, 0.57]，需扩样。

### 3.3 根因：区域归因本身不可靠

`expressions.alpha_id` 大面积为空 → 仅 148 / 367 颗有 prod 的 alpha 能用权威键归因（覆盖 40%）。
**在补齐 `expressions.alpha_id` 回填之前，任何"按区域的过闸率排名"都只能用于止损判断，不能用于选区决策。**

### 3.4 修正后的行动建议

1. **立即执行（证据充分）**：MEA / DEU / IND 停开新波，存量只做维护。
2. **先修数据再决策**：补齐 `expressions.alpha_id` 回填（或改用仿真时记录的 region），重算区域表。
3. **扩样优先于下注**：GLB / ASI / GBR 各做 20–30 条 probe 扩样，**用扩样后的数据**再决定投入区，不要用现有小样本下注。

---

## 4. 缺陷清单（按优先级）

### P0 — 直接吞掉提交名额

**D1 · 异步受理无补发闭环（实证：3 颗 alpha 悬空 >24h）**
- 证据：本会话提交 `O0GjWqeY` / `2rpX85Ax` / `np8VGNz3`，平台回 `201 Accepted (async)` 与 `200 + Non-JSON 空体`；24 小时后查询**仍为 `UNSUBMITTED`**。
- 根因：客户端 `_poll_submit_until_resolved(max_polls=6, sleep_s=10)` 仅 **60 秒**窗口，超时即返回 `Accepted (async)`；workflow `submit_alpha` 节点 **Step 4 只有 `_poll_status`，没有任何 re-POST 分支**（`src/wqb/workflow/nodes/submit_alpha.py:262`）。全仓仅 `brain_mixin_simulation.py` 识别该形态，**无任何补发代码**。
- 连带损失：`_retire_queue` 仅在 `success` 时退役 → 悬空项**永久滞留待提交队列**，被反复选中重试。
- 修复：Step 4 超时仍为 `UNSUBMITTED` → **re-POST 一次**，再轮询；二次仍悬空则标记 `ASYNC_STUCK` 并落库告警，不再重复占用队列槽位。

**D2 · 配额无跨会话互斥（实证：ET 09-25 全程 0 提交）**
- 证据：ET 2026-09-25 当日 4 个 REGULAR 名额 + 1 个 SUPER 名额**全部被并行会话消耗**（GBR ×3 + KOR `KP78pLWk` + KOR SUPER `9qjGvaWe`），本会话准备好的候选一颗未提交。
- 根因：`tools/quota_status.py` 是**只读观测**，无预留/占坑机制；多会话共享同一账号配额。
- 修复：提交前用 `POST /submit` 的 `REGULAR_SUBMISSION value/limit` 做**原子性真值校验**（唯一可靠口径），并在提交前 30 秒内复检；建议增加仓库级 `quota_lock` 文件锁。

### P1 — 结构性效率损失

**D3 · prod 预检覆盖率仅 4.4%（1,081 个 IS 合格候选从未进闸门）**
- 未测 prod 且满足 `sharpe≥1.58 & fitness≥1.0` 的候选分布：

  | 区域 | DEU | GLB | ASI | IND | EUR | MEA | USA | KOR | GBR | HKG |
  |---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
  | 未测数 | 299 | **257** | **223** | 152 | 49 | 40 | 30 | 15 | 11 | 5 |

- 修复：**先按"止损"（可信）后按"扩样"（待证）分两步**——① 立即降权 DEU/MEA 的 339 个未测候选（两口径一致的停投结论）；② GLB / ASI / GBR 各投 20~30 条 probe **扩样**，用扩样后的数据决定是否升区，**不要**直接按初版排名下注（该排名已撤回，见 §3）。

**D4 · `inventory_scan` 默认 `--regions all`（已知必崩配置）**
- 证据：dry-run 构建命令为 `build_gate_prior_from_inventory.py --regions all --emit-candidates …`；项目经验库明确记录 **`--regions all` 并发必 SSL EOF，必须逐区串行**。
- 修复：节点默认值改为逐区串行循环，或加 `--regions` 白名单校验拦截 `all`。

**D5 · GEM 的 LLM 通道无健康预检（dry-run 假绿）**
- 证据：`config.json` 中 `moonshot_base_url = https://api.deepseek.com`、`model = deepseek-v4-flash`；经验库记录该通道 **402 Insufficient Balance**，实跑报"no meta.json within 90s"的假失败。dry-run **只能验证命令构建，验证不了 LLM 可达性**，故显示 OK。
- 修复：① 在 dry-run 中增加 LLM 连通性/余额探针（零 token 消耗）；② 把 `--ideas-file` 旁路固化为**默认路径**（手写 ideas md 完全跳过 LLM，已验证可行）。

**D11 · 区域资源配置与过闸率反向** —— 见 §3，这是"挖不出可提交因子"的直接原因，列为 P1。

### P2 — 治理与卫生

| 编号 | 问题 | 证据 |
|---|---|---|
| D6 | 门禁断链 | dry-run 输出 WARN：**14 个活跃波 / 84 条表达式无 `gate_results`**（GLB probe_glb_w1~w5_20260921 等）。修复入口 `tools/wave_gate.py --wave <wave>` |
| D7 | hypothesis_round 从未启用 | 唯一 dry-run FAIL：`data/hypothesis_catalog/` 为空。假设优先工作流在生产中零使用 |
| D8 | `batch_track` 默认 `submit: bool = True` | 与 AGENTS.md「提交类节点不入自动链」原则冲突，存在**偷跑配额**风险。建议默认改 `False` |
| D9 | skill 解析落到历史 Agent 位 | 命令中路径为 `C:\Users\MENGTAO/.claude/skills\...`（分隔符混用），仓库 `Claude/skills/` 仅作兜底。当前同步一致，但一旦某安装位落后即静默改变 pipeline 行为 |
| D10 | GEM `config.json` 明文凭据 | 含 BRAIN 邮箱/密码 + LLM key（已被 `.gitignore` 的 `**/config.json` 覆盖，**无 git 泄露**），但建议迁入 `.env` |

---

## 5. 优化方案

### 核心论断

> **瓶颈 = "选得不准"，不是"挖得不多"。**
> 64,982 条表达式 → 65 颗提交（0.10%）。加吞吐只会把 64,982 变成 200,000，转化率不变。
> 唯一有效的杠杆是把**筛选**前移，并把**选区**对准结构性低相关区域。

### 杠杆一：选区再平衡（ROI 最高，立即执行）

| 动作 | 依据 |
|---|---|
| **IND / MEA / DEU 停止新增投入**（★唯一统计稳健的一条） | 两种口径一致：MEA 18.2%/CI[0.11,0.29]、IND 15.1%/CI[0.08,0.27]、DEU 0%/CI[0.00,0.19]，均显著低于池均值 → 信号域已被生产池占满。存量只做维护，不开新波 |
| **先修数据再选区** | `expressions.alpha_id` 大面积为空（权威键仅能归因 148/367 = 40%），区域表在补齐前**只能用于止损、不能用于选区** |
| **GLB / ASI / GBR 只扩样、不下注** | 修正后 GLB n=15（CI 0.36–0.80）、ASI n=6、GBR n=11 —— 方向性提示但置信不足。先各投 20~30 条 probe 扩样，用扩样后数据决定是否升区。GLB 有首颗 SUPER `A1NQ57NW`（IS S4.26/F3.72）可作辅助旁证，但不替代相关性证据 |

### 杠杆二：把 prod 闸门判定前移到生成阶段

- **现状**：先回测 8,169 条，再筛；95.6% 从未测 prod，算力沉没。
- **改造**：在 S2 生成后、S3 回测前，插入**低相关先验筛选**——
  1. 按**字段族 / 数据集**做正交选波（同族挤压已三次实证：`0.672→0.8168`、`0.5836→0.9805`、`0.606→0.7079`）；
  2. **每族每波只保留 1 条**进入回测，其余直接判死并记 `FAMILY_DUP`，不消耗回测槽位；
  3. 回测后**先测 prod 再评估 IS**（prod 是 64.7% 的主漏斗，应先于 IS 淘汰）。

### 杠杆三：修掉吞名额的 P0 缺陷

- D1 异步补发闭环（3 颗已悬空，可立即补发救回 `O0GjWqeY` / `2rpX85Ax` / `np8VGNz3`）
- D2 提交前原子配额校验 + 仓库级锁

### 分阶段路线图

| 阶段 | 动作 | 验收标准 |
|---|---|---|
| **T+0（今天）** | ① 补发救回 3 颗悬空 alpha（若 ET 09-26 配额允许）<br>② `inventory_scan` 默认值改逐区串行<br>③ `batch_track` 默认 `submit=False` | 3 颗 alpha 脱离 `UNSUBMITTED`；两个默认值改动过单测 |
| **T+1~2** | ① `submit_alpha` 加 re-POST 分支 + `ASYNC_STUCK` 落库<br>② GEM 加 LLM 健康探针，失败自动切 `--ideas-file` | 新增单测覆盖异步补发路径；GEM 干跑能提前报 LLM 不可用 |
| **T+3~5** | ① GLB 定向 prod 实测（257 个未测候选，按族去重后分批）<br>② ASI/HKG probe 扩样各 20~30 条 | GLB 新增 ≥10 颗过闸候选；ASI/HKG 样本量达 20+ |
| **T+1 周** | ① 补齐 14 波 `gate_results`<br>② 按扩样结果重排区域优先级<br>③ 把低相关先验前移进 S2→S3 门禁 | 无门禁断链；转化率从 0.10% 起量 |

---

## 6. 当前可立即执行的动作（ET 09-26）

| 项 | 状态 |
|---|---|
| ET 09-25 配额 | **已耗尽**（REGULAR 4/4 + SUPER 1/1，均被并行会话消耗） |
| 剩余 READY 候选 | `np8VGNz3`（USA, S2.32/F1.60）、`VkGJ73eA`（USA, S1.70/F1.15）—— **prod 均未测** |
| 悬空待补发 | `O0GjWqeY`（KOR, S2.44/F2.85）、`2rpX85Ax`（USA, S2.71/F1.55）、`np8VGNz3`（USA, S2.32/F1.60） |
| 建议顺序 | 配额重置后：**先补发 3 颗悬空**（最高 IS 强度且已确认提交层受理），再测 `VkGJ73eA` 的 prod |

---

## 7. 复现命令

```bash
# 静态一致性
python tools/audit_node_registration.py
python tools/sync_skills.py --check

# 节点级 dry-run 全量（19 个）
python logs/_tmp_dryrun_audit.py        # 产出 logs/_dryrun_audit.json

# 权威单测
python -m pytest tests/unit/test_skill_integrity.py tests/unit/test_workflow.py -q   # 110 passed

# 配额真值（唯一可靠口径）
python tools/quota_status.py
```

> 注：`quota_status.py` 不区分 REGULAR / SUPER；REGULAR 余量**唯一可靠来源**是 `POST /alphas/{id}/submit` 响应中 `REGULAR_SUBMISSION` 的 `value/limit`。
