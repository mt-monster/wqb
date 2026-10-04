# KOR 因子挖掘优化全面方案（独立复核版）

> 任务：从 `tracking/KOR` 总结挖掘优化经验，逐层打开分析，给出全面优化方案。
> 方法：对全部真实产物做只读复核——169 键战役台账、102 个 wave 文件（854 表达式）、24 个脚本、21 份白名单、7 份评审、多样性复盘——逐层提取事实，再给出方案。
> 与已有文档的关系：本目录已有两份文档（13:20 流程总结、14:13 逐层分析，均非本会话产物）。本文对其做了**逐条独立验证**，§六列出勘误（其中"13 份 record 脚本""11/10 白名单 split"两处与事实不符），并补全其**完全缺失的挖掘策略层**（三面结构墙、快扫协议、毒表达式、配额教训）。

---

## 一、战役现状定量画像（复核实证）

| 维度 | 数值 | 来源 |
|---|---|---|
| 战役设置 | KOR / TOP600 / D1 / SECTOR / decay4 / trunc0.08 / maxTrade ON | `settings` |
| 规模 | 102 个 wave 文件，854 表达式（762 唯一，**92 条重复**），~35 个 wave 编号 | 文件统计 |
| 结果 | **0 达标、0 submit_ready、21 个数据集判死** | `qualified_alphas=[]` / `wave35_summary` |
| 最近候选 | `KPGZmLMl`（model170 四腿）：sh2.03/fit1.52/2y2.09/mg11.3bp/tvr26.1%/rn1.70/PROD0.601，**仅剩 CW 一墙** | `wave22P7v2_twoyear_confirmed` |
| 次近候选 | pv106 双腿：sh1.45/fit0.93/2y1.66（sh<1.58、fit<1.0 双墙，五维扫描封顶） | `wave34_summary` |
| 首个破局 | wave6 `VkGz2vrb`：sh1.68 IS 全过，但 **PROD 0.7668>0.7** 被拒 | `waves[0].verdict` |
| 早期评审 | wave1/3/3b/3c/4/5 共 141 个 alpha，**0 candidate、0 near**，max sh≤0.85 | `reviews/*` |
| 算子分布 | rank 1469 / multiply 1369 / add 617 / ts_av_diff 333 / vec_avg 286 / ts_decay_linear 185；**trade_when=0、winsorize=0、bucket≈0、ts_ir=5** | 我的全量统计 |
| 字段集中度 | mdl219 三字段（surp 146 / numrevy1 134 / divyield 125）占绝对多数 | 同上 |

**一句话诊断**：战役的瓶颈不在算子与参数，而在「数据集贫瘠 × 骨架单一 × 三面结构墙（CW / 2Y / PROD）」三者叠加——这与台账 `improvement_review_2026_08_15` 的自诊完全一致，我的独立统计予以证实。

---

## 二、挖掘策略层经验（已有文档完全缺失的部分）

### 2.1 三面结构墙（本战役的核心发现）

**墙 1：CW（CONCENTRATED_WEIGHT，集中度权重）——击杀 61 次，是最大杀手**
- 实证：model170 的 39/39 变体 CW 全败（rank 形态/decay 平滑/group_rank/zscore/signed_power/truncation 矩阵/SUBINDUSTRY 对照/bucket 离散化全部试过）；信号本身极强（sh1.89/fit1.39/2y2.03/PROD0.601/9 年全盈利）但**无法过 CW → 不可提交**。
- 论坛手册（LC97552，63 票）核心结论已入台账 `forum_cw_manual`：**CW 是数据品质问题，不是参数问题——truncation/decay/neutralization 修不了 CW**。
- 已验证的解法方向：① 事件型字段用**跨 Category rank 加法**（`add(rank(event_field), rank(ts_rank(close,90)))`，有 FAIL→PASS 且 2y 0.09→3.11 的案例）；② **蓝海字段（userCount=0）是 CW 免费通行证**；③ VECTOR 先 `vec_avg` 再 `ts_backfill`（顺序反了会触发 event inputs 错误）。
- **结构性根因**：90% 表达式是"rank 腿线性混合"单一范式（§一 算子分布证实），在 TOP600 小宇宙上天然权重集中。CW 墙与骨架单一是同一枚硬币的两面。

