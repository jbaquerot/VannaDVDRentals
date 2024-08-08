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
        Mistral.__init__(self, config={'api_key': MISTRAL_API_KEY, 'model': MISTRAL_MODEL})

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
    vn.train(documentation="the table actor stores actor data including first name and last name.")
    vn.train(documentation="the table film stores film data such as title, release year, length, rating, etc.")
    vn.train(documentation="the table film_actor stores the relationships between films and actors.")
    vn.train(documentation="the table category stores film’s categories data.")
    vn.train(documentation="the table film_category stores the relationships between films and categories.")
    vn.train(documentation="the tabel store contains the store data including manager staff and address.")
    vn.train(documentation="the table inventory: stores inventory data, film_id, store_id.")
    vn.train(documentation="the table rental: stores rental date, inventory_id, customer_id, return date.")
    vn.train(documentation="the table payment: stores customer’s payments, payment date. It can be used to calculate the sales. ")
    vn.train(documentation="the table staff: stores staff first name, last name, address_id, email, store_id where belongs, username and password")
    vn.train(documentation="the table customer: stores customer first name, last name, email, address_id, if the customer is active or not, creation date.")
    vn.train(documentation="the table address: stores address data for staff and customers")
    vn.train(documentation="the table city: stores city names and the country_id that belongs")
    vn.train(documentation="the table country: stores country names.")



     # You can also add SQL queries to your training data. This is useful if you have some queries already laying around. You can just copy and paste those from your editor to begin generating new SQL.
    
    question="How many stores does it have?"
    sql = """
        SELECT COUNT(DISTINCT(store_id)) AS num_stores 
        FOM store
        """
    vn.train(question = question, sql=sql)

    question = "Find the first names of all customers from the customer table"
    sql = """
        SELECT first_name FROM customer;
    """
    vn.train(question = question, sql=sql)

    question = "return the full names and emails of all customers from the customer table"
    sql = """
        SELECT 
            first_name || ' ' || last_name,
            email
        FROM 
        customer;
    """
    vn.train(question = question, sql=sql)

    question = "sort customers by their first names in ascending order"
    sql = """
        SELECT 
            first_name, 
            last_name 
        FROM 
            customer 
        ORDER BY 
            first_name ASC;
    """
    vn.train(question = question, sql=sql)

    question = "get customer_id, first_name and last_name for each payment from the customer table"
    sql = """
        SELECT 
            customer.customer_id, 
            customer.first_name, 
            customer.last_name, 
            payment.amount, 
            payment.payment_date 
        FROM 
            customer 
        INNER JOIN payment ON payment.customer_id = customer.customer_id 
        ORDER BY 
            payment.payment_date;
    """
    vn.train(question = question, sql=sql)


    question = "retrieve the total payment paid by each customer"
    sql = """
        SELECT 
            customer_id, 
            SUM (amount) 
        FROM 
            payment 
        GROUP BY 
            customer_id 
        ORDER BY 
            customer_id;
    """
    vn.train(question = question, sql=sql)


    question = "retrieve the total payment for each customer and display the customer name and amount"
    sql = """
        SELECT 
            first_name || ' ' || last_name full_name, 
            SUM (amount) amount 
        FROM 
            payment 
        INNER JOIN customer USING (customer_id) 
        GROUP BY 
            full_name 
        ORDER BY 
            amount DESC;        
    """
    vn.train(question = question, sql=sql)

    question = "select the only customers who have been spending more than 200"
    sql = """
        SELECT 
            customer_id, 
            SUM (amount) amount 
        FROM 
            payment 
        GROUP BY 
            customer_id 
        HAVING 
            SUM (amount) > 200 
        ORDER BY 
            amount DESC;       
    """
    vn.train(question = question, sql=sql)


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
