# -*- coding: utf-8 -*-
"""probe_batch_mode.py - 2+6 探针批模式（早期判死机制，真实回测版）。

核心逻辑：
  1. Layer 0：先跑 2 条探针（最强候选），|S|<0.3 判死，省 6 条配额
  2. Layer 1：有信号则继续跑剩余 6 条，无 |S|>=0.5 判死（KOR 加严）
  3. Mode B 资格线判定：最强候选 S>=1.25 且 F>=0.8 则提示升级

真实回测路径：expressions 入库 → pipeline.py run --submit → 等 checkpoint → DB 拉指标。

用法:
  # dry-run 只打印探针分配，不执行回测
  python tools/probe_batch_mode.py --campaign-dir tracking/KOR \
      --dataset risk88 --datasets analyst16 --wave 165 --dry-run

  # 正式执行（入库 + 回测 + 判定）
  python tools/probe_batch_mode.py --campaign-dir tracking/KOR \
      --dataset risk88 --datasets analyst16 --wave 165

  # 从 DB 读候选（推荐，与 wave_gate.py --from-db 同源）
  python tools/probe_batch_mode.py --campaign-dir tracking/KOR \
      --dataset risk88 --wave 165 --from-db
"""
import argparse
import json
import os
import subprocess
import sys
from typing import Dict, List, Any, Tuple, Optional

# 添加 tools 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# toolkit scripts 目录解析（与 wave_gate.py 同一模式）
_TOOLKIT_CANDIDATES = [
    os.environ.get("WQ_TOOLKIT_DIR"),
    os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills",
                 "wq-brain-campaign-toolkit", "scripts"),
    os.path.join(os.path.expanduser("~"), ".cursor", "skills",
                 "wq-brain-campaign-toolkit", "scripts"),
    os.path.join(os.path.expanduser("~"), ".workbuddy", "skills",
                 "wq-brain-campaign-toolkit", "scripts"),
]


def _find_toolkit() -> str:
    for d in _TOOLKIT_CANDIDATES:
        if d and os.path.isfile(os.path.join(d, "pipeline.py")):
            return d
    raise FileNotFoundError(
        f"未找到 pipeline.py：设 WQ_TOOLKIT_DIR 指定"
        f"（已搜 {', '.join(c for c in _TOOLKIT_CANDIDATES if c)}）")


def _find_mcp_python() -> str:
    """MCP venv Python 解释器（网络调用必须走 venv）。"""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    venv_py = os.path.join(repo_root, "world-quant-brain-mcp",
                           ".venv", "Scripts", "python.exe")
    if os.path.isfile(venv_py):
        return venv_py
    return sys.executable


