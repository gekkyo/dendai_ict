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
        
        pass
    
    def initGraph(self) -> None:
        pass
    
    def start(self) -> None:
        logging.info("start")
        
        self.interval = SetInterval(Global.graphDrawInterval, self.update)
    
    def stop(self) -> None:
        logging.info("stop")
        
        if self.interval is not None:
            self.interval.cancel()
    
    def update(self) -> None:
        pass
