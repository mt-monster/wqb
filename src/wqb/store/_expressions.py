# -*- coding: utf-8 -*-
"""ExpressionsMixin: expression CRUD for CampaignStore."""
from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List, Optional, Sequence

from ._common import ExprItem, _as_expr, _dumps, _loads, _now


def expression_fingerprint(expr: str) -> str:
    """表达式规范指纹：去空白 + 小写后取 sha1 前 12 位。

    2026-09-06：此前 fingerprint 完全依赖调用方传入，而绝大多数调用方不传 ——
    实测 9 924 行里 3 059 行（30.8%）为 NULL，KOR 单区就有 1 008 行。任何按
    fingerprint 做的去重/查重都会静默漏掉这三成，全库重复表达式 1 833 行（18.5%）。

    归一化口径对齐 toolkit `_lib/common.py:norm_expr`（去全部空白），另加小写，
    使 `rank(Close)` 与 `rank( close )` 同指纹。取 12 位与库中既有指纹等宽。
    """
    normalized = re.sub(r"\s+", "", expr or "").lower()
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:12]


def _expr_skeleton(expr: str) -> Optional[str]:
    """自动计算结构骨架签名（写库时缺省填充；失败返回 None，绝不阻断写入）。

    2026-09-17：实际生成链路（GEM runner → AI 调 MCP upsert_expressions）此前
    **不写 skeleton**（全库 0 行），因为唯一写入方 `gem_wave` 节点不在实际流程中。
    改在规范写入器里自动计算 → 任何路径（MCP / CLI / 批处理）落库的行都带骨架，
    生成期去重与复用率统计立即可用。
    实现复用 `wqb.expression.skeleton.structural_signature`（纯函数，零外部依赖）。
    """
    try:
        from ..expression.skeleton import structural_signature
        return structural_signature(expr)
    except Exception:
        return None


#: 纪律废弃终态（归档，不再进选波/回测/提交）。唯一允许覆盖"已回测行"（alpha_id 非空）
#: 状态的目标态：把一条已有 alpha 的行改回 pending/selected 会让它被重新烧配额回测。
TERMINAL_STATUSES = ("superseded", "dropped")

#: build_wave 选波落库后，本波未被选中且仍处于这些"待选"态的行归档为 superseded。
#: dropped/selected/gated 不在其中（纪律废弃 / 已在闸门或回测链上），alpha_id 非空行另有守卫。
UNPICKED_SUPERSEDE_FROM = ("gem", "pending", "enhanced")

#: settings_json 里的状态变更审计键。它不是回测设置——list_expressions 会把它从 settings
#: 视图里摘出来提到行顶层，防止被当作 sim settings 原样并进平台 payload。
STATUS_CHANGE_KEY = "status_change"

# 单条 UPDATE 里原地合并审计信息：settings_json 是 JSON 对象时 json_set 只动 status_change
# 这一个键（decay/neutralization/truncation 等原样保留）；NULL/空串/非法 JSON/非对象时从 {}
# 起步。json_object 里引用的 `status` 列取的是 UPDATE 前的旧值（SQL 语义），正好记 from。
_STATUS_CHANGE_SET_SQL = (
    "status=?, updated_at=?, settings_json=json_set("
    "CASE WHEN settings_json IS NOT NULL AND json_valid(settings_json)"
    "      AND json_type(settings_json)='object' THEN settings_json ELSE '{}' END, "
    f"'$.{STATUS_CHANGE_KEY}', "
    "json_object('from', status, 'to', ?, 'reason', ?, 'at', ?))"
)


def _status_change_set_params(to_status: str, reason: Optional[str], now: str) -> List[Any]:
    """与 _STATUS_CHANGE_SET_SQL 的 ? 顺序一一对应。"""
    return [to_status, now, to_status, reason, now]


