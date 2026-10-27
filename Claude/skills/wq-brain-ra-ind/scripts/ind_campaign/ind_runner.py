#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ind_runner.py — IND 全量流水线看门狗（自动重启 + 停滞检测）。

2026-10-25：从 EUR 侧复制到 IND skill 自带一份，region 硬钉为 IND。
此前 IND 借用 EUR skill 的 eur_runner.py（靠 WQB_CAMPAIGN_REGION=IND），代码归属
与运行区域不一致；现在 IND 自带，断点/结果/digest/锁仍按 _IND 隔离，可与 EUR 并行。

为什么需要它（2026-10-24 三次同类事故）
--------------------------------------
`tools/full_template_campaign.py` 依赖的 HTTP 链路里存在**无超时的阻塞调用**，
表现为「日志静止 + CPU 0 增量 + TCP 连接不变」，但 dispatcher/harvester 都不报错：

  1. 10-24 14:08 停机：日志仅 795B，停在鉴权；
  2. 10-24 21:59→22:35：派发 57 条后 36 分钟零输出（harvest 侧）；
  3. 10-24 23:02→23:35：`multi_source_model` 派发 37 条后 33 分钟零输出，且 `sims` 里第 7 批为 null。

已做的局部修补：`harvest_until_done` 加 900s 墙钟壳（有 `[harvest-timeout]` 日志）。
但**不能覆盖全部阻塞点**（dispatch 的 subprocess、平台字段拉取、stage2 电池等），
所以正确做法是**外部看门狗**：检测停滞 → 杀掉 → 重启续跑。
续跑是安全的：checkpoint 里 `sims` 记着已派发的 multisim，重启会 `[resume] 复用已派发 N 批`，
不会重复派发；只有当前集的收割重做。

判定「停滞」的口径
------------------
只认 **日志文件 mtime**。流水线每个阶段都会打印（派发/收割重试/矩阵覆盖/设置轴），
所以「日志 30 分钟没长一个字节」必然是卡死，不是慢——已用 CPU 0 增量交叉验证过。

用法
----
  python tools/campaign_supervisor.py                 # 前台跑（建议 nohup / 后台任务）
  python tools/campaign_supervisor.py --stall-sec 1800 --max-restarts 200
  python tools/campaign_supervisor.py --once          # 只检查一次，不拉起
