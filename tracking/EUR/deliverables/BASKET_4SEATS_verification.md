{
 "date": "2026-11-09",
 "basket": "0.5 口径最大独立集 4 席（精确求解）",
 "members": [
  {
   "id": "MPYEEwj8",
   "family": "tm_",
   "S": 3.83,
   "F": 2.56,
   "TO": 0.2529,
   "twoY": 2.27,
   "sub": 2.37,
   "fRA": 0,
   "self": 0.3484,
   "selfPass": true,
   "yearly": "2014-2023 / 10年 / 零空窗 / 零负年 / minLongCount 1334",
   "prod": null
  },
  {
   "id": "58EmKpkk",
   "family": "tm_",
   "S": 2.64,
   "F": 1.29,
   "TO": 0.2678,
   "twoY": 2.15,
   "sub": 1.5,
   "fRA": 0,
   "self": 0.2703,
   "selfPass": true,
   "yearly": "2014-2023 / 10年 / 零空窗 / 零负年 / minLongCount 1323",
   "prod": null
  },
  {
   "id": "O0ALVWmJ",
   "family": "probability_",
   "S": 2.37,
   "F": 1.62,
   "TO": 0.1335,
   "twoY": 2.51,
   "sub": 1.32,
   "fRA": 0,
   "self": 0.3333,
   "selfPass": true,
   "yearly": "2014-2023 / 10年 / 零空窗 / 零负年 / minLongCount 1279",
   "prod": null,
   "note": "度数=0，与全部候选互相关 <0.5，篮子核心"
  },
  {
   "id": "LLMvveP2",
   "family": "tm_",
   "S": 2.21,
   "F": 1.23,
   "TO": 0.2106,
   "twoY": 2.5,
   "sub": 1.51,
   "fRA": 0,
   "self": 0.2438,
   "selfPass": true,
   "yearly": "2014-2023 / 10年 / 零空窗 / 零负年 / minLongCount 1320",
   "prod": null
  }
 ],
 "verificationStatus": "★ 除 prod 外全部验证完成：全闸（S/F/2Y/TO/fRA）+ self <0.7 + 逐年 10 年无空窗无负年。**只差 prod 一个数字。**",
 "selfNote": "4 席 self 均显著低于已交付两颗（0.24–0.35 vs 0.46–0.53），因为它们是 tm 族 / 不同切面，与已提交池重合度更低。",
 "nextStep": "恢复 prod 测试后，任一颗 prod<0.7 即可成为第 3 颗达标件；4 颗若全过则本役达 6 颗（但受 self 闸约束需逐颗核对互相关）。",
 "platformRecheck_20261109": {
  "status": "6 颗全部 UNSUBMITTED，指标无漂移；prescreen 全部 REVIEW、0 REJECT",
  "marginUpdate": [
   {
    "id": "MPYEEwj8",
    "marginBp": 8.92,
    "note": "过 5bp 线但余量薄"
   },
   {
    "id": "58EmKpkk",
    "marginBp": 4.77,
    "note": "★ 低于 5bp 门槛 ⇒ **TO 26.8% 高换手侵蚀 margin**，即使 prod 达标也可能被 MARGIN 闸拦"
   },
   {
    "id": "O0ALVWmJ",
    "marginBp": 9.38,
    "note": "过线，本批最稳"
   },
   {
    "id": "LLMvveP2",
    "marginBp": 6.2,
    "note": "过线但薄"
   }
  ],
  "revisedFeasibility": "4 席中 58EmKpkk 有 margin 隐患（4.77bp<5bp），**实际可提交数可能从 4 降到 3**；且 tm 族 TO 21-27% 贴 30% 上限。",
  "rankAfterRecheck": "综合 sub/margin/TO：O0ALVWmJ（sub1.32/margin9.38bp/TO13.4%）与 MPYEEwj8（sub2.37/margin8.92bp）为优先验证顺序；LLMvveP2 次之；58EmKpkk 最后（margin 不达标）。"
 },
 "prodFinal": {
  "date": "2026-11-10",
  "results": [
   {
    "id": "MPYEEwj8",
    "family": "tm_",
    "S": 3.83,
    "prod": 0.8785,
    "verdict": "FAIL"
   },
   {
    "id": "LLMvveP2",
    "family": "tm_",
    "S": 2.21,
    "prod": 0.8161,
    "verdict": "FAIL"
   },
   {
    "id": "O0ALVWmJ",
    "family": "probability_",
    "S": 2.37,
    "prod": 0.7388,
    "verdict": "FAIL"
   },
   {
    "id": "58EmKpkk",
    "family": "tm_",
    "margin": "4.77bp < 5bp",
    "prod": null,
    "verdict": "FAIL（margin 闸）"
   }
  ],
  "verdict": "★ 4 席篮子 prod 全灭，无一颗可提交"
 },
 "familyProdFloor": {
  "finding": "★ U 形曲线的极小值因信号族而异（跨族不适用）",
  "probability": {
   "points": "S1.96→0.7240 / S2.05→0.6476✅ / S2.28→0.6881✅ / S2.37→0.7388 / S2.90→0.7289 / S2.92→0.7536 / S2.96→0.7464 / S4.13→0.8328 / S4.29→0.8175",
   "floor": "0.6476（leAnKOEA）"
  },
  "tm": {
   "points": "S2.21→0.8161 / S3.83→0.8785",
   "floor": "0.8161"
  },
  "conclusion": "tm_ 族 prod 地板比 probability 族高约 0.17（0.8161 vs 0.6476）⇒ **tm_ 族虽与 probability 族互相关正交（0.13-0.24），但 globally 更拥挤，整体不可提交**。"
 },
 "finalCapacity": {
  "revised": "★ EUR 实际可提交数 = **1**（P0oR7vYw 与 leAnKOEA 二选一；其余全部 prod/margin 出局）",
  "breakdown": "probability 族出 2 颗达标（互相关 0.7837 只能提一颗）；tm_ 族 0 颗（地板 0.8161）；risk60 族 0 颗（深墙 0.9156）"
 },
 "compliantBatchFinal": {
  "date": "2026-11-10 03:22",
  "batch": "3B0ufyL857z9og1exEcSdYr（合规替代批，去 insider_matrix 腿）",
  "prodResults": [
   {
    "id": "KPJ1rG0j",
    "structure": "三腿 OTHER×ANALYST×RISK",
    "S": 1.96,
    "F": 1.49,
    "TO": 0.1189,
    "twoY": 2.32,
    "marginBp": 12.16,
    "prod": 0.6957,
    "self": 0.5773,
    "yearly": "10年无空窗",
    "compliant": true
   },
   {
    "id": "78L5ngRL",
    "structure": "两腿 OTHER×ANALYST+平滑",
    "S": 2.2,
    "F": 1.65,
    "TO": 0.1486,
    "twoY": 2.56,
    "marginBp": 11.22,
    "prod": 0.7149,
    "compliant": true
   },
   {
    "id": "WjO5eAMk",
    "structure": "两腿 OTHER×ANALYST",
    "S": 2.16,
    "F": 1.52,
    "TO": 0.1006,
    "twoY": 2.12,
    "marginBp": 12.37,
    "prod": 0.732,
    "compliant": true
   },
   {
    "id": "9qxnWpZe",
    "structure": "两腿 OTHER×ANALYST",
    "S": 1.87,
    "F": 1.23,
    "TO": 0.0753,
    "twoY": 2.47,
    "marginBp": 14.47,
    "prod": 0.7276,
    "compliant": true
   }
  ],
  "internalCorr": {
   "KPJ1rG0j|78L5ngRL": 0.9233,
   "KPJ1rG0j|leAnKOEA": 0.589,
   "78L5ngRL|leAnKOEA": 0.4963
  },
  "verdict": "★ 合规件内部互相关 0.92 ⇒ 合规席位只有 1 颗（KPJ1rG0j，prod 余量仅 0.0043）",
  "exhausted": "★ 合规批 4 颗 prod 全测完：仅 KPJ1rG0j（0.6957）过线。9qxnWpZe 0.7276 / 78L5ngRL 0.7149 / WjO5eAMk 0.7320 全在 0.71-0.73 贴线区。**合规候选的 prod 已穷尽，继续跑批边际收益为负。**"
 },
 "finalDecisionMatrix": {
  "paths": [
   {
    "path": "A 单席合规",
    "combo": "KPJ1rG0j",
    "prod": 0.6957,
    "compliant": true,
    "note": "prod 余量 0.0043 偏薄，风险：平台复核波动可能超线"
   },
   {
    "path": "B 单席高质",
    "combo": "leAnKOEA",
    "prod": 0.6476,
    "compliant": false,
    "note": "含 insider_matrix(other) 腿，违反自设组腿约束；但指标三项最优"
   },
   {
    "path": "C 双席混合",
    "combo": "leAnKOEA + 78L5ngRL",
    "prod": "0.6476 / 0.7149",
    "compliant": false,
    "note": "互相关 0.4963 可同篮；但 leAnKOEA 有合规瑕疵，且 78L5ngRL prod 0.7149 超线"
   }
  ],
  "recommendation": "A（KPJ1rG0j）是唯一完全合规路径；若你裁定 insider_matrix 归类争议可豁免，则 B（leAnKOEA）指标最稳"
 },
 "complianceDualSeat": {
  "date": "2026-11-10 04:00",
  "achieved": "★★★ 全合规双席达成",
  "members": [
   {
    "id": "KPJ1rG0j",
    "structure": "三腿 OTHER×ANALYST×RISK",
    "S": 1.96,
    "F": 1.49,
    "twoY": 2.32,
    "marginBp": 12.16,
    "self": 0.5773,
    "prod": 0.6957,
    "yearly": "10年无空窗",
    "compliant": true
   },
   {
    "id": "rKRx7v6m",
    "structure": "三腿 OTHER×ANALYST×SENTIMENT",
    "S": 3.22,
    "F": 2.14,
    "twoY": 2.07,
    "marginBp": 8.87,
    "self": 0.3376,
    "prod": 0.6756,
    "yearly": "10年无空窗",
    "compliant": true
   }
  ],
  "mutualCorr": 0.3887,
  "note": "两颗均不含 insider_matrix 腿（合规）；互相关 0.3887 < 0.5 可同篮；prod 均过线（0.6957 / 0.6756）",
  "quotaUsed": "OTHER×ANALYST、OTHER×RISK、OTHER×SENTIMENT = 3/5"
 },
 "capacityFinal2": {
  "date": "2026-11-10 04:12",
  "test": "同批 5 件（KPJ1rG0j/rKRx7v6m/58EXJo7M/2rAY5bq6/E56dQX09）互相关矩阵",
  "result": "最大独立集仍 = 2 席（KPJ1rG0j + rKRx7v6m）",
  "keyCorrs": {
   "rKR|58EX": 0.4191,
   "KPJ|58EX": 0.7179,
   "rKR|E56d": 0.3257,
   "KPJ|E56d": 0.7834
  },
  "conclusion": "★ 同批换 relpopularity 腿 / 平滑 / 两腿，无法突破 2 席 ⇒ **techindi 主腿 + 多稀释腿的容量已到顶**。第 3 席必须换主腿（换数据集/换信号族）。"
 }
}