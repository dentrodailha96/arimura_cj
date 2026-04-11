# ---------------------------------------------------------------
# NOTE: Create a db_connection.py file alongside this one:

import psycopg2

def get_connection():
    return psycopg2.connect(
         host="ep-soft-lab-aca39wz6-pooler.sa-east-1.aws.neon.tech",
         dbname="db_arimura",
         user="neondb_owner",
         password="npg_tnGaIEQkoJ16",
         port=5432
     )

