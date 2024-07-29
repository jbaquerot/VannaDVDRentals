import os
import psycopg2
import chromadb
from vanna.chromadb import ChromaDB_VectorStore
from vanna.mistral import Mistral

# Configuración de la base de datos Postgres
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Configuración de ChromaDB
CHROMA_HOST = os.getenv('CHROMA_HOST')
CHROMA_PORT = os.getenv('CHROMA_PORT')

# Configuración de Mistral API
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
MISTRAL_MODEL = os.getenv('MISTRAL_MODEL')

# Conexión a la base de datos Postgres
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Conexión a ChromaDB
#chroma_client = chromadb.Client(host=CHROMA_HOST, port=CHROMA_PORT)

# Inicialización de VannaClient
class MyVanna(ChromaDB_VectorStore, Mistral):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Mistral.__init__(self, config={'api_key': MISTRAL_API_KEY, 'model': 'mistral-tiny'})

vn = MyVanna()

vn.connect_to_postgres(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)

def train_vanna():
    # The information schema query may need some tweaking depending on your database. This is a good starting point.
    df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

    # This will break up the information schema into bite-sized chunks that can be referenced by the LLM
    plan = vn.get_training_plan_generic(df_information_schema)

    # If you like the plan, then uncomment this and run it to train
    vn.train(plan=plan)

    # The following are methods for adding training data. Make sure you modify the examples to match your database.

    # DDL statements are powerful because they specify table names, colume names, types, and potentially relationships
    vn.train(ddl="""
        CREATE TABLE IF NOT EXISTS my-table (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            age INT
        )
    """)

    # Sometimes you may want to add documentation about your business terminology or definitions.
    vn.train(documentation="the table actor – stores actor data including first name and last name.")
    vn.train(documentation="the table film – stores film data such as title, release year, length, rating, etc.")
    vn.train(documentation="the table film_actor – stores the relationships between films and actors.")
    vn.train(documentation="the table category – stores film’s categories data.")
    vn.train(documentation="the table film_category- stores the relationships between films and categories.")
    vn.train(documentation="the tabel store – contains the store data including manager staff and address.")
    vn.train(documentation="the table inventory – stores inventory data.")
    vn.train(documentation="the table rental – stores rental data.")
    vn.train(documentation="the table payment – stores customer’s payments.")
    vn.train(documentation="the table staff – stores staff data.")
    vn.train(documentation="the table customer – stores customer data.")
    vn.train(documentation="the table address – stores address data for staff and customers")
    vn.train(documentation="the table city – stores city names")
    vn.train(documentation="the table country – stores country names.")



     # You can also add SQL queries to your training data. This is useful if you have some queries already laying around. You can just copy and paste those from your editor to begin generating new SQL.
    question = "What is the film more rental in 2005?"
    sql = """
        SELECT f.title, COUNT(*) AS total_rentals 
        FROM film f
        JOIN inventory i ON f.film_id = i.film_id
        JOIN Rental r ON i.inventory_id = r.inventory_id
        WHERE EXTRACT(YEAR FROM r.rental_date) = '2005'
        GROUP BY f.title
        ORDER BY total_rentals DESC LIMIT 1;
    """
    vn.train(question = question, sql=sql)

    question = "what is the rental evolution of the film 'Bucket Brotherhood'?"
    sql = """
        SELECT f.title, 
        DATE_PART('YEAR',r.rental_date) as rental_year,
        DATE_PART('MONTH',r.rental_date) as rental_month,
        COUNT(*) AS total_rentals 
        FROM film f
        JOIN inventory i ON f.film_id = i.film_id
        JOIN Rental r ON i.inventory_id = r.inventory_id
        WHERE f.title = 'Bucket Brotherhood'
        GROUP BY f.title, rental_year, rental_month
        ORDER BY rental_year, rental_month, total_rentals;
    """
    vn.train(question = question, sql=sql)

if __name__ == "__main__":
    train_vanna()
    print("Vanna ha sido entrenada y la base de datos vectorial ha sido creada.")
