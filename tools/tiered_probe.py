# -*- coding: utf-8 -*-
"""tiered_probe.py - 三层探针编排器（L0 判死 → L1 确认 → L2 升级）。

在 probe_batch_mode.py 的 2+6 模式之上，增加 Layer 2 自动升级：
  - L0（2 条）：快速判死，|S|<0.3 即停，省 6 条配额
  - L1（6 条）：信号确认，无 |S|>=0.5 判死
  - L2（8 条）：ModeA 变体自动生成，基于最强候选推过提交线

组合腿快腿轮换：L1 的组合腿从 fast_pool 轮换，避免全绑同一字段。

用法:
  # 完整三层探针（新数据集首探）
  python tools/tiered_probe.py --campaign-dir tracking/KOR \
      --dataset risk88 --datasets analyst16 --wave 165 \
      --slow-fields rsk88_mfm_ase1_ind_semiconductors,rsk88_mfm_ase1_ri_volatility \
      --fast-pool anl16_afterest_percentage,pv106_lastspreadbp

  # 只做 L0 快速判死
  python tools/tiered_probe.py --campaign-dir tracking/KOR \
      --dataset news38 --wave 166 --l0-only \
      --slow-fields mws38_tone_score --fast-pool pv106_lastspreadbp

  # 跳过 L0 直接 L1（已知有信号的数据集）
  python tools/tiered_probe.py --campaign-dir tracking/KOR \
      --dataset analyst16 --wave 167 --skip-l0 \
      --slow-fields anl16_afterest_percentage --fast-pool pv106_lastspreadbp
"""
import argparse
import json
import os
import sys
from typing import Dict, List, Any, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe_batch_mode import ProbeBatchExecutor, _wqb_store, _find_toolkit, _find_mcp_python


