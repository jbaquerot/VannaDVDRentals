import os
import psycopg2
from streamlit import get_report_ctx
from streamlit.server.server import Server

class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

def get_session_state():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session

session_state = get_session_state()

import chromadb
import streamlit as st

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



# ======= BEGIN VANNA SETUP =======

from vanna.chromadb import ChromaDB_VectorStore
from vanna.mistral import Mistral

class MyVanna(ChromaDB_VectorStore, Mistral):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Mistral.__init__(self, config={'api_key': MISTRAL_API_KEY, 'model': 'mistral-tiny'})

vn = MyVanna()

vn.connect_to_postgres(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)

# ======= END VANNA SETUP =======

my_question = st.session_state.get("my_question", default=None)

if "conversation" not in session_state:
    session_state.conversation = []

if my_question is None:
    my_question = st.text_input(
        "Ask me a question about your data",
        key="my_question",
    )
else:
    st.text(my_question)
    session_state.conversation.append(("User", my_question))

    sql = vn.generate_sql(my_question)
    df = vn.run_sql(sql)
    code = vn.generate_plotly_code(question=my_question, sql=sql, df=df)
    fig = vn.get_plotly_figure(plotly_code=code, df=df)

    session_state.conversation.append(("Bot", fig))

    for role, message in session_state.conversation:
        st.text(f"{role}: {message}")



