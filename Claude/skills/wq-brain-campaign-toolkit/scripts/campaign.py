# -*- coding: utf-8 -*-
"""campaign.py - 战役工具包统一入口：子命令分发到各能力脚本。

用法:
  python campaign.py --campaign-dir <DIR> <子命令> [子命令参数...]

子命令:
  scan-fields   -> scan_fields.py   （typed catalog 字段扫描）
  score         -> score_datasets.py（数据集评分/探针计划/三灯评分）
  gate          -> gate.py          （5 闸预检）
  build-wave    -> build_wave.py    （选波）
  assemble-priors -> assemble_priors.py （从 DB KB 确定性组装 GEM priors 文件）
  pipeline      -> pipeline.py      （端到端编排 + quota）
  review        -> review_wave.py   （walls 诊断）
  metrics       -> metrics_cache.py （指标读穿缓存）
  diversity     -> diversity_audit.py（多样性审计）
  diversity-extract -> diversity_extract.py（单数据集多样性榨取）
  s2-mark       -> s2_compliance_mark.py（S2 合规标记：特征工程文档记录）
  ledger        -> _lib/ledger.py   （台账统一 CLI）
  registry      -\u003e _lib/registry.py （registry 实证层统一 CLI：dead_end/win/campaign/orphan）
  wave          -\u003e _lib/wave_results.py（wave_results 台账统一 CLI：upsert/import/get/list）

`campaign.py --campaign-dir <DIR> gate ...` 等价 `gate.py --campaign-dir <DIR> ...`。
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SUBCOMMANDS = {
    "scan-fields": "scan_fields",
    "score": "score_datasets",
    "gate": "gate",
    "build-wave": "build_wave",
    "assemble-priors": "assemble_priors",
    "pipeline": "pipeline",
    "review": "review_wave",
    "metrics": "metrics_cache",
    "diversity": "diversity_audit",
    "diversity-extract": "diversity_extract",
    "s2-mark": "s2_compliance_mark",
}


def main():
    argv = sys.argv[1:]
    # 提取全局 --campaign-dir（位置任意），其余参数透传给子命令
    cdir = None
    rest = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--campaign-dir" and i + 1 < len(argv):
            cdir = argv[i + 1]
            i += 2
        elif a.startswith("--campaign-dir="):
            cdir = a.split("=", 1)[1]
            i += 1
        else:
            rest.append(a)
            i += 1
    if not rest or rest[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if rest else 1)
    cmd, sub_argv = rest[0], rest[1:]

    from _lib.common import CampaignContext
    ctx = CampaignContext(cdir)

    if cmd == "ledger":
        from _lib.ledger import cli_main
        sys.exit(cli_main(ctx, sub_argv))
    if cmd == "registry":
        from _lib.registry import cli_main
        sys.exit(cli_main(ctx, sub_argv))
    if cmd == "wave":
        from _lib.wave_results import cli_main
        sys.exit(cli_main(ctx, sub_argv))
    mod_name = SUBCOMMANDS.get(cmd)
    if not mod_name:
        print(f"未知子命令: {cmd}\n可用: {sorted(SUBCOMMANDS) + ['ledger', 'registry', 'wave']}", file=sys.stderr)
        sys.exit(1)
    sys.argv = [mod_name + ".py", "--campaign-dir", ctx.dir] + sub_argv
    m = importlib.import_module(mod_name)
    m.main()


if __name__ == "__main__":
    main()
