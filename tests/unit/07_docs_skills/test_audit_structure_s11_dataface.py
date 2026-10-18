# -*- coding: utf-8 -*-
"""test_audit_structure_s11_dataface.py — S11 取面必须覆盖「顶层非脚本件」，且基线缺失不得关掉整闸。

为什么补这一条（2026-10-14 布局审计批次F，`reports/project_layout_audit_20261014.md` §2.C-3）
------------------------------------------------------------------------------------------
S11 的取面一直是 `TOOLS.glob("*.py")`，2026-10-14 上午补了「无扩展名件」一条（活样本
`tools/mcp_py`）。剩下的另一半同样结构性失明：**带扩展名但不是 `.py`** 的顶层件。

活样本是 `tools/skeleton_quota.json`：一个多维配额**数据配置**，在 CLI 层顶层躺了一个多月，
`THEMES.json` 里没有它、`tools/README.md` 里没有它，S4（盘符，只扫 `*.py`）/ S14（按脚本名登记）/
S16（只看报告面）也都看不见它 —— 本轮靠**人读目录**才发现。这正是 §8.12 说的
「同一类漂移出现第二次，就机械拦住」：无扩展名失明与数据件失明是**同一族的两个方向**。

顺带修掉一个 fail-open：旧代码在 `if not baseline:` 处 **`return`**，于是
「.py 存量清单读不到」连带关掉同闸其余全部检查，读数只有一行 WARN，看着像本闸已评估。
现在只跳过确实依赖基线的 `added`/`gone` 两条，其余照校 —— 本文件的
`test_baseline_missing_does_not_disable_the_rest` 就是这条的负例。

⚠ 只读：全部用 tmp_path 沙箱 + monkeypatch，不动真实 `tools/`。
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "audit_structure.py"


@pytest.fixture(scope="module")
def az():
    if not TOOL.is_file():
        pytest.skip("audit_structure.py 不存在")
    spec = importlib.util.spec_from_file_location("wqb_audit_s11_dataface", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["wqb_audit_s11_dataface"] = mod
    spec.loader.exec_module(mod)
    return mod


class _Rows:
    def __init__(self):
        self.rows = []

    def fail(self, check, detail): self.rows.append(("FAIL", check, detail))
    def warn(self, check, detail): self.rows.append(("WARN", check, detail))
    def ok(self, check, detail): self.rows.append(("OK", check, detail))

    def by(self, level):
        return [r for r in self.rows if r[0] == level]


def _sandbox(tmp_path, monkeypatch, az, *, top=(), themes_files=("a.py",), baseline=None):
    """造一棵假 tools/：`top` 是要放在顶层的文件名，其余按 THEMES/基线补齐。"""
    tools = tmp_path / "tools"
    (tools / "x").mkdir(parents=True)
    names = set(top) | {"a.py"}
    for n in names:
        (tools / n).write_text("x\n" if not n.endswith(".py") else "#!/usr/bin/env python\n",
                               encoding="utf-8")
    themes = {"themes": {"x": {"dir": "tools/x", "files": list(themes_files), "moved_files": []}}}
    (tools / "THEMES.json").write_text(json.dumps(themes, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(az, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(az, "TOOLS", tools)
    monkeypatch.setattr(az, "_s11_baseline",
                        lambda: set(baseline) if baseline is not None else set(names) - set(top))
    return tools


def _run(az):
    rep = _Rows()
    az.check_s11_tools_top_frozen(rep)
    return rep


# ---------------------------------------------------------------- ① 真实仓库：不空过
def test_real_repo_top_non_script_files_are_all_registered(az):
    """★ 真实 `tools/` 顶层的每个非脚本件都必须在允许清单里（现状须全绿）。

    这条本身就是「再塞一个数据件」的机械拦截：新增即红，且红在磁盘事实而不是文本断言上。
    """
    if not (REPO / "tools").is_dir():
        pytest.skip("无 tools/")
    on_disk = sorted(p.name for p in (REPO / "tools").iterdir()
                     if p.is_file() and p.suffix and not p.name.startswith(".")
                     and p.suffix != ".py")
    undeclared = sorted(set(on_disk) - set(az.TOOLS_TOP_DATA_ALLOWLIST))
    assert not undeclared, (
        f"tools/ 顶层有未登记的非脚本件 {undeclared}：按 §8.13 迁到归属位"
        f"（区域级 tracking/<R>/reference/、规范级 src/wqb/<包>/、文档 tools/docs/），"
        f"或确认该常驻后登记到 audit_structure.TOOLS_TOP_DATA_ALLOWLIST 并写明理由")


def test_allowlist_entries_actually_live_at_top_level(az):
    """登记项必须**真在**顶层 —— 否则清单会随迁移腐烂，下一个人在表里读到已搬走的件。"""
    if not (REPO / "tools").is_dir():
        pytest.skip("无 tools/")
    on_disk = {p.name for p in (REPO / "tools").iterdir()
               if p.is_file() and not p.name.startswith(".")}
    ghost = sorted(set(az.TOOLS_TOP_DATA_ALLOWLIST) - on_disk)
    assert not ghost, f"允许清单里有顶层已不存在的项：{ghost}"


def test_allowlist_reason_explains_who_reads_it(az):
    """每条登记都要写明「谁读它」——S13 的同款纪律：无理由的清单会退化成黑名单。"""
    for name, why in az.TOOLS_TOP_DATA_ALLOWLIST.items():
        assert why and len(why) >= 8, f"{name} 缺少常驻理由"


# ---------------------------------------------------------------- ② 负例：闸真的会红
def test_stray_data_file_fails(az, tmp_path, monkeypatch):
    """★ 核心负例：顶层多一个未登记的 `foo.json` → 必须 FAIL 并点名该件。"""
    _sandbox(tmp_path, monkeypatch, az, top=("foo.json",))
    rep = _run(az)
    fails = rep.by("FAIL")
    assert fails, f"未登记的顶层数据件未被拦下：{rep.rows}"
    assert any("foo.json" in r[2] for r in fails), rep.rows
    assert any("tracking/" in r[2] and "reference" in r[2] for r in fails), (
        f"FAIL 文案必须给出归属位，否则下一个人只会把它挪回顶层：{fails}")


def test_registered_data_files_pass(az, tmp_path, monkeypatch):
    """清单内的三件（README + 两份登记表）不得报错。"""
    _sandbox(tmp_path, monkeypatch, az,
             top=tuple(az.TOOLS_TOP_DATA_ALLOWLIST))
    rep = _run(az)
    assert not rep.by("FAIL"), rep.rows
    ok = rep.by("OK")
    assert ok and "非脚本件 3 个" in ok[0][2], (
        f"OK 读数要把顶层数据件数量摆出来（只报脚本数=数据件再次隐形）：{rep.rows}")


def test_ghost_allowlist_entry_is_warn_not_fail(az, tmp_path, monkeypatch):
    """清单里多一项磁盘上没有的 → WARN（可清理），不阻断提交。"""
    _sandbox(tmp_path, monkeypatch, az)
    monkeypatch.setattr(az, "TOOLS_TOP_DATA_ALLOWLIST",
                        dict(az.TOOLS_TOP_DATA_ALLOWLIST,
                             **{"__probe_missing__.json": "负例：登记了但顶层没有"}))
    rep = _run(az)
    assert not rep.by("FAIL"), rep.rows
    assert rep.by("WARN"), f"清单腐烂应当 WARN：{rep.rows}"


# ---------------------------------------------------------------- ③ fail-open 自纠
def test_baseline_missing_does_not_disable_the_rest(az, tmp_path, monkeypatch):
    """★ 基线读不到时**只**关掉 added/gone 两条，其余各条照校。

    旧写法 `if not baseline: warn; return` 会让「无扩展名件」「未登记数据件」
    「无主题归属」「moved_files 不符」一起静默 —— 而 pre-commit 只看 FAIL，
    于是 .py 清单一坏整闸就没了，读数看着像已评估。
    """
    _sandbox(tmp_path, monkeypatch, az, top=("foo.json",), baseline=set())
    rep = _run(az)
    assert any("基线为空" in r[2] for r in rep.by("WARN")), (
        f"基线缺失应当 WARN 点名：{rep.rows}")
    assert any("foo.json" in r[2] for r in rep.by("FAIL")), (
        f"基线缺失不得关掉数据件检查（fail-open）：{rep.rows}")


def test_extless_file_still_fails_with_empty_baseline(az, tmp_path, monkeypatch):
    """无扩展名那条同样不得被早退吞掉（同一个 return 的两半）。"""
    _sandbox(tmp_path, monkeypatch, az, top=("no_extension_script",), baseline=set())
    rep = _run(az)
    assert any("no_extension_script" in r[2] for r in rep.by("FAIL")), rep.rows


# ---------------------------------------------------------------- ④ 批次F 的迁移事实
def _nonexist_re():
    """取 `doc_path_refs.py` 的「有意提及」关键词表（**不自己抄一份**）。

    那张表与 `skill_lint._NONEXIST` 由 `test_governance_gates_selfcheck.py` 守对齐；
    本测试若要判「这行是历史叙述还是活指针」，就必须用**同一个**口径，
    否则会出现「治理闸放行、单测拦下」的两套真值 —— 正是本项目反复在修的那类漂移。
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "_dpr_for_s11", REPO / "tools" / "code-audit" / "doc_path_refs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.NONEXIST


