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
    df = pd.read_csv("carsWithLabels.csv", sep=';')
    df = df.drop(columns="make")
    df = df.drop(columns="model")
    df = df.drop(columns="exterior_color")
    df = df.drop(columns="fuel_type")
    df = df.drop(columns="transmission")
    df = df.drop(columns="body_type")
    df['log_price'] = np.log(df['price'])
    df = df.drop(columns="price")
    y = df['log_price']
    X = df.loc[:, df.columns != 'log_price']
    regr = LinearRegression()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    regr.fit(X_train, y_train)
    return regr


def parseAttributesToLabels(make, model, body, fuel, exterior_color, transmission):
    data = pd.read_csv("carsWithLabels.csv", sep=';')
    makeMapping = dict(zip(data['make'], data['make_label']))
    modelMapping = dict(zip(data['model'], data['model_label']))
    bodyMapping = dict(zip(data['body_type'], data['body_type_label']))
    fuelMapping = dict(zip(data['fuel_type'], data['fuel_type_label']))
    colorMapping = dict(zip(data['exterior_color'], data['exterior_color_label']))
    transMapping = dict(zip(data['transmission'], data['transmission_label']))
    makeLabel = makeMapping[make]
    modelLabel = modelMapping[model]
    bodyLabel = bodyMapping[body]
    fuelLabel = fuelMapping[fuel]
    colorLabel = colorMapping[exterior_color]
    transLabel = transMapping[transmission]
    return makeLabel, modelLabel, bodyLabel, fuelLabel, colorLabel, transLabel

