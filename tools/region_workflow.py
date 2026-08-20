# -*- coding: utf-8 -*-
"""分 region 流程优化脚本。

根据 region 配置包（tracking/region_config.json）优化挖掘流程：
- 数据集选择（优先 strong_datasets，weak_datasets 小步快跑）
- 字段扫描（字段名规则库/字段分组/字段类型区分）
- 表达式生成（窗口自适应/组合信号/结构重构）
- 设置调优（设置优先级/小步快跑）
"""
import json, os

WS = r"d:\coding\traeCN_project\wqb"
CONFIG_PATH = os.path.join(WS, "tracking", "region_config.json")

def load_region_config():
    """加载 region 配置包。"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_datasets(region):
    """根据 region 获取数据集列表（优先 strong_datasets，weak_datasets 小步快跑）。"""
    config = load_region_config()
    if region not in config:
        raise ValueError(f"未知 region: {region}")
    cfg = config[region]
    # 优先 strong_datasets，weak_datasets 小步快跑
    datasets = cfg["strong_datasets"] + cfg["weak_datasets"]
    probe_size = cfg["probe_size"]
    return datasets, probe_size

def get_field_rules(region, dataset):
    """根据 region + dataset 获取字段规则。"""
    config = load_region_config()
    if region not in config:
        raise ValueError(f"未知 region: {region}")
    cfg = config[region]
    # 字段名规则库
    if "field_rules" in cfg and dataset in cfg["field_rules"]:
        return cfg["field_rules"][dataset]
    # 字段分组
    if "field_groups" in cfg and dataset in cfg["field_groups"]:
        return cfg["field_groups"][dataset]
    return None

def get_window_adaptive(region, field):
    """根据 region + field 获取窗口自适应。"""
    config = load_region_config()
    if region not in config:
        raise ValueError(f"未知 region: {region}")
    cfg = config[region]
    if "window_adaptive" in cfg and field in cfg["window_adaptive"]:
        return cfg["window_adaptive"][field]
    return 20  # 默认窗口

def get_combo_signals(region):
    """根据 region 获取组合信号。"""
    config = load_region_config()
    if region not in config:
        raise ValueError(f"未知 region: {region}")
    cfg = config[region]
    if "combo_signal" in cfg:
        return cfg["combo_signal"]
    return []

def get_settings_priority(region):
    """根据 region 获取设置优先级。"""
    config = load_region_config()
    if region not in config:
        raise ValueError(f"未知 region: {region}")
    cfg = config[region]
    return cfg["settings_priority"]

def get_prod_wall(region, dataset):
    """根据 region + dataset 获取 PROD 墙。"""
    config = load_region_config()
    if region not in config:
        raise ValueError(f"未知 region: {region}")
    cfg = config[region]
    if "prod_wall" in cfg and dataset in cfg["prod_wall"]:
        return cfg["prod_wall"][dataset]
    return None

def need_structure_rebuild(region):
    """根据 region 判断是否需要结构重构。"""
    config = load_region_config()
    if region not in config:
        raise ValueError(f"未知 region: {region}")
    cfg = config[region]
    return cfg.get("structure_rebuild", False)

# 示例用法
if __name__ == "__main__":
    # GBR 示例
    print("=== GBR ===")
    datasets, probe_size = get_datasets("GBR")
    print(f"数据集: {datasets}, 探针批次: {probe_size}")
    print(f"字段规则: {get_field_rules('GBR', 'model264')}")
    print(f"窗口自适应: {get_window_adaptive('GBR', 'ep_yield_pct_smest')}")
    print(f"设置优先级: {get_settings_priority('GBR')}")
    
    # USA 示例
    print("\n=== USA ===")
    datasets, probe_size = get_datasets("USA")
    print(f"数据集: {datasets}, 探针批次: {probe_size}")
    print(f"字段分组: {get_field_rules('USA', 'ml_factor_proj')}")
    print(f"组合信号: {get_combo_signals('USA')}")
    print(f"设置优先级: {get_settings_priority('USA')}")
    
    # KOR 示例
    print("\n=== KOR ===")
    datasets, probe_size = get_datasets("KOR")
    print(f"数据集: {datasets}, 探针批次: {probe_size}")
    print(f"PROD 墙: {get_prod_wall('KOR', 'insider_feats')}")
    print(f"需要结构重构: {need_structure_rebuild('KOR')}")
    print(f"设置优先级: {get_settings_priority('KOR')}")
