# -*- coding: utf-8 -*-
"""waiver.py — 闸「放行 / 豁免」台账协议的命令行（实现见 src/wqb/waiver.py）。

子命令：
  gates [--markdown]               可豁免的闸 / 批准人 / 最长有效期 / 逃生口 / 不可豁免的红线（--markdown = INDEX 嵌入表）
  list  --region R                 该区全部 waiver（新键 waiver_* + 旧键 stop_rules_override /
                                   backlog_gate_override），标 ACTIVE / EXPIRED / INVALID / NO_EXPIRY
  new   --gate G --region R ...    校验并生成一条 waiver；默认只打印值与 MCP 调用（不写库），
                                   加 --write 才经 CampaignStore 写入本地 wqb.db
  check --gate G --region R [--wave W]   该闸此刻是否有生效 waiver（退出码 0=有 / 1=无或无效）

例：
  python tools/waiver.py gates
  python tools/waiver.py list --region GBR
  python tools/waiver.py new --gate semantic --region KOR --wave 31 --reason-code NO_INPUT_AVAILABLE \\
      --reason "该数据集无描述文，无法生成 s1_semantic" --evidence "field_semantic_classify 报 no description" \\
      --approved-by agent --days 3
  python tools/waiver.py check --gate stop_rules --region GBR

agent 写台账优先走 wqb-db MCP：把 `new` 打印的 `mcp__wqb-db__upsert_ledger_key(...)` 原样调用即可；
不要手写 JSON（字段 / 有效期 / 批准人的校验在 wqb.waiver，手写会绕过）。
运行环境：MCP venv（`WQ_PY` 或 world-quant-brain-mcp/.venv，自动 re-exec）。
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器 / MCP 目录解析


def _connect(readonly=True):
    from wqb.db_conn import connect
    return connect(readonly=readonly)


def cmd_gates(a):
    from wqb import waiver as W
    if getattr(a, "markdown", False):
        print(W.render_switch_table())      # 嵌入 Claude/skills/INDEX.md（tests/unit/test_waiver.py 比对）
        return 0
    print("可豁免的闸（新增可豁免闸须先在 wqb.waiver.GATE_POLICIES 登记）：")
    for g, p in W.GATE_POLICIES.items():
        print(f"  {g:13s} {p.title}\n"
              f"    批准人：{'/'.join(p.approvers)}；最长 {p.max_days} 天；旧键：{p.legacy_key or '—'}；"
              f"逃生口：{'、'.join(p.flags)}")
    print("\nreason_code 枚举：")
    for k, v in W.REASON_CODES.items():
        print(f"  {k:24s} {v}")
    print("\n不可豁免的红线（无论谁批准都无效）：")
    for k, v in W.RED_LINES.items():
        print(f"  {k:26s} {v}")
    print(f"\nWQB_WAIVER_MODE={W.resolve_mode()}（off / warn / enforce；缺省 warn：跳过闸而无 waiver 只告警，"
          "enforce 则拒绝）")
    return 0


def cmd_list(a):
    from wqb import waiver as W
    conn = _connect()
    try:
        items = W.load_all(conn, a.region)
    finally:
        conn.close()
    if not items:
        print(f"{a.region.upper()}：无 waiver（新键 waiver_* 与旧键都没有）")
        return 0
    bad = 0
    for w in items:
        flag = w.status + (" NO_EXPIRY" if any("NO_EXPIRY" in x for x in w.warnings) else "")
        print(f"[{flag}] {w.source_key}  {w.reason_code or 'LEGACY'}/{w.approved_by or '?'}  "
              f"至 {w.expires_at or '无到期日'}\n    {w.reason or '(无 reason)'}")
        for p in w.problems:
            print(f"    ✗ {p}")
        bad += w.status != W.ACTIVE or bool(w.warnings)
    print(f"\n共 {len(items)} 条，其中 {bad} 条需处理（过期 / 无效 / 无到期日）")
    return 0


def cmd_new(a):
    from wqb import waiver as W
    try:
        p = W.build_payload(a.gate, a.region, reason_code=a.reason_code, reason=a.reason,
                            approved_by=a.approved_by, days=a.days,
                            evidence=a.evidence, wave=a.wave)
    except W.WaiverError as e:
        print(f"✗ 校验失败：{e}", file=sys.stderr)
        return 2
    print(f"key   = {p['key']}\nvalue = {json.dumps(p['value'], ensure_ascii=False, indent=2)}")
    if a.write:
        from wqb.store import CampaignStore
        from wqb.db_conn import default_db_path
        CampaignStore(default_db_path()).upsert_ledger(p["region"], p["key"], p["value"])
        print("\n已写入本地 wqb.db（ledger_kv）。")
    else:
        print(f"\n（未写库）agent 请调用：\n  {p['mcp_call']}\n脚本环境加 --write 直接写入。")
    return 0


def cmd_check(a):
    from wqb import waiver as W
    conn = _connect()
    try:
        w = W.load(conn, a.gate, a.region, a.wave)
    finally:
        conn.close()
    if w is None:
        print(f"无 waiver：{a.gate}/{a.region.upper()}（写法见 python tools/waiver.py new --help）")
        return 1
    print(f"[{w.status}] {w.summary()}")
    for x in w.problems + w.warnings:
        print(f"  - {x}")
    return 0 if w.active else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="闸放行 / 豁免台账协议（wqb.waiver）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("gates", help="可豁免的闸 / 红线 / 枚举")
    p.add_argument("--markdown", action="store_true", help="只输出「闸与逃生口总表」（INDEX.md 嵌入块）")
    p = sub.add_parser("list", help="列出某区全部 waiver")
    p.add_argument("--region", required=True)
    p = sub.add_parser("new", help="校验并生成一条 waiver（默认不写库）")
    p.add_argument("--gate", required=True)
    p.add_argument("--region", required=True)
    p.add_argument("--wave", default=None, help="波号；缺省 = all（该区所有波）")
    p.add_argument("--reason-code", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--evidence", default=None, help="键 / id / 命令输出摘要（部分 reason_code 必填）")
    p.add_argument("--approved-by", required=True, choices=("user", "agent"))
    p.add_argument("--days", type=int, required=True, help="有效天数（受该闸上限约束）")
    p.add_argument("--write", action="store_true", help="经 CampaignStore 写入本地 wqb.db")
    p = sub.add_parser("check", help="该闸此刻是否有生效 waiver")
    p.add_argument("--gate", required=True)
    p.add_argument("--region", required=True)
    p.add_argument("--wave", default=None)
    a = ap.parse_args(argv)

    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()
    return {"gates": cmd_gates, "list": cmd_list, "new": cmd_new, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
