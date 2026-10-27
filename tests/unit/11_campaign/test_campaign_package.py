# -*- coding: utf-8 -*-
"""full_template_campaign 拆分后的回归测试（2026-10-25）。

只覆盖「今天真实踩过的坑」——每条用例都对应一次线上事故，目的不是覆盖率，
而是在无人值守跑 169 个集时，这些行为不再靠"改完重启、用线上撞"来验证：

1. `config` 路径必须解析到仓库根（拆包后少上溯一层会让断点/日志全部落错目录）
2. `LIT_CACHE` 必须存在（原单体文件引用了它但从未定义，两处 try 吞成 NameError ⇒ 缓存全程是死的）
3. `sims_terminal` 必须三态（异常 → None，不能当"还在跑"）
4. `wait_slot` 连续 3 次 None 必须放行（否则静默死等 GATE_TIMEOUT，model182 卡 1839s 的直接原因）
5. `wait_slot` 必须有心跳（静默不能超过 1 分钟）
6. persist 原子写往返无损
7. `build_one_family` 对全部 17 个族（13 L1×L2 + dw + pp + res/reslag）都产出语法平衡、≤10 调用点的表达式
8. `emit_digest` 同一集重跑必须**替换**原行而不是追加（否则行数 ≠ done 数）
"""
import os
import sys
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

def _find_root(start):
    """向上找到同时含 tools/ 与 data/ 的目录（不靠数 dirname 层数，避免挪目录就失效）。"""
    p = os.path.abspath(start)
    for _ in range(8):
        if os.path.isdir(os.path.join(p, "tools")) and os.path.isdir(os.path.join(p, "data")):
            return p
        p = os.path.dirname(p)
    raise RuntimeError(f"找不到仓库根，起点 {start}")


ROOT = _find_root(os.path.dirname(os.path.abspath(__file__)))
# 2026-10-25 迁移：引擎已从 tools/ 搬进 IND skill（tools/wqb_campaign 不再存在）。
# 仍以仓库内副本为测试对象：仓库 Claude/skills/ 是编辑权威，安装位是派生物。
CAMPAIGN_DIR = os.path.join(
    ROOT, "Claude", "skills", "wq-brain-ra-ind", "scripts", "ind_campaign")
if not os.path.isdir(os.path.join(CAMPAIGN_DIR, "wqb_campaign")):
    raise RuntimeError(f"campaign 引擎目录不存在：{CAMPAIGN_DIR}")
sys.path.insert(0, CAMPAIGN_DIR)

import wqb_campaign  # noqa: E402
from wqb_campaign import config, persist, report, generate, transport, lit, fields  # noqa: E402
import campaign_semantics as sem  # noqa: E402

OPS = {
    "ts_backfill", "ts_delta", "ts_decay_linear", "ts_ir", "ts_zscore", "ts_quantile",
    "ts_rank", "ts_scale", "ts_mean", "ts_std_dev", "vec_avg", "vec_sum", "vec_stddev",
    "rank", "quantile", "divide", "add", "subtract", "multiply", "if_else", "greater",
    # 残差化族（2026-10-25）：不进来就会被 count_calls 漏数，≤10 约束形同虚设
    "ts_regression", "ts_delay",
    # robust 几何族（2026-10-26）：group_rank 是破 robust 墙的杠杆之一，
    # signed_power(·,3) 是凸变换；漏登记会让 ≤10 的守护对整族失效
    "group_rank", "signed_power", "abs",
}


def count_calls(expr):
    import re
    return sum(1 for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", expr)
               if m.group(1) in OPS)


def balanced(expr):
    bal = 0
    for ch in expr:
        if ch == "(":
            bal += 1
        elif ch == ")":
            bal -= 1
            if bal < 0:
                return False
    return bal == 0


class FakeResp:
    def __init__(self, payload):
        self._p = payload

    def json(self):
        if isinstance(self._p, Exception):
            raise self._p
        return self._p


class TestConfig(unittest.TestCase):
    def test_root_points_to_repo_root(self):
        self.assertTrue(os.path.isdir(os.path.join(config.ROOT, "data")))
        self.assertTrue(os.path.isfile(config.DB))
        self.assertIn(os.path.join("results", "full_template_campaign_checkpoint.json"), config.CKPT)

    def test_lit_cache_is_defined(self):
        # 回归：原文件 compute_lit 用 LIT_CACHE 但从未定义
        self.assertTrue(hasattr(config, "LIT_CACHE"))
        self.assertTrue(config.LIT_CACHE.endswith("eur_lit_counts.json"))
        self.assertEqual(config.DELAY, 1)


class TestLitQuarter(unittest.TestCase):
    """点亮口径：平台 `get_pyramid_alphas()` 默认**当季**，三格塔满 3 颗点亮。

    2026-10-25 用户裁定。旧口径（历史累计 stage=OS，`>3`）会把 IND 的
    FUNDAMENTAL(当季2) / RISK(1) / INSTITUTIONS(1) 误判为已点亮而排除在开波范围外。
    """

    def test_counts_from_pyramid_reads_region_delay_bucket(self):
        # ① 客户端原始 list 形态（brain_api 直返；2026-10-25 实测）
        raw = {"pyramids": [
            {"category": {"id": "fundamental", "name": "Fundamental"},
             "region": "IND", "delay": 1, "alphaCount": 2},
            {"category": {"id": "risk"}, "region": "IND", "delay": 1, "alphaCount": 1},
            {"category": {"id": "pv"}, "region": "IND", "delay": 1, "alphaCount": 8},
            {"category": {"id": "earnings"}, "region": "IND", "delay": 1, "alphaCount": 0},
            {"category": {"id": "pv"}, "region": "IND", "delay": 0, "alphaCount": 99},
            {"category": {"id": "pv"}, "region": "USA", "delay": 1, "alphaCount": 7},
        ], "from_cache": False}
        self.assertEqual(lit.counts_from_pyramid(raw, "IND"),
                         {"FUNDAMENTAL": 2, "RISK": 1, "PV": 8})
        self.assertEqual(lit.counts_from_pyramid(raw, "IND", "D0"), {"PV": 99})
        self.assertEqual(lit.counts_from_pyramid(raw, "USA"), {"PV": 7})

        # ② MCP `_slim_pyramids` 重排后的 dict 形态
        slim = {"pyramids": {
            "IND": {"D1": {"fundamental": 2, "risk": 1, "institutions": 1,
                           "pv": 8, "earnings": 0, "option": None}},
            "EUR": {"D1": {"pv": 1}},
        }}
        self.assertEqual(lit.counts_from_pyramid(slim, "IND"),
                         {"FUNDAMENTAL": 2, "RISK": 1, "INSTITUTIONS": 1, "PV": 8})
        self.assertEqual(lit.counts_from_pyramid(slim, "IND", "D0"), {})
        self.assertEqual(lit.counts_from_pyramid(slim, "EUR"), {"PV": 1})
        self.assertEqual(lit.counts_from_pyramid({}, "IND"), {})
        self.assertEqual(lit.counts_from_pyramid({"pyramids": "x"}, "IND"), {})

    def test_three_lights_tower(self):
        self.assertEqual(sem.lit_set({"PV": 8, "MODEL": 3, "FUNDAMENTAL": 2}),
                         {"PV", "MODEL"})
        self.assertEqual(sem.lit_set({"MODEL": 3}), {"MODEL"})
        self.assertEqual(sem.lit_set({"MODEL": 2}), set())
        self.assertEqual(sem.lit_set({"MODEL": "3"}), {"MODEL"})
        self.assertEqual(sem.lit_set({"MODEL": None}), set())
        # 兼容现成集合（视为已判定）
        self.assertEqual(sem.lit_set({"pv"}), {"PV"})
        self.assertEqual(sem.lit_set(None), set())


class TestPersist(unittest.TestCase):
    def test_ckpt_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            ck = os.path.join(td, "ck.json")
            with patch.object(persist, "CKPT", ck):
                data = {"done": ["a", "b"], "sims": {"a": [["x", "lvl_rk", 0]]}}
                persist.save_ckpt(data)
                self.assertEqual(persist.load_ckpt(), data)
                self.assertFalse(os.path.exists(ck + ".tmp"))

    def test_results_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            lg = os.path.join(td, "res.json")
            with patch.object(persist, "LOG", lg):
                data = {"results": {"a": {"verdict": "ALIVE", "max_s": 1.9}}}
                persist.save_results(data)
                self.assertEqual(persist.load_results(), data)


class TestTransportTerminal(unittest.TestCase):
    def _fake_brain(self, behaviour):
        import types

        class BC:
            base_url = "https://example.invalid"

            async def ensure_authenticated(self):
                return None

            async def _request(self, method, url, **kw):
                return behaviour()

        m = types.ModuleType("brain_api")
        m.brain_client = BC()
        return m

    def test_exception_returns_none_not_false(self):
        # 回归：旧实现 except → False，让 wait_slot 以为批次还在跑
        mod = self._fake_brain(lambda: (_ for _ in ()).throw(RuntimeError("boom")))
        with patch.dict(sys.modules, {"brain_api": mod}):
            self.assertIsNone(transport.sims_terminal("sid"))

    def test_bad_json_returns_none(self):
        mod = self._fake_brain(lambda: FakeResp(ValueError("not json")))
        with patch.dict(sys.modules, {"brain_api": mod}):
            self.assertIsNone(transport.sims_terminal("sid"))

    def test_all_children_terminal_returns_true(self):
        mod = self._fake_brain(lambda: FakeResp(
            {"children": [{"status": "COMPLETE"}, {"status": "ERROR"}]}))
        with patch.dict(sys.modules, {"brain_api": mod}):
            self.assertIs(transport.sims_terminal("sid"), True)

    def test_running_child_returns_false(self):
        mod = self._fake_brain(lambda: FakeResp(
            {"children": [{"status": "COMPLETE"}, {"status": "RUNNING"}]}))
        with patch.dict(sys.modules, {"brain_api": mod}):
            self.assertIs(transport.sims_terminal("sid"), False)


