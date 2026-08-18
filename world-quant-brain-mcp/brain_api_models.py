# -*- coding: utf-8 -*-
"""brain_api_models — 从 brain_api.py 拆出的纯数据模型层（2026-08-18 P3 二次拆分）。

仅含 Pydantic 模型，不依赖 BrainApiClient / 网络 / redis。抽离目的是给 4113 行
单体 brain_api.py 瘦身、建立"模型 / http / cache / client facade"分包结构的第一步，
同时保持 ``from brain_api import SimulationSettings`` 等旧导入路径可用（brain_api.py 重新导出）。

原文件 docstring 曾误称"不含 FastMCP/redis/bs4"——实际 brain_api.py 顶部确实 import 了三者，
该声明已同步更正。
"""
import re
from typing import Optional

from pydantic import BaseModel, EmailStr, model_validator


class AuthCredentials(BaseModel):
    email: EmailStr
    password: str


class SimulationSettings(BaseModel):
    instrumentType: str = "EQUITY"
    region: str = "USA"
    universe: str = "TOP3000"
    delay: int = 1
    decay: float = 0.0
    neutralization: str = "NONE"
    truncation: float = 0.0
    pasteurization: str = "ON"
    unitHandling: Optional[str] = "VERIFY"
    nanHandling: Optional[str] = "OFF"
    language: str = "FASTEXPR"
    lookback: Optional[int] = None
    visualization: bool = True
    testPeriod: str = "P0Y0M"
    selectionHandling: str = "POSITIVE"
    selectionLimit: int = 1000
    maxTrade: str = "OFF"
    componentActivation: str = "IS"


class SimulationData(BaseModel):
    type: str = "REGULAR"  # "REGULAR" or "SUPER"
    settings: SimulationSettings
    regular: Optional[str] = None
    combo: Optional[str] = None
    selection: Optional[str] = None

    @model_validator(mode="after")
    def validate_super_selection_rules(self) -> "SimulationData":
        if self.type.upper() != "SUPER":
            return self

        region = self.settings.region.upper()
        if region != "USA":
            return self

        if not self.selection:
            raise ValueError('USA SUPER simulations require selection to include (prod_correlation > 0)')

        if not re.search(r"\(\s*prod_correlation\s*>\s*0(?:\.0+)?\s*\)", self.selection):
            raise ValueError('USA SUPER simulations require selection to include (prod_correlation > 0)')

        return self
