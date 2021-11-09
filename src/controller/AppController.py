import logging
import pathlib
import time
from typing import Any

import PySimpleGUI as sg
import pandas as pd

from src.model.Model import Model
from src.util import Global, GraphUtil


class AppController:
    def __init__(self) -> None:
        """コンストラクタ"""
        logging.info("init")

        self.values: Any = None

    def handle(self, event_key: str, values: Any) -> None:
        """イベントごとに呼ばれる
        Args:
            event_key(str): イベントが起きたパーツのID
            values(Any): イベントでの値
        """
        logging.info("AppController:handle")
        # logging.info(event_key)

        # 外部から値参照するためクラスに保存
        self.values = values
        try:
            eval("self." + event_key + "()")
        except Exception:
            pass

    def btn_refresh(self) -> None:
        """ポートリロードボタン"""
        logging.info("btn_refresh")

        Global.serialController.update_port_selection()

    def btn_connect(self) -> None:
        """接続ボタン"""
        logging.info("btn_connect")

        if Global.serialController.open_serial():
            # 通信開始

            # ボタン類
            Global.appView.window["btn_connect"].update(disabled=True)

            if len(Model.baselineSerialData) == 0:
                # ベースライン計測できるように
                Global.appView.window["btn_base_start"].update(disabled=False)
                Global.appView.window["btn_load_raw"].update(disabled=False)
            else:
                Global.appView.window["btn_test_start"].update(disabled=False)

            # シリアル通信開始
            Global.serialController.start()
            # グラフ描画開始
            Global.graph_raw.start()
            Global.graph_hb.start()

    def btn_base_start(self) -> None:
        """ベース計測開始ボタン"""
        logging.info("btn_base_start")

        Global.baseStartTime = 0
        Global.baseEndTime = 0
        Global.testStartTime = 0
        Global.testEndTime = 0

        # ボタン
        Global.appView.window["btn_base_start"].update(disabled=True)
        Global.appView.window["btn_base_stop"].update(disabled=False)

        # 開始時間保存
        Global.baseStartTime = Model.serialData.time.values[-1]
        Global.baseEndTime = 0

    def btn_base_stop(self) -> None:
        """ベース計測停止ボタン"""
        logging.info("btn_base_stop")

        Global.baseEndTime = Model.serialData.time.values[-1]

        if Global.baseEndTime - Global.baseStartTime < Global.requiredBaseDuration:
            # 時間が足りない
            sg.popup_error("最低" + str(Global.requiredBaseDuration) + "ミリ秒の計測が必要です")
            logging.error("最低" + str(Global.requiredBaseDuration) + "ミリ秒の計測が必要です")

            # ペースラインストップボタン押せるように
            Global.appView.window["btn_base_stop"].update(disabled=False)
            Global.baseEndTime = 0
        else:
            logging.info("ストップ")
            # ペースラインストップボタン押せなく
            Global.appView.window["btn_base_stop"].update(disabled=True)
            # 本計測スタート押せるように
            Global.appView.window["btn_test_start"].update(disabled=False)
            # 保存ボタン押せるように
            Global.appView.window["btn_save_raw"].update(disabled=False)
            # Global.appView.window["btn_load_test"].update(disabled = False)
            # 各種グラフ押せるように
            Global.appView.window["btn_save_raw_graph"].update(disabled=False)
            Global.appView.window["btn_save_heart_graph"].update(disabled=False)
            Global.appView.window["btn_save_fft_graph"].update(disabled=False)

            # ベースラインデータ保存
            Model.baselineSerialData = Model.serialData[
                (Model.serialData["time"] > Global.baseStartTime)
                & (Model.serialData["time"] < Global.baseEndTime)
            ]
            Model.baselineBpmData = Model.bpmData[
                (Model.bpmData.index > Global.baseStartTime)
                & (Model.bpmData.index < Global.baseEndTime)
            ]

            # グラフ止める
            GraphUtil.stop_all_graph()

            # FFTのベースライン計算
            Global.graph_fft.set_baseline()

    def btn_test_start(self) -> None:
        """本計測開始ボタン"""
        logging.info("btn_test_start")

        Global.baseStartTime = 0
        Global.baseEndTime = 0
        Global.testStartTime = 0
        Global.testEndTime = 0

        Global.appView.window["btn_save_raw"].update(disabled=True)

        # 本計測スタート押せなくしてストップ押せるように
        Global.appView.window["btn_test_start"].update(disabled=True)
        Global.appView.window["btn_test_stop"].update(disabled=False)

        # 計測データ保存できないように
        Global.appView.window["btn_save_test"].update(disabled=True)

        # グラフ保存できないように
        Global.appView.window["btn_save_raw_graph"].update(disabled=True)
        Global.appView.window["btn_save_heart_graph"].update(disabled=True)
        Global.appView.window["btn_save_fft_graph"].update(disabled=True)
        Global.appView.window["btn_save_ratio_graph"].update(disabled=True)

        # 計測開始時間保存
        Global.testStartTime = Model.serialData.time.values[-1]

        # グラフ描画開始
        Global.graph_raw.start()
        Global.graph_hb.start()
        Global.graph_fft.start()
        Global.graph_ratio.start()

    def btn_test_stop(self) -> None:
        """本計測停止ボタン"""
        logging.info("btn_test_stop")

        Global.appView.window["btn_test_stop"].update(disabled=True)
        Global.testEndTime = Model.serialData.time.values[-1]

        if Global.testEndTime - Global.testStartTime < Global.requiredBaseDuration:
            # 時間が足りない
            sg.popup_error("最低" + str(Global.requiredBaseDuration) + "ミリ秒の計測が必要です")
            logging.error("最低" + str(Global.requiredBaseDuration) + "ミリ秒の計測が必要です")
            Global.appView.window["btn_test_stop"].update(disabled=False)
            Global.testEndTime = 0
        else:
            logging.info("ストップ")
            # 時間足りた
            Global.appView.window["btn_test_start"].update(disabled=False)
            # 計測データボタン
            Global.appView.window["btn_save_test"].update(disabled=False)

            # グラフ保存できるように
            Global.appView.window["btn_save_raw_graph"].update(disabled=False)
            Global.appView.window["btn_save_heart_graph"].update(disabled=False)
            Global.appView.window["btn_save_fft_graph"].update(disabled=False)
            Global.appView.window["btn_save_ratio_graph"].update(disabled=False)

            Model.testSerialData = Model.serialData[
                (Model.serialData["time"] > Global.testStartTime)
                & (Model.serialData["time"] < Global.testEndTime)
            ]
            Model.testBpmData = Model.bpmData[
                (Model.bpmData.index > Global.testStartTime)
                & (Model.bpmData.index < Global.testEndTime)
            ]

            GraphUtil.stop_all_graph()

    def btn_save_raw(self) -> None:
        """生データ保存ボタン"""
        logging.info("btn_save_raw")

        # 生データ
        time_str = time.strftime("%Y%m%d-%H%M%S")
        filename = time_str + "-serial.csv"
        filepath = Global.outDir.joinpath(filename)
        if Model.baselineSerialData is not None:
            Model.baselineSerialData.to_csv(filepath)

        # 心拍データ
        filename = time_str + "-hb.csv"
        filepath = Global.outDir.joinpath(filename)
        if Model.baselineBpmData is not None:
            s = Model.baselineBpmData.to_csv(filepath)
            if s is None:
                sg.popup("保存されました (" + filename + ")")

    def btn_load_raw(self) -> None:
        """生データロードボタン"""
        logging.info("btn_load_raw")

        if Global.settings["raw_csv"] is None:
            s = sg.popup_get_file("ファイルを選択して下さい")
        else:
            s = sg.popup_get_file("ファイルを選択して下さい", default_path=Global.settings["raw_csv"])

        path = pathlib.Path(s)

        if path.exists():
            logging.info("ファイル存在する")

            Global.settings["raw_csv"] = str(path.absolute())

            # ボタン
            Global.appView.window["btn_base_start"].update(disabled=True)
            Global.appView.window["btn_base_stop"].update(disabled=True)
            Global.appView.window["btn_save_raw"].update(disabled=True)

            Global.appView.window["btn_save_raw_graph"].update(disabled=False)
            Global.appView.window["btn_save_heart_graph"].update(disabled=False)

            Global.appView.window["btn_save_test"].update(disabled=True)

            Global.appView.window["btn_save_fft_graph"].update(disabled=False)
            Global.appView.window["btn_save_ratio_graph"].update(disabled=True)
            Global.appView.window["btn_test_start"].update(disabled=True)
            Global.appView.window["btn_test_stop"].update(disabled=True)

            # すべてのグラフ止める
            GraphUtil.stop_all_graph()
            GraphUtil.init_all_graph()

            Global.baseStartTime = 0
            Global.baseEndTime = 0
            Global.testStartTime = 0
            Global.testEndTime = 0

            # データを反映
            Model.serialData = pd.read_csv(path)
            Global.serialController.check_beat()

            # シリアルデータ
            Model.baselineSerialData = Model.serialData.copy()

            # グラフを更新
            Global.graph_raw.update(force=True)
            Global.graph_hb.update(force=True)

            # HBデータ
            Model.baselineBpmData = Model.bpmData.copy()

            # FFTのベースライン計算
            Global.graph_fft.set_baseline()

            # 一度データを初期化
            if len(Model.serialData) > 0:
                Model.serialData = Model.serialData[0:0]

            if len(Model.bpmData) > 0:
                Model.bpmData = Model.bpmData[0:0]

            # シリアル止める
            Global.appView.window["btn_connect"].update(disabled=False)
            Global.serialController.stop()
            Global.serialController.initialize()

        else:
            sg.popup_error("ファイルが存在しません")

    def btn_save_test(self) -> None:
        """計測データ保存ボタン"""

        logging.info("btn_save_test")

        time_str = time.strftime("%Y%m%d-%H%M%S")
        filename = time_str + "-experiment-raw.csv"
        filepath = Global.outDir.joinpath(filename)
        if Model.testSerialData is not None:
            Model.testSerialData.to_csv(filepath)

        filename = time_str + "-experiment-hb.csv"
        filepath = Global.outDir.joinpath(filename)
        if Model.testBpmData is not None:
            s = Model.testBpmData.to_csv(filepath)
            if s is None:
                sg.popup("保存されました (" + filename + ")")

    def btn_save_raw_graph(self) -> None:
        """生グラフ保存ボタン"""
        logging.info("btn_save_raw_graph")
        try:
            time_str = time.strftime("%Y%m%d-%H%M%S")
            filename = time_str + "-graph-raw.png"
            filepath = Global.outDir.joinpath(filename)
            Global.graph_raw.fig.savefig(filepath, dpi=300)
            sg.popup("保存されました (" + filename + ")")
        except Exception:
            print("err")
            pass

    def btn_save_heart_graph(self) -> None:
        """心拍グラフ保存ボタン"""
        logging.info("btn_save_heart_graph")
        try:
            time_str = time.strftime("%Y%m%d-%H%M%S")
            filename = time_str + "-graph-hb.png"
            filepath = Global.outDir.joinpath(filename)
            Global.graph_hb.fig.savefig(filepath, dpi=300)
            sg.popup("保存されました (" + filename + ")")
        except Exception:
            pass

    def btn_save_fft_graph(self) -> None:
        """FFTグラフ保存ボタン"""
        logging.info("btn_save_fft_graph")
        try:
            time_str = time.strftime("%Y%m%d-%H%M%S")
            filename = time_str + "-graph-fft.png"
            filepath = Global.outDir.joinpath(filename)
            Global.graph_fft.fig.savefig(filepath, dpi=300)
            sg.popup("保存されました (" + filename + ")")
        except Exception:
            pass

    def btn_save_ratio_graph(self) -> None:
        """FFTグラフ保存ボタン"""
        logging.info("btn_save_ratio_graph")
        try:
            time_str = time.strftime("%Y%m%d-%H%M%S")
            filename = time_str + "-graph-ratio.png"
            filepath = Global.outDir.joinpath(filename)
            Global.graph_ratio.fig.savefig(filepath, dpi=300)
            sg.popup("保存されました (" + filename + ")")
        except Exception:
            pass

    def btn_reset(self) -> None:
        """リセットボタン"""
        logging.info("btn_reset")

        Global.appView.window["btn_connect"].update(disabled=False)

        Global.appView.window["btn_save_raw"].update(disabled=True)
        Global.appView.window["btn_load_raw"].update(disabled=True)
        Global.appView.window["btn_save_raw_graph"].update(disabled=True)

        Global.appView.window["btn_save_test"].update(disabled=True)

        Global.appView.window["btn_save_heart_graph"].update(disabled=True)
        Global.appView.window["btn_save_fft_graph"].update(disabled=True)
        Global.appView.window["btn_save_ratio_graph"].update(disabled=True)

        Global.appView.window["btn_base_start"].update(disabled=True)
        Global.appView.window["btn_base_stop"].update(disabled=True)

        Global.appView.window["btn_test_start"].update(disabled=True)
        Global.appView.window["btn_test_stop"].update(disabled=True)

        # 表示更新
        Global.appView.window["text_hb"].update("0")
        Global.appView.window["text_lf"].update("0")
        Global.appView.window["text_hf"].update("0")
        Global.appView.window["text_ratio"].update("0")
        Global.appView.window["text_sub"].update("0")

        # シリアル止める
        Global.serialController.stop()
        Global.serialController.initialize()

        # すべてのグラフ止める
        GraphUtil.stop_all_graph()
        GraphUtil.init_all_graph()

        Global.baseStartTime = 0
        Global.baseEndTime = 0
        Global.testStartTime = 0
        Global.testEndTime = 0

        if len(Model.serialData) > 0:
            Model.serialData = Model.serialData[0:0]

        if len(Model.bpmData) > 0:
            Model.bpmData = Model.bpmData[0:0]

        if len(Model.ratioData) > 0:
            Model.ratioData = Model.ratioData[0:0]

        if len(Model.baselineSerialData) > 0:
            Model.baselineSerialData = Model.baselineSerialData[0:0]

        if len(Model.baselineBpmData) > 0:
            Model.baselineBpmData = Model.baselineBpmData[0:0]

        if len(Model.testSerialData) > 0:
            Model.testSerialData = Model.testSerialData[0:0]

        if len(Model.testBpmData) > 0:
            Model.testBpmData = Model.testBpmData[0:0]
