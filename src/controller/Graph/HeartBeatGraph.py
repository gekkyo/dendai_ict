import collections
import logging

import pandas as pd
from matplotlib import pyplot as plt

from src.controller.Graph.BaseGraph import BaseGraph
from src.model.Model import Model
from src.util import Global, GraphUtil, SignalUtil


class HeartBeatGraph(BaseGraph):
    def __init__(self, parts_name: str) -> None:
        """コンストラクタ
        Args:
            parts_name (str): guiのID
        """
        logging.info("init")

        super().__init__()
        Global.graphArray.append(self)

        self.maxX = 10
        self.maxY = 200

        self.fig, self.ax = GraphUtil.init_graph(
            figsize=(6.4, 4.8), target=Global.appView.window[parts_name]
        )
        (self.line,) = self.ax.plot([], [], linewidth=0.5, color="lightslategray")  # プロット

        self.ax.set_xlim(0, self.maxX)
        self.ax.set_ylim(0, self.maxY)
        self.ax.set_xlabel("msec")
        self.ax.set_ylabel("BPM")
        plt.tight_layout()
        self.prevTime = None
        pass

    def init_graph(self) -> None:
        """グラフ初期化"""
        logging.info("init_graph")

        self.ax.set_xlim(0, self.maxX)
        self.ax.set_ylim(0, self.maxY)
        self.line.set_data([], [])
        self.prevTime = None

    def diff_to_bpm(self, x: float) -> int:
        return max(30, int(1000 / x * 60))

    def update(self) -> None:
        """データ処理"""

        data = Model.serialData.query("is_peak == 1")
        data = data.tail(30 * Global.sensorPerSecond).copy()

        # print(data)

        # データが有れば
        if len(data) > 2:

            # 1つ後の時間との差分を計算
            data["diff"] = data["time"].diff(1)

            # 欠損値の補間
            data = data.fillna({"diff": 1000})

            # bpmに直す
            data["bpm"] = data["diff"].map(self.diff_to_bpm)
            # print(data)

            # print((data.at[data.index[-1], "time"] - data.at[data.index[0], "time"]))

            # スプライン曲線
            num = int(
                (data.at[data.index[-1], "time"] - data.at[data.index[0], "time"]) / Global.splineT
            )

            # print(num)

            x_list, y_list = SignalUtil.spline1(
                data["time"].to_list(), data["bpm"].to_list(), num - 1
            )

            # BPMグラフ描画
            self.ax.set_xlim(
                data["time"].tolist()[-1] - Global.rawGraphSpan, data["time"].tolist()[-1]
            )
            x_arr = list(collections.deque(x_list, int(Global.rawGraphSpan / Global.splineT)))
            y_arr = list(collections.deque(y_list, int(Global.rawGraphSpan / Global.splineT)))
            self.ax.set_ylim(min(y_arr) - 10, max(y_arr) + 10)
            self.line.set_data(x_arr, y_arr)

            tmp_df = pd.DataFrame(list(zip(x_list, y_list)), columns=["time", "y"]).set_index(
                "time"
            )
            tmp_df.sort_index(inplace=True)

            last_time = 0
            if len(Model.bpmData) > 0:
                last_time = Model.bpmData.index.values[-1]
            append_df = tmp_df.query("time >" + str(last_time))

            # print(append_df)

            # Model.bpmData = pd.concat(Model.bpmData,append_df)
            if len(append_df) > 0:
                Model.bpmData = Model.bpmData.append(append_df)
                Model.bpmData.sort_index(inplace=True)
                # print(Model.bpmData.index.duplicated())
                # 溢れたら古いものから消す
                Model.serialData = Model.serialData.tail(Global.maxKeepSensorLength)
                # 表示を更新
                Global.appView.window["text_hb"].update(str(append_df.tail(1)["y"].values[0]))

            # self.prevTime = data.at[-1, "time"]

    def start(self, interval: float = Global.graphDrawInterval) -> None:
        """スレッド開始する

        Args:
            interval(float):呼び出す間隔
        """
        logging.info("start")

        self.init_graph()

        super().start(interval)

    def stop(self) -> None:
        """スレッド終了する"""
        logging.info("stop")

        super().stop()
