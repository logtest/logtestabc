import numpy as np
import pandas as pd
import iisignature

def compute_levy_area_from_returns_iisignature_new(returns1, returns2, T=1.0):
    """
    Calculate Lévy area from two lists of stock daily returns using iisignature (new method, no time component).
    
    Parameters:
    returns1 (list or np.array): Daily returns of stock 1
    returns2 (list or np.array): Daily returns of stock 2
    T (float): Time horizon (default 1.0, normalized, unused here)
    
    Returns:
    float: Lévy area (positive if stock1 leads, negative if stock2 leads)
    """
    # Ensure inputs are numpy arrays and have the same length
    returns1 = np.array(returns1)
    returns2 = np.array(returns2)
    if len(returns1) != len(returns2):
        raise ValueError("Return series must have the same length")
    
    # Cumulate returns to get paths (like log-prices)
    path1 = np.cumsum(returns1)
    path2 = np.cumsum(returns2)
    
    # Construct 2D path [X_t, Y_t]
    path = np.column_stack([path1, path2])
    
    # Compute signature up to level 2
    signature = iisignature.sig(path, 2)
    
    # Lévy area = ((X,Y) - (Y,X)) / 2
    # Signature terms for [X, Y]: [X, Y, (X,X), (X,Y), (Y,X), (Y,Y)]
    XY_index = 3  # (X,Y) term
    YX_index = 4  # (Y,X) term
    levy_area = 0.5 * (signature[XY_index] - signature[YX_index])
    
    return levy_area

def compute_levy_area_from_returns_pandas(returns1, returns2, T=1.0):
    """
    Calculate Lévy area from two lists of stock daily returns using Pandas.
    
    Parameters:
    returns1 (list or np.array): Daily returns of stock 1
    returns2 (list or np.array): Daily returns of stock 2
    T (float): Time horizon (default 1.0, normalized)
    
    Returns:
    float: Lévy area (positive if stock1 leads, negative if stock2 leads)
    """
    # Convert inputs to Pandas Series
    returns1 = pd.Series(returns1)
    returns2 = pd.Series(returns2)
    if len(returns1) != len(returns2):
        raise ValueError("Return series must have the same length")
    
    # Cumulate returns to get paths (like log-prices)
    path1 = returns1.cumsum()
    path2 = returns2.cumsum()
    
    # Compute increments (dY_t = Y_{t+1} - Y_t, dX_t = X_{t+1} - X_t)
    dY = returns2  # Returns are the increments
    dX = returns1
    
    # Compute integrands: X_t * dY_t - Y_t * dX_t
    #integrand = path1.shift(1) * dY - path2.shift(1) * dX
    integrand = path1 * dY - path2 * dX
    
    # Sum, skipping NaN (first term due to shift)
    levy_area = integrand[1:].sum() / 2
    
    return levy_area


def calc_levy_area_path(path):
    # signature of path up to level 2
    signature = iisignature.sig(path, 2) 
    # levy area
    levy_area = 0.5 * (signature[3] - signature[4])    
    return levy_area

# levy area
def calc_levy_area(x,y):
    path = np.append(x.reshape((-1,1)), y.reshape((-1,1)), axis=1)
    #return calc_levy_area_path(path)
    signature = iisignature.sig(path, 2) 
    return  0.5 * (signature[3] - signature[4]) 

def calc_levy_area_v2(x,y):
    #x = (x - x.mean())/x.std()
    #y = (y - y.mean())/y.std()
    
    path_x = x.cumsum()
    path_y = y.cumsum()
    
    path = np.append(path_x.reshape((-1,1)), path_y.reshape((-1,1)), axis=1)
    #return calc_levy_area_path(path)
    signature = iisignature.sig(path, 2) 
    return  0.5 * (signature[3] - signature[4]) 


def main():
    # Example: Simulated daily returns
    np.random.seed(42)
    N = 252  # Approx. 1 year of trading days
    returns1 = np.random.normal(0, 0.05, N)  # Stock 1 returns
    returns2 = np.random.normal(0, 0.05, N)  # Stock 2 returns
    # Introduce a slight lag in returns2 to simulate lead-lag
    returns2[1:] = 0.05*returns2[1:] + 0.95 * returns1[:-1]
    
    # Compute Lévy area using all methods
    levy_area_iisig_new = compute_levy_area_from_returns_iisignature_new(returns1, returns2)
    levy_area_pandas = compute_levy_area_from_returns_pandas(returns1, returns2)
    calc_levy_area(returns1,returns2)
    calc_levy_area_v2(returns1,returns2)
    
    # Print results
    print(f"Lévy area (iisignature, new, no time): {levy_area_iisig_new:.6f}")
    print(f"Lévy area (Pandas): {levy_area_pandas:.6f}")

    print(f"Difference (new iisig vs Pandas): {abs(levy_area_iisig_new - levy_area_pandas):.6f}")

    # Interpret result
    if levy_area_iisig_new > 0:
        print("Stock 1 may lead Stock 2")
    elif levy_area_iisig_new < 0:
        print("Stock 2 may lead Stock 1")
    else:
        print("No clear lead-lag relationship")
    
    # Debugging: Compare integrands
    path1 = np.cumsum(returns1)
    path2 = np.cumsum(returns2)
    dY = returns2
    dX = returns1
    integrand_pandas = (pd.Series(returns1).cumsum().shift(1) * pd.Series(returns2) - 
                        pd.Series(returns2).cumsum().shift(1) * pd.Series(returns1))[1:]
    integrand_manual = pd.Series(path1[:-1] * dY[1:] - path2[:-1] * dX[1:])
    print("\nDebugging: Mean absolute difference in integrands (Pandas vs manual):", 
          np.abs(integrand_pandas - integrand_manual).mean())
    
    
    data = pd.read_csv('c:/temp/levy_testdata.csv',index=True)
    data = data[['BTC-USD','ETH-USD']]
    # Calculate the returns based on 'Adj Close'
    rets = data.pct_change().dropna()

    # Standardize the returns
    std_rets = (rets - rets.mean()) / rets.std()


    # Define the path
    path = std_rets.values
    
    r1 = path[:,0]
    r2 = path[:,1]
    
    #below is good!!!
    compute_levy_area_from_returns_iisignature_new(r1, r2)
    compute_levy_area_from_returns_pandas(r1, r2)
    calc_levy_area(r1,r2)
    calc_levy_area_v2(r1,r2)
    

if __name__ == "__main__":
    main()