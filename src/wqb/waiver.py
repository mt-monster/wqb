# -*- coding: utf-8 -*-
"""wqb.waiver — 闸「放行 / 豁免」台账协议的唯一实现（skills 审查 X-8 / RA-28 / RA-117 / RD-01）。

背景（2026-09-29 审查）：SKILL.md 里「可显式降级，但必须在台账记因 / 留痕 / 豁免」共 17 处，没有一处给
键名、字段、有效期、谁有权批准。仓库里唯一真在用的两个放行键（``stop_rules_override`` /
``backlog_gate_override``）在 ``campaign.py`` 里各手写一份 SQL + JSON + 日期比较（逐字重复），并且：
缺 ``until`` 就是**永久放行**、没有批准人、不进任何报告首行——放行是静默的。

协议
----
键：``waiver_<gate>_<region>_<wave|all>``（ledger_kv 的 region 列 = ``<region>``）。值（JSON 对象）::

    {"gate": "semantic",              # 闸 id，必须在 GATE_POLICIES 注册
     "reason_code": "NO_INPUT_AVAILABLE",   # REASON_CODES 枚举
     "reason": "该数据集无描述文，s1_semantic 无法生成",   # 人话原因（USER_INSTRUCTION 须引用指令原话）
     "evidence": "ledger:GBR/s1_semantic_x1 缺失；尝试 field_semantic_classify 报 ...",   # 键 / id / 命令输出
     "approved_by": "agent",          # user | agent；受 GATE_POLICIES[gate].approvers 约束
     "created_at": "2026-09-29",
     "expires_at": "2026-10-03"}      # 必填；含当天；最长有效期受 GATE_POLICIES[gate].max_days 约束

读取顺序：``waiver_<gate>_<region>_<wave>`` → ``waiver_<gate>_<region>_all`` → 旧键（``legacy_key``）。
旧键 ``{"reason","until"}`` 继续被识别（``until`` → ``expires_at``），**缺 ``until`` 仍放行但标 NO_EXPIRY
告警**——不静默改变现有行为，只让永久放行变得可见；新写入一律用新键。

红线：``RED_LINES`` 里的项没有 waiver——不管谁批准都不能豁免（提交前的用户确认、凭据外发……）。
``load`` / ``check_skip`` 对红线直接返回 INVALID。

使用
----
* 闸代码：``load(conn, "stop_rules", region)`` → ``Waiver | None``；``ACTIVE`` 才放行，并把 ``to_dict()`` 放进
  gate 结果，横幅由 ``banner_lines`` 统一生成（不要各闸自己拼）。
* CLI 跳过开关（``--skip-semantic-gate`` 等）：``check_skip``（缺省 warn：无 waiver 只告警；
  ``WQB_WAIVER_MODE=enforce`` 时无 waiver 即拒）。
* 写 waiver：``build_payload`` 生成并校验，agent 走 ``mcp__wqb-db__upsert_ledger_key``；脚本走 ``record``。
"""
from __future__ import annotations

import datetime as _dt
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

WAIVER_PREFIX = "waiver_"
ALL_WAVES = "all"

#: 放行原因枚举（reason_code）。自由文本只放 ``reason``，不进枚举。
REASON_CODES: Dict[str, str] = {
    "USER_INSTRUCTION": "用户显式指令（reason 须引用指令原话或日期；approved_by 必须是 user）",
    "REPAIR_BATCH": "修复批：候选按设计复用同族骨架，多样性/覆盖类闸不适用",
    "PROBE_BATCH": "探针批：为取证刻意窄化，覆盖/多样性类闸不适用",
    "NO_INPUT_AVAILABLE": "前置输入无法产出（如无体检包 / 无语义台账且无法生成），evidence 须记尝试过程",
    "PLATFORM_UNAVAILABLE": "平台侧能力或端点当前不可用，evidence 须留响应",
    "SUPERSEDED_BY_EVIDENCE": "有更强证据取代该闸的前提（evidence 必填）",
}
#: 必须带 evidence 的 reason_code
EVIDENCE_REQUIRED = frozenset({"SUPERSEDED_BY_EVIDENCE", "NO_INPUT_AVAILABLE", "PLATFORM_UNAVAILABLE"})

APPROVERS = ("user", "agent")

