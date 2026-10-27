# -*- coding: utf-8 -*-
"""db_conn — data/wqb.db 规范连接工厂（single point of truth，2026-09-20）。

背景（reports/db_concurrent_write_lock_audit_20260920.md）：
  多会话并发下 `database is locked` 事故的四个根因之一是裸
  ``sqlite3.connect`` 散布全库且 ``busy_timeout`` 不一（默认 5s~30s）。
  本模块是全库唯一允许直接调用 ``sqlite3.connect`` 打开 **wqb.db** 的地方。

规范（所有经本工厂的连接自动获得）：
  - ``journal_mode=WAL``      读写并发不互斥（幂等，持久化于库文件）
  - ``busy_timeout=60000``    写锁排队 60s（统一口径，替代 5s/10s/30s 不一）
  - ``foreign_keys=ON``       外键约束（2026-09-07 P1.4 起口径）
  - ``synchronous=NORMAL``    WAL 下安全且更快

守卫：``tests/unit/test_db_write_guards.py::test_no_naked_sqlite_connect``
静态扫描活跃目录，禁止白名单外出现 ``sqlite3.connect(``。

零依赖设计：本模块只 import 标准库；``default_db_path`` 与
``wqb.store._common`` 保持同口径（WQB_DB_PATH 环境变量优先），
但刻意复制而非 import，避免把轻量工具脚本拖进 store 包的 import 链。
"""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any, Optional

_DEFAULT_REL = Path("data") / "wqb.db"

#: 允许直接 ``sqlite3.connect`` 的文件（相对仓库根，/ 分隔）。静态守卫消费。
#: GEM/feature_engineering 三处为「无 src 依赖环境」的合规内联（已升级 PRAGMA），
#: 守卫要求其内容含 busy_timeout 以确保升级到位。
DIRECT_CONNECT_WHITELIST = (
    "src/wqb/db_conn.py",           # 本文件
    "wqb_db_mcp.py",                # MCP server 自管连接（配置同规范）
    "tools/lib/wqb_db.py",          # tools 层兼容 re-export
    "tools/fields/skeleton_panel.py",  # 区域字段骨架探针（pre-existing untracked）
    "tools/gates/operator_coverage_audit.py",  # 算子覆盖审计（pre-existing untracked）
    "Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/db.py",  # toolkit 同构工厂
    "Claude/skills/brain-make-some-gem/scripts/headless_runner/run.py",
    "Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/run_pipeline.py",
    "Claude/skills/brain-data-feature-engineering/scripts/feature_engineering.py",
    "tools/sreq_precheck.py",           # S_req 前置筛选（pre-existing untracked）
    "tools/_ab_adopt.py",                # A/B 批次收割（pre-existing untracked）
    "tools/_ab_template.py",              # P3 A/B 验证（pre-existing untracked）
    "tools/_dataset_report.py",           # EUR 战役全景报告（pre-existing untracked）
    "tools/_e1_probe_pp.py",              # E1 pp vs lvl_rk A/B（pre-existing untracked）
    "tools/_grp_rank_probe.py",           # group_rank 模板实验（pre-existing untracked）
    "tools/_lowcov_status.py",            # 低覆盖波状态（pre-existing untracked）
    "tools/_modelfam_probe.py",           # 模型型集字段探针（pre-existing untracked）
    "tools/_pvpc_gen_preflight.py",       # *_pre_close_2 表达式预生成（pre-existing untracked）
    "tools/_pv_preclose_sweep.py",        # *_pre_close_2 子族扫描（pre-existing untracked）
    "tools/_test_carrier_upgrade.py",      # carrier_expand 离线验证（pre-existing untracked）
    "tools/_unlit_sweep.py",              # 未点亮塔攻坚（pre-existing untracked）
    "tools/_wide_probe.py",               # 全集字段宽探针（pre-existing untracked）
)


