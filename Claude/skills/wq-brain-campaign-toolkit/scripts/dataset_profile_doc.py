"""Toolkit dispatcher for the canonical per-dataset field-profile doc generator.

`campaign.py --campaign-dir <DIR> field-profile ...` 进入这里：

  · 推导区域：显式 `--region` 优先；否则取 campaign 目录的 `config/settings.json`
    的 `region`（toolkit 纪律：region 只从 settings.json 派生），再退回目录名；
  · 剥掉 toolkit / workflow 层参数（`--campaign-dir`、`--wave`——字段画像是区域级产物，
    不按波过滤），其余参数原样转给 `tools/fields/dataset_profile_doc.py`；
  · **缺省落盘**（S6 产物），`--dry-run` 或 `--list` 时只预览。

目标脚本是仓库级工具（`tools/fields/dataset_profile_doc.py`），本分发器只负责
「定位仓库根 + 参数适配」，渲染逻辑不在这里复制。
"""
import importlib.util
import json
import sys
from pathlib import Path

_TARGET = Path("tools") / "fields" / "dataset_profile_doc.py"


def _take(argv, flag):
    """取出 flag（含 `--flag=value` 形式）与其值，返回 (value, 剩余参数)。"""
    value, rest, i = None, [], 0
    while i < len(argv):
        arg = argv[i]
        if arg == flag and i + 1 < len(argv):
            value = argv[i + 1]
            i += 2
        elif arg.startswith(flag + "="):
            value = arg.split("=", 1)[1]
            i += 1
        else:
            rest.append(arg)
            i += 1
    return value, rest


def _find_repo(campaign_dir):
    origins = []
    if campaign_dir:
        origins.append(Path(campaign_dir).expanduser().resolve())
    origins.append(Path.cwd().resolve())
    for origin in origins:
        for root in (origin, *origin.parents):
            if (root / _TARGET).is_file():
                return root
    return None


def _region_from_settings(campaign_dir):
    """campaign 目录 `config/settings.json` 的 region（toolkit 纪律的唯一来源）。

    缺文件 / 坏 JSON / 无 region 键 ⇒ None（交调用方退回目录名）。
    """
    if not campaign_dir:
        return None
    cfg = Path(campaign_dir).expanduser() / "config" / "settings.json"
    try:
        data = json.loads(cfg.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return None
    region = str(data.get("region") or "").strip().upper()
    return region or None


def main():
    campaign_dir, argv = _take(sys.argv[1:], "--campaign-dir")
    _wave, argv = _take(argv, "--wave")          # 波号对区域级字段画像无意义；workflow 节点可能带上
    region, argv = _take(argv, "--region")
    if not region:
        region = _region_from_settings(campaign_dir)
    if not region:
        if not campaign_dir:
            raise SystemExit(
                "field-profile 需要 --campaign-dir（据此推导区域）或显式 --region")
        region = Path(campaign_dir).name.upper()

    root = _find_repo(campaign_dir)
    if root is None:
        raise RuntimeError("未找到工作区 tools/fields/dataset_profile_doc.py")

    if "--dry-run" in argv:
        argv = [arg for arg in argv if arg != "--dry-run"]
    elif "--list" not in argv and "--apply" not in argv:
        argv.append("--apply")                   # S6 默认落盘

    # 按**文件路径**加载目标模块：本分发器与目标脚本同名，若按模块名 import，
    # `campaign.py` 已把本模块注册进 sys.modules（同名），会自己 import 自己。
    spec = importlib.util.spec_from_file_location(
        "wqb_toolkit_dataset_profile_doc", root / _TARGET)
    target = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(target)
    return target.main(["--region", region] + argv)


if __name__ == "__main__":
    raise SystemExit(main())