class TestWaitSlot(unittest.TestCase):
    def _run(self, seq, max_inflight=1):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        it = iter(seq)
        fake_time = type("T", (), {"sleep": staticmethod(lambda s: None),
                                   "time": staticmethod(lambda: 0.0)})
        with patch.object(transport, "sims_terminal", lambda sid: next(it)), \
                patch.object(transport, "MAX_INFLIGHT", max_inflight), \
                patch.object(transport, "GATE_TIMEOUT", 10 ** 6), \
                patch.object(transport, "time", fake_time), \
                redirect_stdout(buf):
            pending = ["s1"]
            transport.wait_slot(pending)
        return pending, buf.getvalue()

    def test_three_none_releases(self):
        # 回归：连续查不到状态必须放行，而不是等满 GATE_TIMEOUT
        pending, out = self._run([None, None, None])
        self.assertEqual(pending, [])
        self.assertIn("连续 3 次查不到状态", out)

    def test_true_releases_immediately(self):
        pending, out = self._run([True])
        self.assertEqual(pending, [])
        self.assertNotIn("超时", out)

    def test_heartbeat_printed(self):
        # 回归：旧版全程静默，人看日志完全看不出卡在哪
        pending, out = self._run([False] * 4 + [True])
        self.assertIn("[gate] 等", out)


class TestGenerate(unittest.TestCase):
    FIELD_M = {"field_name": "demo_field", "field_type": "MATRIX", "sem_type": "level"}
    FIELD_V = {"field_name": "demo_vec", "field_type": "VECTOR", "sem_type": "count"}

    def test_all_families_balanced_and_within_10_calls(self):
        """L1×L2 家族必须 ≤10 调用点；dw / pp 是结构模板，不适用该约束。

        实测：`pp` = `if_else(greater(rank(<dw>), 0.85), <dw>, 0)`，dw 结构被**写了两遍**
        （门控里一次、取值一次）⇒ 17 个调用点。这是模板库的既有形态（sentiment26/wp99v7qv 的成品），
        ≤10 是「手搭交付 alpha」的约束，不是模板库的。此处只把数字钉住，防止无意改重。
        """
        l1l2 = [f"{a}_{b or 'pl'}" for a, b in generate.FAMILIES]
        for r in (self.FIELD_M, self.FIELD_V):
            for tpl in l1l2:
                e = generate.build_one_family(tpl, r, "daily")
                self.assertIsNotNone(e, f"{tpl} 返回 None")
                self.assertTrue(balanced(e), f"{tpl} 括号不平衡: {e}")
                self.assertLessEqual(count_calls(e), 10,
                                     f"{tpl} 调用点 {count_calls(e)} > 10: {e}")
            # 残差化族（跨数据集结构，2026-10-25 接入）：同样钉住平衡与调用点数
            for tpl in generate.RESIDUAL_TPL:
                e = generate.build_one_family(tpl, r, "daily")
                self.assertIsNotNone(e, f"{tpl} 返回 None")
                self.assertTrue(balanced(e), f"{tpl} 括号不平衡: {e}")
                self.assertLessEqual(count_calls(e), 10,
                                     f"{tpl} 调用点 {count_calls(e)} > 10: {e}")
            # dw / pp 只校验平衡 + 固定规模。
            # VECTOR 字段的两处改写互相抵消：剥掉 2 个 ts_backfill(-2)、加 2 个 vec_*（+2）
            # ⇒ dw 仍是 7（2026-10-25 IND option1「VECTOR 不能 backfill」实测）；
            # pp = if_else(1) + greater(1) + rank(1) + 2×dw ⇒ pp = 3 + 2*dw = 17。
            dw_exp = 7
            for tpl, expect in (("dw", dw_exp), ("pp", 3 + 2 * dw_exp)):
                e = generate.build_one_family(tpl, r, "daily")
                self.assertTrue(balanced(e), f"{tpl} 括号不平衡")
                self.assertEqual(count_calls(e), expect,
                                 f"{tpl} 调用点变了（预期 {expect}）：{e}")

    def test_l1_coverage_fills_missing_layer(self):
        # d2 属 diff 层 ⇒ 只补 lvl
        out = generate.ensure_l1_coverage({"d2_rk"})
        self.assertIn("lvl_rk", out)
        self.assertIn("d2_rk", out)
        self.assertNotIn("d1_rk", out)
        # 只给水平 ⇒ 补差分
        out2 = generate.ensure_l1_coverage({"lvl_rk"})
        self.assertIn("d1_rk", out2)
        # 空集合不处理
        self.assertEqual(generate.ensure_l1_coverage(set()), set())

    def test_retired_family_gate_by_form(self):
        """P1-5 零收益族退役（2026-10-27）：只退役差分几何 d2_rk/d2_qc。

        A/B #6（fnd86 · decay 10 · 3 字段 × 4 族）实测：d2 两族 6/6 <1.0 与 §6 同向；
        ed_rk（1.48/2.91/1.31）与 dw（1.10/2.48/0.82）都被证伪 ⇒ level 族恢复。
        报告：reports/ind_campaign_template_eval_20261026.md §11。
        WQB_LEGACY_FAMILIES ⇒ 全量回退旧笛卡尔积（两侧都断言，防止反向改动）。
        """
        g = generate
        self.assertFalse(g._family_enabled("d2_rk", "change"))
        self.assertFalse(g._family_enabled("d2_qc", "discrete_rating"))
        # level 几何族：A/B #6 证伪了退役 ⇒ 任何形态都必须放行
        for fam in ("ed_rk", "ir_pl", "dw", "lvl_rk"):
            for form in ("event_date", "level_ratio", "other", "change"):
                self.assertTrue(g._family_enabled(fam, form), f"{fam} 在 {form} 形态下应已恢复")
        with patch.object(g, "LEGACY_FAMILIES", True):
            for fam in ("d2_rk", "d2_qc"):
                self.assertTrue(g._family_enabled(fam, "other"), f"LEGACY 必须放行 {fam}")

    def test_build_exprs_drops_retired_families(self):
        """build_exprs 实际产出面上，只有 d2_* 不再出现在默认笛卡尔积里。

        用 `_force_full=True` 绕开形态减法与 35% 安全阀，直接看「全交叉」是什么。
        """
        def fams(form, **kw):
            sel = [dict(self.FIELD_M, tier="full", form=form, ftier="transparent")]
            return [t for t, _ in generate.build_exprs(sel, "annual", cat="FUNDAMENTAL", **kw)]

        full = fams("other", _force_full=True)
        for fam in ("d2_rk", "d2_qc"):
            self.assertNotIn(fam, full, f"{fam} 应已从默认笛卡尔积退役")
        for fam in ("lvl_rk", "ed_rk", "ir_pl", "dw"):
            self.assertIn(fam, full, f"{fam} 未被 A/B #6 证伪，必须留在全交叉里")
        self.assertIn("lvl_rk", fams("level_ratio"), "形态命中时族的保留由 FORM_FAMILIES 决定")
        self.assertIn("dw", fams("level_ratio"))
        with patch.object(generate, "LEGACY_FAMILIES", True):
            legacy = fams("other", _force_full=True)
        for fam in ("d2_rk", "d2_qc"):
            self.assertIn(fam, legacy, f"LEGACY 回退应恢复 {fam}")

    def test_tl_restored_for_gated_category(self):
        """tl（单窗 tail 门控）随 level 族一起恢复：§6 的 9 行 0 命中是 decay 4 旧几何。

        A/B #6 只证伪了 level 族的退役（ed_rk/dw ≥1.0），tl 按「未证伪即保留」恢复；
        pp 是 IND 唯一被证实能过 prod 墙的门控，两者并存。
        """
        sel = [dict(self.FIELD_M, tier="full", form="other", ftier="transparent")]
        got = [t for t, _ in generate.build_exprs(sel, "annual", cat="SENTIMENT", _force_full=True)]
        self.assertIn("tl", got, "tl 已恢复（A/B #6 未证伪 level 族退役）")
        self.assertIn("pp", got, "pp 是 IND 唯一被证实能过 prod 墙的门控，必须保留")

    def test_blackbox_families_keep_dw(self):
        """dw 经 A/B #6 证伪（fnd86 · decay 10：1.10 / 2.48 / 0.82）⇒ 回到黑盒族集合。"""
        self.assertIn("dw", generate.BLACKBOX_FAMILIES)
        self.assertIn("pp", generate.BLACKBOX_FAMILIES)
        self.assertIn("lvl_rk", generate.BLACKBOX_FAMILIES)
        self.assertFalse(hasattr(generate, "_BLACKBOX_FAMILIES"),
                         "dw 恢复后不再需要 _BLACKBOX_FAMILIES 这层间接")

    def test_atom_only_skips_residual_family(self):
        """WQB_ATOM_ONLY 开关（2026-10-26 用户口径「IND 优先挖掘 ATOM」）。

        残差族把 PV 的 `returns` 当回归自变量 ⇒ 属跨数据集腿，不是 ATOM。
        开关打开时必须整族返回空；关着时照常产出 res/reslag。
        两侧都断言，防止 `if not ATOM_ONLY` 之类的反向改动静默吞掉或复活整族。
        """
        sel = [{"field_name": "assets", "field_type": "MATRIX", "sem_type": "value",
                "tier": "full", "form": "single"}]
        with patch.object(generate, "ATOM_ONLY", False):
            out = generate.build_residual(sel, cat="FUNDAMENTAL")
            self.assertEqual({t for t, _ in out}, {"res", "reslag"})
        with patch.object(generate, "ATOM_ONLY", True):
            self.assertEqual(generate.build_residual(sel, cat="FUNDAMENTAL"), [])


