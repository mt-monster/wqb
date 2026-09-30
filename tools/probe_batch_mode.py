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

from mcp_batch_writer import DirectDBWriter  # noqa: E402

# toolkit scripts 目录解析：tools/skill_paths（与 wave_gate / workflow 节点同一顺序，2026-09-27 R12）
from skill_paths import skill_script_dirs  # noqa: E402

_TOOLKIT_CANDIDATES = skill_script_dirs("wq-brain-campaign-toolkit", "WQ_TOOLKIT_DIR")


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
    # 不传路径 = store.default_db_path()：WQB_DB_PATH 优先，否则 <repo>/data/wqb.db（R19 同口径）
    return CampaignStore()


class ProbeBatchExecutor:
    """探针批执行器（真实回测版）"""

    # Layer 0 判死阈值（快速判死）
    L0_DEAD_THRESHOLD = 0.3   # |S|<0.3 判死
    # Layer 1 判死阈值（KOR 加严）
    L1_DEAD_THRESHOLD = 0.5   # |S|<0.5 判死
    # Mode B 资格线（2026-09-04 方案 B：默认单点模式，可被 thresholds.json 覆盖为分布模式）
    MODE_B_S = 1.25
    MODE_B_F = 0.8

    def __init__(self, campaign_dir: str, dataset: str, wave: int,
                 datasets_extra: str = "", dry_run: bool = False,
                 probe_size: int = 2, full_size: int = 6,
                 pipeline_timeout: int = 1500):
        self.campaign_dir = campaign_dir
        self.dataset = dataset
        self.wave = wave
        self.datasets_extra = datasets_extra
        self.dry_run = dry_run
        # 2026-09-29 修复：--probe-size / --full-size 此前被完全忽略（execute 硬编码
        # n=2 / [:6]），导致用户传 --probe-size 8 仍只跑 2 条探针。
        self.probe_size = max(1, int(probe_size))
        self.full_size = max(0, int(full_size))
        # pipeline 子进程超时（秒）。600s 会把未跑完的多模拟误判为"无回测结果"。
        self.pipeline_timeout = max(60, int(pipeline_timeout))
        self.toolkit_dir = _find_toolkit()
        self.mcp_py = _find_mcp_python()
        # 2026-09-04 方案 B：从 thresholds.json 读区域化 Mode B 配置（含分布感知参数）
        self._mode_b_cfg = self._load_mode_b_config()

    def _load_mode_b_config(self) -> Dict[str, Any]:
        """加载 Mode B 配置（2026-09-09 起主闸委托 mode_b_config 统一加载器）.

        主闸 sharpe_min/fitness_min 从 mode_b_config.load_mode_b_config 取（解析
        $ref / 全局权威 / 区域覆盖 / 自适应学习区域 ledger），不再直接读区域文件
        的硬编码字段（区域文件已改为 $ref 引用全局）。
        distribution 模式的 p75/count 字段仍从区域 thresholds.json 读（该模式为
        区域实验特性，未上收全局）。

        返回字段：
          - mode: "point"（单点，默认）| "distribution"（分布感知）
          - sharpe_min / fitness_min: 单点模式阈值（主闸，来自统一加载器）
          - sharpe_p75_min / fitness_p75_min: 分布模式 p75 分位阈值
          - count_above_min: 分布模式至少 N 条过线（与 p75 二选一）
        """
        # 主闸：委托统一加载器（含 $ref 解析与全局兜底）
        main = {"sharpe_min": self.MODE_B_S, "fitness_min": self.MODE_B_F}
        try:
            repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            src = os.path.join(repo_root, "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            from wqb.workflow.mode_b_config import load_mode_b_config
            region = self._resolve_region()
            store = None
            try:
                store = _wqb_store()
            except Exception:
                store = None
            try:
                cfg_full = load_mode_b_config(store, region=region)
                mg = cfg_full.get("main_gate") or {}
                main["sharpe_min"] = float(mg.get("sharpe_min", self.MODE_B_S))
                main["fitness_min"] = float(mg.get("fitness_min", self.MODE_B_F))
            finally:
                if store is not None:
                    try:
                        store.close()
                    except Exception:
                        pass
        except Exception:
            pass

        default = {
            "mode": "point",
            "sharpe_min": main["sharpe_min"],
            "fitness_min": main["fitness_min"],
        }
        try:
            thresholds_path = os.path.join(
                self.campaign_dir, "config", "thresholds.json"
            )
            if not os.path.exists(thresholds_path):
                return default
            with open(thresholds_path, "r", encoding="utf-8") as f:
                thresholds = json.load(f)
            mbq = thresholds.get("mode_b_qualification", {})
            if not isinstance(mbq, dict):
                return default
            # 合并配置：主闸以统一加载器为准（不被区域旧硬编码覆盖），
            # 仅 distribution 模式字段从区域文件读
            cfg = default.copy()
            cfg["mode"] = mbq.get("mode", "point")
            if cfg["mode"] == "distribution":
                cfg["sharpe_p75_min"] = float(mbq.get("sharpe_p75_min", cfg["sharpe_min"]))
                cfg["fitness_p75_min"] = float(mbq.get("fitness_p75_min", cfg["fitness_min"]))
                cfg["count_above_min"] = int(mbq.get("count_above_min", 2))
            return cfg
        except Exception:
            return default

    # ---- 候选选择 ----

    def _poison_prefilter(self, candidates: List[Dict]) -> List[Dict]:
        """闸5 `equal_weight_leg_add` 预过滤（2026-09-29 新增）。

        背景：pv30 探针批实证 —— 含 `add(abs(A),abs(B))` 归一化分母的表达式会被
        wave_gate 的闸5 结构判定拦成 `[POISON:equal_weight_leg_add]`，导致
        `pipeline.py run` 退出码 1、**整批未提交回测**，probe 被误判 PROBE_DEAD
        （"无回测结果"实为 gate 拦截，非信号弱）。故在提交前先用 toolkit
        `gate._detect_equal_weight_leg_add` 同源判定剔除，避免整批白跑。

        判定与 wave_gate 完全同源（复用 gate.py 实现，非另写正则），符合
        「文档里的安全承诺必须与实现同源校验」纪律。

        Returns:
            保留的候选列表（被 POISON 判中的剔除）；判定不可用时原样返回。
        """
        import re as _re
        try:
            scripts = self.toolkit_dir
            if scripts not in sys.path:
                sys.path.insert(0, scripts)
            import gate as gate_mod  # noqa: WPS433
            from _lib.common import load_platform_constraints  # noqa: WPS433
            pc = load_platform_constraints()
            base_non_field = (
                set(pc.get("known_ops", []))
                | set(pc.get("group_identifiers", []))
                | set(pc.get("driver_args", []))
            )
        except Exception as exc:  # 判定不可用则跳过，不阻断
            print(f"[poison-prefilter] 预过滤不可用（{exc}），跳过")
            return candidates

        kept, dropped = [], []
        for c in candidates:
            expr = c.get("expression", "") or ""
            if not expr:
                continue
            # kw_args：表达式内 `name=` 形式的名字（与 gate.check_one 同口径）
            kw = set(_re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=", expr))
            non_field = base_non_field | kw
            try:
                if gate_mod._detect_equal_weight_leg_add(expr, non_field):
                    dropped.append(c)
                    continue
            except Exception:
                pass  # 单条判定失败→保留，交给 wave_gate 兜底
            kept.append(c)

        if dropped:
            print(f"[poison-prefilter] 剔除 {len(dropped)} 条 "
                  f"equal_weight_leg_add 高危，保留 {len(kept)} 条")
            for d in dropped[:5]:
                print(f"  - {d.get('id', '?')}: {d.get('expression', '')[:90]}")
        return kept

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
        """检查是否有候选过 Mode B 资格线（2026-09-04 方案 B：支持分布感知）.

        单点模式（point，旧行为）：max(sharpe) >= S 且 max(fitness) >= F
        分布模式（distribution）：
          - sharpe_p75 >= X 且 fitness_p75 >= Y（前 25% 候选的分位值）
          - 或 count(sharpe >= S 且 fitness >= F) >= N（至少 N 条过线）
        """
        cfg = self._mode_b_cfg
        mode = cfg.get("mode", "point")

        # 提取有效候选（sharpe/fitness 非空）
        valid = []
        for r in results:
            s = abs(r.get("sharpe") or 0)
            f = r.get("fitness") or 0
            if s > 0 or f > 0:
                valid.append({"sharpe": s, "fitness": f, "raw": r})

        if not valid:
            return (False, None)

        if mode == "distribution":
            # 分布感知模式
            sharpes = sorted([v["sharpe"] for v in valid], reverse=True)
            fitnesses = sorted([v["fitness"] for v in valid], reverse=True)
            # p75 分位（前 25%）
            p75_idx = max(0, int(len(sharpes) * 0.25) - 1)
            sharpe_p75 = sharpes[p75_idx] if sharpes else 0
            fitness_p75 = fitnesses[p75_idx] if fitnesses else 0
            # count 过线条数
            count_above = sum(
                1 for v in valid
                if v["sharpe"] >= cfg["sharpe_min"] and v["fitness"] >= cfg["fitness_min"]
            )
            # 判定：p75 达标 或 count 达标
            p75_ok = (sharpe_p75 >= cfg.get("sharpe_p75_min", cfg["sharpe_min"])
                      and fitness_p75 >= cfg.get("fitness_p75_min", cfg["fitness_min"]))
            count_ok = count_above >= cfg.get("count_above_min", 2)
            eligible = p75_ok or count_ok
            best = max(valid, key=lambda v: v["sharpe"])["raw"] if eligible else None
            return (eligible, best)

        # 单点模式（旧行为）
        best = None
        for v in valid:
            if v["sharpe"] >= cfg["sharpe_min"] and v["fitness"] >= cfg["fitness_min"]:
                if best is None or v["sharpe"] > abs(best.get("sharpe") or 0):
                    best = v["raw"]
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
        # 闸5 equal_weight_leg_add 预过滤：剔除会被 wave_gate POISON 拦的表达式
        candidates = self._poison_prefilter(candidates)
        if not candidates:
            return {"status": "PROBE_DEAD", "l0_results": [],
                    "l1_results": None, "best": None, "saved_quota": 0,
                    "decision_reason": "全部候选命中闸5 equal_weight_leg_add 预过滤"}

        # Phase 1: Layer 0 探针批（默认 2 条，可经 --probe-size 调整）
        probe_candidates = self.select_probe_candidates(
            candidates, n=self.probe_size)
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
            result["saved_quota"] = max(0, len(candidates) - self.probe_size)
            print(f"[L0] 判死: {reason}，节省 {result['saved_quota']} 条配额")
            return result

        # Phase 2: Layer 1 完整批（剩余条数，可经 --full-size 调整）
        remaining = [c for i, c in enumerate(candidates)
                     if c.get("id", i) not in probe_ids][:self.full_size]
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
        # 2026-09-29：600s 硬编码超时会导致多模拟未跑完就被判"无回测结果"
        # （假判死 PROBE_DEAD）。改为可配置，默认 1500s 覆盖 DEU 八槽批实测耗时。
        # 2026-09-29（二修）：cwd 必须是仓库根。原写 dirname²(toolkit_dir)——
        # 解析到 ~/.claude/skills（个人配置目录）时，pipeline 的日志清理会触发
        # SAFE_DELETE_BULK_CONFIRM_REQUIRED 删除安全闸 → 秒退 exit 1 →
        # 回落 DB 历史行误判（max|S| 取自陈旧行）。repo_root = tools/ 的上一级。
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True,
                timeout=self.pipeline_timeout,
                cwd=repo_root,
            )
        except subprocess.TimeoutExpired:
            print(f"[{layer}] pipeline 超时（{self.pipeline_timeout}s），"
                  f"尝试从 DB 拉已有结果")
            return self._fetch_batch_results(wave_str, exprs)

        print(f"[{layer}] pipeline 退出码: {proc.returncode}")
        if proc.stdout:
            for line in proc.stdout.splitlines():
                if any(k in line for k in
                       ["[submit]", "[poll]", "[done]",
                        "COMPLETE", "ERROR", "FAIL"]):
                    print(f"  {line}")
        # 2026-09-29 修复：exit!=0 时只打 stdout 过滤行 + stderr 末 500 字符，
        # 真报错（traceback / gate 拦截原因）常被 safe-delete 等噪音顶掉 → 假判死。
        # 失败时必须给出 stdout/stderr 尾部全文（各 3000 字符）。
        if proc.returncode != 0:
            if proc.stdout:
                print(f"[{layer}] stdout 尾部:\n{proc.stdout[-3000:]}",
                      file=sys.stderr)
            if proc.stderr:
                print(f"[{layer}] stderr 尾部:\n{proc.stderr[-3000:]}",
                      file=sys.stderr)

        # 4. 从 DB 拉回测结果
        return self._fetch_batch_results(wave_str, exprs)

    def _fetch_batch_results(self, wave: str, exprs: List[str]) -> List[Dict]:
        """拉回测结果并只保留本批表达式。

        2026-09-29 三修：_fetch_results 会拉全波历史行，pipeline 失败时
        max|S| 取自陈旧行 → 探针判定被污染（实测误报 WEAK_SIGNAL）。
        判定只允许看本批表达式的结果行。
        """
        rows = self._fetch_results(wave)
        want = set(exprs or [])
        if not want:
            return rows
        kept = [r for r in rows if (r.get("expression") or "") in want]
        print(f"[db] 本批表达式命中 {len(kept)}/{len(rows)} 条（其余为陈旧行，不参与判定）")
        if not kept and rows:
            print(f"[db][WARN] 本批 0 条命中但全波有 {len(rows)} 条陈旧行——"
                  f"pipeline 结果只落 checkpoint，需 harvest_multisim_alphas 收批后"
                  f"再判定；禁止回退用陈旧行下结论")
        return kept

    def _upsert_exprs(self, exprs: List[str], wave: str):
        """表达式入库（走 DirectDBWriter，WAL 优化版）。"""
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(repo_root, "data", "wqb.db")
        region = self._resolve_region()
        items = [{"expression": e, "status": "gated"} for e in exprs]
        with DirectDBWriter(db_path) as writer:
            r = writer.upsert_expressions(region, wave, items, dataset=self.dataset)
        if "error" in r:
            print(f"[db][ERROR] 入库失败: {r['error']}")
        else:
            print(f"[db] 入库 {r.get('n')} 条 wave={wave}")

    def _fetch_results(self, wave: str) -> List[Dict]:
        """从 DB 拉回测结果（backtest_results 表，DirectDBWriter 只读）。"""
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(repo_root, "data", "wqb.db")
        region = self._resolve_region()
        # 读操作仍走 CampaignStore（DirectDBWriter 未实现 list_backtest_rows）
        st = _wqb_store()
        try:
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
    ap.add_argument("--wave", required=True,
                    help="波号（字符串，支持 '97' / 's2_pattern_scores_d1' 等）")
    ap.add_argument("--candidates", help="候选表达式 JSON（与 --from-db 二选一）")
    ap.add_argument("--from-db", action="store_true",
                    help="从 expressions 表读候选（推荐）")
    ap.add_argument("--probe-size", type=int, default=2, help="探针批大小")
    ap.add_argument("--full-size", type=int, default=6, help="完整批大小")
    ap.add_argument("--pipeline-timeout", type=int, default=1500,
                    help="pipeline 子进程超时秒数（默认 1500，避免多模拟未跑完被误判）")
    ap.add_argument("--dry-run", action="store_true",
                    help="只打印探针分配，不执行回测")
    args = ap.parse_args()

    # 2026-09-29 修复：--campaign-dir 传相对路径时，pipeline 子进程 cwd = skill
    # 脚本目录（common.py 用 os.path.abspath(campaign_dir or os.getcwd()) 相对解析），
    # 会解析到 skill 安装位（~/.claude/skills/tracking/...）→ FileNotFoundError。
    # 这里统一转绝对路径，从根上消除 cwd 依赖。
    args.campaign_dir = os.path.abspath(args.campaign_dir)

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
        datasets_extra=args.datasets, dry_run=args.dry_run,
        probe_size=args.probe_size, full_size=args.full_size,
        pipeline_timeout=args.pipeline_timeout)
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
