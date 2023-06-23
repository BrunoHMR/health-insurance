import pickle
import os
import pandas as pd
import numpy  as np
from flask import Flask, request, Response
from healthinsurance.HealthInsurance import HealthInsurance

path = ''
model = pickle.load(open(path + 'model/health_insurance_model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/healthinsurance/predict', methods=['POST'])
def health_insurance_predict():
    test_json = request.get_json()

    if test_json:
        if isinstance(test_json, dict):
            test_raw = pd.DataFrame(test_json, index=[0])

        else:
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())

        pipeline = HealthInsurance()

        df1 = pipeline.data_cleaning(test_raw)

        df2 = pipeline.data_preparation(df1)

        df_response = pipeline.get_prediction(model, test_raw, df2)

        return df_response

    else:
        return Response('{}', status=200, mimetype='application/json')

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host = '0.0.0.0', port = port, debug = True)