#: 不可豁免的红线（任何人批准都无效）。文档「不可覆盖红线」表以此为准（tests/unit/test_waiver.py 守）。
RED_LINES: Dict[str, str] = {
    "submit_user_confirmation": "POST /alphas/{id}/submit 前的用户明确确认——不可逆动作，不存在「豁免确认」",
    "credentials": "凭据只在 world-quant-brain-mcp/.env：禁止读取、打印、提交、外发",
    "platform_terms": "平台使用条款与限额（提交配额、并发上限）——平台侧强制，本地无豁免权",
}


@dataclass(frozen=True)
class GatePolicy:
    gate: str
    title: str
    approvers: Tuple[str, ...]
    max_days: int
    legacy_key: Optional[str] = None
    #: 对应的 CLI / 环境逃生口（文档与横幅引用）
    flags: Tuple[str, ...] = ()
    #: 以下三项只服务文档总表（`render_switch_table`，嵌入 INDEX.md；skills 审查 X-6）
    layer: str = ""            # 所在层
    default: str = ""          # 缺省行为
    flip: str = "—"            # 含日期翻转时写明日期与登记号（docs/time_bombs.json）


#: 可豁免的闸。新增可豁免闸必须先在这里登记（登记即声明批准人与最长有效期）。
GATE_POLICIES: Dict[str, GatePolicy] = {p.gate: p for p in (
    GatePolicy("stop_rules", "区域停止规则闸（规则 A / B1 / B2）", ("user",), 30, "stop_rules_override",
               ("WQB_DISABLE_STOP_RULES_GATE=1（仅测试隔离）",),
               layer="开波区域闸（节点一律拦截；CLI 随 gate-mode）", default="常开"),
    GatePolicy("backlog", "区域积压闸（conversion / pending+gated / 未消费）", ("user",), 30, "backlog_gate_override",
               ("WQB_DISABLE_BACKLOG_GATE=1（仅测试隔离）",),
               layer="开波区域闸（节点一律拦截；CLI 随 gate-mode）", default="常开"),
    GatePolicy("region_gates", "开波区域闸整体降级（catalog / signal_floor / stop_rules / backlog）", ("user",), 7, None,
               ("--gate-mode warn|off", "WQB_GATE_MODE=warn|off"),
               layer="wave_gate / build_wave CLI", default="warn 至 2026-10-11，之后 enforce",
               flip="**2026-10-12**（TB-02）"),
    GatePolicy("inspect", "字段体检硬门（缺体检包）", ("user", "agent"), 7, None,
               ("--inspect-mode off|warn", "WQB_INSPECT_MODE"),
               layer="wave_gate 内置", default="warn；新数据集首波自适应 enforce"),
    GatePolicy("semantic", "闸 SEM 字段语义归类", ("user", "agent"), 7, None,
               ("--skip-semantic-gate", "--semantic-gate off|warn", "WQB_SEM_MODE"),
               layer="wave_gate 内置", default="enforce（缺台账 exit 2）"),
    GatePolicy("diversity", "gate.py 闸 6 多样性契约", ("user", "agent"), 3, None,
               ("--skip-diversity-gate",),
               layer="gate.py 闸 6", default="常开（repair / probe 批豁免）"),
    GatePolicy("prod_family", "闸 PF 信号族死路预检", ("user", "agent"), 3, None,
               ("--no-prod-family-gate",),
               layer="wave_gate 内置", default="开"),
)}

#: wave_gate CLI 开关 → 闸 id（`tools/wave_gate.py` 用它把「开了哪些逃生口」翻成 waiver 检查）
FLAG_TO_GATE: Dict[str, str] = {
    "--skip-diversity-gate": "diversity",
    "--skip-semantic-gate": "semantic",
    "--semantic-gate off": "semantic",
    "--inspect-mode off": "inspect",
    "--no-prod-family-gate": "prod_family",
}

MODES = ("off", "warn", "enforce")
DEFAULT_MODE = "warn"

#: 状态
ACTIVE, EXPIRED, INVALID = "ACTIVE", "EXPIRED", "INVALID"


class WaiverError(ValueError):
    """build_payload / record 校验失败。"""