class TestEmitDigest(unittest.TestCase):
    def test_rerun_replaces_line_not_appends(self):
        with tempfile.TemporaryDirectory() as td:
            dg = os.path.join(td, "d.md")
            pg = os.path.join(td, "p.json")
            ck = {"done": ["demo"]}
            res = {"results": {"demo": {"verdict": "ALIVE", "max_s": 1.6, "max_2y": 1.7,
                                        "n_joint": 0, "n_alphas": 3, "prod_top": 0.5}}}
            with patch.object(report, "DIGEST", dg), patch.object(report, "PROGRESS", pg):
                report.emit_digest("demo", "MODEL", res, ck, 169)
                report.emit_digest("demo", "MODEL", res, ck, 169)
            lines = [l for l in open(dg, encoding="utf-8") if l.startswith("- ")]
            self.assertEqual(len(lines), 1, f"digest 行数应为 1，实际 {lines}")


class TestBadTokensGuards(unittest.TestCase):
    """2026-10-25 事故回归：`ts_backfill` 被误拉黑 ⇒ 所有模板族被丢 ⇒ 72 个集判 NO_DATA。"""

    def test_structural_operator_cannot_be_blacklisted(self):
        from wqb_campaign import bad_tokens as bt
        saved = bt.BAD_TOKENS
        try:
            bt.BAD_TOKENS = set()
            got = bt.note_bad_tokens(['inaccessible or unknown operator "ts_backfill"'], verbose=False)
            self.assertEqual(got, set(), "结构算子不应被写入黑名单")
            self.assertNotIn("ts_backfill", bt.BAD_TOKENS)
        finally:
            bt.BAD_TOKENS = saved

    def test_ghost_field_still_blacklisted(self):
        from wqb_campaign import bad_tokens as bt
        saved = bt.BAD_TOKENS
        try:
            bt.BAD_TOKENS = set()
            got = bt.note_bad_tokens(['unknown variable "earnings_volatility_trend"'], verbose=False)
            self.assertIn("earnings_volatility_trend", got)
        finally:
            bt.BAD_TOKENS = saved

    def test_filter_refuses_to_drop_everything(self):
        from wqb_campaign import bad_tokens as bt
        saved = bt.BAD_TOKENS
        try:
            bt.BAD_TOKENS = {"ts_backfill"}
            e2 = [("lvl_rk", "rank(ts_backfill(x,22))"),
                  ("d1_rk", "rank(ts_delta(ts_backfill(x,22),22))")]
            self.assertEqual(bt.filter_bad(e2)[1], 0)
            e6 = [(f"t{i}", f"rank(ts_backfill(x,{i}))") for i in range(6)]
            self.assertEqual(bt.filter_bad(e6)[1], 0)
        finally:
            bt.BAD_TOKENS = saved

    def test_filter_still_drops_real_bad_field(self):
        from wqb_campaign import bad_tokens as bt
        saved = bt.BAD_TOKENS
        try:
            bt.BAD_TOKENS = {"ghost_field"}
            e = [("a", "rank(ghost_field)"), ("b", "rank(ts_backfill(x,22))"),
                 ("c", "rank(ts_delta(x,22))"), ("d", "rank(rank(x))"),
                 ("e", "rank(ts_mean(x,22))")]
            self.assertEqual(bt.filter_bad(e)[1], 1)
        finally:
            bt.BAD_TOKENS = saved


class TestSupervisorFuse(unittest.TestCase):
    """2026-10-25 空转事故：72 个集 n_alphas=0 却一路跑到 169 才被发现 ⇒ 需要熔断。"""

    def setUp(self):
        # 2026-10-25 迁移：campaign_supervisor.py → IND skill 自带 ind_runner.py
        # ⚠ ind_runner.py 在**模块 import 时**把 WQB_CAMPAIGN_REGION 钉成 IND（生产需要：
        #   它 spawn 的 ind_main.py 靠 env 继承区域）。本进程 import 一次就会泄漏给后续用例，
        #   而区域相关模块常量按**各自首次 import 时**的 config.REGION 定档
        #   （sweep.SWEEP_VARIANTS / REGION_SETTINGS 等）⇒ 之后 TestRegionParam 的
        #   finally 会把这个泄漏值当"旧值"恢复，TestProdTarget 再 import pipeline_ind 时
        #   sweep 就绑到 IND 表（2026-10-26 实测：整文件跑才红的顺序耦合）。
        #   这里 import 后立即还原，测试进程的区域状态不接受副作用。
        old = os.environ.get("WQB_CAMPAIGN_REGION")
        try:
            import ind_runner as sup
        finally:
            if old is None:
                os.environ.pop("WQB_CAMPAIGN_REGION", None)
            else:
                os.environ["WQB_CAMPAIGN_REGION"] = old
        self.sup = sup

    def test_counts_trailing_zero_alpha(self):
        done = ["ok1", "z1", "z2", "z3"]
        res = {"ok1": {"verdict": "DEAD", "n_alphas": 50},
               "z1": {"verdict": "NO_DATA", "n_alphas": 0},
               "z2": {"verdict": "NO_DATA", "n_alphas": 0},
               "z3": {"verdict": "NO_DATA", "n_alphas": 0}}
        self.assertEqual(self.sup.zero_alpha_streak(done, res), 3)

    def test_skip_verdicts_are_ignored_not_counted(self):
        done = ["z1", "skip1", "z2"]
        res = {"z1": {"verdict": "NO_DATA", "n_alphas": 0},
               "skip1": {"verdict": "SKIPPED_LOW_COV", "n_alphas": None},
               "z2": {"verdict": "NO_DATA", "n_alphas": 0}}
        self.assertEqual(self.sup.zero_alpha_streak(done, res), 2)

    def test_healthy_dataset_breaks_streak(self):
        done = ["z1", "z2", "good", "z3"]
        res = {"z1": {"verdict": "NO_DATA", "n_alphas": 0},
               "z2": {"verdict": "NO_DATA", "n_alphas": 0},
               "good": {"verdict": "DEAD", "n_alphas": 42},
               "z3": {"verdict": "NO_DATA", "n_alphas": 0}}
        self.assertEqual(self.sup.zero_alpha_streak(done, res), 1)

    def test_sim_fail_without_alphas_counts(self):
        # SIM_FAIL/SIM 异常同样"没产出"，是管道坏的信号，应计入
        done = ["a", "b"]
        res = {"a": {"verdict": "SIM_FAIL", "n_alphas": 0},
               "b": {"verdict": "SIM_FAIL", "n_alphas": 0}}
        self.assertEqual(self.sup.zero_alpha_streak(done, res), 2)

    def test_empty_inputs(self):
        self.assertEqual(self.sup.zero_alpha_streak([], {}), 0)


class TestRegionParam(unittest.TestCase):
    """2026-10-25 为 IND 开波做的区域参数化。

    最关键的一条：**断点/结果/digest 必须按区域隔离**，否则 IND 会与 EUR 共用 done 列表互相覆盖。
    """

    def test_ind_paths_isolated_and_settings_switched(self):
        import importlib
        import wqb_campaign.config as cfg
        old = os.environ.get("WQB_CAMPAIGN_REGION")
        os.environ["WQB_CAMPAIGN_REGION"] = "IND"
        try:
            importlib.reload(cfg)
            self.assertEqual(cfg.REGION, "IND")
            for p in (cfg.CKPT, cfg.LOG, cfg.DIGEST, cfg.PROGRESS):
                self.assertIn("_IND", os.path.basename(p), f"{p} 未按区域隔离")
            self.assertIn("ind_lit_counts", os.path.basename(cfg.LIT_CACHE))
            s = cfg.REGION_SETTINGS
            self.assertEqual((s["universe"], s["neutralization"]), ("TOP500", "STATISTICAL"))
            # IND 与 EUR 的两个关键差异：nanHandling / maxTrade 都是 OFF
            self.assertEqual(s["nan_handling"], "OFF")
            self.assertEqual(s["max_trade"], "OFF")
        finally:
            if old is None:
                os.environ.pop("WQB_CAMPAIGN_REGION", None)
            else:
                os.environ["WQB_CAMPAIGN_REGION"] = old
            importlib.reload(cfg)

    def test_eur_keeps_original_paths(self):
        import importlib
        import wqb_campaign.config as cfg
        old = os.environ.pop("WQB_CAMPAIGN_REGION", None)
        try:
            importlib.reload(cfg)
            self.assertEqual(cfg.REGION, "EUR")
            self.assertNotIn("_EUR", os.path.basename(cfg.CKPT), "EUR 不应加后缀（会丢既有断点）")
            self.assertEqual(cfg.REGION_SETTINGS["neutralization"], "FAST")
            self.assertEqual(cfg.REGION_SETTINGS["max_trade"], "ON")
        finally:
            if old is not None:
                os.environ["WQB_CAMPAIGN_REGION"] = old
            importlib.reload(cfg)


