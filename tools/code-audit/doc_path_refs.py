#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""doc_path_refs — 活文档里引用的仓库内路径必须真实可达（2026-10-06 新增，P3）。

为什么要有这个工具
------------------
本仓库发生过一类反复事故：**源码/文档从未入库，只以工作区未跟踪文件存在**，
被 `git clean -fd` 清掉后无法从 git 恢复（`tools/` 曾一次丢 17 个脚本，
`docs/experience/02_signal_patterns.md` 丢过 332 行）。事后复盘时最直接的
人工痕迹就是：**AGENTS.md / skills 文档里写着某个路径，而该路径根本不存在**。

另一个同样致命的形态是"文档写了、目录不存在"——会直接误导下一个动手的 Agent
（它照着文档去跑一个不存在的测试，或去改一个不存在的脚本）。

所以本工具把「文档 → 仓库内路径」这条引用边变成可机检的断言：

  - **BROKEN**    ：活文档引用了它，但 git 未跟踪**且**磁盘不存在 → 文档腐烂 / 又一批丢失件
  - **UNTRACKED** ：活文档引用了它，磁盘存在，但 git 未跟踪 → 事故前兆（下次 clean 就没）

与 `repo_governance_check.py` 的分界
------------------------------------
`repo_governance_check.py` 看**工作区**（未跟踪源码总数 = 事故先行指标，与文档无关）；
本工具看**文档→路径的引用边**。前者回答"树里有没有未入库的东西"，
后者回答"文档承诺的东西还在不在"。两者互补，都挂 pre-commit。

棘轮（ratchet）语义
-------------------
存量违规**不阻断**（历史报告/区域运行时目录天然有大量此类引用），
基线记录在 `tests/fixtures/doc_path_refs_baseline.json`；
**只对新增违规 FAIL**。修好一条不会自动放行新的，也不会因为别人加了新文档而互相干扰。
更新基线用 `--update-baseline`（应当只在"确认这些违规合理"时才跑）。

**只有 BROKEN 阻断，UNTRACKED 仅告警**，理由：
① 「文件在磁盘但不在 git」这条信号由 `repo_governance_check.py` 专职负责（pre-commit 告警位），
   在这里重复成硬闸只会双重维护；
② `git commit <pathspec>` 的**部分提交**会用临时索引跑钩子，此时"准备放进下一个提交"的文件
   在本工具眼里就是未跟踪 —— 硬闸会给出假阳性并卡住合理提交。

按设计不入库的根（BOOT_NOT_TRACKED）
-------------------------------------
这些目录**本来就不该被 git 跟踪**（运行期产物 / 外部数据 / 归档），
文档引用它们是正常行为，故整体豁免，不参与判定：

  data/ logs/ cache/ results/ research-data/ extensions/ selfcorr_quick_out/ attic/
  .workbuddy/ .qoder-cn/ .trae-cn/ .claude/ .cursor/

用法
----
    python tools/code-audit/doc_path_refs.py                  # 闸：有新增违规则 exit 1
    python tools/code-audit/doc_path_refs.py --report         # 只打印当前全部违规（不判 exit）
    python tools/code-audit/doc_path_refs.py --update-baseline # 重写基线
    python tools/code-audit/doc_path_refs.py --json           # 机器可读
    python tools/code-audit/doc_path_refs.py --include-history # 连历史报告一起看（诊断用）

退出码：0 = 干净（或只有 UNTRACKED 告警）/ 1 = 有**新增 BROKEN** / 2 = 工具自身故障
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path。向上探测双标记，**与文件层数无关**
    （AGENTS.md §8：禁止新增 `parents[N]` / `dirname(dirname())` 这类层数硬编码）。
    必须先于 `import wqb.*`，故只能内联，不能借 `wqb.paths` 自己。
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()

from wqb.paths import find_repo_root  # noqa: E402

REPO = find_repo_root(__file__)
BASELINE = REPO / "tests" / "fixtures" / "doc_path_refs_baseline.json"

#: 活文档 = 在读、在指导行动的文档。历史报告(reports/、output_report/)与
#: 计划(docs/plans/)不参与判定：它们记录的是"当时的树"，路径过期属正常。
LIVE_EXACT = {"AGENTS.md", "README.md", "CLAUDE.md", "tools/README.md"}
LIVE_PREFIX = ("docs/", "Claude/skills/")
NOT_LIVE_PREFIX = ("docs/plans/",)

#: 按设计不入库的根：文档引用它们属正常，整体豁免
BOOT_NOT_TRACKED = (
    "data/", "logs/", "cache/", "results/", "research-data/", "extensions/",
    "selfcorr_quick_out/", "attic/",
    ".workbuddy/", ".qoder-cn/", ".trae-cn/", ".claude/", ".cursor/",
)

