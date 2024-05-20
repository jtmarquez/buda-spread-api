# Base image
FROM python:3

# set work directory
WORKDIR /

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY [ "requirements.txt", "run.sh", "./"]
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt && chmod +x ./run.sh

# copy project
COPY . .

# Give setup script permissions
RUN chmod +x ./initial_setup.sh

# Execute script permissions
RUN ./initial_setup.sh

# Set entrypoint
ENTRYPOINT bash ./run.sh
