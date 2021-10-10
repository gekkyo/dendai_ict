import collections
import logging

import matplotlib.pyplot as plt

from src.controller.Graph.BaseGraph import BaseGraph
from src.model.Model import Model
from src.util import Global, GraphUtil


class RawGraph(BaseGraph):
    def __init__(self, parts_name: str) -> None:
        """コンストラクタ
        Args:
            parts_name (str): guiのID
        """
        logging.info("init")

        super().__init__()
        Global.graphArray.append(self)

        self.maxX = 10
        self.maxY = 1000

        self.fig, self.ax = GraphUtil.init_graph(
            figsize=(6.4, 4.8), target=Global.appView.window[parts_name]
        )

        (self.line,) = self.ax.plot([], [], linewidth=0.7, color="lightslategray")
        # self.filtered_line, = self.ax.plot([], [], linewidth = 0.5, color="green")
        self.scatter = self.ax.scatter([], [], zorder=3)
        self.ax.set_xlim(0, self.maxX)
        self.ax.set_ylim(0, self.maxY)
        self.ax.set_xlabel("msec")
        self.ax.set_ylabel("Sensor Value")
        plt.tight_layout()
        pass

    def init_graph(self) -> None:

        """グラフ初期化"""
        logging.info("init_graph")

        self.ax.set_xlim(0, self.maxX)
        self.ax.set_ylim(0, self.maxY)
        self.line.set_data([], [])
        self.scatter.set_offsets([[0, 0]])

    def update(self, force: bool = False) -> None:
        """データ処理"""

        data = Model.serialData.copy()

        # print(data)

        # データが有れば
        if len(data) > 0:

            # ECGグラフ描画
            self.ax.set_xlim(
                data["time"].tolist()[-1] - Global.rawGraphSpan, data["time"].tolist()[-1]
            )

            x_arr = list(collections.deque(data["time"].values.tolist(), Global.rawGraphNumSignal))
            y_arr = list(collections.deque(data["raw"].values.tolist(), Global.rawGraphNumSignal))
            self.ax.set_ylim(min(y_arr) - 20, max(y_arr) + 20)
            self.line.set_data(x_arr, y_arr)
            # self.fig.canvas.draw()

            # ピーク描画
            peaks = data.query("is_peak == 1")
            peaks_pos = []
            for idx in range(peaks.shape[0]):
                x_pos = peaks.at[peaks.index[idx], "time"]
                y_pos = peaks.at[peaks.index[idx], "raw"]
                peaks_pos.append([x_pos, y_pos])

            if len(peaks_pos) > 0:
                self.scatter.set_offsets(peaks_pos)

            if Global.baseStartTime != 0:
                if Global.baseEndTime == 0:
                    self.ax.axvspan(Global.baseStartTime, self.ax.get_xlim()[1], color="beige")
                else:
                    self.ax.axvspan(Global.baseStartTime, Global.baseEndTime, color="beige")

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
