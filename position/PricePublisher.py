import asyncio
import threading

import task
from scipy.stats import norm

from option.models import Option
from option.serializers import OptionSerializer
from position import QueueEngine
from stock.models import Stock
from stock.serializers import StockSerializer
import time

import numpy as np

risk_free_rate = 0.2
publisher_enabled = False
thread: threading.Thread = None

def geometric_brownian_motion(S0, mu, sigma, T, dt):
    """
    Simulate a Geometric Brownian Motion path.

    Parameters:
    S0 : float : Initial stock price
    mu : float : Expected return
    sigma : float : Volatility
    T : float : Total time (in years)
    dt : float : Time step (in years)

    Returns:
    np.array : Simulated stock prices
    """
    N = int(T / dt)  # Number of time steps
    t = np.linspace(0, T, N)
    W = np.random.standard_normal(size=N)
    W = np.cumsum(W) * np.sqrt(dt)  # Brownian motion
    X = (mu - 0.5 * sigma ** 2) * t + sigma * W
    S = S0 * np.exp(X)
    return S


def black_scholes(S, K, T, r, sigma, option_type='CALL'):
    """
    S       Current stock price
    K       Strike price
    T       Time to maturity in years (5 trading days)
    r       Risk-free interest rate
    sigma   Volatility
    """
    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'CALL':
        # Calculate call option price
        call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return call_price
    elif option_type == 'PUT':
        # Calculate put option price
        put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return put_price

def do_publishing():
    global publisher_enabled
    publisher_enabled = True
    stocks = StockSerializer(instance=Stock.objects.all(), many=True)
    options = OptionSerializer(instance=Option.objects.all(), many=True)
    while publisher_enabled:
        price_dict: dict = {}
        for stock in stocks.data:
            stock_price = geometric_brownian_motion(float(stock["initial_price"]), float(stock["expected_return"]),
                                                    float(stock["volatility"]),
                                                    1.0/252.0, 1/252.0)
            price_dict[stock["symbol"]] = float(stock_price[0])
        for option in options.data:
            option_price = black_scholes(price_dict[option["stock_symbol"]], float(option["strike_price"]),
                                         option["days_to_maturity"],
                                         risk_free_rate, float(option["volatility"]), option["option_type"])
            price_dict[option["symbol"]] = float(option_price)
        print(price_dict)
        QueueEngine.put(price_dict)
        time.sleep(1)  # Publish every second

def start_publishing():
    global thread
    if thread is None:
        thread = threading.Thread(target=do_publishing)
    if not thread.is_alive():
        thread.start()

def stop_publishing():
    global publisher_enabled
    publisher_enabled = False
    global thread
