# Copyright (c) 2026 Olga Scrivner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Regenerate the original W08 synthetic dataset and four instructional figures.

Run from any directory: python path/to/module08/generate_figures.py
Requires numpy, pandas, matplotlib, and statsmodels. No network access needed.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

HERE = Path(__file__).resolve().parent
FIGURES = HERE / "figures"
FIGURES.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.dpi": 160})
BLUE, ORANGE, GREEN = "#0072B2", "#D55E00", "#009E73"

rng = np.random.default_rng(8)
dates = pd.date_range("2020-01-01", periods=60, freq="MS")
t = np.arange(60)
values = np.round(100 + 0.8 * t + 20 * np.sin(2 * np.pi * t / 12)
                  + rng.normal(0, 4, 60), 1)
s = pd.Series(values, index=dates, name="demand")
s.rename_axis("month").to_csv(HERE / "monthly_demand.csv")


def save(fig, name):
    fig.savefig(FIGURES / name, bbox_inches="tight")
    plt.close(fig)


fig, ax = plt.subplots(figsize=(9, 4.5), layout="constrained")
ax.plot(s.index, s, color=BLUE, label="Monthly demand", marker=".")
ax.plot(s.index, s.rolling(12).mean(), color=ORANGE,
        linewidth=2, label="Trailing 12-month mean")
ax.annotate("Peaks recur about 12 months apart", xy=(s.index[15], s.iloc[15]),
            xytext=(s.index[3], 168), arrowprops={"arrowstyle": "->"})
ax.annotate("Underlying level rises", xy=(s.index[45], 130),
            xytext=(s.index[23], 82), arrowprops={"arrowstyle": "->"})
ax.set(title="Synthetic monthly demand: trend and annual seasonality",
       xlabel="Month", ylabel="Demand (illustrative units)", ylim=(70, 180))
ax.legend(loc="upper right")
save(fig, "patterns.png")

result = STL(s, period=12, robust=True).fit()
fig, axes = plt.subplots(4, 1, sharex=True, figsize=(9, 8), layout="constrained")
for ax, data, label in zip(axes, [s, result.trend, result.seasonal, result.resid],
                         ["Observed", "Trend", "Seasonal", "Remainder"]):
    ax.plot(s.index, data, color=BLUE)
    ax.set_ylabel(label + "\n(units)")
axes[2].axhline(0, color="0.5", linewidth=0.8)
axes[3].axhline(0, color="0.5", linewidth=0.8)
axes[0].set_title("STL decomposition of the complete historical series (period = 12)")
axes[-1].set_xlabel("Month")
save(fig, "decomposition.png")

fig, axes = plt.subplots(1, 2, figsize=(9, 4.5), layout="constrained")
for ax, lag in zip(axes, [1, 12]):
    ax.scatter(s.shift(lag), s, color=BLUE, alpha=0.8)
    ax.set(xlabel=f"Demand {lag} month(s) earlier (units)",
           ylabel="Current demand (units)", title=f"Lag {lag} months")
fig.suptitle("Lag plots: nearby values and the same month last year")
save(fig, "lags.png")

train, test = s.iloc[:-12], s.iloc[-12:]
naive = pd.Series(train.iloc[-1], index=test.index)
seasonal = pd.Series(train.iloc[-12:].to_numpy(), index=test.index)
fig, ax = plt.subplots(figsize=(9, 4.5), layout="constrained")
ax.plot(train.index, train, color="0.4", label="Training observations")
ax.plot(test.index, test, color=BLUE, marker="o", label="Held-out actuals")
ax.plot(test.index, naive, color=ORANGE, linestyle="--", label="Naive forecast")
ax.plot(test.index, seasonal, color=GREEN, linestyle=":", linewidth=2.5,
        label="Seasonal naive forecast")
boundary = train.index[-1] + (test.index[0] - train.index[-1]) / 2
ax.axvline(boundary, color="black", linestyle="--", label="Forecast cutoff")
ax.axvspan(boundary, test.index[-1], color="0.8", alpha=0.2)
ax.set(title="Forecasts made at December 2023: next 12 months",
       xlabel="Month", ylabel="Demand (illustrative units)")
ax.legend(loc="upper left", fontsize=9)
save(fig, "forecasts.png")

for name, forecast in [("Naive", naive), ("Seasonal naive", seasonal)]:
    error = test - forecast
    print(f"{name}: MAE={error.abs().mean():.2f}, RMSE={np.sqrt((error**2).mean()):.2f}")
