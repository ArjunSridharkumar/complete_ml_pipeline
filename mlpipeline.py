# dags/ml_pipeline_dag.py

# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from airflow import DAG
# from importmonkey import add_path
import pandas as pd
from airflow.models import Variable
import os
import sys
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# DAGBAGS_DIR = Variable.get('DAGBAGS_DIR')
# sys.path.append(DAGBAGS_DIR + '/src/')


# from src.data_preprocessing import load_data, preprocess_data
from src.data_processing import load_data, preprocess_data,split_train_test_data
from src.model_training import train_model, evaluate_model
# from src.model_training import train_model, evaluate_model

# add_path("~/src")
# from data_processing import load_data,preprocess_data
# from model_training import train_model, evaluate_model


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'ml_pipeline',
    default_args=default_args,
    description='A simple ML pipeline',
    schedule_interval=None,
)

def load_data_task():
    filepath = '/opt/airflow/dags/data/loan/loan.csv'
    # print ("files",os.listdir(filepath))
    df = load_data(filepath)
    print ('df')
    print ('================================')
    print (df)
    # df.to_csv("output_of_load_data_task.csv")
    return df

def preprocess_data_task(**kwargs):
    ti = kwargs['ti']
    # print (ti)
    df = ti.xcom_pull(task_ids='load_data')
    X,y = preprocess_data(df)
    return X,y
    # print (os.listdir())
    # df = pd.read_csv("output_of_load_data_task.csv")
    # print (df)
def split_data_task(**kwargs):
    ti = kwargs['ti']
    X,y = ti.xcom_pull(task_ids="preprocess_data")
    X_train, X_test, y_train, y_test = split_train_test_data(X,y)
    # X_train = list(X_train)
    # X_test = list(X_test)
    print ('X_train ,X_test')
    print ('================================')
    # print (X_train,X_test)
    # X_train.to_csv("X_train.csv")
    # X_test.to_csv("X_test.csv")
    # y_train.to_csv("y_train.csv")
    # y_test.to_csv("y_test.csv")
    print (X_train.shape)
    print (X_test.shape)
    print (y_train.shape)
    print (y_test.shape)
    return X_train, X_test, y_train, y_test

def train_model_task(**kwargs):
    ti = kwargs['ti']
    # X_train, X_test, y_train, y_test = preprocess_data_task()

    X_train, X_test, y_train, y_test = ti.xcom_pull(task_ids='split_data')
    # # return_list =  ti.xcom_pull(task_ids='preprocess_data')
    # X_train = return_list[0]
    # X_test = return_list[1]
    # y_train = return_list[2]
    # y_test = return_list[3]
    # X_train = pd.read_csv("./../X_train.csv")
    # X_test = pd.read_csv("./../X_X_testtrain.csv")
    # y_train = pd.read_csv("./../y_train.csv")
    # y_test = pd.read_csv("./../y_test.csv")
    # print (type(X_train))
    # X_train =
    model = train_model(X_train, y_train)
    # print (type(model))
    return model

def evaluate_model_task(**kwargs):
    ti = kwargs['ti']
    model = ti.xcom_pull(task_ids='train_model')
    # model,X_test,y_test = train_model_task()
    X_train, X_test, y_train, y_test = ti.xcom_pull(task_ids='split_data')
    evaluate_model(model, X_test, y_test)

load_data_op = PythonOperator(
    task_id='load_data',
    python_callable=load_data_task,
    dag=dag,
)


preprocess_data_op = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data_task,
    dag=dag,
)

split_data_op = PythonOperator(
    task_id='split_data',
    python_callable=split_data_task,
    dag=dag,
)

train_model_op = PythonOperator(
    task_id='train_model',
    python_callable=train_model_task,
    dag=dag,
)

evaluate_model_op = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model_task,
    dag=dag,
)

load_data_op >> preprocess_data_op >> split_data_op >> train_model_op >> evaluate_model_op