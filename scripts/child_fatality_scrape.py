import os
import re
import time
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import pdfplumber
import zipcodes
from typing import List, Dict


def download_all_pdfs(url: str) -> str:
    """
    Download all PDFs from a specified URL and save to a local directory.

    Args:
        url (str): URL to scrape for PDF links.

    Returns:
        save_dir (str): Directory where PDFs are saved.

    Example:
        url = 'https://www.some_url.com'
        download_all_pdfs(url)
    """

    # Get the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all links in the webpage
    links = soup.find_all("a")

    # directory pdfs will be saved
    county = url.split("/")[-2]
    save_dir = os.path.join(".", "output_files", f"{county}_pdfs")  # use os.path.join for OS compatibility

    # UNIQUE: this uploadedFiles path is required, why?
    # Due to the level of inconsistency in the pdf formats between counties
    # Clark has consistency: 2023-01-17_ID_1469166.pdf, 2023-01-22_ID_1506602.pdf, etc...
    # Washoe & Rural are random: 1482308_child_B.pdf, Disclosure_Form_Final_01_04_2019.pdf
    upload_href = (
        f"/uploadedFiles/dcfsnvgov/content/Programs/CWS/CPS/ChildFatalities/{county}"
    )

    # Download each PDF
    for link in links:
        href = link.get("href")
        if href and upload_href in href and href.endswith(".pdf"):

            # append needed dcfs link since pdf hrefs don't come naturally with it
            prefix_for_href = "https://dcfs.nv.gov/"
            href = prefix_for_href + href

            # Get the PDF content
            pdf_response = requests.get(href)

            # Get the PDF name from the URL
            pdf_name = os.path.basename(href)

            # Create the directory if it doesn't exist
            if not os.path.exists(save_dir):
                print(f"Making Directory: {save_dir.split('/')[-1]}")
                os.makedirs(save_dir)

            # Save the PDFs to the directory
            with open(os.path.join(save_dir, pdf_name), "wb") as f:
                f.write(pdf_response.content)

    return save_dir


def list_files(path: str) -> List[str]:
    """
    Lists all files in a specified directory.

    Args:
        path (str): Path of the directory to list files from.

    Returns:
        files (list): List of file names in the directory.

    Example:
        path = '/path/to/directory'
        list_files(path)
    """

    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append(file)

    return files


def restructure_alphabetical_dict(alphabetical_dict: Dict[str, str]) -> Dict[str, str]:
    """
    Restructures a dictionary by splitting values into a new key-value pair.

    Args:
        alphabetical_dict (dict): Dictionary to be restructured.

    Returns:
        new_dict (dict): Restructured dictionary with new key-value pairs.

    Example:
        alphabetical_dict = {'A': 'A. Some Key: Some Value'}
        restructure_alphabetical_dict(alphabetical_dict)
        # Output: {'Some Key': 'Some Value'}
    """

    new_dict = {}
    for key, value in alphabetical_dict.items():
        # Split the value into a key-value pair
        split_value = value.split(":", 1)
        if len(split_value) > 1:
            # The key is everything before ":" and the value is everything after ":"
            new_key = split_value[0]
            # Replace all '\n' in the value with empty string
            new_value = split_value[1].replace("\n", "")
            new_dict[new_key] = new_value
    return new_dict


def full_merge_dicts(data: Dict[str, str], new_dict: Dict[str, str]) -> Dict[str, str]:
    """
    Merges two dictionaries, updating existing keys and adding new keys and values.

    Args:
        data (dict): The original dictionary to be merged.
        new_dict (dict): The dictionary containing new keys and values to be merged.

    Returns:
        dict: The merged dictionary with updated and added key-value pairs.

    Example:
        data = {"A": "hi", "B": ""}
        new_dict = {"B": "hey", "C": "you"}
        merge_dicts(data, new_dict)
        >>> {'A': 'hi', 'B': 'hey', 'C': 'you'}
    """
    for key in new_dict:
        data[key] = new_dict[key]
    return data


def merge_dicts(data: Dict[str, str], new_dict: Dict[str, str]) -> Dict[str, str]:
    """
    Merges two dictionaries. If a key is present in both, the value from new_dict is used.

    Args:
        data (dict): First dictionary to merge.
        new_dict (dict): Second dictionary to merge.

    Returns:
        data (dict): Merged dictionary.

    Example:
        data = {'key1': 'value1', 'key2': ''}
        new_dict = {'key2': 'new_value2', 'key3': 'value3'}
        merge_dicts(data, new_dict)
        # Output: {'key1': 'value1', 'key2': 'new_value2'}
    """

    for key in new_dict:
        if key in data:
            data[key] = new_dict[key]
    return data


