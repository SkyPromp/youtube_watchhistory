from re import findall
from html import unescape


def reformat_data(input_file):
    with open(input_file, encoding="utf-8") as f:
        with open("WatchHistory.csv", "w", encoding="utf-8") as history:
            for line in f:
                if "content-cell" in line:
                    line = unescape(line)
                    vids = findall(r'<div class="content-cell[^"]*">Je hebt naar(.*?)</div>', line)

                    for v in vids:
                        v = v.replace(";", ":")  # for csv encoding purposes
                        data = findall(r'<a href="([^"]*)">([^<]*)</a>.*?gekeken<br><a href="([^"]*)">([^<]*)</a><br>(.*)', v)
                        if data:
                            data = data[0]
                            video_link, video_name, channel_link, channel_name, date = data
                            history.write(f"{video_name};{channel_name};{date};{video_link};{channel_link}\n")


def get_stats(csv_file):
    hist_channels = {}
    hist_vids = {}

    with open(csv_file, "r", encoding="utf-8") as csv:
        for line in csv:
            video_name, channel_name, date, video_link, channel_link = line.rstrip("\n").split(";")

            if channel_name not in hist_channels:
                hist_channels[channel_name] = 1
            else:
                hist_channels[channel_name] += 1

            formatted = f"{video_name};{channel_name}"

            if formatted not in hist_vids:
                hist_vids[formatted] = 1
            else:
                hist_vids[formatted] += 1

    hist_channels = hist_channels.items()
    hist_channels = sorted(hist_channels, key=lambda datapoint: datapoint[1], reverse=True)

    with open("ChannelsWatched.csv", "w", encoding="utf-8") as f:
        for channel, amount in hist_channels:
            f.write(f"{channel};{amount}\n")

    hist_vids = hist_vids.items()
    hist_vids = sorted(hist_vids, key=lambda datapoint: datapoint[1], reverse=True)

    with open("VidsWatched.csv", "w", encoding="utf-8") as f:
        for vid, amount in hist_vids:
            f.write(f"{vid};{amount}\n")


reformat_data("MyActivity.html")
get_stats("WatchHistory.csv")
