---
last_verified: 2026-09-29
name: brain-inspect-raw-template-create-setting
description: "把外部 / 手写的 idea JSON（*_idea_*.json：template / idea / expression_list）解析出来，核对该 region/delay 的合法仿真设置选项，并把表达式按给定设置写入 expressions 表（S2→S3 的 DB 入库通道之一）。只用于外部或手写的 idea 文件；GEM 生成的表达式已直接入库，不必经过本 skill。"
layer: L3
allowed-tools:
  - Read
  - Bash
user-invocable: true
---

# brain-inspect-raw-template-create-setting

## 职责边界

- **本 skill 负责**：两件事——① 解析**外部 / 手写**的 idea JSON，核对合法设置选项（`sim_options_snapshot` / `settings_candidates`），并用 `build_alpha_list.py` 把表达式按给定设置**写入 `expressions` 表**；② 新区域合法设置选项的快照。**设置决策不在这里做**：设置一律来自战役 `settings.json` / profile `settings_proven` / pipeline 的 `--set`、`--neutralization`。
- **本 skill 不做**：不写 `settings.json`、不发起回测、不改表达式、不提交；**不与 GEM 节点入库并用**（同一个 idea 只走一条入库通道，见下）。
- **上游 / 下游**：上游 = 用户手里的 idea JSON（命名 `<dataset>_<region>_<delay>_idea_<ts>.json`，含 `template` / `idea` / `expression_list` 三键），或 `brain-make-some-gem` 落盘的同格式文件；下游 = S3 批量回测（`pipeline.py --from-db` / `workflow_batch_track` 读 `expressions` 表；执行入口选用见 `brain-sim-alphas-in-batch-and-track`）。

**运行环境**：所有 Python 命令用 MCP venv（`$WQ_PY`）。凭据由脚本自己读取——**agent 不读取 `.env`、不打印凭据、不把口令放命令行**（AGENTS.md）。

## 何时走本通道（两条入库通道互斥）

| 场景 | 入库通道 |
|---|---|
| 表达式由 `brain-make-some-gem` / `workflow_gem` 生成 | **GEM 节点已直接把表达式写进 `expressions` 表**（`status=gem`）→ **不要**再走本 skill，否则同一批表达式入库两次 |
| **外部 / 手写**的 idea JSON（论坛模板、用户给的表达式清单） | **本 skill**：`build_alpha_list.py` 写 `expressions` 表（`status=pending`） |
| 已在库里的 idea / 波，只想**按设置展开**（RA 步 6 的「设置展开」） | 本 skill 的 `build_alpha_list.py --from-db`（注意：这是**本脚本**的参数——从 DB 里的 idea 或该波表达式取式，按给定设置重写入同一波；不是 `pipeline.py` 的 `--from-db`） |

## 确定性流程

1. **入口** `scripts/process_template.py --file <idea.json>`：解析 idea → `idea_context.json`；取合法设置选项（缺 `sim_options_snapshot.json` 才联网）→ `settings_candidates.json`（该 region/delay 的合法 universe / 中性化等，**只用来核对**）。产物默认落在 skill 目录的 `processed_templates/<文件名>/`（已 gitignore、不参与 skill 同步），可用 `--out-dir` 指到别处。脚本到此结束。
2. **设置取值**：跟随战役 `tracking/<REGION>/config/settings.json`，或 profile 的 `settings_proven`（已验证设置跟 win 走）。A/B 实验与覆盖走 pipeline 的 `--neutralization` / `--set`，不在本环节做多组设置的人工决策循环。**中性化必须选一个有效选项（生产回测不能是 `None`）**；这条只约束**生产回测**——字段探测（`brain-datafield-exploration-general`）恰恰要求 `Neutralization: None`，两边各管各的场景。
3. **入库** `scripts/build_alpha_list.py`：以 JSON 字符串传设置（`region` / `delay` / `universe` / `neutralization` 必填，缺失抛 `KeyError`），**`--campaign-dir tracking/<REGION>`** 让没给的可选字段取战役 `settings.json`：

```powershell
& $WQ_PY scripts/build_alpha_list.py --idea idea_context.json --campaign-dir tracking/<REGION> `
    --settings_json '{"region":"<R>","delay":<D>,"universe":"<U>","neutralization":"<N>"}'
