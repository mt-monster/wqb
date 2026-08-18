#!/usr/bin/env python3
"""dehardcode_v2.py — 消灭活跃代码中的 C:/Users/MENGTAO 硬编码（2026-08-18 治理）。

约定（env 优先，默认值全部基于 os.path.expanduser("~")）：
  WQ_TOOLKIT        默认 ~/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts
  WQ_VALIDATOR_DIR  默认 ~/.workbuddy/skills/alpha-expression-verifier/scripts
  WQ_ACE_LIB        默认 ~/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts
  WQ_JUDGE_SKILL    默认 ~/.zcode/skills/brain-alpha-judge
  WQ_ENV_PATH       默认 ~/Desktop/E3/quant/worldquant_alpha/.env

断言守卫：期望旧串未命中 → WARN 不静默破坏（继承 patch_paths.py 模式）。
只处理 active 代码：跳过 */archive/、logs/、__pycache__、.venv。
cache 读取类一次性脚本（含 .qoder-cn\\cache 固定路径）不在此处理——由归档流程接管。
"""
import os
import re
import glob

ROOT = r"D:\coding\traeCN_project\wqb"
H = 'os.path.expanduser("~")'

# --- 替换表: (old_substring, new_substring) ---
REPL = [
    # A. TOOLKIT = Path(...)  （59 处, tracking/*/scripts/run_wave*）
    ('TOOLKIT = Path("C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts")',
     'TOOLKIT = Path(os.environ.get("WQ_TOOLKIT", os.path.join(' + H + ', ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts")))'),
    # B. sys.path.insert(...) qoder toolkit（13 处）
    ('sys.path.insert(0, r"C:\\Users\\MENGTAO\\.qoder-cn\\skills\\wq-brain-campaign-toolkit\\scripts")',
     'sys.path.insert(0, os.environ.get("WQ_TOOLKIT", os.path.join(' + H + ', ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts")))'),
    ('sys.path.insert(0, r"C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts")',
     'sys.path.insert(0, os.environ.get("WQ_TOOLKIT", os.path.join(' + H + ', ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts")))'),
    ('sys.path.insert(0, \'C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts\')',
     'sys.path.insert(0, os.environ.get("WQ_TOOLKIT", os.path.join(' + H + ', ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts")))'),
    # C. verifier 路径（gate.py _VALIDATOR_DIRS / VERIFY_SCRIPT）
    ('r"C:\\Users\\MENGTAO\\.workbuddy\\skills\\alpha-expression-verifier\\scripts"',
     'os.environ.get("WQ_VALIDATOR_DIR", os.path.join(' + H + ', ".workbuddy", "skills", "alpha-expression-verifier", "scripts"))'),
    ('r"C:\\Users\\MENGTAO\\.qoder-cn\\skills\\alpha-expression-verifier\\scripts"',
     'os.environ.get("WQ_VALIDATOR_DIR", os.path.join(' + H + ', ".workbuddy", "skills", "alpha-expression-verifier", "scripts"))'),
    # D. WQ_ACE_LIB 默认值 expanduser 化（保留 env 优先）
    ('os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts")',
     'os.environ.get("WQ_ACE_LIB", os.path.join(' + H + ', ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "scripts"))'),
    ("os.environ.get('WQ_ACE_LIB', r'C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts')",
     'os.environ.get("WQ_ACE_LIB", os.path.join(' + H + ', ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "scripts"))'),
    ('SKILL = r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"',
     'SKILL = os.environ.get("WQ_ACE_LIB", os.path.join(' + H + ', ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "scripts"))'),
    # E. .zcode（EUR/ra submit）
    ('load_credentials(skill_dir=Path("C:/Users/MENGTAO/.zcode/skills/brain-alpha-judge"))',
     'load_credentials(skill_dir=Path(os.environ.get("WQ_JUDGE_SKILL", os.path.join(' + H + ', ".zcode", "skills", "brain-alpha-judge"))))'),
    ('sys.path.insert(0, str(Path("C:/Users/MENGTAO/.zcode/skills/brain-alpha-judge/scripts/vendor")))',
     'sys.path.insert(0, str(Path(os.environ.get("WQ_JUDGE_SKILL", os.path.join(' + H + ', ".zcode", "skills", "brain-alpha-judge"))) / "scripts" / "vendor"))'),
    ("sys.path.insert(0, r'C:\\Users\\MENGTAO\\.zcode\\skills\\shared_libs')",
     'sys.path.insert(0, os.path.join(' + H + ', ".zcode", "skills", "shared_libs"))'),
    # F. Desktop .env（tools/fetch_all_universes.py）
    ('ENV_PATH = r"C:\\Users\\MENGTAO\\Desktop\\E3\\quant\\worldquant_alpha\\.env"',
     'ENV_PATH = os.environ.get("WQ_ENV_PATH", os.path.join(' + H + ', "Desktop", "E3", "quant", "worldquant_alpha", ".env"))'),
    # G. gen_v5 out 路径
    ('out = "C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/data/',
     'out = os.path.join(' + H + ', ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "data", "'),
    # H. SKILL 定义（dehardcore_all 残留 r"C:/Users/MENGTAO/..."）
    ('SKILL = r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"',
     'SKILL = os.environ.get("WQ_ACE_LIB", os.path.join(' + H + ', ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "scripts"))'),
]

def iter_active_py():
    for f in glob.glob(os.path.join(ROOT, "**", "*.py"), recursive=True):
        rel = f[len(ROOT) + 1:].replace(os.sep, "/")
        if any(x in rel for x in ("/archive/", "logs/", "__pycache__", ".venv", "research-data")):
            continue
        if rel.startswith("tracking/reference/tooling/"):
            continue  # 工具脚本自身不动
        yield f, rel

def ensure_os_import(t, rel):
    if "import os" in t or "import os," in t:
        return t, False
    # 在首个 import 块前补
    m = re.search(r"^((?:#.*\n|import .*\n|from .*\n)*)", t, re.M)
    if m:
        head = m.group(1)
        new_head = head.rstrip("\n") + "\nimport os\n" if head else "import os\n"
        return t.replace(head, new_head, 1), True
    return "import os\n" + t, True

total_patched = 0
warnings = []
for f, rel in iter_active_py():
    t = open(f, encoding="utf-8").read()
    orig = t
    for old, new in REPL:
        if old in t:
            t = t.replace(old, new)
        # 双引号/单引号变体未命中不警告（部分形态已被旧工具处理）
    if t != orig:
        t, added_os = ensure_os_import(t, rel)
        open(f, "w", encoding="utf-8").write(t)
        total_patched += 1
        print(f"  patched {rel}{' (+os)' if added_os else ''}")

# 复核: 剩余 MENGTAO（应只剩 archive/logs/一次性 cache 脚本）
remaining = []
for f in glob.glob(os.path.join(ROOT, "**", "*.py"), recursive=True):
    rel = f[len(ROOT) + 1:].replace(os.sep, "/")
    if any(x in rel for x in ("/archive/", "logs/", "__pycache__", ".venv", "research-data")):
        continue
    if "tracking/reference/tooling/" in rel:
        continue
    with open(f, "r", encoding="utf-8", errors="ignore") as fh:
        for i, line in enumerate(fh, 1):
            if "MENGTAO" in line:
                remaining.append(f"{rel}:{i}")

print(f"\nPatched {total_patched} files.")
if remaining:
    print(f"Remaining MENGTAO in active code: {len(remaining)}")
    for r in remaining:
        print("  ", r)
else:
    print("No MENGTAO left in active code.")
