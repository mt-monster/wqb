# SUPER alpha（SA）参数台账（EUR 实测）

> 从 `MEMORY.md` 外移。做 SA 前必读。

## 硬参数

- `selectionLimit` **平台硬下限 = 10**（<10 直接 400）。
- 论坛 78 赞帖建议 **30–100 起测、≤500**。
- 实际生效数 = `min(limit, 组件池)`，**组件池是 region 级**（非 universe 级）⇒ SA 指标天花板由该 region 的 ACTIVE REGULAR 数决定：
  **EUR 14｜IND 38｜USA 44**。

## 指标三档

| 档位 | 门槛 |
|---|---|
| 平台底线 | S 1.58 / F 1.0 / prod<0.7 |
| 社区合格 | **prod<0.6 且 TO<0.30** |
| 比赛档 | S 5.6–7.0 / F 5.6–8.9+ |

## 组件筛选阈值

`turnover < 0.3` × `prod_corr < 0.6` × `author_fitness ≥ 2`

## 中性化 / 族选择

- 中性化 Fitness 排序（IND 实测）：**CROWDING > RAM > SLOW/FAST**
- 选族规则：`TO < 0.10 → SLOW`；`TO > 0.20 → FAST`

## 组件数效应

⚠ **组件数↑ ⇒ self↓ 但 prod↑**
- EUR 实测：`l10` → self 0.33 / prod 0.56；`l12` → self 0.29 / prod 0.61。
⇒ 加组件治 self 但恶化 prod，prod 已近 0.6 时不要再加。
