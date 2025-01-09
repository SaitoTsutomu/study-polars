# Polars入門

## はじめに

これはPolars 1.19.0の学習用の教材です。

https://polars-ja.github.io/docs-ja/

※ 「データサイエンティスト協会スキル定義委員」の「データサイエンス100本ノック（構造化データ加工編）」を参考にしています。

## 準備

`uv`をインストールしてください。

https://docs.astral.sh/uv/

リポジトリ一式をダウンロードして解凍してください。

```
curl -L -o study-polars.zip https://github.com/SaitoTsutomu/study-polars/archive/refs/heads/master.zip
unzip study-polars.zip
cd study-polars-master
```

## 学習開始

教材は、`nbs/study_polars.ipynb`です。
次のコマンドを実行すると、教材を`work/study_polars.ipynb`にコピーし、Jupyterが起動します。

```
uv run study-polars
```

※ `work/study_polars.ipynb`が存在する場合はコピーしません。2回目以降は続きから学習できます。もし、新規に始めたい場合は、`uv run study-polars --new`としてください。

`study_polars.ipynb`を開いて学習を始めてください。

### 手順

* 青いセルの説明を読む
* 白いセルに問題の解答を書く
* 黄色いセルを実行して確認する

セル内でしか使わない変数は、`_`で始まります。
