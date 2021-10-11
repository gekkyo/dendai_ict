from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.controller.AppController import AppController
    from src.controller.Graph.BaseGraph import BaseGraph
    from src.controller.Graph.FftGraph import FftGraph
    from src.controller.Graph.HeartBeatGraph import HeartBeatGraph
    from src.controller.Graph.RatioGraph import RatioGraph
    from src.controller.Graph.RawGraph import RawGraph
    from src.controller.SerialController import SerialController
    from src.view.AppView import AppView

# 初期ポート
initialPort = "/dev/cu.usbmodem14301"

# ルート階層
root_path = pathlib.Path("../")

# csv書き出しディレクトリ
outDir = pathlib.Path(root_path, "output/")

# コンフィグ設定
settings_file = pathlib.Path(root_path, r"settings_file.cfg")
settings_default = {"raw_csv": None, "port": initialPort}
settings: dict = {}

# センサー取得インターバル(sec)
getSerialInterval = 0.1

# グラフ描画インターバル(sec)
graphDrawInterval = 0.2

# FFTインターバル(sec)
graphFftInterval = 0.5

# センサーの取得間隔(msec)
sensorInterval = 20

# 秒間データが何個あるか
sensorPerSecond = int(1000 / sensorInterval)

# 山を調べるための間隔(sec * 秒間の個数)
numOfSample = 2 * sensorPerSecond

# センサー値をいくつ保管するか(60sec * 3min * 秒間の個数)
maxKeepSensorLength = 60 * 3 * sensorPerSecond

# 最大値を見つけるためにいくつずつずらして調べるか(msec)
rollingSpan = 300
rollingWindow = int(rollingSpan / sensorInterval)

# グラフ表示スパン
rawGraphSpan = 30 * 1000

# グラフ表示内にいくつデータが有るか
rawGraphNumSignal = 30 * sensorPerSecond

# スプライン曲線の周期
splineT = 10
splineFreq = splineT / 1000
splineNumPerSecond = 1000 / splineT

# 補間値をいくつ保管するか(60sec * 3min * 秒間の個数)
maxKeepBpmLength = 60 * 3 * splineNumPerSecond

divideNumPerHz = 100

# ベースライン計測に必要な最低時間
requiredBaseDuration = 1 * 1000

# FFTの範囲(秒)
maxFftInterval = 82

# ベース計測開始時刻
baseStartTime = 0
baseEndTime = 0

# 本計測開始時刻
testStartTime = 0
testEndTime = 0

# 各種クラスへの参照
appView: AppView
serialController: SerialController
appController: AppController

# 各種グラフへの参照
graph_raw: RawGraph
graph_hb: HeartBeatGraph
graph_fft: FftGraph
graph_ratio: RatioGraph
graphArray: list[BaseGraph] = []
