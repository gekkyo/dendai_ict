import logging

from matplotlib import pyplot as plt

from src.controller.Graph.BaseGraph import BaseGraph
from src.util import Global, GraphUtil


class RatioGraph(BaseGraph):
    
    def __init__ (self, partsname:str)->None:
        """コンストラクタ
        Args:
            partsname (str): guiのID
        """
        
        logging.info("init")
        
        super().__init__()
        
        self.ax = GraphUtil.init_graph(figsize = (6.4, 1.8),
                                       target = Global.appView.window[partsname])
        self.line, = self.ax.plot([], [], linewidth = 0.5, color = "lightslategray")  # プロット
        self.ax.set_ylim(0, 1000)
        self.ax.set_xlim(0, 10)
        self.ax.set_xlabel("msec")
        self.ax.set_ylabel("RATIO")
        plt.tight_layout()
        pass
    
    def initGraph(self)->None:
        """グラフ初期化"""
        logging.info("init_garph")
        
        self.ax.set_ylim(0, 1000)
        self.ax.set_xlim(0, 10)
        self.line.set_data([], [])
    
    def update (self)->None:
        pass
