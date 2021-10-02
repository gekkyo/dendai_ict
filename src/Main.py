import logging

import chromalog
from chromalog.colorizer import GenericColorizer
from colorama import (
    Fore,
    Style,
    )

from src.controller.AppController import AppController
from src.controller.SerialController import SerialController
from src.util import Global
from src.view.AppView import AppView


def main() -> None:
    """
    メイン関数
    """
    
    colorizer = GenericColorizer(color_map = {
            'info': (Fore.GREEN, Style.RESET_ALL)
            })
    chromalog.basicConfig(level = logging.INFO, colorizer = colorizer, format = '%(asctime)s.%(msecs)03d : %(levelname)s - %(filename)s - %(message)s', datefmt = "%H:%M:%S")
    # logging.basicConfig(level = logging.INFO)
    logging.info('main')
    
    # シリアル通信
    serialController = SerialController()
    Global.serialController = serialController
    
    # GUIビュー
    appView = AppView()
    Global.appView = appView
    
    # コントローラー
    appController = AppController()
    Global.appController = appController
    
    # ウインドウ表示
    appView.show_window()
    
    # GUI処理待機
    while True:
        event, values = appView.window.read()
        appController.handle(event, values)
        if event is None:
            break
    
    # 終了
    appView.close_window()


if __name__ == '__main__':
    main()
