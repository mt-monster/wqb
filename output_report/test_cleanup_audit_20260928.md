# 测试套件冗余/无用审查报告

**日期**：2026-09-28  
**范围**：项目全部测试文件（`pytest.ini` 的 `testpaths = tests world-quant-brain-mcp/tests`，外加 `Claude/skills/wq-brain-campaign-toolkit/tests` 与 `logs/` 下游离临时测试）  
**方法**：静态 AST 分析（103 个测试文件）+ `pytest --collect-only` 实证收集（1668 用例）+ 单元核对（被删功能脚本存在性校验）

---

## 一、结论先行

测试套件整体**健康、精简，无大面积冗余**。五项判定标准中：

| 判定标准 | 实证结果 |
|---|---|
| 未被引用 / 从未执行 | 仅 1 个文件（`test_enhance_v2.py`）不在 `testpaths` 内、从未被 `pytest` 收集执行 |
| 内容重复 | 无完全重复文件（sha 比对）、无跨文件同名测试用例 |
| 空断言 / 恒真断言 | 0 处（`assert True` / `x==x` / `const==const` 扫描为 0） |
| 对应功能已移除 | 仅 `test_enhance_v2.py`：其测试的 12 个工具脚本中 **9 个已不存在**（工具包已重构为另一套管线） |
| 超出当前版本范围 | 7 个 dated 快照回归测试仍守卫现存代码，**不属于超出范围**（见第四节，建议保留） |

**建议清理文件共 3 个**（1 个确定冗余 + 2 个 scratch 临时文件），移除对现行 1668 用例套件**零影响**。

---

## 二、全量盘点

- 配置内收集：`tests/`（1 根 + 97 `unit/`）+ `world-quant-brain-mcp/tests/`（5）= **103 个 .py 测试文件**
- `pytest --collect-only` 结果：**1668 个用例收集成功，0 个收集错误** → 所有导入均可解析，无因功能移除导致的破坏
- 配置外：1 个技能测试 `test_enhance_v2.py`（不在 `testpaths`）、`logs/` 下 2 个 `_tmp_*` 临时测试

---

## 三、待清理清单（经确认后移除）

### 🔴 1. `Claude/skills/wq-brain-campaign-toolkit/tests/test_enhance_v2.py`
- **判定原因**：
  1. **对应功能已移除**：该文件通过 `subprocess` 调用工具包 `scripts/` 下 12 个脚本，实测其中 **9 个已不存在**（已确认 `scripts/` 目录已重构为 `assemble_priors.py / budget_planner.py / build_wave.py / campaign.py / composition_validator.py / diversity_extract.py …` 等新管线）。缺失脚本：`ortho_prescreen` `migrate_templates` `proxy_prescreen` `calibrate_probe` `param_opt` `fit_mix_weights` `build_mix` `rescue_checklist` `diversity_slots`。
  2. **从未执行**：不在 `pytest.ini` 的 `testpaths` 内，且自身不是 pytest 风格（无 `test_*` 函数，只有 `main()` + `if __name__=="__main__"`），`pytest` 收集 0 用例 → 套件从不运行它。
  3. **硬编码路径脆弱**：第 18 行硬编码 `PY = r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe"`，跨环境即失效。
  4. **配套文档亦过时**：`Claude/skills/wq-brain-campaign-toolkit/references/enhancement-v2.md` 仍描述已被删脚本（文档不在本次清理范围，仅提示你后续同步）。
- **影响评估**：**无**（不被 `pytest` 收集，删除不改变任何收集到的 1668 用例；仅移除一份已失效的手工回归脚本）。

### 🟡 2. `logs/_tmp_test_economic.py`
- **判定原因**：`logs/` 下的临时 scratch 测试（`_tmp_` 前缀），不在 `testpaths`，从未被收集，内容为一次性经济指标探测，无回归价值。
- **影响评估**：**无**（纯 scratch 文件，删除不影响套件）。

