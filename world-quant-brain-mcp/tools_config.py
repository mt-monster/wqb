"""配置管理工具 (manage_config) — MCP 工具层 (2026-08-13 自 main.py 按域拆分)。"""
import re
from typing import Dict, Optional, Any

from mcp_core import mcp, brain_client, load_config, save_config

@mcp.tool()

async def manage_config(action: str = "get", settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Manage configuration settings - get or update configuration.
    
    Args:
        action: Action to perform ("get" to retrieve config, "set" to update config)
        settings: Configuration settings to update (required when action="set")
    
    Returns:
        Current or updated configuration including authentication status
    """
    config = load_config()
    
    if action == "set" and settings:
        config.update(settings)
        save_config(config)
        
    is_authed = await brain_client.is_authenticated()
    config['isAuthenticated'] = is_authed
    
    # Mask password for security
    if 'password' in config:
        config['password'] = '********'
        
    return config

# --- Simulation Tools ---
