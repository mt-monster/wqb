#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_all_universes.py
======================
向 WQ BRAIN 平台 `OPTIONS /simulations` 拉取全部区域（InstrumentType=EQUITY）的
合法 universe / delay / neutralization，固化为 JSON + 可粘贴的 Python dict。

用法
----
    python tools/fetch_all_universes.py              # 拉取并覆写固化 JSON
    python tools/fetch_all_universes.py --dry-run    # 只在终端打印，**不写盘**

⚠ 人工一次性运维脚本，**不进 CI**（凭据 + 联网 + 写盘，三件事都在 `main()` 里，
  本模块被 import 时**无任何副作用**——2026-10-06 之前这三件事全在模块级，
  `import fetch_all_universes` 就会真的认证并覆写已入库的 JSON）。

副作用：**覆写**已入库的 `tracking/mining/platform_universes_all_regions.json`
（原子写：先写 `.tmp` 再 `os.replace`，中断不会留下半截 JSON）。
日常查合法档位请用 MCP 工具 `get_platform_setting_options`（凭据在服务端），不要跑本脚本。

⚠ 与 `tracking/README.md` 有契约：输出目录 `tracking/mining/` 的**目录名不可改名/移走**。

退出码：0 = 成功；1 = 凭据缺失 / 认证失败 / 拉取失败。
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# --- 凭据（2026-09-29，skills 审查 AR-10 / X-14 / X-15）---
# 此前缺省 .env 路径指向项目外的作者桌面目录。现在：环境变量 > MCP 服务的 .env（仓库内）；
# 变量名认标准 CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD，旧名 WQ_USERNAME / WQ_PASSWORD 仍认。
# 日常取合法档位请用 MCP 工具 get_platform_setting_options（凭据在服务端）；本脚本只在需要把整张表批量固化成 JSON 时用。

def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path：向上探测双标记，**与文件层数无关**
    （AGENTS.md §8 禁止新增 `parents[N]` / `dirname(dirname())` 这类层数硬编码）。
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()
from wqb.paths import find_repo_root  # noqa: E402
REPO_ROOT = find_repo_root(__file__)
BASE = "https://api.worldquantbrain.com"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="拉取平台合法 universe/delay/neutralization 并固化")
    ap.add_argument("--dry-run", action="store_true",
                    help="只打印，不覆写 tracking/mining/platform_universes_all_regions.json")
    args = ap.parse_args(argv)

    env_path = os.environ.get("WQ_ENV_PATH") or str(REPO_ROOT / "world-quant-brain-mcp" / ".env")
    load_dotenv(env_path)
    username = os.getenv("CREDENTIALS_EMAIL") or os.getenv("WQ_USERNAME", "")
    password = os.getenv("CREDENTIALS_PASSWORD") or os.getenv("WQ_PASSWORD", "")

    if not username or not password:
        print("ERROR: 凭据缺失：请在环境里设 CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD（或用 WQ_ENV_PATH 指向 .env）")
        return 1

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    # --- auth ---
    print("[1/3] Authenticating...", flush=True)
    resp = session.post(f"{BASE}/authentication",
                        auth=(username, password), timeout=30)
    if resp.status_code != 201:
        print(f"AUTH FAILED: {resp.status_code} {resp.text[:200]}")
        return 1
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
        print(f"FAILED: {r.status_code} {r.text[:300]}")
        return 1

    data = r.json()
    print("  OK, parsing...")

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

    # Python dict —— 合法档位的唯一常量出处在 `config.REGIONS`（真值以平台为准），
    # 不要把本段输出粘进任何 `tools/eur_field_coverage.py`（该脚本已不存在）。
    print("\n===== Python dict (对照 src/wqb/config.py 的 REGIONS) =====")
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

    # save JSON（原子写：先 .tmp 再 os.replace，中断不留半截文件）
    out_dir = REPO_ROOT / "tracking" / "mining"
    out_path = out_dir / "platform_universes_all_regions.json"
    result = {
        'fetched_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'instrumentType': 'EQUITY',
        'regions': {r: {'universes': universe_dict[r], 'delays': delay_dict[r], 'neutralizations': neutralization_dict[r]}
                    for r in sorted(universe_dict.keys())},
        'raw_rows': sorted(rows, key=lambda x: x['region']),
    }
    if args.dry_run:
        print(f"\n[DRY-RUN] 未写盘；目标为 {out_path}（{len(universe_dict)} 个区域）")
        return 0
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_name(out_path.name + ".tmp")
    try:
        tmp.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        os.replace(tmp, out_path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    print(f"\n[SAVED] {out_path}")
    print(f"Total regions: {len(universe_dict)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