@dataclass
class Waiver:
    gate: str
    region: str
    wave: str
    reason_code: str = ""
    reason: str = ""
    evidence: Any = None
    approved_by: str = ""
    created_at: Optional[str] = None
    expires_at: Optional[str] = None
    source_key: str = ""
    legacy: bool = False
    status: str = INVALID
    problems: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def active(self) -> bool:
        return self.status == ACTIVE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gate": self.gate, "region": self.region, "wave": self.wave,
            "reason_code": self.reason_code, "reason": self.reason, "evidence": self.evidence,
            "approved_by": self.approved_by, "created_at": self.created_at,
            "expires_at": self.expires_at, "source_key": self.source_key, "legacy": self.legacy,
            "status": self.status, "problems": list(self.problems), "warnings": list(self.warnings),
        }

    def summary(self) -> str:
        who = self.approved_by or "?"
        until = self.expires_at or "无到期日"
        tag = f"{self.reason_code or 'LEGACY'}/{who}"
        return f"{self.source_key}（{tag}，至 {until}）：{self.reason}"


# ---------------------------------------------------------------- 键


def waiver_key(gate: str, region: str, wave: Optional[Any] = None) -> str:
    """``waiver_<gate>_<region>_<wave|all>``。region 统一大写；wave 缺省 ``all``。"""
    w = ALL_WAVES if wave in (None, "", 0, "0") else str(wave)
    return f"{WAIVER_PREFIX}{gate}_{str(region).upper()}_{w}"


def parse_key(key: str) -> Optional[Tuple[str, str, str]]:
    """``waiver_<gate>_<region>_<wave>`` → (gate, region, wave)；不是 waiver 键 / 闸未注册 → None。

    gate 名含下划线（``stop_rules``），靠已注册闸名做最长前缀匹配；region 不含下划线，余下全是 wave。
    """
    if not key.startswith(WAIVER_PREFIX):
        return None
    rest = key[len(WAIVER_PREFIX):]
    for gate in sorted(GATE_POLICIES, key=len, reverse=True):
        if rest.startswith(gate + "_"):
            tail = rest[len(gate) + 1:]
            region, _, wave = tail.partition("_")
            if region and wave:
                return gate, region, wave
    return None


# ---------------------------------------------------------------- 校验


def _parse_date(s: Any) -> Optional[_dt.date]:
    if isinstance(s, _dt.datetime):
        return s.date()
    if isinstance(s, _dt.date):
        return s
    if not isinstance(s, str) or not s.strip():
        return None
    text = s.strip()
    try:
        return _dt.date.fromisoformat(text[:10])
    except ValueError:
        return None


def _today(today: Optional[_dt.date]) -> _dt.date:
    return today or _dt.date.today()


def normalize(gate: str, region: str, wave: str, value: Any, *, source_key: str,
              legacy: bool = False, today: Optional[_dt.date] = None) -> Waiver:
    """把台账里的一条值校验成 Waiver（纯函数，不碰库）。"""
    t = _today(today)
    w = Waiver(gate=gate, region=str(region).upper(), wave=str(wave), source_key=source_key,
               legacy=legacy)
    if gate in RED_LINES:
        w.problems.append(f"RED_LINE：{RED_LINES[gate]}——不可豁免")
        return w
    policy = GATE_POLICIES.get(gate)
    if policy is None:
        w.problems.append(f"闸 {gate!r} 未在 GATE_POLICIES 登记（可豁免的闸：{', '.join(sorted(GATE_POLICIES))}）")
        return w
    if isinstance(value, (str, bytes)):
        try:
            value = json.loads(value)
        except Exception:
            value = None
    if not isinstance(value, dict):
        w.problems.append("值不是 JSON 对象")
        return w

    w.reason = str(value.get("reason") or "").strip()
    w.evidence = value.get("evidence")
    if not w.reason:
        w.problems.append("缺 reason（人话原因）")

    if legacy:
        # 旧键 {"reason","until"}：保持既有语义（有 reason 即放行，until 含当天），只补可见性告警。
        w.reason_code = str(value.get("reason_code") or "LEGACY")
        w.approved_by = str(value.get("approved_by") or "legacy")
        w.created_at = str(value.get("created_at") or "") or None
        raw_until = value.get("until") if value.get("until") not in (None, "") else value.get("expires_at")
        if raw_until in (None, ""):
            w.warnings.append("NO_EXPIRY：旧键没有 until，等于永久放行——请改写为带 expires_at 的 waiver")
        else:
            d = _parse_date(raw_until)
            if d is None:
                w.problems.append(f"until={raw_until!r} 无法解析为日期（fail closed，不按永久处理）")
            else:
                w.expires_at = d.isoformat()
    else:
        w.reason_code = str(value.get("reason_code") or "")
        w.approved_by = str(value.get("approved_by") or "")
        w.created_at = str(value.get("created_at") or "") or None
        if w.reason_code not in REASON_CODES:
            w.problems.append(f"reason_code={w.reason_code!r} 不在枚举 {sorted(REASON_CODES)}")
        if w.approved_by not in APPROVERS:
            w.problems.append(f"approved_by={w.approved_by!r} 须为 user|agent")
        elif w.approved_by not in policy.approvers:
            w.problems.append(f"闸 {gate} 只允许 {'/'.join(policy.approvers)} 批准，得到 {w.approved_by}")
        if w.reason_code == "USER_INSTRUCTION" and w.approved_by != "user":
            w.problems.append("USER_INSTRUCTION 的 approved_by 必须是 user")
        if w.reason_code in EVIDENCE_REQUIRED and not w.evidence:
            w.problems.append(f"reason_code={w.reason_code} 必须带 evidence")
        gv = value.get("gate")
        if gv not in (None, "", gate):
            w.problems.append(f"值里的 gate={gv!r} 与键里的 {gate!r} 不一致")
        created = _parse_date(w.created_at)
        expires = _parse_date(value.get("expires_at"))
        if created is None:
            w.problems.append("缺 created_at（YYYY-MM-DD）")
        else:
            w.created_at = created.isoformat()
        if expires is None:
            w.problems.append("缺 expires_at（YYYY-MM-DD；不允许永久 waiver）")
        else:
            w.expires_at = expires.isoformat()
            if created is not None:
                if expires < created:
                    w.problems.append("expires_at 早于 created_at")
                elif (expires - created).days > policy.max_days:
                    w.problems.append(
                        f"有效期 {(expires - created).days} 天超过闸 {gate} 上限 {policy.max_days} 天")
    if w.problems:
        w.status = INVALID
    elif w.expires_at and _parse_date(w.expires_at) < t:
        w.status = EXPIRED
    else:
        w.status = ACTIVE
    return w