def test_skeleton_quota_relocated_to_region_reference(az):
    """`tools/skeleton_quota.json` 已迁进 `tracking/KOR/reference/`，且不再被任何代码按旧路径引用。

    迁移判据（写进件里的 `_owner`）：唯一读取方是本区脚本 + toolkit
    `config/platform_constraints.json._doc` 的既定口径「区域级 skeleton_quota 放战役目录 reference/」。
    """
    old = REPO / "tools" / "skeleton_quota.json"
    new = REPO / "tracking" / "KOR" / "reference" / "skeleton_quota.json"
    assert not old.exists(), f"{old} 仍在 tools/ 顶层（批次F 的迁移动作未完成）"
    assert new.is_file(), f"{new} 不存在"
    # 扫的是「**读者会照它去开文件**」那层面：代码 + 索引 + 长期规范文档。
    # 治理文档（AGENTS.md / 根 README）允许提旧路径，但必须是**带日期状态的叙述**，
    # 由下面那条测试按 `doc_path_refs.NONEXIST` 同口径校。本闸自身（`tools/audit_structure.py`）
    # 与这条测试的正文同理 —— 那是战例叙述、不是指针，扫进来只会逼下次讲战例时删掉上下文。
    faces = [REPO / "docs", REPO / "src", REPO / "Claude" / "skills",
             REPO / "tracking" / "KOR", REPO / "world-quant-brain-mcp",
             REPO / "tools" / "README.md"]
    hits = []
    for root in faces:
        if root.is_file():
            files = [root]
        elif root.is_dir():
            files = [p for p in list(root.rglob("*.md")) + list(root.rglob("*.py"))
                     if "__pycache__" not in p.parts and "archive" not in p.parts]
        else:
            continue
        for p in files:
            if "tools/skeleton_quota.json" in p.read_text(encoding="utf-8", errors="replace"):
                hits.append(str(p.relative_to(REPO)))
    assert not hits, f"仍有文件按旧路径 `tools/skeleton_quota.json` 引用（活文档死指针）：{hits}"


