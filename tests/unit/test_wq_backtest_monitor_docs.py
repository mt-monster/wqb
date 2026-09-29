# -*- coding: utf-8 -*-
"""wq-backtest-monitor 文档与代码的一致性（skills 审查 BM-01…BM-18，2026-09-29）。

  · §14.2 旧命令模板四条全部与真实 CLI 不符——现在文档里出现的每个 `campaign.py` 子命令 flag 都必须能在该子命令的
    `--help` 里找到（用真实 argparse 校验）；
  · 判停阈值只引 `config.WAIT_THRESHOLDS`（且与 poller 默认值相等）；checkpoint 在 ledger `ckpt_w<wave>`，不再教读文件；
  · 不再有「四关」「v52b / tri_track / YPgAa3WR 实例」「TOP800/1500/2500/5000 非法」「方法论规则手工 +1」等过期说法；
  · 回写 SOP 只在 RA 步 9，monitor 只触发并核验；没有 OS 监控的承诺；allowed-tools 只增只读 DB 工具。
"""
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SK = ROOT / "Claude" / "skills" / "wq-backtest-monitor"
TOOLKIT = ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
SKILL = (SK / "SKILL.md").read_text(encoding="utf-8")
sys.path.insert(0, str(ROOT / "src"))


def _venv_python():
    p = ROOT / "world-quant-brain-mcp" / ".venv" / "bin" / "python"
    return str(p) if p.exists() else sys.executable


def _help(*sub):
    out = subprocess.run([_venv_python(), str(TOOLKIT / "campaign.py"), "--campaign-dir", "tracking/KOR", *sub, "--help"],
                         capture_output=True, text=True, cwd=str(ROOT))
    assert out.returncode == 0, out.stderr
    return out.stdout


def _cli_lines():
    block = SKILL.split("**无 MCP 的逃生阀**", 1)[1].split("```", 2)[1]
    return [ln for ln in block.splitlines() if "campaign.py" in ln]


@pytest.mark.parametrize("sub", [("wave", "upsert"), ("registry", "add-dead-end"), ("registry", "add-win")])
def test_every_flag_in_the_documented_commands_exists_in_the_real_cli(sub):
    lines = [ln for ln in _cli_lines() if " ".join(sub) in ln]
    assert len(lines) == 1, f"文档里应恰有一条 {' '.join(sub)} 命令"
    helptext = _help(*sub)
    for flag in re.findall(r"(--[a-z][a-z-]+)", lines[0]):
        if flag == "--campaign-dir":
            continue
        assert flag in helptext, f"{' '.join(sub)}：文档用了不存在的 flag {flag}"


def test_required_flags_of_the_real_cli_are_all_supplied():
    for sub, required in ((("wave", "upsert"), ["--wave"]),
                          (("registry", "add-dead-end"), ["--id", "--family", "--reason", "--rule"]),
                          (("registry", "add-win"), ["--id", "--what", "--key"])):
        line = [ln for ln in _cli_lines() if " ".join(sub) in ln][0]
        for flag in required:
            assert flag in line, f"{' '.join(sub)} 缺必填参数 {flag}"
        assert "--dry-run" in line                                  # 模板默认先校验、不落库


def test_no_deprecated_verdict_key_writer_is_taught():
    assert "set-verdict" not in "\n".join(_cli_lines())
    assert "`ledger set-verdict` 写的就是它，已废止" in SKILL


def test_stall_thresholds_are_from_config_and_equal_to_the_poller_defaults():
    from wqb.config import WAIT_THRESHOLDS as W
    sys.path.insert(0, str(TOOLKIT))
    from _lib.poller import DEFAULT_POLL
    assert DEFAULT_POLL["stall_minutes"] == W["sim_stall_min"] and DEFAULT_POLL["timeout_minutes"] == W["sim_timeout_min"]
    assert "WAIT_THRESHOLDS" in SKILL and "sim_stall_min" in SKILL and "sim_timeout_min" in SKILL
    for hand_copied in ("60min", "360min", "60 min 无变化"):
        assert hand_copied not in SKILL


def test_checkpoint_lives_in_the_ledger_not_a_results_file():
    assert "ckpt_w" in SKILL and "results/pipeline_" not in SKILL and "found_alphas" not in SKILL
    from wqb.store import CampaignStore  # noqa: F401  ——键名与 store 的检查点约定一致
    src = (TOOLKIT / "pipeline.py").read_text(encoding="utf-8")
    assert 'f"db:ledger_kv/{ctx.region}/ckpt_w{wave}"' in src


def test_checkpoint_batch_fields_named_in_the_eta_section_are_the_ones_pipeline_writes():
    src = (TOOLKIT / "pipeline.py").read_text(encoding="utf-8")
    for field in ('"submitted_at"', '"multisim"', '"status": "RUNNING"'):
        assert field in src
    assert "没有完成时间戳" in SKILL and "吞吐法" in SKILL          # 如实写明 ETA 只能粗估


def test_stale_claims_are_gone():
    for stale in ("四关", "v52b", "tri_track", "YPgAa3WR", "collect_verified_pids", "TOP800/1500/2500/5000",
                  "Get-CimInstance Win32_Process` 全量枚举为发现入口", "C≈7", "Token-Bucket", "唯一标准依据",
                  "times_applied +1", "最接近者"):
        assert stale not in SKILL, f"monitor 里还有过期说法：{stale}"
    assert "手工再 +1 会重复计数" in SKILL and "REGIONS[region]['universes']" in SKILL


def test_writeback_sop_lives_only_in_ra_step9_and_monitor_only_triggers_and_verifies():
    boundary = SKILL.split("## 职责边界", 1)[1].split("\n## ", 1)[0]
    assert "不是" in boundary and "step9-writeback.md" in boundary
    assert "触发并核验" in boundary
    assert "OS 表现监控与重着色" in boundary and "没有任何 skill / 工具承接" in boundary
    contract = (ROOT / "Claude" / "skills" / "CONTRACT.md").read_text(encoding="utf-8")       # 共享产物归属表（从 INDEX 拆出）
    assert "wave_results_contract.upsert_wave_result" in contract


def test_submit_status_audit_maps_to_existing_labels_and_names_the_queue_table():
    for needle in ("SUBMITTABLE", "BLOCKED", "UNVERIFIABLE", "ALREADY_SUBMITTED", "tools/submit_queue.py list",
                   "corr_checked_at", "refresh=True", "PASS_CHEAP"):
        assert needle in SKILL
    assert "不是同一物" in SKILL                                     # ledger 键 submit_ready ≠ SQL 表 submit_ready


def test_allowed_tools_grew_only_by_read_only_db_tools():
    fm = SKILL.split("---", 2)[1]
    tools = re.findall(r"(?m)^  - (\S+)$", fm)
    added = [t for t in tools if t.startswith("mcp__")]
    assert added and all(t.rsplit("__", 1)[1].startswith(("get_", "list_")) for t in added), added
    assert "mcp__wqb-db__*" not in tools and not any("upsert" in t for t in tools)


def test_scenario_cards_exist_with_the_two_mandatory_chapters_in_the_sample():
    text = (SK / "references" / "scenarios.md").read_text(encoding="utf-8")
    assert all(f"卡 BM-{i}" in text for i in (1, 2, 3))
    sample = text.split("```text", 1)[1].split("```", 1)[0]
    assert sample.count("\n") <= 20 and "R2 进度与 ETA" in sample and "R2 提交状态盘点" in sample
    assert "3 个候选：0 已提交，1 待提交" in sample