class TieredProbeOrchestrator:
    """三层探针编排器"""

    # Layer 0 阈值
    L0_DEAD = 0.3
    L0_COUNT = 2

    # Layer 1 阈值
    L1_DEAD = 0.5
    L1_COUNT = 6

    # Mode B 资格线
    MODE_B_S = 1.25
    MODE_B_F = 0.8

    # Layer 2 变体数
    L2_COUNT = 8

    def __init__(self, campaign_dir: str, dataset: str, wave: int,
                 datasets_extra: str = "",
                 slow_fields: Optional[List[str]] = None,
                 fast_pool: Optional[List[str]] = None,
                 neutralization: str = "SECTOR",
                 decay: int = 4,
                 l0_only: bool = False,
                 skip_l0: bool = False,
                 dry_run: bool = False):
        self.campaign_dir = campaign_dir
        self.dataset = dataset
        self.wave = wave
        self.datasets_extra = datasets_extra
        self.slow_fields = slow_fields or []
        self.fast_pool = fast_pool or []
        self.neutralization = neutralization
        self.decay = decay
        self.l0_only = l0_only
        self.skip_l0 = skip_l0
        self.dry_run = dry_run
        self.executor = ProbeBatchExecutor(
            campaign_dir, dataset, wave,
            datasets_extra=datasets_extra, dry_run=dry_run)

    # ---- 候选生成 ----

    def generate_candidates(self) -> List[Dict]:
        """生成 8 条探针候选（2 单信号 + 6 组合腿，快腿轮换）。

        组合腿硬约束：0.4 慢 × 0.6 快，禁止 add(A,B) 裸混。
        快腿轮换：从 fast_pool 轮换，避免全绑同一字段。
        """
        candidates = []
        idx = 0

        # 2 条单信号探针
        for field in self.slow_fields[:2]:
            candidates.append({
                "id": f"S{idx}",
                "expression": f"rank(ts_backfill({field}, 22))",
                "family": "single",
                "fields": [field],
            })
            idx += 1

        # 6 条组合腿探针（快腿轮换）
        slow_pool = self.slow_fields * 3  # 循环用
        for i in range(self.L1_COUNT):
            slow = slow_pool[i % len(slow_pool)]
            fast = self.fast_pool[i % len(self.fast_pool)] if self.fast_pool else "close"
            # 慢腿预处理轮换：raw / reverse / ts_decay_linear
            if i % 3 == 0:
                slow_expr = f"rank(ts_backfill({slow}, 22))"
            elif i % 3 == 1:
                slow_expr = f"rank(reverse(ts_backfill({slow}, 22)))"
            else:
                slow_expr = f"rank(ts_decay_linear(ts_backfill({slow}, 22), 22))"
            fast_expr = f"rank(ts_backfill(vec_avg({fast}), 22))" if "anl" in fast else f"rank(ts_backfill({fast}, 22))"
            expr = f"add(multiply(0.4, {slow_expr}), multiply(0.6, {fast_expr}))"
            candidates.append({
                "id": f"C{idx}",
                "expression": expr,
                "family": "combo",
                "fields": [slow, fast],
            })
            idx += 1

        return candidates

    # ---- 三层执行 ----

    def run(self) -> Dict[str, Any]:
        """执行三层探针。

        Returns:
            status: L0_DEAD | L1_DEAD | WEAK_SIGNAL | MODE_B_ELIGIBLE | UPGRADED
            layers: {l0: [...], l1: [...], l2: [...]}
            best: 最强候选
            total_quota_used: 总配额消耗
        """
        candidates = self.generate_candidates()
        print(f"[tiered] 生成 {len(candidates)} 条候选 "
              f"(2 单信号 + {len(candidates)-2} 组合腿)")
        for c in candidates:
            print(f"  {c['id']}: [{c['family']}] {c['expression'][:70]}...")

        if self.dry_run:
            print("[tiered][dry-run] 仅打印，不执行回测")
            return {"status": "DRY_RUN", "candidates": candidates}

        result = {
            "status": "UNKNOWN",
            "layers": {"l0": [], "l1": [], "l2": []},
            "best": None,
            "total_quota_used": 0,
        }

        # Layer 0: 2 条快速判死（skip_l0 时跳过）
        l0_results = []
        if not self.skip_l0:
            print(f"\n{'='*50}")
            print(f"[L0] 快速判死（{self.L0_COUNT} 条）")
            print(f"{'='*50}")
            l0_candidates = self.executor.select_probe_candidates(
                candidates, n=self.L0_COUNT)
            l0_results = self.executor._run_batch(l0_candidates, layer="L0")
            result["layers"]["l0"] = l0_results
            result["total_quota_used"] += len(l0_candidates)

            l0_dead, l0_reason = self.executor.analyze_results(
                l0_results, self.L0_DEAD)
            if l0_dead == "DEAD":
                result["status"] = "L0_DEAD"
                result["decision_reason"] = l0_reason
                print(f"[L0] 判死: {l0_reason}，节省 {len(candidates)-self.L0_COUNT} 条配额")
                return result

            if self.l0_only:
                result["status"] = "L0_PASS"
                result["decision_reason"] = f"L0 有信号，l0_only 模式停止"
                return result
        else:
            print("[L0] 跳过（--skip-l0）")

        # Layer 1: 6 条信号确认
        print(f"\n{'='*50}")
        print(f"[L1] 信号确认（{self.L1_COUNT} 条）")
        print(f"{'='*50}")
        if self.skip_l0:
            l1_candidates = candidates[:self.L1_COUNT]
        else:
            l0_ids = {c.get("id") for c in l0_candidates}
            l1_candidates = [c for c in candidates if c.get("id") not in l0_ids][:self.L1_COUNT]
        l1_results = self.executor._run_batch(l1_candidates, layer="L1")
        result["layers"]["l1"] = l1_results
        result["total_quota_used"] += len(l1_candidates)

        all_results = l0_results + l1_results
        l1_dead, l1_reason = self.executor.analyze_results(
            all_results, self.L1_DEAD)
        if l1_dead == "DEAD":
            result["status"] = "L1_DEAD"
            result["decision_reason"] = l1_reason
            print(f"[L1] 判死: {l1_reason}")
            return result

        # Mode B 资格线判定
        eligible, best = self.executor.check_mode_b_eligible(all_results)
        result["best"] = best

        if not eligible:
            result["status"] = "WEAK_SIGNAL"
            best_s = max(abs(r.get("sharpe") or 0) for r in all_results)
            result["decision_reason"] = (
                f"弱信号: max|S|={best_s:.2f} 未达 ModeB 线")
            print(f"[L1] 弱信号: max|S|={best_s:.2f}")
            return result

        # Layer 2: ModeA 变体自动生成
        print(f"\n{'='*50}")
        print(f"[L2] ModeA 变体升级（{self.L2_COUNT} 条）")
        print(f"[L2] 基线: {best.get('alpha_id', '?')} "
              f"S={best.get('sharpe'):.2f} F={best.get('fitness'):.2f}")
        print(f"{'='*50}")

        l2_variants = self._generate_modea_variants(best)
        l2_results = self.executor._run_batch(l2_variants, layer="L2")
        result["layers"]["l2"] = l2_results
        result["total_quota_used"] += len(l2_variants)

        # L2 判定
        l2_eligible, l2_best = self.executor.check_mode_b_eligible(l2_results)
        if l2_best:
            result["best"] = l2_best
        all_l2 = all_results + l2_results
        final_eligible, final_best = self.executor.check_mode_b_eligible(all_l2)

        if final_eligible:
            result["status"] = "UPGRADED"
            result["best"] = final_best
            result["decision_reason"] = (
                f"L2 升级成功: {final_best.get('alpha_id', '?')} "
                f"S={final_best.get('sharpe'):.2f} F={final_best.get('fitness'):.2f}")
        else:
            result["status"] = "MODE_B_ELIGIBLE"
            result["decision_reason"] = (
                f"L1 过 ModeB 线但 L2 未提升: "
                f"best S={best.get('sharpe'):.2f} F={best.get('fitness'):.2f}")

        return result

    # ---- ModeA 变体生成 ----

    def _generate_modea_variants(self, best: Dict) -> List[Dict]:
        """基于最强候选生成 ModeA 变体（8 条）。

        变体维度：中性化 × decay × truncation × 结构
        禁止：同信号加权调参（0.4/0.6 改 0.3/0.7）
        """
        base_expr = best.get("expression", "")
        variants = []
        idx = 0

        # 中性化变体
        for neut in ["SECTOR", "SUBINDUSTRY"]:
            variants.append({
                "id": f"M{idx}",
                "expression": base_expr,
                "neutralization": neut,
                "decay": self.decay,
                "note": f"neut={neut}",
            })
            idx += 1

        # decay 变体
        for d in [2, 6]:
            variants.append({
                "id": f"M{idx}",
                "expression": base_expr,
                "neutralization": self.neutralization,
                "decay": d,
                "note": f"decay={d}",
            })
            idx += 1

        # truncation 变体
        for t in [0.02, 0.05]:
            variants.append({
                "id": f"M{idx}",
                "expression": base_expr,
                "neutralization": self.neutralization,
                "decay": self.decay,
                "truncation": t,
                "note": f"trunc={t}",
            })
            idx += 1

        # 结构变体：ts_decay_linear 包裹慢腿
        # 尝试从表达式中提取慢腿字段
        slow_field = self._extract_slow_field(base_expr)
        if slow_field:
            wrapped = base_expr.replace(
                f"ts_backfill({slow_field}, 22)",
                f"ts_decay_linear(ts_backfill({slow_field}, 22), 22)")
            if wrapped != base_expr:
                variants.append({
                    "id": f"M{idx}",
                    "expression": wrapped,
                    "neutralization": self.neutralization,
                    "decay": self.decay,
                    "note": "slow_leg_ts_decay",
                })
                idx += 1

        # 窗口变体：慢腿 w22→w66
        if slow_field:
            w66 = base_expr.replace(
                f"ts_backfill({slow_field}, 22)",
                f"ts_backfill({slow_field}, 66)")
            if w66 != base_expr:
                variants.append({
                    "id": f"M{idx}",
                    "expression": w66,
                    "neutralization": self.neutralization,
                    "decay": self.decay,
                    "note": "slow_leg_w66",
                })
                idx += 1

        return variants[:self.L2_COUNT]

    @staticmethod
    def _extract_slow_field(expr: str) -> Optional[str]:
        """从组合腿表达式中提取慢腿字段名。"""
        import re
        # 匹配 ts_backfill(field, N) 中的 field
        m = re.search(r"ts_backfill\(([a-zA-Z_][\w]*)\s*,\s*\d+\)", expr)
        return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser(description="三层探针编排器")
    ap.add_argument("--campaign-dir", required=True)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--datasets", default="",
                    help="逗号分隔额外数据集（跨金字塔 mix）")
    ap.add_argument("--wave", type=int, required=True)
    ap.add_argument("--slow-fields", required=True,
                    help="慢腿字段，逗号分隔")
    ap.add_argument("--fast-pool", required=True,
                    help="快腿字段池，逗号分隔（轮换用）")
    ap.add_argument("--neutralization", default="SECTOR")
    ap.add_argument("--decay", type=int, default=4)
    ap.add_argument("--l0-only", action="store_true",
                    help="只做 L0 快速判死")
    ap.add_argument("--skip-l0", action="store_true",
                    help="跳过 L0 直接 L1")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    slow_fields = [f.strip() for f in args.slow_fields.split(",") if f.strip()]
    fast_pool = [f.strip() for f in args.fast_pool.split(",") if f.strip()]

    orchestrator = TieredProbeOrchestrator(
        args.campaign_dir, args.dataset, args.wave,
        datasets_extra=args.datasets,
        slow_fields=slow_fields,
        fast_pool=fast_pool,
        neutralization=args.neutralization,
        decay=args.decay,
        l0_only=args.l0_only,
        skip_l0=args.skip_l0,
        dry_run=args.dry_run,
    )

    result = orchestrator.run()

    # 输出汇总
    print(f"\n{'='*60}")
    print(f"三层探针结果 - Wave {args.wave} / {args.dataset}")
    print(f"{'='*60}")
    print(f"状态: {result['status']}")
    print(f"配额消耗: {result.get('total_quota_used', 0)} 条")
    if result.get("best"):
        b = result["best"]
        print(f"最强候选: {b.get('alpha_id', '?')} "
              f"S={b.get('sharpe'):.2f} F={b.get('fitness'):.2f}")
    for layer, results in result.get("layers", {}).items():
        if results:
            print(f"  {layer}: {len(results)} 条")

    # 保存结果
    out_path = os.path.join(args.campaign_dir, "cache",
                            f"tiered_wave{args.wave}_{args.dataset}.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n结果已保存: {out_path}")

    sys.exit(0 if result["status"] not in ("L0_DEAD", "L1_DEAD") else 1)


if __name__ == "__main__":
    main()
