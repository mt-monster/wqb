"""Toolkit dispatcher for canonical repository dataset-experience logic."""
import sys
from pathlib import Path


def main():
    roots = [Path.cwd()]
    if '--campaign-dir' in sys.argv:
        roots.insert(0, Path(sys.argv[sys.argv.index('--campaign-dir') + 1]).resolve())
    for origin in roots:
        for root in (origin, *origin.parents):
            if (root / 'src/wqb/research/dataset_experience.py').is_file():
                sys.path.insert(0, str(root / 'src'))
                from wqb.research.dataset_experience import main as run
                return run()
    raise RuntimeError('未找到工作区 src/wqb/research/dataset_experience.py')


if __name__ == '__main__':
    raise SystemExit(main())