BACKTICK = re.compile(r"`([^`\n]{3,200})`")
MDLINK = re.compile(r"\]\(([^)\n]{3,200})\)")
FENCE = re.compile(r"^\s*(```|~~~)")
LINE_SUF = re.compile(r":\d+(-\d+)?(,\d+(-\d+)?)*$")
SYM_SUF = re.compile(r"::.*$")
#: 出现在反引号里但显然不是路径的东西：通配/占位/模板名/带空格的散文
BADCHARS = set('*<>{}|^$\\"\'`[]~ ')
TEMPLATE_WORDS = ("YYYY", "NN_", "XXXX", "<", ">")

#: 已知"文件型"扩展名。用于剥掉 `foo/config.json.ghost_ops` 这类
#: **「文件 + 其中某个键」**的引用尾巴 —— `.ghost_ops` 是 JSON 里的键名，
#: 不是路径的一部分；不剥掉的话真实存在的文件会被判成 BROKEN（假阳性）。
#: 用**前瞻**匹配"扩展名 + 点 + 标识符(至行尾)"，再截到扩展名末位。
KNOWN_EXTS = (
    "py", "pyi", "md", "json", "jsonl", "sql", "yaml", "yml", "toml", "ini", "cfg",
    "sh", "ps1", "bat", "js", "mjs", "cjs", "ts", "tsx", "txt", "csv", "lock",
)
EXT_THEN_KEY = re.compile(r"\.(" + "|".join(KNOWN_EXTS) + r")(?=\.[A-Za-z_]\w*$)")

#: MCP JSON-RPC 方法名：长得像路径（`tools/list`）、也命中顶层目录 `tools`，
#: 但它是协议方法名，**不是文件**。不豁免就永远是假阳性。
PROTOCOL_TOKENS = {
    "tools/list", "tools/call", "tools/get",
    "prompts/list", "prompts/get",
    "resources/list", "resources/read", "resources/templates/list",
    "notifications/initialized", "notifications/cancelled",
}

#: 与 `tools/skill_lint.py` 的 path-token 检查**同口径**的豁免标记。
#: 文档里写明「不存在 / 已归档 / 旧文」的路径是**有意提及**（用于记录已下架事实），
#: 不是死指针。不认这个豁免，闸就会把正确的文档判成违规——两边口径必须一致。
EXEMPT_MARK = "lint:counterexample"
NONEXIST = re.compile(
    r"不存在|从未存在|已归档|已删除|已删|旧文|旧稿|not exist|已移除|已迁|已下架|已废弃|已废止|已停止"
    r"|未生成|还没生成|丢了|丢失|已丢|已停用|停用",
    re.I,
)


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(REPO), capture_output=True, text=True)


def strip_fences(text: str) -> str:
    """剥掉 fenced code block：里面的路径多为示例/配方，不是引用。"""
    out, infence = [], False
    for ln in text.split("\n"):
        if FENCE.match(ln):
            infence = not infence
            continue
        if not infence:
            out.append(ln)
    return "\n".join(out)


def normalize(token: str) -> str | None:
    """把反引号/链接里的 token 归一成仓库相对路径；不像路径就返回 None。"""
    t = token.strip()
    if t.startswith("<") and t.endswith(">"):
        return None
    t = t.split("#", 1)[0].split("?", 1)[0]
    t = SYM_SUF.sub("", t)
    t = LINE_SUF.sub("", t)
    t = t.replace("\\", "/").strip()
    m = EXT_THEN_KEY.search(t)
    if m:
        t = t[: m.end(1)]  # `a/config.json.ghost_ops` -> `a/config.json`
    while t.startswith("./"):
        t = t[2:]
    for ell in ("…", "..."):
        if ell in t:
            if t.endswith(ell):
                t = t[: -len(ell)]
            else:
                return None
    t = t.rstrip("/")
    if not t or t.startswith("../") or t.startswith("/"):
        return None
    if "://" in t or t.startswith("mailto:"):
        return None
    if any(c in t for c in BADCHARS):
        return None
    if any(w in t for w in TEMPLATE_WORDS):
        return None
    if t in PROTOCOL_TOKENS:  # `tools/list` —— MCP 方法名，不是文件
        return None
    return t or None


def is_live(doc: str) -> bool:
    if doc.startswith(NOT_LIVE_PREFIX):
        return False
    return doc in LIVE_EXACT or doc.startswith(LIVE_PREFIX)


def is_boot(doc: str) -> bool:
    return doc.startswith(BOOT_NOT_TRACKED)


