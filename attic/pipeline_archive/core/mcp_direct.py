# -*- coding: utf-8 -*-
"""pipeline/core/mcp_direct.py - 直接 import 的 MCP 客户端

通过直接 import wqb-mcp 的 brain_api 模块，实现无需启动额外服务的 MCP 调用。
这是最快落地的方案，适合 pipeline 集成。

注意：
1. 需要 world-quant-brain-mcp/.env 凭据文件
2. 需要安装 wqb-mcp 的依赖（requests/pandas/pydantic 等）
3. 与 Qoder 客户端的 stdio 模式互不干扰
"""
import os
import sys
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional

# 添加 MCP 目录到路径
MCP_DIR = Path(__file__).resolve().parent.parent.parent / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP_DIR))

# 检查依赖
try:
    from brain_api import brain_client, SimulationSettings, SimulationData
    MCP_DIRECT_AVAILABLE = True
except ImportError as e:
    print(f"[WARN] 无法导入 brain_api: {e}")
    print(f"[WARN] 请确保已安装 wqb-mcp 依赖: pip install -r {MCP_DIR}/requirements.txt")
    MCP_DIRECT_AVAILABLE = False


class DirectMCPClient:
    """直接 import 的 MCP 客户端"""
    
    def __init__(self):
        if not MCP_DIRECT_AVAILABLE:
            raise RuntimeError("brain_api 不可用，请检查依赖安装")
        self.client = brain_client
    
    async def _ensure_auth(self):
        """确保已认证"""
        await self.client.ensure_authenticated()
    
    def create_multi_simulation(
        self,
        expressions: List[str],
        region: str = "GBR",
        universe: str = "TOP700",
        delay: int = 1,
        decay: int = 4,
        neutralization: str = "SUBINDUSTRY",
        truncation: float = 0.08,
        max_trade: str = "ON",
        validate_fields: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """创建批量模拟（同步包装）"""
        return asyncio.run(self._create_multi_simulation_async(
            expressions, region, universe, delay, decay,
            neutralization, truncation, max_trade, validate_fields, **kwargs
        ))
    
    async def _create_multi_simulation_async(
        self,
        expressions: List[str],
        region: str,
        universe: str,
        delay: int,
        decay: int,
        neutralization: str,
        truncation: float,
        max_trade: str,
        validate_fields: bool,
        **kwargs
    ) -> Dict[str, Any]:
        """创建批量模拟（异步实现）"""
        await self._ensure_auth()
        
        # 构建设置
        settings = SimulationSettings(
            region=region,
            universe=universe,
            delay=delay,
            decay=decay,
            neutralization=neutralization,
            truncation=truncation,
            maxTrade=max_trade,
            pasteurization="ON",
            unitHandling="VERIFY",
            nanHandling="ON",
            language="FASTEXPR",
            visualization=False
        )
        
        # 构建模拟数据列表
        simulations = []
        for expr in expressions:
            sim_data = SimulationData(
                type="REGULAR",
                settings=settings,
                regular=expr
            )
            simulations.append(sim_data)
        
        # 调用批量创建
        # 注意：brain_api.py 中没有直接的 create_multi_simulation
        # 需要调用底层的 API 端点
        # 这里使用单发模式循环创建（或找到批量端点）
        
        results = []
        for sim_data in simulations:
            try:
                result = await self.client.create_simulation(sim_data)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e), "expression": sim_data.regular})
        
        return {
            "status": "submitted",
            "count": len(results),
            "results": results,
            "note": "使用直接 import 模式，实际为单发循环"
        }
    
    def get_simulation_status(self, location: str) -> Dict[str, Any]:
        """查询模拟状态"""
        return asyncio.run(self._get_simulation_status_async(location))
    
    async def _get_simulation_status_async(self, location: str) -> Dict[str, Any]:
        """查询模拟状态（异步）"""
        await self._ensure_auth()
        # 调用 brain_client 的查询方法
        # 需要根据 brain_api.py 的实际接口调整
        return {"status": "PENDING", "location": location}
    
    def get_alpha_details(self, alpha_id: str) -> Dict[str, Any]:
        """获取 alpha 详情"""
        return asyncio.run(self._get_alpha_details_async(alpha_id))
    
    async def _get_alpha_details_async(self, alpha_id: str) -> Dict[str, Any]:
        """获取 alpha 详情（异步）"""
        await self._ensure_auth()
        # 调用 brain_client 的查询方法
        return {"alpha_id": alpha_id, "status": "mock"}


# 全局客户端实例
_client: Optional[DirectMCPClient] = None


def get_direct_client() -> DirectMCPClient:
    """获取直接 import 的 MCP 客户端（单例）"""
    global _client
    if _client is None:
        _client = DirectMCPClient()
    return _client


def is_available() -> bool:
    """检查直接 import 模式是否可用"""
    return MCP_DIRECT_AVAILABLE
