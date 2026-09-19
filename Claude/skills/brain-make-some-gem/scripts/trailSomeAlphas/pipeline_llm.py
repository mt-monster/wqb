# -*- coding: utf-8 -*-
"""GEM LLM 调用层：Moonshot OpenAI 兼容接口（SSE 流式 + 指数退避重试）。

2026-09-12 从 run_pipeline.py 拆出。

兼容性注意：headless_runner/run.py 通过替换 `run_pipeline.call_moonshot`
拦截并增强本调用（流式观察 + 空内容重试 + 超时降 field 重试）。
调用方必须经 run_pipeline 模块全局名（裸名）调用才能被 monkey-patch 拦截；
本模块提供原始实现，自身不得缓存/转发 call_moonshot 引用。
"""
import json
import os
import time

import requests


def call_moonshot(api_key: str, model: str, system_prompt: str, user_prompt: str, timeout_s: int = 900):
    base_url = os.environ.get("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1")
    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],

        # Default to streaming so the user can observe model progress.
        "stream": True,
    }

    retries = int(os.environ.get("MOONSHOT_RETRIES", "2"))
    backoff_s = float(os.environ.get("MOONSHOT_RETRY_BACKOFF", "2"))

    def _stream_sse_and_collect(resp: requests.Response) -> str:
        """Read OpenAI-compatible SSE stream and print deltas live.

        Still returns the full accumulated assistant content so existing callers
        (which expect a string) keep working.
        """

        content_parts: list[str] = []
        thinking_parts: list[str] = []
        thinking = False

        # Ensure requests doesn't try to decode as bytes.
        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            line = raw_line.strip()
            if not line.startswith("data:"):
                continue
            data_str = line[5:].strip()
            if data_str == "[DONE]":
                break

            try:
                event = json.loads(data_str)
            except Exception:
                continue

            choices = event.get("choices") or []
            if not choices:
                continue
            choice0 = choices[0] if isinstance(choices[0], dict) else None
            if not choice0:
                continue

            delta = choice0.get("delta") or {}
            if not isinstance(delta, dict):
                delta = {}

            # Moonshot/Kimi exposes reasoning tokens as `reasoning_content`.
            reasoning = delta.get("reasoning_content")
            if reasoning:
                if not thinking:
                    thinking = True
                    print("=============开始思考=============", flush=True)
                thinking_parts.append(str(reasoning))
                print(str(reasoning), end="", flush=True)

            piece = delta.get("content")
            if piece:
                if thinking:
                    thinking = False
                    print("\n=============思考结束=============", flush=True)
                content_parts.append(str(piece))
                print(str(piece), end="", flush=True)

            finish_reason = choice0.get("finish_reason")
            if finish_reason:
                break

        # If the stream ended while still "thinking", close the marker cleanly.
        if thinking:
            print("\n=============思考结束=============", flush=True)

        return "".join(content_parts)

    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout_s, stream=True)
            resp.encoding = "utf-8"
            if resp.status_code >= 300:
                raise RuntimeError(f"Moonshot API error {resp.status_code}: {resp.text}")

            # Prefer SSE streaming when available.
            ctype = (resp.headers.get("Content-Type") or "").lower()
            if "text/event-stream" in ctype or payload.get("stream"):
                return _stream_sse_and_collect(resp)

            data = resp.json()
            break
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            last_exc = exc
            if attempt >= retries:
                raise
            time.sleep(backoff_s * (2**attempt))
        except requests.exceptions.RequestException as exc:
            # Other request-layer issues: retry a bit, but don't loop forever.
            last_exc = exc
            if attempt >= retries:
                raise
            time.sleep(backoff_s * (2**attempt))
    else:
        raise last_exc or RuntimeError("Moonshot request failed")

    try:
        return data["choices"][0]["message"]["content"]
    except Exception as exc:
        raise RuntimeError(f"Unexpected Moonshot response: {data}") from exc
