import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
lbl_encode = LabelEncoder()
le = LabelEncoder()
from sklearn.model_selection import train_test_split


df = pd.read_csv("resources/cars_regression.csv", sep = ';')
#df[:,0] = labelencoder_X.fit_transform(df[:,0])
df = df.drop(columns="photo_links")
df = df.drop(columns="city")
df = df.drop(columns="zip")
df = df.drop(columns="country")
df = df.drop(columns="user_id")
df = df.drop(columns="seller_name")
df = df.drop(columns="street")
df = df.drop(columns="photo_url")
df = df.drop(columns="features")
df = df.drop(columns="miles_indicator")
df = df.drop(columns="vdp_url")

df['make_label'] = lbl_encode.fit_transform(df['make'])
#To count the make:  df['make'].value_counts() and  df['make_label'].value_counts()
df['model_label'] = lbl_encode.fit_transform(df['model'])
df['exterior_color_label'] = lbl_encode.fit_transform(df['exterior_color'])
df['fuel_type_label'] = lbl_encode.fit_transform(df['fuel_type'])
df['transmission_label'] = lbl_encode.fit_transform(df['transmission'])
df['body_type_label'] = lbl_encode.fit_transform(df['body_type'])

#Splitting the data to train/test
df_train, df_test =  train_test_split(df,test_size = 0.2, random_state= 0)

#Feature scaling to standardize distribution
sc_X = StandardScaler()
df_train = sc_X.fit_transform(df_train)
df_test = sc_X.transform(df_test)

print(df.to_markdown())
