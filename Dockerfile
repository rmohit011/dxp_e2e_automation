FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update

# Install OpenJDK (required for Allure)
RUN apt-get install -y openjdk-11-jre-headless

# Download and install Allure
RUN wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.15.0/allure-commandline-2.15.0.zip
RUN unzip allure-commandline-2.15.0.zip -d /opt/
RUN ln -s /opt/allure-2.15.0/bin/allure /usr/local/bin/allure

# Verify the installation
RUN allure --version

COPY . .
CMD ["sleep", "3600"]
