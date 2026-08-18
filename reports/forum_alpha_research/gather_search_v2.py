import asyncio, json, re, base64, urllib.parse
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession

URL = "http://localhost:8876/mcp"

QUERIES = [
    "alpha 生成 经验",
    "大模型 生成 Alpha",
    "中性化 neutralization",
    "PPA 挖掘",
    "prod correlation 生产相关",
    "turnover fitness",
    "数据集 字段 选择",
    "region 区域 选择",
    "模板 template 算子",
    "sharpe 过闸",
    "self correlation 自相关",
    "alpha 思路 灵感",
]

def extract_id(link):
    if not link:
        return None
    m = re.search(r"[?&]data=([^&]+)", link)
    if not m:
        mm = re.search(r"posts/(\d+)", link)
        return mm.group(1) if mm else None
    data = urllib.parse.unquote(m.group(1))
    try:
        raw = base64.b64decode(data)
    except Exception:
        return None
    s = raw.decode("latin-1", errors="ignore")
    mm = re.search(r"posts/(\d+)", s)
    return mm.group(1) if mm else None

async def search(sess, q):
    res = await sess.call_tool("search_forum_posts", {"search_query": q, "max_results": 15})
    texts = [c.text for c in res.content if getattr(c, "type", None) == "text"]
    blob = "\n".join(texts)
    try:
        data = json.loads(blob)
    except Exception:
        return None
    return data.get("results") if isinstance(data, dict) else None

async def main():
    async with streamablehttp_client(URL) as (rd, wr, _):
        async with ClientSession(rd, wr) as sess:
            await sess.initialize()
            seen = {}
            for q in QUERIES:
                results = None
                for attempt in range(4):
                    results = await search(sess, q)
                    if results:
                        break
                    await asyncio.sleep(6)
                if not results:
                    print(f"  [EMPTY] {q}")
                    continue
                cnt = 0
                for p in results:
                    if not isinstance(p, dict):
                        continue
                    pid = extract_id(p.get("link"))
                    title = p.get("title", "(no title)")
                    if not pid:
                        continue
                    if pid not in seen:
                        seen[pid] = {"title": title, "link": p.get("link"), "queries": [q]}; cnt += 1
                    else:
                        if q not in seen[pid]["queries"]:
                            seen[pid]["queries"].append(q)
                print(f"  {q!r}: +{cnt} new (total {len(seen)})")
                await asyncio.sleep(2)
            print(f"\nTOTAL unique posts: {len(seen)}")
            with open("D:/coding/traeCN_project/wqb/reports/forum_alpha_research/search_results.json", "w", encoding="utf-8") as f:
                json.dump(seen, f, ensure_ascii=False, indent=2)
            for pid, info in seen.items():
                print(f"  {pid}  {info['title']}")

if __name__ == "__main__":
    asyncio.run(main())
