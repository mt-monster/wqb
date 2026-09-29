# -*- coding: utf-8 -*-
"""selfcorr-quick 的 skill.py（skills 审查 SC-03 / SC-07 / SC-09）：

  · 不再依赖已被移除的 pkg_resources / 硬 import tqdm——缺依赖时给出可复制的安装命令，非交互环境不 input()；
  · 凭据只走环境变量（标准命名 CREDENTIALS_*，旧别名 BRAIN_* 兼容），--password 使用时告警；
  · 缓存池与 Excel 落在固定目录，而不是随 CWD；
  · 本地 SELF 偏低时给出「结构性盲区」警告，并带池的最后刷新时间。
"""
import importlib.util
import pickle
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "Claude" / "skills" / "brain-calculate-alpha-selfcorr-quick" / "scripts" / "skill.py"


@pytest.fixture(scope="module")
def sk():
    spec = importlib.util.spec_from_file_location("selfcorr_quick_skill_under_test", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)                   # 缺 tqdm / 无 pkg_resources 也必须能 import
    return mod


def test_module_imports_without_pkg_resources(sk):
    assert "pkg_resources" not in SCRIPT.read_text(encoding="utf-8").replace("不依赖已被移除的 pkg_resources", "")
    assert callable(sk.tqdm)


def test_version_tuple_and_missing_detection(sk, monkeypatch):
    assert sk._version_tuple("2.3.3.post1") == (2, 3, 3) and sk._version_tuple("2.0") == (2, 0)
    versions = {"requests": "2.34.2", "pandas": "2.3.3", "numpy": "1.20.0", "tqdm": None, "openpyxl": "3.1.5"}

    def fake_version(name):
        v = versions[name]
        if v is None:
            raise sk.importlib_metadata.PackageNotFoundError(name)
        return v

    monkeypatch.setattr(sk.importlib_metadata, "version", fake_version)
    assert sk.find_missing_requirements() == ["numpy>=1.24.0", "tqdm>=4.65.0"]


def test_missing_deps_in_non_interactive_shell_prints_command_and_never_prompts(sk, monkeypatch, capsys):
    monkeypatch.setattr(sk, "find_missing_requirements", lambda: ["tqdm>=4.65.0"])
    monkeypatch.setattr(sk.sys.stdin, "isatty", lambda: False, raising=False)
    monkeypatch.setattr("builtins.input", lambda *_: pytest.fail("非交互环境不得调用 input()"))
    assert sk.check_and_install_requirements() is False
    out = capsys.readouterr().out
    assert "pip install" in out and '"tqdm>=4.65.0"' in out and "非交互" in out


def test_credentials_prefer_env_and_warn_on_cli_password(sk):
    env = {"CREDENTIALS_EMAIL": "a@example.invalid", "CREDENTIALS_PASSWORD": "pw-env"}
    assert sk.resolve_credentials(environ=env) == ("a@example.invalid", "pw-env", [])
    legacy = {"BRAIN_USERNAME": "b@example.invalid", "BRAIN_PASSWORD": "pw-legacy"}
    assert sk.resolve_credentials(environ=legacy)[:2] == ("b@example.invalid", "pw-legacy")
    u, p, warns = sk.resolve_credentials("c@example.invalid", "pw-cli", environ={})
    assert (u, p) == ("c@example.invalid", "pw-cli") and warns and "环境变量" in warns[0]
    assert sk.resolve_credentials(environ={}) == ("", "", [])


def test_out_dir_is_fixed_not_cwd(sk, monkeypatch, tmp_path):
    monkeypatch.setenv("WQ_SELFCORR_OUT_DIR", str(tmp_path / "out"))
    assert sk.default_out_dir() == tmp_path / "out"
    monkeypatch.delenv("WQ_SELFCORR_OUT_DIR")
    monkeypatch.chdir(tmp_path)
    got = sk.default_out_dir()
    assert got == ROOT / "data" / "selfcorr_quick" and tmp_path not in got.parents      # 仓库内运行 → 固定在 data/（已 gitignore）


def test_pool_meta_reports_refresh_time_and_size(sk, tmp_path):
    assert sk.pool_meta(tmp_path) == {"pool_last_refreshed": None, "pool_alpha_count": None}
    (tmp_path / "os_alpha_pnls.pickle").write_bytes(pickle.dumps({}))
    (tmp_path / "os_alpha_ids.pickle").write_bytes(pickle.dumps({"IND": ["a", "b"], "USA": ["c"]}))
    meta = sk.pool_meta(tmp_path)
    assert meta["pool_alpha_count"] == 3 and meta["pool_last_refreshed"]


@pytest.mark.parametrize("value,expect_banner", [(0.229, True), (0.69, True), (0.7, False), (0.81, False), (None, False), (float("nan"), False)])
def test_blind_spot_banner_only_when_local_value_is_low(sk, value, expect_banner):
    banner = sk.blind_spot_banner(value)
    assert (banner is not None) is expect_banner
    if banner:
        assert "本地值低 ≠ 平台低" in banner and "提交前须平台实测" in banner