**墙 2：2Y（LOW_2Y_SHARPE，近两年衰减）——KOR/D1 信号系统性失效**
- 实证：institutions6（max|sh|0.86 但全家族 2y≤1.02）、model192（sh0.94 但 2y≤0.45）、model30（2y≤0.56）、model32（IS sh1.32 战役最强但 2y 全家族为负）——**信号只存在于历史区间**。
- 由此沉淀的快扫决策规则（`pipeline_note_2y_wall`）：**批 A 即查最强式 2y，max|sh| 高但 2y<0.6 直接红灯判死，不深挖**。fundamental44 即按此快速判死（省了一整轮深挖）。

**墙 3：PROD_CORRELATION（>0.7 拒）——与 USA 主导 book 的相关性**
- 实证：multi_source_model 的 `price_volume_quantile1_*_pred` 族与 PROD 存量相关 0.77–0.87，扰动/换层/SECTOR/中性化三波全撞 → 数据集判死。VkGz2vrb（sh1.68 IS 全过）唯一死因就是 PROD 0.7668。
- 教训：**IS 全过 ≠ 可提交**；PROD 是异步计算的提交期闸门，须以重检为准；去相关扰动批（wave6b_v2：ts_delta5/ts_rank22/signed_power0.5/60d 换层等 6 式）是唯一正确应对，但需早做。

### 2.2 快扫探针协议（已设计未接线的最大浪费）

`reference/kor_dataset_probe_battery.json`（8 探针 × 三灯评分）是战役沉淀的高质量资产：
- 探针组：P1 水平正 `rank(F)` / P2 水平镜像 `-rank(F)` / P3 差分 / P4 均值差分 / P5 衰减水平 / P6 时序自归一 / P7 动量 / P8 稀疏修复，每数据集 ≤6 字段 × 8 探针 = 48 式。
- 评分公式：`potential = max|sharpe|×2 + 镜像机会 + margin达标 + tvr达标`；**≥2.0 绿灯深挖 / 1.0–2.0 黄灯限 2 批 / <1.0 红灯判死**。
- **但它从未被脚本自动执行**——21 个数据集的生死全部靠人工整波试错判定。若接线，「每死一个数据集 = 烧一整波 8 式」可降为「探针批即判」，按 21 个死数据集估算可省约一半的试错模拟。

### 2.3 毒表达式与整批 CANCELLED（最新实证，14:38 入库）

- 教训链：连续 4 批 8/8 全 CANCELLED → 初判"日配额耗尽" → **对照批（全安全式）COMPLETE 推翻配额假设** → 二分探针（probe2–6）实锤真因：`add(multiply(rank(x),0.4), add(multiply(rank(y),0.3), multiply(rank(z),0.3)))` **嵌套三腿 add 结构**毒杀整批（`poison_nested_add_finding`）。
- 规则化：三腿混合优先写成 `add(add(a,b),c)` 左结合；连续 CANCELLED 时**先跑对照批区分"配额问题 vs 毒表达式"**，再决定是否停手。

### 2.4 数据集选择是第一优先级（非算子调参）

- 用户诊断已入台账：KOR/D1 候选池 os_is_sharpe 中位数仅 0.2–0.5，**零竞争与高质量互斥**（model313 cov0.76 但信号弱、other571 cov0.26）——选集锁死上限 sh~1.0。
- 双门槛 `cov≥0.85 且 alphaCount≤50` 破互斥；Tier1 首选 `behavioral_signals`（cov0.87/alpha0/value9 三项全满）、`equity_forum_data`（value10 零竞争）。
- 21 死数据集的死亡原因分布：**2Y 墙 ×6、无信号 ×6、CW 墙 ×3、覆盖不足 ×2、PROD 拥挤 ×1、其他 ×3**——2Y 与无信号合计过半，印证"数据集先天不足"。

### 2.5 纪律的正反面

- 正面（守住）：模板穷尽才切换（best<0.8 且 ≥40 式 + 论坛无解）、submit_ready 缓冲（配额 remaining=0 时达标不提交）、`polling_tooling_freeze` 唯一轮询入口、台账 `utf-8-sig` 编码。
- 反面（失守）：92 条重复表达式（重复烧配额）；`waveT_abandoned` 一个 multisim 卡 progress 0.1 超 24h 无超时熔断；同批多 multisim 并发导致后到批无错误 CANCELLED（`pipeline_note_cancel`）。

---

## 三、逐层打开分析（8 层，每层：现状实证 → 问题 → 优化）

