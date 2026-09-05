#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eur_field_coverage.py
=====================
实时拉取 WQ BRAIN 平台指定区域（默认 EUR）的**数据集覆盖率**与**字段级覆盖率**，
用于判断某区域挖掘失败的根因究竟是"平台无数据"还是"选错了数据集"。

双通道设计
----------
1) MCP 通道（默认，推荐）：复用本机常驻的 world-quant-brain-mcp 服务
   （http://127.0.0.1:8876/mcp）已建立的稳定登录会话，调用 get_datasets /
   get_datafields。规避沙箱环境到 api.worldquantbrain.com 的 TLS 抖动。
2) 直连通道（--mode direct）：用 .env 中的凭据自行 Basic Auth 登录后直接打
   REST API。网络不稳时会自动指数退避重试。

关键 API 约束（实测）
--------------------
- GET /data-fields 必须同时提供 instrumentType + region + delay + universe；
  单独给 dataset.id 而不给 universe 会返回 400 Invalid query。
- universe 取值必须是该区域的合法档位，否则 500。EUR 合法档位：
  TOP2500 / TOP1200 / TOP800 / TOP400 / TOPCS1600 / ILLIQUID_MINVOL1M。
- GET /data-sets 直接返回每个数据集的 coverage / fieldCount / userCount /
  alphaCount / valueScore / pyramidMultiplier，比逐字段聚合快 2 个数量级，
  因此数据集级覆盖率优先走 get_datasets。

输出
----
- 控制台：覆盖率分布、重点数据集核查、PPA 机会排行（高覆盖 + 低拥挤）
- JSON：tracking/mining/field_coverage_<region>_d<delay>_<universe>.json

用法
----
    python tools/eur_field_coverage.py
    python tools/eur_field_coverage.py --region EUR --delay 1 --universe TOP1200
    python tools/eur_field_coverage.py --region USA --delay 1 --universe TOP3000
    python tools/eur_field_coverage.py --dataset-fields ml_factor_proj   # 下钻字段级
    python tools/eur_field_coverage.py --mode direct                     # 不走 MCP
