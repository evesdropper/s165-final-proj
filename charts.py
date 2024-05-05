import numpy as np
import pandas as pd

TS_ALBUMS = {
        "Lover": ["2019/08/23", "2019/10/17"],
        "Folklore": ["2020/07/24", "2020/09/17"],
        "Evermore": ["2020/12/11", "2021/02/05"],
        "Midnights": ["2022/10/21", "2022/12/10"],
}

df = pd.read_csv("./charts.csv").dropna()
df = df.loc[df["country"] == "us"]
df = df[["date", "position", "streams", "artists"]]

ts_init = df.loc[df["artists"] == "['Taylor Swift']"].sort_values("date")
ts_init['date'] = pd.to_datetime(ts_init['date']) 

for album, daterange in TS_ALBUMS.items():
    start_date, end_date = daterange[0], daterange[1]
    mask = (ts_init['date'] > start_date) & (ts_init['date'] <= end_date)
    ts_album = ts_init[["date", "position", "streams"]].loc[mask]
    ts_album_grouped = ts_album.groupby(["date"]).agg("mean", "sum")
    ts_album_grouped["streams"] = ts_album_grouped["streams"].astype(int)
    ts_album_grouped.to_csv(f"{album.lower()}-streaming.csv")
