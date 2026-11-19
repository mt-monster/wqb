# 08 — 外部论文取证：稳定通道 + 多样证硬闸（2026-11-19）

> 用户 2026-11-19 明令：① 项目中所有查论文的地方必须用**明确稳定可靠**的方式，不稳定的弃用；
> ② 证据闸不要「留痕就算过」，要「一定能查到论文」；③ **还要多样证——≥5 篇不同论文**（本轮补：≥3 不同第一作者）。

## 1. 唯一稳定通道 = `tools/research/paper_search.py`

三层冗余 + fail-closed，唯一实现（tools/README 已登记）：

| 层 | 通道 | 实测（2026-11-19 项目 venv） |
|---|---|---|
| 1 主 | **Crossref REST** `api.crossref.org/works` | 稳定 1.2s，精确命中期刊 DOI/作者/年；作者模式 `query.author` |
| 2 补 | **arXiv API** `export.arxiv.org/api/query` | 稳定 1.3s，偏物理/CS/量化预印本；纯金融词常空 |
| 3 保底 | **本地论文库** `docs/reference` + `docs/experience` + ra-pipeline references | 确定可用；已沉淀 Miller/Fama/Tetlock 等经典锚 |

**明确弃用**（实测不稳）：
- `WebSearch` — 结果被异常文本污染 / 超时（本会话多次）
- `WebFetch` — 页面 403/超时（`docs/reference/eur_paper_evidence_20261118.md` 实证）
- `Semantic Scholar API` — HTTP 429 限流（实测）
- `domain_search` — 昂贵、高延迟（KOR skill 原通道 B）

调用：
```bash
world-quant-brain-mcp/.venv/Scripts/python.exe -X utf8 tools/research/paper_search.py \
  --query "divergence of opinion short selling,post earnings announcement drift" \
  --diverse --min-papers 5 --min-authors 3 --limit 5
# diverse_ok: True | papers=15/5 authors=13/3
```

## 2. 相关性校验（防 Crossref 假阳性）

Crossref 对**任意**查询都返回"最接近"结果（查 `nonexistent xyz zzz` 返回 `ZZZ; Zzz`）。
`_relevance()` 强制校验：
- 机制查询：标题含 ≥1 个长实词(≥6) 或 ≥2 个短实词(3-5)
- 作者+年份查询（闸从 cite 抽的 `Lakonishok Lee 2001`）：走 `query.author` + 作者姓氏命中
- 本地层：必须与 query 实词重叠（不能只靠关键词表，否则任何含 momentum 的行都命中）

单篇/孤证不算通过。

## 3. 多样证判定 `verify_diverse()`

跨多个查询累积 → 按 DOI/标题归一化去重 → 统计不同第一作者数 →
`diverse_ok = (n_papers >= 5 and n_authors >= 3)`。全失败/孤证 = found=false → fail-closed。

## 4. 证据闸改造（EVID-PAPER 默认硬拦）

`Claude/skills/wq-brain-campaign-toolkit/scripts/_gate_knowledge.py::check_evidence_gate`：
- 不再只查 ledger 留痕键存在；**自己调 `verify_diverse` 实证**
- 检索词来源优先级：留痕 `papers[].cite`（作者+年份，Crossref 精确核验）> `paperPrior` > `question` 机制措辞
- **禁止用 dataset 名兜底**：`"institutions"` 这类泛词会返回同名无关论文，制造 5 篇 4 作者的假阳性（实测）
- `diverse_ok=false` → EVID-PAPER severity=fail → `gate_pass=false`
- **默认硬拦（所有 wave_gate）**，不再只在 `--require-evidence` 时生效（用户 2026-11-19 裁定）
- repair/probe 批仍自动豁免（参数变体不重查）

验证（真实平台）：
- 有 cite 留痕的 `insiders` → 10 篇/3 作者 pass
- 无留痕的 `institutions25` / 假查询 → 0 篇 fail-closed

## 5. 落点清单

- 工具：`tools/research/paper_search.py`（唯一实现）；守护 `tests/unit/09_core/test_paper_search_stable_channel.py`（8 例）
- 闸：`_gate_knowledge.py`（EVID-PAPER 实证 + 多样证）、`gate.py`（注释同步）
- 规约：`AGENTS.md` §8.11、`ra-pipeline/SKILL.md`（机制证据闸）、`forum_and_doc_tools_guide.md`、`docs/env_and_switches.md`
- Skill 通道 B：`wq-brain-ra-kor/SKILL.md`、`ra-pipeline/references/_six-step-core.md`（WebSearch/domain_search → paper_search，已 sync_skills 到 5 安装位）
- Saved workflow：`gbr-regular-alpha-mine`（v9）、`deu-unlit-tower-regular`（v4）证据员 ask 改为 `--diverse ≥5 篇/3 作者` + 留痕 papers[] ≥5 条 cite
- 验证：根 tests **4494 passed / 17 skipped**；两 workflow SaveWorkflow 编译通过
