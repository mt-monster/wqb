# -*- coding: utf-8 -*-
"""labs_field_profile_batch.py — BRAIN Labs 批量字段画像脚本（在 Labs JupyterLab 里运行）。

用途：无 WebDataScope 时，用 Labs 原始面板数据批量计算字段分布画像，
      输出与 WebDataScope 兼容的 shape 口径（zero_inflated/point_mass/ceiling/spread/concentrated），
      回填 data/wqb.db 的 field_profile 表。

运行方式：
  1. 在 BRAIN Labs（JupyterLab，`from brain import Brain` 可用）里粘贴本脚本并执行；
  2. 脚本把画像 JSON 写到 OUTPUT_PATH（默认 /tmp/field_profile_<dataset>_<region>.json）；
  3. 把该 JSON 拷回本机，用 tools/field_profile_from_labs.py 入库（ingest）。

设计说明：
  - VECTOR 字段：每天每股票多值，get_data_frame 返回后先 flatten 成一维取值序列再统计。
  - 分布形状映射（与 tools/webdata_quality.py classify_distribution 同口径）：
      zero_inflated: [0,0.1) 占比 > 50%
      point_mass:    单档占比 > 90%（近似常量/哑变量）
      ceiling:       [0.9,1] 占比 > 50%（截尾）
      concentrated:  前3档占比 > 70%
      spread:        其他（分布分散）
  - 只读统计，不仿真、不提交，不烧回测配额。
"""
import json
import numpy as np
import pandas as pd

# ---- 配置（按需修改） ----
DATASET_ID = "shortinterest3"
REGION = "KOR"
UNIVERSE = "TOP600"
DELAY = 1
# 要画像的字段（shortinterest3 全部 56 个字段，来自平台 get_datafields）。
FIELDS = [
    "available_market_value_usd",
    "available_market_value_usd_twn",
    "available_share_count",
    "available_share_count_twn",
    "average_loan_duration_days",
    "average_loan_duration_days_main",
    "average_loan_duration_days_p5_d1",
    "average_loan_duration_days_p5_twn",
    "borrow_activity_score",
    "borrow_activity_score_twn",
    "loan_rate_volatility",
    "loan_rate_volatility_main",
    "loan_rate_volatility_p5_d1",
    "loan_rate_volatility_p5_twn",
    "loan_utilization_ratio",
    "loan_utilization_ratio_d1",
    "loan_utilization_ratio_twn",
    "loan_utilization_ratio_u2_twn",
    "loaned_market_value_usd",
    "loaned_market_value_usd_main",
    "loaned_market_value_usd_p5_d1",
    "loaned_market_value_usd_p5_twn",
    "loaned_share_count",
    "loaned_share_count_main",
    "loaned_share_count_p5_d1",
    "loaned_share_count_p5_twn",
    "loaned_share_count_r2",
    "loaned_share_count_r2_d1",
    "loaned_share_count_r2_twn",
    "max_loan_rate",
    "max_loan_rate_main",
    "max_loan_rate_p5_d1",
    "max_loan_rate_p5_twn",
    "mean_loan_rate",
    "mean_loan_rate_main",
    "mean_loan_rate_p5_d1",
    "mean_loan_rate_p5_twn",
    "min_loan_rate",
    "min_loan_rate_main",
    "min_loan_rate_p5_d1",
    "min_loan_rate_p5_twn",
    "new_loaned_share_count",
    "new_loaned_share_count_d1",
    "new_loaned_share_count_twn",
    "rate_bin_lower_limit",
    "rate_bin_lower_limit_d1",
    "rate_bin_lower_limit_twn",
    "rate_bin_upper_limit",
    "rate_bin_upper_limit_d1",
    "rate_bin_upper_limit_twn",
    "shrt3_bar",
    "shrt3_utilizationpercent_units",
    "transaction_count",
    "transaction_count_main",
    "transaction_count_p5_d1",
    "transaction_count_p5_twn",
]
OUTPUT_PATH = f"/tmp/field_profile_{DATASET_ID}_{REGION}.json"

# 诊断探针：设为 True 时只对 DIAG_FIELD 打印 get_data_frame 返回结构（类型/形状/dtype/前几行），
# 用于排查 VECTOR 字段返回 None 的根因。排查完设回 False 跑全量。
DIAG_PROBE = False
DIAG_FIELD = "shrt3_bar"


