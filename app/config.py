import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL


load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DB = os.getenv("MYSQL_DB", "netpulse_db")
MYSQL_USER = os.getenv("MYSQL_USER", "netpulse_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "change_me")
DATABASE_URL = os.getenv("DATABASE_URL") or URL.create(
    "mysql+pymysql",
    username=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DB,
).render_as_string(hide_password=False)
STORAGE_BACKEND = os.getenv("NETPULSE_STORAGE", "memory").strip().lower()

if STORAGE_BACKEND not in {"memory", "mysql"}:
    raise ValueError("NETPULSE_STORAGE must be either 'memory' or 'mysql'.")