def build_payload(gate: str, region: str, *, reason_code: str, reason: str, approved_by: str,
                  days: int, evidence: Any = None, wave: Optional[Any] = None,
                  today: Optional[_dt.date] = None) -> Dict[str, Any]:
    """生成并校验 waiver 值；返回 ``{"key", "region", "value", "mcp_call"}``。校验失败抛 WaiverError。"""
    t = _today(today)
    value = {
        "gate": gate, "reason_code": reason_code, "reason": reason, "evidence": evidence,
        "approved_by": approved_by, "created_at": t.isoformat(),
        "expires_at": (t + _dt.timedelta(days=int(days))).isoformat(),
    }
    key = waiver_key(gate, region, wave)
    w = normalize(gate, region, str(wave or ALL_WAVES), value, source_key=key, today=t)
    if w.status != ACTIVE:
        raise WaiverError("；".join(w.problems) or f"状态 {w.status}")
    return {
        "key": key, "region": str(region).upper(), "value": value,
        "mcp_call": (f"mcp__wqb-db__upsert_ledger_key(region={str(region).upper()!r}, key={key!r}, "
                     f"value={json.dumps(value, ensure_ascii=False)})"),
    }


# ---------------------------------------------------------------- 读 / 写


def _read_value(conn: Any, region: str, key: str) -> Tuple[bool, Any]:
    """读 ledger_kv 一条（只用 region/key/value 三列——测试夹具的 ledger_kv 可能只有这三列）。"""
    row = conn.execute("SELECT value FROM ledger_kv WHERE region=? AND key=?",
                       (str(region).upper(), key)).fetchone()
    if not row:
        return False, None
    v = row[0]
    if isinstance(v, (str, bytes)):
        try:
            return True, json.loads(v)
        except Exception:
            return True, None
    return True, v


def candidate_keys(gate: str, region: str, wave: Optional[Any] = None) -> List[Tuple[str, bool]]:
    """按优先级排列的 (键, 是否旧键)：wave 专属 → all → 旧键。"""
    out: List[Tuple[str, bool]] = []
    w = ALL_WAVES if wave in (None, "", 0, "0") else str(wave)
    if w != ALL_WAVES:
        out.append((waiver_key(gate, region, w), False))
    out.append((waiver_key(gate, region, ALL_WAVES), False))
    pol = GATE_POLICIES.get(gate)
    if pol and pol.legacy_key:
        out.append((pol.legacy_key, True))
    return out


