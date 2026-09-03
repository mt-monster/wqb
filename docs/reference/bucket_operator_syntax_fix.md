# bucket() 算子语法修复指南

## 问题根因

平台解析器对 `bucket()` 的第二参数有严格要求：**必须是命名参数** `range="..."` 或 `buckets="..."`，不能是位置参数字符串。

### 错误写法（平台报 `invalid input at index 1, must be an expression`）

```python
bucket(rank(cap), "0.3,0.7")           # ❌ 位置参数字符串
bucket(rank(cap), '0.3,0.7')           # ❌ 单引号也一样错
```

### 正确写法

#### 方式 1：`range="start,end,step"`（等距分箱）

```python
bucket(rank(cap), range="0,1,0.1")     # ✅ 10 箱：0-0.1, 0.1-0.2, ..., 0.9-1.0
bucket(rank(cap), range="0,1,0.05")    # ✅ 20 箱：更细粒度
bucket(rank(cap), range="0.3,0.7,0.1") # ✅ 4 箱：0.3-0.4, 0.4-0.5, 0.5-0.6, 0.6-0.7
```

**语义**：从 `start` 到 `end` 按 `step` 步长切分。

#### 方式 2：`buckets="t1,t2,..."`（显式边界分箱）

```python
bucket(rank(cap), buckets="0.3,0.7")        # ✅ 3 箱：<0.3, 0.3-0.7, >0.7
bucket(rank(cap), buckets="0.2,0.5,0.8")    # ✅ 4 箱：<0.2, 0.2-0.5, 0.5-0.8, >0.8
bucket(rank(cap), buckets="2,5,6,7,10")     # ✅ 6 箱（整数边界）
```

**语义**：按显式阈值切分，n 个边界产生 n+1 个箱。

---

## 修复对照表

| 错误表达式 | 修复后 | 说明 |
|---|---|---|
| `bucket(rank(cap), "0.3,0.7")` | `bucket(rank(cap), range="0.3,0.7,0.1")` | 等距 4 箱（0.3-0.4, ..., 0.6-0.7） |
| `bucket(rank(cap), "0.3,0.7")` | `bucket(rank(cap), buckets="0.3,0.7")` | 显式 3 箱（<0.3, 0.3-0.7, >0.7） |
| `bucket(rank(x), "0,1,0.1")` | `bucket(rank(x), range="0,1,0.1")` | 标准 10 箱 |

---

## 完整示例

### 场景：市值分组中性化

```python
# ❌ 错误
group_neutralize(alpha, bucket(rank(cap), "0.3,0.7"))

# ✅ 修复 1：等距 10 箱（最常用）
group_neutralize(alpha, bucket(rank(cap), range="0,1,0.1"))

# ✅ 修复 2：显式 3 箱（粗粒度）
group_neutralize(alpha, bucket(rank(cap), buckets="0.3,0.7"))

# ✅ 修复 3：显式 5 箱（细粒度）
group_neutralize(alpha, bucket(rank(cap), buckets="0.2,0.4,0.6,0.8"))
```

### 场景：双重中性化（行业 + 市值）

```python
# ❌ 错误
a1 = group_neutralize(alpha, bucket(rank(cap), "0,1,0.1"))
group_neutralize(a1, industry)

# ✅ 修复
a1 = group_neutralize(alpha, bucket(rank(cap), range="0,1,0.1"))
group_neutralize(a1, industry)
```

---

## 验证清单

提交前检查：

1. `bucket(` 后第二参数是否有 `range=` 或 `buckets=` 前缀？
2. 字符串值是否用双引号 `"..."` 包裹？
3. `range` 是三段式 `start,end,step`？
4. `buckets` 是逗号分隔的阈值列表？

---

## 平台文档引用

`docs/reference/operators_notes.md` 第 75 行：

```
bucket(rank(x), range="0, 1, 0.1", skipBoth=False, NaNGroup=False)
bucket(rank(x), buckets="2,5,6,7,10", skipBoth=False, NaNGroup=False)
```

可选参数 `skipBoth` / `NaNGroup` 有默认值，通常省略。
