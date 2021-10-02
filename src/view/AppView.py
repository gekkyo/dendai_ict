import logging
import sys

import PySimpleGUI as sg
import matplotlib.pyplot as plt
from PySimpleGUI import TITLE_LOCATION_TOP

from src.controller.Graph.FftGraph import FftGraph
from src.controller.Graph.HeartBeatGraph import HeartBeatGraph
from src.controller.Graph.RatioGraph import RatioGraph
from src.controller.Graph.RawGraph import RawGraph
from src.util import Global, GraphUtil
from src.view.Style import *


class AppView:
    
    def __init__(self) -> None:
        """
        コンストラクタ
        """
        
        logging.info("init")
        
        # メインウインドウ
        self.window: sg.Window
        
        # テーマ
        sg.theme('SystemDefault')
        
        # グラフ
        upper_canvas_left = [[sg.Canvas(key = 'upper_canvas_left_up', **fig_style_s)], [sg.Canvas(key = 'upper_canvas_left_down', **fig_style_s)]]
        self.upper_canvas_right = [[sg.Canvas(key = 'upper_canvas_right_up', **fig_style_m)], [sg.Canvas(key = 'upper_canvas_right_down', **fig_style_ss)]]
        
        # セットアップ
        setup_layout = [
                [sg.Combo([], key = 'port_select', **port_selection_style), sg.Button(button_text = 'RELOAD', key = "btn_reflesh",
                                                                                      **input_button_style_reflesh)],
                [sg.Button(button_text = 'CONNECT', key = "btn_connect", disabled = False, **input_button_style_l)]]
        setup_frame = [
                [sg.Frame('セットアップ', title_location = TITLE_LOCATION_TOP, layout = setup_layout, **column_setup)]
                ]
        
        # 生データ
        raw_save_layout = [
                [sg.Button(button_text = '保存', key = "btn_save_raw", disabled = True, **input_button_style_s),
                 sg.Button(button_text = 'ロード', key = "btn_load_raw", disabled = False, **input_button_style_s)],
                [sg.Button(button_text = 'グラフ保存', key = "btn_save_raw_graph", disabled = True, **input_button_style_sl)]
                ]
        
        # 心拍数データ
        heart_save_layout = [
                [sg.Button(button_text = 'グラフ保存', key = "btn_save_heart_graph", disabled = True, **input_button_style_sl)]]
        
        # FFTデータ
        fft_save_layout = [
                [sg.Button(button_text = 'グラフ保存', key = "btn_save_fft_graph", disabled = True, **input_button_style_sl)]]
        
        # 比率データ
        ratio_save_layout = [
                [sg.Button(button_text = 'グラフ保存', key = "btn_save_ratio_graph", disabled = True, **input_button_style_sl)]]
        
        save_frame = [
                [sg.Frame('生データ', title_location = TITLE_LOCATION_TOP, layout = raw_save_layout, **column_save_item)],
                [sg.Frame('心拍数データ', title_location = TITLE_LOCATION_TOP, layout = heart_save_layout, **column_save_item)],
                [sg.Frame('FFTデータ', title_location = TITLE_LOCATION_TOP, layout = fft_save_layout, **column_save_item)],
                [sg.Frame('比率データ', title_location = TITLE_LOCATION_TOP, layout = ratio_save_layout, **column_save_item)],
                ]
        
        # 保存レイアウト
        save_frame = [
                [sg.Frame('SAVE/LOAD', title_location = TITLE_LOCATION_TOP, layout = save_frame, **column_save)],
                ]
        
        # リセットエリア
        reset_layout = [
                [sg.Button(button_text = 'RESET', key = "btn_reset", disabled = False, **input_button_style_reset)]]
        reset_frame = [
                [sg.Frame('リセット', title_location = TITLE_LOCATION_TOP, layout = reset_layout, **column_reset)]
                ]
        
        # ベースデータ
        base_layout = [
                [sg.Button(button_text = 'スタート', key = "btn_base_start", disabled = True, **input_button_style_m),
                 sg.Button(button_text = 'ストップ', key = "btn_base_stop", disabled = True, **input_button_style_m)]]
        base_frame = [
                [sg.Frame('ベースライン計測', title_location = TITLE_LOCATION_TOP, layout = base_layout, **column_base_frame)]
                ]
        
        # 計測
        test_layout = [
                [sg.Button(button_text = 'スタート', key = "btn_test_start", disabled = True, **input_button_style_m),
                 sg.Button(button_text = 'ストップ', key = "btn_test_stop", disabled = True, **input_button_style_m)]]
        test_frame = [
                [sg.Frame('本計測', title_location = TITLE_LOCATION_TOP, layout = test_layout, **column_base_frame)]
                ]
        
        # 左右列
        leftRaw = [
                [sg.Column(upper_canvas_left, **column_graph_l), sg.Column(self.upper_canvas_right, **column_graph_l)],
                [sg.Column(base_frame, **column_base), sg.Column(test_frame, **column_base)],
                ]
        rightRaw = [
                [sg.Column(setup_frame, **column_setup)],
                [sg.Column(save_frame, **column_save)],
                [sg.Column(reset_frame, **column_save)],
                ]
        
        # 統合
        self.layout = [[sg.Column(leftRaw, **column_left),
                        sg.Column(rightRaw, **column_right)]]
    
    def show_window(self) -> None:
        """
        ウインドウを表示
        """
        
        logging.info("show_window")
        
        self.window = sg.Window(title = '嘘発見アプリ', layout = self.layout, **window_style)
        
        Global.graph_raw = RawGraph("upper_canvas_left_up")
        Global.graph_hb = HeartBeatGraph("upper_canvas_left_down")
        Global.graph_fft = FftGraph("upper_canvas_right_up")
        Global.graph_ratio = RatioGraph("upper_canvas_right_down")
        
        self.updatePortSelection()
    
    def updatePortSelection(self) -> None:
        """
        シリアルポート情報を更新する
        """
        
        logging.info("updatePortSelection")
        
        Global.serialController.getAvailablePorts()
        ports = Global.serialController.ports
        
        values = Global.appController.values
        value = ""
        
        # 開始時
        if values == None:
            if Global.initialPort in ports:
                value = Global.initialPort
        
        # ポート存在するかチェック
        if values and values["port_select"]:
            value = values["port_select"]
        if value in ports is False:
            value = ""
        
        # 選択肢を更新
        if len(ports) > 0:
            self.window["port_select"].update(values = ports)
        
        # 選択中の値を更新
        if value != "":
            self.window["port_select"].update(value = value)
    
    def close_window(self) -> None:
        """
        ウインドウを閉じてアプリ終了
        """
        
        logging.info("close_window")
        
        # グラフ処理止める
        GraphUtil.stopAllGraph()
        plt.close("all")
        
        # シリアル通信止める
        Global.serialController.stop()
        
        # ウインドウ閉じて終了
        self.window.close()
        sys.exit()
