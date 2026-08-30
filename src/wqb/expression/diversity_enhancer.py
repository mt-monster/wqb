# -*- coding: utf-8 -*-
"""Alpha表达式多样性增强系统.

提供操作符探索率提升、模板骨架多样性增强、实时多样性监控等功能.

Architecture (2026-08-29 refactor): the original 962-line monolith was
split into focused submodules. This file re-exports all public names
for backward compatibility.

    diversity_enhancer.py (facade, re-exports)
      ├── _op_signatures.py   DiversityMetrics, UNARY/BINARY_OPS, op_arity_style
      ├── _metrics.py         OperatorQuotaManager, DiversityMonitor
      └── _enhancer.py        StructuralMutationEngine, DiversityEnhancer,
                               enhance_expressions, analyze_diversity, signal_evidence_gate
"""
from __future__ import annotations

# Re-export all public names — backward compatibility with
# `from wqb.expression.diversity_enhancer import …`
from ._op_signatures import (  # noqa: F401
    BINARY_OPS,
    UNARY_OPS,
    DiversityMetrics,
    op_arity_style,
)
from ._metrics import (  # noqa: F401
    DiversityMonitor,
    OperatorQuotaManager,
)
from ._enhancer import (  # noqa: F401
    DiversityEnhancer,
    StructuralMutationEngine,
    analyze_diversity,
    enhance_expressions,
    signal_evidence_gate,
)

__all__ = [
    "DiversityMetrics",
    "OperatorQuotaManager",
    "StructuralMutationEngine",
    "DiversityMonitor",
    "DiversityEnhancer",
    "op_arity_style",
    "UNARY_OPS",
    "BINARY_OPS",
    "enhance_expressions",
    "analyze_diversity",
    "signal_evidence_gate",
]
