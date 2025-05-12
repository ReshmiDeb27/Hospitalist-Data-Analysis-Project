from pickle import PERSID
from tkinter import INSERT
import pandas as pd
import sqlite3

# Connect to SQLite, which creates a new database file if one isn't already present
conn = sqlite3.connect("hospital_data.db")
cursor = conn.cursor()

# Deletes old tables creating fresh ones during setup to avoid conflict
cursor.execute("DROP TABLE IF EXISTS PERSON")
cursor.execute("DROP TABLE IF EXISTS ENCOUNTER")
cursor.execute("DROP TABLE IF EXISTS OUTCOME")
cursor.execute("DROP TABLE IF EXISTS summary")

# Define the PERSON table schema for storing basic patient information
cursor.execute("""
    CREATE TABLE PERSON (
        PATIENT_ID TEXT,
        ENCOUNTER_ID TEXT,
        BIRTH_DATE TEXT,
        GENDER TEXT,
        PATIENT_TYPE TEXT
    )
""")

# Create an ENCOUNTER table to store information related to individual patient visits, locations, and timestamps
cursor.execute("""
    CREATE TABLE ENCOUNTER (
        ENCOUNTER_ID TEXT,
        FACILITY TEXT,
        UNIT TEXT,
        ADMIT_SOURCE TEXT,
        ADMIT_DT_TM TEXT,
        DISCHARGE_DT_TM TEXT
    )
""")

# Create an OUTCOME table for recording discharge status and patient exit information
cursor.execute("""
    CREATE TABLE OUTCOME (
        ENCOUNTER_ID TEXT,
        DISCHARGE_DISPOSITION TEXT
    )
""")

# Create the SUMMARY table to store aggregated patient metrics for reporting and analysis
cursor.execute("""
    CREATE TABLE summary (
        admit_month TEXT,
        gender TEXT,
        age_group TEXT,
        length_of_stay_avg REAL
    )
""")