def collect(tracked: set[str], include_history: bool) -> dict[str, set[str]]:
    """返回 ref -> 引用它的文档集合（仅活文档，除非 include_history）。

    逐行扫描（不用全文正则）是为了能看**行内语境**：
    写明「不存在 / 已归档 / 旧文」的行是有意提及，必须豁免（同 skill_lint 口径）。
    """
    top = {p.split("/", 1)[0] for p in tracked if "/" in p}
    for entry in os.listdir(REPO):
        if (REPO / entry).is_dir() and entry != ".git":
            top.add(entry)

    refs: dict[str, set[str]] = defaultdict(set)
    for md in sorted(tracked):
        if not md.endswith(".md"):
            continue
        if os.path.basename(md) == "CHANGELOG.md":
            continue  # 变更日志记的是当时事实，路径过期属正常（同 skill_lint 口径）
        if not include_history and not is_live(md):
            continue
        path = REPO / md
        if not path.exists():
            continue
        try:
            lines = strip_fences(path.read_text(encoding="utf-8", errors="replace")).split("\n")
        except OSError:
            continue
        for i, ln in enumerate(lines):
            if NONEXIST.search(ln) or EXEMPT_MARK in ln:
                continue
            if i and EXEMPT_MARK in lines[i - 1]:
                continue
            for rx in (BACKTICK, MDLINK):
                for m in rx.finditer(ln):
                    t = normalize(m.group(1))
                    if not t or "/" not in t:
                        continue
                    if t.split("/", 1)[0] not in top:
                        continue
                    refs[t].add(md)
    return refs


def _ignored_set() -> set[str]:
    """一次取全：按 .gitignore（含嵌套）被忽略且未跟踪的文件路径。

    对这类路径「未被跟踪」是**预期行为**（`.env`、`.venv/`、`data/` 等），
    文档引用它们没问题，必须豁免，否则闸只会淹没在噪声里。

    为什么不用 `git check-ignore --stdin` 批喂：实测 Git for Windows 上该模式
    结果不稳定（同一批路径加不加末尾换行，命中集合都会变），不能作为闸的依据。
    `ls-files --others --ignored` 是确定性的一次枚举，且天然覆盖嵌套 .gitignore。
    """
    r = subprocess.run(
        ["git", "ls-files", "--others", "--ignored", "--exclude-standard", "-z"],
        cwd=str(REPO), capture_output=True, text=True,
    )
    return {p for p in r.stdout.split("\0") if p}


def classify(refs: dict[str, set[str]], tracked: set[str]) -> tuple[dict, dict]:
    """拆分 BROKEN / UNTRACKED。

    三条纪律（都是踩过的坑）：
      1. **先判是否已跟踪**：无扩展名的文件名（`pre-commit`/`Makefile`）会被
         「末段无点 ⇒ 目录」的启发式误判，必须让 git 索引说了算。
      2. **目录引用单独处理**：git 从不跟踪目录，用磁盘存在性判断即可，
         绝不能因为「不在 git 索引里」就当成未入库源文件。
      3. **gitignored 一律豁免**：那是按设计不入库，不是丢失。
    """
    broken, untracked = {}, {}
    ignored = _ignored_set()

    def is_ignored(t: str) -> bool:
        return t in ignored or any(p.startswith(t + "/") for p in ignored)

    for t, docs in sorted(refs.items()):
        if is_boot(t) or t in tracked or is_ignored(t):
            continue
        last = t.rsplit("/", 1)[-1]
        if "." not in last:  # 形如 `tools/foo` —— 当目录引用处理
            if (REPO / t).is_dir() or any(p.startswith(t + "/") for p in tracked):
                continue
            broken[t] = sorted(docs)
            continue
        if (REPO / t).exists():
            untracked[t] = sorted(docs)
        else:
            broken[t] = sorted(docs)
    return broken, untracked


def load_baseline() -> set[str]:
    if not BASELINE.exists():
        return set()
    try:
        data = json.loads(BASELINE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    got = set(data.get("violations") or [])
    got |= set(data.get("untracked") or [])
    return got


#: 剩余存量违规的三类合理成因（2026-10-06 逐条复核后写入基线，避免它变成"没人知道为什么留着"的债）。
#: 不带仓库路径 token（否则本文件自身会被本闸判违规）。
TRIAGE_NOTE = (
    "剩余条目全部属于「**有意缺席**」，逐条复核于 2026-10-06，共三类："
    "① docs/design/ 下的**计划 / 设计稿**引用尚未落地的模块（如 modeb_* 一族、corr_screen 节点、"
    "family_key 工具、某个尚未编写的测试）——这类文档描述的是「将要建什么」，不是「现在有什么」，"
    "与 docs/plans/ 同性质；"
    "② **未初始化区域 TWN 的模板路径**（tracking/TWN/**）——开区前按设计就不存在，"
    "相关 SKILL 已写明「本区没有战役目录、开波前先补」；"
    "③ **运行期按需生成的目录**（tracking/runs、tracking/taxonomies）——首次跑对应流程才出现。"
    "处置纪律：这些**不阻断提交**，但也不要「顺手清掉」——清掉会把「计划中」误表达成「已放弃」。"
    "要收紧基线，先在对应的设计文档里给这些路径加上「尚未落地」的说明（本工具认同行/上一行的豁免标记）。"
)


def write_baseline(violations: list[str], untracked: list[str], n_docs: int) -> None:
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_doc": (
            "doc_path_refs.py 的棘轮基线（2026-10-06 P3）。此处列出的路径是"
            "『活文档引用但当前不可达』的**存量**违规：不阻断提交，但不得新增。"
            "修好一条请重跑 --update-baseline 收紧；只在确认违规合理时才手工放宽。"
        ),
        "_triage": TRIAGE_NOTE,
        "_generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_live_docs_checked": n_docs,
        "violations": sorted(violations),
        "untracked": sorted(untracked),
    }
    tmp = BASELINE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, BASELINE)


