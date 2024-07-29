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
Clona el repositorio o crea la estructura de archivos manualmente.
Navega al directorio del proyecto.
Abra una consola del sistema operativo ejecuta el siguiente comando para construir los contenedores:

```sh 
docker compose up --build
```

## 2. Cargar la base de datos DVDRentals

Este apartado está basado en [Load PostgreSQL Sample Database](https://www.postgresqltutorial.com/postgresql-getting-started/load-postgresql-sample-database/)

### 2.1 Create the dvdrental database

*pg_restore* es una utilidad para restaurar una base de datos desde un archivo.

Para crear una base de datos y cargar datos desde un archivo, siga estos pasos:

Primero, abra otra consola del sistema y conéctese al contendor de PostgreSQL usando la herramienta *psql*:

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

En segundo lugar, cree una nueva base de datos llamada dvdrental usando la instrucción *CREATE DATABASE*:

```sh
CREATE DATABASE dvdrental;
```

Salida:

```sh
CREATE DATABASE
```
PostgreSQL creará una nueva base de datos llamada *dvdrental*.

En tercer lugar, verifique la creación de la base de datos usando el comando *\l*. El comando *\l* mostrará todas las bases de datos en el servidor PostgreSQL:

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

Cuarto, desconéctese del servidor PostgreSQL y salga de *psql* usando el comando *quit*:
```sh
\q
```

### 2.2 Restore the sample database from a tar file

Quinto, descargue la base de datos de muestra [dvdrental.zip](https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip) y extraiga el archivo tar en un directorio como './data/temp'.

Para verificar que el directorio se ha montado correctamente, puedes ejecutar un comando dentro del contenedor de PostgreSQL para listar los archivos en el directorio montado.

```sh
docker exec -it postgres-container ls -al /var/lib/postgresql/data
```

```sh
docker exec -it postgres-container ls -al /tmp/shared
```

Esto debería mostrar los archivos en el directorio /var/lib/postgresql/data dentro del contenedor, que deberían corresponder a los archivos en el directorio data/postgres en tu máquina local.

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

### 2.3 Verifica la base de datos de ejemplo

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


## 3. Abrir un navegador e introdución la URL:
[localhost:8080](localhost:8080)

