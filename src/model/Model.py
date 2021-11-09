import pandas as pd
from pandas import DataFrame


class Model:
    # 生データ
    serialData = pd.DataFrame(
        columns=["timecode", "raw", "time", "is_peak", "diff", "bpm"], dtype="int64"
    ).set_index("timecode")

    # 心拍データ
    bpmData = pd.DataFrame(columns=["time", "y"]).set_index("time")

    # 保存用データ
    baselineSerialData: DataFrame = serialData.copy()
    baselineBpmData: DataFrame = bpmData.copy()

    testSerialData: DataFrame = serialData.copy()
    testBpmData: DataFrame = bpmData.copy()

    ratioData = pd.DataFrame(columns=["time", "y"]).set_index("time")
