# -*- coding: utf-8 -*-
"""submit_batch.py - 通用**批量派发仿真**（dispatch，REST 直连），取代 tools/_submit_*.py（共 31 个同构一次性脚本）。

⚠ 词义（skills 审查 SB-24）：这里的「提交」= 把表达式**派发去仿真**（`POST /simulations`），**不是**把 alpha 提交上平台
（`POST /alphas/{id}/submit`，不可逆，走 `workflow_submit_alpha`，见 worldquant-submit-alpha 的提交链）。文件名沿用旧称，含义以本段为准。

入口边界（避免重复实现）：
  - 本文件 = 规范 REST CLI：直接 POST {base_url}/simulations，payload 为 [{type, settings, regular}]。
  - tools/mcp_5slot_batch.py = MCP-SSE 客户端：经 wq-brain-http MCP 调 create_multi_simulation
    （payload 形状为 {alpha_expressions, **settings}），二者传输层与 payload schema 不同，不合并。
  - world-quant-brain-mcp/tools_submit.py 的 submit_alpha = 把**已存在的 alpha_id 提交上平台**的生产原语（不可逆；
    用户确认后经 workflow_submit_alpha 调用，不要直接用）。
  回测批量仿真只有上述两条 REST / MCP 客户端，请勿再新增第三套。

所有被取代脚本的共同结构：
  MCP_DIR + chdir + BrainApiClient + BASE(USA/TOP3000/EQUITY/2014-2023)
  + load(expr 文件) + 组装 payload(type=REGULAR, settings=dict(BASE, decay, neutralization))
  + POST {base_url}/simulations + 打印 Location

用法:
  # 单批次（绝大多数 _submit_* 同构场景）
  python submit_batch.py --path tracking/USA/runs/xxx_batch.txt --decay 4 --neutralization SUBINDUSTRY

  # 多批次（逐批不同 decay / universe，对应 _submit_inst6_t12 / _submit_inst6_z）
  python submit_batch.py --spec spec.json
  # spec.json 例: [{"path":"a.txt","decay":1,"universe":"TOP3000"},
  #                {"path":"b.txt","decay":2,"universe":"TOP1000"}]

  # 试跑（不触网，仅打印将提交的 payload）
  python submit_batch.py --path x.txt --decay 4 --neutralization SUBINDUSTRY --dry-run

可选覆盖 BASE 任意字段: --region/--universe/--delay/--start/--end/--type/--truncation。

⚠ 设置档不可比（2026-10-03，见 warn_strength_gates）
--------------------------------------------------
`nanHandling` / `maxTrade` / `decay` / `neutralization` / `truncation` **不是风格开关，
是强度闸**：IND behavioral_signals 族同表达式 decay8 下，nanHandling=OFF 或
maxTrade=ON ⇒ `sharpe 2.19 → 0.46`。**换档位 = 换信号**，跨档位结果不可比。

而回测入口有多套、缺省互不相同（本工具 BASE / MCP `create_simulation` /
MCP `create_multi_simulation` / `brain-sim-alphas-in-batch-and-track` 纯透传无缺省）：
- 本工具现每次运行回显实际生效档位，命中弱档时打 `[WARN]`；
- 战役权威档位仍以 `tracking/<R>/config/settings.json` 为准（toolkit 铁律：
  region 只从 settings.json 派生）。**本工具 BASE 与之可能不一致，必要时显式传参覆盖。**
- 需要 settings 全显式可控时用 `tools/ind_sim_submit.py`。
"""
import argparse
import asyncio
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台 MCP 目录解析（tools/_pyenv.py）

MCP_DIR = str(_pyenv.mcp_dir())

# 平台并发上限约 10（2026-10-23 实测：campaign 4 + 单条 8 时，第 9~10 条起报
# CONCURRENT_SIMULATION_LIMIT_EXCEEDED）。战役把在飞上限提到 7 后 429 必然出现，
# 这里按 Retry-After 退避重试；重试耗尽才算该批失败。
RETRY_429 = 6