# Load PERSON data from the CSV file and insert it into the PERSON table in the database
cursor.executescript("""
INSERT INTO PERSON VALUES
('P001', 'E001', '14-03-2005', 'Male', 'Inpatient'),
('P002', 'E002', '16-12-1995', 'Male', 'Inpatient'),
('P003', 'E003', '18-07-1954', 'Female', 'Inpatient'),
('P004', 'E004', '24-07-1973', 'Male', 'Outpatient'),
('P005', 'E005', '16-07-2010', 'Male', 'Outpatient'),
('P006', 'E006', '27-10-2016', 'Female', 'Inpatient'),
('P007', 'E007', '27-02-1970', 'Female', 'Inpatient'),
('P008', 'E008', '13-01-1949', 'Male', 'Inpatient'),
('P009', 'E009', '19-05-1945', 'Female', 'Inpatient'),
('P010', 'E010', '08-09-1960', 'Male', 'Outpatient'),
('P011', 'E011', '24-01-2018', 'Female', 'Outpatient'),
('P012', 'E012', '31-01-1969', 'Female', 'Inpatient'),
('P013', 'E013', '25-05-1975', 'Male', 'Outpatient'),
('P014', 'E014', '13-06-1951', 'Female', 'Inpatient'),
('P015', 'E015', '26-04-2001', 'Female', 'Outpatient'),
('P016', 'E016', '22-03-1967', 'Male', 'Inpatient'),
('P017', 'E017', '30-04-1948', 'Female', 'Outpatient'),
('P018', 'E018', '18-10-1985', 'Male', 'Outpatient'),
('P019', 'E019', '28-02-1955', 'Male', 'Outpatient'),
('P020', 'E020', '05-10-2004', 'Female', 'Outpatient'),
('P021', 'E021', '15-08-2005', 'Male', 'Inpatient'),
('P022', 'E022', '08-02-1964', 'Male', 'Outpatient'),
('P023', 'E023', '14-07-1964', 'Female', 'Inpatient'),
('P024', 'E024', '24-05-1950', 'Male', 'Inpatient'),
('P025', 'E025', '24-05-2008', 'Male', 'Inpatient'),
('P026', 'E026', '14-11-1953', 'Female', 'Outpatient'),
('P027', 'E027', '11-07-2024', 'Male', 'Inpatient'),
('P028', 'E028', '20-10-1959', 'Male', 'Inpatient'),
('P029', 'E029', '19-01-1960', 'Male', 'Outpatient'),
('P030', 'E030', '08-11-1942', 'Male', 'Outpatient'),
('P031', 'E031', '13-06-2013', 'Male', 'Outpatient'),
('P032', 'E032', '15-03-1968', 'Female', 'Outpatient'),
('P033', 'E033', '10-02-2023', 'Male', 'Outpatient'),
('P034', 'E034', '03-08-1999', 'Male', 'Outpatient'),
('P035', 'E035', '28-10-1999', 'Female', 'Outpatient'),
('P036', 'E036', '02-03-2015', 'Female', 'Inpatient'),
('P037', 'E037', '12-04-2015', 'Male', 'Inpatient'),
('P038', 'E038', '06-11-1951', 'Female', 'Inpatient'),
('P039', 'E039', '16-03-1979', 'Female', 'Outpatient'),
('P040', 'E040', '13-07-1970', 'Female', 'Outpatient'),
('P041', 'E041', '22-09-1956', 'Female', 'Outpatient'),
('P042', 'E042', '12-04-1978', 'Male', 'Inpatient'),
('P043', 'E043', '19-06-1976', 'Female', 'Outpatient'),
('P044', 'E044', '20-04-2010', 'Male', 'Outpatient'),
('P045', 'E045', '24-03-2019', 'Female', 'Inpatient'),
('P046', 'E046', '07-05-1960', 'Female', 'Inpatient'),
('P047', 'E047', '22-08-2022', 'Male', 'Inpatient'),
('P048', 'E048', '28-11-1943', 'Male', 'Outpatient'),
('P049', 'E049', '03-09-1952', 'Male', 'Inpatient'),
('P050', 'E050', '10-09-2011', 'Female', 'Inpatient'),
('P051', 'E051', '19-04-1969', 'Male', 'Inpatient'),
('P052', 'E052', '14-01-1963', 'Male', 'Outpatient'),
('P053', 'E053', '26-03-2018', 'Female', 'Inpatient'),
('P054', 'E054', '01-03-2003', 'Male', 'Outpatient'),
('P055', 'E055', '23-02-1961', 'Female', 'Inpatient'),
('P056', 'E056', '19-12-2006', 'Male', 'Inpatient'),
('P057', 'E057', '20-05-1986', 'Male', 'Inpatient'),
('P058', 'E058', '29-01-1963', 'Male', 'Inpatient'),
('P059', 'E059', '02-02-1939', 'Male', 'Inpatient'),
('P060', 'E060', '19-09-1956', 'Male', 'Outpatient'),
('P061', 'E061', '26-02-1968', 'Male', 'Outpatient');
""")

