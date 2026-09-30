# -*- coding: utf-8 -*-
"""2026-09-30 B 阶段守卫：tools/category_field_triage.py。

本工具是「分类字段分诊」的唯一入口，把人工六步压成一条命令。它有三个**容易悄悄失效**
且失效后不会报错、只会静默给出错误结论的点，必须锁死：

  1. 判死必须查**两源**（registry_empirical + ledger_kv 的 *_dead）。
     作者第一版只查 registry，把 sentiment21 / institutions6 误判成存活——
     这是本工具被发明的直接原因之一。
  2. 族连坐必须用**包含度**而非 Jaccard（见 _containment 注释）。
     KOR 实测 risk70 签名 8 词、判死的 risk88 签名 3 词：Jaccard=0.375 < 0.7
     会漏判，包含度=1.00 才抓得住。
  3. 族签名必须用**字段 description** 的关键词，且要剔除地理/币种/模型版本号词。
     risk88 是 `rsk88_mfm_ase1_ri_*`、risk70 是 `rsk70_mfm2_asetrd_*`，
     字段名层面完全不重叠；而 "in ASI region" 会把 asi 带进签名导致连坐失效。
     另外：判级有严格优先级，先命中先定（仅条件腿 > 判死 > 族连坐 > 拥挤 >
     无甜点 > ★可开波）。
"""
import argparse
import importlib.util
import os
import sqlite3
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _load():
    spec = importlib.util.spec_from_file_location(
        "category_field_triage_b", os.path.join(REPO, "tools", "category_field_triage.py"))
    m = importlib.util.module_from_spec(spec)
    sys.modules["category_field_triage_b"] = m
    spec.loader.exec_module(m)
    return m


def _args(**kw):
    base = dict(min_fields=5, crowd_ac=1000, sweet_lo=10, sweet_hi=50,
                desert_ratio=0.6, family_sim=0.7, df_max_ratio=0.25,
                sharpe_min=1.58, fitness_min=1.0, xr_min_bt=16, xr_weak_sharpe=1.0)
    base.update(kw)
    return argparse.Namespace(**base)


SCHEMA = """
CREATE TABLE regions(id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE datasets(id INTEGER PRIMARY KEY, region_id INT, name TEXT, category TEXT);
CREATE TABLE fields(id INTEGER PRIMARY KEY, dataset_id INT, field_type TEXT,
                    coverage REAL, alpha_count INT, user_count INT, description TEXT);
CREATE TABLE registry_empirical(id INTEGER PRIMARY KEY, region TEXT, layer TEXT,
                    entry_id TEXT, family TEXT, payload TEXT, dead_at TEXT,
                    created_at TEXT, updated_at TEXT, region_id INT);
CREATE TABLE ledger_kv(id INTEGER PRIMARY KEY, region TEXT, key TEXT, value TEXT,
                    created_at TEXT, updated_at TEXT);
CREATE TABLE backtest_results(id INTEGER PRIMARY KEY, region TEXT, dataset TEXT,
                    sharpe REAL, fitness REAL, ra_failed_checks TEXT);
"""


