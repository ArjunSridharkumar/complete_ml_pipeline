# src/model_training.py
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from src.data_processing import load_data, preprocess_data

def train_model(X_train, y_train):
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    if not os.path.exists("/opt/airflow/dags/models"):
        os.mkdir("/opt/airflow/dags/models")
    with open("/opt/airflow/dags/models/trained_model.pkl","wb") as f:
        pickle.dump(model,f)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    # print("Confusion Matrix:")
    # print(confusion_matrix(y_test, y_pred))
    cm = confusion_matrix(y_test, y_pred)
    # print("Classification Report:")
    # print(classification_report(y_test, y_pred))
    cr = classification_report(y_test, y_pred)
    # Save confusion matrix to a file
    with open('/opt/airflow/dags/confusion_matrix.txt', 'w') as f:
        f.write("Confusion Matrix:\n")
        f.write(str(cm) + '\n')

    # Save classification report to a file
    with open('/opt/airflow/dags/classification_report.txt', 'w') as f:
        f.write("Classification Report:\n")
        f.write(cr + '\n')

if __name__ == "__main__":
    filepath = '../data/creditcard.csv'
    df = load_data(filepath)
    X_train, X_test, y_train, y_test = preprocess_data(df)

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    print("Model training and evaluation complete!")