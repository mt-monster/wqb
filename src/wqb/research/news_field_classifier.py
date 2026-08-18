"""wqb.research.news_field_classifier — 5-family news field taxonomy.

News/sentiment dataset fields are bucketed into families so expression
generation can respect field semantics (direction vs attention vs
dispersion etc.). Classification order: dataset overrides → keyword rules
on the field id → keyword rules on the description → DIRECTION default.
"""

from __future__ import annotations

import fnmatch
import json
import os
from enum import Enum
from typing import Dict, List, Optional


class FieldFamily(Enum):
    DIRECTION = "direction"
    ATTENTION = "attention"
    DISPERSION = "dispersion"
    EVENT_TYPE = "event_type"
    PEER_CONTEXT = "peer_context"


# Per-dataset overrides (fnmatch patterns → family), checked first.
DATASET_OVERRIDES: Dict[str, Dict[str, FieldFamily]] = {
    "news12": {
        "news_pct_*min": FieldFamily.DIRECTION,
        "news_vol_stddev": FieldFamily.DISPERSION,
    },
}

# Keyword rules per family; families are matched in priority order below.
KEYWORD_RULES: Dict[FieldFamily, List[str]] = {
    FieldFamily.PEER_CONTEXT: ["peer", "sector_avg", "industry_avg"],
    FieldFamily.EVENT_TYPE: ["topic", "event", "category_code", "type"],
    FieldFamily.DISPERSION: ["stddev", "std_dev", "variance", "dispersion",
                             "divergence"],
    FieldFamily.ATTENTION: ["relevance", "buzz", "volume_count", "mentions",
                            "attention", "coverage_count", "novelty"],
    FieldFamily.DIRECTION: ["tone", "sentiment", "polarity", "direction",
                            "score", "rating"],
}

# Priority order: more specific families first; DIRECTION is also default.
_FAMILY_PRIORITY = [
    FieldFamily.PEER_CONTEXT,
    FieldFamily.EVENT_TYPE,
    FieldFamily.DISPERSION,
    FieldFamily.ATTENTION,
    FieldFamily.DIRECTION,
]


def is_news_dataset(name: str, category: Optional[str] = None) -> bool:
    """Detect news/sentiment datasets by prefix or category."""
    if category == "news":
        return True
    prefix = name.lower()
    return (prefix.startswith("news") or prefix.startswith("snt")
            or prefix.startswith("sentiment"))


def _match_keywords(text: str) -> Optional[FieldFamily]:
    lowered = text.lower()
    for family in _FAMILY_PRIORITY:
        for kw in KEYWORD_RULES[family]:
            if kw in lowered:
                return family
    return None


def classify_field(field_id: str, description: Optional[str] = None,
                   dataset_id: Optional[str] = None) -> FieldFamily:
    """Classify a single field into a family."""
    if dataset_id and dataset_id in DATASET_OVERRIDES:
        for pattern, family in DATASET_OVERRIDES[dataset_id].items():
            if fnmatch.fnmatch(field_id, pattern):
                return family
    match = _match_keywords(field_id)
    if match is not None:
        return match
    if description:
        match = _match_keywords(description)
        if match is not None:
            return match
    return FieldFamily.DIRECTION


def classify_dataset_fields(fields: List[dict],
                            dataset_id: Optional[str] = None
                            ) -> Dict[str, FieldFamily]:
    """Classify every field of a dataset (list of {id, description})."""
    taxonomy: Dict[str, FieldFamily] = {}
    for field in fields:
        fid = field.get("id", "")
        taxonomy[fid] = classify_field(
            fid, description=field.get("description"), dataset_id=dataset_id)
    return taxonomy


def _taxonomy_path(dataset: str, region: str, cache_dir: str) -> str:
    return os.path.join(cache_dir, f"taxonomy_{dataset}_{region}.json")


def save_taxonomy(dataset: str, region: str,
                  taxonomy: Dict[str, FieldFamily],
                  cache_dir: Optional[str] = None) -> str:
    """Persist a taxonomy as JSON; returns the written path."""
    cache_dir = cache_dir or os.path.join("tracking", "taxonomies")
    os.makedirs(cache_dir, exist_ok=True)
    payload = {
        "dataset": dataset,
        "region": region,
        "families": {fid: family.value for fid, family in taxonomy.items()},
    }
    path = _taxonomy_path(dataset, region, cache_dir)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return path


def load_taxonomy(dataset: str, region: str,
                  cache_dir: Optional[str] = None) -> Optional[dict]:
    """Load a previously saved taxonomy; None when not cached."""
    cache_dir = cache_dir or os.path.join("tracking", "taxonomies")
    path = _taxonomy_path(dataset, region, cache_dir)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
