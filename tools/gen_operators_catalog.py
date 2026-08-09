#!/usr/bin/env python3
"""Generate src/wqb/operators/ modules from data/operators_verified.json.

This gives the previously-empty ``src/wqb/operators/`` package a concrete
carrier for the verified/ghost operator lists (resolves project-structure
issue A). Run after updating the JSON:

    python tools/gen_operators_catalog.py
"""
import datetime
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "operators_verified.json")
DST = os.path.join(ROOT, "src", "wqb", "operators")


def py_list(name, items):
    lines = [f"{name} = ["]
    for i, it in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        lines.append(f'    "{it}"{comma}')
    lines.append("]")
    return "\n".join(lines)


def main():
    with open(SRC, encoding="utf-8") as f:
        data = json.load(f)
    verified = data.get("verified", [])
    ghost = data.get("ghost", [])
    known = data.get("known_ghosts", [])
    summary = data.get("summary", {})
    os.makedirs(DST, exist_ok=True)

    header = (
        "# AUTO-GENERATED from data/operators_verified.json — do not edit by hand.\n"
        f"# Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n"
        f"# Source summary: {summary}\n\n"
    )

    with open(os.path.join(DST, "verified.py"), "w", encoding="utf-8") as f:
        f.write(header)
        f.write('"""Operators verified live on the WQ BRAIN platform (safe to use directly)."""\n\n')
        f.write(py_list("VERIFIED_OPERATORS", verified) + "\n")

    with open(os.path.join(DST, "ghost.py"), "w", encoding="utf-8") as f:
        f.write(header)
        f.write(
            '"""Ghost operators: names the expression parser accepts but that are NOT real '
            'WQ functions; substitute with verified equivalents."""\n\n'
        )
        f.write(py_list("GHOST_OPERATORS", ghost) + "\n")

    with open(os.path.join(DST, "known_ghosts.py"), "w", encoding="utf-8") as f:
        f.write(header)
        f.write('"""Subset of GHOST_OPERATORS known to be mis-used / frequently mistaken for real ops."""\n\n')
        f.write(py_list("KNOWN_GHOSTS", known) + "\n")

    with open(os.path.join(DST, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(header)
        f.write('"""Verified / ghost operator catalog (generated from data/operators_verified.json)."""\n\n')
        f.write("from .verified import VERIFIED_OPERATORS\n")
        f.write("from .ghost import GHOST_OPERATORS\n")
        f.write("from .known_ghosts import KNOWN_GHOSTS\n\n")
        f.write("__all__ = ['VERIFIED_OPERATORS', 'GHOST_OPERATORS', 'KNOWN_GHOSTS']\n")

    print(
        f"Generated operators catalog -> {DST}\n"
        f"  verified={len(verified)} ghost={len(ghost)} known_ghosts={len(known)}"
    )


if __name__ == "__main__":
    main()
