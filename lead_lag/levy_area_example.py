
import numpy as np

# Define data arrays
X1 = np.array([1., 3., 5., 8.]).reshape((-1,1))
X2 = np.array([1., 4., 2., 6.]).reshape((-1,1))

# Construct a path from the data
path = np.append(X1, X2, axis=1)
print(f"Path Length = {path.shape[0]}, Path Dimension = {path.shape[1]}.")
print(f'Path = \n{path}')



import iisignature

signature = iisignature.sig(path, 2)   # signature of path up to level 2
signature



def calc_levy_area_path(path):
    # signature of path up to level 2
    signature = iisignature.sig(path, 2) 
    # levy area
    levy_area = 0.5 * (signature[3] - signature[4])    
    return levy_area


def calc_levy_area(x,y):
    path = np.append(x.reshape((-1,1)), y.reshape((-1,1)), axis=1)
    return calc_levy_area_path(path)


import yfinance as yf
# Define ticker symbols
tickers = ['BTC-USD', 'ETH-USD']

# Download historical data and filter-out Adj Close
data = yf.download(tickers, start='2023-09-01', end='2025-05-19')
data = data['Close']

# Calculate the returns based on 'Adj Close'
rets = data.pct_change().dropna()

# Standardize the returns
std_rets = (rets - rets.mean()) / rets.std()

# Define the path
path = std_rets.values

# Calculate Levy area
print(f'Lévy area between Bitcoin and Etherium is equal to {calc_levy_area_path(path)}')

calc_levy_area(np.array(std_rets['BTC-USD']),np.array(std_rets['ETH-USD']))