def default_db_path(workspace_root: Optional[str] = None) -> str:
    """与 ``wqb.store._common.default_db_path`` 同口径的 DB 路径解析。

    优先级：``WQB_DB_PATH`` 环境变量 > workspace_root > 向上探测仓库根 >
    cwd/data/wqb.db。
    """
    env = os.environ.get("WQB_DB_PATH")
    if env:
        return env
    if workspace_root:
        return str(Path(workspace_root) / _DEFAULT_REL)
    here = Path(__file__).resolve()
    for parent in here.parents:
        cand = parent / _DEFAULT_REL
        if cand.exists() or (parent / "src" / "wqb").is_dir():
            return str(parent / _DEFAULT_REL)
    return str(Path.cwd() / _DEFAULT_REL)


def production_db_path() -> str:
    """本仓库的生产库绝对路径（``<仓库根>/data/wqb.db``）；探不到仓库根则返回空串。

    与 :func:`default_db_path` 用同一对标记向上探测，但**刻意不看 `WQB_DB_PATH`**：
    本函数的职责就是回答「哪个路径是生产库」，环境变量是待检对象而不是判据。
    """
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            return str(parent / _DEFAULT_REL)
    return ""


def reject_production_db_under_tests(path: Any, *, entry: str) -> None:
    """结果层硬闸：**pytest 运行期间**不得拿生产 ``data/wqb.db`` 的**可写**连接。

    为什么在 ``wqb_db_mcp`` 之外还要有一份（2026-10-14 实测补，AGENTS.md §8.4 第 9 项）：
    那份闸只挂在 MCP 门面的 ``get_db_path()`` 上，而 **tools/ 与 toolkit 的直写路径走
    ``wqb.store.CampaignStore``，不经门面**。于是同一类失效（隔离静默不起作用 → 写生产库）
    在门面被守住之后**照样发生**：本次全量回归期间，``tests/unit/04_gates/
    test_inspect_mode_failclosed_p1p1.py`` 用 subprocess 起 ``tools/wave_gate.py``，
    子进程拿的是 CLI 缺省库位（生产 ``data/wqb.db``），实测往 ``ledger_kv`` 写了
    ``KOR/gate_ws2_pytest_inspect_model109`` 一行（``updated_at=2026-10-14T23:27:21``）。
    该键在库里已存在三份同期测试件（2026-09-28 / 10-03 / 10-04），说明这一类**不是第一次**，
    按 §4 第 7 条必须机械拦住而不是靠人记。

    ⚠ **判据必须是「与仓库根那个生产库同一个文件」，不是「以 `/data/wqb.db` 结尾」**。
    第一版就是写成后缀匹配的，实测把 **27 个用例打成 ERROR、5 个 FAILED**：本仓大量用例
    用 `tmp_path/ws/data/wqb.db` 这种**已经正确隔离**的临时库（目录结构刻意仿生产布局，
    例如 `CampaignStore.from_workspace(tmp)`），后缀匹配把它们全认成了生产库 —— 闸的
    失效方向从「静默写生产」变成「把隔离好的测试全砸了」，一样不可用。
    现判据 = `os.path.samefile` 级别的路径归一比较（`normcase(realpath)`），
    盘符/分隔符/大小写三种写法都覆盖，且临时库天然不相等。

    为什么闸在**构造连接**时而不是 ``commit()`` 时：``PRAGMA journal_mode=WAL`` 是持久化的
    库级属性（见 :func:`connect` 的 ``readonly`` 说明），门店一开就已经改库文件字节；
    且 ``ensure_schema()`` 会 ``CREATE TABLE``。等到 commit 才拦，隔离失效已经落了地。

    放行口径与门面**保持一致**（同一套语义才不会出现「门面拦、store 放」）：
      - 不在 pytest 下 ⇒ 不管（生产服务/CLI 正常写库是设计内行为）；
      - ``WQB_ALLOW_REAL_DB=1`` ⇒ 放行（要绕过就得在测试里写明理由，不会静默通过）；
      - 探不到仓库根 ⇒ 无从判定，**放行而不是猜**（本函数只在「确认是生产库」时才有拦截权）；
      - 其他一律走 ``WQB_DB_PATH`` 或显式传临时库路径。
    """
    if "PYTEST_CURRENT_TEST" not in os.environ:
        return
    if os.environ.get("WQB_ALLOW_REAL_DB") == "1":
        return
    prod = production_db_path()
    if not prod or not path:
        return
    if os.path.normcase(os.path.realpath(str(path))) != os.path.normcase(os.path.realpath(prod)):
        return
    raise RuntimeError(
        f"测试运行中 {entry} 指向生产库 {path} —— 隔离未生效，拒绝打开可写连接。"
        "临时库请传 CampaignStore(tmp_path) 或设 WQB_DB_PATH"
        "（子进程用 env 注入，见 tests/unit/04_gates/test_inspect_mode_failclosed_p1p1.py 的 "
        "_run_wave_gate）；确需读写真库请显式 monkeypatch.setenv('WQB_ALLOW_REAL_DB', '1') 并写明理由。")


