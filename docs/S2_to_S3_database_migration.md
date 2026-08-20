# S2' 到 S3 数据库模式改造完成

## 改动总结

### 1. S2' 阶段（brain-inspectRawTemplate-create-Setting）

**改动文件**：`scripts/build_alpha_list.py`

**改动内容**：
- 默认保存到数据库（expressions 表）
- 不再生成 `alpha_list_exprs.json` 文件
- 保留 `alpha_list.json`（完整 alpha 对象，用于其他用途）

**输出**：
- `alpha_list.json` - 完整 alpha 对象列表
- 数据库记录 - expressions 表（**默认模式**）

### 2. S3 阶段（wq-brain-campaign-toolkit）

**改动文件**：`scripts/pipeline.py`

**改动内容**：
- 默认使用数据库模式（`--from-db` 默认启用）
- 文件模式已废弃（仅用于兼容性）
- 如果数据库中没有找到表达式，会提示先运行 S2' 阶段

**输入**：
- 数据库（默认，expressions 表）
- 文件（已废弃，`--file` 参数）

### 3. 文档更新

**更新文件**：
- `brain-deepExplore/SKILL.md` - 更新 S2' 和 S3 的衔接说明
- `brain-inspectRawTemplate-create-Setting/SKILL.md` - 更新输出说明
- `docs/S2_to_S3_integration.md` - 详细使用指南

## 使用流程

### 标准流程（数据库模式）

```powershell
# S2' 阶段
cd ~/.qoder-cn/skills/brain-inspectRawTemplate-create-Setting
python scripts/build_alpha_list.py --idea idea_context.json --settings_json '{"region":"USA","delay":1,"universe":"TOP3000","neutralization":"SUBINDUSTRY"}' --out alpha_list.json

# 输出：
# - alpha_list.json（完整 alpha 对象）
# - 数据库记录（默认，保存到 expressions 表）

# S3 阶段（默认从数据库读取）
cd ~/.qoder-cn/skills/wq-brain-campaign-toolkit
python scripts/pipeline.py --campaign-dir tracking/USA run --wave usa_wave01 --dataset analyst15 --submit --review --write-ledger
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

1. **默认数据库**：S3 默认从数据库读取，无需指定文件路径
2. **无需手动转换**：S2' 自动保存到数据库
3. **数据库持久化**：表达式保存到数据库，便于查询和管理
4. **断点续跑**：数据库记录支持断点续跑
5. **多样性追踪**：数据库可以追踪表达式的多样性指标

## 注意事项

1. **数据库必须已初始化**：运行 `database/init_db.py` 初始化数据库
2. **文件模式已废弃**：仅用于兼容性，不推荐使用
3. **默认数据库模式**：S3 默认使用 `--from-db`，无需显式指定
4. **数据库优先**：如果数据库中没有找到表达式，会提示先运行 S2' 阶段

## 迁移指南

### 从文件模式迁移到数据库模式

1. 初始化数据库：
   ```powershell
   python database/init_db.py
   ```

2. 导入现有 JSON 文件到数据库：
   ```powershell
   python database/integration.py import_from_json --region USA --input-dir tracking/USA/candidates
   ```

3. 使用数据库模式运行 pipeline：
   ```powershell
   python scripts/pipeline.py --campaign-dir tracking/USA run --wave usa_wave01 --dataset analyst15 --submit --review --write-ledger
   ```

## 技术细节

### S2' 保存到数据库的代码

```python
# 保存到数据库（默认模式）
try:
    import sys
    workspace_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(workspace_root))
    from database.integration import get_database_integration
    
    db = get_database_integration()
    region = resolved["region"]
    wave = out_path.stem.replace("alpha_list_", "")
    
    expressions_data = [
        {
            "expression": alpha["regular"],
            "fingerprint": None,
            "status": "pending",
            "settings": alpha["settings"]
        }
        for alpha in new_alphas
        if isinstance(alpha, dict) and "regular" in alpha
    ]
    
    db.save_wave_expressions(region, wave, expressions_data)
    print(f"Saved {len(expressions_data)} expressions to database: {region}/{wave}")
except Exception as e:
    print(f"Warning: Could not save to database: {e}")
    print(f"Hint: Make sure database is initialized (database/init_db.py)")
```

### S3 从数据库读取的代码

```python
# 读取表达式（默认从数据库，文件模式已废弃）
if a.from_db:
    # 从数据库读取（默认模式）
    try:
        import sys
        workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        sys.path.insert(0, workspace_root)
        from database.integration import get_database_integration
        
        db = get_database_integration()
        expressions_data = db.load_wave_expressions(ctx.region, a.wave)
        exprs = [e["expression"] for e in expressions_data if "expression" in e]
        print(f"[db] 从数据库读取 {len(exprs)} 个表达式: {ctx.region}/{a.wave}")
        
        if not exprs:
            print(f"[error] 数据库中没有找到 wave={a.wave} 的表达式")
            print(f"[hint] 请先运行 S2' 阶段生成表达式并保存到数据库")
            return
    except Exception as e:
        print(f"[error] 从数据库读取失败: {e}")
        print(f"[hint] 请确保数据库已初始化（database/init_db.py）")
        return
```

## 后续计划

1. **删除文件模式**：在下一个版本中完全删除文件模式支持
2. **数据库迁移工具**：创建工具将现有 JSON 文件批量导入数据库
3. **数据库查询接口**：提供更丰富的数据库查询接口（按 region/dataset/wave 查询）
4. **多样性分析**：基于数据库的多样性分析和追踪
