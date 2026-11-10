{
 "date": "2026-11-10 04:30",
 "finding": "★★★ 可同时提交数 = 3（此前误判为 2）",
 "matrix": {
  "KPJ1rG0j|rKRx7v6m": 0.3887,
  "leAnKOEA|rKRx7v6m": 0.3969,
  "P0oR7vYw|rKRx7v6m": 0.5215,
  "leAnKOEA|KPJ1rG0j": 0.589,
  "P0oR7vYw|KPJ1rG0j": 0.7285,
  "P0oR7vYw|leAnKOEA": 0.7837
 },
 "maxSubmittableSet": {
  "members": [
   "leAnKOEA",
   "KPJ1rG0j",
   "rKRx7v6m"
  ],
  "size": 3,
  "gate": "0.7 平台 self 闸",
  "exact": true
 },
 "excluded": {
  "id": "P0oR7vYw",
  "reason": "与 KPJ 0.7285、与 leAn 0.7837 双双超 0.7"
 },
 "submissionPlan": {
  "order": "任意顺序（全对 <0.7）",
  "caveat": "leAnKOEA 含 insider_matrix(other) 腿（合规瑕疵，需用户豁免）；若不豁免则只提交 KPJ + rKR 两颗"
 },
 "basketVsSubmission": "0.5 篮子口径：{leAn,rKR} 0.3969 / {KPJ,rKR} 0.3887 可同篮，{leAn,KPJ} 0.589 不可 ⇒ 篮子 2 席、提交 3 颗（篮子与提交是两个不同口径）"
}