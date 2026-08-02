"""News / sentiment / socialmedia field classifier.

Divides the fields of ``news``, ``sentiment``, and ``socialmedia`` datasets into
five families so that downstream batch construction can enforce cross-family
diversity (the 6-bucket framework).

The five families are:

* **DIRECTION** -- signed sentiment / tone / price-reaction.
* **ATTENTION** -- relevance, volume, mention count, buzz.
* **DISPERSION** -- stddev, novelty, uncertainty, disagreement.
* **EVENT_TYPE** -- topic codes, significance flags, deal types, intraday /
  front-page indicators.
* **PEER_CONTEXT** -- pre-aggregated peer / group values.

Classification proceeds in two stages:

1. **Dataset-specific overrides** (``DATASET_OVERRIDES``) -- exact-match rules
   that handle known non-obvious field naming conventions (e.g. news12's
   ``news_pct_*min`` is a price-reaction / direction field, not a generic
   percentage).
2. **Keyword rules** (``KEYWORD_RULES``) -- substring matching on both the
   field id and its description.  When multiple keywords from different
   families match, the keyword that appears at the earliest character
   position in the field id wins (with longest-keyword as a tie-breaker).
   This resolves ambiguity for fields like ``"relevance_score"`` which
   contains both an ATTENTION keyword (``"relevance"``) and a DIRECTION
   keyword (``"score"``).

If no keyword matches, the field defaults to **DIRECTION** (the most common
family in practice).

Cached taxonomies are persisted under ``data/field_taxonomy/`` as
``<region>_<dataset>.json`` so that re-classification is only needed when the
dataset's field list changes.
"""

from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Optional

__all__ = [
    "FieldFamily",
    "NEWS_CATEGORIES",
    "NEWS_DATASET_PREFIXES",
    "KEYWORD_RULES",
    "DATASET_OVERRIDES",
    "classify_field",
    "classify_dataset_fields",
    "save_taxonomy",
    "load_taxonomy",
    "is_news_dataset",
]


# ---------------------------------------------------------------------------
# Field families
# ---------------------------------------------------------------------------

class FieldFamily(Enum):
    """The five families that news/sentiment/socialmedia fields are mapped to."""

    DIRECTION = "direction"
    ATTENTION = "attention"
    DISPERSION = "dispersion"
    EVENT_TYPE = "event_type"
    PEER_CONTEXT = "peer_context"

    def __str__(self) -> str:
        return self.value


# ---------------------------------------------------------------------------
# Dataset identification
# ---------------------------------------------------------------------------

#: Platform ``category`` values that trigger the 5-family classifier.
NEWS_CATEGORIES: set[str] = {"news", "sentiment", "socialmedia"}

#: Dataset-id prefixes that trigger the 5-family classifier even when the
#: platform ``category`` field is missing or ambiguous.
NEWS_DATASET_PREFIXES: set[str] = {"news", "nws", "sentiment", "snt"}


# ---------------------------------------------------------------------------
# Keyword rules
# ---------------------------------------------------------------------------

#: Per-family keyword lists.  When a field id or description contains
#: keywords from multiple families, the keyword appearing at the earliest
#: character position wins (longest keyword breaks ties).  See
#: ``_match_keywords`` for the full disambiguation logic.
KEYWORD_RULES: dict[FieldFamily, list[str]] = {
    FieldFamily.DIRECTION: [
        "tone",
        "polarity",
        "sentiment",
        "score",
        "direction",
        "bullish",
        "bearish",
        "positive",
        "negative",
        "signal",
        "return",
        "reaction",
        "pct",
        "ret",
    ],
    FieldFamily.ATTENTION: [
        "relevance",
        "volume",
        "count",
        "mention",
        "buzz",
        "activity",
        "coverage",
        "frequency",
        "intensity",
    ],
    FieldFamily.DISPERSION: [
        "stddev",
        "std_dev",
        "novelty",
        "uncertainty",
        "disagreement",
        "dispersion",
        "variance",
        "spread",
        "range",
    ],
    FieldFamily.EVENT_TYPE: [
        "topic",
        "significance",
        "flag",
        "deal",
        "type",
        "event",
        "trigger",
        "mainz",
        "vol_ratio",
        "atrratio",
        "intraday",
        "front_page",
    ],
    FieldFamily.PEER_CONTEXT: [
        "peer",
        "aggregate",
        "average",
        "mean",
        "group",
        "benchmark",
        "baseline",
    ],
}