"""

import argparse
import base64
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

BASE_URL = "https://api.worldquantbrain.com"
MCP_URI = "http://127.0.0.1:8876/mcp"

def _detect_workspace():
    """
    定位工作区（决定 .env 与输出目录的基准）。
    优先级：环境变量 WQB_WORKSPACE > 当前工作目录（若含 world-quant-brain-mcp/tracking）
            > 脚本上一级目录（脚本置于项目 tools/ 下的情形）。
    这样脚本既可放在项目 tools/，也可作为 skill 资源在任意项目中调用。
    """
    env = os.getenv("WQB_WORKSPACE")
    if env and Path(env).is_dir():
        return Path(env).resolve()
    cwd = Path.cwd()
    for base in (cwd, *cwd.parents):
        if (base / "world-quant-brain-mcp").is_dir() or (base / "tracking").is_dir():
            return base
    return Path(__file__).resolve().parent.parent


WORKSPACE = _detect_workspace()

# 各区域合法 universe（来自 get_platform_setting_options 实测）
VALID_UNIVERSES = {
    "USA": ["TOP3000", "TOP2000", "TOP1000", "TOP500", "TOP200", "ILLIQUID_MINVOL1M", "TOPSP500"],
    "EUR": ["TOP2500", "TOP1200", "TOP800", "TOP400", "TOPCS1600", "ILLIQUID_MINVOL1M"],
    "GLB": ["TOP3000", "MINVOL1M", "MINVOL10M", "TOPDIV3000"],
    "ASI": ["TOP500", "MINVOL1M", "MINVOL10M", "ILLIQUID_MINVOL1M"],
    "CHN": ["TOP2000U"],
    "HKG": ["TOP500", "TOP800"],
    "KOR": ["TOP600"],
    "IND": ["TOP500"],
    "GBR": ["TOP700"],
    "DEU": ["TOP500"],
    "MEA": ["TOP300", "TOP400"],
}

DEFAULT_UNIVERSE = {"EUR": "TOP1200", "USA": "TOP3000", "GLB": "TOP3000",
                    "CHN": "TOP2000U", "HKG": "TOP800", "KOR": "TOP600"}

# EUR 战役(2026-08-05 结论)中实际用过 / 被推荐过的数据集，需重点核查
FOCUS_DATASETS = [
    "model30", "pv20", "news21", "insiders12",           # 实际用过
    "fundamental86", "risk59", "model216", "fundamental94",  # 曾被推荐
]


# --------------------------------------------------------------------------
# MCP 通道
# --------------------------------------------------------------------------
class McpChannel:
    """通过常驻 MCP server 复用其稳定登录会话。"""

    def __init__(self, uri=MCP_URI):
        self.uri = uri
        self.sid = None

    def _open(self):
        body = json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                       "clientInfo": {"name": "eur_field_coverage", "version": "2.0"}},
        }).encode()
        req = urllib.request.Request(self.uri, data=body, headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"})
        resp = urllib.request.urlopen(req, timeout=120)
        sid = resp.headers.get("mcp-session-id")
        if not sid:
            raise RuntimeError("MCP server 未返回 mcp-session-id")
        notif = json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}).encode()
        try:
            urllib.request.urlopen(urllib.request.Request(self.uri, data=notif, headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "mcp-session-id": sid}), timeout=30)
        except Exception:
            pass
        self.sid = sid
        return sid

    def call(self, tool, arguments, timeout=1800):
        if self.sid is None:
            self._open()
        body = json.dumps({"jsonrpc": "2.0", "id": 999, "method": "tools/call",
                           "params": {"name": tool, "arguments": arguments}}).encode()

        def _do(sid):
            req = urllib.request.Request(self.uri, data=body, headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "mcp-session-id": sid})
            return urllib.request.urlopen(req, timeout=timeout).read().decode()

        try:
            content = _do(self.sid)
        except urllib.error.HTTPError:
            content = _do(self._open())          # session 过期，重开

        payload = None
        for line in content.splitlines():
            if line.startswith("data: "):
                payload = json.loads(line[6:])
        if not payload or "result" not in payload:
            raise RuntimeError(f"MCP 响应异常: {str(payload)[:300]}")
        text = "".join(c.get("text", "") for c in payload["result"].get("content", []))
        if payload["result"].get("isError"):
            raise RuntimeError(f"MCP 工具报错: {text[:300]}")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw": text}

    def get_datasets(self, region, delay, universe, instrument_type="EQUITY"):
        return self.call("get_datasets", {
            "instrument_type": instrument_type, "region": region,
            "delay": delay, "universe": universe})

    def get_datafields(self, region, delay, universe, dataset_id, instrument_type="EQUITY"):
        return self.call("get_datafields", {
            "instrument_type": instrument_type, "region": region, "delay": delay,
            "universe": universe, "dataset_id": dataset_id, "filter_sharpe": False})


# --------------------------------------------------------------------------
# 直连通道
# --------------------------------------------------------------------------
class DirectChannel:
    """自行登录直接打 REST API，用于 MCP server 未运行时的兜底。仅用标准库。"""

    def __init__(self, env_path):
        import http.cookiejar
        email, password = self._load_credentials(env_path)
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.jar))
        token = base64.b64encode(f"{email}:{password}".encode()).decode()
        req = urllib.request.Request(f"{BASE_URL}/authentication", data=b"",
                                     headers={"Authorization": f"Basic {token}"},
                                     method="POST")
        try:
            resp = self.opener.open(req, timeout=60)
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"登录失败 HTTP {e.code}: {e.read().decode()[:200]}")
        if resp.status not in (200, 201):
            raise RuntimeError(f"登录失败 HTTP {resp.status}")

    @staticmethod
    def _load_credentials(env_path):
        email = os.getenv("CREDENTIALS_EMAIL")
        password = os.getenv("CREDENTIALS_PASSWORD")
        if email and password:
            return email, password
        p = Path(env_path)
        if not p.is_absolute():
            p = WORKSPACE / p
        if not p.exists():
            raise FileNotFoundError(f"找不到凭据文件: {p}")
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            v = v.strip().strip('"').strip("'")
            if k.strip() == "CREDENTIALS_EMAIL":
                email = v
            elif k.strip() == "CREDENTIALS_PASSWORD":
                password = v
        if not (email and password):
            raise RuntimeError("凭据文件中缺少 CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD")
        return email, password

    def _get(self, path, params, max_retries=8, base_wait=8):
        import urllib.parse
        url = f"{BASE_URL}{path}?{urllib.parse.urlencode(params)}"
        for attempt in range(max_retries):
            try:
                resp = self.opener.open(urllib.request.Request(url), timeout=90)
                return json.loads(resp.read().decode())
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                    wait = base_wait * (2 ** attempt)
                    print(f"  HTTP {e.code}，{wait}s 后重试 ({attempt+1}/{max_retries})",
                          file=sys.stderr)
                    time.sleep(wait)
                    continue
                raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:200]}")
            except Exception as e:
                # 沙箱到 api.worldquantbrain.com 存在 TLS 抖动，需退避重试
                if attempt == max_retries - 1:
                    raise
                wait = base_wait * (2 ** attempt)
                print(f"  链路异常 {type(e).__name__}，{wait}s 后重试 ({attempt+1}/{max_retries})",
                      file=sys.stderr)
                time.sleep(wait)
        raise RuntimeError("重试耗尽")

    def get_datasets(self, region, delay, universe, instrument_type="EQUITY"):
        out, offset, limit = [], 0, 50
        total = None
        while True:
            d = self._get("/data-sets", {"instrumentType": instrument_type, "region": region,
                                         "delay": delay, "universe": universe,
                                         "limit": limit, "offset": offset})
            rs = d.get("results", [])
            out.extend(rs)
            total = total if total is not None else d.get("count", 0)
            if len(rs) < limit or len(out) >= total:
                break
            offset += limit
            time.sleep(1.0)
        return {"results": out, "count": len(out)}

    def get_datafields(self, region, delay, universe, dataset_id, instrument_type="EQUITY"):
        out, offset, limit = [], 0, 50
        total = None
        while True:
            params = {"instrumentType": instrument_type, "region": region, "delay": delay,
                      "universe": universe, "limit": limit, "offset": offset}
            if dataset_id:
                params["dataset.id"] = dataset_id
            d = self._get("/data-fields", params)
            rs = d.get("results", [])
            out.extend(rs)
            total = total if total is not None else d.get("count", 0)
            if len(rs) < limit or len(out) >= total:
                break
            offset += limit
            time.sleep(1.0)
        return {"results": out, "count": len(out)}


# --------------------------------------------------------------------------
# 分析
# --------------------------------------------------------------------------
def normalise(datasets):
    """直连 API 的 category/subcategory 是 dict，MCP 已扁平化为 str，此处统一为 str。"""
    for d in datasets:
        for key in ("category", "subcategory"):
            v = d.get(key)
            if isinstance(v, dict):
                d[key] = v.get("id") or v.get("name") or "?"
        for key in ("coverage", "valueScore", "pyramidMultiplier"):
            if d.get(key) is None:
                d[key] = 0.0
        for key in ("fieldCount", "userCount", "alphaCount"):
            if d.get(key) is None:
                d[key] = 0
    return datasets


def analyse(datasets):
    cov = [d.get("coverage", 0.0) for d in datasets]
    return {
        "dataset_count": len(datasets),
        "coverage_mean": round(statistics.mean(cov), 4) if cov else 0,
        "coverage_median": round(statistics.median(cov), 4) if cov else 0,
        "coverage_min": round(min(cov), 4) if cov else 0,
        "coverage_max": round(max(cov), 4) if cov else 0,
        "bucket_ge_090": sum(1 for c in cov if c >= 0.90),
        "bucket_070_090": sum(1 for c in cov if 0.70 <= c < 0.90),
        "bucket_lt_070": sum(1 for c in cov if c < 0.70),
        "total_fields": sum(d.get("fieldCount", 0) for d in datasets),
        "by_category": dict(Counter(d.get("category", "?") for d in datasets).most_common()),
    }


def rank_opportunities(datasets, min_cov=0.85, max_alphas=50, min_fields=10):
    """PPA 机会：高覆盖 + 未拥挤 + 字段量足够，按金字塔倍率/拥挤度排序。"""
    cand = [d for d in datasets
            if d.get("coverage", 0) >= min_cov
            and d.get("fieldCount", 0) >= min_fields
            and d.get("alphaCount", 10 ** 9) <= max_alphas]
    cand.sort(key=lambda d: (-d.get("pyramidMultiplier", 0),
                             d.get("alphaCount", 0),
                             -d.get("coverage", 0)))
    return cand


def slim(d):
    return {k: d.get(k) for k in
            ("id", "name", "category", "coverage", "fieldCount",
             "userCount", "alphaCount", "valueScore", "pyramidMultiplier")}


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="实时拉取 WQ BRAIN 数据集/字段覆盖率")
    ap.add_argument("--region", default="EUR")
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--universe", default=None, help="缺省按区域自动选取")
    ap.add_argument("--instrument-type", default="EQUITY")
    ap.add_argument("--mode", choices=["mcp", "direct"], default="mcp")
    ap.add_argument("--env-path", default="world-quant-brain-mcp/.env")
    ap.add_argument("--dataset-fields", default=None,
                    help="下钻某数据集的字段级覆盖率，例如 ml_factor_proj")
    ap.add_argument("--min-cov", type=float, default=0.85)
    ap.add_argument("--max-alphas", type=int, default=50)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--out-dir", default=None,
                    help="兼容：仅显式指定时写 field_coverage_*.json（默认入 DB ledger，不落共享数据湖）")
    args = ap.parse_args()

    region = args.region.upper()
    universe = args.universe or DEFAULT_UNIVERSE.get(region)
    if universe is None:
        ap.error(f"区域 {region} 未预设 universe，请显式指定 --universe")
    legal = VALID_UNIVERSES.get(region)
    if legal and universe not in legal:
        ap.error(f"universe={universe} 对 {region} 非法。合法档位: {legal}")

    if args.mode == "mcp":
        ch = McpChannel()
        print(f"[通道] MCP {MCP_URI}（复用常驻服务的稳定会话）")
    else:
        ch = DirectChannel(args.env_path)
        print(f"[通道] 直连 {BASE_URL}")

    print(f"[查询] {args.instrument_type} / {region} / delay={args.delay} / {universe}\n")

    # ---- 字段级下钻 ----
    if args.dataset_fields:
        d = ch.get_datafields(region, args.delay, universe, args.dataset_fields,
                              args.instrument_type)
        fields = d.get("results", [])
        print(f"数据集 {args.dataset_fields}: {len(fields)} 个字段\n")
        print(f"{'field id':<38}{'cov':<9}{'type':<10}{'users':<7}{'alphas'}")
        for f in sorted(fields, key=lambda x: -x.get("coverage", 0))[:args.top]:
            print(f"{str(f.get('id'))[:37]:<38}{f.get('coverage'):<9}"
                  f"{str(f.get('type'))[:9]:<10}{f.get('userCount'):<7}{f.get('alphaCount')}")
        cov = [f.get("coverage", 0) for f in fields]
        if cov:
            print(f"\n字段覆盖率: mean={statistics.mean(cov):.4f} "
                  f"median={statistics.median(cov):.4f} min={min(cov):.4f} max={max(cov):.4f}")
        out = {"query": {"region": region, "delay": args.delay, "universe": universe,
                         "dataset_id": args.dataset_fields},
               "field_count": len(fields), "fields": fields}
    else:
        # ---- 数据集级覆盖率 ----
        d = ch.get_datasets(region, args.delay, universe, args.instrument_type)
        datasets = d.get("results", [])
        if not datasets:
            print("！平台返回 0 个数据集 —— 该区域/档位确实无可用数据。")
            sys.exit(2)

        datasets = normalise(datasets)
        stats = analyse(datasets)
        print(f"=== 覆盖率总览（{stats['dataset_count']} 个数据集 / "
              f"{stats['total_fields']} 个字段）===")
        print(f"coverage  mean={stats['coverage_mean']}  median={stats['coverage_median']}  "
              f"min={stats['coverage_min']}  max={stats['coverage_max']}")
        print(f"分档      >=0.90: {stats['bucket_ge_090']}   "
              f"0.70~0.90: {stats['bucket_070_090']}   <0.70: {stats['bucket_lt_070']}")
        print(f"类别      {stats['by_category']}\n")

        m = {x["id"]: x for x in datasets}
        print("=== 重点数据集核查 ===")
        print(f"{'dataset':<18}{'状态':<8}{'cov':<9}{'fields':<8}{'users':<7}{'alphas':<8}{'pm'}")
        focus_report = {}
        for fid in FOCUS_DATASETS:
            r = m.get(fid)
            if r is None:
                print(f"{fid:<18}{'不存在':<6}  —— 该区域未提供此数据集")
                focus_report[fid] = {"available": False}
            else:
                print(f"{fid:<18}{'可用':<8}{r['coverage']:<9}{r['fieldCount']:<8}"
                      f"{r['userCount']:<7}{r['alphaCount']:<8}{r['pyramidMultiplier']}")
                focus_report[fid] = {"available": True, **slim(r)}
        print()

        cand = rank_opportunities(datasets, args.min_cov, args.max_alphas)
        print(f"=== PPA 机会排行（cov>={args.min_cov} / alphaCount<={args.max_alphas} / "
              f"fields>=10，共 {len(cand)} 个）===")
        print(f"{'id':<26}{'cov':<9}{'fields':<8}{'users':<7}{'alphas':<8}{'vs':<6}{'pm':<6}{'cat'}")
        for r in cand[:args.top]:
            print(f"{r['id']:<26}{r['coverage']:<9}{r['fieldCount']:<8}{r['userCount']:<7}"
                  f"{r['alphaCount']:<8}{r['valueScore']:<6}{r['pyramidMultiplier']:<6}{r['category']}")

        out = {
            "query": {"instrument_type": args.instrument_type, "region": region,
                      "delay": args.delay, "universe": universe},
            "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "channel": args.mode,
            "stats": stats,
            "focus_check": focus_report,
            "opportunities": [slim(r) for r in cand],
            "all_datasets": [slim(r) for r in datasets],
        }

    # 主轨入库：体检报告入 DB ledger（health_<region>_d<delay>），不落共享数据湖 tracking/mining
    try:
        roots = [os.environ.get("WQB_ROOT"), os.environ.get("WQ_PROJECT_ROOT"),
                 r"D:\coding\traeCN_project\wqb"]
        st = None
        for root in roots:
            if not root:
                continue
            src = os.path.join(root, "src")
            if os.path.isdir(os.path.join(src, "wqb")):
                if src not in sys.path:
                    sys.path.insert(0, src)
                from wqb.store import CampaignStore
                db = os.environ.get("WQB_DB_PATH") or os.path.join(root, "data", "wqb.db")
                st = CampaignStore(db)
                break
        if st is not None:
            try:
                key = f"health_{region}_d{args.delay}_{universe}"
                st.upsert_ledger(region, key, out)
                print(f"[db] 体检报告入 ledger {region}:{key}")
            finally:
                st.close()
    except Exception as e:
        print(f"[db] 入库异常（仅提示，不影响控制台输出）: {e}", file=sys.stderr)

    # 文件仅显式 --out-dir 指定时写（兼容导出视图）
    if args.out_dir:
        out_dir = Path(args.out_dir)
        if not out_dir.is_absolute():
            out_dir = WORKSPACE / out_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        suffix = f"_{args.dataset_fields}" if args.dataset_fields else ""
        out_path = out_dir / f"field_coverage_{region}_d{args.delay}_{universe}{suffix}.json"
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[保存] {out_path}")


if __name__ == "__main__":
    main()
