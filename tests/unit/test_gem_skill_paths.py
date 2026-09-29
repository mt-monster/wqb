# -*- coding: utf-8 -*-
"""GEM 引擎的 skill 目录解析与内嵌副本不变量（2026-09-26 审计固化）。

## 缘起

`brain-make-some-gem` 内置了一份 GEM 引擎（`scripts/trailSomeAlphas/`），其 `pipeline_paths.py`
过去把两个 skill 目录**写死成内嵌位**：

    FEATURE_ENGINEERING_DIR   = SKILLS_DIR / "brain-data-feature-engineering"
    FEATURE_IMPLEMENTATION_DIR = SKILLS_DIR / "brain-feature-implementation"

后果（2026-09-26 实测）：

1. `brain-feature-implementation/SKILL.md` 的内嵌副本停在 **2026-08-22 的 49 行旧英文稿**
   （还引用不存在的 `manage_todo_list`），一旦有人在兜底位读到它就会照旧稿操作；
2. `brain-data-feature-engineering` 的内嵌目录**连 SKILL.md 都没有**，而
   `read_text_optional()` 失败**返回空串**，且完全静默；
3. `*_ideas.md` 产物写进 skill 树内部，污染仓库。

现已统一为 `env > skill_roots 候选 > 内嵌 legacy 兜底`，并把产物根迁到 `GEM_REPORT_ROOT`。
本模块守住这些不变量，防止回退。

2026-09-29 更正（skills 审查 FE-13 / GM-13）：**SKILL.md 正文从不进 LLM prompt**——`build_prompt` 只用
dfe `SKILL.md`「是否非空」决定附不附一句固定的 8 问提示，FI 那份完全不用（`test_se_docs.py` 的 AST 测试钉死）。
上面「拼进 prompt」的说法是历史误解；这些守护仍然有意义，但理由是「不让同名文件互相矛盾、解析异常可见」，
不是「文档篇幅直接影响生成质量」。dfe 三个内嵌副本文件（`reference.md` / `examples.md` / `OUTPUT_TEMPLATE.md`）
自此也纳入逐字节守护。
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "Claude" / "skills"
GEM_SKILL = SKILLS_DIR / "brain-make-some-gem"
TRAIL_DIR = GEM_SKILL / "scripts" / "trailSomeAlphas"
AUTHORITATIVE_FI = SKILLS_DIR / "brain-feature-implementation" / "SKILL.md"
EMBEDDED_FI = TRAIL_DIR / "skills" / "brain-feature-implementation" / "SKILL.md"
EMBEDDED_DFE = TRAIL_DIR / "skills" / "brain-data-feature-engineering"
def _find_mcp_venv() -> Path:
    """Windows（Scripts/python.exe）与 POSIX（bin/python）两种 venv 布局都认；都没有时返回前者，让 skip 信息有意义。"""
    venv = REPO_ROOT / "world-quant-brain-mcp" / ".venv"
    for rel in (("Scripts", "python.exe"), ("bin", "python")):
        cand = venv.joinpath(*rel)
        if cand.is_file():
            return cand
    return venv / "Scripts" / "python.exe"


#: 用于实跑解析子进程的 MCP venv 解释器（与 `src/wqb/workflow/_common.py` 找 venv 的口径一致）
_MCP_VENV = _find_mcp_venv()


def _norm(path: Path) -> bytes:
    """归一换行：仓库 LF / 安装位 CRLF 的历史差异不算漂移。"""
    return path.read_bytes().replace(b"\r\n", b"\n")


def test_embedded_fi_copy_matches_authoritative():
    """内嵌 FI 的 SKILL.md 必须与顶层权威版**逐字一致**。

    理由不是「会被拼进 prompt」（不会，见模块 docstring 的更正），而是同名不同文会让人在兜底位读到过时规范：
    2026-09-26 前它是 49 行旧稿（还引用不存在的 `manage_todo_list`），与权威版相差 31 行独有内容。
    """
    assert AUTHORITATIVE_FI.is_file(), f"权威版缺失：{AUTHORITATIVE_FI}"
    assert EMBEDDED_FI.is_file(), f"内嵌副本缺失：{EMBEDDED_FI}"
    a, b = _norm(AUTHORITATIVE_FI), _norm(EMBEDDED_FI)
    assert a == b, (
        "GEM 内嵌的 brain-feature-implementation/SKILL.md 与顶层权威版漂移（不进 prompt，但同名不同文会让人在兜底位读到旧规范）。"
        " 修复：python tools/sync_gem_embedded_skill.py --apply"
    )


def test_embedded_dfe_copies_match_authoritative():
    """dfe 内嵌目录里的三个文件必须与顶层逐字节一致（此前只守 FI 的 SKILL.md，`reference.md` 已悄悄漂移到 399 行旧稿）。"""
    if not EMBEDDED_DFE.is_dir():
        pytest.skip("内嵌 dfe 目录不存在，无需守护")
    top = SKILLS_DIR / "brain-data-feature-engineering"
    for name in ("reference.md", "examples.md", "OUTPUT_TEMPLATE.md"):
        assert (top / name).is_file(), f"权威版缺失：{top / name}"
        assert (EMBEDDED_DFE / name).is_file(), f"内嵌副本缺失：{EMBEDDED_DFE / name}"
        assert _norm(top / name) == _norm(EMBEDDED_DFE / name), (
            f"内嵌 dfe/{name} 与顶层漂移。修复：python tools/sync_gem_embedded_skill.py --apply")


def test_embedded_dfe_dir_is_marked_generated_and_the_sync_tool_covers_it():
    if not EMBEDDED_DFE.is_dir():
        pytest.skip("内嵌 dfe 目录不存在，无需守护")
    marker = EMBEDDED_DFE / "GENERATED.md"
    assert marker.is_file(), "内嵌 dfe 目录应带 GENERATED.md 标记（勿手改的派生副本）"
    text = marker.read_text(encoding="utf-8")
    assert "sync_gem_embedded_skill.py" in text and "SKILL.md" in text
    sync = (REPO_ROOT / "tools" / "sync_gem_embedded_skill.py").read_text(encoding="utf-8")
    for name in ("reference.md", "examples.md", "OUTPUT_TEMPLATE.md"):
        assert name in sync


def test_embedded_dfe_has_no_skill_md():
    """内嵌 dfe 目录**不得**放 SKILL.md —— 解析探针正是用它把该目录排除掉。

    若在此处补一份 SKILL.md，`_resolve_skill_dir` 会改选内嵌目录，
    顶层 322 行文档将再次被静默屏蔽（这正是本模块要防的回退）。
    """
    if not EMBEDDED_DFE.is_dir():
        pytest.skip("内嵌 dfe 目录不存在，无需守护")
    assert not (EMBEDDED_DFE / "SKILL.md").is_file(), (
        "内嵌 brain-data-feature-engineering 出现了 SKILL.md —— 会让解析改选内嵌位、"
        "静默屏蔽顶层权威文档。请删除它（产物/模板可留，SKILL.md 不可留）。"
    )


def test_embedded_scripts_are_present_and_validator_is_byte_identical():
    """INDEX「嵌套副本」纪律 #1（skills 审查 IX-15）：内嵌 `scripts/` 是硬依赖，不能缺；`validator.py` 与权威版逐字节相同。"""
    scripts = TRAIL_DIR / "skills" / "brain-feature-implementation" / "scripts"
    for name in ("ace_lib.py", "helpful_functions.py", "validator.py", "implement_idea.py", "fetch_dataset.py"):
        assert (scripts / name).is_file(), f"内嵌 scripts/ 缺 {name}（硬依赖，不得删除）"
    authoritative = SKILLS_DIR / "alpha-expression-verifier" / "scripts" / "validator.py"
    assert _norm(scripts / "validator.py") == _norm(authoritative), (
        "内嵌 validator.py 与 alpha-expression-verifier 权威版漂移——四处（权威 + toolkit 侧 + FI + 内嵌 FI）一起覆盖")


