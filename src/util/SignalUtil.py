import math
from typing import Iterable, Union

import numpy as np
import numpy.typing as npt
from scipy import signal
from scipy.interpolate import interpolate


def bandpass(
    x: Union[npt.NDArray, Iterable, int, float],
    sample_rate: int,
    fp: int,
    fs: int,
    g_pass: float,
    g_stop: float,
) -> npt.NDArray:
    """バンドパスフィルタ
    Args:
        x: 信号
        sample_rate: サンプリング周波数
        fp: 通過域端周波数[Hz]※ベクトル
        fs: 阻止域端周波数[Hz]※ベクトル
        g_pass: 通過域端最大損失[dB]
        g_stop: 阻止域端最小損失[dB]

    Returns:
        npt.NDArray: 処理済みの信号
    """

    fn = sample_rate / 2  # ナイキスト周波数
    wp = fp / fn  # ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn  # ナイキスト周波数で阻止域端周波数を正規化
    n, wn = signal.buttord(wp, ws, g_pass, g_stop)  # オーダーとバターワースの正規化周波数を計算
    # noinspection PyTupleAssignmentBalance
    b, a = signal.butter(n, wn, btype="band")  # フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x)  # 信号に対してフィルタをかける
    return y  # フィルタ後の信号を返す


def spline1(
    x: Union[list[float], npt.NDArray], y: Union[list[float], npt.NDArray], point: float
) -> tuple[npt.NDArray, npt.NDArray]:
    """スプライン補間関数
    Args:
        x: x信号
        y: y信号
        point: 分割数

    Returns:
        tuple[npt.NDArray,npt.NDArray]: 処理済みのデータ配列
    """
    # logging.info("spline")

    f = interpolate.interp1d(x, y, kind="linear")

    result_x = np.linspace(int(x[0]), int(x[-1]), num=int(point), endpoint=True)
    result_y = f(result_x)
    return result_x, result_y


def prev_pow_2(n: int) -> int:
    """一番近い2のx乗を調べる
    Args:
        n(int): 調べる数

    Returns:
        int:2の乗数
    """
    if n == 0:
        return 0
    if n == 1:
        return 1

    m_f = np.log2(n)
    m_i = np.floor(m_f)
    return int(math.pow(2.0, m_i))


def min_max_normalize(arr: npt.NDArray) -> npt.NDArray:
    return (arr - arr.min(initial=0)) / (arr.max(initial=1) - arr.min(initial=0))


def standard_normalize(arr: npt.NDArray) -> npt.NDArray:
    return (arr - arr.mean()) / arr.std(ddof=1)
