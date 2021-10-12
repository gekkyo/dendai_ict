import logging
from decimal import Decimal
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

        self.fig, self.ax, self.figAgg = GraphUtil.init_graph(
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

        self.line.set_data([], [])

    def set_baseline(self) -> None:
        """ベースのFFTグラフ作成"""
        logging.info("set_baseline")

        tail_num: int = int(
            min(len(Model.baselineBpmData), Global.maxFftInterval * Global.splineNumPerSecond)
        )
        data = Model.baselineBpmData.tail(tail_num).copy()
        data = data["y"].tolist()

        # グラフ描画
        x_list, y_list = self.draw_fft_graph(np.array(data), self.baseline)

        # 面積と比率を計算
        self.base_area_measurement = (
            sum(y_list[5 : 15 + 1] / 100),
            sum(y_list[15 : 40 + 1] / 100),
        )

        if self.base_area_measurement[1] != 0:
            cur_ratio = Decimal(self.base_area_measurement[0]) / Decimal(
                self.base_area_measurement[1]
            )
        else:
            cur_ratio = Decimal(1)

        # 表示を更新
        Global.appView.window["text_lf"].update(str(round(self.base_area_measurement[0], 5)))
        Global.appView.window["text_hf"].update(str(round(self.base_area_measurement[1], 5)))
        Global.appView.window["text_ratio"].update(str(round(cur_ratio, 5)))

    def update(self) -> None:
        """データ処理"""

        tail_num: int = int(
            min(len(Model.bpmData), Global.maxFftInterval * Global.splineNumPerSecond)
        )
        data = Model.bpmData.tail(tail_num).copy()

        # データが有れば
        if len(data) > 2:
            self.currentTime = data.tail(1).index.values[0]

            # 新しい心拍データが無ければ無視
            if len(Model.ratioData) > 0 and Model.ratioData.index.values[-1] == self.currentTime:
                return

            # グラフ描画・面積・比率計算
            np_data = data["y"].tolist()
            x_list, y_list = self.draw_fft_graph(np.array(np_data), self.line)
            cur_area_measurement = (sum(y_list[5 : 15 + 1] / 100), sum(y_list[15 : 40 + 1] / 100))

            if cur_area_measurement[1] != 0:
                cur_ratio = Decimal(cur_area_measurement[0]) / Decimal(cur_area_measurement[1])
            else:
                cur_ratio = Decimal(1)

            # 表示を更新
            Global.appView.window["text_lf"].update(str(round(cur_area_measurement[0], 5)))
            Global.appView.window["text_hf"].update(str(round(cur_area_measurement[1], 5)))
            Global.appView.window["text_ratio"].update(str(round(cur_ratio, 5)))

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

        # print(n)

        # ハニング窓
        # hamming = np.hamming(n)  # type: ignore

        # fft
        f = MyFFT.my_fft(p_data)

        # FFTの複素数結果を絶対に変換
        f_abs = np.abs(f)

        # 交流成分はデータ数で割って2倍する
        f_abs_amp = f_abs / n * 2

        # 直流成分は2倍不要
        f_abs_amp[0] = f_abs_amp[0] / 2
        f_abs_amp[0] = 0

        # f_abs_amp_std = min_max_normalize(f_abs_amp)

        # 周波数軸
        freq = np.linspace(0, 1.0 / Global.splineFreq, n)

        x_avg, y_avg = SignalUtil.moving_avg(freq, f_abs_amp)

        # 補間(1hzを100個に分割)
        x_list, y_list = SignalUtil.spline1(
            x_avg, y_avg, (x_avg[-1] - x_avg[0]) * Global.divideNumPerHz, "cubic"
        )

        # グラフ描画
        self.ax.set_ylim(min(y_list), max(y_list))
        # self.ax.set_xlim(min(x_list), max(x_list))
        line.set_data(x_list, y_list)

        # self.ax.collections.clear()
        # self.ax.fill_between(
        #     x_list,
        #     0,
        #     y_list,
        #     where=(0.05 <= x_list) & (x_list <= 0.15),
        #     facecolor="lightcyan",
        #     interpolate=True,
        # )
        # self.ax.fill_between(
        #     x_list,
        #     0,
        #     y_list,
        #     where=(0.15 <= x_list) & (x_list <= 0.40),
        #     facecolor="lavenderblush",
        #     interpolate=True,
        # )

        return x_list, y_list

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
