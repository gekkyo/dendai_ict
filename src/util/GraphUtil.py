# matplotlib
import logging

import PySimpleGUI as sg
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src.util import Global


def init() -> None:
    """matplotlib初期化"""
    logging.info("init")

    # グラフを表示させない
    matplotlib.use("Agg")

    # グラフの初期設定
    plt.rcParams["font.size"] = 8
    plt.rcParams["axes.linewidth"] = 0.5
    plt.rcParams["xtick.minor.visible"] = True  # x軸補助目盛りの追加
    plt.rcParams["ytick.minor.visible"] = True  # y軸補助目盛りの追加
    plt.rcParams["xtick.major.width"] = 0.2  # x軸主目盛り線の線幅
    plt.rcParams["ytick.major.width"] = 0.2  # y軸主目盛り線の線幅
    plt.rcParams["xtick.minor.width"] = 0.2  # x軸補助目盛り線の線幅
    plt.rcParams["ytick.minor.width"] = 0.2
    # plt.rcParams["figure.autolayout"] = True

    # plotを表示させない
    # plt.switch_backend("Agg")
    # インタラクティブモード
    plt.ion()


def init_graph(figsize: tuple, target: sg.Canvas) -> tuple[Figure, Axes]:
    """グラフを作成する
    Args:
        figsize(float,float): グラフサイズ
        target(sg.Canvas): ターゲットのキャンバス

    Returns:
        Axes:グラフのAxes
    """
    logging.info("init_graph")

    # 埋め込む用のfigを作成する．
    fig: Figure = plt.figure(figsize=figsize)
    ax: Axes = fig.add_subplot(111)
    ax.grid(linewidth=0.4, linestyle="dotted")
    # ax.set_ylim(ylim[0], ylim[1])
    # ax.set_xlim(xlim[0], ylim[1])
    # ax.plot(0, 0, linewidth = 0.5)  # プロット

    # figとCanvasを関連付ける．
    tcv = target.TKCanvas
    draw_fig(tcv, fig)
    return fig, ax


def draw_fig(cv: sg.Canvas.TKCanvas, fig: Figure) -> FigureCanvasTkAgg:
    """描画関数

    Args:
        cv(sg.Canvas.TKCanvas): ターゲットのキャンバス
        fig(Figure): 描画するFigure

    Returns:
        FigureCanvasTkAgg: widget
    """
    logging.info("draw_fig")

    figure_canvas_agg = FigureCanvasTkAgg(fig, cv)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def stop_all_graph() -> None:
    """すべてのグラフを止める"""
    logging.info("stop_all_graph")

    for graph in Global.graphArray:
        graph.stop()


def init_all_graph() -> None:
    """すべてのグラフ初期化"""
    logging.info("init_all_graph")

    for graph in Global.graphArray:
        graph.init_graph()