BASE = {
    "instrumentType": "EQUITY", "region": "USA", "universe": "TOP3000",
    "delay": 1, "truncation": 0.0, "pasteurization": "ON",
    # ⚠ 2026-10-03：maxTrade 由 ON 改 OFF。
    #   原值 ON 的两重问题——① 本工具是**无区上下文的裸工具**，不应擅自替某个区
    #   决定档位；② 实测它是**强度闸**而非中性档：.workbuddy/memory/2026-10-02.md
    #   记 IND behavioral_signals 族同表达式 decay8 下 `maxTrade=ON ⇒ sharpe 2.19 → 0.46`，
    #   即一个「可有可无的开关」实际能把信号打掉 4 倍，而本工具此前默认打开它。
    #
    # ⚠ 2026-10-24 更正（原注「与 settings.json 直接矛盾（各区均为 OFF）」有误）：
    #   `tracking/<R>/config/settings.json` 是**按区策略**，13 区中 5 区 ON
    #   （ASI / EUR / GBR / HKG / MEA）、8 区 OFF（AMR / CHN / DEU / GLB / IND / JPN / KOR / USA；
    #   USA 为 maxTrade OFF + nanHandling ON 的混合档）。
    #   EUR 战役（full_template_campaign.py）硬编码 ON 与 EUR 区档**一致，与本工具不矛盾**——
    #   二者场景不同：战役跑该区权威档，本工具是无区缺省取最强信号档。
    #   ⇒ 带区上下文的派发请显式传 `--max-trade`，或走 campaign_intel._xr_region_settings
    #     读 settings.json；不要依赖本工具缺省。缺省 OFF 是「无区时的最强信号档」，不是错误。
    "unitHandling": "VERIFY",
    # ⚠ nanHandling 维持 OFF —— 与 settings.json 一致，**但**实测同族
    #   `nanHandling=OFF ⇒ 2.19 → 0.46`（同上一来源）。战役口径与实测在此冲突，
    #   属需人工裁决的选区决策，本工具不擅自翻转；改为每次运行显式警告 +
    #   `--nan-handling` 可覆盖。裁决前该族请显式传 `--nan-handling ON`。
    "nanHandling": "OFF",
    "maxTrade": "OFF",
    "maxPosition": "OFF", "language": "FASTEXPR", "visualization": False,
    "startDate": "2014-01-01", "endDate": "2023-12-31",
}

#: ⚠ 已知「强度闸」档位——不是风格偏好，会直接改变信号强度（实测见 BASE 注释）。
#: 运行前若命中则显式告警，避免静默用弱档跑完整批再发现结论不可用。
#: 口径来源 .workbuddy/memory/2026-10-02.md（IND behavioral_signals，decay8 同表达式）。
STRENGTH_GATE_SETTINGS = ("nanHandling", "maxTrade")
#: 各键的「已实测会削弱强度」取值（None = 该取值本身是安全档）
WEAK_VALUES = {"nanHandling": {"OFF"}, "maxTrade": {"ON"}}


def load(path):
    """读表达式文件，一行一条。

    ⚠ 2026-10-03：去 UTF-8 BOM。PowerShell 的 `Out-File -Encoding utf8` /
    `Set-Content -Encoding utf8`（Windows PS 5.1）会写 BOM，原实现直接
    `l.strip()` 留下 '\\ufeff'，于是表达式变成 `'\\ufeffadd(rank(...))'` 提交上去
    ——平台侧表现为单条 ERROR 或整批 CANCELLED，而本地看不出任何异常。
    """
    with open(path, encoding="utf-8-sig") as f:
        return [l.strip().lstrip("﻿") for l in f
                if l.strip() and not l.strip().startswith("#")]


