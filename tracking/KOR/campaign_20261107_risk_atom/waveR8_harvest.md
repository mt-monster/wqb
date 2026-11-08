# Wave R8 收割 + 归因（risk59 深扫 · COMPLETE 8/8 · **全集判弱**）

- multisim: 2zfoOI5Ar4ANbwb6hapOEdK · KOR/TOP600/D1 · STATISTICAL · decay4 · trunc0.08

## 读数
| id | S | F | TO | 2Y | raFail | 几何 |
|---|---:|---:|---:|---:|---:|---|
| akKQxMd9 | **0.67** | 0.35 | 0.0781 | **1.20** | 3 | bid_rate w22 水平 |
| omEJWAgm | 0.60 | 0.28 | 0.0696 | 1.01 | 3 | 利用率 ÷ 可借量 比值 |
| O0AM8qxp | 0.36 | 0.13 | 0.0708 | 1.25 | 3 | 费率 合取 利用率 |
| O0AM8qxv | 0.28 | 0.09 | 0.0982 | 0.36 | 4 | ts_corr(费率, 空头存量) |
| RREl6q8n | 0.17 | 0.04 | 0.0694 | 0.27 | 3 | s3utilization w22 |
| JjeWQYOx | 0.00 | 0.00 | 0.1025 | −0.23 | 4 | squeeze 做多高（M3 反臂） |
| Vkxm0qPY | −0.27 | −0.06 | 0.2383 | **−1.70** | 6 | DTC ts_rank 66 |
| GrWKOYLx | −0.44 | −0.14 | 0.1865 | −0.41 | 6 | crowded_score ts_zscore 252 |

## 判定：**risk59 在 KOR/TOP600/D1 判弱（不成气候）**
- 8 种互异几何，最好仅 S 0.67 / 2Y 1.20，离 S>=1.58 差 0.91；无一接近。
- 交叉印证先行战役：risk59 上 QPvr1vPM（offer_rate + hump, STATISTICAL）S 1.02、mLoJrQrW（s3utilization 双 rank）S 0.58。
  ⇒ **同一集在两条独立战役、多种几何下都只到 S ~1.0，属集合级天花板，不是参数问题。**
- M3 挤压反臂（JjeWQYOx S 0.00）与做空臂（R4 rKRN5JM1 S −0.17）**两臂都无信号** ⇒ M3 机制判死。
- M2 融券约束溢价：方向对但幅度小（bid_rate 做空高费率 S 0.67 是本集最好）⇒ **只能当辅助/门控，不能当主信号**。
- ⚠ 覆盖：risk59 的 2014 年 longCount=0（先行战役终验），实际仅 9 年 ⇒ 即便出货也须标注。

## 后续纪律
- ⛔ **risk59 不再投入**（已 8 几何 + 先行战役 2 形态 = 10 个变体全弱）。
- ⛔ risk71 / risk72 已排除（字段全是 dsrt 反转族，且覆盖 0.35–0.91）。
- ✅ 主力转 **risk70 载荷族 × RAM × decay1 × trunc0.04**（见 strategic_pivot.md），即 R10。
