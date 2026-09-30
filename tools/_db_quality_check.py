#!/usr/bin/env python3
"""DB quality audit: nulls, duplicates, FK integrity, cross-table consistency.

2026-09-30（P1）：改走 `wqb.db_conn.connect` 规范工厂，不再裸 sqlite3.connect。
裸连会绕过 WAL / busy_timeout=60s / foreign_keys=ON 口径，正是
`tests/unit/01_store_db/test_db_write_guards.py` 拦的 `database is locked` 根因。
从 __file__ 上溯到仓库根，换机器 / 云端容器不再指向不存在的盘符。
"""
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]  # tools/_db_quality_check.py -> repo root
sys.path.insert(0, str(REPO_ROOT / "src"))

from wqb.db_conn import connect  # noqa: E402

db = connect(row_factory=sqlite3.Row)  # row_factory 交给工厂，不事后改
cur = db.cursor()

tables = ['alphas','backtest_results','campaign_state','cross_region_lessons','datasets','expressions',
          'external_fields','field_profile','fields','gate_results','ledger_kv','regions','registry_empirical',
          'structural_variant_results','submission_ledger','submit_ready','wave_results','waves']

print("=" * 80)
print("六、数据完整性 - 空值统计（各表关键字段）")
print("=" * 80)

key_fields = {
    'alphas': ['alpha_id','expression','region_id','dataset_id','sharpe','fitness','status','platform_status','prod_correlation','self_correlation'],
    'backtest_results': ['alpha_id','status','sharpe','fitness','code','expression_id'],
    'expressions': ['expression','wave_id','status','sharpe','alpha_id','fingerprint','skeleton'],
    'submit_ready': ['alpha_id','region','expr','sharpe','fitness','gate','status'],
    'waves': ['region_id','wave_number','dataset_id','status'],
    'wave_results': ['region','wave_number','verdict','status'],
    'submission_ledger': ['alpha_id','region','submission_type','status'],
    'datasets': ['name','region_id','category','tier','status'],
    'fields': ['dataset_id','field_name','field_type','coverage'],
    'field_profile': ['dataset_id','field_name','coverage','skew'],
    'ledger_kv': ['region','key','value'],
    'registry_empirical': ['region','layer','entry_id','payload'],
    'regions': ['name','universe_legal','delay_legal'],
    'gate_results': ['region','wave','dataset','all_pass','report_json'],
    'campaign_state': ['region_id','current_wave','status'],
    'cross_region_lessons': ['lesson_id','family','finding','rule'],
    'external_fields': ['field_name','region','verified'],
    'structural_variant_results': ['region','wave_number','variant_id','original_expression','variant_expression','strategy'],
}

for t in tables:
    if t not in key_fields:
        continue
    cur.execute("SELECT COUNT(*) FROM " + t)
    total = cur.fetchone()[0]
    if total == 0:
        print(f"\n  {t}: 0 行（空表）")
        continue
    print(f"\n  {t} ({total} 行):")
    for col in key_fields[t]:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t} WHERE {col} IS NULL OR {col}=''")
            null_cnt = cur.fetchone()[0]
            if null_cnt > 0:
                pct = null_cnt * 100.0 / total
                print(f"    {col:<25} 空值 {null_cnt:>6} ({pct:>5.1f}%)")
        except:
            pass

print("\n" + "=" * 80)
print("七、数据完整性 - 重复数据检查")
print("=" * 80)

unique_checks = [
    ('alphas', 'alpha_id', 'alpha_id 应唯一'),
    ('submit_ready', 'alpha_id, region', 'alpha_id+region 应唯一'),
    ('expressions', 'wave_id, expression', 'wave_id+expression 应唯一'),
    ('waves', 'region_id, wave_number', 'region_id+wave_number 应唯一'),
    ('wave_results', 'region, wave_number', 'region+wave_number 应唯一'),
    ('datasets', 'name, region_id', 'name+region_id 应唯一'),
    ('fields', 'dataset_id, field_name', 'dataset_id+field_name 应唯一'),
    ('field_profile', 'dataset_id, field_name', 'dataset_id+field_name 应唯一'),
    ('submission_ledger', 'alpha_id, submitted_at', 'alpha_id+submitted_at 应唯一'),
    ('ledger_kv', 'region, key', 'region+key 应唯一'),
    ('regions', 'name', 'name 应唯一'),
    ('registry_empirical', 'region, layer, entry_id', 'region+layer+entry_id 应唯一'),
    ('gate_results', 'region, wave, dataset', 'region+wave+dataset 应唯一'),
    ('cross_region_lessons', 'lesson_id', 'lesson_id 应唯一'),
    ('structural_variant_results', 'region, wave_number, variant_id', 'region+wave_number+variant_id 应唯一'),
]

