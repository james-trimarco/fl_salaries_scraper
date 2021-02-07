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


#     @pytest.mark.parametrize(
#         "filename,expected",
#         [
#             ("DummyCoreIntegrator.xlsx", format.FORMATS["core integrator"]["input"]),
#             ("DummyPromptComments.xlsx", format.FORMATS["comments"]["input"]),
#         ],
#     )
#     def test_dummy_reports(self, filename, expected):
#         """check_format() should pass when dataframe has expected format"""
#         # setup
#         path = Path.cwd() / "tests" / "format_reports" / filename
#         df = pd.read_excel(path, engine="openpyxl")
#         print(df.dtypes)

#         # execution
#         passed, error = format.check_format(df, expected)
#         print(error)

#         # validation
#         assert passed
#         assert error is None


# class TestFormatReports:
#     """Tests the main functions in format_reports.py"""

#     def test_clean_report(self):
#         """Tests clean_report() against a sample dataframe to make sure that
#         the column names were standardized, white spaces were stripped,
#         and rows without a vendor_id were dropped"""

#         # setup
#         cols = ["Extra Space", "Vendor ID", "Document Number", "Date (Julian)"]
#         df_in = pd.DataFrame(data.DATAFRAMES["sample_raw"])
#         expected_cols = ["extra_space", "vendor_id", "document_number", "date_julian"]
#         expected_str = ["Row 1", "Row 2"]
#         expected_doc = [123, "P195"]
#         expected_vendor = [55564, 54376]

#         # execution
#         df_out = format.clean_report(df_in, return_cols=cols)
#         out_cols = df_out.columns
#         out_str = list(df_out["extra_space"])
#         out_vendor = list(df_out["vendor_id"])

#         # validation
#         for col in expected_cols:
#             assert col in out_cols
#         assert out_str == expected_str
#         assert out_vendor == expected_vendor

#     def test_format_comments_report(self):
#         """Tests format_report() against a dummy comments excel file"""
#         # input
#         file_name = "DummyPromptComments.xlsx"
#         input_format = format.FORMATS["comments"]["input"]
#         output_format = format.FORMATS["comments"]["output"]
#         expected = data.DATAFRAMES["comments_output"]

#         # setup
#         file_path = Path.cwd() / "tests" / "format_reports" / file_name
#         df_in = pd.read_excel(file_path, engine="openpyxl")
#         passed, errors = format.check_format(df_in, input_format)
#         assert passed

#         # execution
#         passed, message, df_out = format.format_report(df_in, "comments")
#         matches, errors = format.check_format(df_out, output_format)

#         print("OUTPUT MESSAGE")
#         pprint(message)
#         print("OUTPUT DTYPES")
#         print(df_out.dtypes)
#         out_data = df_out.head(2).to_dict("list")
#         print("OUTPUT")
#         pprint(out_data)
#         print("EXPECTED")
#         pprint(expected)

#         # validation
#         assert passed
#         assert list(df_out.columns) == list(expected.keys())
#         assert matches
#         assert out_data == expected

#     def test_format_core_integrator_report(self):
#         """Tests format_report() against dummy core integrator excel file"""
#         # input
#         file_name = "DummyCoreIntegrator.xlsx"
#         input_format = format.FORMATS["core integrator"]["input"]
#         output_format = format.FORMATS["core integrator"]["output"]
#         expected = data.DATAFRAMES["core_output"]

#         # setup
#         file_path = Path.cwd() / "tests" / "format_reports" / file_name
#         df_in = pd.read_excel(file_path, engine="openpyxl")
#         passed, errors = format.check_format(df_in, input_format)
#         assert passed

#         # execution
#         passed, errors, df_out = format.format_report(df_in, "core integrator")
#         matches, errors = format.check_format(df_out, output_format)

#         print("OUTPUT DTYPES")
#         print(df_out.dtypes)
#         out_data = df_out.head(2).to_dict("list")
#         print("OUTPUT")
#         pprint(out_data)
#         print("EXPECTED")
#         pprint(expected)

#         # validation
#         assert passed
#         assert list(df_out.columns) == list(expected.keys())
#         assert len(df_out["location"]) == 17
#         assert df_out.head(2).equals(pd.DataFrame(expected))
