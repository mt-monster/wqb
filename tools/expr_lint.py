#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
expr_lint.py — FASTEXPR 表达式双重门禁: 算子签名 + 字段合法性 (生成前强制校验)

背景 (2026-08-16 实战教训):
  1. ts_backfill(x, d, 0) k=0 非法 → 整批 CANCELLED (批次 A/B 全灭)
  2. rank(x, subindustry) → rank 只接受 1 个输入 (第二参是数值 rate),
     分组 rank 必须用 group_rank(x, group) → 整批 CANCELLED (批次 A2)
  3. group_vector_neut / vector_neut 为顾问专属算子 → ERROR (批次 C)
  4. hump(x, 0.01) 第二参必须命名 hump=0.01, 位置传参报
     "Invalid number of inputs : 2, should be exactly 1" → 探针批全灭

字段门控 (data/fields_gate/ 目录, 按 scope 分文件如 USA_TOP3000_D1.json; 兼容旧版单文件 fields_gate.json):
  - 未知字段(不在白名单、非常量/平台字段/分组字段) → 拦截
  - VECTOR 字段必须被 vec_* 聚合包裹, 直接裸用 → 拦截
  - GROUP 字段(subindustry 等)只允许出现在 group_* 算子的分组参数位
  - coverage < MIN_COVERAGE (默认0.6) 字段 → 拦截 (低覆盖 → 权重集中/CONCENTRATED_WEIGHT)
  - 兼容旧格式字段值为纯类型字符串

双数据集混合门控 (2026-08-16 用户策略升级):
  - 允许跨数据集混合字段构造经济学意义 alpha (如 微结构 × 基本面 知情确认)
  - 统计表达式实际使用的数据集集合, >2 个数据集 → 拦截 (上限 2 个, 保持信号可归因)
  - 恰好 2 个数据集 → 通过并输出 [MIX] 标注, 供台账记录混合组合
  - 单数据集表达式不受影响 (原纪律为子集)

用法:
  python tools/expr_lint.py "expr1" "expr2" ...
  python tools/expr_lint.py --file exprs.txt [--fields data/fields_gate --scope USA/TOP3000/D1 --min-cov 0.6 --max-datasets 2]
退出码: 0=全部通过, 1=存在违规

签名数据来源: shared_libs/operators_catalog.py (2026-08-11 平台 get_operators 102 算子)。
scope 审计 (2026-08-16): 102 = REGULAR 可用 83 (25 全 scope + 58 COMBO+REGULAR)
          + COMBO-only 17 + SELECTION-only 2; REGULAR 可用者入 SIGNATURES,
          COMBO/SELECTION 受限者入 FORBIDDEN, 幽灵算子由 operators_verified.json 管理。
