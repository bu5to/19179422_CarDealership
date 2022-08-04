import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
import scipy.stats
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import scale
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error

df = pd.read_csv("resources/cars.csv", sep=';')

lbl_encode = LabelEncoder()
sc = StandardScaler()

# df['log_price'] = np.log(df['price'])
df['make_label'] = lbl_encode.fit_transform(df['brand'])
# To count the make:  df['make'].value_counts() and  df['make_label'].value_counts()
df['model_label'] = lbl_encode.fit_transform(df['model'])
df['fuel_type_label'] = lbl_encode.fit_transform(df['fuelType'])
df['transmission_label'] = lbl_encode.fit_transform(df['transmission'])
df = df.dropna()


#df_sample = df.sample(n = 15)
#df_sample.to_csv("sampledata.csv", index=False)

#df_sample = df_sample.drop(columns="brand")
#df_sample = df_sample.drop(columns="model")
#df_sample = df_sample.drop(columns="fuelType")
#df_sample = df_sample.drop(columns="transmission")
#df_sample['log_price'] = np.log(df_sample['price'])
#df_sample = df_sample.drop(columns="price")
#y_sample = df_sample['log_price']
#X_sample = df_sample.loc[:, df_sample.columns != 'log_price']

df = df.drop(columns="brand")
df = df.drop(columns="model")
df = df.drop(columns="fuelType")
df = df.drop(columns="transmission")
df['log_price'] = np.log(df['price'])
df = df.drop(columns="price")

y = df['log_price']
X = df.loc[:, df.columns != 'log_price']
regr = LinearRegression()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

#Run principal component analysis to see the RMSE values depending on the different factors.

X_train_scaled = scale(X_train)
X_test_scaled = scale(X_test)

for i in range(1, X_train_pc.shape[1]+1):
    rmse_score = -1 * cross_val_score(lin_reg,
                                      X_train_pc[:,:i], # Use first k principal components
                                      y_train,
                                      cv=cv,
                                      scoring='neg_root_mean_squared_error').mean()
    rmse_list.append(rmse_score)

plt.plot(rmse_list, '-o')
plt.xlabel('Number of principal components in regression')
plt.ylabel('RMSE')
plt.title('Quality')
plt.xlim(xmin=-1)
plt.xticks(np.arange(X_train_pc.shape[1]), np.arange(1, X_train_pc.shape[1]+1))
plt.axhline(y=lr_score_train, color='g', linestyle='-')

plt.show()

scaled_data = preprocessing.scale(df.T)
pca = PCA()
pca.fit(scaled_data)
pca_data = pca.transform(scaled_data)
per_var = np.round(pca.explained_variance_ratio_ * 100, decimals=1)
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]

#plt.bar(x=range(1,len(per_var)+1), height = per_var, tick_label = labels)
#plt.ylabel('Percentage of explained variance')
#plt.xlabel('Principal Component')
#plt.show()

indexes = list(df.columns)

pca_df = pd.DataFrame(pca_data, index=indexes, columns=labels)
plt.title('Feature importance according to the PCA analysis')
plt.xlabel('PC1 - {0}%'.format(per_var[0]))
plt.ylabel('PC2 - {0}%'.format(per_var[1]))
for sample in pca_df.index:
    plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))
plt.show()


best_pc_num = 8

# Train model with first 9 principal components
lin_reg_pc = LinearRegression().fit(X_train_pc[:,:best_pc_num], y_train)

# Get cross-validation RMSE (train set)
pcr_score_train = -1 * cross_val_score(lin_reg_pc,
                                       X_train_pc[:,:best_pc_num],
                                       y_train,
                                       cv=cv,
                                       scoring='neg_root_mean_squared_error').mean()

# Train model on training set
lin_reg_pc = LinearRegression().fit(X_train_pc[:,:best_pc_num], y_train)

# Get first 9 principal components of test set
X_test_pc = pca.transform(X_test_scaled)[:,:best_pc_num]

# Predict on test data
preds = lin_reg_pc.predict(X_test_pc)
pcr_score_test = mean_squared_error(y_test, preds, squared=False)



X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
regr = regr.fit(X_train, y_train)
regressor_OLS = sm.OLS(endog=y_train, exog=X_train).fit()
#with open("largedatasummary.txt", "a") as o:
 #   o.write(str(regressor_OLS.summary()))

from sklearn.decomposition import PCA


regressor_SVR_rbf = SVR(kernel='rbf')
regressor_SVR_rbf = regressor_SVR_rbf.fit(X_train,y_train)



regressor_SVR_poly = SVR(kernel='poly')
regressor_SVR_poly = regressor_SVR_poly.fit(X_train,y_train)


regressor_SVR_linear = SVR(kernel='linear')
regressor_SVR_linear = regressor_SVR_linear.fit(X_train,y_train)

def getPredictedValues(df, regr):
    predictedValues = []
    for index, row in df.iterrows():
        x = [row["year"], row["mileage"], row["tax"], row["engineSize"],
                 row["co2_emissions"], row["make_label"], row["model_label"], row["fuel_type_label"], row["transmission_label"]]
        prediction = regr.predict([x])
        predictedValues.append(prediction)
    return predictedValues


realPrices = y_sample.to_numpy()
predPrices = getPredictedValues(X_sample, regr)
predPricesSVR = getPredictedValues(X_sample, regressor_SVR_rbf)
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
with open("largedatasummary.txt", "a") as o:
    o.write(regressor_OLS.f_test(A))
print(regressor_OLS.f_test(A))

mae_mlr = mae(realValues, predValues)
mse_mlr = mean_squared_error(realValues, predValues)

mae_svr = mae(realValues, predValuesSVR)
mse_svr = mean_squared_error(realValues, predValuesSVR)

mae_svr_poly = mae(realValues, predValuesSVRPoly)
mse_svr_poly = mean_squared_error(realValues, predValuesSVRPoly)

mae_svr_linear = mae(realValues, predValuesSVRLinear)
mse_svr_linear = mean_squared_error(realValues, predValuesSVRLinear)