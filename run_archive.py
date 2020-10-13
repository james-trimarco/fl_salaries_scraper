import pandas as pd
import requests
import psycopg2
import urllib.parse as up
from pathlib import Path
import sqlalchemy as db
from datetime import date

from utils import execute_sql
from private.config import config

rebuild = False

sql_path = Path.cwd() / "sql"
archive_path = Path.cwd() / "archive"

up.uses_netloc.append("postgres")
url = up.urlparse(config["url"])

print(url.hostname)

db_url = db.engine.url.URL(
    drivername="postgresql",
    username=config["username"],
    password=config["password"],
    host=config["host"],
    database=config["username"],
    port=config["port"],
)

# create an engine
engine = db.create_engine(db_url, echo=False)

if rebuild:
    print("Creating schemas")
    execute_sql(sql_path / "create_schema.sql", engine, read_file=True)
    print("Creating tables")
    execute_sql(sql_path / "create_tables.sql", engine, read_file=True)

today = date.today()
fdate = date.today().strftime("%Y-%m-%d")


base_url = "https://salaries.myflorida.com/"
download_suffix = "?action=index&controller=salaries&format=csv"
download_url = base_url + download_suffix
salaries_raw = pd.read_csv(download_url)
print(salaries_raw.head(3))
salaries_raw.columns = [col.lower().replace(" ", "_") for col in salaries_raw.columns]

salaries_raw.to_csv(path_or_buf=archive_path / f"fl_salaries_{fdate}.csv", na_rep="NA")