### 层① 数据集体检与选择
- **现状**：`record_whitelist_v2.py` 手写 Tier1/Tier2 进台账；双门槛靠人算；探针电池未接线（§2.2）。`wave30_rejected` 等拒绝记录散落台账。
- **问题**：数据集发现 = 手写清单 + 整波试错；拒绝理由（cov0.75、字段 9 个、拥挤 357…）有规则但没固化成可执行筛选器。
- **优化**：
  - **M1（P0）** `score_datasets.py`：直连 `get_datasets(KOR/TOP600)` 全量评分 `w1·cov + w2·(1/max(alphaCount,1)) + w3·log(fieldCount) + w4·valueScore`，输出排序 + Tier，取代手写清单。
  - **M2（P0）** 接线探针电池：Top-N 候选先跑 P1–P8 探针批（≤48 式），按三灯公式自动判 绿/黄/红；红灯直接写 `xxx_dead` 台账，**不占正式 wave**。

### 层② 字段收割与类型预检
- **现状**：`kor_scan_fields.py/2/3` + `scan_aieq.py` 四份同构脚本，硬编码读 `.qoder-cn\cache\...\task-4d7` 外部会话缓存，正则抽字段 id，**从未取 `type` 列**。
- **问题**：换会话即失效、不可复现；类型缺失 → wave2 `acquisition_model` event 字段直套 rank/ts_*，24/24 ERROR 浪费 48 次配额。
- **优化**：
  - **M3（P0）** 统一 `scan_fields.py --dataset <id>`：走 `get_datafields` 取 `{id, type, coverage, userCount, alphaCount}`，落 `reference/kor_<dataset>_fields.json` typed catalog，取代 4 份脚本。
  - **M4（P0）** 类型数据驱动：预检的 event 判定从"正则剥 vec_*"（`kor_preflight_check.py` L99-117，嵌套/别名会误判）改为查 catalog 的 `type` 字段。

### 层③ 因子生成
- **现状**：外部 LLM（makeSomeGem）产表达式 → `batch_validate_kor.py` 只做语法闸 → `validate_wave2v2/3` 逐波复制。
- **问题（实证）**：生成非类型感知（LLM 拿不到字段 type）；骨架单一（rank+multiply+add 占 3469 次调用，trade_when/winsorize/bucket 零使用）；92 条重复表达式。
- **优化**：
  - **M5（P0）** 把 typed catalog + 多样性审计的 `unused_ops`（trade_when/bucket/ts_ir/winsorize）**注入生成提示词**，强制每波至少 N 式用未探索算子——直接针对 CW 墙的骨架根因。
  - **M6（P1）** 生成即去重：对全历史 wave 文件建表达式哈希集，新候选先查重（可省 92/854 ≈ 11% 的模拟）。
  - **M7（P1）** 合并 `batch_validate` + 逐波 `validate_wave*` 为参数化 `gate.py --file <path>`（语法+白名单+类型三合一，详见层⑤）。

### 层④ 选波与分层抽样
- **现状**：`select_wave1.py` 按前缀 `startswith` 分 9 桶、每桶 8、字段去重——**仅 wave1 用过**；wave17V 之后全部手工内联，选波纪律退化。
- **问题**：前缀分桶碰撞（`ts_delta` 同时命中 C1/C4）；后期 wave 高度同质；无 near-miss 优先级。
- **优化**：
  - **M8（P1）** `build_wave.py` 接管全部 wave：解析算子树前两节点分桶（消除碰撞）；按历史 near-miss（sh>1.2 的字段/骨架）加权抽样；每波强制骨架配比（如线性混合 ≤50%，事件门控/分组/比率 ≥30%）。

### 层⑤ 提交前预检（战役最成熟资产）
- **现状**：`kor_preflight_check.py` 三道闸（语法/白名单/类型禁用），已拦截 ts_min/ts_max、quantile 2 参、event 裸用等多起事故。设计优秀。
- **问题（实证）**：闸1 每表达式一次 `subprocess` 调 verifier（L48，N 次进程启动）；且 **verifier 路径指向 `.qoder-cn\skills\alpha-expression-verifier\...`（L20）——又一处外部 IDE 硬依赖，已有文档未捕获**；默认白名单写死 chart_cnn（L19）；3e 闸靠正则；无缓存。
- **优化**：
  - **M9（P0）** verifier 改为 `import` 直调 + 路径改为 `.workbuddy` 安装位置（或环境变量），消除子进程与 Qoder 依赖。
  - **M10（P1）** `--dataset` 自动派生白名单路径；接入 typed catalog（M4）替代正则 3e；pass/fail 结果落缓存幂等跳过。
  - **M11（P1）** 新增毒模式闸：把"嵌套三腿 add"（`poison_nested_add_finding`）与已证 ERROR 模式写入 `banned_patterns`，让血泪教训成为自动拦截。

