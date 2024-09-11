#!/bin/bash

# Variables de entorno
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}
DB_NAME=${DB_NAME:-dvdrental}
DB_HOST=${DB_HOST:-postgres-container}
DB_PORT=${DB_PORT:-5432}

# Descargar el archivo de respaldo
BACKUP_URL="https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip"
BACKUP_FILE="dvdrental.zip"
EXTRACTED_FILE="dvdrental.tar"

# Descargar el archivo de respaldo
echo "Descargando el archivo de respaldo..."
curl -o $BACKUP_FILE $BACKUP_URL

# Descomprimir el archivo de respaldo
echo "Descomprimiendo el archivo de respaldo..."
unzip $BACKUP_FILE

# Crear la base de datos
echo "Creando la base de datos $DB_NAME..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -c "CREATE DATABASE $DB_NAME;"

# Cargar los datos en la base de datos
echo "Cargando los datos en la base de datos $DB_NAME..."
PGPASSWORD=$DB_PASSWORD pg_restore -h $DB_HOST -U $DB_USER -d $DB_NAME -v $EXTRACTED_FILE

echo "Base de datos $DB_NAME creada y cargada con éxito."
