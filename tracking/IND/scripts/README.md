# scripts/ — IND 挖掘脚本

> 2026-08-18 治理说明

**镜像关系（重要）**：本目录活跃工具脚本与 `tracking/KOR/scripts/` 内容一致（历史整目录克隆，脚本通过 `os.path.dirname(__file__)` 定位本区域根目录，故同份代码两处部署各自生效）。**修改任一区域工具脚本时须同步另一区域，或未来迁移为 `tracking/shared/scripts/` 参数化版本。**

- `archive/`：历史 wave 记录脚本（`record_*` / `_tmp_*`），只读归档。
- 其余为活跃工具：`gate.py`（统一提交前闸门）、`kor_pipeline.py`、`kor_scan_fields*.py`、`filter_*.py`、`build_wave.py` 等。

注意：本目录脚本文件名沿用 KOR 时期命名（如 `kor_pipeline.py`），指向的是所在区域（IND）的数据，并非 KOR。
