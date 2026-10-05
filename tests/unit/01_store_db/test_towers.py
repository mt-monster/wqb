# -*- coding: utf-8 -*-
"""塔位解析与 towers 列归一的单元测试。

覆盖：
  * wqb.towers.parse_tower / format_tower / category_key / lookup_multiplier
  * wqb.towers.infer_tower（表达式 → 数据字段 → datasets.category → 塔名）
  * wqb.store.submit_queue.normalize_towers（2026-10-05 三态格式回归）
  * wqb.store.submit_queue.priority 的倍率不再被静默丢弃
"""
import json

import pytest


# ---------------------------------------------------------------------------
# wqb.towers
# ---------------------------------------------------------------------------

class TestParseFormatTower:
    def test_roundtrip(self):
        from wqb.towers import format_tower, parse_tower
        assert parse_tower(format_tower("usa", 1, "model")) == ("USA", 1, "MODEL")
        assert parse_tower(format_tower("EUR", 0, "FUNDAMENTAL")) == ("EUR", 0, "FUNDAMENTAL")

    def test_parse_variants(self):
        from wqb.towers import parse_tower
        assert parse_tower("  usa / d1 / model ") == ("USA", 1, "MODEL")
        assert parse_tower("USA/D10/MODEL") == ("USA", 10, "MODEL")

    def test_parse_is_case_insensitive_on_d_and_category(self):
        """回归（2026-10-05）：正则里字面量 `/D` 曾只认大写 D，
        `parse_tower("usa/d1/model")` 返回 None——小写塔名被静默判为非法。
        根因：regex 未加 re.IGNORECASE。修复后任意大小写均合法，输出统一大写。
        """
        from wqb.towers import parse_tower
        assert parse_tower("usa/d1/model") == ("USA", 1, "MODEL")
        assert parse_tower("usa/D1/model") == ("USA", 1, "MODEL")
        assert parse_tower("Usa/D1/Model") == ("USA", 1, "MODEL")
        # 输出必须规范化为大写（不因输入大小写而变化）
        assert parse_tower("usa/d1/model") == parse_tower("USA/D1/MODEL")

    def test_parse_rejects_non_tower_strings(self):
        """裸 category 标签（'OTHER'/'OTHER+ANALYST'）与残缺塔名都不能当塔。"""
        from wqb.towers import parse_tower
        assert parse_tower("OTHER") is None
        assert parse_tower("OTHER+ANALYST") is None
        assert parse_tower("EUR/D1") is None
        assert parse_tower("D1/MODEL") is None
        assert parse_tower("") is None
        assert parse_tower(None) is None
        assert parse_tower("[{'name': 'USA/D1/MODEL'}]") is None


class TestCategoryKey:
    def test_alias_normalization(self):
        from wqb.towers import category_key
        assert category_key("INSIDERS") == "insider"
        assert category_key("INSTITUTIONS") == "institution"
        assert category_key("SocialMedia") == "social_media"
        assert category_key("MODEL") == "model"
        assert category_key("PV") == "pv"

    def test_case_and_whitespace_insensitive(self):
        from wqb.towers import category_key
        assert category_key("  Model ") == "model"
        assert category_key("") == ""


class TestLookupMultiplier:
    def test_string_key_form(self):
        from wqb.towers import lookup_multiplier
        t = {"USA/D1/model": 1.3, "KOR/D1/fundamental": 1.6}
        assert lookup_multiplier(t, "USA", 1, "MODEL") == 1.3
        assert lookup_multiplier(t, "KOR", 1, "FUNDAMENTAL") == 1.6
        assert lookup_multiplier(t, "EUR", 1, "MODEL") is None
        assert lookup_multiplier(t, "USA", 0, "MODEL") is None

    def test_tuple_key_form(self):
        from wqb.towers import lookup_multiplier
        t = {("USA", 1, "model"): 1.3}
        assert lookup_multiplier(t, "USA", 1, "MODEL") == 1.3

    def test_empty_and_empty_table(self):
        from wqb.towers import lookup_multiplier
        assert lookup_multiplier({}, "USA", 1, "MODEL") is None
        assert lookup_multiplier(None, "USA", 1, "MODEL") is None


