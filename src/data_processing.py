# src/data_preprocessing.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

def preprocess_data(df):
    #There are no none values in the dataset. Checked in the preprocessing notebook.
    #If nan values in inference then we should return None
    if df.isnull().values.any():
        print("Columns with missing values:")
        return None
    #retrieve only the numerical features
    columns_to_drop = ['credit.policy', 'purpose', 'not.fully.paid', 'delinq.2yrs', 'inq.last.6mths', 'pub.rec']
    if 'not.fully.paid' not in df.columns.tolist():
        columns_to_drop.remove('not.fully.paid')
    X = df.drop(columns_to_drop, axis=1)
    if 'not.fully.paid' in df.columns.tolist():
        y = df['not.fully.paid']
        return X, y
    else:
        return X

    # print (df.columns.tolist())
    # print ("preprocess_data")
    # y = df['not.fully.paid']
    # return X,y
def split_train_test_data(X,y):
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    # X_train = X_train.to_list()
    # X_test = X_test.to_list()
    # import pdb;pdb.set_trace()
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    filepath = './../output_of_load_data_task.csv'
    df = load_data(filepath)
    X_train, X_test, y_train, y_test = preprocess_data(df)
    print("Data preprocessing complete!")