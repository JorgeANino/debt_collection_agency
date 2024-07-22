# Debt Collection Agency

## Overview

This project is a Django-based web application that allows a collection agency to manage accounts, clients, and consumers. The application provides APIs to ingest data from CSV files and retrieve account information with various filters.

## Prerequisites

- Docker
- Docker Compose
- Git

## Setup Instructions

### Clone the Repository

Clone the repository to your local machine using the following command:

git clone https://github.com/yourusername/webapp.git
cd webapp

### Environment Variables

Copy the sample environment file and rename it to `.env`:

cp .env.sample .env

Edit the `.env` file and fill in the environment variables:

DEBUG=True
DATABASE=postgres
DB_NAME=webapp_db
DB_USER=user
DB_PASSWORD=test
DB_HOST=db
DB_PORT=5432
SECRET_KEY='secret'
ALLOWED_HOSTS=''

### Running the Application

Navigate to the `deploy/` folder and run the containers using the following command:

cd deploy
sudo sh run_containers.sh

This will build and start the Docker containers for your application.

### Accessing the Application

Once the containers are up and running, you can access the application at:

http://localhost:8000

## API Endpoints

### Upload CSV

Endpoint to upload a CSV file containing account information.

- **URL**: `/api/v1/v1/upload-csv/`
- **Method**: `POST`
- **Form Data**:
  - `file`: The CSV file to upload.
  - `agency_name`: The name of the collection agency.

### Retrieve Accounts

Endpoint to retrieve accounts with optional filters.

- **URL**: `/api/v1/v1/accounts/`
- **Method**: `GET`
- **Query Parameters**:
  - `min_balance`: Minimum balance to filter accounts by.
  - `max_balance`: Maximum balance to filter accounts by.
  - `consumer_name`: Consumer name to filter accounts by.
  - `status`: Status to filter accounts by.
  - `agency_name`: Agency name to filter accounts by.
  - `client_reference_no`: Client reference number to filter accounts by.
  - `consumer_ssn`: Consumer SSN to filter accounts by.

## Running Tests

To run the tests for the application, use the following command:

python manage.py test

This will execute the test suite and provide feedback on the status of your codebase.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
