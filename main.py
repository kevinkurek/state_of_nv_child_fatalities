import time
import config
from ChildFatalityScrape import run

# run for Clark, Washoe, and Rural Nevada
def main():
    
    # Start the timer
    start_time = time.time()
    
    for url in config.URL_LIST:
        print(f"Getting info from: {url}")
        run(url=url,
                keys=config.KEYS, 
                rename_cols=config.RENAME_COLS, 
                time_cols=config.TIME_COLS)

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Execution time for main.py: {round(elapsed_time,2)} seconds")
    
    return "Done"
    
if __name__ == "__main__":
    return_value = main()
    print(return_value)