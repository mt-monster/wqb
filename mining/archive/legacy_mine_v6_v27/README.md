# legacy_mine_v6_v27 — 退役的挖掘版本脚本（archive）

> 归档日期：2026-08-18 | 原因：版本爆炸治理

这 22 个 `mine_v6.py .. mine_v27.py` 是历史挖掘脚本，彼此是复制粘贴变体（版本爆炸）。
已被 `mining/scripts/mine_core.py`（参数化模板 + checkpoint/resume）取代。

**规则：**
- 本目录只读归档，**禁止**再往这里添加新版本脚本。
- 新挖掘任务一律用 `mining/scripts/mine_core.py`，以"数据（候选列表 + 设置）"而非"脚本副本"表达差异。
- 需要复现历史结果时，从 git 历史或本目录找回（`git log -- mining/archive/mine_v20.py`）。
- 本目录脚本仍含 `C:/Users/MENGTAO/...` 硬编码路径，属历史快照，不做环境变量化改造。
