from itertools import groupby

import numpy as np
import pandas as pd

df = pd.DataFrame(
    {
        "Group": ["A"] * 4 + ["B"] * 4,
        "Timestamp": ["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04"] * 2,
        "Value": [1.0, 0.9, 1.2, 1.1, 2.2, 2.0, 2.5, 2.3],
    }
)

# df = df.sort_values("Animal")
grouped = [list(x) for _, x in groupby(df.to_numpy(), key=lambda x: x[0])]

print(grouped[0])

print(grouped[1])

print(np.lib.stride_tricks.sliding_window_view(np.arange(10), 3))
