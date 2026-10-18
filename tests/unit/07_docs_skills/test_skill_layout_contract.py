# -*- coding: utf-8 -*-
"""skill 目录布局契约的机械守护（2026-10-18 新增）。

## 缘起

2026-10-18 的 skills 目录层级审查（`reports/skills_hierarchy_audit_20261018.md`）
清点出 7 类问题，其中两类**必须用测试固化**，否则必然回退：

1. **`reference.md` 与 `references/` 并存**：历史上 skill 从「单文件」演进到「目录」时，
   有 3 个 skill 中途留下了两份参考入口，读到哪份取决于检索实现 ⇒ **检索权威歧义**。
   已一次性合并为 `references/overview.md`，本模块锁死该形态。

2. **`config/` 与 `configs/` 的语义边界**（此处**不是**命名不一致）：
   - `config/` = 静态配置资产（可提交、可批量处理），使用者 `wq-brain-campaign-toolkit`；
   - `configs/config.json` = **凭据契约路径**，被两条测试 + `load_credentials.py`
     的明文凭据迁移检测锁定（见 `test_judge_never_submits.py` /
     `test_sf_docs.py`），**改名会破坏凭据安全断言**。
   ⇒ 表面像分裂，实则语义不同。本模块把这条边界写成断言，防止后人"统一"它。

同时守护两条「未来禁止」项（当前仓库合规，设为前置红线）：
- skill **根目录不得出现** `.py` 可执行代码（一律下沉 `scripts/`）；
- skill 内 **不得出现** `data/` 运行期产物目录（安装到 6 处会复制垃圾）。

详见 `reports/skills_hierarchy_audit_20261018.md`。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "Claude" / "skills"

# 凭据契约路径：唯一允许的「复数」目录名，且用途已锁定为明文凭据迁移检测。
CREDENTIAL_CONTRACT = "configs/config.json"


def _skill_dirs() -> list[Path]:
    return sorted(p for p in SKILLS.iterdir() if p.is_dir())


def test_no_skill_has_both_reference_file_and_references_dir():
    """reference.md 与 references/ 不得并存（检索权威歧义）。"""
    offenders = [
        p.name for p in _skill_dirs()
        if (p / "reference.md").is_file() and (p / "references").is_dir()
    ]
    assert not offenders, (
        "这些 skill 同时存在 reference.md 与 references/，参考入口有二、检索会歧义："
        f"{offenders}。把 reference.md 移入 references/overview.md 并更新 SKILL.md 引用。"
    )


def test_reference_md_only_allowed_without_references_dir():
    """reference.md 只允许出现在「没有 references/ 目录」的 skill 上（单文件形态）。"""
    offenders = [
        p.name for p in _skill_dirs()
        if (p / "reference.md").is_file() and (p / "references").is_dir()
    ]
    # 与上一条同源，保留独立断言便于失败时定位到不同意图
    assert not offenders, f"见 test_no_skill_has_both_reference_file_and_references_dir：{offenders}"


def test_configs_directory_is_only_the_credential_contract():
    """`configs/` 只能是凭据契约路径，禁止被当普通配置目录扩散。"""
    allowed = {"brain-alpha-judge", "brain-forum-browse", "brain-sim-alphas-in-batch-and-track"}
    offenders = [p.name for p in _skill_dirs() if (p / "configs").is_dir() and p.name not in allowed]
    assert not offenders, (
        f"`configs/` 语义已锁定为凭据契约路径（{CREDENTIAL_CONTRACT}），"
        f"只有 {sorted(allowed)} 可用。新增 skill 若只是普通配置，请用 `config/`（单数）：{offenders}"
    )


def test_credential_contract_path_is_not_renamed():
    """凭据契约路径本身不得消失（改名会破坏两条凭据安全测试）。"""
    holders = [p.name for p in _skill_dirs() if (p / "configs").is_dir()]
    assert holders, (
        "没有任何 skill 保留 `configs/` 目录。若曾整体改名为 `config/`，"
        f"必须恢复 `{CREDENTIAL_CONTRACT}`：该字面量被 test_judge_never_submits.py 与 "
        "test_sf_docs.py 断言，并用于 load_credentials.py 的明文凭据迁移检测。"
    )


def test_skill_root_has_no_executable_python():
    """skill 根目录不得放 `.py`（代码一律下沉 scripts/）。

    ⚠ 例外：`brain-inspect-raw-template-create-setting` 的根目录 `ace_lib.py` /
    `helpful_functions.py` 是**历史遗留的原地入口**（脚本按 CWD 相对路径加载），
    且 `scripts/` 下并无同名副本——不是「重复实现」，而是「唯一实现放错了层」。
    在确认调用方全部改路径之前列为白名单，并记录该 skill 的待办。
    """
    whitelist = {
        "brain-inspect-raw-template-create-setting",  # 待办：下沉到 scripts/（§P2-7）
    }
    offenders = []
    for p in _skill_dirs():
        if p.name in whitelist:
            continue
        offenders += [f"{p.name}/{f.name}" for f in p.glob("*.py")]
    assert not offenders, (
        f"skill 根目录出现可执行代码，应下沉到 scripts/：{offenders}"
    )


def test_skill_has_no_runtime_data_dir():
    """skill 内 `data/` 只允许**随 skill 分发的静态资产**，不得是运行期产物。

    ⚠ 2026-10-18 修正（初判有误）：本模块初版断言「skill 内不得有 data/」，
    但 `.gitignore` 154-159 行已有专门裁决——skill 自带 data/ 是**skill 内容**
    （judge 论坛语料、robustness 事件样例等），用 `!Claude/skills/*/data/**` 反向纳入版本控制，
    只排除其下的运行期快照 `data/*/final_expressions.json`。
    ⇒ 正确契约不是「禁 data/」，而是「data/ 内不得残留运行期快照」。
    """
    runtime_pattern = "final_expressions.json"
    offenders = []
    for p in _skill_dirs():
        offenders += [f"{p.name}/data/{f.relative_to(p)}"
                      for f in (p / "data").rglob(runtime_pattern)] if (p / "data").is_dir() else []
    assert not offenders, (
        f"skill 的 data/ 属静态资产（.gitignore 已显式裁决），但其下混入了运行期快照 "
        f"`{runtime_pattern}`：{offenders}。该文件应落到 results/ 或 logs/。"
    )