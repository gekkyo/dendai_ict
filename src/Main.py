import logging

import chromalog
from chromalog.colorizer import GenericColorizer
from colorama import Fore, Style

from src.controller.AppController import AppController
from src.controller.SerialController import SerialController
from src.util import Global, GraphUtil
from src.view.AppView import AppView


def main() -> None:
    """メイン関数"""

    # ログ設定
    colorizer = GenericColorizer(color_map={"info": (Fore.GREEN, Style.RESET_ALL)})
    chromalog.basicConfig(
        level=logging.INFO,
        colorizer=colorizer,
        format="%(asctime)s.%(msecs)03d : %(levelname)s - %(filename)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    # logging.basicConfig(level = logging.INFO)
    logging.info("main")

    # matplotlib初期化
    GraphUtil.init()

    # シリアル通信
    serial_controller = SerialController()
    Global.serialController = serial_controller

    # GUIビュー
    app_view = AppView()
    Global.appView = app_view

    # コントローラー
    app_controller = AppController()
    Global.appController = app_controller

    # グラフ用意
    app_view.prepare_graph()
    # ポート選択初期化
    serial_controller.update_port_selection()

    # GUI処理待機
    while True:
        event, values = app_view.window.read()
        app_controller.handle(event, values)
        if event is None:
            break

    # 終了
    app_view.close_window()


if __name__ == "__main__":
    main()