def connect(
    db: Optional[str] = None,
    timeout: float = 60.0,
    row_factory: Any = None,
    readonly: bool = False,
    check_same_thread: Optional[bool] = None,
) -> sqlite3.Connection:
    """打开一个符合全库规范的 wqb.db 连接。

    Args:
        db: DB 路径；缺省走 :func:`default_db_path`（测试可传临时路径）。
        timeout: sqlite3 连接层 timeout（秒），同时写入 ``busy_timeout``。
            60s 覆盖已知的全部短事务竞争窗口；长事务应由
            ``wqb.store.db_write_mutex`` 调度而非拉长本参数。
        row_factory: 可选（如 ``sqlite3.Row``）。
        readonly: **只读工具必须传 True**（2026-09-20 补：step_funnel 只读契约）。
            置 True 时以 ``mode=ro`` URI 打开，并**跳过会改写库文件的
            ``PRAGMA journal_mode=WAL``**——WAL 是持久化的库级属性，一旦设置
            即使不写任何行也会改变 DB 文件字节，破坏
            ``tests/unit/test_step_funnel_p5.py::test_run_does_not_modify_db``。
        check_same_thread: 是否允许跨线程共用本连接。``None``（缺省）= 用 sqlite3 默认
            （True，禁止跨线程）。**共享型 store（``CampaignStore``，被 MCP 服务跨
            线程共用）必须显式传 ``False``**，否则会抛
            ``SQLite objects created in a thread can only be used in that same thread``。
            ⚠ 只读 URI 模式不支持该参数（sqlite3 不接受 URI 形式的 check_same_thread），
            故只读连接恒为默认值——只读场景通常单线程使用，不影响。

    Returns:
        已应用规范 PRAGMA 的 ``sqlite3.Connection``。
    """
    path = db or default_db_path()
    if readonly:
        # as_uri() 正确处理 Windows 盘符、反斜杠与空格。
        conn = sqlite3.connect(f"{Path(path).as_uri()}?mode=ro", uri=True, timeout=timeout)
    else:
        kwargs: Dict[str, Any] = {"timeout": timeout}
        if check_same_thread is not None:
            kwargs["check_same_thread"] = check_same_thread
        conn = sqlite3.connect(path, **kwargs)
    if row_factory is not None:
        conn.row_factory = row_factory
    conn.execute("PRAGMA foreign_keys=ON")
    if not readonly:
        # journal_mode=WAL 幂等且持久化（库级）；只读连接必须跳过，否则改库字节。
        conn.execute("PRAGMA journal_mode=WAL")
    # busy_timeout 与连接 timeout 同口径（连接级，只读同样适用）。
    conn.execute(f"PRAGMA busy_timeout={int(timeout * 1000)}")
    if not readonly:
        conn.execute("PRAGMA synchronous=NORMAL")
    return conn
