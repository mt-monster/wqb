# -*- coding: utf-8 -*-
"""harvest.py - multisim 收割器：一次调用取全批子仿真 alpha 指标并落盘。

替代逐波手写 _wNNN_harvest.py 临时脚本：children -> 子仿真 -> alpha -> is 指标
四层遍历在一个进程内完成（复用登录态 + 429 退避），按 sharpe 排序打印，
产出 <campaign>/results/{ms}_metrics.json 供判定与台账回写。

用法:
  python harvest.py --ms <multisimulation_id>                              # 仅打印（无战役目录）
  python harvest.py --campaign-dir tracking/KOR --ms <id> --tags a,b,c     # 打印+落盘
  python harvest.py --campaign-dir tracking/KOR --ms <id> --wait           # 轮询直到 COMPLETE 再收割
  python harvest.py --campaign-dir tracking/KOR --ms <id> --out out.json   # 自定义输出路径

说明:
  - multisim children 顺序与提交顺序一致，--tags 按序映射到 tag 列。
  - 未完成且未 --wait 时打印 progress 并退出码 2（便于编排脚本区分）。
  - 子仿真 FAIL/无 alpha 记入 error 行，不影响其余收割。
"""
import argparse
import datetime
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import add_campaign_arg, load_credentials
from _lib.api import Api, api_call

POLL_INTERVAL = 30


def harvest(api, msid, tags):
    """收割：返回 (rows, meta)。rows 已按 sharpe 降序。"""
    ms = json.load(api_call(api, "get", "/simulations/" + msid))
    kids = ms.get("children") or []
    rows = []
    for i, k in enumerate(kids):
        sid = k if isinstance(k, str) else (k.get("location") or k.get("id"))
        d = json.load(api_call(api, "get", "/simulations/" + sid))
        aid = d.get("alpha")
        if isinstance(aid, dict):
            aid = aid.get("id")
        tag = (tags[i] if i < len(tags) else None) or str(i)
        if not aid:
            rows.append({"index": i, "tag": tag, "status": d.get("status"),
                         "error": str(d.get("error") or "no alpha")[:120]})
            continue
        a = json.load(api_call(api, "get", "/alphas/" + aid))
        m = a.get("is") or {}
        rows.append({
            "index": i, "tag": tag, "alpha": aid,
            "sh": m.get("sharpe"), "fit": m.get("fitness"),
            "tvr": round((m.get("turnover") or 0) * 100, 1),
            "2y": m.get("two_year_sharpe"),
            "failed": a.get("failedChecks") or [],
        })
    rows.sort(key=lambda r: -(r.get("sh") if r.get("sh") is not None else -99))
    meta = {
        "ms": msid,
        "progress": ms.get("progress"),
        "status": ms.get("status"),
        "children": len(kids),
        "fetched_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    return rows, meta


def print_rows(rows):
    for r in rows:
        if "error" in r:
            print("%-22s %s ERR %s" % (r["tag"], r.get("status"), r["error"]))
        else:
            print("%-22s %-10s sh%-7s fit%-7s tvr%-6s 2y%-6s %s" % (
                r["tag"], r["alpha"], r["sh"], r["fit"], r["tvr"], r["2y"],
                ",".join(r["failed"]) or "-"))


def main():
    ap = argparse.ArgumentParser(description="multisim 收割器")
    add_campaign_arg(ap)
    ap.add_argument("--ms", required=True, help="multisimulation id 或完整 URL")
    ap.add_argument("--tags", help="逗号分隔 tag 列表，按 children 顺序映射")
    ap.add_argument("--wait", action="store_true", help="轮询直到 COMPLETE 再收割（默认不等待）")
    ap.add_argument("--timeout", type=int, default=1800, help="--wait 轮询超时秒数（默认 1800）")
    ap.add_argument("--out", help="输出 JSON 路径（缺省 <campaign>/results/{ms}_metrics.json）")
    ap.add_argument("--stdout", action="store_true", help="只打印不落盘")
    a = ap.parse_args()

    msid = a.ms.rstrip("/").split("/")[-1]
    tags = [t.strip() for t in a.tags.split(",") if t.strip()] if a.tags else []

    e, pw = load_credentials()
    api = Api()
    api.login(e, pw)

    # 初始探测（平台完成态为 COMPLETE；失败态 ERROR/FAIL）
    ms = json.load(api_call(api, "get", "/simulations/" + msid))
    status = ms.get("status")
    progress = ms.get("progress")
    if status != "COMPLETE":
        if not a.wait:
            print("progress=%s status=%s children=%d  (用 --wait 轮询到完成)" % (
                progress, status, len(ms.get("children") or [])), file=sys.stderr)
            sys.exit(2)
        deadline = time.time() + a.timeout
        while time.time() < deadline:
            time.sleep(POLL_INTERVAL)
            ms = json.load(api_call(api, "get", "/simulations/" + msid))
            status = ms.get("status")
            if status in ("COMPLETE", "ERROR", "FAIL"):
                break
            print("progress=%s ..." % ms.get("progress"), file=sys.stderr)
        if status != "COMPLETE":
            print("timeout/failed: status=%s" % status, file=sys.stderr)
            sys.exit(3)

    rows, meta = harvest(api, msid, tags)
    print("progress=%s status=%s children=%d" % (
        meta["progress"], meta["status"], meta["children"]), file=sys.stderr)
    print_rows(rows)

    payload = {"meta": meta, "rows": rows}
    # 主轨入库：harvest 结果入 ledger（平台 alpha id 无本地 code，不走 backtest_rows 表达式关联）
    if a.campaign_dir:
        try:
            from _lib.wqb_store import get_store
            from _lib.common import CampaignContext
            cm = CampaignContext(os.path.abspath(a.campaign_dir))
            st = get_store(cm)
            try:
                st.upsert_ledger(cm.region, f"harvest_{msid}", payload)
                print("[db] harvest -> ledger harvest_%s (%d rows)" % (msid, len(rows)), file=sys.stderr)
            finally:
                st.close()
        except Exception as e:
            print(f"[db] 入库异常: {e}", file=sys.stderr)

    # 文件仅显式 --out 或未 --stdout 时写导出视图
    out_path = a.out
    if not out_path and not a.stdout and a.campaign_dir:
        cdir = os.path.abspath(a.campaign_dir)
        out_path = os.path.join(cdir, "results", "%s_metrics.json" % msid)
    if out_path:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)
        print("metrics -> %s (%d rows)" % (out_path, len(rows)), file=sys.stderr)


if __name__ == "__main__":
    main()