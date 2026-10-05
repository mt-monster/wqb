"""Map arXiv paper abstracts to quantifiable WorldQuant factor concepts.

Two layers:
  * Rule layer (always on): keyword -> factor concept + suggested operators.
  * LLM layer (optional, --llm): OpenAI-compatible chat completion that returns
    a structured JSON mapping; falls back to the rule layer on any failure.

The output is meant to feed Mode B (idea-level) alpha improvement: give the
researcher concrete, implementable signal concepts instead of raw abstracts.
"""
import os
import json
import requests


def _load_dotenv():
    """Best-effort load of OPENAI_* from a sibling .arxiv_llm.env / .env file."""
    here = os.path.dirname(os.path.abspath(__file__))
    env = {}
    for name in ('.arxiv_llm.env', '.env'):
        path = os.path.join(here, name)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#') or '=' not in line:
                            continue
                        k, v = line.split('=', 1)
                        env[k.strip()] = v.strip().strip('"').strip("'")
            except Exception:
                pass
    return env


def _resolve_llm_config(explicit_key=None, explicit_base=None, explicit_model=None):
    dotenv = _load_dotenv()
    api_key = explicit_key or os.environ.get('OPENAI_API_KEY') or dotenv.get('OPENAI_API_KEY')
    base_url = (explicit_base or os.environ.get('OPENAI_BASE_URL') or
                dotenv.get('OPENAI_BASE_URL') or 'https://api.deepseek.com/v1')
    model = (explicit_model or os.environ.get('OPENAI_MODEL') or
             dotenv.get('OPENAI_MODEL') or 'deepseek-v4-flash')
    return api_key, base_url, model


def _normalize_base_url(base_url):
    """Turn a DeepSeek/OpenAI-style base into a /v1/chat/completions endpoint."""
    base = (base_url or 'https://api.deepseek.com/v1').rstrip('/')
    if not base.endswith('/v1'):
        base += '/v1'
    return base + '/chat/completions'


# (needle, concept_label, suggested_operators, one_line_idea)
RULES = [
    ('post-earnings-announcement drift', 'PEAD / 盈余公告后漂移',
     ['rank', 'ts_zscore', 'ts_rank'], '盈余公告后 N 日收益漂移，用 ts_zscore(return, N) 捕捉'),
    ('earnings', '盈余事件/预期', ['rank', 'ts_delta'], '盈余公告或预期修正事件，配合 ts_delta 看变化'),
    ('analyst', '分析师预期修正', ['rank', 'ts_delta'], '分析师评级/目标价修正，用 ts_delta 度量修正方向'),
    ('momentum', '动量', ['rank', 'ts_zscore', 'decay_linear'], '过去收益持续性，decay_linear 给近期更高权重'),
    ('reversal', '短期反转', ['rank', 'ts_rank'], '短期反转效应，用 ts_rank 反向'),
    ('anomaly', '统计异常', ['zscore', 'ts_zscore'], '偏离常态的异常值，zscore 标准化'),
    ('sentiment', '情绪', ['rank', 'group_rank'], '投资者/新闻情绪，按行业 group_rank'),
    ('emotion', '情绪', ['rank', 'group_rank'], '文本情绪信号'),
    ('volatility', '波动率', ['ts_std_dev', 'log'], '收益波动，ts_std_dev 度量'),
    ('liquidity', '流动性', ['rank', 'scale'], '交易活跃度/流动性'),
    ('volume', '成交量', ['rank', 'log'], '成交量异常或趋势'),
    ('value', '价值', ['rank'], '估值因子（价值/便宜）'),
    ('quality', '质量', ['rank'], '盈利质量因子'),
    ('jump', '价格跳跃', ['abs', 'log'], '财报/事件日价格跳跃'),
    ('drift', '趋势漂移', ['ts_zscore', 'rank'], '收益趋势漂移'),
    ('spillover', '跨资产溢出', ['rank', 'correlation'], '跨资产/跨期信息溢出'),
    ('attention', '关注度', ['rank', 'scale'], '投资者关注度/搜索量'),
    ('skew', '偏度', ['rank'], '收益分布偏度'),
    ('dispersion', '离散度', ['rank', 'std'], '预期离散度/分歧'),
    ('forecast', '预测', ['rank', 'ts_zscore'], '宏观/一致预期'),
]


def _rule_map(text):
    text = (text or '').lower()
    hits = []
    for needle, label, ops, idea in RULES:
        if needle in text:
            hits.append({'concept': label, 'operators': ops, 'idea': idea})
    seen = {}
    for h in hits:
        seen.setdefault(h['concept'], h)
    return list(seen.values())


def _llm_map(papers, model=None, base_url=None, api_key=None):
    """Return {paper_id: {...}} from an OpenAI-compatible endpoint, or None on failure."""
    api_key, base_url, model = _resolve_llm_config(api_key, base_url, model)
    if not api_key:
        print("[concept_extract] --llm set but no OPENAI_API_KEY found (env or .arxiv_llm.env); using rule layer instead.")
        return None
    url = _normalize_base_url(base_url)

    abstracts = "\n\n".join(
        f"ID: {p.get('paper_id')}\nTITLE: {p.get('title')}\nABSTRACT: {p.get('abstract')}"
        for p in papers
    )
    sys_prompt = (
        "You are a quantitative finance researcher. For each paper, extract concrete, "
        "implementable WorldQuant BRAIN alpha factor concepts. Return ONLY a JSON object "
        "mapping each paper ID to {\"concepts\": [short factor concept strings], "
        "\"operators\": [WQ operators like rank/ts_zscore/ts_rank/decay_linear/group_rank], "
        "\"idea\": one-line implementable signal description}."
    )
    try:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": abstracts},
                ],
                "temperature": 0.2,
            },
            timeout=90,
        )
        resp.raise_for_status()
        content = resp.json()['choices'][0]['message']['content']
        content = content.strip()
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
        return json.loads(content)
    except Exception as e:
        print(f"[concept_extract] LLM mapping failed ({e}); falling back to rule layer.")
        return None


def extract_concepts(papers, use_llm=False, api_key=None, model=None, base_url=None):
    """Return {paper_id: {...}} of extracted factor concepts for each paper."""
    out = {}
    llm_results = _llm_map(papers, model=model, base_url=base_url, api_key=api_key) if use_llm else None
    for p in papers:
        pid = p.get('paper_id')
        if llm_results and pid in llm_results:
            out[pid] = llm_results[pid]
        else:
            rules = _rule_map(p.get('abstract'))
            out[pid] = {
                'concepts': [r['concept'] for r in rules],
                'operators': sorted({op for r in rules for op in r['operators']}),
                'idea': '; '.join(r['idea'] for r in rules) if rules else 'no rule match',
            }
    return out


if __name__ == '__main__':
    print("Use from arxiv_api.py with --concepts / --llm")
