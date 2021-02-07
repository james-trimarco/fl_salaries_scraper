import pandas as pd
from pathlib import Path
from utils.download_to_archive import DOWNLOAD_URL, scrape_salary_data, set_http_version

if __name__ == "__main__":
    # SCRAPING
    set_http_version()
    # set path to archive
    archive_path = Path.cwd() / "archive"
    scrape_salary_data(archive_path, DOWNLOAD_URL)

    # BUILD DATABASE

