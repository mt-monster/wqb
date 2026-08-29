"""Alpha 查询与属性工具 — MCP 工具层 (2026-08-13 自 main.py 按域拆分)。"""
import os, re
from typing import Dict, List, Optional, Any

from mcp_core import mcp, brain_client, _slim_alpha_response, _slim_alpha_list, _slim_yearly, _slim_pnl

@mcp.tool()

async def get_alpha_details(alpha_id: str) -> Dict[str, Any]:
    """
    Get detailed information about an alpha.
    
    Args:
        alpha_id: The ID of the alpha to retrieve
    
    Returns:
        Detailed alpha information
    """
    try:
        return _slim_alpha_response(await brain_client.get_alpha_details(alpha_id))
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def get_alpha_pnl(alpha_id: str) -> Dict[str, Any]:
    """
    Get PnL (Profit and Loss) data for an alpha.
    
    Args:
        alpha_id: The ID of the alpha
    
    Returns:
        PnL data for the alpha
    """
    try:
        return _slim_pnl(await brain_client.get_alpha_pnl(alpha_id))
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def get_user_alphas(
    stage: str = "IS",
    limit: int = 30,
    offset: int = 0,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    submission_start_date: Optional[str] = None,
    submission_end_date: Optional[str] = None,
    order: Optional[str] = None,
    hidden: Optional[bool] = None,
    region: Optional[str] = None,
    status: Optional[str] = None,
    type: Optional[str] = None,
    is_super: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Get user's alphas with advanced filtering, pagination, and sorting.

    This tool retrieves a list of your alphas, allowing for detailed filtering based on stage,
    creation date, submission date, visibility, region, status, type, and super alpha flag.
    It also supports pagination and custom sorting.

    Args:
        stage (str): The stage of the alphas to retrieve.
            - "IS": In-Sample (alphas that have not been submitted).
            - "OS": Out-of-Sample (alphas that have been submitted).
            Defaults to "IS".
        limit (int): The maximum number of alphas to return in a single request.
            For example, `limit=50` will return at most 50 alphas. Defaults to 30.
        offset (int): The number of alphas to skip from the beginning of the list.
            Used for pagination. For example, `limit=50, offset=50` will retrieve alphas 51-100.
            Defaults to 0.
        start_date (Optional[str]): The earliest creation date for the alphas to be included.
            Filters for alphas created on or after this date.
            Example format: "2023-01-01T00:00:00Z".
        end_date (Optional[str]): The latest creation date for the alphas to be included.
            Filters for alphas created before this date.
            Example format: "2023-12-31T23:59:59Z".
        submission_start_date (Optional[str]): The earliest submission date for the alphas.
            Only applies to "OS" alphas. Filters for alphas submitted on or after this date.
            Example format: "2024-01-01T00:00:00Z".
        submission_end_date (Optional[str]): The latest submission date for the alphas.
            Only applies to "OS" alphas. Filters for alphas submitted before this date.
            Example format: "2024-06-30T23:59:59Z".
        order (Optional[str]): The sorting order for the returned alphas.
            Prefix with a hyphen (-) for descending order.
            Examples: "name" (sort by name ascending), "-dateSubmitted" (sort by submission date descending).
        hidden (Optional[bool]): Filter alphas based on their visibility.
            - `True`: Only return hidden alphas.
            - `False`: Only return non-hidden alphas.
            If not provided, both hidden and non-hidden alphas are returned.
        region (Optional[str]): Filter alphas by region.
            Common values: "USA", "EUR", "ASI", "GLB", etc.
            If not provided, alphas from all regions are returned.
        status (Optional[str]): Filter alphas by their OS status.
            Common values: "ACTIVE", "SUPERSEDED", "UNSUBMITTED", etc.
            If not provided, alphas with any status are returned.
        type (Optional[str]): Filter alphas by their expression type.
            Common values: "REGULAR", "SUPER", etc.
            If not provided, alphas of all types are returned.
        is_super (Optional[bool]): Filter to only super alphas (True) or non-super alphas (False).
            If not provided, both super and non-super alphas are returned.

    Returns:
        Dict[str, Any]: A dictionary containing a list of alpha details under the 'results' key,
        along with pagination information. If an error occurs, it returns a dictionary with an 'error' key.
    """
    try:
        return _slim_alpha_list(await brain_client.get_user_alphas(
            stage=stage, limit=limit, offset=offset, start_date=start_date,
            end_date=end_date, submission_start_date=submission_start_date,
            submission_end_date=submission_end_date, order=order, hidden=hidden,
            region=region, status=status, alpha_type=type, is_super=is_super,
        ))
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def get_alpha_yearly_stats(alpha_id: str) -> Dict[str, Any]:
    """Get yearly statistics for an alpha."""
    try:
        return _slim_yearly(await brain_client.get_alpha_yearly_stats(alpha_id))
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def set_alpha_properties(alpha_id: str, name: Optional[str] = None, 
                               color: Optional[str] = None, tags: Optional[List[str]] = None,
                               descriptions: str = "None",
                               selection_description: Optional[str] = None,
                               combo_description: Optional[str] = None) -> Dict[str, Any]:
    """
      Note: Update alpha properties (name, color, tags, descriptions).
      For SUPER alphas, selection_description and combo_description are also required and must
      each be at least 100 English characters.
      Args:
        color: may be one of `RED` `GREEN` `YELLOW` `BLUE` `PURPLE`；
        name: 使用生产相关性命名，不能带空格；建议基于 production correlation
        的最大值命名，例如 `0.6534` 表示 prod correlation = 0.6534；
        tags 至少包含 `PowerPoolSelected`；
        descriptions: Write in English, <=100 words. The three sections MUST be separated by
        actual newline characters (i.e. use the JSON escape sequence \\n\\n between sections,
        NOT the literal text "\\n\\n"). Example value:
        "Idea: <your idea here>\\n\\nRationale for data used: <your rationale>\\n\\nRationale for operators used: <your rationale>"
        The three section headers must appear exactly as:
        - Idea:
        - Rationale for data used:
        - Rationale for operators used:
        selection_description: (SUPER alpha only) Description of the selection expression logic.
        Must be at least 100 English characters. Write in English.
        combo_description: (SUPER alpha only) Description of the combo expression logic.
        Must be at least 100 English characters. Write in English.
    """
    try:
        if descriptions and descriptions == "None":
            return {
                "error": (
                    "descriptions cannot be the literal string 'None'. "
                    "Please regenerate it in English using exactly these three sections: "
                    "Idea:, Rationale for data used:, and Rationale for operators used:."
                )
            }
        # Normalize literal \n sequences to actual newlines in case the LLM emits
        # backslash-n as two characters rather than a true newline escape.
        if descriptions and descriptions != "None":
            descriptions = descriptions.replace('\\n', '\n')
        return _slim_alpha_response(await brain_client.set_alpha_properties(alpha_id, name, color, tags, descriptions,
                                                       selection_description, combo_description))
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def get_record_sets(alpha_id: str) -> Dict[str, Any]:
    """List available record sets for an alpha."""
    try:
        return await brain_client.get_record_sets(alpha_id)
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def get_record_set_data(alpha_id: str, record_set_name: str) -> Dict[str, Any]:
    """Get data from a specific record set."""
    try:
        return await brain_client.get_record_set_data(alpha_id, record_set_name)
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
