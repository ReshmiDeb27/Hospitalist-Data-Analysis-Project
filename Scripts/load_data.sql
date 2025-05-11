-- Drop tables if they exist
DROP TABLE IF EXISTS PERSON;
DROP TABLE IF EXISTS ENCOUNTER;
DROP TABLE IF EXISTS OUTCOME;

-- Create PERSON table
CREATE TABLE PERSON (
    PATIENT_ID VARCHAR(100),
    ENCOUNTER_ID VARCHAR(100),
    BIRTH_DATE CHAR(25),
    GENDER VARCHAR(80),
    PATIENT_TYPE VARCHAR(80)
);

-- Create ENCOUNTER table
CREATE TABLE ENCOUNTER (
    ENCOUNTER_ID VARCHAR(100),
    FACILITY VARCHAR(80),
    UNIT VARCHAR(80),
    ADMIT_SOURCE VARCHAR(80),
    ADMIT_DT_TM CHAR(25),
    DISCHARGE_DT_TM CHAR(25)
);

-- Create OUTCOME table
CREATE TABLE OUTCOME (
    ENCOUNTER_ID VARCHAR(100),
    DISCHARGE_DISPOSITION VARCHAR(80)
);

-- Set mode to CSV (only works in SQLite CLI)
.mode csv
.headers on

-- Import CSV data (update paths as needed)
.import 'input/person.csv' PERSON
.import 'input/encounter.csv' ENCOUNTER
.import 'input/outcome.csv' OUTCOME
