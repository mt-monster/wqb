# -*- coding: utf-8 -*-
"""optimization-v1 文档与代码的一致性守护（skills 审查 OP-04/06/07/09/11/12/13/16）。

  1. reference.md §8 主题算子表：「已核验」栏 ⊂ known_ops，「未列入清单」栏 ∩ known_ops = ∅，且都不含 ghost / inaccessible 算子；
  2. structural-interaction-forms.md 里出现的每个算子都在 known_ops（文档声称「均已核验」）；
  3. 不再指示写自建结果文本文件 / 不再出现旧的工具名与 0.5 的 salvage 过滤；
  4. 组合腿救援的入场方式与 `platform_constraints.json` 的 `spread_signal_ruling` 一致（F1 仅限同源）；
  5. Mode A 校验层三段与 arXiv 外发边界都写在 SKILL 里。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SK = ROOT / "Claude" / "skills" / "wq-brain-alpha-optimization-v1"
PC = json.loads((ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "config" / "platform_constraints.json")
                .read_text(encoding="utf-8"))
KNOWN = set(PC["known_ops"])
BAD = set(PC.get("ghost_ops") or []) | set(PC.get("inaccessible_ops") or [])


def _t(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _theme_rows():
    text = _t(SK / "reference.md")
    section = text.split("## 8. 主题配额", 1)[1].split("## 9.", 1)[0]
    rows = [ln for ln in section.splitlines() if re.match(r"^\| [A-F] \|", ln)]
    assert len(rows) == 6, "主题表应有 A–F 六行"
    return rows


def _ops(cell: str):
    return re.findall(r"`([a-z][a-z_0-9]*)`", cell)


def test_theme_table_verified_column_matches_known_ops():
    for row in _theme_rows():
        cells = [c.strip() for c in row.strip("|").split("|")]
        verified, unverified = _ops(cells[2]), _ops(cells[3])
        assert verified, f"主题 {cells[0]} 没有任何已核验算子"
        assert not [o for o in verified if o not in KNOWN], f"{cells[0]} 的「已核验」含不在 known_ops 的算子：{[o for o in verified if o not in KNOWN]}"
        assert not [o for o in unverified if o in KNOWN], f"{cells[0]} 的「未列入清单」栏已在 known_ops 内，请挪到已核验栏：{[o for o in unverified if o in KNOWN]}"
        assert not (set(verified) | set(unverified)) & BAD, f"{cells[0]} 列了 ghost / inaccessible 算子"


def test_every_theme_has_a_verified_operator_so_the_4_of_6_quota_is_satisfiable():
    verified_themes = sum(1 for row in _theme_rows() if _ops([c.strip() for c in row.strip("|").split("|")][2]))
    assert verified_themes >= 4


def test_forms_doc_only_uses_verified_operators():
    text = _t(SK / "references" / "structural-interaction-forms.md")
    used = set(re.findall(r"\b([a-z][a-z_0-9]*)\(", text)) - {"NaN"}
    assert not [o for o in used if o not in KNOWN], f"形态库出现不在 known_ops 的算子：{sorted(o for o in used if o not in KNOWN)}"
    assert not used & BAD


def test_forms_f1_is_restricted_to_same_source_like_the_user_ruling():
    text = _t(SK / "references" / "structural-interaction-forms.md")
    assert "仅限同源辅助腿" in text and "spread_cross_dataset" in text
    ruling = PC["spread_signal_ruling"]
    assert any("不同数据集" in v for v in ruling["violation_when"]), "spread_signal_ruling 的违规条件变了：请同步形态库 F1"
    # 每个入场方式都在判据表里
    for way in ("① 条件", "② 分组轴", "③ 残差化", "④ 协动对象", "⑤ 同源价差"):
        assert way in text


def test_no_self_made_result_text_file_and_no_stale_names():
    # 「不要另写 …_optimization_results.txt」这类**禁止句**里允许出现旧名；其余行不得出现
    blob = "\n".join(ln for p in (SK / "SKILL.md", SK / "reference.md", SK / "examples.md")
                     for ln in _t(p).splitlines() if "不要" not in ln)
    for stale in ("_optimization_results.txt", "open(target_file", "create_multiSim", "get_SimError_detail", "min_sharpe=0.5",
                  "Skill-ImproveTheme"):
        assert stale not in blob, f"optimization-v1 文档里还有过期写法：{stale}"
    assert "harvest_multisim_results" in blob and "backtest_results" in blob


def test_skill_declares_operator_ceiling_is_ppa_only_and_uses_config_for_thresholds():
    skill = _t(SK / "SKILL.md")
    assert "**PPA** 候选的 `operatorCount` 上限 8" in skill and "REGULAR 无此上限" in skill
    for hand_copied in ("1%–40%", "Turnover 在 1%", "Sharpe > 1.58", "Fitness > 1.0"):
        assert hand_copied not in skill, f"SKILL 里手抄了阈值：{hand_copied}（引用 wqb.config.GATES_INTERNAL）"
    assert "GATES_INTERNAL" in skill


def test_mode_a_validation_layer_and_gate_command_are_documented():
    skill = _t(SK / "SKILL.md")
    for needle in ("ghost-audit", "wave_gate.py", "--batch-type repair", "不查幽灵算子"):
        assert needle in skill
    # 命令里的 --batch-type 取值必须是 wave_gate 真实支持的
    src = (ROOT / "tools" / "wave_gate.py").read_text(encoding="utf-8")
    assert 'choices=("explore", "repair", "probe")' in src


def test_description_no_longer_promises_a_prod_number():
    head = _t(SK / "SKILL.md").split("---", 2)[1]
    assert "压到" not in head.replace("不承诺把 PROD 压到某个数", "") and "不承诺" in head   # 只允许出现「不承诺…」的否定句
    assert "D0-P" in head


def test_arxiv_egress_boundary_is_stated_and_script_single_copy():
    skill = _t(SK / "SKILL.md")
    for needle in ("export.arxiv.org", "OPENAI_API_KEY", "只发通用关键词", "api.deepseek.com"):
        assert needle in skill
    assert not (ROOT / "Claude" / "skills" / "brain-explain-alphas" / "scripts" / "arxiv_api.py").exists(), "arxiv_api.py 应只有一份"
    assert (SK / "scripts" / "arxiv_api.py").exists()