class TestRobustGeom(unittest.TestCase):
    """robust 几何族（2026-10-26）：模板库缺的那三条已验证杠杆。

    背景（runbook §9.8 第 3 层）：旧 14 个模板全是 L2_NORM(L1_EXTRACT(field))，
    没有一个 group 算子；而 fnd86 史册里唯一有效的三个杠杆——
    短 bf(22) + 固定 z 窗(252) + **decay 10**、group_rank(·, sector)、连续 z 上 signed_power(·,3)
    ——一个都没进来 ⇒ IND 的 ATOM 全部卡在 robust（0.78–0.99，闸线 1.0）。
    这里把「结构本身」钉死，防止后续重构又退回单调归一。
    """

    FIELD_M = {"field_name": "demo_field", "field_type": "MATRIX", "sem_type": "value",
               "tier": "full", "form": "single"}
    FIELD_V = {"field_name": "demo_vec", "field_type": "VECTOR", "sem_type": "count",
               "tier": "full", "form": "single"}

    def test_env_gate_defaults_off_outside_ind(self):
        # 测试环境 REGION=EUR ⇒ 默认不产（只有 IND 的 robust 闸是 1.0 绝对线）
        with patch.object(generate, "ROBUST_GEOM", False):
            self.assertEqual(generate.build_robust_geom([self.FIELD_M]), [])
        with patch.object(generate, "ROBUST_GEOM", True):
            self.assertTrue(generate.build_robust_geom([self.FIELD_M]))

    def test_eleven_templates_balanced_and_within_10_calls(self):
        self.assertEqual(len(generate.ROBUST_TPL), 11)
        # 调用点上限：引擎自设 ≤10 控复杂度（REGULAR 平台无硬上限，见 brain-alpha-robustness）。
        # 例外 = 两个「dev + 居中凸」模板（各 12）：dev（除以 |均值|，是 prod 0.7672→0.6989
        # 的唯一来源）与「居中后再凸」两把钥匙叠加，压不到 10；成品 MP0JYmL8 / 58jPrvZ1
        # 均实测平台 FULL 仿真通过且全闸 pass，故登记例外而不是退回 z 版（z 版 prod 0.7672 ✗）。
        cap = {"rg_grdev_p3": 12, "rg_grdev_p3_sec": 12}
        for r in (self.FIELD_M, self.FIELD_V):
            for tpl in generate.ROBUST_TPL:
                e = generate.build_one_family(tpl, r, "annual")
                self.assertIsNotNone(e, f"{tpl} 返回 None")
                self.assertTrue(balanced(e), f"{tpl} 括号不平衡: {e}")
                self.assertLessEqual(count_calls(e), cap.get(tpl, 10),
                                     f"{tpl} 调用点 {count_calls(e)} > {cap.get(tpl, 10)}: {e}")

    def test_geometry_is_not_old_monotone_normalization(self):
        e = generate._robust_expr("rg_rkz", self.FIELD_M)
        self.assertEqual(e, "rank(ts_zscore(ts_backfill(demo_field, 22), 252))")
        # 旧几何 | 新几何的三个杠杆，缺一条就退回「单调归一」那套
        self.assertIn(f", {generate.RG_BF})", e)          # 短 backfill 22（不是 freq 表的 252）
        self.assertIn(f", {generate.RG_ZW})", e)          # 固定 z 窗 252
        self.assertNotIn("ts_rank(", e)                   # ts_rank(x,252) 实测 robust 0.96 ✗
        self.assertEqual(generate.RG_BF, 22)
        self.assertEqual(generate.RG_ZW, 252)
        self.assertEqual(generate.ROBUST_DECAY, 10)       # 未登记族的回落档（z/rank/dev 实测 10）

    def test_decay_by_template_matches_platform_winners(self):
        """decay 按结构分档（2026-10-26）：两颗全闸 ATOM 成品的实测设置。

        ⚠ 旧实现全局 ROBUST_DECAY=10 ⇒ 居中凸族（成品 decay=6）与 lvvol 族（成品 decay=2）
        跑的是未验证设置，电池复现不出自己的赢家（A/B #1/#2）。
        """
        self.assertEqual(generate.robust_decay("rg_rkz"), 10)
        self.assertEqual(generate.robust_decay("rg_grz"), 10)
        self.assertEqual(generate.robust_decay("rg_rkdev"), 10)
        self.assertEqual(generate.robust_decay("rg_grdev_p3"), 6)          # 58jPrvZ1
        self.assertEqual(generate.robust_decay("rg_grdev_p3_sec"), 6)
        self.assertEqual(generate.robust_decay("rg_grdev_p3_sec_neg"), 6)  # 镜像后缀要剥
        self.assertEqual(generate.robust_decay("rg_lvvol"), 2)             # gJWnrZgg
        self.assertEqual(generate.robust_decay("rg_lvvol_sec"), 2)
        self.assertEqual(generate.robust_decay("rg_lvvol_sec_cx"), 2)      # 载体扩散后缀要剥
        self.assertEqual(generate.robust_decay("lvl_rk"), 10)              # 非 rg 族回落
        self.assertEqual(generate.robust_decay(None), 10)

    def test_reproduces_two_ind_winner_codes(self):
        """A/B #1/#2（报告 §9）：电池构造必须与平台两颗全闸 ATOM 成品的 code 逐字一致。

        gJWnrZgg（S2.14/F1.70/2Y1.99/sub0.93/rob1.02）：rg_lvvol_sec，smooth 2 + decay 2。
        58jPrvZ1（S1.64/F1.27/2Y2.23/sub1.55/rob1.12）：rg_grdev_p3_sec，decay 6，且 VECTOR
            字段**带** ts_backfill（analyst_consensus 必须在 RG_BACKFILL_DS 缺省白名单里）。
        任何一处改动（smooth / bf / allowlist / dev 形态）都会让这两条断言变红。
        """
        with patch.object(generate, "RG_LV_SMOOTH", 2):
            lv = generate.build_one_family(
                "rg_lvvol_sec",
                {"field_name": "fnd86_earnings_score", "field_type": "MATRIX",
                 "sem_type": "value"}, "quarterly", ds="fundamental86")
        self.assertEqual(
            lv,
            "group_rank(ts_mean(ts_backfill(multiply(fnd86_earnings_score, "
            "add(ts_std_dev(fnd86_earnings_score, 65), 1)), 22), 2), sector)")
        self.assertEqual(generate.robust_decay("rg_lvvol_sec"), 2)

        dev = generate.build_one_family(
            "rg_grdev_p3_sec",
            {"field_name": "mean_flash_estimate_ebt_annual12", "field_type": "VECTOR",
             "sem_type": "value"}, "annual", ds="analyst_consensus")
        self.assertEqual(
            dev,
            "signed_power(subtract(group_rank(divide(subtract("
            "ts_backfill(vec_avg(mean_flash_estimate_ebt_annual12), 22), "
            "ts_mean(ts_backfill(vec_avg(mean_flash_estimate_ebt_annual12), 22), 252)), "
            "add(abs(ts_mean(ts_backfill(vec_avg(mean_flash_estimate_ebt_annual12), 22), 252)), 1)), "
            "sector), 0.5), 3)")
        self.assertEqual(generate.robust_decay("rg_grdev_p3_sec"), 6)
        # 缺省允许 backfill：58jPrvZ1 的逐字 code 就带 ts_backfill(vec_avg(...), 22)
        self.assertIn("analyst_consensus", generate.RG_BACKFILL_DS)

    def test_group_and_convex_levers_present(self):
        g = generate._robust_expr("rg_grz", self.FIELD_M)
        self.assertIn("group_rank(", g)
        self.assertIn("sector", g)
        gi = generate._robust_expr("rg_grdev_ind", self.FIELD_M)
        self.assertIn("group_rank(", gi)
        self.assertIn("industry", gi)
        p = generate._robust_expr("rg_grz_p3", self.FIELD_M)
        self.assertIn("signed_power(", p)
        self.assertTrue(p.endswith(", 3)"), f"凸指数必须是 3（≥1.5 才凸）: {p}")
        d = generate._robust_expr("rg_grdev", self.FIELD_M)
        self.assertIn("divide(subtract(", d)
        self.assertIn("abs(", d)

    def test_centered_convex_and_vol_scaled_level(self):
        """2026-10-26 实证补进来的两把钥匙（旧 7 族里都没有）。

        ① 居中再凸：group_rank∈[0,1] 直接 signed_power 只压前半段，
           居中到 [-0.5,0.5] 才是「放大两端」⇒ analyst 族 robust 0.86→1.22、S1.49→1.53。
        ② 波动缩放水平项：multiply(F, 1+ts_std_dev(F,65)) 再 bf22+平滑
           ⇒ fnd86 族 smooth2/decay2 S2.14/robust 1.02（成品 gJWnrZgg）、smooth5 S2.18/robust 1.06（无分组）。
        """
        p = generate._robust_expr("rg_grdev_p3", self.FIELD_M)
        self.assertIn("signed_power(subtract(group_rank(", p)
        self.assertTrue(p.endswith(", 0.5), 3)"), p)
        self.assertIn("industry", p)

        # sector 轴同几何：2026-10-26 同批实测比 industry 版强一档
        # （S1.56→1.64 / sub1.49→1.55 / 2Y1.85→2.23，成品 58jPrvZ1 全闸 pass）
        ps = generate._robust_expr("rg_grdev_p3_sec", self.FIELD_M)
        self.assertIn("signed_power(subtract(group_rank(", ps)
        self.assertTrue(ps.endswith(", 0.5), 3)"), ps)
        self.assertIn("sector", ps)

        lv = generate._robust_expr("rg_lvvol", self.FIELD_M)
        self.assertEqual(generate.RG_LV_STD, 65)
        # 平滑档按区域定档：IND=2（成品 gJWnrZgg decay2 全闸过），其余区域沿用 5。
        # 测试进程是 EUR ⇒ RG_LV_SMOOTH 走 5；IND 的行为在下面 test_reproduces... 用 patch 验证。
        self.assertEqual(generate.default_lv_smooth("IND"), 2)
        self.assertEqual(generate.default_lv_smooth("EUR"), 5)
        # 模块常量在 import 时按当时区域定档（不可与 config.REGION 比：本文件另有用例
        # importlib.reload(config) 临时改区域，测试顺序随机时读到的是瞬时值）
        self.assertIn(generate.RG_LV_SMOOTH, (2, 5))
        self.assertIn("ts_std_dev(demo_field, 65)", lv)
        self.assertIn(
            f"ts_backfill(multiply(demo_field, add(ts_std_dev(demo_field, 65), 1)), {generate.RG_BF})", lv)
        self.assertTrue(lv.startswith("rank("), lv)

        lvs = generate._robust_expr("rg_lvvol_sec", self.FIELD_M)
        self.assertIn("group_rank(", lvs)
        self.assertIn("sector", lvs)
        # VECTOR 默认剥 backfill：波动缩放项也必须跟着剥
        with patch.object(generate, "RG_BACKFILL_DS", set()):
            e = generate.build_one_family("rg_lvvol", self.FIELD_V, "annual", ds="demo")
            self.assertNotIn("ts_backfill", e)

    def test_templates_are_atom_pure(self):
        """robust 族必须单数据集：混进 PV 的 returns/cap/close 就不再是 ATOM。"""
        import re
        for tpl in generate.ROBUST_TPL:
            for r in (self.FIELD_M, self.FIELD_V):
                e = generate.build_one_family(tpl, r, "annual")
                for tok in ("returns", "cap", "close"):
                    self.assertIsNone(re.search(rf"\b{tok}\b", e),
                                      f"{tpl} 混入 PV 字段 {tok}: {e}")

    def test_vector_backfill_stripped_unless_allowlisted(self):
        with patch.object(generate, "RG_BACKFILL_DS", set()):
            e = generate.build_one_family("rg_rkz", self.FIELD_V, "annual", ds="demo")
            self.assertNotIn("ts_backfill", e)
        with patch.object(generate, "RG_BACKFILL_DS", {"demo"}):
            e2 = generate.build_one_family("rg_rkz", self.FIELD_V, "annual", ds="demo")
            self.assertIn("ts_backfill", e2)

    def test_probe_and_skip_fields_excluded(self):
        probe = dict(self.FIELD_M, tier="probe")
        skip = dict(self.FIELD_M, form="skip")
        with patch.object(generate, "ROBUST_GEOM", True), \
                patch.object(generate, "ROBUST_PROBE", False):
            self.assertEqual(generate.build_robust_geom([probe, skip]), [])

    def test_probe_gets_only_the_robust_probe_template(self):
        """探针层仍需 robust 信号（2026-10-26 P1-4）：开时只跑 ROBUST_PROBE_TPL，1 条/字段。

        依据：`lvl_rk` 是全库信息量最低的族（中位 S 0.00），而 IND 的闸问的是「稳健几何下
        有没有方向」——sentiment21 全电池 best 1.12(lvl_rk) 判 DEAD，同字段手工 dev 却 rob1.38。
        成本纪律是「1 条/字段」，不是「11 族」：全 11 族会让探针从 2 批涨到 22 批。
        """
        probe = dict(self.FIELD_M, tier="probe")
        skip = dict(self.FIELD_M, form="skip")
        with patch.object(generate, "ROBUST_GEOM", True), \
                patch.object(generate, "ROBUST_PROBE", True):
            got = generate.build_robust_geom([probe, skip])
        self.assertEqual([t for t, _ in got], list(generate.ROBUST_PROBE_TPL),
                         "探针层必须只跑 ROBUST_PROBE_TPL（skip 字段仍排除）")
        self.assertIn(generate.ROBUST_PROBE_TPL[0], generate.ROBUST_TPL,
                      "探针模板必须来自 ROBUST_TPL，否则 _robust_expr 返回 None")
        # 探针表达式与全字段版逐字相同 ⇒ 才能与 rg 组共用同一批（同 tpl 同 decay 合并）
        self.assertEqual(got[0][1],
                         generate.build_one_family("rg_grdev_p3_sec", self.FIELD_M, "annual"))
        # 探针批必须落结构自己的 decay（6），不能掉进缺省 10/区域 4
        self.assertEqual(generate.robust_decay(generate.ROBUST_PROBE_TPL[0]), 6)

    def test_atom_only_does_not_suppress_robust_geom(self):
        # ATOM_ONLY 只关残差族（吃 PV returns）；robust 族是单数据集，必须照产
        with patch.object(generate, "ROBUST_GEOM", True), \
                patch.object(generate, "ATOM_ONLY", True):
            self.assertTrue(generate.build_robust_geom([self.FIELD_M]))


