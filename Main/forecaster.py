import numpy as np
import matplotlib.dates as mpl_dates
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import tensorflow as tf

#assert tf.version.VERSION > 2.3.1 , print("Upgrade tensorflow")

path = "finadata.csv"

def prepare_data(path):
    """
    Reads and prepares the dataset for prediction
    and plotting
    
    """
    assert type(path)==type(''), print("path is not string")

    # Loading Data
    data = pd.read_csv(path)
    #Prepare Data
    X = data.drop(['Date', 'next_day_closing_price'], axis=1).to_numpy().reshape(len(data), 1, 10)
    #Labels for evaluation
    Y = data['next_day_closing_price'].to_numpy().reshape(-1,1)

    return X, Y, data


path_model = "bilstmnew.h5"
def forecast(X, path_model=path_model):
    """
    Predicting using model .h5 file and prepared data
    
    """
    model = tf.keras.models.load_model(path_model)
    
    predictions = model.predict(X).reshape(-1,1)
    
    return predictions


def estimate_profit(data, predictions, initial_capita):
    """
    Estimates the profit given initial capita at today's 
    open price and
    according to predicted closed price of next day
    """

    num_btc = initial_capita/data.iloc[:,-1].iloc[-1]
    prof_scale = predictions[-1]/data.iloc[:,-1].iloc[-1] - 1
    profit = initial_capita*prof_scale
    
    return round(num_btc, 6), round(profit[-1], 2)


def update():
    """
    Simiulates how data update works in the UI
    ONLY FOR THE DEMO
    """
    ad1 = r"E:\Books and PDF\ICE Master's\Data Science 2\Project\Main\Data\finaldata.csv"
    ad2 = r"E:\Books and PDF\ICE Master's\Data Science 2\Project\Main\Data\finaldata_rescaled.csv"
    df2c = pd.read_csv(ad2).drop('Unnamed: 0',axis=1)
    #df_c = pd.concat([df1c,df2c], axis=0)
    df2c.to_csv(ad1, columns=df2c.columns, index=False)