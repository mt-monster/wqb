# -*- coding: utf-8 -*-
"""路径与全局常量。唯一事实源：任何模块不得自己拼路径。"""
import os

def _resolve_repo_root(start):
    """定位仓库根（含 data/ 与 world-quant-brain-mcp/）。

    2026-10-25 搬到技能目录后，`dirname×N` 不再能到仓库 ⇒ 改为：
      ① 优先 env WQB_REPO_ROOT（显式、最可靠）
      ② 否则从本文件向上找（本文件在仓库内时有效，如 tools/ 或 tools/wqb_campaign/）
    找不到就抛错，**绝不静默退回**（否则断点/结果会写到技能目录下，等于丢数据）。
    """
    env = os.environ.get("WQB_REPO_ROOT")
    if env and os.path.isdir(os.path.join(env, "data")):
        return os.path.abspath(env)
    p = os.path.abspath(start)
    for _ in range(10):
        if (os.path.isdir(os.path.join(p, "data"))
                and os.path.isdir(os.path.join(p, "world-quant-brain-mcp"))):
            return p
        p = os.path.dirname(p)
    raise RuntimeError(
        f"无法定位仓库根（起点 {start}）⇒ 请设置环境变量 WQB_REPO_ROOT=<仓库根>")


import sys



# ROOT = 仓库根（不是本文件所在目录）。搬出 tools/ 后必须靠 env 或向上搜索。
ROOT = _resolve_repo_root(os.path.dirname(os.path.abspath(__file__)))
assert os.path.isdir(os.path.join(ROOT, "data")), f"ROOT 解析错误：{ROOT}"
DB = os.path.join(ROOT, "data", "wqb.db")
VENV_PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
# wqb-scripts/ 按仓库铁律住在仓库外，路径由 $WQB_SCRIPTS 或 ~/wqb-scripts/ 推导，禁硬编码本机盘符
_WQB_SCRIPTS_DIR = os.environ.get("WQB_SCRIPTS") or os.path.join(os.path.expanduser("~"), "wqb-scripts")
WQB_TOOLS = os.path.join(_WQB_SCRIPTS_DIR, "wqb_tools.py")
# ★★★★★ 区域参数化（2026-10-25，为 IND 开波）：默认 EUR，用环境变量切换 **不改一行代码**：
#   WQB_CAMPAIGN_REGION=IND python tools/full_template_campaign.py
# ⚠ 断点/结果/digest 必须按区域隔离：EUR 沿用原名（不破坏既有进度），其它区域加 _<REGION> 后缀。
#   否则 IND 会与 EUR 共用 done 列表，直接互相覆盖。
REGION = os.environ.get("WQB_CAMPAIGN_REGION", "EUR").upper()

# 本流水线固定 D1（fields.py 以 delay=1 查平台字段；金字塔计数也取 D1 分桶）。
# lit.compute_lit 依赖它把 `pyramids[REGION]["D1"]` 取出来，勿各自硬编码。
DELAY = 1

# ★ 2026-10-25 用户定稿：**EUR 只有一条车道**，不设 lane 维度。
#   同一 (区域) 只允许一个 supervisor + 一个 campaign，由 lock.py 的 PID 锁保证；
#   区域之间仍隔离（IND/USA… 各用 _<REGION> 后缀）。
# ★★★★★ 2026-10-25 关键修复：把本模块的 REGION **写回环境变量**，
#   否则 `campaign_semantics.REGION` 会用它自己的默认值（EUR），
#   导致 all_datasets/fields 查错区域的 dataset_profile —— KOR 副本因此实际跑的是
#   同名的 EUR 数据集（结果全废）。两个模块必须共享同一个 REGION。
os.environ.setdefault("WQB_CAMPAIGN_REGION", REGION)

_SUF = "" if REGION == "EUR" else f"_{REGION}"