# ---------------------------------------------------------------------------
# Dataset-specific overrides
# ---------------------------------------------------------------------------

#: Exact (or prefix) field-id overrides for specific datasets.  These take
#: priority over keyword rules because field naming conventions differ across
#: datasets and can be misleading (e.g. ``news_vol_stddev`` looks like an
#: ATTENTION field by keyword but is actually a DISPERSION field).
#:
#: Each dataset maps to a list of *(field_pattern, family)* tuples.  A
#: ``field_pattern`` ending with ``"*"`` is treated as a prefix match;
#: otherwise it must match the field id exactly (case-insensitive).
DATASET_OVERRIDES: dict[str, list[tuple[str, FieldFamily]]] = {
    "news12": [
        ("news_pct_*min", FieldFamily.DIRECTION),
        ("news_max_up_ret", FieldFamily.DIRECTION),
        ("news_max_dn_ret", FieldFamily.DIRECTION),
        ("news_ton_last", FieldFamily.DIRECTION),
        ("news_vol_stddev", FieldFamily.DISPERSION),
        ("nws12_mainz_vol_ratio", FieldFamily.EVENT_TYPE),
        ("atrratio", FieldFamily.EVENT_TYPE),
        ("news_vol_ratio", FieldFamily.EVENT_TYPE),
        ("news_front_page", FieldFamily.EVENT_TYPE),
    ],
    "news29": [
        ("news_tone", FieldFamily.DIRECTION),
        ("news_sentiment", FieldFamily.DIRECTION),
        ("news_score", FieldFamily.DIRECTION),
        ("news_buzz", FieldFamily.ATTENTION),
        ("news_volume", FieldFamily.ATTENTION),
        ("news_novelty", FieldFamily.DISPERSION),
        ("news_event_type", FieldFamily.EVENT_TYPE),
        ("news_topic", FieldFamily.EVENT_TYPE),
        ("news_peer_avg", FieldFamily.PEER_CONTEXT),
        ("news_group_mean", FieldFamily.PEER_CONTEXT),
    ],
    "news73": [
        ("news_pos_score", FieldFamily.DIRECTION),
        ("news_neg_score", FieldFamily.DIRECTION),
        ("news_polarity", FieldFamily.DIRECTION),
        ("news_mention_count", FieldFamily.ATTENTION),
        ("news_coverage", FieldFamily.ATTENTION),
        ("news_disagreement", FieldFamily.DISPERSION),
        ("news_uncertainty", FieldFamily.DISPERSION),
        ("news_significance", FieldFamily.EVENT_TYPE),
        ("news_intraday", FieldFamily.EVENT_TYPE),
        ("news_peer_benchmark", FieldFamily.PEER_CONTEXT),
    ],
    "news94": [
        ("news_direction", FieldFamily.DIRECTION),
        ("news_tone_score", FieldFamily.DIRECTION),
        ("news_bull_bear", FieldFamily.DIRECTION),
        ("news_activity", FieldFamily.ATTENTION),
        ("news_intensity", FieldFamily.ATTENTION),
        ("news_std_dev", FieldFamily.DISPERSION),
        ("news_spread", FieldFamily.DISPERSION),
        ("news_event_flag", FieldFamily.EVENT_TYPE),
        ("news_deal_type", FieldFamily.EVENT_TYPE),
        ("news_aggregate", FieldFamily.PEER_CONTEXT),
        ("news_baseline", FieldFamily.PEER_CONTEXT),
    ],
}


# ---------------------------------------------------------------------------
# Classification logic
# ---------------------------------------------------------------------------

def _match_override(field_id_lower: str, dataset_id_lower: str) -> Optional[FieldFamily]:
    """Check dataset-specific overrides for an exact or prefix match.

    Parameters
    ----------
    field_id_lower : str
        The field id, already lower-cased.
    dataset_id_lower : str
        The dataset id, already lower-cased.

    Returns
    -------
    FieldFamily or None
        The family if an override matches, otherwise ``None``.
    """
    overrides = DATASET_OVERRIDES.get(dataset_id_lower)
    if overrides is None:
        return None
    for pattern, family in overrides:
        if pattern.endswith("*"):
            prefix = pattern[:-1]
            if field_id_lower.startswith(prefix):
                return family
        elif pattern == field_id_lower:
            return family
    return None


