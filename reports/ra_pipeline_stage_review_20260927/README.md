# RA 九步流水线沙箱 dry-run —— 附件

主报告：[`../ra_pipeline_stage_review_20260927.md`](../ra_pipeline_stage_review_20260927.md)

| 文件 | 作用 |
|---|---|
| `dryrun_transcript.txt` | 2026-09-27 演练完整实录（路径已脱敏为 `<SBX>` / `<SANDBOX>`；重复的启动自检告警行已折叠） |
| `reproduce.sh` | 一条命令复现：在临时目录 `git archive HEAD`、建 mcp stub、本地装 `ply`/`msgpack`、播种合成库、跑演练 |
| `seed_db.py` | 合成种子库（region=KOR，虚构数据集 `syn_analyst`；全部为夹具数字，不代表生产） |
| `sbx_guard.py` | 隔离护栏：拦截 socket / subprocess，记录每个探针的文件系统与库内容变化 |
| `run_dryrun.py` | 九步逐阶段演练 + 19 个 workflow 节点 dry-run 契约扫描 |

全部脚本只在临时工作目录里的仓库副本上运行，不读写真实仓库与生产库 `data/wqb.db`，不访问平台。