# Load ENCOUNTER data from the CSV file and insert it into the ENCOUNTER table in the database
cursor.executescript("""
INSERT INTO ENCOUNTER VALUES
('E001', 'Community Hospital', 'General Ward', 'ER', '27-10-2024 02:25', '06-11-2024 12:25'),
('E002', 'Community Hospital', 'ICU', 'ER', '01-01-2025 19:53', '12-01-2025 03:53'),
('E003', 'Community Hospital', 'General Ward', 'Referral', '30-01-2025 05:07', '05-02-2025 14:07'),
('E004', 'Community Hospital', 'Surgery', 'Referral', '07-02-2025 19:57', '08-02-2025 23:57'),
('E005', 'Community Hospital', 'General Ward', 'Referral', '16-07-2024 22:37', '25-07-2024 01:37'),
('E006', 'Main Hospital', 'Pediatrics', 'Clinic', '16-03-2025 00:59', '19-03-2025 03:59'),
('E007', 'Community Hospital', 'ICU', 'ER', '27-03-2025 08:16', '05-04-2025 18:16'),
('E008', 'Community Hospital', 'Pediatrics', 'Transfer', '23-12-2024 01:20', '01-01-2025 12:20'),
('E009', 'Main Hospital', 'Surgery', 'ER', '29-10-2024 12:07', '30-10-2024 21:07'),
('E010', 'Community Hospital', 'Surgery', 'Transfer', '21-04-2025 19:46', '27-04-2025 23:46'),
('E011', 'Community Hospital', 'Pediatrics', 'Referral', '29-10-2024 07:45', '05-11-2024 13:45'),
('E012', 'Community Hospital', 'Pediatrics', 'Referral', '26-11-2024 04:17', '05-12-2024 08:17'),
('E013', 'Community Hospital', 'Surgery', 'Clinic', '10-11-2024 23:23', '13-11-2024 11:23'),
('E014', 'Main Hospital', 'ICU', 'Transfer', '21-11-2024 14:35', '27-11-2024 22:35'),
('E015', 'Main Hospital', 'Pediatrics', 'Clinic', '29-12-2024 04:36', '01-01-2025 12:36'),
('E016', 'Community Hospital', 'Pediatrics', 'ER', '12-10-2024 12:56', '21-10-2024 14:56'),
('E017', 'Community Hospital', 'ICU', 'ER', '29-09-2024 20:16', '04-10-2024 05:16'),
('E018', 'Community Hospital', 'General Ward', 'Referral', '27-06-2024 02:51', '04-07-2024 10:51'),
('E019', 'Main Hospital', 'Pediatrics', 'Clinic', '21-05-2024 14:50', '31-05-2024 15:50'),
('E020', 'Main Hospital', 'General Ward', 'Clinic', '05-03-2025 16:51', '07-03-2025 19:51'),
('E021', 'Community Hospital', 'ICU', 'Transfer', '12-05-2024 17:02', '15-05-2024 04:02'),
('E022', 'Main Hospital', 'Surgery', 'Clinic', '11-06-2024 12:44', '17-06-2024 15:44'),
('E023', 'Community Hospital', 'Pediatrics', 'Clinic', '13-01-2025 12:50', '16-01-2025 23:50'),
('E024', 'Main Hospital', 'Pediatrics', 'Referral', '21-12-2024 23:53', '27-12-2024 00:53'),
('E025', 'Main Hospital', 'Pediatrics', 'ER', '14-08-2024 04:33', '18-08-2024 09:33'),
('E026', 'Community Hospital', 'Surgery', 'Clinic', '20-12-2024 10:54', '26-12-2024 13:54'),
('E027', 'Main Hospital', 'ICU', 'Referral', '17-04-2025 02:33', '24-04-2025 11:33'),
('E028', 'Main Hospital', 'General Ward', 'Referral', '05-07-2024 23:07', '11-07-2024 01:07'),
('E029', 'Main Hospital', 'Pediatrics', 'Transfer', '03-02-2025 02:49', '12-02-2025 08:49'),
('E030', 'Community Hospital', 'General Ward', 'Transfer', '27-08-2024 21:28', '03-09-2024 23:28'),
('E031', 'Main Hospital', 'Surgery', 'ER', '02-10-2024 08:48', '12-10-2024 14:48'),
('E032', 'Community Hospital', 'General Ward', 'Transfer', '01-02-2025 20:43', '10-02-2025 02:43'),
('E033', 'Community Hospital', 'ICU', 'ER', '17-04-2025 10:56', '27-04-2025 22:56'),
('E034', 'Community Hospital', 'Pediatrics', 'Transfer', '08-03-2025 12:23', '14-03-2025 21:23'),
('E035', 'Community Hospital', 'ICU', 'Clinic', '06-10-2024 06:05', '11-10-2024 15:05'),
('E036', 'Community Hospital', 'Surgery', 'Transfer', '10-05-2025 17:11', '12-05-2025 21:11'),
('E037', 'Community Hospital', 'Pediatrics', 'Transfer', '10-09-2024 06:29', '14-09-2024 17:29'),
('E038', 'Community Hospital', 'ICU', 'ER', '21-03-2025 08:09', '28-03-2025 12:09'),
('E039', 'Community Hospital', 'Surgery', 'Transfer', '23-11-2024 21:25', '30-11-2024 09:25'),
('E040', 'Main Hospital', 'Surgery', 'ER', '07-07-2024 02:00', '08-07-2024 10:00'),
('E041', 'Community Hospital', 'Pediatrics', 'ER', '06-08-2024 10:53', '09-08-2024 14:53'),
('E042', 'Community Hospital', 'ICU', 'Referral', '11-04-2025 23:26', '19-04-2025 11:26'),
('E043', 'Main Hospital', 'ICU', 'Clinic', '13-10-2024 11:21', '19-10-2024 14:21'),
('E044', 'Community Hospital', 'Surgery', 'Clinic', '02-02-2025 15:12', '10-02-2025 20:12'),
('E045', 'Community Hospital', 'Pediatrics', 'Referral', '11-01-2025 02:30', '18-01-2025 11:30'),
('E046', 'Main Hospital', 'General Ward', 'ER', '24-10-2024 06:12', '03-11-2024 18:12'),
('E047', 'Main Hospital', 'General Ward', 'Clinic', '27-10-2024 07:18', '01-11-2024 19:18'),
('E048', 'Main Hospital', 'ICU', 'Transfer', '26-11-2024 19:09', '03-12-2024 20:09'),
('E049', 'Main Hospital', 'Surgery', 'Transfer', '11-03-2025 23:36', '13-03-2025 02:36'),
('E050', 'Community Hospital', 'ICU', 'ER', '10-07-2024 19:21', '15-07-2024 06:21'),
('E051', 'Community Hospital', 'Surgery', 'Referral', '17-07-2024 05:53', '25-07-2024 10:53'),
('E052', 'Community Hospital', 'Pediatrics', 'Referral', '14-12-2024 10:57', '16-12-2024 22:57'),
('E053', 'Community Hospital', 'General Ward', 'Clinic', '04-06-2024 20:15', '14-06-2024 01:15'),
('E054', 'Main Hospital', 'General Ward', 'Clinic', '29-04-2025 12:08', '30-04-2025 20:08'),
('E055', 'Community Hospital', 'General Ward', 'Clinic', '21-09-2024 01:04', '27-09-2024 08:04'),
('E056', 'Main Hospital', 'Surgery', 'Referral', '08-12-2024 06:36', '11-12-2024 14:36'),
('E057', 'Community Hospital', 'Pediatrics', 'Transfer', '14-07-2024 07:03', '19-07-2024 08:03'),
('E058', 'Main Hospital', 'ICU', 'Transfer', '10-07-2024 01:13', '18-07-2024 10:13'),
('E059', 'Community Hospital', 'Surgery', 'ER', '28-08-2024 01:46', '07-09-2024 07:46'),
('E060', 'Main Hospital', 'General Ward', 'Clinic', '10-01-2025 01:22', '20-01-2025 07:22'),
('E061', 'Main Hospital', 'ICU', 'Clinic', '23-09-2024 14:20', '24-09-2024 21:20'),
('E062', 'Main Hospital', 'ICU', 'Referral', '29-07-2024 17:09', '05-08-2024 02:09'),
('E063', 'Main Hospital', 'Pediatrics', 'ER', '27-09-2024 19:24', '05-10-2024 05:24'),
('E064', 'Main Hospital', 'General Ward', 'Clinic', '11-11-2024 05:55', '15-11-2024 14:55'),
('E065', 'Community Hospital', 'General Ward', 'Transfer', '09-09-2024 07:36', '10-09-2024 10:36'),
('E066', 'Main Hospital', 'Surgery', 'Clinic', '27-09-2024 03:04', '30-09-2024 11:04'),
('E067', 'Main Hospital', 'ICU', 'Transfer', '27-06-2024 19:25', '04-07-2024 23:25'),
('E068', 'Community Hospital', 'General Ward', 'Clinic', '25-06-2024 03:27', '30-06-2024 13:27'),
('E069', 'Community Hospital', 'General Ward', 'Referral', '17-03-2025 06:11', '25-03-2025 18:11'),
('E070', 'Community Hospital', 'General Ward', 'Transfer', '24-01-2025 21:01', '31-01-2025 09:01'),
('E071', 'Main Hospital', 'Surgery', 'Clinic', '25-09-2024 21:10', '30-09-2024 01:10'),
('E072', 'Main Hospital', 'Pediatrics', 'ER', '01-06-2024 21:37', '05-06-2024 02:37'),
('E073', 'Community Hospital', 'Surgery', 'ER', '20-02-2025 23:54', '01-03-2025 03:54'),
('E074', 'Community Hospital', 'ICU', 'Clinic', '23-01-2025 15:40', '31-01-2025 22:40'),
('E075', 'Community Hospital', 'General Ward', 'Clinic', '08-11-2024 13:54', '18-11-2024 18:54'),
('E076', 'Main Hospital', 'ICU', 'Clinic', '20-02-2025 04:20', '24-02-2025 07:20'),
('E077', 'Community Hospital', 'Pediatrics', 'Transfer', '15-01-2025 04:49', '17-01-2025 05:49'),
('E078', 'Main Hospital', 'General Ward', 'Referral', '05-09-2024 01:43', '09-09-2024 08:43'),
('E079', 'Main Hospital', 'Pediatrics', 'Referral', '10-09-2024 09:14', '12-09-2024 15:14'),
('E080', 'Main Hospital', 'ICU', 'Referral', '16-02-2025 12:14', '26-02-2025 20:14'),
('E081', 'Main Hospital', 'General Ward', 'Clinic', '03-08-2024 10:07', '05-08-2024 13:07'),
('E082', 'Main Hospital', 'General Ward', 'Clinic', '07-11-2024 02:53', '12-11-2024 11:53'),
('E083', 'Main Hospital', 'ICU', 'Referral', '17-06-2024 23:58', '28-06-2024 10:58'),
('E084', 'Community Hospital', 'Pediatrics', 'ER', '31-05-2024 15:02', '06-06-2024 00:02'),
('E085', 'Community Hospital', 'Surgery', 'ER', '09-03-2025 07:08', '17-03-2025 13:08'),
('E086', 'Community Hospital', 'General Ward', 'Clinic', '27-11-2024 07:29', '02-12-2024 08:29'),
('E087', 'Main Hospital', 'General Ward', 'Clinic', '25-06-2024 00:32', '02-07-2024 04:32'),
('E088', 'Main Hospital', 'General Ward', 'Transfer', '19-01-2025 10:12', '26-01-2025 19:12'),
('E089', 'Main Hospital', 'ICU', 'ER', '21-10-2024 10:05', '23-10-2024 21:05'),
('E090', 'Main Hospital', 'General Ward', 'Referral', '10-07-2024 23:04', '21-07-2024 03:04'),
('E091', 'Community Hospital', 'General Ward', 'Clinic', '29-12-2024 01:34', '01-01-2025 09:34'),
('E092', 'Main Hospital', 'Pediatrics', 'ER', '08-07-2024 09:23', '12-07-2024 12:23'),
('E093', 'Main Hospital', 'ICU', 'ER', '27-10-2024 20:07', '07-11-2024 02:07'),
('E094', 'Community Hospital', 'Surgery', 'ER', '07-05-2025 00:16', '13-05-2025 09:16'),
('E095', 'Community Hospital', 'Surgery', 'Referral', '10-01-2025 11:00', '12-01-2025 20:00'),
('E096', 'Community Hospital', 'Pediatrics', 'ER', '19-10-2024 08:45', '28-10-2024 09:45'),
('E097', 'Main Hospital', 'Surgery', 'ER', '25-04-2025 20:06', '05-05-2025 22:06'),
('E098', 'Main Hospital', 'General Ward', 'Clinic', '09-01-2025 21:35', '14-01-2025 23:35'),
('E099', 'Community Hospital', 'General Ward', 'Referral', '06-12-2024 00:32', '13-12-2024 12:32'),
('E100', 'Community Hospital', 'ICU', 'Referral', '11-05-2024 01:27', '21-05-2024 06:27');
""")

