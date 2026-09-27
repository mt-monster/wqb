# RA 九步流水线 dry-run —— 附件

主报告：[`../ra_pipeline_stage_review_20260927.md`](../ra_pipeline_stage_review_20260927.md)（第一轮 §12，第二轮 §14）

## 第一轮：沙箱

| 文件 | 作用 |
|---|---|
| `dryrun_transcript.txt` | 2026-09-27 演练完整实录（路径已脱敏为 `<SBX>` / `<SANDBOX>`；重复的启动自检告警行已折叠） |
| `reproduce.sh` | 一条命令复现：在临时目录 `git archive HEAD`、建 mcp stub、本地装 `ply`/`msgpack`、播种合成库、跑演练 |
| `seed_db.py` | 合成种子库（region=KOR，虚构数据集 `syn_analyst`；全部为夹具数字，不代表生产） |
| `sbx_guard.py` | 隔离护栏：拦截 socket / subprocess，记录每个探针的文件系统与库内容变化 |
| `run_dryrun.py` | 九步逐阶段演练 + 19 个 workflow 节点 dry-run 契约扫描 |

以上脚本只在临时工作目录里的仓库副本上运行，不读写真实仓库与生产库 `data/wqb.db`，不访问平台。

## 第二轮：P0 修复后的真实环境复跑（`realenv/`）

| 文件 | 作用 |
|---|---|
| `realenv/run_realenv.py` | 按 `.mcp.json` 翻译成本机路径，经 stdio 真实启动 `wqb-db` 与 `wq-brain-http`；把 `tracking/KOR` 的真实历史经 MCP 写工具导入；九步逐阶段演练；另起修复前原始副本的两个 server 做 P0 对照 |
| `realenv/reproduce_realenv.sh` | 一条命令复现（可选环境变量：`REALENV_SCRATCH`、`PRE_FIX_REV`、`REALENV_ALLOW_DB_SWAP`） |
| `realenv/realenv_transcript.txt` | 最终一遍的完整实录（路径已脱敏为 `<repo>` / `<scratch>` / `<base>`） |

这一轮**会**在真实仓库里运行，保护措施如下：
- `data/wqb.db` 演练期间临时移开，结束（含异常退出）后移回；超过 5MB 的库需要显式设 `REALENV_ALLOW_DB_SWAP=1` 才会动。
- `tracking/KOR/priors/` 有未提交改动时拒跑；真实 assemble-priors 会重写该目录，演练结束时 git 复原。
- 演练中 `wave_gate` 在仓库根造出的杂散目录（报告 N19）会被检测并删除。
- 不需要、也不读取 BRAIN 凭据（`world-quant-brain-mcp/.env`）。平台类工具只记录无凭据时的失败形态，零平台写入。
