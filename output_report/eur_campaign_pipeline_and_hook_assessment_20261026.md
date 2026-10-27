# EUR Campaign 流水线工作流全景 + 钩子适用性评估

生成：2026-10-26 12:05　｜　范围：`wq-brain-ra-eur`（EUR 战役引擎）+ 仓库级守门点

---

## 0 一句话结论

流水线是**两层**结构：外层是 ra-pipeline 的九步 SOP（人/Agent 编排），内层是
`wqb_campaign` 引擎的逐集状态机（12 个阶段）。**绝大多数守门点应该在代码内**，
因为判定依赖流水线内部状态；**钩子只适合守「不可逆 + 可被绕过 + 判定只看外部输入」的边界**。

钩子唯一不可替代的价值是**拦绕过路径**（人或 Agent 不跑脚本、直接调 MCP 工具）。
它**只能否决，不能修复** —— 所以"yp 算不出来"这类根因永远只能在代码里解。

---

## 1 外层：ra-pipeline 九步 SOP

| 步 | 阶段 | 主入口 | 产物 | 守门形式 |
|---|---|---|---|---|
| 1 | S-PRE 查表 | `wq-brain-campaign-matrix` + `wqb-db` 工具 | 选区/选集决策 | 人工 |
| 2 | S0 数据集体检 | `workflow_campaign(stage="S0")` | 数据集画像 | 代码 |
| 3 | S1 字段扫描 | `workflow_campaign(stage="S1")` | 字段语义/形态 | 代码 |
| 4 | S2 概念生成 | `workflow_gem` | 表达式波 | 代码（幽灵算子/arity） |
| 5 | S2→S3 门禁 | `wave_gate` / `tools/wave_gate.py` | gate_results | 代码（硬门） |
| 6 | S3 并发回测 | `workflow_batch_track` | IS 指标 | 平台（并发/额度） |
| 7 | S4 诊断改进 | `workflow_campaign(stage="S4")` | 改进变体 | 代码 |
| 8 | S4→S5 判定 | `brain-alpha-robustness` → `submit_verdict` → `check_correlation(refresh)` → **用户确认** → `workflow_submit_alpha` | 提交 | **代码闸 + 人工 + 不可逆** |
| 9 | S6 复盘回写 | `upsert_wave_result` / `seal_dead_end` | KB/DB | 代码 |

---

## 2 内层：campaign 引擎 12 阶段（`wqb_campaign/pipeline.py`）

| # | 阶段 | 做什么 | 关键参数 | 失败模式 |
|---|---|---|---|---|
| 0 | preflight | 载入平台黑名单 token、lit 计数、并发上限 | `BAD_TOKENS` | 黑名单缺失 ⇒ 整批 FAIL |
| 1 | 选集排序 | lit→virgin→类目→暴露多样性→EV | — | 顺序差 ⇒ 好集被跳过 |
| 2 | skip 判定 | coverage < eff_min（0.6；处女地 0.35）、`n_fields<3` | `--min-cov` | **46% 集被跳过** |
| 3 | 字段选择 | 语义分类 → 每维 2 个代表 → full ≤8 + probe ≤12；幽灵字段平台认证 | `PER_DIM`/`FULL_FIELD_CAP` | 百字段集只测 8 个（覆盖率 0.3%） |
| 4 | 形态判定 | form / exposure 标注（VECTOR 特判） | — | 误判 ⇒ 秒拒且整批 CANCELLED |
| 5 | 表达式构造 | L1×L2 交叉 12 族 + 双窗；probe 只 1 条 lvl_rk | `FREQ_WIN` | 结构错 ⇒ 空批 |
| 6 | 派发 | 每族均分 ≤10/批，`wait_slot` 控在飞 | `--max-inflight` | 单条批 ⇒ `COMPLETE children=0` |
| 7 | 收割 | 三态；前 2 批 FAIL 且无果 ⇒ abort 本集 | — | 平台侧算子报错 |
| 8 | 毒化自愈 | 整批 FAIL 的式剔黑名单后重派一次 | — | 未自愈 ⇒ 白丢 |
| 9 | stage2 电池 | `S≥1.35` 的 top3 × 6 变体（4 稀疏 + 2 幂） | `STAGE2_MIN_S` | 触发线过低 ⇒ 白烧 |
| 10 | 载体扩散 | 最强族补跑未覆盖 probe 字段 | — | — |
| 11 | 设置轴扫 | `1.2≤S<1.58` 时扫 universe/中性化 | 三档 | **按集级 max_s 判 ⇒ 漏扫真候选** |
| 12 | 判定 | `joint` → ALIVE / SPLIT / BORDERLINE / DEAD / **INVALID_SAMPLE**；yp + 十年代码闸；prod 三颗 | — | **yp fail-open（已修）** |