### 层⑥ 回测提交与轮询
- **现状**：`kor_poll_pipeline.py`（唯一入口）+ `kor_fetch_metrics.py`（直连 API）。`polling_tooling_freeze` 纪律值得保留。
- **问题（实证，含已有文档遗漏）**：`--wait` 只睡一次复查一次且**复查时重新登录**（L99）；fetch_metrics 双登录（multisim 分支一次 + 主流程一次）；**ERROR 分支只取前 8 个 child**（L66 `[:8]`，>8 批次错误信息截断——已有文档未捕获）；无指标缓存（review 被迫依赖外部 cache 的诱因）；无配额闸；无超时熔断（waveT 挂起 24h 案例）。
- **优化**：
  - **M12（P0）** 指标本地缓存 `cache/metrics/<alpha_id>.json`：命中即返——review 全面去外部 cache 依赖的前提，配额与耗时双降。
  - **M13（P0）** `--wait` 改轮询循环（指数退避、轮询到 terminal、超时熔断 24h→放弃并记台账）；单进程单登录复用 opener。
  - **M14（P1）** 提交前配额闸（当日 sim 计数 + submit 余量，超阈熔断）+ 单批在飞规则（`pipeline_note_cancel`）固化进提交函数；ERROR 分支取全量 child。

### 层⑦ 指标评审与筛选（最脆弱层）
- **现状**：`review_wave1/3/5.py` 三份同构，**硬编码 `.qoder-cn` 会话 cache 的 .txt dump**（`review_wave1.py` L4），阈值散落三处，未回写台账。实测 141 alpha / 0 candidate / 0 near。
- **优化**：
  - **M15（P0）** `review_wave.py --multisim <id>` 消费 M12 的指标缓存，**彻底移除外部 cache 依赖**；阈值集中 `config/thresholds.json`（sh>1.58/fit>1/2y>1.6/margin>5bp/tvr 5–30%/RA 全过）。
  - **M16（P1）** 评审结果自动回写台账 `submit_ready`/`qualified_alphas` + near 池（sh>1.2）标记增强方向（哪堵墙：CW/2Y/PROD/tvr）。

### 层⑧ 决策与台账
- **现状**：多样性审计（算子探索率 ~12%）静态一次性；数据集切换事后手动标记；5 份 `record_*.py` 直写 169 键大 JSON（`json.dump` 无原子写，整夜战役中断即损坏风险）；4 份 `_tmp_*` 探针残留。
- **优化**：
  - **M17（P0）** 统一 `kor_ledger.py` CLI（add-wave / set-verdict / mark-dead / add-whitelist），内部原子写（tmp+os.replace）+ schema 守卫，取代全部 record 脚本。
  - **M18（P1）** 每波自动累积「算子集/字段集/骨架分布」进台账 `waves[].exploration`，输出探索率曲线；红黄绿灯判死规则（M2）自动触发数据集切换，不再事后补记。
  - **M19（P2）** 清理 `_tmp_*`；`polling_tooling_freeze` 纪律扩展为「scripts/ 禁临时文件」。

---

## 四、全面优化路线图

### P0（先做，一周量级，收益最大）
| 编号 | 项 | 收益 |
|---|---|---|
| M1+M2 | 数据集自动评分 + 探针电池接线 | 数据集从"整波试错"转"48 式探针即判"，21 死的成本结构直接腰斩 |
| M3+M4 | typed catalog + 类型数据驱动 | 从源消除 event 盲废（48 配额事故类） |
| M5 | 生成注入类型 + unused_ops | 直击骨架单一 → CW 墙的结构性根因 |
| M12 | 指标缓存 | 评审去外部依赖、API 配额大降 |
| M15+M9 | 评审/预检去 `.qoder-cn` 硬编码 | 可复现、可迁移（当前最大脆弱点） |
| M17 | 台账 CLI + 原子写 | 防 169 键战场记忆损坏 |

### P1（随后，工程闭环）
M6 生成去重 / M7 gate 合并 / M8 选波接管 / M10 白名单派生 / M11 毒模式闸 / M13 轮询循环+熔断 / M14 配额闸 / M16 台账回写 / M18 多样性累积