class TestPostproc(unittest.TestCase):
    """后处理电池的幂次（2026-10-26）。

    `signed_power(code, 0.7)` 是凹变换（压尾），而 fnd86 史册实证有效方向是凸（≥1.5：
    `signed_power(·,3)` 把 robust 从 0.9x 抬到 1.00）⇒ IND 缺省改 3，其余区域保持 0.7。
    """

    def test_signed_power_honours_configured_pow(self):
        codes = [c for _, c in generate.build_postproc("rank(x)")]
        self.assertTrue(any(c == f"signed_power(rank(x), {generate.PP_POW:g})" for c in codes),
                        f"未按 PP_POW={generate.PP_POW} 构造：{codes}")
        with patch.object(generate, "PP_POW", 3.0):
            codes3 = [c for _, c in generate.build_postproc("rank(x)")]
        self.assertIn("signed_power(rank(x), 3)", codes3)
        with patch.object(generate, "PP_POW", 0.7):
            codes7 = [c for _, c in generate.build_postproc("rank(x)")]
        self.assertIn("signed_power(rank(x), 0.7)", codes7)


class TestHarvestRow(unittest.TestCase):
    """收割脚本 stdout 的 `rob=` 字段（2026-10-26）。

    旧脚本只输出 S/F/tvr/2Y/sub ⇒ robust 闸完全没有输入，pipeline 只能拿 S 选 prod 目标，
    每次都挑到 robust 0.8x 的高 S 废料。缺字段必须降级成 None（fail-closed），
    不能把 sentinel -99 当真实值送进闸门比较。
    """

    def test_parse_with_rob(self):
        out = ("+ ABC123 S=1.61 F=1.13 tvr=0.123 2Y=2.96 sub=1.26 rob=1.02\n"
               "x kid9 msg=HTTP 500 on child sim\n"
               "status=COMPLETE children=10\n")
        rows, errs = transport.parse_rows(out)
        self.assertEqual(rows, [("ABC123", 1.61, 1.13, 2.96, 1.26, 1.02)])
        self.assertEqual(errs, ["HTTP 500 on child sim"])

    def test_parse_legacy_without_rob(self):
        rows, _ = transport.parse_rows("+ ABC123 S=1.2 F=0.9 tvr=na 2Y=1.5 sub=1.1\n")
        self.assertEqual(rows, [("ABC123", 1.2, 0.9, 1.5, 1.1, None)])

    def test_sentinel_becomes_none(self):
        rows, _ = transport.parse_rows(
            "+ ABC123 S=1.2 F=0.9 tvr=0.1 2Y=1.5 sub=1.1 rob=-99.00\n")
        self.assertIsNone(rows[0][5])
        self.assertIsNone(transport._val_or_none("-99.00"))

    def test_row6_accepts_legacy_5_tuple(self):
        self.assertEqual(transport.row6(("A", 1.0, 0.9, 1.1, 0.8)), ("A", 1.0, 0.9, 1.1, 0.8, None))
        self.assertEqual(transport.row6(("A", 1.0, 0.9, 1.1, 0.8, 1.03)),
                         ("A", 1.0, 0.9, 1.1, 0.8, 1.03))
        self.assertIsNone(transport.row6(None))
        self.assertIsNone(transport.row6(("A", 1.0)))


class TestSimIdParse(unittest.TestCase):
    """派发输出解析（2026-10-26 事故回归）。

    旧实现指向仓库外的 `~/wqb-scripts/wqb_tools.py`（未跟踪、无备份）。该文件消失后
    dispatch 全场返回 None，战役表面在跑、实际一个作业都没派出。现改为调用仓库内
    `tools/submit_batch.py`，从 `status=201 -> <Location>` 取 id。
    """

    def test_location_url(self):
        out = ("[x.txt] n=10 decay=10 neut=STATISTICAL overrides={}\n"
               "  status=201 -> https://api.worldquantbrain.com/simulations/3xkQ9mZ\n"
               "ALL SUBMITTED (1 批)\n")
        self.assertEqual(transport._sim_id_from_output(out), "3xkQ9mZ")

    def test_trailing_slash(self):
        out = "  status=201 -> https://api.worldquantbrain.com/simulations/3xkQ9mZ/\n"
        self.assertEqual(transport._sim_id_from_output(out), "3xkQ9mZ")

    def test_non_201_must_not_yield_id(self):
        # 失败行是 `status=400 -> `（Location 为空）；宽松匹配会把下一行 BODY 当 id
        out = ('  status=400 -> \n  BODY: {"detail": "bad"}\n'
               "PARTIAL/FAILED: 成功 0/1 批，失败 1 批\n")
        self.assertIsNone(transport._sim_id_from_output(out))

    def test_empty_output(self):
        self.assertIsNone(transport._sim_id_from_output(""))
        self.assertIsNone(transport._sim_id_from_output(None))

    def test_legacy_json_shape_still_supported(self):
        self.assertEqual(transport._sim_id_from_output('{"sim_id": "abc123"}'), "abc123")

    def test_dispatcher_is_repo_local_and_exists(self):
        # 仓库外脚本消失过一次；派发器必须留在仓库内、受版本控制
        self.assertTrue(os.path.isfile(transport.SUBMIT_BATCH),
                        f"派发器不存在：{transport.SUBMIT_BATCH}")
        self.assertTrue(os.path.normcase(transport.SUBMIT_BATCH).startswith(
            os.path.normcase(transport.ROOT)))


