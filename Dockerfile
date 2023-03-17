FROM apache/airflow:2.2.3-python3.9

LABEL name="sde"
LABEL maintainer="Alexandre Garito"
LABEL description="Docker image for superdataexplorer.com main dags"
LABEL version="1.0"

WORKDIR /app
COPY . .
COPY dags /opt/airflow/dags

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080
EXPOSE 8050

# If the container runs within GCP :
# - PROJECT_ID is set manually as an environment variable from the GCP Cloud Run service creation.
# - GOOGLE_APPLICATION_CREDENTIALS environment variable is automatically accessed by the Google APIs.
# Uncomment and provide both environment variables below if you run the container outside GCP.

# ENV PROJECT_ID = my-project-id-here
# ENV GOOGLE_APPLICATION_CREDENTIALS = mycredentials

# Start the Airflow webserver and scheduler
# CMD ["sh", "-c", "pytest tests && python --version && echo $PROJECT_ID && ls && airflow webserver -p 8080 && airflow scheduler"]
ENTRYPOINT ["python"]
CMD ["pytest tests && python --version && echo $PROJECT_ID && ls && airflow webserver -p 8080 && airflow scheduler"]
# CMD ["pytest tests; python --version; echo $PROJECT_ID; ls; airflow webserver -p 8080; airflow scheduler"]