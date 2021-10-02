import serial
import numpy as np
from matplotlib import pyplot as plt


ser = serial.Serial('/dev/cu.usbmodem14401', 9600, timeout = None)

tArr = np.zeros(0)
vArr = np.zeros(0)

def realtime_graph(time, value):
    global tArr
    global vArr
    print(time)
    print(value)
    tArr = np.append(tArr,time)
    vArr = np.append(vArr,value)
    print(tArr)
    print(vArr)
    line, = plt.plot(tArr,vArr,"ro",lw="1.0", label="y=x")  # (x,y)のプロット
    #line.set_ydata(vArr)   # y値を更新
    plt.title("Graph")  # グラフタイトル
    plt.xlabel("time")     # x軸ラベル
    plt.ylabel("value")     # y軸ラベル
    plt.legend()        # 凡例表示
    plt.grid()          # グリッド表示
    plt.xlim([0, 1000])    # x軸範囲
    plt.ylim([0, 800])    # y軸範囲
    plt.draw()          # グラフの描画
    plt.pause(0.01)     # 更新時間間隔
    plt.clf()           # 画面初期化

plt.ion()           # 対話モードオン

counter = 0

while True:
    data = ser.readline().strip().rsplit()
    realtime_graph(counter,int.from_bytes(data[0], byteorder='big', signed = False))
    counter += 1

# t = np.zeros(100)
# y = np.zeros(100)
#
#
#
#
#
#
# plt.ion()
# plt.figure()
# li, = plt.plot(t, y)
# plt.ylim(0, 5)
# plt.xlabel("time[s]")
# plt.ylabel("Voltage[V]")
#
# data = ser.readline().strip().rsplit()
# print(data[0])
# tInt = float(data[0])
#
# counter = 0
#
# plt.show()
#
# while True:
#     try:
#         data = ser.readline().strip().rsplit()
#         # 配列をキューと見たてて要素を追加・削除
#         t = np.append(t, counter)
#         counter = counter +1
#         t = np.delete(t, 0)
#         y = np.append(y, float(data[0]))
#         y = np.delete(y, 0)
#
#         print(t)
#
#         li.set_xdata(t)
#         li.set_ydata(y)
#         plt.xlim(min(t), max(t))
#         plt.draw()
#
#     except KeyboardInterrupt:
#         ser.close()
#         break
#
#