class TestProdTarget(unittest.TestCase):
    """prod 探针目标选择（2026-10-26 事故回归）。

    旧实现无条件取 max_S ⇒ IND 里每次挑到的都是 robust 0.78–0.99 的高 S 废料，
    真正 robust 过线的候选**从没测过 prod**，于是「ATOM 全没过」的结论里混着假阴性。
    """

    @staticmethod
    def _a(aid, s, rob=None, y2=3.0, sub=1.2, f=1.1):
        return {"alpha": aid, "s": s, "f": f, "y2": y2, "sub": sub, "rob": rob}

    def test_prefers_robust_clean_over_higher_sharpe(self):
        from wqb_campaign import pipeline_ind
        cands = [self._a("HIGH_S_BAD_ROB", 1.70, rob=0.78),
                 self._a("ROB_CLEAN", 1.61, rob=1.02),
                 self._a("MID", 1.65, rob=0.99)]
        got = pipeline_ind.pick_prod_target(cands, g2y=1.0, gsub=1.0, grob=1.0)
        self.assertEqual(got["alpha"], "ROB_CLEAN")

    def test_robust_candidate_must_still_pass_ra_gates(self):
        from wqb_campaign import pipeline_ind
        cands = [self._a("ROB_BUT_2Y_FAIL", 1.75, rob=1.01, y2=0.5),
                 self._a("RA_CLEAN_NO_ROB", 1.60, rob=None, y2=2.9)]
        got = pipeline_ind.pick_prod_target(cands, g2y=1.0, gsub=1.0, grob=1.0)
        self.assertEqual(got["alpha"], "RA_CLEAN_NO_ROB")

    def test_falls_back_to_max_sharpe(self):
        from wqb_campaign import pipeline_ind
        cands = [self._a("A", 1.40, rob=0.8), self._a("B", 1.55, rob=0.9)]
        got = pipeline_ind.pick_prod_target(cands, g2y=1.0, gsub=1.0, grob=1.0)
        self.assertEqual(got["alpha"], "B")

    def test_eur_keeps_old_max_sharpe_behaviour(self):
        from wqb_campaign import pipeline_ind
        cands = [self._a("A", 1.70, rob=0.5), self._a("B", 1.60, rob=None)]
        got = pipeline_ind.pick_prod_target(cands, g2y=1.58, gsub=None, grob=None)
        self.assertEqual(got["alpha"], "A")

    def test_val_sentinel(self):
        from wqb_campaign import pipeline_ind
        self.assertIsNone(pipeline_ind._val(-99))
        self.assertIsNone(pipeline_ind._val(None))
        self.assertEqual(pipeline_ind._val(1.02), 1.02)
        self.assertIsNone(pipeline_ind.pick_prod_target(
            [self._a("X", None)], g2y=1.0, gsub=1.0, grob=1.0))


class TestSettingsSweep(unittest.TestCase):
    """近闸集设置轴补扫（P0-3，2026-10-26）。

    旧实现三个坑，都直接烧平台配额：
    ① IND 的 universe 只有 TOP500 ⇒ `u2500` 变体必然无效派发；
    ② 两条候选基座 decay 不同还塞进同一批 ⇒ `dispatch` 只有一套 settings，只能拆成 n=1 批，
       而单条批必为 `COMPLETE children=0`（永远收不到结果）；
    ③ 变体表缺 decay 轴 —— 两颗成品恰恰是 decay6 / decay2 才过闸的。
    """

    @staticmethod
    def _a(tpl, s, aid="A"):
        return {"alpha": aid, "tpl": tpl, "s": s, "f": 1.1, "y2": 1.2,
                "sub": 1.0, "rob": 1.0}

    def test_ind_variants_have_decay_axes_and_no_u2500(self):
        tags = [t for t, _ in config.SWEEP_VARIANTS_BY_REGION["IND"]]
        self.assertEqual(tags, ["d6", "d2", "subind", "crowd"])
        self.assertNotIn("u2500", tags, "IND 的 universe 只有 TOP500，u2500 是白烧")
        # 其它区域仍是历史三变体（含 u2500）
        self.assertIn("u2500", [t for t, _ in config.DEFAULT_SWEEP_VARIANTS])

    def test_base_decay_by_structure(self):
        from wqb_campaign import sweep
        self.assertEqual(sweep._base_decay("rg_lvvol_sec"), 2)
        self.assertEqual(sweep._base_decay("rg_grdev_p3"), 6)
        self.assertEqual(sweep._base_decay("rg_rkz"), 10, "未登记的 robust 族回落 10")
        self.assertEqual(sweep._base_decay("lvl_rk"), 4, "非 robust 族走区域缺省 decay")
        self.assertEqual(sweep._base_decay(None), 4)

    def test_is_atom_row(self):
        from wqb_campaign import sweep
        for tpl in ("res", "reslag", "pp", "tl"):
            self.assertFalse(sweep._is_atom_row(self._a(tpl, 1.5)), f"{tpl} 不是 ATOM 族")
        self.assertFalse(sweep._is_atom_row(self._a("sw_d6", 1.5)), "sweep 自身的行不能再当目标")
        for tpl in ("lvl_rk", "dw", "rg_lvvol_sec", "d1_rk"):
            self.assertTrue(sweep._is_atom_row(self._a(tpl, 1.5)), f"{tpl} 应是 ATOM 族")

    def test_pick_pairs_atom_first_within_same_base_decay(self):
        from wqb_campaign import sweep
        cand = [self._a("res", 1.62, "RES_HIGH"),      # 非 ATOM 但 S 最高
                self._a("lvl_rk", 1.55, "ATOM_LVL"),
                self._a("dw", 1.40, "ATOM_DW")]
        got, dec = sweep._pick_pairs(cand)
        self.assertEqual(dec, 4)
        self.assertEqual([a["alpha"] for a in got], ["ATOM_LVL", "ATOM_DW"],
                         "组内有 ≥2 条 ATOM 时两席都给 ATOM，S 最高的非 ATOM 不占位")

    def test_pick_pairs_non_atom_fills_second_slot_when_atom_is_alone(self):
        from wqb_campaign import sweep
        cand = [self._a("res", 1.62, "RES_HIGH"),
                self._a("lvl_rk", 1.55, "ATOM_LVL")]
        got, dec = sweep._pick_pairs(cand)
        self.assertEqual(dec, 4)
        self.assertEqual([a["alpha"] for a in got], ["ATOM_LVL", "RES_HIGH"])

    def test_pick_pairs_skips_singleton_group_even_if_higher(self):
        from wqb_campaign import sweep
        cand = [self._a("rg_lvvol_sec", 1.57, "HIGH_BUT_ALONE"),   # decay 2，组内只有 1 条
                self._a("lvl_rk", 1.50, "A"),
                self._a("d1_rk", 1.45, "B")]                       # 两条都在 decay 4
        got, dec = sweep._pick_pairs(cand)
        self.assertEqual(dec, 4)
        self.assertEqual([a["alpha"] for a in got], ["A", "B"])

    def test_pick_pairs_returns_empty_when_no_pair(self):
        from wqb_campaign import sweep
        cand = [self._a("res", 1.60, "X"), self._a("rg_lvvol_sec", 1.50, "Y")]
        self.assertEqual(sweep._pick_pairs(cand), ([], None))

    def test_variants_for_adds_nan_on_only_for_event_cats(self):
        from wqb_campaign import sweep
        base = [t for t, _ in sweep.SWEEP_VARIANTS]
        self.assertEqual([t for t, _ in sweep._variants_for("FUNDAMENTAL")], base)
        sent = [t for t, _ in sweep._variants_for("sentiment")]
        self.assertEqual(sent, base + ["nanon"], "事件/情绪类才补 nanHandling=ON")
        self.assertTrue({"INSIDERS", "OPTION", "NEWS", "SENTIMENT"} <= set(sweep.NAN_ON_CATS))

    def test_out_of_range_sweep_is_noop(self):
        from wqb_campaign import sweep
        st = {}
        self.assertEqual(sweep.settings_sweep("demo", [self._a("lvl_rk", 1.58)], st, {}, 1.58),
                         (1.58, {}))
        self.assertEqual(sweep.settings_sweep("demo", [self._a("lvl_rk", 1.10)], st, {}, 1.10),
                         (1.10, {}))
        self.assertEqual(sweep.settings_sweep("demo", [], st, {}, 1.30), (1.30, {}))

    def test_dispatch_uses_one_tag_per_variant(self):
        """一个变体内所有表达式必须同标签 —— 否则 dispatch 按标签分批退化成 n=1 空批。

        2026-10-26 实测：旧版按源模板打 `lvl_sc_d6`/`lvl_tr_d6` ⇒ 各 1 条批 ⇒ 平台
        `COMPLETE children=0`，`settings_sweep` 从来没出过结果。
        """
        from wqb_campaign import sweep
        seen = {}

        def fake_dispatch(items, ds, label, on_batch=None, settings=None):
            tags = {t for t, _ in items}
            self.assertEqual(len(tags), 1,
                             f"{label} 打了多个标签 ⇒ dispatch 分组后每条批只有 1 个孩子")
            self.assertGreaterEqual(len(items), 2, "单条批必为空批")
            seen[label] = (items, settings)
            return []

        cand = [dict(alpha="A1", tpl="lvl_sc", s=1.19, f=0.3, y2=1.7, sub=0.7, rob=None),
                dict(alpha="A2", tpl="lvl_tr", s=1.06, f=0.3, y2=0.8, sub=0.8, rob=None)]
        with patch.object(sweep, "fetch_codes",
                          lambda ids: {i: f"code_{i}" for i in ids}), \
                patch.object(sweep, "dispatch", fake_dispatch), \
                patch.object(sweep, "save_ckpt", lambda ck: None):
            sweep.settings_sweep("demo", cand, {"sims": {}}, {}, 1.2)
        self.assertTrue(seen, "sweep 未派发任何变体")
        # 断言按**当前区域表**推导，不硬编码 4：本文件的 import 期区域由
        # WQB_CAMPAIGN_REGION 决定（缺省 EUR）。写死 4 会让 IND 表下的 d6/d2 误红。
        var_map = dict(sweep._variants_for(None))
        base_dec = sweep._base_decay("lvl_sc")          # 非 robust 族 ⇒ 区域缺省 decay
        for label, (items, settings) in seen.items():
            var = var_map.get(label, {})
            expect = int(str(var.get("decay", base_dec)))
            self.assertEqual(int(str(settings.get("decay"))), expect,
                             f"{label} 的 decay 应为「基座 + 变体覆写」（覆写={var}）")
            self.assertEqual({e for _, e in items}, {"code_A1", "code_A2"},
                             f"{label} 丢表达式 ⇒ 该批次不完整")


