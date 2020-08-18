import pandas as pd

from os import listdir
from os.path import isfile, join

def read_csv(directory, ticker):
  return pd.read_csv(directory + ticker + ".csv",
    index_col='time',
    parse_dates=['time'],
    usecols=['time', 'close']
  )

def load_closing_data(directory):
  '''
  Requires:
    - all files in directory must be .csv files with the appropriate data format:
      1. number of rows are all the same
      2. each .csv file has *the same* 'time' column
      3. each .csv file has a 'closing' column
  Returns:
    df: pandas.DataFrame
        - df.index will be the 'time' column that matches the 'time' column of all the given data
        - has the closing column of every ticker in the given directory
  '''
  files = listdir(directory)

  ticker1 = files[0][0:-4]
  ticker2 = files[1][0:-4]

  df1 = read_csv(directory, ticker1)
  df2 = read_csv(directory, ticker2)

  # Leave the 'close' column for ticker1 without a suffix so that added columns cannot be named 'close'.
  # Will change the name to include the suffix later.
  df = df1.join(df2, rsuffix=ticker2)

  for i in range(2, len(files)):
    # Ignore hidden files (e.g. ".DS_Store")
    f = files[i]
    if not f.startswith('.') and isfile(join(directory, f)):
      ticker3 = f[0:-4]
      # Note that you may not see all files being read because we are ignoring hidden files.
      print("Reading file", i, "of", len(files),":", ticker3)
      df3 = read_csv(directory, ticker3)
      df = df.join(df3, rsuffix=ticker3)

  # Now that we're done adding columns, we can rename 'close' to correspond to ticker1.
  df = df.rename(columns={"close": "close" + ticker1})

  return df

df = load_closing_data('data/')
df.to_csv('accumulated_data/my_close_data.csv')