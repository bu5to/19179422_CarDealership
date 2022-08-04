import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
matplotlib.style.use('ggplot')

def carsModel():
    df = pd.read_csv("resources/carsWithLabels.csv", sep=';')
    df = df.drop(columns="make")
    df = df.drop(columns="model")
    df = df.drop(columns="fuelType")
    df = df.drop(columns="transmission")
    df['log_price'] = np.log(df['price'])
    df = df.drop(columns="price")
    y = df['log_price']
    X = df.loc[:, df.columns != 'log_price']
    regr = LinearRegression()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    regr.fit(X_train, y_train)
    return regr


def parseAttributesToLabels(make, model, fuel, transmission):
    data = pd.read_csv("resources/carsWithLabels.csv", sep=';')
    makeMapping = dict(zip(data['make'], data['make_label']))
    modelMapping = dict(zip(data['model'], data['model_label']))
    fuelMapping = dict(zip(data['fuelType'], data['fuel_type_label']))
    transMapping = dict(zip(data['transmission'], data['transmission_label']))
    makeLabel = makeMapping[make]
    print(makeLabel)
    modelLabel = modelMapping[model]
    print(modelLabel)
    fuelLabel = fuelMapping[fuel]
    transLabel = transMapping[transmission]
    return makeLabel, modelLabel, fuelLabel, transLabel

