# db_config.py
from sqlalchemy import create_engine

HOST = "localhost"
PORT = 5432
DB_NAME = "facturas_db"
USERNAME = "postgres"
PASSWORD = "postgres"

def get_engine():
    return create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")
