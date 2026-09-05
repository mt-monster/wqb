# 增强流水线 v2（Enhancement Pipeline v2）

> 定位：GBR 战役实证"29 批 232 回测同质化 + 评估不闭环"后的增强逻辑升级。
> 设计原则：**平台回测配额只花在本地筛过的精英身上**；全部新工具零配额，
> 与现有引擎（probe 三灯 / repair 爬山 / gate 6 闸 / build_wave）无缝拼接。
> 本文档为权威 SOP；各脚本自身的 docstring 是参数细则。

## 一、流水线全景（HyperBand 三级淘汰 + 九工具）

```
[生成端] makeSomeGem / build_wave / diversity_extract
   │ 候选池
   ▼
L1 本地代理层（零配额，全部脚本）
   ├─ proxy_prescreen.py   历史回测训练的分类器：低分直接不投
   ├─ ortho_prescreen.py   与历史强信号去同质（sim>0.4 剔除）
   ├─ migrate_templates.py 跨区域成功骨架字段替换（新结构来源）
   └─ diversity_slots.py   闸6 注入契约渲染（非线性变换/事件门控模板）
   ▼ 精英池
L2 平台便宜批（探针三灯 + gate 6 闸 + 设置对照）
   ├─ gate.py（闸6 批级多样性强制）→ 七槽填槽提交
   ├─ neutralization_sweep.py  中性化/decay 对照批（验证过度中性化假说）
   └─ score_datasets.py --probe-score  三灯判定（黄灯限 2 批）
   ▼
L3 精批（repair 爬山 + 组合放大）
   ├─ param_opt.py           TPE 提议参数组合（替代固定网格）
   ├─ build_mix.py / fit_mix_weights.py  跨数据集 mix + 学权重
   └─ rescue_checklist.py    判死前七武器核对（未全绿不得判死）
   ▼
[S5 提交] brain-alpha-judge → worldquant-submit-alpha
[校准回路] calibrate_probe.py 定期把判死/候选历史拟合回三灯权重
```

三级淘汰 = HyperBand 思想的两段式推广：便宜批（多结构各 1-2 条）→ 中批
（胜者变体）→ 精批（参数调优），每级只带上一级精英，预算封顶。

## 二、九工具速查

| 脚本 | 层 | 输入 | 输出 | 触发场景 |
|---|---|---|---|---|
| `ortho_prescreen.py` | L1 | 候选 JSON + results/ | reference/ortho_prescreen_report.json + ortho_kept_exprs.json | 每波新候选提交前 |
| `migrate_templates.py` | L1 | 源区域 candidates/ + 目标 typed catalog | candidates/migrated_*.json | 区域骨架耗尽时引入新结构 |
| `proxy_prescreen.py` | L1 | results/*.csv 训练；候选打分 | reference/proxy_model.joblib + proxy_score_report.json | 积累 ≥30 样本后启用 |
| `calibrate_probe.py` | 校准回路 | 各区域 results + 台账 | reference/probe_weights_calibrated.json（--apply 写回 thresholds） | 每 2-3 战役周期 |
| `param_opt.py` | L3 | 参数空间 JSON + 历史得分 | reference/param_opt_next.json | repair 批参数提议 |
| `fit_mix_weights.py` | L3 | alpha id 列表（拉免费 PnL） | reference/mix_weights_fit.json | 混合前学权重 |
| `build_mix.py` | L3 | 两侧 top 信号文件 | candidates/mix_*.json | 单数据集顶到天花板 |
| `neutralization_sweep.py` | L2 | top 赢家表达式 | candidates/settings_sweep_alpha_list.json（交 batch_simulator） | 验证中性化/decay 假说 |
| `rescue_checklist.py` | L3 判死闸 | --dataset | reference/rescue_checklist_<ds>.json（--fail 未全绿退出 1） | 判死前必跑 |

## 三、标准 SOP

### 3.1 新波候选提交前（L1 必做）
```powershell
python ortho_prescreen.py --campaign-dir tracking/GBR --exprs <新波文件>
# sim>0.4 的同质候选被剔除；kept 清单才进 gate
python proxy_prescreen.py --campaign-dir tracking/GBR --score <kept 文件> [--filter]
# 模型训练过一次后可用；PASS/REVIEW/DROP 三档
```

### 3.2 判死前（L3 判死闸，接在 --probe-score --mark-dead 之前）
```powershell
python rescue_checklist.py --campaign-dir tracking/GBR --dataset <DS> --fail
# 七武器（mirror/backfill/中性化对照/事件门控/迁移/mix/repair）未全绿 → 退出 1，禁止判死
# MISS 项逐个补齐后再跑，全绿才执行 mark_dead
```

### 3.3 三灯权重校准（每 2-3 战役周期）
```powershell
python calibrate_probe.py --campaign-dir tracking/GBR --extra-regions tracking/KOR tracking/USA
# 先看 reference/probe_weights_calibrated.json 的样本量与权重方向
# 确认合理后 --apply 写回 thresholds.json probe_scoring_v2
```

### 3.4 中性化对照轨（GBR 过度中性化假说验证，1-2 批成本）
```powershell
python neutralization_sweep.py --campaign-dir tracking/GBR --exprs <top 赢家>
# 输出 alpha_list.json 交 batch_simulator 七槽提交
# 回测后对比 SUBINDUSTRY/SECTOR/MARKET/STATISTICAL 四档 sharpe 分布
```

## 四、护栏与红线

1. **所有新脚本不得烧仿真配额**（fit_mix_weights 只做免费 PnL 查询）。
2. **校准/评分输出一律"建议"，硬过滤由人确认**：proxy 的 --filter、
   calibrate 的 --apply 都是显式开关，不默认动线上配置。
3. **判死纪律**：rescue_checklist --fail 未全绿时，任何流程不得 mark_dead。
4. **迁移/混合产物与本地生成同等对待**：必须过 ortho → gate 6 闸，不得直投。
5. **与闸6 契约关系**：L1 工具是"加宽候选池+预筛"；闸6 是"批级多样性兜底"，
   两者互补，不可互相替代。
6. **回归测试**：改动任何脚本后跑 `python tests/test_enhance_v2.py`（零配额，
   假战役目录自动建于系统临时目录，47 项断言覆盖 9 工具 + 闸6 回归）。

## 五、与既有引擎的接缝

- probe 三灯（score_datasets.py）权重来自 thresholds.json probe_scoring_v2，
  calibrate_probe 只改 w_* 与 green/yellow_min，不动 breadth_bar 等结构阈值。
- repair 批参数网格由 param_opt 提议后仍走原有 repair 渲染路径（表达式
  渲染 + gate 全闸），只是参数组合来源从"手拍网格"变"TPE 提议"。
- build_wave 的骨架配给与闸6 的 skeleton_quota 不变；migrate/mix 产物作为
  新候选源进入 build_wave 或直接 gate。
- batch_simulator 消费 settings_sweep 的 alpha_list.json（字段名 `regular`
  与 per-item settings 已验证兼容）。
