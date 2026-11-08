# Wave R11 池（anlystsn 强轴 x 8 条正交腿 · preflight 全绿 · READY）

> 依据 strategic_pivot.md：anlystsn 是 KOR risk 塔唯一强轴（omERn83n S1.62/F1.23/2Y2.27/raFail=0）。
> 做法：保持已验证骨架不变，**只换正交腿**，看哪条腿留下的特质情绪暴露最纯。

## 骨架（9 算子，<=12）

    ts_target_tvr_decay(signed_power(group_rank(winsorize(
      vector_neut(rank(ts_backfill(rsk70_mfm2_asetrd_anlystsn, 40)),
                  rank(ts_backfill(rsk70_mfm2_asetrd_<LEG>, 22))),
      std=0.38), sector), 2.5), target_tvr=0.22)

## 8 条正交腿
| # | 正交腿 | 语义 |
|---|---|---|
| R11-01 | size | 剥离规模暴露 |
| R11-02 | beta | 剥离市场 beta |
| R11-03 | resvol | 剥离残差波动 |
| R11-04 | btop | 剥离价值（账面市值） |
| R11-05 | earnyild | 剥离盈利收益率 |
| R11-06 | srisk | 剥离特异风险 |
| R11-07 | indmom | 剥离行业动量 |
| R11-08 | ltrevrsl | 剥离长期反转 |

## 设置（与 omERn83n 完全一致，隔离变量）
KOR / TOP600 / D1 · **REVERSION_AND_MOMENTUM** · **decay 1** · **truncation 0.04** · unitHandling VERIFY · nanHandling ON · pasteurization ON · maxTrade OFF

## 风险提示（先行战役实证）
- anlystsn 同族变体的 **prod / self 会互撞**：omERn83n prod 已 0.6898，离 0.70 只余 0.0102。
- 参考：anlystsn 水平 vs ts_rank(anlystsn,252) 互相关 0.6007（可共存）。
- ⇒ R11 出货后**必须先查池内互相关再选入**，不能全收。

## 备选扩产路径（R12，若 R11 不够）
- 换 signed_power 指数 {2.0, 3.0}、target_tvr {0.15, 0.30}、winsorize std {0.5}、group 轴 {industry, subindustry}、backfill 窗 {22, 66}
- 换主字段：earnyild / btop / earnqlty / divyild（R10 结果定）
