import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def carsModel():
    '''
    Creates the linear regression model, applies logarithmic transformation and fits it.
    :return: The fitted linear regression model.
    '''
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
    '''
    Searches the attributes through the CSV files and converts it to the labels that represents
    the attributes passed.
    :param make: The make of the car.
    :param model: The model of the car.
    :param fuel: The fuel type of the car.
    :param transmission: The transmission of the car.
    :return: The list of labels that will be used to make predictions in the car price prediction model.
    '''
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
