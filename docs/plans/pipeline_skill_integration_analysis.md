# Pipeline 集成到 Skills 流程的方案分析

## 当前 Skills 架构

```
brain-deepExplore (编排入口)
    ├── brain-nextMove-analysis (每日诊断)
    ├── brain-makeSomeGem (生成候选表达式)
    ├── brain-inspectRawTemplate-create-Setting (设置扩展)
    ├── brain-enhance-template (模板增强)
    └── brain-simAlphasinBatch-and-track (批量回测+追踪)
```

## 集成目标

将 **多样性增强 pipeline** 嵌入到 skills 流程的合适位置，实现：
1. 自动多样性分析（gate 后）
2. 自动结构变异增强（submit 前）
3. 无需直接调用 MCP（复用现有 skill 的 MCP 调用）

---

## 方案对比

### 方案 A：嵌入 brain-simAlphasinBatch-and-track（推荐）

**位置**：在 `batch_simulator.py` 提交前插入多样性增强阶段

**优点**：
- ✅ 最接近实际提交点，增强效果直接
- ✅ 复用现有 skill 的 MCP 调用（无需重复实现）
- ✅ 对现有流程侵入最小
- ✅ 支持断点续跑（CSV 追踪）

**缺点**：
- ⚠️ 需要修改 `batch_simulator.py`
- ⚠️ 增强后的表达式需要重新 lint

**实现**：
```python
# 在 batch_simulator.py 的 submit 前插入
from pipeline.core.diversity_enhancer import enhance_expressions

def submit_with_diversity(exprs, **kwargs):
    # 多样性分析
    report = analyze_diversity(exprs)
    
    # 自动增强
    if need_enhance(report):
        exprs = enhance_expressions(exprs)
    
    # 原有提交逻辑
    return original_submit(exprs, **kwargs)
```

---

### 方案 B：新建 brain-diversity-enhancer skill

**位置**：在 `brain-enhance-template` 和 `brain-simAlphasinBatch-and-track` 之间插入新 skill

**优点**：
- ✅ 符合 skills 单一职责原则
- ✅ 可独立调用/测试
- ✅ 不修改现有 skill

**缺点**：
- ❌ 增加编排复杂度
- ❌ 需要修改 brain-deepExplore 的编排逻辑
- ❌  artifact 传递链变长

**实现**：
```
brain-deepExplore 编排:
    ...
    ├── brain-enhance-template (模板增强)
    ├── brain-diversity-enhancer (新增：多样性增强)  <-- 插入点
    └── brain-simAlphasinBatch-and-track (批量回测)
```

---

### 方案 C：嵌入 brain-deepExplore 编排层

**位置**：在 `brain-deepExplore` 的 Daily Loop Phases 中插入多样性检查

**优点**：
- ✅ 最高层控制，全局视角
- ✅ 可跨 skill 协调

**缺点**：
- ❌ 编排层过于厚重
- ❌ 违反 skills 单一职责
- ❌ 难以复用

---

### 方案 D：独立 pipeline 脚本 + skill 调用（当前方案）

**位置**：pipeline 作为独立脚本，skill 通过 RunTerminal 调用

**优点**：
- ✅ 完全解耦
- ✅ 可独立演进

**缺点**：
- ❌ 需要手动触发
- ❌ 与 skills 流程割裂
- ❌ 需要额外传递 artifact 路径

---

## 推荐方案：方案 A（嵌入 brain-simAlphasinBatch-and-track）

### 理由

1. **最小侵入**：只修改一个文件 `batch_simulator.py`
2. **最大复用**：直接使用现有 skill 的 MCP 调用、CSV 追踪、断点续跑
3. **最自然的位置**：提交前最后一步，确保增强后的表达式被提交
4. **符合用户习惯**：用户已经熟悉 `brain-simAlphasinBatch-and-track` 的使用

### 具体实现步骤

#### 步骤 1：创建多样性增强模块

```python
# .qoder/skills/brain-simAlphasinBatch-and-track/scripts/diversity_enhancer.py

import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from wqb.expression.diversity_enhancer import (
    analyze_diversity, enhance_expressions, DiversityMonitor
)


def enhance_if_needed(exprs, mode="auto", verbose=True):
    """
    多样性增强入口
    
    Args:
        exprs: 表达式列表
        mode: auto/always/never
        verbose: 是否打印详情
    
    Returns:
        (增强后的表达式列表, 多样性报告)
    """
    if mode == "never":
        return exprs, {"status": "skipped"}
    
    # 分析多样性
    report = analyze_diversity(exprs)
    
    if verbose:
        print(f"[diversity] 算子熵={report['current_metrics']['operator_entropy']:.3f}")
        print(f"[diversity] 覆盖率={report['current_metrics']['coverage_rate']:.2%}")
        print(f"[diversity] 新颖度={report['current_metrics']['novelty_score']:.2%}")
        print(f"[diversity] 结构相似度={report['current_metrics']['structural_similarity']:.2%}")
    
    # 判断是否需要增强
    need_enhance = False
    if mode == "always":
        need_enhance = True
    elif mode == "auto":
        m = report["current_metrics"]
        if (m['operator_entropy'] < 2.0 or
            m['coverage_rate'] < 0.5 or
            m['novelty_score'] < 0.8 or
            m['structural_similarity'] > 0.7):
            need_enhance = True
    
    if need_enhance:
        if verbose:
            print(f"[diversity] 多样性不足，执行增强...")
        enhanced, enhance_report = enhance_expressions(exprs, target_count=len(exprs))
        return enhanced, enhance_report
    
    return exprs, report
```

