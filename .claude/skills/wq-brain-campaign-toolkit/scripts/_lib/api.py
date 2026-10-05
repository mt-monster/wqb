# -*- coding: utf-8 -*-
"""_lib/api.py - 平台 API 层：Basic auth + cookie jar（纯标准库）+ 传输级重试 + 429 指数退避。

单进程单登录纪律：一个进程只建一个 Api 实例并复用（multisim 分支与 per-alpha 循环共享）。

重试分层（2026-09-04）：
- 传输级（TLS 断开/连接重置/超时等网络抖动）在 Api 内部重试 3 次（scan_fields.py
  直连 api.get 曾因此 SSLZeroReturnError 整批崩溃）；
- 429 限流：2026-09-20 起由 _open_with_retry 在传输层统一退避（api_call 的外层退避保留为第二道）。
"""
import base64
import http.client
import http.cookiejar
import json
import ssl
import time
import urllib.error
import urllib.request

BASE = "https://api.worldquantbrain.com"


def _open_with_retry(open_fn, retries=3, base_delay=2, rate_retries=5, rate_base_delay=5):
    """传输级重试 + 429 限流退避（2026-09-20 合并进传输层）。

    - 连接层异常（URLError 非 HTTP 分支、ssl 错误、连接重置/断开、超时）重试 3 次（2s/4s 退避）；
    - HTTP 429 在此按 rate_base_delay 起 ×2 倍增重试 rate_retries 次（优先遵守 Retry-After）。
      2026-09-20 ASI S1 实证：scan_fields/score_datasets/pipeline 等 8 处直接 ``api.get``
      不经 ``api_call``，一个 429 就整任务崩（catalog 断链→gate 必崩）。429 是账户级限速，
      与调用方语义无关，因此统一在传输层兜底；其余状态码仍直接抛给调用方。
    """
    delay = base_delay
    rate_delay = rate_base_delay
    conn_tries = 0
    rate_tries = 0
    while True:
        try:
            return open_fn()
        except urllib.error.HTTPError as e:
            if e.code == 429 and rate_tries < rate_retries - 1:
                rate_tries += 1
                wait = rate_delay
                ra = None
                try:
                    ra = e.headers.get("Retry-After") if e.headers is not None else None
                except Exception:
                    ra = None
                if ra:
                    try:
                        wait = max(wait, float(ra))
                    except ValueError:
                        pass
                time.sleep(wait)
                rate_delay *= 2
                continue
            raise  # 非 429 状态码不重试；429 超过次数也抛出
        except (urllib.error.URLError, ssl.SSLError, ConnectionResetError,
                http.client.RemoteDisconnected, http.client.IncompleteRead,
                TimeoutError) as e:
            conn_tries += 1
            if conn_tries < retries:
                time.sleep(delay)
                delay *= 2
                continue
            raise e


class Api:
    def __init__(self):
        self.jar = http.cookiejar.CookieJar()
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

    def post(self, path, payload=None, headers=None):
        data = json.dumps(payload).encode() if payload is not None else None
        h = {"Content-Type": "application/json"}
        if headers:
            h.update(headers)
        req = urllib.request.Request(BASE + path, data=data, headers=h)
        return _open_with_retry(lambda: self.op.open(req, timeout=60))

    def get(self, path):
        req = urllib.request.Request(BASE + path)
        return _open_with_retry(lambda: self.op.open(req, timeout=60))

    def login(self, email, password):
        enc = base64.b64encode(("%s:%s" % (email, password)).encode()).decode()
        req = urllib.request.Request(BASE + "/authentication", data=b"",
                                     headers={"Authorization": "Basic " + enc})
        _open_with_retry(lambda: self.op.open(req, timeout=60))


def api_call(api, method, path, payload=None, retries=5, base_delay=5):
    """429 指数退避包装：429 时 base_delay 起 ×2 倍增重试；非 429 直接抛。"""
    delay = base_delay
    for i in range(retries):
        try:
            return (api.post(path, payload) if method == "post" else api.get(path))
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
