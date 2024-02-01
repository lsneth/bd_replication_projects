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
# dat2 = pdat.filter(pl.col('Date').str.contains(['2024']))
plot2 = plot + ggsize(400, 150) + coord_fixed(xlim=(pl.datetime(year=2023, month=1, day=1), pl.datetime(year=2024, month=12, day=31)))
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
