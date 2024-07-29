#!/bin/bash

# Cargar las variables de entorno desde el archivo .env
export $(grep -v '^#' .env | xargs)

# Sustituir las variables en el script SQL
envsubst < sql/create_user.sql > sql/create_user_temp.sql

# Ejecutar el script SQL en el contenedor de PostgreSQL
docker exec -it postgres-container psql -U postgres -f sql/create_user_temp.sql

# Limpiar el archivo temporal
rm sql/create_user_temp.sql