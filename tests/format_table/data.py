from datetime import datetime as dt
import numpy as np


def make_dt(string):
    format = "%m/%d/%Y %I:%M:%S %p"  # datetime like 10/11/2019 4:17:57 PM
    date = dt.strptime(string, format)
    return date


FORMATS = {
    "sample_processed": {
        "agency_name": ["object"],
        "budget_entity": ["object"],
        "position_number": ["object"],
        "last_name": ["object"],
        "first_name": ["object"],
        "middle_name": ["object"],
        "is_salaried": ["bool"],
        "is_full_time": ["bool"],
        "class_code": ["object"],
        "class_title": ["object"],
        "state_hire_date": ["datetime64[ns]"],
        "salary": ["float64"],
        "ops_hourly_rate": ["float64"],
    },
    "sample_raw": {
        "Agency Name": ["object"],
        "Budget Entity": ["float64"],
        "Position Number": ["object"],
        "Last Name": ["object"],
        "First Name": ["object"],
        "Middle Name": ["object"],
        "Employee Type": ["object"],
        "Full/Part Time": ["object"],
        "Class Code": ["object"],
        "Class Title": ["object"],
        "State Hire Date": ["object"],
        "Salary": ["object"],
        "OPS Hourly Rate": ["object"],
    },
}


DATAFRAMES = {
    "sample_raw": {
        "Agency Name": [
            "Agency for Health Care Admin",
            "Department of Corrections",
            "Department of Juvenile Justice",
        ],
        "Budget Entity": [
            "HEALTH FAC & PRAC REG",
            "SPECIALTY INST OPERATIONS",
            "DETENTION CENTERS",
        ],
        "Position Number": ["25", "64202", "900323"],
        "Last Name": ["ZWISSLER", "BELL", "DESYLVIA"],
        "First Name": ["SUSAN", "EDWARD", "VONDA"],
        "Middle Name": ["W", np.nan, "KAYE"],
        "Employee Type": ["Salaried", "Salaried", "OPS"],
        "Full/Part Time": ["Full Time", "Full Time", "Part Time"],
        "Class Code": ["5620", "8005", "5712"],
        "Class Title": [
            "HEALTH FACILITY EVALUATOR II",
            "CORRECTIONAL OFFICER SERGEANT",
            "JUVENILE JUSTICE DETENTION OFFICER II",
        ],
        "State Hire Date": ["6/27/86", "5/22/15", np.nan],
        "Salary": ["$     3,3278.96", "$     7,4905.74", np.nan],
        "OPS Hourly Rate": [np.nan, np.nan, "$         13.00"],
    },
    "sample_processed": {
        "agency_name": [
            "agency for health care admin",
            "department of corrections",
            "department of juvenile justice",
        ],
        "budget_entity": [
            "health fac & prac reg",
            "specialty inst operations",
            "detention centers",
        ],
        "position_number": ["25", "64202", "900323"],
        "last_name": ["zwissler", "bell", "desylvia"],
        "first_name": ["susan", "edward", "vonda"],
        "middle_name": ["w", np.nan, "kaye"],
        "is_salaried": [True, True, False],
        "is_full_time": [True, True, False],
        "class_code": ["5620", "8005", "5712"],
        "class_title": [
            "health facility evaluator ii",
            "correctional officer sergeant",
            "juvenile justice detention officer ii",
        ],
        "state_hire_date": [dt(1989, 6, 27), dt(2015, 5, 22), np.nan],
        "salary": [33278.96, 74905.74, np.nan],
        "ops_hourly_rate": [np.nan, np.nan, 13.00],
    },
}

