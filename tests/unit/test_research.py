"""Unit tests for wqb.research modules — evidence, hypothesis_miner, news_field_classifier.

Covers:

- **evidence.py**: Evidence dataclass, get_evidence filter, add_evidence validation.
- **hypothesis_miner.py**: HypothesisVerdict enum, judge() decision logic,
  Hypothesis/ExperimentResult dataclasses, load_catalog with JSON fallback,
  run_hypothesis_round, save_to_ledger.
- **news_field_classifier.py**: FieldFamily enum, classify_field (overrides + keywords),
  classify_dataset_fields, save_taxonomy/load_taxonomy, is_news_dataset.
"""

import json
import os
from pathlib import Path

import pytest

from wqb.research.evidence import (
    EVIDENCE_REGISTRY,
    Evidence,
    add_evidence,
    get_evidence,
)
from wqb.research.hypothesis_miner import (
    ExperimentResult,
    Hypothesis,
    HypothesisVerdict,
    HYPOTHESIS_CLASSES,
    judge,
    load_catalog,
    run_hypothesis_round,
    save_to_ledger,
)
from wqb.research.news_field_classifier import (
    DATASET_OVERRIDES,
    FieldFamily,
    KEYWORD_RULES,
    classify_dataset_fields,
    classify_field,
    is_news_dataset,
    load_taxonomy,
    save_taxonomy,
)


# ===========================================================================
# evidence.py
# ===========================================================================

def test_evidence_registry_nonempty():
    assert len(EVIDENCE_REGISTRY) > 0


def test_evidence_to_dict():
    e = EVIDENCE_REGISTRY[0]
    d = e.to_dict()
    assert isinstance(d, dict)
    assert "source" in d
    assert "category" in d


def test_get_evidence_all():
    result = get_evidence()
    assert len(result) == len(EVIDENCE_REGISTRY)


def test_get_evidence_filter_by_category():
    result = get_evidence(category="structure_diversity")
    assert all(e.category == "structure_diversity" for e in result)


def test_get_evidence_unknown_category_returns_empty():
    result = get_evidence(category="nonexistent")
    assert result == []


def test_add_evidence_valid():
    initial_count = len(EVIDENCE_REGISTRY)
    e = Evidence(
        source="test_source",
        source_type="paper",
        category="observability",
        design_implication="Test implication",
        actionable_rule="Test rule",
        date="2026-01-01",
    )
    add_evidence(e)
    assert len(EVIDENCE_REGISTRY) == initial_count + 1


def test_add_evidence_wrong_type_raises():
    with pytest.raises(TypeError):
        add_evidence({"not": "an Evidence"})


def test_add_evidence_empty_source_raises():
    with pytest.raises(ValueError):
        add_evidence(Evidence(
            source="",
            source_type="paper",
            category="observability",
            design_implication="x",
            actionable_rule="x",
            date="2026-01-01",
        ))


def test_add_evidence_empty_date_raises():
    with pytest.raises(ValueError):
        add_evidence(Evidence(
            source="src",
            source_type="paper",
            category="observability",
            design_implication="x",
            actionable_rule="x",
            date="",
        ))


# ===========================================================================
# hypothesis_miner.py
# ===========================================================================

def test_hypothesis_verdict_values():
    assert HypothesisVerdict.REJECTED.value == "rejected"
    assert HypothesisVerdict.SUPPORTED.value == "supported"


def test_hypothesis_classes_count():
    assert len(HYPOTHESIS_CLASSES) == 12
    assert "over_reaction" in HYPOTHESIS_CLASSES


def test_hypothesis_to_dict():
    h = Hypothesis(
        hypothesis_id="test_01",
        hypothesis_class="over_reaction",
        description="Test hypothesis",
        minimal_expression="rank(close)",
        ablation_no_gate="close",
        control_constant="1",
        variant="rank(ts_delay(close, 1))",
        expected_direction="positive",
    )
    d = h.to_dict()
    assert d["hypothesis_id"] == "test_01"
    assert d["hypothesis_class"] == "over_reaction"


