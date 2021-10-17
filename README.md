# 2021 情報通信プロジェクト (Group A)

情報通信プロジェクト グループA ポリグラフプロジェクトです。

<img alt="GUIスクリーンショット" src="https://user-images.githubusercontent.com/2655028/136725715-44bbc6ae-ea1e-4e80-821c-a9c4fb136bf9.png">

## 💻 Environment

#### OS

* MacOS 10.15.7

#### Devices

* Arduino MKR WiFi 1010
* [心拍センサ](https://pulsesensor.com/)

## 🧰 Prerequisites
#### Language

* python = ">=3.9,<3.10"

#### Libraries

* chromalog = "^1.0.5"
* PySimpleGUI = "^4.49.0"
* matplotlib = "^3.4.3"
* pathlib = "^1.0.1"
* pandas = "^1.3.3"
* scipy = "^1.7.1"
* pyserial = "^3.5"
* colorama = "^0.4.4"

## 🗂 Folder Structure

```
.
│
├ README.md .............................. 説明
│
├ .gitignore
├ .poetry.toml
├ .requirements.txt
├ .setup.cfg ............................. mypy / flake8設定
│
├ src
│ ├ Main.py .............................. メインプログラムファイル
│ ├ util
│ │ ├ fft
│ │ │ ├ MyFFT.py ......................... FFT処理
│ │ │ 〜
│ │ ├ Global.py .......................... 各種初期設定
│ │ ├ GraphUtil.py ....................... グラフ関係ユーティリティ
│ │ ├ SetInterval.py ..................... スレッド処理ユーティリティ
│ │ └ SignalUtil.py ...................... 信号処理ユーティリティ
│ ├ view
│ │ │ AppView.py ......................... GUI要素
│ │ └ Style.py ........................... GUIパーツ設定
│ ├ controller
│ │ ├ Graph
│ │ │ ├ RawGraph.py ...................... 元信号グラフ処理
│ │ │ ├ HeartBeatGraph.py ................ 心拍グラフ処理
│ │ │ ├ FftGraph.py ...................... FFTグラフ処理
│ │ │ ├ BaseGraph.py ..................... 比率グラフ処理
│ │ │ 〜
│ │ ├ AppController.py ................... メインコントローラ
│ │ └ SerialController.py ................ シリアル通信処理・ピーク検出
│ └ model
│   └ Model.py ........................... 時系列データクラス
.
```

## 🔧 Install Dependencies

### poetry

```
poetry install
```

### pip

```
pip install -r requirements.txt
```

## 🎯 Launch

### terminal

```
PYTHONPATH=./ python3 ./src/Main.py
```

### VS Code

`PYTHONPATH` を通す必要があるため、まず `setting.json` に以下を追加。

```
"python.envFile": "${workspaceFolder}/.env"
```
プロジェクトルートに `.env` ファイルを作成し以下を追加。
```
PYTHONPATH=./:${PYTHONPATH}
```
VS Codeの設定に以下を設定。(デフォルトではオフになっています)
```
"code-runner.runInTerminal": "true"
```
プロジェクトルートをワークスペースに追加し、`Main.py` を `Run Code` すれば起動します。

## ⭐ Usage

https://user-images.githubusercontent.com/2655028/137635171-29106e66-53e3-4e16-95f4-425a2474b555.mp4


## 🙆 Contributors

このプロジェクトは [東京電機大学](https://www.dendai.ac.jp/) 工学部に所属する以下のメンバーで作成しました。

#### 海辺康志(17NC011) / 高橋和希(18EC067) / 高橋凌矢(18EC069) / 山下健太郎(18NC063)

