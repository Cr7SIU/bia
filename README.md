# BIA Project

This project is designed to automate the extraction of geospatial data from CSV files, process and clean the data using Python's Pandas library, made a requests into the Postcodes.io API to enrich the dataset with UK postcode information and load the dataframe into a PostgreSQL database, facilitating the generation of comprehensive reports that provide valuable insights..

## Project Structure

- **data/**: Contains the data files used in the project.
- **geo_requests/**: Module that handles geographic requests to the API and loads data into the database.
- **.gitignore**: Specifies files and directories that Git should ignore.
- **Dockerfile**: Script to build the Docker image of the application.
- **LICENSE**: Project's license file.
- **README.md**: This file, providing an overview of the project.
- **docker-compose.yaml**: Configuration file for Docker Compose.
- **init.sql**: SQL script to initialize the PostgreSQL database.
- **main.py**: Main application script.
- **requirements.txt**: List of Python dependencies required for the project.

## Prerequisites

- **Docker**: Ensure Docker is installed on your system. You can download it from [Docker's official website](https://www.docker.com/).
- **Docker Compose**: You'll also need Docker Compose, which typically comes bundled with Docker Desktop.

## Installation and Execution

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Cr7SIU/bia.git
   cd bia
