import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

lbl_encode = LabelEncoder()
matplotlib.style.use('ggplot')

df = pd.read_csv("resources/cars_regression.csv", sep=';')
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

df['make_label'] = lbl_encode.fit_transform(df['make'])
# To count the make:  df['make'].value_counts() and  df['make_label'].value_counts()
df['model_label'] = lbl_encode.fit_transform(df['model'])
df['exterior_color_label'] = lbl_encode.fit_transform(df['exterior_color'])
df['fuel_type_label'] = lbl_encode.fit_transform(df['fuel_type'])
df['transmission_label'] = lbl_encode.fit_transform(df['transmission'])
df['body_type_label'] = lbl_encode.fit_transform(df['body_type'])

df_backup = df #Creating a backup DF to store the original values along with the labels
# Use this only if testing in console
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
#sns.kdeplot(df['make_label'], ax=ax1)
#sns.kdeplot(df['insurance_group'], ax=ax1)
#ax2.set_title('After feature Scaling')
sns.kdeplot(scaled_df['price'], ax=ax2)
#sns.kdeplot(scaled_df['make_label'], ax=ax2)
#sns.kdeplot(scaled_df['insurance_group'], ax=ax2)
plt.show()

#X = df.iloc[:,:-1].values
#y = df.iloc[:,0].values
#X_train, X_test, y_train, y_test =  train_test_split(X,y,test_size = 0.2, random_state= 0) #fitting multiple regression model to the training set
#regressor = LinearRegression()
#regressor.fit(X_train, y_train)#predicting the test set results
#y_pred = regressor.predict(X_test)
#regressor_OLS = sm.OLS(endog = y_train, exog = X_train).fit()
#regressor_OLS.summary()

# Splitting the data to train/test
y = df['price']
X = df.loc[:, df.columns != 'price']

#Applying log transformation
data = df['price']

data_log = np.log(data)
data_sqrt = np.sqrt(data)

#define grid of plots
fig, axs = plt.subplots(nrows=1, ncols=3)

#create histograms
axs[0].hist(data, edgecolor='black')
axs[1].hist(data_log, edgecolor='black')
axs[2].hist(data_sqrt, edgecolor='black')

#add title to each histogram
axs[0].set_title('Original Data')
axs[1].set_title('Log-Transformed Data')
axs[2].set_title('Square root Transformed Data')


# Feature scaling to standardize distribution
sc_X = StandardScaler()
df_train = sc_X.fit_transform(df_train)
df_test = sc_X.transform(df_test)

print(df.to_markdown())
