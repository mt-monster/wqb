"""wqb.store — campaign artifact persistence (data/wqb.db).

Single source of truth for expressions, field catalogs, gate reports,
backtest rows, diversity potential, checkpoints, and methodology rules.
JSON/CSV files are not the campaign write path.
"""

from wqb.store.campaign import CampaignStore, default_db_path, get_database_integration
from wqb.store._corr_cache import (
    CORR_FRESH_HOURS,
    CORR_SOURCES,
    NON_REALTIME_SOURCES,
    corr_age_hours,
    normalize_corr_source,
)

__all__ = [
    "CampaignStore",
    "default_db_path",
    "get_database_integration",
    "CORR_FRESH_HOURS",
    "CORR_SOURCES",
    "NON_REALTIME_SOURCES",
    "corr_age_hours",
    "normalize_corr_source",
]
