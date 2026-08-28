# -*- coding: utf-8 -*-
"""修复 BOM 损坏脚本：剥离文件内所有 U+FEFF 字符。

背景：部分 run_wave*.py 首行 `import os` 被插到 shebang 之前，
导致原本属于 shebang 行首的 BOM 卡在第 2 行中间，Python 无法解析。

安全约束（遵循项目纪律）：
- 只用 Python open(encoding='utf-8')，绝不用 PowerShell Get/Set-Content（GBK 会破坏 CJK）
- newline='' 保留原始换行符（CRLF），不做隐式转换
- 动手前 .bak 备份
- 逐文件校验：修复前后 CJK 字符数必须一致（防 mojibake）
"""
import os
import sys
import ast

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 16 个真实波次脚本（8 个 _tmp_ 已按用户确认删除）
TARGETS = [
    "tracking/EUR/scripts/run_wave19_aea.py",
    "tracking/EUR/scripts/run_wave21_starmine.py",
    "tracking/EUR/scripts/run_wave22_arh.py",
    "tracking/EUR/scripts/run_wave23_ac.py",
    "tracking/EUR/scripts/run_wave24_ipv.py",
    "tracking/EUR/scripts/run_wave25_fhp.py",
    "tracking/EUR/scripts/run_wave26_m238.py",
    "tracking/EUR/scripts/run_wave27_acq.py",
    "tracking/EUR/scripts/run_wave28_inst6.py",
    "tracking/EUR/scripts/run_wave29_m354.py",
    "tracking/EUR/scripts/run_wave30_news54.py",
    "tracking/EUR/scripts/run_wave4_uni_probe.py",
    "tracking/EUR/scripts/run_wave5_pspat_probe.py",
    "tracking/EUR/scripts/run_wave6_fcfmix_probe.py",
    "tracking/EUR/scripts/run_wave6b_fcfmix_probe.py",
    "tracking/HKG/scripts/run_wave2_nsnlp_ts.py",
]

BOM = "\ufeff"


def cjk_count(s):
    """统计 CJK 字符数，用于校验修复未破坏中文"""
    return sum(1 for ch in s if "\u4e00" <= ch <= "\u9fff")


def main():
    fixed, skipped, failed = [], [], []

    for rel in TARGETS:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            skipped.append((rel, "文件不存在"))
            continue

        # 读取（保留原始换行符）
        with open(path, encoding="utf-8", newline="") as f:
            before = f.read()

        if BOM not in before:
            skipped.append((rel, "无 BOM，跳过"))
            continue

        n_bom = before.count(BOM)
        cjk_before = cjk_count(before)

        # 备份
        bak = path + ".bak_bom"
        with open(bak, "w", encoding="utf-8", newline="") as f:
            f.write(before)

        # 剥离 BOM
        after = before.replace(BOM, "")

        # 校验：CJK 数量必须一致（防编码破坏）
        if cjk_count(after) != cjk_before:
            failed.append((rel, f"CJK 数量变化 {cjk_before} -> {cjk_count(after)}，已回滚"))
            os.remove(bak)
            continue

        # 校验：修复后必须能解析
        try:
            ast.parse(after)
        except SyntaxError as e:
            failed.append((rel, f"修复后仍语法错误 line {e.lineno}: {e.msg}"))
            os.remove(bak)
            continue

        # 写回
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(after)

        fixed.append((rel, n_bom, cjk_before))

    # ---- 输出 ----
    print(f"修复成功: {len(fixed)} 个")
    for rel, n, cjk in fixed:
        print(f"  OK  {rel}  (移除 {n} 个 BOM, CJK {cjk} 字符完好)")

    if skipped:
        print(f"\n跳过: {len(skipped)} 个")
        for rel, why in skipped:
            print(f"  --  {rel}: {why}")

    if failed:
        print(f"\n失败: {len(failed)} 个")
        for rel, why in failed:
            print(f"  XX  {rel}: {why}")

    print(f"\n备份位置: 各文件同目录下 *.bak_bom")


if __name__ == "__main__":
    main()