---

## 3 现有守门点盘点

| 守门点 | 位置 | 类型 | 是否 fail-closed |
|---|---|---|---|
| 提交总开关 | `wqb.config.ALLOW_ALPHA_SUBMIT`（env `WQB_ALLOW_ALPHA_SUBMIT=1` 才放行） | 代码 | ✅ |
| 提交判定否决权 | `tools/submit_verdict.py`（只拦不放） | 代码 | ✅（未捕获异常也归 BLOCKED） |
| 相关性终验 | `check_correlation(refresh=True)` | 平台 + 代码 | ✅ |
| yp / 十年数据 | pipeline `deliverable` | 代码 | ✅（今天由 fail-open 改为 fail-closed） |
| 单实例锁 | `lane_<REGION>_<LANE>.lock` + 判活修复 | 代码 | ✅ |
| 空转熔断 | `--zero-alpha-stop` | 代码 | ✅ |
| 平台额度 | 平台侧 WARNING | 平台 | ⚠ 仅告警不阻断 |
| 凭据禁读 | AGENTS.md 约定 | **约定** | ❌ 无强制 |
| 破坏性文件操作 | 无 | — | ❌ 无强制 |
| 绕过脚本直调 MCP 提交 | 无 | — | 依赖 `ALLOW_ALPHA_SUBMIT` |

---

## 4 钩子适用性评估

### 4.1 判据（5 条，全中才算适合）

| 代号 | 判据 | 说明 |
|---|---|---|
| **C1** | 判定**不需要**流水线内部状态 | 只看工具参数 / 本地文件 / 平台返回值 |
| **C2** | 失败**不可逆**或代价高 | 提交、删除、泄密 |
| **C3** | 存在**绕过路径**需拦 | 人或 Agent 可直接调工具，不跑脚本 |
| **C4** | 逻辑**稳定** | 不随实验频繁改 |
| **C5** | 拦截**成本低** | 毫秒级，不调平台、不占额度 |

> 关键：钩子**只能否决，不能修复**。凡属"数据算不出来 / 状态缺失"的根因，一律回代码。

### 4.2 逐点结论

| 守门点 | C1 | C2 | C3 | C4 | C5 | 结论 |
|---|---|---|---|---|---|---|
| **提交前全套断言**（verdict==可提交 且 yp 非空非 fragile 且 prod/self<0.7） | 部分（读 results 反查 alpha→dataset） | **极高**（不可逆） | **高**（MCP 工具可绕过脚本） | 稳定 | 低 | **强推荐**（唯一真钩子场景） |
| **凭据禁读**（`.env` / `credentials`） | **是**（路径匹配） | 高（泄密） | 高 | 稳定 | 极低 | **强推荐**（当前只有约定，零强制） |
| **破坏性操作**（删除 `results/` `checkpoint` `data/wqb.db`） | 是（命令匹配） | 高 | 中 | 稳定 | 极低 | 推荐 |
| **提交后补设 properties**（提交节点会覆盖 name） | 部分（需 alpha_id） | 中（元数据丢失） | 高 | 稳定 | 低 | 推荐（PostToolUse 自动补） |
| 派发前并发/额度闸 | 部分（需查平台计数） | 中 | 中 | **变动** | 中（调 API） | 一般；`transport.wait_slot` 内做更好 |
| 表达式预检（幽灵算子/arity） | 是（纯本地） | 中（浪费仿真） | 高 | 稳定 | 低 | 可选；已有 `preflight_expressions` |
| **yp / deliverable / verdict 判定** | **否**（需引擎内部状态） | — | — | — | — | **不适合** → 代码（已修） |
| 单实例锁 / 空转熔断 | **否** | 中 | — | — | — | 不适合 → 代码（已有） |
| 论坛检索限速 | 是 | 低 | 低 | 变动 | 中 | 不必要 |

