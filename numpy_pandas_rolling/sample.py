from itertools import groupby

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view


def moving_average(x, window=3):
    rolled = sliding_window_view(x, window, axis=0)
    return rolled.mean(axis=-1)


df = pd.read_csv("sample.csv", index_col=0)
print(df)

_res = [
    moving_average(np.array(list(x))[:, 1], window=3)
    for k, x in groupby(df.to_numpy(), key=lambda x: x[0])
]

res = np.hstack(_res)

print(res)

print(df.groupby("Group").rolling(3).mean())