def _diag_inspect(brain, field_id):
    """打印 get_data_field / get_data_frame 对单字段的返回结构（排查 None 根因）。"""
    print(f"===== DIAG {field_id} =====")
    # 1) get_data_field
    data_field = None
    try:
        data_field = brain.get_data_field(field_id)
        print(f"get_data_field OK: type={type(data_field).__name__}, "
              f"field.type={getattr(data_field, 'type', None)}")
    except Exception as exc:
        print(f"get_data_field FAILED: {exc}")
    # 2) get_data_frame(data_field)
    df = None
    if data_field is not None:
        try:
            df = brain.get_data_frame(data_field)
            print(f"get_data_frame(data_field) OK: type={type(df).__name__}")
        except Exception as exc:
            print(f"get_data_frame(data_field) FAILED: {exc}")
    # 3) fallback kwargs
    if df is None:
        for kwargs in (
            {"field_id": field_id, "dataset_id": DATASET_ID, "region": REGION, "universe": UNIVERSE, "delay": DELAY},
            {"field_id": field_id, "region": REGION, "universe": UNIVERSE, "delay": DELAY},
        ):
            try:
                df = brain.get_data_frame(**kwargs)
                print(f"get_data_frame({list(kwargs)[:1]}...) OK: type={type(df).__name__}")
                break
            except Exception as exc:
                print(f"get_data_frame({kwargs}) FAILED: {exc}")
    if df is None:
        print("=> df is None (所有途径都失败)")
        return
    # 结构检查
    try:
        import pandas as _pd
        if isinstance(df, _pd.DataFrame):
            print(f"DataFrame shape={df.shape}, dtypes={dict(df.dtypes.astype(str))}")
            print(f"columns[:5]={list(df.columns)[:5]}")
            print(f"head(2):\n{df.head(2)}")
            # cell 内容类型
            first = df.iloc[0, 0] if df.shape[0] and df.shape[1] else None
            print(f"first cell type={type(first).__name__}, value={repr(first)[:120]}")
        elif isinstance(df, _pd.Series):
            print(f"Series len={len(df)}, dtype={df.dtype}")
            print(f"head(3):\n{df.head(3)}")
        else:
            print(f"非 DataFrame/Series: {type(df).__name__}, repr={repr(df)[:200]}")
    except Exception as exc:
        print(f"inspect error: {exc}")
    # flatten 测试
    vals = _flatten_values(df)
    print(f"_flatten_values -> size={vals.size}, sample={vals[:5]}")

    # ---- 时间范围探测：get_data_frame 默认只返回 2 行，尝试拉更长 ----
    print("\n----- 时间范围探测 -----")
    try:
        import inspect as _inspect
        try:
            print(f"get_data_frame signature: {_inspect.signature(brain.get_data_frame)}")
        except Exception as e:
            print(f"signature unavailable: {e}")
        doc = (brain.get_data_frame.__doc__ or "")
        if doc:
            print(f"get_data_frame doc: {doc[:400]}")
    except Exception:
        pass
    # 尝试常见时间参数拉更长序列
    for extra in (
        {"start_date": "2018-01-01", "end_date": "2023-12-31"},
        {"days": 1260},
        {"limit": 1260},
        {"lookback": 1260},
    ):
        try:
            kw = {"field_id": field_id, "dataset_id": DATASET_ID, "region": REGION,
                  "universe": UNIVERSE, "delay": DELAY}
            kw.update(extra)
            df2 = brain.get_data_frame(**kw)
            n = df2.shape[0] if hasattr(df2, "shape") else len(df2)
            print(f"  get_data_frame(+{list(extra)[0]}) -> rows={n}")
            if n and n > 2:
                print(f"  >>> 成功拉长时间: {list(extra)[0]} 参数有效, rows={n}")
                break
        except Exception as e:
            print(f"  get_data_frame(+{list(extra)[0]}) FAILED: {str(e)[:120]}")


def _flatten_values(df):
    """把 get_data_frame 返回（MATRIX 或 VECTOR）压成一维有限取值序列。

    VECTOR 字段：DataFrame 每个 cell 是 ndarray（如 array([9])，一天多笔）或 None。
    需逐 cell 展开：ndarray/list → 取所有有限元素；标量 → 直接取；None/NaN → 跳过。
    MATRIX 字段：cell 是标量，同样兼容。
    """
    if df is None:
        return np.array([])
    out = []
    try:
        # DataFrame / Series → 逐 cell 处理（兼容 cell 为 ndarray 的 VECTOR 结构）
        if isinstance(df, pd.DataFrame):
            iterator = (df.iloc[r, c] for r in range(df.shape[0]) for c in range(df.shape[1]))
        elif isinstance(df, pd.Series):
            iterator = iter(df.tolist())
        else:
            iterator = iter(np.asarray(df).ravel())
        for cell in iterator:
            if cell is None:
                continue
            # cell 是 ndarray / list / tuple（VECTOR：一天多值）
            if isinstance(cell, (np.ndarray, list, tuple)):
                for x in np.asarray(cell, dtype=object).ravel():
                    try:
                        v = float(x)
                    except (TypeError, ValueError):
                        continue
                    if np.isfinite(v):
                        out.append(v)
            else:
                # cell 是标量（MATRIX 或单值）
                try:
                    v = float(cell)
                except (TypeError, ValueError):
                    continue
                if np.isfinite(v):
                    out.append(v)
    except Exception:
        return np.array([])
    return np.asarray(out, dtype=float)