def load(conn: Any, gate: str, region: str, wave: Optional[Any] = None,
         today: Optional[_dt.date] = None) -> Optional[Waiver]:
    """读该闸当前生效的 waiver。

    有 ACTIVE 的返回第一个 ACTIVE；否则返回**第一个存在但无效/过期**的（让闸的报错点名原因）；
    一个都没有 → None。库不可读 / 缺表 → **异常原样抛出**（既有闸的失败语义由调用方的 try 决定，
    这里不把「读不到」悄悄变成「没有 waiver」或「有 waiver」）。
    """
    if gate in RED_LINES:
        return normalize(gate, region, str(wave or ALL_WAVES), {}, source_key="(red-line)", today=today)
    first_bad: Optional[Waiver] = None
    for key, legacy in candidate_keys(gate, region, wave):
        found, value = _read_value(conn, region, key)
        if not found:
            continue
        wv = normalize(gate, region, str(wave or ALL_WAVES), value, source_key=key,
                       legacy=legacy, today=today)
        if wv.active:
            return wv
        first_bad = first_bad or wv
    return first_bad


def load_all(conn: Any, region: str, today: Optional[_dt.date] = None) -> List[Waiver]:
    """该区全部 waiver（新键 + 旧键），含过期 / 无效——供 `tools/waiver.py list` 与审计。"""
    out: List[Waiver] = []
    region = str(region).upper()
    legacy_map = {p.legacy_key: p.gate for p in GATE_POLICIES.values() if p.legacy_key}
    rows = conn.execute("SELECT key, value FROM ledger_kv WHERE region=? AND (key LIKE ? OR key IN (%s))"
                        % ",".join("?" * len(legacy_map)),
                        (region, WAIVER_PREFIX + "%", *legacy_map)).fetchall()
    for key, raw in rows:
        try:
            value = json.loads(raw) if isinstance(raw, (str, bytes)) else raw
        except Exception:
            value = None
        if key in legacy_map:
            out.append(normalize(legacy_map[key], region, ALL_WAVES, value, source_key=key,
                                 legacy=True, today=today))
            continue
        parsed = parse_key(key)
        if parsed is None:
            w = Waiver(gate="?", region=region, wave="?", source_key=key)
            w.problems.append("键名不符合 waiver_<gate>_<region>_<wave> 或闸未登记")
            out.append(w)
            continue
        gate, reg, wave = parsed
        out.append(normalize(gate, reg, wave, value, source_key=key, today=today))
    return sorted(out, key=lambda x: (x.gate, x.source_key))


def record(store: Any, gate: str, region: str, **kw: Any) -> Dict[str, Any]:
    """校验后经 CampaignStore.upsert_ledger 写入。参数同 ``build_payload``。"""
    p = build_payload(gate, region, **kw)
    store.upsert_ledger(p["region"], p["key"], p["value"])
    return p


# ---------------------------------------------------------------- 横幅 / 跳过检查


def resolve_mode(cli: Optional[str] = None, env: Optional[Dict[str, str]] = None) -> str:
    """``--waiver-mode`` > ``WQB_WAIVER_MODE`` > warn。非法值退回缺省并不静默：调用方会把 note 打出来。"""
    env = os.environ if env is None else env
    for raw in (cli, env.get("WQB_WAIVER_MODE")):
        if raw and raw.strip().lower() in MODES:
            return raw.strip().lower()
    return DEFAULT_MODE


@dataclass
class SkipDecision:
    gate: str
    flag: str
    waiver: Optional[Waiver]
    ok: bool
    lines: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {"gate": self.gate, "flag": self.flag, "ok": self.ok,
                "waiver": self.waiver.to_dict() if self.waiver else None}