def warn_strength_gates(settings):
    """档位回显 + 强度闸告警。

    为什么必须显式告警（2026-10-03）
    --------------------------------
    `nanHandling` / `maxTrade` 看起来像「风格开关」，实测是**强度闸**：
    IND behavioral_signals 族同表达式 decay8 下，二者取弱档
    ⇒ `sharpe 2.19 → 0.46`。也就是说换档位等于**换信号**，而不只是换风格。

    而回测入口有多套且缺省互不相同（本工具 / MCP `create_simulation` /
    MCP `create_multi_simulation` / `brain-sim-alphas-in-batch-and-track`），
    「用哪套工具跑」会静默改变结论。本函数让每次运行都回显实际生效的档位，
    至少让「跨工具结果不可比」这件事在日志里可见。
    """
    weak = [f"{k}={settings[k]}" for k in STRENGTH_GATE_SETTINGS
            if settings.get(k) in WEAK_VALUES.get(k, set())]
    print(f"[settings] nanHandling={settings.get('nanHandling')} "
          f"maxTrade={settings.get('maxTrade')} decay={settings.get('decay')} "
          f"neutralization={settings.get('neutralization')} "
          f"truncation={settings.get('truncation')} universe={settings.get('universe')}")
    if weak:
        print(f"[WARN] 命中已实测的**弱强度档**：{', '.join(weak)}。"
              f"这些不是风格开关而是强度闸（IND behavioral_signals decay8 实测："
              f"弱档 ⇒ sharpe 2.19→0.46）。若本批结论用于选族/判死，"
              f"请先用强档复测或显式覆盖（如 --nan-handling ON）。"
              f"⚠ 换档位=换信号，跨档位结果不可比。", file=sys.stderr)
    return bool(weak)


def build_payload(exprs, decay, neutralization, atype, overrides):
    settings = dict(BASE, decay=decay, neutralization=neutralization)
    # type 只在 payload 顶层，不进 settings
    settings.update({k: v for k, v in overrides.items() if k != "type"})
    return [{"type": atype, "settings": settings, "regular": e} for e in exprs]


#: spec 允许透传进 settings 的键白名单（前缀 + 全量键）。
#: 2026-10-02：原先只认 6 个固定键，spec 里的 nanHandling / pasteurization /
#: unitHandling / maxTrade / maxPosition / language / visualization / truncation
#: 全被静默丢弃 ⇒ 派发口径与 `tracking/<R>/config/settings.json` 漂移
#: （实测 ASI 历史 alpha 为 nanHandling=ON，而 BASE 硬编码 OFF）。
SETTINGS_PASSTHROUGH = {
    "instrumentType", "region", "universe", "delay", "decay", "neutralization",
    "truncation", "pasteurization", "unitHandling", "nanHandling",
    "maxTrade", "maxPosition", "language", "visualization",
    "startDate", "endDate",
    # 2026-10-22：QUICK 模式（平台 2026-09-21 新增）。返回 PnL/Sub-universe PnL/
    # WC/Fitness/IS Ladder/Sharpe/Returns/Turnover，跳过可视化与 Theme/Competition/
    # Correlation 检查、不能直接提交。⚠ QUICK 按纯 RA 标准判 Fail，边界比 FULL 严。
    "simulationMode",
}


def batches_from_args(args):
    """返回 list of (tag, path, decay, neutralization, overrides)。"""
    overrides = {}
    for k, v in [
        ("region", args.region), ("universe", args.universe), ("delay", args.delay),
        ("startDate", args.start), ("endDate", args.end), ("truncation", args.truncation),
        ("nanHandling", args.nan_handling), ("maxTrade", args.max_trade),
        ("simulationMode", args.simulation_mode),
        ("type", args.type if args.type else None),
    ]:
        if v is not None:
            overrides[k] = v
    n = args.neutralization or "SUBINDUSTRY"
    t = args.type or "REGULAR"
    return [(os.path.basename(p), p, args.decay, n, dict(overrides)) for p in args.path]


