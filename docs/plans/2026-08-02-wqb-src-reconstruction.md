# WQB Source Reconstruction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconstruct all `src/wqb/...` Python modules referenced by the 5 BRAIN alpha-mining SKILL.md files, based solely on the API contracts, thresholds, and behavioral descriptions documented in those skills and their reference files.

**Architecture:** A Python package `wqb` with sub-packages `config`, `expression`, `research`, `search`, `memory`, `submit`. Each module is inferred from explicit function/class references, parameter signatures, return-value descriptions, and threshold tables scattered across the 5 SKILL.md files + 6 reference markdown files. The package provides CLI entry points (`wqb plan`, `wqb doctor`, `wqb operator-audit`, etc.) and importable APIs (`wqb.config.neutralization_search_order(...)`, `wqb.expression.validator.check_batch(...)`, etc.).

**Tech Stack:** Python 3.10+, dataclasses, enum, pathlib, json/sqlite3 for persistence, click for CLI.

---

## Inference Sources

All file contents are inferred from these SKILL.md references:

| Source SKILL | Referenced path | What we know |
|---|---|---|
| orchestrator §1 | `src/wqb/config.py` | search space, hard rules, `REGIONS`, `neutralization_search_order(region)`, `OP_FAMILIES` |
| orchestrator §2, research §1 | `src/wqb/research/evidence.py` | recent papers, platform guidance, design signals |
| orchestrator §3 | `src/wqb/search/scheduler.py` | budget allocation by category/region/coverage |
| orchestrator §10 | `src/wqb/memory/db.py` | simulation cache (hash dedup), bookkeeping tables |
| orchestrator §13 | `wqb.expression.validator.check_batch(...)` | batch diversity validation |
| orchestrator §15 | `src/wqb/search/news_loop.py` | `enforce_batch_diversity`, `ensure_safe_for_dispatch` |
| orchestrator §16 | `src/wqb/expression/operator_audit.py` | `GhostOperatorError`, operator audit |
| research §7 | `src/wqb/expression/paradigms.py` | 13 paradigms, `Template`, `PRE_OPS_*`, `render()` |
| research §8 | `grammar._OP_ARITY` | operator arity map |
| research §10 | `src/wqb/research/news_field_classifier.py` | 5-family classifier |
| research §13 | `src/wqb/research/hypothesis_miner.py` | `run_hypothesis_round()`, `judge()` |
| robustness Phase D | `wqb.memory.events.emit`, `wqb.search.failure_memory.record`, `submit.describer` | event/failure/describer APIs |

## File Structure

```
src/wqb/
├── __init__.py              # Package version, public API re-exports
├── config.py                # REGIONS, neutralization_search_order, OP_FAMILIES, constants
├── cli.py                   # CLI entry point (wqb plan/doctor/operator-audit/...)
├── expression/
│   ├── __init__.py
│   ├── grammar.py           # _OP_ARITY, verified operator lists, expression parser
│   ├── paradigms.py         # P1-P13 paradigms, Template dataclass, PRE_OPS_*, render()
│   ├── validator.py         # check_batch(), _shape_signature()
│   └── operator_audit.py    # operator_audit(), GhostOperatorError
├── research/
│   ├── __init__.py
│   ├── evidence.py          # Evidence dataclass, evidence registry
│   ├── news_field_classifier.py  # classify_field(), 5 families
│   └── hypothesis_miner.py  # run_hypothesis_round(), judge()
├── search/
│   ├── __init__.py
│   ├── scheduler.py         # Scheduler class, plan()
│   ├── news_loop.py         # NewsLoop, enforce_batch_diversity, ensure_safe_for_dispatch
│   └── failure_memory.py    # record(), FailureRecord
├── memory/
│   ├── __init__.py
│   ├── db.py                # SimulationDB, hash cache, bookkeeping tables
│   └── events.py            # emit(), EventLog
└── submit/
    ├── __init__.py
    └── describer.py         # describe_alpha(), annotate_soft_flags()
```

---

### Task 1: Package skeleton and config.py

