# -*- coding: utf-8 -*-
"""队列脚本关键路径验证（只读+描述 PATCH，不提交）：1 号候选 RR7OWQKd。"""
import asyncio
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(WQ_ROOT / "src"))
sys.path.insert(0, str(WQ_ROOT / "tracking" / "_submit_kit"))

from _submit_queue_20260901 import precheck_prod, ensure_description  # noqa: E402


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    aid = "RR7OWQKd"
    pc, ok = await precheck_prod(brain, aid)
    print(f"[precheck_prod] {aid} PROD={pc} pass={ok}")

    d_ok, d_len = await ensure_description(brain, aid)
    print(f"[ensure_description] {aid} ok={d_ok} len={d_len}")


if __name__ == "__main__":
    asyncio.run(main())
