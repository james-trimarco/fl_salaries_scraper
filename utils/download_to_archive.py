import pandas as pd
import requests
import csv
import urllib.request
import urllib.parse as up
from pathlib import Path
from datetime import date
from http.client import IncompleteRead
import http.client as http


# set url to download data from
BASE_URL = "https://salaries.myflorida.com/"
URL_SUFFIX = "?action=index&controller=salaries&format=csv"
DOWNLOAD_URL = BASE_URL + URL_SUFFIX


def set_http_version():
    # This move seems to reduce the likelihood of IncompleteRead errors
    http.HTTPConnection._http_vsn = 10
    http.HTTPConnection._http_vsn_str = "HTTP/1.0"
    return


def scrape_salary_data(archive_path, download_url, max_retries=5):
    today = date.today()
    formatted_date = date.today().strftime("%Y-%m-%d")
    current_salaries_path = archive_path / f"fl_salaries_{formatted_date}.csv"
    print(f"Requesting data from {download_url}")
    response = urllib.request.urlopen(download_url)

    max_retries = max_retries
    attempt = 0
    while attempt < max_retries:
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
    return

