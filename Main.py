from model import create_model
from model import test_predictions
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
data = "SPY-5-years.csv"
model = create_model(data)
predictions, etf_prices = test_predictions(model,"SPY.csv")
p_list = predictions.tolist()
balance = 1000000
stock_count = 0

etf_price_list = etf_prices.tolist()
pl = []
days = []
assets = []

for i in range(0,len(p_list)):
    prediction = p_list[i][0] 
    if (prediction < 0.001):
        balance += stock_count*etf_price_list[i]
        stock_count = 0
    elif (prediction < 0.005 and prediction > 0.001):
        if ( balance - etf_price_list[i]*100 > 0):
            stock_count += 20
            balance -= etf_price_list[i]*20
    elif (prediction < 0.01 and prediction > 0.005):
        if ( balance - etf_price_list[i]*100 > 0):
            stock_count += 100
            balance -= etf_price_list[i]*100
    elif (prediction > 0.01):
        if ( balance - etf_price_list[i]*300 > 0):
            stock_count += 300
            balance -= etf_price_list[i]*300
    pl.append(((balance+etf_price_list[i]*stock_count)-1000000))
    assets.append(etf_price_list[i]*stock_count)
    days.append(i)


plt.plot(days,pl)
balance += etf_price_list[-1]*stock_count 
print("P\L = " + str(balance-1000000))
plt.show()
plt.plot(days,assets)
plt.show()