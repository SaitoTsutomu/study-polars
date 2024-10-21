from pathlib import Path

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def show_score(dir_="work", file="study_polars.ipynb"):
    with (Path(dir_) / file).open() as fp:
        nb = nbformat.read(fp, as_version=4)
    ep = ExecutePreprocessor(timeout=60, kernel_name="python3")
    nb_out = ep.preprocess(nb, {"metadata": {"path": dir_}})[0]
    n_ok = n_ng = 0
    for cell in nb_out["cells"]:
        if cell["cell_type"] != "code":
            continue
        outputs = cell.get("outputs", [])
        text = "".join(output["text"] for output in outputs if output["output_type"] == "stream")
        if text.startswith("\x1b[31mOK"):
            n_ok += 1
        elif text.startswith("\x1b[31mNG"):
            n_ng += 1
    rate = n_ok / (n_ok + n_ng)
    print(f"{n_ok + n_ng}問中 {n_ok}問正解({rate:.0%})")
    if rate == 0:
        print("ここからスタートだ!")
    elif rate < 0.2:
        print("やったね! 少し進んだよ")
    elif rate < 0.5:
        print("いいね! 半分正解したよ")
    elif rate < 0.8:
        print("素晴らしい! ほぼ完璧")
    else:
        print("完璧! おめでとう!")


if __name__ == "__main__":
    show_score()
