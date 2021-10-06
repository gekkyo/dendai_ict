import logging
import sys

import matplotlib.pyplot as plt
import PySimpleGUI as sg
from PySimpleGUI import TITLE_LOCATION_TOP

from src.controller.Graph.FftGraph import FftGraph
from src.controller.Graph.HeartBeatGraph import HeartBeatGraph
from src.controller.Graph.RatioGraph import RatioGraph
from src.controller.Graph.RawGraph import RawGraph
from src.util import Global, GraphUtil
from src.view.Style import (
    column_base,
    column_base_frame,
    column_graph_l,
    column_left,
    column_reset,
    column_right,
    column_save,
    column_save_item,
    column_setup,
    column_values,
    fig_style_l,
    input_button_style_l,
    input_button_style_m,
    input_button_style_refresh,
    input_button_style_reset,
    input_button_style_s,
    input_button_style_sl,
    port_selection_style,
    values_text_style,
    values_text_title_style,
    window_style,
)


class AppView:
    def __init__(self) -> None:
        """コンストラクタ"""
        logging.info("init")

        # メインウインドウ
        self.window: sg.Window

        # テーマ
        sg.theme("LightGray1")

        # グラフ
        upper_canvas_left = [
            [sg.Canvas(key="upper_canvas_left_up", **fig_style_l)],
            [sg.Canvas(key="upper_canvas_left_down", **fig_style_l)],
        ]
        upper_canvas_right = [
            [sg.Canvas(key="upper_canvas_right_up", **fig_style_l)],
            [sg.Canvas(key="upper_canvas_right_down", **fig_style_l)],
        ]

        # 値表示
        values_layout = [
            [sg.Text(text="心拍数", key="text_hb_title", **values_text_title_style)],
            [sg.Text(text="0", key="text_hb", **values_text_style)],
            [sg.Text(text="LF", key="text_lf_title", **values_text_title_style)],
            [sg.Text(text="0", key="text_lf", **values_text_style)],
            [sg.Text(text="HF", key="text_hf_title", **values_text_title_style)],
            [sg.Text(text="0", key="text_hf", **values_text_style)],
            [sg.Text(text="LF/HF比率", key="text_ratio_title", **values_text_title_style)],
            [sg.Text(text="0", key="text_ratio", **values_text_style)],
            [sg.Text(text="ベースライン比率からの差", key="text_sub_title", **values_text_title_style)],
            [sg.Text(text="0", key="text_sub", **values_text_style)],
        ]
        values_frame = [
            [
                sg.Frame(
                    "計測値", title_location=TITLE_LOCATION_TOP, layout=values_layout, **column_values
                )
            ],
            [sg.HorizontalSeparator(color="#FEFEFE", pad=(10, 20))],
        ]

        # セットアップ
        setup_layout = [
            [
                sg.Combo([], key="port_select", **port_selection_style),
                sg.Button(button_text="RELOAD", key="btn_refresh", **input_button_style_refresh),
            ],
            [
                sg.Button(
                    button_text="CONNECT",
                    key="btn_connect",
                    disabled=False,
                    **input_button_style_l
                )
            ],
        ]
        setup_frame = [
            [
                sg.Frame(
                    "セットアップ",
                    title_location=TITLE_LOCATION_TOP,
                    layout=setup_layout,
                    **column_setup
                )
            ]
        ]

        # 生データ
        raw_save_layout = [
            [
                sg.Button(
                    button_text="保存", key="btn_save_raw", disabled=True, **input_button_style_s
                ),
                sg.Button(
                    button_text="ロード", key="btn_load_raw", disabled=True, **input_button_style_s
                ),
            ],
            [
                sg.Button(
                    button_text="グラフ保存",
                    key="btn_save_raw_graph",
                    disabled=True,
                    **input_button_style_sl
                )
            ],
        ]

        # 計測データ
        test_save_layout = [
            [
                sg.Button(
                    button_text="保存", key="btn_save_test", disabled=True, **input_button_style_sl
                )
            ]
        ]

        # 心拍数データ
        heart_save_layout = [
            [
                sg.Button(
                    button_text="グラフ保存",
                    key="btn_save_heart_graph",
                    disabled=True,
                    **input_button_style_sl
                )
            ]
        ]

        # FFTデータ
        fft_save_layout = [
            [
                sg.Button(
                    button_text="グラフ保存",
                    key="btn_save_fft_graph",
                    disabled=True,
                    **input_button_style_sl
                )
            ]
        ]

        # 比率データ
        ratio_save_layout = [
            [
                sg.Button(
                    button_text="グラフ保存",
                    key="btn_save_ratio_graph",
                    disabled=True,
                    **input_button_style_sl
                )
            ]
        ]

        save_frame = [
            [
                sg.Frame(
                    "ベースラインデータ",
                    title_location=TITLE_LOCATION_TOP,
                    layout=raw_save_layout,
                    **column_save_item
                )
            ],
            [
                sg.Frame(
                    "計測データ",
                    title_location=TITLE_LOCATION_TOP,
                    layout=test_save_layout,
                    **column_save_item
                )
            ],
            [
                sg.Frame(
                    "心拍数データ",
                    title_location=TITLE_LOCATION_TOP,
                    layout=heart_save_layout,
                    **column_save_item
                )
            ],
            [
                sg.Frame(
                    "FFTデータ",
                    title_location=TITLE_LOCATION_TOP,
                    layout=fft_save_layout,
                    **column_save_item
                )
            ],
            [
                sg.Frame(
                    "比率データ",
                    title_location=TITLE_LOCATION_TOP,
                    layout=ratio_save_layout,
                    **column_save_item
                )
            ],
        ]

        # 保存レイアウト
        save_frame = [
            [
                sg.Frame(
                    "SAVE/LOAD",
                    title_location=TITLE_LOCATION_TOP,
                    layout=save_frame,
                    **column_save
                )
            ],
        ]

        # リセットエリア
        reset_layout = [
            [
                sg.Button(
                    button_text="RESET",
                    key="btn_reset",
                    disabled=False,
                    **input_button_style_reset
                )
            ]
        ]
        reset_frame = [
            [
                sg.Frame(
                    "リセット", title_location=TITLE_LOCATION_TOP, layout=reset_layout, **column_reset
                )
            ]
        ]

        # ベースデータ
        base_layout = [
            [
                sg.Button(
                    button_text="スタート", key="btn_base_start", disabled=True, **input_button_style_m
                ),
                sg.Button(
                    button_text="ストップ", key="btn_base_stop", disabled=True, **input_button_style_m
                ),
            ]
        ]
        base_frame = [
            [
                sg.Frame(
                    "ベースライン計測",
                    title_location=TITLE_LOCATION_TOP,
                    layout=base_layout,
                    **column_base_frame
                )
            ]
        ]

        # 計測
        test_layout = [
            [
                sg.Button(
                    button_text="スタート", key="btn_test_start", disabled=True, **input_button_style_m
                ),
                sg.Button(
                    button_text="ストップ", key="btn_test_stop", disabled=True, **input_button_style_m
                ),
            ]
        ]
        test_frame = [
            [
                sg.Frame(
                    "本計測",
                    title_location=TITLE_LOCATION_TOP,
                    layout=test_layout,
                    **column_base_frame
                )
            ]
        ]

        # 左右列
        left_raw = [
            [
                sg.Column(upper_canvas_left, **column_graph_l),
                sg.Column(upper_canvas_right, **column_graph_l),
            ],
            [sg.Column(base_frame, **column_base), sg.Column(test_frame, **column_base)],
        ]
        right_raw = [
            [sg.Column(values_frame, **column_values)],
            [sg.Column(setup_frame, **column_setup)],
            [sg.Column(save_frame, **column_save)],
            [sg.Column(reset_frame, **column_save)],
        ]

        # 統合
        self.layout = [[sg.Column(left_raw, **column_left), sg.Column(right_raw, **column_right)]]

        # ウインドウ表示
        self.window = sg.Window(title="嘘発見アプリ", layout=self.layout, **window_style)

    def prepare_graph(self) -> None:
        """グラフを用意"""
        logging.info("prepare_graph")

        Global.graph_raw = RawGraph("upper_canvas_left_up")
        Global.graph_hb = HeartBeatGraph("upper_canvas_left_down")
        Global.graph_fft = FftGraph("upper_canvas_right_up")
        Global.graph_ratio = RatioGraph("upper_canvas_right_down")

    def close_window(self) -> None:
        """ウインドウを閉じてアプリ終了"""
        logging.info("close_window")

        # グラフ処理止める
        GraphUtil.stop_all_graph()
        plt.close("all")

        # シリアル通信止める
        Global.serialController.stop()

        # ウインドウ閉じて終了
        self.window.close()
        sys.exit()
