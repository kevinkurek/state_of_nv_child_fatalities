import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv('.env')
FULL_DATA_PATH = os.getenv("FULL_DATA_PATH")# Full config for main.py



###### CHANGEABLE VARIABLES

SCRAPE_YEARS = ['2021', '2022', '2023']
URL_based_run=False

######




# Built for Kevin Development, shouldn't have to change ever.

# used in main to run all urls
URL_LIST = [
    "https://dcfs.nv.gov/Programs/CWS/CPS/ChildFatalities/Clark/",
    "https://dcfs.nv.gov/Programs/CWS/CPS/ChildFatalities/Rural/",
    "https://dcfs.nv.gov/Programs/CWS/CPS/ChildFatalities/Washoe/",
]

# TODO: bad practice to have python inside config, but ok for dev/debugging
FULL_PATH_COUNTIES = [
    os.path.join(fr"{FULL_DATA_PATH}", "Clark"),
    os.path.join(fr"{FULL_DATA_PATH}", "Rural"),
    os.path.join(fr"{FULL_DATA_PATH}", "Washoe"),
]  # used in main to run all folder paths if given

# Define the keys you want to extract
KEYS = [
    "Date",
    "Agency Name",
    "Agency Address",
    "Date of written notification to the Division of Child and Family Services and Legislative Auditor",
    "Internal reference UNITY Case Number",
    "Internal reference UNITY Case Number or Report Number",
    "Child Fatality Date of Death",
    "Near Fatality Date of Near Fatality",
    "A summary of the report of abuse or neglect and a factual description of the contents of the report",
    "The date of birth and gender of child",
    "The cause of the fatality or near fatality, if such information has been determined",
    "The date that the child suffered the fatality or near fatality",
    "Date of the notification to the child welfare agency of the death of a child",
    "Location of child at the time of death or near fatality (city/county)",
]

# rename columns
RENAME_COLS = {
    "date_of_written_notification_to_the_division_of_child_and_family_services_and_legislative_auditor": "date_of_written_notification",
    "near_fatality_date_of_near_fatality": "near_fatality_date",
    "a_summary_of_the_report_of_abuse_or_neglect_and_a_factual_description_of_the_contents_of_the_report": "summary_of_incident",
    "location_of_child_at_the_time_of_death_or_near_fatality_city/county": "location_of_child_at_time_of_incident",
    "date_of_the_notification_to_the_child_welfare_agency_of_the_death_of_a_child": "date_of_notification_to_welfare_agency_of_death",
    "the_date_that_the_child_suffered_the_fatality_or_near_fatality": "date_child_suffered_incident",
    "the_date_of_birth_and_gender_of_child": "date_of_birth_and_gender",
    "the_cause_of_the_fatality_or_near_fatality,_if_such_information_has_been_determined": "cause_of_incident_if_determined",
}

# renamed time columns
TIME_COLS = [
    "date",
    "date_of_written_notification",
    "child_fatality_date_of_death",
    "near_fatality_date",
]
