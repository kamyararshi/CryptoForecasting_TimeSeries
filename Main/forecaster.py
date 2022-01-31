import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import tensorflow as tf

#assert tf.version.VERSION > 2.3.1 , print("Upgrade tensorflow")

path = "BINANCE_BTCUSDT, 1D.csv"
def prepare_data(path):
    """
    
    """
    assert type(path)==type(''), print("path is not string")

    # Loading Data
    data = pd.read_csv(path, date_parser = True)
    data["time"] = data["time"].apply(lambda x: x[:10])
    data['diff'] = data['close']-data['open']
    # MinMaxScaling
    scaler = StandardScaler()
    dataf = data.drop("time", axis=1).to_numpy()
    datas = scaler.fit_transform(dataf)

    # Creating sequences of 60 instances
    X = [] 
    Y = []
    for i in range(60, data.shape[0]):

        X.append(datas[i-60:i])
        #Y.append(datas[i,:-1])
    
    return np.array(X), scaler, data


path_model = "Multivariate_LSTM_4out_diff_stdscale.h5"
def forecast(X, scaler, path_model=path_model):
    """
    
    """
    model = tf.keras.models.load_model(path_model)
    #X, _, scaler, _ = prepare_data(path=path_data)
    
    predictions = model.predict(X)*np.sqrt(scaler.var_[:-1]) + scaler.mean_[:-1]
    
    return predictions


def estimate_profit(data, predictions, initial_capita):
    """
    
    """

    my_formatter = "{0:.2f}"
    num_btc = initial_capita/data.iloc[-1][-2]
    prof_scale = predictions[-1][-1]/data.iloc[-1][-2] - 1
    profit = initial_capita*prof_scale
    
    return my_formatter.format(num_btc), my_formatter.format(profit)