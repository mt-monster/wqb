"""judge 的平台凭据加载：**只读进程环境变量**（skills 审查 JD-07 / T0-15，2026-09-29）。

此前的读取链有 4 个来源——`configs/config.json`（明文 username / password）→ 环境变量 → `world-quant-brain-mcp/.env`
→ `~/secrets/platform-brain.json`——其中文档直接指示读取 `.env`，与 AGENTS.md「凭据位于 `.env`：禁止读取、打印或提交」冲突。
现在与 toolkit / MCP 对齐，只认进程环境变量（云端由环境设置注入，本地由 shell 提供）：

    CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD        （首选，MCP 与 toolkit 的标准命名）
    BRAIN_USERNAME（或 BRAIN_EMAIL）/ BRAIN_PASSWORD  （旧别名，仍认）

`configs/config.json` 与 `~/secrets/platform-brain.json` 里的凭据**不再读取**（发现会在 stderr 提示迁移，不打印值）。
缺凭据时抛 RuntimeError，`judge_alpha.py` 据此降级为「表达式启发式 + verdict 上限 REVIEW」。
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BrainCredentials:
    username: str
    password: str
    brain_api_url: str = "https://api.worldquantbrain.com"
    brain_url: str = "https://platform.worldquantbrain.com"


def _read_json_file(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (FileNotFoundError, ValueError, OSError):
        return {}


def _has_plaintext_credentials(path: Path, *keys: str) -> bool:
    data = _read_json_file(path)
    return any(str(data.get(k) or "").strip() for k in keys)


def load_credentials(
    *,
    skill_dir: Path,
    config_filename: str = "configs/config.json",
    allow_env: bool = True,
    allow_home_secrets: bool = False,   # 保留形参以兼容旧调用；不再读取 ~/secrets/platform-brain.json
) -> BrainCredentials:
    brain_api_url = os.environ.get("BRAIN_API_URL", "https://api.worldquantbrain.com")
    brain_url = os.environ.get("BRAIN_URL", "https://platform.worldquantbrain.com")

    if allow_env:
        username = (os.environ.get("CREDENTIALS_EMAIL")
                    or os.environ.get("BRAIN_USERNAME")
                    or os.environ.get("BRAIN_EMAIL") or "").strip()
        password = (os.environ.get("CREDENTIALS_PASSWORD") or os.environ.get("BRAIN_PASSWORD") or "").strip()
        if username and password:
            return BrainCredentials(username=username, password=password,
                                    brain_api_url=brain_api_url, brain_url=brain_url)

    stale = []
    if _has_plaintext_credentials(skill_dir / config_filename, "username", "email", "password"):
        stale.append(config_filename)
    if _has_plaintext_credentials(Path.home() / "secrets" / "platform-brain.json", "username", "email", "password"):
        stale.append("~/secrets/platform-brain.json")
    if stale:
        print(f"[judge] 忽略 {', '.join(stale)} 里的明文凭据：只读进程环境变量 "
              "CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD（请迁移并删除这些明文，值不会被打印）", file=sys.stderr)

    raise RuntimeError(
        "Missing BRAIN credentials: set CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD in the process environment "
        "(no file-based sources; see AGENTS.md security constraint)."
    )
