# %%
import polars as pl
import pandas as pd
import plotly.express as px

import plotly.graph_objects as go
from datetime import datetime
from lets_plot import *
LetsPlot.setup_html()

# %%
pdat = pl.read_parquet("stock.parquet")

# %%
# Create a time series chart that shows performance of all 10 stocks.
plot = ggplot(pdat, aes(x='Date', y='AdjClose', color='ticker')) + \
    geom_line() +\
    scale_x_datetime() +\
    labs(
        x="Date",
        y="Adjusted Closing Price",
        title="My chart of the top 10 stocks"
    )

plot.show()
# pdat.head()

# %%
# now fix the html size and only show the last year and save the chart
dat2 = pdat.filter(pl.col("Date").dt.year() == 2023)

plot2 = ggplot(dat2, aes(x='Date', y='AdjClose', color='ticker')) + \
    geom_line() +\
    scale_x_datetime() +\
    labs(
        x="Date",
        y="Adjusted Closing Price",
        title="My chart of the top 10 stocks in 2023"
    ) + ggsize(400, 150)

plot2.show()

# %%
## plotly candlestick chart
# https://plotly.com/python/candlestick-charts/

df=pdat.filter(pl.col('ticker') == "TGT")

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

fig.show()

# %%
