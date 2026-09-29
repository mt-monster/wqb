# -*- coding: utf-8 -*-
"""wave_gate.py - 每波门禁编排器（替代 tracking/<REGION>/scripts/_gate_waveNN.py 族）。

在单次调用内完成：
  1) 候选解析：--candidates JSON（{expressions:[{id,expr}]} / [str] / {exprs:[...]}）
     或 --exprs-file（每行一条）或 --expr（单条）
  2) 语法校验：alpha-expression-verifier（与 gate 闸1 同源，先于 5 闸执行，
     失败即整波拦截——语法错误是整批 CANCELLED 连坐的头号元凶）
  3) 5 闸预检 + 批级多样性：复用 wq-brain-campaign-toolkit 的权威 gate.py
     （路径自动解析 WQ_TOOLKIT_DIR → ~/.qoder-cn/skills → ~/.workbuddy/skills，勿硬编码）
  4) 六维结构多样性 + 质量预估（建议2/3 落地，2026-08-27）：
     pool_diversity.assess 六维报告；quality_predict.predict_all 回测前预估，
     EXPECTED_BLOCK 候选默认仅标注，--quality-block 开启硬拦截（回测配额闸门）
  5) 结果落盘：<campaign-dir>/cache/gate_wave<wave>_<dataset>.json（完整）
     + <campaign-dir>/cache/gate_wave<wave>_<dataset>.out.txt（人类摘要）

用法:
  python tools/wave_gate.py --campaign-dir tracking/KOR --dataset model219 --wave 97 \
      --candidates candidates/wave97_exprs.json
  python tools/wave_gate.py --campaign-dir tracking/USA --dataset fund28 --wave 31 \
      --exprs-file candidates/w31.txt --skip-diversity-gate
  python tools/wave_gate.py --campaign-dir tracking/KOR --dataset model219 \
      --expr "rank(close)" --wave 98

退出码: 0=PASS（语法+5 闸全过）, 1=FAIL（闸门不过，表达式不合格）,
        2=ERROR（gate.py 子进程崩溃/未给出结论 —— 环境问题，不是表达式问题；
          stderr 原文已透传到 [gate ] stderr| 行，自愈命令通常就在里面）
运行环境: 与 gate.py 一致，纯标准库，任意 Python 3.10+ 均可。
"""
import argparse
import importlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# ---- skill 目录自动解析 ----
# 2026-09-27 R12：改走 tools/skill_paths（WQ_*_DIR > ~/.claude > ~/.codex > 历史 Agent 位 >
# 仓库自带 Claude/skills，与 workflow 节点同一顺序）。此前只认 WQ_*_DIR 与 qoder-cn / cursor /
# workbuddy 三个历史位，CLI 直跑与未设 env 的宿主找不到 verifier / gate.py。
_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
from skill_paths import skill_script_dirs  # noqa: E402

_TOOLKIT_CANDIDATES = skill_script_dirs("wq-brain-campaign-toolkit", "WQ_TOOLKIT_DIR")
_VALIDATOR_CANDIDATES = skill_script_dirs("alpha-expression-verifier", "WQ_VALIDATOR_DIR")


def find_script(candidates, name):
    for d in candidates:
        if d and os.path.isfile(os.path.join(d, name)):
            return os.path.join(d, name)
    raise FileNotFoundError(
        f"未找到 {name}：设 WQ_TOOLKIT_DIR/WQ_VALIDATOR_DIR 指定（已搜 "
        f"{', '.join(c for c in candidates if c)}）")


# ---- 工作区根 / 战役库路径（2026-09-27 R19 收敛为一处）----
# 此前 7 处各写 `WQB_ROOT or WQ_PROJECT_ROOT or <作者本机盘符路径>`：仓库不在该盘符时，
# --exprs-file 候选被写进 cwd 下一个以该盘符路径命名的杂散目录（.gitignore 的 data/ 规则把它
# 吞掉，git status 看不见），gate.py 读真库找不到候选 → exit 2 "门禁未跑完"。
# 这 7 处还都不认 WQB_DB_PATH，而 toolkit gate.py（经 get_store）认。
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


def _write_back_gate_status(campaign, region, wave, gate_json, seeded):
    """--exprs-file / --candidates / --expr 入库的候选：按 gate.py 逐条结论回写 status。

    2026-09-27 R7/R21：此前候选在门禁**之前**以 gated 入库、结论出来后不回写 ——
    gated 同时表示"送过闸"与"过了闸"，FAIL 候选照样计入积压闸的 pending+gated
    （KOR 真实复现：三次重跑门禁留下 117 条 gated，积压 32% 越过 30% 上限拦下下一波）。
    现在：入库为 pending → 静态闸 1-5 逐条 PASS → gated；FAIL → fail（与 pipeline 坏式
    回写同一状态：build_wave / 去重不再重选；reason 记闸门原因，重跑门禁通过会改回 gated）。
    只因闸门环境缺失而 FAIL 的（issues 全是 [SYNTAX_UNKNOWN]/[ARITY_UNKNOWN]）保持 pending：
    那是"没校验"，不是"式子坏"——同日真实环境复现过 op_arity 不可达时 39/39 全记 fail。
    只动本批入库的式子；批级闸（多样性 / 知识闸）不改逐条状态。
    """
    verdicts = {}
    for it in (gate_json.get("report") or []):
        e = str(it.get("expr") or "").strip()
        if e:
            verdicts[e] = it
    if not verdicts:
        print("[state] gate.py 未回传逐条结论（toolkit 旧版？），候选保持 pending")
        return None
    CampaignStore = _campaign_store_cls(campaign)
    st = CampaignStore(_wqb_db_path(campaign))
    n_gated = n_fail = n_unverified = 0
    try:
        ids = {}
        for row in st.list_expressions(region, str(wave)):
            ex = str(row.get("expression") or "").strip()
            if ex and row.get("id") is not None:
                ids.setdefault(ex, int(row["id"]))
        passed = []
        for e in dict.fromkeys(x.strip() for x in seeded):
            it, eid = verdicts.get(e), ids.get(e)
            if it is None or eid is None:
                continue
            if it.get("pass"):
                passed.append(eid)
            elif _env_unknown_only(it.get("issues")):
                n_unverified += 1
            else:
                reason = ("gate FAIL: " + "；".join(map(str, it.get("issues") or [])))[:200]
                res = st.set_expression_status(region, str(wave), "fail", ids=[eid], reason=reason)
                n_fail += int(res.get("n_updated") or 0)
        if passed:
            res = st.set_expression_status(region, str(wave), "gated", ids=passed,
                                           reason="gate PASS（静态闸 1-5）")
            n_gated += int(res.get("n_updated") or 0)
    finally:
        st.close()
    print(f"[state] 逐条状态回写：gated {n_gated} / fail {n_fail}（FAIL 候选不再计入积压）"
          + (f" / 未判定 {n_unverified}（闸门环境缺失，保持 pending）" if n_unverified else ""))
    return {"gated": n_gated, "fail": n_fail, "unverified": n_unverified}


#: gate.py 的"闸门环境缺失"逐条标记（与 toolkit gate.ENV_UNKNOWN_TAGS 一致）：没校验，不是式子坏
_ENV_UNKNOWN = re.compile(r"^\[(SYNTAX|ARITY)_UNKNOWN\]")


def _env_unknown_only(issues):
    issues = [str(x) for x in (issues or [])]
    return bool(issues) and all(_ENV_UNKNOWN.match(x) for x in issues)


# ---- gate.py 子进程终态判定（ERROR / FAIL / PASS 三分）----
# 历史缺陷（2026-09-08 修复）：gate.py 崩溃时 stdout 无 JSON，旧实现把它记成
# all_pass=None 再一路落到 FAIL 分支，使用者看到的是"表达式不合格"，而真实原因
# （如缺 typed catalog）只有单独手跑 gate.py 才看得到。现在无结论 = ERROR。
_GATE_ERR_TAIL = 4000  # stderr 截尾上限：FileNotFoundError 的自愈命令在 traceback 末尾，800 会把它切掉
_GATE_OUT_TAIL = 800   # stdout 只做背景，真正的原因在 stderr


def parse_gate_payload(stdout):
    """从 gate.py 的 stdout 取结论 JSON（payload 恒为最后一次打印，indent=1）。

    返回 dict（含 bool all_pass）或 None。None 表示 gate.py 没有给出结论，
    调用方必须按 ERROR 处理，不得当成 all_pass=False。
    """
    text = stdout or ""
    starts, off = [], 0
    for line in text.splitlines(keepends=True):
        starts.append(off)
        off += len(line)
    for i in reversed(starts):
        if text[i:i + 1] != "{":
            continue
        try:
            obj = json.loads(text[i:].strip())
        except Exception:
            continue
        if isinstance(obj, dict) and isinstance(obj.get("all_pass"), bool):
            return obj
    return None


def _echo_block(text, prefix, limit):
    """把子进程输出原样透传（截尾但不静默丢弃）。"""
    s = (text or "").rstrip()
    if not s:
        return False
    if len(s) > limit:
        print(f"{prefix} ...(前 {len(s) - limit} 字符省略)")
        s = s[-limit:]
    for line in s.splitlines():
        print(f"{prefix} {line}")
    return True


def gate_error_exit(cmd, r, reason):
    """gate.py 未给出结论 -> ERROR 终态，措辞与"闸门不过"的 FAIL 严格区分。

    透传 stderr 原文（gate.py 的异常消息里通常已带自愈命令，如
    `scan_fields.py --campaign-dir <dir> --dataset <ds>`），并以退出码 2 结束
    （FAIL 仍为 1），让上游 pipeline 能区分"环境坏了"与"这批表达式不合格"。
    """
    print()
    print(f"[gate ] ERROR: {reason}")
    # stdout 先打（多是 store 启动 WARN 之类的背景噪声），stderr 后打 ——
    # 真正的原因要紧挨着 [done ] 行，别被噪声挤到上面去。
    _echo_block(r.stdout, "[gate ] stdout|", _GATE_OUT_TAIL)
    if not _echo_block(r.stderr, "[gate ] stderr|", _GATE_ERR_TAIL):
        print("[gate ] stderr| (空)")
    print(f"[gate ] 复现命令: {subprocess.list2cmdline(cmd)}")
    print("[done ] ERROR: 门禁未跑完 —— gate.py 异常退出，不是闸门不过。"
          "本波未产出门禁结论，也未写 gate_results；按上面 stderr 修复环境后重跑。")
    sys.exit(2)


def gate_fail_reasons(payload):
    """从 gate.py 结论里摘出失败的子闸，供 FAIL 行给出可读原因。"""
    reasons = []
    total, passed = payload.get("total"), payload.get("passed")
    if isinstance(total, int) and isinstance(passed, int) and passed < total:
        reasons.append(f"静态闸 1-5 拦截 {total - passed}/{total} 条")
    for key, label in (("diversity_gate", "批级多样性闸"),
                       ("sanity_gates", "数据质量闸"),
                       ("priors_gate", "知识闸")):
        sub = payload.get(key)
        if isinstance(sub, dict) and sub.get("pass") is False:
            n = len(sub.get("issues") or [])
            reasons.append(label + (f"（{n} 项）" if n else ""))
    blocked = (payload.get("gate0") or {}).get("blocked") or []
    if blocked:
        reasons.append(f"闸0 语义反模式（{len(blocked)} 条）")
    env_only = [it for it in (payload.get("report") or [])
                if not it.get("pass") and _env_unknown_only(it.get("issues"))]
    if env_only:
        reasons.append(f"其中 {len(env_only)} 条仅因闸门环境缺失（verifier / op_arity 不可达）判 FAIL、"
                       "不是表达式问题——设 WQB_WORKSPACE 指向工作区根 / WQ_VALIDATOR_DIR 后重跑")
    return reasons


