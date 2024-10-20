"""
下記を実行して何も出力されなければ問題なし
```
uv run src/tools/create_check_code.py &&\
uv run tmp/code_ok.py | grep NG &&\
uv run tmp/code_ng.py | grep OK
```
"""  # noqa: INP001

import re
from pathlib import Path

import nbformat


def proc_prob(fp_ok, fp_ng, count, cell1, cell2, cell3, cell4):  # noqa: C901 PLR0912 PLR0913 PLR0915 PLR0917
    msg = f"Cell {count}: invalid 問題"
    source = cell1["source"]
    metadata = cell1["metadata"]
    if not re.match("### `問題[0-9A-Z]{3}`", source):
        raise ValueError(msg)
    if not source.endswith("**解答欄**"):
        raise ValueError(msg)
    if metadata.get("editable", False) or not metadata.get("frozen", False):
        raise ValueError(msg)
    title = source.splitlines()[0]
    fp_ok.write("\nprint('# ==========')\n")
    fp_ng.write("\nprint('# ==========')\n")
    fp_ok.write(f"print('{title}')\n")
    fp_ng.write(f"print('{title}')\n")

    msg = f"Cell {count + 1}: invalid 解答欄"
    source = cell2["source"]
    metadata = cell2["metadata"]
    if cell2["cell_type"] != "code":
        raise ValueError(msg)
    last = source.strip().splitlines()[-1]
    if not last.startswith("# ここから解答を作成"):
        raise ValueError(msg)
    if not metadata.get("editable", False) or metadata.get("frozen", False):
        raise ValueError(msg)
    fp_ok.write(f"{source}\n")
    fp_ng.write(f"{source}\n")

    msg = f"Cell {count + 2}: invalid 解答例"
    source = cell3["source"]
    metadata = cell3["metadata"]
    if cell3["cell_type"] != "markdown":
        raise ValueError(msg)
    if not source.startswith("<details><summary>解答例</summary>"):
        raise ValueError(msg)
    if re.match(r"_ans = \w+ = ", source):
        raise ValueError(msg)
    answers = re.findall("```python\n(.*?)```", source, re.DOTALL)
    if not answers:
        raise ValueError(msg)
    if metadata.get("editable", False) or not metadata.get("frozen", False):
        raise ValueError(msg)

    msg = f"Cell {count + 3}: invalid 検証"
    source = cell4["source"]
    metadata = cell4["metadata"]
    if cell4["cell_type"] != "code":
        raise ValueError(msg)
    if not source.startswith("# このセルを実行してください"):
        raise ValueError(msg)
    if (
        metadata.get("editable", False)
        or metadata.get("frozen", False)
        or "source_hidden" not in metadata.get("jupyter", {})
    ):
        raise ValueError(msg)
    for answer in answers:
        fp_ok.write(f"{answer}\n")
        fp_ok.write(f"{source}\n")
        fp_ng.write(f"{source}\n")
    return title


def create_check_code(nb_path, fp_ok, fp_ng):
    fp_ok.write("import os\nos.chdir('tmp')\n")
    fp_ng.write("import os\nos.chdir('tmp')\n")
    nb = nbformat.reads(nb_path.read_text(), 4)
    cells = nb["cells"]
    n_cells = len(cells)
    title = ""
    it = iter(cells)
    count = 0
    while count < n_cells:
        count += 1
        cell = next(it)
        source = cell["source"]
        if not source:
            msg = f"Cell {count}: empty source"
            raise ValueError(msg)
        cell_type = cell["cell_type"]
        if cell_type == "markdown":
            if m := re.search(r"^skip (\d+)", source):
                n = int(m.group(1))
                print(f"Skip {n} cells at {count}")
                count += n
                for _ in range(n):
                    next(it)
                continue
            if source.startswith("### `問題"):
                prev = title
                title = proc_prob(fp_ok, fp_ng, count, cell, next(it), next(it), next(it))
                if prev > title:
                    msg = f"Cell {count}: invalid 問題"
                    raise ValueError(msg)
                count += 3
            elif source.startswith("<details><summary>解答例</summary>"):
                msg = f"Cell {count}: invalid 解答例"
                raise ValueError(msg)
        elif cell_type == "code":
            last = source.strip().splitlines()[-1]
            if last.startswith("# ここから解答を作成"):
                msg = f"Cell {count}: invalid 解答欄"
                raise ValueError(msg)
            if source.startswith("# このセルを実行してください"):
                fp_ok.write(f"{source}\n")
                fp_ng.write(f"{source}\n")


if __name__ == "__main__":
    in_nb = Path("nbs/study_polars.ipynb")
    out_ok = Path("tmp/code_ok.py")
    out_ng = Path("tmp/code_ng.py")
    with out_ok.open("w") as fp_ok, out_ng.open("w") as fp_ng:
        create_check_code(in_nb, fp_ok, fp_ng)
