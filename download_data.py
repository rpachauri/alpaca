# Get a set of the tickers we already downloaded data for
from os import listdir
from os.path import isfile, join

mypath='data'

tickers_we_already_have = set()


for f in listdir(mypath):
  if isfile(join(mypath, f)):
    tickers_we_already_have.add(f[0:-4])

# if there are no files, then we want to be able to download all stocks.
# assuming no ticker starts with '!', we will download all stocks.
last_ticker = sorted(tickers_we_already_have)[-1] if len(tickers_we_already_have) > 0 else '!'


import alpaca_trade_api as tradeapi
import api_key

api = tradeapi.REST(key_id=api_key.APCA_API_KEY_ID,secret_key=api_key.APCA_API_SECRET_KEY)

# get the whole list of assets from Alpaca
assets = api.list_assets()

# filter assets by only those that are tradeable
filtered_assets = []
for asset in assets:
  if asset.tradable:
    # we only need the asset symbol in order to get the barset
    filtered_assets.append(asset.symbol)

filtered_assets = sorted(filtered_assets)

# create a sample dataframe
amzn_df = api.get_barset(
    symbols='AMZN',
    timeframe="1D",
    limit=253,
  ).df

# amzn_df['AMZN'].to_csv('data/AMZN.csv')

# get the start and end date from the sample dataframe
start_date = amzn_df.index[0].to_pydatetime().date()
end_date = amzn_df.index[-1].to_pydatetime().date()

# save all assets with the same timeframe of data as our sample dataframe
for asset in filtered_assets:
  # skip downloading for assets we already have
  if asset < last_ticker:
    continue

  print("Getting data for:", asset)
  returned_data = api.get_barset(
      symbols=asset,
      timeframe="1D",
      limit=253,
    ).df
  
  if (len(returned_data.index) == 0):
    # there is no data for this asset
    continue

  if (returned_data[asset]['close'].mean()) < 10:
    # filter out stocks for which the mean prices is less than $10
    continue

  # if the dataframe has the same timeframe as our sample dataframe:
  if (returned_data.index[0].to_pydatetime().date() == start_date and
      returned_data.index[-1].to_pydatetime().date() == end_date):
    # save the dataframe using the ticker symbol as the name
    print("Saving:", asset)
    returned_data[asset].to_csv('data/' + asset + '.csv')