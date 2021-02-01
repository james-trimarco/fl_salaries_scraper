import pandas as pd
from pathlib import Path
from utils.download_to_archive import DOWNLOAD_URL, scrape_salary_data, set_http_version

if __name__ == "__main__":
    # set path to archive
    archive_path = Path.cwd() / "archives" / "archive_raw"
    scrape_salary_data(archive_path, DOWNLOAD_URL)

