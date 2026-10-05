from __future__ import annotations

import time
from typing import Any, Dict, List

from auth_utils import create_authenticated_session


class AceClient:
    def __init__(
        self,
        *,
        username: str,
        password: str,
        brain_api_url: str = "https://api.worldquantbrain.com",
        interactive_biometric: bool = False,
    ) -> None:
        self.base_url = brain_api_url.rstrip("/")
        self.session = create_authenticated_session(
            username=username,
            password=password,
            brain_api_url=self.base_url,
            interactive_biometric=interactive_biometric,
        )

    def _request_json(self, method: str, path: str) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        while True:
            response = self.session.request(method, url)
            retry_after = response.headers.get("Retry-After") or response.headers.get("retry-after")
            if retry_after:
                time.sleep(float(retry_after))
                continue
            response.raise_for_status()
            text = (response.text or "").strip()
            return response.json() if text else {}

    def get_alpha_details(self, alpha_id: str) -> Dict[str, Any]:
        return self._request_json("GET", f"/alphas/{alpha_id}")

    def get_submission_checks(self, alpha_id: str) -> List[Dict[str, Any]]:
        payload = self._request_json("GET", f"/alphas/{alpha_id}/check")
        return payload.get("is", {}).get("checks", [])

    def get_self_correlations(self, alpha_id: str) -> Dict[str, Any]:
        return self._request_json("GET", f"/alphas/{alpha_id}/correlations/self")

    def get_prod_correlations(self, alpha_id: str) -> Dict[str, Any]:
        return self._request_json("GET", f"/alphas/{alpha_id}/correlations/prod")

    def get_yearly_stats(self, alpha_id: str) -> Dict[str, Any]:
        return self._request_json("GET", f"/alphas/{alpha_id}/recordsets/yearly-stats")

    def get_user_alphas(
        self,
        *,
        stage: str = "OS",
        limit: int = 500,
        offset: int = 0,
        start_date: str | None = None,
        end_date: str | None = None,
        submission_start_date: str | None = None,
        submission_end_date: str | None = None,
        order: str | None = None,
        hidden: bool | None = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "stage": stage,
            "limit": limit,
            "offset": offset,
        }
        if start_date:
            params["dateCreated>"] = start_date
        if end_date:
            params["dateCreated<"] = end_date
        if submission_start_date:
            params["dateSubmitted>"] = submission_start_date
        if submission_end_date:
            params["dateSubmitted<"] = submission_end_date
        if order:
            params["order"] = order
        if hidden is not None:
            params["hidden"] = str(hidden).lower()

        url = f"{self.base_url}/users/self/alphas"
        while True:
            response = self.session.get(url, params=params)
            retry_after = response.headers.get("Retry-After") or response.headers.get("retry-after")
            if retry_after:
                time.sleep(float(retry_after))
                continue
            response.raise_for_status()
            text = (response.text or "").strip()
            return response.json() if text else {}

    def get_pyramid_multipliers(self) -> Dict[str, Any]:
        return self._request_json("GET", "/users/self/activities/pyramid-multipliers")

    def submit_alpha(self, alpha_id: str) -> bool:
        """已移除（2026-09-29）：judge 是参考层，不提交。

        提交只走 workflow_submit_alpha（用户明确确认后；见 worldquant-submit-alpha）。
        保留同名方法只为让误用者得到明确报错，而不是 AttributeError。
        """
        raise RuntimeError(
            "AceClient.submit_alpha 已移除：judge 不提交；提交请用 workflow_submit_alpha（需用户明确确认）")

    def get_submit_verdict(self, alpha_id: str) -> Dict[str, Any]:
        """只读：GET /alphas/{id}/submit（**不再 POST**）。

        2026-09-29：此前本方法先 `POST /alphas/{id}/submit` 再 GET，而 baseline_from_platform
        每跑一次 judge 都会调用它——评审一次就真的提交（或触发提交）一次候选，通过的 POST
        不可撤销（且其后的 classify_check_pass 调用曾被外层 try/except 吞掉异常，事故无痕）。
        已改为纯 GET。
        注意：GET /submit 对未提交候选平台恒返 404（2026-09-26 实测，死端点），返回值只作信息，
        不构成提交判定；提交判定 = submit_verdict + prod 实测 + 用户确认（见 worldquant-submit-alpha）。
        """
        verdict = self.session.get(f"{self.base_url}/alphas/{alpha_id}/submit")
        body = verdict.json() if (verdict.text or "").strip() else {}
        checks = body.get("is", {}).get("checks", []) if isinstance(body, dict) else []
        failed = [c.get("name") for c in checks if classify_check_pass(c) is False]
        return {
            "post_status": None,          # 保留键名兼容下游；本方法不再发 POST
            "verdict_status": verdict.status_code,
            "final_success": verdict.status_code == 200,
            "failed_checks": failed,
            "note": "read-only GET; dead endpoint (404) for unsubmitted alphas — informational only",
        }


def classify_check_pass(check: Dict[str, Any]) -> bool | None:
    """PASS/FAIL tri-state: True=pass, False=fail, None=pending/unknown.

    PENDING (e.g. SELF_CORRELATION during async checks) must NOT be treated
    as failure - it is unresolved. get_alpha_details WARNING for 2Y/CW is not
    the real verdict (WARNING is classified as None here, so it never blocks by itself);
    the authoritative veto is submit_verdict (hard-gate WARNINGs count as FAIL there).
    """
    for key in ("result", "status", "checkResult"):
        value = check.get(key)
        if isinstance(value, bool):
            return value
        normalized = str(value or "").strip().lower()
        if normalized in {"pass", "passed", "ok", "true", "success"}:
            return True
        if normalized in {"fail", "failed", "false", "error"}:
            return False
        if normalized in {"pending", "warning", "warn", "unknown"}:
            return None
    return None


def extract_max_correlation(payload: Any) -> float | None:
    values: List[float] = []

    def _walk(node: Any, parent_key: str = "") -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                _walk(value, key)
            return
        if isinstance(node, list):
            for item in node:
                _walk(item, parent_key)
            return
        if isinstance(node, (int, float)) and "corr" in parent_key.lower():
            values.append(float(node))

    _walk(payload)
    return max(values) if values else None