def test_judge_rejected_pseudo_signal():
    """primary_sharpe ~= control_sharpe → REJECTED."""
    result = ExperimentResult(
        hypothesis_id="t1",
        primary_sharpe=0.5,
        ablation_sharpe=0.4,
        control_sharpe=0.45,  # within 0.1 of 0.5
        variant_sharpe=0.48,
    )
    verdict = judge(result)
    assert verdict["status"] == HypothesisVerdict.REJECTED
    assert verdict["diagnostics"]["pseudo_signal"] is True


def test_judge_needs_refinement_low_sharpe():
    """primary_sharpe < 0.3 → NEEDS_REFINEMENT."""
    result = ExperimentResult(
        hypothesis_id="t1",
        primary_sharpe=0.2,
        ablation_sharpe=0.1,
        control_sharpe=0.0,  # far enough from primary
        variant_sharpe=0.15,
    )
    verdict = judge(result)
    assert verdict["status"] == HypothesisVerdict.NEEDS_REFINEMENT


def test_judge_supported_strong_signal():
    """primary_sharpe >> control_sharpe AND fitness > 0.8 → SUPPORTED."""
    result = ExperimentResult(
        hypothesis_id="t1",
        primary_sharpe=1.5,
        ablation_sharpe=1.0,
        control_sharpe=0.0,
        variant_sharpe=1.3,
        primary_fitness=1.0,
        control_fitness=0.0,
    )
    verdict = judge(result)
    assert verdict["status"] == HypothesisVerdict.SUPPORTED


def test_judge_partially_supported():
    """primary_sharpe > control by >0.1 but not enough for SUPPORTED."""
    result = ExperimentResult(
        hypothesis_id="t1",
        primary_sharpe=0.8,
        ablation_sharpe=0.5,
        control_sharpe=0.5,
        variant_sharpe=0.6,
        primary_fitness=0.4,
        control_fitness=0.0,
    )
    verdict = judge(result)
    assert verdict["status"] == HypothesisVerdict.PARTIALLY_SUPPORTED


def test_judge_diagnostics_structure():
    result = ExperimentResult(
        hypothesis_id="t1",
        primary_sharpe=1.0,
        ablation_sharpe=0.8,
        control_sharpe=0.0,
        variant_sharpe=0.9,
    )
    verdict = judge(result)
    diag = verdict["diagnostics"]
    assert "sharpe_delta" in diag
    assert "ablation_delta" in diag
    assert "variant_delta" in diag
    assert "pseudo_signal" in diag


def test_load_catalog_json(tmp_path):
    catalog = {
        "hypotheses": [
            {
                "hypothesis_id": "h1",
                "hypothesis_class": "over_reaction",
                "description": "Over-reaction to news",
                "minimal_expression": "rank(close)",
                "ablation_no_gate": "close",
                "control_constant": "1",
                "variant": "rank(ts_delay(close, 1))",
                "expected_direction": "positive",
            }
        ]
    }
    path = tmp_path / "catalog.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(catalog, f)
    hypotheses = load_catalog(str(path))
    assert len(hypotheses) == 1
    assert hypotheses[0].hypothesis_id == "h1"


def test_load_catalog_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_catalog(str(tmp_path / "nonexistent.yaml"))


def test_load_catalog_missing_required_field_raises(tmp_path):
    catalog = {"hypotheses": [{"hypothesis_id": "h1"}]}
    path = tmp_path / "bad.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(catalog, f)
    with pytest.raises(ValueError):
        load_catalog(str(path))


def test_run_hypothesis_round(tmp_path):
    catalog = {
        "hypotheses": [
            {
                "hypothesis_id": "h1",
                "hypothesis_class": "over_reaction",
                "description": "x",
                "minimal_expression": "rank(close)",
                "ablation_no_gate": "close",
                "control_constant": "1",
                "variant": "rank(volume)",
                "expected_direction": "positive",
            }
        ]
    }
    path = tmp_path / "cat.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(catalog, f)
    experiments = run_hypothesis_round(str(path), max_hypotheses=1)
    assert "h1" in experiments
    assert len(experiments["h1"]["expressions"]) == 4


def test_run_hypothesis_round_invalid_max_raises(tmp_path):
    catalog = {"hypotheses": []}
    path = tmp_path / "cat.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(catalog, f)
    with pytest.raises(ValueError):
        run_hypothesis_round(str(path), max_hypotheses=0)


