import math
from typing import Union

import numpy as np
import numpy.typing as npt
from scipy.interpolate import interpolate


def spline1(
    x: Union[list[float], npt.NDArray],
    y: Union[list[float], npt.NDArray],
    point: float,
    kind: str = "linear",
) -> tuple[npt.NDArray, npt.NDArray]:
    """スプライン補間関数
    Args:
        kind: 補間方法
        x: x信号
        y: y信号
        point: 分割数

    Returns:
        tuple[npt.NDArray,npt.NDArray]: 処理済みのデータ配列
    """
    # logging.info("spline")

    f = interpolate.interp1d(x, y, kind=kind)

    result_x = np.linspace(int(x[0]), int(x[-1]), num=int(point), endpoint=True)
    result_y = f(result_x)
    return result_x, result_y


def moving_avg(
    in_x: Union[list[float], npt.NDArray], in_y: Union[list[float], npt.NDArray]
) -> tuple[npt.NDArray, npt.NDArray]:
    """移動平均
    Args:
        in_x:x信号
        in_y:y信号
    Returns:
        tuple[npt.NDArray,npt.NDArray]: 処理済みのデータ配列
    """
    np_y_conv = np.convolve(in_y, np.ones(2) / float(2), mode="same")  # 畳み込む
    out_x_dat = np.linspace(min(in_x), max(in_x), np.size(np_y_conv))

    return out_x_dat, np_y_conv


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
