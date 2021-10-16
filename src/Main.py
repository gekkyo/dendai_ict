import logging
from json import dump as json_dump
from json import load as json_load
from os import PathLike

import chromalog
import PySimpleGUI as sg
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

    Global.settings = load_settings(Global.settings_file, Global.settings_default)

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
        event, values = app_view.window.read(timeout=10)
        if event == sg.TIMEOUT_EVENT:
            continue
        if event == sg.WIN_CLOSED:
            break
        app_controller.handle(event, values)

    # 終了
    save_settings(Global.settings_file, Global.settings)
    app_view.close_window()


def load_settings(settings_file: PathLike, default_settings: dict) -> dict:
    """設定ファイルを読み込む
    Args:
        settings_file(PathLike):設定ファイルのパス
        default_settings(dict): デフォルト設定

    Returns:
        dict:設定
    """
    logging.info("load_settings")

    try:
        with open(settings_file, "r") as f:
            settings = json_load(f)
    except Exception:
        logging.warning("設定ファイル作成")
        settings = default_settings
        save_settings(settings_file, settings)
    return settings


def save_settings(settings_file: PathLike, settings: dict) -> None:
    """設定ファイルを保存
    Args:
        settings_file(PathLike):設定ファイルのパス
        settings(dict): 設定
    """
    logging.info("save_settings")

    with open(settings_file, "w") as f:
        json_dump(settings, f)


if __name__ == "__main__":
    main()