#### 步骤 2：修改 batch_simulator.py

```python
# 在 batch_simulator.py 的 submit 函数中插入

from diversity_enhancer import enhance_if_needed

def submit_batch(exprs, settings, **kwargs):
    # 新增：多样性增强
    exprs, diversity_report = enhance_if_needed(
        exprs, 
        mode=kwargs.get("enhance_diversity", "auto"),
        verbose=True
    )
    
    # 记录多样性报告到 CSV
    if diversity_report.get("enhanced"):
        kwargs["diversity_enhanced"] = True
        kwargs["diversity_report"] = diversity_report
    
    # 原有提交逻辑
    return original_submit_batch(exprs, settings, **kwargs)
```

#### 步骤 3：更新 SKILL.md

```markdown
## 多样性增强（2026-08-17 新增）

本 skill 已集成多样性增强 pipeline，提交前自动分析并增强表达式多样性。

### 使用方式

```powershell
# 自动模式（默认）：多样性不足时自动增强
python scripts/batch_simulator.py ... --enhance-diversity auto

# 强制增强：无论多样性指标如何都执行增强
python scripts/batch_simulator.py ... --enhance-diversity always

# 禁用增强：保持原始表达式
python scripts/batch_simulator.py ... --enhance-diversity never
```

### 增强动作

当检测到以下情况时自动增强：
- 算子熵 < 2.0（算子多样性不足）
- 覆盖率 < 50%（算子覆盖率不足）
- 新颖度 < 80%（表达式重复度过高）
- 结构相似度 > 70%（模板骨架过于相似）

增强方式包括：
- 结构变异（swap_branches/insert_layer/delete_layer 等）
- 算子替换（ts_rank → ts_scale 等）
- 添加事件门控（trade_when/if_else）
- 添加分组（group_rank/group_zscore）
```

---

## 立即可落地的最小改动

如果您希望**立即使用**而不修改现有 skill，可以使用以下**桥接脚本**：

```python
# run_batch_with_diversity.py
"""桥接脚本：在调用 brain-simAlphasinBatch-and-track 前执行多样性增强"""

import sys
import json
from pathlib import Path

# 添加项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from wqb.expression.diversity_enhancer import analyze_diversity, enhance_expressions


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="输入表达式文件")
    ap.add_argument("--output", required=True, help="输出增强后表达式文件")
    ap.add_argument("--mode", default="auto", choices=["auto", "always", "never"])
    args = ap.parse_args()
    
    # 读取表达式
    with open(args.input, encoding="utf-8") as f:
        exprs = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    print(f"[load] 加载 {len(exprs)} 个表达式")
    
    # 多样性分析
    report = analyze_diversity(exprs)
    m = report["current_metrics"]
    print(f"[diversity] 算子熵={m['operator_entropy']:.3f} "
          f"覆盖率={m['coverage_rate']:.2%} "
          f"新颖度={m['novelty_score']:.2%} "
          f"结构相似度={m['structural_similarity']:.2%}")
    
    # 判断是否需要增强
    need_enhance = False
    if args.mode == "always":
        need_enhance = True
    elif args.mode == "auto":
        if (m['operator_entropy'] < 2.0 or
            m['coverage_rate'] < 0.5 or
            m['novelty_score'] < 0.8 or
            m['structural_similarity'] > 0.7):
            need_enhance = True
    
    if need_enhance:
        print(f"[diversity] 执行增强...")
        exprs, enhance_report = enhance_expressions(exprs, target_count=len(exprs))
        print(f"[diversity] 增强完成")
    else:
        print(f"[diversity] 多样性良好，无需增强")
    
    # 写入输出
    with open(args.output, "w", encoding="utf-8") as f:
        for expr in exprs:
            f.write(expr + "\n")
    
    print(f"[output] 已写入 {args.output}")
    print(f"[next] 请使用 brain-simAlphasinBatch-and-track 提交:")
    print(f"  python scripts/batch_simulator.py --alpha-json {args.output} ...")


if __name__ == "__main__":
    main()
```

使用方式：
```powershell
# 1. 多样性增强
python run_batch_with_diversity.py --input tracking/GBR/candidates/gbr_model106_batch8.txt --output tracking/GBR/candidates/gbr_model106_batch8_enhanced.txt --mode auto

# 2. 使用现有 skill 提交
Set-Location ".qoder/skills/brain-simAlphasinBatch-and-track"
python scripts/batch_simulator.py --alpha-json ../../../tracking/GBR/candidates/gbr_model106_batch8_enhanced.txt ...
```

---

## 决策建议

| 场景 | 推荐方案 | 理由 |
|:---|:---|:---|
| 立即使用，不改代码 | 桥接脚本 | 零侵入，立即可用 |
| 长期使用，愿意改代码 | 方案 A（嵌入 batch_simulator） | 最自然，复用现有基础设施 |
| 严格遵循 skills 架构 | 方案 B（新建 skill） | 符合单一职责，但编排复杂 |

**当前建议**：先用桥接脚本验证效果，确认多样性增强有价值后再嵌入 `batch_simulator.py`。
