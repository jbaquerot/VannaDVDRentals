# Vanna App

Esta aplicación en Python utiliza la librería `vanna.ai` para hacer consultas SQL en lenguaje natural, utilizando el modelo Mistral via Mistral API y la base de datos vectorial ChromaDB. Todo esto está disponible en contenedores Docker utilizando Docker Compose y funciona tanto en Windows como en MacOS. Además, Vanna se conecta a una base de datos Postgres de ejemplo ([DVDRentals](https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/)) que se está ejecutando en un contenedor Docker en local.

## Estructura del Proyecto
```
vanna-app/
│
├── docker-compose.yml
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│   └── start.sh
│   └── train_vanna.py
└── data/
│   ├── postgres/
│   ├── temp/
└── sql/
│   ├── create_user.sql
```

## 1. Construimos el entorno para la aplicación
Clona el repositorio /jbaquerot/VannaDVDRentals:
```sh
# Actualizar la lista de paquetes
sudo apt update

# Instalar Git
sudo apt install git

# Clonar el repositorio
git clone https://github.com/jbaquerot/VannaDVDRentals.git

# Navegar al directorio del repositorio
cd VannaDVDRentals

# Verificar el estado del repositorio
git status
```

Navega al directorio del proyecto.
Abra una consola del sistema operativo ejecuta el siguiente comando para construir los contenedores:

```sh 
cd VannaDVDRentals
docker compose up --build
```

## 2. Cargar la base de datos *dvdrental* 

