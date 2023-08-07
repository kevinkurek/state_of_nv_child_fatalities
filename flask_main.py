import os
import time
from flask import Flask
import config.CONFIG as CONFIG
from scripts.child_fatality_scrape import run

# Create a Flask app
app = Flask(__name__)


@app.route("/")
def main():
    # Start the timer
    start_time = time.time()

    for url in CONFIG.URL_LIST:
        print(f"Getting info from: {url}")
        run(
            url=url,
            keys=CONFIG.KEYS,
            rename_cols=CONFIG.RENAME_COLS,
            time_cols=CONFIG.TIME_COLS,
        )

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Execution time for main.py: {round(elapsed_time,2)} seconds")

    return "Done", 200


if __name__ == "__main__":
    # TODO: Turn into production server after debugging
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
