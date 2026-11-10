# -*- coding: utf-8 -*-
"""category_coverage_audit.py — 数据集层穷尽性闸（2026-11-06 事故后新增）。

为什么需要它（与 tools/gates/operator_coverage_audit.py 同一类错误，只差一层）
------------------------------------------------------------------------------
2026-11-06 复盘发现：此前所有「某 category 已穷尽 / 某面已封盘」的判断，分母都是
tracking/mining/field_coverage_*.json。那份缓存**只登记曾经查询过的数据集** ——
它天然漏掉「从未被查询过」的集，于是「没查过」被读成「没有」，
「模板不够」被误诊成「机制不成立」。

实取平台全表（GET /data-sets 真分页）后的差额：

    region          平台总数   当时本地认知                     category 实况
    EUR/TOPCS1600      173    field_coverage 缓存只列 7 个 OTHER   OTHER 实为 36
    USA/TOP3000        286    只测过 4 个 OTHER                    OTHER 实为 56
    GLB/MINVOL1M       138    只测过 3-4 个 OTHER                  OTHER 实为 25
    ASI/MINVOL1M       158    从未按 category 清点                 OTHER 实为 27

data/wqb.db 的 datasets 表**同样不能当分母**：它不分 universe/delay，
实测 USA 354 > 平台 286、EUR 225 > 平台 173（混入其它档位），
而 CHN 21 行 / JPN 19 行的 category 整列为空 —— 又高估又错配，且在缺口上还是空的。

⇒ 结论：**穷尽性只有一个权威分母 = 按 (region, universe, delay) 实取平台全表。**
   本工具把这条判据机械化，正如 operator_coverage_audit 把「方向穷尽」机械化。

口径（三条，缺一不可）
----------------------
1. **分母** = 平台 GET /data-sets 分页全表，且必须 complete=True
   （paginate_all(strict=True)：页数不足 count 直接抛 PaginationError，
   绝不把「没拉全」当「拉完了」）。分页不完整 ⇒ exit 2，永不输出 EXHAUSTED。
2. **分子** = 「已实测集合」，由两路并集构成：
   - DB expressions 里该 region 真有回测记录的数据集（机械证据，缺省开启）；
   - --tested / --tested-file 显式传入的「已判决」清单
     （含**已判死但没跑过回测**的集 —— 那种判决本身没有回测证据，
     本工具不替它背书，必须由调用方显式声明）。
3. **verdict** = EXHAUSTED **当且仅当** 差集为空。差集非空一律 NOT_EXHAUSTED。

## 2026-11-09 增补：分子必须有 field 级背书（`--field-audit`）

事故：分母修好了，**分子没修**。`--tested` / `--tested-file` 传入的「已判死」清单
没有任何 field 级验证，于是「数据集级 coverage=0 + 档案里写一句已判死」就能把整枝数据
静默送进分子，gate 照样吐 EXHAUSTED。GBR 实证反例：`techindi_model` 数据集级
`coverage=0`、真实字段 399 个、贡献该战役 10 席中的 2 席。

修法：声明的已测集必须过 `tools/audit_dataset_coverage.py` 的审计 JSON 校验——
`status=TESTED`（我的 alpha code 真引用该集字段）或 `status=NO_DATA`（field 级实查确实无数据）
才算**已排除**；其余一律**剥出分子**、记为 `reversible_assumptions` 并让 verdict 转 NOT_EXHAUSTED。

::

    # 先跑 field 级审计（会花几分钟：每集一次 /data-fields）
    python tools/audit_dataset_coverage.py --region GBR --universe TOP700 --delay 1 \
        --cache data/dataset_assets/GBR_coverage_audit_d1.json \
        --md reports/dataset_experience/gbr_coverage_audit_20261109.md

    # 再判穷尽（判死清单必须过审计）
    python tools/gates/category_coverage_audit.py --region GBR --universe TOP700 --delay 1 \
        --category OTHER --tested-file tracking/GBR/dead_list.txt \
        --field-audit data/dataset_assets/GBR_coverage_audit_d1.json

用法
----
::

    # ① 某 (region, universe, delay) 的全 category 家底（先看分布对不对）
    python tools/gates/category_coverage_audit.py --region EUR --universe TOPCS1600 --delay 1 --all-categories

    # ② 判「EUR 的 OTHER 已穷尽」是否成立（核心用法；差集非空即 exit 1）
    python tools/gates/category_coverage_audit.py --region EUR --universe TOPCS1600 \
        --delay 1 --category OTHER

    # ③ 落权威快照，之后离线复核（零平台请求；data/ 已 gitignore）
    python tools/gates/category_coverage_audit.py --region USA --universe TOP3000 \
        --delay 1 --all-categories --save-snapshot
    python tools/gates/category_coverage_audit.py --region USA --universe TOP3000 \
        --delay 1 --category OTHER --snapshot data/catalog/datasets_USA_TOP3000_d1.json

    # ④ 把「已判死但未回测」的集显式计入已测（判死清单由战役维护）
    python tools/gates/category_coverage_audit.py --region EUR --universe TOPCS1600 \
        --delay 1 --category OTHER --tested other455,other567,other571

退出码：0 = EXHAUSTED（差集为空，可宣称穷尽）；1 = NOT_EXHAUSTED（差集非空）；
        2 = 数据源/参数错误（平台未拉全、快照不完整、category 不存在、参数非法）。

**不要**把它当 full_coverage_gate.py 的替代：那个管「一个数据集内部字段/模板族/算子
是否扫完」，本工具管「一个 category 下的数据集是否都进过场」。两者串联的顺序是
本工具 → full_coverage_gate.py → wave_gate.py。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set

def _find_repo_root() -> Path:
    """向上探测 pyproject.toml + src/wqb 双标记（不用层数硬编码，见 AGENTS.md §8.13）。"""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").is_file() and (parent / "src" / "wqb").is_dir():
            return parent
    raise SystemExit("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


REPO_ROOT = _find_repo_root()


def _bootstrap() -> None:
    """把 src/ 与 tools/lib/ 放上 sys.path（向上探测，与所在层数解耦）。"""
    for extra in (REPO_ROOT / "src", REPO_ROOT / "tools" / "lib"):
        if extra.is_dir() and str(extra) not in sys.path:
            sys.path.insert(0, str(extra))


_bootstrap()

SNAPSHOT_DIR = REPO_ROOT / "data" / "catalog"
DEFAULT_DB = REPO_ROOT / "data" / "wqb.db"

EXIT_EXHAUSTED = 0
EXIT_NOT_EXHAUSTED = 1
EXIT_ERROR = 2


class SourceError(RuntimeError):
    """分母/分子无法确证 —— 一律 exit 2，绝不降级成「穷尽」或「未穷尽」。"""


# --------------------------------------------------------------- 平台分母

def _dataset_id(item: Dict[str, Any]) -> str:
    return str(item.get("id") or "").strip()


def _category_of(item: Dict[str, Any]) -> str:
    """平台 category 是嵌套 dict {id,name}；也见过裸字符串 / type 字段。"""
    raw = item.get("category")
    if isinstance(raw, dict):
        return str(raw.get("id") or raw.get("name") or "").strip()
    return str(raw or item.get("type") or "").strip()


def _slim(item: Dict[str, Any]) -> Dict[str, Any]:
    """只保留判据要用的字段：全表原始返回体大，快照落盘要能长期可读。"""
    return {
        "id": _dataset_id(item),
        "name": item.get("name"),
        "category": _category_of(item),
        "field_count": item.get("fieldCount"),
        "alpha_count": item.get("alphaCount"),
        "coverage": item.get("coverage"),
        "user_count": item.get("userCount"),
        "value_score": item.get("valueScore"),
    }


def fetch_platform_datasets(region: str, universe: str, delay: int, *,
                            limit: int = 50, sleep: float = 0.3,
                            api: Any = None) -> Dict[str, Any]:
    """取 (region, universe, delay) 下的平台数据集全表（真分页，fail-closed）。

    复用 tools/lib/api_client.paginate_all 的完整性契约：拉到的条数少于平台声明的
    count 即抛 PaginationError —— 这是本工具唯一权威分母。
    """
    from api_client import Api, load_creds, paginate_all  # 延迟导入：--snapshot 模式不碰网络

    if api is None:
        email, password = load_creds()
        if not email or not password:
            raise SourceError("平台凭据缺失（~/.brain_credentials / ~/.brain_mcp_config.json / MCP .env 均未取到）")
        api = Api()
        api.login(email, password)

    base = ("/data-sets?instrumentType=EQUITY&region=%s&delay=%d&universe=%s"
            % (region.upper(), int(delay), universe))
    page = paginate_all(api, base, limit=limit, sleep=sleep, strict=True)
    items = [_slim(x) for x in page["items"] if _dataset_id(x)]
    return {
        "region": region.upper(),
        "universe": universe,
        "delay": int(delay),
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "platform_count": page["platform_count"],
        "complete": bool(page["complete"]),
        "pages": page["pages"],
        "datasets": items,
    }


def load_snapshot(path) -> Dict[str, Any]:
    """读权威快照。complete 不是 True 的旧快照一律拒绝（fail-closed）。"""
    p = Path(path)
    if not p.is_file():
        raise SourceError("快照不存在: %s" % p)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise SourceError("快照读取失败 %s: %s" % (p, exc)) from exc
    if not isinstance(data, dict) or not isinstance(data.get("datasets"), list):
        raise SourceError("快照结构不识别（缺 datasets 列表）: %s" % p)
    if data.get("complete") is not True:
        raise SourceError("快照 complete=%r 不是 True：不完整的分页结果不得当作平台全表: %s"
                          % (data.get("complete"), p))
    return data


def default_snapshot_path(region: str, universe: str, delay: int) -> Path:
    return SNAPSHOT_DIR / ("datasets_%s_%s_d%d.json" % (region.upper(), universe, int(delay)))


def save_snapshot(payload: Dict[str, Any], path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


# --------------------------------------------------------------- 已测分子

def load_tested_from_db(region: str, db_path=None) -> Set[str]:
    """DB expressions 里该 region 有回测记录的数据集（机械证据，小写）。

    这是「已进过场」的最小可证集合。**不**读 datasets 表（不分 universe/delay），
    **不**读 field_coverage_*.json（只含查过的集）。
    """
    db = Path(db_path or DEFAULT_DB)
    if not db.is_file():
        raise SourceError("本地库不存在: %s（用 --no-db + --tested 走纯清单模式）" % db)
    from wqb.db_conn import connect as _connect  # 全库唯一连接工厂（禁裸 sqlite3.connect）

    try:
        conn = _connect(str(db), readonly=True)
    except Exception as exc:  # noqa: BLE001
        raise SourceError("本地库连接失败 %s: %s" % (db, exc)) from exc
    try:
        rows = conn.execute(
            "SELECT DISTINCT lower(dataset) FROM expressions "
            "WHERE upper(region)=? AND dataset IS NOT NULL AND dataset != ''",
            (region.upper(),),
        ).fetchall()
    finally:
        conn.close()
    return {str(r[0]).strip() for r in rows if r and r[0]}


def load_local_datasets(region: str, db_path=None) -> Set[str]:
    """DB datasets 表里该 region 的条目（小写）—— 只用于报告「本地多出的」。"""
    db = Path(db_path or DEFAULT_DB)
    if not db.is_file():
        return set()
    from wqb.db_conn import connect as _connect

    try:
        conn = _connect(str(db), readonly=True)
        try:
            rows = conn.execute(
                "SELECT DISTINCT lower(d.name) FROM datasets d "
                "JOIN regions r ON r.id=d.region_id WHERE upper(r.name)=?",
                (region.upper(),),
            ).fetchall()
        finally:
            conn.close()
    except Exception:  # noqa: BLE001 —— 辅助信息，取不到不影响判据
        return set()
    return {str(r[0]).strip() for r in rows if r and r[0]}


def load_tested_file(path) -> Set[str]:
    """从 JSON（list / {datasets|tested: [...]}）或纯文本（一行一个 / 逗号分隔）读清单。"""
    p = Path(path)
    if not p.is_file():
        raise SourceError("已测清单不存在: %s" % p)
    raw = p.read_text(encoding="utf-8", errors="ignore")
    names: Set[str] = set()
    text = raw.strip()
    if text.startswith("{") or text.startswith("["):
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise SourceError("已测清单 JSON 解析失败 %s: %s" % (p, exc)) from exc
        if isinstance(data, dict):
            for key in ("datasets", "tested", "judged", "ids"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break
        if isinstance(data, list):
            for x in data:
                if isinstance(x, str):
                    names.add(x.strip().lower())
                elif isinstance(x, dict):
                    for key in ("dataset", "id", "name"):
                        if isinstance(x.get(key), str):
                            names.add(x[key].strip().lower())
                            break
        return {n for n in names if n}
    for chunk in text.replace("\n", ",").split(","):
        n = chunk.strip().lower()
        if n and not n.startswith("#"):
            names.add(n)
    return names


# --------------------------------------------------------------- 判据

def category_histogram(items: Sequence[Dict[str, Any]]) -> Dict[str, int]:
    hist: Dict[str, int] = {}
    for it in items:
        cat = _category_of(it) or "(none)"
        hist[cat] = hist.get(cat, 0) + 1
    return dict(sorted(hist.items(), key=lambda kv: (-kv[1], kv[0].upper())))


def resolve_category(items: Sequence[Dict[str, Any]], wanted: Optional[str]) -> Optional[str]:
    """把调用方给的 category 归一到平台实际写法；该面 0 个数据集即报错。

    **为什么必须报错而不是返回空集**：空差集会被读成「已穷尽」——
    「这个面本来就不存在」与「这个面全测完了」在差集上无法区分。
    """
    if not wanted:
        return None
    hist = category_histogram(items)
    lookup = {k.strip().upper(): k for k in hist}
    hit = lookup.get(str(wanted).strip().upper())
    if not hit:
        raise SourceError(
            "category %r 在本 (region, universe, delay) 下 0 个数据集；已知 category: %s"
            % (wanted, ", ".join("%s(%d)" % kv for kv in hist.items())))
    return hit


def build_report(items: Sequence[Dict[str, Any]], category: Optional[str],
                 tested: Iterable[str], local=None) -> Dict[str, Any]:
    """分母 − 分子 = 未测集合；verdict 只看差集是否为空。"""
    scoped = items
    if category:
        scoped = [it for it in items
                  if (_category_of(it) or "").strip().upper() == category.strip().upper()]
    platform_ids = {_dataset_id(it) for it in scoped if _dataset_id(it)}
    # extra_local 必须对**全量**平台集比较：与 category 子集比会把「本区其它 category 的集」
    # 全部误报成「本地多出的」（2026-11-06 实测 EUR/other 面因此虚报 189 个）。
    all_platform_ids = {_dataset_id(it) for it in items if _dataset_id(it)}
    tested_l = {str(x).strip().lower() for x in tested if str(x).strip()}
    covered = {i for i in platform_ids if i.lower() in tested_l}
    untested = sorted(platform_ids - covered, key=str.lower)
    local_l = {str(x).strip().lower() for x in (local or set())}
    extra_local = sorted((local_l - {i.lower() for i in all_platform_ids}), key=str.lower)
    return {
        "category": category,
        "platform_total": len(platform_ids),
        "tested_in_scope": len(covered),
        "untested_count": len(untested),
        "untested": untested,
        "extra_local_count": len(extra_local),
        "extra_local": extra_local,
        "verdict": "EXHAUSTED" if (platform_ids and not untested) else "NOT_EXHAUSTED",
    }


# --------------------------------------------------- field 级背书（2026-11-09 根因治理）
#
# 事故复盘：本闸 2026-11-06 修好了**分母**（实取平台全表），但分子里的「已判死」清单
# 由调用方显式传入，**没有任何 field 级背书**。于是「数据集级 coverage=0 + 档案里写一句
# 已判死」就能把整枝数据静默送进分子，gate 照样吐 EXHAUSTED。GBR 2026-11-09 实测：
# techindi_model 数据集级 coverage=0，却有 399 个字段真实数据，并贡献该战役 10 席中的 2 席。
#
# ⇒ 修法：**声明的已测集（--tested / --tested-file）必须过 field 级实查**，
#    证据来自 tools/audit_dataset_coverage.py 的审计 JSON：
#      status=TESTED   -> 我的 alpha code 真引用了该集字段（平台侧回测证据）
#      status=NO_DATA  -> field 级实查确实无数据（这才是「判死」的合法证据）
#    其余（UNTESTED_BLIND / UNTESTED_COV_OK / PROBE_FAILED / UNVERIFIED / 不在审计内）一律**剥出分子**并计入
#    reversible_assumptions —— 它们是「可逆假设」，不是「已排除」。

FIELD_EVIDENCE_OK = ("TESTED", "NO_DATA")


def load_field_audit(path: str) -> Dict[str, Any]:
    """读 tools/audit_dataset_coverage.py 产出的审计 JSON（唯一 field 级证据源）。"""
    p = Path(path)
    if not p.is_file():
        raise SourceError("field 审计文件不存在: %s" % path)
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise SourceError("field 审计文件不可解析（%s: %s）" % (type(exc).__name__, exc))
    rows = {}
    for row in payload.get("rows") or []:
        ds = str(row.get("dataset") or "").strip().lower()
        if ds:
            rows[ds] = row
    if not rows:
        raise SourceError("field 审计文件 rows 为空：%s" % path)
    return {"path": path, "generated_at": payload.get("generated_at"),
            "scope": payload.get("scope") or {}, "rows": rows}


def apply_field_audit(tested: Set[str], declared: Set[str],
                      field_audit: Dict[str, Any]) -> Dict[str, Any]:
    """把声明的已测集中「无 field 级背书」的集剥出分子。DB 机械证据不动。"""
    rows = field_audit["rows"]
    stripped, kept = [], []
    for ds in sorted(declared, key=str.lower):
        row = rows.get(ds.strip().lower())
        status = (row or {}).get("status")
        if row is not None and status in FIELD_EVIDENCE_OK:
            kept.append(ds)
        else:
            stripped.append({
                "dataset": ds,
                "audit_status": status or "NOT_IN_AUDIT",
                "has_data": (row or {}).get("has_data"),
                "dataset_cov": (row or {}).get("dataset_cov"),
                "fields_seen": (row or {}).get("fields_seen"),
                "max_field_cov": (row or {}).get("max_field_cov"),
                "alpha_hits": (row or {}).get("evidence_hit_n"),
                "why": ("有真实字段数据但零回测证据" if status in ("UNTESTED_BLIND",
                                                          "UNTESTED_COV_OK")
                        else "field 级未验伪" if status == "UNVERIFIED"
                        else "探针没跑成，仍是「不知道」" if status == "PROBE_FAILED"
                        else "不在 field 审计内"),
            })
    strip_l = {s["dataset"].strip().lower() for s in stripped}
    remaining = {t for t in tested if str(t).strip().lower() not in strip_l}
    return {"tested": remaining, "kept": kept, "stripped": stripped}


# --------------------------------------------------------------- CLI

def _split_csv(value: Optional[str]) -> Set[str]:
    out: Set[str] = set()
    for chunk in (value or "").replace(";", ",").split(","):
        n = chunk.strip().lower()
        if n:
            out.add(n)
    return out


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="数据集层穷尽性闸：平台全表(分母) − 已实测集合(分子) = 未测集合",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--region", required=True, help="区域代码（EUR/USA/GLB/...）")
    ap.add_argument("--universe", help="宇宙档位；缺省取 wqb.config.default_universe(region)")
    ap.add_argument("--delay", type=int, help="数据延迟；缺省取 wqb.config.default_delay(region)")
    ap.add_argument("--category", help="只审计该 category（必须平台实有此面，否则 exit 2）")
    ap.add_argument("--all-categories", action="store_true", help="打印全 category 计数分布")
    ap.add_argument("--tested", help="显式已测清单，逗号分隔")
    ap.add_argument("--tested-file", help="已测清单文件（JSON 列表 / 一行一个 / 逗号分隔）")
    ap.add_argument("--field-audit",
                    help="tools/audit_dataset_coverage.py 的审计 JSON：--tested/--tested-file "
                         "声明的集必须在此文件里是 TESTED 或 NO_DATA，否则剥出分子")
    ap.add_argument("--no-db", action="store_true", help="不从数据库取已测集合（纯清单模式）")
    ap.add_argument("--db", help="本地库路径（缺省 data/wqb.db）")
    ap.add_argument("--snapshot", help="读已落盘的平台全表快照（零平台请求）")
    ap.add_argument("--save-snapshot", nargs="?", const="__default__",
                    help="把本次平台全表落盘（不带值 = data/catalog/datasets_<R>_<U>_d<D>.json）")
    ap.add_argument("--limit", type=int, default=50, help="分页大小（平台硬顶 50）")
    ap.add_argument("--show-extra-local", action="store_true",
                    help="展开「本地 datasets 表多出」的条目名（缺省只打印计数）")
    ap.add_argument("--json", action="store_true", help="机读输出")
    args = ap.parse_args(argv)

    # ---- 解析 region / universe / delay
    try:
        from wqb import config as wqb_config
    except Exception as exc:  # noqa: BLE001
        print("[cca] 无法导入 wqb.config: %s" % exc, file=sys.stderr)
        return EXIT_ERROR
    region = args.region.strip().upper()
    if region not in wqb_config.REGIONS:
        print("[cca] 未知区域 %r；已知 %s" % (region, sorted(wqb_config.REGIONS)), file=sys.stderr)
        return EXIT_ERROR
    universe = args.universe or wqb_config.default_universe(region)
    delay = args.delay if args.delay is not None else wqb_config.default_delay(region)

    # ---- 分母
    try:
        if args.snapshot:
            payload = load_snapshot(args.snapshot)
            if str(payload.get("region", "")).upper() != region:
                raise SourceError("快照 region=%r 与 --region %r 不一致"
                                  % (payload.get("region"), region))
            if str(payload.get("universe", "")) != str(universe):
                raise SourceError("快照 universe=%r 与 --universe %r 不一致"
                                  % (payload.get("universe"), universe))
            if int(payload.get("delay", -1)) != int(delay):
                raise SourceError("快照 delay=%r 与 --delay %r 不一致"
                                  % (payload.get("delay"), delay))
            payload["source"] = "snapshot:%s" % args.snapshot
        else:
            payload = fetch_platform_datasets(region, universe, delay, limit=args.limit)
            payload["source"] = "platform:/data-sets"
            if not payload["complete"]:
                raise SourceError("平台分页未拉全（%s/%s），拒绝据此判定穷尽"
                                  % (len(payload["datasets"]), payload["platform_count"]))
        if args.save_snapshot and args.snapshot:
            raise SourceError("--snapshot 与 --save-snapshot 不能同时用（会覆盖权威快照源）")
        if args.save_snapshot:
            target = (default_snapshot_path(region, universe, delay)
                      if args.save_snapshot == "__default__" else Path(args.save_snapshot))
            payload["saved_to"] = str(save_snapshot(payload, target))
    except SourceError as exc:
        print("[cca] %s" % exc, file=sys.stderr)
        return EXIT_ERROR
    except Exception as exc:  # noqa: BLE001 —— 网络/鉴权/分页异常一律 fail-closed
        print("[cca] 平台取数失败（%s: %s）—— 不得据此判定穷尽" % (type(exc).__name__, exc),
              file=sys.stderr)
        return EXIT_ERROR

    items: List[Dict[str, Any]] = payload["datasets"]
    if not items:
        print("[cca] 平台在 %s/%s/d%d 返回 0 个数据集 —— universe 或 delay 可能不合法，"
              "拒绝输出 verdict" % (region, universe, delay), file=sys.stderr)
        return EXIT_ERROR

    # ---- 分子
    tested: Set[str] = set()
    declared: Set[str] = set()          # 调用方显式声明的已测/已判死集（需 field 级背书）
    tested_sources: List[str] = []
    try:
        if not args.no_db:
            tested |= load_tested_from_db(region, args.db)
            tested_sources.append("db:expressions(region=%s)" % region)
        if args.tested:
            _t = _split_csv(args.tested)
            tested |= _t
            declared |= _t
            tested_sources.append("cli:--tested")
        if args.tested_file:
            _t = load_tested_file(args.tested_file)
            tested |= _t
            declared |= _t
            tested_sources.append("file:%s" % args.tested_file)
    except SourceError as exc:
        print("[cca] %s" % exc, file=sys.stderr)
        return EXIT_ERROR

    # ---- field 级背书（2026-11-09）：声明的已测集不许只靠档案/数据集级 coverage
    field_audit_meta: Dict[str, Any] = {"status": "absent"}
    stripped: List[Dict[str, Any]] = []
    if args.field_audit:
        try:
            fa = load_field_audit(args.field_audit)
        except SourceError as exc:
            print("[cca] %s" % exc, file=sys.stderr)
            return EXIT_ERROR
        applied = apply_field_audit(tested, declared, fa)
        tested = applied["tested"]
        stripped = applied["stripped"]
        field_audit_meta = {
            "status": "applied",
            "path": fa["path"],
            "generated_at": fa["generated_at"],
            "audit_scope": fa["scope"],
            "declared": len(declared),
            "backed": len(applied["kept"]),
            "stripped": len(stripped),
        }
    elif declared:
        field_audit_meta = {
            "status": "missing",
            "note": ("给了 --tested/--tested-file 但没给 --field-audit：这些声明没有 field 级"
                     "背书（2026-11-09 GBR 根因）⇒ 本次 verdict 仅供参考，不得作为穷尽证据"),
        }

    try:
        category = resolve_category(items, args.category)
    except SourceError as exc:
        print("[cca] %s" % exc, file=sys.stderr)
        return EXIT_ERROR

    local = set() if args.no_db else load_local_datasets(region, args.db)
    report = build_report(items, category, tested, local)
    report.update({
        "region": region,
        "universe": universe,
        "delay": delay,
        "source": payload.get("source"),
        "platform_count": payload.get("platform_count"),
        "fetched_at": payload.get("fetched_at"),
        "tested_sources": tested_sources,
        "tested_total": len(tested),
        "field_audit": field_audit_meta,
        "reversible_assumptions": stripped,
        "all_categories": category_histogram(items),
    })
    if not tested_sources:
        report["warning"] = ("分子为空（--no-db 且未给 --tested）⇒ 全部记为未测；"
                            "这是保守方向，不是穷尽证据")
    if payload.get("saved_to"):
        report["snapshot"] = payload["saved_to"]

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("[category_coverage_audit] %s/%s/d%d  source=%s  platform=%s (%s 页)"
              % (region, universe, delay, report["source"],
                 report["platform_count"], payload.get("pages")))
        print("  已测分子: %d 个数据集  [%s]"
              % (report["tested_total"], "; ".join(tested_sources) or "空"))
        if args.all_categories:
            print("  全 category 分布:")
            for cat, n in report["all_categories"].items():
                mark = ""
                if category and cat.strip().upper() == category.strip().upper():
                    mark = "   <<< 当前审计面"
                print("    %-24s %4d%s" % (cat, n, mark))
        print("  审计面: %s" % (category or "全 category"))
        print("  平台 %d / 已测 %d / 未测 %d"
              % (report["platform_total"], report["tested_in_scope"], report["untested_count"]))
        if report["untested"]:
            shown = report["untested"][:40]
            tail = "" if len(shown) == report["untested_count"] else \
                " …(共 %d 个，用 --json 取全量)" % report["untested_count"]
            print("  未测差集: %s%s" % (", ".join(shown), tail))
        if report["extra_local"]:
            extra_note = "（--show-extra-local 展开）"
            if args.show_extra_local:
                head = report["extra_local"][:15]
                extra_note = ": " + ", ".join(head)
                if report["extra_local_count"] > 15:
                    extra_note += " …"
            print("  本地 datasets 表比平台多 %d 个（不分 universe/delay，且混有由表达式串生成的"
                  "伪数据集行；仅提示，不参与判据）%s"
                  % (report["extra_local_count"], extra_note))
        fa_meta = report.get("field_audit") or {}
        if fa_meta.get("status") == "applied":
            print("  field 级背书: %s" % fa_meta.get("path"))
            print("    声明已测 %d / 有背书 %d / **剥出 %d**"
                  % (fa_meta.get("declared", 0), fa_meta.get("backed", 0),
                     fa_meta.get("stripped", 0)))
            for s in report.get("reversible_assumptions") or []:
                print("    ✗ %-22s %-16s fields=%s maxCov=%s hits=%s  <- %s"
                      % (s["dataset"], s["audit_status"], s["fields_seen"],
                         s["max_field_cov"], s["alpha_hits"], s["why"]))
        elif fa_meta.get("status") == "missing":
            print("  ⚠ %s" % fa_meta.get("note"))
        if report.get("warning"):
            print("  ⚠ %s" % report["warning"])
        if report.get("snapshot"):
            print("  权威快照: %s" % report["snapshot"])
        print("  VERDICT: %s" % report["verdict"])
        if report["verdict"] == "NOT_EXHAUSTED":
            print("  ⇒ 差集非空：**不得**宣称该面「已穷尽 / 已封盘」；"
                  "正确表述是「已测 %d/%d」，剩余差集须先入场。"
                  % (report["tested_in_scope"], report["platform_total"]))

    return EXIT_EXHAUSTED if report["verdict"] == "EXHAUSTED" else EXIT_NOT_EXHAUSTED


if __name__ == "__main__":
    sys.exit(main())
