#!/usr/bin/env python3
"""Parse a saved MCP get_datafields/get_datasets tool output file and print a
compact field/dataset summary sorted by usage.

Usage:
    python tools/parse_fields.py <path-to-saved-toolcall-output.txt> [datasets]
"""
import json
import re
import sys


def main():
    path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "fields"
    t = open(path, encoding="utf-8").read()
    # Saved MCP output wraps the payload as a JSON array of {type,text},
    # where text itself is an escaped JSON string. Decode twice.
    i = t.find("[{")
    if i < 0:
        i = t.find("{")
    dec = json.JSONDecoder()
    obj, _ = dec.raw_decode(t[i:])
    if isinstance(obj, list):
        obj = obj[0]
    d = obj["text"] if isinstance(obj, dict) and "text" in obj else obj
    if isinstance(d, str):
        d = json.loads(d)
    rows = d["results"]
    if mode == "datasets":
        rows = sorted(rows, key=lambda x: -x.get("alphaCount", 0))
        print(f"total {len(rows)} datasets. Top by alphaCount:")
        for r in rows[:40]:
            pm = r.get("pyramidMultiplier", "?")
            print(f"  {r.get('alphaCount',0):>5}a/{r.get('userCount',0):>4}u "
                  f"cov={r.get('coverage',0):.2f} pm={pm} "
                  f"{r.get('category','?'):12} {r['id']}")
    else:
        rows = sorted(rows, key=lambda x: -x.get("alphaCount", 0))
        print(f"total {len(rows)} fields. Top by alphaCount:")
        for r in rows[:35]:
            print(f"  {r.get('alphaCount',0):>5}a/{r.get('userCount',0):>4}u "
                  f"cov={r.get('coverage',0):.2f} {r.get('type','?'):6} {r['id']}")
            desc = r.get("description", "")
            if desc:
                print(f"        {desc[:120]}")


if __name__ == "__main__":
    main()
