# Use the official Python base image
FROM python:3.13.1


#Update the package lists
RUN apt-get update

COPY . /postgres_python



# Set the working directory in the container
WORKDIR /postgres_python

RUN pip install --no-cache-dir -r requirements.txt

# Start an interactive shell
CMD ["python", "main.py", "data\postcodesgeo.csv"]