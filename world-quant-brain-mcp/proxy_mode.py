#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""proxy_mode - 代理模式开关（一键切换「论坛走代理 / 直连」）。

为什么需要它（2026-11-07 实测）
================================
本机常年把 HTTP(S)_PROXY 指向 127.0.0.1:7897。代理一关，端口就没了，
但环境变量还留着，于是两条通道的命运完全不同：

  - 平台 API：`main.py` 早已把 worldquantbrain.com 加进 NO_PROXY（2026-11-06 补丁），
    实测直连 `api.worldquantbrain.com` 返回 401（可达），**不受影响**；
  - 论坛通道：`forum_functions._forum_proxies()` 会回落到 HTTPS_PROXY，
    把 Playwright / requests 指向死端口 —— 论坛工具全部打空。

切换语义（两个通道分开管，不搞一刀切）
======================================
  mode=off（直连）    平台直连（不变）；论坛清空代理变量 + 置 WQB_FORUM_BYPASS_PROXY=1 → 直连
  mode=on （走代理）  平台仍直连（实测可直连且更稳）；论坛走 proxy_url
  mode=auto（不干预） 什么都不改，保持进程继承来的环境（默认值，向后兼容）

即：**开关只控制论坛/浏览器通道 + 本进程的代理环境变量**；平台通道永远保持
NO_PROXY 直连（要关掉这条绕行用 `WQB_PLATFORM_BYPASS_PROXY=0`）。

持久化
======
配置文件缺省 `<repo>/cache/proxy_mode.json`（cache/ 已 gitignore，属本机运行期
状态，不随仓库分发）。可用 `WQB_PROXY_MODE_FILE` 覆盖。