def _wqb_store():
    """加载 CampaignStore（延迟导入，避免模块级依赖）。"""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(repo_root, "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    from wqb.store import CampaignStore
    db_path = os.path.join(repo_root, "data", "wqb.db")
    return CampaignStore(db_path)


class ProbeBatchExecutor:
    """探针批执行器（真实回测版）"""

    # Layer 0 判死阈值（快速判死）
    L0_DEAD_THRESHOLD = 0.3   # |S|<0.3 判死
    # Layer 1 判死阈值（KOR 加严）
    L1_DEAD_THRESHOLD = 0.5   # |S|<0.5 判死
    # Mode B 资格线
    MODE_B_S = 1.25
    MODE_B_F = 0.8

    def __init__(self, campaign_dir: str, dataset: str, wave: int,
                 datasets_extra: str = "", dry_run: bool = False):
        self.campaign_dir = campaign_dir
        self.dataset = dataset
        self.wave = wave
        self.datasets_extra = datasets_extra
        self.dry_run = dry_run
        self.toolkit_dir = _find_toolkit()
        self.mcp_py = _find_mcp_python()

    # ---- 候选选择 ----

    def select_probe_candidates(self, candidates: List[Dict],
                                 n: int = 2) -> List[Dict]:
        """选择最强探针候选（质量预估 + 多样性启发式）。"""
        scored = []
        for c in candidates:
            score = 0
            if c.get("quality_verdict") == "EXPECTED_PASS":
                score += 100
            elif c.get("quality_verdict") == "REVIEW":
                score += 50
            expr = c.get("expression", "")
            if "ts_backfill" in expr:
                score += 10
            if "group_neutralize" in expr:
                score += 10
            if "add" in expr and "multiply" in expr:
                score += 15  # 组合腿加分
            if "rank" in expr:
                score += 5
            scored.append((score, c))
        scored.sort(key=lambda x: -x[0])
        return [c for _, c in scored[:n]]

    # ---- 结果分析 ----

    def analyze_results(self, results: List[Dict],
                        threshold: float) -> Tuple[str, str]:
        """分析回测结果，返回 (decision, reason)。"""
        sharpes = [abs(r.get("sharpe") or 0) for r in results]
        if not sharpes:
            return "DEAD", "无回测结果"
        if all(s < threshold for s in sharpes):
            return "DEAD", (f"全灭: |S|={['%.2f' % s for s in sharpes]}, "
                            f"均<{threshold}")
        best = max(sharpes)
        return "CONTINUE", f"有信号: max|S|={best:.2f}>={threshold}"

    def check_mode_b_eligible(self, results: List[Dict]
                               ) -> Tuple[bool, Optional[Dict]]:
        """检查是否有候选过 Mode B 资格线。"""
        best = None
        for r in results:
            s = abs(r.get("sharpe") or 0)
            f = r.get("fitness") or 0
            if s >= self.MODE_B_S and f >= self.MODE_B_F:
                if best is None or s > abs(best.get("sharpe") or 0):
                    best = r
        return (best is not None, best)

    # ---- 主执行流程 ----

    def execute(self, candidates: List[Dict]) -> Dict[str, Any]:
        """执行 2+6 探针批（真实回测）。

        Returns:
            status: PROBE_DEAD | WEAK_SIGNAL | MODE_B_ELIGIBLE | DRY_RUN
            l0_results: Layer 0 回测结果
            l1_results: Layer 1 回测结果（判死时为 None）
            best: 最强候选（过 Mode B 线时非 None）
            saved_quota: 节省的配额条数
            decision_reason: 判定原因
        """
        # Phase 1: Layer 0 探针批（2 条）
        probe_candidates = self.select_probe_candidates(candidates, n=2)
        probe_ids = [c.get("id", i) for i, c in enumerate(probe_candidates)]

        print(f"[L0] 探针候选 ({len(probe_candidates)} 条):")
        for c in probe_candidates:
            print(f"  - {c.get('id', '?')}: "
                  f"{c.get('expression', '')[:80]}...")

        if self.dry_run:
            print("[L0][dry-run] 仅打印，不执行回测")
            return {"status": "DRY_RUN", "l0_results": [],
                    "l1_results": None, "best": None,
                    "saved_quota": 0, "decision_reason": "dry-run"}

        l0_results = self._run_batch(probe_candidates, layer="L0")
        decision, reason = self.analyze_results(
            l0_results, self.L0_DEAD_THRESHOLD)

        result = {
            "status": f"PROBE_{decision}",
            "l0_results": l0_results,
            "l1_results": None,
            "best": None,
            "saved_quota": 0,
            "decision_reason": reason,
        }

        if decision == "DEAD":
            result["saved_quota"] = len(candidates) - 2
            print(f"[L0] 判死: {reason}，节省 {result['saved_quota']} 条配额")
            return result

        # Phase 2: Layer 1 完整批（剩余 6 条）
        remaining = [c for i, c in enumerate(candidates)
                     if c.get("id", i) not in probe_ids][:6]
        print(f"[L1] 继续完整批: {len(remaining)} 条")
        l1_results = self._run_batch(remaining, layer="L1")
        all_results = l0_results + l1_results
        result["l1_results"] = l1_results

        # Layer 1 判定
        l1_decision, l1_reason = self.analyze_results(
            all_results, self.L1_DEAD_THRESHOLD)
        result["decision_reason"] = l1_reason

        if l1_decision == "DEAD":
            result["status"] = "PROBE_DEAD"
            print(f"[L1] 判死: {l1_reason}")
            return result

        # Mode B 资格线判定
        eligible, best = self.check_mode_b_eligible(all_results)
        result["best"] = best
        if eligible:
            result["status"] = "MODE_B_ELIGIBLE"
            print(f"[L1] Mode B 达标: {best.get('alpha_id', '?')} "
                  f"S={best.get('sharpe'):.2f} F={best.get('fitness'):.2f}")
        else:
            result["status"] = "WEAK_SIGNAL"
            best_s = max(abs(r.get("sharpe") or 0) for r in all_results)
            print(f"[L1] 弱信号: max|S|={best_s:.2f} 未达 ModeB 线 "
                  f"(S>={self.MODE_B_S} 且 F>={self.MODE_B_F})")

        return result

    # ---- 真实回测 ----

    def _run_batch(self, candidates: List[Dict],
                   layer: str = "L0") -> List[Dict]:
        """真实回测：入库 → pipeline.py run --submit → DB 拉指标。

        复用 pipeline.py 的七槽填槽/checkpoint/配额闸，不重复造轮子。
        """
        exprs = [c.get("expression", "") for c in candidates
                 if c.get("expression")]
        if not exprs:
            print(f"[{layer}] 无表达式，跳过")
            return []

        # 1. 入库（status=gated，pipeline.py 从 DB 读）
        wave_str = str(self.wave)
        self._upsert_exprs(exprs, wave_str)

        # 2. 构建 pipeline.py 命令
        pipeline_py = os.path.join(self.toolkit_dir, "pipeline.py")
        cmd = [
            self.mcp_py, pipeline_py, "run",
            "--campaign-dir", self.campaign_dir,
            "--dataset", self.dataset,
            "--wave", wave_str,
            "--submit",
            "--skip-diversity-gate",
            "--fresh",
        ]
        if self.datasets_extra:
            cmd.extend(["--datasets", self.datasets_extra])

        print(f"[{layer}] 提交回测: n={len(exprs)}")

        # 3. 执行（同步等待，pipeline 内部有 checkpoint 断点续跑）
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True,
                timeout=600,
                cwd=os.path.dirname(os.path.dirname(self.toolkit_dir)),
            )
        except subprocess.TimeoutExpired:
            print(f"[{layer}] pipeline 超时（600s），尝试从 DB 拉已有结果")
            return self._fetch_results(wave_str)

        print(f"[{layer}] pipeline 退出码: {proc.returncode}")
        if proc.stdout:
            for line in proc.stdout.splitlines():
                if any(k in line for k in
                       ["[submit]", "[poll]", "[done]",
                        "COMPLETE", "ERROR", "FAIL"]):
                    print(f"  {line}")
        if proc.returncode != 0 and proc.stderr:
            print(f"[{layer}] stderr: {proc.stderr[-500:]}",
                  file=sys.stderr)

        # 4. 从 DB 拉回测结果
        return self._fetch_results(wave_str)

    def _upsert_exprs(self, exprs: List[str], wave: str):
        """表达式入库（走 CampaignStore）。"""
        st = _wqb_store()
        try:
            region = self._resolve_region()
            items = [{"expression": e, "status": "gated"} for e in exprs]
            r = st.upsert_expressions(region, wave, items,
                                      dataset=self.dataset)
            print(f"[db] 入库 {r.get('n')} 条 wave={wave}")
        finally:
            st.close()

    def _fetch_results(self, wave: str) -> List[Dict]:
        """从 DB 拉回测结果（backtest_results 表）。"""
        st = _wqb_store()
        try:
            region = self._resolve_region()
            rows = st.list_backtest_rows(region, wave)
            results = []
            for r in rows:
                results.append({
                    "alpha_id": r.get("alpha_id"),
                    "expression": r.get("code") or r.get("expression"),
                    "sharpe": r.get("sharpe"),
                    "fitness": r.get("fitness"),
                    "turnover": r.get("turnover"),
                    "status": r.get("status"),
                })
            print(f"[db] 拉取 {len(results)} 条回测结果 wave={wave}")
            return results
        finally:
            st.close()

    def _resolve_region(self) -> str:
        """从 campaign_dir 解析 region。"""
        settings_path = os.path.join(self.campaign_dir, "config",
                                     "settings.json")
        if os.path.isfile(settings_path):
            with open(settings_path, encoding="utf-8") as f:
                return json.load(f).get("region", "KOR")
        return os.path.basename(self.campaign_dir.rstrip("/\\"))


