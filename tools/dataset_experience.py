"""CLI for the canonical dataset-experience renderer."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from wqb.research.dataset_experience import main

if __name__ == '__main__':
    raise SystemExit(main())
