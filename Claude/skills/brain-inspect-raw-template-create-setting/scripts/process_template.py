from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
PYTHON_EXE = sys.executable

def run_step(script_name: str, args: list[str]) -> None:
    """Run a script from the scripts directory with the given arguments."""
    script_path = SCRIPTS_DIR / script_name
    cmd = [PYTHON_EXE, str(script_path)] + args
    print(f"Running: {script_name} {' '.join(args)}")
    try:
        subprocess.run(cmd, check=True, cwd=SKILL_DIR)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(description="Process a single template file and generate artifacts in a dedicated folder.")
    parser.add_argument("--file", required=True, help="Path to the input idea JSON file.")
    parser.add_argument("--force-fetch-options", action="store_true", help="Force fetching new simulation options even if snapshot exists.")
    parser.add_argument("--out-dir", default=None,
                        help="Where to write artifacts (default: <skill>/processed_templates/<file stem>/, gitignored and not synced).")
    args = parser.parse_args()

    input_path = Path(args.file).resolve()
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    # 1. Create output directory
    output_dir = Path(args.out_dir).resolve() if args.out_dir else SKILL_DIR / "processed_templates" / input_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")

    # 2. Parse idea file
    idea_context_path = output_dir / "idea_context.json"
    run_step("parse_idea_file.py", ["--input", str(input_path), "--out", str(idea_context_path)])

    # 3. Handle Simulation Options
    # Strategy: Use shared snapshot in skill root if available to save time/network, unless forced.
    global_options_path = SKILL_DIR / "sim_options_snapshot.json"
    
    if args.force_fetch_options or not global_options_path.exists():
        print("Fetching simulation options (network required)...")
        run_step("fetch_sim_options.py", ["--out", str(global_options_path)])
    
    # Optional: Copy snapshot to output dir for full reproducibility? 
    # Let's verify if the user wants strictly isolated execution. 
    # For now, we pass the global path to resolve_settings.
    
    # 4. Resolve Candidates (Not final choice)
    candidates_path = output_dir / "settings_candidates.json"
    run_step("resolve_settings.py", [
        "--idea", str(idea_context_path),
        "--options", str(global_options_path),
        "--out", str(candidates_path)
    ])

    print("\n-------------------------------------------------------------")
    print("STEP 1 COMPLETE: Candidates Generated")
    print(f"Candidates file: {candidates_path}")
    print("-------------------------------------------------------------")
    print("NEXT STEPS:")
    print("1. 'idea_context.json' 说明 idea 的意图；'settings_candidates.json' 只用来**核对**该 region/delay 的合法选项，不是让你在这里做设置决策。")
    print("2. 设置取战役 tracking/<REGION>/config/settings.json（或 profile settings_proven）；A/B 实验走 pipeline 的 --neutralization / --set。")
    print("3. 把外部 idea 的表达式写入 expressions 表（S3 pipeline --from-db 读它）：")
    print(f"   $WQ_PY scripts/build_alpha_list.py --idea {idea_context_path} --campaign-dir tracking/<REGION> --settings_json '{{\"region\":\"<R>\",\"delay\":<D>,\"universe\":\"<U>\",\"neutralization\":\"<N>\"}}'")
    print("   （没给的可选字段取战役 settings.json；每个字段的来源会打印。--out 只用于兼容地导出 alpha_list.json，不是交接文件。）")
    print("-------------------------------------------------------------")

    # Stop here: the agent reviews the candidates, then writes expressions with build_alpha_list.py.
    sys.exit(0)

if __name__ == "__main__":
    main()