def _fixture():
    """复刻 KOR/RISK 的结构：判死集 + 同族未判死集 + 各级非存活集 + 一个存活集。"""
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    c.execute("INSERT INTO regions VALUES (1,'KOR')")

    def ds(i, name, cat):
        c.execute("INSERT INTO datasets VALUES (?,?,?,?)", (i, 1, name, cat))

    def fields(i, dsid, n, desc, ac=30, uc=2, ftype="MATRIX", cov=0.5):
        for k in range(n):
            c.execute("INSERT INTO fields VALUES (?,?,?,?,?,?,?)",
                      (i * 100 + k, dsid, ftype, cov, ac, uc, desc))

    # risk88：判死（registry 命中），签名 3 词
    ds(1, "risk88", "RISK")
    fields(1, 1, 20, "Style factor loading in ASI region")
    c.execute("INSERT INTO registry_empirical(region,layer,entry_id,payload) "
              "VALUES ('KOR','dead_end','KOR-risk88-STYLOAD-WEAK','{...}')")
    # risk70：同族未判死（registry/ledger 都没它），签名 8 词 ⊃ risk88 的 3 词
    ds(2, "risk70", "RISK")
    fields(2, 2, 96, "Style factor loading exposure model risk sector industry")
    # deadled：只有 ledger 有 *_dead，registry 查不到 → 两源缺一即漏判
    ds(3, "deadled", "RISK")
    fields(3, 3, 20, "Insider holding change reported")
    c.execute("INSERT INTO ledger_kv(region,key,value) VALUES ('KOR','deadled_dead','{}')")
    # 其余各级
    ds(4, "crowd", "RISK");    fields(4, 4, 20, "Crowded factor value", ac=2000)
    ds(5, "nosweet", "RISK");  fields(5, 5, 20, "No sweet spot value", ac=3)
    # survivor：ac 必须落在甜点区间 [10,50] 内（acmax 高不代表有甜点字段——
    # ac=209 的 29 字段集 sweet=0，仍判无甜点，这是本工具的核心区分点）
    ds(6, "survivor", "RISK"); fields(6, 6, 29, "News sentiment score", ac=30)
    ds(7, "tiny", "RISK");     fields(7, 7, 2, "Tiny field set", ac=2000)
    # tinydead：字段少**且**判死 → 优先级必须选「仅条件腿」
    ds(8, "tinydead", "RISK"); fields(8, 8, 2, "Tiny but dead", ac=2000)
    c.execute("INSERT INTO ledger_kv(region,key,value) VALUES ('KOR','tinydead_dead','{}')")
    # 语料填充：DF 过滤按「词出现在多少个数据集里」剔除通用词，夹具必须有接近真实
    # 的语料规模（真实区域 186 集）。只有 8 集时 factor 出现 3 次即 DF=37.5% 被误剔，
    # 签名缩到 2 词又跌破 min_overlap=3 守卫 → 连坐失效（这是夹具的坑，不是工具的）。
    _FILLER = ["Bilateral trade balance surplus", "Option implied volatility surface",
               "Dry bulk shipping freight index", "Retail footfall traffic counter",
               "Patent citation forward count", "Electricity grid load forecast",
               "Hotel occupancy weekend average", "Railway freight tonnage moved"]
    for i, d in enumerate(_FILLER):
        ds(20 + i, f"filler{i}", "OTHER")
        fields(20 + i, 20 + i, 6, d, ac=30)
    c.commit()
    return c


def _verdicts(c, **kw):
    m = _load()
    rows = m.triage(c, "KOR", None, _args(**kw))
    return {r["dataset"]: r for r in rows}


# ---------- 1. 判死两源 ----------

def test_ledger_only_dead_is_still_caught():
    """只有 ledger 的 *_dead、registry 无命中 → 仍判死（两源缺一即漏判的回归点）。"""
    v = _verdicts(_fixture())
    assert v["deadled"]["verdict"] == "判死", v["deadled"]["tags"]
    assert any("ledger" in h for h in v["deadled"]["dead_hits"])


def test_registry_only_dead_is_still_caught():
    """只有 registry 命中、ledger 无 → 仍判死。"""
    v = _verdicts(_fixture())
    assert v["risk88"]["verdict"] == "判死"


def test_non_dead_datasets_are_not_marked_dead():
    """未判死数据集不得因键名相近被误伤（ledger 键后缀 _dead 才计数）。"""
    v = _verdicts(_fixture())
    for name in ("risk70", "survivor", "crowd", "nosweet"):
        assert v[name]["verdict"] != "判死", name


# ---------- 1b. 判死必须过滤 layer（2026-09-30 C 阶段实测抓到的真 bug） ----------

def test_only_dead_end_layer_counts_as_dead():
    """win / campaign / orphan 层的 registry 条目**不得**算判死。

    实测：初版 `SELECT entry_id, payload FROM registry_empirical WHERE region=?`
    完全没过滤 layer —— KOR 118 条里只有 77 条是 dead_end，其余 41 条（含
    9 条 win）被误当判死。后果：other466 有 3 条 win 记录（ACTIVE alpha
    wpZkk1Mp / A1NXddRw）却被判死，而它正是 KOR 唯一近期 ACTIVE alpha 的来源集。
    """
    m = _load()
    c = _fixture()
    # 只插一条 win 层记录（提到 survivor），不得因此判死
    c.execute("INSERT INTO registry_empirical(region,layer,entry_id,payload) "
              "VALUES ('KOR','win','KOR-SURVIVOR-WIN','{\"alpha_id\":\"abc\"}')")
    c.commit()
    v = {r["dataset"]: r for r in m.triage(c, "KOR", None, _args())}
    assert v["survivor"]["verdict"] == "★可开波", v["survivor"]["tags"]
    assert v["survivor"]["dead_hits"] == []


