FROM python:3.9.5

LABEL name="sde"
LABEL maintainer="Alexandre Garito"
LABEL description="Docker image for superdataexplorer.com main script"
LABEL version="1.0"

WORKDIR /app
COPY . .



# FONTS

# Install required packages for downloading fonts
RUN apt-get update && \
    apt-get install -y wget unzip fontconfig

# Create directories for the fonts
RUN mkdir -p /usr/share/fonts/truetype/lato && \
    mkdir -p /usr/share/fonts/truetype/roboto && \
    mkdir -p /usr/share/fonts/opentype/league-spartan

# Download and install Lato font files
RUN wget https://fonts.google.com/download?family=Lato -O lato.zip && \
    unzip lato.zip -d /usr/share/fonts/truetype/lato/ && \
    rm lato.zip

# Download and install Roboto font files
RUN wget https://fonts.google.com/download?family=Roboto -O roboto.zip && \
    unzip roboto.zip -d /usr/share/fonts/truetype/roboto/ && \
    rm roboto.zip

# Download and install League Spartan font files
RUN wget https://github.com/theleagueof/league-spartan/raw/master/LeagueSpartan-Bold.otf -O /usr/share/fonts/opentype/league-spartan/LeagueSpartan-Bold.otf

# Update font cache
RUN fc-cache -f -v

# Clean up
RUN apt-get remove -y wget unzip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*



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