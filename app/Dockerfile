# Utilizar una imagen base de Python 3.10
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt requirements.txt

# Instalar las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias adicionales para el script de inicialización
RUN apt-get update && apt-get install -y curl unzip postgresql-client

# Copiar el script de espera y el script de inicialización al contenedor
COPY wait-for-postgres.sh /app/wait-for-postgres.sh
COPY setup_db.sh /app/setup_db.sh

# Dar permisos de ejecución a los scripts
RUN chmod +x /app/wait-for-postgres.sh /app/setup_db.sh

# Copiar el resto de los archivos de la aplicación al contenedor
COPY . .

# Especificar el comando para ejecutar el script de espera, el script de inicialización y luego la aplicación
CMD ["sh", "-c", "/app/wait-for-postgres.sh postgres-container && /app/setup_db.sh && sh start.sh"]