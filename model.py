

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.preprocessing import scale
import tensorflow as tf
import statsmodels.api as sm
import keras.losses
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt

def create_model(data):
    
    df = pd.read_csv(data)

    df['daily_future_close'] = df['Last'].shift(-1)
    df['daily_close_future_pct'] = df['daily_future_close'].pct_change()
    df['daily_close_pct'] = df['Last'].pct_change()
    df['daily_vol_pct'] = df['Volume'].pct_change()

    # a list of the feature names for later
    feature_names = ['daily_close_pct']  

    # Create SMA moving averages and rsi for timeperiods of 14, 30, and 50
    for n in [14, 30, 50]:

     # Create the SMA indicator for each value in last
      df['ma' + str(n)] = df['Last'].rolling(n).mean().pct_change()
      feature_names += ['ma' + str(n)]
 
    # Drop all na values
    df = df.dropna()
    feature_names += ['daily_vol_pct']
    features = df[feature_names]
    targets = df['daily_close_future_pct']


    linear_features = sm.add_constant(features)
    train_features = linear_features
    train_targets = targets


    # Create the linear model and complete the least squares fit
    model = sm.OLS(train_targets, train_features)

    # Standardize the train features
    scaled_train_features = scale(train_features)

    # Create the model
    epochs = [1000]
    layers = [[25,30,1]]

    def model_func(layer):
        model = Sequential()
        model.add(Dense(layer[0], input_dim=scaled_train_features.shape[1], activation='relu'))
        model.add(Dense(layer[1], activation='relu'))
        model.add(Dense(layer[2], activation='linear'))
        return model

    for epoch in epochs:
        for layer in layers:
            model = model_func(layer)
            model.compile(optimizer='adam', loss='mse')
#            history = model.fit(scaled_train_features, train_targets, epochs=epoch)

    #plot loss function
#     plt.plot(history.history['loss'])
#     plt.title('Loss Function: ' + str(round(history.history['loss'][-1], 6)))
#     plt.show()
    train_preds = model.predict(scaled_train_features)

    #Plot predictions vs actual
    plt.scatter(train_preds, train_targets)
    plt.xlabel('Predictions')
    plt.ylabel('Actual')
    plt.show()

    return model

def test_predictions(model,data):

    df = pd.read_csv(data)


    df['daily_close_pct'] = df['Last'].pct_change()
    df['daily_vol_pct'] = df['Volume'].pct_change()

    # a list of the feature names for later
    feature_names = ['daily_close_pct']  

    # Create SMA moving averages and rsi for timeperiods of 14, 30, and 50
    for n in [14, 30, 50]:
      df['ma' + str(n)] = df['Last'].rolling(n).mean().pct_change()
      feature_names += ['ma' + str(n)]

    feature_names += ['daily_vol_pct']
    df = df.dropna()
    features = df[feature_names]
    test_features = sm.add_constant(features)
    scaled_test_features = scale(test_features)
    test_preds = model.predict(scaled_test_features)
    
    return test_preds, df['Last']