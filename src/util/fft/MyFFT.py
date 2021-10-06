import numpy as np
import numpy.typing as npt


def my_fft(x: npt.NDArray) -> npt.NDArray:
    """FFT処理をします
    Args:
        x:信号の配列

    Returns:
        npt.NDArray:FFT結果
    """

    n = x.shape[0]  # xの長さをを調べ、Nに代入
    hat_x = np.zeros(n, dtype="complex")  # 複素数型の0をN個用意(フーリエ変換後の変数)
    k = np.arange(0, n // 2)  # 0から2/n-1まで,2/N個並べた配列(n//2で整数化) バタフライ演算の過程で半分のk
    w = np.exp(-1j * 2 * np.pi * k / n)  # 回転因子

    if n == 2:
        # 2点DFTのバタフライ演算
        hat_x[0] = x[0] + x[1]
        hat_x[1] = x[0] - x[1]
        return hat_x

    if n >= 4:
        # バタフライ演算
        even = my_fft(x[0:n:2])  # 偶数
        odd = my_fft(x[1:n:2])  # 奇数

        hat_x[0 : n // 2] = even + w * odd
        hat_x[n // 2 : n] = even - w * odd
        return hat_x

    return np.zeros(n)
