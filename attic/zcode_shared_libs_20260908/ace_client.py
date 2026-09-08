"""AceClient — BRAIN 直连客户端 (单一事实源, 2026-08-13 提升自 brain-alpha-judge vendor).

原 vendor 副本已改为薄引用 shim (`brain-alpha-judge/scripts/vendor/ace_client.py`),
所有 skill 统一 import 本文件。新增方法只加这里。
"""
from __future__ import annotations

import time
from typing import Any, Dict, List

try:  # 作为包导入 (from shared_libs.ace_client import ...)
    from .auth_utils import create_authenticated_session
except ImportError:  # 作为裸脚本/目录导入 (sys.path 含 shared_libs 时)
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

    def _get_json(self, path: str, *, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """GET with Retry-After honouring (429 backoff) — used by the generic getters below."""
        url = f"{self.base_url}{path}"
        while True:
            response = self.session.get(url, params=params)
            retry_after = response.headers.get("Retry-After") or response.headers.get("retry-after")
            if retry_after:
                time.sleep(float(retry_after))
                continue
            response.raise_for_status()
            text = (response.text or "").strip()
            return response.json() if text else {}

    def get_alpha_details(self, alpha_id: str) -> Dict[str, Any]:
        return self._request_json("GET", f"/alphas/{alpha_id}")

    # ---- 2026-08-13 P1 轮新增: 通用平台查询 (供 brain-campaign-kickoff / brain-submit-verify) ----

    def get_datasets(
        self,
        *,
        region: str = "USA",
        delay: int = 1,
        universe: str | None = None,
        category: str | None = None,
        theme: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """GET /data-sets — 数据集级体检 (coverage/fieldCount/userCount/alphaCount/
        valueScore/pyramidMultiplier)。参数口径同 MCP get_datasets。"""
        params: Dict[str, Any] = {
            "region": region, "delay": delay, "limit": limit, "offset": offset,
        }
        if universe:
            params["universe"] = universe
        if category:
            params["category"] = category
        if theme:
            params["theme"] = theme
        return self._get_json("/data-sets", params=params)

    def get_datafields(
        self,
        *,
        region: str = "USA",
        delay: int = 1,
        universe: str,
        dataset_id: str | None = None,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """GET /data-fields — 必须四参齐全 (instrumentType+region+delay+universe),
        只给 dataset.id 而不给 universe → 400 Invalid query (平台实测约束)。"""
        params: Dict[str, Any] = {
            "instrumentType": "EQUITY",
            "region": region,
            "delay": delay,
            "universe": universe,
            "limit": limit,
            "offset": offset,
        }
        if dataset_id:
            params["dataset.id"] = dataset_id
        if search:
            params["search"] = search
        return self._get_json("/data-fields", params=params)

    def get_messages(self, limit: int = 20) -> Dict[str, Any]:
        """GET /users/self/messages — 当期主题公告 (ANNOUNCEMENT 类)。"""
        return self._get_json("/users/self/messages", params={"limit": limit})

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
        response = self.session.post(f"{self.base_url}/alphas/{alpha_id}/submit")
        while True:
            retry_after = response.headers.get("Retry-After") or response.headers.get("retry-after")
            if not retry_after:
                break
            time.sleep(float(retry_after))
            response = self.session.get(f"{self.base_url}/alphas/{alpha_id}/submit")
        return response.status_code == 200

    def get_submit_verdict(self, alpha_id: str, poll_rounds: int = 3, poll_interval: float = 60.0) -> Dict[str, Any]:
        """Real submission verdict (GBR campaign verified + 2026-08-12 EUR fix).

        POST /submit -> 201 = accepted (async checks pending).
        GET  /submit -> 200 = FINAL SUCCESS / 403 = rejected (body has FAIL checks)
                      / 404 = submission record cleared (was rejected async).

        **2026-08-12 fix**: the first GET right after POST can return 200 with
        SELF_CORRELATION / PROD_CORRELATION still PENDING — treating that as
        success caused a false "FINAL SUCCESS" (qMNEG2Z2: first GET 200,
        async verdict later 403 PROD_CORRELATION 0.839). We now poll until
        async checks resolve (or rounds exhausted). The only reliable success
        signal remains the alpha appearing in the OS pool (status=ACTIVE).
        """
        post = self.session.post(f"{self.base_url}/alphas/{alpha_id}/submit")
        result = self._read_verdict(alpha_id, post.status_code)
        rounds_used = 0
        while (
            rounds_used < poll_rounds
            and result["verdict_status"] == 200
            and result["pending_async_checks"]
        ):
            time.sleep(poll_interval)
            result = self._read_verdict(alpha_id, post.status_code)
            rounds_used += 1
        result["poll_rounds_used"] = rounds_used
        return result

    def _read_verdict(self, alpha_id: str, post_status: int) -> Dict[str, Any]:
        verdict = self.session.get(f"{self.base_url}/alphas/{alpha_id}/submit")
        body = verdict.json() if (verdict.text or "").strip() else {}
        checks = body.get("is", {}).get("checks", [])
        failed = [c.get("name") for c in checks if classify_check_pass(c) is False]
        pending = [c.get("name") for c in checks if classify_check_pass(c) is None]
        # async checks that must resolve before we trust a 200
        # 单一事实源: thresholds.ASYNC_CHECK_NAMES (fallback 保留本地副本以防导入顺序问题)
        try:
            from thresholds import ASYNC_CHECK_NAMES as async_names
        except ImportError:
            async_names = {
                "SELF_CORRELATION", "PROD_CORRELATION", "POWER_POOL_CORRELATION",
                "DATA_DIVERSITY", "REGULAR_SUBMISSION", "D0_SUBMISSION",
            }
        pending_async = [n for n in pending if n in async_names]
        # 404 = submission record cleared (async-rejected); 403 = explicit FAIL body
        if verdict.status_code == 404:
            status = "CLEARED"
            final = False
        elif verdict.status_code == 200 and not failed and not pending_async:
            status = "PASS"
            final = True
        elif verdict.status_code == 200 and (failed or pending_async):
            status = "PENDING"  # async checks not yet resolved, keep polling
            final = False
        else:  # 403 or anything else
            status = "FAIL"
            final = False
        return {
            "post_status": post_status,
            "verdict_status": verdict.status_code,
            "verdict": status,
            "final_success": final,
            "failed_checks": failed,
            "pending_checks": pending,
            "pending_async_checks": pending_async,
        }

    def get_submission_quota(self, window_hours: int = 48, limit: int = 4) -> Dict[str, Any]:
        """Estimate REGULAR_SUBMISSION quota usage (rolling 48h, limit 4).

        Counts OS alphas whose dateSubmitted falls inside the trailing
        window and reports remaining slots plus the earliest release time.
        Platform-verified: REGULAR_SUBMISSION check shows limit=4 rolling 48h
        (2026-08-12: value=3 after IND x2 + 1 prior submission).
        """
        import datetime as _dt
        try:
            payload = self.get_user_alphas(stage="OS", limit=100, order="-dateSubmitted")
        except Exception as exc:
            return {"error": str(exc)}

        now = _dt.datetime.now(_dt.timezone.utc)

        def _parse(ts: str):
            if not ts:
                return None
            try:
                parsed = _dt.datetime.fromisoformat(ts)
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=_dt.timezone.utc)
                return parsed
            except ValueError:
                return None

        submissions = []
        for alpha in payload.get("results", []):
            parsed = _parse(alpha.get("dateSubmitted"))
            if parsed:
                submissions.append((alpha.get("id"), parsed))
        used = [aid for aid, ts in submissions if (now - ts).total_seconds() <= window_hours * 3600]
        remaining = max(0, limit - len(used))
        latest = max((ts for _, ts in submissions), default=None)
        release = (latest + _dt.timedelta(hours=window_hours)).isoformat() if latest else None
        hours_left = max(0.0, (latest + _dt.timedelta(hours=window_hours) - now).total_seconds() / 3600) if latest else None
        return {
            "limit": limit,
            "window_hours": window_hours,
            "used": len(used),
            "used_ids": used,
            "remaining": remaining,
            "earliest_release_utc": release,
            "hours_until_release": hours_left,
        }


def classify_check_pass(check: Dict[str, Any]) -> bool | None:
    """PASS/FAIL tri-state: True=pass, False=fail, None=pending/unknown.

    PENDING (e.g. SELF_CORRELATION during async checks) must NOT be treated
    as failure - it is unresolved. get_alpha_details WARNING for 2Y/CW is not
    the real verdict; call get_submit_verdict() for the authoritative result.
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
