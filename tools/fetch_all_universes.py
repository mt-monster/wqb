#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
"""
fetch_all_universes.py
======================
向 WQ BRAIN 平台 OPTIONS /simulations 拉取全部区域(InstrumentType=EQUITY)
的合法 universe / delay / neutralization，固化为 JSON + Python dict。
"""
import json, os, sys, time
from pathlib import Path
from dotenv import load_dotenv
import requests

# --- load .env ---
ENV_PATH = os.environ.get("WQ_ENV_PATH", os.path.join(os.path.expanduser("~"), "Desktop", "E3", "quant", "worldquant_alpha", ".env"))
load_dotenv(ENV_PATH)
USERNAME = os.getenv("WQ_USERNAME", "")
PASSWORD = os.getenv("WQ_PASSWORD", "")
BASE = "https://api.worldquantbrain.com"

if not USERNAME or not PASSWORD:
    print("ERROR: WQ_USERNAME/WQ_PASSWORD not found in .env"); sys.exit(1)

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

# --- auth ---
print("[1/3] Authenticating...", flush=True)
resp = session.post(f"{BASE}/authentication",
                     auth=(USERNAME, PASSWORD), timeout=30)
if resp.status_code != 201:
    print(f"AUTH FAILED: {resp.status_code} {resp.text[:200]}"); sys.exit(1)
print("  OK")

# --- OPTIONS /simulations ---
print("[2/3] Fetching OPTIONS /simulations...", flush=True)
for attempt in range(3):
    r = session.options(f"{BASE}/simulations", timeout=45)
    if r.status_code == 200:
        break
    print(f"  attempt {attempt+1}: {r.status_code}, retrying...")
    time.sleep(3 * (attempt + 1))
else:
    print(f"FAILED: {r.status_code} {r.text[:300]}"); sys.exit(1)

data = r.json()
print(f"  OK, parsing...")

# --- parse ---
settings = data['actions']['POST']['settings']['children']
instrument_types = []
region_map = {}
universe_map = {}
delay_map = {}
neutralization_map = {}

for key, setting in settings.items():
    if setting.get('type') != 'choice':
        continue
    label = setting.get('label', '')
    if label == 'Instrument type':
        instrument_types = setting['choices']
    elif label == 'Region':
        region_map = setting['choices']['instrumentType']
    elif label == 'Universe':
        universe_map = setting['choices']['instrumentType']
    elif label == 'Delay':
        delay_map = setting['choices']['instrumentType']
    elif label == 'Neutralization':
        neutralization_map = setting['choices']['instrumentType']

# Build comprehensive table (focus on EQUITY)
rows = []
universe_dict = {}
delay_dict = {}
neutralization_dict = {}

for it in instrument_types:
    it_val = it['value']
    if it_val != 'EQUITY':
        continue  # focus on EQUITY (stock alphas)
    regions = region_map.get(it_val, [])
    for region in regions:
        r_val = region['value']
        # universes
        unis = [u['value'] for u in universe_map.get(it_val, {}).get('region', {}).get(r_val, [])]
        delays = [d['value'] for d in delay_map.get(it_val, {}).get('region', {}).get(r_val, [])]
        neuts = [n['value'] for n in neutralization_map.get(it_val, {}).get('region', {}).get(r_val, [])]
        row = {
            'instrumentType': it_val,
            'region': r_val,
            'delays': delays,
            'universes': unis,
            'neutralizations': neuts,
        }
        rows.append(row)
        universe_dict[r_val] = unis
        delay_dict[r_val] = delays
        neutralization_dict[r_val] = neuts

# --- output ---
print("\n[3/3] RESULTS (InstrumentType=EQUITY):")
print(f"{'Region':<8} {'Delays':<12} {'Universes':<60} Neutralizations")
print("-" * 120)
for row in sorted(rows, key=lambda x: x['region']):
    print(f"{row['region']:<8} {str(row['delays']):<12} {str(row['universes']):<60} {row['neutralizations']}")

# Python dict for VALID_UNIVERSES
print("\n===== Python dict (paste into eur_field_coverage.py) =====")
print("VALID_UNIVERSES = {")
for r in sorted(universe_dict.keys()):
    unis = universe_dict[r]
    print(f'    "{r}": {unis},')
print("}")

print("\n===== DELAYS =====")
print("VALID_DELAYS = {")
for r in sorted(delay_dict.keys()):
    print(f'    "{r}": {delay_dict[r]},')
print("}")

print("\n===== NEUTRALIZATIONS =====")
print("VALID_NEUTRALIZATIONS = {")
for r in sorted(neutralization_dict.keys()):
    print(f'    "{r}": {neutralization_dict[r]},')
print("}")

# save JSON
out_dir = Path(r"D:\coding\traeCN_project\wqb\tracking\mining")
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "platform_universes_all_regions.json"
result = {
    'fetched_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
    'instrumentType': 'EQUITY',
    'regions': {r: {'universes': universe_dict[r], 'delays': delay_dict[r], 'neutralizations': neutralization_dict[r]}
                for r in sorted(universe_dict.keys())},
    'raw_rows': sorted(rows, key=lambda x: x['region']),
}
out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"\n[SAVED] {out_path}")
print(f"Total regions: {len(universe_dict)}")
