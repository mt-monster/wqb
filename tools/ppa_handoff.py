# -*- coding: utf-8 -*-
"""ppa_handoff.py — PPA（Power Pool）人工提交通道的交接单与回写（skills 审查 SB-22）。

背景：合法 PPA（MCP 预检线不满足者，如 Sharpe∈[1.0, 1.3)）必须走**平台 web UI 人工提交**——这是 agent 无法执行的通道。
此前文档把它写成流程步骤，但没有交接单、没有回写命令：agent 走到这一步既不知道该停下，也不知道用户提交后怎么落账。

  sheet   生成交接单（Markdown）：候选 id / 区域 / 表达式 / IS 指标 / PPA 资格门（Failed PPA、PENDING）/ 算子与字段计数，
          以及**必须由人核对**的项（PPAC、当期主题窗口、web UI 提交）。agent 打印交接单后**停下**，不重复催、不换通道。
  record  用户说「已在 web UI 提交」后回写：先向平台核验 status ∈ {ACTIVE, SUBMITTED} 且 dateSubmitted 非空，
          再写 submission_ledger（submission_type=PPA）。核验不过 → 不写，exit 1。

用法（自动 re-exec 到 MCP venv；`WQ_PY` 可覆盖）：
  python tools/ppa_handoff.py sheet  --alpha-id <ID> [--ppac 0.41]
  python tools/ppa_handoff.py record --alpha-id <ID>

退出码：0 = 成功；1 = 核验不过 / 平台不可达；2 = 参数错误。
"""
import argparse
import asyncio
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器 / MCP 目录解析

#: 交接单里的 PPA 判据。来源：worldquant-submit-alpha 文档（平台 Power Pool 规则）；**本环境未向平台复核**，以平台当期规则为准。
PPA_DOC_RULES = {"sharpe_min": 1.0, "operators_max": 8, "fields_max": 3, "ppac_max": 0.5}

