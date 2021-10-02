import logging

from matplotlib import pyplot as plt

from src.controller.Graph.BaseGraph import BaseGraph
from src.util import Global, GraphUtil


class FftGraph(BaseGraph):
    
    def __init__(self, partsname: str) -> None:
        """
        コンストラクタ
        
        Args:
            partsname (str): guiのID
        """
        
        logging.info("init")
        
        super().__init__()
        
        self.ax = GraphUtil.init_graph(figsize = (6.4, 3.0),
                                       target = Global.appView.window[partsname])
        self.baseline, = self.ax.plot([], [], linewidth = 0.3, color = "silver")  # プロット
        self.line, = self.ax.plot([], [], linewidth = 0.5, color = "lightslategray")  # プロット
        self.ax.set_ylim(0, 1000)
        self.ax.set_xlim(0, 10)
        self.ax.set_xlabel("msec")
        self.ax.set_ylabel("FTT")
        plt.tight_layout()
        pass
    
    def initGraph(self)->None:
        self.ax.set_ylim(0, 1000)
        self.ax.set_xlim(0, 10)
        self.baseline.set_data([], [])
        self.line.set_data([], [])
    
    def setBaseline(self)->None:
        pass
    
    def update(self)->None:
        pass