def main() -> int:
    ap = argparse.ArgumentParser(description="活文档内仓库路径引用核验（棘轮）")
    ap.add_argument("--report", action="store_true", help="只打印，不按基线判 exit")
    ap.add_argument("--update-baseline", action="store_true", help="重写棘轮基线")
    ap.add_argument("--include-history", action="store_true", help="连历史报告一起看（诊断）")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    args = ap.parse_args()

    try:
        tracked = {p for p in _git("ls-files", "-z").stdout.split("\0") if p}
    except OSError as e:  # pragma: no cover
        print(f"[doc_path_refs] git 不可用：{e}", file=sys.stderr)
        return 2
    if not tracked:
        print("[doc_path_refs] 未取到 git 索引（不在工作区？）", file=sys.stderr)
        return 2

    refs = collect(tracked, args.include_history)
    broken, untracked = classify(refs, tracked)
    live_docs = sum(1 for p in tracked if p.endswith(".md") and is_live(p))

    baseline = load_baseline()
    new_broken = sorted(set(broken) - baseline)
    new_untracked = sorted(set(untracked) - baseline)

    if args.update_baseline:
        write_baseline(sorted(broken), sorted(untracked), live_docs)
        print(f"[doc_path_refs] 基线已写入 {BASELINE.relative_to(REPO)}"
              f"（BROKEN {len(broken)} / UNTRACKED {len(untracked)}）")
        return 0

    if args.json:
        print(json.dumps({
            "live_docs": live_docs,
            "broken": broken, "untracked": untracked,
            "new_broken": new_broken, "new_untracked": new_untracked,
            "baseline": sorted(baseline),
        }, ensure_ascii=False, indent=1))
        return 0

    print(f"[doc_path_refs] 活文档 {live_docs} 篇 ｜ 候选引用 {len(refs)} 条")
    print(f"  BROKEN {len(broken)}（基线 {len(baseline & set(broken))}）"
          f" ｜ UNTRACKED {len(untracked)}")

    # ★ 只有 BROKEN 阻断。UNTRACKED 只告警，理由有二：
    #   ① 「文件在磁盘但不在 git」这条信号由 repo_governance_check.py 专职负责（pre-commit 告警位），
    #      在此重复成硬闸只会双重维护；
    #   ② `git commit <pathspec>` 的**部分提交**会用临时索引（GIT_INDEX_FILE）跑钩子，
    #      此时"准备放到下一个提交"的文件在本钩子眼里就是未跟踪 —— 硬闸会给出**假阳性**并卡住提交。
    if new_broken:
        print("\n❌ 新增违规：活文档引用了不可达路径 —— 修掉，或显式 --update-baseline：")
        for t in new_broken:
            print(f"  [BROKEN ] {t}\n            <- {', '.join(broken[t][:4])}")
    else:
        print("\n✅ 无新增死指针")
    if new_untracked:
        print(f"\n⚠ 以下 {len(new_untracked)} 条是「活文档引用了未入库文件」（不阻断；"
              f"同口径见 `repo_governance_check.py`）：")
        for t in new_untracked:
            print(f"  [UNTRACK] {t}\n            <- {', '.join(untracked[t][:4])}")

    if args.report:
        print(f"\n—— 当前全部 BROKEN（含存量 {len(broken)} 条）——")
        for t in sorted(broken):
            print(f"  {t}  <- {', '.join(broken[t][:3])}")
        print(f"\n—— 当前全部 UNTRACKED（{len(untracked)} 条）——")
        for t in sorted(untracked):
            print(f"  {t}  <- {', '.join(untracked[t][:3])}")
        return 0

    return 1 if new_broken else 0


if __name__ == "__main__":
    sys.exit(main())
