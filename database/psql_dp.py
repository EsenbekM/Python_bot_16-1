import psycopg2
from config import URI

db = psycopg2.connect(URI, sslmode='require')
cursor = db.cursor()

