# CryptoForecasting_TimeSeries

# 1. Web scrapping 

### Source 1: Bitinfocharts 
It provides following 17 raw features. The features were retrieved using a custom python script.

**i) Number of transactions in blockchain per day**


**ii) Average block size (KB)**

**iii) Number of sent by addresses**
These are distinct addresses from which payments are made every day.

**iv) Number of active addresses**
number of unique addresses taking part in a transaction by either sending or receiving Bitcoins.

**v) Average mining difficulty (Hash/day)**
A higher difficulty means that it will take more computing power to mine the same number of blocks, making the network more secure against attacks.

**vi) Average hash rate (hash/s)**
Hash rate is a measure of the mining computational power per second used.

**Vii) Mining Profitability (USD)**
It is mining profitability for 1 Hash/s

**Viii) Sent coins (USD)**
It is the total value of Bitcoins sent daily.

**ix) Average & Median transaction fee (USD)**
Each transaction can have a transaction fee determined by the sender and paid to miners who verify the transaction. 

**x) Average block time (minutes)**
Block time is the time required to create the next block in a chain. It is a time taken by a blockchain miner to find a solution to the hash. Usually, it is around 10 minutes, but can fluctuate depending on the hash rate of the network.

**xi) Average & Median Transaction Value (USD)**
The average & median value of the transactions in Bitcoin

**xii) Tweets & Google Trends to “Bitcoin” per day**
Number of tweets & google trends. These features represent impact of social media on bitcoin price.

**xiii) Average Fee Percentage in Total Block Reward**
Bitcoin block rewards are new bitcoins awarded to miners for being the first to solve a complex math problem and creating a new block of verified bitcoin transactions. 

**xiv) Top 100 Richest Addresses to Total coins**
This is the ratio between top 100 rich addresses to total coins.


## Source 2: Using Quandl
Following Two Features were collected using Quandl API

**i) Miner Revenue (USD)**
Total value of coin base block rewards and transaction fees paid to miners.
**ii) Number of coins in circulation**
It is a total number of mined bitcoins that are currently circulating on the network. The total supply of BTC is limited to 21 million.

## Source 3: Using investpy
The OHLC features & target variable is mined using investpy API, which retrieves data from investing.com. Values of the previous day are used to predict next day closing price.

**i) Opening Price**

**ii) Highest Price**

**iii) Lowest Price**

**iv) Closing Price**

# Scaling

For scaling the features, robust scalar followed by min-max scalar was used. Robust scalar uses the interquartile range, so that it is robust to outliers. Kepp in mind, only fetures will be scaled, but not Target variable.

# Feature selection

feature selection had to be performed to select top important features. Random forest regressor was used to select the top 10 important features.

# Training Methodology

We decided to train model for various sliding windows. Train on 500 data points and test on next 100 data points using Bidirectional-LSTM. MAPE, MAE and RMSE as our evaluation metrics. With this approach, we can train 26 models for amount of data we have scrapped. Each will be capable of predicting Bitcoin closing price of next 1 day (for next 100 days) with lowest MAPE possible. 

## Model:
Model has 2 hidden BiLSTM layers of 400 and 500 neurons each, and a dense layer with single neuron to predict Closing price of next 1 day.

# Results

Using Bi-LSTM:
    
MAE Train: 160.76

RMSE Train: 279.93

MAE Test: 414.51

RMSE Test: 561.76

MAPE: 0.03

Please note that, except MAPE all other metrics are avearge of particular metric values on all models.
While MAPE indicates, last 100 days prediction's Mean Absolute Percentage Error. 
