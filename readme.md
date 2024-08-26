
# Machine Learning Pipeline Project

## Overview
The Machine learning task is to predict if a bank customer would repay a loan or not given a record of customers of the bank and their loan details.
The task itself is supervised since labels have been provided for the data.
The dataset can be download from [kaggle](https://www.kaggle.com/datasets/itssuru/loan-data/data).

## Project Structure
```
ml_pipeline_project/
├── ml_pipeline.py
├── eda.ipynb
├── models
│   ├── trained_model.pkl
├── scripts
│   ├── start_flask_app.sh
│   ├── start_airflow_server.sh
├── output
│   ├── confusion_matrix.txt
│   ├── classification_report.txt
├── data/
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── evaluation.py
│   └── api.py
├── requirements.txt
└── README.md
```

## Requirements
The requirements.txt highlights the packages required if reproduction is necessary.
python version: 3.10.12

## Setup Instructions to reproduce
## Reproducing using the sourcecode from GitHub

### 1. Clone the Repository
```bash
git clone https://github.com/arjunsridharkumaro/complete_ml_pipeline.git
cd complete_ml_pipeline
```

### 2. Set Up the Python Environment
Create a virtual environment and install the dependencies.
```bash
python -m venv ml_pipeline_venv
source ml_pipeline_venv/bin/activate
pip install -r requirements.txt
```
(You can install python 3.10.12 from [here](https://www.python.org/downloads/release/python-31012/).)

### 3. Data Preparation
Download the dataset from Kaggle and put the loan.csv in the data/loan/ directory.

### 4. Run Exploratory Data Analysis (EDA)
Run the EDA scripts. The EDA is performed in a jupyter notebook currently.
```bash
jupyter eda.ipynb
```

### 5. Run the Pipeline Using Apache Airflow
1. Set up Airflow. Create a user. :
   ```bash
   export AIRFLOW_HOME=~/airflow
   airflow db init
   airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
   ```
2. Start the Airflow webserver and scheduler:
   ```bash
   airflow webserver --port 8080
   airflow scheduler
   ```
3. Access the Airflow UI at `http://localhost:8080`. Search trigger the `ml_pipeline` DAG.

### 6. Build and Run the Docker Container (To share the ML model amongst collaborators)
You can containerize the entire project to ensure consistent execution across different environments.
```bash
docker build -t ml_pipeline_project .
docker run -it ml_pipeline_project
```

### 7.  Serve the Model via Flask API

#### 7a. Serve the Model.
To expose the trained model via an API:
```bash
python src/api.py
```
- The API will be available at `http://127.0.0.1:5000`.

#### 7b. Perform Model inference.
- Use a POST request to `/predict` with JSON input to get predictions.
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: applicat ion/json" -d '{"features": [1,debt_consolidation,0.1496,194.02,10.71441777,4,667,3180.041667,3839,76.8,0,0,1]}'
```

![Example GIF](https://github.com/ArjunSridharkumar/complete_ml_pipeline/raw/main/flask_recording.gif)

## Reproducing using the Docker container.

### 1. Pull the container from the docker registry
```bash
docker pull arjunsridhar9720/rbc_assessment:latest
```

### 2. Run the container
```bash
./train_model.sh
```
### 3. Clean up
```bash
./clean_up.sh
```

## AirFlow Pipeline Structure
The pipeline includes the following steps: (the airflow task name is indicated inside the brackets)
1. **Data Ingestion (load_data)**: Load the dataset from the specified source.
2. **Data Preprocessing (preprocess_data)**: Handle missing values, perform feature scaling,
3. **Data Splitting (split_data)**: Split the data into training and testing sets.
3. **Model Training (train_model)**: Train the machine learning model on the preprocessed data.
4. **Model Evaluation (evaluate_model)**: Generate the model evaluation metrics.

## Testing of the pipeline
Each of the individual task can be tested using (no need to start the server and scheduler):
```bash
airflow tasks test ml_pipeline load_data
airflow tasks test ml_pipeline <task_name>
```

## CI/CD Pipeline Proposal
For CI/CD, I have used GitHub Actions to automate:
- **Docker Image CI**: This workflow allows to update the codebase and the docker container as changes are made in the ML pipeline and modelling process.

The GitHub Actions workflow file `.github/workflows/docker-image.yml` contains the steps.

![Example GIF](https://github.com/ArjunSridharkumar/complete_ml_pipeline/raw/main/ci_cd.gif)