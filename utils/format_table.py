import pandas as pd
from utils.df_formats import FORMATS


# NON_NULLABLE = ["vendor_id", "document_number"]


def format_salaries(val):
    """
    """
    if val != val:
        return np.nan
    else:
        assert isinstance(val, str)
        if val[0] == "$":
            val = val[1:]
        val = val.replace(",", "")
    return val


def numeric_string(val, fill):
    """
    """
    if val != val:
        print("nan detected")
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
        error = f"Table report doesn't match expected input format: {errors}"
        return False, error, None

    # # clean report and standardize merge columns
    df = clean_report(df_raw)
    df = df.rename(
        columns={"employee_type": "is_salaried", "full/part_time": "is_full_time"}
    )
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

    df["position_number"] = (
        df["position_number"].astype("float").astype("Int64").astype(str).str.zfill(7)
    )
    df["class_code"] = (
        df["class_code"].astype("float").astype("Int64").astype(str).str.zfill(5)
    )

    salary_map = {"is_salaried": {"SALARIED": True, "OPS": False}}
    full_time_map = {"is_full_time": {"FULL TIME": True, "PART TIME": False}}

    df = df.replace(salary_map)
    df = df.replace(full_time_map)

    print(df.head())

    # {'is_salaried': {'accepted': ['bool'], 'actual': 'object'},
    # 'is_full_time': {'accepted': ['bool'], 'actual': 'object'},
    # 'state_hire_date': {'accepted': ['datetime64[ns]'], 'actual': 'object'},
    # 'ops_hourly_rate': {'accepted': ['float64'], 'actual': 'object'}}"

    # check that output dataframe
    # passed, errors = check_format(df, output)
    # if not passed:
    #     error = f"Table didn't get formatted correctly: {errors}"
    #     return False, error, None

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
