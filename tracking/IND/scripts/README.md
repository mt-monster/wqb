# scripts/ — IND 挖掘脚本

> 2026-08-29 去重说明

**历史背景**：本目录原为 `tracking/KOR/scripts/` 的整目录克隆（112 个文件逐字节相同）。
2026-08-29 去重治理删除了全部 112 个克隆文件。共享工具脚本已由 `tools/` 下通用工具取代
（见 `tools/README.md`），区域差异通过 `--region IND` 参数传入。

**当前保留文件**（IND 独有，非 KOR 克隆）：

| 文件 | 用途 |
|------|------|
| `batch_validate_kor.py` | IND 批量语法校验（内容与 KOR 版有差异） |
| `run_wave27.py` | IND wave27 ASI analyst46 runner |
| `run_wave28.py` | IND wave28 ASI analyst46 runner |
| `run_wave30.py` | IND wave30 ASI analyst46 runner |

> 注意：`run_wave*.py` 文件名含 "ASI" 是历史遗留，实际运行区域为 IND。
> 如需 KOR 共享工具脚本，请使用 `tools/` 下通用工具或 `tracking/KOR/scripts/`。
