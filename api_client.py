import requests
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()
base_url = "https://api.adzuna.com/v1/api/jobs"
APP_KEY = os.getenv("APP_KEY")
APP_ID = os.getenv("APP_ID")
data = {"gb": [], "us": [], "pl": []}
for page in range(1,1000):
    for country in data:
        url = f"{base_url}/{country}/search/{page}?app_id={APP_ID}&app_key={APP_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            json_content = response.json()
            offers = json_content.get("results",[])
            data[country].extend(offers)
        else:
            print(f"Error {response.status_code} for {country} on page {page}")
        time.sleep(1)

print("Fetching finished. Now writing to file")
with open("data/raw/raw_json_data_2", 'w') as f:
    json.dump(data,f,indent=4)
print("Finished")