class TestInferTower:
    """表达式反推塔位——平台对 UNSUBMITTED alpha 返回 pyramids=None，只能靠表达式。

    用真实本地库（data/wqb.db）跑端到端：2026-10-05 实测三颗 READY 候选的期望值。
    """

    @pytest.mark.skipif(
        __import__("pathlib").Path("data/wqb.db").resolve()
        != __import__("pathlib").Path("D:/coding/traeCN_project/wqb/data/wqb.db").resolve(),
        reason="需要真实本地库")
    def test_real_candidates_match_expected(self):
        import sqlite3
        from wqb.towers import infer_tower

        con = sqlite3.connect("data/wqb.db")
        con.row_factory = sqlite3.Row
        try:
            rows = {r["alpha_id"]: dict(r) for r in con.execute(
                "SELECT alpha_id, region, expr FROM submit_ready")}
        finally:
            con.close()

        cases = {
            "N1VnJjXg": "EUR/D1/MODEL",
            "O08EjLVp": "USA/D1/MODEL",
            "LLZ6wZO2": "KOR/D1/FUNDAMENTAL",
        }
        for aid, want in cases.items():
            got = infer_tower(rows[aid]["expr"], rows[aid]["region"])
            assert got is not None, f"{aid} 未能反推塔位"
            assert got["tower"] == want, (aid, got["tower"], want)

    @pytest.mark.skipif(
        __import__("pathlib").Path("data/wqb.db").resolve()
        != __import__("pathlib").Path("D:/coding/traeCN_project/wqb/data/wqb.db").resolve(),
        reason="需要真实本地库")
    def test_grouping_keys_are_not_counted_as_signal(self):
        """industry/market/sector 等分组键不该改变 category 判定。"""
        import sqlite3
        from wqb.towers import infer_tower

        con = sqlite3.connect("data/wqb.db")
        con.row_factory = sqlite3.Row
        try:
            rows = {r["alpha_id"]: dict(r) for r in con.execute(
                "SELECT alpha_id, region, expr FROM submit_ready")}
        finally:
            con.close()
        # O08EjLVp 用了 group_rank(..., industry)；industry 是分组键不应计入字段
        got = infer_tower(rows["O08EjLVp"]["expr"], rows["O08EjLVp"]["region"])
        assert "industry" not in got["fields"]
        assert got["fields"] == ["forecast_yield_metric_2", "forecast_yield_metric_3"]

    def test_infer_tower_rejects_non_expression(self):
        from wqb.towers import infer_tower
        assert infer_tower("", "USA") is None
        assert infer_tower("R83", "USA") is None  # 配方标签形态（无 '('）
        assert infer_tower(None, "USA") is None


# ---------------------------------------------------------------------------
# wqb.store.submit_queue.normalize_towers / priority
# ---------------------------------------------------------------------------

