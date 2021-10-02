# matplotlib
import logging

import PySimpleGUI as sg
import matplotlib
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.util import Global

matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams["font.size"] = 8
plt.rcParams["axes.linewidth"] = 0.5
plt.rcParams["xtick.minor.visible"] = True  # x軸補助目盛りの追加
plt.rcParams["ytick.minor.visible"] = True  # y軸補助目盛りの追加
plt.rcParams["xtick.major.width"] = 0.2  # x軸主目盛り線の線幅
plt.rcParams["ytick.major.width"] = 0.2  # y軸主目盛り線の線幅
plt.rcParams["xtick.minor.width"] = 0.2  # x軸補助目盛り線の線幅
plt.rcParams["ytick.minor.width"] = 0.2
# plt.rcParams["figure.autolayout"] = True
plt.switch_backend('Agg')
plt.ion()


def init_graph(figsize: tuple, target: sg.Canvas) -> Axes:
    # 埋め込む用のfigを作成する．
    fig: Figure = plt.figure(figsize = figsize)
    ax: Axes = fig.add_subplot(111)
    ax.grid(linewidth = 0.4, linestyle = "dotted")
    # ax.set_ylim(ylim[0], ylim[1])
    # ax.set_xlim(xlim[0], ylim[1])
    # ax.plot(0, 0, linewidth = 0.5)  # プロット
    
    # figとCanvasを関連付ける．
    tcv = target.TKCanvas
    draw_fig(tcv, fig)
    return ax


# 描画用の関数
def draw_fig(cv: sg.Canvas.TKCanvas, fig: Figure) -> FigureCanvasTkAgg:
    figure_canvas_agg = FigureCanvasTkAgg(fig, cv)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side = 'top', fill = 'both', expand = 1)
    return figure_canvas_agg


def stopAllGraph() -> None:
    logging.info("stopAllGraph")
    for graph in Global.graphArray:
        graph.stop()


def initAllGraph() -> None:
    logging.info("initAllGraph")
    for graph in Global.graphArray:
        graph.initGraph()
