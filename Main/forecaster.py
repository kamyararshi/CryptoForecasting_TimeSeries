import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
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
    
    # MinMaxScaling
    scaler = MinMaxScaler()
    dataf = data.drop("time", axis=1).to_numpy()
    datas = scaler.fit_transform(dataf)

    # Creating sequences of 60 instances
    X = [] 
    Y = []
    for i in range(60, data.shape[0]):

        X.append(datas[i-60:i])
        Y.append(datas[i])
    
    return np.array(X), np.array(Y), scaler, data


path_model = "Multivariate_LSTM_4out.h5"
def forecast(path_model=path_model, path_data=path):
    """
    
    """
    model = tf.keras.models.load_model(path_model)
    X, _, scaler, _ = prepare_data(path=path_data)
    
    predictions = model.predict(X)/scaler.scale_
    
    return predictions