### P2（打磨）
M19 清临时文件 + 跨数据集 wave 平衡 + preflight 缓存

### 挖掘策略面（与工程面并行，不依赖代码）
1. **蓝海优先打 `behavioral_signals` / `equity_forum_data`**（三项全满、零竞争）——零竞争字段同时是 CW 免费通行证，一箭双雕。
2. **骨架配给制**：每波强制 trade_when 事件门控 / bucket 离散化 / group 比率骨架占比 ≥30%，打破 rank 线性混合单范式（CW 墙根治方向）。
3. **KPGZmLMl 复活路线**：model170 四腿仅剩 CW 一墙，按手册"跨 Category rank 加法"（P9-v3 批已设计）优先验证——这是全战役离达标最近的一发。
4. **2Y 红灯前置**：所有新数据集探针批必查 max|sh| 式的 2y，<0.6 即红灯（已规则化，须执行到位）。
5. **PROD 早探**：IS 过闸候选立即提交探测读 prodCorr（零成本），避免"IS 全过但 PROD 0.77"的后期才发现。

---

## 五、跨层系统性风险（3 类）

1. **外部 IDE 会话依赖（最高危）**：`.qoder-cn` 路径共 **8 处**（scan_fields×3、scan_aieq、review×3 的 cache dump + preflight 的 verifier skill 路径）——换会话/清缓存即全链路不可复现。M3/M9/M12/M15 组合根除。
2. **无端到端编排与断点续跑**：8 层人工串跑、无 driver、无 checkpoint——不符合项目"一切回测脚本必须断点续跑"的既定纪律。建议 P1 末加 `kor_pipeline.py` 配置驱动串联 ③→⑦，每步落 checkpoint。
3. **配额/成本意识**：重复表达式 92 条、指标反复重拉、数据集整波试错、无配额闸——M2/M6/M12/M14 组合解决。

---

## 六、对已有两份文档的勘误与补充

| 项 | 已有文档（14:13）声称 | 复核事实 |
|---|---|---|
| record 脚本数 | "13 份 record_*.py" | **实际 5 份**（record_cw_manual/dayclose/p10/poison/whitelist_v2） |
| 白名单 schema split | "11 fields-list vs 10 verified-dict" | **实际 15 vs 5**；且 fields-list 格式**已带字段级 type**，verified-dict 不带 |
| preflight 外部依赖 | 未提 | verifier 路径指向 `.qoder-cn\skills\...`（第 8 处外部依赖） |
| CW 墙 | 仅一句带过 | CW=CONCENTRATED_WEIGHT，**61 次击杀、战役最大杀手**，有完整论坛手册与解法体系（§2.1） |
| 快扫协议 | 未提 | 红黄绿灯 + 探针电池 + 2Y 前置规则已成文未接线（§2.2） |
| 毒表达式 | 未提 | 嵌套三腿 add 毒杀整批，14:38 刚实锤入库（§2.3） |
| 配额教训 | "无配额闸" | 完整故事：配额假设被对照批**推翻**，真因毒表达式（§2.3） |
| ERROR 截断 | 未提 | poll_pipeline ERROR 分支只取前 8 child（§层⑥） |

结论：14:13 文档的**工程化分析框架（O1–O27）大体成立**（子进程、双登录、无原子写、硬编码 cache 等均属实），但**挖掘策略层完全缺失**——而本战役 0/21 的真正原因在策略层（三面墙 + 数据集贫瘠 + 骨架单一），不在脚本层。两手都要抓：策略层决定"能不能挖出"，工程层决定"挖得多快多稳"。

---

## 七、下一步行动清单（按依赖排序）

1. 配额重置后：提交 P9-v3（model170 跨 Category CW 解法）+ wave6b_v2 去相关批评审。
2. 落地 M1+M2（评分器+探针接线），对 `behavioral_signals`/`equity_forum_data` 跑探针批三灯判定。
3. 落地 M12+M15（指标缓存+评审重构），摘除 `.qoder-cn` 依赖。
4. 落地 M5（生成注入 unused_ops），下一波起骨架配给制。
5. KPGZmLMl 若 CW 过闸 → submit_ready（注意 48h 配额与 SELF/PROD/DATA_DIVERSITY 三检）。

---

*复核范围：169 键台账全量、102 wave 文件全量统计、24 脚本中关键 7 个逐行核读、21 白名单 schema 普查、7 评审 JSON 汇总。所有「实证」均可回溯到具体文件/键/行号。*
