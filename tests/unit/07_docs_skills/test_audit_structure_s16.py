# -*- coding: utf-8 -*-
"""test_audit_structure_s16.py — S16「报告/产物命名规范」的守护测试。

为什么要有 S16
--------------
AGENTS.md §8.13 的命名规范（日期 `YYYYMMDD` **作后缀**、不带杠、纯 ASCII 无空格）
此前只写在文档里。2026-10-08 第二轮输出目录复核发现两个后果：

  ① 第一轮治理把 `output_report/`+`reports/` 的日期带杠件全部改名，却**漏扫了
     `tracking/` 顶层** —— 4 个 `tracking/2026-10-0X_robustness.md` 一直躺着；
  ② 之后仍有会话把分析报告写进 `cache/`（不入库，`git clean -fd` 即永久丢失）。

文字纪律守不住持续的写入。S16 把它变成读数：**存量入基线 → WARN，新增违规 → FAIL**。

本文件只测两件事：① S16 挂进了 `CHECKS`（否则写了函数也没人跑）；
② 命名判据本身判得对（纯函数 `_naming_violations`，无需沙箱、只读）。
"""
import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "audit_structure.py"


@pytest.fixture(scope="module")
def az():
    if not TOOL.is_file():
        pytest.skip("audit_structure.py 不存在")
    spec = importlib.util.spec_from_file_location("wqb_audit_s16", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["wqb_audit_s16"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_s16_is_registered_in_checks(az):
    """S16 必须挂进 CHECKS，否则写了检查函数也没人跑（S13 的同款守）。"""
    assert "s16" in az.CHECKS, "S16 未注册到 CHECKS"
    assert az.CHECKS["s16"][1] is az.check_s16_output_naming


@pytest.mark.parametrize("name", [
    "skills_review_20261003.md",          # §8.13 的正例
    "output_report_20261008.md",
    "DEU_field_profile_complete_20261008.md",
    "ra_pipeline_stage_audit_20260916.md",
    "d9_status_backfill_rollback_20260928.json",
    "robustness_20261007.md",
])
def test_compliant_names_pass(az, name):
    assert az._naming_violations(name) == [], f"{name} 应合规却被判违规"


@pytest.mark.parametrize("name,kw", [
    ("2026-10-08_robustness.md", "带杠"),        # 上一轮漏网的实际形态
    ("db_schema_audit_2026-08-26.md", "带杠"),
    ("eur_d1_20260924_financing_mode_b1.md", "不在末尾"),  # 日期夹在中间
    ("ra_pipeline_stage_audit_20260916_v3.md", "不在末尾"),
    ("glb_campaign_20261008_breakthrough.md", "不在末尾"),
    ("字段报告 20261008.md", "ASCII"),           # 非 ASCII + 空格
])
def test_violating_names_are_caught(az, name, kw):
    bad = az._naming_violations(name)
    assert bad, f"{name} 违反规范却没被判出来"
    assert any(kw in b for b in bad), f"{name} 判出来了但理由不含「{kw}」：{bad}"


def test_scan_exempts_readme_and_non_report_suffixes(az):
    """目录说明与非报告类扩展名不进扫描面（否则会把 README / 图片等误判成产物）。"""
    assert "README.md" in az.S16_EXEMPT_NAMES
    assert ".md" in az.S16_SUFFIXES
    assert ".png" not in az.S16_SUFFIXES and ".bin" not in az.S16_SUFFIXES


def test_scan_covers_the_layer_that_was_missed(az):
    """扫描面必须含 `tracking/` 顶层 —— 第一轮治理漏的正是这一层。"""
    src = TOOL.read_text(encoding="utf-8")
    assert '"tracking/*.md"' in src or "'tracking/*.md'" in src, (
        "S16 的 git ls-files 路径表缺 `tracking/*.md`："
        "第一轮治理漏掉的就是 tracking/ 顶层，扫描面不能再退回只看 output_report/reports")


# ---------------------------------------------------------------- 2026-10-10 新增
# P2-D：规则④「人工报告必须有日期」+ 机器产物豁免 + 未跟踪件 WARN 预检。
# 动因：§8.13 原写「产物与报告**一律** `YYYYMMDD` 作后缀」，而实现只在**已含日期**时
# 校验格式位置 ⇒ 无日期的文件名永不过闸、也永进不了基线（实测 87 个）。文档与实现漂移，
# 下一个人读 §8.13 会以为那批都是违规。故补齐实现 + 给机器产物开口子（两者都要守住）。

def test_rule4_flags_missing_date_for_hand_written_reports(az):
    """人工报告无日期 ⇒ 判违规（规则④，2026-10-10 P2-D）。"""
    bad = az._naming_violations("output_report/alpha_template_library_summary.md")
    assert bad == ["缺日期（报告应带 YYYYMMDD）"], f"无日期的人工报告应被判缺日期：{bad}"


def test_rule4_exempts_machine_generated_artifacts(az):
    """机器产物无日期 ⇒ 合规。

    `*_ideas.md` / `*_campain.md` 由生成器模板拼名，消费方依赖**同名覆盖**：
      - `src/wqb/workflow/nodes/feature_engineering.py` 的 `stale_ideas_md_path`
      - `dataset_experience.py` 生成 + `step9_audit.py` 校验的既定文件名（§8.13）
    塞日期会让同一数据集每跑一次多一个文件、stale 比对失效 ⇒ 必须豁免。
    """
    for name in ("fe_EUR_delay1_news36_ideas.md", "USA_pv1_13f_campain.md"):
        rel = f"output_report/{name}"
        assert az._is_machine_name(rel), f"{name} 应被识别为机器产物"
        assert az._naming_violations(rel, machine_ok=True) == [], (
            f"{name} 是机器产物，不该因缺日期被判违规")


def test_machine_exemption_does_not_relax_other_rules(az):
    """豁免只针对规则④：机器产物违反其它三条照样 FAIL。

    守住「开口子」的边界 —— 否则豁免会静默扩大成「机器产物怎么命名都行」。
    """
    assert az._naming_violations("2026-10-01_x_ideas.md", machine_ok=True), (
        "带杠日期对机器产物也应判违规")
    assert az._naming_violations("x_20261001_ideas.md", machine_ok=True), (
        "日期不在末尾对机器产物也应判违规")
    assert az._naming_violations("字段 2026_ideas.md", machine_ok=True), (
        "非 ASCII / 空格对机器产物也应判违规")


def test_machine_suffixes_are_documented(az):
    """豁免清单必须写明理由（否则下一个人会以为是随手开的洞）。"""
    src = TOOL.read_text(encoding="utf-8")
    i = src.index("S16_MACHINE_SUFFIXES")
    # 理由注释写在常量**上方**，故窗口要同时覆盖前文与后文
    assert "stale_ideas_md_path" in src[max(0, i - 900):i + 400], (
        "S16_MACHINE_SUFFIXES 的注释必须点名 stale_ideas_md_path 这个真实约束，"
        "否则豁免理由不可追溯")


def test_untracked_prescan_exists_and_is_warn_only(az):
    """未跟踪件预检必须存在，且**只 WARN 不 FAIL**。

    背景：`_s16_targets()` 只取 git 跟踪的（有意取舍：在途文件不该拦别人的提交），
    代价是违规在 `git add` 前完全隐形。2026-10-10 实测复发一次
    （`tracking/2026-10-09_robustness.md` 静默通过、一 add 即 FAIL，同类问题第二轮）。
    预检把它提前到「写盘即见」；但语义必须是 WARN —— 并行会话的在途文件不该互相拦截。
    """
    assert hasattr(az, "_s16_untracked"), "缺 _s16_untracked()：命名违规会退回 git add 前不可见"
    body = TOOL.read_text(encoding="utf-8")
    start = body.index("def check_s16_output_naming")
    seg = body[start:]
    assert "rep.warn" in seg, "S16 主检查里找不到 WARN 分支"
    pend_call = "pend = _s16_untracked()"
    assert pend_call in seg, "S16 主检查没接上未跟踪件预检"
    # 未跟踪件不得进 new_ones（那会变成 FAIL）
    assert "new_ones" in seg


def test_untracked_prescan_sees_the_recurring_violation_shape(az):
    """预检的判定函数必须逮到 2026-10-10 复发的那个形态（未跟踪 + 日期带杠）。

    不真造文件（避免污染 `tracking/`），只验 `_naming_violations` 对带杠名的结论 ——
    预检本身调的就是这个纯函数，判不出来则扫到了也看不见。
    """
    bad = az._naming_violations("tracking/2026-10-09_robustness.md")
    assert bad == ["日期带杠（应为 YYYYMMDD 无杠）"], (
        f"带杠日期必须判出「日期带杠」，否则预检即使扫到也看不见：{bad}")


def test_output_report_scripts_are_caught(az, monkeypatch):
    """规则⑤：`output_report/` 混入 `.py` 必须被逮到（2026-10-10 第四轮 P1-4）。

    起因：第三轮人工核过「0 子目录、0 .py」却**没有机械闸守**（`S16_SUFFIXES` 只含
    报告类扩展名，命名规则天然管不到 `.py`），随后即再现 `output_report/diff_t4.py`。
    语义与命名预检同款分岔：跟踪件 FAIL（进索引就是提交时刻）、在途件 WARN。
    """
    assert hasattr(az, "_s16_script_hits"), (
        "缺 _s16_script_hits()：产物目录混入脚本将永远隐形")
    # 闸的自检：真实仓库当前不得有脚本混入（须在 monkeypatch 之前，否则拿到注入的假值）
    tracked, pend = az._s16_script_hits()
    assert tracked == [] and pend == [], (
        f"output_report/ 现有脚本混入，按 §8.13 迁出：{tracked + pend}")

    class _Rep:
        def __init__(self):
            self.fails, self.warns, self.oks = [], [], []

        def fail(self, t, m):
            self.fails.append(m)

        def warn(self, t, m):
            self.warns.append(m)

        def ok(self, t, m):
            self.oks.append(m)

    monkeypatch.setattr(az, "_s16_script_hits",
                        lambda: (["output_report/bad.py"], ["output_report/pending.py"]))
    rep = _Rep()
    az.check_s16_output_naming(rep)
    assert any("bad.py" in m and "不得混入脚本" in m for m in rep.fails), (
        "跟踪的 output_report/*.py 必须 FAIL")
    assert any("pending.py" in m for m in rep.warns), (
        "在途（未跟踪）的 output_report/*.py 必须 WARN")


# ---------------------------------------------------------------- 2026-10-14 新增（规则⑥）
# 布局审计 §4：`docs/` 整个不在 S16 的取面里（`_s16_targets()` 只有
# output_report / reports / tracking 顶层），于是本轮在 `docs/reference/` 抓到两份
# 结论式报告时，命名与归属两道读数都是绿的 —— **结构性失明**，与 S11 的扩展名失明、
# S18 的顶层失明同一类。补面后必须同时守住「docs/ 不要求日期」这条边界，
# 否则会把 docs/ 的 79 篇规范文档全判成违规（实测无日期件占多数）。

def test_docs_face_is_not_vacuous(az):
    """取面必须真取到东西：空面 = 加了个永不执行的分支（同 S14/S18/S20 的非空过要求）。"""
    face = az._s16_docs_targets()
    assert len(face) >= 50, f"docs/ 面异常薄（{len(face)} 件），取面大概率写错了"
    assert any(rel.startswith("docs/plans/") for rel in face), (
        "docs/plans/ 必须**进面**（豁免只发生在判据层，不在取面层排除 —— "
        "否则该目录里的非 ASCII / 大写名也一并瞎了）")


def test_docs_rule_does_not_require_a_date(az):
    """docs/ 是长期规范区，无日期**不是**违规（规则④不适用于本面）。

    这条是本轮最容易写错的地方：直接把报告面的 `_naming_violations` 拿来用，
    `docs/reference/tool_registry.md`、`docs/experience/01_platform_gates.md`
    这类正当文件名会全红 —— 一道天天误红的闸等于没有闸。
    """
    for rel in ("docs/reference/tool_registry.md",
                "docs/experience/01_platform_gates.md",
                "docs/governance/branch_policy.md",
                "docs/design/prod_corr_persistence_design_20260918.md"):
        assert az._docs_naming_violations(rel) == [], f"{rel} 应合规却被判违规"


def test_docs_rule_flags_the_two_real_cases(az):
    """抓到的那两件原样复现：`CODE_QUALITY_SUMMARY.md` / `INTEGRATION_COMPLETE.md`。

    2026-08 的一次性完工总结躺在规范目录、大写命名。§8.13 的大写豁免只给**区域码**
    （DEU/EUR/…），纯英文大写开头不在豁免列 —— 实测全 docs/ 面唯一的大写开头只剩 3 个 README。
    """
    for rel in ("docs/reference/CODE_QUALITY_SUMMARY.md",
                "docs/reference/INTEGRATION_COMPLETE.md"):
        bad = az._docs_naming_violations(rel)
        assert any("大写" in b for b in bad), f"{rel} 应判出大写开头违规：{bad}"


def test_docs_plans_exempt_is_date_shape_only(az):
    """`docs/plans/` 只豁免**日期形态**（§8.13 明示它保持 `YYYY-MM-DD-<主题>.md` 前缀）。

    非 ASCII 与大写在 plans 里照样判 —— 豁免范围必须钉死，否则整个目录变成永久盲区。
    """
    assert az._docs_naming_violations("docs/plans/2026-08-02-wqb-src-reconstruction.md") == []
    bad = az._docs_naming_violations("docs/plans/2026-10-04_中文计划.md")
    assert any("ASCII" in b for b in bad), f"plans 豁免不得扩到非 ASCII：{bad}"
    bad2 = az._docs_naming_violations("docs/plans/2026-10-04_PLAN.md")
    assert any("大写" in b for b in bad2), f"plans 豁免不得扩到大写命名：{bad2}"
    # 面外目录（reference）里的带杠日期仍要判
    assert any("带杠" in b for b in az._docs_naming_violations("docs/reference/2026-10-04_x.md"))


def test_docs_face_passes_on_this_repo(az):
    """本轮已把两份结论件迁去 reports/ ⇒ 真仓库的 docs/ 面必须 0 违规。

    再红就说明有人又把一次性报告塞回规范目录（这次是第二轮：批次2 清过 docs/ 顶层的日期件）。
    """
    viol = {rel: az._docs_naming_violations(rel) for rel in az._s16_docs_targets()}
    bad = {k: v for k, v in viol.items() if v}
    assert not bad, f"docs/ 面违反 §8.13：{bad}"


def test_docs_violation_fails_and_names_the_remedy(az, monkeypatch):
    """可红 + 报错给得出**归属**修法：不是只说「改名」，要说清结论件该去 reports/。"""

    class _Rep:
        def __init__(self):
            self.fails, self.warns, self.oks = [], [], []

        def fail(self, t, m):
            self.fails.append(m)

        def warn(self, t, m):
            self.warns.append(m)

        def ok(self, t, m):
            self.oks.append(m)

    def fake(others=False):
        return [] if others else ["docs/reference/MY_ONE_OFF_AUDIT.md"]

    monkeypatch.setattr(az, "_s16_docs_targets", fake)
    rep = _Rep()
    az.check_s16_output_naming(rep)
    hit = [m for m in rep.fails if "MY_ONE_OFF_AUDIT" in m]
    assert hit, f"docs/ 违规必须 FAIL：{rep.fails}"
    assert "reports/" in hit[0], f"修法必须指出结论件去处：{hit[0]}"


def test_docs_face_fails_closed(az, monkeypatch):
    """取不到 docs/ 清单不得当作通过：静默空集 = 这条规则形同虚设（与 S18 同口径）。"""

    class _Rep:
        def __init__(self):
            self.fails, self.warns, self.oks = [], [], []

        def fail(self, t, m):
            self.fails.append(m)

        def warn(self, t, m):
            self.warns.append(m)

        def ok(self, t, m):
            self.oks.append(m)

    def boom(others=False):
        raise RuntimeError("git ls-files 失败 rc=128")

    monkeypatch.setattr(az, "_s16_docs_targets", boom)
    rep = _Rep()
    az.check_s16_output_naming(rep)
    assert any("docs/" in m and "不当作" in m for m in rep.fails), rep.fails


