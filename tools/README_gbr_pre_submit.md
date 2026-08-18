# GBR 区域提交前检查使用示例

## 概述

本目录包含三个工具脚本，用于确保 GBR 区域 alpha 表达式的安全提交：

1. **`validate_gbr_fields.py`** - 字段验证脚本
2. **`test_gbr_batch_isolation.py`** - 批次隔离测试脚本  
3. **`gbr_pre_submit_check.py`** - 集成提交前检查脚本

## 使用方法

### 1. 字段验证

验证表达式中所有字段在 GBR 区域是否存在：

```bash
cd tools
python validate_gbr_fields.py --expressions-file ../tracking/GBR/candidates/gbr_w09_model264_batch2_retry.txt --output gbr_field_validation_report.json
```

### 2. 批次隔离测试

小批次测试表达式，确认无误后再加入大批次：

```bash
cd tools
python test_gbr_batch_isolation.py --expressions-file ../tracking/GBR/candidates/gbr_w09_model264_batch2_retry.txt --batch-size 2 --output gbr_batch_isolation_report.json
```

### 3. 完整提交前检查

运行完整的提交前检查（推荐）：

```bash
cd tools
python gbr_pre_submit_check.py --expressions-file ../tracking/GBR/candidates/gbr_w09_model264_batch2_retry.txt --batch-size 2
```

## 针对 model264 数据集的修正

### 问题
原始批次 `gbr_w09_model264_batch2.txt` 包含无效字段 `mdl264_3l_eps_sur_decay_l3`，导致整个批次被平台连坐取消。

### 解决方案
使用修正版本 `gbr_w09_model264_batch2_retry.txt`，该版本已移除无效字段：

```bash
# 验证修正版本
python gbr_pre_submit_check.py --expressions-file ../tracking/GBR/candidates/gbr_w09_model264_batch2_retry.txt

# 如果检查通过，可以安全提交
```

## 输出文件

- `gbr_field_validation_report.json` - 字段验证报告
- `gbr_batch_isolation_report.json` - 批次隔离测试报告  
- `gbr_pre_submit_check_report.json` - 最终检查报告

## 注意事项

1. **字段验证**：确保所有字段在 GBR 区域存在且可用
2. **批次隔离**：新字段先用小批次测试，避免整批取消
3. **连坐取消**：一个无效字段会导致整个批次被取消
4. **延迟设置**：脚本内置延迟，避免请求过快触发限流

## 故障排除

### 字段验证失败
- 检查字段名拼写是否正确
- 确认字段在 GBR 区域是否可用
- 查看 `gbr_field_validation_report.json` 中的无效字段列表

### 批次隔离测试失败
- 检查表达式语法是否正确
- 确认字段组合是否有效
- 查看 `gbr_batch_isolation_report.json` 中的错误详情

### 提交后仍然取消
- 检查是否有新的无效字段
- 确认平台是否有临时限制
- 查看平台返回的具体错误信息
