# %%
import polars as pl
from lets_plot import *
LetsPlot.setup_html()

# %%
# dat = pl.read_csv("Motor_Vehicle_Collisions_-_Crashes_20240124.csv")\
#     .with_columns(
#         pl.col("CRASH DATE").str.to_date("%m/%d/%Y").alias("date"),
#         pl.col("CRASH TIME").str.to_time("%H:%M").alias("time"),
#         pl.concat_str(["CRASH DATE","CRASH TIME"], separator=" ")\
#             .str.to_datetime("%m/%d/%Y %H:%M").alias("date_time"))

# dat.write_parquet("ny_crashes.parquet", compression="zstd", compression_level=15)
# %%
dat = pl.read_parquet("ny_crashes.parquet")
# %%
# Create a new column that reports the date and base hour the accident happened.
# Use that column to get an accident rate and injury rate per hour data set.
rate_hour = dat\
    .with_columns(pl.col('date_time').dt.truncate('1h').alias('hour_floor'))\
    .with_columns(pl.col('hour_floor').dt.hour())\
    .group_by('hour_floor')\
    .agg(
        # pl.col('NUMBER OF PERSONS INJURED').sum().alias('injured_total'),
        pl.col('BOROUGH').count().alias('accident_count')
    )
rate_hour.head()

# %%
rate_day = dat\
    .with_columns(pl.col('date_time').dt.truncate('1d').alias('day_floor'))\
    .group_by('day_floor')\
    .agg(
        pl.col('NUMBER OF PERSONS INJURED').sum().alias('injured_total'),
        pl.col('BOROUGH').count().alias('accident_count')
    )\
    .with_columns(pl.col("day_floor").dt.weekday().alias("weekday"))

rate_day.head()

# %%
# Now we want to create two visuals: the number of chrashes per hour and one that shows the number of injuries per day
# Use `lets-plot` and `plotly`to build interactive visualizations displaying the rate of injuries over time.
ggplot(rate_day.sort('weekday'), aes(x='weekday', y='accident_count')) +\
    geom_boxplot() +\
    scale_x_discrete()

# %%

ggplot(rate_hour.sort('hour_floor')) + geom_point(aes(x='hour_floor', y='accident_count', color='accident_count'), alpha=0.7, size=4) + \
    scale_color_discrete() + \
    scale_x_discrete() +\
    theme(legend_position='none') + \
    geom_line(aes(x='hour_floor', y='accident_count'), linetype=3)
# %%
