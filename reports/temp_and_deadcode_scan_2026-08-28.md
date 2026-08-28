# 临时文件与无用代码扫描报告

> 扫描时间：2026-08-28 18:40
> 扫描范围：仓库全量（排除 `attic/` 归档区、`.git`、`.venv`、`data/`、`research-data/`）
> 扫描工具：`tracking/_scratch/_scan_deadcode.py`（v1）、`_scan_deadcode_v2.py`（v2，排除装饰器误报）
> 原始报告：`tracking/_scratch/_deadcode_report_v2.json`
> **状态：仅扫描分析，未做任何修改/删除。待用户确认后执行。**

---

## 一、扫描结果总览

| 类别 | 数量 | 影响面 | 建议 |
|---|---|---|---|
| **BOM 损坏脚本**（语法错误） | **24** | 🔴 高 — 无法被 Python 解析 | 修复或删除 |
| 未使用 import | 531 | 🟡 中 — 代码臃肿，无功能影响 | 建议清理 |
| 真·死代码（跨文件校验零引用） | 4 | 🟢 低 | 可安全删除 |
| `_scratch` 一次性脚本 | 97（464K） | 🟢 低 — 已 gitignored | 可清理 |
| 已追踪备份文件 `.bak_*` | 3 | 🟢 低 | 可清理 |
| 运行时临时目录 | ~237M | 🟢 低 — 已 gitignored | 可选清理 |

---

## 二、🔴 P0：24 个 BOM 损坏脚本（无法解析）

### 问题描述

这些文件第 2 行开头存在 **U+FEFF（BOM）字符**，导致 Python 无法解析：

```
00000000: 696d 706f 7274 206f 730d 0aef bbbf 2321  import os..... #!
                                    ^^^^^^^^
                                    BOM 卡在第 2 行开头
```

根因：文件首行 `import os` 被插入到了 shebang `#!/usr/bin/env python3` **之前**，
而 BOM 原本属于 shebang 行开头，拼接后卡在第 2 行中间位置。

### 验证结果

```
$ python -c "import ast; ast.parse(open('tracking/EUR/scripts/run_wave19_aea.py',encoding='utf-8').read())"
SyntaxError: invalid non-printable character U+FEFF
```

**这些脚本一旦执行就会立即抛 SyntaxError。** 且 `git grep` 显示它们**未被任何其他文件引用**（独立执行脚本）。

### 完整清单（24 个）

| 目录 | 文件 | 数量 |
|---|---|---|
| `tracking/EUR/scripts/` | `run_wave19_aea.py`, `run_wave21_starmine.py`, `run_wave22_arh.py`, `run_wave23_ac.py`, `run_wave24_ipv.py`, `run_wave25_fhp.py`, `run_wave26_m238.py`, `run_wave27_acq.py`, `run_wave28_inst6.py`, `run_wave29_m354.py`, `run_wave30_news54.py`, `run_wave4_uni_probe.py`, `run_wave5_pspat_probe.py`, `run_wave6_fcfmix_probe.py`, `run_wave6b_fcfmix_probe.py` | 15 |
| `tracking/HKG/scripts/` | `run_wave2_nsnlp_ts.py` | 1 |
| `tracking/IND/scripts/archive/` | `_tmp_w22gh.py`, `_tmp_w22i.py`, `_tmp_w22j.py`, `_tmp_w22kl.py` | 4 |
| `tracking/KOR/scripts/archive/` | `_tmp_w22gh.py`, `_tmp_w22i.py`, `_tmp_w22j.py`, `_tmp_w22kl.py` | 4 |

### 处置选项

- **A. 修复**（推荐）：剥离第 2 行的 BOM 字符 → 脚本可正常执行
- **B. 删除**：这些波次若已完成且产物已归档，可直接删除
- **C. 归档**：`git mv` 到 `attic/`（符合项目"不硬删"纪律）

> ⚠️ 注意：8 个 `archive/_tmp_w22*.py` 位于 archive 目录且以 `_tmp_` 命名，
> 明显是临时文件，**建议直接删除**；其余 16 个是真实波次脚本，**建议修复**。

---

## 三、🟡 P1：531 个未使用 import

### 分布

| 目录 | 未用 import | 文件数 |
|---|---|---|
| `world-quant-brain-mcp/` | **454** | 22 |
| `src/` | 19 | 11 |
| `tracking/KOR/` | 19 | 9 |
| `mining/` | 12 | 10 |
| `tools/` | 8 | 8 |
| `tests/` | 6 | 3 |
| 其他（tracking/reference, EUR, GBR, USA, IND, polling） | 13 | 12 |

### 根因：模板化复制

`world-quant-brain-mcp/` 占 85%（454/531）。对比两个文件的 import 块，**几乎逐字相同**：

```python
# tools_submit.py 与 tools_config.py 的 import 块（完全一致）
import json, os, re, asyncio, time, logging
from typing import Dict, List, Optional, Any, Union, Sequence, Tuple
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path

from mcp_core import (mcp, brain_client, logger, save_config, _slim_checks, _slim_alpha,
    _slim_alpha_response, _slim_alpha_list, _slim_multisim, _slim_datafields, _slim_datasets,
    _records_to_dicts, _slim_yearly, _slim_pnl, _slim_correlation_block, _slim_check_correlation,
    _slim_pyramids, _slim_text_lookup, _ra_bad, _truncate, _unwrap_result, _rewrap, _is_error)
```

