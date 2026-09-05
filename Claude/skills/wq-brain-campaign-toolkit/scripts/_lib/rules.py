# -*- coding: utf-8 -*-
"""_lib/rules.py - 方法论自学习规则引擎（L2 结构化 + L3 消费 + L4 验证）。

核心思想：把"事后写经验 md"升级为"流程中自动回流的闭环"。
规则 = 机器可消费的结构化条目（带适用条件 trigger + 动作 action + 证据 evidence
+ 置信度 confidence + 状态 status），存储于战役目录 reference/methodology_rules.json。

四层闭环：
  L1 采集  runner 收割后 extract_signals() 从结果自动识别模式 -> 候选规则
  L2 结构化 RuleStore 读写 rules.json（原子写），md 给人看 / rules.json 给机器消费
  L3 消费  build_wave/gate/pipeline 执行前 query() 强制注入（硬门拦截/提示）
  L4 验证  validate() 新数据与旧规则冲突 -> 降级 confidence / 标 contested / 触发翻案批

规则 schema（单条）：
  rule_id      唯一标识（snake_case）
  type         strategy | dead_end | gate_override | universe_lever | field_whitelist | diagnosis
               | explore_contract（多样性注入契约，原 diversity_audit 台账契约并入）
  trigger      适用条件 dict：region/universe/dataset_type/condition（"*"=通配）
  action       机器可执行动作 dict：{"op": "...", "params": {...}, "message": "给人看的提示"}
  evidence     证据 dict：campaign/wave/metrics 等
  confidence   0.0-1.0，初始 0.8，验证成功 +0.05（封顶 1.0），冲突 *0.7
  status       active | contested | deprecated
  times_applied / times_succeeded  应用/成功计数（L4 用）
  created_at / validated_at        ISO 时间戳
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import atomic_write, load_json

RULES_VERSION = 1

# 全局规则库：toolkit config/ 下，跨 region 共享（所有战役通用方法论）。
_LIB = os.path.dirname(os.path.abspath(__file__))
_TOOLKIT_ROOT = os.path.dirname(os.path.dirname(_LIB))
GLOBAL_RULES_PATH = os.path.join(_TOOLKIT_ROOT, "config", "methodology_rules.json")


def _now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def _today():
    return datetime.date.today().isoformat()


def _region_from_dir(campaign_dir):
    return os.path.basename(os.path.abspath(campaign_dir)).upper()


# ---------------- L2：规则存储 ----------------

class RuleStore:
    """区域 methodology_rules 入库（ledger_kv）；全局规则仍读 toolkit config 文件。

    测试用 tmp_path（路径不含 tracking/）继续走文件，避免污染 data/wqb.db。
    """

    def __init__(self, campaign_dir, global_path=None):
        self.dir = os.path.abspath(campaign_dir)
        self.path = os.path.join(self.dir, "reference", "methodology_rules.json")
        self.global_path = global_path or GLOBAL_RULES_PATH
        self.region = _region_from_dir(self.dir)

    def _use_db(self):
        if os.environ.get("WQB_RULES_FILE_ONLY") == "1":
            return False
        parts = self.dir.replace("\\", "/").split("/")
        if "tracking" in parts:
            return True
        return bool(os.environ.get("WQB_DB_PATH"))

    def _store(self):
        from wqb_store import get_store
        class _Ctx:
            pass
        c = _Ctx()
        c.dir = self.dir
        c.region = self.region
        return get_store(c)

    def _load_file(self, path):
        if not os.path.exists(path):
            return {"version": RULES_VERSION, "rules": []}
        try:
            d = load_json(path, encoding="utf-8-sig")
        except Exception:
            return {"version": RULES_VERSION, "rules": []}
        d.setdefault("version", RULES_VERSION)
        d.setdefault("rules", [])
        return d

    def _load_region_db(self):
        st = self._store()
        try:
            data = st.get_methodology_rules(self.region)
        finally:
            st.close()
        if data and isinstance(data, dict):
            data.setdefault("version", RULES_VERSION)
            data.setdefault("rules", [])
            return data
        # 一次性从旧文件迁移
        file_data = self._load_file(self.path)
        if file_data.get("rules"):
            self._save_region_db(file_data)
        return file_data

    def _save_region_db(self, data):
        data["version"] = RULES_VERSION
        data["updated_at"] = _now()
        st = self._store()
        try:
            st.upsert_methodology_rules(self.region, data)
        finally:
            st.close()

    def load(self):
        """合并全局 + 区域规则（区域优先，同 rule_id 区域覆盖全局）。"""
        g = self._load_file(self.global_path)
        r = self.load_region_only()
        merged = {x.get("rule_id"): x for x in g["rules"] if x.get("rule_id")}
        for x in r["rules"]:
            if x.get("rule_id"):
                merged[x["rule_id"]] = x
        return {"version": RULES_VERSION, "rules": list(merged.values()),
                "_global_count": len(g["rules"]), "_region_count": len(r["rules"])}

    def load_region_only(self):
        """仅区域规则（upsert/save 作用对象）。"""
        if self._use_db():
            try:
                return self._load_region_db()
            except Exception:
                return self._load_file(self.path)
        return self._load_file(self.path)

    def save(self, data):
        data["version"] = RULES_VERSION
        data["updated_at"] = _now()
        if self._use_db():
            try:
                self._save_region_db(data)
                return
            except Exception:
                pass
        atomic_write(self.path, data)

    def get(self, rule_id):
        for r in self.load()["rules"]:
            if r.get("rule_id") == rule_id:
                return r
        return None

    def upsert(self, rule, global_scope=None):
        """按 rule_id 幂等写入；已存在则合并（保留计数/时间戳）。

        global_scope：True=写全局库（跨 region 共享）；False=写区域库；
                      None=按 rule.trigger.region 自动路由（"*"/缺省 -> 全局，否则 -> 区域）。
        """
        if global_scope is None:
            trig_region = (rule.get("trigger") or {}).get("region")
            global_scope = trig_region in (None, "", "*")
        if global_scope:
            target_path = self.global_path
            data = self._load_file(target_path)
            rules = data["rules"]
            for i, r in enumerate(rules):
                if r.get("rule_id") == rule.get("rule_id"):
                    merged = dict(r)
                    merged.update({k: v for k, v in rule.items() if v is not None})
                    for k in ("times_applied", "times_succeeded", "created_at"):
                        if k not in rule:
                            merged[k] = r.get(k, 0 if k != "created_at" else _now())
                    rules[i] = merged
                    self._save_to(target_path, data)
                    return merged
            rule.setdefault("created_at", _now())
            rule.setdefault("times_applied", 0)
            rule.setdefault("times_succeeded", 0)
            rule.setdefault("confidence", 0.8)
            rule.setdefault("status", "active")
            rules.append(rule)
            self._save_to(target_path, data)
            return rule

        # 区域库：DB 优先
        data = self.load_region_only()
        rules = data["rules"]
        for i, r in enumerate(rules):
            if r.get("rule_id") == rule.get("rule_id"):
                merged = dict(r)
                merged.update({k: v for k, v in rule.items() if v is not None})
                for k in ("times_applied", "times_succeeded", "created_at"):
                    if k not in rule:
                        merged[k] = r.get(k, 0 if k != "created_at" else _now())
                rules[i] = merged
                self.save(data)
                return merged
        rule.setdefault("created_at", _now())
        rule.setdefault("times_applied", 0)
        rule.setdefault("times_succeeded", 0)
        rule.setdefault("confidence", 0.8)
        rule.setdefault("status", "active")
        rules.append(rule)
        self.save(data)
        return rule

    def _save_to(self, path, data):
        data["version"] = RULES_VERSION
        data["updated_at"] = _now()
        atomic_write(path, data)

    def query(self, rule_type=None, region=None, universe=None,
              dataset_type=None, status="active"):
        """L3 消费入口：按适用条件过滤出当前上下文命中的规则。"""
        out = []
        for r in self.load()["rules"]:
            if status and r.get("status") != status:
                continue
            if rule_type and r.get("type") != rule_type:
                continue
            t = r.get("trigger", {})
            if not _match(t.get("region"), region):
                continue
            if not _match(t.get("universe"), universe):
                continue
            if not _match(t.get("dataset_type"), dataset_type):
                continue
            out.append(r)
        return out


def _match(pattern, value):
    """trigger 字段匹配：None/"*" 通配；否则需相等（大小写不敏感）。"""
    if pattern in (None, "", "*"):
        return True
    if value is None:
        return True  # 上下文未提供该维度 -> 不据此过滤
    return str(pattern).upper() == str(value).upper()


# ---------------- L3：消费（硬门注入） ----------------

def _store_for(ctx):
    """从 ctx 构造 RuleStore；ctx 可携带 global_path（测试隔离用）。"""
    d = ctx.dir if hasattr(ctx, "dir") else ctx
    gp = getattr(ctx, "global_path", None)
    return RuleStore(d, global_path=gp)


def apply_rules(ctx, rule_type, context=None):
    """执行脚本调用：返回命中的 active 规则列表（按 confidence 降序）。

    context: {"region":..., "universe":..., "dataset_type":...}
    调用方负责把 rule["action"] 转成具体行为（拦截/提示/覆盖）。
    """
    context = context or {}
    store = _store_for(ctx)
    rules = store.query(rule_type=rule_type,
                        region=context.get("region"),
                        universe=context.get("universe"),
                        dataset_type=context.get("dataset_type"))
    return sorted(rules, key=lambda r: -r.get("confidence", 0))


def check_universe_lever(ctx, intended_universe):
    """OPT-2 修复：runner 启动前校验 universe 是否命中"判死杠杆"规则。

    返回 (ok, messages)。命中 active universe_lever 规则且 intended 等于判死值 -> ok=False。
    """
    store = _store_for(ctx)
    region = getattr(ctx, "region", None)
    msgs, ok = [], True
    for r in store.query(rule_type="universe_lever", region=region):
        dead_val = (r.get("action") or {}).get("dead_universe")
        if dead_val and str(dead_val).upper() == str(intended_universe).upper():
            ok = False
            msgs.append(f"[rules] universe={intended_universe} 命中判死规则 "
                        f"{r['rule_id']}（{r.get('action', {}).get('message', '')}）")
            # 拦截生效即一次应用，计入 times_applied 供成功率校准
            r["times_applied"] = r.get("times_applied", 0) + 1
            store.upsert(r, global_scope=False)
    return ok, msgs


# ---------------- L1：采集（信号提取） ----------------

def extract_signals(rows, wave_meta=None):
    """从 runner 收割的 rows（metrics dict 列表）自动识别方法论模式 -> 候选规则。

    rows: [{"expr":..., "sharpe":..., "prod_corr":..., "rn_fitness":..., ...}, ...]
    返回 candidate rule dict 列表（未写库，由调用方 upsert）。
    """
    signals = []
    rows = [r for r in rows if isinstance(r, dict)]
    if not rows:
        return signals
    # 模式1：prod corr 随某权重单调变化 -> 稀释策略信号
    sig = _detect_dilution(rows)
    if sig:
        signals.append(sig)
    # 模式2：universe 变窄 IS 全崩 -> universe 杠杆判死
    sig = _detect_universe_collapse(rows, wave_meta)
    if sig:
        signals.append(sig)
    # 模式3：全部 LOW_SHARPE -> 数据集需加工/字段太弱
    sig = _detect_all_low_sharpe(rows, wave_meta)
    if sig:
        signals.append(sig)
    return signals


def _f(r, *keys):
    for k in keys:
        v = r.get(k)
        if isinstance(v, (int, float)):
            return float(v)
    return None


def _detect_dilution(rows):
    """检测 prod_corr 随权重参数单调下降（稀释策略有效的证据）。"""
    pts = []
    for r in rows:
        w = _f(r, "weight", "mix_weight", "fcf_weight")
        pc = _f(r, "prod_corr", "prodCorrelation", "prod_correlation")
        if w is not None and pc is not None:
            pts.append((w, pc))
    if len(pts) < 3:
        return None
    pts.sort()
    ws = [p[0] for p in pts]
    pcs = [p[1] for p in pts]
    # 权重升序排列后：prod_corr 单调升 = 权重越低 prod 越低 = 稀释有效（允许相邻相等）
    mono = all(pcs[i] <= pcs[i + 1] + 1e-9 for i in range(len(pcs) - 1))
    if not mono or pcs[-1] - pcs[0] < 0.05:
        return None
    return {
        "rule_id": f"auto_dilution_{_today()}",
        "type": "strategy",
        "trigger": {"condition": "is_strong AND prod_corr > 0.7", "region": "*"},
        "action": {"op": "gradient_dilute",
                   "params": {"weight_range": [ws[0], ws[-1]]},
                   "message": f"检测到稀释策略信号：权重 {ws[-1]}→{ws[0]} 时 "
                              f"prod_corr {pcs[-1]:.3f}→{pcs[0]:.3f} 单调降"},
        "evidence": {"weight_prod_curve": pts},
        "confidence": 0.6,  # 自动提取的信号初始置信度低于人工复盘
        "status": "active",
        "source": "auto_extract",
    }


def _detect_universe_collapse(rows, wave_meta):
    """检测 universe 变窄导致 IS 全崩（universe 杠杆判死证据）。"""
    meta = wave_meta or {}
    uni = meta.get("universe")
    sharpes = [_f(r, "sharpe") for r in rows]
    sharpes = [s for s in sharpes if s is not None]
    if not uni or len(sharpes) < 3:
        return None
    if max(sharpes) < 0.5:  # 全崩
        return {
            "rule_id": f"auto_universe_collapse_{uni}_{_today()}",
            "type": "universe_lever",
            "trigger": {"universe": uni, "region": meta.get("region", "*")},
            "action": {"op": "block_universe", "dead_universe": uni,
                       "message": f"universe={uni} 下 {len(sharpes)} 条全崩 "
                                  f"(max sharpe={max(sharpes):.2f})，疑似杠杆判死"},
            "evidence": {"universe": uni, "max_sharpe": max(sharpes), "n": len(sharpes)},
            "confidence": 0.5,  # 单次全崩不足以判死，需人工/多波确认
            "status": "contested",  # 自动提取的判死先标 contested，人工确认后转 active
            "source": "auto_extract",
        }
    return None


def _detect_all_low_sharpe(rows, wave_meta):
    sharpes = [_f(r, "sharpe") for r in rows]
    sharpes = [s for s in sharpes if s is not None]
    if len(sharpes) < 5:
        return None
    if max(sharpes) < 1.0:
        meta = wave_meta or {}
        return {
            "rule_id": f"auto_low_sharpe_{meta.get('dataset', 'x')}_{_today()}",
            "type": "diagnosis",
            "trigger": {"dataset": meta.get("dataset", "*"), "region": meta.get("region", "*")},
            "action": {"op": "flag_dataset_weak",
                       "message": f"dataset={meta.get('dataset')} {len(sharpes)} 条 "
                                  f"max sharpe={max(sharpes):.2f}<1.0，单字段太弱需复合/加工"},
            "evidence": {"max_sharpe": max(sharpes), "n": len(sharpes)},
            "confidence": 0.5,
            "status": "contested",
            "source": "auto_extract",
        }
    return None


# ---------------- L4：验证（过期/证伪） ----------------

def rule_success_rate(rule):
    """规则成功率 = times_succeeded / times_applied；未应用过返回 None。

    times_applied 由 consume_contract / check_universe_lever 递增，
    times_succeeded 由 validate_rules 递增。二者缺一则成功率无意义。
    """
    applied = rule.get("times_applied", 0) or 0
    if applied <= 0:
        return None
    return round(rule.get("times_succeeded", 0) / applied, 3)

def validate_rules(ctx, new_rows, wave_meta=None):
    """用新回测数据校验 active 规则；冲突则降级/标 contested，返回变更报告。

    当前实现的校验：
      - universe_lever 判死规则：若新数据在判死 universe 下出现 sharpe>=1.0 -> 证伪
      - strategy dilution 规则：若新数据 prod 曲线不再单调 -> 降 confidence
    """
    store = _store_for(ctx)
    data = store.load()  # 合并视图（全局+区域），用于读取
    report = {"validated": 0, "degraded": [], "falsified": [], "reinforced": []}
    meta = wave_meta or {}
    sharpes = [_f(r, "sharpe") for r in new_rows if isinstance(r, dict)]
    sharpes = [s for s in sharpes if s is not None]
    max_sharpe = max(sharpes) if sharpes else None
    cur_uni = meta.get("universe")

    for r in data["rules"]:
        if r.get("status") not in ("active", "contested"):
            continue
        t = r.get("trigger", {})
        changed_rule = None
        # universe_lever 证伪：判死 universe 下出现强 alpha
        if r.get("type") == "universe_lever":
            dead = (r.get("action") or {}).get("dead_universe")
            if dead and cur_uni and str(dead).upper() == str(cur_uni).upper():
                report["validated"] += 1
                if max_sharpe is not None and max_sharpe >= 1.0:
                    r["confidence"] = round(r.get("confidence", 0.8) * 0.7, 3)
                    r["status"] = "contested"
                    r.setdefault("contest_evidence", []).append(
                        {"at": _now(), "max_sharpe": max_sharpe, "universe": cur_uni})
                    report["falsified"].append(r["rule_id"])
                    changed_rule = r
                else:
                    r["times_succeeded"] = r.get("times_succeeded", 0) + 1
                    r["confidence"] = min(1.0, round(r.get("confidence", 0.8) + 0.05, 3))
                    if r["status"] == "contested" and r["confidence"] >= 0.7:
                        r["status"] = "active"  # 复核通过转正
                    report["reinforced"].append(r["rule_id"])
                    changed_rule = r
        if changed_rule is not None:
            changed_rule["validated_at"] = _now()
            # 按 trigger.region 路由写回全局或区域库（避免合并视图污染）
            store.upsert(changed_rule)
    return report


# ---------------- explore_contract：多样性注入契约（融合多样性评估闭环） ----------------

# 契约存于规则 action 字段，schema：
#   action = {
#     "op": "inject_diversity",
#     "required_operators": [...],      # 每批至少 per_batch_min_operators 条使用其中之一
#     "skeleton_quota": {name: n},      # 每批骨架 name 至少 n 条
#     "per_batch_min_operators": 2,
#     "expires_after_batches": 10,      # 消费满 N 批后过期
#     "exempt": ["repair"],             # 豁免的 batch_type
#     "consumed_batches": [digest...],  # 已消费批内容哈希（幂等）
#     "issued_at": ISO,
#   }

CONTRACT_TYPE = "explore_contract"


def get_active_contract(ctx, batch_type="explore"):
    """取当前生效的多样性注入契约（闸6 消费入口）。

    返回契约 action dict 或 None。规则：
      - 无 active explore_contract 规则 -> None
      - batch_type 在 exempt 中 -> None（豁免）
      - consumed_batches 达到 expires_after_batches -> None（过期失效）
    多条契约取最新 issued_at。
    """
    store = _store_for(ctx)
    region = getattr(ctx, "region", None)
    contracts = store.query(rule_type=CONTRACT_TYPE, region=region)
    if not contracts:
        return None
    # 最新优先
    contracts.sort(key=lambda r: (r.get("action") or {}).get("issued_at", ""), reverse=True)
    for r in contracts:
        act = r.get("action") or {}
        if batch_type in act.get("exempt", []):
            continue
        if len(act.get("consumed_batches", [])) >= act.get("expires_after_batches", 10):
            continue
        act["_rule_id"] = r["rule_id"]  # 携带 rule_id 供消费回写
        return act
    return None


def get_contract_expiry_state(ctx, batch_type="explore"):
    """区分契约 缺失 / 过期 / 生效 三态，供闸6 的 fail-closed 判定（P0-2 修复）。

    原 get_active_contract 在 consumed>=expires 时直接返回 None，使闸6 静默 vacuous 通过、
    四层多样性保证在无人察觉下悄悄失效。本函数把"过期"与"缺失"区分开，让 gate 能对
    过期契约显式 FAIL-CLOSED（而非静默放过）。

    返回 (state, act)：
      - ("none", None)    无 active explore_contract 规则（或 batch_type 在 exempt 中）
      - ("expired", act)  存在 active 契约但 consumed_batches >= expires_after_batches（已失效）
      - ("active", act)   正常生效契约（act 携带 _rule_id，与 get_active_contract 返回一致）
    """
    store = _store_for(ctx)
    region = getattr(ctx, "region", None)
    contracts = store.query(rule_type=CONTRACT_TYPE, region=region)
    if not contracts:
        return "none", None
    # 最新优先
    contracts.sort(key=lambda r: (r.get("action") or {}).get("issued_at", ""), reverse=True)
    for r in contracts:
        act = r.get("action") or {}
        if batch_type in act.get("exempt", []):
            continue
        act = dict(act)  # 拷副本，避免改动 store 内缓存对象
        act["_rule_id"] = r["rule_id"]
        if len(act.get("consumed_batches", [])) >= act.get("expires_after_batches", 10):
            return "expired", act
        return "active", act
    return "none", None


def renew_contract(ctx, expired_act):
    """P0-2 自动续约：以过期契约的同款参数签发新契约（consumed_batches 清零）。

    保留 required_operators / skeleton_quota / per_batch_min_operators / exempt /
    factor_templates，使新契约承载一致的多样性强制。返回新 rule_id 或 None（异常失败）。
    调用方负责确保 expired_act 确实已过期（通常来自 get_contract_expiry_state 的 expired 态）。
    """
    try:
        region = getattr(ctx, "region", None) or (expired_act.get("trigger") or {}).get("region")
        return issue_contract(
            ctx,
            required_operators=expired_act.get("required_operators", []),
            skeleton_quota=expired_act.get("skeleton_quota", {}) or {},
            region=region,
            per_batch_min_operators=expired_act.get("per_batch_min_operators", 2),
            expires_after_batches=expired_act.get("expires_after_batches", 10),
            exempt=tuple(expired_act.get("exempt", ("repair",))),
            factor_templates=expired_act.get("factor_templates"),
        )
    except Exception:
        return None


def consume_contract(ctx, rule_id, digest):
    """闸6 总闸通过后回写：把批内容哈希记入契约 consumed_batches（幂等）。

    同时递增 times_applied——契约真正作用于一个批次即算一次应用，
    与 consumed_batches 长度保持一致，供 rule_success_rate() 计算成功率。
    """
    store = _store_for(ctx)
    r = store.get(rule_id)
    if not r:
        return
    act = r.setdefault("action", {})
    cb = act.setdefault("consumed_batches", [])
    if digest not in cb:
        cb.append(digest)
        r["times_applied"] = r.get("times_applied", 0) + 1
        # 契约是区域规则（trigger 带 region），upsert 自动路由回区域库
        store.upsert(r, global_scope=False)


def issue_contract(ctx, required_operators, skeleton_quota, region,
                   per_batch_min_operators=2, expires_after_batches=10,
                   exempt=("repair",), evidence=None, factor_templates=None):
    """diversity_audit 调用：签发新多样性注入契约（写区域规则库）。

    factor_templates: 可选，语义驱动全覆盖的实例化因子 {op: {expr,fields,meaning,...}}，
      写入 action 供 build_wave 直接消费（get_active_contract 返回的 action 携带）。
    返回 rule_id。同 region 新契约签发后，旧契约应被 deprecate（调用方负责或在此处理）。
    """
    store = _store_for(ctx)
    # 先 deprecate 同 region 旧契约（单活跃契约原则）
    for old in store.query(rule_type=CONTRACT_TYPE, region=region, status="active"):
        old["status"] = "deprecated"
        store.upsert(old, global_scope=False)
    # rule_id 带时间戳（含微秒）防多次签发碰撞
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    rid = f"explore_contract_{region}_{ts}"
    action = {
        "op": "inject_diversity",
        "required_operators": list(required_operators),
        "skeleton_quota": dict(skeleton_quota),
        "per_batch_min_operators": per_batch_min_operators,
        "expires_after_batches": expires_after_batches,
        "exempt": list(exempt),
        "consumed_batches": [],
        "issued_at": _now(),
    }
    if factor_templates:
        action["factor_templates"] = factor_templates
    rule = {
        "rule_id": rid,
        "type": CONTRACT_TYPE,
        "trigger": {"region": region},
        "action": action,
        "evidence": evidence or {},
        "confidence": 1.0,
        "status": "active",
        "source": "diversity_audit",
    }
    store.upsert(rule, global_scope=False)
    return rid


def reconcile_contract_landing(ctx, region, ops_counter, skel_counter):
    """L4 落地率对账：diversity_audit 用最新扫描分布对上一活跃/近期契约逐项对账。

    ops_counter/skel_counter: collections.Counter（本次审计的算子/骨架分布）。
    返回 landing 报告 dict 或 None（无契约可对账时）。同时按落地率调契约 confidence：
      算子全落地 -> +0.05（封顶 1.0）；落地率 < 50% -> *0.8 并标 contested（提示契约脱离实际）。
    """
    store = _store_for(ctx)
    # 找最近一条契约（含 deprecated，用于对账上一周期）
    allc = [r for r in store.load()["rules"] if r.get("type") == CONTRACT_TYPE
            and (r.get("trigger") or {}).get("region") == region]
    if not allc:
        return None
    allc.sort(key=lambda r: (r.get("action") or {}).get("issued_at", ""), reverse=True)
    contract = allc[0]
    act = contract.get("action") or {}
    req_ops = act.get("required_operators", [])
    per_op = {op: {"used": ops_counter.get(op, 0), "landed": ops_counter.get(op, 0) > 0}
              for op in req_ops}
    landed_ops = [op for op, v in per_op.items() if v["landed"]]
    missed_ops = [op for op, v in per_op.items() if not v["landed"]]
    per_skel = {s: {"used": skel_counter.get(s, 0), "landed": skel_counter.get(s, 0) >= q}
                for s, q in (act.get("skeleton_quota") or {}).items()}
    n_landed = len(landed_ops)
    landing_rate = (n_landed / len(req_ops)) if req_ops else 1.0
    parts = []
    if per_op:
        parts.append(f"算子落地 {n_landed}/{len(per_op)}"
                     + (f"，未落地: {missed_ops}" if missed_ops else ""))
    if per_skel:
        parts.append(f"骨架落地 {sum(1 for v in per_skel.values() if v['landed'])}/{len(per_skel)}")
    # L4：按落地率调置信度（仅对仍 active 的契约调；deprecated 不再调）
    if contract.get("status") == "active":
        if landing_rate >= 1.0:
            contract["confidence"] = min(1.0, round(contract.get("confidence", 1.0) + 0.05, 3))
            # 契约全项落地即一次成功。validate_rules 只覆盖 universe_lever/dilution，
            # explore_contract 的成功信号在落地率对账，此处不记则成功率恒为 0。
            contract["times_succeeded"] = contract.get("times_succeeded", 0) + 1
        elif landing_rate < 0.5:
            contract["confidence"] = round(contract.get("confidence", 1.0) * 0.8, 3)
            contract["status"] = "contested"
        contract["validated_at"] = _now()
        store.upsert(contract, global_scope=False)
    return {
        "checked_against": act.get("issued_at"),
        "contract_rule_id": contract["rule_id"],
        "consumed_batches": len(act.get("consumed_batches", [])),
        "per_operator": per_op,
        "per_skeleton": per_skel,
        "landing_rate": round(landing_rate, 3),
        "summary": "；".join(parts) if parts else "无强制项",
    }


# ---------------- P1：verdict 自动推荐（规则 -> 下波方向） ----------------

def recommend_next_wave(ctx, rows, near=None, wave_meta=None):
    """verdict 后自动推荐下波方向（仅建议，非强制；提交前仍过 5 闸 + 闸6）。

    输入：
      rows      本波全部行（含 sharpe/fitness/two_year_sharpe/margin_bp/turnover_pct/
                prod_corr/rn_fitness/walls 等，walls 由 review_wave 诊断填入）
      near      near 池行（sharpe 过 near 闸但未达标的行，含 walls）
      wave_meta {"region","universe","dataset"}
    输出：
      推荐列表，按 priority 降序。每条：
        {"direction", "rationale", "priority", "action_hint", "source_rule"|None}

    双路驱动：
      1. walls 聚合：统计哪堵墙命中最多 -> 基础方向（结构层 vs 参数层）
      2. 规则匹配：strategy/diagnosis/universe_lever 规则按当前指标特征命中 -> 策略建议
    """
    meta = wave_meta or {}
    region = meta.get("region") or getattr(ctx, "region", None)
    store = _store_for(ctx)
    rows = [r for r in (rows or []) if isinstance(r, dict)]
    near = [r for r in (near or []) if isinstance(r, dict)]
    recs = []

    # ---- 指标特征提取 ----
    sharpes = [_f(r, "sharpe") for r in rows]
    sharpes = [s for s in sharpes if s is not None]
    max_sharpe = max(sharpes) if sharpes else None
    prods = [_f(r, "prod_corr", "prodCorrelation", "prod_correlation") for r in rows]
    prods = [p for p in prods if p is not None]
    max_prod = max(prods) if prods else None
    rnfs = [_f(r, "rn_fitness", "rnFitness") for r in rows]
    rnfs = [x for x in rnfs if x is not None]

    # ---- walls 聚合（哪堵墙最多）----
    wall_count = {}
    for r in rows:
        for w in (r.get("walls") or []):
            if w.endswith("_UNKNOWN") or w in ("NO_DATA", "RA_OTHER"):
                continue
            wall_count[w] = wall_count.get(w, 0) + 1
    dom_wall = max(wall_count, key=wall_count.get) if wall_count else None

    # ---- 规则匹配（strategy/diagnosis/universe_lever）----
    strat_rules = store.query(rule_type="strategy", region=region)
    diag_rules = store.query(rule_type="diagnosis", region=region)
    uni_rules = store.query(rule_type="universe_lever", region=region)

    # universe 判死规则：当前 universe 命中判死 -> 最高优先级换 universe
    cur_uni = meta.get("universe")
    for r in uni_rules:
        dead = (r.get("action") or {}).get("dead_universe")
        if dead and cur_uni and str(dead).upper() == str(cur_uni).upper():
            correct = (r.get("evidence") or {}).get("correct_universe")
            recs.append({
                "direction": f"换 universe：当前 {cur_uni} 已判死",
                "rationale": (r.get("action") or {}).get("message", ""),
                "priority": 100,
                "action_hint": f"改用 {correct or '更宽 universe'} 重跑" if correct else "换更宽 universe",
                "source_rule": r["rule_id"],
            })

    # 稀释策略：IS 强 + prod_corr 撞墙 -> 梯度稀释（命中 prod_wall_dilution_v1）
    if max_sharpe is not None and max_sharpe >= 1.0 and max_prod is not None and max_prod > 0.7:
        for r in strat_rules:
            if (r.get("action") or {}).get("op") == "gradient_dilute":
                params = (r.get("action") or {}).get("params") or {}
                recs.append({
                    "direction": "prod 墙稀释：IS 强但 prod_corr>0.7",
                    "rationale": (r.get("action") or {}).get("message", ""),
                    "priority": 90,
                    "action_hint": f"compute_mutual_correlation 找 |corr|<{params.get('corr_threshold', 0.3)} "
                                   f"低相关分量，梯度稀释步长 {params.get('weight_step', 0.1)}",
                    "source_rule": r["rule_id"],
                })
                # rnf 权衡警告（rnf_dilution_tradeoff_v1）
                for dr in diag_rules:
                    if (dr.get("action") or {}).get("op") == "warn_rnf_drop":
                        recs.append({
                            "direction": "注意 rnf 随稀释下降",
                            "rationale": (dr.get("action") or {}).get("message", ""),
                            "priority": 50,
                            "action_hint": "稀释破 prod 墙时同步评估 rnf 是否跌破用户闸（默认 0.6）",
                            "source_rule": dr["rule_id"],
                        })
                break

    # ---- walls 驱动的基础方向 ----
    if dom_wall == "SHARPE" and max_sharpe is not None and max_sharpe < 1.0:
        recs.append({
            "direction": "结构层重构：字段太弱（max sharpe<1.0）",
            "rationale": f"{wall_count.get('SHARPE', 0)}/{len(rows)} 行卡 SHARPE 墙且全波 max "
                         f"sharpe={max_sharpe:.2f}<1.0，单字段信号不足",
            "priority": 80,
            "action_hint": "复合多字段/换更强数据集/加事件门控，而非调参数",
            "source_rule": None,
        })
    elif dom_wall in ("2Y", "MARGIN", "TVR") and near:
        # near 池卡参数墙 -> 参数层调（decay/窗口/中性化）
        recs.append({
            "direction": f"参数层调优：near 池卡 {dom_wall} 墙",
            "rationale": f"{len(near)} 行 near 池（sharpe 过 near 闸），主要卡 {dom_wall}，"
                         f"IS 已强仅需参数微调",
            "priority": 70,
            "action_hint": {"2Y": "缩短窗口/提高信号近期权重", "MARGIN": "降换手/调 decay",
                            "TVR": "调 truncation/decay 压或提升手"}.get(dom_wall, "调参数"),
            "source_rule": None,
        })
    elif dom_wall == "CW":
        recs.append({
            "direction": "集中度墙：骨架多样性不足",
            "rationale": f"{wall_count.get('CW', 0)} 行卡 CONCENTRATED_WEIGHT，权重过度集中",
            "priority": 75,
            "action_hint": "group_neut/分组包裹/换骨架，参考闸6 多样性契约",
            "source_rule": None,
        })

    # 全部达标 -> 可提交
    cands = [r for r in rows if not (r.get("walls"))]
    if cands and not recs:
        recs.append({
            "direction": "本波有达标候选，进入提交评审",
            "rationale": f"{len(cands)} 行全门槛过，可走 brain-alpha-judge 双闸评审",
            "priority": 95,
            "action_hint": "提交前查 prod_corr + PPA 主题匹配",
            "source_rule": None,
        })

    # 按优先级降序
    recs.sort(key=lambda x: -x["priority"])
    return recs
