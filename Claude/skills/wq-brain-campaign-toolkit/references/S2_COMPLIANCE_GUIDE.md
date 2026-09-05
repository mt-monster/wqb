# S2 合规硬闸与检查清单使用指南

## 概述

为防止跳过 `brain-data-feature-engineering` skill 直接手写候选池，现已落地两层防御机制：

1. **第二层：检查清单** - 每次进入 S2 前的自查模板
2. **第一层：流程硬闸** - `pipeline.py` 入口强制校验

---

## 第二层：检查清单（自查模板）

### 文件位置
`references/S2_COMPLIANCE_CHECKLIST.md`

### 使用方法

1. 每次进入 S2 前，复制清单内容到当前波次的 `WAVE_LEDGER.md`
2. 逐项确认并勾选
3. 全部完成后，执行 `s2-mark` 命令写入合规记录

### 清单内容摘要

- 已调用 `brain-data-feature-engineering` skill（时间/参数/输出路径）
- 已生成特征工程 markdown 文档（包含字段分类/覆盖率/建议）
- 候选池基于 skill 输出构建（非手写）
- 决策依据完整填写
- 禁止事项确认（未跳过/未简化/未错误认知）

---

## 第一层：流程硬闸（强制校验）

### 机制说明

`pipeline.py run` 在读取表达式前，会强制校验 S2 合规记录：

- 检查 `ledger_kv` 中是否存在 `s2_compliance_w{wave}` 记录
- 检查 `feature_engineering_doc` 字段是否存在且文件有效
- 检查文档是否包含必要章节（字段/特征/建议）
- 检查 `candidate_pool_source` 是否为 `skill`

### 校验失败行为

```
[S2-COMPLIANCE] 未找到 wave=36 的 S2 合规记录（ledger_kv key=s2_compliance_w36）
[S2-COMPLIANCE] 中止：必须先完成特征工程 skill 并记录文档路径
[S2-COMPLIANCE] 逃生阀：--force 强行继续（需在台账记录原因）
```

### 逃生阀

使用 `--force` 可强行继续，但必须在台账中记录原因：

```bash
python pipeline.py --campaign-dir tracking/KOR run --wave 36 --dataset kor_streetaccount1 --force
```

---

## 标准工作流程

### 步骤 1: 调用特征工程 skill

```bash
# 通过 Skill 工具调用
Skill(brain-data-feature-engineering, region=KOR, dataset=kor_streetaccount1, delay=1)
```

### 步骤 2: 生成特征工程文档

skill 会输出 markdown 文档，例如：
`tracking/KOR/feature_engineering_kor_streetaccount1_20260826.md`

### 步骤 3: 填写检查清单

将 `S2_COMPLIANCE_CHECKLIST.md` 内容复制到 `WAVE_LEDGER.md`，逐项勾选。

### 步骤 4: 写入合规标记

```bash
python campaign.py --campaign-dir tracking/KOR s2-mark \
    --wave 36 \
    --doc-path tracking/KOR/feature_engineering_kor_streetaccount1_20260826.md \
    --candidate-pool-source skill \
    --notes "brain-data-feature-engineering skill 生成"
```

### 步骤 5: 运行 pipeline

```bash
python campaign.py --campaign-dir tracking/KOR pipeline run \
    --wave 36 --dataset kor_streetaccount1 --submit
```

此时硬闸校验通过，正常执行。

---

## 文件清单

| 文件 | 路径 | 说明 |
|:---|:---|:---|
| 检查清单模板 | `references/S2_COMPLIANCE_CHECKLIST.md` | 每次 S2 前自查用 |
| 硬闸校验函数 | `scripts/pipeline.py::_check_s2_compliance` | pipeline 入口强制校验 |
| 合规标记工具 | `scripts/s2_compliance_mark.py` | 写入 S2 合规记录到 ledger_kv |
| 子命令注册 | `scripts/campaign.py` | 添加 `s2-mark` 子命令 |

---

## 故障排查

### 问题 1: 硬闸报错"未找到 S2 合规记录"

**原因**: 未执行 `s2-mark` 命令写入记录

**解决**:
```bash
python campaign.py --campaign-dir <DIR> s2-mark --wave <WAVE> --doc-path <PATH>
```

### 问题 2: 硬闸报错"文档不存在"

**原因**: `--doc-path` 路径错误或文件被移动

**解决**: 确认文档实际路径，重新执行 `s2-mark --force` 覆盖

### 问题 3: 硬闸报错"候选池来源标记异常"

**原因**: `candidate_pool_source` 不是 `skill`（可能是 `manual`）

**解决**: 如确实为 skill 生成，重新标记：
```bash
python campaign.py --campaign-dir <DIR> s2-mark --wave <WAVE> --doc-path <PATH> --candidate-pool-source skill --force
```

如为手动构建，需补做特征工程 skill 或接受风险使用 `--force` 继续。

---

## 版本历史

- **1.0** (2026-08-26): 初始版本，落地两层防御机制
