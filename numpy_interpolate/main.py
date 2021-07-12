import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(1234)


def interpolate(y, x, limit_direction="both"):
    x_p = x.squeeze()
    isnan = np.isnan(y)
    y_p = y[~isnan]

    if limit_direction == "forward":
        start = np.where(~isnan)[0][0]
        interp_idx = np.where(isnan)[0][start:]
        y_interp = np.interp(x_p[interp_idx], x_p[~isnan], y_p)
        y[interp_idx] = y_interp
        return y
    elif limit_direction == "backward":
        end = np.where(~isnan)[0][-1]
        interp_idx = np.where(isnan)[0][:end]
        y_interp = np.interp(x_p[interp_idx], x_p[~isnan], y_p)
        y[interp_idx] = y_interp
        return y
    elif limit_direction == "both":
        y_interp = np.interp(x_p[isnan], x_p[~isnan], y_p)
        y[isnan] = y_interp
        return y


n = 100
Y = np.random.standard_normal((n, 10))
x = np.arange(n).reshape(-1, 1)

missing_index = np.unravel_index(np.random.choice(n * 10, 500), Y.shape)
Y[missing_index] = np.nan

Y = np.array(
    [
        [np.nan, np.nan, 4],
        [np.nan, 3, 4],
        [3, np.nan, np.nan],
        [9, 74, np.nan],
        [29, np.nan, 32],
        [np.nan, np.nan, 34],
    ]
)
x = np.arange(6).reshape(-1, 1)

# Pandas
Y_df = pd.DataFrame(Y)

start = time.time()
Y_df = Y_df.interpolate(limit_direction="backward")
pandas_time = time.time() - start

start = time.time()
Y_interp = np.apply_along_axis(interpolate, 0, Y.copy(), x=x, limit_direction="backward")
Y_interp_df = pd.DataFrame(Y_interp)
numpy_time = time.time() - start

print(Y)
print("------")
print(Y_interp)
print(Y_df)

# fig, ax = plt.subplots()
# ax.plot(x.squeeze(), Y[:, 0], "o", label="Original")
# ax.plot(x.squeeze(), Y_df.to_numpy()[:, 0], "^", label="Pandas")
# ax.plot(x.squeeze(), Y_interp[:, 0], ".", label="Numpy")

# ax.legend()

# fig.tight_layout()
# plt.show()

# print(f"Pandas: {pandas_time:.10f}, Numpy: {numpy_time:.10f}")
# print((Y_df.to_numpy()[missing_index] - Y_interp[missing_index]).sum())
