# MCP 不可用时的 REST 兜底（仅提交一颗**已确认**的 REGULAR alpha）

> 什么时候用：`mcp__wq-brain-http__*` 起不来（服务未连上、路径 ENOENT 等）**且**用户已明确确认要提交这一颗。平常一律走 MCP（自带重试 / 超时 / 预检）。
> ⚠ **不可逆**：下面的脚本会真 POST `/alphas/{id}/submit`。前置、确认、核验同 [`submit-chain.md`](submit-chain.md) §0；脚本内置 `CONFIRMED_BY_USER` 闸，默认拒跑。
> **凭据**：只读进程环境变量 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（云端由环境设置注入，本地由 shell 环境提供）。**不读 `.env`、不打印、不放命令行**（AGENTS.md：凭据只在 `.env`，禁止读取 / 打印 / 提交）。
> 认证与 MCP 服务端一致：`POST /authentication` 基本认证 → 201。若返回 401 且要求生物认证，须先在浏览器完成，脚本处理不了。

与旧版兜底相比的修正（SB-09）：① 403 不再被 `assert` 吞掉——读出 `is.checks` 里的 FAIL 项；② 实现异步受理的**补发一次**（补发前先确认 `dateSubmitted` 为空）与 `ASYNC_STUCK`；③ 属性用规范值（color `BLUE`，name 按 `docs/alpha_properties_spec.md`）；④ 退避带 `Retry-After`；⑤ 不读 `.env`。

```python
import os, sys, time, requests

BASE = "https://api.worldquantbrain.com"
AID = "<ALPHA_ID>"
CONFIRMED_BY_USER = False          # 用户在本会话明确确认后才改 True（放行权威，见 submit-chain §1）
FLIP_WAIT_S, POLL_S = 240, 5       # 取自 wqb.config.WAIT_THRESHOLDS: submit_flip_wait_s / submit_flip_poll_s

def login():
    email, pw = os.environ.get("CREDENTIALS_EMAIL"), os.environ.get("CREDENTIALS_PASSWORD")
    if not (email and pw):
        sys.exit("缺 CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD 环境变量")
    s = requests.Session()
    r = s.post(f"{BASE}/authentication", auth=(email, pw))
    if r.status_code != 201:
        sys.exit(f"认证失败 HTTP {r.status_code}")
    return s

def call(s, method, path, **kw):
    """429：按 Retry-After 与指数退避取较大者（封顶 120 s），最多 8 次。禁止固定退避。"""
    for attempt in range(8):
        r = s.request(method, f"{BASE}{path}", **kw)
        if r.status_code != 429:
            return r
        time.sleep(min(120, max(int(r.headers.get("Retry-After", 5)), 2 ** attempt)))
    return r

def status_of(s):
    d = call(s, "GET", f"/alphas/{AID}").json()
    return d.get("status"), d.get("dateSubmitted")

def submit_once(s):
    r = call(s, "POST", f"/alphas/{AID}/submit")
    if r.status_code == 403:                                   # 失败：读全量 checks 与真因，不重试
        body = r.json() if r.text else {}
        fails = [c for c in (body.get("is") or {}).get("checks", []) if c.get("result") == "FAIL"]
        sys.exit(f"403：{[(c['name'], c.get('value'), c.get('limit')) for c in fails]}"
                 "（REGULAR_SUBMISSION value>=limit = 当日配额用尽，不是候选缺陷：记待次日，不判死）")
    return r.status_code                                       # 200 / 201 / 202：都当「已受理，等翻转」

def wait_flip(s):
    t0 = time.time()
    while time.time() - t0 < FLIP_WAIT_S:
        st, ds = status_of(s)
        if st != "UNSUBMITTED":
            return st, ds
        time.sleep(POLL_S)
    return "UNSUBMITTED", None

if __name__ == "__main__":
    if not CONFIRMED_BY_USER:
        sys.exit("未确认：不提交。用户明确确认后再把 CONFIRMED_BY_USER 置 True")
    s = login()
    st, ds = status_of(s)
    if st != "UNSUBMITTED" or ds:
        sys.exit(f"status={st} dateSubmitted={ds}：不是待提交状态，不要再 POST")
    # 属性：description 必须**嵌套**写 {"regular": {"description": …}}（扁平写法被 400 "Unexpected property."）
    # r = call(s, "PATCH", f"/alphas/{AID}", json={"name": "<name>", "color": "BLUE", "tags": [...],
    #                                              "regular": {"description": "<三段式 ≥100 词>"}})
    print("POST →", submit_once(s))
    st, ds = wait_flip(s)
    if st == "UNSUBMITTED":                                    # 窗口内未翻：确认 dateSubmitted 仍空 → 补发一次 → 再等一个窗口
        st, ds = status_of(s)
        if st == "UNSUBMITTED" and not ds:
            print("补发 POST →", submit_once(s))
            st, ds = wait_flip(s)
    print("ACTIVE" if st == "ACTIVE" else f"ASYNC_STUCK（status={st}）：不再重试，知会用户", ds)
```
