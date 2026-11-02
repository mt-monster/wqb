# 各 Region 最优 SuperAlpha 方案 — 全流程扫描报告

**日期**: 2026-11-02  
**执行方式**: probe_sa_candidates.py --refresh → MCP 数据采集 → 槽位分类 → 方案文档  
**数据基线**: probe 缓存生成时间 2026-11-02T11:50:04+08:00

---

## 0. 核心结论

> **SA 线全域饱和，本轮无新建 SA 可行槽位。**

- 8 个 GO 区域（USA/IND/KOR/GBR/EUR/GLB/DEU/MEA）的所有可用 universe 均已被 SUPER 占用。
- 6 个「零 OS」槽位（USA/TOP200、EUR/TOP1200/800/400、CHN/TOP2000U、AMR/TOP600）全部无 REGULAR OS 组件，且 EUR 三档已在 10-31 实测撞 prod 墙。
- ASI（pool=9）、HKG（pool=6）组件不足硬下限 10，不可建。
- MEA 不在 platform_options 的 region 列表中，无法新建 SA（已有 2 颗保留）。
- **5 颗 UNSUBMITTED（IS 阶段）仍待命**，是唯一可推进的线索。

---

## 1. 组件池现状（probe_sa_candidates --refresh）

| Region | Active Submitted | Total Regular | Verdict |
|--------|-----------------|---------------|---------|
| USA | 46 | 283 | GO |
| IND | 45 | 63 | GO |
| KOR | 30 | 43 | GO |
| GBR | 21 | 45 | GO |
| MEA | 19 | 19 | GO（但平台不开放） |
| EUR | 19 | 600 | GO |
| GLB | 17 | 166 | GO |
| DEU | 11 | 52 | GO |
| ASI | 9 | 9 | **BLOCKED** (<10) |
| HKG | 6 | 6 | **BLOCKED** (<10) |

**与 11-01 对比**: 组件池完全未变（USA 46→46, IND 45→45, KOR 30→30, GBR 21→21, EUR 19→19, GLB 17→17, DEU 11→11）。

---

## 2. SUPER 占用情况

### 2.1 已 ACTIVE SUPER（44 颗）

| Region | Universe | 数量 | IDs |
|--------|----------|------|-----|
| IND | TOP500 | 11 | 88vKp8Va, pw52P3jb, wpbQjeKp, d51nKZJE, E5RA8pRL, j28vXOAW, MPaGzEx8, QPbjxMYw, wpjrMnz5, gJjN80rm, E5l23mrm |
| KOR | TOP600 | 10 | O0Aw0Y7Y, RRA9EZKz, 9qWJv1do, 9qWbA1g9, npPVP253, O0NLjMZR, 9qjGvaWe, rKOPg9gd, j23jgb8Z, E5vwqXNK |
| USA | TOP3000 | 4 | gJePPn0K, A1vMQ8Ve, KPGvRMg1, gJ8eVmNM |
| USA | TOP2000 | 1 | vROw5Rkd |
| USA | TOP1000 | 1 | LL5aX6Y2 |
| USA | TOP500 | 1 | E567rQvR |
| USA | TOPSP500 | 1 | 2rj3ddl5 |
| GBR | TOP700 | 4 | rKRbrZKo, MPYAOR0r, e7QGwrx6, YPMp39q6 |
| GLB | MINVOL1M | 2 | LL5amzov, A1NQ57NW |
| GLB | MINVOL10M | 1 | LLMVPag1 |
| GLB | TOP3000 | 1 | QPKVK8VW |
| GLB | TOPDIV3000 | 1 | npARO63x |
| EUR | TOP2500 | 2 | kqJOQgnk, GrgGkV1o |
| EUR | TOPCS1600 | 1 | vROOONwd |
| DEU | TOP500 | 1 | mLYLEm99 |
| MEA | TOP400 | 2 | 78jYpn0Z, 3qlYKAaO |

**按 Region 汇总**: IND 12 / KOR 11 / USA 10 / GBR 4 / GLB 5 / EUR 4 / DEU 1 / MEA 2 = **44 ACTIVE**

### 2.2 UNSUBMITTED（IS 阶段，5 颗）

| ID | Region | Universe | Neutralization | 创建时间 |
|----|--------|----------|---------------|---------|
| 9qx9aAa2 | EUR | TOP2500 | FAST | 2026-10-31 |
| RREN2WPg | KOR | TOP600 | CROWDING | 2026-10-31 |
| mLoqx1v1 | IND | TOP500 | FAST | 2026-10-31 |
| gJemoaZO | USA | TOP3000 | MARKET | 2026-10-31 |
| bl6NWjNR | USA | TOP3000 | SLOW | 2026-10-31 |

> 这 5 颗是 10-31 FAST 族破墙实验的产物。其中 9qx9aAa2（EUR FAST d1 l10: S4.83/F3.99/self0.671/prod0.670）、mLoqx1v1（IND FAST d1 l10: S4.52/F3.66/self0.651/prod0.651）、rKRbrZKo（GBR FAST d1 l10: S3.80/F2.96/self0.476/prod0.617）已 PASS 双闸。rKRbrZKo 已于 11-01 提交成功。

---

## 3. 槽位分类

### 3.1 GO 区域 × 平台可用 Universe

