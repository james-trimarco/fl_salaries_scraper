DROP TABLE if exists raw.salaries;

CREATE TABLE if not exists raw.salaries (
    upload_id INT NOT NULL,
    record_id INT UNIQUE,
    agency_name CHAR,
    budget_entity CHAR,
    position_number CHAR,
    last_name CHAR,
    first_name CHAR,
    middle_name CHAR,
    employee_type CHAR,
    full_or_part_time CHAR,
    class_code CHAR,
    class_title CHAR,
    state_hire_date CHAR,
    salary CHAR,
    ops_hourly_rate CHAR
);

DROP TABLE if exists raw.uploads;

CREATE TABLE if not exists raw.uploads (
    upload_id CHAR,
    record_id CHAR
);