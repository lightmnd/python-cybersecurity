import json
import csv
import time
from googlesearch import search

# Configuration
DORKS_FILE = "dorks.txt"
JSON_FILE = "dorks_results.json"
CSV_FILE = "dorks_results.csv"
MAX_RESULTS_PER_DORK = 10 # Maximum number of results per dork
DELAY = 3 # Sleep between attempts to avoid rate limiting

# Read the dorks from the txt file
try:
    with open(DORKS_FILE, "r") as file:
        dorks = [line.strip() for line in file if line.strip()]
        print("DORKS -->", dorks)

except FileNotFoundError:
    print("Error: Dorks file not found.")
    exit(1)

# Initialize the results dictionary
results_list = []

# Iterate over each dork
for dork in dorks:
    print(f"Searching for: {dork}")
    dork_results = []

    try:
        for result in search(dork, num_results=MAX_RESULTS_PER_DORK, lang="en"):
            print(result)
            dork_results.append(result)
            time.sleep(DELAY) # Pause to avoid banning

        results_list.extend(dork_results)

    except Exception as e:
        print(f"Error: {e}")

# Save the results to a JSON file
with open(JSON_FILE, "w") as json_file:
    json.dump(results_list, json_file, indent=4)

# Save the results to a CSV file
with open(CSV_FILE, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    for result in results_list:
        writer.writerow([result])


print(f"Results saved to {JSON_FILE} and {CSV_FILE}")
