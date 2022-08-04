import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
import scipy.stats
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler


matplotlib.style.use('ggplot')

lbl_encode = LabelEncoder()

df = pd.read_csv("resources/cars.csv", sep=';')
# df[:,0] = labelencoder_X.fit_transform(df[:,0])
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

# df['log_price'] = np.log(df['price'])
df['make_label'] = lbl_encode.fit_transform(df['brand'])
# To count the make:  df['make'].value_counts() and  df['make_label'].value_counts()
df['model_label'] = lbl_encode.fit_transform(df['model'])
df['fuel_type_label'] = lbl_encode.fit_transform(df['fuelType'])
df['transmission_label'] = lbl_encode.fit_transform(df['transmission'])
df = df.dropna()

df_backup = df  # Creating a backup DF to store the original values along with the labels
# Use this only if testing in console
df_backup.to_csv('resources/carsWithLabels.csv', sep=';', index=False)
df = df.drop(columns="make")
df = df.drop(columns="model")
df = df.drop(columns="exterior_color")
df = df.drop(columns="fuel_type")
df = df.drop(columns="transmission")
df = df.drop(columns="body_type")

scaler = StandardScaler()
scaled_df = scaler.fit_transform(df)
scaled_df = pd.DataFrame(scaled_df,
                         columns=['price', 'miles', 'year', 'doors', 'insurance_group', 'engine_size', 'co2_emission',
                                  'make_label', 'model_label', 'exterior_color_label', 'fuel_type_label',
                                  'transmission_label', 'body_type_label'])
# Plotting scaled df
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(6, 5))
ax1.set_title('Before feature Scaling')
sns.kdeplot(df['price'], ax=ax1)
# sns.kdeplot(df['make_label'], ax=ax1)
# sns.kdeplot(df['insurance_group'], ax=ax1)
ax2.set_title('After feature Scaling')
sns.kdeplot(scaled_df['price'], ax=ax2)
# sns.kdeplot(scaled_df['make_label'], ax=ax2)
# sns.kdeplot(scaled_df['insurance_group'], ax=ax2)
# plt.show()

# X = df.iloc[:,:-1].values
# y = df.iloc[:,0].values
# X_train, X_test, y_train, y_test =  train_test_split(X,y,test_size = 0.2, random_state= 0) #fitting multiple regression model to the training set
# regressor = LinearRegression()
# regressor.fit(X_train, y_train)#predicting the test set results
# y_pred = regressor.predict(X_test)
# regressor_OLS = sm.OLS(endog = y_train, exog = X_train).fit()
# regressor_OLS.summary()

