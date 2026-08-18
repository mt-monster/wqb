"""wqb.memory.events — append-only JSONL event log.

Events are stored one file per day (``YYYY-MM-DD.jsonl``) under the events
directory. Records are dicts carrying at least ``event`` and ``timestamp``.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

EVENT_ROBUSTNESS_AUDIT = "robustness.audit"
EVENT_SIMULATION_BATCH = "simulation.batch"
EVENT_ALPHA_QUALIFIED = "alpha.qualified"
EVENT_ALPHA_REJECTED = "alpha.rejected"
EVENT_SCHEDULER_PLAN = "scheduler.plan"

ALL_EVENT_TYPES = [
    EVENT_ROBUSTNESS_AUDIT,
    EVENT_SIMULATION_BATCH,
    EVENT_ALPHA_QUALIFIED,
    EVENT_ALPHA_REJECTED,
    EVENT_SCHEDULER_PLAN,
]

DEFAULT_EVENTS_DIR = os.path.join("data", "events")


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _event_file_path(directory: str, date: Optional[str] = None) -> str:
    return os.path.join(directory, f"{date or _today_str()}.jsonl")


def emit_to_dir(directory: str, event: str, **payload) -> Dict:
    """Append an event record to ``<directory>/<today>.jsonl``."""
    os.makedirs(directory, exist_ok=True)
    record: Dict = {
        "event": event,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    record.update(payload)
    with open(_event_file_path(directory), "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def emit(event: str, **payload) -> Dict:
    """Append an event record to the default events directory."""
    return emit_to_dir(DEFAULT_EVENTS_DIR, event, **payload)


class EventLog:
    """Read-side API over a directory of daily JSONL event files."""

    def __init__(self, directory: str):
        self.directory = directory

    def list_dates(self) -> List[str]:
        if not os.path.isdir(self.directory):
            return []
        dates = [
            name[:-len(".jsonl")]
            for name in os.listdir(self.directory)
            if name.endswith(".jsonl")
        ]
        return sorted(dates)

    def read(self, date: Optional[str] = None) -> List[Dict]:
        """Return all events for a date (defaults to today); bad lines skip."""
        path = _event_file_path(self.directory, date)
        if not os.path.exists(path):
            return []
        events: List[Dict] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return events

    def query(self, event_name: Optional[str] = None) -> List[Dict]:
        """Return all events across all dates, optionally filtered."""
        out: List[Dict] = []
        for date in self.list_dates():
            for ev in self.read(date):
                if event_name is None or ev.get("event") == event_name:
                    out.append(ev)
        return out

    def recent(self, n: int) -> List[Dict]:
        """Return the N most recent events (newest last)."""
        return self.query()[-n:]

    def count(self, event_name: Optional[str] = None) -> int:
        return len(self.query(event_name))
