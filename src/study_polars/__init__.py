import shutil
import sys
from pathlib import Path

from jupyter_core.command import main as jupyter_main


def main():
    cwd = Path()
    (cwd / "work").mkdir(exist_ok=True)
    nb = "study_polars.ipynb"
    if sys.argv[-1] == "--new" or not (cwd / "work" / nb).exists():
        shutil.copyfile(cwd / "nbs" / nb, cwd / "work" / nb)
    sys.argv = ["jupyter", "lab", "work"]
    sys.exit(jupyter_main())