for table, cols, desc in unique_checks:
    try:
        cur.execute(f"SELECT {cols}, COUNT(*) c FROM {table} GROUP BY {cols} HAVING c > 1")
        dups = cur.fetchall()
        if dups:
            print(f"  {table}: {desc} -> {len(dups)} 组重复")
            for d in dups[:3]:
                print(f"    {dict(d)}")
        else:
            print(f"  {table}: {desc} -> OK")
    except Exception as e:
        print(f"  {table}: {desc} -> 检查失败: {e}")

print("\n" + "=" * 80)
print("八、数据完整性 - 外键关联检查")
print("=" * 80)

fk_checks = [
    ('alphas', 'region_id', 'regions', 'id'),
    ('alphas', 'dataset_id', 'datasets', 'id'),
    ('backtest_results', 'expression_id', 'expressions', 'id'),
    ('expressions', 'wave_id', 'waves', 'id'),
    ('waves', 'region_id', 'regions', 'id'),
    ('waves', 'dataset_id', 'datasets', 'id'),
    ('fields', 'dataset_id', 'datasets', 'id'),
    ('field_profile', 'dataset_id', 'datasets', 'id'),
    ('campaign_state', 'region_id', 'regions', 'id'),
    ('wave_results', 'region_id', 'regions', 'id'),
]

for child, col, parent, pcol in fk_checks:
    try:
        sql = f"SELECT COUNT(*) FROM {child} c LEFT JOIN {parent} p ON c.{col}=p.{pcol} WHERE c.{col} IS NOT NULL AND p.{pcol} IS NULL"
        cur.execute(sql)
        orphans = cur.fetchone()[0]
        if orphans > 0:
            print(f"  {child}.{col} -> {parent}.{pcol}: {orphans} 孤儿记录")
            cur.execute(f"SELECT DISTINCT c.{col} FROM {child} c LEFT JOIN {parent} p ON c.{col}=p.{pcol} WHERE c.{col} IS NOT NULL AND p.{pcol} IS NULL LIMIT 5")
            vals = [r[0] for r in cur.fetchall()]
            print(f"    示例值: {vals}")
        else:
            print(f"  {child}.{col} -> {parent}.{pcol}: OK")
    except Exception as e:
        print(f"  {child}.{col} -> {parent}.{pcol}: 检查失败: {e}")

print("\n" + "=" * 80)
print("九、数据完整性 - 跨表一致性检查")
print("=" * 80)

# alphas vs submit_ready
cur.execute("SELECT COUNT(*) FROM alphas a LEFT JOIN submit_ready s ON a.alpha_id=s.alpha_id WHERE a.platform_status IN ('ACTIVE','DEOMMISSIONED') AND s.alpha_id IS NULL")
print(f"  已提交 alpha 不在 submit_ready: {cur.fetchone()[0]}")

cur.execute("SELECT COUNT(*) FROM submit_ready s LEFT JOIN alphas a ON s.alpha_id=a.alpha_id WHERE a.alpha_id IS NULL")
print(f"  submit_ready 中 alpha 不在 alphas 表: {cur.fetchone()[0]}")

# expressions vs backtest_results
cur.execute("SELECT COUNT(*) FROM expressions e LEFT JOIN backtest_results b ON e.id=b.expression_id WHERE b.id IS NULL")
print(f"  expressions 无 backtest_results: {cur.fetchone()[0]}")

