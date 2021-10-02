import threading
import time
from typing import Any


class SetInterval:
    
    def __init__(self, interval: float, action: Any) -> None:
        """
        コンストラクタ
        Args:
            interval (float): 呼び出し間隔
            action (Any): 呼ぶ出す関数
        """
        
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target = self.__setInterval)
        thread.start()
    
    def __setInterval(self) -> None:
        """
        スレッド処理
        """
        
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            t = threading.Thread(target = self.action)
            t.daemon = True
            t.start()
    
    def cancel(self) -> None:
        """
        スレッドを止める
        """
        
        self.stopEvent.set()