class ExpressionsMixin:
    """Expression upsert/list/history methods."""

    def upsert_expressions(
        self,
        region: str,
        wave: str,
        items: Sequence[ExprItem],
        dataset: Optional[str] = None,
        status: str = "pending",
        commit: bool = True,
        source: Optional[str] = None,
    ) -> Dict[str, Any]:
        wave_id = self._ensure_wave(region, str(wave), dataset)
        now = _now()
        n = 0
        cur = self.connection.cursor()
        # 冗余列 region/wave/dataset 必须从 wave_id 关联派生，避免与父表（waves→regions/datasets）漂移
        # 2026-09-15 修复：此前 SELECT 同时选出 r.name 与 d.name 两个都叫 name 的列，
        # sqlite3.Row["name"] 取第一个 → resolved_dataset 恒等于区域名。实测全库 13 847 行里
        # 7 418 行 dataset==region（GBR wave57 写成 'GBR'，waves 表却是 pv47），
        # list_expressions(dataset=…) 全靠"旧行回退"分支才查得到。列名必须取别名。
        cur.execute(
            "SELECT r.name AS region_name, w.wave_number, d.name AS dataset_name FROM waves w "
            "JOIN regions r ON r.id=w.region_id "
            "LEFT JOIN datasets d ON d.id=w.dataset_id WHERE w.id=?",
            (wave_id,),
        )
        _wr = cur.fetchone()
        resolved_region = _wr["region_name"] if _wr else region
        resolved_wave = str(_wr["wave_number"]) if _wr else str(wave)
        resolved_dataset = _wr["dataset_name"] if _wr and _wr["dataset_name"] else (dataset or None)
        for raw in items:
            item = _as_expr(raw)
            expr = (item.get("expression") or "").strip()
            if not expr:
                continue
            st = item.get("status") or status
            settings = item.get("settings") or item.get("settings_json")
            settings_json = _dumps(settings) if isinstance(settings, (dict, list)) else settings
            cur.execute(
                "SELECT id FROM expressions WHERE wave_id=? AND expression=?",
                (wave_id, expr),
            )
            row = cur.fetchone()
            vals = (
                # 调用方没给就现算，杜绝 NULL 指纹（去重全靠它）
                item.get("fingerprint") or expression_fingerprint(expr),
                st,
                item.get("alpha_id"),
                item.get("sharpe"),
                item.get("fitness"),
                item.get("margin"),
                item.get("turnover"),
                resolved_region,
                resolved_wave,
                resolved_dataset,
                settings_json,
                # ---- 2026-09-17 新增：provenance 与生成期属性 ----
                # source：此前**没有任何代码路径写这一列** → 全库 89.8% 为 NULL，
                #   GEM 产出无法辨识（按 source 过滤只能看到一个月前的语料），
                #   也无法做 phased/skeleton 模式的 A/B。现按「条目优先、函数参数兜底」写入。
                item.get("source") or source,
                item.get("bucket"),
                # skeleton：条目优先；缺省**自动计算**（2026-09-17 补）。
                # 此前只有 gem_wave 节点写这一列，而该节点不在实际生成链路中
                # （实际链路 = GEM runner → AI 调 MCP upsert）→ 全库 0 行。
                # 规格：字段→F、数字→N、算子按「后紧跟 (」识别，纯函数零成本。
                item.get("skeleton") or _expr_skeleton(expr),
                1 if item.get("selected") else 0,
                item.get("expected_exposure") or item.get("exposure"),
                now,
            )
            if row:
                # 2026-09-09 D12 修复：dropped/superseded 是纪律废弃终态，
                # build_wave 重选时不得被无条件 UPDATE 覆盖回 selected。
                # 此前 upsert 的 UPDATE 分支无条件写 status，Agent 手动 dropped 的
                # 零 alpha 骨架（iso_week_number 日历哑字段）每次重选波都复活。
                _existing_id = int(row[0])
                cur.execute("SELECT status FROM expressions WHERE id=?", (_existing_id,))
                _cur_status = (cur.fetchone() or [None])[0]
                if _cur_status in ("dropped", "superseded") and st == "selected":
                    continue  # 保留废弃终态，不计入本波（n 不自增）
                cur.execute(
                    """UPDATE expressions SET fingerprint=?, status=?, alpha_id=?,
                       sharpe=?, fitness=?, margin=?, turnover=?, region=?, wave=?,
                       dataset=?, settings_json=?, source=?, bucket=?, skeleton=?,
                       selected=?, expected_exposure=?, updated_at=? WHERE id=?""",
                    vals + (_existing_id,),
                )
            else:
                cur.execute(
                    """INSERT INTO expressions
                       (wave_id, expression, fingerprint, status, alpha_id, sharpe,
                        fitness, margin, turnover, region, wave, dataset,
                        settings_json, source, bucket, skeleton, selected,
                        expected_exposure, created_at, updated_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (wave_id, expr) + vals + (now,),
                )
            n += 1
        cur.execute(
            "UPDATE waves SET expression_count=?, updated_at=? WHERE id=?",
            (n, now, wave_id),
        )
        # commit=False 让调用方把本次 upsert 与后续写（如 supersede_unpicked）合成一个事务
        if commit:
            self.connection.commit()
        return {"n": n, "region": region, "wave": str(wave), "dataset": dataset}

    def set_expression_status(
        self,
        region: str,
        wave: str,
        to_status: str,
        ids: Optional[Sequence[int]] = None,
        from_status: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        """批量改 expressions.status（单条 UPDATE，region+wave 限定）。

        2026-09-12（GBR wave57 实测）：Agent 要把一波 43 条候选整体改状态，唯一写路径是
        upsert_expressions —— 必须把 43 条完整表达式原样回传，服务端 3 ms，MCP 侧却要吐
        3-4k token；成本在载荷不在库。本方法只收 id 列表或状态过滤，一条 UPDATE 落地，
        回传只有计数。

        规则：
          - ids / from_status 至少给一个（同给取交集）；无过滤的全波改状态没有正当场景，
            只会是误操作，直接拒绝（ValueError）
          - 已回测行（alpha_id 非空）受保护：只有 to_status 是终态归档（TERMINAL_STATUSES）
            才允许改，否则本次 UPDATE 自动跳过它们并以 n_protected 回报（不静默）
          - reason 连同 from/to/at 合并进 settings_json.status_change（json_set 原地合并，
            既有 decay/neutralization 等设置键不动）
        """
        id_list = [int(i) for i in (ids or [])]
        if not id_list and not from_status:
            raise ValueError("set_expression_status: ids 或 from_status 至少给一个（拒绝无过滤全波改状态）")
        to_status = (to_status or "").strip()
        if not to_status:
            raise ValueError("set_expression_status: to_status 不能为空")
        where = "region=? AND wave=?"
        params: List[Any] = [region, str(wave)]
        if id_list:
            where += f" AND id IN ({','.join('?' * len(id_list))})"
            params += id_list
        if from_status:
            where += " AND status=?"
            params.append(from_status)
        cur = self.connection.cursor()
        n_protected = 0
        if to_status not in TERMINAL_STATUSES:
            cur.execute(
                f"SELECT COUNT(*) FROM expressions WHERE {where} "
                "AND alpha_id IS NOT NULL AND alpha_id<>''",
                params,
            )
            n_protected = int(cur.fetchone()[0])
            where += " AND (alpha_id IS NULL OR alpha_id='')"
        now = _now()
        cur.execute(
            f"UPDATE expressions SET {_STATUS_CHANGE_SET_SQL} WHERE {where}",
            _status_change_set_params(to_status, reason, now) + params,
        )
        n_updated = int(cur.rowcount)
        self.connection.commit()
        return {
            "n_updated": n_updated,
            "n_protected": n_protected,
            "n_requested": len(id_list) if id_list else None,
            "region": region,
            "wave": str(wave),
            "from_status": from_status,
            "to_status": to_status,
        }

    def supersede_unpicked(
        self,
        region: str,
        wave: str,
        keep: Sequence[str],
        reason: Optional[str] = None,
        from_statuses: Sequence[str] = UNPICKED_SUPERSEDE_FROM,
        commit: bool = True,
    ) -> int:
        """把本波未被选中、仍处于待选态的行归档为 superseded（单条 UPDATE）。

        build_wave 选波的"权威化"：此前 upsert 只把 picked 写成 selected，落选的 gem/pending
        /enhanced 行原样留在波里，下游 pipeline/gate 按波读表达式时分不清哪些是本波真正的
        选集（GBR wave57 实测痛点）。规则与 build_wave 的候选读取口径对齐：
          - keep 里的表达式（按原文精确匹配，与 upsert 的 UNIQUE(wave_id, expression) 同口径）不动
          - 只动 from_statuses（默认 gem/pending/enhanced）；dropped/selected/gated 等一律不碰
          - alpha_id 非空行（已回测）一律不碰，即便 superseded 是终态
          - 范围只按 region+wave：一波只有一个数据集（waves.dataset_id），且 2026-09-15 前
            写入的行 dataset 列是区域名（见 upsert_expressions 的列名修复），按 dataset
            过滤会把这些旧行静默漏掉
        返回归档行数。commit=False 供调用方与 upsert_expressions(commit=False) 合成一个事务。
        """
        keep_list = [k for k in dict.fromkeys(keep or []) if k]
        statuses = [s for s in from_statuses if s and s not in TERMINAL_STATUSES]
        if not statuses:
            return 0
        where = (
            "region=? AND wave=? AND (alpha_id IS NULL OR alpha_id='') "
            f"AND status IN ({','.join('?' * len(statuses))})"
        )
        params: List[Any] = [region, str(wave)] + statuses
        if keep_list:
            where += f" AND expression NOT IN ({','.join('?' * len(keep_list))})"
            params += keep_list
        cur = self.connection.cursor()
        cur.execute(
            f"UPDATE expressions SET {_STATUS_CHANGE_SET_SQL} WHERE {where}",
            _status_change_set_params("superseded", reason, _now()) + params,
        )
        n = int(cur.rowcount)
        if commit:
            self.connection.commit()
        return n

    def list_expressions(
        self,
        region: str,
        wave: str,
        dataset: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM expressions WHERE region=? AND wave=?"
        params: List[Any] = [region, str(wave)]
        if dataset:
            sql += " AND (dataset=? OR dataset IS NULL)"
            params.append(dataset)
        if status:
            sql += " AND status=?"
            params.append(status)
        else:
            # 默认排除 superseded（2026-09-01：表达式更新留档态不参与选波/回测）
            # + dropped（2026-09-09 D12：纪律废弃终态）。此前只排 superseded，
            # pipeline.py S3 回测无 status 过滤 → Agent dropped 的零 alpha 骨架
            # （iso_week_number 日历哑字段）照样烧回测配额。
            sql += " AND status NOT IN ('superseded', 'dropped')"
        sql += " ORDER BY id"
        cur = self.connection.cursor()
        cur.execute(sql, params)
        out = []
        for row in cur.fetchall():
            d = dict(row)
            if d.get("settings_json"):
                d["settings"] = _loads(d["settings_json"])
                # 审计键提到行顶层：settings 视图必须只剩回测设置——tools_sim /
                # pipeline per-item overrides 会把 settings 的每个键原样并进平台 payload。
                if isinstance(d["settings"], dict) and STATUS_CHANGE_KEY in d["settings"]:
                    d[STATUS_CHANGE_KEY] = d["settings"].pop(STATUS_CHANGE_KEY)
            out.append(d)
        if out:
            return out
        # fallback: old rows without denormalized region/wave
        rid = None
        cur.execute("SELECT id FROM regions WHERE name=?", (region,))
        r = cur.fetchone()
        if not r:
            return []
        rid = int(r[0])
        cur.execute(
            "SELECT id FROM waves WHERE region_id=? AND wave_number=?",
            (rid, str(wave)),
        )
        w = cur.fetchone()
        if not w:
            return []
        cur.execute(
            "SELECT * FROM expressions WHERE wave_id=? ORDER BY id",
            (int(w[0]),),
        )
        return [dict(row) for row in cur.fetchall()]

    def history_expressions(
        self,
        region: str,
        exclude_waves: Optional[Sequence[str]] = None,
        include_generated: bool = True,
    ) -> List[str]:
        """本区已出现过的表达式，供 build_wave 做全历史去重。

        2026-09-06：原实现无条件排除 `status in ('gem','raw')`。那是个过宽的钝器 ——
        它想解决的是"别把本波自己的输入过滤掉"，而这件事 `exclude_waves`
        （当前波 + `s2_<dataset>_d<delay>` 源波）已经精确解决了。按状态全局排除的
        代价是：**其他波次**生成过的表达式对去重完全隐形，同一条可以一波一波重复生成。

        实测：1 681 条 gem/raw 行里有 759 条与本区其他行重复（EUR 350 / IND 213 /
        KOR 182），正是全库 18.5% 重复率的主要来源之一。

        `include_generated=False` 可回到旧行为（应急逃生用，会重新放大重复）。
        """
        cur = self.connection.cursor()
        cur.execute(
            "SELECT expression, wave, status FROM expressions WHERE region=?",
            (region,),
        )
        skip = {str(w) for w in (exclude_waves or [])}
        skip_status = set() if include_generated else {"gem", "raw"}
        out = []
        for r in cur.fetchall():
            if r[1] and str(r[1]) in skip:
                continue
            if skip_status and (r[2] or "") in skip_status:
                continue
            if r[0]:
                out.append(r[0])
        return out

    save_wave_expressions = upsert_expressions
    load_wave_expressions = list_expressions