Este apartado está basado en [Load PostgreSQL Sample Database](https://www.postgresqltutorial.com/postgresql-getting-started/load-postgresql-sample-database/)

### 2.1 Crear la base de datos *dvdrental* 

*pg_restore* es una utilidad para restaurar una base de datos desde un archivo.

Para crear una base de datos y cargar datos desde un archivo, siga estos pasos:

Primero, abra OTRA consola del sistema y conéctese al contendor de PostgreSQL usando la herramienta *psql*:

```sh
docker exec -it postgres-container psql -U postgres
```

Es posible que le pida que ingrese una contraseña para el usuario de Postgres:
```sh
Password for user postgres:
```

La contraseña del usuario de Postgres es la que ingresó durante la instalación de PostgreSQL.

Después de ingresar la contraseña correctamente, se conectará al servidor PostgreSQL.

El símbolo del sistema se verá así:
```sh
postgres=#
```

En segundo lugar, verifique que la base de datos *dvdrental* está creada usando el comando *\l*. El comando *\l* mostrará todas las bases de datos en el servidor PostgreSQL:

```sh
\l
```
Salida:

List of databases

|   Name    |  Owner   | Encoding | Locale Provider |          Collate           |           Ctype            | ICU Locale | ICU Rules |   Access privileges
-----------|----------|----------|-----------------|----------------------------|----------------------------|------------|-----------|-----------------------
 dvdrental | postgres | UTF8     | libc            | English_United States.1252 | English_United States.1252 |            |           |
 postgres  | postgres | UTF8     | libc            | English_United States.1252 | English_United States.1252 |            |           |
 template0 | postgres | UTF8     | libc            | English_United States.1252 | English_United States.1252 |            |           | =c/postgres+postgres=CTc/postgres
 template1 | postgres | UTF8     | libc            | English_United States.1252 | English_United States.1252 |            |           | =c/postgres+postgres=CTc/postgres
(4 rows)

El resultado muestra que *dvdrental* está en la lista, lo que significa que ha creado la base de datos *dvdrental* correctamente.

Tenga en cuenta que otras bases de datos como *postgres*, *template0* y *template1* son las bases de datos del sistema.

Tercero, desconéctese del servidor PostgreSQL y salga de *psql* usando el comando *quit*:
```sh
\q
```

### 2.2 Restaurar la base de datos de *dvdrental* desde un archivo tar

Cuarto, descargue la base de datos de muestra [dvdrental.zip](https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip) y extraiga el archivo tar en un directorio como './data/temp'. Puedes utilizar el comando *curl* como sigue:

```sh
sudo curl -o ./data/temp/dvdrental.zip https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip
```

Para verificar que el directorio se ha montado correctamente, puedes ejecutar un comando dentro del contenedor de PostgreSQL para listar los archivos en el directorio montado.

```sh
docker exec -it postgres-container ls -al /tmp/shared
```

Esto debería mostrar los archivos en el directorio /var/lib/postgresql/data dentro del contenedor, que deberían corresponder a los archivos en el directorio data/postgres en tu máquina local.

Quinto, descomprime el fichero *dvdrental.zip*
```sh
sudo unzip ./data/temp/dvdrental.zip -d ./data/temp
```

Sexto, cargue la base de datos de dvdrental usando el comando pg_restore:

```sh
docker exec -it postgres-container pg_restore -U postgres -d dvdrental /tmp/shared/dvdrental.tar
```

En este comando:

*-U postgres* indica a *pg_restore* que conecte el servidor PostgreSQL utilizando el usuario de postgres.

*-d dvdrental* especifica la base de datos de destino que se cargará.
Le pedirá que ingrese la contraseña del usuario de Postgres. Ingrese la contraseña del usuario de postgres y presione Enter (o la tecla Return):

```sh
Password:
```

Tomará unos segundos cargar los datos almacenados en el archivo *dvdrental.tar* en la base de datos de *dvdrental*.

### 2.3 Verifica la base de datos *dvdrental* 

Primero conecta a la PostgreSQL usando el comando *psql*
```sh
docker exec -it postgres-container psql -U postgres
```
Segundo, cambia de base de datos actual a *dvdrental*:

```sh
\c dvdrental
```

El símbolo del sistema cambiará a lo siguiente:
```sh
dvdrental=#
```

En tercer lugar, muestre todas las tablas en la base de datos de *dvdrental*:

```sh
\dt
```

Sal de postgres
```sh
\q
```

Luego hay que rearrancar los contenedores
```sh
docker compose restart
```


## 3. Editar el fichero *.env*
Tienes que editar el fichero *.env* con tu clave *MISTRAL_API_KEY*

```
#Parámetros PostgreSQL
DB_USER=postgres
DB_PASSWORD=testVanna
DB_NAME=dvdrental
DB_HOST=localhost  
DB_PORT=5432

#Parámetros CHROMA
CHROMA_HOST=localhost
CHROMA_PORT=8000

#Parámetros API MISTRAL
MISTRAL_API_KEY=<you-mistral-key>
MISTRAL_MODEL=mistral-tiny
```

## 4. Abrir un navegador e introdución la URL:
Si todo ha ido bien, pueder abrir un navegador e ir a [localhost:8080](localhost:8080)

## 5. Algunas consultas de ejemplo
Aquí te dejo algunas consultas de prueba.

```
How many stores does it have?
```

También en español:
```
Cuantas tiendas hay?
```

```
Can you show me the sales evolution?
```
```
Can you show me the sales evolution month by month?
```

```
Which movies are the top 10 most paid?
```
```
Which are the top 10 actors who appear in the most movies?
```

## 6. Detener y eliminar los contenedores
Cuando hayas acabado de hacer pruebas, puedes detener y eliminar los contenedores con
```sh
# Detener y eliminar los contenedores
docker-compose down

# Eliminar todas las imágenes que no están en uso
docker image prune -a

# Eliminar todos los volúmenes que no están en uso
docker volume prune

# Eliminar todas las redes que no están en uso
docker network prune
```

Después de ejecutar estos comandos, puedes verificar que todos los contenedores, imágenes, volúmenes y redes han sido eliminados:
```sh
# Verificar contenedores
docker ps -a

# Verificar imágenes
docker images

# Verificar volúmenes
docker volume ls

# Verificar redes
docker network ls
```


