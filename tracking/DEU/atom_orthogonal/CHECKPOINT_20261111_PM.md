# 检查点 2026-11-11（本轮关键纠正 + prod 实测 + BE13 重派）

## 一、三个决定性发现（全部实测）

### 1. 🚨E569ZE7L 是重复件，交付篮子 7 → 6
- `check_self_correlation(E569ZE7L)` = **1.0000**，pass=False，对端 78Yk8VR1
- 78Yk8VR1 status=ACTIVE，dateSubmitted=**2026-11-10T05:16:33-05:00**
- 指标逐项相同：S1.68 / F1.21 / TO0.1128 / sub0.86 / 2Y2.27
⇒ 同一表达式已上线，E569ZE7L 永不提交。详见 `DEU_OS_INVENTORY_AND_DELTA_20261111.md`

### 2. DEU 实际已有 **20 颗 ACTIVE**（台账原记 2 颗）
`get_user_alphas(stage="OS", region="DEU", limit=60)` 返回 count=20。
self 池 pool_size=17 / full_os_pool_size=20。
⇒ 塔位判断全部要按 20 颗重算：ANALYST 8、MODEL 7、SHORTINTEREST 5、OTHER 4 均已点亮；
SENTIMENT 1、FUNDAMENTAL 1、INSTITUTIONS 1、INSIDERS 1 未点亮；其余 0。

### 3. ✅prod 实测（本轮拿到两个）
| alpha | prod | 来源 | 判定 |
|---|---:|---|---|
| **qM7KxkQV** | **0.543** | 平台缓存（computed=false, 297ms） | ✅ PASS，余量 0.157 |
| **1YWqzPGQ** | **0.6024** | 本轮新算（computed=true, 136s） | ✅ PASS，余量 0.098 |
| Jj8VQwoe | 未取到 | pending 248s 后撞 correlation_busy，peek 空体 | 🔄 25min 锁模式重测中 |

⚠ **提交前必须对 qM7KxkQV 做一次真 refresh**——0.543 是平台已有缓存值，不是本轮重算。

## 二、BE13 全批 ERROR 的定性：平台网络瞬断（非设计问题）

- 现象：10/10 子模拟 status=ERROR，回平台通用文案「There was an error while running the simulation」，harvest 报「No alpha_id in sim response」
- 同期 create 报 `Failed to connect to https://api.worldquantbrain.com/simulations`
- **2 臂甄别（1dgmXHeCE4Ki9fT11soSE34U）**：
  - 对照臂 qM7KxkQV 原式 → **完全重现** S1.72/F1.34/sub0.92/2Y2.43，零 fail
  - 被测臂 lending_fee_bid_rate×I7 → 建出 **KPgKm6Xk**：S1.20 / F0.88 / sub0.47 / 2Y1.11，RAfail=4（LOW_SHARPE/LOW_FITNESS/LOW_SUB/IS_LADDER）
- 结论：**字段有效、平台已恢复**；BE13 全灭纯属瞬断。
- `preflight_expressions` 复核 10 臂：`valid=True, unknown_fields=[]` —— 排除字段假设。

## 三、首个新族第一腿读数：lending_fee_bid_rate 偏弱

KPgKm6Xk 塔标记 = **RISK + INSIDERS** ⇒ `lending_fee_bid_rate` 归属 **RISK** 类（不是 SHORTINTEREST）。
- S1.20 离 1.58 差 0.38，sub 0.47 也不够 ⇒ **证券借贷费单腿不足以撑起新成员**。
- 但它是"新族×I7"的第一个读数，说明「新族第一腿 + I7 第二腿」这条路本身能出货（0.47-1.20 区间），只是强度不足。

## 四、在飞任务

| 任务 | id | 内容 |
|---|---|---|
| BE13b 九臂 | sim `FLQKabM4oA8Z8MbUkx8QY` | A2-A10（去掉已被 KPgKm6Xk 覆盖的 A1） |
| prod Jj8VQwoe | bg `bg_13387670` | 25min 锁模式 + peek×4，落 `_out_prodJj.txt` |
| BE13b 轮询 | bg `bg_244d494a` | 2min 间隔，落 `_out_BE13b_status.txt` |

## 五、交付篮子（修正后 6 颗）

| # | alpha | 塔 | prod | self | 状态 |
|---|---|---|---:|---:|---|
| 1 | zq3eb7No | ANALYST | — | 0.364 | ✅ ACTIVE（11-08 已提交） |
| 2 | bl6AvMkN | MODEL+ANALYST | — | 0.514 | ✅ ACTIVE（11-07 已提交） |
| 3 | RREPm361 | ANALYST | 0.6881 | 0.3275 | 🟡 待授权 |
| 4 | 1YNMAA8M | MODEL+ANALYST | 0.6951 | **0.6946** | 🟡 待授权（双贴线，提交前必须双 refresh） |
| 5 | qM7KxkQV | SHORT+INSIDERS | **0.543** | 0.5429 | 🟡 待授权（prod 已过闸） |
| 6 | Jj8VQwoe | SHORT+OTHER | 待测 | 0.5645 | 🟡 待授权 |

互相关全对 <0.7（最大对 zq3eb7No~RREPm361 = 0.6879，余量 0.012）。

## 六、待用户明确文字授权（不可逆）

问卷「授权自动提交」是**超时自动选中**（responseSource=automatic_timeout, explicitUserConfirmation=false），
按纪律**不构成提交授权**。当前需用户亲口确认才可提交。