"""
import argparse
import json
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


import subprocess
import sys
import time
from datetime import datetime

# ★ 必须在 import wqb_campaign 之前钉住区域：config.py 缺省 EUR 并会写回环境变量，
#   漏设会让 IND 跑 EUR 的断点/数据集（KOR 副本踩过此坑）。锁路径也按 REGION 隔离。
os.environ["WQB_CAMPAIGN_REGION"] = "IND"

from wqb_campaign.lock import InstanceLock, AlreadyRunning

ROOT = _resolve_repo_root(os.path.dirname(os.path.abspath(__file__)))
VENV_PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
# 入口取**同目录**的副本（搬出 tools/ 后不能再指向 tools/，否则又被别的会话改动）
# 入口名不含 campaign，避开按 `*campaign*` 的模糊进程清理
CAMPAIGN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ind_main.py")

# 2026-10-25 区域化：CKPT/RESULTS/DIGEST/TOTAL/锁 全部按区域隔离。
# IND 硬钉，不再从外部 env 读取——区域归属由文件所在 skill 决定，避免多区域串用。
REGION = "IND"
# IND 只有一条车道（2026-10-25 用户定稿）：同区域靠 PID 锁保证单实例
_SUF = f"_{REGION}"
# 状态目录与 wqb_campaign/config.py 同一口径（否则看门狗读错断点，判断「是否完成」全错）
STATE_DIR = os.environ.get("WQB_CAMPAIGN_STATE_DIR") or os.path.join(ROOT, "results")
CKPT = os.path.join(STATE_DIR, f"full_template_campaign_checkpoint{_SUF}.json")
RESULTS = os.path.join(STATE_DIR, f"full_template_campaign_results{_SUF}.json")
DIGEST = os.path.join(STATE_DIR, f"campaign_digest{_SUF}.md")
LOGDIR = os.path.join(ROOT, "logs")
# 看门狗日志按车道分开，避免多车道交错（原先是共用一个文件）
SUPLOG = os.path.join(LOGDIR, f"campaign_supervisor{_SUF}.log")


def _total_datasets():
    """区域目标池大小（dataset_profile 中 n_fields>=3 的集数）。"""
    try:
        import sqlite3
        con = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db"))
        n = con.execute("SELECT count(*) FROM dataset_profile WHERE region=? AND n_fields>=3",
                        (REGION,)).fetchone()[0]
        con.close()
        return int(n) or 169
    except Exception:
        return 169


TOTAL = _total_datasets()

#: 这些判定本来就不跑仿真（覆盖率/字段数不够），没有 alpha 属正常，不计入「空转」。
ZERO_SKIP = {"SKIPPED_LOW_COV", "SKIPPED_TOO_FEW_FIELDS"}


def results_map():
    try:
        return json.load(open(RESULTS, encoding="utf-8")).get("results") or {}
    except Exception:
        return {}


def zero_alpha_streak(done, results):
    """从 done 尾部往前数：连续多少个「非 SKIP 判定 且 n_alphas==0」的集。

    2026-10-25 事故：`ts_backfill` 被误拉黑后，`filter_bad` 把全部表达式丢掉，
    每个集都 `n_alphas=0` 却仍判 NO_DATA 继续往前跑 —— 10 分钟"跑完"92 个集、
    一直到 169 才被发现。本函数就是那条告警的判据：连续 N 个集一条 alpha 都没产出，
    说明**管道坏了**（黑名单/派发/收割），不是**信号差**，必须停下来而不是继续空转。

    SKIP 判定被跳过（既不累积也不打断），因为它们不消耗仿真、本来就没有 alpha。
    """
    streak = 0
    for ds in reversed(list(done or [])):
        v = results.get(ds) or {}
        if v.get("verdict") in ZERO_SKIP:
            continue
        if (v.get("n_alphas") or 0) == 0:
            streak += 1
        else:
            break
    return streak


def now():
    return datetime.now().strftime("%m-%d %H:%M:%S")


def log(msg):
    line = f"[{now()}] {msg}"
    print(line, flush=True)
    os.makedirs(LOGDIR, exist_ok=True)
    with open(SUPLOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def done_count():
    try:
        ck = json.load(open(CKPT, encoding="utf-8"))
        return len(ck.get("done") or [])
    except Exception:
        return -1


def last_verdict():
    try:
        lines = [l for l in open(DIGEST, encoding="utf-8") if l.startswith("- ")]
        return lines[-1].strip() if lines else "(empty)"
    except Exception:
        return "(unreadable)"


def run_campaign(logpath, max_inflight=2, extra=None):
    """起一个流水线子进程，stdout/stderr 追加到 logpath。"""
    fh = open(logpath, "a", encoding="utf-8")
    fh.write(f"\n\n===== supervisor launch @ {now()} =====\n")
    fh.flush()
    p = subprocess.Popen(
        [VENV_PY, "-u", CAMPAIGN, "--max-inflight", str(max_inflight)] + list(extra or []),
        cwd=ROOT, stdout=fh, stderr=subprocess.STDOUT,
        creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
    )
    return p, fh


def kill_tree(p):
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"],
                           capture_output=True)
        else:
            p.kill()
    except Exception as e:
        log(f"kill 失败 {p.pid}: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stall-sec", type=int, default=1800,
                    help="日志静止超过该秒数判为卡死并重启（默认 1800=30min）")
    ap.add_argument("--max-restarts", type=int, default=200)
    ap.add_argument("--check-sec", type=int, default=60)
    ap.add_argument("--max-inflight", type=int, default=2,
                    help="campaign 在飞仿真上限（IND 用户定稿：并发 2）")
    ap.add_argument("--zero-alpha-stop", type=int, default=3,
                    help="连续 N 个非 SKIP 集 n_alphas=0 即熔断退出（默认 3；0=关闭）")
    ap.add_argument("--once", action="store_true")
    # 2026-10-25：透传到子进程的 campaign 参数（此前托管器只传 --max-inflight，
    # 导致 --datasets / --min-cov / --require-ten-years 无法生效）
    ap.add_argument("--datasets", default=None, help="只跑指定集（逗号分隔）")
    ap.add_argument("--only-cats", default=None,
                    help="只跑这些类别（逗号分隔，硬过滤）；用于「优先点未亮的塔」，"
                         "如 OTHER,RISK,FUNDAMENTAL,NEWS,MACRO,IMBALANCE")
    ap.add_argument("--min-cov", type=float, default=None, help="全局覆盖率门槛（覆盖 0.6 字面量）")
    ap.add_argument("--require-ten-years", action="store_true",
                    help="候选必须 10 年都有持仓数据（year_profile.n_years>=10）")
    ap.add_argument("--keep-fields", default=None,
                    help="点名纳入的字段（逗号分隔）：跳过平台字段清单与覆盖率闸，"
                         "并优先占用字段预算（定向复挖用）")
    args = ap.parse_args()

    # ---- 完成判据 ----
    # ⚠ done_count() 是**全局**已完成数（含范围外的集）。若直接把「范围集数」当 TOTAL，
    #   全局 done 会立刻 >= 它 ⇒ 启动即误判"全部完成"退出（限定 --datasets 时同理）。
    #   正确口径：TOTAL = 当前全局已完成 + 范围内还没做的。
    global TOTAL
    # REGION 已在模块级硬钉为 IND（并写入环境变量），此处不再重新读取。
    if args.datasets or args.only_cats:
        _done = set()
        try:
            _done = set(json.load(open(CKPT, encoding="utf-8")).get("done") or [])
        except Exception:
            pass
        _scope = set()
        try:
            import sqlite3
            _con = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db"))
            if args.datasets:
                _want = {x.strip() for x in args.datasets.split(",") if x.strip()}
                _rows = _con.execute(
                    "SELECT dataset FROM dataset_profile WHERE region=?", (REGION,)).fetchall()
                _scope = {r[0] for r in _rows} & _want
            else:
                _cats = [c.strip().upper() for c in args.only_cats.split(",") if c.strip()]
                _rows = _con.execute(
                    "SELECT dataset FROM dataset_profile WHERE region=? AND n_fields>=3 "
                    "AND UPPER(category) IN (%s)" % ",".join("?" * len(_cats)),
                    [REGION] + _cats).fetchall()
                _scope = {r[0] for r in _rows}
            _con.close()
        except Exception as e:
            log(f"范围统计失败 {type(e).__name__}: {e}（TOTAL 回落 {TOTAL}）")
        if _scope:
            TOTAL = len(_done) + len(_scope - _done)
            log(f"范围 {len(_scope)} 个集（已完成 {len(_scope & _done)}，待跑 "
                f"{len(_scope - _done)}）⇒ 目标 TOTAL={TOTAL}")

    if args.once:
        d = done_count()
        log(f"[once] done={d}/{TOTAL} 最后判定: {last_verdict()}")
        return

    log(f"supervisor 启动｜stall_sec={args.stall_sec} check_sec={args.check_sec}"
        f"｜max_inflight={args.max_inflight}｜only_cats={args.only_cats or '全部'}"
        f"｜空转熔断 {args.zero_alpha_stop} 个集")
    extra = []
    if args.datasets:
        extra += ["--datasets", args.datasets]
    if args.only_cats:
        extra += ["--only-cats", args.only_cats]
    if args.min_cov is not None:
        extra += ["--min-cov", str(args.min_cov)]
    if args.require_ten_years:
        extra += ["--require-ten-years"]
    if args.keep_fields:
        extra += ["--keep-fields", args.keep_fields]
    if extra:
        log(f"透传 campaign 参数：{' '.join(extra)}")
    restarts = 0
    no_prog = 0
    prev_done = done_count()
    # 日志名带区域后缀：EUR/KOR 若在同一分钟启动会撞同一个文件名（今天真实发生，日志交错）
    logpath = os.path.join(LOGDIR, f"campaign_sup{_SUF}_{datetime.now():%Y%m%d_%H%M}.log")

    while True:
        d = done_count()
        if d >= TOTAL:
            log(f"全部完成 done={d}/{TOTAL}，看门狗退出")
            return
        if restarts > args.max_restarts:
            log(f"重启次数超上限 {args.max_restarts}，退出（需人工介入）")
            return

        p, fh = run_campaign(logpath, args.max_inflight, extra)
        log(f"已拉起 PID={p.pid}｜当前 done={d}/{TOTAL}｜日志 {os.path.basename(logpath)}")

        stalled = False
        last_report = time.time()
        while True:
            time.sleep(args.check_sec)
            rc = p.poll()
            if rc is not None:
                log(f"子进程退出 rc={rc}｜done={done_count()}/{TOTAL}")
                break
            try:
                age = time.time() - os.path.getmtime(logpath)
            except OSError:
                age = 0
            if age > args.stall_sec:
                log(f"检测到停滞：日志 {int(age)}s 未增长（阈值 {args.stall_sec}s）"
                    f"｜done={done_count()}/{TOTAL} ⇒ 杀进程重启")
                kill_tree(p)
                stalled = True
                break
            if time.time() - last_report > 600:
                _ck = {"done": []}
                try:
                    _ck = json.load(open(CKPT, encoding="utf-8"))
                except Exception:
                    pass
                _st = zero_alpha_streak(_ck.get("done") or [], results_map())
                log(f"心跳 done={done_count()}/{TOTAL} 日志静默 {int(age)}s"
                    f"｜零alpha连击 {_st}/{args.zero_alpha_stop}")
                last_report = time.time()

            # ---- 空转熔断（2026-10-25 事故判据）----
            if args.zero_alpha_stop > 0:
                try:
                    _ck = json.load(open(CKPT, encoding="utf-8"))
                except Exception:
                    _ck = {"done": []}
                st = zero_alpha_streak(_ck.get("done") or [], results_map())
                if st >= args.zero_alpha_stop:
                    log(f"⛔ 空转熔断：连续 {st} 个非 SKIP 集 n_alphas=0 "
                        f"（阈值 {args.zero_alpha_stop}）⇒ 管道坏了，不是信号差。"
                        f"请先查 cache/bad_tokens.json 与派发/收割日志，再重启。")
                    kill_tree(p)
                    fh.close()
                    return 2

        try:
            fh.close()
        except Exception:
            pass

        d2 = done_count()
        if d2 >= TOTAL:
            log(f"全部完成 done={d2}/{TOTAL}，看门狗退出")
            return
        # 按类别过滤时 done 永远到不了 TOTAL（分母是全区，过滤后只跑一部分）
        # ⇒ 用「连续 3 轮重启都没有新增完成」判定这轮真的跑空了，避免空转重启死循环
        if d2 <= prev_done:
            no_prog += 1
            log(f"本轮无新增（done 仍 {d2}）｜连续无进展 {no_prog}/3")
            if no_prog >= 3:
                log(f"连续 3 轮无新增 ⇒ 该筛选条件下已无可跑集合，退出（done={d2}/{TOTAL}）")
                return
        else:
            no_prog = 0
        prev_done = d2
        restarts += 1
        log(f"第 {restarts} 次重启{'（因停滞）' if stalled else '（因子进程退出）'}")
        time.sleep(20)


if __name__ == "__main__":
    # 单实例：同一 (region, lane) 只允许一个 supervisor
    try:
        with InstanceLock("supervisor"):
            sys.exit(main())
    except AlreadyRunning as e:
        log(f"[lock] {e}")
        sys.exit(3)
