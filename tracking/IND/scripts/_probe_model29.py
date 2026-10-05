"""model29(id=1376) 字段侦查：全部字段 + coverage + user/alpha count，按 coverage 排序找高覆盖 sibling。"""
import sys

sys.path.insert(0, "src")
from wqb.region_catalog import RegionCatalog  # noqa: E402

rc = RegionCatalog()
fs = rc._conn.execute(
    "SELECT field_name, field_type, coverage, user_count, alpha_count, description "
    "FROM fields WHERE dataset_id=1376 ORDER BY coverage DESC",
).fetchall()
print(f"model29 (IND) total {len(fs)} fields\n")
print(f"{'field_name':<46} {'cov':<8} {'uc':<6} {'ac':<6} type      description")
for f in fs:
    d = (f["description"] or "").replace("\n", " ")[:64]
    cov = f["coverage"]
    print(f"{f['field_name']:<46} {cov if cov is not None else '-':<8} "
          f"{f['user_count'] if f['user_count'] is not None else '-':<6} "
          f"{f['alpha_count'] if f['alpha_count'] is not None else '-':<6} "
          f"{str(f['field_type'])[:7]:<9} {d}")

print("\n=== forecast_deviation* 家族 ===")
for f in fs:
    if "forecast_deviation" in (f["field_name"] or ""):
        print(f"  {f['field_name']:<46} cov={f['coverage']} uc={f['user_count']} ac={f['alpha_count']}")
