import os
import time

import japanize_matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm


def moving_average(x, winsize):
    results = np.full(x.shape, np.nan)
    rolled = np.lib.stride_tricks.sliding_window_view(x, winsize, axis=0)
    results[winsize - 1 :] = rolled.mean(axis=2)
    return results


np.random.seed(1234)
mpl.rcParams["font.size"] = 18
japanize_matplotlib.japanize()

# 設定
stride = 1000000
nrows_list = np.arange(100, 50000 * 200 + stride, stride)
ncols = 50
winsize = 20

# データ準備
data_size = (nrows_list[-1], ncols)
data = np.random.standard_normal(data_size)
base = pd.DataFrame(data)

# 処理時間の計測
pandas_times = []
numpy_times = []
numpy_times_without_convert = []
for i in tqdm(range(0, nrows_list.size)):
    df = base.head(nrows_list[i])

    start = time.time()
    results_pandas = df.rolling(winsize).mean()
    pandas_times += [time.time() - start]

    start = time.time()
    results_numpy = moving_average(df.to_numpy(), winsize)
    numpy_times_without_convert += [time.time() - start]
    results_numpy = pd.DataFrame(results_numpy)
    numpy_times += [time.time() - start]

# データ数に対する処理時間の関係をグラフ化
fig, ax = plt.subplots(figsize=(16, 9))
ax.plot(nrows_list, pandas_times, label="Pandas")
ax.plot(nrows_list, numpy_times, label="Numpy")
ax.set(xlabel="データ数", ylabel="実行時間 [s]")
ax.legend()
fig.tight_layout()

savename = "./rolling_apply/datapoints_vs_time.png"
os.makedirs(os.path.dirname(savename), exist_ok=True)
plt.savefig(savename, dpi=300)
plt.close()

# Pandas と Numpy で同じ結果かどうかを時系列プロットしてチェック
fig, ax = plt.subplots(figsize=(16, 9))
data_1 = results_pandas.iloc[:, 0].to_numpy()[:2000]
data_2 = results_numpy.iloc[:, 0].to_numpy()[:2000]
ax.plot(np.arange(data_1.shape[0]), data_1, label="Pandas")
ax.plot(np.arange(data_1.shape[0]), data_2, ls="--", label="Numpy")
ax.set(xlabel=r"$x_t$", ylabel=r"$y_t$")
ax.legend()
fig.tight_layout()

savename = "./rolling_apply/time-series-plot.png"
plt.savefig(savename, dpi=300)
plt.close()