def main():
    ap = argparse.ArgumentParser(description="2+6 探针批模式（真实回测版）")
    ap.add_argument("--campaign-dir", required=True)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--datasets", default="",
                    help="逗号分隔额外数据集（跨金字塔 mix）")
    ap.add_argument("--wave", type=int, required=True)
    ap.add_argument("--candidates", help="候选表达式 JSON（与 --from-db 二选一）")
    ap.add_argument("--from-db", action="store_true",
                    help="从 expressions 表读候选（推荐）")
    ap.add_argument("--probe-size", type=int, default=2, help="探针批大小")
    ap.add_argument("--full-size", type=int, default=6, help="完整批大小")
    ap.add_argument("--dry-run", action="store_true",
                    help="只打印探针分配，不执行回测")
    args = ap.parse_args()

    # 加载候选
    if args.from_db:
        st = _wqb_store()
        try:
            executor_tmp = ProbeBatchExecutor(
                args.campaign_dir, args.dataset, args.wave,
                datasets_extra=args.datasets, dry_run=True)
            region = executor_tmp._resolve_region()
            rows = st.list_expressions(region, str(args.wave),
                                       dataset=args.dataset)
            candidates = [{"id": r.get("id"), "expression": r.get("expression")}
                          for r in rows if r.get("expression")]
        finally:
            st.close()
        if not candidates:
            print(f"db 无候选: wave={args.wave} dataset={args.dataset}")
            sys.exit(1)
    elif args.candidates:
        with open(args.candidates, encoding="utf-8") as f:
            data = json.load(f)
        candidates = (data if isinstance(data, list)
                      else data.get("expressions", []))
    else:
        print("需要 --candidates 或 --from-db 之一")
        sys.exit(1)

    executor = ProbeBatchExecutor(
        args.campaign_dir, args.dataset, args.wave,
        datasets_extra=args.datasets, dry_run=args.dry_run)
    result = executor.execute(candidates)

    # 输出结果
    print(f"\n{'=' * 60}")
    print(f"探针批模式结果 - Wave {args.wave} / {args.dataset}")
    print(f"{'=' * 60}")
    print(f"状态: {result['status']}")
    print(f"决策原因: {result['decision_reason']}")
    print(f"节省配额: {result['saved_quota']} 条")

    if result.get("best"):
        b = result["best"]
        print(f"\n最强候选: {b.get('alpha_id', '?')} "
              f"S={b.get('sharpe'):.2f} F={b.get('fitness'):.2f}")

    if result.get("l1_results"):
        print(f"\n完整批结果: {len(result['l1_results'])} 条")

    # 保存结果
    out_path = os.path.join(args.campaign_dir, "cache",
                            f"probe_wave{args.wave}_{args.dataset}.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存: {out_path}")

    sys.exit(0 if result["status"] != "PROBE_DEAD" else 1)


if __name__ == "__main__":
    main()
