import pytest
import pandas as pd
from pathlib import Path
from pprint import pprint

import tests.format_table.data as data
import utils.format_table as format


class TestCheckTable:
    """Tests check_format() against a few different scenarios"""

    def test_correct_format(self):
        """check_format() should pass when dataframe has expected format"""
        # setup
        expected = data.FORMATS["sample_processed"]
        df = pd.DataFrame(data.DATAFRAMES["sample_processed"])
        print(df.dtypes)

        # execution
        passed, error = format.check_format(df, expected)
        print(error)

        # validation
        assert passed
        assert error is None

    def test_missing_column(self):
        """Check_format() should not pass and return an error message with
        the missing columns when dataframe doesn't have all expected cols"""
        # input
        missing_col = "position_number"
        exp_error = f"The following columns are missing: {[missing_col]}"
        expected = data.FORMATS["sample_processed"]

        # setup
        df_raw = pd.DataFrame(data.DATAFRAMES["sample_processed"])
        df = df_raw.drop(columns="position_number")
        assert missing_col not in df.columns

        # execution
        passed, error = format.check_format(df, expected)
        print(error)

        # validation
        assert not passed
        assert error == exp_error

    def test_wrong_dtype(self):
        """Check_format() should not pass and return an error message with
        the list of incorrect dtypes if the dtypes don't match expected"""
        # input
        col, dtype = "class_code", "int64"
        wrong_dtype = {col: {"accepted": ["object"], "actual": dtype}}
        exp_error = f"The following columns have the wrong type: {wrong_dtype}"
        expected = data.FORMATS["sample_processed"]

        # setup
        df = pd.DataFrame(data.DATAFRAMES["sample_processed"])
        df[col] = df[col].astype(dtype)
        assert df[col].dtype == dtype
        print(df.dtypes)

        # execution
        passed, error = format.check_format(df, expected)
        print("WRONG DTYPE")
        print(wrong_dtype)
        print("ERROR")
        print(error)

        # validation
        assert not passed
        assert error == exp_error


class TestFormatReports:
    """Tests the main functions in format_reports.py"""

    def test_clean_report(self):
        """Tests clean_report() against a sample dataframe to make sure that
        the column names were standardized and white spaces were stripped."""

        # setup
        cols = [
            "Budget Entity",
            "Position Number",
        ]
        df_in = pd.DataFrame(data.DATAFRAMES["sample_raw"])
        expected_cols = ["budget_entity", "position_number"]
        expected_entity = [
            "HEALTH FAC & PRAC REG",
            "SPECIALTY INST OPERATIONS",
            "DETENTION CENTERS",
        ]
        expected_position = ["25", "64202", "900323"]

        # execution
        df_out = format.clean_report(df_in, return_cols=cols)
        out_cols = df_out.columns
        out_entity = list(df_out["budget_entity"])
        out_position = list(df_out["position_number"])

        # validation
        for col in expected_cols:
            assert col in out_cols
        assert out_entity == expected_entity
        assert out_position == expected_position

    def test_format_table(self):
        """Tests format_table() against dummy .csv file"""
        # input
        input_file_name = "dummy_fl_salary_input.csv"
        output_file_name = "dummy_fl_salary_output.pkl"
        input_file_path = Path.cwd() / "tests" / "format_table" / input_file_name
        output_file_path = Path.cwd() / "tests" / "format_table" / output_file_name
        input_format = format.FORMATS["input"]
        output_format = format.FORMATS["output"]

        # setup
        df_in = pd.read_csv(input_file_path, dtype="object")
        expected = pd.read_pickle(output_file_path)

        passed, errors = format.check_format(df_in, input_format)
        assert passed

        # execution
        passed, errors, df_out = format.format_table(df_in)
        matches, errors = format.check_format(df_out, output_format)

        print("OUTPUT DTYPES")
        print(df_out.dtypes)
        out_data = df_out.head(2).to_dict("list")
        print("OUTPUT")
        pprint(out_data)
        print("EXPECTED")
        pprint(expected)

        # validation
        assert passed
        assert list(df_out.columns) == list(expected.keys())
        assert (df_out["position_number"].str.len() == 8).all()
        assert (df_out["class_code"].str.len() == 5).all()
        # assert df_out.head(2).equals(pd.DataFrame(expected))
