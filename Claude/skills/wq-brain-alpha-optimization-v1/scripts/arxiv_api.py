import requests
import xml.etree.ElementTree as ET
import os
import sys
import argparse
import time
import hashlib
import json


# ---------------------------------------------------------------------------
# arXiv archive -> concrete arXiv subcategory list. Archive-level `cat:q-fin`
# queries return 0 results; the API requires a specific subcategory (q-fin.ST).
# ---------------------------------------------------------------------------
CAT_EXPANSION = {
    'q-fin': ['q-fin.ST', 'q-fin.CP', 'q-fin.PM', 'q-fin.GN', 'q-fin.RG', 'q-fin.MF', 'q-fin.PR'],
    'econ': ['econ.GN', 'econ.EM', 'econ.TH'],
    'stat': ['stat.AP', 'stat.ML', 'stat.ME', 'stat.CO', 'stat.TH'],
    'cs': ['cs.LG', 'cs.AI', 'cs.CE', 'cs.CR', 'cs.DS'],
}

# Local cache so repeated identical queries never hit the network twice.
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.arxiv_cache.json')
# arXiv politeness: keep >= 3s between successive requests.
_MIN_INTERVAL = 3.0
_LAST_CALL = 0.0


def _throttle():
    """Sleep just enough to keep >= _MIN_INTERVAL between arXiv requests."""
    global _LAST_CALL
    now = time.time()
    wait = _MIN_INTERVAL - (now - _LAST_CALL)
    if wait > 0:
        time.sleep(wait)
    _LAST_CALL = time.time()