def env_error_exit(reason):
    """门禁环境缺失（verifier / ply / toolkit gate.py）→ ERROR 终态，退出码 2（闸门不过的 FAIL 为 1）。

    2026-09-27 R12（审计 N12）：此前缺 ply 时 verifier 在 import 阶段 sys.exit(1)，缺 verifier /
    gate.py 时 FileNotFoundError 未捕获（Python 同样 exit 1）——上游把"环境坏了"读成"这批表达式不合格"。
    """
    print(f"[done ] ERROR: 门禁环境缺失 —— {reason}。本波未产出门禁结论、也未写 gate_results，"
          "不是表达式问题；修好环境后重跑。")
    sys.exit(2)


def load_validator():
    """动态加载 alpha-expression-verifier 的 ExpressionValidator（直调，免子进程）。"""
    try:
        dir_ = os.path.dirname(find_script(_VALIDATOR_CANDIDATES, "validator.py"))
    except FileNotFoundError as e:
        env_error_exit(str(e))
    sys.path.insert(0, dir_)
    try:
        mod = importlib.import_module("validator")
    except (ImportError, SystemExit) as e:  # verifier 缺 ply 时在 import 阶段 sys.exit(1)
        env_error_exit(f"alpha-expression-verifier 加载失败（{dir_}；通常是缺 ply："
                       f"pip install -r world-quant-brain-mcp/requirements.txt）：{e!r}")
    return mod.ExpressionValidator()


def load_arity_checker():
    """加载 wqb.expression.op_arity.check_expression（算子元数 + 命名参数闸）。

    本文件在仓库 tools/ 下，src/ 必然相邻；取不到即视为 checkout 损坏，
    调用方标 ARITY_UNKNOWN 并计 FAIL——静默放过才是最坏结果。
    """
    src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
    if os.path.isdir(src) and src not in sys.path:
        sys.path.insert(0, src)
    try:
        from wqb.expression.op_arity import check_expression as _chk
    except Exception as exc:  # pragma: no cover - 仅在 checkout 损坏时触发
        print(f"[arity] 模块不可达: {exc}")
        return None
    return _chk


def parse_candidates(a):
    """候选解析 → [(id_or_index, expr)]；兼容 DB / JSON / txt / 单条。"""
    if getattr(a, "from_db", False):
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        # tools/wave_gate.py 不在 toolkit scripts 下，直接 import wqb.store
        CampaignStore = _campaign_store_cls(a.campaign_dir)
        st = CampaignStore(_wqb_db_path(a.campaign_dir))
        try:
            region = a.region
            if not region:
                settings = json.load(open(os.path.join(a.campaign_dir, "config", "settings.json"), encoding="utf-8"))
                region = settings.get("region")
            rows = st.list_expressions(region, str(a.wave), dataset=a.dataset)
            if not rows:
                rows = st.list_expressions(region, str(a.wave))
            # 2026-09-03 修复：--from-db 时保留 expressions.id，避免 gate_results.syntax.items[].id 是 1-N 序号
            # 2026-09-03 修复2：排除 superseded 行（坏行/已提交候选不应再入门禁与回测）
            # 2026-09-09 D12 修复：同时排除 dropped（纪律废弃终态）。此前只排 superseded，
            # Agent dropped 的零 alpha 骨架（含 vec_* 类型不兼容的 11637）仍入门禁，
            # 一条 [TYPE] FAIL 拖垮整波 all_pass。
            items = [{"id": r.get("id"), "expression": r.get("expression")} for r in rows
                     if r.get("expression") and r.get("status") not in ("superseded", "dropped")]
        finally:
            st.close()
        if not items:
            raise SystemExit(f"db 无候选: wave={a.wave} dataset={a.dataset}")
    elif a.candidates:
        d = json.load(open(a.candidates, encoding="utf-8"))
        items = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
    elif a.exprs_file:
        items = [ln.strip() for ln in open(a.exprs_file, encoding="utf-8") if ln.strip()]
    elif a.expr:
        items = [a.expr]
    else:
        raise SystemExit("need --from-db / --candidates / --exprs-file / --expr 之一")
    out = []
    for i, it in enumerate(items, 1):
        if isinstance(it, dict):
            e = it.get("expr") or it.get("code") or it.get("expression")
            cid = it.get("id") or it.get("name") or i
        elif isinstance(it, str):
            e, cid = it, i
        else:
            continue
        if e:
            out.append((cid, e))
    if not out:
        raise SystemExit("候选解析为空")
    return out


# ---- 机制-形状一致性软闸（--template-family，WARN 不阻断）----
import re as _re


def _load_template_families_for_gate():
    """加载 toolkit config/template_families.json（config 在 scripts 上一级）。"""
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


def _field_profile_map_for_gate(region, dataset, campaign_dir=None):
    """从 wqb.db 读 field_profile（注入 src/，与 parse_candidates 同模式）。"""
    try:
        CampaignStore = _campaign_store_cls(campaign_dir)
        st = CampaignStore(_wqb_db_path(campaign_dir))
        try:
            return st.get_field_profile_map(region, dataset)
        finally:
            st.close()
    except Exception:
        return {}


def _semantic_gate(a, campaign, items):
    """闸 SEM：字段语义归类硬门（2026-09-28）。

    读 ledger `s1_semantic_<dataset>`（由 tools/field_semantic_classify.py 产出），
    把命中 `blocked_fields`（货币代码 / 汇率换算 / 标识符 / 分类码 / 日期口径）
    的表达式**直接剔出候选**——这类表达式语法全对但语义为恒等式或字符串比较，
    语法闸与 gate.py 都拦不住，只能靠回测烧配额。

    返回 dict：{region, dataset, ledger_missing, blocked_field_count,
                removed: [(cid, expr, hit)], items: 幸存的 [(cid, expr)]}
    """
    import re as _re
    region = a.region
    if not region:
        try:
            with open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8") as f:
                region = (json.load(f) or {}).get("region")
        except Exception:
            region = None
    if not region:
        region = os.path.basename(str(campaign)).upper()
    dataset = a.dataset

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from wqb.db_conn import connect as _dbconn  # 规范工厂（禁裸 sqlite3.connect）
    conn = _dbconn(readonly=True)
    try:
        row = conn.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key=?",
            (region, f"s1_semantic_{dataset}"),
        ).fetchone()
    except Exception as e:
        # ⚠ 读不到台账（库不可达 / 缺表 / 库被换）**等同于未做归类**，按缺台账 fail-closed。
        # 2026-09-28：此前这里被上层 `except Exception` 吞成「闸 SEM 异常（不阻断）」，
        # 等于给了「换个空库就能绕过」的口子——与 fail-closed 契约相悖。
        print(f"[sem  ] 台账不可读（按缺台账处理）: {e}", file=sys.stderr)
        return {"region": region, "dataset": dataset, "ledger_missing": True,
                "blocked_field_count": 0, "removed": [], "items": items}
    finally:
        conn.close()

    if row is None:
        return {"region": region, "dataset": dataset, "ledger_missing": True,
                "blocked_field_count": 0, "removed": [], "items": items}

    try:
        sem = json.loads(row[0])
    except Exception as e:
        print(f"[sem  ] s1_semantic_{dataset} 解析失败（按缺台账处理）: {e}", file=sys.stderr)
        return {"region": region, "dataset": dataset, "ledger_missing": True,
                "blocked_field_count": 0, "removed": [], "items": items}

    blocked = {b["field"] if isinstance(b, dict) else b for b in (sem.get("blocked_fields") or [])}
    # 非信号字段的宽匹配：台账黑名单 + 名称模式双保险（防台账过期 / 漏网）。
    #
    # ⚠ 2026-09-28 收紧：原模式含 `is_` / `_flag$` / `_code$` 等**未锚定子串**，会把
    # `oth466_is_ebit_oper_q`（**Income Statement** EBIT，users=248）这类字段当布尔标志误杀
    # —— 实测 other466 上误杀 39/177（22%），且被杀的恰是 users 最高的利润表核心字段。
    # 歧义缩写（is = Income Statement）与「技术分析 indicator」不能靠名字/裸名词判，
    # 故此处只保留**无歧义强标识符**；标志位由 `s1_semantic_<ds>` 的描述文判定结果承担
    # （见 tools/field_semantic_classify.py 的 NON_SIGNAL_DESC_PATTERNS）。
    _BAD_PAT = _re.compile(
        r"currency_code|cur_code|_ras\d*$|exrate|exchange_rate|^fx_|_fx_|_fx$|"
        r"gvkey|cusip|isin|sedol|ticker|iso_country|country_code|exchange_code|region_code|"
        r"fiscal_year_end|report_date|period_end|_date$|_dt$|"
        r"_share_class_|shares_outstanding_class")
    removed, keep = [], []
    for cid, e in items:
        fields = [f for f in _re.findall(r"\b[a-z][a-z0-9_]{4,}\b", e or "")]
        hit = [f for f in fields if f in blocked or _BAD_PAT.search(f)]
        if hit:
            removed.append((cid, e, hit[:3]))
        else:
            keep.append((cid, e))

    print(f"[sem  ] 闸 SEM: 台账命中，黑名单 {len(blocked)} 字段；"
          f"候选 {len(items)} -> 剔除 {len(removed)} -> 幸存 {len(keep)}"
          + (f"（剔除率 {100*len(removed)/max(1,len(items)):.1f}%）" if items else ""))
    for cid, e, hit in removed[:8]:
        print(f"[sem  ]   ✗ {cid}: 非信号字段 {hit} :: {str(e)[:90]}")
    if len(removed) > 8:
        print(f"[sem  ]   … 另有 {len(removed)-8} 条同类剔除")

    # ---- 落库：命中的表达式标 dropped（2026-09-28）----
    # 只在内存里剔除**不够**：gate.py / pipeline.py 都是按 DB 的 expressions.status 取数，
    # 不落库的话这 172 条语义垃圾照样会被 gate.py 判定、被 pipeline.py 发批。
    # 仅 --from-db 路径的 id 才是真实 expressions.id（--exprs-file 是 1..N 序号）。
    dropped_n = 0
    if getattr(a, "from_db", False) and removed:
        ids = [cid for cid, _, _ in removed if isinstance(cid, int)]
        if ids:
            dbp = _wqb_db_path(campaign)
            conn = _dbconn()
            try:
                ph = ",".join("?" * len(ids))
                cur = conn.execute(
                    f"UPDATE expressions SET status='dropped', updated_at=? "
                    f"WHERE id IN ({ph}) AND region=?",
                    (__import__("datetime").datetime.now().isoformat(timespec="seconds"), *ids, region),
                )
                conn.commit()
                dropped_n = cur.rowcount
            except Exception as e:
                print(f"[sem  ] ⚠ 落库标 dropped 失败（内存剔除仍生效）: {e}", file=sys.stderr)
            finally:
                conn.close()
            print(f"[sem  ] 已落库标 dropped {dropped_n} 条（防下游按 DB status 取回）")

    return {"region": region, "dataset": dataset, "ledger_missing": False,
            "blocked_field_count": len(blocked), "removed": removed, "items": keep,
            "dropped_in_db": dropped_n}


