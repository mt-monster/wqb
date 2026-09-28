"""Validate reviewed experiment identities; selection remains in build_wave."""
from __future__ import annotations


def bind_selection_contract(contract, rows, *, region, dataset, wave, delay,
                            source_wave, capacity, expected_count=None):
    """Fail closed before selection; never revive archived or simulated sources."""
    def fail(reason):
        raise ValueError(f"[selection-contract] {reason}")

    if not isinstance(contract, dict):
        fail("missing or invalid ledger value")
    for key, actual in (("region", region), ("dataset", dataset),
                        ("wave", str(wave)), ("delay", delay)):
        if contract.get(key) != actual:
            fail(f"{key} mismatch: planned={contract.get(key)!r} actual={actual!r}")
    planned_source = contract.get("source_wave")
    if not isinstance(planned_source, str) or not planned_source:
        fail("source_wave required")
    if source_wave and source_wave != planned_source:
        fail("source_wave mismatch")
    required = contract.get("required")
    if not isinstance(required, list) or not required:
        fail("nonempty required list needed")
    if capacity < len(required):
        fail(f"capacity={capacity} below required={len(required)}; split/review plan explicitly")
    if expected_count is not None and expected_count != len(required):
        fail("expected-count conflicts with required list")
    by_id = {r["id"]: r for r in rows}
    ids, identities, roles = set(), set(), set()
    for item in required:
        if not isinstance(item, dict):
            fail("required item must be an object")
        sid = item.get("source_id")
        if type(sid) is not int or sid in ids:
            fail(f"invalid/duplicate source_id={sid!r}")
        if item.get("role") not in ("hypothesis", "control"):
            fail(f"source_id={sid} needs hypothesis/control role")
        if any(not isinstance(item.get(k), str) or not item[k].strip()
               for k in ("mechanism", "rationale", "expression")):
            fail(f"source_id={sid} needs mechanism, rationale and exact expression")
        role = (item["mechanism"], item["role"])
        if role in roles:
            fail(f"duplicate mechanism/role={role}; name distinct experimental questions")
        identity = "".join(item["expression"].split())
        if identity in identities:
            fail(f"duplicate expression at source_id={sid}")
        row = by_id.get(sid)
        if row is None:
            fail(f"source_id={sid} missing from source pool")
        if any(row.get(k) != v for k, v in (("region", region), ("dataset", dataset),
                                            ("wave", planned_source))):
            fail(f"source_id={sid} wrong provenance")
        if row.get("expression") != item["expression"]:
            fail(f"source_id={sid} expression changed; review plan again")
        if row.get("alpha_id") or row.get("status") not in ("gem", "pending", "enhanced", "selected"):
            fail(f"source_id={sid} protected status={row.get('status')} alpha_id={row.get('alpha_id')}")
        ids.add(sid)
        identities.add(identity)
        roles.add(role)
    return required
