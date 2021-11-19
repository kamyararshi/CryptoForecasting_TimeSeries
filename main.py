import pandas as pd
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

data = cg.get_coin_ohlc_by_id('bitcoin', 'usd', 'max')
df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close']);
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms');
print(df.head(10));