# 区域回测设置（来源：tracking/<R>/config/settings.json；改这里等价于改区域缺省）
# ⚠ 各区域差异极大，**不能沿用 EUR 的值**：EUR 是 TOPCS1600/SUBINDUSTRY/FAST；
#   IND 是 TOP500/STATISTICAL，且 nanHandling=OFF、maxTrade=OFF（EUR 都是 ON）。
REGION_SETTINGS = {
    "EUR": {"universe": "TOPCS1600", "neutralization": "FAST", "decay": "4",
            "truncation": "0.08", "nan_handling": "ON", "max_trade": "ON"},
    "IND": {"universe": "TOP500", "neutralization": "STATISTICAL", "decay": "4",
            "truncation": "0.08", "nan_handling": "OFF", "max_trade": "OFF"},
    # ★ USA 开波（2026-10-25）：以 tracking/USA/config/settings.json 为准
    #   （原表写的是 INDUSTRY/decay4/maxTrade ON，与 USA 区域档位不一致 ⇒ 已订正）
    "USA": {"universe": "TOP3000", "neutralization": "SUBINDUSTRY", "decay": "5",
            "truncation": "0.08", "nan_handling": "ON", "max_trade": "OFF"},
    "HKG": {"universe": "TOP500", "neutralization": "INDUSTRY", "decay": "4",
            "truncation": "0.08", "nan_handling": "ON", "max_trade": "ON"},
    "JPN": {"universe": "TOP1200", "neutralization": "INDUSTRY", "decay": "4",
            "truncation": "0.08", "nan_handling": "ON", "max_trade": "ON"},
    "ASI": {"universe": "MINVOL1M", "neutralization": "INDUSTRY", "decay": "4",
            "truncation": "0.08", "nan_handling": "ON", "max_trade": "ON"},
    "KOR": {"universe": "TOP600", "neutralization": "INDUSTRY", "decay": "4",
            "truncation": "0.08", "nan_handling": "ON", "max_trade": "ON"},
    "TWN": {"universe": "TOP500", "neutralization": "INDUSTRY", "decay": "4",
            "truncation": "0.08", "nan_handling": "ON", "max_trade": "ON"},
    "GBR": {"universe": "TOP800", "neutralization": "INDUSTRY", "decay": "4",
            "truncation": "0.08", "nan_handling": "ON", "max_trade": "ON"},
    "DEU": {"universe": "TOP800", "neutralization": "INDUSTRY", "decay": "4",
            "truncation": "0.08", "nan_handling": "ON", "max_trade": "ON"},
}.get(REGION, {"universe": "TOP500", "neutralization": "INDUSTRY", "decay": "4",
               "truncation": "0.08", "nan_handling": "ON", "max_trade": "ON"})

# ★ 状态目录是否跟着代码走？（2026-10-25 评估）
#   默认**不搬**：断点是「数据」，仓库 results/ 是既有约定（报告/审计/备份都在那），
#   而代码已搬到技能目录，二者不该混。冲突由「单实例锁 + 单目录单写者」解决，不是换目录。
#   但保留开关，需要在完全隔离时可用：
#     WQB_CAMPAIGN_STATE_DIR=<任意目录>
STATE_DIR = os.environ.get("WQB_CAMPAIGN_STATE_DIR") or os.path.join(ROOT, "results")

CKPT = os.path.join(STATE_DIR, f"full_template_campaign_checkpoint{_SUF}.json")
LOG = os.path.join(STATE_DIR, f"full_template_campaign_results{_SUF}.json")
DIGEST = os.path.join(STATE_DIR, f"campaign_digest{_SUF}.md")
PROGRESS = os.path.join(STATE_DIR, f"campaign_progress{_SUF}.json")
HEARTBEAT = os.path.join(ROOT, "cache", f"campaign_heartbeat{_SUF}.json")
# ★ 2026-10-25 补：原文件 compute_lit 里引用了 LIT_CACHE 但**全文从未定义**，
# 两处 try 都把它吞成 NameError ⇒ 缓存读/写全程是死的，每次启动都重拉全部 OS alpha。
LIT_CACHE = os.path.join(ROOT, "cache", f"{REGION.lower()}_lit_counts.json")