def _extract_fields_from_expr(expr, known_fields):
    """从表达式提取引用的字段 id（在 known_fields 集合内）。"""
    tokens = _re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr)
    return [t for t in tokens if t in known_fields]


def _match_premise(profile, premise, field_id):
    """轻量版机制前提校验（与 implement_idea._field_matches_family 同逻辑，纯标准库）。"""
    if not premise or not profile:
        return True
    forbidden = premise.get("forbidden_shape")
    if forbidden and (profile.get("shape") or "unknown") in forbidden:
        return False
    shape_req = premise.get("shape_requirement") or {}
    shapes = premise.get("shape") or shape_req.get("shape")
    if shapes and (profile.get("shape") or "unknown") not in shapes:
        return False
    cov = profile.get("coverage")
    cov_max = premise.get("coverage_max") or shape_req.get("coverage_max")
    if cov_max is not None and cov is not None and float(cov) > float(cov_max):
        return False
    cov_min = premise.get("coverage_min") or shape_req.get("coverage_min")
    if cov_min is not None and cov is not None and float(cov) < float(cov_min):
        return False
    if "integer" in premise or "integer" in shape_req:
        want = bool(premise.get("integer", shape_req.get("integer")))
        if bool(profile.get("integer")) != want:
            return False
    freqs = premise.get("freq") or shape_req.get("freq")
    if freqs and (profile.get("freq") or "") not in freqs:
        return False
    dtypes = premise.get("data_type")
    if dtypes:
        ftype = (profile.get("data_type") or profile.get("type") or "").upper()
        if ftype and ftype not in [str(d).upper() for d in dtypes]:
            return False
    sem = premise.get("semantic_requirement") or {}
    patterns = sem.get("field_name_pattern") or []
    if patterns and field_id:
        fid = str(field_id).lower()
        if not any(_re.search(p, fid, flags=_re.IGNORECASE) for p in patterns):
            return False
    return True


def _family_shape_gate(items, a, campaign):
    """机制-形状一致性软闸：校验候选字段形状+语义是否满足 --template-family 的 mechanism_premise。

    WARN 不阻断。返回 {family, checked, mismatches: [{id, fields, shapes}], warn: bool}。
    """
    families = _load_template_families_for_gate().get("families") or []
    family = next((f for f in families if f.get("family_id") == a.template_family), None)
    if not family:
        print(f"[famshape] warn: 族 '{a.template_family}' 未注册，跳过软闸")
        return None
    premise = family.get("mechanism_premise") or family.get("field_profile_match") or {}
    if not premise:
        print(f"[famshape] warn: 族 '{a.template_family}' 无 mechanism_premise，跳过软闸")
        return None

    region = a.region
    if not region:
        try:
            settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
            region = settings.get("region")
        except Exception:
            region = None
    if not region:
        print("[famshape] warn: 无 region，跳过软闸")
        return None

    prof_map = _field_profile_map_for_gate(region, a.dataset, campaign)
    if not prof_map:
        print(f"[famshape] warn: {region}/{a.dataset} 无 field_profile，跳过软闸")
        return None
    known = set(prof_map.keys())

    mismatches = []
    checked = 0
    for cid, expr in items:
        fields = _extract_fields_from_expr(expr, known)
        if not fields:
            continue
        checked += 1
        bad = [(f, (prof_map[f].get("shape") or "unknown")) for f in fields
               if not _match_premise(prof_map[f], premise, f)]
        if bad:
            mismatches.append({"id": cid, "bad_fields": bad, "expr": expr[:80]})

    warn = bool(mismatches)
    print(f"[famshape] 族 '{a.template_family}' 机制-形状一致性: {checked} 候选校验, "
          f"{len(mismatches)} 不匹配 => {'WARN' if warn else 'PASS'}")
    for m in mismatches[:5]:
        print(f"[famshape]   不匹配 id={m['id']}: {m['bad_fields']}")
    return {"family": a.template_family, "checked": checked,
            "mismatch_count": len(mismatches), "mismatches": mismatches, "warn": warn}


def _settings_region(campaign_dir):
    """从战役目录的 config/settings.json 读 region（--region 缺省时的兜底）。"""
    try:
        with open(os.path.join(campaign_dir, "config", "settings.json"),
                  encoding="utf-8") as f:
            return json.load(f).get("region")
    except Exception:
        return None


#: 体检硬门缺包时的合法行为。warn = 灰度默认（告警放行），enforce = fail-closed 整波拦截。
INSPECT_MODES = ("off", "warn", "enforce")
DEFAULT_INSPECT_MODE = "warn"


def resolve_inspect_mode(cli_value=None, env=None):
    """解析体检硬门缺包策略，优先级：CLI > 环境变量 `WQB_INSPECT_MODE` > 默认 warn。

    2026-09-17 P1-1：此前缺包**恒静默放行**，导致「无体检包」与「体检通过」在输出上
    无法区分（历史三连复发）。抽出本函数使策略可单测，并支持 CLI 强制 fail-closed。
    非法取值一律回落默认（不让拼错的 mode 意外关掉把关）。
    """
    env = os.environ if env is None else env
    raw = cli_value or env.get("WQB_INSPECT_MODE") or DEFAULT_INSPECT_MODE
    mode = str(raw).strip().lower()
    return mode if mode in INSPECT_MODES else DEFAULT_INSPECT_MODE


