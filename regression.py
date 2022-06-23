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
    df = df.drop(columns="photo_links")
    df = df.drop(columns="city")
    df = df.drop(columns="zip")
    df = df.drop(columns="country")
    df = df.drop(columns="user_id")
    df = df.drop(columns="seller_name")
    df = df.drop(columns="currency_indicator")
    df = df.drop(columns="heading")
    df = df.drop(columns="id")
    df = df.drop(columns="street")
    df = df.drop(columns="photo_url")
    df = df.drop(columns="features")
    df = df.drop(columns="miles_indicator")
    df = df.drop(columns="vdp_url")
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
    regr.fit(X, y)
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

