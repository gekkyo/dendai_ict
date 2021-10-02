import typing

import pandas as pd
from pandas import DataFrame


class Model:
    serialData = pd.DataFrame(columns = ["timecode", "raw", "time", "is_peak", "diff", "bpm"], dtype = "int64").set_index("timecode")
    # serialData["bpm"] = serialData["bpm"].astype("float64")
    
    bpmData = pd.DataFrame(columns = ["time", "y"]).set_index("time")
    
    # 保存用データ
    baselineSerialData: typing.Optional[DataFrame] = None
    baselineBpmData: typing.Optional[DataFrame] = None
