FROM python:3.9.5

LABEL name="sde"
LABEL maintainer="Alexandre Garito"
LABEL description="Docker image data-pipeline-demo-1 main script"
LABEL version="1.0"

WORKDIR /app
COPY . .

RUN apt-get update; apt-get install -y fontconfig

# Installing fonts
RUN mkdir -p /usr/share/fonts/truetype/
RUN install -m644 fonts/Lato.ttf /usr/share/fonts/truetype/
RUN install -m644 fonts/Roboto.ttf /usr/share/fonts/truetype/

# Update font cache
RUN fc-cache -f -v

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8050

# If the container runs within GCP :
# - PROJECT_ID is set manually as an environment variable from the GCP Cloud Run service creation.
# - GOOGLE_APPLICATION_CREDENTIALS environment variable is automatically accessed by the Google APIs.
# Uncomment and provide both environment variables below if you run the container outside GCP.

# ENV PROJECT_ID = my-project-id-here
# ENV GOOGLE_APPLICATION_CREDENTIALS = mycredentials

CMD ["sh", "-c", "pytest tests && python --version && echo $PROJECT_ID &&  ls && python main.py"]