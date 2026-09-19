"""Mode B Idea Layer Improvement Pipeline - Integrated Workflow.

This pipeline implements the 4-phase Mode B improvement strategy:
- Phase 0: Conditional signals (regime-dependent)
- Phase 1: Residual structures (industry-neutralized)
- Phase 2: Interaction terms (cross-concept)
- Phase 3: Temporal innovations (momentum/acceleration/inflection)

Usage:
    python modeb_improvement_pipeline.py --region IND --dataset model252 --base-field defensiveness_composite_score
"""

import sqlite3
import hashlib
from datetime import datetime, timezone
from typing import List, Tuple, Dict
from dataclasses import dataclass

DB = r'D:\coding\traeCN_project\wqb\data\wqb.db'


@dataclass
class ImprovementExpr:
    expr: str
    tag: str
    phase: int
    concept: str
    expected_improvement: str


class ModeBImprovementPipeline:
    """Systematic Mode B idea layer improvement pipeline."""
    
    def __init__(self, region: str, dataset: str, base_field: str):
        self.region = region
        self.dataset = dataset
        self.base_field = base_field
        self.conn = sqlite3.connect(DB)
        self.conn.row_factory = sqlite3.Row
        
    def generate_all_phases(self) -> Dict[int, List[ImprovementExpr]]:
        """Generate all 4 phases of improvements."""
        return {
            0: self.phase0_conditional(),
            1: self.phase1_residual(),
            2: self.phase2_interaction(),
            3: self.phase3_temporal(),
        }
    
    def phase0_conditional(self) -> List[ImprovementExpr]:
        """Phase 0: Conditional signals (regime-dependent)."""
        f = self.base_field
        return [
            ImprovementExpr(
                f"trade_when(ts_zscore(ts_std_dev(returns, 21), 63) > 1, rank(ts_backfill({f}, 66)), nan)",
                "cond_highvol", 0, "regime", "robust +0.2"
            ),
            ImprovementExpr(
                f"trade_when(ts_zscore(ts_std_dev(returns, 21), 63) > 1, rank({f}), rank(-{f}))",
                "cond_switch", 0, "regime", "robust +0.15"
            ),
            ImprovementExpr(
                f"trade_when(ts_zscore(ts_delta(ts_mean(volume, 21), 5), 63) < -1, rank(ts_backfill({f}, 66)), nan)",
                "cond_volcontract", 0, "regime", "robust +0.1"
            ),
            ImprovementExpr(
                f"trade_when(ts_std_dev(returns, 21) > ts_mean(ts_std_dev(returns, 21), 63), rank(ts_backfill({f}, 66)), nan)",
                "cond_volmean", 0, "regime", "robust +0.1"
            ),
        ]
    
    def phase1_residual(self) -> List[ImprovementExpr]:
        """Phase 1: Residual structures (industry-neutralized)."""
        f = self.base_field
        return [
            ImprovementExpr(
                f"subtract(rank(ts_backfill({f}, 66)), group_neutralize(rank(ts_backfill({f}, 66)), industry))",
                "resid_industry", 1, "residual", "prod -0.1"
            ),
            ImprovementExpr(
                f"subtract(rank({f}), group_neutralize(rank({f}), subindustry))",
                "resid_subind", 1, "residual", "prod -0.08"
            ),
            ImprovementExpr(
                f"ts_zscore(subtract(rank({f}), group_neutralize(rank({f}), industry)), 63)",
                "resid_zscore", 1, "residual", "prod -0.12"
            ),
        ]
    
    def phase2_interaction(self) -> List[ImprovementExpr]:
        """Phase 2: Interaction terms (cross-concept)."""
        f = self.base_field
        return [
            ImprovementExpr(
                f"multiply(rank({f}), rank(ts_delta(ts_mean(volume, 21), 5)))",
                "def_x_liquidity", 2, "interaction", "S +0.3"
            ),
            ImprovementExpr(
                f"multiply(rank(ts_backfill({f}, 66)), rank(ts_zscore(volume, 63)))",
                "def_x_volzscore", 2, "interaction", "S +0.25"
            ),
            ImprovementExpr(
                f"multiply(rank({f}), rank(-ts_std_dev(returns, 21)))",
                "def_x_lowvol", 2, "interaction", "S +0.2"
            ),
            ImprovementExpr(
                f"multiply(rank({f}), rank(ts_arg_max(volume, 21)))",
                "def_x_volpeak", 2, "interaction", "S +0.2"
            ),
        ]
    
    def phase3_temporal(self) -> List[ImprovementExpr]:
        """Phase 3: Temporal innovations (momentum/acceleration/inflection)."""
        f = self.base_field
        return [
            ImprovementExpr(
                f"rank(ts_delta({f}, 21))",
                "temp_momentum", 3, "temporal", "new signal"
            ),
            ImprovementExpr(
                f"rank(ts_delta(ts_delta({f}, 5), 5))",
                "temp_accel", 3, "temporal", "new signal"
            ),
            ImprovementExpr(
                f"rank(ts_arg_max({f}, 63))",
                "temp_inflection", 3, "temporal", "new signal"
            ),
            ImprovementExpr(
                f"rank(ts_zscore({f}, 252))",
                "temp_longz", 3, "temporal", "S +0.15"
            ),
        ]
    
    def insert_wave(self, exprs: List[ImprovementExpr], wave: str) -> int:
        """Insert expressions into a wave."""
        max_wid = self.conn.execute("SELECT COALESCE(MAX(wave_id), 0) FROM expressions").fetchone()[0]
        new_wave_id = max_wid + 1
        max_id = self.conn.execute("SELECT MAX(id) FROM expressions").fetchone()[0]
        now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
        
        for i, e in enumerate(exprs):
            new_id = max_id + 1 + i
            fp = hashlib.sha1(e.expr.encode()).hexdigest()[:16]
            self.conn.execute("""
            INSERT INTO expressions (id, wave_id, expression, fingerprint, status, region, wave, dataset, created_at, updated_at)
            VALUES (?, ?, ?, ?, 'selected', ?, ?, ?, ?, ?)
            """, (new_id, new_wave_id, e.expr, fp, self.region, wave, self.dataset, now, now))
            print(f"  wave{wave} <- {new_id} ({e.tag}): {e.expr[:60]}...")
        
        self.conn.commit()
        return len(exprs)
    
    def run_phase(self, phase: int, wave: str = None) -> int:
        """Run a specific phase."""
        all_phases = self.generate_all_phases()
        exprs = all_phases.get(phase, [])
        if not exprs:
            print(f"Phase {phase} not found")
            return 0
        
        wave = wave or str(160 + phase)
        print(f"\n=== Phase {phase}: {exprs[0].concept} ===")
        return self.insert_wave(exprs, wave)
    
    def run_all(self, start_wave: int = 160) -> Dict[int, int]:
        """Run all phases."""
        results = {}
        all_phases = self.generate_all_phases()
        
        for phase, exprs in all_phases.items():
            wave = str(start_wave + phase)
            print(f"\n=== Phase {phase}: {exprs[0].concept} (wave {wave}) ===")
            results[phase] = self.insert_wave(exprs, wave)
        
        return results
    
    def close(self):
        self.conn.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Mode B Idea Layer Improvement Pipeline")
    parser.add_argument("--region", required=True, help="Region code")
    parser.add_argument("--dataset", required=True, help="Dataset ID")
    parser.add_argument("--base-field", required=True, help="Base field name")
    parser.add_argument("--phase", type=int, help="Run specific phase (0-3)")
    parser.add_argument("--start-wave", type=int, default=160, help="Starting wave number")
    parser.add_argument("--all", action="store_true", help="Run all phases")
    
    args = parser.parse_args()
    
    pipeline = ModeBImprovementPipeline(args.region, args.dataset, args.base_field)
    
    try:
        if args.all:
            results = pipeline.run_all(args.start_wave)
            print(f"\n=== Summary ===")
            for phase, count in results.items():
                print(f"  Phase {phase}: {count} expressions")
        elif args.phase is not None:
            count = pipeline.run_phase(args.phase)
            print(f"\nPhase {args.phase}: {count} expressions")
        else:
            print("Specify --phase N or --all")
    finally:
        pipeline.close()


if __name__ == "__main__":
    main()
