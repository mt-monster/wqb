# -*- coding: utf-8 -*-
"""pack_reader.py — WebDataScope 数据包的统一打开入口。

背景（2026-09-25 P4）：仓库里四个体检/字段画像工具的默认包路径都指向
`research-data/WebData_20260219_V0.10.9.zip`，但磁盘上**只有解压后的目录**
`research-data/WebData_20260219_V0.10.9/`（163 个文件），且各工具只写
`zipfile.ZipFile(zip_path)`，无目录兜底 → 默认路径**必然打不开**。
这是 `.workbuddy/memory` 里反复出现「体检包本地不可达」的真正根因。

统一契约：
    with open_pack(path) as pack:
        raw = pack.read("data/oth/info_data.bin")

- `path` 是 **目录** → 走 DirArchive（按包内相对路径读文件）；
- `path` 是 **zip 文件** → 走 zipfile.ZipFile（原语义完全不变）；
- `path` 不存在 → 由 zipfile 抛 FileNotFoundError，**fail-closed 语义保持不变**
  （`tests/unit/test_inspect_mode_failclosed_p1p1.py` 依赖这条）。

只读套装即可，不实现写入/追加。
"""
from __future__ import annotations

import os
import zipfile


class DirArchive:
    """把已解压的数据包目录伪装成 ZipFile 的只读子集。

    只实现这些工具真正用到的接口：`read()`、`namelist()`、上下文管理器。
    路径一律是包内相对路径（如 `data/oth/info_data.bin`），与 ZipFile 成员名一致。
    """

    def __init__(self, root: str):
        self.root = os.path.abspath(root)

    # ---- 上下文管理器 -------------------------------------------------------
    def __enter__(self) -> "DirArchive":
        return self

    def __exit__(self, *exc) -> bool:
        return False

    def close(self) -> None:
        pass

    # ---- ZipFile 子集 -------------------------------------------------------
    def read(self, name: str) -> bytes:
        full = os.path.join(self.root, name)
        if not os.path.isfile(full):
            # 与 ZipFile 一致：缺成员抛 KeyError，便于上层按缺失处理
            raise KeyError(f"There is no item named {name!r} in the directory pack {self.root}")
        with open(full, "rb") as fh:
            return fh.read()

    def namelist(self) -> list:
        out = []
        base_len = len(self.root) + 1
        for dp, _dns, fns in os.walk(self.root):
            for fn in fns:
                full = os.path.join(dp, fn)
                out.append(full[base_len:].replace("\\", "/"))
        return sorted(out)

    def __contains__(self, name: str) -> bool:
        return os.path.isfile(os.path.join(self.root, name))

    def __repr__(self) -> str:  # pragma: no cover
        return f"<DirArchive {self.root}>"


def open_pack(path: str):
    """打开数据包，自动识别「zip 文件」与「已解压目录」。

    不存在/非法路径 → 抛错（不静默降级），保证"缺包"仍能被上层 fail-closed 判据捕获。
    """
    if os.path.isdir(str(path)):
        return DirArchive(path)
    return zipfile.ZipFile(path)