def check_skip(conn: Any, gate: str, region: str, wave: Optional[Any], flag: str, *,
               mode: str = DEFAULT_MODE, today: Optional[_dt.date] = None) -> SkipDecision:
    """CLI 逃生口（跳过某闸）的 waiver 检查。

    * 有 ACTIVE waiver → ok，横幅点名批准人 / 原因 / 到期日；
    * 无 / 过期 / 无效 → warn 模式 ok=True 但横幅醒目告警；enforce 模式 ok=False（调用方 exit 2）；
    * off 模式不查（用于测试隔离，横幅仍提示“未检查”）。
    """
    if mode == "off":
        return SkipDecision(gate, flag, None, True, [f"[waiver] 闸 {gate} 被跳过（{flag}）：WQB_WAIVER_MODE=off，未检查 waiver"])
    read_err = ""
    wv = None
    if conn is not None:
        try:
            wv = load(conn, gate, region, wave, today=today)
        except Exception as e:  # 库不可读：按「无 waiver」处理（enforce 下 fail closed）
            read_err = f"（台账不可读：{type(e).__name__}: {e}）"
    if wv is not None and wv.active:
        lines = [f"[waiver] ⚠ 闸 {gate} 被跳过（{flag}）—— 已有 waiver：{wv.summary()}"]
        lines += [f"[waiver]    ⚠ {x}" for x in wv.warnings]
        return SkipDecision(gate, flag, wv, True, lines)
    why = ("无 waiver 记录" + read_err) if wv is None else f"waiver {wv.status}：{'；'.join(wv.problems) or '已过期'}"
    example = waiver_key(gate, region, wave)
    lines = [f"[waiver] ★ 闸 {gate} 被跳过（{flag}），{why}。"
             f"请先写台账 {example}（见 wqb.waiver / `python tools/waiver.py new --gate {gate} --region {str(region).upper()}`）"]
    return SkipDecision(gate, flag, wv, mode != "enforce", lines)


def banner_lines(waivers: Iterable[Waiver], header: str = "[waiver]") -> List[str]:
    """把生效中的 waiver 列成报告首行提示（每个被放行的闸一行；无则空）。"""
    lines = []
    for w in waivers:
        if w.active:
            lines.append(f"{header} ⚠ 闸 {w.gate} 已被放行：{w.summary()}")
            lines += [f"{header}    ⚠ {x}" for x in w.warnings]
    return lines


def gate_report_fields(w: Optional[Waiver]) -> Dict[str, Any]:
    """闸结果 dict 里与 waiver 有关的字段（campaign.py 两个闸共用；``override`` 保持旧形状供既有调用与测试）。"""
    if w is None:
        return {}
    out: Dict[str, Any] = {"waiver": w.to_dict()}
    if w.active:
        out["override"] = {"reason": w.reason, "until": w.expires_at}
    return out


def write_hint(gate: str, region: str) -> str:
    """闸拦截时给出的「怎么写放行」提示（各闸共用，避免各自手写一份会漂移的示例）。"""
    pol = GATE_POLICIES[gate]
    tmpl = {"gate": gate, "reason_code": "USER_INSTRUCTION", "reason": "<用户指令原话>",
            "approved_by": pol.approvers[0], "created_at": "<YYYY-MM-DD>",
            "expires_at": f"<YYYY-MM-DD，距 created_at ≤{pol.max_days} 天>"}
    hint = (f"waiver：mcp__wqb-db__upsert_ledger_key(region={str(region).upper()!r}, "
            f"key={waiver_key(gate, region)!r}, value={json.dumps(tmpl, ensure_ascii=False)})")
    if pol.legacy_key:
        hint += f"（旧键 {pol.legacy_key} {{reason, until}} 仍被识别；缺 until 视为永久放行并告警）"
    return hint


def rejected_note(w: Optional[Waiver]) -> str:
    """存在 waiver 但没被采纳时的说明（过期 / 无效），拼进闸的 error；无则空串。"""
    if w is None or w.active:
        return ""
    return f"（已有 {w.source_key} 但{w.status}：{'；'.join(w.problems) or '已过期（到期日 ' + str(w.expires_at) + '）'}，未采纳）"


def render_switch_table() -> str:
    """「闸与逃生口总表」（Markdown）——嵌入 Claude/skills/INDEX.md 的 switch-table 块，
    tests/unit/test_waiver.py 比对；改政策先改 GATE_POLICIES，再重新生成。"""
    def esc(x: str) -> str:            # 单元格里的 | 必须转义，否则表格错列
        return x.replace("|", "\\|")

    rows = ["| 闸 id（waiver 的 gate） | 层 | 判据 | 逃生口 | 缺省 | 日期翻转 | waiver 批准人 / 最长 |",
            "|---|---|---|---|---|---|---|"]
    for g, p in GATE_POLICIES.items():
        rows.append("| `{g}` | {layer} | {title} | {flags} | {default} | {flip} | {who} / {n} 天 |".format(
            g=g, layer=esc(p.layer), title=esc(p.title), flags="、".join(f"`{esc(f)}`" for f in p.flags),
            default=esc(p.default), flip=esc(p.flip), who="/".join(p.approvers), n=p.max_days))
    return "\n".join(rows)
