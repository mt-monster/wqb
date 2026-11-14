# ★塔点亮推演：提交这 14 颗会把 INSIDERS 塔从 0 点亮到 4

日期：2026-11-12

## 一、14 颗的塔分布（平台实测）

| # | alpha | S | 塔构成 | eff | 状态 |
|---|---:|---|---|---:|---|
| 1 | vR1oxZA3 | 3.27 | （无标记）| — | ACTIVE |
| 2 | d5apW38x | 2.36 | **INSIDERS+MODEL** | 2 | UNSUBMITTED |
| 3 | WjlMlWJd | 2.21 | **PV+INSIDERS+ANALYST** | 0 | UNSUBMITTED |
| 4 | RREPm361 | 2.02 | ANALYST | 1 | UNSUBMITTED |
| 5 | zq3eb7No | 2.01 | ANALYST | 1 | ACTIVE |
| 6 | rKRx2Alj | 1.95 | MODEL+ANALYST | 2 | ACTIVE |
| 7 | 9qlz29Oe | 1.86 | SHORTINTEREST+NEWS | 2 | UNSUBMITTED |
| 8 | npa9PKWw | 1.74 | **INSIDERS+OTHER** | 2 | UNSUBMITTED |
| 9 | qM7KxkQV | 1.72 | SHORTINTEREST+**INSIDERS** | 2 | UNSUBMITTED |
| 10 | 78Yk8VR1 | 1.68 | SHORTINTEREST | 1 | ACTIVE |
| 11 | Jj8VQwoe | 1.65 | SHORTINTEREST+OTHER | 2 | UNSUBMITTED |
| 12 | GrW9OxmG | 1.62 | ANALYST | 1 | ACTIVE |
| 13 | bl6AvMkN | 1.61 | MODEL+ANALYST | 2 | ACTIVE |
| 14 | d5a2vxzY | 1.60 | SHORTINTEREST | 1 | UNSUBMITTED |

## 二、塔计数推演

| 塔 | 平台当前 | 提交 14 颗后 | 点亮阈值 | 状态 |
|---|---:|---:|---:|---|
| **INSIDERS** | **0** | **4** | 3 | ✅ **将从 0 直接点亮** |
| ANALYST | 6 | 6（无新增）| 3 | 已点亮 |
| SHORTINTEREST | 3 | 5 | 3 | 已点亮 |
| MODEL | 3 | 3（无新增）| 3 | 已点亮 |
| **OTHER** | **2** | **2** | 3 | ❌ **只差 1 颗** |
| **PV** | 0 | 1 | 3 | ❌ 差 2 颗 |
| **NEWS** | 0 | 1 | 3 | ❌ 差 2 颗 |

## 三、三条可执行判断

### 判断1：INSIDERS 塔已可点亮
d5apW38x / WjlMlWJd / npa9PKWw / qM7KxkQV 四颗都带 INSIDERS 塔。
⇒ **只要授权提交这 4 颗，DEU/D1 的 INSIDERS 塔就从 0 变成 4（点亮）。**
⇒ 这也说明「锁 insiders」的战术目标（点 insiders 塔）已经达成，只是卡在提交授权上。

### 判断2：OTHER 塔只差 1 颗
当前 2 颗（来自 npa9PKWw 与 Jj8VQwoe）。
⇒ **再出一颗带 OTHER 塔的合规件，就能点亮第三座塔。**
⇒ BE163（翻转权重）里有 O4 主导的 R6/R7/R8 三臂，若其中出件，正好补 OTHER。

### 判断3：PV / NEWS 塔各差 2 颗
WjlMlWJd 贡献 PV 1 颗、9qlz29Oe 贡献 NEWS 1 颗。各需再 2 颗。

## 四、对 20 颗目标的意义

当前 14 颗的实际价值高于数字本身：**它能把 insiders 塔从 0 点亮**，这是本战役最直接的可量化战果。
若再补 1 颗 OTHER 塔的件，就能同时点亮 insiders + other 两座塔。