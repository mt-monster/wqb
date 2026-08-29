"""提交与配额工具 (tri-state 语义见 brain-submit-verify skill) — MCP 工具层 (2026-08-13 自 main.py 按域拆分)。"""
import re, time
from typing import Dict, Any

from mcp_core import mcp, brain_client

@mcp.tool()

async def submit_alpha(alpha_id: str, force: bool = False) -> Dict[str, Any]:
    """
    Submit an alpha for production with pre-submission IS metrics check.

    Before submitting, this tool automatically checks the alpha's IS metrics against
    the following thresholds:
    - Sharpe > 1.3 and Fitness > 0.75 (local heuristic, NOT platform limits)
    - Margin > 8bp (local heuristic, NOT a platform check — downgraded to warning 2026-08-13)
    - Turnover between 4% and 40%
    - Returns > 4%
    - All IS checks must PASS (no FAIL)

    The platform's real verdict is decided at submit time by checks such as
    SELF_CORRELATION / PROD_CORRELATION / DATA_DIVERSITY / REGULAR_SUBMISSION
    (rolling 48h, limit 4) / LOW_2Y_SHARPE etc. Use force=True to skip the
    local heuristic entirely (e.g. margin below 8bp but platform-passable),
    or use the tri-state verdict flow (POST /submit 201 -> poll GET /submit
    until async checks resolve; GET 200 is NOT final while correlation
    checks are PENDING).

    Args:
        alpha_id: The ID of the alpha to submit
        force: Skip the local pre-submission heuristic check (default False)
    Returns:
        Submission result including pre-check details
    """
    try:
        if not force:
            # Fetch alpha details for IS metrics check
            alpha_details = await brain_client.get_alpha_details(alpha_id)
            check_result = brain_client.pre_submit_check(alpha_details)

            if not check_result['passed']:
                return {
                    "success": False,
                    "blocked": True,
                    "reason": "Pre-submission IS metrics check failed. Alpha does not meet submission thresholds.",
                    "check_result": check_result,
                    "hint": "Local heuristic only. Platform decides at submit time (PROD_CORRELATION etc.). "
                            "Re-run with force=True to skip, or use the tri-state verdict flow.",
                }

            # Passed check — proceed to submit
            submit_result = await brain_client.submit_alpha(alpha_id)
            success = submit_result.get("success", False) if isinstance(submit_result, dict) else bool(submit_result)
            return {
                "success": success,
                "blocked": False,
                "check_result": check_result,
                "submit_detail": submit_result,
            }
        else:
            submit_result = await brain_client.submit_alpha(alpha_id)
            success = submit_result.get("success", False) if isinstance(submit_result, dict) else bool(submit_result)
            return {"success": success, "forced": True, "submit_detail": submit_result}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

# get_submission_quota MCP tool removed (2026-08-25 user request)
# @mcp.tool()
# async def get_submission_quota() -> Dict[str, Any]:
#     """Estimate the REGULAR_SUBMISSION quota usage — DUAL view (rolling + daily)."""
#     try:
#         return await brain_client.get_submission_quota()
#     except Exception as e:
#         return {"error": f"An unexpected error occurred: {str(e)}"}