# Load OUTCOME data from the CSV file and insert it into the OUTCOME table in the database
cursor.executescript("""
INSERT INTO OUTCOME VALUES
('E001', 'Expired'),
('E002', 'Transferred'),
('E003', 'Transferred'),
('E004', 'Expired'),
('E005', 'Left AMA'),
('E006', 'Left AMA'),
('E007', 'Rehab'),
('E008', 'Expired'),
('E009', 'Transferred'),
('E010', 'Left AMA'),
('E011', 'Transferred'),
('E012', 'Home'),
('E013', 'Home'),
('E014', 'Left AMA'),
('E015', 'Expired'),
('E016', 'Home'),
('E017', 'Expired'),
('E018', 'Left AMA'),
('E019', 'Rehab'),
('E020', 'Left AMA'),
('E021', 'Transferred'),
('E022', 'Rehab'),
('E023', 'Transferred'),
('E024', 'Transferred'),
('E025', 'Left AMA'),
('E026', 'Transferred'),
('E027', 'Expired'),
('E028', 'Rehab'),
('E029', 'Rehab'),
('E030', 'Left AMA'),
('E031', 'Left AMA'),
('E032', 'Expired'),
('E033', 'Rehab'),
('E034', 'Transferred'),
('E035', 'Transferred'),
('E036', 'Transferred'),
('E037', 'Transferred'),
('E038', 'Left AMA'),
('E039', 'Home'),
('E040', 'Expired'),
('E041', 'Transferred'),
('E042', 'Home'),
('E043', 'Transferred'),
('E044', 'Left AMA'),
('E045', 'Transferred'),
('E046', 'Transferred'),
('E047', 'Rehab'),
('E048', 'Expired'),
('E049', 'Expired'),
('E050', 'Transferred'),
('E051', 'Expired'),
('E052', 'Rehab'),
('E053', 'Rehab'),
('E054', 'Transferred'),
('E055', 'Rehab'),
('E056', 'Expired'),
('E057', 'Transferred'),
('E058', 'Transferred'),
('E059', 'Transferred'),
('E060', 'Rehab'),
('E061', 'Home'),
('E062', 'Transferred'),
('E063', 'Home'),
('E064', 'Transferred'),
('E065', 'Left AMA'),
('E066', 'Home'),
('E067', 'Expired'),
('E068', 'Expired'),
('E069', 'Home'),
('E070', 'Expired'),
('E071', 'Home'),
('E072', 'Left AMA'),
('E073', 'Rehab'),
('E074', 'Transferred'),
('E075', 'Left AMA'),
('E076', 'Left AMA'),
('E077', 'Home'),
('E078', 'Home'),
('E079', 'Expired'),
('E080', 'Left AMA'),
('E081', 'Left AMA'),
('E082', 'Rehab'),
('E083', 'Transferred'),
('E084', 'Home'),
('E085', 'Left AMA'),
('E086', 'Expired'),
('E087', 'Left AMA'),
('E088', 'Expired'),
('E089', 'Home'),
('E090', 'Home'),
('E091', 'Rehab'),
('E092', 'Transferred'),
('E093', 'Expired'),
('E094', 'Left AMA'),
('E095', 'Left AMA'),
('E096', 'Rehab'),
('E097', 'Home'),
('E098', 'Transferred'),
('E099', 'Left AMA'),
('E100', 'Expired');
""")
                            
# Commit inserted data and safely close the database connection
conn.commit()
cursor.close()
conn.close()

print("SQLite tables created and summary data loaded successfully.")
