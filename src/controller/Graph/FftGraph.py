import logging
from typing import Any

import numpy as np
import numpy.typing as npt
import pandas as pd
from matplotlib import pyplot as plt

from src.controller.Graph.BaseGraph import BaseGraph
from src.model.Model import Model
from src.util import Global, GraphUtil, SignalUtil
from src.util.fft import MyFFT


class FftGraph(BaseGraph):
    def __init__(self, parts_name: str) -> None:
        """コンストラクタ
        Args:
            parts_name (str): guiのID
        """

        logging.info("init")

        super().__init__()
        Global.graphArray.append(self)

        self.maxX = 1
        self.maxY = 20

        self.fig, self.ax = GraphUtil.init_graph(
            figsize=(6.4, 4.8), target=Global.appView.window[parts_name]
        )
        (self.baseline,) = self.ax.plot([], [], linewidth=0.3, color="silver")  # プロット
        (self.line,) = self.ax.plot([], [], linewidth=0.5, color="lightslategray")  # プロット
        self.ax.set_xlim(0, self.maxX)
        self.ax.set_ylim(0, self.maxY)
        self.ax.set_xlabel("Hz")
        self.ax.set_ylabel("FTT")
        # self.ax.set_yscale("symlog")

        self.base_area_measurement = (0, 0)
        self.currentTime = 0

        plt.tight_layout()

        pass

    def init_graph(self) -> None:
        """グラフ初期化"""
        logging.info("init_graph")

        self.ax.set_xlim(0, self.maxX)
        self.ax.set_ylim(0, self.maxY)
        self.baseline.set_data([], [])
        self.line.set_data([], [])
        self.base_area_measurement = (0, 0)
        self.currentTime = 0

    def reset_main_graph(self) -> None:
        """ベースライン以外のグラフ初期化"""
        logging.info("reset_main_graph")

        # self.ax.set_ylim(0, self.maxy)
        # self.ax.set_xlim(0, self.maxHz)
        self.line.set_data([], [])

    def set_baseline(self) -> None:
        """ベースのFFTグラフ作成"""
        logging.info("set_baseline")

        # Model.baselineBpmData.to_csv("../output/beat.csv")
        print(Model.baselineBpmData)
        data = (
            Model.baselineBpmData["y"]
            .tail(Global.maxFftInterval * Global.splineNumPerSecond)
            .copy()
            .tolist()
        )

        x_list, y_list = self.draw_fft_graph(np.array(data), self.baseline)

        self.base_area_measurement = (sum(y_list[5 : 15 + 1]), sum(y_list[15 : 40 + 1]))

        # print(self.base_area_measurement)
        # print(self.base_area_measurement[0] / self.base_area_measurement[1])

        # 表示を更新
        Global.appView.window["text_lf"].update(str(round(self.base_area_measurement[0])))
        Global.appView.window["text_hf"].update(str(round(self.base_area_measurement[1])))
        Global.appView.window["text_ratio"].update(
            str(round(self.base_area_measurement[0] / self.base_area_measurement[1], 3))
        )

    def update(self) -> None:
        """データ処理"""

        data = Model.bpmData.tail(Global.maxFftInterval * 100).copy()

        # データが有れば
        if len(data) > 2:
            self.currentTime = data.tail(1).copy().index.values[0]

            np_data = data["y"].tolist()
            x_list, y_list = self.draw_fft_graph(np.array(np_data), self.line)
            cur_area_measurement = (sum(y_list[5 : 15 + 1]), sum(y_list[15 : 40 + 1]))

            # 表示を更新
            Global.appView.window["text_lf"].update(str(round(cur_area_measurement[0])))
            Global.appView.window["text_hf"].update(str(round(cur_area_measurement[1])))
            Global.appView.window["text_ratio"].update(
                str(round(cur_area_measurement[0] / cur_area_measurement[1], 3))
            )
            Global.appView.window["text_sub"].update(
                str(
                    round(
                        self.base_area_measurement[0] / self.base_area_measurement[1]
                        - cur_area_measurement[0] / cur_area_measurement[1],
                        3,
                    )
                )
            )

            # データを追加してゆく
            Model.ratioData = Model.ratioData.append(
                pd.DataFrame(
                    data={"y": cur_area_measurement[0] / cur_area_measurement[1]},
                    index=[self.currentTime],
                )
            )

    def draw_fft_graph(self, data: npt.NDArray, line: Any) -> tuple[npt.NDArray, npt.NDArray]:
        """FFTグラフを書く
        Args:
            data(npt.NDArray):データ配列
            line(Any):描画対象のライン
        Returns:
            tuple[npt.NDArray, npt.NDArray]:パワースペクトルのx,yのリスト
        """
        # 2のべき乗個に揃える
        n = SignalUtil.prev_pow_2(len(data))
        p_data = data[-n:]

        print(n)

        # ハミング窓
        hamming = np.hamming(n)  # type: ignore
        # fft
        # f = np.fft.fft(p_data * hamming)
        f = MyFFT.my_fft(p_data * hamming)
        # print(f)
        # 振幅パワースペクトル
        amp = np.abs(f) / n
        freq = np.linspace(0, 1.0 / Global.splineFreq, n)  # 周波数軸
        #
        # print("amp")
        # print(amp)
        #
        # 補間
        x_list, y_list = SignalUtil.spline1(freq, amp, (1.0 / Global.splineFreq) * 100)

        # グラフ描画
        self.ax.set_ylim(0, max(y_list))

        line.set_data(x_list, y_list)

        return x_list, y_list

        # print((1.0 / Global.splineFreq) / n)

    def start(self, interval: float = Global.graphFftInterval) -> None:
        """スレッド開始する

        Args:
            interval(float):呼び出す間隔
        """
        logging.info("start")

        self.reset_main_graph()

        super().start(interval)

    def stop(self) -> None:
        """スレッド終了する"""
        logging.info("stop")

        super().stop()