def test_governance_docs_mention_old_path_only_as_dated_history():
    """AGENTS.md 可以写旧路径，但**只能写在带状态的叙述行里**。

    为什么要单独校这一条：批次F 收尾时我在 AGENTS.md 讲「`glob('*.py')` 的取面失明」，
    旧路径就那样进了文档 —— `doc_path_refs.py` 当场判 BROKEN（它是棘轮硬闸，会卡提交），
    而这恰恰是**该保留的提及**（后来人 grep 旧路径要能查到它去了哪）。
    两边的公约就是 `NONEXIST` 关键词表：同行写清「已迁 / 已下架 / 不存在」即放行。
    本测试校的就是这个公约，**不放任 AGENTS.md 退化成「删掉提及」**（那是把误判固化）。
    """
    nonexist = _nonexist_re()
    bad = []
    for md in (REPO / "AGENTS.md", REPO / "CLAUDE.md", REPO / "README.md"):
        if not md.is_file():
            continue
        for i, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if "tools/skeleton_quota.json" in line and not nonexist.search(line):
                bad.append(f"{md.name}:{i}")
    assert not bad, (
        f"旧路径出现在**没有状态说明**的行上（会被 doc_path_refs 判成活文档死指针）：{bad}；"
        "在同一行补「已迁至 tracking/KOR/reference/」这类措辞即可，两边口径一致")


def test_kor_consumer_uses_new_path_and_loud_fallback():
    """读取方要按新路径取件，且**兜底不得静默**。

    实测战例（本轮复现过）：旧代码在文件缺失时 `quota_config = DEFAULT_QUOTA`，
    而 `DEFAULT_QUOTA` 的形状是 `{'structure': {名: float}}`，抽样读的是
    `quota_config['dimensions']['mechanism'][名]['cap']` ⇒ `.get('dimensions')` 拿空 dict
    → 两轮抽样一次不跑 → **选波静默返回 0 条候选**，不报错。
    """
    src = (REPO / "tracking" / "KOR" / "scripts" / "build_wave.py").read_text(encoding="utf-8")
    assert 'os.path.join(ROOT, "reference", "skeleton_quota.json")' in src, (
        "读取方没按迁移后的位置取件")
    assert "def default_quota_config" in src, (
        "缺兜底形状转换：文件缺失时会退回形状不同的 DEFAULT_QUOTA（静默 0 条）")
    assert 'print(f"[warn] 未找到多维配额配置' in src, (
        "配置文件缺失必须顶屏告警，不得静默降级")

    # 用 AST 判「有没有把 DEFAULT_QUOTA 直接当 quota_config 用」——
    # 源码正文里**故意**留着一条解释旧写法的注释，按字符串匹配会把自己写的说明当成违规。
    import ast
    tree = ast.parse(src)
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            names = {t.id for t in node.targets if isinstance(t, ast.Name)}
            val = node.value
            src_names = ({val.id} if isinstance(val, ast.Name)
                         else {b.id for b in getattr(val, "elts", []) if isinstance(b, ast.Name)})
            if "quota_config" in names and "DEFAULT_QUOTA" in src_names:
                bad.append(node.lineno)
    assert not bad, f"这些行仍把 DEFAULT_QUOTA 原样赋给 quota_config（形状不兼容⇒静默 0 条）：{bad}"
