# -*- coding: utf-8 -*-
"""工作区根 / 战役库路径解析 + skill 目录自动定位。

从 2026-09-30 单文件 `tools/wave_gate.py` 拆出（包化，见 `__init__.py` 的拆分说明）。
本模块是包内**唯一**的路径事实源 —— 其余子模块一律 `from ._paths import ...`，
不得各自计算 `__file__` 层级。

⚠ 包化后 `__file__` 比单文件时**深了一层**：`tools/wave_gate/_paths.py`
→ 上溯 2 级是 `tools/`，上溯 3 级才是仓库根。本模块内已按新深度修正；
其他子模块若需要仓库根，必须走 `REPO_ROOT`，禁止自行拼 `os.path.dirname`。
"""
import os
import sys

# ---- skill 目录自动解析 ----
# 2026-09-27 R12：改走 tools/skill_paths（WQ_*_DIR > ~/.claude > ~/.codex > 历史 Agent 位 >
# 仓库自带 Claude/skills，与 workflow 节点同一顺序）。此前只认 WQ_*_DIR 与 qoder-cn / cursor /
# workbuddy 三个历史位，CLI 直跑与未设 env 的宿主找不到 verifier / gate.py。
_TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
from skill_paths import skill_script_dirs  # noqa: E402

_TOOLKIT_CANDIDATES = skill_script_dirs("wq-brain-campaign-toolkit", "WQ_TOOLKIT_DIR")
_VALIDATOR_CANDIDATES = skill_script_dirs("alpha-expression-verifier", "WQ_VALIDATOR_DIR")

# ---- 工作区根 / 战役库路径（2026-09-27 R19 收敛为一处）----
# 此前 7 处各写 `WQB_ROOT or WQ_PROJECT_ROOT or <作者本机盘符路径>`：仓库不在该盘符时，
# --exprs-file 候选被写进 cwd 下一个以该盘符路径命名的杂散目录（.gitignore 的 data/ 规则把它
# 吞掉，git status 看不见），gate.py 读真库找不到候选 → exit 2 "门禁未跑完"。
# 这 7 处还都不认 WQB_DB_PATH，而 toolkit gate.py（经 get_store）认。
#
# 包化后：本文件位于 tools/wave_gate/_paths.py，故仓库根 = 上溯 3 级。
_REPO_ROOT = os.path.dirname(_TOOLS_DIR)

#: 仓库根（供包内其他模块复用；禁止各自重算 __file__ 层级）。
REPO_ROOT = _REPO_ROOT


def find_script(candidates, name):
    for d in candidates:
        if d and os.path.isfile(os.path.join(d, name)):
            return os.path.join(d, name)
    raise FileNotFoundError(
        f"未找到 {name}：设 WQ_TOOLKIT_DIR/WQ_VALIDATOR_DIR 指定（已搜 "
        f"{', '.join(c for c in candidates if c)}）")


def _wqb_root(campaign_dir=None):
    """工作区根。顺序与 toolkit `_lib/wqb_store._workspace_roots` 一致：
    战役目录上溯（src/wqb 或 data/wqb.db 标记）> WQB_WORKSPACE > WQB_ROOT > WQ_PROJECT_ROOT
    > 本文件所在仓库。"""
    if campaign_dir:
        p = os.path.abspath(campaign_dir)
        for _ in range(8):
            if (os.path.isdir(os.path.join(p, "src", "wqb"))
                    or os.path.exists(os.path.join(p, "data", "wqb.db"))):
                return p
            parent = os.path.dirname(p)
            if parent == p:
                break
            p = parent
    return (os.environ.get("WQB_WORKSPACE") or os.environ.get("WQB_ROOT")
            or os.environ.get("WQ_PROJECT_ROOT") or _REPO_ROOT)


def _wqb_db_path(campaign_dir=None):
    """战役库路径：WQB_DB_PATH 优先（与 toolkit gate.py 同口径），否则 <工作区>/data/wqb.db。"""
    return os.environ.get("WQB_DB_PATH") or os.path.join(_wqb_root(campaign_dir), "data", "wqb.db")


def _campaign_store_cls(campaign_dir=None):
    """让 wqb 包可导入并返回 CampaignStore：优先工作区 src/，否则本仓库 src/。"""
    for root in (_wqb_root(campaign_dir), _REPO_ROOT):
        src = os.path.join(root, "src")
        if os.path.isdir(os.path.join(src, "wqb")):
            if src not in sys.path:
                sys.path.insert(0, src)
            break
    from wqb.store import CampaignStore
    return CampaignStore


def _settings_region(campaign_dir):
    """从战役目录的 config/settings.json 读 region（--region 缺省时的兜底）。"""
    try:
        with open(os.path.join(campaign_dir, "config", "settings.json"),
                  encoding="utf-8") as f:
            import json
            return json.load(f).get("region")
    except Exception:
        return None


def _load_region_gates():
    """加载 toolkit 的 `_lib/region_gates`（2026-09-17 P0-1：开波闸下沉到本入口）。

    wave_gate 是 S2→S3 的实际门禁入口，但原先不跑 signal_floor / stop_rules /
    backlog 三道区域闸 —— 直调它会绕过它们。优先用 WQ_TOOLKIT_DIR（已安装位），
    回落仓库自带 `Claude/skills/.../scripts` 源。
    """
    cands = []
    env = os.environ.get("WQ_TOOLKIT_DIR")
    if env:
        cands.append(env)
    cands.append(os.path.join(_REPO_ROOT, "Claude", "skills",
                              "wq-brain-campaign-toolkit", "scripts"))
    for d in cands:
        if os.path.isfile(os.path.join(d, "_lib", "region_gates.py")):
            if d not in sys.path:
                sys.path.insert(0, d)
            try:
                from _lib import region_gates as rg
                return rg
            except Exception:
                continue
    return None


def _load_template_families_for_gate():
    """加载 toolkit config/template_families.json（config 在 scripts 上一级）。"""
    import json
    for d in _TOOLKIT_CANDIDATES:
        if not d:
            continue
        for cand in (os.path.join(os.path.dirname(d), "config", "template_families.json"),
                     os.path.join(d, "config", "template_families.json")):
            if os.path.isfile(cand):
                try:
                    return json.load(open(cand, encoding="utf-8"))
                except Exception:
                    continue
    return {}
