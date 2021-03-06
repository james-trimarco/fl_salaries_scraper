import pandas as pd
from utils.df_formats import FORMATS
import numpy as np


def format_salaries(val):
    """
    """
    if val != val:
        return np.nan
    else:
        assert isinstance(val, str)
        if val[0] == "$":
            val = val[1:].strip()
        val = val.replace(",", "")
        val = val.replace(".", "")
    return val


def numeric_string(val, fill):
    """
    """
    if val != val:
        return np.nan
    else:
        return str(int(val)).zfill(fill)


def format_table(df_raw):
    """Formats the input reports for merging and calculation
    Args:
        df_raw (dataframe): Input dataframe to be formatted
    Returns:
        df (dataframe): The formatted dataframe
    """
    input = FORMATS["input"]
    output = FORMATS["output"]
    return_cols = input.keys()  # which columns to preserve

    # check that the core report matches expected input format
    passed, errors = check_format(df_raw, input)
    if not passed:
        error = f"The input table doesn't match expected format: {errors}"
        return False, error, None

    # clean report and standardize merge columns
    df = clean_report(df_raw)
    df = df.rename(
        columns={"employee_type": "is_salaried", "full/part_time": "is_full_time"}
    )
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

    # convert ID fields to 0-padded numeric strings
    df["position_number"] = df["position_number"].apply(lambda x: numeric_string(x, 7))
    df["class_code"] = df["class_code"].apply(lambda x: numeric_string(x, 5))

    # convert two cols to booleans
    salary_map = {"is_salaried": {"SALARIED": True, "OPS": False}}
    full_time_map = {"is_full_time": {"FULL TIME": True, "PART TIME": False}}
    df = df.replace(salary_map)
    df = df.replace(full_time_map)
    df[["is_salaried", "is_full_time"]] = df[["is_salaried", "is_full_time"]].astype(
        "bool"
    )

    # format our numeric strings to represent cents as integers
    df["salary"] = df["salary"].apply(format_salaries)
    df["ops_hourly_rate"] = df["ops_hourly_rate"].apply(format_salaries)
    # cast to integers
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce").astype(pd.Int64Dtype())
    df["ops_hourly_rate"] = pd.to_numeric(df["salary"], errors="coerce").astype(
        pd.Int64Dtype()
    )
    df["state_hire_date"] = df["state_hire_date"].astype("datetime64").dt.date

    # check that output dataframe
    passed, errors = check_format(df, output)
    if not passed:
        error = f"Table didn't get formatted correctly: {errors}"
        return False, error, None

    message = f"Successfully formatted Florida salaries table."
    return True, message, df


def check_format(df, format):
    """ Checks the column names and dtypes of the dataframe against
    a dictionary with the expected values for both of those things
    Args:
        df (dataframe): Dataframe to check
        format: Dictionary of required cols and list of acceptable dtypes
    Returns:
        passed: Boolean that indicates whether or not the check passed
        error: Error message if the check did not pass
    """

    # check that all of the expected columns are present
    exp_cols = format.keys()
    missing_cols = [col for col in exp_cols if col not in df.columns]
    if missing_cols:
        error = f"The following columns are missing: {missing_cols}"
        return False, error

    # check that each column has a dtype that is accepted
    wrong_dtypes = {}
    for col, accepted_dtypes in format.items():
        dtype = str(df[col].dtype)
        if dtype not in accepted_dtypes:
            wrong_dtypes[col] = {"accepted": accepted_dtypes, "actual": dtype}
    if wrong_dtypes:
        error = f"The following columns have the wrong type: {wrong_dtypes}"
        return False, error

    return True, None


def clean_report(df_raw, na_cols=None, return_cols=None):
    """ Cleans a dataframe by standardizing column names, stripping whitespaces
    around string values, dropping rows with missing data (for certain cols)
    Args:
        df_raw (dataframe): Input dataframe
        na_cols (list): List of cols to check for missing values
        return_cols (list): List of cols to return, default returns all cols
    Returns:
        df (dataframe): Clean dataframe
    """
    print("cleaning the report")

    # make a copy of the columns to return
    if return_cols:
        df = df_raw[return_cols].copy()
    else:
        df = df_raw.copy()

    # standardize col names
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    df.columns = [col.replace("(", "") for col in df.columns]
    df.columns = [col.replace(")", "") for col in df.columns]

    # remove whitespaces around string columns
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df