async def run(batches, sleep, dry_run):
    # 2026-10-06 修：循环内 `os.chdir(MCP_DIR)` 从不还原 ⇒ 第 2 批起相对路径失效、
    # `load(path)` 抛 FileNotFoundError、**脚本静默死在第一批之后**（--spec 多批实际只发第 1 批）。
    # 解：开跑前把全部 path 固化为绝对路径。
    batches = [(tag, os.path.abspath(path), decay, neut, ov)
               for tag, path, decay, neut, ov in batches]
    # 2026-10-24 修（本波实测）：旧实现无论成败都打印 "ALL SUBMITTED"。
    #   insd_trx_w1 首派 ILLIQUID_MINVOL1M 时 10/10 被平台 400 拒（universe 不可用），
    #   脚本仍打印 ALL SUBMITTED —— 调用方（人/Agent/上游节点）会把它当成已发批，
    #   下游"收批"永远等不到结果。改为：失败计数 + 非零退出码 + 末行不撒谎。
    submitted = []
    failed = []
    # 2026-10-24 修（本轮实测）：旧实现在**每批**都 new 一个 BrainApiClient() 并
    # ensure_authenticated() —— 10 批 = 10 次登录，第 8 批起平台返 429（登录限流），
    # 整批在鉴权处抛异常，08/09/10 未派出。改为惰性创建一次、全批复用同一会话。
    client = None
    for tag, path, decay, neut, overrides in batches:
        exprs = load(path)
        payload = build_payload(exprs, decay, neut, overrides.get("type", "REGULAR"), overrides)
        print(f"[{tag}] n={len(payload)} decay={decay} neut={neut} "
              f"type={overrides.get('type','REGULAR')} overrides={overrides}")
        if payload:
            warn_strength_gates(payload[0]["settings"])
        if dry_run:
            print("  DRY-RUN sample:", payload[0] if payload else None)
            continue
        os.chdir(MCP_DIR)
        # 2026-10-02：os.chdir 不会把目录加入 sys.path，venv 下 import brain_api
        # 直接 ModuleNotFoundError。显式插 sys.path。
        if MCP_DIR not in sys.path:
            sys.path.insert(0, MCP_DIR)
        from brain_api import BrainApiClient  # noqa: E402
        if client is None:
            client = BrainApiClient()
            await client.ensure_authenticated()
        # 2026-10-08：n=1 时平台拒收包裹数组（"Multi-simulations require multiple
        # simulations…Single simulations are required to be submitted without the
        # wrapping array"）⇒ 单条发裸 dict，多条才用数组。
        body = payload[0] if len(payload) == 1 else payload
        resp = await client._request("POST", f"{client.base_url}/simulations", json=body)
        # 2026-10-23 修：并发上限提到 7 后必然遇到 429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED。
        # 旧代码 `!= 201` 只打印 BODY 就进入下一批 ⇒ 提高并发反而成批丢作业。
        # 退避时长复用 BrainApiClient._retry_wait_seconds（与 _request_json_with_retries
        # 同一套算法，含 Retry-After 解析），不自己实现第二套；之所以没直接用那个方法，
        # 是它只回 JSON 会丢掉 Location 头，而派发必须靠它取 multisim id。
        attempt = 0
        while resp.status_code == 429 and attempt < RETRY_429:
            wait = client._retry_wait_seconds(resp, attempt)
            print(f"  429 并发已满，等 {wait:.0f}s 重试（{attempt + 1}/{RETRY_429}）")
            await asyncio.sleep(wait)
            resp = await client._request("POST", f"{client.base_url}/simulations", json=body)
            attempt += 1
        loc = resp.headers.get("Location", "")
        print(f"  status={resp.status_code} -> {loc}")
        if resp.status_code != 201:
            print("  BODY:", resp.text[:500])
            failed.append({"tag": tag, "status": resp.status_code,
                           "body": resp.text[:300]})
        else:
            submitted.append({"tag": tag, "n": len(payload), "location": loc})
        time.sleep(sleep)
    if dry_run:
        print("DRY-RUN DONE")
        return
    if failed:
        print(f"PARTIAL/FAILED: 成功 {len(submitted)}/{len(batches)} 批，失败 {len(failed)} 批")
        for f in failed:
            print(f"  FAILED {f['tag']}: status={f['status']} {f['body']}")
        raise SystemExit(1)
    print(f"ALL SUBMITTED ({len(submitted)} 批)")
    for s in submitted:
        print(f"  {s['tag']}: n={s['n']} -> {s['location'] or '(无 Location 头)'}")


