# GCP hosted micro-ETL pipeline and dashboard  

<br>

Dashboard link : https://data-pipeline-demo-1-orqlvqurxq-ew.a.run.app/

Tools & skills in this project :  

✅ Python (API calls, pandas, pytest unit testing, Dash-Plotly, code documentation) 

✅ Docker (managing dependencies and interactions with GCP environment)  

✅ Google Cloud Platform:  
    ✔ Cloud Build (CI/CD from GitHub repo)  
    ✔ Cloud Run (runs Docker containers)  
    ✔ Cloud Composer (Managed Airflow)  
    ✔ Secret Manager (secure access to secrets hosted in GCP)  

<br>

The purpose of this project is to showcase my ability to employ Python in extracting, transforming, loading, and displaying a simple set of API data within an interactive dashboard that updates daily. This serves as a small "A to Z project" in my data engineering journey, where I can gain experience with some tools and challenges involved in the field. This project also involves some DevOps processes and tools such as CI/CD, Docker, and Airflow. Although dashboarding is not a core skill in data engineering, here it serves as an accessory tool that demonstrates the functionality of this pipeline.  

The pipeline is coded in Python. The app is run in a Docker container on Google Cloud Platform (GCP). Data is extracted with API requests, transformed using pandas, loaded into a GCP Cloud SQL PostgreSQL database, and showcased in this dashboard using the Dash-Plotly web framework (based on Flask). With GCP Cloud Build, the code is automatically pulled from the GitHub repo with each new commit, built as a Docker image, and a container is deployed on GCP Cloud Run. At the start of the container, unit tests are run with pytest, then the data extraction scripts are called, then the Dash-Plotly app and web server is called. Every day at 2 AM UTC, a GCP Cloud Composer (managed Airflow) DAG triggers a container reboot to refresh the data.  

Free and easily accessible API data was prioritized to facilitate long-term stability of the pipeline, so it mostly focuses on the biggest companies in the Technology field.  

My original idea was to use the data of those companies by crossing their market capitalization, their number of employees, and their daily current job offerings to give a ranking of these companies when it comes to market cap per employee and market cap per job offer. This would've been a simple approach to find the "best-capitalized job offers" by company. Unfortunately, I realized that daily job offering data is quite tricky to obtain, often paid and often incomplete. So, I decided to replace it with Twitter social media sentiment, a data source simple to obtain and also updated daily. As a result, the dashboard would display the "best-capitalized workforce" for each company, along with their social media sentiment. Since the Twitter API ceased to be freely accessible in February 2023, the API I used ceased to provide it, and I had to switch to Reddit social sentiment, which is unfortunately more scarce than Twitter sentiment, but it's still the best option I have for now without having to redesign the entire social sentiment part of the pipeline.  

As of March 2023, this dashboard primarily serves as a small working technical demo; however, I am committed to update and enhance the dashboard with more valuable data as I advance in my data engineering journey.
