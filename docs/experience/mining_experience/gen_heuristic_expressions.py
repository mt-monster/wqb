#!/usr/bin/env python3
"""
mining_experience/gen_heuristic_expressions.py

Standalone script that generates candidate alpha expressions driven by
mining experience heuristics (rules.json). Can be used as:
  1. A standalone tool to generate expressions for simulation
  2. Imported as a module by pipeline scripts

Usage:
    python gen_heuristic_expressions.py --region USA --universe TOP3000 --datasets mdl177 --count 100
    python gen_heuristic_expressions.py --region IND --universe TOP500 --datasets mdl177 --count 200
    python gen_heuristic_expressions.py --region MEA --universe TOP400 --datasets mdl31 --count 50
    python gen_heuristic_expressions.py --score "group_rank(ts_rank(fnd6_drlt,60),sector)" --region USA --universe TOP3000
    python gen_heuristic_expressions.py --sa-recipe
"""

import argparse
import json
import sys
from pathlib import Path

# Ensure the project root is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mining_experience.heuristic_engine import (
    HeuristicEngine,
    get_engine,
    get_preferred_templates,
    get_region_recommendations,
    get_sa_recipe,
    score_expression,
    generate_expressions,
)


def cmd_generate(args):
    """Generate candidate expressions."""
    engine = get_engine()

    # Get region recommendations
    recs = get_region_recommendations(args.region, args.universe)
    print(f"=== Region: {args.region}/{args.universe}/D{args.delay} ===")
    print(f"Total submitted alphas: {recs.get('total_alphas', '?')}")
    print(f"Avg Sharpe: {recs.get('avg_sharpe', '?')}")
    print(f"Recommended params: {json.dumps(recs.get('best_params', {}), indent=2)}")
    print()

    # Preferred templates
    templates = get_preferred_templates(args.region, args.universe)
    print(f"Preferred templates (ordered): {templates}")
    print()

    # Data source ranking
    print("Data source ranking:")
    sources = engine.get_data_source_ranking(args.region, args.universe)
    for src_name, src_info in sources[:10]:
        best_fields = src_info.get("best_fields", [])
        sign = engine.get_sign_direction(src_name)
        print(f"  [{src_info.get('priority', 99)}] {src_name}: "
              f"sh={src_info.get('avg_sh', '?')} "
              f"decay={src_info.get('os_decay_risk', '?')} "
              f"sign={sign}")
        if best_fields:
            print(f"       fields: {best_fields[:5]}")
    print()

    # Build field list
    fields = []
    for ds_prefix in args.datasets:
        src_info = recs.get("data_sources", {}).get(ds_prefix, {})
        if src_info.get("best_fields"):
            for f in src_info["best_fields"]:
                fields.append(f"{ds_prefix}_{f}" if not f.startswith(ds_prefix) else f)
        else:
            # Use the prefix as a placeholder
            fields.append(f"{ds_prefix}_FIELD")

    # Generate expressions
    exprs = generate_expressions(
        region=args.region,
        universe=args.universe,
        fields=fields,
        count=args.count,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(exprs, f, indent=2)
        print(f"Wrote {len(exprs)} expressions to {args.output}")
    else:
        print(f"Generated {len(exprs)} expressions:")
        print(f"{'#':>3} {'Score':>6} {'Risk':>6} {'Template':<35} Expression")
        print("-" * 120)
        for i, e in enumerate(exprs[:args.count]):
            print(f"{i+1:>3} {e['score']:>6.1f} {e['risk']:>6} {e['template']:<35} {e['expression'][:70]}")
            if e.get("recommendations"):
                for rec in e["recommendations"]:
                    print(f"     → {rec}")

    return exprs


def cmd_score(args):
    """Score a single expression."""
    result = score_expression(args.expression, args.region, args.universe)
    print(f"Expression: {args.expression}")
    print(f"Region: {args.region}/{args.universe}")
    print()
    print(f"Score: {result['total_score']}")
    print(f"Template match: {result['template_match']}")
    print(f"OS decay risk: {result['os_decay_risk']}")
    print(f"Recommendations:")
    for rec in result["recommendations"]:
        print(f"  • {rec}")
    return result


def cmd_sa_recipe(args):
    """Print the best SA recipe."""
    recipe = get_sa_recipe()
    print("=== SA Recipe ===")
    print(json.dumps(recipe, indent=2))


def cmd_templates(args):
    """List all available templates with their stats."""
    engine = get_engine()
    templates = engine._rules.get("templates", {})

    print(f"{'Template':<40} {'Sh':>5} {'Decay':>7} {'Pri':>4} {'Count':>6} {'Suppress':>9}")
    print("-" * 80)
    for name, info in sorted(templates.items(), key=lambda x: x[1].get("priority", 99)):
        suppress = "YES" if info.get("suppress") else ""
        print(f"{name:<40} {info.get('avg_sharpe', '?'):>5} "
              f"{info.get('os_decay_risk', '?'):>7} "
              f"{info.get('priority', 99):>4} "
              f"{info.get('count', '?'):>6} "
              f"{suppress:>9}")

    print()
    print("Anti-decay templates (preferred):")
    for t in engine.get_anti_decay_templates():
        info = templates.get(t, {})
        print(f"  ✓ {t}: sh={info.get('avg_sharpe')} decay={info.get('os_decay_risk')}")
    print()
    print("High-decay templates (suppress):")
    for t in engine.get_high_decay_templates():
        info = templates.get(t, {})
        print(f"  ✗ {t}: sh={info.get('avg_sharpe')} decay={info.get('os_decay_risk')}")


def main():
    parser = argparse.ArgumentParser(
        description="Experience-driven alpha expression generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --region USA --universe TOP3000 --datasets fnd6 --count 20
  %(prog)s --region IND --universe TOP500 --datasets mdl177 --count 100
  %(prog)s --score "group_rank(ts_rank(fnd6_drlt,60),sector)" --region USA --universe TOP3000
  %(prog)s --sa-recipe
  %(prog)s --templates
        """,
    )

    parser.add_argument("--region", default="USA", help="Region code (default: USA)")
    parser.add_argument("--universe", default="TOP3000", help="Universe (default: TOP3000)")
    parser.add_argument("--delay", type=int, default=1, help="Data delay (default: 1)")
    parser.add_argument("--datasets", nargs="+", default=["fnd6"],
                        help="Dataset prefixes to use (default: fnd6)")
    parser.add_argument("--count", type=int, default=50, help="Number of expressions to generate (default: 50)")
    parser.add_argument("--output", "-o", help="Output file path (JSON)")
    parser.add_argument("--expression", help="Expression to score")
    parser.add_argument("--score", help="Expression to score (alias for --expression)")
    parser.add_argument("--sa-recipe", action="store_true", help="Print SA recipe")
    parser.add_argument("--templates", action="store_true", help="List all templates")

    args = parser.parse_args()

    if args.sa_recipe:
        cmd_sa_recipe(args)
    elif args.templates:
        cmd_templates(args)
    elif args.score or args.expression:
        expr = args.score or args.expression
        cmd_score(type('Args', (), {'expression': expr, 'region': args.region, 'universe': args.universe})())
    else:
        cmd_generate(args)


if __name__ == "__main__":
    main()