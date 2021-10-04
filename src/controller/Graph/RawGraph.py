import collections
import logging

import matplotlib.pyplot as plt

from src.controller.Graph.BaseGraph import BaseGraph
from src.model.Model import Model
from src.util import GraphUtil, Global


class RawGraph(BaseGraph):
    
    def __init__(self, partsname: str) -> None:
        """コンストラクタ
        Args:
            partsname (str): guiのID
        """
        logging.info("init")
        
        super().__init__()
        
        self.ax = GraphUtil.init_graph(figsize = (6.4, 2.4), target = Global.appView.window[partsname])
        
        self.line, = self.ax.plot([], [], linewidth = 0.5, color = "lightslategray")  # プロット
        # self.filtered_line, = self.ax.plot([], [], linewidth = 0.5, color="green")  # プロット
        self.scatter = self.ax.scatter([], [])
        self.ax.set_ylim(0, 1000)
        self.ax.set_xlim(0, 10)
        self.ax.set_xlabel("msec")
        self.ax.set_ylabel("Sensor Value")
        plt.tight_layout()
        pass
    
    def initGraph(self) -> None:
        """グラフ初期化"""
        logging.info("init_garph")
        
        self.ax.set_ylim(0, 1000)
        self.ax.set_xlim(0, 10)
        self.line.set_data([], [])
        self.scatter.set_offsets([[0, 0]])
    
    def update(self) -> None:
        """データ処理"""
        
        data = Model.serialData
        
        # データが有れば
        if len(data) > 0:
            
            # ECGグラフ描画
            self.ax.set_xlim(data["time"].tolist()[-1] - Global.rawGraphSpan, data["time"].tolist()[-1])
            xArr = list(collections.deque(data["time"].values.tolist(), Global.rawGraphNumSignal))
            yArr = list(collections.deque(data["raw"].values.tolist(), Global.rawGraphNumSignal))
            self.ax.set_ylim(min(yArr) - 20, max(yArr) + 20)
            self.line.set_data(xArr, yArr)
            
            # ピーク描画
            peaks = data.query("is_peak == 1")
            peaks_pos = []
            for idx in range(peaks.shape[0]):
                xpos = peaks.at[peaks.index[idx], "time"]
                ypos = peaks.at[peaks.index[idx], "raw"]
                peaks_pos.append([xpos, ypos])
            
            if len(peaks_pos) > 0:
                self.scatter.set_offsets(peaks_pos)
    
    def start(self) -> None:
        """スレッド開始する"""
        logging.info("start")
        
        self.initGraph()
        
        super().start()
    
    def stop(self) -> None:
        """スレッド終了する"""
        logging.info("stop")
        
        super().stop()