```

   `alpha_list.json` 只有显式传 `--out` 才会写（兼容导出，**不是交接文件**——交接以 `expressions` 表为准）。

## 可选字段的默认值（会悄悄改变回测口径，务必看打印）

`--settings_json` 里没给的可选字段，优先取 `--campaign-dir` 的 `config/settings.json`，再用脚本缺省；**每次运行都会打印每个字段的来源**（`settings_json` / `campaign settings.json` / `脚本缺省`）。脚本缺省：`decay=0`、`truncation=0.08`、`pasteurization=ON`、`testPeriod=P0Y0M0D`、`unitHandling=VERIFY`、`nanHandling=OFF`、`maxTrade=OFF`、`visualization=false`。

**战役并不统一**：各区 `settings.json` 里 `nanHandling` 有 ON 也有 OFF（7 OFF / 6 ON），`maxTrade` 同样（8 OFF / 5 ON）——所以**不要假定脚本缺省 = 战役口径**，不传 `--campaign-dir` 时用了脚本缺省就要在汇报里说明。`testPeriod`：「无测试期」统一写 `P0Y0M0D`；`P6Y` 是真实的 6 年测试期，不是无测试期。

## 手动步骤（调试）

```powershell
& $WQ_PY scripts/parse_idea_file.py --input <idea.json> --out idea_context.json
& $WQ_PY scripts/fetch_sim_options.py --out sim_options_snapshot.json          # 需要凭据（由脚本读取）
& $WQ_PY scripts/resolve_settings.py --idea idea_context.json --options sim_options_snapshot.json --out settings_candidates.json
& $WQ_PY scripts/build_alpha_list.py --idea idea_context.json --campaign-dir tracking/<REGION> --settings_json '<JSON>'
```

多组设置需要重复入库时，换设置组合重复执行 `build_alpha_list.py`（同一 `wave`、同一表达式在不同设置下是不同的 per-item override；同一波内表达式文本必须不同的约束见 toolkit SKILL §12）。

## 凭据（脚本读取，标准名优先）

`scripts/load_credentials.py` 的解析顺序：环境变量 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（标准，与 MCP 服务、toolkit、`batch_simulator.py` 同名；另认旧别名 `BRAIN_USERNAME` / `BRAIN_EMAIL` / `BRAIN_PASSWORD`）→ 本 skill 目录的 `config.json`（本地文件，见 `config.example.json`，已 `.gitignore`）→ `~/secrets/platform-brain.json`。仅获取模拟选项时需要凭据。切勿提交真实凭据。

## 常见错误

| 现象 | 含义 | 处理 |
|---|---|---|
| `Unsupported filename format` | 文件名不符合 `<dataset>_<REGION>_<0\|1>_idea_<ts>.json` | 改名，或用手动步骤并显式传 region / delay |
| `KeyError: 'universe'` 等 | `--settings_json` 缺必填四键 | 补齐 `region` / `delay` / `universe` / `neutralization` |
| `DB 无表达式: <region>/<wave>` | `--from-db` 取不到 idea 或该波表达式 | 先 GEM 入库，或改传 `--idea` |
| `找不到 wqb 工作区` | 脚本在仓库外运行 | 设 `WQB_WORKSPACE` 指向工作区根 |
| 校验失败的表达式出现在 `idea_context.json` 的 `validation_failures` | 语法 / 算子不合法 | 修表达式后重跑；不要绕过 |

## 情景卡

### 情景 IR-A　用户给了论坛上的一份 idea JSON，要放进 KOR 回测

- **前置状态**：文件名合规，KOR 战役目录存在。
- **步骤**：① `process_template.py --file …` 核对合法选项；② 设置取 `tracking/KOR/config/settings.json`；③ `build_alpha_list.py … --campaign-dir tracking/KOR --settings_json '{…}'`；④ 看打印的「可选字段来源」，`脚本缺省` 的要向用户说明；⑤ 交 S3。
- **完成定义**：`expressions` 表里该波有 `status=pending` 的行，且设置来源已汇报。
- **反例**：GEM 已入库的批次再来一遍；漏传 `--campaign-dir` 却声称「与战役口径一致」。

### 情景 IR-B　字段探测和生产回测对中性化要求相反

- **前置状态**：`brain-datafield-exploration-general` 要求 `Neutralization: None`，本 skill 要求「不能为 None」。
- **处置**：不矛盾——探测（看字段本身的信号）与生产回测（要可提交）是两个场景，各按各自 skill 的要求；不要把探测用的设置带进 `build_alpha_list.py`。