def test_save_to_ledger(tmp_path):
    verdict = {
        "status": HypothesisVerdict.SUPPORTED,
        "reason": "Strong signal",
        "diagnostics": {"sharpe_delta": 1.0},
    }
    path = save_to_ledger(verdict, "test_session", ledger_dir=str(tmp_path))
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        line = f.read().strip()
    record = json.loads(line)
    assert record["session_id"] == "test_session"
    assert record["status"] == "supported"


# ===========================================================================
# news_field_classifier.py
# ===========================================================================

def test_classify_field_override_news12():
    """Dataset override: news_pct_*min → DIRECTION."""
    assert classify_field("news_pct_5min", dataset_id="news12") == FieldFamily.DIRECTION


def test_classify_field_override_vol_stddev():
    """Dataset override: news_vol_stddev → DISPERSION."""
    assert classify_field("news_vol_stddev", dataset_id="news12") == FieldFamily.DISPERSION


def test_classify_field_keyword_direction():
    """Keyword match: 'tone' → DIRECTION."""
    assert classify_field("news_tone") == FieldFamily.DIRECTION


def test_classify_field_keyword_attention():
    """Keyword match: 'relevance' before 'score' → ATTENTION."""
    assert classify_field("relevance_score") == FieldFamily.ATTENTION


def test_classify_field_keyword_dispersion():
    """Keyword match: 'stddev' → DISPERSION."""
    assert classify_field("vol_stddev") == FieldFamily.DISPERSION


def test_classify_field_keyword_event_type():
    """Keyword match: 'topic' → EVENT_TYPE."""
    assert classify_field("news_topic_code") == FieldFamily.EVENT_TYPE


def test_classify_field_keyword_peer_context():
    """Keyword match: 'peer' → PEER_CONTEXT."""
    assert classify_field("peer_average") == FieldFamily.PEER_CONTEXT


def test_classify_field_default_direction():
    """No keyword match → DIRECTION default."""
    assert classify_field("abc_xyz") == FieldFamily.DIRECTION


def test_classify_field_description_fallback():
    """Field id has no keyword; description matches."""
    result = classify_field("abc", description="This measures tone polarity")
    assert result == FieldFamily.DIRECTION


def test_classify_dataset_fields():
    fields = [
        {"id": "news_ton_last", "description": "tone last value"},
        {"id": "news_vol_stddev", "description": "volume std dev"},
        {"id": "news_buzz", "description": "buzz level"},
    ]
    taxonomy = classify_dataset_fields(fields, "news12")
    assert taxonomy["news_ton_last"] == FieldFamily.DIRECTION
    assert taxonomy["news_vol_stddev"] == FieldFamily.DISPERSION
    assert taxonomy["news_buzz"] == FieldFamily.ATTENTION


def test_save_and_load_taxonomy(tmp_path):
    taxonomy = {
        "news_ton_last": FieldFamily.DIRECTION,
        "news_vol_stddev": FieldFamily.DISPERSION,
    }
    path = save_taxonomy("news12", "USA", taxonomy, cache_dir=str(tmp_path))
    assert os.path.exists(path)
    loaded = load_taxonomy("news12", "USA", cache_dir=str(tmp_path))
    assert loaded is not None
    assert loaded["families"]["news_ton_last"] == "direction"


def test_load_taxonomy_nonexistent_returns_none(tmp_path):
    assert load_taxonomy("news99", "USA", cache_dir=str(tmp_path)) is None


def test_is_news_dataset_classifier():
    assert is_news_dataset("news12") is True
    assert is_news_dataset("fundamental44", category="fundamental") is False
    assert is_news_dataset("sentiment22") is True


def test_field_family_enum_values():
    assert FieldFamily.DIRECTION.value == "direction"
    assert FieldFamily.ATTENTION.value == "attention"
    assert FieldFamily.DISPERSION.value == "dispersion"
    assert FieldFamily.EVENT_TYPE.value == "event_type"
    assert FieldFamily.PEER_CONTEXT.value == "peer_context"


def test_keyword_rules_nonempty():
    for family, keywords in KEYWORD_RULES.items():
        assert len(keywords) > 0
        assert isinstance(keywords, list)


def test_dataset_overrides_news12_has_entries():
    assert len(DATASET_OVERRIDES["news12"]) > 0