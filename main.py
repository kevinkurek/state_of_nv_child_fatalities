import os
import time
import pandas as pd
import config.CONFIG as CONFIG
from scripts.child_fatality_scrape import run_pdf_scraping_URL, run_pdf_scraping_FOLDER
from scripts.prior_history import run_and_merge_prior_history_counts
from dotenv import load_dotenv


# run for Clark, Washoe, and Rural Nevada
def main(URL_based_run=CONFIG.URL_based_run):
    # Start the timer
    start_time = time.time()

    if URL_based_run:
        print("Running main from URLs")
        for url in CONFIG.URL_LIST:
            print(f"Getting info from: {url}")
            run_pdf_scraping_URL(
                url=url,
                keys=CONFIG.KEYS,
                rename_cols=CONFIG.RENAME_COLS,
                time_cols=CONFIG.TIME_COLS,
            )

    else:
        print("Running main from FULL_DATA_PATH")

        for county_folder in CONFIG.FULL_PATH_COUNTIES:
            print(county_folder)
            print(f"Getting info from: {county_folder}")

            run_pdf_scraping_FOLDER(
                county_folder=county_folder,
                keys=CONFIG.KEYS,
                rename_cols=CONFIG.RENAME_COLS,
                time_cols=CONFIG.TIME_COLS,
            )



    # Runs prior history count extraction and merges with csvs from run_pdf_scraping
    run_and_merge_prior_history_counts(directory="./output_files/")

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Execution time for main.py: {round(elapsed_time,2)} seconds")

    return "Done", 200


if __name__ == "__main__":

    # load environment variables
    load_dotenv('.env')

    # run main()
    return_value = main(URL_based_run=CONFIG.URL_based_run)
    print(return_value)
