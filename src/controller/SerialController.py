import logging
import math
import typing

import PySimpleGUI as sg
import numpy as np
import pandas as pd
import scipy.stats
import serial
import serial.tools.list_ports
from serial import SerialException, Serial

from src.model.Model import Model
from src.util import Global
from src.util.SetInterval import SetInterval


class SerialController:
    
    # 初期化
    def __init__(self) -> None:
        """
        コンストラクタ
        """
        
        logging.info("init")
        
        self.interval: typing.Optional[SetInterval] = None
        self.serial: typing.Optional[Serial] = None
        self.ports: list[str] = []
        self.startTime: typing.Optional[int] = None
        
        self.getAvailablePorts()
    
    def initialize(self) -> None:
        self.startTime = None
    
    # 使用可能なポート一覧取得
    def getAvailablePorts(self) -> None:
        logging.info("getAvailablePorts")
        
        curPorts: list[str] = []
        ports = serial.tools.list_ports.comports()
        
        for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))
            curPorts.append(port)
        
        self.ports = curPorts
    
    # シリアルポート用意
    def openSerial(self) -> bool:
        logging.info("openSerial")
        
        try:
            if Global.appController.values and Global.appController.values["port_select"]:
                self.serial = serial.Serial(Global.appController.values["port_select"], 115200,
                                            timeout = 0)
                logging.info("SERIAL OPEN")
                return True
            else:
                logging.error("シリアルポートが選択されていません。")
                sg.popup_error('シリアルポートが選択されていません。')
                return False
        
        except SerialException as e:
            sg.popup_error('シリアルポート開放に失敗しました。')
            logging.error(e)
            return False
    
    # 読み込み開始
    def start(self) -> None:
        logging.info("start")
        try:
            self.openSerial()
        except SerialException as e:
            logging.error(e)
        else:
            Model.serialData = Model.serialData[0:0]
            
            # 随時シリアルポートのデータを処理
            self.interval = SetInterval(Global.getSerialInterval, self.thread_task)
        pass
    
    # データ処理
    def thread_task(self) -> None:
        
        # 読み込み可能なら
        if self.serial is not None and self.serial.readable():
            
            # 読み込めるだけ読み込む
            try:
                lines = self.serial.readlines()
            except:
                logging.error("シリアルエラー")
            else:
                for val in lines:
                    val = val.strip().rsplit()
                    
                    if len(val) == 2:
                        
                        # 読み込み開始時刻を保存
                        if self.startTime is None:
                            self.startTime = int(val[0])
                        
                        # データを追加してゆく
                        Model.serialData = Model.serialData.append(
                                pd.DataFrame(
                                        data = {"raw": int(val[1]), "time": int(val[0]) - self.startTime},
                                        index = [int(val[0])]))
                        
                        # 溢れたら古いものから消す
                        Model.serialData = Model.serialData.tail(Global.maxKeepSensorLength)
                
                # 山を調べる
                # ラスト数秒間
                if len(Model.serialData) >= Global.numOfSample:
                    sample = Model.serialData.tail(Global.numOfSample).copy()
                    # print(len(sample))
                    
                    # 平均と標準偏差を求める
                    ave = scipy.stats.trim_mean(sample["raw"], 0.2)
                    sd = np.std(scipy.stats.trimboth(sample["raw"], 0.2))
                    
                    # 山とみなすしきい値
                    limit = ave + sd * 4
                    
                    # ローリングして最大値を求める
                    rolling = sample["raw"].rolling(Global.rollingWindow, center = True).max()
                    
                    raw_values = sample["raw"].values
                    time_values = sample["time"].values
                    prevTime = 0
                    for idx in range(sample.shape[0] - 1):
                        # 最大値がある
                        if not math.isnan(rolling[rolling.index[idx]]):
                            # 最大値でしきい値を超え、次の値が今と違う場合は山とみなす
                            if raw_values[idx] == rolling[rolling.index[idx]] and raw_values[idx] > limit and raw_values[idx] != raw_values[idx + 1]:
                                if time_values[idx] - prevTime > Global.rollingSpan:
                                    sample.at[sample.index[idx], "is_peak"] = 1
                                    prevTime = time_values[idx]
                    
                    peak = sample.query("is_peak==1").copy()
                    peak["diff"] = peak["time"].diff(1)
                    peak = peak.query("diff <" + str(Global.rollingSpan)).copy()
                    for index, row in peak.iterrows():
                        sample.loc[index, "is_peak"] = 0
                    
                    # データ更新
                    Model.serialData.update(sample)
    
    # 読み込み終了
    def stop(self) -> None:
        logging.info("stop")
        if self.interval is not None:
            self.interval.cancel()
        self.startTime = None