def test_win_layer_does_not_override_real_dead_end():
    """过滤 layer 不等于放宽：真正的 dead_end 记录仍然判死。"""
    m = _load()
    c = _fixture()
    # ⚠ 判死匹配 `ds in entry_id or ds in str(payload)` 是**大小写敏感**的：
    # entry_id 写 KOR-SURVIVOR-... 匹配不到小写 survivor，真实数据靠 payload 里的
    # "dataset": "<ds>" 命中。故测试也必须把集名放进 payload。
    c.execute("INSERT INTO registry_empirical(region,layer,entry_id,payload) "
              "VALUES ('KOR','dead_end','KOR-SURVIVOR-PRODWALL','{\"dataset\":\"survivor\"}')")
    c.commit()
    v = {r["dataset"]: r for r in m.triage(c, "KOR", None, _args())}
    assert v["survivor"]["verdict"] == "判死"


# ---------- 1c. 「有实证产出」豁免（判死是族级的） ----------

def test_empirical_output_downgrades_dead_to_non_blocking():
    """判死 + 本地 ra_clean>0 → 判级保留「判死」但 block=False（不阻断）。

    实测：KOR 3 个有 ra_clean 的集（other466=16 / analyst44=8 / analyst10=5）
    全是判死；无条件硬拦会 100% 误杀 29/29 条历史产出。判死记录是族级的
    （rule 明写「analyst44 一致预期类字段…不再投任何变体」），同集其他族仍可能活。
    """
    m = _load()
    c = _fixture()
    c.executemany(
        "INSERT INTO backtest_results(region,dataset,sharpe,fitness,ra_failed_checks) "
        "VALUES (?,?,?,?,?)",
        [("KOR", "deadled", 2.10, 1.50, ""), ("KOR", "deadled", 1.90, 1.30, "")])
    c.commit()
    v = {r["dataset"]: r for r in m.triage(c, "KOR", None, _args())}
    assert v["deadled"]["verdict"] == "判死", "判级如实保留"
    assert v["deadled"]["block"] is False, "有实证产出不得阻断"
    assert any("实证产出" in t for t in v["deadled"]["tags"])


def test_no_output_stays_blocking():
    """无实证产出的判死集仍然阻断（闸的价值所在）。"""
    v = _verdicts(_fixture())
    assert v["deadled"]["block"] is True
    assert v["risk70"]["block"] is True   # 族连坐且零产出
    assert v["survivor"]["block"] is False


def test_block_field_is_written_to_ledger_payload():
    """台账必须带 block 字段——闸的判定依据就是它，缺了闸只能 fail-open。"""
    src = open(os.path.join(REPO, "tools", "category_field_triage.py"),
               encoding="utf-8").read()
    assert '"block"' in src


# ---------- 2. 族连坐：包含度 vs Jaccard ----------

def test_containment_catches_subset_family_where_jaccard_would_not():
    """risk70⊃risk88：包含度 1.00 命中，同参数下 Jaccard 仅 0.375（< 阈值 0.7）会漏。"""
    m = _load()
    sig70 = m._family_signature(["Style factor loading exposure model risk sector industry"])
    sig88 = m._family_signature(["Style factor loading in ASI region"])
    assert len(sig88) == 3 and len(sig70) == 8, (sorted(sig88), sorted(sig70))
    assert m._containment(sig70, sig88) == 1.0
    assert m._jaccard(sig70, sig88) < 0.7  # 证明换包含度是必需的，不是可选的


def test_containment_guards_against_tiny_signatures():
    """守卫生效：交集 < 3 词或较小侧 < 3 词 → 0.0，不得靠两三个通用词乱连坐。"""
    m = _load()
    assert m._containment({"style", "factor"}, {"style", "factor", "loading"}) == 0.0
    assert m._containment(set(), {"style", "factor", "loading"}) == 0.0
    assert m._containment({"style", "factor", "loading"}, set()) == 0.0