### 4.3 环境现状

- `~/.workbuddy/settings.json` **无 `hooks` 键** ⇒ 钩子机制未配置，需从零建。
- `toolControl` 只支持 `disabledToolIds` / `disabledMcpServerIds`（整体禁用），**不支持条件逻辑**。
- 仓库内 `.workbuddy/` 只有 `backup/` 与 `memory/`，无 hook 脚本目录。

⇒ 引入钩子 = 新建一套配置 + 脚本 + 维护，**不建议为了"补 yp"这样的根因问题引入**。

---

## 5 推荐落地顺序

| 优先 | 做什么 | 在哪 | 为什么 |
|---|---|---|---|
| **P0** | 提交前断言（yp/prod/verdict 三重） | 钩子 `PreToolUse` → `workflow_submit_alpha` / `workflow_execute` | 唯一"不可逆 + 可绕过"的场景；等 `ALLOW_ALPHA_SUBMIT` 真被打开时它就是唯一守门人 |
| **P0** | 凭据禁读 | 钩子 `PreToolUse` → `Read`/`Bash`，路径含 `.env` 即拒 | 当前零强制，代价极低 |
| P1 | 破坏性文件操作保护 | 钩子 `PreToolUse` → `Bash`，匹配 `rm -rf results/` `checkpoint` `wqb.db` | 今天已发生过整批进程被杀、锁残留 |
| P1 | 提交后补 properties | 钩子 `PostToolUse` → 提交成功后 `set_alpha_properties` | 提交会覆盖 name，需补 descriptions |
| **不进钩子** | yp 判定 / 设置轴扫触发 / 并发闸 / 单实例锁 | 代码 | 依赖内部状态或需精确控制 |

### P0 钩子骨架（提交前断言）

```python
# hooks/pre_submit_guard.py  —— PreToolUse: workflow_submit_alpha / workflow_execute
import json, os, sys

payload = json.load(sys.stdin)
tool = payload.get("tool_name", "")
if not tool.endswith(("workflow_submit_alpha", "workflow_execute")):
    sys.exit(0)                      # 非提交类，放行

args = payload.get("tool_input") or {}
if str(args.get("node", "")) not in ("submit_alpha", "workflow_submit_alpha") \
   and "workflow_submit_alpha" not in tool:
    sys.exit(0)

alpha_id = args.get("alpha_id") or (args.get("args") or {}).get("alpha_id")
if not alpha_id:
    print("BLOCKED: 提交调用缺少 alpha_id，无法校验 yp/prod", file=sys.stderr)
    sys.exit(2)

ROOT = os.environ.get("WQB_REPO_ROOT", r"D:\coding\traeCN_project\wqb")
res = json.load(open(os.path.join(ROOT, "results",
                                  "full_template_campaign_results.json"), encoding="utf-8"))
ds = None
for k, v in (res.get("results") or {}).items():
    if isinstance(v, dict) and any(a.get("alpha") == alpha_id for a in (v.get("alphas") or [])):
        ds, rec = k, v
        break
if ds is None:
    print(f"BLOCKED: {alpha_id} 不在 results 里（未经流水线评估）", file=sys.stderr)
    sys.exit(2)

yp = rec.get("year_profile")
if not isinstance(yp, dict):
    print(f"BLOCKED: {ds} 年度画像缺失（fail-closed）", file=sys.stderr); sys.exit(2)
if yp.get("fragile"):
    print(f"BLOCKED: {ds} 样本无效（首年{yp.get('first_year')}/{yp.get('n_years')}年）",
          file=sys.stderr); sys.exit(2)
if rec.get("verdict") not in ("ALIVE",):
    print(f"BLOCKED: {ds} verdict={rec.get('verdict')}，非 ALIVE", file=sys.stderr); sys.exit(2)

sys.exit(0)                          # 放行
```

---

## 6 今天踩过的坑（对应到流程缺陷）