def _match_keywords(field_id_lower: str, description_lower: str) -> FieldFamily:
    """Apply keyword rules to determine the field family.

    Matching strategy (designed to handle ambiguous field names where
    multiple keyword families could match, e.g. ``"relevance_score"``
    contains both ``"relevance"`` (ATTENTION) and ``"score"`` (DIRECTION)):

    1. **Field-id priority** -- keywords found in the field id take
       precedence over keywords found only in the description.
    2. **Earliest position wins** -- among all keyword matches in the field
       id, the family whose keyword appears at the earliest character
       position wins.  This ensures ``"relevance_score"`` maps to
       ATTENTION (``"relevance"`` at position 0) rather than DIRECTION
       (``"score"`` at position 10).
    3. **Longest keyword breaks ties** -- if two keywords start at the same
       position, the longer (more specific) one wins.
    4. If no keyword matches the field id, the same positional logic is
       applied to the description.
    5. Falls back to ``FieldFamily.DIRECTION`` if nothing matches.

    Parameters
    ----------
    field_id_lower : str
        The field id, already lower-cased.
    description_lower : str
        The field description, already lower-cased.

    Returns
    -------
    FieldFamily
        The matched family, or ``FieldFamily.DIRECTION`` as default.
    """
    # Helper: scan a text string for the best keyword match across all
    # families.  Returns (best_family, best_position, best_keyword_len)
    # or (None, -1, 0) if no match.
    def _best_match(text: str) -> tuple[Optional[FieldFamily], int, int]:
        best_family: Optional[FieldFamily] = None
        best_pos: int = -1
        best_kw_len: int = 0
        for family in FieldFamily:
            keywords = KEYWORD_RULES.get(family, [])
            for kw in keywords:
                pos = text.find(kw)
                if pos == -1:
                    continue
                if (
                    best_pos == -1
                    or pos < best_pos
                    or (pos == best_pos and len(kw) > best_kw_len)
                ):
                    best_family = family
                    best_pos = pos
                    best_kw_len = len(kw)
        return best_family, best_pos, best_kw_len

    # 1. Try field id first
    fam, _, _ = _best_match(field_id_lower)
    if fam is not None:
        return fam

    # 2. Fall back to description
    if description_lower:
        fam, _, _ = _best_match(description_lower)
        if fam is not None:
            return fam

    # 3. Default
    return FieldFamily.DIRECTION


def classify_field(
    field_id: str,
    description: str = "",
    dataset_id: str = "",
) -> FieldFamily:
    """Classify a single news/sentiment/socialmedia field into a family.

    Classification order:
      1. ``DATASET_OVERRIDES`` exact/prefix match (if *dataset_id* is given).
      2. ``KEYWORD_RULES`` substring match on field id and description.
      3. Default: ``FieldFamily.DIRECTION``.

    Parameters
    ----------
    field_id : str
        The platform field id (e.g. ``"news_ton_last"``,
        ``"fnd5_revenue_mean"``).
    description : str, optional
        The human-readable field description.  Improves keyword-match accuracy
        when the field id itself is ambiguous.
    dataset_id : str, optional
        The dataset id (e.g. ``"news12"``).  Enables dataset-specific overrides.

    Returns
    -------
    FieldFamily
        One of the five families.

    Examples
    --------
    >>> classify_field("news_ton_last", dataset_id="news12")
    <FieldFamily.DIRECTION: 'direction'>
    >>> classify_field("news_vol_stddev", dataset_id="news12")
    <FieldFamily.DISPERSION: 'dispersion'>
    >>> classify_field("relevance_score")
    <FieldFamily.ATTENTION: 'attention'>
    """
    fid_lower = field_id.lower().strip()
    desc_lower = description.lower().strip()
    ds_lower = dataset_id.lower().strip()

    # 1. Dataset-specific overrides
    if ds_lower:
        override = _match_override(fid_lower, ds_lower)
        if override is not None:
            return override

    # 2. Keyword rules
    return _match_keywords(fid_lower, desc_lower)