def _cache_load():
    try:
        with open(CACHE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def _cache_save(db):
    try:
        with open(CACHE_PATH, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _cache_key(query, max_results, cat):
    raw = f"{query}|{max_results}|{cat}"
    return hashlib.md5(raw.encode('utf-8')).hexdigest()


def _build_search_query(query, cat=None):
    """Assemble the arXiv search_query string. Expand known archives to their
    subcategories so `--cat q-fin` matches the whole archive instead of 0 results."""
    if not cat:
        return query
    if cat in CAT_EXPANSION:
        cat_clause = ' OR '.join(f'cat:{c}' for c in CAT_EXPANSION[cat])
        return f'({cat_clause}) AND ({query})'
    return f'cat:{cat} AND ({query})'


def search_arxiv(query, max_results=10, cat=None):
    """Search arXiv for papers, optionally scoped to a category (e.g. 'q-fin') to cut noise.

    Results are cached locally (keyed by query+cat+max_results) and requests are
    throttled to >=3s apart to respect arXiv's rate limits.
    """
    key = _cache_key(query, max_results, cat)
    db = _cache_load()
    if key in db:
        return db[key]

    base_url = "https://export.arxiv.org/api/query"
    search_query = _build_search_query(query, cat)
    params = {
        'search_query': search_query,
        'start': 0,
        'max_results': max_results,
    }

    _throttle()
    response = requests.get(base_url, params=params)
    text = response.text
    db[key] = text
    _cache_save(db)
    return text


def get_paper_metadata(paper_id):
    """Get paper metadata directly from arXiv API"""
    try:
        metadata_url = f"https://export.arxiv.org/api/query?id_list={paper_id}"
        _throttle()
        response = requests.get(metadata_url)
        if response.status_code == 200:
            papers = parse_search_results(response.text)
            if papers and len(papers) > 0:
                return papers[0]
        return None
    except Exception as e:
        print(f"Error fetching paper metadata: {e}")
        return None


def download_paper(paper_id, output_dir=".", paper_title=None):
    """Download a paper by its ID and rename it to the paper title"""
    pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    response = requests.get(pdf_url)

    if response.status_code == 200:
        if paper_title:
            clean_title = "".join(c for c in paper_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_title = clean_title.replace(' ', '_')[:100]
            filename = f"{clean_title}.pdf"
        else:
            filename = f"{paper_id}.pdf"

        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filepath}")
        return filepath
    else:
        print(f"Failed to download paper {paper_id}")
        return None


def parse_search_results(xml_content):
    """Parse XML search results and extract paper information"""
    try:
        root = ET.fromstring(xml_content)
        papers = []
        for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
            paper_info = {}
            title_elem = entry.find('.//{http://www.w3.org/2005/Atom}title')
            if title_elem is not None:
                paper_info['title'] = title_elem.text.strip()
            authors = []
            for author in entry.findall('.//{http://www.w3.org/2005/Atom}author'):
                name_elem = author.find('.//{http://www.w3.org/2005/Atom}name')
                if name_elem is not None:
                    authors.append(name_elem.text.strip())
            paper_info['authors'] = authors
            summary_elem = entry.find('.//{http://www.w3.org/2005/Atom}summary')
            if summary_elem is not None:
                paper_info['abstract'] = summary_elem.text.strip()
            id_elem = entry.find('.//{http://www.w3.org/2005/Atom}id')
            if id_elem is not None:
                paper_info['paper_id'] = id_elem.text.split('/')[-1]
            published_elem = entry.find('.//{http://www.w3.org/2005/Atom}published')
            if published_elem is not None:
                paper_info['published'] = published_elem.text.strip()
            papers.append(paper_info)
        return papers
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []


def search_and_download(query, max_results=5, download_first=False, cat=None,
                        json_path=None, concepts=False, use_llm=False,
                        llm_model=None, llm_base=None):
    """Search for papers; optionally download the first result, write results to
    JSON, and/or extract quantifiable factor concepts (Mode B idea feed)."""
    print(f"Searching arXiv for: '{query}'" + (f"  [cat:{cat}]" if cat else ""))
    print("-" * 50)

    results = search_arxiv(query, max_results, cat=cat)
    papers = parse_search_results(results)

    if not papers:
        print("No papers found.")
        return

    concepts_out = None
    if concepts:
        from concept_extract import extract_concepts
        concepts_out = extract_concepts(papers, use_llm=use_llm,
                                        model=llm_model, base_url=llm_base)

    # Structured output mode: dump to JSON (optionally with concepts) for pipeline.
    if json_path:
        payload = papers
        if concepts:
            payload = [dict(p, concepts=concepts_out.get(p['paper_id'])) for p in papers]
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"Wrote {len(papers)} papers -> {json_path}" + (" (with concepts)" if concepts else ""))
        return

    # Display search results
    print(f"Found {len(papers)} papers:\n")
    for i, paper in enumerate(papers, 1):
        print(f"{i}. Title: {paper.get('title', 'N/A')}")
        print(f"   Authors: {', '.join(paper.get('authors', ['N/A']))}")
        print(f"   Paper ID: {paper.get('paper_id', 'N/A')}")
        print(f"   Published: {paper.get('published', 'N/A')}")
        print(f"   Abstract: {paper.get('abstract', 'N/A')[:200]}...")
        if concepts and concepts_out:
            pc = concepts_out.get(paper.get('paper_id'))
            if pc:
                print(f"   Concepts: {', '.join(pc.get('concepts', []))}")
                print(f"   Suggested ops: {', '.join(pc.get('operators', []))}")
                print(f"   Idea: {pc.get('idea', '')}")
        print()

    if download_first and papers:
        first_paper = papers[0]
        paper_id = first_paper.get('paper_id')
        paper_title = first_paper.get('title')
        if paper_id:
            print(f"Downloading first paper: {paper_id}")
            download_paper(paper_id, paper_title=paper_title)
        else:
            print("Could not extract paper ID for download")


def interactive_mode():
    """Interactive mode for searching arXiv"""
    print("🔍 arXiv Paper Search Tool")
    print("=" * 40)
    print("Commands:")
    print("  search <query> [max_results] - Search for papers")
    print("  download <paper_id> - Download a specific paper")
    print("  help - Show this help message")
    print("  quit/exit - Exit the program")
    print()

    while True:
        try:
            command = input("📚 arxiv> ").strip()
            if not command:
                continue
            parts = command.split()
            cmd = parts[0].lower()
            if cmd in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            elif cmd == 'help':
                print("Commands:")
                print("  search <query> [max_results] - Search for papers")
                print("  download <paper_id> - Download a specific paper")
                print("  help - Show this help message")
                print("  quit/exit - Exit the program")
                print()
            elif cmd == 'search':
                if len(parts) < 2:
                    print("Usage: search <query> [max_results]")
                    continue
                query = ' '.join(parts[1:-1]) if len(parts) > 2 else parts[1]
                max_results = int(parts[-1]) if len(parts) > 2 and parts[-1].isdigit() else 5
                search_and_download(query, max_results, download_first=False)
            elif cmd == 'download':
                if len(parts) < 2:
                    print("Usage: download <paper_id>")
                    continue
                paper_id = parts[1]
                paper_info = get_paper_metadata(paper_id)
                if paper_info and paper_info.get('title'):
                    paper_title = paper_info['title']
                    print(f"Found paper: {paper_title}")
                    download_paper(paper_id, paper_title=paper_title)
                else:
                    print(f"Could not find paper information for {paper_id}")
                    print("Downloading with paper ID as filename...")
                    download_paper(paper_id)
            else:
                print(f"Unknown command: {cmd}")
                print("Type 'help' for available commands")
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search and download papers from arXiv')
    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('-n', '--max_results', type=int, default=5, help='Maximum number of results (default: 5)')
    parser.add_argument('-d', '--download', action='store_true', help='Download the first result')
    parser.add_argument('-c', '--cat', help='Restrict to an arXiv category/archive, e.g. q-fin (auto-expands to subcategories)')
    parser.add_argument('-j', '--json', metavar='PATH', help='Write results as JSON to PATH instead of printing')
    parser.add_argument('--concepts', action='store_true', help='Extract quantifiable factor concepts from abstracts (Mode B feed)')
    parser.add_argument('--llm', action='store_true', help='Use an OpenAI-compatible LLM for concept extraction (reads .arxiv_llm.env / env)')
    parser.add_argument('--llm-model', help='Override LLM model (default from config: deepseek-v4-flash)')
    parser.add_argument('--llm-base', help='Override LLM base URL (default from config: https://api.deepseek.com/v1)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Start interactive mode')

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.query:
        search_and_download(args.query, args.max_results, args.download,
                            cat=args.cat, json_path=args.json,
                            concepts=args.concepts, use_llm=args.llm,
                            llm_model=args.llm_model, llm_base=args.llm_base)
    else:
        interactive_mode()