def main():
    ap = argparse.ArgumentParser(description="通用 alpha 批量提交（取代 _submit_*.py）")
    ap.add_argument("--path", nargs="+", help="表达式文件路径（可多个，使用相同 decay/neut）")
    ap.add_argument("--decay", type=int, help="decay 值")
    ap.add_argument("--neutralization", default="SUBINDUSTRY")
    ap.add_argument("--type", default="REGULAR")
    ap.add_argument("--spec", help="多批次 JSON 规格文件（list of {path,decay,neutralization?,universe?,type?}）")
    # BASE 覆盖
    ap.add_argument("--region")
    ap.add_argument("--universe")
    ap.add_argument("--delay", type=int)
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--truncation", type=float)
    ap.add_argument("--simulation-mode", choices=["QUICK", "FULL"],
                    help="QUICK=快速初筛（跳过可视化/Theme/Correlation，不能提交）；FULL=完整（终审/提交前用）")
    # ⚠ 强度闸档位（2026-10-03 新增）：nanHandling / maxTrade 实测会改变信号强度
    # （不是风格开关）。BASE 有缺省，但**跨工具缺省互不相同**，故开放显式覆盖，
    # 避免「用哪个入口跑」静默改变结论。
    ap.add_argument("--nan-handling", choices=["ON", "OFF"],
                    help="nanHandling 档位（实测强度闸；BASE 缺省 OFF，与 settings.json 一致）")
    ap.add_argument("--max-trade", choices=["ON", "OFF"],
                    help="maxTrade 档位（实测强度闸；BASE 缺省 OFF）")
    ap.add_argument("--sleep", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.spec:
        spec = json.load(open(args.spec, encoding="utf-8"))
        batches = []
        # 2026-10-09 修（--spec 分支曾**完全忽略** CLI 的区域/档位参数）：
        #   实测 `--spec ... --region DEU --truncation 0.08` 生成的 payload 是
        #   region='USA' + truncation=0.0（BASE 硬编码）⇒ 整批跑错区域/档位。
        #   与 `--path` 分支（batches_from_args）对齐：CLI 显式值作为**默认值**，
        #   spec 条目里的同名键再覆盖它（条目优先）。
        # 2026-10-26 修（本波实测）：`--neutralization` / `--simulation-mode` 在 --spec 分支
        #   被静默丢弃 —— 跑到平台上实际是 SUBINDUSTRY + 平台缺省模式（打印行里能看见），
        #   与 `--path` 分支口径不一致。同 2026-10-09 那次漏 region/档位的形态。
        cli_defaults = {k: v for k, v in (
            ("region", args.region), ("universe", args.universe), ("delay", args.delay),
            ("startDate", args.start), ("endDate", args.end), ("truncation", args.truncation),
            ("nanHandling", args.nan_handling), ("maxTrade", args.max_trade),
            ("simulationMode", args.simulation_mode),
            ("neutralization", args.neutralization),
        ) if v is not None}
        for b in spec:
            ov = dict(cli_defaults)
            # 2026-10-02：放开到 SETTINGS_PASSTHROUGH 白名单（原先只 6 个键，
            # nanHandling 等区域配置项被静默丢弃 → 与 settings.json 口径漂移）
            for k, v in b.items():
                if k in SETTINGS_PASSTHROUGH and v is not None:
                    ov[k] = v
            if b.get("type") is not None:
                ov["type"] = b["type"]
            batches.append((os.path.basename(b["path"]), b["path"],
                            b.get("decay", args.decay),
                            b.get("neutralization", args.neutralization or "SUBINDUSTRY"), ov))
    elif args.path and args.decay is not None:
        batches = batches_from_args(args)
    else:
        ap.error("需提供 --spec，或同时提供 --path 与 --decay")
    asyncio.run(run(batches, args.sleep, args.dry_run))


if __name__ == "__main__":
    main()
