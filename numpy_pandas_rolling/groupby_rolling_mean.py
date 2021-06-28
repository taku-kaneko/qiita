import itertools as it
import os
import time

import japanize_matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm


def moving_average(x, winsize):
    x = np.array(x)[:, 1:].astype(np.float32)
    results = np.full(x.shape, np.nan)
    rolled = np.lib.stride_tricks.sliding_window_view(x, winsize, axis=0)
    results[winsize - 1 :] = rolled.mean(axis=2)
    return results


np.random.seed(1234)
mpl.rcParams["font.size"] = 18
japanize_matplotlib.japanize()

# 設定
stride = 5000
n_groups_list = np.arange(100, 50000 + stride, stride)
nrows = 200
ncols = 50
winsize = 20

# データ準備
data_size = (n_groups_list[-1] * nrows, ncols)
groups = np.array(sorted(list(range(n_groups_list[-1])) * nrows)).reshape(-1, 1)
data = np.random.standard_normal(data_size)
base = pd.DataFrame(np.concatenate([groups.astype(int), data], axis=1))
base = base.rename(columns={0: "Groups"})

# 処理時間の計測
pandas_times = []
pandarallel_times = []
numpy_times = []
for i in tqdm(range(0, n_groups_list.size)):
    df = base.loc[base["Groups"].isin(list(range(n_groups_list[i])))]

    start = time.time()
    results_pandas = df.groupby("Groups").rolling(winsize).mean().drop(columns="Groups")
    pandas_times += [time.time() - start]

    start = time.time()
    results_numpy = [
        moving_average(list(x), winsize) for _, x in it.groupby(df.to_numpy(), key=lambda x: x[0])
    ]
    results_numpy = pd.DataFrame(np.vstack(results_numpy), columns=np.arange(1, ncols + 1))
    results_numpy = pd.concat([df["Groups"].reset_index(drop=True), results_numpy], axis=1)
    numpy_times += [time.time() - start]

# データ数に対する処理時間の関係をグラフ化
fig, ax = plt.subplots(figsize=(16, 9))
ax.plot(n_groups_list, pandas_times, label="Pandas")
ax.plot(n_groups_list, numpy_times, label="Numpy")
ax.set(xlabel="グループ数", ylabel="処理時間 [s]")
ax.legend()
fig.tight_layout()

savename = "./groupby_rolling_mean/groups_vs_time.png"
os.makedirs(os.path.dirname(savename), exist_ok=True)
plt.savefig(savename, dpi=300)
plt.close()

#
results_pandas = results_pandas.reset_index()

fig, ax = plt.subplots(figsize=(16, 9))
show_groups = [1]
data_1 = results_pandas.loc[results_pandas["Groups"].isin(show_groups), 1].to_numpy()
data_2 = results_numpy.loc[results_numpy["Groups"].isin(show_groups), 1].to_numpy()
ax.plot(np.arange(data_1.shape[0]), data_1, label="Pandas")
ax.plot(np.arange(data_1.shape[0]), data_2, ls="--", label="Numpy")
ax.set(xlabel=r"$x_t$", ylabel=r"$y_t$")
ax.legend()
fig.tight_layout()

savename = "./groupby_rolling_mean/time-series-plot.png"
os.makedirs(os.path.dirname(savename), exist_ok=True)
plt.savefig(savename, dpi=300)
plt.close()
