"""SPC 预测挑战工具 — MCP 工具层 (2026-08-13 自 main.py 按域拆分)。"""
import json, os, re, asyncio, time, logging
from typing import Dict, List, Optional, Any, Union, Sequence, Tuple
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path

from mcp_core import (mcp, brain_client, logger, save_config, _slim_checks, _slim_alpha,
    _slim_alpha_response, _slim_alpha_list, _slim_multisim, _slim_datafields, _slim_datasets,
    _records_to_dicts, _slim_yearly, _slim_pnl, _slim_correlation_block, _slim_check_correlation,
    _slim_pyramids, _slim_text_lookup, _ra_bad, _truncate, _unwrap_result, _rewrap, _is_error)

@mcp.tool()

async def get_spc_submissions(limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    """
    List the current user's SPC (Systematic Predictions Challenge) prompt submissions.

    Args:
        limit: Maximum number of submissions to return (default: 50)
        offset: Pagination offset (default: 0)

    Returns:
        Paginated list of submissions with id, name, prompt, sampleOutput, model,
        modelVersion, weight, updateFrequency, lastModified, and status
    """
    try:
        return await brain_client.get_spc_submissions(limit, offset)
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def create_spc_submission(
    name: str,
    prompt: str,
    sample_output: str,
    model: str,
    model_version: str,
    weight: float,
    update_frequency: str,
    skip_validation: bool = False,
) -> Dict[str, Any]:
    """
    Create a new SPC (Systematic Predictions Challenge) prompt submission.

    The prompt is run periodically by the platform on the chosen model; its JSON
    output (ISIN|MIC keys, confidence scores in [-1, 1]) forms a long/short
    portfolio whose PnL is scored. Local validation of the sample output
    (JSON shape, ISIN|MIC format, ISIN checksum, score range) runs before
    submitting; failures are returned without submitting.

    Args:
        name: Submission name (max 200 characters)
        prompt: English prompt text sent to the model (max 10000 characters)
        sample_output: Sample JSON output produced by the prompt, as a string.
            Must be a pure JSON object mapping "ISIN|MIC" to numeric scores in [-1, 1]
        model: One of gpt, claude, gemini, deepseek, kimi, qwen, glm, llama, minimax, mistral
        model_version: Model version string, e.g. "5" or "4.8" (max 100 characters)
        weight: Prompt weight between 0 and 1 (two decimals). 0 means the prompt does not run
        update_frequency: One of daily, weekly, monthly, quarterly
        skip_validation: Submit even if local validation fails (default: False)

    Returns:
        The created submission (including its id), or validation errors
    """
    try:
        return await brain_client.create_spc_submission(
            name, prompt, sample_output, model, model_version, weight, update_frequency, skip_validation
        )
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def set_spc_submission_weight(submission_id: str, weight: float) -> Dict[str, Any]:
    """
    Set the weight of an existing SPC submission. Setting weight to 0 withdraws it.

    Weight is the ONLY field the platform allows changing after creation; there
    is no DELETE, and prompt text, model, and frequency are immutable. To change
    a prompt's content, create a new submission with create_spc_submission and
    set the old one's weight to 0. Use get_spc_submissions to find ids.

    Args:
        submission_id: Id of the submission to update (e.g. "V45nl1y")
        weight: New weight between 0 and 1 (two decimals); 0 withdraws the prompt

    Returns:
        The updated submission, or validation errors
    """
    try:
        return await brain_client.set_spc_submission_weight(submission_id, weight)
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def get_spc_leaderboard(
    board: Optional[str] = None,
    limit: int = 30,
    offset: int = 0,
) -> Dict[str, Any]:
    """
    Get the SPC (Systematic Predictions Challenge) monthly leaderboard.

    Args:
        board: Month key like "202607" (default: current month, chosen server-side)
        limit: Maximum number of entries to return (default: 30)
        offset: Pagination offset (default: 0)

    Returns:
        Leaderboard entries aggregated by user
    """
    try:
        return await brain_client.get_spc_leaderboard(board, limit, offset)
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


# --- Forum Tools ---
