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
        logging.info(event_key)
        
        self.values = values
        
        try:
            eval("self." + event_key + "()")
        except:
            pass
    
    def btn_reflesh(self) -> None:
        """ポートリロードボタン"""
        logging.info("btn_reflesh")

        Global.appView.updatePortSelection()
    
    def btn_connect(self) -> None:
        """接続ボタン"""
        logging.info("btn_connect")
        
        if Global.serialController.openSerial():
            # 通信開始
            # ボタン類
            Global.appView.window["btn_connect"].update(disabled = True)
            # ベースライン計測できるように
            Global.appView.window["btn_base_start"].update(disabled = False)
            
            # シリアル通信開始
            Global.serialController.start()
            # グラフ描画開始
            Global.graph_raw.start()
            Global.graph_hb.start()
    
    def btn_base_start(self) -> None:
        """ベース計測開始ボタン"""
        logging.info("btn_base_start")
        
        Global.appView.window["btn_base_start"].update(disabled = True)
        Global.appView.window["btn_base_stop"].update(disabled = False)
        
        Global.baseStartTime = Model.serialData.time.values[-1]
    
    def btn_base_stop(self) -> None:
        """ベース計測停止ボタン"""
        logging.info("btn_base_stop")
        
        Global.appView.window["btn_base_stop"].update(disabled = True)
        Global.baseEndTime = Model.serialData.time.values[-1]
        
        if Global.baseEndTime - Global.baseStartTime < Global.requiredBaseDuration:
            # 時間が足りない
            sg.popup_error('最低15秒の計測が必要です')
            logging.error("最低15秒の計測が必要です")
            Global.appView.window["btn_base_stop"].update(disabled = False)
            Global.baseEndTime = 0
        else:
            logging.info("ストップ")
            # 時間足りた
            Global.appView.window["btn_test_start"].update(disabled = False)
            # 保存ボタン
            Global.appView.window["btn_save_raw"].update(disabled = False)
            Global.appView.window["btn_save_raw_graph"].update(disabled = False)
            Global.appView.window["btn_save_heart_graph"].update(disabled = False)
            
            Model.baselineSerialData = Model.serialData[(Model.serialData['time'] > Global.baseStartTime) & (Model.serialData['time'] < Global.baseEndTime)]
            Model.baselineBpmData = Model.bpmData[(Model.bpmData.index > Global.baseStartTime) & (Model.bpmData.index < Global.baseEndTime)]
            
            GraphUtil.stopAllGraph()
    
    def btn_save_raw(self) -> None:
        """生データ保存ボタン"""
        logging.info("btn_save_raw")
        
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = timestr + "-serial.csv"
        filepath = Global.outDir.joinpath(filename)
        if Model.baselineSerialData is not None:
            s = Model.baselineSerialData.to_csv(filepath)
            if s is None:
                sg.popup("保存されました (" + filename + ")")
    
    def btn_load_raw(self) -> None:
        """生データロードボタン"""
        logging.info("btn_load_raw")
        
        s = sg.popup_get_file("ファイルを選択して下さい")
        path = pathlib.Path(s)
        
        if path.exists():
            logging.info("ファイル存在する")
            
            # ボタン
            Global.appView.window["btn_base_start"].update(disabled = True)
            Global.appView.window["btn_base_stop"].update(disabled = True)
            Global.appView.window["btn_save_raw"].update(disabled = False)
            Global.appView.window["btn_save_raw_graph"].update(disabled = False)
            Global.appView.window["btn_save_heart_graph"].update(disabled = False)
            Global.appView.window["btn_save_fft_graph"].update(disabled = True)
            Global.appView.window["btn_save_ratio_graph"].update(disabled = True)
            Global.appView.window["btn_test_start"].update(disabled = False)
            Global.appView.window["btn_test_stop"].update(disabled = True)
            
            # すべてのグラフ止める
            GraphUtil.stopAllGraph()
            GraphUtil.initAllGraph()
            
            # データを反映
            Model.serialData = pd.read_csv(path)
            Model.baselineSerialData = Model.serialData.copy()
            Global.graph_raw.update()
            
            Global.graph_hb.update()
            Model.baselineBpmData = Model.bpmData.copy()
            Global.graph_hb.update()
        
        else:
            sg.popup_error("ファイルが存在しません")
    
    def btn_reset(self) -> None:
        """リセットボタン"""
        logging.info("btn_reset")
        
        Global.appView.window["btn_connect"].update(disabled = False)
        
        Global.appView.window["btn_save_raw"].update(disabled = True)
        Global.appView.window["btn_load_raw"].update(disabled = False)
        Global.appView.window["btn_save_raw_graph"].update(disabled = True)
        
        # Global.appView.window["btn_save_heart"].update(disabled = True)
        # Global.appView.window["btn_load_heart"].update(disabled = False)
        Global.appView.window["btn_save_heart_graph"].update(disabled = True)
        
        # Global.appView.window["btn_save_fft"].update(disabled = True)
        # Global.appView.window["btn_load_fft"].update(disabled = False)
        Global.appView.window["btn_save_fft_graph"].update(disabled = True)
        
        Global.appView.window["btn_save_ratio_graph"].update(disabled = True)
        
        Global.appView.window["btn_base_start"].update(disabled = True)
        Global.appView.window["btn_base_stop"].update(disabled = True)
        
        Global.appView.window["btn_test_start"].update(disabled = True)
        Global.appView.window["btn_test_stop"].update(disabled = True)
        
        # シリアル止める
        Global.serialController.stop()
        Global.serialController.initialize()
        
        # すべてのグラフ止める
        GraphUtil.stopAllGraph()
        GraphUtil.initAllGraph()
        
        Global.baseStartTime = 0
        Global.baseEndTime = 0
        Model.serialData = Model.serialData[0:0]
        Model.bpmData = Model.bpmData[0:0]