| Region | Universe | REGULAR OS | SUPER | 状态 |
|--------|----------|-----------|-------|------|
| USA | TOP3000 | 13 | 4 | 🔴 OCCUPIED |
| USA | TOP2000 | 6 | 1 | 🔴 OCCUPIED |
| USA | TOP1000 | 1 | 1 | 🔴 OCCUPIED |
| USA | TOP500 | 1 | 1 | 🔴 OCCUPIED |
| USA | TOPSP500 | 1 | 1 | 🔴 OCCUPIED |
| USA | TOP200 | **0** | 0 | ⚪ ZERO OS |
| IND | TOP500 | 54 | 11 | 🔴 OCCUPIED |
| KOR | TOP600 | 34 | 10 | 🔴 OCCUPIED |
| GBR | TOP700 | 21 | 4 | 🔴 OCCUPIED |
| EUR | TOP2500 | 10 | 2 | 🔴 OCCUPIED |
| EUR | TOPCS1600 | 10 | 1 | 🔴 OCCUPIED |
| EUR | TOP1200 | **0** | 0 | ⚪ ZERO OS |
| EUR | TOP800 | **0** | 0 | ⚪ ZERO OS |
| EUR | TOP400 | **0** | 0 | ⚪ ZERO OS |
| GLB | MINVOL1M | 17 | 2 | 🔴 OCCUPIED |
| GLB | MINVOL10M | 1 | 1 | 🔴 OCCUPIED |
| GLB | TOP3000 | 1 | 1 | 🔴 OCCUPIED |
| GLB | TOPDIV3000 | 1 | 1 | 🔴 OCCUPIED |
| DEU | TOP500 | 12 | 1 | 🔴 OCCUPIED |

### 3.2 停投区

| 区域 | 原因 |
|------|------|
| **MEA** | 不在 platform_options 的 region 列表中（实测 HTTP 400 `Region MEA is not available`），无法新建 SA |
| **ASI** | 组件池 9 < 硬下限 10 |
| **HKG** | 组件池 6 < 硬下限 10 |
| **AMR** | 不在 probe 缓存中，零 OS，无组件池 |
| **CHN** | 不在 probe 缓存中，零 OS，无组件池 |
| **USA/TOP200** | 零 OS（无 REGULAR 组件），self 恒 0 |
| **EUR/TOP1200** | 零 OS，10-31 实测 prod 墙（结构性） |
| **EUR/TOP800** | 零 OS，10-31 实测 prod 墙（结构性） |
| **EUR/TOP400** | 零 OS，10-31 实测 prod 墙（结构性） |

---

## 4. 本轮可执行操作

### 4.1 新建 SA

> **无。** 所有 GO 区域的可用 universe 均已被 SUPER 占用。6 个零 OS 档全部无 REGULAR OS 组件（self 恒 0），且 EUR 三档已在 10-31 实测撞 prod 墙。

### 4.2 推进 UNSUBMITTED（5 颗）

| 优先级 | ID | 操作 | 备注 |
|--------|----|------|------|
| 🔴 高 | `9qx9aAa2` | 提交（需用户点名） | EUR/TOP2500 FAST d1 l10, S4.83/F3.99/self0.671/prod0.670, 余量 0.030 |
| 🔴 高 | `mLoqx1v1` | 提交（需用户点名） | IND/TOP500 FAST d1 l10, S4.52/F3.66/self0.651/prod0.651, 余量 0.049 |
| 🟡 中 | `RREN2WPg` | 复测后提交 | KOR/TOP600 CROWDING d1 l10, self/prod 0.955 撞墙，需换族 |
| 🟡 中 | `gJemoaZO` | 复测后提交 | USA/TOP3000 MARKET d1 l10, self/prod 0.828 撞墙 |
| 🟡 中 | `bl6NWjNR` | 复测后提交 | USA/TOP3000 SLOW d1 l10, self/prod 0.783 撞墙 |

### 4.3 已 PASS 但待提交

| ID | Region | 配置 | S | F | self | prod | 余量 |
|----|--------|------|---|---|------|------|------|
| `rKRbrZKo` | GBR | TOP700 FAST d1 l10 | 3.80 | 2.96 | 0.476 | 0.617 | 0.083 |

> rKRbrZKo 已于 11-01 提交成功（ACTIVE），GBR SA 计数 5→6。

---

## 5. 平台约束

- **合法 neutralization 族**: NONE / REVERSION_AND_MOMENTUM / STATISTICAL / CROWDING / FAST / SLOW / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / SLOW_AND_FAST / COUNTRY（RAM 不合法，实测 400 拒绝）
- **SA 硬下限**: 组件池 ≥ 10（selectionLimit < 10 直接 400）
- **prod 红线**: ≥ 0.7（严格不等式）
- **SA 配额**: 账号级全局 1 SUPER/日
- **combo 表达式**: 仅 `combo_a(alpha)` 可用
- **SA 提交**: 仅 RA 通道（PPA/Power Pool 不接受）

---

## 6. 下轮建议

1. **复测 3 颗 PASS 候选**（9qx9aAa2 / mLoqx1v1 / RREN2WPg）：台账 prod >48h 不可信，终验必 refresh=True。
2. **IND/GBR 继续试 FAST l12/l14/cp3**（combo_power 增益不动 prod）。
3. **KOR 试 FAST 族**（CROWDING 已撞墙 RREN2WPg 0.955）。
4. **USA 仅剩 combo 整形**（TOP3000 四族全撞：SLOW 0.783 / MARKET 0.828 / CROWDING 0.723 / STAT 0.695-0.823）。
5. **EUR 零 OS 三档**（TOP1200/800/400）结构性 prod 墙，除非换信息源否则无解。
6. **单档仿真 ~6-8 分钟**，批量派发需后台跑（`nohup ... > log 2>&1 &`）。

---

## 7. 产出文件

- 方案文档: `output_report/SA_best_per_region_plan_20261102.md`（本文件）
- 盘点数据: `results/sa_probe_cache.json`
- MCP 原始数据: `C:\Users\MENGTAO\.workbuddy\projects\d-coding-traeCN_project-wqb\c3a152fd-bb69-41e5-bea5-2c01af0588d8\tool-results\`