cur.execute("SELECT COUNT(*) FROM backtest_results b LEFT JOIN expressions e ON b.expression_id=e.id WHERE e.id IS NULL")
print(f"  backtest_results 无 expressions: {cur.fetchone()[0]}")

# waves vs expressions
cur.execute("SELECT COUNT(*) FROM waves w LEFT JOIN expressions e ON w.id=e.wave_id WHERE e.id IS NULL")
print(f"  waves 无 expressions: {cur.fetchone()[0]}")

# datasets vs fields
cur.execute("SELECT COUNT(*) FROM datasets d LEFT JOIN fields f ON d.id=f.dataset_id WHERE f.id IS NULL")
print(f"  datasets 无 fields: {cur.fetchone()[0]}")

# alphas vs submission_ledger
cur.execute("SELECT COUNT(*) FROM submission_ledger sl LEFT JOIN alphas a ON sl.alpha_id=a.alpha_id WHERE a.alpha_id IS NULL")
print(f"  submission_ledger 中 alpha 不在 alphas: {cur.fetchone()[0]}")

# Check status consistency between alphas and submit_ready
cur.execute("""
    SELECT a.alpha_id, a.platform_status, s.status
    FROM alphas a JOIN submit_ready s ON a.alpha_id=s.alpha_id
    WHERE (a.platform_status='ACTIVE' AND s.status NOT IN ('SUBMITTED','BLOCKED'))
       OR (a.platform_status='UNSUBMITTED' AND s.status='SUBMITTED')
    LIMIT 10
""")
mismatches = cur.fetchall()
print(f"  alphas vs submit_ready 状态不一致: {len(mismatches)} 颗")
for m in mismatches:
    print(f"    {m[0]}: platform={m[1]} vs queue={m[2]}")

print("\n" + "=" * 80)
print("十、数据完整性 - 数据量统计与异常值检查")
print("=" * 80)

# Check for anomalous values
print("  异常值检查:")

# alphas with extreme sharpe
cur.execute("SELECT alpha_id, sharpe, status FROM alphas WHERE sharpe > 10 OR sharpe < -10 ORDER BY sharpe DESC LIMIT 10")
extreme = cur.fetchall()
if extreme:
    print(f"  alphas 极端 sharpe (>10 or <-10): {len(extreme)} 颗")
    for r in extreme:
        print(f"    {r[0]}: sharpe={r[1]} status={r[2]}")

# alphas with null sharpe
cur.execute("SELECT COUNT(*) FROM alphas WHERE sharpe IS NULL")
print(f"  alphas sharpe=NULL: {cur.fetchone()[0]}")

# alphas with null fitness
cur.execute("SELECT COUNT(*) FROM alphas WHERE fitness IS NULL")
print(f"  alphas fitness=NULL: {cur.fetchone()[0]}")

# expressions with null sharpe
cur.execute("SELECT COUNT(*) FROM expressions WHERE sharpe IS NULL")
print(f"  expressions sharpe=NULL: {cur.fetchone()[0]}")

# submit_ready with null sharpe
cur.execute("SELECT COUNT(*) FROM submit_ready WHERE sharpe IS NULL")
print(f"  submit_ready sharpe=NULL: {cur.fetchone()[0]}")

# Check for negative values in should-be-positive fields
cur.execute("SELECT COUNT(*) FROM alphas WHERE turnover < 0")
print(f"  alphas turnover<0: {cur.fetchone()[0]}")

cur.execute("SELECT COUNT(*) FROM alphas WHERE sharpe < 0 AND status='ACTIVE'")
print(f"  alphas ACTIVE but sharpe<0: {cur.fetchone()[0]}")

# Check for duplicate expressions across different alpha_ids
cur.execute("""
    SELECT expression, COUNT(DISTINCT alpha_id) as cnt
    FROM alphas
    GROUP BY expression
    HAVING cnt > 1
    ORDER BY cnt DESC
    LIMIT 10
""")
dup_exprs = cur.fetchall()
print(f"\n  alphas 中相同 expression 对应多个 alpha_id: {len(dup_exprs)} 组")
for r in dup_exprs:
    print(f"    expr={r[0][:80]}... -> {r[1]} 个 alpha_id")

db.close()
print("\n完成。")
