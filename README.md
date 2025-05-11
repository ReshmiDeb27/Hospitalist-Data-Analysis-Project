## Database Table: PERSON

This table was created in the Snowflake schema `RESHMI_DB.DASHBOARD_DATA` to store patient demographic and encounter information used in the project.

### SQL DDL:

CREATE OR REPLACE TABLE RESHMI_DB.DASHBOARD_DATA.PERSON (
    PATIENT_ID VARCHAR(16777216),
    ENCOUNTER_ID VARCHAR(400),
    BIRTH_DATE TIMESTAMP_NTZ(9),
    GENDER VARCHAR(80),
    PATIENT_TYPE VARCHAR(80)
);

## Database Table: ENCOUNTER

This table was created in the Snowflake schema `RESHMI_DB.DASHBOARD_DATA` to store information about patient hospital encounters, including admission and discharge timestamps.

### SQL DDL:

CREATE OR REPLACE TABLE RESHMI_DB.DASHBOARD_DATA.ENCOUNTER (
    ENCOUNTER_ID VARCHAR(400),
    FACILITY VARCHAR(80),
    UNIT VARCHAR(80),
    ADMIT_SOURCE VARCHAR(80),
    ADMIT_DT_TM TIMESTAMP_LTZ(9),
    DISCHARGE_DT_TM TIMESTAMP_LTZ(9)
);

## Database Table: OUTCOME

This table stores discharge-related outcome information for each patient encounter. It is used to analyze post-encounter disposition (e.g., home, rehab, expired).

### SQL DDL:

```sql
CREATE OR REPLACE TABLE RESHMI_DB.DASHBOARD_DATA.OUTCOME (
    ENCOUNTER_ID VARCHAR(400),
    DISCHARGE_DISPOSITION VARCHAR(80)
);
