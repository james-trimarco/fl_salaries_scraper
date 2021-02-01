import pandas as pd
import requests
import csv
import urllib.request
import urllib.parse as up
from pathlib import Path
from datetime import date
from http.client import IncompleteRead

import http.client as http

http.HTTPConnection._http_vsn = 10
http.HTTPConnection._http_vsn_str = "HTTP/1.0"

# from utils import execute_sql
# from private.config import config
# rebuild = False
# sql_path = Path.cwd() / "sql"
# up.uses_netloc.append("postgres")
# url = up.urlparse(config["url"])

# # print(url.hostname)

# db_url = db.engine.url.URL(
#     drivername="postgresql",
#     username=config["username"],
#     password=config["password"],
#     host=config["host"],
#     database=config["username"],
#     port=config["port"],
# )

# # create an engine
# engine = db.create_engine(db_url, echo=False)

# if rebuild:
#     print("Creating schemas")
#     execute_sql(sql_path / "create_schema.sql", engine, read_file=True)
#     print("Creating tables")
#     execute_sql(sql_path / "create_tables.sql", engine, read_file=True)

# set path to archive
archive_path = Path.cwd() / "archives" / "archive_raw"

# set url to download data from
base_url = "https://salaries.myflorida.com/"
download_suffix = "?action=index&controller=salaries&format=csv"
download_url = base_url + download_suffix


def scrape_salary_data(archive_path, download_url):
    today = date.today()
    formatted_date = date.today().strftime("%Y-%m-%d")
    current_salaries_path = archive_path / f"fl_salaries_{formatted_date}.csv"

    response = urllib.request.urlopen(download_url)

    maxretries = 5
    attempt = 0
    while attempt < maxretries:
        try:
            lines = [l.decode("utf-8") for l in response.readlines()]
            fl_reader = csv.reader(lines)
            with open(current_salaries_path, "w", newline="") as csvfile:
                fl_writer = csv.writer(
                    csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL,
                )
                for idx, row in enumerate(fl_reader):
                    print(idx)
                    fl_writer.writerow(row)
        except IncompleteRead as e:
            attempt += 1
            print(f"Failed on attempt {attempt} with error {e}")
        else:
            break


scrape_salary_data(archive_path, download_url)

# salaries_raw = pd.read_csv(download_url)
# print(salaries_raw.head(3))
# salaries_raw.columns = [col.lower().replace(" ", "_") for col in salaries_raw.columns]

# salaries_raw.to_csv(path_or_buf=archive_path / f"fl_salaries_{fdate}.csv", na_rep="NA")

