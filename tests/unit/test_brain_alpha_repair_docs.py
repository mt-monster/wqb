# -*- coding: utf-8 -*-
"""brain-alpha-repair 的「声明已上移的术语必须能在目标文件里 grep 到」检查（skills 审查 RE-01 / RE-05 / RE-10）。

旧版 SKILL 声称 6 类配方「已上移进 optimization-v1」，实际那里一个都没有，而这份声明又被 INDEX 当卖点。
现在 references/repair-recipes.md 的「旧声明逐项核销」表逐行登记去向；本测试对每个标「有」的行，
要求其「校验的术语」至少在该行引用的一个文件里出现——以后再写「X 已上移到 Y」而 Y 里没有 X，测试就红。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPAIR = ROOT / "Claude" / "skills" / "brain-alpha-repair"
RECIPES = REPAIR / "references" / "repair-recipes.md"
PC = json.loads((ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "config" / "platform_constraints.json")
                .read_text(encoding="utf-8"))
_SEARCH_DIRS = ("Claude/skills", "tools", "docs/reference", "src")


def _resolve(ref: str, base: Path):
    ref = ref.split("#")[0].split("::")[0].strip()
    if not ref:
        return None
    for cand in ((base / ref).resolve(), (ROOT / ref).resolve()):
        if cand.is_file():
            return cand
    name = Path(ref).name                                  # 只有文件名（如 step5-gates.md）：在仓库相关目录里找
    for d in _SEARCH_DIRS:
        hits = sorted((ROOT / d).rglob(name))
        if hits:
            return hits[0]
    return None


def _table_rows():
    text = RECIPES.read_text(encoding="utf-8")
    section = text.split("## 一、旧声明逐项核销", 1)[1].split("## 二、", 1)[0]
    return [ln for ln in section.splitlines() if ln.startswith("| ") and not ln.startswith("| ---") and "旧声明的配方" not in ln]


def test_every_claimed_location_actually_contains_the_declared_terms():
    rows = _table_rows()
    assert len(rows) == 6, "旧声明共 6 类，逐项核销表应有 6 行"
    checked = 0
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        name, status, where, terms = cells[0], cells[1], cells[2], _terms(cells[3])
        if not terms:
            assert "撤回" in status or "遗失" in status, f"{name}：没有校验术语时必须是「撤回」"
            continue
        refs = re.findall(r"\]\(([^)]+)\)", where) + [t for t in re.findall(r"`([^`]+)`", where) if "." in t and " " not in t]
        files = [f for f in (_resolve(r, RECIPES.parent) for r in refs) if f]
        assert files, f"{name}：登记的去向解析不到任何文件：{where[:80]}"
        blob = "\n".join(f.read_text(encoding="utf-8", errors="replace") for f in files)
        for term in terms:
            assert term in blob, f"{name}：声明已上移，但术语「{term}」在 {[str(f.relative_to(ROOT)) for f in files]} 里 grep 不到"
        checked += 1
    assert checked >= 4


def _terms(cell: str):
    return [t for t in re.findall(r"`([^`]+)`", cell)] if cell.strip() not in ("—", "-") else []


def test_skill_no_longer_claims_recipes_live_in_optimization_v1():
    skill = (REPAIR / "SKILL.md").read_text(encoding="utf-8")
    assert "并不成立" in skill and "已撤回" in skill
    idx = (ROOT / "Claude" / "skills" / "INDEX.md").read_text(encoding="utf-8")
    assert "5 轴旋转 + 6 武器" not in idx, "INDEX 仍把已撤回的配方当卖点"


def test_no_dead_requirements_left_in_skill():
    skill = (REPAIR / "SKILL.md").read_text(encoding="utf-8")
    body = skill.split("## 修复工作流", 1)[1]
    # 这两个说法只允许出现在「说明它为什么被删」的语境里
    assert body.count("trajectory_steps") == 1 and "没有任何写入方" in body
    for stale in ("周额度", "先 5 个多样化探针", "`POST /alphas/{id}/submit`"):
        assert stale not in body.replace("**不要**用 `POST /submit` 探测", "")


def test_recipe_templates_only_use_known_operators():
    text = RECIPES.read_text(encoding="utf-8")
    table = text.split("## 二、三类修复的可复制模板", 1)[1].split("## 三、", 1)[0]
    rows = [ln for ln in table.splitlines() if re.match(r"^\| \*\*(turnover|coverage|correlation)\*\*", ln)]
    assert len(rows) == 3
    known = set(PC["known_ops"])
    for row in rows:
        template_cell = [c.strip() for c in row.strip("|").split("|")][2]
        used = set(re.findall(r"\b([a-z][a-z_0-9]*)\(", template_cell))
        assert not [o for o in used if o not in known], f"模板里有不在 known_ops 的算子：{sorted(o for o in used if o not in known)}"


def test_description_is_no_longer_a_trigger_competing_with_optimization_v1():
    head = (REPAIR / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
    assert "非改进入口" in head
    assert "触发词" not in head and "候选修复 /" not in head
