# -*- coding: utf-8 -*-
"""_gate_diversity.py - gate.py 拆分·闸6 批级多样性（exposure 持久化 + diversity_audit）。

依赖 _gate_expr_checks：batch_digest（批级幂等）、_check_family_ceiling（运行时迟绑定，
在 check_batch_diversity 函数体内 import——mutable 全局必须在调用时读）。
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import skeleton, expr_fields
from _lib import rules as rules_mod
from _lib.ledger import make_ledger_store
from _gate_expr_checks import batch_digest

def _extract_exposure_from_idea(idea_text):
    """从 GEM idea 文本提取 expected_exposure（收益来源标签）。

    GEM 按 concept_first_rules 输出：
      - **Expected Exposure**: value / momentum / quality / lowvol / liquidity / sentiment / ...
    缺失返回 None（旧 idea 兼容）。
    """
    if not idea_text:
        return None
    # 2026-09-01 兼容兜底格式 "**Expected Exposure** (inferred): xxx"
    # （GEM _ensure_expected_exposure 推断追加的行带 (inferred) 标记）
    m = re.search(r"\*\*Expected Exposure\*\*[^\n:]*:\s*([^\n]+)", idea_text, re.IGNORECASE)
    if not m:
        return None
    raw = m.group(1).strip().strip('`').strip()
    # 标准化：小写、去空格、去标点
    return re.sub(r"[^a-z0-9_]", "", raw.lower().replace(" ", "_")) or None


def _persist_exposure_map(ctx, exp_map):
    """把 expression → expected_exposure 回写 `expressions.expected_exposure`（2026-09-17 新增）。

    ## 为什么
    `_load_exposure_map()` 在**闸6 的伪多样性检查**里算出了这份映射，然后**用完即丢**。
    后果：GEM `SKILL.md` 规则 7（按语义维度判多样性：≥3 个 Expected Exposure）与
    规则 8（用 `risk_neutralized_sharpe` 验证 Exposure 声明）**没有可度量的输入** ——
    验证侧数据早已落库，缺的是**声明侧**。

    ## 行为
    - **尽力而为**：任何异常都吞掉并返回 0，绝不影响门禁判定；
    - 只写**非空** exposure，且不覆盖已有非空值（避免用推断值污染人工标注）；
    - 返回成功更新的行数。
    """
    if not exp_map:
        return 0
    try:
        from _lib.wqb_store import get_store
        st = get_store(ctx)
        try:
            cur = st.connection.cursor()
            n = 0
            for expr, exposure in exp_map.items():
                if not expr or not exposure:
                    continue
                cur.execute(
                    "UPDATE expressions SET expected_exposure=?, updated_at=datetime('now') "
                    "WHERE region=? AND expression=? "
                    "AND (expected_exposure IS NULL OR expected_exposure='')",
                    (str(exposure), ctx.region, expr),
                )
                n += cur.rowcount
            st.connection.commit()
            return n
        finally:
            st.close()
    except Exception:
        return 0


def _load_exposure_map(ctx, dataset, delay=1):
    """从 DB idea ledger 加载 expression -> expected_exposure 映射。"""
    try:
        from _lib.wqb_store import get_store
        st = get_store(ctx)
        try:
            idea = st.get_idea(ctx.region, dataset, delay)
        finally:
            st.close()
        if not idea or not isinstance(idea, dict):
            return {}
        t2i = idea.get("template_to_idea") or {}
        expr_list = idea.get("expression_list") or []
        # template -> exposure
        tpl_exp = {}
        for tpl, idea_text in t2i.items():
            exp = _extract_exposure_from_idea(idea_text)
            if exp:
                tpl_exp[tpl] = exp
        # expression -> exposure（模板是 expression 的前缀/包含关系）
        out = {}
        for expr in expr_list:
            for tpl, exp in tpl_exp.items():
                # 模板中的 {variable} 已被替换为具体字段，做包含匹配
                tpl_prefix = tpl.split("{")[0] if "{" in tpl else tpl
                if tpl_prefix and tpl_prefix in expr:
                    out[expr] = exp
                    break
        return out
    except Exception:
        return {}


def check_batch_diversity(exprs, ctx, batch_type="explore", skip=False, dataset=None, delay=1):
    from _gate_expr_checks import _check_family_ceiling
    """闸6 批级多样性：强制落地多样性注入契约 + 收益来源多样性。

    契约来源（优先级）：
      1. 自学习规则引擎 explore_contract 规则（rules_mod.get_active_contract）——新路径
      2. 台账 diversity_audit_latest.next_round_injections——旧路径 fallback（兼容）
    规则：
      - batch_type 在契约 exempt 中（默认 repair）→ 豁免
      - consumed_batches 达到 expires_after_batches → 契约过期失效
      - 批内容哈希已在 consumed_batches → 已消费，不重复计数
      - 不达标 → issues 非空，拒绝提交（必须补注多样性槽位后重过闸）
    收益来源多样性（2026-08-26 新增）：
      - 从 DB idea ledger 提取每条 expression 的 expected_exposure
      - 同批 >60% 表达式共享同一 exposure 且字段族相同 → FAIL（伪多样性）
      - 无 exposure 元信息 → WARN 不阻断（向后兼容）
    返回 (issues, consume_ref)：consume_ref 仅在契约生效且全部达标时非空，
    为 {"digest":..., "rule_id":...|None}，由 main 在总闸通过后回写消费（幂等）。
    """
    if skip:
        return [], None

    # ---- P1-2 家族天花板预检（2026-08-31 新增，WARN 不阻断） ----
    # 主导腿信号族占比 ≥2/3 的批（wave94/95/98/104 实证 SELF≥0.9 必死），
    # 与闸6 的骨架/算子/exposure 多样性互补（字段信号族维度）。
    # WARN 不阻断：避免与现有契约冲突，仅提示建议分散。
    # 位置：skip 之后、契约检查之前——无论契约是否存在都执行的通用检查。
    if _check_family_ceiling is not None and len(exprs) >= 3:
        try:
            _fc_ok, _fc_reason, _fc_details = _check_family_ceiling(exprs)
            if not _fc_ok:
                print(f"[DIVERSITY-WARN][P1-2] 家族天花板预警：{_fc_reason}；"
                      f"建议分散信号族（momentum/value/quality/volatility/liquidity/sentiment/analyst）")
        except Exception as _e:
            print(f"[DIVERSITY-WARN][P1-2] 家族天花板预检异常（不阻断）: {_e}")

    # P0-2 (2026-08-25): 契约过期 = 静默 fail-open 修复。
    #   原 get_active_contract 在 consumed>=expires 时返回 None，使闸6 静默 vacuous 通过、
    #   四层多样性保证在无人察觉下悄悄失效。现以三态判定：
    #     - expired -> FAIL-CLOSED（阻断提交） + 自动续约新契约，要求重跑闸门按新契约校验本批
    #     - none    -> 维持现状（P0-3 待修：缺失契约亦应 fail-closed）
    #     - active  -> 正常校验
    inj = None
    rule_id = None
    try:
        _cstate, _cact = rules_mod.get_contract_expiry_state(ctx, batch_type=batch_type)
    except Exception:
        _cstate, _cact = "none", None
    if _cstate == "expired":
        _new_rid = rules_mod.renew_contract(ctx, _cact)
        _msg = (f"已自动续约新契约 {_new_rid}" if _new_rid
                else "自动续约失败，请手动调用 issue_contract 续约")
        return [f"[DIVERSITY-EXPIRED] 多样性注入契约已消费满 "
                f"{len(_cact.get('consumed_batches', []))}/"
                f"{_cact.get('expires_after_batches', 10)} 批，保证已静默失效；"
                f"{_msg}，请重跑闸门按新契约校验本批"], None
    if _cstate == "active":
        inj = _cact
        rule_id = _cact.get("_rule_id")
    # 旧路径 fallback：台账契约（兼容）
    if inj is None:
        try:
            state = make_ledger_store(ctx).load()
        except Exception:
            return [], None
        if not state:
            return [], None
        inj = (state.get("diversity_audit_latest") or {}).get("next_round_injections")
        if not inj:
            return [], None
        if batch_type in inj.get("exempt", []):
            return [], None
        # P0-2 旧路径同样 fail-closed：台账契约过期不再静默通过
        if len(inj.get("consumed_batches", [])) >= inj.get("expires_after_batches", 10):
            return [f"[DIVERSITY-EXPIRED] 台账多样性契约已消费满 "
                    f"{len(inj.get('consumed_batches', []))}/{inj.get('expires_after_batches', 10)} 批，"
                    f"保证已失效；请续约后重跑闸门"], None
    consumed = inj.get("consumed_batches", [])
    digest = batch_digest(exprs)
    if digest in consumed:
        return [], None
    issues = []
    req_ops = set(inj.get("required_operators", []))
    if req_ops:
        # fix(2026-08-25): (算子,字段) 组合去重计数——原实现只数"用了 required 算子的
        #   表达式条数"，导致两条 group_neutralize(同字段) 被误判为 2 份多样性。
        #   现改为：对每个含 required 算子的表达式，将其与表达式内全部叶子字段
        #   （不被 '(' 紧跟的非数字标识符）配对，按 (算子,字段) 互异组合计数。
        #   注：嵌套 required 算子会被扁平计为同一表达式的字段组合，属保守（不会虚增多样性）。
        _op_call = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(")
        # 叶子字段 = 不被 '(' 紧跟（忽略空白）的标识符，且非纯数字。
        # 用 \b 锁词边界，避免贪婪回退把算子名 group_neutralize 截成 group_neutraliz 当字段。
        _leaf = lambda e: {t for t in re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\b(?!\s*\()", e)
                           if not t.isdigit()}

        def _expr_combos(e):
            ops_present = set(_op_call.findall(e)) & req_ops
            return {(op, f) for op in ops_present for f in _leaf(e)}

        # 2026-09-24 P1 强度优先：闸 6 从「跨族算子组合」改为「字段族不重复」。
        # 原实现要求每批 ≥2 个互异 (算子,字段) 组合使用 required 算子，
        # 导致 build_wave 的 diversity-heal 注入 group_cartesian_product(sector,sector)
        # 等 degenerate 式凑数（5 次命中），烧配额在无意义式上。
        # 现改为：只查「同一字段族不重复」（用 _lib.common.expr_fields 提取字段集合，
        # 同一字段集合的表达式最多 max_field_repeat 条），多样性交给字段族不重复
        # 与算子树分桶（bucket_key）来控，不再强制跨族算子组合。
        # 字段族不重复检查（2026-09-24 P1）：同一字段集合的表达式最多 max_field_repeat 条
        _max_field_repeat = int(os.environ.get("WQB_MAX_FIELD_REPEAT", "3"))
        _field_counter = collections.Counter()
        _field_duplicates = []
        for e in exprs:
            fields = frozenset(expr_fields(e, known_ops=None, min_len=6))
            _field_counter[fields] += 1
            if _field_counter[fields] > _max_field_repeat:
                _field_duplicates.append({
                    "fields": sorted(fields),
                    "count": _field_counter[fields],
                    "limit": _max_field_repeat,
                })
        if _field_duplicates:
            issues.append(
                f"[DIVERSITY-FIELD] 字段族重复超限：{len(_field_duplicates)} 个字段族"
                f"出现次数 > {_max_field_repeat}（同一字段集合的表达式过多，"
                f"回测必高相关；请换字段组合或换信号概念）"
            )
            for dup in _field_duplicates[:5]:  # 只留前 5 个示例
                print(f"[DIVERSITY-FIELD] 字段族 {dup['fields']} 出现 {dup['count']} 次"
                      f"（上限 {_max_field_repeat}）")
        # 可选冗余粗筛（无需收益数据）：两条表达式的 (算子,字段) 组合集完全相同
        #   = 结构性近重复信号，建议保留其一避免浪费配额（非阻断 WARN）。
        # 2026-09-24 P1：per_expr 已随「跨族算子组合」检查一起移除，
        # 结构性近重复信号改用字段集合判定（同一字段集合出现 >1 次即 WARN）。
        _field_sets = [frozenset(expr_fields(e, known_ops=None, min_len=6)) for e in exprs]
        _sig_counter = collections.Counter(_field_sets)
        for _s, _c in _sig_counter.items():
            if _c > 1 and _s:
                print(f"[DIVERSITY-WARN] 结构性近重复信号（{_c} 条共享字段集合 "
                      f"{sorted(_s)}）——建议保留其一，避免浪费配额")
    skel_counts = collections.Counter(skeleton(e) for e in exprs)
    for name, quota in (inj.get("skeleton_quota") or {}).items():
        if skel_counts.get(name, 0) < quota:
            issues.append(f"[DIVERSITY] 骨架 {name} 达标 {skel_counts.get(name, 0)}/{quota}")

    # ---- 收益来源多样性闸（2026-08-26 新增） ----
    # 从 DB idea ledger 提取 expected_exposure，同批 >60% 共享同一 exposure 且字段族相同 → FAIL
    if dataset:
        exp_map = _load_exposure_map(ctx, dataset, delay=delay)
        if exp_map:
            # 2026-09-17：顺带把这份映射落库（此前算完即丢 → GEM 规则 7/8 无法度量）
            persisted = _persist_exposure_map(ctx, exp_map)
            if persisted:
                print(f"[DIVERSITY] expected_exposure 回写 {persisted} 条")
            # 提取字段族（字段前缀，如 starmine_/fnd72_/oth455_）
            def _field_family(e):
                fields = expr_fields(e, known_ops=None, min_len=6)
                if not fields:
                    return "unknown"
                # 取第一个字段的前缀（下划线第一段）
                f = sorted(fields)[0]
                return f.split("_")[0] if "_" in f else f[:6]

            exp_groups = collections.defaultdict(list)
            for e in exprs:
                exp = exp_map.get(e)
                if exp:
                    exp_groups[(exp, _field_family(e))].append(e)
            total_with_exp = sum(len(v) for v in exp_groups.values())
            if total_with_exp > 0:
                # 找最大组
                (top_exp, top_fam), top_exprs = max(exp_groups.items(), key=lambda kv: len(kv[1]))
                share = len(top_exprs) / len(exprs)
                if share > 0.6 and len(exprs) >= 3:
                    issues.append(
                        f"[DIVERSITY-EXPOSURE] 收益来源伪多样性：{len(top_exprs)}/{len(exprs)} "
                        f"({share:.0%}) 表达式共享 exposure={top_exp} + 字段族={top_fam}，"
                        f"结构不同但收益来源相同，回测必高相关；请换字段组合或换 exposure"
                    )
                elif share > 0.4:
                    print(f"[DIVERSITY-WARN] 收益来源集中：{share:.0%} 表达式共享 "
                          f"exposure={top_exp} + 字段族={top_fam}（建议分散）")
        else:
            print(f"[DIVERSITY-WARN] 无 expected_exposure 元信息（dataset={dataset}），"
                  f"收益来源多样性闸降级为 WARN；请确保 GEM prompt 要求输出 Expected Exposure")

    consume_ref = None if issues else {"digest": digest, "rule_id": rule_id}
    return issues, consume_ref


def consume_diversity(ctx, consume_ref):
    """闸6 契约消费回写（幂等，digest 去重）。

    rule_id 命中走规则引擎新路径（explore_contract），否则台账 fallback
    （diversity_audit_latest.next_round_injections.consumed_batches）。
    CLI main 与 pipeline 批级闸共用，保持两入口消费口径一致。
    """
    if not consume_ref:
        return
    digest = consume_ref["digest"]
    rule_id = consume_ref.get("rule_id")
    if rule_id:
        try:
            rules_mod.consume_contract(ctx, rule_id, digest)
        except Exception as e:
            print(f"[rules] 契约消费回写异常: {e}", file=sys.stderr)
    else:
        store = make_ledger_store(ctx)

        def consume(d):
            inj = (d.get("diversity_audit_latest") or {}).get("next_round_injections")
            if inj is not None:
                cb = inj.setdefault("consumed_batches", [])
                if digest not in cb:
                    cb.append(digest)

        store.update(consume)


# ---- 闸 7/8：数据质量预检（2026-08-23） ----

