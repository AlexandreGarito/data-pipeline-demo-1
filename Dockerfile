FROM python:3.9.5

LABEL name="sde"
LABEL maintainer="Alexandre Garito"
LABEL description="Docker image for superdataexplorer.com main script"
LABEL version="1.0"

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8050

# If the container runs within GCP :
# - PROJECT_ID is set manually as an environment variable from the GCP Cloud Run service creation.
# - GOOGLE_APPLICATION_CREDENTIALS environment variable is automatically accessed by the Google APIs.
# Uncomment and provide both environment variables below if you run the container outside GCP.

# ENV PROJECT_ID = my-project-id-here
# ENV GOOGLE_APPLICATION_CREDENTIALS = mycredentials

CMD ["sh", "-c", "python --version && python main.py"]