新增算子前先查 definition + scope 再补录; 新数据集先 get_datafields 再补 fields_gate 对应 scope 文件。
"""
import re
import sys
import json
import os

# ---------- 算子签名: name -> (min_args, max_args) ----------
SIGNATURES = {
    'add': (2, None), 'multiply': (2, None), 'subtract': (2, None),
    'max': (2, None), 'min': (2, None),
    'sign': (1, 1), 'log': (1, 1), 'abs': (1, 1), 'sqrt': (1, 1),
    'inverse': (1, 1), 'reverse': (1, 1), 'pasteurize': (1, 1),
    'densify': (1, 1), 'divide': (2, 2), 'power': (2, 2),
    'signed_power': (2, 2),
    'or': (2, 2), 'and': (2, 2), 'not': (1, 1), 'is_nan': (1, 1),
    'if_else': (3, 3),
    'equal': (2, 2), 'not_equal': (2, 2), 'greater': (2, 2),
    'greater_equal': (2, 2), 'less': (2, 2), 'less_equal': (2, 2),
    'ts_corr': (3, 3), 'ts_zscore': (2, 2), 'ts_returns': (2, 3),
    'ts_product': (2, 2), 'ts_std_dev': (2, 2),
    'ts_backfill': (2, 3),
    'days_from_last_change': (1, 1), 'last_diff_value': (2, 2),
    'ts_scale': (2, 3), 'ts_sum': (2, 2), 'ts_av_diff': (2, 2),
    'ts_kurtosis': (2, 2), 'ts_mean': (2, 2), 'ts_arg_max': (2, 2),
    'ts_rank': (2, 3), 'ts_ir': (2, 2), 'ts_delay': (2, 2),
    'ts_quantile': (2, 3), 'ts_count_nans': (2, 2),
    'ts_covariance': (3, 3), 'ts_decay_linear': (2, 3),
    'ts_arg_min': (2, 2), 'ts_regression': (3, 5),
    'ts_max_diff': (2, 2), 'kth_element': (3, 4),
    'hump': (1, 2), 'ts_delta': (2, 2), 'ts_step': (1, 1),
    'ts_target_tvr_decay': (1, 4), 'ts_target_tvr_hump': (1, 4),
    'winsorize': (1, 2), 'rank': (1, 2),
    'zscore': (1, 1), 'scale': (1, 4), 'normalize': (1, 3),
    'quantile': (1, 1),  # 平台实证仅 1 参（2026-08-14 wave17Z: 2 参报 Invalid number of inputs 级联 CANCEL 整批）
    'vec_min': (1, 1), 'vec_max': (1, 1), 'vec_avg': (1, 1),
    'vec_sum': (1, 1), 'vec_count': (1, 1), 'vec_stddev': (1, 1),
    'vec_range': (1, 1),
    'bucket': (2, 4), 'tail': (1, 4), 'trade_when': (3, 3),
    'group_mean': (3, 3), 'group_rank': (2, 2),
    'group_backfill': (3, 4), 'group_scale': (2, 2),
    'group_count': (2, 2), 'group_zscore': (2, 2),
    'group_std_dev': (2, 2), 'group_sum': (2, 2),
    'group_neutralize': (2, 2), 'group_cartesian_product': (2, 2),
}

# group_* 算子的分组参数位置 (0-based)
GROUP_ARG_POS = {
    'group_rank': 1, 'group_scale': 1, 'group_count': 1,
    'group_zscore': 1, 'group_std_dev': 1, 'group_sum': 1,
    'group_neutralize': 1, 'group_mean': 2, 'group_backfill': 1,
    'group_cartesian_product': (0, 1),
}

# 命名参数强制表: op -> {arg_pos: 'name'} (位置传参会被平台拒收)
NAMED_ONLY = {'hump': {1: 'hump'}}

# 单位语义高危后缀: 带物理单位的字段与纯常量直接 add/subtract 会报
# "Incompatible unit ... expected Unit[CSShare:1], found Unit[]" (WARNING级)
# 修法: divide(a, b) 相除消单位, 或 multiply(x, 1.0) 不可靠, 优先用比率结构
UNIT_SUFFIXES = ('share_count', '_shares', 'market_value')

# VECTOR 字段禁止直接包裹的算子 (event 输入不支持, 2026-08-18 wave34 教训)
# 这些算子直接包裹 VECTOR 字段会报 "does not support event inputs"
VECTOR_FORBIDDEN_OPS = {
    'ts_backfill', 'ts_delta', 'divide', 'subtract', 'add', 'multiply',
    'ts_zscore', 'ts_rank', 'ts_corr', 'ts_covariance', 'ts_regression',
    'ts_mean', 'ts_sum', 'ts_std_dev', 'ts_product', 'ts_av_diff',
    'ts_kurtosis', 'ts_arg_max', 'ts_arg_min', 'ts_max_diff',
    'ts_scale', 'ts_delay', 'ts_quantile', 'ts_count_nans',
    'ts_decay_linear', 'ts_ir', 'ts_returns', 'ts_step',
    'rank', 'zscore', 'scale', 'normalize', 'quantile',
    'winsorize', 'bucket', 'tail', 'trade_when',
    'group_mean', 'group_rank', 'group_backfill', 'group_scale',
    'group_count', 'group_zscore', 'group_std_dev', 'group_sum',
    'group_neutralize', 'group_cartesian_product',
    'power', 'signed_power', 'log', 'sqrt', 'abs', 'inverse', 'reverse',
    'sign', 'pasteurize', 'densify', 'max', 'min',
    'if_else', 'equal', 'not_equal', 'greater', 'greater_equal',
    'less', 'less_equal', 'or', 'and', 'not', 'is_nan',
    'days_from_last_change', 'last_diff_value', 'kth_element',
    'hump', 'ts_target_tvr_decay', 'ts_target_tvr_hump',
}

# 已知权限受限 / scope 受限算子 (REGULAR alpha 不可用)
FORBIDDEN = {
    'group_vector_neut': '顾问(Consultant)专属, 报 inaccessible/unknown operator',
    'vector_neut': '顾问(Consultant)专属, 用 group_neutralize 等价替代',
    # COMBO-only: 组合 alpha 专用, REGULAR 表达式不可用 (2026-08-16 scope 审计补录)
    'generate_stats': '仅 COMBO scope (逐日统计), REGULAR 不可用',
    'combo_a': '仅 COMBO scope (多信号组合), REGULAR 不可用',
    'self_corr': '仅 COMBO scope (相关矩阵), REGULAR 不可用',
    'reduce_avg': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_choose': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_count': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_ir': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_kurtosis': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_max': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_min': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_norm': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_percentage': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_powersum': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_range': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_skewness': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_stddev': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    'reduce_sum': '仅 COMBO scope (reduce 家族), REGULAR 不可用',
    # SELECTION-only: 选择型 alpha 专用
    'in': '仅 SELECTION scope (成员测试), REGULAR 不可用',
    'universe_size': '仅 SELECTION scope (universe 大小), REGULAR 不可用',
}

# 平台内置字段 (不在数据集白名单但合法)
PLATFORM_FIELDS = {
    'open', 'high', 'low', 'close', 'vwap', 'returns', 'adv20', 'adv60',
    'cap', 'sharesout', 'volume', 'cap3', 'rank', 'sector', 'industry',
    'subindustry', 'country', 'exchange', 'sector_country',
    'industry_country', 'sector_exchange', 'date', 'bucket',
}
GROUP_FIELDS = {
    'subindustry', 'industry', 'sector', 'country', 'exchange',
    'sector_country', 'industry_country', 'sector_exchange', 'bucket',
}


def load_fields(path, scope):
    """加载字段白名单 {field: {'type', 'coverage'}}, 合并 scope 下所有数据集。
    兼容旧格式(字段值为纯类型字符串, coverage 缺省 1.0)。
    支持两种路径模式:
      - 单文件: data/fields_gate.json (旧版, 向后兼容)
      - 目录:   data/fields_gate/ 下按 scope 分文件 (USA_TOP3000_D1.json 等)
    返回 (merged, ds_map): ds_map = {field: set(数据集)} 供双数据集门控。"""
    if not path:
        return None, None
    # 目录模式: data/fields_gate/USA_TOP3000_D1.json
    if os.path.isdir(path):
        fname = scope.replace('/', '_') + '.json'
        fpath = os.path.join(path, fname)
        if not os.path.exists(fpath):
            return None, None
        try:
            with open(fpath, encoding='utf-8') as f:
                data = json.load(f)
            # 目录模式下 data 直接是 {dataset: {fields: {...}}}
            merged = {}
            ds_map = {}
            for ds, info in data.items():
                for k, v in info.get('fields', {}).items():
                    if isinstance(v, dict):
                        merged[k] = {'type': v.get('type', 'MATRIX'), 'coverage': v.get('coverage', 1.0)}
                    else:
                        merged[k] = {'type': v, 'coverage': 1.0}
                    ds_map.setdefault(k, set()).add(ds)
            return (merged or None), (ds_map or None)
        except Exception:
            return None, None
    # 单文件模式 (向后兼容)
    if not os.path.exists(path):
        return None, None
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        merged = {}
        ds_map = {}
        for ds, info in data.get(scope, {}).items():
            for k, v in info.get('fields', {}).items():
                if isinstance(v, dict):
                    merged[k] = {'type': v.get('type', 'MATRIX'), 'coverage': v.get('coverage', 1.0)}
                else:
                    merged[k] = {'type': v, 'coverage': 1.0}
                ds_map.setdefault(k, set()).add(ds)
        return (merged or None), (ds_map or None)
    except Exception:
        return None, None


def _split_args(s):
    args, depth, cur, in_str = [], 0, '', False
    for ch in s:
        if ch == '"' or ch == "'":
            in_str = not in_str
            cur += ch
            continue
        if not in_str:
            if ch in '([':
                depth += 1
            elif ch in ')]':
                depth -= 1
            if ch == ',' and depth == 0:
                args.append(cur.strip())
                cur = ''
                continue
        cur += ch
    if cur.strip():
        args.append(cur.strip())
    return args


def _is_leaf(expr):
    return not re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\(', expr.strip())


def _has_unit_field(arg, fields):
    """参数里是否含带物理单位的高危字段 (叶子或嵌套均可)。"""
    m = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)\s*$', arg, re.S)
    if m and m.group(1) in SIGNATURES:
        return any(_has_unit_field(a, fields) for a in _split_args(m.group(2)))
    name = arg.strip().split('=')[-1].strip() if '=' in arg else arg.strip()
    if not re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', name):
        return False
    known = fields is None or name in fields or name in PLATFORM_FIELDS
    return known and any(name.endswith(s) for s in UNIT_SUFFIXES)


def _check_leaf(expr, errors, ctx, loc):
    """叶子节点: 常量/平台字段/分组字段/数据字段(带类型检查)。"""
    e = expr.strip()
    if re.fullmatch(r'-?[0-9]+(\.[0-9]+)?', e):
        return
    if re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*=(.*)', e):  # 命名参数值
        e = e.split('=', 1)[1].strip()
        if re.fullmatch(r'-?[0-9]+(\.[0-9]+)?', e) or e.startswith('"') or e.startswith("'"):
            return
    m = re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', e)
    if not m:
        return  # 比较式/复合, 交给递归或忽略
    name = e
    if name in FORBIDDEN:
        errors.append(f'[{loc}] 禁用算子 {name}: {FORBIDDEN[name]}')
        return
    if name in PLATFORM_FIELDS:
        return
    fields = ctx['fields']
    if fields is None:
        return  # 未加载白名单则跳过字段检查
    if name not in fields:
        errors.append(f'[{loc}] 字段 "{name}" 不在 get_datafields 白名单 (先查字段再写表达式)')
        return
    info = fields[name]
    if info['type'] == 'VECTOR' and not ctx['in_vec']:
        errors.append(f'[{loc}] VECTOR 字段 "{name}" 必须用 vec_* 聚合包裹 (vec_avg/vec_sum/...)')
    min_cov = ctx.get('min_cov', 0.0)
    if info['coverage'] < min_cov:
        errors.append(f'[{loc}] 字段 "{name}" coverage={info["coverage"]} < {min_cov}, 低覆盖易致 CONCENTRATED_WEIGHT/信号稀疏, 换高覆盖字段')
    # 双数据集门控: 记录字段归属的数据集
    ds_map = ctx.get('ds_map')
    if ds_map and name in ds_map:
        ctx['used_ds'].update(ds_map[name])


def _walk(expr, errors, ctx, path='', in_vec=False):
    m = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)\s*$', expr, re.S)
    if not m:
        _check_leaf(expr, errors, {**ctx, 'in_vec': in_vec}, path)
        return
    name, inner = m.group(1), m.group(2)
    loc = path + name

    if name in FORBIDDEN:
        errors.append(f'[{loc}] 禁用算子 {name}: {FORBIDDEN[name]}')
        return
    if name not in SIGNATURES:
        errors.append(f'[{loc}] 未知算子 {name} (不在 REGULAR 83 算子白名单, 先查 get_operators/catalog 再补录)')
        return

    args = _split_args(inner)
    lo, hi = SIGNATURES[name]
    n = len(args)
    if n < lo or (hi is not None and n > hi):
        rng = f'{lo}+' if hi is None else str(lo) if lo == hi else f'{lo}-{hi}'
        errors.append(f'[{loc}] {name} 需要 {rng} 个参数, 实给 {n}: {expr.strip()}')
        return

    # VECTOR 字段禁止直接包裹检查 (2026-08-18 wave34 教训)
    # 若当前算子在 VECTOR_FORBIDDEN_OPS 中, 且参数中包含 VECTOR 字段 → 报错
    if name in VECTOR_FORBIDDEN_OPS and ctx.get('fields'):
        for i, a in enumerate(args):
            if _is_leaf(a):
                a_name = a.strip().split('=')[-1].strip() if '=' in a else a.strip()
                if a_name in ctx['fields'] and ctx['fields'][a_name].get('type') == 'VECTOR':
                    errors.append(
                        f'[{loc}] VECTOR 字段 "{a_name}" 不能被 {name} 直接包裹 '
                        f'(event 输入不支持, 会报 "does not support event inputs"); '
                        f'请先用 vec_avg/vec_sum 聚合: {name}(vec_avg({a_name}), ...)'
                    )

    # 命名参数强制检查 (hump 第二参必须 hump=0.01)
    for pos, kw in NAMED_ONLY.get(name, {}).items():
        if pos < n and not args[pos].startswith(kw + '='):
            errors.append(f'[{loc}] {name} 第{pos + 1}参必须命名传参 "{kw}={args[pos]}", 位置传参会报 Invalid number of inputs')

    # 语义级校验
    if name == 'ts_backfill' and n == 3:
        k = args[2].strip()
        if k.startswith('k='):
            k = k[2:].strip()
        if not re.fullmatch(r'[1-9][0-9]*', k):
            errors.append(f'[{loc}] ts_backfill 第三参 k 必须为正整数(默认1), k={k} 非法 (k=0 连坐整批)')
    if name == 'rank' and n == 2:
        rate = args[1].strip()
        if not re.fullmatch(r'[0-9]+(\.[0-9]+)?', rate):
            errors.append(f'[{loc}] rank 第二参是数值 rate(默认2), 不接受分组字段 "{rate}"; 组内排名请用 group_rank(x, group)')

    # 单位语义检查: add/subtract 带单位字段 ± 纯常量 → Incompatible unit
    if name in ('add', 'subtract') and n == 2:
        a_unit = _has_unit_field(args[0], ctx['fields'])
        b_unit = _has_unit_field(args[1], ctx['fields'])
        a_const = re.fullmatch(r'-?[0-9]+(\.[0-9]+)?', args[0].strip())
        b_const = re.fullmatch(r'-?[0-9]+(\.[0-9]+)?', args[1].strip())
        if (a_unit and b_const) or (b_unit and a_const):
            errors.append(f'[{loc}] {name}(带单位字段, 常量) 会报 Incompatible unit (Unit[CSShare] vs Unit[]); 改用 divide(a, b) 比率结构消单位')

    # 分组参数位置检查: GROUP 字段只能出现在 group_* 的分组位
    gpos = GROUP_ARG_POS.get(name)
    for i, a in enumerate(args):
        if _is_leaf(a):
            a_name = a.strip().split('=')[0].strip() if '=' in a else a.strip()
            if a_name in GROUP_FIELDS:
                ok = (i in gpos) if isinstance(gpos, tuple) else (i == gpos)
                if not ok:
                    errors.append(f'[{loc}] 分组字段 "{a_name}" 只允许出现在 {name} 的分组参数位')
                    continue
        child_vec = in_vec or name.startswith('vec_')
        _walk(a, errors, ctx, loc + '>', in_vec=child_vec)


def lint(expr, fields=None, min_cov=0.6, ds_map=None, max_ds=2):
    errors = []
    if expr.count('(') != expr.count(')'):
        errors.append('[括号] 左右括号数量不匹配')
    ctx = {'fields': fields, 'min_cov': min_cov, 'ds_map': ds_map, 'used_ds': set()}
    _walk(expr.strip(), errors, ctx)
    if ds_map and len(ctx['used_ds']) > max_ds:
        errors.append(f'[MIX] 表达式跨 {len(ctx["used_ds"])} 个数据集: {sorted(ctx["used_ds"])} — 混合上限 {max_ds} 个 (当前口径, 保持信号可归因), 超限拦截; 若已授权放宽用 --max-datasets N')
    return errors, sorted(ctx['used_ds'])


def main():
    argv = sys.argv[1:]
    exprs, fields_path, scope, min_cov, max_ds = [], 'data/fields_gate', 'USA/TOP3000/D1', 0.6, 2
    if '--file' in argv:
        i = argv.index('--file')
        with open(argv[i + 1], encoding='utf-8') as f:
            exprs = [ln.strip() for ln in f if ln.strip() and not ln.startswith('#')]
        argv = argv[:i] + argv[i + 2:]
    if '--fields' in argv:
        i = argv.index('--fields')
        fields_path = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if '--scope' in argv:
        i = argv.index('--scope')
        scope = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if '--min-cov' in argv:
        i = argv.index('--min-cov')
        min_cov = float(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    if '--max-datasets' in argv:
        i = argv.index('--max-datasets')
        max_ds = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    if not exprs:
        exprs = argv
    if not exprs:
        print('用法: expr_lint.py "expr" ... | --file exprs.txt [--fields fields_gate --scope USA/TOP3000/D1]')
        sys.exit(2)

    if not os.path.isabs(fields_path):
        fields_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), fields_path)
    fields, ds_map = load_fields(fields_path, scope)
    if fields is None:
        print(f'[警告] 字段白名单未加载 ({fields_path} scope={scope}), 字段门控关闭!')
    else:
        print(f'[门控] 字段白名单 {len(fields)} 个 (scope={scope}, 最低coverage={min_cov})')

    bad = 0
    for i, e in enumerate(exprs, 1):
        errs, used_ds = lint(e, fields, min_cov, ds_map, max_ds)
        mix = f' [MIX {len(used_ds)}数据集:{"+".join(used_ds)}]' if len(used_ds) >= 2 else ''
        if errs:
            bad += 1
            print(f'[FAIL] #{i} {e}{mix}')
            for er in errs:
                print(f'       - {er}')
        else:
            print(f'[OK]   #{i} {e}{mix}')
    print(f'\n共 {len(exprs)} 条, 通过 {len(exprs) - bad}, 失败 {bad}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
