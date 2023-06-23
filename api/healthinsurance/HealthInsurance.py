import pickle
import inflection
import numpy  as np
import pandas as pd

class HealthInsurance():
    
    def __init__(self):
        self.home_path = ''
        self.annual_premium = pickle.load(open(self.home_path + 'parameter/annual_premium.pkl', 'rb'))
        self.age = pickle.load(open(self.home_path + 'parameter/age.pkl', 'rb'))
        self.vintage = pickle.load(open(self.home_path + 'parameter/vintage.pkl', 'rb'))
        self.region_code = pickle.load(open(self.home_path + 'parameter/region_code.pkl', 'rb'))
        self.policy_sales_channel = pickle.load(open(self.home_path + 'parameter/policy_sales_channel.pkl', 'rb'))
        
    def data_cleaning(self, df1):
        cols_old = ['id', 'Gender', 'Age', 'Driving_License', 'Region_Code',
       'Previously_Insured', 'Vehicle_Age', 'Vehicle_Damage', 'Annual_Premium',
       'Policy_Sales_Channel', 'Vintage']
        
        # renomeando colunas
        snakecase = lambda x: inflection.underscore(x)
        cols_new = list(map(snakecase, cols_old))
        df1.columns = cols_new
        
        # alterando dados float64 para diminuir o tamanho do dataset
        df1['region_code'] = df1['region_code'].astype('int64')
        df1['policy_sales_channel'] = df1['policy_sales_channel'].astype('int64')
        df1['annual_premium'] = df1['annual_premium'].astype('float32')

        # transformando atributos categóricos em numéricos
        df1['gender'] = df1['gender'].apply(lambda x: 0 if x == 'Female' else 1)
        df1['vehicle_damage'] = df1['vehicle_damage'].apply(lambda x: 0 if x == 'No' else 1)
        df1['vehicle_age'] = df1['vehicle_age'].apply(lambda x: 1 if (x == '< 1 Year') else 
                                                      2 if (x == '1-2 Year') else 
                                                      3 if (x == '> 2 Years') else x)
        
        return df1
        
    def data_preparation(self, df2):
        df2['annual_premium'] = self.annual_premium.fit_transform(df2[['annual_premium']].values)
        df2['age'] = self.age.fit_transform(df2[['age']].values)
        df2['vintage'] = self.vintage.fit_transform(df2[['vintage']].values)
        df2.loc[:,'region_code'] = df2['region_code'].map(self.region_code)
        df2.loc[:,'policy_sales_channel'] = df2['policy_sales_channel'].map(self.policy_sales_channel)
        # para caso algum 'policy_sales_channel' ou 'region_code' não aparça na validação, preencher com 0
        df2 = df2.fillna(0)
        cols_selected_mdi = ['vintage', 'annual_premium', 'age', 'region_code', 'vehicle_damage', 'policy_sales_channel', 'previously_insured']
        df2 = df2[cols_selected_mdi]
        
        return df2

    def get_prediction(self, xgb_final, df_original, df_prep):
        predicao = xgb_final.predict_proba(df_prep)
        df_original['score'] = predicao[:,1].tolist()
        
        return df_original.to_json(orient='records')