### 🟡 3. `logs/_tmp_probe_cluster_test.py`
- **判定原因**：同上，`logs/` 下临时探测脚本，未进入套件，`probe_cluster` 相关功能已在 `tests/unit/test_cluster_variants.py` 中以规范方式覆盖。
- **影响评估**：**无**。

> 另：`logs/_pt_final2/.../test_enhance_v2.py` 与 `logs/_pytest_tmp3/.../test_enhance_v2.py` 是该脚本运行时的 pytest 缓存副本，非套件成员，可随 `logs/` 常规清理一并处理（不列入强制删除）。

---

## 四、已审查但建议保留（非冗余，请勿误删）

以下 7 个 dated 快照/修复回归测试虽带日期或 `fixes`/`landing` 字样，但经核对**仍守卫现存模块**，属有价值的回归护栏，不建议清理：

| 文件 | 守卫目标（现存） |
|---|---|
| `tests/unit/test_p0_fixes_20260927.py` | `mcp_batch_writer` `wqb.store` `wqb.workflow.nodes` 等现存模块 |
| `tests/unit/test_p1_fixes_20260927.py` | `assemble_priors` `gate` `wave_gate` `wqb.wave_results_contract` `wqb.workflow.executor` 等现存模块 |
| `tests/unit/test_p1_batch2_20260927.py` | `probe_batch_mode` `review_wave` `wave_gate` `wqb.store` 等现存模块 |
| `tests/unit/test_optimization_landing_20260925.py` | `wqb.store` `wqb.workflow` 现存模块 |
| `tests/unit/test_campaign_intel_20260919_landing.py` | 现存 campaign intel 模块 |
| `tests/unit/test_wiring_fixes_20260915.py` | `wqb.workflow.nodes` 现存模块 |
| `tests/unit/test_audit_fixes.py` | `wqb.config` `wqb.store` `wqb.workflow` 等现存模块（36 用例综合审计） |

若你认为 dated 文件名影响可读性，可后续单独做「重命名/合并快照」改造——但那是重构动作，非冗余删除，需另行确认。

---

## 五、健康度指标（基线）

- 收集用例数：**1668**，收集错误：**0**
- 解析失败文件：**0**
- 空断言 / 恒真断言：**0**
- 完全重复内容文件：**0**；跨文件同名测试：**0**
- 类内测试方法已正确计数（初版脚本漏算类方法，已修正；`test_db_write_guards.py` 实为 14 个有效测试方法，非空文件）

---

## 六、下一步

请将上述第三节清单（1 个确定冗余 + 2 个 scratch）**确认**后，我再执行移除。确认前**不会删除任何文件**。

移除后建议跑一次 `pytest -q` 复验 1668 用例仍为绿，以闭环。

---

## 七、执行结果（2026-09-28 已确认并执行）

用户确认后，3 个文件已按偏好**移至 Windows 回收站（可恢复，非硬删除）**，工具：`ctypes` 调用 `SHFileOperation` + `FOF_ALLOWUNDO`。

| 文件 | 结果 |
|---|---|
| `Claude/skills/wq-brain-campaign-toolkit/tests/test_enhance_v2.py` | ✅ 已移入回收站 |
| `logs/_tmp_test_economic.py` | ✅ 已移入回收站 |
| `logs/_tmp_probe_cluster_test.py` | ✅ 已移入回收站 |

**复验**：`pytest --collect-only` 仍为 **1668 用例 / 0 错误**，与被清理前完全一致 → 清理对现行测试套件**零影响**。

> 备注（未处理，非本次确认范围）：
> - `Claude/skills/wq-brain-campaign-toolkit/references/enhancement-v2.md` 仍描述已删脚本，建议后续同步更新。
> - `logs/_pt_final2/.../test_enhance_v2.py` 与 `logs/_pytest_tmp3/.../test_enhance_v2.py` 为运行残留缓存副本，可随 `logs/` 常规清理处理。