| 缺陷 | 表现 | 根因 | 已修 |
|---|---|---|---|
| yp fail-open | yp=null 反而放行，`quant_factor_lib` 被当候选挖了 2 小时 | `not (yp and fragile)` 对 None 恒真 | ✅ 改 fail-closed |
| yp 恒为 None | 所有集 yp 缺失 | `from wqb_tools import _get_json` 模块已丢失，异常被吞 | ✅ 内联实现 |
| 设置轴扫漏扫 | `KPmV08Vx`(S1.48) 从未被扫 | 触发按**集级 max_s**，非按 alpha | ⬜ 待修 |
| stage2 触发线过低 | 6 集烧 90 条仿真、0 收获 | 0.8 触发，电池全是单调变换 | ✅ 提到 1.35 |
| prod 只测 max-S 一颗 | risk70 测在市值暴露上白测 | 单点采样 | ✅ 改测 3 颗 |
| `check_prod` 内轮询过短 | 平台要 1-5 分钟，60s 必放弃且重调会重算 | 超时设置 | ✅ 拿满剩余预算 + busy 快速退出 |

---

## 7 落地记录（2026-10-26 12:40）

### 7.1 设置轴扫改为按 alpha 判（`wqb_campaign/sweep.py`，EUR/KOR 同步）

原判据 `1.2 <= max_s < 1.58` 是**集级**的 ⇒ 集级 max_s ≥1.58 时整集跳过设置轴扫，
集内真正落在带内的候选（例：`KPmV08Vx` S=1.48）从未被扫过。现改为按 **alpha** 判：
取集内所有落在 [1.2,1.58) 的 alpha，按 S 降序取前 2；若仅 1 颗，则补 1 颗最强非带内构造凑批
（单条批会变成空批——这是既有约束）。

### 7.2 钩子已落地并通过自测

| 项 | 内容 |
|---|---|
| 脚本 | `.workbuddy/hooks/campaign_guard.py` |
| 配置 | `~/.workbuddy/settings.json` 的 `hooks` 键（用户级；备份 `.bak_hooks_20261026`）；项目级 `.workbuddy/settings.json` 保留同份副本 |
| 事件 | `PreToolUse`（提交类 / Read·Grep·Glob / Bash）、`PostToolUse`（提交类） |
| 自测 | `tools/hook_selftest.py` —— **9 场景全过** |

| 守门 | 触发 | 决策 |
|---|---|---|
| **G1 提交前断言** | `workflow_submit_alpha` / `workflow_execute(node=submit)` / `submit_verdict` | verdict=ALIVE + yp 有效且非 fragile + prod<0.7，缺一即 exit 2 |
| **G2 凭据禁读** | 文件工具的路径字段；Bash 中「读类动词 + 同段文件名」 | exit 2 |
| **G3 破坏性操作** | Bash 递归删除命中 `results/` `checkpoint` `wqb.db` `lane_` | exit 2 |
| **G4 提交后提醒** | 提交类工具 `PostToolUse` | 非阻塞提示补 `set_alpha_properties` |

### 7.3 实测踩到的四个坑（已全部修复）

| 坑 | 现象 | 修法 |
|---|---|---|
| guard 内部调 `allow()` | `sys.exit(0)` 让后续检查全部跳过 ⇒ 删除保护形同虚设 | 各 guard 只 `deny()` 或 `return`，统一在 main 末尾放行 |
| 按子串匹配 | 任何含该文件名的命令行都被拦（含文档、echo）⇒ 误杀自己的测试命令 | 文件工具看路径字段；Bash 要求动词与同名参数同段 |
| heredoc 正文被当参数 | 写文档时正文提到受保护路径/凭据名，整条命令被拦 | 抽 `_cmd_head()`：命中 heredoc 定界符后只分析其之前的部分 |
| `" ".join()` 尾随空格 | `$` 锚点失效 ⇒ 文件工具场景漏拦 | 改按路径分段判定，不用正则锚点 |

**结论：钩子必须实测**。前三版都是「看起来对」但行为错，靠 9 场景自测才逐个暴露。

### 7.4 回滚

```bash
cp ~/.workbuddy/settings.json.bak_hooks_20261026 ~/.workbuddy/settings.json
```

---

## 8 归因分析：为什么引擎不做钩子，完整性校验做

### 8.1 判断依据

