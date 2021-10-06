import numpy as np
import matplotlib.pyplot as plt

import MyFFT as F

PI = np.pi

N = 2**8 # 2の累乗のデータ数
fs = 100 # サンプリング周波数
T = 1/fs # サンプリング周期
PI = np.pi
f1 = 10; f2 = 20; f3 = 30 # sin波に使う周波数
A1 = 1; A2 = 0.5; A3 = 0.8 #sin波に使う振幅
t = np.arange(0, N*T, T) # sin波の時間 N*T秒

#サンプルのsin波形
x = A1*np.sin(2*PI*f1*t)+A2*np.sin(2*PI*f2*t)+A3*np.sin(2*PI*f3*t)

testF = F.my_fft(x)
amp = 2*np.abs(testF)/N # プロットの振幅
freq = np.linspace(0, fs, N) # プロットの周波数

plt.plot(freq[:int(N/2)+1], amp[:int(N/2)+1])
plt.show()
