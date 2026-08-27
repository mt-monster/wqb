import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from brain_api import brain_client

async def test():
    print("[INFO] 尝试认证...")
    try:
        # brain_client.authenticate 会从 .env 加载凭据
        r = await asyncio.wait_for(brain_client.authenticate(None, None), timeout=20)
        print("[RESULT]", r)
    except asyncio.TimeoutError:
        print("[TIMEOUT] 认证超时，可能需要浏览器生物识别")
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")

asyncio.run(test())