| 判据 | 归因引擎 | 归因完整性校验 |
|---|---|---|
| C1 不需流水线内部状态 | ❌ **不合格**：需要「同字段多变体横向矩阵」（族 × maxS × 中位数）、sweep 轴结果、年度画像 | ✅ 只看本地台账有无该集的记录 |
| C2 失败不可逆 | ❌ 归因是知识产出，不改变不可逆结果 | ⚠ 弱：带着未归因候选收工，下次要重算 |
| C3 存在绕过路径 | — | ✅ 人/Agent 可以直接收工不做归因 |
| C4 逻辑稳定 | ✅ | ✅ |
| C5 拦截成本低 | ❌ **不合格**：要调平台取年度数据/相关性 | ✅ 读两个本地文件，毫秒级 |

⇒ **引擎进代码（流水线阶段），完整性校验进钩子（Stop）**。

理由的核心：钩子只能看到**单次工具调用的参数**，而归因的输入是**整个变体矩阵**。
把归因塞进钩子，要么拿不到矩阵算不出东西，要么为了拿矩阵去调平台（违反 C5 且会拖慢每次工具调用）。

### 8.2 落地

| 组件 | 位置 | 职责 |
|---|---|---|
| 归因引擎 | `wqb_campaign/attribution.py`（EUR/KOR 同步） | `build_record()` 按模板族算 ΔS、判赢家、生成结论句；`append_record()` 落 jsonl |
| 流水线接线 | `pipeline.py` 判定后、存结果前 | 每个集自动记一条，含 verdict / yp / sweep / 族矩阵 |
| 回溯扫描 | `tools/attribution_scan.py` | 补历史 + 出跨集轴效应汇总 + 写 `output_report/attribution_matrix_20261026.md` |
| 完整性钩子 | `campaign_guard.py::guard_attribution`（`Stop` 事件） | 有 `S≥1.5` 的候选却无归因记录 ⇒ exit 2，不许收工 |

台账：`results/attribution_ledger.jsonl`（每行一条，`jq`/pandas 可直接消费）

### 8.3 回溯归因的首批结论（21 个可归因集）

**赢家族**：`pp`（后处理电池）10 次、`lvl_rk` 5 次、其余各 1 次。

**各轴相对赢家的平均 ΔS**（越接近 0 = 该轴越不拖后腿）：

| 轴 | n | 平均 ΔS |
|---|---|---|
| 后处理电池（L4 截面） | 21 | **−0.016** |
| 水平量·截面秩 | 21 | −0.282 |
| 双窗（L3 时间结构） | 20 | −0.399 |
| 水平量·时序秩 | 19 | −0.571 |
| 水平量·分位 | 19 | −0.583 |
| 水平量·zscore | 19 | −0.600 |
| 水平量·scale | 19 | −0.617 |
| 变化量·秩 | 14 | −0.645 |
| 一阶差分·秩 | 20 | −0.752 |
| 二阶差分·秩 | 16 | **−1.009** |
| 语义代表值 | 9 | **−1.140** |

**三条可执行结论**：

1. **EUR 的 S 几乎全部来自「后处理电池（L4 截面处理）」** —— 它 10/21 次成为赢家，且相对赢家只掉 0.016。
   这意味着选错 L4 就等于白测；而 L1/L2 的变换只要不太离谱，影响远小于 L4。
2. **差分类变换是负梯度**：一阶 −0.75、二阶 **−1.01**。今天在 `qfl_cassie_model_merton` 上
   实测的 B1（双差分→单差分）−1.00、B2（外差 22→66）−1.06 与这个统计完全吻合。
3. **「语义代表值」是最差轴**（−1.14，n=9）：直接把代表字段当信号用，几乎总是弱于其它构造。

族间跨度均值 **1.31**、最大 **2.58** ⇒ 同一字段换错轴可损失 1.3 个 Sharpe，
比大多数「信号本身好坏」的差异还大。**选轴比选字段更值钱**。

### 8.4 Stop 钩子实测

| 场景 | 结果 |
|---|---|
| 台账存在、覆盖所有 S≥1.5 的集 | exit 0（放行） |
| 暂时移走台账 | **exit 2**，并列出 8+ 个未归因集，提示跑 `tools/attribution_scan.py` |
