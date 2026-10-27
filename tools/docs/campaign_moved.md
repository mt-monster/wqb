# EUR 全数据集流水线：唯一入口在哪

**2026-10-25 定稿：EUR 只有一条流水线、一套脚本，位于技能目录：**

```
C:\Users\MENGTAO\.workbuddy\skills\wq-brain-ra-eur\scripts\
    eur_runner.py           托管器（停滞重启 / 空转熔断 / 单实例锁）
    eur_main.py             流水线入口（--datasets / --audit / --only-cats …）
    wqb_campaign/           实现包
        config.py           路径与区域配置（EUR 无后缀；IND 等用 _<REGION>）
        lock.py             PID 单实例锁（防同一断点双写）
        persist.py          checkpoint / results / heartbeat 原子读写
        bad_tokens.py       平台拒绝名单（含结构算子保护）
        transport.py        sims_terminal / wait_slot / dispatch / harvest
        fields.py           字段选择（语义分类 / 幽灵过滤 / full+probe）
        generate.py         模板族 + build_exprs + 后处理电池
        audit.py            check_prod / year_profile
        lit.py              点塔计数
        sweep.py            设置轴补扫
        report.py           digest / progress
        pipeline.py         run()（原 main）
    campaign_semantics.py   字段语义事实源
    campaign_year_audit.py  逐年画像审计
    campaign_final_report.py 成果报告
    run_eur.cmd             启动器
```

## 没有副本、没有车道

原 `tools/full_template_campaign.py` + `tools/campaign_supervisor.py` + `tools/wqb_campaign/`
已全部归档到 `attic/campaign_dup_20261025/`（可回溯，不在执行路径上）。

**车道（lane）概念已取消。** 曾用 `WQB_CAMPAIGN_LANE` 让同一区域并行跑两套策略，
用户 2026-10-25 定稿：**EUR 就一套车道**。现在同一区域靠 `lock.py` 的 PID 锁保证
「一个 supervisor + 一个 campaign」，第二个实例直接拒绝启动。

## 启动

```bat
C:\Users\MENGTAO\.workbuddy\skills\wq-brain-ra-eur\scripts\run_eur.cmd
```

或手动：

```bash
cd C:\Users\MENGTAO\.workbuddy\skills\wq-brain-ra-eur\scripts
set WQB_REPO_ROOT=D:\coding\traeCN_project\wqb
set WQB_CAMPAIGN_REGION=EUR          # 省略即 EUR
python eur_runner.py --stall-sec 900 --check-sec 60 --zero-alpha-stop 3 --max-inflight 4
```

可选旋钮（不设即原始行为）：

| 变量 | 作用 | 默认 |
|---|---|---|
| `WQB_CAMPAIGN_FULL_CAP` | 每集 full 层字段上限 | 8 |
| `WQB_CAMPAIGN_STATE_DIR` | 断点/报告目录 | `<repo>/results` |
| `WQB_CAMPAIGN_REGION` | 切区域（IND/USA… 断点自动加 `_<REGION>`） | EUR |

## 断点与报告

| 文件 | 说明 |
|---|---|
| `results/full_template_campaign_checkpoint.json` | 断点（`done` 列表 + 已派批次） |
| `results/full_template_campaign_results.json` | 每集判定与全部 alpha 指标 |
| `results/campaign_digest.md` | 一集一行的进度摘要 |

## 仍然共享的东西（有意为之）

- `tools/submit_batch.py` + `tools/_pyenv.py`：通用派发工具，多个流程在用，不属于本流水线。
- `cache/bad_tokens.json`：平台拒绝名单（写为原子替换）。