def _waiver_phase(a, campaign, region, inspect_mode, rg):
    """逃生口 → waiver 检查（2026-09-29，skills 审查 X-8）。

    开了哪个逃生口（`--skip-diversity-gate` / `--skip-semantic-gate` / `--semantic-gate off` /
    `--inspect-mode off` / `--no-prod-family-gate` / 区域闸显式降级），就查台账里有没有对应闸的
    有效 waiver（键 `waiver_<gate>_<region>_<wave|all>`，协议与校验在 `wqb.waiver`）。
    缺省 warn：无 waiver 只在**首屏**打醒目告警并进报告 `waivers`；`--waiver-mode enforce`
    （或 `WQB_WAIVER_MODE=enforce`）下无 waiver 即 exit 2。逃生口本身不变，只是不再能静默使用。
    返回 SkipDecision 列表（供写进报告）。
    """
    for root in (_wqb_root(campaign), _REPO_ROOT):
        src = os.path.join(root, "src")
        if os.path.isdir(os.path.join(src, "wqb")):
            if src not in sys.path:
                sys.path.insert(0, src)
            break
    try:
        from wqb import waiver as W
    except Exception as e:  # 无 wqb 包时本闸其余部分也跑不起来；不因检查本身崩溃
        print(f"[waiver] wqb.waiver 不可导入（{type(e).__name__}: {e}）：逃生口未做 waiver 检查", file=sys.stderr)
        return []

    rg_mode = rg_default = None
    if rg is not None and getattr(rg, "resolve_mode", None):
        rg_mode, _ = rg.resolve_mode(a.gate_mode)
        _dm = getattr(rg, "default_mode", None)      # 旧安装位的 toolkit 可能没有
        rg_default = _dm() if _dm else None
    sem_env = (os.environ.get("WQB_SEM_MODE") or "").strip().lower()
    esc = []
    if a.skip_diversity_gate:
        esc.append(("diversity", "--skip-diversity-gate"))
    if a.skip_semantic_gate:
        esc.append(("semantic", "--skip-semantic-gate"))
    elif a.semantic_gate == "off":
        esc.append(("semantic", "--semantic-gate off"))
    elif a.semantic_gate is None and sem_env == "off":
        esc.append(("semantic", "WQB_SEM_MODE=off"))
    if inspect_mode == "off":
        esc.append(("inspect", "--inspect-mode off"))
    if not a.prod_family_gate:
        esc.append(("prod_family", "--no-prod-family-gate"))
    # 区域闸：显式 off，或灰度期结束后显式回退 warn 才算逃生口（灰度期缺省 warn 不是逃生）
    if rg_mode == "off" or (rg_mode == "warn" and rg_default == "enforce"):
        esc.append(("region_gates", f"--gate-mode {rg_mode}"))
    if not esc:
        return []

    mode = W.resolve_mode(a.waiver_mode)
    conn = None
    if mode != "off":
        try:
            from wqb.db_conn import connect as _dbconn
            conn = _dbconn(_wqb_db_path(campaign), readonly=True)
        except Exception as e:  # 库不可达：check_skip 按「无 waiver」处理（enforce 下 fail closed）
            print(f"[waiver] 台账不可读（{e}）：按无 waiver 处理", file=sys.stderr)
    decisions = []
    try:
        for gate, flag in esc:
            decisions.append(W.check_skip(conn, gate, region, a.wave, flag, mode=mode))
    finally:
        if conn is not None:
            conn.close()
    for d in decisions:
        for line in d.lines:
            print(line, file=sys.stdout if d.ok else sys.stderr)
    blocked = [d for d in decisions if not d.ok]
    if blocked:
        print(f"[waiver] ★★ waiver-mode=enforce：{', '.join(d.gate for d in blocked)} 被跳过但没有有效 waiver"
              "→ 拒绝开波（exit 2）。先写 waiver，或去掉对应逃生口。", file=sys.stderr)
        sys.exit(2)
    return decisions


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
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cands.append(os.path.join(repo, "Claude", "skills",
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


# ---- 闸 PF：信号族死路预检闸（2026-09-25 P2 落地，gate.py 闸9 已占用窗口白名单）----
# 背景：F2 闸门凭证断档（2055 UNSUBMITTED 中 90.5% 的 prod_corr 未测）；
# IND intraday_pv_feats 连投 3 波 24 条（S 4.4-6.5 全 IS 过）后才查 prod=0.79-0.92 整族报废。
# SOP "任何新信号族在投入第二波之前必须先 prod-first 探针" 此前无代码级把关。
# 本闸把 prod-first 从「S4 收批后必调」前移到「七槽开批前硬门」，判据：
#   - 同表达式字段族 = 已确认 prod 撞墙死路（基于 DB 中同字段集的实测 prod_corr）→ FAIL 拦截
#   - 同表达式字段族 = 已知 prod 干净（prod<0.7）  → PASS（家族已探明，可扩批）
#   - 新信号族（无任何 prod 记录）                  → WARN（建议先 prod-first 探针再扩批）
# 判据是"表达式中字段集精确匹配"，独立于闸 2.6 的字段热度 / 数据集占比判据。

_PF_OPS_GATE = set("""
rank add multiply subtract divide group_rank group_zscore group_neutralize group_mean group_sum
group_count group_scale group_std_dev group_backfill ts_mean ts_delta ts_zscore ts_rank ts_backfill
ts_decay_linear ts_std_dev ts_sum ts_max ts_min ts_corr ts_covariance ts_regression ts_av_diff
ts_arg_max ts_arg_min ts_product ts_quantile ts_count_nans ts_scale ts_step ts_returns ts_ir
ts_delay ts_kurtosis ts_max_diff vec_avg vec_sum vec_max vec_min vec_stddev vec_count vec_range
winsorize scale normalize signed_power quantile power reverse zscore abs log sign sqrt inverse
densify pasteurize hump kth_element trade_when if_else bucket greater less equal and or not is_nan
not_equal less_equal greater_equal max min days_from_last_change last_diff_value vector_neut tail
industry sector subindustry market country exchange std range rettype driver buckets
true false nan cap close open high low volume vwap returns adv20 sharesout free_float split dividend
""".split())


_OPS_PATTERN = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(")


def _extract_ops(expr):
    """提取表达式里所有函数调用名（小写）。"""
    return [m.group(1).lower() for m in _OPS_PATTERN.finditer((expr or "").lower())]


def _pf_family(expr, n_ops=2):
    """信号族指纹 = 前 n_ops 个函数调用名 join（保留算子结构）。

    判据：对 mdl135_d01_icc 的实证 —— 同字段在「+ vec_avg」骨架下 prod=0.76-0.82（死路），
    在「+ vec_avg × ts_zscore」骨架下 prod=0.46-0.57（干净）。所以**骨架比字段更准**。
    取前 n_ops=2 个算子做族指纹，平衡宽（易匹配）与窄（精准）的粒度。
    """
    ops = _extract_ops(expr)
    return "→".join(ops[:n_ops]) if ops else "?"


def _load_prod_wall_families(region, n_ops=2):
    """读 alphas 表 + ledger_kv，按信号族指纹（骨架前缀）分组。

    2026-09-25 P1 增强：除 alphas 表（全库 prod 覆盖率仅 4.4%）外，还读 ledger_kv
    里 `prod_family_<region>_<skeleton>` 键（由 campaign_intel.py prod-first 探针
    自动回写），让闸 PF 下次跑时能直接消费最新证据，不再只依赖 alphas 表的稀疏记录。

    墙家族 = 同骨架至少有 1 条 prod_corr >= 0.7 的实测记录；
    干净家族 = 有 >=1 条 prod_corr < 0.7 的记录。
    """
    try:
        # 2026-09-27：勿硬编码本机路径（P1 R19 守护 test_wave_gate_db_path_never_hardcoded）；
        # 复用统一解析：src 注入走 _campaign_store_cls（工作区 src 优先），库路径走 _wqb_db_path。
        CampaignStore = _campaign_store_cls()
        st = CampaignStore(_wqb_db_path())
        try:
            rows = st.list_alphas_by_region(region)  # 字段含 alpha_id/expression/prod_correlation/corr_checked_at
        finally:
            st.close()
    except Exception:
        return {}
    fams = {}
    for r in rows:
        fam = _pf_family(r.get("expression") or "", n_ops)
        if not fam or fam == "?":
            continue
        pc = r.get("prod_correlation")
        if pc is None:
            continue
        pc = float(pc)
        cur = fams.setdefault(fam, {"prod_corr": pc, "prod_max": pc, "n": 0, "n_wall": 0,
                                    "examples": []})
        cur["n"] += 1
        # 2026-09-28 max/min 双记（此前只留 min=最干净，把"族里出现过 ≥0.7 撞墙"误标成干净，
        # 注释却写"取最严格"）。死路判据看 min（全族皆墙才 enforced），混合证据看 max（WARN+加深）。
        cur["prod_corr"] = min(cur["prod_corr"], pc)
        cur["prod_max"] = max(cur.get("prod_max", pc), pc)
        if pc >= 0.7:
            cur["n_wall"] += 1
        if len(cur["examples"]) < 3:
            cur["examples"].append(r.get("expression", "")[:60])

    if n_ops != 2:
        # 3 算子粒度只用 alphas 行（ledger 键固定是 2 算子骨架名，无法反推）
        return fams

    # 2026-09-25 P1：合并 ledger_kv 里 prod-first 探针回写的骨架指纹（覆盖率补偿）
    try:
        import sqlite3 as _sq
        _db = os.path.join(wqb_root, "data", "wqb.db")
        _c = _sq.connect(_db)
        _c.row_factory = _sq.Row
        _prefix = f"prod_family_{region}_"
        for _r in _c.execute(
                "SELECT key, value FROM ledger_kv WHERE region=? AND key LIKE ?",
                (region, _prefix + "%")):
            try:
                _fam = _r["key"][len(_prefix):]
                _v = json.loads(_r["value"] or "{}")
                _pc = _v.get("prod_corr")
                if _pc is None or not _fam:
                    continue
                _pc = float(_pc)
                _cur = fams.setdefault(_fam, {"prod_corr": _pc, "prod_max": _pc, "n": 0,
                                             "n_wall": 0, "examples": []})
                _cur["n"] += 1
                _cur["prod_corr"] = min(_cur["prod_corr"], _pc)
                _cur["prod_max"] = max(_cur.get("prod_max", _pc), _pc)
                if _pc >= 0.7:
                    _cur["n_wall"] += 1
                if _v.get("alpha_id") and len(_cur["examples"]) < 3:
                    _cur["examples"].append(_v["alpha_id"])
            except Exception:
                continue
        _c.close()
    except Exception:
        pass
    return fams


def check_prod_family_gate(exprs, region, dataset, min_confidence_n=3):
    """闸 PF：骨架级死路预检（prod-first 前置）。

    判据（基于 mdl135_d01_icc 实证：骨架比字段更准）：
      同骨架前缀（前 2 个算子）= 已确认 prod>=0.7 死路  → 拦截（fail-closed）
      同骨架前缀 = 已探明 prod<0.7 干净                    → 通过（该骨架已探明）
      新骨架前缀（无任何 prod 记录）                        → WARN（建议先 prod-first 探针）

    2026-09-25 P5 增强（粒度自适应 + 置信度）：
      - 区隔离：骨架指纹按 region 分库存储（ledger_kv `prod_family_<region>_*`），
        避免跨区误判（rank→ts_backfill 在 KOR 干净 prod=0.54、在 IND 死路 prod=0.725）。
      - 低置信度：骨架指纹 n < min_confidence_n（缺省 3）只 WARN 不 enforced，
        避免小样本误伤（如 n=1 的 rank→group_zscore 在 KOR prod=0.763）。
      - 粒度自适应：若某骨架前缀在本区有混合记录（干净 + 死路），自动加深到前 3 算子。

    Returns report dict（供落 gate_results 与打印）：
      status   = pass / warn / enforced(有家族死路)
      violations = 命中已死路家族的表达式明细
      unknown_families = 未探明的骨架指纹列表（建议 prod-first）
      passed = not violations
    """
    fams = _load_prod_wall_families(region)

    # 2026-09-25 P5：低置信度（n < min_confidence_n）只 WARN 不 enforced
    dead_fams = {f: v for f, v in fams.items()
                 if v["prod_corr"] >= 0.7 and v["n"] >= min_confidence_n}
    dead_fams_low_conf = {f: v for f, v in fams.items()
                          if v["prod_corr"] >= 0.7 and v["n"] < min_confidence_n}
    # 2026-09-28：mixed = 同骨架既有 ≥0.7 撞墙记录又有干净记录（2 算子粒度过粗）。
    # 此前这类族被 min() 归进 ok（GLB 实测 group_zscore→ts_decay_linear 37 条、
    # max 0.9929 仍判"干净"），死路证据被吞。现单列 MIXED：不 enforced（避免误伤
    # 干净变体），但也不算干净——走 3 算子加深判定，加深后仍混合 → WARN + 建议探针。
    mixed_fams = {f: v for f, v in fams.items()
                  if v.get("prod_max", v["prod_corr"]) >= 0.7 > v["prod_corr"]}
    ok_fams = {f: v for f, v in fams.items()
               if v.get("prod_max", v["prod_corr"]) < 0.7}
    unknown_fams = set()

    fams3 = None  # 懒加载：仅遇 MIXED 族才建 3 算子粒度索引

    def _fams3_index():
        nonlocal fams3
        if fams3 is None:
            fams3 = _load_prod_wall_families(region, n_ops=3)
        return fams3

    violations = []
    expr_status = []  # per-expr for diagnostics
    for i, expr in enumerate(exprs):
        fam = _pf_family(expr)
        if fam in dead_fams:
            prod_v = fams[fam]["prod_corr"]
            violations.append({"index": i, "family": fam, "prod_corr": prod_v,
                               "reason": f"骨架指纹 '{fam}' 已确认 prod_corr={prod_v:.3f} ≥ 0.7 死路"
                                         f"（族级 STOP，先换正交概念或新骨架）",
                               "expr": expr[:100]})
            expr_status.append({"index": i, "verdict": "DEAD", "family": fam})
        elif fam in dead_fams_low_conf:
            # 低置信度死路：只 WARN 不 enforced（避免小样本误伤）
            prod_v = dead_fams_low_conf[fam]["prod_corr"]
            expr_status.append({"index": i, "verdict": "WARN_LOW_CONF",
                                "family": fam, "prod_corr": prod_v,
                                "n": dead_fams_low_conf[fam]["n"]})
            unknown_fams.add(fam)
        elif fam in mixed_fams:
            # MIXED：3 算子粒度加深再判一次（ledger 只存 2 算子键，加深索引只用 alphas 行）
            fam3 = _pf_family(expr, 3)
            f3 = _fams3_index().get(fam3)
            if f3 and f3["prod_corr"] >= 0.7 and f3["n"] >= min_confidence_n:
                violations.append({"index": i, "family": fam3, "granularity": 3,
                                   "prod_corr": f3["prod_corr"],
                                   "reason": f"骨架指纹 '{fam}' 证据混合，加深到 '{fam3}' 后确认 "
                                             f"prod_corr={f3['prod_corr']:.3f} ≥ 0.7 死路",
                                   "expr": expr[:100]})
                expr_status.append({"index": i, "verdict": "DEAD", "family": fam3,
                                    "granularity": 3})
            elif f3 and f3.get("prod_max", f3["prod_corr"]) < 0.7:
                expr_status.append({"index": i, "verdict": "OK_DEEP", "family": fam3,
                                    "granularity": 3, "prod_corr": f3["prod_corr"]})
            else:
                unknown_fams.add(fam3 or fam)
                expr_status.append({"index": i, "verdict": "WARN_MIXED", "family": fam,
                                    "deep_family": fam3,
                                    "prod_min": mixed_fams[fam]["prod_corr"],
                                    "prod_max": mixed_fams[fam].get("prod_max"),
                                    "n_wall": mixed_fams[fam].get("n_wall", 0)})
        elif fam in ok_fams:
            expr_status.append({"index": i, "verdict": "OK", "family": fam,
                                "prod_corr": ok_fams[fam]["prod_corr"]})
        else:
            unknown_fams.add(fam)
            expr_status.append({"index": i, "verdict": "UNKNOWN", "family": fam})

    status = "enforced" if violations else ("warn" if unknown_fams else "pass")
    report = {"status": status, "n_checked": len(exprs),
              "n_history_families": len(fams),
              "n_dead_families": len(dead_fams), "n_ok_families": len(ok_fams),
              "n_mixed_families": len(mixed_fams),
              "n_low_conf_dead_families": len(dead_fams_low_conf),
              "n_unknown_families": len(unknown_fams),
              "dead_families_sample": sorted(dead_fams)[:15],
              "mixed_families_sample": sorted(mixed_fams)[:15],
              "ok_families_sample": sorted(ok_fams)[:15],
              "unknown_families_sample": sorted(unknown_fams)[:15],
              "violations": violations, "expr_status": expr_status,
              "passed": not violations}
    if violations:
        report["message"] = (f"{len(violations)}/{len(exprs)} 条表达式命中已死路骨架指纹"
                             f"（{len(dead_fams)} 个骨架已确认死路，n≥{min_confidence_n}）—— 闸 PF 拦截")
    elif unknown_fams:
        report["message"] = (f"PASS；{len(unknown_fams)}/{len(exprs)}"
                             f" 条表达式骨架指纹未探明或低置信度或证据混合，建议先 prod-first 探针"
                             + (f"（mixed 族 {len(mixed_fams)} 个）" if mixed_fams else ""))
    else:
        report["message"] = f"PASS（{len(exprs)} 条全部命中已探明干净骨架）"
    return report


def format_prod_family_report(report):
    lines = [f"[prod-family] 状态={report['status']} {report['message']}"]
    if report.get("dead_families_sample"):
        lines.append(f"[prod-family] 已死路骨架样本: {report['dead_families_sample'][:5]}"
                     + (f" 等 {report.get('n_dead_families', 0)} 个" if report.get("n_dead_families", 0) > 5 else ""))
    for v in report.get("violations", [])[:5]:
        lines.append(f"[prod-family]   命中 #{v['index']}: prod={v['prod_corr']:.3f} {v['family']} | {v['expr']}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="每波门禁编排器：语法 + 5 闸 + 多样性")
    ap.add_argument("--campaign-dir", required=True, help="战役根目录 (如 tracking/KOR)")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--datasets", default="",
                    help="逗号分隔额外数据集，与 --dataset 合并白名单（跨金字塔 mix）")
    ap.add_argument("--wave", default="0",
                    help="波号（字符串，支持 '97' / 's2_pattern_scores_d1' 等；"
                         "与 toolkit pipeline/gate 及 waves.wave_number 同型。"
                         "2026-09-07 P0-3：原 type=int 导致字符串波号无法进门禁——"
                         "ws2_* 波 gate_rows=0 断链的根因）")
    ap.add_argument("--from-db", action="store_true", help="从 expressions 表读候选（推荐）")
    ap.add_argument("--region", default=None, help="区域（缺省读 settings.json）")
    ap.add_argument("--gate-mode", default=None, choices=("off", "warn", "enforce"),
                    help="开波前区域闸模式（2026-09-17 P0-1）：off / warn(只告警) / "
                         "enforce(命中即退出码 2）。缺省先看 WQB_GATE_MODE，再按日期："
                         "灰度期（至 toolkit _lib/region_gates.WARN_SUNSET）warn，之后 enforce")
    ap.add_argument("--candidates", help="兼容：候选 JSON")
    ap.add_argument("--exprs-file", help="每行一条表达式的 txt")
    ap.add_argument("--expr", help="单条表达式")
    ap.add_argument("--skip-diversity-gate", action="store_true", help="透传 toolkit gate.py（repair 批等）")
    ap.add_argument("--skip-semantic-gate", action="store_true",
                    help="跳过闸 SEM（字段语义归类硬门）。默认**强制开启**：缺 s1_semantic_<dataset> "
                         "台账即 exit 2，命中非信号字段（货币代码/汇率/标识符/分类码）的表达式直接剔出候选。"
                         "仅在已确认该数据集无需语义归类时显式使用（会打印醒目告警）。")
    ap.add_argument("--semantic-gate", dest="semantic_gate", default=None,
                    choices=("off", "warn", "enforce"),
                    help="闸 SEM 模式（缺省读环境变量 WQB_SEM_MODE，兜底 enforce）："
                         "off=跳过（= --skip-semantic-gate）/ warn=缺台账仅告警 / "
                         "enforce=缺台账 exit 2 + 黑名单字段剔出候选。")
    ap.add_argument("--batch-type", default="explore", choices=("explore", "repair", "probe"),
                    help="repair/probe 批不做 qp 质量预估标注（2026-09-19：修复批实测 S2.1 却被预估 0.65 BLOCK，纯噪音）")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--fix", action="store_true", help="透传：VECTOR 数据集自动裹 vec_* 后检测")
    ap.add_argument("--inspect-mode", default=None, choices=("off", "warn", "enforce"),
                    help="体检硬门「缺包」时的行为（缺省读环境变量 WQB_INSPECT_MODE，兜底 warn）："
                         "off=跳过不报 / warn=告警但放行（灰度默认）/ "
                         "enforce=fail-closed，缺包即整波拦截（开新数据集前建议 enforce）")
    ap.add_argument("--waiver-mode", default=None, choices=("off", "warn", "enforce"),
                    help="逃生口 waiver 检查（缺省读环境变量 WQB_WAIVER_MODE，兜底 warn）："
                         "warn=用了 --skip-* / --inspect-mode off 等逃生口而台账无有效 waiver 时首屏告警 / "
                         "enforce=无 waiver 即 exit 2 / off=不查（仅测试隔离）。协议见 wqb.waiver、tools/waiver.py")
    ap.add_argument("--prod-family-gate", dest="prod_family_gate", action="store_true",
                    default=True,
                    help="闸 PF：信号族死路预检（2026-09-25，零配额，纯静态）。命中已死路信号族拦截，"
                         "新信号族 WARN 建议 prod-first 探针；--no-prod-family-gate 可关闭")
    ap.add_argument("--no-prod-family-gate", dest="prod_family_gate", action="store_false",
                    help="关闭闸 PF（默认开；enforced 态违规仍会拦截）")
    ap.add_argument("--skip-quality", action="store_true", help="跳过质量预估+六维多样性阶段")
    ap.add_argument("--quality-block", action="store_true",
                    help="EXPECTED_BLOCK 候选计入 FAIL（默认仅标注；回测配额闸门建议开启）")
    ap.add_argument("--probe-mode", action="store_true",
                    help="启用 2+6 探针批模式（早期判死）")
    ap.add_argument("--gem-validate", action="store_true",
                    help="启用 GEM 候选池强制校验")
    ap.add_argument("--min-gem-ratio", type=float, default=0.8,
                    help="GEM 候选最小占比（默认 0.8）")
    ap.add_argument("--s2-field-validate", action="store_true",
                    help="启用 S1 字段候选池强制校验（防止跳过特征工程推荐）")
    ap.add_argument("--s2-field-block", action="store_true",
                    help="S1 字段校验失败时计入 FAIL（默认仅标注）")
    ap.add_argument("--template-family", default=None,
                    help="模板族 family_id（template_families.json）。指定时启用机制-形状一致性软闸："
                         "校验候选字段形状+语义是否满足该族 mechanism_premise，不满足标 WARN（不阻断）")
    a = ap.parse_args()

    items = parse_candidates(a)
    campaign = a.campaign_dir.rstrip("/\\")
    tag = str(a.wave) if a.wave and a.wave != "0" else str(int(__import__("time").time()))

    # 体检硬门缺包策略（2026-09-17 P1-1：由"恒静默放行"升级为可选 fail-closed）
    _inspect_mode = resolve_inspect_mode(a.inspect_mode)

    # 逃生口 → waiver 检查（首屏；见 _waiver_phase）
    _rg = _load_region_gates()
    _wv_region = a.region or _settings_region(campaign) or os.path.basename(campaign).upper()
    _wv_decisions = _waiver_phase(a, campaign, _wv_region, _inspect_mode, _rg)

    # ---- 开波前区域闸（2026-09-17 P0-1 下沉）----
    # signal_floor / stop_rules / backlog 三道闸原先只在 workflow 的 S2/S3 节点生效；
    # 直调本脚本会绕过它们（实证 JPN 2026-09-16）。模式由 toolkit region_gates.resolve_mode 定：
    # --gate-mode > WQB_GATE_MODE > 按日期的缺省（灰度期 warn，2026-10-12 起 enforce）。
    if _rg is None:
        print("[wave_gate] [region-gates] ★未找到 toolkit region_gates，本次跳过开波闸"
              "（设 WQ_TOOLKIT_DIR 可解）", file=sys.stderr)
    else:
        _region_for_gates = a.region
        if not _region_for_gates:
            try:
                with open(os.path.join(campaign, "config", "settings.json"),
                          encoding="utf-8") as f:
                    _region_for_gates = (json.load(f) or {}).get("region")
            except Exception:
                _region_for_gates = None
        if not _region_for_gates:
            _region_for_gates = os.path.basename(campaign).upper()
        _resolve = getattr(_rg, "resolve_mode", None)
        if _resolve is not None:
            _mode, _mode_note = _resolve(a.gate_mode)
            _rep = _rg.run_region_gates(campaign, _region_for_gates, mode=_mode,
                                        dataset=a.dataset, mode_note=_mode_note)
        else:  # 安装位的 toolkit 早于 2026-09-27（没有灰度截止日）：沿用旧缺省，并提示同步
            print("[wave_gate] [region-gates] ★toolkit 安装位过旧（缺 resolve_mode），沿用旧缺省 warn；"
                  "请跑 python tools/sync_skills.py", file=sys.stderr)
            _mode = a.gate_mode or os.environ.get("WQB_GATE_MODE", _rg.MODE_WARN)
            _rep = _rg.run_region_gates(campaign, _region_for_gates, mode=_mode,
                                        dataset=a.dataset)
        if not _rep.get("ok", True):
            print(f"[wave_gate] ★★ 开波被阻断（gate-mode=enforce，命中 "
                  f"{'、'.join(_rep.get('hits') or [])}）", file=sys.stderr)
            sys.exit(2)

    # ---- 0) GEM 候选池校验（可选）----
    gem_report = None
    if a.gem_validate:
        try:
            tools_dir = os.path.dirname(os.path.abspath(__file__))
            if tools_dir not in sys.path:
                sys.path.insert(0, tools_dir)
            from gem_validator import GEMValidator
            validator = GEMValidator()
            candidates_for_gem = [{"id": cid, "expression": e} for cid, e in items]
            gem_report = validator.validate_wave(candidates_for_gem, tag, a.min_gem_ratio)
            print(f"[gem  ] GEM 候选: {gem_report['gem_count']}/{gem_report['total']} "
                  f"({gem_report['gem_ratio']:.1%}) => {'PASS' if gem_report['pass'] else 'FAIL'}")
            if not gem_report["pass"]:
                print(f"[gem  ] 非 GEM 候选: {len(gem_report['non_gem_candidates'])} 条")
        except Exception as e:
            print(f"[gem  ] GEM 校验失败（不阻断）: {e}")

    # ---- 0.6) 机制-形状一致性软闸（--template-family 指定时启用，WARN 不阻断）----
    family_shape_report = None
    if a.template_family:
        family_shape_report = _family_shape_gate(items, a, campaign)

    # ---- 0.5) S1 字段候选池强制校验（2026-09-03 落地，防 wave=170 事故）----
    s2_field_report = None
    if a.s2_field_validate:
        try:
            tools_dir = os.path.dirname(os.path.abspath(__file__))
            if tools_dir not in sys.path:
                sys.path.insert(0, tools_dir)
            from s2_field_validator import validate_wave_fields
            db_path = _wqb_db_path(campaign)
            # region 缺省时从 settings.json 读取（与 parse_candidates 对齐）
            region = a.region
            if not region:
                settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
                region = settings.get("region")
            exprs_only = [e for _, e in items]
            s2_field_report = validate_wave_fields(
                region, str(tag), a.dataset, exprs_only, db_path
            )
            print(f"[s2fld] {s2_field_report['message']}")
            if s2_field_report["extra"]:
                print(f"[s2fld] 额外字段（非 S1 推荐）: {s2_field_report['extra'][:5]}")
            if s2_field_report["forbidden"]:
                print(f"[s2fld] 禁用字段命中: {s2_field_report['forbidden']}")
            if not s2_field_report["pass"] and a.s2_field_block:
                print(f"[s2fld] BLOCK 模式：计入 FAIL")
        except Exception as e:
            print(f"[s2fld] S1 字段校验失败（不阻断）: {e}")
            s2_field_report = {"pass": True, "message": f"校验异常: {e}"}

    # ---- 0.2) 闸 SEM：字段语义归类硬门（2026-09-28 落地，fail-closed）----
    # 起因：KOR/fundamental17 首波跳过了「字段经济含义归类」直接进 GEM，
    # 348 条产物里 49.4% 落在货币代码 / 汇率叉乘这类**非信号字段**上
    # （三角套汇恒等式、字符串分类码）—— 语法全对、语义全废，语法闸与 gate.py
    # 都拦不住，只能靠回测烧配额。typed catalog（类型/覆盖/users）不回答
    # 「这字段能不能当信号」，必须由 s1_semantic_<ds> 台账回答。
    # 契约：
    #   缺台账  -> 默认 fail-closed exit 2（并打印生成命令），--skip-semantic-gate 放行并告警
    #   有台账  -> 命中 blocked_fields 的表达式**直接剔出候选**（不进语法闸、不进回测）
    # 产物来源：python tools/field_semantic_classify.py --region <R> --dataset <DS> --write-ledger
    # 模式解析：CLI > 环境变量 WQB_SEM_MODE > 缺省 enforce（与 WQB_INSPECT_MODE / WQB_GATE_MODE 同构）
    _sem_mode = (os.environ.get("WQB_SEM_MODE") or "enforce").strip().lower()
    if a.skip_semantic_gate or a.semantic_gate == "off":
        _sem_mode = "off"
    elif a.semantic_gate in ("warn", "enforce"):
        _sem_mode = a.semantic_gate
    if _sem_mode == "off":
        print("[sem  ] ⚠ 闸 SEM 已关闭（--skip-semantic-gate / WQB_SEM_MODE=off）："
              "非信号字段（货币代码/汇率/标识符）不会被拦截，语义废产物可能进回测烧配额。")
    sem_report = None
    if _sem_mode != "off":
        try:
            sem_report = _semantic_gate(a, campaign, items)
            items = sem_report["items"]  # 已剔除黑名单命中项
            if sem_report["ledger_missing"]:
                print("[sem  ] %s 缺 s1_semantic_%s 台账。" % (
                    "★★ 闸 SEM 阻断：" if _sem_mode == "enforce" else "[warn] 闸 SEM 告警：", a.dataset),
                    file=sys.stderr)
                print("[sem  ]    修复：python tools/field_semantic_classify.py --region %s "
                      "--dataset %s --write-ledger" % (sem_report["region"], a.dataset), file=sys.stderr)
                if _sem_mode == "enforce":
                    print("[sem  ]    确需放行加 --skip-semantic-gate / --semantic-gate warn "
                          "（会打印醒目告警并在 gate_results 留痕）。", file=sys.stderr)
                    sys.exit(2)
        except SystemExit:
            raise
        except Exception as e:
            print(f"[sem  ] 闸 SEM 异常（不阻断）: {e}")
            sem_report = None

    # ---- 1) 语法校验（PLY 括号/字段 + 算子元数/命名参数）----
    # 2026-09-07：hump(x, 0.005) 曾以"语法 8/8 PASS"过闸，平台回
    # "Invalid number of inputs : 2, should be exactly 1 input(s)." 并 CANCEL 整批
    # 8 条 multisim。PLY verifier 只查括号平衡与字段存在性，查不出"命名参数被当
    # 位置参数传"，故此处并联 op_arity（catalog 驱动，见 src/wqb/expression/op_arity.py）。
    validator = load_validator()
    arity_check = load_arity_checker()
    syntax = []
    for cid, e in items:
        r = validator.check_expression(e)
        errors = list(r.get("errors") or []) if not r.get("valid") else []
        if arity_check is not None:
            errors.extend(arity_check(e))
        else:
            errors.append("[ARITY_UNKNOWN] op_arity 不可达（本仓库 src/wqb/expression/op_arity.py 导入失败，见上方 [arity] 行），"
                          "算子元数/命名参数未校验")
        ok = not errors
        syntax.append({"id": cid, "valid": ok, "errors": errors})
        print(f"[syntax] {cid}: {'PASS' if ok else 'FAIL ' + str(errors)[:240]}")

    # ---- 2) 5 闸 + 多样性（权威实现：toolkit gate.py，从 DB 或 stdin 表达式）----
    try:
        gate_py = find_script(_TOOLKIT_CANDIDATES, "gate.py")
    except FileNotFoundError as e:
        env_error_exit(str(e))
    cmd = [sys.executable, gate_py, "--campaign-dir", campaign, "--dataset", a.dataset,
           "--wave", str(tag), "--batch-type", a.batch_type]
    if a.datasets:
        cmd.extend(["--datasets", a.datasets])
    seeded = None  # 本脚本代为入库的候选（仅这些由本脚本回写逐条状态）
    if a.from_db or (not a.candidates and not a.exprs_file and not a.expr):
        cmd.append("--from-db")
    else:
        # 兼容旧入口：把解析后的表达式 upsert 再 --from-db，避免写 cache json
        CampaignStore = _campaign_store_cls(campaign)
        settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
        region = a.region or settings.get("region")
        st = CampaignStore(_wqb_db_path(campaign))
        try:
            # 2026-09-27 R7：先入 pending，门禁逐条结论出来后再回写 gated / fail（见 _write_back_gate_status）
            st.upsert_expressions(region, str(tag), [e for _, e in items], dataset=a.dataset, status="pending")
        finally:
            st.close()
        seeded = (region, [e for _, e in items])
        cmd.append("--from-db")
    if a.skip_diversity_gate:
        cmd.append("--skip-diversity-gate")
    if a.no_cache:
        cmd.append("--no-cache")
    if a.fix:
        cmd.append("--fix")
    print(f"\n[gate ] {os.path.basename(gate_py)} --from-db --wave {tag}")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    gate_json = parse_gate_payload(r.stdout)
    # 三分终态：无结论 = ERROR（环境/实现坏了），有结论才谈 PASS/FAIL（表达式合不合格）。
    if gate_json is None:
        gate_error_exit(  # 不返回：内部 sys.exit(2)
            cmd, r, f"gate.py 退出码 {r.returncode}，stdout 未给出结论 JSON")
    if r.stderr and r.stderr.strip():  # gate.py 未崩但有告警（如入库异常）—— 同样不静默丢弃
        print("[gate ] WARN: gate.py 有 stderr 输出（不阻断）")
        _echo_block(r.stderr, "[gate ] stderr|", _GATE_ERR_TAIL)
    gate_pass = bool(gate_json["all_pass"])
    if gate_pass != (r.returncode == 0):  # gate.py 契约：exit 0 <=> all_pass=True
        print(f"[gate ] WARN: gate.py 退出码 {r.returncode} 与 all_pass={gate_pass} 不一致，以 all_pass 为准")
    if not gate_pass:
        reasons = gate_fail_reasons(gate_json)
        print("[gate ] FAIL: 闸门不过（gate.py 正常返回 all_pass=false）"
              + ("；" + "、".join(reasons) if reasons else ""))

    state_writeback = None
    if seeded:
        state_writeback = _write_back_gate_status(campaign, seeded[0], tag, gate_json, seeded[1])

    report = {
        "wave": a.wave, "dataset": a.dataset, "campaign_dir": campaign,
        "gate_exit": r.returncode,
        "syntax": {"total": len(syntax), "passed": sum(1 for s in syntax if s["valid"]),
                   "items": syntax},
        "gate": gate_json,
    }
    if state_writeback is not None:
        report["state_writeback"] = state_writeback
    if _wv_decisions:
        report["waivers"] = [d.to_dict() for d in _wv_decisions]
    if s2_field_report:
        report["s2_field_validation"] = s2_field_report

    # ---- 2.5) 体检→表达式硬门（2026-09-06 接线；2026-09-17 补 fail-closed 档）----
    # ra-pipeline 步 5 把它写成"回测前必过"，但此前整条可执行路径上零调用方。
    # 有体检包就逐条校验并计入 FAIL；没有体检包按 --inspect-mode 处理：
    #   warn（灰度默认）= 告警但放行；enforce = 缺包即整波拦截（fail-closed）。
    # 静默通过才是最坏的结果（低覆盖/厚尾/稀疏事件的预处理约束会一路裸奔到仿真）。
    inspect_report = None
    inspect_unavailable = False
    if _inspect_mode == "off":
        print("[inspect] 体检硬门已按 --inspect-mode=off 显式跳过（无把关）")
        report["field_inspect"] = {"status": "skipped", "reason": "inspect-mode=off"}
    else:
        try:
            tools_dir = os.path.dirname(os.path.abspath(__file__))
            if tools_dir not in sys.path:
                sys.path.insert(0, tools_dir)
            import field_inspect_gate as fig_mod
            passed_exprs = [e for (cid, e), s in zip(items, syntax) if s["valid"]]
            if passed_exprs:
                # region 必须走 settings.json 兜底：--region 默认 None（见其 help
                # "缺省读 settings.json"），直接用 a.region 会传空串进来，
                # 于是体检包路径拼成 field_inspect__<ds>.json，明明有包也报"未生效"。
                _region = a.region or _settings_region(campaign) or ""
                inspect_report = fig_mod.check_expressions(
                    passed_exprs, region=_region, dataset=a.dataset
                )
                print("\n" + fig_mod.format_report(inspect_report))
                report["field_inspect"] = inspect_report
                inspect_unavailable = inspect_report.get("status") == "unavailable"
            else:
                # 无有效候选 → 本闸无从校验，按"未生效"处理（enforce 下会拦截，合理）
                inspect_unavailable = True
        except Exception as e:
            print(f"[inspect] 体检硬门执行异常（不阻断）: {e}")
            report["field_inspect"] = {"status": "error", "error": str(e)}
            inspect_unavailable = True

    # 2026-09-28 默认闸定调（新数据集首波 fail-closed）：用户未显式给 --inspect-mode、
    # 也无 WQB_INSPECT_MODE 时，缺包行为自适应——新数据集首波（本区该集 0 回测）缺包
    # → 升为 enforce（预处理约束不能裸奔到仿真）；熟集缺包 → 维持灰度 warn。
    if inspect_unavailable and _inspect_mode != "off" and a.inspect_mode is None \
            and not os.environ.get("WQB_INSPECT_MODE"):
        try:
            import sqlite3 as _sq9
            _region9 = a.region or _settings_region(campaign) or ""
            _c9 = _sq9.connect(_wqb_db_path(campaign))
            try:
                _n9 = _c9.execute(
                    "SELECT COUNT(*) FROM backtest_results WHERE region=? AND dataset=?",
                    (_region9, a.dataset)).fetchone()[0]
            finally:
                _c9.close()
            if int(_n9 or 0) == 0:
                _inspect_mode = "enforce"
                print("[inspect] 新数据集首波缺体检包（本区该集 0 回测）→ 自动升为 enforce（fail-closed）")
        except Exception:
            pass  # 查不到库时维持灰度，不因环境问题拦波

    if inspect_unavailable and _inspect_mode == "enforce":
        print(
            "[inspect] ★★ fail-closed：本数据集无可用体检包（或体检执行异常），"
            "按 --inspect-mode=enforce 拦截整波，候选未回测。\n"
            "          生成体检包：python tools/gen_field_inspect_packs.py "
            "--region <REGION> --delay <D>\n"
            "          确认无包可生成时临时降级：--inspect-mode warn",
            file=sys.stderr,
        )

    # ---- 2.6) PROD 饱和闸（2026-09-07 P1-1 前移接线）----
    # 审计实证：全库可提交库存仅 MEA 3 颗，prod 饱和是全局第一瓶颈。
    # 此闸在 S3 回测前拦截饱和字段/饱和数据集（enforced 态违规计入 FAIL；
    # 无历史数据区域不阻断，但报告"未生效"）。
    prod_sat_report = None
    try:
        tools_dir = os.path.dirname(os.path.abspath(__file__))
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        import prod_saturation_gate as psg
        _region = a.region or _settings_region(campaign) or ""
        if _region:
            prod_sat_report = psg.check_wave(
                [e for _, e in items], region=_region, dataset=a.dataset
            )
            print("\n" + psg.format_report(prod_sat_report))
            report["prod_saturation"] = prod_sat_report
    except Exception as e:
        print(f"[prod-sat] PROD 饱和闸执行异常（不阻断）: {e}")
        report["prod_saturation"] = {"status": "error", "error": str(e)}

    # ---- 2.7) 闸 PF：信号族死路预检（2026-09-25 P2 落地）----
    # 判据（独立于闸 2.6 的字段热度/数据集占比）：
    #   同表达式字段集 = 已确认 prod>=0.7 死路  → 拦截
    #   同表达式字段集 = 已探明 prod<0.7 干净   → 通过（家族已探明）
    #   新信号族（无任何 prod 记录）            → WARN（建议 prod-first 探针）
    # 判据精确性：表达式字段集与 alphas 表中实测字段集精确匹配，避免字段热力交叉。
    pf_report = None
    try:
        _region = a.region or _settings_region(campaign) or ""
        if _region:
            pf_report = check_prod_family_gate(
                [e for _, e in items], region=_region, dataset=a.dataset
            )
            print("\n" + format_prod_family_report(pf_report))
            report["prod_family"] = pf_report
    except Exception as e:
        print(f"[prod-family] 闸 PF 执行异常（不阻断）: {e}")
        report["prod_family"] = {"status": "error", "error": str(e)}

    # ---- 3) 六维多样性 + 质量预估（建议2/3 落地；仅对语法通过候选，避免噪声）----
    quality_block_ids = []
    if getattr(a, "batch_type", "explore") in ("repair", "probe") and not a.skip_quality:
        print(f"[qp   ] batch_type={a.batch_type}：跳过质量预估标注（修复/探针批以实测为准）")
        a.skip_quality = True
    if not a.skip_quality:
        try:
            tools_dir = os.path.dirname(os.path.abspath(__file__))
            if tools_dir not in sys.path:
                sys.path.insert(0, tools_dir)
            import pool_diversity as pd_mod
            import quality_predict as qp_mod
            import sqlite3 as _sq
            passed_exprs = [e for (cid, e), s in zip(items, syntax) if s["valid"]]
            # 2026-09-13：pool_diversity 已重写为多维标签体系（skeleton_tags），旧 assess
            # 接口被移除 —— 此处降级跳过六维展示（不阻断门禁），保留新版可用的兼容路径。
            _assess = getattr(pd_mod, "assess", None) or getattr(pd_mod, "assess_multidimensional", None)
            if _assess is None:
                print("\n[div  ] pool_diversity.assess 不存在（新版已重写），六维报告跳过")
                report["diversity"] = {"skipped": True, "reason": "assess removed in pooled rewrite"}
            else:
                div_report = _assess(passed_exprs, region=a.region)
                report["diversity"] = div_report
                if div_report.get("issues"):
                    print("\n[div  ] 六维多样性风险:")
                    for it in div_report["issues"]:
                        print(f"        - {it}")
                elif div_report.get("operator_stats"):
                    print(f"\n[div  ] 六维多样性 PASS（算子熵={div_report['operator_stats']['entropy']}, "
                          f"同质占比={div_report['structural_similarity']['homog_ratio']:.0%}）")
                else:
                    print("\n[div  ] 新版多样性报告（格式已更新）")
            
            # 2026-09-04 新增：算子类别覆盖检查（Logical/Group/Vector 至少 1 个）
            import re as _re2
            def _extract_all_operators(expr: str) -> set:
                """提取表达式中所有算子（函数名）。"""
                return set(_re2.findall(r"([a-z_]+)\(", expr))
            
            OP_CATEGORIES = {
                "Logical": {"or", "and", "not", "is_nan", "less", "equal", "greater", "if_else", "not_equal", "less_equal", "greater_equal"},
                "Group": {"group_mean", "group_rank", "group_backfill", "group_scale", "group_count", "group_zscore", "group_std_dev", "group_sum", "group_neutralize", "group_cartesian_product"},
                "Vector": {"vec_min", "vec_count", "vec_sum", "vec_max", "vec_avg", "vec_stddev", "vec_range"},
                "Time Series": {"ts_corr", "ts_zscore", "ts_returns", "ts_product", "ts_std_dev", "ts_backfill", "days_from_last_change", "last_diff_value", "ts_scale", "ts_step", "ts_sum", "ts_av_diff", "ts_kurtosis", "ts_mean", "ts_arg_max", "ts_rank", "ts_ir", "ts_delay", "ts_quantile", "ts_count_nans", "ts_covariance", "ts_decay_linear", "ts_arg_min", "ts_regression", "ts_max_diff", "kth_element", "hump", "ts_delta"},
                "Cross Sectional": {"winsorize", "rank", "zscore", "scale", "normalize", "quantile"},
                "Arithmetic": {"add", "multiply", "sign", "subtract", "pasteurize", "log", "max", "abs", "divide", "min", "signed_power", "inverse", "sqrt", "reverse", "power", "densify"},
            }
            
            all_ops = set()
            for e in passed_exprs:
                all_ops.update(_extract_all_operators(e))
            
            category_coverage = {}
            for cat, ops in OP_CATEGORIES.items():
                covered = ops & all_ops
                category_coverage[cat] = {"covered": len(covered), "total": len(ops), "ops": sorted(covered)}
            
            report["operator_category_coverage"] = category_coverage
            
            # 硬闸：Logical/Group/Vector 至少 1 个
            logical_ok = category_coverage["Logical"]["covered"] >= 1
            group_ok = category_coverage["Group"]["covered"] >= 1
            vector_ok = category_coverage["Vector"]["covered"] >= 1
            
            # 2026-09-04 优化：MATRIX 数据集豁免 Vector 类别（无 VECTOR 字段可用）
            dataset_data_type = None
            try:
                import sqlite3 as _sq2
                conn_tmp = _sq2.connect(_wqb_db_path(campaign))
                row_tmp = conn_tmp.execute(
                    "SELECT data_type FROM datasets WHERE name=? LIMIT 1",
                    (a.dataset,)
                ).fetchone()
                conn_tmp.close()
                if row_tmp:
                    dataset_data_type = row_tmp[0]
            except Exception:
                pass
            
            vector_required = dataset_data_type != "MATRIX"  # MATRIX 数据集豁免 Vector
            vector_ok = category_coverage["Vector"]["covered"] >= 1 if vector_required else True

            # 2026-09-08：Logical 由硬闸降为条件闸。
            # 依据 859 条过闸样本——if_else 出现率仅 5.1%，trade_when/bucket 未进前 22；
            # 而 group_rank 32.0% / vec_avg 12.6%。强制 Logical 等于强制一槽落在低过闸率区。
            # 只有事件型数据集（有明确事件时点）才把 Logical 缺失判 FAIL，其余出 WARNING。
            logical_required = False
            try:
                from operator_coverage import is_event_type_dataset  # toolkit _lib
                _field_names = None
                try:
                    conn_f = _sq2.connect(_wqb_db_path(campaign))
                    _field_names = [r[0] for r in conn_f.execute(
                        "SELECT f.field_name FROM fields f JOIN datasets d ON d.id=f.dataset_id "
                        "WHERE d.name=?", (a.dataset,)).fetchall()]
                    conn_f.close()
                except Exception:
                    pass
                logical_required = bool(is_event_type_dataset(
                    dataset_name=a.dataset, field_names=_field_names))
            except Exception:
                logical_required = False  # 判不准就不升闸（代价不对称：误升会压垮 sharpe）

            hard_missing = []
            if not group_ok:
                hard_missing.append("Group")
            if not vector_ok:
                hard_missing.append("Vector")
            if logical_required and not logical_ok:
                hard_missing.append("Logical")

            if hard_missing:
                report["operator_category_gate"] = {
                    "pass": False,
                    "missing": hard_missing,
                    "logical_required": logical_required,
                    "message": f"算子类别覆盖不足：缺 {', '.join(hard_missing)} 类别"
                                f"（Group/Vector 必须；Logical 仅事件型数据集必须）"
                }
                print(f"[opcat][INFO] 算子类别覆盖不足（提示性，不计入 FAIL）：缺 {', '.join(hard_missing)} 类别")
                print(f"        Logical: {category_coverage['Logical']['covered']}/{category_coverage['Logical']['total']}"
                      f"{'（事件型数据集，必须）' if logical_required else '（非事件型，不强制）'}, "
                      f"Group: {category_coverage['Group']['covered']}/{category_coverage['Group']['total']}, "
                      f"Vector: {category_coverage['Vector']['covered']}/{category_coverage['Vector']['total']}")
            else:
                warns = []
                if not logical_ok and not logical_required:
                    warns.append("Logical")
                report["operator_category_gate"] = {"pass": True, "warnings": warns,
                                                   "logical_required": logical_required}
                print(f"[opcat] 算子类别覆盖 PASS（Logical {category_coverage['Logical']['covered']}/11, "
                      f"Group {category_coverage['Group']['covered']}/10, Vector {category_coverage['Vector']['covered']}/7）")
                if warns:
                    print(f"[opcat] WARNING：本波无 Logical 类算子。非事件型数据集不强制"
                          f"（if_else 在 859 条过闸样本中仅占 5.1%），仅提示。")
            settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
            qregion = a.region or settings.get("region")
            qconn = _sq.connect(_wqb_db_path(campaign))
            try:
                q_results, _ = qp_mod.predict_all([(e, a.dataset) for e in passed_exprs], qregion, qconn)
            finally:
                qconn.close()
            by_expr = {qr["expr"]: qr for qr in q_results}  # expr 被截断 120 字符，全量表达式前缀匹配
            qp_summary = {"direct_submit": 0, "combo_candidate": 0, "weak_signal": 0,
                          "expected_block": 0, "hard_reject": 0, "blocked": []}
            for (cid, e), s in zip(items, syntax):
                if not s["valid"]:
                    continue
                qr = by_expr.get(e[:120])
                if not qr:
                    continue
                v = qr["verdict"]
                if v == "DIRECT_SUBMIT":
                    qp_summary["direct_submit"] += 1
                elif v == "COMBO_CANDIDATE":
                    qp_summary["combo_candidate"] += 1
                elif v == "WEAK_SIGNAL":
                    qp_summary["weak_signal"] += 1
                elif v == "HARD_REJECT":
                    qp_summary["hard_reject"] += 1
                    quality_block_ids.append(cid)
                    qp_summary["blocked"].append({"id": cid, "reasons": qr["reasons"], "verdict": v})
                    print(f"[qp   ][INFO] ADVISORY_HARD {cid}: {'; '.join(qr['reasons'])}（建议性标注，不判 FAIL）")
                else:  # EXPECTED_BLOCK
                    qp_summary["expected_block"] += 1
                    quality_block_ids.append(cid)
                    qp_summary["blocked"].append({"id": cid, "reasons": qr["reasons"], "verdict": v})
                    print(f"[qp   ][INFO] ADVISORY {cid}: {'; '.join(qr['reasons'])}（建议性标注，不判 FAIL）")
            report["quality_predict"] = qp_summary
            print(f"[qp   ] 质量预估（INFO 建议层，2026-09-28 降级——实测把真实过闸者/ACTIVE 原式也判 BLOCK）: "
                  f"DIRECT={qp_summary['direct_submit']} COMBO={qp_summary['combo_candidate']} "
                  f"WEAK={qp_summary['weak_signal']} ADV_BLOCK={qp_summary['expected_block']} "
                  f"ADV_HARD={qp_summary['hard_reject']}"
                  + ("（--quality-block：计入 FAIL）" if a.quality_block else "（仅标注）"))
        except Exception as e:
            report["quality_predict"] = {"error": str(e)}
            print(f"[qp   ] 质量预估阶段失败（不阻断门禁）: {e}")

    # ---- 3.5) 参数变体聚类（2026-09-02 优化点⑤：同骨架同字段仅差参数的归一簇）----
    # 背景：wave 146 三条全闸通过候选互相关 0.9933-0.9985（max_mutually_below_subset=1），
    # Mode A 参数变体不构成多颗额度。此闸在回测前识别变体簇，每簇只留 1 条。
    variant_clusters = {}
    variant_warnings = []
    if not a.skip_quality:
        import re as _re
        def _extract_skeleton(expr: str) -> str:
            """提取表达式骨架：去掉数字参数，只留结构。"""
            s = _re.sub(r'\d+\.?\d*', 'N', expr)
            s = _re.sub(r'\s+', '', s)
            return s
        def _extract_fields(expr: str) -> frozenset:
            """提取表达式中的字段名（vec_avg/vec_sum 包裹的或裸字段）。"""
            fields = set()
            for m in _re.finditer(r'vec_(?:avg|sum)\(([a-zA-Z_][\w]*)\)', expr):
                fields.add(m.group(1))
            _ops = {'rank','ts_delta','ts_mean','ts_zscore','ts_backfill','vec_avg','vec_sum',
                    'divide','subtract','add','multiply','ts_decay_linear','group_neutralize',
                    'ts_std_dev','abs','sign','log','max','min','if_else','ts_rank','scale',
                    'group_rank','ts_sum','ts_av_diff','ts_delay','ts_corr','ts_covariance',
                    'group_zscore','ts_regression','last_diff_value','kth_element','ts_arg_max',
                    'ts_arg_min','ts_max','ts_min','ts_product','inverse','signed_power','tail',
                    'trade_when','is_nan','nan_out','purify','densify','winsorize','zscore',
                    'ts_count_nans','ts_median','ts_percentile','ts_step','ts_scale','reverse',
                    'bucket','industry','sector','subindustry','market','country'}
            for tok in _re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]{3,}\b', expr):
                if tok.lower() not in _ops and not tok.isdigit():
                    fields.add(tok)
            return frozenset(fields)
        passed_items = [(cid, e) for (cid, e), s in zip(items, syntax) if s["valid"]]
        for cid, e in passed_items:
            skel = _extract_skeleton(e)
            fields = _extract_fields(e)
            key = (skel, fields)
            if key not in variant_clusters:
                variant_clusters[key] = []
            variant_clusters[key].append((cid, e))
        for key, cluster in variant_clusters.items():
            if len(cluster) > 1:
                ids = [cid for cid, _ in cluster]
                variant_warnings.append({
                    "cluster_ids": ids,
                    "count": len(cluster),
                    "skeleton_preview": cluster[0][1][:80],
                    "fields": sorted(key[1]),
                })
                print(f"[var  ] 参数变体簇 {ids}: {len(cluster)} 条同骨架同字段，建议只留 1 条")
        if variant_warnings:
            report["variant_clusters"] = variant_warnings
            print(f"[var  ] 共发现 {len(variant_warnings)} 个参数变体簇（回测前建议每簇只留 1 条）")
        else:
            print(f"[var  ] 参数变体聚类 PASS（无同骨架同字段变体）")

    def _persist_gate_report(final_all_pass=None):
        """落 gate_results。final_all_pass 非 None 时写 final verdict。

        2026-09-28 修：`store.upsert_gate_result` 取的是 `report.get("all_pass")`，
        而本函数内 all_pass 是在**这次写库之后**才算出来的 → DB 列恒为 0，
        与 report_json 里的真实判定打架。停止规则 C（`gate_results.all_pass 全 0`
        → 判区域信号族死）会因此误杀。故末尾用真实 verdict 再 upsert 一次覆盖。
        """
        try:
            _store = _campaign_store_cls(campaign)
            _settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
            _region = a.region or _settings.get("region")
            if final_all_pass is not None:
                report["all_pass"] = bool(final_all_pass)
            _st = _store(_wqb_db_path(campaign))
            try:
                _st.upsert_gate_result(_region, str(tag), a.dataset, report)
            finally:
                _st.close()
            print(f"\n[out  ] db gate_results/{_region}/{tag}/{a.dataset}"
                  + (f" all_pass={report['all_pass']}" if final_all_pass is not None else ""))
        except Exception as e:
            print(f"[out  ] gate 入库失败: {e}")

    _persist_gate_report()

    # ---- 4) 探针批模式（可选）----
    probe_report = None
    if a.probe_mode and len(items) > 2:
        try:
            tools_dir = os.path.dirname(os.path.abspath(__file__))
            if tools_dir not in sys.path:
                sys.path.insert(0, tools_dir)
            from probe_batch_mode import ProbeBatchExecutor
            # gate 阶段只做探针分配标记（结构预判），不做真实回测
            executor = ProbeBatchExecutor(
                campaign, a.dataset, 0,  # wave=0 占位，gate 阶段不需要
                datasets_extra=a.datasets or "",
                dry_run=True)
            candidates_for_probe = [{"id": cid, "expression": e} for cid, e in items]
            # 只做探针分配，不执行回测
            probe_candidates = executor.select_probe_candidates(candidates_for_probe, n=2)
            probe_report = {
                "status": "PROBE_ASSIGNED",
                "probe_ids": [c.get("id") for c in probe_candidates],
                "probe_count": len(probe_candidates),
                "total_count": len(candidates_for_probe),
                "decision_reason": "gate 阶段探针分配（回测判死走 probe_batch_mode.py）",
                "saved_quota": 0,
            }
            print(f"[probe] 探针批模式: {probe_report['status']}")
            print(f"[probe] 决策原因: {probe_report['decision_reason']}")
            if probe_report["saved_quota"] > 0:
                print(f"[probe] 节省配额: {probe_report['saved_quota']} 条")
        except Exception as e:
            print(f"[probe] 探针批模式失败（不阻断）: {e}")

    all_pass = all(s["valid"] for s in syntax) and gate_pass
    if a.quality_block and quality_block_ids:
        all_pass = False
    if gem_report and not gem_report["pass"]:
        all_pass = False
    if s2_field_report and not s2_field_report["pass"] and a.s2_field_block:
        all_pass = False
    if probe_report and probe_report["status"] == "PROBE_DEAD":
        all_pass = False
        print(f"[done ] 探针批判死数据集，整波拦截")
    # 体检硬门违规硬阻断（有体检数据才可能出现 violations；无数据不阻断）
    if inspect_report and inspect_report.get("violations"):
        all_pass = False
        print(f"[done ] 体检硬门拦截 {len(inspect_report['violations'])} 条违规候选")
    # 体检包缺失 + enforce → fail-closed 整波拦截（2026-09-17 P1-1）
    if inspect_unavailable and _inspect_mode == "enforce":
        all_pass = False
        print("[done ] 体检硬门 fail-closed 拦截：缺体检包（inspect-mode=enforce）")
    # PROD 饱和闸硬阻断（enforced 态才可能 FAIL；unavailable 不阻断）
    if prod_sat_report and prod_sat_report.get("status") == "enforced" and not prod_sat_report.get("passed", True):
        all_pass = False
        n_v = len(prod_sat_report.get("violations") or [])
        print(f"[done ] PROD 饱和闸拦截：{n_v} 条命中饱和字段"
              + ("；当前数据集整判饱和" if prod_sat_report.get("current_dataset_saturated") else ""))
    # 闸 PF 硬阻断：命中已死路信号族 → 整波拦截
    if pf_report and pf_report.get("status") == "enforced" and pf_report.get("violations"):
        all_pass = False
        n_v = len(pf_report.get("violations") or [])
        print(f"[done ] 闸 PF 拦截：{n_v} 条命中已死路信号族（prod_corr ≥0.7 已实测死路）")
    g = gate_json  # ERROR 已在调用处退出，此处 all_pass 必为 bool（不再有 None 终态）
    qp = report.get("quality_predict") or {}
    qp_note = ""
    if isinstance(qp, dict) and "error" not in qp and qp:
        qp_note = (f" 质量预估 D/C/W/B/H={qp.get('direct_submit')}/{qp.get('combo_candidate')}/"
                   f"{qp.get('weak_signal')}/{qp.get('expected_block')}/{qp.get('hard_reject')}"
                   + (f"（拦截 {len(quality_block_ids)} 条{'计入 FAIL' if a.quality_block else ' 仅标注'}）"
                      if (qp.get('expected_block') or qp.get('hard_reject')) else ""))
    gem_note = f" GEM={gem_report['gem_ratio']:.0%}" if gem_report else ""
    s2fld_note = ""
    if s2_field_report:
        cov = s2_field_report.get("coverage", 0)
        s2fld_note = f" S1字段={cov:.0%}" + ("(BLOCK)" if not s2_field_report["pass"] and a.s2_field_block else "")
    probe_note = f" Probe={probe_report['status']}" if probe_report else ""
    print(f"[done ] 语法 {report['syntax']['passed']}/{report['syntax']['total']}, "
          f"gate all_pass={str(g['all_pass']).lower()} passed={g.get('passed')}/{g.get('total')}"
          f"{qp_note}{gem_note}{s2fld_note}{probe_note} => {'PASS' if all_pass else 'FAIL'}")
    # 用**最终 verdict** 覆盖写一次（首次落库时 all_pass 尚未算出，见 _persist_gate_report 注释）
    _persist_gate_report(final_all_pass=all_pass)
    sys.exit(0 if all_pass else 1)

if __name__ == "__main__":
    import os as _os_sc; _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")  # 启动校验每进程只打一次（2026-09-19）
    # L3 写库互斥（2026-09-20）：门禁写 gate_results/expressions，与 build_wave/pipeline/harvest 排队
    _src = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
    if _src not in sys.path:
        sys.path.insert(0, _src)
    from wqb.db_write_lock import write_lock as _wlock
    with _wlock(tag="dbwrite_wave_gate", ttl_sec=1200, wait_timeout=120):
        main()
