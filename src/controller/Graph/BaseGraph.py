import logging
import typing

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.util.SetInterval import SetInterval


class BaseGraph:
    def __init__(self) -> None:
        """コンストラクタ"""
        logging.info("init")

        self.ax: Axes
        self.fig: Figure
        self.interval: typing.Optional[SetInterval] = None

    def init_graph(self) -> None:
        """グラフ初期化"""
        pass

    def start(self, interval: float) -> None:
        """スレッド開始"""
        logging.info("start")

        self.interval = SetInterval(interval, self.update)

    def stop(self) -> None:
        """スレッド終了"""
        logging.info("stop")

        if self.interval is not None:
            self.interval.cancel()

    def update(self) -> None:
        """スレッド処理"""
        pass