**成因**：2026-08-13 从 `main.py` 按域拆分为 `tools_*.py` 时，每个文件都复制了
完整 import 清单，但各文件实际只用到其中一部分。

### 高频未用 import（模板化证据）

| 名字 | 出现在 N 个文件的未用列表 |
|---|---|
| `json` | 26 |
| `sys` | 17 |
| `Union` | 16 |
| `timedelta` | 16 |
| `datetime` | 15 |
| `sleep` | 15 |
| `Path` | 13 |
| `_slim_checks`, `_slim_alpha`, `_records_to_dicts`, `_ra_bad`, `_truncate` 等 | 各 10 |

### 处置建议

纯删除未使用的 import 行，**零功能风险**（不影响运行时行为）。
但涉及 75 个文件，建议：
- 用自动化工具（如 `autoflake`）批量处理
- 处理后必须跑 `pytest` 回归验证

---

## 四、🟢 P2：4 个真·死代码（已跨文件校验）

对初筛的 347 个"死定义"做了两轮过滤：
1. 排除装饰器注册（`@mcp.tool()` 等）→ 剩 347
2. 排除 pytest 测试函数（`test_*`）→ 剩 57
3. **跨文件 `git grep -w` 校验** → 剩 **4**

> 53 个初筛项实为**公共 API**（如 `src/wqb/config.py` 的 `neutralization_search_order`
> 被 4 个文件引用、`parse_expression` 被 `validator.py` 引用），**不是死代码**。

### 真正零引用的 4 个

| 文件 | 行号 | 定义 | 说明 |
|---|---|---|---|
| `src/wqb/workflow/mcp_check.py` | 156 | `get_mcp_tool_for_task` | 工作流 MCP 检查，未接入 |
| `src/wqb/workflow/mcp_check.py` | 168 | `format_mcp_reminder` | 同上 |
| `tools/wave_results_writer.py` | 87 | `read_wave_result` | 只写不读的对称性残留 |
| `world-quant-brain-mcp/scripts/python_alpha_policy.py` | 11 | `load_policy` | 策略加载，未被调用 |

> ⚠️ 保守提示：`mcp_check.py` 的 2 个函数可能是**预留接口**（供未来或外部 agent 调用），
> 建议删除前确认其设计意图。

---

## 五、🟢 P3：临时文件与运行时目录

### 5.1 `tracking/_scratch/`（97 个文件，464K）

已 gitignored，**不进版本库**。全部为 2026-08 的一次性脚本：
- 95 个 `.py` + 6 个 `.json`（部分文件无扩展名）
- 典型：`_db_fix_p0.py`、`_db_fix_items_345.py`（DB 修复脚本，已执行完毕）
- `_query_*.py`、`_analyze_*.py`（一次性查询）
- `_gen_w8~w11.py`、`_show_*.py`（早期波次生成/查看脚本）

> 这些是**可恢复暂存区**（项目纪律：临时脚本移入此处而非硬删）。
> 清理不影响版本库，但会丢失执行记录。

### 5.2 3 个已追踪备份文件（已进 git）

| 文件 | 大小 | 日期 |
|---|---|---|
| `tracking/KOR/reference/kor_generation_constraints.json.bak_20260815` | 2.5K | 08-16 |
| `tracking/USA/config/thresholds.json.bak_precal_20260827` | 3.8K | 08-27 |
| `tracking/USA/priors/usa_priors.json.bak_20260826` | 2.0K | 08-26 |

均已随 git 历史永久保存，**删除不影响可恢复性**。

### 5.3 运行时目录（已 gitignored，共 ~237M）

| 目录 | 占用 | 说明 |
|---|---|---|
| `data/` | 143M | SQLite 数据库 + **多份 .bak 备份** |
| `research-data/` | 84M | WebDataScope 抓取数据 |
| `logs/` | 7.9M | 运行日志 |
| `.pytest_tmp/` | 2.2M | pytest 运行时产物 |
| `tracking/_scratch/` | 464K | 一次性脚本 |
| `.pytest_cache/` | 39K | pytest 缓存 |

> `data/` 含本次及历次 DB 修复的备份（`wqb.db.bak.*`），如需释放空间可清理旧备份。

---

## 六、建议的清理优先级

| 优先级 | 项目 | 动作 | 风险 |
|---|---|---|---|
| **P0** | 24 个 BOM 损坏脚本 | 修复 16 个波次脚本 / 删除 8 个 `_tmp_` | 低（当前本就无法运行） |
| **P1** | 531 个未使用 import | `autoflake` 批量删除 + pytest 回归 | 低（零功能影响） |
| **P2** | 4 个真死代码 | 删除（建议先确认 mcp_check 2 个是否为预留） | 低 |
| **P3** | `_scratch` 97 文件 | 清理（可恢复暂存区） | 极低（不进 git） |
| **P3** | 3 个 `.bak_*` | 删除（git 历史可恢复） | 极低 |
| **P3** | 运行时目录 | 清理旧 DB 备份 / 日志 | 低 |

---

## 七、未纳入清理的建议保留项

- **`attic/` 归档区**（266 个文件）：项目"不硬删"纪律的归档区，**不建议清理**
- **`src/wqb/config.py` 等公共 API**：初筛误报，实际被多文件引用
- **`world-quant-brain-mcp/` 的 mixin 类**：被 `brain_api.py` 组合使用，非死代码

---

*报告生成：只读扫描，未修改任何文件。等待用户确认清理范围后执行。*
