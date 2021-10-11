import logging
import math
import typing

import numpy as np
import pandas as pd
import PySimpleGUI as sg
import scipy.stats
import serial
import serial.tools.list_ports
from serial import Serial, SerialException

from src.model.Model import Model
from src.util import Global
from src.util.SetInterval import SetInterval


class SerialController:
    def __init__(self) -> None:
        """コンストラクタ"""
        logging.info("init")

        self.interval: typing.Optional[SetInterval] = None
        self.serial: typing.Optional[Serial] = None
        self.ports: list[str] = []
        self.startTime: typing.Optional[int] = None
        self.isConnected = False

        self.get_available_ports()

    def initialize(self) -> None:
        """初期化"""
        logging.info("initialize")
        self.isConnected = False
        self.startTime = None

    def get_available_ports(self) -> None:
        """使用可能なポート一覧取得"""
        logging.info("get_available_ports")

        cur_ports: list[str] = []
        ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))
            cur_ports.append(port)

        self.ports = cur_ports

    def open_serial(self) -> bool:
        """シリアルポート用意
        Returns:
            bool: シリアルポート開放できたか
        """
        logging.info("open_serial")

        if self.isConnected:
            return True

        try:
            if Global.appController.values and Global.appController.values["port_select"]:
                self.serial = serial.Serial(
                    Global.appController.values["port_select"], 9600, timeout=0
                )
                self.isConnected = True

                Global.settings["port"] = Global.appController.values["port_select"]
                logging.info("SERIAL OPEN")
                return True
            else:
                self.isConnected = False
                logging.error("シリアルポートが選択されていません。")
                sg.popup_error("シリアルポートが選択されていません。")
                return False

        except SerialException as e:
            sg.popup_error("シリアルポート開放に失敗しました。")
            logging.error(e)
            self.isConnected = False
            return False

    def start(self) -> None:
        """読み込み開始"""
        logging.info("start")

        try:
            self.open_serial()
        except SerialException as e:
            self.isConnected = False
            logging.error(e)
        else:
            Model.serialData = Model.serialData[0:0]

            # 随時シリアルポートのデータを処理
            self.interval = SetInterval(Global.getSerialInterval, self.thread_task)
        pass

    def thread_task(self) -> None:
        """データ処理"""

        if self.serial is None or not self.serial.readable():
            return

        # 読み込めるだけ読み込む
        try:
            lines = self.serial.readlines()
        except Exception:
            logging.error("シリアルエラー")
        else:
            for val in lines:
                val = val.strip().rsplit()

                if len(val) == 2:

                    # 値がおかしいときはスキップ
                    if len(Model.serialData) > 0:
                        if int(val[0]) < Model.serialData.index.values[-1]:
                            continue
                        # if abs(int(val[0]) - Model.serialData.index.values[-1]) > 1000:
                        #     continue
                        if int(val[1]) < 500 or int(val[1]) > 1100:
                            continue

                    # 読み込み開始時刻を保存
                    if self.startTime is None:
                        self.startTime = int(val[0])

                    # データを追加してゆく
                    Model.serialData = Model.serialData.append(
                        pd.DataFrame(
                            data={"raw": int(val[1]), "time": int(val[0]) - self.startTime},
                            index=[int(val[0])],
                        )
                    )

            # 溢れたら古いものから消す
            tail_num = int(min(len(Model.serialData), Global.maxKeepSensorLength))
            Model.serialData = Model.serialData.tail(tail_num).copy()

            # 心拍を調べる
            self.check_beat()

    def check_beat(self) -> None:
        """心拍を検知"""

        # ラスト数秒間
        if len(Model.serialData) >= Global.numOfSample:

            tail_num = int(min(len(Model.serialData), Global.numOfSample))
            sample = Model.serialData.tail(tail_num).copy()

            # 平均と標準偏差を求める
            ave = scipy.stats.trim_mean(sample["raw"], 0.2)
            sd = np.std(scipy.stats.trimboth(sample["raw"], 0.2))

            # 山とみなすしきい値
            limit = ave + sd * 4

            # ローリングして最大値を求める
            rolling = sample["raw"].rolling(Global.rollingWindow, center=True).max()

            raw_values = sample["raw"].values
            time_values = sample["time"].values
            prev_time = 0

            for idx in range(sample.shape[0] - 1):
                # 最大値がある
                if not math.isnan(rolling[rolling.index[idx]]):
                    # 最大値でしきい値を超え、次の値が今と違う場合は山とみなす
                    if (
                        raw_values[idx] == rolling[rolling.index[idx]]
                        and raw_values[idx] > limit
                        and raw_values[idx] != raw_values[idx + 1]
                    ):
                        if time_values[idx] - prev_time > Global.rollingSpan:
                            sample.at[sample.index[idx], "is_peak"] = 1
                            prev_time = time_values[idx]

            # ピーク間の幅がローリング間隔より短ければはじめのみ残す
            peak = sample.query("is_peak==1").copy()
            peak["diff"] = peak["time"].diff(1)
            peak = peak.query("diff <" + str(Global.rollingSpan)).copy()
            for index, row in peak.iterrows():
                sample.loc[index, "is_peak"] = 0

            # データ更新
            Model.serialData.update(sample)

    def update_port_selection(self) -> None:
        """シリアルポート情報を更新する"""
        logging.info("update_port_selection")

        Global.serialController.get_available_ports()
        ports = Global.serialController.ports

        values = Global.appController.values
        value = ""

        # 開始時
        if values is None:
            if Global.settings["port"] in ports:
                value = Global.settings["port"]

        # ポート存在するかチェック
        if values and values["port_select"]:
            value = values["port_select"]
        if value in ports is False:
            value = ""

        # 選択肢を更新
        if len(ports) > 0:
            Global.appView.window["port_select"].update(values=ports)

        # 選択中の値を更新
        if value != "":
            Global.appView.window["port_select"].update(value=value)

    def stop(self) -> None:
        """読み込み終了"""
        logging.info("stop")

        if self.interval is not None:
            self.interval.cancel()
        self.startTime = None