**Files:**
- Create: `src/wqb/__init__.py`
- Create: `src/wqb/config.py`
- Create: `src/wqb/expression/__init__.py`
- Create: `src/wqb/research/__init__.py`
- Create: `src/wqb/search/__init__.py`
- Create: `src/wqb/memory/__init__.py`
- Create: `src/wqb/submit/__init__.py`

- [ ] **Step 1: Create all `__init__.py` files** with minimal package exports.

- [ ] **Step 2: Implement `config.py`** with:
  - `REGIONS` dict mapping region → {universes, neutralizations, delays, categories}
  - `neutralization_search_order(region)` returning full supported neutralization list
  - `OP_FAMILIES` dict grouping operators by family
  - Ghost operator blacklist (purged 2026-04-23)
  - USA default universe = `TOP3000`
  - Full USA neutralization sweep (11 options)

- [ ] **Step 3: Verify imports work** with `python -c "from wqb.config import REGIONS, neutralization_search_order"`

---

### Task 2: Expression module — grammar.py

**Files:**
- Create: `src/wqb/expression/grammar.py`

- [ ] **Step 1: Implement `grammar.py`** with:
  - `_OP_ARITY` dict: operator name → arity (1=unary, 2=binary, 3=ternary)
  - Verified-safe operator list (from research §8)
  - Ghost operator blacklist
  - Expression parser/tokenizer for shape classification

---

### Task 3: Expression module — paradigms.py

**Files:**
- Create: `src/wqb/expression/paradigms.py`

- [ ] **Step 1: Implement `paradigms.py`** with:
  - `Template` dataclass: paradigm, name, expression, asymmetric, pre_op_pool_a, pre_op_pool_b
  - 13 paradigms P1–P13 with paradigm enum
  - `PRE_OPS_WINDOWED` and `PRE_OPS_WINDOWLESS` operator pools
  - `render(tpl, a, b, pre_op=...)` function
  - 12 asymmetric variants (asym_*)
  - Template registry with all paradigm templates

---

### Task 4: Expression module — validator.py

**Files:**
- Create: `src/wqb/expression/validator.py`

- [ ] **Step 1: Implement `validator.py`** with:
  - `check_batch(expressions)` → `(ok: bool, reason: str, details: dict)`
  - Diversity gates: ≥3 dual-field, ≥2 outer wrappers, ≥2 windows, ≥2 groups, ≥2 shape signatures
  - `_shape_signature(expr)` → tuple of (top_op, binop, pre_op_family_a, pre_op_family_b, window_bucket)
  - Shape classes S1/S4/S5/S9

---

### Task 5: Expression module — operator_audit.py

**Files:**
- Create: `src/wqb/expression/operator_audit.py`

- [ ] **Step 1: Implement `operator_audit.py`** with:
  - `GhostOperatorError` exception
  - `operator_audit(live_operators)` → diff library ops vs platform, write `data/operators_verified.json`
  - `ensure_safe_for_dispatch(expressions, verified_ops)` → raises `GhostOperatorError` if ghost op found

---

### Task 6: Research module — evidence.py

**Files:**
- Create: `src/wqb/research/evidence.py`

- [ ] **Step 1: Implement `evidence.py`** with:
  - `Evidence` dataclass: source, design_implication, category, date
  - Evidence registry (list of known design signals)
  - `get_evidence()` → returns machine-usable records

---

### Task 7: Research module — news_field_classifier.py

**Files:**
- Create: `src/wqb/research/news_field_classifier.py`

- [ ] **Step 1: Implement `news_field_classifier.py`** with:
  - 5 families enum: DIRECTION, ATTENTION, DISPERSION, EVENT_TYPE, PEER_CONTEXT
  - `classify_field(field_id, description, dataset_id)` → family
  - Keyword rules per family
  - Per-dataset overrides for news12/news29/news73/news94
  - Taxonomy cache at `data/field_taxonomy/<region>_<dataset>.json`

---

### Task 8: Research module — hypothesis_miner.py

**Files:**
- Create: `src/wqb/research/hypothesis_miner.py`