def _shape_of(values):
    """与 WebDataScope classify_distribution 同口径的 5 类形状判定。"""
    if values.size == 0:
        return "unknown", {}
    vmin, vmax = float(np.min(values)), float(np.max(values))
    rng = vmax - vmin
    if rng <= 0:
        return "point_mass", {"reason": "constant"}
    # 归一化到 [0,1] 后按分位段统计（模拟 yearly_distribution 的 20 档直方图）
    norm = (values - vmin) / rng
    bins = np.linspace(0, 1, 21)
    hist, _ = np.histogram(norm, bins=bins)
    total = hist.sum()
    if total <= 0:
        return "unknown", {}
    freq = hist / total
    top_share = float(freq.max())
    low_tail = float(freq[:2].sum())   # [0,0.1)
    high_tail = float(freq[-2:].sum()) # [0.9,1]
    top3 = float(np.sort(freq)[-3:].sum())
    if top_share > 0.9:
        return "point_mass", {"top_share": round(top_share, 4)}
    if low_tail > 0.5:
        return "zero_inflated", {"low_tail": round(low_tail, 4)}
    if high_tail > 0.5:
        return "ceiling", {"high_tail": round(high_tail, 4)}
    if top3 > 0.7:
        return "concentrated", {"top3": round(top3, 4)}
    return "spread", {}


def _profile_of(brain, field_id):
    """对单字段算画像（含 VECTOR flatten）。"""
    errors = []
    df = None
    data_field = None
    try:
        data_field = brain.get_data_field(field_id)
        df = brain.get_data_frame(data_field)
    except Exception as exc:
        errors.append(f"get_data_frame(data_field): {exc}")
        for kwargs in (
            {"field_id": field_id, "dataset_id": DATASET_ID, "region": REGION, "universe": UNIVERSE, "delay": DELAY},
            {"field_id": field_id, "region": REGION, "universe": UNIVERSE, "delay": DELAY},
        ):
            try:
                df = brain.get_data_frame(**kwargs)
                break
            except Exception as e2:
                errors.append(f"get_data_frame({kwargs}): {e2}")
    if df is None:
        return {"field_name": field_id, "error": " | ".join(errors)}

    values = _flatten_values(df)
    ftype = getattr(data_field, "type", None) or "MATRIX"
    if values.size == 0:
        return {"field_name": field_id, "data_type": ftype, "error": "no finite values"}

    total = values.size
    zero_ratio = float(np.sum(values == 0) / total)
    s = pd.Series(values)
    skew = float(s.skew()) if total > 2 else None
    kurt = float(s.kurt()) if total > 3 else None
    uniq = int(np.unique(values[:50000] if total > 50000 else values).size)
    shape, shape_info = _shape_of(values)

    return {
        "field_name": field_id,
        "data_type": ftype,
        "shape": shape,
        "coverage": None,  # Labs 单期快照无法给时间覆盖度；以平台 get_datafields 为准
        "skew": round(skew, 3) if skew is not None else None,
        "kurt": round(kurt, 3) if kurt is not None else None,
        "integer": bool(uniq <= 12),
        "freq": None,
        "pos_ratio": round(float(np.sum(values > 0) / total), 4),
        "neg_ratio": round(float(np.sum(values < 0) / total), 4),
        "near_zero_ratio": round(zero_ratio, 4),
        "approx_unique_count": uniq,
        "n_values": int(total),
        "shape_info": shape_info,
        "source": "brain_labs",
    }


def main():
    from brain import Brain
    try:
        brain = Brain(region=REGION, delay=DELAY, universe=UNIVERSE)
    except TypeError:
        brain = Brain()
    if DIAG_PROBE:
        _diag_inspect(brain, DIAG_FIELD)
        return
    out = {"dataset": DATASET_ID, "region": REGION, "universe": UNIVERSE, "delay": DELAY,
           "fields": [], "source": "brain_labs"}
    for fid in FIELDS:
        prof = _profile_of(brain, fid)
        out["fields"].append(prof)
        print(f"[{fid}] shape={prof.get('shape')} zero={prof.get('near_zero_ratio')} "
              f"skew={prof.get('skew')} uniq={prof.get('approx_unique_count')}")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nWROTE {OUTPUT_PATH}  ({len(out['fields'])} fields)")


if __name__ == "__main__":
    main()