def test_gem_report_root_is_outside_skill_tree():
    """产物根必须在 skill 树之外（防 `*_ideas.md` 再次污染仓库/安装位）。"""
    src = (TRAIL_DIR / "pipeline_paths.py").read_text(encoding="utf-8")
    assert "GEM_REPORT_ROOT" in src, "pipeline_paths.py 应定义 GEM_REPORT_ROOT"
    assert "GEM_REPORT_ROOT = GEM_DATA_ROOT" in src, (
        "GEM_REPORT_ROOT 应派生自 GEM_DATA_ROOT（与 data/ 同源迁出 skill 树）"
    )
    reports = (TRAIL_DIR / "pipeline_reports.py").read_text(encoding="utf-8")
    assert "output_dir = GEM_REPORT_ROOT" in reports, (
        "save_ideas_report 应写 GEM_REPORT_ROOT，而不是 FEATURE_ENGINEERING_DIR/output_report"
    )


def _run_resolution() -> dict:
    """在子进程里用真实解析逻辑跑一次（避免污染本进程 sys.path）。"""
    if not _MCP_VENV.is_file():
        pytest.skip(f"MCP venv 不存在，跳过实跑解析：{_MCP_VENV}")
    code = (
        "import json, sys; sys.path.insert(0, r'%s');"
        "import pipeline_paths as pp;"
        "print(json.dumps({"
        "'fi_dir': str(pp.FEATURE_IMPLEMENTATION_DIR),"
        "'fi_source': pp.SKILL_DIR_SOURCES['feature_implementation'][1],"
        "'dfe_dir': str(pp.FEATURE_ENGINEERING_DIR),"
        "'dfe_source': pp.SKILL_DIR_SOURCES['feature_engineering'][1],"
        "'missing': pp.missing_skill_docs(),"
        "'report_root': str(pp.GEM_REPORT_ROOT),"
        "}, ensure_ascii=False))" % str(TRAIL_DIR)
    )
    env = dict(os.environ)
    env.pop("WQB_FI_SKILL_DIR", None)
    env.pop("WQB_DFE_SKILL_DIR", None)
    # cwd 用临时目录：vendored ace_lib 一 import 就在 CWD 建 `ace.log`，放在 skill 树里会污染源位并被 sync_skills 带到安装位
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run([str(_MCP_VENV), "-c", code], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", cwd=td, env=env, timeout=120)
    assert r.returncode == 0, f"解析子进程失败：\n{r.stdout}\n{r.stderr}"
    return json.loads(r.stdout.strip().splitlines()[-1])


def test_resolution_finds_docs_and_avoids_embedded_legacy():
    """两个 skill 目录都必须解析到**带 SKILL.md 的权威副本**，且不能落到内嵌 legacy。

    这是本节的核心回归：旧实现下 dfe 恒落内嵌（无 SKILL.md）→ 文档静默为空串进 prompt。
    """
    res = _run_resolution()
    assert res["missing"] == [], f"有 skill 文档缺失（skill 目录解析异常，FI 目录同时承载 scripts/）：{res['missing']}"
    for key in ("fi_dir", "dfe_dir"):
        d = Path(res[key])
        assert (d / "SKILL.md").is_file(), f"{key}={d} 下没有 SKILL.md"
    for key in ("fi_source", "dfe_source"):
        assert res[key] != "embedded:legacy", (
            f"{key} 落到内嵌 legacy 兜底（{res[key]}）—— 权威副本未被选中，"
            "会读到过时/缺失的文档与脚本"
        )
    assert not str(res["report_root"]).startswith(str(GEM_SKILL)), (
        f"report_root 落在 skill 树内：{res['report_root']}"
    )


def test_moonshot_402_is_non_retryable():
    """LLM 通道的 401/402/403 必须**不可重试**且带绕行指引。

    实测（2026-09-26）：402 Insufficient Balance 走通用 `except Exception` 重试 3 次后，
    被外层「no meta.json within 90s」吞掉——真因完全不可见，排障极难。
    """
    src = (GEM_SKILL / "scripts" / "headless_runner" / "run.py").read_text(encoding="utf-8")
    assert "class _MoonshotNonRetryable" in src, "缺不可重试异常类"
    assert "raise _MoonshotNonRetryable" in src, "未在 401/402/403 分支抛不可重试异常"
    # 只在 `_patched_call_moonshot` 函数体内检查顺序（全文件有多处 except Exception）
    i_fn = src.find("def _patched_call_moonshot")
    i_end = src.find("rp.call_moonshot =", i_fn)
    body = src[i_fn:i_end]
    i_nr = body.find("except _MoonshotNonRetryable:")
    i_all = body.find("except Exception as exc:")
    assert 0 < i_nr < i_all, (
        "moonshot 重试循环里，不可重试分支必须排在通用 except **之前**（否则永远轮不到）\n"
        f"  except _MoonshotNonRetryable 相对位置={i_nr}, except Exception 相对位置={i_all}")
    i_raise = body.find("raise _MoonshotNonRetryable")
    assert "--ideas-file" in body[i_raise:i_raise + 900], (
        "不可重试错误信息必须给出 --ideas-file 绕行指引")
