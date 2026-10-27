# -*- coding: utf-8 -*-
"""区域 skill 脚手架的落点与幂等守护（2026-10-20）。

背景（真 bug，已修）：`tools/skills/gen_region_skill_scaffold.py` 用
`Path(__file__).resolve().parents[1]` 推导仓库根，而本文件在 `tools/skills/` 下
⇒ 算成 `tools/` ⇒ `--apply` 把 `config/README.md` 等写进
`tools/Claude/skills/wq-brain-ra-<区>/...`（错误落点，且不报错）。

AGENTS.md §8.13 明写「仓库根推导一律层数无关」，故本文件守护三件事：
1. 脚手架解析出的 SKILLS 必须在**仓库根**下（不是 tools/ 下）；
2. `--apply` 后目标区域确实拿到 `config/` 四目录产物；
3. 脚手架「只增不删」：已存在的文件不覆盖（幂等）。
"""
import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOL = REPO_ROOT / "tools" / "skills" / "gen_region_skill_scaffold.py"


def _load_tool():
    """按文件路径加载工具模块（它不在包内，不能直接 import）。"""
    spec = importlib.util.spec_from_file_location("_scaffold_under_test", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_repo_root_resolution_is_depth_independent():
    """仓库根必须靠标记探测，不是层数硬编码。

    变异反查：把 `REPO` 改回 `parents[1]`，本用例必须立刻失败
    （那会让落点变成 `tools/Claude/skills/...`）。
    """
    mod = _load_tool()
    assert mod.REPO == REPO_ROOT, (
        f"脚手架解析的仓库根是 {mod.REPO}，应为 {REPO_ROOT}；"
        "多半是层数硬编码（parents[N]）失效"
    )
    assert mod.SKILLS == REPO_ROOT / "Claude" / "skills"


def test_no_phantom_tree_under_tools():
    """`tools/` 下不得出现 `Claude/skills/` 假树（错误落点的产物）。"""
    assert not (REPO_ROOT / "tools" / "Claude").exists(), (
        "tools/Claude/ 是脚手架根推导错误时留下的假树，应删除；"
        "重建请用 --apply 打到仓库根"
    )


def test_apply_creates_config_dir_in_repo_and_is_idempotent(tmp_path, monkeypatch):
    """`--apply` 把产物写到仓库根的目标区域，且重复执行不覆盖既有内容。

    ⚠ 用 `tmp_path` 当 skill 根：脚手架的 `SKILLS` 是模块级常量，
    若在「根推导失效」的变异态下跑本用例，会往 `tools/Claude/skills/` 真目录
    写垃圾（2026-10-20 实测踩过）。monkeypatch 把 SKILLS 钉到 tmp 目录，
    让本用例只验「写盘 + 幂等」两件事，不依赖仓库根推导。
    """
    mod = _load_tool()
    monkeypatch.setattr(mod, "SKILLS", tmp_path / "skills")
    tmp_skill = tmp_path / "skills" / "wq-brain-ra-zztest"
    tmp_skill.mkdir(parents=True, exist_ok=True)
    (tmp_skill / "SKILL.md").write_text(
        "---\nname: wq-brain-ra-zztest\n---\n\n## 区域控制面板\n", encoding="utf-8"
    )
    assert mod.put(tmp_skill / "config" / "README.md", "body", True) == "OK"
    assert (tmp_skill / "config" / "README.md").exists()
    # 幂等：已存在不覆盖
    assert mod.put(tmp_skill / "config" / "README.md", "other", True) == "SKIP"
    assert (tmp_skill / "config" / "README.md").read_text(encoding="utf-8") == "body"
    # PLAN 模式不写盘
    assert mod.put(tmp_skill / "config" / "other.md", "x", False) == "PLAN"
    assert not (tmp_skill / "config" / "other.md").exists()


def test_every_region_skill_has_config_dir():
    """13 个区 skill 的 `config/` 必须齐整（2026-10-20 EUR 误删事件的守护）。"""
    mod = _load_tool()
    missing = []
    for r in mod.regions():
        d = mod.SKILLS / f"wq-brain-ra-{r.lower()}"
        if not (d / "config" / "README.md").exists():
            missing.append(r)
    assert not missing, (
        f"这些区域 skill 缺 config/README.md：{missing}；"
        "用 `python tools/skills/gen_region_skill_scaffold.py --region <R> --apply` 补齐"
    )


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