def classify_dataset_fields(
    fields: list[dict],
    dataset_id: str,
    region: str = "USA",
) -> dict[str, FieldFamily]:
    """Batch-classify all fields in a dataset.

    Parameters
    ----------
    fields : list[dict]
        List of field dicts as returned by ``get_datafields``.  Each dict
        should contain at least an ``"id"`` key; a ``"description"`` key is
        used if present.
    dataset_id : str
        The dataset id (e.g. ``"news12"``).
    region : str, optional
        Region tag, currently unused by the classifier itself but kept for
        API symmetry with ``save_taxonomy`` / ``load_taxonomy``.

    Returns
    -------
    dict[str, FieldFamily]
        Mapping ``{field_id: FieldFamily}``.

    Examples
    --------
    >>> fields = [
    ...     {"id": "news_ton_last", "description": "tone last value"},
    ...     {"id": "news_vol_stddev", "description": "volume std dev"},
    ... ]
    >>> result = classify_dataset_fields(fields, "news12")
    >>> result["news_ton_last"]
    <FieldFamily.DIRECTION: 'direction'>
    >>> result["news_vol_stddev"]
    <FieldFamily.DISPERSION: 'dispersion'>
    """
    taxonomy: dict[str, FieldFamily] = {}
    for f in fields:
        fid = f.get("id", "")
        if not fid:
            continue
        desc = f.get("description", "")
        taxonomy[fid] = classify_field(fid, description=desc, dataset_id=dataset_id)
    return taxonomy


# ---------------------------------------------------------------------------
# Taxonomy persistence
# ---------------------------------------------------------------------------

def _taxonomy_path(
    dataset_id: str,
    region: str,
    cache_dir: str = "data/field_taxonomy",
) -> Path:
    """Build the canonical cache path for a taxonomy file."""
    safe_region = region.lower().strip()
    safe_dataset = dataset_id.lower().strip()
    return Path(cache_dir) / f"{safe_region}_{safe_dataset}.json"


def save_taxonomy(
    dataset_id: str,
    region: str,
    taxonomy: dict[str, FieldFamily],
    cache_dir: str = "data/field_taxonomy",
) -> str:
    """Persist a field taxonomy to disk as JSON.

    Parameters
    ----------
    dataset_id : str
        The dataset id (e.g. ``"news12"``).
    region : str
        The region tag (e.g. ``"USA"``).
    taxonomy : dict[str, FieldFamily]
        The taxonomy dict as returned by ``classify_dataset_fields``.
    cache_dir : str, optional
        Directory under which to store the JSON file.

    Returns
    -------
    str
        The absolute path to the written file (as a string).
    """
    path = _taxonomy_path(dataset_id, region, cache_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    serialisable = {
        "dataset_id": dataset_id,
        "region": region,
        "families": {fid: fam.value for fid, fam in taxonomy.items()},
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(serialisable, fh, indent=2, ensure_ascii=False)
    return str(path.resolve())


def load_taxonomy(
    dataset_id: str,
    region: str,
    cache_dir: str = "data/field_taxonomy",
) -> Optional[dict]:
    """Load a previously cached taxonomy from disk.

    Parameters
    ----------
    dataset_id : str
        The dataset id.
    region : str
        The region tag.
    cache_dir : str, optional
        Directory where taxonomy JSON files are stored.

    Returns
    -------
    dict or None
        A dict with keys ``"dataset_id"``, ``"region"``, and ``"families"``
        (where each value is a family *string*, not an enum), or ``None`` if
        no cached file exists.
    """
    path = _taxonomy_path(dataset_id, region, cache_dir)
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Dataset identification
# ---------------------------------------------------------------------------

def is_news_dataset(dataset_id: str, category: str = "") -> bool:
    """Determine whether a dataset belongs to the news/sentiment/socialmedia space.

    A dataset qualifies if:
      * Its platform ``category`` is in ``NEWS_CATEGORIES``, **or**
      * Its id starts with one of the ``NEWS_DATASET_PREFIXES``.

    Parameters
    ----------
    dataset_id : str
        The dataset id (e.g. ``"news12"``, ``"snt21"``).
    category : str, optional
        The platform ``category`` field (e.g. ``"news"``, ``"sentiment"``).

    Returns
    -------
    bool
        ``True`` if the dataset is a news/sentiment/socialmedia dataset.

    Examples
    --------
    >>> is_news_dataset("news12")
    True
    >>> is_news_dataset("fundamental44", category="fundamental")
    False
    >>> is_news_dataset("fnd5", category="news")
    True
    """
    if category and category.lower().strip() in NEWS_CATEGORIES:
        return True
    ds_lower = dataset_id.lower().strip()
    for prefix in NEWS_DATASET_PREFIXES:
        if ds_lower.startswith(prefix):
            return True
    return False
