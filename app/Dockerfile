# Utilizar una imagen base de Python 3.10
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt requirements.txt

# Instalar las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación al contenedor
COPY . .


# Especificar el comando para ejecutar el entrenamiento y la aplicación
CMD ["sh", "start.sh"]