热切换
======
`apply()` 直接改 `os.environ`。requests 每次请求都重读环境变量、Playwright 每次
launch 也重读 → **本进程内立即生效，无需重启服务**。
"""
from __future__ import annotations

import json
import os
import socket
import time
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlparse

__all__ = [
    "DEFAULT_PROXY_URL", "MODES", "config_path", "read_config", "write_config",
    "apply", "bootstrap", "snapshot", "status", "probe_direct", "probe_port",
]

#: 缺省代理地址（历史值，见 forum_functions 的注释）
DEFAULT_PROXY_URL = "http://127.0.0.1:7897"
MODES = ("on", "off", "auto")

#: 代理类环境变量全表（大小写各一份，requests/urllib 都认）
PROXY_KEYS = ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
              "http_proxy", "https_proxy", "all_proxy")

PLATFORM_URL = "https://api.worldquantbrain.com"
FORUM_URL = "https://support.worldquantbrain.com/hc/en-us"
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")


def _repo_root() -> Path:
    """向上探测仓库根（pyproject.toml + src/wqb 双标记），不用层数硬编码。"""
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "pyproject.toml").is_file() and (p / "src" / "wqb").is_dir():
            return p
    return here.parent.parent


def config_path() -> Path:
    override = (os.getenv("WQB_PROXY_MODE_FILE") or "").strip()
    if override:
        return Path(override).expanduser()
    return _repo_root() / "cache" / "proxy_mode.json"


def _first_env_url() -> str:
    # 逐个字面量读取：docs/env_registry.json 的扫描器只认 os.getenv("字面量")，
    # 用 for key in (...) 的间接写法会让登记项被判成「登记了但没人读」。
    for val in (os.getenv("WQB_PROXY_URL"), os.getenv("FORUM_SETTINGS_PROXY"),
                os.getenv("HTTPS_PROXY"), os.getenv("https_proxy"),
                os.getenv("HTTP_PROXY"), os.getenv("http_proxy")):
        val = (val or "").strip()
        if val:
            return val
    return DEFAULT_PROXY_URL


def read_config() -> Dict[str, Any]:
    """读持久化配置；文件缺失 / 损坏一律回落 mode=auto（不干预）。"""
    path = config_path()
    base = {"mode": "auto", "proxy_url": _first_env_url(),
            "updated_at": "", "source": str(path)}
    if not path.is_file():
        return base
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 — 坏文件不得拖死服务
        return base
    if not isinstance(raw, dict):
        return base
    mode = str(raw.get("mode") or "auto").strip().lower()
    if mode not in MODES:
        mode = "auto"
    url = str(raw.get("proxy_url") or "").strip() or base["proxy_url"]
    return {"mode": mode, "proxy_url": url,
            "updated_at": str(raw.get("updated_at") or ""), "source": str(path)}


def write_config(mode: str, proxy_url: Optional[str] = None) -> Dict[str, Any]:
    """写持久化配置（不改进程 env）。返回写入后的配置。"""
    mode = (mode or "").strip().lower()
    if mode not in MODES:
        raise ValueError(f"mode 必须是 {MODES} 之一，收到: {mode!r}")
    url = (proxy_url or "").strip() or read_config()["proxy_url"] or DEFAULT_PROXY_URL
    cfg = {"mode": mode, "proxy_url": url,
           "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cfg["source"] = str(path)
    return cfg


def apply(cfg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """把配置落实到当前进程的 os.environ（热生效）。"""
    cfg = cfg or read_config()
    mode = cfg["mode"]
    url = cfg["proxy_url"]
    changed: Dict[str, Optional[str]] = {}
    if mode == "on":
        for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
            os.environ[key] = url
            changed[key] = url
        if os.environ.pop("WQB_FORUM_BYPASS_PROXY", None) is not None:
            changed["WQB_FORUM_BYPASS_PROXY"] = None
    elif mode == "off":
        for key in PROXY_KEYS:
            if key in os.environ:
                os.environ.pop(key, None)
                changed[key] = None
        os.environ["WQB_FORUM_BYPASS_PROXY"] = "1"
        changed["WQB_FORUM_BYPASS_PROXY"] = "1"
    # mode=auto：不干预
    return {"mode": mode, "proxy_url": url, "changed": changed}


def bootstrap() -> Dict[str, Any]:
    """服务启动时调用一次：把上次选择的模式重新落实到进程 env。"""
    cfg = read_config()
    out = apply(cfg)
    if cfg["mode"] != "auto":
        print(f"[proxy_mode] mode={cfg['mode']} forum={'proxy ' + cfg['proxy_url'] if cfg['mode'] == 'on' else 'direct'}"
              f" (config: {cfg['source']})", flush=True)
    return out


def _env_proxy_view() -> Dict[str, str]:
    return {k: os.environ[k] for k in PROXY_KEYS if os.environ.get(k)}


def snapshot() -> Dict[str, Any]:
    """当前状态（不联网）：配置 + 进程 env 的代理视图。"""
    cfg = read_config()
    return {"config": cfg, "process_env": _env_proxy_view(),
            "forum_bypass": (os.getenv("WQB_FORUM_BYPASS_PROXY") or "") == "1",
            "platform_bypass": (os.getenv("WQB_PLATFORM_BYPASS_PROXY") or "1") != "0"}


def probe_port(proxy_url: Optional[str] = None) -> Dict[str, Any]:
    """代理端口是否真的在监听（关代理后端口消失，这是最快的判据）。"""
    url = proxy_url or read_config()["proxy_url"]
    parsed = urlparse(url if "://" in url else "http://" + url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 7897
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)
    try:
        alive = sock.connect_ex((host, port)) == 0
    except OSError:
        alive = False
    finally:
        sock.close()
    return {"url": url, "host": host, "port": port, "listening": alive}


def probe_direct(target: str = "platform", timeout: int = 15) -> Dict[str, Any]:
    """绕过一切代理变量，测目标站点是否直连可达。"""
    url = PLATFORM_URL if target == "platform" else FORUM_URL
    try:
        import requests  # 局部导入：本模块在纯配置场景下不应硬依赖
        resp = requests.get(url, proxies={"http": None, "https": None},
                            timeout=timeout, headers={"User-Agent": _UA},
                            allow_redirects=False)
        return {"target": target, "url": url, "status": resp.status_code,
                "cf_mitigated": resp.headers.get("cf-mitigated", "")}
    except Exception as exc:  # noqa: BLE001 — 探测失败要如实返回
        return {"target": target, "url": url, "error": f"{type(exc).__name__}: {exc}"}


def status(do_probe: bool = True) -> Dict[str, Any]:
    """一键体检：配置 + 进程 env + 代理端口 + 平台/论坛直连。"""
    out = snapshot()
    if do_probe:
        out["proxy_port"] = probe_port(out["config"]["proxy_url"])
        out["platform_direct"] = probe_direct("platform")
        out["forum_direct"] = probe_direct("forum")
        out["hint"] = _hint(out)
    return out


def _hint(state: Dict[str, Any]) -> str:
    mode = state["config"]["mode"]
    alive = bool((state.get("proxy_port") or {}).get("listening"))
    forum = state.get("forum_direct") or {}
    cf = str(forum.get("cf_mitigated") or "").lower()
    if mode == "on" and not alive:
        return "模式是 on，但代理端口没在监听 —— 论坛会打空，先确认代理软件已开"
    if mode == "off" and cf == "challenge":
        return "直连被 Cloudflare 挑战拦住（403 cf-mitigated: challenge）—— 论坛大概率不可用，需要开代理再切 on"
    if mode == "auto":
        return "auto 不干预进程 env；要固定行为请切 on/off"
    return "ok"


def _main(argv=None) -> int:
    """本模块自带的极简 CLI：只影响**当前进程**，不碰常驻服务。

    常驻服务的切换请用 MCP 工具 `set_proxy_mode` 或 tools/infra/proxy_mode.py。
    """
    import argparse
    ap = argparse.ArgumentParser(description="代理模式开关（仅作用于当前进程）")
    ap.add_argument("action", nargs="?", default="status",
                    choices=["status", "on", "off", "auto"])
    ap.add_argument("--url", default=None, help="代理地址（缺省沿用配置/环境变量）")
    ap.add_argument("--no-probe", action="store_true", help="status 时不联网")
    args = ap.parse_args(argv)

    if args.action == "status":
        print(json.dumps(status(do_probe=not args.no_probe), ensure_ascii=False, indent=2))
        return 0
    cfg = write_config(args.action, args.url)
    applied = apply(cfg)
    print(json.dumps({"config": cfg, "applied": applied}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
