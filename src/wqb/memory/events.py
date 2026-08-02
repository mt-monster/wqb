"""Event log: append-only JSONL event store with query helpers.

Implements the event logging infrastructure (orchestrator §11, robustness
Phase D.2).  Events are appended to ``data/events/<today>.jsonl``, one JSON
object per line:

.. code-block:: json

    {"event": "alpha.robustness_audit", "timestamp": "2026-04-22T...", "decision": "REJECT", ...}

Public API
----------
- :func:`emit` — append an event to today's log file.
- :class:`EventLog` — read/query/recent helper.
- Event type constants (``EVENT_ROBUSTNESS_AUDIT``, etc.).
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone, date
from typing import List, Optional


# ---------------------------------------------------------------------------
# Event type constants
# ---------------------------------------------------------------------------

EVENT_ROBUSTNESS_AUDIT: str = "alpha.robustness_audit"
EVENT_SIMULATION_BATCH: str = "alpha.simulation_batch"
EVENT_ALPHA_QUALIFIED: str = "alpha.qualified"
EVENT_ALPHA_REJECTED: str = "alpha.rejected"
EVENT_SCHEDULER_PLAN: str = "scheduler.plan"

ALL_EVENT_TYPES: tuple = (
    EVENT_ROBUSTNESS_AUDIT,
    EVENT_SIMULATION_BATCH,
    EVENT_ALPHA_QUALIFIED,
    EVENT_ALPHA_REJECTED,
    EVENT_SCHEDULER_PLAN,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _today_str() -> str:
    """Return today's date as ``YYYY-MM-DD`` in UTC."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _now_iso() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def _event_file_path(events_dir: str, date_str: str) -> str:
    """Build the JSONL file path for a given date."""
    return os.path.join(events_dir, f"{date_str}.jsonl")


def _ensure_dir(path: str) -> None:
    """Ensure a directory exists."""
    os.makedirs(path, exist_ok=True)


# ---------------------------------------------------------------------------
# emit()
# ---------------------------------------------------------------------------


def emit(event_name: str, **payload) -> dict:
    """Append an event to today's log file.

    The event is written to ``data/events/<today>.jsonl`` as a single JSON
    line.  The directory is created automatically if it does not exist.

    Parameters
    ----------
    event_name : str
        Event type (use one of the ``EVENT_*`` constants).
    **payload
        Additional key-value pairs to include in the event record.

    Returns
    -------
    dict
        The full event record that was written.
    """
    events_dir = "data/events"
    return emit_to_dir(events_dir, event_name, **payload)


def emit_to_dir(events_dir: str, event_name: str, **payload) -> dict:
    """Append an event to a specific events directory.

    Parameters
    ----------
    events_dir : str
        Directory containing per-day JSONL files.
    event_name : str
        Event type.
    **payload
        Additional key-value pairs.

    Returns
    -------
    dict
        The full event record that was written.
    """
    record = {
        "event": event_name,
        "timestamp": _now_iso(),
        **payload,
    }

    _ensure_dir(events_dir)
    filepath = _event_file_path(events_dir, _today_str())
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")

    return record


# ---------------------------------------------------------------------------
# EventLog
# ---------------------------------------------------------------------------


class EventLog:
    """Read and query the append-only event log.

    Parameters
    ----------
    events_dir : str
        Directory containing per-day ``<YYYY-MM-DD>.jsonl`` files.
        Default: ``"data/events"``.

    Examples
    --------
    >>> log = EventLog("data/events")
    >>> events = log.read("2026-04-22")
    >>> audits = log.query(event_name="alpha.robustness_audit")
    >>> recent = log.recent(50)
    """

    def __init__(self, events_dir: str = "data/events"):
        self.events_dir = events_dir

    # ------------------------------------------------------------------
    # Reading
    # ------------------------------------------------------------------

    def read(self, date: Optional[str] = None) -> List[dict]:
        """Read all events for a given date.

        Parameters
        ----------
        date : str or None
            Date string in ``YYYY-MM-DD`` format.  If ``None``, defaults to
            today (UTC).

        Returns
        -------
        list[dict]
            All event records for that date, in chronological order.
            Returns an empty list if the file does not exist.
        """
        date_str = date or _today_str()
        filepath = _event_file_path(self.events_dir, date_str)
        if not os.path.exists(filepath):
            return []

        events: List[dict] = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return events

    def query(
        self,
        event_name: Optional[str] = None,
        date: Optional[str] = None,
    ) -> List[dict]:
        """Query events by event name and/or date.

        Parameters
        ----------
        event_name : str or None
            If provided, filter to events with this ``event`` field.
            If ``None``, return all events for the date.
        date : str or None
            Date string in ``YYYY-MM-DD`` format.  If ``None``, defaults to
            today.

        Returns
        -------
        list[dict]
            Matching event records.
        """
        events = self.read(date)
        if event_name is None:
            return events
        return [e for e in events if e.get("event") == event_name]

    def recent(self, n: int = 100) -> List[dict]:
        """Return the most recent *n* events across all available dates.

        Scans all ``*.jsonl`` files in the events directory, sorted by
        filename (which encodes the date), and returns the last *n* events.

        Parameters
        ----------
        n : int
            Maximum number of events to return.

        Returns
        -------
        list[dict]
            Up to *n* most recent event records, in chronological order
            (oldest first among the returned set).
        """
        if not os.path.exists(self.events_dir):
            return []

        # List all date files sorted by name (= date)
        files = sorted(
            f for f in os.listdir(self.events_dir)
            if f.endswith(".jsonl")
        )

        all_events: List[dict] = []
        for fname in files:
            filepath = os.path.join(self.events_dir, fname)
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        all_events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

        # Return the last n events
        if len(all_events) > n:
            return all_events[-n:]
        return all_events

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def list_dates(self) -> List[str]:
        """Return a sorted list of all dates that have event files."""
        if not os.path.exists(self.events_dir):
            return []
        dates = [
            f.removesuffix(".jsonl")
            for f in os.listdir(self.events_dir)
            if f.endswith(".jsonl")
        ]
        return sorted(dates)

    def count(self, event_name: Optional[str] = None, date: Optional[str] = None) -> int:
        """Count events matching the filter."""
        return len(self.query(event_name=event_name, date=date))
