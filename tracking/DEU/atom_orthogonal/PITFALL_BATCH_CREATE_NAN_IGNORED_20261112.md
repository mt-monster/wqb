# ★平台坑：batch_create_simulations 静默忽略 base_nan_handling

日期：2026-11-12
影响：BE135 首派 9 臂全部作废（整波误判为"加腿全崩"）

## 现象

用 `batch_create_simulations` 派 9 臂，顶层传 `base_nan_handling: "ON"`：

```json
{ "base_region":"DEU","base_universe":"TOP500","base_delay":1,"base_decay":0,
  "base_neutralization":"SUBINDUSTRY","base_truncation":0.08,
  "base_nan_handling":"ON","base_pasteurization":"ON",
  "base_unit_handling":"VERIFY","base_language":"FASTEXPR",
  "items":[{"expression":"..."}] }
```

返回 `ok:true` + sim id，无任何报错。但生成的 alpha：

| id | 匹配臂 | settings.nanHandling | S | F | TO | longCount |
|---|---|---|---:|---:|---:|---:|
| d5apjdrX | S1 | **OFF** | 0.60 | 0.39 | 23.9% | 13 |
| zqdZkOp1 | S1 | **OFF** | 0.57 | 0.37 | 23.4% | — |
| kqadjQpz | S2 | **OFF** | 0.40 | 0.22 | 22.0% | — |
| aka67o5O | S3 | **OFF** | 0.56 | 0.35 | 23.7% | 13 |
| KPg37kKz | S7 | **OFF** | 0.47 | 0.28 | 21.8% | — |

**同一构造在 nan=ON 下（mLapjPLX / rK7Y2vEJ 等）是 S 1.50-1.55**；nan=OFF 下塌到 0.40-0.60，longCount 从 120/175 掉到 13/13，drawdown 41%。
⇒ **不是"加腿失败"，是整波设置被篡改作废。**

## 结论与纪律

1. **`batch_create_simulations` 的 `base_nan_handling` 不生效**（静默 fallback 到 OFF）。基础回测设置（至少 nanHandling）不可信。
2. 凡"事件型/稀疏型"数据集，nanHandling 是**数量级杠杆**（本族 ON 1.5 vs OFF 0.5），设置被篡改会让整波读数量级塌陷。
3. **收割后必须逐条用 `get_alpha_details` 核对 `settings`**（nanHandling / decay / neutralization / truncation），不能只看返回的 ok:true。
4. **量级异常先查设置再下结论**：整批 S 塌一个数量级 = 先怀疑设置被改，而非构造失效。
5. 派发通道优先级：**`create_multi_simulation`（settings 可信）> `batch_create_simulations`（settings 不可信）**。

## 处置

- 原 9 臂作废，改用 `create_multi_simulation` 重派全 10 臂（含 S10）：`2P7HbD3gO4OObiLKsc9MqcL`
- 上述 5 只残骸 alpha 不再引用，其读数不进任何台账。
