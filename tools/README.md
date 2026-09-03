# tools/ 通用工具索引

区域无关的战役工具链。约定：
- **退出码**：`0`=PASS/成功，`1`=FAIL/失败（可直接串进 pipeline）
- **网络工具运行环境**：MCP venv（`$WQ_PY` 或 `world-quant-brain-mcp/.venv`），自动 `os.execv` 重启，勿用系统 python
- **skill 依赖路径**：自动解析 `WQ_VALIDATOR_DIR` / `WQ_TOOLKIT_DIR` → `~/.qoder-cn/skills` → `~/.workbuddy/skills`，**禁止硬编码**

## 提交前闸门（构建候选池后、回测前）

| 工具 | 用途 | 取代 |
|---|---|---|
| `wave_gate.py` | 每波门禁编排：语法校验 + 5 闸 + 六维多样性 + 质量预估（EXPECTED_BLOCK 默认标注，`--quality-block` 硬拦截），一键落盘 `cache/gate_wave<N>_<ds>.{json,txt}` | `tracking/<R>/scripts/_gate_waveNN.py` 族 |
| `pool_diversity.py` | 候选池表达式结构多样性评估（算子熵/骨架配额/字段集中度/预处理/成对相似度/主导族风险，六维），`--file/--exprs/DB`，`--json` 落盘；已被 `wave_gate.py` 集成调用 | 手写多样性统计脚本 |
| `quality_predict.py` | 候选池质量预估（回测前）：三层先验预估 Sharpe/Fitness + 本地结构代理预估 SELF_CORR 风险，输出 EXPECTED_PASS/REVIEW/EXPECTED_BLOCK；`--status UNSUBMITTED` 直筛存量池，已被 `wave_gate.py` 集成调用 | 手写相关性/质量预判脚本 |
| `gate.py` | 战役统一提交前闸门（5 闸 + 批级多样性，权威实现在 skill toolkit） | — |
| `expr_lint.py` | 算子签名/字段白名单快速门禁（非战役场景） | — |
| `corr_precheck.py` | 相关性墙预判（设计阶段字段重叠检查） | — |

## 回测与状态

| 工具 | 用途 | 取代 |
|---|---|---|
| `mcp_5slot_batch.py` | 五槽并发回测（MCP 驱动） | — |
| `batch_status.py` | 批次/子任务状态查询与 `--watch` 轮询（multisim 或单条） | `tracking/_scratch/check_*batch*.py`、`track_mea_super_resume.py` 轮询段 |
| `harvest_multisim.py` | multisim 收批：拉 children → 拉 alpha 详情 → 关联 expressions → 可选 upsert backtest_rows | `tracking/*/scripts/poll_wave*.py`、手写收批脚本 |
| `submit_batch.py` | 批量提交（`--spec` 支持逐批不同设置） | 31 个 `_submit_*.py` |

## 探针编排（新数据集首探）

| 工具 | 用途 | 取代 |
|---|---|---|
| `probe_batch_mode.py` | 2+6 探针批模式：L0（2 条）快速判死 → L1（6 条）信号确认，真实回测（入库→pipeline→DB 拉指标） | 手写 8 探针表达式 + 手动判定 |
| `tiered_probe.py` | 三层探针编排器：L0 判死 → L1 确认 → L2 ModeA 变体自动升级；组合腿快腿轮换（fast_pool 多样性）；慢腿预处理轮换（raw/reverse/ts_decay_linear） | 手写 ModeA 变体波 |

> `wave_gate.py --probe-mode` 只做门禁阶段探针分配标记（结构预判），真实回测判死走 `probe_batch_mode.py` / `tiered_probe.py`。

## SUPER alpha 流水线

| 工具 | 用途 | 取代 |
|---|---|---|
| `sa_probe.py` | 组件池探针：≥10 ACTIVE REGULAR 硬前置，GO/BLOCKED | `probe_kor_sa.py`、`tracking/_scratch/probe_sa2_*.py` |
| `super_build.py` | select / status / probe / submit 四子命令全流程 | `track_mea_super.py` / `_resume` / `_submit` 三件套 |

## 提交判定

| 工具 | 用途 | 取代 |
|---|---|---|
| `submit_verdict.py` | 提交层判定双视图：模拟 checks + `GET /alphas/{id}/submit`（403 盲区拦截，零配额） | 手写 GET/POST submit 探针 |

## 代码体检 / 清理

| 工具 | 用途 | 取代 |
|---|---|---|
| `scan_deadcode.py` | 死代码只读扫描：未用 import + 死定义（排除注册式装饰器 @mcp.tool()/@fixture 等反射调用）；支持 `--path` 单文件/子目录、`--out` JSON 报告 | `tracking/_scratch/_scan_deadcode*.py` |
| `fix_bom.py` | BOM(U+FEFF) 剥离修复：默认 `--dry-run` 列出含 BOM 的 .py；`--apply` 才修（备份 + CJK 数量校验 + ast.parse 校验） | `tracking/_scratch/_fix_bom.py` |
| `clean_unused_imports.py` | 清理未用 import：默认 `--dry-run` 列出；`--apply` 才删（**跨文件 re-export 校验**防 SHAPE_CLASSES 误删 + `.bak_imp` 备份 + ast.parse 校验）；可 `--report` 接 scan_deadcode 的 JSON | `tracking/_scratch/_clean_unused_imports.py` |

> 三者均遵循 dead-code-cleanup skill 红线：**默认只读/dry-run，删除动作必须显式 `--apply`**。原稿已归档 `attic/tools_archive/_2026-08-28_*`。

## MCP 体检

| 工具 | 用途 |
|---|---|
| `mcp_ping.py` | MCP 服务连通性 + 调用时长测试：对 `.mcp.json` 全部服务做 stdio 握手（initialize/tools/list）+ 只读探针真实调用计时（wq-brain-http 3 个平台只读探针 / wqb-db 4 个 DB 查询）。`--service X` 单服务、`--full` 附全工具注册清单、`--timeout N` 握手超时。退出码 0=全过 / 1=有失败。零配额消耗（探针全部无副作用） |

## 纪律（AGENTS.md §9）

1. **禁止新建** `_gate_*` / `check_*batch*` / `probe_*sa*` / `_submit_*` / `track_*_super*` 类一次性脚本；先用本索引查工具。
2. 缺参/缺能力 → 改对应工具加参数（保持 `--help` 自文档），不写新脚本。
3. 一次性排障探针仍可写 `tracking/_scratch/`，但完成即归档 `attic/`，不留在活跃目录。

## 相关参考

- 战例权威实现：`~/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts/`（`WQ_TOOLKIT_DIR`）
- 平台 API 封装：`world-quant-brain-mcp/brain_api.py`（`BrainApiClient`，自带 429 退避/Redis 缓存）