class TestKeepFields(unittest.TestCase):
    """`--keep-fields` 强制占 full 席位（2026-10-26）。

    定向复挖 ATOM 时点名 6 个 analyst_consensus 字段，实测只有 2 个过覆盖率闸，
    其余降级成单条 lvl_rk 探针 ⇒ 新几何只跑在 2 个字段上，「结构行不行」的结论被污染。
    """

    KEEP = ["mean_flash_estimate_pretax_annual12",
            "mean_flash_estimate_eps_annual12_3",
            "mean_estimate_eps_annual12_3",
            "mean_flash_estimate_reportednet_annual12_2",
            "mean_flash_estimate_ebit_annual12_2",
            "mean_flash_estimate_ebt_annual12",
            "demo_id"]           # 名字像元数据 ⇒ 验证 keep 能穿过元数据丢弃

    def _db(self):
        con = sqlite3.connect(":memory:")
        con.executescript("""
        CREATE TABLE regions(id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE datasets(id INTEGER PRIMARY KEY, name TEXT, region_id INTEGER);
        CREATE TABLE fields(id INTEGER PRIMARY KEY, dataset_id INTEGER, field_name TEXT,
                            field_type TEXT, coverage REAL, description TEXT);
        CREATE TABLE field_semantic_type(region TEXT, dataset TEXT, field TEXT, sem_type TEXT);
        INSERT INTO regions VALUES (1, 'IND');
        INSERT INTO datasets VALUES (1, 'demo', 1);
        """)
        for i in range(10):
            con.execute("INSERT INTO fields(dataset_id, field_name, field_type, coverage, description)"
                        " VALUES (1, ?, 'MATRIX', 0.9, 'plain level field')",
                        (f"level_{i}",))
            con.execute("INSERT INTO field_semantic_type VALUES ('IND','demo',?, 'level')",
                        (f"level_{i}",))
        for i, n in enumerate(self.KEEP):
            cov = 0.2 if i % 2 == 0 else 0.9    # 一半低于覆盖率闸（偶数下标）
            con.execute("INSERT INTO fields(dataset_id, field_name, field_type, coverage, description)"
                        " VALUES (1, ?, 'MATRIX', ?, '')", (n, cov))
        return con

    def test_query_without_coverage_gate(self):
        con = self._db()
        with patch.object(fields, "REGION", "IND"):
            got = {r["field_name"] for r in fields._query_fields(con, "demo", names=self.KEEP)}
            self.assertEqual(got, set(self.KEEP))
            gated = {r["field_name"] for r in fields._query_fields(con, "demo", min_cov=0.5)}
        self.assertNotIn(self.KEEP[0], gated)      # 0.2 < 0.5

    def test_keep_fields_all_full_tier(self):
        con = self._db()
        with patch.object(fields, "REGION", "IND"), \
                patch.object(fields, "platform_fields", lambda ds: None), \
                patch.object(fields, "FULL_FIELD_CAP", 8):
            out = fields.select_fields(con, "demo", field_min_cov=0.5,
                                       keep_fields=self.KEEP)
        by = {r["field_name"]: r for r in out}
        for n in self.KEEP:
            self.assertIn(n, by, f"keep 字段 {n} 被丢掉")
            self.assertEqual(by[n]["tier"], "full", f"{n} 应为 full，实际 {by[n]['tier']}")
        self.assertGreaterEqual(len([r for r in out if r["tier"] == "full"]), len(self.KEEP))

    def test_only_names_does_not_expand_cap(self):
        """断点清单含 probe（最多 20 个），不能因为「续跑」就把上限撑大、把 probe 升成 full。"""
        con = self._db()
        all_names = [f"level_{i}" for i in range(10)] + self.KEEP
        with patch.object(fields, "REGION", "IND"), \
                patch.object(fields, "platform_fields", lambda ds: None), \
                patch.object(fields, "FULL_FIELD_CAP", 8):
            out = fields.select_fields(con, "demo", field_min_cov=0.5,
                                       only_names=all_names)
        self.assertLessEqual(len([r for r in out if r["tier"] == "full"]), 8,
                             "only_names 不应把续跑字段全部升成 full")

    def test_keep_fields_outrank_dimension_diversity(self):
        """keep 全部同属一个语义维时，不能被「每维先留 1 个」挤掉（2026-10-26 实测：6 只进 4）。"""
        con = sqlite3.connect(":memory:")
        con.executescript("""
        CREATE TABLE regions(id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE datasets(id INTEGER PRIMARY KEY, name TEXT, region_id INTEGER);
        CREATE TABLE fields(id INTEGER PRIMARY KEY, dataset_id INTEGER, field_name TEXT,
                            field_type TEXT, coverage REAL, description TEXT);
        CREATE TABLE field_semantic_type(region TEXT, dataset TEXT, field TEXT, sem_type TEXT);
        INSERT INTO regions VALUES (1, 'IND');
        INSERT INTO datasets VALUES (1, 'demo', 1);
        """)
        letters = "abcdefghijkl"
        for i, ch in enumerate(letters):    # 12 个非 keep 字段，覆盖率高且各占一个语义维
            nm = f"field_{ch}"              # ⚠ 名字不能以 _数字 结尾：同源去重会把 f_00..f_11 全并成 "f"
            con.execute("INSERT INTO fields(dataset_id, field_name, field_type, coverage, description)"
                        " VALUES (1, ?, 'MATRIX', 0.99, 'plain level field')", (nm,))
            con.execute("INSERT INTO field_semantic_type VALUES ('IND','demo',?, ?)",
                        (nm, f"dim_{i}"))
        for n in self.KEEP[:6]:             # keep 字段覆盖率全部低于闸，靠强制纳入
            con.execute("INSERT INTO fields(dataset_id, field_name, field_type, coverage, description)"
                        " VALUES (1, ?, 'MATRIX', 0.3, '')", (n,))
        with patch.object(fields, "REGION", "IND"), \
                patch.object(fields, "platform_fields", lambda ds: None), \
                patch.object(fields, "FULL_FIELD_CAP", 8):
            out = fields.select_fields(con, "demo", field_min_cov=0.5,
                                       keep_fields=self.KEEP[:6])
        full = {r["field_name"] for r in out if r["tier"] == "full"}
        for n in self.KEEP[:6]:
            self.assertIn(n, full, f"keep 字段 {n} 被维度多样性挤掉")
        self.assertEqual(len(full), 8)

    def test_unknown_keep_name_is_skipped_not_fatal(self):
        con = self._db()
        with patch.object(fields, "REGION", "IND"), \
                patch.object(fields, "platform_fields", lambda ds: None), \
                patch.object(fields, "FULL_FIELD_CAP", 8):
            out = fields.select_fields(con, "demo", field_min_cov=0.5,
                                       keep_fields=["no_such_field"]) 
        self.assertTrue(out)
        self.assertNotIn("no_such_field", {r["field_name"] for r in out})