- [ ] **Step 1: Implement `hypothesis_miner.py`** with:
  - `run_hypothesis_round(catalog_path, max_hypotheses=1)` → 4-alpha experiment dict
  - `judge(results)` → verdict dict (status: rejected/partially_supported/supported/needs_refinement)
  - Pseudo-signal detection: primary Sharpe ≈ control Sharpe → rejected
  - Ledger persistence to `data/hypothesis_ledger/<session>.jsonl`

---

### Task 9: Search module — scheduler.py

**Files:**
- Create: `src/wqb/search/scheduler.py`

- [ ] **Step 1: Implement `scheduler.py`** with:
  - `Scheduler` class with `plan(date)` method
  - Budget allocation by uncovered category, region priority, search coverage
  - Failure memory integration (deprioritize failed arms)
  - Session pack generation (`prepare-session-pack`, `validate-session-pack`)

---

### Task 10: Search module — news_loop.py

**Files:**
- Create: `src/wqb/search/news_loop.py`

- [ ] **Step 1: Implement `news_loop.py`** with:
  - `NewsLoop` class with closed-loop mining logic
  - `enforce_batch_diversity(batch)` → validates ≥3 buckets, ≥1 HIGH, ≥2 vec_ops, shape_variety ≥2
  - `ensure_safe_for_dispatch(expressions)` → raises `GhostOperatorError` on ghost ops
  - Beta posterior bucket sampling (biased toward D/E/P)
  - Cross-family field pairing rules
  - Event-gated template inclusion (P15)
  - Failure attribution per result

---

### Task 11: Search module — failure_memory.py

**Files:**
- Create: `src/wqb/search/failure_memory.py`

- [ ] **Step 1: Implement `failure_memory.py`** with:
  - `FailureRecord` dataclass: category, dataset, universe, paradigm, shape_bucket
  - `record(signature)` → persists failure to `data/failure_memory.jsonl`
  - `is_deprioritized(signature)` → bool
  - `get_failed_arms()` → list of failed signatures

---

### Task 12: Memory module — db.py

**Files:**
- Create: `src/wqb/memory/db.py`

- [ ] **Step 1: Implement `db.py`** with:
  - `SimulationDB` class with SQLite backend
  - Hash-based simulation cache (`get_cached(hash)`, `put_cached(hash, result)`)
  - Bookkeeping tables: `trajectories`, `trajectory_steps`, `insights`, `batch_log`
  - `doctor()` → checks all tables exist, returns report

---

### Task 13: Memory module — events.py

**Files:**
- Create: `src/wqb/memory/events.py`

- [ ] **Step 1: Implement `events.py`** with:
  - `emit(event_name, **payload)` → appends to `data/events/<today>.jsonl`
  - `EventLog` class for reading/querying events
  - Event types: `alpha.robustness_audit`, `alpha.simulation_batch`, etc.

---

### Task 14: Submit module — describer.py

**Files:**
- Create: `src/wqb/submit/describer.py`

- [ ] **Step 1: Implement `describer.py`** with:
  - `describe_alpha(alpha_details, robustness_report)` → description string
  - `annotate_soft_flags(description, soft_flags)` → annotated description
  - Economic interpretability template

---

### Task 15: CLI entry point

**Files:**
- Create: `src/wqb/cli.py`

- [ ] **Step 1: Implement `cli.py`** with click-based CLI:
  - `wqb plan --date <YYYY-MM-DD>`
  - `wqb doctor`
  - `wqb operator-audit`
  - `wqb research`
  - `wqb settings`
  - `wqb validate-session-pack <dir>`
  - `wqb prepare-session-pack --date <YYYY-MM-DD> --materialize --submission-policy manual_review`
  - `wqb news-refresh-portfolio`

---

### Task 16: Verification

- [ ] **Step 1: Verify all imports work** — `python -c "import wqb; from wqb.config import REGIONS; from wqb.expression.validator import check_batch; ..."`
- [ ] **Step 2: Run smoke tests** — verify `neutralization_search_order("USA")` returns 11 items, `check_batch([])` returns ok=False, etc.
