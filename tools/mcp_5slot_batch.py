#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mcp_5slot_batch.py — MCP 驱动的五槽并发回测脚本

用法示例（GBR D1 TOP700，batch=8，5 槽同提）：
    python tools/mcp_5slot_batch.py \
        --alpha-json tracking/GBR/candidates/probe_model264_stageA_exprs.json \
        --settings-json tracking/GBR/config/settings.json \
        --output-csv tracking/GBR/results/mcp_5slot_model264.csv \
        --max-in-flight 5 --batch-size 8

输入格式支持：
    1) 表达式字符串列表：["rank(...)", ...]
    2) 带 settings 的对象：{"expressions": [...], "settings": {...}}
    3) 完整 alpha 列表：[{"type":"REGULAR","settings":{...},"regular":"..."}, ...]

输出 CSV 列：
    batch_idx, expression, multisim_id, child_location, status, alpha_id,
    sharpe, fitness, two_year_sharpe, margin_bp, turnover_pct,
    rn_sharpe, rn_fitness, ra_failed_count, failed_checks, error
"""

import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

DEFAULT_MCP_URL = "http://127.0.0.1:8876/mcp"
TERMINAL_STATUSES = {"COMPLETE", "ERROR", "WARNING"}


class McpClient:
    """与本地 wq-brain-http MCP 服务通信的最小 SSE 客户端。"""

    def __init__(self, url: str = DEFAULT_MCP_URL):
        self.url = url
        self.session_id: Optional[str] = None
        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        self._init_session()

    def _init_session(self) -> None:
        body = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "mcp_5slot_batch", "version": "1.0"},
            },
        }
        r = requests.post(self.url, json=body, headers=self.headers, timeout=30)
        r.raise_for_status()
        sid = r.headers.get("mcp-session-id")
        if not sid:
            raise RuntimeError("MCP initialize 未返回 mcp-session-id")
        self.session_id = sid
        self.headers["mcp-session-id"] = sid
        print(f"[MCP] session initialized: {sid[:8]}...")

    def _parse_sse(self, text: str) -> Any:
        """从 text/event-stream 响应中提取最后一个 JSON 结果。"""
        events = []
        for chunk in text.strip().split("\n\n"):
            data_lines = []
            for line in chunk.splitlines():
                if line.startswith("data:"):
                    data_lines.append(line[5:].strip())
            if data_lines:
                try:
                    events.append(json.loads("".join(data_lines)))
                except json.JSONDecodeError:
                    continue
        if not events:
            return {}
        last = events[-1]
        return last.get("result", {})

    def _extract_tool_result(self, resp: Dict[str, Any]) -> Any:
        """优先取 structuredContent.result，否则解析 content[0].text。"""
        sc = resp.get("structuredContent")
        if isinstance(sc, dict) and "result" in sc:
            return sc["result"]
        for item in resp.get("content", []):
            if item.get("type") == "text":
                try:
                    return json.loads(item["text"])
                except json.JSONDecodeError:
                    continue
        return resp

    def call(self, tool_name: str, arguments: Dict[str, Any], timeout: float = 60.0) -> Any:
        body = {
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000),
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        }
        r = requests.post(self.url, json=body, headers=self.headers, timeout=timeout)
        r.raise_for_status()
        raw = self._parse_sse(r.text)
        return self._extract_tool_result(raw)


def normalize_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """把战役 settings.json 的 camelCase 键映射为 MCP tool 的 snake_case 参数。"""
    mapping = {
        "instrumentType": "instrument_type",
        "unitHandling": "unit_handling",
        "nanHandling": "nan_handling",
        "maxTrade": "max_trade",
        "testPeriod": "test_period",
        "startDate": "_startDate",
        "endDate": "_endDate",
    }
    out: Dict[str, Any] = {}
    for k, v in settings.items():
        if k.startswith("_"):
            continue
        mk = mapping.get(k, k)
        if mk.startswith("_"):
            continue
        out[mk] = v

    defaults = {
        "instrument_type": "EQUITY",
        "region": "GBR",
        "universe": "TOP700",
        "delay": 1,
        "decay": 4,
        "neutralization": "SUBINDUSTRY",
        "truncation": 0.08,
        "pasteurization": "ON",
        "unit_handling": "VERIFY",
        "nan_handling": "ON",
        "language": "FASTEXPR",
        "visualization": False,
        "test_period": "P0Y0M",
    }
    for k, v in defaults.items():
        out.setdefault(k, v)

    # 这些字段不是 create_multi_simulation 的参数，而是运行时控制
    out.pop("wait_for_completion", None)
    out.pop("validate_fields", None)
    return out


def load_alpha_list(path: str, settings: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """统一读取输入，输出 [{type, settings, regular}, ...]。"""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    base_settings = normalize_settings(settings) if settings else normalize_settings({})

    if isinstance(data, list):
        alphas = []
        for item in data:
            if isinstance(item, str):
                alphas.append({"type": "REGULAR", "settings": dict(base_settings), "regular": item})
            elif isinstance(item, dict):
                alpha_settings = dict(base_settings)
                if "settings" in item:
                    alpha_settings.update(normalize_settings(item["settings"]))
                alphas.append({
                    "type": item.get("type", "REGULAR"),
                    "settings": alpha_settings,
                    "regular": item.get("regular") or item.get("expression") or item.get("expr"),
                    "dataset": item.get("dataset", ""),
                })
        return alphas

    if isinstance(data, dict):
        exprs = data.get("expressions") or data.get("exprs") or []
        s = dict(base_settings)
        if "settings" in data:
            s.update(normalize_settings(data["settings"]))
        ds = data.get("dataset", "")
        return [{"type": "REGULAR", "settings": s, "regular": e, "dataset": ds} for e in exprs if isinstance(e, str)]

    raise ValueError(f"不支持的输入格式: {type(data)}")


def flatten_settings_for_mcp(alpha: Dict[str, Any]) -> Dict[str, Any]:
    """把 alpha.settings 转成 create_multi_simulation 的参数。"""
    s = dict(alpha["settings"])
    # 确保类型正确
    for k in ("delay", "decay"):
        if k in s:
            s[k] = int(s[k])
    for k in ("truncation",):
        if k in s:
            s[k] = float(s[k])
    s.setdefault("wait_for_completion", False)
    s.setdefault("validate_fields", False)
    return s


def submit_batch(client: McpClient, batch: List[Dict[str, Any]], batch_idx: int) -> Dict[str, Any]:
    """提交一批（最多 8 条）alpha。"""
    settings = flatten_settings_for_mcp(batch[0])
    exprs = [a["regular"] for a in batch]
    payload = dict(settings)
    payload["alpha_expressions"] = exprs
    print(f"[submit] batch {batch_idx}: {len(exprs)} exprs, region={settings.get('region')}, universe={settings.get('universe')}")
    try:
        return client.call("create_multi_simulation", payload, timeout=120.0)
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"batch {batch_idx} submit failed: {e}") from e


def is_terminal_status(status: Optional[str]) -> bool:
    return status is not None and status.upper() in TERMINAL_STATUSES


def parse_margin_bp(margin: Any) -> Optional[float]:
    """margin 可能是 0.0005 (float) 或 5 (bp)。统一返回 bp。"""
    if margin is None:
        return None
    try:
        m = float(margin)
    except (TypeError, ValueError):
        return None
    if 0 < m < 0.1:  # 看起来是 ratio
        return round(m * 10000, 4)
    return round(m, 4)


def parse_turnover_pct(tvr: Any) -> Optional[float]:
    if tvr is None:
        return None
    try:
        v = float(tvr)
    except (TypeError, ValueError):
        return None
    if v > 1.0:  # 已经是百分比
        return round(v, 4)
    return round(v * 100, 4)


def fetch_alpha_metrics(client: McpClient, alpha_id: str) -> Dict[str, Any]:
    """调用 get_alpha_details 并提取关键指标。"""
    try:
        det = client.call("get_alpha_details", {"alpha_id": alpha_id}, timeout=30.0)
    except Exception as e:
        return {"error": f"get_alpha_details failed: {e}"}

    metrics = det.get("metrics", {}) or {}
    ra = det.get("ra", {}) or {}
    failed = ra.get("failed_ra_count")
    if failed is None:
        failed = len(ra.get("ra_failed_checks", []))

    return {
        "code": det.get("code"),
        "sharpe": metrics.get("sharpe"),
        "fitness": metrics.get("fitness"),
        "two_year_sharpe": metrics.get("two_year_sharpe"),
        "margin_bp": parse_margin_bp(metrics.get("margin")),
        "turnover_pct": parse_turnover_pct(metrics.get("turnover")),
        "rn_sharpe": metrics.get("risk_neutralized_sharpe"),
        "rn_fitness": None,  # API 不直接返回 RN fitness
        "ra_failed_count": failed,
        "failed_checks": ",".join(ra.get("ra_failed_checks", [])) if isinstance(ra.get("ra_failed_checks"), list) else "",
    }


def poll_multisim(
    client: McpClient,
    msid: str,
    expressions: List[str],
    done_children: set,
    datasets: List[str] = None,
) -> tuple:
    """
    轮询一个 multisim。
    返回 (new_rows, all_children_terminal, updated_done_children)
    """
    children_res = client.call(
        "get_multisimulation_children",
        {"multisimulation_location": msid},
        timeout=60.0,
    )
    children = children_res.get("children", []) or []
    child_count = children_res.get("child_count", len(children))

    if child_count == 0:
        # 子任务还没生成，看看 multisim 本身有没有 terminal
        ms_status = client.call("lookINTO_SimError_message", {"locations": [msid]}, timeout=60.0)
        st = ms_status.get("results", [{}])[0]
        if is_terminal_status(st.get("status")):
            # 整个 multisim 失败/完成但没有子任务
            row = {
                "expression": "",
                "dataset": datasets[0] if datasets else "",
                "multisim_id": msid,
                "child_location": msid,
                "status": st.get("status"),
                "alpha_id": None,
                "error": st.get("error") or "multisim terminal with no children",
            }
            return [row], True, done_children
        return [], False, done_children

    child_urls = [c.get("location_url") or c.get("location") for c in children]
    statuses = client.call("lookINTO_SimError_message", {"locations": child_urls}, timeout=60.0)
    status_list = statuses.get("results", [])

    new_rows = []
    all_terminal = True
    for i, st in enumerate(status_list):
        child_url = child_urls[i]
        if child_url in done_children:
            continue
        status = st.get("status")
        if not is_terminal_status(status):
            all_terminal = False
            continue

        expr = expressions[i] if i < len(expressions) else ""
        ds = datasets[i] if datasets and i < len(datasets) else ""
        row: Dict[str, Any] = {
            "expression": expr,
            "dataset": ds,
            "multisim_id": msid,
            "child_location": child_url,
            "status": status,
            "alpha_id": st.get("alpha"),
            "error": st.get("error") or "",
        }
        if st.get("alpha"):
            row.update(fetch_alpha_metrics(client, st["alpha"]))
        new_rows.append(row)
        done_children.add(child_url)

    return new_rows, all_terminal, done_children


def main() -> int:
    ap = argparse.ArgumentParser(description="MCP 五槽并发回测脚本")
    ap.add_argument("--alpha-json", required=True, help="alpha/表达式输入 JSON")
    ap.add_argument("--settings-json", help="公共 settings JSON（如 tracking/<REGION>/config/settings.json）")
    ap.add_argument("--output-csv", required=True, help="输出 CSV 路径")
    ap.add_argument("--mcp-url", default=DEFAULT_MCP_URL, help="MCP HTTP 地址")
    ap.add_argument("--batch-size", type=int, default=8, help="每个 multisim 的表达式数（≤10）")
    ap.add_argument("--max-in-flight", type=int, default=5, help="同时在飞的 multisim 数")
    ap.add_argument("--poll-interval", type=int, default=20, help="轮询间隔（秒）")
    ap.add_argument("--timeout", type=int, default=600, help="单个 multisim 最长等待（秒）")
    args = ap.parse_args()

    if args.batch_size > 10:
        print("[warn] create_multi_simulation 上限 10 条，已调整为 10")
        args.batch_size = 10

    base_settings: Optional[Dict[str, Any]] = None
    if args.settings_json:
        base_settings = json.loads(Path(args.settings_json).read_text(encoding="utf-8"))

    alphas = load_alpha_list(args.alpha_json, base_settings)
    if not alphas:
        print("[error] 没有可提交的 alpha")
        return 2

    batches = [alphas[i : i + args.batch_size] for i in range(0, len(alphas), args.batch_size)]
    print(f"[info] total alphas={len(alphas)}, batches={len(batches)}, max-in-flight={args.max_in_flight}")

    client = McpClient(args.mcp_url)

    out_path = Path(args.output_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "batch_idx", "expression", "multisim_id", "child_location", "status",
        "alpha_id", "code", "dataset", "sharpe", "fitness", "two_year_sharpe", "margin_bp",
        "turnover_pct", "rn_sharpe", "rn_fitness", "ra_failed_count",
        "failed_checks", "error",
    ]
    csv_file = out_path.open("w", newline="", encoding="utf-8")
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    in_flight: Dict[str, Dict[str, Any]] = {}
    next_batch_idx = 0
    submitted_total = 0

    try:
        while next_batch_idx < len(batches) or in_flight:
            # 补槽：尽可能把在飞数打到 max-in-flight
            while len(in_flight) < args.max_in_flight and next_batch_idx < len(batches):
                batch = batches[next_batch_idx]
                try:
                    res = submit_batch(client, batch, next_batch_idx + 1)
                    msid = res.get("multisimulation_location") or res.get("multisimulation_url")
                    if not msid:
                        print(f"[error] batch {next_batch_idx + 1} 未返回 multisim location: {res}")
                        next_batch_idx += 1
                        continue
                    in_flight[msid] = {
                        "batch_idx": next_batch_idx + 1,
                        "expressions": [a["regular"] for a in batch],
                        "datasets": [a.get("dataset", "") for a in batch],
                        "done_children": set(),
                        "submitted_at": time.time(),
                    }
                    submitted_total += len(batch)
                    print(f"[flight] {len(in_flight)}/{args.max_in_flight} in-flight, msid={msid}")
                except Exception as e:
                    print(f"[error] batch {next_batch_idx + 1} submit failed: {e}")
                    time.sleep(10)
                    continue
                next_batch_idx += 1

            # 轮询所有在飞 multisim
            finished_msids = []
            for msid, info in list(in_flight.items()):
                elapsed = time.time() - info["submitted_at"]
                if elapsed > args.timeout:
                    print(f"[warn] msid={msid} 超时 ({elapsed:.0f}s)，当作失败")
                    for expr in info["expressions"]:
                        writer.writerow({
                            "batch_idx": info["batch_idx"],
                            "expression": expr,
                            "multisim_id": msid,
                            "status": "TIMEOUT",
                            "error": "poll timeout",
                        })
                    finished_msids.append(msid)
                    continue

                try:
                    rows, all_terminal, done_set = poll_multisim(
                        client, msid, info["expressions"], info["done_children"], info.get("datasets", [])
                    )
                    info["done_children"] = done_set
                    for row in rows:
                        row.setdefault("batch_idx", info["batch_idx"])
                        writer.writerow(row)
                        csv_file.flush()
                    if all_terminal:
                        print(f"[done] batch {info['batch_idx']} msid={msid} terminal")
                        finished_msids.append(msid)
                except Exception as e:
                    print(f"[warn] poll msid={msid} error: {e}")

            for msid in finished_msids:
                in_flight.pop(msid, None)

            if next_batch_idx < len(batches) or in_flight:
                time.sleep(args.poll_interval)

    except KeyboardInterrupt:
        print("\n[warn] 被用户中断")
    finally:
        csv_file.close()

    print(f"[done] CSV={out_path}, submitted={submitted_total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