class TestNormalizeTowers:
    """2026-10-05 实测 submit_ready.towers 三种格式并存，旧 priority 只认一种。"""

    def test_none_and_empty(self):
        from wqb.store.submit_queue import normalize_towers
        assert normalize_towers(None) == []
        assert normalize_towers("") == []
        assert normalize_towers("[]") == []
        assert normalize_towers("null") == []

    def test_bare_string(self):
        """裸字符串形态——旧实现 json.loads 抛错后静默退化为 1.0。"""
        from wqb.store.submit_queue import normalize_towers
        assert normalize_towers("USA/D1/MODEL") == [("USA/D1/MODEL", None)]

    def test_json_list_of_str(self):
        from wqb.store.submit_queue import normalize_towers
        assert normalize_towers('["KOR/D1/FUNDAMENTAL"]') == [("KOR/D1/FUNDAMENTAL", None)]

    def test_json_list_of_dict(self):
        from wqb.store.submit_queue import normalize_towers
        raw = json.dumps([{"name": "EUR/D1/MODEL", "multiplier": 1.3}])
        assert normalize_towers(raw) == [("EUR/D1/MODEL", 1.3)]

    def test_dict_without_multiplier(self):
        from wqb.store.submit_queue import normalize_towers
        raw = json.dumps([{"name": "USA/D1/MODEL"}])
        assert normalize_towers(raw) == [("USA/D1/MODEL", None)]

    def test_platform_shape_dict(self):
        """{"region","delay","category":{"id"}} 平台原始形态 → 组装成塔名。"""
        from wqb.store.submit_queue import normalize_towers
        raw = json.dumps([{"region": "USA", "delay": 1, "category": {"id": "MODEL"}}])
        assert normalize_towers(raw) == [("USA/D1/MODEL", None)]

    def test_plain_list_input(self):
        from wqb.store.submit_queue import normalize_towers
        assert normalize_towers(["EUR/D1/MODEL"]) == [("EUR/D1/MODEL", None)]
        assert normalize_towers([{"name": "EUR/D1/MODEL", "multiplier": 1.3}]) \
            == [("EUR/D1/MODEL", 1.3)]

    def test_garbage_mult_falls_back_to_none(self):
        from wqb.store.submit_queue import normalize_towers
        raw = json.dumps([{"name": "USA/D1/MODEL", "multiplier": "1.3"}])
        assert normalize_towers(raw) == [("USA/D1/MODEL", 1.3)]
        raw = json.dumps([{"name": "USA/D1/MODEL", "multiplier": "abc"}])
        assert normalize_towers(raw) == [("USA/D1/MODEL", None)]


class TestPriorityUsesTowerMultiplier:
    """回归：旧 priority 对裸字符串/空数组形态全部退化为 1.0，塔倍率被静默丢弃。"""

    def _row(self, fitness=1.55, prod=0.5626, selfc=0.1301, towers="USA/D1/MODEL"):
        return {"fitness": fitness, "prod": prod, "self": selfc, "towers": towers}

    def test_bare_string_without_multiplier_falls_back_to_one(self):
        """裸字符串拿不到倍率 → 保留旧行为（1.0），不炸。"""
        from wqb.store.submit_queue import priority
        r = self._row(towers="USA/D1/MODEL")
        assert priority(r) == round(1.55 * 1.0 + 0.5 * ((0.7 - 0.5626) + (0.7 - 0.1301)), 4)

    def test_canonical_dict_form_applies_multiplier(self):
        from wqb.store.submit_queue import priority
        r = self._row(towers=json.dumps([{"name": "USA/D1/MODEL", "multiplier": 1.3}]))
        expected = round(1.55 * 1.3 + 0.5 * ((0.7 - 0.5626) + (0.7 - 0.1301)), 4)
        assert priority(r) == expected
        # 倍率生效意味着排序结果确实变了
        bare = self._row(towers="USA/D1/MODEL")
        assert priority(r) > priority(bare)

    def test_missing_metrics_do_not_crash(self):
        from wqb.store.submit_queue import priority
        assert priority({}) == 0.0
        r = self._row(prod=None, selfc=None, towers="[]")
        assert priority(r) == round(1.55, 4)

    def test_missing_keys_do_not_crash(self):
        from wqb.store.submit_queue import priority

        class NoKey(dict):
            def __getitem__(self, k):
                raise KeyError(k)

        assert priority(NoKey()) == 0.0

    def test_max_of_multiple_multipliers(self):
        from wqb.store.submit_queue import priority
        r = self._row(towers=json.dumps(
            [{"name": "USA/D1/MODEL", "multiplier": 1.0},
             {"name": "USA/D1/FUNDAMENTAL", "multiplier": 1.5}]))
        assert priority(r) == round(1.55 * 1.5 + 0.5 * ((0.7 - 0.5626) + (0.7 - 0.1301)), 4)
