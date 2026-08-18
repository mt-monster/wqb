# tools/archive — 退役的一次性脚本

本目录归档原 `tools/` 下 90 个下划线前缀（`_`）一次性脚本，于 2026-08-18 统一清理。

## 为什么归档
- 全仓扫描确认这 90 个脚本**零外部引用**（无任何代码 import 或子进程调用它们），均为手动跑过即弃的分析/提交辅助脚本。
- 命名混乱、重复度高，长期沉淀造成 `tools/` 噪声（113 → 24 文件）。

## 提交类脚本的替代
原 31 个 `tools/_submit_*.py` 高度同构（仅 `path/decay/neutralization` 变异），
统一提炼为 **`tools/submit_batch.py`**（参数化、支持 `--dry-run`、多批次 `--spec`）。

等价命令示例：
```bash
# 原: python tools/_submit_insiders3_ax.py
python tools/submit_batch.py --path tracking/USA/runs/usa_insiders3_batch_ax.txt --decay 4 --neutralization SUBINDUSTRY

# 原: _submit_inst6_z.py（decay 8/12/16 三批阶梯）
python tools/submit_batch.py --spec spec.json   # spec.json: [{"path":...,"decay":8},...]
```

## 恢复方式
如需找回某个脚本：从本目录 `git mv` 回 `tools/`，或 `git log -- <path>` 追溯历史。
所有归档文件 git 历史完整保留（KOR 等同构区域脚本走 `git mv`）。
