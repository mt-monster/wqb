{
 "title": "EUR 战役交付快照（2026-11-09）",
 "status": "2 颗验证通过 / 未提交",
 "validated": [
  {
   "rank": 1,
   "id": "P0oR7vYw",
   "S": 2.28,
   "F": 1.61,
   "TO": 0.0924,
   "returns": 0.0623,
   "twoYearSharpe": 2.42,
   "sub": 1.46,
   "marginBp": 13.48,
   "failedRa": 0,
   "checksFail": [],
   "self": 0.5347,
   "prod": 0.6881,
   "yearlyCoverage": "2014-2023 全 10 年 longCount>0 且 pnl>0"
  },
  {
   "rank": 2,
   "id": "leAnKOEA",
   "S": 2.05,
   "F": 1.39,
   "TO": 0.0715,
   "returns": 0.0577,
   "twoYearSharpe": 2.48,
   "sub": 1.28,
   "marginBp": 16.13,
   "failedRa": 0,
   "checksFail": [],
   "self": 0.4625,
   "prod": 0.6476
  }
 ],
 "deliveryConstraint": "两颗互相关 0.7837 > 0.7 ⇒ 提交其一后另一颗 self 必爆，实际只能提交一颗。建议 leAnKOEA（prod 余量 0.0524 vs 0.0119）。",
 "basket4": {
  "note": "0.5 全局口径最大独立集 = 4 席（精确求解，非贪心）",
  "members": [
   "MPYEEwj8",
   "58EmKpkk",
   "O0ALVWmJ",
   "LLMvveP2"
  ],
  "prodStatus": "全 4 席的 prod 均未取到（槽位阻塞）；MPYEEwj8 与 58EmKpkk 为 tm 族，O0ALVWmJ 为 probability 族（度数=0）"
 },
 "capacityFormula": "可出席位数 ≈ 独立模型族数 × 每族 2 席。techindi_model 含 2 个独立模型族（probability_* / tm_*）⇒ 约 4 席。",
 "archivedPaths": [
  "tracking/EUR/deliverables/DELIVERY_01_P0oR7vYw.json",
  "tracking/EUR/deliverables/DELIVERY_02_leAnKOEA.json",
  "tracking/EUR/reports/eur15_facet_capacity_20261109.md",
  "tracking/EUR/reports/eur15_tm_family_20261109.md",
  "tracking/EUR/reports/eur15_zero_tower_feasibility_20261109.md",
  "tracking/EUR/candidates/cross_techindi_analyst.json",
  "tracking/EUR/candidates/cross_techindi_trileg.json",
  "tracking/EUR/candidates/cross_techindi_q5d5.json",
  "tracking/EUR/WAVE_LEDGER.md"
 ],
 "technicalBlocker": "prod 相关性计算：MCP 120s 硬上限 vs 平台 4–8 分钟计算 ⇒ 超时即丢弃；prod_wait.py 加锁模式虽能等久，但与自身/其它进程争抢账号级单并发槽。本役累计 8+ 次同类失败。"
}