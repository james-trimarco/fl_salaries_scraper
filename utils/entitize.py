import pandas as pd
from pathlib import Path

# employees
# statuses
# changes


def read_employees():
    employees_path = Path.cwd() / "data" / "employees.pkl"
    try:
        pd.read_pickle(employees_path)
    except FileNotFoundError as e:
        print(e)
    return None


if __name__ == "__main__":
    read_employees()
