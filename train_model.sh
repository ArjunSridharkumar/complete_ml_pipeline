#Steps to be executed

#Pull the docker image
docker pull arjunsridhar9720/rbc_assessment:latest

#Run the airflow server and webserc
docker run -d -p 8080:8080 -p 5000:5000 --name ml_pipeline_container arjunsridhar9720/rbc_assessment:latest
docker exec ml_pipeline_container bash /opt/airflow/dags/scripts/start_airflow_server.sh

#Run