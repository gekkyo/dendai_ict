from typing import Iterable, Union

import numpy as np
from numpy import ndarray
from scipy import signal
from scipy.interpolate import interpolate


def bandpass(x: Union[ndarray, Iterable, int, float], samplerate: int, fp: int, fs: int, gpass: float, gstop: float) -> ndarray:
    """バンドパスフィルタ
    Args:
        x: 信号
        samplerate: サンプリング周波数
        fp: 通過域端周波数[Hz]※ベクトル
        fs: 阻止域端周波数[Hz]※ベクトル
        gpass: 通過域端最大損失[dB]
        gstop: 阻止域端最小損失[dB]

    Returns:
        ndarray: 処理済みの信号
    """
    
    fn = samplerate / 2  # ナイキスト周波数
    wp = fp / fn  # ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn  # ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  # オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, btype = "band")  # フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x)  # 信号に対してフィルタをかける
    return y  # フィルタ後の信号を返す


def spline1(x: list[float], y: list[float], point: float) -> tuple[ndarray, ndarray]:
    """スプライン補間関数
    Args:
        x: x信号
        y: y信号
        point: 分割数

    Returns:
        tuple[ndarray,ndarray]: 処理済みのデータ配列
    """
    # logging.info("spline")
    f = interpolate.interp1d(x, y, kind = "quadratic")
    X = np.linspace(int(x[0]), int(x[-1]), num = int(point), endpoint = True)
    Y = f(X)
    return X, Y
