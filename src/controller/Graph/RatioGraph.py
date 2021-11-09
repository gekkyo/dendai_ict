import logging

from matplotlib import pyplot as plt

from src.controller.Graph.BaseGraph import BaseGraph
from src.model.Model import Model
from src.util import Global, GraphUtil


class RatioGraph(BaseGraph):
    def __init__(self, parts_name: str) -> None:
        """コンストラクタ
        Args:
            parts_name (str): guiのID
        """
        logging.info("init")

        super().__init__()
        Global.graphArray.append(self)

        self.maxX = 100
        self.maxY = 5

        self.fig, self.ax, self.figAgg = GraphUtil.init_graph(
            figsize=(6.4, 4.8), target=Global.appView.window[parts_name]
        )
        (self.line,) = self.ax.plot([], [], linewidth=0.5, color="lightslategray")  # プロット
        self.ax.set_xlim(0, self.maxX)
        self.ax.set_ylim(0, self.maxY)
        self.ax.set_xlabel("msec")
        self.ax.set_ylabel("RATIO")
        plt.tight_layout()
        pass

    def init_graph(self) -> None:
        """グラフ初期化"""
        logging.info("init_graph")

        self.ax.set_xlim(0, self.maxX)
        self.ax.set_ylim(0, self.maxY)
        self.line.set_data([], [])

    def update(self) -> None:
        """データ処理"""

        tail_num = int(min(len(Model.ratioData), Global.rawGraphNumSignal))
        data = Model.ratioData.tail(tail_num).copy()

        # データが有れば
        if len(data) > 2:
            # グラフ描画
            base_ratio = (
                Global.graph_fft.base_area_measurement[0]
                / Global.graph_fft.base_area_measurement[1]
            )
            # print(base_ratio)
            x_arr = data.index.values.tolist()
            y_arr = data["y"].values.tolist()
            y_arr = y_arr / base_ratio
            self.ax.set_xlim(x_arr[-1] - Global.rawGraphSpan, x_arr[-1])
            self.ax.set_ylim(min(y_arr) - 0.1, max(y_arr) + 0.1)
            self.line.set_data(x_arr, y_arr)

            # テキスト更新
            Global.appView.window["text_sub"].update(str(round(y_arr[-1], 5)))

            # 溢れたら古いものから消す
            Model.ratioData = Model.ratioData.tail(Global.maxKeepSensorLength)

    def start(self, interval: float = Global.graphFftInterval) -> None:
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
