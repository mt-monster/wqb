# -*- coding: utf-8 -*-
"""_lib/common.py - 战役工具包公共层：原子写 / 配置加载 / region 派生 / 表达式工具 / 凭证链。

所有能力脚本通过 CampaignContext 拿战役目录的一切路径与配置：
    ctx = CampaignContext("D:/.../tracking/KOR")   # 或 None = 当前工作目录

铁律：region 只从 config/settings.json 的 region 字段派生（禁止从目录名猜），
并校验与战役目录名一致（测试可用环境变量 CAMPAIGN_SKIP_DIR_CHECK=1 跳过）。
"""
import json
import os
import re
import sys

_LIB = os.path.dirname(os.path.abspath(__file__))           # scripts/_lib
SCRIPTS_DIR = os.path.dirname(_LIB)                          # scripts
TOOLKIT_ROOT = os.path.dirname(SCRIPTS_DIR)                  # skill 根
PLATFORM_CONSTRAINTS = os.path.join(TOOLKIT_ROOT, "config", "platform_constraints.json")


# ---------------- JSON 读写 ----------------

def load_json(path, encoding="utf-8-sig"):
    """读 JSON；默认 utf-8-sig 容忍 Windows 产物 BOM（无 BOM 时与 utf-8 等价）。"""
    with open(path, encoding=encoding) as f:
        return json.load(f)


def atomic_write(path, obj, encoding="utf-8", indent=1):
    """tmp + os.replace 原子写；自动建父目录。

    Windows 下目标文件可能被其他进程瞬时读占（如外部轮询脚本），
    os.replace 会抛 PermissionError；指数退避重试 5 次（最长约 7.5s）。
    """
    import time
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding=encoding) as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
    for attempt in range(5):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if attempt == 4:
                raise
            time.sleep(0.5 * (attempt + 1))


def load_platform_constraints():
    """平台级约束单一事实源（toolkit config/）。"""
    return load_json(PLATFORM_CONSTRAINTS)


# ---------------- 凭证链 ----------------

def load_credentials():
    """WQ_USERNAME/WQ_PASSWORD → BRAIN_CREDENTIALS(路径) → ~/.brain_credentials → MCP_CONFIG_FILE。"""
    u, p = os.environ.get("WQ_USERNAME"), os.environ.get("WQ_PASSWORD")
    if u and p:
        return u, p
    path = os.environ.get("BRAIN_CREDENTIALS") or os.path.expanduser("~/.brain_credentials")
    if os.path.exists(path):
        d = load_json(path)
        if isinstance(d, list) and len(d) >= 2:
            return d[0], d[1]
        if isinstance(d, dict) and d.get("email"):
            return d["email"], d.get("password")
    cfg_path = os.environ.get("MCP_CONFIG_FILE") or os.path.expanduser("~/.brain_mcp_config.json")
    cfg = load_json(cfg_path)
    c = cfg.get("credentials", {})
    return c.get("email"), c.get("password")


# ---------------- 战役上下文 ----------------

class CampaignContext:
    """战役目录解析器：路径、配置、region 派生。"""

    def __init__(self, campaign_dir=None):
        self.dir = os.path.abspath(campaign_dir or os.getcwd())
        self.settings = load_json(self.path("config", "settings.json"))
        self.thresholds = load_json(self.path("config", "thresholds.json"))
        self.region = self.settings.get("region")
        if not self.region:
            raise SystemExit(f"[ctx] {self.dir}/config/settings.json 缺 region 字段")
        self.prefix = self.region.lower()  # 文件名前缀，如 kor
        base = os.path.basename(self.dir.rstrip("\\/"))
        if (base.upper() != self.region.upper()
                and os.environ.get("CAMPAIGN_SKIP_DIR_CHECK") != "1"):
            raise SystemExit(
                f"[ctx] 战役目录名 {base} 与 settings.region={self.region} 不一致，"
                f"疑似指错目录；确认无误可设 CAMPAIGN_SKIP_DIR_CHECK=1 跳过")

    # -- 路径 --
    def path(self, *parts):
        return os.path.join(self.dir, *parts)

    def ref_path(self, name):
        return self.path("reference", name)

    def cache_path(self, *parts):
        return self.path("cache", *parts)

    @property
    def ledger_path(self):
        return self.path(f"{self.prefix}_d1_campaign_state.json")

    def catalog_path(self, dataset):
        """typed catalog（新版，优先）。"""
        return self.ref_path(f"{self.prefix}_{dataset}_fields.json")

    def whitelist_path(self, dataset):
        """legacy 白名单（兜底）。"""
        return self.ref_path(f"{self.prefix}_{dataset}_field_whitelist.json")

    def constraints_path(self):
        """区域生成约束（operator_stats/skeleton_quota/区域特有 poison）。"""
        return self.ref_path(f"{self.prefix}_generation_constraints.json")

    def ranking_path(self):
        return self.ref_path(f"{self.prefix}_dataset_ranking.json")

    def review_out_path(self, tag):
        return self.path("reviews", f"{self.prefix}_review_{tag}.json")

    # -- 配置 --
    def batch_size(self):
        return int(self.settings.get("_multi_sim_batch_size", 8))

    def thresh(self, section, default=None):
        return self.thresholds.get(section, default if default is not None else {})


