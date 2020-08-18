# alpaca
Using the Alpaca API

## Environment Setup
I created this project using the anaconda distribution. You can install it [here](https://docs.anaconda.com/anaconda/install/). If you prefer a lightweight version, you can [install Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) instead.

Create the conda environment with:

    $ conda env create -f environment.yml

Activate the conda environment with:

    $ conda activate alpaca

## Collecting OHLCV Data
If you'd like to play around with generating the data, follow these steps:
  1. `$ touch api_key.py`
  2. Add APCA_API_KEY_ID and APCA_API_SECRET_KEY to your `api_key.py` file.
  
      1. You have to get your own API keys from Alpaca. `api_key.py` has already been added to the `.gitignore` file. This is important because you should not be sharing your API keys with anyone.
      2. An example of what this file should look like is given below:
  
    APCA_API_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
    APCA_API_SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
  
  3. `$ python download_data.py`

      1. First, this program downloads OHLCV data from Alpaca for the past 253 days for AMZN.
      2. While Alpaca will let you retrieve OHLCV for up to 200 assets at a time, I found the responses to be weird. It seems that a request is made for 253 days of valid data _for each stock_. This means that if an asset is missing data from the most recent 253 days, then the returned pandas DataFrame will have > 253 rows with NaN values for the dates an asset is missing data but another asset has data.
      3. To counteract this, I retrieve OHLCV data for each asset and make sure the timeframe matches the timeframe for AMZN. Note that this means you'll easily be hitting the rate limit.
      4. I also filter out assets that aren't tradable or have a mean closing price lower than $10. Feel free to edit these filters. For context, I found these filters reduced the number of assets from ~8,000 to ~1,300.
      5. Saves each asset to a .csv file in the directory `data/`

  4. `$ python accumulate_data.py`

      1. This program reads the .csv files in the directory `data/`
      2. It accumulates the close data for all those files into one pandas Dataframe and saves it into a file called `my_close_data.csv` in the `accumulated_data/` directory.
      3. And voila! You can use `my_close_data.csv` to perform stock prediction.
      
