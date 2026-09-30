# -*- coding: utf-8 -*-
"""晚绑定的协作者解析（保住拆分前 `monkeypatch.setattr(wave_gate, ...)` 的测试契约）。

## 为什么需要本模块（2026-09-30 包化时踩到的坑）

拆分前所有闸函数都在 `tools/wave_gate.py` 一个命名空间里，测试惯用：
    monkeypatch.setattr(wave_gate, "_campaign_store_cls", lambda *a, **k: _FakeStore)

拆分后闸函数搬进包内子模块，若直接写
    from ._paths import _campaign_store_cls
    ...
    CampaignStore = _campaign_store_cls()      # ← 模块加载期已绑定，patch 打不中
则**所有以 patch 方式注入假库的测试会静默走到真库**（本仓 4 个 PF 测试因此转红）。

修法：子模块不直接调用 `_campaign_store_cls`，而是经本模块**晚绑定**查找 ——
优先 `sys.modules["wave_gate"]`（shim，即 monkeypatch 落点），找不到才回落包内实现。
这样"patch 打哪个名字都能生效"，与拆分前语义一致。
"""
import sys


def _shim():
    """返回 shim 模块（`tools/wave_gate.py`）；未加载时 None。

    ⚠ 用 `sys.modules` 而非 import：包内导入 shim 会构成循环，
    且 shim 只在 CLI/测试入口出现，非入口场景回落包内实现即可。
    """
    return sys.modules.get("wave_gate")


def resolve(name, default):
    """晚绑定取 `name`：shim 上有则用 shim 的（monkeypatch 优先），否则用 default。"""
    mod = _shim()
    if mod is not None:
        got = getattr(mod, name, None)
        if got is not None:
            return got
    return default


def campaign_store_cls(campaign_dir=None):
    """晚绑定的 CampaignStore 工厂（等价拆分前的 `_campaign_store_cls`）。"""
    from ._paths import _campaign_store_cls as _default
    fn = resolve("_campaign_store_cls", _default)
    return fn(campaign_dir)


def wqb_db_path(campaign_dir=None):
    """晚绑定的库路径（等价拆分前的 `_wqb_db_path`）。"""
    from ._paths import _wqb_db_path as _default
    fn = resolve("_wqb_db_path", _default)
    return fn(campaign_dir)


def wqb_root(campaign_dir=None):
    """晚绑定工作区根（等价拆分前的 `_wqb_root`）。"""
    from ._paths import _wqb_root as _default
    fn = resolve("_wqb_root", _default)
    return fn(campaign_dir)


def load_region_gates():
    """晚绑定 toolkit region_gates 装载器（等价拆分前的 `_load_region_gates`）。"""
    from ._paths import _load_region_gates as _default
    fn = resolve("_load_region_gates", _default)
    return fn()


def settings_region(campaign_dir):
    """晚绑定 region 兜底（等价拆分前的 `_settings_region`）。"""
    from ._paths import _settings_region as _default
    fn = resolve("_settings_region", _default)
    return fn(campaign_dir)
