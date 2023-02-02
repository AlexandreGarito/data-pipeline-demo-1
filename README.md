# Data pipeline demo 1 : micro ETL and web visualization

The project is to create a demonstration micro data pipeline and web visualization dashboard with a little domain name I recently bought : superdataexplorer.com  

<br>

My goal is to showcase junior-level knowledge with the following tools :
- Python ![image]({https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue})

- Airflow
- Jenkins
- Docker
- Google Cloud Platform  

<br>

The pipeline follows these 4 steps :
- Extract data with API calls
- Transform data with pandas
- Load data to a GCP hosted PostgreSQL database (Cloud SQL)
- Generate a visual dashboard with Dash & Plotly

<br>

The app consist of two Docker containers running on GCP (Cloud Run) :
- An Airflow instance scheduling the pipeline python tasks
- A Jenkins CI/CD server used to unit test new commits, build the docker image, and deploy the new container to GCP Cloud Run.

<br>

Other details :
- Secrets (API keys and database credentials) are securely stored and accessed through GCP Secret Manager.