class TestNegMirror(unittest.TestCase):
    """P0-2 负向强信号镜像（2026-10-26）。

    镜像的数学前提是「整式取反 ⇒ 指标精确取负、换手与集中度不变」，所以三条纪律
    必须在代码里可验：① 只镜像奇对称族；② 换手不跟着变 ⇒ TO>0.40 的源镜像后照旧死；
    ③ 镜像行**不进** `all_alphas`（否则 `max_s`/joint/设置轴扫描会被「−4.35 镜出的 +4.35」污染）。
    """

    @staticmethod
    def _a(aid, s, tpl="lvl_rk", f=1.1, y2=2.0, sub=1.1, rob=1.1, neg=False):
        return {"alpha": aid, "tpl": tpl, "s": s, "f": f, "y2": y2,
                "sub": sub, "rob": rob, "neg": neg}

    def test_neg_stats_excludes_mirror_rows(self):
        from wqb_campaign import mirror
        st = mirror.neg_stats([self._a("A", 0.4), self._a("B", -2.2),
                               self._a("C", -1.7), self._a("M", 9.9, neg=True)])
        self.assertEqual(st["min_s"], -2.2)
        self.assertEqual(st["max_abs_s"], -2.2)
        self.assertEqual(st["max_neg_s"], -1.7, "负向簇上沿取最大（最接近 0）的负值")
        self.assertEqual(st["n_strong"], 2, "镜像行不得计入 n_strong")

    def test_neg_stats_empty_and_all_positive(self):
        from wqb_campaign import mirror
        self.assertEqual(mirror.neg_stats([])["n_strong"], 0)
        st = mirror.neg_stats([self._a("A", 0.9)])
        self.assertIsNone(st["max_neg_s"])
        self.assertEqual(st["min_s"], 0.9)
        self.assertEqual(st["n_strong"], 0)

    def test_pick_sources_whitelist_order_and_gate(self):
        from wqb_campaign import mirror
        alphas = [
            self._a("NEG_OK_A", -1.70),
            self._a("NEG_OK_B", -2.40, tpl="rg_grdev_p3_sec"),
            self._a("SUFFIX_CX", -1.80, tpl="d1_rk_cx"),   # 派发后缀应被 norm_tpl 剥掉
            self._a("WEAK", -1.57),                        # 差 0.01 不进
            self._a("DW", -2.0, tpl="dw"),                 # 两 rank 乘积（偶）
            self._a("PP", -2.0, tpl="pp"),                 # 门控：取反后选另一批股票
            self._a("TL", -2.0, tpl="tl"),
            self._a("DSP", -2.0, tpl="dsp_rk"),            # vec_stddev 非负
            self._a("LVV", -2.0, tpl="rg_lvvol_sec"),      # 含 ts_std_dev（偶）
            self._a("RES", -2.0, tpl="res"),               # 含 PV returns，非 ATOM
            self._a("RESLAG", -2.0, tpl="reslag"),
            self._a("MIRROR_ROW", -3.0, neg=True),
        ]
        got = [a["alpha"] for a in mirror._pick_sources(alphas)]
        self.assertEqual(got, ["NEG_OK_B", "SUFFIX_CX", "NEG_OK_A"],
                         "只留奇对称族、过 −1.58 门槛、按 S 升序（越负越优先）")

    def test_dispatch_settings_replicates_full_source_settings(self):
        from wqb_campaign import mirror
        st = mirror._dispatch_settings({
            "settings": {"universe": "TOP500", "neutralization": "SUBINDUSTRY",
                         "truncation": "0.08", "nan_handling": "OFF"},
            "decay": 6})
        self.assertEqual(st["neutralization"], "SUBINDUSTRY", "只覆写 decay 会让镜像变成另一个实验")
        self.assertEqual(st["decay"], "6")
        self.assertEqual(mirror._dispatch_settings({"settings": {}, "decay": 2}), {"decay": "2"})

    def test_joint_thresholds(self):
        from wqb_campaign import mirror
        ok = {"s": 1.58, "f": 1.0, "y2": 1.0, "sub": 1.0, "rob": 1.0}
        self.assertTrue(mirror._joint(ok, 1.0, 1.0, 1.0))
        self.assertFalse(mirror._joint(dict(ok, s=1.57), 1.0, 1.0, 1.0))
        self.assertFalse(mirror._joint(dict(ok, rob=0.99), 1.0, 1.0, 1.0))
        self.assertFalse(mirror._joint(dict(ok, rob=None), 1.0, 1.0, 1.0),
                         "rob 取不到（None）不能当通过")
        self.assertTrue(mirror._joint({"s": 1.7, "f": 1.2, "y2": 2.0}, 1.58),
                        "EUR（gsub/grob=None）保持旧口径")

    def test_is_mirror_tpl_structural_exclusions(self):
        for tpl in ("dw", "pp", "tl", "dsp_rk", "rg_lvvol_sec", "res", "reslag", None):
            self.assertFalse(generate.is_mirror_tpl(tpl), f"{tpl} 不是奇对称结构，不能镜像")
        for tpl in ("lvl_rk", "d1_rk_cx", "rg_grdev_p3_sec_f", "ed_rk", "ir_pl"):
            self.assertTrue(generate.is_mirror_tpl(tpl))

    def test_fetch_alpha_meta_parses_contract(self):
        from wqb_campaign import transport

        class R:
            returncode = 0
            stdout = (
                '+ ABC123 atom=1 decay=6 tvr=0.8702 '
                'settings={"universe":"TOP500","neutralization":"SUBINDUSTRY"} '
                'code=rank(ts_backfill(eps, 252))\n'
                '# ABC123 effective=1 atom=1\n'
                '+ DEF456 atom=0 decay=4 tvr=na settings={} code=rank(x)\n'
            )

        with patch.object(transport, "_meta_script", lambda: __file__), \
                patch.object(transport.subprocess, "run", lambda *a, **k: R()):
            got = transport.fetch_alpha_meta(["ABC123", "DEF456", " "])
        self.assertEqual(set(got), {"ABC123", "DEF456"})
        self.assertEqual(got["ABC123"]["atom"], 1)
        self.assertEqual(got["ABC123"]["decay"], 6)
        self.assertAlmostEqual(got["ABC123"]["tvr"], 0.8702)
        self.assertEqual(got["ABC123"]["settings"]["neutralization"], "SUBINDUSTRY")
        self.assertEqual(got["ABC123"]["code"], "rank(ts_backfill(eps, 252))")
        self.assertIsNone(got["DEF456"]["tvr"])
        self.assertEqual(transport.fetch_alpha_meta([]), {}, "空输入不得起子进程")

    def _run(self, src_tvr, harvest_rows, prod=0.41, meta_atom=1, neg_mirror=True):
        """跑一次 run_neg_mirror（全部子进程/平台调用打桩）→ (neg, all_alphas, dispatched, ck)。"""
        from wqb_campaign import mirror
        src = self._a("SRC", -2.5, tpl="rg_grdev_p3_sec",
                      f=-1.2, y2=-2.1, sub=-1.3, rob=-1.1)
        all_alphas = [src]
        dispatched = {}
        ck = {"sims": {}}
        prod_calls = []

        def fake_dispatch(exprs, ds, label, on_batch=None, settings=None):
            dispatched["exprs"] = exprs
            dispatched["settings"] = settings
            if on_batch:
                on_batch([("SIM1", exprs[0][0], 0)])
            return [("SIM1", exprs[0][0], 0)]

        def fake_harvest(sid, ds, tag=""):
            return [harvest_rows], [], "ok"

        def fake_prod(aid):
            prod_calls.append(aid)
            return prod

        saved = mirror.NEG_MIRROR
        try:
            mirror.NEG_MIRROR = neg_mirror
            with patch.object(mirror, "fetch_alpha_meta",
                              lambda ids: {i: {"code": "rank(x)", "atom": meta_atom, "decay": 6,
                                               "tvr": src_tvr,
                                               "settings": {"universe": "TOP500",
                                                            "neutralization": "SUBINDUSTRY"}}
                                           for i in ids}), \
                    patch.object(mirror, "dispatch", fake_dispatch), \
                    patch.object(mirror, "harvest_until_done", fake_harvest), \
                    patch.object(mirror, "fetch_codes",
                                 lambda ids: {i: "multiply(-1, rank(x))" for i in ids}), \
                    patch.object(mirror, "save_ckpt", lambda ck: None), \
                    patch.object(mirror, "note_bad_tokens", lambda e: None), \
                    patch.object(mirror, "check_prod", fake_prod):
                neg = mirror.run_neg_mirror("demo", all_alphas, ck, 1.0, 1.0, 1.0)
        finally:
            mirror.NEG_MIRROR = saved
        return neg, all_alphas, dispatched, ck, prod_calls

    def test_mirror_dispatches_negated_code_and_never_touches_forward_battery(self):
        neg, all_alphas, dispatched, ck, prod_calls = self._run(
            src_tvr=0.22, harvest_rows=("MIR", 1.90, 1.40, 1.60, 1.20, 1.05))
        self.assertEqual(len(all_alphas), 1, "镜像行不得并入 all_alphas")
        self.assertEqual(all_alphas[0]["alpha"], "SRC")
        self.assertEqual(dispatched["exprs"], [("rg_grdev_p3_sec_neg", "multiply(-1, rank(x))")])
        self.assertEqual(dispatched["settings"]["neutralization"], "SUBINDUSTRY")
        self.assertEqual(dispatched["settings"]["decay"], "6")
        self.assertEqual(neg["joint"], 1)
        self.assertEqual(neg["turnover_blocked"], 0)
        self.assertEqual(neg["prod_top"], 0.41)
        self.assertEqual(prod_calls, ["MIR"])
        self.assertEqual(neg["sources"][0]["alpha"], "SRC")
        self.assertIn("demo@ng_d6", ck["sims"], "断点键把镜像批与主派发隔离")

    def test_turnover_identical_so_source_too_high_still_blocked(self):
        neg, _, _, _, prod_calls = self._run(
            src_tvr=0.8702, harvest_rows=("MIR", 1.90, 1.40, 1.60, 1.20, 1.05), prod=0.41)
        self.assertEqual(neg["joint"], 1, "指标确实全过")
        self.assertEqual(neg["turnover_blocked"], 1, "TO 不随取反改变 ⇒ 0.87 照旧超 0.40")
        self.assertIsNone(neg["prod_top"])
        self.assertEqual(prod_calls, [], "被换手拦下的镜像不值得再花 prod 配额")

    def test_non_atom_source_is_skipped(self):
        neg, _, dispatched, _, _ = self._run(
            src_tvr=0.2, harvest_rows=("MIR", 1.9, 1.4, 1.6, 1.2, 1.05), meta_atom=0)
        self.assertEqual(dispatched, {}, "非 ATOM 源不得派发镜像")
        self.assertEqual(neg["mirrors"], [])
        self.assertTrue(any("非 ATOM" in s["why"] for s in neg["skipped"]))

    def test_switch_off_only_reports_stats(self):
        neg, _, dispatched, _, _ = self._run(
            src_tvr=0.2, harvest_rows=("MIR", 1.9, 1.4, 1.6, 1.2, 1.05), neg_mirror=False)
        self.assertEqual(dispatched, {})
        self.assertEqual(neg["n_strong"], 1)
        self.assertEqual(neg["mirrors"], [])


class TestDecideVerdict(unittest.TestCase):
    """P0-2 新增两个 verdict 的优先级（抽成纯函数就为这条用例）。"""

    def test_priority_chain(self):
        from wqb_campaign import pipeline_ind as p
        d = p.decide_verdict
        self.assertEqual(d(False, 2, ["e"], False, False, [], 0.0, 0), "SIM_FAIL")
        self.assertEqual(d(False, 0, ["e"], False, False, [], 0.0, 0), "ERROR")
        self.assertEqual(d(False, 0, [], False, False, [], 0.0, 0), "NO_DATA")
        self.assertEqual(d(True, 0, [], True, True, [], 2.0, 3), "INSUFFICIENT_HISTORY",
                         "十年数据否决优先于 ALIVE")
        self.assertEqual(d(True, 0, [], False, True, ["M"], 2.0, 3), "ALIVE")
        self.assertEqual(d(True, 0, [], False, False, ["M"], 1.2, 3), "ALIVE_NEG")
        self.assertEqual(d(True, 0, [], False, False, [], 1.31, 3), "BORDERLINE")
        self.assertEqual(d(True, 0, [], False, False, [], 1.29, 3), "DEAD_NEG",
                         "正负两向都不可交付但有 |S|≥1.58 的结构 ⇒ 不能判「无信号」")
        self.assertEqual(d(True, 0, [], False, False, [], 1.2, 0), "DEAD")
        self.assertEqual(d(True, 0, [], False, False, [], 0.9, None), "DEAD")


if __name__ == "__main__":
    unittest.main(verbosity=2)
