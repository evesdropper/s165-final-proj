import billboard
import datetime
import matplotlib.pyplot as plt

# albums with Name: Release Date
TS_ALBUMS = {
        "Taylor Swift": "2006-10-24",
        "Fearless": "2008-11-11",
        "Speak Now": "2010-10-25",
        "Red": "2012-10-22",
        "1989": "2014-10-27",
        "Reputation": "2017-11-10",
        "Lover": "2019-08-23",
        "Folklore": "2020-07-24",
        "Evermore": "2020-12-11",
        "Fearless TV": "2021-04-09",
        "Red TV": "2021-11-12",
        "Midnights": "2022-10-21",
        "Speak Now TV": "2023-07-07",
        "1989 TV": "2023-10-27"
}

MODE = "chart"

def get_highest_ranked_song(album_name, release_date, offset_weeks=0):
    chart_date = (datetime.datetime.strptime(release_date, "%Y-%m-%d") + datetime.timedelta(days=7 * offset_weeks)).strftime("%Y-%m-%d")
    chart = billboard.ChartData('hot-100', date=chart_date)
    for i in range(100):
        if chart[i].artist == "Taylor Swift":
            return chart_date, chart[i].title, i+1
    return chart_date, "N/A", 101


if MODE == "csv":
    with open("ts.csv", "w") as f:
        f.write("Album, Date, Highest Ranked Song, Song Ranking\n")
    for album, release_date in TS_ALBUMS.items():
        with open("ts.csv", "a") as f:
            chart_date, song, pos = get_highest_ranked_song(album, release_date)
            f.write(f"{album}, {chart_date}, {song}, {pos}\n")
        for i in range(1, 8):
            with open("ts.csv", "a") as f:
                chart_date, song, pos = get_highest_ranked_song(album, release_date, offset_weeks=i)
                f.write(f" , {chart_date}, {song}, {pos}\n")
        with open("ts.csv", "a") as f:
            f.write(" , , , \n")

if MODE == "chart":
    ts_albums_plot = {}

    for album, release_date in TS_ALBUMS.items():
        album_charthistory = []
        for i in range(8):
            _, _, pos = get_highest_ranked_song(album, release_date, offset_weeks=i)
            album_charthistory.append(pos)
        ts_albums_plot[album] = album_charthistory

    for album, charthistory in ts_albums_plot.items():
        plt.plot(charthistory, label=album)
    plt.title("Taylor Swift Billboard Hot 100 Chart Placing for previous albums")
    plt.xlabel("Weeks after Album Release")
    plt.ylabel("Position on Billboard Hot 100")
    plt.gca().invert_yaxis()
    plt.ylim(1, 101)
    plt.legend(loc=1)
    plt.show()
    plt.savefig("./data/album-rankings.png")