_CALL = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(")


def count_operators(expression):
    """表达式里的算子调用：(总次数, 去重个数)。平台按哪种口径数「≤8」文档未说，两个都给。"""
    names = _CALL.findall(expression or "")
    return len(names), len(set(names))


def count_fields(expression):
    """引用的字段标识符个数（去重）。走 wqb.expression 的标识符抽取，排除算子名。"""
    from wqb.expression.grammar import extract_identifiers
    ops = set(_CALL.findall(expression or ""))
    return len({t for t in extract_identifiers(expression or "") if t not in ops and not t.replace(".", "").isdigit()})


def build_sheet(detail, ppac=None):
    """detail = get_alpha_details 返回体 → 交接单 Markdown。纯函数，可离线单测。"""
    from wqb.config import compute_webdata_failed_counts
    is_ = detail.get("is") or {}
    checks = is_.get("checks") or []
    counts = compute_webdata_failed_counts(checks)
    settings = detail.get("settings") or {}
    expr = ((detail.get("regular") or {}).get("code")) or detail.get("code") or ""
    n_calls, n_distinct = count_operators(expr)
    n_fields = count_fields(expr)
    sharpe = is_.get("sharpe")
    R = PPA_DOC_RULES

    def mark(ok):
        return "✔" if ok else "✘"

    ppac_txt = "**待填**（本地 `brain-calculate-alpha-selfcorr-quick` 算）" if ppac is None else f"{ppac}  {mark(ppac < R['ppac_max'])}"
    lines = [
        f"# PPA 人工提交交接单：{detail.get('id') or '<ALPHA_ID>'}",
        "",
        "> agent 到这里**停下并交接**：web UI 提交是人工通道，agent 不执行、不重复催。用户提交后运行 "
        "`python tools/ppa_handoff.py record --alpha-id <ID>` 回写。",
        "",
        f"- 区域 / universe / delay：{settings.get('region')} / {settings.get('universe')} / D{settings.get('delay')}",
        f"- 平台状态：{detail.get('status')}（须为 UNSUBMITTED 才需要提交）",
        f"- 表达式：`{expr}`",
        f"- IS：Sharpe {sharpe}、Fitness {is_.get('fitness')}、Turnover {is_.get('turnover')}",
        "",
        "## 自动核对（口径见 `wqb.config.compute_webdata_failed_counts`；判据数字见 submit-alpha 文档，本环境未向平台复核）",
        f"- Failed PPA = {counts['failed_ppa']} {mark(counts['failed_ppa'] == 0)}"
        + (f"（{', '.join(counts['ppa_failed_names'])}）" if counts["ppa_failed_names"] else ""),
        f"- PPA 名单内仍 PENDING：{counts['ppa_pending_names'] or '无'}（有则待其算完再交接）",
        f"- Sharpe ≥ {R['sharpe_min']}：{sharpe} {mark(isinstance(sharpe, (int, float)) and sharpe >= R['sharpe_min'])}",
        f"- 算子 ≤ {R['operators_max']}：调用 {n_calls} 次 / 去重 {n_distinct} 个 {mark(n_distinct <= R['operators_max'])}"
        "（平台按哪种口径数未在文档写明，两个都列）",
        f"- 字段 ≤ {R['fields_max']}：{n_fields} 个 {mark(n_fields <= R['fields_max'])}",
        "",
        "## 必须由人核对（agent 无法确认）",
        f"- PPAC < {R['ppac_max']}：{ppac_txt}",
        "- 当期活跃 Power Pool **主题窗口**（平台右上角铃铛；`MATCHES_THEMES` = PASS 才受理；非活跃区域报 "
        "\"does not match any Power Pool Theme\"）：**待填**",
        "- 已准备好的属性：name（`<REGION>_<R|S>_<family>_<seq>`）、color `PURPLE`、tags `CH_PPA` + `SRC_<数据集>` + `PowerPoolSelected`、"
        "三段式 description（≥100 词）——见 `docs/alpha_properties_spec.md`",
        "",
        "## 用户不在线时",
        "候选留在提交队列（`submit_ready` 表，status 不变），**不重复催、不改走 MCP 通道**（MCP 预检会拦合法 PPA）。",
    ]
    return "\n".join(lines)


def record_submission(store, detail, region=None):
    """核验后回写 submission_ledger；返回 (ok, message)。纯逻辑，store 可用测试替身。"""
    status = detail.get("status")
    if status not in ("ACTIVE", "SUBMITTED") or not detail.get("dateSubmitted"):
        return False, (f"平台上 status={status}、dateSubmitted={detail.get('dateSubmitted')}——还没有提交成功，不回写。"
                       "请确认 web UI 提交完成后再运行（翻转可能有 2–3 分钟延迟）。")
    region = region or (detail.get("settings") or {}).get("region")
    r = store.upsert_submission(detail.get("id"), region=region, submission_type="PPA", status="ACTIVE",
                                submitted_at=detail.get("dateSubmitted"),
                                verdict={"source": "ppa_handoff", "channel": "web_ui"})
    return True, f"已回写 submission_ledger：{r}"


async def _fetch(alpha_id):
    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()
    return await brain.get_alpha_details(alpha_id)


def main(argv=None):
    ap = argparse.ArgumentParser(description="PPA 人工提交通道：交接单与回写")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("sheet", help="生成交接单（Markdown）")
    p.add_argument("--alpha-id", required=True)
    p.add_argument("--ppac", type=float, default=None, help="本地算出的 PPAC（缺省则交接单里标待填）")
    p.add_argument("--json", dest="detail_json", default=None, help="离线：用已保存的 get_alpha_details JSON，不连平台")
    p = sub.add_parser("record", help="用户已在 web UI 提交后回写 submission_ledger")
    p.add_argument("--alpha-id", required=True)
    p.add_argument("--region", default=None)
    a = ap.parse_args(argv)

    if a.cmd == "sheet" and a.detail_json:
        with open(a.detail_json, encoding="utf-8") as f:
            detail = json.load(f)
        _pyenv.bootstrap_paths()
    else:
        try:
            detail = asyncio.run(_fetch(a.alpha_id))
        except Exception as e:  # noqa: BLE001  平台不可达等
            print(f"✗ 取 alpha 详情失败：{type(e).__name__}: {e}", file=sys.stderr)
            return 1
    if a.cmd == "sheet":
        print(build_sheet(detail, a.ppac))
        return 0
    from wqb.db_conn import default_db_path
    from wqb.store import CampaignStore
    ok, msg = record_submission(CampaignStore(default_db_path()), detail, a.region)
    print(msg, file=sys.stdout if ok else sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
