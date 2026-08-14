# -*- coding: utf-8 -*-
"""KOR/D1 chart_cnn_alpha 提交前双校验脚本。

用法:
  python kor_preflight_check.py --file kor_wave16O_exprs.json
  python kor_preflight_check.py --expr "rank(close)"

三道闸:
  1. 语法校验: 调用 alpha-expression-verifier 的 verify_expr.py
  2. 字段白名单: 表达式中的字段必须在 kor_chart_cnn_alpha_field_whitelist.json
     (仅收录平台回测 COMPLETE 验证过的字段)
  3. 数据类型/禁用模式: MATRIX数据集禁 vec_*; bucket/ts_entropy/ts_median 等
     已知整批CANCELLED元凶直接拦截
退出码: 0=全部PASS, 1=存在FAIL(禁止提交)
"""
import argparse, json, re, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WHITELIST = os.path.join(HERE, "..", "reference", "kor_chart_cnn_alpha_field_whitelist.json")
VERIFY_SCRIPT = r"C:\Users\MENGTAO\.qoder-cn\skills\alpha-expression-verifier\scripts\verify_expr.py"

# FASTEXPR 已知算子/函数(非字段)。新增算子前先确认平台支持再补录。
KNOWN_OPS = {
    "rank", "add", "subtract", "multiply", "divide", "signed_power", "sqrt",
    "greater", "less", "if_else", "trade_when", "delay", "delta",
    "ts_delay", "ts_delta", "ts_mean", "ts_sum", "ts_std_dev", "ts_rank",
    "ts_decay_linear", "ts_min", "ts_max", "ts_ir", "ts_av_diff", "ts_scale",
    "ts_zscore", "ts_backfill", "ts_arg_max", "ts_arg_min", "ts_product",
    "group_rank", "group_neutralize", "group_mean", "group_sum", "group_zscore",
    "quantile", "pasteurize", "normalize", "vec_avg", "vec_max", "vec_min",
    "vec_sum", "vec_count", "vec_norm", "bucket", "range", "winsorize",
    "abs", "log", "sign", "exp", "power",
}
# MATRIX 数据集禁用的 VECTOR 聚合算子
VECTOR_ONLY_OPS = {"vec_avg", "vec_max", "vec_min", "vec_sum", "vec_count", "vec_norm"}
# 分组标识符(group_rank/group_neutralize等的合法分组参数, 非数据字段)
GROUP_IDENTIFIERS = {"sector", "subindustry", "industry", "market", "country", "exchange"}

def extract_identifiers(expr):
    return re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr)

def check_syntax(expr):
    try:
        out = subprocess.run([sys.executable, VERIFY_SCRIPT, expr],
                             capture_output=True, text=True, timeout=30)
        d = json.loads(out.stdout)
        return bool(d.get("valid")), d.get("errors", [])
    except Exception as e:
        return False, [f"verifier error: {e}"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="含 expressions 列表的 JSON 文件")
    ap.add_argument("--expr", help="单个表达式")
    ap.add_argument("--whitelist", default=DEFAULT_WHITELIST)
    args = ap.parse_args()

    if args.file:
        exprs = json.load(open(args.file, encoding="utf-8"))["expressions"]
    elif args.expr:
        exprs = [args.expr]
    else:
        ap.error("need --file or --expr")

    wl = json.load(open(args.whitelist, encoding="utf-8"))
    verified = set(wl["verified_fields"].keys())
    data_type = wl.get("data_type", "MATRIX")
    banned = wl.get("banned_patterns", [])

    all_pass = True
    report = []
    for i, e in enumerate(exprs, 1):
        item = {"index": i, "issues": []}
        # 闸1: 语法
        ok, errs = check_syntax(e)
        if not ok:
            item["issues"].append(f"[SYNTAX] {errs}")
        # 提取标识符
        idents = set(extract_identifiers(e))
        fields = idents - KNOWN_OPS - GROUP_IDENTIFIERS
        ops_used = idents & KNOWN_OPS
        # 闸2: 字段白名单
        unknown = sorted(fields - verified)
        if unknown:
            item["issues"].append(f"[FIELD] 未验证字段(不在COMPLETE白名单): {unknown}")
        # 闸3a: MATRIX 禁 vec_*
        if data_type == "MATRIX":
            bad_ops = ops_used & VECTOR_ONLY_OPS
            if bad_ops:
                item["issues"].append(f"[TYPE] MATRIX数据集禁用vec_*聚合: {sorted(bad_ops)}")
        # 闸3b: 禁用模式
        for bp in banned:
            scope = bp.get("scope", "all")
            if scope == "vector_dataset" and data_type == "MATRIX":
                continue  # ts_backfill在MATRIX上合法
            if re.search(bp["pattern"], e):
                item["issues"].append(f"[BANNED] {bp['reason']}")
        item["fields"] = sorted(fields)
        item["pass"] = not item["issues"]
        all_pass = all_pass and item["pass"]
        report.append(item)

    print(json.dumps({"all_pass": all_pass, "total": len(exprs),
                      "passed": sum(r["pass"] for r in report),
                      "report": report}, ensure_ascii=False, indent=1))
    sys.exit(0 if all_pass else 1)

if __name__ == "__main__":
    main()