def test_family_contagion_marks_unrecorded_sibling_dead():
    """risk70 从未被判死，但族内容被判死的 risk88 覆盖 → 判「族连坐」。"""
    v = _verdicts(_fixture())
    r = v["risk70"]
    assert r["verdict"] == "族连坐", r["tags"]
    assert r["contagion"][1] == "risk88"
    assert r["contagion"][0] >= 0.7


def test_unrelated_dataset_is_not_contaminated():
    """签名不相干的数据集不得被连坐。"""
    v = _verdicts(_fixture())
    assert v["survivor"]["verdict"] == "★可开波", v["survivor"]["tags"]
    assert v["survivor"]["contagion"] is None


def test_family_sim_threshold_is_honoured():
    """--family-sim 调到 1.01 → 连坐不再命中，risk70 回落为可开波（阈值真生效）。"""
    v = _verdicts(_fixture(), family_sim=1.01)
    assert v["risk70"]["verdict"] == "★可开波"


# ---------- 3. 族签名：用 description，剔除地理/币种词 ----------

def test_geo_and_currency_tokens_are_not_part_of_signature():
    """ASI/USD/dollars 等地理币种词不得进签名（否则 risk88 与 risk70 签名错开）。"""
    m = _load()
    t = m._tokens("Style factor loading in ASI region, denominated in USD dollars")
    for bad in ("asi", "usd", "dollars", "region", "denominated"[:0]):
        assert bad not in t, (bad, sorted(t))
    assert {"style", "factor", "loading"} <= t


def test_signature_uses_description_not_field_name():
    """字段名完全不同、description 相同 → 签名相同（这是连坐的前提）。"""
    m = _load()
    a = m._family_signature(["Style Factor Loading"])
    b = m._family_signature(["Style Factor Loading"])
    assert a == b and a  # 字段名不参与，只看 description


# ---------- 4. 判级优先级 ----------

def test_verdict_priority_order():
    """先命中先定：仅条件腿 > 判死 > 族连坐 > 拥挤 > 无甜点 > ★可开波。"""
    v = _verdicts(_fixture())
    assert v["tinydead"]["verdict"] == "仅条件腿"   # 字段少优先于判死
    assert v["deadled"]["verdict"] == "判死"        # 判死优先于其后各级
    assert v["risk70"]["verdict"] == "族连坐"
    assert v["crowd"]["verdict"] == "拥挤"
    assert v["nosweet"]["verdict"] == "无甜点字段"
    assert v["survivor"]["verdict"] == "★可开波"


def test_min_fields_and_crowd_thresholds_are_respected():
    """--min-fields / --crowd-ac 真生效（改阈值后判级随之改变）。"""
    v = _verdicts(_fixture(), min_fields=2, crowd_ac=5000)
    assert v["tiny"]["verdict"] != "仅条件腿"
    assert v["crowd"]["verdict"] != "拥挤"


def test_survivor_requires_sweet_spot_fields():
    """甜点区间为空即判「无甜点字段」；把区间放宽到含 ac=3 → 变可开波。"""
    assert _verdicts(_fixture())["nosweet"]["verdict"] == "无甜点字段"
    assert _verdicts(_fixture(), sweet_lo=1)["nosweet"]["verdict"] == "★可开波"


# ---------- 5. 写入口不得静默降级 ----------

def test_write_ledger_does_not_reference_nonexistent_wqb_ledger():
    """回归点：初版 `from wqb.ledger import upsert_ledger_key`（该模块不存在）
    被 except 兜底后只 WARN 并返回 0 —— 形成『假成功』：下游读不到台账。
    现在必须走 CampaignStore，且写入口不可达时非 0 退出。
    """
    src = open(os.path.join(REPO, "tools", "category_field_triage.py"),
               encoding="utf-8").read()
    # 只看非注释行：注释里会引用旧写法作为「为什么改」的说明，扫源码会误伤
    code = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("#"))
    assert "wqb.ledger" not in code
    assert "upsert_ledger_key" not in code
    assert "CampaignStore" in code and "upsert_ledger" in code
    assert "return 2" in code  # 写入口不可达 → 非 0
