# src/api.py

from flask import Flask, request, jsonify
import pickle
import pandas as pd
from data_processing import load_data, preprocess_data
with open('/opt/airflow/dags/models/trained_model.pkl', 'rb') as file:
# with open('trained_model.pkl', 'rb') as file:
    model = pickle.load(file)


app = Flask(__name__)

# # Load and preprocess data
# df = load_data('../data/creditcard.csv')
# X_train, X_test, y_train, y_test = preprocess_data(df)

# # Train model
# model = train_model(X_train, y_train)

@app.route('/predict', methods=['POST'])
def predict():
    # data = request.get_json(force=True)
    # prediction = model.predict([data['features']])
    # return jsonify({'prediction': prediction.tolist()})


    X = None
    data = request.get_json(force=True)
    data_list = data['features']
    if len(data_list) != 13:
        print ("Amount of features are not equal to 12. Some features are missing or extra")
        return None
    columns_list=['credit.policy','purpose','int.rate','installment','log.annual.inc','dti','fico','days.with.cr.line','revol.bal','revol.util',
                  'inq.last.6mths','delinq.2yrs','pub.rec']
    df = pd.DataFrame([data_list], columns=columns_list)
    try:
        X = preprocess_data(df)
    # X =
    except Exception as e:
        print ("exception occured at preprocess_data due to ", e)
    X.reset_index(drop = True, inplace = True)
    try:
        prediction = model.predict([X.iloc[0].tolist()])
    except Exception as e:
        print ("error at", e)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(port=5000,debug=True)