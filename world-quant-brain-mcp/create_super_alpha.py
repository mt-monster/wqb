"""临时脚本：绕过 MCP 工具层 bug，直接调用 brain_api 创建 SUPER alpha。
仅用于本次 SuperAlpha 创建；用完即删。
"""
import asyncio, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from brain_api import BrainApiClient, SimulationData, SimulationSettings

COMBO = 'combination(alpha("gJ8eVmNM"), alpha("xAdL5vmN"), alpha("06exgMk"), alpha("zGMV9N8"), alpha("AmYvjPe"))'
SELECTION = '(prod_correlation > 0)'


async def main():
    client = BrainApiClient()
    await client.ensure_authenticated()
    print("[AUTH] authenticated", flush=True)

    settings = SimulationSettings(
        instrumentType="EQUITY",
        region="USA",
        universe="TOP3000",
        delay=1,
        decay=5,
        neutralization="MARKET",
        truncation=0.08,
        testPeriod="P0Y0M",
        language="FASTEXPR",
        visualization=False,
        pasteurization="ON",
        maxTrade="OFF",
        selectionHandling="POSITIVE",
        selectionLimit=1000,
        componentActivation="IS",
        unitHandling="VERIFY",
        nanHandling="ON",
    )
    sim_data = SimulationData(
        type="SUPER",
        settings=settings,
        combo=COMBO,
        selection=SELECTION,
    )
    print("[CREATE] posting SUPER simulation...", flush=True)
    result = await client.create_simulation(sim_data)
    print("[RESULT]")
    print(json.dumps(result, indent=2, default=str)[:5000])


if __name__ == "__main__":
    asyncio.run(main())
