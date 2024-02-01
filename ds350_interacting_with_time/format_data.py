# %%
import polars as pl
import pandas as pd
import yfinance as yf
# %%
url = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
table = pd.read_html(url)[0]
tickers_500 = table.Symbol.tolist()
tickers_use = ["CXW", "F", "GM", "KR", "WDC", "NKE","T", "WDAY", "WFC", "WMT", "TGT"]

# %%
pl.Config.set_fmt_str_lengths(100)
pl.Config.set_tbl_rows(50)
pl.Config.set_fmt_table_cell_list_len(100)

# %%
# example for one ticker
msft = yf.Ticker("MSFT")
msft.history(period="2y", interval="1h")

# %%
dat = yf.download(tickers_use, period="5y", interval="1d").reset_index()


# %%
dat = pl.from_pandas(dat).melt(id_vars="('Date', '')")\
    .with_columns(
        pl.col("variable").str.replace_many(["'", "(", ")", " "], "").str.split_exact(',', 1)
    )\
    .unnest('variable')\
    .rename({"('Date', '')": 'Date'})\
    .pivot(columns='field_0', values='value', index=["Date", "field_1"], aggregate_function='first')\
    .rename({"field_1": 'ticker'})

dat.write_parquet('./stock.parquet')
# %%
# We want this.
# ┌────────┬──────────────┬───────────┬───────────┬───────────┬───────────┬───────────┬──────────┐
# │ ticker ┆ date         ┆ Adj Close ┆ Close     ┆ High      ┆ Low       ┆ Open      ┆ Volume   │
# │ ---    ┆ ---          ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---      │
# │ str    ┆ datetime[ns] ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64      │
# ╞════════╪══════════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪══════════╡
# │ CXW    ┆ 2019-01-25   ┆ 16.794144 ┆ 19.17     ┆ 19.360001 ┆ 18.959999 ┆ 19.280001 ┆ 496300.0 │
# │        ┆ 00:00:00     ┆           ┆           ┆           ┆           ┆           ┆          │
# │ CXW    ┆ 2019-01-28   ┆ 16.855467 ┆ 19.24     ┆ 19.360001 ┆ 18.889999 ┆ 19.120001 ┆ 621000.0 │
# │        ┆ 00:00:00     ┆           ┆           ┆           ┆           ┆           ┆          │
# │ CXW    ┆ 2019-01-29   ┆ 17.197132 ┆ 19.629999 ┆ 19.690001 ┆ 19.139999 ┆ 19.290001 ┆ 457800.0 │
# │        ┆ 00:00:00     ┆           ┆           ┆           ┆           ┆           ┆          │
# │ CXW    ┆ 2019-01-30   ┆ 17.144569 ┆ 19.57     ┆ 19.790001 ┆ 19.4      ┆ 19.629999 ┆ 534000.0 │
# │        ┆ 00:00:00     ┆           ┆           ┆           ┆           ┆           ┆          │
# │ CXW    ┆ 2019-01-31   ┆ 17.407389 ┆ 19.870001 ┆ 19.870001 ┆ 19.33     ┆ 19.58     ┆ 526000.0 │
# │        ┆ 00:00:00     ┆           ┆           ┆           ┆           ┆           ┆          │
# └────────┴──────────────┴───────────┴───────────┴───────────┴───────────┴───────────┴──────────┘

# pdat = 



# pdat.write_parquet("stock.parquet")
# %%
