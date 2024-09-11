
# Project Vanna DVDRentals

This project is a comprehensive test and demonstration of the Vanna.ai library. The project involves setting up a PostgreSQL database using data from the DVDRentals application. This database is then utilized by a Python application that is containerized and managed using Docker and Docker Compose. The primary goal of this project is to showcase the capabilities of the Vanna.ai library in a real-world application scenario.


## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Docker and Docker Compose installed on your machine.
- Git installed on your machine.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/jbaquerot/VannaDVDRentals
   cd VannaDVDRentals
   ```

2. **Create a `.env` file**:
   - Create a `.env` file in the root of the project with the following content:
     ```env
     DB_USER=your_db_user
     DB_PASSWORD=your_db_password
     DB_NAME=your_db_name
     CHROMA_HOST=chroma-container
     CHROMA_PORT=8000
     MISTRAL_API_KEY=your_api_key
     MISTRAL_MODEL=mistral-tiny
     ```

3. **Build and run the Docker containers**:
   ```sh
   docker-compose up --build
   ```

## Configuration

### `.env` File

The `.env` file contains environment variables used by the Docker containers. Here is an example:

```env
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
CHROMA_HOST=chroma-container
CHROMA_PORT=8000
MISTRAL_API_KEY=your_api_key
MISTRAL_MODEL=mistral-tiny
```

### `docker-compose.yml`

The `docker-compose.yml` file defines the services that will be run using Docker Compose. Here is an example:

```yaml
services:
  postgres:
    image: postgres:latest
    container_name: postgres-container
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "5432:5432"
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
      - ./data/temp:/tmp/shared
    networks:
      - vanna-net

  chroma:
    image: chromadb/chroma:latest
    container_name: chroma-container
    ports:
      - "8000:8000"
    networks:
      - vanna-net

  vanna:
    build:
      context: ./app
      dockerfile: Dockerfile
    container_name: vanna-container
    environment:
      DB_HOST: postgres-container
      DB_PORT: 5432
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
      CHROMA_HOST: ${CHROMA_HOST}
      CHROMA_PORT: ${CHROMA_PORT}
      MISTRAL_API_KEY: ${MISTRAL_API_KEY}
    ports:
      - "8080:8080"
    depends_on:
      - postgres
    networks:
      - vanna-net

networks:
  vanna-net:
    driver: bridge
```

### `Dockerfile`

The `Dockerfile` defines the environment for the Python application. Here is an example:

```Dockerfile
# Use a base image of Python 3.10
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt requirements.txt

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for the initialization script
RUN apt-get update && apt-get install -y curl unzip postgresql-client

# Copy the initialization script to the container
COPY setup_db.sh /app/setup_db.sh
COPY wait-for-postgres.sh /app/wait-for-postgres.sh

# Give execute permissions to the initialization scripts
RUN chmod +x /app/setup_db.sh /app/wait-for-postgres.sh

# Copy the rest of the application files to the container
COPY . .

# Specify the command to run the initialization script and then the application
CMD ["sh", "-c", "/app/wait-for-postgres.sh postgres-container && /app/setup_db.sh && sh start.sh"]
```

### `setup_db.sh`

The `setup_db.sh` script initializes the PostgreSQL database with data from a remote repository. Here is an example:

```sh
#!/bin/bash

# Environment variables
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}
DB_NAME=${DB_NAME:-dvdrental}
DB_HOST=${DB_HOST:-postgres-container}
DB_PORT=${DB_PORT:-5432}

# Download the backup file
BACKUP_URL="https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip"
BACKUP_FILE="dvdrental.zip"
EXTRACTED_FILE="dvdrental.tar"

# Download the backup file
echo "Downloading the backup file..."
curl -o $BACKUP_FILE $BACKUP_URL

# Unzip the backup file
echo "Unzipping the backup file..."
unzip $BACKUP_FILE

# Create the database
echo "Creating the database $DB_NAME..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -c "CREATE DATABASE $DB_NAME;"

# Load the data into the database
echo "Loading the data into the database $DB_NAME..."
PGPASSWORD=$DB_PASSWORD pg_restore -h $DB_HOST -U $DB_USER -d $DB_NAME -v $EXTRACTED_FILE

echo "Database $DB_NAME created and loaded successfully."
```

### `wait-for-postgres.sh`

The `wait-for-postgres.sh` script waits for the PostgreSQL server to be ready before running the initialization script. Here is an example:

```sh
#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD=$DB_PASSWORD psql -h "$host" -U "$DB_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
```

## Usage

1. **Start the application**:
   ```sh
   docker-compose up --build
   ```

2. **Access the application**:
   - The application will be available at `http://localhost:8080`.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Contact

José Carlos Baquero

Project Link: [https://github.com/jbaquerot/VannaDVDRentals](https://github.com/jbaquerot/VannaDVDRentals)