# attic/tmp_scripts_20261004 — 一次性排障/探针脚本归档（AGENTS.md §7「归档而非删除」）

## 本批（2026-10-04 结构审计归档，11 个）

`tools/tmp_*.py`：2026-10-04 12:34–13:01 生成的临时排障脚本，**全部零引用**
（3522 个受控文本文件全库扫描确认无任何 import / 文档路径引用 / 子进程调用）。
其中 9 个含本机硬编码盘符（`D:\` / `C:\`），本来就不满足 S4 可移植性要求。

| 文件 | 大小 | 说明 |
|---|---|---|
| `tmp_a16n_neut.py` | 1.4 KB | 中性化探针 |
| `tmp_a2y.py` | 0.7 KB | 2Y 相关查询 |
| `tmp_alphadetail.py` | 0.8 KB | alpha 详情抓取 |
| `tmp_checks_raw.py` | 0.8 KB | 闸检查原始输出 |
| `tmp_corr.py` / `tmp_corr2.py` / `tmp_corr3.py` | 1.1/1.5/0.8 KB | 相关性查询三版 |
| `tmp_inflight.py` | 0.8 KB | 在飞任务查询 |
| `tmp_preflight.py` | 1.7 KB | preflight 探针 |
| `tmp_wave_ckpt.py` | 0.8 KB | checkpoint 探查 |
| `tmp_wave_full.py` | 0.5 KB | 全波次探查 |

归档原因：会话已结束（用户 2026-10-04 确认不再有并行会话），脚本零引用且带本机盘符。
留着会持续触发 `audit_structure` 的 S4（硬编码路径）与 S11（顶层冻结），
阻塞 pre-commit。

## 前批（同目录，6 个）

`tmp_eur_deadends.py` / `tmp_eur_deadpayload.py` / `tmp_eur_hist.py` /
`tmp_eur_rank.py` / `tmp_eur_rank2.py` / `tmp_eur_white.py`

## 恢复方式

本目录只读、不参与任何运行路径。若需回取：直接复制回 `tools/` 顶层，
并按硬编码盘符改成相对仓库根的推导（`Path(__file__).resolve().parents[1]`），
否则会再次触发 S4。