# Splitting the data to train/test with MLR
y = df['price']
X = df.loc[:, df.columns != 'price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=0)  # fitting multiple regression model to the training set
regressor = LinearRegression()
regressor.fit(X_train, y_train)  # predicting the test set results
y_pred = regressor.predict(X_test)
regressor_OLS = sm.OLS(endog=y_train, exog=X_train).fit()
# regressor_OLS.summary()

# Splitting the data to train/test with MLR
df['log_price'] = np.log(df['price'])
df = df.drop(columns="price")
y = df['log_price']
X = df.loc[:, df.columns != 'log_price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=0)  # fitting multiple regression model to the training set
regressor = LinearRegression()
regressor.fit(X_train, y_train)  # predicting the test set results
y_pred = regressor.predict(X_test)
regressor_OLS = sm.OLS(endog=y_train, exog=X_train).fit()
regressor_OLS.summary()

X = df[
    ['miles', 'year', 'engine_size', 'make_label', 'model_label', 'body_type_label', 'co2_emission', 'fuel_type_label',
     'transmission_label', 'insurance_group']]
regr = LinearRegression()
regr.fit(X, y)

# Sample of predicting cars' prices manually.
le_name_mapping = dict(zip(df['model_label'], df['model']))
makemapping = dict(zip(df['make_label'], df['make']))
bodymapping = dict(zip(df['body_type_label'], df['body_type']))

predPrice = regr.predict([[110548, 2012, 2.2, 9, 135, 8, 149, 0, 0, 37]])
predPrice = regr.predict([[51292, 2015, 1.5, 14, 80, 4, 136, 2, 1, 4]])
predPrice = regr.predict([[26168, 2011, 1.2, 24, 53, 4, 121, 2, 1, 9]])
predPrice = regr.predict([[86107, 2010, 1.4, 28, 43, 4, 129, 2, 1, 6]])
predPrice = regr.predict([[66488, 2012, 3, 4, 63, 5, 177, 2, 1, 19]])

# A way to predict the price from the front-end considering these parameters must be made.

# Applying log transformation
data = df['price']

data_log = np.log(data)
data_sqrt = np.sqrt(data)

# define grid of plots
fig, axs = plt.subplots(nrows=1, ncols=3)

# create histograms
axs[0].hist(data, edgecolor='black')
axs[1].hist(data_log, edgecolor='black')
axs[2].hist(data_sqrt, edgecolor='black')

# add title to each histogram
axs[0].set_title('Original Data')
axs[1].set_title('Log-Transformed Data')
axs[2].set_title('Square root Transformed Data')

# Feature scaling to standardize distribution
sc_X = StandardScaler()
df_train = sc_X.fit_transform(df_train)
df_test = sc_X.transform(df_test)


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


def parseAttributesToLabels(model, make, body, fuel, exterior_color, transmission):
    data = pd.read_csv("carsWithLabels.csv", sep=';')
    modelMapping = dict(zip(data['model'], data['model_label']))
    makeMapping = dict(zip(data['make'], data['make_label']))
    bodyMapping = dict(zip(data['body'], data['body_type_label']))
    fuelMapping = dict(zip(data['fuel'], data['fuel_type_label']))
    colorMapping = dict(zip(data['exterior_color'], data['exterior_color_label']))
    transMapping = dict(zip(data['transmission'], data['transmission_label']))
    modelLabel = modelMapping[model]
    makeLabel = makeMapping[make]
    bodyLabel = bodyMapping[body]
    fuelLabel = fuelMapping[fuel]
    colorLabel = colorMapping[exterior_color]
    transLabel = transMapping[transmission]
    return modelLabel, makeLabel, bodyLabel, fuelLabel, colorLabel, transLabel


########################### AFTER PRESENTATION ####################################
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
regr = regr.fit(X_train, y_train)
regressor_OLS = sm.OLS(endog=y_train, exog=X_train).fit()
regressor_OLS.summary()



#Getting real and predicted prices


regressor_SVR_rbf = SVR(kernel='rbf')
regressor_SVR_rbf = regressor_SVR_rbf.fit(X_train,y_train)

regressor_SVR_linear = SVR(kernel='linear')
regressor_SVR_linear = regressor_SVR_linear.fit(X_train,y_train)

regressor_SVR_poly = SVR(kernel='poly')
regressor_SVR_poly = regressor_SVR_poly.fit(X_train,y_train)

def getPredictedValues(df, regr):
    predictedValues = []
    for index, row in df.iterrows():
        x = [row["miles"], row["year"], row["doors"], row["insurance_group"],
                 row["engine_size"], row["co2_emission"], row["make_label"], row["model_label"],
                 row["exterior_color_label"], row["fuel_type_label"], row["transmission_label"],
                 row["body_type_label"]]
        prediction = regr.predict([x])
        predictedValues.append(prediction)
   # for i in range(len(df)):
    #    if i != 0:
     #       x = [df.loc[i, "miles"], df.loc[i, "year"], df.loc[i, "doors"], df.loc[i, "insurance_group"],
      #           df.loc[i, "engine_size"], df.loc[i, "co2_emission"], df.loc[i, "make_label"], df.loc[i, "model_label"],
       #          df.loc[i, "exterior_color_label"], df.loc[i, "fuel_type_label"], df.loc[i, "transmission_label"],
        #         df.loc[i, "body_type_label"]]
         #   prediction = regr.predict([x])
          #  predictedValues.append(prediction)
    return predictedValues


realPrices = y_test.to_numpy()
predPrices = getPredictedValues(X_test, regr)
predPricesSVR = getPredictedValues(X_test, regressor_SVR_rbf)
predPricesSVRPoly = getPredictedValues(X_test, regressor_SVR_poly)
predPricesSVRLinear = getPredictedValues(X_test, regressor_SVR_linear)

predValues = []
realValues = []
predValuesSVR = []
predValuesSVRPoly = []
predValuesSVRLinear = []

for x in predPrices:
    predValues.append(x[0])
for x in realPrices:
    realValues.append(x)
for x in predPricesSVR:
    predValuesSVR.append(x[0])
for x in predPricesSVRPoly:
    predValuesSVRPoly.append(x[0])
for x in predPricesSVRLinear:
    predValuesSVRLinear.append(x[0])



def mae(y_true, predictions):
    y_true, predictions = np.array(y_true), np.array(predictions)
    return np.mean(np.abs(y_true - predictions))

A = np.identity(len(regressor_OLS.params))
A = A[1:,:]
print(regressor_OLS.f_test(A))

mae_mlr = mae(realValues, predValues)
mse_mlr = mean_squared_error(realValues, predValues)

mae_svr = mae(realValues, predValuesSVR)
mse_svr = mean_squared_error(realValues, predValuesSVR)

mae_svr_poly = mae(realValues, predValuesSVRPoly)
mse_svr_poly = mean_squared_error(realValues, predValuesSVRPoly)

mae_svr_linear = mae(realValues, predValuesSVRLinear)
mse_svr_linear = mean_squared_error(realValues, predValuesSVRLinear)
