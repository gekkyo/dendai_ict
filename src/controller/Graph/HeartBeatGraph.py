import collections
import logging

import pandas as pd
from matplotlib import pyplot as plt

from src.controller.Graph.BaseGraph import BaseGraph
from src.model.Model import Model
from src.util import Global, GraphUtil, SignalUtil


class HeartBeatGraph(BaseGraph):
    
    def __init__(self, partsname: str) -> None:
        """コンストラクタ
        Args:
            partsname (str): guiのID
        """
        logging.info("init")
        
        super().__init__()
        
        self.ax = GraphUtil.init_graph(figsize = (6.4, 2.4), target = Global.appView.window[partsname])
        self.line, = self.ax.plot([], [], linewidth = 0.5, color = "lightslategray")  # プロット
        
        self.ax.set_ylim(0, 1000)
        self.ax.set_xlim(0, 10)
        self.ax.set_xlabel("msec")
        self.ax.set_ylabel("BPM")
        plt.tight_layout()
        self.prevTime = None
        pass
    
    def initGraph(self) -> None:
        """グラフ初期化"""
        logging.info("init_garph")
        
        self.ax.set_ylim(0, 1000)
        self.ax.set_xlim(0, 10)
        self.line.set_data([], [])
        self.prevTime = None
    
    def update(self) -> None:
        """データ処理"""

        data = Model.serialData.query("is_peak == 1")
        data = data.tail(30 * Global.sensorPerSecond).copy()
        
        # print(data)
        
        # データが有れば
        if len(data) > 2:
            data["diff"] = data["time"].diff(1)
            data = data.fillna({"diff": 1000})
            func = lambda x: max(40, int(1000 / x * 60))
            data["bpm"] = data["diff"].map(func)
            # print(data)
            
            # print((data.at[data.index[-1], "time"] - data.at[data.index[0], "time"]))
            
            # スプライン曲線
            num = int((data.at[data.index[-1], "time"] - data.at[data.index[0], "time"]) / Global.splineT)
            xlist, ylist = SignalUtil.spline1(data["time"].to_list(), data["bpm"].to_list(), num)
            #
            # print(num)
            # print(y)
            
            # BPMグラフ描画
            self.ax.set_xlim(data["time"].tolist()[-1] - Global.rawGraphSpan, data["time"].tolist()[-1])
            xArr = list(collections.deque(xlist, int(Global.rawGraphSpan / Global.splineT)))
            yArr = list(collections.deque(ylist, int(Global.rawGraphSpan / Global.splineT)))
            self.ax.set_ylim(min(yArr) - 10, max(yArr) + 10)
            self.line.set_data(xArr, yArr)
            
            tmp_df = pd.DataFrame(list(zip(xlist, ylist)), columns = ["time", "y"]).set_index("time")
            tmp_df.sort_index(inplace = True)
            #     tmp_df.append(pd.DataFrame(data = {"y": ylist[index]}, index = [xval]))
            #
            # Model.bpmData.update(tmp_df)
            
            lastTime = 0
            if len(Model.bpmData) > 0:
                lastTime = Model.bpmData.index.values[-1]
            append_df = tmp_df.query("time >" + str(lastTime))
            
            # print(append_df)
            
            # Model.bpmData = pd.concat(Model.bpmData,append_df)
            if len(append_df) > 0:
                Model.bpmData = Model.bpmData.append(append_df)
                Model.bpmData.sort_index(inplace = True)
                # print(Model.bpmData.index.duplicated())
                # 溢れたら古いものから消す
                Model.serialData = Model.serialData.tail(Global.maxKeepSensorLength)
            
            # self.prevTime = data.at[-1, "time"]

    def start(self) -> None:
        """スレッド開始する"""
        logging.info("start")
    
        self.initGraph()
    
        super().start()

    def stop(self) -> None:
        """スレッド終了する"""
        logging.info("stop")
    
        super().stop()
