import logging
import threading
import time
from typing import Any


class SetInterval:
    def __init__(self, interval: float, action: Any) -> None:
        """コンストラクタ
        Args:
            interval (float): 呼び出し間隔
            action (Any): 呼ぶ出す関数
        """
        logging.info("init")

        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__set_interval)
        thread.start()

    def __set_interval(self) -> None:
        """スレッド処理"""

        next_time = time.time() + self.interval
        while not self.stopEvent.wait(next_time - time.time()):
            next_time += self.interval
            t = threading.Thread(target=self.action)
            t.daemon = True
            t.start()

    def cancel(self) -> None:
        """スレッドを止める"""
        logging.info("cancel")

        self.stopEvent.set()
