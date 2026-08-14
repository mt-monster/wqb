# tracking/ — Alpha 挖掘进度与资产追踪目录

本目录集中管理 WorldQuant BRAIN alpha 挖掘过程产生的进度、结果、评审、脚本与参考素材。
于 2026-08-14 完成结构化重组（见下方"7 项优化方案"）。

## 1. 目录结构

```
tracking/
├── EUR/  KOR/  USA/  IND/  GLB/  DEU/     # 各区域（DEU 由 deepexplore_deu 并入）
│   ├── candidates/   # 候选表达式、字段表、plan、matrix、fields、score 等输入/中间产物
│   ├── results/      # 回测结果、metrics、break、summary、final、valid 输出
│   ├── reviews/      # 证据评审（review_wave* / diversity_review 等）
│   ├── reports/      # 挖掘报告、method、recap、health 等
│   ├── scripts/      # 该区域专用脚本（*.py）
│   └── reference/    # 区域级参考素材（如字段白名单）
│   └── ra/  ppa/     # EUR 专属主题子目录（eur_ra_20260812 / ppa_mining 并入）
├── FORUM/            # 论坛灵感源（forum_* 帖子/搜索 dump），扁平存放
├── reference/        # 跨区域参考（101_alphas_pdf、expr_analyst11、pyramid_multipliers、webdata_quality）
├── mining/           # ⚠️ 共享数据湖（外部工具 fetch_all_universes.py 写入，请勿改名/移动）
├── sessions/         # 会话日志（按日期子目录）
├── runs/             # labs_data_analysis_agent.py 运行输出
├── archive/          # 大文件压缩冷备（archive/large/*.zip），原文件保留
├── MANIFEST.json     # 全量文件索引（区域/生命周期/逻辑统一名/原路径/大小）
└── _move_map.json    # 重组审计轨迹（旧路径 → 新路径），可据此或 backup 还原
```

## 2. 命名约定（统一前缀）

- 区域文件统一使用 `REGION_` 大写前缀（如 `EUR_2y_results.json`、`KOR_wave11_exprs.json`）。
- 逻辑统一名（MANIFEST 中 `unified_name`）：`{REGION}_{stage}_{wave}_{type}.{ext}`，便于跨文件检索。
- 脚本一律放在对应区域 `scripts/`，路径用 `HERE = dirname(abspath(__file__))` 相对解析，避免硬编码绝对路径。

## 3. 关键不变式（重组时务必遵守）

1. **`mining/` 目录名与内容不可改名/移动** —— `tools/fetch_all_universes.py` 向 `tracking/mining/` 写入固化 universe 数据。
2. **KOR 流水线依赖关系**（脚本间通过文件名互引，已随本次重组同步改写）：
   - `kor_pattern_scores_valid_exprs.json`（batch_validate_kor 输出 → select_wave1 输入）位于 `KOR/candidates/`
   - `kor_wave*_exprs.json` 位于 `KOR/candidates/`（kor_op_exploration_stats 以 `glob('...KOR/candidates/kor_wave*.json')` 读取）
   - `kor_wave*_review.json` 位于 `KOR/reviews/`
   - 白名单 `kor_chart_cnn_alpha_field_whitelist.json` 位于 `KOR/reference/`（kor_preflight_check 默认 `../reference/` 解析）
3. 外部工具默认路径已对齐：`tools/forum_research.py` → `tracking/FORUM/`、`tools/webdata_quality.py` → `tracking/reference/`。

## 4. 还原与回滚

- 本次重组前已全量备份：`tracking_backup_20260814/`（与重组前结构一致）。
- `_move_map.json` 记录每个文件的旧→新路径，可据此脚本化还原。
- `MANIFEST.json` 含 `original_path` 字段，便于审计。

## 5. 7 项优化方案落地情况

| # | 方案 | 落地 |
|---|------|------|
| ① | 区域内按生命周期细分目录 | ✅ EUR/KOR/USA/IND/GLB/DEU 均建 candidates/results/reviews/reports/scripts/reference |
| ② | 统一命名 `{region}_{stage}_{wave}_{type}` | ✅ 区域文件统一 `REGION_` 前缀；MANIFEST 提供全量逻辑统一名 |
| ③ | MANIFEST.json 关联索引 | ✅ 993 文件索引（区域/生命周期/类型/大小/原路径） |
| ④ | 大文件压缩归档 | ✅ 5 个大文件（共 ~15MB）压缩至 `archive/large/`，原文件保留 |
| ⑤ | 脚本配置化去硬编码 | ✅ 10 个 tracking 脚本 + 2 个外部工具路径改为相对/对齐新布局 |
| ⑥ | 清理空目录与冗余 | ✅ 移除空 `deepexplore_deu/templates`、空主题目录；删除临时 inventory 文件 |
| ⑦ | git 版本控制 | ✅ 取消根 `.gitignore` 对 tracking 的整目录屏蔽，加 `tracking/.gitignore` 排除 mining/archive/runs |
