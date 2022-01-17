from pycoingecko import CoinGeckoAPI
from datetime import datetime
import pandas as pd


def update_data():
    data = pd.read_csv("BINANCE_BTCUSDT, 1D.csv")
    date = data["time"]
    timestamp = datetime.strptime(date[len(date) - 1], '%Y-%m-%dT%H:%M:%SZ').timestamp()

    cg = CoinGeckoAPI()
    weekly_ohlc = cg.get_coin_ohlc_by_id("bitcoin", "usd", 30)
    high, low = -1, 999999999
    counter = 0
    day_started = False
    saved_date, opening = "", ""

    for each_list in weekly_ohlc:
        date_in_list = datetime.utcfromtimestamp(each_list[0] / 1000).strftime('%Y-%m-%dT%H:%M:%SZ')
        if timestamp+3600 < each_list[0] / 1000:
            if date_in_list.endswith("00:00:00Z"):
                opening = each_list[1]
                high, low = each_list[2], each_list[3]
                day_started = True
                saved_date = date_in_list
                counter += 1
            else:
                if day_started:
                    counter += 1
                    if each_list[2] > high:
                        high = each_list[2]
                    if each_list[3] < low:
                        low = each_list[3]
        if counter == 6:
            close = each_list[4]
            counter = 0
            day_started = False
            data.loc[len(data)] = {'time': saved_date, 'open': opening, 'high': high, 'low': low, 'close': close}

    data.to_csv("BINANCE_BTCUSDT, 1D.csv", index=False)


if __name__ == '__main__':
    update_data()
