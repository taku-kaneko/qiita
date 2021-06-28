import itertools as it
from typing import Any, Union

import numpy as np
import pandas as pd


def _rolling(x: np.ndarray, winSize: int, func: Any, *args, **kwargs) -> np.ndarray:
    results = np.full(x.shape, np.nan)
    rolled = np.lib.stride_tricks.sliding_window_view(x, winSize, axis=0)

    if type(func) is str:
        if func == "mean":
            results[winSize - 1 :] = x.mean(axis=-1)
        elif func == "std":
            results[winSize - 1 :] = x.std(axis=-1, ddof=1)
        elif func == "var":
            results[winSize - 1 :] = x.var(axis=-1, ddof=1)
        elif func == "max":
            results[winSize - 1 :] = x.max(axis=-1)
        elif func == "min":
            results[winSize - 1 :] = x.min(axis=-1)
    else:
        results[winSize - 1 :] = func(rolled, *args, **kwargs)
    return results


def rollingApply(
    df: pd.DataFrame,
    groups: Union[str, list[str]],
    winSize: int,
    func: Any,
    usecols: list[str] = None,
    *args,
    **kwargs,
) -> pd.DataFrame:
    groups_columns_location = df.columns.get_loc(groups)

    if usecols is None:
        if type(groups) is str:
            tmp = ~df.columns.isin([groups])
        else:
            tmp = ~df.columns.isin(groups)
        usecols = df.columns[tmp].to_list()

    usecols_location = [df.columns.get_loc(col) for col in usecols]

    res = [
        _rolling(np.array(list(x))[:, usecols_location], winSize, func, *args, **kwargs)
        for _, x in it.groupby(df.to_numpy(), key=lambda x: x[groups_columns_location])
    ]

    res_df = pd.DataFrame(np.vstack(res), columns=usecols)
    res_df = pd.concat([df[groups], res_df], axis=1)

    return res_df
