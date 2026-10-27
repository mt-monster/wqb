# -*- coding: utf-8 -*-
"""钩子自测：通过子进程跑 campaign_guard.py，断言 6 个场景的退出码。

注意：本文件含敏感字样的字面量，但**不从 Bash 命令行传入**，
而是由脚本内部构造 payload，避免钩子按命令行误杀（2026-10-26 踩过）。
"""
import json
import subprocess
import sys

PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
GUARD = os.path.join(ROOT, ".workbuddy", "hooks", "campaign_guard.py")
SECRET_NAME = "." + "env"        # 拆开拼，避免本文件被 Grep 时命中又触发拦截

SUBMIT = "mcp__wq-brain-http__workflow_submit_alpha"

CASES = [
    ("G1a 提交·样本无效", {"hook_event_name": "PreToolUse", "tool_name": SUBMIT,
                     "tool_input": {"alpha_id": "0mjLM6vG"}}, 2),
    ("G1b 提交·prod 墙", {"hook_event_name": "PreToolUse", "tool_name": SUBMIT,
                     "tool_input": {"alpha_id": "vROPXLNa"}}, 2),
    ("G1c 提交·缺 alpha_id", {"hook_event_name": "PreToolUse", "tool_name": SUBMIT,
                         "tool_input": {}}, 2),
    ("G2a Read 凭据文件", {"hook_event_name": "PreToolUse", "tool_name": "Read",
                      "tool_input": {"file_path": os.path.join("x", SECRET_NAME)}}, 2),
    ("G2b Bash 打印凭据", {"hook_event_name": "PreToolUse", "tool_name": "Bash",
                      "tool_input": {"command": "cat " + SECRET_NAME}}, 2),
    ("G2c Bash 仅提及（应放行）", {"hook_event_name": "PreToolUse", "tool_name": "Bash",
                           "tool_input": {"command": "echo 不要读 " + SECRET_NAME}}, 0),
    ("G3a 递归删 results", {"hook_event_name": "PreToolUse", "tool_name": "Bash",
                        "tool_input": {"command": "rm -rf results/"}}, 2),
    ("G3b 普通 ls（应放行）", {"hook_event_name": "PreToolUse", "tool_name": "Bash",
                         "tool_input": {"command": "ls -la results"}}, 0),
    ("G4 PostToolUse 提醒", {"hook_event_name": "PostToolUse", "tool_name": SUBMIT,
                        "tool_input": {"alpha_id": "x"}}, 0),
]

fail = 0
for name, payload, want in CASES:
    r = subprocess.run([PY, GUARD], input=json.dumps(payload),
                       capture_output=True, text=True)
    ok = r.returncode == want
    if not ok:
        fail += 1
    msg = (r.stderr or "").strip().splitlines()
    print("[{}] {}  期望 exit={} 实际={}  {}".format(
        "PASS" if ok else "FAIL", name, want, r.returncode,
        msg[0][:78] if msg else ""))

print()
print("结果：{} 通过 / {} 失败".format(len(CASES) - fail, fail))
sys.exit(1 if fail else 0)
