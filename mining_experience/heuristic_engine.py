"""
mining_experience/heuristic_engine.py

Decision engine that loads structured mining heuristics from rules.json and
provides an API for alpha mining pipelines to query region-specific best
practices, template priorities, OS decay risk scores, and expression generation.

Usage:
    from mining_experience.heuristic_engine import HeuristicEngine

    engine = HeuristicEngine()
    recs = engine.get_region_recommendations("USA", "TOP3000")
    score = engine.score_expression("group_rank(ts_rank(fnd6_drlt,60), sector)")
    should_suppress = engine.should_suppress_template("vector_neut")
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Singleton loader
# ---------------------------------------------------------------------------

_RULES_CACHE: Optional[Dict[str, Any]] = None


def load_rules() -> Dict[str, Any]:
    """Load rules.json from the package directory (cached)."""
    global _RULES_CACHE
    if _RULES_CACHE is None:
        _rules_path = Path(__file__).resolve().parent / "rules.json"
        with open(_rules_path, "r", encoding="utf-8") as f:
            _RULES_CACHE = json.load(f)
    return _RULES_CACHE


def reset_rules_cache():
    """Clear the rules cache (useful for testing or hot-reload)."""
    global _RULES_CACHE
    _RULES_CACHE = None


# ---------------------------------------------------------------------------
# HeuristicEngine
# ---------------------------------------------------------------------------

class HeuristicEngine:
    """
    Wraps rules.json into a queryable decision engine for alpha mining.
    """

    def __init__(self, rules_path: Optional[str] = None):
        if rules_path:
            with open(rules_path, "r", encoding="utf-8") as f:
                self._rules = json.load(f)
        else:
            self._rules = load_rules()

    # ------------------------------------------------------------------
    # Region-level recommendations
    # ------------------------------------------------------------------

    def get_region_key(self, region: str, universe: str, delay: int = 1) -> str:
        """Build the region/universe/delay key used in rules.json."""
        return f"{region}/{universe}/D{delay}"

    def get_region_recommendations(
        self, region: str, universe: str, delay: int = 1
    ) -> Dict[str, Any]:
        """
        Return all heuristics for a region/universe/delay combination.

        Returns dict with keys: data_sources, best_params, templates,
        best_params, sign_directions, window_recommendations.
        """
        key = self.get_region_key(region, universe, delay)
        region_data = self._rules.get("regions", {}).get(key, {})
        if not region_data:
            # Try partial match: just region
            for rk, rv in self._rules.get("regions", {}).items():
                if rk.startswith(f"{region}/"):
                    region_data = rv
                    break

        return {
            "key": key,
            "total_alphas": region_data.get("total_alphas", 0),
            "avg_sharpe": region_data.get("avg_sharpe"),
            "data_sources": region_data.get("data_sources", {}),
            "best_params": region_data.get("best_params", self.get_param_defaults(region)),
            "template_patterns": region_data.get("template_patterns", []),
            "weight_ratios": region_data.get("weight_ratios", {}),
        }

    # ------------------------------------------------------------------
    # Data source affinity
    # ------------------------------------------------------------------

    def get_data_source_ranking(
        self, region: str, universe: str
    ) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Return data sources ranked by priority (lowest priority number first).
        Each entry is (source_name, source_info_dict).
        """
        recs = self.get_region_recommendations(region, universe)
        sources = recs.get("data_sources", {})
        ranked = sorted(sources.items(), key=lambda x: x[1].get("priority", 99))
        return ranked

    def is_preferred_source(
        self, dataset_prefix: str, region: str, universe: str
    ) -> bool:
        """Check if a dataset prefix is a preferred source for this region."""
        recs = self.get_region_recommendations(region, universe)
        sources = recs.get("data_sources", {})
        return dataset_prefix in sources

    def get_sign_direction(self, dataset: str) -> str:
        """Get the sign direction for a dataset ('negative' or 'positive')."""
        sign_map = self._rules.get("sign_directions", {})
        for direction, datasets in sign_map.items():
            if dataset in datasets:
                return direction
        return "positive"  # default

    # ------------------------------------------------------------------
    # Template scoring
    # ------------------------------------------------------------------

    def get_template_info(self, template_name: str) -> Dict[str, Any]:
        """Get full info for a named template."""
        return self._rules.get("templates", {}).get(template_name, {})

    def get_template_priority(self, template_name: str) -> int:
        """Get priority score (lower = better). Returns 99 if unknown."""
        info = self.get_template_info(template_name)
        return info.get("priority", 99)

    def get_template_decay_risk(self, template_name: str) -> str:
        """Get OS decay risk: 'low', 'medium', 'high', or 'unknown'."""
        info = self.get_template_info(template_name)
        return info.get("os_decay_risk", "unknown")

    def should_suppress_template(self, template_name: str) -> bool:
        """Check if a template should be suppressed due to high OS decay."""
        info = self.get_template_info(template_name)
        return info.get("suppress", False)

    def get_anti_decay_templates(self) -> List[str]:
        """Return templates known to have low OS decay."""
        return self._rules.get("os_decay_analysis", {}).get("anti_decay_templates", [])

    def get_high_decay_templates(self) -> List[str]:
        """Return templates known to have high OS decay."""
        return self._rules.get("os_decay_analysis", {}).get("high_decay_templates", [])

    def get_preferred_templates(
        self, region: str, universe: str
    ) -> List[str]:
        """
        Return template names ordered by preference for the given region.
        Suppresses high-decay templates unless no alternatives exist.
        """
        region_key = self.get_region_key(region, universe)
        region_data = self._rules.get("regions", {}).get(region_key, {})
        recs = self.get_region_recommendations(region, universe)
        sources = recs.get("data_sources", {})

        # Collect applicable template names from data sources
        applicable = set()
        for src_name, src_info in sources.items():
            pref = src_info.get("preferred_template")
            if pref:
                applicable.add(pref)
            # Also check all templates for dataset applicability
            for tname, tinfo in self._rules.get("templates", {}).items():
                datasets = tinfo.get("applicable_datasets", [])
                regions_app = tinfo.get("applicable_regions", [])
                if src_name in datasets or region in regions_app:
                    applicable.add(tname)

        # Sort by priority, suppress high-decay ones
        ranked = sorted(applicable, key=lambda t: self.get_template_priority(t))
        suppressed = set(self.get_high_decay_templates())
        return [t for t in ranked if t not in suppressed]

    # ------------------------------------------------------------------
    # Expression scoring
    # ------------------------------------------------------------------

    def score_expression(self, code: str, region: str, universe: str) -> Dict[str, Any]:
        """
        Score an expression string based on heuristic rules.

        Returns dict with:
            total_score: float (higher = better)
            template_match: str or None
            os_decay_risk: str
            recommendations: list of str
        """
        if not code or not code.strip():
            return {"total_score": 0, "template_match": None, "os_decay_risk": "unknown", "recommendations": ["empty expression"]}

        score = 50.0  # base score
        recommendations = []
        matched_template = None
        decay_risk = "medium"

        # 1. Detect template pattern
        templates = self._rules.get("templates", {})
        for tname, tinfo in templates.items():
            pattern = tinfo.get("pattern", "")
            # Check if expression matches template pattern (simplified heuristic)
            if self._matches_template_pattern(code, pattern):
                matched_template = tname
                priority = tinfo.get("priority", 99)
                decay = tinfo.get("os_decay_risk", "medium")
                decay_risk = decay
                avg_sh = tinfo.get("avg_sharpe", 1.0)

                # Score by priority
                if priority <= 3:
                    score += 30
                elif priority <= 5:
                    score += 15
                elif priority <= 7:
                    score += 5

                # Score by avg sharpe
                score += (avg_sh - 1.0) * 10

                # Penalty for high decay
                if decay == "high":
                    score -= 40
                    recommendations.append(f"HIGH OS DECAY RISK: template '{tname}'")
                elif decay == "low":
                    score += 10

                break

        # 2. Check for suppress patterns
        suppress_indicators = {
            "vector_neut": "high_decay",
            "ts_std_dev(FIELD": "high_decay",
            "group_mean(ts_std_dev": "high_decay",
        }
        for indicator, risk in suppress_indicators.items():
            if indicator in code:
                score -= 20
                recommendations.append(f"Contains {risk} pattern: '{indicator}'")
                decay_risk = "high"

        # 3. Check for preferred patterns
        preferred_indicators = {
            "group_rank(ts_rank": "stable_rank",
            "ts_sum(FIELD, 252)": "cumulative_sum",
            "group_neutralize": "neutralized",
            "winsorize": "outlier_robust",
        }
        for indicator, label in preferred_indicators.items():
            if indicator in code:
                score += 10
                recommendations.append(f"Contains preferred pattern: '{label}'")

        # 4. Region-specific adjustments
        recs = self.get_region_recommendations(region, universe)
        sources = recs.get("data_sources", {})
        for src_name, src_info in sources.items():
            if src_name in code:
                priority = src_info.get("priority", 99)
                if priority <= 2:
                    score += 10
                    recommendations.append(f"Uses preferred source: {src_name}")

        # 5. Check for anti-decay patterns
        if "vector_neut" not in code and "ts_std_dev" not in code:
            if matched_template is None:
                score += 5  # unknown but not obviously bad

        return {
            "total_score": round(score, 1),
            "template_match": matched_template,
            "os_decay_risk": decay_risk,
            "recommendations": recommendations,
        }

    def _matches_template_pattern(self, code: str, pattern: str) -> bool:
        """Simple heuristic: check if key tokens from pattern appear in code."""
        # Extract key operator names from pattern
        key_tokens = []
        for token in re.findall(r'[\w_]+', pattern):
            if token in ("FIELD", "FIELD_A", "FIELD_B", "N", "group", "n", "w1", "w2", "A", "B"):
                continue
            if len(token) > 3:
                key_tokens.append(token)

        if not key_tokens:
            return False

        # Require at least 60% of key tokens to appear in code
        matches = sum(1 for t in key_tokens if t in code)
        return matches / len(key_tokens) >= 0.6

    # ------------------------------------------------------------------
    # Parameter defaults
    # ------------------------------------------------------------------

    def get_param_defaults(self, region: str) -> Dict[str, Any]:
        """Get recommended simulation parameters for a region."""
        by_region = self._rules.get("parameter_defaults", {}).get("by_region", {})
        common = self._rules.get("parameter_defaults", {}).get("common", {})
        region_params = by_region.get(region, {})
        return {**common, **region_params}

    def get_simulation_settings(
        self, region: str, universe: str, delay: int = 1
    ) -> Dict[str, Any]:
        """Get complete simulation settings dict for a region/universe."""
        defaults = self.get_param_defaults(region)
        by_universe = self._rules.get("parameter_defaults", {}).get("by_universe", {})
        uni_params = by_universe.get(universe, {})

        settings = {
            "instrumentType": "EQUITY",
            "region": region,
            "universe": universe,
            "delay": delay,
            "decay": defaults.get("decay", 5),
            "neutralization": defaults.get("neutralization", "MARKET"),
            "truncation": defaults.get("truncation", 0.08),
            "pasteurization": defaults.get("pasteurization", "ON"),
            "unitHandling": defaults.get("unit_handling", "VERIFY"),
            "nanHandling": defaults.get("nan_handling", "ON"),
            "maxTrade": defaults.get("maxTrade", "OFF"),
            "maxPosition": defaults.get("maxPosition", "OFF"),
            "language": defaults.get("language", "FASTEXPR"),
            "visualization": defaults.get("visualization", False),
            "startDate": defaults.get("start_date", "2014-01-01"),
            "endDate": defaults.get("end_date", "2023-12-31"),
            "selectionHandling": uni_params.get("selectionHandling", "POSITIVE"),
            "selectionLimit": uni_params.get("selectionLimit", 1000),
        }
        return settings

    # ------------------------------------------------------------------
    # Window recommendations
    # ------------------------------------------------------------------

    def get_recommended_windows(self, operator: str) -> List[int]:
        """Get recommended time windows for a given operator."""
        windows = self._rules.get("window_recommendations", {})
        return windows.get(operator, [22, 66, 250])

    # ------------------------------------------------------------------
    # SA recipe
    # ------------------------------------------------------------------

    def get_sa_recipe(self) -> Dict[str, Any]:
        """Return the best-known SA construction recipe."""
        return self._rules.get("sa_recipe", {})

    # ------------------------------------------------------------------
    # Expression generation helpers
    # ------------------------------------------------------------------

    def generate_expressions(
        self,
        region: str,
        universe: str,
        fields: List[str],
        count: int = 100,
        template_names: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate candidate expressions based on heuristics.

        Args:
            region: Region code
            universe: Universe name
            fields: List of raw field names to use
            count: Target number of expressions
            template_names: Optional list of template names to use

        Returns:
            List of dicts with keys: expression, template, score, risk
        """
        if template_names is None:
            template_names = self.get_preferred_templates(region, universe)

        # If no templates found, use all non-suppressed
        if not template_names:
            template_names = [
                t for t, info in self._rules.get("templates", {}).items()
                if not info.get("suppress", False)
            ]

        results = []
        windows = self._rules.get("window_recommendations", {})

        for field in fields:
            for tname in template_names:
                if len(results) >= count:
                    break
                expr = self._apply_template(field, tname, windows)
                if expr:
                    score_info = self.score_expression(expr, region, universe)
                    results.append({
                        "expression": expr,
                        "template": tname,
                        "field": field,
                        "score": score_info["total_score"],
                        "risk": score_info["os_decay_risk"],
                        "recommendations": score_info["recommendations"],
                    })
            if len(results) >= count:
                break

        # Sort by score descending
        results.sort(key=lambda x: -x["score"])
        return results[:count]

    def _apply_template(
        self, field: str, template_name: str, windows: Dict[str, List[int]]
    ) -> Optional[str]:
        """Apply a template pattern to a field name, returning an expression."""

        # group_rank_ts_rank
        if template_name == "group_rank_ts_rank":
            grp = "sector"
            win = windows.get("ts_rank", [60])[0]
            return f"group_rank(ts_rank({field}, {win}), {grp})"

        # ts_sum_layered_neut
        if template_name == "ts_sum_layered_neut":
            return (
                f"a = ts_sum({field}, 252);"
                f"a1 = group_neutralize(a, market);"
                f"a2 = group_neutralize(a1, bucket(rank(cap), range='0.1,1,0.1'));"
            )

        # log_diff_relative_value
        if template_name == "log_diff_relative_value":
            # Requires two fields; skip if only one provided
            return None

        # multi_factor_weighted_rank
        if template_name == "multi_factor_weighted_rank":
            win_bf = windows.get("ts_backfill", [66])[0]
            win_rk = windows.get("ts_rank", [250])[0]
            return (
                f"rank(ts_rank(ts_backfill({field}, {win_bf}), {win_rk}))"
            )

        # ts_rank_ts_backfill_simple
        if template_name == "ts_rank_ts_backfill_simple":
            win_bf = windows.get("ts_backfill", [66])[0]
            win_rk = windows.get("ts_rank", [250])[0]
            return f"rank(ts_rank(ts_backfill({field}, {win_bf}), {win_rk}))"

        # ts_decay_signed_power
        if template_name == "ts_decay_signed_power":
            return (
                f"ts_decay_linear(signed_power("
                f"subtract(group_rank(vec_avg({field}), subindustry), 0.5), 5), 90)"
            )

        # trade_when_volume
        if template_name == "trade_when_volume":
            return (
                f"trade_when(ts_arg_max(volume, 5) == 0, "
                f"group_zscore(group_rank(ts_sum({field}, 30), subindustry), "
                f"densify(bucket(rank(assets), range='0.1,1,0.1'))))"
            )

        # ts_ir_winsorize
        if template_name == "ts_ir_winsorize":
            return (
                f"group_rank(ts_ir(winsorize(ts_backfill(vec_avg({field}), 120), std=4), 20), industry)"
            )

        # ts_delta_dual_window
        if template_name == "ts_delta_dual_window":
            return (
                f"add(multiply(rank(ts_delta(ts_backfill({field}, 66), 66)), 0.5), "
                f"multiply(rank(ts_delta(ts_backfill({field}, 66), 22)), 0.5))"
            )

        # ts_delta_backfill_rank
        if template_name == "ts_delta_backfill_rank":
            win_rk = windows.get("ts_rank", [250])[0]
            return (
                f"rank(ts_rank(ts_delta(ts_backfill(vec_avg({field}), 200), 66), {win_rk}))"
            )

        # simple_price_volume
        if template_name == "simple_price_volume":
            return "-rank(ts_sum((close-low)/(high-close), 3))"

        # group_zscore_ts_zscore_subtract
        if template_name == "group_zscore_ts_zscore_subtract":
            return (
                f"scale(rank(group_zscore(ts_zscore(subtract("
                f"ts_mean(ts_backfill({field}, 66), 22), "
                f"ts_mean(ts_backfill({field}, 66), 22)), 189), industry)))"
            )

        # Fallback: try to construct a simple expression
        return f"rank(ts_rank({field}, 60))"


# ---------------------------------------------------------------------------
# Module-level convenience functions
# ---------------------------------------------------------------------------

_engine_cache: Optional[HeuristicEngine] = None


def get_engine(rules_path: Optional[str] = None) -> HeuristicEngine:
    """Get or create the singleton HeuristicEngine instance."""
    global _engine_cache
    if _engine_cache is None or rules_path:
        _engine_cache = HeuristicEngine(rules_path)
    return _engine_cache


# Common shortcuts
def get_region_recommendations(region: str, universe: str) -> Dict[str, Any]:
    return get_engine().get_region_recommendations(region, universe)


def score_expression(code: str, region: str, universe: str) -> Dict[str, Any]:
    return get_engine().score_expression(code, region, universe)


def should_suppress_template(template: str) -> bool:
    return get_engine().should_suppress_template(template)


def get_preferred_templates(region: str, universe: str) -> List[str]:
    return get_engine().get_preferred_templates(region, universe)


def get_sa_recipe() -> Dict[str, Any]:
    return get_engine().get_sa_recipe()


def generate_expressions(
    region: str,
    universe: str,
    fields: List[str],
    count: int = 100,
) -> List[Dict[str, Any]]:
    return get_engine().generate_expressions(region, universe, fields, count=count)