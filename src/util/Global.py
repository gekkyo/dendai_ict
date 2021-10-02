from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.controller.Graph.BaseGraph import BaseGraph
    from src.controller.AppController import AppController
    from src.controller.Graph.RawGraph import RawGraph
    from src.controller.Graph.FftGraph import FftGraph
    from src.controller.Graph.HeartBeatGraph import HeartBeatGraph
    from src.controller.Graph.RatioGraph import RatioGraph
    from src.controller.SerialController import SerialController
    from src.view.AppView import AppView

# 初期ポート
initialPort = '/dev/cu.usbmodem14401'

# 書き出しディレクトリ
outDir = pathlib.Path("../output/")

# センサー取得インターバル
getSerialInterval = 0.1

# グラフ描画インターバル
graphDrawInterval = 0.1

# センサーの取得間隔(msec)
sensorInterval = 20

# 秒間データが何個あるか
sensorPerSecond = int(1000 / sensorInterval)

# 山を調べるための窓間隔
numOfSample = 2 * sensorPerSecond

# センサー値をいくつ保管するか
maxKeepSensorLength = 60 * 2 * sensorPerSecond

# 最大値を見つけるためにいくつずつずらして調べるか
rollingSpan = 200
rollingWindow = int(rollingSpan / sensorInterval)

# グラフ表示スパン
rawGraphSpan = 15 * 1000

# スプライン曲線の周期
splineT = 10

# グラフ表示内にいくつデータが有るか
rawGraphNumSignal = 15 * sensorPerSecond

# ベースライン計測に必要な最低時間
requiredBaseDuration = 1 * 1000

# ベース計測開始時刻
baseStartTime = 0
baseEndTime = 0

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
