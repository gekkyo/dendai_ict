import logging
import typing

from matplotlib.pyplot import axes

from src.util import Global
from src.util.SetInterval import SetInterval


class BaseGraph:
    
    def __init__(self) -> None:
        """
        コンストラクタ
        """
        logging.info("init")
        
        Global.graphArray.append(self)
        
        self.ax: axes
        self.interval: typing.Optional[SetInterval] = None
        
    
    def initGraph(self) -> None:
        """グラフ初期化"""
        pass
    
    def start(self) -> None:
        """スレッド開始"""
        logging.info("start")
        
        self.interval = SetInterval(Global.graphDrawInterval, self.update)
    
    def stop(self) -> None:
        """スレッド終了"""
        logging.info("stop")
        
        if self.interval is not None:
            self.interval.cancel()
    
    def update(self) -> None:
        """スレッド処理"""
        pass
