import os
import psycopg2
from dotenv import load_dotenv

environment = "dev"

def get_connection():

    _env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path=_env_path, override=True)
    print("Connection Prod success!")

    url = os.getenv("DATABASE_URL")
    if url:
        return psycopg2.connect(url)
    
    host = os.getenv("DB_HOST")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT", "5432")

    if not all([host, dbname, user, password]):
        raise RuntimeError("Set DATABASE_URL or DB_HOST/DB_NAME/DB_USER/DB_PASSWORD in .env")

    return psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
        