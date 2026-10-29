# -*- coding: utf-8 -*-
"""``wqb.corr_timing`` 与 ``tools/probe/corr_timing_report.py`` 的守卫（2026-10-28 P2-8）。

打点是**跨进程的唯一事实源**：MCP 服务把 ``[corr-t] {...}`` 写进 stderr（由
``tools/start_wq_mcp.py`` 合并到 ``logs/wq-brain-http.log``），本模块负责解析与汇总，
CLI 只做 IO 与排版。两边靠字段名契约耦合，故除了纯函数单测之外，还做**写入方
AST 反查**：打点里出现的每个关键字都必须在 ``FIELDS`` 里声明（反过来漏声明会导致
Agent 侧新增一个永远读不到的死字段——与 S1「闸对结构性失明」同族）。
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
for _p in (str(ROOT / "src"), str(ROOT / "world-quant-brain-mcp"), str(ROOT / "tools")):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb import corr_timing as ct  # noqa: E402

CLI = ROOT / "tools" / "probe" / "corr_timing_report.py"


# ---------------------------------------------------------------- 解析
class TestParseLine:
    def test_marker_mid_line_and_trailing_text(self):
        line = ('[INFO] 2026-10-28 [corr-t] {"event": "success", "alpha": 123, '
                '"elapsed_ms": "12.7", "ts": "2026-10-28T00:00:00"} 尾巴粘连')
        rec = ct.parse_line(line)
        assert rec is not None
        assert rec["event"] == "success"
        assert rec["alpha"] == "123"          # 统一成 str（日志里可能混进 int）
        assert rec["elapsed_ms"] == 12        # 字符串数字也收

    def test_negative_elapsed_clamped_to_zero(self):
        r = ct.parse_line('[corr-t] {"event":"busy","alpha":"A","elapsed_ms":-5}')
        assert r["elapsed_ms"] == 0

    def test_unparseable_elapsed_defaults_zero(self):
        r = ct.parse_line('[corr-t] {"event":"busy","alpha":"A","elapsed_ms":"abc"}')
        assert r["elapsed_ms"] == 0

    @pytest.mark.parametrize("line", [
        "",                                            # 空行
        "普通日志没有打点标记",
        "[corr-t] ",                                   # 只有标记
        "[corr-t] {bad json",                          # 坏 JSON
        "[corr-t] [1, 2, 3]",                          # 非 dict
        '[corr-t] {"alpha": "A"}',                     # 缺 event
        '[corr-t] {"event": "", "alpha": "A"}',        # 空 event
        '[corr-t] {"event": 42, "alpha": "A"}',        # 非字符串 event
    ])
    def test_rejects_bad_lines(self, line):
        assert ct.parse_line(line) is None

    def test_parse_lines_keeps_order_and_drops_noise(self):
        lines = [
            "[corr-t] {\"event\":\"busy\",\"alpha\":\"A\"}",
            "noise",
            "[corr-t] {\"event\":\"success\",\"alpha\":\"B\"}",
        ]
        recs = ct.parse_lines(lines)
        assert [r["event"] for r in recs] == ["busy", "success"]

    def test_parse_file_missing_returns_empty(self, tmp_path):
        assert ct.parse_file(str(tmp_path / "nope.log")) == []

    def test_parse_file_tolerates_decoding_errors(self, tmp_path):
        p = tmp_path / "x.log"
        p.write_bytes(b'[corr-t] {"event":"busy","alpha":"A"}\n\xff\xfe garbage\n')
        recs = ct.parse_file(str(p))
        assert len(recs) == 1 and recs[0]["event"] == "busy"


# ---------------------------------------------------------------- 纯函数
class TestHelpers:
    def test_pct_nearest_rank(self):
        vals = [10, 20, 30, 40]
        assert ct._pct([], 50) == 0
        assert ct._pct(vals, 0) == 10
        assert ct._pct(vals, 100) == 40
        assert ct._pct(vals, 50) == 30
        assert ct._pct([7], 90) == 7

    @pytest.mark.parametrize("ts,ok", [
        ("2026-10-28T00:00:00", True),
        ("2026-10-28 00:00:00", True),
        ("2026-10-28", False),
        ("", False),
        (None, False),
    ])
    def test_ts_of(self, ts, ok):
        assert (ct._ts_of({"ts": ts}) is not None) is ok

    def test_sec_rounding(self):
        assert ct._sec(9499) == 9.5
        assert ct._sec(0) == 0.0

    def test_default_log_path_under_repo_logs(self):
        p = ct.default_log_path()
        assert p.endswith(os.path.join("logs", "wq-brain-http.log"))


# ---------------------------------------------------------------- 汇总
def _records():
    return [
        {"event": "cache_hit", "alpha": "A1", "elapsed_ms": 100,
         "ts": "2026-10-28T00:00:00", "source": "cache:corr_cache"},
        {"event": "pre_read_hit", "alpha": "A2", "elapsed_ms": 250,
         "ts": "2026-10-28T00:01:00", "source": "alpha_detail_cached"},
        {"event": "inflight_join", "alpha": "A1", "elapsed_ms": 5000,
         "ts": "2026-10-28T00:05:00", "source": "alpha_detail_cached"},
        {"event": "same_alpha_join", "alpha": "A3", "elapsed_ms": 7000,
         "ts": "2026-10-28T00:10:00", "source": "alpha_detail_cached"},
        {"event": "success", "alpha": "A4", "elapsed_ms": 94000,
         "ts": "2026-10-28T00:12:00", "source": "platform_poll", "computed": True},
        {"event": "pending", "alpha": "A5", "elapsed_ms": 120000,
         "ts": "2026-10-28T00:14:00", "retry_after": 195},
        {"event": "busy", "alpha": "A6", "elapsed_ms": 3,
         "ts": "2026-10-28T00:15:00", "retry_after": 180, "cooldown": True},
        {"event": "inflight_busy", "alpha": "A6", "elapsed_ms": 4,
         "ts": "2026-10-28T00:16:00", "retry_after": 30},
        {"event": "same_alpha_wait_timeout", "alpha": "A7", "elapsed_ms": 25000,
         "ts": "2026-10-28T00:17:00"},
        {"event": "terminal", "alpha": "A8", "elapsed_ms": 12,
         "ts": "2026-10-28T00:18:00", "http_status": 403},
        {"event": "success", "alpha": "A4", "elapsed_ms": 2,
         "ts": "2026-10-28T00:19:00", "source": "platform_poll", "computed": False},
    ]


class TestSummarize:
    def test_outcomes_exclude_precursor_event(self):
        s = ct.summarize(_records())
        o = s["outcomes"]
        # same_alpha_wait_timeout 是 busy 的前导事件，不进分母（否则一次失败数两次）
        assert o["got_value"] == 6
        assert o["no_value"] == 4
        assert o["value_rate"] == pytest.approx(0.6)
        assert o["joins"] == 2
        assert o["cache_hits"] == 1
        assert o["pre_read_hits"] == 1
        assert o["platform_polls"] == 4
        assert o["computed"] == 1
        assert o["computed_of_success"] == 2

    def test_time_buckets(self):
        t = ct.summarize(_records())["time_s"]
        assert t["platform_success"] == pytest.approx(94.0)
        assert t["platform_pending"] == pytest.approx(120.0)
        assert t["join_wait"] == pytest.approx(12.0)
        assert t["same_alpha_wait_timeout"] == pytest.approx(25.0)

    def test_window_and_counts(self):
        s = ct.summarize(_records())
        assert s["records"] == 11 and s["alphas"] == 8
        assert s["window"]["first"] == "2026-10-28T00:00:00"
        assert s["window"]["last"] == "2026-10-28T00:19:00"
        assert s["window"]["span_h"] == pytest.approx(0.32)

    def test_sources_sorted_by_count(self):
        assert ct.summarize(_records())["sources"] == {
            "alpha_detail_cached": 3,
            "platform_poll": 2,
            "cache:corr_cache": 1,
        }

    def test_retry_after_stats(self):
        ra = ct.summarize(_records())["retry_after"]
        assert ra == {"count": 3, "median_s": 180, "max_s": 195}

    def test_top_and_repeat_alphas(self):
        s = ct.summarize(_records(), top=3)
        assert [p["alpha"] for p in s["top_alphas"]] == ["A5", "A4", "A7"]
        assert s["top_alphas"][1]["events"] == 2
        assert s["repeat_alphas"] == [
            {"alpha": "A1", "events": 2, "kinds": ["cache_hit", "inflight_join"]},
            {"alpha": "A4", "events": 2, "kinds": ["success"]},
            {"alpha": "A6", "events": 2, "kinds": ["busy", "inflight_busy"]},
        ]

    def test_empty_is_stable(self):
        s = ct.summarize([])
        assert s["records"] == 0 and s["alphas"] == 0
        assert s["window"] == {"first": None, "last": None, "span_h": None}
        assert s["outcomes"]["value_rate"] is None
        assert s["retry_after"] == {"count": 0, "median_s": 0, "max_s": 0}
        assert s["top_alphas"] == [] and s["repeat_alphas"] == []

    def test_non_dict_records_ignored(self):
        s = ct.summarize([None, "x", {"event": ""}, _records()[0]])
        assert s["records"] == 1


# ---------------------------------------------------------------- 写入方契约
WRITERS = [
    ROOT / "world-quant-brain-mcp" / "brain_mixin_spcread.py",
    ROOT / "world-quant-brain-mcp" / "brain_mixin_correlation.py",
]


def _timing_calls(path: Path):
    """返回 ``[(event, set(keyword_names))]``：写入方 ``_corr_log_timing(...)`` 的实参面。"""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = getattr(fn, "attr", None) or getattr(fn, "id", None)
        if name != "_corr_log_timing":
            continue
        assert len(node.args) >= 3, f"{path.name}: _corr_log_timing 缺 (event, alpha, t0)"
        event = node.args[0].value if isinstance(node.args[0], ast.Constant) else "<dyn>"
        out.append((event, {kw.arg for kw in node.keywords if kw.arg}))
    return out


class TestWriterContract:
    def test_every_writer_keyword_is_declared(self):
        unknown = set()
        seen_events = set()
        for p in WRITERS:
            for event, keys in _timing_calls(p):
                seen_events.add(event)
                unknown |= keys - set(ct.FIELDS)
        assert not unknown, f"打点字段未声明进 FIELDS：{sorted(unknown)}"
        # 写入方确实被扫到了（防止 AST 口径漂移成空转）
        assert len(seen_events) >= 8, sorted(seen_events)

    def test_every_written_event_is_known(self):
        known = set(ct.OUTCOME_EVENTS) | {"same_alpha_wait_timeout"}
        bad = set()
        for p in WRITERS:
            for event, _keys in _timing_calls(p):
                if event != "<dyn>" and event not in known:
                    bad.add(event)
        assert not bad, f"新事件没进 corr_timing 的词表：{sorted(bad)}"

    def test_correlation_writer_logs_cache_hit(self):
        events = {e for e, _ in _timing_calls(WRITERS[1])}
        assert "cache_hit" in events


# ---------------------------------------------------------------- CLI（子进程）
def _run_cli(*args):
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(CLI), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(ROOT), env=env, timeout=120,
    )


class TestReportCli:
    def test_missing_log_exits_2(self, tmp_path):
        r = _run_cli("--log", str(tmp_path / "nope.log"))
        assert r.returncode == 2
        assert "日志不存在" in (r.stderr or "")

    def test_no_records_hint(self, tmp_path):
        p = tmp_path / "empty.log"
        p.write_text("nothing here\n", encoding="utf-8")
        r = _run_cli("--log", str(p))
        assert r.returncode == 0
        assert "未找到 [corr-t] 打点" in r.stdout

    def test_summary_and_json_and_events(self, tmp_path):
        log = tmp_path / "wq.log"
        log.write_text("\n".join(
            json.dumps({"event": "x", "alpha": "A"})  # 无标记的行不该被收
            for _ in range(1)
        ) + "\n" + "\n".join(
            "[INFO] [corr-t] " + json.dumps(r, ensure_ascii=False)
            for r in _records()
        ) + "\n", encoding="utf-8")
        out = tmp_path / "corr.json"
        r = _run_cli("--log", str(log), "--since", "2026-10-28T00:00:00",
                     "--json", str(out), "--events", "--top", "3")
        assert r.returncode == 0, r.stderr
        assert "打点：11 条 / 8 个 alpha" in r.stdout
        assert "▶ 结果构成" in r.stdout
        assert "拿到值 6 / 终局 10（60.0%）" in r.stdout
        assert "▶ 原始打点" in r.stdout
        payload = json.loads(out.read_text(encoding="utf-8"))
        assert payload["summary"]["records"] == 11
        assert payload["since"] == "2026-10-28T00:00:00"
        assert [p["alpha"] for p in payload["summary"]["top_alphas"]] == ["A5", "A4", "A7"]

    def test_since_filters_out_everything(self, tmp_path):
        log = tmp_path / "wq.log"
        log.write_text("[corr-t] " + json.dumps(_records()[0]) + "\n", encoding="utf-8")
        r = _run_cli("--log", str(log), "--since", "2030-01-01T00:00:00")
        assert r.returncode == 0
        assert "未找到 [corr-t] 打点" in r.stdout
