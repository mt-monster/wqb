# -*- coding: utf-8 -*-
"""field_gate.py - 组合前字段可用性本地闸（可复用库）。

数据源（优先级从高到低）：
  1. fields 表 verified=1 且 verified_context 匹配该区域上下文 → 可用（已批量验证）
  2. external_fields 表 verified=1 → 可用（外部/跨区字段，已实测）
  3. 平台内置字段（open/close/sector 等）→ 可用
  4. 其余 → 未验证（拦截或告警）

设计原则：
  - 纯本地查询，0 API 调用，毫秒级。
  - 作为 expr_lint 的 fields_gate json 白名单之外的**补充闸**：
    json 白名单管"类型/覆盖", 本闸管"该字段在当前区域上下文是否真的可用"(token-name 隐患)。
"""
import os
import sqlite3

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "wqb.db")

PLATFORM_FIELDS = {
    'open', 'high', 'low', 'close', 'vwap', 'returns', 'adv20', 'adv60',
    'cap', 'sharesout', 'volume', 'cap3', 'rank', 'sector', 'industry',
    'subindustry', 'country', 'exchange', 'sector_country',
    'industry_country', 'sector_exchange', 'date', 'bucket',
}


def _connect(db_path=None):
    return sqlite3.connect(db_path or DB)


def load_verified_fields(region, context_prefix=None, db_path=None):
    """加载某区域已验证可用字段集合（fields.verified=1）。

    context_prefix: 形如 "IND/TOP500/D1"；若给了则只认该 context 验证过的字段，
                    否则认该区域所有 verified=1 字段。
    返回 set(field_name)。
    """
    conn = _connect(db_path)
    cur = conn.cursor()
    q = """SELECT DISTINCT f.field_name, f.verified_context FROM fields f
           JOIN datasets d ON d.id=f.dataset_id JOIN regions rg ON rg.id=d.region_id
           WHERE rg.name=? AND f.verified=1"""
    rows = cur.execute(q, (region,)).fetchall()
    out = set()
    for name, ctx in rows:
        if context_prefix and ctx != context_prefix:
            continue
        out.add(name)
    conn.close()
    return out


def load_external_verified(region, db_path=None):
    """加载某区域已实测可用的外部/跨区字段（external_fields.verified=1）。"""
    conn = _connect(db_path)
    cur = conn.cursor()
    out = {r[0] for r in cur.execute(
        "SELECT field_name FROM external_fields WHERE region=? AND verified=1",
        (region,))}
    conn.close()
    return out


def load_external_known(region, db_path=None):
    """加载某区域所有已知外部字段（不论 verified），供提示用。"""
    conn = _connect(db_path)
    cur = conn.cursor()
    out = {r[0]: (r[1], r[2]) for r in cur.execute(
        "SELECT field_name, in_local_db, source_regions FROM external_fields WHERE region=?",
        (region,))}
    conn.close()
    return out


def check_expression_fields(field_names, region, context_prefix=None, db_path=None):
    """检查一组字段在该区域上下文的可用性。

    返回 dict:
      ok:       [已验证可用字段]
      external: [在外部表但尚未实测 verified 的字段]（需提示先实测）
      unknown:  [完全未知字段]（token-name 隐患，拦截）
    """
    verified = load_verified_fields(region, context_prefix, db_path)
    ext_verified = load_external_verified(region, db_path)
    ext_known = load_external_known(region, db_path)

    ok, external, unknown = [], [], []
    for name in field_names:
        if name in PLATFORM_FIELDS:
            ok.append(name)
        elif name in verified or name in ext_verified:
            ok.append(name)
        elif name in ext_known:
            external.append(name)
        else:
            unknown.append(name)
    return {"ok": ok, "external": external, "unknown": unknown}
