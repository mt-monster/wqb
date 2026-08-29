"""BRAIN Labs 工具 (labs 脚本发射/结果回传) — MCP 工具层 (2026-08-13 自 main.py 按域拆分)。"""
import json, os, re
from typing import Dict, List, Any
from pathlib import Path

from mcp_core import mcp, load_config

@mcp.tool()

async def authenticate_brainlabs() -> Dict[str, Any]:
    """
    Sign in to BRAIN Labs and return the live AWS WorkSpaces deepLink session URL.

    BRAIN Labs is delivered as an AWS WorkSpaces Web pixel-stream, so it cannot be
    code-driven headlessly; this tool performs the two-step sign-in (platform +
    Labs password) via Playwright and hands back the WorkSpaces URL to open, plus
    the decoded internal labs URL/token. Serialized through a single-concurrency
    lock (LABS_MAX_CONCURRENCY, default 1) because a Labs account has exactly one
    interactive session.

    Returns:
        {status, workspaces_url, labs_url, token, note} or {error}.
    """
    try:
        config = load_config()
        credentials = config.get("credentials", {})
        email = credentials.get("email")
        password = credentials.get("password")
        if not email or not password:
            return {"error": "No BRAIN credentials configured (CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD)."}
        return await labs_client.open_labs_session(email, password)
    except Exception as e:
        return {"error": f"BRAIN Labs sign-in failed: {str(e)}"}

@mcp.tool()

async def emit_labs_script(
    dataset_id: str,
    fields: List[str],
    region: str = "USA",
    universe: str = "TOP3000",
    delay: int = 1,
    labs_output: str = "/tmp/labs_data_analysis_result.json",
) -> Dict[str, Any]:
    """
    Generate the pasteable BRAIN Labs data-analysis script for a dataset's MATRIX fields.

    Raw panel data is only available inside Labs (`from brain import Brain`), so the
    emitted script must be run in the Labs JupyterLab. Requires the LABS_AGENT_SCRIPT
    env var to point at labs_data_analysis_agent.py. Serialized by the Labs lock.

    Args:
        dataset_id: Dataset id to analyze.
        fields: MATRIX field ids (at most two for downstream Python alpha design).
        region/universe/delay: Simulation target context.
        labs_output: Path the in-Labs script writes its JSON result to.
    """
    try:
        return await labs_client.emit_labs_script(
            dataset_id=dataset_id,
            fields=fields,
            region=region,
            universe=universe,
            delay=delay,
            labs_output=labs_output,
        )
    except Exception as e:
        return {"error": f"emit_labs_script failed: {str(e)}"}

@mcp.tool()

async def ingest_labs_result(result_json: str) -> Dict[str, Any]:
    """
    Parse a BRAIN Labs data-analysis result (a JSON string or a file path) and return it.

    Use after running the emit_labs_script output inside Labs. Serialized by the Labs lock.
    """
    try:
        return await labs_client.ingest_labs_result(result_json)
    except Exception as e:
        return {"error": f"ingest_labs_result failed: {str(e)}"}
