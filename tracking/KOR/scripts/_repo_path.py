# -*- coding: utf-8 -*-
"""_repo_path.py —— 层数无关的仓库根解析（AGENTS.md §8.13）。

为什么需要它
------------
本目录（`tracking/KOR/scripts/`）历史上并存**五种**仓库根写法，其中三个文件是错的
（2026-10-15 实测；本目录从 `tracking/KOR/` 看是三层深，仓库根在 `parents[3]`）：

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))   # kor_ledger_write.py:11
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))   # kor_spre_read.py:6
    REPO = Path(__file__).resolve().parents[1]                             # _kor_s6_writeback.py:15

前两条解析成 `tracking/KOR/src`、第三条解析成 `tracking/KOR`，都少两层。**这类错不报错**：
往 `sys.path` 塞一个不存在的路径是静默 no-op，`import wqb` 靠 pip 的 editable 安装救回来
就一切如常，换台机器或换个 cwd 才 ImportError。这正是 AGENTS.md §8.13 说的
「文件一旦移动一层就静默指错目录」。

正确写法本目录已有先例：`kor_opportunity_scan.py:32-35`（向上探测双标记）。

约定
----
- 判据 = 同时存在 `pyproject.toml` 与 `src/wqb/`（与 `wqb.paths._ROOT_MARKERS` 同口径）。
- 优先用已安装的 `wqb.paths`（仓库 venv 是 `pip install -e .`，正常工作路径）；
  仅当 `wqb` 不可导入时才回落到本地向上探测 —— 回落存在的理由是「脚本被从仓库外
  的裸解释器直接跑」，而不是「省掉一次 import」。
- **不要**在本目录新脚本里再写 `parents[N]` / `dirname(dirname(...))`。

用法::

    from _repo_path import REPO          # pathlib.Path，仓库根
    FAMILIES = REPO / "Claude" / "skills" / ...
"""
from __future__ import annotations

from pathlib import Path

_ROOT_MARKERS = ("pyproject.toml", "src/wqb")


def _probe(start: Path) -> Path:
    """向上探测仓库根；探不到显式报错，不猜。"""
    base = start if start.is_dir() else start.parent
    for parent in (base, *base.parents):
        if parent.is_dir() and all((parent / m).exists() for m in _ROOT_MARKERS):
            return parent
    raise RuntimeError(
        f"仓库根未找到（从 {base} 向上未出现 {list(_ROOT_MARKERS)}）；"
        f"可用 WQB_ROOT 显式指定，或在本仓 venv 里运行"
    )


def repo_root(start: str | Path | None = None) -> Path:
    """仓库根。`start` 缺省用本模块位置（同目录脚本写 `repo_root(__file__)` 亦可）。"""
    try:
        from wqb.paths import find_repo_root  # 权威实现（含 WQB_ROOT 覆盖）
    except ImportError:
        return _probe(Path(start or __file__).resolve())
    return find_repo_root(start)


#: 本目录脚本的默认根（模块导入即解析一次，省得每个脚本各算一遍）
REPO: Path = repo_root(__file__)
