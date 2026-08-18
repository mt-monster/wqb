import asyncio, json
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession

URL = "http://localhost:8876/mcp"

IDS = [
    "28239268385431",  # 大模型生成Alpha尝试
    "36335101288215",  # LLM变种Alpha生成工作流
    "35591278645015",  # [MCP]基于操作符生成alpha的工作流分享
    "41653035827223",  # [Python alpha]基于LLms 工作流的python alpha制作经验分享
    "30628371704215",  # 如何使用研究论文在 WQ BRAIN 中生成 Alpha 策略
    "34417037635863",  # 借用大语言模型(LLM)自动生成和发掘Alpha因子
    "36881490529815",  # 【Community Leader】零预算持续生成Alpha模板
    "29878528858135",  # 新手一个多月提交147个alpha的经验总结
    "40737593669911",  # 【经验分享】尝试Python alpha
    "13159766419479",  # “中性化”底层机制
    "41285612019351",  # Neutralization 的类型与作用
    "42078917602455",  # 【Quant101】AI因子挖掘实战 High Turnover PPA
    "37084044827159",  # 如何批量监测Prod Correlation
    "36680834830743",  # 降低Alpha的Prod Correlation：实用技巧与案例分享
    "28466349225623",  # 如何选择数据集的一些经验【备战Pyramid】
    "28790043236887",  # 掌握 Pyramid 策略：区域优化指南
    "41379941061143",  # Alpha 表达式设计模式与通用模板
    "19253259366039",  # fitness 与 turnover 关系
    "30927669645207",  # 如何拯救高turnover因子
    "42018671130391",  # Alpha 过拟合的早期信号与应对策略
    "30523862838167",  # 关于本地self-correlation检查
    "42738863064215",  # Super Alpha 实战 Combination 拆解 1-maxCorr
]

def clip(s, n):
    if not s:
        return ""
    s = s.replace("\r", "")
    return s if len(s) <= n else s[:n] + f"\n...[truncated {len(s)-n} chars]"

async def main():
    async with streamablehttp_client(URL) as (rd, wr, _):
        async with ClientSession(rd, wr) as sess:
            await sess.initialize()
            out = []
            for aid in IDS:
                try:
                    res = await sess.call_tool("read_forum_post", {"article_id": aid, "include_comments": True})
                except Exception as e:
                    out.append({"id": aid, "error": f"{type(e).__name__}: {e}"})
                    await asyncio.sleep(2)
                    continue
                texts = [c.text for c in res.content if getattr(c, "type", None) == "text"]
                blob = "\n".join(texts)
                try:
                    data = json.loads(blob)
                except Exception:
                    data = {"_raw": clip(blob, 2000)}
                # normalize
                if isinstance(data, dict):
                    post = data.get("post") or {}
                    title = post.get("title") or data.get("title") or "(no title)"
                    author = post.get("author") or data.get("author") or "?"
                    body = post.get("body") or post.get("content") or post.get("details") or data.get("body") or ""
                    comments = data.get("comments") or data.get("replies") or []
                else:
                    title = "(no title)"; author = "?"; body = ""; comments = []
                cobjs = []
                if isinstance(comments, list):
                    for cm in comments[:15]:
                        if isinstance(cm, dict):
                            cobjs.append({"author": cm.get("author") or cm.get("user") or "?", "text": clip(cm.get("body") or cm.get("text") or cm.get("content") or "", 700)})
                        elif isinstance(cm, str):
                            cobjs.append({"author": "?", "text": clip(cm, 700)})
                out.append({
                    "id": aid,
                    "title": title,
                    "body": clip(body, 2200),
                    "n_comments": len(cobjs),
                    "comments": cobjs,
                })
                print(f"  read {aid} | {title[:30]} | body={len(body)} comments={len(cobjs)}")
                await asyncio.sleep(1.5)
            with open("D:/coding/traeCN_project/wqb/reports/forum_alpha_research/read_posts.json", "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
            print(f"\nsaved {len(out)} posts -> read_posts.json")

if __name__ == "__main__":
    asyncio.run(main())
