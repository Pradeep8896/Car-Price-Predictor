import numpy as np
import pandas as pd

import streamlit as st
import pickle

pipe=pickle.load(open('pipe.pkl','rb'))
final_df=pickle.load(open('clean_df.pkl','rb'))



def price_predictor(km_driven, fuel, mileage, car_name, transmission, used_year):
  temp_dict={'km_driven':km_driven,'fuel':fuel,'seller_type':'Individual',
            'transmission':transmission,'owner':'First Owner',
            'mileage':mileage,
            'seats':4,'car_name':car_name,'used_year':used_year,'engine_cc':1500,
            'max_power_bhp':100,'torque_upd':180}
  df=pd.DataFrame(temp_dict, index=[0])
  price= pipe.predict(df)[0][0]
  if price<0:
    return 'Not Available'
  else:
    return f'Price : {round(price,2)} INR'

st.header('Car Price Predictor CAR DEKHO')

year=final_df[['used_year']]
year['Year']=2022-year['used_year']
year=year.sort_values('Year', ascending=False)

car_name=st.selectbox('Car Name',(final_df['car_name'].unique()))

col1, col2, col3 = st.columns(3)

with col1:
  km_driven=st.number_input('Kilometer')
with col2:
  fuel=st.selectbox('Fuel type',(final_df['fuel'].unique()))
with col3:
  mileage=st.number_input('Mielage')

col1,col2 = st.columns(2)
with col1:

  transmission=st.selectbox('Transmission Type',(final_df['transmission'].unique()))
with col2:
  used_year=st.selectbox('Year of Purchase',(year['Year'].unique()))

def year_fin(text):
  used_year=2022-text
  return used_year

if st.button('Predict Price'):
  st.header(price_predictor(km_driven, fuel, mileage, car_name, transmission, year_fin(used_year)))
