import numpy as np
from scipy.special import softmax

def create_portfolio(num_assets, num_assets_in_portfolio):
  '''
  Args:
    num_assets: the number of assets in our stock universe
    num_assets_in_portfolio: a number in the range [1, num_assets]
  Requires:
    1 <= num_assets_in_portfolio <= num_assets
  Returns:
    portfolio_weights:
      - has shape (num_assets, 1)
      - only num_assets_in_portfolio have weights; all other assets have weights == 0
      - sum(portfolio_weights) == 1
  '''
  # asset_weights are the weights we'd like to assign to the assets we will choose.
  asset_weights = []
  for _ in range(num_assets_in_portfolio):
    asset_weights.append(np.random.random())
  # Make the asset weights sum to 1.
  asset_weights = softmax(np.array(asset_weights))

  # asset_indices maintains a 1:1 relationship with asset_weights.
  # We will make portfolio_weights[asset_indices[i]] = asset_weights[i]
  asset_indices = np.random.choice(a=np.arange(num_assets), size=num_assets_in_portfolio)

  # Create portfolio weights from these asset weights.
  portfolio_weights = np.zeros(shape=(num_assets, 1))
  for i in range(num_assets_in_portfolio):
    portfolio_weights[asset_indices[i]] = asset_weights[i]
  return portfolio_weights

def create_list_of_portfolios(num_assets):
  '''
  Returns:
    portfolios:
      - a list of portfolios
  '''
  portfolios = []
  # minimum of 2 assets in each portfolio.
  for num_assets_in_portfolio in range(2, num_assets):
    # create 10 portfolios where each portfolio consists of num_assets_in_portfolio assets.
    for _ in range(10):
      portfolios.append(create_portfolio(num_assets, num_assets_in_portfolio))
  return portfolios