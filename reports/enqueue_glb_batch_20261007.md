# GLB 打地基批次入选清单（§三 → §二）· 2026-10-07 · **实测后已撤回（勿入队）**

> ⛔ **check_correlation(refresh=True) 实测（见 `results/glb_prod_recheck_20261007.json`）：8 颗全部过不了 prod 闸**（7 颗 0.754–0.879，`ZYbjlbX0` 异步未回源=null）。GLB/D1 PV+RISK 的 0/3 是**本账户**白空间、非**平台**白空间——production book 高度拥挤。
> ⇒ **下面「推荐入队批次」作废，不要 `--approve` 这批**；入队只会沉淀为 PROD_BLOCKED。骨架与自家 ACTIVE 不碰撞 **≠** 过 prod 闸（prod 比的是全平台 book）。本节仅留作「账户白空间≠平台白空间」的反面战例。

---


> 源：`enqueue_propose` 提案 46 里的 22 颗 GLB 代表（L2 每骨架留 1）。全部 GLB/D1 塔 **0/3 打地基**（当季口径），是本次最大白空间。
> 自锁全库比对（`sq._sig` vs alphas 全 ACTIVE，GLB 有 11 颗 ACTIVE）⇒ **排除 3 颗命中 ACTIVE 同骨架**：
> `Xgb1Q9e1`(→`MPakRYgz/O0NoPARJ`)、`zq85PwYG`(→`d5bnE8jJ`)、`akbWK6V5`(→`gJboYLRl/mLmxKN12`)。
> 其余 19 颗骨架干净。**prod 全 None（未测）⇒ 每颗提交前必须 `check_correlation(refresh=True)` 终验。**

## 推荐入队批次（8 颗 · PV×5 ＋ RISK×3，兼顾两座新塔）

| 提交优先 | alpha_id | 塔(0/3) | S | F | 2Y | prod | 备注 |
|---|---|---|---|---|---|---|---|
| 1 | `qM0vJZQE` | PV | 3.24 | 2.52 | **3.97 ✓** | None | 指标齐，最快可判 |
| 2 | `YPMnode6` | PV | 3.10 | 2.28 | **3.81 ✓** | None | 指标齐 |
| 3 | `58g9qMJX` | PV | 3.15 | 1.53 | **2.33 ✓** | None | 指标齐（F 偏弱） |
| 4 | `e7bLOO2l` | PV | **3.70** | 2.62 | 待核 | None | 全批最高 S，先补 2Y |
| 5 | `88jO2Pem` | **RISK** | 3.45 | **3.27** | 待核 | None | 最佳 RISK（点亮第二塔） |
| 6 | `ZYbjlbX0` | PV | 3.55 | 1.57 | 待核 | None | 先补 2Y |
| 7 | `GrbkvJjZ` | RISK | 2.74 | 2.94 | 待核 | None | RISK 备选 |
| 8 | `gJbxzpNQ` | RISK | 2.51 | 3.23 | 待核 | None | RISK 备选（F 高） |

> 排序键：塔档同为 0/3 ⇒ 按「业绩 + 指标完整度」；RISK 与 PV 混编以点亮 GLB 两座塔（提交时仍受 RA 4 颗/ET 日全账户约束，与 WjegEmQO/58gkLAkk 共享配额）。

## 执行链（用户裁决；本会话未跑任一步）

```bash
# 0) 先补待核的 2Y/sub（默认 dry-run，核对后加 --apply）
python tools/data-repair/backfill_alpha_metrics_from_platform.py \
    --ids e7bLOO2l 88jO2Pem ZYbjlbX0 GrbkvJjZ gJbxzpNQ
#    -> 确认平台确有 2Y 达标后：追加 --apply

# 1) L3 入队（哈希校验 + 重跑 L1）；--approve 只挑上面 8 颗，排除 3 颗自锁
python tools/ledger/enqueue_propose.py --apply \
    --proposal results/enqueue_proposal_20261007-014236.json \
    --approved-by <你的名字> \
    --reason "GLB/D1 0/3 打地基白空间：PV+RISK 族代表，已排除命中 GLB ACTIVE 的 3 颗" \
    --approve qM0vJZQE,YPMnode6,58g9qMJX,e7bLOO2l,88jO2Pem,ZYbjlbX0,GrbkvJjZ,gJbxzpNQ

# 2) 重跑盘点，让它们在 SUBMIT_NOW 现形
python tools/verdict/submit_inventory.py --no-csv

# 3) 提交前逐颗终验（prod=None 不可信快照）
#    MCP check_correlation(alpha_id, refresh=True) → 确认 prod/self 双 <0.7 且 2Y≥1.58
```

## 落选/待办
- **排除（自锁）**：`Xgb1Q9e1`、`zq85PwYG`、`akbWK6V5`。
- **可选扩批**（若 GLB 配额富余）：`P02nwrZq`(PV 3.15)、`88jKRbRz`(PV 2.75 prod0.5624 已测)、`qM0d8V5A`(PV 2.59 2Y3.6)、`LLNlZKMa`(PV 2.53 prod0.5066)。
- 提示：入队不占配额；真正卡口是「每颗 refresh 终验 + RA 4/ET 日全账户」。GLB 一次别入太多同塔，先 PV/RISK 各点一座。
