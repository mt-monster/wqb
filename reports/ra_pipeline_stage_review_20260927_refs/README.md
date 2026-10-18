# RA 九步流水线 dry-run —— 附件

主报告：[`../ra_pipeline_stage_review_20260927.md`](../ra_pipeline_stage_review_20260927.md)（第一轮 §12，第二轮 §14，第三轮 §14.8，第四轮 §14.9）

## 第一轮：沙箱

| 文件 | 作用 |
|---|---|
| `dryrun_transcript.txt` | 2026-09-27 演练完整实录（路径已脱敏为 `<SBX>` / `<SANDBOX>`；重复的启动自检告警行已折叠） |
| `reproduce.sh` | 一条命令复现：在临时目录 `git archive HEAD`、建 mcp stub、本地装 `ply`/`msgpack`、播种合成库、跑演练 |
| `seed_db.py` | 合成种子库（region=KOR，虚构数据集 `syn_analyst`；全部为夹具数字，不代表生产） |
| `sbx_guard.py` | 隔离护栏：拦截 socket / subprocess，记录每个探针的文件系统与库内容变化 |
| `run_dryrun.py` | 九步逐阶段演练 + 19 个 workflow 节点 dry-run 契约扫描 |

以上脚本只在临时工作目录里的仓库副本上运行，不读写真实仓库与生产库 `data/wqb.db`，不访问平台。

## 第二轮 – 第四轮：P0、P1 修复后的真实环境复跑（`realenv/`）

| 文件 | 作用 |
|---|---|
| `realenv/run_realenv.py` | • 按 `.mcp.json` 翻译成本机路径，经 stdio 真实启动 `wqb-db` 与 `wq-brain-http`（env 原样）。<br>• 把 `tracking/KOR` 的真实历史经 MCP 写工具导入。<br>• 九步逐阶段演练，每步打印【阶段小结】（输入 / 处理 / 输出变化 / 价值判定）。<br>• 另起修复前原始副本的两个 server 做 P0 对照。<br>• 末尾打印 P1 验证清单（✅ / ❌ / ➖ 三态） |
| `realenv/reproduce_realenv.sh` | 一条命令复现（可选环境变量：`REALENV_SCRATCH`、`PRE_FIX_REV`、`REALENV_ALLOW_DB_SWAP`） |
| `realenv/realenv_transcript.txt` | 第四轮（P1 第二批 R22 / R5 / R12 / R4 / R3 修复后）最终一遍的完整实录（路径已脱敏为 `<repo>` / `<scratch>` / `<base>` / `~`） |
| `realenv/realenv_transcript_r18_r21.txt` | 第三轮（P1 第一批 R18–R21 修复后）实录，第二批各项对照它的步 5–9 与附 A |
| `realenv/realenv_transcript_p0.txt` | 第二轮（P0 修复后、P1 修复前）实录，供同名步骤逐行对照 |

这一轮**会**在真实仓库里运行，保护措施如下：
- `data/wqb.db` 演练期间临时移开，结束（含异常退出）后移回；超过 5MB 的库需要显式设 `REALENV_ALLOW_DB_SWAP=1` 才会动。
- `tracking/KOR/priors/` 有未提交改动时拒跑；真实 assemble-priors 会重写该目录，演练结束时 git 复原。
- 演练中 `wave_gate` 在仓库根造出的杂散目录（报告 N19）会被检测并删除。
- 步 5 的 R12 探针把写入指到演练库的副本；`probe_batch_mode --dry-run` 写进 `tracking/KOR/cache/` 的结果文件由演练删除。
- 不需要、也不读取 BRAIN 凭据（`world-quant-brain-mcp/.env`）。平台类工具只记录无凭据时的失败形态，零平台写入。
