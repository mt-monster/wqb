# -*- coding: utf-8 -*-
"""闸 SEM：字段语义归类硬门（2026-09-28 落地，fail-closed）。

从 2026-09-30 单文件 `tools/wave_gate.py` 拆出。

起因：KOR/fundamental17 首波跳过了「字段经济含义归类」直接进 GEM，
348 条产物里 49.4% 落在货币代码 / 汇率叉乘这类**非信号字段**上
（三角套汇恒等式、字符串分类码）—— 语法全对、语义全废，语法闸与 gate.py
都拦不住，只能靠回测烧配额。typed catalog（类型/覆盖/users）不回答
「这字段能不能当信号」，必须由 s1_semantic_<ds> 台账回答。

契约：
  缺台账  -> 默认 fail-closed exit 2（并打印生成命令），--skip-semantic-gate 放行并告警
  有台账  -> 命中 blocked_fields 的表达式**直接剔出候选**（不进语法闸、不进回测）
产物来源：python tools/field_semantic_classify.py --region <R> --dataset <DS> --write-ledger
"""
import json
import os
import re
import sys
from pathlib import Path

from ._paths import REPO_ROOT, _wqb_db_path


def _semantic_gate(a, campaign, items):
    """闸 SEM：字段语义归类硬门（2026-09-28）。

    读 ledger `s1_semantic_<dataset>`（由 tools/field_semantic_classify.py 产出），
    把命中 `blocked_fields`（货币代码 / 汇率换算 / 标识符 / 分类码 / 日期口径）
    的表达式**直接剔出候选**——这类表达式语法全对但语义为恒等式或字符串比较，
    语法闸与 gate.py 都拦不住，只能靠回测烧配额。

    返回 dict：{region, dataset, ledger_missing, blocked_field_count,
                removed: [(cid, expr, hit)], items: 幸存的 [(cid, expr)]}
    """
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

    sys.path.insert(0, os.path.join(REPO_ROOT, "src"))
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
    _BAD_PAT = re.compile(
        r"currency_code|cur_code|_ras\d*$|exrate|exchange_rate|^fx_|_fx_|_fx$|"
        r"gvkey|cusip|isin|sedol|ticker|iso_country|country_code|exchange_code|region_code|"
        r"fiscal_year_end|report_date|period_end|_date$|_dt$|"
        r"_share_class_|shares_outstanding_class")
    removed, keep = [], []
    for cid, e in items:
        fields = [f for f in re.findall(r"\b[a-z][a-z0-9_]{4,}\b", e or "")]
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
            conn = _dbconn()
            try:
                ph = ",".join("?" * len(ids))
                import datetime as _dt
                cur = conn.execute(
                    f"UPDATE expressions SET status='dropped', updated_at=? "
                    f"WHERE id IN ({ph}) AND region=?",
                    (_dt.datetime.now().isoformat(timespec="seconds"), *ids, region),
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
