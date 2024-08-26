
# Use a standard Linux distribution as the base image
FROM ubuntu:22.04

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHON_VERSION=3.9

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    libpq-dev \
    curl \
    git \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    locales \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create Airflow directories
RUN mkdir -p $AIRFLOW_HOME/dags $AIRFLOW_HOME/logs $AIRFLOW_HOME/plugins $AIRFLOW_HOME/dags/src $AIRFLOW_HOME/dags/data

# Install Airflow and its dependencies
RUN pip3 install --no-cache-dir apache-airflow flask pendulum pyarrow pydantic flask-session pandas scikit-learn

# Copy DAGs, source code, and data
COPY ./mlpipeline.py $AIRFLOW_HOME/dags/mlpipeline.py
COPY ./src/ $AIRFLOW_HOME/dags/src/
COPY ./data/loan/ $AIRFLOW_HOME/dags/data/loan/

# Copy and install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

# Copy shell files and change permissions
COPY ./shell_files/ $AIRFLOW_HOME/shell_files/
RUN chmod +x $AIRFLOW_HOME/shell_files/*.sh

# Initialize Airflow database
RUN $AIRFLOW_HOME/shell_files/run_airflow_db_init.sh

# Set the entrypoint to start Airflow services
ENTRYPOINT ["/opt/airflow/shell_files/entrypoint.sh"]

# Expose ports for webserver, scheduler, and flower
EXPOSE 8080 8793 5000
