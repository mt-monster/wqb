# -*- coding: utf-8 -*-
"""审计闸自测：audit_write_targets.py 的白名单判定 + 棘轮行为（2026-10-20）。

钉住两件事：
1) **规则真的生效**：裸相对路径的写盘必须判 VIOLATE；§8.13 白名单目录必须放行。
2) **不误吞**：短变量名（`p.write_text`）解析不出路径 → 判 UNKNOWN，
   绝不判 VIOLATE（宁可漏报，不可用假证据卡提交）。
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "code-audit" / "audit_write_targets.py"


def _load_tool():
    """按文件路径加载（tools/code-audit/ 无 __init__.py）。"""
    spec = importlib.util.spec_from_file_location("audit_write_targets", TOOL)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_whitelist_allows_output_report():
    at = _load_tool()
    kind, _ = at.classify_target('Path("output_report/campaign_summary.md").write_text(...)')
    assert kind == "ALLOWED"


def test_whitelist_allows_tracking_region_dir():
    at = _load_tool()
    kind, label = at.classify_target('ROOT / "tracking" / "IND" / "results.json"')
    assert kind == "ALLOWED", f"tracking 区域面未放行：{label}"


def test_whitelist_allows_cache_logs_data_results():
    at = _load_tool()
    for target in ['Path("cache/foo.bin")', 'Path("logs/x.log")',
                   'Path("data/wqb.db")', 'Path("results/x.json")']:
        kind, _ = at.classify_target(target)
        assert kind == "ALLOWED", f"{target} 应放行"


def test_whitelist_allows_tempfile_and_wqb_root():
    at = _load_tool()
    for target in ["/tmp/foo.json", "tmp_path / 'x'",
                   "tempfile.NamedTemporaryFile()", "WQB_TASK_ROOT"]:
        kind, _ = at.classify_target(target)
        assert kind == "ALLOWED", f"{target} 应放行"


def test_violate_bare_relative_filename():
    """裸文件名（无目录前缀，含扩展名）落 cwd → 违规。"""
    at = _load_tool()
    kind, label = at.classify_target('"scheduler_state.json"')
    assert kind == "VIOLATE", f"裸文件名未判违规：{label}"
    assert "裸文件名" in label


def test_violate_writes_into_source_dir():
    at = _load_tool()
    kind, label = at.classify_target('Path("src/wqb/state.json").write_text(...)')
    assert kind == "VIOLATE", f"写进 src/ 未判违规：{label}"
    assert label == "src"


def test_violate_writes_into_tools_dir():
    at = _load_tool()
    kind, label = at.classify_target('Path("tools/tmp_debug.json")')
    assert kind == "VIOLATE", f"写进 tools/ 未判违规：{label}"
    assert label == "tools"


def test_violate_writes_into_docs_or_reports():
    at = _load_tool()
    for t in ['Path("docs/foo.md")', 'Path("reports/foo.md")']:
        kind, label = at.classify_target(t)
        assert kind == "VIOLATE", f"{t} 未判违规：{label}"


def test_violate_matches_docs_without_trailing_slash():
    """Python 里 `REPO / "docs" / "x"` 展开后是 `"docs"`（无尾斜杠），
    这类写法必须被识别为违规。2026-10-20 index_tables.py 就踩过：
    `ENV_DOC = REPO / "docs" / "env_and_switches.md"` 一度被漏报成 UNKNOWN。"""
    at = _load_tool()
    for t in ['REPO / "docs" / "env_and_switches.md"', '"docs" "env_registry.json"']:
        kind, label = at.classify_target(t)
        assert kind == "VIOLATE", f"无斜杠形式漏报：{t} → {kind}"
        assert label == "docs"


def test_violate_ignores_identifier_prefix():
    """`my_docs` / `docs_count` 这种含 docs 的标识符不算违规（前/后有单词字符）。"""
    at = _load_tool()
    for t in ['my_docs_xxx', 'docs_count']:
        kind, _ = at.classify_target(t)
        assert kind != "VIOLATE", f"标识符含 docs 被误判：{t}"


def test_unknown_for_short_varname_is_not_violate():
    """短变量名（`p`/`tmp`/`out`）解析不出路径 → UNKNOWN，绝不判 VIOLATE。

    这是防「假证据卡提交」的关键：解析失败不能升级成违规。
    """
    at = _load_tool()
    # 模拟 `p.write_text(...)` 解析出来的字符串：只有变量名，没有路径字面量
    for material in ["p p write_text", "out out write_text", "tmp tmp write_text"]:
        kind, _ = at.classify_target(material)
        assert kind != "VIOLATE", f"解析失败被误判违规：{material}"


def test_violate_priority_over_allow_substring():
    """违规优先级高于白名单：`docs/x/tmp.txt` 应判违规而不是因为含 'tmp' 被放行。"""
    at = _load_tool()
    kind, label = at.classify_target('Path("docs/some/tmp_foo.json")')
    assert kind == "VIOLATE", f"违规片段被 'tmp' 子串遮蔽：{label}"


def test_full_scan_current_state_has_no_new_violations(tmp_path, monkeypatch):
    """当前全仓扫描：0 新增违规（棘轮基线为空 = 当前零高危）。"""
    at = _load_tool()
    items = at.scan(at.REPO)
    violations = [i for i in items if i["kind"] == "VIOLATE"]
    # 允许 UNKNOWN（解析不出路径），但不允许 VIOLATE
    assert violations == [], (
        "发现未登记的写盘违规：\n" +
        "\n".join(f"  {v['file']}:{v['line']}  ← {v['label']} | {v['hint'][:60]}"
                  for v in violations[:10])
    )


def test_ratchet_blocks_new_violation_beyond_baseline(tmp_path, monkeypatch):
    """棘轮：基线外的违规必须阻断（返回码 1）。"""
    at = _load_tool()
    # 手动造一条「不在基线」的违规
    baseline = set()  # 空基线
    new_viol = {"file": "tools/new_bad.py", "line": 1,
                "kind": "VIOLATE", "label": "tools", "hint": "Path('tools/x.json')"}
    assert at._fingerprint(new_viol) not in baseline
    # 模拟 main 的判定逻辑
    new_violations = [v for v in [new_viol] if at._fingerprint(v) not in baseline]
    assert len(new_violations) == 1, "基线外的违规未被识别为新增"


def test_update_baseline_roundtrip(tmp_path, monkeypatch):
    """--update-baseline 写的文件能被 load_baseline 读回来。"""
    at = _load_tool()
    fake_base = tmp_path / "baseline.json"
    monkeypatch.setattr(at, "BASELINE", fake_base)
    items = {"tools/a.py::VIOLATE::src", "src/wqb/b.py::VIOLATE::docs/"}
    at.save_baseline(items)
    assert fake_base.exists()
    loaded = at.load_baseline()
    assert loaded == items


def test_baseline_persists_without_line_numbers(tmp_path, monkeypatch):
    """基线指纹不含行号：无关改动导致行号漂移不影响棘轮。"""
    at = _load_tool()
    item = {"file": "tools/a.py", "line": 42,
            "kind": "VIOLATE", "label": "docs", "hint": "Path('docs/x')"}
    fp = at._fingerprint(item)
    item2 = dict(item, line=999)  # 行号变了
    assert at._fingerprint(item2) == fp, "指纹里含行号（应不含）"
