# toolkit 文档归档（2026-09-29，skills 审查 TR-31 / TR-32 / TR-33）

这些文档从 `Claude/skills/wq-brain-campaign-toolkit/` 移出，**只作历史留存，不得当作现行规则**：

| 文件 | 为什么归档 |
|---|---|
| `enhancement-v2.md` | 自称「权威 SOP」，整篇描述的 9 个脚本（`proxy_prescreen` / `ortho_prescreen` / `migrate_templates` / `diversity_slots` / `param_opt` / `build_mix` / `fit_mix_weights` / `rescue_checklist` / `calibrate_probe`）均已于 2026-08-31 归档；含被禁的「学混合权重」，以及与 RA 判死判据冲突的「`rescue_checklist` 未全绿禁止判死」。仅保留一句原则：**预算只花在本地筛过的精英上**（已并入 toolkit SKILL） |
| `S2_COMPLIANCE_CHECKLIST.md` / `S2_COMPLIANCE_GUIDE.md` | 要求「每次进 S2 必须调用特征工程 skill、候选池基于特征工程文档构建、缺记录即中止」——三条均已被撤回（RA 步 3：特征工程按需、仅人读、禁注入 GEM；`pipeline.py` 缺记录只打印提示）；清单还要求复制进 `WAVE_LEDGER.md`（该文件是生成物）。`campaign.py s2-mark` 仍作为可选标记保留 |
| `DIVERSITY_EXTRACT_{README,SUMMARY,QUICKSTART}.md` | 三份互为近似拷贝（546 行）、营销文风、引用不存在的 `scripts/test_diversity_extract.py`、教「自动创建 candidates/reviews 目录」（与 DB 单轨冲突）。现行说明合并为 `references/diversity-extract.md`（≤ 60 行） |
