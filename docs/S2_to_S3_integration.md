# S2' 到 S3 衔接指南

## 问题背景

之前 S2' 阶段（`brain-inspectRawTemplate-create-Setting`）生成的 `alpha_list.json` 格式与 S3 阶段（`pipeline.py`）期望的输入格式不匹配，导致需要手动转换。

## 修复方案

### 1. S2' 阶段改动

`build_alpha_list.py` 现在会同时生成三种输出：

1. **alpha_list.json** - 完整 alpha 对象列表（含 region/universe/delay 等设置）
2. **alpha_list_exprs.json** - 纯表达式列表（S3 pipeline 兼容格式，已废弃）
3. **数据库记录** - 保存到 `expressions` 表（**默认模式**）

### 2. S3 阶段改动

`pipeline.py` 现在**默认使用数据库模式**：

- **数据库模式**（默认）：`--from-db --wave <wave_name>`（默认启用）
- **文件模式**（已废弃）：`--file alpha_list_exprs.json`（仅用于兼容性）

## 使用流程

### 标准流程（数据库模式）

```powershell
# S2' 阶段
cd ~/.qoder-cn/skills/brain-inspectRawTemplate-create-Setting
python scripts/build_alpha_list.py --idea idea_context.json --settings_json '{"region":"USA","delay":1,"universe":"TOP3000","neutralization":"SUBINDUSTRY"}' --out alpha_list.json

# 输出：
# - alpha_list.json（完整 alpha 对象）
# - alpha_list_exprs.json（S3 兼容，已废弃）
# - 数据库记录（**默认**，保存到 expressions 表）

# S3 阶段（默认从数据库读取）
cd ~/.qoder-cn/skills/wq-brain-campaign-toolkit
python scripts/pipeline.py --campaign-dir tracking/USA run --wave usa_wave01 --dataset analyst15 --submit --review --write-ledger
```

### 兼容性流程（文件模式，已废弃）

```powershell
# S2' 阶段（同上）

# S3 阶段（文件模式，不推荐）
cd ~/.qoder-cn/skills/wq-brain-campaign-toolkit
python scripts/pipeline.py --campaign-dir tracking/USA run --file tracking/USA/candidates/alpha_list_exprs.json --wave usa_wave01 --dataset analyst15 --submit --review --write-ledger
```

## 数据库 Schema

S2' 保存到数据库的表达式包含以下字段：

- `wave_id` - 波次 ID
- `expression` - 表达式字符串
- `fingerprint` - 表达式指纹（可选）
- `status` - 状态（pending/complete/error）
- `settings` - 设置快照（JSON）

S3 从数据库读取时，会提取 `expression` 字段。

## 优势

1. **无需手动转换**：S2' 自动生成 S3 兼容格式
2. **数据库持久化**：表达式保存到数据库，便于查询和管理
3. **断点续跑**：数据库记录支持断点续跑
4. **多样性追踪**：数据库可以追踪表达式的多样性指标
5. **默认数据库**：S3 默认从数据库读取，无需指定文件路径

## 注意事项

1. **数据库必须已初始化**：运行 `database/init_db.py` 初始化数据库
2. **文件模式已废弃**：仅用于兼容性，不推荐使用
3. **默认数据库模式**：S3 默认使用 `--from-db`，无需显式指定
4. **数据库优先**：如果数据库中没有找到表达式，会提示先运行 S2' 阶段
