import time
import pandas as pd
import config.CONFIG as CONFIG
from scripts.child_fatality_scrape import run_pdf_scraping
from scripts.prior_history import run_and_merge_prior_history_counts


# run for Clark, Washoe, and Rural Nevada
def main():
    # Start the timer
    start_time = time.time()

    for url in CONFIG.URL_LIST:
        print(f"Getting info from: {url}")
        run_pdf_scraping(
            url=url,
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
    return_value = main()
    print(return_value)
