{
 "wave": "eur15-FACET3",
 "date": "2026-11-09",
 "batches": [
  "2ChaXL8kz5c6arm8OeSNl6g",
  "1uFkpdb1u4WP9l6Ncr10Mbs",
  "44ogdT3qh4r1bJFPOGlDR8B"
 ],
 "totalGateUnique": 17,
 "mis05": {
  "size": 3,
  "members": [
   "zq3xJeAG",
   "pwd2Zaob",
   "O0ALVWmJ"
  ],
  "exact": true,
  "note": "17 件精确求解仍为 3 席"
 },
 "capacityLaw": {
  "finding": "切面多样化能降低两两互相关（0.95→0.24），但不能突破 3 席上限",
  "reason": "89 个可用切面全部源于同一个底层信号（techindi 模型预测的收益分位）。不同切面只是同一因子的不同噪声实现/时间窗，PnL 仍高度同质。",
  "correctedClaim": "撤回上一轮「切面多样化使 15 颗在 EUR 重新可行」的判断——上限是 3 席。"
 },
 "lowDegreeSeeds": {
  "zq3xJeAG": 5,
  "9qxemlAx": 5,
  "E56jMqqJ": 5,
  "wpQdA5nv": 5,
  "78L5Ro05": 5,
  "zq3xnrjV": 5,
  "O0ALVWmJ": 6,
  "pwd2Zaob": 9
 },
 "thirdBatch": [
  {
   "id": "58Emdj9k",
   "S": 3.61,
   "F": 2.7,
   "TO": 0.1729,
   "twoY": 2.36,
   "sub": 2.26,
   "fRA": 0
  },
  {
   "id": "wpQdk9O2",
   "S": 3.72,
   "F": 2.48,
   "TO": 0.2009,
   "twoY": 2.94,
   "sub": 1.98,
   "fRA": 0
  },
  {
   "id": "O0ALXJkv",
   "S": 3.15,
   "F": 2.28,
   "TO": 0.168,
   "twoY": 2.22,
   "sub": 2.21,
   "fRA": 0
  },
  {
   "id": "zq3xnrjV",
   "S": 2.88,
   "F": 2.09,
   "TO": 0.1535,
   "twoY": 2.36,
   "sub": 1.66,
   "fRA": 0
  },
  {
   "id": "78L5Ro05",
   "S": 2.83,
   "F": 2.02,
   "TO": 0.1605,
   "twoY": 2.71,
   "sub": 1.64,
   "fRA": 0
  }
 ],
 "engErr": "第三批首发 10/10 全部 No alpha_id in sim response——因 2 个字段不存在（_131 零桶）导致整批被拒。发批前必须 preflight。",
 "delivered": [
  {
   "id": "P0oR7vYw",
   "S": 2.28,
   "F": 1.61,
   "twoY": 2.42,
   "TO": 0.0924,
   "prod": 0.6881,
   "self": 0.5347
  },
  {
   "id": "leAnKOEA",
   "S": 2.05,
   "F": 1.39,
   "twoY": 2.48,
   "TO": 0.0715,
   "prod": 0.6476,
   "self": 0.4625
  }
 ],
 "deliveryConstraint": "P0oR7vYw 与 leAnKOEA 互相关 0.7837 > 0.7 ⇒ 提交其一后另一颗 self 必爆，两颗实际只能提交一颗。"
}