def add_campaign_arg(ap):
    """给 argparse 统一挂 --campaign-dir。"""
    ap.add_argument("--campaign-dir", default=None,
                    help="战役目录路径（缺省=当前工作目录）")


def ctx_from_args(args):
    return CampaignContext(getattr(args, "campaign_dir", None))


# ---------------- 表达式工具（build_wave 与 diversity_audit 共用，禁止两处拷贝） ----------------

def norm_expr(e):
    return re.sub(r"\s+", "", e)


def expr_fields(e, known_ops=None, min_len=6):
    """表达式中的字段标识符（启发式：长度>6 且非算子）。"""
    toks = {t for t in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", e) if len(t) > min_len}
    return toks - set(known_ops) if known_ops else toks


def bucket_key(expr):
    """根调用 + 第一个函数参数，如 rank(ts_av_diff(F,10)) -> 'rank>ts_av_diff'。"""
    m = re.match(r"\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", expr)
    if not m:
        return "atom"
    root = m.group(1)
    m2 = re.search(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", expr[m.end():])
    return f"{root}>{m2.group(1)}" if m2 else f"{root}>atom"


def skeleton(expr):
    """骨架五分类（优先级与 platform_constraints.skeleton_classes 一致）。"""
    if "trade_when(" in expr or "if_else(" in expr:
        return "event_gated"
    if "group_" in expr:
        return "group"
    if "divide(" in expr:
        return "ratio"
    if "add(" in expr or "multiply(" in expr:
        return "linear_mix"
    return "single"


def read_exprs_file(path):
    """读取表达式文件（list 或 {expressions|exprs:[...]}），只保留字符串。"""
    d = load_json(path)
    ex = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
    return [e for e in ex if isinstance(e, str)]


def read_expr_items(path):
    """读取表达式条目（场景3）：保留纯字符串 与带表达式的 dict（键名
    expr|expression|regular，兼容 neutralization_sweep 产物）；丢弃无表达式键的 dict。
    pipeline per-item settings 输入专用。"""
    d = load_json(path)
    ex = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
    out = []
    for e in ex:
        if isinstance(e, str):
            out.append(e)
        elif isinstance(e, dict) and (e.get("expr") or e.get("expression") or e.get("regular")):
            out.append(e)
    return out


def read_exprs_any(path):
    """读取表达式文件（兼容更多形态）：list / {expressions|exprs:[...]} /
    wave 风格 dict-of-lists（如 kor_wave11_exprs.json 的 {wave名: [...]}）。
    只保留字符串。"""
    d = load_json(path)
    if isinstance(d, list):
        return [e for e in d if isinstance(e, str)]
    if isinstance(d, dict):
        ex = d.get("expressions") or d.get("exprs") or d.get("mixes")
        if isinstance(ex, list):
            return [e for e in ex if isinstance(e, str)]
        out = []
        for v in d.values():
            if isinstance(v, list):
                for e in v:
                    if isinstance(e, str):
                        out.append(e)
            elif isinstance(v, dict) and isinstance(v.get("exprs"), list):
                out.extend(e for e in v["exprs"] if isinstance(e, str))
        return out
    return []