def scrape_individual_pdf(pages_text: List[str], keys: List[str]) -> pd.DataFrame:
    """
    Scrapes text from each page of a PDF document and organizes it into a dictionary,
    which is then turned into a pandas DataFrame.

    Args:
        pages_text (list): List of strings, where each string represents the text on a page of the PDF.
        keys (list): List of keys to initialize the dictionary with.

    Returns:
        df (DataFrame): DataFrame created from the scraped data.

    Example:
        keys = ['key1', 'key2']
        pages_text = ['Page 1 text', 'Page 2 text']
        scrape_individual_pdf(pages_text, keys)
    """

    # Initialize a dictionary with the keys and empty values
    data = {key: "" for key in keys}
    alphabetical_dict = {}
    current_alphabetical_key = None
    information_for_release_index = None

    # Find the index of 'INFORMATION FOR RELEASE'
    for page_text in pages_text:
        lines = page_text.split("\n")
        for i, line in enumerate(lines):
            if "INFORMATION FOR RELEASE" in line:
                information_for_release_index = i
                break

    for page_text in pages_text:
        lines = page_text.split("\n")

        for i, line in enumerate(lines):
            if i < information_for_release_index:
                # Split each line into a key-value pair
                if ": " in line:
                    key, value = line.split(": ", 1)
                    # Only add the key-value pair to the dictionary if the key is in the list of keys
                    if key in keys and not data[key]:
                        data[key] = value
            else:
                # For lines after "INFORMATION FOR RELEASE"
                match = re.match(r"([A-Z])\.", line)
                if match:
                    # Alphabetical key detected
                    current_alphabetical_key = match.group(1)
                    # Initialize the new key in the dictionary
                    alphabetical_dict[current_alphabetical_key] = (
                        line[3:] + "\n"
                    )  # remove the redundant key by slicing from index 3
                elif current_alphabetical_key:
                    # If it's not a new key, append the line to the last key's value
                    alphabetical_dict[current_alphabetical_key] += line + "\n"

    # Needed to restructure alphabetical dictionary for messiness inside
    new_dict = restructure_alphabetical_dict(alphabetical_dict)

    # Put new_dict = {'A summary of the report of abuse or neglect and a factual description of the contents of the report': 'CCDFS received ....'}
    # into "data" dict which currently has blank values for the associated keys
    data = merge_dicts(data, new_dict)

    # Now you can create a DataFrame from your data
    df = pd.DataFrame(data, index=[0])

    # Replace empty strings with NaN
    df.replace("", np.nan, inplace=True)

    return df


def loop_pdf_scrape(
    file_list: List[str], path: str, keys: List[str]
) -> List[pd.DataFrame]:
    """
    Iterates over a list of PDF files in a directory and scrapes each one.

    Args:
        file_list (list): List of file names.
        path (str): Path of the directory where the files are located.
        keys (list): List of keys to initialize the dictionary with.

    Returns:
        df_list (list): List of DataFrames, where each DataFrame represents the scraped data from a PDF.

    Example:
        file_list = ['file1.pdf', 'file2.pdf']
        path = '/path/to/directory'
        keys = ['key1', 'key2']
        loop_pdf_scrape(file_list, path, keys)
    """

    df_list = []
    for pdf_file in file_list:

        # make sure full directory is appended before opening
        pdf_file = path + "/" + pdf_file

        with pdfplumber.open(pdf_file) as pdf:
            # Extract text from each page
            pages_text = [page.extract_text() for page in pdf.pages]
            individual_df = scrape_individual_pdf(pages_text, keys)
            df_list.append(individual_df)

    return df_list


def get_city_by_zip(zip_code: str) -> str:
    """
    This function returns the city corresponding to the given zip code.
    It uses the `matching` function from the `zipcodes` package to find the city.

    Parameters:
    zip_code (str): The zip code for which to find the corresponding city.

    Returns:
    str: The city that corresponds to the given zip code. If no city is found, it returns None.

    Example:
    >>> get_city_by_zip('89706')
    'Carson City'

    >>> get_city_by_zip('00000')
    np.nan

    >>> get_city_by_zip('abcd-123')
    np.nan
    """

    try:
        result = zipcodes.is_real(str(zip_code))
    except Exception:
        return np.nan

    result = zipcodes.matching(str(zip_code))
    # If a result was found, return the city from the first match
    if result:
        return result[0]["city"]

    # If no result was found, return np.nan
    return np.nan

def parse_dob_gender(value):
    # First, we find DOB by searching for a pattern that looks like a date
    dob_match = re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', value)
    dob = dob_match.group(0) if dob_match else None

    # Next, we look for gender by checking for the words "male" or "female" (case insensitive)
    gender_match = re.search(r'male|female', value, re.IGNORECASE)
    gender = gender_match.group(0) if gender_match else None

    return pd.Series([dob, gender])

def cleaning_df(
    df_list: List[pd.DataFrame], rename_cols: Dict[str, str], time_cols: List[str]
) -> pd.DataFrame:
    """
    Takes a list of DataFrames, concatenates them into a single DataFrame,
    and performs a series of cleaning operations.

    Args:
        df_list (list): List of DataFrames to clean and concatenate.
        rename_cols (dict): Dictionary mapping old column names to new column names.
        time_cols (list): List of columns that contain dates.

    Returns:
        df (DataFrame): Cleaned and concatenated DataFrame.

    Example:
        df_list = [DataFrame1, DataFrame2]
        rename_cols = {'old_name1': 'new_name1', 'old_name2': 'new_name2'}
        time_cols = ['date_column1', 'date_column2']
        cleaning_df(df_list, rename_cols, time_cols)
    """

    # concatenate final list of dataframes
    df = pd.concat(df_list).reset_index(drop=True)

    # make column names pretty
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
    )

    # rename long columns
    df = df.rename(columns=rename_cols)

    # convert to pandas datetime dtype
    df[time_cols] = df[time_cols].apply(
        pd.to_datetime, format="%m/%d/%Y", errors="coerce"
    )

    # unify 'Internal reference UNITY Case Number' columns
    col1, col2 = (
        "internal_reference_unity_case_number_or_report_number",
        "internal_reference_unity_case_number",
    )
    df[col2] = df[col2].fillna(df[col1])

    # drop old 'report number' version of column
    df = df.drop([col1], axis=1)

    # separate DOB & gender into their own columns
    df[['DOB', 'gender']] = df['date_of_birth_and_gender'].apply(parse_dob_gender)

    # sort values by date, newest at top
    df = df.sort_values(by="date", ascending=False).reset_index(drop=True)

    # create zip code, if zip is not a 5 digit integer set to np.nan
    # df['agency_zip'] = df['agency_address'].apply(lambda x: x.split()[-1] if re.match("^\d{5}$", x.split()[-1]) else np.nan)

    # Apply the function to the zip column and create a new column 'city'
    # non-trivial because PDF has a lot of human error so we have to use the zipcodes package
    # df['agency_city'] = df['agency_zip'].apply(get_city_by_zip)

    return df


def run(
    url: str, keys: List[str], rename_cols: Dict[str, str], time_cols: List[str]
) -> None:
    """
    Executes a full run of downloading all PDFs from a provided URL, scraping each PDF for data,
    and finally cleaning and saving the data into a .csv file.

    Args:
        url (str): The URL where the PDFs are located.
        keys (list): List of keys to initialize the dictionary with for data scraping.
        rename_cols (dict): Dictionary mapping old column names to new column names for cleaning the DataFrame.
        time_cols (list): List of columns that contain dates for converting to datetime.

    Example:
        url = 'http://example.com'
        keys = ['key1', 'key2']
        rename_cols = {'old_name1': 'new_name1', 'old_name2': 'new_name2'}
        time_cols = ['date_column1', 'date_column2']
        run(url, keys, rename_cols, time_cols)

    Note:
        This function prints progress messages and saves the final dataframe as a .csv file.
        It also calculates and prints the total execution time.
    """

    # Start the timer
    start_time = time.time()

    # takes about 2 min to download all files from url for Clark County
    save_dir = download_all_pdfs(url)
    print("Done downloading all pdfs")

    # Call the function to create a list of all pdfs from directory
    file_list = list_files(path=save_dir)

    # list all local pdfs
    file_list = list_files(path=save_dir)
    print(len(file_list))

    # scrape each individual pdf from file_list: takes about 35 seconds for Clark County
    df_list = loop_pdf_scrape(file_list, path=save_dir, keys=keys)
    print("Done scraping pdfs")

    # concatenate final list of dataframes, clean, and sort dataframe
    final_df = cleaning_df(df_list, rename_cols, time_cols)
    print(final_df.shape)

    # save final csv per county
    county = url.split("/")[-2]
    csv_filename = f"./output_files/child_fatality_{county}.csv"
    final_df.to_csv(csv_filename, index=False)
    print(f"Saved {csv_filename}")

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Execution time for {county}: {round(elapsed_time,2)} seconds")


if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    import config.CONFIG as CONFIG
    # from config import CONFIG
    # from state.config import CONFIG
    # from state_of_

    # Rural (smallest to debug on)
    run(
        url=CONFIG.URL2,
        keys=CONFIG.KEYS,
        rename_cols=CONFIG.RENAME_COLS,
        time_cols=CONFIG.TIME_COLS,
    )

    # Clark
    # run(url=config.URL1,
    #     keys=config.KEYS,
    #     rename_cols=config.RENAME_COLS,
    #     time_cols=config.TIME_COLS)

    # Washoe
    # run(url=config.URL3,
    #         keys=config.KEYS,
    #         rename_cols=config.RENAME_COLS,
    #         time_cols=config.TIME_COLS)
